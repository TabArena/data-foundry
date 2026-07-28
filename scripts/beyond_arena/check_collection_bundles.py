"""Run the bundle checks over every container of a collection and report findings by check.

Use this to (a) audit an already-shipped collection and (b) calibrate a new check in
``data_foundry.bundle_checks`` before choosing its severity: a rule that fires on many
healthy datasets is noise, and a hard ``error`` must be reproducible on a real bundle.

Run from the repo root::

    python scripts/beyond_arena/check_collection_bundles.py                       # BeyondArena, via cache/HF
    python scripts/beyond_arena/check_collection_bundles.py --base-dir <warehouse>  # local warehouse
    python scripts/beyond_arena/check_collection_bundles.py --json findings.json

Containers are loaded one at a time (a full collection does not fit in memory).
"""

from __future__ import annotations

import argparse
import gc
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

from data_foundry.bundle_checks import SEVERITY_ORDER, run_bundle_checks
from data_foundry.collections import get_collection


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--collection", default="BeyondArena", help="Registered collection name.")
    parser.add_argument(
        "--base-dir",
        default=None,
        help="Load from this local warehouse instead of the collection's source (offline).",
    )
    parser.add_argument("--json", dest="json_path", default=None, help="Write all findings to this JSON file.")
    parser.add_argument("--examples", type=int, default=5, help="Findings to print per check (default 5).")
    parser.add_argument("--limit", type=int, default=None, help="Only check the first N containers (for a smoke run).")
    parser.add_argument(
        "--heavy-cell-budget",
        type=int,
        default=None,
        help="Override the cell budget for the O(rows x cols) checks.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    collection = get_collection(args.collection)
    findings: dict[str, list[str]] = defaultdict(list)
    severities: dict[str, str] = {}
    counts: Counter[str] = Counter()

    check_kwargs = {} if args.heavy_cell_budget is None else {"heavy_cell_budget": args.heavy_cell_budget}
    entries = collection.entries[: args.limit] if args.limit else collection.entries

    for i, entry in enumerate(entries, start=1):
        print(f"[{i}/{len(entries)}] {entry.unique_name}", file=sys.stderr, flush=True)
        try:
            container = (
                entry.load(args.base_dir) if args.base_dir is not None else collection.get_dataset(entry.uuid)
            )
        except Exception as error:  # noqa: BLE001 - one broken container must not stop the audit
            counts["load_failed"] += 1
            findings["container_load_failed"].append(f"{entry.unique_name}: {type(error).__name__}: {error}")
            continue

        report = run_bundle_checks(container, verbose=False, **check_kwargs)
        counts["clean" if report.ok else "with_errors"] += 1
        for result in report.results:
            severities[result.slug] = result.severity
            findings[result.slug].append(f"{container.dataset_metadata.unique_name}: {result.message}")
        del container, report
        gc.collect()

    print(f"\n{len(entries)} container(s): {dict(counts)}\n")
    for slug in sorted(findings, key=lambda s: (SEVERITY_ORDER.get(severities.get(s, "error"), 0), -len(findings[s]))):
        print(f"## [{severities.get(slug, 'error')}] {slug}: {len(findings[slug])}")
        for message in findings[slug][: args.examples]:
            print(f"   - {message}")
        if len(findings[slug]) > args.examples:
            print(f"   … {len(findings[slug]) - args.examples} more")
        print()

    if args.json_path:
        payload = {"counts": dict(counts), "severities": severities, "findings": findings}
        Path(args.json_path).write_text(json.dumps(payload, indent=2))
        print(f"Wrote {args.json_path}")

    return 1 if counts["with_errors"] or counts["load_failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
