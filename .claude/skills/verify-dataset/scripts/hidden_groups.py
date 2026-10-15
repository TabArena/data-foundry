"""Hidden groups: columns, keys of all columns but one and near copies that carry the label, and a random split's gain.

Usage::

    python .claude/skills/verify-dataset/scripts/hidden_groups.py <unique_name> ... [--all] [--built] [--jobs 8]
        [--out DIR] [--include-grouped]

An IID split assumes the rows are independent. When many rows share an entity (a patient, a customer, a product)
and the entity carries the label, a random split puts rows of one entity on both sides, and a model can score by
recognising the entity instead of learning the task. This probe looks for such entities among the columns, among rows
identical in all columns but one, and among clusters of rows that agree on almost every column.

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
5. **Near copies** (``(near copies)``, the ``near_copies`` entry of the JSON): a group that no single column holds,
   such as the salt forms of one compound in a table of fingerprint bits. Each row becomes a set of tokens, one per
   feature column: a numeric column with more than ``COPY_BINS`` values gives its quantile bin, any other column its
   value (missing is a value), and a value held by more than ``COPY_DOMINANT`` of the rows gives no token, so on
   fingerprint bits that are mostly 0 the similarity is the Tanimoto coefficient. Two rows are near copies when
   their token sets have a Jaccard similarity of at least ``COPY_SIMILARITY`` (0.85: 92% of the columns agree when
   no value is dominant) and share at least ``COPY_MIN_SHARED`` tokens, so a table with fewer informative columns
   has no near copies (its groups are combinations of a few columns, which step 6 covers). The clusters are the
   connected components; a cluster of more than ``COPY_MAX_CLUSTER`` rows is a
   common profile (empty records, a default customer) or a chain of neighbours, not one entity, and its rows count
   as singletons (``rows_in_large_clusters``). Pairs are found by MinHash (``MINHASH_BANDS`` bands of
   ``MINHASH_ROWS`` hashes; all pairs of a bucket of up to ``BUCKET_WINDOW`` rows, in a larger bucket each row with
   the next one and the first) and checked exactly, so it takes seconds on 100k rows and about a minute on 2.5M;
   frames over ``MAX_COPY_CELLS`` cells use a random subset of the columns (``columns_used``). The probe reports
   the clusters (count, rows in clusters of two or more, largest, sizes), ``s_id``, the clusters at each similarity
   of ``COPY_LADDER``, and, when at least ``COPY_MIN_SHARE`` of the rows are in a cluster of two or more, the split
   gap of step 4 with grouped folds that are the random folds with each cluster moved into the fold of its first
   row, so the two splits differ only in the clustered rows.
6. **Composite keys** (``(all but Age)``, the ``composite_keys`` entry of the JSON): rows identical in every column
   but one are repeated measurements of one entity at another age, dose, time or position (a concrete mix tested at
   several ages, a wind-tunnel run measured at several frequencies), a group that no single column holds and that a
   table of a few columns cannot show as near copies. Each key is all columns but the left-out ones (the target and
   a known group column are never part of it, constant columns do not count, a missing value is a value), hashed
   exactly. The rows that share a key of at most ``COPY_MAX_CLUSTER`` rows with a row that differs are the
   ``varying_share`` (a larger key is a common profile, such as a customer with every column empty). A key counts
   when it holds a column of at least ``MIN_GROUPS`` values (a key of only coarse columns, such as binary symptoms,
   is a profile that new rows share by chance), at least ``MIN_GROUPS`` keys hold differing rows, the
   ``varying_share`` is at least ``KEY_MIN_SHARE`` and at least ``1 / KEY_CHANCE`` times the share with every column
   permuted on its own (``baseline_share``: repeats by chance, as in a factorial design of a few categories), and no
   key holds more than ``MAX_TOP_SHARE`` of the rows. The probe first leaves out one column; only when no key counts,
   two (a time column and one derived from it), if the number of keys times the rows stays within ``KEY_BUDGET`` (a
   wide table checks a random subset of the one-column keys, ``keys_checked``). The ``N_KEYS`` keys with the most
   rows above chance get ``s_id`` and the split gap of step 4 with folds by key.

A column candidate is **eligible** when its value carries the label (``s_id - s_smooth >= MIN_IDENTITY``) and it
looks like an entity: at least ``MIN_STATIC`` attributes, or a label that its value nearly fixes
(``s_id >= STRONG_ID``: a molecule's conformations, the samples of one mouse). The near copies are eligible when at
least ``COPY_ELIGIBLE_SHARE`` of the rows are in a cluster of two or more and the clusters carry the label
(``s_id >= MIN_IDENTITY``; they have no smooth part and share most columns by construction). A composite key is
eligible when it counts (step 6) and carries the label (``s_id >= MIN_IDENTITY``). A candidate is a
**hit** when it is eligible, ``gap >= MIN_GAP`` and ``gap >= MIN_RELATIVE_GAP * skill(random)``. A composite key is
evidence of an entity by itself, so its gap may instead raise the error left by ``KEY_ERROR_RISE``
(``gap >= KEY_ERROR_RISE * (1 - skill(random))``): concrete's mixes cost 7% of the skill but nearly double the
error (R^2 0.923 against 0.857). A hit is a question, not a verdict: re-split a dataset by a column only when the
context says the rows share an entity that new data would not have (the source describes the column as an id, or
the use case predicts for new entities), or the evidence is very strong; then the use case decides, not the size of
the gap. A near-copy cluster is never the group key itself: it points to an entity, and the key comes from the
source. How to read the output: ``.claude/skills/verify-dataset/references/task_probes.md`` (hidden groups).

**Temporal tasks** get no gap and no hit: the shipped splits already hold out the future, and an entity that recurs
across the cutoff is part of the task (a customer's next month). Instead, for the ``N_TESTED`` top candidates (the
eligible ones, listed as ``entity_like``, first), the composite keys and the near copies, the probe reports the share
of test rows whose value (or cluster, or key) occurs among the training rows of each shipped split
(``test_rows_seen``, with its range over the splits): how often the entities recur across the cutoff. The time column
is no candidate and no near-copy token (a composite key can leave it out), and only the scored candidates are turned
into model inputs.

``--include-grouped`` also runs the grouped datasets as if they were IID (their known group column is marked, and
left out of the near-copy tokens and the composite keys; a key with the same groups is marked as the known group):
the positive controls for the thresholds.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from itertools import combinations
from math import comb
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1")

import lightgbm as lgb
import numpy as np
import pandas as pd
from data_foundry.schema import as_column_list
from data_foundry.v2 import discover_datasets
from joblib import Parallel, delayed
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
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

NEAR_COPIES = "(near copies)"
"""The name of the near-copy candidate in the output (it is no column)."""
COPY_BINS = 16
COPY_DOMINANT = 0.5
COPY_SIMILARITY = 0.85
COPY_LADDER = (0.9, 0.85, 0.8, 0.7)
COPY_MIN_SHARE = 0.01
COPY_ELIGIBLE_SHARE = 0.1
COPY_MIN_SHARED = 10
COPY_MAX_CLUSTER = 100
MINHASH_BANDS = 20
MINHASH_ROWS = 6
BUCKET_WINDOW = 20
MAX_COPY_CELLS = 30_000_000
COPY_SIZES = ((2, 2), (3, 5), (6, 20), (21, None))
"""The cluster sizes counted in ``cluster_sizes``."""

KEY_MIN_SHARE = 0.1
"""Composite keys: the least share of the rows in keys whose rows differ."""
KEY_CHANCE = 0.25
"""Composite keys: the most that share may be with independent columns, relative to the share observed."""
KEY_ERROR_RISE = 0.25
"""Composite keys: a gap that raises the error left (``1 - skill``) by this share is large enough."""
KEY_MAX_LEFT_OUT = 2
KEY_BUDGET = 200_000_000
"""Rows times keys hashed by the composite-key search."""
KEY_CACHE_CELLS = 10_000_000
"""Frames up to this many cells keep the column hashes in memory."""
N_KEYS = 2
"""Composite keys that get ``s_id`` and the split gap."""


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
        elif len(np.unique(y[train])) == 1:  # a training fold with one class predicts it
            pred[test, y[train][0]] = 1.0
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


def moved(y: np.ndarray, groups: np.ndarray, n_classes: int) -> list:
    """The random folds of :func:`splits`, with every group moved into the fold of its first row: the two splits
    differ only in the rows that share a group.
    """
    fold = np.empty(len(y), dtype=np.int64)
    for k, (_, test) in enumerate(splits(y, None, n_classes)):
        fold[test] = k
    first = np.empty(groups.max() + 1, dtype=np.int64)
    first[groups[::-1]] = np.arange(len(groups))[::-1]
    fold = fold[first[groups]]
    return [(np.flatnonzero(fold != k), np.flatnonzero(fold == k)) for k in range(FOLDS)]


def subsample(groups: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Positions of whole groups, in random order, up to ``MAX_ROWS`` rows (all rows when the frame fits). At least
    ``FOLDS`` groups are kept; when they hold more than ``MAX_ROWS`` rows, a random part of their rows.
    """
    if len(groups) <= MAX_ROWS:
        return np.arange(len(groups))
    order = rng.permutation(np.unique(groups))
    sizes = np.bincount(groups)[order]
    keep = order[: max(FOLDS, int(np.searchsorted(np.cumsum(sizes), MAX_ROWS)))]
    rows = np.flatnonzero(np.isin(groups, keep))
    return rows if len(rows) <= MAX_ROWS else np.sort(rng.choice(rows, MAX_ROWS, replace=False))


