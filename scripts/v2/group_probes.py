"""Group probes for one grouped v2 dataset: does the grouping matter, and is there signal across groups?

Usage::

    python scripts/v2/group_probes.py <unique_name> [--root datasets/_dev/tabarena-v0pt2] [--repeats 3]
        [--permutations 100] [--max-rows 200000] [--n-jobs 8]

Prints:

* the split gap: untuned LightGBM on 3-fold IID splits (stratified for classification) against the shipped grouped
  splits of repeat 0, with the spread over folds. A clear drop under grouped splits means rows of a group inform
  each other (an IID split would leak); a gap within the fold spread means the grouping changes little;
* learnability across groups: several untuned model families (regularised linear, random forest, LightGBM, kNN) on
  the first ``--repeats`` shipped repeats, scored on the out-of-fold predictions per row and, for one label per
  group, per group (the mean of a group's predictions), against the baseline of always predicting the prior;
* for one label per group: a permutation test that shuffles the labels across groups and re-runs the grouped CV with
  the best model; its p-value says whether the per-group score could come from chance.

Scores are ROC AUC (one-vs-rest macro for multiclass) or R^2. Group, target and string columns are not features;
categoricals enter as codes and datetimes as numbers. A frame over ``--max-rows`` keeps a random set of whole
groups. The numbers are indicative (untuned models) and meant for the curation decision; how to read them:
``.claude/skills/check-candidate/references/leak_checks.md`` (probe 11).
"""

from __future__ import annotations

import argparse
import os
import sys

os.environ.setdefault("OMP_NUM_THREADS", "1")

import lightgbm as lgb
import numpy as np
import pandas as pd
from data_foundry.schema import as_column_list
from data_foundry.v2 import discover_datasets
from joblib import Parallel, delayed
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import r2_score, roc_auc_score
from sklearn.model_selection import KFold, StratifiedKFold
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def features(df: pd.DataFrame, drop: list[str]) -> pd.DataFrame:
    """Numeric model inputs: categoricals as codes, datetimes as seconds, strings left out, NaN as the median."""
    X = df.drop(columns=drop).select_dtypes(exclude=["string", "object"])
    for col in X.columns:
        if isinstance(X[col].dtype, pd.CategoricalDtype):
            X[col] = X[col].cat.codes.replace(-1, np.nan)
        elif pd.api.types.is_datetime64_any_dtype(X[col]):
            X[col] = X[col].astype("int64") // 10**9
    X = X.astype(float)
    X = X.fillna(X.median()).fillna(0.0)
    X.columns = [f"f{i}" for i in range(X.shape[1])]  # LightGBM rejects some characters in names
    return X


def models(*, regression: bool) -> dict:
    """Untuned models of four families."""
    if regression:
        return {
            "ridge": lambda: make_pipeline(StandardScaler(), Ridge(alpha=1.0)),
            "random_forest": lambda: RandomForestRegressor(
                n_estimators=300, min_samples_leaf=2, n_jobs=1, random_state=0
            ),
            "lightgbm": lambda: lgb.LGBMRegressor(n_estimators=300, learning_rate=0.05, verbose=-1, n_jobs=1),
            "knn5": lambda: make_pipeline(StandardScaler(), KNeighborsRegressor(n_neighbors=5)),
        }
    return {
        "logreg": lambda: make_pipeline(StandardScaler(), LogisticRegression(C=0.1, max_iter=5000)),
        "random_forest": lambda: RandomForestClassifier(n_estimators=300, n_jobs=1, random_state=0),
        "lightgbm": lambda: lgb.LGBMClassifier(n_estimators=300, learning_rate=0.05, verbose=-1, n_jobs=1),
        "knn5": lambda: make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=5)),
    }


def out_of_fold(make, X: pd.DataFrame, y: np.ndarray, folds: list, n_classes: int) -> np.ndarray:
    """Out-of-fold predictions of one repeat: class probabilities, or values for regression (``n_classes=0``)."""
    pred = np.zeros((len(X), max(n_classes, 1)))
    for train, test in folds:
        model = make().fit(X.iloc[train], y[train])
        if n_classes:
            pred[np.ix_(test, model.classes_)] = model.predict_proba(X.iloc[test])
        else:
            pred[test, 0] = model.predict(X.iloc[test])
    return pred


def score(y: np.ndarray, pred: np.ndarray, n_classes: int) -> float:
    """ROC AUC (macro one-vs-rest for multiclass) or R^2; higher is better."""
    if not n_classes:
        return float(r2_score(y, pred[:, 0]))
    if n_classes == 2:  # binary
        return float(roc_auc_score(y, pred[:, 1]))
    p = pred.clip(1e-12)
    return float(roc_auc_score(y, p / p.sum(axis=1, keepdims=True), multi_class="ovr", labels=list(range(n_classes))))


