"""The standard steps of every curated frame: drop columns, cast dtypes, fix the row order.

:class:`~data_foundry.v2.dataset.AbstractCuratedDataset` applies ``cast_dtypes`` (from the ``FeatureTypes`` that
``_feature_types`` returns), ``canonical_dtypes`` and ``canonical_nans`` (so pandas 2 and 3 and every platform
build the same container) and ``order_rows`` (the rows in the order of their content, then a stable sort by the
time column, else a shuffle unless ``shuffle = False``) after ``_clean``. ``drop_columns`` is for ``_clean`` (it
fails on a misspelled name), and ``anonymize_ids`` gives stable anonymous ids. The functions are public so
``_clean`` can also call them mid-way, for example when a filter needs a parsed date.
"""

from __future__ import annotations

import hashlib
from collections.abc import Iterable, Mapping

import numpy as np
import pandas as pd

from data_foundry.utils.dtypes import is_str_dtype

SHUFFLE_RANDOM_STATE = 42
"""The seed of the final shuffle of IID and grouped data (the collection has always used 42)."""

PANDAS_3 = int(pd.__version__.split(".", maxsplit=1)[0]) >= 3
"""pandas 3 always copies on write, infers text as the ``str`` dtype and parses dates to ``us`` or ``s``."""


def copy_on_write_enabled() -> bool:
    """Whether pandas copies on write here: always under pandas 3, under pandas 2 when the option is set."""
    return PANDAS_3 or bool(pd.get_option("mode.copy_on_write"))


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
    df = df.copy(deep=not copy_on_write_enabled())
    for col, fmt in formats.items():
        if fmt is None and pd.api.types.is_numeric_dtype(df[col]) and not pd.api.types.is_bool_dtype(df[col]):
            msg = (
                f"`{col}` is numeric, and `pd.to_datetime` reads numbers as nanoseconds since 1970. Give its format "
                f"(`datetime={{'{col}': '%Y%m%d'}}`) or convert it in `_clean` (`pd.to_datetime(..., unit='s')`)."
            )
            raise ValueError(msg)
        df[col] = pd.to_datetime(df[col], format=fmt)
    for col in string:
        df[col] = df[col].where(df[col].notna(), np.nan).astype("string")
    for col in categorical:
        df[col] = df[col].astype("category").cat.remove_unused_categories()
        categories = df[col].cat.categories
        if isinstance(categories.dtype, pd.StringDtype):  # `string` categories come back as `object` from parquet
            df[col] = df[col].cat.rename_categories(categories.astype(object))
    return df


def canonical_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    """Store the dtypes that pandas 2 and pandas 3 choose differently in one way, so both build the same container.

    * datetimes and durations: nanoseconds (pandas 3 parses to ``us`` or ``s``, polars gives ``us``, Excel ``ms``;
      the checksum hashes the integers);
    * text in the pandas 3 ``str`` dtype: ``object``, as pandas 2 reads it (the ``string`` dtype of
      ``cast_dtypes`` stays as it is).

    The values do not change.

    Raises:
        ValueError: A date lies outside the nanosecond range (years 1677 to 2262).
    """
    out = df
    for col in df.columns:
        dtype = df[col].dtype
        if _time_unit(dtype) not in (None, "ns"):
            try:
                fixed = df[col].dt.as_unit("ns")
            except (pd.errors.OutOfBoundsDatetime, pd.errors.OutOfBoundsTimedelta) as error:
                msg = f"`{col}` holds dates outside 1677-2262; store them as numbers (a year, days since a date)."
                raise ValueError(msg) from error
        elif is_str_dtype(dtype):
            fixed = df[col].astype(object)
        else:
            continue
        out = df.copy(deep=False) if out is df else out
        out[col] = fixed
    return out


def _time_unit(dtype: object) -> str | None:
    """The unit of a datetime or timedelta dtype (``ns``, ``us``, ...), else None."""
    if isinstance(dtype, pd.DatetimeTZDtype):
        return dtype.unit
    if isinstance(dtype, np.dtype) and dtype.kind in "mM":
        return np.datetime_data(dtype)[0]
    return None


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

    First the rows are put in the order of their content (:func:`content_order`), so the container depends only
    on which rows ``_clean`` returns, not on the order it returns them in (a join, a file listing or a library
    version can change that). Then a temporal task (``time_on`` set) is sorted by time with a stable sort, so ties
    keep the content order; other tasks are shuffled with :data:`SHUFFLE_RANDOM_STATE`, which removes any signal
    the source order carries (sorted by target, by location, by collection batch). With ``shuffle`` False, the
    order ``_clean`` returns is kept (and only a temporal task is sorted by time).
    """
    if not shuffle and time_on is None:
        return df.reset_index(drop=True)
    # positions first, then one copy of the frame (a `_1m` source can be tens of GB)
    positions = content_order(df) if shuffle else np.arange(len(df))
    if time_on is not None:
        times = df[time_on].iloc[positions].reset_index(drop=True)
        positions = positions[times.sort_values(kind="stable").index.to_numpy()]
    else:  # the same permutation as `df.sample(frac=1, random_state=...)`: it depends only on the length
        positions = pd.Series(positions).sample(frac=1, random_state=SHUFFLE_RANDOM_STATE).to_numpy()
    return df.iloc[positions].reset_index(drop=True)


def content_order(df: pd.DataFrame) -> np.ndarray:
    """The positions of the rows sorted by a hash of their values (stable: identical rows keep their order).

    The hash covers every column in order and ignores the index; a categorical value hashes by its label, not
    its code, so the order does not depend on the order of the categories either.
    """
    hashes = pd.util.hash_pandas_object(df, index=False).to_numpy()
    return np.argsort(hashes, kind="stable")


def anonymize_ids(values: pd.Series, *, length: int = 12) -> pd.Series:
    """Replace identifiers by stable anonymous codes (a hash of each value), the same on every run.

    Use it instead of random ids (``uuid.uuid4()``): random ids change the data, the checksum and grouped
    splits on every run. A text value is hashed as it is; any other value with its type, so ``1`` and ``"1"`` get
    different codes.
    """
    codes = {
        v: hashlib.blake2b(_id_text(v).encode(), digest_size=16).hexdigest()[:length] for v in values.dropna().unique()
    }
    return values.map(codes)


def _id_text(value: object) -> str:
    """The text :func:`anonymize_ids` hashes: a string itself, anything else prefixed with its type name."""
    return value if isinstance(value, str) else f"{type(value).__name__}:{value}"
