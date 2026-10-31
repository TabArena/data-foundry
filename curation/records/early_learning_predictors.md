---
unique_name: early_learning_predictors
name: early_learning_predictors
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
collections:
- New (BeyondArena)
original_source: Website
year: '2024'
domain: education
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.datafirst.uct.ac.za/dataportal/index.php/catalog/962
- https://zindi.africa/competitions/datadrive2030-early-learning-predictors-challenge
notebook_path: datasets/beyond_iid/grouped/early_learning_predictors/early_learning_predictors.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/early_learning_predictors/dataset.py
source_row: 742
type_adapter_id: curation-record-v1
---

## Comments

Very nice dataset. It was used in a Zindi challenge, where an additional focus next to predictive performance was on interpretability. I think they used random splits, but it should be either temporal or group based (by school). Needs some preprocessing since it doesn't make sense to use all ~1200 features. But we can follow the Zindi challenge, where a subset of features was provided

predict whether a child thrives by five

CC (2026-10-21, Lennart): "yes we should have one clear way to treat 0/1 flags": every 0/1 flag (a feature holding only 0 and 1, plus missing values; booleans too) is categorical (CLEAN-14, amended). Typed categorical here: count_staff_unpaid_managers, pra_breadwinner, pra_letcee_club, practitioner, pri_funding_subsidy, quintile_used.

CC (2026-10-21, Lennart): on which 0/1 columns are flags: "no if we can infer from the semantic context, keep it a number, this is a real-world bias. We want to make things categorical if we know from the context they are indeed such" (CLEAN-14, amended again). Kept categorical: pra_breadwinner, pra_letcee_club, pri_funding_subsidy (yes/no questions by name). Reverted: count_staff_unpaid_managers (a count), practitioner and quintile_used (meaning not documented).

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source rmse — the Zindi challenge's error metric, root mean squared error of the total ELOM score.

**Assessment (AI, 2026-10-26):** an open doubt under CLEAN-14, from the cross-dataset item of 2026-10-21: `practitioner` and `quintile_used` hold only 0 and 1 and stay numeric because no codebook gives their meaning; they become categorical if a codebook names them yes/no items.

CC (2026-10-30, Lennart): the Stata missing codes `.a` and `.b` become missing values and the 46 columns that held them are numeric (45 in the cleaned frame: the `count_register_*` and `count_staff_*` counts, the `pri_amount_*`, `pri_expense_*` and `pri_fees_*` amounts, `pri_capacity`, `pri_dsd_year`, `teacher_duration`). The source's codebook types them `numeric`; the codes occur only where the question was asked (a skipped question is blank), so they are unanswered questions, which the source does not define further. Raised by Adrian in issue #36 and found by the dtype probe's sweep the same day. CLEAN-10, CLEAN-14.

CC (2026-10-30, Lennart): `teacher_duration` is dropped: the minutes the teacher's rating form was open, a timer of the data collection like the `duration_elom` timers, whose little signal follows the survey round (CLEAN-22). The notes now match the code on the assessor's id (`id_enumerator`), which is dropped with the other ids: the curation note, `known` and `fit_reason` had said it was kept.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): 19 ordinal scales typed as ordered categories in the codebook's order (CLEAN-14, amended): `child_years_in_programme`, `pqa_curriculum_literacy`, `pqa_curriculum_ncf`, `pqa_curriculum_numeracy`, `pqa_environment_accessible`, `pqa_environment_appropriate`, `pqa_environment_areas`, `pqa_environment_open`, `pqa_environment_outdoor`, `pqa_environment_variety`, `pqa_relationships_acknowledge`, `pqa_relationships_discipline` and 7 more (the README lists their levels); their codes that mean unknown (don't know, refused, not asked) are missing in `child_years_in_programme` (CLEAN-10); left unordered: `child_stunted` (a partial order); `pri_calc_time_close` (no longer in the frame (dropped by a cleaning step of this branch)); `pri_calc_time_open` (no longer in the frame (dropped by a cleaning step of this branch)); ordinal scales shipped as numbers, left as numbers for the curator's review: `quintile`, `gr_ecd`, `obs_booknumber`, `obs_condition_equipment`, `obs_infrastructure`, `obs_material_display`, `plan`, `pqa_assessment_observation`, `pqa_assessment_systematic`, `pqa_curriculum_balance`, `pqa_curriculum_plan`, `pra_adequacy_materials` and 57 more; codes shipped as numbers, left for the curator's review: `gr_1_tt`, `grade_r`, `obs_building`, `obs_cooking_census`, `obs_heating_census`, `obs_lighting_census`, `obs_water`, `pra_class_language`, `pra_job`, `pra_previous`, `pra_shape`, `pri_bank` and 6 more; cleaning: child_stunted's two spellings of Normal merged; pra_dob a date; pri_calc_time_open/close (copies of the hour and minute columns where present) and certificate_registration_npo (a copy of certificate_register) dropped; 26 free-text columns strings; language_match noted..

CC (2026-10-31, Lennart): marks on the review board of PR #37 (ordinal scales in the codebook's order, also when shipped as numbers; a state outside a scale missing when the column has no other missing value, else the lowest level; cycles ordered; codes shipped as numbers as categories): 69 ordinal scales shipped as numbers are ordered categories (point 3); child_stunted ordered after merging its two spellings of Normal; 18 answer codes stored as numbers are categories.

## Reference

DataDrive2030. ELOM and Thrive by Five Index 2016-2023, Merged Data [dataset]. Version 1. Cape Town: DataDrive2030 [producer], 2024. Cape Town: DataFirst [distributor], 2024. DOI: https://doi.org/10.25828/WG0D-Y909
