"""Group probes for a grouped task: does the grouping matter, and is there signal across groups?

Tooling-independent: ``run`` takes a pandas frame, its target column and problem type, the group columns and the
grouped splits (one list of ``(train_idx, test_idx)`` folds per repeat), prints and returns:

* the split gap: untuned LightGBM on 3-fold IID splits (stratified for classification) against the grouped splits of
  the first repeat, with the spread over folds. A clear drop under grouped splits means rows of a group inform each
  other (an IID split would leak); a gap within the fold spread means the grouping changes little;
* learnability across groups: several untuned model families (regularised linear, random forest, LightGBM, kNN) on
  the first ``n_repeats`` repeats, scored on the out-of-fold predictions per row and, for one label per group, per
  group (the mean of a group's predictions), against the baseline of always predicting the prior; only the rows some
  fold of the repeat tests are scored (a holdout or a row budget leaves rows untested);
* for one label per group: a permutation test that shuffles the labels across groups and re-runs the grouped CV with
  the best model; its p-value says whether the per-group score could come from chance.

Scores are ROC AUC or R^2; a multiclass ROC AUC is the mean of the one-vs-rest ROC AUCs over the classes present in
the scored rows (a grouped fold can lack a class). Group, target and string columns are not features, nor the columns
``feature_cols`` leaves out; the inputs are those of the task probes (``curation_probes.text.features``: categoricals
as codes, datetimes and durations as seconds). A frame over ``max_rows`` keeps a random set of whole groups. The
numbers are indicative (untuned models) and meant for the curation decision.

With a training weight (``sample_weight``, such as the years insured of a claims-per-year target), every model is
fitted with it as each row's weight (kNN takes none and is fitted without it) and every score weights the rows by it,
a group by the sum of its rows' weights.
"""

from __future__ import annotations

import lightgbm as lgb
import numpy as np
import pandas as pd
from joblib import Parallel, delayed
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import r2_score, roc_auc_score
from sklearn.model_selection import KFold, StratifiedKFold
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from curation_probes import weights
from curation_probes.task import linear_inputs
from curation_probes.text import features


def models(*, regression: bool, categorical: list[str] | None = None) -> dict:
    """Untuned models of four families; ``categorical`` names the columns the linear models one-hot encode."""
    categorical = categorical or []
    if regression:
        return {
            "ridge": lambda: make_pipeline(linear_inputs(categorical), Ridge(alpha=1.0)),
            "random_forest": lambda: RandomForestRegressor(
                n_estimators=300, min_samples_leaf=2, n_jobs=1, random_state=0
            ),
            "lightgbm": lambda: lgb.LGBMRegressor(n_estimators=300, learning_rate=0.05, verbose=-1, n_jobs=1),
            "knn5": lambda: make_pipeline(StandardScaler(), KNeighborsRegressor(n_neighbors=5)),
        }
    return {
        "logreg": lambda: make_pipeline(linear_inputs(categorical), LogisticRegression(C=0.1, max_iter=5000)),
        "random_forest": lambda: RandomForestClassifier(n_estimators=300, n_jobs=1, random_state=0),
        "lightgbm": lambda: lgb.LGBMClassifier(n_estimators=300, learning_rate=0.05, verbose=-1, n_jobs=1),
        "knn5": lambda: make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=5)),
    }


def out_of_fold(
    make, X: pd.DataFrame, y: np.ndarray, folds: list, n_classes: int, weight: np.ndarray | None = None
) -> np.ndarray:
    """Out-of-fold predictions of one repeat: class probabilities, or values for regression (``n_classes=0``); each
    model fitted with the rows' ``weight`` when given. A row no fold tests (a holdout, the rows a row budget or a time
    window leaves out) keeps NaN: score only the rows of ``tested``.
    """
    pred = np.full((len(X), max(n_classes, 1)), np.nan)
    for train, test in folds:
        if n_classes:
            pred[test] = 0.0  # a class the training side lacks gets probability 0
        model = weights.fit(make(), X.iloc[train], y[train], weights.take(weight, train))
        if n_classes:
            pred[np.ix_(test, model.classes_)] = model.predict_proba(X.iloc[test])
        else:
            pred[test, 0] = model.predict(X.iloc[test])
    return pred


