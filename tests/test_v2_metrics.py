"""Tests for the metric registry and the scorers (``data_foundry.v2.metrics``)."""

from __future__ import annotations

import ast
import dataclasses
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import scipy.stats
from data_foundry import bundle_checks
from data_foundry.schema import MetricSpec, PredictiveMLTaskMetadataV2, ScoringColumn
from data_foundry.v2 import metrics as m
from data_foundry.v2.dataset import metric_spec
from data_foundry.v2.metrics import METRICS, Metric, score, scorer, to_sklearn_scorer
from pydantic import TypeAdapter
from sklearn import metrics as skm
from sklearn.linear_model import LinearRegression, LogisticRegression

N = 500
RNG = np.random.default_rng(0)
Y_BIN = RNG.choice(["no", "yes"], size=N)
P_BIN = RNG.uniform(size=N)
L_BIN = RNG.choice(["no", "yes"], size=N)
CLASSES = ["a", "b", "c", "d"]
Y_MULTI = RNG.choice(CLASSES, size=N)
P_MULTI = RNG.dirichlet(np.ones(len(CLASSES)), size=N)
L_MULTI = RNG.choice(CLASSES, size=N)
Y_REG = RNG.gamma(2.0, size=N)
P_REG = Y_REG + RNG.normal(scale=0.5, size=N).clip(-1, None)
P_REG = np.abs(P_REG)

Y01 = (Y_BIN == "yes").astype(int)
Y_CODES = np.searchsorted(CLASSES, Y_MULTI)

EXPECTED = {
    "roc_auc": (Y_BIN, P_BIN, skm.roc_auc_score(Y01, P_BIN)),
    "average_precision": (Y_BIN, P_BIN, skm.average_precision_score(Y01, P_BIN)),
    "f1": (Y_BIN, L_BIN, skm.f1_score(Y_BIN, L_BIN, pos_label="yes")),
    "precision": (Y_BIN, L_BIN, skm.precision_score(Y_BIN, L_BIN, pos_label="yes")),
    "recall": (Y_BIN, L_BIN, skm.recall_score(Y_BIN, L_BIN, pos_label="yes")),
    "log_loss": (Y_MULTI, P_MULTI, skm.log_loss(Y_MULTI, P_MULTI, labels=CLASSES)),
    "accuracy": (Y_MULTI, L_MULTI, skm.accuracy_score(Y_MULTI, L_MULTI)),
    "balanced_accuracy": (Y_MULTI, L_MULTI, skm.balanced_accuracy_score(Y_MULTI, L_MULTI)),
    "mcc": (Y_MULTI, L_MULTI, skm.matthews_corrcoef(Y_MULTI, L_MULTI)),
    "f1_macro": (Y_MULTI, L_MULTI, skm.f1_score(Y_MULTI, L_MULTI, average="macro")),
    "f1_micro": (Y_MULTI, L_MULTI, skm.f1_score(Y_MULTI, L_MULTI, average="micro")),
    "f1_weighted": (Y_MULTI, L_MULTI, skm.f1_score(Y_MULTI, L_MULTI, average="weighted")),
    "roc_auc_ovo_macro": (Y_MULTI, P_MULTI, skm.roc_auc_score(Y_MULTI, P_MULTI, multi_class="ovo", average="macro")),
    "roc_auc_ovr_macro": (Y_MULTI, P_MULTI, skm.roc_auc_score(Y_MULTI, P_MULTI, multi_class="ovr", average="macro")),
    "mean_poisson_deviance": (Y_REG, P_REG, skm.mean_poisson_deviance(Y_REG, P_REG)),
    "rmse": (Y_REG, P_REG, np.sqrt(skm.mean_squared_error(Y_REG, P_REG))),
    "mae": (Y_REG, P_REG, skm.mean_absolute_error(Y_REG, P_REG)),
    "mse": (Y_REG, P_REG, skm.mean_squared_error(Y_REG, P_REG)),
    "r2": (Y_REG, P_REG, skm.r2_score(Y_REG, P_REG)),
    "rmsle": (Y_REG, P_REG, np.sqrt(np.mean((np.log1p(Y_REG) - np.log1p(P_REG)) ** 2))),
    "mape": (Y_REG, P_REG, skm.mean_absolute_percentage_error(Y_REG, P_REG)),
    "median_absolute_error": (Y_REG, P_REG, skm.median_absolute_error(Y_REG, P_REG)),
    "pearsonr": (Y_REG, P_REG, scipy.stats.pearsonr(Y_REG, P_REG).statistic),
    "spearmanr": (Y_REG, P_REG, scipy.stats.spearmanr(Y_REG, P_REG).statistic),
}


