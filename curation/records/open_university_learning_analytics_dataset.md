---
unique_name: open_university_learning_analytics_dataset
name: Open University Learning Analytics dataset
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
suggestion: No (Retired)
decision_markers:
- Needs extensive data wrangling
- Too Small
tags:
- Non-IID (Grouped)
- 'Samples: Over Time'
- 'Time: Dated'
- 'Target: Fixed Delay'
- 'Entities: Recur'
- Dated Event Log
collections:
- New (BeyondArena)
original_source: Website
year: '2015'
collection_period: 2013-2014
domain: education
required_split:
- Grouped (NON-IID)
problem_type: Multiclass Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.24432/C5KK69
- https://analyse.kmi.open.ac.uk/
- https://analyse.kmi.open.ac.uk/open-dataset
- https://doi.org/10.6084/m9.figshare.5081998.v1
source_row: 738
type_adapter_id: curation-record-v1
---

## Comments

Could be transformed into a prediction task https://www.kaggle.com/code/devassaxd/student-performance-prediction-complete-analysis#Part-3:-Modeling

On the website they also talk about their predictive models

Use cases of the data (?):
https://dl.acm.org/doi/10.1145/3576050.3576061

https://www.sciencedirect.com/science/article/pii/S2666920X22000637?via%3Dihub (explains how to do feature selection for the task?)

We might follow the Kaggle notebook as it seems to know more of the data and use case. Seems reasonable in most cases for the task. Could be made for several tasks, unclear which one would be best

**Assessment (AI, 2026-10-07):** The task is final_result (four classes) on day 60 for the 26,395 registrations active then, using only what is known by day 60. The Kaggle notebook above uses the exam score, so it leaks the result. The OU trains on other presentations of a module (OULAD page: "the J presentation must be used to inform the B presentation or vice versa"). Four start dates cannot give three temporal windows, so the split holds out whole presentations. LightGBM log-loss skill: IID 0.193, grouped 0.141, 2014J hold-out 0.099. BBB 2014J marks its first TMA 1 or 100 (weight 0), and models score below the prior there. Data: figshare 10.6084/m9.figshare.5081998.v1 (CC BY 4.0); the OU link is dead.

**Assessment (AI, 2026-10-20):** priority 3 for the review of the added dataset: gap + (problem_type multiclass_classification), use case -, source +, shape +, risk - (Issue 5: recurring students leak across folds, kept; features built from seven joined tables). Large, well-sourced education multiclass task with real grouped structure; its day-60 framing and multi-table features are our own choices.

**Assessment (AI, 2026-10-20):** Review panel (re-check): ship after changes, made in the definition. A per-fold train filter now drops the concurrent and later registrations of each fold's test students (LEAK-17; 577-901 train rows per split; its effect net of random removal is not distinguishable from zero), and weight-0 TMA marks are left out of score_mean/score_min (USE-6; 1,655 rows, 1,652 of BBB 2014J, whose first TMA is marked 1 or 100). Untuned LightGBM log-loss skill 0.167 (sd 0.015 over 9 splits, was 0.141 and 0.052); random forest, LightGBM and logistic regression now score alike (no_spread, TP-3: read the first tuned run). The figshare md5 matches and all seven CSVs are byte-identical. Open: the SPLIT-14 amendment for the three too-few-periods datasets, the day-60 marks against the LEAK-10 earlier-grades row, the assumed 14-day TMA marking delay, the scope of the weight-0 change and the dataset pending tuned results (Review issues 1, 11, 4, 9, 12). Priority 3: gap + (problem_type multiclass_classification), use case - (fit approximate; day 60 and the four-class target are our framing), source + (OU page and Sci. Data paper), shape + (26,395 units, 40 features, grouped), risk - (seven joined tables; ships only after the SPLIT-14 amendment).

CC (2026-10-21, Lennart): ok on the cross-dataset item: LEAK-10's grades row now reads "earlier grades not yet known at the prediction point: drop them"; the day-60 assessment marks stay (Cases row in leak_checks.md).

CC (2026-10-21, Lennart): option (a) of the cross-dataset item on tasks with too few periods: the closest regime that keeps the rows, tagged as forced from temporal, with the cost measured against the valid windows (SPLIT-8 amended).

