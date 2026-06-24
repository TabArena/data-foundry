---
unique_name: drug_consumption
name: drug_consumption
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
decision_markers:
- No Good Target  / Scientific Discovery
- Ethical Issue
tags:
- 2nd Tier / Scientfic Discovery
- AI-Filled (Verify)
collections:
- TabArena Reject
year: '2015'
domain: social science
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C5TC7S
source_row: 819
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

UCI 'Drug Consumption (quantified)' dataset: ~1885 respondents with Big-Five personality scores plus demographics, used to predict use of each of ~18 drugs (multiple binary/ordinal targets). It is genuine real-world tabular data with a defensible predictive target (per-drug usage), but it was framed as a scientific-discovery study of personality-drug links rather than a single benchmark task, and it is already tagged TabArena Reject / 2nd Tier. The choice of target is ambiguous (18 candidates) and drug-use prediction from personality raises mild ethical/representativeness concerns. A human must pick the actual target used, confirm sample size after dropping near-constant drugs, and weigh the ethical framing before promoting it.

---

CC: ""Predict using demographic and psychological data whether a person uses drugs. 18 Different targets available. Unclear which one used in Talent. Scientific discovery task.

Categorical data made to be numeric by default""

## Reference

The Five Factor Model of personality and evaluation of drug consumption risk
By E. Fehrman, A. Muhammad, E. Mirkes, Vincent Egan, A. Gorban. 2015

Published in Data Science
