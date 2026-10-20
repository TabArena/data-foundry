"""Decision register: the curators' and the AI's decisions by rule, and the places where they may disagree.

Usage::

    python .claude/skills/knowledge-data-foundry/scripts/decision_register.py [--since YYYY-MM-DD] [--names a,b]
        [--rule ID] [--json PATH] [--records curation/records] [--root datasets/_dev/tabarena-v0pt2]
        [--knowledge .claude/skills/knowledge-curation]

Sources, one decision each:

* every record's ``## Comments``: the paragraphs that start with ``CC (date, name):`` (kind ``cc``),
  ``**Assessment (AI, date)...:**`` (``assessment``), ``**Exception to <ID> (date, name):**`` (``exception``),
  ``**Consistency check (AI, date):**`` (``consistency``) and ``**Counter-argument (AI)...:**`` (``counter``); each
  carries the record's ``suggestion`` (as ``verdict``) and ``decision_markers``. A paragraph ends at a blank line or
  the next such label;
* every ``<root>/*/REVIEW.md``: the titles of the numbered open issues (``open_issue``, author AI, undated);
* the Cases tables of the knowledge files (``<knowledge>/**/*.md``): markdown tables whose header starts with
  ``| Rule |`` (``case``; their ``Kind`` column is kept as ``case_kind``). Missing files or tables are fine.

Each decision gets an outcome from the keyword rules of ``OUTCOME_RULES``, read from its head: the bold lead or the
first sentence, or for the AI's kinds the first sentence that says "recommend". Rule IDs are the
``SEL|USE|LEAK|SPLIT|PROV|TP|CLEAN|EV-<n>`` named anywhere in the text; the legacy "task_probes.md rule N" (or
"rules N-M", "rules N and M") maps to ``TP-N``. Decisions are grouped by rule ID; those without one by their record's
markers and by the mechanisms of ``MECHANISMS`` (a keyword list, easy to extend) they name anywhere.

Flags are candidates for an agent or a curator to check, never verdicts. They compare the mechanisms a decision names
in its head or the sentence after it (``reason_mechanisms``), not anywhere in its text, to stay precise:

* ``exception_without_reason``: an exception line without a "Serves P<k>" (or "serves <rule ID>") part, or with
  fewer than ``MIN_REASON_WORDS`` words before it.
* ``opposite_outcomes``: a rule ID or mechanism that the curators' CC decisions both keep and exclude on different
  datasets; the pairs are listed.
* ``drift``: such pairs by one curator with a clean switch over time (every keep at least ``DRIFT_MIN_DAYS`` days
  before every exclude, or the reverse): the curator's practice changed, so the earlier side may be due for another
  look. The pairs that make a drift are not repeated under ``opposite_outcomes``.
* ``amendment_due``: exceptions to the same rule ID on ``AMENDMENT_AT`` or more datasets (exception lines of the
  records and Cases rows of kind ``exception``).
* ``exception_to_must``: an exception to a rule whose strength is Must (not graded): a Must has no exceptions, only a
  higher-ranked Must overrides it, so the departure is either not reasonable or an amendment of the rule.

``--since``, ``--names`` and ``--rule`` select the decisions shown; the flags still compare them against all the
others, and a flag is shown when a selected decision takes part in it. ``--json PATH`` writes everything.
"""

from __future__ import annotations

import argparse
import datetime
import json
import re
import sys
from collections import defaultdict
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

from data_foundry.curation._paths import records_dir, resolve_curation_root, skills_dir
from data_foundry.curation.store import load_all

if TYPE_CHECKING:
    from data_foundry.curation.record import CurationRecord

# --------------------------------------------------------------------------- the register's vocabulary (extend here)
MECHANISMS: dict[str, str] = {
    "scaling over all rows": (
        r"\b(?:scal(?:e|ed|es|ing)|z-scor\w*|normali[sz]\w*|standardi[sz]\w*|quantile transform\w*|min-max|"
        r"clipped|imputed|chosen by variance)\b[^.;]{0,60}?\b(?:over|across)\s+(?:all|the whole|every|both)\b"
        r"|\bover all rows\b"
    ),
    "transductive": r"\btransductive\b",
    "feature selection": r"\b(?:feature|column) selection\b|\blabel-aware\b",
    "duplicate rows": r"\b(?:duplicated? rows|exact (?:copies|duplicates)|deduplicat\w*|drop the duplicates)\b",
    "duplicate dataset": r"\bduplicate of\b|\bversion case\b",
    "hidden group": r"\bhidden groups?\b",
    "too small": r"\btoo small\b",
    "trivial": r"\btrivial\b",
    "impossible values": r"\bimpossible (?:values?|answers?)\b",
    "one-hot": r"\bone-hot\b",
    "generated data": r"\b(?:generated|simulated|artificial|synthetic) data\b|\bAHDS\b",
    "post-outcome feature": r"\bpost-(?:outcome|election|admission)\b|\bafter the outcome\b|\bprediction point\b",
} | {
    f"probe flag {flag}": rf"\b{flag}\b"
    for flag in ("no_signal", "solved", "no_spread", "one_feature", "drift_baseline", "unstable", "few_minority")
}
"""Mechanism name -> regex (case-insensitive). The task-probe flags (``curation_probes/task.py``) are mechanisms too:
the same flag, kept on one dataset and retired on another, is worth a look."""

