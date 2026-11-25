"""The time basis a definition names agrees with the collection facts of its record (SPLIT-8, SPLIT-32).

The record's facts describe the source; the definition's time basis says why its split fits the use case. A few
combinations contradict each other whatever the use case (the rules: ``data_foundry.curation.consistency``), and this
test reads every record against its loaded definition so that a contradiction shows up when it is written. A known contradiction is listed in
``PENDING`` with where it is decided or why it stands; an entry that no longer contradicts must leave the list.
"""

from __future__ import annotations

import pytest
from data_foundry.curation._paths import records_dir, resolve_curation_root
from data_foundry.curation.consistency import definition_basis, time_basis_problems
from data_foundry.curation.store import load_all
from data_foundry.v2.registry import load_definition

REPO = resolve_curation_root().parent

PENDING = {}
"""Records whose contradiction is known: an open review item, or a written exception the curator decided."""


@pytest.fixture(scope="module")
def found() -> dict[str, list[str]]:
    """Every record's contradictions, by unique name."""
    out = {}
    for record in load_all(records_dir()):
        if not record.v2_path or not (REPO / record.v2_path).exists():
            continue
        basis, regime = definition_basis(load_definition(REPO / record.v2_path))
        hits = time_basis_problems(set(record.tags or []), basis, regime)
        if hits:
            out[record.unique_name] = hits
    return out


def test_time_basis_agrees_with_the_collection_facts(found: dict[str, list[str]]) -> None:
    """No record contradicts its definition's time basis, apart from the pending ones."""
    new = {name: hits for name, hits in found.items() if name not in PENDING}
    assert not new, "\n".join(f"{name}: {'; '.join(hits)}" for name, hits in sorted(new.items()))


def test_pending_contradictions_still_hold(found: dict[str, list[str]]) -> None:
    """A pending entry whose contradiction is gone leaves the list."""
    resolved = sorted(set(PENDING) - set(found))
    assert not resolved, f"no longer contradictory, drop from PENDING: {resolved}"


@pytest.mark.parametrize(
    ("facts", "basis", "regime", "expected"),
    [
        ({"Samples: One Moment", "Target: Fixed Delay"}, {"ForcedIIDFromTemporal"}, "iid", 0),
        ({"Samples: One Moment"}, {"ForcedIIDFromTemporal"}, "iid", 0),
        ({"Samples: One Moment"}, set(), "temporal", 1),
        ({"Samples: No Time Dimension"}, {"ForcedIIDFromTemporal"}, "iid", 1),
        ({"Samples: Over Time", "Time: Lost", "Target: Fixed Delay"}, {"StationaryRelation"}, "iid", 1),
        ({"Samples: Over Time", "Time: Dated"}, {"StationaryRelation"}, "iid", 0),
        ({"Samples: Over Time", "Time: Lost"}, {"AssumedStationaryRelation"}, "iid", 0),
        ({"Samples: Over Time", "Time: Lost", "Time: Within Entity"}, {"AssumedStationaryRelation"}, "grouped", 0),
        ({"Samples: Over Time", "Time: Dated"}, {"AssumedStationaryRelation"}, "iid", 1),
        ({"Samples: Over Time", "Time: Inferred"}, {"AssumedStationaryRelation"}, "iid", 1),
        ({"Samples: No Time Dimension"}, {"AssumedStationaryRelation"}, "iid", 1),
        ({"Samples: One Moment", "Target: Fixed Delay"}, {"AssumedStationaryRelation"}, "iid", 0),
    ],
)
def test_contradictions(facts: set[str], basis: set[str], regime: str, expected: int) -> None:
    """Each rule fires on its contradiction and not on the combination the rules allow."""
    assert len(time_basis_problems(facts, basis, regime)) == expected
