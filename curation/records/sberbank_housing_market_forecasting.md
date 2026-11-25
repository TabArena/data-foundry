---
unique_name: sberbank_housing_market_forecasting
name: Sberbank Housing
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
priority: 3
tags:
- Non-IID (Temporal)
- 'Samples: Over Time'
- 'Time: Dated'
- 'Target: Varying Delay'
- 'Features: Read Later'
- Dated Event Log
collections:
- TabArena Reject
- TabRed
original_source: Kaggle
year: '2017'
collection_period: Aug 2011 - Jun 2015
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.kaggle.com/competitions/sberbank-russian-housing-market
- https://github.com/yandex-research/tabred/tree/main/preprocessing#sberbank-housing-market-forecasting
notebook_path: datasets/beyond_iid/temporal/sberbank_housing_market_forecasting/sberbank_housing_market_forecasting.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/sberbank_housing_market_forecasting/dataset.py
source_row: 711
type_adapter_id: curation-record-v1
---

## Comments

Use TabRed preprocessing (verify it)

TabRed uses 5 and 7 months for splits

Data splits used by Kaggle experts were grouped/stratified IID ("CV for Investment type model was almost unusable, but CV for OwnerOccupier"). The predicted mean was then off for test data and they used some magic numbers to correct. Thus it sounds like real temporal splits would be better. https://www.kaggle.com/competitions/sberbank-russian-housing-market/discussion/32717

Moreover, it seems that the data is merged from two groups!

CC (2026-10-14, Lennart): Keep all 1,126 sales whose build year is after the year of sale (1,124 look like flats sold before completion). 28,321 rows.

CC (2026-10-21, Lennart): "ok" on the consistency check against mortgage (which lags each macro series to its release, LEAK-10); mortgage's lag applied: the monthly and quarterly macro series are lagged by one period.

