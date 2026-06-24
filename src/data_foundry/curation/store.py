"""Persist curation records as one markdown file per dataset.

File layout (``<unique_name>.md``)::

    ---
    unique_name: phiusiil_phishing
    name: PhiUSIIL Phishing URL
    checked_by: [Andrej]
    data_foundry_status: [DF: Yes, BeyondArena]
    ...
    type_adapter_id: curation-record-v1
    ---

    # PhiUSIIL Phishing URL

    ## Comments

    Recent dataset for phishing website detection ...

    ## Reference

    @article{...}

Structured fields live in the YAML front-matter (empty / null fields are omitted
to keep diffs clean). The two free-text fields — ``comments`` and ``reference`` —
live in the markdown body under fixed ``## Comments`` / ``## Reference`` headers,
so they read and diff naturally. Round-trips through :func:`markdown_to_record`.
"""

from __future__ import annotations

import re
from pathlib import Path

import yaml

from data_foundry.curation._paths import records_dir
from data_foundry.curation.record import BODY_FIELDS, FIELDS, CurationRecord

BODY_SECTION_TITLES: dict[str, str] = {"comments": "Comments", "reference": "Reference"}

_FRONT_MATTER_RE = re.compile(r"\A---\n(.*?)\n---\n?(.*)\Z", re.DOTALL)


def record_to_markdown(record: CurationRecord) -> str:
    """Render a record as a YAML-front-matter + markdown-body string."""
    front: dict[str, object] = {"unique_name": record.unique_name, "name": record.name}
    for f in FIELDS:
        if f.name == "name" or f.kind == "body":
            continue
        value = getattr(record, f.name)
        if value is None or value in ([], ""):
            continue
        front[f.name] = value
    if record.source_row is not None:
        front["source_row"] = record.source_row
    if record.needs_review:
        front["needs_review"] = record.needs_review
    front["type_adapter_id"] = record.type_adapter_id

    front_text = yaml.safe_dump(front, sort_keys=False, allow_unicode=True, default_flow_style=False, width=4096)

    body_parts = [f"# {record.name}".rstrip()]
    for field in BODY_FIELDS:
        value = getattr(record, field)
        if value and value.strip():
            body_parts.append(f"## {BODY_SECTION_TITLES[field]}\n\n{value.strip()}")

    return f"---\n{front_text}---\n\n" + "\n\n".join(body_parts) + "\n"


def _parse_body_sections(body: str) -> dict[str, str | None]:
    """Extract ``comments`` / ``reference`` from the markdown body."""
    title_to_field = {v: k for k, v in BODY_SECTION_TITLES.items()}
    pattern = re.compile(rf"^##\s+({'|'.join(map(re.escape, title_to_field))})\s*$", re.MULTILINE)
    matches = list(pattern.finditer(body))
    out: dict[str, str | None] = dict.fromkeys(BODY_SECTION_TITLES)
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        content = body[start:end].strip()
        out[title_to_field[m.group(1)]] = content or None
    return out


def markdown_to_record(text: str) -> CurationRecord:
    """Parse a markdown file (front-matter + body) back into a record."""
    match = _FRONT_MATTER_RE.match(text)
    if match is None:
        raise ValueError("Curation record is missing the YAML front-matter (--- ... ---) block.")
    front = yaml.safe_load(match.group(1)) or {}
    front.update(_parse_body_sections(match.group(2)))
    return CurationRecord(**front)


def save_record(record: CurationRecord, directory: str | Path | None = None) -> Path:
    """Write ``record`` to ``<directory>/<unique_name>.md`` and return the path."""
    target_dir = Path(directory) if directory is not None else records_dir()
    target_dir.mkdir(parents=True, exist_ok=True)
    path = target_dir / f"{record.unique_name}.md"
    path.write_text(record_to_markdown(record))
    return path


def load_record(path: str | Path) -> CurationRecord:
    """Load a single record from its markdown file."""
    return markdown_to_record(Path(path).read_text())


def load_all(directory: str | Path | None = None) -> list[CurationRecord]:
    """Load every ``*.md`` record from ``directory`` (sorted by file name).

    Files whose name starts with ``_`` (e.g. ``_template.md``) are skipped: they are
    documentation/scaffolding, not real candidate datasets, mirroring the ``datasets/``
    tree convention where ``_template`` / ``_maintenance`` are not datasets.
    """
    target_dir = Path(directory) if directory is not None else records_dir()
    if not target_dir.exists():
        return []
    return [load_record(p) for p in sorted(target_dir.glob("*.md")) if not p.name.startswith("_")]


def load_index(directory: str | Path | None = None) -> dict[str, CurationRecord]:
    """Load every record keyed by ``unique_name``."""
    return {r.unique_name: r for r in load_all(directory)}


def record_to_dict(record: CurationRecord) -> dict[str, object]:
    """Flatten a record to a JSON-serializable dict (lists kept as lists)."""
    return {name: getattr(record, name) for name in record.__dataclass_fields__}


def record_from_dict(data: dict[str, object]) -> CurationRecord:
    """Construct (and validate) a record from a dict, ignoring unknown keys."""
    known = set(CurationRecord.__dataclass_fields__)
    return CurationRecord(**{k: v for k, v in data.items() if k in known})
