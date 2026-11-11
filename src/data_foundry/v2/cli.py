"""The ``data-foundry-curation dataset`` subcommands for v2 dataset folders.

::

    data-foundry-curation dataset list  [--root DIR]                    # tasks and parents, with their state
    data-foundry-curation dataset check <name-or-folder> [--root DIR]   # full pipeline, no save, writes README.md
    data-foundry-curation dataset build <name-or-folder> [--root DIR]   # check + save + verify (mints the UUID)
    data-foundry-curation dataset new   <name> [--root DIR]             # scaffold dataset.py
    data-foundry-curation dataset new   <parent>_<variant> --parent <parent> [--root DIR]   # scaffold a child

A dataset is given either as a folder holding ``dataset.py`` or as a name under ``--root`` (default:
``$DATA_FOUNDRY_DATASETS_ROOT``, else the current directory). From the repository, run the commands as
``.venv/bin/python -m data_foundry.curation.cli dataset ...``: another install of the package may come first on PATH.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import sys
from pathlib import Path
from typing import TYPE_CHECKING, get_args

import pandas as pd

from data_foundry.curation._paths import records_dir
from data_foundry.curation.store import load_record
from data_foundry.schema import DatasetSource, Domain
from data_foundry.v2.dataset import (
    CLI_COMMAND,
    DEFINITION_FILENAME,
    REPORT_FILENAME,
    DatasetDefinitionError,
    is_task,
    parent_definition,
)
from data_foundry.v2.registry import discover_definitions, instance, load_definition
from data_foundry.v2.report import read_report

if TYPE_CHECKING:
    import argparse

DATASETS_ROOT_ENV = "DATA_FOUNDRY_DATASETS_ROOT"
"""Environment variable naming the default folder of dataset folders."""

TEMPLATE_DIR_ENV = "DATA_FOUNDRY_V2_TEMPLATE"
"""Environment variable naming the template folder that ``dataset new`` copies."""

_REPO_TEMPLATE = Path(__file__).resolve().parents[3] / "datasets" / "_template"

PROBLEM_TYPES = {
    "regression": ("regression",),
    "binary classification": ("binary_classification",),
    "multiclass classification": ("multiclass_classification",),
    "classification": ("multiclass_classification",),
}


def _root(args: argparse.Namespace) -> Path:
    return Path(args.root or os.environ.get(DATASETS_ROOT_ENV) or ".")


def _folder(args: argparse.Namespace) -> Path:
    target = Path(args.target)
    if (target / DEFINITION_FILENAME).is_file():
        return target
    return _root(args) / args.target


def _cmd_list(args: argparse.Namespace) -> int:
    registry = discover_definitions(_root(args), strict=False)
    parents = {parent_definition(cls).unique_name for cls in registry.values() if parent_definition(cls) is not None}
    for name, cls in registry.items():
        folder = Path(sys.modules[cls.__module__].__file__).parent
        report = read_report(folder / REPORT_FILENAME)
        build = report.get("build") or {}
        state = "not checked" if not report else ("built " + build["uuid"] if build else "checked")
        if report.get("build_stale"):
            state += " (stale)"
        kind = cls.task_metadata.split_regime if is_task(cls) else "parent" if name in parents else "parent, no child"
        parent = parent_definition(cls)
        family = f"  <- {parent.unique_name}" if parent is not None else ""
        print(f"{name:55s} {kind:18s} {state}{family}")
    n_tasks = sum(is_task(cls) for cls in registry.values())
    print(f"{n_tasks} dataset(s) and {len(registry) - n_tasks} parent(s) under {_root(args)}")
    broken = len(list(_root(args).glob(f"*/{DEFINITION_FILENAME}"))) - len(registry)
    if broken:
        print(f"{broken} definition(s) do not import; see the `Skipping <name>` warnings above.", file=sys.stderr)
        return 1
    return 0


def _cmd_check(args: argparse.Namespace) -> int:
    try:
        ds = instance(load_definition(_folder(args)))
        result = ds.check()
    except DatasetDefinitionError as error:  # a partial parent
        print(error, file=sys.stderr)
        return 1
    print(f"Wrote {ds.report_path}")
    return 0 if result.ok else 1


WINDOW_COLUMNS = (
    "window",
    "chosen",
    "test_start",
    "test_end",
    "period",
    "weekdays",
    "n_test",
    "train_share",
    "target_test",
    "target_train",
    "psi_max",
    "psi_median",
    "top_drift",
    "unseen_categories",
)
"""The columns ``dataset windows`` prints; ``--csv`` writes every column."""


def _cmd_windows(args: argparse.Namespace) -> int:
    try:
        ds = instance(load_definition(_folder(args)))
        table = ds.window_stats(
            window=args.window,
            unit=args.unit,
            gap=args.gap,
            gap_unit=args.gap_unit,
            step=args.step,
            min_train_fraction=args.min_train_fraction,
            n_rows=args.rows,
        )
    except DatasetDefinitionError as error:
        print(error, file=sys.stderr)
        return 1
    if args.csv:
        table.to_csv(args.csv, index=False)
        print(f"Wrote {args.csv}")
    shown = table[[c for c in WINDOW_COLUMNS if c in table.columns]].copy()
    shown["chosen"] = shown["chosen"].map({True: "*", False: ""})
    with pd.option_context("display.width", 250, "display.max_columns", None, "display.max_colwidth", 60):
        print(shown.to_string(index=False))
    print(
        f"{len(table)} window(s); * marks the definition's own. Data statistics only, never a model's score: choose "
        "the windows from the use case (SPLIT-15), always with the newest, and declare them with "
        "`TemporalSplits(cutoffs=...)`."
    )
    return 0


def _cmd_build(args: argparse.Namespace) -> int:
    ds = load_definition(_folder(args))()
    if not ds.is_task:
        print(f"{ds.unique_name} is a parent (no `target`): it is never built; build its children.", file=sys.stderr)
        return 1
    ds.build()
    print(f"Wrote {ds.report_path}")
    return 0


# The record's domain and original_source values that name one schema value (`data_foundry.schema.Domain` and
# `DatasetSource`); any other value ("Other" domain, "Company", "?") stays TODO for the curator.
RECORD_DOMAINS = {
    **{d: d for d in get_args(Domain)},
    "handcrafted/toy": "handcrafted",
    "Multimedia (from non-tabular modalities)": "multimedia",
}
RECORD_SOURCES = {
    **{s: s for s in get_args(DatasetSource)},
    "Github": "GitHub",
    "Website": "Other",
}


def _class_name(unique_name: str) -> str:
    name = "".join(part.capitalize() for part in unique_name.split("_"))
    return name if name[:1].isalpha() else f"Dataset{name}"


def _prefill(text: str, record: object | None) -> str:
    """Fill the template fields the curation record can answer; everything else stays TODO."""
    if record is None:
        return text

    def put(field: str, value: str | None) -> None:
        nonlocal text
        if value:
            text = re.sub(rf'(\b{field}\s*=\s*)"TODO"', lambda m: f"{m.group(1)}{json.dumps(value)}", text, count=1)

    put("domain", RECORD_DOMAINS.get(getattr(record, "domain", None) or ""))
    # the publication source of the template's `sources`
    put("platform", RECORD_SOURCES.get(getattr(record, "original_source", None) or ""))
    links = getattr(record, "source_links", None) or []
    put("url", links[0] if links else None)
    put("year", getattr(record, "year", None))
    problem = PROBLEM_TYPES.get((getattr(record, "problem_type", None) or "").strip().lower())
    if problem:
        put("problem_type", problem[0])
    return text


CHILD_TEMPLATE = '''"""Curated dataset definition for `{name}` (data-foundry v2), a child of `{parent}`.

