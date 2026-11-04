"""A sweep over the skill files: what must hold after any change to them.

The prose lines are at most 120 characters; the rule heads are ones the decision register reads (a known prefix, a
strength, one definition per ID); the Cases tables name defined rules, use a known kind and keep the table's number
of cells; every cited rule ID is defined; every skill has its frontmatter; the indexes of the two knowledge skills
list every file they hold; and the register runs on the repository. Links are checked by ``test_doc_links.py``.
"""

from __future__ import annotations

import importlib.util
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / ".claude" / "skills"
KNOWLEDGE = SKILLS / "knowledge-curation"
KDF = SKILLS / "knowledge-data-foundry"
SKILL_DOCS = sorted(SKILLS.rglob("*.md"))
WIDTH = 120
CASE_KINDS = {"applied", "exception", "proposed", "overrule"}
"""The kinds of a Cases row: a rule applied, an exception to it, a proposal not yet decided, a source's choice that
the curator overruled."""
RETIRED_IDS = {"SEL-17": "merged into PROV-1 and PROV-2 on 2026-10-19; selection.md cites it as the former rule"}
"""Rule IDs that are cited on purpose although no file defines them any more, with the reason."""
REGISTER_FLOOR = 175
"""The register found 175 rule IDs on 2026-11-04; fewer means rule heads stopped being read."""
ANY_HEAD = re.compile(r"^(?:\s*(?:[-*]|\d+\.)\s+)?\*\*([A-Z]+)-(\d+)\b")


@pytest.fixture(scope="module")
def register():
    """The decision register script as a module (it lives in a skill, not in the package)."""
    path = KDF / "scripts" / "decision_register.py"
    spec = importlib.util.spec_from_file_location("decision_register", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module  # dataclasses look their module up there
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def defined(register):
    """The rule IDs the knowledge files define, as the register reads them."""
    return register.rule_ids_defined(KNOWLEDGE)


def _rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def _prose(path: Path):
    """(line number, line) of the prose lines: outside the YAML front matter and fenced code, not table rows."""
    lines = path.read_text(encoding="utf-8").splitlines()
    fenced, front = False, bool(lines) and lines[0] == "---"
    for number, line in enumerate(lines, 1):
        if front:
            if number > 1 and line == "---":
                front = False
            continue
        stripped = line.lstrip()
        if stripped.startswith(("```", "~~~")):
            fenced = not fenced
            continue
        if not fenced and not stripped.startswith("|"):
            yield number, line


def _too_long(line: str) -> bool:
    """Over the width, unless it is a heading made of one link or the word across the margin is a long URL or path."""
    if len(line) <= WIDTH or re.fullmatch(r"#{1,6}\s+\[[^\]]*\]\([^)]*\)\s*", line):
        return False
    crossing = next((m.group(0) for m in re.finditer(r"\S+", line) if m.start() < WIDTH < m.end()), None)
    return not (crossing and len(crossing) >= 40 and "/" in crossing)


def _cells(row: str) -> list[str]:
    """The cells of a table row, split on the pipes outside inline code that are not escaped."""
    cells, cell, code, previous = [], [], False, ""
    for char in row.strip():
        if char == "`":
            code = not code
        if char == "|" and not code and previous != "\\":
            cells.append("".join(cell).strip())
            cell = []
        else:
            cell.append(char)
        previous = char
    cells.append("".join(cell).strip())
    return cells[1:-1]


def _rule_tables(path: Path):
    """(header line, header cells, [(line, cells)]) of each table whose header's first cell is ``Rule``."""
    lines = path.read_text(encoding="utf-8").splitlines()
    fenced, number = False, 0
    while number < len(lines):
        line = lines[number]
        if line.lstrip().startswith(("```", "~~~")):
            fenced = not fenced
        elif not fenced and line.startswith("|") and _cells(line)[:1] == ["Rule"]:
            header, rows, row = _cells(line), [], number + 2
            while row < len(lines) and lines[row].startswith("|"):
                rows.append((row + 1, _cells(lines[row])))
                row += 1
            yield number + 1, header, rows
            number = row
            continue
        number += 1


def _heads():
    """(file, line, rule ID, prefix) of every rule head in the knowledge files, whatever its prefix."""
    for path in sorted((KNOWLEDGE / "references").glob("*.md")):
        fenced = False
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if line.lstrip().startswith("```"):
                fenced = not fenced
            elif not fenced and (match := ANY_HEAD.match(line)):
                yield path.name, number, f"{match.group(1)}-{match.group(2)}", match.group(1)


def _frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"---\n(.*?)\n---\n", text, re.DOTALL)
    return yaml.safe_load(match.group(1)) if match else {}


