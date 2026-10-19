"""Task probes: is the task worth benchmarking, or empty, solved, or the same for every model?

Tooling-independent: ``run`` takes a pandas frame, its target column and problem type, the splits as
``(train_idx, test_idx)`` row positions (IID folds, grouped folds or the newest temporal windows, so the probe follows
the task's regime), the group columns, the time column and how a grouped task is scored. It probes every split up to
30 for a dataset of at most 5,000 scored units (rows, or groups for a task scored per group), else the first 5
(``n_splits`` overrides both), with untuned models:

* baselines: a dummy that predicts the train side's class shares (classification) or mean (regression); for a
  temporal task also a drift baseline, the same from the newest rows of the train side (as many as the test window
  holds, at most a fifth of the train side);
* three model families: a regularised linear model, a random forest and LightGBM (regression predictions are clipped
  to the train side's target range); on wide data (more than 1,000 model inputs) a fourth, ``selected_linear``: the
  500 inputs with the strongest univariate F-test on the train side, then the same linear model, so that a linear
  model is not judged by its fit to tens of thousands of columns;
* the best single feature, chosen on each split's training side: of the five features LightGBM uses most there, the
  one that scores best alone on an inner hold-out of the train side (whole groups for a grouped task, the newest rows
  for a temporal one); it is then refitted on the train side and scored on the test side;
* the scores: ROC AUC (binary), macro ROC AUC and log loss (multiclass), R^2 and RMSE (regression), per row and,
  for a task scored per group (``prediction_unit="group"`` with the aggregation ``mean``, ``any`` or ``last``), per
  group;
* the units of each class in each test fold, in rows (or in groups for a task scored per group).

Every score is also a skill against the dummy, 0 for the dummy and 1 for a perfect model: ``2 AUC - 1`` (binary),
``1 - log loss / dummy log loss`` (multiclass), ``1 - MSE / dummy MSE`` (regression). The flags are questions for the
curator, not verdicts:

* ``no_signal``: the best family's mean skill is not above twice its standard error (nor above 0.02);
* ``solved``: ROC AUC, macro ROC AUC or R^2 of at least 0.995;
* ``no_spread``: the best and the worst family differ by less than twice the standard error of their per-split
  difference (paired by split), or by less than 0.01;
* ``one_feature``: the single feature reaches 95% of the best family's skill, and leaves at most 1.25 times its
  remaining error (``1 - skill``): the models remove less than a fifth of what that feature leaves;
* ``drift_baseline``: for a temporal task, the drift baseline's loss (log loss, or squared error) is within 2% of
  the best family's;
* ``unstable``: the best family beats the dummy on fewer than 80% of the splits, or the standard error of its mean
  skill is above 0.05. For a temporal task the standard error counts only when the best family loses to the dummy on
  a window: windows are not exchangeable, and a level that drifts between them moves every model's skill with the
  dummy's error (paired by window, a model that beats the dummy on every window is not unstable);
* ``few_minority``: a probed test fold holds fewer than 5 rows (or groups) of a class, binary or multiclass; the
  report names each class that falls short with its smallest count in a test fold.

Group and target columns are not features. Text (string) columns enter as 16 TF-IDF + SVD components each, fitted on
the train side (``text=False`` leaves them out; see ``curation_probes.text``). Categoricals enter as codes and
datetimes as numbers. Train and test sides are capped at ``max_rows`` random rows (whole groups for a task scored per
group). The numbers are indicative (untuned models); check a flag against tuned methods before acting on it.
"""

from __future__ import annotations

import lightgbm as lgb
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.feature_selection import SelectKBest, f_classif, f_regression
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import log_loss, roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from curation_probes.text import MAX_TEXT_COLUMNS, TEXT_COMPONENTS, encode_text, features

