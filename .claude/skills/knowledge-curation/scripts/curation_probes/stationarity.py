"""The stationary-relation test (SPLIT-32): is the target's relation to the features flat across the periods the
data holds?

Where a forward use case meets no usable windows, SPLIT-32 lets a split stay random (or grouped by the unit) as a
``StationaryRelation`` only when the target and its relation to the features are measured flat across the periods
the data holds. ``stationary_relation`` measures it, the same way for every dataset:

* **Windows:** the newest ``n_windows`` periods P with enough rows (for periods without an order, such as month
  classes, every period), each tested on its own.
* **Test rows:** per seed, a random half of P (whole units where a unit recurs and the use case meets new units:
  ``units``); the units of the test half leave every training side.
* **Two models, the same test rows:** a *forward* model trained on the rows before P (for unordered periods, on the
  other periods), and a *contemporaneous* model trained on as many rows, made of the whole other half of P and the
  rest drawn at random from the rows before P. Both are scored on the test half by the task's metric, and a constant
  predictor (the forward side's weighted mean or class shares) beside them.
* **The gap** is how much worse the forward model scores than the contemporaneous one (positive when worse, whatever
  the metric's direction): what having seen the period buys. Its mean and SD are over ``seeds`` seeds, each of which
  draws the test half, the contemporaneous sample and the models' seeds anew.
* **The floor** is ``FLOOR_SHARE`` of the distance between the contemporaneous model and the constant predictor: a
  gap below it is too small to matter, whatever its noise.
* **Models:** a regularised LightGBM (probe 23's settings, ``leak._regularised``) on every training row, and, where
  ``foundation`` gives one, a tabular foundation model on at most ``max_foundation_train`` training rows and
  ``max_foundation_test`` test rows (both drawn by the same rules). For a time basis it is one state-of-the-art
  tabular foundation model, on a GPU: TabPFN v3.5 (``tabpfn_v35``) or Kumo-Tabular (``kumo_tabular``).

A window is **not flat** for a model when its mean gap is above both two SDs and the floor; **flat** when it is not, the
contemporaneous model beats the constant predictor, and the test was fine enough to see a gap of a few floors (two SDs
at most ``INCONCLUSIVE_RATIO`` floors); **inconclusive** otherwise (a model without skill cannot lose any). The gap
averaged over the windows (``pooled``: its SD is the root of the summed variances over k windows, divided by k) is read
the same way, so a small set gets the evidence of all its windows, both ways. The dataset is not flat when one window,
or the pooled gap, is not flat for one model; flat when, for a model that beats the constant in every window, the
pooled gap is flat; inconclusive otherwise. For classification, a class share that changes by a factor of
``SHARE_FACTOR`` or more between two periods, with a chi-square p below ``SHARE_P``, is a change in recording and makes
the dataset not flat whatever the models say; a moving share below that is reported, not counted (SPLIT-32).

The verdict on the relation covers the newest ``TIME_BASIS_WINDOWS`` periods (every period, unordered), whatever their
training share: SPLIT-14's floor is for a split's windows, not for this test. A run on fewer (``test_periods``, or
``n_windows`` below it, as when each window runs as its own job) reports ``verdict: partial`` with its own reading in
``partial_verdict``; ``combine_runs`` joins the runs into the verdict.
"""

from __future__ import annotations

from collections.abc import Callable

import numpy as np
import pandas as pd
from scipy.stats import fisher_exact

from . import leak

FLOOR_SHARE = 0.01
"""The floor: a share of the distance between the contemporaneous model and the constant predictor."""
INCONCLUSIVE_RATIO = 10.0
"""A window whose two SDs exceed this many floors cannot show a gap that matters: inconclusive, not flat."""
SHARE_FACTOR = 2.0
SHARE_P = 0.01
"""A class share that changes by this factor between two periods, at this chi-square p, is a change in recording."""
MIN_WINDOW_ROWS = 40
"""Rows a period needs to be a window: a test half of 20 rows at least."""
TIME_BASIS_WINDOWS = 3
"""The newest periods a verdict on the relation covers (SPLIT-32); a run on fewer is partial."""

