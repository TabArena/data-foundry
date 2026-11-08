"""Every registered metric under edge cases: the stability rules of a metric in the library.

The rules (``knowledge-data-foundry/references/definitions.md``, "Metric stability"): a prediction a model can make
(constant, tied, zero, negative, huge, probabilities of 0 and 1) gets a finite score; the score does not depend on the
row order, ties included; a NaN or infinite prediction raises a ValueError; a fold whose truth leaves the metric
undefined (one class, a constant target, no loss) gives NaN or a ValueError, never an infinite value, a
ZeroDivisionError or a number made of rounding noise. A metric added to the registry is checked here automatically;
it needs an entry in ``EXAMPLE_PARAMS`` when it takes required params.
"""

from __future__ import annotations

import warnings

import numpy as np
import pytest
from data_foundry.v2.dataset import metric_spec
from data_foundry.v2.metrics import METRICS, Metric, score

EXAMPLE_PARAMS = {
    ("cost_matrix", "binary_classification"): {"labels": [0, 1], "matrix": [[0, 1], [5, 0]]},
    ("cost_matrix", "multiclass_classification"): {"labels": [0, 1, 2], "matrix": [[0, 1, 2], [1, 0, 1], [2, 1, 0]]},
    ("precision_at_k", "binary_classification"): {"k": 5},
    ("average_precision_at_k", "binary_classification"): {"k": 5},
    ("par_k", "regression"): {"cutoff": 100},
    ("mean_group_top_k_overlap", "regression"): {"k": 3},
    ("mean_tweedie_deviance", "regression"): {"power": 1.5, "min_prediction": 1.0},
    ("mean_poisson_deviance", "regression"): {"min_prediction": 1e-6},
}
"""Params for metrics that cannot be declared without them."""

N = 72
CASES = [(name, problem_type) for name, d in METRICS.items() for problem_type in d.problem_types]
IDS = [f"{name}-{problem_type.split('_')[0]}" for name, problem_type in CASES]


def _spec(name: str, problem_type: str):
    d = METRICS[name]
    params = EXAMPLE_PARAMS.get((name, problem_type), {})
    metric = Metric.source(name, reference="x", params=params, inputs={role: role for role in d.inputs})
    return metric_spec(metric, problem_type)


def _n_classes(problem_type: str) -> int:
    return 2 if problem_type == "binary_classification" else 3


