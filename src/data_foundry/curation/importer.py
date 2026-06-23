"""One-time migration: legacy curation Google Sheet (CSV export) -> records.

The importer is deliberately *lossless and lenient*: messy or unmapped dropdown
values are preserved verbatim and flagged via :attr:`CurationRecord.needs_review`
rather than dropped or coerced. Re-running it is idempotent for a given sheet.

Run via the CLI::

    python -m data_foundry.curation.cli import-sheet "curation/TabArena-v0.2 - Main.csv"
"""

from __future__ import annotations

import csv
import re
from dataclasses import dataclass, field
from pathlib import Path

from data_foundry.curation.record import CurationRecord, load_vocabularies
from data_foundry.curation.store import save_record

# Single-value sheet columns -> record field.
SINGLE_MAP: dict[str, str] = {
    "Data Foundry": "data_foundry_status",
    "Suggestion": "suggestion",
    "Original Source (Website)": "original_source",
    "Year": "year",
    "Context Domain": "domain",
    "Problem Type": "problem_type",
    "Original Data State": "original_data_state",
}
# Multi-value (comma-combined) sheet columns -> record field.
MULTI_MAP: dict[str, str] = {
    "Checked by": "checked_by",
    "Decision Markers": "decision_markers",
    "New Tag": "tags",
    "Source (Benchmark / Collection)": "collections",
    "Required split": "required_split",
}
NAME_COL = "Name"
LINKS_COL = "Source (and Link to download)"
COMMENTS_COL = "Free Comments"
REFERENCE_COL = "Reference"

_SNAKE_HINT_RE = re.compile(r"\(([a-z0-9][a-z0-9_]*)\)")


def paren_aware_split(value: str) -> list[str]:
    """Split a multi-value cell on top-level commas, ignoring commas in ``(...)``.

    ``"Random (IID), Grouped (NON-IID)"`` -> ``["Random (IID)", "Grouped (NON-IID)"]``.
    """
    parts, depth, cur = [], 0, ""
    for ch in value:
        if ch == "(":
            depth += 1
            cur += ch
        elif ch == ")":
            depth = max(0, depth - 1)
            cur += ch
        elif ch == "," and depth == 0:
            parts.append(cur)
            cur = ""
        else:
            cur += ch
    parts.append(cur)
    return [p.strip() for p in parts if p.strip()]


def to_snake(text: str) -> str:
    """Convert arbitrary text to a snake_case identifier."""
    return re.sub(r"_+", "_", re.sub(r"[^0-9a-z]+", "_", text.strip().lower())).strip("_")


def parse_name(raw: str) -> tuple[str, str | None]:
    r"""Split the ``Name`` cell into ``(display_name, unique_name_hint)``.

    Curators wrote the snake_case id as a trailing ``(snake_hint)`` parenthetical,
    e.g. ``"PhiUSIIL Phishing URL (Website)\\n(phiusiil_phishing)"``. The hint (if
    any) is extracted; the display name is the remainder with whitespace collapsed.
    """
    raw = raw.strip()
    hints = _SNAKE_HINT_RE.findall(raw)
    hint = hints[-1] if hints else None
    display = raw
    if hint:
        display = display.replace(f"({hint})", "")
    display = " ".join(display.split()).strip()
    return display, hint


def split_links(value: str) -> list[str]:
    """One link / DOI per non-empty line of the source cell."""
    return [line.strip() for line in value.splitlines() if line.strip()]


@dataclass
class ImportReport:
    """Summary of an import run, for the post-migration checkpoint."""

    n_rows: int = 0
    n_written: int = 0
    collisions: list[str] = field(default_factory=list)
    needs_review_fields: dict[str, int] = field(default_factory=dict)
    n_needs_review: int = 0
    status_counts: dict[str, int] = field(default_factory=dict)

    def summary(self) -> str:
        """Render a short human-readable summary of the import run."""
        lines = [
            f"Imported {self.n_written}/{self.n_rows} rows.",
            f"Records needing review (unmapped dropdown values): {self.n_needs_review}.",
        ]
        if self.needs_review_fields:
            top = sorted(self.needs_review_fields.items(), key=lambda kv: -kv[1])
            lines.append("  per field: " + ", ".join(f"{k}={v}" for k, v in top))
        if self.status_counts:
            status = ", ".join(f"{k or '∅'}={v}" for k, v in self.status_counts.items())
            lines.append("  data_foundry_status: " + status)
        if self.collisions:
            shown = ", ".join(self.collisions[:8]) + (" …" if len(self.collisions) > 8 else "")
            lines.append(f"  unique_name collisions resolved ({len(self.collisions)}): {shown}")
        return "\n".join(lines)


def _build_record(
    row: dict[str, str], source_row: int, unique_name: str, vocab: dict[str, list[str]]
) -> CurationRecord:
    display, _ = parse_name(row.get(NAME_COL, ""))
    kwargs: dict[str, object] = {"unique_name": unique_name, "name": display or unique_name, "source_row": source_row}
    for col, fieldname in SINGLE_MAP.items():
        val = (row.get(col) or "").strip()
        kwargs[fieldname] = val or None
    for col, fieldname in MULTI_MAP.items():
        kwargs[fieldname] = paren_aware_split(row.get(col) or "")
    kwargs["source_links"] = split_links(row.get(LINKS_COL) or "")
    kwargs["comments"] = (row.get(COMMENTS_COL) or "").strip() or None
    kwargs["reference"] = (row.get(REFERENCE_COL) or "").strip() or None

    record = CurationRecord(**kwargs)
    record.needs_review = record.review_reasons(vocab)
    return record


def import_sheet(
    csv_path: str | Path,
    out_dir: str | Path | None = None,
    *,
    vocab: dict[str, list[str]] | None = None,
    write: bool = True,
) -> tuple[list[CurationRecord], ImportReport]:
    """Parse the sheet CSV into records (optionally writing them) + a report."""
    vocab = vocab if vocab is not None else load_vocabularies()
    with Path(csv_path).open(newline="") as f:
        rows = list(csv.DictReader(f))
    report = ImportReport()
    records: list[CurationRecord] = []
    seen: dict[str, int] = {}

    for i, row in enumerate(rows):
        if not any((v or "").strip() for v in row.values()):
            continue
        source_row = i + 2  # +1 for header, +1 for 1-based
        report.n_rows += 1

        _, hint = parse_name(row.get(NAME_COL, ""))
        base = hint or to_snake(parse_name(row.get(NAME_COL, ""))[0]) or f"row_{source_row}"
        unique_name = base
        if base in seen:
            seen[base] += 1
            unique_name = f"{base}_{seen[base]}"
            report.collisions.append(unique_name)
        else:
            seen[base] = 1

        record = _build_record(row, source_row, unique_name, vocab)
        records.append(record)

        status = record.data_foundry_status
        report.status_counts[status] = report.status_counts.get(status, 0) + 1
        if record.needs_review:
            report.n_needs_review += 1
            for f in record.needs_review:
                report.needs_review_fields[f] = report.needs_review_fields.get(f, 0) + 1
        if write:
            save_record(record, out_dir)
            report.n_written += 1

    return records, report
