---
unique_name: dementia_prediction
name: Dementia Prediction Dataset
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
- WIP (DF)
claimed_by: Lennart
suggestion: Yes (Disagreement)
decision_markers:
- Wrong Domain / Source Modality
- Time-series (Classification)
- Selection Bias
tags:
- Tiny Data
- Non-IID (Grouped)
- 'Samples: Over Time'
- 'Time: Dated'
- 'Entities: Recur'
collections:
- New (BeyondArena)
original_source: Other
year: '2010'
domain: medical & healthcare
required_split:
- Grouped (NON-IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/shashwatwork/dementia-prediction-dataset/data
- https://data.mendeley.com/datasets/tsy6rbc5d4/1
notebook_path: datasets/beyond_iid/grouped/dementia_prediction/dementia_prediction.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/dementia_prediction/dataset.py
source_row: 4
type_adapter_id: curation-record-v1
---

## Comments

need to figure out how to use the data, source seems likely image data?

the version of this dataset is created from the study and taken from another one

Grouped data

AT: No objection, but we need to quickly talk about how we proceed with medical image data

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback log_loss — the OASIS-2 paper reports group analyses, no prediction metric.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): ordinal scales shipped as numbers, left as numbers for the curator's review: `SES`.

CC (2026-10-31, Lennart): marks on the review board of PR #37 (ordinal scales in the codebook's order, also when shipped as numbers; a state outside a scale missing when the column has no other missing value, else the lowest level; cycles ordered; codes shipped as numbers as categories): 1 ordinal scales shipped as numbers are ordered categories (point 3).

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `oasis3_dementia_status` (TBD -> Yes, priority 3). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-01, Lennart): the decode rule (a code whose codebook says in words what each level is carries the words; a score without them is a number): 1 scores are numbers (SES).

CC (2026-11-01, Lennart): the target rule (CLEAN-25) and the cut-end rule (CLEAN-14): the target is an ordered category, no_dementia < very_mild_AD < mild_AD.

**Assessment (AI, 2026-11-08):** one vote per unit (the scan of 2026-11-08 after boreal_postfire_lichen_biomass's issue 7): the 150 people have 1 to 5 visits (91 two, 13 four or five), and the use case is a first visit, while every follow-up visit is scored as if it were one. On the 60 shipped splits with 8 untuned models: weighting each visit by 1 over the person's visits ranks the models at Kendall tau 0.94 per split (lowest 0.71) and 1.0 for the ranking by the mean, the same best model on 56 of 60; scoring only each test person's first visit (OASIS-2's visit 1, 48 to 52 per fold against 112 to 138 visits) at 0.87 (lowest 0.57) and 0.93, the same best on 49 of 60. Open for Lennart as issue 1 of the record's Review; recommended: each person counts once (B), or the first visits only (C); log loss would first need an optional weight input. Script: `one_vote_scan/apply_2026-11-08/dementia_first_visit.py` in the exposure review's run folder.

CC (2026-11-08, Lennart): issue 1, B: each person counts once. The log loss weights a visit by 1 over the person's number of visits (`person_weight`, a scoring column for the metric only); follow-up visits stay scored as if each were a first visit, at one vote per person. The weight is for scoring only, never a `sample_weight`, also though it does not follow from the inputs (Lennart's rule of 2026-11-08, MET-15 amended, MET-17); the bundle warning accepted with that reason.

**Assessment (AI, 2026-11-08):** training with the weight changes a logistic regression's weighted log loss by -0.004 (SE 0.003, lower on 35 of 60 grouped random splits), within noise. New checksum v2:85704fee... (not built); `dataset check` 0 errors, 0 warnings.

CC (2026-11-08, Lennart): the declared metric (log_loss, weighted by person_weight) is checked.

## Review

