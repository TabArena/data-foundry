---
unique_name: census_income
name: Census-Income
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
decision_markers:
- Outdated
- Duplicate
tags:
- 2nd Tier / Scientfic Discovery
- AI-Filled (Verify)
collections:
- TabArena Reject
year: '1995'
domain: social science
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.openml.org/d/4535
- http://www.census.gov/
source_row: 823
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

KDD Census-Income (1994/1995 Current Population Survey), ~300k rows and 41 demographic/employment variables, predicting whether income exceeds a threshold; effectively a larger version of the Adult dataset. It is a genuine, well-defined real-world tabular binary classification, but it is outdated (1990s) and substantially overlaps Adult, and it already sits in the TabArena Reject collection; note the instance-weight column must be excluded to avoid leakage. These overlap/outdated concerns argue against first-tier inclusion rather than against validity. A human should decide on Adult redundancy, confirm the instance-weight handling, and consider whether a newer Census/CPS extract is preferable.

---

CC: "weighted census data extracted from the 1994 and 1995 Current Population Surveys conducted by the U.S. Census Bureau. The data contains 41 demographic and employment related variables. 300k samples. Attention: One of the features is instance weight for stratified sampling - should not be used in prediction. Task is as in adult - this can be seen as a larger version of adult"

Likely outdated or could get newer data.
