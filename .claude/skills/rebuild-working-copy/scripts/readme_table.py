"""Write the dataset table of the working copy's README.md from each folder's generated README frontmatter.

Usage, from the repository root::

    .venv/bin/python .claude/skills/rebuild-working-copy/scripts/readme_table.py [--root datasets/_dev/tabarena-v0pt2]

The table (regime, rows, features, splits, UUID, open warnings) goes between the ``<!-- datasets:start -->`` and
``<!-- datasets:end -->`` markers of ``<root>/README.md``; a folder without a build, or whose README is stale, shows
"not built". Run it after a rebuild and whenever a dataset is added, removed or rebuilt.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from data_foundry.v2 import read_report

START, END = "<!-- datasets:start -->", "<!-- datasets:end -->"
REGIME = {"iid": "IID", "temporal_non_iid": "temporal", "grouped_non_iid": "grouped"}


def table(root: Path) -> str:
    """The markdown table of every dataset folder under ``root``."""
    rows = [
        "| dataset | regime | rows | features | splits | UUID | open warnings |",
        "|---|---|---|---|---|---|---|",
    ]
    for folder in sorted(p for p in root.iterdir() if (p / "dataset.py").is_file()):
        front = read_report(folder / "README.md")
        if not front:
            rows.append(f"| [`{folder.name}`]({folder.name}/) | | | | | not built | |")
            continue
        task, data, splits = front["task"], front["data"], front["splits"]
        regime = REGIME.get(task["split_regime"], task["split_regime"])
        grouping = task.get("grouping") or {}
        if grouping.get("prediction_unit") == "group":
            regime += f" (per group: {grouping['aggregation']})"
        build = front.get("build") or {}
        uuid = f"`{build['uuid']}`" if build and not front.get("build_stale") else "not built"
        warnings = ", ".join(f"`{w}`" for w in front["bundle_checks"]["warnings"])
        rows.append(
            f"| [`{folder.name}`]({folder.name}/) | {regime} | {data['n_rows']:,} | {data['n_features']:,} | "
            f"{splits['n_repeats']} x {splits['n_folds']} | {uuid} | {warnings} |"
        )
    return "\n".join(rows)


def main() -> int:
    """Write the table into the README between its markers."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", type=Path, default=Path("datasets/_dev/tabarena-v0pt2"))
    args = parser.parse_args()

    path = args.root / "README.md"
    text = path.read_text()
    block = f"{START}\n{table(args.root)}\n{END}"
    if START in text:
        text = text[: text.index(START)] + block + text[text.index(END) + len(END) :]
    else:
        text = text.rstrip() + "\n\n" + block + "\n"
    path.write_text(text)
    print("table written:", text.count("\n| [`"), "datasets")
    return 0


if __name__ == "__main__":
    sys.exit(main())
