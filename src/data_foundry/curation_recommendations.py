from __future__ import annotations

import pandas as pd


def get_recommended_iid_splits_dimensions(
    dataset: pd.DataFrame,
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
    n_train_samples = int(len(dataset) * 2 / 3)
    if n_train_samples < 500:
        return 20, 3, None
    if n_train_samples < 2_500:
        return 10, 3, None
    if n_train_samples < 250_000:
        return 3, 3, None
    if n_train_samples < 1_000_000:
        return 1, 3, None

    return 1, 1, 250_000


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
        raise ValueError(
            "Dataset index must be a RangeIndex starting from 0 (do reset_index!)."
        )

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
        print("Using Stratified IID splits.")
        rkf = RepeatedStratifiedKFold(
            n_splits=n_splits, n_repeats=n_repeats, random_state=SPLIT_RANDOM_STATE
        )
    else:
        rkf = RepeatedKFold(
            n_splits=n_splits, n_repeats=n_repeats, random_state=SPLIT_RANDOM_STATE
        )
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
