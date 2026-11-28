"""``data-foundry probe``: run one probe on datasets of a working copy.

Usage::

    data-foundry probe {leak,task,group,hidden-groups,time,dtypes,generated} NAME... [--all] [--built]
        [--root datasets/_dev/tabarena-v0pt2] [--jobs 1] [--n-jobs 8] [--out DIR] [probe options]

The options every probe shares:

* ``NAME...`` or ``--all``: the datasets, by unique name, or every definition under ``--root`` (the TabArena v0.2
  working copy by default; the raw files come from the local warehouse, ``$DATA_FOUNDRY_WAREHOUSE``).
* ``--built``: read the built container instead of rebuilding the frame from the raw files: the build of the
  definition's ``README.md`` build record when it is in the local warehouse, else a registered collection's copy
  (from the cache, ``$DATA_FOUNDRY_CACHE``, downloaded into it if missing). The leak probes read the definition only.
* ``--jobs``: datasets probed in parallel (default 1); ``--n-jobs``: threads per model (default 8).
* ``--out DIR``: one JSON per dataset (``DIR/<name>.json``) and ``DIR/summary.md`` (the dtype probe also writes
  ``flagged.csv``).

Each probe's own options follow its name (``data-foundry probe task --help``). The probe modules say what each number
measures; the reading of the flags is in ``.claude/skills/knowledge-data-foundry/references/checks_and_probes.md``. A
dataset that fails is reported and the others still run; the exit code is 1 when one failed.
"""

from __future__ import annotations

import argparse
import importlib
import json
import os
import traceback
from pathlib import Path
from types import ModuleType

DEFAULT_ROOT = Path("datasets/_dev/tabarena-v0pt2")

PROBES = {
    "leak": ("data_foundry.probes.leak.modes", "Leak probes: what a model learns that it should not (LEAK rules)."),
    "task": ("data_foundry.probes.task", "Task probes: is the task empty, solved, or the same for every model?"),
    "group": ("data_foundry.probes.groups", "Group probes: does the grouping matter, is there signal across groups?"),
    "hidden-groups": (
        "data_foundry.probes.hidden_groups",
        "Hidden groups: columns, keys, near copies and texts that act as an entity.",
    ),
    "time": (
        "data_foundry.probes.time_recovery",
        "Time recovery: does a split that is not temporal keep a time order?",
    ),
    "dtypes": ("data_foundry.probes.dtypes", "Dtype probes: is each column typed by its meaning?"),
    "generated": ("data_foundry.probes.generated", "Generated data: is the target a formula or a rule set?"),
}
"""Each subcommand's module and help line. A module gives ``probe(name, root, args)`` and ``render(result)``, and may
give ``header(args)``, ``summary(results)``, ``write_extra(out, results)`` and ``READS_BUILT = False``."""


def _module(probe: str) -> ModuleType:
    # imported on use: the probes need the `probes` extra (LightGBM), the rest of the curation CLI does not
    os.environ.setdefault("OMP_NUM_THREADS", "1")
    return importlib.import_module(PROBES[probe][0])


def _shared_options() -> argparse.ArgumentParser:
    shared = argparse.ArgumentParser(add_help=False)
    shared.add_argument("names", nargs="*", metavar="NAME", help="Datasets by unique name under --root.")
    shared.add_argument("--all", action="store_true", help="Probe every definition under --root.")
    shared.add_argument("--built", action="store_true", help="Read the built containers instead of the raw files.")
    shared.add_argument("--root", type=Path, default=DEFAULT_ROOT, help=f"Folder of the definitions ({DEFAULT_ROOT}).")
    shared.add_argument("--jobs", type=int, default=1, help="Datasets probed in parallel (default 1).")
    shared.add_argument("--n-jobs", type=int, default=8, help="Threads per model (default 8).")
    shared.add_argument("--out", type=Path, help="Write one JSON per dataset and summary.md here.")
    return shared