OUTCOME_RULES: dict[str, tuple[str, ...]] = {
    "other": (r"^\W*new (?:record|candidate)\b",),
    "exclude": (
        r"\bretir(?:e|ed|es|ing)\b",
        r"\bexclud(?:e|ed|es|ing)\b",
        r"\bdrop(?:ped)? the dataset\b",
        r"\bremoved from (?:TabArena|the benchmark|the working copy)\b",
        r"(?-i:`No(?: \(Retired\))?`)",
        r"^\W*duplicate of\b",
        r"(?:→|->)\s*`?Duplicate\b",
        r"(?-i:(?<![\w`-])No(?=\*\*|[.:,;)]|\s+[\u2014\u2013-]\s|\s+\(|\s*$))",
    ),
    "fix": (
        r"\bfix(?:es|ed|ing)?\b",
        r"\bdrop(?:s|ped|ping)?\b",
        r"\bre-?split\b",
        r"\brebuil(?:d|ds|t)\b",
        r"\bdeduplicat\w*",
        r"\bre-?defined?\b",
        r"\(was (?:IID|grouped|temporal)\)",
        r"\blagged\b",
        r"\bcleaned\b",
        r"\bchanged to\b",
    ),
    "keep": (
        r"\bkeep(?:s|ing)?\b",
        r"\bkept\b",
        r"\bship(?:s|ped)?\b",
        r"\bstays?\b",
        r"\bvalid\b",
        r"\baccept(?:s|ed)?\b",
        r"\bno leak\b",
    ),
}
"""Outcome -> regexes (case-insensitive unless marked ``(?-i:...)``) over a decision's head, with its parentheticals
removed (they cite other records). ``other`` is tried first, then ``exclude``; between ``fix`` and ``keep`` the
earlier match wins; nothing gives ``other``."""

MIN_REASON_WORDS = 8
DRIFT_MIN_DAYS = 2
AMENDMENT_AT = 3
HEAD_WORDS = 40
MAX_PAIRS_SHOWN = 6
TEXT_CHARS = 220

# --------------------------------------------------------------------------- patterns
ID_ALT = r"(?:SEL|USE|LEAK|SPLIT|PROV|TP|CLEAN|EV)-\d+"
RULE_ID = re.compile(rf"\b{ID_ALT}\b")
LEGACY_TP = re.compile(r"task_probes\.md`?,?\s+rules?\s+(\d+)(?:\s*(-|\u2013|to|and)\s*(\d+))?")
DEFINITION = re.compile(rf"^(?:\s*(?:[-*]|\d+\.)\s+)?\*\*({ID_ALT})\b[^*\n]*\*\*")
STRENGTH = re.compile(rf"\*\*({ID_ALT}) \(([^)]*)\)")
SERVES = re.compile(rf"\b[Ss]erves\s+(P\d+|{ID_ALT})\b")
DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
_LEAD = r"^\s*(?:[-*]\s+)?"
_AI_LABEL = r" \(AI(?:,\s*(?P<date>\d{4}-\d{2}-\d{2}))?\)[^*]*?:?\*\*:?\s*"
STARTS: dict[str, re.Pattern] = {
    "cc": re.compile(r"^\s*CC \((?P<date>\d{4}-\d{2}-\d{2}),\s*(?P<author>[^)]+)\):\s*"),
    "assessment": re.compile(_LEAD + r"\*\*Assessment" + _AI_LABEL),
    "exception": re.compile(_LEAD + r"\*\*Exception to (?P<ids>[^*]+?)(?:\s*\((?P<meta>[^)]*)\))?:?\*\*:?\s*"),
    "consistency": re.compile(_LEAD + r"\*\*Consistency check" + _AI_LABEL),
    "counter": re.compile(_LEAD + r"\*\*Counter-argument" + _AI_LABEL),
}
AI_KINDS = ("assessment", "consistency", "counter", "open_issue")
_SENTENCE_END = re.compile(r"(?<=[.!?])\s+(?=[A-Z`*(\[\"'])|:\s+(?=- )")
_CASE_AUTHOR = re.compile(r"\(\d{4}-\d{2}-\d{2},\s*([A-Z][a-z]+)\)|\(([A-Z][a-z]+),\s*\d{4}-\d{2}-\d{2}\)")
_ISSUE = re.compile(r"^(\d+)\.\s+(.*)$")
_TITLE = re.compile(r"^#\s+(\S+)\s*$")
_MECHANISMS = {name: re.compile(pattern, re.IGNORECASE) for name, pattern in MECHANISMS.items()}
_OUTCOMES = {k: [re.compile(p, re.IGNORECASE | re.MULTILINE) for p in v] for k, v in OUTCOME_RULES.items()}


