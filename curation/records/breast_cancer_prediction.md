---
unique_name: breast_cancer_prediction
name: Breast cancer prediction
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
suggestion: 'Yes'
tags:
- New IID
- 'Samples: Over Time'
- 'Time: Lost'
- 'Target: Fixed Delay'
- Clinical Study
collections:
- TabSTAR
original_source: GOV Website
year: '2014'
collection_period: Jan 2005 - Dec 2008
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.bcsc-research.org/index.php/datasets/mammography_dataset
- https://www.kaggle.com/datasets/haithemhermessi/breast-cancer-screening-data-set
- https://www.openml.org/search?type=data&id=43687&sort=runs&status=active
v2_path: datasets/_dev/tabarena-v0pt2/breast_cancer_prediction/dataset.py
source_row: 677
type_adapter_id: curation-record-v1
---

## Comments

Cancer type and Is_Binary_Indicator_Of_Cancer_Diagnosis and Radiologists_Assessment might be target cols

"Some women contribute multiple examinations to the dataset." -> some leakage / problems

**Assessment (AI, 2026-10-07):** The original is the BCSC Digital Mammography Dataset (bcsc-research.org, 2014; download after a registration form, "teaching tool only"). Our file is byte-identical to the BCSC's `dataset.csv`; Kaggle and OpenML 43687 drop two duplicate rows. Target: cancer within one year, the BCSC's own question ("predict occurrence of any cancer using patient characteristics and mammography assessment"). Cancer type encodes the label and is dropped; TabSTAR keeps it. 3,133 of 36,714 women (`ptid`) have 2-4 exams; the 20 of them with cancer are positive only on their last. Grouped by woman. The BI-RADS assessment alone gives AUC 0.907, boosted trees 0.93; without the radiologist's readings, logistic regression reaches 0.58. Open: does the breast_w image rule cover these readings?

CC (2026-10-15, Lennart): The BI-RADS readings are valid tabular inputs: screening programmes run tabular risk models on them, so the image-scoring rule (breast_w) does not apply; the real-world use decides. One exam per woman, her earliest, with IID folds: the use case is one woman's screening read and most women have one exam.

**Assessment (AI, 2026-10-15):** One exam per woman keeps 36,714 rows and 239 of the 259 cancers (the 20 women with cancer and several exams are positive only on their last exam). Untuned LightGBM scores alike either way (ROC AUC 0.928 earliest exam, 0.923 latest, 0.925 all exams grouped). Regularised LightGBM 0.929 and a random forest 0.927 beat the assessment alone (0.914) on 8 of 9 splits.

CC (2026-10-15, Lennart): Ship (review of the 2026-10-07 run).

CC (2026-10-21, Lennart): "yes we should have one clear way to treat 0/1 flags": every 0/1 flag (a feature holding only 0 and 1, plus missing values; booleans too) is categorical (CLEAN-14, amended). Typed categorical here: comparison_mammogram_available, current_hormone_therapy, prior_breast_biopsy, prior_mammogram, family_history_breast_cancer.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — The BCSC page poses the question (predict any cancer from patient characteristics and the mammography assessment) but names no metric; it suggests the data for 'statistical methods for binary outcomes'.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): left unordered: `birads_assessment` (a level outside the scale is a state of its own); ordinal scales shipped as numbers, left as numbers for the curator's review: `birads_breast_density`.

CC (2026-10-31, Lennart): marks on the review board of PR #37 (ordinal scales in the codebook's order, also when shipped as numbers; a state outside a scale missing when the column has no other missing value, else the lowest level; cycles ordered; codes shipped as numbers as categories): 1 ordinal scales shipped as numbers are ordered categories (point 3); 1 columns with a state outside the scale ordered, the state placed by the rule.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found a related task: `bcsc_risk_estimation` (TBD -> Yes, priority 3). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-01, Lennart): the decode rule (a code whose codebook says in words what each level is carries the words; a score without them is a number): 1 coded columns carry their words.

CC (2026-11-17, Andrej): the declared split (random, 3x3 folds, `ForcedIIDFromTemporal`) is checked: the split decision tree, walked without the current split, reaches the split it ships (blind split walk).

CC (2026-11-18, Andrej): the forced tag stays (Review issue 1, A; stationarity reasoning, SPLIT-32 as amended today): no reason to take later samples as interchangeable. The main feature is a reading that technology and BI-RADS coding changed; changed coding is a fact against.

## Review

**Outcome:** added. Stationarity reasoning of 2026-11-18: the definition reaches the forced step with no time to measure; decided below (issue 1, A, 2026-11-18).

