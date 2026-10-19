"""Generated-data probes: is the target a formula or a rule set of the features, or were the columns drawn one by one?

Usage::

    python .claude/skills/knowledge-data-foundry/scripts/generated_probes.py <unique_name> ... [--all] [--built]
        [--jobs 8] [--out DIR]

Runs the checks of ``curation_probes.generated`` on each dataset's frame, with its group columns left out of the
features; ``.claude/skills/knowledge-curation/scripts/curation_probes/generated.py`` says what each check measures
and when it raises a flag (its ``check_frame`` runs them on any table, for data without a definition). ``--all``
probes every definition under ``--root``; ``--built`` reads the container recorded in each ``README.md``'s build
record instead of rebuilding the frame from the raw files; ``--jobs`` sets the datasets probed in parallel.
``--out DIR`` writes one JSON per dataset and ``summary.md`` there. A flag is a question, not a verdict; how to read
them: ``.claude/skills/knowledge-curation/references/task_probes.md`` (generated data).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1")
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "knowledge-curation" / "scripts"))

import dataset_io
from curation_probes import generated
from joblib import Parallel, delayed


def probe(name: str, root: Path, *, built: bool) -> dict:
    """Run the checks of ``curation_probes.generated`` on one dataset."""
    started = time.time()
    data = dataset_io.load(name, root, built=built)
    result = {"name": name, "origin": data.origin}
    result |= generated.check_frame(data.df, data.target, data.problem_type, data.group_cols)
    result["seconds"] = round(time.time() - started)
    return result


def _safe(name: str, root: Path, **kwargs) -> dict:
    try:
        return probe(name, root, **kwargs)
    except Exception as error:  # noqa: BLE001 - one failing dataset must not stop a sweep
        return {"name": name, "error": f"{type(error).__name__}: {error}"[:300], "flags": []}


def render(r: dict) -> str:
    """One line per dataset."""
    if "error" in r:
        return f"{r['name']}: error {r['error']}"
    if "exact_share" in r:
        detail = (
            f"exact {r['exact_share']:.1%} ({r['transform']}) vs shuffled {r['exact_share_shuffled']:.1%}, "
            f"{r['terms']} terms on {r['n_fit']} rows"
        )
    elif "pure_minority_share" in r:
        detail = (
            f"rule leaves cover {r['pure_minority_share']:.1%} of the minority rows ({len(r['rule_leaves'])} leaves)"
        )
    else:
        detail = r.get("skipped", "")
    if "pair_share" in r:
        detail += (
            f"; columns: {r['pair_share']:.1%} of {r['pairs']} pairs dependent, "
            f"{r['uniform_columns']} of {r['uniform_tested']} uniform"
        )
    if "class_pair_share" in r:
        detail += (
            f"; within {r['classes']} classes: {r['class_pair_share']:.1%} of {r['class_pairs']} pairs dependent, "
            f"{r['class_uniform_columns']} of {r['class_uniform_tested']} uniform"
        )
    return f"{r['name']} ({r['problem_type']}, {r['rows']} rows): {detail}; flags {r['flags']}"


def main(argv: list[str] | None = None) -> int:
    """Probe the datasets; see the module docstring."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("names", nargs="*")
    parser.add_argument("--all", action="store_true", help="Probe every definition under --root.")
    parser.add_argument("--root", type=Path, default=Path("datasets/_dev/tabarena-v0pt2"))
    parser.add_argument("--built", action="store_true", help="Read the built containers (README build record).")
    parser.add_argument("--jobs", type=int, default=1, help="Datasets probed in parallel.")
    parser.add_argument("--out", type=Path, help="Write one JSON per dataset and summary.md here.")
    args = parser.parse_args(argv)
    names = dataset_io.dataset_names(args.root) if args.all else args.names
    if not names:
        parser.error("name at least one dataset, or pass --all")
    results = Parallel(n_jobs=args.jobs)(delayed(_safe)(n, args.root, built=args.built) for n in names)
    for r in results:
        print(render(r))
    if args.out:
        args.out.mkdir(parents=True, exist_ok=True)
        for r in results:
            (args.out / f"{r['name']}.json").write_text(json.dumps(r, indent=1, default=str))
        lines = [f"- {render(r)}" for r in sorted(results, key=lambda r: (not r["flags"], r["name"]))]
        (args.out / "summary.md").write_text("\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
