---
unique_name: early_stage_diabetes_risk_prediction
name: Early Stage Diabetes Risk Prediction
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: No (Retired)
decision_markers:
- Selection Bias
- Not Representative
tags:
- Tiny Data
collections:
- New (BeyondArena)
- TabSTAR
original_source: UCI
year: '2020'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C5VG8H
- https://www.openml.org/search?type=data&id=43643&sort=runs&status=active
- https://www.kaggle.com/datasets/ishandutta/early-stage-diabetes-risk-prediction-dataset
notebook_path: datasets/beyond_iid/new_iid/early_stage_diabetes_risk_prediction/early_stage_diabetes_risk_prediction.ipynb
source_row: 765
type_adapter_id: curation-record-v1
---

## Comments

Looks good

CC (2026-10-19, Andrej): I disagree with keeping it; the patients are not the population the task is for, and the file is half duplicates.

- **Wrong population:** the use case is screening adults for a blood-sugar test, but every row is a patient of a diabetes hospital, 62% diabetic (69% after dedup); UCI calls them "newly diabetic or would be diabetic". How the negatives were recruited and how the label was set is not stated. Other datasets pass with an approximate fit, but here the gap is why the features work at all.
- **The symptoms work because of who was sampled** (spectrum bias: a test looks better when cases are clear-cut and controls are healthy; Ransohoff and Feinstein 1978). Early type 2 diabetes is usually without symptoms, which is why screening uses blood tests; here symptomatic patients face hospital negatives who mostly report none. Polyuria and polydipsia (frequent urination, excessive thirst; the classic symptoms in the diagnostic criteria) added up, with no training, give AUC 0.905, LR on them plus sex 0.937. Partial paresis (partial paralysis, a late complication) is a strong positive marker, so many positives are established cases, not early ones.
- **Half the file repeats itself:** 52% of the 520 rows exactly repeat another row on all 17 columns (61% of negatives, 46% of positives), mostly rows with several symptoms, which distinct patients would rarely share; 74% of rows 260-519 repeat a row from 0-259. After dedup only 78 negatives remain (~26 per test fold), the class balance shifts from 62% to 69% positive, and which rows are real patients is unknown.

Suggest excluding.

Ransohoff DF, Feinstein AR. Problems of spectrum and bias in evaluating the efficacy of diagnostic tests. N Engl J Med. 1978;299(17):926-930. doi:10.1056/NEJM197810262991705

Islam MMF, Ferdousi R, Rahman S, Bushra HY. Likelihood prediction of diabetes at early stage using data mining techniques. In: Computer Vision and Machine Intelligence in Medical Image Analysis. Advances in Intelligent Systems and Computing, vol 992. Singapore: Springer; 2019:113-125. doi:10.1007/978-981-13-8798-2_12

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — Islam et al. 2019 report accuracy with precision, recall and F-measure, no unique metric and no threshold or costs (MET-5, MET-6).

CC (2026-11-10, Andrej): stays retired, for several reasons that hold together, not one: the selection bias (69% diabetic, late symptoms such as partial paresis in 57% of positives, negatives mostly men) makes the task not even an approximate fit for early-stage screening; an untrained symptom rule reaching ROC AUC 0.905 is far too high for the noisy real task; and models solving it almost perfectly (TabPFN 3.5 0.972) is unrealistic. Markers `Selection Bias` and `Not Representative`.

CC (2026-11-11, Andrej): BeyondArena v0.2 review page, early_stage_diabetes_risk_prediction: the marks repeat the decisions of 2026-11-10 and change nothing here.
- Issue 1 (`discuss`): stays retired on the reasons together, as the CC of 2026-11-10 records.
- Issue 2 (`change`, B: keep and document): confirmed but not applicable: the folder is out of the working copy, so the sex skew and the alopecia confound are written into the record's Review instead of a definition.
- The review moved from the folder's file into this record's `## Review` section.

## Review

