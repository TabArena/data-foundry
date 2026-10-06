---
name: rebuild-working-copy
description: Rebuild the datasets of the TabArena v0.2 working copy (`datasets/_dev/tabarena-v0pt2/`) and verify the build. Runs `dataset build` in parallel, compares the result with the previous build and the committed READMEs, checks that the traced raw inputs alone reproduce every checksum, writes a local backup zip of those inputs, and updates the README table and the CHANGELOG. Use when the user asks to rebuild all or several datasets, after a framework change that changes the containers (metadata format, split protocol, standard preprocessing), or before the collection is released.
argument-hint: "[<unique_name>,...]"
user-invocable: true
---

# Rebuild the working copy

A build runs every definition end to end, saves a new container with a new UUID under the warehouse
(`<warehouse>/<unique_name>/<uuid>/`) and rewrites the folder's `README.md`. The containers stay local; git gets the
READMEs, the table and the log. The shipped BeyondArena containers are never touched.

**Input (optional):** comma-separated unique names to rebuild only those; by default every definition under the root.

$ARGUMENTS

For a single dataset, `.venv/bin/python -m data_foundry.curation.cli dataset build <folder>` is enough; still do
steps 5 and 8 for it.

The scripts are in [`scripts/`](scripts/); run them from the repository root with `.venv/bin/python`. Below, `$K` is
`.claude/skills/rebuild-working-copy/scripts`, `$OUT` a scratch folder for this run (outside the repository) and
`$PREV` the scratch folder of the previous run, if you still have it.

## Before you start

1. Settle the open decisions that change a dataset (a retirement, an edited definition) before the rebuild, not
   after it: a second full rebuild costs another hour of machine time and another round of checks.
2. Build in the repository's `.venv` (the `build` extra; pandas 2.3 or 3 give the same containers, scikit-learn
   must stay below 1.8). `pytest -q` passes, and
   `.venv/bin/python -m data_foundry.curation.cli dataset list --root datasets/_dev/tabarena-v0pt2` lists every
   definition (it exits non-zero when one does not import).
3. Commit the definitions first if the build record should carry a clean `git_sha`. A build from a dirty tree records
   `<sha>-dirty`, and rewriting the branch after the build leaves that sha out of the history.
4. Memory sets the parallelism: at 16 jobs the full set fits in about 730 GB. The largest dataset
   (maps_router_eta_1m) peaks at about 205 GB, the next ones at about 70, 50 and 35 GB;
   acquire_valued_shoppers_challenge (about 150 GB) and home_credit_default_stability_1m (about 126 GB) peak while
   their `_prepare_raw_files` inputs are traced (a full build traces them).

## Step 1: build

```bash
.venv/bin/python $K/build_all.py $OUT/build --jobs 16 [--previous $PREV/build] [--only a,b]
```

Run it in the background: about 10 to 17 minutes of wall time at 16 jobs in October 2026 (2,000 to 3,600 s of
summed build time; the wall time is set by maps_router_eta_1m alone).
Each dataset writes `$OUT/build/<name>.json`: status, findings, checksum, UUID, saved path, time, peak memory, and the
raw files it read (traced, `read`). The two definitions with `prepared_raw_files` also record the inputs of their
`_prepare_raw_files` step (`prepare_read`). `--previous` starts the longest builds first.

## Step 2: compare

```bash
.venv/bin/python $K/compare_builds.py $OUT/build [--previous $PREV/build] [--base-ref HEAD]
```

What a good build shows, and what to do otherwise:

* every dataset `ok`. A crash or an error is a finding: fix the definition or the framework, log the fix, and rebuild
  only the affected datasets (`--only`). Report each one with its cause, as in the rebuild of 2026-10-01 (an object
  column, NaNs with the sign bit, a text category that changed dtype);
* `reload verification failed: []`: every saved container reloads and its stored checksum equals the recomputed one;
* no new warning against the committed READMEs, or each new one explained. A warning the definition accepts on
  purpose goes into its `accepted_check_warnings` with the reason, which needs that dataset rebuilt;
* `rows or splits changed` and `raw files read changed` list only the datasets whose definitions changed.

## Step 3: reproduce from the traced inputs

```bash
.venv/bin/python $K/minimal_inputs.py $OUT/build links $OUT/minimal_warehouse
DATA_FOUNDRY_WAREHOUSE=$OUT/minimal_warehouse .venv/bin/python $K/build_all.py $OUT/minimal --check-only --jobs 16
.venv/bin/python $K/compare_builds.py $OUT/minimal --expect-checksums $OUT/build
```

`checksum differs from the full build: []` shows that the traced files are all a rebuild needs. A difference means
a build read a file the trace missed (a reader the tracer does not wrap) or is not deterministic; find out which
before the README claims the inputs suffice. Containers are deterministic across machines in rows and splits, but a
numpy `log` or `exp` can differ in its last bit between CPUs (california_house_prices_2020), so compare checksums on
one machine.

## Step 4: back up the inputs

```bash
.venv/bin/python $K/minimal_inputs.py $OUT/build zip <path>/tabarena-v0pt2-raw-inputs-<date>.zip
```

The zip holds the traced files under `local-data-warehouse/` with `MANIFEST.tsv` (size, SHA-256, the datasets that
read each file) and a `README.txt`. It is a local backup for the user: never add it to git, and say where it is.

## Step 5: update the docs of the working copy

* the dataset table: `.venv/bin/python $K/readme_table.py` (between the `<!-- datasets:start/end -->` markers);
* the "Rebuild" section of `datasets/_dev/tabarena-v0pt2/README.md`: the date, the number of datasets, the container
  format, and the count and size of the traced raw files;
* a dated `CHANGELOG.md` entry, newest first: what was rebuilt and why, crashes and their fixes, the open warnings
  (count and datasets), and the verification of steps 2 and 3;
* `TODO.md` (what the build settled or raised) and, when datasets were removed, the counts in `LEAK_AUDIT.md`,
  `AGENTS.md`, `datasets/README.md`, `GETTING_STARTED.md` and the add-dataset patterns.

## Step 6: the task-probe sweep (when rows or splits changed)

```bash
.venv/bin/python .claude/skills/verify-dataset/scripts/task_probes.py --all --built --jobs 8 --out $OUT/probes
```

The sweep's output stays in `$OUT/probes` (`summary.md` and one JSON per dataset); nothing of it goes into git. A
flag is a question, not a verdict. A dataset whose record already holds a dated task-probe decision for the same flag
needs no new one unless its numbers moved. Every other flag gets a decision as
`.claude/skills/verify-dataset/references/task_probes.md` describes (check it with `tuned_results.py` first). Record
each decision in the record (a dated comment with the evidence), in `CHANGELOG.md`, and as a row of that reference's
cases table; list the flags still open in `TODO.md`.

## Step 7: the superseded containers

The previous build's containers stay in the warehouse next to the new ones (each README's `build.path` names the
current one). List them for the user with their size; delete them only when the user says so.

## Step 8: commit

The READMEs, the table, the CHANGELOG and the other docs, on the branch the user names. Commits and pushes need the
user's ask (CLAUDE.md).

## Rules

* Report what happened with the numbers: crashes, errors, new warnings, a step that was skipped. "All verified" only
  after steps 2 and 3 ran on this build.
* Never rebuild a shipped BeyondArena dataset to check it; the collection pins its UUIDs.
* Never delete containers or raw files on your own.
* The raw inputs and containers never go into git.
