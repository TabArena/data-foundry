---
unique_name: dementia_prediction
name: Dementia Prediction Dataset
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
decision_markers:
- Wrong Domain / Source Modality
- Time-series (Classification)
- Selection Bias
- Class-dependent Recording
tags:
- Tiny Data
- Non-IID (Grouped)
- 'Samples: Over Time'
- 'Time: Lost'
- 'Time: Within Entity'
- 'Entities: Recur'
- Panel Data
collections:
- New (BeyondArena)
original_source: Other
year: '2010'
collection_period: Unknown
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

CC (2026-10-19, Andrej): Keep; no reason to exclude after review. Fixed licence and notes in `dataset.py`.

- **MMSE dominates** (a 30-point cognitive test; log loss 0.62 alone vs 0.94 prior), but all features do better (0.59). Not circular: the dementia rating ignores test scores (Marcus et al. 2010).
- **Licence:** `CC BY NC 3.0` was a Mendeley re-uploader's; now the OASIS terms (non-commercial, academic only).
- **Volunteer cohort, few borderline cases:** documented; the split by person stays.
- **Missing SES/MMSE only in demented visits** (21 rows): small effect, documented, kept.

Marcus DS, Fotenos AF, Csernansky JG, Morris JC, Buckner RL. Open Access Series of Imaging Studies: longitudinal MRI data in nondemented and demented older adults. J Cogn Neurosci. 2010;22(12):2677-2684. doi:10.1162/jocn.2009.21407

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback log_loss — the OASIS-2 paper reports group analyses, no prediction metric.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): ordinal scales shipped as numbers, left as numbers for the curator's review: `SES`.

CC (2026-10-31, Lennart): marks on the review board of PR #37 (ordinal scales in the codebook's order, also when shipped as numbers; a state outside a scale missing when the column has no other missing value, else the lowest level; cycles ordered; codes shipped as numbers as categories): 1 ordinal scales shipped as numbers are ordered categories (point 3).

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `oasis3_dementia_status` (TBD -> Yes, priority 3). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-01, Lennart): the decode rule (a code whose codebook says in words what each level is carries the words; a score without them is a number): 1 scores are numbers (SES).

CC (2026-11-01, Lennart): the target rule (CLEAN-25) and the cut-end rule (CLEAN-14): the target is an ordered category, no_dementia < very_mild_AD < mild_AD.

CC (2026-11-05, Andrej): ship after one change (Review issue 2, B): eTIV (estimated total intracranial volume) and ASF (atlas scaling factor, 1755 / eTIV) are written at one precision in every row, eTIV in whole cm³ and ASF to three decimals. In 112 of the 370 visits eTIV carried 9 to 11 decimals, a second numerical route that covered 9 of 150 first visits but 103 of 220 follow-ups, so the format told a model which visit it was; after the fix the decimal counts alone give ROC AUC 0.50-0.53 (0.54-0.56 before) and the models score as before. Marker `Class-dependent Recording`; suggestion `Yes` (Review issue 1). The declared split (by subject) and metric (log loss) checked and kept. `dataset check` clean; not rebuilt.

**Assessment (AI, 2026-11-08):** one vote per unit (the scan of 2026-11-08 after boreal_postfire_lichen_biomass's issue 7): the 150 people have 1 to 5 visits (91 two, 13 four or five), and the use case is a first visit, while every follow-up visit is scored as if it were one. On the 60 shipped splits with 8 untuned models: weighting each visit by 1 over the person's visits ranks the models at Kendall tau 0.94 per split (lowest 0.71) and 1.0 for the ranking by the mean, the same best model on 56 of 60; scoring only each test person's first visit (OASIS-2's visit 1, 48 to 52 per fold against 112 to 138 visits) at 0.87 (lowest 0.57) and 0.93, the same best on 49 of 60. Open for Lennart as issue 5 of the record's Review; recommended: each person counts once (B), or the first visits only (C); log loss would first need an optional weight input. Script: `one_vote_scan/apply_2026-11-08/dementia_first_visit.py` in the exposure review's run folder.

