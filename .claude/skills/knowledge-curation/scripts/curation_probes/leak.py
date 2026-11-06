"""Leak probes: what a model learns from the data that it should not.

Tooling-independent: ``run`` takes a pandas frame, its target column and problem type, the splits as
``(train_idx, test_idx)`` row positions and the group columns (which are not features), fits untuned LightGBM on the
first ``n_splits`` splits, prints each number as soon as it is known and returns them all:

* the score with all features (ROC AUC, one-vs-rest for multiclass, or R^2), and of a depth-2 and a depth-3
  decision tree: a shallow tree close to the full model means the label is a rule over a few columns (a definition,
  a lookup, or a label assigned from the features);
* the score of each feature alone, and of each column's missing-value indicator alone, best first;
* the score without each of the three strongest single features (a drop-one test misses a column that has a
  copy, such as kick's ``WheelType`` and ``WheelTypeID``: drop such columns together);
* on every split given (not only the probed ones, and every row), the share of test rows whose feature vector has an
  exact copy in train, and how the copies split by label: the same label only or another label only, each with one
  copy or two or more, and both labels (``copy_counts``); when the data has string or datetime columns, the same with
  them included; and for each string column of more than 50 distinct values the share of test rows whose value occurs
  in train on the first split (a copy at the level of a SMILES string or a text);
* each such string column alone, and all features with the string columns, encoded as in the task probes (TF-IDF +
  SVD fitted on the train side; character n-grams for one-token strings such as a SMILES): a text whose content
  gives the label away scores close to the full model on its own;
* the 1-nearest-neighbour label agreement (R^2 for regression) for the closest tenth of the test rows and for
  all of them, against chance;
* for a binary target, the ROC AUC of a label-free score: each row's distance to its nearest other row.
* for a classification target, the score of the number format alone (probe 17): the decimals each value of a float
  column is written with, all columns together and the three best alone. Classes recorded differently give
  themselves away here (gallstone_disease 0.947 before the fix, 0.557 after).

With a training weight (``sample_weight``: a rate's realized denominator, such as the years insured), every fit is
trained with it as each row's weight and every R^2 and ROC AUC weights the test rows by it, the 1-NN R^2 and the
distance score included; the screen, the copies and the 1-NN label agreement stay counts of rows.

``fill_counts`` (probe 18) needs the rows in the source's order, which ``run`` does not get: it counts, per column and
class, the cells that lie on a straight line between the cells above and below, the trace of gaps filled by
interpolation. Run it on the raw table.

``weight_proxy`` (probe 22) asks whether the features carry a realized weight, such as the time on risk of a rate
target that a claim can cut short: a LightGBM of the weight on the features, the task's metric with the weight added as
a feature against the honest fit (the leak reference), each top feature's gain through the weight with its SD over
splits and seeds, and for a Gini metric the score of 1/weight alone. ``weight_proxy_lines`` prints it.

The raw state has four more probes, which read the table before ``_clean`` and, through the lineage (the raw
position of each curated row), what ``_clean`` did to it: ``row_order`` (probe 10, the target in the source's row
order), ``removed_rows`` (probe 19, the target of the rows ``_clean`` removed against the kept ones),
``dropped_column_proxies`` (probe 20, each raw column the definition drops, alone against the target on the shipped
splits) and ``raw_copies`` (probe 21, copies before deduplication, by label). ``raw_lines`` prints them.

``target_by_period`` (probe 13) needs the time of each row: it sets the target of the newest periods (an event rate,
the class shares, a duration's p50 and p90, a count's zero share, the rows per day) against the band the earlier
periods give, the test for a target right-censored at the release end. It fits no model.

Wide data: with more than ``max_single_features`` columns, only that many enter the single-feature fits, and the
output says how many were screened out. The screen keeps the columns that best explain the label alone on the first
split's training side: a step function over 10 quantile bins (the levels of a categorical of at most 10; missing
values are a bin of their own), scored by mutual information (the share of variance for regression) less its expected
value without signal. A categorical of more levels gets the out-of-fold score of its per-level label distribution, in
the same units. Against full scans, the default keeps all 8 best single features of coad_colon_adenocarcinoma and
ov_ovarian_cancer, 7 of lgg_low_grade_glioma's (its best score included) and the 50 best of
mercedes_benz_greener_manufacturing (370 categoricals); ranking by the gain of one LightGBM fit missed coad's 41 best.
Columns with the same missing values share one missing-indicator fit, and more than ``max_single_features``
distinct patterns are screened the same way. The all-feature, shallow-tree and drop-one fits use every column.

A multiclass ROC AUC is the mean of the one-vs-rest ROC AUCs over the classes present in the test fold (a grouped or
temporal fold can lack a class); a class the training side lacks gets probability 0. String and datetime columns
are not inputs of the other fits, group columns are not features, and train and test rows are capped at
``max_rows`` each. The numbers are indicative (untuned models, a few splits) and meant for comparing the data with a
suspected fix.
"""

from __future__ import annotations

import lightgbm as lgb
import numpy as np
import pandas as pd
from sklearn.metrics import r2_score, roc_auc_score
from sklearn.neighbors import NearestNeighbors
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor

from curation_probes import weights
from curation_probes.text import encode_text

BINS = 10
"""Quantile bins of the screen's step function; a categorical of more levels is scored by ``level_score``."""
WIDE_STRING = 50
"""A string column with more distinct values than this gets its own train-overlap line."""


def auc(y_true: np.ndarray, proba: np.ndarray, classes: np.ndarray, weight: np.ndarray | None = None) -> float:
    """ROC AUC of ``proba`` (one column per entry of ``classes``); for more than two classes, the mean one-vs-rest
    ROC AUC over the classes present in ``y_true``. NaN when ``y_true`` holds one class only. ``weight``: each row's
    weight, or None.
    """
    present = [k for k, c in enumerate(classes) if np.any(y_true == c)]
    if len(present) < 2:
        return float("nan")
    if len(classes) == 2:  # binary
        return float(roc_auc_score(y_true == classes[1], proba[:, 1], sample_weight=weight))
    return float(np.mean([roc_auc_score(y_true == classes[k], proba[:, k], sample_weight=weight) for k in present]))


def class_proba(model, data: pd.DataFrame, classes: np.ndarray) -> np.ndarray:
    """The model's class probabilities, one column per entry of ``classes`` (0 for a class it was not trained on)."""
    out = np.zeros((len(data), len(classes)))
    position = {c: i for i, c in enumerate(classes)}
    out[:, [position[c] for c in model.classes_]] = model.predict_proba(data)
    return out


def score(
    data: pd.DataFrame,
    y: pd.Series,
    pairs: list,
    *,
    regression: bool,
    n_jobs: int = 8,
    weight: np.ndarray | None = None,
) -> float:
    """Mean ROC AUC (one-vs-rest for multiclass, see ``auc``) or R^2 of an untuned LightGBM over the split pairs;
    with ``weight`` (one per row of ``data``), fitted and scored with it.
    """
    classes = None if regression else np.unique(y.to_numpy())
    return float(
        np.nanmean(
            [
                fit_score(
                    data.iloc[tr],
                    data.iloc[te],
                    y.iloc[tr],
                    y.iloc[te],
                    classes,
                    regression=regression,
                    n_jobs=n_jobs,
                    w_train=weights.take(weight, tr),
                    w_test=weights.take(weight, te),
                )
                for tr, te in pairs
            ]
        )
    )


def fit_score(
    x_train,
    x_test,
    y_train,
    y_test,
    classes,
    *,
    regression: bool,
    n_jobs: int,
    w_train: np.ndarray | None = None,
    w_test: np.ndarray | None = None,
) -> float:
    """One untuned LightGBM fit, scored as in ``score``; ``w_train`` and ``w_test``: the rows' weights, or None."""
    model = (lgb.LGBMRegressor if regression else lgb.LGBMClassifier)(n_estimators=200, verbose=-1, n_jobs=n_jobs)
    # LightGBM refuses names with JSON characters (a spectrum's `M/Z:800.32`); the fit needs no names
    names = [f"f{i}" for i in range(x_train.shape[1])]
    x_train, x_test = x_train.set_axis(names, axis=1), x_test.set_axis(names, axis=1)
    weights.fit(model, x_train, y_train, w_train)
    if regression:
        return r2_score(y_test, model.predict(x_test), sample_weight=w_test)
    return auc(y_test.to_numpy(), class_proba(model, x_test, classes), classes, w_test)


def text_score(
    df: pd.DataFrame,
    columns: list[str],
    base: pd.DataFrame | None,
    y: pd.Series,
    pairs: list,
    *,
    regression: bool,
    n_jobs: int,
    weight: np.ndarray | None = None,
) -> float:
    """``score`` with the string ``columns`` encoded per split on its train side (and ``base`` next to them)."""
    classes = None if regression else np.unique(y.to_numpy())
    out = []
    for tr, te in pairs:
        t_tr, t_te, blocks = encode_text(df, columns, tr, te)
        if not blocks:
            return float("nan")
        if base is not None:
            t_tr = pd.concat([base.iloc[tr].reset_index(drop=True), t_tr], axis=1)
            t_te = pd.concat([base.iloc[te].reset_index(drop=True), t_te], axis=1)
        w_tr, w_te = weights.take(weight, tr), weights.take(weight, te)
        out.append(
            fit_score(
                t_tr,
                t_te,
                y.iloc[tr],
                y.iloc[te],
                classes,
                regression=regression,
                n_jobs=n_jobs,
                w_train=w_tr,
                w_test=w_te,
            )
        )
    return float(np.nanmean(out))


def tree_score(
    data: pd.DataFrame, y: pd.Series, pairs: list, *, regression: bool, depth: int, weight: np.ndarray | None = None
) -> float:
    """Mean ROC AUC (one-vs-rest for multiclass, see ``auc``) or R^2 of a decision tree of the given depth."""
    numeric = data.apply(
        lambda s: s.cat.codes.where(s.cat.codes >= 0) if isinstance(s.dtype, pd.CategoricalDtype) else s
    ).astype(float)
    classes = None if regression else np.unique(y.to_numpy())
    out = []
    for tr, te in pairs:
        model = (DecisionTreeRegressor if regression else DecisionTreeClassifier)(max_depth=depth, random_state=0)
        weights.fit(model, numeric.iloc[tr], y.iloc[tr], weights.take(weight, tr))
        if regression:
            out.append(r2_score(y.iloc[te], model.predict(numeric.iloc[te]), sample_weight=weights.take(weight, te)))
            continue
        proba = class_proba(model, numeric.iloc[te], classes)
        out.append(auc(y.iloc[te].to_numpy(), proba, classes, weights.take(weight, te)))
    return float(np.nanmean(out))


