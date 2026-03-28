from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
from data_foundry.curation_recommendations import (
    _get_grouped_splits_via_groupkfold,
    _get_grouped_splits_via_index_split,
    get_recommended_grouped_splits,
    get_recommended_iid_splits,
    get_recommended_splits_dimensions,
    subsample_temporal,
)
from data_foundry.schema import PredictiveMLSplitsMetadata


class DummySized:
    def __init__(self, n):
        self._n = n

    def __len__(self):
        return self._n


@pytest.fixture
def make_dataset():
    def _make(n, classification=False, n_classes=2, seed=0):
        rng = np.random.RandomState(seed)
        df = pd.DataFrame({"feat": rng.randn(n)})
        if classification:
            labels = np.tile(np.arange(n_classes), int(np.ceil(n / n_classes)))[:n]
            rng.shuffle(labels)
            df["target"] = labels
        else:
            df["target"] = rng.randn(n)
        return df.reset_index(drop=True)

    return _make


@pytest.fixture
def grouped_dataset_per_group(make_dataset):
    n_groups, group_size = 12, 5
    n = n_groups * group_size
    df = make_dataset(n=n, classification=True, n_classes=3, seed=7)
    df["group"] = np.repeat(np.arange(n_groups), group_size)
    group_labels = (df["group"] % 3).astype(int)
    df["strat_group"] = group_labels
    return df


@pytest.fixture
def grouped_dataset_per_sample(make_dataset):
    n_groups, group_size = 10, 6
    n = n_groups * group_size
    df = make_dataset(n=n, classification=True, n_classes=3, seed=11)
    df["group"] = np.repeat(np.arange(n_groups), group_size)
    return df


def _validate_pair(n, train_idx, test_idx):
    assert isinstance(train_idx, list)
    assert isinstance(test_idx, list)
    s_train, s_test = set(train_idx), set(test_idx)
    assert s_train.isdisjoint(s_test)
    assert s_train.union(s_test) == set(range(n))


# --- Split dimension recommendations ---
@pytest.mark.parametrize(
    ("n_samples", "expected"),
    [
        (100, (20, 3, None)),
        (500, (20, 3, None)),
        (2499, (10, 3, None)),
        (2500, (10, 3, None)),
        (249_999, (3, 3, None)),
        (250_000, (3, 3, None)),
        (999_999, (1, 3, None)),
        (1_000_000, (1, 3, None)),
        (1_250_000, (1, 1, 250_000)),
    ],
)
def test_get_recommended_splits_dimensions_boundaries(n_samples, expected):
    got = get_recommended_splits_dimensions(dataset=DummySized(n_samples))
    assert got == expected


def test_get_recommended_splits_dimensions_time_on_raises(make_dataset):
    df = make_dataset(100)
    with pytest.raises(ValueError, match="time-based"):
        get_recommended_splits_dimensions(dataset=df, time_on="ts")


def test_get_recommended_splits_dimensions_group_per_group_uses_n_groups(grouped_dataset_per_group):
    got = get_recommended_splits_dimensions(
        dataset=grouped_dataset_per_group,
        group_on="group",
        group_labels="per_group",
    )
    assert got == (20, 3, None)


# --- IID splits ---
def test_iid_non_range_index_raises(make_dataset):
    df = make_dataset(10)
    df.index = pd.RangeIndex(start=1, stop=11)
    with pytest.raises(ValueError, match="RangeIndex"):
        get_recommended_iid_splits(dataset=df, n_repeats=1, n_splits=1, test_size=2, stratify_on=None)


def test_iid_single_train_test_and_metadata(make_dataset):
    df = make_dataset(100)
    splits = get_recommended_iid_splits(dataset=df, n_repeats=1, n_splits=1, test_size=20, stratify_on=None)
    train_idx, test_idx = splits[0][0]
    _validate_pair(len(df), train_idx, test_idx)
    sm = PredictiveMLSplitsMetadata(splits_comment="test", splits=splits)
    assert sm.splits == splits


def test_iid_kfold_structure(make_dataset):
    df = make_dataset(90)
    n_repeats, n_splits = 3, 3
    splits = get_recommended_iid_splits(
        dataset=df,
        n_repeats=n_repeats,
        n_splits=n_splits,
        test_size=None,
        stratify_on=None,
    )
    assert len(splits) == n_repeats
    for repeat_folds in splits.values():
        assert len(repeat_folds) == n_splits
        for train_idx, test_idx in repeat_folds.values():
            _validate_pair(len(df), train_idx, test_idx)


