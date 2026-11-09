"""Official curated dataset collections (pinned UUIDs) shipped with data_foundry."""

from __future__ import annotations

from data_foundry.collections._core import COLLECTION_FILE, CollectionEntry, DatasetCollection, collection_file_budget
from data_foundry.collections._registry import (
    BEYOND_ARENA,
    TABARENA_V0PT2_ROW_BUDGET,
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
    "COLLECTION_FILE",
    "DATA_FOUNDRY_CACHE_ENV",
    "DEFAULT_CACHE_DIR",
    "TABARENA_V0PT2_ROW_BUDGET",
    "CollectionEntry",
    "DataSource",
    "DatasetCollection",
    "HuggingFaceSource",
    "LocalWarehouseSource",
    "clear_cache",
    "collection_file_budget",
    "get_collection",
    "list_collections",
    "resolve_cache_dir",
]
