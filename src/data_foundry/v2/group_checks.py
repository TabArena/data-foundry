"""Group statistics of a grouped v2 task, shown in the README's "Group structure" section, and their findings.

The statistics are cheap and deterministic, so :meth:`~data_foundry.v2.dataset.AbstractCuratedDataset.check`
computes them for every grouped task:

* the shape: groups, rows per group, the largest group's share, and the test groups per fold (the sample size of a
  score per group);
* the label granularity: the share of groups whose rows all have one label;
* the clustering: how often a row's nearest neighbour (standardised numeric features, a sample of rows) is in its own
  group, against the share expected if groups were unrelated to the features; and the share of the label variance
  the group explains, against the same for shuffled group ids.

The findings (:func:`group_findings`):

* ``groups_test_groups_few`` (warning): a fold tests on fewer than :data:`MIN_TEST_GROUPS` groups.
* ``groups_largest_share_high`` (warning): one group holds more than :data:`MAX_GROUP_SHARE` of the rows.
* ``groups_labels_constant`` (warning): ``labels="per_sample"``, yet at least :data:`CONSTANT_LABEL_SHARE` of the
  groups have a single label.
* ``groups_not_clustered`` (info): rows are no closer to their own group than chance and the group explains no more
  of the label than shuffled groups: the grouping may not be needed.

Model-based diagnostics (the IID vs grouped score gap, learnability across groups with a permutation test) are slow,
so they run on demand: ``scripts/v2/group_probes.py``.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import numpy as np
import pandas as pd

from data_foundry.bundle_checks import CheckResult
from data_foundry.schema import as_column_list

if TYPE_CHECKING:
    from data_foundry.curation_container import CuratedContainer

MIN_TEST_GROUPS = 20
"""A fold with fewer test groups gives a score that rests on few independent units."""

MAX_GROUP_SHARE = 0.20
"""One group with more of the rows dominates every score that counts rows."""

CONSTANT_LABEL_SHARE = 0.95
"""``per_sample`` labels with at least this share of single-label groups are likely one label per group."""

NEIGHBOUR_SAMPLE_ROWS = 20_000
"""Rows sampled for the nearest-neighbour statistic."""

NEAR_CHANCE_FACTOR = 1.5
"""A statistic within this factor of its chance level counts as "close to chance"."""

RANDOM_STATE = 0
"""Seed of the row sample and the shuffled group ids, so the README stays the same for the same data."""


@dataclass(frozen=True)
class GroupStats:
    """The group statistics of one grouped task (see the module docstring)."""

    n_groups: int
    rows_per_group: tuple[int, float, int]
    """Min, median and max rows per group."""
    largest_share: float
    test_groups_per_fold: tuple[int, int]
    """Min and max number of groups in a test fold."""
    single_label_share: float
    neighbour_same_group: float | None
    neighbour_chance: float | None
    label_share_by_group: float | None
    label_share_shuffled: float | None


def group_stats(container: CuratedContainer) -> GroupStats | None:
    """The statistics of a grouped task, or None for an IID or temporal task."""
    grouping = container.grouping
    if grouping is None:
        return None
    df = container.dataset
    columns = as_column_list(grouping.on)
    groups = df.groupby(columns, sort=False, observed=True, dropna=False).ngroup().to_numpy()
    sizes = np.bincount(groups)
    target = df[container.task_metadata.target_column_name]

    test_groups = [
        len(np.unique(groups[np.asarray(test, dtype=int)]))
        for folds in container.experiment_metadata.splits.values()
        for _train, test in folds.values()
    ]
    labels_per_group = target.groupby(groups, sort=False, observed=True).nunique(dropna=True)
    same, chance = _neighbour_share(df, groups, exclude=[*columns, target.name])
    by_group, shuffled = _label_share(target, groups, is_classification=container.task_metadata.is_classification)
    return GroupStats(
        n_groups=len(sizes),
        rows_per_group=(int(sizes.min()), float(np.median(sizes)), int(sizes.max())),
        largest_share=float(sizes.max() / len(df)),
        test_groups_per_fold=(min(test_groups), max(test_groups)),
        single_label_share=float((labels_per_group <= 1).mean()),
        neighbour_same_group=same,
        neighbour_chance=chance,
        label_share_by_group=by_group,
        label_share_shuffled=shuffled,
    )


def group_findings(container: CuratedContainer, stats: GroupStats | None) -> list[CheckResult]:
    """The findings of :func:`group_stats` (see the module docstring)."""
    if stats is None:
        return []
    grouping = container.grouping
    findings = []
    low, high = stats.test_groups_per_fold
    if low < MIN_TEST_GROUPS:
        findings.append(
            CheckResult(
                "groups_test_groups_few",
                "warning",
                f"A test fold holds {low} groups ({low}-{high} per fold, {stats.n_groups} groups in all): a score per "
                "group rests on few independent units, and a score per row on not many more.",
                hint="Keep the dataset only if its signal across groups is real (`scripts/v2/group_probes.py`), and "
                "accept the warning with that reason.",
            ),
        )
    if stats.largest_share > MAX_GROUP_SHARE:
        findings.append(
            CheckResult(
                "groups_largest_share_high",
                "warning",
                f"The largest group holds {stats.largest_share:.0%} of the rows; it dominates every score that counts "
                "rows and the fold it lands in.",
                hint="Check whether the group is real (one entity) or a catch-all value such as 'unknown'.",
            ),
        )
    if grouping.labels == "per_sample" and stats.single_label_share >= CONSTANT_LABEL_SHARE:
        findings.append(
            CheckResult(
                "groups_labels_constant",
                "warning",
                f"labels='per_sample', yet {stats.single_label_share:.1%} of the groups have a single label "
                f"({round((1 - stats.single_label_share) * stats.n_groups):,} of {stats.n_groups:,} have several).",
                hint="If the label is one per group by construction, declare `labels='per_group'`; otherwise say in "
                "the definition why it may differ within a group.",
            ),
        )
    if _near_chance(stats.neighbour_same_group, stats.neighbour_chance) and _near_chance(
        stats.label_share_by_group, stats.label_share_shuffled
    ):
        findings.append(
            CheckResult(
                "groups_not_clustered",
                "info",
                f"Rows are no closer to their own group than chance ({stats.neighbour_same_group:.1%} of nearest "
                f"neighbours vs {stats.neighbour_chance:.1%}), and the group explains no more of the label than "
                f"shuffled groups ({stats.label_share_by_group:.2f} vs {stats.label_share_shuffled:.2f}).",
                hint="The grouping may not be needed: compare IID and grouped scores with "
                "`scripts/v2/group_probes.py`.",
            ),
        )
    return findings


def _near_chance(value: float | None, chance: float | None) -> bool:
    return value is not None and chance is not None and value <= NEAR_CHANCE_FACTOR * chance


def _neighbour_share(df: pd.DataFrame, groups: np.ndarray, *, exclude: list[str]) -> tuple[float | None, float | None]:
    """The share of sampled rows whose nearest other row is in the same group, and that share for unrelated groups."""
    from sklearn.neighbors import NearestNeighbors  # noqa: PLC0415 - heavy import

    numeric = df.drop(columns=[c for c in exclude if c in df.columns]).select_dtypes(include=["number", "bool"])
    if numeric.shape[1] == 0 or len(df) < 3:  # a row, its neighbour and one more
        return None, None
    rng = np.random.default_rng(RANDOM_STATE)
    sample = np.sort(rng.choice(len(df), size=min(NEIGHBOUR_SAMPLE_ROWS, len(df)), replace=False))
    values = numeric.iloc[sample].astype(float)
    spread = values.std()
    values = values.loc[:, spread > 0]
    if values.shape[1] == 0:
        return None, None
    standardised = ((values - values.mean()) / values.std()).fillna(0.0).to_numpy()
    _, neighbours = NearestNeighbors(n_neighbors=2).fit(standardised).kneighbors(standardised)
    sampled_groups = groups[sample]
    same = float(np.mean(sampled_groups[neighbours[:, 1]] == sampled_groups))
    shares = np.bincount(sampled_groups) / len(sampled_groups)
    return same, float(np.sum(shares**2))


def _label_share(
    target: pd.Series, groups: np.ndarray, *, is_classification: bool
) -> tuple[float | None, float | None]:
    """The share of the label variance between group means (eta squared), for the groups and for shuffled groups."""
    if is_classification:
        labels = pd.get_dummies(target.astype(str)).to_numpy(dtype=float)
    else:
        labels = pd.to_numeric(target, errors="coerce").to_numpy(dtype=float)[:, None]
    keep = ~np.isnan(labels).any(axis=1)
    labels, groups = labels[keep], groups[keep]
    total = ((labels - labels.mean(axis=0)) ** 2).sum()
    if total == 0:
        return None, None

    def between(ids: np.ndarray) -> float:
        counts = np.bincount(ids)
        sums = np.stack([np.bincount(ids, weights=labels[:, j]) for j in range(labels.shape[1])], axis=1)
        means = sums[counts > 0] / counts[counts > 0, None]
        return float((counts[counts > 0, None] * (means - labels.mean(axis=0)) ** 2).sum() / total)

    shuffled = np.random.default_rng(RANDOM_STATE).permutation(groups)
    return between(groups), between(shuffled)