# --------------------------------------------------------------------------- prose
@pytest.mark.parametrize("doc", SKILL_DOCS, ids=_rel)
def test_prose_lines_fit_the_width(doc):
    """Prose wraps at 120 characters, as the code does; tables, code and front matter are exempt."""
    long = [number for number, line in _prose(doc) if _too_long(line)]
    assert not long, f"{_rel(doc)}: lines over {WIDTH} characters: {long}"


# --------------------------------------------------------------------------- rule heads
def test_rule_head_prefixes_are_known_to_the_register(register):
    """A rule with a prefix the register does not know is invisible to it (MET was missing until 2026-11-04)."""
    known = set(re.search(r"\(\?:([A-Z|]+)\)", register.ID_ALT).group(1).split("|"))
    unknown = sorted({(file, line, rule) for file, line, rule, prefix in _heads() if prefix not in known})
    assert not unknown, f"rule heads with a prefix missing from the register's ID_ALT: {unknown}"


def test_every_rule_head_is_read_with_a_strength(register, defined):
    """The register reads each head whole, wrapped or not, with its strength (CLEAN-11 was missed until 2026-11-04)."""
    strengths = register.rule_strengths(KNOWLEDGE)
    heads = {rule for _, _, rule, _ in _heads()}
    assert not heads - defined, f"rule heads the register does not read: {sorted(heads - defined)}"
    assert not heads - set(strengths), f"rule heads without a strength: {sorted(heads - set(strengths))}"


def test_no_rule_is_defined_twice():
    """One head per rule ID: a second one would make the register read only one of them."""
    counts = Counter(rule for _, _, rule, _ in _heads())
    twice = {rule: [(f, n) for f, n, r, _ in _heads() if r == rule] for rule, count in counts.items() if count > 1}
    assert not twice, f"rule IDs defined more than once: {twice}"


# --------------------------------------------------------------------------- Cases tables
CASE_TABLES = [(path, line, header, rows) for path in SKILL_DOCS for line, header, rows in _rule_tables(path) if rows]


@pytest.mark.parametrize(
    ("path", "line", "header", "rows"), CASE_TABLES, ids=lambda v: _rel(v) if isinstance(v, Path) else ""
)
def test_cases_rows_are_well_formed(path, line, header, rows, register, defined):
    """Each row has the header's cells, names defined rules in its first cell, and a known kind."""
    problems = []
    for number, cells in rows:
        if len(cells) != len(header):
            problems.append((number, f"{len(cells)} cells, the header has {len(header)}"))
            continue
        ids = register.rule_ids_in(cells[0])
        if not ids and not cells[0].endswith("(factor)"):  # a weighed factor of the file, named, not numbered
            problems.append((number, f"no rule ID in {cells[0]!r}"))
        undefined = [rule for rule in ids if rule not in defined and rule not in RETIRED_IDS]
        if undefined:
            problems.append((number, f"undefined rule IDs {undefined}"))
        if header[-1] == "Kind" and cells[-1] not in CASE_KINDS:
            problems.append((number, f"kind {cells[-1]!r} is none of {sorted(CASE_KINDS)}"))
    assert not problems, f"{_rel(path)}, the table at line {line}: {problems}"


