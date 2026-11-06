---
unique_name: blood_tests_drink_prediction
name: liver-disorders
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: No (Retired)
decision_markers:
- Outdated
- Not Representative
- Selection Bias
- No Good Target / Scientific Discovery
tags:
- Tiny Data
collections:
- TabArena Reject
original_source: UCI
year: '1990'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.openml.org/d/8
- https://doi.org/10.24432/C54G67
notebook_path: datasets/beyond_iid/new_iid/blood_tests_drink_prediction/blood_tests_drink_prediction.ipynb
source_row: 751
type_adapter_id: curation-record-v1
---

## Comments

need to create the drinks column as a target, need to see if it is still a good task then. (drinks>5) otherwise, we can just treat it as a regression task...

Unclear if the target makes for a relevant, real-world dataset but for now we can add it and filter later again (which might happen)

Discussion: Task is to predict no. of drinks a person consumes as a proxy for liver diseases based on blood tests. This is not a meaningful task, e.g., what kind of decision would it motivate? If a doctor has the time to collect blood samples, asking for drinking behavior is simple.
Also, there is selection bias as almost only drinking people (336/345) and only males are in the sample.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback rmse — The source frames a classification of liver disorder (the selector column was misread as the label); McDermott & Forsyth say the intended label is drinks dichotomised, with no metric for a regression on the count. Our regression on drinks is our own task, so the regression fallback applies.

**Assessment (AI, 2026-10-21):** metric now `Metric.from_context("rmsle", target_transform="log1p")` instead of the fallback rmse on the log1p target: drinks per day is a right-skewed count whose error matters relative to the amount; the target still ships as log1p, and RMSLE is computed after the inverse, on the original scale (MET-3). Needs a rebuild to reach the container.

CC (2026-10-21, Lennart): ship the target on the modelling scale, score on the original scale (target_transform).

**Assessment (AI, 2026-10-27):** The open questions for the curator are in the folder's `REVIEW.md` (review of the Tiny Data datasets, written from the earlier findings, no review panel); the AI recommends shipping it. Priority 1: gap -, use case - (written by the curators), source +, shape -, risk - (undocumented label origin; `Trivial` untested).
**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `nhanes_alcohol_drinks_from_blood_tests` (TBD -> 2nd Tier, priority 2). Each is screened in its own record; this record's verdict stays the curator's.

**Assessment (AI, 2026-11-04):** reviewed for the BeyondArena v0.2 review page, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the folder's `REVIEW.md`. Keep with changes: the source's own task (drinks from blood markers) with a weak but real signal; drop the four records entered twice (a lookup of the copies beats every benchmark method) and remove the refuted Trivial marker. Priority 1: gap 0, use case 0, source 1, shape 0, risk -1.

CC (2026-11-05, Andrej): retired (`No (Retired)`, `No Good Target / Scientific Discovery`): no decision rests on the prediction. The data is the BUPA liver-disorders file (UCI, 1990): 345 men, five blood tests that respond to alcohol, and the number of drinks per day each reported.
- **As a stand-in for liver damage it fails:** the file was framed as a test for liver disorders with the drinks as a proxy (McDermott & Forsyth 2016: the intended label is the drinks, cut into two classes), but a drink count is not a measure of damage, and the blood tests themselves are the better measure.
- **As the definition's use case it leads to nothing:** the definition reads it as checking a patient's account of drinking from blood markers; once a doctor has the blood values, those values guide what happens next, and an estimate of the drinks adds nothing to act on (asking is simpler).
- **The sample would not carry over:** men only, 336 of 345 drink, and how the drinks were recorded is not stated.
Not changed: `Trivial` stays for now (open on the review page: the single-feature test refuted it, skill +0.05 against +0.10 to +0.17 for the methods). Had the dataset stayed, the four records entered twice would have been dropped.

CC (2026-11-10, Andrej): `Trivial` removed (review page issue 2, B): the test refuted it; the best single feature reaches skill +0.05 against +0.10 to +0.17 for every method configuration. The retirement's reasons stand.

## Reference

@book{forsyth1986machine,
  title={Machine learning: applications in expert systems and information retrieval},
  author={Forsyth, Richard and Rada, Roy},
  year={1986},
  publisher={Halsted Press}
}
