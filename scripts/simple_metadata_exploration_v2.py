"""Very simple experimental script to extract some metadata from a local data warehouse."""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
from data_foundry.curation_container import CuratedContainer
from tqdm import tqdm

DATA_FOUNDRY_CACHE = Path("/home/lennart_priorlabs_ai/code/large_data_ensemble/data-foundry/local-data-warehouse")

# Resolve paths relative to the data-foundry root
SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent

sys.path.insert(0, str(ROOT_DIR / "datasets" / "beyond_iid"))
from _tmp_state_paths import GROUPED, NEW_IID, OLD_IID, TEMPORAL

ALL_DATASETS = OLD_IID + NEW_IID + TEMPORAL + GROUPED


def _is_period_col(s: pd.Series) -> bool:
    return isinstance(s.dtype, pd.PeriodDtype)


def _count_column_types(df: pd.DataFrame, excluded_columns: set[str]) -> dict[str, int]:
    """Count column types (excluding given columns).

    Returns counts for numerical, categorical, datetime, text, and binary columns, plus
    "non_binary" variants of each type that exclude columns with exactly two distinct
    non-null values. The "binary" count is cross-cutting (any dtype) and overlaps with
    the other type categories.
    """
    feature_df = df.drop(columns=[c for c in excluded_columns if c in df.columns])
    binary_cols = {c for c in feature_df.columns if feature_df[c].nunique(dropna=True) == 2}

    numerical_cols = feature_df.select_dtypes(include=["number"], exclude=["bool"]).columns
    categorical_cols = feature_df.select_dtypes(include=["category", "bool"]).columns
    datetime_cols = list(feature_df.select_dtypes(include=["datetime", "datetimetz"]).columns)
    datetime_cols += [c for c in feature_df.columns if _is_period_col(feature_df[c])]
    text_cols = feature_df.select_dtypes(include=["string"]).columns

    return {
        "numerical": len(numerical_cols),
        "categorical": len(categorical_cols),
        "datetime": len(datetime_cols),
        "text": len(text_cols),
        "binary": len(binary_cols),
        "numerical_non_binary": sum(c not in binary_cols for c in numerical_cols),
        "categorical_non_binary": sum(c not in binary_cols for c in categorical_cols),
        "datetime_non_binary": sum(c not in binary_cols for c in datetime_cols),
        "text_non_binary": sum(c not in binary_cols for c in text_cols),
    }


def _categorical_cardinality_stats(
    feature_df: pd.DataFrame,
) -> tuple[int | None, float | None, float | None, int]:
    """Return (max, mean, median, num_high_cardinality>50) across categorical feature columns."""
    cat_cols = feature_df.select_dtypes(include=["category"]).columns
    if len(cat_cols) == 0:
        return None, None, None, 0
    cardinalities = pd.Series([feature_df[c].nunique() for c in cat_cols])
    num_high = int((cardinalities > 50).sum())
    return int(cardinalities.max()), float(cardinalities.mean()), float(cardinalities.median()), num_high


def _text_char_stats(
    feature_df: pd.DataFrame,
) -> tuple[float | None, float | None, int | None, int | None]:
    """Return (mean, median, max, num_cells>100_chars) across all text feature cells."""
    text_cols = feature_df.select_dtypes(include=["string"]).columns
    if len(text_cols) == 0:
        return None, None, None, None
    lengths = pd.concat([feature_df[c].dropna().str.len() for c in text_cols], ignore_index=True)
    if len(lengths) == 0:
        return None, None, None, None
    num_high = int((lengths > 100).sum())
    return float(lengths.mean()), float(lengths.median()), int(lengths.max()), num_high


