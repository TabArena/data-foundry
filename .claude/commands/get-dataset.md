Download (or hit the cache for) a single dataset from BeyondArena and load
it as a `CuratedContainer`.

## When to invoke

* The user names a specific dataset they want to load (by `unique_name` or
  by UUID).
* The user wants to **inspect** the metadata, dtypes, target, or splits of
  one dataset without running a model.
* The user is verifying that a container is on disk / re-downloading after
  a known upstream change.

If the user wants every dataset in a collection, use `/browse-collection`.

If the user wants to *fit a model* on the dataset, use `/benchmark-dataset`
— this skill stops at "loaded and ready to use."

## What you have

* `BEYOND_ARENA.get_dataset(name_or_uuid, *, cache_dir=None,
  load_dataset=True, load_test_data=False, force_download=False)` — the
  one-call entry point.
* `container.describe()` — full identity + dtype counts + per-section
  metadata.
* `container.describe_container()`, `container.describe_dataset()`,
  `task.describe()`, `experiment_metadata.describe()` — finer-grained
  views.
* `container.checksum == container._create_checksum()` — sanity check that
  on-disk bytes are intact (the existing examples assert this).
* `curation/records/<unique_name>.md` — the curation record. Its
  `notebook_path` names the notebook that produced this container, so
  "how was this preprocessed / why this target / why this split" is one
  file away; `## Comments` holds the triage reasoning.

## Canonical examples to read or run

* Round-trip + checksum verification —
  [`examples/download_beyond_arena_dataset.py`](../../examples/download_beyond_arena_dataset.py)
* Loading and inspecting a container from disk —
  [`examples/load_curated_container.py`](../../examples/load_curated_container.py)

## Quick recipe

```python
from data_foundry.collections import BEYOND_ARENA

container = BEYOND_ARENA.get_dataset("airfoil_self_noise")

print(container.describe())                                   # full overview
assert container.checksum == container._create_checksum(), "container corrupted"

df = container.dataset
target = container.task_metadata.target_column_name
regime = container.task_metadata.split_regime  # "iid" / "temporal_non_iid" / "grouped_non_iid"
```

## Cache management

* The cache lives at `~/.cache/data_foundry/<collection>/` by default;
  override with `cache_dir=...` or `$DATA_FOUNDRY_CACHE`.
* Force re-download a stale container:
  `BEYOND_ARENA.get_dataset(name, force_download=True)`.
* Drop the collection's cache: `BEYOND_ARENA.clear_cache()`.

## Gotchas

* If the dataset is **versioned** (`is_versioned=True` on the
  `CollectionEntry`), the on-disk path is `<name>/versions/<uuid>/`. The
  collection API hides this — but it shows up in
  `entry.relative_path` and may surprise users grep'ing the warehouse.
* `huggingface_hub` is only imported on a cache miss; if the file is
  already on disk, the package does not need it installed.
