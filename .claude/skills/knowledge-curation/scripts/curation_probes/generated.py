"""Generated-data probes: is the target a formula or a rule set of the features, or were the columns drawn one by one?

Real measurements carry noise in every row and depend on each other; a generator often computes the target exactly
for most rows and adds noise to a few, assigns labels by crisp rules, or draws each column on its own, often uniformly
over a range. Four checks, on at most ``MAX_ROWS`` rows. They are tooling-independent: ``check_frame`` takes a
pandas frame of features, target and group columns, the target column and the problem type:

* **Regression, exact formula** (``exact_share``): a median (L1) regression of the target on simple terms (the
  numeric features, their squares, one-hot categoricals with at most ``MAX_LEVELS`` levels, and the products of each
  binary column with each numeric feature) on ``n_fit`` rows. ``exact_share`` is the share of rows it fits within
  rounding (half a unit of the target's last decimal, or ``1e-6`` relative), not counting the rows at a mass point of
  the target (a value held by ``MASS_POINT`` of the rows, such as a timeout: sat11_hand_algo_runtime has 36% of its
  rows at the cap, which any model that predicts the cap hits exactly). An L1 fit passes exactly through about
  ``p`` rows anyway, so the same fit on a shuffled target gives the baseline (``exact_share_shuffled``). The target is
  also tried after ``exp`` / ``expm1`` (a curator may have logged it). healthcare_insurance_expenses: 73% exact
  (its generator also has a threshold term), against 1% shuffled.
* **Classification, rule leaves** (``pure_minority_share``): a tree of depth ``TREE_DEPTH`` (leaves of at least
  ``min_leaf`` rows) is fit on one half and read on the other; a leaf whose held-out rows all belong to one class that
  is not the most frequent is a rule leaf. ``pure_minority_share`` is the share of the held-out minority rows that
  fall in rule leaves (averaged over both halves). churn: the international-plan rules cover a large share.
* **All tasks, independent columns** (``pair_share``, ``uniform_share``): the features and the target together, on
  ``SAMPLE_ROWS`` rows and at most ``MAX_COLUMNS`` columns (seeded samples). ``pair_share`` is the share of column
  pairs that depend on each other at level ``PAIR_P``: Spearman's rho for two ordered columns, a chi-square test on at
  most ``BINS + 1`` cells when one of them is nominal. Independent columns give about ``PAIR_P``. ``uniform_share``
  is the share of the ordered columns of at least ``UNIFORM_MIN_VALUES`` values that a KS test cannot tell from a
  uniform over their range (p above ``UNIFORM_P``); they are listed in ``uniform_names``. hepatitis_c_egypt (UCI 503,
  not added): 5.7% of 406 pairs, 11 of 17 columns uniform. Neither statistic separates on its own:
  santander_customer_transaction_prediction has 5.4% of its pairs dependent and no uniform column,
  homesite_quote_conversion 13 of 42 columns uniform (its equal-frequency bin codes) and 45% of its pairs dependent.
* **Classes, uniform within each class** (``class_pair_share``, ``class_uniform_share``): the same two statistics on
  the features within each class of at least ``MIN_CLASS_ROWS`` rows (at most ``SAMPLE_ROWS`` per class; a regression
  target of at most ``MAX_LEVELS`` values counts as classes), pooled over the classes. Drawing each feature uniformly
  within its class's range leaves the whole table dependent, since the ranges differ by class, so the check above
  misses it. OpenML 46372, made that way from the 197 rows of corporate_credit_rating_cat_data_set_ratings_raitings:
  4.0% of 150 pairs within the classes, 60 of 60 class-column cells uniform, but 90.5% of the pairs in the whole file.

Flags: ``formula`` (``exact_share >= FORMULA_SHARE`` and at least ``FORMULA_RATIO`` times the shuffled baseline),
``rule_leaves`` (``pure_minority_share >= RULE_SHARE``), ``independent_columns`` (``pair_share <= INDEPENDENT_SHARE``
and ``uniform_share >= UNIFORM_SHARE`` of at least ``MIN_UNIFORM_COLUMNS`` tested columns) and
``uniform_within_class`` (the same thresholds on the pooled within-class statistics, with at least
``MIN_UNIFORM_COLUMNS`` tested columns per class on average). A flag is a question: a legitimately deterministic
target (a computed score, a label defined by thresholds) or a leak gives the first two signals, and inputs set by a
design (a uniform grid, a Latin hypercube) can give the last two. Read the source (simulated, generated, "artificial")
and look for other signs (independence that the world would not show, identical distributions across columns) before
proposing anything.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency, kstest, norm, rankdata
from sklearn.linear_model import QuantileRegressor
from sklearn.tree import DecisionTreeClassifier

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
SAMPLE_ROWS = 1000
"""Rows (per class, for the within-class check) the independence checks read. The noise band of a correlation
shrinks with the rows, so a fixed sample keeps the shares comparable across datasets."""
MAX_COLUMNS = 100
BINS = 5
PAIR_P = 0.05
UNIFORM_P = 0.01
UNIFORM_MIN_VALUES = 20
MIN_UNIFORM_COLUMNS = 5
MIN_CLASS_ROWS = 50
INDEPENDENT_SHARE = 0.10
UNIFORM_SHARE = 0.5


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


def encode(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    """Each usable column as floats for the independence checks, and the nominal ones among them.

    Numeric, boolean, datetime (as seconds) and timedelta columns keep their order, and so do ordered categoricals.
    Any other categorical or text column enters as codes (a missing value is a level of its own) and is nominal when it
    has more than two levels. Constant columns and text columns with a distinct value in more than half the rows (an
    id, free text) are left out.
    """
    out, nominal = {}, []
    for col in df.columns:
        values = df[col]
        if isinstance(values.dtype, pd.PeriodDtype):
            values = values.dt.to_timestamp()
        if pd.api.types.is_bool_dtype(values):
            out[col] = values.astype(float)
        elif pd.api.types.is_datetime64_any_dtype(values):
            out[col] = (values - pd.Timestamp(0, tz=values.dt.tz)) / pd.Timedelta(seconds=1)
        elif pd.api.types.is_timedelta64_dtype(values):
            out[col] = values / pd.Timedelta(seconds=1)
        elif pd.api.types.is_numeric_dtype(values):
            out[col] = values.astype(float)
        elif isinstance(values.dtype, pd.CategoricalDtype) and values.dtype.ordered:
            out[col] = values.cat.codes.replace(-1, np.nan).astype(float)
        else:
            codes, levels = pd.factorize(values.astype(object))
            if len(levels) > 0.5 * len(values):
                continue
            out[col] = pd.Series(np.where(codes < 0, len(levels), codes), index=df.index).astype(float)
            if out[col].nunique() > 2:
                nominal.append(col)
    X = pd.DataFrame(out, index=df.index)
    filled = X.fillna(np.inf)  # a missing value counts as a value of its own
    keep = filled.ne(filled.iloc[0]).any()
    return X.loc[:, keep], [c for c in nominal if keep[c]]


def cells(values: np.ndarray, *, nominal: bool) -> np.ndarray:
    """Codes 0, 1, ... of at most ``BINS + 1`` cells: the ``BINS`` most frequent levels of a nominal column (the rest
    in one cell), quantile bins of any other.
    """
    if nominal:
        _, codes, counts = np.unique(values, return_inverse=True, return_counts=True)
        mapping = np.full(len(counts), BINS)
        top = np.argsort(-counts, kind="stable")[:BINS]
        mapping[top] = np.arange(len(top))
        return mapping[codes]
    edges = np.unique(np.quantile(values, np.linspace(0, 1, BINS + 1)[1:-1]))
    return np.searchsorted(edges, values, side="right")


def dependent_pairs(X: pd.DataFrame, nominal: list[str]) -> tuple[int, int]:
    """How many column pairs of ``X`` depend on each other at level ``PAIR_P``, and how many pairs were tested.

    Two ordered columns: Spearman's rho outside the band that independence leaves at that level. A pair with a nominal
    column: a chi-square test on the cells of ``cells``.
    """
    X = X.fillna(X.median())
    is_nominal = [c in nominal for c in X.columns]
    with np.errstate(invalid="ignore", divide="ignore"):
        rho = np.corrcoef(np.column_stack([rankdata(X[c]) for c in X.columns]), rowvar=False)
    band = norm.ppf(1 - PAIR_P / 2) / np.sqrt(len(X) - 1)
    codes = [cells(X[c].to_numpy(), nominal=flag) for c, flag in zip(X.columns, is_nominal, strict=True)]
    hits = pairs = 0
    for i in range(X.shape[1]):
        for j in range(i + 1, X.shape[1]):
            if is_nominal[i] or is_nominal[j]:
                table = np.zeros((BINS + 1, BINS + 1))
                np.add.at(table, (codes[i], codes[j]), 1)
                table = table[table.sum(axis=1) > 0][:, table.sum(axis=0) > 0]
                if min(table.shape) < 2:
                    continue
                hit = chi2_contingency(table, correction=False).pvalue < PAIR_P
            elif np.isfinite(rho[i, j]):
                hit = abs(rho[i, j]) > band
            else:
                continue
            pairs += 1
            hits += int(hit)
    return hits, pairs


def uniform_columns(X: pd.DataFrame, nominal: list[str], rng: np.random.Generator) -> tuple[list[str], int]:
    """The ordered columns of at least ``UNIFORM_MIN_VALUES`` distinct values that a KS test cannot tell from a uniform
    over their range (p above ``UNIFORM_P``), and how many were tested. Values on a grid (integers, a fixed number of
    decimals) are first spread uniformly over their grid cell, so that a discrete uniform tests as uniform.
    """
    uniform, tested = [], 0
    for col in X.columns:
        values = X[col].dropna().to_numpy()
        if col in nominal or len(np.unique(values)) < UNIFORM_MIN_VALUES:
            continue
        tested += 1
        values = values + rng.random(len(values)) * 10.0 ** -decimals(values)
        low, high = values.min(), values.max()
        if kstest((values - low) / (high - low), "uniform").pvalue > UNIFORM_P:
            uniform.append(str(col))
    return uniform, tested


def columns_sample(columns: pd.Index, keep: str | None, rng: np.random.Generator) -> list[str]:
    """At most ``MAX_COLUMNS`` columns (a seeded sample, always with ``keep``), in their order."""
    if len(columns) <= MAX_COLUMNS:
        return list(columns)
    others = [c for c in columns if c != keep]
    chosen = set(rng.choice(others, MAX_COLUMNS - (keep is not None), replace=False).tolist()) | {keep}
    return [c for c in columns if c in chosen]


def independence_check(df: pd.DataFrame, target: str) -> dict:
    """The independent-columns check of the module docstring, on the features and the target together."""
    rng = np.random.default_rng(0)
    rows = np.sort(rng.choice(len(df), min(len(df), SAMPLE_ROWS), replace=False))
    X, nominal = encode(df[columns_sample(df.columns, target, rng)].iloc[rows])
    if X.shape[1] < 3:
        return {"independence_skipped": f"{X.shape[1]} usable columns"}
    hits, pairs = dependent_pairs(X, nominal)
    uniform, tested = uniform_columns(X, nominal, rng)
    return {
        "pair_share": hits / pairs if pairs else float("nan"),
        "pairs": pairs,
        "uniform_share": len(uniform) / tested if tested else float("nan"),
        "uniform_columns": len(uniform),
        "uniform_tested": tested,
        "uniform_names": uniform[:20],
        "independence_rows": len(rows),
    }


def class_check(X: pd.DataFrame, y: pd.Series, problem_type: str) -> dict:
    """The within-class check of the module docstring: the independence statistics on the features within each class
    of at least ``MIN_CLASS_ROWS`` rows (a regression target of at most ``MAX_LEVELS`` values counts as classes),
    pooled over the classes.
    """
    counts = y.value_counts()
    if problem_type == "regression" and len(counts) > MAX_LEVELS:
        return {"class_skipped": f"regression target with {len(counts)} values"}
    counts = counts[counts >= MIN_CLASS_ROWS].iloc[:MAX_LEVELS]
    if len(counts) < 2:
        return {"class_skipped": f"{len(counts)} classes of at least {MIN_CLASS_ROWS} rows"}
    rng = np.random.default_rng(0)
    X = X[columns_sample(X.columns, None, rng)]
    detail = []
    for label in counts.index:
        rows = np.flatnonzero((y == label).to_numpy())
        rows = np.sort(rng.choice(rows, min(len(rows), SAMPLE_ROWS), replace=False))
        Xc, nominal = encode(X.iloc[rows])
        hits, pairs = dependent_pairs(Xc, nominal) if Xc.shape[1] >= 2 else (0, 0)
        uniform, tested = uniform_columns(Xc, nominal, rng)
        detail.append({"class": str(label), "rows": len(rows), "hits": hits, "pairs": pairs, "tested": tested})
        detail[-1] |= {"uniform": len(uniform), "uniform_names": uniform[:10]}
    hits, pairs, uniform, tested = (sum(d[k] for d in detail) for k in ("hits", "pairs", "uniform", "tested"))
    return {
        "class_pair_share": hits / pairs if pairs else float("nan"),
        "class_pairs": pairs,
        "class_uniform_share": uniform / tested if tested else float("nan"),
        "class_uniform_columns": uniform,
        "class_uniform_tested": tested,
        "classes": len(counts),
        "class_detail": detail,
    }


def check_frame(df: pd.DataFrame, target: str, problem_type: str, group_cols: list[str]) -> dict:
    """Run the checks of the module docstring on one table of features, target and group columns, and set the flags."""
    rng = np.random.default_rng(0)
    if len(df) > MAX_ROWS:
        df = df.iloc[np.sort(rng.choice(len(df), MAX_ROWS, replace=False))].reset_index(drop=True)
    X = df.drop(columns=[target, *group_cols])
    result = {"problem_type": problem_type, "rows": len(df)}
    if problem_type == "regression":
        result |= formula_check(X, df[target].to_numpy(dtype=float), rng)
    else:
        result |= rule_check(X, df[target].astype(str).to_numpy(), rng)
    result |= independence_check(df.drop(columns=group_cols), target)
    labelled = df[target].notna().to_numpy()
    y = df[target] if problem_type == "regression" else df[target].astype(str)
    result |= class_check(X[labelled], y[labelled], problem_type)
    flags = []
    if result.get("exact_share", 0) >= FORMULA_SHARE and result["exact_share"] >= FORMULA_RATIO * max(
        result["exact_share_shuffled"], 0.01
    ):
        flags.append("formula")
    if result.get("pure_minority_share", 0) >= RULE_SHARE:
        flags.append("rule_leaves")
    if (
        result.get("pair_share", 1.0) <= INDEPENDENT_SHARE
        and result.get("uniform_tested", 0) >= MIN_UNIFORM_COLUMNS
        and result["uniform_share"] >= UNIFORM_SHARE
    ):
        flags.append("independent_columns")
    if (
        result.get("class_pair_share", 1.0) <= INDEPENDENT_SHARE
        and result.get("class_uniform_tested", 0) >= MIN_UNIFORM_COLUMNS * result["classes"]
        and result["class_uniform_share"] >= UNIFORM_SHARE
    ):
        flags.append("uniform_within_class")
    result["flags"] = flags
    return result
