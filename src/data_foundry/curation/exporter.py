"""One-way compile of the git-native records into a flat, browsable view.

Git stays the source of truth; this produces a derived snapshot for people who
just want to read/filter the backlog: :func:`to_dataframe`, written to a file by
:func:`export_csv` or :func:`export_xlsx`.

Multi-value fields are joined with `` | `` so a single cell stays human-readable. Number fields (``priority``) and
``source_row`` stay integer columns (pandas ``Int64``), empty where a record has none.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from data_foundry.curation.record import FIELDS, CurationRecord
from data_foundry.curation.store import load_all

MULTI_JOIN = " | "

FLAT_VIEW_SKIPS: frozenset[str] = frozenset({"review"})
"""Fields left out of the flat view: a record's review runs to hundreds of thousands of characters, and an Excel cell
holds 32,767. The record, the dashboard and the site show it."""

# Column order for the flat view: id, then the sheet-style labels, then review flag.
_COLUMNS: list[tuple[str, str]] = (
    [("unique_name", "unique_name")]
    + [(f.name, f.label) for f in FIELDS if f.name not in FLAT_VIEW_SKIPS]
    + [("needs_review", "Needs Review"), ("source_row", "Source Row")]
)
# Integer columns: kept as nullable integers, so an empty cell does not turn the column into text (or floats).
_INT_COLUMNS: frozenset[str] = frozenset({"source_row", *(f.name for f in FIELDS if f.kind == "number")})


def _cell(value: object, *, integer: bool = False) -> object:
    if isinstance(value, list):
        return MULTI_JOIN.join(str(v) for v in value)
    if value is None:
        return None if integer else ""
    return value


def to_dataframe(records: list[CurationRecord] | None = None, directory: str | Path | None = None) -> pd.DataFrame:
    """Flatten records into a single DataFrame with human-readable column labels."""
    records = records if records is not None else load_all(directory)
    rows = [{label: _cell(getattr(r, name), integer=name in _INT_COLUMNS) for name, label in _COLUMNS} for r in records]
    df = pd.DataFrame(rows, columns=[label for _, label in _COLUMNS])
    for name, label in _COLUMNS:
        if name in _INT_COLUMNS:
            df[label] = df[label].astype("Int64")
    return df


def export_csv(path: str | Path, directory: str | Path | None = None) -> Path:
    """Write the flat view to a CSV file."""
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    to_dataframe(directory=directory).to_csv(out, index=False)
    return out


def export_xlsx(path: str | Path, directory: str | Path | None = None) -> Path:
    """Write the flat view to an Excel ``.xlsx`` file (upload-ready for Google Sheets)."""
    from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE  # noqa: PLC0415 - only needed for xlsx

    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    df = to_dataframe(directory=directory)
    # Strip control characters openpyxl rejects (some free-text comments contain them); the integer columns stay.
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].map(lambda v: ILLEGAL_CHARACTERS_RE.sub("", v) if isinstance(v, str) else v)
    df.to_excel(out, index=False)
    return out
