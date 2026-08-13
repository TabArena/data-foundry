"""Re-run all notebooks referenced in _tmp_state_paths_bad_dtypes.py and update UUIDs in final_uuid_list.py."""

from __future__ import annotations

import json
import re
import subprocess
import sys
import time
from pathlib import Path

# Resolve the data-foundry root (script now lives under scripts/beyond_arena/).
ROOT = Path(__file__).resolve().parent.parent.parent
BEYOND_IID = ROOT / "datasets" / "beyond_iid"
STATE_PATHS_FILE = BEYOND_IID / "final_uuid_list.py"
PROGRESS_FILE = BEYOND_IID / "_rerun_progress.json"

UUID_RE = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")

# Category mapping: list name -> subdirectory
CATEGORY_MAP = {
    "OLD_IID": "old_iid",
    "NEW_IID": "new_iid",
    "TEMPORAL": "temporal",
    "GROUPED": "grouped",
}


def load_entries() -> list[tuple[str, str, str]]:
    """Load entries from _tmp_state_paths_bad_dtypes.py. Returns (list_name, entry, old_uuid)."""
    sys.path.insert(0, str(BEYOND_IID))
    from _tmp_state_paths_bad_dtypes import GROUPED, NEW_IID, OLD_IID, TEMPORAL

    entries = []
    for list_name, items in [("OLD_IID", OLD_IID), ("NEW_IID", NEW_IID), ("TEMPORAL", TEMPORAL), ("GROUPED", GROUPED)]:
        for entry in items:
            parts = entry.split("/")
            if "/versions/" in entry:
                old_uuid = parts[-1]  # name/versions/uuid
            else:
                old_uuid = parts[-1]  # name/uuid
            entries.append((list_name, entry, old_uuid))
    return entries


def entry_to_notebook_path(entry: str, category: str) -> Path:
    """Map an entry string to its notebook path."""
    parts = entry.split("/")
    name = parts[0]
    is_versioned = "/versions/" in entry
    nb_name = f"{name}_1m.ipynb" if is_versioned else f"{name}.ipynb"

    nb_path = BEYOND_IID / category / name / nb_name
    if nb_path.exists():
        return nb_path

    raise FileNotFoundError(f"Notebook not found for {entry} in {category}: tried {nb_path}")


def execute_notebook(nb_path: Path, timeout_seconds: int = 3600) -> None:
    """Execute notebook in-place using papermill."""
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "papermill",
            str(nb_path),
            str(nb_path),
            "--cwd",
            str(nb_path.parent),
            "--execution-timeout",
            str(timeout_seconds),
            "--no-progress-bar",
        ],
        capture_output=True,
        text=True,
        timeout=timeout_seconds + 120,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Notebook execution failed:\nSTDOUT: {result.stdout[-2000:]}\nSTDERR: {result.stderr[-2000:]}")


def extract_uuid_from_notebook(nb_path: Path) -> str:
    """Extract the new UUID from the last cell's output."""
    with open(nb_path) as f:
        nb = json.load(f)

    # Find the last code cell (skip any trailing markdown)
    last_code_cell = None
    for cell in reversed(nb["cells"]):
        if cell.get("cell_type") == "code":
            last_code_cell = cell
            break

    if last_code_cell is None:
        raise ValueError(f"No code cell found in {nb_path}")

    # Collect all text output from the last code cell
    all_text_lines = []
    for output in last_code_cell.get("outputs", []):
        if output.get("output_type") == "stream" and "text" in output:
            all_text_lines.extend(output["text"])

    # Find the first line that is purely a UUID
    for line in all_text_lines:
        stripped = line.strip()
        if UUID_RE.fullmatch(stripped):
            return stripped

    raise ValueError(f"No UUID found in output of {nb_path}. Output lines: {all_text_lines}")


def load_progress() -> dict:
    """Load progress from JSON file."""
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE) as f:
            return json.load(f)
    return {"completed": {}, "failed": {}}


def save_progress(progress: dict) -> None:
    """Save progress to JSON file."""
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f, indent=2)


def main():
    entries = load_entries()
    progress = load_progress()
    state_content = STATE_PATHS_FILE.read_text()

    total = len(entries)
    completed_count = 0
    failed_count = 0
    skipped_count = 0

    print(f"Total entries to process: {total}")
    print(f"Already completed: {len(progress['completed'])}")
    print(f"Previously failed: {len(progress['failed'])}")
    print()

    try:
        for i, (list_name, entry, old_uuid) in enumerate(entries, 1):
            # Skip already completed
            if entry in progress["completed"]:
                skipped_count += 1
                continue

            category = CATEGORY_MAP[list_name]

            try:
                nb_path = entry_to_notebook_path(entry, category)
            except FileNotFoundError as e:
                print(f"[{i}/{total}] SKIP (not found): {entry} - {e}")
                progress["failed"][entry] = {"error": str(e), "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")}
                failed_count += 1
                save_progress(progress)
                continue

            print(f"[{i}/{total}] Running: {entry} -> {nb_path.relative_to(ROOT)}")
            t0 = time.time()

            try:
                execute_notebook(nb_path)
                new_uuid = extract_uuid_from_notebook(nb_path)
                elapsed = time.time() - t0

                # Update state file content
                state_content = state_content.replace(old_uuid, new_uuid)

                # Record progress
                progress["completed"][entry] = {
                    "old_uuid": old_uuid,
                    "new_uuid": new_uuid,
                    "notebook": str(nb_path.relative_to(ROOT)),
                    "elapsed_seconds": round(elapsed, 1),
                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
                }
                # Remove from failed if previously failed
                progress["failed"].pop(entry, None)
                completed_count += 1

                print(f"  OK ({elapsed:.1f}s): {old_uuid} -> {new_uuid}")

            except Exception as e:
                elapsed = time.time() - t0
                print(f"  FAILED ({elapsed:.1f}s): {e}")
                progress["failed"][entry] = {
                    "error": str(e)[:500],
                    "notebook": str(nb_path.relative_to(ROOT)),
                    "elapsed_seconds": round(elapsed, 1),
                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
                }
                failed_count += 1

            # Save progress after each notebook
            save_progress(progress)

    except KeyboardInterrupt:
        print("\nInterrupted! Saving progress...")
    finally:
        # Write updated state file
        STATE_PATHS_FILE.write_text(state_content)
        save_progress(progress)

    print(f"\nDone! Completed: {completed_count}, Failed: {failed_count}, Skipped: {skipped_count}")
    if progress["failed"]:
        print("\nFailed notebooks:")
        for entry, info in progress["failed"].items():
            print(f"  {entry}: {info.get('error', 'unknown')[:200]}")


if __name__ == "__main__":
    main()
