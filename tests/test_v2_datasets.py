"""Registry-driven tests over the v2 dataset folders: no per-dataset test file is needed.

Every ``datasets/_dev/tabarena-v0pt2/<name>/dataset.py`` is discovered and checked:

* always: the class imports and validates (one test per folder, so a half-filled scaffold fails its own test and not
  the collection of all the others), and its ``README.md`` belongs to it (skipped while ``dataset.py`` holds a
  ``TODO(verify)`` marker, i.e. a definition waiting for its rebuild);
* with ``DATA_FOUNDRY_V2_DATA_CHECKS=1`` and the raw data in the warehouse: a fresh ``check()`` gives the
  checksum recorded in ``README.md`` (the definition has not drifted from its evidence). This reads the
  full data, so it is opt-in.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest
from data_foundry.v2 import discover_datasets, load_definition, read_report

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
