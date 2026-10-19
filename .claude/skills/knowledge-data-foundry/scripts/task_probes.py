"""Task probes for v2 datasets: is the task worth benchmarking, or empty, solved, or the same for every model?

Usage::

    python .claude/skills/knowledge-data-foundry/scripts/task_probes.py <unique_name> [<unique_name> ...]
        [--root datasets/_dev/tabarena-v0pt2]
    python .claude/skills/knowledge-data-foundry/scripts/task_probes.py --all [--built] [--jobs 8] [--out DIR]

Runs the task probes of ``curation_probes.task`` (``.claude/skills/knowledge-curation/scripts/curation_probes/task.py``
says what is measured and when each flag is raised) on each dataset's shipped splits, with its group and time columns
and, for a task scored per group (``Grouping(prediction_unit="group")``), the grouping's aggregation and
``time_on``. ``--all`` probes every definition under ``--root``; ``--built`` reads the container recorded in each
``README.md``'s build record instead of rebuilding the frame from the raw files. ``--splits`` sets the splits probed
(default: up to 30 for small data, else 5), ``--max-rows`` caps each train and test side, ``--no-text`` leaves text
columns out instead of encoding them, ``--n-jobs`` sets the threads per model and ``--jobs`` the datasets probed in
parallel. ``--out DIR`` writes one JSON per dataset and ``summary.md`` there.

The flags are questions for the curator, not verdicts; how to answer each one:
``.claude/skills/knowledge-curation/references/task_probes.md``. The numbers are indicative (untuned models); a flag is
checked against tuned methods before anyone acts on it (``tuned_results.py``).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import traceback
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1")
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "knowledge-curation" / "scripts"))

import dataset_io
from curation_probes import task
from joblib import Parallel, delayed


def probe(name: str, root: Path, *, built: bool, n_splits: int | None, max_rows: int, n_jobs: int, text: bool) -> dict:
    """Run the probes of ``curation_probes.task`` on one dataset and return the numbers and flags."""
    started = time.time()
    data = dataset_io.load(name, root, built=built)
    grouping = data.grouping
    result = task.run(
        data.df,
        data.target,
        data.problem_type,
        data.flat_splits(),
        group_cols=data.group_cols,
        prediction_unit=grouping.prediction_unit if grouping is not None else "row",
        aggregation=grouping.aggregation if grouping is not None else None,
        group_time_on=grouping.time_on if grouping is not None else None,
        time_on=data.time_on,
        n_splits=n_splits,
        max_rows=max_rows,
        n_jobs=n_jobs,
        text=text,
    )
    seconds = round(time.time() - started)
    return {"name": name, "origin": data.origin, "regime": data.regime} | result | {"seconds": seconds}


def render(result: dict) -> str:
    """A short text report of one dataset's probes."""
    if "error" in result:
        return f"{result['name']}: CRASH {result['error']}"
    t = result["scores"]
    keys = [k for k in ("auc", "macro_auc", "log_loss", "r2", "rmse") if f"{k}_mean" in t["dummy"]]
    head = (
        f"{result['name']} ({result['regime']}, {result['problem_type']}, unit {result['unit']}, {result['origin']}): "
        f"{result['rows']:,} rows, {result['features']} features"
        + (f" + {result['text_columns']} text columns" if result["text_columns"] else "")
        + f", {result['splits_probed']} of {result['splits_shipped']} splits, {result['seconds']} s"
    )
    lines = [head]
    for key in ["dummy", "drift", "linear", "selected_linear", "random_forest", "lightgbm", "single_feature"]:
        if key in t:
            cells = ", ".join(f"{k} {t[key][f'{k}_mean']:.3f}" for k in keys)
            lines.append(f"  {key:>15}: skill {t[key]['skill_mean']:+.3f} +- {t[key]['skill_std']:.3f} | {cells}")
    lines.append(
        f"  best family {result['best']}: beats the dummy on {result['best_beats_dummy_share']:.0%} of the splits, "
        f"standard error of its mean skill {result['best_skill_se']:.3f}"
    )
    if "spread" in t:
        s = t["spread"]
        lines.append(
            f"  spread {s['best']} - {s['worst']}: {s['best_minus_worst']:+.3f} (paired SE {s['paired_se']:.3f})"
        )
    if result["single_feature"]["chosen"]:
        chosen = ", ".join(f"{k!r} {v}x" for k, v in result["single_feature"]["chosen"].items())
        lines.append(f"  single feature chosen per split: {chosen}")
    if result["smallest_class_per_test_fold"] is not None:
        what = "groups" if result["unit"].startswith("group") else "rows"
        lines.append(f"  smallest class in a test fold: {result['smallest_class_per_test_fold']} {what}")
        if few := result.get("few_minority_classes"):
            named = ", ".join(f"{k!r} {v}" for k, v in list(few.items())[:20])
            more = f" and {len(few) - 20} more" if len(few) > 20 else ""
            lines.append(f"  classes under {task.FEW_MINORITY} {what} in a test fold (smallest count): {named}{more}")
    lines.append(f"  flags: {', '.join(result['flags']) or 'none'}")
    return "\n".join(lines)


