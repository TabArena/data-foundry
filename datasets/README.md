# `datasets/`

The dataset definitions of Data Foundry, by state. New datasets are v2 folders (one `dataset.py`, an
`explore.ipynb` workbench and a generated `README.md`; [CONTRIBUTING_DATASETS.md](../CONTRIBUTING_DATASETS.md)).
The notebooks in this tree are Data Foundry v1, kept as the record of what shipped
([DATA_FOUNDRY_V1.md](../DATA_FOUNDRY_V1.md)); never add a dataset as a notebook.

```
datasets/
├── _template/        # the v2 template `dataset new` copies: dataset.py + explore.ipynb
├── _dev/             # work in progress, one folder per collection being built
│   ├── tabarena-v0pt2/      # the TabArena v0.2 working copy: 125 v2 definitions (start with its GETTING_STARTED.md)
│   └── feature_selection/   # v1 notebooks of the feature-selection work (SelectArena)
├── beyond_iid/       # the shipped BeyondArena collection (v1 notebooks), pinned in final_uuid_list.py
└── _maintenance/     # everything kept for reference or development that is not in a shipped collection
    ├── _old_collections/    # tabarena-v0pt1/: the TabArena v0.1 datasets re-curated when TabArena merged into BeyondArena
    ├── _deprecated/         # once in Data Foundry, no longer used
    ├── _suspended/          # on hold
    └── _out_of_scope/       # outside the benchmark's scope (too small, too late, IID versions of non-IID tasks)
```

| Folder | Format | What it is | Who edits it |
|---|---|---|---|
| [`_template/`](_template/) | v2 | The template `.venv/bin/python -m data_foundry.curation.cli dataset new` copies. | Framework changes only. |
| [`_dev/tabarena-v0pt2/`](_dev/tabarena-v0pt2/) | v2 | One folder per dataset of TabArena v0.2, built as container format 2. Its [`README.md`](_dev/tabarena-v0pt2/README.md) has the dataset table, [`GETTING_STARTED.md`](_dev/tabarena-v0pt2/GETTING_STARTED.md) the way in, [`CHANGELOG.md`](_dev/tabarena-v0pt2/CHANGELOG.md) every change. | Curators, through PRs; every change gets a CHANGELOG entry. |
| [`_dev/feature_selection/`](_dev/feature_selection/) | v1 | Notebooks of the feature-selection work; several are older copies of datasets that shipped from `beyond_iid/`. | Not for new datasets. |
| [`beyond_iid/`](beyond_iid/) | v1 | The BeyondArena notebooks (`old_iid/`, `new_iid/`, `temporal/`, `grouped/`), the ablation variants (`_ablations/`) and [`final_uuid_list.py`](beyond_iid/final_uuid_list.py), the `(unique_name, uuid)` pins of the shipped containers. | Frozen: a shipped notebook is not re-run (a re-run makes a new UUID). |
| [`_maintenance/`](_maintenance/) | v1 | Datasets outside a shipped collection, kept for provenance: the TabArena v0.1 re-curation (`_old_collections/tabarena-v0pt1/`), deprecated, suspended and out-of-scope datasets. A record of a dataset here carries `DF: Yes` without a collection tag on purpose (see [`_deprecated/README.md`](_maintenance/_deprecated/README.md)). | Rarely; moving a dataset here updates its record's `notebook_path`. |

Each curation record points at its definition: `v2_path` at the `dataset.py`, and `notebook_path` at the v1 notebook
of a dataset curated with v1 (`.venv/bin/python -m data_foundry.curation.cli sync-notebooks` keeps both in sync with
this tree).

Raw data and saved containers never live here: they are in `local-data-warehouse/<unique_name>/` (gitignored;
`$DATA_FOUNDRY_WAREHOUSE` overrides it).
