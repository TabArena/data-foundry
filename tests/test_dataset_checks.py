from __future__ import annotations

import pandas as pd
import pytest
from data_foundry.dataset_checks import run_all_checks


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


@pytest.fixture
def no_dup_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "f1": [1.0, 2.0, 3.0, 4.0],
            "f2": [10, 20, 30, 40],
            "target": pd.Categorical([0, 1, 0, 1]),
        }
    )


# --- Return types and structure ---
@pytest.mark.parametrize(
    ("problem_type", "target_feature"),
    [("binary_classification", "target_clf"), ("regression", "target_reg")],
)
def test_run_all_checks_returns_expected_types(base_df, problem_type, target_feature):
    out = run_all_checks(
        data=base_df,
        problem_type=problem_type,
        target_feature=target_feature,
        print_report=False,
        sample_threshold=10_000,
    )
    assert len(out) == 5
    df_head, summary, numeric_stats, cat_stats, target_df = out
    assert isinstance(df_head, pd.DataFrame)
    assert isinstance(summary, pd.DataFrame)
    assert isinstance(target_df, pd.DataFrame)
    assert isinstance(numeric_stats, (pd.DataFrame, str))
    assert isinstance(cat_stats, (pd.DataFrame, str))


def test_summary_has_expected_columns(base_df):
    _, summary, _, _, _ = run_all_checks(
        data=base_df,
        problem_type="binary_classification",
        target_feature="target_clf",
        print_report=False,
    )
    for col in ("dtype", "n_missing", "pct_missing", "n_unique", "examples"):
        assert col in summary.columns, f"Expected column '{col}' in summary"


def test_numeric_stats_has_expected_columns(base_df):
    _, _, numeric_stats, _, _ = run_all_checks(
        data=base_df,
        problem_type="binary_classification",
        target_feature="target_clf",
        print_report=False,
    )
    assert isinstance(numeric_stats, pd.DataFrame)
    for col in ("count", "mean", "std", "min", "max"):
        assert col in numeric_stats.columns, f"Expected column '{col}' in numeric_stats"


def test_classification_target_df_has_expected_columns(base_df):
    _, _, _, _, target_df = run_all_checks(
        data=base_df,
        problem_type="binary_classification",
        target_feature="target_clf",
        print_report=False,
    )
    assert "count" in target_df.columns
    assert "pct" in target_df.columns


def test_regression_target_df_has_expected_columns(base_df):
    _, _, _, _, target_df = run_all_checks(
        data=base_df,
        problem_type="regression",
        target_feature="target_reg",
        print_report=False,
    )
    for col in ("y_missing_count", "skew_y", "skew_log", "var_y", "var_log", "log_used", "dist_hint"):
        assert col in target_df.columns, f"Expected column '{col}' in regression target_df"


def test_df_head_is_at_most_5_rows(base_df):
    df_head, _, _, _, _ = run_all_checks(
        data=base_df,
        problem_type="binary_classification",
        target_feature="target_clf",
        print_report=False,
    )
    assert len(df_head) <= 5


# --- Input validation ---


def test_run_all_checks_rejects_object_dtype():
    df = pd.DataFrame({"f1": [1, 2], "obj": ["a", "b"], "target": pd.Categorical([0, 1])})
    with pytest.raises(TypeError, match="object dtype"):
        run_all_checks(
            data=df, problem_type="binary_classification", target_feature="target", print_report=False
        )


def test_run_all_checks_rejects_missing_target(base_df):
    with pytest.raises(ValueError, match="not in the DataFrame"):
        run_all_checks(
            data=base_df, problem_type="binary_classification", target_feature="missing", print_report=False
        )


def test_run_all_checks_requires_classification_or_problem_type(base_df):
    with pytest.raises(ValueError, match="At least one"):
        run_all_checks(data=base_df, target_feature="target_clf", print_report=False)


# --- Sampling ---
def test_run_all_checks_sampling_branch_runs(base_df):
    df = pd.concat([base_df] * 200, ignore_index=True)
    out = run_all_checks(
        data=df,
        problem_type="binary_classification",
        target_feature="target_clf",
        print_report=False,
        sample_threshold=20,
        sample_frac=0.2,
        sample_random_state=123,
    )
    _, summary, _, _, target_df = out
    assert "examples" in summary.columns
    assert set(target_df.columns) == {"count", "pct"}


# --- Duplicate detection ---
def test_run_all_checks_duplicate_checks_prints(capsys, base_df):
    run_all_checks(
        data=base_df,
        problem_type="binary_classification",
        target_feature="target_clf",
        print_report=False,
        duplicate_row_check=True,
        duplicate_column_check=True,
    )
    captured = capsys.readouterr().out
    assert "Duplicate Report" in captured
    assert "Duplicate columns" in captured


