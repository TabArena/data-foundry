# Batch runs with several agents

How a batch of records is worked by parallel agents on this machine, and the limits that shaped the runs of October
2026 (59 datasets added by about 20 parallel agents on 2026-10-06/07).

## A batch of records

When the curator names several records or a dashboard filter (for example "every record with `suggestion = Yes`,
`data_foundry_status` without `DF: Yes`, `claimed_by` empty, `checked_by` without `AI (UNVERIFIED)`"):

1. List the matching records first and skip any claimed by another curator.
2. Group them into units, one per source (records that share a download are one unit).
3. Per unit, one agent does the work with the data in hand (download, definition, `dataset check`, the probes), a
   second agent verifies the result against
   [verification.md](../../knowledge-curation/references/verification.md), and the first applies each finding or
   rejects it with evidence.
4. Nothing is built. The open questions go into each folder's `REVIEW.md` and into the records of datasets not added
   ([working_copy.md](working_copy.md)); the run's process log and evidence go into
   `local-data-warehouse/_runs/<date>_<run>/`.
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
* Builds need memory more than cores: [rebuild.md](rebuild.md) lists the peaks.

## Brief for a unit agent

Name in the brief: the records and the folder names, the knowledge files to read for each step (the workflow skill's
"Knowledge used" table), the thread caps, the run folder for scratch output, that nothing is built, committed or
pushed, and that records are edited only through the store API ([records.md](records.md)).
