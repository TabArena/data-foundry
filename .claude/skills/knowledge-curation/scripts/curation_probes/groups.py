"""Group probes for a grouped task: does the grouping matter, and is there signal across groups?

Tooling-independent: ``run`` takes a pandas frame, its target column and problem type, the group columns and the
grouped splits (one list of ``(train_idx, test_idx)`` folds per repeat), prints and returns:

* the split gap: untuned LightGBM on 3-fold IID splits (stratified for classification) against the grouped splits of
  the first repeat, with the spread over folds. A clear drop under grouped splits means rows of a group inform each
  other (an IID split would leak); a gap within the fold spread means the grouping changes little;
* learnability across groups: several untuned model families (regularised linear, random forest, LightGBM, kNN) on
  the first ``n_repeats`` repeats, scored on the out-of-fold predictions per row and, for one label per group, per
  group (the mean of a group's predictions), against the baseline of always predicting the prior;
* for one label per group: a permutation test that shuffles the labels across groups and re-runs the grouped CV with
  the best model; its p-value says whether the per-group score could come from chance.

Scores are ROC AUC or R^2; a multiclass ROC AUC is the mean of the one-vs-rest ROC AUCs over the classes present in
the scored rows (a grouped fold can lack a class). Group, target and string columns are not features; categoricals
enter as codes and datetimes as numbers. A frame over ``max_rows`` keeps a random set of whole groups. The numbers are
indicative (untuned models) and meant for the curation decision.
"""

from __future__ import annotations

import lightgbm as lgb
import numpy as np
import pandas as pd
from joblib import Parallel, delayed
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import r2_score, roc_auc_score
from sklearn.model_selection import KFold, StratifiedKFold
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


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


def linear_inputs(categorical: list[str]) -> ColumnTransformer:
    """The linear models' inputs: categories one-hot (64 levels at most, the rarer ones pooled), the rest scaled."""
    return ColumnTransformer(
        [("categories", OneHotEncoder(handle_unknown="infrequent_if_exist", max_categories=64), categorical)],
        remainder=StandardScaler(),
    )


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
    """ROC AUC (for multiclass, the mean one-vs-rest ROC AUC over the classes present in ``y``) or R^2; higher is
    better. NaN for a multiclass ``y`` of one class.
    """
    if not n_classes:
        return float(r2_score(y, pred[:, 0]))
    if n_classes == 2:  # binary
        return float(roc_auc_score(y, pred[:, 1]))
    p = pred.clip(1e-12)
    p = p / p.sum(axis=1, keepdims=True)
    present = np.unique(y)
    return float(np.mean([roc_auc_score(y == k, p[:, k]) for k in present])) if len(present) > 1 else float("nan")


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
    regression = problem_type == "regression"
    labels_of = df[target]
    if regression:
        y, n_classes = labels_of.to_numpy(dtype=float), 0
    else:
        classes = sorted(labels_of.astype(str).unique())
        y, n_classes = labels_of.astype(str).map({c: i for i, c in enumerate(classes)}).to_numpy(), len(classes)
    X = features(df, [target, *group_cols])
    by_group = per_group_labels
    print(
        f"{name}: {len(df):,} rows, {X.shape[1]} features, {len(np.unique(groups)):,} groups, "
        f"{len(repeats)} repeat(s) x {len(repeats[0])} folds; metric {'R^2' if regression else 'ROC AUC'}"
    )
    result: dict = {"name": name, "rows": len(df), "features": X.shape[1], "groups": len(np.unique(groups))}

    lgbm = models(regression=regression)["lightgbm"]
    iid_cv = KFold(3, shuffle=True, random_state=0) if regression else StratifiedKFold(3, shuffle=True, random_state=0)
    iid = [score(y[te], out_of_fold(lgbm, X, y, [(tr, te)], n_classes)[te], n_classes) for tr, te in iid_cv.split(X, y)]
    grouped = [score(y[te], out_of_fold(lgbm, X, y, [(tr, te)], n_classes)[te], n_classes) for tr, te in repeats[0]]
    print(
        f"split gap (LightGBM, per fold): IID {np.mean(iid):.3f} +- {np.std(iid):.3f}, "
        f"grouped {np.mean(grouped):.3f} +- {np.std(grouped):.3f}, gap {np.mean(iid) - np.mean(grouped):.3f}"
    )
    result["split_gap"] = {"iid": iid, "grouped": grouped, "gap": float(np.mean(iid) - np.mean(grouped))}

    baseline = 0.0 if regression else 0.5
    print(f"learnability across groups (baseline {baseline:.1f}), per row" + (" / per group" if by_group else ""))
    categorical = [
        f"f{i}"
        for i, column in enumerate(
            df.drop(columns=[target, *group_cols]).select_dtypes(exclude=["string", "object"]).columns
        )
        if isinstance(df[column].dtype, pd.CategoricalDtype)
    ]
    candidates = models(regression=regression, categorical=categorical)
    results = Parallel(n_jobs=min(n_jobs, len(candidates)))(
        delayed(evaluate)(make, X, y, groups, repeats, n_classes, by_group=by_group) for make in candidates.values()
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
            candidates[best], X, permuted.loc[groups].to_numpy(), groups, repeats, n_classes, by_group=True
        )[1]

    null = np.array(Parallel(n_jobs=n_jobs)(delayed(shuffled)(s) for s in range(permutations)))
    p_value = (1 + (null >= real).sum()) / (1 + len(null))
    print(
        f"permutation test ({best}, labels shuffled across groups, {len(null)} runs): per-group score {real:.3f}, "
        f"null mean {null.mean():.3f}, null 95% quantile {np.quantile(null, 0.95):.3f}, p = {p_value:.3f}"
    )
    result["permutation"] = {"model": best, "score": real, "null_mean": float(null.mean()), "p_value": p_value}
    return result