def _leak_options(parser: argparse.ArgumentParser) -> None:
    """The options of ``data-foundry probe leak`` beside the shared ones."""
    parser.add_argument("--splits", type=int, default=3, help="Shipped splits probed (default 3).")
    parser.add_argument("--max-rows", type=int, default=50_000, help="Rows kept of each train and test side.")
    parser.add_argument(
        "--max-single-features", type=int, default=300, help="Columns (and missing patterns) fitted one by one."
    )
    parser.add_argument("--time-on", help="Probe 13's time column; default the task's.")
    parser.add_argument(
        "--period", choices=("D", "W", "M", "Q", "Y"), help="Probe 13's calendar period (default chosen)."
    )
    parser.add_argument("--tz", help="Probe 13's timezone: aware times are converted to it.")
    parser.add_argument("--positive", help="Probe 13's event class of a binary target; default the minority class.")
    parser.add_argument("--tail", type=int, help="Probe 13's newest periods tested; default a fifth, 2 to 8.")
    parser.add_argument("--period-only", action="store_true", help="Run probe 13 alone, without a model.")
    parser.add_argument("--raw", action="store_true", help="Run the probes of the raw state alone (10, 18-21).")
    parser.add_argument("--weight-proxy", action="store_true", help="Run probe 22 alone: do features carry the weight?")
    parser.add_argument("--weight-column", help="Probe 22's weight; default the task's sample weight.")
    parser.add_argument(
        "--objective",
        default="metric",
        help="Probe 22's fits of the target: metric (default: a deviance's own loss, else L2), l2, or an objective.",
    )
    parser.add_argument("--seeds", type=int, default=3, help="Probe 22's and 23's LightGBM seeds per split.")
    parser.add_argument(
        "--forced-split", action="store_true", help="Run probe 23 alone: the leak tests of a forced split."
    )
    parser.add_argument("--forced-splits", type=int, default=9, help="Probe 23's splits (default 9).")
    parser.add_argument(
        "--stationary-relation", action="store_true", help="Run the stationary-relation test alone (SPLIT-32)."
    )
    parser.add_argument("--unordered", action="store_true", help="Its periods have no order (month classes).")
    parser.add_argument("--unit", help="Its unit column, or none; default the definition's group column.")
    parser.add_argument("--exclude", nargs="*", help="Further columns that name the period: no model input.")
    parser.add_argument("--windows", type=int, default=3, help="Its windows, newest first (default 3).")
    parser.add_argument("--test-period", nargs="*", help="Only these windows, by period label (one job per window).")
    parser.add_argument("--stationary-seeds", type=int, default=5, help="Its seeds (default 5).")
    parser.add_argument("--max-test", type=int, help="Its LightGBM test rows per window, at most; default all.")
    parser.add_argument(
        "--foundation",
        choices=("none", "tabpfn", "kumo"),
        default="none",
        help="Its foundation model, one state-of-the-art TFM for a time basis: tabpfn (TabPFN v3.5) or kumo.",
    )
    parser.add_argument("--device", help="The foundation model's device; default cuda for tabpfn, cpu for kumo.")
    parser.add_argument("--threads", type=int, help="The foundation model's threads; default --n-jobs.")
    parser.add_argument("--max-foundation-train", type=int, default=20_000, help="Its training rows per fit, at most.")
    parser.add_argument("--max-foundation-test", type=int, default=5_000, help="Its test rows per window, at most.")


def _task_options(parser: argparse.ArgumentParser) -> None:
    """The options of ``data-foundry probe task`` beside the shared ones."""
    parser.add_argument("--splits", type=int, help="Splits to probe (default: up to 30 for small data, else 5).")
    parser.add_argument("--max-rows", type=int, default=200_000, help="Rows kept of each train and test side.")
    parser.add_argument("--no-text", action="store_true", help="Leave text columns out instead of encoding them.")


def _group_options(parser: argparse.ArgumentParser) -> None:
    """The options of ``data-foundry probe group`` beside the shared ones."""
    parser.add_argument("--repeats", type=int, default=3, help="Repeats of the grouped splits used, from the first.")
    parser.add_argument("--permutations", type=int, default=100, help="Runs of the permutation test (0 skips it).")
    parser.add_argument("--max-rows", type=int, default=200_000, help="Rows kept (whole groups, at random).")


