"""Schema for a single dataset *curation record*.

A curation record is the upstream triage/decision unit for a candidate dataset:
who looked at it, whether it should go into Data Foundry, why (decision markers),
how it should be split, free-text discussion, and so on. It is intentionally
separate from :mod:`data_foundry.schema` (which describes datasets that have
*already* been promoted to curated containers).

One record is persisted as one ``<unique_name>.md`` file — structured fields in
YAML front-matter, free-text fields (``comments``, ``reference``) in the markdown
body. See :mod:`data_foundry.curation.store` for (de)serialization.

The set of allowed dropdown values lives in a git-tracked ``vocabularies.yaml``
(see :func:`load_vocabularies`); it is *advisory* — a record may carry a value
not in the vocabulary, in which case it is flagged via ``needs_review`` rather
than rejected. This keeps the dropdowns editable globally without code changes.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pydantic
import yaml

from data_foundry.curation._paths import vocabularies_path

MultilineStr = str


@dataclass(frozen=True)
class FieldSpec:
    """Tooling metadata for one curation field.

    Drives the importer (how to parse a sheet cell), the store (which fields go
    to the markdown body), and the dashboard (column type + dropdown source).
    """

    name: str
    """Attribute name on :class:`CurationRecord`."""
    label: str
    """Human label, matching the original spreadsheet column where applicable."""
    kind: str
    """One of ``"text"``, ``"select"``, ``"multiselect"``, ``"links"``, ``"body"``."""
    vocab: str | None = None
    """Vocabulary key for ``select``/``multiselect`` fields (defaults to ``name``)."""
    help: str = ""
    """Short human description, surfaced in the dashboard and docs."""

    @property
    def vocab_key(self) -> str | None:
        """Vocabulary key for dropdown-backed fields, else ``None``."""
        if self.kind in ("select", "multiselect"):
            return self.vocab or self.name
        return None

    @property
    def is_list(self) -> bool:
        """Whether the field stores a list of values."""
        return self.kind in ("multiselect", "links")


# The curation fields, in display / front-matter order. ``unique_name`` is the
# stable id (file stem) and is handled separately from this list.
FIELDS: tuple[FieldSpec, ...] = (
    FieldSpec(
        "name",
        "Source Name",
        "text",
        help="Names this dataset has been published under across its sources and collections.",
    ),
    FieldSpec("checked_by", "Checked by", "multiselect", help="People who reviewed the dataset."),
    FieldSpec(
        "data_foundry_status",
        "Data Foundry",
        "multiselect",
        help="Integration state (DF: …) and benchmark membership (TabArena (v0.1) / BeyondArena).",
    ),
    FieldSpec("suggestion", "Suggestion", "select", help="Whether we suggest including the dataset."),
    FieldSpec("decision_markers", "Decision Markers", "multiselect", help="Reasons / decision flags."),
    FieldSpec("tags", "Prio Tag", "multiselect", help="Tags to determine the priority of investigating the dataset."),
    FieldSpec("collections", "Source (Benchmark / Collection)", "multiselect", help="Source benchmarks/collections."),
    FieldSpec("original_source", "Original Source (Website)", "select", help="Where the data was first shared."),
    FieldSpec("year", "Year", "text", help="Publication / collection year."),
    FieldSpec("domain", "Context Domain", "select", help="Real-world application domain."),
    FieldSpec("required_split", "Required split", "multiselect", help="Evaluation split regime."),
    FieldSpec("problem_type", "Problem Type", "select", help="Predictive ML problem type."),
    FieldSpec("original_data_state", "Original Data State", "select", help="Shape of the raw data."),
    FieldSpec("source_links", "Source Links", "links", help="Download links / DOIs (one per line)."),
    FieldSpec("comments", "Free Comments", "body", help="Free-text curation discussion."),
    FieldSpec("reference", "Reference", "body", help="Academic reference / citation (often BibTeX)."),
)

FIELDS_BY_NAME: dict[str, FieldSpec] = {f.name: f for f in FIELDS}
BODY_FIELDS: tuple[str, ...] = tuple(f.name for f in FIELDS if f.kind == "body")
LIST_FIELDS: tuple[str, ...] = tuple(f.name for f in FIELDS if f.is_list)
VOCAB_FIELDS: dict[str, str] = {f.name: f.vocab_key for f in FIELDS if f.vocab_key}  # type: ignore[misc]

# Fields that must be filled in for a candidate to be considered triaged. Left
# empty, they flag the record for review (see CurationRecord.review_reasons).
REQUIRED_FIELDS: tuple[str, ...] = ("suggestion",)

# Curation-workflow marker values (kept here so tooling, tests and the AI-review
# pass all agree on the exact strings).
AI_REVIEWER: str = "AI (UNVERIFIED)"
"""``checked_by`` value meaning "an AI triaged this; a human still must verify it"."""
AI_FILLED_TAG: str = "AI-Filled (Verify)"
"""``tags`` value flagging records whose fields were populated by the AI-review pass."""
COLLECTION_TAGS: tuple[str, ...] = ("TabArena (v0.1)", "BeyondArena")
"""``data_foundry_status`` values denoting membership in one of *our* shipped collections."""
ACCEPTED_SUGGESTIONS: tuple[str, ...] = ("Yes", "Yes (Disagreement)")
"""``suggestion`` values that count as "accepted for inclusion".

