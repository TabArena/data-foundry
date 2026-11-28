"""The rules of a split's time basis (SPLIT-8, SPLIT-32, SPLIT-35): why a split that is not temporal is not.

A definition declares it as ``time_basis = TimeBasis(tag, reason, ...)``, and ``group_basis = GroupBasis(reason)``
for a group the use case holds out but the data cannot key (both in :mod:`data_foundry.schema`). The build adds the
tags to ``data_tags`` and stores both declarations in the dataset metadata (``DatasetMetadataV2.time_basis`` and
``.group_basis``). One function (:func:`problems`) checks a definition and a built container alike; :func:`line` is
the sentence the README shows.
"""

from __future__ import annotations

import datetime
import re

from data_foundry.schema import (
    FORCED_TIME_TAGS,
    GROUP_BASIS_TAGS,
    TIME_BASIS_TAGS,
    GroupBasis,
    TimeBasis,
)

__all__ = ["GroupBasis", "TimeBasis"]

BASIS_TAGS = (*TIME_BASIS_TAGS, *FORCED_TIME_TAGS)
"""Every tag a :class:`TimeBasis` may carry: a use-case prototype or a forced tag; a split has one at most."""

HUMAN_SET_TIME_TAGS = ("StationaryRelation", "AssumedStationaryRelation")
"""Prototypes only a person sets (SPLIT-32): an AI may offer one with the facts for and against (for
`StationaryRelation`, the stationary-relation test's reading), and recommend it, but writes it only when a person asks.
Their :class:`TimeBasis` names the person (``set_by``), the date (``on``) and a reason of :data:`MIN_REASON_WORDS`
words at least (for `StationaryRelation`, the measurement)."""

MIN_REASON_WORDS = 8
"""The shortest reason a human-set time basis takes, in words."""

UNGROUPED_TAGS = ("ForcedIIDFromTemporal", "ForcedIIDFromGrouped")
"""Tags that mark an IID split: no ``grouping`` and no ``temporal``."""

GROUPED_TAGS = ("UnseenGroup", "ForcedGroupedFromTemporal")
"""Tags that hold out whole groups: they need a ``grouping``."""

Problem = tuple[str, str, str]
"""A finding of :func:`problems`: ``(slug, severity, message)``."""

_NOT_A_PERSON = re.compile(r"\b(?:ai|claude|agent|model|llm|bot|assistant)\b", re.IGNORECASE)


def person_problem(who: str | None) -> str | None:
    """Why ``who`` cannot be the person who set a time basis, or None: a name, never an AI or a tool."""
    who = (who or "").strip()
    if not who:
        return "no person is named"
    if _NOT_A_PERSON.search(who) or not who[:1].isupper():
        return f"`{who}` is not a person; only a person sets it"
    return None


def date_problem(on: str | None) -> str | None:
    """Why ``on`` is not a date of the form YYYY-MM-DD, or None."""
    try:
        datetime.date.fromisoformat((on or "").strip())
    except ValueError:
        return f"`{on}` is not a date (YYYY-MM-DD)"
    return None


def _attribution_problems(set_by: str | None, on: str | None) -> list[str]:
    """What is wrong with the person and the date a basis names (both or neither)."""
    found = []
    if (set_by is None) != (on is None):
        found.append("`set_by` and `on` go together: the person and the date they set it")
    if set_by is not None and (problem := person_problem(set_by)):
        found.append(problem)
    if on is not None and (problem := date_problem(on)):
        found.append(problem)
    return found


def declaration_problems(basis: TimeBasis | GroupBasis) -> list[str]:
    """What is wrong with a time basis or a group basis itself, before the split is looked at."""
    found = [] if " ".join((basis.reason or "").split()) else ["the reason is empty"]
    if isinstance(basis, GroupBasis):
        return found + _attribution_problems(basis.set_by, basis.on)
    if basis.tag not in BASIS_TAGS:
        found.insert(0, f"`{basis.tag}` is no time basis; one of {list(BASIS_TAGS)}")
    found += _attribution_problems(basis.set_by, basis.on)
    if basis.tag in HUMAN_SET_TIME_TAGS:
        if basis.set_by is None:
            found.append(f"only a person sets `{basis.tag}`: give `set_by` and `on` (SPLIT-32)")
        if len(basis.reason.split()) < MIN_REASON_WORDS:
            found.append(f"the reason is shorter than {MIN_REASON_WORDS} words")
    return found