def score(y: np.ndarray, pred: np.ndarray, n_classes: int, weight: np.ndarray | None = None) -> float:
    """ROC AUC (for multiclass, the mean one-vs-rest ROC AUC over the classes present in ``y``) or R^2, each row
    weighted by ``weight`` when given; higher is better. NaN for a multiclass ``y`` of one class.
    """
    if not n_classes:
        return float(r2_score(y, pred[:, 0], sample_weight=weight))
    if n_classes == 2:  # binary
        return float(roc_auc_score(y, pred[:, 1], sample_weight=weight))
    p = pred.clip(1e-12)
    p = p / p.sum(axis=1, keepdims=True)
    present = np.unique(y)
    if len(present) < 2:
        return float("nan")
    return float(np.mean([roc_auc_score(y == k, p[:, k], sample_weight=weight) for k in present]))


def per_group(
    pred: np.ndarray, y: np.ndarray, groups: np.ndarray, weight: np.ndarray | None = None
) -> tuple[np.ndarray, np.ndarray, np.ndarray | None]:
    """The mean prediction, the label and (with ``weight``) the summed weight of every group (labels are one per
    group).
    """
    frame = pd.DataFrame(pred).assign(_y=y, _g=groups).groupby("_g", sort=True)
    summed = None if weight is None else pd.Series(weight).groupby(groups, sort=True).sum().to_numpy()
    return frame.mean().drop(columns="_y").to_numpy(), frame["_y"].first().to_numpy(), summed


def tested(folds: list, n_rows: int) -> np.ndarray:
    """Whether some fold of one repeat tests each row."""
    mask = np.zeros(n_rows, dtype=bool)
    for _, test in folds:
        mask[np.asarray(test, dtype=int)] = True
    return mask


def evaluate(make, X, y, groups, repeats, n_classes, *, by_group: bool, weight=None) -> tuple[float, float | None]:
    """Mean score over the repeats, per row and (with ``by_group``) per group, on the rows some fold of the repeat
    tests; weighted by ``weight`` when given.
    """
    rows, grouped = [], []
    for folds in repeats:
        seen = tested(folds, len(X))
        pred = out_of_fold(make, X, y, folds, n_classes, weight)[seen]
        w = weights.take(weight, seen)
        rows.append(score(y[seen], pred, n_classes, w))
        if by_group:
            gp, gy, gw = per_group(pred, y[seen], groups[seen], w)
            grouped.append(score(gy, gp, n_classes, gw))
    return float(np.mean(rows)), (float(np.mean(grouped)) if by_group else None)


