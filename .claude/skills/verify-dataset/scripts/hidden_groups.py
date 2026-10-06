"""Hidden groups in IID tasks: columns whose repeated values carry the label, and what an IID split gains from them.

Usage::

    python .claude/skills/verify-dataset/scripts/hidden_groups.py <unique_name> ... [--all] [--built] [--jobs 8]
        [--out DIR] [--include-grouped]

An IID split assumes the rows are independent. When many rows share an entity (a patient, a customer, a product)
and the entity carries the label, a random split puts rows of one entity on both sides, and a model can score by
recognising the entity instead of learning the task. This probe looks for such entities among the columns.

1. **Candidates**: columns with repeated values (at least ``MIN_GROUPS`` values, a mean of at least
   ``MIN_MEAN_SIZE`` rows per value, at least ``MIN_REPEATED_SHARE`` of the rows sharing their value with another
   row, no value holding more than ``MAX_TOP_SHARE`` of the rows): categoricals, text and integer-valued numbers.
   Missing values are their own singleton groups.
2. **Memorisation** (``s_id``): each row with a repeated value is predicted by the other rows with that value (a
   leave-one-out group mean, shrunk to the prior), scored as skill (``2 AUC - 1``, macro for multiclass, or
   ``1 - MSE / MSE(mean)``). **Smooth part** (``s_smooth``): LightGBM on that column alone, with the rows of each
   value held out together, so it can only use what the value says about unseen values (an age, a count). The
   difference is what knowing *this* value adds.
3. **Attributes** (``static``): the other columns that are constant within the rows of a value (in at least
   ``STATIC_SHARE`` of the repeated values, against at most ``STATIC_BASELINE`` when the same group sizes are drawn
   at random), and coarser than the candidate (a column with as many values is an alias, such as a code next to
   its title). An entity has attributes (a respondent keeps their age and income across the scenarios); a plain
   category or a design variable (an occupation, an angle of attack) fixes no other column.
4. **Split gap** for the ``N_TESTED`` eligible candidates (below) with the largest ``s_id - s_smooth``: untuned
   LightGBM on all non-text features, 3-fold random split against 3-fold split by the candidate's values
   (stratified for classification), on at most ``MAX_ROWS`` rows (whole groups).
   ``gap = skill(random) - skill(grouped)``. Holding out the values of any useful feature opens a gap, so the gap
   alone does not make an entity.

A candidate is **eligible** when its value carries the label (``s_id - s_smooth >= MIN_IDENTITY``) and it looks
like an entity: at least ``MIN_STATIC`` attributes, or a label that its value nearly fixes (``s_id >= STRONG_ID``:
a molecule's conformations, the samples of one mouse). It is a **hit** when it is eligible, ``gap >= MIN_GAP`` and
``gap >= MIN_RELATIVE_GAP * skill(random)``. A hit is a question, not a verdict: re-split a dataset by a column
only when the context says the rows share an entity that new data would not have (the source describes the column
as an id, or the use case predicts for new entities), or the evidence is very strong; then the use case decides,
not the size of the gap. How to read the output:
``.claude/skills/verify-dataset/references/task_probes.md`` (hidden groups).

``--include-grouped`` also runs the grouped datasets as if they were IID (their known group column is marked):
the positive controls for the thresholds.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1")

import lightgbm as lgb
import numpy as np
import pandas as pd
from data_foundry.schema import as_column_list
from data_foundry.v2 import discover_datasets
from joblib import Parallel, delayed
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import GroupKFold, KFold, StratifiedGroupKFold, StratifiedKFold

sys.path.insert(0, str(Path(__file__).parent))
from task_probes import features, load

MIN_GROUPS = 20
MIN_MEAN_SIZE = 1.5
MIN_REPEATED_SHARE = 0.3
MAX_TOP_SHARE = 0.5
MAX_SCORED = 20
"""Candidates (by ``s_id``) that get the smooth-part model."""
N_TESTED = 3
MAX_ROWS = 100_000
MIN_GAP = 0.02
MIN_RELATIVE_GAP = 0.1
MIN_STATIC = 3
MIN_IDENTITY = 0.1
STRONG_ID = 0.5
STATIC_SHARE = 0.95
STATIC_BASELINE = 0.8
MAX_STATIC_COLUMNS = 200
FOLDS = 3


def constant_share(groups: np.ndarray, codes: np.ndarray) -> float:
    """The share of the groups with at least two rows in which ``codes`` takes one value."""
    order = np.argsort(groups, kind="stable")
    g, c = groups[order], codes[order]
    starts = np.flatnonzero(np.r_[True, g[1:] != g[:-1]])
    sizes = np.diff(np.r_[starts, len(g)])
    same = np.minimum.reduceat(c, starts) == np.maximum.reduceat(c, starts)
    repeated = sizes >= 2
    return float(same[repeated].mean()) if repeated.any() else 0.0


def attributes(
    df: pd.DataFrame, groups: np.ndarray, skip: list[str], rng: np.random.Generator
) -> tuple[list[str], list[str]]:
    """The attributes and the aliases of the groups (see the module docstring); at most ``MAX_STATIC_COLUMNS``
    columns are checked.
    """
    columns = [c for c in df.columns if c not in skip]
    if len(columns) > MAX_STATIC_COLUMNS:
        columns = list(rng.choice(columns, MAX_STATIC_COLUMNS, replace=False))
    shuffled = rng.permutation(groups)
    n_groups = len(np.unique(groups))
    static, aliases = [], []
    for col in columns:
        codes = pd.factorize(df[col], use_na_sentinel=False)[0]
        if constant_share(groups, codes) >= STATIC_SHARE and constant_share(shuffled, codes) <= STATIC_BASELINE:
            (aliases if len(np.unique(codes)) >= n_groups else static).append(col)
    return static, aliases


def skill(y: np.ndarray, pred: np.ndarray, n_classes: int) -> float:
    """``2 AUC - 1`` (macro one-vs-rest for multiclass), or ``1 - MSE / MSE(mean)`` for regression."""
    if n_classes == 0:
        dummy = float(np.mean((y - y.mean()) ** 2))
        return float("nan") if dummy == 0 else 1.0 - float(np.mean((y - pred) ** 2)) / dummy
    present = np.unique(y)
    if len(present) < 2:
        return float("nan")
    if n_classes == 2:
        return 2.0 * roc_auc_score(y, pred[:, 1]) - 1.0
    aucs = [roc_auc_score(y == c, pred[:, c]) for c in present]
    return 2.0 * float(np.mean(aucs)) - 1.0


def group_codes(values: pd.Series) -> np.ndarray:
    """Integer group ids; every missing value is its own group."""
    codes = pd.factorize(values, use_na_sentinel=True)[0].astype(np.int64)
    missing = codes < 0
    codes[missing] = codes.max() + 1 + np.arange(missing.sum())
    return codes


def is_candidate(values: pd.Series) -> bool:
    """Repeated values in a categorical, text or integer-valued column (thresholds in the module docstring)."""
    dtype = values.dtype
    if pd.api.types.is_bool_dtype(dtype) or pd.api.types.is_datetime64_any_dtype(dtype):
        return False
    if pd.api.types.is_float_dtype(dtype):
        present = values.dropna().to_numpy()
        if len(present) == 0 or not np.all(np.mod(present, 1) == 0):
            return False
    counts = values.value_counts(dropna=True)
    n = len(values)
    if len(counts) < MIN_GROUPS or n / len(counts) < MIN_MEAN_SIZE:
        return False
    if counts.iloc[0] > MAX_TOP_SHARE * n:
        return False
    return counts[counts >= 2].sum() >= MIN_REPEATED_SHARE * n


def leave_one_out(groups: np.ndarray, y: np.ndarray, n_classes: int) -> tuple[np.ndarray, np.ndarray]:
    """Rows that share their group, and their prediction from the other rows of the group (shrunk to the prior)."""
    sizes = np.bincount(groups)
    rows = np.flatnonzero(sizes[groups] >= 2)
    g, others = groups[rows], sizes[groups[rows]] - 1
    if n_classes == 0:
        sums = np.bincount(groups, weights=y)
        prior = y.mean()
        pred = (sums[g] - y[rows] + prior) / (others + 1)
        return rows, pred
    counts = np.zeros((len(sizes), n_classes))
    np.add.at(counts, (groups, y), 1.0)
    prior = np.bincount(y, minlength=n_classes) / len(y)
    own = np.eye(n_classes)[y[rows]]
    pred = (counts[g] - own + prior) / (others + 1)[:, None]
    return rows, pred


def oof(
    X: pd.DataFrame, y: np.ndarray, n_classes: int, folds: list, n_jobs: int, *, rows: np.ndarray | None = None
) -> tuple[np.ndarray, list[float]]:
    """Out-of-fold predictions of untuned LightGBM, and the skill per fold."""
    pred = np.zeros((len(y), max(n_classes, 1)))
    per_fold = []
    for train, test in folds:
        if n_classes == 0:
            model = lgb.LGBMRegressor(n_estimators=200, verbose=-1, n_jobs=n_jobs)
            model.fit(X.iloc[train], y[train])
            pred[test, 0] = model.predict(X.iloc[test])
        else:
            model = lgb.LGBMClassifier(n_estimators=200, verbose=-1, n_jobs=n_jobs)
            model.fit(X.iloc[train], y[train])
            pred[np.ix_(test, model.classes_)] = model.predict_proba(X.iloc[test])
        part = pred[test, 0] if n_classes == 0 else pred[test]
        per_fold.append(skill(y[test], part, n_classes))
    out = pred[:, 0] if n_classes == 0 else pred
    if rows is not None:
        out = out[rows]
    return out, per_fold


def splits(y: np.ndarray, groups: np.ndarray | None, n_classes: int) -> list:
    """3 folds: random (stratified for classification), or by group when ``groups`` is given."""
    index = np.zeros(len(y))
    if groups is None:
        if n_classes:
            return list(StratifiedKFold(FOLDS, shuffle=True, random_state=0).split(index, y))
        return list(KFold(FOLDS, shuffle=True, random_state=0).split(index, y))
    if n_classes:
        cv = StratifiedGroupKFold(FOLDS, shuffle=True, random_state=0)
        return list(cv.split(index, y, groups))
    return list(GroupKFold(FOLDS, shuffle=True, random_state=0).split(index, y, groups))


def subsample(groups: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Positions of whole groups, in random order, up to ``MAX_ROWS`` rows (all rows when the frame fits)."""
    if len(groups) <= MAX_ROWS:
        return np.arange(len(groups))
    order = rng.permutation(np.unique(groups))
    sizes = np.bincount(groups)[order]
    keep = order[: max(1, int(np.searchsorted(np.cumsum(sizes), MAX_ROWS)))]
    return np.flatnonzero(np.isin(groups, keep))


