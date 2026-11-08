"""Quick leak probes for one v2 dataset: what a model learns from the data that it should not.

Usage::

    python .claude/skills/knowledge-data-foundry/scripts/leak_probes.py <unique_name>
        [--root datasets/_dev/tabarena-v0pt2] [--splits 3] [--max-rows 50000] [--max-single-features 300]
        [--n-jobs 8] [--out DIR]
        [--time-on COLUMN] [--period D|W|M|Q|Y] [--tz ZONE] [--positive LABEL] [--tail N] [--period-only] [--raw]
    python .claude/skills/knowledge-data-foundry/scripts/leak_probes.py <unique_name> --weight-proxy
        [--weight-column COLUMN] [--objective metric|l2|OBJECTIVE] [--seeds 3] [--splits 3] [--max-rows 50000]
        [--n-jobs 8] [--out DIR]

Rebuilds the frame and the split plan from ``<root>/<unique_name>/dataset.py`` and runs the leak probes of
``curation_probes.leak`` (``.claude/skills/knowledge-curation/scripts/curation_probes/leak.py`` says what each number
measures) on the first ``--splits`` shipped splits: untuned LightGBM with ``--n-jobs`` threads, train and test rows
capped at ``--max-rows`` each, at most ``--max-single-features`` columns (and missing patterns) fitted one by one, and
the definition's group columns left out of the features. ``--out DIR`` also writes the numbers to
``DIR/<unique_name>.json``. The numbers are indicative (untuned models, a few splits) and meant for comparing the
shipped data with a suspected fix. For a classification task whose raw file is one table holding the target column,
it also counts, per column and class, the cells on a straight line between their neighbours in the raw file's order
(probe 18: gaps filled by interpolation). When the task has a time column (``--time-on`` names another), it sets the
target of the newest periods against the band of the earlier ones (probe 13, ``leak.target_by_period``, the test for
right-censoring at the release end); ``--period``, ``--tz``, ``--positive`` and ``--tail`` set its periods, timezone,
event class and tested periods, and ``--period-only`` runs probe 13 alone, without a model. Exact copies (probe 5) are
counted on every shipped split. ``--raw`` runs the probes of the raw state alone: the table ``_load_raw`` returns and,
through the lineage of ``process(lineage=True)``, what ``_clean`` did to it (probe 10, the target in the raw row order;
18, straight-line fills; 19, the rows ``_clean`` removed against the kept ones; 20, each dropped raw column alone on the
shipped splits; 21, copies before deduplication). The features are the definition's model inputs: a scoring column
kept as the time key is not one. A task with a training weight (``sample_weight``) is probed with it: every fit is
trained with it as each row's weight, and every R^2 and ROC AUC is weighted. ``--weight-proxy`` runs probe 22 alone
(``leak.weight_proxy``): whether the features carry the weight, on the task's sample weight or the column
``--weight-column`` names (a feature named there is taken out of the features for this probe; a scoring column is read
from the scoring columns), on the first ``--splits`` splits with ``--seeds`` LightGBM seeds each, every side capped at
``--max-rows`` random rows, scored by the declared metric. Its fits of the target are, by default (``--objective
metric``), the weighted actuarial fit: a deviance metric's own objective (LightGBM's Poisson objective, or Tweedie at
the metric's power); for any other metric on a task with a training weight, Poisson when every target times its weight
is a whole count (claims per year insured) and Tweedie at power 1.5 for any other non-negative rate (a cost per year
insured, scored by a Gini), on the original scale of a log-shipped target; L2 fits otherwise. ``--objective l2`` makes
them L2 fits on the shipped scale, and any other value is passed to LightGBM as the objective. LEAK-41 asks for both
the L2 and the actuarial fit and decides on the worse: when an actuarial fit exists, the output says to run the other
one. On a rate, L2 fits are noisy under a deviance
(bemtpl97, 20,000 rows: the weight as a feature gains +0.0005 with an SD of 0.0066 under L2, +0.0039 with an SD of
0.0013 under the Poisson fit). How to read them: ``.claude/skills/knowledge-curation/references/leak_checks.md``.
The probes use the shipped target; when the definition changed the target (merged, dropped or binned classes), run
the same checks on the source's labels in a scratch notebook as well (section 1 of that file).
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "knowledge-curation" / "scripts"))
import dataset_io
from curation_probes import leak


def target_by_period(data: dataset_io.ProbeInput, args: argparse.Namespace) -> dict | None:
    """Probe 13 on the task's time column (or ``--time-on``); None, with the reason printed, when it cannot run."""
    time_on = args.time_on or data.time_on
    if not time_on:
        leak.say("target by period (probe 13): not run (no time column; name one with --time-on)")
        return None
    if time_on not in data.df.columns:
        leak.say(f"target by period (probe 13): not run (no column {time_on!r})")
        return None
    try:
        return leak.target_by_period(
            data.df[time_on],
            data.df[data.target],
            data.problem_type,
            freq=args.period,
            tz=args.tz,
            positive=args.positive,
            tail=args.tail,
        )
    except ValueError as err:
        leak.say(f"target by period (probe 13): not run ({err})")
        return None


