---
unique_name: heart_statlog
name: heart_statlog
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Duplicate
tags:
- AI-Filled (Verify)
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`Duplicate`, PROV-6): Statlog (Heart) is a 270-row cut of the Cleveland heart-disease data, which ships as `heart_disease_cleveland` (Lennart, `Yes`); the workbook's reject (Lennart, Andrej: sample size) points the same way, for another reason.
- Source: UCI 145 "Statlog (Heart)", DOI 10.24432/C57303, from the StatLog project; UCI: "This dataset is a heart disease database similar to a database already present in the repository (Heart Disease databases) but in a slightly different form"; `heart.doc`: "13 attributes (which have been extracted from a larger set of 75)", "Absence (1) or presence (2) of heart disease", "270 observations", and a cost matrix (a missed disease costs 5, a false alarm 1).
- Measured (2026-10-22, the two small UCI files): all 270 rows of `heart.dat` match a row of `processed.cleveland.data` (297 rows without missing values) on all 13 features, and all 270 labels agree (Statlog 2 = Cleveland num > 0). So it is a subset of `heart_disease_cleveland` with the binary target we already ship.
- Does the cost matrix make it a distinct task (PROV-7)? No: the same target, units and features; the matrix is a metric that `heart_disease_cleveland` could adopt (MET-6, MET-7), noted there if the curator wants it.
- On `Too Small`: 270 rows with 120 positives is not a handful per fold (TP-5); the old marker would not hold by itself.
- External collections: OpenML 53 (heart-statlog), PMLB, many benchmark suites.
- Reject check (AI, 2026-10-22): stands. PROV-6, by measurement (re-run 2026-10-22): all 270 rows of UCI heart.dat equal a row of processed.cleveland.data (297 complete rows) on all 13 features and all 270 labels agree (2 = num>0); UCI: "similar to a database already present in the repository ... in a slightly different form" (https://archive.ics.uci.edu/dataset/145/statlog+heart). heart_disease_cleveland ships (Yes). The cost matrix is a metric, not a distinct task (PROV-7 does not apply).

The Heart (Statlog) dataset is a classic UCI heart-disease classification set with only about 270 rows. Prior TabArena curation and both reviewers flagged it as tiny / sample-size. While the task itself (presence of heart disease) is a legitimate medical binary classification, the dataset is too small to be useful for the benchmark. No on the size criterion.

**Update (policy):** "Too Small" is no longer a rejection reason — dataset size is assessed *after* Data Foundry processing. Re-classified off No to TBD -> 2nd Tier pending that post-DF size check.

---

Imported from the TabArena curation workbook.

TabArena curation verdict: Tiny data.

Lennart: Sample size

Andrej: Sample size