def run(  # noqa: PLR0913
    df: pd.DataFrame,
    target: str,
    problem_type: str,
    group_cols: list[str],
    splits: list[list],
    *,
    per_group_labels: bool,
    name: str = "dataset",
    n_repeats: int = 3,
    permutations: int = 100,
    max_rows: int = 200_000,
    n_jobs: int = 8,
    sample_weight: np.ndarray | None = None,
    feature_cols: list[str] | tuple[str, ...] | None = None,
) -> dict:
    """Print the probes of the module docstring for one grouped frame and return their numbers.

    Args:
        df: The rows, with the target and the group columns.
        target: The target column.
        problem_type: ``"regression"``, or a classification type.
        group_cols: The group columns (a missing value is a group of its own).
        splits: The grouped splits, one list of ``(train_idx, test_idx)`` row positions per repeat.
        per_group_labels: Whether the label is one per group (adds the per-group scores and the permutation test).
        name: The dataset's name in the first line.
        n_repeats: Repeats to use, from the first.
        permutations: Runs of the permutation test (0 skips it).
        max_rows: Rows kept (whole groups, at random).
        n_jobs: Processes for the model families and the permutation runs.
        sample_weight: The task's training weight, one value per row of ``df`` (never a column of it), or None.
        feature_cols: The model inputs, when not every column but the target and the groups is one (a time column
            that dates the label, the unit of a unit weight).
    """
    groups = df.groupby(group_cols, sort=False, observed=True, dropna=False).ngroup().to_numpy()
    rng = np.random.default_rng(0)
    keep = np.arange(len(df))
    if len(df) > max_rows:  # whole groups, at random
        order = rng.permutation(groups.max() + 1)
        sizes = np.bincount(groups)
        chosen = order[: np.searchsorted(np.cumsum(sizes[order]), max_rows) + 1]
        keep = np.flatnonzero(np.isin(groups, chosen))
    position = np.full(len(df), -1)
    position[keep] = np.arange(len(keep))

    def remap(idx: list[int]) -> np.ndarray:
        mapped = position[np.asarray(idx, dtype=int)]
        return mapped[mapped >= 0]

    repeats = [[(remap(tr), remap(te)) for tr, te in folds] for folds in splits[:n_repeats]]
    df, groups = df.iloc[keep].reset_index(drop=True), groups[keep]
    weight = None if sample_weight is None else np.asarray(sample_weight, dtype=float)[keep]
    regression = problem_type == "regression"
    labels_of = df[target]
    if regression:
        y, n_classes = labels_of.to_numpy(dtype=float), 0
    else:
        classes = sorted(labels_of.astype(str).unique())
        y, n_classes = labels_of.astype(str).map({c: i for i, c in enumerate(classes)}).to_numpy(), len(classes)
    inputs = df[list(feature_cols)] if feature_cols is not None else df.drop(columns=[target, *group_cols])
    X, names, _ = features(inputs, [target, *group_cols])  # string columns are left out
    by_group = per_group_labels
    weighted = ", weighted by the training weight" if weight is not None else ""
    print(
        f"{name}: {len(df):,} rows, {X.shape[1]} features, {len(np.unique(groups)):,} groups, "
        f"{len(repeats)} repeat(s) x {len(repeats[0])} folds; metric {'R^2' if regression else 'ROC AUC'}{weighted}"
    )
    result: dict = {"name": name, "rows": len(df), "features": X.shape[1], "groups": len(np.unique(groups))}
    result["weighted"] = weight is not None

    lgbm = models(regression=regression)["lightgbm"]
    iid_cv = KFold(3, shuffle=True, random_state=0) if regression else StratifiedKFold(3, shuffle=True, random_state=0)

    def fold_score(tr: np.ndarray, te: np.ndarray) -> float:
        pred = out_of_fold(lgbm, X, y, [(tr, te)], n_classes, weight)[te]
        return score(y[te], pred, n_classes, weights.take(weight, te))

    iid = [fold_score(tr, te) for tr, te in iid_cv.split(X, y)]
    grouped = [fold_score(tr, te) for tr, te in repeats[0]]
    print(
        f"split gap (LightGBM, per fold): IID {np.mean(iid):.3f} +- {np.std(iid):.3f}, "
        f"grouped {np.mean(grouped):.3f} +- {np.std(grouped):.3f}, gap {np.mean(iid) - np.mean(grouped):.3f}"
    )
    result["split_gap"] = {"iid": iid, "grouped": grouped, "gap": float(np.mean(iid) - np.mean(grouped))}

    baseline = 0.0 if regression else 0.5
    print(f"learnability across groups (baseline {baseline:.1f}), per row" + (" / per group" if by_group else ""))
    categorical = [f"f{i}" for i, column in enumerate(names) if isinstance(df[column].dtype, pd.CategoricalDtype)]
    candidates = models(regression=regression, categorical=categorical)
    results = Parallel(n_jobs=min(n_jobs, len(candidates)))(
        delayed(evaluate)(make, X, y, groups, repeats, n_classes, by_group=by_group, weight=weight)
        for make in candidates.values()
    )
    for model, (row, grp) in zip(candidates, results, strict=True):
        print(f"  {model:>14}: {row:.3f}" + (f" / {grp:.3f}" if grp is not None else ""))
    result["learnability"] = {m: {"row": r, "group": g} for m, (r, g) in zip(candidates, results, strict=True)}

    if not by_group or permutations <= 0:
        return result
    best = max(candidates, key=lambda n: results[list(candidates).index(n)][1])
    real = results[list(candidates).index(best)][1]
    labels = pd.Series(y).groupby(groups).first()

    def shuffled(seed: int) -> float:
        permuted = pd.Series(np.random.default_rng(seed).permutation(labels.to_numpy()), index=labels.index)
        return evaluate(
            candidates[best],
            X,
            permuted.loc[groups].to_numpy(),
            groups,
            repeats,
            n_classes,
            by_group=True,
            weight=weight,
        )[1]

    null = np.array(Parallel(n_jobs=n_jobs)(delayed(shuffled)(s) for s in range(permutations)))
    p_value = (1 + (null >= real).sum()) / (1 + len(null))
    print(
        f"permutation test ({best}, labels shuffled across groups, {len(null)} runs): per-group score {real:.3f}, "
        f"null mean {null.mean():.3f}, null 95% quantile {np.quantile(null, 0.95):.3f}, p = {p_value:.3f}"
    )
    result["permutation"] = {"model": best, "score": real, "null_mean": float(null.mean()), "p_value": p_value}
    return result
