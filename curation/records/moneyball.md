---
unique_name: moneyball
name: Moneyball
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
decision_markers:
- No Good Target  / Scientific Discovery
tags:
- 2nd Tier / Scientfic Discovery
- AI-Filled (Verify)
collections:
- TabArena Reject
- TabSTAR
year: '2000'
domain: Other
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/wduckett/moneyball-mlb-stats-19622012/data
- https://www.openml.org/search?type=data&id=41021
source_row: 802
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

The Moneyball MLB stats dataset (1962-2012, OpenML 41021), estimating runs scored from team-season statistics. The curator notes it is clearly an analytics task rather than a predictive-performance task, with a linear model best in TabRepo, and may require a temporal split. It is in TabArena Reject but the curator suggests it could be included to cover the linear-model bias. This is borderline: a real dataset with a clear regression target but weak as a predictive benchmark and likely small. TBD -> 2nd Tier; a human must confirm size, the temporal split, and whether the analytics framing is acceptable.

---

CC: "Baseball dataset that estimates the runs scored. Might be relevant task. Might require temporal split, but need to understand the task better. In general this is clearly not a predictive performance task but an analytics task. Linear model best in TabRepo. Could include to also cover this bias"

## Reference

Kaggle (https://www.kaggle.com/datasets/wduckett/moneyball-mlb-stats-19622012/data), originally from The Analytics Edge course on EdX (https://www.edx.org/learn/analytics/massachusetts-institute-of-technology-the-analytics-edge). Data collected from baseball-reference.com
