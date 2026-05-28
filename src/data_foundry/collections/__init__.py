"""Official curated dataset collections (pinned UUIDs) shipped with data_foundry.
"""

from __future__ import annotations

from data_foundry.collections._core import CollectionEntry, DatasetCollection
from data_foundry.collections._registry import (
    BEYOND_ARENA,
    get_collection,
    list_collections,
)
from data_foundry.collections._sources import (
    DATA_FOUNDRY_CACHE_ENV,
    DEFAULT_CACHE_DIR,
    DataSource,
    HuggingFaceSource,
    LocalWarehouseSource,
    clear_cache,
    resolve_cache_dir,
)

__all__ = [
    "BEYOND_ARENA",
    "DATA_FOUNDRY_CACHE_ENV",
    "DEFAULT_CACHE_DIR",
    "CollectionEntry",
    "DataSource",
    "DatasetCollection",
    "HuggingFaceSource",
    "LocalWarehouseSource",
    "clear_cache",
    "get_collection",
    "list_collections",
    "resolve_cache_dir",
]
