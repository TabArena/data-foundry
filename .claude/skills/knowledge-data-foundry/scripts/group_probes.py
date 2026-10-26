"""Group probes for one grouped v2 dataset: does the grouping matter, and is there signal across groups?

Usage::

    python .claude/skills/knowledge-data-foundry/scripts/group_probes.py <unique_name>
        [--root datasets/_dev/tabarena-v0pt2] [--repeats 3] [--permutations 100] [--max-rows 200000] [--n-jobs 8]

Rebuilds the frame and the split plan from ``<root>/<unique_name>/dataset.py`` and runs the group probes of
``curation_probes.groups`` (``.claude/skills/knowledge-curation/scripts/curation_probes/groups.py`` says what each
number measures) on the grouping's columns and the shipped grouped splits: the first ``--repeats`` repeats,
``--permutations`` runs of the permutation test when the labels are one per group (``Grouping(labels="per_group")``),
a random set of whole groups when the frame has more than ``--max-rows`` rows, and ``--n-jobs`` processes. A
definition without a grouping is no grouped task (exit code 1). The numbers are indicative (untuned models) and meant
for the curation decision; how to read them: ``.claude/skills/knowledge-curation/references/leak_checks.md`` (probe 11).
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1")
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "knowledge-curation" / "scripts"))

import dataset_io
from curation_probes import groups


def main(argv: list[str] | None = None) -> int:
    """Print the probes for one dataset; see the module docstring."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("name")
    parser.add_argument("--root", default="datasets/_dev/tabarena-v0pt2")
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--permutations", type=int, default=100)
    parser.add_argument("--max-rows", type=int, default=200_000)
    parser.add_argument("--n-jobs", type=int, default=8)
    args = parser.parse_args(argv)

    ds = dataset_io.definition(args.name, args.root)
    if ds.task_metadata.grouping is None:
        print(f"{args.name} is not a grouped task.")
        return 1
    data = dataset_io.from_definition(ds)
    groups.run(
        data.df,
        data.target,
        data.problem_type,
        data.group_cols,
        data.repeats(),
        per_group_labels=data.grouping.labels == "per_group",
        name=args.name,
        n_repeats=args.repeats,
        permutations=args.permutations,
        max_rows=args.max_rows,
        n_jobs=args.n_jobs,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
