# video_transcoding_time_prediction

**Outcome:** added. In the working copy since the migration; a scan of 2026-11-08 for units with unequal numbers of
rows (raised on boreal_postfire_lichen_biomass's issue 7) found that 80 of the 1,099 videos hold 97.8% of the jobs
and so nearly all of the RMSLE. The AI recommends keeping the score per job and naming this in the notes (issue 1).

**Main points:** Open: issue 1, keep each job's vote with a note, or count each video once?

**Issues for Lennart:**

1. **Keep the RMSLE per job with a note on the 80 full-grid videos, or count each video once?**

   * **Problem:**
     - A row is one transcoding job, and 80 of the 1,099 videos were transcoded to the full grid of 841 output settings, so these 80 videos hold 97.8% of the jobs and nearly all of the score.
     - The scheduler acts per job, but the grid is the experimenters' design, not a cluster's mix of jobs, while one vote per video would give the 1,018 videos with a single job 93% of the weight.
     - Should the score stay per job, with a note that names this, or should each job weigh 1 over its video's number of jobs, so that each video counts once?
   * **Background:**
     - Jobs per video: 80 videos with 841 (67,280 jobs), one with 486, and 1,018 with one (1.5% of the jobs). A test
       fold holds 366 or 367 videos and 19,686 to 26,407 jobs on the 9 shipped splits.
     - 13 of the 18 inputs describe the video and the other 5 the output setting (codec, bitrate, frame rate,
       resolution); a model gives each job its own time, and a weight changes only how much each job counts.
     - Per job, the score is in effect the error on the output settings of the full-grid videos in a test fold (about
       a third of the 80); per video, it is mostly the error on one job of each single-job video.
   * **Rules:** the use case decides at which unit the score counts[^vt-unit]; the scheduler acts per job, so the
     rules point to the job, and the imbalance is the source's design; the call is a weighing.
   * **Effect on the task:** per job, a model that predicts how the output settings change the time of a few videos
     wins; per video, a model that predicts the time of one job of many different videos wins. A cluster's queue would
     hold neither mix.
   * **Experiments:** the scan of 2026-11-08, 8 untuned predictors (random forest, extra trees, two LightGBM, two
     ridge, kNN and the training mean) on the 9 shipped splits. Kendall tau measures how far two orders of the models
     agree, 1 when they are the same.
     - Per video against per job: tau 0.90 per split on average (lowest 0.79) and 0.93 for the ranking by the mean
       over the splits; the same best model on 3 of 9 splits.
     - The top pair swaps: random forest leads per job (RMSLE 0.182 against LightGBM's 0.185), LightGBM per video
       (0.238 against 0.246).
   * **Consistency:**
     - No dataset has decided a designed grid. In the same scan, airfoil_self_noise (bands of a spectrum, 8 to 19 per
       run) and concrete_compressive_strength (ages of a mix) stay per row, their units close to equal or each row
       its own question.
     - superconductivity, pancreatic_cancer_mouse_detection and dementia_prediction, raised by the same scan, have an
       actor who acts per unit; here the scheduler acts per job.
     - asp_potassco_classification (the same scan) has the same shape, and its issue 5 recommends the same note.
   * **Panel:** none; raised by the one-vote-per-unit scan of 2026-11-08 (boreal_postfire_lichen_biomass issue 7).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Per job (implemented) | RMSLE over all jobs, as now | the scheduler's unit; nothing changes | the notes do not say that 80 videos decide the score |
     | B | Per job, with a note | as A; the notes say that 80 full-grid videos hold 97.8% of the jobs, and what counting each video once would change | each job is a decision; the reader knows what the score weighs | 80 videos still decide the score |
     | C | Each video counts once | RMSLE weighted by 1 over the video's jobs, a scoring column for the metric only; RMSLE first gets an optional weight input | every video counts | the 1,018 single-job videos take 93% of the weight; the scheduler does not act per video; a framework change; the best model changes on 6 of 9 splits |

   * **Recommendation:** B: the scheduler acts per job, and one vote per video would trade the grid's weight for the
     single-job videos' weight, neither of them a cluster's mix; the note tells the reader what the score measures.
     **Decision:** A, B or C?

   **Notes for the AI:** on B: a dated bullet in `curation_comments`: "Each job is scored once. 80 of the 1,099 videos
   were transcoded to the full grid of 841 output settings and hold 97.8% of the jobs, so the score is in effect the
   error on new output settings of these videos; 1,018 videos have one job. Counting each video once would give those
   93% of the weight; it ranks 8 untuned models at Kendall tau 0.90 per split (0.93 for the ranking by the mean) and
   swaps the top pair, random forest and LightGBM (Lennart, 2026-11-08, review issue 1)." On C: `rmsle` gets an
   optional `weight` input in `src/data_foundry/v2/metrics.py` (with a test), a `video_weight` scoring column, 1 over
   the video's jobs, `inputs={"weight": "video_weight"}` on the metric, no `sample_weight`, the check's warning
   accepted as for pancreatic_cancer_mouse_detection. Then `dataset check`, the CC line and a CHANGELOG entry.

   [^vt-unit]: **SPLIT-23** (Must): the source's use case, cited, decides what one prediction is (a row, or a whole
     group). **MET-1** (Must): the declared metric scores the real task, at the unit the actor acts on.