def test_every_standard_metric_has_a_reference_value() -> None:
    assert set(EXPECTED) == {name for name, d in METRICS.items() if d.kind == "standard"}


@pytest.mark.parametrize("name", sorted(EXPECTED))
def test_standard_metric_equals_its_reference(name: str) -> None:
    y_true, y_pred, expected = EXPECTED[name]
    problem_type = METRICS[name].problem_types[-1]
    spec = metric_spec(Metric.source(name, reference="https://example.org"), problem_type)
    assert score(spec, y_true, y_pred) == pytest.approx(expected, rel=1e-12, abs=1e-12)


def test_binary_log_loss_and_accuracy_take_both_problem_types() -> None:
    p2 = np.column_stack([1 - P_BIN, P_BIN])
    spec = Metric.source("log_loss").resolve("binary_classification")
    assert score(spec, Y_BIN, P_BIN) == pytest.approx(skm.log_loss(Y01, P_BIN))
    assert score(spec, Y_BIN, p2) == pytest.approx(skm.log_loss(Y01, P_BIN))
    assert score(Metric.source("accuracy"), Y_BIN, L_BIN) == pytest.approx(skm.accuracy_score(Y_BIN, L_BIN))


def test_labels_set_the_column_order_and_the_positive_class() -> None:
    reversed_labels = ["yes", "no"]  # the positive class is labels[1]: "no"
    expected = skm.roc_auc_score(1 - Y01, P_BIN)
    assert score(Metric.source("roc_auc"), Y_BIN, P_BIN, labels=reversed_labels) == pytest.approx(expected)
    order = [2, 0, 3, 1]
    shuffled = [CLASSES[i] for i in order]
    loss = score(Metric.source("log_loss"), Y_MULTI, P_MULTI[:, order], labels=shuffled)
    assert loss == pytest.approx(EXPECTED["log_loss"][2])


def test_the_registry_is_the_source_of_known_metrics() -> None:
    assert m.known_metrics() == bundle_checks.KNOWN_METRICS
    assert bundle_checks.TABARENA_DEFAULT_METRICS == m.FALLBACK_METRICS
    standard = {name for name, d in METRICS.items() if d.kind == "standard"}
    assert m.known_metrics()["binary_classification"] & standard == {
        "roc_auc",
        "average_precision",
        "log_loss",
        "accuracy",
        "balanced_accuracy",
        "f1",
        "mcc",
        "precision",
        "recall",
    }


@pytest.mark.parametrize(
    ("problem_type", "name", "prediction", "greater"),
    [
        ("binary_classification", "roc_auc", "proba", True),
        ("multiclass_classification", "log_loss", "proba", False),
        ("regression", "rmse", "value", False),
    ],
)
def test_fallback_resolves_by_problem_type(problem_type, name, prediction, greater) -> None:
    spec = metric_spec(Metric.fallback(reason="no metric on the page"), problem_type)
    assert (spec.name, spec.kind, spec.origin, spec.prediction, spec.greater_is_better) == (
        name,
        "standard",
        "fallback",
        prediction,
        greater,
    )
    assert spec.reason == "no metric on the page"


def test_constructors_refuse_unknown_names_and_params() -> None:
    with pytest.raises(ValueError, match="Did you mean roc_auc"):
        Metric.source("roc_auk")
    with pytest.raises(ValueError, match="takes the params"):
        Metric.source("rmse", params={"k": 3})
    with pytest.raises(ValueError, match="origin"):
        Metric(name="rmse", origin="guess")


