---
unique_name: early_learning_predictors
name: early_learning_predictors
checked_by:
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
- WIP (DF)
claimed_by: Andrej
suggestion: 'Yes'
priority: 2
decision_markers:
- Needs extensive data wrangling
tags:
- Non-IID (Grouped)
- 'Samples: Over Time'
- 'Time: Dated'
- 'Entities: Recur'
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

**Assessment (AI, 2026-11-04):** reviewed for the BeyondArena v0.2 review page, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the record's Review. Ship as defined: target parts, other child assessments, ids and timers are dropped and the split holds out facilities; the use case is the curation's (approximate) and value is unmeasured. Priority 2: gap 0, use case 0, source 1, shape 1, risk -1.

CC (2026-11-05, Lennart): GitHub issue #48 review: the ward ships as the national ward code `id_ward_best` (569 wards), a category, in place of `ward_best` (the ward's number within its municipality, which named different wards with one number). The sampling cluster `id_cluster_original` stays dropped: it exists only in the 2021 round, a unit of that survey's sample design that marks the round, while the ward is a place a new facility has too. The declared metric (RMSE, Zindi) is checked.

**Assessment (AI, 2026-11-05):** a ward holds 1 to 18 facilities (median 3, 28.5% hold one), the split groups by facility, so the ward contains whole groups and reveals no test facility's rows. Issue #48's other points on this dataset hold no change: `programme` was categorical already, `pra_agency_*` and `pra_job` stay as the #37 ordinal review decided, the free-text "other" columns stay strings.

CC (2026-11-12, Andrej): split by assessment campaign (a round of child assessments), from the BeyondArena v0.2 review page (Review issues 3-5).
- Use case: a funder scores the children of its next campaign, at new facilities and at facilities surveyed before, and the survey can change between campaigns. The children were assessed in about eight campaigns (2016-2023), each its own study with its own sample of facilities and questionnaire, and the mean score jumps between them (40.9 to 54.2). So each of the four campaigns of 2022 and 2023 is tested once, trained on all earlier campaigns, including the earlier children of returning facilities. The facility split shipped before learned each campaign's level and questions from its other facilities and scored 0.4 to 5.0 RMSE better than a coming campaign allows (untuned LightGBM, same test children, equal training size).
- `id_facility` is numbered per study: where two campaigns share a number, province and quintile agree only within October 2020 to March 2022, elsewhere at the rate of two random facilities. About 120 facilities return in a later campaign, not 761 as counted before. Noted in the curation notes; the number is dropped with the other ids.
- `Entities: Recur`: a facility holds several children, and about 120 facilities return in a later campaign.
- Not checked or built yet: `dataset check` needs the raw DataFirst file, which is not on this machine.

