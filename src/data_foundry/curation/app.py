"""Local, single-user web dashboard for editing curation records.

A dependency-light stand-in for the old Google Sheet: a stdlib HTTP server that
serves a single-page Tabulator.js grid and reads/writes the per-dataset markdown
records in place. Each edit rewrites exactly one ``<unique_name>.md`` file, so the
diff a curator commits is minimal and reviewable.

The Guidelines page (``guidelines.html``) renders the markdown files of the two knowledge skills
(:data:`GUIDELINE_SKILLS`) in the browser, read from ``.claude/skills/`` on every request: ``/api/docs``
lists them and ``/docs/<skill>/<path>.md`` returns one file as written, so the page and the skills an
agent reads are the same text. Its first page, "Start here", is ``.claude/skills/README.md`` (the map of
all skills), served as ``/docs/start/README.md`` when the file exists.

Start it with::

    python -m data_foundry.curation.cli serve          # then open http://127.0.0.1:8765

The server is meant to run locally per curator (edit -> git commit -> PR); it is
not hardened for multi-user or public exposure.

Claims come from the live claims board (:mod:`data_foundry.curation.claims`), not from the records: a background
thread fetches the board every :data:`CLAIMS_REFRESH_S` seconds, the records payload shows each record's live holder
in ``claimed_by`` (with the details in ``live_claim``), and editing the Claimed by cell claims (your own name) or
releases (empty) through ``POST /api/claims/<name>``, which also mirrors the claim into the record.
"""

from __future__ import annotations

import json
import os
import re
import threading
import time
from dataclasses import asdict
from functools import partial
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

from data_foundry.curation import claims
from data_foundry.curation._paths import records_dir, resolve_curation_root, skills_dir, vocabularies_path
from data_foundry.curation.notebooks import resolve_notebook
from data_foundry.curation.record import ACCEPTED_SUGGESTIONS, FIELDS, load_vocabularies, save_vocabularies
from data_foundry.curation.store import (
    load_all,
    load_record,
    record_from_dict,
    record_to_dict,
    save_record,
)

STATIC_DIR = Path(__file__).parent / "static"

# Base URL for linking a dataset's curation notebook on GitHub (overridable for forks/branches).
GITHUB_BLOB_BASE: str = os.environ.get(
    "DATA_FOUNDRY_GITHUB_BLOB_BASE", "https://github.com/TabArena/data-foundry/blob/main"
).rstrip("/")

GUIDELINE_SKILLS: dict[str, str] = {
    "knowledge-curation": "Curation knowledge",
    "knowledge-data-foundry": "Data Foundry",
}
"""Skills the Guidelines page (``guidelines.html``) renders: folder under ``.claude/skills`` -> section title."""

START_SECTION: str = "start"
"""Reserved section key of the Guidelines page's first entry, "Start here" (no skill folder has this name)."""
START_TITLE: str = "Start here"
START_DOC: str = f"{START_SECTION}/README.md"
"""Key (and ``/docs/`` URL path) of the Start here page."""
START_REPO_PATH: str = ".claude/skills/README.md"
"""Where the Start here page lives in the repo; its relative links are resolved from here."""

CLAIMS_REFRESH_S: float = 20.0
"""How often the dashboard server fetches the claims board."""

_FRONT_MATTER = re.compile(r"\A﻿?---[ \t]*\r?\n(?:.*?\r?\n)?(?:---|\.\.\.)[ \t]*(?:\r?\n|\Z)", re.DOTALL)
_FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
_H1 = re.compile(r"^ {0,3}#[ \t]+(.+?)(?:[ \t]+#+)?[ \t]*$")


def _schema_payload() -> dict[str, object]:
    return {
        "fields": [
            {"name": f.name, "label": f.label, "kind": f.kind, "vocab": f.vocab_key, "help": f.help} for f in FIELDS
        ],
        "vocabularies": load_vocabularies(),
    }


