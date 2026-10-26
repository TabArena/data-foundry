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
* the share of test rows whose feature vector has an exact copy in train; when the data has string or datetime
  columns, the same share with them included, and for each string column of more than 50 distinct values the share
  of test rows whose value occurs in train (a copy at the level of a SMILES string or a text);
* each such string column alone, and all features with the string columns, encoded as in the task probes (TF-IDF +
  SVD fitted on the train side; character n-grams for one-token strings such as a SMILES): a text whose content
  gives the label away scores close to the full model on its own;
* the 1-nearest-neighbour label agreement (R^2 for regression) for the closest tenth of the test rows and for
  all of them, against chance;
* for a binary target, the ROC AUC of a label-free score: each row's distance to its nearest other row.

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

from curation_probes.text import encode_text

BINS = 10
"""Quantile bins of the screen's step function; a categorical of more levels is scored by ``level_score``."""
WIDE_STRING = 50
"""A string column with more distinct values than this gets its own train-overlap line."""


def auc(y_true: np.ndarray, proba: np.ndarray, classes: np.ndarray) -> float:
    """ROC AUC of ``proba`` (one column per entry of ``classes``); for more than two classes, the mean one-vs-rest
    ROC AUC over the classes present in ``y_true``. NaN when ``y_true`` holds one class only.
    """
    present = [k for k, c in enumerate(classes) if np.any(y_true == c)]
    if len(present) < 2:
        return float("nan")
    if len(classes) == 2:  # binary
        return float(roc_auc_score(y_true == classes[1], proba[:, 1]))
    return float(np.mean([roc_auc_score(y_true == classes[k], proba[:, k]) for k in present]))


def class_proba(model, data: pd.DataFrame, classes: np.ndarray) -> np.ndarray:
    """The model's class probabilities, one column per entry of ``classes`` (0 for a class it was not trained on)."""
    out = np.zeros((len(data), len(classes)))
    position = {c: i for i, c in enumerate(classes)}
    out[:, [position[c] for c in model.classes_]] = model.predict_proba(data)
    return out


def score(data: pd.DataFrame, y: pd.Series, pairs: list, *, regression: bool, n_jobs: int = 8) -> float:
    """Mean ROC AUC (one-vs-rest for multiclass, see ``auc``) or R^2 of an untuned LightGBM over the split pairs."""
    classes = None if regression else np.unique(y.to_numpy())
    return float(
        np.nanmean(
            [
                fit_score(
                    data.iloc[tr], data.iloc[te], y.iloc[tr], y.iloc[te], classes, regression=regression, n_jobs=n_jobs
                )
                for tr, te in pairs
            ]
        )
    )


def fit_score(x_train, x_test, y_train, y_test, classes, *, regression: bool, n_jobs: int) -> float:
    """One untuned LightGBM fit, scored as in ``score``."""
    model = (lgb.LGBMRegressor if regression else lgb.LGBMClassifier)(n_estimators=200, verbose=-1, n_jobs=n_jobs)
    model.fit(x_train, y_train)
    if regression:
        return r2_score(y_test, model.predict(x_test))
    return auc(y_test.to_numpy(), class_proba(model, x_test, classes), classes)


def text_score(
    df: pd.DataFrame,
    columns: list[str],
    base: pd.DataFrame | None,
    y: pd.Series,
    pairs: list,
    *,
    regression: bool,
    n_jobs: int,
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
        out.append(fit_score(t_tr, t_te, y.iloc[tr], y.iloc[te], classes, regression=regression, n_jobs=n_jobs))
    return float(np.nanmean(out))


def tree_score(data: pd.DataFrame, y: pd.Series, pairs: list, *, regression: bool, depth: int) -> float:
    """Mean ROC AUC (one-vs-rest for multiclass, see ``auc``) or R^2 of a decision tree of the given depth."""
    numeric = data.apply(
        lambda s: s.cat.codes.where(s.cat.codes >= 0) if isinstance(s.dtype, pd.CategoricalDtype) else s
    ).astype(float)
    classes = None if regression else np.unique(y.to_numpy())
    out = []
    for tr, te in pairs:
        model = (DecisionTreeRegressor if regression else DecisionTreeClassifier)(max_depth=depth, random_state=0)
        model.fit(numeric.iloc[tr], y.iloc[tr])
        if regression:
            out.append(r2_score(y.iloc[te], model.predict(numeric.iloc[te])))
            continue
        out.append(auc(y.iloc[te].to_numpy(), class_proba(model, numeric.iloc[te], classes), classes))
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
    features: pd.DataFrame, X: pd.DataFrame, y: pd.Series, pairs: list, *, regression: bool, n_jobs: int
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
        col: text_score(features, [col], None, y, pairs, regression=regression, n_jobs=n_jobs) for col in wide
    }
    say(f"string column alone, as text: { {c: round(v, 3) for c, v in out['string_alone'].items()} }")
    out["all_features_with_strings"] = text_score(features, wide, X, y, pairs, regression=regression, n_jobs=n_jobs)
    say(f"all features with the string columns as text: {out['all_features_with_strings']:.3f}")
    return out


