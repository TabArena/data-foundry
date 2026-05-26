"""Download a single curated container from Hugging Face via Data Foundry.

Each official collection knows where its containers live. For BeyondArena
that is the ``TabArena/BeyondArena`` Hub dataset; calling ``get_dataset``
downloads only the requested container (not the whole repo) and caches it.

The cache directory is resolved in this order:
    explicit `cache_dir=...` argument
    > $DATA_FOUNDRY_CACHE
    > ~/.cache/data_foundry/<collection-name>/

Run::

    # Default: use ~/.cache/data_foundry/BeyondArena.
    python examples/download_from_huggingface.py

    # Pin a specific cache directory.
    python examples/download_from_huggingface.py /tmp/my_cache

    # Or set $DATA_FOUNDRY_CACHE before invoking the example.
"""

from __future__ import annotations

import sys
from pathlib import Path

from data_foundry.collections import BEYOND_ARENA


def main(cache_dir: Path | None) -> None:
    print(f"Fetching one container from {BEYOND_ARENA.source!r}")
    print(f"Cache override: {cache_dir}")

    # Look up by `unique_name` (or UUID — both work).
    container = BEYOND_ARENA.get_dataset("airfoil_self_noise", cache_dir=cache_dir)

    print(f"\nLoaded `{container.dataset_metadata.unique_name}`")
    print(f"  uuid:        {container.uuid}")
    print(f"  checksum:    {container.checksum[:16]}...")
    print(f"  shape:       {container.dataset.shape}")
    print(f"  target:      {container.task_metadata.target_column_name}")
    print(f"  loaded from: {container.loaded_from_path}")
    container.dataset_metadata.local_data_directory_base = "/home/lennart_priorlabs_ai/code/large_data_ensemble/data-foundry/local-data-warehouse"

    # Verify that the checksum matches the on-disk data (recompute it from the files).
    assert container.checksum == container._create_checksum(), "Checksum mismatch! The on-disk data may be corrupted."

if __name__ == "__main__":
    override = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    main(override)