def test_spec_round_trips_through_json() -> None:
    spec = metric_spec(
        Metric.stand_in("pearsonr", original="per-era CORR", reason="needs eras", reference="https://numer.ai"),
        "regression",
    )
    task = PredictiveMLTaskMetadataV2(
        target_column_name="y",
        problem_type="regression",
        objective_metric=spec,
        scoring_columns=[ScoringColumn(column="era", role="group", used_by="pearsonr", description="the week")],
    )
    adapter = TypeAdapter(PredictiveMLTaskMetadataV2)
    dumped = json.loads(json.dumps(adapter.dump_python(task, mode="json")))
    assert dumped["objective_metric"]["origin"] == "stand_in"
    assert adapter.validate_python(dumped) == task
    # the plain JSON dict scores like the spec
    assert score(dumped["objective_metric"], Y_REG, P_REG) == pytest.approx(EXPECTED["pearsonr"][2])


def _group_metric() -> m.MetricDef:
    def mean_group_mae(y_true, y_pred, *, group, **_):
        frame = pd.DataFrame({"e": np.abs(y_true - np.asarray(y_pred, dtype=float)), "g": group})
        return float(frame.groupby("g")["e"].mean().mean())

    return m.MetricDef(
        name="test_mean_group_mae",
        problem_types=("regression",),
        prediction="value",
        greater_is_better=False,
        fn=mean_group_mae,
        implementation="test",
        definition="mean over groups of the group's MAE",
        kind="custom",
        inputs=("group",),
    )


class _Container:
    """Duck-typed container: what `scorer` reads."""

    def __init__(self, df: pd.DataFrame, task: PredictiveMLTaskMetadataV2) -> None:
        self.dataset = df
        self.task_metadata = task


def test_scorer_takes_the_group_input_by_row_index(monkeypatch: pytest.MonkeyPatch) -> None:
    definition = _group_metric()
    monkeypatch.setitem(METRICS, definition.name, definition)
    df = pd.DataFrame({"x": np.arange(8.0), "era": list("aabbccdd"), "y": np.arange(8.0)})
    spec = metric_spec(
        Metric.source(definition.name, reference="https://example.org", inputs={"group": "era"}), "regression"
    )
    task = PredictiveMLTaskMetadataV2(
        target_column_name="y",
        problem_type="regression",
        objective_metric=spec,
        scoring_columns=[ScoringColumn(column="era", role="group", used_by=definition.name, description="d")],
    )
    rows = np.array([1, 2, 3, 6])  # groups a, b, b, d
    y_pred = df["y"].to_numpy()[rows] + np.array([1.0, 2.0, 0.0, 4.0])
    value = scorer(_Container(df, task))(df["y"].to_numpy()[rows], y_pred, rows)
    assert value == pytest.approx(np.mean([1.0, 1.0, 4.0]))
    with pytest.raises(ValueError, match="row_index"):
        scorer(_Container(df, task))(df["y"].to_numpy()[rows], y_pred)
    with pytest.raises(ValueError, match="needs the input"):
        score(spec, df["y"].to_numpy()[rows], y_pred)


def test_scorer_uses_the_target_categories_as_labels() -> None:
    df = pd.DataFrame({"y": pd.Categorical(Y_BIN, categories=["yes", "no"])})
    task = PredictiveMLTaskMetadataV2(
        target_column_name="y",
        problem_type="binary_classification",
        objective_metric=metric_spec(Metric.fallback(reason="r"), "binary_classification"),
    )
    value = scorer(_Container(df, task))(Y_BIN, P_BIN)  # P_BIN is the probability of "no", the second category
    assert value == pytest.approx(skm.roc_auc_score(1 - Y01, P_BIN))


def test_local_metric_scores_with_its_own_code_but_its_spec_does_not() -> None:
    local = Metric.local(lambda y, p, **_: float(np.max(np.abs(y - p))), name="max_error", prediction="value",
                         greater_is_better=False)  # fmt: skip
    assert score(local, Y_REG, P_REG) == pytest.approx(np.max(np.abs(Y_REG - P_REG)))
    spec = metric_spec(local, "regression")
    assert spec.kind == "local"
    with pytest.raises(ValueError, match="local"):
        score(spec, Y_REG, P_REG)


