"""Format-2 containers: dtype round trips, metadata a newer version wrote, failed saves and the helper columns."""

from __future__ import annotations

import dataclasses
import json
import logging

import numpy as np
import pandas as pd
import pandas.testing as pdt
import pytest
from data_foundry.curation_container import CuratedContainer, feature_columns, split_columns
from data_foundry.schema import Grouping, PredictiveMLSplitsMetadata, PredictiveMLTaskMetadataV2
from data_foundry.utils.checksum import encode_pydantic_metadata

from tests.test_bundle_checks import _unit_container, make_spec, make_v2_container


def _toy(df: pd.DataFrame, **task) -> CuratedContainer:
    """A format-2 container of ``df`` (a binary ``target`` column), split into two folds."""
    rows = np.arange(len(df))
    splits = {0: {f: (rows[rows % 2 != f].tolist(), rows[rows % 2 == f].tolist()) for f in range(2)}}
    return make_v2_container(df, splits=splits, **task)


def _target(n: int) -> pd.Categorical:
    return pd.Categorical(["yes", "no"] * (n // 2))


def test_format_2_dtypes_round_trip(tmp_path):
    n = 12
    df = pd.DataFrame(
        {
            "tz": pd.date_range("2020-03-29", periods=n, freq="h", tz="Europe/Berlin"),
            "naive": pd.date_range("2020-01-01", periods=n, freq="D"),
            "per": pd.period_range("2020-01", periods=n, freq="M"),
            "td": pd.to_timedelta(np.arange(n), unit="s"),
            "intcat": pd.Categorical([1, 2, np.nan, 3] * 3),
            "ord": pd.Categorical(["lo", "hi", "mid"] * 4, categories=["lo", "mid", "hi"], ordered=True),
            "i64": pd.array([1, None, 3] * 4, dtype="Int64"),
            "b": pd.array([True, None, False] * 4, dtype="boolean"),
            "s": pd.array(["a", None, "c"] * 4, dtype="string"),
            "target": _target(n),
        }
    )
    container = _toy(df)
    loaded = CuratedContainer.load(container.save(save_dir=tmp_path))
    assert loaded.verify()
    for col in df.columns:
        pdt.assert_series_equal(loaded.dataset[col], df[col], check_categorical=True)
        if isinstance(df[col].dtype, pd.CategoricalDtype):
            assert loaded.dataset[col].cat.ordered == df[col].cat.ordered
            assert str(loaded.dataset[col].cat.categories.dtype) == str(df[col].cat.categories.dtype)


def test_text_saved_under_infer_string_loads_with_its_missing_values(tmp_path):
    """Text in pandas 3's ``str`` dtype is saved as ``object``; nulls never come back as the text "None"."""
    with pd.option_context("future.infer_string", True):  # noqa: FBT003
        df = pd.DataFrame({"t": ["a", None, "c", None], "target": _target(4)})
        path = _toy(df).save(save_dir=tmp_path)
    assert json.loads((path / "dtypes.json").read_text())["t"] == "object"
    loaded = CuratedContainer.load(path)
    assert loaded.dataset["t"].isna().tolist() == [False, True, False, True]
    assert loaded.verify()


def test_a_str_entry_in_an_older_dtypes_file_is_not_cast(tmp_path):
    df = pd.DataFrame({"t": pd.Series(["a", None, "c", None], dtype=object), "target": _target(4)})
    path = _toy(df).save(save_dir=tmp_path)
    dtypes = json.loads((path / "dtypes.json").read_text())
    (path / "dtypes.json").write_text(json.dumps(dtypes | {"t": "str"}))  # as pandas 3 wrote it before the fix
    loaded = CuratedContainer.load(path)
    assert "None" not in loaded.dataset["t"].tolist()
    assert loaded.verify()


@pytest.mark.parametrize("tz", ["Europe/Berlin", None])
def test_a_datetime_categorical_is_refused(tz):
    times = pd.to_datetime(["2020-01-01", "2021-01-01"] * 2)
    df = pd.DataFrame({"when": pd.Categorical(times.tz_localize(tz) if tz else times), "target": _target(4)})
    with pytest.raises(ValueError, match=r"datetime categories.*Store each as a datetime column"):
        _toy(df)


def test_restoring_categories_never_adds_missing_values(tmp_path):
    df = pd.DataFrame({"c": pd.Categorical(["a", "b", "a", "b"]), "target": _target(4)})
    path = _toy(df).save(save_dir=tmp_path)
    details = json.loads((path / "categories.json").read_text())
    details["c"]["categories"] = ["x", "y"]  # categories that do not hold the stored values
    (path / "categories.json").write_text(json.dumps(details))
    with pytest.raises(ValueError, match="would turn values into missing values"):
        CuratedContainer.load(path)


# --- metadata a newer data_foundry wrote ---------------------------------------------------------------------------
def _edit(path, prefix: str, change) -> None:
    (file,) = path.glob(f"{prefix}.*.json")
    data = json.loads(file.read_text())
    change(data)
    file.write_text(json.dumps(data))


@pytest.mark.parametrize("prefix", ["task_metadata", "experiment_metadata"])
def test_an_unknown_task_or_split_field_is_refused(tmp_path, prefix):
    path = _toy(pd.DataFrame({"x": np.arange(4.0), "target": _target(4)})).save(save_dir=tmp_path)
    _edit(path, prefix, lambda d: d.update(added_later=1))
    with pytest.raises(ValueError, match=r"added_later.*newer data_foundry\. Upgrade"):
        CuratedContainer.load(path)


def test_an_unknown_format_1_task_or_split_field_is_refused(tmp_path):
    from tests.test_curation_container import _grouped_toy  # noqa: PLC0415

    for prefix in ("task_metadata", "experiment_metadata"):
        path = _grouped_toy().save(save_dir=tmp_path / prefix)
        _edit(path, prefix, lambda d: d.update(added_later=1))
        with pytest.raises(ValueError, match="newer data_foundry"):
            CuratedContainer.load(path)


def test_an_unknown_dataset_metadata_field_is_dropped_with_a_warning(tmp_path, caplog):
    container = _toy(pd.DataFrame({"x": np.arange(4.0), "target": _target(4)}))
    path = container.save(save_dir=tmp_path)
    _edit(path, "dataset_metadata", lambda d: d.update(added_later=1))
    with caplog.at_level(logging.WARNING):
        loaded = CuratedContainer.load(path)
    assert "ignoring fields this version does not know: ['added_later']" in caplog.text
    assert loaded.verify()


# --- save -----------------------------------------------------------------------------------------------------------
def test_a_failed_save_leaves_no_temporary_folder(tmp_path, monkeypatch):
    container = _toy(pd.DataFrame({"x": np.arange(4.0), "target": _target(4)}))

    def fail(*_args, **_kwargs):
        raise OSError("disk full")

    monkeypatch.setattr(CuratedContainer, "_save_categories", staticmethod(fail))
    with pytest.raises(OSError, match="disk full"):
        container.save(save_dir=tmp_path)
    assert list((tmp_path / "toy_ds").iterdir()) == []


def test_save_and_checksum_print_nothing(tmp_path, capsys):
    container = _toy(pd.DataFrame({"x": np.arange(4.0), "target": _target(4)}))
    CuratedContainer.load(container.save(save_dir=tmp_path)).verify()
    assert capsys.readouterr().out == ""


def test_a_format_2_container_refuses_a_version_comment():
    container = _toy(pd.DataFrame({"x": np.arange(4.0), "target": _target(4)}))
    with pytest.raises(ValueError, match="format-2 container keeps no version_comment"):
        dataclasses.replace(container, checksum=None, version_comment="sub-sampled")


def test_time_of_prediction_is_stored_unset_as_in_grouping():
    def task(**kwargs):
        return PredictiveMLTaskMetadataV2(
            target_column_name="y", problem_type="regression", objective_metric=make_spec(), time_on="t", **kwargs
        )

    assert task(time_of="prediction").time_of is None
    assert encode_pydantic_metadata(task(time_of="prediction")) == encode_pydantic_metadata(task())


# --- split_columns --------------------------------------------------------------------------------------------------
def test_split_columns_hold_the_unit_of_a_unit_weight():
    container = _unit_container()
    assert "plot" in split_columns(container)
    assert "plot" not in feature_columns(container)


def test_split_columns_hold_the_order_inside_a_group_and_its_prediction_point():
    n = 8
    df = pd.DataFrame(
        {
            "p": np.arange(n),
            "g": np.repeat([1, 2, 3, 4], 2),
            "t": np.arange(n) + 1,
            "x": np.arange(n, dtype=float),
            "target": _target(n),
        }
    )
    grouping = Grouping(on="g", labels="per_sample", time_on="t", time_of="label", prediction_time="p")
    rows = np.arange(n)
    splits = {0: {0: (rows[:4].tolist(), rows[4:].tolist()), 1: (rows[4:].tolist(), rows[:4].tolist())}}
    container = make_v2_container(df, grouping=grouping, splits=splits)
    assert split_columns(container) == ["p", "g", "t"]  # frame order, each once
    assert feature_columns(container) == ["p", "x"]


def test_a_format_1_container_has_no_grouping():
    from tests.test_curation_container import _grouped_toy  # noqa: PLC0415

    assert _grouped_toy().grouping is None


def test_split_columns_without_a_grouping_or_unit_are_unchanged():
    df = pd.DataFrame({"t": np.arange(4), "x": np.arange(4.0), "target": _target(4)})
    container = dataclasses.replace(
        _toy(df, time_on="t"),
        experiment_metadata=PredictiveMLSplitsMetadata(splits_comment="x", splits={0: {0: ([0, 1], [2, 3])}}),
        checksum=None,
    )
    assert split_columns(container) == ["t"]