class _ClaimsPoller:
    """Fetches the claims board every :data:`CLAIMS_REFRESH_S` seconds in a daemon thread; keeps the last error."""

    def __init__(self, interval: float = CLAIMS_REFRESH_S) -> None:
        self.interval = interval
        self.error: str | None = None

    def start(self) -> None:
        """Run the loop in a daemon thread (it dies with the server)."""
        threading.Thread(target=self._loop, name="claims-poller", daemon=True).start()

    def _loop(self) -> None:
        while True:
            try:
                claims.fetch()
                self.error = None
            except claims.ClaimsError as exc:
                self.error = str(exc).splitlines()[0]
            time.sleep(self.interval)


_POLLER: _ClaimsPoller | None = None


def _claims_payload() -> dict[str, object]:
    """The state of the claims board for the page: who you are, when it was fetched, the last error."""
    board = claims.cached_board()
    return {
        "me": claims.configured_curator(),
        "remote": claims.claims_remote(),
        "branch": claims.claims_branch(),
        "tip": board.tip if board else None,
        "fetched_at": board.fetched_at if board else None,
        "count": len(board.claims) if board else 0,
        "error": _POLLER.error if _POLLER is not None else None,
    }


def _overlay_claim(row: dict[str, object], board: claims.Board | None) -> dict[str, object]:
    """Show the live holder in ``claimed_by`` and the claim in ``live_claim``.

    Without a board (none fetched, or no claims branch yet) the row keeps the record's own value.
    """
    if board is None or board.tip is None:
        return row
    claim = board.claims.get(str(row["unique_name"]))
    row["claimed_by"] = claim.holder if claim else None
    row["live_claim"] = {**asdict(claim), "expired": claim.expired()} if claim else None
    return row


def _records_payload(directory: Path | None) -> list[dict[str, object]]:
    """Serialise every record, augmented with read-only *derived* link fields.

    ``notebook_path`` is a real record field, so the pointer a record carries is used as-is; only
    records that have none fall back to :func:`~data_foundry.curation.notebooks.resolve_notebook`
    (a dataset curated but not yet synced). Either way the dataset's notebook gets a
    ``notebook_url`` (GitHub main link), and every record gets ``record_path`` / ``record_url``
    pointing at its own markdown file
    (``curation/records/<name>.md``), so a record can be referenced directly from the UI. The
    ``*_url`` keys are not part of the record schema and are never written back — the
    dashboard's per-row 📓 / 📄 buttons read them (live and on the static site). With a cached
    claims board, ``claimed_by`` is the live holder and ``live_claim`` the claim (:func:`_overlay_claim`).
    """
    repo_root = resolve_curation_root().parent.resolve()
    records_root = (Path(directory) if directory is not None else records_dir()).resolve()
    board = claims.cached_board()
    payload: list[dict[str, object]] = []
    for r in load_all(directory):
        d = _overlay_claim(record_to_dict(r), board)
        rel = r.notebook_path or resolve_notebook(r)
        if rel:
            d["notebook_path"] = rel
            d["notebook_url"] = f"{GITHUB_BLOB_BASE}/{rel}"
        if r.v2_path:
            d["v2_url"] = f"{GITHUB_BLOB_BASE}/{r.v2_path}"
        try:
            rec_rel = (records_root / f"{r.unique_name}.md").relative_to(repo_root).as_posix()
        except ValueError:  # custom records dir outside the repo: no stable GitHub link
            rec_rel = None
        if rec_rel:
            d["record_path"] = rec_rel
            d["record_url"] = f"{GITHUB_BLOB_BASE}/{rec_rel}"
        payload.append(d)
    return payload


