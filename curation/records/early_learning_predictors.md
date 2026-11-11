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
- 'Samples: Over Time'
- 'Time: Dated'
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

CC (2026-11-11, Andrej): BeyondArena v0.2 review page, early_learning_predictors:
- Issue 3 (split by time) marked `discuss` again ("we actually want to generalize to new unseen facilities ... but if there is temporal drift that might be a problem") and stays open. Reassessed: the grouped + temporal option holds out whole facilities too, so it tests the unseen-facility question and adds the forward direction; the drift is not only a level shift (taking one offset per window out still leaves +0.4 to +3.3 RMSE over the facility split on the same children, untuned LightGBM). The recommendation stays grouped + temporal; the facility split stays implemented in the meantime.
- The review moved from the folder's file into this record's `## Review` section.

## Review

**Outcome:** added. DataDrive2030's merged ELOM and Thrive by Five Index data 2016-2023 (DataFirst, CC BY,
https://doi.org/10.25828/WG0D-Y909), the data of Zindi's Early Learning Predictors Challenge: 18,874 children aged
50-69 months assessed at 2,541 early learning facilities in South Africa; the target is the child's total score on the
Early Learning Outcomes Measure (ELOM, a standard test of 23 items over five areas of development), predicted from 739
features of the child, the facility, the practitioner and the teacher; split by facility, scored by RMSE (Zindi's
metric). The AI recommends shipping it as defined. Reviewed on 2026-11-04 without a panel, from the gathered evidence
(the record, the CHANGELOG, the definition's notes); no model run exists for it. Validity: the parts and other
versions of the score, the other child assessments (`_sef`, `child_observe_*`), the survey year, the assessors' and
other ids and the data-collection timers are dropped, so no feature is read off the test; the facility split matches
a new facility; the source's question is explanatory, and the definition's use case (a funder estimating children's
scores at a new facility without a full assessment) is the curation's, rated approximate, as `fit_reason` says; some
surveys were made after the assessment, which `fit_reason` names. Value: untested here (no model run, no task
probe on record); Zindi ran it as a prediction challenge. Quality: 80% of the cells are missing, survey rounds asked
different questions, and the Stata missing codes, ordinal scales and codes are settled (Lennart, 2026-10-30 to
2026-11-01). Weighed: a documented survey with a codebook and a DOI +, a facility split +, an explanatory source and
features that mix survey rounds -, value unmeasured.

**Main points:** Ship as defined (issue 1)? Split by assessment date with the test facilities held out, or keep the
facility split with no time-basis tag, 0.3 to 4.8 RMSE below what later rounds cost (issue 3)? New on 2026-11-10:
the drift is a jump between survey rounds (mean 54.2, 40.9, 52.5 in three half-years), and grouped + temporal holds out
unseen facilities too (issue 3, answer)?

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

   **Andrej (2026-11-11, discuss):** Reassess this again, we actually want to generalize to new unseen facilities in
   this case but if there is temporal drift that might be a problem. So think again.

   **Answer (AI, 2026-11-11):** Reassessed, no new measurement; nothing in the numbers of 2026-11-10 changes the
   reading, and B is the only option that gives you unseen facilities *and* answers the drift. B stays the
   recommendation; the one fact that could move it to A is a judgement, not a measurement.

   * **Your goal is not in tension with B:** B is grouped *and* temporal. Every test child in a window belongs to a
     facility whose rows are all out of training, so B tests exactly the generalisation A tests, over a subset of
     the children, and adds the forward direction on top. C (temporal only) is the option that gives up unseen
     facilities, and it is worse than B in all four windows (+0.1 to +0.8 RMSE).
   * **The drift is not only a level that a practitioner could recalibrate:** taking one offset per window out still
     leaves B above A on the same children in all four windows.

     | Test window | Children | Train share (B) | B | B minus its offset | A, same children | B minus offset, cost over A |
     |---|---|---|---|---|---|---|
     | Jan-Jun 2022 | 2,706 | 53% | 14.08 | 14.07 | 13.49 | +0.58 |
     | Jul-Dec 2022 | 1,196 | 71% | 14.24 | 13.65 | 13.23 | +0.42 |
     | Jan-Jun 2023 | 2,338 | 61% | 17.54 | 15.76 | 12.51 | +3.25 |
     | Jul-Dec 2023 | 1,638 | 87% | 15.28 | 14.04 | 13.16 | +0.88 |

   * **So A is optimistic for a reason beyond the shift in the mean:** under A a test child's round is learned from
     other facilities of the same and later rounds (a model tells a window's children from the earlier ones at ROC
     AUC 0.998 to 1.000 with dates and age removed), which a funder scoring a coming round does not have.
   * **The one real argument for A, unchanged and not settleable by a measurement:** each window is a new survey
     round as much as a new date (early 2023 lacks 159 columns the earlier rounds filled), so B partly scores
     transfer across questionnaires. If the rounds are read as a redesign of the instrument rather than as drift in
     the world, A is the honest split and the redesign is a defect of the release, not of the task.
   * **Not measured:** the 2016-2021 rounds as windows (too few dated children before 2021 for a fourth window that
     trains on half the data), and whether a feature subset common to all rounds removes the round offset.
   * **Options:** unchanged from the answer above.

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Grouped only (implemented) | 3 x 3 folds by facility, all rounds | most test rows; stable scores; no questionnaire transfer in the score | trains on the test round; 0.4 to 3.3 RMSE kinder than a coming round even after the offset |
     | b | Grouped + temporal | 4 six-month windows from 2022-01-01, the test facilities' earlier rows out of training | unseen facilities *and* the forward direction, the use case | 4 small test sets; each window is a new questionnaire as much as a new date |
     | c | Temporal only | the same 4 windows, all earlier rows kept | more training rows | tests facilities already seen; worse than b everywhere |

   * **Recommendation:** b, unchanged. **Decision:** b, a or c?

## Reference

DataDrive2030. ELOM and Thrive by Five Index 2016-2023, Merged Data [dataset]. Version 1. Cape Town: DataDrive2030 [producer], 2024. Cape Town: DataFirst [distributor], 2024. DOI: https://doi.org/10.25828/WG0D-Y909
