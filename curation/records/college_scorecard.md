---
unique_name: college_scorecard
name: College scorecard
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
tags:
- Non-IID (Temporal)
- '?'
collections:
- TableShift
- TabSTAR
original_source: GOV Website
required_split:
- Temporal (NON-IID)
problem_type: Regression
source_links:
- https://www.openml.org/d/46674
- https://collegescorecard.ed.gov/
- https://tableshift.org/datasets.html#college-scorecard
v2_path: datasets/_dev/tabarena-v0pt2/college_scorecard/dataset.py
source_row: 704
type_adapter_id: curation-record-v1
---

## Comments

Need to figure out real task/target. Binarized version of regression by TableShift.

Data looks good, but the group split is synthetically created and not part of the real task. Real task is just temporal and we have (de facto) data from each institution at time point T. Need to take some more time to look at the data but from the description it sounds taken out of context for the sake of the benchmark (which is fine in general, but not for us where we want to have real tasks!).

**Assessment (AI, 2026-10-07):** OpenML 46674 should not be the source. TableShift's `(C150_4 > 0.5).astype(int)` turns a missing rate into class 0, so roughly 90,000 of its 108,794 negatives have no completion rate, and its features come from the year the rate is reported, six years after the cohort entered. The v2 definition uses the Department of Education's June 2026 files: one row per four-year institution and entering cohort (fall 2001-2018), features from the entry-year file (with the institution's latest published completion and retention rates), target C150_4 from the file six years later, temporal split with a five-cohort label gap. Untuned LightGBM R² 0.80-0.81; the carried-forward rate 0.73-0.76. `colleges` (OpenML 42727) is a one-year Scorecard snapshot with target `percent_pell_grant`.

CC (2026-10-19, Lennart): ship. The Department of Education's files, not OpenML 46674; one row per four-year institution and entering cohort, target C150_4 six files later (regression), the institution's published completion and retention rates as features, cohorts of 30 or more, temporal by cohort with a five-year label gap; SAT math and average converted to the old scale from 2017 on, the reading percentiles left out.
