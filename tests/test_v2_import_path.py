"""The old import path `data_foundry.v2` resolves to the modules' new homes while open pull requests still use it."""

from __future__ import annotations

import importlib
import subprocess
import sys

import pytest

MOVED = {
    "metrics": "data_foundry.metrics",
    "encodings": "data_foundry.encodings",
    "special": "data_foundry.special",
    "chemistry": "data_foundry.special.chemistry",
    "spectra": "data_foundry.special.spectra",
    "dataset": "data_foundry.definition.dataset",
    "preprocessing": "data_foundry.definition.preprocessing",
    "registry": "data_foundry.definition.registry",
    "splits": "data_foundry.definition.splits",
    "windows": "data_foundry.definition.windows",
    "report": "data_foundry.definition.report",
}


@pytest.mark.parametrize(("old", "new"), MOVED.items())
def test_an_old_module_path_is_the_new_module(old: str, new: str) -> None:
    assert importlib.import_module(f"data_foundry.v2.{old}") is importlib.import_module(new)


def test_the_old_package_exports_the_definition_api() -> None:
    import data_foundry.definition as new
    import data_foundry.v2 as old

    assert old.AbstractCuratedDataset is new.AbstractCuratedDataset
    assert set(old.__all__) == set(new.__all__)


def test_the_consumer_modules_load_nothing_of_the_build_side() -> None:
    """A benchmark that scores, sub-samples and encodes never imports the definition side or the curation log."""
    code = (
        "import sys; import data_foundry.metrics, data_foundry.sampling, data_foundry.special.chemistry, "
        "data_foundry.special.spectra, data_foundry.encodings, data_foundry.curation_container; "
        "print(' '.join(m for m in sys.modules if m.startswith('data_foundry')))"
    )
    run = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, check=True)  # noqa: S603 - fixed code
    loaded = run.stdout.split()
    heavy = [
        m for m in loaded if m.startswith(("data_foundry.definition", "data_foundry.curation.", "data_foundry.v2"))
    ]
    assert not heavy
    assert "data_foundry.bundle_checks" not in loaded
