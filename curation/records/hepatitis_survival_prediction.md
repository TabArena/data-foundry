---
unique_name: hepatitis_survival_prediction
name: hepatitis
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
decision_markers:
- Outdated
tags:
- Tiny Data
- 'Samples: Over Time'
- 'Time: Lost'
- 'Target: Unknown'
- Clinical Study
collections:
- TabArena Reject
original_source: UCI
year: '1988'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://github.com/EpistasisLab/pmlb/blob/master/datasets/hepatitis/metadata.yaml
- https://doi.org/10.24432/C5Q59J
- https://www.kaggle.com/datasets/abdelazizsami/hepatitis
notebook_path: datasets/beyond_iid/new_iid/hepatitis_survival_prediction/hepatitis_survival_prediction.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/hepatitis_survival_prediction/dataset.py
source_row: 760
type_adapter_id: curation-record-v1
---

## Comments

Already preprocessed data but otherwise looks like a good task, need to check group and cost files but would add!

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — Efron & Gong 1981/1986 study how to estimate the error rate of Gregory's logistic rule on these 155 patients: a statistics-methods paper, not a decision; 32 deaths, so accuracy is coarse. Original rejected: error rate. roc_auc is the binary fallback.

CC (2026-10-21, Lennart): the metric is the roc_auc fallback; Efron & Gong's error rate is the object of a resampling study on 155 patients, not the task's metric.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `optn_liver_waitlist_90day_mortality` (TBD -> Yes, priority 3). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-01, Lennart): the target rule (CLEAN-25) and the cut-end rule (CLEAN-14): the target ships as No/Yes, Yes the event (1 means the patient died (UCI: 1 DIE, 2 LIVE)).

CC (2026-11-17, Andrej): the declared split (random, 20x3 folds, `ForcedIIDFromTemporal`) is checked: the split decision tree, walked without the current split, reaches the split it ships (blind split review, cross-dataset item).

CC (2026-11-18, Andrej): the forced tag stays (Review issue 1, A; stationarity reasoning, SPLIT-32 as amended today): no reason to take later samples as interchangeable. An old one-time study whose outcome treatment has since transformed.

## Review

**Outcome:** added. Stationarity reasoning of 2026-11-18: the definition reaches the forced step with no time to measure; decided below.

**Main points:** Keep `ForcedIIDFromTemporal`, or tag `AssumedStationaryRelation`?

**Issues for Andrej:**

1. **Keep `ForcedIIDFromTemporal`, or tag `AssumedStationaryRelation`?**

   * **Problem:**
     - Time: Lost: 155 patients described by Efron and Gong 1981; place, period and follow-up unstated; no date or order.
     - Use: A physician estimates hepatitis prognosis today, 45+ years after collection.
     - Mechanism: Bilirubin, albumin, prothrombin, ascites, varices to death: liver physiology, but survival given them depends on treatment (antivirals, transplantation), which changed completely; two inputs are treatments.
   * **Background:** similar datasets[^asr].

     | Similar dataset or source | What was measured | Verdict | Why similar |
     |---|---|---|---|
     | cirrhosis_patient_survival_prediction (Mayo PBC) | v3 test over rebuilt two-year registration periods 1974-81 | inconclusive (counts as unmeasured) | liver-disease prognosis from lab values, small single-centre cohort |
     | AASLD-IDSA HCV guidance (2014 onward) / HBV nucleos(t)ide antivirals (literature, cited from memory: check) | curative or suppressive antiviral therapy introduced | changed treatments | chronic viral hepatitis prognosis |

   * **For a stationary use case:**
     - the physiological severity markers are those of Child-Pugh, still in use.
   * **Against:**
     - ~45-year span.
     - treatments changed (antivirals, transplant) and are inputs.
     - follow-up period unknown.
   * **Earlier views:**
     - CC 2026-11-17 (Andrej): random 20x3 checked by blind walk.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep `ForcedIIDFromTemporal` (implemented) | The folds stay; the Time basis line names the reasoning below | Claims only what is known | The split stands for later samples only as far as the use case is stationary |
     | B | `AssumedStationaryRelation` | The folds stay; you give the reason (eight words or more) | Documents why random folds stand for later samples | ~45-year span; treatments changed (antivirals, transplant) and are inputs |

   * **Recommendation:** A, an old one-time study whose outcome treatment has since transformed. Confidence: high. **Decision:** A or B?

   [^asr]: **SPLIT-32** (Should; amended 2026-11-18, Andrej): "where it holds none, the review reasons whether the use case can be taken as stationary, from the domain's mechanism and from similar datasets ..., where the AI offers `AssumedStationaryRelation` with a recommendation for a person to decide." `AssumedStationaryRelation` keeps the forced split's folds and replaces only the tag; its line opens `AssumedStationaryRelation (<person>, <date>): <reason>`.

   **Andrej (2026-11-18, ok):** as implemented.

   **Resolved (2026-11-18, Andrej):** A, as implemented: the forced tag stays; the `Time basis:` line gives the reasoning (An old one-time study whose outcome treatment has since transformed.)

## Reference

?
