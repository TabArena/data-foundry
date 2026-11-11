---
unique_name: homesite_quote_conversion
name: Homesite_Quote_Conversion
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
priority: 3
decision_markers:
- Anonymized
tags:
- Non-IID (Temporal)
collections:
- TabArena Reject
- TabRed
original_source: Kaggle
year: '2015'
domain: insurance
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/competitions/homesite-quote-conversion/data?select=train.csv.zip
notebook_path: datasets/beyond_iid/new_iid/homesite_quote_conversion/homesite_quote_conversion.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/homesite_quote_conversion/dataset.py
source_row: 651
type_adapter_id: curation-record-v1
---

## Comments

CC: "Split seems to be random per QuoteNumber sample; feature engineered geographic information as it seems"

This data was used as non-IID by TabRed! It was non-iid by https://arxiv.org/abs/2407.02112

LP: I vote for IID based on the Kaggle discussions on how to do cross-validation, my understanding of the prediction task, and that the test data contains timestamps from the same period as the train. At the same time, the date seems to be a real-world factor that we could introduce for splits and use in such a way. Likely we want to treat it as non-IID

We keep it as IID but add a warning to its usage.

CC (2026-10-01, Lennart): Leak audit: possible leak, kept for now on purpose; revisit if the fields are ever documented. `PropertyField37` x `PersonalField12` looks like a status code filled after the quote: (Y, 1-4) holds 20,008 quotes, 99.3% converted (40.6% of all conversions); (Y, 5) holds 54,769 quotes, 0.14% converted. Dropping both lowers LightGBM AUC from 0.965 to 0.915. Kept because the fields are anonymised (the meaning cannot be checked), Homesite set the competition up with them (the official test data has the same fields), and removing a possibly valid signal on a guess would change the host's task. The Kaggle discussions (about 80 threads read via the kaggle CLI, incl. the winners' and best-single-model threads) never mention either field; top private scores were AUC 0.969-0.97, so all strong solutions used the signal. Cost to keep in mind: the dataset sits near its ceiling, which compresses differences between strong models.

**Assessment (AI, 2026-10-19):** open since the leak audit of 2026-10-01: two bundle-check warnings have no decision yet (13 columns constant once -1 becomes missing; a `' '` level in `GeographicField63`). To settle in the next pass: drop the constant columns and turn the blank level into missing, or accept each warning with its reason.

CC (2026-10-21, Lennart): ok on the follow-up item: a strong kept leak does not make the fit approximate (USE-8 amended); the kept leak is named in `fit_reason` as kept, not as a gap.

**Assessment (AI, 2026-10-21):** fit set to `direct`; the two status-like fields (ROC AUC 0.965 with, 0.915 without) are named in `fit_reason` as kept and noted.

CC (2026-10-21, Lennart): "yes we should have one clear way to treat 0/1 flags": every 0/1 flag (a feature holding only 0 and 1, plus missing values; booleans too) is categorical (CLEAN-14, amended). Typed categorical here: SalesField3, SalesField9, PersonalField1, PersonalField2, PersonalField6, PropertyField8, PropertyField29.

CC (2026-10-21, Lennart): on which 0/1 columns are flags: "no if we can infer from the semantic context, keep it a number, this is a real-world bias. We want to make things categorical if we know from the context they are indeed such" (CLEAN-14, amended again). Reverted: SalesField3, SalesField9, PersonalField1, PersonalField2, PersonalField6, PropertyField8, PropertyField29 stay numeric (anonymized fields).

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source roc_auc — AUC (area under the ROC curve) (https://www.kaggle.com/competitions/homesite-quote-conversion/overview/evaluation).

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found a related task: `liberty_mutual_property_inspection` (TBD -> Yes, priority 4). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-01, Lennart): the target rule (CLEAN-25) and the cut-end rule (CLEAN-14): the target ships as No/Yes, Yes the event (1 is the event).

**Assessment (AI, 2026-11-04):** reviewed for the BeyondArena v0.2 review page, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the record's Review. Ship after splitting by quote date (the data is dated and the use case scores new quotes) and two small cleanups; the kept status-like field pair (99.3-99.8% vs 0.1% buyers inside one branch) stays under LEAK-38 unless Andrej drops it. Priority 3: gap 1, use case 1, source 0, shape 1, risk -1.

CC (2026-11-11, Andrej): `PropertyField37` and `PersonalField12` dropped (review page issue 1, B): "There is no way that it is possible to predict a task like that with such a precision. We can use common sense on that to justify the decision."
- With `PropertyField37` = Y, codes 1 to 3 of `PersonalField12` converted at 99.3% to 99.8% (19,934 quotes) and code 5 at 0.14% (54,769); no field known when a quote is issued tells a customer's purchase that precisely, so the pair is treated as recorded after the decision (LEAK-10).
- Not kept under LEAK-38: its rule keeps untestable fields, but a near-certain outcome inside a large branch is the test here; the rule's wording is a separate question (the Review).
- Untuned LightGBM, 3 random folds: ROC AUC 0.965 with the pair, 0.952 without (the 0.915 of 2026-10-01 is reached only when `PersonalField9` and `PersonalField10A/B` go too: `PersonalField9` = 3 marks the same 54,785 quotes as code 5; open as Review issue 4).
- `fit_reason` and the curation note rewritten; `dataset check`: 0 errors, the 2 warnings of issue 3. Not built.

CC (2026-11-11, Andrej): review page marks:
- `year` 2015, as the definition has it (field mark): the competition launched in November 2015.
- `PersonalField9`, `PersonalField10A` and `PersonalField10B` dropped with the pair (issue 4, B): `PersonalField9` = 3 marks the same 54,785 non-buyers (0.14%) as code 5, and `PersonalField10A/B` are missing on exactly these rows; ROC AUC 0.916 without the five (untuned LightGBM, 3 random folds).
- `PropertyField6` (0 in every row) dropped, the blank level of `GeographicField63` (2 quotes) set to missing, the twelve 25-or-missing presence flags accepted in `accepted_check_warnings` (issue 3, B); `dataset check`: 0 errors, 0 warnings.
- LEAK-38 amended with a clause (issue 5, A): a field that fixes a person's later decision at near-certainty inside a large group is a measured mechanism, so LEAK-10 applies; homesite moves to its dropped cases, with a LEAK-10 mechanisms row. The rule's other kept fields (african_credit_scoring_challenge, medical_facility_operational_data, tunisian_fraud_detection_challenge, sendy_logistics_challenge) show no such group and stay.

