"""A self-contained HTML page for looking at one v2 dataset on your own: target, features, correlations and signal.

Usage, from the repository root::

    .venv/bin/python .claude/skills/verify-dataset/scripts/explore_page.py <unique_name>
        [--root datasets/_dev/tabarena-v0pt2] [--built | --shipped] [--out PATH] [--splits N] [--permutations 20]
        [--feature-permutations 5] [--max-rows 20000] [--signal-rows 5000] [--max-detail 3000] [--n-jobs 8]

``--shipped`` reads the shipped BeyondArena container (downloaded once into ``~/.cache/data_foundry``), so the page
works without the raw files; the definition, when there is one, still gives the ``task_summary``.

Writes ``PATH`` (default ``~/.cache/data_foundry/explore/<unique_name>.html``): one file, no server, no network;
open it in a browser. Everything is computed here and embedded, so the page opens at once whatever the dataset's
size.

On the shipped splits (the first ``--splits``: every split up to 10 for at most 5,000 rows, else 3):

* the task, its ``task_summary`` and the split sizes; the classes (or the target's mean) per test fold;
* per feature: type, missing share, distinct values, summary statistics, and the distribution split by class (or
  the target's mean per bin, for regression);
* per feature, how well it predicts the target alone: the feature binned on each split's training side (quantile
  bins, or its levels), each bin's target share (or mean) from the training rows, scored on the test rows. Chosen
  and fitted on the training side only, so ranking the features by it is not a selection effect. The skill is
  ``2 AUC - 1`` (binary), ``1 - log loss / dummy log loss`` (multiclass) or ``1 - MSE / dummy MSE`` (regression), 0
  for the dummy. The same scoring on ``--feature-permutations`` shuffles of the labels gives the noise band
  (features below it are no better than chance) and the best feature's score on each shuffle: picked from many
  features, the best one has to beat that, not 0;
* the most correlated feature pairs (Spearman, on up to 5,000 rows and ``--max-detail`` features);
* the signal check: the three untuned model families of ``task_probes.py`` on the true labels and on
  ``--permutations`` shuffles of them (the same splits each time), with the p-value of each family's mean skill and
  of the best family's. Labels that are constant within the task's groups are shuffled across groups. Train and test
  sides are capped at ``--signal-rows`` random rows. ``--permutations 0`` skips the shuffles.

Text columns are profiled but not modelled. Rows are scored as rows, also for a task scored per group. The numbers
are untuned and indicative, like those of ``task_probes.py``; ``tuned_results.py`` has the benchmark's methods.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.curation_container import CuratedContainer
from data_foundry.schema import as_column_list, resolve_warehouse_dir
from data_foundry.v2 import load_definition, read_report
from joblib import Parallel, delayed

sys.path.insert(0, str(Path(__file__).parent))
from task_probes import features, models, predict, scores

TEMPLATE = Path(__file__).parent.parent / "assets" / "explore_page.html"
SMALL_ROWS = 5_000
SMALL_SPLITS = 10
DEFAULT_SPLITS = 3
N_BINS = 20
"""Quantile bins per numeric feature for its single-feature skill."""
MAX_LEVELS = 50
"""Levels of a categorical feature kept for its single-feature skill; the rest share one bin."""
SMOOTHING = 10.0
"""Pseudo-rows of the training side's overall target share (or mean) added to each bin."""
HIST_BINS = 30
TOP_LEVELS = 20
TOP_PAIRS = 100
CORR_ROWS = 5_000