def test_duplicate_rows_are_counted(capsys, base_df):
    # base_df has rows 0 and 5 identical (all columns same) → at least 1 duplicate reported
    run_all_checks(
        data=base_df,
        problem_type="binary_classification",
        target_feature="target_clf",
        print_report=False,
        duplicate_row_check=True,
        duplicate_column_check=False,
    )
    captured = capsys.readouterr().out
    # At least 1 exact duplicate row exists
    assert "Total duplicate rows: 1" in captured


def test_duplicate_columns_are_counted(capsys, base_df):
    # base_df has f2 and f2_dup which are identical
    run_all_checks(
        data=base_df,
        problem_type="binary_classification",
        target_feature="target_clf",
        print_report=False,
        duplicate_row_check=False,
        duplicate_column_check=True,
    )
    captured = capsys.readouterr().out
    assert "Duplicate columns: 1" in captured


def test_no_duplicate_rows_reported(capsys, no_dup_df):
    run_all_checks(
        data=no_dup_df,
        problem_type="binary_classification",
        target_feature="target",
        print_report=False,
        duplicate_row_check=True,
        duplicate_column_check=False,
    )
    captured = capsys.readouterr().out
    assert "Total duplicate rows: 0" in captured


def test_no_duplicate_columns_reported(capsys, no_dup_df):
    run_all_checks(
        data=no_dup_df,
        problem_type="binary_classification",
        target_feature="target",
        print_report=False,
        duplicate_row_check=False,
        duplicate_column_check=True,
    )
    captured = capsys.readouterr().out
    assert "Duplicate columns: 0" in captured


def test_duplicate_row_check_false_skips(capsys, base_df):
    run_all_checks(
        data=base_df,
        problem_type="binary_classification",
        target_feature="target_clf",
        print_report=False,
        duplicate_row_check=False,
        duplicate_column_check=True,
    )
    captured = capsys.readouterr().out
    assert "Duplicate Report" not in captured


def test_duplicate_column_check_false_skips(capsys, base_df):
    run_all_checks(
        data=base_df,
        problem_type="binary_classification",
        target_feature="target_clf",
        print_report=False,
        duplicate_row_check=True,
        duplicate_column_check=False,
    )
    captured = capsys.readouterr().out
    assert "Duplicate columns" not in captured


# --- Completion signal ---
def test_run_all_checks_print_report_false_still_completes(base_df, capsys):
    run_all_checks(
        data=base_df,
        problem_type="regression",
        target_feature="target_reg",
        print_report=False,
    )
    captured = capsys.readouterr().out
    assert "Data quality checks completed." in captured


# --- NaN handling ---
def test_nan_values_in_features():
    df = pd.DataFrame(
        {
            "f1": [1.0, float("nan"), 3.0, 4.0],
            "f2": [10, 20, 30, 40],
            "target": pd.Categorical([0, 1, 0, 1]),
        }
    )
    _, summary, _, _, _ = run_all_checks(
        data=df,
        problem_type="binary_classification",
        target_feature="target",
        print_report=False,
        duplicate_row_check=False,
        duplicate_column_check=False,
    )
    assert summary.loc[summary["index"] == "f1", "n_missing"].iloc[0] == 1


# --- Categorical columns ---
def test_with_categorical_column():
    df = pd.DataFrame(
        {
            "f1": [1.0, 2.0, 3.0, 4.0],
            "cat_col": pd.Categorical(["a", "b", "a", "b"]),
            "target": pd.Categorical([0, 1, 0, 1]),
        }
    )
    _, _, _, cat_stats, _ = run_all_checks(
        data=df,
        problem_type="binary_classification",
        target_feature="target",
        print_report=False,
        duplicate_row_check=False,
        duplicate_column_check=False,
    )
    assert isinstance(cat_stats, pd.DataFrame)


def test_all_numeric_produces_no_cat_stats():
    df = pd.DataFrame(
        {
            "f1": [1.0, 2.0, 3.0, 4.0],
            "f2": [10, 20, 30, 40],
            "target": [0.5, 1.5, 2.5, 3.5],
        }
    )
    _, _, _, cat_stats, _ = run_all_checks(
        data=df,
        problem_type="regression",
        target_feature="target",
        print_report=False,
        duplicate_row_check=False,
        duplicate_column_check=False,
    )
    assert isinstance(cat_stats, str)


# --- Classification target validation ---


def test_classification_rejects_non_categorical_int_target():
    df = pd.DataFrame({"f1": [1, 2, 3, 4], "target": [0, 1, 0, 1]})
    with pytest.raises(TypeError, match="Expected category dtype"):
        run_all_checks(
            data=df,
            target_feature="target",
            problem_type="binary_classification",
            print_report=False,
            duplicate_row_check=False,
            duplicate_column_check=False,
        )