def run(
    df: pd.DataFrame,
    target: str,
    problem_type: str,
    splits: list,
    *,
    group_cols: list[str] | tuple[str, ...] = (),
    name: str = "dataset",
    n_splits: int = 3,
    max_rows: int = 50_000,
    max_single_features: int = 300,
    n_jobs: int = 8,
) -> dict:
    """Print the probes of the module docstring for one frame and return their numbers.

    Args:
        df: The rows, with the target and the group columns.
        target: The target column.
        problem_type: ``"regression"``, or a classification type.
        splits: ``(train_idx, test_idx)`` row positions; the first ``n_splits`` are probed.
        group_cols: Columns that are not features (a group id).
        name: The dataset's name in the first line and the result.
        n_splits: Splits to probe.
        max_rows: Rows kept (at random) of each train and test side.
        max_single_features: Columns (and missing patterns) fitted one by one; more are screened first.
        n_jobs: Threads per LightGBM model.
    """
    regression = problem_type == "regression"
    y = df[target]
    features = df.drop(columns=[target, *group_cols])
    X = features.select_dtypes(exclude=["string", "object", "datetime"])
    rng = np.random.default_rng(0)
    cap = lambda idx: np.sort(rng.choice(idx, min(len(idx), max_rows), replace=False))
    pairs = [(cap(tr), cap(te)) for tr, te in splits][:n_splits]
    fit = lambda data: score(data, y, pairs, regression=regression, n_jobs=n_jobs)
    result = {"name": name, "problem_type": problem_type, "rows": len(df), "features_probed": X.shape[1]}
    result["splits"] = len(pairs)

    say(f"{name}: {len(df):,} rows, {X.shape[1]} features probed, {len(pairs)} splits")
    result["all_features"] = fit(X)
    say(f"all features: {result['all_features']:.3f}")
    shallow = [tree_score(X, y, pairs, regression=regression, depth=d) for d in (2, 3)]
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
    result["without"] = {}
    for col in single.index[:3]:
        result["without"][col] = fit(X.drop(columns=[col]))
        say(f"without {col}: {result['without'][col]:.3f}")

    tr, te = pairs[0]
    key = pd.util.hash_pandas_object(X, index=False)
    result["exact_copy_share"] = float(key.iloc[te].isin(set(key.iloc[tr])).mean())
    say(f"test rows with an exact feature copy in train: {result['exact_copy_share']:.1%}")
    other = [c for c in features.columns if c not in X.columns]
    if other:
        key = pd.util.hash_pandas_object(features, index=False)
        result["exact_copy_share_all_columns"] = float(key.iloc[te].isin(set(key.iloc[tr])).mean())
        say(
            f"test rows with an exact copy in train, string and datetime columns included ({len(other)} of them): "
            f"{result['exact_copy_share_all_columns']:.1%}"
        )
    result.update(string_checks(features, X, y, pairs, regression=regression, n_jobs=n_jobs))

    Z = neighbour_space(X)
    dist, idx = NearestNeighbors(n_neighbors=1).fit(Z[tr]).kneighbors(Z[te])
    nn_y, te_y = y.iloc[tr].to_numpy()[idx[:, 0]], y.iloc[te].to_numpy()
    close = dist[:, 0] <= np.quantile(dist[:, 0], 0.1)
    if regression:
        result["nn_r2"] = {"closest_tenth": r2_score(te_y[close], nn_y[close]), "all": r2_score(te_y, nn_y)}
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
        distance_auc = roc_auc_score(y.iloc[rows] == positive, -d_all)
        result["distance_auc"] = max(distance_auc, 1 - distance_auc)
        say(f"nearest-neighbour distance alone (label-free), AUC: {result['distance_auc']:.3f}")
    return result