def clean(value):
    """JSON-safe numbers: NaN and infinities become None, numpy scalars plain Python."""
    if isinstance(value, dict):
        return {str(k): clean(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [clean(v) for v in value]
    if isinstance(value, np.ndarray):
        return clean(value.tolist())
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (float, np.floating)):
        return None if not math.isfinite(value) else round(float(value), 6)
    return value


def kind_of(series: pd.Series) -> str:
    """numeric, categorical, datetime or text."""
    if isinstance(series.dtype, pd.CategoricalDtype) or pd.api.types.is_bool_dtype(series):
        return "categorical"
    if pd.api.types.is_datetime64_any_dtype(series) or isinstance(series.dtype, pd.PeriodDtype):
        return "datetime"
    if pd.api.types.is_numeric_dtype(series):
        return "numeric"
    return "text"


def encode_target(target: pd.Series, *, regression: bool) -> tuple[np.ndarray, list[str], int]:
    """The target as floats (regression) or class codes, the class names, and the number of classes."""
    if regression:
        return target.to_numpy(dtype=float), [], 0
    codes, classes = pd.factorize(target, sort=True)
    return codes, [str(c) for c in classes], len(classes)


def shuffle(y: np.ndarray, groups: np.ndarray | None, rng: np.random.Generator) -> np.ndarray:
    """``y`` shuffled across groups when it is constant within them, else across rows."""
    if groups is not None:
        frame = pd.DataFrame({"y": y, "g": groups})
        per_group = frame.groupby("g")["y"].nunique()
        if (per_group == 1).all():
            first = frame.groupby("g")["y"].first()
            mapping = pd.Series(rng.permutation(first.to_numpy()), index=first.index)
            return mapping.loc[groups].to_numpy()
    return rng.permutation(y)


def predictor_codes(values: np.ndarray, kind: str, train: np.ndarray) -> np.ndarray:
    """Bin ids of every row, from bins fitted on the ``train`` rows; missing values get their own bin (-1)."""
    out = np.full(len(values), -1, dtype=np.int64)
    present = ~pd.isna(values)
    if kind == "categorical":
        codes = values.astype(float)
        tr = codes[train][present[train]]
        if len(tr) == 0:
            return out
        levels, counts = np.unique(tr, return_counts=True)
        keep = levels[np.argsort(-counts)[:MAX_LEVELS]]
        index = {v: i for i, v in enumerate(keep)}
        out[present] = [index.get(v, len(keep)) for v in codes[present]]
        return out
    x = values.astype(float)
    tr = x[train][present[train]]
    if len(tr) == 0:
        return out
    edges = np.unique(np.quantile(tr, np.linspace(0, 1, N_BINS + 1)[1:-1]))
    out[present] = np.searchsorted(edges, x[present], side="right")
    return out


def bin_predictions(codes: np.ndarray, y: np.ndarray, train: np.ndarray, test: np.ndarray, n_classes: int):
    """Each test row's bin target share (or mean) from the training rows, shrunk towards the overall one."""
    tr_codes, te_codes = codes[train] + 1, codes[test] + 1  # bin 0 is missing
    n_bins = int(max(tr_codes.max(initial=0), te_codes.max(initial=0))) + 1
    counts = np.bincount(tr_codes, minlength=n_bins).astype(float)
    if not n_classes:
        prior = float(y[train].mean())
        sums = np.bincount(tr_codes, weights=y[train], minlength=n_bins)
        means = (sums + SMOOTHING * prior) / (counts + SMOOTHING)
        return means[te_codes], np.full(len(test), prior)
    onehot = np.zeros((len(train), n_classes))
    onehot[np.arange(len(train)), y[train]] = 1
    prior = (onehot.sum(0) + 1) / (len(train) + n_classes)
    per_bin = np.zeros((n_bins, n_classes))
    np.add.at(per_bin, tr_codes, onehot)
    shares = (per_bin + SMOOTHING * prior) / (counts[:, None] + SMOOTHING)
    return shares[te_codes], prior[None, :]


def single_feature_skill(values, kind, y, pairs, n_classes) -> list[float]:
    """The feature's test skill alone on each split (see the module docstring)."""
    skills = []
    for train, test in pairs:
        codes = predictor_codes(values, kind, train)
        pred, ref = bin_predictions(codes, y, train, test, n_classes)
        skills.append(scores(y[test], pred, ref, n_classes)["skill"])
    return skills


def histogram(values: np.ndarray, kind: str, y: np.ndarray, n_classes: int) -> dict:
    """The feature's distribution by class (or the target's mean per bin), for the page's drill-down."""
    missing = pd.isna(values)

    def summarize(mask_list: list[np.ndarray]) -> list:
        if n_classes:
            return [np.bincount(y[m], minlength=n_classes).tolist() for m in mask_list]
        return [[int(m.sum()), float(y[m].mean()) if m.any() else None] for m in mask_list]

    miss = summarize([missing])[0] if missing.any() else None
    if kind == "categorical":
        levels = pd.Series(values[~missing]).astype(str)
        top = levels.value_counts().index[:TOP_LEVELS].tolist()
        labels = pd.Series(values).astype(str).to_numpy()
        masks = [(labels == level) & ~missing for level in top]
        rest = ~missing & ~np.isin(labels, top)
        if rest.any():
            top, masks = [*top, "(other)"], [*masks, rest]
        return {"type": "levels", "labels": top, "bins": summarize(masks), "missing": miss}
    x = values.astype(float)
    finite = x[~missing]
    if len(finite) == 0:
        return {"type": "levels", "labels": [], "bins": [], "missing": miss}
    uniques = np.unique(finite)
    if len(uniques) <= HIST_BINS:
        masks = [(x == u) & ~missing for u in uniques]
        return {"type": "levels", "labels": [f"{u:g}" for u in uniques], "bins": summarize(masks), "missing": miss}
    lo, hi = np.quantile(finite, [0.005, 0.995])
    if lo == hi:
        lo, hi = finite.min(), finite.max()
    edges = np.linspace(lo, hi, HIST_BINS + 1)
    idx = np.clip(np.searchsorted(edges, np.where(missing, lo, x), side="right") - 1, 0, HIST_BINS - 1)
    masks = [(idx == i) & ~missing for i in range(HIST_BINS)]
    return {"type": "range", "edges": edges.tolist(), "bins": summarize(masks), "missing": miss}


def profile(series: pd.Series, kind: str) -> dict:
    """Summary statistics of one column."""
    out = {
        "missing": float(series.isna().mean()),
        "unique": int(series.nunique(dropna=True)),
    }
    if kind == "numeric":
        x = series.astype(float)
        out.update(
            {
                "mean": x.mean(),
                "std": x.std(),
                "min": x.min(),
                "q25": x.quantile(0.25),
                "median": x.median(),
                "q75": x.quantile(0.75),
                "max": x.max(),
                "zeros": float((x == 0).mean()),
            }
        )
    elif kind == "datetime":
        x = series.dropna()
        if isinstance(series.dtype, pd.PeriodDtype):
            x = x.dt.to_timestamp()
        out.update({"min": str(x.min()) if len(x) else None, "max": str(x.max()) if len(x) else None})
    else:
        counts = series.astype(str)[series.notna()].value_counts().head(10)
        out["top"] = [[k[:80], int(v)] for k, v in counts.items()]
        if kind == "text":
            out["mean_length"] = float(series.dropna().astype(str).str.len().mean())
    return out


def correlations(X: pd.DataFrame, names: list[str], rng: np.random.Generator) -> dict:
    """The most correlated feature pairs (Spearman) and the count of near-duplicate pairs."""
    rows = rng.choice(len(X), min(len(X), CORR_ROWS), replace=False)
    sub = X.iloc[np.sort(rows)]
    keep = [i for i in range(sub.shape[1]) if (sub.iloc[:, i] != sub.iloc[0, i]).any()]
    if len(keep) < 2:
        return {"pairs": [], "n_features": len(keep), "above_099": 0, "above_09": 0}
    ranks = sub.iloc[:, keep].rank().to_numpy()
    corr = np.corrcoef(ranks, rowvar=False)
    iu = np.triu_indices(len(keep), k=1)
    values = np.abs(corr[iu])
    order = np.argsort(-values)[:TOP_PAIRS]
    pairs = [[names[keep[iu[0][k]]], names[keep[iu[1][k]]], float(corr[iu][k])] for k in order]
    return {
        "pairs": pairs,
        "n_features": len(keep),
        "above_099": int((values >= 0.99).sum()),
        "above_09": int((values >= 0.9).sum()),
    }


def model_skills(X, y, pairs, regression, n_classes, n_jobs) -> dict[str, list[float]]:
    """Each model family's test skill on each split."""
    out = {}
    for name, make in models(regression=regression, n_jobs=n_jobs).items():
        skills = []
        for train, test in pairs:
            model = make().fit(X.iloc[train], y[train])
            pred = predict(model, X.iloc[test], n_classes)
            if regression:
                lo, hi = y[train].min(), y[train].max()
                pred, ref = np.clip(pred, lo, hi), np.full(len(test), y[train].mean())
            else:
                ref = (np.bincount(y[train], minlength=n_classes) / len(train))[None, :]
            skills.append(scores(y[test], pred, ref, n_classes)["skill"])
        out[name] = skills
    return out


def signal_check(X, y, groups, pairs, regression, n_classes, n_permutations, n_jobs) -> dict:
    """The model families on the true labels and on shuffled ones, the same splits each time."""
    true = model_skills(X, y, pairs, regression, n_classes, n_jobs)

    def one(seed: int) -> dict[str, list[float]]:
        y_shuffled = shuffle(y, groups, np.random.default_rng(1000 + seed))
        return model_skills(X, y_shuffled, pairs, regression, n_classes, 1)

    null = Parallel(n_jobs=n_jobs)(delayed(one)(s) for s in range(n_permutations)) if n_permutations else []
    families = {}
    for name, skills in true.items():
        mean = float(np.nanmean(skills))
        null_means = np.array([np.nanmean(n[name]) for n in null])
        null_above = np.array([np.mean(np.array(n[name]) > 0) for n in null])
        families[name] = {
            "skills": skills,
            "mean": mean,
            "above_zero": float(np.mean(np.array(skills) > 0)),
            "null_means": null_means.tolist(),
            "null_q95": float(np.quantile(null_means, 0.95)) if len(null) else None,
            "null_above_q95": float(np.quantile(null_above, 0.95)) if len(null) else None,
            "p": float((1 + np.sum(null_means >= mean)) / (1 + len(null))) if len(null) else None,
        }
    best_true = max(f["mean"] for f in families.values())
    best_null = np.array([max(np.nanmean(n[k]) for k in true) for n in null])
    return {
        "families": families,
        "best": {
            "mean": best_true,
            "null_means": best_null.tolist(),
            "null_q95": float(np.quantile(best_null, 0.95)) if len(null) else None,
            "p": float((1 + np.sum(best_null >= best_true)) / (1 + len(null))) if len(null) else None,
        },
        "n_permutations": n_permutations,
    }


def cap(pairs, max_rows: int, rng: np.random.Generator) -> list[tuple[np.ndarray, np.ndarray]]:
    """The splits with each side capped at ``max_rows`` random rows."""

    def capped(rows: np.ndarray) -> np.ndarray:
        return np.sort(rng.choice(rows, max_rows, replace=False)) if len(rows) > max_rows else rows

    return [(capped(train), capped(test)) for train, test in pairs]


def load(name: str, root: Path, *, built: bool, shipped: bool) -> tuple[CuratedContainer, str, object]:
    """The container of ``name`` (shipped, built, or rebuilt from the definition), where it came from, and the
    definition class (None when there is none). Imports only this dataset's ``dataset.py``, unlike
    ``task_probes.load``.
    """
    definition = root / name / "dataset.py"
    cls = load_definition(definition) if definition.is_file() else None
    if shipped:
        from data_foundry.collections import BEYOND_ARENA  # noqa: PLC0415 - only for --shipped

        return BEYOND_ARENA.get_dataset(name), "shipped BeyondArena", cls
    if cls is None:
        raise SystemExit(f"{name}: no {definition}; pass --root, or --shipped for the BeyondArena container")
    if built:
        build = (read_report(root / name / "README.md") or {}).get("build") or {}
        if build.get("path"):
            return CuratedContainer.load(resolve_warehouse_dir() / build["path"]), "built", cls
    return cls().to_container(), "rebuilt", cls


def group_columns(container: CuratedContainer) -> list[str]:
    """The task's group columns; a format-1 container keeps them in ``task_metadata.group_on``."""
    if getattr(container, "format_version", 2) >= 2:
        grouping = container.grouping
        return as_column_list(grouping.on) if grouping is not None else []
    return as_column_list(getattr(container.task_metadata, "group_on", None) or [])


def task_summary(cls) -> dict | None:
    """The definition's ``task_summary`` fields, for the page's "In brief"."""
    summary = getattr(cls, "task_summary", None)
    if summary is None:
        return None
    fields = ["question", "use_case", "row", "predicted", "known", "split", "fit", "fit_reason"]
    return {f: getattr(summary, f, None) for f in fields}


def build(args: argparse.Namespace) -> dict:  # noqa: C901, PLR0912
    """Everything the page shows, as one JSON-ready dict."""
    rng = np.random.default_rng(0)
    container, origin, cls = load(args.name, args.root, built=args.built, shipped=args.shipped)
    task = container.task_metadata
    df = container.dataset
    target_name = task.target_column_name
    regression = task.problem_type == "regression"
    group_cols = [c for c in group_columns(container) if c in df.columns]
    y, classes, n_classes = encode_target(df[target_name], regression=regression)
    groups = df.groupby(group_cols, sort=False, observed=True).ngroup().to_numpy() if group_cols else None

    flat = [
        (np.asarray(tr), np.asarray(te))
        for folds in container.experiment_metadata.splits.values()
        for tr, te in folds.values()
    ]
    n_splits = args.splits or (min(len(flat), SMALL_SPLITS) if len(df) <= SMALL_ROWS else DEFAULT_SPLITS)
    pairs = cap(flat[:n_splits], args.max_rows, rng)
    print(f"{args.name}: {len(df):,} rows, {df.shape[1] - 1:,} columns, {n_splits} of {len(flat)} splits ({origin})")

    # Splits: sizes and the target in each test fold, for every shipped split
    split_rows = []
    for i, (train, test) in enumerate(flat):
        row = {"i": i, "n_train": len(train), "n_test": len(test)}
        if n_classes:
            row["test_classes"] = np.bincount(y[test], minlength=n_classes).tolist()
        else:
            row["test_mean"] = float(y[test].mean())
        if task.time_on is not None:
            t = df[task.time_on]
            row["train_time"] = [str(t.iloc[train].min()), str(t.iloc[train].max())]
            row["test_time"] = [str(t.iloc[test].min()), str(t.iloc[test].max())]
        if groups is not None:
            row["test_groups"] = len(np.unique(groups[test]))
        split_rows.append(row)

    columns = [c for c in df.columns if c != target_name]
    kinds = {c: kind_of(df[c]) for c in columns}
    scored = [c for c in columns if kinds[c] != "text" and c not in group_cols]

    # Single-feature skill, on the true labels and on one shuffle per split (the noise band)
    def values_of(c: str) -> np.ndarray:
        s = df[c]
        if kinds[c] == "categorical":
            return s.astype("category").cat.codes.replace(-1, np.nan).to_numpy(dtype=float)
        if kinds[c] == "datetime":
            if isinstance(s.dtype, pd.PeriodDtype):
                s = s.dt.to_timestamp()
            return np.where(s.isna(), np.nan, s.astype("int64") // 10**9).astype(float)
        return s.to_numpy(dtype=float, na_value=np.nan)

    n_shuffles = max(1, args.feature_permutations)
    print(f"single-feature skill: {len(scored):,} features x {n_splits} splits, true labels and {n_shuffles} shuffles")
    kind_for_bins = {c: "categorical" if kinds[c] == "categorical" else "numeric" for c in scored}

    def per_feature(target: np.ndarray) -> list[list[float]]:
        return Parallel(n_jobs=args.n_jobs, batch_size=16)(
            delayed(single_feature_skill)(values_of(c), kind_for_bins[c], target, pairs, n_classes) for c in scored
        )

    true_skills = per_feature(y)
    null_means, null_best = [], []  # every feature's mean skill, and the best feature's, per shuffle
    for k in range(n_shuffles):
        means = np.array(
            [np.nanmean(s) if len(s) else np.nan for s in per_feature(shuffle(y, groups, np.random.default_rng(7 + k)))]
        )
        means = means[np.isfinite(means)]
        null_means.extend(means.tolist())
        if len(means):
            null_best.append(float(means.max()))
    null_means, null_best = np.array(null_means), np.array(null_best)

    skill_of = {c: s for c, s in zip(scored, true_skills)}
    ranked = sorted(scored, key=lambda c: -np.nan_to_num(np.nanmean(skill_of[c]), nan=-9))
    detail = set(ranked[: args.max_detail]) | {c for c in columns if kinds[c] in ("text",)}

    feature_rows = []
    for c in columns:
        row = {"name": c, "kind": kinds[c], "dtype": str(df[c].dtype), **profile(df[c], kinds[c])}
        if c in group_cols:
            row["role"] = "group"
        if c == task.time_on:
            row["role"] = "time"
        if c in skill_of:
            s = np.array(skill_of[c], dtype=float)
            row["skill"] = float(np.nanmean(s))
            row["skill_sd"] = float(np.nanstd(s))
            row["skill_above"] = float(np.mean(s > 0))
            row["skills"] = s.tolist()
        if c in detail and kinds[c] != "text":
            # categoricals by their level names, not the codes used for scoring
            raw = df[c].to_numpy(dtype=object) if kinds[c] == "categorical" else values_of(c)
            row["hist"] = histogram(raw, kind_for_bins[c], y, n_classes)
        feature_rows.append(row)

    # Correlations of the features with detail
    X, names, _ = features(df, [target_name, *group_cols])
    corr_cols = [i for i, n in enumerate(names) if n in detail]
    print(f"correlations: {len(corr_cols):,} features")
    corr = correlations(X.iloc[:, corr_cols], [names[i] for i in corr_cols], rng)

    signal = None
    if not args.no_signal:
        print(f"signal check: 3 families x {n_splits} splits, true labels and {args.permutations} shuffles")
        signal = signal_check(
            X, y, groups, cap(pairs, args.signal_rows, rng), regression, n_classes, args.permutations, args.n_jobs
        )

    target = {"name": target_name, "classes": classes}
    if n_classes:
        target["counts"] = np.bincount(y, minlength=n_classes).tolist()
    else:
        target["hist"] = histogram(y, "numeric", np.zeros(len(y), dtype=int), 1)
        target["stats"] = profile(df[target_name], "numeric")

    return {
        "name": args.name,
        "generated": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "origin": origin,
        "task": {
            "problem_type": task.problem_type,
            "metric": getattr(task, "objective_metric_name", None),
            "target": target_name,
            "time_on": task.time_on,
            "group_on": group_cols,
            "n_rows": len(df),
            "n_columns": len(columns),
            "kinds": pd.Series(kinds).value_counts().to_dict(),
            "n_splits_total": len(flat),
            "n_splits_used": n_splits,
            "max_rows": args.max_rows,
            "signal_rows": args.signal_rows,
        },
        "summary": task_summary(cls),
        "target": target,
        "splits": split_rows,
        "features": feature_rows,
        "noise": {
            "q95": float(np.quantile(null_means, 0.95)) if len(null_means) else None,
            "q99": float(np.quantile(null_means, 0.99)) if len(null_means) else None,
            "max": float(null_means.max()) if len(null_means) else None,
            "best": null_best.tolist(),
            "shuffles": n_shuffles,
        },
        "correlations": corr,
        "signal": signal,
        "skill_name": "2 AUC - 1" if n_classes == 2 else ("1 - log loss / dummy" if n_classes else "1 - MSE / dummy"),
    }


def main(argv: list[str] | None = None) -> int:
    """Build the page of one dataset and write it."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("name")
    parser.add_argument("--root", type=Path, default=Path("datasets/_dev/tabarena-v0pt2"))
    parser.add_argument("--built", action="store_true", help="read the built container instead of rebuilding")
    parser.add_argument("--shipped", action="store_true", help="read the shipped BeyondArena container (cached)")
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--splits", type=int, default=None)
    parser.add_argument("--permutations", type=int, default=20)
    parser.add_argument(
        "--feature-permutations", type=int, default=5, help="shuffles for the single-feature noise band"
    )
    parser.add_argument("--no-signal", action="store_true", help="skip the model families")
    parser.add_argument("--max-rows", type=int, default=20_000, help="cap on the train and test sides per split")
    parser.add_argument("--signal-rows", type=int, default=5_000, help="the same cap for the signal check")
    parser.add_argument("--max-detail", type=int, default=3_000, help="features with a drill-down and correlations")
    parser.add_argument("--n-jobs", type=int, default=8)
    args = parser.parse_args(argv)

    data = clean(build(args))
    out = args.out or Path.home() / ".cache" / "data_foundry" / "explore" / f"{args.name}.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(data, separators=(",", ":")).replace("</", "<\\/")
    page = TEMPLATE.read_text().replace("__TITLE__", args.name).replace("__DATA__", payload)
    out.write_text(page)
    print(f"wrote {out} ({out.stat().st_size / 1e6:.1f} MB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
