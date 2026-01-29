from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
from data_foundry.curation_recommendations import (
    get_recommended_iid_splits,
    get_recommended_iid_splits_dimensions,
)
from data_foundry.schema import PredictiveMLSplitsMetadata


class DummySized:
    """Lightweight object with a given length for dimension-only tests."""

    def __init__(self, n):
        self._n = n

    def __len__(self):
        return self._n


@pytest.mark.parametrize(
    ("n_samples", "expected"),
    [
        (100, (20, 3, None)),  # < 500
        (500, (10, 3, None)),  # 500 <= n < 2500
        (2499, (10, 3, None)),
        (2500, (3, 3, None)),  # 2500 <= n < 250000
        (249_999, (3, 3, None)),
        (250_000, (1, 3, None)),  # 250000 <= n < 1_000_000
        (999_999, (1, 3, None)),
        (1_000_000, (1, 1, 250_000)),  # >= 1_000_000
    ],
)
def test_get_recommended_iid_splits_dimensions(n_samples, expected):
    # use DummySized to avoid allocating huge DataFrames
    obj = DummySized(n_samples)
    got = get_recommended_iid_splits_dimensions(obj)
    assert got == expected


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
        return df

    return _make


def _validate_iid_train_test_pair(n, train_idx, test_idx):
    # indices are lists of ints
    assert isinstance(train_idx, list)
    assert isinstance(test_idx, list)
    assert all(isinstance(i, int) for i in train_idx)
    assert all(isinstance(i, int) for i in test_idx)
    # disjoint and union covers whole dataset
    s_train, s_test = set(train_idx), set(test_idx)
    assert s_train.isdisjoint(s_test)
    assert s_train.union(s_test) == set(range(n))


def test_single_train_test_split_makeable_and_valid(make_dataset):
    df = make_dataset(100, classification=False)
    splits = get_recommended_iid_splits(
        dataset=df,
        n_repeats=1,
        n_splits=1,
        test_size=20,
        stratify_on=None,
    )
    # expected top-level repeat key 0 and fold key 0
    assert 0 in splits
    assert 0 in splits[0]
    train_idx, test_idx = splits[0][0]
    _validate_iid_train_test_pair(len(df), train_idx, test_idx)
    # ensure fits into PredictiveMLSplitsMetadata
    sm = PredictiveMLSplitsMetadata(splits_comment="test", splits=splits)
    assert sm.splits == splits


def test_repeated_cv_structure(make_dataset):
    n = 60
    df = make_dataset(n)
    n_repeats, n_splits = 2, 3
    splits = get_recommended_iid_splits(
        dataset=df,
        n_repeats=n_repeats,
        n_splits=n_splits,
        test_size=None,
        stratify_on=None,
    )
    # repeats present
    assert len(splits) == n_repeats
    for _rep_id, fold_dict in splits.items():
        # each repeat must contain exactly n_splits folds
        assert len(fold_dict) == n_splits
        # collect all test indices in this repeat
        all_test = []
        for _fold_id, (train_idx, test_idx) in fold_dict.items():
            _validate_iid_train_test_pair(n, train_idx, test_idx)
            all_test.extend(test_idx)
        # across folds within a repeat, test indices should partition the dataset
        assert set(all_test) == set(range(n))
        # ensure no overlap between test sets of different folds within repeat
        lists = [set(v[1]) for v in fold_dict.values()]
        total = sum(len(s) for s in lists)
        assert total == n  # partitioning -> total sizes sum to n


def test_stratify_runs_and_returns_valid_splits(make_dataset):
    n = 100
    n_classes = 4
    df = make_dataset(n, classification=True, n_classes=n_classes)
    splits = get_recommended_iid_splits(
        dataset=df,
        n_repeats=1,
        n_splits=5,
        test_size=None,
        stratify_on="target",
    )
    # sanity checks on structure
    assert 0 in splits
    assert 0 in splits[0]
    for _rep, fold_dict in splits.items():
        for _fold, (train_idx, test_idx) in fold_dict.items():
            _validate_iid_train_test_pair(n, train_idx, test_idx)
            # check that labels referenced by test_idx exist in dataset
            targets_in_test = set(df.loc[test_idx, "target"].unique())
            assert targets_in_test.issubset(set(range(n_classes)))
    # convertible to PredictiveMLSplitsMetadata
    sm = PredictiveMLSplitsMetadata(splits_comment="strat", splits=splits)
    assert sm.splits == splits


def test_non_range_index_raises(make_dataset):
    df = make_dataset(10)
    # change index so it's no longer RangeIndex(start=0, stop=len)
    df.index = pd.RangeIndex(start=1, stop=11)
    with pytest.raises(ValueError):
        get_recommended_iid_splits(
            dataset=df,
            n_repeats=1,
            n_splits=1,
            test_size=2,
            stratify_on=None,
        )