def test_to_sklearn_scorer_matches_cross_validation_use() -> None:
    x = RNG.normal(size=(200, 3))
    y = np.where(x[:, 0] + RNG.normal(size=200) > 0, "yes", "no")
    model = LogisticRegression().fit(x, y)
    sk = to_sklearn_scorer(Metric.source("roc_auc"))
    assert sk(model, x, y) == pytest.approx(skm.roc_auc_score(y == "yes", model.predict_proba(x)[:, 1]))
    rmse = to_sklearn_scorer(Metric.source("rmse"))
    reg = LinearRegression().fit(x, x[:, 0])
    assert rmse(reg, x, x[:, 0]) == pytest.approx(-0.0, abs=1e-9)  # greater_is_better=False: negated


def test_dummy_prediction_matches_the_kind() -> None:
    assert m.dummy_prediction("proba", Y_BIN, 10).shape == (10,)
    assert m.dummy_prediction("proba", Y_MULTI, 10).shape == (10, 4)
    assert set(m.dummy_prediction("label", Y_MULTI, 50)) <= set(CLASSES)


def test_the_module_imports_nothing_else_from_data_foundry() -> None:
    """It can be copied out on its own."""
    tree = ast.parse(Path(m.__file__).read_text())
    imported = {
        alias.name.split(".")[0] for node in ast.walk(tree) if isinstance(node, ast.Import) for alias in node.names
    }
    imported |= {node.module.split(".")[0] for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)}
    assert imported <= {"__future__", "collections", "dataclasses", "difflib", "math", "typing", "numpy", "pandas",
                        "sklearn", "scipy"}  # fmt: skip


def test_metric_spec_fields_are_the_spec_dict() -> None:
    assert {f.name for f in dataclasses.fields(MetricSpec)} == set(Metric.source("rmse").spec("regression"))


def test_scorer_aggregates_per_group_as_the_grouping_says():
    from types import SimpleNamespace

    from data_foundry.v2.metrics import Metric, scorer

    frame = pd.DataFrame(
        {
            "y": pd.Categorical(["no", "no", "yes", "yes", "no", "no"]),
            "customer": ["a", "a", "b", "b", "c", "c"],
            "date": [2, 1, 1, 2, 2, 1],
        }
    )
    spec = Metric.source("roc_auc", original="AUC", reference="x").spec("binary_classification")
    for how, pred, expected in (
        ("mean", [0.1, 0.3, 0.9, 0.7, 0.2, 0.6], 1.0),
        ("last", [0.1, 0.9, 0.2, 0.8, 0.3, 0.95], 1.0),
    ):
        grouping = SimpleNamespace(on="customer", prediction_unit="group", aggregation=how, time_on="date")
        task = SimpleNamespace(target_column_name="y", objective_metric=spec, grouping=grouping)
        score_rows = scorer(SimpleNamespace(task_metadata=task, dataset=frame))
        assert score_rows(frame["y"].to_numpy(), np.array(pred), np.arange(6)) == pytest.approx(expected)


def test_a_metric_from_context_needs_a_reason():
    from data_foundry.v2.metrics import Metric

    spec = Metric.from_context("rmsle", reason="a price's error matters relative to the price").spec("regression")
    assert (spec["name"], spec["origin"]) == ("rmsle", "context")
    with pytest.raises(TypeError):
        Metric.from_context("rmsle")  # type: ignore[call-arg]


# --- target_transform: the target ships on a modelling scale, the metric is computed on the original scale ---------

_TRANSFORMS = {"log": np.log, "log1p": np.log1p, "log10": np.log10}


@pytest.mark.parametrize("transform", sorted(_TRANSFORMS))
@pytest.mark.parametrize("name", ["rmse", "mae", "rmsle", "r2"])
def test_target_transform_scores_on_the_original_scale(transform: str, name: str) -> None:
    """The inverse of the shipped scale is applied to y_true and y_pred before the metric."""
    rng = np.random.default_rng(3)
    raw = rng.uniform(1, 1000, 400)
    pred = raw * rng.uniform(0.7, 1.3, 400)
    forward = _TRANSFORMS[transform]
    shipped = metric_spec(Metric.source(name, reference="x", target_transform=transform), "regression")
    plain = metric_spec(Metric.source(name, reference="x"), "regression")
    assert shipped.target_transform == transform
    expected = score(plain, raw, pred)
    assert score(shipped, forward(raw), forward(pred)) == pytest.approx(expected, rel=1e-9)
    # the dict of the JSON file, the Metric itself and the sklearn scorer all invert
    assert score(dataclasses.asdict(shipped), forward(raw), forward(pred)) == pytest.approx(expected, rel=1e-9)
    assert score(Metric.source(name, target_transform=transform), forward(raw), forward(pred)) == pytest.approx(
        expected, rel=1e-9
    )


