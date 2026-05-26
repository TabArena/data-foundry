"""Survey the official collections, then pre-download every BeyondArena container.

This example walks the full lifecycle of an official collection:

1. enumerate which collections ship with data_foundry,
2. inspect ``BEYOND_ARENA`` (counts, versioned entries, first few pointers),
3. warm the cache up front with :meth:`DatasetCollection.prefetch` — one
   bulk download pass before any container is loaded,
4. iterate the now-warm cache via :meth:`DatasetCollection.iter_containers`
   and verify each container's stored checksum against the on-disk data.

Run::

    # Default cache (~/.cache/data_foundry/BeyondArena).
    python examples/download_all_beyond_arena_datasets.py

    # Pin a specific cache directory.
    python examples/download_all_beyond_arena_datasets.py /tmp/my_cache
"""

from __future__ import annotations

import sys
from pathlib import Path

from data_foundry.collections import BEYOND_ARENA, get_collection, list_collections
from tqdm import tqdm


def print_collection_overview() -> None:
    print("Available official collections:")
    for name in list_collections():
        coll = get_collection(name)
        print(f"  - {name:<14} ({len(coll):>3} containers) — {coll.description}")

    print()
    print(f"Inspecting `{BEYOND_ARENA.name}`:")
    print(f"  total entries:        {len(BEYOND_ARENA)}")
    print(f"  unique dataset names: {len(set(BEYOND_ARENA.unique_names))}")
    print(f"  versioned entries:    {sum(1 for e in BEYOND_ARENA if e.is_versioned)}")
    print("  first 3 entries:")
    for entry in BEYOND_ARENA.entries[:3]:
        print(f"    - {entry.unique_name}  uuid={entry.uuid}  versioned={entry.is_versioned}")


def main(cache_dir: Path | None) -> None:
    print_collection_overview()

    print()
    print(f"Pre-downloading {len(BEYOND_ARENA)} containers from {BEYOND_ARENA.source!r}")
    print(f"Cache override: {cache_dir}\n")

    # `prefetch` materializes every container on disk without parsing the data.
    # Fail fast on network errors here, before any training code runs.
    paths = BEYOND_ARENA.prefetch(cache_dir=cache_dir)
    print(f"Cached {len(paths)} containers (example path: {paths[0]}).\n")

    # Cache is now warm — this loop hits the local filesystem only.
    progress = tqdm(
        BEYOND_ARENA.iter_containers(cache_dir=cache_dir),
        total=len(BEYOND_ARENA),
        desc="Verifying",
        unit="container",
    )
    for container in progress:
        name = container.dataset_metadata.unique_name
        assert container.checksum == container._create_checksum(), (
            f"Checksum mismatch for `{name}` — cached data may be corrupted."
        )
        progress.write(
            f"  {name:<40} rows={container.dataset.shape[0]:>8}  "
            f"target={container.task_metadata.target_column_name}",
        )

    print(f"\nDone — {len(BEYOND_ARENA)} containers downloaded and verified.")


if __name__ == "__main__":
    override = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    main(override)