Foundation = Callable[[pd.DataFrame, np.ndarray, pd.DataFrame, int], np.ndarray]
"""``fit_predict(x_train, y_train, x_test, seed)``: values, or class probabilities in the order of ``fits.classes``."""


def _draw_units(rows: np.ndarray, size: float, units: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Whether each of ``rows`` is drawn: whole units in a random order until about ``size`` rows (at least one unit).
    ``units`` are integer codes, so the membership test is vectorised.
    """
    u = units[rows]
    keys, counts = np.unique(u, return_counts=True)
    order = rng.permutation(len(keys))
    n_take = max(1, int(np.searchsorted(np.cumsum(counts[order]), size)))
    return np.isin(u, keys[order[:n_take]])


def _halves(rows: np.ndarray, units: np.ndarray | None, rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
    """A random half of ``rows`` (whole units when ``units`` is given) and the rest."""
    if units is None:
        perm = rng.permutation(rows)
        return np.sort(perm[: len(rows) // 2]), np.sort(perm[len(rows) // 2 :])
    in_test = _draw_units(rows, len(rows) / 2, units, rng)
    return rows[in_test], rows[~in_test]


def _cap(rows: np.ndarray, cap: int | None, units: np.ndarray | None, rng: np.random.Generator) -> np.ndarray:
    """At most ``cap`` of ``rows``, drawn at random (whole units when ``units`` is given)."""
    if cap is None or len(rows) <= cap:
        return rows
    if units is None:
        return np.sort(rng.choice(rows, cap, replace=False))
    return rows[_draw_units(rows, cap, units, rng)]


def _contemporaneous(before: np.ndarray, rest: np.ndarray, size: int, rng: np.random.Generator) -> np.ndarray:
    """``size`` training rows that include the whole other half of the period (``rest``), filled up from ``before``."""
    if len(rest) >= size:
        return np.sort(rng.choice(rest, size, replace=False))
    fill = rng.choice(before, size - len(rest), replace=False) if size > len(rest) else np.array([], dtype=int)
    return np.sort(np.concatenate([rest, fill]).astype(int))


def recording_change(
    y: pd.Series, codes: np.ndarray, labels: list[str], problem_type: str, *, min_rows: int = MIN_WINDOW_ROWS
) -> dict | None:
    """The largest change of a class share between two periods of ``min_rows`` rows or more, and whether it counts as
    a change in recording (a factor of ``SHARE_FACTOR`` or more at a Fisher exact p below ``SHARE_P``); None for a
    regression. Where a pair counts, the largest such change is reported.
    """
    if problem_type == "regression":
        return None
    classes, class_codes = np.unique(y.to_numpy(), return_inverse=True)
    n_periods = len(labels)
    table = np.bincount(codes * len(classes) + class_codes, minlength=n_periods * len(classes))
    table = table.reshape(n_periods, len(classes))
    rows = table.sum(axis=1)
    periods = [k for k in range(n_periods) if rows[k] >= min_rows]
    best, best_counting = None, None
    for j, c in enumerate(classes):
        share = table[:, j] / np.maximum(rows, 1)
        for a in periods:
            for b in periods:
                if share[a] <= share[b] or share[b] == 0:
                    continue
                pair = np.array([[table[a, j], rows[a] - table[a, j]], [table[b, j], rows[b] - table[b, j]]])
                change = {
                    "class": str(c),
                    "high": labels[a],
                    "low": labels[b],
                    "high_share": float(share[a]),
                    "low_share": float(share[b]),
                    "factor": float(share[a] / share[b]),
                    "p": float(fisher_exact(pair)[1]),
                }
                change["counts"] = bool(change["factor"] >= SHARE_FACTOR and change["p"] < SHARE_P)
                if best is None or change["factor"] > best["factor"]:
                    best = change
                if change["counts"] and (best_counting is None or change["factor"] > best_counting["factor"]):
                    best_counting = change
    return best_counting or best


def _window_verdict(gap: float, sd: float, floor: float, skill: float) -> str:
    if gap > 2 * sd and gap > floor:
        return "not flat"
    if skill > 0 and 2 * sd <= INCONCLUSIVE_RATIO * floor:
        return "flat"
    return "inconclusive"


def _summary(scores: dict, sign: float) -> dict:
    f, c, k = (np.asarray(scores[x], dtype=float) for x in ("forward", "contemporaneous", "constant"))
    gaps = sign * (c - f)
    gap, sd = float(np.nanmean(gaps)), float(np.nanstd(gaps, ddof=1)) if len(gaps) > 1 else float("nan")
    skill = float(sign * (np.nanmean(c) - np.nanmean(k)))
    floor = FLOOR_SHARE * abs(skill)
    return {
        "forward": float(np.nanmean(f)),
        "contemporaneous": float(np.nanmean(c)),
        "constant": float(np.nanmean(k)),
        "gap": gap,
        "gap_sd": sd,
        "floor": floor,
        "gaps": [float(g) for g in gaps],
        "skill": skill,
        "verdict": _window_verdict(gap, sd if np.isfinite(sd) else np.inf, floor, skill),
    }


def stationary_relation(  # noqa: C901, PLR0913
    df: pd.DataFrame,
    target: str,
    problem_type: str,
    periods,
    *,
    labels: list[str] | None = None,
    ordered: bool = True,
    units=None,
    sample_weight=None,
    feature_cols: list[str] | tuple[str, ...] | None = None,
    exclude_cols: list[str] | tuple[str, ...] = (),
    metric: dict | None = None,
    fit_params: dict | None = None,
    n_windows: int = 3,
    test_periods: list[str] | None = None,
    seeds: int = 5,
    max_test: int | None = None,
    foundation: Foundation | None = None,
    foundation_name: str = "foundation model",
    max_foundation_train: int = 20_000,
    max_foundation_test: int = 5_000,
    n_estimators: int = 500,
    n_jobs: int = 8,
    min_rows: int = MIN_WINDOW_ROWS,
    report: bool = True,
) -> dict:
    """Measure whether the relation of ``target`` to the features is flat across ``periods``; see the module docstring.

    Args:
        df: The rows: the features, the target, and any unit or period column (left out of the features).
        target: The target column.
        problem_type: ``"regression"``, or a classification type.
        periods: Each row's period code, 0 to k - 1 (``leak.outcome_periods``), in time order when ``ordered``.
        labels: The name of each period.
        ordered: False for periods without an order (each period is then a window, trained on the others).
        units: Each row's unit where a unit recurs and the use case meets new units, else None.
        sample_weight: The task's training weight, one value per row, or None.
        feature_cols: The model inputs (default: every column but the target and ``exclude_cols``).
        exclude_cols: Columns that are no input: the period column and anything that names the period.
        metric: The task's own metric (``curation_probes.weights``), or None for R^2 or ROC AUC.
        fit_params: LightGBM parameters, such as ``{"objective": "tweedie"}``.
        n_windows: Windows, newest first (ordered periods only).
        test_periods: Only these windows, by label (to run each window as its own job); the verdict is then
            ``partial`` unless they hold the newest ``TIME_BASIS_WINDOWS`` (``combine_runs`` joins the jobs).
        seeds: Repeats; each draws the test half, the contemporaneous sample and the models' seeds anew.
        max_test: A cap on the LightGBM test rows per window (None: the whole half).
        foundation: A foundation model's ``fit_predict``, or None to run LightGBM alone.
        foundation_name: Its name in the report.
        max_foundation_train: Its training rows per fit, at most.
        max_foundation_test: Its test rows per window, at most (a subset of the LightGBM test rows).
        n_estimators: Trees per LightGBM fit.
        n_jobs: Threads per LightGBM model.
        min_rows: Rows a period needs to be a window.
        report: Print ``stationary_relation_lines``.
    """
    codes = np.asarray(periods, dtype=np.int64)
    if len(codes) != len(df):
        raise ValueError(f"periods: one code per row needed ({len(codes):,} for {len(df):,} rows)")
    count = int(codes.max()) + 1
    labels = list(labels) if labels is not None else [str(k) for k in range(count)]
    unit_arr = (
        None if units is None else pd.factorize(pd.Series(units).reset_index(drop=True), use_na_sentinel=False)[0]
    )
    df = df.reset_index(drop=True)
    fits = leak._TargetFits(
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
    X = leak._forced_inputs(df, [c for c in columns if c not in {target, *exclude_cols}])
    rows_per = np.bincount(codes, minlength=count)
    windows = _windows(
        codes, rows_per, labels, ordered=ordered, n_windows=n_windows, test_periods=test_periods, min_rows=min_rows
    )
    newest = _windows(
        codes, rows_per, labels, ordered=ordered, n_windows=TIME_BASIS_WINDOWS, test_periods=None, min_rows=min_rows
    )
    out = {
        "protocol": "stationary-relation test",
        "periods": labels,
        "ordered": ordered,
        "rows_by_period": [int(r) for r in rows_per],
        "units": units is not None,
        "target_by_period": _target_by_period(fits, codes, labels),
        "recording_change": recording_change(df[target], codes, labels, problem_type, min_rows=min_rows),
        "foundation": foundation_name if foundation is not None else None,
        "newest": [labels[k] for k in newest],
        "windows": [],
    }
    models = ["lightgbm"] + (["foundation"] if foundation is not None else [])
    for k in windows:
        scores = {m: {"forward": [], "contemporaneous": [], "constant": []} for m in models}
        sizes: dict = {"test_period": labels[k], "rows_in_period": int(rows_per[k])}
        p_rows = np.flatnonzero(codes == k)
        before_all = np.flatnonzero(codes < k) if ordered else np.flatnonzero(codes != k)
        x_forward = X.iloc[before_all] if unit_arr is None else None  # without units, one forward side for all seeds
        for seed in range(seeds):
            rng = np.random.default_rng(1000 * k + seed)
            test, rest = _halves(p_rows, unit_arr, rng)
            before = before_all
            if unit_arr is not None:  # the test half's units leave every training side
                gone = np.unique(unit_arr[test])
                before = before[~np.isin(unit_arr[before], gone)]
                rest = rest[~np.isin(unit_arr[rest], gone)]
            test = _cap(test, max_test, unit_arr, rng)
            forward = before
            contemporaneous = _contemporaneous(before, rest, len(forward), rng)
            sizes.setdefault("n_forward_train", []).append(len(forward))
            sizes.setdefault("n_from_period", []).append(int(np.isin(contemporaneous, rest).sum()))
            sizes.setdefault("n_test", []).append(len(test))
            const = fits.score(fits.constant(forward, len(test)), test)
            for side, tr in (("forward", forward), ("contemporaneous", contemporaneous)):
                x_tr = x_forward if side == "forward" and x_forward is not None else X.iloc[tr]
                pred = fits.fit_predict(x_tr, X.iloc[test], tr, seed)
                scores["lightgbm"][side].append(fits.score(pred, test))
            scores["lightgbm"]["constant"].append(const)
            if foundation is not None:
                t_f = _cap(test, max_foundation_test, unit_arr, rng)
                f_tr, c_tr = (_cap(tr, max_foundation_train, unit_arr, rng) for tr in (forward, contemporaneous))
                sizes.setdefault("n_foundation_train", []).append(len(f_tr))
                sizes.setdefault("n_foundation_test", []).append(len(t_f))
                for side, tr in (("forward", f_tr), ("contemporaneous", c_tr)):
                    pred = foundation(X.iloc[tr], fits.truth[tr], X.iloc[t_f], seed)
                    scores["foundation"][side].append(fits.score(pred, t_f))
                scores["foundation"]["constant"].append(fits.score(fits.constant(f_tr, len(t_f)), t_f))
        window = {key: (sorted({min(v), max(v)}) if isinstance(v, list) else v) for key, v in sizes.items()}
        for m in models:
            window[m] = _summary(scores[m], fits.sign)
        out["windows"].append(window)
    _set_verdict(out, models)
    out["metric_errors"] = fits.errors
    if report:
        for line in stationary_relation_lines(out):
            leak.say(line)
    return out


def _windows(
    codes: np.ndarray,
    rows_per: np.ndarray,
    labels: list[str],
    *,
    ordered: bool,
    n_windows: int,
    test_periods: list[str] | None,
    min_rows: int,
) -> list[int]:
    """The windows' period codes: the newest ``n_windows`` with ``min_rows`` rows and as many before them (every
    period with ``min_rows`` rows, unordered), narrowed to ``test_periods`` where given.
    """
    usable = [k for k in range(len(rows_per)) if rows_per[k] >= min_rows]
    if ordered:
        windows = [k for k in reversed(usable) if (codes < k).sum() >= min_rows][:n_windows]
    else:
        windows = list(reversed(usable))
    if test_periods is None:
        return windows
    missing = [p for p in test_periods if p not in labels]
    if missing:
        raise ValueError(f"test_periods: no period {missing}")
    return [k for k in windows if labels[k] in test_periods]


def _target_by_period(fits: leak._TargetFits, codes: np.ndarray, labels: list[str]) -> list[dict]:
    rows = []
    for k, label in enumerate(labels):
        mask = codes == k
        if not mask.any():
            continue
        if fits.regression:
            rows.append({"period": label, "rows": int(mask.sum()), "mean": float(np.mean(fits.truth[mask]))})
        else:
            shares = {str(c): float(np.mean(fits.truth[mask] == c)) for c in fits.classes}
            rows.append({"period": label, "rows": int(mask.sum()), "shares": shares})
    return rows


def pooled(windows: list[dict], model: str) -> dict:
    """A model's gap averaged over the windows: the mean gap, its SD (the square root of the summed variances, over
    the k windows), the mean floor, and whether the contemporaneous model beat the constant in every window.
    """
    ss = [w[model] for w in windows if model in w]
    k = len(ss)
    sds = np.array([s["gap_sd"] for s in ss], dtype=float)
    return {
        "gap": float(np.mean([s["gap"] for s in ss])) if k else float("nan"),
        "gap_sd": float(np.sqrt(np.sum(sds**2)) / k) if k and np.all(np.isfinite(sds)) else float("inf"),
        "floor": float(np.mean([s["floor"] for s in ss])) if k else float("nan"),
        "skill": bool(k) and all(s["skill"] > 0 for s in ss),
    }


def _verdict(out: dict, models: list[str]) -> str:
    if not out["windows"]:
        return "not measurable"
    out["pooled"] = {m: pooled(out["windows"], m) for m in models}
    rc = out.get("recording_change")
    if rc and rc.get("counts"):
        return "not flat"
    if any(w[m]["verdict"] == "not flat" for w in out["windows"] for m in models if m in w):
        return "not flat"
    complete = [m for m in models if all(m in w for w in out["windows"])]  # a model seen in some windows only
    readings = [
        _window_verdict(p["gap"], p["gap_sd"], p["floor"], 1.0 if p["skill"] else 0.0)
        for m, p in out["pooled"].items()
        if m in complete
    ]
    if "not flat" in readings:  # no window alone shows it, all of them together do
        return "not flat"
    return "flat" if "flat" in readings else "inconclusive"


def _set_verdict(out: dict, models: list[str]) -> None:
    """``out["verdict"]``, or ``partial`` (with ``partial_verdict``) when the windows miss one of the newest."""
    verdict = _verdict(out, models)
    tested = {w["test_period"] for w in out["windows"]}
    untested = [p for p in out.get("newest", []) if p not in tested]
    out.pop("partial_verdict", None)
    out["untested"] = untested
    if untested and verdict != "not flat":  # a not-flat window stands on its own
        out["partial_verdict"] = verdict
        verdict = "partial"
    out["verdict"] = verdict


def combine_runs(results: list[dict]) -> dict:
    """One verdict from runs of the test on the same data, each on some of the windows (one job per window): the
    windows joined (a period tested twice keeps its first run) and the verdict read again.
    """
    if not results:
        raise ValueError("combine_runs: no runs")
    first = results[0]
    if any(r["periods"] != first["periods"] or r.get("newest") != first.get("newest") for r in results):
        raise ValueError("combine_runs: the runs are not on the same periods")
    seen: dict[str, dict] = {}
    for r in results:
        for w in r["windows"]:
            seen.setdefault(w["test_period"], w)
    order = {p: i for i, p in enumerate(first["periods"])}
    out = {**first, "windows": sorted(seen.values(), key=lambda w: -order[w["test_period"]])}
    models = ["lightgbm"] + (["foundation"] if any("foundation" in w for w in out["windows"]) else [])
    _set_verdict(out, models)
    return out


def stationary_relation_lines(result: dict) -> list[str]:
    """The test's report: one line per window and model, the recording check and the verdict."""
    names = {"lightgbm": "LightGBM", "foundation": result.get("foundation") or "foundation model"}
    lines = [f"stationary relation: {len(result['windows'])} window(s) of {len(result['periods'])} periods"]
    for w in result["windows"]:
        for m in ("lightgbm", "foundation"):
            if m not in w:
                continue
            s = w[m]
            lines.append(
                f"  {w['test_period']}: {names[m]} forward {s['forward']:.4f}, "
                f"contemporaneous {s['contemporaneous']:.4f}, constant {s['constant']:.4f}; "
                f"gap {s['gap']:+.4f} ± {s['gap_sd']:.4f}, floor {s['floor']:.4f}: "
                f"{s['verdict']}"
            )
    rc = result.get("recording_change")
    if rc:
        lines.append(
            f"  largest class-share change: {rc['class']} {rc['low_share']:.1%} ({rc['low']}) to "
            f"{rc['high_share']:.1%} ({rc['high']}), factor {rc['factor']:.1f}, p {rc['p']:.2g}: "
            f"{'a change in recording' if rc['counts'] else 'not counted'}"
        )
    if result["verdict"] == "partial":
        lines.append(
            f"  verdict: partial ({result['partial_verdict']} on these windows; untested of the newest: "
            f"{', '.join(result['untested'])}; combine the runs with combine_runs)"
        )
    else:
        lines.append(f"  verdict: {result['verdict']}")
    return lines


