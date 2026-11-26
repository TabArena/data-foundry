---
unique_name: pheochromocytoma_paraganglioma_metastasis
name: Metastatic pheochromocytoma and paraganglioma (Pamporaki et al. 2023, Zenodo 7749613)
checked_by:
- Andrej
data_foundry_status:
- WIP (DF)
claimed_by: Andrej
suggestion: 'Yes'
priority: 3
decision_markers:
- Class-dependent Recording
tags:
- Clinical Study
- 'Samples: Over Time'
- 'Time: Lost'
- 'Target: Varying Delay'
original_source: Other
year: '2023'
collection_period: Unknown
domain: medical & healthcare
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.5281/zenodo.7749613
- https://www.nature.com/articles/s41467-024-45879-8
- https://doi.org/10.1186/s12911-026-03654-3
- https://doi.org/10.1016/S2589-7500(23)00094-8
v2_path: datasets/_dev/tabarena-v0pt2/pheochromocytoma_paraganglioma_metastasis/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

**AI summary:**

**Screening (AI, 2026-11-25):** `TBD -> Yes`, priority 3: real, documented cohorts of pheochromocytoma and paraganglioma patients (Pamporaki et al. 2023, Lancet Digit Health; Zenodo, CC BY 4.0), 788 patients, nine preoperative clinical and biochemical features plus SDHB status, target metastatic disease; a small but clean clinical task with a stated preoperative use case and two cohorts.
- Source: Pamporaki, Berends, Filippatos, Prodanov, Meuter, Prejbisz et al., "Prediction of metastatic pheochromocytoma and paraganglioma: a machine learning modelling study using data from a cross-sectional cohort", Lancet Digit Health 5:e551-e559 (2023), doi 10.1016/S2589-7500(23)00094-8 (read from PMC10565306); data: Zenodo 10.5281/zenodo.7749613, `DataZonodo.xlsx`, published 2023-03-19, CC BY 4.0 ("The data generated in this study are available in the online platform (zenodo...)", Data availability). As published (previewed): one sheet, 788 patients x 40 columns: `Patient ID`, `Internal Testing (IT)/External Validatio (EV)` (493 IT, 295 EV), sex, age at diagnosis of first tumour, `Predictions for metastatic disease` (EV only: the prospective methoxytyramine call, values NO / YES-possible / YES-moderate / YES-strong / "false negative"), plasma normetanephrine, metanephrine and methoxytyramine, previous history of PPGL, adrenal or extra-adrenal location, `Presence of SDHB` (NO 596, YES 112, "not tested" 80), tumour category (single, bilateral, multifocal), spherical tumour volume, target `Metastatic YES/NO` (IT 166 of 493, EV 57 of 295), then 24 columns of the 12 specialists' risk calls without and with SDHB. Contrary to the data scout's note, the external validation cohort (295 PMT patients) is in the file: "The best candidate ML models were then externally validated using the dataset of 295 patients with PPGL who were enrolled in the PMT-trial ... These included the 267 patients with positive test results and another 28 with negative test results" (Methods).
- Use case: "these models allow for predictions at first diagnosis of PPGL by utilizing clinical features routinely and preoperatively available"; "identifying patients with low probabilities of metastases, who may then be excluded from intensive, long-term and costly follow-up programs, our ML models provide justification for preoperative functional imaging and extensive follow-up in patients with high probability of metastases" (Discussion). Actor: an endocrinologist at first diagnosis, deciding functional imaging and follow-up intensity; fit direct. Collection: patients enrolled over years in the NIH protocol 00-CH-0093, the PRESCRIPT trial and the prospective PMT trial (Germany, Poland, the Netherlands), no date per row (`Samples: Over Time`, `Time: Lost`); metastases are "the presence of metastases in tissues distant from the primary tumor" found at diagnosis or during follow-up of varying length (`Target: Varying Delay`; "The shorter duration of follow-up among patients without compared to those with metastases in the prospective PMT cohort"); type Clinical Study.
- Split: leaf [L-PLACE.random] (Random · `ForcedIIDFromGrouped`, the transfer untested) because [CLI.meets] the source's use is at other centres (it trains on NIH and PRESCRIPT patients and validates on the PMT cohort), [PLACE.several] the release holds two cohorts (the IT/EV column), short of the enough-groups check, with no centre or country column, [PLACE.units] one row per patient. Open: whether to ship the source's IT-to-EV split as a recorded departure (Arasteh kept it; Shaktah drew a random split); prevalence differs by cohort (34% against 19%).
- Siblings and duplicates: none among `curation/records/` (grep pheochromocytoma, paraganglioma, Pamporaki, methoxytyramine). Arasteh et al. 2024 used the same file with "the same (training and test) dataset distribution as the original study" (Results, "Metastatic disease"), 493 and 295 patients; Shaktah et al. 2026 read a CSV of the sheet, dropped only `Predictions for metastatic disease`, the target text and the ID, and split at random (`TabPFN_MetDis_CPU.py`, `KeepSplit = False`), and its script drops neither the IT/EV flag nor the 24 specialist-prediction columns (whether a shared helper does was not checked). Both are copies (PROV-4, PROV-8): /add-dataset starts from the Zenodo file. External collections: Arasteh et al. 2024; Shaktah et al. 2026.
- Better data: none found (data scout, 2026-11-25: Zenodo, figshare, the TU Dresden research portal, the web). Later work is imaging-based (CT radiomics, Insights Imaging 2025) or molecular (figshare 25792479, 79 SDHB patients, multi-omic), not the same task.
- Papers and pages: Pamporaki et al. 2023 (ensemble tree classifier AUC 0.942 on the external cohort against 0.815 for the best specialist); Arasteh et al. 2024 (GBM 0.949, re-implemented AdaBoost 0.951); Shaktah et al. 2026 (CatBoost 0.934, LR 0.928, TabPFN 0.918).
- Metric: the paper reports AUC, MCC and balanced accuracy ("The best performing ENS model, which had an AUC of 0.942 ..., an MCC of 0.851 and a balanced accuracy of 88%", Results) and chose the final model on "the best MCC and balanced accuracy metrics" (Discussion), threshold metrics at no threshold fixed by a decision: several reported, so the fallback `roc_auc` (MET-5, MET-6); inputs none.
- Risks for /add-dataset: drop `Predictions for metastatic disease` (EV only; its "false negative" value is written with hindsight) and the 24 specialist columns (LEAK-10; they are the paper's comparators); `Presence of SDHB` is "often not available at initial diagnosis" (Discussion) and "not tested" for 80 patients: keep as the paper's ten-feature variant or drop for the nine-feature one, a USE-3 call; `Previous history of PPGLs` marks recurrent patients, more common in the training cohort; outcome ascertainment shorter in the prospective cohort (label noise towards "no"); size 788 (TP-5 is fine at 223 positives).
- Priority: gap 0 (medical, binary), use case + (named actor and decision, direct), source + (Lancet Digit Health, CC BY deposit), shape 0 (788 patients, 10 features), no risk point (the leaky columns are named and droppable).

Candidate from Shaktah et al. 2026, "Established machine learning matches tabular foundation models in clinical predictions", BMC Med Inform Decis Mak 26:364 (https://doi.org/10.1186/s12911-026-03654-3), one of its twelve binary clinical tasks.

CC (2026-11-25, Andrej): accepted for adding in the screening review (issues 1 A (SDHB kept, "not tested" its own value) and 2 A (repeated 3-fold CV on all 788 patients)).

**Assessment (AI, 2026-11-25):** `Class-dependent Recording`: 14 patients, all metastatic and all in the earlier cohorts, carry plasma values with decimals (methoxytyramine 8.35 and 16.70 pg/mL, 0.05 and 0.1 nmol/L converted); every other value is a whole number. The format alone scores ROC AUC 0.531; the definition rounds the three plasma values to whole pg/mL, which leaves the models unchanged (random forest 0.9445 either way). Tumour volume is missing for 29 of 223 metastatic patients against 7 of 565 others (indicator alone 0.559), kept as published: median-filling moves no model by more than 0.001. Correction to the screening: the paper's best model (ENS, AUC 0.942) does not use SDHB status; the ENS model with it scores 0.940 (Results).

**Assessment (AI, 2026-11-25):** review panel (full): ship after changes, made (fit approximate, ROC AUC declared as the paper's metric, cohort a provenance column, three notes reworded, paired risk-count comparison: models ahead on 30 of 30 splits by +0.033 to +0.044); disputed: none; for the curator: issue 3 (USE-3, USE-11: the 221 patients with an earlier tumour). Priority 3: gap 0, use case + (named actor and decision, approximate fit), source + (paper and CC BY deposit), shape 0 (788 patients, 10 features), risk 0 (no leak; the open recurrent-patient question).

## Review

**Outcome:** added. 788 patients of Pamporaki et al. 2023 (Zenodo 7749613), metastatic disease (223, 28%) from ten preoperative features, repeated 3-fold cross-validation on random patients as decided (issues 1 and 2). Valid: no leak found, and no exploit beats adding a column of random numbers (+0.002 ROC AUC). Value: trained models beat an untrained count of five risk factors on all 30 splits (ROC AUC 0.945 for a random forest against 0.904). The panel recommends shipping after changes, made except for one question: 221 patients (28%, 156 of the 223 positives) came in with an earlier tumour, not at the first diagnosis the use case still names (issue 3).

**Main points:** Keep the 221 patients with an earlier tumour under reworded framing, or keep only the first-tumour patients (issue 3)?

**Issues for Andrej:**


1. **Keep SDHB status as a feature?**

   * **Problem:**
     - The paper's best model uses ten features with SDHB, but the Discussion calls SDHB "often not available at initial diagnosis", the prediction point of the use case[^use3].
     - 80 of 788 patients are "not tested"; the paper also reports a nine-feature model without it.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep SDHB, with "not tested" as its own value (implemented) | the paper's ten-feature model | the source's main task; "not tested" is what the endocrinologist knows | SDHB known for most patients here, more than at a first visit |
     | B | Drop SDHB | the paper's nine-feature model | holds only what every first visit has | weaker than the source's main model |

   * **Recommendation:** A: the test is ordered at diagnosis in the source's centres, and "not tested" keeps the missing case honest. **Decision:** A or B?

   **Andrej (2026-11-25, ok):** As implemented (A).

   **Resolved (2026-11-25, Andrej):** A: SDHB status stays a feature, with "not tested" as its own value.

   [^use3]: **USE-3** (Must): name the prediction point: when the model is used and what is known then. A value that did not exist at that point is a leak.

2. **Random split, or the source's internal-to-external split?**

   * **Problem:**
     - The release holds two cohorts (493 internal, 295 external, metastatic 34% and 19%) and no centre column, so the split tree reaches a forced random leaf[^split36].
     - Arasteh's 2024 benchmark kept the source's split, and Shaktah's drew a random one.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Repeated 3-fold cross-validation on all 788 (implemented) | the forced random leaf; the cohort flag is no feature | varied training sides; uses every patient | transfer to a new centre untested |
     | B | The source's split as a recorded departure | train on 493, test on 295 | the source's validation; tests transfer to the prospective cohort | one training side only; 57 test positives |

   * **Recommendation:** A: a single fixed split gives one training side, and two cohorts are too few groups to test transfer. **Decision:** A or B?

   **Andrej (2026-11-25, ok):** As implemented (A).

   **Resolved (2026-11-25, Andrej):** A: repeated 3-fold cross-validation on all 788 patients; the cohort flag is no feature.

   [^split36]: **SPLIT-36** (Should): a definition's split is decided by walking the split decision tree; a forced leaf is for the curator to look at.
   [^source]: Source task before our own: the source's own task and split are tested first and preferred when valid.

3. **Keep the 221 patients who came in with an earlier tumour?**

   * **Problem:**
     - The prediction point is "at first diagnosis, before surgery", but 221 of 788 patients have `previous_ppgl` = Yes (a recurrence or a new tumour), and they hold 156 of the 223 metastatic patients[^use3].
     - For them, age, location and volume describe the first tumour while the plasma values come from the later presentation, so one row mixes two moments.
     - Whether their metastases were already known when they entered the study cannot be checked from the release or the paper's main text.
   * **Background:** in the prospective trial, recurrent patients more often have all three plasma values below the reference limits (adrenal 13% against 2% of first-tumour patients, extra-adrenal 52% against 21%), and they are metastatic in 71% of cases against 12%.
   * **Effect on the task:** the score on all patients overstates the score at a true first diagnosis by about 0.05 ROC AUC (higher is better); the first two rows are the task gamer's tuned model on the 30 shipped splits, and the third covers several models.

     | Test rows | ROC AUC |
     |---|---|
     | all patients | 0.938 |
     | first-tumour patients only | 0.886 |
     | trained and tested on first-tumour patients only | 0.87-0.92 |

   * **Consistency:** A follows the source, whose own task includes these patients[^source]; B follows the closest precedent, which keeps only the row at the use case's moment (breast_cancer_prediction, each woman's earliest exam)[^use11].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep all rows and reword the use case (implemented) | rows, the approximate fit and the first-tumour note as now; still to do: `use_case`, `row` and `known` reworded from "at first diagnosis" to "at presentation with a first or a recurrent tumour" | the source's task and all 223 positives; the plasma values are known at that presentation | part of the recurrent positives may have been known at entry |
     | B | Keep only the 567 first-tumour patients | `previous_ppgl` dropped with the rows | the use case as stated; no label possibly known at entry | 67 positives, about 22 per test fold; departs from the source's task |

   * **Recommendation:** A: it keeps the source's task and all 223 positives, and once reworded, every row's features are known at its prediction point; choose B if you hold that these patients typically entered with their metastases already known. The advocate and the critic both land here; the paper's Supplementary Methods or the authors would settle that fact. **Decision:** A or B?

   **Notes for the AI:** On A: reword `use_case`, `row`, `known` and `fit_reason` as option A says; add the distinguishing fact (metastases found by imaging, the plasma values known at the recurrence) to SEL-7's Cases. On B: filter `previous_ppgl == "No"` in `_clean`, drop the column, update the counts in every note, re-run `dataset check` and the task probe on the cluster.

   **Andrej (2026-11-26, discuss):** Can we identify whether the same patients occur multiple times?

   **Answer (AI, 2026-11-26):** one patient is probably entered twice within the earlier cohorts; no patient is found in both cohorts.

   * **Problem:**
     - The release has no patient key, but a patient's sex, age at the first tumour, location, SDHB status, tumour category and first-tumour volume stay the same at every enrolment, so a repeat must match on all six.
     - The 47 cross-cohort pairs the split audit counted match on sex, age, location, SDHB and category only, and every one of them differs in tumour volume.
   * **Experiments:** pairs of rows in the raw file (788 patients; the 36 without a volume left out of the six-field match).

     | Match | Pairs | Across the two cohorts | Same label | Expected by chance |
     |---|---|---|---|---|
     | all six fields exact | 1 | 0 | 1 | 0.13 (age and volume shuffled within sex and location, 200 draws) |
     | five fields, volume left out | 85 | 47 | 64 | not computed |
     | same sex and location, age within 0.1 year, volume within 1% | 0 | 0 | 0 | |

   * **Background:** the one pair (rows 468 and 475 of the earlier cohorts): men aged 54.9, bilateral adrenal tumours of volume 159.5 (no other row has it), no earlier tumour, both not metastatic; their plasma values differ, and row 475's metanephrine equals its normetanephrine (537 and 537), which looks like an entry error.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Keep both rows, with a note (implemented: rows kept, no note yet) | a note naming the pair | no guess about which row is right | one patient may sit on both sides of a fold, with the same label |
     | b | Drop row 475 | one row fewer | no repeated patient; drops the row with the likely entry error | an inference from six matching fields, not a patient key |

   * **Recommendation:** a: one pair of 788 with the same label cannot move a score, and the release cannot confirm it is one person; this does not change issue 3's A or B. **Decision:** a or b?

   [^use3]: **USE-3** (Must): name the prediction point: when the model is used and what is known then. A value that did not exist at that point is a leak.
   [^use11]: **USE-11** (Must): when the use case is the first event of each entity, one row per entity; take one row per entity only when the use case is that row.
   [^source]: Source task before our own: the source's own task and split are tested first and preferred when valid.

**Review panel:** ship after changes (mediator). Claims: 25 tested, 20 hold, 3 refuted and reworded (the metric's origin, the "false negative" reason, one count), 1 untested. Blind review: include with changes; its main concern is the recurrent patients. Task gamer: not gameable, no exploit above noise. Agreed: no leak, the random split (the source's cohort split scores the same, CI about ±0.03), SDHB, the cleaning. Disputed: none left open; the recurrent patients go to you as issue 3.

<details><summary>Mediator</summary>

**Mediator: pheochromocytoma_paraganglioma_metastasis (2026-11-25)**

I read all nine reports, both briefs with their rebuttals, `dataset.py`, the README and the record. I trained no models. I ran one pandas crosstab on the raw sheet (login node, no fits) to settle the one fact still in dispute, and I checked the smallest tumour volumes.

**Recommendation**

```text
Verdict: ship after changes.
Validity: SEL-3 holds; LEAK-10 holds (24 specialist calls, the PMT investigator's prediction and the label-sorted
  Patient ID dropped); LEAK-13 triggered, fixed (plasma rounded to whole pg/mL; the format scored 0.531 before, nothing after);
  USE-3 triggered: "at first diagnosis" is false for the 221 rows with previous_ppgl = Yes (156 of the 223
  positives). Fixed by rewording to "first or recurrent presentation" (A) or by keeping only first-tumour rows (B): the curator decides;
  USE-8 triggered: fit "direct" contradicts the open label horizon the definition names itself. Fixed: fit approximate, in A and B;
  SEL-7 does not apply by its letter (the metastases are found by imaging or histology, not self-reported). The concern
  behind it (positives already known at entry) is open and cannot be measured in the file;
  SPLIT-36 forced leaf L-PLACE.random, settled (issue 2 A), and the measurements confirm it.
Value: TP-4 holds (untrained 5-factor count 0.904 against 0.945; cutoffs to be sourced); TP-5 holds in A and B
  (B: 67 positives, about 22 per test fold); MET-5: roc_auc is the source's metric (model selection by AUC, Methods),
  not a fallback.
Quality: CLEAN-11: the 0.0 volume is unusual, not impossible, so it stays (this overturns the panel's agreed fix);
  three notes refuted or imprecise, reword them; cohort declared as a provenance NonFeature (same container, matches the sibling).
Weighed: source + (Lancet Digit Health, CC BY), size 0 (788), use case + (named actor, decision), headroom + (models
  0.94 against the best specialist's 0.815).
For the curator: issue 1, A or B for the recurrent rows (a question of fact the file cannot answer).
```

**Agreed facts**

All of these were checked by at least two reports and nobody disputes them.

- 788 patients and 223 metastatic (28%). The earlier cohorts have 493 patients (166 metastatic, 34%) and the PMT trial 295 (57, 19%). The Zenodo file matches its md5. The parquet reproduces every marginal of the source.
- The dropped columns are correctly dropped: the 24 specialist calls, `Predictions for metastatic disease` (PMT only, a comparator), `Patient ID` (sorted into exact blocks by cohort and outcome) and `cohort` (the curator's decision).
- No exploitable leak. Every task-gamer attack moved AUC by 0.003 or less. A column of random numbers moves it by +0.0020. A classifier separating train from test rows scores 0.486. There are no duplicate or near-duplicate feature rows. The shipped order is shuffled.
- `previous_ppgl = Yes` means "local recurrence and/or new tumor" (Table 1). It holds for 221 rows: 156 metastatic, 70.6% against 11.8% of the others.
  - The effect holds in both cohorts: 54% against 8% in PMT, 79% against 14.5% in the earlier cohorts.
  - Without the column, models score about 0.89. On first-tumour rows only, they score 0.87-0.92 (E5b, E5c, task gamer 0.886).
- The source split is tested and gives the same scores as random folds: IT to EV scores 0.926-0.947 (95% CI about ±0.03), and random folds score 0.937-0.948. A single split cannot rank the models. Every test fold holds both cohorts.
- SDHB status costs 0.002-0.003 when dropped, inside the noise band. Its "not tested" level (80 patients) does not follow the outcome. Settled (issue 1 A); no new fact.
- The label merges metastases found at diagnosis and during follow-up. Follow-up is shorter for the negatives (PMT 49.3 against 99.7 months), so some "No" labels are censored.
- ROC AUC is the criterion the paper selects models by (Methods). The "final by MCC and balanced accuracy" sentence of the Discussion is contradicted by Table 2.
- The "false negative" value marks the 28 PMT patients with negative biochemistry ("another 28 with negative test results"). It is not a hindsight call.
- 29 of the 36 missing volumes belong to patients with an earlier tumour; 27 of those 29 are metastatic. The note's "27 with an earlier tumour" is wrong.

**Settled by measurement (the one disputed fact)**

**Dispute:**
- **Advocate:** the excess of biochemically negative recurrent PMT patients is explained by tumour type (head-and-neck paragangliomas are often silent), not by when the blood was drawn.
- **Critic:** the plasma values of recurrent patients come from a visit after the first tumour.

**Test:** the share with all three plasma values below the reference limits (NMN < 180, MN < 90, MTY < 18 pg/mL), by cohort, location and `previous_ppgl`.

| Cohort | Location | First tumour: n, biochemically negative, metastatic | Recurrent: n, biochemically negative, metastatic |
|---|---|---|---|
| PMT | adrenal | 179, 2%, 3% | 30, 13%, 63% |
| PMT | extra-adrenal | 42, 21%, 29% | 44, 52%, 48% |
| earlier | adrenal | 264, 6%, 4% | 56, 9%, 66% |
| earlier | extra-adrenal | 82, 18%, 48% | 91, 20%, 87% |

**Result:**
- In PMT, the excess holds within each location (13% against 2%, 52% against 21%). So tumour type does not explain it, and the advocate's competing explanation fails.
- In the earlier cohorts there is hardly any excess.
- What this shows: in the PMT trial, a recurrent patient's plasma values are taken at the recurrence, after the first tumour was treated. That is consistent with a prediction point "at the recurrent presentation", where these values are known. It is not a leak.
- What it does not show: whether the patient's metastases were already known at entry. That question stays open (issue 1).

**Smallest volumes:** 0.0, 0.1, 0.1, 0.1, 0.2, 0.4, … cm³ (one decimal). The 0.0 belongs to an extra-adrenal, non-metastatic PMT patient. It is a tumour under 0.05 cm³ (under about 4.6 mm across), which is unusual but possible and sits on a continuum with the next values. Under CLEAN-11, unusual values stay. The column auditor, advocate and critic agreed to make it missing; I recommend against it, with a one-line note at most.

**Changes to make now (no decision needed)**

1\. **USE-8 (Must), fit.** Set `fit="approximate"`.
   - Rewrite `fit_reason` to name the gaps:
     - (i) the label has no stated horizon: metastases are counted at diagnosis or during follow-up of varying length, and the negatives were followed for less time (PMT 49 against 100 months), so some "No" are not final;
     - (ii) for patients with an earlier tumour, age, location and volume describe the initial tumour, while the plasma values are from the later presentation (measured above for the PMT trial);
     - (iii) transfer to a new centre is untested.
   - Gap (ii) disappears under option B; gap (i) stays in both options.
2\. **MET-5 (Should), metric origin.** Replace `Metric.fallback(...)` with `Metric.source("roc_auc", original="AUC", reference="Pamporaki et al. 2023, Methods: candidate and top models selected according to AUC")`. The score does not change.
3\. **Notes refuted or imprecise (EV-2).** Reword in `curation_comments`:
   - Bullet 2: replace "its value 'false negative' (28 patients, 9 metastatic) was written with hindsight" with "its value 'false negative' marks the 28 PMT patients whose biochemical tests were negative (Methods; 9 metastatic)". The drop stands as a comparator given for one cohort only. Fix the matching comment in `_clean` the same way.
   - Volume bullet: "29 of them with an earlier tumour (27 of the metastatic)".
   - `group_basis` and the cohort note: "0.939-0.947 on the PMT trial" becomes "0.93-0.95 on the PMT trial (95% CI about ±0.03 on 295 patients)".
4\. **TP-4 (Must for any `Trivial` proof), the five-factor note.**
   - Say where each cutoff comes from. MTY 33 pg/mL is 0.2 nmol/L (× 167); give the clinical source if there is one. Volume 33.5 cm³ is a 4 cm sphere; give the size source. Otherwise write "cutoffs chosen by us".
   - Report the gain paired per split on the 30 splits (one cluster run). The verdict cannot move: the gap is about 20 fold SEs.
5\. **Consistency with deafness_gene_carrier_hearing_loss (same leaf, same curator, same day).**
   - Keep `cohort` in `_clean` and declare it `NonFeature("cohort", "provenance", "the study that enrolled the patient: earlier cohorts (IT) or the PMT trial (EV)")` instead of dropping it.
   - Nothing about it enters the container (definitions.md, `non_features`), so the curator's "no feature" decision is unchanged. The README lists it under "Never features", and a later task can hold PMT out.
6\. **CLEAN-11 (Should).** Keep the 0.0 volume (see above). Optionally add "one volume of 0.0 cm³ (under 0.05, extra-adrenal) kept" to the volume bullet.
7\. **LEAK-42 (weak), note only.** Add one sentence to `group_basis`: about 10-18 cross-cohort pairs match on sex, age, SDHB, location and category beyond chance (possible re-enrolled patients, at most about 2% of rows). They cannot be linked without IDs, and the IT-to-EV score shows no effect.
8\. **Record (editor).** The `## Review` Outcome and Main points still read "not added; screened". Update them when the review is written.

Not for this record: `split_tree.md` says no v0.2 definition reaches L-PLACE.random. Three now do (deafness, wild_type_attr, pheo). This goes in the working copy's cross-dataset REVIEW.md.

**Issues for the curator, ranked**

**1. The 221 patients with an earlier tumour: reword the task (A), or keep only first-tumour patients (B)? (P3; USE-3 Must, USE-11 Must; validity)**

**Problem.**
- The use case says "at first diagnosis, before surgery". For 221 rows (28%, holding 70% of the positives) the presentation is a recurrence or a new tumour.
- The headline score comes mostly from those rows: 0.938 on all test rows against 0.886 on first-tumour test rows (same model).
- If some of these patients' metastases were already known at entry, part of the label was known at the prediction point. That is the concern of SEL-7, though not its letter.

**Effect.**
- Under A, the benchmark scores both presentations, and the reworded task is valid per row: the history and the recurrence's plasma values are known at that presentation.
- Under B, it scores the stated use case on a smaller task.

**Best evidence for A** (advocate; the source-before-own practice):
- The source's task and one of its nine features include these patients.
- The recurrence effect holds in the prospective PMT cohort (54% against 8%).
- MTY is lower in recurrent metastatic patients (median 23 against 52 pg/mL), which goes against the values reflecting a known metastatic burden.
- The plasma values are from the recurrent presentation (table above), so they are known at that point.

**Best evidence for B** (critic, column auditor, domain practitioner; USE-11, breast_cancer_prediction):
- B is the use case as stated.
- The practitioner would "image anyway" the recurrent patients, so the decision differs for them.
- Whether their metastases were known at entry cannot be checked: no dates, and the supplement is unread.
- B still scores 0.87-0.92 with about 22 positives per test fold (TP-5 holds).

**What would settle it:** the Supplementary Methods of Pamporaki et al. 2023 (the inclusion rules of the NIH protocol, PRESCRIPT and PMT for patients with recurrent or metastatic disease), or the authors.

**Options.**

| | Option | What changes | Pro | Con |
|---|---|---|---|---|
| A | Keep all 788 | `use_case`, `row`, `known`: "at presentation with a first or a recurrent tumour, before surgery"; a note gives the first-tumour score (about 0.89) | the source's task; all 223 positives | positives already known at entry stay possible and unmeasured |
| B | Keep the 567 first-tumour patients, drop `previous_ppgl` (constant) | rows filter, task summary counts, notes | the stated use case; no doubt about known metastases | 67 positives; departs from the source's task and its published scores |

**Recommendation:** A, unless the curator holds or finds that recurrent patients typically entered with metastases already known; then B. Both sides of the panel give the same recommendation. If A is chosen, record the distinguishing fact in SEL-7's Cases (imaging-found label, not self-reported; whether it was known at entry is unproven) as the first partial-prevalence keep.

**Decision:** A or B?

**Disputed points**

- **Plasma sampling time.** Settled by the table above: in PMT the values are from the recurrent presentation, and tumour type does not explain the excess. Both the critic's "not the first diagnosis" and the advocate's "not a leak" hold. Neither settles issue 1.
- **SEL-7.** Both sides concede it does not apply by its letter. The open concern is issue 1.
- **Follow-up as "note only".** The advocate conceded in rebuttal: USE-8 lists a label with no stated horizon as a gap that makes the fit approximate (differentiated_thyroid_cancer_recurrence). This is change 1.
- **0.0 volume.** The panel agreed to make it missing; the data say otherwise (change 6).
- **Blind reviewer: restore the cohort flag or ship the source split.** Settled by the curator (issue 2 A) and confirmed by the split auditor's numbers. The provenance NonFeature (change 5) is the most the evidence supports.

**Task gamer's exploits, mapped**

The definition has no `Potential leak, kept on purpose:` note and no accepted warnings (`accepted: {}`).

| # | Exploit | Gain measured | Rule | Note in the definition | New or known |
|---|---|---|---|---|---|
| 1 | Cohort recovered by joining to the Zenodo file | +0.0025 untuned, +0.0015 tuned (noise +0.0020) | SPLIT-36 / group basis; curator's cohort decision | cohort note: "the flag gains at most 0.002" | known; size agrees |
| 2 | Ranks, bins and value counts over train and test together | +0.0019 / +0.0009 | LEAK-30 (a participant's transductive transform, not ours) | none | new, within noise; no note needed |
| 3 | Volume-missing indicator | +0.0006 | LEAK-13 (class-dependent recording) | volume bullet: indicator 0.559, median fill moves no model by more than 0.001 | known; size agrees |
| 4 | Keeping `sdhb_variant` | +0.0027 | USE-3 | SDHB bullet, issue 1 A (E8: -0.0016 RF) | known, settled; size agrees |
| 5 | Format-only model (NaN flags) | 0.580 alone, 0 over baseline | LEAK-13 | decimal bullet: 0.531 before rounding; no decimals remain | known; agrees |
| A | Recurrent rows inflate the score (0.938 against 0.886) | -0.05 on first-tumour rows | USE-3, USE-8, USE-11 | `previous_ppgl` note (0.87-0.92 first-tumour) | the size is known; its framing as a prediction-point mismatch is new: issue 1 |
| - | Test labels in the parquet; the public Zenodo file maps 1:1 | total | none (harness; public source) | none | out of scope, as the gamer says |

**Consistency with precedent**

**Followed:**
- the random split on L-PLACE.random (deafness, wild_type_attr, the same day);
- plasma rounding (hepatitis_c_prediction, gallstone_disease, regensburg_pediatric_appendicitis, dementia_prediction);
- comparator columns dropped (2_month_survival_rate_prediction);
- volume kept missing after measuring (LEAK-13);
- TP-4 keep (california_house_prices_2020 side, far from sepsis_survival and ljubljana_breast_cancer).

**Departures now fixed by the changes above:**
- `cohort` dropped while deafness declares `source_file` as provenance (change 5; no distinguishing fact);
- the metric labelled fallback while the source selects by AUC (change 2; MET-5's forest_fires-type case);
- fit direct with an unsettled horizon, against differentiated_thyroid_cancer_recurrence (change 1).

**Open departure:** the recurrent rows against USE-11 (breast_cancer_prediction) and the SEL-7 cases (cdc_diabetes, stroke_prediction). The fact that sets this case apart is the imaging-found label and the source's own inclusion of these patients. Whether the label was known at entry is unproven, so the case goes to the curator as issue 1, not as an exception taken by the AI.

</details>

<details><summary>Claim audit</summary>

**claim-auditor: pheochromocytoma_paraganglioma_metastasis**

Tests: raw file (md5 ba4001d3... matches the definition), the definition loaded through `dataset_io.from_definition`, the builder's `experiments/experiments.json` (model numbers reused, not refit; no model trained on the login node), and the paper (PMC10565306, read twice). Scratch scripts: `panel/claim-auditor_scratch/claim_auditor_*.py`.

**Claims table**

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 1 | 788 patients, 223 metastatic (28%); 493 earlier (34%) + 295 PMT (19%) | task_summary, bullet 4 | crosstab raw | holds | IT 166/493, EV 57/295 | - |
| 2 | Seven tertiary centres in the USA and Europe | task_summary.row | paper | holds (weak) | "seven international tertiary centers"; centres named only in the supplement; NIH (USA) + European affiliations | PROV |
| 3 | Ten features = the paper's nine + SDHB | bullet 1 | paper Methods | holds | nine listed, second analysis "supplemented by presence of SDHB" | USE-3 |
| 4 | "false negative" (28 patients, 9 metastatic) "was written with hindsight" | bullet 2 | raw + paper | **refuted (the reason)** | the 28 are the paper's "another 28 with negative test results" (negative biochemistry; 23 head-and-neck PGL): 24/28 extra-adrenal, median MTY 5.5 vs 15 pg/mL in the other PMT patients, 19/28 non-metastatic. The value names the biochemical test result, not a metastasis call made after the fact. The drop itself stands (comparator, PMT only). | LEAK-10 |
| 5 | Patient ID sorted by cohort and outcome (1-238 EV no, 239-295 EV yes, 296-622 IT no, 623-788 IT yes) | bullet 3 | id ranges | holds | exact blocks, monotone IDs | LEAK |
| 6 | SDHB "not tested" 80 = Table 1 60+17+2+1 | bullet 5 | raw + paper | holds | file 60/17 IT, 2/1 EV; paper same | - |
| 7 | Best ENS AUC 0.942 without SDHB, 0.940 with | bullet 5 | paper | holds | Results quote | - |
| 8 | 14 decimal-plasma rows, all metastatic IT (IDs 626-788); all others whole | bullet 6 | raw | holds | 14 rows, IT/YES only; MTY 8.35 = 0.05 nmol/L x 167 | LEAK (class-dependent recording) |
| 9 | Rounded 8 and 17 occur in both classes (31, 20) | bullet 6 | raw | holds | MTY=8: 24 No/7 Yes; 17: 12/8 | - |
| 10 | Format alone AUC 0.531; rounding leaves RF at 0.9445 | bullet 6 | experiments.json E7 | holds | 0.5314; RF 0.9445 both | - |
| 11 | Volume 0-2,368, fits cm3 (~16.5 cm sphere) | bullet 7 | raw + Table 1 | holds (loosely) | (6x2368/pi)^(1/3) = 16.5; sphere-equivalent diameters from geometric means 3.3/5.4 (IT), 3.5/6.7 (EV) cm vs paper's size 2.7/4.4, 2.8/5.4 cm: same order, ratio ~1.2 | - |
| 12 | Volume missing 36, 29 metastatic (13% vs 1.2%), "27 with an earlier tumour" | bullet 7 | raw | **imprecise** | 29 of the 36 have an earlier tumour; 27 is the count among the 29 metastatic. Other numbers hold. | - |
| 13 | Missing indicator AUC 0.559; median fill moves no model > 0.001 | bullet 7 | recomputed / E6 | holds | 0.5588; RF 0.9445 vs 0.9436, LGBM -0.0007 | - |
| 14 | Missing age 1, MN 6, NMN 1, MTY 1; MTY = 0 for 4 PMT patients | bullet 8 | raw | holds | exact; the four are EV (3 No, 1 Yes) | - |
| 15 | previous_ppgl 221, 156 metastatic (54% PMT, 79% earlier); RF 0.945 -> 0.899 without; first-tumour 567 (67 met) score 0.87-0.92 | bullet 9 | raw + E5 | holds | 40/74, 116/147; E5 0.8992; E5b 0.871-0.920; counts match Table 1 (31/327, 116/166, 34/238, 40/57) | USE-3 |
| 16 | Follow-up geometric means 82.8 vs 95.6, 49.3 vs 99.7 months | bullet 10 | paper Table 1 | holds | exact | - |
| 17 | No duplicate rows; no test row with an exact copy of its features in training | bullet 11 | processed frame | holds | 0 duplicated feature vectors at all | SPLIT |
| 18 | Features tell the cohort with AUC 0.71-0.72; the flag gains at most 0.002; IT->EV 0.939-0.947 ~ random folds on EV 0.943-0.947 | bullet 12, group_basis | E2/E3/E4 | holds | 0.706-0.724; +0.0012 to +0.0020; 0.939/0.943/0.947 vs 0.943-0.947 | SPLIT-36 |
| 19 | Untrained 5-factor count AUC 0.904 vs 0.945 | bullet 13 | recomputed on shipped frame | holds | 0.9041; 33.5 cm3 = 4.0 cm sphere | TP-4 |
| 20 | Repeated 3-fold CV, stratified, all 788 | splits_comment | plan | holds | 10 x 3 folds, disjoint, 74-75 positives per test fold | - |
| 21 | Metric: ROC AUC is computable and means what it meant at the source | metric (MET-2) | dummy scored per fold with the declared scorer | holds | 30/30 folds score 0.5 on a constant; per-row unit, no inputs, 74-75 positives per fold; same target and classes; AUC is prevalence-free, so the pooled 28% vs the paper's 19% EV prevalence does not change its meaning | MET-2 |
| 22 | Metric reason: "candidate models by ROC AUC and the final one by MCC and balanced accuracy (Methods, objective 2; Results)" -> fallback | metric reason, README | paper | **refuted (the reason and the origin)** | Methods: models chosen "according to ... AUC", "with consideration of MCC and balanced accuracy"; 40 of 380 to external validation, top models "selected by comparing their predictive performance according to AUC". Only the Discussion says ENS had "the best MMC and balanced accuracy", and Table 2 contradicts it (TC: MCC 0.863, BA 0.890 vs ENS 0.851, 0.878). AUC is the criterion the paper selects by: under MET-5 a deliberate choice, so `roc_auc` is the source's metric, not a fallback. | MET-5, MET-1 |
| 23 | time_basis ForcedIIDFromTemporal: no date in the file | time_basis | raw columns | holds | no date column among the 40 | - |
| 24 | Record screening: Presence of SDHB NO 596 / YES 112 / not tested 80; prediction values; 40 columns | record Screening | raw | holds | exact | - |
| 25 | Record screening: cohorts from NIH 00-CH-0093, PRESCRIPT, PMT (Germany, Poland, NL) | record Screening | paper main text | untested | the main text does not name them (supplement); not decisive | PROV |

Implied claims: every feature known at the prediction point holds for the ten kept (Table 1 inputs, preoperative); the target is the paper's ("metastases in tissues distant from the primary tumor ... where chromaffin cells are normally absent", matches `predicted`). The prediction-point caveat for `previous_ppgl` (70% of metastatic vs 12% of the others carry it; metastases may predate this presentation) is already written as a note and is not refuted.

**Refuted and untested, ranked**

1\. **Metric origin (claim 22; MET-5, Should).** The value `roc_auc` holds; the origin `fallback` and its reason do not. The paper selects candidate and top models by AUC (Methods), with MCC/BA only "considered"; the "final one by MCC and balanced accuracy" rests on a Discussion sentence that Table 2 contradicts. Changes: the README's Metric block would say the source chose ROC AUC. Mildest remedy: declare it as the paper's metric (`Metric.source`-style origin, reference = Methods, model selection by AUC) or, if fallback is kept, rewrite the reason to "the paper selects models by ROC AUC (Methods), the same as the fallback". No score changes.
2\. **"false negative" written with hindsight (claim 4; LEAK-10 reasoning).** The value marks the 28 PMT patients with negative biochemical tests (paper: "another 28 with negative test results", 23 head-and-neck), not a hindsight metastasis call. Changes nothing in the data (the column goes either way as the investigator's comparator, PMT-only). Remedy: reword bullet 2: "its value 'false negative' marks the 28 patients whose biochemical tests were negative (Methods)".
3\. **"27 with an earlier tumour" (claim 12).** 29 of the 36 missing-volume patients have an earlier tumour; 27 is among the 29 metastatic. Remedy: "29 of them with an earlier tumour (27 of the metastatic)".
4\. **Untested: the centre names in the record's screening (claim 25)** - in the paper's supplement only; no bearing on the task.

Nothing bears against the settled decisions (SDHB kept, random 3-fold CV): the numbers behind both (claims 6, 7, 18) reproduce.

</details>

<details><summary>Column audit</summary>

**Column audit: pheochromocytoma_paraganglioma_metastasis**

Read-only. Light pandas inspection of the raw sheet on the login node, no model fits. Scripts are in `panel/column-auditor_insp*.py`.

**Files.** The Zenodo API for record 7749613 lists one file, `DataZonodo.xlsx` (250,154 bytes, md5 ba4001d3…, which matches the definition), and the workbook has one sheet (`Sheet1`). `_load_raw` reads columns A:N. The 2 empty columns and the 24 specialist columns are left out with reasons. Nothing in the release is missing from the load.

**Dtype probe.** It flagged nothing: 10 columns, no codebook.

**Column table**

| column | meaning (paper, PMC10565306) | known at the prediction point (first diagnosis, before surgery)? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| `sex` | sex, F/M | yes | category, 2 levels | fine | |
| `age_at_first_diagnosis` | "age at initial tumor diagnosis". 1 missing. Geometric means match Table 1 for the external cohort (44.7/40.7); training cohort with metastases 33.6 against the table's 31.8 | yes | float. 15-19% of ages are whole numbers in every cohort/class cell, about what chance gives for one-decimal ages, so no format signal | fine | |
| `plasma_normetanephrine` | plasma free normetanephrine, pg/mL. When the blood was drawn is not stated in the paper; PMT patients "presented with positive biochemical test results at initial screening", plus 28 with negative results | **no for the 221 recurrent patients** (see problem 1); yes for first-tumour patients | float, rounded to whole pg/mL. 7 values had one decimal, all from patients with metastases in the earlier cohorts | rounding fine; timing is a question | USE-3 |
| `plasma_metanephrine` | as above | as above | 13 one-decimal values, all from patients with metastases in the earlier cohorts; rounded. Min 1, 6 missing | as above | USE-3 |
| `plasma_methoxytyramine` | as above | as above | 12 decimal values (8.35, 16.70 = 0.05, 0.1 nmol/L ×167), all from patients with metastases in the earlier cohorts; rounded. 4 zeros in PMT (3 without, 1 with metastases), plausibly below the detection limit | as above | USE-3 |
| `previous_ppgl` | "previous history of PPGL", Table 1 footnote "local recurrence and/or new tumor" | **by definition always "No" at a first diagnosis** | category Yes/No | contradicts the stated prediction point; question for the curator (problem 1) | USE-3 (Must) |
| `primary_tumour_location` | "primary tumor location" (adrenal/extra-adrenal) | yes (imaging) | category | fine | |
| `sdhb_variant` | germline SDHB pathogenic variant ("Testing for germline pathogenic variants … in 708 patients"), not tissue IHC. "not tested" 80 = Table 1's untested count (60+17+2+1) | timing of the test not stated; settled by the curator (issue 1 A) | category, 3 levels | fine (settled) | |
| `tumour_category` | single/bilateral/multifocal, "presence of multifocal disease". The paper does not say whether multifocality includes later (metachronous) tumours | for first-tumour patients probably yes. M is twice as common among recurrent patients (63 against 30), which suggests it accrues over the history | category, nominal (not ordinal), correct | fine; question for the curator in the recurrent rows (part of problem 1) | USE-3 |
| `primary_tumour_volume` | "spherical volume of primary tumor(s)". The paper's Table 1 gives "initial tumor size" in cm | yes in principle (preoperative imaging). Missing for 36; 27 of them recurrent, so the initial tumour's size was not on record | float. The unit fits cm³/mL: the equal-volume sphere diameter has geometric means 3.3/5.5 cm (training) and 3.5/6.7 cm (external) against Table 1's 2.7/4.4 and 2.8/5.4 cm. That ratio (~1.23, ~2× in volume) points to a different volume formula, but a monotone transform is harmless for the models. One value is 0.0 (PMT, no metastases, extra-adrenal), impossible as a tumour volume unless under 0.05 mL | fine; 0.0 is minor (problem 3) | CLEAN (impossible values) |
| `metastatic` (target) | "presence of metastases in tissues distant from the primary tumor", found by imaging or histopathology at diagnosis or follow-up | n/a | category Yes/No | fine. Follow-up length differs by outcome, as the definition already notes | |

Dropped columns, checked: `patient_id` (sorted by cohort and outcome: PMT without metastases 1-238, with 239-295; earlier cohorts without 296-622, with 623-788, so the ID encodes the label; drop correct). `cohort` (curator's decision). `Predictions for metastatic disease` (PMT only; its "false negative" value is hindsight; drop correct). 24 specialist columns (comparators; drop correct).

**Problems, ranked**

**1. `previous_ppgl` and the plasma values of the recurrent patients are not from the stated prediction point (USE-3, Must; question for the curator)**

The decisive fact: at "first diagnosis, before surgery" `previous_ppgl` is "No" by definition. Yet 221 of 788 rows (28%; 156 of them metastatic, 70% of all metastatic) are "Yes". These rows are patients seen at a later presentation, a recurrence or a new tumour.

For those rows the plasma values come from that later visit, not from the first diagnosis:
- All 28 PMT "false negative" patients (the 28 with negative screening tests) have every plasma value below the upper reference limits (NMN 180, MN 90, MTY 18 pg/mL). 19 of the 28 are recurrent, including all 9 with metastases.
- Biochemically negative share in PMT: 6% (13/221) among first-tumour patients, all without metastases, against 36% (27/74) among recurrent patients. In the earlier cohorts: 9% (30/346) against 16% (24/147).
- Values below the reference limits in a patient with a known PPGL are what a measurement taken after an earlier resection, during surveillance, looks like.

Age, location and volume describe the initial tumour, and volume is missing for 27 of the recurrent patients. So a recurrent row mixes data from two dates.

Some recurrent patients may already have had diagnosed metastases when they were enrolled. The file cannot show this: there is no enrollment date and no date of metastasis.

The curation comments already note the column ("one of the paper's nine features and stays"): random forest 0.945 with it, 0.899 without, and 0.87-0.92 on the 567 first-tumour patients. What has not been weighed until now is that the plasma timing also differs, and that the declared `known`/`fit = direct` hold only for the first-tumour rows.

Options:
- **A.** Keep everything as the source did, and reword the prediction point to "at the presentation recorded in the study: the first tumour, or a later recurrence or new tumour". `fit` becomes approximate.
- **B.** Restrict to the 567 first-tumour patients (67 metastatic) and drop `previous_ppgl`, which is then constant. This matches the stated use case, at the cost of fewer positives.
- **C.** Drop only `previous_ppgl`. This does not fix the plasma timing (not recommended).

The source's task includes these rows, so A follows the source. B is the task as our use case states it. This needs the curator.

**2. `tumour_category` in recurrent rows (question, low; folds into 1)**

Multifocal disease is "M" for 63 recurrent patients against 30 first-tumour patients. For recurrent patients it may count tumours that appeared after the first diagnosis. Under option B this question disappears.

**3. `primary_tumour_volume` = 0.0 for one patient (cleaning, low)**

A tumour cannot have volume 0. Either set it to missing or keep it and note it as below 0.05 mL. One row; no effect on scores.

**Checks that found nothing**

- **Plasma rounding.** After rounding, no decimal format remains. The 14 rows with decimals were all from the earlier cohorts and all metastatic, as the definition says. Their values (e.g. NMN 33.7, 55.8) are genuinely low, which fits surveillance measurements and supports problem 1, but this is not a format artefact.
- **No other format signal.** Number of decimals in age and volume does not depend on class beyond chance. Plasma values sitting on an nmol/L conversion grid do not separate the classes.
- **SDHB status.** It is the germline variant, not postoperative tissue staining. "not tested" is 77 of 80 in the earlier cohorts and 62 of 80 without metastases, so there is no outcome-driven gap. The curator has settled this column.
- **Volume unit.** cm³ is consistent with the data. The exact formula differs from Table 1's diameter by about 2× in volume, which is harmless.

</details>

<details><summary>Split audit</summary>

**Split audit: pheochromocytoma_paraganglioma_metastasis**

**Verdict: right, with notes.** The forced leaf L-PLACE.random (10 x 3-fold CV over all 788 patients, stratified on the outcome) is what the tree gives. The source's IT-to-EV split, run with confidence intervals and in both directions, gives the same scores as the random folds. On one 295-patient test side its 95% CI is about ±0.03, wider than any gap between models, so the curator's decision (issue 2 A) holds on the evidence. There is no finding that calls for a re-split.

**Tree walk (SPLIT-36)**

Clinical Study → [CLI.meets] at first diagnosis, at other centres (the source trains on the earlier cohorts and validates on the PMT trial) → Place step → [PLACE.several] no: there is no centre column, and the two cohorts are studies (each one multi-centre), too few groups → [PLACE.units] no: one row per patient → **L-PLACE.random**, `ForcedIIDFromGrouped`.

- This matches `split_leaf`, the `group_basis` and what ships.
- The other answer to [CLI.meets], "later patients at the same clinic", leads to [CLI.dated] no → Order and windows. The only order that can be rebuilt is the cohort order, which gives two periods, so the split is forced IID there too. The `time_basis` `ForcedIIDFromTemporal` line says this, beside the group basis as SPLIT-35 requires.
- The leaf is forced and the curator has decided it. The tree's "No v0.2 definition reaches it yet" under L-PLACE.random will be out of date once this definition (and its kather siblings deafness_gene_carrier_hearing_loss and wild_type_attr_cardiac_amyloidosis) lands. That is a doc note for the main session.

**Evidence (a cluster run)**

Script: (a script in the run folder). Output: `panel/split-auditor_exp.json`. Models: LightGBM, random forest (NaN filled with -1), and logistic regression on log-transformed values. ROC AUC, with the 95% bootstrap CI (2,000 resamples) for the single splits.

| Split | LightGBM | Random forest | Logistic |
|---|---|---|---|
| Shipped 10 x 3 CV (mean ± sd over folds) | 0.937 ± 0.010 | 0.943 ± 0.011 | 0.948 ± 0.009 |
| CV stratified on cohort x outcome | 0.938 | 0.943 | 0.949 |
| Random 493-patient train, mixed cohorts (20 draws) | 0.937 ± 0.013 | 0.941 ± 0.015 | 0.947 ± 0.014 |
| Source: IT (493) → EV (295) | 0.943 [0.912, 0.970] | 0.926 [0.889, 0.958] | 0.947 [0.918, 0.970] |
| Reverse: EV (295) → IT (493) | 0.900 [0.868, 0.928] | 0.940 [0.919, 0.960] | 0.945 [0.922, 0.963] |

- **Transfer.** Transfer across cohorts costs nothing measurable. Every source-split score lies within its CI of the random-fold mean. Training on the 295 PMT patients loses only for LightGBM (0.900), which fits that small training side poorly.
- **Model ranking.** A single fixed split cannot rank the models. Random forest comes last under IT→EV and LightGBM comes last under the random folds, and both gaps are inside one split's CI. This supports option A (SPLIT-15: several varied training sides).
- **Cohort mix in the test folds.** Every shipped test fold holds both cohorts: the EV share is 0.33–0.43 and there are 13–25 EV positives per fold. The positive rate is 0.281–0.285 in every fold. Stratifying on cohort x outcome changes nothing.
- **Row order.** The raw order is sorted by cohort and outcome (time probe: `sorted_by_target`, through the dropped Patient ID). The shipped `data.parquet` is not sorted: there are 306 class runs and positives run from position 3 to 786. No order leak reaches a participant.
- **Group basis figure.** The group basis gives "0.939–0.947 on the PMT trial". With a different NaN handling for the random forest I get 0.926–0.947. The claim stands, but a range of 0.93–0.95 with its CI (about ±0.03 on 295 patients) is the honest wording.

**Notes (none needs a re-split)**

1\. **Possible patients shared across cohorts.** Unverifiable, at most about 2% of rows, no measurable effect (LEAK-42 tests, weak).
   - Pairs from different cohorts with an exact match on sex, age at first diagnosis (0.1 y), SDHB, location and tumour category: 47 EV–IT pairs. Shifting age by ±0.1 to ±0.6 y as a control gives 32–43 (mean 36.5).
   - Matching on sex and age alone gives 133 against 107–121.
   - The excess of about 10–18 pairs could be recurrent patients enrolled again in the PMT trial. Part of it may come from the cohorts recording age differently: 17% of IT ages end in .0 against 8% of EV ages.
   - There are no patient IDs to link them, so SPLIT-24 cannot rebuild the groups. The labels travel only weakly: of the excess pairs, 6 are metastatic in both rows against about 2 by chance.
   - The score does not move: IT→EV and the random folds agree. Remedy: none. At most, add a sentence to the group basis.
2\. **Cohort is a study and era, not a place.** The paper names seven tertiary centres in all but does not say, in the main text, whether centres overlap between the cohorts (Supplemental Methods). The IT→EV test is therefore mostly a test of study, era and enrolment, and only partly of centre. The `group_basis` wording ("the file names no centre, only two cohorts, too few groups") is right. The `split` sentence "transfer to a new centre is not tested" is also right.
3\. **Labels not yet settled at the cut (`Target: Varying Delay`).** Follow-up in the PMT trial is 49 against 100 months, without against with metastases. Some labels of "No" are not final. No split can fix this, and the definition already says so (fit_reason, curation note). Not a split problem.
4\. **No temporal alternative exists.** There is no date per row, and the cohort order gives two periods. `ForcedIIDFromTemporal` is correct.

**Rules cited**

SPLIT-36, SPLIT-35, SPLIT-32, SPLIT-15, SPLIT-24, LEAK-42.

</details>

<details><summary>Domain practitioner</summary>

**Fit: approximate** (the definition declares direct). Target and inputs are the ones used at first diagnosis, but 221 of 788 patients (28%) are not at first diagnosis and hold 156 of the 223 metastatic cases (70%); the headline score mostly reflects those recurrent patients, for whom the decision differs. Plasma sampling time unresolved (supplement not fetchable): untested.

Sources: Pamporaki et al. 2023 main text (PMC10565306; supplement returned a placeholder); the record, dataset.py, builder experiments E5/E5b/E5c/E8; light crosstabs on the clean room; clinical background (Endocrine Society 2014, ESE 2016, WHO 2017/2022) from knowledge, unchecked.

Gaps, ranked:
1. Two prediction points in one table (USE-3, USE-8). previous_ppgl = Yes ("local recurrence and/or new tumor") patients are already under follow-up; guidelines image them anyway; metastases may be known. Recurrent 156/221 metastatic (79% earlier cohorts) vs first-tumour 67/567. Models 0.945 all rows; 0.87-0.92 trained on first-tumour only (E5b); 0.88-0.91 on first-tumour rows trained on all (E5c); untrained risk count 0.904. Size/location of recurrent patients are the initial tumour's; 27 of 36 missing volumes are recurrent metastatic patients. Not a leak claim (disclosed, one of the paper's nine features); fit should be approximate with this named, or the use case "at presentation, first or recurrent".
2. Plasma sampling time (USE-3; open, untested): main text gives none for earlier cohorts (166 of 223 metastatic). If drawn after metastases were known, methoxytyramine would partly measure metastatic burden. Data points the other way: median methoxytyramine 23 pg/mL recurrent metastatic vs 52 first-tumour metastatic. Settle via Supplementary Methods or the authors.
3. Label follow-up window (USE-5): synchronous and metachronous metastases merged; PMT negatives 49 months geometric mean follow-up; some No = not yet. Disclosed; modest.
4. SDHB at the imaging decision (settled A; evidence only): germline result "rarely available preoperatively"; fits follow-up decision better; dropping costs 0.9429 vs 0.9445 (E8).
5. Tertiary referral sample: 28% metastatic, 112/788 SDHB; ranking ok, calibration would not carry over.
6. Missing inputs an expert has: other germline results (RET, VHL, NF1), CT/MRI appearance, family history; histopathology only after surgery (gap, not leak).

Would I use it? Yes for first-tumour patients; would trust more knowing the sampling time and the first-tumour accuracy (~0.90); the 0.94 is inflated by recurrent patients I would image anyway.

Expert changes: record the dual prediction point (fit approximate or a use case naming recurrent presentation); report first-tumour performance; get sampling time. First-tumour-only task (567, 67 positives) is an option, not a recommendation.

Metric: keep roc_auc (no threshold fixed, MET-6/7/8; calibration would not transfer across prevalences 34% vs 19%; MET-9 gives no case for AUPRC).

</details>

<details><summary>Blind review</summary>

**Verdict**

**Include with changes** — this is a real, well-sourced clinical prediction task with genuine, non-trivial signal and good method separation, but the prepared file silently pools the study's derivation and external-validation cohorts, drops the cohort indicator, and carries one predictor (`previous_ppgl`) whose timing relative to the outcome I could not establish.

**What I did**

Read `task.md` and `data.parquet` (788 × 11); downloaded the public source file `DataZonodo.xlsx` from Zenodo 7749613 into an isolated scratch directory and compared it row-for-row with the parquet; read the Lancet Digital Health 2023 source paper (PMC10565306) and the two downstream benchmark papers. I opened no file outside the clean room other than the Zenodo download I made myself.

**Provenance confirmed.** The parquet is the Pamporaki et al. 2023 PPGL dataset, shuffled, with the clinical columns kept and the leaky/auxiliary columns correctly dropped. Marginals match the source exactly: sex 411/377, previous PPGL 567/221, location 529/259, SDHB 596/112/80, tumour category 634/93/61, outcome 565/223, and the missing-value counts 1/1/6/1/36. 774 of 788 rows join exactly to source rows. The source sheet also contains a column `Predictions for metastatic disease` (the model's own output on the validation cohort) and 24 columns of specialist interpretations — **all correctly excluded**. That is the right call and the most important leak was avoided.

---

**Concerns, most to least serious**

**1. `previous_ppgl` — the strongest predictor, with unverified temporal ordering**

It is by far the biggest single driver: alone it reaches CV AUC **0.792**; removing it drops LightGBM from **0.935 → 0.886** (bigger than any other ablation). P(metastatic | previous PPGL = Yes) = **156/221 = 70.6%** vs **67/567 = 11.8%**.

The paper defines it in a Table 1 footnote as "*local recurrence and/or new tumor*", while claiming the model "*allow[s] for predictions at first diagnosis of PPGL by utilizing clinical features routinely and preoperatively available*". Those two statements sit uneasily together: a patient has no prior PPGL at their *first* diagnosis, and `age_at_first_diagnosis` is separately recorded as the age at the initial tumour. So the index moment is not the first diagnosis for 221 patients. Whether the recurrence was recorded *before* metastases were found, or tallied across the whole follow-up, is not stated in the main text. If the latter, part of this feature is post-baseline information about the same disease trajectory as the label.

**What I'd change:** get this settled from the Supplement before shipping, and state the prediction time explicitly in `task.md`. If it cannot be settled, ship the task anyway but document the caveat — the task retains AUC 0.886 without this column, so a `previous_ppgl`-free variant is a viable fallback and still a good benchmark task.

**2. The IID split discards the study's cohort design, and the cohort label was dropped**

The source xlsx has a column `Internal Testing (IT)/External Validatio (EV)`: **493 IT** (NIH + PRESCRIPT, retrospective) and **295 EV** (PMT trial, prospective, Germany/Poland/Netherlands). The parquet drops it. Prevalence differs materially — IT 31.7%, EV 19.3% — and the cohort itself is partly predictable from the features (AUC 0.709), chiefly via `sdhb_variant = "not tested"` (16.1% in IT vs 1.0% in EV) and `tumour_category`. `task.md` describes the regime simply as "IID (random rows)", which is not what the data is.

Two consequences:
- **Comparability is lost.** Every published number on this dataset uses the predefined split: Pamporaki AUROC 0.942, Arasteh et al. (*Nat Commun* 2024) re-implemented AdaBoost 0.951 ± 0.014 and ChatGPT-ADA GBM 0.949 ± 0.015, and Shaktah et al. (*BMC MIDM* 2026 — the TabPFN benchmark) state the four Arasteh datasets were "*used as provided, including predefined splits and engineered features*". A benchmark that reports 10×3 random CV cannot be compared against any of these.
- **A genuinely interesting shift task is thrown away** for a weaker one.

In its favour: I checked, and the shift does *not* make scores dishonest. Training on IT and testing on EV gives **AUC 0.937**, essentially identical to the 10×3 random CV (0.935); EV→IT gives 0.913. So the random split is not an easier task — it is just a *different and unpublishable* one.

**What I'd change:** restore the `cohort` column (IT/EV) and either ship the predefined split as the primary regime, or keep IID CV but carry the column so the published split can be reproduced and so group-wise CV is possible.

**3. The outcome's timing is undefined — prognosis or classification?**

The paper's definition is "*Metastatic disease was defined as the presence of metastases in tissues distant from the primary tumor, where chromaffin cells are normally absent*", ascertained by "*conventional and functional imaging or histopathological examination of resected lymph nodes*". It does not say whether these were synchronous (present at the index work-up) or metachronous (found later). Follow-up was substantially shorter in non-metastatic patients in the validation cohort (geometric mean 49.3 vs 99.7 months), and the authors concede this "*may have impacted the importance of methoxytyramine to predict metastases by underestimating diagnostic sensitivity*" — i.e. some "No" labels are likely censored, not negative.

This matters for what the task *is*. If the metastases were already visible on the staging scan, the model is not predicting anything a clinician would not already know; if metachronous, it is a genuine prognostic task that would justify intensified surveillance. The clinical use case — at the pre-operative work-up of a newly diagnosed PPGL, decide follow-up intensity and surgical extent — is real and decision-relevant either way, but the label's meaning should be stated.

**What I'd change:** state in `task.md` that "No" includes patients with limited follow-up, i.e. the negative class is partly censored.

**4. Informative missingness in `primary_tumour_volume`**

36 rows are missing it, and **29 of 36 (80.6%)** are metastatic, against 25.8% among rows where it is present. A model trained on missing-indicators alone gets AUC 0.559. This is plausibly real-world-available information (unresectable or unlocated primary in advanced disease), not a recording artefact alone — but it is a shortcut that rewards imputation strategies that preserve missingness, and benchmark users will not expect it. Volume is otherwise the second-strongest feature (alone AUC 0.742; median 106.5 cm³ in metastatic vs 20.7 cm³ in non-metastatic).

**What I'd change:** document it in `task.md`. No change to the data.

**5. Prevalence is enriched ~1.5–3× over clinical reality**

223/788 = **28.3%** metastatic, against the paper's own framing of "*up to 20% rate of metastatic disease*" and far above unselected-population estimates; the training cohort comes partly from an NIH tertiary referral protocol. Ranking metrics (AUROC) are unaffected, but prior-sensitive metrics — accuracy, average precision (I measure AP ≈ 0.88–0.90), calibration, any fixed-threshold score — do not transfer to clinical use.

**What I'd change:** nothing in the data; note it in `task.md` and prefer AUROC over AP/accuracy for headline reporting.

**6. `sdhb_variant` is in the file but was deliberately excluded by the authors**

The paper is explicit: the selected model "*did not utilize SDHB variant status as a feature*" and was preferred because it worked "*without requirement for SDHB variant data, which is often not available at initial diagnosis*". Germline testing takes weeks; if the prediction is made pre-operatively, this column may not exist yet. Its `not tested` level is also a cohort fingerprint (see #2). Empirically it barely matters — dropping it moves LightGBM 0.935 → 0.933 — so this is a documentation issue rather than a scoring one.

**What I'd change:** keep it (it is in the public source and hurts nothing) but say in `task.md` that it deviates from the published feature set and may be unavailable at prediction time.

**7. Minor data-fidelity and metadata issues**

- **Rounding:** ~14 metanephrine values were cast to integers somewhere in preparation (source 8.35 → 8, 16.7 → 17, 33.7 → 34, 54.6 → 55, 134.3 → 134). Clinically negligible, but it is an unnecessary loss and it is why 14 rows would not join to the source. Age and volume were preserved exactly.
- **Units are undocumented.** The three metanephrines are pg/mL (source header `Plasma NMN pg/ml` etc.); volume is the source's "*Spherical volume of primary tumor(s)*", i.e. derived from an imaging diameter, in cm³. `task.md` should carry a data dictionary.
- **Edge values:** one tumour volume of 0.0 cm³ and four methoxytyramine values of 0 pg/mL (presumably below the limit of detection) — these are left-censored, not true zeros. 62 patients are under 18, which is correct for SDHB-driven PPGL, not an error.
- **Source links are partly misleading.** The Nature Communications link in `task.md` (s41467-024-45879-8) is Arasteh et al., *"Large language models streamline automated machine learning for clinical studies"* — a paper that *reuses* this dataset, not its source. The clinical source is the Lancet Digital Health link. Worth reordering so the primary source is first.

**Positives worth recording**

- **Real data, right target, plausible values.** Multi-centre human cohort from seven tertiary centres; every marginal reproduces the public source exactly; the predictor–outcome relationships match established PPGL biology (extra-adrenal 58.3% vs adrenal 13.6% metastatic; SDHB+ 79.5%; bilateral disease only 3.3%, as expected for hereditary adrenal syndromes).
- **No duplicates.** Zero exact duplicate rows, zero duplicate feature rows, zero duplicate (age, NMN, MN, MTY) keys.
- **Non-trivial with real headroom and good resolution.** Majority-class accuracy 0.717; best single feature AUC 0.792; full models 0.927–0.949. The best human specialist reached 0.815 and the mean of 12 specialists 0.710 — so this is a task where models genuinely beat experts, not one that is saturated. Despite n=788, the 10×3 paired design separates methods cleanly: logistic-regression-on-logs 0.9487 > RF 0.9436 > LGBM 0.9348 > kNN 0.9272, with paired t of 4.3–10.3. Note that **a well-specified linear model beats the GBDT here** — that is a useful property for a benchmark, not a defect.
- **Sensible preparation.** Types are right (categoricals as `category`, numerics as float), missing values are real NaN rather than sentinel codes, no one-hot mangling, and the specialist-interpretation and model-prediction columns from the source were correctly dropped.
- **Training weight:** `task.md` declares no weight column, so that question does not arise. Given the enriched prevalence, I would *not* add one.

---

**What I could not check**

- **The Supplement** to the Lancet DH paper (Supplemental Methods/Results, Tables 1–9), which the main text says contains the cohort sources, the metastasis-ascertainment detail, the timing of germline genetic testing, and the missing-data handling. Concerns #1 and #3 are only resolvable there.
- **Whether `primary_tumour_volume` is imaging-derived or from the resected specimen.** The source header "Spherical volume of primary tumor(s)" strongly implies a sphere computed from an imaging diameter, consistent with the "preoperatively available" claim, but neither the paper's main text nor the Zenodo record states it.
- **Whether any patient appears in both the IT and EV cohorts.** No patient identifier survives into the parquet, and the source `Patient ID` is a per-row index; the cohorts are nominally distinct protocols, but I could not verify no overlap.
- **The exact cohort label for 14 of 788 rows**, because of the integer rounding in #7 — my IT/EV figures above are 479/295 rather than the true 493/295. This does not change any conclusion.
- **The AUROC that Shaktah et al. 2026 report for this specific task** — the value sits in a figure that could not be read, so I cannot say how the published TabPFN-vs-baselines numbers compare to mine.

</details>

<details><summary>Task gamer</summary>

All attacks are run. Writing up.

---

**Pheochromocytoma/paraganglioma metastasis — exploit report**

**Verdict: this task is essentially not gameable — every artefact I could build (cohort identity recovered from the published file, transductive statistics, missingness, format/precision, row order, duplicate patients) moves AUC by ≤0.003, which is exactly what adding a column of random numbers does; the one real defect is not a leak but the population: 28% of rows are patients presenting with a *recurrent* PPGL, not "at first diagnosis", and they inflate the headline AUC from ~0.886 to ~0.938.**

Honest baseline (untuned LightGBM on `features()`, 30 shipped splits): **0.93537** (sd 0.0098, min 0.9184, max 0.9603).
Better honest model (tuned LGBM + metabolite ratios, `work/final.py`): **0.94101**.
Noise band: refitting with one extra column of random numbers gives 0.93386 / 0.93550 / 0.93633 (untuned) and 0.93879 / 0.93979 / 0.94116 (tuned) — **any gain below ≈0.002 is noise**, and a paired t-test over the 30 splits calls a pure random column "significant" (+0.0020, p=0.012), so paired p-values are worthless here.

**Exploits, ranked by gain**

| # | Exploit | Script | Honest score | Exploited score | Gain (per split, range) | A deployed model has it? | Fix |
|---|---|---|---|---|---|---|---|
| 1 | Cohort flag (retrospective NIH/PRESCRIPT vs prospective PMT) recovered by joining every kit row to the Zenodo file | `work/map2.py`, `work/ex_cohort.py`, `work/stat.py` | 0.93537 / 0.94101 | 0.93791 / 0.94248 | +0.0025 (−0.0047…+0.0099), +0.0015 tuned | No — but gain = random-column noise | None needed; if wanted, ship the cohort column as a feature or split by cohort |
| 2 | Transductive features: percentile rank, 20-quantile bin and exact-value count of each numeric column computed over train+test together | `work/battery.py`, `work/iso.py` | 0.93537 / 0.94101 | 0.93730 / 0.94194 | +0.0019 / +0.0009 | No | None needed |
| 3 | Missing-value pattern (36 rows with no `primary_tumour_volume`, 80.6% metastatic) used as a feature | `work/nanx.py` | 0.93537 | 0.93537 (explicit indicators), 0.93473 (imputed away) | +0.0006 | Arguably not | None needed; redundant with `previous_ppgl` |
| 4 | `sdhb_variant`, which the source authors say "is rarely available preoperatively" | `work/battery.py` | 0.93267 (dropped) | 0.93537 (kept) | +0.0027 | Usually not, at the stated prediction point | Drop the column, or move the prediction point to "after genetic testing" |
| 5 | Format-only model (integer-ness, last decimal digit, multiple-of-10, NaN flags; no values) | `work/battery.py` | 0.5 (chance) | 0.57976 | +0.08 over chance, but 0.0 over baseline | n/a | None needed; all of it is the NaN flags |

Nothing here is worth having. For reference, the published model on this cohort reported AUC 0.942 (Lancet Digit Health 2023), i.e. the honest baseline already sits at the literature ceiling.

**Flaws that distort the task (not exploits a participant switches on)**

| # | What is wrong | The honest choice | Score as shipped | Score under the honest choice | Fix |
|---|---|---|---|---|---|
| A | 221/788 rows (28%) have `previous_ppgl = Yes` — the patient is being worked up for a recurrence, not a first diagnosis as `task.md` states. Their metastasis rate is 70.6% vs 11.8%; one binary column does most of the work | Score only rows at a genuine first diagnosis | 0.93794 (tuned, all test rows) | **0.8860** (same model, `previous_ppgl = No` test rows only); 0.8825 if also trained only on those rows | Either restrict the task to `previous_ppgl = No` rows, or change the prediction point to "at presentation (first or recurrent)" |

I found **no** flaw in the opposite direction: dropping the recurrence rows from *training* does not help (0.8825 vs 0.8860 on the first-diagnosis test rows), no training row is dated after the prediction point (the regime is IID, there is no time column), and nothing in the splits penalises an honest model.

**Mechanisms**

**1 — Cohort.** The kit pools two cohorts with different case mix: the retrospective NIH/Netherlands training cohort (493 rows, 33.7% metastatic) and the prospective PMT cohort (295 rows, 19.3%). Pooling them and splitting IID means test rows come from the same two populations as training, which is easier than the external validation the source paper did. I recovered the cohort label for all 788 rows by matching to `DataZonodo.xlsx` (every row matched 1:1, all distances ≈0 after the kit's rounding of the plasma values to integers) and added it as a feature: 0.93537 → 0.93791. A random column added to the same model gives 0.93737. The cohort is also ~70% predictable from the features themselves (LGBM AUC 0.698), mostly through `sdhb_variant = "not tested"` (77 of 80 such rows are retrospective-cohort), so the model already has most of it. Not worth a fix.

**2 — Transductive statistics.** Ranks/quantile bins and exact-value counts over all rows add +0.0009…+0.0019. The value counts pick up repeated plasma readings (e.g. methoxytyramine = 10 pg/mL occurs 63 times, 35% metastatic, vs 7 pg/mL 52 times, 8%) which look like per-laboratory below-limit substitutions. To test whether those exact values carry a site fingerprint, I jittered every numeric column uniformly within its rounding step: 0.93537 → 0.93539 / 0.93664 / 0.93629. No precision or sentinel leak survives in the kit.

**3 — Missingness.** `primary_tumour_volume` is missing in 36 rows of which 80.6% are metastatic — a referral artefact (the primary was resected elsewhere before enrolment), not something a pre-surgical imaging workup would reproduce. But 80.6% of those same rows also have `previous_ppgl = Yes`, so the information is already there: median-imputing every numeric column, which destroys the pattern entirely, costs 0.0006.

**A — The population.** `task.md` says the prediction is made "at first diagnosis of a pheochromocytoma or paraganglioma, before surgery". For 221 rows this is false: `previous_ppgl = Yes` means the record is a later presentation of a patient already known to have had a PPGL, and `age_at_first_diagnosis` refers to that earlier tumour. Such patients are metastatic in 70.6% of cases, and the pattern holds in both cohorts separately (prospective PMT: 54.1% vs 7.7%; retrospective: 78.9% vs 14.5%), so it is genuine clinical signal available at *their* presentation — it is the task's description of the prediction point that does not fit them. Removing `previous_ppgl` from the feature set costs more than any other column (0.9354 → 0.8884), and scoring the full model only on the rows the task claims to be about drops it from 0.938 to 0.886. That 0.05 is the real headline inflation in this task, and no participant can decline it.

**Attacks that found nothing**

1\. **Row order / ids** (`work/base.py`, inline checks): row index alone AUC 0.531; next-row label agreement 0.611 vs 0.594 expected; positive rate flat across blocks of 50; adding row position to the model: 0.93459 (−0.0008). The kit shuffled the source order (correlation of kit position with source patient ID 0.012), and the cohorts are evenly spread over the file (44–71 prospective rows per block of 100).
2\. **Decimals / last digit / trailing zeros** (`work/battery.py`): all plasma columns are whole numbers, age and volume one decimal everywhere; last-decimal-digit positive rates 0.21–0.36 across 10 digits on ~70 rows each; multiples of 10 have positive rate 0.36 vs 0.27 (n≈80, not distinguishable). Format-only model 0.580, entirely from NaN flags.
3\. **Exact / near copies across the split** (`work/subgroup.py`): no duplicate rows, no duplicate feature rows; smallest standardised nearest-neighbour distance in the whole table 0.023 (no near-copies); 1-NN train-label prediction scores 0.783, far below the model.
4\. **Same patient on both sides** (inline, `work/map.py`): candidate same-patient keys (sex + age at first diagnosis, optionally + SDHB status, since both are fixed per patient) give within-group label agreement 0.606 vs 0.594 chance (loose key) and 0.708 vs a stratified-permutation null of 0.685 ± 0.037, p = 0.295 (strict key). No group leakage.
5\. **Training rows a deployed model would not have** (`work/subgroup.py`): the regime is IID with no time column; there is no label-dependent inclusion rule I can detect, and dropping recurrence rows from training does not help.
6\. **Test-set composition / train-vs-test classifier** (`work/subgroup.py`): LGBM separating a split's test rows from its training rows scores AUC 0.486 — the splits are genuinely random. Each of the 788 rows is a test row in exactly 10 of 30 splits; fold-wise positive rates are 0.2814 / 0.2852 / 0.2824 (stratified); no train/test overlap, full coverage.
7\. **Columns from after the prediction point** (`work/battery.py`, leave-one-out): no column comes close to the full model alone (best single: `primary_tumour_volume` AUC 0.778, `previous_ppgl` 0.71 as a binary); no column only takes a value once the outcome has happened. `tumour_category` and `primary_tumour_volume` come from the pre-surgical imaging the source describes; `sdhb_variant` is the only timing-questionable one (finding 4).
8\. **The weight**: `task.json` has `sample_weight: null`, no time column, no group column — nothing to attack.
9\. **Whole-table transforms** (`work/battery.py`, `work/iso.py`): standardisation, ranks, quantile bins — covered by finding 2, all noise.
10\. **Lookups / shallow formula**: a depth-limited tree is just a weaker model (tuned small-leaf LGBM is the best honest model at 0.941); there is no formula that recovers the target.
11\. **Metric quirks**: `metrics.py` calls `sklearn.metrics.roc_auc_score` on the positive-class column, unweighted, no grouping. Nothing to exploit in ties or class order.

Two trivial total breaks exist and I am not ranking them, per the task's rule: `data.parquet` ships the target for the test rows, so any "prediction" could be the label; and all 788 kit rows map 1:1 onto the published `DataZonodo.xlsx` (I built the mapping in `work/map2.py`), from which the label — and also the 12 specialists' prediction columns the kit dropped — can be read directly.

**What I could not check**

- **Whether the plasma metabolites were measured at the first diagnosis or at a later enrolment visit** for the 221 recurrence patients. If they were measured at the later visit, those 28% of rows contain biochemistry taken *after* the outcome had developed, which would make finding A a genuine leak rather than a population mismatch. The paper's main text does not say; the Supplemental Methods (not in the open-access manuscript I could retrieve) would decide it. The fact that the prospective PMT cohort — measured at initial biochemical screening — shows the same recurrence effect (54% vs 8%) argues against a pure leak.
- **Whether `tumour_category = multifocal` (93 rows, 47% metastatic) was ever assigned on the basis of lesions later judged to be metastases.** Distinguishing multifocal primaries from metastases is clinically ambiguous; the source defines metastases as deposits in chromaffin-free tissue, which largely guards against it, but the per-patient adjudication is not in the data.
- The Lancet Digital Health supplement and the full publisher text (PMC and Springer both refuse automated fetches; I used the NCBI e-utils XML of PMC10565306, which carries the main text but not the supplement). I found no competition forum, "magic feature" thread or published criticism of this dataset — it is a clinical cohort released alongside one paper, reused in the Kather-group TabPFN benchmark (BMC Med Inform Decis Mak 2026), not a competition dataset.

Sources: [Zenodo record 7749613](https://zenodo.org/records/7749613) · [Pamporaki et al., Lancet Digit Health 2023 (PMC10565306)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10565306) · [Shaktah et al., BMC Med Inform Decis Mak 2026](https://bmcmedinformdecismak.biomedcentral.com/articles/10.1186/s12911-026-03654-3)

</details>

<details><summary>Precedent check</summary>

**Precedent check: `pheochromocytoma_paraganglioma_metastasis` (2026-11-25)**

I read the files only and trained no models. I ran the decision register (7,375 decisions, 46 flags). None of the flags names this dataset. Only the TP-4 flags (drift and opposite outcomes) bear on it, and I read their cases. The register output is in `panel/precedent-checker_register.md` and `panel/register.json`.

**Decisions that follow precedent**

| Decision | Verdict | Closest precedents |
|---|---|---|
| Random split on L-PLACE.random, `ForcedIIDFromGrouped`, the source's internal-to-external split not taken (settled, issue 2) | consistent | The only other two definitions on this leaf were decided by Andrej today, 2026-11-25, in the same way: `deafness_gene_carrier_hearing_loss` (two recruiting sources, source split rejected, issue 2 A) and `wild_type_attr_cardiac_amyloidosis`. The pheo cross-check (trained on the earlier cohorts, scored on PMT 0.939-0.947, against random folds on PMT rows 0.943-0.947) matches the check deafness made (0.750 against 0.750). |
| Plasma values rounded to whole pg/mL (`Class-dependent Recording`) | consistent | LEAK-13: hepatitis_c_prediction (2026-09-30), gallstone_disease, regensburg_pediatric_appendicitis (2026-10-27), dementia_prediction (2026-11-05). The effect was measured first (format alone 0.531, models unchanged), as LEAK-13 asks. LEAK-15 (retire) does not apply: one format, undone. |
| Tumour volume missing mostly for metastatic patients, kept as published with a measured note | consistent | LEAK-13's "first measure" (indicator 0.559, median fill moves no model by more than 0.001). It differs from heart_failure_followup_survival (LEAK-40): those cells were filled from the outcome groups, these are blank. |
| Specialists' 24 risk calls and the PMT investigator's prediction dropped | consistent | USE-6 case 2_month_survival_rate_prediction (2026-10-26, Lennart): the physicians' estimates are the source's comparators, not inputs. The "false negative" value, written with hindsight, is LEAK-10. |
| `Patient ID` dropped (sorted by cohort and outcome) | consistent | The identifier practice in definitions.md (a running id encodes the order or origin). |
| SDHB status kept with "not tested" as its own value (settled, issue 1) | consistent | CLEAN-10 practice: the missing case keeps its meaning. |
| Metric fallback ROC AUC | consistent | MET-5 and MET-6. The two leaf siblings use the same fallback (deafness, wild_type). |
| Time basis `ForcedIIDFromTemporal` (deafness uses `Timeless`) | departs, with a stated reason | Patients enrolled over years with dates lost, against germline genotypes in deafness. The fact differs, so the departure is sound. |
| TP-4: untrained count of 5 risk factors 0.904 against 0.945; kept | consistent on outcome | The gain (0.04 AUC, fold SE about 0.002) is far above sepsis_survival (+0.001, retired at step 2) and ljubljana_breast_cancer (a match, retired). It sits with the kept cases (california_house_prices_2020). The method has gaps; see item 3. |

**Departures for the curator (in the record's review-issue shape)**

**1. Declare the cohort flag a provenance column, as deafness declares its source file?** (departs without a stated reason; low stakes)

* **Problem:**
  - Both datasets have the same resolution, "no feature", decided the same day by the same curator. Deafness keeps `source_file` as `NonFeature(..., "provenance")`; pheo drops `cohort` in `_clean`.
  - Deafness is the only definition with a provenance `NonFeature`, so there is no wider practice yet. definitions.md names this use: "a `source_file` declared as provenance may be the group key of a task that holds files out."
* **Options:**

  | | Option | Pro | Con |
  |---|---|---|---|
  | a | Keep `cohort` as `NonFeature("cohort", "provenance", ...)` | matches deafness; the README lists it under "Never features"; a later task can hold the PMT cohort out | one more declared column |
  | b | Drop it, as implemented | simpler | two leaf siblings that differ for no stated reason |
* **Recommendation:** a, so the two cases match. The best guess at a fact that sets them apart: none written down.
* Rules: SPLIT-36, the `non_features` section of definitions.md.

**2. The 221 patients with an earlier tumour are not at the stated prediction point, "at first diagnosis". Keep them?** (departs, with a stated reason that covers only part of it)

* **Problem:**
  - The use case and the prediction point say "at first diagnosis", but 221 of 788 patients present with a recurrence. 156 of them are metastatic (79% in the earlier cohorts). The definition's note says "their metastases may have shown before this presentation".
  - SEL-7 cases retire labels the patient already has: cdc_diabetes_health_indicators (2026-10-15) and stroke_prediction (2026-10-26). USE-11 keeps only the row at the use case's point: breast_cancer_prediction, each woman's earliest exam (2026-10-15).
  - The stated reason, "one of the paper's nine features", explains why the column stays, not why these rows are inside the use case.
  - Measured: without the column RF scores 0.899. On the 567 first-tumour patients (67 metastatic) models score 0.87-0.92.
  - Facts that may set it apart (best guess, option a): metastases are found by imaging, not self-reported as in the SEL-7 cases; the source's task includes these patients; and it is unknown whether their metastases were known before entry.
* **Options:**

  | | Option | Pro | Con |
  |---|---|---|---|
  | a | Keep all rows (implemented) and reword the use case and row to "at presentation with a primary or recurrent tumour" | the source's task first (source-before-own); all 223 positives | a share of the recurrent positives may be known at entry, a partial SEL-7 |
  | b | Keep only the 567 first-tumour patients, drop `previous_ppgl` | matches the stated prediction point; follows USE-11 / breast_cancer_prediction | 67 positives, about 22 per test fold; departs from the source's task |
* **Recommendation:** a with the wording fix, unless the curator holds that the recurrent patients' metastases were typically known at entry; then b.
* Rules: USE-3 (Must), SEL-7 (Must), USE-11 (Must), the source-before-own practice.

**3. Name the sources of the risk-factor cutoffs and pair the TP-4 comparison per split?** (wording and method; no change to the verdict)

* **Problem:**
  - The note's untrained score uses methoxytyramine over 33 pg/mL and volume over 33.5 (about 4 cm), but cites no source for either cutoff. TP-4 says to take the rule from the field's sources, not from the rows. ljubljana_breast_cancer's first proof was replaced because its node cut-off had "unrecorded source" (2026-11-12).
  - `experiments.json` holds one pooled AUC (E9: 0.9041), not a comparison paired per split as amended TP-4 asks.
* **Options:**

  | | Option | Pro | Con |
  |---|---|---|---|
  | a | Cite the cutoffs (for example the 0.2 nmol/L methoxytyramine limit, if that is the source) and report the paired gain on the 30 splits | follows amended TP-4 and the Ljubljana precedent | one cluster run |
  | b | Keep the note as written | no work | unverifiable rule |
* **Recommendation:** a. The verdict will very likely stand: the gap is about 20 times the fold SE.
* Rules: TP-4 (Must).

**Cross-dataset note (several datasets)**

`split_tree.md` (lines 342-343) still says L-PLACE.random has "No v0.2 definition reaches it yet". Three definitions now reach it (deafness, wild_type, pheo, all 2026-11-25), and the curator decided all three the same way (random). This fits the empty-leaf practice (a reviewer decides the first cases). The leaf's examples line needs an update. This belongs in the working copy's REVIEW.md, not in this record.

**Drift and amendments**

No drift on this dataset's rules. This is not a third exception of a kind under SEL-7 or USE-11: the pheo case would be the first partial-prevalence keep, so if option a is chosen, the stated distinguishing fact should go into SEL-7's Cases.

</details>

<details><summary>Advocate (brief and rebuttal)</summary>

**Advocate: pheochromocytoma_paraganglioma_metastasis (opening brief)**

**Position:** ship. Three wording changes in `dataset.py` (the prediction point and fit, the metric origin, three
refuted or imprecise notes) and one optional declaration (`cohort` as a provenance non-feature). No change to the
rows, the features or the split unless the curator takes the fallback in point 2.

**1. A real task with nothing to exploit (P3, P4; USE-12 Must, LEAK-10 Must, TP-4 Must)**

- **Claim:** a documented clinical task (Lancet Digit Health 2023, CC BY 4.0, 788 patients, 223 positives) with
  real headroom and no exploitable leak.
- **Evidence:**
  - Every attack the task gamer built moved AUC by 0.003 or less. A column of random numbers moves it by the same
    amount (+0.0020). The attacks were: the cohort flag recovered from Zenodo (+0.0025), transductive ranks and
    counts (+0.0019), missing-value flags (+0.0006), number format, row order and patient matching.
  - Train-vs-test separation scores 0.486. There are no duplicate rows and no near-copies.
  - The blind reviewer, without our notes, found that every comparator column was "correctly excluded".
  - TP-4: an untrained count of five risk factors scores 0.904, against 0.945 for the best models. The gap is about
    20 times the fold SE, so the task is not trivial.
  - Models still beat the experts: the best of the 12 specialists scored 0.815. Methods separate cleanly (logistic
    0.949 > RF 0.943 > LGBM 0.937 > kNN 0.927).
- **Why it outranks:** no panel report claims a leak. Every objection below is about framing or wording, which is P7
  or a USE-8 statement. None is a validity failure without a fix.

**2. The recurrent patients: concede the wording, keep the rows (USE-3 Must, USE-8 Must, SEL-7 Must)**

This is the critic's strongest point, and the facts behind it are real. Our use case says "at first diagnosis", but
221 of the 788 patients (156 of the 223 positives) present with a recurrence or a new tumour. Scored on first-tumour
rows only, the models reach 0.886, not 0.938.

- **Claim:** these rows are a second real prediction point, not a leak. The mildest fix is to the definition's
  words, not its rows.
- **Evidence that `previous_ppgl` is not post-outcome information:**
  - The clinician knows the patient's history at the presentation. So the column is known at that row's prediction
    point (USE-3 holds per row).
  - The effect holds in the prospective PMT cohort, whose biochemistry was taken "at initial screening": 54% of the
    recurrent patients there are metastatic, against 8% of the first-tumour patients. The earlier cohorts show the
    same pattern (79% against 14.5%).
  - Methoxytyramine is lower in recurrent metastatic patients than in first-tumour metastatic ones (median 23 against
    52 pg/mL). A measurement of known metastatic burden would push it the other way.
  - The source's own task includes these patients, and one of its nine features names them. The source's task comes
    before our own.
- **Why SEL-7 does not apply:** that rule is about a label the respondent reports in the same interview, which
  nobody predicts. Here metastases are found by imaging or histopathology, and the label includes metastases found
  during follow-up. Whether some recurrent patients already had known metastases at entry cannot be read from the
  file (no dates). It is unproven either way, and it is the curator's call.
- **Mildest remedy:**
  - Reword `use_case`, `row` and `known` to "at presentation with a first or a recurrent tumour, before surgery".
  - Set `fit` to approximate, naming two gaps: the two kinds of presentation, and that the plasma sampling time is
    not stated for the recurrent rows (USE-8 lists exactly such a known gap).
  - Report the first-tumour score (0.87-0.92) in a note.
- **Fallback if the curator holds that metastases were typically known at entry:** keep only the 567 first-tumour
  patients (option B). That task still scores 0.87-0.92 with 67 positives, about 22 per test fold, which can be
  scored (TP-5). So the dataset survives either branch. This is a reframing, not a reason to exclude.

**3. The random split is right, and measured to be so (SPLIT-36 Should, SPLIT-15 Must; settled, issue 2 A)**

- **Claim:** the forced random leaf is what the tree gives, and it does not flatter the source's transfer test.
- **Evidence:**
  - Split auditor (a cluster run): the source's split, IT to EV, scores 0.943, 0.926 and 0.947 (95% CI about
    ±0.03). Random folds score 0.937, 0.943 and 0.948. All are within each other's interval. The blind reviewer
    finds the same (0.937 against 0.935).
  - A single fixed split cannot rank the models: RF comes last under IT to EV, LGBM last under the random folds,
    and both gaps sit inside one split's CI. SPLIT-15 asks for varied training sides.
  - Every test fold holds both cohorts (EV share 0.33-0.43).
  - Precedent: the only other two definitions on L-PLACE.random were decided the same way the same day
    (deafness_gene_carrier_hearing_loss, wild_type_attr_cardiac_amyloidosis).
- **Answers the blind reviewer's "comparability lost":**
  - No rule makes comparability with published numbers a criterion. The source split was tested first, as the
    source-before-own practice asks.
  - It was valid but gave one training side, and it scores the same.
  - The curator decided this with that evidence in hand.

**4. SDHB kept: settled, and nothing new against it (USE-3 Must; settled, issue 1 A)**

- **Evidence:**
  - Dropping SDHB costs 0.0027 (task gamer) or 0.0016 (E8), which is inside the random-column noise band. Keeping it
    gives no shortcut.
  - "not tested" (80 patients) is a real state that the endocrinologist knows. It is spread mostly over non-metastatic
    patients (62 of 80), so the gap does not follow the outcome.
  - The paper itself reports a ten-feature model with SDHB (0.940).
- **Why it outranks:**
  - The blind reviewer and the task gamer repeat a concern the curator already weighed: the Discussion's "often not
    available at initial diagnosis".
  - No new fact has come up. Under "Who decides", a settled curator decision stands unless new evidence arrives.
- **Remedy:** none. At most, note in `known` that SDHB status is the germline result where available.

**5. The cleaning follows precedent and was measured first (LEAK-13 Must, CLEAN rules)**

- **Plasma decimals:**
  - 14 rows with decimals, all metastatic, are rounded to whole pg/mL. The format alone scored 0.531, and the
    models are unchanged after rounding (RF 0.9445 either way).
  - This follows the same pattern as hepatitis_c_prediction, gallstone_disease, regensburg_pediatric_appendicitis
    and dementia_prediction (precedent checker: consistent).
- **Tumour volume missing for 36 patients (29 of them positive):**
  - It is kept as published. The missing flag alone scores 0.559, and median filling costs 0.0006 to 0.001.
  - The gap is also redundant: 29 of the 36 have an earlier tumour, so `previous_ppgl` carries the same signal.
- **One volume of 0.0 (column auditor):** a cheap CLEAN fix (set it to missing, or note it as below 0.05 mL) on one
  row, with no effect on the scores. Take it or leave it with a note.

**6. ROC AUC holds, on a stronger footing than stated (MET-5 Should)**

- **Claim:** the metric is right. Only its stated origin is wrong.
- **Evidence:** the claim auditor finds that the paper selects its candidate and final models "according to AUC"
  (Methods). MCC and balanced accuracy were only "considered", and Table 2 contradicts the Discussion's
  MCC sentence. Under MET-5 that is one deliberate choice, so ROC AUC is the source's metric. The domain
  practitioner independently keeps `roc_auc`: no threshold is fixed, and the prevalence differs by cohort (34%
  against 19%).
- **Remedy:** declare the origin as the source's metric, or keep the fallback with the reason rewritten. The score
  is unchanged either way.

**7. Concessions that cost nothing (wording and provenance)**

- **Cohort flag:** the precedent checker shows that deafness declares its `source_file` as a provenance
  `NonFeature`, while we drop `cohort`. I concede the inconsistency. Declaring `cohort` as
  `NonFeature(..., "provenance")` keeps it out of the features, as the curator decided. It matches the sibling
  dataset and lets a later task hold PMT out.
- **"false negative" written with hindsight (bullet 2):** this is refuted. The value marks the 28 patients with
  negative biochemistry. The drop still stands, because the column is a comparator recorded for PMT only. Reword it.
- **Smaller wording fixes:**
  - "27 with an earlier tumour" should be "29 (27 of them metastatic)".
  - The group-basis range should be 0.93-0.95 with its CI.
  - TP-4's cutoffs need a cited source and a per-split paired gain. The verdict will not move.
- **Things to note, not fix:**
  - Possible patients shared across cohorts: at most about 2% of rows, unverifiable, and the score does not move
    (LEAK-42, weak).
  - A shorter follow-up for negatives is already disclosed (`Target: Varying Delay`, `fit_reason`).

**Judgment record (advocate's view):**

```text
Verdict: ship after changes.
Validity: USE-3/USE-8 triggered: two presentations in one table, fixed by rewording, fit approximate (fallback:
first-tumour rows only); LEAK-10 holds (comparators dropped); LEAK-13 fixed (rounding); SPLIT-36 forced leaf, settled.
Value: TP-4 holds (0.904 vs 0.945); MET-5 holds (AUC is the source's selection criterion).
Quality: volume 0.0 (cheap fix); notes reworded.
For the curator: whether the recurrent patients' metastases were typically known at entry (if so, option B).
```

**Rebuttal**

The critic and I agree on the verdict: ship after changes, with no exclusion and the settled decisions unchanged.
The one remaining difference is how much weight one piece of evidence bears in critic point 1.

1\. **Prediction point: I concede the remedy and dispute one inference.**
   - **Conceded.** "Direct, at first diagnosis" cannot ship as written. Remedy (a), with `fit = "approximate"`, is
     also my remedy. Option (b) is the curator's fallback.
   - **Disputed.** The critic infers that the recurrent rows' plasma values come from a later surveillance visit.
     The evidence does not establish that.
     - The biochemically negative PMT patients are mostly the trial's "another 28 with negative test results". The
       claim auditor found that 24 of these 28 have extra-adrenal tumours, 23 of them head-and-neck. Such tumours
       are often biochemically silent at any visit. Tumour type is therefore a competing explanation for the
       negative values, independent of when the blood was drawn.
     - PMT enrolled patients at "initial screening", and recurrent PMT patients show the same effect (54% against
       8% metastatic).
     - Methoxytyramine is lower in recurrent metastatic patients than in first-tumour metastatic ones (median 23
       against 52 pg/mL). That points away from a reading of known metastatic burden.
   - **What follows.** The sampling time stays open (EV-1: unsettled, not shown either way). `fit_reason` should
     name it as an unknown, not as a fact that the rows mix two dates. Age, location and volume describing the
     initial tumour is a real two-date mix, and I concede it.
   - **SEL-7.** I agree it is an open risk that cannot be measured. It is the curator's call, and it is the one
     question that decides between (a) and (b).

2\. **Open label horizon: conceded.**
   - I had treated follow-up as a note only. USE-8 lists "no stated horizon" as a known gap that makes a fit
     approximate. The precedent is differentiated_thyroid_cancer_recurrence. The definition's own `fit_reason`
     names this gap, so `direct` contradicts it.
   - What follows: the fit is approximate for two independent reasons, and `fit_reason` names both. It would stay
     approximate even under option (b). No data change.

3\. **Metric origin: agreed.** This is my point 6. ROC AUC becomes the source's metric. No score changes.

4\. **Refuted notes: agreed.** The three rewordings are in my point 7. The "false negative" fact also bears on point 1,
   in the direction given above.

5\. **TP-4 cutoffs: conceded.** Cite a source for the cutoffs, or say they were chosen by us, and add the gain paired
   per split. The verdict does not move: the gap is about 20 fold SEs.

6\. **Cohort as a provenance NonFeature: agreed.** This is my point 7. It also answers the blind reviewer's
   comparability concern without changing the split.

7\. **The 0.0 tumour volume: agreed.** Set it to missing. This is a cheap CLEAN fix.

**Combined changes, none of which touches the split or the feature set:**
- Reword `use_case`, `row` and `known`.
- Set `fit` to approximate, giving the reasons: two kinds of presentation, an open horizon, and an unknown plasma
  sampling time. Note the first-tumour score (about 0.89).
- Set the metric origin to the source's metric.
- Reword three notes and the TP-4 note.
- Declare `cohort` as a provenance NonFeature.
- Set the 0.0 volume to missing.

**For the curator:** were the recurrent patients' metastases typically known at entry? If yes, take option (b).

</details>

<details><summary>Critic (brief and rebuttal)</summary>

**Critic: pheochromocytoma_paraganglioma_metastasis (opening brief)**

Position: ship only after changes. Nothing here calls for exclusion. The curator's settled decisions stay as they are: SDHB kept with "not tested", random repeated 3-fold CV, and the cohort flag not a feature. I do not reopen them. Points 1 and 2 are about validity (P3); the rest are about documentation and method.

**1. The stated prediction point does not hold for 28% of the rows, which carry 70% of the positives (USE-3, Must; USE-8, Must)**

- **Problem.** `use_case` and `known` say "at first diagnosis, before surgery", and `fit = "direct"`. But 221 of 788 patients have `previous_ppgl = Yes`, which the source defines as "local recurrence and/or new tumor". At a first diagnosis that value is "No" by definition. These 221 rows hold 156 of the 223 metastatic patients. The definition admits this only in a note ("their metastases may have shown before this presentation").
- **The rows also mix two dates.** For these patients, age, location and volume describe the initial tumour, and 27 of the 36 missing volumes are recurrent metastatic patients. The plasma values look like they come from the later visit:
  - Biochemically negative patients: 36% of recurrent PMT patients (27/74) against 6% of first-tumour PMT patients (13/221) (column auditor).
  - All 9 metastatic "false negative" PMT patients are recurrent.
  - Values below the reference limits in a patient with a known PPGL look like surveillance values taken after a resection.
- **Effect on the task.**
  - The headline score is mostly about patients the use case does not describe. A tuned model scores 0.938 on all test rows and 0.886 on the first-tumour rows only (task gamer). On the first-tumour rows, models score 0.87-0.92 (E5b and E5c).
  - The domain practitioner calls the fit approximate: "the 0.94 is inflated by recurrent patients I would image anyway".
  - Whether some recurrent patients already had known metastases when they entered the study cannot be checked: there is no date, and the supplement is unread. If they had, this is a partial SEL-7 (Must): a label the patient already has.
- **Evidence.** Column auditor, problem 1. Domain practitioner, gap 1. Task gamer, flaw A. Precedent checker, departure 2: SEL-7 cases cdc_diabetes and stroke_prediction, and USE-11 breast_cancer_prediction. Blind reviewer, concern 1.
- **Remedy (mildest first).**
  - **(a)** Keep all rows, as the source did (source before own). Reword `use_case`, `row` and `known` to "at presentation with a first or a recurrent tumour". Set `fit = "approximate"`, and have `fit_reason` name the two-date rows and the first-tumour score (about 0.89).
  - **(b)** Restrict to the 567 first-tumour patients (67 positives, about 22 per test fold) and drop `previous_ppgl`. Take (b) if the supplement, or the curator, holds that recurrent patients' metastases were typically known at entry.
  - Either way, the curator decides. Shipping "direct, at first diagnosis" as written is not an option.

**2. The label has no stated horizon, so the fit is approximate even without point 1 (USE-8, Must; USE-5, Must)**

- **Problem.** The label counts metastases found "at diagnosis or during follow-up of varying length". Follow-up in the PMT trial is 49.3 months for patients without metastases against 99.7 months for patients with them (Table 1). Synchronous and metachronous metastases are merged.
- **Rule.** USE-8 names "a label definition the sources do not settle (no stated horizon …)" as a reason the fit is approximate. The precedent is differentiated_thyroid_cancer_recurrence. The definition's own `fit_reason` names this gap and still declares `direct`.
- **Remedy.** `fit = "approximate"`, and `fit_reason` names the open horizon and the partly censored "No" labels. No data change.

**3. The metric origin is mislabelled (MET-5, Should)**

- **Problem.** The reason says the paper picked "the final one by MCC and balanced accuracy". The claim auditor refutes this:
  - In Methods, the paper selects both the candidate and the top models "according to … AUC", with MCC and balanced accuracy only "considered".
  - The MCC claim appears only in a Discussion sentence, and Table 2 contradicts it (TC: 0.863/0.890 against ENS 0.851/0.878).
- **Effect.** No score changes. The README misstates what the source chose.
- **Remedy.** Declare ROC AUC as the source's metric (model selection by AUC, Methods). If the fallback is kept, rewrite the reason to "the paper selects models by ROC AUC, the same as the fallback".

**4. Notes that the evidence refutes (writing; EV-2)**

- **"false negative" "was written with hindsight": refuted.** The value marks the 28 PMT patients with negative biochemical tests ("another 28 with negative test results", Methods). Dropping the column still stands, as a comparator recorded for one cohort only. Reword the reason. This fact also strengthens point 1.
- **Volume note: "27 with an earlier tumour" is imprecise.** 29 of the 36 have an earlier tumour; 27 is the count among the metastatic.
- **`group_basis` "0.939-0.947 on the PMT trial" is too precise.** The split auditor gets 0.926-0.947 under another NaN handling, with a 95% CI of about ±0.03 on 295 patients. Write 0.93-0.95 and give the CI.
- **Remedy.** Edit the wording of the three notes. The conclusions stand.

**5. The untrained risk-factor rule has unsourced cutoffs and an unpaired score (TP-4, Must on any `Trivial` proof)**

- **Problem.** The note's cutoffs (methoxytyramine over 33 pg/mL, volume over 33.5) cite no source. TP-4 asks for the rule from the field's sources, as in the Ljubljana precedent (2026-11-12). E9 is also one pooled AUC, not a comparison paired per split.
- **Effect.** None on the verdict: the gap (0.904 against 0.945) is about 20 fold SEs.
- **Remedy.** Cite the cutoffs, or reword the note as "a five-factor count with cutoffs chosen by us". Add the paired per-split gain when convenient.

**6. The cohort flag is handled differently from the same-day sibling (consistency; Should)**

- **Problem.** deafness_gene_carrier_hearing_loss, on the same leaf and decided by the same curator the same day, keeps its source file as `NonFeature(..., "provenance")`. Here `cohort` is dropped. No fact sets the two cases apart.
- **Effect.** Keeping it as a NonFeature still honours "not a feature", and lets a later task, or a reader, reproduce the source's IT-to-EV split. This also answers the blind reviewer's comparability concern without changing the split.
- **Remedy.** Declare `cohort` as a provenance NonFeature instead of dropping it.

**7. One impossible tumour volume (CLEAN, quality)**

- **Problem.** `primary_tumour_volume = 0.0` for one PMT patient.
- **Remedy.** Set it to missing, or add a one-line note. No effect on scores. This is not a reason against the task.

**Judgment record (critic's view)**
Verdict: ship after changes.
Validity: USE-3 / USE-8 triggered (prediction point and fit wrong for the recurrent rows); fix by rewording to "first or recurrent presentation" with fit approximate, or restrict to first-tumour rows; SEL-7 risk open, not measurable without the supplement. USE-8 also triggered by the open label horizon.
Value: TP-4 holds (not trivial); cutoff sourcing to fix.
Quality: MET-5 origin and three refuted notes to reword; cohort as a provenance NonFeature for consistency; one 0.0 volume.

**Rebuttal**

The advocate and I agree on the verdict (ship after changes), on the remedies, and on handing the curator the recurrent-row fork. What is left in dispute is narrow.

1\. **A real task with nothing to exploit: concede.** No report claims a leak. TP-4 holds (0.904 against 0.945), and every exploit sits inside the random-column noise band. I never argued for excluding the task.

2\. **Recurrent patients: concede the remedy (reword, fit approximate, first-tumour score in a note, option B as the fallback). I dispute two of the supporting arguments, which the curator should not take as settled.**
   - **"Biochemistry taken at initial screening" does not show the plasma values belong to the first tumour.** For a recurrent PMT patient, the screening is the recurrence's. The column auditor counts 27 of 74 recurrent PMT patients biochemically negative against 13 of 221 first-tumour patients. All 9 metastatic "false negatives" are recurrent. So the two-date problem is in the prospective cohort too.
   - **Lower methoxytyramine in recurrent metastatic patients (23 against 52 pg/mL) argues against metastatic burden, but for surveillance timing.** Low values after a resection are what a later measurement looks like. The evidence is consistent with the advocate's "not a leak" and with my "not the first diagnosis". It is not evidence for "at the first presentation".
   - **SEL-7: I concede that its letter (a label the respondent reports in the same interview) does not fit**, since imaging finds these metastases. The concern behind it, a positive already known when the prediction is made, is unproven either way, as the advocate says. Under USE-3 (Must) that stays the curator's question: "were the recurrent patients' metastases typically known at entry? If yes, take B". It is not a resolved point.
   - **I accept the advocate's extra fit gap (plasma sampling time unstated for the recurrent rows).** It should go into `fit_reason`.

3\. **Random split: concede.** It is settled (issue 2 A), and I did not contest it.

4\. **SDHB: concede.** It is settled (issue 1 A), and no new fact has come up.

5\. **Cleaning: concede.** The volume of 0.0 is a cheap fix or a note, as I said.

6\. **Metric: concede.** We agree: ROC AUC is the source's metric, and the origin should be relabelled.

7\. **Concessions: agreed, except for "follow-up already disclosed, note only" (dispute).** USE-8 (Must) says a label whose horizon the sources do not settle makes the fit approximate. Disclosing the horizon in a note is not enough while `fit` says direct. Since both sides now set the fit to approximate under point 2, the fix costs nothing: `fit_reason` names the open horizon (partly censored "No" labels, 49 against 100 months of follow-up in PMT) as its own gap, beside the two presentations and the plasma timing. This matters if the curator takes option B: the first-tumour task would still be approximate for this reason alone. On possible patients shared across cohorts I concede: note only.

**What remains for the curator**
- Option A or B for the recurrent rows: were the metastases known at entry?
- The fit is approximate in either case, and `fit_reason` names three gaps:
  1. the two kinds of presentation (gone under B);
  2. the plasma sampling time;
  3. the open label horizon.

</details>
