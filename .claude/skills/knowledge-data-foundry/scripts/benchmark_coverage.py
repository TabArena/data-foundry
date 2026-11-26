"""Benchmark coverage and the measured priority factors: what the accepted datasets cover, what a new one adds.

Usage::

    python .claude/skills/knowledge-data-foundry/scripts/benchmark_coverage.py coverage [--json PATH]
        [--records curation/records] [--vocab curation/vocabularies.yaml]
    python .claude/skills/knowledge-data-foundry/scripts/benchmark_coverage.py priority [NAME ...] [--json PATH]
        [--root datasets/_dev/tabarena-v0pt2] [--records curation/records]

Both count the accepted datasets per value and mark a value thin when its count is at most max(2, half the median
count over the values seen in that field) (``thin_threshold``). The placeholders (``?``, ``TBD``, ``Custom``,
``Other``), an empty field (``(empty)``) and the out-of-scope domains (handcrafted, multimedia) are never thin and
stay out of the median (``never_thin``, case-insensitive). Thin values are where screening finds the datasets the
benchmark lacks; they are priorities for the curator, not verdicts.

``coverage`` reads the records. A record counts as accepted when its ``suggestion`` is ``Yes`` or ``Yes
(Disagreement)``, or its ``data_foundry_status`` holds ``DF: Yes``, and its ``suggestion`` is not ``No (Retired)``.
It counts ``domain``, ``problem_type``, ``required_split`` (the regime) and ``original_source``; a vocabulary value of
the first three that no accepted dataset has is listed as thin with a count of 0, and a record with two regimes in
``required_split`` counts once under each. The output is a set of markdown tables.

``priority`` measures two of the five factors of a record's ``priority`` (knowledge-curation ``selection.md``,
"Priority") for datasets with a definition, the same way for every record:

* gap: the definition's domain, problem type or split regime is thin among the accepted definitions of the working
  copy (a folder whose record holds ``DF: Yes``), counted over the definitions, so an empty record field hides no
  dataset;
* shape: about 1,000 units or more (groups, for a task predicted per group) and 5 features or more, with a feature
  type other than numeric or a grouped or temporal split.

The other three factors, a clear use case, a strong source and a known risk, are judgments from the source and the
open issues; whoever sets the priority writes them in the record. Without names, ``priority`` lists the records whose
review (``## Review``) has something open: the records the review page shows. The output is a markdown table (record,
current priority, gap, shape and the facts behind them). ``--json PATH`` also writes the numbers of either.
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from collections import Counter
from pathlib import Path

from data_foundry.curation._paths import records_dir, vocabularies_path
from data_foundry.curation.record import ACCEPTED_SUGGESTIONS, RETIRED_SUGGESTION, CurationRecord, load_vocabularies
from data_foundry.curation.review import is_settled, read_reviews
from data_foundry.curation.store import load_all
from data_foundry.definition import load_definition, read_report

FIELDS: tuple[str, ...] = ("domain", "problem_type", "required_split", "original_source")
"""The record fields the coverage is counted over."""
VOCAB_FIELDS: tuple[str, ...] = ("domain", "problem_type", "required_split")
"""Fields whose vocabulary values without an accepted dataset are listed as thin."""
PLACEHOLDERS: frozenset[str] = frozenset({"?", "TBD", "Custom", "Other"})
"""Values that name no real category: never thin, left out of the median."""
OUT_OF_SCOPE: frozenset[str] = frozenset(
    {"handcrafted", "handcrafted/toy", "multimedia", "Multimedia (from non-tabular modalities)"}
)
"""Domains whose datasets are out of scope (selection.md, SEL-12 and SEL-16): never a gap to fill, so never thin."""
EMPTY = "(empty)"
DF_YES = "DF: Yes"
_NEVER_THIN = {v.lower() for v in PLACEHOLDERS | OUT_OF_SCOPE | {EMPTY}}
THIN_RULE = (
    "a value is thin when its count is at most max(2, half the median count over the values seen in that field); "
    "a vocabulary value with no accepted dataset is thin with count 0 (domain, problem_type, required_split); "
    "(empty), the placeholders ?, TBD, Custom, Other and the out-of-scope domains (handcrafted, multimedia) are "
    "never thin and stay out of the median"
)


def never_thin(value: str) -> bool:
    """A placeholder, an empty field or an out-of-scope domain, in any case: never thin, left out of the median."""
    return str(value).lower() in _NEVER_THIN


def is_accepted(record: CurationRecord) -> bool:
    """Whether the record is in the accepted set: a ``Yes`` verdict or ``DF: Yes``, and not retired."""
    if record.suggestion == RETIRED_SUGGESTION:
        return False
    return record.suggestion in ACCEPTED_SUGGESTIONS or DF_YES in record.data_foundry_status


def _values(record: CurationRecord, field: str) -> list[str]:
    value = getattr(record, field)
    if isinstance(value, list):
        return [v for v in value if v] or [EMPTY]
    return [value] if value else [EMPTY]


def thin_threshold(counts: list[int]) -> float:
    """The largest count that is still thin: max(2, half the median of ``counts``)."""
    return max(2.0, statistics.median(counts) / 2) if counts else 2.0


def coverage(records: list[CurationRecord], vocab: dict[str, list[str]]) -> dict:
    """The accepted set's counts per field value, with the thin marks and the datasets behind each value."""
    accepted = [r for r in records if is_accepted(r)]
    fields: dict[str, dict] = {}
    for field in FIELDS:
        names: dict[str, list[str]] = {}
        for record in accepted:
            for value in _values(record, field):
                names.setdefault(value, []).append(record.unique_name)
        counts = Counter({value: len(members) for value, members in names.items()})
        real = {value for value in counts if not never_thin(value)}
        seen = [counts[value] for value in real]
        threshold = thin_threshold(seen)
        rows = [
            {
                "value": value,
                "count": n,
                "share": round(n / len(accepted), 4) if accepted else 0.0,
                "thin": value in real and n <= threshold,
                "in_vocabulary": value in vocab.get(field, []),
                "datasets": sorted(names[value]),
            }
            for value, n in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
        ]
        if field in VOCAB_FIELDS:
            rows += [
                {"value": v, "count": 0, "share": 0.0, "thin": True, "in_vocabulary": True, "datasets": []}
                for v in vocab.get(field, [])
                if v not in counts and not never_thin(v)
            ]
        fields[field] = {
            "median": statistics.median(seen) if seen else 0,
            "thin_threshold": threshold,
            "values": rows,
        }
    return {"accepted": len(accepted), "records": len(records), "thin_rule": THIN_RULE, "fields": fields}


