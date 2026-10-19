# The TabArena v0.2 working copy

`datasets/_dev/tabarena-v0pt2/` holds one v2 folder per dataset of TabArena v0.2 ([definitions.md](definitions.md)),
plus:

* `README.md`: how to rebuild, and the table of datasets with their UUIDs, generated between the
  `<!-- datasets:start/end -->` markers by `.claude/skills/rebuild-working-copy/scripts/readme_table.py`;
* `GETTING_STARTED.md`: the way in for a new curator;
* `CHANGELOG.md`: the dated log of every change, newest first;
* `BENCHMARK_CHANGES_TODO.md`: what the TabArena harness still needs (group columns, per-group scoring, metrics);
* a `REVIEW.md` in a dataset folder while that dataset has open issues for the curator.

## Rules

* Every change to the copy (an edited definition or helper file, an added or removed dataset, a re-run that makes a
  new container) gets a dated `CHANGELOG.md` entry. A new, removed or rebuilt dataset also refreshes the README table.
* A dataset retired to `No (Retired)` or `No` is removed from the copy (its definition stays in the git history), and
  its record's `v2_path` is cleared in the same change ([records.md](records.md)).
* New work is v2 only. The BeyondArena notebooks are Data Foundry v1; never add or re-curate a dataset with v1
  ([DATA_FOUNDRY_V1.md](../../../../DATA_FOUNDRY_V1.md)). Collections still ship both container formats.
* The docs of the copy list no dataset names or counts that change quickly; the generated table and the filtered
  curation log do (Lennart, 2026-10-12).
* A generated `README.md` is never edited by hand. Text it takes from the code (a script path, a check message) stays
  stale until the next `dataset check` or build of that folder.

## Open issues: `REVIEW.md`

While a dataset has questions for the curator, they live in `<folder>/REVIEW.md`, next to the definition they concern:
a short outcome, the open issues numbered, the alternatives with their numbers, the record fields that disagree with
the definition, and public evidence links. The format is the review skill's
[review_file_format.md](../../review-added-datasets/references/review_file_format.md). Cross-dataset items go into a
root `datasets/_dev/tabarena-v0pt2/REVIEW.md` while they are open. A record without a folder keeps its open issues in
an `**Open issues (AI, date):**` block of the record.

When the curator settles an issue, its decision goes into `dataset.py` (code and `curation_comments`) and the record
(a `CC` line), and the issue leaves `REVIEW.md`; the file is deleted when it is empty. `/review-added-datasets` builds
the review page from these files. The process log of a run (what was tried, probe outputs, scraped pages, evidence
scripts) stays in the local run folder `local-data-warehouse/_runs/<date>_<run>/`, never in git.

## Builds

`.venv/bin/python -m data_foundry.curation.cli dataset build <folder>` runs the definition end to end, saves a new
container with a new UUID under the warehouse (`<warehouse>/<unique_name>/<uuid>/`, or
`<version_of>/versions/<uuid>/` for a `_1m` version), verifies the export, and records the UUID, checksum and git
commit in the README front matter. There is no v0.2 collection in the registry yet: record the UUID in a dated
CHANGELOG entry, refresh the README table, and never add it to `BEYOND_ARENA_UUIDS`. A build happens only when the
curator asks; `dataset check` gives the same container without saving. `/rebuild-working-copy` rebuilds and verifies
many datasets at once.

* Build in the repository's `.venv` with the `build` extra. pandas 2.3 and 3 give the same containers; scikit-learn
  stays below 1.8.
* Commit the definitions first when the build record should carry a clean `git_sha`; a dirty tree records
  `<sha>-dirty`.
* Never rebuild a shipped BeyondArena dataset to check it: the collection pins its UUIDs
  (`src/data_foundry/collections/_registry.py`).

## The local warehouse

`local-data-warehouse/` (gitignored) holds the raw files of each dataset, the containers, and the run folders
(`_runs/<date>_<run>/`: run reports, review-page sources, agents' outputs and evidence). Its data never leaves the
machine and is never committed; personal data in raw files (ids, phone numbers, names) stays there (Lennart,
2026-10-12). A private review page built from a run folder may be published for the curator. `minimal_inputs.py` of the
rebuild skill collects the raw files the builds read into a local zip backup.

After a verified rebuild (every new container reloads with its checksum and the traced-input check passes), the
containers whose UUID is not a README's current `build.uuid` may be deleted, with a note in the rebuild's CHANGELOG
entry. Never delete a UUID pinned in `src/data_foundry/collections/_registry.py`, raw files, or the containers of
retired datasets without asking.
