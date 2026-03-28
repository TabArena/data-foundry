from __future__ import annotations

from pathlib import Path

import pytest
from data_foundry.schema import (
    DatasetMetadata,
    PredictiveMLSplitsMetadata,
    PredictiveMLTaskMetadata,
)


@pytest.fixture
def base_dataset_metadata_kwargs(tmp_path) -> dict:
    return {
        "unique_name": "toy",
        "dataset_year": "2025",
        "domain_str": "finance",
        "dataset_source": "Kaggle",
        "original_dataset_source_download_link": "http://example",
        "download_description": "desc",
        "academic_reference_bibtex": "bib",
        "academic_reference_bibtex_key": "key",
        "license": None,
        "data_tags": ["IID"],
        "curation_comments": None,
        "local_data_directory_base": str(tmp_path),
    }


@pytest.mark.parametrize(
    ("version_from_unique_name", "expected_path_suffix", "expected_save_suffix"),
    [
        (None, "toy", "toy/abc123"),
        ("toy_base", "toy_base", "toy_base/versions/abc123"),
    ],
)
def test_dataset_metadata_path_and_save_path(
    base_dataset_metadata_kwargs,
    version_from_unique_name,
    expected_path_suffix,
    expected_save_suffix,
):
    dm = DatasetMetadata(
        **base_dataset_metadata_kwargs,
        version_from_unique_name=version_from_unique_name,
    )

    assert dm.path == Path(base_dataset_metadata_kwargs["local_data_directory_base"]) / expected_path_suffix
    assert dm.get_save_path(uuid="abc123") == Path(base_dataset_metadata_kwargs["local_data_directory_base"]) / expected_save_suffix


@pytest.mark.parametrize(
    ("problem_type", "expected"),
    [
        ("binary_classification", True),
        ("multiclass_classification", True),
        ("regression", False),
    ],
)
def test_predictive_task_is_classification(problem_type, expected):
    tm = PredictiveMLTaskMetadata(
        target_column_name="y",
        problem_type=problem_type,
        objective_metric_name="metric",
    )
    assert tm.is_classification == expected


@pytest.mark.parametrize(
    "task_kwargs",
    [
        {
            "group_on": "group_id",
            "time_on": "ts",
            "group_labels": "per_group",
        },
        {
            "group_on": "group_id",
            "time_on": None,
            "group_labels": None,
        },
    ],
)
def test_predictive_task_invalid_group_time_combinations_raise(task_kwargs):
    with pytest.raises(ValueError):
        PredictiveMLTaskMetadata(
            target_column_name="y",
            problem_type="regression",
            objective_metric_name="rmse",
            **task_kwargs,
        )


def test_predictive_splits_metadata_basic():
    splits = {0: {0: ([0, 1], [2, 3])}}
    sm = PredictiveMLSplitsMetadata(splits_comment="test", splits=splits)
    assert sm.splits == splits
    assert sm.type_adapter_id == "predictive-ml-splits-mold-v1"