def test_iid_kfold_all_test_folds_cover_full_dataset(make_dataset):
    df = make_dataset(90)
    splits = get_recommended_iid_splits(
        dataset=df,
        n_repeats=1,
        n_splits=3,
        test_size=None,
        stratify_on=None,
    )
    all_test_indices = set()
    for train_idx, test_idx in splits[0].values():
        all_test_indices.update(test_idx)
    assert all_test_indices == set(range(len(df)))


def test_iid_splits_are_deterministic(make_dataset):
    df = make_dataset(60)
    kwargs = dict(dataset=df, n_repeats=2, n_splits=3, test_size=None, stratify_on=None)
    splits1 = get_recommended_iid_splits(**kwargs)
    splits2 = get_recommended_iid_splits(**kwargs)
    for repeat_i in splits1:
        for fold_i in splits1[repeat_i]:
            assert splits1[repeat_i][fold_i][0] == splits2[repeat_i][fold_i][0]
            assert splits1[repeat_i][fold_i][1] == splits2[repeat_i][fold_i][1]


def test_iid_stratified_splits_structure(make_dataset):
    df = make_dataset(60, classification=True, n_classes=2)
    splits = get_recommended_iid_splits(
        dataset=df,
        n_repeats=2,
        n_splits=3,
        test_size=None,
        stratify_on="target",
    )
    assert len(splits) == 2
    for repeat_folds in splits.values():
        assert len(repeat_folds) == 3
        for train_idx, test_idx in repeat_folds.values():
            _validate_pair(len(df), train_idx, test_idx)


# --- Grouped splits ---
@pytest.mark.parametrize("stratify_on", [None, "target"])
def test_grouped_repeated_structure_and_group_isolation(grouped_dataset_per_sample, stratify_on):
    df = grouped_dataset_per_sample
    splits = get_recommended_grouped_splits(
        dataset=df,
        n_repeats=2,
        n_splits=3,
        group_on="group",
        group_labels="per_sample",
        test_size=None,
        stratify_on=stratify_on,
    )

    assert len(splits) == 2
    for repeat_folds in splits.values():
        assert len(repeat_folds) == 3
        for train_idx, test_idx in repeat_folds.values():
            _validate_pair(len(df), train_idx, test_idx)
            train_groups = set(df.loc[train_idx, "group"].unique())
            test_groups = set(df.loc[test_idx, "group"].unique())
            assert train_groups.isdisjoint(test_groups)


@pytest.mark.parametrize("group_labels", ["per_group", "per_sample"])
def test_grouped_single_split_requires_positive_test_size(grouped_dataset_per_group, group_labels):
    with pytest.raises(ValueError, match="test_size"):
        get_recommended_grouped_splits(
            dataset=grouped_dataset_per_group,
            n_repeats=1,
            n_splits=1,
            group_on="group",
            group_labels=group_labels,
            test_size=0,
            stratify_on=None,
        )


def test_grouped_per_group_stratify_consistency_raises(grouped_dataset_per_group):
    df = grouped_dataset_per_group.copy()
    first_group = df["group"].iloc[0]
    idxs = df.index[df["group"] == first_group].tolist()
    df.loc[idxs[0], "strat_group"] = 99

    with pytest.raises(ValueError, match="single unique value"):
        get_recommended_grouped_splits(
            dataset=df,
            n_repeats=1,
            n_splits=3,
            group_on="group",
            group_labels="per_group",
            test_size=None,
            stratify_on="strat_group",
        )


def test_grouped_non_range_index_raises(grouped_dataset_per_group):
    df = grouped_dataset_per_group.copy()
    df.index = pd.RangeIndex(start=1, stop=len(df) + 1)
    with pytest.raises(ValueError, match="RangeIndex"):
        get_recommended_grouped_splits(
            dataset=df,
            n_repeats=1,
            n_splits=3,
            group_on="group",
            group_labels="per_group",
            test_size=None,
            stratify_on=None,
        )