def tabpfn_v35(problem_type: str, classes, *, device: str = "cuda") -> Foundation:
    """TabPFN v3.5 (the public ``tabpfn`` package with the public Hugging Face weights ``Prior-Labs/tabpfn_3_5``) as a
    ``Foundation``: one of the state-of-the-art foundation models a time basis can quote (SPLIT-32).

    Categories go in as their codes, named as categorical features; dates are already days. Classification returns
    the probability columns in the order of ``classes`` (a class missing from a training side scores 0), regression
    the mean. Run it on a GPU, on a node started through SkyPilot: v3.5 on a CPU is refused, as it is too slow there.
    Raises ``ImportError`` without the package.
    """
    if device == "cpu":
        raise ValueError("tabpfn_v35: run TabPFN v3.5 on a GPU (device='cuda'), not on a CPU")
    from tabpfn import TabPFNClassifier, TabPFNRegressor  # noqa: PLC0415 - an optional dependency
    from tabpfn.constants import ModelVersion  # noqa: PLC0415

    regression = problem_type == "regression"
    position = None if regression else {c: i for i, c in enumerate(classes)}

    def fit_predict(x_tr: pd.DataFrame, y_tr: np.ndarray, x_te: pd.DataFrame, seed: int) -> np.ndarray:
        both = pd.concat([x_tr, x_te], ignore_index=True)  # one coding of each category for both sides
        cat_idx, columns = [], {}
        for i, c in enumerate(both.columns):
            s = both[c]
            if isinstance(s.dtype, pd.CategoricalDtype):
                columns[c] = s.cat.codes.astype(float).where(s.notna())
                cat_idx.append(i)
            else:
                columns[c] = pd.to_numeric(s, errors="coerce").astype(float)
        X = pd.DataFrame(columns).to_numpy(dtype=np.float32)
        n = len(x_tr)
        estimator = TabPFNRegressor if regression else TabPFNClassifier
        model = estimator.create_default_for_version(
            ModelVersion.V3_5,
            device=device,
            ignore_pretraining_limits=True,
            random_state=seed,
            categorical_features_indices=cat_idx or None,
        )
        model.fit(X[:n], np.asarray(y_tr))
        if regression:
            return np.asarray(model.predict(X[n:]), dtype=float)
        proba = np.asarray(model.predict_proba(X[n:]), dtype=float)
        out = np.zeros((len(x_te), len(position)))
        for j, c in enumerate(model.classes_):
            out[:, position[c]] = proba[:, j]
        return out

    return fit_predict


