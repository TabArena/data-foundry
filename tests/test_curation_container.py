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
) -> tuple[pd.DataFrame, DatasetMetadata, PredictiveMLTaskMetadata, PredictiveMLSplitsMetadata]:
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


# --- Save / load round-trip ---
def test_curated_container_save_load_checksum_and_files(make_toy_objects, tmp_path):
    df, dataset_metadata, task_metadata, splits_metadata = make_toy_objects

    curated = CuratedContainer(
        dataset=df,
        dataset_metadata=dataset_metadata,
        task_metadata=task_metadata,
        experiment_metadata=splits_metadata,
    )

    save_path = curated.save(save_dir=tmp_path)
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


def test_save_and_load_with_test_dataset(make_toy_objects, toy_test_dataset, tmp_path):
    df, dataset_metadata, task_metadata, splits_metadata = make_toy_objects
    curated = CuratedContainer(
        dataset=df,
        test_dataset=toy_test_dataset,
        dataset_metadata=dataset_metadata,
        task_metadata=task_metadata,
        experiment_metadata=splits_metadata,
    )

    save_path = curated.save(save_dir=tmp_path)
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
    tmp_path,
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
    save_path = curated.save(save_dir=tmp_path)

    loaded = CuratedContainer.load(
        save_path,
        load_dataset=load_dataset,
        load_test_data=load_test_data,
    )

    assert (loaded.dataset is None) is expect_dataset_none
    assert (loaded.test_dataset is None) is expect_test_none


def test_load_test_dataset_uses_loaded_from_path(make_toy_objects, toy_test_dataset, tmp_path):
    df, dataset_metadata, task_metadata, splits_metadata = make_toy_objects
    curated = CuratedContainer(
        dataset=df,
        test_dataset=toy_test_dataset,
        dataset_metadata=dataset_metadata,
        task_metadata=task_metadata,
        experiment_metadata=splits_metadata,
    )
    save_path = curated.save(save_dir=tmp_path)

    loaded = CuratedContainer.load(save_path, load_test_data=False)
    assert loaded.test_dataset is None

    got = loaded.load_test_dataset()
    pdt.assert_frame_equal(got, toy_test_dataset)


def test_load_test_dataset_raises_without_path_or_file(make_toy_objects, tmp_path):
    df, dataset_metadata, task_metadata, splits_metadata = make_toy_objects
    curated = CuratedContainer(
        dataset=df,
        dataset_metadata=dataset_metadata,
        task_metadata=task_metadata,
        experiment_metadata=splits_metadata,
    )

    with pytest.raises(ValueError, match="Path must be provided"):
        curated.load_test_dataset()

    save_path = curated.save(save_dir=tmp_path)
    loaded = CuratedContainer.load(save_path)
    with pytest.raises(ValueError, match="does not include a test dataset"):
        loaded.load_test_dataset()


# --- Backward compatibility ---
def test_load_backward_compatible_licence_key(make_toy_objects, tmp_path):
    df, dataset_metadata, task_metadata, splits_metadata = make_toy_objects
    curated = CuratedContainer(
        dataset=df,
        dataset_metadata=dataset_metadata,
        task_metadata=task_metadata,
        experiment_metadata=splits_metadata,
    )
    save_path = curated.save(save_dir=tmp_path)

    dataset_meta_file = save_path / f"dataset_metadata.{dataset_metadata.type_adapter_id}.json"
    with dataset_meta_file.open("r") as f:
        payload = json.load(f)
    payload["licence"] = payload.pop("license")
    with dataset_meta_file.open("w") as f:
        json.dump(payload, f)

    loaded = CuratedContainer.load(save_path)
    assert loaded.dataset_metadata.license is None


# --- Checksum behaviour ---
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


def test_checksum_is_deterministic(make_toy_objects):
    df, dataset_metadata, task_metadata, splits_metadata = make_toy_objects
    curated = CuratedContainer(
        dataset=df,
        dataset_metadata=dataset_metadata,
        task_metadata=task_metadata,
        experiment_metadata=splits_metadata,
    )
    assert curated._create_checksum() == curated._create_checksum()


def test_checksum_changes_when_task_metadata_changes(make_toy_objects):
    df, dataset_metadata, task_metadata, splits_metadata = make_toy_objects
    task_metadata_alt = PredictiveMLTaskMetadata(
        target_column_name="target",
        problem_type="binary_classification",
        objective_metric_name="different_metric",
    )
    c1 = CuratedContainer(
        dataset=df,
        dataset_metadata=dataset_metadata,
        task_metadata=task_metadata,
        experiment_metadata=splits_metadata,
    )
    c2 = CuratedContainer(
        dataset=df,
        dataset_metadata=dataset_metadata,
        task_metadata=task_metadata_alt,
        experiment_metadata=splits_metadata,
    )
    assert c1.checksum != c2.checksum


