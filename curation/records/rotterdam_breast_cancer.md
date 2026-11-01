---
unique_name: rotterdam_breast_cancer
name: Rotterdam tumour bank primary breast cancer cohort (rotterdam)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
original_source: Other
year: '2013'
domain: medical & healthcare
original_data_state: One Table
source_links:
- https://doi.org/10.1186/1471-2288-13-33
- https://pmc.ncbi.nlm.nih.gov/articles/PMC3667097/
- https://rdrr.io/cran/survival/man/rotterdam.html
- https://github.com/ErikinBC/SurvSet
- https://arxiv.org/abs/2203.03094
- https://cran.r-project.org/package=survival
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: 2,982 primary breast cancer patients of the Rotterdam tumour bank with tumour size, grade, nodes, hormone receptors, menopause, age, year of surgery, treatments and follow-up to relapse and death, published with Royston and Altman's prognostic-model paper; a classic prognostic cohort for a fixed-horizon survival target, with the adjuvant treatments to judge as inputs.
- Source: Royston and Altman, "External validation of a Cox prognostic model: principles and methods", BMC Medical Research Methodology 13:33 (2013, doi 10.1186/1471-2288-13-33): "The original dataset comprised 2982 primary breast cancer patients", follow-up 1 to 231 months (median 107), and "The Rotterdam data (with RFS truncated to 120 months) can be downloaded"; the full data ship as `rotterdam` in the R package survival: 2,982 rows x 15 columns (pid, year of surgery, age, meno, size in three bands, grade, nodes, pgr, er, hormon, chemo, rtime, recur, dtime, death). The help page notes 43 patients who died without a recorded relapse after their relapse censoring time (death dates updated later), an open question for recurrence-free survival. The surgery years are in `year`; their range was not read.
- Use case: at primary surgery the oncologist estimates the risk of death or relapse, which informs adjuvant therapy; the paper names the use only broadly ("informing treatment or other clinical decisions for individual patients", risk stratification for trial entry), fit approximate. Target: death (or relapse) within 5 years of surgery from dtime and death, patients censored earlier dropped (USE-5, as cirrhosis_patient_survival_prediction). Regime IID over patients, or temporal by year of surgery; to decide from the use case (SPLIT-1).
- Siblings and duplicates: `haberman_survival` (`No`, `Trivial`, `Outdated`: 306 patients, three features), for which this was found; `metabric_breast_cancer_clinical` (unscreened, another cohort and the same kind of task); the SurvSet siblings `flchain_mortality` and `smart_vascular_events` (unscreened, other cohorts). No record of the GBSG validation cohort (686 patients, the `gbsg` data of the survival package). External collections: SurvSet (Drysdale 2022, arXiv 2203.03094, GitHub ErikinBC/SurvSet; not in the `collections` vocabulary, so named here only); a use with GBSG in DeepSurv-style survival benchmarks was not checked.
- Better data: found as better data for `haberman_survival`, and from the curator's Zotero collection (items 96 and 140, SurvSet); no further search this round.
- Papers and pages: Royston and Altman 2013 (PMC3667097); the survival package help page; SurvSet. The tumour bank's own first publications (Erasmus MC) were not traced.
- Metric: the paper uses "Harrell's c-index of concordance", Gönen and Heller's K and the Royston-Sauerbrei D statistic, with calibration plots: several measures for a survival model, none fixed for a horizon, so the fallback `roc_auc` for the 5-year binary target (MET-5, MET-8); inputs none.
- Risks for /add-dataset: `hormon` and `chemo` are the adjuvant treatments given after surgery; for a risk estimate that informs that decision they are not inputs (USE-4, LEAK-10), for a prognosis under the treatment received they are, so the framing decides; rtime, recur, dtime and death are the outcomes and go except as the target's inputs; the 43 deaths after relapse censoring for a relapse target; the size bands are coarse; `pid` is an id.
- Priority: gap 0 (medical, binary, IID are not thin), use case 0 (named only broadly by the paper), source + (a methods paper and the survival package's documented copy), shape + (2,982 patients, 10 mixed features, 8 without the treatments), risk - (treatment columns and a target we build from censored follow-up).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `haberman_survival`; the curator's Zotero collection, item 140: "SurvSet: An open-source time-to-event dataset repository"; the curator's Zotero collection, item 96: "SurvSet: An open-source time-to-event dataset repository".
- as published: 2,982 primary breast cancer patients, 15 columns: year of surgery, age, menopause, tumour size, grade, positive nodes, PR, ER, hormonal and chemotherapy, days to relapse and relapse flag, days to ...; target: death within 5 years of primary surgery, built from dtime and death, with patients censored before 5 years dropped (Haberman's target); recurrence-free ...; access: open.
- Why: Same task as haberman_survival: survival 5 years after surgery for primary breast cancer. Haberman's three features (age, year of operation, positive axillary nodes) are all columns here. | Classic published prognostic cohort with a direct clinical use; fixed-horizon framing as in cirrhosis (USE-5). Also found by the ...
- Adds: 2,982 patients against 306. A cohort operated decades after Haberman's 1958-1970 one, so less Outdated. Adds tumour size, grade, ER, PR, menopausal status and the treatments, which answers the Trivial and Not Representative markers (two features plus a year). Event times are given, so the 5-year label can be rebuilt ...
