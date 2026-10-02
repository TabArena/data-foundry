"""Build (or check) every v2 dataset of a folder in parallel, one ``build_one.py`` process per dataset.

Usage, from the repository root::

    .venv/bin/python .claude/skills/rebuild-working-copy/scripts/build_all.py <out_dir>
        [--root datasets/_dev/tabarena-v0pt2] [--jobs 16] [--previous <dir>] [--check-only] [--only a,b,...]

Each dataset writes ``<out_dir>/<name>.json`` (see ``build_one.py``) and ``<name>.log``; this prints one line per
finished dataset. ``--previous`` is the out_dir of an earlier run: its build times order the datasets longest first,
so the largest builds do not start last. Memory is the limit, not cores: the largest dataset (maps_router_eta_1m)
peaks at about 172 GB, the next ones at 58, 39 and 28 GB. The definitions with ``prepared_raw_files`` also trace their
``_prepare_raw_files`` inputs (``prepare_read``) on a full build, which takes acquire_valued_shoppers_challenge to about
145 GB.

For the check against a minimal warehouse, point ``DATA_FOUNDRY_WAREHOUSE`` at it and pass ``--check-only``.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _order(names: list[str], previous: Path | None) -> list[str]:
    if previous is None:
        return sorted(names)
    seconds = {}
    for name in names:
        f = previous / f"{name}.json"
        seconds[name] = json.loads(f.read_text()).get("seconds", 0) if f.exists() else 0
    return sorted(names, key=lambda n: (-seconds[n], n))


def _definitions(root: Path) -> list[str]:
    return sorted(p.parent.name for p in root.glob("*/dataset.py"))


def _prepares(root: Path, name: str) -> bool:
    return "prepared_raw_files" in (root / name / "dataset.py").read_text()


def main() -> int:
    """Run build_one.py for every dataset, a few at a time."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("out_dir", type=Path)
    parser.add_argument("--root", type=Path, default=Path("datasets/_dev/tabarena-v0pt2"))
    parser.add_argument("--jobs", type=int, default=16)
    parser.add_argument("--previous", type=Path, help="An earlier out_dir, to start the longest builds first.")
    parser.add_argument("--check-only", action="store_true", help="Run `check` without saving (no UUID).")
    parser.add_argument("--only", help="Comma-separated unique names; default: every definition under --root.")
    args = parser.parse_args()

    names = args.only.split(",") if args.only else _definitions(args.root)
    args.out_dir.mkdir(parents=True, exist_ok=True)

    def run(name: str) -> str:
        command = [sys.executable, str(HERE / "build_one.py"), name, str(args.out_dir / f"{name}.json")]
        command += ["--root", str(args.root)]
        if args.check_only:
            command.append("--check-only")
        elif _prepares(args.root, name):
            command.append("--trace-prepare")
        with (args.out_dir / f"{name}.log").open("w") as log:
            subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, check=False)
        lines = (args.out_dir / f"{name}.log").read_text().strip().splitlines()
        return lines[-1] if lines else f"{name}: no output"

    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures = [pool.submit(run, name) for name in _order(names, args.previous)]
        for i, future in enumerate(as_completed(futures), start=1):
            print(f"[{i}/{len(futures)}] {future.result()}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