**Assessment (AI, 2026-10-21):** tagged `ForcedGroupedFromTemporal`. Cost: on the one valid window (test 2014J) untuned LightGBM log loss 1.205 grouped against 1.185 temporal, same ranking of three model families (review panel, 2026-10-20, before the train filter and the weight-0 change). Review issue 1 settled.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback log_loss — The source is a data descriptor (OU Analyse open dataset) with no prediction task or metric; our day-60 four-class task is our construction.

CC (2026-10-22, Lennart): issue 4: keep the 14-day TMA marking delay with its note. Issue 9: leave only the weight-0 TMA marks out of the scores; FFF's graded quizzes stay. Issue 12: keep the dataset despite `no_spread` and mark it for later: re-check with the first tuned run (TP-3).

**Assessment (AI, 2026-10-22):** all three issues settled as implemented; a `Spread (TP-3)` bullet in the notes and a TP-3 cases row in task_probes.md mark the re-check with the first tuned run. REVIEW.md removed (nothing left open). Not built yet.

CC (2026-10-26, Lennart): verdict ship.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): 3 ordinal scales typed as ordered categories in the codebook's order (CLEAN-14, amended): `highest_education`, `imd_band`, `age_band` (the README lists their levels).

CC (2026-11-20, Andrej): Review issue 1, C: the split holds out one start date at a time (4 splits, 66.5-83.7% training after the student filter), because the relation is measured not flat for every start date even with the other three, later ones included, in training; the module-presentation folds mixed concurrent presentations into training.

CC (2026-11-20, Andrej): retired as `Too Small` (Review issue 2, C): the relation is measured not flat across start dates, and a forward split that trains only on cohorts concluded before the test cohort starts exists once (2014J); one start date out at a time trained on later and unfinished cohorts (0.04 log loss easier for 2014B at equal size), and the module-presentation folds on concurrent ones.

## Review

**Outcome:** added. Settled on the review of 2026-10-20 to 2026-10-26 (Lennart: verdict ship); reopened on
2026-11-19 by the split check, as the stationary-relation test reads the relation not flat across the start dates.

**Main points:** Retired as `Too Small` (issue 2): the four start dates give one forward split on concluded cohorts; issue 1 chose one start date out at a time, which trained on later cohorts.

**Issues for Andrej:**

