"""The custom metrics of ``data_foundry.v2.metrics`` against their official or reference implementations.

Each official implementation is vendored below, as published (only reformatted, with the I/O around it removed), with
its source. Each metric is also checked on a small case computed by hand. The 1M-row timings were measured
once, on 2026-10-21, and are not part of the test run.
"""

from __future__ import annotations

import itertools

import numpy as np
import pandas as pd
import pytest
from data_foundry.schema import ScoringColumn
from data_foundry.v2.dataset import metric_spec
from data_foundry.v2.metrics import METRICS, Metric, dummy_prediction, row_weight_column, score
from scipy import special, stats
from sklearn.metrics import mean_squared_error, roc_auc_score

from tests.test_bundle_checks import make_iid_frame, make_v2_container, metric_findings

CUSTOM = sorted(name for name, d in METRICS.items() if d.kind == "custom")


def _spec(name: str, problem_type: str, **kwargs):
    return metric_spec(Metric.source(name, reference="https://example.org", **kwargs), problem_type)


# --- cost_matrix ---------------------------------------------------------------------------------------------------

# FORCE 2020 penalty matrix, lithology_competition/data/penalty_matrix.npy of
# https://github.com/bolgebrygg/Force-2020-Machine-Learning-competition (rows and columns in the order of the starter
# notebook's lithology_numbers: 30000, 65030, 65000, 80000, 74000, 70000, 70032, 88000, 86000, 99000, 90000, 93000).
FORCE_A = np.array(
    [
        [0.0, 2.0, 3.5, 3.0, 3.75, 3.5, 3.5, 4.0, 4.0, 2.5, 3.875, 3.25],
        [2.0, 0.0, 2.375, 2.75, 4.0, 3.75, 3.75, 3.875, 4.0, 3.0, 3.75, 3.0],
        [3.5, 2.375, 0.0, 2.0, 3.5, 3.5, 3.75, 4.0, 4.0, 2.75, 3.25, 3.0],
        [3.0, 2.75, 2.0, 0.0, 2.5, 2.0, 2.25, 4.0, 4.0, 3.375, 3.75, 3.25],
        [3.75, 4.0, 3.5, 2.5, 0.0, 2.625, 2.875, 3.75, 3.25, 3.0, 4.0, 3.625],
        [3.5, 3.75, 3.5, 2.0, 2.625, 0.0, 1.375, 4.0, 3.75, 3.5, 4.0, 3.625],
        [3.5, 3.75, 3.75, 2.25, 2.875, 1.375, 0.0, 4.0, 3.75, 3.125, 4.0, 3.75],
        [4.0, 3.875, 4.0, 4.0, 3.75, 4.0, 4.0, 0.0, 2.75, 3.75, 3.75, 4.0],
        [4.0, 4.0, 4.0, 4.0, 3.25, 3.75, 3.75, 2.75, 0.0, 4.0, 4.0, 3.875],
        [2.5, 3.0, 2.75, 3.375, 3.0, 3.5, 3.125, 3.75, 4.0, 0.0, 2.5, 3.25],
        [3.875, 3.75, 3.25, 3.75, 4.0, 4.0, 4.0, 3.75, 4.0, 2.5, 0.0, 4.0],
        [3.25, 3.0, 3.0, 3.25, 3.625, 3.625, 3.75, 4.0, 3.875, 3.25, 4.0, 0.0],
    ]
)
FORCE_CODES = [30000, 65030, 65000, 80000, 74000, 70000, 70032, 88000, 86000, 99000, 90000, 93000]


def force_score(y_true, y_pred, A=FORCE_A):
    """``score`` of the FORCE 2020 starter notebook (lithology_competition/data/starter_notebook.ipynb)."""
    S = 0.0
    y_true = y_true.astype(int)
    y_pred = y_pred.astype(int)
    for i in range(y_true.shape[0]):
        S -= A[y_true[i], y_pred[i]]
    return S / y_true.shape[0]


def test_cost_matrix_equals_the_force_2020_score_negated() -> None:
    rng = np.random.default_rng(1)
    t, p = rng.integers(0, 12, 5000), rng.integers(0, 12, 5000)
    names = [f"litho_{c}" for c in FORCE_CODES]
    spec = _spec("cost_matrix", "multiclass_classification", params={"labels": names, "matrix": FORCE_A.tolist()})
    value = score(spec, np.array(names)[t], np.array(names)[p])
    assert value == pytest.approx(-force_score(t, p), rel=1e-12)
    assert spec.greater_is_better is False
    assert spec.prediction == "label"


def test_cost_matrix_by_hand_and_from_probabilities() -> None:
    params = {"labels": ["good", "bad"], "matrix": [[0, 1], [5, 0]]}  # Statlog German credit: C[true][pred]
    y = np.array(["good", "good", "bad", "bad"])
    pred = np.array(["good", "bad", "good", "bad"])
    assert score(_spec("cost_matrix", "binary_classification", params=params), y, pred) == pytest.approx(6 / 4)
    # probabilities of the second sorted class ("good"), labels ["bad", "good"]: predict bad when p(bad) > 1/6
    proba_spec = _spec("cost_matrix", "binary_classification", params={**params, "prediction": "proba"})
    assert proba_spec.prediction == "proba"
    p_good = np.array([0.9, 0.8, 0.85, 0.1])  # p(bad) = 0.1, 0.2, 0.15, 0.9 -> good, bad, good, bad
    assert score(proba_spec, y, p_good) == pytest.approx((0 + 1 + 5 + 0) / 4)
    # aps_failure: 10 per false alarm, 500 per missed failure; the total cost is n times the mean
    aps = {"labels": ["neg", "pos"], "matrix": [[0, 10], [500, 0]]}
    y = np.array(["neg"] * 8 + ["pos"] * 2)
    pred = np.array(["neg"] * 7 + ["pos"] + ["neg", "pos"])
    assert score(_spec("cost_matrix", "binary_classification", params=aps), y, pred) * len(y) == pytest.approx(510)


def test_cost_matrix_refuses_bad_params() -> None:
    with pytest.raises(ValueError, match="missing param"):
        Metric.source("cost_matrix", params={"labels": ["a", "b"]})
    with pytest.raises(ValueError, match="2 x 2"):
        Metric.source("cost_matrix", params={"labels": ["a", "b"], "matrix": [[0, 1, 2]]})
    with pytest.raises(ValueError, match="prediction kind"):
        Metric.source("cost_matrix", params={"labels": ["a", "b"], "matrix": [[0, 1], [1, 0]], "prediction": "x"})


# --- precision_at_k / average_precision_at_k -----------------------------------------------------------------------


def apk(yt, s, k):
    """AP@k by the formula of Avito's evaluation page (its scorer is not public)."""
    order = np.argsort(-s)[:k]
    rel = yt[order]
    prec = np.cumsum(rel) / np.arange(1, len(rel) + 1)
    return float((prec * rel).sum() / min(k, yt.sum()))


def test_precision_at_k_equals_the_top_k_share_and_by_hand() -> None:
    rng = np.random.default_rng(2)
    y = rng.integers(0, 2, 4000)
    s = rng.uniform(size=4000)
    expected = y[np.argsort(-s)[:800]].mean()  # CoIL 2000: 800 of 4,000
    assert score(_spec("precision_at_k", "binary_classification", params={"k_fraction": 0.2}), y, s) == expected
    assert score(_spec("precision_at_k", "binary_classification", params={"k": 800}), y, s) == expected
    # ties at the cut-off count by their expected share: top 3 of scores [.9, .5, .5, .5, .1], two of the three
    # rows tied at .5 are positive, two slots -> 1 + 2 * 2/3
    y = np.array([1, 1, 0, 1, 0])
    s = np.array([0.9, 0.5, 0.5, 0.5, 0.1])
    value = score(_spec("precision_at_k", "binary_classification", params={"k": 3}), y, s)
    assert value == pytest.approx((1 + 2 * 2 / 3) / 3)


def test_average_precision_at_k_equals_the_reference() -> None:
    rng = np.random.default_rng(3)
    y = (rng.uniform(size=20000) < 0.05).astype(int)
    s = rng.uniform(size=20000) + 0.3 * y
    for k in (50, 1000, 5000):
        spec = _spec("average_precision_at_k", "binary_classification", params={"k": k})
        assert score(spec, y, s) == pytest.approx(apk(y, s, k), rel=1e-12)
    spec = _spec("average_precision_at_k", "binary_classification", params={"k_fraction": 0.025})
    assert score(spec, y, s) == pytest.approx(apk(y, s, 500), rel=1e-12)
    # by hand: ranks 1..4 relevant 1, 0, 1, 0; k = 4; two positives -> (1/1 + 2/3) / 2
    value = score(
        _spec("average_precision_at_k", "binary_classification", params={"k": 4}),
        np.array([1, 0, 1, 0, 0]),
        np.array([0.9, 0.8, 0.7, 0.6, 0.5]),
    )
    assert value == pytest.approx((1 + 2 / 3) / 2)


