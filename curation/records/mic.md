---
unique_name: mic
name: MIC
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: 'Yes'
tags:
- 'Samples: Over Time'
- 'Time: Lost'
- 'Target: Varying Delay'
- Clinical Study
original_source: Other
year: '2020'
collection_period: 1992-1995
required_split:
- Random (IID)
source_links:
- https://www.openml.org/search?type=data&id=45648
- https://doi.org/10.24432/C53P5M
notebook_path: datasets/beyond_iid/old_iid/mic/mic.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/mic/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

CC (2026-09-30, Lennart): **Leak fixed: predict at admission, dropping the 9 ICU day-1..3 columns.** The dataset description (Golovenkin et al., Leicester data 2020, doi 10.25392/leicester.data.12045261.v3, "Problems to solve") defines four prediction times; at admission all inputs except columns 93-95 and 100-105 (R_AB_1..3_n, NA_R_1..3_n, NOT_NA_1..3_n) may be used, at the end of day 3 all of them. The notebook used day 3, but LET_IS ("Lethal outcome (cause)", column 124) counts any in-hospital death, so a patient who died before day 2 or 3 has no records for those days: 126 of the 138 rows missing a day-3 field died (91%, base rate 16%); 74 of the 110 cardiogenic-shock deaths miss day-2 and day-3 fields, against 10 of 1,428 survivors. Golovenkin et al. 2020 (GigaScience 9:giaa128) list these variables as "in the ICU in the second/third day of the hospital period" (Table 1) and refer to the Leicester description for the task. Dropping them: death AUC 0.93 -> 0.91 (leak audit 2026-09-24). ZSN_A (chronic heart failure, anamnesis) is missing for 54 rows, 93% of them deaths (flag AUC 0.59): an admission-time field, kept.

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Myocardial infarction complications Database - Almost no description or source info on OpenML. Likely from: https://scholar.google.de/citations?view_op=view_citation&hl=de&user=Gms_lDcAAAAJ&citation_for_view=Gms_lDcAAAAJ:olpn-zPbct0C;

Seems to be a preprocessed version from 10.24432/C53P5M UCI
Contains EEG data? Several outputs

Hospital mortality prediction at different time points with details which (time-invariant) features are allowed. Relevant task.

Potential issue: EEG data?

Lennart: Maybe a valid predictive task but might contain non-tabular source data

Andrej: use UCI versionNeeds some preprocessing and is rather small, but otherwise is a good dataset.

CC (2026-10-12, Lennart): Kept in TabArena v0.2 after the task-probe review (flag `few_minority`, multiclass). Thromboembolism (lethal outcome 5) has 12 rows, 4 in every test fold of about 567. They are 0.7% of the test rows and 4.8% of a random forest's log loss (0.58 against 0.71 for the class shares). Too Small is for a task whose scored units are a handful; one rare class of the source's own labels that does not decide the score is part of the task.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback log_loss — The deposit lists prediction problems and time points but no evaluation metric; the GigaScience paper studies trajectories, not prediction scores.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): 11 ordinal scales typed as ordered categories in the codebook's order (CLEAN-14, amended): `INF_ANAM`, `STENOK_AN`, `FK_STENOK`, `IBS_POST`, `GB`, `DLIT_AG`, `ant_im`, `lat_im`, `inf_im`, `post_im`, `TIME_B_S` (the README lists their levels); left unordered: `ZSN_A` (a partial order).

CC (2026-11-01, Lennart): marks on the review board of PR #37: ZSN_A stays unordered as a partial order (two lines of severity), noted in the definition.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `gusto_i_mi_mortality` (TBD -> Yes, priority 3). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-01, Lennart): the decode rule (a code whose codebook says in words what each level is carries the words; a score without them is a number): 11 coded columns carry their words; 2 scores are numbers (FK_STENOK, GB).

CC (2026-11-01, Lennart): the target rule (CLEAN-25) and the cut-end rule (CLEAN-14): counts with a cut end are numbers: INF_ANAM.

CC (2026-11-01, Lennart): counts with a cut end stay ordered categories of the source's levels, the cut end a level of its own (CLEAN-14): the lossless form, chosen from the context rather than by model runs; the same day's numbers with censoring flags are reverted.

