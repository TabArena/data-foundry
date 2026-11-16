"""Approved custom train caps survive changes to the collection budget API."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import load_definition
from data_foundry.v2.dataset import effective_row_budget, raw_name

ROOT = Path(__file__).resolve().parents[1] / "datasets" / "_dev" / "tabarena-v0pt2"
# Fixed source-row memberships measured with the originally qualified sampler, seed 4267.
EXPECTED = {
    "duolingo_spaced_repetition_recall": {
        "0": [[2, 6, 7, 10, 24, 30, 34, 43, 47, 49, 55, 58, 63, 66, 69, 74, 75, 77, 79, 82], [87, 89]],
        "1": [[2, 6, 7, 10, 24, 28, 30, 34, 43, 47, 49, 55, 58, 63, 66, 69, 74, 75, 77, 79], [84, 86]],
        "2": [[2, 6, 7, 10, 19, 24, 28, 30, 34, 43, 47, 49, 55, 58, 63, 66, 69, 74, 75, 77], [82, 83]],
    },
    "fugaku_hpc_job_failure": {
        "0": [[2, 3, 5, 12, 15, 20, 33, 34, 42, 49, 52, 55, 62, 68, 77, 79, 84, 90, 91, 93], [104, 107]],
        "1": [[2, 3, 5, 12, 15, 20, 33, 34, 39, 42, 44, 49, 52, 54, 55, 62, 68, 71, 77, 79], [84, 90]],
        "2": [[2, 3, 5, 11, 12, 15, 19, 20, 33, 34, 39, 42, 44, 49, 52, 54, 55, 62, 68, 71], [72, 79]],
    },
}


def definition(name, monkeypatch):
    """Use small caps to exercise the approved protocol on fixed synthetic rows."""
    cls = load_definition(ROOT / name / "dataset.py")
    module = sys.modules[cls.__module__]
    monkeypatch.setattr(module, "TRAIN_CAP", 20)
    monkeypatch.setattr(module, "TEST_CAP", 2)
    assert effective_row_budget(cls) is None
    assert raw_name(cls) == name
    return cls(), module


def test_duolingo_custom_caps_keep_the_approved_training_draw(monkeypatch):
    """Check exact source-row identity and the one-day training gap."""
    name = "duolingo_spaced_repetition_recall"
    ds, _module = definition(name, monkeypatch)
    frame = pd.DataFrame({"timestamp": pd.date_range("2013-02-01", periods=90, freq="8h"), "source_row": np.arange(90)})
    plan = ds._make_splits(frame)
    for repeat, folds in plan.splits.items():
        train, test = folds[0]
        assert [plan.df.source_row.iloc[side].tolist() for side in (train, test)] == EXPECTED[name][str(repeat)]
        assert plan.df.timestamp.iloc[train].max() < plan.df.timestamp.iloc[test].min() - pd.Timedelta(days=1)


def test_fugaku_custom_caps_preserve_maturity_filter_and_class_quotas(monkeypatch):
    """Delayed outcomes cannot enter the capped, class-proportional training draw."""
    name = "fugaku_hpc_job_failure"
    _ds, module = definition(name, monkeypatch)
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
    selected, report = module._select_temporal(frame, module._window_spec())
    assert report["trimmed"]
    assert any(window["excluded_late_labels"] > 0 for window in report["windows"])
    for repeat, window in enumerate(report["windows"]):
        train, test = [(selected._split_roles & (1 << (2 * repeat + side))) != 0 for side in [0, 1]]
        assert [selected._source_row[side].tolist() for side in (train, test)] == EXPECTED[name][str(repeat)]
        assert selected.edt[train].lt(pd.Timestamp(window["cutoff"])).all()
