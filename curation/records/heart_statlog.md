---
unique_name: heart_statlog
name: heart_statlog
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Too Small
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

The Heart (Statlog) dataset is a classic UCI heart-disease classification set with only about 270 rows. Prior TabArena curation and both reviewers flagged it as tiny / sample-size. While the task itself (presence of heart disease) is a legitimate medical binary classification, the dataset is too small to be useful for the benchmark. No on the size criterion.

---

Imported from the TabArena curation workbook.

TabArena curation verdict: Tiny data.

Lennart: Sample size

Andrej: Sample size
