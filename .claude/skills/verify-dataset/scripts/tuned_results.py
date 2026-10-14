"""Tuned results for one dataset: do the methods beat a dummy, do they spread, does one raw feature match them?

Usage::

    python .claude/skills/verify-dataset/scripts/tuned_results.py <unique_name> [--feature auto|<column>]
        [--artifacts ~/.cache/tabarena/artifacts] [--suites beyond_iid_benchmark_2026,beyondarena-2026-09-22,...]

Reads the per-fold results of the TabArena runs cached under ``--artifacts`` (``<suite>/methods/<method>/results/
hpo_results.parquet``; the suites must hold the dataset) and the shipped BeyondArena container the runs used. On the
folds that at least 90% of the methods cover, with one entry per method and configuration (default, and tuned +
ensemble where tuning ran), it prints:

* the dummy on the same shipped splits: ROC AUC 0.5, the train side's class shares for log loss, its mean for RMSE;
* per method: the mean score, its skill against the dummy (``2 AUC - 1``, ``1 - log loss / dummy``,
  ``1 - MSE / dummy MSE``), the folds on which it beats the dummy, and whether it is tied with the best (its paired
  per-fold difference to the best within two standard errors; repeated folds overlap, so read it as a lower bound on
  the ties);
* the agreement of the method ranks across folds (Kendall's W: 0 a new order on every fold, 1 the same order);
* with ``--feature``: the raw feature ranked against the methods, with no model. ``auto`` picks the best single
  feature on each fold's training side (by ROC AUC for a binary task, by R^2 of a monotone fit for regression); a
  column name fixes it. Binary tasks score the column's order, regression a monotone (isotonic) fit on the train side.

The runs used the shipped (format-1) containers; when the v2 definition has changed since (split, columns, scoring),
say so next to the numbers. Fold ``k`` is split ``n_folds * repeat + fold`` of ``experiment_metadata.splits``.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.collections import BEYOND_ARENA
from scipy.stats import rankdata
from sklearn.isotonic import IsotonicRegression
from sklearn.metrics import roc_auc_score

SUITES = "beyond_iid_benchmark_2026,beyondarena-2026-09-22,beyondarena-2026-09-24"
CONFIGS = ("default", "tuned_ensemble")


def load_results(artifacts: Path, suites: list[str], name: str) -> tuple[pd.DataFrame, str]:
    """The per-fold results of ``name`` (as the runs named it: the first 40 characters, a dash and a hash)."""
    frames = [
        pd.read_parquet(f, columns=["dataset", "fold", "method", "metric_error", "metric", "method_subtype"])
        for suite in suites
        for f in sorted((artifacts / suite / "methods").glob("*/results/hpo_results.parquet"))
    ]
    if not frames:
        raise SystemExit(f"no hpo_results.parquet under {artifacts} for the suites {suites}")
    d = pd.concat(frames, ignore_index=True)
    d = d[d.method_subtype.isin(CONFIGS) & ~d.dataset.str.startswith("Task-")]
    stem = d.dataset.str.rsplit("-", n=1).str[0]
    for candidate in (name, f"{name}_1m", name.removesuffix("_1m")):
        hit = d[stem == candidate[:40]]
        if len(hit):
            return hit, candidate
    raise SystemExit(f"{name}: not in the cached results")


def dummy_errors(container, metric: str) -> pd.Series:
    """The dummy's error on every shipped split, indexed like the results' folds."""
    y = container.dataset[container.task_metadata.target_column_name]
    splits = container.experiment_metadata.splits
    n_folds = max(len(f) for f in splits.values())
    out = {}
    for repeat, folds in splits.items():
        for fold, (train, test) in folds.items():
            y_tr, y_te = y.iloc[np.asarray(train)], y.iloc[np.asarray(test)]
            if metric == "roc_auc":
                err = 0.5
            elif metric == "log_loss":
                shares = y_tr.astype(str).value_counts(normalize=True)
                err = float(-np.log(y_te.astype(str).map(shares).fillna(1e-15).clip(1e-15, 1).astype(float)).mean())
            else:
                err = float(np.sqrt(((y_te.astype(float) - y_tr.astype(float).mean()) ** 2).mean()))
            out[n_folds * int(repeat) + int(fold)] = err
    return pd.Series(out)


def skill(err, dummy, metric: str):
    """Skill against the dummy for an error (scalar or Series)."""
    if metric == "roc_auc":
        return 1 - 2 * err
    if metric == "log_loss":
        return 1 - err / dummy
    return 1 - (err / dummy) ** 2


def kendall_w(wide: pd.DataFrame) -> float:
    """Agreement of the method ranks across folds (rows are folds, columns methods)."""
    n, k = wide.shape
    if n < 2 or k < 3:
        return float("nan")
    ranks = np.vstack([rankdata(row) for row in wide.to_numpy()])
    total = ranks.sum(axis=0)
    return float(12 * ((total - total.mean()) ** 2).sum() / (n**2 * (k**3 - k)))


def raw_feature(container, metric: str, folds: list[int], feature: str) -> tuple[pd.Series, pd.Series]:
    """The raw feature's error per fold (as 1 - AUC or RMSE) and the column chosen on each fold's train side."""
    df = container.dataset
    target = container.task_metadata.target_column_name
    X = df.drop(columns=[target]).apply(
        lambda s: s.cat.codes.where(s.cat.codes >= 0) if isinstance(s.dtype, pd.CategoricalDtype) else s
    )
    X = X.apply(pd.to_numeric, errors="coerce").select_dtypes("number")
    if metric == "roc_auc":
        y = (df[target].astype(str) == sorted(df[target].astype(str).unique())[-1]).astype(int).to_numpy()
    else:
        y = df[target].astype(float).to_numpy()
    splits = container.experiment_metadata.splits
    n_folds = max(len(f) for f in splits.values())
    errors, chosen = {}, {}
    for repeat, fs in splits.items():
        for fold, (split_train, split_test) in fs.items():
            k = n_folds * int(repeat) + int(fold)
            if k not in folds:
                continue
            train, test = np.asarray(split_train), np.asarray(split_test)
            filled = X.fillna(X.iloc[train].median())
            if feature != "auto":
                col = feature
            elif metric == "roc_auc":
                col = filled.iloc[train].apply(lambda s, rows=train: abs(roc_auc_score(y[rows], s) - 0.5)).idxmax()
            else:
                col = (
                    filled.iloc[train]
                    .apply(lambda s, rows=train: abs(np.corrcoef(s, y[rows])[0, 1]) if s.std() else 0)
                    .idxmax()
                )
            x = filled[col].to_numpy()
            if metric == "roc_auc":
                sign = 1 if roc_auc_score(y[train], x[train]) >= 0.5 else -1
                errors[k] = 1 - roc_auc_score(y[test], sign * x[test])
            else:
                iso = IsotonicRegression(out_of_bounds="clip", increasing="auto").fit(x[train], y[train])
                errors[k] = float(np.sqrt(((y[test] - iso.predict(x[test])) ** 2).mean()))
            chosen[k] = col
    return pd.Series(errors), pd.Series(chosen)


def main(argv: list[str] | None = None) -> int:
    """Print the tuned results for one dataset; see the module docstring."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("name")
    parser.add_argument("--artifacts", type=Path, default=Path.home() / ".cache" / "tabarena" / "artifacts")
    parser.add_argument("--suites", default=SUITES)
    parser.add_argument("--feature", help="'auto' (chosen per fold) or a column name: rank the raw feature too.")
    args = parser.parse_args(argv)

    results, run_name = load_results(args.artifacts, args.suites.split(","), args.name)
    metric = results.metric.iloc[0]
    wide = results.pivot_table(index="fold", columns="method", values="metric_error")
    per_fold = wide.notna().sum(axis=1)
    wide = wide[per_fold >= 0.9 * per_fold.max()]
    wide = wide.loc[:, wide.notna().all()]
    folds = [int(f) for f in wide.index]
    try:
        container = BEYOND_ARENA.get_dataset(run_name)
    except KeyError:
        container = BEYOND_ARENA.get_dataset(run_name.removesuffix("_1m"))
    dummy = dummy_errors(container, metric).loc[folds]

    means = wide.mean().sort_values()
    best = means.index[0]
    diff = wide.sub(wide[best], axis=0)
    se = diff.std(ddof=1) / np.sqrt(len(diff)) if len(diff) > 1 else diff.std() * np.nan
    shown = "AUC" if metric == "roc_auc" else ("log loss" if metric == "log_loss" else "RMSE")
    table = pd.DataFrame(
        {
            shown: (1 - means) if metric == "roc_auc" else means,
            "skill": skill(means, dummy.mean(), metric),
            "folds above dummy": (wide.lt(dummy, axis=0)).sum().reindex(means.index),
            "tied with best": [m == best or bool(diff[m].mean() < 2 * se[m]) for m in means.index],
        }
    )
    print(f"{args.name} (runs: {run_name}, metric {metric}): {len(folds)} folds, {len(means)} method configurations")
    dummy_shown = 0.5 if metric == "roc_auc" else dummy.mean()
    print(
        f"dummy {shown} {dummy_shown:.4f}; the runs used the shipped container, so check the v2 definition for changes"
    )
    print(table.round(4).to_string())
    tied = int(table["tied with best"].sum()) if len(folds) > 1 else None
    print(
        f"best {best}; median skill {table['skill'].median():+.3f}; tied with the best: "
        + (f"{tied} of {len(means)}" if tied is not None else "one fold, not testable")
        + f"; Kendall's W {kendall_w(wide):.2f}"
    )
    if args.feature:
        if metric == "log_loss":
            print("raw feature: not available for a multiclass task (score its per-class order by hand)")
            return 0
        raw, chosen = raw_feature(container, metric, folds, args.feature)
        raw = raw.loc[folds]
        value = 1 - raw.mean() if metric == "roc_auc" else raw.mean()
        beaten = int((means > raw.mean()).sum())
        above_best = int((raw < wide[best]).sum())
        print(
            f"raw feature ({chosen.value_counts().to_dict()}): {shown} {value:.4f}, skill "
            f"{skill(raw.mean(), dummy.mean(), metric):+.3f}; better than {beaten} of {len(means)} configurations, "
            f"better than the best on {above_best} of {len(folds)} folds"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
