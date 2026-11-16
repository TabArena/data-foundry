"""Every record of a definition names one data collection type, which agrees with its collection facts (SPLIT-35).

The type says how the source collected its rows; the collection facts (SPLIT-32) say when the samples arrive and where
time lives. Three of SPLIT-35's rules tie the two: panel data needs a recorded occasion, a dated event log needs a date
or an order per row, and a database snapshot or a clinical study whose rows keep one is a dated event log. A known
contradiction is listed in ``PENDING`` with where it is decided; an entry that no longer contradicts leaves the list.
"""

from __future__ import annotations

import pytest
import yaml
from data_foundry.curation._paths import records_dir, resolve_curation_root
from data_foundry.curation.store import load_all

REPO = resolve_curation_root().parent
COLLECTION_TYPES = (
    "Expanding Science Catalogue",
    "Experimental Results",
    "Clinical Study",
    "Survey",
    "Database Snapshot",
    "Dated Event Log",
    "Panel Data",
)
DATED = {"Time: Dated", "Time: Inferred"}
OCCASION = DATED | {"Time: Within Entity"}

PENDING: dict[str, str] = {}
"""Records whose contradiction is known, with where it is decided."""


def contradictions(tags: set[str]) -> list[str]:
    """The ways a record's collection type disagrees with SPLIT-35 or with its collection facts."""
    types = tags & set(COLLECTION_TYPES)
    if len(types) != 1:
        return [f"{len(types)} collection types, one expected"]
    (kind,) = types
    found = []
    dated_rows = "Samples: Over Time" in tags and bool(tags & DATED)
    if kind == "Dated Event Log" and not dated_rows:
        found.append("a dated event log needs samples over time with a date or an order per row")
    if kind in ("Database Snapshot", "Clinical Study") and dated_rows:
        found.append(f"a {kind.lower()} whose rows keep a date or an order is a dated event log")
    if kind == "Panel Data" and not tags & OCCASION:
        found.append("panel data needs a recorded occasion: a date, an inferred order or an order within the unit")
    return found


@pytest.fixture(scope="module")
def found() -> dict[str, list[str]]:
    """Every definition record's contradictions, by unique name."""
    out = {}
    for record in load_all(records_dir()):
        if not record.v2_path or not (REPO / record.v2_path).exists():
            continue
        hits = contradictions(set(record.tags or []))
        if hits:
            out[record.unique_name] = hits
    return out


def test_collection_types_are_in_the_vocabulary() -> None:
    """The seven types are tags the dashboard offers."""
    vocabulary = yaml.safe_load((REPO / "curation" / "vocabularies.yaml").read_text())
    assert set(COLLECTION_TYPES) <= set(vocabulary["tags"])


def test_collection_type_agrees_with_the_collection_facts(found: dict[str, list[str]]) -> None:
    """Every definition record has one collection type that its facts allow, apart from the pending ones."""
    new = {name: hits for name, hits in found.items() if name not in PENDING}
    assert not new, "\n".join(f"{name}: {'; '.join(hits)}" for name, hits in sorted(new.items()))


def test_pending_contradictions_still_hold(found: dict[str, list[str]]) -> None:
    """A pending entry whose contradiction is gone leaves the list."""
    resolved = sorted(set(PENDING) - set(found))
    assert not resolved, f"no longer contradictory, drop from PENDING: {resolved}"


@pytest.mark.parametrize(
    ("tags", "expected"),
    [
        ({"Dated Event Log", "Samples: Over Time", "Time: Dated"}, 0),
        ({"Dated Event Log", "Samples: Over Time", "Time: Lost"}, 1),
        ({"Database Snapshot", "Samples: Over Time", "Time: Lost"}, 0),
        ({"Database Snapshot", "Samples: One Moment"}, 0),
        ({"Database Snapshot", "Samples: Over Time", "Time: Inferred"}, 1),
        ({"Clinical Study", "Samples: Over Time", "Time: Dated"}, 1),
        ({"Experimental Results", "Samples: Over Time", "Time: Dated"}, 0),
        ({"Panel Data", "Samples: Over Time", "Time: Lost", "Time: Within Entity"}, 0),
        ({"Panel Data", "Samples: Over Time", "Time: Lost"}, 1),
        ({"Survey", "Samples: Over Time", "Time: Dated"}, 0),
        ({"Samples: Over Time", "Time: Dated"}, 1),
        ({"Survey", "Database Snapshot", "Samples: One Moment"}, 1),
    ],
)
def test_contradictions(tags: set[str], expected: int) -> None:
    """Each rule fires on its contradiction and not on the combination the rules allow."""
    assert len(contradictions(tags)) == expected
