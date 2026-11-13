---
unique_name: video_transcoding_time_prediction
name: video_transcoding
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 3
decision_markers:
- Outdated
tags:
- Non-IID (Grouped)
- 'Samples: No Time Dimension'
- 'Entities: Recur'
collections:
- TabArena Reject
- TabSTAR
original_source: UCI
year: '2015'
domain: technology & internet
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C58C9K
- https://www.openml.org/d/44974
notebook_path: datasets/beyond_iid/grouped/video_transcoding_time_prediction/video_transcoding_time_prediction.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/video_transcoding_time_prediction/dataset.py
source_row: 698
type_adapter_id: curation-record-v1
---

## Comments

CC: "Real data, preprocessed, information about decoding videos, the same video appears several times. If the task is to predict new videos, either group split is required, or we need to make sure that random split does not introduce unwanted behaviour of models learning distribution shifts between videos"

"transcoding time prediction model"

Valid metadata use case / problem!

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback rmse — the paper's R2 on the raw time is known only from a dissertation abstract and is not computable on the shipped log target; rmse on log time.

CC (2026-10-21, Lennart): proposal accepted: the fallback rmse on the log transcoding time, not r2 on the raw time.

**Assessment (AI, 2026-10-21):** metric now `Metric.from_context("rmsle", target_transform="log")` instead of the fallback rmse on the log target: transcoding times span orders of magnitude and a scheduler cares about the relative error (the source's R2 on the raw time is not verified, the paper was not read); the target still ships as log, and RMSLE is computed after the inverse, on the original scale (MET-3). Needs a rebuild to reach the container.

CC (2026-10-21, Lennart): ship the target on the modelling scale, score on the original scale (target_transform).

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `x264_ugc_encoding_time` (TBD -> Yes, priority 3). Each is screened in its own record; this record's verdict stays the curator's.

**Assessment (AI, 2026-11-04):** reviewed for the BeyondArena v0.2 review page, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the record's Review. Ship as defined: real transcoding measurements held out by video for load balancing; no defect found, spread unmeasured. Priority 3: gap 0, use case 1, source 1, shape 1, risk -1.

CC (2026-11-06, Andrej): time basis `Timeless` accepted on the BeyondArena v0.2 review page (issue 2, B, through the cross-dataset item on routine `Timeless` issues): designed transcoding jobs on one machine, none dated, all jobs of a video held out together. The `Time basis:` line is in the definition's notes, ending with what the split cannot test; the tag enters `data_tags` once PR #50 is in the working copy.

**Assessment (AI, 2026-11-08):** one vote per unit (the scan of 2026-11-08 after boreal_postfire_lichen_biomass's issue 7): 80 of the 1,099 videos were transcoded to the full grid of 841 output settings and hold 97.8% of the 68,784 jobs; 1,018 videos have one job and would take 93% of the weight if each video counted once. The scheduler acts per job. Counting each video once ranks 8 untuned models at Kendall tau 0.90 per split (lowest 0.79) and 0.93 for the ranking by the mean over the 9 shipped splits, the same best model on 3 of 9 (random forest and LightGBM swap at the top). Open for Lennart as issue 1 of the record's Review; recommended: per job, with a note that names the 80 full-grid videos (B).

CC (2026-11-08, Lennart): issue 4, B: scored per job, with a note. Each job is a decision of the scheduler (MET-17); the notes say that 80 full-grid videos hold 97.8% of the jobs, that one vote per video would give the 1,018 single-job videos 93% of the weight, and that it ranks 8 untuned models at Kendall tau 0.90 per split.

CC (2026-11-08, Lennart): the declared metric (rmsle) is checked.

CC (2026-11-11, Andrej): BeyondArena v0.2 review page, video_transcoding_time_prediction, issue 3 (leak and score), B, keep with notes:
- No leak: no column is measured during or after a job, and the video split raises LightGBM's RMSLE from 0.081 (row split) to 0.181.
- The task summary now says the time does not grow with the video's duration (likely a fixed-length piece) and that 81 large videos carry the score; the check's table is in the definition's notes. Rows, split and metric unchanged.

## Review

**Outcome:** added. UCI's online video transcoding data (Deneke et al. 2014): 68,784 ffmpeg transcoding jobs of 1,099
YouTube videos on one Intel i7 machine, predicting the job's time (log scale, scored by RMSLE on the time) from the
input video's properties and the output setting; whole videos are held out. The AI recommends shipping it as defined.
Reviewed without a panel, from the record, the definition and one cheap check; there is no model run and no
earlier experiment on it. Validity: real measurements, every feature known before a job starts, and the memory a job
used (measured together with the time) dropped. The check on the shipped rows confirms the definition's account: 80
videos carry 841 jobs each and one video 486, together 98.5% of the jobs, while 1,018 videos have one job; the input
columns are constant within each video, so `video_id` is a video. A test fold therefore stands for about 27 large videos
plus about 340 single jobs. Value: not measured (no benchmark runs on this definition). Quality: 81 rows (0.1%) repeat
another row's features with another time, most likely one output setting measured twice per large video (840 distinct
output settings, 841 jobs per large video). Weighed: a documented measurement study with a clear operational use (+),
one machine and one ffmpeg version (-), few large test videos per fold and no measured spread (-).

**Main points:** Shipped as defined (issue 1, 2026-11-11; verdict ship, metric and split ok); the video split is named
`Timeless` (issue 2, resolved 2026-11-06); no leak, kept with notes on what the time is and that 81 videos carry the
score (issue 3, resolved 2026-11-11). No open issue. Issue 4 (Lennart, 2026-11-08): Resolved on 2026-11-08: scored per job, each job a decision of the scheduler, with a note that 80 full-grid videos hold 97.8% of the jobs (issue 1).

**Record judgment:** valid. The task is the source's ("transcoding time prediction for proactive load balancing"),
the split by video is the record's and Lennart's early call, and the metric is his (RMSLE on the time, 2026-10-21).
The record's `Outdated` marker has no rule behind it: the times hold for one 2014 setup, which `fit_reason` already
says, and the physics of the task does not age with it. The data-scouting run of 2026-10-31 found better data for the
same task, `x264_ugc_encoding_time` (priority 3), screened in its own record and not added yet. A multi-target sweep of
2026-11-02 proposed the `Multi-target` tag (time and memory are both in the source); that is a tag question of that
sweep, not of this definition.

**Issues for Andrej:**

1. **Ship as defined?**

   * **Problem:**
     - Nothing open was found: real measurements of one transcoding setup, features known before a job starts, the
       memory measured with the time dropped, and whole videos held out.
     - No run measured how far methods spread on it, and a test fold rests on about 27 large videos plus about 340
       single jobs.
     - Ship as defined, or retire?
   * **Background:** 80 videos carry 841 jobs each and one video 486 (98.5% of the jobs); the input columns are
     constant within each video. The source's use is load balancing in a transcoding cluster (Deneke et al. 2014).
     `x264_ugc_encoding_time` (priority 3) is screened as better data and not added.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Ship as defined (implemented) | 68,784 jobs of 1,099 videos, grouped by video, RMSLE on the time | the source's task; a split that matches new videos; no defect found | one machine and one ffmpeg version; spread unmeasured |
     | B | Retire | `No (Retired)`, a CC line, the folder removed | leaves the place to a newer encoding-time set once added | no defect of the data found |

   * **Recommendation:** A: no reason in the task itself to retire it[^1a]. **Decision:** A or B?

   [^1a]: **TP-2** (Should): retire, fix or keep a task for a concrete reason found in the task itself; until one is
     found, the task stays.

   **Resolved (2026-11-11, Andrej):** A (mark `ok`, 2026-11-10): shipped as defined, nothing changed. The leak and score
   question stays open in issue 3.

2. **Time basis: name the video split `Timeless`, as runs of one designed experiment?**

   * **Problem:**
     - Each row is one ffmpeg job of a designed experiment on one Intel i7 machine: a YouTube video transcoded to one
       output setting (the full grid of 841 settings for 80 videos, mostly one job for the rest), with the video's
       properties and the setting known before the job; no job is dated and the run order is not in the release.
     - The record carries `Samples: No Time Dimension` and no time or target fact, which fits designed runs; the split
       holds out whole videos and names no time basis yet.
     - A job's time on that machine is the outcome of a designed run, the case the `Timeless` prototype names[^2a].
   * **Background:** the 81 rows that repeat another row's features with another time (one setting measured twice per
     large video) stay with their video on one side. Load on the machine may have varied during the experiment; with
     no run order that is noise, not a period that carries the target. Newer codecs and machines are outside the
     release (the record's `Outdated` marker).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Video split, no time basis (implemented) | as now | nothing to change | the definition does not say why a split that is not temporal is safe in time |
     | B | Video split, `Timeless` | as now; the tag and a `Time basis:` line naming the one-machine experiment | states the fact the split rests on; as the other designed-run sets | none found |

   * **Recommendation:** B: one experiment of designed jobs on one machine, nothing dated. **Decision:** A or B?

   **Notes for the AI:** on B, once PR #50 is in: `data_tags = ("Timeless",)` (the class adds `Non-IID`, `Grouped`),
   a curation bullet `- Time basis: Timeless: designed transcoding jobs on one machine (Deneke et al. 2014); the
   video's properties and the output setting are known before a job, no job is dated, and all jobs of a video are
   held out together.`, `splits_comment` unchanged; `dataset check`.

   [^2a]: **SPLIT-32** (Should): how the data was collected is information for the split; the record carries the
     source's collection facts, and a definition can name the use-case prototype it follows with a `Time basis:`
     line. `Timeless`: the target is a fixed property of the item, the same whenever it is measured (a material's
     strength, a molecule's activity, a species, the outcome of a designed run); the split is random or grouped by
     item family.

   **Resolved (2026-11-06, Andrej):** B, accepted through the cross-dataset item "Accept the routine `Timeless` time
   issues with one mark?" The `Time basis: Timeless:` bullet is in `curation_comments`, ending with what the split
   cannot test (another machine or newer codecs); the split and `data_tags` are unchanged. The tag `Timeless` enters
   `data_tags` once PR #50 is in the working copy.

3. **Is the transcoding task leaking, and is its score realistic?**

   * **Problem:**
     - Andrej's verdict note: "I'm unsure about this dataset and I assume it might be leaking. How exactly is the
       score and is this realistic? Open a new discussion item for that."
     - No leak found: every column is an input-video property or an output setting, and holding out whole videos
       raises LightGBM's RMSLE from 0.081 (row split) to 0.181, so the grouping does its job.
     - The score is realistic for one machine but rests on 81 large videos, and the time does not grow with the
       video's duration (33 s to 29 min), so the target looks like the time of a fixed-length piece, not of the whole
       video.
   * **How the score works:** the model predicts the log of `utime` per job; the scorer takes exp and computes RMSLE
     (log1p) on the time. Splits: 3 repeats x 3 folds by `video_id`; a test fold holds 23 to 31 large videos (20,000 to
     26,000 jobs) plus about 340 single-job videos. An RMSLE of 0.18 is roughly a 20% error on a job's time.
   * **Experiments** (3x3 shipped splits, sbatch on cpuhigh32):

     | Model | RMSLE | SD over folds | Large-video jobs | Single jobs |
     |---|---|---|---|---|
     | constant (train mean) | 0.961 | 0.015 | 0.962 | 0.952 |
     | formula: log(output pixels x fps x duration) | 0.798 | 0.037 | 0.797 | 0.826 |
     | formula + output codec | 0.553 | 0.053 | 0.552 | 0.617 |
     | median per output setting (840 cells) | 0.373 | 0.054 | 0.372 | 0.419 |
     | linear (logs + codecs) | 0.346 | 0.022 | 0.345 | 0.378 |
     | LightGBM, output setting + duration only | 0.412 | 0.040 | 0.411 | 0.456 |
     | LightGBM untuned, all features | 0.181 | 0.023 | 0.180 | 0.239 |
     | LightGBM, row-random split (contrast, not shipped) | 0.081 | 0.000 | | |
     | noise floor: 81 repeated jobs, SD on log1p | 0.113 | | | |

   * **Checks:**

     | Check | Result |
     |---|---|
     | Columns measured during or after the job | none left: UCI lists the frame counts, sizes, bitrate and frame rate as the input video's; `umem` is dropped |
     | 81 jobs measured twice | one random setting per large video run twice, both in the same video's fold; median gap 3% of the time |
     | Output grid near-deterministic? | no: 4 codecs x 7 bitrates x 5 frame rates x 6 sizes = 840 cells; the cell median scores 0.373, not near the 0.113 floor |
     | Per-video features through the grouping | input columns constant per video (all 13); the video split removes them, the row split shows the gain they would give (0.181 to 0.081) |
     | Same settings of other videos | the cell median explains 82% of the variance within large videos; the rest is the video (input bitrate r = 0.91, input pixels r = 0.82 with the video's offset) |
     | Time vs duration | the video's offset does not follow its duration (r = 0.04, slope 0.01 on log-log) |
     | Concentration | the 27 worst test videos carry 65% of LightGBM's squared error, single-job videos 2.5% |

   * **Use case:** a transcoding service scheduling jobs knows the input video's container metadata and the requested
     output before the job, as the features do. One i7-3720QM and one ffmpeg build fit a service that runs one
     hardware type; the service would need its own times, and a scheduler of whole videos would need time that grows
     with duration, which this target does not show (UCI calls it "total transcoding time").
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep as defined (implemented) | as now | no leak; features known before the job; video split matches new videos | the summary says "total time" while the time ignores duration; 81 videos decide the score |
     | B | Keep with notes | as A; `predicted` and `fit_reason` say the time does not grow with the duration (a fixed-length piece, apparently) and that 81 large videos carry the score | states what the score measures; no change to rows or split | edit waits for Lennart's claim (until 2026-11-15) |
     | C | Weight each video once in the score | as A, scored per video so single jobs count as much as large videos | the 1,018 single-job videos would count | the large videos' full grid is the task's content; the weights are ours, not the source's |
     | D | Retire | `No (Retired)`, a CC line, the folder removed | leaves room for `x264_ugc_encoding_time` once added | no defect found; the replacement is not added yet |

   * **Recommendation:** B: nothing leaks and the score is plausible (0.18 between the 0.11 floor and the 0.37 cell
     median), but the summary should say what the time is[^3a]. **Decision:** A, B, C or D?

   **Notes for the AI:** on B, after 2026-11-15 or with Lennart's consent: in `dataset.py`, `predicted="The
   transcoding time of a job, on a log scale; the unit is not stated, and the time does not grow with the video's
   duration (33 s to 29 min), so it is likely the time of a fixed-length piece."`; add to `fit_reason`: "81 large
   videos (about 27 per test fold) carry the score; single-job videos add 2.5% of the error."; a curation bullet with
   the table above; a `CC (<date>, Andrej):` line in the record with `Andrej` in `checked_by`; `dataset check`.

   [^3a]: **TP-2** (Should): retire, fix or keep a task for a concrete reason found in the task itself; until one is
     found, the task stays.

   **Resolved (2026-11-11, Andrej):** B (mark `ok`): kept with notes, text only. `predicted` says the time does not
   grow with the video's duration (likely a fixed-length piece); `fit_reason` says 81 large videos (about 27 per test
   fold) carry the score and single-job videos add 2.5% of the error; a curation bullet carries the check's table.
   Rows, split and metric unchanged, so no `dataset check`; the README picks the text up at the next check or build.
   CC line in the record.

4. **Keep the RMSLE per job with a note on the 80 full-grid videos, or count each video once?**

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

   **Lennart (2026-11-08, change):** Option B: Per job, with a note.

   **Resolved (2026-11-08, Lennart):** B, per job with a note. The score is unchanged; a dated bullet in the notes
   says that each job is a decision of the scheduler, that 80 full-grid videos hold 97.8% of the jobs, that one vote
   per video would give the 1,018 single-job videos 93% of the weight, and that it ranks 8 untuned models at Kendall
   tau 0.90 per split.

## Reference

@inproceedings{deneke2014video,
  title={Video transcoding time prediction for proactive load balancing},
  author={Deneke, Tewodors and Haile, Habtegebreil and Lafond, S{\'e}bastien and Lilius, Johan},
  booktitle={2014 IEEE International Conference on Multimedia and Expo (ICME)},
  pages={1--6},
  year={2014},
  organization={IEEE}
}
