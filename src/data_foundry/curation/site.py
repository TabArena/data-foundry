"""Compile the curation backlog into a self-contained, read-only static site.

Git stays the source of truth; :func:`build_site` freezes the two read endpoints
the local dashboard serves (``/api/schema`` and ``/api/records``) into static
JSON next to a read-only copy of the single-page app. The result is a folder any
static host (GitHub Pages, Netlify, S3, ...) can serve with no Python process:
view, search, sort, filter, and pin all run in the browser, and every editing
path is disabled.

The app HTML is the *same* ``static/index.html`` the live dashboard uses; the
build only injects ``window.DF_STATIC = true`` ahead of it, which the SPA reads
to point its fetches at the sibling JSON files and drop all write affordances.
This keeps a single source of truth for the page and avoids drift.
"""

from __future__ import annotations

import json
from pathlib import Path

from data_foundry.curation._paths import records_dir
from data_foundry.curation.app import STATIC_DIR, _records_payload, _schema_payload

# Injected just before </head> so the flag is set before the SPA's own script runs.
_STATIC_FLAG = "<script>window.DF_STATIC = true;</script>\n</head>"


def build_site(out_dir: str | Path, directory: str | Path | None = None) -> Path:
    """Write a read-only static site (``index.html`` + ``schema.json`` + ``records.json``).

    Args:
        out_dir: Destination directory; created if missing. Existing
            ``index.html`` / ``*.json`` in it are overwritten.
        directory: Records directory to snapshot (defaults to the standard one).

    Returns:
        The output directory path.
    """
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    records = records_dir() if directory is None else Path(directory)
    _write_json(out / "schema.json", _schema_payload())
    _write_json(out / "records.json", _records_payload(records))

    html = (STATIC_DIR / "index.html").read_text(encoding="utf-8")
    if "</head>" not in html:  # pragma: no cover - guards against template drift
        raise ValueError("static/index.html has no </head> to inject the read-only flag before.")
    html = html.replace("</head>", _STATIC_FLAG, 1)
    (out / "index.html").write_text(html, encoding="utf-8")

    # Copy auxiliary static pages (e.g. guidelines.html) verbatim; only index.html
    # gets the read-only flag. Their cross-links to the grid are relative, so they
    # resolve correctly whether served at the site root or under a Pages subpath.
    for page in STATIC_DIR.glob("*.html"):
        if page.name != "index.html":
            (out / page.name).write_text(page.read_text(encoding="utf-8"), encoding="utf-8")
    return out


def _write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
