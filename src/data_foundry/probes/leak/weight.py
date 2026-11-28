"""Probe 22, the weight proxy: do the features carry a realized weight, such as a time on risk a claim can cut short?"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.metrics import r2_score

from data_foundry.probes import models
from data_foundry.probes.leak.core import say
from data_foundry.probes.leak.fits import TargetFits, spread, stat_text

PROXY_SD = 2.0
"""A feature is flagged when its weight-mediated gain is above this many SDs (over splits x seeds) ..."""


PROXY_SHARE = 0.1
"""... and above this share of the leak reference (what the weight itself gains as a feature)."""


PROXY_TIMING = (
    "The decision is a timing call (LEAK-41): a feature known at the prediction point stays, even when it predicts "
    "the weight through risk selection (USE-6); a column set or cut after it (an earned premium, a realized length) is "
    "no model input, or ships in a form known at the start (annualised to the planned term)."
)


def _inverse_weight(w: np.ndarray, n_classes: int) -> np.ndarray | None:
    """1/weight as a prediction: the values, or for a binary task the probabilities of the second class (1/weight
    scaled into (0, 1]; ``weight_proxy`` also tries the first); None for a multiclass task. A weight of 0 gets twice
    the largest finite inverse.
    """
    inv = 1.0 / np.where(w > 0, w, np.nan)
    finite = np.isfinite(inv)
    inv = np.where(finite, inv, 2 * inv[finite].max() if finite.any() else 1.0)
    if not n_classes:
        return inv
    if n_classes != 2:
        return None
    p = inv / inv.max()
    return np.column_stack([1 - p, p])


def weight_proxy(  # noqa: C901, PLR0912, PLR0913
    df: pd.DataFrame,
    target: str,
    problem_type: str,
    splits: list,
    weight,
    *,
    sample_weight=None,
    feature_cols: list[str] | tuple[str, ...] | None = None,
    group_cols: list[str] | tuple[str, ...] = (),
    metric: dict | None = None,
    weight_name: str = "weight",
    name: str = "dataset",
    n_splits: int = 3,
    max_rows: int = 50_000,
    seeds: tuple[int, ...] = (0, 1, 2),
    top: int = 5,
    n_estimators: int = 200,
    fit_params: dict | None = None,
    n_jobs: int = 8,
    report: bool = True,
) -> dict:
    """Probe 22: do the features carry a realized weight, and how much of their gain goes through it?

    A weight the outcome can cut short (the time insured of a policy cancelled after a claim) is never a feature
    (LEAK-41); this probe asks whether a feature stands in for it. On the first ``n_splits`` splits, each side capped
    at ``max_rows`` random rows (seed 0), and once per seed of ``seeds`` (LightGBM bags rows, so the seeds differ):

    a. a LightGBM regression of the weight on the features, fitted on each train side and scored on its test side:
       R^2, the Spearman correlation and the ``top`` features by gain;
    b. the leak reference: the task's ``metric`` (else R^2 or ROC AUC, weighted) for an honest LightGBM fit on the
       features, trained on the target as it ships with the training weight as each row's weight (an L2 fit, or the
       objective ``fit_params`` sets, such as the weighted Poisson fit of a claims rate), against the same fit with
       the weight added as a feature: what a perfect proxy of the weight gains;
    c. for each of those top features F: its gain (the score with F against the score without it, positive when F
       helps, whatever the metric's direction), once without the weight among the features and once with it. The
       weight-mediated part is the first gain less the second, with its mean and SD over splits x seeds: a feature
       that stands in for the weight loses its gain once the weight is there;
    d. the weight alone: for a Gini metric (``metric["gini"]``), a ranking metric, the score of 1/weight as the
       prediction (for a binary task, as the probability of the class it scores better for); for any other metric,
       which also scores the level, the score of a fit of the target on the weight alone (the fits of b, with the
       weight as the one input). Neither bounds what a proxy gains: b is what the weight adds to the features.

    A feature is flagged when its weight-mediated part is above ``PROXY_SD`` SDs and above ``PROXY_SHARE`` of the leak
    reference. A flag is no verdict: whether the feature stays is a timing call (``PROXY_TIMING``).

    Args:
        df: The rows, with the target and the group columns.
        target: The target column.
        problem_type: ``"regression"``, or a classification type.
        splits: ``(train_idx, test_idx)`` row positions; the first ``n_splits`` are probed.
        weight: The weight under study, one value per row of ``df``: the task's sample weight, or a candidate column
            (never one of the features; a column of ``df`` named ``weight_name`` is left out of them).
        sample_weight: The task's training weight, which every fit is trained with; None trains with ``weight``.
        feature_cols: The model inputs (default: every column but the target and the groups).
        group_cols: Columns that are not features (a group id).
        metric: The task's own metric (see ``curation_probes.weights``), or None for R^2 or ROC AUC.
        weight_name: The weight's name in the report.
        name: The dataset's name in the result.
        n_splits: Splits to probe.
        max_rows: Rows kept (at random) of each train and test side.
        seeds: The LightGBM seeds; each split is fitted once per seed.
        top: The features of the weight model checked in c.
        n_estimators: Trees per LightGBM fit.
        fit_params: LightGBM parameters of the fits of the target (b, c), such as ``{"objective": "poisson"}``; None
            for LightGBM's default (L2, or log loss). LEAK-41 asks for the L2 fit and the weighted actuarial fit.
        n_jobs: Threads per LightGBM model.
        report: Print the lines of ``weight_proxy_lines``.
    """
    regression = problem_type == "regression"
    w = np.asarray(weight, dtype=float)
    if len(w) != len(df) or not np.isfinite(w).all() or (w < 0).any():
        raise ValueError(f"`{weight_name}` needs a finite weight >= 0 on each of the {len(df):,} rows")
    train_w = w if sample_weight is None else np.asarray(sample_weight, dtype=float)
    columns = list(feature_cols) if feature_cols is not None else [c for c in df.columns if c != target]
    columns = [c for c in columns if c not in {weight_name, target, *group_cols}]
    X = df[columns].select_dtypes(exclude=["string", "object", "datetime", "datetimetz"])
    names = list(X.columns)
    X = X.set_axis([f"f{i}" for i in range(X.shape[1])], axis=1)  # LightGBM refuses some characters in names
    fits = TargetFits(
        df[target],
        problem_type,
        train_w,
        metric=metric,
        fit_params=fit_params,
        n_estimators=n_estimators,
        n_jobs=n_jobs,
    )
    evaluate, fit_predict, sign = fits.score, fits.fit_predict, fits.sign
    gini = bool(metric is not None and metric.get("gini"))

    rng = np.random.default_rng(0)
    cap = lambda idx: np.sort(rng.choice(idx, min(len(idx), max_rows), replace=False))
    chosen = [(np.asarray(tr), np.asarray(te)) for tr, te in list(splits)[:n_splits]]
    sampled = any(len(tr) > max_rows or len(te) > max_rows for tr, te in chosen)
    pairs = [(cap(tr), cap(te)) for tr, te in chosen]
    seeds = tuple(seeds)

    # a. and b.: the weight from the features, and the honest fit against the one with the weight as a feature;
    # d.: the weight alone, as 1/weight under a Gini, else as a fit of the target on it
    r2s, rhos, gains, weight_alone, constant = [], [], [], [], []
    honest, with_weight = {}, {}
    for i, (tr, te) in enumerate(pairs):
        x_tr, x_te = X.iloc[tr], X.iloc[te]
        constant.append(evaluate(fits.constant(tr, len(te)), te))
        for seed in seeds:
            if X.shape[1]:
                proxy = models.bagged(regression=True, seed=seed, n_estimators=n_estimators, n_jobs=n_jobs)
                guess = proxy.fit(x_tr, w[tr]).predict(x_te)
                r2s.append(r2_score(w[te], guess))
                rhos.append(pd.Series(w[te]).corr(pd.Series(guess), method="spearman") if np.ptp(guess) else np.nan)
                gain = proxy.booster_.feature_importance(importance_type="gain")
                gains.append(gain / gain.sum() if gain.sum() > 0 else gain)
            honest[i, seed] = evaluate(fit_predict(x_tr, x_te, tr, seed), te)
            plus = fit_predict(x_tr.assign(_weight=w[tr]), x_te.assign(_weight=w[te]), tr, seed)
            with_weight[i, seed] = evaluate(plus, te)
            if not gini:  # a level-sensitive metric: a model of the target on the weight alone
                only = fit_predict(pd.DataFrame({"_weight": w[tr]}), pd.DataFrame({"_weight": w[te]}), tr, seed)
                weight_alone.append(evaluate(only, te))
        inverse = _inverse_weight(w[te], fits.n_classes)
        if inverse is not None and regression:
            inverse = fits.to_shipped(inverse)  # the scorer moves it back: 1/weight on the scale the metric scores
        if gini and inverse is not None:
            # a binary task's class order is arbitrary: 1/weight may point to either class, and the better one counts
            options = [inverse] if not fits.n_classes else [inverse, inverse[:, ::-1]]
            tried = [sign * evaluate(p, te) for p in options]
            weight_alone.append(sign * np.nanmax(tried) if np.isfinite(tried).any() else np.nan)
    mean_gain = pd.Series(np.mean(gains, axis=0) if gains else np.zeros(len(names)), index=names)
    mean_gain = mean_gain.sort_values(ascending=False, kind="stable")
    checked = [f for f in mean_gain.index[:top] if mean_gain[f] > 0]

    # c.: each top feature's gain without the weight among the features and with it
    plain: dict[str, list[float]] = {f: [] for f in checked}
    through: dict[str, list[float]] = {f: [] for f in checked}
    for i, (tr, te) in enumerate(pairs):
        for f in checked:
            col = f"f{names.index(f)}"
            a_tr, a_te = X.iloc[tr].drop(columns=[col]), X.iloc[te].drop(columns=[col])
            for seed in seeds:
                without = evaluate(fit_predict(a_tr, a_te, tr, seed), te)
                plus = fit_predict(a_tr.assign(_weight=w[tr]), a_te.assign(_weight=w[te]), tr, seed)
                plain[f].append(sign * (honest[i, seed] - without))
                through[f].append(sign * (with_weight[i, seed] - evaluate(plus, te)))

    reference = spread(sign * (with_weight[k] - honest[k]) for k in honest)
    features_checked = {}
    for f in checked:
        mediated = spread(np.asarray(plain[f]) - np.asarray(through[f]))
        alone = spread(plain[f])
        noise = alone["mean"] <= 0 or alone["mean"] < PROXY_SD * alone["sd"]  # no share of a gain within noise
        features_checked[f] = {
            "weight_gain_share": float(mean_gain[f]),
            "gain_without_weight": alone,
            "gain_with_weight": spread(through[f]),
            "weight_mediated": mediated,
            "mediated_share": float("nan") if noise else mediated["mean"] / alone["mean"],
            "flag": bool(
                mediated["mean"] > PROXY_SD * mediated["sd"] and mediated["mean"] > PROXY_SHARE * reference["mean"]
            ),
        }
    result = {
        "name": name,
        "weight": weight_name,
        "metric": metric["name"] if metric is not None else ("r2" if regression else "roc_auc"),
        "declared_metric": metric is not None,
        "greater_is_better": sign > 0,
        "metric_row_weight": metric.get("row_weight") if metric is not None else None,
        "trained_with_sample_weight": sample_weight is not None,
        "fit_params": dict(fit_params or {}),
        "objective": (fit_params or {}).get("objective") or ("L2" if regression else "log loss"),
        "rows": len(df),
        "features": X.shape[1],
        "splits": len(pairs),
        "seeds": list(seeds),
        "max_rows": max_rows,
        "subsampled": sampled,
        "weight_model": {
            "r2": spread(r2s),
            "spearman": spread(rhos),
            "top_features": {f: round(float(mean_gain[f]), 4) for f in mean_gain.index[:top]},
        },
        "honest": spread(honest.values()),
        "with_weight": spread(with_weight.values()),
        "leak_reference": reference,
        "constant": spread(constant),
        "weight_alone": {"as": "1/weight" if gini else "fit", **spread(weight_alone)} if weight_alone else None,
        "features_checked": features_checked,
        "flags": [f for f, v in features_checked.items() if v["flag"]],
        "thresholds": {"sd": PROXY_SD, "share_of_leak_reference": PROXY_SHARE},
        "metric_errors": fits.errors,
    }
    if result["flags"]:
        named = ", ".join(f"`{f}`" for f in result["flags"])
        head = (
            f"Part of the gain of {named} goes through `{weight_name}`, above noise ({PROXY_SD:g} SDs over splits x "
            f"seeds, and {PROXY_SHARE:.0%} of the leak reference): it shrinks once the weight is a feature. "
        )
    else:
        head = f"No checked feature's gain goes through `{weight_name}` above noise. "
    result["reading"] = head + PROXY_TIMING
    if report:
        for line in weight_proxy_lines(result):
            say(line)
    return result


def weight_proxy_lines(result: dict) -> list[str]:
    """``weight_proxy``'s result as the lines of the report: what was fitted, the weight model, the leak reference,
    the weight alone, a table of the checked features and the reading.
    """
    weight = result["weight"]
    rows = (
        f"train and test sides capped at {result['max_rows']:,} random rows (seed 0)"
        if result["subsampled"]
        else "every row of the splits"
    )
    direction = "higher" if result["greater_is_better"] else "lower"
    weighted = f", weighted by `{result['metric_row_weight']}`" if result["metric_row_weight"] else ""
    if not result["declared_metric"]:
        weighted = "; no declared metric, so the probe's own, weighted by the training weight"
    trained = "the task's sample weight" if result["trained_with_sample_weight"] else f"`{weight}`"
    lines = [
        f"weight proxy (probe 22) of `{weight}`: {result['splits']} splits x {len(result['seeds'])} seeds, {rows}; "
        f"metric {result['metric']} ({direction} is better{weighted}); every fit of the target trained with {trained} "
        f"as the row weight (LightGBM objective {result['objective']})"
    ]
    model = result["weight_model"]
    top = ", ".join(f"{f} {share:.0%}" for f, share in model["top_features"].items()) or "none"
    lines.append(
        f"  the weight from the features (LightGBM, fitted on each train side): R^2 {stat_text(model['r2'])}, "
        f"Spearman {stat_text(model['spearman'])}; top features by gain: {top}"
    )
    lines.append(
        f"  leak reference: honest fit {stat_text(result['honest'])}, with the weight as a feature "
        f"{stat_text(result['with_weight'])}; the weight gains {stat_text(result['leak_reference'], signed=True)}"
    )
    alone = result["weight_alone"]
    if alone:
        how = (
            "1/weight alone as the prediction"
            if alone["as"] == "1/weight"
            else f"a fit of the target on the weight alone (objective {result['objective']})"
        )
        lines.append(
            f"  {how}: {stat_text(alone)}, against the honest fit's {result['honest']['mean']:.5g} and the weighted "
            f"constant's {result['constant']['mean']:.5g}"
        )
    table = [("feature", "gain without the weight", "gain with it", "weight-mediated (share of the gain)", "")]
    for f, v in result["features_checked"].items():
        share = "" if np.isnan(v["mediated_share"]) else f", {v['mediated_share']:.0%}"
        table.append(
            (
                f,
                stat_text(v["gain_without_weight"], signed=True),
                stat_text(v["gain_with_weight"], signed=True),
                stat_text(v["weight_mediated"], signed=True) + share,
                "flag" if v["flag"] else "",
            )
        )
    if len(table) > 1:
        widths = [max(len(row[k]) for row in table) for k in range(len(table[0]))]
        lines += ["  " + "  ".join(c.ljust(widths[k]) for k, c in enumerate(row)).rstrip() for row in table]
    if result["metric_errors"]:
        lines.append(f"  the metric failed on some fits (scored NaN, left out): {result['metric_errors'][0]}")
    lines.append(f"  reading: {result['reading']}")
    return lines
