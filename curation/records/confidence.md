---
unique_name: confidence
name: confidence
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Too Small
tags:
- AI-Filled (Verify)
original_source: Github
year: '?'
domain: Other
required_split:
- '?'
problem_type: Regression
original_data_state: One Table
source_links:
- https://github.com/EpistasisLab/pmlb/blob/master/datasets/confidence/metadata.yaml
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

PMLB 'confidence' dataset with only 72 samples. Both the prior TabArena verdict and the two named reviewers (Lennart, Andrej) flagged it as too small, and 72 rows is far below what the benchmark's CV protocol can support. There is no path to making this representative at that size. Reject on size; no further verification needed.

---

Imported from the TabArena curation workbook.

TabArena curation verdict: Tiny data.

72 samples,  too small with 3-fold CV.

Lennart: too small

Andrej: too small
