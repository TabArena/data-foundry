from __future__ import annotations

import hashlib
import json
from typing import Any

import pandas as pd
import pydantic


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

    # Canonical: sorted keys, compact separators
    s = json.dumps(py, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return s.encode("utf-8")


def encode_dataset(df: pd.DataFrame) -> bytes:
    """Stable fingerprint for a DataFrame: schema + content (+ index)."""
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



