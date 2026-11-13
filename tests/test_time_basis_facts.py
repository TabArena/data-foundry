"""The time basis a definition names agrees with the collection facts of its record (SPLIT-8, SPLIT-32).

The record's facts describe the source; the definition's time basis says why its split fits the use case. A few
combinations contradict each other whatever the use case, and this test reads every record against its definition so
that a contradiction shows up when it is written, not only on a review page. A known contradiction is listed in
``PENDING`` with where it is decided or why it stands; an entry that no longer contradicts must leave the list.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
from data_foundry.curation._paths import records_dir, resolve_curation_root
from data_foundry.curation.store import load_all
from data_foundry.schema import FORCED_TIME_TAGS, TIME_BASIS_TAGS

REPO = resolve_curation_root().parent
LATER_TARGETS = {"Target: Later", "Target: Varying Delay", "Target: Revised Later"}

PENDING = {
    "churn_telco_south_asia": (
        "one moment, target later, but no closed window: when the churn was observed is not stated (forced, 2026-10-21)"
    ),
}
"""Records whose contradiction is known: an open review item, or a written exception the curator decided."""


def _definition(path: Path) -> tuple[set[str], str]:
    """The time-basis tags of a definition file and its split regime, read from the source."""
    src = path.read_text()
    tags: set[str] = set()
    for m in re.finditer(r"^    data_tags = \(([^)]*)\)", src, re.M):
        tags |= set(re.findall(r'"([A-Za-z]+)"', m.group(1)))
    regime = (
        "temporal"
        if re.search(r"^    temporal = ", src, re.M)
        else "grouped"
        if "grouping = Grouping(" in src
        else "iid"
    )
    return tags & {*TIME_BASIS_TAGS, *FORCED_TIME_TAGS}, regime


def contradictions(facts: set[str], basis: set[str], regime: str) -> list[str]:
    """The ways a definition's time basis and split contradict its record's collection facts."""
    found = []
    forced = bool(basis & set(FORCED_TIME_TAGS))
    if "Samples: One Moment" in facts and forced and facts & LATER_TARGETS:
        found.append("one moment with a later target is a DelayedTarget, not forced")
    if "Samples: One Moment" in facts and regime == "temporal":
        found.append("one moment has no time to split on")
    if "Samples: No Time Dimension" in facts and (forced or regime == "temporal"):
        found.append("no time dimension, yet forced from temporal or split by time")
    if "StationaryRelation" in basis and "Time: Lost" in facts and not facts & {"Time: Dated", "Time: Inferred"}:
        found.append("StationaryRelation is measured on dates, and the time is lost")
    return found


@pytest.fixture(scope="module")
def found() -> dict[str, list[str]]:
    """Every record's contradictions, by unique name."""
    out = {}
    for record in load_all(records_dir()):
        if not record.v2_path or not (REPO / record.v2_path).exists():
            continue
        basis, regime = _definition(REPO / record.v2_path)
        hits = contradictions(set(record.tags or []), basis, regime)
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
        ({"Samples: One Moment", "Target: Later"}, {"ForcedIIDFromTemporal"}, "iid", 1),
        ({"Samples: One Moment"}, {"ForcedIIDFromTemporal"}, "iid", 0),
        ({"Samples: One Moment", "Target: Unknown"}, {"ForcedIIDFromTemporal"}, "iid", 0),
        ({"Samples: One Moment", "Target: Later"}, {"DelayedTarget"}, "iid", 0),
        ({"Samples: One Moment"}, set(), "temporal", 1),
        ({"Samples: No Time Dimension"}, {"ForcedIIDFromTemporal"}, "iid", 1),
        ({"Samples: Over Time", "Time: Lost", "Target: Later"}, {"StationaryRelation"}, "iid", 1),
        ({"Samples: Over Time", "Time: Dated"}, {"StationaryRelation"}, "iid", 0),
    ],
)
def test_contradictions(facts: set[str], basis: set[str], regime: str, expected: int) -> None:
    """Each rule fires on its contradiction and not on the combination the rules allow."""
    assert len(contradictions(facts, basis, regime)) == expected