**Outcome:** added. In the working copy since the migration; a scan of 2026-11-08 for units with unequal numbers of
rows (raised on boreal_postfire_lichen_biomass's issue 7) found that the log loss counts a person once per visit, 1 to
5 times, while the use case is a first visit. Resolved on 2026-11-08: each person counts once in the log loss
(issue 1).

**Main points:** Open: none. Resolved on 2026-11-08: each person counts once in the log loss, weighted by 1 over the
person's visits (issue 1).

**Issues for Lennart:**

1. **Count each person once in the log loss, score only the first visits, or each visit, as now?**

   * **Problem:**
     - A row is one visit, and the 150 people of OASIS-2 have 1 to 5 visits each (91 two, 43 three, 13 four or five), so a person seen five times counts five times in the log loss.
     - The use case is a first visit at a memory clinic, but follow-up visits of test people are scored as if each were a first visit, and each visit has its own rating (31 people change it).
     - Should each visit weigh 1 over its person's number of visits, so that each person counts once, or should only each test person's first visit count?
   * **Background:**
     - 370 visits of 150 people (the 3 visits rated moderate dementia are dropped, all of them follow-ups); a test fold
       holds about 50 people and 112 to 138 visits.
     - The inputs differ between visits (age, the cognitive test score, the MRI measures), and so can the rating; a
       model gives each visit its own prediction, and the weight changes only how much each visit counts.
     - The first visit is OASIS-2's visit 1, which the definition drops as a feature and would keep as a scoring
       column only; every person has one among the shipped rows. At first visits the ratings are 57% no dementia, 35%
       very mild and 9% mild, against 56%, 33% and 11% over all visits.
   * **Rules:** the use case decides what one prediction is and at which unit the score counts[^dp-unit]. Neither
     weight follows from the inputs, so B and C accept the check's warning with a reason the rules do not name yet (a
     weight that gives each unit one vote), as for pancreatic_cancer_mouse_detection[^dp-weight].
   * **Effect on the task:** per visit, people followed longer weigh more, and with them the follow-ups, rated mild a
     little more often (13% of the 220 follow-ups against 9% of the first visits); per person, each person counts once;
     first visits only, the score asks exactly what the use case asks, on less than half the test rows. Training keeps
     every visit under all three.
   * **Experiments:** 8 untuned predictors (two logistic regressions, random forest, extra trees, two LightGBM, kNN and
     the class shares) on the 60 shipped splits, re-run on 2026-11-08 for option C (the scan's first 30 splits give
     about the same taus for B: 0.94 per split, lowest 0.71, 1.0 for the mean). Kendall tau measures how far two orders of the models agree, 1 when they are the same.
     - Per person against per visit: tau 0.94 per split on average (lowest 0.71) and 1.0 for the ranking by the mean
       over the splits; the same best model on 56 of 60 splits.
     - First visit only against per visit: tau 0.87 per split (lowest 0.57) and 0.93 for the ranking by the mean
       (extra trees and the strong logistic regression swap, 0.750 and 0.751); the same best model on 49 of 60 splits,
       on 48 to 52 scored visits per fold.
     - The logistic regression leads under all three (log loss 0.62 per visit, 0.67 per person, 0.59 on first
       visits).
   * **Consistency:**
     - boreal_postfire_lichen_biomass counts each plot once since 2026-11-08[^dp-boreal]; there every input belongs
       to the plot, here none of the visit's measurements do.
     - The same scan raised superconductivity (per composition) and pancreatic_cancer_mouse_detection (per mouse).
     - sepsis_survival_minimal_clinical_records and wids_diabetes_mellitus score each admission of a returning patient
       per row (each admission a decision); here the use case is a first visit.
   * **Panel:** none; raised by the one-vote-per-unit scan of 2026-11-08 (boreal_postfire_lichen_biomass issue 7).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Per visit (implemented) | log loss over all visits | every rated visit scored; nothing changes | a person counts by the number of visits, 1 to 5; follow-ups scored as first visits |
     | B | Each person counts once | log loss weighted by 1 over the person's visits, a scoring column for the metric only; log loss first gets an optional weight input | one vote per person, the clinic's unit; ranks models as per visit (tau 1.0 for the mean) | a framework change; the check's warning accepted with a reason the rules do not name yet; follow-ups still scored as first visits |
     | C | First visit only | weight 1 on each test person's first visit and 0 on the follow-ups, from OASIS-2's visit number, for scoring only; same framework change as B | scores exactly the first-visit use case; one vote per person | 48 to 52 scored visits per fold instead of 112 to 138, a noisier score; the same framework change |

   * **Recommendation:** B: the clinic acts once per person, and B keeps every visit in the score; C if the score
     should match the first-visit framing exactly, at the cost of more than half the scored rows. **Decision:** A, B or
     C?

   **Notes for the AI:** on B or C: (1) `log_loss` takes no `weight` today; give it an optional row weight in
   `src/data_foundry/v2/metrics.py` (scikit-learn's `sample_weight`, `optional_inputs=("weight",)`,
   `weighted_definition` so the unweighted spec stays unchanged), with a test; one change serves
   asp_potassco_classification too if its issue 5 goes that way; (2) in `_clean`, before `Visit` is dropped, add
   `person_weight` (B: `1.0 / df.groupby("Subject ID")["Subject ID"].transform("size")`, after the moderate visits are
   dropped) or `first_visit_weight` (C: `(df["Visit"] == 1).astype(float)`), declared as a `ScoringColumn(...,
   role="weight", used_by="log_loss")`; (3) `Metric.fallback(reason=..., inputs={"weight": ...})`, the reason naming
   the weighting; no `sample_weight`; (4) accept `task_metric_weight_without_sample_weight` with the reason used for
   pancreatic_cancer_mouse_detection (a design weight of the score that gives each person one vote, SPLIT-23; not an
   amount at risk, MET-15; not a survey weight, MET-16); (5) on C, the `fit_reason` sentence "Follow-up visits of test
   people are scored as if each were a first visit" goes, and the task summary's `split` says only first visits are
   scored; on B, the grouping's definition adds that each person counts once; (6) `dataset check`, the CC line, a
   CHANGELOG entry, a Cases row in metrics.md. On A: a note that a person counts by the number of visits (tau 0.94 per
   split against one vote per person). The re-run: `one_vote_scan/apply_2026-11-08/dementia_first_visit.py` in the
   exposure review's run folder.

   [^dp-unit]: **SPLIT-23** (Must): the source's use case, cited, decides what one prediction is (a row, or a whole
     group). **MET-1** (Must): the declared metric scores the real task, at the unit the actor acts on.
   [^dp-weight]: **MET-15** (Must): a metric weight that is a function of the features needs no sample weight, and
     the bundle check `task_metric_weight_without_sample_weight` is then accepted with that reason; a realized amount
     at risk is also the training weight. A weight that gives each unit one vote and does not follow from the inputs
     is not named.
   [^dp-boreal]: boreal_postfire_lichen_biomass, issue 7, Lennart, 2026-11-08: "Option B: Each plot counts once."

   **Lennart (2026-11-08, change):** Option B: Each person counts once.

   **Resolved (2026-11-08, Lennart):** B, each person counts once. `log_loss` got an optional `weight` input, and the
   log loss is weighted by `person_weight`, 1 over the person's number of visits, a scoring column for the metric only
   with no training weight (Lennart's rule of 2026-11-08: a one-vote weight is for scoring only; training with it
   measured -0.004 log loss, within noise). Follow-up visits stay scored as if each were a first visit, at one vote
   per person; the notes, the metric's reason and the record say so.

## Reference

Rel source paper: Open Access Series of Imaging Studies: Longitudinal MRI Data in Nondemented and Demented Older Adults  https://direct.mit.edu/jocn/article/22/12/2677/4983/Open-Access-Series-of-Imaging-Studies-Longitudinal
