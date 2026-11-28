"""Fixtures several test modules use; the plain helpers they share are in ``helpers.py``."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from data_foundry.schema import DATA_FOUNDRY_WAREHOUSE_ENV


@pytest.fixture
def warehouse(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """A temporary warehouse holding the raw file of the toy definition (``helpers.DEFINITION``): 600 rows."""
    root = tmp_path / "warehouse"
    rng = np.random.default_rng(0)
    raw = pd.DataFrame(
        {
            "row_id": np.arange(600),
            "x1": rng.normal(size=600),
            "colour": rng.choice(["red", "green", "blue"], size=600),
            "y": rng.integers(0, 2, size=600),
        },
    )
    (root / "toy_ds").mkdir(parents=True)
    raw.to_csv(root / "toy_ds" / "toy.csv", index=False)
    monkeypatch.setenv(DATA_FOUNDRY_WAREHOUSE_ENV, str(root))
    return root
