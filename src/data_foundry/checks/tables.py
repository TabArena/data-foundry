"""The summary tables of a frame (:func:`run_all_checks`) that each dataset's README shows under "Data checks"."""

from __future__ import annotations

import numpy as np
import pandas as pd
from pandas.api import types as pdtypes

from data_foundry.utils.dtypes import object_columns

CLASSIFICATION = ("binary_classification", "multiclass_classification")

MAX_VALUE_LENGTH = 67
"""A category value longer than this is cut in the categorical table."""


def run_all_checks(
    *,
    data: pd.DataFrame,
    target_feature: str,
    problem_type: str,
    sample_threshold: int = 1_000_000,
    sample_frac: float = 0.1,
    sample_random_state: int = 0,
) -> dict[str, pd.DataFrame | str]:
    """The README's summary tables of ``data``.

    Missing-value and unique counts and the class counts of a classification target are exact; on a frame with more
    than ``sample_threshold`` rows the example values, the numeric and categorical statistics and the regression
    target's shape are computed on a random sample of ``sample_frac`` of the rows.

    Args:
        data: The curated frame.
        target_feature: The target column.
        problem_type: ``"binary_classification"``, ``"multiclass_classification"`` or ``"regression"``.
        sample_threshold: Above this many rows the heavier statistics use a sample.
        sample_frac: The share of rows sampled.
        sample_random_state: The seed of the sample.

    Returns:
        ``summary`` (per column: dtype, missing values, distinct values, examples), ``numeric_stats``, ``cat_stats``
        (the five most frequent values per column) and ``target`` (the class counts, or the regression target's
        shape). ``numeric_stats`` and ``cat_stats`` are a sentence when the frame has no such column.

    Raises:
        TypeError: A column has ``object`` dtype, or a classification target is not ``category``.
        ValueError: The target is not a column, or its class count does not fit the problem type.
    """
    object_cols = object_columns(data)
    if object_cols:
        raise TypeError(f"DataFrame contains object dtype columns: {object_cols}")
    if target_feature not in data.columns:
        raise ValueError(f"target_feature '{target_feature}' is not in the DataFrame.")
    classification = problem_type in CLASSIFICATION
    if classification:
        _check_classification_target(data[target_feature], target_feature, problem_type)

    n_rows = len(data)
    use_sampling = sample_frac is not None and n_rows > sample_threshold and 0.0 < sample_frac < 1.0
    sample_df = data.sample(frac=sample_frac, random_state=sample_random_state) if use_sampling else data
    sample_idx = sample_df.index if use_sampling else None
    cols = list(data.columns)
    numeric_cols = [c for c in cols if pdtypes.is_numeric_dtype(data[c])]
    return {
        "summary": _summary(data, cols, sample_idx),
        "numeric_stats": _numeric_stats(data, numeric_cols, sample_idx),
        "cat_stats": _cat_stats(data, [c for c in cols if c not in numeric_cols], sample_idx),
        "target": _target_table(data, target_feature, sample_df, classification=classification),
    }


def _check_classification_target(target: pd.Series, name: str, problem_type: str) -> None:
    if not isinstance(target.dtype, pd.CategoricalDtype):
        raise TypeError(
            f"Classification target '{name}' has dtype '{target.dtype}'. Expected category dtype for classification "
            "tasks."
        )
    n_classes = target.nunique()
    if problem_type == "binary_classification" and n_classes != 2:
        raise ValueError(
            f"problem_type is 'binary_classification' but target '{name}' has {n_classes} unique classes (expected "
            "exactly 2)."
        )
    if problem_type == "multiclass_classification" and n_classes < 3:
        raise ValueError(
            f"problem_type is 'multiclass_classification' but target '{name}' has {n_classes} unique classes "
            "(expected at least 3)."
        )


def _summary(data: pd.DataFrame, cols: list, sample_idx: pd.Index | None) -> pd.DataFrame:
    """Per column: dtype, missing values (count and percent), distinct values and the ten most frequent values."""
    n_missing = pd.Series(index=cols, dtype=int)
    n_unique = pd.Series(index=cols, dtype=int)
    examples = {}
    for c in cols:
        s = data[c]
        n_missing[c] = int(s.isna().sum())
        n_unique[c] = int(s.nunique())
        examples[c] = _examples(s if sample_idx is None else s.loc[sample_idx])
    summary = pd.DataFrame(
        {
            "dtype": data.dtypes,
            "n_missing": n_missing,
            "pct_missing": (n_missing / len(data) * 100).round(2),
            "n_unique": n_unique,
        }
    )
    summary["examples"] = pd.Series(examples)
    summary["dtype"] = summary["dtype"].astype("string")
    return summary.sort_values(["dtype", "pct_missing"], ascending=[True, False]).reset_index()


