"""Generated-data probes: is the target a formula or a rule set of the features, as in simulated data?

Usage::

    python .claude/skills/verify-dataset/scripts/generated_probes.py <unique_name> ... [--all] [--built] [--jobs 8]
        [--out DIR]

Real measurements carry noise in every row; a generator often computes the target exactly for most rows and adds
noise to a few, or assigns labels by crisp rules. Two checks, on at most ``MAX_ROWS`` rows:

* **Regression, exact formula** (``exact_share``): a median (L1) regression of the target on simple terms (the
  numeric features, their squares, one-hot categoricals with at most ``MAX_LEVELS`` levels, and the products of each
  binary column with each numeric feature) on ``n_fit`` rows. ``exact_share`` is the share of rows it fits within
  rounding (half a unit of the target's last decimal, or ``1e-6`` relative), not counting the rows at a mass point of
  the target (a value held by ``MASS_POINT`` of the rows, such as a timeout: sat11_hand_algo_runtime has 36% of its
  rows at the cap, which any model that predicts the cap hits exactly). An L1 fit passes exactly through about
  ``p`` rows anyway, so the same fit on a shuffled target gives the baseline (``exact_share_shuffled``). The target is
  also tried after ``exp`` / ``expm1`` (a definition may have logged it). healthcare_insurance_expenses: 73% exact
  (its generator also has a threshold term), against 1% shuffled.
* **Classification, rule leaves** (``pure_minority_share``): a tree of depth ``TREE_DEPTH`` (leaves of at least
  ``min_leaf`` rows) is fit on one half and read on the other; a leaf whose held-out rows all belong to one class that
  is not the most frequent is a rule leaf. ``pure_minority_share`` is the share of the held-out minority rows that
  fall in rule leaves (averaged over both halves). churn: the international-plan rules cover a large share.

Flags: ``formula`` (``exact_share >= FORMULA_SHARE`` and at least ``FORMULA_RATIO`` times the shuffled baseline) and
``rule_leaves`` (``pure_minority_share >= RULE_SHARE``). A flag is a question: a legitimately deterministic target
(a computed score, a label defined by thresholds) or a leak gives the same signal. Read the source (simulated,
generated, "artificial") and look for other signs (independence that the world would not show, identical
distributions across columns) before proposing anything; how to read them:
``.claude/skills/verify-dataset/references/task_probes.md`` (generated data).
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import discover_datasets
from joblib import Parallel, delayed
from sklearn.linear_model import QuantileRegressor
from sklearn.tree import DecisionTreeClassifier

sys.path.insert(0, str(Path(__file__).parent))
from task_probes import load

MAX_ROWS = 20_000
MAX_LEVELS = 20
MAX_TERMS = 200
MIN_ROWS_PER_TERM = 10
MASS_POINT = 0.05
"""A target value held by at least this share of the rows is a mass point (left out of the exact share)."""
FORMULA_SHARE = 0.1
FORMULA_RATIO = 3.0
TREE_DEPTH = 5
RULE_SHARE = 0.2


def design(df: pd.DataFrame, drop: list[str], *, codes: bool = False) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Numeric features (datetimes as seconds, booleans as 0/1) and one-hot categoricals of few levels; with
    ``codes``, a categorical of more levels enters as its codes (for the tree).
    """
    X = df.drop(columns=[c for c in drop if c in df.columns])
    numeric, binary = {}, {}
    for col in X.columns:
        values = X[col]
        if isinstance(values.dtype, pd.CategoricalDtype) or values.dtype == object:
            levels = values.astype(object).dropna().unique()
            if 2 <= len(levels) <= MAX_LEVELS:
                for level in sorted(levels, key=str)[1:]:
                    binary[f"{col}={level}"] = (values.astype(object) == level).astype(float)
            elif codes and len(levels) > MAX_LEVELS:
                numeric[col] = pd.Series(pd.factorize(values.astype(object))[0], index=X.index).astype(float)
        elif pd.api.types.is_bool_dtype(values):
            binary[col] = values.astype(float)
        elif pd.api.types.is_datetime64_any_dtype(values):
            numeric[col] = values.astype("int64") // 10**9
        elif pd.api.types.is_numeric_dtype(values):
            if values.nunique() == 2:
                binary[col] = (values == values.max()).astype(float)
            else:
                numeric[col] = values.astype(float)
    return pd.DataFrame(numeric, index=X.index), pd.DataFrame(binary, index=X.index)