@dataclass
class Decision:
    """One decision (or open question) with what the register groups and compares it by."""

    dataset: str
    date: str | None
    author: str
    kind: str
    outcome: str
    rule_ids: list[str]
    markers: list[str]
    mechanisms: list[str]
    reason_mechanisms: list[str]
    text: str
    verdict: str | None = None
    source: str = ""
    case_kind: str | None = None
    full: str = field(default="", repr=False)

    @property
    def datasets(self) -> set[str]:
        """The dataset names (a Cases row can name several, comma-separated)."""
        return {n.strip() for n in self.dataset.split(",") if n.strip()}

    @property
    def label(self) -> str:
        """``dataset (date, author, kind)`` for a flag."""
        return f"`{self.dataset}` ({self.date or 'undated'}, {self.author}, {self.kind})"

    def to_json(self) -> dict:
        """The decision without its full text."""
        out = asdict(self)
        out.pop("full")
        return out


@dataclass
class ExceptionLine:
    """One ``**Exception to <ID> (date, name):**`` paragraph, with the parts the reason check needs."""

    rule_ids: list[str]
    date: str | None
    author: str | None
    reason: str
    serves: str | None
    words_before_serves: int

    @property
    def problem(self) -> str | None:
        """Why the reason is thin, or None when it has a Serves part after enough words."""
        if self.serves is None:
            return "no 'Serves P<k>' (or 'serves <rule ID>') part"
        if self.words_before_serves < MIN_REASON_WORDS:
            return f"{self.words_before_serves} words before 'Serves {self.serves}' (fewer than {MIN_REASON_WORDS})"
        return None


@dataclass
class Flag:
    """A candidate inconsistency for an agent or curator to check."""

    kind: str
    key: str
    message: str
    decisions: list[Decision]
    pairs: list[tuple[Decision, Decision]] = field(default_factory=list)

    def to_json(self) -> dict:
        """The flag with its decisions and pairs as dicts."""
        return {
            "kind": self.kind,
            "key": self.key,
            "message": self.message,
            "decisions": [d.to_json() for d in self.decisions],
            "pairs": [[k.to_json(), e.to_json()] for k, e in self.pairs],
        }


# --------------------------------------------------------------------------- rule IDs and exception lines
def _id_key(rule_id: str) -> tuple[str, int]:
    prefix, _, number = rule_id.partition("-")
    return prefix, int(number) if number.isdigit() else 0


def rule_ids_in(text: str) -> list[str]:
    """The rule IDs a text names, with the legacy ``task_probes.md rule N`` as ``TP-N``; sorted, unique."""
    ids = set(RULE_ID.findall(text))
    for match in LEGACY_TP.finditer(text):
        first, sep, second = int(match.group(1)), match.group(2), match.group(3)
        if second is None:
            ids.add(f"TP-{first}")
        elif sep == "and":
            ids |= {f"TP-{first}", f"TP-{second}"}
        else:
            ids |= {f"TP-{n}" for n in range(first, int(second) + 1)}
    return sorted(ids, key=_id_key)


def rule_ids_defined(knowledge_dir: Path | str) -> set[str]:
    """The rule IDs the knowledge files define: ``**LEAK-3 (Must).**`` at the start of a line, outside code fences."""
    found: set[str] = set()
    root = Path(knowledge_dir)
    if not root.exists():
        return found
    for path in sorted(root.rglob("*.md")):
        fenced = False
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.lstrip().startswith("```"):
                fenced = not fenced
            elif not fenced and (match := DEFINITION.match(line)):
                found.add(match.group(1))
    return found