def test_top_k_params_take_exactly_one_cut_off() -> None:
    with pytest.raises(ValueError, match="exactly one"):
        Metric.source("precision_at_k")
    with pytest.raises(ValueError, match="exactly one"):
        Metric.source("precision_at_k", params={"k": 3, "k_fraction": 0.1})
    with pytest.raises(ValueError, match="k_fraction"):
        Metric.source("average_precision_at_k", params={"k_fraction": 1.5})


# --- rmspe ---------------------------------------------------------------------------------------------------------


def test_rmspe_ignores_zero_targets_and_by_hand() -> None:
    rng = np.random.default_rng(4)
    y = rng.integers(0, 3000, 5000).astype(float)
    y[:100] = 0
    p = y * rng.uniform(0.8, 1.2, 5000) + 5
    terms = [((yi - pi) / yi) ** 2 for yi, pi in zip(y, p, strict=True) if yi != 0]
    assert score(_spec("rmspe", "regression"), y, p) == pytest.approx(np.sqrt(np.mean(terms)), rel=1e-12)
    # by hand: (100 - 90) / 100 = 0.1, (200 - 220) / 200 = -0.1, the zero row is ignored -> 0.1
    assert score(_spec("rmspe", "regression"), [100, 200, 0], [90, 220, 7]) == pytest.approx(0.1)


# --- gini_top_capture (AmEx) ---------------------------------------------------------------------------------------


def amex_metric(y_true: pd.DataFrame, y_pred: pd.DataFrame) -> float:
    """The official AmEx metric, https://www.kaggle.com/code/inversion/amex-competition-metric-python (verbatim)."""

    def top_four_percent_captured(y_true: pd.DataFrame, y_pred: pd.DataFrame) -> float:
        df = pd.concat([y_true, y_pred], axis="columns").sort_values("prediction", ascending=False)
        df["weight"] = df["target"].apply(lambda x: 20 if x == 0 else 1)
        four_pct_cutoff = int(0.04 * df["weight"].sum())
        df["weight_cumsum"] = df["weight"].cumsum()
        df_cutoff = df.loc[df["weight_cumsum"] <= four_pct_cutoff]
        return (df_cutoff["target"] == 1).sum() / (df["target"] == 1).sum()

    def weighted_gini(y_true: pd.DataFrame, y_pred: pd.DataFrame) -> float:
        df = pd.concat([y_true, y_pred], axis="columns").sort_values("prediction", ascending=False)
        df["weight"] = df["target"].apply(lambda x: 20 if x == 0 else 1)
        df["random"] = (df["weight"] / df["weight"].sum()).cumsum()
        total_pos = (df["target"] * df["weight"]).sum()
        df["cum_pos_found"] = (df["target"] * df["weight"]).cumsum()
        df["lorentz"] = df["cum_pos_found"] / total_pos
        df["gini"] = (df["lorentz"] - df["random"]) * df["weight"]
        return df["gini"].sum()

    def normalized_weighted_gini(y_true: pd.DataFrame, y_pred: pd.DataFrame) -> float:
        y_true_pred = y_true.rename(columns={"target": "prediction"})
        return weighted_gini(y_true, y_pred) / weighted_gini(y_true, y_true_pred)

    g = normalized_weighted_gini(y_true, y_pred)
    d = top_four_percent_captured(y_true, y_pred)

    return 0.5 * (g + d)


@pytest.mark.parametrize("seed", [0, 1, 2])
def test_gini_top_capture_equals_the_official_amex_metric(seed: int) -> None:
    rng = np.random.default_rng(seed)
    n = 30000
    y = (rng.uniform(size=n) < 0.25).astype(int)
    s = rng.uniform(size=n) + 0.4 * y * rng.uniform(size=n)
    official = amex_metric(pd.DataFrame({"target": y}), pd.DataFrame({"prediction": s}))
    spec = _spec("gini_top_capture", "binary_classification", params={"top_fraction": 0.04, "negative_weight": 20})
    assert score(spec, y, s) == pytest.approx(official, rel=1e-10, abs=1e-12)
    assert score(_spec("gini_top_capture", "binary_classification"), y, s) == pytest.approx(official, rel=1e-10)


def test_gini_top_capture_by_hand() -> None:
    # a perfect ranking: normalized Gini 1; the top 4% of the weight holds all positives when they weigh < 4%
    y = np.array([1] * 2 + [0] * 98)  # weight 2 + 98 * 20 = 1962; cut-off int(78.48) = 78 >= 2
    s = np.r_[np.ones(2), np.zeros(98)] + np.linspace(0, 0.1, 100)[::-1]
    assert score(_spec("gini_top_capture", "binary_classification"), y, s) == pytest.approx(1.0)


# --- normalized_gini (Allstate 2011) and normalized_weighted_gini (Liberty Mutual 2014) ----------------------------


def kaggle_gini(actual, pred):
    """The normalized Gini reference code posted on Kaggle (Ben Hamner; reused by the insurance competitions)."""

    def gini(actual, pred):
        assert len(actual) == len(pred)
        all = np.asarray(np.c_[actual, pred, np.arange(len(actual))], dtype=float)  # noqa: A001 (as published)
        all = all[np.lexsort((all[:, 2], -1 * all[:, 1]))]  # noqa: A001
        total_losses = all[:, 0].sum()
        gini_sum = all[:, 0].cumsum().sum() / total_losses
        gini_sum -= (len(actual) + 1) / 2.0
        return gini_sum / len(actual)

    return gini(actual, pred) / gini(actual, actual)


def liberty_normalized_weighted_gini(solution, weights, submission):
    """Liberty Mutual Fire Peril's corrected weighted Gini (forum thread 9880); ``DataFrame.sort`` became
    ``sort_values``.
    """

    def weighted_gini(solution, weights, submission):
        df = pd.DataFrame({"solution": solution, "weights": weights, "submission": submission})
        df = df.sort_values("submission", ascending=False)
        df["random"] = (df.weights / df.weights.sum()).cumsum()
        total_pos = (df.solution * df.weights).sum()
        df["cumPosFound"] = (df.solution * df.weights).cumsum()
        df["Lorentz"] = df.cumPosFound / total_pos
        return sum(df.Lorentz[1:].values * (df.random[:-1])) - sum(df.Lorentz[:-1].values * (df.random[1:]))  # noqa: PD011

    return weighted_gini(solution, weights, submission) / weighted_gini(solution, weights, solution)


@pytest.mark.parametrize("seed", [0, 1, 2])
def test_normalized_gini_equals_the_kaggle_code(seed: int) -> None:
    rng = np.random.default_rng(seed)
    n = 20000
    y = np.where(rng.uniform(size=n) < 0.05, rng.lognormal(7, 1.5, n), 0.0)
    p = 0.3 * (y > 0) + rng.uniform(size=n)
    assert score(_spec("normalized_gini", "regression"), y, p) == pytest.approx(kaggle_gini(y, p), rel=1e-10)


def test_normalized_gini_by_hand() -> None:
    # sorted by p: losses 1, 3, 2, 0, 0 -> cumulative shares sum to 23 / 6, minus (5 + 1) / 2, over 5: 1 / 6;
    # perfect order 3, 2, 1, 0, 0 -> 26 / 6 - 3 = 4 / 3, over 5: 4 / 15; ratio 0.625
    value = score(_spec("normalized_gini", "regression"), [1, 0, 3, 0, 2], [0.9, 0.1, 0.8, 0.2, 0.5])
    assert value == pytest.approx(0.625)


@pytest.mark.parametrize("seed", [0, 1, 2])
def test_normalized_weighted_gini_equals_the_liberty_code(seed: int) -> None:
    rng = np.random.default_rng(seed)
    n = 20000
    y = np.where(rng.uniform(size=n) < 0.01, rng.exponential(2.0, n), 0.0)
    w = rng.uniform(0.1, 5.0, n)
    p = 0.5 * (y > 0) + rng.uniform(size=n)
    spec = _spec("normalized_weighted_gini", "regression", inputs={"weight": "w"})
    official = liberty_normalized_weighted_gini(y, w, p)
    assert score(spec, y, p, weight=w) == pytest.approx(official, rel=1e-10)


def test_normalized_ginis_score_a_constant_prediction_zero() -> None:
    rng = np.random.default_rng(0)
    y = np.where(rng.uniform(size=5000) < 0.05, rng.lognormal(7, 1.5, 5000), 0.0)
    w = rng.uniform(0.1, 5.0, 5000)
    assert score(_spec("normalized_gini", "regression"), y, np.ones_like(y)) == pytest.approx(0.0, abs=1e-12)
    spec = _spec("normalized_weighted_gini", "regression", inputs={"weight": "w"})
    assert score(spec, y, np.ones_like(y), weight=w) == pytest.approx(0.0, abs=1e-12)