def probe(name: str, root: Path, *, built: bool, n_jobs: int, include_grouped: bool) -> dict:
    """Run the probe of the module docstring on one dataset."""
    started = time.time()
    container, origin = load(name, root, built=built)
    task, grouping = container.task_metadata, container.grouping
    regime = "temporal" if task.time_on is not None else "grouped" if grouping is not None else "iid"
    result: dict = {"name": name, "regime": regime, "origin": origin}
    if regime == "temporal" or (regime == "grouped" and not include_grouped):
        return result | {"skipped": f"{regime} task"}
    df = container.dataset
    target = df[task.target_column_name]
    if task.problem_type == "regression":
        y, n_classes = target.to_numpy(dtype=float), 0
    else:
        y = pd.factorize(target, sort=True)[0]
        n_classes = int(y.max()) + 1
    known = as_column_list(grouping.on) if grouping is not None else []
    X, names, _ = features(df, [task.target_column_name])
    by_name = dict(zip(names, X.columns, strict=True))
    result |= {"rows": len(df), "known_group_columns": known}

    scored = []
    for col in df.columns:
        if col == task.target_column_name or not is_candidate(df[col]):
            continue
        groups = group_codes(df[col])
        rows, pred = leave_one_out(groups, y, n_classes)
        sizes = np.bincount(groups)
        scored.append(
            {
                "column": col,
                "dtype": str(df[col].dtype),
                "values": int(df[col].nunique()),
                "mean_rows_per_value": round(len(df) / max(df[col].nunique(), 1), 2),
                "repeated_share": round(float(np.mean(sizes[groups] >= 2)), 3),
                "s_id": skill(y[rows], pred, n_classes),
                "known_group": col in known,
                "_groups": groups,
                "_rows": rows,
            }
        )
    scored.sort(key=lambda c: -np.nan_to_num(c["s_id"], nan=-1))
    rng = np.random.default_rng(0)
    for cand in scored[:MAX_SCORED]:
        groups, rows = cand["_groups"], cand["_rows"]
        if cand["column"] not in by_name:  # a text column: no smooth part
            cand["s_smooth"] = 0.0
        else:
            keep = rows if len(rows) <= MAX_ROWS else np.sort(rng.choice(rows, MAX_ROWS, replace=False))
            one = X[[by_name[cand["column"]]]].iloc[keep].reset_index(drop=True)
            pred, _ = oof(one, y[keep], n_classes, splits(y[keep], groups[keep], n_classes), n_jobs)
            cand["s_smooth"] = skill(y[keep], pred, n_classes)
        cand["s_identity"] = cand["s_id"] - cand["s_smooth"]
        static, aliases = attributes(df, groups, [cand["column"], task.target_column_name], rng)
        cand["static"] = len(static)
        cand["static_columns"] = static[:10]
        cand["aliases"] = aliases[:5]
        cand["eligible"] = bool(
            np.nan_to_num(cand["s_identity"], nan=-1) >= MIN_IDENTITY
            and (cand["static"] >= MIN_STATIC or np.nan_to_num(cand["s_id"], nan=-1) >= STRONG_ID)
        )
    ranked = sorted(scored[:MAX_SCORED], key=lambda c: (not c["eligible"], -np.nan_to_num(c["s_identity"], nan=-1)))
    for cand in ranked[:N_TESTED]:
        keep = subsample(cand["_groups"], rng)
        Xs, ys, gs = X.iloc[keep].reset_index(drop=True), y[keep], cand["_groups"][keep]
        _, random_folds = oof(Xs, ys, n_classes, splits(ys, None, n_classes), n_jobs)
        _, group_folds = oof(Xs, ys, n_classes, splits(ys, gs, n_classes), n_jobs)
        cand["skill_random"] = float(np.nanmean(random_folds))
        cand["skill_grouped"] = float(np.nanmean(group_folds))
        cand["gap"] = cand["skill_random"] - cand["skill_grouped"]
        cand["gap_fold_sd"] = float(np.nanstd(np.subtract(random_folds, group_folds)))
        cand["rows_tested"] = len(keep)
        cand["hit"] = bool(
            cand["eligible"] and cand["gap"] >= MIN_GAP and cand["gap"] >= MIN_RELATIVE_GAP * cand["skill_random"]
        )
    for cand in scored:
        cand.pop("_groups"), cand.pop("_rows")
    result["candidates"] = len(scored)
    result["scored"] = ranked
    result["hits"] = [c["column"] for c in ranked if c.get("hit")]
    result["seconds"] = round(time.time() - started)
    return result


