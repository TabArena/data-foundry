"""The model probes of the leak run (``run``): what a model learns from the data that it should not.

The package docstring (``data_foundry.probes.leak``) says what each number measures; ``score`` and ``fit_score`` are
the untuned LightGBM fits the other leak modules share, and ``say`` prints a line of the report.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.metrics import r2_score, roc_auc_score
from sklearn.neighbors import NearestNeighbors
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor

from data_foundry.probes import encode, models, scoring

BINS = 10
"""Quantile bins of the screen's step function; a categorical of more levels is scored by ``level_score``."""


WIDE_STRING = 50
"""A string column with more distinct values than this gets its own train-overlap line."""


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
                    w_train=scoring.take(weight, tr),
                    w_test=scoring.take(weight, te),
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
    model = models.lightgbm(regression=regression, n_jobs=n_jobs)
    x_train, x_test = encode.lightgbm_names(x_train), encode.lightgbm_names(x_test)
    models.fit(model, x_train, y_train, w_train)
    if regression:
        return r2_score(y_test, model.predict(x_test), sample_weight=w_test)
    return scoring.auc(y_test.to_numpy(), models.class_proba(model, x_test, classes), classes, w_test)


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
        t_tr, t_te, blocks = encode.encode_text(df, columns, tr, te)
        if not blocks:
            return float("nan")
        if base is not None:
            t_tr = pd.concat([base.iloc[tr].reset_index(drop=True), t_tr], axis=1)
            t_te = pd.concat([base.iloc[te].reset_index(drop=True), t_te], axis=1)
        w_tr, w_te = scoring.take(weight, tr), scoring.take(weight, te)
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
        models.fit(model, numeric.iloc[tr], y.iloc[tr], scoring.take(weight, tr))
        if regression:
            out.append(r2_score(y.iloc[te], model.predict(numeric.iloc[te]), sample_weight=scoring.take(weight, te)))
            continue
        proba = models.class_proba(model, numeric.iloc[te], classes)
        out.append(scoring.auc(y.iloc[te].to_numpy(), proba, classes, scoring.take(weight, te)))
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
    # booleans as 0/1 numbers: get_dummies passes a bool column through, and a nullable one's missing values with it
    num = X.select_dtypes(["number", "bool", "boolean"]).astype(float)
    cats = [c for c in X.columns if c not in num and X[c].nunique() <= 50]
    parts = [((num - num.mean()) / num.std()).fillna(0), pd.get_dummies(X[cats], dummy_na=True) if cats else None]
    return pd.concat(parts, axis=1).to_numpy(dtype=float)


def without_strongest(X: pd.DataFrame, strongest: list, fit) -> dict:
    """The score of ``fit`` on ``X`` without each column of ``strongest``; none with one column, whose drop leaves
    nothing to fit.
    """
    out = {}
    for col in strongest if X.shape[1] > 1 else []:
        out[col] = fit(X.drop(columns=[col]))
        say(f"without {col}: {out[col]:.3f}")
    return out


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
    X = encode.native(features)
    rng = np.random.default_rng(0)
    cap = lambda idx: np.sort(rng.choice(idx, min(len(idx), max_rows), replace=False))
    pairs = [(cap(tr), cap(te)) for tr, te in splits][:n_splits]
    fit = lambda data: score(data, y, pairs, regression=regression, n_jobs=n_jobs, weight=weight)
    result = {"name": name, "problem_type": problem_type, "rows": len(df), "features_probed": X.shape[1]}
    result["splits"] = len(pairs)
    result["weighted"] = weight is not None

    weighted = ", every fit and score weighted by the training weight" if weight is not None else ""
    say(f"{name}: {len(df):,} rows, {X.shape[1]} features probed, {len(pairs)} splits{weighted}")
    if X.shape[1] == 0:
        result["skipped"] = "no numeric, categorical or boolean feature: only string and datetime columns"
        say(f"no model fits: {result['skipped']} (the task probes encode the strings as text)")
        result.update(string_checks(features, X, y, pairs, regression=regression, n_jobs=n_jobs, weight=weight))
        return result
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
    result["without"] = without_strongest(X, list(single.index[:3]), fit)

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
        w_te = scoring.take(weight, te)
        result["nn_r2"] = {
            "closest_tenth": r2_score(te_y[close], nn_y[close], sample_weight=scoring.take(w_te, close)),
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
        # the second observed class: a categorical's levels can include one no row holds
        observed = set(y.dropna())
        levels = y.cat.categories if isinstance(y.dtype, pd.CategoricalDtype) else np.unique(y.dropna())
        positive = [c for c in levels if c in observed][1]
        distance_auc = roc_auc_score(y.iloc[rows] == positive, -d_all, sample_weight=scoring.take(weight, rows))
        result["distance_auc"] = max(distance_auc, 1 - distance_auc)
        say(f"nearest-neighbour distance alone (label-free), AUC: {result['distance_auc']:.3f}")
    return result
