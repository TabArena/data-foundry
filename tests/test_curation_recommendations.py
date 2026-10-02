from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
from data_foundry.curation_recommendations import (
    LEGACY_SINGLE_SPLIT_RANDOM_STATE,
    SPLIT_RANDOM_STATE,
    _get_grouped_splits_via_groupkfold,
    _get_grouped_splits_via_index_split,
    get_recommended_grouped_splits,
    get_recommended_iid_splits,
    get_recommended_splits_dimensions,
    subsample_split_to_budget,
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


def test_iid_single_split_uses_the_shared_default_seed(make_dataset):
    """The single train/test split is seeded like the k-fold splits (``SPLIT_RANDOM_STATE``)."""
    from sklearn.model_selection import train_test_split

    df = make_dataset(100)
    splits = get_recommended_iid_splits(dataset=df, n_repeats=1, n_splits=1, test_size=20, stratify_on=None)
    expected_train, expected_test = train_test_split(df.index, test_size=20, random_state=SPLIT_RANDOM_STATE)
    assert splits[0][0] == (expected_train.tolist(), expected_test.tolist())


def test_iid_single_split_legacy_seed_reproduces_the_old_split(make_dataset):
    """Passing the legacy seed rebuilds a single split made while the seed was hard-coded to 42."""
    from sklearn.model_selection import train_test_split

    df = make_dataset(100)
    splits = get_recommended_iid_splits(
        dataset=df,
        n_repeats=1,
        n_splits=1,
        test_size=20,
        stratify_on=None,
        random_state=LEGACY_SINGLE_SPLIT_RANDOM_STATE,
    )
    old_train, old_test = train_test_split(df.index, test_size=20, random_state=42)
    assert splits[0][0] == (old_train.tolist(), old_test.tolist())


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


def test_subsample_temporal_uses_iloc_positions_for_non_range_index():
    df = pd.DataFrame(
        {
            "feat": [10, 11, 12, 13],
            "target": pd.Categorical([0, 1, 0, 1]),
        },
        index=[100, 101, 102, 103],
    )

    df_reduced, new_train_idx, new_test_idx = subsample_temporal(
        df=df,
        train_idx=[0, 1],
        test_idx=[2, 3],
        train_cap=10,
        test_cap=10,
        seed=42,
        stratify_on=None,
    )

    assert df_reduced["feat"].tolist() == [10, 11, 12, 13]
    assert df_reduced.index.tolist() == [0, 1, 2, 3]
    assert new_train_idx == [0, 1]
    assert new_test_idx == [2, 3]


# --- random_state ---


def _flat(splits):
    return [(tuple(tr), tuple(te)) for folds in splits.values() for tr, te in folds.values()]


def test_split_random_state_is_the_default_seed():
    """The module-level seed keeps the value the splitters used before it was exposed."""
    assert SPLIT_RANDOM_STATE == 4267


def test_iid_default_seed_equals_explicit_split_random_state(make_dataset):
    """Omitting ``random_state`` yields the same IID folds as passing the module constant."""
    df = make_dataset(60, classification=True)
    kwargs = dict(dataset=df, n_repeats=2, n_splits=3, test_size=None, stratify_on="target")
    assert _flat(get_recommended_iid_splits(**kwargs)) == _flat(
        get_recommended_iid_splits(**kwargs, random_state=SPLIT_RANDOM_STATE)
    )


def test_iid_random_state_changes_the_folds(make_dataset):
    """A different ``random_state`` produces different IID folds."""
    df = make_dataset(60)
    kwargs = dict(dataset=df, n_repeats=1, n_splits=3, test_size=None, stratify_on=None)
    assert _flat(get_recommended_iid_splits(**kwargs)) != _flat(get_recommended_iid_splits(**kwargs, random_state=1))


@pytest.mark.parametrize("group_labels", ["per_group", "per_sample"])
def test_grouped_random_state_is_forwarded(grouped_dataset_per_group, grouped_dataset_per_sample, group_labels):
    """``random_state`` reaches both grouped splitting paths and defaults to the module constant."""
    df = grouped_dataset_per_group if group_labels == "per_group" else grouped_dataset_per_sample
    kwargs = dict(
        dataset=df,
        n_repeats=2,
        n_splits=3,
        group_on="group",
        group_labels=group_labels,
        test_size=None,
        stratify_on="strat_group" if group_labels == "per_group" else "target",
    )
    default = _flat(get_recommended_grouped_splits(**kwargs))
    assert default == _flat(get_recommended_grouped_splits(**kwargs, random_state=SPLIT_RANDOM_STATE))
    assert default != _flat(get_recommended_grouped_splits(**kwargs, random_state=SPLIT_RANDOM_STATE + 1))


# --- Row budget / sub-sampling --------------------------------------------------------
def test_large_per_group_dataset_gets_a_single_split(monkeypatch):
    """The row count decides first: a large dataset with few groups is not cross-validated."""
    from data_foundry import curation_recommendations as cr

    monkeypatch.setattr(cr, "SPLIT_TRAIN_ROW_BUDGET", 80)
    monkeypatch.setattr(cr, "SPLIT_TEST_ROW_BUDGET", 20)
    df = pd.DataFrame({"g": np.repeat(np.arange(10), 12), "y": 0})  # 120 rows, 10 groups
    assert cr.get_recommended_splits_dimensions(dataset=df, group_on="g", group_labels="per_group") == (1, 1, 20)


def _grouped_frame(n_groups=200, seed=0):
    rng = np.random.default_rng(seed)
    sizes = rng.integers(1, 20, size=n_groups)
    groups = np.repeat(np.arange(n_groups), sizes)
    labels = np.repeat(rng.choice(["a", "b"], size=n_groups, p=[0.8, 0.2]), sizes)
    return pd.DataFrame({"g": groups, "y": pd.Categorical(labels), "x": rng.normal(size=len(groups))})


def test_subsample_split_to_budget_keeps_groups_whole_and_fits_the_caps():
    df = _grouped_frame()
    test_groups = set(range(0, 200, 4))
    test_idx = [i for i, g in enumerate(df["g"]) if g in test_groups]
    train_idx = [i for i, g in enumerate(df["g"]) if g not in test_groups]
    reduced, train, test = subsample_split_to_budget(
        df=df, train_idx=train_idx, test_idx=test_idx, group_on="g", stratify_on="y", train_cap=500, test_cap=100
    )
    assert len(train) <= 500 and len(test) <= 100
    assert reduced.index.equals(pd.RangeIndex(len(reduced)))
    train_g, test_g = set(reduced.iloc[train]["g"]), set(reduced.iloc[test]["g"])
    assert train_g.isdisjoint(test_g) and test_g <= test_groups
    for g in train_g | test_g:  # every kept group is complete
        assert (reduced["g"] == g).sum() == (df["g"] == g).sum()


def test_subsample_split_to_budget_keeps_the_class_balance():
    df = _grouped_frame(n_groups=2000, seed=1)
    everything = list(range(len(df)))
    reduced, train, _ = subsample_split_to_budget(
        df=df, train_idx=everything, test_idx=[], group_on="g", stratify_on="y", train_cap=len(df) // 4
    )
    before = (df["y"] == "b").mean()
    after = (reduced.iloc[train]["y"] == "b").mean()
    assert abs(after - before) < 0.03


def test_subsample_split_to_budget_is_a_no_op_within_budget():
    df = _grouped_frame()
    train_idx, test_idx = list(range(50)), list(range(50, 60))
    reduced, train, test = subsample_split_to_budget(df=df, train_idx=train_idx, test_idx=test_idx, group_on="g")
    assert reduced.equals(df.iloc[train_idx + test_idx].reset_index(drop=True))
    assert (len(train), len(test)) == (50, 10)


# --- Seeds -----------------------------------------------------------------------------


def test_subsample_temporal_defaults_to_the_shared_seed():
    df = pd.DataFrame({"x": np.arange(100)})
    kwargs = dict(df=df, train_idx=list(range(80)), test_idx=list(range(80, 100)), train_cap=10, test_cap=5)
    assert subsample_temporal(**kwargs)[0].equals(subsample_temporal(**kwargs, seed=SPLIT_RANDOM_STATE)[0])
