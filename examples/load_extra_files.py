"""Detect and resolve extra (non-core) artifacts shipped next to a :class:`CuratedContainer`.

Data Foundry persists six core files per container (dataset + dtypes + container metadata
+ three pydantic-tagged metadata blobs) and optionally a test-dataset pair. Producers may
also ship arbitrary sidecar files in the same directory — embedding caches, per-fold
prediction archives, dataset documentation, etc.

Data Foundry does not interpret these files. It exposes just enough to discover them and
resolve their path so the caller can load them with whatever library is appropriate
(``pd.read_parquet``, ``json.load``, ``np.load``, …).

The toy container shipped with the package includes one such extra: ``toy_extra.parquet``.

Run::

    python examples/load_extra_files.py
    python examples/load_extra_files.py /path/to/warehouse/<name>/<uuid>
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
from data_foundry.curation_container import CuratedContainer
from data_foundry.examples import get_toy_container_path


def main(path: Path) -> None:
    """List the container's extra files and load the first one as a DataFrame."""
    container = CuratedContainer.load(path)

    extras = container.list_extra_files()
    print(f"Extra files present in {path}:")
    for name in extras:
        print(f"  - {name}")
    if not extras:
        print("  (none)")
        return

    target = extras[0]
    print(f"\nhas_extra_file({target!r})  -> {container.has_extra_file(target)}")
    print(f"extra_file_path({target!r}) -> {container.extra_file_path(target)}")

    print(f"has_extra_file('does_not_exist.bin') -> {container.has_extra_file('does_not_exist.bin')}")

    resolved = container.extra_file_path(target)
    if resolved.suffix == ".parquet":
        df = pd.read_parquet(resolved)
        print(f"\nLoaded {target} as DataFrame {df.shape}:")
        print(df.head().to_string())


if __name__ == "__main__":
    container_path = Path(sys.argv[1]) if len(sys.argv) > 1 else get_toy_container_path()
    main(container_path)
