"""Quick leak probes for one v2 dataset: what a model learns from the data that it should not.

Usage::

    python .claude/skills/knowledge-data-foundry/scripts/leak_probes.py <unique_name>
        [--root datasets/_dev/tabarena-v0pt2] [--splits 3] [--max-rows 50000] [--max-single-features 300]
        [--n-jobs 8] [--out DIR]
        [--time-on COLUMN] [--period D|W|M|Q|Y] [--tz ZONE] [--positive LABEL] [--tail N] [--period-only] [--raw]

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
kept as the time key is not one. How to read them: ``.claude/skills/knowledge-curation/references/leak_checks.md``.
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
            )
    out["raw_copies"] = leak.raw_copies(raw, raw_target)
    for line in leak.raw_lines(out):
        leak.say(line)
    if "fills" in out:
        leak.say(f"cells on a straight line between their neighbours (probe 18), per class: {out['fills'] or 'none'}")
    if rows is None:
        leak.say("removed rows and dropped columns (probes 19, 20): not run (no lineage)")
    return out


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
    args = parser.parse_args(argv)
    result = probe(args)
    if args.out:
        args.out.mkdir(parents=True, exist_ok=True)
        (args.out / f"{args.name}.json").write_text(json.dumps(result, indent=1, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
