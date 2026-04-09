"""Exhaustive tests for DataFrame dtype preservation through parquet save/load round-trips."""

from __future__ import annotations

import json
import logging

import numpy as np
import pandas as pd
import pandas.testing as pdt
from data_foundry.curation_container import CuratedContainer
from data_foundry.schema import (
    DatasetMetadata,
    PredictiveMLSplitsMetadata,
    PredictiveMLTaskMetadata,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_metadata(tmp_path):
    """Return (dataset_metadata, task_metadata, splits_metadata) with target='target'."""
    dataset_metadata = DatasetMetadata(
        unique_name="dtype_test",
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
        objective_metric_name="roc_auc",
    )
    splits_metadata = PredictiveMLSplitsMetadata(
        splits_comment="toy",
        splits={0: {0: ([0, 1], [2, 3])}},
    )
    return dataset_metadata, task_metadata, splits_metadata


def _round_trip(df: pd.DataFrame, tmp_path, *, as_test_dataset: bool = False) -> pd.DataFrame:
    """Save a CuratedContainer and load it back, returning the loaded DataFrame."""
    dataset_metadata, task_metadata, splits_metadata = _make_metadata(tmp_path)

    if as_test_dataset:
        # Use a trivial main dataset so target column exists
        main_df = pd.DataFrame({"target": [0, 1, 0, 1], "x": [1, 2, 3, 4]})
        container = CuratedContainer(
            dataset=main_df,
            test_dataset=df,
            dataset_metadata=dataset_metadata,
            task_metadata=task_metadata,
            experiment_metadata=splits_metadata,
        )
        save_path = container.save()
        loaded = CuratedContainer.load(save_path, load_test_data=True)
        return loaded.test_dataset
    # Ensure the df has a 'target' column for the task metadata
    if "target" not in df.columns:
        df = df.copy()
        df["target"] = [0, 1, 0, 1]
    container = CuratedContainer(
        dataset=df,
        dataset_metadata=dataset_metadata,
        task_metadata=task_metadata,
        experiment_metadata=splits_metadata,
    )
    save_path = container.save()
    loaded = CuratedContainer.load(save_path)
    return loaded.dataset


# ---------------------------------------------------------------------------
# Numeric dtypes
# ---------------------------------------------------------------------------


class TestNumericDtypes:
    def test_int64(self, tmp_path):
        df = pd.DataFrame({"a": pd.array([1, 2, 3, 4], dtype="int64"), "target": [0, 1, 0, 1]})
        result = _round_trip(df, tmp_path)
        pdt.assert_frame_equal(result, df)

    def test_int32(self, tmp_path):
        df = pd.DataFrame({"a": pd.array([1, 2, 3, 4], dtype="int32"), "target": [0, 1, 0, 1]})
        result = _round_trip(df, tmp_path)
        pdt.assert_frame_equal(result, df)

    def test_int16(self, tmp_path):
        df = pd.DataFrame({"a": pd.array([1, 2, 3, 4], dtype="int16"), "target": [0, 1, 0, 1]})
        result = _round_trip(df, tmp_path)
        pdt.assert_frame_equal(result, df)

    def test_int8(self, tmp_path):
        df = pd.DataFrame({"a": pd.array([1, 2, 3, 4], dtype="int8"), "target": [0, 1, 0, 1]})
        result = _round_trip(df, tmp_path)
        pdt.assert_frame_equal(result, df)

    def test_uint8(self, tmp_path):
        df = pd.DataFrame({"a": pd.array([1, 2, 3, 4], dtype="uint8"), "target": [0, 1, 0, 1]})
        result = _round_trip(df, tmp_path)
        pdt.assert_frame_equal(result, df)

    def test_uint16(self, tmp_path):
        df = pd.DataFrame({"a": pd.array([1, 2, 3, 4], dtype="uint16"), "target": [0, 1, 0, 1]})
        result = _round_trip(df, tmp_path)
        pdt.assert_frame_equal(result, df)

    def test_uint32(self, tmp_path):
        df = pd.DataFrame({"a": pd.array([1, 2, 3, 4], dtype="uint32"), "target": [0, 1, 0, 1]})
        result = _round_trip(df, tmp_path)
        pdt.assert_frame_equal(result, df)

    def test_uint64(self, tmp_path):
        df = pd.DataFrame({"a": pd.array([1, 2, 3, 4], dtype="uint64"), "target": [0, 1, 0, 1]})
        result = _round_trip(df, tmp_path)
        pdt.assert_frame_equal(result, df)

    def test_float32(self, tmp_path):
        df = pd.DataFrame({"a": pd.array([1.1, 2.2, 3.3, 4.4], dtype="float32"), "target": [0, 1, 0, 1]})
        result = _round_trip(df, tmp_path)
        pdt.assert_frame_equal(result, df)

    def test_float64(self, tmp_path):
        df = pd.DataFrame({"a": pd.array([1.1, 2.2, 3.3, 4.4], dtype="float64"), "target": [0, 1, 0, 1]})
        result = _round_trip(df, tmp_path)
        pdt.assert_frame_equal(result, df)


# ---------------------------------------------------------------------------
# Nullable (pandas extension) dtypes
# ---------------------------------------------------------------------------


class TestNullableDtypes:
    def test_nullable_int64(self, tmp_path):
        df = pd.DataFrame({"a": pd.array([1, 2, None, 4], dtype="Int64"), "target": [0, 1, 0, 1]})
        result = _round_trip(df, tmp_path)
        pdt.assert_frame_equal(result, df)

    def test_nullable_int32(self, tmp_path):
        df = pd.DataFrame({"a": pd.array([1, 2, None, 4], dtype="Int32"), "target": [0, 1, 0, 1]})
        result = _round_trip(df, tmp_path)
        pdt.assert_frame_equal(result, df)

    def test_nullable_int16(self, tmp_path):
        df = pd.DataFrame({"a": pd.array([1, 2, None, 4], dtype="Int16"), "target": [0, 1, 0, 1]})
        result = _round_trip(df, tmp_path)
        pdt.assert_frame_equal(result, df)

    def test_nullable_int8(self, tmp_path):
        df = pd.DataFrame({"a": pd.array([1, 2, None, 4], dtype="Int8"), "target": [0, 1, 0, 1]})
        result = _round_trip(df, tmp_path)
        pdt.assert_frame_equal(result, df)

    def test_nullable_uint8(self, tmp_path):
        df = pd.DataFrame({"a": pd.array([1, 2, None, 4], dtype="UInt8"), "target": [0, 1, 0, 1]})
        result = _round_trip(df, tmp_path)
        pdt.assert_frame_equal(result, df)

    def test_nullable_uint16(self, tmp_path):
        df = pd.DataFrame({"a": pd.array([1, 2, None, 4], dtype="UInt16"), "target": [0, 1, 0, 1]})
        result = _round_trip(df, tmp_path)
        pdt.assert_frame_equal(result, df)

    def test_nullable_uint32(self, tmp_path):
        df = pd.DataFrame({"a": pd.array([1, 2, None, 4], dtype="UInt32"), "target": [0, 1, 0, 1]})
        result = _round_trip(df, tmp_path)
        pdt.assert_frame_equal(result, df)

    def test_nullable_uint64(self, tmp_path):
        df = pd.DataFrame({"a": pd.array([1, 2, None, 4], dtype="UInt64"), "target": [0, 1, 0, 1]})
        result = _round_trip(df, tmp_path)
        pdt.assert_frame_equal(result, df)

    def test_nullable_float32(self, tmp_path):
        df = pd.DataFrame({"a": pd.array([1.1, 2.2, None, 4.4], dtype="Float32"), "target": [0, 1, 0, 1]})
        result = _round_trip(df, tmp_path)
        pdt.assert_frame_equal(result, df)

    def test_nullable_float64(self, tmp_path):
        df = pd.DataFrame({"a": pd.array([1.1, 2.2, None, 4.4], dtype="Float64"), "target": [0, 1, 0, 1]})
        result = _round_trip(df, tmp_path)
        pdt.assert_frame_equal(result, df)

    def test_nullable_boolean(self, tmp_path):
        df = pd.DataFrame({"a": pd.array([True, False, None, True], dtype="boolean"), "target": [0, 1, 0, 1]})
        result = _round_trip(df, tmp_path)
        pdt.assert_frame_equal(result, df)

    def test_nullable_string(self, tmp_path):
        df = pd.DataFrame({"a": pd.array(["x", "y", None, "z"], dtype="string"), "target": [0, 1, 0, 1]})
        result = _round_trip(df, tmp_path)
        pdt.assert_frame_equal(result, df)


# ---------------------------------------------------------------------------
# Boolean dtype
# ---------------------------------------------------------------------------


class TestBoolDtype:
    def test_numpy_bool(self, tmp_path):
        df = pd.DataFrame({"a": pd.array([True, False, True, False], dtype="bool"), "target": [0, 1, 0, 1]})
        result = _round_trip(df, tmp_path)
        pdt.assert_frame_equal(result, df)


# ---------------------------------------------------------------------------
# Category dtype
# ---------------------------------------------------------------------------


class TestCategoryDtype:
    def test_string_category(self, tmp_path):
        df = pd.DataFrame(
            {"a": pd.Categorical(["cat", "dog", "cat", "bird"]), "target": [0, 1, 0, 1]},
        )
        result = _round_trip(df, tmp_path)
        pdt.assert_frame_equal(result, df, check_categorical=False)
        assert result["a"].dtype.name == "category"

    def test_int_category(self, tmp_path):
        df = pd.DataFrame(
            {"a": pd.Categorical([1, 2, 3, 1]), "target": [0, 1, 0, 1]},
        )
        result = _round_trip(df, tmp_path)
        pdt.assert_frame_equal(result, df, check_categorical=False)
        assert result["a"].dtype.name == "category"

    def test_ordered_category(self, tmp_path):
        cat_type = pd.CategoricalDtype(categories=["low", "mid", "high"], ordered=True)
        df = pd.DataFrame(
            {"a": pd.Categorical(["low", "mid", "high", "low"], dtype=cat_type), "target": [0, 1, 0, 1]},
        )
        result = _round_trip(df, tmp_path)
        pdt.assert_frame_equal(result, df, check_categorical=False)
        assert result["a"].dtype.name == "category"
        assert set(result["a"].cat.categories) == {"low", "mid", "high"}

    def test_category_with_na(self, tmp_path):
        df = pd.DataFrame(
            {"a": pd.Categorical(["cat", None, "dog", "cat"]), "target": [0, 1, 0, 1]},
        )
        result = _round_trip(df, tmp_path)
        pdt.assert_frame_equal(result, df, check_categorical=False)
        assert result["a"].dtype.name == "category"
        assert pd.isna(result["a"].iloc[1])


# ---------------------------------------------------------------------------
# Datetime / Timedelta dtypes
# ---------------------------------------------------------------------------


class TestDatetimeDtypes:
    def test_datetime64_ns(self, tmp_path):
        df = pd.DataFrame(
            {
                "a": pd.to_datetime(["2020-01-01", "2020-06-15", "2021-01-01", "2021-12-31"]),
                "target": [0, 1, 0, 1],
            }
        )
        result = _round_trip(df, tmp_path)
        pdt.assert_frame_equal(result, df)

    def test_datetime64_with_na(self, tmp_path):
        df = pd.DataFrame(
            {
                "a": pd.to_datetime(["2020-01-01", None, "2021-01-01", "2021-12-31"]),
                "target": [0, 1, 0, 1],
            }
        )
        result = _round_trip(df, tmp_path)
        pdt.assert_frame_equal(result, df)


# ---------------------------------------------------------------------------
# String / object dtypes
# ---------------------------------------------------------------------------


class TestStringDtypes:
    def test_pandas_string_dtype(self, tmp_path):
        df = pd.DataFrame({"a": pd.array(["hello", "world", "foo", "bar"], dtype="string"), "target": [0, 1, 0, 1]})
        result = _round_trip(df, tmp_path)
        pdt.assert_frame_equal(result, df)


# ---------------------------------------------------------------------------
# Mixed-column DataFrames (realistic scenarios)
# ---------------------------------------------------------------------------


class TestMixedColumns:
    def test_typical_tabular_dataset(self, tmp_path):
        """A realistic mix of dtypes that a curated dataset might have."""
        df = pd.DataFrame(
            {
                "id": pd.array([1, 2, 3, 4], dtype="int64"),
                "score": pd.array([0.95, 0.42, 0.78, 0.13], dtype="float64"),
                "label": pd.Categorical(["A", "B", "A", "C"]),
                "is_valid": pd.array([True, False, True, True], dtype="bool"),
                "name": pd.array(["alice", "bob", "carol", "dave"], dtype="string"),
                "target": [0, 1, 0, 1],
            }
        )
        result = _round_trip(df, tmp_path)
        pdt.assert_frame_equal(result, df, check_categorical=False)

        assert result["id"].dtype == np.dtype("int64")
        assert result["score"].dtype == np.dtype("float64")
        assert result["label"].dtype.name == "category"
        assert result["is_valid"].dtype == np.dtype("bool")
        assert result["name"].dtype == pd.StringDtype()

    def test_nullable_int_with_missing_values(self, tmp_path):
        """The classic parquet gotcha: int column with NAs should stay Int64, not become float64."""
        df = pd.DataFrame(
            {
                "a": pd.array([1, None, 3, None], dtype="Int64"),
                "b": pd.array([10, 20, None, 40], dtype="Int32"),
                "target": [0, 1, 0, 1],
            }
        )
        result = _round_trip(df, tmp_path)
        pdt.assert_frame_equal(result, df)

    def test_multiple_categories_and_numerics(self, tmp_path):
        df = pd.DataFrame(
            {
                "cat1": pd.Categorical(["a", "b", "a", "c"]),
                "cat2": pd.Categorical([1, 2, 3, 1]),
                "num1": pd.array([1.0, 2.0, 3.0, 4.0], dtype="float32"),
                "num2": pd.array([100, 200, 300, 400], dtype="int16"),
                "target": [0, 1, 0, 1],
            }
        )
        result = _round_trip(df, tmp_path)
        pdt.assert_frame_equal(result, df, check_categorical=False)


# ---------------------------------------------------------------------------
# Test dataset dtype preservation
# ---------------------------------------------------------------------------


class TestTestDatasetDtypes:
    def test_test_dataset_dtypes_preserved(self, tmp_path):
        """Dtypes and values should be preserved for the test_dataset as well."""
        test_df = pd.DataFrame(
            {
                "a": pd.array([10, None, 30, 40], dtype="Int64"),
                "b": pd.Categorical(["x", "y", "x", "z"]),
                "c": pd.array([True, False, None, True], dtype="boolean"),
                "target": [0, 1, 0, 1],
            }
        )
        result = _round_trip(test_df, tmp_path, as_test_dataset=True)
        pdt.assert_frame_equal(result, test_df, check_categorical=False)

    def test_test_dataset_load_via_load_test_dataset_method(self, tmp_path):
        """Dtypes and values should be preserved when using load_test_dataset() method."""
        dataset_metadata, task_metadata, splits_metadata = _make_metadata(tmp_path)
        main_df = pd.DataFrame({"target": [0, 1, 0, 1], "x": [1, 2, 3, 4]})
        test_df = pd.DataFrame(
            {
                "a": pd.array([1, None, 3, 4], dtype="Int32"),
                "target": [0, 1, 0, 1],
            }
        )
        container = CuratedContainer(
            dataset=main_df,
            test_dataset=test_df,
            dataset_metadata=dataset_metadata,
            task_metadata=task_metadata,
            experiment_metadata=splits_metadata,
        )
        save_path = container.save()

        loaded = CuratedContainer.load(save_path, load_test_data=False)
        assert loaded.test_dataset is None

        result = loaded.load_test_dataset()
        pdt.assert_frame_equal(result, test_df)


# ---------------------------------------------------------------------------
# Backward compatibility
# ---------------------------------------------------------------------------


class TestBackwardCompatibility:
    def test_load_without_dtypes_json(self, tmp_path, caplog):
        """Legacy saves without dtypes.json should load with a warning, no crash."""
        dataset_metadata, task_metadata, splits_metadata = _make_metadata(tmp_path)
        df = pd.DataFrame(
            {
                "a": pd.array([1, 2, 3, 4], dtype="Int64"),
                "target": [0, 1, 0, 1],
            }
        )
        container = CuratedContainer(
            dataset=df,
            dataset_metadata=dataset_metadata,
            task_metadata=task_metadata,
            experiment_metadata=splits_metadata,
        )
        save_path = container.save()

        # Remove dtypes.json to simulate a legacy save
        dtypes_file = save_path / "dtypes.json"
        assert dtypes_file.exists()
        dtypes_file.unlink()

        with caplog.at_level(logging.WARNING, logger="data_foundry.curation_container"):
            loaded = CuratedContainer.load(save_path)

        assert loaded.dataset is not None
        assert "not found" in caplog.text

    def test_load_test_dataset_without_test_dtypes_json(self, tmp_path, caplog):
        """Legacy saves without test_dtypes.json should load with a warning."""
        dataset_metadata, task_metadata, splits_metadata = _make_metadata(tmp_path)
        main_df = pd.DataFrame({"target": [0, 1, 0, 1], "x": [1, 2, 3, 4]})
        test_df = pd.DataFrame({"a": pd.array([1, None, 3, 4], dtype="Int32"), "target": [0, 1, 0, 1]})

        container = CuratedContainer(
            dataset=main_df,
            test_dataset=test_df,
            dataset_metadata=dataset_metadata,
            task_metadata=task_metadata,
            experiment_metadata=splits_metadata,
        )
        save_path = container.save()

        # Remove test_dtypes.json
        test_dtypes_file = save_path / "test_dtypes.json"
        assert test_dtypes_file.exists()
        test_dtypes_file.unlink()

        with caplog.at_level(logging.WARNING, logger="data_foundry.curation_container"):
            loaded = CuratedContainer.load(save_path, load_test_data=True)

        assert loaded.test_dataset is not None
        assert "not found" in caplog.text

    def test_dtypes_json_with_extra_column(self, tmp_path, caplog):
        """If dtypes.json mentions a column not in the DataFrame, warn and skip."""
        dataset_metadata, task_metadata, splits_metadata = _make_metadata(tmp_path)
        df = pd.DataFrame({"a": [1, 2, 3, 4], "target": [0, 1, 0, 1]})
        container = CuratedContainer(
            dataset=df,
            dataset_metadata=dataset_metadata,
            task_metadata=task_metadata,
            experiment_metadata=splits_metadata,
        )
        save_path = container.save()

        # Add a fake column to dtypes.json
        dtypes_file = save_path / "dtypes.json"
        with dtypes_file.open("r") as f:
            dtypes = json.load(f)
        dtypes["nonexistent_column"] = "float64"
        with dtypes_file.open("w") as f:
            json.dump(dtypes, f)

        with caplog.at_level(logging.WARNING, logger="data_foundry.curation_container"):
            loaded = CuratedContainer.load(save_path)

        assert loaded.dataset is not None
        assert "nonexistent_column" in caplog.text

    def test_dtypes_json_with_invalid_dtype(self, tmp_path, caplog):
        """If a dtype string is invalid/uncastable, warn and skip that column."""
        dataset_metadata, task_metadata, splits_metadata = _make_metadata(tmp_path)
        df = pd.DataFrame({"a": ["hello", "world", "foo", "bar"], "target": [0, 1, 0, 1]})
        container = CuratedContainer(
            dataset=df,
            dataset_metadata=dataset_metadata,
            task_metadata=task_metadata,
            experiment_metadata=splits_metadata,
        )
        save_path = container.save()

        # Corrupt the dtype for column 'a'
        dtypes_file = save_path / "dtypes.json"
        with dtypes_file.open("r") as f:
            dtypes = json.load(f)
        dtypes["a"] = "int64"  # strings can't be cast to int64
        with dtypes_file.open("w") as f:
            json.dump(dtypes, f)

        with caplog.at_level(logging.WARNING, logger="data_foundry.curation_container"):
            loaded = CuratedContainer.load(save_path)

        assert loaded.dataset is not None
        assert "Failed to cast" in caplog.text


# ---------------------------------------------------------------------------
# dtypes.json file contents
# ---------------------------------------------------------------------------


class TestDtypesJsonFile:
    def test_dtypes_json_is_written(self, tmp_path):
        """The dtypes.json file should exist after save."""
        dataset_metadata, task_metadata, splits_metadata = _make_metadata(tmp_path)
        df = pd.DataFrame({"a": [1, 2, 3, 4], "target": [0, 1, 0, 1]})
        container = CuratedContainer(
            dataset=df,
            dataset_metadata=dataset_metadata,
            task_metadata=task_metadata,
            experiment_metadata=splits_metadata,
        )
        save_path = container.save()
        assert (save_path / "dtypes.json").exists()

    def test_dtypes_json_contents(self, tmp_path):
        """The dtypes.json should contain correct dtype strings."""
        dataset_metadata, task_metadata, splits_metadata = _make_metadata(tmp_path)
        df = pd.DataFrame(
            {
                "a": pd.array([1, 2, 3, 4], dtype="Int64"),
                "b": pd.Categorical(["x", "y", "x", "z"]),
                "c": pd.array([1.0, 2.0, 3.0, 4.0], dtype="float32"),
                "target": [0, 1, 0, 1],
            }
        )
        container = CuratedContainer(
            dataset=df,
            dataset_metadata=dataset_metadata,
            task_metadata=task_metadata,
            experiment_metadata=splits_metadata,
        )
        save_path = container.save()

        with (save_path / "dtypes.json").open("r") as f:
            dtypes = json.load(f)

        assert dtypes["a"] == "Int64"
        assert dtypes["b"] == "category"
        assert dtypes["c"] == "float32"

    def test_test_dtypes_json_is_written(self, tmp_path):
        """The test_dtypes.json file should exist after save when test_dataset is present."""
        dataset_metadata, task_metadata, splits_metadata = _make_metadata(tmp_path)
        main_df = pd.DataFrame({"target": [0, 1, 0, 1], "x": [1, 2, 3, 4]})
        test_df = pd.DataFrame({"target": [0, 1, 0, 1], "x": [5, 6, 7, 8]})
        container = CuratedContainer(
            dataset=main_df,
            test_dataset=test_df,
            dataset_metadata=dataset_metadata,
            task_metadata=task_metadata,
            experiment_metadata=splits_metadata,
        )
        save_path = container.save()
        assert (save_path / "test_dtypes.json").exists()

    def test_no_test_dtypes_json_when_no_test_dataset(self, tmp_path):
        """test_dtypes.json should NOT exist when there's no test_dataset."""
        dataset_metadata, task_metadata, splits_metadata = _make_metadata(tmp_path)
        df = pd.DataFrame({"a": [1, 2, 3, 4], "target": [0, 1, 0, 1]})
        container = CuratedContainer(
            dataset=df,
            dataset_metadata=dataset_metadata,
            task_metadata=task_metadata,
            experiment_metadata=splits_metadata,
        )
        save_path = container.save()
        assert not (save_path / "test_dtypes.json").exists()


# ---------------------------------------------------------------------------
# Checksum stability: dtype restoration should not break existing checksums
# ---------------------------------------------------------------------------


class TestChecksumStability:
    def test_checksum_stable_after_round_trip(self, tmp_path):
        """Loading a saved container should produce the same checksum."""
        dataset_metadata, task_metadata, splits_metadata = _make_metadata(tmp_path)
        df = pd.DataFrame(
            {
                "a": pd.array([1, None, 3, 4], dtype="Int64"),
                "b": pd.Categorical(["x", "y", "x", "z"]),
                "target": [0, 1, 0, 1],
            }
        )
        container = CuratedContainer(
            dataset=df,
            dataset_metadata=dataset_metadata,
            task_metadata=task_metadata,
            experiment_metadata=splits_metadata,
        )
        original_checksum = container.checksum
        save_path = container.save()

        loaded = CuratedContainer.load(save_path)
        recomputed_checksum = loaded._create_checksum()

        assert original_checksum == loaded.checksum
        assert original_checksum == recomputed_checksum
