# Getting started with dataset curation for TabArena v0.2

This guide gets a new curator from zero to a first contribution: what this folder is, how to set up Data Foundry,
where the curation notes live, the recommended workflow, and the two things you will do in it, **settling candidate
records** and **adding datasets**, with a list of candidates to pick from.

## 1. What this folder is

[TabArena](https://tabarena.ai/) benchmarks tabular ML on curated, real-world prediction tasks.
This folder is the working copy of its next version, **TabArena v0.2**: one folder per dataset, each a v2 definition
(`dataset.py`) built as a curated container. It started from the datasets of
[BeyondArena](https://huggingface.co/datasets/TabArena/BeyondArena), re-curated and audited, and new datasets join it
here; [`README.md`](README.md) lists the current ones. The datasets come from three split regimes: random (IID), **temporal** (predict the future)
and **grouped** (generalise to unseen entities such as patients or customers).

> [!TIP]
> **Large datasets are a priority.** Real tasks with roughly 1M–10M usable training rows are rare in public
> benchmarks, and most of them are non-IID. Candidates of that size carry the tag **`Review Prio 1 (Atlas)`** in
> the curation log (the tag comes from the earlier Atlas plan for a large-data collection, now folded into
> TabArena v0.2); pick from them first (section 7). A frame above 1.5M rows ships as a sub-sampled `<name>_1m`
> version, and each split trains on at most 1M rows.

The selection criteria (unique source, a real predictive task, no irreversible leakage, ethically unambiguous, not
trivial) are the same for every dataset; the [**📖 Guidelines**](https://tabarena.github.io/data-foundry/guidelines.html)
page of the curation log is the reference (it renders the two knowledge skills, `.claude/skills/knowledge-curation/`
and `.claude/skills/knowledge-data-foundry/`).

The recommended workflow (October 2026): Claude does the research and the writing, you make the decisions. The
commands are explained for people in [`.claude/skills/README.md`](../../../.claude/skills/README.md), which the
dashboard also shows as "Start here".

```
1. AI screens         /screen-candidates: a quick pass from the source, a verdict and a priority 1-5 per record,
                      labelled AI (UNVERIFIED); the obvious rejects are argued against before they are written
2. You check it       /review-screened-candidates: the dashboard's Screening queue, highest priority first;
                      accept (Yes), keep for later or reject
3. AI adds the Yes    /add-dataset on a dashboard filter: per source one agent writes the definition and runs the
                      checks and probes, then a review panel of agents attacks it; nothing is built; open issues,
                      ranked, in REVIEW.md
4. You review it      /review-added-datasets: a page with each dataset's use case, its open issues, the panel's
                      reports and files; you set a verdict per dataset and a mark per issue, Claude checks them for
                      consistency with earlier decisions and applies them
5. Build              on your ask ("rebuild X"): new containers (UUIDs), the CHANGELOG entry and the README table
```

Steps 2 and 4 are yours; Claude never commits, pushes or builds without your go-ahead. Sections 5 and 6 describe
each step, and how to do one dataset by hand.

## 2. Set up Data Foundry

Python 3.10+ and [`uv`](https://docs.astral.sh/uv/):

```bash
git clone https://github.com/TabArena/data-foundry.git
cd data-foundry
uv venv --seed && source .venv/bin/activate
uv pip install -e ".[dev]"   # dev = the build and tests extras plus the curation tools (autogluon, kaggle, …)
pytest -q                          # sanity check
```

Run the tools with the repository's environment, `.venv/bin/python -m data_foundry.curation.cli …`; a
`data-foundry-curation` on your PATH may be an older install.

The parts of the repository you will touch:

```
data-foundry/
├── curation/records/            # one markdown record per candidate dataset (the curation log)
├── datasets/_dev/tabarena-v0pt2/  # this folder: one v2 folder per dataset
├── datasets/_template/          # the template `dataset new` copies
├── .claude/skills/              # the Claude Code workflows (triage, check, add, verify, rebuild)
└── local-data-warehouse/        # gitignored: raw downloads and saved containers
```

More: [`datasets/README.md`](../../README.md) (the tree), [`CONTRIBUTING_DATASETS.md`](../../../CONTRIBUTING_DATASETS.md)
(the definition, step by step), [`AGENTS.md`](../../../AGENTS.md) (if you work with coding agents).

## 3. This folder

| File | What it holds |
|---|---|
| [`README.md`](README.md) | The table of datasets (regime, size, splits, UUID, open warnings) and how to rebuild them. |
| [`CHANGELOG.md`](CHANGELOG.md) | Every change to the folder, newest first. Add an entry with each PR. |
| [`BENCHMARK_CHANGES_TODO.md`](BENCHMARK_CHANGES_TODO.md) | What the TabArena harness has to change for these datasets. |

Each dataset folder holds `dataset.py` (the definition, the only file edited by hand), `explore.ipynb` (the
workbench: `ds = workbench()`) and `README.md` (generated: the dataset page with sample rows, checks, splits and the
build record).

## 4. The curation log

Every candidate has one markdown record under [`curation/records/`](../../../curation/records) (YAML front-matter
for the structured fields, free text in `## Comments`). The records are the memory of the curation effort: read a
record's comments before you work on its dataset.

The log is published read-only at [**tabarena.github.io/data-foundry**](https://tabarena.github.io/data-foundry/).
The large-data candidates:

> 🗂️ **[Large-data priority — filtered curation log](https://tabarena.github.io/data-foundry/#hf.tags=Review+Prio+1+%28Atlas%29)**
> — or, with the local dashboard running (section 5):
> [the same view locally](http://127.0.0.1:8765/#hf.tags=Review+Prio+1+%28Atlas%29)

Any filtered view can be shared like this: set the filters and click **🔗 Copy link** next to *✕ Clear filters*.

## 5. Workflow A: settling candidate records (steps 1 and 2)

Settling a record means deciding its verdict: read the sources and comments, decide whether it belongs
(`suggestion`), flag issues (`decision_markers`), fill in the metadata (problem type, required split, …) and write
the reasoning into `## Comments`.

**Recommended: Claude drafts, you decide.** In Claude Code, open the repository and run `/screen-candidates` (on new
links, names or the untriaged records): Claude researches each candidate from its source, writes what it found into
the record, rejects the obvious cases and gives the rest a priority. Each draft carries `AI (UNVERIFIED)` in
`checked_by` until you have checked it. Then run `/review-screened-candidates`: it opens the dashboard's
**Screening** queue (highest priority first); read the screening block, follow the sources it cites, change what you
disagree with, and verify the row (✓). For a deeper look at one record, run `/screen-candidates <unique_name>`.

Without Claude, start the dashboard yourself, a spreadsheet-like grid over the records whose edits rewrite the
markdown files in place:

```bash
.venv/bin/python -m data_foundry.curation.cli serve        # → http://127.0.0.1:8765
```

* Filter to the large-data candidates: the **tags** column filter → `Review Prio 1 (Atlas)`.
* Read the [**📖 Guidelines**](http://127.0.0.1:8765/guidelines.html) page before your first triage: the selection
  criteria and the recurring decision patterns.
* The status column shows what a row needs: 🤖 AI-drafted (a human verifies it with the ✓ action), ⚠ untriaged,
  ★ accepted but not yet in Data Foundry. Each row links its record (📄) and, once curated, its definition (🧩).

When you are done: `.venv/bin/python -m data_foundry.curation.cli validate`, then commit the changed records and
open a PR (Claude prepares both on request, and never commits or pushes without your go-ahead).

## 6. Workflow B: adding datasets (steps 3 to 5)

Once a record is accepted (`Yes`), the dataset needs a v2 definition: one `dataset.py` that turns the raw download
into a curated container (metadata → read → clean → dtypes → the regime → splits), with a `task_summary` that says
in plain words what is predicted, for whom, from what, and how well the split matches the real use (`fit`: direct or
approximate). The steps are in [`CONTRIBUTING_DATASETS.md`](../../../CONTRIBUTING_DATASETS.md); the folder goes to
`datasets/_dev/tabarena-v0pt2/<unique_name>/`.

**Recommended: Claude adds a batch, you review it.**

1. Claim the records first (section 7), then in Claude Code run `/add-dataset` on a dashboard filter, for example
   "every record with `suggestion = Yes`, `data_foundry_status` without `DF: Yes`, claimed by me, `checked_by` without
   `AI (UNVERIFIED)`" (only records you have checked).
   Per source one agent downloads the data, writes the definition, runs `dataset check` and the leak, task and group
   probes and the verification checklist; then a review panel of agents attacks the result (a claim auditor, column
   and split auditors, a domain practitioner, a blind reviewer that sees none of our notes, a precedent checker, an
   advocate and a critic, a mediator). Nothing is built. The open issues for you go, ranked and numbered, into each
   dataset folder's `REVIEW.md`, with the panel's reports below them.
2. Run `/review-added-datasets`. It builds the review page from the `REVIEW.md` files, a local HTML file or a Claude artifact you can
   share. Each dataset opens on its use case (the `task_summary`), then tabs for your decisions (the issues and the
   record fields that disagree with the definition), the review panel's reports, the run's details, `dataset.py`, the
   generated README and the curation record. Set a verdict per dataset (ship, ship after changes, don't ship, discuss) and a mark per issue
   (as implemented, change, discuss), with a note where you want something done or answered.
3. Tell Claude to apply your marks. It first checks each mark against the rules and similar earlier decisions and
   asks you to reflect where one looks inconsistent (never changing your mark). Then it changes the definitions, records your decisions in the curation records
   (dated `CC (<date>, <name>):` lines), retires what you rejected, writes the CHANGELOG entry, answers your
   questions on the page, removes the settled issues from `REVIEW.md` and republishes the page with only what is
   still open. Repeat until every dataset has a verdict.
4. The shipped datasets are built when you ask ("rebuild X and Y"; new UUIDs, the README table, the CHANGELOG),
   and the containers they replace are deleted once the new build is verified. Then commit and open the PR; it sets
   `DF: Yes` on the shipped records and releases their claims.

**One dataset by hand:** run `/add-dataset <unique_name>`. It reads the record, scaffolds the folder with the
metadata, BibTeX and regime pre-filled, and loops on `dataset check`; everything that needs a look at the data is
left as a `TODO(verify)` marker. From there you do the data science: download and load the raw data, clean it
(dtypes, missing values, identifiers, the target), read the check results in the generated README, decide and check
the split, and judge whether the result is a sound benchmark task. Then run `/add-dataset <unique_name>` again on the
folder for the verification and the review panel, and open the PR; a curator builds the container after review.

**Learn from the definitions in this folder.** The Data Foundry knowledge names a reference definition for each
regime (IID, grouped, temporal, late labels, a sub-sampled `_1m` version, heavy raw data) in
[`definitions.md`](../../../.claude/skills/knowledge-data-foundry/references/definitions.md), "Reference
definitions"; read the closest one in full before you write your own.

## 7. Where to start: the large-data candidates

The candidates change every week, so this guide does not list them. The
[filtered curation log](https://tabarena.github.io/data-foundry/#hf.tags=Review+Prio+1+%28Atlas%29) (or
[the same view locally](http://127.0.0.1:8765/#hf.tags=Review+Prio+1+%28Atlas%29) with the dashboard running) shows
them with their state: a `TBD -> …` suggestion needs settling (Workflow A), a `Yes` without `DF: Yes` needs a
definition (Workflow B). Each record's comments say what is open.

Pick one, or a batch, and claim it before you start, so nobody else works on it:

1. **Find what is free.** The *Claimed by* filter on *(empty)* shows the records nobody holds
   ([the same view locally](http://127.0.0.1:8765/#hf.claimed_by=+%E2%88%85)). Leave a record claimed by someone
   else alone, or ask them.
2. **Claim on `main`, ahead of the work.** Branch from `main`, set `WIP (Triage)` (verdict still open) or `WIP (DF)`
   (a final `Yes`, definition to write) and your name in `claimed_by` on the records you take, and nothing else.
   Open a small PR and merge it as soon as CI passes: the published log then shows your claim. Claude makes this
   claim branch on request.
3. **Work on your own branch.** Merge `main` into it after the claim PR (the claim lines are identical on both
   sides, so nothing conflicts) and do the work there, as long as it takes.
4. **Release.** The PR that brings the work to `main` sets the final state (`DF: Yes`, or the settled suggestion)
   and clears `claimed_by`. Giving a record up without the work is another small PR on `main`.

A WIP state without a name, or a name without a WIP state, puts the record in the Review queue. The record's
comments, the Guidelines tab and the definitions in this folder answer most questions; for the rest, ask the team
(Lennart).