1. **Split: hold out whole start dates instead of module-presentations, now that the relation is measured not flat?**

   * **Problem:**
     - The stationary-relation test (2026-11-19) reads the relation not flat across the four start dates: tested on
       2014J, training on the earlier start dates costs more log loss than training on as many 2014J rows, by far more
       than the test's floor.

       | Test start date | Model | Gap (log loss) | SD over 5 seeds | Floor | Verdict |
       |---|---|---|---|---|---|
       | 2014J | LightGBM | +0.040 | 0.002 | 0.0025 | not flat |
       | 2014J | Kumo-Tabular | +0.045 | 0.003 | 0.0027 | not flat |
       | 2014B | LightGBM | +0.015 | 0.005 | 0.0024 | not flat |

     - Since 2026-11-18 a relation measured not flat is held out by whole periods, four for a task of 3 repeats, or
       the task is `Too Small`; never by the unit[^split16]. The definition holds out module-presentations (22 runs
       of 7 modules): 67% of a fold's training rows come from presentations running at the same time as the test
       ones, so a fold does not test a start date the model has not seen.
     - The grouping was chosen on 2026-10-21 (Lennart, option (a): forced grouped), before any stationarity verdict;
       the `Time basis:` line does not give the verdict[^split32].
     - Rows per start date: 2013B 3,924 (14.9%), 2013J 7,445 (28.2%), 2014B 6,191 (23.5%), 2014J 8,835 (33.5%).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep module-presentations (implemented) | Split unchanged; the splits comment gives the reason a module-presentation stands for a period, and the `Time basis:` line the verdict | 22 groups, six to nine per test fold | Most training rows run at the same time as the test rows, which the measured drift makes easier than deployment |
     | B | Group on the start date (4 groups) | `grouping` on the start date, grouped 3-fold CV with 3 repeats (six distinct groupings of four dates); the train filter keeps dropping test students' later registrations; `Time basis:` line with the verdict; a rebuild | Every fold tests whole start dates no training row shares | Only four groups: a fold holding two dates (up to 62% of the rows) trains on 38%; a fold may train on later dates for an earlier one |

   * **Recommendation:** B, the path the rules give a relation measured not flat, and four start dates are enough
     for 3 repeats. **Decision:** A or B?

   **Notes for the AI:** on B, `Grouping(on=...)` moves to the start date (code_presentation, dropped as a feature
   after the split), the splits comment, `task_summary.split`, the `Time basis:` line, the departure table entry and
   SPLIT-8's Cases row change; on A, the reason goes in the splits comment and the departure table.

   **Andrej (2026-11-19, discuss):** Wouldn't be an alternatice to get closer to 9 splits be to holdout single classes?

   **Answer (AI, 2026-11-19):** yes, if a held-out class (a module-presentation, one run of a course) keeps its whole start date out of training: then no training row runs at the same time as the test rows, and there are 22 such splits, more than the 9 of the target.

   * **The four start dates and 22 presentations** (26,395 registrations):

     | Start date | Presentations | Registrations | Rows per presentation | Training if this date is left out |
     |---|---|---|---|---|
     | 2013B | 3 (BBB, DDD, FFF) | 3,924 | 1,075 to 1,454 | 85.1% |
     | 2013J | 6 (AAA, BBB, DDD, EEE, FFF, GGG) | 7,445 | 363 to 1,910 | 71.8% |
     | 2014B | 6 (BBB, CCC, DDD, EEE, FFF, GGG) | 6,191 | 586 to 1,352 | 76.5% |
     | 2014J | 7 (AAA to GGG) | 8,835 | 340 to 1,868 | 66.5% |

   * **The layouts:**

     | | Option | Splits | Test registrations | Training | Rows running at the same time as the test in training |
     |---|---|---|---|---|---|
     | A | 3 x 3 folds over the 22 presentations (implemented) | 9 | 6 to 9 presentations a fold | about two thirds | 67% of training rows |
     | B | 3 x 3 folds over the 4 start dates | 9 (6 distinct groupings) | one or two dates | 38% to 85% | none |
     | C | One start date held out at a time | 4 | 3,924 to 8,835 | 66.5% to 85.1% | none |
     | D | One presentation held out at a time, its start date out of training | 22 | 340 to 1,910 | 66.5% to 85.1% | none |

   * D tests each course run on its own, with the same training a whole-date hold-out gives; it differs from C only in scoring each presentation separately, which gives 22 splits instead of 4.
   * Both B and D train partly on later start dates, as every grouped split does; the student filter (a test student's concurrent and later registrations out of training) stays in each.
   * With D, the 22 splits are more than the target of 9; the test sizes vary fivefold (340 to 1,910).

   **Recommendation:** D: it holds out whole periods from training, as the rules ask for a relation measured not flat, and reaches more than the 9 splits; C if you prefer one score per start date. **Decision:** A, B, C or D?

   **Notes for the AI:** on D, `_make_splits` builds one split per module-presentation: test = its rows, train = the rows of the other three start dates, then the student filter; `data_tags` stays `ForcedGroupedFromTemporal`; the `Time basis:` line gives the v3 verdict (not flat: +0.040 to +0.045 log loss on 2014J); splits comment and task summary; rebuild and `dataset check`.

   **Andrej (2026-11-19, discuss):** Do the presentations, like AAA in two different start dates, mean the same course? Could we group by course simulating a new course as the use case?

   **Answer (AI, 2026-11-19):** yes, AAA 2013J and AAA 2014J are two runs of the same module (course); grouping by module would test a course the model has never seen, a different use case from the one the definition states.

   * **The modules:** seven, each run two to four times; registrations per module:

     | Module | Presentations | Registrations |
     |---|---|---|
     | AAA | 2013J, 2014J | 703 |
     | BBB | 2013B, 2013J, 2014B, 2014J | 6,226 |
     | CCC | 2014B, 2014J | 3,220 |
     | DDD | 2013B, 2013J, 2014B, 2014J | 5,017 |
     | EEE | 2013J, 2014B, 2014J | 2,485 |
     | FFF | 2013B, 2013J, 2014B, 2014J | 6,338 |
     | GGG | 2013J, 2014B, 2014J | 2,406 |

   * **The use case today:** OU Analyse scores the students of a running presentation with a model trained on earlier presentations of the same module (the OULAD page: each presentation "informed by the previous one of its kind"). A new course is the case where no earlier presentation exists; OU Analyse then uses other modules, so it is a real but different task.
   * **As a split:** E, 3-fold CV over the seven modules with 3 repeats (9 splits); folds of very unequal size (AAA 703 to FFF 6,338 registrations); students who take several modules recur across groups, so the student filter would stay; modules differ in subject and assessment design, so the score would mostly measure transfer between subjects.

   | | Option | Splits | What it tests |
   |---|---|---|---|
   | D | One presentation held out at a time, its start date out of training | 22 | a new run of a known course, nothing concurrent in training |
   | E | 3 x 3 folds over the seven modules | 9 | a course the model has never seen |

   **Recommendation:** D, because it keeps the use case the definition and the source describe; E only if the task's use case changes to new courses. **Decision:** A, B, C, D or E?

   **Andrej (2026-11-20, discuss):** Show me how the split train test sizes would look like with each option

   **Answer (AI, 2026-11-20):** counted on the definition's frame (26,395 registrations); A as shipped (with the student filter), B and E with the framework's own grouped 3 x 3 folds (before the student filter, which removes 3-6% of a train side).

   | | Option | Splits | Train registrations | Train share | Test registrations |
   |---|---|---|---|---|---|
   | A | 3 x 3 over the 22 presentations (shipped) | 9 | 14,931-17,946 | 56.6-68.0% | 7,694-10,563 |
   | B | 3 x 3 over the 4 start dates | 9 (6 distinct test sets) | 11,369-22,471 | 43.1-85.1% | 3,924-15,026 |
   | C | one start date held out | 4 | 17,560-22,471 | 66.5-85.1% | 3,924-8,835 |
   | D | one presentation held out, its start date out of training | 22 | 17,560-22,471 | 66.5-85.1% | 340-1,910 |
   | E | 3 x 3 over the 7 modules | 9 | 11,820-23,207 | 44.8-87.9% | 3,188-14,575 |

   * **B, fold by fold:** a fold holding two start dates tests 12,759 or 15,026 registrations and trains on 43-52%; the four single dates repeat across repeats (2013J and 2014B twice), so 9 splits hold 6 distinct test sets.
   * **C and D:** the train side of a held-out start date is the other three dates: 17,560 (2014J out), 18,950 (2013J), 20,204 (2014B), 22,471 (2013B).
   * **D per presentation:** test sizes by start date: 2013B 1,075-1,454; 2013J 363-1,910; 2014B 586-1,352; 2014J 340-1,868 (AAA the smallest, 340 and 363).
   * **E:** module sizes differ more than fivefold (AAA 703 to FFF 6,338), so folds range from 3,188 to 14,575 test registrations (87.9% to 44.8% train).

   **Recommendation:** D, unchanged: no training row runs at the same time as a test row, every train side holds two thirds or more, and every test presentation is far above the minimum; C if one score per start date is preferred. **Decision:** A, B, C, D or E?

   **Andrej (2026-11-20, discuss):** But we don't need 22 splits, so I am not sure about your suggestion.

   **Answer (AI, 2026-11-20):** agreed, 22 are more than needed; C gives the same clean hold-out with four splits, one per start date.

   * **C, one start date held out at a time:** 4 splits, train 66.5-85.1% (17,560-22,471 registrations), test 3,924-8,835; the test date's presentations are all held out together, so nothing in training runs at the same time; the student filter stays.
   * Four splits are fewer than the 9 an IID split would get, which the rules accept (never under three) with the reason written: four start dates.
   * B (3 x 3 over the four dates) reaches 9 by regrouping the same four dates: 6 distinct test sets, folds down to 43% training.
   * D (22 splits) scores each course run separately with the same training as C; it adds splits, not new information.

   **Recommendation:** C. **Decision:** A, B, C, D or E?

   **Andrej (2026-11-20, discuss):** Give me the options in the panel again

   **Answer (AI, 2026-11-20):** all options in one panel (26,395 registrations; the student filter applies to every option and removes 3-6% of a train side).

   | | Option | What it does | Splits | Train share | Test registrations | Pro | Con |
   |---|---|---|---|---|---|---|---|
   | A | 3 x 3 folds over the 22 module-presentations (implemented) | groups = one run of one course | 9 | 56.6-68.0% | 7,694-10,563 | the target count; balanced folds | 67% of a fold's training rows run at the same time as its test rows, while the relation is measured not flat across start dates |
   | B | 3 x 3 folds over the 4 start dates | groups = whole start dates | 9 (6 distinct test sets) | 43.1-85.1% | 3,924-15,026 | whole periods, nothing concurrent | test sets repeat across repeats; folds of two dates train on 43-52% |
   | C | One start date held out at a time | leave one period out | 4 | 66.5-85.1% | 3,924-8,835 | whole periods, nothing concurrent, each date tested once | 4 of 9 splits (accepted with the reason: four start dates) |
   | D | One presentation held out, its start date out of training | as C, scored per course run | 22 | 66.5-85.1% | 340-1,910 | per-course scores | more splits than needed, no new information over C |
   | E | 3 x 3 folds over the 7 modules | groups = whole courses | 9 | 44.8-87.9% | 3,188-14,575 | tests a course never seen | a different use case (a new course); folds very unequal |

   **Recommendation:** C: it holds whole start dates out, as the rules ask for a relation measured not flat, with no concurrent rows in training and every train side above two thirds. **Decision:** A, B, C, D or E?

   **Andrej (2026-11-20, discuss):** Do a stationarity test on the one start date held out suggestion.

   **Answer (AI, 2026-11-20):** all four start dates read not flat with the other three in training (5 seeds, all rows, both models): no start date is taught by the others as well as by itself, even with later dates in training, so C, which holds each date out whole, is the split the rules ask for.

   * **Setup:** for each held-out start date, a model trained on the other three dates (earlier and later, as C trains) against one trained on as many rows of the held-out date itself, both scored on the rest of that date's rows; log loss; LightGBM and Kumo-Tabular, 5 seeds; a gap above both two SDs and the floor reads not flat.
   * **Results:**

     | Held-out date | LightGBM gap | Floors | Kumo-Tabular gap | Floors | Verdict |
     |---|---|---|---|---|---|
     | 2013B | +0.022 ± 0.007 | 8.4 | +0.095 ± 0.018 | 33.3 | not flat |
     | 2013J | +0.011 ± 0.002 | 4.7 | +0.014 ± 0.001 | 5.5 | not flat |
     | 2014B | +0.011 ± 0.003 | 3.9 | +0.020 ± 0.002 | 6.5 | not flat |
     | 2014J | +0.040 ± 0.002 | 16.0 | +0.045 ± 0.003 | 16.6 | not flat |

     For 2014J, the newest date, "the other dates" are exactly the earlier ones, so it repeats the test of 2026-11-19. Quick one-seed runs posted earlier today read 2013J and 2014B near flat; the full runs do not confirm that.
   * **What it means for C:** the relation differs by start date at both ends and in the middle, most for the oldest (2013B) and the newest (2014J). A split that mixes a date's rows into training (A, module-presentations) scores the model on a date it has partly seen; C scores each date unseen, as deployment meets the next presentation.

   **Recommendation:** C, unchanged. **Decision:** A, B, C, D or E?

   **Andrej (2026-11-20, discuss):** Agree.

   **Resolved (2026-11-20, Andrej):** C: one start date held out at a time, 1 repeat x 4 folds, grouped on the new `start_date` column (no input); the train filter keeps dropping test students' later registrations.

   | Test start date | Test rows | Train after filter (share) | Test rows with a student in training |
   |---|---|---|---|
   | 2013B | 3,924 | 22,091 (83.7%) | 0% |
   | 2013J | 7,445 | 17,944 (68.0%) | 1.3% |
   | 2014B | 6,191 | 19,703 (74.6%) | 9.2% |
   | 2014J | 8,835 | 17,560 (66.5%) | 13.2% |

   The `Time basis:` line gives the stationarity test (all four dates not flat); `ForcedGroupedFromTemporal` kept (whole periods held out, as online_shoppers); 4 of 9 splits and the few, large groups accepted with this decision. `dataset check`: 0 errors, 0 warnings. Not rebuilt.

   [^split16]: **SPLIT-16** (Must): a relation measured not stationary is never split by the unit or at random: whole periods are held out where there are enough for the task's repeats (four for 3 repeats, five for 10 or 20), else the task is `Too Small`.

   [^split32]: **SPLIT-32** (Should): where the data holds two or more periods, the stationary-relation test is run and its verdict goes into the `Time basis:` line; a relation measured flat keeps the split random, tagged `StationaryRelation`.

2. **Option C trains on later start dates: keep it, or test forward only?**

   * **Problem:**
     - Three of C's four splits train on start dates after the test date (2013B on all three later dates, 2013J on 2014B and 2014J, 2014B on 2014J), which a deployed model never has (your question of 2026-11-20: "we now have temporal leakage, especially if students match in train and test?").
     - At the same training size, those later dates make the held-out date far easier than the earlier dates alone: 0.039 log loss for 2014B, 0.36 for 2013J; C's full training side gains more.
     - Student overlap is no leak: the train filter drops a test student's later registrations, so only earlier ones stay (0%, 1.3%, 9.2% and 13.2% of the test rows by date).
   * **Measured** (LightGBM, 3 seeds, the definition's frame; log loss, lower is better; macro ROC AUC):

     | Test start date | Training side | Train rows (share) | Log loss | ROC AUC |
     |---|---|---|---|---|
     | 2013J | earlier dates only (2013B) | 3,924 (14.9%) | 1.421 | 0.696 |
     | 2013J | C cut to that size | 3,924 | 1.058 | 0.739 |
     | 2013J | C | 17,944 (68.0%) | 0.970 | 0.768 |
     | 2014B | earlier dates only | 11,369 (43.1%) | 1.099 | 0.750 |
     | 2014B | C cut to that size | 11,369 | 1.060 | 0.762 |
     | 2014B | C | 19,703 (74.6%) | 1.040 | 0.767 |
     | 2014J | earlier dates only = C | 17,560 (66.5%) | 1.038 | 0.754 |

     The 2013J gap is partly modules that 2013B does not run; 2014B's 0.039 is the cleaner reading. Only 2014J is forward under C.
   * **Your earlier curation of the same data** (the relational OULAD task): rolling-origin splits over the four cohorts, "not per-module-presentation", with a training cohort admitted only once it has concluded by the test cohort's start. A presentation runs about 261-269 days, longer than the four months between starts, so 2013J's results did not exist when 2014B began (nor at our prediction point, day 60 of 2014B). That gives: 2013J trained on 2013B; 2014B trained on 2013B only; 2014J trained on 2013B, 2013J and 2014B. Repeated evaluation came from several prediction days per split (days 7, 14, 21, 28), not from more cohorts.
   * **The concluded-cohort rule here:** C breaks it twice (later cohorts, and earlier cohorts still running). Forward splits that keep it:

     | Test cohort | Training cohorts | Train rows (share) |
     |---|---|---|
     | 2013J | 2013B | 3,924 (14.9%) |
     | 2014B | 2013B | 3,924 (14.9%) |
     | 2014J | 2013B, 2013J, 2014B | 17,560 (66.5%) |

     Only 2014J trains on half or more; 2013J and 2014B share one training side, so they count as one split (splits are counted by distinct training sides), and both train on 14.9%, under the 30% floor of any exception.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep C (implemented), as a stated departure | one start date out at a time; the splits comment names the later and unfinished cohorts in training | every start date tested; 66.5-83.7% training | trains on cohorts whose results did not exist yet: 0.04 log loss easier for 2014B at equal size; the departure stands against the concluded-cohort rule you used before |
     | B | Lennart's grouped folds | 3 x 3 folds over the 22 module-presentations (as on 2026-10-21) | 9 splits, the original call | 67% of a fold's training rows run at the same time as the test rows; the same leak as A, larger |
     | C | Retire as `Too Small` | `No (Retired)`, `Too Small`; the folder goes in a retirement PR | no split that leaks or repeats a training side | loses the dataset; the relation is measured not flat, and the forward cohorts give one valid split |
     | D | A new task: several prediction days | rows = registration x prediction day (e.g. days 30, 60, 90; every table cut at that day, as in the relational task); forward splits on concluded cohorts, newest 2014J tested at each day | no leak; training sides differ by prediction day | a different task and a rebuild; 2014J is the only test cohort, so every split tests October 2014; training on the same students at each day |

   * **Recommendation:** C (`Too Small`): with your concluded-cohort rule and distinct training sides, the four cohorts give one valid split; D only if a multi-day task is worth a rebuild, and A only as a stated departure. **Decision:** A, B, C or D?

   **Andrej (2026-11-20, change):** Option C: Retire as Too Small.

   **Resolved (2026-11-20, Andrej):** C: retired as `Too Small`. With training cohorts admitted only once concluded, and splits counted by distinct training sides, the four start dates give one valid forward split (2014J on 66.5%); every other layout trains on later or unfinished cohorts (A, and issue 1's C) or on concurrent presentations (Lennart's grouped folds). The definition is back to its last committed state (issue 1's C reverted); the folder leaves in a retirement PR.

## Reference

Kuzilek J., Hlosta M., Zdrahal Z. Open University Learning Analytics dataset Sci. Data 4:170171 doi: 10.1038/sdata.2017.171 (2017).
