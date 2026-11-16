"""Supply eligible temporal history when a custom definition samples both split sides.

Use ``custom_sample`` from a definition's ``_make_splits`` hook. Apply any label-availability filter before capturing
``population``. The floor check uses that population; the container stores only the sampled rows and positions.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from data_foundry.v2 import RowBudget, SplitPlan, TemporalSplits
from data_foundry.v2.splits import sample_temporal_splits


def custom_sample(frame: pd.DataFrame) -> SplitPlan:
    """Sample fixed training draws while preserving the eligible population for checks."""
    splits = TemporalSplits(window=1, unit="days", n_windows=3, gap=1).splits(frame, "time")
    population = SplitPlan(df=frame, splits={r: dict(folds) for r, folds in splits.items()})
    rank = np.random.default_rng(4267).permutation(len(frame))
    for folds in splits.values():
        for fold, (train, test) in folds.items():
            positions = np.asarray(train)
            folds[fold] = (np.sort(positions[np.argsort(rank[positions])[:20]]), test)
    reduced, sampled, _ = sample_temporal_splits(frame, splits, RowBudget(train=20, test=2))
    return SplitPlan(df=reduced, splits=sampled, before_sampling=population)


if __name__ == "__main__":
    plan = custom_sample(pd.DataFrame({"time": pd.date_range("2020-01-01", periods=90, freq="8h")}))
    print({r: [(len(train), len(test)) for train, test in folds.values()] for r, folds in plan.splits.items()})