def test_checksum_changes_when_experiment_metadata_changes(make_toy_objects):
    df, dataset_metadata, task_metadata, splits_metadata = make_toy_objects
    splits_alt = PredictiveMLSplitsMetadata(
        splits_comment="different splits",
        splits={0: {0: ([0, 2], [1, 3])}},
    )
    c1 = CuratedContainer(
        dataset=df,
        dataset_metadata=dataset_metadata,
        task_metadata=task_metadata,
        experiment_metadata=splits_metadata,
    )
    c2 = CuratedContainer(
        dataset=df,
        dataset_metadata=dataset_metadata,
        task_metadata=task_metadata,
        experiment_metadata=splits_alt,
    )
    assert c1.checksum != c2.checksum


# --- UUID and properties ---
def test_uuid_is_auto_generated(make_toy_objects):
    df, dataset_metadata, task_metadata, splits_metadata = make_toy_objects
    curated = CuratedContainer(
        dataset=df,
        dataset_metadata=dataset_metadata,
        task_metadata=task_metadata,
        experiment_metadata=splits_metadata,
    )
    assert curated.uuid is not None
    assert isinstance(curated.uuid, str)
    assert len(curated.uuid) > 0


def test_uuid_uniqueness(make_toy_objects):
    df, dataset_metadata, task_metadata, splits_metadata = make_toy_objects
    c1 = CuratedContainer(
        dataset=df,
        dataset_metadata=dataset_metadata,
        task_metadata=task_metadata,
        experiment_metadata=splits_metadata,
    )
    c2 = CuratedContainer(
        dataset=df,
        dataset_metadata=dataset_metadata,
        task_metadata=task_metadata,
        experiment_metadata=splits_metadata,
    )
    assert c1.uuid != c2.uuid


def test_unique_name_property(make_toy_objects):
    df, dataset_metadata, task_metadata, splits_metadata = make_toy_objects
    curated = CuratedContainer(
        dataset=df,
        dataset_metadata=dataset_metadata,
        task_metadata=task_metadata,
        experiment_metadata=splits_metadata,
    )
    assert curated.unique_name == f"toy_ds/{curated.uuid}"


def test_container_metadata_property(make_toy_objects):
    df, dataset_metadata, task_metadata, splits_metadata = make_toy_objects
    curated = CuratedContainer(
        dataset=df,
        dataset_metadata=dataset_metadata,
        task_metadata=task_metadata,
        experiment_metadata=splits_metadata,
    )
    meta = curated.container_metadata
    assert set(meta.keys()) == {"uuid", "checksum", "version_comment"}
    assert meta["uuid"] == curated.uuid
    assert meta["checksum"] == curated.checksum
    assert meta["version_comment"] is None


def test_version_comment_saved_and_loaded(make_toy_objects, tmp_path):
    df, dataset_metadata, task_metadata, splits_metadata = make_toy_objects
    curated = CuratedContainer(
        dataset=df,
        dataset_metadata=dataset_metadata,
        task_metadata=task_metadata,
        experiment_metadata=splits_metadata,
        version_comment="First stable release",
    )
    save_path = curated.save(save_dir=tmp_path)
    loaded = CuratedContainer.load(save_path)
    assert loaded.version_comment == "First stable release"


# --- Extra (non-core) artifacts ---
def _save_curated(make_toy_objects, tmp_path):
    df, dataset_metadata, task_metadata, splits_metadata = make_toy_objects
    curated = CuratedContainer(
        dataset=df,
        dataset_metadata=dataset_metadata,
        task_metadata=task_metadata,
        experiment_metadata=splits_metadata,
    )
    return curated.save(save_dir=tmp_path)


def test_extra_file_path_resolves_against_loaded_from_path(make_toy_objects, tmp_path):
    save_path = _save_curated(make_toy_objects, tmp_path)
    (save_path / "sidecar.bin").write_bytes(b"hello")

    loaded = CuratedContainer.load(save_path)
    resolved = loaded.extra_file_path("sidecar.bin")
    assert resolved == save_path / "sidecar.bin"
    assert resolved.read_bytes() == b"hello"


