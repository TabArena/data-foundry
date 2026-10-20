"""One-way compile of the git-native records into a flat, browsable view.

Git stays the source of truth; this produces a derived snapshot for people who
just want to read/filter the backlog:

* :func:`to_dataframe` / :func:`export_csv` / :func:`export_parquet` — local files;
* :func:`push_to_gsheet` — overwrite a (read-only-for-others) Google Sheet tab,
  so non-coding stakeholders keep the familiar grid without being a write path.

Multi-value fields are joined with `` | `` so a single cell stays human-readable. Number fields (``priority``) and
``source_row`` stay integer columns (pandas ``Int64``), empty where a record has none.
"""

from __future__ import annotations

import os
from pathlib import Path

import pandas as pd

from data_foundry.curation.record import FIELDS, CurationRecord
from data_foundry.curation.store import load_all

MULTI_JOIN = " | "

# Column order for the flat view: id, then the sheet-style labels, then review flag.
_COLUMNS: list[tuple[str, str]] = (
    [("unique_name", "unique_name")]
    + [(f.name, f.label) for f in FIELDS]
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


def export_parquet(path: str | Path, directory: str | Path | None = None) -> Path:
    """Write the flat view to a Parquet file."""
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    to_dataframe(directory=directory).to_parquet(out, index=False)
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


def _authorize_gspread(service_account_file: str | Path | None):
    """Authorize a gspread client.

    Credential precedence:

    1. ``service_account_file`` argument or ``$GOOGLE_APPLICATION_CREDENTIALS`` — a JSON key;
    2. gspread's default key at ``~/.config/gspread/service_account.json``;
    3. Application Default Credentials — e.g. a GCE VM's attached service account
       (no key file needed; the token comes from the metadata server).
    """
    try:
        import gspread  # noqa: PLC0415 - optional dependency, imported only when publishing
    except ImportError as exc:  # pragma: no cover - optional dependency
        raise ImportError("push_to_gsheet requires gspread: pip install 'data-foundry[curation]'") from exc

    sa_file = service_account_file or os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if sa_file:
        return gspread.service_account(filename=sa_file)
    if (Path.home() / ".config" / "gspread" / "service_account.json").exists():
        return gspread.service_account()

    import google.auth  # noqa: PLC0415 - only needed for the ADC fallback

    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds, _ = google.auth.default(scopes=scopes)
    return gspread.authorize(creds)


def push_to_gsheet(
    spreadsheet: str,
    worksheet: str = "Main",
    *,
    service_account_file: str | Path | None = None,
    directory: str | Path | None = None,
) -> int:
    """Overwrite a Google Sheet worksheet with the current flat view.

    Authentication is resolved by :func:`_authorize_gspread` (key file, gspread
    default key, or Application Default Credentials). ``spreadsheet`` is a sheet
    key or URL, which must be shared (Editor) with the authenticating service
    account. Returns the number of data rows written. This is a *one-way* publish
    — share the Sheet read-only with everyone except that service account.
    """
    import gspread  # noqa: PLC0415 - optional dependency, imported only when publishing

    gc = _authorize_gspread(service_account_file)
    looks_like_url = "http" in spreadsheet
    key = gspread.utils.extract_id_from_url(spreadsheet) if looks_like_url else spreadsheet
    book = gc.open_by_key(key) if (looks_like_url or len(key) > 30) else gc.open(spreadsheet)

    df = to_dataframe(directory=directory).astype(object).fillna("")
    try:
        ws = book.worksheet(worksheet)
        ws.clear()
    except gspread.WorksheetNotFound:
        ws = book.add_worksheet(title=worksheet, rows=len(df) + 10, cols=len(df.columns) + 2)
    ws.update([df.columns.tolist(), *df.astype(str).to_numpy().tolist()])
    return len(df)