CC (2026-11-11, Andrej): split by quote date, no gap (review page issue 2, b, and the reply on the gap):
- Nine monthly windows back from May 2015, each trained on every earlier quote (smallest training side 184,261 quotes, 70.7%); `required_split` Temporal (NON-IID), tag Non-IID (Temporal) in place of Larger IID Data.
- Why not random, as in the competition: Homesite scores the quotes it issues next and conversion drifts (15.3% to 19.9% a month); the random folds score 0.008 above the windows' mean (untuned LightGBM, before the drops), nearly all of it from the test months themselves.
- No gap: the last weekdays convert as before (18 May 2015: 19.3%) and the source names no horizon; a 7-day gap moves the mean ROC AUC from 0.9043 to 0.9040, 30 days to 0.9025.

CC (2026-11-11, Andrej): field set decided afresh (review page issue 6, D) and `SalesField5` kept (issue 7, A):
- `PersonalField2` and `PersonalField13` dropped: after the five fields above, `PersonalField1` = 1 with `PersonalField2` = 0 still marked 7,266 quotes at 98.0% bought, and `PersonalField13` = 1 marked 2,092 at 97.8%; the fewest fields that leave no group of 300 quotes at 95% or more (a depth-6 tree) go, and `PersonalField1`, graded on its own (21.0% against 12.9%), stays. Mean ROC AUC over the nine windows 0.904 to 0.898 (untuned LightGBM).
- Why not more: the near-zero side (66,506 quotes, 12 buyers) stays, as a quote that cannot be bought is known when it is issued; on the 130,844 quotes no near-certain marker settles the model scores 0.859, within what an insurer could plausibly reach with data known at the quote.
- `SalesField5` kept with a `Potential leak, kept on purpose:` note: the strongest field (level 5 6.7% against 30.5% to 32.5% on those quotes, stable 2013 to 2015), which may be the sales channel or a sales stage; graded, so the untestable-field rule keeps it (0.879 without it).
- LEAK-38's near-certainty clause now states the stopping point (no large group near-certain, the fewest fields, a field graded alone stays) and that rows the decision cannot reach stay; homesite's case and the LEAK-10 mechanisms row extended.

## Review

**Outcome:** added. Homesite's Kaggle competition (launched November 2015): 260,753 home-insurance quotes from
1 January 2013 to 18 May 2015 with about 295 anonymised fields on the coverage, the sale, the customer, the property
and its area; the target is whether the customer bought the quoted policy (18.75%), scored by ROC AUC, the
competition's metric, on random quotes. The AI recommends shipping it after two changes: split by quote date (issue 2)
and drop one constant column and one blank level (issue 3); the kept status-like fields stay as Lennart decided, with
a sharper note (issue 1). Reviewed without a review panel, from the gathered evidence: the record and its leak audit of
2026-10-01, the BeyondArena results on the shipped data and checks on the shipped data; there is no model run for
it. Validity: the definition keeps the competition's task and metric; two anonymised fields almost give the label
away inside one branch (issue 1); the quotes are dated but split at random, against the use case of scoring new quotes
(issue 2). Value: on the one BeyondArena fold the methods spread from ROC AUC 0.944 (linear model) to 0.968 (tuned
CatBoost), close to the ceiling the kept fields set; the best single raw column reaches 0.750. Quality: one constant
column and a blank level left from the leak audit (issue 3). Weighed: the insurer's own quotes, dates and metric +, a
probable post-quote status kept and a random split of dated data -.

**Main points:** all issues settled on 2026-11-11: the status pair and the three fields marking its non-buyer code
dropped (issues 1 and 4), then `PersonalField2` and `PersonalField13`, the fewest fields that leave no group of 300
quotes at 95% bought (issue 6, D); `SalesField5` kept with a note (issue 7); nine monthly windows with no gap (issue
2); the constant column and the blank level cleaned (issue 3); the near-certainty clause in the keep rule, now with its
stopping point (issues 5 and 6). Mean ROC AUC over the windows 0.898 (untuned LightGBM). The definition is not
rebuilt.

**Record judgment:** valid. The use case is the host's: estimate
which quotes turn into purchases, to judge price changes and keep the customer mix it wants. The metric review page
proposes log loss for this dataset; that question stays there.

**Issues for Andrej:**

