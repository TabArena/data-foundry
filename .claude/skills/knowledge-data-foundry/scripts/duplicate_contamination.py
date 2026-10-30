"""Count exact training-profile matches, label conflicts and multiplicity on every shipped fold.

Example::

    python .claude/skills/knowledge-data-foundry/scripts/duplicate_contamination.py <name> --built
        --out /tmp/copies.json

No model fits or dataset edits. Optional --losses reads a packet with frame_digest
and folds, each containing ordered train_indices, test_indices and per-row losses.
Obtain frame_digest from a run on the same frame first; verify the prediction artifact's
data/model/scorer provenance before constructing that packet. The tool validates frame
and split alignment, not the provenance of supplied model losses.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "knowledge-curation" / "scripts"))

import dataset_io
from curation_probes import duplicate_contamination


def main(argv: list[str] | None = None) -> int:
    """Write counts and optional aligned-loss summaries without fitting a model."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("name")
    parser.add_argument("--root", type=Path, default=Path("datasets/_dev/tabarena-v0pt2"))
    parser.add_argument("--built", action="store_true", help="Read the container recorded in the generated README.")
    parser.add_argument(
        "--exclude", nargs="*", default=[], help="Explicit extra predictor exclusions, recorded in output."
    )
    parser.add_argument("--losses", type=Path, help="Optional frame/split-bound JSON packet of per-test-row losses.")
    parser.add_argument("--row-details", action="store_true", help="Also export test positions and exact match counts.")
    parser.add_argument("--out", type=Path)
    args = parser.parse_args(argv)
    data = dataset_io.load(args.name, args.root, built=args.built)
    if set(args.exclude) - set(data.df):
        parser.error("Every excluded column must exist in the frame.")
    excluded = {data.target, *data.group_cols, *args.exclude}
    declared = data.feature_cols
    features = [c for c in (declared if declared is not None else data.df.columns) if c not in excluded]
    losses = json.loads(args.losses.read_text()) if args.losses else None
    result = duplicate_contamination.run(
        data.df,
        data.target,
        data.flat_splits(),
        features=features,
        losses=losses,
        include_rows=args.row_details,
    )
    for row, (repeat, fold) in zip(result["folds"], ((r, f) for r in data.splits for f in data.splits[r]), strict=True):
        row.update({"repeat": str(repeat), "fold": str(fold)})
    result |= {
        "name": args.name,
        "origin": data.origin,
        "target": data.target,
        "extra_excluded": args.exclude,
        "group_columns_excluded": data.group_cols,
        "scoring_columns_excluded": list(data.scoring_cols),
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
