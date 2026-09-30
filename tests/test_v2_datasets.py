"""Registry-driven tests over the v2 dataset folders: no per-dataset test file is needed.

Every ``datasets/_dev/tabarena-v0pt2/<name>/dataset.py`` is discovered and checked:

* always: the class imports and validates, and its ``report.md`` belongs to it (skipped while the folder still holds
  the v1 notebook it was migrated from, i.e. before the migration was checked);
* with ``DATA_FOUNDRY_V2_DATA_CHECKS=1`` and the raw data in the warehouse: a fresh ``check()`` gives the
  checksum recorded in ``report.md`` (the definition has not drifted from its evidence). This reads the
  full data, so it is opt-in.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest
from data_foundry.v2 import discover_datasets, read_report

ROOT = Path(__file__).resolve().parents[1] / "datasets" / "_dev" / "tabarena-v0pt2"
REGISTRY = discover_datasets(ROOT) if ROOT.is_dir() else {}
DATA_CHECKS = os.environ.get("DATA_FOUNDRY_V2_DATA_CHECKS") == "1"


def test_registry_is_not_empty() -> None:
    if not ROOT.is_dir():
        pytest.skip("no datasets/ tree")
    assert REGISTRY, f"no dataset.py under {ROOT}"


@pytest.mark.parametrize("name", sorted(REGISTRY))
def test_definition_has_its_report(name: str) -> None:
    ds = REGISTRY[name]()
    assert ds.folder.name == name
    if not ds.report_path.exists() and any(p.name != "explore.ipynb" for p in ds.folder.glob("*.ipynb")):
        pytest.skip("migrated from the v1 notebook next to it; not checked yet (scripts/v2/check_equivalence.py)")
    report = read_report(ds.report_path)
    assert report, f"{ds.report_path} is missing: run `data-foundry-curation dataset check {ds.folder}`"
    assert report["unique_name"] == name
    assert report["task"]["target"] == ds.task_metadata.target_column_name
    assert report["bundle_checks"]["ok"], f"{name}: report.md records bundle-check errors"


@pytest.mark.parametrize("name", sorted(REGISTRY))
def test_definition_matches_its_report(name: str) -> None:
    if not DATA_CHECKS:
        pytest.skip("set DATA_FOUNDRY_V2_DATA_CHECKS=1 to rebuild from the raw data")
    ds = REGISTRY[name]()
    if not ds.raw_dir.is_dir():
        pytest.skip(f"raw data not in the warehouse: {ds.raw_dir}")
    if not read_report(ds.report_path):
        pytest.skip("no report.md yet (migration not checked)")
    result = ds.check(write_report=False, verbose=False)
    assert result.container.checksum == read_report(ds.report_path)["checksum"], (
        f"{name}: dataset.py no longer gives the checksum in report.md; re-run `dataset check` and review the diff"
    )