def kumo_tabular(
    problem_type: str,
    classes,
    *,
    device: str = "cpu",
    threads: int | None = None,
    num_estimators: int = 8,
    size: str = "large",
    point: str = "mean",
) -> Foundation:
    """NVIDIA's Kumo-Tabular (``structured-data-models``, imported here) as a ``Foundation``: one of the
    state-of-the-art foundation models a time basis can quote (SPLIT-32).

    Classification returns the probability columns in the order of ``classes``; regression the mean (``point="mean"``)
    or the median of its 999 quantiles. A column empty on a training side is left out of that fit. Raises
    ``ImportError`` without the package.
    """
    import sdm  # noqa: PLC0415 - an optional dependency
    import torch  # noqa: PLC0415

    if threads:
        torch.set_num_threads(threads)
    regression = problem_type == "regression"
    model = sdm.models.KumoTabular(size=size, device=device)
    names = None if regression else [str(c) for c in classes]

    def fit_predict(x_tr: pd.DataFrame, y_tr: np.ndarray, x_te: pd.DataFrame, seed: int) -> np.ndarray:
        keep = [c for c in x_tr.columns if x_tr[c].notna().any()]
        both = pd.concat([x_tr[keep], x_te[keep]], ignore_index=True)
        y = pd.Series(np.concatenate([np.asarray(y_tr), np.asarray(y_tr)[:1].repeat(len(x_te))]))
        both["__target__"] = y.to_numpy(dtype=float) if regression else y.astype(str).to_numpy()
        stypes = sdm.infer_stypes(both, overrides={"__target__": "numerical" if regression else "categorical"})
        table = sdm.TableTensor.from_pandas(df=both, stypes=stypes, device=device)
        n = len(x_tr)
        model.fit(
            x=table[:n].drop_columns("__target__"),
            y=table[:n, "__target__"],
            num_estimators=num_estimators,
            generator=torch.Generator().manual_seed(seed),
        )
        pred = model.predict(table[n:].drop_columns("__target__")).to_pandas()
        model.clear()
        if regression:
            q = pred[[c for c in pred.columns if str(c).startswith("q")]].to_numpy(dtype=float)
            return np.median(q, axis=1) if point == "median" else q.mean(axis=1)
        probs = np.column_stack(
            [pred[c].to_numpy(dtype=float) if c in pred.columns else np.zeros(len(pred)) for c in names]
        )
        return probs / np.clip(probs.sum(axis=1, keepdims=True), 1e-12, None)

    return fit_predict
