from __future__ import annotations

from typing import TYPE_CHECKING, Literal

import numpy as np
import pandas as pd

if TYPE_CHECKING:
    from data_foundry.schema import GroupLabelTypes


#: The seed every IID and grouped split in this module is built with unless a caller passes
#: ``random_state``: repeated k-fold, grouped k-fold, and the single train/test split used for the largest
#: datasets. Exposed so downstream code that wants to reproduce or align with these splits (for example an
#: inner validation split seeded like the outer one) can refer to it by name instead of copying the number.
#: Curation notebooks pass it explicitly and record it in :attr:`PredictiveMLSplitsMetadata.split_random_state`.
SPLIT_RANDOM_STATE = 4267

#: The seed the single train/test split used before 2026-09-29, when it ignored ``random_state``. Pass it to
#: reproduce such a split, e.g. the BeyondArena splits of ``mercari_price_suggestion`` and ``amex_non_iid``.
LEGACY_SINGLE_SPLIT_RANDOM_STATE = 42

#: Row budget of every outer split: at most this many rows on the train side ...
SPLIT_TRAIN_ROW_BUDGET = 1_000_000
#: ... and at most this many on the test side. Enforced by ``bundle_checks``; :func:`subsample_temporal`
#: caps to it by default, and :func:`get_recommended_splits_dimensions` recommends a single split with this
#: test size for datasets with ``SPLIT_TRAIN_ROW_BUDGET + SPLIT_TEST_ROW_BUDGET`` samples or more.
SPLIT_TEST_ROW_BUDGET = 250_000


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
      * A dataset with 1_250_000 rows or more always gets the single split, also when N counts groups
        (``group_labels="per_group"``), because of the per-split row budget. Its ``<unique_name>_1m``
        notebook then caps the split with :func:`subsample_split_to_budget`.


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

    # The row budget comes first: a dataset this large gets a single split even when its groups are few
    # enough for cross-validation (per-group labels), since every fold would exceed the row budget. Such a
    # dataset is sub-sampled to the budget in its `<unique_name>_1m` notebook (see `subsample_split_to_budget`).
    if n_samples >= SPLIT_TRAIN_ROW_BUDGET + SPLIT_TEST_ROW_BUDGET:
        return 1, 1, SPLIT_TEST_ROW_BUDGET

    if (group_on is not None) and (group_labels == "per_group"):
        n_groups = dataset[group_on].nunique()
        print(f"Providing recommendations based on number of groups ({n_groups}).")
        n_samples = n_groups

    # Dataset provides enough samples for a single train-test split with a large test set,
    # so we recommend that.
    if n_samples >= SPLIT_TRAIN_ROW_BUDGET + SPLIT_TEST_ROW_BUDGET:
        return 1, 1, SPLIT_TEST_ROW_BUDGET

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
    random_state: int = SPLIT_RANDOM_STATE,
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
        random_state (int): Seed of the repeated (stratified) k-fold splitter and of the single
            train/test split. Defaults to :data:`SPLIT_RANDOM_STATE`. Before 2026-09-29 the single
            split ignored it and always used :data:`LEGACY_SINGLE_SPLIT_RANDOM_STATE`; pass that to
            reproduce such a split.

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

    # Single train-test split
    if n_repeats == 1 and n_splits == 1:
        train_indices, test_indices = train_test_split(
            X.index,
            test_size=test_size,
            stratify=y,
            random_state=random_state,
        )
        splits[0] = {0: (train_indices.tolist(), test_indices.tolist())}
        return splits

    # Repeated (Stratified) K-Fold Cross-Validation
    if stratify_on is not None:
        rkf = RepeatedStratifiedKFold(n_splits=n_splits, n_repeats=n_repeats, random_state=random_state)
    else:
        rkf = RepeatedKFold(n_splits=n_splits, n_repeats=n_repeats, random_state=random_state)
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
    random_state: int = SPLIT_RANDOM_STATE,
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
        random_state (int): Seed of the splitter (repeat ``i`` of the per-sample path uses
            ``random_state + i``). Defaults to :data:`SPLIT_RANDOM_STATE`.

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
            random_state=random_state,
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
            random_state=random_state,
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
    random_state: int = SPLIT_RANDOM_STATE,
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
        random_state=random_state,
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
    random_state: int = SPLIT_RANDOM_STATE,
) -> dict[int, dict[int, tuple[list[int], list[int]]]]:
    """Fallback for grouped splits."""
    from sklearn.model_selection import GroupKFold, StratifiedGroupKFold
    from sklearn.utils.multiclass import type_of_target

    X = dataset
    y = dataset[stratify_on] if stratify_on is not None else None
    group = dataset[group_on]
    splits: dict[int, dict[int, tuple[list[int], list[int]]]] = {}
    splitter_cls = StratifiedGroupKFold if stratify_on is not None else GroupKFold

    if stratify_on:
        target_type = type_of_target(y)
        if target_type not in ("binary", "multiclass"):
            raise ValueError(
                f"StratifiedGroupKFold only supports binary and multiclass targets, but got {target_type}!",
                "Solution: Cast your target to 'category' dtype with 2 or more unique values for stratification.",
            )

    if n_repeats == 1 and n_splits == 1:
        if test_size is None or test_size <= 0:
            raise ValueError("test_size must be a positive integer for single train-test split!")

        n_groups = group.nunique()
        avg_rows_per_group = group.value_counts().mean()
        group_test_size = test_size / avg_rows_per_group
        approximate_splits = round(n_groups / group_test_size)
        approximate_splits = int(max(2, min(n_groups, approximate_splits)))

        splitter_inst = splitter_cls(n_splits=approximate_splits, shuffle=True, random_state=random_state)
        train_index, test_index = next(splitter_inst.split(X=X, y=y, groups=group))
        return {0: {0: (train_index.tolist(), test_index.tolist())}}

    for repeat_i in range(n_repeats):
        splits[repeat_i] = {}
        splitter_inst = splitter_cls(
            n_splits=n_splits,
            random_state=random_state + repeat_i,
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
    train_cap: int = SPLIT_TRAIN_ROW_BUDGET,
    test_cap: int = SPLIT_TEST_ROW_BUDGET,
    seed: int = SPLIT_RANDOM_STATE,
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
        seed: Random seed for reproducible subsampling. Defaults to :data:`SPLIT_RANDOM_STATE` (it was 42
            before 2026-09-29; pass 42 to reproduce an older subsample).
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

    # The input indices are documented as iloc-based positions, so preserve
    # positional semantics even when the DataFrame has custom index labels.
    df_reduced = df.iloc[selected_idx].copy().reset_index(drop=True)

    n_train = len(train_idx)
    new_train_idx = np.arange(n_train)
    new_test_idx = np.arange(n_train, len(df_reduced))

    return df_reduced, new_train_idx.tolist(), new_test_idx.tolist()


def subsample_split_to_budget(
    *,
    df: pd.DataFrame,
    train_idx: list[int],
    test_idx: list[int],
    group_on: str | None = None,
    stratify_on: str | None = None,
    train_cap: int = SPLIT_TRAIN_ROW_BUDGET,
    test_cap: int = SPLIT_TEST_ROW_BUDGET,
    random_state: int = SPLIT_RANDOM_STATE,
) -> tuple[pd.DataFrame, list[int], list[int]]:
    """Sub-sample one train/test split to the row budget, reduce the frame to its rows, and re-index.

    This is the sub-sampling step of a ``<unique_name>_1m`` notebook for IID and grouped data (temporal
    data uses :func:`subsample_temporal`): build the single train/test split the recommendation gives for
    a dataset of 1.25M rows or more, then cap it here. Without ``group_on`` rows are sampled, like
    :func:`subsample_temporal`. With ``group_on`` whole groups are sampled, so no group is cut and none
    moves between train and test; each side then holds at most ``cap`` rows, filled greedily from a
    random group order. With ``stratify_on`` that order interleaves the groups of each stratum (a group's
    stratum is its most frequent value), so the kept groups keep roughly the class balance.

    Args:
        df: Source dataframe with a RangeIndex; ``train_idx``/``test_idx`` are positions in it.
        train_idx: Train positions.
        test_idx: Test positions.
        group_on: Column whose values must stay whole. None samples rows.
        stratify_on: Column to keep balanced while sampling.
        train_cap: Maximum rows on the train side.
        test_cap: Maximum rows on the test side.
        random_state: Seed of the sampling. Defaults to :data:`SPLIT_RANDOM_STATE`.

    Returns:
        The reduced frame (train rows first, then test rows, index reset), and the new train and test
        positions in it.
    """
    if group_on is None:
        return subsample_temporal(
            df=df,
            train_idx=train_idx,
            test_idx=test_idx,
            train_cap=train_cap,
            test_cap=test_cap,
            seed=random_state,
            stratify_on=stratify_on,
        )

    rng = np.random.default_rng(random_state)

    def keep_groups(positions: np.ndarray, cap: int) -> np.ndarray:
        if len(positions) <= cap:
            return positions
        side = df.iloc[positions]
        codes, uniques = pd.factorize(side[group_on].to_numpy())
        sizes = np.bincount(codes, minlength=len(uniques))
        order = rng.permutation(len(uniques))
        if stratify_on is not None:
            strata = side.groupby(codes, sort=True)[stratify_on].agg(lambda s: s.value_counts().index[0]).to_numpy()
            strata_codes = pd.factorize(strata[order])[0]
            # rank of each group inside its stratum, scaled to [0, 1): sorting on it interleaves the strata
            rank = np.zeros(len(order))
            for s in np.unique(strata_codes):
                members = np.flatnonzero(strata_codes == s)
                rank[members] = (np.arange(len(members)) + 0.5) / len(members)
            order = order[np.argsort(rank, kind="stable")]
        kept, total = np.zeros(len(uniques), dtype=bool), 0
        for g in order:
            if total + sizes[g] <= cap:
                kept[g] = True
                total += sizes[g]
            if total == cap:
                break
        return positions[kept[codes]]

    train_idx = keep_groups(np.asarray(train_idx), train_cap)
    test_idx = keep_groups(np.asarray(test_idx), test_cap)
    df_reduced = df.iloc[np.concatenate([train_idx, test_idx])].copy().reset_index(drop=True)
    n_train = len(train_idx)
    return df_reduced, list(range(n_train)), list(range(n_train, len(df_reduced)))


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


TemporalUnit = Literal["days", "weeks", "months", "years", "unique", "rows"]
"""How :func:`get_temporal_window_splits` measures a test window.

* ``"days"`` / ``"weeks"``: calendar days (windows end on day boundaries).
* ``"months"`` / ``"years"``: calendar months / years (windows end on month / year starts).
* ``"unique"``: distinct values of the time column (dates, years, or a numeric time index).
* ``"rows"``: rows in time order (for a time index that is only a row order).
"""

_CALENDAR_UNITS = ("days", "weeks", "months", "years")


def _calendar_offset(unit: str, n: int) -> pd.DateOffset:
    return pd.DateOffset(**{unit: n})


def _calendar_end(last: pd.Timestamp, unit: str) -> pd.Timestamp:
    """The exclusive end of the newest window: the unit boundary after ``last``."""
    day = last.normalize()
    if unit in ("days", "weeks"):
        return day + pd.Timedelta(days=1)
    if unit == "months":
        return day.replace(day=1) + pd.DateOffset(months=1)
    return day.replace(month=1, day=1) + pd.DateOffset(years=1)


def get_temporal_window_splits(  # noqa: C901, PLR0912 - one branch per unit and stop rule
    *,
    dataset: pd.DataFrame,
    time_on: str,
    window: int | None = 1,
    unit: TemporalUnit = "days",
    n_windows: int | None = None,
    step: int | None = None,
    gap: int = 0,
    cutoffs: list | tuple | None = None,
    min_train_fraction: float | None = None,
) -> dict[int, dict[int, tuple[list[int], list[int]]]]:
    """Expanding-window temporal splits: test windows walking back from the newest data, train = all earlier rows.

    This is the shared form of the temporal splits in the collection. Each test window covers ``window``
    units; the next window moves back by ``step`` units (default: ``window``, so windows are contiguous;
    ``step < window`` makes consecutive windows overlap). Train is every row strictly before the window
    start minus ``gap`` units (a planning gap between prediction time and the test period). Rows after a
    window are unused by that split. Split 0 is the newest window (``{window_i: {0: (train, test)}}``), the
    layout the bundle checks expect.

    Windows stop when ``n_windows`` are built, when a window or its train side would be empty, or when the
    train side falls below ``min_train_fraction`` of all rows.

    Args:
        dataset: The frame, sorted ascending by ``time_on`` with a RangeIndex (splits are positions).
        time_on: The time column: datetime for calendar units, any sortable type for ``"unique"``/``"rows"``.
        window: Test-window length in ``unit``. With ``cutoffs``, None means "from the cutoff to the end of the
            data". For ``"unique"``/``"rows"``, None derives the length from ``n_windows`` and
            ``min_train_fraction``: the newest ``1 - min_train_fraction`` of the values (rows) is cut into
            ``n_windows`` equal windows.
        unit: See :data:`TemporalUnit`.
        n_windows: How many windows to build (None: as many as the stop rules allow).
        step: How far each window moves back, in ``unit`` (default ``window``).
        gap: Units between the end of train and the start of the test window.
        cutoffs: Explicit test-window starts (for example ``["2016"]`` or ``[2023, 2024, 2025]``) instead of
            walking back from the newest data. They are ordered newest first; ``n_windows`` and ``step`` are
            ignored.
        min_train_fraction: Stop before a window whose train side has less than this share of the data: of the
            distinct time values for ``"unique"``, of the rows otherwise.

    Returns:
        The outer splits ``{window_i: {0: (train_positions, test_positions)}}``, newest window first.
    """
    df = dataset
    times = df[time_on]
    if not times.is_monotonic_increasing:
        raise ValueError(f"`{time_on}` must be sorted ascending (sort the frame before splitting).")
    if not isinstance(df.index, pd.RangeIndex) or df.index.start != 0:
        raise ValueError("The frame needs a fresh RangeIndex: splits are positions.")
    if unit not in (*_CALENDAR_UNITS, "unique", "rows"):
        raise ValueError(f"Unknown unit {unit!r}.")
    if unit in _CALENDAR_UNITS and not pd.api.types.is_datetime64_any_dtype(times):
        raise ValueError(f"Calendar unit {unit!r} needs a datetime `{time_on}`; use unit='unique' or 'rows'.")
    n_rows = len(df)
    positions = np.arange(n_rows)

    # Express every window as a half-open interval [start, end) on an ordered "axis": timestamps for
    # calendar units, positions in the sorted unique values for "unique", row positions for "rows".
    if unit == "unique":
        values = pd.Index(times.unique())
        axis = values.get_indexer(times)
        axis_max = len(values)
    elif unit == "rows":
        axis = positions
        axis_max = n_rows
    else:
        axis = times

    if window is None and cutoffs is None:
        if unit in _CALENDAR_UNITS or n_windows is None or min_train_fraction is None:
            raise ValueError("window=None needs unit 'unique'/'rows' with n_windows and min_train_fraction.")
        window = int(axis_max * (1 - min_train_fraction) / n_windows)
        if window < 1:
            raise ValueError("Too few time values for that many windows.")
    step = window if step is None else step

    intervals: list[tuple] = []
    if cutoffs is not None:
        for cutoff in sorted(cutoffs, reverse=True):
            if unit in _CALENDAR_UNITS:
                start = pd.Timestamp(str(cutoff))
                end = None if window is None else start + _calendar_offset(unit, window)
                train_end = start - _calendar_offset(unit, gap) if gap else start
            else:
                start = int(values.get_loc(cutoff)) if unit == "unique" else int(cutoff)
                end = None if window is None else start + window
                train_end = start - gap
            intervals.append((start, end, train_end))
    else:
        i = 0
        while n_windows is None or i < n_windows:
            if unit in _CALENDAR_UNITS:
                end = _calendar_end(times.iloc[-1], unit) - _calendar_offset(unit, step * i)
                start = end - _calendar_offset(unit, window)
                train_end = start - _calendar_offset(unit, gap) if gap else start
            else:
                end = axis_max - step * i
                start = end - window
                train_end = start - gap
                if start <= 0:
                    break
            intervals.append((start, end, train_end))
            i += 1
            if n_windows is None and i > 10_000:
                break

    splits: dict[int, dict[int, tuple[list[int], list[int]]]] = {}
    for start, end, train_end in intervals:
        test_mask = (axis >= start) & ((axis < end) if end is not None else True)
        train_mask = axis < train_end
        test_idx = positions[np.asarray(test_mask)].tolist()
        train_idx = positions[np.asarray(train_mask)].tolist()
        if not test_idx or not train_idx:
            if cutoffs is not None:
                raise ValueError(f"The window starting at {start} has an empty train or test side.")
            break
        if min_train_fraction is not None:
            # Share of the axis: distinct time values for "unique", rows otherwise.
            share = train_end / axis_max if unit == "unique" else len(train_idx) / n_rows
            if share < min_train_fraction - 1e-9:
                break
        splits[len(splits)] = {0: (train_idx, test_idx)}
    if not splits:
        raise ValueError("No temporal window could be built; check window, unit and the data's time range.")
    return splits
