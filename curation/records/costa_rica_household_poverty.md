---
unique_name: costa_rica_household_poverty
name: Costa Rican Household Poverty Level Prediction
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
original_source: Kaggle
year: '2018'
domain: social science
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/competitions/costa-rican-household-poverty-prediction
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: the IDB's Kaggle task to improve the proxy means test that qualifies poor households for aid, four ordinal poverty levels from Costa Rican household attributes, scored by macro F1 on heads of household; only about 3,000 households are labelled, and the survey behind it is not named.
- Source: Kaggle competition "Costa Rican Household Poverty Level Prediction" (2018-07-18 to 2018-09-19, 616 teams, kernels only; the rules name Kaggle as sponsor, the Description the Inter-American Development Bank). Files (Kaggle API): train.csv 3.2 MB with the Target, test.csv 8.0 MB without, codebook.csv. Data page: "One row represents one person in our data sample. Multiple people can be part of a single household. Only predictions for heads of household are scored"; "This data contains 142 total columns"; Target "an ordinal variable indicating groups of income levels. 1 = extreme poverty 2 = moderate poverty 3 = vulnerable households 4 = non vulnerable households"; `idhogar` the household, `parentesco1` the head; columns on rent, overcrowding, wall, floor and roof materials, water, assets, household composition and schooling. The row counts (about 9,557 people in about 2,988 households in train) are the scout's, not read.
- Use case: a social programme that cannot verify incomes classifies a household's need from observable attributes (the proxy means test) to decide who receives aid; the Description: "agencies use a model that considers a family's observable household attributes like the material of their walls and ceiling, or the assets found in the home to classify them and predict their level of need". Fit direct. Regime: the unit is the household; one row per head of household is IID over households, or individuals grouped by `idhogar` (to decide).
- Siblings and duplicates: `economic_well_being_prediction_challenge` (`TBD -> Yes`, 3; Zindi, African survey clusters, a wealth index), `womxn_in_big_data_south_africa_female_headed_households_in_south_africa` and `financial_inclusion_in_africa_for_botswana`: other countries and targets, no duplicate (searched Costa Rica, poverty, proxy means). External collections: none found (OpenML searched by name).
- Better data: from the gap scout for multiclass tasks and the gap scout for social science; no further search this round.
- Papers and pages: the competition's Description, Data, Evaluation and Rules pages (read through the Kaggle API).
- Metric: "Submissions will be evaluated based on their macro F1 score" (Evaluation page), on heads of household only, a competition metric on hard labels (MET-4): `f1_macro`; inputs: `parentesco1` to pick the scored rows, a scoring filter (or ship one row per household).
- Risks for /add-dataset: only train.csv is labelled (about 3,000 households; count the extreme-poverty class per fold, TP-5); the upstream survey (likely INEC's ENAHO) and its year are not named on the pages read (PROV-2), nor how the IDB set the Target (USE-5); possibly households whose members carry different Targets or that lack a head (to check); one-hot and squared columns to collapse (the scout's note; CLEAN); columns that mix "yes"/"no" with numbers (to check in the codebook).
- Priority: gap + (social science and multiclass thin), use case + (the sponsor names the aid decision), source 0 (a competition with a codebook, the survey behind it unnamed), shape + (about 3,000 households x 142 columns, binary, ordinal and numeric, households as groups), risk - (a small labelled set, the survey and the Target's construction unknown).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the gap scout for multiclass tasks; the gap scout for social science.
- as published: 9,557 labelled individuals in about 2,990 households x 143 columns (dwelling materials and condition, assets, household composition, education, region, area, rent), plus 23,856 unlabelled test ...; target: Target: 1 extreme poverty, 2 moderate poverty, 3 vulnerable, 4 non-vulnerable household; access: registration.
- Why: A development bank's competition with a direct targeting decision; scored by macro F1 on heads of household. Risks: the upstream survey is not named on the pages read (likely Costa Rica's ENAHO, to confirm), some households have members with different targets, and the unit is the household (group by idhogar) | ...
- Adds: A multiclass social-policy task (social science has 1 accepted dataset) with a household grouping and mixed binary, ordinal and numeric features | Welfare targeting; a multiclass target; grouped regime (households, several members per household sharing the label); mixed types (binary indicators, counts, rent amount). ...