SOLVED = 0.995
"""ROC AUC, macro ROC AUC or R^2 from which a task counts as solved."""
MIN_SKILL = 0.02
"""A skill below this is no signal, whatever the noise."""
MIN_SPREAD = 0.01
"""A skill spread between the model families below this is no spread, whatever the noise."""
ONE_FEATURE_SHARE = 0.95
"""One feature carries the task when it reaches this share of the best family's skill ..."""
ONE_FEATURE_ROOM = 1.25
"""... and its remaining error is at most this multiple of the best family's."""
UNSTABLE_SHARE = 0.8
"""The best family has to beat the dummy on at least this share of the splits."""
UNSTABLE_SE = 0.05
"""A standard error of the best family's mean skill above this makes the comparison unstable."""
DRIFT_MARGIN = 1.02
"""The drift baseline is as good as the models when its loss is within this factor of the best family's."""
FEW_MINORITY = 5
"""A test fold with fewer rows (or groups) of a class than this cannot score that class."""
SMALL_UNITS = 5_000
"""Up to this many scored units (rows, or groups), every shipped split is probed (at most ``SMALL_SPLITS``)."""
SMALL_SPLITS = 30
DEFAULT_SPLITS = 5
N_SINGLE = 5
"""Single-feature candidates per split: the features LightGBM uses most on its train side."""
WIDE_INPUTS = 1_000
"""Above this many model inputs the probe adds ``selected_linear``."""
SELECTED_INPUTS = 500
"""The inputs ``selected_linear`` keeps, chosen by a univariate F-test on each train side."""


FLAG_RULES = {
    "no_signal": "TP-1, TP-2",
    "solved": "TP-6, TP-4",
    "no_spread": "TP-3",
    "one_feature": "TP-4",
    "drift_baseline": "TP-1, TP-2",
    "unstable": "TP-1, TP-5",
    "few_minority": "TP-5, TP-8",
}
"""The rules of ``task_probes.md`` that answer each flag; its readings, highest rank first, are in ``evidence.md``."""


def linear_inputs(categorical: list[str]) -> ColumnTransformer:
    """The linear family's inputs: categories one-hot (64 levels at most, the rarer ones pooled), the rest scaled.

    A category's code is no number: read as one, a linear model ranks the levels by their arbitrary order.
    """
    return ColumnTransformer(
        [("categories", OneHotEncoder(handle_unknown="infrequent_if_exist", max_categories=64), categorical)],
        remainder=StandardScaler(),
    )


def models(*, regression: bool, n_jobs: int, categorical: list[str] | None = None, n_inputs: int = 0) -> dict:
    """The untuned model families; ``categorical`` names the columns the linear family one-hot encodes.

    With more than ``WIDE_INPUTS`` inputs, ``selected_linear`` joins them: the linear model on the
    ``SELECTED_INPUTS`` inputs of the strongest univariate F-test, chosen inside the pipeline on the train side.
    """
    categorical = categorical or []
    if regression:
        out = {
            "linear": lambda: make_pipeline(linear_inputs(categorical), Ridge(alpha=1.0)),
            "random_forest": lambda: RandomForestRegressor(
                n_estimators=200, min_samples_leaf=2, max_features="sqrt", n_jobs=n_jobs, random_state=0
            ),
            "lightgbm": lambda: lgb.LGBMRegressor(n_estimators=300, learning_rate=0.05, verbose=-1, n_jobs=n_jobs),
        }
        select, linear = f_regression, lambda: Ridge(alpha=1.0)
    else:
        out = {
            "linear": lambda: make_pipeline(linear_inputs(categorical), LogisticRegression(C=1.0, max_iter=2000)),
            "random_forest": lambda: RandomForestClassifier(
                n_estimators=200, min_samples_leaf=2, n_jobs=n_jobs, random_state=0
            ),
            "lightgbm": lambda: lgb.LGBMClassifier(n_estimators=300, learning_rate=0.05, verbose=-1, n_jobs=n_jobs),
        }
        select, linear = f_classif, lambda: LogisticRegression(C=1.0, max_iter=2000)
    if n_inputs > WIDE_INPUTS:
        out["selected_linear"] = lambda: make_pipeline(
            linear_inputs(categorical), SelectKBest(select, k=SELECTED_INPUTS), linear()
        )
    return out


