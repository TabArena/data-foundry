---
name: triage-candidates
description: Triage candidate datasets in the curation backlog (`curation/records/`). Starts the local curation dashboard and loads the curation guidelines (IID vs non-IID, selection criteria, decision patterns, duplicates, processing conventions). Use when the user wants to open the dashboard, work the backlog, add or edit a candidate record, or asks whether a dataset belongs in the benchmark, which split it needs, or how to process it. Other dataset skills (check-candidate, verify-dataset) read its guidelines as their rubric.
user-invocable: true
---

# Triage candidates

Triage candidate datasets in the curation backlog: start the local dashboard and help the
user decide which candidates belong in the benchmark. Invoking this skill loads the
**curation guidelines** ([`references/curation_guidelines.md`](references/curation_guidelines.md)) into context so you can advise on selection and processing
decisions the way a human curator would.

## When to invoke

* The user wants to **open the curation dashboard** / work on the dataset backlog.
* The user asks whether a dataset **belongs in the benchmark**, what split it needs,
  or how to **process** it — answer using the guidelines (`references/curation_guidelines.md`).
* The user wants to **add, edit, or triage** a candidate dataset record.

For an independent deep-dive on one record the curator is looking at ("check X", "what did I miss"),
use `/check-candidate <unique_name>`: it runs the source-tracing protocol against these guidelines.
If the user instead wants to process an already-decided dataset (scaffold its v2
`dataset.py` folder), use `/add-dataset`; to check a filled-in definition, notebook or saved
bundle before it ships, use `/verify-dataset`.

## Step 1 — Start the dashboard

Run the server in the background, then point the user at the URL:

```bash
.venv/bin/python -m data_foundry.curation.cli serve            # → http://127.0.0.1:8765
# (equivalently: .venv/bin/python -m data_foundry.curation.cli serve)
```

Tell the user to open **http://127.0.0.1:8765** (hard-refresh once if the tab was already open). The page
polls the server's change token every 2 s and patches its table in place, so records you save from the
CLI / store API show up in the open tab within seconds, without losing scroll, filters or pins. The dashboard
edits the markdown records in place; the **📖 Guidelines** button opens the same
guidelines as `references/curation_guidelines.md`.

## How the backlog is stored

* The source of truth is **one markdown file per dataset** at
  `curation/records/<unique_name>.md`: YAML **front-matter** for the structured /
  dropdown fields, plus a body with `## Comments` and `## Reference`.
* **Add / triage a dataset** = create or edit its `.md` record — by hand, with you
  (the agent), or in the dashboard. Keep the front-matter valid YAML; empty fields
  are simply omitted.
* The per-record schema is `CurationRecord` in
  [`src/data_foundry/curation/record.py`](../../../src/data_foundry/curation/record.py)
  (fields: `unique_name`, `name`, `checked_by`, `data_foundry_status`, `suggestion`,
  `decision_markers`, `tags`, `collections`, `original_source`, `year`, `domain`,
  `required_split`, `problem_type`, `original_data_state`, `source_links`, `notebook_path`, `v2_path`,
  `comments`, `reference`, `needs_review`).
* **`notebook_path` is the record's own pointer to its curation notebook** — one dataset, one
  notebook, stored in the record rather than resolved from the tree. See the pointer rules
  in [`references/record_pointers.md`](references/record_pointers.md) for when to set and check them.