def _version_payload(directory: Path | None) -> dict[str, object]:
    """Cheap change token for the records on disk, polled by the dashboard to refresh itself.

    The newest ``mtime_ns`` over the record files and ``vocabularies.yaml``, joined with the
    record count (so a deleted file moves the token even when nothing newer was written). Every
    write path moves it: a dashboard edit from another tab, an agent's ``save_record``, a
    ``git pull``, or a hand edit. One ``scandir`` pass over ~1,300 files, cheap enough to poll.
    """
    target = Path(directory) if directory is not None else records_dir()
    newest = 0
    count = 0
    if target.exists():
        with os.scandir(target) as entries:
            for entry in entries:
                if entry.name.endswith(".md") and not entry.name.startswith("_") and entry.is_file():
                    count += 1
                    newest = max(newest, entry.stat().st_mtime_ns)
    vocab = Path(vocabularies_path())
    if vocab.exists():
        newest = max(newest, vocab.stat().st_mtime_ns)
    board = claims.cached_board()  # a claim pushed by anyone moves the token too
    tip = (board.tip or "none")[:12] if board is not None else "-"
    return {"version": f"{newest}-{count}-{tip}", "records": count}


def start_readme_path() -> Path:
    """The Start here page: ``README.md`` at the top of ``.claude/skills`` (it need not exist)."""
    return skills_dir() / "README.md"


def guideline_doc_files(start_readme: Path | None = None) -> dict[str, Path]:
    """Every markdown file of the Guidelines page, keyed ``<skill>/<path>`` (posix, relative to the skill).

    The first key is :data:`START_DOC` when the Start here README exists; the guideline skills' files
    follow. This map is the whole set of files the server hands out under ``/docs/`` and the static
    build copies: a request is looked up in it and never joined onto the file system, so no path can
    leave the README and the two skill folders. Hidden files and folders are skipped, and so is a file
    that resolves outside its skill folder (a symlink out). The folders are read on every call, so an
    edited or added file shows without a restart.

    Args:
        start_readme: The Start here README (defaults to :func:`start_readme_path`).

    Returns:
        ``{"<skill>/<path>": file}``, the Start here page first.
    """
    root = skills_dir()
    files: dict[str, Path] = {}
    readme = start_readme_path() if start_readme is None else Path(start_readme)
    if readme.is_file():
        files[START_DOC] = readme
    for skill in GUIDELINE_SKILLS:
        skill_dir = root / skill
        if not skill_dir.is_dir():
            continue
        real_dir = skill_dir.resolve()
        for path in sorted(skill_dir.rglob("*.md")):
            rel = path.relative_to(skill_dir)
            if any(part.startswith(".") for part in rel.parts) or not path.is_file():
                continue
            if not path.resolve().is_relative_to(real_dir):
                continue
            files[f"{skill}/{rel.as_posix()}"] = path
    return files


def _first_heading(text: str) -> str | None:
    """The text of a markdown file's first ``# `` heading, outside front matter and code fences."""
    fence: str | None = None
    for line in _FRONT_MATTER.sub("", text, count=1).splitlines():
        opened = _FENCE.match(line)
        if fence is not None:  # inside a fenced block: only its closing fence matters
            if opened and opened.group(1)[0] == fence[0] and len(opened.group(1)) >= len(fence):
                fence = None
            continue
        if opened:
            fence = opened.group(1)
            continue
        match = _H1.match(line)
        if match:
            title = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", match.group(1))  # [text](url) -> text
            return title.replace("`", "").replace("**", "").strip() or None
    return None


def _index_order(index: str, rel: str) -> tuple[bool, bool, int, str]:
    """Sort key: ``SKILL.md`` first, then the files in the order the ``SKILL.md`` text first names them."""
    at = index.find(rel)
    return (rel != "SKILL.md", at < 0, at, rel)