def test_normalized_ginis_average_tied_predictions_over_their_orderings() -> None:
    # the official codes break ties by row order; the library scores the mean over all orderings of the tied rows
    y = np.array([0.0, 3.0, 0.0, 1.0, 2.0, 0.0])
    w = np.array([1.0, 2.0, 0.5, 4.0, 1.0, 3.0])
    p = np.array([0.7, 0.2, 0.2, 0.2, 0.9, 0.7])
    orders = [list(o) for o in itertools.permutations(range(6))]  # every row order, each one official value
    official = [kaggle_gini(y[o], p[o]) for o in orders]
    weighted = [liberty_normalized_weighted_gini(y[o], w[o], p[o]) for o in orders]
    assert score(_spec("normalized_gini", "regression"), y, p) == pytest.approx(np.mean(official), rel=1e-12)
    spec = _spec("normalized_weighted_gini", "regression", inputs={"weight": "w"})
    assert score(spec, y, p, weight=w) == pytest.approx(np.mean(weighted), rel=1e-12)


def frees_ordered_lorenz_gini(loss, base, score):
    """Frees, Meyers and Cummings (2011), eq. (2.2): 1 - 2 x the area under the ordered Lorenz curve, the rows sorted
    by ascending relativity score / base, x the cumulative share of the base premium, y the cumulative share of the
    losses (trapezoids between the points).
    """
    order = np.argsort(score / base, kind="stable")
    x = np.r_[0.0, np.cumsum(base[order])] / base.sum()
    y = np.r_[0.0, np.cumsum(loss[order])] / loss.sum()
    return 1.0 - 2.0 * float(np.sum((x[1:] - x[:-1]) * (y[1:] + y[:-1]) / 2.0))


@pytest.mark.parametrize("seed", [0, 1, 2])
def test_ordered_lorenz_gini_equals_frees_formula(seed: int) -> None:
    rng = np.random.default_rng(seed)
    n = 5000
    base = rng.lognormal(7, 1, n)
    y = np.where(rng.uniform(size=n) < 0.1, rng.lognormal(8, 1.5, n), 0.0)
    p = base * np.exp(0.5 * (y > 0) + rng.normal(0, 1, n))
    spec = _spec("ordered_lorenz_gini", "regression", inputs={"weight": "Premium"})
    official = frees_ordered_lorenz_gini(y, base, p)
    assert score(spec, y, p, weight=base) == pytest.approx(official, rel=1e-10)


def test_ordered_lorenz_gini_by_hand_and_on_the_base() -> None:
    # equal premiums, relativities in the losses' order: x 0, .25, .5, .75, 1 and y 0, 0, 0, .25, 1 give an area of
    # 0.1875 under the curve, so 1 - 2 x 0.1875 = 0.625; a score proportional to the base scores 0
    spec = _spec("ordered_lorenz_gini", "regression", inputs={"weight": "Premium"})
    base = np.array([1.0, 1.0, 1.0, 1.0])
    loss = np.array([0.0, 0.0, 1.0, 3.0])
    assert score(spec, loss, base * np.array([1, 2, 3, 4]), weight=base) == pytest.approx(0.625)
    base = np.array([100.0, 300.0, 50.0, 800.0])
    assert score(spec, loss, 2.5 * base, weight=base) == pytest.approx(0.0, abs=1e-12)


@pytest.mark.parametrize("seed", [0, 1])
def test_ordered_lorenz_gini_per_unit_scores_a_rate_with_its_exposure(seed: int) -> None:
    """``per_unit``: a loss per year insured ordered by the predicted rate, x the cumulative years. The same as the
    totals on the base of the years, and the unnormalised form of ``normalized_weighted_gini`` on the rate.
    """
    rng = np.random.default_rng(seed)
    n = 4000
    years = rng.uniform(0.05, 1.0, n)
    rate = np.where(rng.uniform(size=n) < 0.1, rng.lognormal(7, 1.2, n), 0.0) / years
    pred = np.exp(rng.normal(5, 1, n)) * (1 + (rate > 0))
    per_unit = _spec("ordered_lorenz_gini", "regression", inputs={"weight": "years"}, params={"per_unit": True})
    totals = _spec("ordered_lorenz_gini", "regression", inputs={"weight": "years"})
    got = score(per_unit, rate, pred, weight=years)
    assert got == pytest.approx(score(totals, rate * years, pred * years, weight=years), rel=1e-12)
    assert got == pytest.approx(frees_ordered_lorenz_gini(rate * years, years, pred * years), rel=1e-10)
    normalized = _spec("normalized_weighted_gini", "regression", inputs={"weight": "years"})
    best = score(per_unit, rate, rate, weight=years)
    assert got == pytest.approx(score(normalized, rate, pred, weight=years) * best, rel=1e-10)
    with pytest.raises(ValueError, match="per_unit"):
        Metric.source("ordered_lorenz_gini", inputs={"weight": "years"}, params={"per_unit": "yes"})


def test_normalized_weighted_gini_host_test_case() -> None:
    # the host's check in thread 9880: "should now score -0.821428571428572"
    spec = _spec("normalized_weighted_gini", "regression", inputs={"weight": "var11"})
    value = score(spec, [0, 0, 1, 0, 1], [0.1, 0.4, 0.3, 1.2, 0.0], weight=[1, 2, 5, 4, 3])
    assert value == pytest.approx(-0.821428571428572, rel=1e-12)


# --- rescaled_mean_tweedie_deviance --------------------------------------------------------------------------------


def rescaled_tweedie_reference(y, w, p, power, floor) -> float:
    """The formula written out, without scikit-learn: the predictions floored, multiplied by the factor that balances
    them with the truth on these rows, then the weighted mean of the Tweedie unit deviance.
    """
    y, w = np.asarray(y, dtype=float), np.asarray(w, dtype=float)
    p = np.maximum(np.asarray(p, dtype=float), floor)
    m = p * (w * y).sum() / (w * p).sum()
    q = power
    if q == 1:
        d = 2 * (special.xlogy(y, y / m) - y + m)
    else:
        d = 2 * (y ** (2 - q) / ((1 - q) * (2 - q)) - y * m ** (1 - q) / (1 - q) + m ** (2 - q) / (2 - q))
    return float((w * d).sum() / w.sum())


def _rescaled(power: float = 1.5, floor: float = 1e-6):
    params = {"power": power, "min_prediction": floor}
    return _spec("rescaled_mean_tweedie_deviance", "regression", params=params, inputs={"weight": "w"})


def _pure_premiums(seed: int, n: int = 20000) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """A charge per year insured over realized years in (0.05, 1], mostly 0, and a predicted rate (some below 1)."""
    rng = np.random.default_rng(seed)
    years = rng.uniform(0.05, 1.0, n)
    rate = np.where(rng.uniform(size=n) < 0.08, rng.gamma(2.0, 400.0, n), 0.0) / years
    pred = rng.gamma(1.0, 60.0, n) * (1 + (rate > 0))
    return rate, years, pred


@pytest.mark.parametrize("seed", [0, 1, 2])
@pytest.mark.parametrize("power", [1.0, 1.5, 1.8])
def test_rescaled_mean_tweedie_deviance_equals_the_formula(seed: int, power: float) -> None:
    """Equal to the formula written out, at three powers, with predictions below the floor."""
    rate, years, pred = _pure_premiums(seed)
    floor = 0.5  # some predictions fall below it
    assert (pred < floor).any()
    expected = rescaled_tweedie_reference(rate, years, pred, power, floor)
    assert score(_rescaled(power, floor), rate, pred, weight=years) == pytest.approx(expected, rel=1e-9)