def _safe_probe(name: str, root: Path, **kwargs) -> dict:
    try:
        return probe(name, root, **kwargs)
    except Exception as error:  # noqa: BLE001 - one crash must not stop a sweep
        return {"name": name, "error": f"{type(error).__name__}: {error}", "traceback": traceback.format_exc()}


def main(argv: list[str] | None = None) -> int:
    """Probe the datasets; see the module docstring."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("names", nargs="*")
    parser.add_argument("--all", action="store_true", help="Probe every definition under --root.")
    parser.add_argument("--root", type=Path, default=Path("datasets/_dev/tabarena-v0pt2"))
    parser.add_argument("--built", action="store_true", help="Read the built containers (README build record).")
    parser.add_argument("--splits", type=int, help="Splits to probe (default: up to 30 for small data, else 5).")
    parser.add_argument("--max-rows", type=int, default=50_000)
    parser.add_argument("--no-text", action="store_true", help="Leave text columns out instead of encoding them.")
    parser.add_argument("--n-jobs", type=int, default=8, help="Threads per model.")
    parser.add_argument("--jobs", type=int, default=1, help="Datasets probed in parallel.")
    parser.add_argument("--out", type=Path, help="Write one JSON per dataset and summary.md here.")
    args = parser.parse_args(argv)

    names = dataset_io.dataset_names(args.root) if args.all else args.names
    if not names:
        parser.error("name at least one dataset, or pass --all")
    kwargs = {
        "built": args.built,
        "n_splits": args.splits,
        "max_rows": args.max_rows,
        "n_jobs": args.n_jobs,
        "text": not args.no_text,
    }
    results = Parallel(n_jobs=args.jobs)(delayed(_safe_probe)(n, args.root, **kwargs) for n in names)
    for result in results:
        print(render(result))
    if args.out:
        args.out.mkdir(parents=True, exist_ok=True)
        for result in results:
            (args.out / f"{result['name']}.json").write_text(json.dumps(result, indent=1, default=str))
        rows = [
            f"| `{r['name']}` | {r.get('regime', '')} | {r.get('unit', '')} | {r.get('best', '')} | "
            + (
                f"{r['scores'][r['best']]['skill_mean']:+.3f} | {', '.join(r['flags']) or ''} |"
                if "error" not in r
                else f" | CRASH: {r['error'][:80]} |"
            )
            for r in results
        ]
        header = "| dataset | regime | unit | best model | best skill | flags |\n|---|---|---|---|---|---|\n"
        (args.out / "summary.md").write_text(header + "\n".join(rows) + "\n")
    return 1 if any("error" in r for r in results) else 0


if __name__ == "__main__":
    sys.exit(main())
