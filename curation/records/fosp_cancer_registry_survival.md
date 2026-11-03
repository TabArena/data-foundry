---
unique_name: fosp_cancer_registry_survival
name: Hospital-Based Cancer Registry of Sao Paulo (RHC/SP), 3-year survival after diagnosis
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
original_source: GOV Website
domain: medical & healthcare
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
source_links:
- https://fosp.saude.sp.gov.br/fosp/diretoria-adjunta-de-informacao-e-epidemiologia/rhc-registro-hospitalar-de-cancer/banco-de-dados-do-rhc/
- https://doi.org/10.1038/s41598-025-34133-w
- https://github.com/CDIA-NSEE/cancer_cross_prediction
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: the São Paulo state hospital cancer registry (FOSP's RHC/SP: 1,178,688 patients diagnosed 2000-2023 in 79 hospitals) with demographics, stage, first-course treatment and follow-up, used for 3-year survival after diagnosis by Cardoso et al. 2026; a large real prognostic task with a temporal split by year of diagnosis, but a recurrence column, the treatment timing and the target's construction are to settle.
- Source: Registro Hospitalar de Câncer do Estado de São Paulo (RHC/SP), Fundação Oncocentro de São Paulo (FOSP), São Paulo state health department. Its page "Banco de dados do RHC" (link 1): cases diagnosed from January 2000, updated quarterly ("A atualização deste banco de dados é trimestral"), anonymised, files by year of diagnosis, download after registration ("Faça um cadastro prévio para acessar os arquivos"); the file list did not load, so the data dictionary was not seen. As described by Cardoso et al. (Methods, "Study population"): "The registry spans cases recorded from January 2000 to December 2023, totaling 1,178,688 patients", from 79 public and private hospitals. Their cut: diagnoses 2000-2019, adults, residents of the state, clinical stage known, microscopic confirmation; 23 predictors (Table 4: age, sex, municipality, care category, prior diagnosis and treatment, clinical stage, seven first-course treatment flags, days from consultation to diagnosis and from diagnosis to treatment, year of diagnosis, health regions, the treating hospital's municipality and qualification, education, `presenca_rec`). Their target: 1 if the patient survived at least three years after diagnosis, from the last follow-up date and vital status; patients with less than three years of follow-up excluded ("Selection of variables").
- Use case: an oncology team estimating a patient's prognosis after diagnosis and first-course treatment. The paper says cross-prediction can "support clinical decision-making when expert models are unavailable" (Discussion), that it is "not yet ready for clinical application", and that overall survival "was justified by the purpose of estimating the general prognosis of patients"; fit approximate (no decision named, and the treatment flags are the hospital's own choice, so a model that informs treatment cannot take them as given). Regime temporal by year of diagnosis (a model fit on past cases is used on new ones); the paper used a random 75/25 split (SPLIT-5, a claim).
- Siblings and duplicates: no other record of the RHC/SP; `seer_breast_cancer_survival` and `seer_breast_cancer_5y_survival` (unscreened, US SEER) are the nearest tasks, another registry and population. External collections: none in our vocabulary.
- Better data: from the curator's Zotero collection (item 146, Cardoso et al.); no search for better data in this run.
- Papers and pages: Cardoso, Egydio, Toporcov, Utida, Curado, Fernandes, Ribeiro, Chin, Parro, "Cross-cancer survival prediction using machine learning models", Sci Rep 16:9623 (2026), https://doi.org/10.1038/s41598-025-34133-w (read from the UFG repository's PDF), code at https://github.com/CDIA-NSEE/cancer_cross_prediction; the same group's colorectal survival comparison on about 45,000 patients (arXiv 2510.24473, abstract read: C-index, IPCW C-index, time-dependent AUC and integrated Brier score).
- Metric: Cardoso et al. report balanced accuracy and F1 per cancer type ("We selected balanced accuracy and f1-score to capture overall model performance with reduced sensitivity to class imbalance", Results, "Phase 2") and sensitivity, specificity, accuracy and AUC in Supplementary Table 1: two threshold metrics side by side and no threshold fixed, so the fallback `roc_auc` (MET-5, MET-6, MET-8). Inputs none.
- Risks for /add-dataset: `presenca_rec` (presence of recurrence) is known only during follow-up and goes (LEAK); the follow-up and death dates build the target and go; the treatment flags and the diagnosis-to-treatment interval put the prediction point after the first treatment (USE-3, to decide); rows alive with less than three years of follow-up go, and the newest diagnosis years cannot reach the horizon (SPLIT-9); one dataset per cancer site or all sites with the topography as a feature, and a row cap, are to decide (PROV-7); the treating hospital is a grouping candidate inside the temporal task (SPLIT-13); the download needs a registration (no criterion, EV-4).
- Priority: gap 0 (medical, binary and temporal are not thin), use case 0 (decision support named only in general, fit approximate), source + (the state registry's documented page and a peer-reviewed paper), shape + (over a million patients, mixed types, 24 diagnosis years), risk - (a post-outcome recurrence column and a target to build from follow-up dates).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 146: "Cross-cancer survival prediction using machine learning models".
- as published: cancer patients, 1,178,688 rows 2000-2023 per the paper, 79 hospitals; ~23 predictors used (age, sex, residence, stage, first-course treatments, diagnosis-to-treatment days, hospital, education); target: survival 3 years after diagnosis (binary; or other horizons), from vital status and last follow-up date; access: registration.
- Why: very large public hospital registry with a real prognostic target, temporal split by diagnosis year, many cancer sites
- Adds: a large Latin-American oncology registry; no cancer registry in the records. Risks: drop presenca_rec (recurrence, after outcome); exclude patients followed less than the horizon (LEAK-23/24); one table per diagnosis year