CC (2026-11-08, Lennart): issue 5, B: each person counts once. The log loss weights a visit by 1 over the person's number of visits (`person_weight`, a scoring column for the metric only); follow-up visits stay scored as if each were a first visit, at one vote per person. The weight is for scoring only, never a `sample_weight`, also though it does not follow from the inputs (Lennart's rule of 2026-11-08, MET-15 amended, MET-17); the bundle warning accepted with that reason.

**Assessment (AI, 2026-11-08):** training with the weight changes a logistic regression's weighted log loss by -0.004 (SE 0.003, lower on 35 of 60 grouped random splits), within noise. New checksum v2:85704fee... (not built); `dataset check` 0 errors, 0 warnings.

CC (2026-11-08, Lennart): the declared metric (log_loss, weighted by person_weight) is checked.

CC (2026-11-11, Andrej): Review issue 3, reply (a), split by person, `ForcedGroupedFromTemporal`: the split by person stays and is tagged `ForcedGroupedFromTemporal` (SPLIT-8), with a `Time basis:` line (no calendar date released; people seen later and scanner or protocol changes are not tested). Review issue 4, option B, `Time: Lost`: the collection fact `Time: Dated` becomes `Time: Lost`, as the only time kept is the order of each person's visits.

CC (2026-11-16, Andrej): collection fact `Time: Within Entity` added to `Time: Lost`: the release keeps no calendar date, but it keeps the order of each person's visits (the visit number and the days since the first visit), an order within the person.

CC (2026-11-17, Andrej): time basis `UnseenGroup` in place of `ForcedGroupedFromTemporal` (Review issue 7, B; replaces the tag of the CC of 2026-11-11): the use case is a person's first visit at a memory clinic, a person the data does not hold, so whole people are held out and each person's course stays on one side. The split is unchanged (stratified 3-fold CV over `Subject ID`, 20 repeats); the calendar stays lost and untested.

## Review

