"""The probes' numeric inputs on a subset of rows equal the whole frame's at those rows (``numeric(..., rows=...)``),
and the task probe, which encodes only the rows its capped sides use, gives the same numbers as on the whole frame.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from data_foundry.probes import task as task_probe
from data_foundry.probes.encode import numeric


def _frame(n: int = 400, seed: int = 0) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    x = rng.normal(size=n)
    x[rng.random(n) < 0.2] = np.nan  # missing values: filled with the median over every row, not over the subset
    level = pd.Categorical(rng.choice(["a", "b", "c", None], size=n), categories=["c", "a", "b"])
    return pd.DataFrame(
        {
            "x": x,
            "level": level,
            "when": pd.Timestamp("2024-01-01") + pd.to_timedelta(rng.integers(0, 300, size=n), unit="D"),
            "empty": np.full(n, np.nan),
            "note": rng.choice(["red", "blue"], size=n).astype(object),
            "y": (x > 0).astype(int),
        }
    )


def test_numeric_on_rows_equals_the_whole_frame_at_those_rows() -> None:
    df = _frame()
    rows = np.sort(np.random.default_rng(1).choice(len(df), 57, replace=False))
    whole, names, text = numeric(df, ["y"])
    part, part_names, part_text = numeric(df, ["y"], rows=rows)
    assert (part_names, part_text) == (names, text) == (["x", "level", "when", "empty"], ["note"])
    pd.testing.assert_frame_equal(part, whole.iloc[rows].reset_index(drop=True))
    assert (part["f3"] == 0.0).all()  # a column without values is filled with 0


def test_task_probe_scores_do_not_depend_on_rows_no_side_uses() -> None:
    """A frame with rows past every split (no side reads them, except through the fill medians) gives the scores of
    the frame cut to the rows the sides use, when no value is missing.
    """
    df = _frame().drop(columns=["note", "empty"]).assign(x=lambda d: d["x"].fillna(0.5), level="a")
    df["level"] = pd.Categorical(df["level"], categories=["a"])
    splits = [(np.arange(0, 200), np.arange(200, 260)), (np.arange(0, 260), np.arange(260, 320))]
    full = task_probe.run(df, "y", "binary_classification", splits, time_on="when", max_rows=150, n_jobs=1)
    cut = task_probe.run(df.iloc[:320], "y", "binary_classification", splits, time_on="when", max_rows=150, n_jobs=1)
    assert (full["rows"], cut["rows"]) == (400, 320)
    for key in ("linear", "random_forest", "lightgbm", "dummy", "drift"):
        assert full["scores"][key] == cut["scores"][key], key
