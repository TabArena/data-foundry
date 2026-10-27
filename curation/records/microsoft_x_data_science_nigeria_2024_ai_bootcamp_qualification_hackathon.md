---
unique_name: microsoft_x_data_science_nigeria_2024_ai_bootcamp_qualification_hackathon
name: microsoft-x-data-science-nigeria-2024-ai-bootcamp-qualification-hackathon
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- TBD
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2024'
domain: medical & healthcare
required_split:
- '?'
problem_type: Binary Classification
source_links:
- https://zindi.africa/competitions/microsoft-x-data-science-nigeria-2024-ai-bootcamp-qualification-hackathon
source_row: 968
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 1: a heart-disease binary task for a training hackathon, about 10k rows of undocumented origin, re-run from a 2023 DSN hackathon.
- Source: Zindi, "Data Science Nigeria X Microsoft 2024 AI Bootcamp Qualification Hackathon", 16-30 September 2024, subtitle "Heart Disease prediction for the DSN AI Bootcamp 2024" (Zindi API). Data page: "There are ~7000 entries in Train and ~3000 entries in Test". Files: `Train Dataset .csv` (317,864 bytes), `Test Dataset.csv` (111,997 bytes), `Variable_Definitions.csv` (470 bytes), so about a dozen short columns. The API names as parent "DSN AI Bootcamp 2023 Mr and Miss Algorithm Hackathon" (August 2023), which has the same description, a 470-byte Variable Definitions file and a Train.csv of 308,417 bytes: the same data, re-split. The origin of the patient records is not stated (Zindi pages, DSN community posts searched); it is probably a public heart-disease table re-uploaded. The columns were not read (login needed).
- Use case: "determining the likelihood of an individual having heart disease ... utilizing easily accessible patient information" for early detection. No actor or moment is named. Fit: approximate. Regime: likely IID (one row per person); unknown until the columns are read.
- Siblings and duplicates: no record for the 2023 parent hackathon. The other DSN records (`dsn_ai_bootcamp_qualification_hackathon_by_data_science_nigeria`, a loan-default task; `dsn_free_ai_classes_in_every_city_2025`, a retail-sales task) are different data. Check against the heart records (`heart_disease*`, `heart_failure*`, `framingham_heart_study_fhs`) and the public 70k cardiovascular or BRFSS heart tables once the columns are known (PROV-4).
- Papers and pages: the Zindi page only; no top solutions found.
- Metric: accuracy ("The error metric for this competition is Accuracy"; API `straight_accuracy`), submitted as hard 0/1 labels. A leaderboard metric (MET-4), but a threshold metric with no stated cost or threshold (MET-6), so the fallback may be preferable. Inputs: none.
- Risks for /add-dataset: unknown origin of the rows (PROV-2: the competition is the source to point to) and a likely duplicate of a known heart dataset (PROV-4). Possibly SEL-7 if the label is a self-reported diagnosis.
- Priority: gap - (medical, binary: not thin), use case - (no actor named), source - (origin undocumented), shape + (about 10k rows), risk - (likely re-upload); floor 1.

A 2024 Zindi qualification hackathon (Data Science Nigeria x Microsoft) with no description in the record beyond the link. Zindi qualification hackathons are typically standard tabular classification/regression tasks, which would be in scope, but the subject matter and target are unknown. There is too little information to reject, so per the heuristics this is a TBD rather than a No. A human must open the competition to identify the actual task, target, problem type, domain, size, and required split before a final verdict.
