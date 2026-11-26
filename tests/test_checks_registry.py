"""The registry of check slugs (``data_foundry.checks.registry``) against the code that emits them."""

from __future__ import annotations

import ast
import re
from collections import defaultdict
from pathlib import Path

import pytest

from data_foundry.checks import registry
from data_foundry.checks.registry import ACCEPTABLE_ERRORS, CHECKS, may_accept

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "src" / "data_foundry"
SLUG_PAGE = ROOT / ".claude" / "skills" / "knowledge-data-foundry" / "references" / "check_slugs.md"
SEVERITIES = {"error", "warning", "info"}


def _severities(node: ast.AST | None) -> set[str] | None:
    """The severities a ``severity`` argument can take, or None when the code computes it."""
    if isinstance(node, ast.Constant) and node.value in SEVERITIES:
        return {node.value}
    if isinstance(node, ast.IfExp):
        body, orelse = _severities(node.body), _severities(node.orelse)
        return body | orelse if body is not None and orelse is not None else None
    return None


def _emitted() -> tuple[dict[str, list[set[str] | None]], set[str]]:
    """Every slug the code can emit, with the severities of each place, found by reading the source.

    A slug is the first argument of a ``CheckResult(...)`` call, or the first item of a ``(slug, severity, message)``
    tuple (the time basis's problems). An f-string slug (``f"task_{field_name}_dtype"``) expands to every string
    constant of its function in the placeholder's place.
    """
    found: dict[str, list[set[str] | None]] = defaultdict(list)
    expanded: set[str] = set()
    for path in sorted(SOURCE.rglob("*.py")):
        tree = ast.parse(path.read_text())
        functions = [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
        for node in ast.walk(tree):
            if isinstance(node, ast.Tuple) and len(node.elts) >= 3:
                slug, severity = node.elts[0], node.elts[1]
                is_slug = isinstance(slug, ast.Constant) and re.fullmatch(r"[a-z]+(_[a-z0-9]+)+", str(slug.value))
                if is_slug and _severities(severity):
                    found[slug.value].append(_severities(severity))
            if not isinstance(node, ast.Call):
                continue
            func = node.func
            name = func.id if isinstance(func, ast.Name) else getattr(func, "attr", None)
            if name != "CheckResult" or not node.args:
                continue
            slug = node.args[0]
            severity = _severities(node.args[1]) if len(node.args) > 1 else None
            if isinstance(slug, ast.Constant):
                found[slug.value].append(severity)
            elif isinstance(slug, ast.JoinedStr):
                pattern = "".join(re.escape(v.value) if isinstance(v, ast.Constant) else "(.+)" for v in slug.values)
                owner = next(f for f in functions if f.lineno <= node.lineno <= f.end_lineno)
                words = {n.value for n in ast.walk(owner) if isinstance(n, ast.Constant) and isinstance(n.value, str)}
                hits = {s for s in CHECKS if (m := re.fullmatch(pattern, s)) and all(g in words for g in m.groups())}
                assert hits, f"{path.name}:{node.lineno}: no registered slug matches {pattern!r}"
                for hit in hits:
                    found[hit].append(severity)
                expanded |= hits
            # a slug held in a variable comes from one of the tuples above
    return dict(found), expanded


EMITTED, EXPANDED = _emitted()


def test_every_emitted_slug_is_registered() -> None:
    assert sorted(set(EMITTED) - set(CHECKS)) == []


def test_every_registered_slug_is_emitted() -> None:
    assert sorted(set(CHECKS) - set(EMITTED)) == []


@pytest.mark.parametrize("slug", sorted(EMITTED))
def test_the_registered_severities_are_those_the_code_emits(slug: str) -> None:
    places = EMITTED[slug]
    known = set().union(*(p for p in places if p is not None))
    registered = set(CHECKS[slug].severities)
    assert known <= registered
    if all(p is not None for p in places):
        assert known == registered


def test_errors_are_acceptable_only_on_purpose() -> None:
    assert may_accept("dataset_constant_column", "warning")
    assert may_accept("splits_rows_unused", "warning")
    assert not may_accept("splits_rows_unused", "error")
    assert may_accept("splits_test_too_small", "error")
    assert not CHECKS["splits_train_under_floor"].acceptable
    assert CHECKS["splits_test_class_missing"].acceptable  # its warning
    assert all(CHECKS[slug].accepted_error for slug in ACCEPTABLE_ERRORS)


def test_every_accepted_slug_of_a_definition_is_acceptable() -> None:
    """``accepted_check_warnings`` of every definition names a slug a definition may accept (or a retired one, which
    the check run reports as ``accepted_check_warnings_unused``).
    """
    refused = []
    for path in sorted((ROOT / "datasets").rglob("dataset.py")):
        for node in ast.walk(ast.parse(path.read_text())):
            targets = node.targets if isinstance(node, ast.Assign) else [getattr(node, "target", None)]
            if not any(isinstance(t, ast.Name) and t.id == "accepted_check_warnings" for t in targets):
                continue
            for key in getattr(node.value, "keys", []):
                check = CHECKS.get(key.value)
                if check is not None and not check.acceptable:
                    refused.append(f"{path.parent.name}: {key.value}")
    assert refused == []


def test_the_slug_page_is_current() -> None:
    assert SLUG_PAGE.read_text() == registry.markdown(), (
        "Regenerate it: .venv/bin/python -m data_foundry.checks.registry > "
        ".claude/skills/knowledge-data-foundry/references/check_slugs.md"
    )