def _hidden_groups_options(parser: argparse.ArgumentParser) -> None:
    """The options of ``data-foundry probe hidden-groups`` beside the shared ones."""
    parser.add_argument("--include-grouped", action="store_true", help="Also run grouped tasks (positive controls).")


def _time_options(parser: argparse.ArgumentParser) -> None:
    """The options of ``data-foundry probe time`` beside the shared ones."""
    parser.add_argument("--include-temporal", action="store_true", help="Also probe datasets with a temporal split.")


def _dtypes_options(parser: argparse.ArgumentParser) -> None:
    """The options of ``data-foundry probe dtypes`` beside the shared ones."""
    parser.add_argument("--codebook", help="A UCI or OpenML dataset link to read the codebook from.")
    parser.add_argument("--no-fetch", action="store_true", help="Read no codebook.")


OPTIONS = {
    "leak": _leak_options,
    "task": _task_options,
    "group": _group_options,
    "hidden-groups": _hidden_groups_options,
    "time": _time_options,
    "dtypes": _dtypes_options,
}
"""Each probe's own options; defined here so that building the parser imports no probe."""


def add_probe_parser(sub: argparse._SubParsersAction) -> None:
    """Register the ``probe`` command group on the curation CLI."""
    p_probe = sub.add_parser("probe", help="Run a probe (leak, task, group, ...) on datasets of a working copy.")
    psub = p_probe.add_subparsers(dest="probe", required=True)
    shared = _shared_options()
    for name, (_, help_text) in PROBES.items():
        p = psub.add_parser(name, help=help_text, description=help_text, parents=[shared])
        p.set_defaults(func=_cmd_probe)
        if name in OPTIONS:
            OPTIONS[name](p)


def _safe(module: ModuleType, name: str, root: Path, args: argparse.Namespace) -> dict:
    try:
        return module.probe(name, root, args)
    except Exception as error:  # noqa: BLE001 - one failing dataset must not stop a sweep
        return {"name": name, "error": f"{type(error).__name__}: {error}"[:300], "traceback": traceback.format_exc()}


def _render(module: ModuleType, result: dict) -> str:
    if "error" in result:
        return f"{result['name']}: error {result['error']}"
    return module.render(result)


def run(probe: str, args: argparse.Namespace) -> list[dict]:
    """Run ``probe`` on the datasets ``args`` names, print each result and write ``--out``; the results."""
    from joblib import Parallel, delayed  # noqa: PLC0415 - with the probes' dependencies

    from data_foundry.probes import inputs  # noqa: PLC0415

    module = _module(probe)
    if args.built and not getattr(module, "READS_BUILT", True):
        raise SystemExit(f"probe {probe}: --built is not supported (it reads the definition and its raw files)")
    names = inputs.dataset_names(args.root) if args.all else list(args.names)
    if not names:
        raise SystemExit(f"probe {probe}: name at least one dataset, or pass --all")
    for line in getattr(module, "header", lambda _args: [])(args):
        print(line)
    results = Parallel(n_jobs=args.jobs)(delayed(_safe)(module, n, args.root, args) for n in names)
    for result in results:
        print(_render(module, result), flush=True)
    if args.out:
        args.out.mkdir(parents=True, exist_ok=True)
        for result in results:
            (args.out / f"{result['name']}.json").write_text(json.dumps(result, indent=1, default=str))
        summary = getattr(module, "summary", None)
        text = summary(results) if summary else "\n".join(f"- {_render(module, r)}" for r in results) + "\n"
        (args.out / "summary.md").write_text(text)
        if hasattr(module, "write_extra"):
            module.write_extra(args.out, results)
    return results


def _cmd_probe(args: argparse.Namespace) -> int:
    results = run(args.probe, args)
    return 1 if any("error" in r for r in results) else 0
