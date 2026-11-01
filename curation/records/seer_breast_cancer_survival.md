---
unique_name: seer_breast_cancer_survival
name: SEER Breast Cancer Data (IEEE DataPort)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
tags:
- AI-Filled (Verify)
original_source: Other
year: '2019'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://ieee-dataport.org/open-access/seer-breast-cancer-data
- https://doi.org/10.21227/a9qy-ph35
- https://seer.cancer.gov/data/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: a 4,024-patient cut of the NCI's SEER registry (women with infiltrating duct and lobular carcinoma, diagnosed 2006-2010) with vital status and survival months; real and documented, but a small fixed cut of the registry that `seer_breast_cancer_5y_survival` takes at full size.
- Source: Jing Teng (North China Electric Power University), "SEER Breast Cancer Data", IEEE DataPort, 18 January 2019, doi 10.21227/a9qy-ph35 (page read): "obtained from the 2017 November update of the SEER Program of the NCI ... female patients with infiltrating duct and lobular carcinoma breast cancer (SEER primary cites recode NOS histology codes 8522/3) diagnosed in 2006-2010. Patients with unknown tumor size, examined regional LNs, regional positive LNs, and patients whose survival months were less than 1 month were excluded; thus, 4024 patients were ultimately included." As published: one CSV (508 KB), 4,024 rows x 15 columns (age, race, marital status, T stage, N stage, 6th stage, grade, A stage, tumor size, estrogen status, progesterone status, regional nodes examined, regional nodes positive, survival months, status). The page names no target; status (alive/dead) is all-cause and read at the registry's follow-up cutoff, so the task is a fixed horizon, death within 60 months from survival months (SEL-6). Download needs an IEEE account. Companion paper: the Bayesian lymph-node-ratio study (IEEE JBHI 2020, PMID 31562112), whose abstract counts 5,279 women of the same selection, not 4,024 (not read; to reconcile).
- Use case: an oncologist at diagnosis estimates a patient's 5-year risk of death from stage, grade, nodes and receptor status, to plan adjuvant treatment and follow-up. Fit approximate: no treatment, HER2 or cause of death, and the source names no actor or decision. Regime IID (one row per patient; the year of diagnosis is not a column).
- Siblings and duplicates: `seer_breast_cancer_5y_survival` (unscreened: the full SEER research data, breast-cancer-specific death within 5 years, 27,064 women in its paper's cohort) is the same registry and the same task at full size, so the two are versions under PROV-6 and the curator picks one; `seer_primary_site_from_metastases` (`TBD -> Yes`, same registry, another task, PROV-7); `metabric_breast_cancer_clinical` and `rotterdam_breast_cancer` (other cohorts of breast-cancer prognosis, PROV-4). Kaggle re-uploads of the same 4,024 rows: `reihanenamdari/breast-cancer` (48,530 downloads), `sujithmandala/seer-breast-cancer-data` and at least six more; none has a record (grep: seer, 4024, reihanenamdari). External collections: none known.
- Better data: from the curator's Zotero collection (item 124); no further search this round. The run's note stands: the SEER research database is the larger source of the same task (`seer_breast_cancer_5y_survival`).
- Papers and pages: the DataPort page (nine citing papers listed); Teng et al., IEEE JBHI 2020 (paywalled, not read); Thakur et al., "Democratising Clinical AI through Dataset Condensation for Classical Clinical Models", arXiv 2603.09356 (2026; its abstract does not name its six datasets; moved here from source_links as related work, PROV-12).
- Metric: none found (the DataPort page defines no task; the JBHI paper was not read), so the fallback `roc_auc` on death within 60 months (MET-1, MET-8); inputs none.
- Risks for /add-dataset: build the 60-month label from survival months and status; every patient has 60 months of potential follow-up only if the cutoff of the November 2017 submission is 31 December 2015 (to confirm); survival months and status never as features (LEAK); A stage, 6th stage and T/N stage encode the same staging in part (CLEAN); the exclusion of unknown tumour size and node counts selects patients (a note).
- Priority: gap 0 (medical, binary and IID covered), use case 0 (approximate, no actor named), source + (NCI SEER, a DataPort DOI and a paper), shape + (4,024 patients, 13 mixed features), risk - (the full registry is a larger version of the same task, PROV-6).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 124: "Democratising Clinical AI through Dataset Condensation for Classical Clinical Models".
- as published: 4,024 female patients with infiltrating duct and lobular carcinoma, diagnosed 2006-2010; 15 columns (age, race, marital status, T/N/6th AJCC stage, grade, SEER historic stage, tumour size, ER/PR ...; target: Vital status (alive/dead) at the end of follow-up, or survival months; a 5-year death label is derivable since every patient has at least 5 years of potential ...; access: registration.
- Why: Real registry data, widely used as a survival benchmark, and the source is documented.
- Adds: Breast cancer prognosis; the existing breast records are diagnosis tasks. Status at a calendar cutoff is SEL-6, so use a fixed horizon. The full SEER research database (signed DUA, hundreds of thousands of cases) is the much larger source for the same task (a version, PROV-6).
