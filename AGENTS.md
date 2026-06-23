# AGENTS.md

Guidance for autonomous coding agents (Claude Code, Cursor, Aider, …)
working inside the **Data Foundry** repository.

If you are an interactive contributor and just want to know the repo layout,
read [`README.md`](README.md) first. This document is the part of that
information an agent needs in order to act safely.

---

## What this repo is

Data Foundry is the data-layer toolkit behind
[BeyondArena](https://huggingface.co/datasets/TabArena/BeyondArena) and
[TabArena](https://tabarena.ai/). The Python package
(`src/data_foundry/`) defines:

* a pydantic-dataclass **schema** for tabular datasets, predictive ML tasks,
  and outer CV splits (`schema.py`);
* a **`CuratedContainer`** that bundles a DataFrame with that schema, persists
  it dtype-faithfully, and computes a Blake2b checksum over everything
  (`curation_container.py`);
* a **collections API** that pins immutable `(unique_name, uuid)` pointers
  and resolves them against a local warehouse or the BeyondArena Hugging
  Face mirror, with cache + force-download semantics (`collections/`);
* helpers used by curation notebooks — sanity checks (`dataset_checks.py`)
  and recommended outer-CV split builders (`curation_recommendations.py`);
* a git-native **curation backlog** (`src/data_foundry/curation/`) — one
  markdown record per candidate dataset under `curation/records/`, with a
  local editing dashboard, a sheet importer, and a one-way CSV/Sheet exporter.
  This replaces the legacy curation Google Sheet; `data-foundry-curation -h`
  lists the CLI (`serve`, `import-sheet`, `validate`, `export`). The editable
  dropdown vocabularies live in `curation/vocabularies.yaml`.

The actual curation work happens in `datasets/`, which is mostly Jupyter
notebooks — see [`CONTRIBUTING_DATASETS.md`](CONTRIBUTING_DATASETS.md).

---

## High-leverage use cases for an agent

Roughly ordered by how often agents are useful here:

### 1. Scaffolding a new curation notebook from spreadsheet metadata

Highest-value: the curator has tab-separated metadata from a spreadsheet
and wants a populated notebook under `datasets/_dev/<topic>/<unique_name>/`.

The `/new-dataset` slash command at
[`.claude/commands/new-dataset.md`](.claude/commands/new-dataset.md) is the
canonical procedure — column mappings, snake-case conversion, target
subfolder picking, BibTeX templates, and which split helper to call for
which regime. **Always read that file before scaffolding.** It encodes
decisions you would otherwise have to guess at.

The skill writes a 17-cell notebook based on
`datasets/_template/_template.ipynb`. Read the template before writing so
the JSON structure is exact.

### 2. Extending the package (schema, container, collections, examples)

When changing core code:

* **Tests live in `tests/`.** Run `pytest -q` after any change. The suite
  is fast (~2s); there is no excuse for not running it.
* **Linting:** `ruff check .` and `ruff format .`. Settings are in
  `pyproject.toml` (`[tool.ruff]`). `from __future__ import annotations`
  is mandatory in every file; 120-char lines; Google-style docstrings.
* **Examples in `examples/` are part of the docs surface.** When you add a
  feature, add or update the matching example, and (only if it's a major
  use case) link it from `README.md`.
* **`describe()` methods** on `DatasetMetadata`, `PredictiveMLTaskMetadata`,
  `PredictiveMLSplitsMetadata`, and `CuratedContainer` are the human-facing
  surface — keep them in sync if you add or rename schema fields.

### 3. Curation tooling work (checks, recommended splits, helpers)

* `dataset_checks.run_all_checks(...)` returns five DataFrames — see
  `simple_metadata_exploration_v2.py` (in `scripts/beyond_arena/`) for how
  the warehouse-wide stats are computed; that file's dtype categorization
  is the reference for `CuratedContainer._feature_dtype_counts`.
* `curation_recommendations.py` has three flavors — IID, grouped, temporal.
  IID and grouped have automated helpers; temporal splits are still
  manual.

### 4. Repo plumbing (CI, packaging, release)

`pyproject.toml` carries PyPI metadata. The release flow is documented in
`README.md` under "Releasing to PyPI" — `uv build` + `uv publish`. Don't
bump versions or publish without explicit human authorization.

---

## Conventions you must follow

* **Always read before writing.** The schema fields and `describe()` output
  are user-facing; pattern-match the existing style rather than inventing
  a new one.
* **`from __future__ import annotations`** at the top of every `.py` file.
* **Don't commit changes unless the user explicitly asks.** Same for
  pushes, PRs, and PyPI publishes.
* **Don't write README files, planning docs, or analysis files** unless
  asked. The repo intentionally has very few `.md` files.
* **Don't add comments that describe what the code does** — only *why*,
  when the why is non-obvious.
* **Curation notebooks must be valid JSON.** When editing them, use
  `nbformat` if available, or treat them as opaque structured data; do not
  hand-edit the cell `source` array without verifying the result parses.

---

## Things that look like blockers but aren't

* **`local-data-warehouse/` is gitignored** and may be empty on a fresh
  clone. That's fine — only the toy container (in
  `src/data_foundry/examples/toy_container/`) ships in-tree; everything
  else is downloaded on demand via the collections API.
* **Huggingface_hub is an optional runtime requirement** for `prefetch` /
  `get_dataset` cache *misses* — if every container is already cached,
  the package does not import it. So a fresh dev env without HF set up
  can still run all of `pytest tests/`.
* **The toy container is regenerated by `scripts/build_toy_container.py`,**
  not edited by hand. If a test fails on a UUID/checksum mismatch, the
  fix is to regenerate, not to update the test expectation.

---

## Pointers

| Topic | Read |
|---|---|
| Repo overview, install, quickstart | [`README.md`](README.md) |
| Curation contribution flow | [`CONTRIBUTING_DATASETS.md`](CONTRIBUTING_DATASETS.md) |
| Schema definitions | [`src/data_foundry/schema.py`](src/data_foundry/schema.py) |
| Curation backlog (records, dashboard, import/export) | [`src/data_foundry/curation/`](src/data_foundry/curation/) |
| Curation records + dropdown vocab (data) | [`curation/`](curation) |
| Container save/load + describe | [`src/data_foundry/curation_container.py`](src/data_foundry/curation_container.py) |
| Collections + cache helpers | [`src/data_foundry/collections/`](src/data_foundry/collections/) |
| Notebook scaffolding skill | [`.claude/commands/new-dataset.md`](.claude/commands/new-dataset.md) |
| Browse / prefetch a collection | [`.claude/commands/browse-collection.md`](.claude/commands/browse-collection.md) |
| Load a single dataset | [`.claude/commands/get-dataset.md`](.claude/commands/get-dataset.md) |
| Fit + score a model on a dataset | [`.claude/commands/benchmark-dataset.md`](.claude/commands/benchmark-dataset.md) |
| Notebook template | [`datasets/_template/_template.ipynb`](datasets/_template/_template.ipynb) |
| Examples (use-case anchors) | [`examples/`](examples) |