Evidence: README.md.
"""

from __future__ import annotations

from data_foundry.v2 import {imports}

{parent_class} = import_definition("{parent}")


class {class_name}({parent_class}):
    unique_name = "{name}"
    derivation = """
        TODO(verify): how this dataset differs from `{parent}` (its target, split, rows or preprocessing).
    """
{task}'''

CHILD_TASK = """    task_summary = TaskSummary(
        question="TODO(verify): the prediction as a one-line question.",
        use_case="TODO(verify): who uses the prediction, when, and the decision it informs.",
        row="TODO(verify): what one row is.",
        predicted="TODO(verify): the target in plain words, by when after the prediction point.",
        known="TODO(verify): what the model knows then, in plain words.",
        split="TODO(verify): what the test data stands for.",
        fit="direct",  # TODO(verify): "direct", "approximate" or "none"
        fit_reason="TODO(verify): why the data simulates the use case this closely.",
    )

    # The task; the parent's other outcomes stay out of the features (drop them in `_clean` with `super()._clean`)
    target = "TODO"
    problem_type = "TODO"
    metric = Metric.fallback(reason="TODO(verify): where we looked for the source's metric, and found none.")
"""

CHILD_OF_TASK = """
    # A child of a task inherits its target, metric, split and summary; override what differs (a `row_budget`
    # adds its suffix to the name, `<parent>_<variant>_1m`), and `_clean` with `super()._clean(raw)` for rows.
