---
unique_name: anes_voting_2026
name: anes_voting_2026
checked_by:
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 3
decision_markers:
- Needs extensive data wrangling
tags:
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

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — ANES (the data's first publication) defines no prediction task. TableShift (Gardner et al. 2023), which defined the voting task, scores accuracy for every task of its benchmark, a house convention, not a choice from the decision; our task differs (temporal year splits, pre-election items only) and 78% voted, so accuracy at 0.5 is coarse. Original rejected: TableShift accuracy. roc_auc is the binary fallback.

CC (2026-10-21, Lennart): metric: the fallback (roc_auc), not TableShift's accuracy.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): 71 ordinal scales typed as ordered categories in the codebook's order (CLEAN-14, amended): `VCF0110`, `VCF0111`, `VCF0114`, `VCF0130a`, `VCF0138`, `VCF0140`, `VCF0140a`, `VCF0301`, `VCF0303`, `VCF0305`, `VCF0310`, `VCF0311` and 59 more (the README lists their levels); their codes that mean unknown (don't know, refused, not asked) are missing in `VCF0110`, `VCF0111`, `VCF0114`, `VCF0130a`, `VCF0138`, `VCF0140`, `VCF0140a`, `VCF0301`, `VCF0303`, `VCF0305`, `VCF0310`, `VCF0311` and 59 more (CLEAN-10); 20 counts and indices stored as text are numbers: `VCF0138a`, `VCF0138b`, `VCF0138c`, `VCF0138d`, `VCF0316`, `VCF0317`, `VCF0320`, `VCF0321`, `VCF0322`, `VCF0323`, `VCF0324`, `VCF0403` and 8 more; left unordered: `VCF0130` (a level outside the scale is a state of its own); `VCF0137` (a partial order); `VCF0148` (a partial order); `VCF0148a` (a partial order); `VCF0149` (a partial order); `VCF0155` (a level outside the scale is a state of its own); `VCF9002` (a level outside the scale is a state of its own); `VCF9044` (a partial order); `VCF9266` (a level outside the scale is a state of its own); ordinal scales shipped as numbers, left as numbers for the curator's review: `VCF0102`, `VCF0103`; codes shipped as numbers, left for the curator's review: `VCF0104`.

CC (2026-10-31, Lennart): marks on the review board of PR #37 (ordinal scales in the codebook's order, also when shipped as numbers; a state outside a scale missing when the column has no other missing value, else the lowest level; cycles ordered; codes shipped as numbers as categories): 2 ordinal scales shipped as numbers are ordered categories (point 3); 4 columns with a state outside the scale ordered, the state placed by the rule.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `ces_validated_turnout` (TBD -> Yes, priority 3). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-01, Lennart): the decode rule (a code whose codebook says in words what each level is carries the words; a score without them is a number): 157 coded columns carry their words; 12 scores are numbers (VCF0834, VCF0839, VCF0842, VCF0843, VCF9073, VCF9077, VCF9081, VCF9085 and more); codes that only mean unknown are missing in the unordered codes too; VCF0130's 0 (not ascertained or not asked) missing; age 0 and the thermometers' DK/NA codes missing; open calls on the review board's ANES sheet.

CC (2026-11-01, Lennart): on the review board's ANES sheet: read 2024's attendance 9 as never (except the short form), recover 2020's VCF0130a never from VCF0130, "all of life" as the respondent's age (VCF9001 a number, VCF9002 by age band), decode the 40 master-code columns; the mention counts' 0 left as it is.

CC (2026-11-01, Lennart): the target rule (CLEAN-25) and the cut-end rule (CLEAN-14): the target ships as No/Yes, Yes the event (2 means voted (ANES codebook)); counts with a cut end are numbers: VCF0138, VCF9122.

CC (2026-11-01, Lennart): counts with a cut end stay ordered categories of the source's levels, the cut end a level of its own (CLEAN-14): the lossless form, chosen from the context rather than by model runs; the same day's numbers with censoring flags are reverted.

**Assessment (AI, 2026-11-06):** review panel (focused, re-review under LEAK-41, MET-14 to MET-16): ship after changes, made: the survey-weight note now names the measured outcome-linked selection (MET-16: weighting by `VCF0009z` lowers the share who say they voted in 8 of the 9 test years, by 2 to 9 points; scored unweighted, weighting the AUC moves it by +0.004 to +0.005); disputed: none; for the curator: no issue (optional follow-up: quote the codebook's `VCF0009z` entry, EV-2).

**Assessment (AI, 2026-11-06):** priority 3 (selection.md, Priority): a good shape (48,587 units, 261 features, temporal) +, a strong source (the ANES cumulative file and its codebook) +; no gap in the benchmark; the use case is the curation's (a pollster's likely-voter screen), so it does not count; no open issue.

CC (2026-11-08, Lennart): the declared metric (`roc_auc`) is checked, as declared; the record ships, with no open issue on the PR #47 review board.

CC (2026-11-11, Lennart): REVIEW issue 1 (which election years to test), as implemented (A): the nine studies 1996 to 2024 stay the test windows, in place of the AI's proposal of the five elections 2008 to 2024; SPLIT-14 as amended on 2026-11-11 admits the four oldest, which train on 49.2%, 46.4%, 43.2% and 40.0% of the respondents (four windows under half, not more than the five at or above it), and nine is the count a random split of this size gets.

CC (2026-11-11, Lennart): the declared horizon (one study, no gap, windows starting 2024, 2020, 2016, 2012, 2008, 2004, 2002, 2000 and 1996) is checked, as a pollster builds a likely-voter screen from the elections already studied and applies it at the next one, so each window is one election and its model up to four years old.

**Assessment (AI, 2026-11-11):** applied in dataset.py: `temporal` unchanged (`window=1, unit="unique", n_windows=9`); test 4,954, 7,442, 3,648, 5,488, 2,102, 1,066, 1,344, 1,554 and 1,534 respondents (2024 to 1996, 29,132 in all), train 43,633, 36,191, 32,543, 27,055, 24,953, 23,887, 22,543, 20,989 and 19,455 (89.8%, 74.5%, 67.0%, 55.7%, 51.4%, 49.2%, 46.4%, 43.2%, 40.0% of 48,587). `task_summary.split` and `splits_comment` now name the nine windows, the four under half with their shares, the length's reason (one election, the test Pew's likely-voter study names; no source sets a length) and why no gap is needed. `dataset check`: 0 errors, 0 warnings (README not regenerated).

CC (2026-11-11, Lennart): accepted `splits_feature_missing_in_test` with a note naming the columns (cross-dataset item "Accept splits_feature_missing_in_test where a column starts or stops being recorded within the history?", A: the data as the deployed model met it).

**Assessment (AI, 2026-11-11):** 95 questions flagged, each missing in at least one test election and recorded on its train side (e.g. VCF0401-VCF0411 last asked in 2004).

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
