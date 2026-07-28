from __future__ import annotations

import dataclasses

import numpy as np
import pandas as pd
import pytest
from data_foundry.bundle_checks import (
    BundleCheckError,
    run_bundle_checks,
    verify_saved_container,
)
from data_foundry.curation_container import CuratedContainer
from data_foundry.schema import (
    DatasetMetadata,
    PredictiveMLSplitsMetadata,
    PredictiveMLTaskMetadata,
)

BIBTEX = """@misc{toy2025dataset,
  author = {Toy Author},
  title  = {A Toy Dataset},
  year   = {2025},
  howpublished = {\\url{https://example.com/toy}}
}
"""


def make_dataset_metadata(**overrides) -> DatasetMetadata:
    kwargs = {
        "unique_name": "toy_ds",
        "dataset_year": "2025",
        "domain_str": "finance",
        "dataset_source": "Kaggle",
        "original_dataset_source_download_link": "https://example.com/toy",
        "download_description": "kaggle datasets download toy",
        "academic_reference_bibtex": BIBTEX,
        "academic_reference_bibtex_key": "toy2025dataset",
        "license": "CC BY 4.0",
        "data_tags": ["IID"],
        "curation_comments": "Read the CSV.",
    }
    kwargs.update(overrides)
    return DatasetMetadata(**kwargs)


def make_iid_frame(n: int = 60) -> pd.DataFrame:
    rng = np.random.default_rng(0)
    return pd.DataFrame(
        {
            "feat_num": rng.normal(size=n),
            "feat_cat": pd.Categorical(rng.choice(["a", "b", "c"], size=n)),
            "target": pd.Categorical(rng.choice(["yes", "no"], size=n)),
        },
    )


def make_iid_splits(n: int = 60, n_folds: int = 3) -> dict:
    folds = {}
    positions = np.arange(n)
    for fold in range(n_folds):
        test = positions[fold::n_folds]
        train = np.setdiff1d(positions, test)
        folds[fold] = (train.tolist(), test.tolist())
    return {0: folds}


def make_container(df: pd.DataFrame | None = None, **overrides) -> CuratedContainer:
    df = make_iid_frame() if df is None else df
    kwargs = {
        "dataset": df,
        "dataset_metadata": make_dataset_metadata(),
        "task_metadata": PredictiveMLTaskMetadata(
            target_column_name="target",
            problem_type="binary_classification",
            objective_metric_name="roc_auc",
            stratify_on="target",
        ),
        "experiment_metadata": PredictiveMLSplitsMetadata(
            splits_comment="Default splits.",
            splits=make_iid_splits(len(df)),
        ),
    }
    kwargs.update(overrides)
    return CuratedContainer(**kwargs)


def slugs_of(container: CuratedContainer, **kwargs) -> list[str]:
    return run_bundle_checks(container, verbose=False, **kwargs).slugs


# --- The happy path -----------------------------------------------------------------
def test_clean_bundle_has_no_errors():
    report = run_bundle_checks(make_container(), verbose=False)
    assert report.ok, report.summary()
    assert report.errors == []


def test_report_is_printed_when_verbose(capsys):
    run_bundle_checks(make_container(), verbose=True)
    assert "Bundle checks — toy_ds" in capsys.readouterr().out


def test_report_to_dict_round_trips():
    report = run_bundle_checks(make_container(), verbose=False)
    payload = report.to_dict()
    assert payload["unique_name"] == "toy_ds"
    assert payload["counts"]["error"] == 0
    assert payload["n_checks_run"] > 0


def test_report_to_json(tmp_path):
    report = run_bundle_checks(make_container(), verbose=False)
    path = report.to_json(tmp_path / "bundle_checks.json")
    assert path.is_file()


# --- Frame-level checks --------------------------------------------------------------
def test_non_range_index_is_an_error():
    df = make_iid_frame()
    df.index = df.index + 5
    assert "dataset_index_range" in slugs_of(make_container(df))


def test_object_dtype_is_an_error():
    df = make_iid_frame()
    df["feat_obj"] = "text"
    df["feat_obj"] = df["feat_obj"].astype("object")
    assert "dataset_object_dtype" in slugs_of(make_container(df))


def test_constant_and_identifier_columns_are_warnings():
    df = make_iid_frame()
    df["const"] = 1.0
    df["row_id"] = pd.Categorical([f"id_{i}" for i in range(len(df))])
    found = slugs_of(make_container(df))
    assert "dataset_constant_column" in found
    assert "dataset_identifier_column" in found


