"""The two measured priority factors of datasets with a definition: a gap in the benchmark and a good shape.

Usage::

    python .claude/skills/knowledge-data-foundry/scripts/priority_factors.py [NAME ...]
        [--root datasets/_dev/tabarena-v0pt2] [--records curation/records] [--json PATH]

A record's ``priority`` (1-5) weighs five factors (knowledge-curation ``selection.md``, "Priority"). Once a dataset has
a definition, two of them can be measured, and this script measures them the same way for every record:

* gap: the definition's domain, problem type or split regime is thin among the accepted datasets of the working copy,
  counted over their definitions (a folder whose record holds ``DF: Yes`` and that has no ``REVIEW.md``), so an empty
  record field hides no dataset. Thin as in ``benchmark_coverage.py``: a count of at most max(2, half the median
  count); the domain ``other`` is never thin.
* shape: about 1,000 units or more (groups, for a task predicted per group) and 5 features or more, with a feature
  type other than numeric or a grouped or temporal split.

The other three factors, a clear use case, a strong source and a known risk, are judgments from the source and the
open issues; whoever sets the priority writes them in the record. Without names, the script lists the records whose
folder has a ``REVIEW.md``: the records the review page shows. The output is a markdown table on stdout (record,
current priority, gap, shape and the facts behind them); ``--json PATH`` also writes the numbers.
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from collections import Counter
from pathlib import Path

from data_foundry.curation.store import load_all
from data_foundry.v2 import load_definition, read_report

DF_YES = "DF: Yes"
NEVER_THIN = frozenset({"other"})
"""Values that name no real category: never thin, left out of the median."""
FACTORS = ("domain", "problem_type", "regime")
FEATURE_TYPES = re.compile(r"Feature types: (\d+) categorical, (\d+) string, (\d+) datetime")
"""The README's count of the declared feature types (the target and the group column are not features)."""


def facts(folder: Path) -> dict | None:
    """The definition's domain, problem type and regime and the README's shape, or None before a first check."""
    front = read_report(folder / "README.md")
    types = FEATURE_TYPES.search((folder / "README.md").read_text()) if front else None
    if not front or not types:
        return None
    task, data = front["task"], front["data"]
    grouping = task.get("grouping") or {}
    per_group = task["split_regime"] == "grouped_non_iid" and grouping.get("prediction_unit") == "group"
    return {
        "domain": load_definition(folder / "dataset.py").domain,
        "problem_type": task["problem_type"],
        "regime": task["split_regime"],
        "units": grouping["n_groups"] if per_group else data["n_rows"],
        "features": data["n_features"],
        "non_numeric": [k for k, n in zip(("categorical", "string", "datetime"), types.groups()) if int(n)],
    }


def thin_values(accepted: list[dict]) -> dict[str, list[str]]:
    """Per factor the thin values among the accepted definitions."""
    thin = {}
    for key in FACTORS:
        counts = Counter(f[key] for f in accepted)
        seen = [n for v, n in counts.items() if v not in NEVER_THIN]
        limit = max(2.0, statistics.median(seen) / 2) if seen else 2.0
        thin[key] = sorted(v for v, n in counts.items() if n <= limit and v not in NEVER_THIN)
    return thin


def score(f: dict, thin: dict[str, list[str]]) -> dict:
    """The gap and shape factors of one definition, each 0 or 1, with the facts behind them."""
    gap = [f"{key} {f[key]}" for key in FACTORS if f[key] in thin[key]]
    good = f["units"] >= 1000 and f["features"] >= 5 and bool(f["non_numeric"] or f["regime"] != "iid")
    types = ", ".join(f["non_numeric"]) or "numeric only"
    return {
        "gap": int(bool(gap)),
        "gap_why": "; ".join(gap) or "no thin domain, problem type or regime",
        "shape": int(good),
        "shape_why": f"{f['units']:,} units, {f['features']:,} features, {types}, {f['regime']}",
    }


def measure(root: Path, records: Path, names: list[str] | None) -> dict:
    """The thin values and, per named record (or per record with a REVIEW.md), its two factors."""
    by_folder = {}
    for record in load_all(records):
        if record.v2_path:
            by_folder[Path(record.v2_path).parent.name] = record
    folders = sorted(p.parent for p in root.glob("*/dataset.py"))
    accepted = []
    for folder in folders:
        record = by_folder.get(folder.name)
        if record and DF_YES in record.data_foundry_status and not (folder / "REVIEW.md").exists():
            f = facts(folder)
            if f:
                accepted.append(f)
    thin = thin_values(accepted)
    if names is None:
        chosen = [f for f in folders if (f / "REVIEW.md").exists() and f.name in by_folder]
    else:
        wanted = {by_folder[f.name].unique_name: f for f in folders if f.name in by_folder}
        unknown = sorted(set(names) - set(wanted))
        if unknown:
            raise SystemExit(f"no folder for: {', '.join(unknown)}")
        chosen = [wanted[n] for n in names]
    rows = []
    for folder in chosen:
        record = by_folder[folder.name]
        f = facts(folder)
        row = {"name": record.unique_name, "folder": folder.name, "priority": record.priority}
        row.update(score(f, thin) if f else {"gap": None, "gap_why": "not checked yet", "shape": None, "shape_why": ""})
        rows.append(row)
    return {"accepted": len(accepted), "thin": thin, "records": rows}


def markdown(result: dict) -> str:
    """The table of the two factors per record, after the thin values they were measured against."""
    thin = "; ".join(f"{k}: {', '.join(v) or 'none'}" for k, v in result["thin"].items())
    lines = [
        f"Thin among the {result['accepted']} accepted definitions: {thin}.",
        "",
        "| record | priority | gap | shape | gap: why | shape: the facts |",
        "|---|---:|---:|---:|---|---|",
    ]
    for r in result["records"]:
        cells = [f"`{r['name']}`", r["priority"] or "", r["gap"], r["shape"], r["gap_why"], r["shape_why"]]
        lines.append("| " + " | ".join("" if c is None else str(c) for c in cells) + " |")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    """Print the factors; write them as JSON too when asked."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("names", nargs="*", help="Unique names; default: the records whose folder has a REVIEW.md.")
    parser.add_argument("--root", type=Path, default=Path("datasets/_dev/tabarena-v0pt2"))
    parser.add_argument("--records", type=Path, default=Path("curation/records"))
    parser.add_argument("--json", type=Path, help="Also write the result as JSON to this path.")
    args = parser.parse_args(argv)
    result = measure(args.root, args.records, args.names or None)
    print(markdown(result))
    if args.json:
        args.json.write_text(json.dumps(result, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
