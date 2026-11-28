# CLAUDE.md

Guidance for Claude Code (and other AI assistants) working in this repo.

This file is intentionally short. The brief on the code (what the package is, where a change goes, the conventions,
the things that look like blockers but aren't) is [**AGENTS.md**](AGENTS.md); the curation work runs through the
skills in `.claude/skills/`. Read AGENTS.md first.

## TL;DR

* **Repo:** [Data Foundry](README.md), the schema and curation toolkit for the tabular datasets behind BeyondArena
  and TabArena.
* **The knowledge every skill uses** is in two reference skills (knowledge only, no workflow):
  [`knowledge-curation`](.claude/skills/knowledge-curation/SKILL.md) (how we decide and curate, independent of the
  tooling, as ranked rules: read `principles.md` first) and
  [`knowledge-data-foundry`](.claude/skills/knowledge-data-foundry/SKILL.md) (how this repo implements it, and the
  house rules). The workflow skills link the exact file at each step.
* **The curation commands** (the overview for people is [`.claude/skills/README.md`](.claude/skills/README.md));
  in each of the two stages the AI works and the curator verifies:
  * `/screen-candidates`: a quick pass from the source link (nothing built) that fills the curation record
    (`curation/records/<name>.md`), rejects the obvious cases and sets a priority 1-5; also "check X";
  * `/review-screened-candidates`: the curator verifies the screening in the local dashboard
    (`.venv/bin/python -m data_foundry.curation.cli serve`);
  * `/add-dataset`: the v2 folder (`dataset.py` + generated `README.md`), checks and probes, then a review panel of
    agents (`.claude/agents/`); the open questions go into the record's `## Review`; also "is X ready?";
  * `/review-added-datasets`: the curator decides on the review page built from the records' `## Review` sections;
    the decisions are checked for consistency and applied;
  * `/review-split-tree`: the split decision tree as a page to read and review.
* **Claims (who works on what):** a live board on the remote's `claims` branch
  (`data-foundry-curation claims list|claim|release`,
  [`claims.md`](.claude/skills/knowledge-data-foundry/references/claims.md)). Claim records before working on them
  and leave the ones another curator holds alone.
* **Builds** happen only on the curator's ask
  ([`rebuild.md`](.claude/skills/knowledge-data-foundry/references/rebuild.md)).
* **Before changes land:** `pytest -q && uvx ruff@0.15.15 check . && uvx ruff@0.15.15 format --check .` (CI runs the
  same; another ruff version formats differently).
* **Conventions:** `from __future__ import annotations` is mandatory; lines ≤120 chars; Google-style docstrings; no
  commits, pushes or PRs without an explicit human ask.
* **Pull requests:** read [`pull_requests.md`](.claude/skills/knowledge-data-foundry/references/pull_requests.md)
  before opening, updating, stacking or merging one.
* **TabArena v0.2 working copy** (`datasets/_dev/tabarena-v0pt2/`, one v2 folder per dataset; its
  `GETTING_STARTED.md` is the way in): every change there gets a dated entry in its `CHANGELOG.md`. A dataset's
  review is the `## Review` section of its record, never a `REVIEW.md` in its folder, and is never deleted. An item
  that spans datasets becomes a draft rule in the knowledge skills or a GitHub issue.
* **v2 only for new work:** never add or re-curate a dataset with v1 (the BeyondArena notebooks);
  [DATA_FOUNDRY_V1.md](DATA_FOUNDRY_V1.md) is the one page about v1.
* **Writing style:** [`style.md`](.claude/skills/knowledge-curation/references/style.md) ("AI Writing Tropes to
  Avoid") applies to docstrings, markdown, commit messages, PR bodies and chat replies.

## Using shipped datasets (load, browse, benchmark)

No slash command for these; [`docs/benchmark_integration.md`](docs/benchmark_integration.md) is the page for fitting
and scoring, the examples the reference ([`examples/README.md`](examples/README.md)).

* **Load one:** `BEYOND_ARENA.get_dataset(name_or_uuid)` from `data_foundry.collections` (both container formats),
  then `container.describe()` and `container.verify()`. How it was built: the record `curation/records/<name>.md`.
* **Browse a collection:** `list_collections()`, `get_collection(name)`, `iter_containers()`, `prefetch()`; the last
  two download several GB, so ask first.
* **Fit and score:** `task = container.task()` gives the folds within the row budget (`task.folds()`), the inputs
  (`task.X(rows)`, a SMILES left out unless `special="encode"` or `"raw"`), the training weight
  (`task.train_weight(rows)`), an inner validation split by the regime (`task.validation_split(rows)`, from
  `task.split_roles`), the scorer (`task.score(y_true, y_pred, rows)`) and the error (`task.error(score)`); never
  re-split, never fit on a scoring column. See `examples/minimal_adapter.py` and `examples/benchmark_container.py`.