def test_feature_identical_to_target_is_leakage():
    df = make_iid_frame()
    df["copy_of_target"] = df["target"]
    assert "dataset_feature_equals_target" in slugs_of(make_container(df))


def test_unused_categories_are_flagged():
    df = make_iid_frame()
    df["feat_cat"] = df["feat_cat"].cat.add_categories(["never_used"])
    assert "dataset_unused_categories" in slugs_of(make_container(df))


def test_missing_value_sentinel_is_flagged():
    df = make_iid_frame()
    df["feat_num"] = [-999.0] * 30 + list(range(30))
    assert "dataset_missing_value_sentinel" in slugs_of(make_container(df))


def test_ordered_target_is_flagged_as_unshuffled():
    df = make_iid_frame()
    df = df.sort_values("target").reset_index(drop=True)
    assert "dataset_row_order_leaks_target" in slugs_of(make_container(df))


def test_heavy_checks_are_skipped_above_the_budget():
    found = slugs_of(make_container(), heavy_cell_budget=1)
    assert "dataset_duplicates_skipped" in found


# --- Task metadata against the frame -------------------------------------------------
def test_missing_target_column_is_an_error():
    task = PredictiveMLTaskMetadata(
        target_column_name="not_a_column",
        problem_type="regression",
        objective_metric_name="rmse",
    )
    assert "task_target_column_name_missing_column" in slugs_of(make_container(task_metadata=task))


def test_classification_target_must_be_categorical():
    df = make_iid_frame()
    df["target"] = (df["target"] == "yes").astype(int)
    assert "task_target_dtype" in slugs_of(make_container(df))