def line(basis: TimeBasis | GroupBasis) -> str:
    """The sentence a README shows for a basis: ``Time basis: <tag> (<person>, <date>; <note>): <reason>``, or
    ``Group basis: <tag> (<person>, <date>): <reason>``.
    """
    reason = " ".join(basis.reason.split())
    if isinstance(basis, GroupBasis):
        attribution = f" ({basis.set_by}, {basis.on})" if basis.set_by or basis.on else ""
        return f"Group basis: {basis.tag}{attribution}: {reason}"
    parts = [f"{basis.set_by}, {basis.on}"] if basis.set_by or basis.on else []
    parts += [" ".join(basis.note.split())] if basis.note else []
    attribution = f" ({'; '.join(parts)})" if parts else ""
    return f"Time basis: {basis.tag}{attribution}: {reason}"


def tags_of(time_basis: TimeBasis | None, group_basis: GroupBasis | None) -> list[str]:
    """The ``data_tags`` the two declarations add."""
    return [basis.tag for basis in (time_basis, group_basis) if isinstance(basis, (TimeBasis, GroupBasis))]


def problems(
    tags: list[str],
    time_basis: TimeBasis | None,
    group_basis: GroupBasis | None,
    *,
    temporal: bool,
    grouped: bool,
) -> list[Problem]:
    """What is wrong with a split's time basis: for a definition once built, and for a built container alike.

    Args:
        tags: The ``data_tags``.
        time_basis: The dataset metadata's ``time_basis``.
        group_basis: The dataset metadata's ``group_basis``.
        temporal: Whether the split is temporal.
        grouped: Whether the split holds out groups (a ``grouping``).
    """
    basis = [t for t in dict.fromkeys(tags) if t in BASIS_TAGS]
    group = [t for t in dict.fromkeys(tags) if t in GROUP_BASIS_TAGS]
    found = _split_problems(basis, group, temporal=temporal, grouped=grouped)
    found += _field_problems(basis, group, time_basis, group_basis)
    if not temporal and not basis and time_basis is None:
        message = "The split is not temporal and the definition does not say why."
        found.append(("meta_time_basis_missing", "info", message))
    return found


def _split_problems(basis: list[str], group: list[str], *, temporal: bool, grouped: bool) -> list[Problem]:
    """The tags against each other and against the split: one basis, no prototype on a temporal split, IID or grouped
    as the tag says.
    """
    found = []
    if len(basis) > 1:
        found.append(("meta_time_basis_several", "error", f"`data_tags` {basis}: a split has one time basis."))
    prototypes = [t for t in basis if t in TIME_BASIS_TAGS]
    if temporal and prototypes:
        message = f"`data_tags` carry {prototypes}, which say why a split is not temporal, but this split is temporal."
        found.append(("meta_time_basis_on_temporal", "error", message))
    for tag in [*basis, *group]:
        if tag in UNGROUPED_TAGS and (temporal or grouped):
            found.append(("meta_time_basis_regime", "error", f"`{tag}` marks an IID split; this one is not IID."))
        if tag in GROUPED_TAGS and not grouped:
            found.append(("meta_time_basis_regime", "error", f"`{tag}` holds out whole groups; the split has none."))
    return found


def _field_problems(
    basis: list[str], group: list[str], time_basis: TimeBasis | None, group_basis: GroupBasis | None
) -> list[Problem]:
    """The stored declarations against the tags: the tag the time basis names, the person of a human-set tag, and a
    group basis for ``ForcedIIDFromGrouped``.
    """
    found = []
    tag = time_basis.tag if time_basis is not None else None
    if tag is not None and tag not in basis:
        message = f"The time basis names `{tag}`, but `data_tags` carry {basis or 'no time basis'}."
        found.append(("meta_time_basis_mismatch", "error", message))
    for listed in basis:
        if time_basis is None:
            found.append(("meta_time_basis_field_missing", "info", f"`{listed}` comes without its time basis."))
        elif listed in HUMAN_SET_TIME_TAGS and listed == tag:
            for problem in [*_attribution_problems(time_basis.set_by, time_basis.on), *_human_set_problems(time_basis)]:
                found.append(("meta_time_basis_unattributed", "error", f"`{listed}`: {problem}."))
    if group and group_basis is None:
        message = "`ForcedIIDFromGrouped` needs its group basis (SPLIT-35)."
        found.append(("meta_group_basis_missing", "error", message))
    return found


def _human_set_problems(time_basis: TimeBasis) -> list[str]:
    """Why a human-set time basis does not name a person and a reason long enough, beyond its attribution's form."""
    if time_basis.set_by is None:
        return ["only a person sets it: name `set_by` and `on` (SPLIT-32)"]
    if len(time_basis.reason.split()) < MIN_REASON_WORDS:
        return [f"the reason is missing or shorter than {MIN_REASON_WORDS} words"]
    return []
