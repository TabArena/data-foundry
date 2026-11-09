"""The row table of a format-2 container: per-row metadata that is not a model feature, next to the data.

``rows.parquet`` holds one row per row of ``dataset.parquet``, in the same order. Today it holds the outer splits, one
column per split named ``split_r<repeat>_f<fold>``, with the value ``train``, ``test`` or empty (the row is in neither
side). The split metadata file then carries everything else about the splits (comment, seed, horizon, gap, row
budget) and names the table and its split columns, so it stays small and readable::

    rows.parquet        split_r0_f0   split_r0_f1   split_r0_f2
    (row 0)             train         test          train
    (row 1)             test          train         (empty)

    roles = pd.read_parquet(folder / "rows.parquet")
    test_positions = np.flatnonzero(roles["split_r0_f0"] == "test")

A side of a split is a set of rows, kept in row order. Splits a row table cannot hold exactly (a side out of row
order, a row repeated or out of range, a row on both sides) stay inline in the split metadata file, so every
container loads back to the splits it was saved with, and its checksum (over the splits, not the files) does not
depend on where they are stored.
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any

import numpy as np
import pandas as pd

if TYPE_CHECKING:
    from pathlib import Path

ROWS_FILE = "rows.parquet"
"""The row table's file name in a container folder."""

SPLITS_TABLE_TYPE = "predictive-ml-splits-table-v1"
"""The type of the split metadata file (``experiment_metadata.<type>.json``) whose splits are in the row table. A
Data Foundry that predates the row table refuses the file as written by a newer version, instead of misreading it."""

SPLIT_ROLES = ("train", "test")
"""The values of a split column; a row in neither side is empty."""

_SPLIT_COLUMN = re.compile(r"split_r(\d+)_f(\d+)")

Splits = dict[int, dict[int, tuple[list[int], list[int]]]]


def split_column(repeat: int, fold: int) -> str:
    """The row table's column of one outer split: ``split_r<repeat>_f<fold>``."""
    return f"split_r{repeat}_f{fold}"


def splits_to_row_table(splits: Splits, n_rows: int) -> pd.DataFrame | None:
    """The split columns of the row table of a frame of ``n_rows`` rows, or None when the table cannot hold
    ``splits`` exactly (a side out of row order, a row repeated or out of range, a row on both sides of a split).
    """
    columns: dict[str, pd.Categorical] = {}
    for repeat, folds in splits.items():
        for fold, sides in folds.items():
            codes = np.full(n_rows, -1, dtype=np.int8)
            for code, side in enumerate(sides):
                positions = np.asarray(side, dtype=np.int64)
                if len(positions) and (np.any(np.diff(positions) <= 0) or positions[0] < 0 or positions[-1] >= n_rows):
                    return None
                if np.any(codes[positions] != -1):
                    return None
                codes[positions] = code
            columns[split_column(repeat, fold)] = pd.Categorical.from_codes(codes, categories=list(SPLIT_ROLES))
    return pd.DataFrame(columns)


def splits_from_row_table(table: pd.DataFrame, columns: list[str]) -> Splits:
    """The outer splits stored in the row table's ``columns``, each side in row order."""
    splits: Splits = {}
    for column in columns:
        match = _SPLIT_COLUMN.fullmatch(column)
        if match is None or column not in table:
            msg = f"{ROWS_FILE}: no split column {column!r} (expected `split_r<repeat>_f<fold>`)."
            raise ValueError(msg)
        values = table[column]
        unknown = set(values.dropna().unique()) - set(SPLIT_ROLES)
        if unknown:
            msg = f"{ROWS_FILE}: column {column!r} holds {sorted(map(str, unknown))}; a split row is train, test or "
            msg += "empty."
            raise ValueError(msg)
        repeat, fold = int(match.group(1)), int(match.group(2))
        train = np.flatnonzero(values.eq("train").to_numpy(dtype=bool)).tolist()
        test = np.flatnonzero(values.eq("test").to_numpy(dtype=bool)).tolist()
        splits.setdefault(repeat, {})[fold] = (train, test)
    return splits


def table_metadata(dumped: dict[str, Any], table: pd.DataFrame) -> dict[str, Any]:
    """The split metadata file of a container whose splits are in the row table.

    That is ``dumped`` (the inline form) without the splits, naming the table and its split columns instead.
    """
    out = {k: v for k, v in dumped.items() if k not in ("splits", "type_adapter_id")}
    return {**out, "splits_file": ROWS_FILE, "split_columns": list(table.columns), "type_adapter_id": SPLITS_TABLE_TYPE}


def inline_metadata(meta_data: dict[str, Any], folder: Path, inline_type: str) -> dict[str, Any]:
    """The inline form of a split metadata file whose splits are in the row table, read from ``folder``."""
    meta_data = dict(meta_data)
    file_name = meta_data.pop("splits_file", ROWS_FILE)
    columns = meta_data.pop("split_columns")
    if not (folder / file_name).is_file():
        msg = f"{folder}: the split metadata names {file_name}, which is missing (an interrupted download?)."
        raise ValueError(msg)
    table = pd.read_parquet(folder / file_name, columns=columns)
    meta_data["splits"] = splits_from_row_table(table, columns)
    meta_data["type_adapter_id"] = inline_type
    return meta_data


def row_table_length(folder: Path) -> int | None:
    """The number of rows of the row table in ``folder``, or None without one."""
    path = folder / ROWS_FILE
    if not path.is_file():
        return None
    import pyarrow.parquet as pq  # noqa: PLC0415 - pandas' parquet engine, needed only here

    return pq.read_metadata(path).num_rows
