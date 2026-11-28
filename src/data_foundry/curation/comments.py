"""The labelled paragraphs of a record's ``## Comments``, and the rule IDs they cite and the knowledge files define.

A comment paragraph starts with one of these labels (``STARTS``) and ends at a blank line or the next label:

* ``CC (<date>, <curator>):``, the curator's decision (kind ``cc``);
* ``**Assessment (AI, <date>):**``, the AI's evidence (``assessment``);
* ``**Exception to <ID> (<date>, <curator>):** <fact>. Serves P<k>: <why>.`` (``exception``);
* ``**Consistency check (AI, <date>):**`` (``consistency``) and ``**Counter-argument (AI, <date>):**`` (``counter``).

A rule ID is ``SEL|USE|LEAK|SPLIT|PROV|TP|CLEAN|EV|MET-<n>``; a knowledge file defines one as ``**LEAK-3 (Must).**``
at the start of a line, outside code fences. The decision register (knowledge-data-foundry's
``decision_register.py``) and the record tests read comments through this module.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterator

ID_ALT = r"(?:SEL|USE|LEAK|SPLIT|PROV|TP|CLEAN|EV|MET)-\d+"
RULE_ID = re.compile(rf"\b{ID_ALT}\b")
LEGACY_TP = re.compile(r"task_probes\.md`?,?\s+rules?\s+(\d+)(?:\s*(-|\u2013|to|and)\s*(\d+))?")
DEFINITION = re.compile(rf"^(?:\s*(?:[-*]|\d+\.)\s+)?\*\*({ID_ALT})\b[^*\n]*\*\*")
DEFINITION_START = re.compile(rf"^(?:\s*(?:[-*]|\d+\.)\s+)?\*\*({ID_ALT})\b")
STRENGTH = re.compile(rf"\*\*({ID_ALT}) \(([^)]*)\)")
SERVES = re.compile(rf"\b[Ss]erves\s+(P\d+|{ID_ALT})\b")
DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
MIN_REASON_WORDS = 8
"""The words an exception's fact needs before its ``Serves`` part."""
_LEAD = r"^\s*(?:[-*]\s+)?"
_AI_LABEL = r" \(AI(?:,\s*(?P<date>\d{4}-\d{2}-\d{2}))?\)[^*]*?:?\*\*:?\s*"
STARTS: dict[str, re.Pattern] = {
    "cc": re.compile(r"^\s*CC \((?P<date>\d{4}-\d{2}-\d{2}),\s*(?P<author>[^)]+)\):\s*"),
    "assessment": re.compile(_LEAD + r"\*\*Assessment" + _AI_LABEL),
    "exception": re.compile(_LEAD + r"\*\*Exception to (?P<ids>[^*]+?)(?:\s*\((?P<meta>[^)]*)\))?:?\*\*:?\s*"),
    "consistency": re.compile(_LEAD + r"\*\*Consistency check" + _AI_LABEL),
    "counter": re.compile(_LEAD + r"\*\*Counter-argument" + _AI_LABEL),
}
"""The label of each kind of comment paragraph."""


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


def id_key(rule_id: str) -> tuple[str, int]:
    """The sort key of a rule ID: its prefix, then its number."""
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
    return sorted(ids, key=id_key)


def _definition_heads(knowledge_dir: Path | str) -> Iterator[str]:
    """The heads of the rule definitions (``**LEAK-3 (Must).**`` at the start of a line, outside code fences), each
    joined across lines until its bold closes, so a head wrapped at 120 characters is still read whole.
    """
    root = Path(knowledge_dir)
    if not root.exists():
        return
    for path in sorted(root.rglob("*.md")):
        fenced = False
        lines = path.read_text(encoding="utf-8").splitlines()
        for i, line in enumerate(lines):
            if line.lstrip().startswith("```"):
                fenced = not fenced
            elif not fenced and DEFINITION_START.match(line):
                head = line
                for more in lines[i + 1 : i + 12]:  # a head runs to its closing bold, within its paragraph
                    if DEFINITION.match(head) or not more.strip():
                        break
                    head = f"{head} {more.strip()}"
                if DEFINITION.match(head):
                    yield head


def rule_ids_defined(knowledge_dir: Path | str) -> set[str]:
    """The rule IDs the knowledge files define: ``**LEAK-3 (Must).**`` at the start of a line, outside code fences."""
    return {DEFINITION.match(head).group(1) for head in _definition_heads(knowledge_dir)}


def rule_strengths(knowledge_dir: Path | str) -> dict[str, str]:
    """The strength each rule ID is defined with, as written (``Must``, ``Should; narrows LEAK-1``, ...)."""
    found: dict[str, str] = {}
    for head in _definition_heads(knowledge_dir):
        if match := STRENGTH.search(head):
            found[match.group(1)] = match.group(2).strip()
    return found


def paragraphs(text: str) -> list[tuple[str, re.Match, str]]:
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


def exception_meta(match: re.Match) -> tuple[list[str], str | None, str | None]:
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
        exception_line(body, *exception_meta(match)) for kind, match, body in paragraphs(text) if kind == "exception"
    ]
