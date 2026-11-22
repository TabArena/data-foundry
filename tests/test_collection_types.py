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
from data_foundry.curation import consistency
from data_foundry.curation._paths import records_dir, resolve_curation_root
from data_foundry.curation.consistency import COLLECTION_TYPES, collection_type_problems, is_typed
from data_foundry.curation.store import load_all

REPO = resolve_curation_root().parent

PENDING: dict[str, str] = {
    "loan_default_prediction_imperial_college": (
        "a snapshot whose record says `Time: Dated`, though no date is given and the loans' order is read from the file"
        " (`Time: Inferred` under SPLIT-32); the fact is corrected with the record"
    ),
}
"""Records whose contradiction is known, with where it is decided."""


def _records() -> dict[str, set[str]]:
    """The tags of every definition record the check reads, by unique name: every one once
    ``consistency.STRICT_COLLECTION_TYPES`` is set, until then those with a collection type or a collection fact."""
    out = {}
    for record in load_all(records_dir()):
        if not record.v2_path or not (REPO / record.v2_path).exists():
            continue
        tags = set(record.tags or [])
        if consistency.STRICT_COLLECTION_TYPES or is_typed(tags):
            out[record.unique_name] = tags
    return out


@pytest.fixture(scope="module")
def found() -> dict[str, list[str]]:
    """Every read definition record's contradictions, by unique name."""
    out = {}
    for name, tags in _records().items():
        hits = collection_type_problems(tags)
        if hits:
            out[name] = hits
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
    resolved = sorted((set(PENDING) & set(_records())) - set(found))
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
    assert len(collection_type_problems(tags)) == expected
