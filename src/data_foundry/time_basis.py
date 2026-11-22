"""The time basis of a split (SPLIT-8, SPLIT-32, SPLIT-35): why a split that is not temporal is not.

A definition declares it as ``time_basis = TimeBasis(tag, reason, ...)``, and ``group_basis = GroupBasis(reason)``
for a group the use case holds out but the data cannot key. The build adds the tags to ``data_tags`` and renders a
``- Time basis:`` (and a ``- Group basis:``) line into ``curation_comments``, so a container carries both without a
new field. One parser (:func:`parse`) reads the rendered lines back, and one function (:func:`problems`) checks a
definition, once rendered, and a built container alike.

The old way, a forced tag in ``data_tags`` and a free-text line in ``curation_comments``, is read while the
definitions move to :class:`TimeBasis` (:data:`ALLOW_UNSTRUCTURED`).
"""

from __future__ import annotations

import datetime
import re
from dataclasses import dataclass
from typing import ClassVar

from data_foundry.schema import FORCED_TIME_TAGS, GROUP_BASIS_TAGS, TIME_BASIS_TAGS

ALLOW_UNSTRUCTURED = True
"""Whether a definition may still name its time basis the old way: a forced tag in ``data_tags`` and a free-text
``Time basis:`` line in ``curation_comments``. True while the definitions move to :class:`TimeBasis`; the change that
completes the move sets it False, and the definition then refuses the old way. Until then an old-way definition's
lines are read as notes: their errors (:data:`OLD_WAY_TOLERATED`) do not stop it."""

OLD_WAY_TOLERATED = frozenset({"meta_time_basis_mismatch", "meta_time_basis_lines"})
"""Line errors an old-way definition is spared while :data:`ALLOW_UNSTRUCTURED` holds: its free text predates the
rendered form (a line that names a tag the definition does not list yet, two lines)."""

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
_BULLET = re.compile(
    r"^[ \t]*-[ \t]*(?P<kind>Time|Group) basis:[ \t]*(?P<body>.*?)(?=\n[ \t]*[-*][ \t]|\n[ \t]*\n|\Z)",
    re.S | re.M,
)
_HEAD = re.compile(r"(?P<head>[A-Za-z]+)[ \t]*(?:\((?P<inside>[^)]*)\))?[ \t]*:(?P<rest>.*)", re.S)
_RULE_ID = re.compile(r"^\s*SPLIT-\d+;\s*")


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


@dataclass(frozen=True)
class TimeBasis:
    """Why a definition's split is not temporal (SPLIT-32), or why a forward use case ships a forced split (SPLIT-8).

    Attributes:
        tag: A use-case prototype (``Timeless``, ``Retrospective``, ``StationaryRelation``,
            ``AssumedStationaryRelation``, ``UnseenGroup``) or a forced tag (``ForcedIIDFromTemporal``,
            ``ForcedGroupedFromTemporal``).
        reason: The fact behind it, ending with what the split cannot test; for a forced tag the reason (time lost,
            or too few periods) and what a dated release would change; for ``StationaryRelation`` the measurement.
        set_by: The person who set it. Required for the tags of :data:`HUMAN_SET_TIME_TAGS`.
        on: The date they set it, ``YYYY-MM-DD``. Required with ``set_by``.
    """

    tag: str
    reason: str
    set_by: str | None = None
    on: str | None = None

    def line(self) -> str:
        """The ``- Time basis:`` bullet the build renders into ``curation_comments``."""
        attribution = f" ({self.set_by}, {self.on})" if self.set_by or self.on else ""
        return f"- Time basis: {self.tag}{attribution}: {' '.join(self.reason.split())}"

    def problems(self) -> list[str]:
        """What is wrong with the declaration itself, before the split is looked at."""
        found = []
        if self.tag not in BASIS_TAGS:
            found.append(f"`{self.tag}` is no time basis; one of {list(BASIS_TAGS)}")
        if not " ".join((self.reason or "").split()):
            found.append("the reason is empty")
        if (self.set_by is None) != (self.on is None):
            found.append("`set_by` and `on` go together: the person and the date they set it")
        if self.set_by is not None and (problem := person_problem(self.set_by)):
            found.append(problem)
        if self.on is not None and (problem := date_problem(self.on)):
            found.append(problem)
        if self.tag in HUMAN_SET_TIME_TAGS:
            if self.set_by is None:
                found.append(f"only a person sets `{self.tag}`: give `set_by` and `on` (SPLIT-32)")
            if len(self.reason.split()) < MIN_REASON_WORDS:
                found.append(f"the reason is shorter than {MIN_REASON_WORDS} words")
        return found


@dataclass(frozen=True)
class GroupBasis:
    """Why a split is random although the use case holds out a group (SPLIT-35): ``ForcedIIDFromGrouped``.

    Attributes:
        reason: The group the use case holds out, why the data cannot key it, and the overlap the random split leaves.
    """

    reason: str
    tag: ClassVar[str] = "ForcedIIDFromGrouped"

    def line(self) -> str:
        """The ``- Group basis:`` bullet the build renders into ``curation_comments``."""
        return f"- Group basis: {' '.join(self.reason.split())}"

    def problems(self) -> list[str]:
        """What is wrong with the declaration itself."""
        return [] if " ".join((self.reason or "").split()) else ["the reason is empty"]


