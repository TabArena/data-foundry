---
unique_name: differentiated_thyroid_cancer_recurrence
name: Differentiated Thyroid Cancer Recurrence
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
suggestion: 'Yes'
priority: 1
tags:
- Tiny Data
- 'Samples: Over Time'
- 'Time: Lost'
- 'Target: Varying Delay'
- Clinical Study
collections:
- TabSTAR
original_source: UCI
year: '2023'
collection_period: 2008-2023
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C5632J
- https://www.openml.org/search?type=data&id=46605&sort=runs&status=active
v2_path: datasets/_dev/tabarena-v0pt2/differentiated_thyroid_cancer_recurrence/dataset.py
source_row: 788
type_adapter_id: curation-record-v1
---

## Comments

Might be panel / longitudinal data, but is already made to be IID

Otherwise, looks reasonable and might be a valid task

Performance in paper is already very high, likely trivial

**Assessment (AI, 2026-10-07):** One row per patient: the 383 differentiated cancers of a 400-patient endocrine-clinic cohort in Hamadan, 2008-2023 (Khazaei et al. 2024, J Res Health Sci 24:e00632, open access; Table 2 matches the file). `Response` is a post-treatment assessment ("determined based on the laboratory findings of thyroglobulin and antithyroglobulin and a whole-body scan", same paper, Methods), and a structural incomplete response is persistent or new metastatic disease (ATA 2015, [B29]): 89 of 91 such patients recurred. The v2 definition drops it and the undefined radiotherapy column and predicts at initial staging. ROC AUC is then 0.93 against 0.896 for the ATA risk alone (beaten on 59-60 of 60 splits), so `Trivial` does not hold. No open text defines recurrence.

**Assessment (AI, 2026-10-20):** priority 1 for the review of the added dataset: gap -, use case -, source +, shape -, risk - (Issue 2: label definition unverified, 'Recurred' may include persistent disease (paper paywalled)). Tiny clinical cohort (383 patients) predicting recurrence at staging; beats ATA risk alone, but the label definition is unverified.

