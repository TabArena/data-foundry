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
- Non-IID (Temporal)
- 'Samples: Over Time'
- 'Time: Dated'
- 'Target: Later'
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

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — ANES (the data's first publication) defines no prediction task. TableShift (Gardner et al. 2023), which defined the voting task, scores accuracy for every task of its benchmark, a house convention, not a choice from the decision; our task differs (temporal year splits, pre-election items only) and 78% voted, so accuracy at 0.5 is coarse. Original rejected: TableShift accuracy. roc_auc is the binary fallback.

CC (2026-10-21, Lennart): metric: the fallback (roc_auc), not TableShift's accuracy.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): 71 ordinal scales typed as ordered categories in the codebook's order (CLEAN-14, amended): `VCF0110`, `VCF0111`, `VCF0114`, `VCF0130a`, `VCF0138`, `VCF0140`, `VCF0140a`, `VCF0301`, `VCF0303`, `VCF0305`, `VCF0310`, `VCF0311` and 59 more (the README lists their levels); their codes that mean unknown (don't know, refused, not asked) are missing in `VCF0110`, `VCF0111`, `VCF0114`, `VCF0130a`, `VCF0138`, `VCF0140`, `VCF0140a`, `VCF0301`, `VCF0303`, `VCF0305`, `VCF0310`, `VCF0311` and 59 more (CLEAN-10); 20 counts and indices stored as text are numbers: `VCF0138a`, `VCF0138b`, `VCF0138c`, `VCF0138d`, `VCF0316`, `VCF0317`, `VCF0320`, `VCF0321`, `VCF0322`, `VCF0323`, `VCF0324`, `VCF0403` and 8 more; left unordered: `VCF0130` (a level outside the scale is a state of its own); `VCF0137` (a partial order); `VCF0148` (a partial order); `VCF0148a` (a partial order); `VCF0149` (a partial order); `VCF0155` (a level outside the scale is a state of its own); `VCF9002` (a level outside the scale is a state of its own); `VCF9044` (a partial order); `VCF9266` (a level outside the scale is a state of its own); ordinal scales shipped as numbers, left as numbers for the curator's review: `VCF0102`, `VCF0103`; codes shipped as numbers, left for the curator's review: `VCF0104`.

CC (2026-10-31, Lennart): marks on the review board of PR #37 (ordinal scales in the codebook's order, also when shipped as numbers; a state outside a scale missing when the column has no other missing value, else the lowest level; cycles ordered; codes shipped as numbers as categories): 2 ordinal scales shipped as numbers are ordered categories (point 3); 4 columns with a state outside the scale ordered, the state placed by the rule.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `ces_validated_turnout` (TBD -> Yes, priority 3). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-01, Lennart): the decode rule (a code whose codebook says in words what each level is carries the words; a score without them is a number): 157 coded columns carry their words; 12 scores are numbers (VCF0834, VCF0839, VCF0842, VCF0843, VCF9073, VCF9077, VCF9081, VCF9085 and more); codes that only mean unknown are missing in the unordered codes too; VCF0130's 0 (not ascertained or not asked) missing; age 0 and the thermometers' DK/NA codes missing; open calls on the review board's ANES sheet.

CC (2026-11-01, Lennart): on the review board's ANES sheet: read 2024's attendance 9 as never (except the short form), recover 2020's VCF0130a never from VCF0130, "all of life" as the respondent's age (VCF9001 a number, VCF9002 by age band), decode the 40 master-code columns; the mention counts' 0 left as it is.

CC (2026-11-01, Lennart): the target rule (CLEAN-25) and the cut-end rule (CLEAN-14): the target ships as No/Yes, Yes the event (2 means voted (ANES codebook)); counts with a cut end are numbers: VCF0138, VCF9122.

CC (2026-11-01, Lennart): counts with a cut end stay ordered categories of the source's levels, the cut end a level of its own (CLEAN-14): the lossless form, chosen from the context rather than by model runs; the same day's numbers with censoring flags are reverted.

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
