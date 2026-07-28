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
[TabArena](https://tabarena.ai/), introduced in the paper
[*Beyond IID: How General Are Tabular Foundation Models, Really?*](https://arxiv.org/abs/2606.30410)
(arXiv:2606.30410). The Python package
(`src/data_foundry/`) defines:

* a pydantic-dataclass **schema** for tabular datasets, predictive ML tasks,
  and outer CV splits (`schema.py`);
* a **`CuratedContainer`** that bundles a DataFrame with that schema, persists
  it dtype-faithfully, and computes a Blake2b checksum over everything
  (`curation_container.py`);
* a **collections API** that pins immutable `(unique_name, uuid)` pointers
  and resolves them against a local warehouse or the BeyondArena Hugging
  Face mirror, with cache + force-download semantics (`collections/`);
* helpers used by curation notebooks — exploratory data checks
  (`dataset_checks.py`), post-hoc bundle integrity checks (`bundle_checks.py`)
  and recommended outer-CV split builders (`curation_recommendations.py`);
* a git-native **curation backlog** (`src/data_foundry/curation/`) that replaces
  the legacy curation Google Sheet. The source of truth is **one markdown record
  per candidate dataset** (YAML front-matter for the structured/dropdown fields +
  a free-text body for `## Comments` / `## Reference`) under `curation/records/`.
  Add or triage a dataset by creating/editing its `<unique_name>.md` file — by
  hand, with an agent, or via the dashboard. A local **Sheets-like dashboard**
  (`data-foundry-curation serve` → http://127.0.0.1:8765) edits those records in
  place and ships a built-in **Guidelines** tab (the curation criteria, from the
  paper). The per-record schema is `CurationRecord` (`curation/record.py`); the
  editable dropdown vocabularies live in `curation/vocabularies.yaml`. The CLI
  (`data-foundry-curation -h`) also covers `import-sheet`, `validate`, `export`,
  and `build-site` (a read-only static site). That static site is published to
  GitHub Pages at https://tabarena.github.io/data-foundry/ — regenerated from
  `curation/records/` on every push to `main` by `.github/workflows/pages.yaml`,
  so editing a record and merging to `main` is what updates the public site.

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

The skill writes a 21-cell notebook based on
`datasets/_template/_template.ipynb`. Read the template before writing so
the JSON structure is exact.

### 2. Verifying a filled-in notebook before it ships

Once the curator has filled in and run the notebook, the `/verify-dataset` slash
command ([`.claude/commands/verify-dataset.md`](.claude/commands/verify-dataset.md))
is the second pass: it runs `bundle_checks` for the mechanical invariants and then
works a 13-item **judgment rubric** for what code cannot settle — is the link really
the original source, does the split regime match the real application, would every
feature have been known at prediction time, do the `curation_comments` describe what
the code actually does, does the BibTeX cite the right work. Verdicts are advisory;
`cannot-verify` is a valid outcome and must never be reported as `pass`.

### 3. Helping a curator triage the backlog (curation dashboard + guidelines)

The backlog is **one markdown record per candidate dataset** in `curation/records/`
(`<unique_name>.md`: YAML front-matter for structured/dropdown fields + a body with
`## Comments` / `## Reference`).

To assist, run the **`/curate`** slash command
([`.claude/commands/curate.md`](.claude/commands/curate.md)). It starts the local
dashboard (`data-foundry-curation serve` → http://127.0.0.1:8765) and, importantly,
**loads the curation guidelines** — the IID/non-IID background, the dataset
*selection criteria*, and the *processing* conventions. **Read those guidelines
before advising** whether a dataset belongs in the benchmark or how to process it;
they encode decisions (IID vs temporal vs grouped, the selection criteria, the
processing conventions) you would otherwise guess at. The guidelines are summarized
in the skill and rendered in full in the dashboard's **Guidelines** tab
(`src/data_foundry/curation/static/guidelines.html`).

Add or triage a dataset by creating/editing its `<unique_name>.md` record (by hand,
with an agent, or in the dashboard); the dashboard and the `build-site` export both
read these files. The per-record schema is `CurationRecord` (`curation/record.py`);
dropdown options live in `curation/vocabularies.yaml`. `curation/_template.md` is a
copy-me, field-by-field guide.

**`data_foundry_status` is a merged multi-tag field** holding both work state
(`DF: Yes` / `WIP (DF)` / `WIP (Triage)` / `DF: Much work` / `DF: Suspended`) and shipped-collection
membership (`TabArena (v0.1)`, `BeyondArena`). Only datasets under `datasets/beyond_iid/`
(and the v0.1 set) carry a collection tag. **`DF: …` with no collection tag is a valid,
intentional state** — the dataset is in Data Foundry but not in a shipped collection
(it lives under `datasets/_maintenance/` — deprecated / suspended / out-of-scope — or
`datasets/_dev/`); do not "fix" it by adding a collection tag. See
`datasets/_maintenance/_deprecated/README.md`. (The separate `collections` field is only
for *external* benchmarks the dataset also appears in: TabSTAR, TabRed, CARTE/TARTE, ….)

### 4. Extending the package (schema, container, collections, examples)

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

### 5. Curation tooling work (checks, recommended splits, helpers)

**There are three check layers; put a new check in the right one.**

| Layer | Where | Scope |
|---|---|---|
| creation-time | `schema.py` `__post_init__` | coherence of *one* metadata object, no DataFrame needed (e.g. `group_labels` requires `group_on`, `time_horizon` requires its unit). Runs on every `CuratedContainer.load`, so a new rule here **must hold for every already-shipped container** — verify against the BeyondArena collection before making one hard. |
| exploratory | `dataset_checks.run_all_checks(...)` | statistics a human reads while curating. Returns five DataFrames whose rendered output is committed in the notebooks — don't change its output shape lightly. |
| post-hoc / bundle | `bundle_checks.py` | *cross-referential* checks over the assembled bundle (DataFrame + task + splits + dataset metadata) and, after export, the save/load round-trip. This is the default home for anything new. |

* `bundle_checks.run_bundle_checks(container)` returns a `BundleCheckReport`
  (errors / warnings / infos, each with a stable `slug`); the notebook calls
  `report.raise_if_errors()` before `save()`, and
  `verify_saved_container(save_path, container=...)` after it. A check that
  fires on a legitimately unusual dataset is accepted via `ignore=[slug]` in
  the notebook, with a reason.
* When adding a check, calibrate it against the shipped collection before
  choosing its severity (`error` only for "no consumer can use this"), and
  keep O(rows x cols) work behind the `heavy_cell_budget` guard.
* `dataset_checks.run_all_checks(...)` returns five DataFrames — see
  `simple_metadata_exploration_v2.py` (in `scripts/beyond_arena/`) for how
  the warehouse-wide stats are computed; that file's dtype categorization
  is the reference for `CuratedContainer._feature_dtype_counts`.
* `curation_recommendations.py` has three flavors — IID, grouped, temporal.
  IID and grouped have automated helpers; temporal splits are still
  manual.

### 6. Repo plumbing (CI, packaging, release)

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
| Public read-only backlog (GitHub Pages) | [tabarena.github.io/data-foundry](https://tabarena.github.io/data-foundry/) · [`.github/workflows/pages.yaml`](.github/workflows/pages.yaml) |
| Start the dashboard + load curation context | [`.claude/commands/curate.md`](.claude/commands/curate.md) |
| Curation guidelines (selection criteria + processing) | [`src/data_foundry/curation/static/guidelines.html`](src/data_foundry/curation/static/guidelines.html) |
| Container save/load + describe | [`src/data_foundry/curation_container.py`](src/data_foundry/curation_container.py) |
| Bundle integrity checks (post-hoc + post-export) | [`src/data_foundry/bundle_checks.py`](src/data_foundry/bundle_checks.py) |
| Collections + cache helpers | [`src/data_foundry/collections/`](src/data_foundry/collections/) |
| Notebook scaffolding skill | [`.claude/commands/new-dataset.md`](.claude/commands/new-dataset.md) |
| Verify a filled-in notebook / bundle (checks + judgment rubric) | [`.claude/commands/verify-dataset.md`](.claude/commands/verify-dataset.md) |
| Browse / prefetch a collection | [`.claude/commands/browse-collection.md`](.claude/commands/browse-collection.md) |
| Load a single dataset | [`.claude/commands/get-dataset.md`](.claude/commands/get-dataset.md) |
| Fit + score a model on a dataset | [`.claude/commands/benchmark-dataset.md`](.claude/commands/benchmark-dataset.md) |
| Notebook template | [`datasets/_template/_template.ipynb`](datasets/_template/_template.ipynb) |
| Examples (use-case anchors) | [`examples/`](examples) |