def per_group(pred: np.ndarray, y: np.ndarray, groups: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """The mean prediction and the label of every group (labels are one per group)."""
    frame = pd.DataFrame(pred).assign(_y=y, _g=groups).groupby("_g", sort=True)
    return frame.mean().drop(columns="_y").to_numpy(), frame["_y"].first().to_numpy()


def evaluate(make, X, y, groups, repeats, n_classes, *, by_group: bool) -> tuple[float, float | None]:
    """Mean score over the repeats, per row and (with ``by_group``) per group."""
    rows, grouped = [], []
    for folds in repeats:
        pred = out_of_fold(make, X, y, folds, n_classes)
        rows.append(score(y, pred, n_classes))
        if by_group:
            gp, gy = per_group(pred, y, groups)
            grouped.append(score(gy, gp, n_classes))
    return float(np.mean(rows)), (float(np.mean(grouped)) if by_group else None)


def main(argv: list[str] | None = None) -> int:
    """Print the probes for one dataset; see the module docstring."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("name")
    parser.add_argument("--root", default="datasets/_dev/tabarena-v0pt2")
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--permutations", type=int, default=100)
    parser.add_argument("--max-rows", type=int, default=200_000)
    parser.add_argument("--n-jobs", type=int, default=8)
    args = parser.parse_args(argv)

    ds = discover_datasets(args.root)[args.name]()
    task = ds.task_metadata
    if task.grouping is None:
        print(f"{args.name} is not a grouped task.")
        return 1
    plan = ds.make_splits()
    df = plan.df
    group_cols = as_column_list(task.grouping.on)
    groups = df.groupby(group_cols, sort=False, observed=True, dropna=False).ngroup().to_numpy()
    rng = np.random.default_rng(0)
    keep = np.arange(len(df))
    if len(df) > args.max_rows:  # whole groups, at random
        order = rng.permutation(groups.max() + 1)
        sizes = np.bincount(groups)
        chosen = order[: np.searchsorted(np.cumsum(sizes[order]), args.max_rows) + 1]
        keep = np.flatnonzero(np.isin(groups, chosen))
    position = np.full(len(df), -1)
    position[keep] = np.arange(len(keep))

    def remap(idx: list[int]) -> np.ndarray:
        mapped = position[np.asarray(idx, dtype=int)]
        return mapped[mapped >= 0]

    repeats = [
        [(remap(tr), remap(te)) for tr, te in plan.splits[r].values()] for r in sorted(plan.splits)[: args.repeats]
    ]
    df, groups = df.iloc[keep].reset_index(drop=True), groups[keep]
    regression = task.problem_type == "regression"
    target = df[task.target_column_name]
    if regression:
        y, n_classes = target.to_numpy(dtype=float), 0
    else:
        classes = sorted(target.astype(str).unique())
        y, n_classes = target.astype(str).map({c: i for i, c in enumerate(classes)}).to_numpy(), len(classes)
    X = features(df, [task.target_column_name, *group_cols])
    by_group = task.grouping.labels == "per_group"
    print(
        f"{args.name}: {len(df):,} rows, {X.shape[1]} features, {len(np.unique(groups)):,} groups, "
        f"{len(repeats)} repeat(s) x {len(repeats[0])} folds; metric {'R^2' if regression else 'ROC AUC'}"
    )

    lgbm = models(regression=regression)["lightgbm"]
    iid_cv = KFold(3, shuffle=True, random_state=0) if regression else StratifiedKFold(3, shuffle=True, random_state=0)
    iid = [score(y[te], out_of_fold(lgbm, X, y, [(tr, te)], n_classes)[te], n_classes) for tr, te in iid_cv.split(X, y)]
    grouped = [score(y[te], out_of_fold(lgbm, X, y, [(tr, te)], n_classes)[te], n_classes) for tr, te in repeats[0]]
    print(
        f"split gap (LightGBM, per fold): IID {np.mean(iid):.3f} +- {np.std(iid):.3f}, "
        f"grouped {np.mean(grouped):.3f} +- {np.std(grouped):.3f}, gap {np.mean(iid) - np.mean(grouped):.3f}"
    )

    baseline = 0.0 if regression else 0.5
    print(f"learnability across groups (baseline {baseline:.1f}), per row" + (" / per group" if by_group else ""))
    candidates = models(regression=regression)
    results = Parallel(n_jobs=min(args.n_jobs, len(candidates)))(
        delayed(evaluate)(make, X, y, groups, repeats, n_classes, by_group=by_group) for make in candidates.values()
    )
    for name, (row, grp) in zip(candidates, results, strict=True):
        print(f"  {name:>14}: {row:.3f}" + (f" / {grp:.3f}" if grp is not None else ""))

    if not by_group or args.permutations <= 0:
        return 0
    best = max(candidates, key=lambda n: results[list(candidates).index(n)][1])
    real = results[list(candidates).index(best)][1]
    labels = pd.Series(y).groupby(groups).first()

    def shuffled(seed: int) -> float:
        permuted = pd.Series(np.random.default_rng(seed).permutation(labels.to_numpy()), index=labels.index)
        return evaluate(
            candidates[best], X, permuted.loc[groups].to_numpy(), groups, repeats, n_classes, by_group=True
        )[1]

    null = np.array(Parallel(n_jobs=args.n_jobs)(delayed(shuffled)(s) for s in range(args.permutations)))
    p_value = (1 + (null >= real).sum()) / (1 + len(null))
    print(
        f"permutation test ({best}, labels shuffled across groups, {len(null)} runs): per-group score {real:.3f}, "
        f"null mean {null.mean():.3f}, null 95% quantile {np.quantile(null, 0.95):.3f}, p = {p_value:.3f}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
