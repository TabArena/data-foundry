"""The custom metrics of ``data_foundry.v2.metrics`` against their official or reference implementations.

Each official implementation is vendored below, as published (only reformatted, with the I/O around it removed), with
its source. Each metric is also checked on a small case computed by hand. The 1M-row timings are in
``local-data-warehouse/_runs/2026-10-21_metrics/bench.py`` (not part of the test run).
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
from data_foundry.schema import ScoringColumn
from data_foundry.v2.dataset import metric_spec
from data_foundry.v2.metrics import METRICS, Metric, dummy_prediction, score
from scipy import stats
from sklearn.metrics import roc_auc_score

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
    """AP@k of local-data-warehouse/_runs/2026-10-21_crosscut/metric_originals/hunt.py (Avito's scorer is not
    public; the formula of its evaluation page).
    """
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
    spec = _spec(
        "par_k", "regression", params={"cutoff": 5000, "k": 10, "target_transform": "log"}, inputs={"group": "i"}
    )
    value = score(spec, log_target[shuffle], predicted[shuffle], group=instance[shuffle])
    assert value == pytest.approx(_par_k_reference(runtime, predicted, instance, 5000, 10), rel=1e-12)


def test_par_k_by_hand() -> None:
    # instance a: predicted fastest is the 3 s run; instance b: the predicted fastest timed out -> 10 * 100
    spec = _spec("par_k", "regression", params={"cutoff": 100}, inputs={"group": "i"})
    value = score(spec, [3, 50, 100, 20], [1, 2, 0.5, 0.9], group=["a", "a", "b", "b"])
    assert value == pytest.approx((3 + 1000) / 2)
    with pytest.raises(ValueError, match="missing param"):
        Metric.source("par_k")


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
                "mean_group_pearsonr",
                "normalized_early_detection_utility",
                "par_k",
                "precision_at_k",
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
    "par_k": {"cutoff": 5000, "target_transform": "log"},
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
    else:
        y = rng.choice(["no", "yes"], n, p=[0.8, 0.2])
    inputs = {role: f"col_{role}" for role in d.inputs}
    spec = _spec(name, problem_type, params=_CHECK_PARAMS.get(name, {}), inputs=inputs)
    values = {
        "group": rng.integers(0, 50, n),
        "order": rng.integers(0, 10, n),
        "weight": rng.uniform(1, 7, n),
    }
    y_pred = dummy_prediction(spec.prediction, y, n, seed=1)
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
    container = make_v2_container(df, spec=spec, scoring_columns=scoring, problem_type=problem_type)
    assert metric_findings(container) == {}
