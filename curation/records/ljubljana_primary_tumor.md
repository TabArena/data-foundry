---
unique_name: ljubljana_primary_tumor
name: Ljubljana Primary Tumor
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
- WIP (DF)
claimed_by: Andrej
suggestion: 'Yes'
priority: 1
decision_markers:
- Selection Bias
tags:
- Tiny Data
- 'Samples: Over Time'
- 'Time: Lost'
collections:
- New (BeyondArena)
original_source: UCI
year: '1988'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C5WK5Q
notebook_path: datasets/beyond_iid/new_iid/ljubljana_primary_tumor/ljubljana_primary_tumor.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/ljubljana_primary_tumor/dataset.py
source_row: 770
type_adapter_id: curation-record-v1
---

## Comments

Need to resolve ordinal encoding, otherwise looks good!

Has a lot of classes, need to see there are enough labels per class or if I need to group some cases / remove some samples

CC (2026-10-12, Lennart): Kept in TabArena v0.2 after the task-probe review (flag `few_minority`, multiclass). Prostate has 10 rows (3-4 per test fold), colon and thyroid 14 each (4-5). Together they are 13% of the test rows and 22% of a random forest's log loss (1.43 against 2.20 for the class shares). The definition already drops the classes with fewer than 10 rows. Too Small is for a task whose scored units are a handful; one rare class of the source's own labels that does not decide the score is part of the task.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback log_loss — The 1986-1987 papers report accuracy only; we drop the classes with fewer than 10 rows (MET-2). Original rejected: accuracy. log_loss is the multiclass fallback.

**Assessment (AI, 2026-10-27):** The open questions for the curator are in the record's Review (review of the Tiny Data datasets, written from the earlier findings, no review panel); the AI recommends shipping it after changes. Priority 1: gap +, use case - (our use case; the patients are not unknown-primary cases), source - (a thin UCI names file), shape -, risk - (the task is not the one the use case names).
**Assessment (AI, 2026-10-27):** evidence for the Selection Bias marker of PR #16, checked on primary-tumor.data: all 20 head and neck patients have neck nodes and 21 of the 24 breast patients have armpit nodes (8% and 4% of the other patients). The rows are patients whose primary was found, with the spread typical of it, not the patients with metastases of unknown origin the use case is about. The definition's fit_reason does not name this yet.

