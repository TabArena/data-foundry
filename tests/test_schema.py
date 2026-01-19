from __future__ import annotations

from pathlib import Path

import pytest
from data_foundry.schema import (
    DatasetMetadata,
    PredictiveMLSplitsMetadata,
    PredictiveMLTaskMetadata,
)


def test_dataset_metadata_path(tmp_path):
    dm = DatasetMetadata(
        unique_name="toy",
        dataset_year="2025",
        domain_str="finance",
        dataset_source="Kaggle",
        original_dataset_source_download_link="http://example",
        download_description="desc",
        academic_reference_bibtex="bib",
        academic_reference_bibtex_key="key",
        licence=None,
        data_tags=["IID"],
        curation_comments=None,
        local_data_directory_base=str(tmp_path),
    )
    assert dm.path == Path(tmp_path) / "toy"


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
        problem_type=problem_type,  # one of the ProblemType literals
        objective_metric_name="metric",
    )
    # The logical expectation: classification types -> True, regression -> False
    assert tm.is_classification == expected


def test_predictive_splits_metadata_basic():
    splits = {0: {0: ([0, 1], [2, 3])}}
    sm = PredictiveMLSplitsMetadata(splits_comment="test", splits=splits)
    assert sm.splits == splits
    assert sm.type_adapter_id == "predictive-ml-splits-mold-v1"