def test_binary_problem_type_with_three_classes_is_an_error():
    df = make_iid_frame()
    df["target"] = pd.Categorical(["a", "b", "c"] * (len(df) // 3))
    assert "task_target_class_count" in slugs_of(make_container(df))


def test_target_missing_values_are_an_error():
    df = make_iid_frame()
    df.loc[0, "target"] = None
    assert "task_target_missing_values" in slugs_of(make_container(df))


def test_empty_metric_is_an_error():
    task = PredictiveMLTaskMetadata(
        target_column_name="target",
        problem_type="binary_classification",
        objective_metric_name="",
    )
    assert "task_metric_empty" in slugs_of(make_container(task_metadata=task))


def test_metric_of_the_wrong_problem_type_is_an_error():
    task = PredictiveMLTaskMetadata(
        target_column_name="target",
        problem_type="binary_classification",
        objective_metric_name="rmse",
    )
    assert "task_metric_problem_type_mismatch" in slugs_of(make_container(task_metadata=task))


def test_custom_metric_is_only_info():
    task = PredictiveMLTaskMetadata(
        target_column_name="target",
        problem_type="binary_classification",
        objective_metric_name="amex_metric",
    )
    report = run_bundle_checks(make_container(task_metadata=task), verbose=False)
    assert "task_metric_unknown" in report.slugs
    assert report.ok


def test_continuous_stratify_column_is_an_error():
    df = make_iid_frame()
    task = PredictiveMLTaskMetadata(
        target_column_name="target",
        problem_type="binary_classification",
        objective_metric_name="roc_auc",
        stratify_on="feat_num",
    )
    assert "task_stratify_dtype" in slugs_of(make_container(df, task_metadata=task))


# --- Splits against the frame --------------------------------------------------------
def test_out_of_bounds_split_index_is_an_error():
    splits = PredictiveMLSplitsMetadata(splits_comment="s", splits={0: {0: ([0, 1], [2, 10_000])}})
    assert "splits_index_out_of_bounds" in slugs_of(make_container(experiment_metadata=splits))


def test_train_test_overlap_is_an_error():
    splits = PredictiveMLSplitsMetadata(splits_comment="s", splits={0: {0: ([0, 1, 2], [2, 3])}})
    assert "splits_train_test_overlap" in slugs_of(make_container(experiment_metadata=splits))


def test_duplicate_indices_within_a_split_are_an_error():
    splits = PredictiveMLSplitsMetadata(splits_comment="s", splits={0: {0: ([0, 0, 1], [2, 3])}})
    assert "splits_duplicate_indices" in slugs_of(make_container(experiment_metadata=splits))


def test_unused_rows_are_an_error_for_iid_splits():
    splits = PredictiveMLSplitsMetadata(splits_comment="s", splits={0: {0: ([0, 1], [2, 3])}})
    assert "splits_rows_unused" in slugs_of(make_container(experiment_metadata=splits))


def test_test_class_unseen_in_train_is_an_error():
    df = pd.DataFrame(
        {
            "feat_num": np.arange(10.0),
            "target": pd.Categorical(["a"] * 8 + ["b", "b"]),
        },
    )
    splits = PredictiveMLSplitsMetadata(
        splits_comment="s",
        splits={0: {0: (list(range(8)), [8, 9])}},
    )
    assert "splits_test_class_unseen_in_train" in slugs_of(make_container(df, experiment_metadata=splits))


# --- Temporal tasks ------------------------------------------------------------------
def make_temporal_container(**overrides) -> CuratedContainer:
    n = 40
    df = pd.DataFrame(
        {
            "ts": pd.date_range("2020-01-01", periods=n, freq="D"),
            "feat_num": np.arange(float(n)),
            "target": np.arange(float(n)) * 2,
        },
    )
    kwargs = {
        "dataset": df,
        "dataset_metadata": make_dataset_metadata(data_tags=["Non-IID", "Temporal"]),
        "task_metadata": PredictiveMLTaskMetadata(
            target_column_name="target",
            problem_type="regression",
            objective_metric_name="rmse",
            time_on="ts",
        ),
        "experiment_metadata": PredictiveMLSplitsMetadata(
            splits_comment="Two 10-day windows, newest first.",
            splits={
                0: {0: (list(range(30)), list(range(30, 40)))},
                1: {0: (list(range(20)), list(range(20, 30)))},
            },
            time_horizon=10,
            time_horizon_unit="days",
        ),
    }
    kwargs.update(overrides)
    return CuratedContainer(**kwargs)


def test_clean_temporal_bundle_has_no_errors():
    report = run_bundle_checks(make_temporal_container(), verbose=False)
    assert report.ok, report.summary()


def test_temporal_task_without_time_horizon_is_an_error():
    splits = PredictiveMLSplitsMetadata(
        splits_comment="s",
        splits={0: {0: (list(range(30)), list(range(30, 40)))}},
    )
    assert "meta_time_horizon_missing" in slugs_of(make_temporal_container(experiment_metadata=splits))


def test_time_horizon_without_time_on_is_an_error():
    splits = PredictiveMLSplitsMetadata(
        splits_comment="s",
        splits=make_iid_splits(),
        time_horizon=3,
        time_horizon_unit="days",
    )
    assert "meta_time_horizon_without_time_on" in slugs_of(make_container(experiment_metadata=splits))


def test_temporal_leakage_is_an_error():
    splits = PredictiveMLSplitsMetadata(
        splits_comment="s",
        splits={0: {0: (list(range(35)), list(range(30, 40)))}},
        time_horizon=10,
        time_horizon_unit="days",
    )
    found = slugs_of(make_temporal_container(experiment_metadata=splits))
    assert "splits_temporal_leakage" in found


def test_temporal_folds_must_be_newest_first():
    splits = PredictiveMLSplitsMetadata(
        splits_comment="s",
        splits={
            0: {0: (list(range(20)), list(range(20, 30)))},
            1: {0: (list(range(30)), list(range(30, 40)))},
        },
        time_horizon=10,
        time_horizon_unit="days",
    )
    assert "splits_temporal_order" in slugs_of(make_temporal_container(experiment_metadata=splits))


def test_unsorted_time_column_is_a_warning():
    container = make_temporal_container()
    shuffled = container.dataset.sample(frac=1.0, random_state=0).reset_index(drop=True)
    report = run_bundle_checks(make_temporal_container(dataset=shuffled), verbose=False)
    assert "task_time_on_not_sorted" in report.slugs


def test_horizon_mismatch_is_a_warning():
    splits = PredictiveMLSplitsMetadata(
        splits_comment="s",
        splits={0: {0: (list(range(30)), list(range(30, 40)))}},
        time_horizon=200,
        time_horizon_unit="days",
    )
    assert "meta_time_horizon_mismatch" in slugs_of(make_temporal_container(experiment_metadata=splits))


def test_non_datetime_time_on_needs_no_calendar_horizon():
    df = pd.DataFrame(
        {
            "t_index": np.arange(40),
            "feat_num": np.arange(40.0),
            "target": np.arange(40.0),
        },
    )
    task = PredictiveMLTaskMetadata(
        target_column_name="target",
        problem_type="regression",
        objective_metric_name="rmse",
        time_on="t_index",
    )
    splits = PredictiveMLSplitsMetadata(
        splits_comment="s",
        splits={0: {0: (list(range(30)), list(range(30, 40)))}},
        time_horizon=5,
        time_horizon_unit="years",
    )
    assert "meta_time_horizon_unit" in slugs_of(
        make_temporal_container(dataset=df, task_metadata=task, experiment_metadata=splits),
    )


# --- Grouped tasks -------------------------------------------------------------------
def make_grouped_container(**overrides) -> CuratedContainer:
    df = pd.DataFrame(
        {
            "group": pd.Categorical([f"g{i // 4}" for i in range(40)]),
            "feat_num": np.arange(40.0),
            "target": pd.Categorical(["yes" if (i // 4) % 2 else "no" for i in range(40)]),
        },
    )
    kwargs = {
        "dataset": df,
        "dataset_metadata": make_dataset_metadata(data_tags=["Non-IID", "Grouped"]),
        "task_metadata": PredictiveMLTaskMetadata(
            target_column_name="target",
            problem_type="binary_classification",
            objective_metric_name="roc_auc",
            group_on="group",
            group_labels="per_group",
        ),
        "experiment_metadata": PredictiveMLSplitsMetadata(
            splits_comment="Grouped split.",
            splits={0: {0: (list(range(20)), list(range(20, 40)))}},
        ),
    }
    kwargs.update(overrides)
    return CuratedContainer(**kwargs)


def test_clean_grouped_bundle_has_no_errors():
    report = run_bundle_checks(make_grouped_container(), verbose=False)
    assert report.ok, report.summary()


def test_group_leakage_is_an_error():
    splits = PredictiveMLSplitsMetadata(
        splits_comment="s",
        splits={0: {0: (list(range(19)), list(range(19, 40)))}},
    )
    assert "splits_group_leakage" in slugs_of(make_grouped_container(experiment_metadata=splits))


def test_per_group_labels_must_be_constant_within_a_group():
    container = make_grouped_container()
    df = container.dataset.copy()
    df.loc[0, "target"] = "yes" if df.loc[0, "target"] == "no" else "no"
    assert "task_group_labels_per_group_violated" in slugs_of(make_grouped_container(dataset=df))


def test_group_per_row_is_an_error():
    container = make_grouped_container()
    df = container.dataset.copy()
    df["group"] = pd.Categorical([f"g{i}" for i in range(len(df))])
    assert "task_group_on_unique_per_row" in slugs_of(make_grouped_container(dataset=df))


# --- Dataset metadata coherence ------------------------------------------------------
def test_iid_tags_on_a_grouped_task_are_flagged():
    container = make_grouped_container(dataset_metadata=make_dataset_metadata(data_tags=["IID"]))
    found = slugs_of(container)
    assert "meta_tags_contradict_regime" in found
    assert "meta_tags_missing_regime" in found


def test_non_iid_tags_on_an_iid_task_are_flagged():
    metadata = make_dataset_metadata(data_tags=["Non-IID", "Temporal"])
    assert "meta_tags_contradict_regime" in slugs_of(make_container(dataset_metadata=metadata))


@pytest.mark.parametrize(
    ("bibtex", "key", "slug"),
    [
        ("@misc{a, title = {T}, year = {2025}, author = {A}", "a", "meta_bibtex_unbalanced_braces"),
        ("no entry here", "a", "meta_bibtex_no_entry"),
        (BIBTEX, "", "meta_bibtex_key_empty"),
        (BIBTEX, "other_key", "meta_bibtex_key_not_defined"),
        ("@misc{a, title = {Tour & Travels}, year = {2025}, author = {A}}", "a", "meta_bibtex_latex_hazard"),
    ],
)
def test_bibtex_problems_are_reported(bibtex, key, slug):
    metadata = make_dataset_metadata(academic_reference_bibtex=bibtex, academic_reference_bibtex_key=key)
    assert slug in slugs_of(make_container(dataset_metadata=metadata))


def test_bibtex_key_underscores_are_not_a_latex_hazard():
    bibtex = "@misc{key_with_underscores, title = {T}, year = {2025}, author = {A}, url = {http://a.com/b_c}}"
    metadata = make_dataset_metadata(
        academic_reference_bibtex=bibtex,
        academic_reference_bibtex_key="key_with_underscores",
    )
    assert "meta_bibtex_latex_hazard" not in slugs_of(make_container(dataset_metadata=metadata))


def test_multiple_bibtex_keys_are_accepted():
    bibtex = BIBTEX + "\n@article{second2024entry, title = {S}, year = {2024}, author = {B}}\n"
    metadata = make_dataset_metadata(
        academic_reference_bibtex=bibtex,
        academic_reference_bibtex_key="toy2025dataset,second2024entry",
    )
    found = slugs_of(make_container(dataset_metadata=metadata))
    assert "meta_bibtex_key_not_defined" not in found
    assert "meta_bibtex_key_count" not in found


def test_placeholder_in_metadata_is_an_error():
    metadata = make_dataset_metadata(curation_comments="TODO: describe the preprocessing")
    assert "meta_placeholder_left" in slugs_of(make_container(dataset_metadata=metadata))


def test_censored_data_values_are_not_placeholders():
    metadata = make_dataset_metadata(curation_comments='ZIP codes are censored as "XXX".')
    assert "meta_placeholder_left" not in slugs_of(make_container(dataset_metadata=metadata))


def test_missing_license_is_a_warning():
    metadata = make_dataset_metadata(license=None)
    assert "meta_license_unknown" in slugs_of(make_container(dataset_metadata=metadata))


def test_empty_splits_comment_is_a_warning():
    splits = PredictiveMLSplitsMetadata(splits_comment="", splits=make_iid_splits())
    assert "meta_splits_comment_empty" in slugs_of(make_container(experiment_metadata=splits))


# --- Optional test dataset -----------------------------------------------------------
def test_test_dataset_dtype_mismatch_is_an_error():
    container = make_container()
    test_dataset = container.dataset.head(5).copy()
    test_dataset["feat_num"] = test_dataset["feat_num"].astype("int64")
    container.test_dataset = test_dataset
    assert "test_dataset_dtype_mismatch" in slugs_of(container)


def test_test_dataset_may_omit_the_target():
    container = make_container()
    container.test_dataset = container.dataset.head(5).drop(columns=["target"]).reset_index(drop=True)
    found = slugs_of(container)
    assert "test_dataset_missing_columns" not in found


# --- ignore / raise ------------------------------------------------------------------
def test_ignore_drops_findings():
    metadata = make_dataset_metadata(license=None)
    report = run_bundle_checks(
        make_container(dataset_metadata=metadata),
        ignore=["meta_license_unknown"],
        verbose=False,
    )
    assert "meta_license_unknown" not in report.slugs
    assert report.ignored == ("meta_license_unknown",)


def test_raise_if_errors_raises_and_lists_slugs():
    df = make_iid_frame()
    df.index = df.index + 1
    report = run_bundle_checks(make_container(df), verbose=False)
    with pytest.raises(BundleCheckError, match="dataset_index_range"):
        report.raise_if_errors()


def test_raise_if_errors_returns_self_when_clean():
    report = run_bundle_checks(make_container(), verbose=False)
    assert report.raise_if_errors() is report


# --- Post-export verification --------------------------------------------------------
def test_verify_saved_container_passes_for_a_round_trip(tmp_path):
    container = make_container()
    save_path = container.save(save_dir=tmp_path)
    report = verify_saved_container(save_path, container=container, verbose=False)
    assert report.ok, report.summary()


def test_verify_saved_container_detects_a_missing_file(tmp_path):
    container = make_container()
    save_path = container.save(save_dir=tmp_path)
    (save_path / "dtypes.json").unlink()
    report = verify_saved_container(save_path, container=container, verbose=False)
    assert "export_files_missing" in report.slugs


def test_verify_saved_container_detects_a_changed_dataset(tmp_path):
    container = make_container()
    save_path = container.save(save_dir=tmp_path)
    tampered = pd.read_parquet(save_path / "dataset.parquet")
    tampered.loc[0, "feat_num"] = 42.0
    tampered.to_parquet(save_path / "dataset.parquet", index=False)
    report = verify_saved_container(save_path, container=container, verbose=False)
    assert "export_values_changed" in report.slugs
    assert "export_checksum_mismatch" in report.slugs


def test_verify_saved_container_detects_a_changed_uuid(tmp_path):
    container = make_container()
    save_path = container.save(save_dir=tmp_path)
    report = verify_saved_container(
        save_path,
        container=dataclasses.replace(container, uuid="00000000-0000-7000-8000-00000000dead"),
        verbose=False,
    )
    assert "export_uuid_mismatch" in report.slugs


def test_verify_saved_container_without_reference_container(tmp_path):
    container = make_container()
    save_path = container.save(save_dir=tmp_path)
    report = verify_saved_container(save_path, verbose=False)
    assert report.ok, report.summary()


def test_verify_saved_container_with_test_dataset(tmp_path):
    container = make_container()
    container.test_dataset = container.dataset.head(5).copy()
    save_path = container.save(save_dir=tmp_path)
    report = verify_saved_container(save_path, container=container, verbose=False)
    assert report.ok, report.summary()