def _docs_payload(files: dict[str, Path] | None = None) -> dict[str, object]:
    """Manifest of the Guidelines page: the sections and, per markdown file, its skill, paths and title.

    When ``files`` holds the Start here README (:data:`START_DOC`), its section and page come first,
    both titled "Start here", with ``repo_path`` :data:`START_REPO_PATH`. Then each skill's ``SKILL.md``,
    titled "Overview"; the other files follow in the order the ``SKILL.md`` first names them (its
    index), then by path. Any other title is the file's first ``# `` heading, else its file name.
    Without the skill folders (a non-editable install) ``docs`` is empty and the page links to the
    files on GitHub instead.

    Args:
        files: The files to describe, as :func:`guideline_doc_files` returns them (read when omitted).

    Returns:
        ``{"github_blob_base", "sections": [{skill, title}], "docs": [{skill, path, repo_path, title, heading}]}``.
    """
    files = guideline_doc_files() if files is None else files
    sections = [{"skill": skill, "title": title} for skill, title in GUIDELINE_SKILLS.items()]
    docs: list[dict[str, object]] = []
    if START_DOC in files:
        sections.insert(0, {"skill": START_SECTION, "title": START_TITLE})
        docs.append(
            {
                "skill": START_SECTION,
                "path": START_DOC.split("/", 1)[1],
                "repo_path": START_REPO_PATH,
                "title": START_TITLE,
                "heading": _first_heading(files[START_DOC].read_text(encoding="utf-8")),
            }
        )
    for skill in GUIDELINE_SKILLS:
        texts = {
            key.split("/", 1)[1]: path.read_text(encoding="utf-8")
            for key, path in files.items()
            if key.split("/", 1)[0] == skill
        }
        for rel in sorted(texts, key=partial(_index_order, texts.get("SKILL.md", ""))):
            heading = _first_heading(texts[rel])
            docs.append(
                {
                    "skill": skill,
                    "path": rel,
                    "repo_path": f".claude/skills/{skill}/{rel}",
                    "title": "Overview" if rel == "SKILL.md" else heading or Path(rel).stem,
                    "heading": heading,
                }
            )
    return {"github_blob_base": GITHUB_BLOB_BASE, "sections": sections, "docs": docs}


