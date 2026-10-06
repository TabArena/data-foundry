"""Canonical encodings of container frames and metadata for the checksum."""

from __future__ import annotations

import hashlib
import json
from typing import Any

import pandas as pd
import pydantic

from data_foundry.utils.dtypes import is_str_dtype


def omit_unset_fields(obj: Any, dumped: Any) -> Any:
    """Drop the fields of ``obj`` listed in its ``_OMIT_WHEN_UNSET`` from ``dumped`` while they are ``None``.

    Fields added to a metadata class after containers shipped are listed there, so a container that does not set
    them keeps its checksum and its saved JSON.
    """
    omit = getattr(type(obj), "_OMIT_WHEN_UNSET", ())
    if omit and isinstance(dumped, dict):
        dumped = {k: v for k, v in dumped.items() if not (k in omit and v is None)}
    return dumped


def encode_pydantic_metadata(obj: Any) -> bytes:
    """Canonical JSON bytes for pydantic dataclasses/models (and plain python types),
    with stable key ordering and no whitespace.
    """
    # Pydantic v2: pydantic_core.to_json gives you JSON bytes directly, already
    # consistent for supported types. We still canonicalize key ordering by going
    # through python + json.dumps(sort_keys=True).
    py = pydantic.TypeAdapter(Any).dump_python(
        obj,
        mode="json",  # json-safe python types
        by_alias=True,
        exclude_none=False,
        round_trip=True,  # preserve e.g. tuples vs lists where possible
    )
    py = omit_unset_fields(obj, py)

    # Canonical: sorted keys, compact separators
    s = json.dumps(py, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return s.encode("utf-8")


CHECKSUM_VERSION = 2
"""The checksum new containers get. Version 1 (a bare hex digest, every container before 2026-10-06) hashes the
dtype names, the values and the index; version 2 (``v2:<hex>``) adds the categories, their order and ``ordered``,
and the test set, and leaves out the index (a new container has a ``RangeIndex``). A container keeps verifying with
the version its checksum states."""


def checksum_version(checksum: str | None) -> int:
    """The version a stored checksum was computed with: the ``v<n>:`` prefix, or 1 for a bare hex digest."""
    if checksum and ":" in checksum:
        prefix = checksum.split(":", 1)[0]
        if prefix.startswith("v") and prefix[1:].isdigit():
            return int(prefix[1:])
        raise ValueError(f"Unknown checksum prefix {prefix!r} in {checksum!r}.")
    return 1


def categorical_details(df: pd.DataFrame) -> dict[str, dict]:
    """Per categorical column: the categories in their order, the dtype of the categories, and ``ordered``.

    Text categories count as ``object`` under pandas 2 and 3 alike (pandas 3 may hold them as ``str``).
    """
    details = {}
    for col, dtype in df.dtypes.items():
        if isinstance(dtype, pd.CategoricalDtype):
            categories = dtype.categories
            details[str(col)] = {
                "categories": categories.tolist(),
                "categories_dtype": "object" if is_str_dtype(categories.dtype) else str(categories.dtype),
                "ordered": bool(dtype.ordered),
            }
    return details


def encode_dataset_v2(df: pd.DataFrame) -> bytes:
    """Checksum version 2 of a frame: shape, column names, dtypes, categorical details and the row values.

    The index is left out (a version-2 container has a ``RangeIndex``), and so is the storage of the ``string``
    dtype (``python`` or ``pyarrow``, which pandas versions choose differently for the same values).
    """
    meta = {
        "shape": df.shape,
        "columns": [str(c) for c in df.columns],
        "dtypes": {str(c): "object" if is_str_dtype(dt) else str(dt) for c, dt in df.dtypes.items()},
        "categories": categorical_details(df),
    }
    row_hashes = pd.util.hash_pandas_object(df, index=False).to_numpy("uint64")
    h = hashlib.blake2b(digest_size=32)
    h.update(encode_pydantic_metadata(meta))
    h.update(row_hashes.tobytes(order="C"))
    return h.digest()


def encode_dataset(df: pd.DataFrame) -> bytes:
    """Stable fingerprint for a DataFrame: schema + content (+ index). Checksum version 1."""
    meta = {
        "shape": df.shape,
        "columns": [str(c) for c in df.columns],
        "index_name": df.index.name,
        "column_names": list(df.columns.names) if df.columns.nlevels > 1 else None,
        "index_names": list(df.index.names) if df.index.nlevels > 1 else None,
        "dtypes": {str(c): str(dt) for c, dt in df.dtypes.items()},
    }

    # Content hash (includes index!)
    row_hashes = pd.util.hash_pandas_object(df, index=True).to_numpy("uint64")

    h = hashlib.blake2b(digest_size=32)
    h.update(encode_pydantic_metadata(meta))
    h.update(row_hashes.tobytes(order="C"))
    return h.digest()
