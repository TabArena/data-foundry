# Data Foundry: a Schema and Toolkit for Curating Tabular ML Datasets

---

| 📂 [Examples](examples) | 🗂️ [Curation Log](https://tabarena.github.io/data-foundry/) | 🚀 [Getting Started](datasets/_dev/tabarena-v0pt2/GETTING_STARTED.md) | 🧑‍🔬 [Contribute a Dataset](CONTRIBUTING_DATASETS.md) | 📄 [Paper](https://arxiv.org/abs/2606.30410) |
|:---:|:---:|:---:|:---:|:---:|

---

**Data Foundry** is the data layer behind the next generation of [TabArena](https://tabarena.ai/) datasets. It provides:

- A small, opinionated **schema** for tabular datasets, tasks (IID / temporal non-IID / grouped non-IID), and outer CV splits — aligned with OpenML where possible, extended where it had to be.
- A **curation toolkit** so a curator turns a raw download into a reproducible artifact: one `dataset.py` definition per dataset (`data_foundry.v2`), with the split protocol, sanity checks, bundle checks and a generated evidence page built in.
- A **collections API** that pins datasets (defined by ``(unique_name, uuid)``) to immutable curated containers and resolves them against a local warehouse or directly against Hugging Face, as for the [BeyondArena Datasets](https://huggingface.co/datasets/TabArena/BeyondArena). It is how every collection ships, BeyondArena today and TabArena v0.2 next.
- A git-native **curation log + dashboard** — the dataset backlog lives as **one markdown record per candidate dataset** under [`curation/records/`](curation/records), edited locally through a Sheets-like dashboard (`data-foundry-curation serve`) with a built-in **Guidelines** tab, and published as a read-only public site on [GitHub Pages](https://tabarena.github.io/data-foundry/). It replaces the old curation spreadsheet; a new dataset is added simply by creating a markdown file.

## ⚡ Quickstart

> [!TIP]
> Pull a real curated dataset from BeyondArena and inspect its full metadata + outer CV splits. The first call fetches from Hugging Face; subsequent calls hit your local cache.

```bash
pip install data-foundry
python examples/load_curated_container.py
```

```python
from data_foundry.collections import BEYOND_ARENA

container = BEYOND_ARENA.get_dataset("airfoil_self_noise")
print(container.describe())          # full identity + dtypes + task + splits
print(container.dataset.shape)       # the actual DataFrame
print(container.task_metadata.split_regime)  # "iid", "temporal_non_iid", or "grouped_non_iid"
```

That's the whole API surface in three lines. See [`examples/benchmark_on_beyond_arena.py`](examples/benchmark_on_beyond_arena.py) for benchmarking Random Forest on the data! 

## 🕹️ Use Cases

<details>
<summary><b>🧪 Inspect a curated container offline</b> — no Hugging Face download required</summary>

The package ships a toy `CuratedContainer` so you can poke at the full API — schema, dtypes, splits, `describe()` — without touching the network. Identical interface to a downloaded BeyondArena container.

```python
from data_foundry.curation_container import CuratedContainer
from data_foundry.examples import get_toy_container_path

container = CuratedContainer.load(get_toy_container_path())
print(container.describe())          # full identity + dtypes + task + splits
print(container.dataset.shape)       # the actual DataFrame
print(container.task_metadata.split_regime)  # "iid", "temporal_non_iid", or "grouped_non_iid"
```

Full inspection script (every metadata field printed): [`examples/load_curated_container.py`](examples/load_curated_container.py).

</details>

<details>
<summary><b>📦 Use one dataset</b> — IID and non-IID variants</summary>

Download a single BeyondArena container by name (or UUID) and iterate its outer CV splits. The collection resolves the container against your local cache; subsequent runs hit disk, not the network.

```python
from data_foundry.collections import BEYOND_ARENA

container = BEYOND_ARENA.get_dataset("airfoil_self_noise")
df = container.dataset
target = container.task_metadata.target_column_name

for repeat_id, folds in container.experiment_metadata.splits.items():
    for fold_id, (train_idx, test_idx) in folds.items():
        X_train, y_train = df.iloc[train_idx].drop(columns=target), df.iloc[train_idx][target]
        X_test,  y_test  = df.iloc[test_idx].drop(columns=target),  df.iloc[test_idx][target]
        # ... fit, evaluate ...
```

Full worked example (Random Forest, RMSE per fold, full metadata via `container.describe()`): [`examples/benchmark_on_beyond_arena.py`](examples/benchmark_on_beyond_arena.py).

**Split regimes.** A collection ships datasets from three regimes — which one a dataset is in shows up directly on `task_metadata`:

| Regime | Set on `task_metadata` | Meaning |
|---|---|---|
| IID | neither `time_on` nor `group_on` | rows are independent; random / stratified splits |
| temporal non-IID | `time_on` set | rows ordered in time; future rows must not leak backwards |
| grouped non-IID | `group_on` set (+ `group_labels`) | all rows of a group stay together in one fold |

**Container formats.** `container.format_version` is `2` for a container built by a `dataset.py` definition (the
TabArena v0.2 working copy and every new dataset) and `1` for the shipped BeyondArena containers, which were built
with Data Foundry v1 ([DATA_FOUNDRY_V1.md](DATA_FOUNDRY_V1.md)); a format-2 container also states it in
`container_metadata.json`. The collections API and `CuratedContainer.load` read both. Both read the same through `task_metadata.time_on`,
`group_on`, `group_labels` and `group_time_on`. Format 2 stores the group fields once, in a `Grouping`
(`data_foundry.schema.Grouping`), and `container.grouping` returns it: the prediction unit (a row, or one prediction
per group with an aggregation such as `mean` or `any`), what a model may know about a group when predicting, and the
definition of a group with its source. A format-1 container has no such block, so `container.grouping` raises
there. The group column is split and scoring metadata, never a model feature. `run_bundle_checks` judges each
format by its own split protocol (v1: the repeat ladder and 250k test rows; v2: 3 folds and 500k test rows).

Side-by-side regime printout (one IID, two grouped variants — `per_group` vs `per_sample` — and one temporal): [`examples/data_foundry_data_regimes.py`](examples/data_foundry_data_regimes.py).

</details>

<details>
<summary><b>🗂️ Use a collection of datasets</b> — pre-download all of BeyondArena</summary>

A collection pins its datasets by `(unique_name, uuid)` and resolves them against a source (Hugging Face, or a local warehouse); `list_collections()` and `get_collection(name)` find the registered ones. `BEYOND_ARENA` is the first, and the TabArena v0.2 collection will be registered the same way. `BEYOND_ARENA.prefetch(...)` batches every container into a single Hugging Face `snapshot_download` call (one network round-trip for the whole collection). On a warm cache it skips importing `huggingface_hub` entirely.

```python
from data_foundry.collections import BEYOND_ARENA

paths = BEYOND_ARENA.prefetch()          # warms the cache once
for container in BEYOND_ARENA.iter_containers():  # now hits disk only
    print(container.dataset_metadata.unique_name, container.dataset.shape)
```

Cache management:

```python
BEYOND_ARENA.clear_cache()                 # nuke this collection's subdir
BEYOND_ARENA.get_dataset(name, force_download=True)  # re-fetch a single container
```

Full worked example with `tqdm` progress + checksum verification: [`examples/download_all_beyond_arena_datasets.py`](examples/download_all_beyond_arena_datasets.py).

</details>

<details>
<summary><b>🧑‍🔬 Curate a dataset</b> — turn a raw download into a CuratedContainer</summary>

A dataset is one class in a `dataset.py`: flat attributes for the metadata and the task, and hooks for reading and
cleaning. The base class adds the dtype casts, the row order, the split protocol, the checks and the export. A
complete small definition ([`blood_transfusion`](datasets/_dev/tabarena-v0pt2/blood_transfusion/dataset.py)),
shortened:

```python
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset


class BloodTransfusion(AbstractCuratedDataset):
    unique_name = "blood_transfusion"
    year = "2008"
    domain = "medical & healthcare"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C5GS39"
    license = "CC BY 4.0"
    download_description = """
        mkdir -p local-data-warehouse/blood_transfusion/ && wget -P local-data-warehouse/blood_transfusion/ <UCI zip> && unzip ...
    """
    bibtex = """
        @article{yeh2009knowledge, title={Knowledge discovery on RFM model using Bernoulli sequence}, ...}
    """
    curation_comments = """
        - We renamed the target and mapped binary values to "Yes"/"No".
        - Anomaly: the data has a lot of duplicates (29%) and several duplicates with different target values.
    """
    target = "DonatedBloodInMarch2007"
    problem_type = "binary_classification"   # metric roc_auc and a stratified IID split by default

    def _load_raw(self, raw_dir):
        return pd.read_csv(raw_dir / "transfusion.data")

    def _clean(self, raw):
        df = raw.set_axis([..., "DonatedBloodInMarch2007"], axis=1)
        df["DonatedBloodInMarch2007"] = df["DonatedBloodInMarch2007"].map({1: "Yes", 0: "No"})
        return df
```

A grouped task adds `grouping = Grouping(on=..., labels=..., prediction_unit=..., definition=...)`, a temporal one
`temporal = Temporal(on=..., splits=TemporalSplits(...))`. Then:

```bash
.venv/bin/python -m data_foundry.curation.cli dataset new <unique_name> --root datasets/_dev/tabarena-v0pt2
.venv/bin/python -m data_foundry.curation.cli dataset check datasets/_dev/tabarena-v0pt2/<unique_name>   # no save; writes README.md
.venv/bin/python -m data_foundry.curation.cli dataset build datasets/_dev/tabarena-v0pt2/<unique_name>   # saves the container (curators)
```

The contributor flow (the steps, the probes, the Claude Code skills, the practices) is in
[**CONTRIBUTING_DATASETS.md**](CONTRIBUTING_DATASETS.md).

</details>

<details>
<summary><b>🗂️ Triage the dataset backlog</b> — the curation log + local dashboard</summary>

Before a dataset becomes a definition, it lives in the **curation log**: one markdown record
per candidate dataset under [`curation/records/`](curation/records). Each `<unique_name>.md`
has YAML front-matter (the structured / dropdown fields) plus a free-text body
(`## Comments`, `## Reference`). Add or triage a dataset by creating/editing its file — by
hand, with an agent, or through the dashboard.

```bash
pip install "data-foundry[curation]"   # or the editable dev install
data-foundry-curation serve            # → http://127.0.0.1:8765
```

The local, Sheets-like **dashboard** edits those records in place (filter by status, pin a
working row, add dropdown options, …) and ships a built-in **Guidelines** tab describing the
selection criteria and processing conventions. Other CLI subcommands:

```bash
data-foundry-curation validate                 # check records against the dropdown vocab
data-foundry-curation sync-notebooks           # refresh each record's notebook_path + v2_path (--check to dry-run)
data-foundry-curation export --format xlsx out.xlsx   # flat snapshot (csv|parquet|xlsx|gsheet)
data-foundry-curation build-site site/          # read-only static copy (e.g. GitHub Pages)
data-foundry-curation dataset check <folder>    # run a v2 dataset.py + bundle checks, write README.md (no save)
```

**Browse it online.** A read-only copy of the backlog is published to GitHub Pages —
[**tabarena.github.io/data-foundry**](https://tabarena.github.io/data-foundry/) — and
regenerated automatically from `curation/records/` on every push to `main` (no install, no
network round-trip to Hugging Face; search, sort, filter, and pin all run in the browser).
Note this makes every record's comments, reviewer names, and decision notes public.

Working with Claude Code? The repo ships five curation workflows (in `.claude/skills/`):

| Command | What it does |
|---|---|
| `/triage-candidates` | Starts the dashboard and loads the curation guidelines, so the agent can help decide which candidates belong. |
| `/check-candidate <name>` | A cited second opinion on one record: traces the original source and writes the evidence into the record. |
| `/add-dataset <name>` | Scaffolds the v2 dataset folder (`dataset.py` + `explore.ipynb`) for a `Yes` candidate from its record. |
| `/verify-dataset <name>` | Runs the bundle checks plus a 15-item judgment rubric (provenance, split regime, leakage) before a dataset ships. |
| `/rebuild-working-copy` | Rebuilds the TabArena v0.2 working copy and verifies the build (comparison, reproduction from the traced inputs, backup). |

Loading, browsing and benchmarking shipped datasets needs no command; `CLAUDE.md` and `examples/` cover it.

</details>

## 🪄 Installation

> [!IMPORTANT]
> Requires Python **3.10+**.

<details>
<summary><b>📦 From PyPI</b> — use Data Foundry as a library</summary>

```bash
pip install data-foundry
```

</details>

<details>
<summary><b>🌱 From source</b> — clone and install editable</summary>

```bash
git clone https://github.com/TabArena/data-foundry.git
cd data-foundry
uv pip install -e .
```

</details>

<details>
<summary><b>🛠️ Developer setup</b> — extras for curation, tests, and tooling</summary>

```bash
git clone https://github.com/TabArena/data-foundry.git
cd data-foundry
uv pip install -e ".[dev,tests]"
pytest                                 # run the test suite
ruff check . && ruff format --check .  # lint + format
```

The `dev` extra adds curation-time deps (`openml`, `kaggle`, `seaborn`, `polars`, etc.); `tests` adds `pytest` and `scikit-learn` (needed for the recommended-split helpers and examples).

</details>

## 🗂️ Repository Structure

```
data-foundry/
├── src/data_foundry/         # the package — schema, container, collections, checks, splits
│   ├── v2/                   # v2 dataset definitions: AbstractCuratedDataset, split protocol, checks, README report
│   ├── schema.py             # DatasetMetadata, PredictiveMLTaskMetadata (format 1) / V2 (+ Grouping), PredictiveMLSplitsMetadata
│   ├── curation_container.py # CuratedContainer (save/load + describe + checksum)
│   ├── collections/          # BEYOND_ARENA, DatasetCollection, HuggingFaceSource, cache helpers
│   ├── curation_recommendations.py  # the v1 split helpers (DATA_FOUNDRY_V1.md)
│   ├── dataset_checks.py     # run_all_checks(...) — sanity stats, rendered in each dataset's README
│   ├── bundle_checks.py      # run_bundle_checks(...) / verify_saved_container(...) — bundle integrity
│   ├── curation/             # curation log toolkit — CurationRecord, store, dashboard (serve), import/export, build-site
│   └── examples/toy_container/  # tiny ready-to-load CuratedContainer shipped in-package
├── curation/                 # the curation log (git-tracked data) — records/*.md + vocabularies.yaml
├── datasets/                 # dataset definitions; see datasets/README.md
│   ├── _template/            # the template `dataset new` copies (dataset.py + explore.ipynb)
│   ├── _dev/                 # work in progress; `tabarena-v0pt2/` is the TabArena v0.2 working copy
│   ├── _maintenance/         # deprecated, suspended and out-of-scope datasets, the old TabArena v0.1 re-curation
│   └── beyond_iid/           # the shipped BeyondArena notebooks (v1), pinned by `final_uuid_list.py`
├── examples/                 # runnable demos (covers the use-cases above); see examples/README.md
├── scripts/                  # one-off tooling (toy container builder, release)
│   └── beyond_arena/         # BeyondArena-specific scripts and outputs (warehouse stats, plots)
├── .claude/skills/           # Claude Code skills; each skill's scripts/ holds the tools it runs
│   ├── verify-dataset/scripts/  # leak, task and group probes for v2 datasets, the collection bundle check
│   └── rebuild-working-copy/scripts/  # rebuild the v0.2 working copy and verify the build
├── tests/                    # pytest test suite
└── local-data-warehouse/     # gitignored — curators write raw + saved containers here
```

## 🧑‍🔬 Contributing a Dataset

The short version (v2):

1. Scaffold the folder: `.venv/bin/python -m data_foundry.curation.cli dataset new <unique_name> --root
   datasets/_dev/tabarena-v0pt2` (or `/add-dataset <unique_name>` in Claude Code), and fill in `dataset.py`.
2. Run `.venv/bin/python -m data_foundry.curation.cli dataset check <folder>` until there are no errors and every
   warning is fixed or accepted with a reason; it writes the folder's `README.md`. Then run the probes in
   `.claude/skills/verify-dataset/scripts/` (leak, task and, for a grouped task, group probes).
3. Open a PR; a curator runs `dataset build`, which saves the container and records its UUID.

The long version is [**CONTRIBUTING_DATASETS.md**](CONTRIBUTING_DATASETS.md); a first contribution to TabArena v0.2
starts with the [getting-started guide](datasets/_dev/tabarena-v0pt2/GETTING_STARTED.md), which also lists the
candidates to work on.

The shipped BeyondArena datasets were built with Data Foundry v1, as curation notebooks pinned in
[`datasets/beyond_iid/final_uuid_list.py`](datasets/beyond_iid/final_uuid_list.py). v1 is retired for new datasets;
[DATA_FOUNDRY_V1.md](DATA_FOUNDRY_V1.md) keeps what is needed to read, check or maintain them.

## 📄 Citation

If you use Data Foundry or the BeyondArena datasets, please cite:

> **Beyond IID: How General Are Tabular Foundation Models, Really?**
> Lennart Purucker, Andrej Tschalzev, Nick Erickson, Gioia Blayer, David Holzmüller,
> Alan Arazi, Alexander Pfefferle, Mustafa Tajjar, Gaël Varoquaux, Frank Hutter.
> arXiv:2606.30410, 2026. <https://arxiv.org/abs/2606.30410>

```bibtex
@misc{purucker2026iidgeneraltabularfoundation,
      title={Beyond IID: How General Are Tabular Foundation Models, Really?},
      author={Lennart Purucker and Andrej Tschalzev and Nick Erickson and Gioia Blayer and David Holzmüller and Alan Arazi and Alexander Pfefferle and Mustafa Tajjar and Gaël Varoquaux and Frank Hutter},
      year={2026},
      eprint={2606.30410},
      archivePrefix={arXiv},
      primaryClass={cs.LG},
      url={https://arxiv.org/abs/2606.30410},
}
```
