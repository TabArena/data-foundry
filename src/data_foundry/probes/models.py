"""The models the probes fit: one place for the families, LightGBM's settings and the foundation-model wrappers.

* ``fit``: a fit with the task's training weight as each row's weight (a model that takes none, such as kNN, is
  fitted without it); ``class_proba`` and ``predict``: class probabilities aligned with all the classes (0 for a class
  the training side lacks), or values.
* ``lightgbm``: untuned LightGBM, the probes' quick model (200 trees unless set); ``bagged``: untuned LightGBM that
  bags rows, so that seeds differ (probes 22 and 23), and ``regularised``: probe 23's settings for it.
* ``families``: the untuned model families of the task and group probes: a regularised linear model, a random forest
  and LightGBM; on wide data (more than ``WIDE_INPUTS`` inputs) ``selected_linear``, and with ``knn`` a 5-nearest-
  neighbour model on the scaled inputs.
* ``tabpfn_v35`` and ``kumo_tabular``: the state-of-the-art tabular foundation models a time basis quotes (SPLIT-32),
  as a ``Foundation``; both need optional packages and a GPU node.

Every model here takes numbers or categories as ``encode`` gives them; the families read ``encode.numeric``.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import lightgbm as lgb
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.feature_selection import SelectKBest, f_classif, f_regression
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.utils.validation import has_fit_parameter

WIDE_INPUTS = 1_000
"""Above this many model inputs the families add ``selected_linear``."""
SELECTED_INPUTS = 500
"""The inputs ``selected_linear`` keeps, chosen by a univariate F-test on each train side."""

Foundation = Callable[[pd.DataFrame, np.ndarray, pd.DataFrame, int], np.ndarray]
"""``fit_predict(x_train, y_train, x_test, seed)``: values, or class probabilities in the order of the classes."""


def fit(model: Any, X: pd.DataFrame, y: np.ndarray, weight: np.ndarray | None = None) -> Any:
    """Fit ``model`` with ``weight`` as each row's weight; a pipeline passes it to its last step. Without a weight, or
    for a model that takes none (kNN), the fit is unweighted.
    """
    final = model.steps[-1][1] if isinstance(model, Pipeline) else model
    if weight is None or not has_fit_parameter(final, "sample_weight"):
        return model.fit(X, y)
    if isinstance(model, Pipeline):
        return model.fit(X, y, **{f"{model.steps[-1][0]}__sample_weight": weight})
    return model.fit(X, y, sample_weight=weight)


def class_proba(model: Any, data: pd.DataFrame, classes: Any) -> np.ndarray:
    """The model's class probabilities, one column per entry of ``classes`` (0 for a class it was not trained on)."""
    out = np.zeros((len(data), len(classes)))
    position = {c: i for i, c in enumerate(classes)}
    out[:, [position[c] for c in model.classes_]] = model.predict_proba(data)
    return out


def predict(model: Any, X: pd.DataFrame, n_classes: int) -> np.ndarray:
    """Class probabilities for labels coded ``0 .. n_classes - 1`` (``class_proba``), or values (``n_classes=0``)."""
    if not n_classes:
        return model.predict(X)
    return class_proba(model, X, range(n_classes))


def lightgbm(*, regression: bool, n_jobs: int, n_estimators: int = 200, **params: Any) -> lgb.LGBMModel:
    """Untuned LightGBM with ``n_estimators`` trees; ``params`` are passed on."""
    model = lgb.LGBMRegressor if regression else lgb.LGBMClassifier
    return model(n_estimators=n_estimators, verbose=-1, n_jobs=n_jobs, **params)


def bagged(*, regression: bool, seed: int, n_estimators: int, n_jobs: int, params: dict | None = None) -> lgb.LGBMModel:
    """Untuned LightGBM that bags rows, so that the seeds differ; ``params`` are passed on and win over these
    settings. Every tree sees every column: with column sampling, dropping one column would change which columns the
    other trees see.
    """
    settings = {"learning_rate": 0.05, "subsample": 0.8, "subsample_freq": 1, "random_state": seed}
    return lightgbm(regression=regression, n_jobs=n_jobs, n_estimators=n_estimators, **{**settings, **(params or {})})


