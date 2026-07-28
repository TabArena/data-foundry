"""Work with the git-native curation backlog programmatically.

The curation backlog (formerly a Google Sheet) lives as one markdown record per
candidate dataset under ``curation/records/``. This example shows how to read,
filter, edit, and snapshot it from code — the same surface the local dashboard
(``data-foundry-curation serve``) and an LLM agent use.

Run with::

    python examples/curation_records.py
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from data_foundry.curation import (
    CurationRecord,
    load_all,
    load_record,
    load_vocabularies,
    save_record,
)
from data_foundry.curation.exporter import to_dataframe


def main() -> None:
    """Load, filter, edit-round-trip, and snapshot the curation backlog."""
    records = load_all()
    print(f"Loaded {len(records)} curation records.")

    # Filter: datasets already integrated into Data Foundry.
    integrated = [r for r in records if "DF: Yes" in r.data_foundry_status]
    print(f"  {len(integrated)} marked 'DF: Yes'.")

    # Filter: records carrying dropdown values not in the vocabulary (need cleanup).
    vocab = load_vocabularies()
    needs_review = [r for r in records if r.unknown_vocab_values(vocab)]
    print(f"  {len(needs_review)} need review (unmapped dropdown values).")

    if integrated:
        print("\nExample record:\n")
        print(integrated[0].describe())

    # Edit + persist round-trip (into a throwaway dir so the repo stays clean).
    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        draft = CurationRecord(
            unique_name="example_dataset",
            name="Example Dataset",
            checked_by=["Lennart"],
            data_foundry_status=["WIP (DF)"],
            suggestion="Yes",
            tags=["New IID"],
            problem_type="Regression",
            comments="A scratch record created by the example.",
        )
        path = save_record(draft, tmp_dir)
        reloaded = load_record(path)
        assert reloaded == draft
        print(f"\nSaved + reloaded a draft record at {path.name} (round-trips cleanly).")

    # One-way snapshot to a flat table (what the exporter / read-only Sheet uses).
    df = to_dataframe(records)
    print(f"\nFlat snapshot: {df.shape[0]} rows x {df.shape[1]} columns.")


if __name__ == "__main__":
    main()
