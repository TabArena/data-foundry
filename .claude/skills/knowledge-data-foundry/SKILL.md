---
name: knowledge-data-foundry
description: "Reference knowledge, no workflow: how this repository (Data Foundry) implements dataset curation. The curation records and their conventions (CC and Assessment lines, AI (UNVERIFIED), WIP claims, pointers), the dashboard, the v2 dataset.py API and patterns, the bundle checks, how to run the probes, the TabArena v0.2 working copy (CHANGELOG, REVIEW.md, builds, the local warehouse), source access recipes, batch runs with agents, and the house rules every workflow follows. Load it when editing a record or a definition, running checks or probes, or when a workflow skill points to one of its files."
user-invocable: false
---

# Data Foundry knowledge

This skill holds knowledge, not steps: it never acts on its own. The workflow skills (`/triage-candidates`,
`/check-candidate`, `/add-dataset`, `/review-added-datasets`, `/rebuild-working-copy`) say which file to read at which
step. It holds what is specific to this repository; the curation knowledge that holds with any tooling is the sibling
skill [knowledge-curation](../knowledge-curation/SKILL.md), and each file here names the general rule it implements.

| Topic | File | Read it when |
|---|---|---|
| The curation records: editing through the store API, comment lines (`CC`, `Assessment`, `Counter-argument`, `Open issues`), AI triage, fields and vocabulary, claims, duplicates and retirements, the review queue, the definition pointers | [records.md](references/records.md) | before reading or writing any record |
| The dashboard: running and restarting it, its filters, pills, pins and links | [dashboard.md](references/dashboard.md) | starting it or explaining it to a curator |
| The v2 definition: the folder, `dataset.py`, the base class, `task_summary`, field mapping, `curation_comments`, the `_clean` recipe, `Grouping` / `Temporal` / `TemporalSplits`, `_1m` versions, traps, bundle-check slugs, `_decisions`, recording decisions, reference definitions, the harness | [definitions.md](references/definitions.md) | writing or reviewing a `dataset.py` |
| Running `dataset check` and the probes, and the checks only Data Foundry has (pointers, template, README) | [checks_and_probes.md](references/checks_and_probes.md) | verifying a definition |
| The TabArena v0.2 working copy: CHANGELOG and README rules, `REVIEW.md`, builds, the local warehouse, superseded containers | [working_copy.md](references/working_copy.md) | changing anything under `datasets/_dev/tabarena-v0pt2/` |
| Reaching sources: the Kaggle command line, PubChem, Zindi, SEC EDGAR, paywalls | [sources_access.md](references/sources_access.md) | a page does not load |
| Batch runs with several agents and the machine's limits | [agent_runs.md](references/agent_runs.md) | planning a run of more than a few datasets |

The probe entry points are in [scripts/](scripts/) (`leak_probes.py`, `task_probes.py`, `group_probes.py`,
`hidden_groups.py`, `generated_probes.py`, `tuned_results.py`, `check_collection_bundles.py`); they load a Data
Foundry dataset and call the general probe library of `knowledge-curation`.

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
  never an argument (knowledge-curation, [selection.md](../knowledge-curation/references/selection.md) and
  [provenance.md](../knowledge-curation/references/provenance.md)).
* Records are edited only through the store API, right after a reload; `CC` lines only for the curator's decisions
  ([records.md](references/records.md)).
* Every change to the working copy gets a CHANGELOG entry ([working_copy.md](references/working_copy.md)).
* A standing rule that comes out of a decision goes into the knowledge skills in the same change, not only into an
  agent's memory: general rules into `knowledge-curation`, rules about this repository here.
