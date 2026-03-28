from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import pandas as pd

if TYPE_CHECKING:
    from data_foundry.schema import GroupLabelTypes


def get_recommended_splits_dimensions(
    *,
    dataset: pd.DataFrame,
    group_on: str | None = None,
    time_on: str | None = None,
    group_labels: GroupLabelTypes | None = None,
) -> tuple[int, int, int | None]:
    """Returns the recommended number of repeats and folds for IID splits.

    N represents the amount of training data we have to a fit a model.
    As we use 3-fold splits, we set N to be len(dataset)*2/3.

    Split recommendations for random split:
      * N < 500: 20-3 (20-repeated 3-fold cross-validation)
      * 500 <= N < 2_500: 10-3
      * 2_500 <= N < 250_000: 3-3
      * 250_000 <= N < 1_000_000: 1-3
      * N >= 1_000_000: 1-1-test_size (single train-test split)
        * Note: test_size is set to 250_000 samples for large datasets.

    Returns:
        A tuple of (n_repeats, n_splits, n_test_size).
            * n_repeats: Number of repeats.
            * n_splits: Number of folds for cross-validation. If n_repeats is 1 and
                n_splits is 1, it indicates a single train-test split.
            * n_test_size: Size of the test set for single train-test split.
                None if cross-validation is recommended.
    """
    if time_on is not None:
        raise ValueError(
            "We cannot provide recommend split dimensions for time-based splits. "
            "Judge the appropriate time horizon manually!"
        )

    n_samples = len(dataset)

    if (group_on is not None) and (group_labels == "per_group"):
        n_groups = dataset[group_on].nunique()
        print(f"Providing recommendations based on number of groups ({n_groups}).")
        n_samples = n_groups

    # Dataset provides enough samples for a single train-test split with a large test set,
    # so we recommend that.
    if n_samples >= 1_250_000:
        return 1, 1, 250_000

    n_train_samples = int(n_samples * 2 / 3)
    if n_train_samples < 500:
        return 20, 3, None
    if n_train_samples < 2_500:
        return 10, 3, None
    if n_train_samples < 250_000:
        return 3, 3, None

    # if n_train_samples < 1_000_000:
    return 1, 3, None


def get_recommended_iid_splits(
    *,
    dataset: pd.DataFrame,
    n_repeats: int,
    n_splits: int,
    test_size: int | None,
    stratify_on: str | None,
):
    """Generates recommended IID splits for the dataset.

    Parameters:
        dataset (pd.DataFrame): The dataset to split.
        n_repeats (int): Number of repeats.
        n_splits (int): Number of splits/folds for cross-validation.
        test_size (int | None): Size of the test set for single train-test split.
            If None, cross-validation is performed.
        stratify_on (str | None): Column name to use for stratification. If None,
            no stratification is applied.

    Returns:
        dict[int, dict[int, tuple[list[int], list[int]]]]: A dictionary of
            train-test splits per repeat and fold.
    """
    from sklearn.model_selection import (
        RepeatedKFold,
        RepeatedStratifiedKFold,
        train_test_split,
    )

    # Sanity check that index is reset
    if not dataset.index.equals(pd.RangeIndex(start=0, stop=len(dataset))):
        raise ValueError("Dataset index must be a RangeIndex starting from 0 (do reset_index!).")

    if stratify_on is not None:
        print("Using Stratified IID splits.")

    X = dataset
    y = dataset[stratify_on] if stratify_on is not None else None

    splits = {}
    SPLIT_RANDOM_STATE = 4267

    # Single train-test split
    if n_repeats == 1 and n_splits == 1:
        train_indices, test_indices = train_test_split(
            X.index,
            test_size=test_size,
            stratify=y,
            random_state=42,
        )
        splits[0] = {0: (train_indices.tolist(), test_indices.tolist())}
        return splits

    # Repeated (Stratified) K-Fold Cross-Validation
    if stratify_on is not None:
        rkf = RepeatedStratifiedKFold(n_splits=n_splits, n_repeats=n_repeats, random_state=SPLIT_RANDOM_STATE)
    else:
        rkf = RepeatedKFold(n_splits=n_splits, n_repeats=n_repeats, random_state=SPLIT_RANDOM_STATE)
    sklearn_splits = rkf.split(
        X=X,
        y=y,
    )

    for split_i, (train_idx, test_idx) in enumerate(sklearn_splits):
        repeat_i = split_i // n_splits
        fold_i = split_i % n_splits
        if repeat_i not in splits:
            splits[repeat_i] = {}
        splits[repeat_i][fold_i] = (train_idx.tolist(), test_idx.tolist())

    return splits


