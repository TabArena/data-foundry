"""Registry-driven tests over the v2 dataset folders: no per-dataset test file is needed.

Every ``datasets/_dev/tabarena-v0pt2/<name>/dataset.py`` is discovered and checked:

* always: the class imports and validates (one test per folder, so a half-filled scaffold fails its own test and not
  the collection of all the others), and its ``README.md`` belongs to it (skipped while ``dataset.py`` holds a
  ``TODO(verify)`` marker, i.e. a definition waiting for its rebuild);
* always: the working copy's ``collection.py`` sets TabArena v0.2's row budget, and the README keeps it: every test
  side within 500k rows, and every train side within 1M unless the dataset is a ``_1m`` version, which gets the budget
  by its name (whose train sides a benchmark sub-samples to 1M);
* with ``DATA_FOUNDRY_V2_DATA_CHECKS=1`` and the raw data in the warehouse: a fresh ``check()`` gives the
  checksum recorded in ``README.md`` (the definition has not drifted from its evidence). This reads the
  full data, so it is opt-in.
"""

from __future__ import annotations

import ast
import os
import re
from pathlib import Path

import pytest
from data_foundry.collections import TABARENA_V0PT2_ROW_BUDGET as V0PT2_ROW_BUDGET
from data_foundry.v2 import discover_datasets, load_definition, read_report
from data_foundry.v2.dataset import collection_row_budget, effective_row_budget

ROOT = Path(__file__).resolve().parents[1] / "datasets" / "_dev" / "tabarena-v0pt2"
FOLDERS = sorted(path.parent.name for path in ROOT.glob("*/dataset.py")) if ROOT.is_dir() else []
REGISTRY = discover_datasets(ROOT, strict=False) if ROOT.is_dir() else {}
DATA_CHECKS = os.environ.get("DATA_FOUNDRY_V2_DATA_CHECKS") == "1"
PENDING_ERRORS: tuple[str, ...] = ()
"""Bundle-check errors a README may record (none: every definition declares its `Metric`)."""


def test_registry_is_not_empty() -> None:
    """At least one folder imports."""
    if not ROOT.is_dir():
        pytest.skip("no datasets/ tree")
    assert REGISTRY, f"no dataset.py under {ROOT}"


@pytest.mark.parametrize("folder", FOLDERS)
def test_definition_imports(folder: str) -> None:
    """A placeholder such as `problem_type = "TODO"` fails here, for this folder only."""
    assert load_definition(ROOT / folder / "dataset.py").dataset_metadata.unique_name == folder


@pytest.mark.parametrize("name", sorted(REGISTRY))
def test_definition_has_its_report(name: str) -> None:
    """The README.md next to the definition was written by it and records no bundle-check error."""
    ds = REGISTRY[name]()
    assert ds.folder.name == name
    if "TODO(verify)" in (ds.folder / "dataset.py").read_text():
        pytest.skip("dataset.py has TODO(verify) markers: pending its rebuild")
    if ds.task_summary is not None and ds.task_summary.fit == "none":
        pytest.skip(
            "`task_summary` fit is none: pending the curator's retirement decision (`dataset check` refuses it)"
        )
    report = read_report(ds.report_path)
    assert report, (
        f"{ds.report_path} is missing: run `.venv/bin/python -m data_foundry.curation.cli dataset check {ds.folder}`"
    )
    assert report["unique_name"] == name
    assert report["task"]["target"] == ds.task_metadata.target_column_name
    # Tolerated until every definition declares its `Metric` (step 5 of the metric plan): remove it then.
    errors = set(report["bundle_checks"].get("errors") or []) - set(PENDING_ERRORS)
    assert report["bundle_checks"]["ok"] or not errors, f"{name}: README.md records bundle-check errors {errors}"


@pytest.mark.parametrize("name", sorted(REGISTRY))
def test_splits_keep_the_v0pt2_row_budget(name: str) -> None:
    """Every split of the README tests within v0.2's budget, and trains within it unless the dataset is a ``_1m``
    version, which gets the collection's budget by its name (a benchmark sub-samples those train sides).
    """
    ds = REGISTRY[name]()
    assert collection_row_budget(type(ds)) == V0PT2_ROW_BUDGET, f"{name}: `collection.py` sets {V0PT2_ROW_BUDGET}"
    budget = effective_row_budget(type(ds))
    report = read_report(ds.report_path)
    if not report:
        pytest.skip("no README.md yet")
    splits = report["splits"]
    if budget is None:
        assert splits["n_train"]["max"] <= V0PT2_ROW_BUDGET.train, (
            f"{name}: a split trains on {splits['n_train']['max']:,} rows; rename it `{name}_1m`, the version that "
            "gets the collection's budget"
        )
    assert splits["n_test"]["max"] <= V0PT2_ROW_BUDGET.test, f"{name}: a split tests on {splits['n_test']['max']:,}"
    if budget is not None:
        assert splits.get("row_budget") == {"train": budget.train, "test": budget.test}, (
            f"{name}: README.md predates its row budget; re-run `dataset check`"
        )


@pytest.mark.parametrize("name", sorted(REGISTRY))
def test_definition_matches_its_report(name: str) -> None:
    """A fresh check from the raw data gives the checksum in README.md (opt-in)."""
    if not DATA_CHECKS:
        pytest.skip("set DATA_FOUNDRY_V2_DATA_CHECKS=1 to rebuild from the raw data")
    ds = REGISTRY[name]()
    if not ds.raw_dir.is_dir():
        pytest.skip(f"raw data not in the warehouse: {ds.raw_dir}")
    if not read_report(ds.report_path):
        pytest.skip("no README.md yet")
    if "metric_origin" not in read_report(ds.report_path)["task"]:
        pytest.skip("README.md predates the metric spec (every checksum changed): re-run `dataset check`")
    result = ds.check(write_report=False, verbose=False)
    assert result.container.checksum == read_report(ds.report_path)["checksum"], (
        f"{name}: dataset.py no longer gives the checksum in README.md; re-run `dataset check` and review the diff"
    )


def _scores(dataset_py: Path) -> list[str]:
    """The definition's module-level `SCORES` list (scores with no words per level), or none."""
    for node in ast.parse(dataset_py.read_text()).body:
        if isinstance(node, ast.Assign) and any(getattr(target, "id", None) == "SCORES" for target in node.targets):
            return list(ast.literal_eval(node.value))
    return []


@pytest.mark.parametrize("folder", [f for f in FOLDERS if _scores(ROOT / f / "dataset.py")])
def test_scores_ship_as_numbers(folder: str) -> None:
    """A column of `SCORES` is a number (CLEAN-14): no feature type casts it back to a category.

    eryhemato_squamous_disease's 10 scores were numbers after `_clean` and categories after a blanket
    `_feature_types` (GitHub issue #48). Read from the README's type lists, so no data is needed.
    """
    readme = (ROOT / folder / "README.md").read_text()
    typed = set()
    for kind in ("categorical", "ordinal", "string", "datetime"):
        line = re.search(rf"^- {kind} \(\d+\): (.*)$", readme, re.MULTILINE)
        typed |= set(re.findall(r"`([^`]+)`", line.group(1))) if line else set()
    assert not typed & set(_scores(ROOT / folder / "dataset.py")), f"{folder}: `SCORES` columns typed as non-numbers"