def _examples(s: pd.Series, n: int = 10) -> str:
    values = []
    for v in s.dropna().value_counts().head(n).index:
        shown = (round(v, 4) if round(v, 4) != 0 else 0.0) if isinstance(v, float) and not np.isnan(v) else v
        values.append(str(shown))
    return ", ".join(values)


def _numeric_stats(data: pd.DataFrame, numeric_cols: list, sample_idx: pd.Index | None) -> pd.DataFrame | str:
    if not numeric_cols:
        return "No numeric features to summarize."
    rows = {}
    for c in numeric_cols:
        s = data[c] if sample_idx is None else data[c].loc[sample_idx]
        cnt = s.count()
        rows[c] = {
            "count": float(cnt),
            "mean": float(s.mean()) if cnt > 0 else np.nan,
            "std": float(s.std()) if cnt > 0 else np.nan,
            "min": float(s.min()) if cnt > 0 else np.nan,
            "max": float(s.max()) if cnt > 0 else np.nan,
        }
    return pd.DataFrame.from_dict(rows, orient="index")[["count", "mean", "std", "min", "max"]]


def _truncate(v: object) -> str:
    if pd.isna(v):
        return "<NA>"
    s = str(v)
    return s if len(s) <= MAX_VALUE_LENGTH else s[: MAX_VALUE_LENGTH - 3] + "..."


def _cat_stats(data: pd.DataFrame, cat_cols: list, sample_idx: pd.Index | None) -> pd.DataFrame | str:
    if not cat_cols:
        return "No categorical/object features to summarize."
    n = len(data) if sample_idx is None else len(sample_idx)
    frames = []
    for col in cat_cols:
        s = data[col] if sample_idx is None else data[col].loc[sample_idx]
        table = s.value_counts(dropna=False).head(5).rename_axis("value").reset_index(name="count")
        table["value"] = table["value"].map(_truncate)
        table["pct"] = (table["count"] / n * 100).round(2)
        table["rank"] = range(1, len(table) + 1)
        table["column"] = col
        frames.append(table[["column", "rank", "value", "count", "pct"]])
    return pd.concat(frames, ignore_index=True).set_index(["column", "rank"]).sort_index()


def _target_table(data: pd.DataFrame, target: str, sample_df: pd.DataFrame, *, classification: bool) -> pd.DataFrame:
    """The class counts (exact), or a regression target's shape: skew and variance before and after a log, and
    whether an exponential or a lognormal fits its positive values better (by AIC).
    """
    from scipy import stats  # noqa: PLC0415 - scipy is a build dependency

    if classification:
        counts = data[target].value_counts(dropna=False)
        return pd.DataFrame({"count": counts, "pct": (counts / len(data) * 100).round(2)})
    y_missing_count = int(data[target].isna().sum())
    y = sample_df[target].dropna().astype(float)
    nonpos_pct = float((y <= 0).mean() * 100) if len(y) > 0 else 0.0
    if (y > 0).all():
        y_log, log_type = np.log(y), "log"
    else:
        y_log, log_type = np.log1p(y), "log1p"
    skew_y = float(stats.skew(y, bias=False)) if len(y) > 0 else np.nan
    skew_log = float(stats.skew(y_log, bias=False)) if len(y_log) > 0 else np.nan
    var_y = float(y.var()) if len(y) > 0 else np.nan
    var_log = float(y_log.var()) if len(y_log) > 0 else np.nan
    y_pos = y[y > 0]
    if len(y_pos) >= 30:
        _, scale = stats.expon.fit(y_pos)
        aic_exp = 2 * 1 - 2 * np.sum(stats.expon.logpdf(y_pos, scale=scale))  # 1 param: scale
        s_fit, _, scale = stats.lognorm.fit(y_pos)
        aic_logn = 2 * 2 - 2 * np.sum(stats.lognorm.logpdf(y_pos, s=s_fit, scale=scale))  # 2 params: s, scale
        dist_hint = "lognormal" if aic_logn < aic_exp else "exponential"
    else:
        aic_exp = aic_logn = np.nan
        dist_hint = "insufficient_data"
    return pd.DataFrame(
        {
            "y_missing_count": [y_missing_count],
            "non_positive_pct": [round(nonpos_pct, 2)],
            "skew_y": [round(skew_y, 3)],
            "skew_log": [round(skew_log, 3)],
            "var_y": [round(var_y, 3)],
            "var_log": [round(var_log, 3)],
            "log_used": [log_type],
            "aic_exponential": [round(aic_exp, 1)],
            "aic_lognormal": [round(aic_logn, 1)],
            "dist_hint": [dist_hint],
        }
    )
