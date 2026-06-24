# Deprecated datasets

Datasets here were once part of Data Foundry but are **deprecated**: kept for provenance,
but **not used anymore** and **not part of any shipped collection** (BeyondArena / TabArena).

## How this shows up in a curation record

A deprecated dataset's curation record (`curation/records/<name>.md`) carries:

- `data_foundry_status: [DF: Yes]` — it **is** in Data Foundry, **but**
- **no** collection tag (`BeyondArena` / `TabArena (v0.1)`) — it is **not** in a shipped collection.

So **`DF: Yes` with no collection tag is the expected, intentional state** for a deprecated
dataset — it does **not** mean the record is missing a tag, and it should not be "fixed" by
adding `BeyondArena`/`TabArena (v0.1)`. The same is true for the sibling buckets below.

## The `datasets/_maintenance/` buckets (all: in Data Foundry, not in a shipped collection)

- `_deprecated/` — was used, now deprecated.
- `_suspended/` — temporarily set aside (these records typically use `DF: Suspended`).
- `_out_of_scope/` — intentionally excluded, with the reason in the subfolder name
  (`_iid_version_of_non_iid`, `_too_small_to_add`, `_too_late_to_add`).
- `_old_collections/` — previously-shipped collections (e.g. `tabarena-v0pt1`).

Datasets actually **shipped today** live under `datasets/beyond_iid/` — their records are tagged
`BeyondArena` (plus `TabArena (v0.1)` for the v0.1 set) **and** `DF: Yes`.
