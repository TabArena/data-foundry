"""Probe 23, the leak tests of a split forced from temporal: the outcome of a test row's period (``period_outcome``)
and its unit (``shared_units``) shared with the training side.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from data_foundry.probes.leak.core import profile_codes, say
from data_foundry.probes.leak.fits import TargetFits, forced_inputs, spread, stat_text

FORCED_SE = 2.0
"""A gain of probe 23 is flagged when its mean over the splits is above this many standard errors."""


MIN_PERIOD_ROWS = 30
"""Test rows a period needs to be scored on its own (the score within a period)."""


LOOKUP_FOLDS = 5
"""Random folds of the training side for the out-of-fold lookup of a training row's unit."""


FORCED_READING = (
    "A leak across a forced split is weighed case by case (SPLIT-8): removed where the data allows, otherwise measured "
    "in the notes; the forced tag stays either way."
)


def _mean_se(values) -> dict:
    """The mean of per-split values, its standard error (SD / sqrt(n), ddof 1), n, and how many are above 0."""
    v = np.asarray(list(values), dtype=float)
    v = v[np.isfinite(v)]
    return {
        "mean": float(v.mean()) if len(v) else float("nan"),
        "se": float(v.std(ddof=1) / np.sqrt(len(v))) if len(v) > 1 else float("nan"),
        "splits": len(v),
        "positive": int((v > 0).sum()),
    }


def _nanmean(values) -> float:
    """The mean of the finite values, NaN when there is none (and no warning)."""
    v = np.asarray(list(values), dtype=float)
    v = v[np.isfinite(v)]
    return float(v.mean()) if len(v) else float("nan")


def _above_noise(stat: dict) -> bool:
    """A gain above 0 by more than ``FORCED_SE`` standard errors."""
    return bool(stat["mean"] > 0 and np.isfinite(stat["se"]) and stat["mean"] > FORCED_SE * stat["se"])


def _capped_pairs(splits: list, n_splits: int, max_rows: int) -> tuple[list, bool]:
    """The first ``n_splits`` splits, each side capped at ``max_rows`` random rows (seed 0), and whether any was."""
    rng = np.random.default_rng(0)
    cap = lambda idx: np.sort(rng.choice(idx, min(len(idx), max_rows), replace=False))
    chosen = [(np.asarray(tr), np.asarray(te)) for tr, te in list(splits)[:n_splits]]
    return [(cap(tr), cap(te)) for tr, te in chosen], any(len(tr) > max_rows or len(te) > max_rows for tr, te in chosen)


def _fit_header(fits: TargetFits, metric: dict | None, fit_params: dict | None, sample_weight) -> dict:
    """What probe 23's fits were: the metric, its direction and row weight, the training weight and the objective."""
    regression = fits.regression
    return {
        "metric": metric["name"] if metric is not None else ("r2" if regression else "roc_auc"),
        "declared_metric": metric is not None,
        "greater_is_better": fits.sign > 0,
        "metric_row_weight": metric.get("row_weight") if metric is not None else None,
        "trained_with_sample_weight": sample_weight is not None,
        "fit_params": dict(fit_params or {}),
        "objective": (fit_params or {}).get("objective") or ("L2" if regression else "log loss"),
    }