def raw_state(ds: object, data: dataset_io.ProbeInput, args: argparse.Namespace) -> dict:
    """The probes of the raw state (10, 18, 19, 20, 21; ``curation_probes.leak``): see the module docstring."""
    out: dict = {"lineage": data.raw_note}
    raw = data.raw
    if raw is None:
        leak.say(f"raw state: not run ({data.raw_note})")
        return out
    rows, target = data.raw_rows, data.target
    raw_target = target if target in raw.columns else None
    traced = data.raw_note if rows is not None else f"none ({data.raw_note})"
    leak.say(f"raw state: {len(raw):,} raw rows, {len(data.df):,} curated rows; lineage: {traced}")
    if rows is not None:
        out["row_order"] = leak.row_order(
            pd.Series(data.df[target].to_numpy(), index=rows).sort_index(kind="stable"), data.problem_type
        )
    elif raw_target is not None:
        out["row_order"] = leak.row_order(raw[raw_target], data.problem_type)
    if data.problem_type != "regression" and raw_target is not None:
        out["fills"] = leak.fill_counts(raw, raw_target)
    if rows is not None:
        kept = np.zeros(len(raw), dtype=bool)
        kept[rows] = True
        out["removed_rows"] = leak.removed_rows(raw[raw_target] if raw_target else None, kept, data.problem_type)
        curated = set(ds.df.columns)  # the curated columns before special features are encoded
        dropped = [c for c in raw.columns if c not in curated and c != raw_target]
        if dropped:
            rng = np.random.default_rng(0)
            cap = lambda idx: np.sort(rng.choice(idx, min(len(idx), args.max_rows), replace=False))
            pairs = [(cap(np.asarray(tr)), cap(np.asarray(te))) for tr, te in data.flat_splits()][: args.splits]
            out["dropped_columns"] = leak.dropped_column_proxies(
                raw.iloc[rows][dropped].reset_index(drop=True),
                data.df[target].reset_index(drop=True),
                pairs,
                regression=data.problem_type == "regression",
                n_jobs=args.n_jobs,
                weight=data.weights,
            )
    out["raw_copies"] = leak.raw_copies(raw, raw_target)
    for line in leak.raw_lines(out):
        leak.say(line)
    if "fills" in out:
        leak.say(f"cells on a straight line between their neighbours (probe 18), per class: {out['fills'] or 'none'}")
    if rows is None:
        leak.say("removed rows and dropped columns (probes 19, 20): not run (no lineage)")
    return out


DEVIANCE_OBJECTIVES = {
    "mean_poisson_deviance": "poisson",
    "mean_tweedie_deviance": "tweedie",
    "rescaled_mean_tweedie_deviance": "tweedie",
}
"""The LightGBM objective of each deviance metric: the weighted actuarial fit of ``--objective metric``."""


RATE_TWEEDIE_POWER = 1.5
"""The Tweedie power of the actuarial fit of a non-negative rate that is not a count, under a metric that is no
deviance (a cost per year insured scored by a Gini)."""


