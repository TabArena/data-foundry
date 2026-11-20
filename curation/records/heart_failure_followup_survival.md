---
unique_name: heart_failure_followup_survival
name: Heart Failure Clinical Records
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
tags:
- Tiny Data
- 'Samples: Over Time'
- 'Time: Lost'
- 'Target: Later'
- Clinical Study
collections:
- New (BeyondArena)
original_source: Other
year: '2017'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C5Z89R
notebook_path: datasets/beyond_iid/new_iid/heart_failure_followup_survival/heart_failure_followup_survival.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/heart_failure_followup_survival/dataset.py
source_row: 766
type_adapter_id: curation-record-v1
---

## Comments

CC (2026-09-30, Lennart): **Leak fixed: dropped `time` (follow-up days), which is only known after the outcome.** Chicco & Jurman 2020 (BMC Med Inform Decis Mak 20:16), Table 1: "Time | Follow-up period | Days | [4,...,285]" and "death event | If the patient died during the follow-up period"; the source study (Ahmad et al. 2017, PLOS ONE 12:e0181001) is a survival analysis with "dead and censored patients at the end of follow up period". Follow-up ends at death or censoring, so early deaths get short times (Chicco & Jurman, Fig. 4: 88.6% of month-0 patients died). Alone it gives ROC AUC 0.84; LightGBM 0.90 -> 0.75 without it (leak audit 2026-09-24). The label is still "died within a patient-specific follow-up of 4-285 days", so some censored patients may have died later.

Looks good

**Assessment (AI, 2026-10-14):** whether follow-up ended on one date for all patients cannot be determined: Ahmad et al. 2017 and Chicco & Jurman 2020 do not say, and neither file has dates. The censored follow-ups (12 to 285 days) fit a common end around mid-January 2016 but do not prove it. Each patient's window starts at their own admission, so the task stays as it is (Lennart's instruction).

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — Ahmad et al. 2017 (first publication) score a Cox model by time-dependent ROC AUC, which needs the follow-up time we drop (leak); Chicco & Jurman 2020 (the binary task we ship) rank by MCC at threshold 0.5, a default threshold, not a decision (MET-6). roc_auc is the binary fallback.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `zigong_heart_failure_mortality` (TBD -> Yes, priority 3). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-01, Lennart): the target rule (CLEAN-25) and the cut-end rule (CLEAN-14): the target ships as No/Yes, Yes the event (1 is the event).

CC (2026-11-17, Andrej): the declared split (random, 20x3 folds, `ForcedIIDFromTemporal`) is checked: the split decision tree, walked without the current split, reaches the split it ships (blind split review, cross-dataset item).

CC (2026-11-18, Andrej): the forced tag stays (Review issue 1, A; stationarity reasoning, SPLIT-32 as amended today): no reason to take later samples as interchangeable. Treatment changes move survival given the same findings, and the label itself depends on admission time; against outweighs the short span.

## Review

**Outcome:** added. Stationarity reasoning of 2026-11-18: the definition reaches the forced step with no time to measure; decided below.

**Main points:** Keep `ForcedIIDFromTemporal`, or tag `AssumedStationaryRelation`?

**Issues for Andrej:**

1. **Keep `ForcedIIDFromTemporal`, or tag `AssumedStationaryRelation`?**

   * **Problem:**
     - Time: Lost for the split: admissions April-December 2015; follow-up time dates survivors only (end ~mid-January 2016), not deaths, so no outcome-free order.
     - Use: A cardiologist estimates death risk in the coming months for heart-failure patients after 2015.
     - Mechanism: Ejection fraction, creatinine, sodium and age to death: physiology, but mortality given these depends on therapy, which changed (ARNI, SGLT2 inhibitors, guideline-directed therapy).
   * **Background:** similar datasets[^asr].

     | Similar dataset or source | What was measured | Verdict | Why similar |
     |---|---|---|---|
     | 2_month_survival_rate_prediction (SUPPORT) | v3 stationary-relation test, phase I 1989-91 -> phase II 1992-94, death ROC AUC forward vs contemporaneous | flat (LightGBM gap 0.0008, TabPFN gap 0.0027) | clinical prognosis of hospitalised patients from admission physiology, one 3-year step |
     | McDonagh TA et al., 2021 ESC Guidelines for heart failure, Eur Heart J 2021;42:3599-3726 (literature, cited from memory: check) | four-pillar therapy (ARNI, beta-blocker, MRA, SGLT2i) with mortality benefit | changed treatments | HFrEF prognosis after 2015 |
     | Davis SE et al., 'Calibration drift in regression and machine learning models for acute kidney injury', JAMIA 2017;24(6):1052-1061 (literature, cited from memory: check) | VA hospital models over 9 years | discrimination stable, calibration drifted | routine-lab clinical risk model used years after fitting |

   * **For a stationary use case:**
     - nine months of collection.
     - SUPPORT tested flat over a 3-year step for hospital prognosis.
   * **Against:**
     - changed treatments since 2015 lower mortality at the same EF/creatinine.
     - variable follow-up 4-285 days: label depends on admission month (later admissions censored earlier)
     - single Faisalabad setting.
   * **Earlier views:**
     - Time basis line (Andrej, 2026-11-11): no split by admission date can be built without the outcome.
     - CC 2026-11-17 (Andrej): random 20x3 checked by blind walk.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep `ForcedIIDFromTemporal` (implemented) | The folds stay; the Time basis line names the reasoning below | Claims only what is known | The split stands for later samples only as far as the use case is stationary |
     | B | `AssumedStationaryRelation` | The folds stay; you give the reason (eight words or more) | Documents why random folds stand for later samples | changed treatments since 2015 lower mortality at the same EF/creatinine; variable follow-up 4-285 days: label depends on admission month (later admissions censored earlier) |

   * **Recommendation:** A, treatment changes move survival given the same findings, and the label itself depends on admission time; against outweighs the short span. Confidence: high. **Decision:** A or B?

   [^asr]: **SPLIT-32** (Should; amended 2026-11-18, Andrej): "where it holds none, the review reasons whether the use case can be taken as stationary, from the domain's mechanism and from similar datasets ..., where the AI offers `AssumedStationaryRelation` with a recommendation for a person to decide." `AssumedStationaryRelation` keeps the forced split's folds and replaces only the tag; its line opens `AssumedStationaryRelation (<person>, <date>): <reason>`.

   **Andrej (2026-11-18, ok):** as implemented.

   **Resolved (2026-11-18, Andrej):** A, as implemented: the forced tag stays; the `Time basis:` line gives the reasoning (Treatment changes move survival given the same findings, and the label itself depends on admission time; against outweighs the short span.)

## Reference

@article{chicco2020machine,
  title={Machine learning can predict survival of patients with heart failure from serum creatinine and ejection fraction alone},
  author={Chicco, Davide and Jurman, Giuseppe},
  journal={BMC medical informatics and decision making},
  volume={20},
  number={1},
  pages={16},
  year={2020},
  publisher={Springer}
}