* Editable dropdown options live in `curation/vocabularies.yaml` (add new options
  there, via the dashboard's ＋ header buttons, or with `save_vocabularies`).
* **The `data_foundry_status` field is a merged multi-tag field** ("Data Foundry" column):
  it holds the *work state* (`DF: Yes`, `WIP (DF)`, `WIP (Triage)`, `DF: Much work`,
  `DF: Suspended`) **and** *benchmark-collection membership* (`TabArena (v0.1)`, `BeyondArena`).
  The two WIP values are mutually exclusive by meaning: `WIP (Triage)` = the verdict is still
  open (a `TBD -> …` / disputed suggestion) and someone is working on settling it;
  `WIP (DF)` = the verdict is a final `Yes` and the Data Foundry integration (the v2 `dataset.py`) is in
  progress. A record whose suggestion is not yet a final `Yes` must **not** carry `WIP (DF)`.
  Every dataset
  shipped in a collection (`datasets/_maintenance/_old_collections/tabarena-v0pt1`,
  `datasets/beyond_iid`) carries its collection tag(s) **plus `DF: Yes`**; there are 51
  TabArena and 142 BeyondArena (union 144). The `collections` field is now only for *external*
  benchmarks/collections (TabSTAR, TabRed, CARTE/TARTE, …), not our own.
* **`DF: Yes` (or any `DF: …`) with NO collection tag is a valid, intentional state**: the dataset
  is in Data Foundry but **not in a shipped collection** — it lives under `datasets/_maintenance/`
  (`_deprecated`, `_suspended`, `_out_of_scope/*`) or `datasets/_dev/`. Do **not** "fix" these by
  adding `BeyondArena`/`TabArena (v0.1)`. Only datasets under `datasets/beyond_iid/` (and the v0.1
  set) carry a collection tag. See `datasets/_maintenance/_deprecated/README.md`.
* The records are now the source of truth — the one-off migrations that built them from the
  legacy sheet / shipped collections (`import-sheet`, `reconcile-tabarena`) have been removed.
* `curation/_template.md` is a copy-me reference documenting how to fill every field
  (files starting with `_` in `records/` are skipped by the loader, so it never counts as a dataset).
* **The review queue is derived, not hand-set.** `needs_review` is recomputed from
  `CurationRecord.review_reasons()` on every save (server, CLI, scripts) — never edit it by
  hand. A record lands in the dashboard's **Review** pill when `review_reasons()` returns
  anything; today that means: an empty **required** field (`suggestion` → untriaged), a dropdown
  value not in `vocabularies.yaml`, `ai_unverified` (an AI triaged it, no human has verified —
  see below), or `ship_conflict` (carries a `TabArena (v0.1)`/`BeyondArena` tag but `suggestion`
  is not an accepted verdict — i.e. not `Yes`/`Yes (Disagreement)`/`No (Retired)`). To add a new automated check,
  extend `review_reasons()` (it is the single source of truth) and add a matching assertion in
  `tests/test_records_integrity.py`.
* After editing records, sanity-check with `.venv/bin/python -m data_foundry.curation.cli validate`.
* **Every new curation file goes into git.** A record you create under `curation/records/`, a
  changed `vocabularies.yaml`, or any other new file under `curation/` must be staged (`git add`)
  as soon as it exists — an untracked record is invisible to PRs, to the GitHub 📄 links and to
  other curators, and it is easy to forget. Staging is not committing: commits and pushes still
  need the human's explicit ask (CLAUDE.md), so before the session ends run `git status`, name
  every uncommitted curation change, and offer the commit.
* **Always reload a record from disk immediately before editing it.** The human edits the same
  files in the dashboard while you are thinking, so a record loaded earlier in the session, or the text you
  remember from reading it, is stale. Do the edit as one short step — `load_record` → change fields →
  recompute `needs_review` → `save_record` — and never write a record from a copy held across several
  turns. This applies to `vocabularies.yaml` and to every other file under `curation/` as well. If you
  notice the file changed between your read and your write, re-read it and redo the edit on the new
  content rather than overwriting.

## Load the guidelines before advising

Read [`references/curation_guidelines.md`](references/curation_guidelines.md) in full before you advise on any record. It holds how we decide whether a dataset belongs
in TabArena and how we curate the ones we keep: the IID / non-IID background, the selection criteria, the quick
decision patterns, the duplicate-check method, reading Kaggle sources, the suggestion values, how to read markers,
and the processing conventions. The rendered version is the dashboard's **Guidelines** tab
(`src/data_foundry/curation/static/guidelines.html`).

Read the other references when the task needs them:

* [`references/record_pointers.md`](references/record_pointers.md): the record's `notebook_path` and `v2_path`,
  which tree each must point into, and when to set and check them.
* [`references/dashboard.md`](references/dashboard.md): the dashboard features (status column, filters, pills,
  pins, copy-link) to explain to a curator.
* [`../check-candidate/references/leak_checks.md`](../check-candidate/references/leak_checks.md): the leak probes
  and what the 2026 BeyondArena leak audit decided for each kind of leak (drop, lag, re-split, keep on purpose,
  retire). Read it before calling a column a leak or a dataset leaky, and before advising how to fix one.

## Push back on weak reasoning (you may second-guess a decision)

You are a curator, not a rubber stamp. A decision being *documented* — in a record's `## Comments`,
a verifier's note, or even the user's stated call — does **not** make it *correct*. When the
evidence contradicts the stated reasoning, **say so and argue your case** rather than deferring.

* **Argue from what the data *is*** — feature composition, true source, size, the actual target —
  **not** from how someone might re-solve the broader problem today. (E.g. a task whose features are
  mostly URL/text tokens + a few geometry numbers is not an "image-recognition" dataset just because
  the objects pictured were ads; a vision model couldn't even see the dominant features.)
* **Steelman the existing decision first**, then give a concrete, falsifiable counter-argument
  (numbers, feature breakdown, what a model can/can't access). Vague disagreement isn't useful;
  evidence is.
* **Surface, don't override.** Don't silently flip a human's verdict. Record your counter-argument
  in the record's `## Comments` under a clear heading (e.g. `**Counter-argument (AI):** …`),
  leaving the human the final call. If you change a field, follow the `AI (UNVERIFIED)` convention.
* This cuts both ways: if pushing back means *keeping* an exclusion the user is inclined to overturn,
  argue that too. The goal is the right call, with the reasoning preserved — not agreement.

## AI-assisted triage (the `AI (UNVERIFIED)` convention)

The AI may draft a *provisional* triage for untriaged records, but it must be **honestly
labelled and human-verified** before it counts. When the AI reviews a record it:

1. sets a `suggestion` (a real verdict, not left blank) and any justified `decision_markers`;
2. fills empty metadata (`problem_type`, `required_split`, `domain`, `year`,
   `original_data_state`) **only** where confidently inferable — never overwriting existing values;
3. adds `AI (UNVERIFIED)` to `checked_by` and `AI-Filled (Verify)` to `tags`;
4. prepends the **⚠️ AI-FILLED — UNVERIFIED** disclaimer to `## Comments`, then its assessment,
   **preserving any existing human notes** below it (never delete prior `CC:`/curator reasoning).

Because `AI (UNVERIFIED)` in `checked_by` adds `ai_unverified` to `review_reasons()`, these rows
stay in the **Review** pill (status 🤖) until a human verifies and removes the AI reviewer (or
replaces it with their own name). This is exactly how a curator finds "what the AI did that I
still need to check". The convention is enforced by `test_ai_reviewed_records_follow_convention`.

## Notes

* The dashboard runs locally per curator (edit → `git` commit → PR). It is not hardened
  for multi-user or public exposure.
* `.venv/bin/python -m data_foundry.curation.cli build-site <out>` produces a read-only static copy (e.g. for
  GitHub Pages); `export` writes a flat CSV/Parquet/XLSX snapshot or pushes to a Sheet.
