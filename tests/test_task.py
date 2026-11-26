"""The task view (`container.task()`): folds, inputs, weights, score and error on both formats."""

from __future__ import annotations

import json

import numpy as np
import pandas as pd
import pytest

from data_foundry.curation_container import CuratedContainer, feature_columns, split_columns
from data_foundry.examples import load_toy_container
from data_foundry.metrics import scorer
from data_foundry.sampling import subsample_train
from data_foundry.schema import Grouping, PredictiveMLSplitsMetadata, RowBudget, ScoringColumn, TrainSampling
from data_foundry.task import BENCHMARK_TASK_FILE, BenchmarkTask, Fold
from data_foundry.v1 import PredictiveMLTaskMetadata
from tests.test_bundle_checks import _spec, _unit_container, make_container, make_iid_frame, make_v2_container


def _positions(container: CuratedContainer) -> list[tuple[int, int, list[int], list[int]]]:
    return [
        (r, f, list(tr), list(te))
        for r, fs in container.experiment_metadata.splits.items()
        for f, (tr, te) in fs.items()
    ]


# --- the shipped toys ---------------------------------------------------------------------------------------------


def test_the_format_1_toy_gets_a_view_with_its_metric_name_as_a_spec():
    container = load_toy_container()
    task = container.task()
    assert isinstance(task, BenchmarkTask)
    assert task.format_version == 1
    assert task.name == "toy_iid_dataset"
    assert task.classes == ("neg", "pos")
    assert task.features == ("feat_num", "feat_int", "feat_cat")
    assert task.metric.name == "roc_auc"
    assert task.metric.prediction == "proba"
    assert task.greater_is_better
    assert task.optimum == 1.0
    assert task.grouping is None
    assert task.sample_weight is task.validation_weight is task.unit_column is task.row_budget is None
    folds = list(task.folds())
    assert [(f.repeat, f.fold, list(f.train), list(f.test)) for f in folds] == _positions(container)
    fold = folds[0]
    assert np.array_equal(fold.train, fold.train_side)
    assert task.train_weight(fold.train) is None
    proba = np.random.default_rng(0).random(len(fold.test))
    value = task.score(task.y(fold.test), proba, fold.test)
    assert value == pytest.approx(scorer(container, metric=task.metric)(task.y(fold.test), proba, fold.test))
    assert task.error(value) == pytest.approx(1.0 - value)
    json.dumps(task.to_dict())


def test_the_format_2_toy_keeps_the_group_and_the_weight_out_of_the_inputs():
    container = load_toy_container(format_version=2)
    assert container.format_version == 2
    assert container.verify()
    task = container.task()
    assert task.features == ("driver_age", "vehicle_size", "region")
    assert task.split_columns == ("customer",)
    assert task.sample_weight == task.validation_weight == "exposure"
    assert task.classes is None
    assert task.optimum == 0.0
    assert not task.greater_is_better
    assert task.grouping.on == "customer"
    assert container.dataset["vehicle_size"].cat.ordered
    for fold in task.folds():
        train_customers = set(container.dataset["customer"].iloc[fold.train])
        assert not train_customers & set(container.dataset["customer"].iloc[fold.test])
    weights = task.train_weight(fold.train)
    assert np.array_equal(weights, container.dataset["exposure"].iloc[fold.train].to_numpy())
    assert np.array_equal(task.validation_weights(fold.test), container.dataset["exposure"].iloc[fold.test])
    prediction = np.full(len(fold.test), float(task.y(fold.train).mean()))
    explicit = task.score(task.y(fold.test).to_numpy(), prediction, fold.test)
    # the weight is a metric input: without rows, the scorer reads them from the index of a pandas y_true
    assert task.score(task.y(fold.test), prediction) == pytest.approx(explicit)
    assert task.error(explicit) == pytest.approx(explicit)
    assert not set(task.X(fold.test).columns) & {"customer", "exposure", "claim_rate"}


