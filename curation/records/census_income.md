---
unique_name: census_income
name: Census-Income
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target  / Scientific Discovery
- Outdated
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

**Screening (AI, 2026-10-22):** `No` (`No Good Target  / Scientific Discovery`, SEL-3): the same income-above-50K task as `adult`, which the curator rejected because no actor decides on it; census survey data binarised by the donor.
- Source: UCI "Census-Income (KDD)" (dataset 117), donated 2000-03-06 (record year 1995 is the survey year; the first publication is 2000, PROV-9): "weighted census data extracted from the 1994 and 1995 current population surveys conducted by the U.S. Census Bureau"; 299,285 rows (199,523 train, 99,762 test), 41 demographic and employment variables; income "binned at $50K" to make a binary problem, from total person income, unlike Adult's.
- Use case: none named by the source; the CC on this record: "Task is as in adult - this can be seen as a larger version of adult"; the curator on `adult`: "Not a meaningful task ... label is wrong, higher/lower 50k is not relevant in such settings". Regime IID.
- Siblings and duplicates: `adult` (`No`, curator CC, TabArena Reject; today's AI assessment there also notes this record is another CPS extract, not a copy). `Duplicate` does not fit (different survey years, rows and variables; PROV-4) and should be dropped; `Outdated` stays (1994-95 data; Folktables ACSIncome is the modern rebuild, no record yet). Already in the TabArena Reject collection.
- Papers and pages: the UCI page lists two GAN papers (Xu & Veeramachaneni 2018) that used it, no task paper.
- Metric: none found on the UCI page, so the fallback would apply (MET-1, MET-11).
- Risks noted for the record: the instance weight "should *not* be used in the classifiers" (UCI).
- Reject check (AI, 2026-10-22): stands. SEL-3 by treat-alike: the record's own CC says 'Task is as in adult - this can be seen as a larger version of adult', and the curators' CC on adult rejects that task ('label is wrong, higher/lower 50k is not relevant in such settings'); UCI 117 bins total person income 'at $50K' from 1994-95 CPS (https://archive.ics.uci.edu/dataset/117/census+income+kdd). No other use case in the source. Agree to drop Duplicate (different CPS extract, PROV-4) and keep Outdated.

KDD Census-Income (1994/1995 Current Population Survey), ~300k rows and 41 demographic/employment variables, predicting whether income exceeds a threshold; effectively a larger version of the Adult dataset. It is a genuine, well-defined real-world tabular binary classification, but it is outdated (1990s) and substantially overlaps Adult, and it already sits in the TabArena Reject collection; note the instance-weight column must be excluded to avoid leakage. These overlap/outdated concerns argue against first-tier inclusion rather than against validity. A human should decide on Adult redundancy, confirm the instance-weight handling, and consider whether a newer Census/CPS extract is preferable.

---

CC: "weighted census data extracted from the 1994 and 1995 Current Population Surveys conducted by the U.S. Census Bureau. The data contains 41 demographic and employment related variables. 300k samples. Attention: One of the features is instance weight for stratified sampling - should not be used in prediction. Task is as in adult - this can be seen as a larger version of adult"

Likely outdated or could get newer data.
