"""The standard steps of every curated frame: drop columns, cast dtypes, fix the row order.

:class:`~data_foundry.v2.dataset.AbstractCuratedDataset` applies ``cast_dtypes`` (from the ``FeatureTypes`` that
``_feature_types`` returns) and ``order_rows`` (a stable sort by the time column, else a shuffle unless ``shuffle =
False``) after ``_clean``. ``drop_columns`` is for ``_clean`` (it fails on a misspelled name), and ``anonymize_ids``
gives stable anonymous ids. The functions are public so ``_clean`` can also call them mid-way, for example when a
filter needs a parsed date.
"""

from __future__ import annotations

import hashlib
from collections.abc import Iterable, Mapping

import numpy as np
import pandas as pd

SHUFFLE_RANDOM_STATE = 42
"""The seed of the final shuffle of IID and grouped data (the collection has always used 42)."""


def _missing(df: pd.DataFrame, columns: Iterable[str]) -> list[str]:
    return [c for c in columns if c not in df.columns]


def drop_columns(df: pd.DataFrame, columns: Iterable[str]) -> pd.DataFrame:
    """Drop ``columns``; a name that is not in the frame is an error (it is usually a typo).

    Raises:
        KeyError: A column is not in the frame.
    """
    columns = list(dict.fromkeys(columns))
    missing = _missing(df, columns)
    if missing:
        raise KeyError(f"Cannot drop columns that are not in the frame: {missing}")
    return df.drop(columns=columns)


def cast_dtypes(
    df: pd.DataFrame,
    *,
    categorical: Iterable[str] = (),
    string: Iterable[str] = (),
    datetime: Iterable[str] | Mapping[str, str | None] = (),
) -> pd.DataFrame:
    """Cast columns by meaning, the same way for every dataset.

    * ``categorical``: ``category`` dtype (unordered), unused categories removed; text categories are stored as
      ``object``, the dtype they come back with from parquet.
    * ``string``: pandas ``string`` dtype (free text / high-cardinality text); missing values stay ``<NA>``.
    * ``datetime``: ``pd.to_datetime``; a mapping gives a per-column ``format`` (None = inferred).

    Numeric columns are left alone; every column not listed must already be numeric or boolean.

    Raises:
        KeyError: A listed column is not in the frame.
        ValueError: A column is listed under two dtypes.
    """
    categorical, string = list(categorical), list(string)
    formats = dict(datetime) if isinstance(datetime, Mapping) else dict.fromkeys(datetime)
    listed = categorical + string + list(formats)
    duplicated = sorted({c for c in listed if listed.count(c) > 1})
    if duplicated:
        raise ValueError(f"Columns listed under more than one dtype: {duplicated}")
    missing = _missing(df, listed)
    if missing:
        raise KeyError(f"Cannot cast columns that are not in the frame: {missing}")

    # a shallow copy under copy-on-write (the dataset pipeline), else a real one so the caller's frame stays as is
    df = df.copy(deep=not pd.get_option("mode.copy_on_write"))
    for col, fmt in formats.items():
        df[col] = pd.to_datetime(df[col], format=fmt)
    for col in string:
        df[col] = df[col].where(df[col].notna(), np.nan).astype("string")
    for col in categorical:
        df[col] = df[col].astype("category").cat.remove_unused_categories()
        categories = df[col].cat.categories
        if isinstance(categories.dtype, pd.StringDtype):  # `string` categories come back as `object` from parquet
            df[col] = df[col].cat.rename_categories(categories.astype(object))
    return df


def canonical_nans(df: pd.DataFrame) -> pd.DataFrame:
    """Write every missing value of a numpy float column as the one standard NaN.

    An invalid operation (``inf - inf``, ``0 / 0``) gives a NaN with the sign bit set on x86, other platforms give
    other bit patterns, and parquet does not keep them all; the checksum hashes the bits, so a frame with such NaNs
    would not verify after a save and load. The values and the column dtypes do not change.
    """
    out = df
    for col in df.columns:
        dtype = df[col].dtype
        if not (isinstance(dtype, np.dtype) and dtype.kind == "f"):
            continue
        values = df[col].to_numpy()
        missing = np.isnan(values)
        if not missing.any():
            continue
        unsigned = f"u{dtype.itemsize}"
        if (values[missing].view(unsigned) != np.array(np.nan, dtype=dtype).view(unsigned)).any():
            fixed = values.copy()
            fixed[missing] = np.nan
            out = df.copy(deep=False) if out is df else out
            out[col] = fixed
    return out


def order_rows(df: pd.DataFrame, *, time_on: str | None, shuffle: bool) -> pd.DataFrame:
    """Fix the row order and reset the index (splits are positions).

    A temporal task (``time_on`` set) is sorted by time with a stable sort, so ties keep their order. Other
    tasks are shuffled with :data:`SHUFFLE_RANDOM_STATE` unless ``shuffle`` is False, which removes any
    signal the source order carries (sorted by target, by location, by collection batch).
    """
    if time_on is not None:
        df = df.sort_values(time_on, kind="stable")
    elif shuffle:
        df = df.sample(frac=1, random_state=SHUFFLE_RANDOM_STATE)
    return df.reset_index(drop=True)


def anonymize_ids(values: pd.Series, *, length: int = 12) -> pd.Series:
    """Replace identifiers by stable anonymous codes (a hash of each value), the same on every run.

    Use it instead of random ids (``uuid.uuid4()``): random ids change the data, the checksum and grouped
    splits on every run.
    """
    codes = {v: hashlib.blake2b(str(v).encode(), digest_size=16).hexdigest()[:length] for v in values.dropna().unique()}
    return values.map(codes)
