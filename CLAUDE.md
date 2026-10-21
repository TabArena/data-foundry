# CLAUDE.md

Guidance for Claude Code (and other AI assistants) working in this repo.

This file is intentionally short. The full agent-facing brief — what the
repo is, the high-value use cases, the conventions to follow, and the
gotchas that look like blockers but aren't — lives in
[**AGENTS.md**](AGENTS.md). Read that first.

## TL;DR

* **Repo:** [Data Foundry](README.md) — schema and curation toolkit for
  tabular datasets behind BeyondArena / TabArena.
* **The knowledge every skill uses** is in two reference skills (knowledge only, no workflow):
  [`knowledge-curation`](.claude/skills/knowledge-curation/SKILL.md) (how we decide and curate, independent of the
  tooling, as ranked rules: read `principles.md` first) and
  [`knowledge-data-foundry`](.claude/skills/knowledge-data-foundry/SKILL.md) (how this repo implements it, and the
  house rules). The workflow skills link the exact file at each step; the dashboard's Guidelines page renders both.
* **The curation commands** (overview for people: [`.claude/skills/README.md`](.claude/skills/README.md)); two
  stages, in each the AI works and the curator verifies:
  * screen candidates — `/screen-candidates`
    ([`.claude/skills/screen-candidates/SKILL.md`](.claude/skills/screen-candidates/SKILL.md)): a quick pass from the
    source link (nothing built) that fills the **curation record** (`curation/records/<name>.md`), rejects the obvious
    cases and sets a priority 1-5; also "check X" on a record without a folder,
  * the curator verifies the screening — `/review-screened-candidates`
    ([`.claude/skills/review-screened-candidates/SKILL.md`](.claude/skills/review-screened-candidates/SKILL.md)):
    the local dashboard (`.venv/bin/python -m data_foundry.curation.cli serve`) on its Screening queue,
  * add a dataset — `/add-dataset`
    ([`.claude/skills/add-dataset/SKILL.md`](.claude/skills/add-dataset/SKILL.md)): the v2 folder (`dataset.py`
    class + `explore.ipynb` + generated `README.md`, API in `src/data_foundry/v2/`), checks and probes, then a review
    panel of agents (`.claude/agents/`); the open questions go into the folder's `REVIEW.md`; also "is X ready?",
  * the curator reviews what was added — `/review-added-datasets`
    ([`.claude/skills/review-added-datasets/SKILL.md`](.claude/skills/review-added-datasets/SKILL.md)): the review
    page from the `REVIEW.md` files; the curator's decisions are checked for consistency and applied.
* **Builds** happen only on the curator's ask
  ([`rebuild.md`](.claude/skills/knowledge-data-foundry/references/rebuild.md)). Otherwise you touch code to extend
  the package (`src/data_foundry/`) and update examples (`examples/`) when an API changes.
* **Before changes land:** `pytest -q && ruff check . && ruff format --check .`
* **Conventions:** `from __future__ import annotations` is mandatory; lines
  ≤120 chars; Google-style docstrings; no commits/pushes without explicit
  human ask.
* **TabArena v0.2 working copy:** `datasets/_dev/tabarena-v0pt2/` holds one
  v2 folder per dataset of TabArena v0.2 (migrated from the BeyondArena notebooks
  and rebuilt on 2026-10-02; its `README.md` has the table of datasets and UUIDs and
  how to rebuild them, its `GETTING_STARTED.md` the way in for a new curator). Every change there (edited definition or helper file, added or
  removed dataset, a re-run that makes a new container) gets a dated entry in its
  `CHANGELOG.md`, and a new, removed or rebuilt dataset also updates the table in its
  `README.md`. A dataset retired to `No (Retired)` is removed from the copy. Open questions for the curator live in
  a folder's `REVIEW.md` until they are settled.
* **v2 only for new work:** every new dataset is a v2 folder. The BeyondArena notebooks are Data Foundry v1;
  never add or re-curate a dataset with v1. [DATA_FOUNDRY_V1.md](DATA_FOUNDRY_V1.md) is the one page about v1.
* **Writing style:** AGENTS.md ends with "AI Writing Tropes to Avoid" — it
  applies to docstrings, markdown, commit messages, and chat replies.

## Using shipped datasets (load, browse, benchmark)

No slash command for these; the examples are the reference ([`examples/README.md`](examples/README.md)). A
collection is how datasets ship (BeyondArena today, the TabArena v0.2 collection next); the calls below work for
both container formats.

* **Load one:** `BEYOND_ARENA.get_dataset(name_or_uuid)` from `data_foundry.collections`, then
  `container.describe()`. Check integrity with `container.verify()` (or `get_dataset(..., verify=True)`).
  How it was built: the record `curation/records/<name>.md` (`notebook_path`, `v2_path`, `## Comments`).
  See `examples/load_curated_container.py`, `examples/benchmark_on_beyond_arena.py`.
* **Browse a collection:** `list_collections()`, `get_collection(name)`, `BEYOND_ARENA.unique_names`,
  `iter_containers()`, `prefetch()`. `prefetch` / `iter_containers` download several GB, so ask
  first. The cache is `~/.cache/data_foundry/<collection>/` (`$DATA_FOUNDRY_CACHE`, `clear_cache()`,
  `force_download=True`). See `examples/download_all_beyond_arena_datasets.py`,
  `examples/data_foundry_data_regimes.py`.
* **Fit a model:** iterate `container.experiment_metadata.splits` as `{repeat: {fold: (train_idx,
  test_idx)}}` and never re-split or shuffle; the splits encode the regime (IID / temporal / grouped).
  Format 2 (`container.format_version == 2`): score by the spec `task_metadata.objective_metric` with
  `data_foundry.v2.metrics.scorer(container)(y_test, y_pred, test_idx)`, and take the inputs from
  `feature_columns(container)` (`data_foundry.curation_container`), which drops the target, the group and the
  scoring columns (`task_metadata.scoring_columns`: metric inputs such as an era, never features). Format 1
  (BeyondArena): score with `task_metadata.objective_metric_name` (`rmse`, `roc_auc`, `log_loss`). Features can be
  categorical, string or datetime, so pick a model that takes mixed dtypes. See
  `examples/benchmark_on_beyond_arena.py`; without Data Foundry, `examples/read_metric_without_data_foundry.py`.

See [AGENTS.md](AGENTS.md) for the long form.