def _inputs(name: str, n: int) -> dict[str, np.ndarray]:
    roles = METRICS[name].inputs
    values = {
        "group": np.repeat(np.arange(n // 6 + 1), 6)[:n],  # groups of 6 rows (an era, a patient, an instance)
        "order": np.tile(np.arange(6), n // 6 + 1)[:n],  # each group's hours or weeks
        "weight": np.random.default_rng(5).uniform(0.5, 2.0, n),
    }
    return {role: values[role] for role in roles}


def _truth(problem_type: str, n: int = N) -> np.ndarray:
    rng = np.random.default_rng(1)
    if problem_type == "regression":
        return rng.gamma(1.0, 50.0, n) * (rng.random(n) < 0.6) + 0.5  # skewed, positive (mape, rmspe need y != 0)
    k = _n_classes(problem_type)
    y = rng.integers(0, k, n)
    y[: 2 * k] = np.tile(np.arange(k), 2)  # every class present, also within the first groups
    return y


def _labels(problem_type: str) -> list[int] | None:
    return None if problem_type == "regression" else list(range(_n_classes(problem_type)))


def _prediction(name: str, problem_type: str, y: np.ndarray, kind: str) -> np.ndarray | None:
    """A prediction of the metric's kind: ``fair`` (informative), or a degenerate one a model can make."""
    rng = np.random.default_rng(2)
    n = len(y)
    prediction = METRICS[name].prediction
    if prediction == "value":
        fair = np.where(rng.random(n) < 0.5, y, y.mean()) + rng.normal(0, 5, n)
        return {
            "fair": fair,
            "constant": np.full(n, 3.0),
            "zero": np.zeros(n),
            "negative": -np.abs(fair) - 1,
            "huge": np.abs(fair) * 1e9,
            "tied": np.round(fair / 40) * 40,
        }.get(kind)
    if prediction == "label":
        return {
            "fair": np.where(rng.random(n) < 0.7, y, rng.integers(0, y.max() + 1, n)),
            "constant": np.zeros(n, dtype=y.dtype),
            "tied": y.copy(),
        }.get(kind)
    k = _n_classes(problem_type)
    if k == 2:
        fair = np.clip(0.5 + 0.3 * (y - 0.5) + rng.normal(0, 0.2, n), 0.01, 0.99)
        return {
            "fair": fair,
            "constant": np.full(n, 0.3),
            "zero": np.where(y == 1, 0.0, 1.0),  # certain and wrong
            "tied": np.round(fair, 1),
        }.get(kind)
    fair = rng.dirichlet(np.ones(k), n)
    tied = np.round(fair, 1) + 1e-3
    return {
        "fair": fair,
        "constant": np.full((n, k), 1 / k),
        "zero": np.eye(k)[(y + 1) % k],  # certain and wrong
        "tied": tied / tied.sum(axis=1, keepdims=True),
    }.get(kind)


def _score(name, problem_type, y, p, **inputs):
    return score(_spec(name, problem_type), y, p, labels=_labels(problem_type), **inputs)


@pytest.mark.parametrize(("name", "problem_type"), CASES, ids=IDS)
@pytest.mark.parametrize("kind", ["fair", "constant", "zero", "negative", "huge", "tied"])
def test_any_prediction_a_model_can_make_gets_a_finite_score(name: str, problem_type: str, kind: str) -> None:
    """Constant, tied, zero, negative or huge values and certain probabilities score a finite number, without the
    warnings of an ill-defined value (a constant baseline is a model too).
    """
    y = _truth(problem_type)
    p = _prediction(name, problem_type, y, kind)
    if p is None:
        pytest.skip(f"no {kind} prediction of kind {METRICS[name].prediction}")
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        value = _score(name, problem_type, y, p, **_inputs(name, len(y)))
    assert np.isfinite(value), (name, kind, value)


@pytest.mark.parametrize(("name", "problem_type"), CASES, ids=IDS)
def test_the_score_does_not_depend_on_the_row_order(name: str, problem_type: str) -> None:
    """Rows in any order, tied predictions included, give the same score (tied rows count by the mean over their
    orderings, not by their position).
    """
    y = _truth(problem_type)
    p = _prediction(name, problem_type, y, "tied")
    inputs = _inputs(name, len(y))
    perm = np.random.default_rng(3).permutation(len(y))
    first = _score(name, problem_type, y, p, **inputs)
    second = _score(name, problem_type, y[perm], p[perm], **{role: v[perm] for role, v in inputs.items()})
    assert second == pytest.approx(first, rel=1e-9, abs=1e-12), name


WEIGHTED = [(name, problem_type) for name, problem_type in CASES if "weight" in METRICS[name].optional_inputs]


@pytest.mark.parametrize(("name", "problem_type"), WEIGHTED, ids=[f"{name}-{p.split('_')[0]}" for name, p in WEIGHTED])
@pytest.mark.parametrize("kind", ["fair", "constant", "zero", "negative", "huge", "tied"])
def test_an_optional_weight_keeps_the_score_finite_and_free_of_the_row_order(
    name: str, problem_type: str, kind: str
) -> None:
    """A metric that may take a ``weight`` (the deviances, RMSE) meets the same rules with one."""
    y = _truth(problem_type)
    p = _prediction(name, problem_type, y, kind)
    if p is None:
        pytest.skip(f"no {kind} prediction of kind {METRICS[name].prediction}")
    params = EXAMPLE_PARAMS.get((name, problem_type), {})
    spec = metric_spec(Metric.source(name, reference="x", params=params, inputs={"weight": "w"}), problem_type)
    w = np.random.default_rng(5).choice([0.2, 0.5, 1.0], len(y))
    perm = np.random.default_rng(3).permutation(len(y))
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        first = score(spec, y, p, weight=w)
    assert np.isfinite(first), (name, kind, first)
    assert score(spec, y[perm], p[perm], weight=w[perm]) == pytest.approx(first, rel=1e-9, abs=1e-12), name


@pytest.mark.parametrize(("name", "problem_type"), CASES, ids=IDS)
@pytest.mark.parametrize("bad", [np.nan, np.inf])
def test_a_nan_or_infinite_prediction_raises(name: str, problem_type: str, bad: float) -> None:
    """A model's NaN or infinite output is an error, never a silent NaN or a score that skipped the row."""
    if METRICS[name].prediction == "label":
        pytest.skip("labels are class values, not numbers")
    y = _truth(problem_type)
    p = _prediction(name, problem_type, y, "fair").astype(float)
    p[(0, 0) if p.ndim == 2 else 0] = bad
    with pytest.raises(ValueError, match="NaN or infinite"):
        _score(name, problem_type, y, p, **_inputs(name, len(y)))


def _degenerate_truths(problem_type: str) -> dict[str, np.ndarray]:
    if problem_type == "regression":
        return {"constant": np.full(N, 7.0), "zeros": np.zeros(N), "one row": np.array([3.0])}
    return {"one class": np.zeros(N, dtype=int), "one row": np.array([1])}


@pytest.mark.parametrize(("name", "problem_type"), CASES, ids=IDS)
def test_a_fold_that_leaves_the_metric_undefined_gives_nan_or_a_value_error(name: str, problem_type: str) -> None:
    """One class, a constant target, no loss, one row: NaN or a clear ValueError, never an infinite value, another
    exception or a number made of rounding noise (|score| above 1e6 for a metric of shares, ranks or relative error).
    """
    for label, y in _degenerate_truths(problem_type).items():
        p = _prediction(name, problem_type, np.resize(_truth(problem_type), len(y)), "fair")[: len(y)]
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")  # scikit-learn's own warnings on a degenerate fold are allowed here
                value = _score(name, problem_type, y, p, **_inputs(name, len(y)))
        except ValueError:
            continue
        assert not np.isinf(value), (name, label, value)
        if np.isfinite(value) and name not in {"rmse", "mse", "mae", "median_absolute_error", "par_k"}:
            assert abs(value) < 1e6, (name, label, value)  # scale-free metrics: a huge value is rounding noise