def test_rescaled_mean_tweedie_deviance_by_hand() -> None:
    """Small cases worked out by hand, the floor before the factor."""
    # y = (0, 4), w = (1, 1), p = (1, 1): c = 4 / 2, m = (2, 2). At q = 1.5 the unit deviance is
    # 2 * (-4 sqrt(y) + 2 y / sqrt(m) + 2 sqrt(m)): 4 sqrt(2) for y = 0, -16 + 12 sqrt(2) for y = 4;
    # the mean is 8 (sqrt(2) - 1)
    assert score(_rescaled(), [0, 4], [1, 1], weight=[1, 1]) == pytest.approx(8 * (np.sqrt(2) - 1), rel=1e-12)
    # w = (3, 1), p = (5, 5): c = 4 / 20, m = (1, 1); the deviance is 4 for y = 0 and 4 for y = 4, weighted mean 4
    assert score(_rescaled(), [0, 4], [5, 5], weight=[3, 1]) == pytest.approx(4.0, rel=1e-12)
    # at q = 1 (Poisson): m = (2, 2); 2 * 2 = 4 for y = 0 and 2 * (4 log 2 - 2) for y = 4, mean 4 log 2
    assert score(_rescaled(1.0), [0, 4], [1, 1], weight=[1, 1]) == pytest.approx(4 * np.log(2), rel=1e-12)
    # the floor applies before the factor: p = (0, 1) at a floor of 0.5 is (0.5, 1), c = 2 / 1.5, m = (2/3, 4/3)
    expected = rescaled_tweedie_reference([0, 2], [1, 1], [0.5, 1.0], 1.5, 0.5)
    assert score(_rescaled(1.5, 0.5), [0, 2], [0.0, 1.0], weight=[1, 1]) == pytest.approx(expected, rel=1e-12)


def test_rescaled_mean_tweedie_deviance_ignores_the_level_and_sees_the_spread() -> None:
    """A common scale of the predictions changes nothing (the game's uniform factor); a change of spread does, which a
    Gini cannot see. A balanced prediction scores its plain weighted Tweedie deviance.
    """
    rate, years, pred = _pure_premiums(4)
    pred = pred + 1.0  # above the floor at every scale below
    spec = _rescaled(1.5, 1e-6)
    base = score(spec, rate, pred, weight=years)
    for factor in (1e-3, 0.37, 12.0, 1e6):
        assert score(spec, rate, factor * pred, weight=years) == pytest.approx(base, rel=1e-10)
    steeper = score(spec, rate, pred**2, weight=years)
    gini = _spec("normalized_weighted_gini", "regression", inputs={"weight": "w"})
    assert score(gini, rate, pred**2, weight=years) == pytest.approx(score(gini, rate, pred, weight=years), rel=1e-12)
    assert abs(steeper - base) > 1e-3 * base
    balanced = pred * (years * rate).sum() / (years * pred).sum()
    plain = Metric.source(
        "mean_tweedie_deviance", params={"power": 1.5, "min_prediction": 1e-6}, inputs={"weight": "w"}
    )
    assert base == pytest.approx(score(plain, rate, balanced, weight=years), rel=1e-12)


def test_rescaled_mean_tweedie_deviance_edges_and_declaration() -> None:
    """NaN without a loss to share, a bad or missing weight raises, both params required, a row weight."""
    spec = _rescaled()
    assert np.isnan(score(spec, [0.0, 0.0], [1.0, 2.0], weight=[1.0, 1.0]))  # no loss: no total to share
    assert np.isnan(score(spec, [0.0, 5.0], [1.0, 2.0], weight=[1.0, 0.0]))  # the loss on a row of weight 0
    with pytest.raises(ValueError, match="weight"):
        score(spec, [0.0, 2.0], [1.0, 1.0], weight=[-1.0, 1.0])
    with pytest.raises(ValueError, match=r"needs the input\(s\) \['weight'\]"):
        score(spec, [0.0, 2.0], [1.0, 1.0])
    with pytest.raises(ValueError, match="missing param"):
        Metric.source("rescaled_mean_tweedie_deviance", params={"power": 1.5}, inputs={"weight": "w"})
    with pytest.raises(ValueError, match="power"):
        Metric.source("rescaled_mean_tweedie_deviance", params={"power": 0.5, "min_prediction": 1.0})
    assert row_weight_column(spec) == "w"


def test_rescaled_mean_tweedie_deviance_is_fast_on_one_million_rows() -> None:
    """Timed on 1M rows (0.03 s on 2026-11-08)."""
    import time  # noqa: PLC0415

    rate, years, pred = _pure_premiums(0, n=1_000_000)
    spec = _rescaled()
    start = time.perf_counter()
    score(spec, rate, pred, weight=years)
    elapsed = time.perf_counter() - start
    print(f"rescaled_mean_tweedie_deviance on 1M rows: {elapsed:.3f} s")
    assert elapsed < 5


# --- weighted_pearsonr ---------------------------------------------------------------------------------------------


def weighted_correlation(a, b, weights):
    """The weighted correlation of the G-Research Crypto Forecasting competition, as posted in its discussions and
    copied in public notebooks (it is not in the organisers' tutorial notebook, checked 2026-10-21).
    """
    w = np.ravel(weights)
    a = np.ravel(a)
    b = np.ravel(b)

    sum_w = np.sum(w)
    mean_a = np.sum(a * w) / sum_w
    mean_b = np.sum(b * w) / sum_w
    var_a = np.sum(w * np.square(a - mean_a)) / sum_w
    var_b = np.sum(w * np.square(b - mean_b)) / sum_w

    cov = np.sum(a * b * w) / np.sum(w) - mean_a * mean_b
    return cov / np.sqrt(var_a * var_b)


ASSET_WEIGHTS = {"Bitcoin": 6.78, "Ethereum": 5.89, "Cardano": 4.41, "Dogecoin": 3.56, "IOTA": 1.1}


def test_weighted_pearsonr_equals_the_reference_by_weights_and_by_key() -> None:
    rng = np.random.default_rng(5)
    n = 20000
    assets = rng.choice(list(ASSET_WEIGHTS), n)
    w = np.array([ASSET_WEIGHTS[a] for a in assets])
    y = rng.normal(scale=0.01, size=n)
    p = 0.1 * y + rng.normal(scale=0.01, size=n)
    reference = weighted_correlation(p, y, w)
    by_weight = score(_spec("weighted_pearsonr", "regression", inputs={"weight": "w"}), y, p, weight=w)
    assert by_weight == pytest.approx(reference, rel=1e-9)
    assert by_weight == pytest.approx(np.cov(y, p, aweights=w)[0, 1] / np.sqrt(
        np.cov(y, aweights=w) * np.cov(p, aweights=w)), rel=1e-9)  # fmt: skip
    keyed = _spec("weighted_pearsonr", "regression", params={"weights": ASSET_WEIGHTS}, inputs={"weight": "Asset"})
    assert score(keyed, y, p, weight=assets) == pytest.approx(reference, rel=1e-9)
    # equal weights: the plain Pearson correlation
    assert score(keyed, y, p, weight=np.full(n, "IOTA")) == pytest.approx(stats.pearsonr(y, p).statistic, rel=1e-9)
    with pytest.raises(ValueError, match="no entry"):
        score(keyed, y[:3], p[:3], weight=np.array(["Bitcoin", "Solana", "IOTA"]))


def test_weighted_pearsonr_by_hand() -> None:
    # weight 2 on (0, 0) duplicates it: the correlation of (0, 0), (0, 0), (1, 1), (2, 1)
    value = score(_spec("weighted_pearsonr", "regression"), [0, 1, 2], [0, 1, 1], weight=[2, 1, 1])
    assert value == pytest.approx(stats.pearsonr([0, 0, 1, 2], [0, 0, 1, 1]).statistic)


# --- mean_group_pearsonr -------------------------------------------------------------------------------------------
# numerai_tools.scoring 0.7.2 (https://github.com/numerai/numerai-tools, MIT License, Copyright (c) 2023 Numerai):
# the functions numerai_corr calls, without the index checks and the top_bottom filter it does not use by default.


def _nt_rank(s: pd.Series, method: str = "average") -> pd.Series:
    return (s.rank(method=method) - 0.5) / s.count()


def _nt_gaussian(df: pd.DataFrame) -> pd.DataFrame:
    return df.apply(stats.norm.ppf)


def _nt_power(df: pd.DataFrame, p: float) -> pd.DataFrame:
    return np.sign(df) * np.abs(df) ** p


def _nt_numerai_corr(predictions: pd.DataFrame, targets: pd.Series) -> pd.Series:
    targets = targets - targets.mean()
    predictions = _nt_power(_nt_gaussian(predictions.apply(_nt_rank)), 1.5)
    targets = _nt_power(targets.to_frame(), 1.5)[targets.name]
    return predictions.apply(lambda sub: targets.corr(sub, method="pearson"))


