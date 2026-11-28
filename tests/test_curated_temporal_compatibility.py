"""Approved custom test caps survive changes to the collection budget API."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

from data_foundry.definition import load_definition
from data_foundry.definition.dataset import effective_row_budget

ROOT = Path(__file__).resolve().parents[1] / "datasets" / "_dev" / "tabarena-v0pt2"


def test_fugaku_1m_keeps_whole_train_sides_and_caps_the_test_windows(monkeypatch):
    """Every mature earlier row trains; delayed outcomes stay out; each test window keeps at most the cap."""
    cls = load_definition(ROOT / "fugaku_hpc_job_failure_1m" / "dataset.py")
    module = sys.modules[cls.__module__]
    monkeypatch.setattr(module, "TEST_CAP", 2)
    assert effective_row_budget(cls) is not None
    days = pd.date_range("2021-01-01", periods=36, freq="MS").repeat(3)
    row = np.arange(len(days))
    frame = pd.DataFrame(
        {
            "adt": days + pd.to_timedelta(np.tile([0, 3, 7], 36), unit="D"),
            "_source_file": np.zeros(len(row), dtype="uint8"),
            "_source_row": row.astype("uint32"),
            "exit state": pd.Categorical(np.where(row % 4 == 0, "failed", "completed")),
        }
    )
    frame["edt"] = frame.adt + pd.to_timedelta(np.where(row % 19 == 0, 400, 2), unit="D")
    kept, splits, report = module._select_temporal(frame, module._window_spec())
    eligible = module._window_spec().splits(frame, "adt")
    assert report["trimmed"]
    assert any(window["excluded_late_labels"] > 0 for window in report["windows"])
    assert np.all(np.diff(kept) > 0)  # source order kept, each source row at most once
    for repeat, window in enumerate(report["windows"]):
        train, test = (kept[np.asarray(side)] for side in splits[repeat][0])
        all_train, all_test = (np.asarray(side) for side in eligible[repeat][0])
        mature = (
            frame.edt.iloc[all_train].lt(pd.Timestamp(window["cutoff"])).to_numpy()
            & frame.adt.iloc[all_train].lt(pd.Timestamp(window["cutoff"]) - module.GAP).to_numpy()
        )
        assert sorted(train) == sorted(all_train[mature])  # every mature earlier row trains
        assert 0 < len(test) <= 2
        assert set(test) <= set(all_test)
        assert frame.edt.iloc[train].lt(pd.Timestamp(window["cutoff"])).all()
