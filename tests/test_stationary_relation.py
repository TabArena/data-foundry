"""The stationary-relation test (SPLIT-32): flat, not flat and inconclusive on synthetic periods."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

pytest.importorskip("lightgbm")

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / ".claude/skills/knowledge-curation/scripts"))

from curation_probes import stationarity


def _data(n_periods=6, rows=1200, drift=False, seed=0, share_jump=False):
    rng = np.random.default_rng(seed)
    n = n_periods * rows
    period = np.repeat(np.arange(n_periods), rows)
    x = rng.normal(size=(n, 4))
    w = np.where(drift & (period >= n_periods - 3), -1.5, 1.5)  # the sign of the first feature flips late
    logit = w * x[:, 0] + 0.8 * x[:, 1]
    if share_jump:
        logit = logit + np.where(period >= n_periods - 2, 2.5, -1.0)
    y = (rng.random(n) < 1 / (1 + np.exp(-logit))).astype(int)
    df = pd.DataFrame(x, columns=["a", "b", "c", "d"])
    df["y"] = y
    df["period"] = period
    return df, period


def _run(df, period, **kw):
    return stationarity.stationary_relation(
        df, "y", "binary", period, exclude_cols=["period"], n_estimators=60, n_jobs=1, seeds=3, report=False, **kw
    )


def test_a_stable_relation_is_flat():
    df, period = _data()
    out = _run(df, period)
    assert out["verdict"] == "flat"
    assert [w["test_period"] for w in out["windows"]] == ["5", "4", "3"]
    assert all(w["lightgbm"]["verdict"] == "flat" for w in out["windows"])


def test_a_drifting_relation_is_not_flat():
    df, period = _data(drift=True)
    out = _run(df, period)
    assert out["verdict"] == "not flat"
    assert out["windows"][-1]["lightgbm"]["gap"] > 0.05  # the first drifted period, trained without it


def test_a_jumping_class_share_counts_as_recording():
    df, period = _data(share_jump=True)
    rc = stationarity.recording_change(df["y"], period, [str(k) for k in range(6)], "binary")
    assert rc["counts"]
    assert rc["factor"] >= 2
    assert _run(df, period)["verdict"] == "not flat"


def test_too_few_rows_are_inconclusive_not_flat():
    df, period = _data(rows=60, seed=3)
    out = _run(df, period, min_rows=40)
    assert out["verdict"] in {"inconclusive", "not flat"}
    assert out["verdict"] != "flat" or all(
        2 * w["lightgbm"]["gap_sd"] <= stationarity.INCONCLUSIVE_RATIO * w["lightgbm"]["floor"] for w in out["windows"]
    )


def test_a_target_without_signal_is_never_flat():
    df, period = _data(seed=5)
    df["y"] = np.random.default_rng(9).integers(0, 2, len(df))
    out = _run(df, period)
    assert all(w["lightgbm"]["verdict"] != "flat" for w in out["windows"])
    assert out["verdict"] != "flat"


def test_unordered_periods_make_every_period_a_window():
    df, period = _data(n_periods=4)
    out = _run(df, period, ordered=False)
    assert sorted(w["test_period"] for w in out["windows"]) == ["0", "1", "2", "3"]


def test_test_periods_pick_windows_by_label():
    df, period = _data(n_periods=4)
    out = _run(df, period, test_periods=["2"])
    assert [w["test_period"] for w in out["windows"]] == ["2"]


def test_the_contemporaneous_side_holds_the_whole_other_half():
    rng = np.random.default_rng(0)
    before, rest = np.arange(100), np.arange(100, 130)
    side = stationarity._contemporaneous(before, rest, 100, rng)
    assert len(side) == 100
    assert set(rest) <= set(side)


def test_test_units_leave_every_training_side():
    df, period = _data(n_periods=4, rows=400)
    units = np.arange(len(df)) // 4  # units of four rows, each within one period
    seen = []

    def stub(x_tr, y_tr, x_te, seed):
        seen.append((set(x_tr.index), set(x_te.index)))
        return np.column_stack([np.full(len(x_te), 0.5), np.full(len(x_te), 0.5)])

    _run(df, period, units=units, foundation=stub, foundation_name="stub", max_foundation_train=10_000)
    for train, test in seen:
        assert not ({u // 4 for u in train} & {u // 4 for u in test})


def test_a_foundation_model_is_reported_beside_lightgbm():
    df, period = _data(n_periods=4)

    def stub(x_tr, y_tr, x_te, seed):
        p = 1 / (1 + np.exp(-1.5 * x_te["f0"].to_numpy()))
        return np.column_stack([1 - p, p])

    out = _run(df, period, foundation=stub, foundation_name="stub")
    assert out["foundation"] == "stub"
    assert all("foundation" in w for w in out["windows"])
    lines = stationarity.stationary_relation_lines(out)
    assert any("stub forward" in line for line in lines)


def test_pooling_the_windows_can_make_a_set_flat():
    windows = [
        {"lightgbm": {"gap": 0.001, "gap_sd": 0.012, "floor": 0.002, "skill": 0.2, "verdict": "inconclusive"}}
        for _ in range(4)
    ]
    out = {"windows": windows, "recording_change": None}
    # each window: 2 SD = 0.024 > 10 floors = 0.02; pooled: 2 * sqrt(4 * 0.012**2) / 4 = 0.012 <= 0.02
    assert stationarity._verdict(out, ["lightgbm"]) == "flat"
    windows[0]["lightgbm"]["skill"] = -0.01
    assert stationarity._verdict(out, ["lightgbm"]) == "inconclusive"


def test_a_pooled_gap_above_two_sds_is_not_flat():
    """Pooling reads the gap both ways: three windows, each inconclusive alone, whose pooled gap of 8 floors stands
    above its two SDs (6.9 floors) are not flat, never flat (SPLIT-32).
    """
    window = {"gap": 0.032, "gap_sd": 0.024, "floor": 0.004, "skill": 0.4}
    window["verdict"] = stationarity._window_verdict(window["gap"], window["gap_sd"], window["floor"], window["skill"])
    assert window["verdict"] == "inconclusive"
    out = {"windows": [{"lightgbm": dict(window)} for _ in range(3)], "recording_change": None}
    assert stationarity._verdict(out, ["lightgbm"]) == "not flat"


def test_a_run_on_fewer_than_the_newest_three_is_partial_and_the_jobs_combine():
    """A verdict covers the newest three periods; one job per window reports `partial`, and `combine_runs` gives the
    verdict of the full run (SPLIT-32).
    """
    df, period = _data()
    full = _run(df, period)
    jobs = [_run(df, period, test_periods=[p]) for p in ("5", "4", "3")]
    assert all(job["verdict"] == "partial" and job["partial_verdict"] == "flat" for job in jobs)
    assert jobs[0]["untested"] == ["4", "3"]
    assert any("verdict: partial" in line for line in stationarity.stationary_relation_lines(jobs[0]))
    combined = stationarity.combine_runs(jobs)
    assert combined["verdict"] == full["verdict"] == "flat"
    assert [w["test_period"] for w in combined["windows"]] == ["5", "4", "3"]
    assert _run(df, period, n_windows=2)["verdict"] == "partial"


def test_a_not_flat_window_stands_in_a_partial_run():
    """One window not flat is enough, so a partial run that finds one reports it (SPLIT-32)."""
    df, period = _data(drift=True)
    assert _run(df, period, test_periods=["3"])["verdict"] == "not flat"


def test_tabpfn_v35_refuses_a_cpu():
    """TabPFN v3.5 runs on a GPU only."""
    with pytest.raises(ValueError, match="on a GPU"):
        stationarity.tabpfn_v35("binary", [0, 1], device="cpu")