def _numerai_frame(seed: int, n_eras: int = 30, per_era: int = 400) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    n = n_eras * per_era
    target = rng.choice([0.0, 0.25, 0.5, 0.75, 1.0], n, p=[0.05, 0.2, 0.5, 0.2, 0.05])
    pred = 0.05 * target + rng.normal(scale=0.1, size=n)
    pred[: n // 10] = np.round(pred[: n // 10], 1)  # some ties
    frame = pd.DataFrame({"era": np.repeat(np.arange(n_eras), per_era), "target": target, "prediction": pred})
    return frame.sample(frac=1, random_state=seed).reset_index(drop=True)  # shuffled rows, as shipped


def _per_era_mean(frame: pd.DataFrame, corr) -> float:
    return float(frame.groupby("era")[["target", "prediction"]].apply(corr).mean())


@pytest.mark.parametrize("method", ["pearson", "numerai_corr"])
def test_mean_group_pearsonr_scores_a_constant_prediction_0(method: str) -> None:
    """A group with a varying target and constant predictions scores 0 (also a float constant like 0.3, whose
    centring leaves rounding noise); a group with a constant target stays out; a declined group counts as 0.
    """
    rng = np.random.default_rng(0)
    group = np.repeat(np.arange(6), 50)
    target = rng.normal(size=group.size)
    target[group == 5] = 1.0  # constant target: left out
    spec = _spec("mean_group_pearsonr", "regression", params={"method": method}, inputs={"group": "g"})
    for constant in (0.3, 0.5, 0.25, 0.1 + 0.2):
        assert score(spec, target, np.full(group.size, constant), group=group) == 0.0
    noisy = target + rng.normal(scale=0.5, size=group.size)
    full = score(spec, target, noisy, group=group)
    half = noisy.copy()
    half[group < 3] = 0.3  # abstain on three of the five scored groups
    assert full > score(spec, target, half, group=group) > 0
    assert np.isnan(score(spec, np.ones(10), np.arange(10.0), group=np.zeros(10)))


@pytest.mark.parametrize("seed", [0, 1])
def test_mean_group_pearsonr_numerai_corr_equals_numerai_tools(seed: int) -> None:
    frame = _numerai_frame(seed)

    def vendored(d: pd.DataFrame) -> float:
        d = d.sort_index()
        return _nt_numerai_corr(d[["prediction"]], d["target"]).iloc[0]

    reference = _per_era_mean(frame, vendored)
    spec = _spec("mean_group_pearsonr", "regression", params={"method": "numerai_corr"}, inputs={"group": "era"})
    value = score(spec, frame["target"], frame["prediction"], group=frame["era"])
    assert value == pytest.approx(reference, rel=1e-9)

    scoring = pytest.importorskip("numerai_tools.scoring")

    def official(d: pd.DataFrame) -> float:
        d = d.sort_index()
        return scoring.numerai_corr(d[["prediction"]], d["target"]).iloc[0]

    assert value == pytest.approx(_per_era_mean(frame, official), rel=1e-9)


def test_mean_group_pearsonr_plain_equals_per_group_scipy_and_by_hand() -> None:
    frame = _numerai_frame(3)
    reference = _per_era_mean(frame, lambda d: stats.pearsonr(d["target"], d["prediction"]).statistic)
    spec = _spec("mean_group_pearsonr", "regression", inputs={"group": "era"})
    assert score(spec, frame["target"], frame["prediction"], group=frame["era"]) == pytest.approx(reference, rel=1e-9)
    # by hand: group a perfectly correlated (1), group b anti-correlated (-1), group c constant (left out) -> 0
    value = score(spec, [1, 2, 3, 1, 2, 3, 5, 5], [1, 2, 3, 3, 2, 1, 4, 7], group=list("aaabbbcc"))
    assert value == pytest.approx(0.0)
    with pytest.raises(ValueError, match="method"):
        Metric.source("mean_group_pearsonr", params={"method": "spearman"})


# --- mean_group_normalized_rmse ------------------------------------------------------------------------------------
# No official code: the reference is scikit-learn's RMSE and numpy's population standard deviation, group by group.


def _normalized_rmse_reference(y_true, y_pred, group) -> float:
    frame = pd.DataFrame({"y": y_true, "p": y_pred, "g": group})
    ratios = [
        np.sqrt(mean_squared_error(d["y"], d["p"])) / np.std(d["y"])
        for _, d in frame.groupby("g")
        if np.std(d["y"]) > 0
    ]
    return float(np.mean(ratios))


@pytest.mark.parametrize("seed", [0, 1, 2])
def test_mean_group_normalized_rmse_equals_per_group_sklearn(seed: int) -> None:
    rng = np.random.default_rng(seed)
    n = 20_000
    group = rng.integers(0, 11, n)
    scale = np.exp(rng.uniform(0, 9, 11))[group]  # groups on scales four orders of magnitude apart, as species counts
    y = rng.poisson(0.5, n) * scale * rng.lognormal(size=n)
    y_pred = np.clip(y + rng.normal(scale=scale), 0, None)
    spec = _spec("mean_group_normalized_rmse", "regression", inputs={"group": "taxon"})
    value = score(spec, y, y_pred, group=group)
    assert value == pytest.approx(_normalized_rmse_reference(y, y_pred, group), rel=1e-9)


def test_mean_group_normalized_rmse_by_hand() -> None:
    spec = _spec("mean_group_normalized_rmse", "regression", inputs={"group": "taxon"})
    # a: y 0, 2 (sd 1), errors 1, 1 -> 1; b: y 0, 200 (sd 100), errors 0, 0 -> 0; c: constant, left out -> mean 0.5
    value = score(spec, [0, 2, 0, 200, 5, 5], [1, 1, 0, 200, 4, 9], group=list("aabbcc"))
    assert value == pytest.approx(0.5)
    # the scale of a group does not change its vote: group b multiplied by 1000 scores the same
    assert score(spec, [0, 2, 0, 200_000], [1, 1, 0, 200_000], group=list("aabb")) == pytest.approx(0.5)


def test_mean_group_normalized_rmse_is_fast_on_one_million_rows() -> None:
    import time  # noqa: PLC0415

    rng = np.random.default_rng(0)
    n = 1_000_000
    y = rng.lognormal(size=n)
    spec = _spec("mean_group_normalized_rmse", "regression", inputs={"group": "taxon"})
    start = time.perf_counter()
    score(spec, y, y + rng.normal(size=n), group=rng.integers(0, 1000, n))
    elapsed = time.perf_counter() - start
    print(f"mean_group_normalized_rmse on 1M rows, 1000 groups: {elapsed:.3f} s")
    assert elapsed < 5


# --- hierarchical_balanced_accuracy --------------------------------------------------------------------------------


def _hierarchical_reference(y_true, y_pred, group) -> float:
    per_class: dict = {}
    for cls in sorted(set(y_true)):
        accuracies = []
        for g in sorted(set(group[y_true == cls])):
            rows = (y_true == cls) & (group == g)
            accuracies.append(np.mean(y_pred[rows] == y_true[rows]))
        per_class[cls] = np.mean(accuracies)
    return float(np.mean(list(per_class.values())))


def test_hierarchical_balanced_accuracy_equals_the_loop_and_by_hand() -> None:
    rng = np.random.default_rng(6)
    strains = np.arange(200)
    species_of = rng.choice(list("ABCDEFGHIJ"), 200)
    group = rng.choice(strains, 3000)
    y = species_of[group]
    pred = np.where(rng.uniform(size=3000) < 0.7, y, rng.choice(list("ABCDEFGHIJ"), 3000))
    spec = _spec("hierarchical_balanced_accuracy", "multiclass_classification", inputs={"group": "Strain"})
    assert score(spec, y, pred, group=group) == pytest.approx(_hierarchical_reference(y, pred, group), rel=1e-12)
    # by hand: species A has strains s1 (2 of 2 right) and s2 (0 of 1 right) -> 0.5; species B, s3 (1 of 4) -> 0.25
    y = np.array(["A", "A", "A", "B", "B", "B", "B"])
    pred = np.array(["A", "A", "B", "B", "A", "A", "A"])
    group = np.array(["s1", "s1", "s2", "s3", "s3", "s3", "s3"])
    assert score(spec, y, pred, group=group) == pytest.approx((0.5 + 0.25) / 2)


# --- gini_stability (Home Credit 2024) -----------------------------------------------------------------------------


def gini_stability(base, w_fallingrate=88.0, w_resstd=-0.5):
    """The hosts' metric, Home Credit 2024 Starter Notebook (https://www.kaggle.com/code/jetakow/
    home-credit-2024-starter-notebook), as on the competition's evaluation page.
    """
    gini_in_time = (
        base.loc[:, ["WEEK_NUM", "target", "score"]]
        .sort_values("WEEK_NUM")
        .groupby("WEEK_NUM")[["target", "score"]]
        .apply(lambda x: 2 * roc_auc_score(x["target"], x["score"]) - 1)
        .tolist()
    )

    x = np.arange(len(gini_in_time))
    y = gini_in_time
    a, b = np.polyfit(x, y, 1)
    y_hat = a * x + b
    residuals = y - y_hat
    res_std = np.std(residuals)
    avg_gini = np.mean(gini_in_time)
    return avg_gini + w_fallingrate * min(0, a) + w_resstd * res_std


@pytest.mark.parametrize("seed", [0, 1, 2])
def test_gini_stability_equals_the_official_metric(seed: int) -> None:
    rng = np.random.default_rng(seed)
    n = 40000
    week = rng.choice(np.arange(10, 30, 2), n)  # gaps in the week numbers: the fit runs over the week index
    y = (rng.uniform(size=n) < 0.05).astype(int)
    drift = 1 - (week - 10) / 40  # the signal fades over the weeks: a negative slope
    s = rng.uniform(size=n) + drift * y * rng.uniform(size=n)
    s[: n // 5] = np.round(s[: n // 5], 2)  # ties
    official = gini_stability(pd.DataFrame({"WEEK_NUM": week, "target": y, "score": s}))
    spec = _spec("gini_stability", "binary_classification", inputs={"order": "WEEK_NUM"})
    assert score(spec, y, s, order=week) == pytest.approx(official, rel=1e-9)


def test_gini_stability_by_hand() -> None:
    # two weeks, each with a perfect ranking: gini 1 and 1, slope 0, residuals 0 -> 1
    y = np.array([0, 1, 0, 1])
    s = np.array([0.1, 0.9, 0.2, 0.8])
    spec = _spec("gini_stability", "binary_classification", inputs={"order": "WEEK_NUM"})
    assert score(spec, y, s, order=[0, 0, 1, 1]) == pytest.approx(1.0)
    # week 0 perfect (gini 1), week 1 inverted (gini -1): slope -2, line through both -> 0 + 88 * -2 - 0 = -176
    s = np.array([0.1, 0.9, 0.8, 0.2])
    assert score(spec, y, s, order=[0, 0, 1, 1]) == pytest.approx(-176.0)


# --- par_k ---------------------------------------------------------------------------------------------------------


def _par_k_reference(runtime, predicted, instance, cutoff, k) -> float:
    """ASlib's PAR10 of a selector (Bischl et al. 2016): per instance run the algorithm predicted fastest; a run
    stopped at the cutoff counts k * cutoff (llama::parscores).
    """
    scores = []
    for inst in pd.unique(instance):
        rows = np.flatnonzero(instance == inst)
        chosen = rows[np.argmin(predicted[rows])]
        scores.append(k * cutoff if runtime[chosen] >= cutoff else runtime[chosen])
    return float(np.mean(scores))


def test_par_k_equals_the_reference_on_log_runtimes() -> None:
    rng = np.random.default_rng(7)
    n_inst, n_algo = 300, 10
    runtime = np.exp(rng.uniform(np.log(0.1), np.log(9000), n_inst * n_algo)).clip(None, 5000)  # 5000: a timeout
    instance = np.repeat(np.arange(n_inst), n_algo)
    log_target = np.log(runtime)  # as sat11 stores it; exp(log(5000)) is 5000.000000000004
    predicted = log_target + rng.normal(scale=1.0, size=len(runtime))
    shuffle = rng.permutation(len(runtime))  # shuffled rows, as shipped
    spec = _spec("par_k", "regression", params={"cutoff": 5000, "k": 10}, inputs={"group": "i"}, target_transform="log")
    value = score(spec, log_target[shuffle], predicted[shuffle], group=instance[shuffle])
    assert value == pytest.approx(_par_k_reference(runtime, predicted, instance, 5000, 10), rel=1e-12)


def test_par_k_by_hand() -> None:
    # instance a: predicted fastest is the 3 s run; instance b: the predicted fastest timed out -> 10 * 100
    spec = _spec("par_k", "regression", params={"cutoff": 100}, inputs={"group": "i"})
    value = score(spec, [3, 50, 100, 20], [1, 2, 0.5, 0.9], group=["a", "a", "b", "b"])
    assert value == pytest.approx((3 + 1000) / 2)
    with pytest.raises(ValueError, match="missing param"):
        Metric.source("par_k")
    with pytest.raises(ValueError, match="takes the params"):  # the spec-level target_transform is the one way
        Metric.source("par_k", params={"cutoff": 100, "target_transform": "log"})


# --- mean_group_top_k_overlap (Buza's Hits@10 per day) ---------------------------------------------------------------
# Buza 2014, Feedback Prediction for Blogs, Sec. 5.1: "For each day of the test data we consider 10 blog pages that
# were predicted to have the largest number of feedbacks. We count how many out of these pages are among the 10 pages
# that received the largest number of feedbacks in the reality. We call this evaluation measure Hits@10 and we average
# Hits@10 for all the days of the test data." No code is published; the reference is that text, as a loop.


def buza_hits_at_k(y_true, y_pred, day, k=10, true_order=None, pred_order=None) -> float:
    """Hits@k averaged over the days, ties broken by the given row orders (default: the row position)."""
    n = len(y_true)
    true_order = np.arange(n) if true_order is None else true_order
    pred_order = np.arange(n) if pred_order is None else pred_order
    hits = []
    for d in pd.unique(day):
        rows = np.flatnonzero(day == d)
        top_pred = rows[np.lexsort((pred_order[rows], -y_pred[rows]))[:k]]
        top_true = rows[np.lexsort((true_order[rows], -y_true[rows]))[:k]]
        hits.append(len(set(top_pred) & set(top_true)))
    return float(np.mean(hits))


def _blog_days(seed: int, n_days: int = 20, per_day: int = 120):
    rng = np.random.default_rng(seed)
    day = np.repeat(np.arange(n_days), per_day)
    comments = rng.negative_binomial(0.3, 0.05, len(day)).astype(float)  # many zeros, a long tail, ties
    noise = rng.normal(scale=1.0, size=len(day))
    return comments, day, noise


@pytest.mark.parametrize("seed", [0, 1, 2])
def test_mean_group_top_k_overlap_equals_buza_hits_at_10_without_ties(seed: int) -> None:
    """Without ties the metric times k is Buza's Hits@10, the strict count; rows shuffled, days in any order."""
    comments, day, noise = _blog_days(seed)
    y = comments + np.random.default_rng(seed + 10).uniform(0, 1e-3, len(comments))  # break the ties in the truth
    pred = np.log1p(y) + noise
    shuffle = np.random.default_rng(seed).permutation(len(y))
    spec = _spec("mean_group_top_k_overlap", "regression", params={"k": 10}, inputs={"group": "day"})
    value = score(spec, y[shuffle], pred[shuffle], group=day[shuffle])
    assert 10 * value == pytest.approx(buza_hits_at_k(y, pred, day), rel=1e-12)


def test_mean_group_top_k_overlap_takes_the_expected_share_over_tie_breaks() -> None:
    """With ties at either cut-off the score is the mean of Buza's count over every way to break them (enumerated)."""
    rng = np.random.default_rng(3)
    y = rng.integers(0, 3, 10).astype(float)  # heavy ties in the truth
    pred = rng.integers(0, 4, 10).astype(float)  # and in the predictions
    day = np.repeat([0, 1], 5)
    k = 2
    exact = []
    for perm_day0 in itertools.permutations(range(5)):
        for perm_pred in itertools.permutations(range(5)):
            order_true = np.concatenate([perm_day0, perm_day0])  # the same tie-breaks on both days: still uniform
            order_pred = np.concatenate([perm_pred, perm_pred])
            exact.append(buza_hits_at_k(y, pred, day, k, order_true, order_pred))
    spec = _spec("mean_group_top_k_overlap", "regression", params={"k": k}, inputs={"group": "d"})
    assert k * score(spec, y, pred, group=day) == pytest.approx(np.mean(exact), rel=1e-12)
    # the strict loop by row position, and counting every tie at the cut-off as a hit, bracket it (6.52 and 6.68)
    comments, day20, noise = _blog_days(4)
    pred20 = np.round(np.log1p(comments) + noise)  # tied predictions too
    spec10 = _spec("mean_group_top_k_overlap", "regression", params={"k": 10}, inputs={"group": "d"})
    expected = 10 * score(spec10, comments, pred20, group=day20)
    strict = [
        buza_hits_at_k(comments, pred20, day20, 10, r.permutation(len(day20)), r.permutation(len(day20)))
        for r in (np.random.default_rng(i) for i in range(400))
    ]
    assert np.mean(strict) == pytest.approx(expected, abs=0.05)


def test_mean_group_top_k_overlap_by_hand() -> None:
    """Small days counted by hand: a plain overlap, a tie at the cut-off, a day smaller than k, a constant."""
    spec = _spec("mean_group_top_k_overlap", "regression", params={"k": 2}, inputs={"group": "d"})
    # day a: true top 2 = rows 0, 1; predicted top 2 = rows 0, 2 -> 1 of 2. day b: the same top 2 -> 2 of 2.
    y = [9, 8, 1, 0, 5, 7, 6, 0]
    p = [3, 1, 2, 0, 0.5, 0.9, 0.8, 0.1]
    d = ["a"] * 4 + ["b"] * 4
    assert score(spec, y, p, group=d) == pytest.approx((0.5 + 1.0) / 2)
    # a tie at the cut-off: day a's predictions 3, 2, 2, 0 -> row 0 in, rows 1 and 2 each in with probability 1/2
    assert score(spec, y, [3, 2, 2, 0, 0.5, 0.9, 0.8, 0.1], group=d) == pytest.approx(((1 + 0.5) / 2 + 1.0) / 2)
    # a day of k rows or fewer is left out (every model would score 1 there): x's one row does not count; y: true
    # top 7, 5, predicted top 2, 5 -> 1 of 2
    assert score(spec, [1, 5, 2, 7], [0, 1, 2, 0], group=["x", "y", "y", "y"]) == pytest.approx(0.5)
    assert np.isnan(score(spec, [1, 5], [0, 1], group=["x", "y"]))  # no day larger than k
    # a constant prediction finds k / n of the top on average
    assert score(spec, [4, 3, 2, 1], [0, 0, 0, 0], group=[0, 0, 0, 0]) == pytest.approx(0.5)
    with pytest.raises(ValueError, match="missing param"):
        Metric.source("mean_group_top_k_overlap")
    for bad in (0, 2.5, True):
        with pytest.raises(ValueError, match="k is a positive integer"):
            Metric.source("mean_group_top_k_overlap", params={"k": bad})


# --- normalized_early_detection_utility (PhysioNet/CinC 2019) ------------------------------------------------------
# https://github.com/physionetchallenges/evaluation-2019/blob/master/evaluate_sepsis_score.py (master, fetched
# 2026-10-21): compute_prediction_utility verbatim, and the utility part of evaluate_sepsis_score without file I/O.


def compute_prediction_utility(labels, predictions, dt_early=-12, dt_optimal=-6, dt_late=3.0, max_u_tp=1,  # noqa: C901, PLR0912
                               min_u_fn=-2, u_fp=-0.05, u_tn=0, check_errors=True):  # noqa: FBT002  # fmt: skip
    """``compute_prediction_utility`` of the official evaluate_sepsis_score.py (verbatim)."""
    # Check inputs for errors.
    if check_errors:
        if len(predictions) != len(labels):
            raise Exception("Numbers of predictions and labels must be the same.")
        for label in labels:
            if label not in (0, 1):
                raise Exception("Labels must satisfy label == 0 or label == 1.")
        for prediction in predictions:
            if prediction not in (0, 1):
                raise Exception("Predictions must satisfy prediction == 0 or prediction == 1.")
        if dt_early >= dt_optimal:
            raise Exception("The earliest beneficial time for predictions must be before the optimal time.")
        if dt_optimal >= dt_late:
            raise Exception("The optimal time for predictions must be before the latest beneficial time.")

    # Does the patient eventually have sepsis?
    if np.any(labels):
        is_septic = True
        t_sepsis = np.argmax(labels) - dt_optimal
    else:
        is_septic = False
        t_sepsis = float("inf")

    n = len(labels)

    # Define slopes and intercept points for utility functions of the form
    # u = m * t + b.
    m_1 = float(max_u_tp) / float(dt_optimal - dt_early)
    b_1 = -m_1 * dt_early
    m_2 = float(-max_u_tp) / float(dt_late - dt_optimal)
    b_2 = -m_2 * dt_late
    m_3 = float(min_u_fn) / float(dt_late - dt_optimal)
    b_3 = -m_3 * dt_optimal

    # Compare predicted and true conditions.
    u = np.zeros(n)
    for t in range(n):
        if t <= t_sepsis + dt_late:
            # TP
            if is_septic and predictions[t]:
                if t <= t_sepsis + dt_optimal:
                    u[t] = max(m_1 * (t - t_sepsis) + b_1, u_fp)
                elif t <= t_sepsis + dt_late:
                    u[t] = m_2 * (t - t_sepsis) + b_2
            # FP
            elif not is_septic and predictions[t]:
                u[t] = u_fp
            # FN
            elif is_septic and not predictions[t]:
                if t <= t_sepsis + dt_optimal:
                    u[t] = 0
                elif t <= t_sepsis + dt_late:
                    u[t] = m_3 * (t - t_sepsis) + b_3
            # TN
            elif not is_septic and not predictions[t]:
                u[t] = u_tn

    # Find total utility for patient.
    return np.sum(u)


def official_normalized_utility(cohort_labels, cohort_predictions) -> float:
    """The utility part of ``evaluate_sepsis_score`` on in-memory patients (lists of per-hour arrays)."""
    dt_early, dt_optimal, dt_late = -12, -6, 3
    max_u_tp, min_u_fn, u_fp, u_tn = 1, -2, -0.05, 0
    num_files = len(cohort_labels)
    observed_utilities = np.zeros(num_files)
    best_utilities = np.zeros(num_files)
    inaction_utilities = np.zeros(num_files)
    for k in range(num_files):
        labels = cohort_labels[k]
        num_rows = len(labels)
        observed_predictions = cohort_predictions[k]
        best_predictions = np.zeros(num_rows)
        inaction_predictions = np.zeros(num_rows)
        if np.any(labels):
            t_sepsis = np.argmax(labels) - dt_optimal
            best_predictions[max(0, t_sepsis + dt_early) : min(t_sepsis + dt_late + 1, num_rows)] = 1
        args = (dt_early, dt_optimal, dt_late, max_u_tp, min_u_fn, u_fp, u_tn)
        observed_utilities[k] = compute_prediction_utility(labels, observed_predictions, *args)
        best_utilities[k] = compute_prediction_utility(labels, best_predictions, *args)
        inaction_utilities[k] = compute_prediction_utility(labels, inaction_predictions, *args)
    unnormalized_observed_utility = np.sum(observed_utilities)
    unnormalized_best_utility = np.sum(best_utilities)
    unnormalized_inaction_utility = np.sum(inaction_utilities)
    return (unnormalized_observed_utility - unnormalized_inaction_utility) / (
        unnormalized_best_utility - unnormalized_inaction_utility
    )


def _patients(seed: int, n_patients: int = 400):
    """Random ICU stays: hours 0..n-1, a third septic with SepsisLabel = 1 from 6 h before onset to the end."""
    rng = np.random.default_rng(seed)
    labels, probas = [], []
    for _ in range(n_patients):
        n = int(rng.integers(5, 80))
        y = np.zeros(n, dtype=int)
        if rng.uniform() < 0.35:
            y[int(rng.integers(0, n)) :] = 1
        labels.append(y)
        probas.append(np.clip(0.3 * y + rng.uniform(size=n) * 0.8, 0, 1))
    return labels, probas


@pytest.mark.parametrize("seed", [0, 1, 2])
def test_normalized_early_detection_utility_equals_the_official_code(seed: int) -> None:
    labels, probas = _patients(seed)
    predictions = [(p >= 0.5).astype(int) for p in probas]
    official = official_normalized_utility(labels, predictions)
    patient = np.concatenate([np.full(len(y), i) for i, y in enumerate(labels)])
    hour = np.concatenate([np.arange(len(y)) for y in labels])
    y, p, pred = np.concatenate(labels), np.concatenate(probas), np.concatenate(predictions)
    shuffle = np.random.default_rng(seed).permutation(len(y))  # shuffled rows, also within a patient
    inputs = {"group": "Patient_ID", "order": "Hour"}
    spec = _spec("normalized_early_detection_utility", "binary_classification", inputs=inputs)
    value = score(spec, y[shuffle], pred[shuffle], group=patient[shuffle], order=hour[shuffle])
    assert value == pytest.approx(official, rel=1e-10, abs=1e-12)
    proba_spec = _spec(
        "normalized_early_detection_utility",
        "binary_classification",
        inputs=inputs,
        params={"prediction": "proba", "threshold": 0.5},
    )
    assert proba_spec.prediction == "proba"
    value = score(proba_spec, y[shuffle], p[shuffle], group=patient[shuffle], order=hour[shuffle])
    assert value == pytest.approx(official, rel=1e-10, abs=1e-12)


def test_normalized_early_detection_utility_by_hand() -> None:
    spec = _spec("normalized_early_detection_utility", "binary_classification", inputs={"group": "p", "order": "h"})
    # one septic patient, 20 hours, SepsisLabel from hour 10: t_sepsis = 16; the best alarms hours 4..19
    y = np.r_[np.zeros(10, int), np.ones(10, int)]
    hours, patient = np.arange(20), np.zeros(20)
    best = (hours >= 4).astype(int)
    assert score(spec, y, best, group=patient, order=hours) == pytest.approx(1.0)
    assert score(spec, y, np.zeros(20, int), group=patient, order=hours) == pytest.approx(0.0)
    # by hand: U_none = sum of the FN utilities -2/9 dt - 4/3 over dt = -5..3 = 2 - 12 = -10; U_best = TP utilities
    # max(dt/6 + 2, -0.05) over dt = -12..-6 (3.5) plus -dt/9 + 1/3 over dt = -5..3 (4) = 7.5. One alarm at hour 16
    # (dt = 0) turns -4/3 into 1/3: U = -10 + 5/3 -> (5/3) / 17.5
    one = (hours == 16).astype(int)
    assert score(spec, y, one, group=patient, order=hours) == pytest.approx((5 / 3) / 17.5)
    assert official_normalized_utility([y], [one]) == pytest.approx((5 / 3) / 17.5)
    # a non-septic patient's false alarms cost 0.05 per hour
    y2 = np.r_[y, np.zeros(5, int)]
    pred = np.r_[best, np.ones(5, int)]
    value = score(spec, y2, pred, group=np.r_[patient, np.ones(5)], order=np.r_[hours, np.arange(5)])
    assert value == pytest.approx((7.5 - 5 * 0.05 + 10) / 17.5)


# --- net_revenue_at_cost -------------------------------------------------------------------------------------------


def kdd98_net_revenue(donation, predicted, cost=0.68) -> float:
    """The KDD Cup 1998 evaluation rule, transcribed from cup98doc.txt ("Evaluation rules": "Sum (the actual donation
    amount - $0.68) over all records for which the expected revenue (or predicted value of the donation) is over
    $0.68"), https://kdd.ics.uci.edu/databases/kddcup98/epsilon_mirror/cup98doc.txt. The cup published no code.
    """
    total = 0.0
    for d, p in zip(donation, predicted, strict=True):
        if p > cost:
            total += d - cost
    return total


@pytest.mark.parametrize("seed", [0, 1, 2])
def test_net_revenue_at_cost_equals_the_cup_rule_per_row(seed: int) -> None:
    rng = np.random.default_rng(seed)
    n = 2000 + 500 * seed
    gave = rng.random(n) < 0.05
    y = np.where(gave, rng.gamma(2.0, 8.0, n), 0.0)  # zero-inflated gift amounts, as in the cup's data
    p = np.round(rng.gamma(0.5, 1.5, n), 2)  # rounded: many predictions tie, some at exactly the cost
    p[: n // 10] = 0.68
    spec = _spec("net_revenue_at_cost", "regression", params={"cost": 0.68})
    assert score(spec, y, p) == pytest.approx(kdd98_net_revenue(y, p) / n, rel=1e-12, abs=1e-15)
    shuffled = rng.permutation(n)
    assert score(spec, y[shuffled], p[shuffled]) == pytest.approx(score(spec, y, p), rel=1e-12)


def test_net_revenue_at_cost_by_hand() -> None:
    spec = _spec("net_revenue_at_cost", "regression", params={"cost": 0.68})
    # mailed: rows 1 (p 5 > 0.68, gift 10), 2 (p 1, gift 0) and 4 (p 0.69, gift 20); row 3 (p 0.68) is not over the
    # cost and row 0 (p 0) is not mailed: (10 - 0.68) + (0 - 0.68) + (20 - 0.68) = 27.96, over 5 rows = 5.592
    assert score(spec, [0, 10, 0, 50, 20], [0, 5, 1, 0.68, 0.69]) == pytest.approx(5.592, rel=1e-12)
    # mailing nobody scores 0, mailing everybody the mean gift minus the cost
    assert score(spec, [0, 10, 0, 50, 20], [0, 0, 0, 0, 0]) == 0.0
    assert score(spec, [0, 10, 0, 50, 20], [9, 9, 9, 9, 9]) == pytest.approx(16 - 0.68, rel=1e-12)


def test_net_revenue_at_cost_refuses_bad_params() -> None:
    for params in ({}, {"cost": -1}, {"cost": float("nan")}, {"cost": "0.68"}, {"cost": True}):
        with pytest.raises(ValueError, match="cost"):
            Metric.source("net_revenue_at_cost", reference="https://example.org", params=params)


def test_net_revenue_at_cost_is_fast_on_one_million_rows() -> None:
    import time  # noqa: PLC0415

    rng = np.random.default_rng(0)
    n = 1_000_000
    y = np.where(rng.random(n) < 0.05, rng.gamma(2.0, 8.0, n), 0.0)
    p = rng.gamma(0.5, 1.5, n)
    spec = _spec("net_revenue_at_cost", "regression", params={"cost": 0.68})
    start = time.perf_counter()
    score(spec, y, p)
    assert time.perf_counter() - start < 2.0


# --- the registry and the checks -----------------------------------------------------------------------------------


def test_every_custom_metric_documents_itself() -> None:
    assert (
        sorted(
            [
                "average_precision_at_k",
                "cost_matrix",
                "gini_stability",
                "gini_top_capture",
                "hierarchical_balanced_accuracy",
                "mean_group_normalized_rmse",
                "mean_group_pearsonr",
                "mean_group_top_k_overlap",
                "net_revenue_at_cost",
                "normalized_early_detection_utility",
                "normalized_gini",
                "normalized_weighted_gini",
                "ordered_lorenz_gini",
                "par_k",
                "precision_at_k",
                "rescaled_mean_tweedie_deviance",
                "rmspe",
                "weighted_pearsonr",
            ]
        )
        == CUSTOM
    )
    for name in CUSTOM:
        d = METRICS[name]
        assert d.definition, name
        assert d.reference, name
        assert d.prediction in ("proba", "label", "value"), name


_CHECK_PARAMS = {
    "cost_matrix": {"labels": ["no", "yes"], "matrix": [[0, 1], [5, 0]]},
    "precision_at_k": {"k_fraction": 0.2},
    "average_precision_at_k": {"k_fraction": 0.1},
    "par_k": {"cutoff": 5000},
    "mean_group_top_k_overlap": {"k": 2},
    "rescaled_mean_tweedie_deviance": {"power": 1.5, "min_prediction": 1e-3},
    "net_revenue_at_cost": {"cost": 0.68},
}


@pytest.mark.parametrize("name", CUSTOM)
def test_every_custom_metric_computes_on_a_dummy_prediction(name: str) -> None:
    """What the bundle check's "computes" step does: a random prediction of the spec's kind, inputs by role."""
    d = METRICS[name]
    problem_type = d.problem_types[0]
    rng = np.random.default_rng(0)
    n = 5000
    if problem_type == "regression":
        y = np.log(rng.uniform(1, 5000, n)) if name == "par_k" else rng.normal(size=n) + 3
        if d.prediction_domain == "positive":  # a deviance: an amount >= 0, mostly 0
            y = np.where(rng.uniform(size=n) < 0.1, rng.gamma(2.0, 100.0, n), 0.0)
    else:
        y = rng.choice(["no", "yes"], n, p=[0.8, 0.2])
    inputs = {role: f"col_{role}" for role in d.inputs}
    spec = _spec(name, problem_type, params=_CHECK_PARAMS.get(name, {}), inputs=inputs)
    values = {
        "group": rng.integers(0, 50, n),
        "order": rng.integers(0, 10, n),
        "weight": rng.uniform(1, 7, n),
    }
    y_pred = dummy_prediction(spec.prediction, y, n, seed=1, domain=d.prediction_domain)
    value = score(spec, y, y_pred, **{role: values[role] for role in d.inputs})
    assert np.isfinite(value), name


_BUNDLE_COLUMNS = {"group": "g", "order": "o", "weight": "w"}


@pytest.mark.parametrize("name", CUSTOM)
def test_every_custom_metric_passes_the_bundle_metric_checks(name: str) -> None:
    """The format-2 bundle checks on a toy container: the spec, its scoring columns and the "computes" step."""
    d = METRICS[name]
    problem_type = d.problem_types[0]
    df = make_iid_frame()
    n = len(df)
    if problem_type == "regression":
        df["target"] = np.log(np.linspace(1, 6000, n)) if name == "par_k" else np.linspace(1, 3, n)
    df["g"] = pd.Categorical([f"g{i % 5}" for i in range(n)])
    df["o"] = np.arange(n) % 2
    df["w"] = 1.0 + np.arange(n) % 3
    inputs = {role: _BUNDLE_COLUMNS[role] for role in d.inputs}
    spec = _spec(name, problem_type, params=_CHECK_PARAMS.get(name, {}), inputs=inputs)
    scoring = [
        ScoringColumn(column=column, role=role, used_by=name, description="toy scoring column")
        for role, column in inputs.items()
    ]
    container = make_v2_container(
        df, spec=spec, scoring_columns=scoring, problem_type=problem_type, sample_weight=row_weight_column(spec)
    )
    assert metric_findings(container) == {}