def terms(numeric: pd.DataFrame, binary: pd.DataFrame, budget: int) -> pd.DataFrame:
    """Main effects, squares and binary x numeric products, dropping the products and then the squares to fit."""
    parts = [numeric, binary]
    squares = numeric.pow(2).add_suffix("^2")
    products = {f"{b}*{n}": binary[b] * numeric[n] for b in binary.columns for n in numeric.columns}
    if numeric.shape[1] + binary.shape[1] + squares.shape[1] + len(products) <= budget:
        parts += [squares, pd.DataFrame(products, index=numeric.index)]
    elif numeric.shape[1] + binary.shape[1] + squares.shape[1] <= budget:
        parts.append(squares)
    out = pd.concat(parts, axis=1).fillna(0.0)
    return out.loc[:, out.std() > 0].iloc[:, :budget]


def decimals(y: np.ndarray) -> int:
    """The number of decimals the target values carry (at most 6)."""
    sample = y[: min(len(y), 2000)]
    for d in range(7):
        if np.allclose(sample, np.round(sample, d), rtol=0, atol=1e-9 * max(1.0, np.abs(sample).max())):
            return d
    return 6


def exact_share(F: pd.DataFrame, y: np.ndarray, counted: np.ndarray) -> float:
    """The share of the ``counted`` rows an L1 regression on ``F`` fits within the rounding of ``y``."""
    tol = max(0.5 * 10.0 ** -decimals(y) + 1e-12, 1e-6 * float(np.median(np.abs(y)) + 1e-12))
    # scale the terms and the target: the LP solver fails on dates in seconds and their squares; a linear rescaling
    # leaves the set of exactly fitted rows unchanged
    std = F.std(axis=0)
    Z = (F - F.mean(axis=0)) / np.where(std > 0, std, 1.0)
    scale = float(np.std(y)) or 1.0
    for solver in ("highs", "highs-ipm"):
        try:
            fit = QuantileRegressor(quantile=0.5, alpha=0.0, solver=solver).fit(Z, y / scale)
        except TypeError:  # the solver found no solution
            continue
        return float(np.mean((np.abs(y - fit.predict(Z) * scale) <= tol)[counted]))
    return float("nan")


