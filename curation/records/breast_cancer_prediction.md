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

CC (2026-11-27, Andrej): the task as defined is not a forecast but the radiologist's own read, and the source is a teaching set (Review issue 2 open).
- Source: the BCSC Digital Mammography Dataset is "recommended for use as a teaching tool only; they should not be used to conduct primary research" (BCSC page), for "teaching data analysis, epidemiological study design, or statistical methods for binary outcomes or correlated data". It is a random sample of 20,000 film and 20,000 digital screening mammograms (2005-2008), with cancers found by linking to cancer registries, which "are used in assessing mammography accuracy".
- No prediction task from the source: overview and codebook pose none. The "source's own question" in `dataset.py` is question 4 of a linked example exam ("Construct a model to predict occurrence of any cancer using patient characteristics and mammography assessment"); the exam's main questions compare the sensitivity, specificity and PPV (share of positive reads that are cancer) of digital and film reads. The task came in through TabSTAR (OpenML 43687), which also keeps the cancer type, a copy of the label.
- The read is the follow-up decision, not a prediction of it: BI-RADS (the radiologist's 0-5 category for the mammogram) 0 means more imaging, 4-5 a biopsy, 1-2 routine screening. Cancers are found through that work-up: women read 0, 4 or 5 (8% of women) hold 87% of the cancers; women read 1-2 can only show up later as interval cancers (found between screens).
- So the score measures the read's accuracy, which the dataset was made to teach: ROC AUC 0.914 for the read alone, 0.93 for the models. Without the radiologist's readings logistic regression reaches 0.58; the BCSC's published risk model at the screening visit, before the read, reaches a c statistic (ROC AUC) of 0.62-0.63 (Barlow WE, White E, Ballard-Barbash R, Vacek PM, Titus-Ernstoff L, Carney PA, Tice JA, Buist DSM, Geller BM, Rosenberg R, Yankaskas BC, Kerlikowske K. Prospective breast cancer risk prediction model for women undergoing screening mammography. J Natl Cancer Inst. 2006;98(17):1204-1214. doi:10.1093/jnci/djj331).
- Lennart's 2026-10-15 argument for the readings cites the BCSC Risk Calculator, which takes the density reading, not the assessment.

## Review

**Outcome:** added; recommended `No` (`No Good Target / Scientific Discovery`): the main feature is the radiologist's follow-up decision, the label is found through that decision, and the source is a teaching set; the risk task before the read goes to `bcsc_risk_estimation` (issue 2). Stationarity reasoning of 2026-11-18: the definition reaches the forced step with no time to measure; decided below (issue 1, A, 2026-11-18).

**Main points:** Retire it for `bcsc_risk_estimation`, or keep one of the tasks this file can still carry (issue 2)? The read alone gives ROC AUC 0.903-0.914 and the models 0.93; before the read the file gives 0.61, beside the BCSC's published 0.62-0.63. Blind task gamer (2026-11-27): nothing gamed beyond the read; its missing value is BI-RADS 0, a recall, set missing by `_clean`. Text fixes that need no decision: the bullet calling the assessment categorical predates the ordinal coding of 2026-10-31; the decision table shows assessment 0 as empty, though that group holds 185 of the 239 cancers; the models beat the assessment alone by 0.006 to 0.013, not "about 0.015". Earlier: `ForcedIIDFromTemporal` stays (issue 1, A, 2026-11-18).

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

2. **Retire the dataset, or keep one of the tasks this file can carry?**

   * **Problem:**
     - The main feature, the BI-RADS assessment (the radiologist's 0-5 category for the mammogram), is the follow-up decision itself: 0 sends a woman to more imaging, 4-5 to a biopsy, 1-2 back to routine screening.
     - The label is found through that decision: women read 0, 4 or 5 (8%) hold 87% of the cancers, so the score (ROC AUC 0.93) measures how accurate the read is.
     - The source is a teaching set ("recommended for use as a teaching tool only; they should not be used to conduct primary research") with no prediction task of its own.
   * **Background:** the BCSC's published risk model at the screening visit, before the read, reaches a c statistic (ROC AUC) of 0.62-0.63 on 2.4M exams[^barlow]; its data are the BCSC Risk Estimation Dataset, `bcsc_risk_estimation`, now being added (no teaching-only clause; citing Barlow 2006 is required).
   * **Experiments:** one exam per woman (first in file order, 246 cancers), 3x3 stratified folds, regularised logistic regression (LR) and LightGBM, ROC AUC:

     | Task | Rows | Cancers | LR | LightGBM |
     |---|---|---|---|---|
     | as implemented (all features) | 36,714 | 246 | 0.915 | 0.927 |
     | the assessment alone | 36,714 | 246 | 0.903 | 0.908 |
     | before the read: no assessment, density kept | 36,714 | 246 | 0.606 | 0.563 |
     | recalled women only (read 0), before the work-up | 2,858 | 188 | 0.569 | 0.542 |
     | negative or benign reads only (1-2): interval cancers | 33,670 | 31 | 0.650 (sd 0.068) | 0.697 (sd 0.067) |

   * **Effect on the task:** every variant without the assessment is a weak task; the interval-cancer one has about 10 cancers per test fold.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Retire, `No Good Target / Scientific Discovery` | `No (Retired)`; the risk task before the read is taken by `bcsc_risk_estimation` | No task built on the decision it would support; no use against the source's teaching-only terms; the risk task on the source made for it (2.4M exams, the published model) | Loses a v0.2 dataset; the marker is a judgment (no precedent of a label found through a feature's decision) |
     | B | Risk before the read | Drop `birads_assessment`; keep density, as the BCSC risk model does; use case: tailor screening at the visit | A real decision (who gets extra screening); keeps the slot | ROC AUC 0.56-0.61; a smaller copy of `bcsc_risk_estimation` with fewer risk factors; still a teaching set |
     | C | Recalled women only | Keep rows read 0; predict which work-ups find cancer | The read's decision is fixed, so it is not a feature | Every recalled woman is worked up anyway, so no decision changes; ROC AUC 0.54-0.57; 2,858 rows |
     | D | Interval cancers | Keep rows read 1-2; predict a cancer missed by the read | A real question (supplemental screening after a negative read) | 31 cancers, about 10 per test fold: too few to rank methods |
     | E | Keep (implemented) | The read stays a feature; the use case is restated as the read's accuracy | No change | The task is the radiologist's decision and its consequence; the score is the read's accuracy, which the dataset was made to teach |

   * **Recommendation:** A, the task needs the decision as a feature, and the risk task before it is better served by `bcsc_risk_estimation`. Confidence: high for not keeping E, medium for the marker. **Decision:** A, B, C, D or E? For A, the marker?

   **Notes for the AI:** A: record `suggestion: No (Retired)`, the marker in the record tags as on other retired records, folder removed as for audiology_diagnosis, CHANGELOG entry. B: drop `birads_assessment` in `_clean`, rewrite `task_summary` and `curation_comments`, rerun `dataset check` and the task probes (TP-2, shuffled labels).

   [^barlow]: Barlow WE, White E, Ballard-Barbash R, Vacek PM, Titus-Ernstoff L, Carney PA, Tice JA, Buist DSM, Geller BM, Rosenberg R, Yankaskas BC, Kerlikowske K. Prospective breast cancer risk prediction model for women undergoing screening mammography. J Natl Cancer Inst. 2006;98(17):1204-1214. doi:10.1093/jnci/djj331.

## Reference

Other
