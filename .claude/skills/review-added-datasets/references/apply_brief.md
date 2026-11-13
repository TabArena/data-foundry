# Brief for agents that apply a round's decisions

A round with decisions on many datasets (the window and horizon rounds of 2026-11-11 decided 29 temporal datasets) is
applied by a few agents in parallel, each with three to five datasets. The main session runs the consistency check
first (Step 4 of the skill), answers the notes that ask a question, and hands each agent this brief with its datasets,
the marks and the curator's notes. It keeps for itself the files several agents would write at once: `CHANGELOG.md`,
the working copy's cross-dataset `REVIEW.md`, the knowledge files and the review page. An agent edits only the
definitions and the records of its datasets: a dataset's review is its record's `## Review`, so there is no other
review file to touch.

## What the brief says

Name the repository, the branch and its `.venv/bin/python`; that nothing is committed, built or pushed; that only the
named datasets are touched; the thread caps (`OMP_NUM_THREADS=8` for a heavy run); and the run folder
`local-data-warehouse/_runs/<date>_<round>/` for evidence and scratch output, each agent under its own name
(`apply_<agent>.md`, never a shared file name), never named in a record, a definition or the CHANGELOG. Then, per
dataset:

1. **`dataset.py`:** the change the mark and its `**Notes for the AI:**` give, exactly (for windows: the `temporal`
   declaration with the cutoffs newest first; for a custom split only what the notes say). Rewrite every text the
   change makes stale: `task_summary`, `curation_comments`, `splits_comment`, the metric's reason; dates, counts,
   shares, and model figures measured before the change (dated or measured again). Remove the claims the review found
   false. House style: plain sentences, no rule IDs in `task_summary`.
2. **The check:** `ds.check(write_report=False)` with 0 errors (never write the README); confirm the counts the notes
   give (each window's test and train rows with `data_foundry.v2.splits.window_bounds` or `ds.make_splits`). A
   warning the curator signed off goes into `accepted_check_warnings` with the numbers and the CC date; no other.
3. **The record** (`curation/records/<unique_name>.md`), where the decision lands in full, in its two sections
   ([records.md](../../knowledge-data-foundry/references/records.md)):
   - `## Comments`, through the store API (`load_record` / `save_record`, appending to `record.comments`):
     - per decided issue: `CC (<date>, <curator>): <the decision in a faithful short form, quoting the note if any>.`
     - for the horizon (issue H): `CC (<date>, <curator>): the declared horizon (<length>, <gap>, windows starting
       <cutoffs or the newest N>) is checked, <why, from H's verdict>.` This opening is what the page reads.
     - for the metric, when the round marked it: `CC (<date>, <curator>): the declared metric (<name>) is checked,
       ...`
     - for the split, when the round marked it: `CC (<date>, <curator>): the declared split (<regime> on <columns>,
       <folds>) is checked, ...`
     - one `**Assessment (AI, <date>):**` line with the evidence (counts, shares).
   - `## Review`, with exact-string edits of the current record file (the Edit tool, after the save above), or through
     `record.review` in the same load and save; never by saving a record loaded before:
     - each decided numbered issue, at its end (after its footnotes and earlier turns), indented by three spaces:
       `**<Curator> (<date>, <mark>):** <the note verbatim, or "As implemented (A)." for an ok without one>` (unless
       it is already the last curator turn), a blank line, then `**Resolved (<date>, <curator>):** <the decision, what
       changed in dataset.py and the record, the check's result>`;
     - the horizon: the same two turns at the end of the `**Horizon:**` block, before `**Issues for <curator>:**`, at
       column 0;
     - `**Outcome:**` and `**Main points:**` say what was decided, in one sentence, and drop the settled questions;
     - never delete an issue.
4. **Collect:** `.venv/bin/python .claude/skills/review-added-datasets/scripts/collect_reviews.py --out
   <run folder>/apply_<agent>.md --names <the records> --horizon-marks <the same> --keep-settled`; fix each warning
   that names your records. `uvx ruff@0.15.15 check` and `format --check` on each `dataset.py` you changed.

The agent returns per dataset one line for `dataset.py` and one for the record (its comments and its review), the
check's result with the numbers, and a one- or two-sentence `CHANGELOG.md` draft, which the main session writes.

## What the main session checks after

* Read each changed `dataset.py` and record diff, not only the agent's summary: a mark word copied wrong ("change" for
  "discuss"), a claim the agent's own measurement contradicts, or a stale count in a text the brief did not name are
  what the rounds of 2026-11-11 found.
* Run `collect_reviews.py` over every record of the round, and `pytest -q` once all agents are done.
* Write the `CHANGELOG.md` entry from the drafts, rebuild the page and republish it (Step 5).
