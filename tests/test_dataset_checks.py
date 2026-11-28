"""Tests for the README's summary tables of a frame (``data_foundry.checks.tables.run_all_checks``)."""

from __future__ import annotations

import pandas as pd
import pytest

from data_foundry.checks import run_all_checks

TABLES = {"summary", "numeric_stats", "cat_stats", "target"}


@pytest.fixture
def base_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "f1": [1.0, 2.0, 3.0, 4.0, 5.0, 1.0],
            "f2": [10, 20, 30, 40, 50, 10],
            "f2_dup": [10, 20, 30, 40, 50, 10],
            "target_clf": pd.Categorical([0, 1, 0, 1, 0, 0]),
            "target_reg": [0.5, 1.5, 2.5, 3.5, 4.5, 0.5],
        }
    )


# --- Return types and structure ---
@pytest.mark.parametrize(
    ("problem_type", "target_feature"),
    [("binary_classification", "target_clf"), ("regression", "target_reg")],
)
def test_run_all_checks_returns_the_readme_tables(base_df, problem_type, target_feature):
    out = run_all_checks(data=base_df, problem_type=problem_type, target_feature=target_feature)
    assert set(out) == TABLES
    assert isinstance(out["summary"], pd.DataFrame)
    assert isinstance(out["target"], pd.DataFrame)
    assert isinstance(out["numeric_stats"], (pd.DataFrame, str))
    assert isinstance(out["cat_stats"], (pd.DataFrame, str))


def test_summary_has_expected_columns(base_df):
    summary = run_all_checks(data=base_df, problem_type="binary_classification", target_feature="target_clf")["summary"]
    for col in ("dtype", "n_missing", "pct_missing", "n_unique", "examples"):
        assert col in summary.columns, f"Expected column '{col}' in summary"


def test_numeric_stats_has_expected_columns(base_df):
    out = run_all_checks(data=base_df, problem_type="binary_classification", target_feature="target_clf")
    assert isinstance(out["numeric_stats"], pd.DataFrame)
    for col in ("count", "mean", "std", "min", "max"):
        assert col in out["numeric_stats"].columns, f"Expected column '{col}' in numeric_stats"


def test_classification_target_df_has_expected_columns(base_df):
    out = run_all_checks(data=base_df, problem_type="binary_classification", target_feature="target_clf")
    assert set(out["target"].columns) == {"count", "pct"}


def test_regression_target_df_has_expected_columns(base_df):
    target_df = run_all_checks(data=base_df, problem_type="regression", target_feature="target_reg")["target"]
    for col in ("y_missing_count", "skew_y", "skew_log", "var_y", "var_log", "log_used", "dist_hint"):
        assert col in target_df.columns, f"Expected column '{col}' in regression target_df"


def test_run_all_checks_prints_nothing(base_df, capsys):
    run_all_checks(data=base_df, problem_type="regression", target_feature="target_reg")
    assert capsys.readouterr().out == ""


def test_run_all_checks_leaves_the_display_options_alone(base_df):
    before = pd.get_option("display.max_rows")
    run_all_checks(data=base_df, problem_type="regression", target_feature="target_reg")
    assert pd.get_option("display.max_rows") == before


# --- Input validation ---


def test_run_all_checks_rejects_object_dtype():
    df = pd.DataFrame({"f1": [1, 2], "obj": ["a", "b"], "target": pd.Categorical([0, 1])})
    with pytest.raises(TypeError, match="object dtype"):
        run_all_checks(data=df, problem_type="binary_classification", target_feature="target")


def test_run_all_checks_rejects_missing_target(base_df):
    with pytest.raises(ValueError, match="not in the DataFrame"):
        run_all_checks(data=base_df, problem_type="binary_classification", target_feature="missing")


@pytest.mark.parametrize(
    "target", [[0, 1, 0, 1], [0.0, 1.0, 0.0, 1.0], [True, False, True, False]], ids=["int", "float", "bool"]
)
def test_classification_rejects_a_target_that_is_no_category(target):
    df = pd.DataFrame({"f1": [1, 2, 3, 4], "target": target})
    with pytest.raises(TypeError, match="Expected category dtype"):
        run_all_checks(data=df, target_feature="target", problem_type="binary_classification")