def test_per_group_splits_group_isolation(grouped_dataset_per_group):
    df = grouped_dataset_per_group
    splits = get_recommended_grouped_splits(
        dataset=df,
        n_repeats=2,
        n_splits=3,
        group_on="group",
        group_labels="per_group",
        test_size=None,
        stratify_on=None,
    )
    assert len(splits) == 2
    for repeat_folds in splits.values():
        assert len(repeat_folds) == 3
        for train_idx, test_idx in repeat_folds.values():
            train_groups = set(df.loc[train_idx, "group"].unique())
            test_groups = set(df.loc[test_idx, "group"].unique())
            assert train_groups.isdisjoint(test_groups)
            # Together they span all groups
            assert train_groups | test_groups == set(df["group"].unique())


def test_per_group_single_split_with_test_size(grouped_dataset_per_group):
    df = grouped_dataset_per_group
    splits = get_recommended_grouped_splits(
        dataset=df,
        n_repeats=1,
        n_splits=1,
        group_on="group",
        group_labels="per_group",
        test_size=15,
        stratify_on=None,
    )
    assert 0 in splits
    assert 0 in splits[0]
    train_idx, test_idx = splits[0][0]
    train_groups = set(df.loc[train_idx, "group"].unique())
    test_groups = set(df.loc[test_idx, "group"].unique())
    assert train_groups.isdisjoint(test_groups)


# --- Internal helpers ---


def test_internal_index_split_helper(grouped_dataset_per_group):
    df = grouped_dataset_per_group
    splits = _get_grouped_splits_via_index_split(
        dataset=df,
        n_repeats=1,
        n_splits=3,
        group_on="group",
        test_size=None,
        stratify_on="strat_group",
    )
    assert 0 in splits and len(splits[0]) == 3


def test_internal_groupkfold_helper_single_split(grouped_dataset_per_sample):
    df = grouped_dataset_per_sample
    splits = _get_grouped_splits_via_groupkfold(
        dataset=df,
        n_repeats=1,
        n_splits=1,
        group_on="group",
        test_size=10,
        stratify_on="target",
    )
    train_idx, test_idx = splits[0][0]
    _validate_pair(len(df), train_idx, test_idx)


def test_internal_groupkfold_helper_multi_fold(grouped_dataset_per_sample):
    df = grouped_dataset_per_sample
    splits = _get_grouped_splits_via_groupkfold(
        dataset=df,
        n_repeats=2,
        n_splits=3,
        group_on="group",
        test_size=None,
        stratify_on=None,
    )
    assert len(splits) == 2
    for repeat_folds in splits.values():
        assert len(repeat_folds) == 3


# --- Subsample temporal ---
def test_subsample_temporal_reindexes_and_caps(make_dataset):
    n = 200
    df = make_dataset(n=n, classification=True, n_classes=2, seed=3)
    train_idx = list(range(160))
    test_idx = list(range(160, 200))

    df_reduced, new_train_idx, new_test_idx = subsample_temporal(
        df=df,
        train_idx=train_idx,
        test_idx=test_idx,
        train_cap=50,
        test_cap=20,
        seed=42,
        stratify_on="target",
    )

    assert len(df_reduced) == 70
    assert len(new_train_idx) == 50
    assert len(new_test_idx) == 20
    assert new_train_idx == list(range(50))
    assert new_test_idx == list(range(50, 70))


def test_subsample_temporal_no_change_when_under_caps(make_dataset):
    n = 100
    df = make_dataset(n=n, classification=True, n_classes=2, seed=5)
    train_idx = list(range(80))
    test_idx = list(range(80, 100))

    df_reduced, new_train_idx, new_test_idx = subsample_temporal(
        df=df,
        train_idx=train_idx,
        test_idx=test_idx,
        train_cap=1_000_000,
        test_cap=250_000,
        seed=42,
        stratify_on=None,
    )

    assert len(new_train_idx) == 80
    assert len(new_test_idx) == 20
    assert len(df_reduced) == 100
    assert new_train_idx == list(range(80))
    assert new_test_idx == list(range(80, 100))


def test_subsample_temporal_no_stratification(make_dataset):
    n = 200
    df = make_dataset(n=n, classification=False, seed=7)
    train_idx = list(range(160))
    test_idx = list(range(160, 200))

    df_reduced, new_train_idx, new_test_idx = subsample_temporal(
        df=df,
        train_idx=train_idx,
        test_idx=test_idx,
        train_cap=50,
        test_cap=20,
        seed=42,
        stratify_on=None,
    )

    assert len(new_train_idx) == 50
    assert len(new_test_idx) == 20
    assert set(new_train_idx).isdisjoint(set(new_test_idx))
