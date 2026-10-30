"""Inspect release-boundary event rates across calendar windows and end buffers.

Example::

    python .claude/skills/knowledge-data-foundry/scripts/label_maturity.py <name> --built
        --positive-label '"Yes"' --reference-start 2018-08-01 --reference-end 2018-10-01
        --min-rate-ratio 0.9 --out /tmp/maturity.json

The reference and optional criterion are curator-chosen for the dataset. This reads
the canonical frame; it does not trim rows, change splits or establish label availability.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "knowledge-curation" / "scripts"))

import dataset_io
from curation_probes import label_maturity


def main(argv: list[str] | None = None) -> int:
    """Write the complete diagnostic to JSON, or print it when --out is absent."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("name")
    parser.add_argument("--root", type=Path, default=Path("datasets/_dev/tabarena-v0pt2"))
    parser.add_argument("--built", action="store_true", help="Read the container recorded in the generated README.")
    parser.add_argument("--time-on", help="Date column; defaults to the task's declared time column.")
    parser.add_argument("--positive-label", type=json.loads, required=True, help="JSON label, e.g. 1 or '\"default\"'.")
    parser.add_argument("--reference-start", required=True, help="Inclusive UTC calendar date.")
    parser.add_argument("--reference-end", required=True, help="Exclusive UTC calendar date.")
    parser.add_argument("--end", help="Exclusive release end; defaults to the day after the latest date.")
    parser.add_argument(
        "--windows", default="1,3,7,14,21,28,all", help="Comma-separated day counts; all = full history."
    )
    parser.add_argument("--buffers", default="0,3,7,14,21,28,31", help="Comma-separated nonnegative end-buffer days.")
    parser.add_argument("--min-rate-ratio", type=float, help="Optional case-specific screen, never a maturity verdict.")
    parser.add_argument("--out", type=Path)
    args = parser.parse_args(argv)
    data = dataset_io.load(args.name, args.root, built=args.built)
    if data.problem_type != "binary_classification":
        parser.error("This diagnostic requires a binary event-label task.")
    time_on = args.time_on or data.time_on
    if not time_on or time_on not in data.df:
        parser.error("Specify an existing date column with --time-on.")
    result = label_maturity.run(
        data.df[time_on],
        data.df[data.target],
        reference_start=args.reference_start,
        reference_end=args.reference_end,
        positive_label=args.positive_label,
        windows=[None if w == "all" else int(w) for w in args.windows.split(",")],
        buffers=[int(b) for b in args.buffers.split(",")],
        end=args.end,
        min_rate_ratio=args.min_rate_ratio,
    )
    result |= {
        "name": args.name,
        "origin": data.origin,
        "time_on": time_on,
        "target": data.target,
        "positive_label": args.positive_label,
    }
    text = json.dumps(result, indent=2, allow_nan=False) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text)
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
