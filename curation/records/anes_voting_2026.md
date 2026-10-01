---
unique_name: anes_voting_2026
name: anes_voting_2026
checked_by:
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
decision_markers:
- Needs extensive data wrangling
tags:
- Non-IID (Grouped)
- Non-IID (Temporal)
collections:
- TableShift
original_source: Website
year: '2026'
domain: social science
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://electionstudies.org/data-center/anes-time-series-cumulative-data-file/
- https://tableshift.org/datasets.html#voting
notebook_path: datasets/beyond_iid/temporal/anes_voting_2026/anes_voting_2026.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/anes_voting_2026/dataset.py
source_row: 1029
type_adapter_id: curation-record-v1
---

## Comments

CC (2026-09-30, Lennart): **Leak fixed: VCF1005 is built from the post-election House vote, plus 56 post-election items the "no post IW" filter missed.** Codebook (Feb 5, 2026, VCF1005 "Party of Voter Respondent/ Party of U.S. House Incumbent"): "1. R Voted: R is partisan of same party as incumbent", "2. R Voted: ...", "3. R is major party partisan but R did not vote ...". So codes 1 and 2 exist only for voters (7,517 and 4,780 rows, all voted; filled 1976-2016, empty in 2020 and 2024). The other 56 list "no Post IW" (VCF0426, VCF0427) or "no post data" (54 VCF92xx: CSES module, knowledge items, thermometers, contributions) as a missing code, i.e. post-election interview. All 57 are now dropped. LightGBM mean AUC on the shipped temporal splits (9 test years): 0.930 with everything, 0.859 without VCF1005, 0.855 without all 57 (2020/2024 unchanged at ~0.87). VCF0713 (pre-election vote intent) and VCF9265 (pre-election: voted in the primary) are pre-election and stay.

task: predict voting participation from a detailed questionnaire.

Data: pre-election interview (features) and a post-election interview (target)

This entry refers to the February 5, 2026 version.

## Reference

@dataset{anes_timeseries_cdf_2026,
    author       = {{American National Election Studies}},
    title        = {Time Series Cumulative Data File (1948--2024)},
    year         = {2026},
    month        = feb,
    day          = {5},
    publisher    = {American National Election Studies},
    note         = {Dataset}
    }