CC (2026-10-27, Lennart): fit approximate (was direct): patients with metastases of unknown origin do not show the selection of these rows, so it is a known gap (USE-8, amended on the review of PR #16); the Selection Bias marker stays.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): 2 ordinal scales typed as ordered categories in the codebook's order (CLEAN-14, amended): `age`, `degree-of-diffe` (the README lists their levels).

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `seer_primary_site_from_metastases` (TBD -> Yes, priority 3). Each is screened in its own record; this record's verdict stays the curator's.

**Assessment (AI, 2026-11-04):** reviewed for the BeyondArena v0.2 review page, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the record's Review. Keep, and drop the 61 rows without a tissue type: the population gap is named (fit approximate, Selection Bias) and the methods separate, but the missing tissue type marks lung and carries about 5% of the skill. Priority 1: gap 1, use case 0, source 0, shape 0, risk -1.

CC (2026-11-09, Andrej): kept (review page issue 1, A). The random split is tagged forced from temporal (issue 3, reply a): no date survives, and a `StationaryRelation` must be measured. The repeated patients stay as distinct patients with the same coarse findings (issue 4, A).

CC (2026-11-11, Andrej): still kept after lung_cancer's retirement (review page issue 5, A). A retrospective series of patients whose primary was found is the known ground truth this task needs; every patient has the site identified. Unlike lung_cancer, whose label is read from the measured specimen, the primary site here comes from a separate work-up.

CC (2026-11-11, Andrej): the 61 blank tissue types stay (review page issue 2, A: drop only a leak that cannot be resolved otherwise). The blank is no leak: 44 of the 61 are poorly differentiated (34 lung), a "type not determined" result a work-up also gives; the 15 rows with neither type nor grade are 27% lung, the base rate. The curation notes say so.

## Review

**Outcome:** added. The site of the primary tumour (11 sites) for 302 cancer patients of the Institute of Oncology in
Ljubljana (UCI, 1988), from age group, sex, the tumour's tissue type and differentiation and 13 sites of spread; the
AI recommends keeping it, with the 61 blank tissue types kept as "type not determined" (issues 1 and 2). Reviewed without a panel,
from the gathered evidence: the record, the earlier experiments of 2026-10-15, model runs on the shipped
data and three new checks (2026-11-04); the first version of this file (2026-10-27) migrated the folder's open
questions from Andrej's review. Validity: the label is the primary site that was found; the patients are not a series
with metastases of unknown origin, so the fit is approximate and the record carries `Selection Bias`, as Lennart
confirmed on 2026-10-27 (issue 1). The tissue type is missing for 45% of the lung patients against 11% of the
others; it carries about 5% of the skill and reads as a "type not determined" result, no leak, so kept (issue 2); the gaps in
differentiation carry nothing measurable. Value: the methods separate clearly (benchmark log loss 1.294 to 1.493,
class shares 2.203), also after the drop. Quality: 10% of the rows are exact duplicates, some with different sites,
kept as naturally occurring. Weighed: a documented clinical series with clear separation +, a population that is not
the use case's, a class-dependent gap and a 1980s feature set -.

**Main points:** Kept (issue 1), still kept after lung_cancer's retirement (issue 5, 2026-11-11); the random split
tagged forced from temporal (issue 3), the repeated patients kept (issue 4) and the 61 blank tissue types kept as a
real "type not determined" result, no leak (issue 2). Nothing open.

**Record judgment:** the record's open points (ordinal encoding, small classes) are settled in the definition and in
Lennart's comment of 2026-10-12, and the cohort gap is in `fit_reason` and the curation notes since 2026-10-20 (fit
approximate, confirmed by Lennart on 2026-10-27). Its reference is "UCI": it can take the definition's citation
(Zwitter and Soklic, Primary Tumor, UCI Machine Learning Repository, https://doi.org/10.24432/C5WK5Q), a change that
needs no mark. Since 2026-10-31 the record notes better data for the same task, `seer_primary_site_from_metastases`
(screened `TBD -> Yes`, not added).

**Issues for Andrej:**

1. **Keep the dataset, although the patients are not the population the use case predicts for?**

   * **Problem:**
     - Andrej disputes Lennart's keep: the use case is an oncologist facing metastases whose origin is unknown, but
       these are cancer patients whose primary was found.
     - Their "metastasis" columns include lymph nodes next to the primary, which point at it: neck nodes in all 20
       head and neck patients, armpit nodes in 21 of 24 breast patients, peritoneum in 24 of 29 ovary patients.
     - Keep it with the gap named, as now, or retire it?
   * **Background:**
     - A cancer of unknown primary is found from its metastases and diagnosed from a biopsy of one of them; the
       primary is then searched for, and the model would say where to look first.
     - The gap is named: `fit_reason` and a curation note give the numbers (2026-10-20), and Lennart set the fit to
       approximate with the `Selection Bias` marker on 2026-10-27, because patients with metastases of unknown origin
       do not show the selection of these rows[^1a]. A selected sample usually keeps its `Yes`[^1b].
     - For retiring: 10% of the rows are exact duplicates, 20% of the test rows have an exact copy in training, 16
       groups of identical rows carry different sites, and the dataset is an overused classic (OpenML 171) with a
       1980s feature set.
     - Better data for the same task was found on 2026-10-31: `seer_primary_site_from_metastases`, the US cancer
       registry from 2010, unscreened by a curator. It has the same selection (primaries that were found), 6
       metastasis sites against 13, and a data agreement that may forbid redistribution; a valid task does not have
       to give way to a better version[^1c].
   * **Effect on the task:** a model learns where the nodes next to each primary sit. A patient whose primary is
     really unknown has no such sign, so the scores overstate how a model would do in the use case.
   * **Experiments:**
     - Earlier own run on the UCI file (20 repeats of 3 folds, seed 4267, 60 splits): a short hand rule (neck nodes
       to head and neck; a woman with armpit nodes to breast; a woman with peritoneum to ovary; a man with bone
       metastases and an adenocarcinoma to prostate; else lung) reaches 44% accuracy; the specialists in Michalski
       et al. (1986) reached 42%, TabPFN 3.5 54%.
     - The same run: log loss TabPFN 3.5 1.308, random forest 1.371, logistic regression 1.388, naive Bayes 1.521,
       class shares 2.203. TabPFN beats logistic regression on 59 of 60 splits, on 55 of 60 without the duplicates
       and on 58 of 60 with the tissue type imputed.
     - Model runs on the shipped data (its 60 splits, 40 benchmark methods): log loss from 1.294 (CauSiLo) to
       1.493 (extra trees, default), median 1.351, TabPFN 3.5 1.296, logistic regression tuned 1.400; a naive Bayes
       model with fitted weights per column reaches 1.289, first of 41.
   * **Consistency:**
     - early_stage_diabetes_risk_prediction was retired on 2026-10-27 for the same objection (Andrej: "the patients
       are not the population the task is for, and the file is half duplicates"); this case differs in fewer
       duplicates (10% against half) and a documented clinical series.
     - eryhemato_squamous_disease keeps the same marker with an approximate fit: its selection is named and no
       exclusion reason survived (2026-10-20).
   * **Sources:** Michalski R, Mozetic I, Hong J, Lavrac N. The multi-purpose incremental learning system AQ15 and
     its testing applications to three medical domains. Proceedings of the Fifth National Conference on Artificial
     Intelligence (AAAI-86), 1986:1041-1045; the UCI page, https://doi.org/10.24432/C5WK5Q.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep with the gap named (implemented) | 302 patients, 11 sites; fit approximate, `Selection Bias`, the cohort in `fit_reason` | the methods separate clearly; the gap is documented; follows the dermatology keep | the scores stand for patients with a known primary |
     | B | Retire with `Not Representative` | record `No (Retired)`; folder removed | no task whose scores overstate the use case; follows early_stage_diabetes_risk_prediction | a real multiclass medical task leaves; no rule makes a named population gap a reason to retire |

   * **Recommendation:** A: no rule that must hold is broken, the gap is named in the definition and the record, and
     the methods spread. **Decision:** keep (A) or retire (B)?

   **Notes for the AI:** on B, `suggestion: No (Retired)`, add `Not Representative` next to `Selection Bias`, remove
   the folder and clear `v2_path`; TP-3 keeps a dataset whose tuned methods spread unless an earlier rule fails, so
   the decision amends USE-8 or the selection-bias paragraph (a population gap that makes the features work retires)
   with this case and early_stage_diabetes_risk_prediction.

   [^1a]: **USE-8** (Must; amended 2026-10-27, Lennart): a selection bias is judged against the real-world setting
     of the use case; when that setting does not share it, the selection is a known gap and the fit is approximate.
     Either way `fit_reason` names the selection and the marker stays.
   [^1b]: selection.md, "Selection bias": mark it `Selection Bias`; the verdict is usually still `Yes` (Andrej,
     2026-10-20). **TP-3** (Must): if tuned methods spread, keep the dataset.
   [^1c]: **TP-6** (Must): keep two questions apart, is the task valid and is it the best version; a valid task
     stays.

   **Resolved (2026-11-09, Andrej):** A, kept.

2. **Drop the rows without a tissue type, which is missing mostly for lung patients?**

   * **Problem:**
     - The tissue type (histology: epidermoid, adeno or anaplastic) is missing for 38 of the 84 lung patients (45%)
       and for 23 of the 218 others (11%), so a blank points to lung.
     - In a work-up for an unknown primary a biopsy of a metastasis always gives the tissue type, so the blank is a
       recording gap of this collection, not a fact of the disease.
     - Keep the gap with its note, drop the 61 rows, or drop the column?
   * **Background:**
     - Class-specific recording is fixed after measuring what the fix removes[^2a], and setting such cells to missing
       is no fix when the gaps follow the classes[^2b]. A row that lacks the input the prediction acts on is no task
       row[^2c]. Andrej's line on gallstone_disease: fix what lets a model tell the classes apart for a reason other
       than the target, tested; hyperlipidemia, recorded for cases only, was dropped there.
     - The differentiation grade was recorded for 46 of the 61 rows without a tissue type, so the tissue was examined
       for most of them; the blank may be a type outside the three coded ones or one not written down. The UCI names
       file says only "unknown value".
     - Missing per site: lung 38 of 84, thyroid 4 of 14, head and neck 4 of 20, stomach 5 of 39, kidney 3 of 24,
       the six other sites 0 to 2 each.
   * **Effect on the task:** a model can learn "no tissue type, so lung"; a naive Bayes model treats
     a blank as its own level for this reason.
   * **Experiments:**
     - Earlier own run (60 splits): imputing the tissue type without the label raises TabPFN 3.5's log loss from
       1.308 to 1.351, about 5% of its gain over the class shares.
     - New checks (2026-11-04, the same 60 splits, logistic regression and random forest on the shipped rows):
       filling the tissue type with its most frequent value raises the log loss from 1.388 to 1.419 and from 1.371 to
       1.414; the two gap flags alone reach 2.116 against 2.203 for the class shares.
     - The sibling: differentiation is missing for 136 rows, 25% of lung patients against 53% of the others, and
       carries nothing measurable (filled 1.395 and 1.373, dropped 1.407 and 1.376).
     - After the drop (241 rows) every site keeps at least 10 patients (prostate and thyroid exactly 10), lung falls
       to 46 (19%), and the models still separate: logistic regression 1.501, random forest 1.436, class shares 2.292;
       the random forest ahead on 59 of 60 splits (44 of 60 before).
   * **Unknown:** what a blank tissue type means (no biopsy, a type outside the three codes, or not written down);
     the donors' records would settle it.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep the gap, with its note (implemented) | 302 rows; the tissue type missing for 61 | no rows lost; the gap is documented | about 5% of the skill rests on a recording gap that marks lung |
     | B | Drop the 61 rows without a tissue type | 241 rows, all 11 sites kept, lung 19% | every row has the input a work-up always has; the models still separate | a fifth of the rows, most of them lung; prostate and thyroid at the 10-patient floor; rows repeating another row's features rise from 16% to 20% |
     | C | Drop the tissue-type column | 302 rows, 16 features | no gap left | the input a clinician reads first leaves the task |

   * **Recommendation:** B, if issue 1 keeps the dataset: it removes the gap without guessing a value, and the task
     keeps its sites and its separation. **Decision:** keep the gap (A), drop the rows (B) or drop the column (C)?

   **Notes for the AI:** on B, in `_clean` drop the rows with a missing `histologic-type` before the filter of sites
   with fewer than 10 patients (all 11 stay); update the curation bullet (61 rows dropped, the counts above),
   `task_summary.row` (241 patients) and `fit_reason`; run `dataset check`; CHANGELOG entry; `CC (<date>, Andrej):`
   line in the record and `Andrej` in `checked_by`. Not built.

   [^2a]: **LEAK-13** (Must): class-specific recording conventions are harmonised, a column filled in for one class
     only is dropped; first measure how much the fix removes.
   [^2b]: **LEAK-40** (Should): setting filled cells to missing is no fix when the gaps follow the classes, as the
     missing values then mark a class.
   [^2c]: **USE-7** (Must): a row that lacks the input the prediction acts on is no task row; drop it rather than
     keep it as missing.

   **Andrej (2026-11-09, discuss):** Could such a recording issue be dealt with by defining train test splits without
   stratification?

   **Answer (AI, 2026-11-09):** no: the gap sits in the features, not in the folds.

   * Stratifying only sets each fold's share of each site. A missing tissue type points to lung (45% of lung patients
     against 11% of the others) in training and test alike, whatever the folds, so a model reads it either way.
   * Unstratified folds change the site shares per fold a little, and nothing about what the blank tells.
   * The fix stays in the data: drop the 61 rows (B), drop the column (C), or keep the gap with its note (A, as now).
   * **Recommendation:** B, unchanged. **Decision:** A, B or C?

   **Andrej (2026-11-11, discuss):** Measure how much this affects models and if it is a problem.

   **Answer (AI, 2026-11-11):** the blank is worth about 5% of TabPFN's skill, mostly on lung, and it looks like a
   real pathology result, not a recording gap. So it is no problem.

   | TabPFN 3.5, shipped 20x3 splits | Rows | Log loss | Lung rows | Other rows | Lung AUC |
   |---|---|---|---|---|---|
   | A, blank as it is | 302 | 1.314 | 0.687 | 1.555 | 0.927 |
   | Blank replaced by a random draw from the column | 302 | 1.357 | 0.748 | 1.592 | 0.908 |
   | C, column dropped | 302 | 1.417 | 0.867 | 1.629 | 0.875 |
   | A, scored on the 241 rows with a tissue type | 241 | 1.399 | 0.911 | 1.514 | 0.914 |
   | B, rows dropped | 241 | 1.418 | 0.979 | 1.521 | 0.912 |

   Class shares: 2.203 on 302 rows, 2.300 on 241.

   * On its own the blank finds 45% of lung patients (AUC 0.67, 62% of blanks are lung). Replacing it with a random
     draw costs 0.044 log loss (worse on 55 of 60 splits), 5% of the gain over the class shares. 8% of TabPFN's lung
     predictions turn into another site without it. Logistic regression and random forest give the same result (0.029 and
     0.039 log loss, worse on 58 and 56 of 60 splits).
   * The known tissue types carry three times as much, and C loses that too (1.417, against 1.357 with the draw). B
     costs the models nothing on the rows it keeps (1.418 against 1.399), but it removes the patients who are hardest
     to place without a type.
   * A blank looks real at prediction time: 34 of the 38 lung blanks have a grade, and all 34 are "poorly"
     differentiated. So the tissue was examined and the type fit none of the three codes, like a large-cell or
     unclassified carcinoma. A biopsy report of a "poorly differentiated carcinoma, type not determined" is common in an
     unknown-primary work-up. Unknown: whether some blanks were never written down.

   | | Option | Effect |
   |---|---|---|
   | A | Keep the blank as "type not determined", with its note | 302 rows; about 5% of the skill rests on the blank, which the use case would also see |
   | B | Drop the 61 rows | 241 rows; removes a real kind of case, mostly lung |
   | C | Drop the column | loses the type's real signal (log loss +0.10) |

   * **Recommendation:** A. The blank does not make the task easier for a reason the use case lacks. The curation note
     can say that a blank tissue type with a poor grade is most likely a type outside the three codes. **Decision:**
     A, B or C?

   **Andrej (2026-11-11, discuss):** If this is a leak that cannot be resolved otherwise, drop, otherwise keep.

   **Answer (AI, 2026-11-11):** no leak, so keep (A). The site signal sits in blanks with a grade, a real pathology
   result; the blanks that may be unrecorded mark no site.

   | Rows without a tissue type | Rows | Lung |
   |---|---|---|
   | grade "poorly" | 44 | 34 (77%) |
   | grade "well" | 2 | 0 |
   | no grade either | 15 | 4 (27%) |
   | all 302 patients | 302 | 84 (28%) |

   * A blank with a poor grade means the tissue was examined and the type fit none of the three codes ("type not
     determined"); an unknown-primary work-up gives that result too, so it is known at prediction time.
   * The 15 rows with neither type nor grade, the ones that may never have been written down, are lung at the base
     rate: nothing to resolve there.
   * No re-encoding needed: the models already read the blank as its own level.

   **Resolved (2026-11-11, Andrej):** A, kept: the 61 blank tissue types stay missing; the curation notes gain a bullet
   reading the blank as a type outside the three codes (the counts above, 5% of TabPFN's skill), and a CC line in the
   record. Text only, nothing rebuilt.

3. **Time basis: name the random split a `StationaryRelation`?**

   * **Problem:**
     - The patients were seen at the Institute of Oncology over an unstated period before 1986, and the primary site, the tissue type and the sites of spread come from the same diagnostic work-up, so the target is a present state; the UCI file is sorted by primary site and keeps no date.
     - The record's facts, `Samples: Over Time` and `Time: Lost`, fit, and with the time lost a stationary relation can only be argued: where a primary spreads does not change, while the share of each site and the work-up (which organs were imaged) change with practice.
     - Name the random split a `StationaryRelation`, argued from the source, or a `ForcedIIDFromTemporal`?
   * **Background:**
     - Michalski et al. (1986) used the data, and it was donated to UCI in November 1988; neither says over which years the patients were seen.
     - The prototypes, by the rule's questions: the primary site is fixed for a patient, but the patients and their work-up arrive over the years, so `Timeless` would hide the change of practice; the use case is a later patient, so not a `Snapshot`; no shared prediction moment, so not a `DelayedTarget`; a present state read from the same work-up, so a `StationaryRelation`[^3a].
     - The arrival study of 2026-11-04 found neither its "no time relation" nor the forced tag a fit and proposed "random, drift only"; the stationary relation covers that reading.
     - When the sites of spread were written relative to finding the primary (regional nodes recorded while staging a known primary) is a question of the prediction point that issue 1 weighs, not of the split.
   * **Experiments:** the time probe of 2026-11-06 finds no date column and a raw order that follows the class (the file is sorted by site), so no time can be recovered.
   * **Effect on the task:** none on the data or the scores; the tag and its line state why a random split stands for the use case.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random split, `StationaryRelation` (implemented) | the shipped split; once PR #50 is in, the tag and a `Time basis:` line | the site and the features come from one work-up; names the drift in practice as the untested part | argued from the source; the years of diagnosis are unknown |
     | B | Random split, `ForcedIIDFromTemporal` | the same split, tagged as forced from temporal[^3b] | says that patients of a later decade are not tested | nothing found that moves the relation; the file has no time for the leak test the forced tag asks for |

   * **Recommendation:** A, if issue 1 keeps the dataset: the target and every feature come from one work-up, and only practice and case mix can drift. **Decision:** A or B?

   **Notes for the AI:** on A, once PR #50 is in: `data_tags = ("StationaryRelation",)` and a curation bullet `- Time
   basis: StationaryRelation: cancer patients of the Institute of Oncology, Ljubljana, seen before 1986 over an unstated
   period; the primary site, the tissue type and the sites of spread come from the same diagnostic work-up. The UCI file
   is sorted by site and keeps no date, so this is argued from the source, not measured; the share of each site and the
   work-up may have drifted over the years.` No `splits_comment` change. On B, `data_tags = ("ForcedIIDFromTemporal",)`
   and a bullet saying that years of diagnosis would allow a split by period.

   [^3a]: **SPLIT-32** (Should): how the data was collected is information for the split; the record carries the
     collection facts, and a definition can name the use-case prototype it follows with a `Time basis:` line. A
     present state read through a relation that time does not move, beyond prevalence and practice, is a
     `StationaryRelation`, measured on a dated source and argued from the source when the time is lost; `Timeless` is a
     fixed property of the item, the same whenever it is measured.
   [^3b]: **SPLIT-8** (Must): a task temporal in nature or by its use case whose release cannot give the windows ships
     in the closest regime, tagged as forced from temporal, after a leak test across the split; the definition says
     what a timestamp would change.

   **Answer (AI, 2026-11-06):** `StationaryRelation` now needs a measurement: if kept, name the random split forced from
   temporal (a, the issue's B), or leave it without a prototype (b)?

   * **Problem:**
     - On the item "One meaning for `StationaryRelation`, measured or argued?" you wrote "I want this to be always
       measured": the tag now needs a dated source on which the target and its relation to the features are shown flat,
       so option A, argued from the source, no longer exists[^3s].
     - The patients were seen over an unstated period before 1986, the UCI file is sorted by site and keeps no date, and
       no parent source dates them (none published), so the relation cannot be measured.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Random split, `ForcedIIDFromTemporal` | the issue's B: the tag and a `Time basis:` line saying the patients span an unstated period and the time is lost; years of diagnosis would test later patients under a changed work-up and case mix | the regime the rules give a forward use case whose time is lost | the leak test can check repeats and hidden groups, not periods |
     | b | Random split, no prototype | a `Time basis:` line saying why none fits, no tag | claims nothing | `dataset check` keeps noting the missing basis |

   * **Recommendation:** a, if issue 1 keeps the dataset. **Decision:** a or b?

   [^3s]: **SPLIT-32** (Should; Andrej, 2026-11-06): a `StationaryRelation` is always measured on a dated source; where
     time is lost it cannot be, and a forward use case takes the forced tag. **SPLIT-8** (Must): the forced split ships
     after its leak test, and its line names the reason and what a dated release would change.

   **Resolved (2026-11-09, Andrej):** a: the random split is tagged `ForcedIIDFromTemporal` in `data_tags`, with its
   `Time basis:` line: no date survives, and a `StationaryRelation` must be measured.

4. **Keep the repeated patients, as distinct patients with the same findings?**

   * **Problem:**
     - 49 of the 302 patients (16%) repeat another patient's 17 findings exactly, 30 of them with the same site (the 10% of duplicates the notes keep), so under a random split 20% of test patients have an exact copy in training.
     - The new rules for repeats of a unit the data does not record set the verdict by three tests (is the link above chance, does the label travel with it, is there an order), and all three read these as distinct patients with the same coarse findings: the natural verdict, which keeps the random split[^4a].
     - Keep the copies as now, or drop the 30 same-site copies?
   * **Experiments** (2026-11-06, the 302 shipped rows):
     - **Link at chance:** the findings are age in three groups, sex and yes/no answers, mostly "no", that hang
       together by site; a null that keeps each site's strongest links between findings (a tree of pairwise
       dependences, 200 draws) gives 57 repeated rows (95% 45-70) against 49 observed. Shuffling each column within
       its site, which breaks those links, gives 27.
     - **The label does not travel:** 16 of the 25 groups of identical patients hold more than one site (48 of their
       74 patients), which copies of one patient's record would not; copies share the site in 58% of 96 pairs,
       against 14% from the site shares and 56% that their findings predict.
     - **No order:** no date or id, and the file is sorted by site.
     - **Overlap:** random 3-fold splits (20 repeats): 20.3% of test patients have an exact copy in training (14% to
       28% per split), and the copies' majority site is right for 52% of them.
   * **Consistency:** follows sepsis_survival_minimal_clinical_records and
     ai4d_lab_tanzania_tourism_classification_challenge, which keep repeated coarse profiles of distinct people[^4b];
     the 16 groups with several sites are an ambiguity the task has[^4c]. Issue 2's drop of the rows without a
     tissue type raises the repeated share from 16% to 20%, on the same coarse findings.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep as is (implemented) | 302 patients, random split; the notes gain the verdict and the 20% overlap | the copies are distinct patients, as a clinic meets them; they occur as often as the findings' links predict | a fifth of test patients has a look-alike in training |
     | B | Drop the same-site copies | 272 patients (30 dropped: 10 of 29 ovary, 6 of 24 breast, 6 of 20 head and neck, 2 of 10 prostate); lung 28% to 30% | no identical row with one site on both sides | drops real patients on a link the tests find to be chance; the sites with a typical pattern of spread lose weight; prostate falls to 8, below the floor of 10 |

   * **Recommendation:** A: the copies are as frequent as the findings' own links predict and share the site only as
     often as their findings predict, so they are distinct patients. **Decision:** keep (A) or drop the copies (B)?

   **Notes for the AI:** on A, once PR #62 is in, replace the duplicate bullet in `curation_comments` with "- Entity
   leakage, natural (2026-11-06): 49 of 302 patients repeat another's 17 findings (30 with the same site); a null
   keeping the findings' links gives as many (57, 95% 45-70), 16 of the 25 groups hold several sites and copies share
   the site as often as their findings predict (58% against 56%), and the file has no order but the site, so they are
   distinct patients with the same coarse findings. Under random 3-fold splits 20% of test patients have an exact copy
   in training."; rerun the numbers if issue 2 drops rows; no data change, no rebuild. On B, `drop_duplicates()` in
   `_clean` before the filter of small sites (prostate then leaves) or after it (prostate kept at 8, under the floor):
   ask which; `row`, `changes` and the notes updated, a `CC (<date>, Andrej):` line in the record.

   [^4a]: **LEAK-41** (Must, draft PR #62): repeats of a unit the data does not record get one verdict; natural when
     the look-alikes are distinct units: the random split stays and the notes give the share of test rows with a
     look-alike in training. **LEAK-42** (Should, draft PR #62): three tests set the verdict: matches against a chance
     rate that keeps the data's structure, label agreement against what the shared features predict, and an order.
   [^4b]: **LEAK-18** (Should): few features and plausible repeats are natural: keep them and say so
     (sepsis_survival_minimal_clinical_records keeps 110,204 rows over 975 distinct feature rows;
     ai4d_lab_tanzania_tourism_classification_challenge its 965 exact copies, Lennart, 2026-11-05).
   [^4c]: **LEAK-20** (Should): feature vectors that occur with both labels are dropped, unless they are genuine
     label ambiguity the task has.

   **Resolved (2026-11-09, Andrej):** A: the repeated patients stay as distinct patients with the same coarse findings;
   the duplicate note is replaced by the entity-leakage numbers.

5. **Still keep it now that lung_cancer is retired on its use case?**

   * **Problem:**
     - Issue 1 kept this dataset with an approximate fit (2026-11-09). A day later lung_cancer was retired on its use
       case (draft PR #75): molecular typing matters for ambiguous biopsies and tumours of unknown origin, and its rows
       hold neither, only the cases where the answer is already clear.
     - The same reading fits here: the decision (where to look for a primary that is unknown) has no rows in this
       data. These are patients whose primary was found, and their regional nodes point at it (issue 1).
     - The two decisions point opposite ways, and PR #75 states nothing that sets them apart. Keep this one with a
       stated difference, or retire it the same way?
   * **Background:**
     - Issue 1 asked whether to retire for representativeness (`Not Representative`). This issue asks about the use
       case, the reason lung_cancer and glioma_grading_clinical_and_mutation_features were retired for[^5a].
     - A gap between the rows and the use case's setting is otherwise an approximate fit, not a retirement[^5b];
       sarcoma and eryhemato_squamous_disease are kept that way.
   * **What could set them apart:**
     - **Where the label comes from.** lung_cancer's histology is read from the same resected tissue the arrays are
       run on, so a model can only cross-check a label the slide already gives, as in glioma. Here the primary site
       is found by a separate work-up (imaging, endoscopy, biopsy of the primary). The findings in the features do
       not contain it, so the task predicts something it does not cross-check, only for another population.
     - **Limit:** the data does not record whether the spread was found before the primary. For most of these
       patients the primary was probably known first, which weakens this point.
   * **Experiments:** none new; issue 1's numbers stand (hand rule 44% accuracy, TabPFN 3.5 54%; benchmark log loss
     1.294 to 1.493, class shares 2.203; TabPFN beats logistic regression on 59 of 60 splits).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep, difference written down (data as now) | data unchanged; a "differs from lung_cancer" note joins the lung_cancer row of the use-case Cases table and this record | follows issue 1 and the approximate-fit cases; the label is not a cross-check | rests on a difference the data cannot confirm (the order of findings) |
     | B | Retire on the use case | `No (Retired)`, `No Good Target / Scientific Discovery` next to `Selection Bias`; folder removed, `v2_path` cleared | one reading for both datasets; matches Andrej's objection of 2026-10-15 | reverses issue 1 of 2026-11-09; a task where the methods spread clearly leaves; the approximate-fit cases then need the same review |

   * **Recommendation:** A: the label is not read from the measured specimen, which is the fact the lung_cancer and
     glioma retirements rest on; the population gap is the one issue 1 already weighed. **Decision:** keep (A) or
     retire (B)?

   **Notes for the AI:** on A, add to the lung_cancer row of the USE-1 Cases table in `use_case.md` (PR #75 branch)
   "Differs from ljubljana_primary_tumor (kept, approximate): its primary site comes from a separate work-up, not from
   the specimen the features measure", and a `CC (<date>, Andrej):` line in this record; `checked_by` gains Andrej. On
   B, `suggestion: No (Retired)`, the marker added, a CC line naming the use case, the USE-1 Cases row, priority
   removed, folder removed and `v2_path` cleared, the same commit pattern as PR #75; then check sarcoma and
   eryhemato_squamous_disease against the same reading.

   [^5a]: **USE-1** (Must): a use case is an actor, a moment and a decision. Cases: glioma_grading_clinical_and_mutation_features
     (a grade already given by the pathologist, 2026-10-26, Lennart); lung_cancer (resected tumours whose slide is
     clear, 2026-11-10, Andrej, draft PR #75).
   [^5b]: **USE-8** (Must; amended 2026-10-27, Lennart): a selection bias is judged against the real-world setting of
     the use case; when that setting does not share it, the selection is a known gap and the fit is approximate.

   **Andrej (2026-11-11, discuss):** It is fine to look at problems retrospectively, as you say these are patients whose
   primary was found, and their regional nodes point at it. We need known ground truth patients for this task, it
   doesn't work otherwise. You also say the decision (where to look for a primary that is unknown) has no rows in this
   data - which is not true since all patients have a location identified, right?

   **Resolved (2026-11-11, Andrej):** A, kept. Right: every patient has the primary site identified, which is the ground
   truth the task needs, and a retrospective series of such patients is how this task can be built at all; the issue's
   claim that the decision has no rows here was wrong. What sets it apart from lung_cancer is that the label comes from
   a separate work-up, not from the specimen the features measure. A CC line in the record says so.

6. **`CrossSectional` instead of `ForcedIIDFromTemporal`?**

   * **Problem:**
     - The definition is tagged `ForcedIIDFromTemporal`, a forward use case whose time was lost[^fo-6].
     - The target is a present state measured with the features: the site of the primary tumour, read from the findings at diagnosis, and the use case reads it for new units at their own present[^cs-6].
     - The tag alone changes: the split stays random.
   * **Background:** the primary is found after the metastases are examined, but it is where the cancer already started; the use case estimates that present fact, not a later state.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Stay `ForcedIIDFromTemporal` (implemented) | the tag and its line stay | the decision stands | the tag claims a forecast the use case does not make |
     | B | `CrossSectional` | the tag and a `Time basis:` line naming the present state, the untested drift for later units and what a dated release would show | names the use case; no claim of a lost forward split | a new prototype on a decided tag |

   * **Recommendation:** B. **Decision:** A or B?

   **Notes for the AI:** on B, swap the tag, write the line, add a CC line; the split does not change.

   [^cs-6]: **SPLIT-32** (Should, 2026-11-13): a target measured together with the features, which the use case reads for new units at their own present, is `CrossSectional`, whether the dates survive or not; its line says whether the drift of the relation was measured or is untested. A label that only arrives later is no present state.
   [^fo-6]: **SPLIT-8** (Must): a forward use case without usable time ships in the closest regime, tagged forced from temporal, with a `Time basis:` line naming the reason.

   **Resolved (2026-11-13, Andrej):** withdrawn: `CrossSectional` was dropped the same day (it named no split the existing prototypes do not give: a present state used later is forced or a measured `StationaryRelation`, used within the covered time `Retrospective`). The tag stays.

## Reference

UCI
