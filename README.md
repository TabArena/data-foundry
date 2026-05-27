# Data Foundry: a Schema and Toolkit for Curating Tabular ML Datasets

---

| 📂 [Examples](examples) | 🧑‍🔬 [Contribute a Dataset](CONTRIBUTING_DATASETS.md) | 📄 [Paper (placeholder — coming soon)](#-citation) |
|:---:|:---:|:---:|

---

**Data Foundry** is the data layer behind the next generation of [TabArena](https://tabarena.ai/) datasets. It provides:

- A small, opinionated **schema** for tabular datasets, tasks (IID / temporal non-IID / grouped non-IID), and outer CV splits — aligned with OpenML where possible, extended where it had to be.
- A **curation toolkit** (sanity checks, recommended-split helpers, dtype-preserving save/load) so a curator turns a raw download into a reproducible artifact in one notebook.
- A **collections API** that pins datasets (defined by ``(unique_name, uuid)``) to immutable curated containers and resolves them against a local warehouse or directly against the [BeyondArena Datasets](https://huggingface.co/datasets/TabArena/BeyondArena).

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

**Split regimes.** BeyondArena ships datasets from three regimes — which one a dataset is in shows up directly on `task_metadata`:

| Regime | Set on `PredictiveMLTaskMetadata` | Meaning |
|---|---|---|
| IID | neither `time_on` nor `group_on` | rows are independent; random / stratified splits |
| temporal non-IID | `time_on` set | rows ordered in time; future rows must not leak backwards |
| grouped non-IID | `group_on` set (+ `group_labels`) | all rows of a group stay together in one fold |

Side-by-side regime printout (one IID, two grouped variants — `per_group` vs `per_sample` — and one temporal): [`examples/data_foundry_data_regimes.py`](examples/data_foundry_data_regimes.py).

</details>

<details>
<summary><b>🗂️ Use a collection of datasets</b> — pre-download all of BeyondArena</summary>

`BEYOND_ARENA.prefetch(...)` batches every container into a single Hugging Face `snapshot_download` call (one network round-trip for the whole collection). On a warm cache it skips importing `huggingface_hub` entirely.

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

Full worked example with `tqdm` progress + checksum verification: [`examples/download_all_beyond_arena_datasets.py`](examples/download_all_beyond_arena_datasets.py). For a single dataset round-trip with checksum verification, see [`examples/download_beyond_arena_dataset.py`](examples/download_beyond_arena_dataset.py).

</details>

<details>
<summary><b>🧑‍🔬 Curate a dataset</b> — turn a raw download into a CuratedContainer</summary>

End-to-end pipeline, condensed (the full runnable version is [`examples/curate_a_dataset.py`](examples/curate_a_dataset.py)):

```python
from data_foundry.schema import DatasetMetadata, PredictiveMLTaskMetadata

# --- Basic metadata
dataset_mold = DatasetMetadata(
    unique_name="blood_transfusion",
    dataset_year="2008",
    domain_str="medical & healthcare",
    dataset_source="UCI",
    original_dataset_source_download_link="https://doi.org/10.24432/C5GS39",
    download_description="""
We download the data from the UCI repository and unzip it to a predefined folder.

mkdir -p local-data-warehouse/blood_transfusion/ \\
  && wget -P local-data-warehouse/blood_transfusion/ \\
       https://archive.ics.uci.edu/static/public/176/blood+transfusion+service+center.zip \\
  && unzip local-data-warehouse/blood_transfusion/blood+transfusion+service+center.zip \\
       -d local-data-warehouse/blood_transfusion/
""",
    academic_reference_bibtex="""@article{yeh2009knowledge,
  title={Knowledge discovery on RFM model using Bernoulli sequence},
  author={Yeh, I-Cheng and Yang, King-Jang and Ting, Tao-Ming},
  journal={Expert Systems with applications},
  volume={36}, number={3}, pages={5866--5871},
  year={2009}, publisher={Elsevier},
}
""",
    academic_reference_bibtex_key="yeh2009knowledge",
    license="CC BY 4.0",
    data_tags=["IID"],
    curation_comments="Renamed features for clarity; mapped target 0/1 → No/Yes; ~29% duplicate rows kept.",
)
task_mold = PredictiveMLTaskMetadata(
    target_column_name="DonatedBloodInMarch2007",
    problem_type="binary_classification",
    objective_metric_name="roc_auc",
    stratify_on="DonatedBloodInMarch2007",
)

# --- Preprocessing
import pandas as pd
df = pd.read_csv(f"{dataset_mold.path}/transfusion.data")
df.columns = [
    "MonthsSinceLastDonation", "NumberOfDonations", "TotalBloodDonated",
    "MonthsSinceFirstDonation", "DonatedBloodInMarch2007",
]
df["DonatedBloodInMarch2007"] = df["DonatedBloodInMarch2007"].map({1: "Yes", 0: "No"})
df["DonatedBloodInMarch2007"] = df["DonatedBloodInMarch2007"].astype("category")
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# --- Sanity checks
from data_foundry import dataset_checks
df_head, summary, numeric_stats, cat_stats, target_df = dataset_checks.run_all_checks(
    data=df,
    target_feature=task_mold.target_column_name,
    problem_type=task_mold.problem_type,
)

# --- Outer CV splits
from data_foundry.curation_recommendations import (
    get_recommended_iid_splits,
    get_recommended_splits_dimensions,
)

n_repeats, n_splits, test_size = get_recommended_splits_dimensions(dataset=df)
splits = get_recommended_iid_splits(
    dataset=df,
    n_repeats=n_repeats,
    n_splits=n_splits,
    test_size=test_size,
    stratify_on=task_mold.stratify_on,
)

# --- Split metadata + container
from data_foundry.schema import PredictiveMLSplitsMetadata
from data_foundry.curation_container import CuratedContainer

splits_mold = PredictiveMLSplitsMetadata(
    splits_comment="Default splits for IID data.",
    splits=splits,
)
curated_data = CuratedContainer(
    dataset=df,
    dataset_metadata=dataset_mold,
    task_metadata=task_mold,
    experiment_metadata=splits_mold,
)
curated_data.save()
print(curated_data.uuid, curated_data.checksum)
```

For the contributor flow (where to put the notebook, how to open the PR, the `/new-dataset` Claude Code skill, best practices around versioning, anomaly tracking, and dtype handling), see [**CONTRIBUTING_DATASETS.md**](CONTRIBUTING_DATASETS.md).

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
│   ├── schema.py             # DatasetMetadata, PredictiveMLTaskMetadata, PredictiveMLSplitsMetadata
│   ├── curation_container.py # CuratedContainer (save/load + describe + checksum)
│   ├── collections/          # BEYOND_ARENA, DatasetCollection, HuggingFaceSource, cache helpers
│   ├── curation_recommendations.py  # recommended split helpers (IID, grouped, temporal)
│   ├── dataset_checks.py     # run_all_checks(...) — sanity stats for the curation notebook
│   └── examples/toy_container/  # tiny ready-to-load CuratedContainer shipped in-package
├── datasets/                 # curation notebooks
│   ├── _template/            # canonical notebook skeleton
│   ├── _dev/                 # contributions land here first
│   ├── _maintenance/         # re-runs / fixes for already-released datasets
│   └── beyond_iid/           # promoted datasets — pinned by `final_uuid_list.py`
├── examples/                 # runnable demos (covers the use-cases above)
├── scripts/                  # one-off tooling (toy container builder)
│   └── beyond_arena/         # BeyondArena-specific scripts and outputs (warehouse stats, plots)
├── tests/                    # pytest test suite
└── local-data-warehouse/     # gitignored — curators write raw + saved containers here
```

## 🧑‍🔬 Contributing a Dataset

The short version:

1. Copy [`datasets/_template/_template.ipynb`](datasets/_template/_template.ipynb)
   to `datasets/_dev/<topic>/<unique_name>/<unique_name>.ipynb`.
2. Run the notebook end-to-end so the saved cells contain populated check
   tables and the final `uuid` / `checksum`.
3. Open a PR — reviewers will move the notebook into the right
   `beyond_iid/` subfolder and append the UUID to
   [`datasets/beyond_iid/final_uuid_list.py`](datasets/beyond_iid/final_uuid_list.py).

The long version (field-by-field walkthrough, split-helper choice, dtype
gotchas, the `/new-dataset` Claude Code scaffolding skill): see
[**CONTRIBUTING_DATASETS.md**](CONTRIBUTING_DATASETS.md).

## 📄 Citation

**PLACEHOLDER**
📄 [arXiv:XXXX](https://arxiv.org/abs/XXX)

```bibtex
PLACEHOLDER
```