def test_binary_classification_rejects_wrong_class_count():
    df = pd.DataFrame({"f1": [1, 2, 3, 4, 5, 6], "target": pd.Categorical([0, 1, 2, 0, 1, 2])})
    with pytest.raises(ValueError, match="binary_classification.*3 unique classes"):
        run_all_checks(data=df, target_feature="target", problem_type="binary_classification")


def test_multiclass_classification_rejects_too_few_classes():
    df = pd.DataFrame({"f1": [1, 2, 3, 4], "target": pd.Categorical([0, 1, 0, 1])})
    with pytest.raises(ValueError, match="multiclass_classification.*2 unique classes"):
        run_all_checks(data=df, target_feature="target", problem_type="multiclass_classification")


def test_multiclass_classification_accepts_three_or_more_classes():
    df = pd.DataFrame({"f1": [1, 2, 3, 4, 5, 6], "target": pd.Categorical([0, 1, 2, 0, 1, 2])})
    out = run_all_checks(data=df, target_feature="target", problem_type="multiclass_classification")
    assert out["target"]["count"].sum() == 6


def test_regression_skips_classification_checks():
    """Regression with float target should not trigger classification checks."""
    df = pd.DataFrame({"f1": [1, 2, 3, 4], "target": [0.5, 1.5, 2.5, 3.5]})
    out = run_all_checks(data=df, target_feature="target", problem_type="regression")
    assert "skew_y" in out["target"].columns


# --- Sampling ---
def test_run_all_checks_sampling_branch_runs(base_df):
    df = pd.concat([base_df] * 200, ignore_index=True)
    out = run_all_checks(
        data=df,
        problem_type="binary_classification",
        target_feature="target_clf",
        sample_threshold=20,
        sample_frac=0.2,
        sample_random_state=123,
    )
    assert "examples" in out["summary"].columns
    assert set(out["target"].columns) == {"count", "pct"}
    assert out["target"]["count"].sum() == len(df)  # the class counts stay exact


def test_run_all_checks_sampling_regression_handles_missing_targets():
    df = pd.DataFrame({"f1": range(10), "target": [1.0, None, 3.0, 4.0, None, 6.0, 7.0, 8.0, 9.0, 10.0]})
    out = run_all_checks(
        data=df, problem_type="regression", target_feature="target", sample_threshold=5, sample_frac=0.5
    )
    assert "examples" in out["summary"].columns
    assert out["target"]["y_missing_count"].iloc[0] == 2
    assert out["target"]["dist_hint"].iloc[0] == "insufficient_data"


# --- NaN handling and column kinds ---
def test_nan_values_in_features():
    df = pd.DataFrame(
        {"f1": [1.0, float("nan"), 3.0, 4.0], "f2": [10, 20, 30, 40], "target": pd.Categorical([0, 1, 0, 1])}
    )
    summary = run_all_checks(data=df, problem_type="binary_classification", target_feature="target")["summary"]
    assert summary.loc[summary["index"] == "f1", "n_missing"].iloc[0] == 1


def test_with_categorical_column():
    df = pd.DataFrame(
        {
            "f1": [1.0, 2.0, 3.0, 4.0],
            "cat_col": pd.Categorical(["a", "b", "a", "b"]),
            "target": pd.Categorical([0, 1, 0, 1]),
        }
    )
    out = run_all_checks(data=df, problem_type="binary_classification", target_feature="target")
    assert isinstance(out["cat_stats"], pd.DataFrame)


def test_all_numeric_produces_no_cat_stats():
    df = pd.DataFrame({"f1": [1.0, 2.0, 3.0, 4.0], "f2": [10, 20, 30, 40], "target": [0.5, 1.5, 2.5, 3.5]})
    out = run_all_checks(data=df, problem_type="regression", target_feature="target")
    assert out["cat_stats"] == "No categorical/object features to summarize."


def test_run_all_checks_takes_an_empty_frame() -> None:
    empty = pd.DataFrame({"f1": pd.Series([], dtype=float), "target": pd.Series([], dtype=float)})
    assert set(run_all_checks(data=empty, target_feature="target", problem_type="regression")) == TABLES
