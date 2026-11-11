---
unique_name: lending_club
name: lending_club
checked_by:
- Lennart
- Alex
- Mustafa
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
priority: 3
tags:
- Free Text (Sentences)
- Non-IID (Temporal)
- 'Samples: Over Time'
- 'Time: Dated'
- 'Target: Varying Delay'
- 'Entities: Recur'
collections:
- TexTabBench Extra
- STRABLE
original_source: Company
year: '2020'
domain: finance
required_split:
- Temporal (NON-IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/imsparsh/lending-club-loan-dataset-2007-2011
- https://www.kaggle.com/datasets/wordsforthewise/lending-club
- https://zenodo.org/records/11295916
- https://www.kaggle.com/datasets/adarshsng/lending-club-loan-data-csv
- https://www.lendingclub.com/
notebook_path: datasets/beyond_iid/temporal/lending_club/lending_club_1m.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/lending_club/dataset.py
source_row: 641
type_adapter_id: curation-record-v1
---

## Comments

Predict whether loan is paid back, needs to be shuffled, TextTabBench drops ['id', 'member_id', 'issue_d', 'url', 'last_pymnt_d', 'last_credit_pull_d'], we will have to make sure that there is no leakage

Text has prefix for date and HTML artifacts
Data might have spatial components

CC (2026-10-01, Lennart): The Zenodo file (Sanz-Guerrero et al.) holds only loans that had finished (fully paid or charged off) by the 2018Q4 snapshot. Against accepted_2007_to_2018Q4.csv.gz, at least 99.8% of the 36-month loans are finished up to 2015Q4, but 57-93% per quarter in 2016 (38% in 2017, 11% in 2018), and only 63-97% of the 60-month loans per quarter from 2014 on. The missing loans are mostly good ones still being repaid, so later or longer loans skew the labels (default rate among finished loans 15-16% in 2013, 24-26% in 2016). The v0.2 definition therefore keeps only the 36-month loans issued up to 2015 (609,544 rows) and tests on the quarters 2015 Q2-Q4; `term` is used only for this selection, not as a feature.

**Assessment (AI, 2026-10-14), joint-applicant fields:** In accepted_2007_to_2018Q4.csv.gz the sec_app_* fields and revol_bal_joint are filled only from 2017Q1 on (1,025 of 4,407 joint applications in 2017Q1, then nearly all of them); joint applications start in 2015Q4 (511 loans) but without these fields. Among the 36-month loans issued up to 2015, all sec_app_* fields and revol_bal_joint are empty, so the sec_app_fico_n the definition built was empty and dropped with them. The definition now leaves these fields out of the merge; the final frame is unchanged (609,544 rows x 82 columns, same values).

CC (2026-10-21, Lennart): record the SPLIT-9 / SPLIT-14 reading and the SPLIT-10 exception (cross-dataset item, ok).

**Exception to SPLIT-10 (2026-10-21, Lennart):** a loan's outcome is known only when it ends, up to 36 months after issue, with no outcome dates: a 36-month gap leaves 5-9% of the rows for training in the three windows, a 12-month gap 33-46%, below the 50% floor. Serves SPLIT-14 (Must) (principles.md, Tensions).

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — Sanz-Guerrero & Arroyo 2025 tune by balanced accuracy for its 'more stable behaviour' and test AUC second with DeLong tests; balanced accuracy fixes no decision threshold or costs for approving a loan (MET-6). Original rejected: balanced accuracy. roc_auc is the binary fallback (the paper's tested metric).

CC (2026-10-21, Lennart): the metric is the roc_auc fallback, not the paper's balanced accuracy.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): 1 ordinal scales typed as ordered categories in the codebook's order (CLEAN-14, amended): `emp_length` (the README lists their levels); their codes that mean unknown (don't know, refused, not asked) are missing in `emp_length` (CLEAN-10).

**Assessment (AI, 2026-11-01):** the benchmark STRABLE (https://arxiv.org/abs/2605.12292) carries this record's data as "Lending Club Loan": Raw file Lending-Club-Loan-Dataset-2007_2011.csv from TextTabBench. Paper says 'interest rate'; config target is loan_status (binary). Tagged STRABLE on 2026-11-01.

CC (2026-11-01, Lennart): the target rule (CLEAN-25) and the cut-end rule (CLEAN-14): counts with a cut end are numbers: emp_length.

CC (2026-11-01, Lennart): counts with a cut end stay ordered categories of the source's levels, the cut end a level of its own (CLEAN-14): the lossless form, chosen from the context rather than by model runs; the same day's numbers with censoring flags are reverted.

**Assessment (AI, 2026-11-10):** priority for the review of the test windows and horizons, which this record never had. Priority 3: gap 0, use case 0, source + (Lending Club's published loan data), shape +, risk 0 (the open issue is the choice of quarters).

CC (2026-11-11, Lennart): REVIEW issue 1 (which quarters), "Reply (b): 2015 Q4, 2015 Q2 and 2014 Q4" to the consistency check: the test windows are October-December 2015, April-June 2015 and October-December 2014, spread over two years now that the amended floor opens 2014. October-December 2014 trains on 45.9% of the loans, the one window under half beside 85.5% and 62.8%, signed off (SPLIT-14 as amended on 2026-11-11). The gap-0 exception to SPLIT-10 of 2026-10-21 stays as recorded.

CC (2026-11-11, Lennart): the declared horizon (3 months, no gap, windows starting 2015-10-01, 2015-04-01 and 2014-10-01) is checked, as the quarter matches the files LendingClub released by calendar quarter and no source names another cadence (the paper shuffles the loans into 5 folds).

**Assessment (AI, 2026-11-11):** applied in dataset.py: `temporal` declares the cutoffs 2015-10-01, 2015-04-01 and 2014-10-01 (3 months, no gap); test 88,667, 64,222 and 49,197 loans, train 520,877, 383,088 and 279,567 (85.5%, 62.8%, 45.9% of 609,544); default rate 14.8%, 15.4% and 14.6% in the windows, 13.8%, 13.3% and 12.8% on the train sides. For these windows a 36-month gap would leave 3.9-8.8% of the rows for training, a 12-month gap 22.5-45.9% and a 6-month gap 62.8%, 45.9% and 33.0%, so the exception's reason holds. `task_summary.split`, `splits_comment` (the windows and why, the shares, the quarterly files as the length's reason, "updated monthly" removed) and the issue-year bullet of `curation_comments` are rewritten; `accepted_check_warnings` accepts `splits_train_under_half` with the sign-off. `dataset check`: 0 errors, 0 warnings (README not regenerated).

CC (2026-11-11, Andrej): Review issues 2 and 3 (numbered 1 and 2 on the review page they were marked on), B and B. Issue 2: `_clean` builds `borrower_key` (the month of the earliest credit line, the 3-digit ZIP code, the state and the lower-cased employer title; not a feature) and a custom `_make_splits` builds the declared windows and then drops from each training side the loans whose key occurs among that window's test loans, as alfa_battle_2_0_task_2 does; `splits_comment` replaces the "no shortcut measured" sentence with the measured numbers, and `splits_rows_unused` is accepted for the loans a match removes from every training side. Issue 3: the 14 fields (`all_util`, `il_util`, `inq_fi`, `inq_last_12m`, `max_bal_bc`, `mths_since_rcnt_il`, `open_acc_6m`, `open_il_12m`, `open_il_24m`, `open_act_il`, `open_rv_12m`, `open_rv_24m`, `total_bal_il`, `total_cu_tl`, named in `FIRST_REPORTED_DEC_2015`) leave the merged list of `_clean` with a curation note: they are empty for every loan issued before December 2015, so no training side holds a value. `dataset check` could not be run: neither warehouse on this machine holds the two raw files, and the figures for the window October-December 2014 are owed with it.

## Review

**Outcome:** added. On 2026-11-11 you chose the test windows 2015 Q4, 2015 Q2 and 2014 Q4 (issue 1, reply (b)),
with 2014 Q4 training on 45.9% of the loans and signed off, and kept the quarterly horizon without a gap (Horizon, A).
On the same day you dropped from each training side the loans of borrowers who take a loan in the test quarter (issue
2, B) and the 14 credit-report fields LendingClub first reported in December 2015 (issue 3, B).

**Main points:** Settled on 2026-11-11: the windows 2015 Q4, 2015 Q2 and 2014 Q4 (issue 1) and the one-quarter horizon
with the gap-0 exception as recorded; the training loans of borrowers who take a loan in the test quarter are dropped
(issue 2) and the 14 credit-report fields first reported in December 2015 leave the merged list (issue 3). Nothing is
left open. Issues 2 and 3 come from the other review of this dataset, where they were numbered 1 and 2; they are
renumbered here so that no number means two things.

**Horizon:**

* **Verdict:** keep the three-month windows (medium confidence): LendingClub released its loan files by calendar
  quarter, the paper we start from uses random folds and states no horizon, and no refit cadence was found.
* **Length:** declared as 3 months, "a model that is refit every quarter" (`splits_comment`). Sanz-Guerrero and Arroyo
  (2025, https://arxiv.org/abs/2401.16458) shuffle the loans and use 5-fold cross-validation ("The dataset is shuffled
  to eliminate biases derived from its original ordering"), so the source gives no horizon. LendingClub's files held
  "complete loan data for all loans issued through the previous completed calendar quarter" (its file description, as
  copied in https://rdrr.io/cran/creditmodel/man/lendingclub.html), while `splits_comment` says the data was updated
  monthly; LendingClub's own refit cadence: none found (the paper, the archived file descriptions, a web search). The
  quarter is a convention that matches the quarterly files, not a stated cadence.
* **Gap:** none, by your recorded exception of 2026-10-21: a loan's outcome comes up to 36 months after issue and the
  data has no outcome dates, and a 12-month gap would leave 33-46% of the rows for training.
* **Time frame:** 36-month loans issued from April 2008 to December 2015 (609,544), the only loans whose outcomes are
  complete in the 2018 Q4 snapshot. 46% of the loans were issued in 2015, so only its four quarters keep half the rows
  for training (2015 Q1: 53.9%). In 2015 Q4, 14 new credit-bureau fields (`all_util`, `inq_fi`, `open_acc_6m`, ...)
  appear, filled on 17% of its loans and missing on every loan of the earlier quarters of 2015.
* **Options:**

  | | Option | What it does | Test windows | Pro | Con |
  |---|---|---|---|---|---|
  | A | Three months (implemented) | quarterly windows, no gap (your exception of 2026-10-21): 4 candidates above the floor, the quarters of 2015 | 3 windows (issue 1's B) of 54,324 to 88,667 loans | matches LendingClub's quarterly loan files | a convention, not a stated cadence |
  | B | One month | 14 candidates, November 2014 to December 2015, 6,051 to 33,186 loans each | 14 candidates of 6,051 to 33,186 loans, November 2014 to December 2015 (2015 alone: 12 of 16,023 to 33,186) | would match the "updated monthly" reading of `splits_comment` | no source either; fewer loans per window |
  | C | Six months | 2 candidates: 2015 H2 (73.4% train share) and H1 (53.9%) | 2 candidates of 118,546 and 162,234 loans | more loans per window | fewer than three windows |
  | D | One year | 2015 alone | 1 candidate of 280,780 loans | all of 2015 in one window | one candidate, fewer than three windows |

* **Recommendation:** A: the quarter matches the files LendingClub released by calendar quarter, and no source names
  another cadence. **Decision:** A, B, C or D?

**Lennart (2026-11-11, ok):** As implemented (A).

**Resolved (2026-11-11, Lennart):** A, three-month windows without a gap, kept: the quarter matches the files
LendingClub released by calendar quarter, and no source names another cadence (the paper shuffles the loans into 5
folds). The gap-0 exception to SPLIT-10 of 2026-10-21 stays as recorded. `splits_comment` gives that reason and no
longer says the data was updated monthly, which the file description contradicts; the windows are issue 1's (b). The
record has the horizon CC line. `dataset check`: 0 errors, 0 warnings (README not regenerated).

**Issues for Lennart:**

1. **Which quarters of 2015 should the test windows be?**

   * **Problem:**
     - The three test windows are 2015 Q2, Q3 and Q4, walking back from the newest, and 2015 Q1 is the only other
       quarter that keeps half the loans for training (53.9%).
     - Since 2026-11-10 the newest window always stays and the others are chosen from the use case and statistics of
       the data, preferring other seasons and months over the windows just before the newest[^lc-split15].
     - Other years are not open, since 46% of the loans were issued in 2015[^lc-split14].
   * **Background:** Each quarter is a season of 2015, so today's windows cover three seasons and B covers three as
     well, with winter in place of summer. The default rate barely moves across the four quarters (14.6% to 15.4%),
     and the train sides sit at 13.2% to 13.8%. The three older quarters show little drift (median PSI 0.02 to
     0.04); the newest is set apart by the 14 bureau fields that start in it (median PSI 0.45). PSI, the population
     stability index, compares a feature's distribution in the window with its train side; above 0.25 is usually read
     as a large shift; a few bureau-history columns (`num_bc_tl` and others) drift by 0.8 to 1.1 in each of the three
     older quarters.
   * **Statistics:** from the candidate table (100,000-row samples of each side for the drift).

     | Window | In | Loans | Default rate, test | Default rate, train side | Train share | Median PSI | Largest PSI |
     |---|---|---|---|---|---|---|---|
     | Oct-Dec 2015 | A, B | 88,667 | 14.8% | 13.8% | 85.5% | 0.445 | 1.28 (`all_util`) |
     | Jul-Sep 2015 | A | 73,567 | 14.6% | 13.5% | 73.4% | 0.023 | 0.78 (`num_bc_tl`) |
     | Apr-Jun 2015 | A, B | 64,222 | 15.4% | 13.3% | 62.8% | 0.027 | 0.92 (`num_bc_tl`) |
     | Jan-Mar 2015 | B | 54,324 | 14.9% | 13.2% | 53.9% | 0.037 | 1.10 (`num_bc_tl`) |

   * **Effect on the task:** A tests the loans of April to December 2015, each with a model refit on everything up to
     the quarter before. B tests October to December, April to June and January to March, so one model is refit on
     2008-2014 alone, before the 2015 volume arrived, and the windows are spread over the whole open year instead of
     its last nine months.
   * **Consistency:** Your CC of 2026-10-01 recorded the windows as "the quarters 2015 Q2-Q4" when the 2016 loans were
     dropped; B departs from that wording, which predates the rewritten rule. The exception for gap 0 holds for both
     options; under B its numbers change (a 12-month gap would leave 28-46% of the rows for training)[^lc-split10].
   * **Sources:** the definition `datasets/_dev/tabarena-v0pt2/lending_club/dataset.py` (`splits_comment`,
     `temporal`); the record `curation/records/lending_club.md` (CC 2026-10-01, the exception of 2026-10-21); the
     candidate table `.venv/bin/python -m data_foundry.curation.cli dataset windows lending_club --root
     datasets/_dev/tabarena-v0pt2` (4 quarters); the bureau fields counted on the definition's frame.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | 2015 Q4, Q3 and Q2 (implemented) | tests Oct-Dec, Jul-Sep and Apr-Jun 2015 | the most training data (oldest 62.8%); the windows of your CC of 2026-10-01 | walks back from the newest; no window in the first months of the year |
     | B | 2015 Q4, Q2 and Q1 | tests Oct-Dec, Apr-Jun and Jan-Mar 2015 | spread over the whole open year; no window right before the newest; adds winter | the oldest trains on 53.9%, with no 2015 loan |

   * **Recommendation:** B, with low stakes: the statistics barely tell the quarters apart, so the choice follows the
     rule's default of spreading the windows over the eligible history rather than taking the quarter just before the
     newest. **Decision:** A or B?

   **Notes for the AI:** on B, `temporal = Temporal(on="issue_d", splits=TemporalSplits(window=3, unit="months",
   cutoffs=("2015-10-01", "2015-04-01", "2015-01-01")))`: test 88,667, 64,222 and 54,324 loans, train 520,877,
   383,088 and 328,764 (85.5%, 62.8%, 53.9%). Then rewrite `task_summary.split` ("Each of the last three quarters of
   2015"), `splits_comment` (the windows, the reasons and the numbers above; the exception's gap figures: a 36-month
   gap and a 12-month gap recomputed for the new windows, 12 months now 28-46%), add a CC line to the record and a
   dated CHANGELOG entry, and run `dataset check` (SPLIT-15). On A, write the reason for walking back into
   `splits_comment` and the record.

   [^lc-split15]: **SPLIT-15** (Must for the newest window, Should for the others; amended 2026-11-10, Lennart and
     Andrej): "The newest window is always a test window ... Prefer windows in other years, then other seasons, then
     other months, weeks or days, over the windows just before the newest. Walking back from the newest is one choice
     among others and needs its reason too, such as a history too short for others, or a use case that only cares
     about the weeks after a refit."
   [^lc-split14]: **SPLIT-14** (Must): at least 3 windows, and no window's train side holds less than 50% of the data.
   [^lc-split10]: **SPLIT-10** (Should): when a label is known only some time after its row, train on the rows whose
     outcome is known by the window's start; the exception of 2026-10-21 (Lennart) sets gap 0 because the label's
     delay would break the 50% floor.

   **Lennart (2026-11-11, change):** Option B: 2015 Q4, Q2 and Q1.

   **Consistency check (AI, 2026-11-11):** Keep all three test windows in 2015, now that the amended floor opens 2014?

   * **Problem:**
     - Option B spreads the windows over 2015 because other years were not open: before today only its four quarters kept
       half the loans for training[^lc1-15].
     - Under today's amended floor 2014 Q4, Q3 and Q2 train on 45.9%, 39.2% and 33.0%, so one of them can be the window
       under half[^lc1-14].
     - Every other mark of this round with another year open took one (mortgage, noaa_storm_events_damage,
       rossmann_store_sales, rain_in_australia, g_research_crypto_forecasting_1m).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | 2015 Q4, Q2 and Q1, as marked | B: 85.5%, 62.8%, 53.9% | every train side keeps half; the default rate barely moves between quarters (14.6% to 15.4%) | one year only, where another is now open |
     | b | 2015 Q4, 2015 Q2 and 2014 Q4 | swaps 2015 Q1 for 2014 Q4 (49,197 loans, 45.9%) | another year at the smallest cost in training data | two fourth quarters, no first quarter |
     | c | 2015 Q4, 2015 Q1 and 2014 Q2 | evenly over the seven open quarters (85.5%, 53.9%, 33.0%) | two years and three seasons | the oldest trains on a third of the loans |

   * **Recommendation:** b, with low stakes: it adds another year at the smallest cost in training data.
     **Decision:** a, b or c?

   [^lc1-15]: **SPLIT-15** (Should for the other windows): "Prefer windows in other years, then other seasons ...".
   [^lc1-14]: **SPLIT-14** (Must; amended 2026-11-11, Lennart). The gap-0 exception to **SPLIT-10** (2026-10-21) still
     holds under any option.

   **Lennart (2026-11-11, change):** Reply (b): 2015 Q4, 2015 Q2 and 2014 Q4

   **Resolved (2026-11-11, Lennart):** b: the test windows are October-December 2015, April-June 2015 and
   October-December 2014, so they spread over two years. `temporal` declares the cutoffs 2015-10-01, 2015-04-01 and
   2014-10-01 (3 months, no gap): test 88,667, 64,222 and 49,197 loans, train 520,877, 383,088 and 279,567 (85.5%,
   62.8%, 45.9%). 2014 Q4 is the one window under half, signed off: `accepted_check_warnings` accepts
   `splits_train_under_half`. The gap-0 exception stays as recorded; for these windows a 36-month gap would leave
   3.9-8.8% for training, a 12-month gap 22.5-45.9%, and `splits_comment` gives these figures. `task_summary.split`,
   `splits_comment` (the windows and why, the counts, the shares) and the issue-year bullet of `curation_comments` are
   rewritten. The record has the decision and the horizon CC lines. `dataset check`: 0 errors, 0 warnings (README not
   regenerated).

2. **Drop the training loans of borrowers who take another loan in the test quarter, as for alfa_battle_2_0_task_2?**

   * **Problem:**
     - A test loan whose borrower had an earlier loan that defaulted defaults at 63% to 74% (2,204 test loans over the three quarters), against 13% when that earlier loan was repaid and 20% for borrowers without one.
     - The earlier default was most likely recorded after the test loan was issued: a lender does not grant a new loan on a charged-off one, and both defaults come together (75% when the earlier loan was issued 6 to 18 months before), so a refit at the quarter's start could not know that label.
     - Drop those borrowers' training loans, as alfa_battle_2_0_task_2 does, or keep them with a note?
   * **Background:**
     - How the data arrives: loans are issued month by month with the application and the credit report of that day; the outcome comes when the loan ends, up to 36 months later, and the release holds only finished loans. The record's collection facts say this (`Samples: Over Time`, `Time: Dated`, `Target: Varying Delay`), and a temporal split carries no time-basis tag[^lc2a].
     - Training on labels that came after the window start is the accepted exception of 2026-10-21 (no gap, since a gap would leave too little training data), and its note says no shortcut of the alfa_battle_2_0_task_2 kind "has been measured here". Such a shortcut, a label of the test row's own borrower set after its prediction point, is removed whatever it costs, unlike recent labels shared through codes such as a branch or a ZIP code[^lc2b].
     - The release has no borrower id, so the borrower is the exact match of four stable fields: the month of the earliest credit line, the 3-digit ZIP code, the state and the employer title. Among rare employer titles with an income within 20%, the pairs agree as one borrower would: 94% default after a defaulted earlier loan, 12% after a repaid one.
   * **Experiments:** shipped container (the 36- and 60-month loans issued up to 2015; the definition keeps the 36-month ones), the three test quarters as now:
     - Test loans with a matched earlier loan: 4,758, 5,494 and 7,775 (5.5% to 6.8%); their training loans are 4,944, 5,810 and 8,282 (about 1% of each training side); test defaults with a defaulted match: 2.3% to 2.5% of all test defaults.
     - LightGBM (400 trees), ROC AUC with the matched training loans against as many training loans dropped at random: 0.6908 against 0.6933 (2015 Q2), 0.7056 against 0.7067 (Q3), 0.7060 against 0.7067 (Q4); on the test loans with a match 0.681 against 0.720, 0.700 against 0.725, 0.703 against 0.722; on the other test loans no change.
   * **Consistency:** alfa_battle_2_0_task_2 drops the training products of clients with a product in the test window (95.1% default after a defaulted earlier product; AUC 0.002 to 0.009 higher without the filter); lt_vehicle_loan_default_prediction keeps its gap 0 because no borrower recurs.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep (implemented) | the note gives the measured link | no change; no constructed key | a training label set after the test loan's issue tells its outcome; 0.001 to 0.003 AUC above the filtered split |
     | B | Drop the matched training loans | per window, training leaves out the loans whose borrower key matches a test-window loan | removes the shortcut, as for alfa_battle_2_0_task_2; costs about 1% of each training side | the key is built from four fields, not an id; a few different borrowers with a common title may match |
     | C | Drop only the matched loans still running | as B, but only the matched loans whose last payment, from LendingClub's file, is after the window start | keeps the matched loans whose outcome was known at the refit | needs `last_pymnt_d` from the raw file as a filter column; a charge-off follows the last payment by months, so the date is approximate |

   * **Recommendation:** B: the link is the borrower's own later-recorded default, the case the rule removes, and the filter costs about 1% of the training rows. **Decision:** A, B or C?

   **Notes for the AI:** on B, in `_clean` build `borrower_key` = `earliest_cr_line` | `zip_code` | `addr_state` | lower-cased, stripped `emp_title` (missing when `emp_title` or `earliest_cr_line` is missing), not a feature; in a custom `_make_splits` (or a training filter if the API has one) drop from each window's training side the loans whose key occurs among the window's test loans; a curation note with the numbers above re-measured on the definition's own rows (36-month loans), and replace the sentence "No shortcut of the kind alfa_battle_2_0_task_2 removes ... has been measured here" in `splits_comment`; `dataset check`, the split probes, rebuild; record `CC` line. The measurement used the shipped container (36- and 60-month loans); repeat it on the definition's frame before applying.

   [^lc2a]: **SPLIT-32** (Should): how the data was collected (the record's facts on samples, time and target) is information for the split; a definition names a use-case prototype only for a split that is not temporal.
   [^lc2b]: **SPLIT-9** (Must): a training row whose label tells a test row's outcome and was not yet known at the prediction point must not be in train, as a label of the test row's own entity set after its prediction point (alfa_battle_2_0_task_2); the shortcut is measured and removed, whatever it costs the training floor; labels shared through codes of many entities fall under SPLIT-10 (lt_vehicle_loan_default_prediction). **SPLIT-10** (Should): the exception of 2026-10-21 for lending_club (no gap; a 36-month gap leaves 5-9% for training). **SPLIT-24** (Must): a key constructed exactly from identical values of the columns that define the entity.

   **Andrej (2026-11-11, change):** Option B: Drop the matched training loans.

   **Resolved (2026-11-11, Andrej):** B: `_clean` builds `borrower_key` (not a feature) and a custom `_make_splits` drops from each window's training side the loans whose key occurs among its test loans; the splits comment's "no shortcut measured" sentence is replaced by the numbers, re-measured on the definition's 36-month loans (LightGBM, 400 trees, Slurm job 1378316):

   | Window | Training loans dropped | Test loans with a match | Default after a defaulted match | ROC AUC, matched dropped | ROC AUC, random drop |
   |---|---|---|---|---|---|
   | 2015 Q2 | 3,216 (0.8%) | 3,122 | 77% (317) | 0.675 | 0.678 |
   | 2015 Q3 | 3,642 (0.8%) | 3,481 | 66% (311) | 0.685 | 0.685 |
   | 2015 Q4 | 5,213 (1.0%) | 4,942 | 59% (391) | 0.686 | 0.688 |

   After a repaid earlier loan 9% default, without a match 15%. `dataset check`: 0 errors; training 379,872 to 515,664 loans (62.3% to 84.6%); 3 loans that match a test loan in all three windows are in no split (accepted warning). Not rebuilt.

   **Answer (AI, 2026-11-11):** carried onto the branch `review-marks-20261111`, which holds the other lineage of this
   review: there the test windows are October-December 2015, April-June 2015 and October-December 2014 (issue 1), not
   the three quarters of 2015 this issue was measured on, and this issue was numbered 1 on the review page. The filter
   itself does not depend on the windows and is applied as decided: `borrower_key` in `_clean` and the custom
   `_make_splits`, which builds `SPLIT_WINDOWS` (the branch's cutoffs) and then drops each window's repeat borrowers
   from its training side. What could not be carried is the measurement: two of the three quarters are the same
   (April-June and October-December 2015) and their figures stand in `splits_comment`; October-December 2014 is not
   measured, because neither this clone's `local-data-warehouse` nor the other checkout's holds the two raw files
   (`LC_loans_granting_model_dataset.csv` and `accepted_2007_to_2018Q4.csv.gz`), so `dataset check` cannot load the
   data here and was not run. The counts of that window, and the check, are owed when the files are back.

3. **Drop the 14 credit-report fields LendingClub began to report in December 2015, empty on every training side?**

   * **Problem:**
     - Fourteen credit-report fields (`all_util`, `il_util`, `inq_fi`, `inq_last_12m`, `max_bal_bc`, `mths_since_rcnt_il`, `open_acc_6m`, `open_il_12m`, `open_il_24m`, `open_act_il`, `open_rv_12m`, `open_rv_24m`, `total_bal_il`, `total_cu_tl`) are empty for every loan issued before December 2015 and filled for 48.6% of December's.
     - So no training side holds a single value of them, and in the test only the December loans of the newest quarter have them, where they mark the month rather than the borrower (default 20.3% filled against 21.4% empty).
     - Drop them, or keep them as the source reports them?
   * **Background:** when each feature comes into existence is part of how the data arrives[^lc3a]; these fields arrive with the last month of the data, after every training cut. The other merged fields that LendingClub added in 2012 are filled on every training side from 2012 on and are not concerned.
   * **Experiments:** missing share by issue month on the shipped container (loans up to 2015).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep (implemented) | the 14 fields stay | the source's report as given | 14 columns empty in every training side; a model can only read them as a marker of December 2015 |
     | B | Drop the 14 fields | removed in `_clean`, with a note | no column a refit could never learn | none found; a later release with loans from 2016 on would use them |

   * **Recommendation:** B: no window can learn from them, and they would only tell some test loans apart by their month. **Decision:** A or B?

   **Notes for the AI:** on B, remove the 14 names from the merged list in `_clean` with a comment ("first reported in December 2015: empty before, 48.6% filled in December 2015"), a curation note, `dataset check`, rebuild; record `CC` line.

   [^lc3a]: **SPLIT-32** (Should): how the data was collected, when each sample, each feature and the target come into existence, is information for the split and for which features are available at the prediction point.

   **Andrej (2026-11-11, change):** Option B: Drop the 14 fields.

   **Resolved (2026-11-11, Andrej):** B: the 14 fields left the merged list in `_clean` (named in `FIRST_REPORTED_DEC_2015`), with a curation note; re-counted on the 36-month loans: none filled before December 2015, 49.2% filled in December, default 15.6% filled and empty alike. `dataset check`: 0 errors; 67 features. Not rebuilt.

   **Answer (AI, 2026-11-11):** applied on the branch `review-marks-20261111` as decided (the 14 names leave the
   merged list of `_clean`, named in `FIRST_REPORTED_DEC_2015`, with the curation note). The argument is unchanged by
   that branch's windows, whose newest is also October-December 2015, so the fields are still empty on every training
   side. `dataset check` could not be run there: the raw files are in no warehouse of this machine.
