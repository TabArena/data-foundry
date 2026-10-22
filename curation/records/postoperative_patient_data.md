---
unique_name: postoperative_patient_data
name: postoperative_patient_data
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Duplicate
- Too Small
tags:
- AI-Filled (Verify)
original_source: Github
year: '?'
domain: medical & healthcare
required_split:
- '?'
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://github.com/EpistasisLab/pmlb/blob/master/datasets/postoperative_patient_data/metadata.yaml
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`Duplicate`, PROV-4): the PMLB copy of the UCI Post-Operative Patient dataset (DOI 10.24432/C5DG6Q), recorded and rejected by Lennart as `post_operative_patient` ("Too small data (less than 96)").
- Source: UCI Machine Learning Repository, Post-Operative Patient (Summers et al., 1993); PMLB `postoperative_patient_data` re-serves it without its own description ("None yet") with the same eight attributes L-CORE, L-SURF, L-O2, L-BP, SURF-STBL, CORE-STBL, BP-STBL, COMFORT and the discharge decision as the target; 88 to 90 rows.
- Siblings and duplicates: `post_operative_patient` (`No`, `Too Small`, checked by Lennart); the workbook note in this record agrees ("88 samples, too small with 3-fold CV. Lennart: too small. Andrej: too small").
- Metric: not needed for a duplicate.
- Reject check (AI, 2026-10-22): stands. PMLB metadata.yaml (https://github.com/EpistasisLab/pmlb/blob/master/datasets/postoperative_patient_data/metadata.yaml) has the same eight attributes as UCI Post-Operative Patient (https://doi.org/10.24432/C5DG6Q). That source is post_operative_patient, which Lennart checked and rejected ('Too small data (less than 96)'). The 88 vs 90 rows come from PMLB dropping rows with missing values, so it is a processed copy (PROV-4).

The UCI/PMLB post-operative patient dataset (predicting discharge decision) has only 88 samples. Prior TabArena verdict and both Lennart and Andrej flagged it as too small for the 3-fold CV protocol. With under 90 rows it is unsuitable for reliable benchmarking. Suggest No on size grounds.

**Update (policy):** "Too Small" is no longer a rejection reason — dataset size is assessed *after* Data Foundry processing. Re-classified off No to TBD -> 2nd Tier pending that post-DF size check.

---

Imported from the TabArena curation workbook.

TabArena curation verdict: Tiny data.

88 samples,  too small with 3-fold CV.

Lennart: too small

Andrej: too small
