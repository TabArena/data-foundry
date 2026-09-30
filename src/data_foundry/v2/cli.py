"""The ``data-foundry-curation dataset`` subcommands for v2 dataset folders.

::

    data-foundry-curation dataset list  [--root DIR]
    data-foundry-curation dataset check <name-or-folder> [--root DIR]   # full pipeline, no save, writes report.md
    data-foundry-curation dataset build <name-or-folder> [--root DIR]   # check + save + verify (mints the UUID)
    data-foundry-curation dataset new   <name> [--root DIR]             # scaffold dataset.py + explore.ipynb

A dataset is given either as a folder holding ``dataset.py`` or as a name under ``--root`` (default:
``$DATA_FOUNDRY_DATASETS_ROOT``, else the current directory).
"""

from __future__ import annotations

import json
import os
import re
import shutil
import sys
from pathlib import Path
from typing import TYPE_CHECKING

from data_foundry.curation._paths import records_dir
from data_foundry.curation.store import load_record
from data_foundry.v2.dataset import DEFINITION_FILENAME, REPORT_FILENAME
from data_foundry.v2.registry import discover_datasets, load_definition
from data_foundry.v2.report import read_report

if TYPE_CHECKING:
    import argparse

DATASETS_ROOT_ENV = "DATA_FOUNDRY_DATASETS_ROOT"
"""Environment variable naming the default folder of dataset folders."""

TEMPLATE_DIR_ENV = "DATA_FOUNDRY_V2_TEMPLATE"
"""Environment variable naming the template folder that ``dataset new`` copies."""

_REPO_TEMPLATE = Path(__file__).resolve().parents[3] / "datasets" / "_template" / "v2"

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
    registry = discover_datasets(_root(args), strict=False)
    for name, cls in registry.items():
        folder = Path(sys.modules[cls.__module__].__file__).parent
        report = read_report(folder / REPORT_FILENAME)
        build = report.get("build") or {}
        state = "not checked" if not report else ("built " + build["uuid"] if build else "checked")
        if report.get("build_stale"):
            state += " (stale)"
        print(f"{name:55s} {cls.task_metadata.split_regime:18s} {state}")
    print(f"{len(registry)} dataset(s) under {_root(args)}")
    return 0


def _cmd_check(args: argparse.Namespace) -> int:
    ds = load_definition(_folder(args))()
    result = ds.check()
    print(f"Wrote {ds.report_path}")
    return 0 if result.ok else 1


def _cmd_build(args: argparse.Namespace) -> int:
    ds = load_definition(_folder(args))()
    ds.build()
    print(f"Wrote {ds.report_path}")
    return 0


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
            text = re.sub(rf'({field} = )"TODO"', lambda m: f"{m.group(1)}{json.dumps(value)}", text, count=1)

    put("year", getattr(record, "year", None))
    links = getattr(record, "source_links", None) or []
    put("source_url", links[0] if links else None)
    problem = PROBLEM_TYPES.get((getattr(record, "problem_type", None) or "").strip().lower())
    if problem:
        put("problem_type", problem[0])
    return text


def _cmd_new(args: argparse.Namespace) -> int:
    name = args.target
    folder = _root(args) / name
    if (folder / DEFINITION_FILENAME).exists():
        print(f"{folder / DEFINITION_FILENAME} already exists.", file=sys.stderr)
        return 1
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
    explore = (template / "explore.ipynb").read_text().replace("<unique_name>", name)
    (folder / "explore.ipynb").write_text(explore)
    for extra in template.iterdir():
        if extra.name not in (DEFINITION_FILENAME, "explore.ipynb") and extra.is_file():
            shutil.copy(extra, folder / extra.name)
    print(f"Scaffolded {folder}/ ({DEFINITION_FILENAME}, explore.ipynb). Fill in every TODO, then run:")
    print(f"  data-foundry-curation dataset check {folder}")
    return 0


def add_dataset_parser(sub: argparse._SubParsersAction) -> None:
    """Register the ``dataset`` command group on the curation CLI."""
    p_dataset = sub.add_parser("dataset", help="Work with v2 dataset folders (dataset.py + report.md).")
    dsub = p_dataset.add_subparsers(dest="dataset_command", required=True)

    def add(name: str, func, help_text: str, *, target: bool = True) -> None:
        p = dsub.add_parser(name, help=help_text)
        if target:
            p.add_argument("target", help="Dataset name under --root, or a folder holding dataset.py.")
        p.add_argument("--root", default=None, help=f"Folder of dataset folders (default: ${DATASETS_ROOT_ENV} or .).")
        p.set_defaults(func=func)

    add("list", _cmd_list, "List the datasets under --root with their report state.", target=False)
    add("check", _cmd_check, "Run the pipeline and bundle checks without saving; write report.md.")
    add("build", _cmd_build, "Check, save the container (new UUID), verify it and write report.md.")
    add("new", _cmd_new, "Scaffold a new dataset folder from the template and the curation record.")