**Outcome:** added; retired 2026-10-27 (`No (Retired)`), reopened 2026-11-10: the AI recommends reversing the
retirement and keeping it with the `Selection Bias` marker and the approximate fit it already has. 520 questionnaire
rows from patients of Sylhet Diabetes Hospital, Bangladesh (UCI 529, Islam et al. 2019), 251 after the definition
drops exact repeats; the label is diabetic or not (69%). The two recorded reasons, the wrong population and the
duplicates, are both real, but the rules treat the first as a concern flag and the definition already fixes the
second (issue 1). TabPFN 3.5 reaches ROC AUC 0.972 and beats the unfitted classic-symptom rule (0.905) on every
fold. The sex column carries a sampling skew: 80 of the 91 women are diabetic (issue 2).

**Main points:** Retired 2026-10-27; reassessed 2026-11-10 and kept retired on several reasons together: the selection
makes the fit none, a symptom rule at 0.905 and near-perfect models are unrealistic (issue 1). Nothing open.

**Record judgment:** valid source, thin documentation (how negatives were recruited and how the label was set are not
stated). The record holds Lennart's `Looks good`, Andrej's CC of 2026-10-19 (wrong population; half the rows repeat)
and `No (Retired)` of 2026-10-27 with the `Selection Bias` marker. PR #58 removes the folder; it waits for issue 1.

**Issues for Andrej:**

