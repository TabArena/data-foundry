"""The minimal input set of a rebuild: a symlinked warehouse to verify it, or a zip with a manifest to back it up.

Usage, from the repository root::

    .venv/bin/python .claude/skills/rebuild-working-copy/scripts/minimal_inputs.py <out_dir> links <warehouse_dir>
    .venv/bin/python .claude/skills/rebuild-working-copy/scripts/minimal_inputs.py <out_dir> zip <out.zip>

``<out_dir>`` is a full ``build_all.py`` run: the inputs are the files each build read (``read``) plus what the
``_prepare_raw_files`` steps read (``prepare_read``), so the prepared files can be regenerated from the archive too.

``links`` builds a warehouse of symlinks to those files; a check-only run against it (``DATA_FOUNDRY_WAREHOUSE``
pointing at it) shows that they suffice. ``zip`` writes them under ``local-data-warehouse/`` with ``MANIFEST.tsv``
(path, bytes, SHA-256, the datasets that read it) and ``README.txt``. The archive is a local backup: never commit it.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import shutil
import sys
import zipfile
from collections import defaultdict
from pathlib import Path

from data_foundry.schema import resolve_warehouse_dir
from data_foundry.v2.dataset import PREPARED_MARKER

STORED = (".gz", ".parquet", ".zip", ".xlsx", ".bz2", ".7z", ".xz", ".png", ".jpg")
"""Already compressed: stored as they are rather than deflated again."""

README = """TabArena v0.2 working copy: the raw input files of the rebuild of {date}

{n} files. Unpack into the data-foundry repository root so that the files land in local-data-warehouse/
(or anywhere, and point DATA_FOUNDRY_WAREHOUSE at the unpacked local-data-warehouse/ folder).

MANIFEST.tsv lists every file with its size, SHA-256 and the datasets that read it ("(prepare)" marks the inputs of a
`_prepare_raw_files` step, from which the prepared files are regenerated).

Rebuild, from the repository root:

    .venv/bin/python -m data_foundry.curation.cli dataset build datasets/_dev/tabarena-v0pt2/<name>

or check without saving (`dataset check`). The definitions are datasets/_dev/tabarena-v0pt2/*/dataset.py; files
next to a definition are in the repository, not in this archive.
"""


def inputs(out_dir: Path) -> dict[str, set[str]]:
    """Every traced raw file of a run, with the datasets that read it."""
    used: dict[str, set[str]] = defaultdict(set)
    for f in sorted(out_dir.glob("*.json")):
        record = json.loads(f.read_text())
        if "name" not in record:
            continue
        for path in record.get("read", []):
            used[path].add(record["name"])
        for path in record.get("prepare_read", []):
            used[path].add(f"{record['name']} (prepare)")
    return used


def prepared_files(warehouse: Path, used: dict[str, set[str]]) -> set[str]:
    """The inputs that a ``_prepare_raw_files`` step wrote, as its marker next to them lists them."""
    prepared = set()
    for folder in {Path(rel).parent for rel in used}:
        marker = warehouse / folder / PREPARED_MARKER
        if marker.is_file():
            prepared |= {(folder / name).as_posix() for name in json.loads(marker.read_text()).get("files", [])}
    return prepared & set(used)


def sha256(path: Path) -> str:
    """The SHA-256 of a file, read in 16 MB blocks."""
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 24), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> int:
    """Link the inputs into a warehouse, or write the zip."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("out_dir", type=Path)
    parser.add_argument("mode", choices=["links", "zip"])
    parser.add_argument("target", type=Path, help="The warehouse folder to link into, or the zip to write.")
    args = parser.parse_args()

    warehouse = resolve_warehouse_dir().resolve()
    used = inputs(args.out_dir)
    total = sum((warehouse / rel).stat().st_size for rel in used)
    if args.mode == "links":
        # a prepared file is copied, not linked, with the hash of the code that wrote it: a `_prepare_raw_files` step
        # that runs in the check would otherwise write through the link into the real warehouse
        prepared = prepared_files(warehouse, used)
        for rel in used:
            link = args.target / rel
            link.parent.mkdir(parents=True, exist_ok=True)
            if not link.exists() and not link.is_symlink():
                if rel in prepared:
                    shutil.copy2(warehouse / rel, link)
                else:
                    link.symlink_to(warehouse / rel)
        for marker in {Path(rel).parent / PREPARED_MARKER for rel in prepared}:
            if (warehouse / marker).is_file():
                shutil.copy2(warehouse / marker, args.target / marker)
        print(f"{len(used)} files, {total / 1e9:.1f} GB, under {args.target} ({len(prepared)} prepared files copied)")
        return 0

    manifest = ["path\tbytes\tsha256\tused_by"]
    with zipfile.ZipFile(args.target, "w", allowZip64=True) as archive:
        for rel in sorted(used):
            src = warehouse / rel
            method = zipfile.ZIP_STORED if src.suffix.lower() in STORED else zipfile.ZIP_DEFLATED
            archive.write(
                src,
                f"local-data-warehouse/{rel}",
                compress_type=method,
                compresslevel=None if method == zipfile.ZIP_STORED else 6,
            )
            manifest.append(
                f"local-data-warehouse/{rel}\t{src.stat().st_size}\t{sha256(src)}\t{', '.join(sorted(used[rel]))}"
            )
            print("added", rel, flush=True)
        archive.writestr("MANIFEST.tsv", "\n".join(manifest) + "\n")
        archive.writestr("README.txt", README.format(n=len(used), date=dt.date.today().isoformat()))
    print(f"wrote {args.target}: {len(used)} files, {args.target.stat().st_size / 1e9:.1f} GB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