def test_rmsle_on_a_log_shipped_target_equals_rmsle_on_the_raw_values() -> None:
    """RMSLE of a log- or log1p-shipped price is RMSLE on the price."""
    rng = np.random.default_rng(4)
    price = rng.lognormal(8, 1, 1000)
    pred = price * rng.lognormal(0, 0.2, 1000)
    spec = Metric.from_context("rmsle", reason="a price", target_transform="log").spec("regression")
    expected = np.sqrt(np.mean((np.log1p(pred) - np.log1p(price)) ** 2))
    assert score(spec, np.log(price), np.log(pred)) == pytest.approx(expected, rel=1e-9)
    # rmsle of a log1p-shipped target is the rmse of the shipped values
    spec = Metric.source("rmsle", reference="x", target_transform="log1p").spec("regression")
    assert score(spec, np.log1p(price), np.log1p(pred)) == pytest.approx(expected, rel=1e-9)


def test_target_transform_is_for_regression_only() -> None:
    """A transform on a classification metric, or an unknown transform, is refused."""
    with pytest.raises(ValueError, match="regression"):
        Metric.source("roc_auc", target_transform="log")
    with pytest.raises(ValueError, match="regression"):
        Metric.fallback(reason="none", target_transform="log").spec("binary_classification")
    with pytest.raises(ValueError, match="target_transform is one of"):
        Metric.source("rmse", target_transform="sqrt")
    with pytest.raises(ValueError, match="regression"):
        MetricSpec(
            name="roc_auc",
            kind="standard",
            prediction="proba",
            greater_is_better=True,
            origin="source",
            target_transform="log",
        )
    # a fallback rmse on a log target can declare it too
    assert Metric.fallback(reason="none", target_transform="log").spec("regression")["target_transform"] == "log"


def test_target_transform_round_trips_through_json() -> None:
    """The field survives the JSON file; a spec saved before it existed reads as identity."""
    spec = metric_spec(Metric.source("rmsle", reference="x", target_transform="log1p"), "regression")
    task = PredictiveMLTaskMetadataV2(target_column_name="y", problem_type="regression", objective_metric=spec)
    adapter = TypeAdapter(PredictiveMLTaskMetadataV2)
    dumped = json.loads(json.dumps(adapter.dump_python(task, mode="json")))
    assert dumped["objective_metric"]["target_transform"] == "log1p"
    assert adapter.validate_python(dumped) == task
    # a spec saved before the field existed reads as identity
    del dumped["objective_metric"]["target_transform"]
    assert adapter.validate_python(dumped).objective_metric.target_transform == "identity"
    assert any("target_transform" in line for line in spec.describe_lines())


@pytest.mark.parametrize("bad", [0.0, -1.0, np.nan, np.inf, -np.inf])
def test_poisson_deviance_rejects_invalid_expected_means(bad) -> None:
    """Computability probes must not weaken the real scorer's strict domain."""
    with pytest.raises(ValueError, match=r"deviance|NaN|infinity"):
        score(Metric.source("mean_poisson_deviance"), [0, 1, 3], [0.2, bad, 2.0])


def test_poisson_deviance_matches_source_likelihood_with_zero_observations() -> None:
    """Compare the source Poisson log-likelihood ratio independently of sklearn."""
    rng = np.random.default_rng(4267)
    y = rng.poisson(0.2, 1000)
    p = rng.lognormal(-2, 1, 1000)
    expected = -2 * np.mean(scipy.stats.poisson.logpmf(y, p) - scipy.stats.poisson.logpmf(y, y))
    assert score(Metric.source("mean_poisson_deviance"), y, p) == pytest.approx(expected, abs=1e-12)
    assert score(Metric.source("mean_poisson_deviance"), [0], [0.25]) == pytest.approx(0.5)
    with pytest.raises(ValueError, match="deviance"):
        score(Metric.source("mean_poisson_deviance"), [-1, 0], [1, 1])
