"""Build (or check) one v2 dataset and record what it read.

Usage, from the repository root::

    .venv/bin/python .claude/skills/rebuild-working-copy/scripts/build_one.py <unique_name> <out.json>
        [--root datasets/_dev/tabarena-v0pt2] [--check-only] [--trace-prepare]

The JSON holds the status, the findings, the checksum, the UUID and saved path of a build, the time, the peak memory,
and every file under the warehouse the build opened for reading (``read``): Python-level opens through an audit hook,
plus the native readers of pandas, pyarrow and polars, which open files without Python's ``open``. Files of the
container the build itself saves (and reads back to verify) are left out.

``--trace-prepare`` also runs the definition's ``_prepare_raw_files`` into a scratch copy of its raw folder and records
the raw files that step reads (``prepare_read``), so a backup of the inputs can regenerate the prepared files. Run it
for the definitions that set ``prepared_raw_files``.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import resource
import shutil
import sys
import tempfile
import time
import traceback
from pathlib import Path

from data_foundry.schema import resolve_warehouse_dir

WAREHOUSE = resolve_warehouse_dir().resolve()
UUID = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")
READ: set[str] = set()


def _note(path: object) -> None:
    try:
        resolved = Path(os.fsdecode(path)).resolve()
    except (TypeError, ValueError, OSError):
        return
    if resolved.is_relative_to(WAREHOUSE) and resolved.is_file():
        READ.add(str(resolved.relative_to(WAREHOUSE)))


def _audit(event: str, args: tuple) -> None:
    if event == "open" and args and isinstance(args[0], str | bytes | os.PathLike):
        mode = args[1] if len(args) > 1 else "r"
        if isinstance(mode, str) and any(m in mode for m in "wax+"):
            return
        _note(args[0])


def _wrap(module: object, name: str) -> None:
    original = getattr(module, name, None)
    if original is None:
        return

    def reader(*args, **kwargs):
        keys = ("path", "source", "filepath_or_buffer", "io", "file", "where")
        source = args[0] if args else next((kwargs[k] for k in keys if k in kwargs), None)
        for item in source if isinstance(source, list | tuple) else [source]:
            if isinstance(item, str | os.PathLike):
                _note(item)
        return original(*args, **kwargs)

    setattr(module, name, reader)


def _install_tracing() -> None:
    sys.addaudithook(_audit)
    import pandas as pd  # noqa: PLC0415 - the readers are wrapped before any definition imports them
    import pyarrow.parquet as pq  # noqa: PLC0415

    for fn in ("read_parquet", "read_csv", "read_table", "read_excel", "read_feather", "read_json", "read_pickle"):
        _wrap(pd, fn)
    for fn in ("read_table", "ParquetFile", "ParquetDataset", "read_metadata", "read_schema"):
        _wrap(pq, fn)
    try:
        import pyarrow.csv as pacsv  # noqa: PLC0415
        import pyarrow.dataset as pads  # noqa: PLC0415

        _wrap(pacsv, "read_csv")
        _wrap(pads, "dataset")
    except ImportError:
        pass
    try:
        import polars as pl  # noqa: PLC0415

        for fn in ("read_csv", "read_parquet", "scan_csv", "scan_parquet", "read_ipc", "scan_ipc", "read_excel"):
            _wrap(pl, fn)
    except ImportError:
        pass


def _trace_prepare(ds) -> list[str]:
    """The raw files ``_prepare_raw_files`` reads, run into a scratch copy of the raw folder (symlinks)."""
    if not ds.prepared_raw_files:
        return []
    READ.clear()
    scratch = Path(tempfile.mkdtemp()) / ds.raw_dir.name

    def skip(_directory: str, names: list[str]) -> list[str]:
        # saved containers (UUID folders), versions, the prepared outputs themselves and kept old copies
        return [n for n in names if UUID.fullmatch(n) or n == "versions" or n in ds.prepared_raw_files or ".pre-" in n]

    shutil.copytree(
        ds.raw_dir,
        scratch,
        symlinks=True,
        ignore=skip,
        copy_function=lambda src, dst: Path(dst).symlink_to(Path(src).resolve()),
    )
    try:
        ds._prepare_raw_files(scratch)
    finally:
        shutil.rmtree(scratch.parent, ignore_errors=True)
    return sorted(READ)


def main() -> int:
    """Build or check one definition and write its record."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("name")
    parser.add_argument("out", type=Path)
    parser.add_argument("--root", type=Path, default=Path("datasets/_dev/tabarena-v0pt2"))
    parser.add_argument("--check-only", action="store_true", help="Run `check` without saving (no UUID).")
    parser.add_argument("--trace-prepare", action="store_true", help="Also record the inputs of _prepare_raw_files.")
    args = parser.parse_args()

    _install_tracing()
    from data_foundry.v2 import load_definition  # noqa: PLC0415 - after the readers are wrapped

    started = time.time()
    record: dict = {"name": args.name, "check_only": args.check_only}
    try:
        ds = load_definition(args.root / args.name / "dataset.py")()
        result = ds.check(write_report=False, verbose=False) if args.check_only else ds.build(verbose=False)
        report, container = result.bundle_report, result.container
        saved = str(result.saved_path.relative_to(WAREHOUSE)) if result.saved_path else None
        record |= {
            "ok": report.ok,
            "uuid": container.uuid if result.saved else None,
            "checksum": container.checksum,
            "format_version": container.format_version,
            "saved_path": saved,
            "rows": len(container.dataset),
            "columns": container.dataset.shape[1],
            "splits": [len(container.experiment_metadata.splits), len(container.experiment_metadata.splits[0])],
            "errors": [[r.slug, r.message] for r in report.errors],
            "warnings": [[r.slug, r.message] for r in report.warnings],
            "infos": [[r.slug, r.message] for r in report.infos],
            "accepted": dict(ds.accepted_check_warnings),
            "read": sorted(p for p in READ if not (saved and p.startswith(saved + "/"))),
        }
        if args.trace_prepare:
            record["prepare_read"] = _trace_prepare(ds)
    except Exception as error:  # noqa: BLE001 - a crash is a result to report, not a reason to stop the sweep
        record |= {"crash": f"{type(error).__name__}: {error}", "traceback": traceback.format_exc()}
        record["read"] = sorted(READ)
    record["seconds"] = round(time.time() - started)
    record["max_rss_gb"] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024**2, 1)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(record, indent=1, default=str))
    status = "CRASH" if "crash" in record else ("ok" if record.get("ok") else "ERRORS")
    print(f"{args.name}: {status} in {record['seconds']} s, {record['max_rss_gb']} GB", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
