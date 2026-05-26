Inspect, prefetch, or compare official dataset collections (today: BeyondArena).

## When to invoke

* The user asks "what datasets are in BeyondArena?", "how many are there?",
  "what's in this collection?", "list the official collections", etc.
* The user wants to **pre-download** every container in a collection before
  going offline / before a benchmark run.
* The user wants to **clear** or **refresh** the local cache.
* The user wants to **compare the three split regimes** (IID / temporal /
  grouped) side by side.

If the user wants exactly one dataset, use `/get-dataset` instead.

If the user wants to fit a model on a dataset, use `/benchmark-dataset`.

## What you have

* `BEYOND_ARENA` — `DatasetCollection` shipped at
  `data_foundry.collections.BEYOND_ARENA`.
* `list_collections()` + `get_collection(name)` — registry lookup.
* `BEYOND_ARENA.prefetch(cache_dir=None, force_download=False)` — batches
  every container into a single `huggingface_hub.snapshot_download` call.
* `BEYOND_ARENA.iter_containers(cache_dir=None, ..., force_download=False)`
  — yields each loaded `CuratedContainer`.
* `BEYOND_ARENA.clear_cache(cache_dir=None)` — wipes this collection's
  cache subdir; `data_foundry.collections.clear_cache(...)` wipes the
  whole `~/.cache/data_foundry/`.
* `container.describe()`, `task.split_regime` ∈ {`"iid"`,
  `"temporal_non_iid"`, `"grouped_non_iid"`}.

## Canonical examples to read or run

* Listing + counts + first entries —
  [`examples/list_official_collections.py`](../../examples/list_official_collections.py)
* Bulk pre-download with tqdm + checksum verification —
  [`examples/download_all_beyond_arena_datasets.py`](../../examples/download_all_beyond_arena_datasets.py)
* Regime comparison printout (IID + grouped[`per_group` + `per_sample`] +
  temporal) — [`examples/data_foundry_data_regimes.py`](../../examples/data_foundry_data_regimes.py)

## Quick recipes

```python
from data_foundry.collections import BEYOND_ARENA, get_collection, list_collections

# Browse what's registered
for name in list_collections():
    c = get_collection(name)
    print(name, len(c), "containers")

# Inspect the BeyondArena registry
print(BEYOND_ARENA.unique_names[:5])
print(sum(1 for e in BEYOND_ARENA if e.is_versioned), "versioned entries")

# Warm the cache once, then iterate locally
BEYOND_ARENA.prefetch()
for container in BEYOND_ARENA.iter_containers():
    print(container.dataset_metadata.unique_name, container.task_metadata.split_regime)
```

## Gotchas

* `prefetch` and `iter_containers` over the full collection download
  several GB — confirm with the user before triggering on their machine.
* The HF cache is per-collection (`~/.cache/data_foundry/<collection>/`).
  Use `BEYOND_ARENA.clear_cache(...)` to drop just BeyondArena.
* `huggingface_hub` is only imported on cache miss — don't suggest
  installing it if every container is already cached.