def render(result: dict) -> str:
    """A short text summary of one dataset."""
    lines = [f"== {result['name']} ({result['regime']}, {result.get('rows', '?')} rows)"]
    if "skipped" in result or "error" in result:
        return lines[0] + f": {result.get('skipped') or result.get('error')}"
    lines.append(f"   candidates {result['candidates']}; hits {result['hits']}")
    for c in result["scored"][:N_TESTED]:
        gap = ""
        if "gap" in c:
            gap = f", gap {c['gap']:+.3f} (random {c['skill_random']:.3f}, grouped {c['skill_grouped']:.3f})"
        mark = " [known group]" if c["known_group"] else ""
        lines.append(
            f"   {c['column']}{mark}: {c['values']} values, {c['mean_rows_per_value']} rows each, "
            f"s_id {c['s_id']:.3f}, s_smooth {c['s_smooth']:.3f}, "
            f"{c['static']} attributes {c['static_columns'][:4]}{gap}"
        )
    return "\n".join(lines)


def _safe(name: str, root: Path, **kwargs) -> dict:
    try:
        return probe(name, root, **kwargs)
    except Exception as error:  # noqa: BLE001 - one failing dataset must not stop a sweep
        return {"name": name, "regime": "?", "error": f"{type(error).__name__}: {error}"[:300]}


