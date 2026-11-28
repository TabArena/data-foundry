"""The fits of the target that probes 22 and 23 and the stationary-relation test share (``TargetFits``), their model
inputs (``forced_inputs``) and the small statistics their reports print.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from sklearn.metrics import r2_score

from data_foundry.probes import encode, models, scoring

if TYPE_CHECKING:
    import pandas as pd


def spread(values) -> dict:
    """The mean and the SD (ddof 1) of the finite values, and how many there are; NaN where there are too few."""
    v = np.asarray(list(values), dtype=float)
    v = v[np.isfinite(v)]
    return {
        "mean": float(v.mean()) if len(v) else float("nan"),
        "sd": float(v.std(ddof=1)) if len(v) > 1 else float("nan"),
        "runs": len(v),
    }


TO_SHIPPED = {"identity": lambda v: v, "log": np.log, "log1p": np.log1p, "log10": np.log10}


FROM_SHIPPED = {"identity": lambda v: v, "log": np.exp, "log1p": np.expm1, "log10": lambda v: np.power(10.0, v)}
"""A metric's ``target_transform`` (``metric["transform"]``): the scale the target ships on, and back."""


RATE_OBJECTIVES = ("poisson", "tweedie", "gamma")
"""LightGBM objectives of a mean on the original scale: fitted there, the predictions moved to the shipped scale."""


class TargetFits:
    """The fits of the target that probes 22 and 23 share: an untuned LightGBM (``_proxy_model``) trained with each
    row's training weight, scored by the task's metric (else R^2 or ROC AUC, weighted by the training weight).

    ``fit_params`` sets the objective (None for LightGBM's default, L2 or log loss); a mean objective of a regression
    (``RATE_OBJECTIVES``) fits the target on its original scale and sends the prediction back to the shipped one.
    ``sign`` is 1 when the metric's higher is better, else -1; a metric that fails on a fold scores NaN, and its first
    error is kept in ``errors``. ``regularised`` fits with ``_regularised``'s settings (probe 23).
    """

    def __init__(
        self,
        y: pd.Series,
        problem_type: str,
        train_w: np.ndarray | None,
        *,
        metric: dict | None,
        fit_params: dict | None,
        n_estimators: int,
        n_jobs: int,
        regularised: bool = False,
    ) -> None:
        """Hold the target (``y``, its problem type), the training weight ``train_w`` and the fit settings."""
        self.regression = problem_type == "regression"
        self.regularised = regularised
        self.y = y
        self.truth = y.to_numpy(dtype=float) if self.regression else y.to_numpy()
        self.classes = None if self.regression else np.unique(self.truth)
        self.n_classes = 0 if self.regression else len(self.classes)
        self.train_w = np.ones(len(y)) if train_w is None else np.asarray(train_w, dtype=float)
        self.metric, self.fit_params = metric, fit_params
        self.n_estimators, self.n_jobs = n_estimators, n_jobs
        self.sign = 1.0 if metric is None or metric["greater_is_better"] else -1.0
        self.errors: list[str] = []
        # a target shipped on a log scale: a mean objective fits the original scale (the scorer inverts the transform)
        transform = (metric or {}).get("transform") or "identity"
        self.to_shipped, self.from_shipped = TO_SHIPPED[transform], FROM_SHIPPED[transform]
        self.on_original_scale = self.regression and (fit_params or {}).get("objective") in RATE_OBJECTIVES

    def score(self, pred: np.ndarray, rows: np.ndarray) -> float:
        """The metric of ``pred`` (values, or class probabilities in the order of ``classes``) on ``rows``."""
        if self.metric is not None:
            classes = () if self.regression else self.classes
            value, error = scoring.declared_score(self.metric, self.truth[rows], pred, rows, classes)
            if error and error not in self.errors:
                self.errors.append(error)
            return value
        if self.regression:
            return float(r2_score(self.truth[rows], pred, sample_weight=self.train_w[rows]))
        return scoring.auc(self.truth[rows], pred, self.classes, self.train_w[rows])

    def constant(self, tr: np.ndarray, n: int) -> np.ndarray:
        """The weighted dummy of the rows ``tr`` for ``n`` rows: the weighted mean, or the weighted class shares."""
        w = self.train_w[tr]
        if self.regression:
            return np.full(n, np.average(self.truth[tr], weights=w))
        shares = np.array([w[self.truth[tr] == c].sum() for c in self.classes]) / w.sum()
        return np.tile(shares, (n, 1))

    def fit_predict(self, x_tr: pd.DataFrame, x_te: pd.DataFrame, tr: np.ndarray, seed: int) -> np.ndarray:
        """Fit on the rows ``tr`` (``x_tr`` holds their inputs) and predict ``x_te``; with no input, the dummy."""
        if not x_tr.shape[1]:
            return self.constant(tr, len(x_te))
        params = {**models.regularised(len(x_tr)), **(self.fit_params or {})} if self.regularised else self.fit_params
        model = models.bagged(
            regression=self.regression, seed=seed, n_estimators=self.n_estimators, n_jobs=self.n_jobs, params=params
        )
        truth = self.truth[tr]
        if self.on_original_scale:  # the rate itself (a Poisson or Tweedie mean), back on the shipped scale
            models.fit(model, x_tr, self.from_shipped(truth), self.train_w[tr])
            pred = self.to_shipped(np.maximum(model.predict(x_te), 0.0))
            return np.clip(pred, truth.min(), truth.max())
        models.fit(model, x_tr, truth if self.regression else self.y.iloc[tr], self.train_w[tr])
        if self.regression:
            return np.clip(model.predict(x_te), truth.min(), truth.max())
        return models.class_proba(model, x_te, self.classes)


def stat_text(stat: dict, *, signed: bool = False) -> str:
    """A mean and its SD as one cell."""
    mean = f"{stat['mean']:+.4g}" if signed else f"{stat['mean']:.5g}"
    return f"{mean} (SD {stat['sd']:.2g})"


def forced_inputs(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Probe 23's model inputs (``encode.native`` with dates): numbers and categories as they ship, dates as days since
    the earliest (a participant reads the period from them), strings left out; the columns renamed for LightGBM.
    """
    return encode.lightgbm_names(encode.native(df[columns], dates=True))
