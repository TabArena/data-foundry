# The TabArena v0.2 working copy

`datasets/_dev/tabarena-v0pt2/` holds one v2 folder per dataset of TabArena v0.2 ([definitions.md](definitions.md)),
plus:

* `README.md`: how to rebuild. It carried a generated table of every dataset and its UUID until the curator
  trimmed it on 2026-10-27 (PR #32); what a dataset is and whether it is built is in its own folder's `README.md`;
* `GETTING_STARTED.md`: the way in for a new curator;
* `CHANGELOG.md`: the dated log of every change, newest first;
* `BENCHMARK_CHANGES_TODO.md`: what the TabArena harness still needs (group columns, per-group scoring, metrics);
* `REVIEW.md`: the review items that span datasets (a rule, a framework change). A dataset's own review is in its
  record, never in its folder (below).

## Rules

* Every change to the copy (an edited definition or helper file, an added or removed dataset, a re-run that makes a
  new container) gets a dated `CHANGELOG.md` entry.
* A dataset retired to `No (Retired)` or `No` is removed from the copy (its definition stays in the git history), and
  its record's `v2_path` is cleared in the same change ([records.md](records.md)); the record keeps its review.
* New work is v2 only. The BeyondArena notebooks are Data Foundry v1; never add or re-curate a dataset with v1
  ([DATA_FOUNDRY_V1.md](../../../../DATA_FOUNDRY_V1.md)). Collections still ship both container formats.
* The docs of the copy list no dataset names or counts that change quickly; the generated table and the filtered
  curation log do (Lennart, 2026-10-12).
* A generated `README.md` is never edited by hand. Text it takes from the code (a script path, a check message) stays
  stale until the next `dataset check` or build of that folder.

## Reviews: the record's `## Review`

A dataset's review is the `## Review` section of its curation record, `curation/records/<unique_name>.md`, so the
record is the one source of the dataset's curation (Lennart, 2026-11-11). It holds the outcome, the open and settled
issues numbered with every turn, the alternatives, the record fields that disagree with the definition, public
evidence links and the review panel; what it holds and how to edit it is in [records.md](records.md), "The review
section", and the format is the review skill's
[review_file_format.md](../../review-added-datasets/references/review_file_format.md). No dataset folder holds a
`REVIEW.md`, and none is created: `/add-dataset` writes the review into the record (Step 8), a re-check adds to it,
and a record without a folder keeps its open issues there too, with an outcome that starts `not added`. A choice taken
per dataset, even one a scan found in several, goes into each dataset's own review as its own issue (Lennart,
2026-11-08).

The working copy's `datasets/_dev/tabarena-v0pt2/REVIEW.md` holds only what is decided once for many datasets (a
rule, a framework change, a family stance). It is the one review file outside the records.

When the curator settles an issue, its decision goes into `dataset.py` (code and `curation_comments`) and the record:
the curator's turn and a closing `**Resolved (<date>, <who>):**` turn in its review, a `CC` line in its comments. A
review is never deleted, so the record keeps every decision and how it was reached (Andrej, 2026-11-02).
`/review-added-datasets` builds the review page from the records' reviews (`collect_reviews.py`). The report and the
page it generates stay in the local run folder `local-data-warehouse/_runs/<date>_<run>/` and are never committed:
they are the only files between the record and the page. The process log of a run (what was tried, probe outputs,
scraped pages, evidence scripts) stays there too, never in git.

## Builds

`.venv/bin/python -m data_foundry.curation.cli dataset build <folder>` runs the definition end to end, saves a new
container with a new UUID under the warehouse (`<warehouse>/<unique_name>/<uuid>/`, a `_1m` version under its own
name too), verifies the export, and records the UUID, checksum and git
commit in the README front matter. There is no v0.2 collection in the registry yet: record the UUID in a dated
CHANGELOG entry and never add it to `BEYOND_ARENA_UUIDS`. A build happens only when the
curator asks; `dataset check` gives the same container without saving. How to rebuild and verify many
datasets at once: [rebuild.md](rebuild.md).

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
2026-10-12). A private review page built from a run folder may be published for the curator. No committed file names
a run folder or another local path ([SKILL.md](../SKILL.md), house rules). `minimal_inputs.py` (see
[rebuild.md](rebuild.md)) collects the raw files the builds read into a local zip backup.

After a verified rebuild (every new container reloads with its checksum and the traced-input check passes), the
containers whose UUID is not a README's current `build.uuid` may be deleted, with a note in the rebuild's CHANGELOG
entry. Never delete a UUID pinned in `src/data_foundry/collections/_registry.py`, raw files, or the containers of
retired datasets without asking.