def step_bins(data: pd.DataFrame) -> np.ndarray:
    """The screen's bin of every cell: quantile bins ``0..BINS-1`` for a number, the level of a categorical (of at
    most ``BINS`` levels; ``level_score`` scores one of more), and ``BINS`` for a missing value.
    """
    categorical = [isinstance(dtype, pd.CategoricalDtype) for dtype in data.dtypes]
    out = np.empty(data.shape, dtype=np.int16)
    numeric = [i for i, is_cat in enumerate(categorical) if not is_cat]
    if numeric:
        pct = data.iloc[:, numeric].astype(float).rank(pct=True).to_numpy()  # in (0, 1], NaN stays NaN
        out[:, numeric] = np.where(np.isnan(pct), BINS, np.minimum(np.ceil(np.nan_to_num(pct) * BINS) - 1, BINS - 1))
    for i in (i for i, is_cat in enumerate(categorical) if is_cat):
        codes = data.iloc[:, i].cat.codes.to_numpy()
        out[:, i] = np.where(codes < 0, BINS, np.minimum(codes, BINS + 1))
    return out


def level_score(
    codes: np.ndarray, target: np.ndarray, *, regression: bool, folds: int = 5, smooth: float = 20.0
) -> float:
    """Out-of-fold score of a categorical of many levels: each level's label distribution (mean for regression),
    shrunk towards the prior by ``smooth`` rows, scored on held-out rows as the log-likelihood gain over the prior
    per row (comparable with mutual information), or as R^2. A level seen in one fold only says nothing.
    """
    levels = np.where(codes < 0, codes.max() + 1, codes)
    n_levels, n = levels.max() + 1, len(levels)
    fold = np.random.default_rng(0).permutation(n) % folds
    gain, pred = 0.0, np.zeros(n)
    for f in range(folds):
        fit, held = fold != f, fold == f
        count = np.bincount(levels[fit], minlength=n_levels)
        if regression:
            mean = target[fit].mean()
            sums = np.bincount(levels[fit], weights=target[fit], minlength=n_levels)
            pred[held] = ((sums + smooth * mean) / (count + smooth))[levels[held]]
            continue
        k = target.max() + 1
        prior = (np.bincount(target[fit], minlength=k) + 1) / (fit.sum() + k)
        joint = np.bincount(levels[fit] * k + target[fit], minlength=n_levels * k).reshape(n_levels, k)
        proba = (joint + smooth * prior) / (count[:, None] + smooth)
        gain += np.log(proba[levels[held], target[held]] / prior[target[held]]).sum()
    if regression:
        total = ((target - target.mean()) ** 2).sum()
        return float(1 - ((target - pred) ** 2).sum() / total) if total else 0.0
    return gain / n


def screen(data: pd.DataFrame, y: pd.Series, *, regression: bool) -> pd.Series:
    """How well each column alone explains ``y`` (the rows of ``data``) as a step function over ``step_bins``:
    mutual information less its expected value without signal (``(bins - 1)(classes - 1) / 2n``), or for
    regression the share of variance less ``(bins - 1) / (n - 1)``; a categorical of more than ``BINS`` levels gets
    its ``level_score``. Higher is more informative.
    """
    slots, n = step_bins(data), len(data)
    target = y.to_numpy(dtype=float) if regression else pd.factorize(y.to_numpy())[0]
    Y = (target - target.mean())[:, None] if regression else np.eye(target.max() + 1)[target]
    used, between, info = (np.zeros(data.shape[1]) for _ in range(3))
    prior = Y.mean(axis=0)
    for s in range(BINS + 2):
        member = (slots == s).astype(float)
        size = member.sum(axis=0)
        used += size > 0
        sums = Y.T @ member  # classes (or 1) x columns
        with np.errstate(divide="ignore", invalid="ignore"):
            if regression:
                between += np.where(size > 0, sums[0] ** 2 / size, 0.0)
            else:
                joint = sums / n
                info += np.nansum(np.where(joint > 0, joint * np.log(joint / (prior[:, None] * size / n)), 0.0), axis=0)
    if regression:
        total = float((Y[:, 0] ** 2).sum())
        value = (between / total if total else np.zeros_like(between)) - (used - 1) / max(n - 1, 1)
    else:
        value = info - (used - 1) * (Y.shape[1] - 1) / (2 * n)
    for i, dtype in enumerate(data.dtypes):
        if isinstance(dtype, pd.CategoricalDtype) and len(dtype.categories) > BINS:
            value[i] = level_score(data.iloc[:, i].cat.codes.to_numpy(), target, regression=regression)
    return pd.Series(value, index=data.columns)


def keep_most_informative(data: pd.DataFrame, y: pd.Series, rows: np.ndarray, limit: int, *, regression: bool) -> list:
    """The columns of ``data`` to fit one by one: all of them, or the ``limit`` best by ``screen`` on ``rows``."""
    if data.shape[1] <= limit:
        return list(data.columns)
    ranked = screen(data.iloc[rows], y.iloc[rows], regression=regression).sort_values(ascending=False, kind="stable")
    return list(ranked.index[:limit])


def neighbour_space(X: pd.DataFrame) -> np.ndarray:
    """Standardised numeric columns plus one-hot categoricals with at most 50 levels."""
    num = X.select_dtypes("number")
    cats = [c for c in X.columns if c not in num and X[c].nunique() <= 50]
    parts = [((num - num.mean()) / num.std()).fillna(0), pd.get_dummies(X[cats], dummy_na=True) if cats else None]
    return pd.concat(parts, axis=1).to_numpy(dtype=float)


def say(line: str) -> None:
    """Print one line of the report as soon as it is known."""
    print(line, flush=True)


def string_checks(
    features: pd.DataFrame,
    X: pd.DataFrame,
    y: pd.Series,
    pairs: list,
    *,
    regression: bool,
    n_jobs: int,
    weight: np.ndarray | None = None,
) -> dict:
    """For each string column of more than ``WIDE_STRING`` values: test values seen in train, and the column as text."""
    tr, te = pairs[0]
    out: dict = {"string_value_in_train": {}}
    for col in features.select_dtypes(include=["string", "object"]).columns:
        values = features[col]
        distinct = int(values.nunique())
        if distinct <= WIDE_STRING:
            continue
        test_values = values.iloc[te].dropna()
        share = float(test_values.isin(set(values.iloc[tr].dropna())).mean()) if len(test_values) else float("nan")
        out["string_value_in_train"][col] = {"distinct": distinct, "share": share}
        say(f"string column {col} ({distinct:,} distinct values): {share:.1%} of the test values occur in train")
    wide = list(out["string_value_in_train"])
    if not wide:
        return out
    out["string_alone"] = {
        col: text_score(features, [col], None, y, pairs, regression=regression, n_jobs=n_jobs, weight=weight)
        for col in wide
    }
    say(f"string column alone, as text: { {c: round(v, 3) for c, v in out['string_alone'].items()} }")
    out["all_features_with_strings"] = text_score(
        features, wide, X, y, pairs, regression=regression, n_jobs=n_jobs, weight=weight
    )
    say(f"all features with the string columns as text: {out['all_features_with_strings']:.3f}")
    return out


def written_decimals(values: pd.Series) -> pd.Series:
    """The decimals each value is written with, at most 8 (2.50 counts 1, 3.0 counts 0); missing stays missing."""
    v = values.astype(float)
    out = pd.Series(np.nan, index=v.index)
    for d in range(8):
        scaled = v * 10.0**d
        whole = (scaled - scaled.round()).abs() <= 1e-9 + 1e-12 * scaled.abs()
        out[out.isna() & v.notna() & whole] = d
    out[out.isna() & v.notna()] = 8
    return out


def straight_line_fills(values: pd.Series) -> pd.Series:
    """Cells on a straight line between the cells above and below, in the order given: a cell whose step from the row
    above equals its step to the row below (and is not zero), in a run of two or more such cells, or alone when the
    step is finer than 0.01. Gaps filled by linear interpolation leave this trace; so do runs of round values by
    chance (92, 91, 90, 89), which only the values themselves can tell apart.
    """
    v = values.astype(float)
    step_in, step_out = v.diff(), -v.diff(-1)
    hit = ((step_in - step_out).abs() < 1e-6 * v.abs().clip(lower=1)) & (step_in.abs() > 1e-9)
    run_size = hit.groupby((hit != hit.shift()).cumsum()).transform("size")
    finer = (step_in * 100 - (step_in * 100).round()).abs() > 1e-6
    return hit & ((run_size >= 2) | finer)


def fill_counts(raw: pd.DataFrame, target: str, *, min_cells: int = 5) -> dict[str, dict[str, int]]:
    """Per numeric column of ``raw``, in its row order, the cells of ``straight_line_fills`` counted per target value;
    the columns with at least ``min_cells`` of them, most first.
    """
    out = {}
    for col in raw.columns:
        if col == target or not pd.api.types.is_numeric_dtype(raw[col]) or raw[col].nunique() <= 5:
            continue
        hit = straight_line_fills(raw[col])
        if hit.sum() >= min_cells:
            out[col] = {str(k): int(n) for k, n in hit.groupby(raw[target]).sum().items()}
    return dict(sorted(out.items(), key=lambda kv: -sum(kv[1].values())))


