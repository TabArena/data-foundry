---
unique_name: optn_liver_waitlist_90day_mortality
name: 'OPTN STAR files / SRTR Standard Analysis Files: liver transplant waiting list, 90-day waitlist mortality'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
decision_markers:
- Needs extensive data wrangling
tags:
- Non-IID (Temporal)
- AI-Filled (Verify)
original_source: GOV Website
domain: medical & healthcare
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://srtr.hrsa.gov/requesting-data/about-srtr-standard-analysis-files-safs/
- https://srtr.hrsa.gov/requesting-data/data-requests/
- https://doi.org/10.1053/j.gastro.2021.08.050
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: the US liver waiting list (OPTN registry) with death or removal as too sick within 90 days of listing, the endpoint MELD ranks candidates by for allocation; a strong source and use case, but transplant censors the label and the files come by request with a fee and a data use agreement.
- Record fix: the run merged two hits that share the SRTR link. This record (by its `unique_name`) is the liver waitlist task of scout_20, found for `hepatitis_survival_prediction`; the title and size it carried ("SRTR / OPTN heart transplant recipients: 1-year post-transplant mortality", 50,356 recipients 2000-2022) belong to the hit from the curator's Zotero collection, item 267 (alias `srtr_heart_transplant_1yr_mortality`: Pigot et al., arXiv 2609.07610, "Translation of Black-Box Clinical Prediction Models into Standalone Transparent Nomograms: Temporal External Validation in Heart Transplantation"; the IMPACT score, doi 10.1016/j.athoracsur.2011.04.030; github.com/AIBCTS/PRiSM). The name now names the liver task, and those three links moved from `source_links` into this line. The heart task is a distinct task on the same registry (PROV-7) and needs its own record.
- Source: the OPTN registry, served as the OPTN STAR files and as the SRTR Standard Analysis Files: "many of the data elements collected by OPTN on all solid organ transplant candidates, donors, and recipients", "from 1987 to the present", candidate files with "status history and status justification", "currently available only in SAS format", released quarterly, $1,000 for a standard SAF (SRTR SAF page, read 2026-10-31). The task as published: Kim et al., "MELD 3.0: The Model for End-Stage Liver Disease Updated for the Modern Era", Gastroenterology 161(6):1887-1895 (2021; PMC8608337, Methods read): OPTN STAR files as of 03/15/2019, 29,410 adults newly waitlisted for a primary liver transplant in 2016-2018, split 70:30 into development (20,587) and validation (8,823), a 2019 cohort for temporal validation; outcome survival to 90 days from registration, with waitlist mortality "removal from the waitlist for death or being too sick", censored at transplant or other removal; candidate inputs age, sex, race, sodium, creatinine, INR, bilirubin, albumin and height.
- Use case: at listing and at each update, the allocation system ranks liver candidates by predicted 90-day mortality without transplant (MELD) and hepatologists decide listing and priority (MELD 3.0 Methods: the model "consider[s] survival probability without transplant", which suits ranking by mortality risk); fit direct; regime temporal, because registrations are dated and allocation policy and practice change (the paper validates on the later 2019 cohort).
- Siblings and duplicates: `hepatitis_survival_prediction` (`Yes`, 155 patients, UCI 1988) and `cirrhosis_patient_survival_prediction` (`Yes`, the Mayo PBC trial) are small chronic liver disease survival sets of another population, not end-stage transplant candidates; `optn_kidney_delayed_graft_function` (unscreened) names the same SAFs for a kidney task; `transplant` (`No`) is unrelated hospital counts. No other OPTN or SRTR liver record (grep: srtr, optn, meld). External collections: none found.
- Better data: found as better data for `hepatitis_survival_prediction`; no further search this round.
- Papers and pages: Kim et al. 2021 above; the earlier MELD and MELD-Na fits of the same endpoint were not read (the web search budget was used up).
- Metric: Harrell's concordance (c) statistic of 90-day survival, with Uno's c (MELD 3.0, Methods, Data Analysis: discrimination "evaluated using the concordance (c) statistic"; 0.869 against 0.862 for MELD-Na), the paper's discrimination criterion next to reclassification and an allocation simulation. On a binary 90-day label the matching metric is `roc_auc` (MET-5, MET-8); inputs none for a binary label.
- Risks for /add-dataset: a transplant within 90 days censors the label, and the sickest candidates are transplanted first, so a binary target needs a stated rule for censored candidates (drop them, count removal for any reason, or a competing-risk framing), and the choice changes what is predicted (USE-5, LEAK-22 to LEAK-26); exception points and status updates after listing stay out of the features (USE-3); the label is built from the status-history tables (joins); access by request (the SRTR SAF fee and approval; the OPTN STAR request page returned 403 to the scout) and no redistribution per the scout (noted only, EV-4).
- Priority: gap 0 (medical, binary and temporal not thin), use case + (allocation by 90-day mortality), source + (national registry with a data dictionary, the MELD 3.0 paper), shape + (29,410 eligible adults in three years in MELD 3.0 alone, labs, demographics and diagnosis, dated), risk - (censoring by transplant, request-only access, a label built from status history).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `hepatitis_survival_prediction`; the curator's Zotero collection, item 267: "Translation of Black-Box Clinical Prediction Models into Standalone Transparent ...".
- as published: one row per adult isolated heart transplant. The paper has 50,356 recipients from 2000-2022 (32,543 / 8,558 / 9,255 by era; 1,081 without full follow-up dropped), drawing 22 predictors from 1,293 ...; target: all-cause death within 365 days of transplant (binary, 10.0%); access: request.
- Why: Large national registry with a hard outcome and mixed-type predictors known at transplant. A recognised clinical prediction task with a published score to compare against. There is a natural temporal split, with a documented shift after the 2018 UNOS allocation change. | the same quantity as ...
- Adds: A transplant-outcome task at registry scale; the existing transplant records are small OpenML or UCI sets. Access (checked 2026-10-31): SRTR SAF by application ($1,000 first SAF, $500 updates, SAS, quarterly) or OPTN STAR file ($0 with a DUA; hrsa.gov pages 403 to automated fetches). Redistribution is barred: a ...

**Assessment (AI, 2026-10-31):** cleanup flag of the data-scouting run: the run merged an SRTR heart-transplant hit into this record; its links moved to the comments, and it needs its own record (`srtr_heart_transplant_1yr_mortality`).