def rule_strengths(knowledge_dir: Path | str) -> dict[str, str]:
    """The strength each rule ID is defined with, as written (``Must``, ``Should; narrows LEAK-1``, ...)."""
    found: dict[str, str] = {}
    root = Path(knowledge_dir)
    if not root.exists():
        return found
    for path in sorted(root.rglob("*.md")):
        fenced = False
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.lstrip().startswith("```"):
                fenced = not fenced
            elif not fenced and DEFINITION.match(line) and (match := STRENGTH.search(line)):
                found[match.group(1)] = match.group(2).strip()
    return found


def _is_must(strength: str | None) -> bool:
    """A plain Must: not a Should or Weigh, and not graded (``Must when strong, Should when weak``)."""
    return bool(strength) and strength.startswith("Must") and "Should" not in strength and "Weigh" not in strength


def _paragraphs(text: str) -> list[tuple[str, re.Match, str]]:
    """The labelled paragraphs of a comment: ``(kind, label match, text after the label)``."""
    out: list[tuple[str, re.Match, list[str]]] = []
    current: list[str] | None = None
    for line in text.splitlines():
        started = next(((kind, m) for kind, pattern in STARTS.items() if (m := pattern.match(line))), None)
        if started is not None:
            current = [line[started[1].end() :]]
            out.append((*started, current))
        elif not line.strip():
            current = None
        elif current is not None:
            current.append(line.strip())
    return [(kind, match, " ".join(lines).strip()) for kind, match, lines in out]


def _exception_meta(match: re.Match) -> tuple[list[str], str | None, str | None]:
    """The rule IDs, date and author of an exception label."""
    meta = match.group("meta") or ""
    found = DATE.search(meta)
    author = DATE.sub("", meta).strip(" ,") or None
    return rule_ids_in(match.group("ids")), found.group(0) if found else None, author


def exception_line(body: str, rule_ids: list[str], date: str | None, author: str | None) -> ExceptionLine:
    """The parts of one exception paragraph's text (after its label)."""
    serves = SERVES.search(body)
    before = body[: serves.start()] if serves else body
    return ExceptionLine(
        rule_ids=rule_ids,
        date=date,
        author=author,
        reason=body,
        serves=serves.group(1) if serves else None,
        words_before_serves=len(before.split()),
    )


def parse_exception_lines(text: str) -> list[ExceptionLine]:
    """Every ``**Exception to <ID> (date, name):** <fact>. Serves P<k>: <why>.`` paragraph of ``text``."""
    return [
        exception_line(body, *_exception_meta(match)) for kind, match, body in _paragraphs(text) if kind == "exception"
    ]


# --------------------------------------------------------------------------- outcome and mechanisms
def _sentences(text: str) -> list[str]:
    return [s for s in _SENTENCE_END.split(text) if s.strip()]


def head_of(text: str, kind: str) -> str:
    """The part of a decision its outcome is read from (see the module docstring)."""
    text = text.strip()
    if kind in AI_KINDS:
        recommend = next((s for s in _sentences(text) if re.search(r"\brecommend", s, re.IGNORECASE)), None)
        if recommend:
            return recommend
    bold = re.match(r"\*\*(.+?)\*\*", text)
    if bold:
        return bold.group(1)
    sentences = _sentences(text)
    return " ".join((sentences[0] if sentences else text).split()[:HEAD_WORDS])


def reason_of(text: str, kind: str) -> str:
    """The head and the sentence after it: where a decision names what it is about."""
    head = head_of(text, kind)
    sentences = _sentences(text.strip())
    at = next((i for i, s in enumerate(sentences) if head[:40] in s or s.strip("* ") in head), 0)
    return " ".join([head, *sentences[at + 1 : at + 2]])


def _without_parentheticals(text: str) -> str:
    previous = None
    while previous != text:
        previous, text = text, re.sub(r"\([^()]*\)", " ", text)
    return text


def outcome_of(head: str) -> str:
    """``keep``, ``exclude``, ``fix`` or ``other`` from the keyword rules (``OUTCOME_RULES``)."""
    head = _without_parentheticals(head)
    if any(p.search(head) for p in _OUTCOMES["other"]):
        return "other"
    if any(p.search(head) for p in _OUTCOMES["exclude"]):
        return "exclude"
    first = {
        outcome: min((m.start() for p in _OUTCOMES[outcome] if (m := p.search(head))), default=None)
        for outcome in ("fix", "keep")
    }
    found = {k: v for k, v in first.items() if v is not None}
    return min(found, key=found.get) if found else "other"