CC (2026-11-17, Andrej): the declared split (random, 10x3 folds, `ForcedIIDFromTemporal`) is checked: the split decision tree, walked without the current split, reaches the split it ships (blind split review, cross-dataset item).

CC (2026-11-18, Andrej): the forced tag stays (Review issue 1, A; stationarity reasoning, SPLIT-32 as amended today): no reason to take later samples as interchangeable. Care drifts measurably within the file and has changed since; both are facts against.

## Review

**Outcome:** added. Stationarity reasoning of 2026-11-18: the definition reaches the forced step with no time to measure; decided below.

**Main points:** Keep `ForcedIIDFromTemporal`, or tag `AssumedStationaryRelation`?

**Issues for Andrej:**

1. **Keep `ForcedIIDFromTemporal`, or tag `AssumedStationaryRelation`?**

   * **Problem:**
     - Time: Lost: Krasnoyarsk 1992-1995, no admission date, file sorted by outcome; order within each block shows drift but the blocks share no calendar.
     - Use: Cardiologists estimate lethal complications at admission for later MI patients, 30 years after.
     - Mechanism: Admission ECG, history and labs to in-hospital death and its cause; mortality given them depends on reperfusion care, which changed (primary PCI) and already drifted inside the file.
   * **Background:** similar datasets[^asr].

     | Similar dataset or source | What was measured | Verdict | Why similar |
     |---|---|---|---|
     | mic's own within-block order | Trental 15%->35% in ICU; first vs second half AUC 0.82/0.58/0.72; last fifth of each block vs random fifth | not flat: death ROC AUC 0.77 vs 0.84 (SD 0.02) | same data |
     | 2_month_survival_rate_prediction (SUPPORT) | v3 stationary-relation test, phase I 1989-91 -> phase II 1992-94, death ROC AUC forward vs contemporaneous | flat (LightGBM gap 0.0008, TabPFN gap 0.0027) | clinical prognosis of hospitalised patients from admission physiology, one 3-year step |
     | Rogers WJ et al., 'Trends in presenting characteristics and hospital mortality among patients with STEMI and NSTEMI in the NRMI, 1990 to 2006', Am Heart J 2008;156:1026-1034 | in-hospital MI mortality 1990-2006 | not flat: mortality fell with reperfusion | same outcome and era |

   * **For a stationary use case:**
     - SUPPORT's admission prognosis was flat over a 3-year step.
   * **Against:**
     - structure in the file order: drift in care and a 0.07 ROC AUC cost on each block's last fifth.
     - changed treatments (PCI, drugs) since the 1990s.
     - 30-year span.
   * **Earlier views:**
     - CC 2026-11-17 (Andrej): random 10x3 checked by blind walk.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep `ForcedIIDFromTemporal` (implemented) | The folds stay; the Time basis line names the reasoning below | Claims only what is known | The split stands for later samples only as far as the use case is stationary |
     | B | `AssumedStationaryRelation` | The folds stay; you give the reason (eight words or more) | Documents why random folds stand for later samples | structure in the file order: drift in care and a 0.07 ROC AUC cost on each block's last fifth; changed treatments (PCI, drugs) since the 1990s |

   * **Recommendation:** A, care drifts measurably within the file and has changed since; both are facts against. Confidence: high. **Decision:** A or B?

   [^asr]: **SPLIT-32** (Should; amended 2026-11-18, Andrej): "where it holds none, the review reasons whether the use case can be taken as stationary, from the domain's mechanism and from similar datasets ..., where the AI offers `AssumedStationaryRelation` with a recommendation for a person to decide." `AssumedStationaryRelation` keeps the forced split's folds and replaces only the tag; its line opens `AssumedStationaryRelation (<person>, <date>): <reason>`.

   **Andrej (2026-11-18, ok):** as implemented.

   **Resolved (2026-11-18, Andrej):** A, as implemented: the forced tag stays; the `Time basis:` line gives the reasoning (Care drifts measurably within the file and has changed since; both are facts against.)

## Reference

Trajectories, bifurcations, and pseudo-time in large clinical datasets: applications to myocardial infarction and diabetes data
By S. E. Golovenkin, Jonathan Bac, A. Chervov, E. M. Mirkes, Y. Orlova, E. Barillot, A. Gorban, A. Zinovyev. 2020

Published in GigaScience
