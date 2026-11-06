"""Time-recovery probe: does a dataset whose split is not temporal still carry a time order (SPLIT-32)?

Usage::

    python .claude/skills/knowledge-data-foundry/scripts/time_probes.py <unique_name> ... [--all] [--built]
        [--include-temporal] [--jobs 4] [--out DIR]

Runs ``curation_probes.time_recovery`` on each dataset: date-like columns in the frame and among the raw columns the
definition drops, the target along the raw row order and along each ID-like column, and few-valued columns that
encode the period. It is model-free and fast. ``--all`` probes every definition under ``--root`` whose split is not
temporal (``--include-temporal`` adds the temporal ones); ``--built`` reads the container of each ``README.md``'s
build record (then the raw columns and the raw order are not available). ``--out DIR`` writes one JSON per dataset
and ``summary.md``. A flag is a question: the reading is in ``.claude/skills/knowledge-curation/references/splits.md``
(SPLIT-32) and ``checks_and_probes.md``.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1")
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "knowledge-curation" / "scripts"))

import dataset_io
from curation_probes import time_recovery
from joblib import Parallel, delayed


def probe(name: str, root: Path, *, built: bool, include_temporal: bool = False) -> dict:
    """Run ``time_recovery.check_frame`` on one dataset."""
    started = time.time()
    if built:
        data = dataset_io.load(name, root, built=True)
    else:
        data = dataset_io.from_definition(dataset_io.definition(name, root), raw=True)
    result = {"name": name, "origin": data.origin, "regime": data.regime}
    if data.regime == "temporal_non_iid" and not include_temporal:
        return result | {"skipped": "temporal split", "flags": []}
    exclude = tuple(data.group_cols) + tuple(data.scoring_cols)
    result |= time_recovery.check_frame(
        data.df, data.target, data.problem_type, exclude=exclude, raw=data.raw, raw_rows=data.raw_rows
    )
    result["raw_note"] = data.raw_note
    result["seconds"] = round(time.time() - started)
    return result


def _safe(name: str, root: Path, **kwargs) -> dict:
    try:
        return probe(name, root, **kwargs)
    except Exception as error:  # noqa: BLE001 - one failing dataset must not stop a sweep
        return {"name": name, "error": f"{type(error).__name__}: {error}"[:300], "flags": []}


def render(r: dict) -> str:
    """One line per dataset."""
    if "error" in r:
        return f"{r['name']}: error {r['error']}"
    if "skipped" in r:
        return f"{r['name']}: skipped ({r['skipped']})"
    parts = []
    if r["time_columns"]:
        parts.append("time columns " + ", ".join(f"{c} ({why})" for c, why in r["time_columns"].items()))
    if r.get("dropped_time_columns"):
        parts.append("dropped " + ", ".join(r["dropped_time_columns"]))
    order = r["order"]
    size = order.get("largest_tenth_gap", order.get("spearman_position"))
    parts.append(f"{r['order_source']} order: p {order['p']:.1e}, size {size:.3f}")
    drifting = [c for c, o in r["id_orders"].items() if o["flag"]]
    if drifting:
        parts.append("IDs with drift " + ", ".join(drifting))
    period = r["period_values"]
    if period.get("columns"):
        parts.append(f"period columns {period['columns']} ({period.get('levels')} levels, p {period.get('p', 1):.1e})")
    return f"{r['name']} ({r['regime']}, {r['rows']} rows): " + "; ".join(parts) + f"; flags {r['flags']}"


def main() -> None:
    """Parse the arguments and probe the datasets."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("names", nargs="*")
    parser.add_argument("--root", type=Path, default=Path("datasets/_dev/tabarena-v0pt2"))
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--built", action="store_true")
    parser.add_argument("--include-temporal", action="store_true")
    parser.add_argument("--jobs", type=int, default=4)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    names = dataset_io.dataset_names(args.root) if args.all else args.names
    if not names:
        parser.error("name a dataset or pass --all")
    results = Parallel(n_jobs=args.jobs)(
        delayed(_safe)(n, args.root, built=args.built, include_temporal=args.include_temporal) for n in names
    )
    lines = [render(r) for r in results]
    print("\n".join(lines))
    if args.out:
        args.out.mkdir(parents=True, exist_ok=True)
        for r in results:
            (args.out / f"{r['name']}.json").write_text(json.dumps(r, indent=1, default=str))
        (args.out / "summary.md").write_text("\n".join(f"- {line}" for line in lines) + "\n")


if __name__ == "__main__":
    main()
