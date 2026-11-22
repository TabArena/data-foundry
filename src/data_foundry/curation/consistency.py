"""The rules that tie a curation record to its definition (SPLIT-32, SPLIT-34).

A record describes its source by collection facts and one data collection type; a definition says why its split fits
the use case (its time basis, :mod:`data_foundry.time_basis`). A few combinations contradict each other whatever the
use case. The rules live here, so the tests, ``dataset check`` and the review page read the same ones:

* :func:`collection_type_problems`: the record's type against SPLIT-34 and its own facts;
* :func:`time_basis_problems`: the definition's time basis and regime against the record's facts;
* :func:`record_problems`: both, for a record and its loaded definition class;
* :func:`all_problems`: every definition record of the repository.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from data_foundry.schema import FORCED_TIME_TAGS, TIME_BASIS_TAGS

if TYPE_CHECKING:
    from data_foundry.curation.record import CurationRecord

COLLECTION_TYPES = (
    "Expanding Science Catalogue",
    "Experimental Results",
    "Clinical Study",
    "Survey",
    "Database Snapshot",
    "Dated Event Log",
    "Panel Data",
)
"""How a source collected its rows, one per record tag (SPLIT-34); the split decision tree starts from it (SPLIT-36)."""

STRICT_COLLECTION_TYPES = False
"""Whether every definition record must name a collection type. False while the records are typed in several
changes (a record with neither a type nor a collection fact is left out); the change that completes the typing sets it
True."""

FACT_PREFIXES = ("Samples:", "Time:", "Target:", "Entities:", "Features:")
"""The prefixes of the collection facts (SPLIT-32)."""

DATED = frozenset({"Time: Dated"})
OCCASION = DATED | {"Time: Inferred", "Time: Within Entity"}


def collection_type_problems(tags: set[str]) -> list[str]:
    """The ways a record's collection type disagrees with SPLIT-34 or with its collection facts."""
    types = tags & set(COLLECTION_TYPES)
    if len(types) != 1:
        return [f"{len(types)} collection types, one expected"]
    (kind,) = types
    found = []
    dated_rows = "Samples: Over Time" in tags and bool(tags & DATED)
    if kind == "Dated Event Log" and not dated_rows:
        found.append("a dated event log needs samples over time with a date its rows record")
    if kind in ("Database Snapshot", "Clinical Study") and dated_rows:
        found.append(f"a {kind.lower()} whose rows record a date is a dated event log")
    if kind == "Panel Data" and not tags & OCCASION:
        found.append("panel data needs a recorded occasion: a date, an inferred order or an order within the unit")
    return found


def time_basis_problems(facts: set[str], basis: set[str], regime: str) -> list[str]:
    """The ways a definition's time basis (``basis``, its tags) and regime (``iid``, ``grouped`` or ``temporal``)
    contradict its record's collection facts.
    """
    found = []
    forced = bool(basis & set(FORCED_TIME_TAGS))
    if "Samples: One Moment" in facts and regime == "temporal":
        found.append("one moment has no time to split on")
    if "Samples: No Time Dimension" in facts and (forced or regime == "temporal"):
        found.append("no time dimension, yet forced from temporal or split by time")
    if "StationaryRelation" in basis and "Time: Lost" in facts and not facts & {"Time: Dated", "Time: Inferred"}:
        found.append("StationaryRelation is measured on dates, and the time is lost")
    if "AssumedStationaryRelation" in basis and facts & {"Time: Dated", "Time: Inferred"}:
        found.append("AssumedStationaryRelation where the time can be measured: measure it instead")
    if "AssumedStationaryRelation" in basis and not facts & {"Samples: Over Time", "Samples: One Moment"}:
        # SPLIT-32: only where the forced tag would stand: samples over time with the time lost, or one moment that
        # holds a single period
        found.append("AssumedStationaryRelation replaces a forced tag, which needs samples over time or one moment")
    return found


def is_typed(tags: set[str]) -> bool:
    """Whether a record carries a collection type or a collection fact."""
    return bool(tags & set(COLLECTION_TYPES)) or any(t.startswith(FACT_PREFIXES) for t in tags)


def definition_basis(cls: type) -> tuple[set[str], str]:
    """A loaded definition's time-basis tags (as its container carries them) and its regime: ``iid``, ``grouped`` or
    ``temporal``.
    """
    tags = set(cls.dataset_metadata.data_tags)
    regime = "temporal" if cls.temporal is not None else "grouped" if cls.grouping is not None else "iid"
    return tags & {*TIME_BASIS_TAGS, *FORCED_TIME_TAGS}, regime


def record_problems(tags: set[str], cls: type | None, *, strict: bool | None = None) -> list[str]:
    """The contradictions between a record (its ``tags``) and its definition class: the collection type (left out for a
    record that is not typed yet, unless ``strict``; default :data:`STRICT_COLLECTION_TYPES`) and the time basis.
    """
    strict = STRICT_COLLECTION_TYPES if strict is None else strict
    found = collection_type_problems(tags) if strict or is_typed(tags) else []
    if cls is not None:
        found += time_basis_problems(tags, *definition_basis(cls))
    return found


def all_problems(records: list[CurationRecord], repo: Path) -> dict[str, list[str]]:
    """Every definition record's contradictions, by unique name: each record with a ``v2_path`` against the definition
    it names (loaded through the registry, so inherited and computed tags count).
    """
    from data_foundry.v2.registry import load_definition  # noqa: PLC0415 - the curation package imports v2 lazily

    out = {}
    for record in records:
        path = repo / record.v2_path if record.v2_path else None
        if path is None or not path.exists():
            continue
        hits = record_problems(set(record.tags or []), load_definition(path))
        if hits:
            out[record.unique_name] = hits
    return out
