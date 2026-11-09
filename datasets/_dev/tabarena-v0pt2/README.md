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

Scoped build on 2026-11-08 (November 9 UTC): one requested definition, container format 2,
four traced input files totaling 5,003,658 bytes. Reload and minimal-input reproduction passed
with zero build errors or warnings. The dated changelog records its UUID and checksum; each dataset's generated
README identifies its own latest build. This scoped run does not update the other definitions' build records.

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
