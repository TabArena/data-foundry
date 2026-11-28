"""Model inputs for the probes: one encoder, so a column enters every probe the same way.

The probes read the model inputs only (``ProbeInput.feature_cols``); these functions turn them into what a model fits:

* ``numeric``: every input as a number, for models that need numbers (linear, random forest, kNN). Categoricals
  enter as their codes, a missing value as one more code after the levels (a median code would depend on the order
  of the levels); datetimes, periods and durations as seconds (``seconds``); a missing number or date as the column's
  median (0 for a column without values). String columns are left out and returned by name.
* ``native``: the inputs as LightGBM and the trees read them, categories kept as categories and missing values as
  missing. String columns are left out, durations enter as seconds, and datetimes are left out or, with
  ``dates=True``, enter as days since the earliest (a participant reads the period from them).
* ``encode_text``: each text column as ``TEXT_COMPONENTS`` TF-IDF + SVD components fitted on the train rows only:
  words for prose, character 2- to 5-grams for strings that are mostly one token (a SMILES, a code, a URL), where
  words would only match whole repeated values.

A missing date stays missing in every mode (as NaN seconds or days) until ``numeric`` fills it with the median.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pandas as pd

from data_foundry.encodings import encode_text_tfidf

if TYPE_CHECKING:
    import numpy as np

MAX_TEXT_COLUMNS = 30


def seconds(values: pd.Series) -> pd.Series:
    """A datetime, period or duration column as float seconds (a datetime since 1970, UTC for one with a time zone);
    a missing value stays NaN. Casting to ``int64`` would turn a missing date into -9.2e9 seconds (pandas 2) or
    raise (pandas 3).
    """
    if isinstance(values.dtype, pd.PeriodDtype):
        values = values.dt.to_timestamp()
    if pd.api.types.is_timedelta64_dtype(values):
        return values / pd.Timedelta(seconds=1)
    return (values - pd.Timestamp(0, tz=values.dt.tz)) / pd.Timedelta(seconds=1)


def is_time(values: pd.Series) -> bool:
    """Whether ``seconds`` takes the column: a datetime (with or without a time zone), a period or a duration."""
    return (
        pd.api.types.is_datetime64_any_dtype(values)
        or pd.api.types.is_timedelta64_dtype(values)
        or isinstance(values.dtype, pd.PeriodDtype)
    )


def numeric(
    df: pd.DataFrame, drop: list[str] | tuple[str, ...] = (), rows: np.ndarray | None = None
) -> tuple[pd.DataFrame, list[str], list[str]]:
    """Numeric model inputs (columns ``f0``, ``f1``, ...), their original names, and the text columns left out;
    ``drop`` names columns that are no inputs.

    ``rows`` (positions in ``df``) returns those rows only, indexed ``0..len(rows) - 1``: a column at a time is
    converted and its median taken over every row, so the values equal the whole frame's at those positions, and the
    memory follows the rows kept (a ``_1m`` container's millions of training rows, of which a probe fits a sample).
    """
    dropped = set(drop)
    inputs = [c for c in df.columns if c not in dropped]
    text = list(df.iloc[:0][inputs].select_dtypes(include=["string", "object"]).columns)
    names = [c for c in inputs if c not in set(text)]
    columns = {}
    for k, col in enumerate(names):
        values = df[col]
        if isinstance(values.dtype, pd.CategoricalDtype):
            values = values.cat.codes.replace(-1, len(values.cat.categories))
        elif is_time(values):
            values = seconds(values)
        values = values.astype(float)
        median = values.median()
        if rows is not None:
            values = values.iloc[rows]
        columns[f"f{k}"] = values.fillna(0.0 if pd.isna(median) else median).to_numpy()
    index = pd.RangeIndex(len(rows)) if rows is not None else df.index
    return pd.DataFrame(columns, index=index), names, text


def native(features: pd.DataFrame, *, dates: bool = False) -> pd.DataFrame:
    """The inputs as LightGBM and the trees read them: no string column, a duration as seconds, and a datetime left
    out or, with ``dates``, as days since the column's earliest (after the other columns). Missing values stay missing.
    """
    # pandas keeps timezone-aware datetimes apart ("datetimetz"); "datetime" alone lets them through to LightGBM
    X = features.select_dtypes(exclude=["string", "object", "datetime", "datetimetz"])
    durations = X.select_dtypes("timedelta").columns
    if len(durations) or dates:
        X = X.copy()
    for col in durations:
        X[col] = seconds(X[col])
    if dates:
        for col in features.columns:
            s = features[col]
            if pd.api.types.is_datetime64_any_dtype(s):
                s = s.dt.tz_localize(None) if s.dt.tz is not None else s
                X[col] = (s - s.min()).dt.total_seconds() / 86_400
    return X


def lightgbm_names(X: pd.DataFrame) -> pd.DataFrame:
    """``X`` with its columns named ``f0``, ``f1``, ...: LightGBM refuses names with JSON characters (a spectrum's
    ``M/Z:800.32``), and the fits need no names.
    """
    return X.set_axis([f"f{i}" for i in range(X.shape[1])], axis=1)


def encode_text(
    df: pd.DataFrame, text: list[str], train: np.ndarray, test: np.ndarray
) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, list[str]]]:
    """Each text column as TF-IDF + SVD components fitted on the train rows (``encodings.encode_text_tfidf``, the
    recommended encoding); the column blocks by source column. A column with no term in its train rows is left out.
    """
    tr_parts, te_parts, blocks = [], [], {}
    for k, col in enumerate(text[:MAX_TEXT_COLUMNS]):
        values = df[col].reset_index(drop=True)
        tr, te = encode_text_tfidf(
            values.iloc[train].reset_index(drop=True), values.iloc[test].reset_index(drop=True), prefix=f"t{k}_"
        )
        if tr.shape[1] == 0:
            continue
        tr_parts.append(tr)
        te_parts.append(te)
        blocks[col] = list(tr.columns)
    if not tr_parts:
        return pd.DataFrame(index=range(len(train))), pd.DataFrame(index=range(len(test))), {}
    return pd.concat(tr_parts, axis=1), pd.concat(te_parts, axis=1), blocks