def formula_check(X: pd.DataFrame, y: np.ndarray, rng: np.random.Generator) -> dict:
    """The exact-formula check of the module docstring."""
    n_fit = min(len(X), 4000)
    rows = rng.choice(len(X), n_fit, replace=False)
    # a value that many rows share (a cap, a timeout, a zero) is hit exactly by any model that predicts the mass
    # point: those rows do not count, and the term budget follows the rows that do
    values, counts = np.unique(y[rows], return_counts=True)
    mass_points = values[counts >= MASS_POINT * n_fit]
    counted = ~np.isin(y[rows], mass_points)
    budget = min(MAX_TERMS, int(counted.sum()) // MIN_ROWS_PER_TERM)
    numeric, binary = design(X.iloc[rows].reset_index(drop=True), [])
    F = terms(numeric, binary, budget) if budget >= 1 else pd.DataFrame()
    if F.shape[1] == 0:
        return {"skipped": "too few rows off the target's mass points", "mass_points": mass_points.tolist()}
    Fs = F.to_numpy()
    candidates = {"identity": y}
    if np.nanmax(y) < 50:
        candidates |= {"exp": np.exp(y), "expm1": np.expm1(y)}
    best = {"exact_share": -1.0}
    for name, target in candidates.items():
        t = target[rows]
        if not np.all(np.isfinite(t)):
            continue
        share = exact_share(Fs, t, counted)
        if share > best["exact_share"]:
            best = {"exact_share": share, "transform": name, "target": t}
    if "target" not in best:
        return {"skipped": "the solver found no fit"}
    order = rng.permutation(n_fit)
    shuffled = exact_share(Fs, best.pop("target")[order], counted[order])
    out = best | {"exact_share_shuffled": shuffled, "terms": F.shape[1], "n_fit": n_fit}
    if len(mass_points):
        out |= {"mass_points": mass_points.tolist(), "mass_point_share": float(1 - counted.mean())}
    return out


def rule_check(X: pd.DataFrame, y: np.ndarray, rng: np.random.Generator) -> dict:
    """The rule-leaf check of the module docstring."""
    numeric, binary = design(X, [], codes=True)
    F = pd.concat([numeric, binary], axis=1).fillna(-1e12).to_numpy()
    if F.shape[1] == 0:
        return {"skipped": "no usable features"}
    classes, counts = np.unique(y, return_counts=True)
    majority = classes[np.argmax(counts)]
    min_leaf = max(20, int(0.005 * len(y)))
    order = rng.permutation(len(y))
    halves = (order[: len(y) // 2], order[len(y) // 2 :])
    shares, leaves = [], []
    for fit_rows, read_rows in (halves, halves[::-1]):
        tree = DecisionTreeClassifier(max_depth=TREE_DEPTH, min_samples_leaf=min_leaf, random_state=0)
        tree.fit(F[fit_rows], y[fit_rows])
        leaf = tree.apply(F[read_rows])
        y_read = y[read_rows]
        covered = 0
        for value in np.unique(leaf):
            labels = y_read[leaf == value]
            if len(labels) >= min_leaf and np.all(labels == labels[0]) and labels[0] != majority:
                covered += len(labels)
                leaves.append({"rows": len(labels), "class": str(labels[0])})
        minority = int(np.sum(y_read != majority))
        shares.append(covered / minority if minority else 0.0)
    return {"pure_minority_share": float(np.mean(shares)), "rule_leaves": leaves[:10], "min_leaf": min_leaf}


def probe(name: str, root: Path, *, built: bool) -> dict:
    """Run the checks of the module docstring on one dataset."""
    started = time.time()
    container, origin = load(name, root, built=built)
    task, grouping = container.task_metadata, container.grouping
    df = container.dataset
    group_cols = (
        list(grouping.on)
        if grouping is not None and isinstance(grouping.on, list)
        else ([grouping.on] if grouping is not None else [])
    )
    rng = np.random.default_rng(0)
    if len(df) > MAX_ROWS:
        df = df.iloc[np.sort(rng.choice(len(df), MAX_ROWS, replace=False))].reset_index(drop=True)
    X = df.drop(columns=[task.target_column_name, *group_cols])
    result = {"name": name, "problem_type": task.problem_type, "rows": len(df), "origin": origin}
    if task.problem_type == "regression":
        result |= formula_check(X, df[task.target_column_name].to_numpy(dtype=float), rng)
    else:
        result |= rule_check(X, df[task.target_column_name].astype(str).to_numpy(), rng)
    flags = []
    if result.get("exact_share", 0) >= FORMULA_SHARE and result["exact_share"] >= FORMULA_RATIO * max(
        result["exact_share_shuffled"], 0.01
    ):
        flags.append("formula")
    if result.get("pure_minority_share", 0) >= RULE_SHARE:
        flags.append("rule_leaves")
    result["flags"] = flags
    result["seconds"] = round(time.time() - started)
    return result


def _safe(name: str, root: Path, **kwargs) -> dict:
    try:
        return probe(name, root, **kwargs)
    except Exception as error:  # noqa: BLE001 - one failing dataset must not stop a sweep
        return {"name": name, "error": f"{type(error).__name__}: {error}"[:300], "flags": []}


def render(r: dict) -> str:
    """One line per dataset."""
    if "error" in r:
        return f"{r['name']}: error {r['error']}"
    if "exact_share" in r:
        detail = (
            f"exact {r['exact_share']:.1%} ({r['transform']}) vs shuffled {r['exact_share_shuffled']:.1%}, "
            f"{r['terms']} terms on {r['n_fit']} rows"
        )
    elif "pure_minority_share" in r:
        detail = (
            f"rule leaves cover {r['pure_minority_share']:.1%} of the minority rows ({len(r['rule_leaves'])} leaves)"
        )
    else:
        detail = r.get("skipped", "")
    return f"{r['name']} ({r['problem_type']}, {r['rows']} rows): {detail}; flags {r['flags']}"


def main(argv: list[str] | None = None) -> int:
    """Probe the datasets; see the module docstring."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("names", nargs="*")
    parser.add_argument("--all", action="store_true", help="Probe every definition under --root.")
    parser.add_argument("--root", type=Path, default=Path("datasets/_dev/tabarena-v0pt2"))
    parser.add_argument("--built", action="store_true", help="Read the built containers (README build record).")
    parser.add_argument("--jobs", type=int, default=1, help="Datasets probed in parallel.")
    parser.add_argument("--out", type=Path, help="Write one JSON per dataset and summary.md here.")
    args = parser.parse_args(argv)
    names = sorted(discover_datasets(args.root)) if args.all else args.names
    if not names:
        parser.error("name at least one dataset, or pass --all")
    results = Parallel(n_jobs=args.jobs)(delayed(_safe)(n, args.root, built=args.built) for n in names)
    for r in results:
        print(render(r))
    if args.out:
        args.out.mkdir(parents=True, exist_ok=True)
        for r in results:
            (args.out / f"{r['name']}.json").write_text(json.dumps(r, indent=1, default=str))
        lines = [f"- {render(r)}" for r in sorted(results, key=lambda r: (not r["flags"], r["name"]))]
        (args.out / "summary.md").write_text("\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