def period_outcome(  # noqa: C901, PLR0912, PLR0913
    df: pd.DataFrame,
    target: str,
    problem_type: str,
    splits: list,
    periods,
    *,
    labels: list[str] | None = None,
    sample_weight=None,
    feature_cols: list[str] | tuple[str, ...] | None = None,
    group_cols: list[str] | tuple[str, ...] = (),
    metric: dict | None = None,
    period_name: str = "period",
    period_kind: str = "",
    name: str = "dataset",
    n_splits: int = 9,
    max_rows: int = 50_000,
    seeds: tuple[int, ...] = (0, 1, 2),
    n_estimators: int = 300,
    fit_params: dict | None = None,
    n_jobs: int = 8,
    min_rows: int = MIN_PERIOD_ROWS,
    report: bool = True,
) -> dict:
    """Probe 23 (a): do the training rows of a test row's period tell its outcome?

    A split forced from temporal (``ForcedGroupedFromTemporal``, ``ForcedIIDFromTemporal``) puts rows of one period on
    both sides, where a model deployed at the period's start would know none of its outcomes: a shock shared by the
    period (a storm, a claims inflation, a price level) reaches the test rows through the training rows of their period.
    On the first ``n_splits`` splits, each side capped at ``max_rows`` random rows (seed 0), and once per seed of
    ``seeds``: the test rows of each period are predicted by a fit without the training rows of that period, and by a
    fit without as many random training rows (the same training size, drawn per split, seed and period). The gain of
    the period's own rows is the score of the second less the score of the first, positive when they help whatever the
    metric's direction, taken pooled over the test side (each period's rows predicted by their own fits) and within a
    period (the mean of the periods' own scores, over those with at least ``min_rows`` test rows), which leaves out a
    shift of level between the periods (a ranking metric, or one rescaled to the scored rows' total, sees it only
    pooled). A split's gain is the mean over its seeds; the result gives the mean over the splits, its standard error
    (a lower bound: the repeats reuse the rows) and the splits with a positive gain, and the gain on each period's
    rows. A gain above ``FORCED_SE`` standard errors is flagged: the split shares the period's outcome. A period
    finer than the cycle of a feature can flag without a shared outcome: a quarter's rows may be the only ones with
    some values of a seasonal feature, which the fit without them extrapolates (pricing_game_2016_french_fleet by
    quarter, +0.46 pooled with SE 0.17, most of it in the fourth quarters, whose cover to 31 December is shortest;
    by year +0.07 with SE 0.22). The default period, the coarsest with three or more, avoids that. The fits are
    LightGBM with ``_regularised``'s settings, trained with the training weight and the objective of ``fit_params``,
    scored by ``metric`` (``TargetFits``), on the model inputs with dates as days since the earliest.

    Args:
        df: The rows, with the target and the group columns.
        target: The target column.
        problem_type: ``"regression"``, or a classification type.
        splits: ``(train_idx, test_idx)`` row positions; the first ``n_splits`` are probed.
        periods: Each row's period code, 0 to k - 1 (``outcome_periods``).
        labels: The name of each period (default its code).
        sample_weight: The task's training weight, one value per row, or None.
        feature_cols: The model inputs (default: every column but the target and the groups).
        group_cols: Columns that are not features.
        metric: The task's own metric (``curation_probes.weights``), or None for R^2 or ROC AUC.
        period_name: The column the periods come from, for the report.
        period_kind: How it was cut (``yearly``, ``years``), for the report.
        name: The dataset's name in the result.
        n_splits: Splits to probe.
        max_rows: Rows kept (at random) of each train and test side.
        seeds: The LightGBM seeds; each split is fitted once per seed.
        n_estimators: Trees per LightGBM fit.
        fit_params: LightGBM parameters of the fits, such as ``{"objective": "tweedie"}``; None for the default.
        n_jobs: Threads per LightGBM model.
        min_rows: Test rows a period needs for its own score.
        report: Print the lines of ``period_outcome_lines``.
    """
    codes = np.asarray(periods, dtype=np.int64)
    if len(codes) != len(df):
        raise ValueError(f"`{period_name}` needs one period per row ({len(codes):,} for {len(df):,} rows)")
    count = int(codes.max()) + 1
    labels = list(labels) if labels is not None else [str(k) for k in range(count)]
    fits = TargetFits(
        df[target],
        problem_type,
        sample_weight,
        metric=metric,
        fit_params=fit_params,
        n_estimators=n_estimators,
        n_jobs=n_jobs,
        regularised=True,
    )
    columns = list(feature_cols) if feature_cols is not None else [c for c in df.columns if c != target]
    X = forced_inputs(df, [c for c in columns if c not in {target, *group_cols}])
    pairs, sampled = _capped_pairs(splits, n_splits, max_rows)
    seeds, sign = tuple(seeds), fits.sign

    pooled, within, constant = [], [], []
    per_period: dict[int, list[float]] = {k: [] for k in range(count)}
    scored = {"without_period": [], "without_random": []}
    whole_side: set[int] = set()  # periods that hold every training row: nothing is left to fit on
    for i, (tr, te) in enumerate(pairs):
        constant.append(fits.score(fits.constant(tr, len(te)), te))
        split_pooled, split_within = [], []
        split_period: dict[int, list[float]] = {k: [] for k in range(count)}
        for seed in seeds:
            rng = np.random.default_rng([i, seed])
            shape = (len(te),) if fits.regression else (len(te), fits.n_classes)
            p_out, p_rand = np.full(shape, np.nan), np.full(shape, np.nan)
            keep = np.zeros(len(te), dtype=bool)
            own_scores = {}
            for k in np.unique(codes[te]):
                at, own = codes[te] == k, codes[tr] == k
                if own.all():
                    whole_side.add(int(k))
                    continue
                keep |= at
                tr_out = tr[~own]
                p_out[at] = fits.fit_predict(X.iloc[tr_out], X.iloc[te[at]], tr_out, seed)
                if own.any():
                    tr_rand = np.sort(rng.choice(tr, len(tr_out), replace=False))
                    p_rand[at] = fits.fit_predict(X.iloc[tr_rand], X.iloc[te[at]], tr_rand, seed)
                else:  # no training row of the period: nothing to leave out
                    p_rand[at] = p_out[at]
                if at.sum() >= min_rows:
                    own_scores[int(k)] = (fits.score(p_out[at], te[at]), fits.score(p_rand[at], te[at]))
            out, rand = fits.score(p_out[keep], te[keep]), fits.score(p_rand[keep], te[keep])
            scored["without_period"].append(out)
            scored["without_random"].append(rand)
            split_pooled.append(sign * (rand - out))
            gains = {k: sign * (r - o) for k, (o, r) in own_scores.items()}
            split_within.append(_nanmean(gains.values()))
            for k, gain in gains.items():
                split_period[k].append(gain)
        pooled.append(_nanmean(split_pooled))
        within.append(_nanmean(split_within))
        for k, values in split_period.items():
            if values:
                per_period[k].append(_nanmean(values))

    result = {
        "name": name,
        "period": period_name,
        "period_kind": period_kind,
        "periods": labels,
        **_fit_header(fits, metric, fit_params, sample_weight),
        "rows": len(df),
        "features": X.shape[1],
        "splits": len(pairs),
        "seeds": list(seeds),
        "max_rows": max_rows,
        "subsampled": sampled,
        "min_rows": min_rows,
        "scores": {
            "without_period": spread(scored["without_period"]),
            "without_random": spread(scored["without_random"]),
            "constant": spread(constant),
        },
        "pooled": _mean_se(pooled),
        "within": _mean_se(within),
        "per_period": {labels[k]: _mean_se(v) for k, v in per_period.items() if v},
        "whole_side_periods": [labels[k] for k in sorted(whole_side)],
        "threshold_se": FORCED_SE,
        "metric_errors": fits.errors,
    }
    result["flags"] = [part for part in ("pooled", "within") if _above_noise(result[part])]
    skill = sign * (result["scores"]["without_period"]["mean"] - result["scores"]["constant"]["mean"])
    result["skill_without_period"] = skill
    if result["flags"]:
        head = (
            f"The training rows of a test row's period add to its score above noise ({FORCED_SE:g} SEs over the "
            f"splits; {', '.join(result['flags'])}): the split shares the period's outcome, which a model deployed at "
            "the period's start would not know. "
        )
    else:
        head = "No gain of the period's own training rows above noise: no outcome of the period is shared across the "
        head += "split at this resolution. "
    result["reading"] = head + FORCED_READING
    if report:
        for line in period_outcome_lines(result):
            say(line)
    return result