**Main points:** Task gamer (blind, 2026-11-27): nothing gamed. Untuned LightGBM ROC AUC 0.928 (a random column moves it by 0.004 to 0.007); row position (0.508 alone), value counts over all rows and `bmi` formats add at most 0.003. Nearly all skill is the radiologist's read: `birads_assessment` alone 0.914, the rest together 0.582. Its missing value (7.8% of rows, 6.5% cancers against 0.16%) is BI-RADS 0, a recall for more imaging placed as missing by `_clean`, so a deployed model has it; a format-only model scores 0.860 through it. Re-audited on 2026-11-27: nothing to decide. The BI-RADS assessment, which carries the signal (without it LightGBM falls to 0.574), is read at the exam before the biopsy that defines the label, and is not the criterion itself (assessments 1 and 2 hold 27 cancers); `CaTypeO` is dropped. Exact feature profiles shared across the split give a target lookup nothing (+0.0005, SE 0.0007). Text fixes need no decision: the bullet calling the assessment categorical predates the ordinal coding of 2026-10-31; the decision table shows assessment 0 as empty, though that group holds 185 of the 239 cancers; and the models beat the assessment alone by 0.006 to 0.013, not "about 0.015". Not tested: the file holds 40,000 exams of 36,714 women, 3,133 of them with two to four exams, so under random folds one woman's exams can fall on both sides of a split; a check grouped by woman was not run. Earlier: `ForcedIIDFromTemporal` stays (issue 1, A, 2026-11-18). Nothing is left open.

**Issues for Andrej:**

1. **Keep `ForcedIIDFromTemporal`, or tag `AssumedStationaryRelation`?**

   * **Problem:**
     - Time: Lost: BCSC Digital Mammography Dataset, exams January 2005 to December 2008, no exam date in the file; film/digital is a stratified 20k/20k draw, not a time proxy.
     - Use: A screening programme estimates 1-year cancer risk after a read, years after 2005-08.
     - Mechanism: The radiologist's BI-RADS assessment carries most signal (ROC AUC 0.914 alone); it depends on imaging technology and reading practice, both of which changed (digital, tomosynthesis, BI-RADS 5th ed. 2013).
   * **Background:** similar datasets[^asr].

     | Similar dataset or source | What was measured | Verdict | Why similar |
     |---|---|---|---|
     | Lehman CD et al., 'National performance benchmarks for modern screening digital mammography: update from the BCSC', Radiology 2017;283:49-58 | recall, sensitivity, cancer detection 2007-2013 vs film-era benchmarks | not flat: recall and detection moved with digital mammography | same consortium and task |
     | BI-RADS Atlas 5th ed. (ACR, 2013) (literature, cited from memory: check) | redefined density categories | changed coding | breast density is a feature |

   * **For a stationary use case:**
     - four years of a large registry.
     - a fixed one-year label window.
   * **Against:**
     - imaging technology changed (film share falls, DBT after 2011)
     - BI-RADS density coding changed in 2013.
     - recall practice moves the assessment-to-cancer relation.
     - use is years after 2008.
   * **Earlier views:**
     - CC 2026-11-17 (Andrej): random 3x3 ForcedIIDFromTemporal checked by blind walk.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep `ForcedIIDFromTemporal` (implemented) | The folds stay; the Time basis line names the reasoning below | Claims only what is known | The split stands for later samples only as far as the use case is stationary |
     | B | `AssumedStationaryRelation` | The folds stay; you give the reason (eight words or more) | Documents why random folds stand for later samples | imaging technology changed (film share falls, DBT after 2011); BI-RADS density coding changed in 2013 |

   * **Recommendation:** A, the main feature is a reading that technology and BI-RADS coding changed; changed coding is a fact against. Confidence: high. **Decision:** A or B?

   [^asr]: **SPLIT-32** (Should; amended 2026-11-18, Andrej): "where it holds none, the review reasons whether the use case can be taken as stationary, from the domain's mechanism and from similar datasets ..., where the AI offers `AssumedStationaryRelation` with a recommendation for a person to decide." `AssumedStationaryRelation` keeps the forced split's folds and replaces only the tag; its line opens `AssumedStationaryRelation (<person>, <date>): <reason>`.

   **Andrej (2026-11-18, ok):** as implemented.

   **Resolved (2026-11-18, Andrej):** A, as implemented: the forced tag stays; the `Time basis:` line gives the reasoning (The main feature is a reading that technology and BI-RADS coding changed; changed coding is a fact against.)

## Reference

Other
