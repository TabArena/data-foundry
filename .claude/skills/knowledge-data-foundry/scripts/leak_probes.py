"""Quick leak probes for one v2 dataset: what a model learns from the data that it should not.

Usage::

    python .claude/skills/knowledge-data-foundry/scripts/leak_probes.py <unique_name>
        [--root datasets/_dev/tabarena-v0pt2] [--splits 3] [--max-rows 50000] [--max-single-features 300]
        [--n-jobs 8] [--out DIR]

Rebuilds the frame and the split plan from ``<root>/<unique_name>/dataset.py`` and runs the leak probes of
``curation_probes.leak`` (``.claude/skills/knowledge-curation/scripts/curation_probes/leak.py`` says what each number
measures) on the first ``--splits`` shipped splits: untuned LightGBM with ``--n-jobs`` threads, train and test rows
capped at ``--max-rows`` each, at most ``--max-single-features`` columns (and missing patterns) fitted one by one, and
the definition's group columns left out of the features. ``--out DIR`` also writes the numbers to
``DIR/<unique_name>.json``. The numbers are indicative (untuned models, a few splits) and meant for comparing the
shipped data with a suspected fix. How to read them: ``.claude/skills/knowledge-curation/references/leak_checks.md``.
The probes use the shipped target; when the definition changed the target (merged, dropped or binned classes), run
the same checks on the source's labels in ``explore.ipynb`` as well (section 1 of that file).
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "knowledge-curation" / "scripts"))
import dataset_io
from curation_probes import leak


def probe(args: argparse.Namespace) -> dict:
    """Print the probes for one dataset and return their numbers; see the module docstring."""
    started = time.time()
    data = dataset_io.from_definition(dataset_io.definition(args.name, args.root))
    result = leak.run(
        data.df,
        data.target,
        data.problem_type,
        data.flat_splits(),
        group_cols=data.group_cols,
        name=args.name,
        n_splits=args.splits,
        max_rows=args.max_rows,
        max_single_features=args.max_single_features,
        n_jobs=args.n_jobs,
    )
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
    args = parser.parse_args(argv)
    result = probe(args)
    if args.out:
        args.out.mkdir(parents=True, exist_ok=True)
        (args.out / f"{args.name}.json").write_text(json.dumps(result, indent=1, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