def _gain(stat: dict) -> str:
    """A gain over the splits as one cell: the mean, its SE, and the splits above 0."""
    se = f"SE {stat['se']:.2g}" if np.isfinite(stat["se"]) else "no SE"
    return f"{stat['mean']:+.4g} ({se}, above 0 on {stat['positive']} of {stat['splits']} splits)"


def _fits_line(result: dict) -> str:
    """The metric and the fits of a probe-23 result, for its first line."""
    direction = "higher" if result["greater_is_better"] else "lower"
    weighted = f", weighted by `{result['metric_row_weight']}`" if result["metric_row_weight"] else ""
    if not result["declared_metric"]:
        weighted = "; no declared metric, so the probe's own"
    trained = ", every fit trained with the task's sample weight" if result["trained_with_sample_weight"] else ""
    rows = (
        f"train and test sides capped at {result['max_rows']:,} random rows (seed 0)"
        if result["subsampled"]
        else "every row of the splits"
    )
    return (
        f"{result['splits']} splits x {len(result['seeds'])} seeds, {rows}; metric {result['metric']} ({direction} is "
        f"better{weighted}){trained} (LightGBM objective {result['objective']})"
    )


def period_outcome_lines(result: dict) -> list[str]:
    """``period_outcome``'s result as the lines of the report."""
    shown = ", ".join(result["periods"][:6]) + (", ..." if len(result["periods"]) > 6 else "")
    kind = f"{result['period_kind']}, " if result["period_kind"] else ""
    scores = result["scores"]
    lines = [
        f"period outcome (probe 23) on `{result['period']}` ({kind}{len(result['periods'])} periods: {shown}): "
        + _fits_line(result),
        "  each test period predicted by a fit without its period's training rows, and by one without as many "
        "random training rows (the same training size)",
        f"  scores: without the period's rows {stat_text(scores['without_period'])}, without random rows "
        f"{stat_text(scores['without_random'])}, the weighted constant {scores['constant']['mean']:.5g}",
        f"  gain of the period's own training rows: pooled {_gain(result['pooled'])}; within a period "
        f"{_gain(result['within'])}",
    ]
    per = "; ".join(f"{k} {v['mean']:+.3g} (SE {v['se']:.2g})" for k, v in result["per_period"].items())
    if per:
        lines.append(f"  per period (at least {result['min_rows']} test rows): {per}")
    if result["whole_side_periods"]:
        lines.append(f"  not tested (every training row in the period): {', '.join(result['whole_side_periods'])}")
    if result["metric_errors"]:
        lines.append(f"  the metric failed on some fits (scored NaN, left out): {result['metric_errors'][0]}")
    lines.append(f"  reading: {result['reading']}")
    return lines


