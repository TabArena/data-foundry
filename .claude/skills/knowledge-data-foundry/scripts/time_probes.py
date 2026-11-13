"""Time-recovery probe: does a dataset whose split is not temporal still carry a time order (SPLIT-32)?

Usage::

    python .claude/skills/knowledge-data-foundry/scripts/time_probes.py <unique_name> ... [--all] [--built]
        [--include-temporal] [--jobs 4] [--out DIR] [--root DIR]

Runs ``curation_probes.time_recovery`` on each dataset: date-like columns in the frame and among the raw columns the
definition drops, the target along the raw row order and along each ID-like column, few-valued columns that encode
the period, rows that repeat one block later (``periodic_blocks``), runs of one entity in consecutive rows
(``entity_runs``), and class blocks that are several pieces (``class_block_drift``). It is model-free and fast.
``--root`` is the folder of the definitions (the TabArena v0.2 working copy by default); the raw files are read from
the local warehouse (``$DATA_FOUNDRY_WAREHOUSE``, else ``local-data-warehouse/`` of the installed package).
``--all`` probes every definition under ``--root`` whose split is not temporal (``--include-temporal`` adds the
temporal ones). ``--built`` reads a container instead of the raw files: the build of the ``README.md``'s build record
when it is in the local warehouse, else the copy of a registered collection (BeyondArena), from the cache
(``$DATA_FOUNDRY_CACHE``, else ``~/.cache/data_foundry/<collection>/``) or downloaded into it. A container's rows are
shuffled, so with ``--built`` the checks of the row order are not run (the output says so); the checks of the values
(date columns, IDs, period values) are. ``--out DIR`` writes one JSON per dataset and ``summary.md``. A flag is a
question: the reading is in ``.claude/skills/knowledge-curation/references/splits.md`` (SPLIT-32) and
``checks_and_probes.md``.
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
from data_foundry.collections import get_collection, list_collections
from data_foundry.curation_container import CuratedContainer
from data_foundry.schema import as_column_list, resolve_warehouse_dir
from data_foundry.v2 import read_report
from joblib import Parallel, delayed

BUILT_WARNING = (
    "warning: --built reads containers, whose rows were shuffled: the checks of the row order (order, "
    "sorted_by_target, periodic_blocks, entity_runs, class_block_drift) are not run."
)


def built_container(name: str, root: Path) -> tuple[CuratedContainer, str]:
    """The built container of ``name`` and where it came from: the build of its ``README.md``'s build record in the
    local warehouse, else the copy of a registered collection (read from the cache, downloaded into it if missing).
    """
    build = (read_report(Path(root) / name / "README.md") or {}).get("build") or {}
    if build.get("path") and (resolve_warehouse_dir() / build["path"] / "dataset.parquet").is_file():
        return CuratedContainer.load(resolve_warehouse_dir() / build["path"]), "built"
    for collection_name in list_collections():
        collection = get_collection(collection_name)
        try:
            collection.find_entry(name)
        except KeyError:
            continue
        return collection.get_dataset(name), f"built ({collection_name})"
    raise FileNotFoundError(f"{name}: no build in the local warehouse and no registered collection holds it")


def built_input(name: str, root: Path) -> tuple[dataset_io.ProbeInput, tuple[str, ...]]:
    """The container of ``name`` as the probes take it, and its group columns (a format-1 container has no grouping
    block, only ``group_on``).
    """
    container, origin = built_container(name, root)
    if container.format_version >= 2:
        data = dataset_io.from_container(container, origin)
        return data, tuple(data.group_cols)
    task = container.task_metadata
    data = dataset_io.ProbeInput(
        df=container.dataset,
        target=task.target_column_name,
        problem_type=task.problem_type,
        regime=task.split_regime,
        splits=container.experiment_metadata.splits,
        grouping=None,
        time_on=task.time_on,
        origin=origin,
    )
    return data, tuple(as_column_list(task.group_on))


def probe(name: str, root: Path, *, built: bool, include_temporal: bool = False) -> dict:
    """Run ``time_recovery.check_frame`` on one dataset."""
    started = time.time()
    if built:
        data, groups = built_input(name, root)
    else:
        data = dataset_io.from_definition(dataset_io.definition(name, root), raw=True)
        groups = tuple(data.group_cols)
    result = {"name": name, "origin": data.origin, "regime": data.regime}
    if data.regime == "temporal_non_iid" and not include_temporal:
        return result | {"skipped": "temporal split", "flags": []}
    exclude = groups + tuple(data.scoring_cols)
    result |= time_recovery.check_frame(
        data.df,
        data.target,
        data.problem_type,
        exclude=exclude,
        raw=data.raw,
        raw_rows=data.raw_rows,
        order_known=not built,
    )
    result["raw_note"] = data.raw_note
    result["seconds"] = round(time.time() - started)
    return result


def _safe(name: str, root: Path, **kwargs) -> dict:
    try:
        return probe(name, root, **kwargs)
    except Exception as error:  # noqa: BLE001 - one failing dataset must not stop a sweep
        return {"name": name, "error": f"{type(error).__name__}: {error}"[:300], "flags": []}


def _render_order(r: dict) -> list[str]:
    """The parts of the line that read the row order."""
    if r["order_source"] == "none":
        return ["row order not read (a built container's rows are shuffled)"]
    order = r["order"]
    size = order.get("largest_tenth_gap", order.get("spearman_position"))
    parts = [f"{r['order_source']} order: p {order['p']:.1e}, size {size:.3f}"]
    blocks = r.get("periodic_blocks", {})
    if blocks.get("standout_windows"):
        target = blocks.get("target", {})
        part = (
            f"rows repeat one block later in {blocks['standout_windows']}/{blocks['windows']} windows (lag "
            f"{min(blocks['lags'])}-{max(blocks['lags'])}, close {blocks['close_at_lag']:.2f} vs "
            f"{blocks['close_around']:.2f}"
        )
        if "same_class_one_block" in target:
            part += (
                f"; '{target['class']}' one block later {target['same_class_one_block']:.2f} vs "
                f"{target['same_class_half_block']:.2f}/{target['same_class_one_and_a_half_blocks']:.2f}"
            )
        parts.append(part + ")")
    runs = r.get("entity_runs", {})
    if runs.get("flag"):
        fixed = sorted(runs["fixed_fields"])
        fixed_text = ", ".join(fixed[:5]) + (f" and {len(fixed) - 5} more" if len(fixed) > 5 else "")
        part = (
            f"runs on {runs['counter']}: {runs['runs']} runs ({runs['runs_from_start']} from the start, "
            f"{runs['runs_of_two_or_more']} of 2+ rows), fixed {fixed_text}"
        )
        if "class_on_last_row" in runs:
            shares = ", ".join(f"{k} {v:.3f}" for k, v in runs["class_on_last_row"].items())
            part += f"; on a run's last row: {shares} (all rows {runs['last_row_share']:.3f})"
        parts.append(part)
    drifting = {k: c for k, c in r.get("class_block_drift", {}).items() if c["drifting"]}
    if drifting:
        parts.append(
            "within class blocks, features drift: "
            + ", ".join(
                f"{k} {c['drifting']}/{c['features']}"
                + (f" (sorted by {', '.join(c['sorted_by'])})" * bool(c["sorted_by"]))
                for k, c in drifting.items()
            )
        )
    return parts


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
    parts += _render_order(r)
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
    if args.built:
        lines.insert(0, BUILT_WARNING)
    print("\n".join(lines))
    if args.out:
        args.out.mkdir(parents=True, exist_ok=True)
        for r in results:
            (args.out / f"{r['name']}.json").write_text(json.dumps(r, indent=1, default=str))
        (args.out / "summary.md").write_text("\n".join(f"- {line}" for line in lines) + "\n")


if __name__ == "__main__":
    main()
