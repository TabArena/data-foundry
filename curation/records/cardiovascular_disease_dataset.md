---
unique_name: cardiovascular_disease_dataset
name: Cardiovascular-Disease-dataset
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Data Quality Issue
- Missing source information
tags:
- 2nd Tier / Scientfic Discovery
- AI-Filled (Verify)
collections:
- New (BeyondArena)
- TabSTAR
- TabArena Reject
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/sulianova/cardiovascular-disease-dataset
- https://www.openml.org/search?type=data&id=45547&sort=runs&status=active
source_row: 828
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

Popular Kaggle/OpenML cardiovascular-disease dataset (predict presence of cardiovascular disease from clinical/examination features). Although widely used, the record and curation notes flag that the data source is unknown, the data may be synthetic, and there are documented quality issues (outliers, implausible values), and it is already in the TabArena Reject collection. Missing provenance plus credible suspicion of synthetic/dirty data make it unsuitable. A human could re-check the discussion threads, but the existing markers (Data Quality Issue, Missing source information) support rejection.

---

CC: ""Source of data is missing. Unclear if real data or not

it is used a lot, also in papers

Various concerns about data quality issues: https://www.kaggle.com/datasets/sulianova/cardiovascular-disease-dataset/discussion/451915
Also see TabArena comments on it""
CC: ""Uploaded by Matthias Feurer - not much information; from Kaggle, seems like a real task without much more information

At the same time see the Kaggle discussions no one knows the source and it might be synthetic data due to outliers. Remove due to missing source information""
