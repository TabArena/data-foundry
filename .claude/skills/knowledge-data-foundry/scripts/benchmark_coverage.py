"""Benchmark coverage: what the accepted datasets cover, per domain, problem type, regime and original source.

Usage::

    python .claude/skills/knowledge-data-foundry/scripts/benchmark_coverage.py [--json PATH]
        [--records curation/records] [--vocab curation/vocabularies.yaml]

A record counts as accepted when its ``suggestion`` is ``Yes`` or ``Yes (Disagreement)``, or its
``data_foundry_status`` holds ``DF: Yes``, and its ``suggestion`` is not ``No (Retired)``. For each of ``domain``,
``problem_type``, ``required_split`` (the regime) and ``original_source`` the script counts the accepted datasets per
value and marks a value thin when its count is at most max(2, half the median count over the values seen in that
field). A vocabulary value of ``domain``, ``problem_type`` or ``required_split`` that no accepted dataset has is listed
as thin with a count of 0. An empty field counts under ``(empty)``; it and the placeholders (``?``, ``TBD``,
``Custom``, ``Other``) are shown but never thin and left out of the median, and so are the out-of-scope domains
(handcrafted, multimedia). A record with two regimes in
``required_split`` counts once under each.

The output is a set of markdown tables on stdout; ``--json PATH`` also writes the numbers. Thin values are where
screening finds the datasets the benchmark lacks; they are priorities for the curator, not verdicts.
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from collections import Counter
from pathlib import Path

from data_foundry.curation._paths import records_dir, vocabularies_path
from data_foundry.curation.record import ACCEPTED_SUGGESTIONS, RETIRED_SUGGESTION, CurationRecord, load_vocabularies
from data_foundry.curation.store import load_all

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
THIN_RULE = (
    "a value is thin when its count is at most max(2, half the median count over the values seen in that field); "
    "a vocabulary value with no accepted dataset is thin with count 0 (domain, problem_type, required_split); "
    "(empty), the placeholders ?, TBD, Custom, Other and the out-of-scope domains (handcrafted, multimedia) are "
    "never thin and stay out of the median"
)


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
        real = {value for value in counts if value != EMPTY and value not in PLACEHOLDERS | OUT_OF_SCOPE}
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
                if v not in counts and v not in PLACEHOLDERS | OUT_OF_SCOPE
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


def main(argv: list[str] | None = None) -> int:
    """Count the accepted set's coverage; see the module docstring."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--records", type=Path, default=None, help="Records folder (default: curation/records).")
    parser.add_argument("--vocab", type=Path, default=None, help="Vocabularies (default: curation/vocabularies.yaml).")
    parser.add_argument("--json", type=Path, help="Also write the numbers as JSON here.")
    args = parser.parse_args(argv)

    records = load_all(args.records or records_dir())
    vocab = load_vocabularies(args.vocab or vocabularies_path())
    result = coverage(records, vocab)
    print(render(result), end="")
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(result, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