def get_recommended_grouped_splits(
    *,
    dataset: pd.DataFrame,
    n_repeats: int,
    n_splits: int,
    group_on: str,
    group_labels: GroupLabelTypes,
    test_size: int | None,
    stratify_on: str | None,
    show_splits: bool = False,
    target_on: str | None = None,
):
    """Generates recommended grouped splits for the dataset.

    This logic has two pathways:
        1) If group_labels is "per_group", we assume that each group has a single unique value
            for the stratify column and create group splits on just the group IDs.
            This ignores the size of the groups when splitting.
        2) If group_labels is "per_sample", we use sklearn's GroupKFold or StratifiedGroupKFold,
            which takes into account the size of the groups when splitting, but does not guarantee
            perfect stratification at the sample level when stratify_on is not None.

    Parameters:
        dataset (pd.DataFrame): The dataset to split.
        n_repeats (int): Number of repeats.
        n_splits (int): Number of splits/folds for cross-validation.
        test_size (int | None): Size of the test set for single train-test split.
            If None, cross-validation is performed.
        stratify_on (str | None): Column name to use for stratification.
        group_on (str): Column name to use for grouping.
        group_labels: Specification of group label type
        show_splits: Whether to print out the distribution of target and group labels in
            the generated splits for sanity checking.
        target_on: only needed for show_splits to give an overview of the target distribution.

    Returns:
        dict[int, dict[int, tuple[list[int], list[int]]]]: A dictionary of
            train-test splits per repeat and fold.
    """
    # Sanity check that index is reset
    if not dataset.index.equals(pd.RangeIndex(start=0, stop=len(dataset))):
        raise ValueError("Dataset index must be a RangeIndex starting from 0 (do reset_index!).")

    if stratify_on is not None:
        print("Using Stratified Grouped splits.")

    if n_repeats == 1 and n_splits == 1 and (test_size is None or test_size <= 0):
        raise ValueError("test_size must be a positive integer for single train-test split!")

    if (group_labels == "per_group") and (stratify_on is not None):
        is_per_group = (dataset.groupby(group_on, observed=True)[stratify_on].nunique() == 1).all()
        if not is_per_group:
            raise ValueError(
                "group_labels is set to 'per_group', but not all groups have "
                "a single unique value for the stratify column!"
            )

    if group_labels == "per_sample":
        print("Using label-per-sample grouped splits.")
        splits = _get_grouped_splits_via_groupkfold(
            dataset=dataset,
            n_repeats=n_repeats,
            n_splits=n_splits,
            group_on=group_on,
            test_size=test_size,
            stratify_on=stratify_on,
        )
    else:
        print("Using label-per-group grouped splits.")
        splits = _get_grouped_splits_via_index_split(
            dataset=dataset,
            n_repeats=n_repeats,
            n_splits=n_splits,
            group_on=group_on,
            test_size=test_size,
            stratify_on=stratify_on,
        )
    if show_splits:
        _show_grouped_splits(
            df=dataset,
            splits=splits,
            group_on=group_on,
            target_on=target_on,
        )
    return splits


