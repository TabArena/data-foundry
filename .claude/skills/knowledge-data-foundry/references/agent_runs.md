# Batch runs with several agents

How a batch of records is worked by parallel agents on this machine, and the limits that shaped the runs of October
2026 (59 datasets added by about 20 parallel agents on 2026-10-06/07).

## A batch of records

When the curator names several records or a dashboard filter (for example "every record with `suggestion = Yes`,
`data_foundry_status` without `DF: Yes`, unclaimed, `checked_by` without `AI (UNVERIFIED)`"):

1. List the matching records first, then claim them in one call (`claims claim <names> --note "<run>"`,
   [claims.md](claims.md)) and work only on the ones it claimed: a skipped name is held by another curator.
2. Group them into units, one per source (records that share a download are one unit).
3. Per unit, one agent does the work with the data in hand (download, definition, `dataset check`, the probes), a
   second agent verifies the result against
   [verification.md](../../knowledge-curation/references/verification.md), and the first applies each finding or
   rejects it with evidence.
4. Nothing is built. The open questions go into each record's `## Review`, also for a dataset that was not added; the
   main session writes it from the unit agents' drafts ([records.md](records.md), "The review section"). The run's
   process log and evidence go into `local-data-warehouse/_runs/<date>_<run>/`, and stay there: the record, the
   definition and the CHANGELOG carry the numbers that matter, never the run folder's path.
5. The curator reviews the result on the page `/review-added-datasets` builds.

## Machine limits

* At most 20 concurrent subagents; an agent resumed with a message counts too, and a slot frees on the task
  notification, not on the hand-back message.
* Cap the threads of every Python run: `OMP_NUM_THREADS=2 OMP_THREAD_LIMIT=2 OMP_WAIT_POLICY=PASSIVE
  MKL_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2 POLARS_MAX_THREADS=2`. LightGBM spin-waiting under oversubscription ran about
  30 times slower.
* The root filesystem holding `/tmp` and the session scratchpad has 48 GB; large intermediates go under the run folder
  in `local-data-warehouse/_runs/` (on `/home`, with 1.7 TB free). `/home` is slow for many small files.
* Agents leave stray work (a `find /` ran 3.5 hours): check `ps` for long-running children before finishing.
* A loop that waits for a run checks the run's process id: `while kill -0 <pid> 2>/dev/null; do sleep 30; done`.
  Never `until ! pgrep -f <pattern>`: the loop's own command line holds the pattern, so pgrep finds the loop itself and
  it never ends (the large add run of 2026-11-09 left 55 such loops, some 7 hours old). Stop every wait loop you
  started before you hand back.
* Builds need memory more than cores: [rebuild.md](rebuild.md) lists the peaks.

## Files agents share

Lessons of the review rounds of 2026-11-10 and 11, where up to six agents applied decisions in parallel:

* Evidence and scratch output go under the run folder, `local-data-warehouse/_runs/<date>_<run>/`, never the
  session scratchpad: a restart wiped the scratchpad and the window tables in it.
* Each agent writes under its own name (`apply_<agent>.md`, `<dataset>_windows.csv`); a shared file name (`out.md`,
  `check.md`) is overwritten by the next agent.
* A file several agents would edit (`CHANGELOG.md`, the working copy's cross-dataset `REVIEW.md`, a knowledge file,
  the review page) is edited by the main session only: the agents return drafts. Two edits of one file at once lose
  one of them.
* An agent's summary is not the change: read the diff (a mark word copied wrong, a claim its own numbers
  contradict).
* Never `git stash`, `git checkout` or `git switch` while agents edit the working tree: the tree changes under them
  and an edit is lost (2026-11-11, a stash during two doc agents' run lost one edit, which the agent re-applied).
* A long run that is no longer needed is stopped (`SendMessage` to the agent, or `TaskStop`), not left to finish:
  maps_router_eta_1m's full window statistics ran 52 minutes for counts already known.

## Brief for a unit agent

Name in the brief: the records and the folder names, the knowledge files to read for each step (the workflow skill's
"Knowledge used" table), the thread caps, the run folder for scratch output, that nothing is built, committed or
pushed, and that records are edited only through the store API, a record's `## Review` also by an exact-string edit
of the current file ([records.md](records.md)).
