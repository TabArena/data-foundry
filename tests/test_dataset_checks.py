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
            "target_clf": [0, 1, 0, 1, 0, 0],
            "target_reg": [0.5, 1.5, 2.5, 3.5, 4.5, 0.5],
        }
    )


@pytest.mark.parametrize("classification,target_feature", [(True, "target_clf"), (False, "target_reg")])
def test_run_all_checks_returns_expected_types(base_df, classification, target_feature):
    out = run_all_checks(
        data=base_df,
        classification=classification,
        target_feature=target_feature,
        print_report=False,
        sample_threshold=10_000,
    )
    assert len(out) == 5
    df_head, summary, numeric_stats, cat_stats, target_df = out
    assert isinstance(df_head, pd.DataFrame)
    assert isinstance(summary, pd.DataFrame)
    assert isinstance(target_df, pd.DataFrame)
    assert isinstance(numeric_stats, pd.DataFrame) or isinstance(numeric_stats, str)
    assert isinstance(cat_stats, pd.DataFrame) or isinstance(cat_stats, str)


def test_run_all_checks_rejects_object_dtype():
    df = pd.DataFrame({"f1": [1, 2], "obj": ["a", "b"], "target": [0, 1]})
    with pytest.raises(TypeError, match="object dtype"):
        run_all_checks(data=df, classification=True, target_feature="target", print_report=False)


def test_run_all_checks_rejects_missing_target(base_df):
    with pytest.raises(ValueError, match="not in the DataFrame"):
        run_all_checks(data=base_df, classification=True, target_feature="missing", print_report=False)


def test_run_all_checks_sampling_branch_runs(base_df):
    df = pd.concat([base_df] * 200, ignore_index=True)
    out = run_all_checks(
        data=df,
        classification=True,
        target_feature="target_clf",
        print_report=False,
        sample_threshold=20,
        sample_frac=0.2,
        sample_random_state=123,
    )
    _, summary, _, _, target_df = out
    assert "examples" in summary.columns
    assert set(target_df.columns) == {"count", "pct"}


def test_run_all_checks_duplicate_checks_prints(capsys, base_df):
    run_all_checks(
        data=base_df,
        classification=True,
        target_feature="target_clf",
        print_report=False,
        duplicate_row_check=True,
        duplicate_column_check=True,
    )
    captured = capsys.readouterr().out
    assert "Duplicate Report" in captured
    assert "Duplicate columns" in captured


def test_run_all_checks_print_report_false_still_completes(base_df, capsys):
    run_all_checks(
        data=base_df,
        classification=False,
        target_feature="target_reg",
        print_report=False,
    )
    captured = capsys.readouterr().out
    assert "Data quality checks completed." in captured