"""


def _scaffold_child(folder: Path, name: str, parent_name: str, root: Path) -> int:
    """Write a child definition of ``parent_name`` into ``folder``."""
    try:
        parent = load_definition(root / parent_name / DEFINITION_FILENAME)
    except (FileNotFoundError, LookupError, ImportError) as error:
        print(f"No parent definition {parent_name!r} under {root}: {error}", file=sys.stderr)
        return 1
    if not name.startswith(f"{parent_name}_"):
        print(f"A child of {parent_name!r} is named `{parent_name}_<variant>`.", file=sys.stderr)
        return 1
    task = is_task(parent)
    text = CHILD_TEMPLATE.format(
        name=name,
        parent=parent_name,
        parent_class=parent.__name__,
        class_name=_class_name(name),
        imports="import_definition" if task else "Metric, TaskSummary, import_definition",
        task=CHILD_OF_TASK if task else CHILD_TASK,
    )
    folder.mkdir(parents=True, exist_ok=True)
    (folder / DEFINITION_FILENAME).write_text(text)
    print(f"Scaffolded {folder}/{DEFINITION_FILENAME}, a child of {parent_name}. Fill in every TODO, then run:")
    print(f"  {CLI_COMMAND} dataset check {folder}")
    return 0


def _cmd_new(args: argparse.Namespace) -> int:
    name = args.target
    folder = _root(args) / name
    if (folder / DEFINITION_FILENAME).exists():
        print(f"{folder / DEFINITION_FILENAME} already exists.", file=sys.stderr)
        return 1
    if getattr(args, "parent", None):
        return _scaffold_child(folder, name, args.parent, _root(args))
    template = Path(os.environ.get(TEMPLATE_DIR_ENV) or _REPO_TEMPLATE)
    if not (template / DEFINITION_FILENAME).is_file():
        print(f"No template at {template} (set ${TEMPLATE_DIR_ENV}).", file=sys.stderr)
        return 1

    record = None
    try:
        record = load_record(Path(args.records_dir or records_dir()) / f"{name}.md")
    except (FileNotFoundError, OSError, ValueError):
        print(f"No curation record for {name!r}; scaffolding without prefill.")

    folder.mkdir(parents=True, exist_ok=True)
    text = (template / DEFINITION_FILENAME).read_text()
    text = text.replace("<unique_name>", name).replace("class ClassName(", f"class {_class_name(name)}(")
    (folder / DEFINITION_FILENAME).write_text(_prefill(text, record))
    for extra in template.iterdir():
        if extra.name != DEFINITION_FILENAME and extra.is_file():
            shutil.copy(extra, folder / extra.name)
    print(f"Scaffolded {folder}/{DEFINITION_FILENAME}. Fill in every TODO, then run:")
    print(f"  {CLI_COMMAND} dataset check {folder}")
    return 0


def add_dataset_parser(sub: argparse._SubParsersAction) -> None:
    """Register the ``dataset`` command group on the curation CLI."""
    p_dataset = sub.add_parser("dataset", help="Work with v2 dataset folders (dataset.py + README.md).")
    dsub = p_dataset.add_subparsers(dest="dataset_command", required=True)

    def add(name: str, func, help_text: str, *, target: bool = True) -> None:
        p = dsub.add_parser(name, help=help_text)
        if target:
            p.add_argument("target", help="Dataset name under --root, or a folder holding dataset.py.")
        p.add_argument("--root", default=None, help=f"Folder of dataset folders (default: ${DATASETS_ROOT_ENV} or .).")
        p.set_defaults(func=func)

    add("list", _cmd_list, "List the datasets under --root with their report state.", target=False)
    add("check", _cmd_check, "Run the pipeline and bundle checks without saving; write README.md.")
    add("build", _cmd_build, "Check, save the container (new UUID), verify it and write README.md.")
    add("new", _cmd_new, "Scaffold a new dataset folder from the template and the curation record.")
    dsub.choices["new"].add_argument(
        "--parent", default=None, help="Scaffold a child of this definition (a folder under --root) instead."
    )
    add("windows", _cmd_windows, "Print the candidate test windows of a temporal dataset with their data statistics.")
    windows = dsub.choices["windows"]
    windows.add_argument("--window", type=int, default=None, help="Window length (default: the declared one).")
    windows.add_argument("--unit", default=None, help="Window unit (default: the declared one).")
    windows.add_argument("--gap", type=int, default=None, help="Gap before each window (default: the declared one).")
    windows.add_argument("--gap-unit", default=None, help="Unit of the gap (default: the declared one).")
    windows.add_argument("--step", type=int, default=None, help="How far candidates move back (default: the window).")
    windows.add_argument(
        "--min-train-fraction",
        type=float,
        default=0.3,
        help="Every train side keeps this share of the rows (0.3, SPLIT-14's lower bound; core windows keep 0.5).",
    )
    windows.add_argument("--rows", type=int, default=100_000, help="Rows sampled per side for the statistics.")
    windows.add_argument("--csv", default=None, help="Also write the full table to this CSV file.")
