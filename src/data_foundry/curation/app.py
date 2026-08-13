"""Local, single-user web dashboard for editing curation records.

A dependency-light stand-in for the old Google Sheet: a stdlib HTTP server that
serves a single-page Tabulator.js grid and reads/writes the per-dataset markdown
records in place. Each edit rewrites exactly one ``<unique_name>.md`` file, so the
diff a curator commits is minimal and reviewable.

Start it with::

    python -m data_foundry.curation.cli serve          # then open http://127.0.0.1:8765

The server is meant to run locally per curator (edit -> git commit -> PR); it is
not hardened for multi-user or public exposure.
"""

from __future__ import annotations

import json
import os
from functools import lru_cache, partial
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

from data_foundry.curation._paths import records_dir, resolve_curation_root, vocabularies_path
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


def _notebook_rank(rel: Path) -> tuple[int, str]:
    """Sort key that prefers a shipped dataset's notebook over its scratch copies.

    The same ``<name>/<name>.ipynb`` often exists several times: once in the shipped
    collection (``datasets/beyond_iid/...``) and once more in a working or retired tree
    (``datasets/_dev/...``, ``datasets/_maintenance/...``). Underscore-prefixed directories
    mark those non-shipped trees, so fewer of them wins; the path itself breaks ties so the
    index does not depend on filesystem walk order.
    """
    parts = rel.parts[:-1]
    return (sum(p.startswith("_") for p in parts), rel.as_posix())


@lru_cache(maxsize=8)
def _notebook_index(datasets_dir: str) -> dict[str, str]:
    """Map a dataset ``unique_name`` -> its repo-relative curation-notebook path.

    Only the canonical per-dataset notebook counts: ``datasets/**/<name>/<name>.ipynb``
    (the layout ``/process-dataset`` scaffolds). Where a name has more than one such
    notebook, :func:`_notebook_rank` picks the shipped one. Cached because the datasets tree
    is large and static for the lifetime of a serve/build.
    """
    base = Path(datasets_dir)
    if not base.exists():
        return {}
    repo_root = base.parent
    candidates: dict[str, Path] = {}
    for nb in base.rglob("*.ipynb"):
        if nb.parent.name != nb.stem:  # canonical <name>/<name>.ipynb only
            continue
        rel = nb.relative_to(repo_root)
        best = candidates.get(nb.stem)
        if best is None or _notebook_rank(rel) < _notebook_rank(best):
            candidates[nb.stem] = rel
    return {name: rel.as_posix() for name, rel in candidates.items()}


def _schema_payload() -> dict[str, object]:
    return {
        "fields": [
            {"name": f.name, "label": f.label, "kind": f.kind, "vocab": f.vocab_key, "help": f.help} for f in FIELDS
        ],
        "vocabularies": load_vocabularies(),
    }


def _records_payload(directory: Path | None) -> list[dict[str, object]]:
    """Serialise every record, augmented with read-only *derived* link fields.

    Datasets with a curation notebook get ``notebook_path`` (repo-relative) and
    ``notebook_url`` (GitHub main link); every record additionally gets ``record_path`` /
    ``record_url`` pointing at its own markdown file (``curation/records/<name>.md``),
    so a record can be referenced directly from the UI. None of these are part of the
    record schema and they are never written back — the dashboard's per-row 📓 / 📄
    buttons read them (live and on the static site).
    """
    repo_root = resolve_curation_root().parent.resolve()
    records_root = (Path(directory) if directory is not None else records_dir()).resolve()
    notebooks = _notebook_index(str(resolve_curation_root().parent / "datasets"))
    payload: list[dict[str, object]] = []
    for r in load_all(directory):
        d = record_to_dict(r)
        rel = notebooks.get(r.unique_name)
        if rel:
            d["notebook_path"] = rel
            d["notebook_url"] = f"{GITHUB_BLOB_BASE}/{rel}"
        try:
            rec_rel = (records_root / f"{r.unique_name}.md").relative_to(repo_root).as_posix()
        except ValueError:  # custom records dir outside the repo: no stable GitHub link
            rec_rel = None
        if rec_rel:
            d["record_path"] = rec_rel
            d["record_url"] = f"{GITHUB_BLOB_BASE}/{rec_rel}"
        payload.append(d)
    return payload


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

    def _read_json_body(self) -> dict[str, object]:
        length = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(length) or b"{}")

    def log_message(self, *args: object) -> None:
        """Silence the default per-request stderr logging."""

    # -- routing ---------------------------------------------------------
    def do_GET(self) -> None:
        """Serve the SPA, the schema, or the records list."""
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