1. **Reverse the retirement, or retire for a reason that holds?**

   * **Problem:**
     - The decisive fact: no unfitted symptom rule comes near the models (classic symptoms 0.905 against TabPFN 3.5
       0.972, TabPFN better on 60 of 60 folds), so the task is not trivial, and among men alone, where the sex skew
       is absent, the models score the same (0.971).
     - The wrong population is real (a diabetes hospital, not a screening population), but the rules make that a
       concern flag that usually keeps the dataset, and the definition already states it as an approximate fit.
     - The duplicates are already dropped by the definition; 78 negatives remain, about 26 per test fold.
   * **Background:**
     - UCI: "collected using direct questionnaires from the patients of Sylhet Diabetes Hospital", "newly diabetic or
       would be diabetic". Whether a patient knew the diagnosis when answering is not stated and cannot be tested.
     - The positives are symptomatic: 73% report frequent urination, 57% partial paresis (a late complication), while
       screen-detected type 2 diabetes is mostly without symptoms. 33 of the 78 negatives report two symptoms or
       fewer, against 7 of the 173 positives.
   * **Experiments:** ROC AUC over the definition's 60 splits (20 repeats x 3 folds, seed 4267), 251 deduplicated
     rows. Rules are scored as they stand, without training. "Men only" scores the same models on the male test rows
     (67 negatives, 93 positives in all).

     | Model or rule | All rows | Men only | TabPFN 3.5 better on (all rows) |
     |---|---|---|---|
     | Frequent urination + excessive thirst, unfitted | 0.905 | 0.919 | 100% of folds (+0.066) |
     | The same + sudden weight loss, unfitted | 0.912 | 0.909 | 100% of folds (+0.060) |
     | Logistic regression | 0.944 | 0.938 | 97% of folds (+0.027) |
     | TabPFN 3.5 without sex and alopecia | 0.958 | 0.971 | 97% of folds (+0.014) |
     | Random forest | 0.972 | 0.969 | 53% of folds (+0.000) |
     | TabPFN 3.5 | 0.972 | 0.971 | |

   * **The candidate reasons and what was found:**

     | Reason | Finding | Holds as an exclusion? |
     |---|---|---|
     | Wrong population (hospital patients, not a screening population) | true; 69% diabetic, symptomatic positives | no: a concern flag, kept with the marker and an approximate fit, which the definition already says[^1a] |
     | Symptoms recorded with or after the diagnosis | not stated; cannot be tested from the file | no: an unsettled label timing makes the fit approximate[^1b] |
     | Cases and controls from different places | not stated; the one trace is sex (88% of women diabetic, 58% of men) | no: among men the models score the same; see issue 2 |
     | Duplicates uneven by class | 52% of rows repeat (61% of negatives, 46% of positives); dropped by the definition | no: fixed[^1c] |
     | Too few negatives | 78 after dedup, about 26 per test fold | no: a tiny-data task[^1d] |
     | Trivial (classic symptoms) | the unfitted rule loses to every model on every fold | no: neither beats nor matches[^1e] |
     | Ages outside the documented 20-65 | 30 deduplicated rows (16 to 90) | no: a documentation gap, not a wrong value |

   * **Consistency:** the selection-bias precedents stay in with the marker: eryhemato_squamous_disease (lichen
     planus patients from a referral series, approximate fit), obesity_estimation and website_phishing (cases and
     controls collected apart). hepatitis_survival_prediction, retired the same day, was reopened on 2026-11-10 for
     the same reason: no recorded reason survives a test or the rules.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Retired, reasons as recorded (implemented) | `No (Retired)` on the CC of 2026-10-19; PR #58 removes the folder | no change to PR #58; the screening use case is far from these patients | departs from the rule that selection bias is a concern flag; the duplicates reason is already fixed |
     | B | Retire on selection bias, with a rule change | the same, plus a rule that selection bias excludes when it is why the features work | states the real objection | a new exclusion that would reopen eryhemato_squamous_disease and the other kept selection-bias datasets; among men the signal is unchanged |
     | C | Reverse the retirement | `suggestion: Yes` with `Selection Bias`; the folder stays; fit stays approximate; PR #58 drops it from its removals | no tested reason against it; models separate clearly from the clinical rule | 251 rows from an undocumented hospital sample stay in the benchmark |

   * **Recommendation:** C: the gaps are real but already written into the fit and the marker, and the rule that
     would retire it (a trivial symptom rule) fails on every fold. **Decision:** keep retired (A), retire with a rule
     change (B), or reverse (C)?

   **Notes for the AI:** on C: record `suggestion: Yes`, keep `Selection Bias`, a `CC (2026-11-10, Andrej):` line in
   Andrej's words that the retirement is reversed (no reason holds; the symptom rule 0.905 against 0.972), `Andrej`
   already in `checked_by`; remove early_stage_diabetes_risk_prediction from PR #58 (record change, CHANGELOG, PR
   description); add the symptom-profile facts (73% polyuria, 57% partial paresis among positives) to `fit_reason`
   or `curation_comments`; run `dataset check`. On A: nothing changes. On B: draft the rule in selection.md
   ("Selection bias") with Andrej's wording and list the kept datasets it would reopen before applying. Evidence:
   `probe_results.csv` and the earlier `results.csv` in the local review folders.

   [^1a]: selection.md, "Selection bias" (Andrej, 2026-10-20; Lennart, 2026-10-27): cases and controls collected
     apart, or only typical or confirmed cases, get `Selection Bias`; "the verdict is usually still `Yes`"; the fit is
     approximate when the real setting of the use case lacks the bias.
   [^1b]: **USE-8** (Must): approximate fit, a stand-in with a known gap, among them a label definition the sources do
     not settle.
   [^1c]: **LEAK-19** (Should): exact copies with the same label are dropped.
   [^1d]: **TP-5** (Must): `Too Small` means a handful of units of a class per test fold; a small dataset as such is
     a tiny-data task like the others.
   [^1e]: **TP-4** (Must; as amended in PR #57): a feature or unfitted rule that beats the methods proves `Trivial`;
     one that matches them makes the dataset a candidate to drop.

   **Andrej (2026-11-10, discuss):** We retire because several potential reasons hold, nut just one: There is selection
   bias that makes the task not even approximate, but also the other things like that 0.9 AUC for this task using a
   simple is way too high given the noisiness of real early stage diabetes predictio and that models solve it almost
   perfectly is also unrealistic.

   **Resolved (2026-11-10, Andrej):** A, stays retired, on the reasons together: a selection that makes the fit none
   (not even approximate for early-stage screening), an untrained symptom rule at ROC AUC 0.905 that is far too high for
   the real task, and near-perfect models (0.972). The record's CC line says so, with the markers `Selection Bias` and
   `Not Representative`; PR #58 keeps its removal.

   **Andrej (2026-11-11, discuss):** We retire because several potential reasons hold, nut just one: There is
   selection bias that makes the task not even approximate, but also the other things like that 0.9 AUC for this task
   using a simple is way too high given the noisiness of real early stage diabetes predictio and that models solve it
   almost perfectly is also unrealistic.

   **Answer (AI, 2026-11-11):** The same note as on 2026-11-10, and it is already carried out: the dataset is
   retired on the three reasons together. Nothing further to apply, and nothing was re-measured.

   * The record holds `suggestion: No (Retired)` with the markers `Selection Bias` and `Not Representative`, and the
     CC line of 2026-11-10 states the three reasons in your words.
   * The folder is out of the working copy, so there is no definition left to change.
   * The one thing the retirement reason does not yet have anywhere but here: it rests on a reading the rules do not
     carry, that selection bias can make a fit none rather than approximate, and that an untrained rule far above
     the real task's noise is itself a reason. The rules under `knowledge-curation/references/` were not edited.

2. **What to do with the sex column, which carries a sampling skew?**

   * **Problem:**
     - 80 of the 91 women are diabetic against 93 of the 160 men, and only 11 of the 78 negatives are women, while
       diabetes is about as common in both sexes in Bangladesh, which points to how the negatives were recruited.
     - Alopecia looks protective only through sex: among men 47% of positives (44 of 93) and 49% of negatives (33 of 67) report it.
     - Keep sex as recorded, note the skew, or drop sex and alopecia, if issue 1 keeps the dataset?
   * **Effect on the task:** a model learns "woman, so diabetic", which would not hold in a screening population.
   * **Experiments:** TabPFN 3.5 over 60 splits: with sex and alopecia 0.972, without 0.958 (TabPFN with them better
     on 97% of folds); among men alone 0.971 both ways. Sex alone reaches ROC AUC 0.661.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep as recorded (implemented) | no change | no change; sex is a legitimate input | the skew is not documented |
     | B | Keep and document | a curation note naming the skew (88% of women, 58% of men diabetic; 11 negative women) and the alopecia confound | the definition says what the column carries; no values change | the model still uses the skew |
     | C | Drop sex and alopecia | both columns leave the features | removes the sampling trace | removes recorded inputs; the selection itself stays; departs from minimal preprocessing for a selection, not a recording, artefact |

   * **Recommendation:** B: the skew comes from selection, which the marker already flags; documenting it changes no
     values. **Decision:** keep (A), keep and document (B) or drop (C)?

   **Notes for the AI:** on B: add to `curation_comments` in dataset.py: "- Note: the negatives are mostly men (67 of
   78); 88% of women are diabetic against 58% of men, which points to how the negatives were recruited. Alopecia
   looks protective only through sex (no difference among men). Dropping sex and alopecia lowers TabPFN 3.5 from
   0.972 to 0.958; among men alone the score is the same." Then `dataset check`. On C: drop `Gender` and `Alopecia`
   in `_clean`, a curation bullet with the numbers, `dataset check`.

   **Andrej (2026-11-10, change):** Option B: Keep and document.

   **Resolved (2026-11-10, Andrej):** no change: the dataset stays retired (issue 1); had it stayed, the sex skew and
   the alopecia confound would have been documented (B).

   **Andrej (2026-11-11, change):** Option B: Keep and document.

   **Resolved (2026-11-11, Andrej):** B confirmed, and it cannot be applied: the dataset is retired (issue 1) and its
   folder is out of the working copy, so there is no `curation_comments` to carry the note. The numbers stay here:
   the negatives are mostly men (67 of 78), 88% of the women are diabetic against 58% of the men, alopecia looks
   protective only through sex (47% of male positives, 49% of male negatives), and dropping sex and alopecia lowers
   TabPFN 3.5 from 0.972 to 0.958 while the men-only score stays 0.971. If the retirement is ever reversed, B is
   what the definition takes.

## Reference

@inproceedings{islam2019likelihood,
  title={Likelihood prediction of diabetes at early stage using data mining techniques},
  author={Islam, MM Faniqul and Ferdousi, Rahatara and Rahman, Sadikur and Bushra, Humayra Yasmin},
  booktitle={Computer Vision and Machine Intelligence in Medical Image Analysis: International Symposium, ISCMM 2019},
  pages={113--125},
  year={2019},
  organization={Springer}
}