def main(argv: list[str] | None = None) -> int:
    """Probe the datasets; see the module docstring."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("names", nargs="*")
    parser.add_argument("--all", action="store_true", help="Probe every definition under --root.")
    parser.add_argument("--root", type=Path, default=Path("datasets/_dev/tabarena-v0pt2"))
    parser.add_argument("--built", action="store_true", help="Read the built containers (README build record).")
    parser.add_argument("--include-grouped", action="store_true", help="Also run grouped tasks (positive controls).")
    parser.add_argument("--n-jobs", type=int, default=4, help="Threads per model.")
    parser.add_argument("--jobs", type=int, default=1, help="Datasets probed in parallel.")
    parser.add_argument("--out", type=Path, help="Write one JSON per dataset and summary.md here.")
    args = parser.parse_args(argv)
    names = sorted(discover_datasets(args.root)) if args.all else args.names
    if not names:
        parser.error("name at least one dataset, or pass --all")
    kwargs = {"built": args.built, "n_jobs": args.n_jobs, "include_grouped": args.include_grouped}
    results = Parallel(n_jobs=args.jobs)(delayed(_safe)(n, args.root, **kwargs) for n in names)
    for result in results:
        print(render(result))
    if args.out:
        args.out.mkdir(parents=True, exist_ok=True)
        for result in results:
            (args.out / f"{result['name']}.json").write_text(json.dumps(result, indent=1, default=str))
        rows = [
            f"| `{r['name']}` | {r['regime']} | {r.get('candidates', '')} | {', '.join(r.get('hits', [])) or ''} | "
            + (
                f"{r['scored'][0]['column']} gap {r['scored'][0].get('gap', float('nan')):+.3f}"
                if r.get("scored")
                else r.get("skipped") or r.get("error", "")
            )
            + " |"
            for r in results
        ]
        header = "| dataset | regime | candidates | hits | top candidate |\n|---|---|---|---|---|\n"
        (args.out / "summary.md").write_text(header + "\n".join(rows) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