def _unit_targets(fits: TargetFits) -> np.ndarray:
    """What a lookup averages, one column per value: the target, the event of a binary target, each class's share."""
    if fits.regression:
        return fits.truth[:, None].astype(float)
    hits = (fits.truth[:, None] == fits.classes[None, :]).astype(float)
    return hits[:, 1:] if fits.n_classes == 2 else hits


def _lookup(
    units: np.ndarray,
    values: np.ndarray,
    w: np.ndarray,
    tr: np.ndarray,
    rows: np.ndarray,
    te: np.ndarray,
    rng,
    groups: np.ndarray | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """The lookup of each row's unit: the weighted mean of ``values`` over the unit's training rows, for the training
    rows ``rows`` out of fold (``LOOKUP_FOLDS`` random folds of the training side ``tr``) and for the test rows ``te``
    over all of ``tr``. A row without a unit (code -1), or whose unit has no such row, gets NaN. The count of the rows
    is left out: it reads no outcome, and a count of similar rows is a feature a deployed model may have.

    With ``groups`` (a group code per row: the split's groups), the folds are drawn by group, so a training row's
    lookup never reads its own group, as a test row's never does. Folds of rows would let it: on
    pricing_game_2016_french_fleet 19.2% of the training periods got an exact-profile lookup, 78% of its weight from
    the same contract, and the fit learned a lookup the test rows never had (+0.117 by row folds, -0.047 by contract).
    """
    size = int(units.max()) + 2  # the last slot holds the rows without a unit

    def table(source: np.ndarray, target: np.ndarray) -> np.ndarray:
        keys = np.where(units[source] >= 0, units[source], size - 1)
        mass = np.bincount(keys, weights=w[source], minlength=size)
        sums = np.column_stack([np.bincount(keys, weights=w[source] * v, minlength=size) for v in values[source].T])
        mass[-1], sums[-1] = 0.0, 0.0
        at = np.where(units[target] >= 0, units[target], size - 1)
        with np.errstate(invalid="ignore", divide="ignore"):
            return np.where(mass[at, None] > 0, sums[at] / mass[at, None], np.nan)

    fold = np.full(len(units), -1)
    if groups is None:
        fold[tr] = rng.permutation(len(tr)) % LOOKUP_FOLDS
    else:
        _, at_group = np.unique(groups[tr], return_inverse=True)
        fold[tr] = (rng.permutation(at_group.max() + 1) % LOOKUP_FOLDS)[at_group]
    on_train = np.empty((len(rows), values.shape[1]))
    for f in range(LOOKUP_FOLDS):
        at = fold[rows] == f
        on_train[at] = table(tr[fold[tr] != f], rows[at])
    return on_train, table(tr, te)


def shared_units(  # noqa: C901, PLR0912, PLR0913
    df: pd.DataFrame,
    target: str,
    problem_type: str,
    splits: list,
    *,
    unit_cols: list[str] | tuple[str, ...] = (),
    sample_weight=None,
    feature_cols: list[str] | tuple[str, ...] | None = None,
    group_cols: list[str] | tuple[str, ...] = (),
    metric: dict | None = None,
    without: str | None = None,
    name: str = "dataset",
    n_splits: int = 9,
    max_rows: int = 50_000,
    seeds: tuple[int, ...] = (0, 1, 2),
    n_estimators: int = 300,
    fit_params: dict | None = None,
    n_jobs: int = 8,
    report: bool = True,
) -> dict:
    """Probe 23 (b): do test rows share their unit with training rows, and what does a lookup of the unit gain?

    The units: each column of ``unit_cols`` (the group columns, which a grouped split never shares; the probe confirms
    it), the exact profile of the model inputs (strings and dates included, unrounded, a missing value equal to a
    missing value: ``profile_codes``), and with ``without`` (the period column) the same profile without it: the unit
    seen in another period. The share of test rows whose unit has a training row is counted on every split given (a
    test row in several repeats counts each time). For each unit with such rows on the probed splits (the first
    ``n_splits``, each side capped at ``max_rows`` random rows, seed 0, once per seed of ``seeds``), a lookup of the
    unit's training target joins the inputs: the weighted mean of the target (of each class's indicator) over the
    unit's training rows, over the whole training side for a test row and out of fold for a training row, the folds
    drawn by the group columns on a grouped split (``_lookup``: a training row never reads its own group, as a test
    row never does; a split that shares its groups gets folds of rows). The gain is the score with the lookup less the
    honest fit's (positive when the lookup helps), and next to it the gain on the test rows with a lookup and the
    change on the rest, each the two fits scored on those rows alone (the parts need not add up to the whole: a
    rescaled or ranked metric of the whole side couples them; scored apart, the rest's change is 0 while its
    predictions stay as they were). A split's numbers are the means over its seeds; over the splits, the mean, its
    standard error and the splits above 0. A gain on the rows with a lookup above ``FORCED_SE`` standard errors is
    flagged: the unit's outcome reaches the test rows through the training side. A change on the rest above noise is
    no route of a leak but a sign that the lookup changed the fit (read the gain with care). For a profile the flag
    has a second reading: natural repeats of coarse features (LEAK-18), whose lookup is the mean of a cell finer than
    the regularised fit makes; whether the copies are one entity decides (LEAK-17). The fits are those of
    ``period_outcome``.

    Args:
        df: The rows, with the target and the group columns.
        target: The target column.
        problem_type: ``"regression"``, or a classification type.
        splits: ``(train_idx, test_idx)`` row positions; the first ``n_splits`` are probed with the lookup.
        unit_cols: Columns whose value names a unit (the group columns).
        sample_weight: The task's training weight, one value per row, or None.
        feature_cols: The model inputs (default: every column but the target and the groups).
        group_cols: Columns that are not features; on a grouped split, the groups the training side's lookup folds
            are drawn by.
        metric: The task's own metric (``curation_probes.weights``), or None for R^2 or ROC AUC.
        without: A model input (the period column) left out of a second profile.
        name: The dataset's name in the result.
        n_splits: Splits to probe with the lookup.
        max_rows: Rows kept (at random) of each train and test side for the lookup fits.
        seeds: The LightGBM seeds; each split is fitted once per seed.
        n_estimators: Trees per LightGBM fit.
        fit_params: LightGBM parameters of the fits; None for the default.
        n_jobs: Threads per LightGBM model.
        report: Print the lines of ``shared_units_lines``.
    """
    fits = TargetFits(
        df[target],
        problem_type,
        sample_weight,
        metric=metric,
        fit_params=fit_params,
        n_estimators=n_estimators,
        n_jobs=n_jobs,
        regularised=True,
    )
    columns = list(feature_cols) if feature_cols is not None else [c for c in df.columns if c != target]
    columns = [c for c in columns if c not in {target, *group_cols}]
    units: dict[str, np.ndarray] = {}
    for col in unit_cols:
        units[f"`{col}`"] = pd.factorize(df[col])[0].astype(np.int64)
    units[f"the exact profile of the {len(columns)} model inputs"] = profile_codes(df[columns])
    if without is not None and without in columns and len(columns) > 1:
        rest = [c for c in columns if c != without]
        units[f"the exact profile without `{without}`"] = profile_codes(df[rest])
    X = forced_inputs(df, columns)
    values = _unit_targets(fits)
    groups = profile_codes(df[list(group_cols)]) if group_cols else None
    pairs, sampled = _capped_pairs(splits, n_splits, max_rows)
    seeds, sign = tuple(seeds), fits.sign

    def matched(codes: np.ndarray, tr: np.ndarray, te: np.ndarray) -> np.ndarray:
        seen = np.bincount(codes[tr][codes[tr] >= 0], minlength=int(codes.max()) + 1) > 0
        return (codes[te] >= 0) & seen[np.maximum(codes[te], 0)]

    found = {}
    for label, codes in units.items():
        per_split = [float(matched(codes, np.asarray(tr), np.asarray(te)).mean()) for tr, te in splits]
        rows = sum(len(te) for _, te in splits)
        hits = round(sum(share * len(te) for share, (_, te) in zip(per_split, splits, strict=True)))
        found[label] = {
            "matched": hits / rows if rows else float("nan"),
            "matched_rows": hits,
            "matched_per_split": per_split,
        }

    honest: dict[tuple[int, int], float] = {}
    parts = ("total", "with_lookup", "rest")
    gains: dict[str, dict[str, list[float]]] = {label: {part: [] for part in parts} for label in units}
    folds_by: set[str] = set()
    for i, (tr, te) in enumerate(pairs):
        tr_all = np.asarray(list(splits)[i][0])
        shared = [label for label, codes in units.items() if matched(codes, tr_all, te).any()]
        # folds by group where the split keeps the groups apart; a split that shares them gets folds of rows
        apart = groups if groups is not None and not matched(groups, tr_all, te).any() else None
        folds_by.add("by row" if apart is None else "by group")
        split_gains = {label: {part: [] for part in parts} for label in units}
        for seed in seeds if shared else ():  # no shared unit on this split: nothing to look up
            plain = fits.fit_predict(X.iloc[tr], X.iloc[te], tr, seed)
            honest[i, seed] = fits.score(plain, te)
            for label in shared:
                rng = np.random.default_rng([i, seed])
                on_tr, on_te = _lookup(units[label], values, fits.train_w, tr_all, tr, te, rng, apart)
                extra = [f"_lookup{j}" for j in range(on_tr.shape[1])]
                x_tr = pd.concat([X.iloc[tr].reset_index(drop=True), pd.DataFrame(on_tr, columns=extra)], axis=1)
                x_te = pd.concat([X.iloc[te].reset_index(drop=True), pd.DataFrame(on_te, columns=extra)], axis=1)
                looked = fits.fit_predict(x_tr, x_te, tr, seed)
                hit = np.isfinite(on_te).any(axis=1)
                total = sign * (fits.score(looked, te) - honest[i, seed])
                # each part scored on its own rows: the rest's change is 0 while its predictions stay as they were (a
                # rescaled or ranked metric of the whole side would couple the parts)
                on_hit, rest = (
                    sign * (fits.score(looked[at], te[at]) - fits.score(plain[at], te[at])) if at.any() else np.nan
                    for at in (hit, ~hit)
                )
                for part, value in zip(parts, (total, on_hit, rest), strict=True):
                    split_gains[label][part].append(value)
        for label, by_part in split_gains.items():
            for part, values_ in by_part.items():
                if values_:
                    gains[label][part].append(_nanmean(values_))
    for label in units:
        fitted = bool(gains[label]["total"])
        found[label]["lookup_gain"] = _mean_se(gains[label]["total"]) if fitted else None
        found[label]["gain_with_lookup"] = _mean_se(gains[label]["with_lookup"]) if fitted else None
        found[label]["change_without_lookup"] = _mean_se(gains[label]["rest"]) if fitted else None
        found[label]["flag"] = fitted and _above_noise(found[label]["gain_with_lookup"])
        rest = found[label]["change_without_lookup"]
        found[label]["rest_moved"] = fitted and (_above_noise(rest) or _above_noise({**rest, "mean": -rest["mean"]}))
    result = {
        "name": name,
        **_fit_header(fits, metric, fit_params, sample_weight),
        "rows": len(df),
        "features": X.shape[1],
        "splits_counted": len(list(splits)),
        "splits": len(pairs),
        "seeds": list(seeds),
        "max_rows": max_rows,
        "subsampled": sampled,
        "lookup_folds": " and ".join(sorted(folds_by)) or "none",
        "honest": spread(honest.values()),
        "units": found,
        "flags": [label for label, v in found.items() if v["flag"]],
        "threshold_se": FORCED_SE,
        "metric_errors": fits.errors,
    }
    if result["flags"]:
        head = (
            f"A lookup of the unit's training rows adds to the score of the test rows that have one, above noise "
            f"({FORCED_SE:g} SEs over the splits; {'; '.join(result['flags'])}): the unit's outcome reaches the test "
            "rows through the training side. "
        )
        if any(label.startswith("the exact profile") for label in result["flags"]):
            head += (
                "For a profile, natural repeats of coarse features read the same (LEAK-18: the lookup is the mean of a "
                "finer cell than the fit makes); whether the copies are one entity decides (LEAK-17). "
            )
    else:
        head = "No lookup of a shared unit adds to the score of the test rows that have one above noise. "
    moved = [label for label, v in found.items() if v["rest_moved"]]
    if moved:
        head += (
            f"The lookup moved the fit on the rows without one ({'; '.join(moved)}): no route of a leak, but its gain "
            "there says the lookup changed the fit; read the gain on the rows with one with care. "
        )
    result["reading"] = head + FORCED_READING
    if report:
        for line in shared_units_lines(result):
            say(line)
    return result


def shared_units_lines(result: dict) -> list[str]:
    """``shared_units``' result as the lines of the report."""
    if result["honest"]["runs"]:
        lines = [
            f"shared units (probe 23): lookups on {_fits_line(result)}; a training row's lookup out of fold, folds "
            f"{result['lookup_folds']}; honest fit {stat_text(result['honest'])}"
        ]
    else:
        lines = [f"shared units (probe 23): no unit shared on the first {result['splits']} splits, so no lookup"]
    for label, unit in result["units"].items():
        spread = [s for s in unit["matched_per_split"] if np.isfinite(s)]
        per_split = f" (per split {min(spread):.1%} to {max(spread):.1%})" if len(spread) > 1 else ""
        line = (
            f"  {label}: {unit['matched']:.1%} of the test rows of {result['splits_counted']} splits "
            f"({unit['matched_rows']:,}) have their unit in training{per_split}"
        )
        if unit["lookup_gain"] is not None:
            line += (
                f"; a lookup of its training target gains {_gain(unit['gain_with_lookup'])} on the test rows with "
                f"one, changes the rest by {_gain(unit['change_without_lookup'])}, in all "
                f"{_gain(unit['lookup_gain'])}"
            )
            line += " flag" if unit["flag"] else ""
        lines.append(line)
    if result["metric_errors"]:
        lines.append(f"  the metric failed on some fits (scored NaN, left out): {result['metric_errors'][0]}")
    lines.append(f"  reading: {result['reading']}")
    return lines