CC (2026-11-12, Andrej): ships with the changes of issues 3 to 5 (BeyondArena v0.2 review page, issue 1, a); the split by assessment campaign and the metric (RMSE, Zindi's) are checked. Not checked or built: `dataset check` needs the raw DataFirst file, which is not on this machine.

CC (2026-11-13, Andrej): back to the facility split (BeyondArena v0.2 review page, issue 6): moving from the facility split to the split by assessment campaign was a mistake; the use case is a new facility again.
- The facility, practitioner and teacher surveys the use case predicts from exist only in the campaigns of October 2020 to December 2021; the four test campaigns of 2022 and 2023 record 11 to 30 columns, the child's own. On them no model beat the child's age alone (untuned LightGBM RMSE 15.53 on all features, 14.84 on age, 15.89 for the mean); on the facility split LightGBM scores 12.91 (age alone 14.47).
- `id_facility` groups the split again; numbers shared across studies fall on one side, a coarser group that cannot leak. `Samples: Over Time`, `Time: Dated` and `Entities: Recur` stay.
- Checked on the raw DataFirst file (`dataset check`: 0 errors, 0 warnings); not built.

CC (2026-11-13, Andrej): every child and every column stay (BeyondArena v0.2 review page, issue 7, A): the use case is the child's record plus whichever facility instruments the study ran (observation, registers, teacher rating; principal and practitioner interviews only in the 2021 national Index); a module a study did not run stays missing.
- On the facility split a model on all rows and columns scores each group of children as well or better than one trained on that group alone (own record only 12.96 against 13.16 RMSE; with the observation 12.79 both; with the interviews 12.19 against 12.27; untuned LightGBM).
- 47% of the children carry only their own record; their gain over age comes mostly from their campaign, learned from its other facilities (`fit_reason`).

CC (2026-11-13, Andrej): two cleaning fixes from the review of the build (BeyondArena v0.2 review page, issues 8 and 9, both B); 735 features.
- Three free-text answers typed as strings like the other 26: `pri_fees_exceptions_other`, `pri_expenseother`, `pra_online_training_details` (66 to 124 different answers each).
- Four multi-select lists dropped, `obs_materials`, `obs_area`, `obs_hazard` and `pri_covid_precautions`: each agrees in every cell with its per-code yes/no columns, which stay. `pri_covid_awareness` stays (55 cells differ).

## Review

**Outcome:** added. DataDrive2030's merged ELOM and Thrive by Five Index data 2016-2023 (DataFirst, CC BY,
https://doi.org/10.25828/WG0D-Y909), the data of Zindi's Early Learning Predictors Challenge: 18,874 children aged
50-69 months assessed at 2,541 early learning facilities in South Africa; the target is the child's total score on the
Early Learning Outcomes Measure (ELOM, a standard test of 23 items over five areas of development), predicted from 739
features of the child, the facility, the practitioner and the teacher; split by facility (issue 6), scored
by RMSE (Zindi's metric). The AI recommends shipping it as defined. Reviewed on 2026-11-04 without a panel, from the gathered evidence
(the record, the CHANGELOG, the definition's notes); no model run exists for it. Validity: the parts and other
versions of the score, the other child assessments (`_sef`, `child_observe_*`), the survey year, the assessors' and
other ids and the data-collection timers are dropped, so no feature is read off the test; the facility split tests a
facility a campaign did not reach (issue 6); the source's question is explanatory, and the definition's use case (a funder estimating children's
scores at a new facility without a full assessment) is the curation's, rated approximate, as `fit_reason` says; some
surveys were made after the assessment, which `fit_reason` names. Value: untested here (no model run, no task
probe on record); Zindi ran it as a prediction challenge. Quality: 80% of the cells are missing, survey rounds asked
different questions, and the Stata missing codes, ordinal scales and codes are settled (Lennart, 2026-10-30 to
2026-11-01). Weighed: a documented survey with a codebook and a DOI +, a facility split +, an explanatory source and
features that mix survey rounds -, value unmeasured.

**Main points:** Back to the facility split (issue 6 B, 2026-11-13): the split by assessment campaign of issue 3 c tested
only campaigns that record the child's own columns, where no model beat the child's age alone. `id_facility` groups the
split again (numbered per study, issue 4 B), `Entities: Recur` stays (issue 5 B). Checked on the raw DataFirst file
(`dataset check`: 0 errors, 0 warnings). Every child and every column stay, the use case reworded to the child's record
plus whichever facility instruments the study ran (issue 7 A). Built on 2026-11-13 (`01a1d456`): no leak, no task-probe
flag (LightGBM R² 0.31). From the build's review: three free-text answers are strings now (issue 8 B), and four
multi-select lists that copied their yes/no columns are dropped (issue 9 B); 735 features, checked, not rebuilt.
Nothing open.

**Record judgment:** valid. The record's `Website` source is the schema's `Other`, as in the definition, and the other
fields agree. `Needs extensive data wrangling` describes the work done. The data scouting found
`thrive_by_five_index_2024`, possibly a newer round of the same survey; it is screened in its own record and does not
change this task's validity.

**Issues for Andrej:**

1. **Ship as defined?**

   * **Problem:**
     - Nothing open was found: the target's parts and other versions, the other child assessments, the survey year, the
       ids and the collection timers are dropped, the split holds out whole facilities, and the codes are settled.
     - What remains is the use case, which the definition writes itself (the source asks which programme features go
       with better scores), and the value, which no run has measured.
     - Ship as defined, or retire?
   * **Background:** Zindi ran the same data as a prediction challenge scored by RMSE, with a random split by child;
     the definition holds out facilities instead and keeps the teacher and parent questionnaires the challenge
     left out. The fit is approximate: some surveys were made after the assessment, and the rows mix survey rounds
     that asked different questions (80% of the cells are missing).
   * **Unknown:** how far the methods spread on this definition; no model run or task probe exists for it.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Ship as defined (implemented) | 18,874 children, 739 features, split by facility, RMSE | a documented national survey with a codebook; a facility split; a wide, sparse table unlike most of the benchmark | an explanatory source; value unmeasured |
     | B | Retire | `No (Retired)`, a CC line, the folder removed | drops a task whose use case is the curation's | no defect of the data found; reverses Andrej's `Yes` |

   * **Recommendation:** A: no validity problem was found, and a weak use case is a caveat the fit already states[^1a].
     **Decision:** A or B?

   [^1a]: **TP-6** (Must): keep two questions apart, whether the task is valid and whether it is the best version; a
     valid task stays.

   **Andrej (2026-11-12, discuss):** See other issues

   **Answer (AI, 2026-11-12):** Ship with the changes of issues 3 to 5?

   * **Problem:**
     - Issues 3 to 5 are applied in the definition and the record: the split by assessment campaign, the note on the
       facility numbers with `id_facility` dropped, and `Entities: Recur`.
     - Nothing else is open, but the definition is not checked or built yet (the raw DataFirst file is not on this
       machine), so the split box of the Use case tab still shows the facility split of the old generated README.
     - Ship with these changes, or retire?
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Ship with the changes of issues 3 to 5 | 18,874 children, four campaign windows, RMSE; checked and built once the raw file is available | a documented survey with a codebook and a DOI; a test of a coming campaign, as the use case asks | each test score carries one campaign offset no feature predicts; the methods' spread on this split is unmeasured |
     | b | Retire | `No (Retired)`, a CC line, the folder removed | drops a task whose use case is the curation's | no defect of the data found |

   * **Recommendation:** a: the split now stands for the use case you described. **Decision:** a or b?

   **Andrej (2026-11-12, discuss):** Reply (a): Ship with the changes of issues 3 to 5

   **Resolved (2026-11-12, Andrej):** a. Ships with the changes of issues 3 to 5 (split by assessment campaign,
   `id_facility` dropped with the other ids, `Entities: Recur`); verdict ship; split and metric (RMSE, Zindi's) marked
   ok; a record CC line. Not checked or built: `dataset check` has not run for these changes, because no copy of the raw
   DataFirst file is on this machine (the download needs a DataFirst account).

2. **Ship the ward as a code, not a number?**

   * **Problem:**
     - `ward_best` (1 to 130, missing for 53% of the children) is the ward's number within its municipality, and it ships as a number.
     - The same number names different places: ward 4 of Steve Tshwete (`id_ward_best` 83103004) and ward 4 of Dr JS Moroka (83106003) are two wards; 101 numbers stand for 569 wards.
     - The national ward code `id_ward_best` is dropped with the ids; issue #48 proposes a category, or dropping both.
   * **Background:** The definition keeps the province, district and municipality (`prov_best`, `dc_best`, `mn_best`) as categories; the Zindi release dropped all of them[^2a].
   * **Effect on the task:** As a number, a model reads ward 4 < ward 23 as an order of places that does not exist; as a category, `ward_best` still pools wards of different municipalities.
   * **Experiments:** A ward holds 1 to 18 facilities (median 3; 28.5% of the wards hold one); the split groups by facility, so a test facility shares its ward with training facilities in most wards, as it shares its municipality.
   * **Consistency:** A code the source ships as a number ships as a category, unless its digits carry meaning (zip code prefixes)[^2a]; the municipality here already ships that way.
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

   [^2a]: **CLEAN-14** (Should): a code the source ships as a number (an id, a type code, a detector column) is a
     category, unless its digits carry meaning a model can use (zip code prefixes, whose nearby values are nearby
     places).

3. **Split by time, or keep the grouped split with no time-basis tag?**

   * **Problem:**
     - Each child's assessment date follows from the birth date and the age in months (82% of the children; the dropped
       `child_date` and `data_year` give it for all), the rounds run from 2016 to 2023, and the use case scores the
       children of a new facility in a coming round, so the assessment date is information for the split, as the
       facility is[^3a].
     - Trained on earlier rounds only, LightGBM's error is higher than with as many children of all rounds in every
       window, by 0.3 to 4.8 RMSE on a score whose spread is about 15.
     - Split by assessment date with the test facilities held out, or keep the facility split with no time-basis tag?
   * **Background:** birth date plus age dates 15,480 children: 426 in 2017-2018, 270 in late 2020, 6,906 in 2021,
     3,902 in 2022 and 3,976 in 2023; the 3,025 children without a birth date are all from the rounds before COVID
     (`pre_covid` yes), and 369 others stay undated here. 761 of the 2,541 facilities were assessed in more than one
     half-year (310 in late 2021 and early 2023), so a split by date alone would test facilities already seen. The mean
     score moves between half-years from 39.6 (early 2018) and 40.9 (early 2023) to 54.2 (late 2022), as each round
     sampled its own facilities with its own questionnaires. Four six-month windows from January 2022, the test facilities left out of
     training, train on 53%, 71%, 61% and 86% of the children.
   * **Experiments:** the BeyondArena copy of the same 18,874 children, with the columns v0.2 has dropped since removed
     (738 of v0.2's 739 features; the national ward code is not in this copy), untuned LightGBM and ridge regression,
     RMSE (Slurm job 1365903):
     - Shipped split by facility (3 x 3, the README's folds): LightGBM 12.97 (12.80 to 13.13); ridge 20.8 (17.2 to
       33.3), unstable on the sparse wide table, so LightGBM's numbers decide.
     - The four windows, each trained on all earlier assessments of other facilities: LightGBM 14.08 (January to June
       2022), 14.24 (July to December 2022), 17.54 (January to June 2023) and 15.28 (July to December 2023, the newest).
     - Same test children and same training size (each window in 3 folds by facility, 3 seeds; earlier assessments
       only against children of all dates, the fold's facilities left out): LightGBM +0.33, +0.72, +4.76 and +1.77
       RMSE, higher on all 36 folds; ridge +2.3 to +12.3 on three windows and -2.9 on the first.
     - Keeping the test facilities' earlier rounds in training makes LightGBM worse by 0.1 to 0.8 RMSE in all four
       windows, so the held-out facilities cost nothing.
   * **Effect on the task:** the facility split trains on children of the same and later rounds, so a test child's
     round level and questionnaire pattern are learned from other facilities of its round; a funder scoring a new
     facility in a coming round has only the earlier rounds.
   * **Unknown:** how much of the shift is time and how much a change of survey; each window holds one or two rounds,
     so it tests a new round as much as a new date.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Facility split, no time-basis tag (implemented) | 3 x 3 folds by facility; no use-case prototype named (`StationaryRelation` is not shown: the mean score moves from 39.6 to 54.2 between half-years and a split by date with the facilities held out costs +0.3 to +4.8 RMSE (LightGBM) at equal training size; the four windows are valid, so no forced tag) | 9 splits over all rounds; no change | LightGBM scores 0.3 to 4.8 RMSE better than on later rounds, in every window; a test child's round is learned from other facilities of the same and later rounds |
     | B | Four windows by assessment date, test facilities held out | the assessment date as the time column; test the four half-years of 2022 and 2023, each trained on all earlier assessments of other facilities (53% to 86% of the children) | a new facility in a coming round, the use case | a custom split; each window is a new survey round as much as a new date |

   * **Recommendation:** B: it is the use case's own question, every window meets the split rules, and the facility
     split's gain is consistent (36 of 36 folds); written so, it ships as a temporal task that holds out facilities,
     as alfa_battle_2_0_task_2 holds out the clients of its test window. **Decision:** A or B?

   **Notes for the AI:** on B, keep the assessment date in `_clean` as `assessment_date` from `child_date` (check it
   against birth date plus age, which dated the windows here, and that every child has one; else `data_year`), declare
   `Temporal(on="assessment_date", horizon=6, horizon_unit="months")` in place of the grouping, and a `_make_splits`
   with four windows starting 2022-01-01, 2022-07-01, 2023-01-01 and 2023-07-01, six months each, whose train side is
   every earlier assessment except those of facilities in the test window (`id_facility` stays out of the features);
   `split`, `fit_reason` and `splits_comment` say so and cite the cost; record `required_split` Temporal, tag
   `Non-IID (Temporal)`; `dataset check`. On A, no time-basis tag in the definition; a curation bullet `- Time
   order: the assessment rounds run 2016-2023 and each child's date follows from
   birth date and age (82%) or the dropped child_date; not split by date, because <the curator's reason>; four
   six-month windows from January 2022, each trained on earlier assessments of other facilities, cost +0.3 to +4.8
   RMSE at equal training size (untuned LightGBM, 36 of 36 folds).`, and `accepted_check_warnings` takes
   `meta_time_present_unused` with that reason (`child_dob` and `pra_dob` are dates). Under either option the record
   gets the tags `Samples: Over Time` and `Time: Dated`. Results: Slurm job 1365903.

   [^3a]: **SPLIT-32** (Should): how the data was collected is information for the split; the record's collection
     facts and, where one fits, the definition's use-case prototype with its `Time basis:` line. **SPLIT-13** (Should): an entity that recurs across the
     cutoff is a question when the use case is a new entity. **SPLIT-14** (Must): at least 3 windows, none training on
     less than half of the data. SPLIT-9 case: alfa_battle_2_0_task_2 drops the training rows of the test window's
     clients (2026-10-26, Lennart).

   **Andrej (2026-11-10, discuss):** Reassess this again, we actually want to generalize to new unseen facilities in
   this case but if there is temporal drift that might be a problem. So think again.

   **Answer (AI, 2026-11-10):** The drift is real and comes as a jump between survey rounds, not a trend; option B
   already holds out unseen facilities and adds time, so it tests both.

   * The mean score jumps between consecutive half-years: 54.2 (late 2022), 40.9 (early 2023), 52.5 (late 2023). The
     half-year explains 8% of the score's variance, the facility 40%.
   * Each round is recognisable from its features: a model tells a window's children from earlier ones with ROC AUC
     0.998 to 1.000 (dates and age removed); early 2023 lacks 159 columns the earlier rounds filled.
   * Under the facility split the model learns each round's level from other facilities of the same round, which a
     funder scoring a coming round does not have.
   * Most of the temporal cost is one offset per window (mean error -7.7 to +6.0); without it, the error stays 0.4 to
     3.3 RMSE above the facility split's on the same children.
   * Temporal only (test facilities' earlier rows kept) is worse than B in all four windows (+0.1 to +0.8 RMSE) and tests
     facilities already seen.

   LightGBM RMSE per test window (Slurm job 1365903; drift probes job 1377084):

   | Test window | Children | Mean score | Train share (B) | B: grouped + temporal | B's offset | B without offset | A: grouped only, same children |
   |---|---|---|---|---|---|---|---|
   | Jan-Jun 2022 | 2,706 | 48.7 | 53% | 14.08 | +0.5 | 14.07 | 13.49 |
   | Jul-Dec 2022 | 1,196 | 54.2 | 71% | 14.24 | +4.1 | 13.65 | 13.23 |
   | Jan-Jun 2023 | 2,338 | 40.9 | 61% | 17.54 | -7.7 | 15.76 | 12.51 |
   | Jul-Dec 2023 | 1,638 | 52.5 | 87% | 15.28 | +6.0 | 14.04 | 13.16 |

   * **Options:**

     | | Option | Splits, test size, train share | Pro | Con |
     |---|---|---|---|---|
     | A | Grouped only (implemented) | 9 (3 x 3 by facility), about 6,300 children each, 67% | most test rows; stable scores | trains on the test round; 0.6 to 5.0 RMSE kinder than a coming round |
     | B | Grouped + temporal | 4 six-month windows from 2022-01-01, test facilities' earlier rows out of training; 1,196 to 2,706 children, 53% to 87% | a new facility in a coming round, the use case | 4 small test sets; each score carries one round offset no feature predicts; a new round is a new questionnaire as much as a new date |
     | C | Temporal only | the same 4 windows, all earlier rows; 56% to 89% | more training rows | tests facilities already seen; worse than B in every window |

   * **Recommendation:** B, with the parameters of the issue's notes: `Temporal(on="assessment_date", horizon=6,
     horizon_unit="months")`, windows starting 2022-01-01, 2022-07-01, 2023-01-01 and 2023-07-01, the test facilities'
     earlier assessments dropped from training. It holds out unseen facilities, as you want, and shows the round shift A
     hides. A stays if the round shift is read as a change of survey design rather than drift. **Decision:** B, A or C?

   **Andrej (2026-11-12, chat):** I believe that the early_learning_predictor dataset constitutes a new case for our
   temporal data handling that was not covered well enough yet. Let me first describe the data: It was collected in
   groups by facilities at different points in time. For the use case, the predictive model would be used on arbitrary
   new facilities, but also repeatedly on students from the same facility. The survey design may also change over time.
   We need to reassess the use case. What would be the best split for the use case, independent of our discussion
   here? So what is the population we want to learn to generalize to? But also, how does that align with our temporal
   tags?

   **Answer (AI, 2026-11-12):**

   * Asked: whom the model should generalize to, which split stands for that, and how it fits the time-basis tags.
   * The population is the children of the next assessment campaign. Three things are new for them at once: the child
     (always: children leave the 50 to 69 months range, and no child is assessed twice), the campaign (always: a new
     date, a new sample of facilities, possibly a new questionnaire) and the facility (mostly new, sometimes known).
   * The data arrive in about eight field campaigns, each its own study (dated by birth date plus age; the 2021 national
     Thrive by Five Index is a multistage cluster sample fielded 20 September to 19 November 2021, DataFirst catalogue
     947; the release calls the rest "the ELOM studies in 2016, 2018, and 2019 and other studies"):

     | Campaign | Children | Facilities | Mean score | Columns over half filled |
     |---|---|---|---|---|
     | 2016-2019 ELOM studies (mostly February-March 2018; 3,025 without a birth date) | 3,451 | 249 | 52.2 | 22 |
     | October-November 2020 | 270 | 48 | 52.5 | 227 |
     | 2021: February-May, and August-November (the national Index) | 6,906 | 1,508 | 46.0 | 244 |
     | January-March 2022 | 2,706 | 375 | 48.7 | 34 |
     | September-November 2022 | 1,196 | 194 | 54.2 | 42 |
     | January-May 2023 (province missing for 81%) | 2,338 | 661 | 40.9 | 11 |
     | August-November 2023 | 1,638 | 197 | 52.5 | 13 |

   * `id_facility` is numbered per study: only about 120 facilities come back in a later campaign, all within October
     2020 to March 2022, not the 761 of the issue's background (issue 4).
   * A facility's level barely carries over to its next campaign, while within one campaign it is clear. The campaign
     explains 6.5% of the score's variance, the facility within its campaign 42%.

     | Facility's mean score, centred on its campaign | Pairs | Correlation |
     |---|---|---|
     | two random halves of its children, same campaign | 2,610 facility-campaigns | 0.57 |
     | October-November 2020, then 2021 (same facility) | 32 | 0.17 |
     | 2021, then January-March 2022 (same facility) | 90 | 0.27 |

   * Per test campaign, the earlier runs (LightGBM, Slurm 1365903) with today's revisit counts:

     | Test campaign | Children | Same number earlier | Same facility earlier | Rows b drops | Train share b / c | RMSE a (same children) / b / c | c minus a at equal size |
     |---|---|---|---|---|---|---|---|
     | January-March 2022 | 2,706 | 24.6% | 24.6% | 654 | 53% / 56% | 13.49 / 14.08 / 14.19 | +0.42 |
     | September-November 2022 | 1,196 | 1.1% | none | 1 | 71% / 71% | 13.23 / 14.24 / 14.38 | +0.83 |
     | January-May 2023 | 2,338 | 71.9% | none confirmed | 3,027 | 61% / 77% | 12.51 / 17.54 / 17.70 | +4.96 |
     | August-November 2023 | 1,638 | 46.4% | none confirmed | 536 | 87% / 89% | 13.16 / 15.28 / 16.09 | +2.62 |

   * How it fits the time-basis tags[^3b]:

     | Fact or question | Here | Covered? |
     |---|---|---|
     | `Samples: Over Time` | yes, about eight campaigns, 2018 to 2023 | yes; that each campaign is a separate study (own sample, questionnaire, assessors) is no fact of its own |
     | `Time: Dated` | `child_date` and `data_year` in the raw file, birth date plus age for 82% | yes |
     | Target | measured at the assessment, no tag | yes |
     | `Entities: Recur` | a facility holds several children; about 120 come back in a later campaign | missing on the record (issue 5); the tag does not say whether entities recur within one moment or across campaigns |
     | `Features: Read Later` | `fit_reason` says some surveys were made after the assessment | not checkable: the release gives no survey dates |
     | Does arriving over time affect the target? | yes: each campaign brings its own selection of facilities and questionnaire, which count as recording changes, and the time is dated | gives a temporal split, not the shipped facility split |
     | New or known entity, decided before the split; grouped or temporal, never both | the use case meets both | the rules ask for one; read with the rule on returning entities inside a temporal split, they give c |
     | Horizon | the next campaign, 4 to 8 months apart | a horizon in months does not name it; anes_voting_2026 takes one window per study |

   * Three gaps, each a cross-dataset item: campaigns that are separate studies (`ba-campaign-windows`), a use case
     that meets new and known entities (`ba-mixed-new-known`), and ids that span merged studies
     (`ba-merged-study-ids`).

   [^3b]: **SPLIT-32** (Should; PR #50): the record's collection facts (`Samples:`, `Time:`, `Target:`, `Entities:`,
     `Features:`) and the definition's prototype; question 4: arriving over time affects the target when how the target
     or the features are recorded changes (a new instrument, a new selection of cases), and dated or inferred time then
     gives a temporal split. **USE-10** (Must): decide from the use case whether the entity is new or known before
     choosing the split. **SPLIT-3** (Must): a task is grouped or temporal, never both. **SPLIT-13** (Should): an entity
     that recurs across the cutoff is part of the task when the model predicts for known entities. **SPLIT-12**
     (Should): the horizon is how far ahead the actor predicts.

   **Answer (AI, 2026-11-12):** Which split stands for the children of a coming campaign at new and known facilities?

   * **Problem:**
     - Only campaigns as test windows, each trained on everything before it, give a model what the funder has: the
       earlier children of a facility that comes back, and no child of the coming campaign.
     - Most facilities that seemed to come back are other facilities with the same number, so b's drop removes mostly
       unrelated facilities (3,027 rows before January-May 2023).
     - The recommendation of b on 2026-11-10 also rested on b scoring better than c in four windows, which may not
       choose a training history[^3c].
   * **Effect on the task:** a tests a new facility in a campaign whose level and questionnaire the model learned from
     the campaign's other facilities; c tests a coming campaign, with its own level and questionnaire, at the new and
     known facilities it brings.
   * **Consistency:** anes_voting_2026 tests each of its last five election studies once, trained on all earlier
     studies, after checking that its cross-year id links respondents only within some panels. A returning entity's
     history stays when the model predicts for known entities[^3d]. b's drop comes from alfa_battle_2_0_task_2, where a
     later default label was a shortcut; the scores of earlier campaigns were known before the test campaign[^3e].
   * **Unknown:** whether a funder recalibrates each campaign on a few fully assessed children; then a comes closer, as
     it learns a campaign's level from that campaign's own children. How much of a campaign's offset is time and how
     much its sample and questionnaire: four windows cannot separate them, and the deployment meets them together.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Facility split (implemented) | 3 x 3 folds by facility over all campaigns; about 6,300 test children each; 67% training | most test children; stable scores; stands for a deployment that knows the campaign (facilities a campaign did not reach, or a model recalibrated on its assessed children) | learns each campaign's level and questionnaire from its other facilities; never tests a changed survey; 0.4 to 5.0 RMSE kinder than a coming campaign |
     | b | Campaigns, test facilities' earlier rows dropped | the four campaigns of 2022 and 2023 as windows, each trained on earlier campaigns minus every facility whose number is in the test campaign; 53% to 87% | new facilities only | drops what the funder has for a known facility; the dropped rows are mostly other facilities; needs a study-aware key (issue 4 C) |
     | c | Campaigns, all earlier rows | the same four windows, each trained on everything before it; 56% to 89%; a quarter of the January-March 2022 children at a facility seen in 2021 | the funder's position: new children at new and known facilities, a new questionnaire; the design of anes_voting_2026 | 4 test sets of 1,196 to 2,706 children; each score carries one campaign offset no feature predicts; known facilities only in the first window |

   * **Recommendation:** c, the use case as you describe it; it replaces b of 2026-11-10. a if funders recalibrate on
     each campaign's assessed children. **Decision:** a, b or c?

   **Notes for the AI:** on c: in `_clean` keep the assessment date as `assessment_date` from `child_date` (check it
   against birth date plus age and that every child has one, else `data_year`), and a `campaign` column (the half-year,
   one study per half-year from 2020 on); `Temporal` on the campaign with one window per campaign and four windows
   (`TemporalSplits(window=1, unit="unique", n_windows=4)`, as anes_voting_2026), horizon 6 months; drop `grouping`;
   check whether the time column ships as a feature (the campaign marks the round, dropped as `data_year`).
   `task_summary`: `split`, `use_case` and `fit_reason` for new and known facilities in a coming campaign whose survey
   may change; `splits_comment` names the four campaigns, the train shares (56%, 71%, 77%, 89%), the share of test
   children at a facility seen before (24.6%, then none) and the cost against the facility split (Slurm 1365903).
   Record: `required_split` Temporal, `Non-IID (Temporal)` in place of `Non-IID (Grouped)`; `dataset check`; the leak
   probes the change touches. On a: the curation bullet of the issue's notes with the numbers above and
   `meta_time_present_unused` accepted. On b: the 2026-11-10 notes, with issue 4 C's key.

   [^3c]: **SPLIT-21** (Must): decide neither the training history nor the windows from a comparison over a few test
     windows.
   [^3d]: **SPLIT-13** (Should): an entity that recurs across the cutoff is part of the task when the model predicts
     for known entities, and a question when the use case is a new entity. **USE-10** (Must): for a known entity, its
     history is legitimate.
   [^3e]: **SPLIT-9** (Must): a training row whose label tells a test row's outcome and was not yet known at the
     prediction point must not be in train (alfa_battle_2_0_task_2 drops the test window's clients' training rows).

   **Andrej (2026-11-12, discuss):** Reply (c): Campaigns, all earlier rows

   **Resolved (2026-11-12, Andrej):** c. In `_clean`, `campaign` is the half-year of the assessment date (`child_date`,
   else birth date plus age, else `data_year` for the rounds before 2020; the build stops if a child stays undated),
   the time column and a feature; `Temporal(on="campaign", splits=TemporalSplits(window=1, unit="unique",
   n_windows=4), horizon=6, horizon_unit="months")` replaces the facility grouping, so `id_facility` is dropped with
   the other ids (issue 4). `task_summary`, a new `splits_comment` and the curation notes say so with this issue's
   numbers; the record has `required_split` Temporal and `Non-IID (Temporal)`, with a CC line. Not checked or built:
   the raw DataFirst file is not on this machine. Tested on the BeyondArena copy (birth date plus age only): one window
   per campaign, each trained on every earlier campaign (57% to 91% of the 18,505 children it can date).

4. **Write down that `id_facility` is numbered per study?**

   * **Problem:**
     - Where two campaigns share a facility number, the facility's province and quintile agree only within the
       campaigns of October 2020 to March 2022, and elsewhere no more often than for two random facilities.
     - So about 120 facilities come back in a later campaign, not 761, and the numbers -2, -1 and 9999 hold 45
       children of unknown facilities.
     - Note it, and build a key that tells the studies apart?
   * **Experiments:** for each pair of campaigns that share numbers, the facility's attributes in both (the most
     frequent value over its children):

     | Campaigns sharing numbers | Shared numbers | Agree | Two random facilities | Same facility? |
     |---|---|---|---|---|
     | October-November 2020 and 2021 | 32 | province 32 of 32 | | yes |
     | 2021 and January-March 2022 | 90 | province 90 of 90, quintile 90 of 90, building 75 of 75 | 0.11, 0.22, 0.75 | yes |
     | 2021 and January-May 2023 | 337 | quintile 0.30 (81), fees 0.04 (51) | 0.27, 0.05 | no |
     | January-March 2022 and January-May 2023 | 79 | province 0 of 7 | | no |
     | September-November 2022 and January-May 2023 | 68 | province 0 of 12 | | no |
     | January-March 2022 and August-November 2023 | 31 | province 0.06 | 0.12 | no |
     | September-November 2022 and August-November 2023 | 52 | province 0.12 | 0.13 | no |
     | 2016-2019 and January-May 2023 | 36 | not checkable (province missing in 2023) | | unknown |

   * **Effect on the task:** the facility split puts two facilities that share a number on one side, a coarser group
     that cannot leak. Under campaign windows nothing uses the number, unless the test facilities' rows are dropped
     (issue 3 b) or a facility's history becomes a feature.
   * **Consistency:** a group key is a true id or one built from the data exactly or by a calibrated link[^4a];
     anes_voting_2026 checked that its cross-year id links respondents only within some panels.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | As is (implemented) | `id_facility` groups the facility split; no note | nothing changes; a shared number cannot leak | the notes and issue 3 counted 761 returning facilities; recurrence read off the number misleads |
     | B | Note it | a curation bullet and a record assessment line: numbered per study, about 120 facilities come back (all October 2020 to March 2022), 45 children under -2, -1 and 9999; the split keeps the number | the notes say what the number is; no change to any split | the facility split's groups stay coarser than the facilities |
     | C | Study-aware key | a facility key: the number within October 2020 to March 2022, campaign plus number elsewhere, each child under a placeholder its own group | one group per facility | a key we build; needed only for issue 3 b or a facility-history feature |

   * **Recommendation:** B; C only with issue 3 b. **Decision:** A, B or C?

   **Notes for the AI:** on B, a curation bullet "- `id_facility` is numbered per study: ..." with the table's
   numbers, and an `**Assessment (AI, <date>):**` line in the record. On C, build the key in `_clean` before the ids are
   dropped and group on it; the 2016-2019 numbers shared with January-May 2023 stay apart (not checkable).

   [^4a]: **SPLIT-24** (Must): group on a true group id, or on one constructed from the data, either exactly or by a
     calibrated link whose match rule comes from how the data were recorded and whose chance rate shows most links are
     real.

   **Andrej (2026-11-12, change):** Option B: Note it.

   **Resolved (2026-11-12, Andrej):** B. A curation bullet with the check's numbers; since issue 3 c removed the
   facility grouping, `id_facility` is dropped with the other ids (as a feature it would name other facilities as
   returning ones); a record CC line.

5. **Tag the record `Entities: Recur`?**

   * **Problem:**
     - The record carries `Samples: Over Time` and `Time: Dated`, but not that the source holds several children of one
       facility (up to 66 under one number).
     - About 120 facilities also come back in a later campaign (issue 4).
     - Add the tag?
   * **Consistency:** the cross-dataset item on returning entities (`ba-entities-recur-sweep`) proposes the tag for
     every source that holds several rows of one entity[^5a].
   * **Unknown:** whether some surveys came after the assessment, as `fit_reason` says (`Features: Read Later`): the
     release gives no survey dates.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | As is (implemented) | `Samples: Over Time`, `Time: Dated` | nothing changes | the record misses the fact the rules on returning entities start from |
     | B | `Entities: Recur` | adds the tag with a CC line | the record states that facilities recur | the tag does not say that most of a facility's rows arrive together and few facilities return |

   * **Recommendation:** B. **Decision:** A or B?

   **Notes for the AI:** on B, through the store API (`Andrej` is in `checked_by` already), with a CC line that names
   the facility and the about 120 returns.

   [^5a]: **SPLIT-32** (Should; PR #50): `Entities: Recur` when the source holds several rows of one entity, with or
     without an id.

   **Andrej (2026-11-12, change):** Option B: Entities: Recur.

   **Resolved (2026-11-12, Andrej):** B. The record carries `Entities: Recur`, with a CC line.

6. **The test campaigns lack the surveys the use case predicts from: change the split or the rows?**

   * **Problem:**
     - The facility, practitioner and teacher surveys exist only in the campaigns of October 2020 to December 2021
       (225 to 242 columns over half filled); the four test campaigns of issue 3 c record 11 to 30, the child's own
       (age, sex, birth date, height, languages, years in the programme) and at most province and quintile.
     - So on the shipped split no model beats the child's age alone: untuned LightGBM on all 740 features scores
       RMSE 15.53, `child_age` alone 14.84, the training mean 15.89; the task probe flags `no_signal` and `unstable`.
     - The use case predicts "from facility, staff and family surveys", so change the split, keep only the children
       who have the surveys, or keep it as is?
   * **Experiments:** the definition as checked on the raw file (`dataset check`: 0 errors; leak probes: no copies across
     the split, no censoring at the end), untuned LightGBM as the probes fit it, RMSE and the correlation of prediction
     and score (r, blind to a campaign's offset):

     | Test campaign | Children | Columns over half filled | Training mean | `child_age` alone | All features | r: age / all |
     |---|---|---|---|---|---|---|
     | January-March 2022 | 3,003 | 30 | 15.96 | 14.34 | 14.11 | 0.44 / 0.48 |
     | September-November 2022 | 1,276 | 19 | 15.62 | 14.56 | 14.27 | 0.29 / 0.38 |
     | January-May 2023 | 2,334 | 11 | 16.52 | 16.34 | 18.35 | 0.12 / 0.12 |
     | August-November 2023 | 1,642 | 13 | 15.48 | 14.14 | 15.41 | 0.35 / 0.31 |

     | Split | Test children per fold | Training mean | `child_age` alone | All features | r all |
     |---|---|---|---|---|---|
     | Campaigns 2022-2023 (implemented) | 1,276 to 3,003 | 15.89 | 14.84 | 15.53 | 0.32 |
     | Facility, all campaigns (3 folds) | about 6,290 | 15.59 | 14.47 | 12.91 | 0.56 |
     | Facility, surveyed campaigns only (7,168 children, 1,517 facilities) | about 2,390 | 14.92 | 14.16 | 12.77 | 0.53 |
     | Campaigns 2021H1, 2021H2, 2022H1 as windows | 1,004 to 5,902 | 16.14 | 14.44 | 14.42 | 0.41 |

     - Removing each campaign's mean error leaves the shipped split's all-feature RMSE at 14.20 against 12.90 on the
       facility split: the gap is the features, not one offset per campaign as the notes say.
     - The last row breaks the rule on training size (its first window trains on 20% of the children)[^6a].
   * **Effect on the task:** on the shipped split a benchmark ranks models by how well they predict a score from age,
     height and a campaign offset; the 700 survey columns are filled in training and empty in every test row.
   * **Also found (wording, under every option):** the notes give training shares of 56%, 71%, 77% and 89%; the folds
     train on 56%, 72%, 79% and 91% (10,619 to 17,232 children). 21.0% of the January-March 2022 children are at a
     facility number seen earlier, not 24.6%. `dataset check` warns `meta_time_horizon_mismatch`: `campaign` is a
     half-year's first day, so a window spans one day against a 6-month horizon.
   * **Consistency:** a row that lacks the input the prediction acts on is no task row[^6b]; the split mirrors the
     application[^6c]. A small but real signal is no reason to retire[^6d]: the surveyed children carry a clear one.
   * **Unknown:** whether a later campaign of DataDrive2030 runs the facility surveys again (the 2024 Thrive by Five
     Index, `thrive_by_five_index_2024`, is screened in its own record); with it, a campaign split could test them.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Campaigns 2022-2023 (implemented) | as now; notes corrected; the horizon warning accepted | a coming campaign, as you described the use case | no test child has the surveys the use case names; no model beats age alone |
     | B | Facility split, all campaigns | back to issue 3 a: 3 x 3 folds by `id_facility` (numbers shared across studies merge into coarser groups, which cannot leak) | 18,874 children; r 0.56 | learns each campaign's level from its other facilities; the child-only campaigns stay in test |
     | C | Surveyed campaigns only, facility split | keep the 7,168 children of October 2020 to December 2021, 3 x 3 folds by facility; the use case reads "a new facility the surveys reach" | every row has the use case's inputs; r 0.53 | drops 62% of the children; no coming campaign can be tested (three campaigns, the last holds 82%) |

   * **Recommendation:** C: it keeps the rows the use case can be scored on and tests new facilities, which the
     surveys allow; B if the child-only campaigns should stay. **Decision:** A, B or C?

   **Notes for the AI:** on C, filter in `_clean` on `campaign` from 2020-07-01 to 2021-07-01 (state the reason in a
   curation bullet with this issue's tables), restore `Grouping(on="id_facility")` with 3 x 3 folds as before issue 3 c
   and drop `temporal`; drop `campaign` as a feature (it then only marks the round, as `data_year` does).
   `task_summary` (`row`, `split`, `use_case`, `fit_reason`), `splits_comment`, record `required_split` Grouped and
   `Non-IID (Grouped)`, the record's row count. On B, the same split without the filter. On A, correct the three
   numbers in `splits_comment` and the notes, replace "mostly one offset per campaign that no feature predicts" with
   this issue's finding, and add `meta_time_horizon_mismatch` to `accepted_check_warnings` with the reason. Then
   `dataset check`, the task and leak probes, a CHANGELOG entry and a CC line.

   [^6a]: **SPLIT-14** (Must): a temporal task has at least 3 windows, and no window's train side holds less than 50%
     of the data.
   [^6b]: **USE-7** (Must): a row that lacks the input the prediction acts on is no task row: drop it rather than keep
     it as missing.
   [^6c]: **SPLIT-1** (Must): the split is the one that most closely mirrors the real-world application.
   [^6d]: **TP-2** (Should): a small but real signal is no reason to retire.

   **Andrej (2026-11-13, discuss):** Seems like moving to a temporal split from a facility split was a mistake. I
   believe now that we should get back to the use case with facility splits.

   **Resolved (2026-11-13, Andrej):** B. The definition is back to the facility split of before issue 3 c (3 x 3 folds
   by `id_facility`, the new-facility use case, `task_summary` and `grouping` as committed); a curation bullet on the
   time order states why it is not split by campaign, with this issue's numbers, and the `id_facility` bullet of issue
   4 now says the split groups on the number. Record: `required_split` Grouped, `Non-IID (Grouped)`, a CC line;
   `Samples: Over Time`, `Time: Dated` and `Entities: Recur` stay. `dataset check`: 0 errors, 0 warnings, the same
   folds as the committed README. Whether to keep only the surveyed children (option C) is issue 7.

7. **Keep only the children who have the facility surveys?**

   * **Problem:**
     - The facility, practitioner and teacher surveys the use case predicts from exist only in the campaigns of October
       2020 to December 2021 (7,168 of the 18,874 children); the others carry 11 to 64 columns, mostly the child's own.
     - On the facility split the child-only campaigns are scored too, from little more than age and height.
     - Drop the children without the surveys, or keep them?
   * **Experiments:** untuned LightGBM, 3 folds by facility, RMSE (Slurm 1383112):

     | Rows | Children | Scored on | Training mean | `child_age` alone | All features | r all |
     |---|---|---|---|---|---|---|
     | All campaigns (implemented) | 18,874 | all children | 15.59 | 14.47 | 12.91 | 0.56 |
     | All campaigns | 18,874 | the surveyed children | 15.05 | 14.14 | 12.74 | 0.53 |
     | Surveyed campaigns only | 7,168 | the surveyed children | 14.92 | 14.16 | 12.77 | 0.53 |

     - Training on the child-only campaigns too changes nothing for the surveyed children (12.74 against 12.77).
   * **Effect on the task:** with all campaigns, 62% of the test children are scored from child columns alone, which a
     funder with the surveys does not meet.
   * **Consistency:** a row that lacks the input the prediction acts on is no task row[^7a]; missing values of the
     other inputs stay missing.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | All campaigns (implemented) | 18,874 children, 3 x 3 folds by facility | the source as released; more test children | 62% of the test children have none of the surveys the use case names |
     | B | Surveyed campaigns only | keep the 7,168 children of October 2020 to December 2021 (1,517 facility numbers), 3 x 3 folds by facility | every row has the use case's inputs; the same score on those children | drops 62% of the children; the 2016-2019 and 2022-2023 studies leave |

   * **Recommendation:** B: the use case's inputs are the surveys, and the child-only rows add nothing to the surveyed
     children's predictions. **Decision:** A or B?

   **Notes for the AI:** on B, filter in `_clean` on the assessment half-year (`child_date`, else birth date plus age)
   from 2020-07-01 to 2021-12-31 before the columns are dropped, with a curation bullet citing this issue's table and
   USE-7; `task_summary.row` (7,168 children, 2020-2021) and `known`; the record's row count and a CC line;
   `dataset check`, the task probe.

   [^7a]: **USE-7** (Must): a row that lacks the input the prediction acts on is no task row: drop it rather than keep
     it as missing.

   **Andrej (2026-11-13, discuss):** Rethink possible use cases from the feature side that would allow to use as much
   information in terms of sample size but als of feature size as possible

   **Answer (AI, 2026-11-13):** Which use case keeps the most children and the most columns?

   * **Asked:** use cases read from the feature side, with as many rows and as many columns as possible.
   * **Found:** the columns come in modules, and which modules a child has depends on the study, not on the campaign
     alone (a module counts when half its columns are filled):

     | Module | Columns | Children | Where |
     |---|---|---|---|
     | Child's record (age, sex, languages, years in the programme; height in most) | about 30 | 18,874 | every study |
     | Teacher's rating of the child | 21 | 7,785 | 2016-2019 (10%), 2020-2022 (39% to 83%) |
     | Facility observation | 160 | 7,646 | October 2020 to 2022 (32% to 89%) |
     | Registers (children and staff counts) | 73 | 6,873 | October 2020 to 2022 |
     | Principal interview and programme quality | 291 | 2,332 | the 2021 national Index only (40%) |
     | Practitioner interview | 139 | 2,029 | the 2021 national Index only (34%) |

     The combinations: child's record only 8,920 children; with observation, registers and teacher 2,730; teacher only
     2,081; all modules 1,817; others smaller.
   * **Experiment:** the facility split as shipped (9 folds), untuned LightGBM, RMSE on the same test children per tier;
     "pooled" trains on all 18,874 children and 740 columns, "tier only" on the tier's own training children and the
     columns they fill (Slurm 1383202):

     | Test children | Per fold | Training mean | `child_age` alone | Tier only | Pooled | r pooled |
     |---|---|---|---|---|---|---|
     | Child's record only | 2,973 | 15.91 | 14.77 | 13.16 | 12.96 | 0.58 |
     | With the facility observation | 2,549 | 14.94 | 14.09 | 12.79 | 12.79 | 0.51 |
     | With the principal and practitioner interviews | 676 | 14.67 | 14.11 | 12.27 | 12.19 | 0.54 |

     - Pooling costs no tier anything: each scores as well or better than with its own rows only.
     - The child's-record-only children reach r 0.58 here against 0.32 on the campaign split (issue 6), so most of
       their gain over age comes from their campaign, learned from its other facilities: the facility split's known
       caveat (a facility a campaign did not reach).
   * **Use cases, from most rows to most columns:**

     | | Use case | Children | Columns | Pro | Con |
     |---|---|---|---|---|---|
     | A | The child's record plus whichever facility instruments the study ran (implemented, use case reworded) | 18,874 | 740 | the most of both; pooling helps every tier; the child's record, the input the prediction acts on, is in every row[^7b] | 47% of the children carry only their own record; their score leans on the campaign |
     | B | A facility the observation reached | 7,646 | about 520 | every row has the facility's own data, also in 2022 | drops 59% of the children; the interviews are mostly missing |
     | C | A full facility audit (principal, practitioner, programme quality) | about 2,330 | about 545 | every module filled | one study (2021), 12% of the children |
     | D | The child's record alone, every study | 18,874 | about 15 | every column filled in every row | throws away the facility data, the source's question |

   * **Recommendation:** A, with the use case written so: "a funder estimates a child's score from the child's record and
     whichever facility instruments its study ran (observation, registers, teacher rating; in the national Index also
     the principal and practitioner interviews)". It keeps every child and every column and loses nothing on any tier.
     **Decision:** A, B, C or D?

   **Notes for the AI:** on A, change `task_summary.use_case`, `known` and `fit_reason` (the modules and their shares;
   the child's-record-only rows lean on the campaign) and a curation bullet with this answer's two tables; no change
   to the rows or the split. On B, filter in `_clean` on rows with half the 160 observation columns filled (before the
   columns are dropped); on C, on the principal interview; on D, keep only the core columns. Each: `dataset check`, a
   record CC line, the CHANGELOG.

   [^7b]: **USE-7** (Must): a row that lacks the input the prediction acts on is no task row; missing values of the
     other inputs stay missing.

   **Andrej (2026-11-13, chat):** I agree - rebuild and then review it

   **Resolved (2026-11-13, Andrej):** A. Rows and columns unchanged; `task_summary.use_case`, `known` (the modules and
   their shares) and `fit_reason` (47% with their own record only, leaning on their campaign) reworded, a curation
   bullet with the answer's two tables, a record CC line. Built on Andrej's ask.

8. **Type the three remaining free-text "other" answers as strings?**

   * **Problem:**
     - `pri_fees_exceptions_other` (124 different answers in 581 children), `pri_expenseother` (83 in 582) and
       `pra_online_training_details` (66 in 346) are the enumerators' free text, typed as categories.
     - The cleaning of 2026-10-30 made the 26 other free-text columns strings; these three were not in its list.
     - Make them strings like the others?
   * **Experiments:** the dtype probe on the built container flags `pri_fees_exceptions_other`; a sweep of the
     category columns for levels of several words found the other two (e.g. "SOME PARENTS CAN'T AFFORD AT ALL AND ALSO
     STAFF MEMBERS ARE NOT ALLOWED TO PAY", "TV LICENSE, DSTV, TOILETRIES").
   * **Consistency:** an open-ended answer is text, not a category[^8a]; the same call as the other 26 columns.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Categories (implemented) | as built | no change | 66 to 124 one-off levels each; unlike the other 26 free-text columns |
     | B | Strings | move the three from `categorical` to `string` in `_feature_types` | the same type as the other free text | a rebuild |

   * **Recommendation:** B. **Decision:** A or B?

   **Notes for the AI:** on B, move the three names, extend the 2026-10-30 curation bullet (26 → 29 columns),
   `dataset check`, CHANGELOG, record CC, rebuild on the curator's ask.

   [^8a]: **CLEAN-14** (Should): a column's type follows its meaning from the context.

   **Andrej (2026-11-13, change):** Option B: Strings.

   **Resolved (2026-11-13, Andrej):** B. The three columns moved from `categorical` to `string` (29 string columns);
   the 2026-10-30 curation bullet names them; record CC. `dataset check`: 0 errors, 0 warnings.

9. **Drop the multi-select lists that copy their yes/no columns?**

   * **Problem:**
     - `obs_materials` (1,134 different values), `obs_area` (167), `obs_hazard` (94) and `pri_covid_precautions` (33)
       hold the codes a facility ticked as one space-separated string, typed as a category.
     - Each has one yes/no column per code (`obs_materials_0` to `obs_materials_97`, 22 columns, and so on), and the
       list and the columns agree in every cell where both are filled; no list is filled where its columns are not.
     - Drop the lists, keeping the yes/no columns?
   * **Experiments:** on the built container, per list: rows with both, cells where list and column disagree:

     | List | Values | Yes/no columns | Rows | Disagreeing cells |
     |---|---|---|---|---|
     | `obs_materials` | 1,134 | 22 | 7,657 | 0 |
     | `obs_area` | 167 | 9 | 7,646 | 0 |
     | `obs_hazard` | 94 | 10 | 2,343 | 0 |
     | `pri_covid_precautions` | 33 | 7 | 2,332 | 0 |
     | `pri_covid_awareness` | 18 | 5 | 2,332 | 55 |

   * **Effect on the task:** as a category, a list is a near-unique id of a facility's ticks (1,134 levels for 7,657
     children), which a model can only match, not generalise; its content is already in the yes/no columns.
   * **Consistency:** a column leaves for what it is, and a copy is a reason[^9a].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep (implemented) | as built | no change | five near-unique categories that repeat 53 columns |
     | B | Drop the four exact copies | `obs_materials`, `obs_area`, `obs_hazard`, `pri_covid_precautions` dropped | no information lost (0 disagreeing cells) | `pri_covid_awareness` stays until its 55 cells are explained |
     | C | Drop all five | B plus `pri_covid_awareness` | one form for every multi-select question | 55 cells where the list says more or other than its columns |

   * **Recommendation:** B; C once the 55 cells are read. **Decision:** A, B or C?

   **Notes for the AI:** on B, add the four to `drop_columns` with a comment, a curation bullet with the table,
   `dataset check`, CHANGELOG, record CC, rebuild on the curator's ask. On C, first read the 55 cells of
   `pri_covid_awareness` against the codebook.

   [^9a]: **CLEAN-22** (Must): columns leave for what they are (a leak, an identifier, a copy, ...), never for how
     many there are.

   **Andrej (2026-11-13, change):** Option B: Drop the four exact copies.

   **Resolved (2026-11-13, Andrej):** B. `obs_materials`, `obs_area`, `obs_hazard` and `pri_covid_precautions` are in
   `drop_columns` with a curation bullet and this issue's numbers; `pri_covid_awareness` stays; 735 features; record CC.
   `dataset check`: 0 errors, 0 warnings. Not rebuilt: the container `01a1d456` predates both changes.

## Reference

DataDrive2030. ELOM and Thrive by Five Index 2016-2023, Merged Data [dataset]. Version 1. Cape Town: DataDrive2030 [producer], 2024. Cape Town: DataFirst [distributor], 2024. DOI: https://doi.org/10.25828/WG0D-Y909
