"""Hidden groups: columns, keys of all columns but one and near copies that carry the label, and a random split's gain.

Usage::

    python .claude/skills/knowledge-data-foundry/scripts/hidden_groups.py <unique_name> ... [--all] [--built] [--jobs 8]
        [--out DIR] [--include-grouped]

Runs the hidden-group probe of ``curation_probes.hidden_groups``
(``.claude/skills/knowledge-curation/scripts/curation_probes/hidden_groups.py`` says what it measures and when a
candidate is a hit) on each dataset: an IID task gets the split gaps; a temporal task (``Temporal(on=...)``) gets the
recurrence of its entities across the shipped splits instead, with its time column left out of the candidates; a
grouped task is skipped. ``--include-grouped`` also runs the grouped datasets as if they were IID (their known group
column is marked, and left out of the near-copy tokens and the composite keys; a key with the same groups is marked as
the known group): the positive controls for the thresholds. ``--all`` probes every definition under ``--root``;
``--built`` reads the container recorded in each ``README.md``'s build record instead of rebuilding the frame from the
raw files. ``--n-jobs`` sets the threads per model and ``--jobs`` the datasets probed in parallel. ``--out DIR`` writes
one JSON per dataset and ``summary.md`` there. How to read the output:
``.claude/skills/knowledge-curation/references/task_probes.md`` (hidden groups).
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
from curation_probes import hidden_groups as hidden
from curation_probes.hidden_groups import COPY_MAX_CLUSTER, COPY_MIN_SHARED, N_TESTED, NEAR_COPIES
from joblib import Parallel, delayed


def probe(name: str, root: Path, *, built: bool, n_jobs: int, include_grouped: bool) -> dict:
    """Run the probe of ``curation_probes.hidden_groups`` on one dataset."""
    started = time.time()
    data = dataset_io.load(name, root, built=built)
    regime = "temporal" if data.time_on is not None else "grouped" if data.grouping is not None else "iid"
    result: dict = {"name": name, "regime": regime, "origin": data.origin}
    if regime == "grouped" and not include_grouped:
        return result | {"skipped": f"{regime} task"}
    result |= hidden.run(
        data.df,
        data.target,
        data.problem_type,
        known=data.group_cols,
        time_on=data.time_on,
        splits=data.flat_splits(),
        n_jobs=n_jobs,
    )
    result["seconds"] = round(time.time() - started)
    return result


def _outcome(c: dict) -> str:
    """The gap (IID) or the recurrence across the cutoff (temporal) of a candidate, as text."""
    if "gap" in c:
        return f", gap {c['gap']:+.3f} (random {c['skill_random']:.3f}, grouped {c['skill_grouped']:.3f})"
    if "test_rows_seen" in c and c["splits"]:
        low, high = c["test_rows_seen_range"]
        return f", test rows seen in train {c['test_rows_seen']:.1%} ({low:.1%}-{high:.1%}, {c['splits']} splits)"
    return ""


def _key_lines(result: dict) -> list[str]:
    """The composite keys of one dataset, or what the search checked when none counts."""
    search = result.get("composite_search")
    if not search:
        return []
    lines = []
    for c in result["composite_keys"]:
        mark = " [known group]" if c["known_group"] else ""
        lines.append(
            f"   {c['column']}{mark}: {c['values']} keys of {c['key_columns']} columns, "
            f"{c['mean_rows_per_value']} rows each, {c['varying_share']:.1%} of the rows share a key with a row "
            f"that differs ({c['baseline_share']:.1%} with independent columns), s_id {c['s_id']:.3f}{_outcome(c)}"
            + (
                f"; {c['rows_in_large_keys']} rows of keys over {COPY_MAX_CLUSTER} left out"
                if c["rows_in_large_keys"]
                else ""
            )
        )
    if search["left_out"]:
        scope = {1: "one column", 2: "one or two columns"}.get(max(search["left_out"]), "a few columns")
        best = f"; best {search['best']} {search['best_varying_share']:.1%}" if search["best"] else ""
        found = f"{search['counted']} count" if search["counted"] else "none counts"
        lines.append(
            f"   (keys of all but {scope}): {found} ({search['keys_checked']} of {search['keys']} keys, "
            f"{search['columns']} columns{best}), {search['seconds']} s"
        )
    else:
        lines.append(f"   (keys of all but one column): not searched ({search['columns']} columns)")
    return lines


def render(result: dict) -> str:
    """A short text summary of one dataset."""
    lines = [f"== {result['name']} ({result['regime']}, {result.get('rows', '?')} rows)"]
    if "skipped" in result or "error" in result:
        return lines[0] + f": {result.get('skipped') or result.get('error')}"
    if result["regime"] == "temporal":
        lines.append(f"   candidates {result['candidates']}; entity-like {result['entity_like']} (temporal: no hits)")
    else:
        lines.append(f"   candidates {result['candidates']}; hits {result['hits']}")
    for c in result["scored"][:N_TESTED]:
        mark = " [known group]" if c["known_group"] else ""
        lines.append(
            f"   {c['column']}{mark}: {c['values']} values, {c['mean_rows_per_value']} rows each, "
            f"s_id {c['s_id']:.3f}, s_smooth {c['s_smooth']:.3f}, "
            f"{c['static']} attributes {c['static_columns'][:4]}{_outcome(c)}"
        )
    lines.extend(_key_lines(result))
    c = result["near_copies"]
    ladder = ", ".join(f"{s['similarity']}: {s['clusters']} ({s['repeated_share']:.1%})" for s in c["ladder"])
    sizes = ", ".join(f"{k}: {v}" for k, v in c["cluster_sizes"].items() if v)
    left_out = []
    if c["rows_with_few_tokens"]:
        left_out.append(f"{c['rows_with_few_tokens']} rows with fewer than {COPY_MIN_SHARED} tokens")
    if c["rows_in_large_clusters"]:
        left_out.append(f"{c['rows_in_large_clusters']} rows of clusters over {COPY_MAX_CLUSTER}")
    lines.append(
        f"   {NEAR_COPIES} at {c['similarity']}: {c['values']} clusters, {c['repeated_share']:.1%} of the rows in "
        f"clusters of 2+, largest {c['largest']} (sizes {sizes or 'none'}), s_id {c['s_id']:.3f}{_outcome(c)}; "
        f"by similarity {ladder}; {c['columns_used']} columns, {c['seconds']} s"
        + "".join(f"; {note} left single" for note in left_out)
    )
    return "\n".join(lines)


def _safe(name: str, root: Path, **kwargs) -> dict:
    try:
        return probe(name, root, **kwargs)
    except Exception as error:  # noqa: BLE001 - one failing dataset must not stop a sweep
        return {"name": name, "regime": "?", "error": f"{type(error).__name__}: {error}"[:300]}


def _summary_row(r: dict) -> str:
    """One line of ``summary.md``."""
    if r.get("scored") is None:
        top = r.get("skipped") or r.get("error", "")
    else:
        parts = []
        for c in [*r["scored"][:1], *r.get("composite_keys", [])[:1], r["near_copies"]]:
            if "gap" in c:
                parts.append(f"{c['column']} gap {c['gap']:+.3f}")
            elif "test_rows_seen" in c:
                parts.append(f"{c['column']} seen {c['test_rows_seen']:.1%}")
            elif c["column"] == NEAR_COPIES:
                parts.append(f"{c['column']} {c['repeated_share']:.1%} of rows")
        top = "; ".join(parts)
    hits = ", ".join(r.get("hits", []))
    return f"| `{r['name']}` | {r['regime']} | {r.get('candidates', '')} | {hits} | {top} |"


def main(argv: list[str] | None = None) -> int:
    """Probe the datasets; see the module docstring."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("names", nargs="*")
    parser.add_argument("--all", action="store_true", help="Probe every definition under --root.")
    parser.add_argument("--root", type=Path, default=Path("datasets/_dev/tabarena-v0pt2"))
    parser.add_argument("--built", action="store_true", help="Read the built containers (README build record).")
    parser.add_argument("--include-grouped", action="store_true", help="Also run grouped tasks (positive controls).")
    parser.add_argument("--n-jobs", type=int, default=4, help="Threads per model.")
    parser.add_argument("--jobs", type=int, default=1, help="Datasets probed in parallel.")
    parser.add_argument("--out", type=Path, help="Write one JSON per dataset and summary.md here.")
    args = parser.parse_args(argv)
    names = dataset_io.dataset_names(args.root) if args.all else args.names
    if not names:
        parser.error("name at least one dataset, or pass --all")
    kwargs = {"built": args.built, "n_jobs": args.n_jobs, "include_grouped": args.include_grouped}
    results = Parallel(n_jobs=args.jobs)(delayed(_safe)(n, args.root, **kwargs) for n in names)
    for result in results:
        print(render(result))
    if args.out:
        args.out.mkdir(parents=True, exist_ok=True)
        for result in results:
            (args.out / f"{result['name']}.json").write_text(json.dumps(result, indent=1, default=str))
        header = "| dataset | regime | candidates | hits | top candidate; composite key; near copies |\n"
        header += "|---|---|---|---|---|\n"
        (args.out / "summary.md").write_text(header + "\n".join(_summary_row(r) for r in results) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
