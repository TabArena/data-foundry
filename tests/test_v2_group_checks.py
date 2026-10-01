"""Tests for the group statistics and findings of grouped v2 tasks (``data_foundry.v2.group_checks``)."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
from data_foundry.curation_container import CuratedContainer
from data_foundry.schema import DatasetMetadata, Grouping, PredictiveMLSplitsMetadata, PredictiveMLTaskMetadataV2
from data_foundry.v2 import group_checks
from data_foundry.v2.splits import grouped_splits


def _container(df: pd.DataFrame, grouping: Grouping | None, problem_type: str = "binary_classification"):
    splits = (
        grouped_splits(df, n_repeats=1, n_folds=3, group_on="g", group_labels=grouping.labels, stratify_on=None)
        if grouping is not None
        else {0: {0: (list(range(len(df) // 2)), list(range(len(df) // 2, len(df))))}}
    )
    return CuratedContainer(
        dataset=df,
        dataset_metadata=DatasetMetadata(
            unique_name="toy",
            dataset_year="2025",
            domain_str="finance",
            dataset_source="Other",
            original_dataset_source_download_link="http://example",
            download_description="d",
            academic_reference_bibtex="b",
            academic_reference_bibtex_key="k",
            license=None,
            data_tags=["Non-IID", "Grouped"],
            curation_comments=None,
        ),
        task_metadata=PredictiveMLTaskMetadataV2(
            target_column_name="y", problem_type=problem_type, objective_metric_name="m", grouping=grouping
        ),
        experiment_metadata=PredictiveMLSplitsMetadata(splits_comment="toy", splits=splits),
        uuid="u",
    )


def _frame(n_groups: int, rows: int, *, clustered: bool, label_per_group: bool) -> pd.DataFrame:
    rng = np.random.default_rng(1)
    groups = np.repeat(np.arange(n_groups), rows)
    centres = rng.normal(size=(n_groups, 3)) * (10 if clustered else 0)
    x = centres[groups] + rng.normal(size=(len(groups), 3))
    y = rng.integers(0, 2, n_groups)[groups] if label_per_group else rng.integers(0, 2, len(groups))
    return pd.DataFrame({"g": groups.astype(str), "x0": x[:, 0], "x1": x[:, 1], "x2": x[:, 2], "y": y})


def _slugs(container: CuratedContainer) -> set[str]:
    return {r.slug for r in group_checks.group_findings(container, group_checks.group_stats(container))}


def test_stats_of_a_clustered_grouped_task() -> None:
    df = _frame(30, 4, clustered=True, label_per_group=True)
    stats = group_checks.group_stats(_container(df, Grouping(on="g", labels="per_group", definition="x")))
    assert stats.n_groups == 30
    assert stats.rows_per_group == (4, 4.0, 4)
    assert stats.test_groups_per_fold == (10, 10)
    assert stats.single_label_share == 1.0
    assert stats.neighbour_same_group > 0.9 > stats.neighbour_chance
    assert stats.label_share_by_group == pytest.approx(1.0)


def test_few_test_groups_and_constant_per_sample_labels_are_flagged() -> None:
    df = _frame(30, 4, clustered=True, label_per_group=True)
    slugs = _slugs(_container(df, Grouping(on="g", labels="per_sample", definition="x")))
    assert slugs == {"groups_test_groups_few", "groups_labels_constant"}


def test_unclustered_groups_are_reported() -> None:
    df = _frame(90, 4, clustered=False, label_per_group=False)
    slugs = _slugs(_container(df, Grouping(on="g", labels="per_sample", definition="x")))
    assert slugs == {"groups_not_clustered"}


def test_a_dominant_group_is_flagged() -> None:
    df = _frame(90, 4, clustered=True, label_per_group=False)
    df.loc[: len(df) // 3, "g"] = "big"
    assert "groups_largest_share_high" in _slugs(_container(df, Grouping(on="g", labels="per_sample", definition="x")))


def test_iid_tasks_have_no_group_stats() -> None:
    df = _frame(10, 4, clustered=False, label_per_group=False)
    container = _container(df, None)
    assert group_checks.group_stats(container) is None
    assert group_checks.group_findings(container, None) == []
