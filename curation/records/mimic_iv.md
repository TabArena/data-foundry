---
unique_name: mimic_iv
name: MIMIC-IV
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- Needs extensive data wrangling
tags:
- '?'
- 2nd Tier / Scientfic Discovery
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Other
year: '2020'
domain: medical & healthcare
required_split:
- '?'
problem_type: TBD
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://physionet.org/content/mimiciv/
- https://doi.org/10.1038/s41597-022-01899-x
source_row: 798
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 2: a strong, documented clinical database with many real tasks, but it is a relational database with no task of its own. A cohort, target and prediction point have to be defined first, and access is credentialed.
- Source: MIT-LCP on PhysioNet, v1.0 in 2020 (current v3.x). Data paper: Johnson et al. 2023, "MIMIC-IV, a freely accessible electronic health record dataset", Scientific Data 10:1. Beth Israel Deaconess hospital and ICU admissions, 2008-2019 (2008-2022 in v3), in the `hosp` and `icu` modules (admissions, labs, medications, chartevents) plus linked ED and note modules. Many tables join on `subject_id`, `hadm_id` and `stay_id`.
- Use case: the database states none. Established tasks are in-hospital or ICU mortality, length of stay, readmission and decompensation at a fixed hour after admission (benchmark pipelines such as YAIB and the MIMIC-IV extraction benchmarks). Actor: ICU clinicians or bed managers. Fit: direct once one task is fixed. Regime: grouped by patient (repeat admissions), or temporal by anchor year.
- Siblings and duplicates: `icu_length_of_stay_icu_mortality` (TableShift, MIMIC-III via MIMIC-Extract; curator Lennart notes the overlap with a sepsis task), `row_549` (a Kaggle upload claiming MIMIC-III). MIMIC-IV overlaps MIMIC-III in time (2008-2012) for some patients, so one MIMIC task per target. External collections: TableShift (MIMIC-III tasks), YAIB.
- Papers and pages: https://physionet.org/content/mimiciv/ ; Johnson et al. 2023 (doi:10.1038/s41597-022-01899-x).
- Metric: none for the database. Each derived task follows the benchmark that defines it (often AUROC or AUPRC for mortality); otherwise the fallback.
- Risks for /add-dataset: heavy joins and a target to build (`Needs extensive data wrangling`); leakage from charted events after the prediction hour; credentialed access with a data use agreement that bars redistribution (EV-4: noted, not weighed). `Ethical Issue` is dropped: the data is de-identified and released for research, and access terms are no ethical concern under SEL-1.
- Priority: gap - (medical; the regime depends on the task), use case - (none until a task is chosen), source + (PhysioNet and Scientific Data paper), shape + (hundreds of thousands of admissions, mixed types), risk - (joins, target construction, leakage after the prediction point).

MIMIC-IV is the large PhysioNet critical-care relational database (many tables to be joined), supporting real clinical prediction tasks like mortality or readmission. It is a genuine real-world source but requires credentialed access (DUA), substantial wrangling to derive a fixed tabular task, and has patient-privacy/ethical access constraints. The curator is unsure which version/task to use or whether it is even feasible. This is not a drop-in dataset, so TBD -> 2nd Tier. A human must decide the specific cohort/target, handle the credentialing and licensing, define the join/feature pipeline, and choose a patient-grouped split.

---

Another MIMIC dataset. Need to figure out which version(s) to use and how, or if even possible.