1. **Keep `PropertyField37` and `PersonalField12`, which look like a status written after the quote, or drop both?**

   * **Problem:**
     - When `PropertyField37` is `Y`, the code of `PersonalField12` nearly is the label: codes 1 to 3 converted at
       99.3% to 99.8% (19,934 quotes) and code 5 at 0.1% (54,769 quotes).
     - Lennart kept both on 2026-10-01 because the fields are anonymised and Homesite released them in its own
       competition, and the rule for such fields lists this dataset as its kept case.
     - Keep them with a sharper note, or drop both?
   * **Background:** checked on the shipped data. Code 5 occurs only with `Y` (54,769 of 54,770 quotes). With `N`
     the same codes 1 to 3 convert at 13.6% to 15.5%, below the base rate of 18.75%, so the code carries little in
     one branch and almost the whole outcome in the other: the shape of a status recorded after the customer decided.
     The pattern is the same in every quarter from 2013 to 2015 (`Y` with codes 1 to 4: 99.1% to 99.5% converted;
     code 5 on 16.5% to 24.1% of a quarter's quotes), so it is no change of recording over time. Kaggle's test file
     carries both fields, and the forum threads never discuss them (record, CC 2026-10-01). A field is dropped when a
     test shows its fill or missingness depends on the outcome; these fields have no fill or missing value to test, so
     their timing cannot be tested and the keep rule applies[^1a][^1b].
   * **Effect on the task:** if the pair is a status, a model reads off the outcome of 28.7% of the quotes (74,777)
     instead of predicting it, which a model scoring new quotes before the customer decides could not do. Dropping
     both lowers untuned LightGBM from ROC AUC 0.965 to 0.915 (leak audit of 2026-10-01).
   * **Consistency:** kick's `WheelType` and expresso_churn_prediction's `REGION` were dropped on 2026-10-22, each
     after a test showed the field's missingness depends on the outcome; this pair offers no such test, which is the
     fact that sets it apart.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep with a sharper note (implemented, note to extend) | both fields stay; the `Potential leak` note gets the branch table and the quarters | follows the rule and Lennart's call; the host's own task; nothing removed on a guess | if a status, 28.7% of the outcomes are read off; scores sit near the ceiling |
     | B | Drop both | the two fields leave; `fit_reason` and the note say why | no possible post-quote status | removes an untested, possibly valid signal from host-designed data; departs from the rule's listed case |

   * **Recommendation:** A, since the timing cannot be tested and the house rule keeps what cannot be tested, with the
     branch table in the note. **Decision:** keep with the sharper note (A), or drop both (B)?

   **Notes for the AI:** on A, add to the `Potential leak, kept on purpose:` bullet: "code 5 of `PersonalField12`
   occurs only with `PropertyField37` = Y; with N, codes 1 to 3 convert at 13.6% to 15.5%; the pattern holds in every
   quarter 2013 to 2015". On B, drop both in `_clean`, rewrite the `fit_reason` sentence and the note, add a CC line
   and rerun `dataset check`.

   **Resolved (2026-11-11, Andrej):** B: "There is no way that it is possible to predict a task like that with such a
   precision. We can use common sense on that to justify the decision." `_clean` drops both fields; the curation note
   and `fit_reason` say why (LEAK-10), the record has a CC line. Measured again (untuned LightGBM, 3 random folds):

   | Columns | ROC AUC |
   |---|---|
   | all (implemented before) | 0.965 |
   | without the pair (now) | 0.952 |
   | also without `PersonalField9`, `PersonalField10A/B` (issue 4) | 0.916 |
   | also without the other near-zero levels (`Field7`, `PropertyField29`, `PersonalField4A/B`, `PropertyField18`) | 0.906 |

   The leak audit's 0.915 "without both" was in fact the third row: the non-buyer half of the status lives on in
   `PersonalField9` (issue 4). LEAK-38 still lists homesite as its kept case: issue 5.

   [^1a]: **LEAK-38** (Should; scope amended 2026-10-22, Lennart): anonymised fields that may be post-outcome, in data
     a company released for its own competition, stay with a `Potential leak, kept on purpose:` note; the rule covers
     only fields whose timing cannot be tested. Cases: homesite (kept); kick and expresso dropped under LEAK-10.
   [^1b]: **LEAK-10** (Must): a feature holds only what existed at the prediction point and never gives the target
     away; out are a column recorded after the outcome and missingness that encodes the outcome.

2. **Split the quotes by date instead of at random?**

   * **Problem:**
     - The quotes are dated from January 2013 to May 2015, but the split draws quotes at random, so every test quote
       has training quotes from the same and later weeks.
     - Lennart kept the random split because Kaggle's test quotes cover the same dates and the forum cross-validated at
       random (record, undated), while TabReD, the collection this record cites, splits this data by date.
     - Split by date, or keep the random split?
   * **Background:** the use case is a model that scores the quotes Homesite issues next, to judge a price change, so
     it is trained on past quotes. Conversion drifts: 20% to 21% in 2013, 16% to 19% in 2014 and 2015 (quarters of the
     shipped data), and outside the fields of issue 1 from 12% to 14% in 2013 to 10.6% to 11.9% since.
     A prescribed split is a claim to check against the
     task, and a dated task that only needs a time split gets one[^2a][^2b].
   * **Effect on the task:** the random split asks for interpolation inside weeks the model has seen; a date split
     asks for the next weeks, after the drift, as a model refit each month would meet them.
   * **Consistency:** follows kick and the other dated tables of the working copy, which are split by time; TabReD
     (Rubachev, Kartashev, Gorishniy and Babenko, "TabReD: Analyzing Pitfalls and Filling the Gaps in Tabular Deep
     Learning Benchmarks", ICLR 2025, https://arxiv.org/abs/2406.19380) uses this dataset with a time split. Departs
     from the competition's own random test set, which the rule on source splits asks to follow unless the task says
     otherwise[^2c].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random quotes (implemented) | 3 x 3 random folds, as now | matches Kaggle's test set and the forum's practice | tests interpolation inside known weeks; ignores the drift the use case meets |
     | B | Monthly windows by quote date | test windows of one month back from May 2015, train on every earlier quote, at least half of the quotes in each train side | mirrors scoring the next quotes; follows the dated tables and TabReD | departs from the competition's split; the date then extrapolates as a feature |

   * **Recommendation:** B, the use case scores future quotes and the data has the dates. **Decision:** keep the
     random split (A), or split by quote date (B)?

   **Notes for the AI:** on B, `temporal = Temporal(on="Original_Quote_Date", splits=TemporalSplits(window=1,
   unit="months", n_windows=9))` or fewer windows if a train side falls below half the rows (SPLIT-14; quotes before
   September 2014 are about 70%); May 2015 is a partial month (to the 18th). Rewrite `task_summary.split`, the
   IID bullet of `curation_comments` and `fit_reason`; record `required_split` to `Temporal (NON-IID)`, the tag
   `Larger IID Data` to the temporal tag, a CC line; CHANGELOG entry; rebuild on Andrej's ask.

   [^2a]: **SPLIT-5** (Must): the split a paper or a dataset page prescribes is a claim to check against the task
     design, not a fact.
   [^2b]: **SPLIT-6** (Must): a fixed predictive task that only needs a temporal split gets a temporal split.
   [^2c]: **SPLIT-19** (Should): when the source defines the split, follow it; a prescribed split is still a claim to
     check.

   **Answer (AI, 2026-11-06):** The quotes are dated, and the small measured cost supports keeping the random split as a stationary relation: monthly windows (b), or random quotes as a stationary relation (a)?

   * **Problem:**
     - Every quote carries `Original_Quote_Date` (1 January 2013 to 18 May 2015, kept as a feature) and Homesite scores the quotes it issues next, so the date is information for the split; the competition's random split can name a stationary relation, with the measured check in its `Time basis:` line[^2d].
     - The measured cost is small: the newest month scores ROC AUC 0.959 against 0.964 on the random folds (untuned LightGBM; logistic regression 0.952 against 0.955).
     - Monthly windows, or random quotes as a stationary relation?
   * **Experiments:** the definition's rows and features, untuned LightGBM and logistic regression (LR), ROC AUC; nine monthly windows back from May 2015 (September 2014 to May 2015, the last to the 18th), each trained on every earlier quote (71% to 98% of the rows):

     | Split | LightGBM | LR | Converted in test |
     |---|---|---|---|
     | a, random 3 x 3 folds (implemented) | 0.964 (fold SD 0.001) | 0.955 (0.001) | 18.8% |
     | b, newest window (May 2015) | 0.959 | 0.952 | 18.3% |
     | b, nine windows, mean | 0.956 (0.943 to 0.963) | 0.941 (0.926 to 0.952) | 15.3% to 19.9% (training 18.7% to 19.3%) |

     - Nearly all of the gap is the test months themselves, not training on later quotes: on the same test rows of the eight older windows, training on as many quotes drawn at random from the whole file scores 0.0017 more (LR 0.0043). January 2015, the month with the fewest conversions (15.3%), is the hardest (0.943).
     - Without the quote date as a feature the windows score the same (0.955 on average): the date that extrapolates in a window costs nothing measurable.
     - No gap is needed: conversion in the newest weeks (18.1% to 19.3% in May 2015) is as high as in the months before, so no purchase is missing at the end of the release, though the delay from quote to purchase is not stated[^2e].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Random quotes (implemented), as a stationary relation | 3 x 3 random folds; definition tag `StationaryRelation`, a `Time basis:` line with the date and the measured check (conversion 15% to 20% a month, later quotes add 0.0017); the date-column warning accepted with the same reason | matches Kaggle's test set and the forum's practice; the most stable score | interpolates inside known weeks; 0.005 above the newest month; a purchase after a quote is a later outcome, not a present state, so the prototype rests on the measurement alone |
     | b | Monthly windows | `Temporal(on="Original_Quote_Date")`, 9 windows of one month back from May 2015 | mirrors scoring the next quotes; follows the dated tables and TabReD; costs little | departs from the competition's split; May 2015 is a partial month |

   * **Recommendation:** b, as before: the data has the dates and the use case scores future quotes, and the small measured cost leaves no reason to keep the random split. **Decision:** a or b?

   **Notes for the AI:** on b, as in the notes above (`TemporalSplits(window=1, unit="months", n_windows=9)`; the smallest training side is 70.7%, so all nine windows hold), no gap, record `required_split` `Temporal (NON-IID)`, tag `Non-IID (Temporal)` in place of `Larger IID Data`. On a, once PR #50 is in: `data_tags = ("Anonymized", "StationaryRelation")`; `accepted_check_warnings["meta_time_present_unused"]` with the reason "`Original_Quote_Date` dates every quote (January 2013 to May 2015); the split stays random as a stationary relation, as the competition's test quotes cover the same dates and conversion holds across the months"; the curation note "- Time basis: StationaryRelation: `Original_Quote_Date` dates every quote from January 2013 to May 2015; the split stays random as in the competition, whose test quotes cover the same dates: conversion holds at 15.3% to 19.9% a month, on the older windows' test rows later quotes add 0.0017 ROC AUC (logistic regression 0.0043), and the newest of nine monthly windows scores 0.959 against 0.964 on random folds (untuned LightGBM; logistic regression 0.952 against 0.955)", replacing the IID bullet; `dataset check`. Under either option the record gets the tags `Samples: Over Time` and `Time: Dated`.

   [^2d]: **SPLIT-32** (Should): how the data was collected is information for the split; the record's collection facts and, where one fits, the definition's use-case prototype with its `Time basis:` line.
   [^2e]: **SPLIT-10** (Should; amended 2026-11-05): no gap where the newest period is as complete as a later read of it would be, or where the time column's step is longer than the label's delay.


   **Andrej (2026-11-11, discuss):** Do we need a planning gap or not?

   **Answer (AI, 2026-11-11):** No gap, neither for the label's delay nor for planning: with monthly windows, train up to the window's start (a), or leave a month between train and test (b)?

   * **Problem:**
     - A gap is set where labels arrive late or where the use case predicts ahead of its data[^2f]. Neither shows
       here: the newest days convert as before, and a gap of a week or a month only lowers the score.
     - Homesite scores each quote as it is issued, with a model refit on the quotes so far; the source names no
       horizon (such as a price filed months ahead), so the use case has no planning gap of its own.
     - No gap, or a one-month planning gap?
   * **Experiments:** after the drops of issues 1, 3 and 4. Conversion on the last weekdays of the release (weekends
     run lower throughout):

     | Days | Conversion |
     |---|---|
     | 28 April to 8 May 2015, weekdays | 16.7% to 23.6% |
     | 11 to 15 May 2015 | 17.4% to 20.8% |
     | 18 May 2015 (the last day) | 19.3% (419 quotes) |

     The newest quotes are as complete as the older ones, so a purchase is recorded within days of its quote.
     Untuned LightGBM on the nine monthly windows (September 2014 to May 2015), trained on every quote before the
     window's start minus the gap:

     | Gap | Mean ROC AUC | Range over the windows | Training rows |
     |---|---|---|---|
     | none | 0.9043 | 0.8980 to 0.9195 | 184,261 to 254,663 |
     | 7 days | 0.9040 | 0.8974 to 0.9197 | 182,437 to 252,243 |
     | 30 days | 0.9025 | 0.8960 to 0.9169 | 176,306 to 244,458 |

     - A week's gap costs 0.0003: the newest labels add no shortcut through recent quotes[^2g].
     - A month's gap costs 0.0018, mostly a month less of training data.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | No gap | each window trains on every quote before its start | the label arrives within days; matches a monthly refit; no measured shortcut | none found |
     | b | One-month planning gap | trains on the quotes up to a month before the window | guards against a deployment lag the source does not state | removes a month of data for no measured reason; 0.0018 lower |

   * **Recommendation:** a. **Decision:** a or b? The split itself (random quotes or monthly windows, the answer
     above) stays open; with random quotes no gap arises.

   **Notes for the AI:** on a, the split comment states "no gap: the last weekdays convert at 17% to 21%, as before;
   a week's gap changes ROC AUC by 0.0003" (only if monthly windows are chosen). On b, `TemporalSplits(...,
   gap=1)` in months and the same sentence with the measured cost.

   [^2f]: **SPLIT-10** (Should): a gap of about the label's delay where labels arrive late, and a planning gap where
     the use case predicts ahead; the measurements decide, and no gap is needed where the newest period is as
     complete as a later read of it.
   [^2g]: **SPLIT-9** (Must): no shortcut through training rows whose labels were not yet known at the prediction
     point.

   **Resolved (2026-11-11, Andrej):** monthly windows by quote date (b of the first answer), with no gap (a of the
   second). `dataset.py` sets `Temporal(on="Original_Quote_Date")` with nine windows of one month back from May 2015,
   each trained on every earlier quote; `task_summary.split`, `changes` and `fit_reason` and the curation note (in
   place of the IID note) say why. The record has `required_split` Temporal (NON-IID), the tag Non-IID (Temporal) in
   place of Larger IID Data and a CC line. `dataset check`: 0 errors, 0 warnings.

   | Nine windows | Fewest | Most |
   |---|---|---|
   | Training quotes | 184,261 (70.7%, September 2014) | 254,663 (May 2015) |
   | Test quotes | 6,090 (May 2015, to the 18th) | 12,241 |

3. **Drop the constant column and set the blank level to missing, and accept the other twelve warnings?**

   * **Problem:**
     - Two bundle-check warnings have no decision since the leak audit (record, 2026-10-19): 13 columns with one
       value, and a blank level in `GeographicField63`.
     - Twelve of the 13 are flags: they hold 25 for about 2.5% of the quotes and are missing elsewhere (the source's
       -1, set to missing), and their buyers' share differs (`GeographicField14A` 4.4% filled, 19.1% missing).
     - Only `PropertyField6` is constant (0 in every row), and the blank level holds 2 quotes.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Leave as is (implemented) | the warnings stay open | none found | a constant column ships; a blank code stands as a category |
     | B | Drop `PropertyField6`, blank to missing, accept the rest | one column fewer; 2 cells missing; the twelve flags accepted with their reason | constant columns go and proxy missing codes become missing, as the cleaning rules ask[^3a] | none found |

   * **Recommendation:** B, the cleaning rules' default, and the twelve flags carry signal. **Decision:** leave (A), or
     clean (B)?

   **Notes for the AI:** on B, add `"PropertyField6"` to the drop list, `df["GeographicField63"] =
   df["GeographicField63"].replace(" ", np.nan)`, accept `dataset_constant_column` in `accepted_check_warnings` with
   "twelve presence flags: 25 or missing (the source's -1), filled in about 2.5% of quotes, buyers' share differs";
   rerun `dataset check`.

   [^3a]: **CLEAN-5** (Should): drop constant columns, all-missing columns and exact copies of another column.
     **CLEAN-10** (Should): convert proxy missing values to real missing values when the encoding can be inferred.

   **Resolved (2026-11-11, Andrej):** B: `PropertyField6` is dropped, the blank level of `GeographicField63` is set to
   missing, and the twelve presence flags are accepted in `accepted_check_warnings` with their reason. `dataset check`:
   0 errors, 0 warnings.

4. **Drop `PersonalField9` and `PersonalField10A/B` with the pair, as they mark the same code-5 quotes?**

   * **Problem:**
     - `PersonalField9` = 3 holds 54,785 quotes, 0.14% converted; 54,769 of them are the pair's (Y, 5) quotes, and
       `PersonalField10A/B` are missing on exactly these rows.
     - So the non-buyer half of the status dropped in issue 1 is still in the data: without the pair ROC AUC is 0.952,
       without these three as well 0.916 (table in issue 1).
     - Drop them as well, or keep them?
   * **Background:** checked on the shipped frame (2026-11-11). Other levels with near-zero conversion exist
     (`Field7` = 23: 66,474 quotes, 0.01%; `PropertyField29` = 0: 60,056, 0%; `PersonalField4A` missing: 24,526,
     0.01%), but none marks the code-5 quotes as a whole (overlap 9,365 to 16,770) and none has a near-certain buyer
     side; quotes that can never be bought (an ineligible risk, a quote only for information) are known when the quote
     is issued. Removing them as well costs a further 0.009.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep (implemented) | the three stay | nothing removed beyond the decided pair | the code-5 status stays readable: 21% of the quotes at 0.14% |
     | B | Drop the three | `PersonalField9`, `PersonalField10A`, `PersonalField10B` leave with the pair | finishes issue 1: neither half of the status is left; ROC AUC 0.916, the leak audit's figure | three more anonymised fields removed |
     | C | B, and drop the other near-zero levels' fields | B plus `Field7`, `PropertyField29`, `PersonalField4A/B`, `PropertyField18` | no near-certain group left | removes fields with a plausible pre-quote reading on no test; 0.906 |

   * **Recommendation:** B, the same status as the decided pair, on the same quotes. **Decision:** A, B or C?

   **Notes for the AI:** on B, add the three to the drop list next to the pair, extend the curation bullet and
   `fit_reason` (0.916), a CC line, `dataset check`.

   **Resolved (2026-11-11, Andrej):** B: the three fields leave with the pair; the curation bullet and `fit_reason`
   say why, the record has a CC line. ROC AUC 0.916 without the five fields (table in issue 1).

5. **Amend the rule that keeps untestable anonymised fields, which lists homesite as its kept case?**

   * **Problem:**
     - The rule keeps anonymised fields in host-released data when their timing cannot be tested[^5a]; issue 1
       dropped such a pair on the size of the effect alone, so the rule's text and its listed case now disagree.
     - Amend that rule with a clause, or write a new rule?
   * **Background:** the rule on what a feature may hold already says a feature never gives the target away[^5b], and
     the exception for text written with the label drops text that alone explains most of the score when the actor
     cannot have it[^5c]. What is new is the test: an outcome that is a person's later choice, fixed at near-certainty
     inside a large group, counts as evidence of a post-outcome field.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Amend the keep rule (a clause) | "The rule does not cover a field that fixes an outcome no one could know at the prediction point (a later human decision) at near-certainty in a large group: that is a measured mechanism, and the field is dropped." Cases: homesite moves to dropped | one rule decides each field; the exception sits where the keep is; small text change | the threshold ("near-certainty", "large group") is a judgment |
     | B | New rule | a separate rule on implausibly precise fields | visible on its own | overlaps the two rules above; a reader must reconcile three rules |
     | C | Case only | change the Cases entry to "dropped (2026-11-11), on the size of the effect" | least text | the rule's text still says such fields stay |

   * **Recommendation:** A. **Decision:** A, B or C?

   **Notes for the AI:** on A, edit LEAK-38 in `leak_checks.md` and add a LEAK-10 mechanisms row (homesite, 99.3% to
   99.8% against 0.14% in one branch); check the kept named fields (african_credit `Amount_Funded_By_Lender`,
   medical_facility's expected-delay table, tunisian refund fields, sendy `Distance (KM)`) against the clause first.

   [^5a]: **LEAK-38** (Should): anonymised or named fields that may be post-outcome, whose timing no test can
     establish, in data the owner released for its own challenge, stay with a `Potential leak, kept on purpose:` note.
   [^5b]: **LEAK-10** (Must): a feature holds only what existed at the prediction point and never gives the target
     away.
   [^5c]: **LEAK-35** (exception): text written together with the label that alone explains most of the score, while
     the use case's actor does not have it at the prediction point, is dropped.

   **Resolved (2026-11-11, Andrej):** A: LEAK-38 now says a field that fixes a person's later decision at
   near-certainty inside a large group is a measured mechanism, so LEAK-10 applies, with the fields that mark the same
   rows; a graded difference in rates is no such test. Homesite moves to the rule's dropped cases, and a LEAK-10
   mechanisms row gives its numbers. The rule's other kept fields show no such group and stay: medical_facility's
   delay table (0.005 MAE), sendy's distance, the tunisian refund fields, african_credit's funded amount.

6. **Which anonymised fields to drop, decided afresh: none, the status pair, or every field behind a near-certain
   group?**

   * **Problem:**
     - After the five dropped fields, `PersonalField1` = 1 with `PersonalField2` = 0 still marks 7,266 quotes at 98.0%
       bought (4,987 outside the dropped buyer codes at 97.1%, every quarter 97% to 100%), and `PersonalField13` = 1
       marks 2,092 at 97.8%.
     - Each field alone is graded (`PersonalField1` 12.9% against 21.0%, `PersonalField2` 20.7% against 17.9%), so
       only the combination is near-certain, the shape of the dropped pair.
     - Issues 1 and 4 stopped at the first status found: which field set, and which general rule decides it?
   * **Background:** a leak sweep on the definition after issues 1, 3 and 4 (2026-11-11), on the shipped frame:
     - On the non-buyer side, `PropertyField29` filled, `Field7` = 23, `PersonalField4A/B` missing, `PropertyField18`
       = 0 and `PropertyField38` missing together cover 66,506 quotes (25.5%) with 12 buyers, 49,728 of them outside
       the dropped code 5; issue 4 kept these fields (option C rejected) because a quote that cannot be bought is known
       when it is issued.
     - Not found: repeated customers (no two quotes share every field; grouping folds by customer leaves ROC AUC at
       0.9154), fields that follow the day's conversion (|r| ≤ 0.015), signal in the 124 geographic fields beyond
       0.0004.
     - Masking only the near-certain cell (blanking `PersonalField1` and `PersonalField2` where they are 1 and 0)
       does not work: the blank becomes the same marker, so the choice is per field.
     - On the three newest windows the model's gain sits in `SalesField5` (35%), `PropertyField29` (15%),
       `PersonalField1` (8%) and `PersonalField2` (7%).
     - How precise the use case can be: at the quote an insurer knows its own price and the change against the
       previous premium, the risk, whether it will underwrite, the channel and the session; it does not know the
       competitors' quotes, which decide most comparison shoppers, nor whether the customer only compares. No public
       benchmark of quote-to-purchase ROC AUC was found; a vendor demo on synthetic cross-sell data reports 0.73[^6b].
       The AI's estimate, not a source: an honest model reaches about 0.70 to 0.85, the upper end with channel or
       session signals.
     - Half the quotes (130,844, 50.2%, 18.0% bought) carry no near-certain marker, buyer or non-buyer (the dropped
       codes included); the other half is settled before any modelling, and those quotes do not respond to price,
       which the use case is about.
   * **Experiments:** untuned LightGBM on the nine monthly windows of issue 2 (300 trees), mean ROC AUC; a depth-6 tree
     on all quotes counts the groups of at least 300 quotes converting at 95% or more, or 0.5% or less:

     | Option | Fields dropped | ROC AUC, mean (range) | Quotes in ≥95% groups | Quotes in ≤0.5% groups |
     |---|---|---|---|---|
     | A | 0 | 0.9563 (0.944 to 0.964) | 23,449 | 93,489 |
     | B | 2 | 0.9437 (0.933 to 0.952) | 6,837 | 92,968 |
     | C (implemented) | 5 | 0.9043 (0.898 to 0.920) | 6,761 | 63,442 |
     | D | 7 | 0.8978 (0.890 to 0.912) | 0 | 63,462 |
     | E | 8 | 0.8935 (0.885 to 0.905) | 0 | 59,621 |
     | F | 14 | 0.8808 (0.866 to 0.893) | 0 | 35,638 |

     - Dropping only `PersonalField2` (C plus one field) leaves 1,472 quotes in ≥95% groups through `PersonalField13`;
       D adds `PersonalField13` and none is left, with `PersonalField1` kept as a graded field.
     - F's one remaining ≤0.5% group (35,638 quotes at 0.38%) takes six graded conditions (`SalesField5` = 5, a high
       `SalesField1B`, `PersonalField15`, `PropertyField8`, `PersonalField26`, `CoverageField6B`): a low-propensity
       segment, not a single field's code.

     Option D scored on the quotes no marker settles (same model and windows):

     | What is scored | ROC AUC, mean (range) |
     |---|---|
     | D, all test quotes | 0.8978 (0.890 to 0.912) |
     | D, test quotes no marker settles | 0.8587 (0.844 to 0.878) |
     | D, trained and tested on those quotes only (option H) | 0.8619 (0.850 to 0.879) |
     | `SalesField5` alone (level means), on those quotes | 0.7647 (0.740 to 0.793) |

     - The settled half adds 0.04 to the score on all quotes; on the open quotes D still sits at the top of the
       estimate above, and most of it is `SalesField5` (issue 7).
   * **Options:**

     | | Option | What it does | General rule it follows | Pro | Con |
     |---|---|---|---|---|---|
     | A | Keep all | restore the pair and the three fields of issue 4 | anonymised fields of a host's own release stay when their timing cannot be tested, however precise[^6a] | the host's data as released; the rule as it stood before today | 9% of the quotes are near-certain buyers; scores near the ceiling; undoes issues 1, 4 and 5 |
     | B | Status pair only | `PropertyField37`, `PersonalField12` | drop only the fields that show the near-certainty themselves, not other fields on the same rows | the smallest drop of issue 1 | the code-5 status stays on `PersonalField9`; contradicts the clause's "fields that mark the same rows go with it" |
     | C | Pair and same-row fields (implemented) | B plus `PersonalField9`, `PersonalField10A/B` | the clause applied to the first status found | issues 1 and 4 as decided | 6,761 quotes in near-certain buyer groups remain; under the clause a stopping point without a rule |
     | D | C plus the fewest fields that leave no near-certain buyer group | C plus `PersonalField2`, `PersonalField13` | a person's later decision fixed at near-certainty in a large group is dropped, the fewest fields that remove every such group, measured by a tree; a graded field stays | no near-certain buyer group left; `PersonalField1` stays where it is graded; the test is repeatable on other datasets | which field of a pair goes is a choice of the search; the threshold (95%, 300 quotes) is set by us |
     | E | C plus every field of a near-certain buyer cell | C plus `PersonalField1`, `PersonalField2`, `PersonalField13` | as D, but every field of a near-certain cell goes, as both fields of the pair did in issue 1 | the same treatment as issue 1's pair; no field choice left to the search | drops `PersonalField1` although it is graded alone; 0.004 below D |
     | F | E plus the near-zero fields | E plus `PropertyField29`, `Field7`, `PersonalField4A/B`, `PropertyField18`, `PropertyField38` | near-certainty in either direction is dropped, whether or not a pre-quote reading (a quote that cannot be bought) exists | no single field or code fixes the outcome either way | reverses issue 4's rejected C; drops fields with a plausible pre-quote reading on no test; 0.013 below E |
     | H | D plus only the open quotes | D's fields, and keep only the 130,844 quotes no marker settles (rows filtered on the markers before the split) | the task covers the rows where the outcome is the actor's open choice, as credit data with outcomes only for granted loans is a valid task | scores what the use case asks, how undecided customers respond; no near-certain group either way; 0.86, within what an insurer could plausibly reach | the filter rests on anonymised markers we read as status; halves the data; the population is our construction, not Homesite's |
     | G | Retire | `No (Retired)`, a CC line, the folder removed | a release whose untestable fields keep showing post-outcome status on both sides cannot be bounded, so its remaining fields are not trusted | no line drawn on a guess | after F the task is real (0.88, graded segments, methods spread); loses TabReD's dataset |

   * **Recommendation:** D: the near-certainty test of today's clause run to the end, with the fewest fields removed
     and a stopping point a tree can check; the non-buyer side stays as issue 4 decided, since an insurer can know at
     the quote that a policy cannot be sold, while no one can know that a customer will buy at 98%. E if every field
     of a cell should go, as in issue 1; H if the task should be the customers who could still decide, at the cost of
     a population defined by our reading of anonymised fields. **Decision:** A, B, C, D, E, F, G or H?

   **Notes for the AI:** on D or E, add the fields to the drop list after the twin with a comment, extend the
   curation bullet and `fit_reason`, rewrite the LEAK-38 clause's stopping point ("until no group of at least 300
   quotes converts at 95% or more", with D's "fewest fields" or E's "every field of the cell") and its homesite case,
   a CC line, `dataset check`. On A or B, the clause of issue 5 is reworded or withdrawn. On F, LEAK-38 drops the
   "person's later decision" qualifier. On G, the retirement steps. On H, D's drops plus a row filter in `load` (the
   non-buyer and buyer conditions of `core.py`, applied before the dropped fields go), the filter stated in `changes`
   and a curation bullet, the record's row count, `dataset check`. Evidence: `~/claude_jobs/homesite_drop/`
   (`sweep.py`, `followup.py`, `round2.py`, `round3.py`, `core.py` and their `.out` files).

   [^6a]: **LEAK-38** (Should; amended 2026-11-11): anonymised fields of a host's own release whose timing cannot be
     tested stay with a note; a field that fixes a person's later decision at near-certainty inside a large group is
     a measured mechanism, and LEAK-10 drops it with the fields that mark the same rows.

   [^6b]: DataRobot, "Predict which insurance products to offer",
     https://pathfinder.datarobot.com/use-case/predict-which-insurance-products-to-offer; on the use of data known at
     the time of the offer: DataRobot, "Dynamic pricing for non-US insurers",
     https://www.datarobot.com/use-cases/dynamic-pricing-for-non-us-insurers/.

   **Resolved (2026-11-11, Andrej):** D: `PersonalField2` and `PersonalField13` are dropped after the five fields,
   the fewest that leave no group of 300 quotes converting at 95% or more; `PersonalField1` stays as a graded field,
   and so does the near-zero side, known when a quote is issued. Mean ROC AUC over the nine windows 0.898 (287
   features, `dataset check` 0 errors, 0 warnings). LEAK-38's clause now states that stopping point and that rows the
   decision cannot reach stay; the homesite case and the LEAK-10 mechanisms row give the numbers.

7. **Keep `SalesField5`, the strongest remaining field, whose timing cannot be tested?**

   * **Problem:**
     - On the quotes no marker settles, `SalesField5` = 5 (71,454 quotes) converts at 6.7% and levels 2 to 4
       (59,388 quotes) at 30.5% to 32.5%, the same in 2013, 2014 and 2015.
     - It carries 35% of the model's gain and alone reaches ROC AUC 0.765 on those quotes, high for one field when
       an honest quote model reaches about 0.70 to 0.85 (issue 6).
     - In sales data the strongest field usually records the sales process: a channel is known at the quote, a stage
       the customer reached (a call back asked for, an application started) partly comes after it.
   * **Background:** the field is anonymised, so its timing cannot be tested. It is graded, not near-certain (no
     level converts above 33% or below 6% on the open quotes), so the near-certainty clause of the keep rule for
     anonymised fields does not reach it[^7a]. On all quotes its levels also carry the dropped status (level 5 holds 36,990 of the code-5
     quotes); the figures above exclude them.

     | `SalesField5`, open quotes | Quotes | Bought | 2013 | 2014 | 2015 |
     |---|---|---|---|---|---|
     | 2 | 7,714 | 30.5% | 28.9% | 31.3% | 31.8% |
     | 3 | 34,232 | 32.5% | 31.1% | 32.7% | 36.1% |
     | 4 | 17,442 | 30.7% | 31.4% | 29.4% | 32.4% |
     | 5 | 71,454 | 6.7% | 8.2% | 6.6% | 5.0% |

   * **Experiments:** option D of issue 6, untuned LightGBM on the nine monthly windows, mean ROC AUC:

     | What is scored | With `SalesField5` | Without |
     |---|---|---|
     | All test quotes | 0.8978 (0.890 to 0.912) | 0.8790 (0.871 to 0.894) |
     | Test quotes no marker settles | 0.8587 (0.844 to 0.878) | 0.8331 (0.814 to 0.853) |
     | Trained and tested on those quotes only | 0.8619 (0.850 to 0.879) | 0.8362 (0.818 to 0.861) |

     - Without it the model loses 0.019 on all quotes and 0.026 on the open ones; the rest of the fields still
       reach 0.83 on the open quotes, inside the estimate of issue 6.
   * **Options:**

     | | Option | What it does | General rule it follows | Pro | Con |
     |---|---|---|---|---|---|
     | A | Keep, with a note (implemented) | a curation bullet: the strongest field, timing untestable, two-valued in effect | an anonymised graded field stays when its timing cannot be tested, as the keep rule says since today | the rule as written; a channel reading is as plausible as a stage reading; stable over three years | if it is a sales stage, part of the score comes after the quote |
     | B | Drop | add `SalesField5` to the drop list | an untestable field whose strength alone is near the ceiling of the use case is dropped | removes the most likely remaining post-quote field | drops on suspicion, not on a measured mechanism; the house rule keeps such fields; loses 0.02 to 0.03 |

   * **Recommendation:** A: graded, stable, and with a plausible pre-quote reading (the channel); the note names it
     as the field to look at if Homesite's field descriptions ever surface. **Decision:** A or B?

   **Notes for the AI:** on A, add to the curation bullets "- `SalesField5` is the strongest field (35% of the
   model's gain; on quotes no near-certain marker settles, level 5 converts at 6.7%, levels 2 to 4 at 30.5% to
   32.5%, the same in 2013 to 2015); it may record the channel (known at the quote) or a sales stage (partly after
   it), which the anonymisation hides; kept under the rule for untestable anonymised fields", `dataset check`. On B,
   add it to the drop list with a comment, extend the curation bullet and `fit_reason`, a CC line, `dataset check`.
   Evidence: `~/claude_jobs/homesite_drop/sf5.py`, `sf5.out`.

   [^7a]: **LEAK-38** (Should; amended 2026-11-11): anonymised fields of a host's own release whose timing cannot be
     tested stay with a note; a field that fixes a person's later decision at near-certainty inside a large group is
     a measured mechanism, and LEAK-10 drops it.

   **Resolved (2026-11-11, Andrej):** A: `SalesField5` stays, with a `Potential leak, kept on purpose:` curation note
   (the channel or a sales stage, hidden by the anonymisation; level 5 6.7% against 30.5% to 32.5% on the quotes no
   marker settles; 0.879 without it; revisit if Homesite's field descriptions surface).

## Reference

Darrel, Stephen D Stayton, and Will Cukierski. Homesite Quote Conversion. https://kaggle.com/competitions/homesite-quote-conversion, 2015. Kaggle.
