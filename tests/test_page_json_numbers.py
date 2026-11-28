"""Every JSON a page reads holds only integers a JavaScript number keeps exactly.

A browser parses a JSON number into a double, which keeps 53 bits: an integer above 2**53 comes back rounded. The
dashboard sent each record's ``mtime_ns`` (about 1.8e18) as a number and compared it on the way back, so 2,104 of the
2,109 records looked changed and almost every edit was refused (fixed 2026-11-27 by sending it as a string). These
tests build every payload and page the repository serves and walk their JSON for such integers.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest

from data_foundry.curation.app import (
    _claims_payload,
    _docs_payload,
    _records_changed_payload,
    _records_payload,
    _schema_payload,
    _version_payload,
)
from data_foundry.curation.record import CurationRecord
from data_foundry.curation.site import build_site
from data_foundry.curation.store import save_record

REPO = Path(__file__).resolve().parents[1]
SAFE = 2**53 - 1
"""The largest integer a JavaScript number holds exactly (``Number.MAX_SAFE_INTEGER``)."""


def unsafe_integers(value: Any, path: str = "$") -> list[str]:
    """The JSON paths of the integers in ``value`` that a JavaScript number would round."""
    if isinstance(value, bool):
        return []
    if isinstance(value, int):
        return [f"{path} = {value}"] if abs(value) > SAFE else []
    if isinstance(value, dict):
        return [hit for k, v in value.items() for hit in unsafe_integers(v, f"{path}.{k}")]
    if isinstance(value, list):
        return [hit for i, v in enumerate(value) for hit in unsafe_integers(v, f"{path}[{i}]")]
    return []


def test_the_walk_finds_an_integer_javascript_rounds() -> None:
    assert unsafe_integers({"a": [1, {"mtime": 1_795_686_619_839_148_732}], "b": True, "c": 2.5e300}) == [
        "$.a[1].mtime = 1795686619839148732"
    ]
    assert unsafe_integers({"count": SAFE, "neg": -SAFE}) == []


@pytest.fixture
def records(tmp_path: Path) -> Path:
    """Two record files with real modification times (nanoseconds since 1970, far above 2**53)."""
    folder = tmp_path / "records"
    for name in ("musk", "credit_g"):
        save_record(CurationRecord(unique_name=name, name=name, comments="A note.", priority=3), folder)
    return folder


def test_the_dashboard_payloads_hold_no_unsafe_integer(records: Path) -> None:
    """``/api/records`` (and its catch-up), ``/api/version``, ``/api/schema``, ``/api/docs`` and ``/api/claims``."""
    payloads = {
        "records": _records_payload(records),
        "catch-up": _records_changed_payload(records, 0, "an-older-tip"),
        "version": _version_payload(records),
        "schema": _schema_payload(),
        "docs": _docs_payload(),
        "claims": _claims_payload(),
    }
    hits = {name: unsafe_integers(json.loads(json.dumps(p))) for name, p in payloads.items()}
    assert not any(hits.values()), hits


def test_the_static_site_holds_no_unsafe_integer(records: Path, tmp_path: Path) -> None:
    out = build_site(tmp_path / "site", records)
    files = sorted(out.rglob("*.json"))
    assert files
    hits = {f.name: unsafe_integers(json.loads(f.read_text())) for f in files}
    assert not any(hits.values()), hits


def _run(script: str, *args: str) -> None:
    subprocess.run(  # noqa: S603 - a script of this repository, run with this interpreter
        [sys.executable, str(REPO / script), *args], check=True, capture_output=True, text=True, cwd=REPO
    )


def test_the_review_page_data_holds_no_unsafe_integer(tmp_path: Path) -> None:
    """The review page of /review-added-datasets, built from three of the repository's records."""
    out = tmp_path / "review"
    _run(
        ".claude/skills/review-added-datasets/scripts/review_page.py",
        "build", "--names", "credit_g,diamonds,apistox", "--keep-settled", "--out", str(out),
    )  # fmt: skip
    files = sorted(out.rglob("*.json"))
    assert files
    hits = {f.name: unsafe_integers(json.loads(f.read_text())) for f in files}
    assert not any(hits.values()), hits


def test_the_split_tree_page_data_holds_no_unsafe_integer(tmp_path: Path) -> None:
    out = tmp_path / "tree"
    _run(
        ".claude/skills/review-split-tree/scripts/build_tree_page.py",
        "--tree", ".claude/skills/knowledge-curation/references/split_tree.md", "--out", str(out),
    )  # fmt: skip
    files = sorted(out.rglob("*.json"))
    assert files
    hits = {f.name: unsafe_integers(json.loads(f.read_text())) for f in files}
    assert not any(hits.values()), hits