def dataset_paths_to_metadata(dataset_paths: list[Path], warehouse_root: Path) -> pd.DataFrame:

    columns = [
        "name",
        "domain",
        "dataset_year",
        "age",
        "source",
        "reference",
        "reference_key",
        "problem_type",
        "num_rows",
        "num_cols",
        "num_classes",
        "minority_class_pct",
        "num_numerical_cols",
        "num_categorical_cols",
        "num_datetime_cols",
        "num_text_cols",
        "num_binary_cols",
        "num_numerical_non_binary_cols",
        "num_categorical_non_binary_cols",
        "num_datetime_non_binary_cols",
        "num_text_non_binary_cols",
        "max_categorical_cardinality",
        "mean_categorical_cardinality",
        "median_categorical_cardinality",
        "num_high_cardinality_cats",
        "text_char_mean",
        "text_char_median",
        "text_char_max",
        "text_char_num_high",
        "num_repeats",
        "num_folds",
        "time_horizon",
        "time_horizon_unit",
        "task_type",
        "uri",
    ]
    current_year = datetime.now().year

    metadata = []
    for path in tqdm(dataset_paths, desc="Extracting metadata from datasets"):
        container = CuratedContainer.load(path)

        name = container.dataset_metadata.unique_name
        domain = container.dataset_metadata.domain_str
        source = container.dataset_metadata.dataset_source
        reference = container.dataset_metadata.academic_reference_bibtex
        reference_key = container.dataset_metadata.academic_reference_bibtex_key

        dataset_year = container.dataset_metadata.dataset_year
        try:
            age = current_year - int(dataset_year)
        except (ValueError, TypeError):
            age = None

        problem_type = container.task_metadata.problem_type
        target_column = container.task_metadata.target_column_name

        if container.task_metadata.time_on is not None:
            task_type = "temporal"
        elif container.task_metadata.group_on is not None:
            task_type = "grouped"
        else:
            task_type = "iid"

        excluded_columns = {target_column}
        if task_type == "grouped":
            group_on = container.task_metadata.group_on
            if isinstance(group_on, list):
                excluded_columns.update(group_on)
            else:
                excluded_columns.add(group_on)

        num_rows, total_cols = container.dataset.shape
        num_cols = total_cols - len(excluded_columns)

        if problem_type in ("binary_classification", "multiclass_classification"):
            class_counts = container.dataset[target_column].value_counts()
            num_classes = len(class_counts)
            minority_class_pct = 100.0 * class_counts.min() / class_counts.sum()
        else:
            num_classes = None
            minority_class_pct = None

        feature_df = container.dataset.drop(
            columns=[c for c in excluded_columns if c in container.dataset.columns]
        )
        col_type_counts = _count_column_types(container.dataset, excluded_columns)
        counted_total = col_type_counts["numerical"] + col_type_counts["categorical"] + col_type_counts["datetime"] + col_type_counts["text"]
        if counted_total != num_cols:
            counted_cols = set(
                feature_df.select_dtypes(
                    include=["number", "bool", "category", "datetime", "datetimetz", "string"]
                ).columns
            )
            counted_cols.update(c for c in feature_df.columns if _is_period_col(feature_df[c]))
            missing = [(c, str(feature_df[c].dtype)) for c in feature_df.columns if c not in counted_cols]
            raise AssertionError(
                f"Column count mismatch for {name}: counted {counted_total} but expected {num_cols}. "
                f"Uncounted columns: {missing}"
            )

        max_cat_card, mean_cat_card, median_cat_card, num_high_card_cats = _categorical_cardinality_stats(feature_df)
        text_char_mean, text_char_median, text_char_max, text_char_num_high = _text_char_stats(feature_df)

        splits = container.experiment_metadata.splits
        num_repeats = len(splits)
        fold_counts = {len(v) for v in splits.values()}
        assert len(fold_counts) == 1, f"Inconsistent fold counts across repeats for {name}: {fold_counts}"
        num_folds = fold_counts.pop()
        time_horizon = container.experiment_metadata.time_horizon
        time_horizon_unit = container.experiment_metadata.time_horizon_unit

        uri = str(path.relative_to(warehouse_root))

        metadata.append(
            [
                name,
                domain,
                dataset_year,
                age,
                source,
                reference,
                reference_key,
                problem_type,
                num_rows,
                num_cols,
                num_classes,
                minority_class_pct,
                col_type_counts["numerical"],
                col_type_counts["categorical"],
                col_type_counts["datetime"],
                col_type_counts["text"],
                col_type_counts["binary"],
                col_type_counts["numerical_non_binary"],
                col_type_counts["categorical_non_binary"],
                col_type_counts["datetime_non_binary"],
                col_type_counts["text_non_binary"],
                max_cat_card,
                mean_cat_card,
                median_cat_card,
                num_high_card_cats,
                text_char_mean,
                text_char_median,
                text_char_max,
                text_char_num_high,
                num_repeats,
                num_folds,
                time_horizon,
                time_horizon_unit,
                task_type,
                uri,
            ]
        )
        del container  # free memory

    return pd.DataFrame(metadata, columns=columns)


if __name__ == "__main__":
    dataset_paths = [DATA_FOUNDRY_CACHE / uri for uri in ALL_DATASETS]
    res = dataset_paths_to_metadata(dataset_paths, warehouse_root=DATA_FOUNDRY_CACHE)
    print(res)
    res.to_csv("warehouse_metadata.csv", index=False)