def rate_objective(rate: np.ndarray | None, weight: np.ndarray | None) -> str:
    """The weighted actuarial fit of a rate under a metric that is no deviance: ``poisson`` when every rate times its
    weight is a whole count (to 1e-6), ``tweedie`` for any other non-negative rate, ``l2`` without a training weight
    or with a negative or missing rate. ``rate`` is the target on its original scale.
    """
    if rate is None or weight is None:
        return "l2"
    rate, weight = np.asarray(rate, dtype=float), np.asarray(weight, dtype=float)
    if not (np.isfinite(rate).all() and (rate >= 0).all()):
        return "l2"
    count = rate * weight
    return "poisson" if np.allclose(count, np.round(count), rtol=0.0, atol=1e-6) else "tweedie"


def fit_params(
    objective: str, metric: dict | None, rate: np.ndarray | None = None, weight: np.ndarray | None = None
) -> dict | None:
    """The LightGBM parameters of probe 22's fits of the target for ``--objective``: None for an L2 fit; for
    ``metric``, the declared deviance's own objective (Tweedie at the metric's power), or for another metric the
    actuarial fit of the rate (``rate_objective`` on the target's original scale and the training weight), else L2.
    """
    power = (metric or {}).get("params", {}).get("power")
    if objective == "metric":
        name = metric["name"] if metric else ""
        if name in DEVIANCE_OBJECTIVES:
            objective = DEVIANCE_OBJECTIVES[name]
        else:
            objective, power = rate_objective(rate, weight), RATE_TWEEDIE_POWER
    if objective in ("l2", "regression"):
        return None
    params = {"objective": objective}
    if objective == "tweedie" and power is not None:
        params["tweedie_variance_power"] = float(power)
    return params


def original_rate(data: dataset_io.ProbeInput, metric: dict | None) -> np.ndarray | None:
    """The target of a regression task with a training weight on its original scale (a log-shipped target sent
    back), the rate ``rate_objective`` reads; None for any other task.
    """
    if data.problem_type != "regression" or data.weights is None:
        return None
    shipped = pd.to_numeric(data.df[data.target], errors="coerce").to_numpy(dtype=float)
    return leak._FROM_SHIPPED[(metric or {}).get("transform") or "identity"](shipped)


def weight_proxy(data: dataset_io.ProbeInput, args: argparse.Namespace) -> dict | None:
    """Probe 22 on the task's sample weight or ``--weight-column``; None, with the reason printed, when it cannot run.

    A column that is still a feature is taken out of the features for this probe; a scoring column (the metric's
    weight of a task without a sample weight) is read from the scoring columns.
    """
    column = getattr(args, "weight_column", None) or data.weight_column
    if not column:
        leak.say("weight proxy (probe 22): not run (the task has no sample_weight; name a column with --weight-column)")
        return None
    features = list(data.feature_cols) if data.feature_cols is not None else None
    if column in data.df.columns:
        values = data.df[column]
        if features is not None and column in features:
            features.remove(column)
            leak.say(f"weight proxy (probe 22): `{column}` is a feature; it is left out of the features here")
    elif data.scoring is not None and column in data.scoring.columns:
        values = data.scoring[column]
    else:
        leak.say(f"weight proxy (probe 22): not run (no column {column!r})")
        return None
    metric = data.declared_metric()
    rate = original_rate(data, metric)
    params = fit_params(getattr(args, "objective", "metric"), metric, rate, data.weights)
    try:
        result = leak.weight_proxy(
            data.df,
            data.target,
            data.problem_type,
            data.flat_splits(),
            pd.to_numeric(values, errors="coerce").to_numpy(dtype=float),
            sample_weight=data.weights,
            feature_cols=features,
            group_cols=data.group_cols,
            metric=metric,
            weight_name=column,
            name=args.name,
            n_splits=args.splits,
            max_rows=args.max_rows,
            seeds=tuple(range(getattr(args, "seeds", 3))),
            fit_params=params,
            n_jobs=args.n_jobs,
        )
    except ValueError as err:
        leak.say(f"weight proxy (probe 22): not run ({err})")
        return None
    if fit_params("metric", metric, rate, data.weights) is not None:  # LEAK-41 takes the worse of the two fits
        other = "metric for the weighted actuarial fit" if params is None else "l2 for the L2 fit"
        leak.say(f"  run again with --objective {other}: LEAK-41 decides on the worse of the two")
    return result


