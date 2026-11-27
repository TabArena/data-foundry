---
unique_name: bcsc_risk_estimation
name: BCSC Risk Estimation Dataset
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
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
