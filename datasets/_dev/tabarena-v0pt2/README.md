# TabArena-v0.2 Curation Overview

Working setup towards TabArena-v0.2: one v2 folder (`dataset.py` and a generated `README.md`) per dataset.

- **New here?** [`GETTING_STARTED.md`](GETTING_STARTED.md): set-up, the two workflows (settling a record, adding a
  dataset) and the large-data candidates to start with.
- **Every change is logged** in [`CHANGELOG.md`](CHANGELOG.md): edits, added or removed files, re-runs that change a
  container.
- Changes the benchmark harness (TabArena) needs for these datasets, for example scoring grouped tasks per group, are
  in [`BENCHMARK_CHANGES_TODO.md`](BENCHMARK_CHANGES_TODO.md).
- Each dataset folder has a `README.md` that `.venv/bin/python -m data_foundry.curation.cli dataset check` generates
  from its `dataset.py`: links to the curation record and the source, how to rebuild, and the evidence.
- Open questions for the curator are in a folder's `REVIEW.md` while they are open (the review page of
  `/review-added-datasets` is built from them); settled decisions are in the curation records
  (`curation/records/<name>.md`), the definitions and the `CHANGELOG.md` entries. How curation works here: the
  knowledge skills [`knowledge-curation`](../../../.claude/skills/knowledge-curation/SKILL.md) and
  [`knowledge-data-foundry`](../../../.claude/skills/knowledge-data-foundry/SKILL.md).

## Rebuild

- 2026-11-05 (internal-skill refresh): rebuilt GeoAI as one format-2 dataset with the same checksum.
  Reload and reproduction from the single 10,000,397-byte Train.csv pass; the new raw-input backup stays local.

- 2026-11-05: rebuilt GeoAI against updated main as one format-2 dataset. The single traced raw file is
  Train.csv (10,000,397 bytes); saved-container reload and reproduction from only that input both pass.
  The raw-input backup remains local. See the GeoAI README and dated changelog for the build identity.
The 2026-11-05 installed-skill alignment rebuild used the same qualified scientific source and reproduced the preceding checksum. One format-2 dataset, one traced raw CSV (5,829,604 bytes); reload, minimal-input reproduction and the local manifested backup are verified. The dated CHANGELOG records the new UUID.

Targeted rebuild on 2026-11-05: one format-2 dataset from one traced raw CSV (5,829,604 bytes). Saved-container reload and a check using only that input reproduce the checksum. The dated CHANGELOG entry records the UUID and accepted protocol. The manifested raw-input backup remains local, outside Git.
Latest scoped build, 2026-11-05: repeated through the updated installed workflow for one format-2 definition and one traced raw input (379,004,009 bytes). Saved reload and reproduction using only that input passed, with zero errors or warnings and an unchanged checksum. This was a single-dataset rebuild, not a rebuild of the full working copy.

- Latest requested scoped build (2026-11-06): one format-2 container, with 43 input dependencies (29,687,404,633
  bytes). Saved-container reload and minimal-input reproduction match the checked checksum; the current trace matches
  the existing input archive, whose payloads and current sources were freshly reverified. Details and remaining
  limitations are in CHANGELOG.
- The raw files come from `local-data-warehouse/` (or `$DATA_FOUNDRY_WAREHOUSE`); each folder's `README.md` gives the
  download command.
- To rebuild, ask Claude; it follows
  [`rebuild.md`](../../../.claude/skills/knowledge-data-foundry/references/rebuild.md).
- Build with the `build` extra installed (the repository's `.venv` has it). scikit-learn must stay below 1.8, which
  changes the grouped splits. Rows and splits are the same on every machine, but a numpy log or exp can differ in its
  last bit between CPUs, so compare checksums on one machine.
- `.claude/skills/knowledge-data-foundry/scripts/task_probes.py --all --built` sweeps the built containers against
  dummy baselines (answer its flags with
  [`task_probes.md`](../../../.claude/skills/knowledge-curation/references/task_probes.md)), and
  `.claude/skills/knowledge-data-foundry/scripts/group_probes.py <name>` probes a grouped task.