def predict(model, X_test: pd.DataFrame, n_classes: int) -> np.ndarray:
    """Class probabilities aligned to all classes, or values (``n_classes=0``)."""
    if not n_classes:
        return model.predict(X_test)
    out = np.zeros((len(X_test), n_classes))
    out[:, model.classes_] = model.predict_proba(X_test)
    return out


def scores(y: np.ndarray, pred: np.ndarray, reference: np.ndarray, n_classes: int) -> dict[str, float]:
    """The scores of ``pred`` and its skill against the constant ``reference`` (the dummy's prediction)."""
    if not n_classes:
        mse, dummy = float(np.mean((y - pred) ** 2)), float(np.mean((y - reference) ** 2))
        total = float(np.mean((y - y.mean()) ** 2))
        return {
            "rmse": mse**0.5,
            "r2": 1 - mse / total if total else float("nan"),
            "skill": 1 - mse / dummy if dummy else float("nan"),
        }
    labels = list(range(n_classes))
    p = np.clip(pred, 1e-12, 1)
    p = np.round(p / p.sum(axis=1, keepdims=True), 12)  # a constant averaged per group stays a constant
    q = np.clip(np.broadcast_to(reference, p.shape), 1e-12, 1)
    q = q / q.sum(axis=1, keepdims=True)
    present = np.unique(y)
    if n_classes == 2:  # binary
        auc = float(roc_auc_score(y, p[:, 1])) if len(present) == 2 else float("nan")
        return {"auc": auc, "log_loss": float(log_loss(y, p, labels=labels)), "skill": 2 * auc - 1}
    ll, ll_dummy = float(log_loss(y, p, labels=labels)), float(log_loss(y, q, labels=labels))
    auc = float("nan")
    if len(present) > 2:
        sub = p[:, present] / p[:, present].sum(axis=1, keepdims=True)
        auc = float(roc_auc_score(y, sub, multi_class="ovr", labels=list(present)))
    return {"macro_auc": auc, "log_loss": ll, "skill": 1 - ll / ll_dummy if ll_dummy else float("nan")}


def by_group(frame: pd.DataFrame, aggregation: str, n_classes: int) -> tuple[np.ndarray, np.ndarray]:
    """Group-level predictions and labels from row-level ones (``frame``: predictions, ``_y``, ``_g``, ``_t``)."""
    cols = [c for c in frame.columns if not str(c).startswith("_")]
    if aggregation == "last":
        last = frame.sort_values("_t", kind="stable").groupby("_g", sort=True).tail(1).sort_values("_g")
        return last[cols].to_numpy(), last["_y"].to_numpy()
    grouped = frame.groupby("_g", sort=True)
    if aggregation == "any":
        pred = grouped[cols].max().to_numpy()
        if n_classes == 2:  # P(negative) as the complement of the max P(positive)
            pred[:, 0] = 1 - pred[:, 1]
        return pred, grouped["_y"].max().to_numpy()
    return grouped[cols].mean().to_numpy(), grouped["_y"].first().to_numpy()


