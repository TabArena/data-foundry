# CLAUDE.md

Guidance for Claude Code (and other AI assistants) working in this repo.

This file is intentionally short. The full agent-facing brief — what the
repo is, the high-value use cases, the conventions to follow, and the
gotchas that look like blockers but aren't — lives in
[**AGENTS.md**](AGENTS.md). Read that first.

## TL;DR

* **Repo:** [Data Foundry](README.md) — schema and curation toolkit for
  tabular datasets behind BeyondArena / TabArena.
* **You touch code mainly to:**
  * triage candidate datasets — the **curation log** of one markdown record per
    candidate under `curation/records/`; the `/triage-candidates` skill
    ([`.claude/skills/triage-candidates/SKILL.md`](.claude/skills/triage-candidates/SKILL.md))
    starts the local dashboard (`.venv/bin/python -m data_foundry.curation.cli serve`) and loads the
    curation guidelines,
  * check one candidate the curator is looking at — the `/check-candidate <unique_name>`
    skill ([`.claude/skills/check-candidate/SKILL.md`](.claude/skills/check-candidate/SKILL.md))
    traces the source and writes a cited second opinion into the record,
  * process a decided candidate — scaffold its v2 dataset folder (`dataset.py`
    class + `explore.ipynb` + generated `README.md`, API in `src/data_foundry/v2/`)
    via the `/add-dataset` skill
    ([`.claude/skills/add-dataset/SKILL.md`](.claude/skills/add-dataset/SKILL.md)),
  * extend the package (`src/data_foundry/`),
  * update examples (`examples/`) when an API changes.
* **Before changes land:** `pytest -q && ruff check . && ruff format --check .`
* **Conventions:** `from __future__ import annotations` is mandatory; lines
  ≤120 chars; Google-style docstrings; no commits/pushes without explicit
  human ask.
* **TabArena v0.2 working copy:** `datasets/_dev/tabarena-v0pt2/` holds one
  v2 folder per dataset of TabArena v0.2 (migrated from the BeyondArena notebooks
  and rebuilt on 2026-10-01; its `README.md` has the table of datasets and UUIDs and
  how to rebuild them). Every change there (edited definition or helper file, added or
  removed dataset, a re-run that makes a new container) gets a dated entry in its
  `CHANGELOG.md`, and a new, removed or rebuilt dataset also updates the table in its
  `README.md`. A dataset retired to `No (Retired)` is removed from the copy.
* **Writing style:** AGENTS.md ends with "AI Writing Tropes to Avoid" — it
  applies to docstrings, markdown, commit messages, and chat replies.

## Using shipped datasets (load, browse, benchmark)

No slash command for these; the examples are the reference.

* **Load one:** `BEYOND_ARENA.get_dataset(name_or_uuid)` from `data_foundry.collections`, then
  `container.describe()`. Check integrity with `container.checksum == container._create_checksum()`.
  How it was built: the record `curation/records/<name>.md` (`notebook_path`, `v2_path`, `## Comments`).
  See `examples/download_beyond_arena_dataset.py`, `examples/load_curated_container.py`.
* **Browse a collection:** `list_collections()`, `get_collection(name)`, `BEYOND_ARENA.unique_names`,
  `iter_containers()`, `prefetch()`. `prefetch` / `iter_containers` download several GB, so ask
  first. The cache is `~/.cache/data_foundry/<collection>/` (`$DATA_FOUNDRY_CACHE`, `clear_cache()`,
  `force_download=True`). See `examples/download_all_beyond_arena_datasets.py`,
  `examples/data_foundry_data_regimes.py`.
* **Fit a model:** iterate `container.experiment_metadata.splits` as `{repeat: {fold: (train_idx,
  test_idx)}}` and never re-split or shuffle; the splits encode the regime (IID / temporal / grouped).
  Score with `task_metadata.objective_metric_name` (`rmse`, `roc_auc`, `log_loss`). Features can be
  categorical, string or datetime, so pick a model that takes mixed dtypes. See
  `examples/benchmark_on_beyond_arena.py`.

See [AGENTS.md](AGENTS.md) for the long form.