def mechanisms_in(text: str) -> list[str]:
    """The mechanisms of ``MECHANISMS`` a text names."""
    return [name for name, pattern in _MECHANISMS.items() if pattern.search(text)]


def _short(text: str) -> str:
    text = " ".join(text.split())
    return text if len(text) <= TEXT_CHARS else text[: TEXT_CHARS - 3].rstrip() + "..."


def make_decision(dataset: str, kind: str, body: str, **fields) -> Decision:
    """A decision from its text: outcome, rule IDs and mechanisms are read from ``body``.

    ``fields`` sets the other attributes (``date``, ``author``, ``markers``, ...); ``rule_ids`` given there are
    added to the ones the text names.
    """
    ids = set(fields.pop("rule_ids", [])) | set(rule_ids_in(body))
    fields.setdefault("markers", [])
    return Decision(
        dataset=dataset,
        kind=kind,
        outcome=outcome_of(head_of(body, kind)),
        rule_ids=sorted(ids, key=_id_key),
        mechanisms=mechanisms_in(body),
        reason_mechanisms=mechanisms_in(reason_of(body, kind)),
        text=_short(body),
        full=body,
        **fields,
    )


# --------------------------------------------------------------------------- the three sources
def record_decisions(records: list[CurationRecord]) -> list[Decision]:
    """The labelled paragraphs of every record's comments."""
    out = []
    for record in records:
        common = {
            "markers": list(record.decision_markers),
            "verdict": record.suggestion,
            "source": f"curation/records/{record.unique_name}.md",
        }
        for kind, match, body in _paragraphs(record.comments or ""):
            if kind == "cc":
                who = {"date": match.group("date"), "author": match.group("author").strip()}
            elif kind == "exception":
                ids, date, author = _exception_meta(match)
                who = {"date": date, "author": author or "?", "rule_ids": ids}
            else:
                who = {"date": match.group("date"), "author": "AI"}
            out.append(make_decision(record.unique_name, kind, body, **who, **common))
    return out


def _issues(lines: list[str]) -> list[list[str]]:
    """The numbered issues of a REVIEW.md: each its first line and its indented or blank continuation lines."""
    issues: list[list[str]] = []
    current: list[str] | None = None
    for line in lines:
        if match := _ISSUE.match(line):
            current = [match.group(2)]
            issues.append(current)
        elif current is not None and (line.startswith("   ") or not line.strip()):
            current.append(line.strip())
        else:
            current = None  # another block of the file ends the issue
    return issues


def review_decisions(root: Path, records: dict[str, CurationRecord]) -> list[Decision]:
    """The numbered open issues of every ``<root>/*/REVIEW.md``, by their titles."""
    out = []
    for path in sorted(root.glob("*/REVIEW.md")) if root.exists() else []:
        lines = path.read_text(encoding="utf-8").splitlines()
        name = next((m.group(1) for line in lines if (m := _TITLE.match(line))), path.parent.name)
        record = records.get(name)
        for issue in _issues(lines):
            bold = re.match(r"\*\*(.+?)\*\*", issue[0])
            title = bold.group(1) if bold else (_sentences(issue[0]) or [issue[0]])[0]
            body = " ".join(s for s in issue if s)
            decision = make_decision(
                name,
                "open_issue",
                title,
                date=None,
                author="AI",
                rule_ids=rule_ids_in(body),
                markers=list(record.decision_markers) if record else [],
                verdict=record.suggestion if record else None,
                source=str(path),
            )
            decision.mechanisms = sorted(set(decision.mechanisms) | set(mechanisms_in(body)))
            out.append(decision)
    return out


def _cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def _plain(cell: str) -> str:
    cell = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", cell)
    return cell.replace("`", "").replace("**", "").strip()


def _column(header: list[str], cells: list[str], *names: str) -> str | None:
    index = next((i for i, h in enumerate(header) if any(h.startswith(n) for n in names)), None)
    return cells[index] if index is not None and index < len(cells) else None


