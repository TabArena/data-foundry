# AGENTS.md

Guidance for coding agents (Claude Code, Cursor, Aider and others) working inside the **Data Foundry** repository:
what the code is, where a change goes, the conventions, and the things that look like blockers but aren't. People
start with [`README.md`](README.md); curation work runs through the skills in `.claude/skills/`.

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
  and resolves them against a local warehouse or a Hugging Face mirror, with cache + force-download semantics
  (`collections/`). It is how every collection ships, both container formats: BeyondArena today, the TabArena v0.2
  collection next;
* the format-2 **task metadata** and its consumer side: `schema.py` (`DatasetMetadataV2`,
  `PredictiveMLTaskMetadataV2`, `Grouping`, `MetricSpec`), the task view `container.task()` (`task.py`), `metrics.py`,
  `sampling.py` (the row budget's train sampler), `special/` and `encodings.py`; format 1 is in `v1/`;
* the **v2 dataset format** (`definition/`): one `dataset.py` class per dataset, its split protocol, the checks
  that need the definition class (`checks.py`) and generated README;
* the **checks** (`checks/`): the bundle checks of a container and the round trip of a saved one (`bundle.py`), the
  checks of a v2 task (`task.py`, `groups.py`), the split protocol's numbers and checks (`protocol.py`), the README's
  summary tables (`tables.py`), and the registry of every check slug (`registry.py`). `checks/` imports nothing of
  `definition/` (a test holds it); `definition/` uses `checks/`. The consumer side (`task.py`, the task view;
  `metrics.py`, `sampling.py`, `special/`, `encodings.py`) loads none of `definition/` and `checks/`;
* the **probes** (`probes/`, the `probes` extra): leak, task, group, hidden-group, time, dtype and generated-data probes
  on a definition or a built container, run as `data-foundry probe <probe> NAME...`;
* a git-native **curation backlog** (`curation/`): one markdown record per candidate dataset under
  `curation/records/` (YAML front matter for the structured fields, then `## Comments`, `## Review`, the dataset's
  review, and `## Reference`). The schema is `CurationRecord` (`curation/record.py`), the dropdown vocabularies are in
  `curation/vocabularies.yaml`, and `curation/review.py` is the one parser of a `## Review` section. The CLI
  (`.venv/bin/python -m data_foundry.curation.cli -h`; `data-foundry` and `data-foundry-curation` are the same command)
  has `serve` (the local dashboard at http://127.0.0.1:8765, whose Guidelines page renders the knowledge skills),
  `validate`, `sync-notebooks` (refreshes each record's `notebook_path` and `v2_path`), `export`, `dataset` (new /
  check / build / list for v2 folders), `probe`, `claims` and `build-site`. The static site is published to
  https://tabarena.github.io/data-foundry/ from `curation/records/` on every push to `main` (`pages.yaml`), so merging
  a record change is what updates the public site.

The actual curation work happens in `datasets/` ([`datasets/README.md`](datasets/README.md) maps it): every new
dataset is a v2 folder (`dataset.py` + a generated `README.md`; its review is in its curation record), and the
TabArena v0.2 working copy is `datasets/_dev/tabarena-v0pt2/` — see
[`CONTRIBUTING_DATASETS.md`](CONTRIBUTING_DATASETS.md). The shipped BeyondArena datasets were built with Data Foundry
v1 (notebooks under `datasets/beyond_iid/`). **Never add or re-curate a dataset with v1**;
[`DATA_FOUNDRY_V1.md`](DATA_FOUNDRY_V1.md) is the one page about v1 (reading, checking and maintaining those notebooks
and their format-1 containers).

---

## High-leverage use cases for an agent

Curation work runs through the skills in `.claude/skills/`; the overview for people (the commands, the pipeline, the
review panel, how decisions are checked) is [`.claude/skills/README.md`](.claude/skills/README.md). The knowledge they
apply lives in two reference skills, read by every workflow at the step that needs it:

* [`knowledge-curation`](.claude/skills/knowledge-curation/SKILL.md): how we decide whether a dataset belongs in
  TabArena and how we curate it, independent of the tooling, as ranked rules with IDs and strengths (principles,
  scope, use case, leaks, splits, provenance, task quality, cleaning; evidence, the verification checklist, writing
  for the curator);
* [`knowledge-data-foundry`](.claude/skills/knowledge-data-foundry/SKILL.md): how this repository implements it
  (records, dashboard, the v2 `dataset.py` API, checks and probe commands, the working copy, batch runs) and the house
  rules.

The workflows form one pipeline of two stages, in each of which the AI works and the curator verifies: screening
(`/screen-candidates`, a quick pass from the source with a priority, then `/review-screened-candidates` in the
dashboard) and adding (`/add-dataset`, which builds the definition, runs a review panel of agents and leaves the open
questions in each record's `## Review`, then `/review-added-datasets` on the review page); `/review-split-tree`
shows the split decision tree for review. Builds
([`rebuild.md`](.claude/skills/knowledge-data-foundry/references/rebuild.md)) and commits happen only on the curator's
ask. Read the skill before doing its task; it names the knowledge files to read at each step. The dashboard's
Guidelines page renders the skills README and the two knowledge skills.

### Extending the package (schema, container, collections, examples)

When changing core code:

* **Tests live in `tests/`.** Run `pytest -q` after any change (about two to five minutes; a single file with
  `pytest tests/test_x.py` while iterating).
* **Linting:** `uvx ruff@0.15.15 check .` and `uvx ruff@0.15.15 format .` (the pinned version CI runs; the frozen v1
  trees are excluded in `pyproject.toml`). `from __future__ import annotations` is mandatory in every file; 120-char
  lines; Google-style docstrings.
* **Examples in `examples/` are part of the docs surface.** When you add a
  feature, add or update the matching example, and (only if it's a major
  use case) link it from `README.md`.
* **`describe()` methods** on `DatasetMetadataV2`, `PredictiveMLTaskMetadataV2`, `PredictiveMLSplitsMetadata`
  (`schema.py`), the format-1 `DatasetMetadata` and `PredictiveMLTaskMetadata` (`v1/`) and `CuratedContainer` are the
  human-facing surface: keep them in sync if you add or rename schema fields.
* **Two container formats, one reader.** `CuratedContainer.format_version` is 2 for a v2 definition's container
  (`PredictiveMLTaskMetadataV2`: the group fields stored once, in `grouping`) and 1 for the shipped BeyondArena
  containers (`PredictiveMLTaskMetadata`, built with v1). Keep the format-1 classes at the shape
  the shipped checksums encode; a new task field for v2 goes into the format-2 class. Code that reads both formats
  uses `task_metadata.group_on` / `group_labels` / `group_time_on` (views of `grouping` in format 2);
  `container.grouping` raises for format 1.

### Curation tooling work (checks, recommended splits, helpers)

**There are four check layers; put a new check in the right one.** Every finding's slug is listed in
`src/data_foundry/checks/registry.py` with its severities, stage and whether a definition may accept it; a new slug
goes there too (a test fails otherwise), and the page
[`check_slugs.md`](.claude/skills/knowledge-data-foundry/references/check_slugs.md) is regenerated from it.

| Layer | Where | Scope |
|---|---|---|
| creation-time | `schema.py` `__post_init__` | coherence of *one* metadata object, no DataFrame needed (e.g. `group_labels` requires `group_on`, `time_horizon` requires its unit, a `Grouping` with `prediction_unit="group"` needs an aggregation). Runs on every `CuratedContainer.load`, so a new rule here **must hold for every already-shipped container** — verify against the BeyondArena collection before making one hard. |
| summary tables | `checks/tables.py` `run_all_checks(...)` | the tables of each dataset's README ("Data checks": feature summary, numeric and categorical statistics, the target). Statistics, no findings. |
| post-hoc / bundle | `checks/bundle.py` | *cross-referential* checks over the assembled bundle (DataFrame + task + splits + dataset metadata) and, after export, the save/load round-trip. It also checks the shipped format-1 containers: keep its format-1 behaviour unchanged. The split protocol follows the container format: format 2 by `checks/protocol.py` `protocol_checks` (called from here). |
| v2 definition | `definition/checks.py`, `checks/task.py`, `checks/groups.py`, `checks/protocol.py`, `_validate_definition` in `definition/dataset.py` | rules of the v2 protocol and the v2 definition format, run by `dataset check` / `dataset build` next to the bundle checks. The default home for a new v2 rule. `_validate_definition` refuses a malformed definition before anything runs. |

* `checks.run_bundle_checks(container)` returns a `BundleCheckReport`
  (errors / warnings / infos, each with a stable `slug`). `dataset build` raises on errors before saving and runs
  `verify_saved_container` after it. A warning that fires on a legitimately unusual dataset is accepted with a
  reason: `accepted_check_warnings = {slug: reason}` in the definition. An error is accepted only when the registry
  lists it in `ACCEPTABLE_ERRORS` with the rule that allows the exception.
* When adding a check, calibrate it against the shipped collection before
  choosing its severity (`error` only for "no consumer can use this"), and
  keep O(rows x cols) work behind the `heavy_cell_budget` guard.
* `checks.run_all_checks(...)` returns the four README tables by name; the dtype categorization of a container's
  features is `CuratedContainer._feature_dtype_counts`.
* Splits: definitions use `src/data_foundry/definition/splits.py` (the v2 protocol, declarative `TemporalSplits`). The v1
  helpers of the BeyondArena notebooks were removed on 2026-11-12 (in git at `6cc3c945`;
  [`DATA_FOUNDRY_V1.md`](DATA_FOUNDRY_V1.md)).

### Repo plumbing (CI, packaging, release)

`pyproject.toml` carries the PyPI metadata and the extras. CI (`.github/workflows/`) runs the tests and the pinned
ruff on every PR (`main.yaml`), publishes the static backlog site on every push to `main` (`pages.yaml`), and a dev
wheel when a push to `main` changed the package (`dev-release.yaml`). The release flow (`scripts/release.sh`, the tag
push that fires `release.yaml`, the prereleases) is in [`DEVELOPMENT.md`](DEVELOPMENT.md). Don't bump versions or
publish without explicit human authorization.

---

## Conventions you must follow

* **Always read before writing.** The schema fields and `describe()` output
  are user-facing; pattern-match the existing style rather than inventing
  a new one.
* **`from __future__ import annotations`** at the top of every `.py` file.
* **Don't commit changes unless the user explicitly asks.** Same for
  pushes, PRs, and PyPI publishes.
* **Pull requests follow
  [`pull_requests.md`](.claude/skills/knowledge-data-foundry/references/pull_requests.md);** read it before opening,
  updating, stacking or merging one.
* **Don't write README files, planning docs, or analysis files** unless
  asked. The repo intentionally has very few `.md` files.
* **Don't add comments that describe what the code does** — only *why*,
  when the why is non-obvious.
* **Notebooks must stay valid JSON** (the v1 notebooks). Edit them with
  `nbformat` or as structured data; do not hand-edit the cell `source` array without verifying the result parses.
* **Prose you write follows
  [`style.md`](.claude/skills/knowledge-curation/references/style.md)** ("AI Writing Tropes to Avoid"): docstrings,
  markdown, commit messages, PR bodies and chat replies alike.

---

## Things that look like blockers but aren't

* **`local-data-warehouse/` is gitignored** and may be empty on a fresh clone. That's fine: only the two toy containers
  (`src/data_foundry/examples/toy_container/`, one per container format) ship in-tree; everything else is downloaded
  on demand through the collections API.
* **`huggingface_hub` is a core dependency, imported lazily:** only a cache *miss* of `prefetch` / `get_dataset`
  imports it and reaches the network. A warm cache never imports it, and the test suite needs no Hugging Face login.
* **The toy containers are regenerated by `scripts/build_toy_container.py`,** not edited by hand. If a test fails on a
  UUID or checksum mismatch, the fix is to regenerate, not to update the test expectation.

---

## Pointers

| Topic | Read |
|---|---|
| Repo overview, install, quickstart | [`README.md`](README.md) |
| Curation contribution flow | [`CONTRIBUTING_DATASETS.md`](CONTRIBUTING_DATASETS.md) · [getting started for TabArena v0.2](datasets/_dev/tabarena-v0pt2/GETTING_STARTED.md) |
| The `datasets/` tree | [`datasets/README.md`](datasets/README.md) |
| Data Foundry v1 (the BeyondArena notebooks, format-1 containers) | [`DATA_FOUNDRY_V1.md`](DATA_FOUNDRY_V1.md) |
| Schema definitions | [`src/data_foundry/schema.py`](src/data_foundry/schema.py) |
| Curation backlog (records, dashboard, import/export) | [`src/data_foundry/curation/`](src/data_foundry/curation/) |
| Curation records + dropdown vocab (data) | [`curation/`](curation) |
| Public read-only backlog (GitHub Pages) | [tabarena.github.io/data-foundry](https://tabarena.github.io/data-foundry/) · [`.github/workflows/pages.yaml`](.github/workflows/pages.yaml) |
| Curation knowledge (selection, use case, splits, leaks, cleaning, task quality, provenance, verification) | [`.claude/skills/knowledge-curation/SKILL.md`](.claude/skills/knowledge-curation/SKILL.md) |
| Data Foundry knowledge (records, dashboard, `dataset.py`, checks and probes, working copy, house rules) | [`.claude/skills/knowledge-data-foundry/SKILL.md`](.claude/skills/knowledge-data-foundry/SKILL.md) |
| The curation skills for people (commands, pipeline, review panel) | [`.claude/skills/README.md`](.claude/skills/README.md) |
| Screen candidates (quick pass, priority) and review the screening (dashboard) | [`.claude/skills/screen-candidates/SKILL.md`](.claude/skills/screen-candidates/SKILL.md) · [`.claude/skills/review-screened-candidates/SKILL.md`](.claude/skills/review-screened-candidates/SKILL.md) |
| Leak checks and the probes | [`leak_checks.md`](.claude/skills/knowledge-curation/references/leak_checks.md) · [`checks_and_probes.md`](.claude/skills/knowledge-data-foundry/references/checks_and_probes.md) · [`src/data_foundry/probes/`](src/data_foundry/probes/) |
| Container save/load + describe | [`src/data_foundry/curation_container.py`](src/data_foundry/curation_container.py) |
| The checks (bundle, task, definition, saved files) and the registry of their slugs | [`src/data_foundry/checks/`](src/data_foundry/checks/) · [`check_slugs.md`](.claude/skills/knowledge-data-foundry/references/check_slugs.md) |
| Collections + cache helpers | [`src/data_foundry/collections/`](src/data_foundry/collections/) |
| Add a dataset: its v2 folder, checks, probes and the review panel ("is X ready?" too) | [`.claude/skills/add-dataset/SKILL.md`](.claude/skills/add-dataset/SKILL.md) · [`src/data_foundry/definition/`](src/data_foundry/definition/) |
| Review a batch of added datasets (the review page) | [`.claude/skills/review-added-datasets/SKILL.md`](.claude/skills/review-added-datasets/SKILL.md) |
| Rebuild the TabArena v0.2 working copy and verify the build | [`rebuild.md`](.claude/skills/knowledge-data-foundry/references/rebuild.md) |
| Load / browse / benchmark shipped datasets (both formats: `container.task()` gives the folds within the row budget, the inputs, the weights, the scorer and the error) | [`docs/benchmark_integration.md`](docs/benchmark_integration.md) · [`CLAUDE.md`](CLAUDE.md) (*Using shipped datasets*) · [`examples/`](examples) · [`src/data_foundry/task.py`](src/data_foundry/task.py) |
| Pull requests: the body, one PR per independent change, stacked PRs with `gh stack` | [`pull_requests.md`](.claude/skills/knowledge-data-foundry/references/pull_requests.md) |
| Dataset template | [`datasets/_template/`](datasets/_template/) |
| Examples (use-case anchors) | [`examples/`](examples) · [`examples/README.md`](examples/README.md) |