# --------------------------------------------------------------------------- cited rule IDs
@pytest.mark.parametrize("doc", SKILL_DOCS, ids=_rel)
def test_cited_rule_ids_are_defined(doc, register, defined):
    """Every rule ID a skill file cites is defined, or listed in RETIRED_IDS with the reason."""
    cited = set(register.RULE_ID.findall(doc.read_text(encoding="utf-8")))
    undefined = sorted(cited - defined - set(RETIRED_IDS))
    assert not undefined, f"{_rel(doc)} cites rule IDs no knowledge file defines: {undefined}"


def test_retired_ids_are_not_defined_again(defined):
    """A retired ID that is defined again no longer belongs in RETIRED_IDS."""
    assert not set(RETIRED_IDS) & defined, f"defined again, drop from RETIRED_IDS: {sorted(set(RETIRED_IDS) & defined)}"


# --------------------------------------------------------------------------- skills and their indexes
@pytest.mark.parametrize("skill", sorted(SKILLS.glob("*/SKILL.md")), ids=lambda p: p.parent.name)
def test_every_skill_has_its_frontmatter(skill):
    """Each SKILL.md has a `name` equal to its folder and a `description`."""
    meta = _frontmatter(skill)
    assert meta.get("name") == skill.parent.name, f"{_rel(skill)}: `name` is {meta.get('name')!r}"
    assert str(meta.get("description") or "").strip(), f"{_rel(skill)}: no `description`"


@pytest.mark.parametrize("skill", [KNOWLEDGE, KDF], ids=lambda p: p.name)
def test_knowledge_index_links_every_reference(skill):
    """The skill's index links each file under references/, and nothing there that does not exist."""
    text = (skill / "SKILL.md").read_text(encoding="utf-8")
    linked = set(re.findall(r"\]\(references/([^)#\s]+)", text))
    present = {p.name for p in (skill / "references").iterdir() if p.is_file()}
    assert not present - linked, f"{skill.name}/SKILL.md does not link: {sorted(present - linked)}"
    assert not linked - present, f"{skill.name}/SKILL.md links missing files: {sorted(linked - present)}"


def test_data_foundry_index_names_every_script():
    """knowledge-data-foundry's SKILL.md names each script in its scripts section, and no script that does not exist."""
    text = (KDF / "SKILL.md").read_text(encoding="utf-8")
    section = re.search(r"The scripts are in .*?(?=\n## )", text, re.DOTALL).group(0)
    named = set(re.findall(r"`([a-z_]+\.py)`", section))
    present = {p.name for p in (KDF / "scripts").glob("*.py")}
    assert not present - named, f"scripts the index does not name: {sorted(present - named)}"
    assert not named - present, f"the index names scripts that do not exist: {sorted(named - present)}"


def test_probe_library_docstring_names_every_module():
    """The curation_probes package docstring lists each module, and no module that does not exist."""
    package = KNOWLEDGE / "scripts" / "curation_probes"
    doc = re.match(r'"""(.*?)"""', (package / "__init__.py").read_text(encoding="utf-8"), re.DOTALL).group(1)
    named = set(re.findall(r"^\* ``([a-z_]+)``:", doc, re.MULTILINE))
    present = {p.stem for p in package.glob("*.py") if p.stem != "__init__"}
    assert named == present, (
        f"modules not listed: {sorted(present - named)}; listed, missing: {sorted(named - present)}"
    )


# --------------------------------------------------------------------------- the register on the repository
def test_decision_register_runs_on_the_repository():
    """The register reads every record and knowledge file without error and finds the rule IDs it should."""
    script = KDF / "scripts" / "decision_register.py"
    done = subprocess.run(  # noqa: S603 - the repository's own script, run with this interpreter
        [sys.executable, str(script), "--since", "2099-01-01"], cwd=ROOT, capture_output=True, text=True, check=False
    )
    assert done.returncode == 0, done.stderr[-2000:]
    found = re.search(r"Rule IDs defined in the knowledge files: (\d+)", done.stdout)
    assert found, done.stdout[:500]
    assert int(found.group(1)) >= REGISTER_FLOOR, f"only {found.group(1)} rule IDs found, at least {REGISTER_FLOOR}"
