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

import numpy as np
import pandas as pd
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer

TEXT_COMPONENTS = 16
MAX_TEXT_COLUMNS = 30
ONE_TOKEN_SHARE = 0.9
"""A text column whose values are a single token in at least this share of rows is encoded by character n-grams."""


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


def numeric(df: pd.DataFrame, drop: list[str] | tuple[str, ...] = ()) -> tuple[pd.DataFrame, list[str], list[str]]:
    """Numeric model inputs (columns ``f0``, ``f1``, ...), their original names, and the text columns left out;
    ``drop`` names columns that are no inputs.
    """
    X = df.drop(columns=[c for c in drop if c in df.columns])
    text = list(X.select_dtypes(include=["string", "object"]).columns)
    X = X.drop(columns=text)
    for col in X.columns:
        if isinstance(X[col].dtype, pd.CategoricalDtype):
            X[col] = X[col].cat.codes.replace(-1, len(X[col].cat.categories))
        elif is_time(X[col]):
            X[col] = seconds(X[col])
    X = X.astype(float)
    names = list(X.columns)
    X = X.fillna(X.median()).fillna(0.0)
    X.columns = [f"f{i}" for i in range(X.shape[1])]
    return X, names, text


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


def text_vectorizer(values: np.ndarray) -> TfidfVectorizer:
    """Word TF-IDF for prose; character 2- to 5-grams when most values are one token (SMILES, codes, URLs)."""
    sample = pd.Series(values[:5_000], dtype="string").fillna("")
    one_token = float((~sample.str.strip().str.contains(r"\s")).mean()) if len(sample) else 0.0
    if one_token >= ONE_TOKEN_SHARE:
        return TfidfVectorizer(
            analyzer="char", ngram_range=(2, 5), max_features=20_000, min_df=2, sublinear_tf=True, dtype=np.float32
        )
    return TfidfVectorizer(max_features=20_000, min_df=2, sublinear_tf=True, dtype=np.float32)


def encode_text(
    df: pd.DataFrame, text: list[str], train: np.ndarray, test: np.ndarray
) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, list[str]]]:
    """Each text column as TF-IDF + SVD components fitted on the train rows; the column blocks by source column."""
    tr_parts, te_parts, blocks = [], [], {}
    for k, col in enumerate(text[:MAX_TEXT_COLUMNS]):
        values = df[col].astype("string").fillna("").to_numpy(dtype=object)
        try:
            vectorizer = text_vectorizer(values[train])
            a_train = vectorizer.fit_transform(values[train])
        except ValueError:  # no term occurs twice: nothing to encode
            continue
        n = min(TEXT_COMPONENTS, a_train.shape[1] - 1)
        if n < 1:
            continue
        svd = TruncatedSVD(n_components=n, random_state=0)
        cols = [f"t{k}_{j}" for j in range(n)]
        tr_parts.append(pd.DataFrame(svd.fit_transform(a_train), columns=cols))
        te_parts.append(pd.DataFrame(svd.transform(vectorizer.transform(values[test])), columns=cols))
        blocks[col] = cols
    if not tr_parts:
        return pd.DataFrame(index=range(len(train))), pd.DataFrame(index=range(len(test))), {}
    return pd.concat(tr_parts, axis=1), pd.concat(te_parts, axis=1), blocks