def test_save_writes_the_task_view_next_to_the_metadata_outside_the_checksum(tmp_path):
    container = load_toy_container(format_version=2)
    shipped = json.loads((container.loaded_from_path / BENCHMARK_TASK_FILE).read_text())
    assert shipped == container.task().to_dict()
    folder = container.save(save_dir=tmp_path)
    assert json.loads((folder / BENCHMARK_TASK_FILE).read_text()) == shipped
    assert BENCHMARK_TASK_FILE not in CuratedContainer.load(folder).list_extra_files()
    (folder / BENCHMARK_TASK_FILE).unlink()  # derived: the container verifies without it
    assert CuratedContainer.load(folder).verify()
    # format 1 keeps the files its readers know
    assert not (load_toy_container().save(save_dir=tmp_path) / BENCHMARK_TASK_FILE).exists()


def test_load_toy_container_defaults_to_format_1_and_refuses_other_formats():
    assert load_toy_container().format_version == 1
    with pytest.raises(ValueError, match="format 1 and 2"):
        load_toy_container(format_version=3)


# --- in-memory format-2 containers -----------------------------------------------------------------------------


def _grouped_any() -> CuratedContainer:
    """Molecules of four conformations each: positive if any conformation is (one prediction per group)."""
    n = 60
    df = make_iid_frame(n).assign(molecule=np.repeat(np.arange(15), 4))
    positive = np.isin(df["molecule"], [0, 2, 3, 5, 8, 9, 12, 14])
    df["target"] = pd.Categorical(np.where(positive, "yes", "no"))
    grouping = Grouping(on="molecule", labels="per_group", prediction_unit="group", aggregation="any")
    fold = df["molecule"].to_numpy() % 3
    rows = np.arange(n)
    splits = {0: {f: (rows[fold != f].tolist(), rows[fold == f].tolist()) for f in range(3)}}
    return make_v2_container(df, spec=_spec("roc_auc"), grouping=grouping, splits=splits)


def test_a_task_scored_per_group_aggregates_the_rows_of_each_group():
    container = _grouped_any()
    task = container.task()
    assert task.grouping.prediction_unit == "group"
    assert "molecule" not in task.features
    assert task.split_columns == ("molecule",)
    fold = next(iter(task.folds()))
    proba = np.random.default_rng(1).random(len(fold.test))
    expected = scorer(container)(task.y(fold.test).to_numpy(), proba, fold.test)
    assert task.score(task.y(fold.test), proba, fold.test) == pytest.approx(expected)
    assert task.score(task.y(fold.test), proba) == pytest.approx(expected)  # rows from the index
    with pytest.raises(ValueError, match="row_index"):
        task.score(task.y(fold.test).to_numpy(), proba)


def test_a_training_weight_is_a_fit_weight_and_never_an_input():
    rng = np.random.default_rng(3)
    df = make_iid_frame().assign(target=rng.gamma(2.0, 1.0, 60), years=rng.uniform(0.1, 1.0, 60))
    weight = ScoringColumn(column="years", role="weight", used_by="rmse", description="years insured")
    container = make_v2_container(
        df,
        spec=_spec("rmse", inputs={"weight": "years"}),
        scoring_columns=[weight],
        sample_weight="years",
        problem_type="regression",
    )
    task = container.task()
    assert task.sample_weight == task.validation_weight == "years"
    assert "years" not in task.features
    fold = next(iter(task.folds()))
    assert np.array_equal(task.train_weight(fold.train), df["years"].iloc[fold.train].to_numpy())
    y = task.y(fold.test)
    prediction = np.full(len(y), 2.0)
    expected = np.sqrt(np.average((y - prediction) ** 2, weights=df["years"].iloc[fold.test]))
    assert task.score(y, prediction) == pytest.approx(expected)
    assert task.error(task.score(y, prediction)) == pytest.approx(expected)


def test_a_unit_weight_weights_validation_and_keeps_its_unit_for_the_split():
    task = _unit_container().task()
    assert task.unit_column == "plot"
    assert task.validation_weight == "plot_weight"
    assert task.sample_weight is None
    assert "plot" in task.split_columns
    assert not {"plot", "plot_weight"} & set(task.features)