def _case(header: list[str], cells: list[str], path: Path) -> Decision:
    """One row of a Cases table."""
    row = " | ".join(cells)
    dataset_cell = _column(header, cells, "dataset", "case", "record", "example") or ""
    names = re.findall(r"`([^`]+)`", dataset_cell) or [_plain(dataset_cell)]
    found = DATE.search(_column(header, cells, "date", "when") or "") or DATE.search(row)
    author = _column(header, cells, "by", "who", "curator", "author")
    if not author:
        named = _CASE_AUTHOR.search(row)
        author = (named.group(1) or named.group(2)) if named else "case table"
    case_kind = _column(header, cells, "kind")
    text = " | ".join(_plain(c) for c in cells[1:])
    decision = make_decision(
        ", ".join(n for n in names if n) or "?",
        "case",
        _column(header, cells, "outcome", "decision", "verdict", "call", "result") or text,
        date=found.group(0) if found else None,
        author=_plain(author),
        rule_ids=rule_ids_in(cells[0]) or rule_ids_in(row),
        source=str(path),
        case_kind=_plain(case_kind) if case_kind else None,
    )
    decision.text, decision.full, decision.mechanisms = _short(text), row, mechanisms_in(row)
    return decision


def case_decisions(knowledge_dir: Path) -> list[Decision]:
    """The rows of the Cases tables (header starting with ``| Rule |``) of the knowledge files."""
    out: list[Decision] = []
    for path in sorted(knowledge_dir.rglob("*.md")) if knowledge_dir.exists() else []:
        lines = path.read_text(encoding="utf-8").splitlines()
        i = 0
        while i < len(lines):
            if not re.match(r"^\|\s*Rule\s*\|", lines[i]):
                i += 1
                continue
            header = [h.lower() for h in _cells(lines[i])]
            i += 2  # the header and its separator
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                out.append(_case(header, _cells(lines[i]), path))
                i += 1
    return out


def collect(records_path: Path, root: Path, knowledge_dir: Path) -> list[Decision]:
    """Every decision of the three sources."""
    records = load_all(records_path)
    by_name = {r.unique_name: r for r in records}
    return record_decisions(records) + review_decisions(root, by_name) + case_decisions(knowledge_dir)


# --------------------------------------------------------------------------- grouping and flags
def group(decisions: list[Decision]) -> dict[str, dict[str, list[Decision]]]:
    """``{"rule": {ID: [...]}, "mechanism": {...}, "marker": {...}, "none": {"": [...]}}``."""
    groups: dict[str, dict[str, list[Decision]]] = {k: defaultdict(list) for k in ("rule", "mechanism", "marker")}
    groups["none"] = defaultdict(list)
    for d in decisions:
        if d.rule_ids:
            for rule_id in d.rule_ids:
                groups["rule"][rule_id].append(d)
            continue
        for name in d.mechanisms:
            groups["mechanism"][name].append(d)
        for marker in d.markers:
            groups["marker"][marker].append(d)
        if not d.mechanisms and not d.markers:
            groups["none"][""].append(d)
    order = {"rule": lambda kv: _id_key(kv[0])}
    return {k: dict(sorted(v.items(), key=order.get(k, lambda kv: kv[0]))) for k, v in groups.items()}


def _date(d: Decision) -> str:
    return d.date or ""


def _days(earlier: str, later: str) -> int:
    """Days from ``earlier`` to ``later`` (0 when either is undated)."""
    if not earlier or not later:
        return 0
    return (datetime.date.fromisoformat(later) - datetime.date.fromisoformat(earlier)).days


def _involved(pairs: list[tuple[Decision, Decision]]) -> list[Decision]:
    return sorted({id(d): d for pair in pairs for d in pair}.values(), key=_date)


def _drift(author: str, key: str, pairs: list[tuple[Decision, Decision]]) -> Flag | None:
    """A drift flag when one curator's pairs switch cleanly from one outcome to the other."""
    last_keep, first_keep = max(_date(k) for k, _ in pairs), min(_date(k) for k, _ in pairs)
    last_exclude, first_exclude = max(_date(e) for _, e in pairs), min(_date(e) for _, e in pairs)
    if _days(last_keep, first_exclude) >= DRIFT_MIN_DAYS:
        earlier, until, later, since = "keep", last_keep, "exclude", first_exclude
    elif _days(last_exclude, first_keep) >= DRIFT_MIN_DAYS:
        earlier, until, later, since = "exclude", last_exclude, "keep", first_keep
    else:
        return None
    message = (
        f"{author}: {earlier} up to {until}, {later} from {since} on; check whether the earlier {earlier} "
        "decisions still hold"
    )
    return Flag("drift", key, message, _involved(pairs), pairs)


