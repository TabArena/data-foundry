"""Compile the curation backlog into a self-contained, read-only static site.

Git stays the source of truth; :func:`build_site` freezes the read endpoints the
local dashboard serves (``/api/schema``, ``/api/records`` and ``/api/docs``) into
static JSON next to a read-only copy of the single-page app. The result is a
folder any static host (GitHub Pages, Netlify, S3, ...) can serve with no Python
process: view, search, sort, filter, and pin all run in the browser, and every
editing path is disabled.

The app HTML is the *same* ``static/index.html`` the live dashboard uses; the
build only injects ``window.DF_STATIC = true`` ahead of it, which the SPA reads
to point its fetches at the sibling JSON files and drop all write affordances.
This keeps a single source of truth for the page and avoids drift. The
Guidelines page (``guidelines.html``) gets the same flag and reads
``docs/manifest.json`` plus the knowledge skills' markdown files, copied to the
``docs/<skill>/<path>.md`` URLs the live server answers, and the Start here page
(``.claude/skills/README.md``) as ``docs/start/README.md``.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

from data_foundry.curation._paths import records_dir
from data_foundry.curation.app import (
    STATIC_DIR,
    _claims_payload,
    _docs_payload,
    _records_payload,
    _schema_payload,
    guideline_doc_files,
)

# Injected just before </head> so the flag is set before the page's own script runs.
_STATIC_FLAG = "<script>window.DF_STATIC = true;</script>\n</head>"


def build_site(
    out_dir: str | Path, directory: str | Path | None = None, *, start_readme: str | Path | None = None
) -> Path:
    """Write a read-only static site.

    The site is ``index.html`` + ``schema.json`` + ``records.json`` (with the claims of the cached claims board,
    see :func:`~data_foundry.curation.app._records_payload`) + ``claims.json`` for the grid, the other
    static pages (``guidelines.html``), and ``docs/manifest.json`` with a copy of every
    guideline markdown file under ``docs/<skill>/<path>.md`` (the Start here README as
    ``docs/start/README.md``).

    Args:
        out_dir: Destination directory; created if missing. Existing pages, ``*.json`` and
            ``docs/`` files of the same name in it are overwritten (nothing is deleted).
        directory: Records directory to snapshot (defaults to the standard one).
        start_readme: The Start here README (defaults to ``.claude/skills/README.md``); a missing
            file leaves the page out.

    Returns:
        The output directory path.
    """
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    records = records_dir() if directory is None else Path(directory)
    _write_json(out / "schema.json", _schema_payload())
    _write_json(out / "records.json", _records_payload(records))
    _write_json(out / "claims.json", _claims_payload())  # the board the records' Claimed by column shows

    # Every page gets the read-only flag: index.html drops its write affordances, guidelines.html reads
    # the frozen docs/manifest.json. Cross-links between the pages are relative, so they resolve whether
    # served at the site root or under a Pages subpath.
    for page in STATIC_DIR.glob("*.html"):
        html = page.read_text(encoding="utf-8")
        if "</head>" not in html:  # pragma: no cover - guards against template drift
            raise ValueError(f"static/{page.name} has no </head> to inject the read-only flag before.")
        (out / page.name).write_text(html.replace("</head>", _STATIC_FLAG, 1), encoding="utf-8")

    # The guideline docs: one manifest and the markdown files it lists, at the same relative URLs
    # (docs/<skill>/<path>.md) the live server answers.
    files = guideline_doc_files(Path(start_readme) if start_readme is not None else None)
    docs = out / "docs"
    docs.mkdir(exist_ok=True)
    for key, path in files.items():
        target = docs / key
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
    _write_json(docs / "manifest.json", _docs_payload(files))
    return out


def _write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
