from __future__ import annotations

import json

import pandas as pd
import pandas.testing as pdt
import pytest
from data_foundry.curation_container import CuratedContainer
from data_foundry.schema import (
    DatasetMetadata,
    PredictiveMLSplitsMetadata,
    PredictiveMLTaskMetadata,
)


@pytest.fixture
def make_toy_objects(
    tmp_path,
) -> tuple[
    pd.DataFrame, DatasetMetadata, PredictiveMLTaskMetadata, PredictiveMLSplitsMetadata
]:
    df = pd.DataFrame(
        {
            "customer_ID": [1, 2, 3, 4],
            "feat1": [0.1, 0.2, 0.3, 0.4],
            "target": [0, 1, 0, 1],
        }
    )

    dataset_metadata = DatasetMetadata(
        unique_name="toy_ds",
        dataset_year="2025",
        domain_str="finance",
        dataset_source="Kaggle",
        original_dataset_source_download_link="http://example",
        download_description="desc",
        academic_reference_bibtex="bib",
        academic_reference_bibtex_key="key",
        license=None,
        data_tags=["IID"],
        curation_comments=None,
        local_data_directory_base=str(tmp_path),
    )

    task_metadata = PredictiveMLTaskMetadata(
        target_column_name="target",
        problem_type="binary_classification",
        objective_metric_name="amex_metric",
        stratify_on="target",
    )

    splits = {0: {0: ([0, 1], [2, 3])}}
    splits_metadata = PredictiveMLSplitsMetadata(splits_comment="toy splits", splits=splits)

    return df, dataset_metadata, task_metadata, splits_metadata


@pytest.fixture
def toy_test_dataset() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "customer_ID": [10, 11],
            "feat1": [0.9, 1.1],
            "target": [1, 0],
        }
    )


def test_curated_container_save_load_checksum_and_files(make_toy_objects):
    df, dataset_metadata, task_metadata, splits_metadata = make_toy_objects

    curated = CuratedContainer(
        dataset=df,
        dataset_metadata=dataset_metadata,
        task_metadata=task_metadata,
        experiment_metadata=splits_metadata,
    )

    save_path = curated.save()
    assert save_path.exists()
    assert save_path.is_dir()

    expected_files = {
        "dataset.parquet",
        f"dataset_metadata.{dataset_metadata.type_adapter_id}.json",
        f"task_metadata.{task_metadata.type_adapter_id}.json",
        f"experiment_metadata.{splits_metadata.type_adapter_id}.json",
        "container_metadata.json",
    }
    actual_files = {p.name for p in save_path.iterdir()}
    assert expected_files.issubset(actual_files)

    loaded = CuratedContainer.load(save_path)

    loaded_checksum = loaded.checksum
    new_checksum = loaded._create_checksum()
    assert curated.checksum == new_checksum
    assert loaded_checksum == new_checksum

    with (save_path / "container_metadata.json").open("r") as f:
        cm = json.load(f)
    assert cm["uuid"] == curated.uuid
    assert cm["checksum"] == curated.checksum
    assert cm["uuid"] == loaded.uuid
    assert cm["checksum"] == loaded.checksum

    pdt.assert_frame_equal(loaded.dataset, df)

    assert loaded.dataset_metadata.unique_name == dataset_metadata.unique_name
    assert loaded.task_metadata.target_column_name == task_metadata.target_column_name
    assert loaded.experiment_metadata.splits == splits_metadata.splits


def test_save_and_load_with_test_dataset(make_toy_objects, toy_test_dataset):
    df, dataset_metadata, task_metadata, splits_metadata = make_toy_objects
    curated = CuratedContainer(
        dataset=df,
        test_dataset=toy_test_dataset,
        dataset_metadata=dataset_metadata,
        task_metadata=task_metadata,
        experiment_metadata=splits_metadata,
    )

    save_path = curated.save()
    assert (save_path / "test_dataset.parquet").exists()

    loaded = CuratedContainer.load(save_path, load_test_data=True)
    assert loaded.test_dataset is not None
    pdt.assert_frame_equal(loaded.test_dataset, toy_test_dataset)


@pytest.mark.parametrize(
    ("load_dataset", "load_test_data", "expect_dataset_none", "expect_test_none"),
    [
        (True, False, False, True),
        (False, False, True, True),
        (False, True, True, False),
    ],
)
def test_load_flags_behavior(
    make_toy_objects,
    toy_test_dataset,
    load_dataset,
    load_test_data,
    expect_dataset_none,
    expect_test_none,
):
    df, dataset_metadata, task_metadata, splits_metadata = make_toy_objects
    curated = CuratedContainer(
        dataset=df,
        test_dataset=toy_test_dataset,
        dataset_metadata=dataset_metadata,
        task_metadata=task_metadata,
        experiment_metadata=splits_metadata,
    )
    save_path = curated.save()

    loaded = CuratedContainer.load(
        save_path,
        load_dataset=load_dataset,
        load_test_data=load_test_data,
    )

    assert (loaded.dataset is None) is expect_dataset_none
    assert (loaded.test_dataset is None) is expect_test_none


def test_load_test_dataset_uses_loaded_from_path(make_toy_objects, toy_test_dataset):
    df, dataset_metadata, task_metadata, splits_metadata = make_toy_objects
    curated = CuratedContainer(
        dataset=df,
        test_dataset=toy_test_dataset,
        dataset_metadata=dataset_metadata,
        task_metadata=task_metadata,
        experiment_metadata=splits_metadata,
    )
    save_path = curated.save()

    loaded = CuratedContainer.load(save_path, load_test_data=False)
    assert loaded.test_dataset is None

    got = loaded.load_test_dataset()
    pdt.assert_frame_equal(got, toy_test_dataset)


def test_load_test_dataset_raises_without_path_or_file(make_toy_objects):
    df, dataset_metadata, task_metadata, splits_metadata = make_toy_objects
    curated = CuratedContainer(
        dataset=df,
        dataset_metadata=dataset_metadata,
        task_metadata=task_metadata,
        experiment_metadata=splits_metadata,
    )

    with pytest.raises(ValueError, match="Path must be provided"):
        curated.load_test_dataset()

    save_path = curated.save()
    loaded = CuratedContainer.load(save_path)
    with pytest.raises(ValueError, match="does not include a test dataset"):
        loaded.load_test_dataset()


def test_checksum_changes_when_dataset_changes(make_toy_objects):
    df, dataset_metadata, task_metadata, splits_metadata = make_toy_objects
    curated = CuratedContainer(
        dataset=df.copy(),
        dataset_metadata=dataset_metadata,
        task_metadata=task_metadata,
        experiment_metadata=splits_metadata,
    )
    checksum_before = curated._create_checksum()
    curated.dataset.loc[0, "feat1"] = 999.0
    checksum_after = curated._create_checksum()
    assert checksum_before != checksum_after


def test_load_backward_compatible_licence_key(make_toy_objects):
    df, dataset_metadata, task_metadata, splits_metadata = make_toy_objects
    curated = CuratedContainer(
        dataset=df,
        dataset_metadata=dataset_metadata,
        task_metadata=task_metadata,
        experiment_metadata=splits_metadata,
    )
    save_path = curated.save()

    dataset_meta_file = save_path / f"dataset_metadata.{dataset_metadata.type_adapter_id}.json"
    with dataset_meta_file.open("r") as f:
        payload = json.load(f)
    payload["licence"] = payload.pop("license")
    with dataset_meta_file.open("w") as f:
        json.dump(payload, f)

    loaded = CuratedContainer.load(save_path)
    assert loaded.dataset_metadata.license is None