def _opposite_flags(decisions: list[Decision]) -> list[Flag]:
    """``drift`` and ``opposite_outcomes`` over the curators' CC decisions, per rule ID and reason mechanism."""
    by_key: dict[str, list[Decision]] = defaultdict(list)
    for d in decisions:
        if d.kind == "cc" and d.outcome in ("keep", "exclude"):
            for key in d.rule_ids + [f"mechanism: {m}" for m in d.reason_mechanisms]:
                by_key[key].append(d)
    flags = []
    for key, items in sorted(by_key.items()):
        keeps = [d for d in items if d.outcome == "keep"]
        excludes = [d for d in items if d.outcome == "exclude"]
        pairs = [(k, e) for k in keeps for e in excludes if not k.datasets & e.datasets]
        drifted: set[tuple[int, int]] = set()
        for author in sorted({d.author for pair in pairs for d in pair}):
            own = [(k, e) for k, e in pairs if k.author == e.author == author]
            if own and (flag := _drift(author, key, own)):
                flags.append(flag)
                drifted |= {(id(k), id(e)) for k, e in own}
        rest = [(k, e) for k, e in pairs if (id(k), id(e)) not in drifted]
        if rest:
            n_keep, n_exclude = len({id(k) for k, _ in rest}), len({id(e) for _, e in rest})
            message = f"{n_keep} keep and {n_exclude} exclude decisions by curators, {len(rest)} pairs"
            flags.append(Flag("opposite_outcomes", key, message, _involved(rest), rest))
    return flags


def flags_for(decisions: list[Decision], strengths: dict[str, str] | None = None) -> list[Flag]:
    """Every flag over all decisions (the selection is applied afterwards); ``strengths`` from ``rule_strengths``."""
    flags: list[Flag] = []
    exceptions = [d for d in decisions if d.kind == "exception"]
    for d in exceptions:
        problem = exception_line(d.full, d.rule_ids, d.date, d.author).problem
        if problem:
            flags.append(Flag("exception_without_reason", ", ".join(d.rule_ids) or "?", problem, [d]))
    flags += _opposite_flags(decisions)
    case_exceptions = [d for d in decisions if d.kind == "case" and "exception" in (d.case_kind or "").lower()]
    by_rule: dict[str, list[Decision]] = defaultdict(list)
    for d in exceptions + case_exceptions:
        for rule_id in d.rule_ids:
            by_rule[rule_id].append(d)
    for rule_id, items in sorted(by_rule.items(), key=lambda kv: _id_key(kv[0])):
        if _is_must((strengths or {}).get(rule_id)):
            for d in items:
                message = (
                    f"an exception to {rule_id}, a Must: only a higher-ranked Must overrides it, else amend the rule"
                )
                flags.append(Flag("exception_to_must", rule_id, message, [d]))
        datasets = set().union(*(d.datasets for d in items))
        if len(datasets) >= AMENDMENT_AT:
            message = f"exceptions to {rule_id} on {len(datasets)} datasets: the next pass proposes an amendment"
            flags.append(Flag("amendment_due", rule_id, message, sorted(items, key=_date)))
    return flags


def selector(since: str | None, names: set[str] | None, rule: str | None):
    """The predicate of ``--since``, ``--names`` and ``--rule`` (undated decisions fail ``--since``)."""

    def selected(d: Decision) -> bool:
        if since and (d.date is None or d.date < since):
            return False
        if names and not names & d.datasets:
            return False
        if rule:
            keys = set(d.rule_ids) if d.rule_ids else set(d.mechanisms) | set(d.markers)
            return rule in keys
        return True

    return selected


def select_flags(flags: list[Flag], selected) -> list[Flag]:
    """The flags a selected decision takes part in, their pairs narrowed to those with a selected side."""
    out = []
    for flag in flags:
        if any(selected(d) for d in flag.decisions):
            flag.pairs = [p for p in flag.pairs if selected(p[0]) or selected(p[1])]
            out.append(flag)
    return out


# --------------------------------------------------------------------------- output
def _cell(text: str) -> str:
    return " ".join(str(text).split()).replace("|", "\\|")


def _table(decisions: list[Decision]) -> list[str]:
    lines = ["| date | dataset | author | kind | outcome | text |", "|---|---|---|---|---|---|"]
    for d in sorted(decisions, key=lambda d: (_date(d), d.dataset)):
        lines.append(f"| {d.date or ''} | `{d.dataset}` | {d.author} | {d.kind} | {d.outcome} | {_cell(d.text)} |")
    return lines