**Assessment (AI, 2026-10-21):** Frequencies read from macro.csv (values constant within each period over 2010-2016): 7 daily market series (exchange rates, Brent, stock indices) keep the sale date; 20 monthly (one month back), 5 quarterly (one quarter back) and 66 yearly series. The yearly series change only on January 1 and hold their own year (Moscow salary of 2014, 61,208 rubles, on 2014 sales), so 64 are lagged by one year; `gdp_annual` and `gdp_annual_growth` already hold the previous year (2014 rows: Russia's 2013 GDP) and stay. `gdp_quart` already holds the previous quarter, so the model now sees GDP two quarters back, as in mortgage. Rows and feature count unchanged (28,321, 386; lagged columns renamed `_lag_1m`/`_lag_1q`/`_lag_1y`). Effect on LightGBM (500 trees, lr 0.03) RMSE over the 5 windows, newest first: 0.2268/0.2448/0.2647/0.2730/0.2548 before, 0.2269/0.2452/0.2633/0.2698/0.2548 after (mean 0.2528 to 0.2520; dummy 0.39), so the unlagged statistics carried no measurable signal. dataset check: 0 errors, 0 warnings; the build is stale (not rebuilt).

CC (2026-10-21, Lennart): the declared metric documents the original use case's metric; overrule it only when it is biased or wrong (evidence from the paper); keep the note of the original metric (TP-6 amended).

**Assessment (AI, 2026-10-21):** metric stays the default RMSE: the competition scored RMSLE on the flat's price (Kaggle API), and the task ships log price per square metre (TabReD), a target the competition did not score, so RMSE on the log target is the nearest listed metric (rule 4). The notes now name RMSLE. Needs a rebuild to reach the container (notes only).

CC (2026-10-21, Lennart): "yes we should have one clear way to treat 0/1 flags": every 0/1 flag (a feature holding only 0 and 1, plus missing values; booleans too) is categorical (CLEAN-14, amended). Typed categorical here: mosque_count_500, mosque_count_1000, mosque_count_1500, mosque_count_2000.

CC (2026-10-21, Lennart): on which 0/1 columns are flags: "no if we can infer from the semantic context, keep it a number, this is a real-world bias. We want to make things categorical if we know from the context they are indeed such" (CLEAN-14, amended again). Reverted: mosque_count_500, mosque_count_1000, mosque_count_1500, mosque_count_2000 (counts) stay numeric.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source rmse — Root Mean Squared Logarithmic Error (RMSLE) on price_doc (https://www.kaggle.com/competitions/sberbank-russian-housing-market/overview/evaluation).

**Assessment (AI, 2026-10-21):** metric stays rmse on log(price_doc / full_sq), not `rmsle` + `target_transform`: the inverse of the shipped target is the price per square metre, not the price the competition scored, so RMSLE after the inverse would score the price per m2 (off by log vs log1p and by the per-m2 scale) and is no closer to the competition's RMSLE than the current RMSE, which equals RMSE of log(price) up to log vs log1p.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): 2 ordinal scales typed as ordered categories in the codebook's order (CLEAN-14, amended): `state`, `ecology` (the README lists their levels); their codes that mean unknown (don't know, refused, not asked) are missing in `state`, `ecology` (CLEAN-10).

CC (2026-10-31, Lennart): marks on the review board of PR #37 (ordinal scales in the codebook's order, also when shipped as numbers; a state outside a scale missing when the column has no other missing value, else the lowest level; cycles ordered; codes shipped as numbers as categories): ID_metro a category, like the other station ids.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `dubai_dld_sales_transactions` (TBD -> Yes, priority 3). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-01, Lennart): the decode rule (a code whose codebook says in words what each level is carries the words; a score without them is a number): 1 coded columns carry their words; 1 scores are numbers (state).

CC (2026-11-06, Andrej): the arrival facts of the temporal split accepted (Review issue 1, B, through the cross-dataset item on arrival notes of temporal splits) and written into `splits_comment`; the split is unchanged. The date is the sale, no recording delay is documented, and the newest month shows no selection by price, so no gap.

CC (2026-11-10, Andrej): "Option B: Target: Varying Delay." (Review issue 2): `Target: Later` replaced by `Target: Varying Delay`.
- A Moscow sale's price arises at its signing, an unrecorded time after each flat came on the market that differs between sales, not at a shared date or after a fixed window.
- The other house-sale records are not changed from here.

**Assessment (AI, 2026-11-10):** priority for the review of the test windows and horizons, which this record never had. Priority 3: gap 0, use case 0, source + (Sberbank's competition), shape +, risk 0 (the open issue is the window length and the floor).

CC (2026-11-11, Lennart): Review issue 6 ("Agree.", to the answer that the windows follow the length of the horizon sign-off): the three seven-month windows of the horizon replace the five half-years from January 2013, whose three oldest trained on 44.3%, 28.6% and 17.8% of the sales.

CC (2026-11-11, Lennart): the declared horizon (7 months, no gap, windows starting 2014-12-01, 2014-05-01 and 2013-10-01) is checked, as seven months is the shortest test period of the sources (TabReD's; the competition tests eleven months), where the half-year was our own assumption; the window under half the sales, October 2013 to April 2014 on 35.4%, beside 83.6% and 59.1%, is signed off with it (Review horizon, a: "Reply (a): Seven months"; SPLIT-14 as amended 2026-11-11).

**Assessment (AI, 2026-11-11):** applied the horizon (a) and issue 6: `temporal` declares `TemporalSplits(window=7, unit="months", cutoffs=("2014-12-01", "2014-05-01", "2013-10-01"))`, confirmed with `window_bounds` on the definition's frame. Test 4,647, 6,936 and 6,704 sales (mean log price per square metre 11.84, 11.82, 11.80); train 23,674, 16,738 and 10,034 (83.6%, 59.1%, 35.4% of 28,321). The windows are adjacent: moving the oldest back lowers its train side (33.3% from September 2013, 31.1% from August). `accepted_check_warnings` takes `splits_train_under_half` with the sign-off; `dataset check`: 0 errors, 0 warnings, no `splits_floor_core` (the five half-years had three windows under half).

CC (2026-11-11, Lennart): accepted `splits_feature_missing_in_test` with a note naming the columns (cross-dataset item "Accept splits_feature_missing_in_test where a column starts or stops being recorded within the history?", A: the data as the deployed model met it).

CC (2026-11-11, Lennart): accepted `time_newest_period_short` with its reason (cross-dataset item "What to do with a newest period that holds far fewer rows than the periods before it?", A).

**Assessment (AI, 2026-11-11):** the lag of `provision_retail_space_sqm` is recorded from 2012 Q1 to 2013 Q4, the two education lags from 2014 Q1; 2015 holds 394 to 724 sales a month, 1,044 to 1,583 from September to December 2014, with a flat log price (11.80 to 11.87).

CC (2026-11-11, Andrej): "Option B: Keep, with a note." (Review issue 4): the district statistics and neighbourhood features stay, with a `Potential leak, kept on purpose:` note in the curation notes and a clause in `fit_reason`.
- None of 145 districts and none of 2,991 buildings sold in more than one year changes in them over 2011-2015, so they are one read of unknown date; older sales may carry facilities (metro stations of 2014-2015) that came after them.
- Not dropped: the read cannot be dated row by row and the data owner released it for its own competition, as the rule on fields of undocumented timing in a host's release allows; revisit if dated district statistics are found.

CC (2026-11-11, Andrej): five quarterly test windows from 2014 Q2 to 2015 Q2 (Review issue 3, B) with a 14-day gap for the deed registration (Review issue 5, B): superseded the same day by Lennart's seven-month windows without a gap (Review issue 6) and on 2026-11-19 by nine one-month windows without a gap (Review issue 7); not applied.

CC (2026-11-17, Andrej): the declared split (temporal on `timestamp`, windows of 7 months, 3 windows at fixed cutoffs, no gap) is checked: the split decision tree, walked without the current split, reaches the split it ships (blind split walk, cross-dataset item).

CC (2026-11-19, Andrej): nine one-month windows, all training on half the sales or more (the seven months were a benchmark's test period, not a refit cadence) (Review issue 7).

## Review

**Outcome:** added. From 2026-11-06 to 2026-11-11 Andrej accepted the time facts of the windows (issue 1), set
`Target: Varying Delay` (issue 2), chose five quarterly windows from 2014 Q2 (issue 3) with a 14-day gap for the deed
registration (issue 5), and kept the district and neighbourhood values, one read of unknown date, with a note
(issue 4). On 2026-11-11 Lennart chose seven-month windows (H, a), which also settles the windows (issue 6): December
2014 to June 2015, May to November 2014 and October 2013 to April 2014, the oldest on 35.4% of the sales with his
sign-off; these replaced the quarterly windows and their gap. On 2026-11-19 Andrej replaced them by nine one-month
windows from March 2014 to June 2015, every one training on half the sales or more, with no gap (issue 7, D); nothing
is left open.

**Main points:** Settled on 2026-11-19: nine one-month test windows (June, April and February 2015; December, October,
August, June, April and March 2014), training on 50.9% to 98.6% (issue 7, D), in place of the three seven-month
windows of 2026-11-11 (issue 6, H), which had replaced five half-years from January 2013, and of the quarterly
windows with a 14-day gap (issues 3 and 5), never shipped. Settled on 2026-11-11: the district and neighbourhood values
stay, with a `Potential leak, kept on purpose:` note and a `fit_reason` clause (issue 4). Settled on 2026-11-10:
`Target: Varying Delay` (issue 2). Settled on 2026-11-06: the time facts of the windows (issue 1), of which issue 7's
rewrite keeps the reason for no gap.

**Horizon:**

* **Verdict:** change to five-month windows (medium confidence): the sources test seven to eleven months, the half-year
  is our own reading of a refit cadence, and five months is the longest length that keeps three separate windows above
  half the sales in the sixteen months open.
* **Length:** declared six months, "a model that is refit every half year", our assumption: no source gives
  Sberbank's refit cadence. The competition tests the eleven months after its training data ("The test set contains
  ~7K realty transactions spanning from July 2015 to May 2016",
  https://www.r-bloggers.com/2017/06/a-data-scientists-guide-to-predicting-housing-prices-in-russia/). TabReD tests
  seven months (1 December 2014 to 30 June 2015) after five months of validation, and its analysis splits use windows
  of 4,500 sales, "roughly 5-7 month time-frame" (https://github.com/yandex-research/tabred/tree/main/preprocessing);
  the record's "TabRed uses 5 and 7 months for splits" is that. A lender values the flat at its sale, so the length
  says how long one fitted model serves.
* **Gap:** none needed: a sale's price is known when it is signed, and the economic statistics are already read one
  period back for their release delay.
* **Time frame:** 28,321 sales from August 2011 to June 2015, dense from 2014: 1,000 to 1,200 a month in 2014, 1,583
  in December 2014 (the month the ruble fell), 394 to 724 a month in 2015. Half the sales lie before March 2014, so the
  windows open are March 2014 to June 2015 (16 months, 13,914 sales); today's windows reach back to January 2013.
* **Options:**

  | | Option | What it does | Test windows | Pro | Con |
  |---|---|---|---|---|---|
  | A | Six months (implemented) | half-year windows, as for a refit every half year: only July to December 2014 and January to June 2015 keep half the sales for training | 5 windows of 3,051 to 6,434 sales (2 above the floor) | today's length; within TabReD's analysis windows of "roughly 5-7 month" | a half-year refit is our assumption: no source gives Sberbank's cadence; two windows above the floor, not three |
  | B | Five months | three separate windows from April 2014 to June 2015, within the sixteen months open | 3 windows of 2,670 to 5,234 sales | the longest length that keeps three separate windows above the floor; the low end of TabReD's analysis windows | shorter than the sources' test periods of seven to eleven months; three windows, the fewest allowed |
  | C | Four months | four windows over all sixteen months open | 4 windows of 2,219 to 4,562 sales | four windows; every month open tested | shorter than any source's test period |
  | D | Six months stepping by three | today's length, four windows three months apart | 4 overlapping windows of 3,064 to 6,288 sales | keeps today's length; four windows | the windows overlap: the sales of July 2014 to March 2015 are tested twice |
  | E | Three months | five quarters from April 2014 | 5 windows of 1,430 to 3,791 sales | five windows | half the shortest source period |

* **Recommendation:** B: five months is the longest length that keeps three separate windows above the floor in the
  sixteen months open, nearest the sources' test periods. **Decision:** A, B, C, D or E?

**Lennart (2026-11-11, discuss):** So we should do 7-11 months from the source, why dont we do 7 then? or is it too little
training data?

**Answer (AI, 2026-11-11):** Use 7-month windows, the shortest test period of the sources, now that the amended floor
admits one window at 35%?

* **Problem:**
  - The sources test 7 to 11 months (Kaggle: July 2015 to May 2016; TabReD: 7 months), and 7 months was out only
    because its third window trains on 35.4% of the sales.
  - Since 2026-11-11 the newest window and one other must train on at least half the sales and further windows on at
    least 30%[^a-14], so 7 months gives exactly three windows: two above half and one at 35.4%.
  - Today's six months test five windows, three of them under half (44.3%, 29%, 17.8%), which the amended floor does
    not admit.
* **Options:**

  | | Option | What it does | Test windows | Pro | Con |
  |---|---|---|---|---|---|
  | a | Seven months | December 2014-June 2015, May-November 2014, October 2013-April 2014 (83.6%, 59.1%, 35.4%) | 3 windows of 4,647 to 6,936 sales | the sources' shortest test period; no choice of windows left to argue | the oldest trains on 35.4% |
  | b | Six months, three windows | January-June 2015, July-December 2014, January-June 2014 (89.2%, 67.0%, 44.3%) | 3 windows of 3,064 to 6,434 sales | today's length; the oldest trains on 44.3% | a length no source uses |
  | c | Five months (the block's B) | February-June 2015, September 2014-January 2015, April-August 2014 (90.6%, 72.1%, 54.8%) | 3 windows of 2,670 to 5,234 sales | every window above half | shorter than every source's test period |

* **Recommendation:** a: the length the sources use, and the amended floor admits its third window.
  **Decision:** a, b or c?

[^a-14]: **SPLIT-14** (Must; amended 2026-11-11, Lennart): the newest window and at least one other train on at least 50% of the data; further windows down to 30%, and at most as many windows under 50% as at or above it.

**Lennart (2026-11-11, discuss):** Reply (a): Seven months

**Resolved (2026-11-11, Lennart):** a, seven-month windows with no gap, the shortest test period of the sources
(TabReD's seven months; the competition tests eleven), in place of the half-year, our own assumption. `temporal`
declares `TemporalSplits(window=7, unit="months", cutoffs=("2014-12-01", "2014-05-01", "2013-10-01"))`, confirmed with
`window_bounds` on the definition's frame: test 4,647, 6,936 and 6,704 sales, train 23,674, 16,738 and 10,034 (83.6%,
59.1%, 35.4%). Your mark signs off the window under half, October 2013 to April 2014 on 35.4%:
`accepted_check_warnings` takes `splits_train_under_half` with it, and the splits comment names it and its share.
`task_summary.split`, the half-year sentence of `fit_reason`, `splits_comment` (the length's reason from this block,
the windows and the counts) and a curation note are rewritten. The record has the horizon CC line. `dataset check`: 0
errors, 0 warnings; the `splits_floor_core` error of the five half-years is gone (README not regenerated).

**Issues:**

1. **Time basis: train on every sale up to the window's start, with no gap, and write in `splits_comment` how the price arrives?**

   * **Problem:**
     - The row's date is the sale, the day its price arises, while the prediction point is before the signing; the
       source does not say when Sberbank learned of a sale, so whether a refit at a window's start knew the last
       weeks' sales is not documented.
     - The split is temporal and needs no time-basis tag[^1a]; `splits_comment` says only that a model is refit every
       half year, and the record's target fact is issue 2.
     - Keep no gap and write the facts down (B), keep the text (A), or leave a one-month gap (C)?
   * **Background:**
     - The house-sale tasks differ by what their sources show: zillow_prize leaves a month because Zillow receives
       sales late, house_sales a week for the measured delay to recording, melbourne_housing_market none because its
       newest weeks were measured complete, and ames_housing and perth_house_prices none because their dates are
       months[^1b].
     - The hosts released the training sales and the test sales (July 2015 to May 2016) together in 2017, so June
       2015 was nearly a year old at the extract; a shortfall from late records is unlikely, and the measurement
       below finds none by price.
   * **Experiments:** today's run on the shipped rows (27,195 sales; LightGBM, 500 trees, three seeds), a refit at
     the start of each of the newest 12 months:

     | Month | Sales | Investment share | Mean residual, no gap | RMSE, no gap | RMSE, one-month gap | RMSE, no gap at the gap's size |
     |---|---|---|---|---|---|---|
     | 2014-07 to 2015-05 (range) | 381 to 1,432 | 54% to 72% | -0.007 to +0.058 | 0.206 to 0.258 | 0.213 to 0.264 | 0.210 to 0.258 |
     | 2015-06 | 333 | 43.5% | -0.016 | 0.263 | 0.265 | 0.264 |
     | mean of the 12 months | | | | | +0.0067 against no gap | -0.0004 against no gap |

     - The newest month of training sales is worth 0.007 RMSE at equal training size; that is what a gap would give
       up, and what the notes should state if the labels were late in use.
     - June 2015 is fewer, less investment-heavy and a little dearer to predict, but its mean residual sits just
       outside the other months' range on the side of a falling market (February 2015: -0.007), not of sales missing
       by their price.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | No gap, text as is (implemented) | each window trains on every sale before it | no change | the reason for no gap and the release-end check stay unwritten |
     | B | No gap, with the time facts in `splits_comment` | as A; the text states that the date is the sale, that no record delay is documented, the release-end check, and what the newest month adds | the reasons and today's numbers written down; keeps the month that matters most in a moving market | rests on the release having no late records, which is argued from the extract date and the residuals, not documented |
     | C | One-month gap | `gap=1` (months): each window trains on the sales up to a month before it | covers a record delay of up to a month, as zillow_prize | no delay is documented or measured; gives up 0.007 RMSE of real recent information |

   * **Recommendation:** B: the measurement shows no selection at the release end and no delay is documented, so no
     gap, with the newest month's worth stated. **Decision:** A, B or C?

   **Notes for the AI:** on B, append to `splits_comment` (after issue 3's rewrite): "Time basis of the windows: the
   date is the sale, the day the price arises; the source gives no date at which Sberbank recorded a sale, and the
   training and test sales were released together in 2017, so the newest training months are complete. No gap: a
   refit at the start of each of the newest 12 months shows no selection by price at the release end (June 2015,
   333 sales, mean residual -0.016 against -0.007 to +0.058 for the other months), and the newest month of training
   sales improves the next month's RMSE by 0.007 at equal training size (LightGBM, 2026-11-06)." No `data_tags`
   change. On C, `gap=1` in `TemporalSplits` (months), recheck the training shares against the floor, `dataset check`.

   [^1a]: **SPLIT-32** (Should): the record carries the source's collection facts; a temporal split needs no use-case
     prototype.
   [^1b]: **SPLIT-10** (Should): a gap of about the label's delay; the measurements decide; no gap where the newest
     period is as complete as a later read of it and no selection by the outcome shows at the release end; the notes
     give what the newest labels add at equal training size. Cases: zillow_prize, house_sales,
     melbourne_housing_market, ames_housing, perth_house_prices.

   **Resolved (2026-11-06, Andrej):** B, accepted through the cross-dataset item "Accept the arrival notes on temporal
   splits with one mark?" The time facts of the windows (the date is the sale, no documented recording delay, the
   release-end check and what the newest month adds) are appended to `splits_comment`; a rewrite under issue 3 keeps
   them. The split, its gap and `data_tags` are unchanged; a temporal split takes no time-basis tag.

   **Superseded in part:** the rewrite of `splits_comment` for the nine one-month windows (issue 7, 2026-11-19) keeps
   only the reason for no gap (a sale's price is known when it is signed); the release-end check and what the newest
   months add are no longer in the definition. No gap holds again since issue 7 (see issue 5).

2. **Correct the record's collection facts: `Target: Varying Delay` instead of `Target: Later`?**

   * **Problem:**
     - `Target: Later` stands for a target that arrives at one shared date or after a fixed window, but a Moscow
       sale's price arises at its signing, an unrecorded and different time after each flat came on the market.
     - The house-sale records disagree: zillow_prize, house_sales and california_house_prices_2020 carry `Target:
       Varying Delay`, melbourne_housing_market and perth_house_prices `Target: Later`, ames_housing and
       miami_housing none.
     - Set `Target: Varying Delay` (B), keep `Target: Later` (A), or drop the target fact because the row is the sale
       (C)?
   * **Background:** the target fact is there to point at the check a split needs: a varying delay points at the
     gap and the release-end test (issue 1), a shared date at a one-moment prototype that does not fit here[^2a].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | `Target: Later` (implemented) | the record as is | no change | names a shared date or a fixed window the sales do not have |
     | B | `Target: Varying Delay` | the record's tag replaced | matches the arrival and three of the house-sale records; points at the gap check | none found |
     | C | No target fact | the tag removed | the price and the date arrive together in the row | hides that the price comes after the features, at a varying time |

   * **Recommendation:** B. **Decision:** A, B or C?

   **Notes for the AI:** on B, in `curation/records/sberbank_housing_market_forecasting.md` replace `'Target: Later'`
   with `'Target: Varying Delay'` in `tags`, add `Andrej` to `checked_by`, and a `CC (<date>, Andrej):` line giving the
   reason. The other house-sale records are not changed from here.

   [^2a]: **SPLIT-32** (Should): `Target: Later` (after the features, at one shared date or after a fixed window),
     `Target: Varying Delay` (after a delay that differs between samples), no tag when the target exists with the
     features.

   **Resolved (2026-11-10, Andrej):** B ("Option B: Target: Varying Delay."): the record's `tags` carry `Target: Varying
   Delay` in place of `Target: Later`, with a CC line; the other house-sale records are not changed from here.

3. **Move the test windows into the newest half of the sales?**

   * **Problem:**
     - The five half-year test windows (2013 H1 to 2015 H1) train on all earlier sales, which for the three oldest
       windows is 18%, about 30% and about 46% of the rows, below the floor of half that the rules set[^3a].
     - The flat's own facts (floors of the building, material, rooms, kitchen area, build year, condition) are
       missing for 97-100% of the sales before July 2013 and recorded from 2014 on, so the two oldest windows test a
       task without them.
     - Use quarterly windows from the newest half, keep half-year windows from 2014, or keep the five windows?
   * **Background:** sales per half-year grow from 628 (2011 H2) to 6,241 (2014 H1), so the early windows are small
     and their training side smaller. On the shipped rows (TabReD's filters, 27,195 sales) the half-year windows train
     on 18.6%, 29.8%, 45.5%, 68.5% and 89.8%; the v0.2 frame (1,126 sales more) gives 17.8% (5,053 rows) for the oldest
     and 89.2% for the newest. The missing shares of the flat's facts by half-year: 100% to 2012, 97% in 2013 H1, 19-39%
     in 2013 H2, 0% (floors, material, rooms) and 16-25% (build year, condition) from 2014. A change in what is
     recorded is a break in the history that the windows should not straddle[^3b].
   * **Effect on the task:** the oldest windows score models trained on a few thousand sales without the flat's
     facts, a smaller and different task than a model refit today; they enter the dataset's mean score with the same
     weight as the newest.
   * **Experiments:** quarterly windows on the shipped rows, newest first: 2015 Q2 (1,418 test sales, train 94.8%),
     2015 Q1 (1,365; 89.8%), 2014 Q4 (3,445; 77.1%), 2014 Q3 (2,340; 68.5%), 2014 Q2 (3,325; 56.3%); all after the
     flat's facts are recorded. The competition's own test period was the next eleven months, so no window length
     copies the source; the half-year in the definition is a chosen refit cadence.
   * **Consistency:** california_house_prices_2020 moved its windows to the newest half for the same rule (2026-10-21);
     wisconsin_local_government_property_insurance_fund ships one window at 41% on the curator's call, where five
     policy years allowed nothing else.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Five half-year windows from 2013 (implemented) | test 2013 H1 to 2015 H1, each trained on all earlier sales | a half-year refit cadence; the most test rows | three windows train on less than half of the rows; two oldest lack the flat's facts |
     | B | Five quarterly windows from 2014 Q2 | test 2014 Q2 to 2015 Q2, each trained on all earlier sales (56% to 95%) | meets the floor with five windows; every window has the flat's facts | a quarterly refit instead of half-yearly; smaller test windows (about 1,400 to 3,400 sales) |
     | C | Three half-year windows from 2014 | test 2014 H1 to 2015 H1 (train about 46%, 69%, 90%) | keeps the half-year cadence; every window has the flat's facts | the oldest window stays just below the floor, on your call |

   * **Recommendation:** B, quarterly windows from the newest half: it meets the rule without an exception and tests
     only the task as it is recorded now. **Decision:** quarterly windows (B), half-year windows from 2014 (C), or the
     five windows as they are (A)?

   **Notes for the AI:** on B, `TemporalSplits(window=3, unit="months", n_windows=5, min_train_fraction=0.5)`; on C,
   `window=6, n_windows=3` and an exception to SPLIT-14 in the notes with the train share. Rewrite `splits_comment`
   and the task summary's `split`, re-run `dataset check` and the task probes, and record the train shares of the
   v0.2 frame.

   [^3a]: **SPLIT-14** (Must): a temporal task has at least 3 windows, and no window's train side holds less than
     50% of the data; a task that cannot meet it ships under SPLIT-8.
   [^3b]: **SPLIT-20** (Should): decide what the train side holds from the use case; check the history for breaks
     (a change of rules or of the data collection). **SPLIT-12** (Should): the horizon is a human judgment from the
     source (its test window, the refit cadence).

   **Answer (AI, 2026-11-06):** the time framing supports B a little more; three facts from today's checks on the
   shipped rows[^3c].

   * **The cut falls on the day the label arises:** the row's date is the sale, so a window's training side holds
     every price known before it, as far as the release shows (issue 1 asks whether a gap is needed).
   * **Fresh months matter in this market:** in monthly refits over the newest year, the newest month's sales improve
     the next month's RMSE by 0.007 at equal training size (LightGBM, three seeds; dropping as many of the oldest
     sales instead changes it by 0.000). A half-year window predicts its sixth month from sales five months older
     than a quarterly one does, so B's quarterly refits are closer to how a model in use would keep up with the
     2014-2015 crisis.
   * **The newest month is in every option's newest window:** June 2015 holds 333 sales (the fewest of the year) with
     43.5% investment purchases against 54% to 72% before; its mean residual of -0.016 lies just below the other
     eleven months' range (-0.007 to +0.058), so its composition shifted without a sign that sales went missing by
     their price (issue 1).

   [^3c]: **SPLIT-32** (Should): how the data was collected is information for the split. **SPLIT-11** (Should):
     train on everything before the window. **SPLIT-20** (Should): decide the training history from the use case.

   **Andrej (2026-11-11, discuss):** Let us think again about what would be the right forecasting horizon and planning
   gap for the task based on the use case at hand and all information we can gather.

   **Answer (AI, 2026-11-11):** quarterly windows from 2014 Q2 fit the use case and are the only five-window design
   with every window above the floor; the gap should cover the deed registration, about two weeks (new issue 5).

   * **Use case:** Sberbank prices a flat at a sale or a mortgage; a model in use is refit regularly and prices the
     sales of the months after its refit. Kaggle's own setup is one model priced 11 months ahead (train to June 2015,
     test July 2015 to May 2016), no gap: a single refit, not a cadence, and one window cannot meet the floor.
   * **Contract to record:** the data dictionary calls the date "date of transaction"; ownership passes only at
     Rosreestr's registration, by law within 10 working days of the filing from 2015 (about two weeks). The dates are
     office days (Sunday 0.4% of sales, Saturday 7.7%, 2 sales on the January holidays): the filing or the
     registration day, the source does not say which.
   * **Fresh months matter:** at equal training size, leaving out the newest month costs 0.010 RMSE, three months
     0.025, six months 0.043 (one-month test windows over the newest year). A longer horizon mostly scores stale models.
   * **Sales per month** grow from about 250 (2012) to about 1,100 (2014), then 400 to 700 in 2015; a quarter holds
     1,400 to 3,800 sales, enough for a stable score.

   | Windows | Gap | Mean RMSE | Train share per window, newest first |
   |---|---|---|---|
   | 5 x 3 months | 0 | 0.240 | 94, 89, 76, 67, 55% |
   | 5 x 3 months | 14 days | 0.244 | 93, 88, 74, 64, 53% |
   | 5 x 3 months | 1 month | 0.250 | 92, 84, 72, 63, 51% |
   | 5 x 3 months | 3 months | 0.263 | 89, 76, 67, 55, 44% |
   | 5 x 3 months | 6 months | 0.279 | 76, 67, 55, 44, 35% |
   | 5 x 6 months (implemented) | 0 | 0.258 | 89, 67, 44, 29, 18% |
   | 3 x 6 months | 0 | 0.251 | 89, 67, 44% |

   LightGBM (500 trees, three seeds) on the v0.2 frame (28,321 sales), 2026-11-11.

   | | Horizon | Pro | Con |
   |---|---|---|---|
   | B | 5 quarterly windows from 2014 Q2 | a quarterly refit keeps up with the 2014-2015 crisis; every window above half; the flat's facts recorded | smaller test windows than half-years |
   | C | 3 half-year windows from 2014 | half-year cadence | oldest window at 44%, below the floor |
   | A | 5 half-year windows (implemented) | most test rows | three windows below half; two before the flat's facts |

   **Recommendation:** B, quarterly windows; the gap is decided in issue 5. **Decision:** B, C or A?

   **Andrej (2026-11-11, discuss):** Agree.

   **Resolved (2026-11-11, Andrej):** B: `TemporalSplits(window=3, unit="months", n_windows=5, min_train_fraction=0.5)`
   with issue 5's 14-day gap: five quarterly test windows, 2014 Q2 to 2015 Q2, train shares 93 to 53%. `splits_comment`,
   the task summary's `split` and `fit_reason` are rewritten; CC line in the record. Dataset check: see issue 5.

   **Superseded:** the same day Lennart chose three seven-month windows (the horizon, a, and issue 6), and on
   2026-11-19 Andrej set nine one-month windows, March 2014 to June 2015, every one training on half the sales or more
   (issue 7). The quarterly windows were never shipped.

4. **Keep the district and neighbourhood values, one read of unknown date copied onto every sale since 2011, with a note?**

   * **Problem:**
     - None of the 145 districts and none of the 2,991 buildings sold in more than one year changes over 2011-2015 in
       any of 26 district and distance columns checked (population, schools, shops, offices, distances to the metro,
       parks and schools, counts of cafés, offices and markets nearby): the neighbourhood is one read, of a date the
       source does not give.
     - Moscow kept building in these years (the metro stations Spartak and Troparyovo opened in 2014, Kotelniki in
       2015), so an older sale can carry a station, shop or school that came after it.
     - Keep the columns with a note (B), keep them as they are (A), or drop the district statistics (C)?
   * **Background:**
     - The read cannot be dated or undone row by row (the release keeps no history), and the data owner released it
       for its own competition; such fields stay with a note that gives the mechanism and when to revisit[^4a].
     - The direction: a later read misdescribes older training sales, which weakens the signal there; a test sale
       can carry an amenity that opened after it, which buyers may or may not have priced in ahead.
     - house_sales keeps its view rating, waterfront flag and the neighbours' areas as of July 2015 with such a note
       (masking the view cost RMSE 0.2147 against 0.2132)[^4b].
     - Issue 3's B puts every test window in 2014-2015, the years closest to any read made for the competition.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep as they are (implemented) | no note | no change | the read's lateness is not stated |
     | B | Keep, with a note | a `Potential leak, kept on purpose:` bullet and a clause in `fit_reason` | the mechanism is written down; follows house_sales | the late part stays in the data |
     | C | Drop the district statistics | the `_raion` columns and the district population counts go; the distances stay | removes the part that is plainly a district table | the distances are the same kind of read; drops a large part of the source's features for a mechanism not shown to carry the target |

   * **Recommendation:** B. **Decision:** A, B or C?

   **Notes for the AI:** on B, a curation bullet: "Potential leak, kept on purpose: the district statistics and the
   neighbourhood features (distances, counts of facilities nearby) are one read of a date the source does not give:
   none of 145 districts and none of 2,991 buildings sold in more than one year changes in them over 2011-2015, while
   the city opened new metro stations (2014-2015) and other facilities. Older sales may carry facilities that came
   after them. They stay: the read cannot be dated row by row and the data owner released it for its competition.
   Revisit if dated district statistics are found." Add to `fit_reason`: "The neighbourhood figures are one read of
   unknown date, kept." `dataset check`; no change to the data.

   [^4a]: **LEAK-38** (Should): fields that may be post-outcome, whose timing the source leaves undocumented and no
     test can establish, in data the data owner released for its own competition, stay with a `Potential leak, kept on
     purpose:` note. **LEAK-10** (Must): attributes looked up after the outcome go where their late cells can be
     located.
   [^4b]: house_sales, curation notes: "Potential leak, kept on purpose: `view` ..., `waterfront`, `sqft_living15` and
     `sqft_lot15` (the neighbours' areas) are as of July 2015."

   **Resolved (2026-11-11, Andrej):** B ("Option B: Keep, with a note."): the columns stay; the curation notes carry
   the drafted `Potential leak, kept on purpose:` bullet (one read of unknown date, no change in 145 districts and
   2,991 buildings over 2011-2015, revisit if dated district statistics are found) and `fit_reason` the clause "The
   neighbourhood figures are one read of unknown date, kept."; CC line in the record. No change to the data.

5. **Leave a 14-day gap for the deed registration?**

   * **Problem:**
     - The date is the "date of transaction"; Rosreestr registers the transfer within 10 working days of the filing
       (the legal limit from 2015), so a refit on a window's first day would not yet know the last two weeks' sales.
     - Issue 1 chose no gap because no recording delay was documented; the registration limit is such a delay if the
       date is the deal's and not the registration's (the source does not say; both fall on office days).
   * **Experiments:** five quarterly windows (issue 3, B), LightGBM: no gap 0.240, 14 days 0.244, one month 0.250;
     with 14 days the train shares are 93% to 53%, all above half.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | No gap (implemented) | train on every sale before the window, as issue 1 chose | keeps the freshest sales | assumes the date is the registration |
     | B | 14-day gap | `gap=14, gap_unit="days"` | covers the legal registration time either way; costs 0.004 | may withhold two weeks that were known |
     | C | One-month gap | `gap=1` (months) | covers a slower bank pipeline too | longer than any documented delay; costs 0.010 |

   * **Recommendation:** B: the one documented delay is the registration, and covering it costs little.
     **Decision:** A, B or C?

   **Notes for the AI:** on B, `TemporalSplits(..., gap=14, gap_unit="days")` with issue 3's windows; replace the "No
   gap" sentence of `splits_comment` with the registration reason and these scores; check the train shares against
   the floor; `dataset check`. On C, `gap=1`.

   **Resolved (2026-11-11, Andrej):** B ("Option B: 14-day gap."): `gap=14, gap_unit="days"` with issue 3's quarterly
   windows; the "No gap" sentence of `splits_comment` is replaced by the registration reason and the scores (no gap 0.240,
   14 days 0.244, one month 0.250); CC line in the record. Dataset check: 0 errors, 0 warnings, 2 infos (9 exact and 11 conflicting duplicate rows); train 14,929 to 26,362 rows (53 to 93%), test 1,430 to 3,791.

   **Superseded:** the gap went with issue 3's quarterly windows. The seven-month windows of 2026-11-11 (issue 6) and
   the nine one-month windows of 2026-11-19 (issue 7) have no gap: a sale's price is known when it is signed.

6. **Which test windows should replace the five half-years from January 2013?**

   * **Problem:**
     - The five half-year test windows reach back to January 2013, and the three oldest train on 44.3%, 28.6% and
       17.8% of the sales, under the half every train side must keep[^sh-split14].
     - Half the sales lie before March 2014, so only two half-years (July to December 2014, January to June 2015) keep
       half for training, one fewer than the three windows every temporal task needs.
     - The newest window always stays and the others are chosen from the use case and statistics of the data, while
       the length comes from the source's horizon, and no source gives six months[^sh-split15][^sh-split12].
   * **Background:**
     - The one exception to the floor, an older window on at least 40% of the rows when two windows are above the
       floor and most test entities recur, does not apply: January to June 2014 trains on 44.3%, but a test row is a
       flat valued once at its sale (the release has no flat id), not an entity the lender re-rates.
     - The sixteen months open hold three phases of the market: 2014 with 1,000 to 1,200 sales a month, December 2014
       with 1,583, and 2015 with 394 to 724. B puts one window in each (April to August 2014, September 2014 to January
       2015, February to June 2015); C cuts all sixteen months into four; D keeps six months with windows three months
       apart, which overlap, so the sales of July 2014 to March 2015 are tested twice.
     - The target, the log price per square metre, has a mean of 11.81 to 11.85 in every candidate window and 11.73 to
       11.77 on the train sides; the 2013 windows of A are lower (11.68 and 11.76).
     - PSI, the population stability index, compares a feature's distribution in the window with its train side;
       above 0.25 is usually read as a large shift. The yearly and quarterly economic statistics hold one value per
       period, so their PSI is large in every window (8 to 18); the median over all features tells the windows apart.
   * **Statistics:** from the candidate tables, over all sales (every side is smaller than the tool's 100,000-row
     sample).

     | Window | In | Test sales | Mean target, test | Train side | Train share | Largest / median PSI |
     |---|---|---|---|---|---|---|
     | Mar-Jun 2015 | C | 2,219 | 11.82 | 11.77 | 92.2% | 11.7 / 0.084 |
     | Feb-Jun 2015 | B | 2,670 | 11.83 | 11.77 | 90.6% | 12.7 / 0.064 |
     | Jan-Jun 2015 | A, D | 3,064 | 11.83 | 11.77 | 89.2% | 17.4 / 0.056 |
     | Nov 2014-Feb 2015 | C | 3,592 | 11.85 | 11.76 | 79.5% | 9.1 / 0.027 |
     | Oct 2014-Mar 2015 | D | 5,221 | 11.84 | 11.76 | 75.8% | 8.8 / 0.034 |
     | Sep 2014-Jan 2015 | B | 5,234 | 11.83 | 11.76 | 72.1% | 8.5 / 0.032 |
     | Jul-Dec 2014 | A, D | 6,288 | 11.83 | 11.75 | 67.0% | 10.6 / 0.028 |
     | Jul-Oct 2014 | C | 3,541 | 11.81 | 11.75 | 67.0% | 12.9 / 0.025 |
     | Apr-Sep 2014 | D | 5,942 | 11.82 | 11.74 | 54.8% | 10.6 / 0.021 |
     | Apr-Aug 2014 | B | 4,893 | 11.82 | 11.74 | 54.8% | 9.8 / 0.020 |
     | Mar-Jun 2014 | C | 4,562 | 11.81 | 11.73 | 50.9% | 9.7 / 0.030 |
     | Jan-Jun 2014 | A | 6,434 | 11.81 | 11.72 | 44.3% | 18.4 / 0.035 |
     | Jul-Dec 2013 | A | 4,431 | 11.76 | 11.70 | 28.6% | 16.5 / 0.059 |
     | Jan-Jun 2013 | A | 3,051 | 11.68 | 11.72 | 17.8% | 18.4 / 0.117 |

   * **Effect on the task:** A scores three of its five windows with models fit on 18% to 44% of the sales, mostly the
     thin years 2011 to 2013. B scores three separate windows, before, around and after the December 2014 rush, each
     model fit on at least 54.8% of the sales and serving five months, against seven to eleven in the sources.
   * **Consistency:** california_house_prices_2020 moved its oldest window from 25% to 50% of the rows (2026-10-21).
     The housing family keeps each source's own horizon rather than one length for all (2026-10-21), and
     medical_facility_operational_data took its window length from its source (2026-11-05); here the source lengths
     do not fit three times into the history open, so B takes the longest that does. No dataset has chosen windows
     under the rewritten rule yet; delivery_eta_1m's issue 1 is open.
   * **Sources:** the definition `datasets/_dev/tabarena-v0pt2/sberbank_housing_market_forecasting/dataset.py`
     (`temporal`, `splits_comment`, `task_summary.split`, `fit_reason`); the record
     `curation/records/sberbank_housing_market_forecasting.md` (no earlier call on the windows); the candidate tables
     `.venv/bin/python -m data_foundry.curation.cli dataset windows sberbank_housing_market_forecasting --root
     datasets/_dev/tabarena-v0pt2` (5 windows) and the same with `--window 5 --unit months` (3 above the floor),
     `--window 4 --unit months` (4) and `--window 6 --unit months --step 3` (4).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Five half-years (implemented) | tests Jan 2013 to Jun 2015 in six-month windows | today's windows; 23,268 test sales | three train sides under the floor (44.3%, 28.6%, 17.8%); the half-year has no source |
     | B | Three five-month windows | tests Feb-Jun 2015, Sep 2014-Jan 2015 and Apr-Aug 2014 | every train side keeps at least 54.8%; one window before, around and after the December 2014 rush; the longest length that fits, nearest the sources | three windows, the fewest allowed; March 2014 untested; 12,797 test sales |
     | C | Four four-month windows | tests Mar-Jun 2015, Nov 2014-Feb 2015, Jul-Oct 2014 and Mar-Jun 2014 | four windows over all sixteen months open; 13,914 test sales | shorter than any source's test period; the oldest trains on 50.9% |
     | D | Six months, three months apart | tests Jan-Jun 2015, Oct 2014-Mar 2015, Jul-Dec 2014 and Apr-Sep 2014 | keeps today's length; four windows, every train side at least 54.8% | the windows overlap, so the sales of July 2014 to March 2015 are tested twice |

   * **Recommendation:** B: the longest length that keeps three separate windows above the floor, nearest the
     sources' seven to eleven months, with one window in each phase of the market. **Decision:** A, B, C or D?

   **Notes for the AI:** on B, `temporal = Temporal(on="timestamp", splits=TemporalSplits(window=5, unit="months",
   cutoffs=("2015-02-01", "2014-09-01", "2014-04-01")))`. Built with `window_bounds` on the definition's frame: test
   2,670, 5,234 and 4,893 sales, train 25,651, 20,417 and 15,524 (90.6%, 72.1%, 54.8%). On C, `TemporalSplits(window=4,
   unit="months", cutoffs=("2015-03-01", "2014-11-01", "2014-07-01", "2014-03-01"))`: test 2,219, 3,592, 3,541 and
   4,562, train 26,102, 22,510, 18,969 and 14,407 (92.2%, 79.5%, 67.0%, 50.9%). On D, `TemporalSplits(window=6,
   unit="months", cutoffs=("2015-01-01", "2014-10-01", "2014-07-01", "2014-04-01"))`: test 3,064, 5,221, 6,288 and
   5,942, train 25,257, 21,466, 18,969 and 15,524 (89.2%, 75.8%, 67.0%, 54.8%). Then rewrite `task_summary.split`
   ("Five test windows of six months, from January 2013 to June 2015 ... as for a model refit every half year"), the
   half-year sentence of `fit_reason` and `splits_comment` (the windows, the reasons and the numbers above), add a CC
   line to the record and a dated CHANGELOG entry, and run `dataset check` (SPLIT-12, SPLIT-14, SPLIT-15).

   [^sh-split14]: **SPLIT-14** (Must): "A temporal task has at least 3 windows, and no window's train side holds less
     than 50% of the data. ... A release with two windows above the floor may add one older window that trains on at
     least 40% of the rows, when most test entities recur (the actor re-rates entities it knows) and folds by entity
     would test unseen ones."
   [^sh-split15]: **SPLIT-15** (Must for the newest window, Should for the others; amended 2026-11-10, Lennart and
     Andrej): "The newest window is always a test window ... The other windows are the curator's choice, per dataset,
     argued from the use case ... The evidence is statistics of the data, never a model's score ... Every choice stays
     above SPLIT-14's floor; the length and the gap come from SPLIT-12."
   [^sh-split12]: **SPLIT-12** (Should): "The horizon is a human judgment from the source: how far ahead the actor
     predicts ..., the competition's own test window, the refit cadence. Choose the test windows to match it and write
     the reasoning down."

   **Lennart (2026-11-11, discuss):** 27 and 18 % seem to low indeed, come back to this case here after you looked over
   the others and my prompt

   **Answer (AI, 2026-11-11):**
   - The floor is amended (2026-11-11): two windows on at least half the sales, further windows down to 30%, never more
     windows under half than above. The 29% and 17.8% windows stay out under it.
   - The windows now follow the length you choose in the horizon (H): at 7 months, 6 months or 5 months exactly three
     windows remain, so this issue closes with H's choice.

   **Lennart (2026-11-11, discuss):** Agree.

   **Resolved (2026-11-11, Lennart):** closed with the horizon's choice (a): three adjacent seven-month windows,
   December 2014 to June 2015, May to November 2014 and October 2013 to April 2014, in place of the five half-years
   from January 2013; the oldest trains on 35.4%, signed off with the horizon's mark, beside 83.6% and 59.1%. Moving the
   older windows back would only lower their train sides (from September 2013 the oldest would train on 33.3%). The same
   edits as the horizon's; the record has the CC line. `dataset check`: 0 errors, 0 warnings.

7. **Train floor: keep the window under half the data as the curator's exception, or drop it?**

   * **Problem:**
     - October 2013 to April 2014 trains on 35.4% of the sales, beside December 2014 to June 2015 and May to November 2014 on 83.6% and 59.1%.
     - Since 2026-11-19, every window trains on at least half the data, and a window under half is the curator's exception for the dataset, down to 30%[^split14]; the sign-off (Lennart, 2026-11-11, review issue H, a) was given under the earlier rule, which admitted such windows beside two at half or more.
     - The definition has 3 windows; the target an IID split would get[^split33] for 28,321 rows is 9; without the window under half it keeps 2.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep the window as the curator's exception (implemented) | The accepted warning is reworded to the new rule; split unchanged | Keeps the periods it tests, as signed off; more windows toward the target | It trains on less than half the data |
     | B | Drop the window under half | The windows under half leave the declaration; a rebuild | Every window trains on half the data or more | 1 fewer window and the period it tests |

   * **Recommendation:** A, the sign-off's reason (periods or test rows the newest windows lack) still holds, and no window is under 30%. **Decision:** A or B?

   **Notes for the AI:** on A, reword the `splits_train_under_half` acceptance (drop "SPLIT-14's two tiers admit it", name the curator's exception and this decision) and add a CC line; on B, remove the windows from the declaration, rebuild, and update the splits comment.

   **Andrej (2026-11-19, discuss):** How exactly are the splits done? Could we reduce the window sizes while staying compliant with the use case and get to more than 50% on each train split?

   **Answer (AI, 2026-11-19):** Yes: the seven months are not fixed by the use case (they are TabReD's test period for one frozen model; no source gives Sberbank's refit cadence), so shorter windows are open, and one-month windows give nine windows that all train on more than half the sales.

   * **How the split is done today:** test windows of 7 calendar months, adjacent (step 7 months), no gap, at fixed starts walking back from the newest sale; each window trains on every sale before its first day. The scored unit is the sale (one row, 28,321 sales; no grouping). The target count for this size is 9 windows; the definition has 3.

     | Window (first and last sale) | Test sales | Train sales | Train share |
     |---|---|---|---|
     | 1 Dec 2014 to 30 Jun 2015 | 4,647 | 23,674 | 83.6% |
     | 3 May to 29 Nov 2014 | 6,936 | 16,738 | 59.1% |
     | 1 Oct 2013 to 30 Apr 2014 | 6,704 | 10,034 | 35.4% |

   * **What the use case and the sources fix, and what is ours:**
     - The sources fix only benchmark test periods: the competition tests the 11 months after its training data (July 2015 to May 2016), TabReD tests 7 months (December 2014 to June 2015) and cuts its analysis splits into windows of 4,500 sales ("roughly 5-7 month time-frame"). Each is how long one frozen model is scored, not how long a lender uses one.
     - The use case (a lender values a flat at its sale) gives no refit cadence, and no source states one. The 7 months is our pick, the shortest source period (Lennart, 2026-11-11).
     - No gap: a sale's price is known when it is signed, and the economic statistics are already read one period back.
     - The data fixes the floor: half the sales lie before 21 February 2014, so a window trains on half or more only from March 2014; March 2014 to June 2015 holds 16 months and 13,914 sales.

   * **Layouts by goal** (counted on the definition's frame; all no gap, every earlier sale in training):

     | Goal | Layout | Windows | Test sales per window | Train share | Overlap |
     |---|---|---|---|---|---|
     | Today | 7 months, adjacent | 3 | 4,647 to 6,936 | 35.4% to 83.6% | none |
     | The use case's length | 7 months, one every 3 months (Dec 2014, Sep 2014, Jun 2014, Mar 2014) | 4 | 4,647 to 7,467 | 50.9% to 83.6% | a sale of Sep to Dec 2014 is tested up to 3 times |
     | The use case's length, to the target | 7 months, one every month (Dec 2014 back to Mar 2014) | 10 | 4,647 to 7,467 | 50.9% to 83.6% | a sale is tested up to 7 times |
     | Stable test sizes, a source's length | TabReD's windows of 4,500 sales | 3 | 4,500 | 52.3% to 84.1% | none |
     | Stable test sizes, to the target | nine windows of 1,573 sales (4 weeks to 3 months each) | 9 | 1,573 | 50.0% to 94.4% | none |
     | Maximal number | one calendar month each, Mar 2014 to Jun 2015 | 16 | 394 to 1,583 | 50.9% to 98.6% | none |
     | Maximal number, at the target | one calendar month, every other month from Jun 2015 to Apr 2014, and Mar 2014 | 9 | 394 to 1,583 | 50.9% to 98.6% | none |
     | (between) | two calendar months, adjacent | 8 | 845 to 2,747 | 50.9% to 96.8% | none |

     The nine one-month windows, newest first:

     | Month | Test sales | Train sales | Train share |
     |---|---|---|---|
     | Jun 2015 | 394 | 27,927 | 98.6% |
     | Apr 2015 | 724 | 26,687 | 94.2% |
     | Feb 2015 | 451 | 25,651 | 90.6% |
     | Dec 2014 | 1,583 | 23,674 | 83.6% |
     | Oct 2014 | 1,044 | 21,466 | 75.8% |
     | Aug 2014 | 771 | 19,646 | 69.4% |
     | Jun 2014 | 1,179 | 17,790 | 62.8% |
     | Apr 2014 | 1,214 | 15,524 | 54.8% |
     | Mar 2014 | 1,117 | 14,407 | 50.9% |

     The nine windows of 1,573 sales start on 2 Apr 2015, 26 Dec 2014, 28 Nov 2014, 21 Oct 2014, 1 Sep 2014, 30 Jun 2014, 21 May 2014, 4 Apr 2014 and 22 Feb 2014; windows counted in sales cut through a day, so sales of one day can sit on both sides of a cut (harmless here: a price is known when it is signed). TabReD's windows of 4,500 sales run 2 Dec 2014 to 30 Jun 2015, 15 Jul to 2 Dec 2014 and 14 Mar to 15 Jul 2014.

   * **Options** (new, after A and B of the issue):

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | C | TabReD's 4,500-sale windows | three windows of 4,500 sales from 14 Mar 2014 | a source's own analysis windows; every window on 52.3% or more; equal test sizes | 3 windows, a third of the target |
     | D | One-month windows, nine | the nine months in the table above | reaches the target of 9; every window on 50.9% or more; holds 2015, the December 2014 rush and spring 2014 | test sizes vary fourfold (394 to 1,583); a monthly refit is our assumption |
     | E | Nine windows of 1,573 sales | equal-count windows over March 2014 to June 2015 | reaches the target; equal test sizes; every month open tested | windows of 4 weeks to 3 months, no fixed horizon; the oldest at 50.0%, on the edge |
     | F | Seven months, one every three months | overlapping 7-month windows from Dec, Sep, Jun and Mar | keeps today's length; every window on 50.9% or more | overlapping windows; 4 of 9 |

   * **Recommendation:** D: the use case ties no length, so the windows can follow the count; one calendar month is the simplest horizon that reaches nine windows above half, and even the smallest month (394 sales) is far above the least test window. C if you want to stay on a length a source uses. **Decision:** A, B, C, D, E or F?

   **Notes for the AI:** on C, `TemporalSplits(window=4500, unit="rows", n_windows=3)`; on D, `TemporalSplits(window=1, unit="months", cutoffs=("2015-06-01", "2015-04-01", "2015-02-01", "2014-12-01", "2014-10-01", "2014-08-01", "2014-06-01", "2014-04-01", "2014-03-01"))`; on E, `TemporalSplits(window=None, unit="rows", n_windows=9, min_train_fraction=0.5)`; on F, `TemporalSplits(window=7, unit="months", cutoffs=("2014-12-01", "2014-09-01", "2014-06-01", "2014-03-01"))`. Each drops `splits_train_under_half` from `accepted_check_warnings`; rewrite `task_summary.split`, the seven-month sentences of `fit_reason` and `splits_comment` (the length is ours, the use case ties none), add a CC line and a CHANGELOG entry, rebuild and run `dataset check`.

   **Andrej (2026-11-19, discuss):** Reply (D): One-month windows, nine

   **Resolved (2026-11-19, Andrej):** D. Nine one-month windows (June, April and February 2015; December, October, August, June, April and March 2014), 394 to 1,583 test sales, training on 50.9% to 98.6%; the under-half acceptance is gone; `fit_reason` and the splits comment say the use case ties no length. `dataset check`: 0 errors, 0 warnings. Not rebuilt.

   [^split14]: **SPLIT-14** (Must): every window trains on at least half the data, lower only as the curator's exception down to 30%; every test window holds at least 33 scored units.

   [^split33]: **SPLIT-33** (Should): an IID or grouped split gets 3-fold cross-validation with 20, 10, 3 or 1 repeats by the units on its train side; SPLIT-15 aims a temporal split at the same count.

## Reference

Alex Matveev, Anastasia_Sidorova_50806198, and DataCanary. Sberbank Russian Housing Market. https://kaggle.com/competitions/sberbank-russian-housing-market, 2017. Kaggle.
