---
unique_name: bcsc_risk_estimation
name: BCSC Risk Estimation Dataset
checked_by:
- AI (UNVERIFIED)
- Andrej
data_foundry_status:
- WIP (Triage)
claimed_by: Andrej
suggestion: 'Yes'
priority: 3
tags:
- AI-Filled (Verify)
- New IID
- 'Samples: Over Time'
- 'Time: Lost'
- 'Target: Fixed Delay'
- Clinical Study
original_source: GOV Website
year: '? (2006)'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.bcsc-research.org/index.php/datasets/rfdataset
- https://www.bcsc-research.org/index.php/datasets/rfdataset/dataset
- https://doi.org/10.1093/jnci/djj331
needs_review:
- ai_unverified
v2_path: datasets/_dev/tabarena-v0pt2/bcsc_risk_estimation/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: 2,392,998 BCSC screening mammograms with the one-year breast cancer outcome and 11 risk factors, the data of Barlow et al. 2006's published risk model; a real screening task, shipped as aggregated counts of categorical factors.
- Source: Breast Cancer Surveillance Consortium (NCI-funded), "Risk Estimation Dataset" (https://www.bcsc-research.org/index.php/datasets/rfdataset), the data of Barlow et al., "Prospective breast cancer risk prediction model for women undergoing screening mammography", JNCI 98(17):1204-1214, 2006 (doi 10.1093/jnci/djj331), which users must cite; the file's own release date is not stated (a one-observation-per-woman version was added in August 2012). As published (documentation page): `risk.txt`, 280,660 records ("This reduces the dataset to 280,660 records"), one per combination of risk factors and outcome with a `count` ("The count variable (16) must be used to obtain correct estimates"); menopaus, agegrp (35-84 in 5-year bands), density (BI-RADS 1-4), race, Hispanic, bmi, agefirst, nrelbc, brstproc, lastmamm, surgmeno, hrt; targets `invasive` and `cancer` (invasive or DCIS within one year); a 75/25 `training` flag; code 9 is unknown. Exams 1996-2002, "this dataset is static". "The index mammogram's assessment is not included." Access after a registration form.
- Use case: a screening programme, at a woman's screening visit, estimates her short-term breast cancer risk from self-reported risk factors, breast density and her last mammogram result, to tailor screening and prevention ("Our risk model may be able to identify women at high risk for breast cancer", abstract); fit direct. Regime IID on the one-woman version: the cells carry no woman id, so the version with several exams per woman cannot be grouped (USE-11, as `breast_cancer_prediction`).
- Siblings and duplicates: `breast_cancer_prediction` (`Yes`; the BCSC Digital Mammography Dataset, 2014) is the same consortium but other exams and a later prediction point (at the read, with the BI-RADS assessment, kept as inputs by CC 2026-10-15); this file stops before the read, so a distinct task (PROV-7). `cbis_ddsm` (this run) is an image collection. No other record of this file (grep for bcsc, rfdataset, breast cancer surveillance). External collections: none found.
- Better data: from the run's search, a related task next to `breast_cancer_prediction`; no further search this round.
- Papers and pages: Barlow et al. 2006 (PubMed 16954473); the BCSC dataset and documentation pages (variables, SAS code for the paper's Table 3 and Table 5 models).
- Metric: the c statistic, the paper's one discrimination measure ("Concordance of the predicted with the observed outcomes was assessed by a concordance (c) statistic", abstract; 0.631 premenopausal, 0.624 postmenopausal), so `roc_auc`, which is also the fallback (MET-5, MET-8); inputs: `count`, used to expand the cells into exams (MET-2).
- Risks for /add-dataset: expand by `count` (2.39M exams, 11,638 cancers per the abstract, about 0.5%) and cap the rows; take the one-woman version; `cancer` (the paper's outcome) against `invasive` (USE-5); drop `training`, a prescribed random split (SPLIT-5); density is the radiologist's reading of the index exam, an input under SEL-14 like the readings of `breast_cancer_prediction`; code 9 as missing, not a level (CLEAN); exams of 1996-2002 under an older BI-RADS density definition, which the documentation flags (`Outdated` to weigh).
- Priority: gap 0 (medical and binary classification are not thin), use case + (the paper names the screening decision), source + (a consortium page, a codebook, a JNCI paper), shape 0 (millions of exams, but 11 low-cardinality categorical factors in aggregated cells), risk 0.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through a related task next to `breast_cancer_prediction`.
- as published: 2,392,998 screening mammograms (1996-2002) aggregated into 280,660 records, one per combination of risk factors and outcome with a count; two versions (multiple exams per woman, one per woman); 12 ...; target: breast cancer diagnosed within one year of the index screening mammogram (cancer: invasive or DCIS; invasive); access: registration.
- Why: same publisher and same outcome as breast_cancer_prediction but a different use case: risk estimation before the read, without the index exam's BI-RADS assessment (deliberately left out of the public file); a strong source with a published model
- Adds: about 60x more screening exams for the same 1-year cancer outcome; caveats: older (1996-2002), aggregated counts (expand by count or use weights), only categorical features

CC (2026-11-27, Andrej): add it. It is the risk task before the mammogram is read, which `breast_cancer_prediction` cannot carry (there the radiologist's read is a feature; its review issue 2).

## Review

**Outcome:** added. The BCSC Risk Estimation Dataset, one exam per woman: 1,007,660 women, 7,319 cancers within a year (0.73%), twelve risk factors known at the screening visit, before the mammogram is read; the risk task that `breast_cancer_prediction` cannot carry (its review issue 2).

**Main points:** Keep the forced time tag (1), ship despite exams of 1996-2002 (2), and take the one-exam-per-woman file (3)? The score is in line with the field: on the paper's own 75/25 split of the all-exams file logistic regression reproduces its c statistic (0.628 and 0.626 against the published 0.631 and 0.624), and on our 3 folds it reaches ROC AUC 0.650, LightGBM 0.656. Methods spread (logistic regression 0.646, LightGBM 0.634, random forest 0.578 in the untuned probes) and the best single feature, the age group, stays below them (0.611). Nothing leaks: 91% of the test women share their exact profile with training women (coarse categories), and looking up those women's outcomes adds nothing (-0.008, SE 0.005).

**Issues for Andrej:**

1. **Keep `ForcedIIDFromTemporal`, or tag `AssumedStationaryRelation`?**

   * **Problem:**
     - Time: Lost: exams 1996-2002, and the file carries no dates.
     - Use: a screening programme estimates a woman's one-year risk at her visit, decades after 2002.
     - Mechanism: two of the strongest inputs changed after 2002: hormone therapy use fell after the Women's Health Initiative trial[^whi], and the BI-RADS density categories were redefined in 2013.
   * **Background:** 28.6% of the exams are of women on hormone therapy; it is the third strongest single feature (ROC AUC 0.567 alone).
   * **For a stationary use case:**
     - the risk factors are those of the BCSC's risk models still in use.
     - a fixed one-year label window.
   * **Against:**
     - hormone therapy use and its link to breast cancer changed after 2002.
     - density coding changed in 2013.
     - film mammography, now replaced by digital and tomosynthesis, detected the cancers that make the label.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep `ForcedIIDFromTemporal` (implemented) | The folds stay; the Time basis line names the reasoning | Claims only what is known | The split stands for later women only as far as the relation is stationary |
     | B | `AssumedStationaryRelation` | The folds stay; you give the reason (eight words or more) | Documents why random folds stand for later women | hormone therapy and density coding changed after 2002 |

   * **Recommendation:** A, the hormone therapy change after 2002 is a fact against stationarity. Confidence: high. **Decision:** A or B?

   [^whi]: Rossouw JE, Anderson GL, Prentice RL, LaCroix AZ, Kooperberg C, Stefanick ML, Jackson RD, Beresford SA, Howard BV, Johnson KC, Kotchen JM, Ockene J; Writing Group for the Women's Health Initiative Investigators. Risks and benefits of estrogen plus progestin in healthy postmenopausal women: principal results from the Women's Health Initiative randomized controlled trial. JAMA. 2002;288(3):321-333. doi:10.1001/jama.288.3.321. SPLIT-32 asks the review to reason whether the use case can be taken as stationary; `AssumedStationaryRelation` is set by a person only.

2. **Ship it although its exams are from 1996-2002?**

   * **Problem:**
     - The exams are 24 to 30 years old, film-era, before the 2002 drop in hormone therapy; the source says the data are static.
     - No newer BCSC file has the outcome: the BCSC Risk Factors summary (2005-2017) has the risk factors but no one-year cancer.
   * **Background:** the BCSC's own risk calculator and its later model versions are built on BCSC data of the same kind, so the task is how the field estimates this risk.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Ship (implemented) | No marker | The only open source of this task, with a published model to compare; 1M women | Old data; the stationarity of issue 1 is not assumed |
     | B | Ship with `Outdated` as a concern | The marker records the age; the dataset ships | Makes the age visible to users | A marker on a shipped dataset is only a note |
     | C | Do not add (`Outdated`) | Not added | No 25-year-old data in the benchmark | Loses the before-the-read risk task, and with `breast_cancer_prediction` retired, the screening question altogether |

   * **Recommendation:** A, the age matters for a deployed model, not for comparing methods on one relation. Confidence: medium. **Decision:** A, B or C?

3. **Take the one-exam-per-woman file, or the all-exams file the paper used?**

   * **Problem:**
     - The source offers two files: all exams (2,392,998, several per woman, the paper's data) and one exam per woman (1,007,660, added in 2012).
     - The all-exams cells carry no woman id, so random folds would put one woman's exams on both sides.
     - The page does not say how the one exam was chosen; its cancer share (0.73% against 0.49%) fits one exam drawn per woman, since women with cancer leave follow-up at the diagnosis.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | One exam per woman (implemented) | `risk_rand.txt`, 1,007,660 rows | Every row a different woman; no row budget needed | Not the paper's exact rows; selection rule not documented |
     | B | All exams | `risk.txt`, 2,392,998 rows, a `_1m` version | The paper's data | One woman's exams on both sides of a split, which no id can prevent |
     | C | Both, as two datasets | Two folders | – | The same task twice, one of them with the copies of B |

   * **Recommendation:** A. Confidence: high. **Decision:** A, B or C?
