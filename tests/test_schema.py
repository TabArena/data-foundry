from __future__ import annotations

import pydantic
import pytest
from data_foundry.schema import (
    DEFAULT_LOCAL_DATA_DIR,
    DatasetMetadata,
    PredictiveMLSplitsMetadata,
    PredictiveMLTaskMetadata,
)


@pytest.fixture
def base_dataset_metadata_kwargs() -> dict:
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
    }


def test_dataset_metadata_type_adapter_id(base_dataset_metadata_kwargs):
    dm = DatasetMetadata(**base_dataset_metadata_kwargs)
    assert dm.type_adapter_id == "dataset-mold-v1"


def test_default_local_data_dir_is_string():
    assert isinstance(DEFAULT_LOCAL_DATA_DIR, str)


def test_dataset_metadata_version_comment(base_dataset_metadata_kwargs):
    dm = DatasetMetadata(
        **base_dataset_metadata_kwargs,
        version_from_unique_name="toy_base",
        version_comment="Added more data rows",
    )
    assert dm.version_comment == "Added more data rows"


def test_dataset_metadata_license_string(base_dataset_metadata_kwargs):
    kwargs = dict(base_dataset_metadata_kwargs)
    kwargs["license"] = "CC BY 4.0"
    dm = DatasetMetadata(**kwargs)
    assert dm.license == "CC BY 4.0"


@pytest.mark.parametrize(
    "data_tags",
    [
        ["IID"],
        ["Non-IID", "Temporal"],
        ["Grouped", "Spatial"],
        ["IID", "Anonymized"],
        ["IID", "2ndTierData"],
        ["ForcedIIDFromTemporal"],
        ["WrongDomain"],
        ["GroupedTemporal"],
    ],
)
def test_dataset_metadata_valid_data_tags(base_dataset_metadata_kwargs, data_tags):
    kwargs = dict(base_dataset_metadata_kwargs)
    kwargs["data_tags"] = data_tags
    dm = DatasetMetadata(**kwargs)
    assert dm.data_tags == data_tags


@pytest.mark.parametrize(
    "domain",
    [
        "education",
        "environmental science & climate",
        "biology & life sciences",
        "handcrafted",
        "chemistry & material science",
        "industry & manufacturing",
        "physics & astronomy",
        "multimedia",
        "medical & healthcare",
        "technology & internet",
        "finance",
        "social science",
        "business & marketing",
        "insurance",
    ],
)
def test_dataset_metadata_all_valid_domains(base_dataset_metadata_kwargs, domain):
    kwargs = dict(base_dataset_metadata_kwargs)
    kwargs["domain_str"] = domain
    dm = DatasetMetadata(**kwargs)
    assert dm.domain_str == domain


@pytest.mark.parametrize(
    "source",
    ["Kaggle", "OpenML", "GitHub", "UCI", "HuggingFace", "GOV Website", "Customer", "Other"],
)
def test_dataset_metadata_all_valid_sources(base_dataset_metadata_kwargs, source):
    kwargs = dict(base_dataset_metadata_kwargs)
    kwargs["dataset_source"] = source
    dm = DatasetMetadata(**kwargs)
    assert dm.dataset_source == source


def test_dataset_metadata_invalid_domain_raises(base_dataset_metadata_kwargs):
    kwargs = dict(base_dataset_metadata_kwargs)
    kwargs["domain_str"] = "not_a_domain"
    with pytest.raises(pydantic.ValidationError):
        DatasetMetadata(**kwargs)


def test_dataset_metadata_invalid_source_raises(base_dataset_metadata_kwargs):
    kwargs = dict(base_dataset_metadata_kwargs)
    kwargs["dataset_source"] = "NotASource"
    with pytest.raises(pydantic.ValidationError):
        DatasetMetadata(**kwargs)


def test_dataset_metadata_invalid_tag_raises(base_dataset_metadata_kwargs):
    kwargs = dict(base_dataset_metadata_kwargs)
    kwargs["data_tags"] = ["NotATag"]
    with pytest.raises(pydantic.ValidationError):
        DatasetMetadata(**kwargs)


def test_dataset_metadata_extra_field_raises(base_dataset_metadata_kwargs):
    with pytest.raises(pydantic.ValidationError):
        DatasetMetadata(**base_dataset_metadata_kwargs, nonexistent_field="value")