def _pair_lines(pairs: list[tuple[Decision, Decision]]) -> list[str]:
    """The keep-exclude pairs, one line per decision of the side with fewer decisions."""
    keeps = {id(k): k for k, _ in pairs}
    excludes = {id(e): e for _, e in pairs}
    by_keep = len(keeps) <= len(excludes)
    side, outcome, other = (keeps, "keep", "exclude") if by_keep else (excludes, "exclude", "keep")
    lines = []
    for key, d in list(side.items())[:MAX_PAIRS_SHOWN]:
        partners = [e if by_keep else k for k, e in pairs if id(k if by_keep else e) == key]
        named = ", ".join(f"`{p.dataset}` ({p.date or 'undated'})" for p in partners)
        lines.append(f"- {outcome} {d.label} vs {other} {named}")
    if len(side) > MAX_PAIRS_SHOWN:
        lines.append(f"- and {len(side) - MAX_PAIRS_SHOWN} more")
    return lines


def _counts(values) -> str:
    counts: dict[str, int] = defaultdict(int)
    for value in values:
        counts[value] += 1
    return ", ".join(f"{k} {v}" for k, v in sorted(counts.items()))


def render(decisions: list[Decision], flags: list[Flag], defined: set[str], *, total: int) -> str:
    """The register as markdown: decisions by rule ID, mechanism and marker, then the flags."""
    groups = group(decisions)
    lines = [
        "# Decision register",
        "",
        f"{len(decisions)} decisions shown of {total} ({_counts(d.kind for d in decisions)}); outcomes "
        f"{_counts(d.outcome for d in decisions)}. Rule IDs defined in the knowledge files: {len(defined) or 'none'}.",
        "",
        "Outcomes come from keyword rules on each decision's head; read the text before acting on one.",
    ]
    titles = {
        "rule": "By rule ID",
        "mechanism": "Without a rule ID, by mechanism",
        "marker": "Without a rule ID, by the record's markers",
    }
    for kind, title in titles.items():
        lines += ["", f"## {title}"]
        if not groups[kind]:
            lines += ["", "None."]
        for key, items in groups[kind].items():
            undefined = kind == "rule" and defined and key not in defined
            note = " (not defined in the knowledge files)" if undefined else ""
            lines += ["", f"### {key}{note} ({len(items)})", "", *_table(items)]
    none = groups["none"].get("", [])
    lines += ["", f"{len(none)} decisions have no rule ID, mechanism or marker (listed in `--json`)."]
    lines += ["", f"## Flags ({len(flags)})", "", "Candidates to check, never verdicts."]
    for i, flag in enumerate(flags, 1):
        lines += ["", f"### {i}. {flag.kind}: {flag.key}", "", flag.message + "."]
        if flag.pairs:
            lines += [*_pair_lines(flag.pairs), "", "The decisions:", ""]
        lines += [f"- {d.label}, {d.outcome}: {_cell(d.text)}" for d in flag.decisions]
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    """Build the register; see the module docstring."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--since", help="Only decisions on or after this date (YYYY-MM-DD).")
    parser.add_argument("--names", help="Only these datasets (comma-separated unique names).")
    parser.add_argument("--rule", help="Only this rule ID (or a mechanism or marker for decisions without an ID).")
    parser.add_argument("--json", type=Path, help="Also write decisions, groups and flags as JSON here.")
    parser.add_argument("--records", type=Path, default=None, help="Records folder (default: curation/records).")
    parser.add_argument("--root", type=Path, default=None, help="Default: datasets/_dev/tabarena-v0pt2.")
    parser.add_argument("--knowledge", type=Path, default=None, help="Default: .claude/skills/knowledge-curation.")
    args = parser.parse_args(argv)

    root = args.root or resolve_curation_root().parent / "datasets" / "_dev" / "tabarena-v0pt2"
    knowledge = args.knowledge or skills_dir() / "knowledge-curation"
    decisions = collect(args.records or records_dir(), root, knowledge)
    defined = rule_ids_defined(knowledge)
    names = {n.strip() for n in args.names.split(",")} if args.names else None
    selected = selector(args.since, names, args.rule)
    flags = select_flags(flags_for(decisions, rule_strengths(knowledge)), selected)
    shown = [d for d in decisions if selected(d)]
    print(render(shown, flags, defined, total=len(decisions)), end="")
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "total": len(decisions),
            "rule_ids_defined": sorted(defined, key=_id_key),
            "groups": {k: {key: len(v) for key, v in g.items()} for k, g in group(shown).items()},
            "flags": [f.to_json() for f in flags],
            "decisions": [d.to_json() for d in shown],
        }
        args.json.write_text(json.dumps(payload, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
