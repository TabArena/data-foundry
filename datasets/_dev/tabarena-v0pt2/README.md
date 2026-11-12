# TabArena-v0.2 Curation Overview

Working setup towards TabArena-v0.2: one v2 folder (`dataset.py` and a generated `README.md`) per dataset.

- **New here?** [`GETTING_STARTED.md`](GETTING_STARTED.md): set-up, the two workflows (settling a record, adding a
  dataset) and the large-data candidates to start with.
- **How a dataset is split** (folds, repeats, the 1M / 500k row budget and the `_1m` versions): the decision tree in
  [`split_protocol.md`](../../../.claude/skills/knowledge-data-foundry/references/split_protocol.md) of the knowledge-data-foundry skill.
- **Every change is logged** in [`CHANGELOG.md`](CHANGELOG.md): edits, added or removed files, re-runs that change a
  container.
- Changes the benchmark harness (TabArena) needs for these datasets, for example scoring grouped tasks per group, are
  in [`BENCHMARK_CHANGES_TODO.md`](BENCHMARK_CHANGES_TODO.md).
- Each dataset folder has a `README.md` that `.venv/bin/python -m data_foundry.curation.cli dataset check` generates
  from its `dataset.py`: links to the curation record and the source, how to rebuild, and the evidence.
- A dataset's review, the questions for the curator and how each was settled, is the `## Review` section of its
  curation record (`curation/records/<name>.md`), never a file in its folder; the review page of
  `/review-added-datasets` is built from these sections. [`REVIEW.md`](REVIEW.md) here holds only the items that span
  datasets. The decisions are in the records, the definitions and the `CHANGELOG.md` entries. How curation works
  here: the knowledge skills [`knowledge-curation`](../../../.claude/skills/knowledge-curation/SKILL.md) and
  [`knowledge-data-foundry`](../../../.claude/skills/knowledge-data-foundry/SKILL.md).

## Rebuild

- Selected build on November 12, 2026: one MixtureSolDB format-2 container, from one traced CSV (41,107,737 bytes). Saved reload and traced-input checksum reproduction pass; the complete scientific frame and all nine folds match accepted qualification. See its generated report and CHANGELOG. Other datasets were not rebuilt.

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