def row_order(y: pd.Series, problem_type: str) -> dict:
    """Probe 10, the target by row position in the source's order: ``y`` is the target of the rows in their raw order.

    A classification target gets the next-row label match against chance (the sum of the squared class shares, with
    a z score) and the largest gap between a class's share in a tenth of the rows and overall; a regression target
    the Spearman correlation with the position and the lag-1 autocorrelation. Rows sorted or blocked by the target
    show up here, and shuffled rows give chance. ``flag``: z of 5 or more, a gap of 0.1 or more, or a correlation of
    0.1 or more in size. A source in time order shows autocorrelation by nature: read it against the time column.
    """
    y = y.reset_index(drop=True)
    n = len(y)
    out: dict = {"rows": n}
    if problem_type == "regression":
        v = pd.to_numeric(y, errors="coerce")
        out["spearman_position"] = float(pd.Series(np.arange(n), dtype=float).corr(v, method="spearman"))
        out["lag1_autocorrelation"] = float(v.autocorr(lag=1)) if n > 2 else float("nan")
        sizes = [abs(out["spearman_position"]), abs(out["lag1_autocorrelation"])]
        out["flag"] = bool(np.nanmax(sizes) >= 0.1) if not np.all(np.isnan(sizes)) else False
        return out
    labels = y.astype(str).where(y.notna())
    shares = labels.value_counts(normalize=True)
    chance = float((shares**2).sum())
    values = labels.to_numpy()
    both = pd.notna(values[1:]) & pd.notna(values[:-1])
    match = float((values[1:][both] == values[:-1][both]).mean()) if both.any() else float("nan")
    se = float(np.sqrt(chance * (1 - chance) / max(int(both.sum()), 1)))
    tenth = np.minimum(np.arange(n) * 10 // max(n, 1), 9)
    by_tenth = pd.crosstab(tenth, labels, normalize="index")
    gap = float((by_tenth - shares.reindex(by_tenth.columns)).abs().to_numpy().max()) if len(by_tenth) else 0.0
    out.update(next_row_match=match, chance=chance, z=(match - chance) / se if se else float("nan"))
    out["largest_tenth_gap"] = gap
    out["flag"] = bool((se and out["z"] >= 5) or gap >= 0.1)
    return out


def removed_rows(raw_y: pd.Series | None, kept: np.ndarray, problem_type: str) -> dict:
    """Probe 19, the rows ``_clean`` removed: ``kept`` marks each raw row that reaches the curated frame (booleans in
    raw order); ``raw_y`` is the raw table's target column, or None when it has none of that name.

    Gives the counts and, with ``raw_y``, the target of the removed rows against the kept ones, unlabelled rows
    counted apart: the class shares (``flag`` at a gap of 0.1 or more), or the medians and the mean shift in
    standard deviations of all labelled rows (``flag`` at 0.5 or more). A filter that removes rows by their outcome (an
    extreme target, one class) selects on the label: CLEAN-11 and USE-7 say when that is right.
    """
    kept = np.asarray(kept, dtype=bool)
    out: dict = {"raw_rows": len(kept), "kept": int(kept.sum()), "removed": int((~kept).sum())}
    if raw_y is None or kept.all():
        return out
    raw_y = raw_y.reset_index(drop=True)
    labelled = raw_y.notna().to_numpy()
    out["removed_unlabelled"] = int((~kept & ~labelled).sum())
    gone, stay = ~kept & labelled, kept & labelled
    if not gone.any():
        out["flag"] = False
        return out
    if problem_type == "regression":
        v = pd.to_numeric(raw_y, errors="coerce")
        a, b = v[gone], v[stay]
        sd = float(v[labelled].std())
        out.update(removed_median=float(a.median()), kept_median=float(b.median()))
        out["mean_shift_sd"] = float((a.mean() - b.mean()) / sd) if sd else float("nan")
        out["flag"] = bool(abs(out["mean_shift_sd"]) >= 0.5) if sd else False
        return out
    labels = raw_y.astype(str)
    removed_shares = labels[gone].value_counts(normalize=True)
    kept_shares = labels[stay].value_counts(normalize=True)
    classes = removed_shares.index.union(kept_shares.index)
    gaps = (removed_shares.reindex(classes, fill_value=0) - kept_shares.reindex(classes, fill_value=0)).abs()
    out["removed_shares"] = {str(k): round(float(v), 4) for k, v in removed_shares.items()}
    out["kept_shares"] = {str(k): round(float(v), 4) for k, v in kept_shares.items()}
    out["largest_share_gap"] = float(gaps.max())
    out["flag"] = bool(gaps.max() >= 0.1)
    return out


def dropped_column_proxies(
    columns: pd.DataFrame,
    y: pd.Series,
    pairs: list,
    *,
    regression: bool,
    n_jobs: int = 8,
    max_columns: int = 50,
    weight: np.ndarray | None = None,
) -> dict:
    """Probe 20, the raw columns the definition drops, each alone against the shipped target (untuned LightGBM, scored
    as ``score``, with the training ``weight`` when the task has one) on ``pairs``: ``columns`` holds them aligned with
    ``y``, row by row of the curated frame.

    A dropped identifier, later measurement or outcome field that scores well alone says what the definition kept out;
    compare it with the kept features alone (``run``). Strings and booleans are scored as categories and a datetime as
    its time stamp; at most ``max_columns`` columns, in the raw table's order. Returns ``{column: score}``, best first
    (None when the fit fails), and ``skipped``, the columns over the limit.
    """
    scores: dict = {}
    for col in list(columns.columns)[:max_columns]:
        x = columns[col]
        if pd.api.types.is_datetime64_any_dtype(x):
            x = (x - x.min()).dt.total_seconds()
        elif not pd.api.types.is_numeric_dtype(x) or pd.api.types.is_bool_dtype(x):
            x = x.astype("string").astype("category")
        try:
            scores[col] = round(score(x.to_frame(), y, pairs, regression=regression, n_jobs=n_jobs, weight=weight), 4)
        except (ValueError, TypeError) as err:  # a column LightGBM cannot read is reported, not fatal
            scores[col] = None
            say(f"dropped column {col}: not scored ({type(err).__name__})")
    ranked = dict(sorted(scores.items(), key=lambda kv: -1.0 if kv[1] is None else -kv[1]))
    return {"scores": ranked, "skipped": max(0, columns.shape[1] - max_columns)}


def raw_copies(raw: pd.DataFrame, target: str | None) -> dict:
    """Probe 21, exact copies in the raw table, before ``_clean`` drops or deduplicates anything: the rows equal in
    every column but the target and the identifiers (a column whose values are all distinct, which would make every
    row unique), their groups, the groups holding more than one label, and the full-row copies.

    Set against probe 5 on the curated frame: copies the definition removed, or the source's own repeats it kept
    (LEAK-16 to LEAK-21).
    """
    has_target = target is not None and target in raw.columns
    inputs = raw.drop(columns=[target]) if has_target else raw
    ids = [c for c in inputs.columns if len(inputs) > 1 and inputs[c].nunique(dropna=False) == len(inputs)]
    inputs = inputs.drop(columns=ids)
    codes = profile_codes(inputs)
    sizes = pd.Series(codes).value_counts()
    repeated = sizes[sizes > 1]
    out: dict = {
        "raw_rows": len(raw),
        "rows_with_input_copy": int(repeated.sum()),
        "copy_groups": len(repeated),
        "identifiers_left_out": ids,
    }
    if has_target:
        labels = raw[target].reset_index(drop=True).astype(str).where(raw[target].reset_index(drop=True).notna())
        several = labels.groupby(codes).nunique(dropna=False)
        out["groups_with_several_labels"] = int((several.reindex(repeated.index) > 1).sum())
        out["full_row_copies"] = int(len(raw) - len(np.unique(profile_codes(raw))))
    return out


def _order_line(order: dict) -> str:
    flag = " - flag" if order["flag"] else ""
    if "next_row_match" in order:
        return (
            f"row order (probe 10), the target in the raw order: next-row label match {order['next_row_match']:.3f} "
            f"against chance {order['chance']:.3f} (z {order['z']:.1f}); largest class-share gap by tenth of the rows "
            f"{order['largest_tenth_gap']:.3f}{flag}"
        )
    return (
        f"row order (probe 10), the target in the raw order: Spearman with the position "
        f"{order['spearman_position']:.3f}, lag-1 autocorrelation {order['lag1_autocorrelation']:.3f}{flag}"
    )


def _removed_line(removed: dict) -> str:
    line = f"rows `_clean` removed (probe 19): {removed['removed']:,} of {removed['raw_rows']:,}"
    if "removed_unlabelled" in removed:
        line += f" ({removed['removed_unlabelled']:,} unlabelled)"
    if "largest_share_gap" in removed:
        line += (
            f"; class shares removed {removed['removed_shares']} against kept {removed['kept_shares']}, "
            f"largest gap {removed['largest_share_gap']:.3f}"
        )
    elif "mean_shift_sd" in removed:
        line += (
            f"; target median removed {removed['removed_median']:.4g} against kept {removed['kept_median']:.4g}, "
            f"mean shift {removed['mean_shift_sd']:+.2f} SD"
        )
    return line + (" - flag" if removed.get("flag") else "")


def _copies_line(copies: dict) -> str:
    line = (
        f"raw copies (probe 21): {copies['rows_with_input_copy']:,} of {copies['raw_rows']:,} rows share their "
        f"inputs with another row, in {copies['copy_groups']:,} groups"
    )
    if copies.get("identifiers_left_out"):
        line += f" (identifiers left out: {copies['identifiers_left_out'][:5]})"
    if "groups_with_several_labels" in copies:
        line += (
            f", {copies['groups_with_several_labels']:,} of them with more than one label; "
            f"{copies['full_row_copies']:,} full-row copies"
        )
    return line


def raw_lines(result: dict) -> list[str]:
    """The report lines of the raw-state probes (``leak_probes.py --raw``), from their results by name."""
    lines = []
    if result.get("row_order"):
        lines.append(_order_line(result["row_order"]))
    if result.get("removed_rows"):
        lines.append(_removed_line(result["removed_rows"]))
    dropped = result.get("dropped_columns")
    if dropped:
        top = dict(list(dropped["scores"].items())[:8])
        more = f"; {dropped['skipped']} more not scored" if dropped["skipped"] else ""
        lines.append(f"each dropped raw column alone (probe 20): {top}{more}")
    if result.get("raw_copies"):
        lines.append(_copies_line(result["raw_copies"]))
    return lines


def profile_codes(frame: pd.DataFrame) -> np.ndarray:
    """One integer per row, the same for rows whose cells are all equal: nothing is rounded, -0.0 equals 0.0, and a
    missing value of any kind (NaN, None, pd.NA, NaT) equals another missing value of its column.
    """
    code = np.zeros(len(frame), dtype=np.int64)
    for col in frame.columns:
        values = frame[col]
        if isinstance(values.dtype, pd.CategoricalDtype):
            cells = values.cat.codes.to_numpy(dtype=np.int64)
        else:
            cells = pd.factorize(values)[0].astype(np.int64)
        code = pd.factorize(code * (cells.max() + 2) + cells + 1)[0].astype(np.int64)
    return code


def copy_counts(profiles: np.ndarray, y: pd.Series, splits: list) -> dict:
    """Probe 5 on every split: each test row's training rows with the same profile (``profile_codes``), by label.

    Returns the shares of the test rows of all splits pooled (a row in several repeats counts each time) that have a
    copy in train (``matched``), and the partition of the matched ones: copies of the same label only and of a
    different label only, each with one copy or two or more, and copies of both labels; plus the matched share of each
    split. For a regression target "the same label" is the same value.
    """
    labels = pd.factorize(pd.Series(y).to_numpy())[0].astype(np.int64)
    pair = pd.factorize(profiles * (labels.max() + 2) + labels + 1)[0]
    joint = np.zeros((3, 3), dtype=np.int64)  # [same-label copies 0/1/2+, different-label copies 0/1/2+]
    per_split = []
    for train_idx, test_idx in splits:
        tr, te = np.asarray(train_idx, dtype=np.int64), np.asarray(test_idx, dtype=np.int64)
        same = np.bincount(pair[tr], minlength=pair.max() + 1)[pair[te]]
        total = np.bincount(profiles[tr], minlength=profiles.max() + 1)[profiles[te]]
        np.add.at(joint, (np.minimum(same, 2), np.minimum(total - same, 2)), 1)
        per_split.append(float((total > 0).mean()) if len(te) else float("nan"))
    rows = int(joint.sum())
    share = lambda count: float(count / rows) if rows else float("nan")
    return {
        "test_rows": rows,
        "splits": len(per_split),
        "matched": share(rows - joint[0, 0]),
        "same_label_only": {"one": share(joint[1, 0]), "two_or_more": share(joint[2, 0])},
        "different_label_only": {"one": share(joint[0, 1]), "two_or_more": share(joint[0, 2])},
        "both_labels": share(joint[1:, 1:].sum()),
        "matched_per_split": per_split,
    }


def copy_line(what: str, counts: dict) -> str:
    """``copy_counts`` as one line of the report."""
    same, other = counts["same_label_only"], counts["different_label_only"]
    spread = [s for s in counts["matched_per_split"] if not np.isnan(s)]
    per_split = f"; per split {min(spread):.1%} to {max(spread):.1%}" if len(spread) > 1 else ""
    return (
        f"{what} ({counts['splits']} splits, {counts['test_rows']:,} test rows): {counts['matched']:.1%} have one; "
        f"same label only {same['one'] + same['two_or_more']:.1%} (two or more copies {same['two_or_more']:.1%}), "
        f"another label only {other['one'] + other['two_or_more']:.1%} (two or more {other['two_or_more']:.1%}), "
        f"both labels {counts['both_labels']:.1%}{per_split}"
    )


# Probe 13: the target by period

PERIOD_FREQS = ("D", "W", "M", "Q", "Y")
"""The calendar periods ``target_by_period`` picks from, finest first."""
YEARS = (1000, 3000)
"""Integer times in this range are read as years."""
PERIOD_NAMES = {
    "D": "daily",
    "W": "weekly",
    "M": "monthly",
    "Q": "quarterly",
    "Y": "yearly",
    "year": "yearly",
    "binned": "equal-count",
}
RANK_BINS = 40
"""Equal-count periods for an integer time column with about one row per value (a rank), at most."""
YEAR_LAG = {"D": 365, "W": 52, "M": 12, "Q": 4}
"""Periods back to the same period a year earlier."""


def period_times(times, *, tz: str | None = None) -> tuple[pd.Series, str]:
    """The time column as naive wall-clock timestamps (kind ``datetime``), years (``year``; also dates that all fall
    on 1 January, a year stored as a date) or other integer periods (``integer``, such as a month index). Aware
    timestamps are converted to ``tz`` first (None keeps their own offset); naive ones are read as already in ``tz``.
    Numbers, numeric categories and numeric strings are never read as nanoseconds since 1970. Raises ``ValueError``
    for booleans, fractional numbers and strings that are no dates.
    """
    s = pd.Series(times).reset_index(drop=True)
    if isinstance(s.dtype, pd.CategoricalDtype):
        s = s.astype(s.cat.categories.dtype)
    if pd.api.types.is_bool_dtype(s):
        raise ValueError("the time column is boolean, not a time")
    if s.dtype == object:
        numbers = pd.to_numeric(s, errors="coerce")
        if numbers.notna().sum() == s.notna().sum() and not s.dropna().map(lambda v: isinstance(v, bool)).any():
            s = numbers
    if pd.api.types.is_numeric_dtype(s):
        known = s.dropna().astype(float)
        if (known != known.round()).any():
            raise ValueError("the time column holds fractional numbers: give dates, years or integer periods")
        kind = "year" if len(known) and YEARS[0] <= known.min() and known.max() <= YEARS[1] else "integer"
        return s.astype("Int64"), kind
    s = _naive_dates(s, tz)
    if _years_as_dates(s):
        return s.dt.year.astype("Int64"), "year"
    return s, "datetime"


def _naive_dates(s: pd.Series, tz: str | None) -> pd.Series:
    """``s`` parsed as dates and made naive in ``tz`` (see ``period_times``)."""
    if not pd.api.types.is_datetime64_any_dtype(s):
        try:
            s = pd.to_datetime(s.astype(object), errors="raise", format="mixed")
        except (ValueError, TypeError) as err:
            raise ValueError(f"the time column is neither dates, years nor integer periods: {err}") from err
    if s.dt.tz is not None:
        s = (s.dt.tz_convert(tz) if tz else s).dt.tz_localize(None)
    return s


def _years_as_dates(s: pd.Series) -> bool:
    """Whether every date is midnight on 1 January: a year stored as a date (a fiscal year)."""
    known = s.dropna()
    return bool(len(known)) and bool(
        ((known.dt.month == 1) & (known.dt.day == 1) & (known == known.dt.normalize())).all()
    )


def choose_period(stamps: pd.Series, *, min_rows: int = 100, max_periods: int = 60) -> str:
    """The finest calendar period (``PERIOD_FREQS``) with 5 to ``max_periods`` periods and a median of at least
    ``min_rows`` rows per period that has rows; when none has that many rows, the coarsest with at least 5 periods.
    """
    fallback = None
    for freq in PERIOD_FREQS:
        per = stamps.dt.to_period(freq)
        span = (per.max() - per.min()).n + 1
        if span < 5:
            break
        fallback = freq
        if span <= max_periods and per.value_counts().median() >= min_rows:
            return freq
    if fallback is None:
        raise ValueError("the times span fewer than 5 days: probe 13 needs at least 5 periods")
    return fallback


def _period_positions(t: pd.Series, kind: str, freq: str | None, *, min_rows: int, max_periods: int):
    """Each row's period position, the period labels, the size of each period that the data covers (days for
    calendar periods, 1 otherwise), the share of each period covered, the period, and whether rows are counted per
    day (calendar periods of dates with day resolution) or per period.

    An integer column with about one row per value that is no year (a rank such as an arrival order, or a running
    id) is cut into equal-count periods by its order, at most ``RANK_BINS``, period ``binned``. Dates that label
    their period (one distinct date in every period, such as month starts) are counted per period, not per day.
    """
    if kind != "datetime":
        values = t.astype("int64").to_numpy()
        if kind == "integer" and len(values) >= 10 and len(np.unique(values)) >= 0.5 * len(values):
            bins = int(np.clip(len(values) // max(min_rows, 1), 5, min(RANK_BINS, max_periods)))
            order = np.argsort(values, kind="stable")
            pos = np.empty(len(values), dtype=np.int64)
            pos[order] = np.arange(len(values)) * bins // len(values)
            edges = [(values[order][pos[order] == b].min(), values[order][pos[order] == b].max()) for b in range(bins)]
            ones = np.ones(bins)
            return pos, [f"{lo}-{hi}" for lo, hi in edges], ones, ones, "binned", False
        steps = np.arange(values.min(), values.max() + 1) if kind == "year" else np.unique(values)
        ones = np.ones(len(steps))
        return np.searchsorted(steps, values), [str(v) for v in steps], ones, ones, kind, False
    if freq is not None and freq not in PERIOD_FREQS:
        raise ValueError(f"period {freq!r}: use one of {PERIOD_FREQS}")
    freq = freq or choose_period(t, min_rows=min_rows, max_periods=max_periods)
    per = t.dt.to_period(freq)
    index = pd.period_range(per.min(), per.max(), freq=freq)
    positions = index.get_indexer(pd.PeriodIndex(per))
    if pd.Series(t.to_numpy()).groupby(positions).nunique().max() <= 1:  # each period holds one date: its label
        ones = np.ones(len(index))
        return positions, [str(p) for p in index], ones, ones, freq, False
    day = pd.Timedelta(days=1)
    starts, ends = index.start_time, index.end_time + pd.Timedelta(1, "ns")
    length = np.asarray((ends - starts) / day, dtype=float)
    days = length.copy()
    first, last = t.min().normalize(), t.max().normalize() + day
    for i in {0, len(index) - 1}:
        days[i] = (min(ends[i], last) - max(starts[i], first)) / day
    return positions, [str(p) for p in index], days, days / length, freq, True


def _plain(value):
    """A JSON value: numpy scalars as Python ones, NaN as None."""
    value = value.item() if hasattr(value, "item") else value
    return None if isinstance(value, float) and np.isnan(value) else value


def _prefix(per_period: np.ndarray) -> np.ndarray:
    """Cumulative sums with a leading 0: the sum over periods ``a`` to ``b - 1`` is ``out[b] - out[a]``."""
    return np.concatenate([[0.0], np.cumsum(per_period)])


class _Periods:
    """The rows put in periods: positions, labels, rows and covered size, and the earlier periods that give the band."""

    def __init__(self, pos: np.ndarray, labels: list[str], size: np.ndarray, tail: int) -> None:
        self.pos, self.labels, self.tail = pos, labels, tail
        self.count = len(labels)
        self.base = self.count - tail
        self.in_base = pos < self.base
        self.rows = np.bincount(pos, minlength=self.count).astype(float)
        self.rows_c, self.size_c = _prefix(self.rows), _prefix(size)

    def total(self, a: int, b: int) -> float:
        """Rows in periods ``a`` to ``b - 1``."""
        return self.rows_c[b] - self.rows_c[a]

    def sums(self, weights: np.ndarray) -> np.ndarray:
        """``_prefix`` of the per-period sums of ``weights``."""
        return _prefix(np.bincount(self.pos, weights=weights.astype(float), minlength=self.count))


def _statistic(value, *, noise=None, show=None, log: bool = False) -> dict:
    """A statistic of a run of periods ``(a, b)``: its value (the tested one), the sampling variance of that value
    under no change (or None), the value shown (when another than the tested one) and whether it is tested on a log
    scale.
    """
    return {"value": value, "noise": noise, "show": show or value, "log": log}


def _rate(periods: _Periods, hits: np.ndarray) -> dict:
    """The share of rows with ``hits`` in a run of periods, with binomial noise at the earlier periods' share."""
    hit_c = periods.sums(hits)
    p0 = float(hits[periods.in_base].mean()) if periods.in_base.any() else float("nan")

    def value(a, b):
        return (hit_c[b] - hit_c[a]) / periods.total(a, b) if periods.total(a, b) else float("nan")

    return _statistic(value, noise=lambda a, b: p0 * (1 - p0) / periods.total(a, b))


def _rows_name(*, per_day: bool) -> str:
    """The name of the row-count statistic: per day for calendar periods of dates (months differ in length), else
    per period.
    """
    return "rows per day" if per_day else "rows per period"


def _period_statistics(
    periods: _Periods, y: pd.Series, problem_type: str, positive, rows_name: str
) -> tuple[dict, dict]:
    """The statistics probe 13 tests (see ``target_by_period``) and what the result says about the classes."""
    p = periods

    def rows_per_unit(a, b):
        return p.total(a, b) / (p.size_c[b] - p.size_c[a]) if p.total(a, b) else float("nan")

    stats = {rows_name: _statistic(rows_per_unit, noise=lambda a, b: 1.0 / p.total(a, b), log=True)}
    if problem_type == "regression":
        v = pd.to_numeric(y, errors="raise").to_numpy(dtype=float)
        sum_c, var0 = p.sums(v), float(np.var(v[p.in_base]))
        stats["mean"] = _statistic(
            lambda a, b: (sum_c[b] - sum_c[a]) / p.total(a, b) if p.total(a, b) else float("nan"),
            noise=lambda a, b: var0 / p.total(a, b),
        )
        if bool((v >= 0).all() and (v == np.round(v)).all()):  # a count
            stats["zero share"] = _rate(p, v == 0)
            return stats, {}
        groups = np.split(v[np.argsort(p.pos, kind="stable")], np.cumsum(p.rows.astype(int))[:-1])
        for q, name in ((0.5, "p50"), (0.9, "p90")):
            # tested as the share above the earlier periods' quantile, which discrete values do not break
            stat = _rate(p, v > float(np.quantile(v[p.in_base], q)))

            def show(a, b, q=q):
                return float(np.quantile(np.concatenate(groups[a:b]), q)) if p.total(a, b) else float("nan")

            stats[name] = {**stat, "show": show}
        return stats, {}
    counts = y.value_counts()
    counts = counts[counts > 0]
    values = y.to_numpy()
    if problem_type != "binary_classification" and len(counts) > 2:
        top = list(counts.index[:10])
        stats.update({f"share of {c}": _rate(p, values == c) for c in top})
        return stats, {"classes": [_plain(c) for c in top]}
    if positive is None:
        if len(counts) < 2:
            raise ValueError("the target holds one class only; name the event class with `positive`")
        positive = counts.index[-1]  # the minority class
    else:
        match = [c for c in counts.index if c == positive or str(c) == str(positive)]
        if not match:
            values_seen = [_plain(c) for c in counts.index]
            raise ValueError(
                f"the positive label {positive!r} does not occur in the target (its values: {values_seen})"
            )
        positive = match[0]
    stats[f"rate of {positive}"] = _rate(p, values == positive)
    return stats, {"positive": _plain(positive)}


def _band(p: _Periods, stat: dict, k: int) -> tuple[float, float, float] | None:
    """The median, the spread (1.4826 x MAD) and the median sampling noise of ``stat`` over every run of ``k``
    consecutive earlier periods (on the statistic's scale); None with fewer than 3 runs.
    """
    vals, noises = [], []
    for a in range(p.base - k + 1):
        value = stat["value"](a, a + k)
        if np.isfinite(value) and (value > 0 or not stat["log"]):
            vals.append(np.log(value) if stat["log"] else value)
            noises.append(stat["noise"](a, a + k) if stat["noise"] else 0.0)
    if len(vals) < 3:
        return None
    vals = np.asarray(vals)
    mid = float(np.median(vals))
    return mid, 1.4826 * float(np.median(np.abs(vals - mid))), float(np.median(noises))


def _z(stat: dict, a: int, b: int, band: tuple | None) -> float | None:
    """How far the run of periods ``(a, b)`` lies from ``band``, in its spread widened by the run's extra noise."""
    value = stat["value"](a, b)
    if band is None or not np.isfinite(value) or (stat["log"] and value <= 0):
        return None
    mid, spread, base_noise = band
    noise = stat["noise"](a, b) if stat["noise"] else 0.0
    var = max(spread**2 + max(noise - base_noise, 0.0), base_noise, 1e-12 * max(abs(mid), 1.0) ** 2)
    return float(((np.log(value) if stat["log"] else value) - mid) / np.sqrt(var))


def _newest(p: _Periods, stat: dict, freq: str, threshold: float) -> dict:
    """``stat`` on each newest period and on the newest 1 to ``tail`` pooled, and the run out of band at the end."""
    bands = {k: _band(p, stat, k) for k in range(1, p.tail + 1)}
    lag = YEAR_LAG.get(freq)
    newest = []
    for i in range(p.base, p.count):
        entry = {"period": p.labels[i], "value": _plain(stat["show"](i, i + 1)), "z": _z(stat, i, i + 1, bands[1])}
        if lag and i - lag >= 0:
            entry["year_earlier"] = _plain(stat["show"](i - lag, i - lag + 1))
        newest.append(entry)
    windows = [
        {
            "periods": k,
            "value": _plain(stat["show"](p.count - k, p.count)),
            "z": _z(stat, p.count - k, p.count, bands[k]),
        }
        for k in range(1, p.tail + 1)
    ]
    last = newest[-1]["z"]
    run_length = 0
    if last is not None and abs(last) >= threshold:
        for entry in reversed(newest):
            if entry["z"] is None or abs(entry["z"]) < threshold or np.sign(entry["z"]) != np.sign(last):
                break
            run_length += 1
    return {
        "newest_periods": newest,
        "newest_windows": windows,
        "trailing_out_of_band": run_length,
        "direction": ("falls" if last < 0 else "rises") if run_length else None,
    }


def _period_reading(out: dict, labels: list[str], period_name: str, threshold: float) -> str:
    """What the curator acts on, in two sentences."""
    flags = [s for s, o in out.items() if o["trailing_out_of_band"]]
    if flags:
        first_out = len(labels) - max(out[s]["trailing_out_of_band"] for s in flags)
        moves = ", ".join(f"{s} {out[s]['direction']}" for s in flags)
        return (
            f"The newest {period_name} periods from {labels[first_out]} on are outside the band of the earlier ones "
            f"({moves}). A fall of an event rate, an upper quantile or the row count at the end only is the mark of "
            "right-censoring: cut before that period (or set a gap of that length), or compare a second download "
            "(LEAK-24); a rise, or a shift the history also shows, is drift."
        )
    pooled = [
        (s, w) for s, o in out.items() for w in o["newest_windows"] if w["z"] is not None and abs(w["z"]) >= threshold
    ]
    if pooled:
        s, w = pooled[0]
        return (
            f"No single newest period is outside the band, but the newest {w['periods']} pooled are ({s}, z "
            f"{w['z']:+.1f}): a mild shift at the end; compare a second download or a finer period."
        )
    return (
        f"No newest period is outside the band of the earlier ones (|z| < {threshold:g}) for any statistic: no sign of "
        "censoring at the release end. It does not show which labels a model refit at a window's start would have "
        "known (SPLIT-10)."
    )


def target_by_period(  # noqa: PLR0913
    times,
    y,
    problem_type: str,
    *,
    freq: str | None = None,
    tz: str | None = None,
    positive=None,
    tail: int | None = None,
    threshold: float = 3.0,
    min_rows: int = 100,
    max_periods: int = 60,
    report: bool = True,
) -> dict:
    """Probe 13: does the target by period show the newest periods losing their late cases?

    A label that is known only some time after the prediction point (a default on the first instalment, a claim
    reported late, a duration still running at the download) is right-censored at the release end: in the newest
    periods the slow or late cases are missing, so an event rate, the upper quantiles of a duration or the row count
    falls there and nowhere else. Credit risk reads this from vintage (cohort) curves of default rates by origination
    month, insurance from the development of claims by accident period (incurred but not reported, IBNR), survival
    analysis as administrative censoring at the end of follow-up. With one release, the probe looks at the end of the
    series: every statistic of the newest periods against the band the earlier periods give.

    The times are put in periods: calendar periods (``freq`` one of ``PERIOD_FREQS``; by default the finest with 5 to
    ``max_periods`` periods and ``min_rows`` rows per period), years (dates that all fall on 1 January are years), or
    other integer periods; an integer column with about one row per value (a rank) is cut into at most ``RANK_BINS``
    equal-count periods by its order, and the output says so. The newest ``tail``
    periods (default a fifth of them, 2 to 8) are tested; the band comes from the earlier ones: for a run of ``k``
    periods, the median and the spread (1.4826 x MAD) of every run of ``k`` consecutive earlier periods, widened by
    the extra sampling noise of a smaller run. So a drop is read against the normal variation of the history, not
    against one chosen period. Statistics: the rows per day the data covers (per period for years and integer
    periods; on a log scale); for a binary target the rate of ``positive`` (default the minority class); for a
    multiclass target the share of each of the ten largest classes; for a regression the mean, and the shares above
    the earlier periods' median and 90th percentile (shown as the run's p50 and p90); for a count target the mean and
    the zero share. A statistic whose newest periods are out of band (``|z| >= threshold``), in a run from the end,
    is flagged with its direction, and the reading says what the curator acts on (LEAK-24: cut where follow-up is
    complete, or compare a second download). The same period a year earlier is shown for seasonal data. A clean
    result says nothing about which labels a model refit at a window's start would have known (SPLIT-10).

    Args:
        times: The time of each row: datetimes, date strings, years or integer periods.
        y: The target.
        problem_type: ``"regression"``, or a classification type.
        freq: The calendar period, or None to choose one (not used for years and integer periods).
        tz: The timezone whose calendar makes the periods; aware times are converted to it.
        positive: The event class of a binary target (matched by value or by its string).
        tail: The newest periods tested; the others give the band (at least 4 of them).
        threshold: The ``|z|`` from which a newest period is out of band.
        min_rows: Rows per period the automatic period choice asks for.
        max_periods: The most periods the automatic choice makes.
        report: Print the summary lines.
    """
    t, kind = period_times(times, tz=tz)
    y = pd.Series(y).reset_index(drop=True)
    if len(t) != len(y):
        raise ValueError(f"{len(t)} times for {len(y)} targets")
    missing_time, missing_target = int(t.isna().sum()), int((y.isna() & t.notna()).sum())
    keep = (t.notna() & y.notna()).to_numpy()
    t, y = t[keep].reset_index(drop=True), y[keep].reset_index(drop=True)
    if not len(t):
        raise ValueError("no row has both a time and a target")
    pos, labels, size, coverage, freq, per_day = _period_positions(
        t, kind, freq, min_rows=min_rows, max_periods=max_periods
    )
    if len(labels) < 5:
        raise ValueError(f"{len(labels)} periods: probe 13 needs at least 5 (4 for the band, 1 to test)")
    tail = min(int(np.clip(len(labels) // 5, 2, 8)) if tail is None else int(tail), len(labels) - 4)
    if tail < 1:
        raise ValueError(f"tail {tail}: test at least 1 period and keep 4 for the band")
    periods = _Periods(pos, labels, size, tail)
    rows_name = _rows_name(per_day=per_day)
    stats, extra = _period_statistics(periods, y, problem_type, positive, rows_name)
    if freq == "binned":  # equal-count periods: their row count says nothing
        stats.pop(rows_name)
    out = {name: _newest(periods, stat, freq, threshold) for name, stat in stats.items()}
    table = []
    for i in range(periods.count):
        row = {"period": labels[i], "rows": int(periods.rows[i])}
        if coverage[i] < 1:
            row["coverage"] = round(float(coverage[i]), 3)
        row.update({s: _plain(stat["show"](i, i + 1)) for s, stat in stats.items() if s != rows_name})
        table.append(row)
    result = {
        "time_kind": kind,
        "period": freq,
        "tz": tz,
        "rows": len(t),
        "missing_time": missing_time,
        "missing_target": missing_target,
        "periods": periods.count,
        "first": labels[0],
        "last": labels[-1],
        "coverage_first": round(float(coverage[0]), 3),
        "coverage_last": round(float(coverage[-1]), 3),
        "tail": tail,
        "threshold": threshold,
        "note": (
            f"an integer time column with about one row per value (a rank or an id): cut into {len(labels)} "
            "equal-count periods by its order"
            if freq == "binned"
            else ""
        ),
        **extra,
        "table": table,
        "statistics": out,
        "flags": [s for s, o in out.items() if o["trailing_out_of_band"]],
        "reading": _period_reading(out, labels, PERIOD_NAMES.get(freq, freq), threshold),
    }
    if report:
        for line in period_lines(result):
            say(line)
    return result


def _cell(entry: dict) -> str:
    """One newest period or run: its value and its z."""
    if entry["value"] is None:
        return "-"
    z = "z n/a" if entry["z"] is None else f"z {entry['z']:+.1f}"
    return f"{entry['value']:.4g} ({z})"


def period_lines(result: dict) -> list[str]:
    """``target_by_period``'s result as the lines of the report."""
    left_out = result["missing_time"] + result["missing_target"]
    head = (
        f"target by period (probe 13): {result['periods']} {PERIOD_NAMES.get(result['period'], result['period'])} "
        f"periods {result['first']} to {result['last']}; the newest {result['tail']} against the band of the "
        f"{result['periods'] - result['tail']} before (|z| >= {result['threshold']:g})"
    )
    if result["coverage_last"] < 1:
        head += f"; the last period {result['coverage_last']:.0%} covered"
    if left_out:
        head += f"; {left_out:,} rows without a time or a target left out"
    if result.get("note"):
        head += f"; {result['note']}"
    lines = [head]
    for name, stat in result["statistics"].items():
        cells = ", ".join(_cell(e) for e in stat["newest_periods"])
        pooled = ", ".join("n/a" if w["z"] is None else f"{w['z']:+.1f}" for w in stat["newest_windows"])
        run_out = stat["trailing_out_of_band"]
        flag = f"; the newest {run_out} out of band, {stat['direction']}" if run_out else ""
        lines.append(
            f"  {name}: newest periods {cells}; newest 1 to {len(stat['newest_windows'])} pooled, z {pooled}{flag}"
        )
    lines.append(f"  reading: {result['reading']}")
    return lines


# Probe 22: the weight proxy

PROXY_SD = 2.0
"""A feature is flagged when its weight-mediated gain is above this many SDs (over splits x seeds) ..."""
PROXY_SHARE = 0.1
"""... and above this share of the leak reference (what the weight itself gains as a feature)."""
PROXY_TIMING = (
    "The decision is a timing call (LEAK-41): a feature known at the prediction point stays, even when it predicts "
    "the weight through risk selection (USE-6); a column set or cut after it (an earned premium, a realized length) is "
    "no model input, or ships in a form known at the start (annualised to the planned term)."
)


def _proxy_model(
    *, regression: bool, seed: int, n_estimators: int, n_jobs: int, params: dict | None = None
) -> lgb.LGBMModel:
    """Untuned LightGBM that bags rows, so that the seeds differ; ``params`` are passed on. Every tree sees every
    column: with column sampling, dropping one column would change which columns the other trees see.
    """
    return (lgb.LGBMRegressor if regression else lgb.LGBMClassifier)(
        n_estimators=n_estimators,
        learning_rate=0.05,
        subsample=0.8,
        subsample_freq=1,
        random_state=seed,
        verbose=-1,
        n_jobs=n_jobs,
        **(params or {}),
    )


def _spread(values) -> dict:
    """The mean and the SD (ddof 1) of the finite values, and how many there are; NaN where there are too few."""
    v = np.asarray(list(values), dtype=float)
    v = v[np.isfinite(v)]
    return {
        "mean": float(v.mean()) if len(v) else float("nan"),
        "sd": float(v.std(ddof=1)) if len(v) > 1 else float("nan"),
        "runs": len(v),
    }


def _inverse_weight(w: np.ndarray, n_classes: int) -> np.ndarray | None:
    """1/weight as a prediction: the values, or for a binary task the probabilities of the second class (1/weight
    scaled into (0, 1]; ``weight_proxy`` also tries the first); None for a multiclass task. A weight of 0 gets twice
    the largest finite inverse.
    """
    inv = 1.0 / np.where(w > 0, w, np.nan)
    finite = np.isfinite(inv)
    inv = np.where(finite, inv, 2 * inv[finite].max() if finite.any() else 1.0)
    if not n_classes:
        return inv
    if n_classes != 2:
        return None
    p = inv / inv.max()
    return np.column_stack([1 - p, p])


def weight_proxy(  # noqa: C901, PLR0912, PLR0913
    df: pd.DataFrame,
    target: str,
    problem_type: str,
    splits: list,
    weight,
    *,
    sample_weight=None,
    feature_cols: list[str] | tuple[str, ...] | None = None,
    group_cols: list[str] | tuple[str, ...] = (),
    metric: dict | None = None,
    weight_name: str = "weight",
    name: str = "dataset",
    n_splits: int = 3,
    max_rows: int = 50_000,
    seeds: tuple[int, ...] = (0, 1, 2),
    top: int = 5,
    n_estimators: int = 200,
    fit_params: dict | None = None,
    n_jobs: int = 8,
    report: bool = True,
) -> dict:
    """Probe 22: do the features carry a realized weight, and how much of their gain goes through it?

    A weight the outcome can cut short (the time insured of a policy cancelled after a claim) is never a feature
    (LEAK-41); this probe asks whether a feature stands in for it. On the first ``n_splits`` splits, each side capped
    at ``max_rows`` random rows (seed 0), and once per seed of ``seeds`` (LightGBM bags rows, so the seeds differ):

    a. a LightGBM regression of the weight on the features, fitted on each train side and scored on its test side:
       R^2, the Spearman correlation and the ``top`` features by gain;
    b. the leak reference: the task's ``metric`` (else R^2 or ROC AUC, weighted) for an honest LightGBM fit on the
       features, trained on the target as it ships with the training weight as each row's weight (an L2 fit, or the
       objective ``fit_params`` sets, such as the weighted Poisson fit of a claims rate), against the same fit with
       the weight added as a feature: what a perfect proxy of the weight gains;
    c. for each of those top features F: its gain (the score with F against the score without it, positive when F
       helps, whatever the metric's direction), once without the weight among the features and once with it. The
       weight-mediated part is the first gain less the second, with its mean and SD over splits x seeds: a feature
       that stands in for the weight loses its gain once the weight is there;
    d. for a Gini metric (``metric["gini"]``): the score of 1/weight alone as the prediction, the ceiling a proxy
       could reach (for a binary task, as the probability of the class it scores better for).

    A feature is flagged when its weight-mediated part is above ``PROXY_SD`` SDs and above ``PROXY_SHARE`` of the leak
    reference. A flag is no verdict: whether the feature stays is a timing call (``PROXY_TIMING``).

    Args:
        df: The rows, with the target and the group columns.
        target: The target column.
        problem_type: ``"regression"``, or a classification type.
        splits: ``(train_idx, test_idx)`` row positions; the first ``n_splits`` are probed.
        weight: The weight under study, one value per row of ``df``: the task's sample weight, or a candidate column
            (never one of the features; a column of ``df`` named ``weight_name`` is left out of them).
        sample_weight: The task's training weight, which every fit is trained with; None trains with ``weight``.
        feature_cols: The model inputs (default: every column but the target and the groups).
        group_cols: Columns that are not features (a group id).
        metric: The task's own metric (see ``curation_probes.weights``), or None for R^2 or ROC AUC.
        weight_name: The weight's name in the report.
        name: The dataset's name in the result.
        n_splits: Splits to probe.
        max_rows: Rows kept (at random) of each train and test side.
        seeds: The LightGBM seeds; each split is fitted once per seed.
        top: The features of the weight model checked in c.
        n_estimators: Trees per LightGBM fit.
        fit_params: LightGBM parameters of the fits of the target (b, c), such as ``{"objective": "poisson"}``; None
            for LightGBM's default (L2, or log loss). LEAK-41 asks for the L2 fit and the weighted actuarial fit.
        n_jobs: Threads per LightGBM model.
        report: Print the lines of ``weight_proxy_lines``.
    """
    regression = problem_type == "regression"
    w = np.asarray(weight, dtype=float)
    if len(w) != len(df) or not np.isfinite(w).all() or (w < 0).any():
        raise ValueError(f"`{weight_name}` needs a finite weight >= 0 on each of the {len(df):,} rows")
    train_w = w if sample_weight is None else np.asarray(sample_weight, dtype=float)
    columns = list(feature_cols) if feature_cols is not None else [c for c in df.columns if c != target]
    columns = [c for c in columns if c not in {weight_name, target, *group_cols}]
    X = df[columns].select_dtypes(exclude=["string", "object", "datetime", "datetimetz"])
    names = list(X.columns)
    X = X.set_axis([f"f{i}" for i in range(X.shape[1])], axis=1)  # LightGBM refuses some characters in names
    y = df[target]
    truth = y.to_numpy(dtype=float) if regression else y.to_numpy()
    classes = np.unique(truth) if not regression else None
    n_classes = 0 if regression else len(classes)
    sign = 1.0 if metric is None or metric["greater_is_better"] else -1.0
    errors: list[str] = []

    def evaluate(pred: np.ndarray, rows: np.ndarray) -> float:
        if metric is not None:
            value, error = weights.declared_score(metric, truth[rows], pred, rows, () if regression else classes)
            if error and error not in errors:
                errors.append(error)
            return value
        if regression:
            return float(r2_score(truth[rows], pred, sample_weight=train_w[rows]))
        return auc(truth[rows], pred, classes, train_w[rows])

    def fit_predict(x_tr: pd.DataFrame, x_te: pd.DataFrame, tr: np.ndarray, seed: int) -> np.ndarray:
        if not x_tr.shape[1]:  # no feature left: the weighted dummy
            if regression:
                return np.full(len(x_te), np.average(truth[tr], weights=train_w[tr]))
            shares = np.array([train_w[tr][truth[tr] == c].sum() for c in classes]) / train_w[tr].sum()
            return np.tile(shares, (len(x_te), 1))
        model = _proxy_model(
            regression=regression, seed=seed, n_estimators=n_estimators, n_jobs=n_jobs, params=fit_params
        )
        weights.fit(model, x_tr, truth[tr] if regression else y.iloc[tr], train_w[tr])
        if regression:
            return np.clip(model.predict(x_te), truth[tr].min(), truth[tr].max())
        return class_proba(model, x_te, classes)

    rng = np.random.default_rng(0)
    cap = lambda idx: np.sort(rng.choice(idx, min(len(idx), max_rows), replace=False))
    chosen = [(np.asarray(tr), np.asarray(te)) for tr, te in list(splits)[:n_splits]]
    sampled = any(len(tr) > max_rows or len(te) > max_rows for tr, te in chosen)
    pairs = [(cap(tr), cap(te)) for tr, te in chosen]
    seeds = tuple(seeds)

    # a. and b.: the weight from the features, and the honest fit against the one with the weight as a feature
    r2s, rhos, gains, ceiling = [], [], [], []
    honest, with_weight = {}, {}
    for i, (tr, te) in enumerate(pairs):
        x_tr, x_te = X.iloc[tr], X.iloc[te]
        for seed in seeds:
            if X.shape[1]:
                proxy = _proxy_model(regression=True, seed=seed, n_estimators=n_estimators, n_jobs=n_jobs)
                guess = proxy.fit(x_tr, w[tr]).predict(x_te)
                r2s.append(r2_score(w[te], guess))
                rhos.append(pd.Series(w[te]).corr(pd.Series(guess), method="spearman") if np.ptp(guess) else np.nan)
                gain = proxy.booster_.feature_importance(importance_type="gain")
                gains.append(gain / gain.sum() if gain.sum() > 0 else gain)
            honest[i, seed] = evaluate(fit_predict(x_tr, x_te, tr, seed), te)
            plus = fit_predict(x_tr.assign(_weight=w[tr]), x_te.assign(_weight=w[te]), tr, seed)
            with_weight[i, seed] = evaluate(plus, te)
        inverse = _inverse_weight(w[te], n_classes)
        if metric is not None and metric.get("gini") and inverse is not None:
            # a binary task's class order is arbitrary: 1/weight may point to either class, and the better one counts
            tried = [sign * evaluate(p, te) for p in ([inverse] if not n_classes else [inverse, inverse[:, ::-1]])]
            ceiling.append(sign * np.nanmax(tried) if np.isfinite(tried).any() else np.nan)
    mean_gain = pd.Series(np.mean(gains, axis=0) if gains else np.zeros(len(names)), index=names)
    mean_gain = mean_gain.sort_values(ascending=False, kind="stable")
    checked = [f for f in mean_gain.index[:top] if mean_gain[f] > 0]

    # c.: each top feature's gain without the weight among the features and with it
    plain: dict[str, list[float]] = {f: [] for f in checked}
    through: dict[str, list[float]] = {f: [] for f in checked}
    for i, (tr, te) in enumerate(pairs):
        for f in checked:
            col = f"f{names.index(f)}"
            a_tr, a_te = X.iloc[tr].drop(columns=[col]), X.iloc[te].drop(columns=[col])
            for seed in seeds:
                without = evaluate(fit_predict(a_tr, a_te, tr, seed), te)
                plus = fit_predict(a_tr.assign(_weight=w[tr]), a_te.assign(_weight=w[te]), tr, seed)
                plain[f].append(sign * (honest[i, seed] - without))
                through[f].append(sign * (with_weight[i, seed] - evaluate(plus, te)))

    reference = _spread(sign * (with_weight[k] - honest[k]) for k in honest)
    features_checked = {}
    for f in checked:
        mediated = _spread(np.asarray(plain[f]) - np.asarray(through[f]))
        alone = _spread(plain[f])
        noise = alone["mean"] <= 0 or alone["mean"] < PROXY_SD * alone["sd"]  # no share of a gain within noise
        features_checked[f] = {
            "weight_gain_share": float(mean_gain[f]),
            "gain_without_weight": alone,
            "gain_with_weight": _spread(through[f]),
            "weight_mediated": mediated,
            "mediated_share": float("nan") if noise else mediated["mean"] / alone["mean"],
            "flag": bool(
                mediated["mean"] > PROXY_SD * mediated["sd"] and mediated["mean"] > PROXY_SHARE * reference["mean"]
            ),
        }
    result = {
        "name": name,
        "weight": weight_name,
        "metric": metric["name"] if metric is not None else ("r2" if regression else "roc_auc"),
        "declared_metric": metric is not None,
        "greater_is_better": sign > 0,
        "metric_row_weight": metric.get("row_weight") if metric is not None else None,
        "trained_with_sample_weight": sample_weight is not None,
        "fit_params": dict(fit_params or {}),
        "objective": (fit_params or {}).get("objective") or ("L2" if regression else "log loss"),
        "rows": len(df),
        "features": X.shape[1],
        "splits": len(pairs),
        "seeds": list(seeds),
        "max_rows": max_rows,
        "subsampled": sampled,
        "weight_model": {
            "r2": _spread(r2s),
            "spearman": _spread(rhos),
            "top_features": {f: round(float(mean_gain[f]), 4) for f in mean_gain.index[:top]},
        },
        "honest": _spread(honest.values()),
        "with_weight": _spread(with_weight.values()),
        "leak_reference": reference,
        "inverse_weight_alone": _spread(ceiling) if ceiling else None,
        "features_checked": features_checked,
        "flags": [f for f, v in features_checked.items() if v["flag"]],
        "thresholds": {"sd": PROXY_SD, "share_of_leak_reference": PROXY_SHARE},
        "metric_errors": errors,
    }
    if result["flags"]:
        named = ", ".join(f"`{f}`" for f in result["flags"])
        head = (
            f"Part of the gain of {named} goes through `{weight_name}`, above noise ({PROXY_SD:g} SDs over splits x "
            f"seeds, and {PROXY_SHARE:.0%} of the leak reference): it shrinks once the weight is a feature. "
        )
    else:
        head = f"No checked feature's gain goes through `{weight_name}` above noise. "
    result["reading"] = head + PROXY_TIMING
    if report:
        for line in weight_proxy_lines(result):
            say(line)
    return result


def _stat(stat: dict, *, signed: bool = False) -> str:
    """A mean and its SD as one cell."""
    mean = f"{stat['mean']:+.4g}" if signed else f"{stat['mean']:.5g}"
    return f"{mean} (SD {stat['sd']:.2g})"


def weight_proxy_lines(result: dict) -> list[str]:
    """``weight_proxy``'s result as the lines of the report: what was fitted, the weight model, the leak reference,
    1/weight alone, a table of the checked features and the reading.
    """
    weight = result["weight"]
    rows = (
        f"train and test sides capped at {result['max_rows']:,} random rows (seed 0)"
        if result["subsampled"]
        else "every row of the splits"
    )
    direction = "higher" if result["greater_is_better"] else "lower"
    weighted = f", weighted by `{result['metric_row_weight']}`" if result["metric_row_weight"] else ""
    if not result["declared_metric"]:
        weighted = "; no declared metric, so the probe's own, weighted by the training weight"
    trained = "the task's sample weight" if result["trained_with_sample_weight"] else f"`{weight}`"
    lines = [
        f"weight proxy (probe 22) of `{weight}`: {result['splits']} splits x {len(result['seeds'])} seeds, {rows}; "
        f"metric {result['metric']} ({direction} is better{weighted}); every fit of the target trained with {trained} "
        f"as the row weight (LightGBM objective {result['objective']})"
    ]
    model = result["weight_model"]
    top = ", ".join(f"{f} {share:.0%}" for f, share in model["top_features"].items()) or "none"
    lines.append(
        f"  the weight from the features (LightGBM, fitted on each train side): R^2 {_stat(model['r2'])}, "
        f"Spearman {_stat(model['spearman'])}; top features by gain: {top}"
    )
    lines.append(
        f"  leak reference: honest fit {_stat(result['honest'])}, with the weight as a feature "
        f"{_stat(result['with_weight'])}; the weight gains {_stat(result['leak_reference'], signed=True)}"
    )
    if result["inverse_weight_alone"]:
        lines.append(
            f"  1/weight alone, the ceiling of a proxy: {_stat(result['inverse_weight_alone'])}, against the honest "
            f"fit's {result['honest']['mean']:.5g}"
        )
    table = [("feature", "gain without the weight", "gain with it", "weight-mediated (share of the gain)", "")]
    for f, v in result["features_checked"].items():
        share = "" if np.isnan(v["mediated_share"]) else f", {v['mediated_share']:.0%}"
        table.append(
            (
                f,
                _stat(v["gain_without_weight"], signed=True),
                _stat(v["gain_with_weight"], signed=True),
                _stat(v["weight_mediated"], signed=True) + share,
                "flag" if v["flag"] else "",
            )
        )
    if len(table) > 1:
        widths = [max(len(row[k]) for row in table) for k in range(len(table[0]))]
        lines += ["  " + "  ".join(c.ljust(widths[k]) for k, c in enumerate(row)).rstrip() for row in table]
    if result["metric_errors"]:
        lines.append(f"  the metric failed on some fits (scored NaN, left out): {result['metric_errors'][0]}")
    lines.append(f"  reading: {result['reading']}")
    return lines


def run(  # noqa: PLR0913
    df: pd.DataFrame,
    target: str,
    problem_type: str,
    splits: list,
    *,
    group_cols: list[str] | tuple[str, ...] = (),
    feature_cols: list[str] | tuple[str, ...] | None = None,
    name: str = "dataset",
    n_splits: int = 3,
    max_rows: int = 50_000,
    max_single_features: int = 300,
    n_jobs: int = 8,
    sample_weight: np.ndarray | None = None,
) -> dict:
    """Print the probes of the module docstring for one frame and return their numbers.

    Args:
        df: The rows, with the target and the group columns.
        target: The target column.
        problem_type: ``"regression"``, or a classification type.
        splits: ``(train_idx, test_idx)`` row positions; the first ``n_splits`` are probed.
        group_cols: Columns that are not features (a group id).
        feature_cols: The model inputs, when not every column but the target and the groups is one (a time key
            that only the metric reads).
        name: The dataset's name in the first line and the result.
        n_splits: Splits to probe.
        max_rows: Rows kept (at random) of each train and test side.
        max_single_features: Columns (and missing patterns) fitted one by one; more are screened first.
        n_jobs: Threads per LightGBM model.
        sample_weight: The task's training weight, one value per row of ``df`` (never a column of it), or None.
    """
    regression = problem_type == "regression"
    y = df[target]
    weight = None if sample_weight is None else np.asarray(sample_weight, dtype=float)
    features = df[list(feature_cols)] if feature_cols is not None else df.drop(columns=[target, *group_cols])
    # pandas keeps timezone-aware datetimes apart ("datetimetz"); "datetime" alone lets them through to LightGBM
    X = features.select_dtypes(exclude=["string", "object", "datetime", "datetimetz"])
    rng = np.random.default_rng(0)
    cap = lambda idx: np.sort(rng.choice(idx, min(len(idx), max_rows), replace=False))
    pairs = [(cap(tr), cap(te)) for tr, te in splits][:n_splits]
    fit = lambda data: score(data, y, pairs, regression=regression, n_jobs=n_jobs, weight=weight)
    result = {"name": name, "problem_type": problem_type, "rows": len(df), "features_probed": X.shape[1]}
    result["splits"] = len(pairs)
    result["weighted"] = weight is not None

    weighted = ", every fit and score weighted by the training weight" if weight is not None else ""
    say(f"{name}: {len(df):,} rows, {X.shape[1]} features probed, {len(pairs)} splits{weighted}")
    result["all_features"] = fit(X)
    say(f"all features: {result['all_features']:.3f}")
    shallow = [tree_score(X, y, pairs, regression=regression, depth=d, weight=weight) for d in (2, 3)]
    result["shallow_tree"] = {"depth_2": shallow[0], "depth_3": shallow[1]}
    say(f"shallow tree (depth 2 / 3): {shallow[0]:.3f} / {shallow[1]:.3f}")

    columns = keep_most_informative(X, y, pairs[0][0], max_single_features, regression=regression)
    result["single_screened_out"] = X.shape[1] - len(columns)
    if result["single_screened_out"]:
        say(
            f"screened out of the single-feature fits: {X.shape[1] - len(columns):,} of {X.shape[1]:,} columns "
            f"(kept the {len(columns)} that explain the label best alone on the first training side)"
        )
    single = pd.Series({c: fit(X[[c]]) for c in columns}).sort_values(ascending=False)
    result["single"] = single.to_dict()
    say(f"each feature alone: {single.head(8).round(3).to_dict()}")

    gaps = X.columns[X.isna().any()]
    patterns: dict[bytes, list] = {}
    for col in gaps:
        patterns.setdefault(np.packbits(X[col].isna().to_numpy()).tobytes(), []).append(col)
    indicators = pd.DataFrame({cols[0]: X[cols[0]].isna() for cols in patterns.values()}, index=X.index)
    fitted = keep_most_informative(indicators, y, pairs[0][0], max_single_features, regression=regression)
    result["missing_patterns"], result["missing_screened_out"] = len(patterns), len(patterns) - len(fitted)
    if result["missing_screened_out"]:
        say(
            f"screened out of the missing-indicator fits: {len(patterns) - len(fitted):,} of {len(patterns):,} "
            "distinct missing-value patterns"
        )
    first_of = {c: cols[0] for cols in patterns.values() for c in cols}
    pattern_score = {first: round(fit(indicators[[first]]), 3) for first in fitted}
    missing = {c: pattern_score[first_of[c]] for c in gaps if first_of[c] in pattern_score}
    missing = dict(sorted(missing.items(), key=lambda kv: -kv[1]))
    result["missing"] = missing
    say(f"missing indicator alone: {dict(list(missing.items())[:5])}")
    if not regression:
        floats = [c for c in X.columns if pd.api.types.is_float_dtype(X[c]) and X[c].nunique() > 5]
        if floats:
            fmt = pd.DataFrame({c: written_decimals(X[c]) for c in floats}, index=X.index)
            result["format_alone"] = fit(fmt)
            top = keep_most_informative(fmt, y, pairs[0][0], 3, regression=False)
            result["format_single"] = {c: round(fit(fmt[[c]]), 3) for c in top}
            say(
                f"number format alone (decimals written, {len(floats)} float columns): {result['format_alone']:.3f}; "
                f"best columns: {result['format_single']}"
            )
    result["without"] = {}
    for col in single.index[:3]:
        result["without"][col] = fit(X.drop(columns=[col]))
        say(f"without {col}: {result['without'][col]:.3f}")

    result["exact_copies"] = copy_counts(profile_codes(X), y, splits)
    result["exact_copy_share"] = result["exact_copies"]["matched"]
    say(copy_line("test rows with an exact feature copy in train", result["exact_copies"]))
    other = [c for c in features.columns if c not in X.columns]
    if other:
        result["exact_copies_all_columns"] = copy_counts(profile_codes(features), y, splits)
        result["exact_copy_share_all_columns"] = result["exact_copies_all_columns"]["matched"]
        say(
            copy_line(
                f"the same, string and datetime columns included ({len(other)} of them)",
                result["exact_copies_all_columns"],
            )
        )
    tr, te = pairs[0]
    result.update(string_checks(features, X, y, pairs, regression=regression, n_jobs=n_jobs, weight=weight))

    Z = neighbour_space(X)
    dist, idx = NearestNeighbors(n_neighbors=1).fit(Z[tr]).kneighbors(Z[te])
    nn_y, te_y = y.iloc[tr].to_numpy()[idx[:, 0]], y.iloc[te].to_numpy()
    close = dist[:, 0] <= np.quantile(dist[:, 0], 0.1)
    if regression:
        w_te = weights.take(weight, te)
        result["nn_r2"] = {
            "closest_tenth": r2_score(te_y[close], nn_y[close], sample_weight=weights.take(w_te, close)),
            "all": r2_score(te_y, nn_y, sample_weight=w_te),
        }
        say(f"1-NN R^2: closest tenth {result['nn_r2']['closest_tenth']:.3f}, all {result['nn_r2']['all']:.3f}")
    else:
        chance = float((y.value_counts(normalize=True) ** 2).sum())
        agree = nn_y == te_y
        result["nn_agreement"] = {"closest_tenth": agree[close].mean(), "all": agree.mean(), "chance": chance}
        say(
            f"1-NN label agreement: closest tenth {agree[close].mean():.3f}, all {agree.mean():.3f}, "
            f"chance {chance:.3f}"
        )
    if not regression and y.nunique() == 2:
        rows = np.union1d(tr, te)
        d_all = NearestNeighbors(n_neighbors=2).fit(Z[rows]).kneighbors(Z[rows])[0][:, 1]
        positive = y.cat.categories[1] if isinstance(y.dtype, pd.CategoricalDtype) else np.unique(y.dropna())[1]
        distance_auc = roc_auc_score(y.iloc[rows] == positive, -d_all, sample_weight=weights.take(weight, rows))
        result["distance_auc"] = max(distance_auc, 1 - distance_auc)
        say(f"nearest-neighbour distance alone (label-free), AUC: {result['distance_auc']:.3f}")
    return result
