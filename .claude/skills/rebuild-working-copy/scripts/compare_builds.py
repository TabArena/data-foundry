"""Summarise a ``build_all.py`` run and compare it with the previous one.

Usage, from the repository root::

    .venv/bin/python .claude/skills/rebuild-working-copy/scripts/compare_builds.py <out_dir>
        [--previous <dir>] [--base-ref HEAD] [--root datasets/_dev/tabarena-v0pt2] [--expect-checksums <dir>]

Reports, and writes to ``<out_dir>/summary.json``:

* the status of each dataset (ok, errors, crash) with the crash message and the error slugs;
* for a full build, whether every saved container reloads and its stored checksum equals the recomputed one;
* the warnings that are new against the committed ``README.md`` frontmatter at ``--base-ref`` and against the
  ``--previous`` run (a run before an ``accepted_check_warnings`` entry still lists the warning it accepts);
* the datasets whose rows, splits or read raw files changed against ``--previous``;
* with ``--expect-checksums`` (the full build's out_dir), the datasets whose checksum differs from it: the check of a
  rebuild from a minimal warehouse;
* the summed build time and the peak memory.
"""

from __future__ import annotations

import argparse
import contextlib
import io
import json
import subprocess
import sys
from pathlib import Path

import yaml


def _results(directory: Path) -> dict[str, dict]:
    return {f.stem: json.loads(f.read_text()) for f in sorted(directory.glob("*.json")) if f.stem != "summary"}


def _committed_warnings(root: Path, name: str, ref: str) -> set[str] | None:
    out = subprocess.run(["git", "show", f"{ref}:{root}/{name}/README.md"], capture_output=True, text=True, check=False)
    if out.returncode != 0 or not out.stdout.startswith("---"):
        return None
    front = yaml.safe_load(out.stdout.split("---", 2)[1]) or {}
    checks = front.get("bundle_checks") or {}
    return set(checks.get("warnings", [])) | set(checks.get("errors", []))


def _verify(saved_path: str) -> bool:
    from data_foundry.curation_container import CuratedContainer  # noqa: PLC0415 - only for full builds
    from data_foundry.schema import resolve_warehouse_dir  # noqa: PLC0415

    with contextlib.redirect_stdout(io.StringIO()):
        container = CuratedContainer.load(resolve_warehouse_dir() / saved_path)
    return container.verify()


def main() -> int:
    """Print the comparison and write summary.json."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("out_dir", type=Path)
    parser.add_argument("--previous", type=Path)
    parser.add_argument("--base-ref", default="HEAD")
    parser.add_argument("--root", type=Path, default=Path("datasets/_dev/tabarena-v0pt2"))
    parser.add_argument("--expect-checksums", type=Path, help="The full build's out_dir, for a minimal-warehouse run.")
    args = parser.parse_args()

    results = _results(args.out_dir)
    previous = _results(args.previous) if args.previous else {}
    expected = _results(args.expect_checksums) if args.expect_checksums else {}
    rows = []
    for name, r in results.items():
        warnings = sorted(w for w, _ in r.get("warnings", []))
        committed = _committed_warnings(args.root, name, args.base_ref)
        before = previous.get(name, {})
        row = {
            "name": name,
            "status": "crash" if "crash" in r else ("ok" if r.get("ok") else "errors"),
            "crash": r.get("crash"),
            "errors": [e for e, _ in r.get("errors", [])],
            "warnings": warnings,
            "new_vs_committed": None if committed is None else sorted(set(warnings) - committed),
            "new_vs_previous": sorted(set(warnings) - {w for w, _ in before.get("warnings", [])}) if before else None,
            "shape_changed": bool(before)
            and (before.get("rows"), before.get("splits")) != (r.get("rows"), r.get("splits")),
            "read_changed": bool(before) and set(before.get("read", [])) != set(r.get("read", [])),
            "format_version": r.get("format_version"),
            "verified": _verify(r["saved_path"]) if r.get("saved_path") else None,
            "checksum_as_expected": (r.get("checksum") == expected[name].get("checksum")) if name in expected else None,
            "seconds": r.get("seconds"),
            "max_rss_gb": r.get("max_rss_gb"),
        }
        rows.append(row)
    (args.out_dir / "summary.json").write_text(json.dumps(rows, indent=1))

    def names(pred) -> list[str]:
        return [r["name"] for r in rows if pred(r)]

    print(f"{len(rows)} datasets: {len(names(lambda r: r['status'] == 'ok'))} ok")
    for r in rows:
        if r["status"] != "ok":
            print(f"  {r['name']}: {r['status']} {r['errors']} {(r['crash'] or '')[:200]}")
    print("format versions:", sorted({r["format_version"] for r in rows}, key=str))
    print("reload verification failed:", names(lambda r: r["verified"] is False))
    print(
        "new warnings vs committed READMEs:", {r["name"]: r["new_vs_committed"] for r in rows if r["new_vs_committed"]}
    )
    print("no committed README:", names(lambda r: r["new_vs_committed"] is None))
    if previous:
        print("new warnings vs previous run:", {r["name"]: r["new_vs_previous"] for r in rows if r["new_vs_previous"]})
        print("rows or splits changed:", names(lambda r: r["shape_changed"]))
        print("raw files read changed:", names(lambda r: r["read_changed"]))
        missing = sorted(set(previous) - set(results))
        print(f"missing from this run: {len(missing)}", missing if len(missing) <= 20 else "(a partial run)")
    if expected:
        print("checksum differs from the full build:", names(lambda r: r["checksum_as_expected"] is False))
    open_warnings = [w for r in rows for w in r["warnings"]]
    print(f"open warnings: {len(open_warnings)} in {len(names(lambda r: r['warnings']))} datasets")
    print(
        f"build time (sum): {sum(r['seconds'] or 0 for r in rows)} s; peak memory: "
        f"{max((r['max_rss_gb'] or 0) for r in rows)} GB"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
