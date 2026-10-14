# Examples

Runnable scripts for using Data Foundry: loading containers, benchmarking on a collection, and working with the
curation log. Run them from the repository root, for example `python examples/load_curated_container.py`.

| Script | What it shows | Needs |
|---|---|---|
| [`load_curated_container.py`](load_curated_container.py) | Load a container and print its identity, data, metadata (both container formats) and extra files. Defaults to the toy container shipped with the package. | nothing |
| [`benchmark_on_beyond_arena.py`](benchmark_on_beyond_arena.py) | Train a random forest on every outer split of one BeyondArena dataset, dropping the group column from the features. | network (first run), scikit-learn |
| [`data_foundry_data_regimes.py`](data_foundry_data_regimes.py) | One IID, two grouped (`per_group`, `per_sample`) and one temporal dataset side by side: how the regime shows up in the metadata. | network (first run) |
| [`download_all_beyond_arena_datasets.py`](download_all_beyond_arena_datasets.py) | The registered collections, then the whole BeyondArena collection downloaded once (`prefetch`) and every checksum verified. | network, several GB |
| [`curation_records.py`](curation_records.py) | Read, filter, edit and snapshot the curation log (`curation/records/`) from code. | a repository checkout |

Containers come through a collection (`data_foundry.collections`): it pins each dataset by `(unique_name, uuid)` and
downloads it once into `~/.cache/data_foundry/<collection>/` (an explicit `cache_dir=...`, then
`$DATA_FOUNDRY_CACHE`, take precedence). BeyondArena is the collection registered today; the TabArena v0.2 collection
will be used the same way.

To curate a dataset there is no example script: a dataset is a `dataset.py` folder made from
[`datasets/_template/`](../datasets/_template/) (`dataset new`), and the definitions of the TabArena v0.2 working
copy are the worked examples, starting with
[`blood_transfusion`](../datasets/_dev/tabarena-v0pt2/blood_transfusion/dataset.py). See
[CONTRIBUTING_DATASETS.md](../CONTRIBUTING_DATASETS.md). The v1 notebook pipeline that built BeyondArena is in
[DATA_FOUNDRY_V1.md](../DATA_FOUNDRY_V1.md).