# --- PredictiveMLTaskMetadata ---
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
        {"group_on": "group_id", "time_on": "ts", "group_labels": "per_group"},
        {"group_on": "group_id", "time_on": None, "group_labels": None},
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


@pytest.mark.parametrize("group_labels", ["per_group", "per_sample"])
def test_predictive_task_valid_group_setup(group_labels):
    tm = PredictiveMLTaskMetadata(
        target_column_name="y",
        problem_type="binary_classification",
        objective_metric_name="roc_auc",
        group_on="customer_id",
        group_labels=group_labels,
    )
    assert tm.group_on == "customer_id"
    assert tm.group_labels == group_labels


def test_predictive_task_group_time_on():
    tm = PredictiveMLTaskMetadata(
        target_column_name="y",
        problem_type="regression",
        objective_metric_name="rmse",
        group_on="customer_id",
        group_labels="per_sample",
        group_time_on="timestamp",
    )
    assert tm.group_time_on == "timestamp"


def test_predictive_task_type_adapter_id():
    tm = PredictiveMLTaskMetadata(
        target_column_name="y",
        problem_type="regression",
        objective_metric_name="rmse",
    )
    assert tm.type_adapter_id == "predictive-ml-task-mold-v1"


def test_predictive_task_extra_field_raises():
    with pytest.raises(pydantic.ValidationError):
        PredictiveMLTaskMetadata(
            target_column_name="y",
            problem_type="regression",
            objective_metric_name="rmse",
            nonexistent_field="value",
        )


def test_predictive_task_time_on_valid():
    tm = PredictiveMLTaskMetadata(
        target_column_name="y",
        problem_type="regression",
        objective_metric_name="rmse",
        time_on="timestamp",
    )
    assert tm.time_on == "timestamp"
    assert tm.group_on is None


def test_predictive_task_stratify_on_list():
    tm = PredictiveMLTaskMetadata(
        target_column_name="y",
        problem_type="binary_classification",
        objective_metric_name="roc_auc",
        stratify_on=["col_a", "col_b"],
    )
    assert tm.stratify_on == ["col_a", "col_b"]


def test_predictive_task_invalid_problem_type_raises():
    with pytest.raises(pydantic.ValidationError):
        PredictiveMLTaskMetadata(
            target_column_name="y",
            problem_type="not_a_type",
            objective_metric_name="rmse",
        )


# --- PredictiveMLSplitsMetadata ---


def test_predictive_splits_metadata_basic():
    splits = {0: {0: ([0, 1], [2, 3])}}
    sm = PredictiveMLSplitsMetadata(splits_comment="test", splits=splits)
    assert sm.splits == splits
    assert sm.type_adapter_id == "predictive-ml-splits-mold-v1"


def test_predictive_splits_metadata_time_horizon():
    splits = {0: {0: ([0, 1], [2, 3])}}
    sm = PredictiveMLSplitsMetadata(
        splits_comment="temporal",
        splits=splits,
        time_horizon=6,
        time_horizon_unit="months",
    )
    assert sm.time_horizon == 6
    assert sm.time_horizon_unit == "months"


@pytest.mark.parametrize("unit", ["steps", "days", "weeks", "months", "years"])
def test_predictive_splits_metadata_all_time_units(unit):
    splits = {0: {0: ([0, 1], [2, 3])}}
    sm = PredictiveMLSplitsMetadata(
        splits_comment="temporal",
        splits=splits,
        time_horizon=1,
        time_horizon_unit=unit,
    )
    assert sm.time_horizon_unit == unit


def test_predictive_splits_metadata_multi_fold():
    splits = {
        0: {0: ([0, 1, 2], [3, 4]), 1: ([0, 3, 4], [1, 2])},
        1: {0: ([1, 2, 3], [0, 4]), 1: ([0, 1, 4], [2, 3])},
    }
    sm = PredictiveMLSplitsMetadata(splits_comment="multi", splits=splits)
    assert len(sm.splits) == 2
    assert len(sm.splits[0]) == 2
    assert len(sm.splits[1]) == 2


def test_predictive_splits_metadata_defaults_are_none():
    sm = PredictiveMLSplitsMetadata(splits_comment="x", splits={0: {0: ([0], [1])}})
    assert sm.time_horizon is None
    assert sm.time_horizon_unit is None
