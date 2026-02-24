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
    # Toy dataframe
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
    splits_metadata = PredictiveMLSplitsMetadata(
        splits_comment="toy splits", splits=splits
    )

    return df, dataset_metadata, task_metadata, splits_metadata


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

    # expected files
    expected_files = {
        "dataset.parquet",
        f"dataset_metadata.{dataset_metadata.type_adapter_id}.json",
        f"task_metadata.{task_metadata.type_adapter_id}.json",
        f"experiment_metadata.{splits_metadata.type_adapter_id}.json",
        "container_metadata.json",
    }
    actual_files = {p.name for p in save_path.iterdir()}
    assert expected_files.issubset(actual_files)

    # load back
    loaded = CuratedContainer.load(save_path)

    # checksum roundtrip checks
    loaded_checksum = loaded.checksum
    new_checksum = loaded._create_checksum()
    assert curated.checksum == new_checksum
    assert loaded_checksum == new_checksum

    # container metadata file content matches object
    with (save_path / "container_metadata.json").open("r") as f:
        cm = json.load(f)
    assert cm["uuid"] == curated.uuid
    assert cm["checksum"] == curated.checksum
    assert cm["uuid"] == loaded.uuid
    assert cm["checksum"] == loaded.checksum

    # dataset equality (reset indexes to be robust)
    pdt.assert_frame_equal(loaded.dataset, df)

    # metadata sanity checks
    assert loaded.dataset_metadata.unique_name == dataset_metadata.unique_name
    assert loaded.task_metadata.target_column_name == task_metadata.target_column_name
    assert loaded.experiment_metadata.splits == splits_metadata.splits

