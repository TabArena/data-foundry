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

    ## Comments

    Recent dataset for phishing website detection ...

    ## Review

    **Outcome:** added. ...

    ## Reference

    @article{...}

Structured fields live in the YAML front-matter (empty / null fields are omitted
to keep diffs clean) — ``name`` is the single source of truth for the dataset name.
The free-text fields live in the markdown body under fixed headers, so they read and diff naturally:
``## Comments`` (the curation discussion), ``## Review`` (the dataset's review, open and settled issues with every
turn, written by /add-dataset and /review-added-datasets) and ``## Reference``. An empty section is omitted.
Round-trips through :func:`markdown_to_record`. A section heading may appear only once, and the body holds nothing
but these sections: a heading line inside a section's text, or text before the first section, is an error on both
save and load, never silently moved or dropped. Files with CRLF line endings are read as well.
"""

from __future__ import annotations

import re
import tempfile
from pathlib import Path

import yaml

from data_foundry.curation._paths import records_dir
from data_foundry.curation.claims import warn_if_claimed
from data_foundry.curation.record import BODY_FIELDS, FIELDS, CurationRecord

BODY_SECTION_TITLES: dict[str, str] = {"comments": "Comments", "review": "Review", "reference": "Reference"}

_FRONT_MATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n)?(.*)\Z", re.DOTALL)
_SECTION_RE = re.compile(
    rf"^##[ \t]+({'|'.join(map(re.escape, BODY_SECTION_TITLES.values()))})[ \t]*\r?$", re.MULTILINE
)


class RecordFormatError(ValueError):
    """A curation record file (or a record about to be written) that does not fit the file layout."""


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

    # The dataset name lives only in the front-matter (`name:`); the body holds just the
    # free-text sections, so there is a single source of truth for the name.
    body_parts = []
    for field in BODY_FIELDS:
        value = getattr(record, field)
        if value and value.strip():
            if clash := _SECTION_RE.search(value):
                line = value.count("\n", 0, clash.start()) + 1
                raise RecordFormatError(
                    f"{record.unique_name}: the {field} text has a line {clash.group(0).strip()!r} (line {line} of "
                    "the field), which would start a new section of the record file; change that heading."
                )
            body_parts.append(f"## {BODY_SECTION_TITLES[field]}\n\n{value.strip()}")
    body = "\n\n".join(body_parts)

    return f"---\n{front_text}---\n" + (f"\n{body}\n" if body else "")


def _parse_body_sections(body: str, source: str = "record", line_offset: int = 0) -> dict[str, str | None]:
    """Extract ``comments`` / ``review`` / ``reference`` from the markdown body.

    Raises :class:`RecordFormatError`, naming ``source`` and the line in the file (``line_offset`` is the number of
    lines before ``body``), on a section heading that appears twice or on text before the first section.
    """
    title_to_field = {v: k for k, v in BODY_SECTION_TITLES.items()}
    matches = list(_SECTION_RE.finditer(body))

    def line_of(pos: int) -> int:
        return line_offset + body.count("\n", 0, pos) + 1

    head = body[: matches[0].start()] if matches else body
    if head.strip():
        pos = len(head) - len(head.lstrip())
        raise RecordFormatError(
            f"{source}: text before the first section (line {line_of(pos)}); the body holds only the sections "
            f"{', '.join('## ' + t for t in BODY_SECTION_TITLES.values())}. Move that text into one of them."
        )
    out: dict[str, str | None] = dict.fromkeys(BODY_SECTION_TITLES)
    seen: dict[str, int] = {}
    for i, m in enumerate(matches):
        title = m.group(1)
        if title in seen:
            raise RecordFormatError(
                f"{source}: the heading '## {title}' appears twice (lines {seen[title]} and {line_of(m.start())}); "
                "a section heading may appear only once. Rename or merge one of them."
            )
        seen[title] = line_of(m.start())
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        content = body[start:end].replace("\r\n", "\n").strip()
        out[title_to_field[title]] = content or None
    return out


def markdown_to_record(text: str, source: str = "record") -> CurationRecord:
    """Parse a markdown file (front-matter + body) back into a record; ``source`` names it in errors."""
    match = _FRONT_MATTER_RE.match(text)
    if match is None:
        raise RecordFormatError(f"{source}: missing the YAML front-matter (--- ... ---) block.")
    front = yaml.safe_load(match.group(1)) or {}
    front.update(_parse_body_sections(match.group(2), source, text.count("\n", 0, match.start(2))))
    return CurationRecord(**front)


def write_atomic(path: str | Path, text: str) -> None:
    """Write ``text`` to ``path`` through a temporary file in the same folder, so a reader never sees half a file."""
    path = Path(path)
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=path.parent, prefix=f".{path.name}.", suffix=".tmp", delete=False
    ) as tmp:
        tmp.write(text)
    tmp_path = Path(tmp.name)
    try:
        # NamedTemporaryFile creates the file as 0600; keep the mode of the file it replaces.
        tmp_path.chmod(path.stat().st_mode & 0o777 if path.exists() else 0o644)
        tmp_path.replace(path)  # atomic on one filesystem
    except BaseException:
        tmp_path.unlink(missing_ok=True)
        raise


def save_record(record: CurationRecord, directory: str | Path | None = None) -> Path:
    """Write ``record`` to ``<directory>/<unique_name>.md`` and return the path.

    Writing a record of the standard records directory while another curator holds its claim (the cached claims board,
    :mod:`data_foundry.curation.claims`) emits a :class:`~data_foundry.curation.claims.ClaimWarning`; the write still
    happens, since claims are advisory.
    """
    target_dir = Path(directory) if directory is not None else records_dir()
    if target_dir.resolve() == records_dir().resolve():
        warn_if_claimed(record.unique_name)
    target_dir.mkdir(parents=True, exist_ok=True)
    path = target_dir / f"{record.unique_name}.md"
    write_atomic(path, record_to_markdown(record))
    return path


def load_record(path: str | Path) -> CurationRecord:
    """Load a single record from its markdown file."""
    return markdown_to_record(Path(path).read_text(encoding="utf-8"), source=str(path))


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