def test_the_folds_fit_on_the_default_sample_within_the_row_budget():
    df = make_iid_frame(120)
    rows = np.arange(120)
    container = make_v2_container(df, splits={0: {0: (rows[:90].tolist(), rows[90:].tolist())}})
    container.experiment_metadata = PredictiveMLSplitsMetadata(
        splits_comment="toy",
        splits=container.experiment_metadata.splits,
        row_budget=RowBudget(train=40, test=60),
        train_sampling=TrainSampling(default="random", unit="rows"),
    )
    task = container.task()
    assert task.row_budget.train == 40
    (fold,) = task.folds()
    assert isinstance(fold, Fold)
    assert len(fold.train_side) == 90
    assert list(fold.train) == subsample_train(container, 0, 0)
    assert len(fold.train) == 40
    assert set(fold.train) <= set(fold.train_side)
    (whole,) = task.folds(budget=False)
    assert np.array_equal(whole.train, whole.train_side)
    assert task.to_dict()["row_budget"] == {"train": 40, "test": 60}


def test_a_label_time_is_a_split_column_and_no_input():
    n = 8
    rows = np.arange(n)
    frame = pd.DataFrame(
        {"sold": rows, "listed": rows - 1, "x": rows * 1.0, "target": pd.Categorical(["yes", "no"] * (n // 2))}
    )
    container = make_v2_container(
        frame,
        time_on="sold",
        time_of="label",
        prediction_time="listed",
        splits={0: {0: (rows[:4].tolist(), rows[4:].tolist())}},
    )
    task = container.task()
    assert task.features == tuple(feature_columns(container)) == ("listed", "x")
    assert task.split_columns == tuple(split_columns(container)) == ("sold",)
    assert task.to_dict()["features"] == ["listed", "x"]


def test_classes_are_sorted_whatever_the_declared_order():
    scale = ["low", "mid", "high"]
    df = make_iid_frame(60).assign(target=pd.Categorical(np.resize(scale, 60), scale, ordered=True))
    container = make_v2_container(df, problem_type="multiclass_classification")
    assert container.task().classes == ("high", "low", "mid")


def test_a_metric_without_a_fixed_optimum_has_no_error():
    df = make_iid_frame().assign(target=np.linspace(0.0, 5.0, 60))
    spec = _spec("net_revenue_at_cost", params={"cost": 0.68})
    task = make_v2_container(df, spec=spec, problem_type="regression").task()
    assert task.optimum is None
    value = task.score(task.y([0, 1, 2]), np.array([1.0, 0.0, 3.0]))
    assert np.isfinite(value)
    with pytest.raises(ValueError, match="no fixed optimum"):
        task.error(value)


def test_a_cost_matrix_optimum_is_its_smallest_cost():
    spec = _spec("cost_matrix", params={"labels": ["no", "yes"], "matrix": [[0.5, 1.0], [5.0, 2.0]]})
    task = make_v2_container(spec=spec).task()
    assert task.optimum == 0.5
    assert not task.greater_is_better
    assert task.error(1.5) == pytest.approx(1.0)


def test_a_format_1_group_column_is_a_row_unit_grouping():
    df = make_iid_frame().assign(g=np.repeat(np.arange(20), 3))
    task_metadata = PredictiveMLTaskMetadata(
        target_column_name="target",
        problem_type="binary_classification",
        objective_metric_name="roc_auc",
        group_on="g",
        group_labels="per_sample",
    )
    task = make_container(df, task_metadata=task_metadata).task()
    assert task.grouping == Grouping(on="g", labels="per_sample")
    assert task.grouping.prediction_unit == "row"
    assert "g" not in task.features
    assert task.split_columns == ("g",)


# --- the scorer without row positions ------------------------------------------------------------------------------


def test_the_scorer_refuses_an_index_that_is_not_the_containers():
    container = load_toy_container(format_version=2)
    score = scorer(container)
    y = container.dataset["claim_rate"].iloc[:20]
    prediction = np.full(20, 0.2)
    assert score(y, prediction) == pytest.approx(score(y.to_numpy(), prediction, np.arange(20)))
    with pytest.raises(ValueError, match="index"):
        score(y.set_axis([f"r{i}" for i in range(20)]), prediction)
    with pytest.raises(ValueError, match="outside"):
        score(y.set_axis(np.arange(20) + 10_000), prediction)
    with pytest.raises(ValueError, match="not the container's target"):
        score(y.set_axis(np.arange(20) + 100), prediction)
