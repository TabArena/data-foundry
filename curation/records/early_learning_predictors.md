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

CC (2026-11-01, Lennart): marks on the review board of PR #37: language_match's 16 written reasons (why the child was assessed in another language than at home) recoded to 0; the 26 free-text columns, categories before, are strings.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `thrive_by_five_index_2024` (TBD -> Yes, priority 3). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-01, Lennart): the decode rule (a code whose codebook says in words what each level is carries the words; a score without them is a number): 93 coded columns carry their words; 7 scores are numbers (quintile, pra_class_space_2, pra_satisfaction_support, ses_cat, ses_proxy, teacher_familiarity_with_child, teacher_selfcare_total); undocumented 0 codes missing (pra_cotlands_visits, pra_free_play, pra_free_play_outdoor, obs_water, pri_bank).

CC (2026-11-01, Lennart): the target rule (CLEAN-25) and the cut-end rule (CLEAN-14): counts with a cut end are numbers: pri_support_dbe, pri_support_dsd, pri_support_municipality, pri_support_ngo, pra_ntataise_attendance, pra_cotlands_visits.

CC (2026-11-01, Lennart): counts with a cut end stay ordered categories of the source's levels, the cut end a level of its own (CLEAN-14): the lossless form, chosen from the context rather than by model runs; the same day's numbers with censoring flags are reverted.

CC (2026-11-05, Lennart): GitHub issue #48 review: the ward ships as the national ward code `id_ward_best` (569 wards), a category, in place of `ward_best` (the ward's number within its municipality, which named different wards with one number). The sampling cluster `id_cluster_original` stays dropped: it exists only in the 2021 round, a unit of that survey's sample design that marks the round, while the ward is a place a new facility has too. The declared metric (RMSE, Zindi) is checked.

**Assessment (AI, 2026-11-05):** a ward holds 1 to 18 facilities (median 3, 28.5% hold one), the split groups by facility, so the ward contains whole groups and reveals no test facility's rows. Issue #48's other points on this dataset hold no change: `programme` was categorical already, `pra_agency_*` and `pra_job` stay as the #37 ordinal review decided, the free-text "other" columns stay strings.

## Review

**Outcome:** added. In the working copy since the migration; GitHub issue #48 (a column-type review of #37) found that
`ward_best`, a ward number, ships as a number. The AI recommends the national ward code as a category in its place.
Its other points on this dataset were settled in #37 or already hold (see the notes of issue 1).

**Main points:** Ship the ward as a code (which one), or drop it?

**Issues for Lennart:**

1. **Ship the ward as a code, not a number?**

   * **Problem:**
     - `ward_best` (1 to 130, missing for 53% of the children) is the ward's number within its municipality, and it ships as a number.
     - The same number names different places: ward 4 of Steve Tshwete (`id_ward_best` 83103004) and ward 4 of Dr JS Moroka (83106003) are two wards; 101 numbers stand for 569 wards.
     - The national ward code `id_ward_best` is dropped with the ids; issue #48 proposes a category, or dropping both.
   * **Background:** The definition keeps the province, district and municipality (`prov_best`, `dc_best`, `mn_best`) as categories; the Zindi release dropped all of them[^1].
   * **Effect on the task:** As a number, a model reads ward 4 < ward 23 as an order of places that does not exist; as a category, `ward_best` still pools wards of different municipalities.
   * **Experiments:** A ward holds 1 to 18 facilities (median 3; 28.5% of the wards hold one); the split groups by facility, so a test facility shares its ward with training facilities in most wards, as it shares its municipality.
   * **Consistency:** A code the source ships as a number ships as a category, unless its digits carry meaning (zip code prefixes)[^1]; the municipality here already ships that way.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Number (implemented) | as now | none found | an order of places that does not exist |
     | B | `ward_best` as a category | one line in `_feature_types` | smallest change; issue #48's first proposal | one level pools up to several wards of different municipalities |
     | C | National ward code as a category | ships `id_ward_best` as a category in place of `ward_best` | one level per ward; the same form as the municipality | brings back a column the notes list with the ids; 569 levels with few facilities each |
     | D | Drop the ward | removes `ward_best` | the location stays at the municipality | loses the finest location the data has |

   * **Recommendation:** C, one level per real ward, kept like the municipality. **Decision:** A, B, C or D?

   **Notes for the AI:** on C, remove `id_ward_best` from `indicator_cols` (it is listed twice), drop `ward_best`,
   add `id_ward_best` to `categorical` (integer codes stay integers, restored as categories by the container,
   Lennart 2026-11-04), and state in `curation_comments` why the ward code stays while the other ids leave. On B,
   add `ward_best` to `categorical`; on D, add it to `drop_columns` with the reason. Then `dataset check`, the group
   probe, a CHANGELOG entry and a CC line in the record. Issue #48's other points on this dataset, not raised here:
   `programme` is categorical already (it was at e24d557 too); the seven `pra_agency_*` columns stay unordered and
   `pra_job` stays a category, as the #37 ordinal review decided (a bipolar choice whose fourth answer, "disagree
   with both", sits off the line; job roles differ in kind); the 26 "other" free-text columns are strings by the
   cleaning of 2026-10-30.

   **Lennart (2026-11-05, change):** Option C: National ward code as a category.

   **Consistency check (AI, 2026-11-05):** Why does the ward code ship when the survey's sampling cluster
   `id_cluster_original`, of the same grain (430 clusters, median 3 facilities), is dropped as "leaks with
   school-based split"? The fact that sets them apart: the cluster exists only in the 2021 round (5,222 children),
   a unit of that survey's sample design that marks the dropped round; the ward is a place, in the 2020-2022 rounds.

   **Lennart (2026-11-05, chat):** Ward ships, note why.

   **Resolved (2026-11-05, Lennart):** C. `id_ward_best` ships as a category, `ward_best` is dropped, and the notes
   say why the ward stays while the sampling cluster leaves.

   [^1]: **CLEAN-14** (Should): a code the source ships as a number (an id, a type code, a detector column) is a
     category, unless its digits carry meaning a model can use (zip code prefixes, whose nearby values are nearby
     places).

## Reference

DataDrive2030. ELOM and Thrive by Five Index 2016-2023, Merged Data [dataset]. Version 1. Cape Town: DataDrive2030 [producer], 2024. Cape Town: DataFirst [distributor], 2024. DOI: https://doi.org/10.25828/WG0D-Y909