def token_codes(df: pd.DataFrame, columns: list[str], rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
    """Each row as one code per column of ``columns`` (quantile bin or value) and, per column, the code that is no
    token (``-1``: none); at most ``MAX_COPY_CELLS`` cells (a random subset of the columns).
    """
    n = len(df)
    if n * len(columns) > MAX_COPY_CELLS:
        chosen = rng.choice(len(columns), max(1, MAX_COPY_CELLS // n), replace=False)
        columns = [columns[i] for i in np.sort(chosen)]
    codes = np.empty((n, len(columns)), dtype=np.int32)
    dominant = np.full(len(columns), -1, dtype=np.int64)
    for j, col in enumerate(columns):
        values = df[col]
        numeric = pd.api.types.is_numeric_dtype(values.dtype) or pd.api.types.is_datetime64_any_dtype(values.dtype)
        if numeric and not pd.api.types.is_bool_dtype(values.dtype) and values.nunique() > COPY_BINS:
            ranks = values.rank(method="min", pct=True).to_numpy(dtype=float)
            code = np.floor(np.nan_to_num(ranks, nan=1.0) * COPY_BINS - 1e-9).astype(np.int64)
            code[np.isnan(ranks)] = COPY_BINS
        else:
            code = pd.factorize(values, use_na_sentinel=False)[0]
        counts = np.bincount(code)
        if counts.max() > COPY_DOMINANT * n:
            dominant[j] = int(counts.argmax())
        codes[:, j] = code
    return codes, dominant


def minhash(codes: np.ndarray, dominant: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """MinHash signatures of the rows' token sets (a row without tokens keeps the largest value)."""
    n = len(codes)
    offsets = np.r_[0, np.cumsum(codes.max(axis=0).astype(np.int64) + 1)]
    rows, cols = np.nonzero(codes != dominant[None, :])
    tokens = offsets[cols] + codes[rows, cols]
    counts = np.bincount(rows, minlength=n)
    starts = np.r_[0, np.cumsum(counts)[:-1]]
    has = counts > 0
    top = np.iinfo(np.uint32).max
    signature = np.full((n, MINHASH_BANDS * MINHASH_ROWS), top, dtype=np.uint32)
    for k in range(signature.shape[1]):
        values = rng.integers(0, top, size=int(offsets[-1]), dtype=np.uint32)[tokens]
        signature[has, k] = np.minimum.reduceat(values, starts[has])
    return signature


def band_pairs(key: np.ndarray) -> np.ndarray:
    """Pairs of rows with the same band key: all pairs of a bucket of up to ``BUCKET_WINDOW`` rows; in a larger
    bucket each row with the next one and with the bucket's first row.
    """
    n = len(key)
    order = np.argsort(key, kind="stable")
    key = key[order]
    starts = np.flatnonzero(np.r_[True, key[1:] != key[:-1]])
    sizes = np.diff(np.r_[starts, n])
    small, leader = np.repeat(sizes <= BUCKET_WINDOW, sizes), np.repeat(starts, sizes)
    found = []
    for step in range(1, BUCKET_WINDOW):
        same = np.flatnonzero((key[step:] == key[:-step]) & (small[step:] | (step == 1)))
        if len(same) == 0:
            break
        found.append(np.column_stack([order[same], order[same + step]]))
    big = np.flatnonzero(~small & (np.arange(n) != leader))
    found.append(np.column_stack([order[leader[big]], order[big]]))
    pairs = np.sort(np.concatenate(found), axis=1).astype(np.int64)
    flat = np.unique(pairs[:, 0] * n + pairs[:, 1])
    return np.column_stack([flat // n, flat % n])


def similar_pairs(
    codes: np.ndarray, dominant: np.ndarray, rng: np.random.Generator
) -> tuple[np.ndarray, np.ndarray, np.ndarray, int]:
    """The pairs of rows that share a MinHash band and are near copies at the lowest similarity of ``COPY_LADDER``
    (checked exactly, band by band), their similarity and shared tokens, and how many pairs were checked.
    """
    n = len(codes)
    signature = minhash(codes, dominant, rng)
    weights = rng.integers(1, np.iinfo(np.int64).max, size=MINHASH_ROWS, dtype=np.uint64) | np.uint64(1)
    kept, checked = [], 0
    for b in range(MINHASH_BANDS):
        band = signature[:, b * MINHASH_ROWS : (b + 1) * MINHASH_ROWS].astype(np.uint64)
        with np.errstate(over="ignore"):
            pairs = band_pairs((band * weights).sum(axis=1, dtype=np.uint64))
        similarity, shared = jaccard(codes, dominant, pairs)
        near = (similarity >= min(COPY_LADDER)) & (shared >= COPY_MIN_SHARED)
        kept.append(np.column_stack([pairs[near], similarity[near], shared[near]]))
        checked += len(pairs)
    found = np.concatenate(kept)
    flat, first = np.unique(found[:, 0].astype(np.int64) * n + found[:, 1].astype(np.int64), return_index=True)
    return np.column_stack([flat // n, flat % n]), found[first, 2], found[first, 3], checked


def jaccard(codes: np.ndarray, dominant: np.ndarray, pairs: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """The Jaccard similarity of the token sets of each pair (1 for two rows without tokens), and the number of
    tokens they share.
    """
    present = codes != dominant[None, :]
    size = present.sum(axis=1)
    similarity, shared = np.empty(len(pairs)), np.empty(len(pairs), dtype=np.int64)
    step = max(1, 20_000_000 // max(codes.shape[1], 1))
    for start in range(0, len(pairs), step):
        a, b = pairs[start : start + step, 0], pairs[start : start + step, 1]
        both = ((codes[a] == codes[b]) & present[a]).sum(axis=1)
        union = size[a] + size[b] - both
        similarity[start : start + step] = np.where(union > 0, both / np.maximum(union, 1), 1.0)
        shared[start : start + step] = both
    return similarity, shared


def singletons(groups: np.ndarray, rows: np.ndarray) -> np.ndarray:
    """``groups`` with each of ``rows`` (a boolean mask) in a group of its own, renumbered from 0."""
    out = groups.copy()
    out[rows] = groups.max() + 1 + np.arange(rows.sum())
    return np.unique(out, return_inverse=True)[1].reshape(-1)


def near_copies(df: pd.DataFrame, columns: list[str], rng: np.random.Generator) -> tuple[dict[float, np.ndarray], dict]:
    """The near-copy clusters of the rows (a group id per row) at each similarity of ``COPY_LADDER``, and what went
    in. Rows with fewer than ``COPY_MIN_SHARED`` tokens, and the rows of clusters larger than ``COPY_MAX_CLUSTER``,
    are singletons (``rows_in_large_clusters`` counts the latter).
    """
    codes, dominant = token_codes(df, columns, rng)
    profiles, inverse = np.unique(codes, axis=0, return_inverse=True)
    inverse = inverse.reshape(-1)
    rich = np.flatnonzero((profiles != dominant[None, :]).sum(axis=1) >= COPY_MIN_SHARED)
    pairs, similarity, checked = np.zeros((0, 2), dtype=np.int64), np.zeros(0), 0
    if len(rich) >= 2:
        pairs, similarity, _, checked = similar_pairs(profiles[rich], dominant, rng)
        pairs = rich[pairs]
    few = ~np.isin(inverse, rich)
    clusters, large = {}, {}
    for threshold in COPY_LADDER:
        keep = similarity >= threshold
        edges = (np.ones(keep.sum()), (pairs[keep, 0], pairs[keep, 1]))
        graph = coo_matrix(edges, shape=(len(profiles), len(profiles)))
        groups = singletons(connected_components(graph, directed=False)[1][inverse], few)
        big = np.bincount(groups)[groups] > COPY_MAX_CLUSTER
        clusters[threshold], large[threshold] = singletons(groups, big), int(big.sum())
    info = {
        "columns_used": codes.shape[1],
        "rows_with_few_tokens": int(few.sum()),
        "distinct_rows": len(profiles),
        "pairs_checked": checked,
    }
    return clusters, info | {"rows_in_large_clusters": large}


def cluster_summary(groups: np.ndarray) -> dict:
    """Count, rows in clusters of two or more, and the largest cluster."""
    sizes = np.bincount(groups)
    return {
        "clusters": int((sizes > 0).sum()),
        "repeated_share": round(float(np.mean(sizes[groups] >= 2)), 4),
        "largest": int(sizes.max()),
    }


def size_counts(sizes: np.ndarray) -> dict[str, int]:
    """The number of clusters per size range of ``COPY_SIZES``."""
    counts = {}
    for low, high in COPY_SIZES:
        label = str(low) if low == high else f"{low}+" if high is None else f"{low}-{high}"
        inside = sizes >= low if high is None else (sizes >= low) & (sizes <= high)
        counts[label] = int(inside.sum())
    return counts


def copy_candidate(
    df: pd.DataFrame, columns: list[str], y: np.ndarray, n_classes: int, rng: np.random.Generator
) -> dict:
    """The near-copy candidate on ``columns`` (step 5 of the module docstring), shaped like a column candidate."""
    started = time.time()
    clusters, info = near_copies(df, columns, rng)
    large = info.pop("rows_in_large_clusters")
    groups = clusters[COPY_SIMILARITY]
    sizes = np.bincount(groups)
    rows, pred = leave_one_out(groups, y, n_classes)
    s_id = skill(y[rows], pred, n_classes) if len(rows) >= 2 else float("nan")
    summary = cluster_summary(groups)
    cand = {
        "column": NEAR_COPIES,
        "dtype": "clusters",
        "similarity": COPY_SIMILARITY,
        "values": summary["clusters"],
        "mean_rows_per_value": round(len(groups) / max(summary["clusters"], 1), 2),
        "repeated_share": summary["repeated_share"],
        "largest": summary["largest"],
        "cluster_sizes": size_counts(sizes),
        "s_id": s_id,
        "s_smooth": 0.0,
        "s_identity": s_id,
        "known_group": False,
        "rows_in_large_clusters": large[COPY_SIMILARITY],
        "ladder": [
            {"similarity": t, **cluster_summary(clusters[t]), "rows_in_large_clusters": large[t]} for t in COPY_LADDER
        ],
        **info,
        "_groups": groups,
        "_rows": rows,
    }
    cand["eligible"] = bool(
        cand["repeated_share"] >= COPY_ELIGIBLE_SHARE and np.nan_to_num(s_id, nan=-1) >= MIN_IDENTITY
    )
    cand["testable"] = bool(cand["repeated_share"] >= COPY_MIN_SHARE and cand["largest"] <= MAX_TOP_SHARE * len(y))
    cand["seconds"] = round(time.time() - started, 1)
    return cand


def column_hash(values: pd.Series, seed: int, *, permute: bool) -> np.ndarray:
    """A random 64-bit number per distinct value of a column (missing is a value), one per row; with ``permute``, in
    a random row order that ``seed`` fixes.
    """
    rng = np.random.default_rng(seed)
    codes = pd.factorize(values, use_na_sentinel=False)[0]
    hashed = rng.integers(1, np.iinfo(np.uint64).max, size=int(codes.max()) + 1, dtype=np.uint64)[codes]
    return hashed[rng.permutation(len(hashed))] if permute else hashed


def key_stats(key: np.ndarray, rows: np.ndarray) -> tuple[np.ndarray, dict]:
    """The group id of each row by ``key``, and the counts of step 6 (``rows``: an id per distinct whole row)."""
    groups = pd.factorize(key)[0].astype(np.int64)
    sizes = np.bincount(groups)
    width = int(rows.max()) + 1
    distinct = np.bincount(pd.unique(groups * width + rows) // width, minlength=len(sizes))
    varying = (distinct >= 2) & (sizes <= COPY_MAX_CLUSTER)
    return groups, {
        "values": len(sizes),
        "repeated_share": round(float(np.mean(sizes[groups] >= 2)), 4),
        "varying_share": round(float(np.mean(varying[groups])), 4),
        "varying_keys": int(varying.sum()),
        "rows_in_large_keys": int(np.sum(sizes[groups] > COPY_MAX_CLUSTER)),
        "largest": int(sizes.max()),
    }


def key_name(left_out: list[str]) -> str:
    """The name of a composite key in the output."""
    return f"(all but {', '.join(left_out)})"


class KeyHashes:
    """Exact hashes of the composite keys of step 6: a column's hash per row, as is or with the column's rows permuted
    on their own (the baseline), and their sum over all columns; a key is the sum minus its left-out columns.
    """

    def __init__(self, df: pd.DataFrame, columns: list[str]) -> None:
        """Hash ``columns`` of ``df``."""
        self.df, self.columns = df, columns
        self.keep = len(df) * len(columns) <= KEY_CACHE_CELLS
        self.store: dict = {}
        self.total: dict = {}
        self.rows: dict = {}

    def summed(self, *, permute: bool) -> tuple[np.ndarray, np.ndarray]:
        """The sum of all column hashes per row and an id per distinct row (computed on first use)."""
        if permute not in self.total:
            total = np.zeros(len(self.df), dtype=np.uint64)
            for j in range(len(self.columns)):
                total += self.column(j, permute=permute)
            self.total[permute] = total
            self.rows[permute] = pd.factorize(total)[0].astype(np.int64)
        return self.total[permute], self.rows[permute]

    def column(self, j: int, *, permute: bool) -> np.ndarray:
        """The hash of column ``j`` per row (kept when the frame is small)."""
        if (j, permute) in self.store:
            return self.store[(j, permute)]
        hashed = column_hash(self.df[self.columns[j]], j, permute=permute)
        if self.keep:
            self.store[(j, permute)] = hashed
        return hashed

    def stats(self, left: tuple[int, ...], *, permute: bool = False) -> tuple[np.ndarray, dict]:
        """:func:`key_stats` of the key of all columns but ``left``."""
        total, rows = self.summed(permute=permute)
        key = total.copy()
        for j in left:
            key -= self.column(j, permute=permute)  # uint64 arithmetic wraps, so this is the others' sum
        return key_stats(key, rows)


def key_sets(p: int, k: int, n: int, rng: np.random.Generator) -> list[tuple[int, ...]] | None:
    """The sets of ``k`` of ``p`` columns to leave out (a random subset when one column at a time exceeds the
    budget), or None when the key would have fewer than two columns or ``k > 1`` exceeds the budget.
    """
    if p - k < 2 or (k > 1 and n * comb(p, k) > KEY_BUDGET):
        return None
    sets = list(combinations(range(p), k))
    if n * len(sets) > KEY_BUDGET:
        sets = [sets[i] for i in np.sort(rng.choice(len(sets), max(1, KEY_BUDGET // n), replace=False))]
    return sets


def repeats(stats: dict, n: int) -> bool:
    """Whether a key's rows repeat enough to count (step 6), before the comparison with chance."""
    return (
        stats["varying_keys"] >= MIN_GROUPS
        and stats["varying_share"] >= KEY_MIN_SHARE
        and stats["largest"] <= MAX_TOP_SHARE * n
    )


def composite_keys(df: pd.DataFrame, columns: list[str], rng: np.random.Generator) -> tuple[list[dict], dict]:
    """The composite keys of step 6 that count, most rows above chance first, with their group ids, and the search."""
    started = time.time()
    n = len(df)
    columns = [c for c in columns if pd.factorize(df[c], use_na_sentinel=False)[0].max() > 0]
    fine = np.array([df[c].nunique() >= MIN_GROUPS for c in columns], dtype=bool)
    hashes = KeyHashes(df, columns)
    found, best, searched, checked, possible = [], ((), -1.0), [], 0, 0
    for k in range(1, KEY_MAX_LEFT_OUT + 1):
        sets = key_sets(len(columns), k, n, rng)
        if sets is None:
            break
        searched.append(k)
        possible += comb(len(columns), k)
        checked += len(sets)
        for left in sets:
            stats = hashes.stats(left)[1]
            best = max(best, (left, stats["varying_share"]), key=lambda b: b[1])
            if not fine.sum() > fine[list(left)].sum() or not repeats(stats, n):
                continue
            baseline = hashes.stats(left, permute=True)[1]["varying_share"]
            if baseline <= KEY_CHANCE * stats["varying_share"]:
                found.append({"left": left, **stats, "baseline_share": baseline})
        if found:
            break
    found.sort(key=lambda c: -(c["varying_share"] - c["baseline_share"]))
    keys = []
    for c in found[:N_KEYS]:
        left = c.pop("left")
        left_out = [columns[j] for j in left]
        keys.append({"column": key_name(left_out), "left_out": left_out, **c, "_groups": hashes.stats(left)[0]})
    search = {
        "left_out": searched,
        "columns": len(columns),
        "keys_checked": checked,
        "keys": possible,
        "counted": len(found),
        "best": key_name([columns[j] for j in best[0]]) if best[0] else None,
        "best_varying_share": best[1] if best[0] else None,
        "seconds": round(time.time() - started, 1),
    }
    return keys, search


def key_candidates(
    df: pd.DataFrame,
    columns: list[str],
    y: np.ndarray,
    n_classes: int,
    known: list[str],
    rng: np.random.Generator,
) -> tuple[list[dict], dict]:
    """The composite keys (step 6), shaped like column candidates, with ``s_id`` and eligibility, and the search."""
    keys, search = composite_keys(df, columns, rng)
    known_groups = df.groupby(known, sort=False, dropna=False, observed=True).ngroup().to_numpy() if known else None
    for cand in keys:
        groups = cand["_groups"]
        rows, pred = leave_one_out(groups, y, n_classes)
        cand["s_id"] = skill(y[rows], pred, n_classes) if len(rows) >= 2 else float("nan")
        cand["s_smooth"] = 0.0
        cand["s_identity"] = cand["s_id"]
        cand["dtype"] = "composite key"
        cand["key_columns"] = search["columns"] - len(cand["left_out"])
        cand["mean_rows_per_value"] = round(len(groups) / max(cand["values"], 1), 2)
        cand["known_group"] = bool(
            known_groups is not None
            and len(np.unique(known_groups)) == cand["values"] == len(pd.unique(groups * len(groups) + known_groups))
        )
        cand["eligible"] = bool(np.nan_to_num(cand["s_id"], nan=-1) >= MIN_IDENTITY)
        cand["_rows"] = rows
    return keys, search


def column_candidates(df: pd.DataFrame, y: np.ndarray, n_classes: int, skip: list[str], known: list[str]) -> list:
    """The candidate columns (step 1) with their ``s_id`` (step 2), best first."""
    scored = []
    for col in df.columns:
        if col in skip or not is_candidate(df[col]):
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
    return scored


def rank(
    scored: list,
    df: pd.DataFrame,
    X: pd.DataFrame,
    by_name: dict,
    y: np.ndarray,
    n_classes: int,
    target: str,
    n_jobs: int,
    rng: np.random.Generator,
) -> list:
    """Steps 2-3 for the scored candidates: smooth part, attributes and eligibility; eligible ones first."""
    for cand in scored:
        groups, rows = cand["_groups"], cand["_rows"]
        if cand["column"] not in by_name:  # a text column: no smooth part
            cand["s_smooth"] = 0.0
        else:
            keep = rows if len(rows) <= MAX_ROWS else np.sort(rng.choice(rows, MAX_ROWS, replace=False))
            one = X[[by_name[cand["column"]]]].iloc[keep].reset_index(drop=True)
            pred, _ = oof(one, y[keep], n_classes, splits(y[keep], groups[keep], n_classes), n_jobs)
            cand["s_smooth"] = skill(y[keep], pred, n_classes)
        cand["s_identity"] = cand["s_id"] - cand["s_smooth"]
        static, aliases = attributes(df, groups, [cand["column"], target], rng)
        cand["static"] = len(static)
        cand["static_columns"] = static[:10]
        cand["aliases"] = aliases[:5]
        cand["eligible"] = bool(
            np.nan_to_num(cand["s_identity"], nan=-1) >= MIN_IDENTITY
            and (cand["static"] >= MIN_STATIC or np.nan_to_num(cand["s_id"], nan=-1) >= STRONG_ID)
        )
    return sorted(scored, key=lambda c: (not c["eligible"], -np.nan_to_num(c["s_identity"], nan=-1)))


def split_gap(
    cand: dict, X: pd.DataFrame, y: np.ndarray, n_classes: int, n_jobs: int, rng: np.random.Generator, cache: dict
) -> None:
    """Step 4 for one candidate: random against grouped folds (moved folds for the near copies); the random folds
    of the full frame are cached.
    """
    keep = subsample(cand["_groups"], rng)
    Xs, ys, gs = X.iloc[keep].reset_index(drop=True), y[keep], cand["_groups"][keep]
    full = len(keep) == len(y)
    if full and "random" in cache:
        random_folds = cache["random"]
    else:
        _, random_folds = oof(Xs, ys, n_classes, splits(ys, None, n_classes), n_jobs)
        if full:
            cache["random"] = random_folds
    grouped = moved(ys, gs, n_classes) if cand["column"] == NEAR_COPIES else splits(ys, gs, n_classes)
    _, group_folds = oof(Xs, ys, n_classes, grouped, n_jobs)
    cand["skill_random"] = float(np.nanmean(random_folds))
    cand["skill_grouped"] = float(np.nanmean(group_folds))
    cand["gap"] = cand["skill_random"] - cand["skill_grouped"]
    cand["gap_fold_sd"] = float(np.nanstd(np.subtract(random_folds, group_folds)))
    cand["rows_tested"] = len(keep)
    large = cand["gap"] >= MIN_RELATIVE_GAP * cand["skill_random"]
    if "left_out" in cand:  # a composite key: or a gap that raises the error left by KEY_ERROR_RISE
        large = large or cand["gap"] >= KEY_ERROR_RISE * (1.0 - cand["skill_random"])
    cand["hit"] = bool(cand["eligible"] and cand["gap"] >= MIN_GAP and large)


def recurrence(cand: dict, shipped: list[tuple[np.ndarray, np.ndarray]]) -> None:
    """For a temporal task: the share of test rows whose value (or cluster) occurs among the training rows."""
    groups = cand["_groups"]
    seen = [float(np.isin(groups[test], groups[train]).mean()) for train, test in shipped if len(test)]
    cand["test_rows_seen"] = float(np.mean(seen)) if seen else float("nan")
    cand["test_rows_seen_range"] = [min(seen), max(seen)] if seen else []
    cand["splits"] = len(seen)


def probe(name: str, root: Path, *, built: bool, n_jobs: int, include_grouped: bool) -> dict:
    """Run the probe of the module docstring on one dataset."""
    started = time.time()
    container, origin = load(name, root, built=built)
    task, grouping = container.task_metadata, container.grouping
    regime = "temporal" if task.time_on is not None else "grouped" if grouping is not None else "iid"
    result: dict = {"name": name, "regime": regime, "origin": origin}
    if regime == "grouped" and not include_grouped:
        return result | {"skipped": f"{regime} task"}
    df = container.dataset
    target = df[task.target_column_name]
    if task.problem_type == "regression":
        y, n_classes = target.to_numpy(dtype=float), 0
    else:
        y = pd.factorize(target, sort=True)[0]
        n_classes = int(y.max()) + 1
    known = as_column_list(grouping.on) if grouping is not None else []
    result |= {"rows": len(df), "known_group_columns": known}
    skip = [task.target_column_name] + ([task.time_on] if regime == "temporal" else [])

    scored = column_candidates(df, y, n_classes, skip, known)
    if regime == "temporal":  # no gap test: only the scored candidates need model inputs
        X, names, _ = features(df[[c["column"] for c in scored[:MAX_SCORED]]], [])
    else:
        X, names, _ = features(df, [task.target_column_name])
    by_name = dict(zip(names, X.columns, strict=True))
    rng = np.random.default_rng(0)
    ranked = rank(scored[:MAX_SCORED], df, X, by_name, y, n_classes, task.target_column_name, n_jobs, rng)
    tokens = [c for c in df.columns if c not in skip and c not in known]
    copies = copy_candidate(df, tokens, y, n_classes, np.random.default_rng(1))
    key_columns = [c for c in df.columns if c != task.target_column_name and c not in known]
    keys, search = key_candidates(df, key_columns, y, n_classes, known, np.random.default_rng(2))

    if regime == "temporal":
        shipped = [
            (np.asarray(train), np.asarray(test))
            for folds in container.experiment_metadata.splits.values()
            for train, test in folds.values()
        ]
        for cand in [*ranked[:N_TESTED], *keys, copies]:
            recurrence(cand, shipped)
    else:
        cache: dict = {}
        for cand in ranked[:N_TESTED]:
            split_gap(cand, X, y, n_classes, n_jobs, rng, cache)
        for cand in keys:
            split_gap(cand, X, y, n_classes, n_jobs, np.random.default_rng(2), cache)
        if copies["testable"]:
            split_gap(copies, X, y, n_classes, n_jobs, np.random.default_rng(1), cache)
    for cand in [*scored, *keys, copies]:
        cand.pop("_groups"), cand.pop("_rows")
    result["candidates"] = len(scored)
    result["scored"] = ranked
    result["composite_keys"] = keys
    result["composite_search"] = search
    result["near_copies"] = copies
    result["hits"] = [c["column"] for c in [*ranked, *keys, copies] if c.get("hit")]
    result["entity_like"] = [c["column"] for c in [*ranked, *keys] if c["eligible"]]
    result["seconds"] = round(time.time() - started)
    return result


def _outcome(c: dict) -> str:
    """The gap (IID) or the recurrence across the cutoff (temporal) of a candidate, as text."""
    if "gap" in c:
        return f", gap {c['gap']:+.3f} (random {c['skill_random']:.3f}, grouped {c['skill_grouped']:.3f})"
    if "test_rows_seen" in c and c["splits"]:
        low, high = c["test_rows_seen_range"]
        return f", test rows seen in train {c['test_rows_seen']:.1%} ({low:.1%}-{high:.1%}, {c['splits']} splits)"
    return ""


def _key_lines(result: dict) -> list[str]:
    """The composite keys of one dataset, or what the search checked when none counts."""
    search = result.get("composite_search")
    if not search:
        return []
    lines = []
    for c in result["composite_keys"]:
        mark = " [known group]" if c["known_group"] else ""
        lines.append(
            f"   {c['column']}{mark}: {c['values']} keys of {c['key_columns']} columns, "
            f"{c['mean_rows_per_value']} rows each, {c['varying_share']:.1%} of the rows share a key with a row "
            f"that differs ({c['baseline_share']:.1%} with independent columns), s_id {c['s_id']:.3f}{_outcome(c)}"
            + (
                f"; {c['rows_in_large_keys']} rows of keys over {COPY_MAX_CLUSTER} left out"
                if c["rows_in_large_keys"]
                else ""
            )
        )
    if search["left_out"]:
        scope = {1: "one column", 2: "one or two columns"}.get(max(search["left_out"]), "a few columns")
        best = f"; best {search['best']} {search['best_varying_share']:.1%}" if search["best"] else ""
        found = f"{search['counted']} count" if search["counted"] else "none counts"
        lines.append(
            f"   (keys of all but {scope}): {found} ({search['keys_checked']} of {search['keys']} keys, "
            f"{search['columns']} columns{best}), {search['seconds']} s"
        )
    else:
        lines.append(f"   (keys of all but one column): not searched ({search['columns']} columns)")
    return lines


def render(result: dict) -> str:
    """A short text summary of one dataset."""
    lines = [f"== {result['name']} ({result['regime']}, {result.get('rows', '?')} rows)"]
    if "skipped" in result or "error" in result:
        return lines[0] + f": {result.get('skipped') or result.get('error')}"
    if result["regime"] == "temporal":
        lines.append(f"   candidates {result['candidates']}; entity-like {result['entity_like']} (temporal: no hits)")
    else:
        lines.append(f"   candidates {result['candidates']}; hits {result['hits']}")
    for c in result["scored"][:N_TESTED]:
        mark = " [known group]" if c["known_group"] else ""
        lines.append(
            f"   {c['column']}{mark}: {c['values']} values, {c['mean_rows_per_value']} rows each, "
            f"s_id {c['s_id']:.3f}, s_smooth {c['s_smooth']:.3f}, "
            f"{c['static']} attributes {c['static_columns'][:4]}{_outcome(c)}"
        )
    lines.extend(_key_lines(result))
    c = result["near_copies"]
    ladder = ", ".join(f"{s['similarity']}: {s['clusters']} ({s['repeated_share']:.1%})" for s in c["ladder"])
    sizes = ", ".join(f"{k}: {v}" for k, v in c["cluster_sizes"].items() if v)
    left_out = []
    if c["rows_with_few_tokens"]:
        left_out.append(f"{c['rows_with_few_tokens']} rows with fewer than {COPY_MIN_SHARED} tokens")
    if c["rows_in_large_clusters"]:
        left_out.append(f"{c['rows_in_large_clusters']} rows of clusters over {COPY_MAX_CLUSTER}")
    lines.append(
        f"   {NEAR_COPIES} at {c['similarity']}: {c['values']} clusters, {c['repeated_share']:.1%} of the rows in "
        f"clusters of 2+, largest {c['largest']} (sizes {sizes or 'none'}), s_id {c['s_id']:.3f}{_outcome(c)}; "
        f"by similarity {ladder}; {c['columns_used']} columns, {c['seconds']} s"
        + "".join(f"; {note} left single" for note in left_out)
    )
    return "\n".join(lines)


def _safe(name: str, root: Path, **kwargs) -> dict:
    try:
        return probe(name, root, **kwargs)
    except Exception as error:  # noqa: BLE001 - one failing dataset must not stop a sweep
        return {"name": name, "regime": "?", "error": f"{type(error).__name__}: {error}"[:300]}


def _summary_row(r: dict) -> str:
    """One line of ``summary.md``."""
    if r.get("scored") is None:
        top = r.get("skipped") or r.get("error", "")
    else:
        parts = []
        for c in [*r["scored"][:1], *r.get("composite_keys", [])[:1], r["near_copies"]]:
            if "gap" in c:
                parts.append(f"{c['column']} gap {c['gap']:+.3f}")
            elif "test_rows_seen" in c:
                parts.append(f"{c['column']} seen {c['test_rows_seen']:.1%}")
            elif c["column"] == NEAR_COPIES:
                parts.append(f"{c['column']} {c['repeated_share']:.1%} of rows")
        top = "; ".join(parts)
    hits = ", ".join(r.get("hits", []))
    return f"| `{r['name']}` | {r['regime']} | {r.get('candidates', '')} | {hits} | {top} |"


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
    names = sorted(discover_datasets(args.root, strict=False)) if args.all else args.names
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
        header = "| dataset | regime | candidates | hits | top candidate; composite key; near copies |\n"
        header += "|---|---|---|---|---|\n"
        (args.out / "summary.md").write_text(header + "\n".join(_summary_row(r) for r in results) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
