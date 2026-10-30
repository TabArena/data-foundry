"""Dtype probes for v2 datasets: is each column typed by its meaning, a count numeric and a code categorical?

Usage::

    python .claude/skills/knowledge-data-foundry/scripts/dtype_probes.py <unique_name> ... [--all]
        [--root datasets/_dev/tabarena-v0pt2] [--codebook URL] [--no-fetch] [--jobs 4] [--out DIR]

Rebuilds each definition's frame from the raw files as the split step leaves it (typed by ``_feature_types``) and
runs ``curation_probes.dtypes`` on it, with the target, the group columns and the scoring columns left out;
``.claude/skills/knowledge-curation/scripts/curation_probes/dtypes.py`` says what each flag means. The codebook is read
from the first UCI or OpenML link of the definition (``source_url``, then ``download_description``), one request per
dataset; ``--codebook URL`` names another, ``--no-fetch`` reads none. ``--all`` probes every definition under
``--root``; ``--jobs`` sets the datasets probed in parallel. ``--out DIR`` writes one JSON per dataset and
``flagged.csv`` there. A flag is a question: the column's meaning decides, by CLEAN-14 of
``.claude/skills/knowledge-curation/references/cleaning_features.md``.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1")
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "knowledge-curation" / "scripts"))

import dataset_io
import pandas as pd
from curation_probes import dtypes
from data_foundry.schema import as_column_list
from joblib import Parallel, delayed


def codebook_link(ds: object) -> str | None:
    """The first UCI or OpenML link of the definition's source link and download description."""
    text = f"{getattr(ds, 'source_url', '') or ''} {getattr(ds, 'download_description', '') or ''}"
    return next((u for u in re.findall(r"https?://[^\s\"'<>)]+", text) if dtypes.codebook_api_url(u)), None)


def probe(name: str, root: Path, *, codebook_url: str | None, fetch: bool) -> dict:
    """Run ``curation_probes.dtypes`` on one definition's frame."""
    started = time.time()
    ds = dataset_io.definition(name, root)
    task = ds.task_metadata
    exclude = [task.target_column_name, *as_column_list(task.group_on), *(c.column for c in task.scoring_columns)]
    result = {"name": name, "codebook_url": (codebook_url or codebook_link(ds)) if fetch else None}
    codebook = {}
    if result["codebook_url"]:
        try:
            codebook = dtypes.fetch_codebook(result["codebook_url"])
        except Exception as error:  # noqa: BLE001 - the probe runs without a codebook
            result["codebook_error"] = f"{type(error).__name__}: {error}"[:200]
    table = dtypes.column_table(ds.make_splits().df, exclude=exclude, codebook=codebook)
    result["columns"] = len(table)
    result["codebook_columns"] = len(codebook)
    result["codebook_matched"] = 0
    if not table.empty:
        matched = table["codebook_type"].notna() | table["codebook_description"].notna()
        result["codebook_matched"] = int(matched.sum())
    result["flagged"] = dtypes.flagged(table).to_dict("records")
    result["seconds"] = round(time.time() - started)
    return result


def _safe(name: str, root: Path, **kwargs) -> dict:
    try:
        return probe(name, root, **kwargs)
    except Exception as error:  # noqa: BLE001 - one failing dataset must not stop a sweep
        return {"name": name, "error": f"{type(error).__name__}: {error}"[:300], "flagged": []}


def render(r: dict) -> str:
    """The dataset's line, then one line per flagged column."""
    if "error" in r:
        return f"{r['name']}: error {r['error']}"
    if r.get("codebook_error"):
        source = f"codebook failed ({r['codebook_error']})"
    elif r.get("codebook_url"):
        source = f"codebook {r['codebook_matched']} of {r['columns']} columns matched ({r['codebook_url']})"
    else:
        source = "no codebook"
    lines = [f"{r['name']}: {len(r['flagged'])} of {r['columns']} columns flagged; {source}"]
    for row in r["flagged"]:
        values = f", {row['value_min']:g} to {row['value_max']:g}" if row["value_min"] is not None else ""
        if row["other_levels"]:
            values += f", also {row['other_levels']}"
        book = ""
        if row["codebook_type"] or row["codebook_description"]:
            book = f"; codebook {row['codebook_type'] or ''} {str(row['codebook_description'] or '')[:90]!r}"
        lines.append(f"  {row['column']} ({row['dtype']}, {row['n_values']} values{values}): {row['flags']}{book}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    """Probe the datasets; see the module docstring."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("names", nargs="*")
    parser.add_argument("--all", action="store_true", help="Probe every definition under --root.")
    parser.add_argument("--root", type=Path, default=Path("datasets/_dev/tabarena-v0pt2"))
    parser.add_argument("--codebook", help="A UCI or OpenML dataset link to read the codebook from.")
    parser.add_argument("--no-fetch", action="store_true", help="Read no codebook.")
    parser.add_argument("--jobs", type=int, default=1, help="Datasets probed in parallel.")
    parser.add_argument("--out", type=Path, help="Write one JSON per dataset and flagged.csv here.")
    args = parser.parse_args(argv)
    names = dataset_io.dataset_names(args.root) if args.all else args.names
    if not names:
        parser.error("name at least one dataset, or pass --all")
    kwargs = {"codebook_url": args.codebook, "fetch": not args.no_fetch}
    results = Parallel(n_jobs=args.jobs)(delayed(_safe)(n, args.root, **kwargs) for n in names)
    for r in results:
        print(render(r))
    if args.out:
        args.out.mkdir(parents=True, exist_ok=True)
        for r in results:
            (args.out / f"{r['name']}.json").write_text(json.dumps(r, indent=1, default=str))
        rows = [{"dataset": r["name"], **row} for r in results for row in r["flagged"]]
        pd.DataFrame(rows).to_csv(args.out / "flagged.csv", index=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
