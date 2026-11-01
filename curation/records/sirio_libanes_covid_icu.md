---
unique_name: sirio_libanes_covid_icu
name: COVID-19 clinical data to predict ICU admission (Hospital Sirio-Libanes, Kaggle)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
- Tiny Data
original_source: Kaggle
year: '2020'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/S%C3%ADrio-Libanes/covid19
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: a hospital's own release of 385 COVID-19 admissions (Hospital Sírio-Libanês, São Paulo and Brasília, 2020) with vitals and labs in five windows after admission and ICU admission as the target; a named decision, but tiny, one pandemic wave, and scaled over all rows by the publisher.
- Source: the Sírio-Libanês Data Intelligence Team, "COVID-19 - Clinical Data to assess diagnosis", Kaggle (first published there in 2020; Kaggle metadata read: CC BY-NC 4.0, 9,282 downloads). As published (the run's note; the file was not opened): one xlsx, 1,925 rows = 385 patients x 5 windows (0-2, 2-4, 4-6, 6-12 and above 12 hours from admission), 231 columns: 3 demographic, 9 grouped prior diseases, 36 blood results and 6 vital signs, expanded to mean, median, max, min, diff and relative diff; target `ICU`. The page: "Data has been cleaned and scaled by column according to Min Max Scaler to fit between -1 and 1", and "Beware NOT to use the data when the target variable is present, as it is unknown the order of the event (maybe the target event happened before the results were obtained)".
- Use case: the page's Task 01, "Predict admission to the ICU of confirmed COVID-19 cases ... so ICU resources can be arranged or patient transfer can be scheduled", with the advice that "a nice model using only the first (0-2) is likely to be more clinically relevant": a hospital decides at admission on ICU beds and transfers. Fit direct for the first window. Regime IID with one row per patient (the 0-2 h window, patients already in the ICU in it dropped); no admission dates ship.
- Siblings and duplicates: `curial_covid_ed_triage` (`TBD -> Yes`, priority 3, COVID-19 triage in Oxford emergency departments, another source and task); `vitaldb_postoperative_icu_admission` (another ICU-admission task). No other record of this release (grep: sirio, libanes, covid). External collections: none known.
- Better data: from the curator's Zotero collection (item 55); no further search this round.
- Papers and pages: the Kaggle page (tasks, window concept, tips); "Comparison of Imputation Strategies for Incomplete Electronic Health Data", medRxiv 2025, https://doi.org/10.1101/2025.08.01.25332573 (uses it; not read; moved here from source_links as related work, PROV-12).
- Metric: none: the page asks for a notebook and names no metric, so the fallback `roc_auc` (MET-1, MET-8); inputs none.
- Risks for /add-dataset: drop windows at and after the ICU transfer (the publisher's instruction) and decide whether the task is the first window only; the min-max scaling over all rows is a weak transductive leak, kept with a note (LEAK-30), and the original units cannot be recovered (PROV-13); many values are missing, and the page's tip to fill them from neighbouring windows would carry later windows into the first (LEAK); the patient identifier is a group id, never a feature; 385 patients is `Tiny Data`.
- Priority: gap 0 (medical and binary covered), use case + (the publisher names the actor and the decision), source + (the hospital's own documented release), shape 0 (385 patients), risk - (the target may precede the measurements of its window; values scaled over all rows).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 55: "Comparison of Imputation Strategies for Incomplete Electronic Health Data".
- as published: patient windows: 1,925 rows = 385 patients x 5 time windows after admission, 231 columns (demographics, disease groups, vitals and labs with mean/median/min/max/diff); one xlsx, 1.0 MB, 2020-06-22; target: ICU admission (ICU column); access: registration.
- Why: A real hospital-released table with a clear operational target, used in the item. Small and from one 2020 COVID wave.
- Adds: No record. Low priority: 385 patients, one hospital, pandemic-era. The rows after the ICU transfer must be dropped (the publisher's own instruction).