A dataset shipped in a collection must carry one of these. ``"Yes (Disagreement)"`` means
*shipped on purpose, but with an unresolved disagreement to re-evaluate later* — it still counts
as accepted (so it is not a ``ship_conflict``), but surfaces under the dashboard's Disagreement
filter rather than as a settled ``"Yes"``.
"""


@pydantic.dataclasses.dataclass(config=pydantic.ConfigDict(extra="forbid"))
class CurationRecord:
    """One candidate dataset's curation/triage state.

    Structured fields persist to YAML front-matter; ``comments`` and ``reference``
    persist to the markdown body. Field semantics mirror the original curation
    spreadsheet columns (see :data:`FIELDS`).
    """

    unique_name: str
    """Stable identifier and file stem (snake_case)."""
    name: str
    """Human-readable dataset name."""

    checked_by: list[str] = pydantic.Field(default_factory=list)
    data_foundry_status: list[str] = pydantic.Field(default_factory=list)
    suggestion: str | None = None
    decision_markers: list[str] = pydantic.Field(default_factory=list)
    tags: list[str] = pydantic.Field(default_factory=list)
    collections: list[str] = pydantic.Field(default_factory=list)
    original_source: str | None = None
    year: str | None = None
    domain: str | None = None
    required_split: list[str] = pydantic.Field(default_factory=list)
    problem_type: str | None = None
    original_data_state: str | None = None
    source_links: list[str] = pydantic.Field(default_factory=list)

    comments: MultilineStr | None = None
    reference: MultilineStr | None = None

    source_row: int | None = None
    """1-based row in the original spreadsheet this record was imported from (provenance)."""
    needs_review: list[str] = pydantic.Field(default_factory=list)
    """Field names whose value is not (yet) in the vocabulary — surfaced for cleanup."""

    type_adapter_id: str = "curation-record-v1"
    """Identifier for the serialization format."""

    def unknown_vocab_values(self, vocab: dict[str, list[str]]) -> dict[str, list[str]]:
        """Return, per field, the values not present in ``vocab``.

        Empty dict means every dropdown value is recognized. Used to populate
        :attr:`needs_review` and by the validator/CLI.
        """
        out: dict[str, list[str]] = {}
        for field, key in VOCAB_FIELDS.items():
            allowed = set(vocab.get(key, []))
            value = getattr(self, field)
            present = value if isinstance(value, list) else ([value] if value else [])
            unknown = [v for v in present if v not in allowed]
            if unknown:
                out[field] = unknown
        return out

    def review_reasons(self, vocab: dict[str, list[str]]) -> list[str]:
        """Reasons a curator still needs to act on this record (-> :attr:`needs_review`).

        This is the single source of truth for the dashboard's **Review** queue
        (the ⚠ / 🤖 status markers and the *Review* pill all read it). It combines:

        * field names whose dropdown value is not in ``vocab`` (typos / stray values);
        * :data:`REQUIRED_FIELDS` still empty — e.g. an untriaged candidate with no
          ``suggestion`` yet (``"suggestion"``);
        * ``"ai_unverified"`` — the record was triaged by the AI pass
          (:data:`AI_REVIEWER` in ``checked_by``) but **no human has verified it**, so it
          stays in the queue until a curator signs off (removes the AI reviewer);
        * ``"ship_conflict"`` — a contradiction: the dataset is shipped in one of our
          collections (:data:`COLLECTION_TAGS`) yet its ``suggestion`` is set to something
          other than an accepted verdict (:data:`ACCEPTED_SUGGESTIONS`).

        Returned sorted for stable serialization.
        """
        reasons = set(self.unknown_vocab_values(vocab))
        for field in REQUIRED_FIELDS:
            if not getattr(self, field):
                reasons.add(field)
        if AI_REVIEWER in (self.checked_by or []):
            reasons.add("ai_unverified")
        shipped = any(t in (self.data_foundry_status or []) for t in COLLECTION_TAGS)
        if shipped and self.suggestion and self.suggestion not in ACCEPTED_SUGGESTIONS:
            reasons.add("ship_conflict")
        return sorted(reasons)

    def describe(self) -> str:
        """Return a compact, human-readable one-record summary."""

        def _one_line(value: str | None, limit: int = 80) -> str:
            if not value:
                return "None"
            first = value.strip().splitlines()[0] if value.strip() else ""
            return first if len(first) <= limit else first[: limit - 1] + "…"

        lines = [f"CurationRecord: {self.unique_name}"]
        for f in FIELDS:
            value = getattr(self, f.name)
            rendered = _one_line(value) if f.kind == "body" else (", ".join(value) if f.is_list else (value or "None"))
            lines.append(f"  {f.label + ':':<34} {rendered}")
        if self.needs_review:
            lines.append(f"  {'needs_review:':<34} {', '.join(self.needs_review)}")
        return "\n".join(lines)


def load_vocabularies(path: str | Path | None = None) -> dict[str, list[str]]:
    """Load the editable dropdown vocabularies.

    Args:
        path: Path to ``vocabularies.yaml``. Defaults to the resolved curation root.

    Returns:
        Mapping of field name -> list of allowed values. Returns an empty dict if
        the file does not exist (validation then treats every value as unknown).
    """
    p = Path(path) if path is not None else vocabularies_path()
    if not p.exists():
        return {}
    data = yaml.safe_load(p.read_text()) or {}
    return {k: list(v or []) for k, v in data.items()}


def save_vocabularies(vocab: dict[str, list[str]], path: str | Path | None = None) -> Path:
    """Persist dropdown vocabularies back to ``vocabularies.yaml`` (block-style lists)."""
    p = Path(path) if path is not None else vocabularies_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(yaml.safe_dump(vocab, sort_keys=False, allow_unicode=True, default_flow_style=False))
    return p
