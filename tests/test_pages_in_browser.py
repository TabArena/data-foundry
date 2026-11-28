"""The repository's pages in a real browser: they load without errors and their flows work.

Two dashboard bugs passed every Python test and showed only in a browser (2026-11-27): an edit check that compared a
rounded JavaScript number, and a refresh that only deleted a row and stopped because Tabulator refuses an empty
update. These tests drive the pages in headless Chromium through Playwright.

They need ``pip install playwright`` and ``playwright install chromium`` (the ``pages in a browser`` CI job does both)
and skip otherwise, unless ``DATA_FOUNDRY_REQUIRE_BROWSER=1`` makes a missing browser a failure. A local Chromium
build can be named with ``DATA_FOUNDRY_CHROMIUM``.
"""

from __future__ import annotations

import os
import subprocess
import sys
import threading
from collections.abc import Iterator
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest

from data_foundry.curation.app import CurationHandler
from data_foundry.curation.record import CurationRecord
from data_foundry.curation.site import build_site
from data_foundry.curation.store import save_record

REPO = Path(__file__).resolve().parents[1]
REQUIRED = os.environ.get("DATA_FOUNDRY_REQUIRE_BROWSER") == "1"


def _unavailable(reason: str) -> None:
    if REQUIRED:
        pytest.fail(f"DATA_FOUNDRY_REQUIRE_BROWSER=1 but {reason}")
    pytest.skip(reason)


@pytest.fixture(scope="module")
def browser() -> Iterator[object]:
    try:
        from playwright.sync_api import sync_playwright  # optional: only these tests need it
    except ImportError:
        _unavailable("playwright is not installed")
    with sync_playwright() as p:
        try:
            chromium = p.chromium.launch(executable_path=os.environ.get("DATA_FOUNDRY_CHROMIUM"), args=["--no-sandbox"])
        except Exception as error:  # noqa: BLE001 - any launch failure means no browser here
            _unavailable(f"Chromium does not start: {str(error)[:200]}")
        yield chromium
        chromium.close()


def _serve(handler: object) -> Iterator[str]:
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=httpd.serve_forever, kwargs={"poll_interval": 0.05}, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{httpd.server_address[1]}"
    finally:
        httpd.shutdown()
        httpd.server_close()


class _Quiet(SimpleHTTPRequestHandler):
    def log_message(self, *args: object) -> None:
        """Silence the per-request log."""


def _open(browser: object, url: str, ready: str) -> tuple[object, list[str]]:
    """A page at ``url`` once ``ready`` (a JavaScript expression) holds, and the list its errors go to."""
    page = browser.new_page()
    errors: list[str] = []
    page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
    page.on("pageerror", lambda e: errors.append(f"page error: {e}"))
    page.on("response", lambda r: errors.append(f"{r.status} {r.url}") if r.status >= 400 else None)
    page.goto(url)
    page.wait_for_function(ready, timeout=60_000)
    return page, errors


@pytest.fixture
def records(tmp_path: Path) -> Path:
    folder = tmp_path / "records"
    for i, name in enumerate(("musk", "credit_g", "diamonds", "apistox")):
        save_record(CurationRecord(unique_name=name, name=name, comments=f"Note {i}.", priority=1 + i % 5), folder)
    return folder


def test_the_dashboard_catches_up_and_saves(browser: object, records: Path) -> None:
    """An outside write shows, a deleted record leaves the table, and an edit through the page is saved."""
    for base in _serve(partial(CurationHandler, directory=records)):
        page, errors = _open(browser, base + "/", "typeof table !== 'undefined' && table.getDataCount() === 4")

        save_record(
            CurationRecord(unique_name="musk", name="musk", comments="Written by an agent.", priority=1), records
        )
        page.wait_for_function("(table.getRow('musk').getData().comments || '').includes('agent')", timeout=20_000)

        (records / "diamonds.md").unlink()
        page.wait_for_function("!table.getRow('diamonds')", timeout=20_000)

        saved = page.evaluate("putRecord('credit_g', {priority: 5}).then(d => d.priority).catch(e => e.message)")
        assert saved == 5, saved
        assert "priority: 5" in (records / "credit_g.md").read_text()
        page.wait_for_timeout(500)
        assert not errors, errors


def test_the_static_site_renders_and_searches(browser: object, records: Path, tmp_path: Path) -> None:
    site = build_site(tmp_path / "site", records)
    for base in _serve(partial(_Quiet, directory=str(site))):
        page, errors = _open(
            browser, base + "/index.html", "typeof table !== 'undefined' && table.getDataCount() === 4"
        )
        page.fill("#search", "diamonds")
        page.wait_for_function("table.getDataCount('active') === 1", timeout=10_000)
        _, more = _open(browser, base + "/guidelines.html", "document.body.innerText.length > 200")
        assert not errors + more, errors + more


def _built_page(tmp_path: Path, script: str, *args: str) -> Path:
    out = tmp_path / "page"
    subprocess.run(  # noqa: S603 - a script of this repository, run with this interpreter
        [sys.executable, str(REPO / script), *args, "--out", str(out)], check=True, capture_output=True, cwd=REPO
    )
    return out


def test_the_review_page_renders(browser: object, tmp_path: Path) -> None:
    out = _built_page(
        tmp_path, ".claude/skills/review-added-datasets/scripts/review_page.py",
        "build", "--names", "credit_g,diamonds,apistox", "--keep-settled",
    )  # fmt: skip
    for base in _serve(partial(_Quiet, directory=str(out))):
        page, errors = _open(browser, base + "/review_page.html", "document.body.innerText.includes('credit_g')")
        page.wait_for_timeout(500)
        assert not errors, errors


def test_the_split_tree_page_renders(browser: object, tmp_path: Path) -> None:
    out = _built_page(
        tmp_path, ".claude/skills/review-split-tree/scripts/build_tree_page.py",
        "--tree", ".claude/skills/knowledge-curation/references/split_tree.md",
    )  # fmt: skip
    (page_file,) = out.glob("*.html")
    for base in _serve(partial(_Quiet, directory=str(out))):
        page, errors = _open(browser, f"{base}/{page_file.name}", "document.body.innerText.length > 300")
        page.wait_for_timeout(500)
        assert not errors, errors