def _get_grouped_splits_via_index_split(
    *,
    dataset: pd.DataFrame,
    n_repeats: int,
    n_splits: int,
    group_on: str,
    test_size: int | None,
    stratify_on: str | None,
) -> dict[int, dict[int, tuple[list[int], list[int]]]]:
    """Create grouped splits by performing normal IID splits on the group indices.
    This logic ignores the impact of group sizes!
    """
    group_values: list[str | int] = []
    group_samples: list[list[int]] = []
    group_stratify: list[object] = []
    multi_label_group_found: bool = False

    for group_value, group_df in dataset.groupby(group_on, sort=False, observed=True):
        group_values.append(group_value)
        group_samples.append(group_df.index.tolist())
        if stratify_on is not None:
            unique_values = list(group_df[stratify_on].unique())
            group_stratify.append(unique_values[0])
            if len(unique_values) > 1:
                multi_label_group_found = True

    if multi_label_group_found:
        raise ValueError("Multi-label group found but: groper_labels='per_group'!")

    group_dataset = pd.DataFrame({group_on: group_values})
    if stratify_on is not None:
        group_dataset[stratify_on] = group_stratify
    group_dataset = group_dataset.reset_index(drop=True)

    if test_size is not None:
        # Adjust test_size such that it is approximately the right size when mapping
        # back from groups to samples, based on the average group size.
        avg_samples_per_group = np.mean([len(samples) for samples in group_samples])
        test_size = int(test_size // avg_samples_per_group)

    print(f"Creating index-based splits for {len(group_dataset)} groups")
    group_splits = get_recommended_iid_splits(
        dataset=group_dataset,
        n_repeats=n_repeats,
        n_splits=n_splits,
        test_size=test_size,
        stratify_on=stratify_on,
    )

    def map_group_indices(indices: list[int]) -> list[int]:
        mapped: list[int] = []
        for group_idx in indices:
            mapped.extend(group_samples[group_idx])
        return mapped

    mapped_splits: dict[int, dict[int, tuple[list[int], list[int]]]] = {}
    all_groups = set(dataset[group_on].unique())
    for repeat_i, folds in group_splits.items():
        mapped_splits[repeat_i] = {}
        for fold_i, (train_group_idxs, test_group_idxs) in folds.items():
            train_idxs = map_group_indices(train_group_idxs)
            test_idxs = map_group_indices(test_group_idxs)

            # sanity check that groups are not mixed between train and test
            train_groups = set(dataset.iloc[train_idxs][group_on].unique())
            test_groups = set(dataset.iloc[test_idxs][group_on].unique())
            # no group should appear in both train and test
            assert train_groups.isdisjoint(test_groups)
            # together they should match the full set of groups
            assert train_groups.union(test_groups) == all_groups

            mapped_splits[repeat_i][fold_i] = (
                train_idxs,
                test_idxs,
            )

    return mapped_splits


def _get_grouped_splits_via_groupkfold(
    *,
    dataset: pd.DataFrame,
    n_repeats: int,
    n_splits: int,
    group_on: str,
    test_size: int | None,
    stratify_on: str | None,
) -> dict[int, dict[int, tuple[list[int], list[int]]]]:
    """Fallback for grouped splits."""
    from sklearn.model_selection import GroupKFold, StratifiedGroupKFold

    X = dataset
    y = dataset[stratify_on] if stratify_on is not None else None
    group = dataset[group_on]
    splits: dict[int, dict[int, tuple[list[int], list[int]]]] = {}
    SPLIT_RANDOM_STATE = 4267
    splitter_cls = StratifiedGroupKFold if stratify_on is not None else GroupKFold

    if n_repeats == 1 and n_splits == 1:
        if test_size is None or test_size <= 0:
            raise ValueError("test_size must be a positive integer for single train-test split!")

        n_groups = group.nunique()
        avg_rows_per_group = group.value_counts().mean()
        group_test_size = test_size / avg_rows_per_group
        approximate_splits = round(n_groups / group_test_size)
        approximate_splits = int(max(2, min(n_groups, approximate_splits)))

        splitter_inst = splitter_cls(n_splits=approximate_splits, shuffle=True, random_state=SPLIT_RANDOM_STATE)
        train_index, test_index = next(splitter_inst.split(X=X, y=y, groups=group))
        return {0: {0: (train_index.tolist(), test_index.tolist())}}

    for repeat_i in range(n_repeats):
        splits[repeat_i] = {}
        splitter_inst = splitter_cls(
            n_splits=n_splits,
            random_state=SPLIT_RANDOM_STATE + repeat_i,
            shuffle=True,
        )
        sklearn_splits = splitter_inst.split(X=X, y=y, groups=group)

        for fold_idx, (train_index, test_index) in enumerate(sklearn_splits):
            splits[repeat_i][fold_idx] = (train_index.tolist(), test_index.tolist())

    return splits


def subsample_temporal(
    *,
    df: pd.DataFrame,
    train_idx: list[int],
    test_idx: list[int],
    train_cap: int = 1_000_000,
    test_cap: int = 250_000,
    seed: int = 42,
    stratify_on: str | None = None,
) -> tuple[pd.DataFrame, list[int], list[int]]:
    """Subsample existing train/test splits, reduce the dataframe to only those rows,
    reset the index, and return the new train/test indices.

    NOTE: we assume the input indices are iloc-based indices!

    Args:
        df: Source dataframe.
        train_idx: Existing train indices referring to rows in `df`.
        test_idx: Existing test indices referring to rows in `df`.
        train_cap: Maximum number of train samples to keep.
        test_cap: Maximum number of test samples to keep.
        seed: Random seed for reproducible subsampling.
        stratify_on: Optional column name to use for stratified subsampling.
            If None, no stratification is applied.

    Returns:
        df_reduced: Filtered dataframe with reset integer index.
        new_train_idx: New train indices in `df_reduced`.
        new_test_idx: New test indices in `df_reduced`.
    """
    from sklearn.model_selection import train_test_split

    train_idx = np.asarray(train_idx)
    test_idx = np.asarray(test_idx)
    stratify_data = df[stratify_on] if stratify_on is not None else None

    if len(train_idx) > train_cap:
        train_idx, _ = train_test_split(
            train_idx,
            train_size=train_cap,
            random_state=seed,
            stratify=stratify_data.iloc[train_idx] if stratify_data is not None else None,
        )

    if len(test_idx) > test_cap:
        test_idx, _ = train_test_split(
            test_idx,
            train_size=test_cap,
            random_state=seed,
            stratify=stratify_data.iloc[test_idx] if stratify_data is not None else None,
        )

    # Preserve train first, then test, so rebuilding indices is trivial and stable.
    selected_idx = np.concatenate([train_idx, test_idx])

    df_reduced = df.loc[selected_idx].copy().reset_index(drop=True)

    n_train = len(train_idx)
    new_train_idx = np.arange(n_train)
    new_test_idx = np.arange(n_train, len(df_reduced))

    return df_reduced, new_train_idx.tolist(), new_test_idx.tolist()


def _show_grouped_splits(
    *,
    df: pd.DataFrame,
    splits: dict[int, dict[int, tuple[list[int], list[int]]]],
    group_on: str,
    target_on: str | None = None,
):
    """Simple utility to show the distribution of groups and target labels in the generated splits."""
    for repeat_idx, fold_values in splits.items():
        for fold_idx, (train_index, test_index) in fold_values.items():
            train_data = df.iloc[train_index]
            test_data = df.iloc[test_index]

            if target_on is None:
                train_target_dist, test_target_dist = None, None
            elif df.iloc[test_index][target_on].dtype.name == "category":
                train_target_dist = df.iloc[train_index][target_on].value_counts(normalize=True).to_dict()
                test_target_dist = df.iloc[test_index][target_on].value_counts(normalize=True).to_dict()

                train_classes = list(np.unique(df.iloc[train_index][target_on]))
                test_classes = list(np.unique(df.iloc[test_index][target_on]))
                if train_classes != test_classes:
                    raise ValueError(
                        f"Warning: Train and test splits have different classes for target {target_on}!"
                        f"\n\tTrain classes: {train_classes}"
                        f"\n\tTest classes: {test_classes}"
                        f"\n\tMissing in train: {set(test_classes) - set(train_classes)}"
                        f"\n\tMissing in test: {set(train_classes) - set(test_classes)}"
                    )
            else:
                train_target_dist = df.iloc[train_index][target_on].mean()
                test_target_dist = df.iloc[test_index][target_on].mean()

            print(f"""Repeat {repeat_idx}, Fold {fold_idx}:
            Train N: {len(train_index)}, Test N: {len(test_index)}
            Target Distribution:
            \tTrain target distribution: {train_target_dist}
            \tTest target distribution: {test_target_dist}
            Group Distribution {group_on}:
            \tTrain: {len(train_data[group_on].unique())}
            \tTest: {len(test_data[group_on].unique())}
            """)