def render(comments: str | None, time_basis: TimeBasis | None, group_basis: GroupBasis | None) -> str | None:
    """``comments`` with the time basis and the group basis appended as bullets, as the build renders them."""
    rendered = [basis.line() for basis in _declared(time_basis, group_basis)]
    if not rendered:
        return comments
    return "\n".join([*([comments.rstrip()] if comments and comments.strip() else []), *rendered])


def tags_of(time_basis: TimeBasis | None, group_basis: GroupBasis | None) -> list[str]:
    """The ``data_tags`` the two declarations add."""
    return [basis.tag for basis in _declared(time_basis, group_basis)]


def _declared(time_basis: object, group_basis: object) -> list[TimeBasis | GroupBasis]:
    """The two declarations that are what they claim (a malformed one is reported by the definition's check)."""
    return [b for b, kind in ((time_basis, TimeBasis), (group_basis, GroupBasis)) if isinstance(b, kind)]


@dataclass(frozen=True)
class Line:
    """A ``Time basis:`` bullet read back from ``curation_comments``.

    Attributes:
        head: The word before the first colon (``Retrospective``, or an old free-text line's first word), or None.
        tag: ``head`` when it is a time basis tag, else None (a free-text line of the old way).
        set_by: The person in the brackets after the tag, or None.
        on: The date in the brackets, or None.
        reason: The text after the tag and its brackets; the whole text for a line without a tag. It ends at the next
            bullet or at a blank line.
    """

    head: str | None
    tag: str | None
    set_by: str | None
    on: str | None
    reason: str


def lines(comments: str | None, kind: str = "Time") -> list[str]:
    """The text of every ``- Time basis:`` (``kind="Group"``: ``- Group basis:``) bullet in ``comments``."""
    return [m["body"] for m in _BULLET.finditer(comments or "") if m["kind"] == kind]


def parse(comments: str | None) -> Line | None:
    """The first ``Time basis:`` bullet of ``comments``, read back, or None."""
    found = lines(comments)
    if not found:
        return None
    body = " ".join(found[0].split())
    m = _HEAD.match(body)
    if m is None or m["head"] not in BASIS_TAGS:
        head = m["head"] if m is not None and m["inside"] is None and len(m["head"]) > 1 else None
        return Line(head=head, tag=None, set_by=None, on=None, reason=body)
    inside = _RULE_ID.sub("", m["inside"] or "")
    who, _, on = inside.rpartition(",") if "," in inside else (inside, "", "")
    return Line(
        head=m["head"],
        tag=m["head"],
        set_by=who.strip() or None,
        on=on.strip() or None,
        reason=m["rest"].strip(),
    )


def problems(tags: list[str], comments: str | None, *, temporal: bool, grouped: bool) -> list[Problem]:
    """What is wrong with a split's time basis: for a definition once rendered, and for a built container alike.

    Args:
        tags: The ``data_tags``.
        comments: The ``curation_comments``, with the rendered ``Time basis:`` and ``Group basis:`` bullets.
        temporal: Whether the split is temporal.
        grouped: Whether the split holds out groups (a ``grouping``).
    """
    basis = [t for t in dict.fromkeys(tags) if t in BASIS_TAGS]
    group = [t for t in dict.fromkeys(tags) if t in GROUP_BASIS_TAGS]
    found = _split_problems(basis, group, temporal=temporal, grouped=grouped)
    found += _line_problems(basis, group, comments)
    if not temporal and not basis and parse(comments) is None:
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


def _line_problems(basis: list[str], group: list[str], comments: str | None) -> list[Problem]:
    """The rendered lines against the tags: one line, the tag it names, the person of a human-set tag."""
    found = []
    line = parse(comments)
    if len(lines(comments)) > 1:
        found.append(("meta_time_basis_lines", "error", "`curation_comments` hold more than one `Time basis:` line."))
    if line is not None and line.tag is not None and line.tag not in basis:
        message = f"The `Time basis:` line names `{line.tag}`, but `data_tags` carry {basis or 'no time basis'}."
        found.append(("meta_time_basis_mismatch", "error", message))
    for tag in basis:
        if line is None:
            found.append(("meta_time_basis_line_missing", "info", f"`{tag}` has no `Time basis:` line."))
        elif line.tag is None:
            message = f"`{tag}` with a free-text `Time basis:` line: declare `time_basis = TimeBasis({tag!r}, ...)`."
            found.append(("meta_time_basis_unstructured", "info", message))
        if tag in HUMAN_SET_TIME_TAGS and (problem := _attribution_problem(tag, line)):
            found.append(("meta_time_basis_unattributed", "error", f"`{tag}`: {problem}."))
    if line is not None and line.tag is None and not basis and line.head and line.head[:1].isupper():
        message = f"The `Time basis:` line starts with `{line.head}`, which is no time basis tag."
        found.append(("meta_time_basis_unstructured", "info", message))
    if group and not lines(comments, "Group"):
        message = "`ForcedIIDFromGrouped` needs a `Group basis:` line (SPLIT-35)."
        found.append(("meta_group_basis_missing", "error", message))
    return found


def _attribution_problem(tag: str, line: Line | None) -> str | None:
    """Why the line of a human-set ``tag`` does not name a person, a date and a reason, or None."""
    if line is None or line.tag != tag:
        return f"its `Time basis:` line must open `{tag} (<person>, <YYYY-MM-DD>): <reason>`"
    for problem in (person_problem(line.set_by), date_problem(line.on)):
        if problem:
            return problem
    if len(line.reason.split()) < MIN_REASON_WORDS:
        return f"the reason is missing or shorter than {MIN_REASON_WORDS} words"
    return None
