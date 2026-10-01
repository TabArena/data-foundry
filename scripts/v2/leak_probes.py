"""Quick leak probes for one v2 dataset: what a model learns from the data that it should not.

Usage::

    python scripts/v2/leak_probes.py <unique_name> [--root datasets/_dev/tabarena-v0pt2] [--splits 3]
        [--max-rows 50000]

Fits untuned LightGBM on the first ``--splits`` shipped splits and prints:

* the score with all features (ROC AUC, one-vs-rest for multiclass, or R^2);
* the score of each feature alone, and of each column's missing-value indicator alone, best first;
* the score without each of the three strongest single features (a drop-one test misses a column that has a
  copy, such as kick's ``WheelType`` and ``WheelTypeID``: drop such columns together);
* the share of test rows whose feature vector has an exact copy in train;
* the 1-nearest-neighbour label agreement (R^2 for regression) for the closest tenth of the test rows and for
  all of them, against chance;
* for a binary target, the ROC AUC of a label-free score: each row's distance to its nearest other row.

String and datetime columns are left out, and train and test rows are capped at ``--max-rows`` each. The
numbers are indicative (untuned models, a few splits) and meant for comparing the shipped data with a
suspected fix. How to read them: ``.claude/skills/check-candidate/references/leak_checks.md``.
"""

from __future__ import annotations

import argparse
import sys

import lightgbm as lgb
import numpy as np
import pandas as pd
from data_foundry.v2 import discover_datasets
from sklearn.metrics import r2_score, roc_auc_score
from sklearn.neighbors import NearestNeighbors


def score(data: pd.DataFrame, y: pd.Series, pairs: list, *, regression: bool) -> float:
    """Mean ROC AUC (one-vs-rest for multiclass) or R^2 of an untuned LightGBM over the split pairs."""
    out = []
    for tr, te in pairs:
        model = (lgb.LGBMRegressor if regression else lgb.LGBMClassifier)(n_estimators=200, verbose=-1, n_jobs=8)
        model.fit(data.iloc[tr], y.iloc[tr])
        if regression:
            out.append(r2_score(y.iloc[te], model.predict(data.iloc[te])))
            continue
        proba = model.predict_proba(data.iloc[te])
        proba = proba[:, 1] if proba.shape[1] == 2 else proba
        out.append(roc_auc_score(y.iloc[te], proba, multi_class="ovr", labels=model.classes_))
    return float(np.mean(out))


def neighbour_space(X: pd.DataFrame) -> np.ndarray:
    """Standardised numeric columns plus one-hot categoricals with at most 50 levels."""
    num = X.select_dtypes("number")
    cats = [c for c in X.columns if c not in num and X[c].nunique() <= 50]
    parts = [((num - num.mean()) / num.std()).fillna(0), pd.get_dummies(X[cats], dummy_na=True) if cats else None]
    return pd.concat(parts, axis=1).to_numpy(dtype=float)


def main(argv: list[str] | None = None) -> int:
    """Print the probes for one dataset; see the module docstring."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("name")
    parser.add_argument("--root", default="datasets/_dev/tabarena-v0pt2")
    parser.add_argument("--splits", type=int, default=3)
    parser.add_argument("--max-rows", type=int, default=50_000)
    args = parser.parse_args(argv)

    ds = discover_datasets(args.root)[args.name]()
    plan = ds.make_splits()
    df, regression = plan.df, ds.problem_type == "regression"
    y = df[ds.target]
    X = df.drop(columns=[ds.target]).select_dtypes(exclude=["string", "object", "datetime"])
    rng = np.random.default_rng(0)
    cap = lambda idx: np.sort(rng.choice(idx, min(len(idx), args.max_rows), replace=False))
    pairs = [(cap(tr), cap(te)) for folds in plan.splits.values() for tr, te in folds.values()][: args.splits]
    fit = lambda data: score(data, y, pairs, regression=regression)

    print(f"{args.name}: {len(df):,} rows, {X.shape[1]} features probed, {len(pairs)} splits")
    print(f"all features: {fit(X):.3f}")
    single = pd.Series({c: fit(X[[c]]) for c in X.columns}).sort_values(ascending=False)
    print("each feature alone:", single.head(8).round(3).to_dict())
    missing = {c: round(fit(X[[c]].isna()), 3) for c in X.columns if X[c].isna().any()}
    print("missing indicator alone:", dict(sorted(missing.items(), key=lambda kv: -kv[1])[:5]))
    for col in single.index[:3]:
        print(f"without {col}: {fit(X.drop(columns=[col])):.3f}")

    tr, te = pairs[0]
    key = pd.util.hash_pandas_object(X, index=False)
    print(f"test rows with an exact feature copy in train: {key.iloc[te].isin(set(key.iloc[tr])).mean():.1%}")
    Z = neighbour_space(X)
    dist, idx = NearestNeighbors(n_neighbors=1).fit(Z[tr]).kneighbors(Z[te])
    nn_y, te_y = y.iloc[tr].to_numpy()[idx[:, 0]], y.iloc[te].to_numpy()
    close = dist[:, 0] <= np.quantile(dist[:, 0], 0.1)
    if regression:
        print(f"1-NN R^2: closest tenth {r2_score(te_y[close], nn_y[close]):.3f}, all {r2_score(te_y, nn_y):.3f}")
        return 0
    chance = (y.value_counts(normalize=True) ** 2).sum()
    agree = nn_y == te_y
    print(f"1-NN label agreement: closest tenth {agree[close].mean():.3f}, all {agree.mean():.3f}, chance {chance:.3f}")
    if y.nunique() == 2:
        rows = np.union1d(tr, te)
        d_all = NearestNeighbors(n_neighbors=2).fit(Z[rows]).kneighbors(Z[rows])[0][:, 1]
        auc = roc_auc_score(y.iloc[rows] == y.cat.categories[1], -d_all)
        print(f"nearest-neighbour distance alone (label-free), AUC: {max(auc, 1 - auc):.3f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