def test_classification_rejects_float_target():
    df = pd.DataFrame({"f1": [1, 2, 3, 4], "target": [0.0, 1.0, 0.0, 1.0]})
    with pytest.raises(TypeError, match="Expected category dtype"):
        run_all_checks(
            data=df,
            target_feature="target",
            problem_type="binary_classification",
            print_report=False,
            duplicate_row_check=False,
            duplicate_column_check=False,
        )


def test_classification_rejects_bool_target():
    df = pd.DataFrame({"f1": [1, 2, 3, 4], "target": [True, False, True, False]})
    with pytest.raises(TypeError, match="Expected category dtype"):
        run_all_checks(
            data=df,
            target_feature="target",
            problem_type="binary_classification",
            print_report=False,
            duplicate_row_check=False,
            duplicate_column_check=False,
        )


def test_binary_classification_rejects_wrong_class_count():
    df = pd.DataFrame({"f1": [1, 2, 3, 4, 5, 6], "target": pd.Categorical([0, 1, 2, 0, 1, 2])})
    with pytest.raises(ValueError, match="binary_classification.*3 unique classes"):
        run_all_checks(
            data=df,
            target_feature="target",
            problem_type="binary_classification",
            print_report=False,
            duplicate_row_check=False,
            duplicate_column_check=False,
        )


def test_multiclass_classification_rejects_too_few_classes():
    df = pd.DataFrame({"f1": [1, 2, 3, 4], "target": pd.Categorical([0, 1, 0, 1])})
    with pytest.raises(ValueError, match="multiclass_classification.*2 unique classes"):
        run_all_checks(
            data=df,
            target_feature="target",
            problem_type="multiclass_classification",
            print_report=False,
            duplicate_row_check=False,
            duplicate_column_check=False,
        )


def test_binary_classification_accepts_two_classes():
    df = pd.DataFrame({"f1": [1, 2, 3, 4], "target": pd.Categorical([0, 1, 0, 1])})
    out = run_all_checks(
        data=df,
        target_feature="target",
        problem_type="binary_classification",
        print_report=False,
        duplicate_row_check=False,
        duplicate_column_check=False,
    )
    assert len(out) == 5


def test_multiclass_classification_accepts_three_or_more_classes():
    df = pd.DataFrame({"f1": [1, 2, 3, 4, 5, 6], "target": pd.Categorical([0, 1, 2, 0, 1, 2])})
    out = run_all_checks(
        data=df,
        target_feature="target",
        problem_type="multiclass_classification",
        print_report=False,
        duplicate_row_check=False,
        duplicate_column_check=False,
    )
    assert len(out) == 5


def test_regression_skips_classification_checks():
    """Regression with float target should not trigger classification checks."""
    df = pd.DataFrame({"f1": [1, 2, 3, 4], "target": [0.5, 1.5, 2.5, 3.5]})
    out = run_all_checks(
        data=df,
        target_feature="target",
        problem_type="regression",
        print_report=False,
        duplicate_row_check=False,
        duplicate_column_check=False,
    )
    assert len(out) == 5


# --- Backward compatibility (classification= without problem_type) ---


def test_backward_compat_classification_true_without_problem_type():
    """Using classification=True without problem_type skips dtype/class-count checks."""
    df = pd.DataFrame({"f1": [1, 2, 3, 4], "target": [0, 1, 0, 1]})
    out = run_all_checks(
        data=df,
        classification=True,
        target_feature="target",
        print_report=False,
        duplicate_row_check=False,
        duplicate_column_check=False,
    )
    assert len(out) == 5


def test_backward_compat_classification_false_without_problem_type():
    """Using classification=False without problem_type runs the regression path."""
    df = pd.DataFrame({"f1": [1, 2, 3, 4], "target": [0.5, 1.5, 2.5, 3.5]})
    out = run_all_checks(
        data=df,
        classification=False,
        target_feature="target",
        print_report=False,
        duplicate_row_check=False,
        duplicate_column_check=False,
    )
    assert len(out) == 5
    _, _, _, _, target_df = out
    assert "skew_y" in target_df.columns


def test_problem_type_overrides_classification_flag():
    """problem_type takes precedence over an explicit classification flag."""
    df = pd.DataFrame({"f1": [1, 2, 3, 4], "target": [0.5, 1.5, 2.5, 3.5]})
    # classification=True but problem_type=regression → runs regression path
    out = run_all_checks(
        data=df,
        classification=True,
        target_feature="target",
        problem_type="regression",
        print_report=False,
        duplicate_row_check=False,
        duplicate_column_check=False,
    )
    _, _, _, _, target_df = out
    assert "skew_y" in target_df.columns