def test_extra_file_path_accepts_explicit_path(make_toy_objects, tmp_path):
    save_path = _save_curated(make_toy_objects, tmp_path)
    (save_path / "doc.txt").write_text("readme")
    loaded = CuratedContainer.load(save_path)

    other_dir = tmp_path / "other"
    other_dir.mkdir()
    (other_dir / "doc.txt").write_text("other-readme")
    assert loaded.extra_file_path("doc.txt", path=other_dir).read_text() == "other-readme"


def test_extra_file_path_requires_path_when_unbound(make_toy_objects):
    df, dataset_metadata, task_metadata, splits_metadata = make_toy_objects
    curated = CuratedContainer(
        dataset=df,
        dataset_metadata=dataset_metadata,
        task_metadata=task_metadata,
        experiment_metadata=splits_metadata,
    )
    with pytest.raises(ValueError, match="loaded_from_path"):
        curated.extra_file_path("anything.bin")


@pytest.mark.parametrize("bad", ["", ".", "..", "sub/dir.bin", "back\\slash.bin"])
def test_extra_file_path_rejects_non_bare_names(make_toy_objects, tmp_path, bad):
    save_path = _save_curated(make_toy_objects, tmp_path)
    loaded = CuratedContainer.load(save_path)
    with pytest.raises(ValueError, match="bare file name"):
        loaded.extra_file_path(bad)


@pytest.mark.parametrize(
    "reserved",
    [
        "dataset.parquet",
        "dtypes.json",
        "test_dataset.parquet",
        "test_dtypes.json",
        "container_metadata.json",
    ],
)
def test_extra_file_path_rejects_reserved_names(make_toy_objects, tmp_path, reserved):
    save_path = _save_curated(make_toy_objects, tmp_path)
    loaded = CuratedContainer.load(save_path)
    with pytest.raises(ValueError, match="core container file"):
        loaded.extra_file_path(reserved)


def test_has_extra_file_true_only_when_present(make_toy_objects, tmp_path):
    save_path = _save_curated(make_toy_objects, tmp_path)
    loaded = CuratedContainer.load(save_path)
    assert loaded.has_extra_file("absent.bin") is False
    (save_path / "absent.bin").write_bytes(b"x")
    assert loaded.has_extra_file("absent.bin") is True


def test_has_extra_file_returns_false_for_invalid_names(make_toy_objects, tmp_path):
    save_path = _save_curated(make_toy_objects, tmp_path)
    loaded = CuratedContainer.load(save_path)
    assert loaded.has_extra_file("") is False
    assert loaded.has_extra_file("sub/dir.bin") is False
    assert loaded.has_extra_file("dataset.parquet") is False


def test_list_extra_files_excludes_core_and_metadata(make_toy_objects, tmp_path):
    save_path = _save_curated(make_toy_objects, tmp_path)
    (save_path / "extra_a.parquet").write_bytes(b"")
    (save_path / "extra_b.txt").write_text("hi")
    loaded = CuratedContainer.load(save_path)

    extras = loaded.list_extra_files()
    assert extras == ["extra_a.parquet", "extra_b.txt"]
    for core in [
        "dataset.parquet",
        "dtypes.json",
        "container_metadata.json",
    ]:
        assert core not in extras
    assert not any(name.endswith(".json") and name.count(".") >= 2 for name in extras)


def test_list_extra_files_empty_when_no_path(make_toy_objects):
    df, dataset_metadata, task_metadata, splits_metadata = make_toy_objects
    curated = CuratedContainer(
        dataset=df,
        dataset_metadata=dataset_metadata,
        task_metadata=task_metadata,
        experiment_metadata=splits_metadata,
    )
    assert curated.list_extra_files() == []


def test_versioned_save_path(tmp_path):
    df = pd.DataFrame({"feat": [1, 2], "target": [0, 1]})
    dataset_metadata = DatasetMetadata(
        unique_name="toy_v2",
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
        version_from_unique_name="toy_base",
    )
    task_metadata = PredictiveMLTaskMetadata(
        target_column_name="target",
        problem_type="binary_classification",
        objective_metric_name="roc_auc",
    )
    splits_metadata = PredictiveMLSplitsMetadata(splits_comment="s", splits={0: {0: ([0], [1])}})

    curated = CuratedContainer(
        dataset=df,
        dataset_metadata=dataset_metadata,
        task_metadata=task_metadata,
        experiment_metadata=splits_metadata,
    )
    save_path = curated.save(save_dir=tmp_path)
    assert "versions" in str(save_path)
    assert save_path.exists()