def inner_holdout(train: np.ndarray, groups: np.ndarray | None, times: np.ndarray | None, seed: int) -> tuple:
    """Positions (within ``train``) of an inner train and validation part: whole groups, the newest rows, or random."""
    n = len(train)
    if groups is not None:
        unique = np.unique(groups[train])
        held = np.random.default_rng(seed).permutation(unique)[: max(1, len(unique) // 4)]
        val = np.isin(groups[train], held)
    elif times is not None:
        val = np.zeros(n, dtype=bool)
        val[np.argsort(times[train], kind="stable")[-max(1, n // 4) :]] = True
    else:
        val = np.zeros(n, dtype=bool)
        val[np.random.default_rng(seed).permutation(n)[: max(1, n // 4)]] = True
    return np.flatnonzero(~val), np.flatnonzero(val)


def run(  # noqa: C901, PLR0912, PLR0913
    df: pd.DataFrame,
    target: str,
    problem_type: str,
    splits: list,
    *,
    group_cols: list[str] | tuple[str, ...] = (),
    prediction_unit: str = "row",
    aggregation: str | None = None,
    group_time_on: str | None = None,
    time_on: str | None = None,
    n_splits: int | None = None,
    max_rows: int = 50_000,
    n_jobs: int = 8,
    text: bool = True,
) -> dict:
    """Run the probes of the module docstring on one frame and return the numbers and flags.

    Args:
        df: The rows, with the target, group and time columns.
        target: The target column.
        problem_type: ``"regression"``, or a classification type.
        splits: ``(train_idx, test_idx)`` row positions, in order; the first ``n_splits`` are probed.
        group_cols: The group columns of a grouped task (not features).
        prediction_unit: ``"group"`` for a task scored per group (one prediction per group), else ``"row"``.
        aggregation: How a task scored per group turns row predictions into one: ``mean``, ``any`` or ``last``.
        group_time_on: The order of the rows inside a group, for ``aggregation="last"``.
        time_on: The time column of a temporal task (adds the drift baseline and a newest-rows inner hold-out).
        n_splits: Splits to probe (default: up to 30 for small data, else 5).
        max_rows: Rows kept (at random; whole groups for a task scored per group) of each train and test side.
        n_jobs: Threads per model.
        text: Encode the text columns (else leave them out).
    """
    regression = problem_type == "regression"
    group_cols = list(group_cols)
    X, names, text_cols = features(df, [target, *group_cols])
    if not text:
        text_cols = []
    labels_of = df[target]
    classes: pd.Index = pd.Index([])
    if regression:
        y, n_classes = labels_of.to_numpy(dtype=float), 0
    else:
        y, classes = pd.factorize(labels_of, sort=True)
        n_classes = len(classes)
    if prediction_unit != "group":
        aggregation = None
    unit = "group" if aggregation in ("mean", "any", "last") else "row"
    groups = df.groupby(group_cols, sort=False, observed=True).ngroup().to_numpy() if group_cols else None
    order = df[group_time_on].to_numpy() if aggregation == "last" else None
    times = df[time_on].to_numpy() if time_on is not None else None

    flat = list(splits)
    if n_splits is None:
        units = len(np.unique(groups)) if unit == "group" else len(df)
        n_splits = min(len(flat), SMALL_SPLITS) if units <= SMALL_UNITS else DEFAULT_SPLITS
    rng = np.random.default_rng(0)
    pairs = []
    for split_train, split_test in flat[:n_splits]:
        full_train, test = np.asarray(split_train), np.asarray(split_test)
        train = full_train
        if len(train) > max_rows:
            train = np.sort(rng.choice(train, max_rows, replace=False))
        if len(test) > max_rows and unit == "group":
            chosen = rng.permutation(np.unique(groups[test]))
            sizes = pd.Series(groups[test]).value_counts().reindex(chosen).to_numpy()
            test = test[np.isin(groups[test], chosen[: max(1, np.searchsorted(np.cumsum(sizes), max_rows))])]
        elif len(test) > max_rows:
            test = np.sort(rng.choice(test, max_rows, replace=False))
        pairs.append((train, test, full_train))

    results: dict[str, list[dict]] = {}
    categorical = [f"f{i}" for i, name in enumerate(names) if isinstance(df[name].dtype, pd.CategoricalDtype)]
    n_inputs = X.shape[1] + TEXT_COMPONENTS * len(text_cols[:MAX_TEXT_COLUMNS])
    candidates = models(regression=regression, n_jobs=n_jobs, categorical=categorical, n_inputs=n_inputs)
    chosen_single: list[str] = []
    class_counts: list[np.ndarray] = []  # the units of each class, per probed test fold
    numeric_blocks = {names[i]: [f"f{i}"] for i in range(len(names))}

    def reference_of(rows: np.ndarray) -> np.ndarray:
        if regression:
            return np.array([y[rows].mean()])
        return (np.bincount(y[rows], minlength=n_classes) / len(rows))[None, :]

    def record(key: str, y_te: np.ndarray, pred: np.ndarray, ref: np.ndarray, test: np.ndarray) -> None:
        if unit == "group":
            frame = pd.DataFrame(pred if n_classes else pred[:, None]).assign(_y=y_te, _g=groups[test])
            if order is not None:
                frame["_t"] = order[test]
            refs = np.broadcast_to(ref, (len(test), max(n_classes, 1)))
            gp, gy = by_group(frame, aggregation, n_classes)
            ref_frame = pd.DataFrame(refs.copy()).assign(_y=y_te, _g=groups[test])
            if order is not None:
                ref_frame["_t"] = order[test]
            gref, _ = by_group(ref_frame, aggregation, n_classes)
            pred, y_te, ref = (gp if n_classes else gp[:, 0]), gy, (gref if n_classes else gref[:, 0])
        results.setdefault(key, []).append(scores(y_te, pred, ref, n_classes))

    def make_single() -> lgb.LGBMModel:
        return (lgb.LGBMRegressor if regression else lgb.LGBMClassifier)(n_estimators=200, verbose=-1, n_jobs=n_jobs)

    for i, (train, test, full_train) in enumerate(pairs):
        ref = reference_of(train)
        y_tr, y_te = y[train], y[test]
        X_tr, X_te = X.iloc[train].reset_index(drop=True), X.iloc[test].reset_index(drop=True)
        text_blocks: dict[str, list[str]] = {}
        if text_cols:
            t_tr, t_te, text_blocks = encode_text(df, text_cols, train, test)
            X_tr, X_te = pd.concat([X_tr, t_tr], axis=1), pd.concat([X_te, t_te], axis=1)
        blocks = numeric_blocks | text_blocks
        if n_classes:
            if unit == "group":
                labels = pd.Series(y_te).groupby(groups[test]).max() if aggregation == "any" else None
                if labels is None:
                    frame = pd.DataFrame({"_y": y_te, "_g": groups[test]})
                    labels = frame.groupby("_g")["_y"].first()
                class_counts.append(np.bincount(labels.to_numpy(), minlength=n_classes))
            else:
                class_counts.append(np.bincount(y_te, minlength=n_classes))
        dummy_pred = np.broadcast_to(ref, (len(test), max(n_classes, 1))).copy()
        record("dummy", y_te, dummy_pred if n_classes else dummy_pred[:, 0], ref, test)
        if times is not None:
            by_time = full_train[np.argsort(times[full_train], kind="stable")]
            newest = by_time[-max(1, min(len(test), len(by_time) // 5)) :]
            drift = np.broadcast_to(reference_of(newest), (len(test), max(n_classes, 1))).copy()
            record("drift", y_te, drift if n_classes else drift[:, 0], ref, test)
        lightgbm = None
        for key, make in candidates.items():
            model = make().fit(X_tr, y_tr)
            pred = predict(model, X_te, n_classes)
            if regression:
                pred = np.clip(pred, y_tr.min(), y_tr.max())
            record(key, y_te, pred, ref, test)
            if key == "lightgbm":
                lightgbm = model

        # The single feature: chosen on this split's training side only.
        if lightgbm is not None and len(blocks) > 1:
            gain = pd.Series(lightgbm.booster_.feature_importance(importance_type="gain"), index=X_tr.columns)
            ranked = sorted(blocks, key=lambda b: -float(gain[blocks[b]].sum()))[:N_SINGLE]
            inner_tr, inner_va = inner_holdout(train, groups, times, seed=i)
            best_block, best_inner = ranked[0], -np.inf
            if len(inner_tr) and len(inner_va):
                inner_ref = reference_of(train[inner_tr])
                for block in ranked:
                    cols = blocks[block]
                    model = make_single().fit(X_tr.iloc[inner_tr][cols], y_tr[inner_tr])
                    inner = scores(
                        y_tr[inner_va], predict(model, X_tr.iloc[inner_va][cols], n_classes), inner_ref, n_classes
                    )
                    if np.isfinite(inner["skill"]) and inner["skill"] > best_inner:
                        best_block, best_inner = block, inner["skill"]
            cols = blocks[best_block]
            model = make_single().fit(X_tr[cols], y_tr)
            record("single_feature", y_te, predict(model, X_te[cols], n_classes), ref, test)
            chosen_single.append(best_block)

    def summary(key: str) -> dict[str, float]:
        frame = pd.DataFrame(results[key])
        out = {f"{k}_mean": float(frame[k].mean()) for k in frame.columns}
        out |= {f"{k}_std": float(frame[k].std(ddof=0)) for k in frame.columns}
        return out

    table = {key: summary(key) for key in results}
    family = [k for k in candidates if k in table]
    best = max(family, key=lambda k: np.nan_to_num(table[k]["skill_mean"], nan=-np.inf))
    best_skill = pd.Series([r["skill"] for r in results[best]])
    se = float(best_skill.std(ddof=1) / np.sqrt(len(best_skill))) if len(best_skill) > 1 else 0.0
    above = float((best_skill > 0).mean())
    flags = []
    if not best_skill.mean() > max(2 * se, MIN_SKILL):
        flags.append("no_signal")
    solved_key = "r2" if regression else ("auc" if n_classes == 2 else "macro_auc")
    if table[best].get(f"{solved_key}_mean", 0) >= SOLVED:
        flags.append("solved")
    if "no_signal" not in flags:
        skills = pd.DataFrame({k: [r["skill"] for r in results[k]] for k in family})
        top, bottom = skills.mean().idxmax(), skills.mean().idxmin()
        diff = skills[top] - skills[bottom]
        paired_se = float(diff.std(ddof=1) / np.sqrt(len(diff))) if len(diff) > 1 else 0.0
        spread = float(diff.mean())
        if not spread > max(2 * paired_se, MIN_SPREAD):
            flags.append("no_spread")
        table["spread"] = {"best_minus_worst": spread, "paired_se": paired_se, "best": top, "worst": bottom}
    single_skill = table.get("single_feature", {}).get("skill_mean")
    if (
        single_skill is not None
        and best_skill.mean() >= 0.1
        and single_skill >= ONE_FEATURE_SHARE * best_skill.mean()
        and (1 - single_skill) <= ONE_FEATURE_ROOM * (1 - best_skill.mean())
    ):
        flags.append("one_feature")
    if "drift" in table:
        loss = "log_loss" if n_classes else "rmse"
        best_loss = min(table[k][f"{loss}_mean"] for k in family)
        drift_loss = table["drift"][f"{loss}_mean"]
        if not n_classes:  # compare squared errors
            best_loss, drift_loss = best_loss**2, drift_loss**2
        if drift_loss <= DRIFT_MARGIN * best_loss:
            flags.append("drift_baseline")
    drift_only = times is not None and above == 1.0  # the skill moves with the dummy's error between windows
    if above < UNSTABLE_SHARE or (se > UNSTABLE_SE and not drift_only):
        flags.append("unstable")
    smallest = np.min(class_counts, axis=0) if class_counts else np.array([], dtype=int)
    few = {str(classes[k]): int(smallest[k]) for k in np.argsort(smallest, kind="stable") if smallest[k] < FEW_MINORITY}
    if few:
        flags.append("few_minority")
    counts = pd.Series(chosen_single).value_counts()
    return {
        "problem_type": problem_type,
        "unit": unit if aggregation is None else f"{unit} ({aggregation})",
        "rows": len(df),
        "features": X.shape[1],
        "text_columns": len(text_cols),
        "splits_probed": len(pairs),
        "splits_shipped": len(flat),
        "scores": table,
        "best": best,
        "best_skill_se": se,
        "best_beats_dummy_share": above,
        "per_split": {
            "best_skill": [round(float(v), 4) for v in best_skill],
            "dummy_loss": [round(float(r["log_loss" if n_classes else "rmse"]), 4) for r in results["dummy"]],
        },
        "single_feature": {"skill": single_skill, "chosen": {str(k): int(v) for k, v in counts.items()}},
        "smallest_class_per_test_fold": int(smallest.min()) if len(smallest) else None,
        "few_minority_classes": few,
        "flags": flags,
        "flag_rules": {flag: FLAG_RULES[flag] for flag in flags},
    }
