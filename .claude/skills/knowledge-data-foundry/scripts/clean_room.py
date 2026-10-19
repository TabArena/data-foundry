"""Clean room: the input folder of a blind reviewer, who judges a dataset without our curation notes.

Usage::

    python .claude/skills/knowledge-data-foundry/scripts/clean_room.py <unique_name> --out DIR [--max-rows 200000]
        [--root datasets/_dev/tabarena-v0pt2] [--records curation/records] [--built]

Loads the v2 definition of ``<unique_name>`` through ``dataset_io.py`` (its curated frame and split plan, rebuilt from
the raw files; ``--built`` reads the container of the README's build record instead) and the curation record for its
source links, and writes two files:

* ``DIR/data.parquet``: the curated frame with the target. A frame with more than ``--max-rows`` rows is a random
  sample of that many rows (seed 0, original order kept), and ``task.md`` says so.
* ``DIR/task.md``: the target column, the problem type, rows x columns, the regime (IID, grouped with the group
  column, temporal with the time column), the number of folds or test windows, and the source links.

Nothing else goes into the folder: no ``task_summary``, ``curation_comments``, record comments, README text or link
notes (the ``#`` lines of ``source_links``), so the reviewer's judgement is their own. The folder name ``<unique_name>``
is not in ``task.md`` either; the links name the source.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import dataset_io
from data_foundry.curation._paths import records_dir, resolve_curation_root
from data_foundry.curation.store import load_record

SEED = 0
REGIMES = {"iid": "IID", "grouped_non_iid": "grouped", "temporal_non_iid": "temporal"}


def source_links(name: str, records: Path, folder_class: type | None = None) -> list[str]:
    """The record's source links without the note lines (``#``); the record of a ``version_of`` folder if needed."""
    path = records / f"{name}.md"
    if not path.exists() and folder_class is not None and getattr(folder_class, "version_of", None):
        path = records / f"{folder_class.version_of}.md"
    if not path.exists():
        return []
    return [link for link in load_record(path).source_links if not link.lstrip().startswith("#")]


def _folder(name: str, root: Path, records: Path) -> tuple[str, Path]:
    """The definition folder of ``name``: ``root/name``, else the folder the record's ``v2_path`` names."""
    if (root / name / "dataset.py").exists():
        return name, root
    path = records / f"{name}.md"
    if path.exists() and (v2_path := load_record(path).v2_path):
        folder = resolve_curation_root().parent / Path(v2_path).parent  # v2_path is relative to the repo
        return folder.name, folder.parent
    raise SystemExit(f"no definition for {name!r}: neither {root / name / 'dataset.py'} nor a v2_path in {path}")


def regime_line(data: dataset_io.ProbeInput) -> str:
    """The regime in one line, with its group or time column."""
    regime = REGIMES.get(data.regime, data.regime)
    groups = ", ".join(f"`{c}`" for c in data.group_cols)
    if regime == "grouped":
        return f"grouped by {groups} (whole groups are held out)"
    if regime == "temporal":
        line = f"temporal on `{data.time_on}` (each test window comes after its training rows)"
        return line + (f"; rows grouped by {groups}" if groups else "")
    return f"{regime} (random rows)"


def splits_line(data: dataset_io.ProbeInput) -> str:
    """The number of folds (IID, grouped) or test windows (temporal)."""
    repeats = data.repeats()
    total = sum(len(r) for r in repeats)
    if REGIMES.get(data.regime) == "temporal":
        return f"{total} test windows"
    folds = {len(r) for r in repeats}
    per = folds.pop() if len(folds) == 1 else f"{min(len(r) for r in repeats)}-{max(len(r) for r in repeats)}"
    return f"{len(repeats)} repeats x {per} folds ({total} train/test splits)"


def task_markdown(data: dataset_io.ProbeInput, links: list[str], *, rows: int, sampled: int | None) -> str:
    """The task.md of the clean room: only the facts the reviewer needs to start."""
    columns = data.df.shape[1]
    lines = [
        "# Task",
        "",
        f"- Target column: `{data.target}`",
        f"- Problem type: {data.problem_type.replace('_', ' ')}",
        f"- Size: {rows:,} rows x {columns} columns (target included)",
        f"- Regime: {regime_line(data)}",
        f"- Splits: {splits_line(data)}",
    ]
    if sampled is not None:
        lines.append(
            f"- `data.parquet` is a random sample of {sampled:,} of the {rows:,} rows (seed {SEED}, original order "
            "kept); the size above is the full data."
        )
    else:
        lines.append("- `data.parquet` holds every row.")
    lines += ["", "## Source links", ""]
    lines += [f"- {link}" for link in links] or ["- (none recorded)"]
    return "\n".join(lines) + "\n"


def write(name: str, out: Path, *, root: Path, records: Path, max_rows: int, built: bool) -> dict:
    """Write ``data.parquet`` and ``task.md`` for ``name`` into ``out``; return what was written."""
    folder, folder_root = _folder(name, root, records)
    ds = dataset_io.definition(folder, folder_root)
    data = dataset_io.load(folder, folder_root, built=True) if built else dataset_io.from_definition(ds)
    links = source_links(name, records, type(ds))
    df = data.df
    rows = len(df)
    sampled = None
    if rows > max_rows:
        df = df.sample(n=max_rows, random_state=SEED).sort_index()
        sampled = max_rows
    out.mkdir(parents=True, exist_ok=True)
    df.reset_index(drop=True).to_parquet(out / "data.parquet")
    (out / "task.md").write_text(task_markdown(data, links, rows=rows, sampled=sampled))
    return {"name": name, "folder": folder, "rows": rows, "columns": df.shape[1], "sampled": sampled, "out": str(out)}


def main(argv: list[str] | None = None) -> int:
    """Write the clean room; see the module docstring."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("name", help="The record's unique_name.")
    parser.add_argument("--out", type=Path, required=True, help="The folder to write data.parquet and task.md to.")
    parser.add_argument("--max-rows", type=int, default=200_000, help="Sample larger frames down to this many rows.")
    parser.add_argument("--root", type=Path, default=None, help="Default: datasets/_dev/tabarena-v0pt2.")
    parser.add_argument("--records", type=Path, default=None, help="Records folder (default: curation/records).")
    parser.add_argument("--built", action="store_true", help="Read the built container (README build record).")
    args = parser.parse_args(argv)

    result = write(
        args.name,
        args.out,
        root=args.root or resolve_curation_root().parent / "datasets" / "_dev" / "tabarena-v0pt2",
        records=args.records or records_dir(),
        max_rows=args.max_rows,
        built=args.built,
    )
    sample = f", sampled to {result['sampled']:,}" if result["sampled"] else ""
    print(f"{result['name']}: {result['rows']:,} rows x {result['columns']} columns{sample} -> {result['out']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