def regularised(rows: int) -> dict:
    """Probe 23's LightGBM settings: shallow trees with many rows a leaf (a 200th of the ``rows`` it trains on, at
    least 20), a slow rate and an L2 penalty, as the hand-run leak tests of 2026-11-06 and 2026-11-08 had them (300
    rows a leaf on 58,000). An untuned fit can score far below the constant (pricing_game_2016_french_fleet: 92.0
    against 82.6 on its deviance), and its overfitting then masks or mimics what the test reads.
    """
    return {"learning_rate": 0.03, "num_leaves": 15, "min_child_samples": max(20, rows // 200), "reg_lambda": 5.0}


def linear_inputs(categorical: list[str]) -> ColumnTransformer:
    """The linear family's inputs: categories one-hot (64 levels at most, the rarer ones pooled), the rest scaled.

    A category's code is no number: read as one, a linear model ranks the levels by their arbitrary order.
    """
    return ColumnTransformer(
        [("categories", OneHotEncoder(handle_unknown="infrequent_if_exist", max_categories=64), categorical)],
        remainder=StandardScaler(),
    )


def families(
    *, regression: bool, n_jobs: int, categorical: list[str] | None = None, n_inputs: int = 0, knn: bool = False
) -> dict[str, Callable[[], Any]]:
    """The untuned model families, each as a function that makes a fresh model; ``categorical`` names the columns the
    linear family one-hot encodes.

    With more than ``WIDE_INPUTS`` inputs, ``selected_linear`` joins them: the linear model on the
    ``SELECTED_INPUTS`` inputs of the strongest univariate F-test, chosen inside the pipeline on the train side. With
    ``knn``, ``knn5``: five nearest neighbours on the scaled inputs (it takes no row weight).
    """
    categorical = categorical or []
    if regression:
        out = {
            "linear": lambda: make_pipeline(linear_inputs(categorical), Ridge(alpha=1.0)),
            "random_forest": lambda: RandomForestRegressor(
                n_estimators=200, min_samples_leaf=2, max_features="sqrt", n_jobs=n_jobs, random_state=0
            ),
            "lightgbm": lambda: lightgbm(regression=True, n_jobs=n_jobs, n_estimators=300, learning_rate=0.05),
        }
        select, linear = f_regression, lambda: Ridge(alpha=1.0)
        neighbours = KNeighborsRegressor
    else:
        out = {
            "linear": lambda: make_pipeline(linear_inputs(categorical), LogisticRegression(C=1.0, max_iter=2000)),
            "random_forest": lambda: RandomForestClassifier(
                n_estimators=200, min_samples_leaf=2, n_jobs=n_jobs, random_state=0
            ),
            "lightgbm": lambda: lightgbm(regression=False, n_jobs=n_jobs, n_estimators=300, learning_rate=0.05),
        }
        select, linear = f_classif, lambda: LogisticRegression(C=1.0, max_iter=2000)
        neighbours = KNeighborsClassifier
    if n_inputs > WIDE_INPUTS:
        out["selected_linear"] = lambda: make_pipeline(
            linear_inputs(categorical), SelectKBest(select, k=SELECTED_INPUTS), linear()
        )
    if knn:
        out["knn5"] = lambda: make_pipeline(StandardScaler(), neighbours(n_neighbors=5))
    return out


def tabpfn_v35(problem_type: str, classes, *, device: str = "cuda") -> Foundation:
    """TabPFN v3.5 (the public ``tabpfn`` package with the public Hugging Face weights ``Prior-Labs/tabpfn_3_5``) as a
    ``Foundation``: one of the state-of-the-art foundation models a time basis can quote (SPLIT-32).

    Categories go in as their codes, named as categorical features; dates are already days. Classification returns
    the probability columns in the order of ``classes`` (a class missing from a training side scores 0), regression
    the mean. Run it on a GPU, on a node started through SkyPilot: v3.5 on a CPU is refused, as it is too slow there.
    Raises ``ImportError`` without the package.
    """
    if device == "cpu":
        raise ValueError("tabpfn_v35: run TabPFN v3.5 on a GPU (device='cuda'), not on a CPU")
    from tabpfn import TabPFNClassifier, TabPFNRegressor  # noqa: PLC0415 - an optional dependency
    from tabpfn.constants import ModelVersion  # noqa: PLC0415

    regression = problem_type == "regression"
    position = None if regression else {c: i for i, c in enumerate(classes)}

    def fit_predict(x_tr: pd.DataFrame, y_tr: np.ndarray, x_te: pd.DataFrame, seed: int) -> np.ndarray:
        both = pd.concat([x_tr, x_te], ignore_index=True)  # one coding of each category for both sides
        cat_idx, columns = [], {}
        for i, c in enumerate(both.columns):
            s = both[c]
            if isinstance(s.dtype, pd.CategoricalDtype):
                columns[c] = s.cat.codes.astype(float).where(s.notna())
                cat_idx.append(i)
            else:
                columns[c] = pd.to_numeric(s, errors="coerce").astype(float)
        X = pd.DataFrame(columns).to_numpy(dtype=np.float32)
        n = len(x_tr)
        estimator = TabPFNRegressor if regression else TabPFNClassifier
        model = estimator.create_default_for_version(
            ModelVersion.V3_5,
            device=device,
            ignore_pretraining_limits=True,
            random_state=seed,
            categorical_features_indices=cat_idx or None,
        )
        model.fit(X[:n], np.asarray(y_tr))
        if regression:
            return np.asarray(model.predict(X[n:]), dtype=float)
        proba = np.asarray(model.predict_proba(X[n:]), dtype=float)
        out = np.zeros((len(x_te), len(position)))
        for j, c in enumerate(model.classes_):
            out[:, position[c]] = proba[:, j]
        return out

    return fit_predict


def kumo_tabular(
    problem_type: str,
    classes,
    *,
    device: str = "cpu",
    threads: int | None = None,
    num_estimators: int = 8,
    size: str = "large",
    point: str = "mean",
) -> Foundation:
    """NVIDIA's Kumo-Tabular (``structured-data-models``, imported here) as a ``Foundation``: one of the
    state-of-the-art foundation models a time basis can quote (SPLIT-32).

    Classification returns the probability columns in the order of ``classes``; regression the mean (``point="mean"``)
    or the median of its 999 quantiles. A column empty on a training side is left out of that fit. Raises
    ``ImportError`` without the package.
    """
    import sdm  # noqa: PLC0415 - an optional dependency
    import torch  # noqa: PLC0415

    if threads:
        torch.set_num_threads(threads)
    regression = problem_type == "regression"
    model = sdm.models.KumoTabular(size=size, device=device)
    names = None if regression else [str(c) for c in classes]

    def fit_predict(x_tr: pd.DataFrame, y_tr: np.ndarray, x_te: pd.DataFrame, seed: int) -> np.ndarray:
        keep = [c for c in x_tr.columns if x_tr[c].notna().any()]
        both = pd.concat([x_tr[keep], x_te[keep]], ignore_index=True)
        y = pd.Series(np.concatenate([np.asarray(y_tr), np.asarray(y_tr)[:1].repeat(len(x_te))]))
        both["__target__"] = y.to_numpy(dtype=float) if regression else y.astype(str).to_numpy()
        stypes = sdm.infer_stypes(both, overrides={"__target__": "numerical" if regression else "categorical"})
        table = sdm.TableTensor.from_pandas(df=both, stypes=stypes, device=device)
        n = len(x_tr)
        model.fit(
            x=table[:n].drop_columns("__target__"),
            y=table[:n, "__target__"],
            num_estimators=num_estimators,
            generator=torch.Generator().manual_seed(seed),
        )
        pred = model.predict(table[n:].drop_columns("__target__")).to_pandas()
        model.clear()
        if regression:
            q = pred[[c for c in pred.columns if str(c).startswith("q")]].to_numpy(dtype=float)
            return np.median(q, axis=1) if point == "median" else q.mean(axis=1)
        probs = np.column_stack(
            [pred[c].to_numpy(dtype=float) if c in pred.columns else np.zeros(len(pred)) for c in names]
        )
        return probs / np.clip(probs.sum(axis=1, keepdims=True), 1e-12, None)

    return fit_predict