**Assessment (AI, 2026-10-20):** Review panel (re-check): ship after changes, made in the definition. The fit is approximate: `M` is kept although 2 of the 18 M1 patients are ATA intermediate risk (a potential leak kept on purpose, +0.001 ROC AUC), the label's breadth is unverified and the data come from one clinic. `Risk` gets a potential-leak note (a crude ATA rule agrees in 337 of 383 rows; at most +0.010 ROC AUC), the use case names the decisions taken at staging (radioiodine, the TSH target, the initial follow-up schedule), and the follow-up is written as the source's claim, which conflicts with the 2008-2023 cohort period. Recurrence is 4.8% / 62.7% / 100% by ATA risk class against about 3% / 21% / 68% in Tuttle 2010, so the label probably counts persistent disease; all 34 high-risk or M1 patients recurred (ROC AUC 0.928 with them, 0.901 without, as for any equally easy positives). `Trivial` is refuted (TP-4: a random forest beats `Risk` alone, 0.896, on 59 of 60 splits). Open for Lennart (the Review): the label and the paper's cohort from the PDF (issue 2), drop or keep `Hx Radiothreapy` (issue 6), and two rule questions in the Across datasets view (USE-8 and an unverified label; thyroid_discordant's `Trivial`). Priority 1: gap -, use case - (the fit is approximate), source +, shape - (383 patients), risk - (the label's definition and the cohort are unverified).

CC (2026-10-21, Lennart): an unverified label definition makes the fit approximate ("yea it does"), and a potential leak kept on purpose does not by itself ("stay with direct fit if the task (without leakage) would be a direct fit"); USE-8 amended. The fit stays approximate, now for the unverified label (breadth and follow-up); the kept `M` is no longer a reason for it.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — Borzooei et al. 2023 report AUC, sensitivity and specificity, none named as the criterion.

CC (2026-10-26, Lennart): the `Trivial` marker is removed, as the definition has it (TP-4: without `Response`, a random forest beats the risk class alone on 59 of 60 splits, mean gain 0.032 ROC AUC; the paper's 0.98-0.997 used `Response`).

**Assessment (AI, 2026-10-26):** the paper read (Borzooei et al. 2024, Eur Arch Otorhinolaryngol 281:2095-2104, the curator's PDF). Cohort: 383 patients of one centre, Table 1 with ATA high risk 32 and M1 18 as in the file, so the 34 high-risk or M1 patients are in the paper's cohort (issue 2: keep, (a)). Label: "recurrence status (including both locoregional and distant metastasis)", persistence not separated from recurrence. Follow-up: "a minimum follow-up period of 10 years ... The study spanned a period of 15 years". `Hx Radiothreapy` is "history of radiation therapy to the head and neck region", recorded with age and smoking at diagnosis (issue 6: keep, (b)). The paper's top feature is the structurally incomplete response (importance 0.843), which we drop.

CC (2026-10-26, Lennart): issue 2: "ok keep then": the 34 ATA high-risk or M1 patients stay, as the paper's cohort includes them (LEAK-22).

CC (2026-10-26, Lennart): issue 6, option (b): `Hx Radiothreapy` stays as a plain input, as the paper defines it as a history of head and neck irradiation collected at diagnosis ("ok (b)").

**Assessment (AI, 2026-10-26):** issues 2 and 6 applied: `Hx Radiothreapy` is back among the 15 features with the paper's definition in the notes; the label, cohort and follow-up notes quote the paper; the metric note cites its Table 2. dataset check: 0 errors, 0 warnings. No open issue left.

CC (2026-10-26, Lennart): verdict ship.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): 5 ordinal scales typed as ordered categories in the codebook's order (CLEAN-14, amended): `Thyroid Function`, `Risk`, `T`, `N`, `Stage` (the README lists their levels).

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `dtc_milan_nijmegen_progression` (TBD -> 2nd Tier, priority 1). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-17, Andrej): the declared split (random, 20x3 folds, `ForcedIIDFromTemporal`) is checked: the split decision tree, walked without the current split, reaches the split it ships (blind split walk).

CC (2026-11-18, Andrej): the forced tag stays (Review issue 1, A; stationarity reasoning, SPLIT-32 as amended today): no reason to take later samples as interchangeable. Changed rules and staging inside and after the collection span are named facts against.

CC (2026-11-27, Andrej): the declared metric (ROC AUC on the recurrence label, the binary fallback) is checked and stays as declared.

CC (2026-11-27, Andrej): ship as defined (review of 2026-11-27).

## Review

**Outcome:** added. Stationarity reasoning of 2026-11-18: the definition reaches the forced step with no time to measure; decided below (issue 1, A, 2026-11-18).

**Main points:** Task gamer (blind, 2026-11-27): nothing gamed. Honest HGB ROC AUC 0.929 (logistic 0.930, noise 0.003); row position and exact-copy lookups score lower. `Risk` alone scores 0.892, 0.037 below the full model: the known kept leak, its size as recorded. Re-audited on 2026-11-27: nothing to decide. `Response`, assessed during follow-up and in its structural category the outcome itself (89 of 91 such patients recurred), is already dropped and among none of the 15 features. Every kept clinical column is a finding at surgery, and the kept-on-purpose note on `Risk` reproduces (without it the score falls by only 0.011 ROC AUC, so the model does not rest on it). The raw file is sorted by outcome rather than time (nearly all recurrences sit in its last hundred rows), which is harmless under stratified random folds and would matter only to someone who took its first rows as a test set. Earlier: `ForcedIIDFromTemporal` stays (issue 1, A, 2026-11-18). Nothing is left open.

**Issues for Andrej:**

1. **Keep `ForcedIIDFromTemporal`, or tag `AssumedStationaryRelation`?**

   * **Problem:**
     - Time: Lost: Hamadan clinic, cohort 2008-2023 (Khazaei et al. 2024) vs the paper's '15 years, 10-year follow-up'; no diagnosis date.
     - Use: An endocrinologist estimates recurrence risk at the initial staging visit for patients treated later.
     - Mechanism: Stage, pathology and ATA risk class to recurrence; recurrence depends on RAI and TSH-suppression practice and on how persistent disease is counted, which the ATA 2015 guidelines changed.
   * **Background:** similar datasets[^asr].

     | Similar dataset or source | What was measured | Verdict | Why similar |
     |---|---|---|---|
     | Haugan BR et al., 2015 ATA Management Guidelines, Thyroid 2016;26(1):1-133 (literature, cited from memory: check) | risk-adapted RAI, new response-to-therapy categories, AJCC 8th staging (2017) | changed rules and coding | same clinical decision |
     | Davis SE et al., 'Calibration drift in regression and machine learning models for acute kidney injury', JAMIA 2017;24(6):1052-1061 (literature, cited from memory: check) | VA hospital models over 9 years | discrimination stable, calibration drifted | routine-lab clinical risk model used years after fitting |

   * **For a stationary use case:**
     - tumour stage and pathology are biological.
   * **Against:**
     - the collection spans ~15 years with a guideline change (2015) and staging change (AJCC 8th, 2017) inside it.
     - the definition itself says later patients are treated 'under later practice'.
     - later patients' labels may be censored (follow-up conflict)
   * **Earlier views:**
     - CC 2026-11-17 (Andrej): random 20x3 checked by blind walk.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep `ForcedIIDFromTemporal` (implemented) | The folds stay; the Time basis line names the reasoning below | Claims only what is known | The split stands for later samples only as far as the use case is stationary |
     | B | `AssumedStationaryRelation` | The folds stay; you give the reason (eight words or more) | Documents why random folds stand for later samples | the collection spans ~15 years with a guideline change (2015) and staging change (AJCC 8th, 2017) inside it; the definition itself says later patients are treated 'under later practice' |

   * **Recommendation:** A, changed rules and staging inside and after the collection span are named facts against. Confidence: high. **Decision:** A or B?

   [^asr]: **SPLIT-32** (Should; amended 2026-11-18, Andrej): "where it holds none, the review reasons whether the use case can be taken as stationary, from the domain's mechanism and from similar datasets ..., where the AI offers `AssumedStationaryRelation` with a recommendation for a person to decide." `AssumedStationaryRelation` keeps the forced split's folds and replaces only the tag; its line opens `AssumedStationaryRelation (<person>, <date>): <reason>`.

   **Andrej (2026-11-18, ok):** as implemented.

   **Resolved (2026-11-18, Andrej):** A, as implemented: the forced tag stays; the `Time basis:` line gives the reasoning (Changed rules and staging inside and after the collection span are named facts against.)

## Reference

@article{borzooei2024machine,
  title={Machine learning for risk stratification of thyroid cancer patients: a 15-year cohort study},
  author={Borzooei, Shiva and Briganti, Giovanni and Golparian, Mitra and Lechien, Jerome R and Tarokhian, Aidin},
  journal={European Archives of Oto-Rhino-Laryngology},
  volume={281},
  number={4},
  pages={2095--2104},
  year={2024},
  publisher={Springer}
}
