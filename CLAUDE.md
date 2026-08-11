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
    candidate under `curation/records/`; the `/triage-candidates` slash command
    ([`.claude/commands/triage-candidates.md`](.claude/commands/triage-candidates.md))
    starts the local dashboard (`data-foundry-curation serve`) and loads the
    curation guidelines,
  * process a decided candidate — scaffold its curation notebook via the
    `/process-dataset` slash command
    ([`.claude/commands/process-dataset.md`](.claude/commands/process-dataset.md)),
  * extend the package (`src/data_foundry/`),
  * update examples (`examples/`) when an API changes.
* **Before changes land:** `pytest -q && ruff check . && ruff format --check .`
* **Conventions:** `from __future__ import annotations` is mandatory; lines
  ≤120 chars; Google-style docstrings; no commits/pushes without explicit
  human ask.
* **Writing style:** AGENTS.md ends with "AI Writing Tropes to Avoid" — it
  applies to docstrings, markdown, commit messages, and chat replies.

See [AGENTS.md](AGENTS.md) for the long form.
