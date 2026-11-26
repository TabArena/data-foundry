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
* with the task's own metric (``metric``, a dict described in ``data_foundry.probes.scoring``): each baseline's and
  family's score by it on the same test rows, computed as the benchmark does (``metric_mean``; ``declared_metric``
  names the best family by it), and for a metric with a floor (``min_prediction``) the share of the predictions at
  or below the floor (``at_floor_mean``), where a family pays the floor's cost;
* the units of each class in each test fold, in rows (or in groups for a task scored per group).

A task with a training weight (``sample_weight``, such as the years insured of a claims-per-year target) is probed
with it: every model is fitted with it as each row's weight, the dummy and the drift baseline are the weighted mean
(``sum(w * y) / sum(w)``) or the weighted class shares, and every score weights the test rows by it (a group by the
sum of its rows' weights). The class counts of ``few_minority`` stay counts of rows or groups.

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

The flags read the probe's own skill. With a declared metric, ``declared_metric["vs_dummy"]`` gives the best family by
that metric against the dummy, paired by split: the mean gain (positive is better), its standard error, the share of
splits it beats the dummy on, and for a loss the gain relative to the dummy's loss. A count or a rate scored by a
deviance has an R^2 near 0.01 by nature, so ``no_signal`` can come with a real gain on the declared metric (fremtpl2,
bemtpl97, 2026-11-06): the report then names both.

Group and target columns are not features. Text (string) columns enter as 16 TF-IDF + SVD components each, fitted on
the train side (``text=False`` leaves them out; see ``data_foundry.probes.encode``). Categoricals enter as codes and
datetimes as numbers. Each train side is capped at ``max_rows`` rows: the newest rows for a temporal task (a random
sample thins the periods next to the test window, the ones a drifting level is learnt from), else random rows; each
test side at ``max_rows`` random rows (whole groups for a task scored per group). The dummy uses the whole train side.
The numbers are indicative (untuned models); check a flag against tuned methods before acting on it.
"""

from __future__ import annotations

import argparse
import time
from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np
import pandas as pd

from data_foundry.encodings import TEXT_COMPONENTS
from data_foundry.probes import inputs, models, scoring
from data_foundry.probes.encode import MAX_TEXT_COLUMNS, encode_text, numeric

if TYPE_CHECKING:
    import lightgbm as lgb

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
MAX_ROWS = 200_000
"""Rows kept of each train and test side (``cap_train``; the test side at random, or whole groups). Raised from 50,000
on 2026-10-21: mortgage 99 s at 200,000 against 22 min uncapped, with the same flags; g_research_crypto_forecasting_1m
(25 min) and force_2020 (31 min) are the slowest measured, so a sweep with ``--jobs 8`` stays within a few hours."""
N_SINGLE = 5
"""Single-feature candidates per split: the features LightGBM uses most on its train side."""


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


def by_group(frame: pd.DataFrame, aggregation: str, n_classes: int) -> tuple[np.ndarray, np.ndarray]:
    """Group-level predictions and labels from row-level ones (``frame``: predictions, ``_y``, ``_g``, ``_t``)."""
    cols = [c for c in frame.columns if not str(c).startswith("_")]
    if aggregation == "last":
        last = frame.sort_values("_t", kind="stable").groupby("_g", sort=True).tail(1).sort_values("_g")
        return last[cols].to_numpy(), last["_y"].to_numpy()
    grouped = frame.groupby("_g", sort=True)
    if aggregation == "any":
        pred = grouped[cols].max().to_numpy(copy=True)  # a writable copy: pandas 3 may return a read-only view
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


def cap_train(train: np.ndarray, max_rows: int, times: np.ndarray | None, rng: np.random.Generator) -> np.ndarray:
    """At most ``max_rows`` positions of a train side, sorted: the newest rows for a temporal task, else at random.

    On a drifting temporal task a random sample thins the periods next to the test window, the ones a model learns
    the current level from; the newest rows keep them whole (mortgage, 2026-10-21).
    """
    if len(train) <= max_rows:
        return train
    if times is not None:
        return np.sort(train[np.argsort(times[train], kind="stable")[-max_rows:]])
    return np.sort(rng.choice(train, max_rows, replace=False))


def vs_dummy(family: list[dict], dummy: list[dict], sign: float) -> dict[str, float] | None:
    """A family against the dummy on the declared metric, paired by split: the mean gain (``sign`` makes a positive
    gain better), its standard error, the share of splits with a gain, and for a loss (``sign`` -1) the gain relative
    to the dummy's mean loss; None when no split scored both.
    """
    pairs = [(f.get("metric"), d.get("metric")) for f, d in zip(family, dummy, strict=True)]
    gain = np.array([sign * (f - d) for f, d in pairs if f is not None and d is not None], dtype=float)
    gain = gain[np.isfinite(gain)]
    if not len(gain):
        return None
    dummy_loss = np.array([d for f, d in pairs if f is not None and d is not None], dtype=float)
    out = {
        "gain_mean": float(gain.mean()),
        "gain_se": float(gain.std(ddof=1) / np.sqrt(len(gain))) if len(gain) > 1 else 0.0,
        "beats_dummy_share": float((gain > 0).mean()),
    }
    if sign < 0 and np.nanmean(dummy_loss) > 0:
        out["relative_gain"] = float(gain.mean() / np.nanmean(dummy_loss))
    return out


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
    non_features: list[str] | tuple[str, ...] = (),
    n_splits: int | None = None,
    max_rows: int = MAX_ROWS,
    n_jobs: int = 8,
    text: bool = True,
    sample_weight: np.ndarray | None = None,
    metric: dict | None = None,
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
        non_features: Further columns of ``df`` no model reads (a time column that dates the label, which ``time_on``
            may still name to order the rows).
        n_splits: Splits to probe (default: up to 30 for small data, else 5).
        max_rows: Rows kept of each train and test side: the newest rows of a temporal task's train side, else
            random rows (whole groups for the test side of a task scored per group).
        n_jobs: Threads per model.
        text: Encode the text columns (else leave them out).
        sample_weight: The task's training weight, one value per row of ``df`` (never a column of it), or None.
        metric: The task's own metric (see ``data_foundry.probes.scoring``), scored next to the probe's scores, or None.
    """
    regression = problem_type == "regression"
    group_cols = list(group_cols)
    labels_of = df[target]
    classes: pd.Index = pd.Index([])
    if regression:
        y, n_classes = labels_of.to_numpy(dtype=float), 0
    else:
        y, classes = pd.factorize(labels_of, sort=True)
        n_classes = len(classes)
    weight = None if sample_weight is None else np.asarray(sample_weight, dtype=float)
    truth = y if regression else labels_of.to_numpy()  # the target as it ships, for the task's metric
    metric_errors: dict[str, str] = {}  # the first error of the task's metric, per model
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
        train = cap_train(full_train, max_rows, times, rng)
        if len(test) > max_rows and unit == "group":
            chosen = rng.permutation(np.unique(groups[test]))
            sizes = pd.Series(groups[test]).value_counts().reindex(chosen).to_numpy()
            test = test[np.isin(groups[test], chosen[: max(1, np.searchsorted(np.cumsum(sizes), max_rows))])]
        elif len(test) > max_rows:
            test = np.sort(rng.choice(test, max_rows, replace=False))
        pairs.append((train, test, full_train))

    # The model inputs of the rows a model fits or predicts only (the whole train sides feed the constants, which read
    # the target alone): a `_1m` container holds millions of training rows, of which each side keeps `max_rows`.
    used = np.unique(np.concatenate([np.concatenate([train, test]) for train, test, _ in pairs])) if pairs else None
    X, names, text_cols = numeric(df, list(dict.fromkeys([target, *group_cols, *non_features])), rows=used)
    if not text:
        text_cols = []

    def at(rows: np.ndarray) -> np.ndarray:
        """The positions of ``rows`` (positions in ``df``) in ``X``."""
        return np.searchsorted(used, rows) if used is not None else rows

    results: dict[str, list[dict]] = {}
    categorical = [f"f{i}" for i, name in enumerate(names) if isinstance(df[name].dtype, pd.CategoricalDtype)]
    n_inputs = X.shape[1] + TEXT_COMPONENTS * len(text_cols[:MAX_TEXT_COLUMNS])
    candidates = models.families(regression=regression, n_jobs=n_jobs, categorical=categorical, n_inputs=n_inputs)
    chosen_single: list[str] = []
    class_counts: list[np.ndarray] = []  # the units of each class, per probed test fold
    numeric_blocks = {names[i]: [f"f{i}"] for i in range(len(names))}

    def reference_of(rows: np.ndarray) -> np.ndarray:
        return scoring.reference(y, rows, n_classes, weight)

    def record(key: str, y_te: np.ndarray, pred: np.ndarray, ref: np.ndarray, test: np.ndarray) -> None:
        extra: dict[str, float | None] = {}
        if metric is not None:  # the row predictions: the task's scorer aggregates a group itself
            extra["metric"], error = scoring.declared_score(metric, truth[test], pred, test, classes)
            if error:
                metric_errors.setdefault(key, error)
            if metric.get("floor") is not None and not n_classes:
                extra["at_floor"] = scoring.at_floor(pred, metric["floor"])
        w_te = scoring.take(weight, test)
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
            if w_te is not None:  # a group weighs the sum of its rows' weights, in by_group's order
                w_te = pd.Series(w_te).groupby(groups[test], sort=True).sum().to_numpy()
        results.setdefault(key, []).append(scoring.scores(y_te, pred, ref, n_classes, w_te) | extra)

    def make_single() -> lgb.LGBMModel:
        return models.lightgbm(regression=regression, n_jobs=n_jobs)

    for i, (train, test, full_train) in enumerate(pairs):
        ref = reference_of(full_train)
        y_tr, y_te = y[train], y[test]
        w_tr = scoring.take(weight, train)
        X_tr, X_te = X.iloc[at(train)].reset_index(drop=True), X.iloc[at(test)].reset_index(drop=True)
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
            model = models.fit(make(), X_tr, y_tr, w_tr)
            pred = models.predict(model, X_te, n_classes)
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
                w_fit, w_va = scoring.take(w_tr, inner_tr), scoring.take(w_tr, inner_va)
                for block in ranked:
                    cols = blocks[block]
                    model = models.fit(make_single(), X_tr.iloc[inner_tr][cols], y_tr[inner_tr], w_fit)
                    pred = models.predict(model, X_tr.iloc[inner_va][cols], n_classes)
                    inner = scoring.scores(y_tr[inner_va], pred, inner_ref, n_classes, w_va)
                    if np.isfinite(inner["skill"]) and inner["skill"] > best_inner:
                        best_block, best_inner = block, inner["skill"]
            cols = blocks[best_block]
            model = models.fit(make_single(), X_tr[cols], y_tr, w_tr)
            record("single_feature", y_te, models.predict(model, X_te[cols], n_classes), ref, test)
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
    declared = None
    if metric is not None:
        sign = 1.0 if metric["greater_is_better"] else -1.0
        scored = [k for k in family if np.isfinite(table[k].get("metric_mean", np.nan))]
        declared = {
            "name": metric["name"],
            "greater_is_better": bool(metric["greater_is_better"]),
            "floor": metric.get("floor"),
            "best": max(scored, key=lambda k: sign * table[k]["metric_mean"]) if scored else None,
            "errors": metric_errors,
        }
        if declared["best"] is not None:
            declared["vs_dummy"] = vs_dummy(results[declared["best"]], results["dummy"], sign)
    return {
        "problem_type": problem_type,
        "unit": unit if aggregation is None else f"{unit} ({aggregation})",
        "rows": len(df),
        "features": X.shape[1],
        "text_columns": len(text_cols),
        "splits_probed": len(pairs),
        "splits_shipped": len(flat),
        "weighted": weight is not None,
        "declared_metric": declared,
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


# On a dataset: `data-foundry probe task`


def probe(name: str, root: Path, args: argparse.Namespace) -> dict:
    """Run ``run`` on one dataset's shipped splits, with its group and time columns, its training weight and its
    declared metric, and return the numbers and flags.
    """
    started = time.time()
    data = inputs.load(name, root, built=args.built)
    grouping = data.grouping
    features = set(data.features)
    result = run(
        data.df,
        data.target,
        data.problem_type,
        data.flat_splits(),
        group_cols=data.group_cols,
        prediction_unit=grouping.prediction_unit if grouping is not None else "row",
        aggregation=grouping.aggregation if grouping is not None else None,
        group_time_on=grouping.time_on if grouping is not None else None,
        time_on=data.time_on,
        non_features=[c for c in data.df.columns if c not in features],
        n_splits=args.splits,
        max_rows=args.max_rows,
        n_jobs=args.n_jobs,
        text=not args.no_text,
        sample_weight=data.weights,
        metric=data.declared_metric(),
    )
    head = {"name": name, "origin": data.origin, "regime": data.regime, "sample_weight": data.weight_column}
    return head | result | {"seconds": round(time.time() - started)}


def weight_and_metric_lines(result: dict) -> list[str]:
    """The report lines of the training weight and the declared metric (its best family, the folds it failed on)."""
    lines = []
    if result.get("sample_weight"):
        lines.append(f"  every model fitted with `{result['sample_weight']}` as the row weight; every score weighted")
    declared = result.get("declared_metric")
    if declared:
        direction = "higher" if declared["greater_is_better"] else "lower"
        floor = f"; floor {declared['floor']:g}" if declared.get("floor") is not None else ""
        lines.append(
            f"  declared metric {declared['name']} ({direction} is better{floor}): best family {declared['best']}"
        )
        if vs := declared.get("vs_dummy"):
            relative = f", {vs['relative_gain']:.1%} of the dummy's loss" if "relative_gain" in vs else ""
            lines.append(
                f"  on it {declared['best']} beats the dummy on {vs['beats_dummy_share']:.0%} of the splits, by "
                f"{vs['gain_mean']:+.4g} (SE {vs['gain_se']:.2g}{relative})"
            )
        lines += [f"  declared metric failed on {k} (scored NaN): {e}" for k, e in declared["errors"].items()]
    return lines


def score_cells(scores: dict, keys: list[str], declared: dict | None) -> str:
    """One model's mean scores, with the declared metric and the share of predictions at its floor."""
    cells = ", ".join(f"{k} {scores[f'{k}_mean']:.3f}" for k in keys)
    if declared and "metric_mean" in scores:
        cells += f" | {declared['name']} {scores['metric_mean']:.5g}"
    if "at_floor_mean" in scores:
        cells += f", at the floor {scores['at_floor_mean']:.1%}"
    return cells


def render(result: dict) -> str:
    """A short text report of one dataset's probes."""
    if "error" in result:
        return f"{result['name']}: CRASH {result['error']}"
    t = result["scores"]
    keys = [k for k in ("auc", "macro_auc", "log_loss", "r2", "rmse") if f"{k}_mean" in t["dummy"]]
    head = (
        f"{result['name']} ({result['regime']}, {result['problem_type']}, unit {result['unit']}, {result['origin']}): "
        f"{result['rows']:,} rows, {result['features']} features"
        + (f" + {result['text_columns']} text columns" if result["text_columns"] else "")
        + f", {result['splits_probed']} of {result['splits_shipped']} splits, {result['seconds']} s"
    )
    lines = [head, *weight_and_metric_lines(result)]
    for key in ["dummy", "drift", "linear", "selected_linear", "random_forest", "lightgbm", "single_feature"]:
        if key in t:
            cells = score_cells(t[key], keys, result.get("declared_metric"))
            lines.append(f"  {key:>15}: skill {t[key]['skill_mean']:+.3f} +- {t[key]['skill_std']:.3f} | {cells}")
    lines.append(
        f"  best family {result['best']}: beats the dummy on {result['best_beats_dummy_share']:.0%} of the splits, "
        f"standard error of its mean skill {result['best_skill_se']:.3f}"
    )
    if "spread" in t:
        s = t["spread"]
        lines.append(
            f"  spread {s['best']} - {s['worst']}: {s['best_minus_worst']:+.3f} (paired SE {s['paired_se']:.3f})"
        )
    if result["single_feature"]["chosen"]:
        chosen = ", ".join(f"{k!r} {v}x" for k, v in result["single_feature"]["chosen"].items())
        lines.append(f"  single feature chosen per split: {chosen}")
    if result["smallest_class_per_test_fold"] is not None:
        what = "groups" if result["unit"].startswith("group") else "rows"
        lines.append(f"  smallest class in a test fold: {result['smallest_class_per_test_fold']} {what}")
        if few := result.get("few_minority_classes"):
            named = ", ".join(f"{k!r} {v}" for k, v in list(few.items())[:20])
            more = f" and {len(few) - 20} more" if len(few) > 20 else ""
            lines.append(f"  classes under {FEW_MINORITY} {what} in a test fold (smallest count): {named}{more}")
    rules = result.get("flag_rules", {})
    flags = [f"{flag} ({rules[flag]})" if flag in rules else flag for flag in result["flags"]]
    lines.append(f"  flags: {', '.join(flags) or 'none'}")
    vs = (result.get("declared_metric") or {}).get("vs_dummy")
    if "no_signal" in result["flags"] and vs and vs["gain_mean"] > 2 * vs["gain_se"] and vs["beats_dummy_share"] >= 0.8:
        lines.append("  no_signal reads the probe's own skill; on the declared metric the best family beats the dummy")
    return "\n".join(lines)


def summary(results: list[dict]) -> str:
    """``summary.md``: one row per dataset with its best family, skill and flags."""
    rows = [
        f"| `{r['name']}` | {r.get('regime', '')} | {r.get('unit', '')} | {r.get('best', '')} | "
        + (
            f"{r['scores'][r['best']]['skill_mean']:+.3f} | {', '.join(r['flags']) or ''} |"
            if "error" not in r
            else f" | CRASH: {r['error'][:80]} |"
        )
        for r in results
    ]
    header = "| dataset | regime | unit | best model | best skill | flags |\n|---|---|---|---|---|---|\n"
    return header + "\n".join(rows) + "\n"