def render(result: dict, *, max_names: int = 8) -> str:
    """The coverage as markdown tables, one per field."""
    lines = [
        "# Benchmark coverage",
        "",
        f"{result['accepted']} accepted datasets of {result['records']} records (suggestion `Yes` or "
        "`Yes (Disagreement)`, or `DF: Yes`; not `No (Retired)`).",
        "",
        f"Thin: {result['thin_rule']}.",
    ]
    for field, data in result["fields"].items():
        thin = [row for row in data["values"] if row["thin"]]
        lines += [
            "",
            f"## {field}",
            "",
            f"Median count {data['median']:g}, thin at {data['thin_threshold']:g} or fewer; "
            f"{len(thin)} thin of {len(data['values'])} values.",
            "",
            "| value | count | share | thin | datasets (thin values) |",
            "|---|---:|---:|---|---|",
        ]
        for row in data["values"]:
            names = ""
            if row["thin"] and row["datasets"]:
                shown = ", ".join(f"`{n}`" for n in row["datasets"][:max_names])
                more = len(row["datasets"]) - max_names
                names = shown + (f" and {more} more" if more > 0 else "")
            vocab_note = "" if row["in_vocabulary"] or row["value"] == EMPTY else " (not in vocabulary)"
            lines.append(
                f"| {row['value']}{vocab_note} | {row['count']} | {row['share']:.1%} | "
                f"{'thin' if row['thin'] else ''} | {names} |"
            )
        total = sum(row["count"] for row in data["values"])
        note = " (a record with several regimes counts under each)" if field == "required_split" else ""
        lines.append(f"| **total**{note} | {total} | | | |")
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------- priority factors
FACTORS = ("domain", "problem_type", "regime")
FEATURE_TYPES = re.compile(r"Feature types: ((?:\d+ [a-z]+)(?:, \d+ [a-z]+)*)")
"""The README's count of the declared feature types (the target and the group column are not features): categorical,
an ordinal count only where a dataset has an ordinal column, string and datetime, then any special features."""
TYPED = ("categorical", "ordinal", "string", "datetime")
"""The declared feature types other than numeric, in the README's order."""


