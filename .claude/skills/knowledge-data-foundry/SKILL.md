---
name: knowledge-data-foundry
description: "Reference knowledge, no workflow: how this repository (Data Foundry) implements dataset curation. The pipeline and its stages, the curation records and their conventions (CC and Assessment lines, AI (UNVERIFIED), WIP claims, pointers), the dashboard, the v2 dataset.py API and patterns, the bundle checks, how to run the probes, the TabArena v0.2 working copy (CHANGELOG, REVIEW.md, builds and how to rebuild, the local warehouse), source access recipes, batch runs with agents, and the house rules every workflow follows. Load it when editing a record or a definition, running checks or probes, or when a workflow skill points to one of its files."
user-invocable: false
---

# Data Foundry knowledge

This skill holds knowledge, not steps: it never acts on its own. The workflow skills (`/screen-candidates`,
`/review-screened-candidates`, `/add-dataset`, `/review-added-datasets`) say which file to read at which step. It holds
what is specific to this repository; the curation knowledge that holds with any tooling, ranked and with rule IDs, is
the sibling skill [knowledge-curation](../knowledge-curation/SKILL.md), and each file here names the general rule it
implements. The overview for people is the [skills README](../README.md).

| Topic | File | Read it when |
|---|---|---|
| The pipeline: the stages and commands, the record after each step, the queues, which file is the truth for what, the agents | [pipeline.md](references/pipeline.md) | finding where a record stands or what comes next |
| The curation records: editing through the store API, comment lines (`CC`, `Assessment`, `Counter-argument`, `Open issues`), AI triage, fields and vocabulary, claims, duplicates and retirements, the review queue, the definition pointers | [records.md](references/records.md) | before reading or writing any record |
| Claims: the live board of who works on which dataset (a git branch), the `claims` commands, the hook, the records' mirror | [claims.md](references/claims.md) | before working on records or folders, and when a claim warning shows |
| The dashboard: running and restarting it, its filters, pills, pins and links | [dashboard.md](references/dashboard.md) | starting it or explaining it to a curator |
| The v2 definition: the folder, `dataset.py`, the base class, `task_summary`, field mapping, `curation_comments`, the `_clean` recipe, `Grouping` / `Temporal` / `TemporalSplits`, `_1m` versions, traps, bundle-check slugs, `_decisions`, recording decisions, reference definitions, the harness | [definitions.md](references/definitions.md) | writing or reviewing a `dataset.py` |
| Running `dataset check` and the probes, and the checks only Data Foundry has (pointers, template, README) | [checks_and_probes.md](references/checks_and_probes.md) | verifying a definition |
| The TabArena v0.2 working copy: CHANGELOG and README rules, `REVIEW.md`, builds, the local warehouse, superseded containers | [working_copy.md](references/working_copy.md) | changing anything under `datasets/_dev/tabarena-v0pt2/` |
| Rebuilding the working copy and verifying the build (only when the curator asks) | [rebuild.md](references/rebuild.md) | the curator asks for a rebuild |
| Reaching sources: the Kaggle command line, PubChem, Zindi, SEC EDGAR, paywalls | [sources_access.md](references/sources_access.md) | a page does not load |
| Batch runs with several agents and the machine's limits | [agent_runs.md](references/agent_runs.md) | planning a run of more than a few datasets |
| Exploring a dataset in a notebook: an optional starting point (`ds = workbench()`), not part of a dataset folder | [explore_notebook_reference.ipynb](references/explore_notebook_reference.ipynb) | you want a notebook to look at a dataset; copy it next to `dataset.py`, do not commit the copy |

The scripts are in [scripts/](scripts/):

* the probe entry points `leak_probes.py`, `task_probes.py`, `group_probes.py`, `hidden_groups.py`,
  `generated_probes.py`, `dtype_probes.py` (they load a Data Foundry dataset through `dataset_io.py` and call the
  general probe library of `knowledge-curation`), `tuned_results.py` and `check_collection_bundles.py`;
* for the pipeline: `benchmark_coverage.py` (the accepted set per domain, problem type and regime, for screening
  priorities), `clean_room.py` (the blind reviewer's folder) and `decision_register.py` (the decisions grouped by rule,
  with the consistency flags);
* for a rebuild: `build_all.py`, `build_one.py`, `compare_builds.py`, `minimal_inputs.py`, `readme_table.py`.

## House rules

Every workflow follows these; each comes from a curator's decision.

* No commit or push without the curator's explicit ask. A commit ends with the attribution line the session gives.
* No `dataset build` without an explicit ask; `dataset check` verifies without saving.
* Never delete raw files, a UUID pinned in `src/data_foundry/collections/_registry.py`, or a retired dataset's
  containers without asking. Superseded working-copy containers may go after a verified rebuild
  ([working_copy.md](references/working_copy.md)). Removing a dataset folder is the curator's call.
* The data in `local-data-warehouse/` never leaves the machine and is never committed. A private review page built for
  the curator may be published.
* Never name company code repositories in records, notes, reports, commit messages or the knowledge files; cite only
  public sources. Before a commit, `git grep` the change for such names.
* Never send the curator's email address or other personal data to an outside service, for example in a request
  header; ask for an organisation contact instead.
* A licence is never a verdict reason; other benchmarks' scores are never evidence; a model's feature cap or runtime is
  never an argument (knowledge-curation, [evidence.md](../knowledge-curation/references/evidence.md), EV-4).
* The curator decides; the AI drafts, assesses and argues, and checks every decision it applies for consistency with
  the rules and precedents, asking the curator to reflect rather than overriding
  ([principles.md](../knowledge-curation/references/principles.md), "Consistent judgement").
* Records are edited only through the store API, right after a reload; `CC` lines only for the curator's decisions
  ([records.md](references/records.md)).
* Every change to the working copy gets a CHANGELOG entry ([working_copy.md](references/working_copy.md)).
* A standing rule that comes out of a decision goes into the knowledge skills in the same change, not only into an
  agent's memory: general rules into `knowledge-curation`, rules about this repository here.