def probe(args: argparse.Namespace) -> dict:
    """Print the probes for one dataset and return their numbers; see the module docstring."""
    started = time.time()
    ds = dataset_io.definition(args.name, args.root)
    raw = getattr(args, "raw", False)  # a Namespace built by hand may not have it
    data = dataset_io.from_definition(ds, raw=True) if raw else dataset_io.from_definition(ds)
    if raw:
        result = {"name": args.name, "raw_state": raw_state(ds, data, args)}
        result["seconds"] = round(time.time() - started)
        return result
    if args.period_only:
        result = {"name": args.name, "target_by_period": target_by_period(data, args)}
        result["seconds"] = round(time.time() - started)
        return result
    if getattr(args, "weight_proxy", False):
        result = {"name": args.name, "weight_proxy": weight_proxy(data, args)}
        result["seconds"] = round(time.time() - started)
        return result
    result = leak.run(
        data.df,
        data.target,
        data.problem_type,
        data.flat_splits(),
        group_cols=data.group_cols,
        feature_cols=data.feature_cols,
        name=args.name,
        n_splits=args.splits,
        max_rows=args.max_rows,
        max_single_features=args.max_single_features,
        n_jobs=args.n_jobs,
        sample_weight=data.weights,
    )
    result["target_by_period"] = target_by_period(data, args)
    raw = ds.raw
    if data.problem_type != "regression" and isinstance(raw, pd.DataFrame) and data.target in raw.columns:
        result["fills"] = leak.fill_counts(raw, data.target)
        leak.say(
            "cells on a straight line between their neighbours (raw file order), per class: "
            f"{result['fills'] or 'none'}"
        )
    else:
        leak.say("straight-line fills: not run (a regression, or the raw file is not one table holding the target)")
    result["seconds"] = round(time.time() - started)
    return result


def main(argv: list[str] | None = None) -> int:
    """Print the probes for one dataset; see the module docstring."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("name")
    parser.add_argument("--root", default="datasets/_dev/tabarena-v0pt2")
    parser.add_argument("--splits", type=int, default=3)
    parser.add_argument("--max-rows", type=int, default=50_000)
    parser.add_argument(
        "--max-single-features", type=int, default=300, help="Columns (and missing patterns) fitted one by one."
    )
    parser.add_argument("--n-jobs", type=int, default=8, help="Threads per LightGBM model.")
    parser.add_argument("--out", type=Path, help="Also write the numbers to OUT/<name>.json.")
    parser.add_argument("--time-on", help="Probe 13's time column; default the task's.")
    parser.add_argument("--period", choices=leak.PERIOD_FREQS, help="Probe 13's calendar period; default chosen.")
    parser.add_argument("--tz", help="Probe 13's timezone: aware times are converted to it.")
    parser.add_argument("--positive", help="Probe 13's event class of a binary target; default the minority class.")
    parser.add_argument("--tail", type=int, help="Probe 13's newest periods tested; default a fifth, 2 to 8.")
    parser.add_argument("--period-only", action="store_true", help="Run probe 13 alone, without a model.")
    parser.add_argument("--raw", action="store_true", help="Run the probes of the raw state alone (10, 18-21).")
    parser.add_argument("--weight-proxy", action="store_true", help="Run probe 22 alone: do features carry the weight?")
    parser.add_argument("--weight-column", help="Probe 22's weight; default the task's sample weight.")
    parser.add_argument(
        "--objective",
        default="metric",
        help="Probe 22's fits of the target: metric (default: a deviance's own loss, else L2), l2, or an objective.",
    )
    parser.add_argument("--seeds", type=int, default=3, help="Probe 22's LightGBM seeds per split.")
    args = parser.parse_args(argv)
    result = probe(args)
    if args.out:
        args.out.mkdir(parents=True, exist_ok=True)
        (args.out / f"{args.name}.json").write_text(json.dumps(result, indent=1, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
