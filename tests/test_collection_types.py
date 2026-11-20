"""Every record of a definition names one data collection type, which agrees with its collection facts (SPLIT-34).

The type says how the source collected its rows; the collection facts (SPLIT-32) say when the samples arrive and where
time lives. Three of SPLIT-34's rules tie the two: panel data needs a recorded occasion, a dated event log needs a date
its raw rows record (an order rebuilt from the data does not count), and a database snapshot or a clinical study whose
rows record one is a dated event log. A known contradiction is listed in ``PENDING`` with where it is decided; an entry
that no longer contradicts leaves the list.
"""

from __future__ import annotations

import pytest
import yaml
from data_foundry.curation._paths import records_dir, resolve_curation_root
from data_foundry.curation.store import load_all
from data_foundry.schema import COLLECTION_TYPES

REPO = resolve_curation_root().parent
DATED = {"Time: Dated"}
OCCASION = DATED | {"Time: Inferred", "Time: Within Entity"}
FACT_PREFIXES = ("Samples:", "Time:", "Target:", "Entities:", "Features:")

PENDING: dict[str, str] = {
    "loan_default_prediction_imperial_college": (
        "a snapshot whose record says `Time: Dated`, though no date is given and the loans' order is read from the file"
        " (`Time: Inferred` under SPLIT-32); the fact is corrected on the PR that owns the collection facts (#50)"
    ),
}
"""Records whose contradiction is known, with where it is decided."""


def contradictions(tags: set[str]) -> list[str]:
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


@pytest.fixture(scope="module")
def found() -> dict[str, list[str]]:
    """Every typed definition record's contradictions, by unique name.

    A record that carries neither a collection type nor a collection fact is not typed yet and is left out; the
    definitions are typed in several pull requests, so such records exist until the last of them lands.
    """
    out = {}
    for name, tags in _typed_records().items():
        hits = contradictions(tags)
        if hits:
            out[name] = hits
    return out


def _typed_records() -> dict[str, set[str]]:
    """The tags of every definition record that carries a collection type or a collection fact, by unique name."""
    out = {}
    for record in load_all(records_dir()):
        if not record.v2_path or not (REPO / record.v2_path).exists():
            continue
        tags = set(record.tags or [])
        if tags & set(COLLECTION_TYPES) or any(t.startswith(FACT_PREFIXES) for t in tags):
            out[record.unique_name] = tags
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
    """A pending entry whose contradiction is gone leaves the list (an entry whose record is not typed yet waits)."""
    resolved = sorted((set(PENDING) & set(_typed_records())) - set(found))
    assert not resolved, f"no longer contradictory, drop from PENDING: {resolved}"


@pytest.mark.parametrize(
    ("tags", "expected"),
    [
        ({"Dated Event Log", "Samples: Over Time", "Time: Dated"}, 0),
        ({"Dated Event Log", "Samples: Over Time", "Time: Lost"}, 1),
        ({"Database Snapshot", "Samples: Over Time", "Time: Lost"}, 0),
        ({"Database Snapshot", "Samples: One Moment"}, 0),
        ({"Database Snapshot", "Samples: Over Time", "Time: Inferred"}, 0),
        ({"Dated Event Log", "Samples: Over Time", "Time: Inferred"}, 1),
        ({"Clinical Study", "Samples: Over Time", "Time: Inferred"}, 0),
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