class CurationHandler(BaseHTTPRequestHandler):
    """Serves the dashboard SPA and a small JSON API over the records directory."""

    server_version = "DataFoundryCuration/1"

    def __init__(self, *args: object, directory: Path, **kwargs: object) -> None:
        """Bind the records directory this handler reads/writes, then init the base."""
        self._records_dir = directory
        super().__init__(*args, **kwargs)  # type: ignore[arg-type]

    # -- helpers ---------------------------------------------------------
    def _send_json(self, payload: object, status: int = 200) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_file(self, path: Path, content_type: str) -> None:
        body = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_doc(self, key: str) -> None:
        """Send one Guidelines markdown file by its ``<skill>/<path>`` key (or :data:`START_DOC`); else a 404."""
        path = guideline_doc_files().get(key)
        if path is None:
            self._send_json({"error": "not found"}, status=404)
            return
        self._send_file(path, "text/markdown; charset=utf-8")

    def _read_json_body(self) -> dict[str, object]:
        length = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(length) or b"{}")

    def log_message(self, *args: object) -> None:
        """Silence the default per-request stderr logging."""

    # -- routing ---------------------------------------------------------
    def do_GET(self) -> None:
        """Serve the SPA, the schema, the records list, the on-disk change token, or the guideline docs."""
        route = urlparse(self.path).path
        try:
            if route in ("/", "/index.html"):
                self._send_file(STATIC_DIR / "index.html", "text/html; charset=utf-8")
            elif route == "/guidelines.html":
                self._send_file(STATIC_DIR / "guidelines.html", "text/html; charset=utf-8")
            elif route == "/api/schema":
                self._send_json(_schema_payload())
            elif route == "/api/records":
                self._send_json(_records_payload(self._records_dir))
            elif route == "/api/version":
                self._send_json(_version_payload(self._records_dir))
            elif route == "/api/docs":
                self._send_json(_docs_payload())
            elif route == "/api/claims":
                self._send_json(_claims_payload())
            elif route.startswith("/docs/"):
                self._send_doc(unquote(route[len("/docs/") :]))
            else:
                self._send_json({"error": "not found"}, status=404)
        except Exception as exc:  # noqa: BLE001 - surface any error to the client
            self._send_json({"error": str(exc)}, status=500)

    def do_PUT(self) -> None:
        """Apply a partial update to one record and rewrite its file."""
        route = urlparse(self.path).path
        try:
            if route.startswith("/api/records/"):
                unique_name = unquote(route[len("/api/records/") :])
                self._update_record(unique_name)
            else:
                self._send_json({"error": "not found"}, status=404)
        except Exception as exc:  # noqa: BLE001
            self._send_json({"error": str(exc)}, status=500)

    def do_POST(self) -> None:
        """Add a new dropdown option to the vocabulary file, or claim / release a dataset."""
        route = urlparse(self.path).path
        try:
            if route == "/api/vocab":
                self._add_vocab_option()
            elif route.startswith("/api/claims/"):
                self._claim_action(unquote(route[len("/api/claims/") :]))
            else:
                self._send_json({"error": "not found"}, status=404)
        except Exception as exc:  # noqa: BLE001
            self._send_json({"error": str(exc)}, status=500)

    # -- handlers --------------------------------------------------------
    def _update_record(self, unique_name: str) -> None:
        patch = self._read_json_body()
        index = {r.unique_name: r for r in load_all(self._records_dir)}
        if unique_name not in index:
            self._send_json({"error": f"unknown record: {unique_name}"}, status=404)
            return
        merged = record_to_dict(index[unique_name])
        merged.update(patch)
        merged.pop("unique_name", None)  # renaming is out of scope for the grid
        merged["unique_name"] = unique_name
        record = record_from_dict(merged)
        record.needs_review = record.review_reasons(load_vocabularies())
        save_record(record, self._records_dir)
        self._send_json(record_to_dict(record))

    def _claim_action(self, unique_name: str) -> None:
        """Claim (``{"action": "claim"}``) or release a dataset on the board, mirror it into the record, return the row.

        The stage follows the record: ``add`` for an accepted dataset, else ``triage``. A dataset another curator
        holds, a missing curator name or an unreachable remote answer 409 with the reason.
        """
        body = self._read_json_body()
        path = Path(self._records_dir) / f"{unique_name}.md"
        if not path.exists():
            self._send_json({"error": f"unknown record: {unique_name}"}, status=404)
            return
        action = body.get("action")
        try:
            if action == "claim":
                stage = "add" if load_record(path).suggestion in ACCEPTED_SUGGESTIONS else "triage"
                outcome = claims.claim([unique_name], stage=stage, note=str(body.get("note") or ""))
            elif action == "release":
                outcome = claims.release([unique_name])
            else:
                self._send_json({"error": "action must be claim or release"}, status=400)
                return
        except claims.ClaimsError as exc:
            self._send_json({"error": str(exc)}, status=409)
            return
        if unique_name in outcome.skipped:
            self._send_json({"error": f"{unique_name}: {outcome.skipped[unique_name]}"}, status=409)
            return
        claims.mirror_to_records(outcome.board, [unique_name], self._records_dir)
        self._send_json(_overlay_claim(record_to_dict(load_record(path)), outcome.board))

    def _add_vocab_option(self) -> None:
        body = self._read_json_body()
        field, value = body.get("field"), body.get("value")
        if not field or not value:
            self._send_json({"error": "field and value are required"}, status=400)
            return
        vocab = load_vocabularies()
        values = vocab.setdefault(str(field), [])
        if value not in values:
            values.append(str(value))
            save_vocabularies(vocab, vocabularies_path())
        self._send_json({"field": field, "values": values})


def serve(host: str = "127.0.0.1", port: int = 8765, directory: str | Path | None = None) -> None:
    """Run the dashboard server until interrupted."""
    global _POLLER  # noqa: PLW0603 - one poller per server process
    target = Path(directory) if directory is not None else records_dir()
    _POLLER = _ClaimsPoller()
    _POLLER.start()
    handler = partial(CurationHandler, directory=target)
    httpd = ThreadingHTTPServer((host, port), handler)
    n = len([p for p in target.glob("*.md") if not p.name.startswith("_")]) if target.exists() else 0
    print(f"Curation dashboard: http://{host}:{port}  ({n} records in {target})")
    print("Press Ctrl+C to stop.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        httpd.server_close()