def feature_type_counts(readme: str) -> dict[str, int] | None:
    """The README's count per declared feature type, or None when it has no ``Feature types`` line."""
    line = FEATURE_TYPES.search(readme)
    if not line:
        return None
    return {kind: int(n) for n, kind in (pair.split(" ") for pair in line.group(1).split(", "))}


def facts(folder: Path) -> dict | None:
    """The definition's domain, problem type and regime and the README's shape, or None before a first check."""
    front = read_report(folder / "README.md")
    types = feature_type_counts((folder / "README.md").read_text()) if front else None
    if not front or types is None:
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
        "non_numeric": [k for k in TYPED if types.get(k)],
    }


def thin_values(accepted: list[dict]) -> dict[str, list[str]]:
    """Per factor the thin values among the accepted definitions."""
    thin = {}
    for key in FACTORS:
        counts = Counter(f[key] for f in accepted)
        limit = thin_threshold([n for v, n in counts.items() if not never_thin(v)])
        thin[key] = sorted(v for v, n in counts.items() if n <= limit and not never_thin(v))
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


def open_reviews(records: Path) -> set[str]:
    """The records whose review has something open for the curator (``review.is_settled``)."""
    return {r.name for r in read_reviews(records) if not is_settled(r, records)}


def measure(root: Path, records: Path, names: list[str] | None) -> dict:
    """The thin values and, per named record (or per record with an open review), its two factors."""
    by_folder = {}
    for record in load_all(records):
        if record.v2_path:
            by_folder[Path(record.v2_path).parent.name] = record
    folders = sorted(p.parent for p in root.glob("*/dataset.py"))
    accepted = []
    for folder in folders:
        record = by_folder.get(folder.name)
        if record and DF_YES in record.data_foundry_status:
            f = facts(folder)
            if f:
                accepted.append(f)
    thin = thin_values(accepted)
    if names is None:
        open_review = open_reviews(records)
        chosen = [f for f in folders if f.name in by_folder and by_folder[f.name].unique_name in open_review]
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
    """``coverage``: the accepted set per field value; ``priority``: the gap and shape factors per record."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest="command", required=True)
    cov = commands.add_parser("coverage", help="The accepted datasets per domain, problem type, regime and source.")
    cov.add_argument("--records", type=Path, default=None, help="Records folder (default: curation/records).")
    cov.add_argument("--vocab", type=Path, default=None, help="Vocabularies (default: curation/vocabularies.yaml).")
    cov.add_argument("--json", type=Path, help="Also write the numbers as JSON here.")
    pri = commands.add_parser("priority", help="The gap and shape factors of datasets with a definition.")
    pri.add_argument("names", nargs="*", help="Unique names; default: the records whose review has something open.")
    pri.add_argument("--root", type=Path, default=Path("datasets/_dev/tabarena-v0pt2"))
    pri.add_argument("--records", type=Path, default=Path("curation/records"))
    pri.add_argument("--json", type=Path, help="Also write the result as JSON to this path.")
    args = parser.parse_args(argv)

    if args.command == "coverage":
        result = coverage(load_all(args.records or records_dir()), load_vocabularies(args.vocab or vocabularies_path()))
        print(render(result), end="")
    else:
        result = measure(args.root, args.records, args.names or None)
        print(markdown(result))
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(result, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