**Outcome:** added. The OASIS-2 study (Marcus et al. 2010): 370 visits of 150 older adults, each visit's clinical
dementia rating (no dementia, very mild or mild) predicted from a short cognitive test, three brain-size measures of
the visit's MRI and demographics, for people held out whole. Reviewed without a panel, from the gathered evidence:
the record, the earlier checks of 2026-10-19, the number-format sweep of 2026-10-27, model runs on the
shipped BeyondArena data (the same rows) and two checks of 2026-11-04. Kept after Andrej's review of 2026-10-19 (issue
1, resolved). The AI recommends shipping it after one change: 112 visits, mostly follow-ups, were written by a second
numerical route that leaves the brain-volume estimate unrounded, and writing the two MRI columns at one precision
removes that trace at no cost to the values (issue 2; LEAK-13). Validity: the rating is assigned without reference to
test scores (Marcus et al. 2010), so the cognitive test score (MMSE) is a predictor, not the criterion; the licence
is the OASIS terms. Value: logistic regression on all features beats MMSE alone; the 37 benchmark methods range from log
loss 0.619 to 0.724 (median 0.663). Quality: research volunteers with few borderline cases (`Selection Bias`); SES and
MMSE are missing only in demented visits, kept and documented. Weighed: a real rating task on a selected cohort, its
use case written by us. A scan of 2026-11-08 for units with unequal numbers of rows (raised on
boreal_postfire_lichen_biomass's issue 7) found that the log loss counted a person once per visit, 1 to 5 times, while
the use case is a first visit; each person now counts once (issue 5).

**Main points:** Open: none. Resolved on 2026-11-05: shipped, suggestion `Yes` (issue 1), eTIV and ASF written at one
precision (issue 2). Resolved on 2026-11-08: each person counts once in the log loss, weighted by 1 over the person's
visits (issue 5). Resolved on 2026-11-11: the split by person tagged `ForcedGroupedFromTemporal` (issue 3) and the
record's `Time: Dated` set to `Time: Lost` (issue 4). Issue 6 (`CrossSectional`) withdrawn on 2026-11-13. Resolved on
2026-11-17: time basis `UnseenGroup` in place of `ForcedGroupedFromTemporal`, split unchanged (issue 7).

**Record judgment:** valid, settled by CC 2026-10-19 (Andrej: keep, licence and notes fixed). The suggestion read
`Yes (Disagreement)`, although Lennart's `Yes` and Andrej's keep agree; it is `Yes` since 2026-11-05 (issue 1). The data-scouting run of 2026-10-31
screened `oasis3_dementia_status` (AI-filled, unverified): the larger OASIS-3 cohort, which needs extensive wrangling.

**Issues for Andrej and Lennart:**

1. **Ship in TabArena v0.2 as defined, and set the suggestion to `Yes`?**
   - Checked and settled (CC 2026-10-19, Andrej): MMSE dominates but is not circular, since the rating ignores test
     scores; the licence of the Mendeley re-upload was replaced by the OASIS Data Use Terms; the volunteer cohort and
     the missing SES and MMSE values are documented. The arguments that MMSE alone suffices and that logistic
     regression beating TabPFN speaks against the task were rejected and stay dropped.
   - Evidence (15 grouped splits, 5 x 3-fold by person, log loss): class shares 0.936, MMSE alone 0.623, logistic
     regression on all features 0.590, TabPFN 0.641; the missing-value pattern alone 0.898.
   - Kept on purpose: research volunteers, where only 14 of 150 people convert, so borderline visits are rarer than
     in a clinic; 220 of 370 visits are follow-ups scored without the earlier ones; the MRI enters as three summary
     volumes. The 21 visits without SES or MMSE are all demented and stay missing, as a clinic would see them; the
     `Class-dependent Recording` marker was considered for this on 2026-10-27 and not set.
   - Implemented: the definition as fixed on 2026-10-19; fit `approximate`.
   - (a) Ship, suggestion `Yes`. (b) Ship and keep `Yes (Disagreement)` until Lennart confirms. (c) Discuss.
   - Rule: the rule that a task stays until a concrete reason to retire is found in the task itself (TP-2, Should);
     the selection-bias pattern keeps the verdict and names the gap in `fit_reason` (selection.md, "Selection bias").
   - Precedent: eryhemato_squamous_disease, kept 2026-10-20 with `Selection Bias` on the same pattern.
   - Recommendation: (a). Decision needed: (a), (b) or (c).

   **Resolved (2026-10-19, Andrej):** kept, with the licence and the notes fixed (CC 2026-10-19). Lennart's `Yes` and
   this keep agree, so the suggestion `Yes (Disagreement)` is stale and becomes `Yes` with the next edit of the record.
   The recording trace found since is a fix within the keep (issue 2).

2. **Write eTIV and ASF at one precision, so that a second recording route leaves no trace?**

   * **Problem:**
     - In 112 of the 370 visits eTIV, the estimated total intracranial volume, is written with 9 to 11 decimals and
       equals exactly 1755 / ASF, while the other visits carry it to 1 or 2 decimals: a second numerical route.
     - That route covers 9 of 150 first visits but 103 of 220 follow-ups, and among follow-ups it marks fewer
       mild dementia (5% against 20%), so it tells a model what the definition dropped on purpose, which visit it is.
     - Round eTIV and ASF to one precision in every row, or keep the values as published?
   * **Background:** ASF, the atlas scaling factor, is by definition 1755 / eTIV, so the two columns carry one
     measurement; the definition drops the visit number and the time since the first visit and scores each visit on
     its own. Model runs on the shipped data found the route from the exact product eTIV x ASF = 1755.
     Class-specific recording conventions are harmonised at the precision of the measured values, after measuring
     what the fix removes[^2a].
   * **Effect on the task:** a model that reads the number format learns which visits are follow-ups, information a
     model of a single visit is not meant to have, and a little of the label with it; the effect is small.
   * **Experiments:**
     - Model runs (20 x 3 grouped splits, log loss): a multinomial logistic model of MMSE, age-adjusted brain
       volume and demographics 0.605; the same with the route flag 0.600; the 37 benchmark methods 0.619 to 0.724.
     - The number-format sweep of 2026-10-27 (BeyondArena splits, macro ROC AUC): the values 0.788, the values with
       their decimal counts 0.802.
     - Check of 2026-11-04 (the v0.2 definition, its 60 grouped splits; logistic regression and gradient boosting):
       the route flag alone ROC AUC 0.527, the decimal counts alone 0.54 to 0.56; adding the flag improves logistic
       regression's log loss by 0.003 (46 of 60 splits) and boosting's ROC AUC by 0.004, adding the decimal counts
       boosting's ROC AUC by 0.010 (49 of 60). With eTIV rounded to whole cm³ and ASF to three decimals in every row,
       the decimal counts alone fall to 0.50 to 0.53 and the models score as before (logistic regression log loss
       0.6145 both ways; class shares 0.950).
   * **Consistency:** follows gallstone_disease and regensburg_pediatric_appendicitis, where columns are written at
     the precision of the measured values (2026-10-21, 2026-10-27).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep as published (implemented) | eTIV and ASF as in the file | the published values | the format tells follow-ups apart and adds 0.004 to 0.010 ROC AUC for a model that reads it |
     | B | One precision | eTIV to whole cm³ and ASF to three decimals in every row; a `curation_comments` bullet; the marker `Class-dependent Recording` | no trace of the route; the values score the same | a new checksum, a rebuild |

   * **Recommendation:** B: the fix removes the trace and costs nothing measurable. **Decision:** keep (A) or one
     precision (B)?

   **Notes for the AI:** on B, add `MEASURED_PRECISION = {"eTIV": 0, "ASF": 3}` and `df = df.round(MEASURED_PRECISION)`
   in `_clean`, a `curation_comments` bullet with the counts above (112 visits, 9 of 150 first visits, 103 of 220
   follow-ups) and the check, the marker `Class-dependent Recording` and `Andrej` in `checked_by` (already there) on
   the record, the suggestion `Yes`; re-run `dataset check`, CHANGELOG entry.

   [^2a]: **LEAK-13** (Must; amended 2026-10-26): class-specific recording conventions are harmonised: write every row
     at the precision of the measured values, computed columns and filled cells included; first measure how much the
     fix removes.

   **Andrej (2026-11-05, change):** I go with B

   **Resolved (2026-11-05, Andrej):** one precision (B): `MEASURED_PRECISION = {"eTIV": 0, "ASF": 3}` applied in `_clean`,
   a curation note with the counts and the check, the record's marker `Class-dependent Recording` and suggestion `Yes`;
   `dataset check` 0 errors, 0 warnings; not rebuilt.

3. **Time basis: name the split by person a `StationaryRelation`?**

   * **Problem:**
     - Each row is one visit, and the dementia rating, the cognitive test and the MRI all come from that visit, so the target is the person's state at the visit; the release has no calendar date, and the visit number and the days since the first visit, which the definition drops, order the visits only within each person.
     - Whole people are held out, so a person's later visits never inform the earlier ones across the split, and nothing in the source suggests that the rating rule or the measures changed over the study.
     - Name the split a `StationaryRelation`, argued from the source, or a `ForcedGroupedFromTemporal`?
   * **Background:**
     - OASIS-2 scanned 150 volunteers on two to five visits at least a year apart, 365 to 2,639 days from the first to the last visit (median 846), with the rating, the MMSE and the MRI at each visit (Marcus et al. 2010).
     - The record carries `Samples: Over Time` and `Time: Dated` and no target fact, since the rating comes with the features; issue 4 asks whether `Time: Dated` should be `Time: Lost`, as the only time kept is an order within each person.
     - The prototypes, by the rule's questions: the rating changes as dementia progresses, so not `Timeless`; the use case rates new people, so not a `Snapshot`; the visits share no prediction moment, so not a `DelayedTarget`; the rating is a present state read from the same visit's tests, and time moves it only along each person's own course, which the split keeps on one side, so a `StationaryRelation`[^3a].
   * **Experiments:** check of 2026-11-06 on the raw file: along the subject number, which may follow enrolment, each fifth of the 150 people has 40% to 50% first visits rated very mild or mild, a mean age at the first visit of 74 to 78 and 2.4 to 2.7 visits per person, with no trend. The subject number is not shown to be time, so this is a weak check. The time probe finds no date column and no order of the rating along the file beyond consecutive visits of one person.
   * **Effect on the task:** none on the data or the scores; the tag and its line state why a split by person, not by date, stands for the use case.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Split by person, `StationaryRelation` (implemented) | the shipped split; once the time-basis tags are in, the tag and a `Time basis:` line | the rating is read from the same visit; each person's course stays on one side | argued from the source: the calendar dates are not released |
     | B | Split by person, `ForcedGroupedFromTemporal` | the same split, tagged as a forward task whose time is lost[^3b] | would fit a use case that predicts the rating at a later visit | the use case rates the present visit; nothing points to a change of the rating over calendar time |

   * **Recommendation:** A: the target is the visit's own state, and the split by person already keeps each person's course on one side. **Decision:** A or B?

   **Notes for the AI:** on A, once the time-basis tags are in: `data_tags = ("WrongDomain", "StationaryRelation")` and a curation
   bullet `- Time basis: StationaryRelation: each visit's clinical dementia rating is read from the same visit's MMSE and
   MRI (Marcus et al. 2010); the 150 people were scanned on 2 to 5 visits over 365 to 2,639 days, and the release keeps
   no calendar date, only the order of each person's visits, which the definition drops. Argued from the source, not
   measured; whole people are held out, so each person's course stays on one side.` No `splits_comment` change. On B,
   `data_tags = ("WrongDomain", "ForcedGroupedFromTemporal")` and a bullet saying that dated visits would allow a split
   by visit year. The subject-number check is a count on the raw file (2026-11-06), no model.

   [^3a]: **SPLIT-32** (Should): how the data was collected is information for the split; the record carries the
     collection facts, and a definition can name the use-case prototype it follows with a `Time basis:` line. A
     present state read through a relation that time does not move, beyond prevalence and practice, is a
     `StationaryRelation`, measured on a dated source and argued from the source when the time is lost.
   [^3b]: **SPLIT-8** (Must): a task temporal in nature or by its use case whose release cannot give the windows ships
     in the closest regime that keeps the rows, tagged as forced from temporal, grouped by the entity when the entities
     recur; the definition says what a timestamp would change.

   **Answer (AI, 2026-11-06):** `StationaryRelation` now needs a measurement: name the split by person forced from
   temporal (a, the issue's B), or leave it without a prototype (b)?

   * **Problem:**
     - On the item "One meaning for `StationaryRelation`, measured or argued?" you wrote "I want this to be always
       measured": the tag now needs a dated source on which the target and its relation to the features are shown flat,
       so option A, argued from the source, no longer exists[^3s].
     - OASIS-2 releases no calendar date, only each person's visit order and the days since the first visit, and no
       parent source dates the visits (none published), so the relation cannot be measured.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Split by person, `ForcedGroupedFromTemporal` | the issue's B: the tag and a `Time basis:` line saying the visits arose over the study's years with no date released; dated visits would test people seen later and changes of scanner or protocol | the regime the rules give a forward use case whose time is lost; the split stays | a forced tag on a target read at the visit |
     | b | Split by person, no prototype | a `Time basis:` line saying why none fits, no tag | claims nothing | `dataset check` keeps noting the missing basis |

   * **Recommendation:** a: new people arrive over the study's years, and nothing dated is left to show that the
     rating's relation stays put. **Decision:** a or b?

   [^3s]: **SPLIT-32** (Should; Andrej, 2026-11-06): a `StationaryRelation` is always measured on a dated source; where
     time is lost it cannot be, and a forward use case takes the forced tag. **SPLIT-8** (Must): the forced split ships
     after its leak test, and its line names the reason and what a dated release would change.

   **Andrej (2026-11-11, discuss):** Reply (a): Split by person, ForcedGroupedFromTemporal

   **Resolved (2026-11-11, Andrej):** a: the split by person stays; `data_tags = ("WrongDomain",
   "ForcedGroupedFromTemporal")` and a `Time basis:` bullet in `curation_comments` (no calendar date; people seen later
   and scanner or protocol changes are not tested); `dataset check` rerun.

   Replaced on 2026-11-17: the tag is `UnseenGroup`, the split unchanged (issue 7).

4. **Correct the record's collection facts?**

   * **Problem:**
     - The record carries `Time: Dated`, but the only time the release and its source keep is the visit number and the days since each person's first visit, an order within each person.
     - The rule counts an order found only within each entity as no time, and no calendar date or enrolment year is released.
     - Set `Time: Lost` in place of `Time: Dated`?
   * **Background:** `Samples: Over Time` fits (visits over up to seven years per person), and no target fact is needed, since the rating is made at the visit[^4a]. The arrival study of 2026-11-04 read the order of each person's visits as recoverable time, which the rule's wording does not count.
   * **Effect on the task:** none; the facts describe the source.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep `Time: Dated` (implemented) | the record unchanged | none found | reads as if a split by date were possible; departs from the rule's wording |
     | B | `Time: Lost` | the tag replaced | follows the rule; says that no calendar time survives | none found |

   * **Recommendation:** B. **Decision:** A or B?

   **Notes for the AI:** on B, in the record's `tags` replace `'Time: Dated'` by `'Time: Lost'`; `Andrej` is already in
   `checked_by`.

   [^4a]: **SPLIT-32** (Should): `Time: Dated` when the release or its source keeps the time or lets us recover it,
     else `Time: Lost`; a time order found only within each entity (a policy's terms) does not count. No target fact
     when the target exists with the features.

   **Resolved (2026-11-11, Andrej):** B: the record's `Time: Dated` is now `Time: Lost`, in the record.

5. **Count each person once in the log loss, score only the first visits, or each visit, as now?**

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
   split against one vote per person).

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

6. **`CrossSectional` instead of `ForcedGroupedFromTemporal`?**

   * **Problem:**
     - The definition is tagged `ForcedGroupedFromTemporal`, a forward use case whose time was lost[^fo-2].
     - The target is a present state measured with the features: the visit's clinical dementia rating, read from the same visit's scan and tests, and the use case reads it for new units at their own present[^cs-2].
     - The tag alone changes: the split stays grouped by subject.
   * **Background:** you tagged it `ForcedGroupedFromTemporal` on 2026-11-11, before `CrossSectional` existed. The use case estimates the rating at the visit from that visit's test and scan; whole people stay held out under either tag.
   * **Recurrence:** the use case meets the same person again: a memory clinic rates people at follow-up visits, and the data holds 2 to 5 visits per person (`Entities: Recur`). A cross-sectional task meets each unit once, so A: the forced grouped tag stays.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Stay `ForcedGroupedFromTemporal` (implemented) | the tag and its line stay | the decision stands | the tag claims a forecast the use case does not make |
     | B | `CrossSectional` | the tag and a `Time basis:` line naming the present state, the untested drift for later units and what a dated release would show | names the use case; no claim of a lost forward split | a new prototype on a decided tag |

   * **Recommendation:** A. **Decision:** A or B?

   **Notes for the AI:** on B, swap the tag, write the line, add a CC line; the split does not change.

   [^cs-2]: **SPLIT-32** (Should, 2026-11-13): a target measured together with the features, which the use case reads for new units at their own present, is `CrossSectional`, whether the dates survive or not; its line says whether the drift of the relation was measured or is untested. A label that only arrives later is no present state.
   [^fo-2]: **SPLIT-8** (Must): a forward use case without usable time ships in the closest regime, tagged forced from temporal, with a `Time basis:` line naming the reason.

   **Resolved (2026-11-13, Andrej):** withdrawn: `CrossSectional` was dropped the same day (it named no split the existing prototypes do not give: a present state used later is forced or a measured `StationaryRelation`, used within the covered time `Retrospective`). The tag stays.

7. **Time basis: tag the 3-fold CV over whole subjects `UnseenGroup` instead of `ForcedGroupedFromTemporal`?**

   * **Problem:**
     - The use case is a person's first visit at a memory clinic, a person the data does not hold, and for that the tree gives whole subjects held out with the tag `UnseenGroup`; the tree already lists dementia_prediction under that leaf.
     - `ForcedGroupedFromTemporal` is the forced step's tag for a use later in time with no periods to hold out; the definition took it on 2026-11-11 because the release keeps no calendar date.
     - Either tag gives the same folds: whole subjects held out on `Subject ID`.
   * **Background:** The use case is a first visit of a new person at a memory clinic, so the model only meets people the panel does not hold. Whole subjects (Subject ID, 150 people, 1-5 visits) are held out; the calendar is lost and stays untested. Confidence of the blind walk: high.
   * **Walk:** the questions as answered without the current split[^tree]:
     - Does the model fill in the period the panel covers, or predict after it? (use case): predict after it. Evidence: Use case: 'at a first visit a memory clinic estimates a person's clinical dementia rating from a short cognitive test and a brain MRI' - people coming to a clinic after the study.
     - Which units does the model predict for? (use case): only new units. Evidence: A first visit is a person the clinic has not seen; no known person's later visit is the use. 150 subjects with 1-5 visits each (Subject ID repeats; 91 have two visits). The visit number and MR delay are dropped, so no within-person history is read.
   * **What the blind dossier lacked, and what it changes:** Partition unchanged (grouped by Subject ID); the definition tags it ForcedGroupedFromTemporal (Andrej, 2026-11-11: calendar lost, people seen later untested) where my Panel walk ('only new units') gives UnseenGroup (new units). The tag differs, not the split. Round 1 reached UnseenGroup too.
   * **Source split:** no. No split prescribed.
   * **What changes:** `data_tags` swaps `ForcedGroupedFromTemporal` for `UnseenGroup`, the `Time basis:` bullet in `curation_comments` opens with `UnseenGroup` and keeps the untested later calendar; a CC line in the record; rebuild for the tags only.
   * **Blindness:** what the walker saw of the shipped split before deciding: saw: the tree's example lists name this dataset under a leaf; ignored as instructed.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Stratified 3-fold CV over whole subjects (`Subject ID`, 150 people with 1-5 visits, about 50 per test fold, 112-138 test and 232-258 train visits), 20 repeats, tagged `ForcedGroupedFromTemporal` (implemented) | No change. | The tag says the use is later in time and the calendar is lost; the `Time basis:` line names what stays untested (people seen later, scanner or protocol changes). | The split follows from the first-visit use case, not from a forced step, so the tag gives the wrong reason for holding people out. |
     | B | The same 3-fold CV over whole subjects, tagged `UnseenGroup` | `data_tags` `("WrongDomain", "ForcedGroupedFromTemporal")` becomes `("WrongDomain", "UnseenGroup")`; the `Time basis:` bullet opens with `UnseenGroup` and keeps what is untested; folds unchanged, the container rebuilt because tags ship in it. | Names why whole people are held out: the clinic meets people the data does not hold, as the grouping's first-visit framing says. | Reverses the tag set on 2026-11-11 and kept on 2026-11-13; the tag no longer shows that the calendar is lost (the line must say it). |

   * **Recommendation:** B, because the definition frames each visit as a first visit of a person not seen in training, a use that aims at new units.. **Decision:** A or B?

   **Notes for the AI:** blind walk of 2026-11-17 (split tree at cd3877cb). On B: set `data_tags` to `UnseenGroup` in `dataset.py`, change the opening of the `Time basis:` bullet and add a CC line; rebuild. No change to the split declaration.

   [^tree]: **SPLIT-36** (Should): walk the decision tree from the record's collection type, answering each question as if no split had been decided; a split the source prescribes is evidence, not an answer.

   **Andrej (2026-11-17, change):** Option B: The same 3-fold CV over whole subjects, tagged UnseenGroup.

   **Resolved (2026-11-17, Andrej):** B. `data_tags` names `UnseenGroup` in place of `ForcedGroupedFromTemporal` (`WrongDomain` stays), and the `Time basis:` line opens with `UnseenGroup (Andrej, 2026-11-17; ForcedGroupedFromTemporal before)`: the use case is a person's first visit at a memory clinic, a person the data does not hold, so whole people are held out and each person's course stays on one side; it keeps what stays untested (people seen later, scanner or protocol changes). The split itself (stratified 3-fold CV over whole subjects, 20 repeats) is unchanged.

## Reference

Rel source paper: Open Access Series of Imaging Studies: Longitudinal MRI Data in Nondemented and Demented Older Adults  https://direct.mit.edu/jocn/article/22/12/2677/4983/Open-Access-Series-of-Imaging-Studies-Longitudinal
