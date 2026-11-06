---
unique_name: video_transcoding_time_prediction
name: video_transcoding
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
decision_markers:
- Outdated
tags:
- Non-IID (Grouped)
- Timeless
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

**Assessment (AI, 2026-11-08):** one vote per unit (the scan of 2026-11-08 after boreal_postfire_lichen_biomass's issue 7): 80 of the 1,099 videos were transcoded to the full grid of 841 output settings and hold 97.8% of the 68,784 jobs; 1,018 videos have one job and would take 93% of the weight if each video counted once. The scheduler acts per job. Counting each video once ranks 8 untuned models at Kendall tau 0.90 per split (lowest 0.79) and 0.93 for the ranking by the mean over the 9 shipped splits, the same best model on 3 of 9 (random forest and LightGBM swap at the top). Open for Lennart as issue 1 of the folder's REVIEW.md; recommended: per job, with a note that names the 80 full-grid videos (B).

CC (2026-11-08, Lennart): issue 1, B: scored per job, with a note. Each job is a decision of the scheduler (MET-17); the notes say that 80 full-grid videos hold 97.8% of the jobs, that one vote per video would give the 1,018 single-job videos 93% of the weight, and that it ranks 8 untuned models at Kendall tau 0.90 per split.

CC (2026-11-08, Lennart): the declared metric (rmsle) is checked.

## Reference

@inproceedings{deneke2014video,
  title={Video transcoding time prediction for proactive load balancing},
  author={Deneke, Tewodors and Haile, Habtegebreil and Lafond, S{\'e}bastien and Lilius, Johan},
  booktitle={2014 IEEE International Conference on Multimedia and Expo (ICME)},
  pages={1--6},
  year={2014},
  organization={IEEE}
}
