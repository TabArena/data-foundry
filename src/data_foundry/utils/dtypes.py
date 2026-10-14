"""Dtype helpers that give the same answer under pandas 2 and pandas 3."""

from __future__ import annotations

import pandas as pd
from pandas.api.types import is_object_dtype


def is_str_dtype(dtype: object) -> bool:
    """Whether ``dtype`` is pandas 3's default text dtype ``str``, which pandas 2 reads as ``object``.

    ``str`` is a ``StringDtype`` with NaN as its missing value; the ``string`` dtype for free text uses ``<NA>``.
    """
    return isinstance(dtype, pd.StringDtype) and dtype.na_value is not pd.NA


def object_columns(df: pd.DataFrame) -> list:
    """The columns of dtype ``object``, counting pandas 3's ``str`` dtype (see :func:`is_str_dtype`).

    Use this instead of ``df.select_dtypes(include=["object"])``, which pandas 3 deprecates for ``str`` columns.
    """
    return [col for col, dtype in df.dtypes.items() if is_object_dtype(dtype) or is_str_dtype(dtype)]
