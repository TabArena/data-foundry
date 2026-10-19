"""Local, single-user web dashboard for editing curation records.

A dependency-light stand-in for the old Google Sheet: a stdlib HTTP server that
serves a single-page Tabulator.js grid and reads/writes the per-dataset markdown
records in place. Each edit rewrites exactly one ``<unique_name>.md`` file, so the
diff a curator commits is minimal and reviewable.

The Guidelines page (``guidelines.html``) renders the markdown files of the two knowledge skills
(:data:`GUIDELINE_SKILLS`) in the browser, read from ``.claude/skills/`` on every request: ``/api/docs``
lists them and ``/docs/<skill>/<path>.md`` returns one file as written, so the page and the skills an
agent reads are the same text.

Start it with::

    python -m data_foundry.curation.cli serve          # then open http://127.0.0.1:8765

The server is meant to run locally per curator (edit -> git commit -> PR); it is
not hardened for multi-user or public exposure.
"""

from __future__ import annotations

import json
import os
import re
from functools import partial
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

from data_foundry.curation._paths import records_dir, resolve_curation_root, skills_dir, vocabularies_path
from data_foundry.curation.notebooks import resolve_notebook
from data_foundry.curation.record import FIELDS, load_vocabularies, save_vocabularies
from data_foundry.curation.store import (
    load_all,
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


def _records_payload(directory: Path | None) -> list[dict[str, object]]:
    """Serialise every record, augmented with read-only *derived* link fields.

    ``notebook_path`` is a real record field, so the pointer a record carries is used as-is; only
    records that have none fall back to :func:`~data_foundry.curation.notebooks.resolve_notebook`
    (a dataset curated but not yet synced). Either way the dataset's notebook gets a
    ``notebook_url`` (GitHub main link), and every record gets ``record_path`` / ``record_url``
    pointing at its own markdown file
    (``curation/records/<name>.md``), so a record can be referenced directly from the UI. The
    ``*_url`` keys are not part of the record schema and are never written back — the
    dashboard's per-row 📓 / 📄 buttons read them (live and on the static site).
    """
    repo_root = resolve_curation_root().parent.resolve()
    records_root = (Path(directory) if directory is not None else records_dir()).resolve()
    payload: list[dict[str, object]] = []
    for r in load_all(directory):
        d = record_to_dict(r)
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
    return {"version": f"{newest}-{count}", "records": count}


def guideline_doc_files() -> dict[str, Path]:
    """Every markdown file of the guideline skills, keyed ``<skill>/<path>`` (posix, relative to the skill).

    This map is the whole set of files the server hands out under ``/docs/`` and the static build
    copies: a request is looked up in it and never joined onto the file system, so no path can
    leave the two skill folders. Hidden files and folders are skipped, and so is a file that
    resolves outside its skill folder (a symlink out). The folders are read on every call, so an
    edited or added file shows without a restart.
    """
    root = skills_dir()
    files: dict[str, Path] = {}
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

    Each skill's ``SKILL.md`` comes first, titled "Overview"; the other files follow in the order
    the ``SKILL.md`` first names them (its index), then by path. Any other title is the file's
    first ``# `` heading, else its file name. Without the skill folders (a non-editable install)
    ``docs`` is empty and the page links to the files on GitHub instead.

    Args:
        files: The files to describe, as :func:`guideline_doc_files` returns them (read when omitted).

    Returns:
        ``{"github_blob_base", "sections": [{skill, title}], "docs": [{skill, path, repo_path, title, heading}]}``.
    """
    files = guideline_doc_files() if files is None else files
    docs: list[dict[str, object]] = []
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
    return {
        "github_blob_base": GITHUB_BLOB_BASE,
        "sections": [{"skill": skill, "title": title} for skill, title in GUIDELINE_SKILLS.items()],
        "docs": docs,
    }


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
        """Send one guideline markdown file by its ``<skill>/<path>`` key; any other path is a 404."""
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
        """Add a new dropdown option to the vocabulary file."""
        route = urlparse(self.path).path
        try:
            if route == "/api/vocab":
                self._add_vocab_option()
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
    target = Path(directory) if directory is not None else records_dir()
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
