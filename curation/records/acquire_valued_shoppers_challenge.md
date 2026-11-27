---
unique_name: acquire_valued_shoppers_challenge
name: Ecom Offers
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
priority: 1
decision_markers:
- Anonymized
tags:
- Non-IID (Temporal)
- 'Samples: Over Time'
- 'Time: Dated'
- 'Target: Fixed Delay'
- Dated Event Log
collections:
- TabArena Reject
- TabRed
original_source: Kaggle
year: '2014'
collection_period: Mar 2013 - Apr 2013
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.kaggle.com/c/acquire-valued-shoppers-challenge
- https://github.com/yandex-research/tabred/tree/main/preprocessing#ecom-offers-acquire-valued-shoppers-by-dmdave
notebook_path: datasets/beyond_iid/temporal/acquire_valued_shoppers_challenge/acquire_valued_shoppers_challenge.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/acquire_valued_shoppers_challenge/dataset.py
source_row: 709
type_adapter_id: curation-record-v1
---

## Comments

Follow TabRed preprocessing and how tables were merged. Investigate test.csv time range to see if it is relevant. Check if customers are unique or recurring across time and if we would need to filter customers.

TabRed uses 4 days as time horizon

CC (2026-10-06, Lennart): Kept as a real task after the task-probe review (flag `no_spread`). The signal is real but weak, and methods are hard to tell apart: the three untuned families reach skill +0.24 to +0.28 (ROC AUC about 0.62-0.64, standard deviation 0.06-0.08 over the 5 five-day windows of 2,758-30,305 test rows); on BeyondArena the best method (TabPFN-3.5-Fast) reaches AUC 0.654 and beats chance in every window, the median 0.646, and 12 of 21 methods are tied with the best. A low ceiling on a real repeat-buyer task, as in TabRed, is no reason to act.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source roc_auc — Area Under Receiver Operating Characteristic Curve (https://www.kaggle.com/competitions/acquire-valued-shoppers-challenge (Kaggle API evaluationMetric)).

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `ijcai15_repeat_buyers` (TBD -> Yes, priority 3). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-01, Lennart): the target rule (CLEAN-25) and the cut-end rule (CLEAN-14): the target ships as No/Yes, Yes the event (1 is the event).

**Assessment (AI, 2026-11-04):** reviewed for BeyondArena v0.2, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the record's Review. Ship as defined with the missing label gap recorded as an exception: the repeat period is unknown, a 5-day gap would leave 41% of the rows for the oldest window, and the newest offers show complete labels; separation is weak (12 of 21 tied), as Lennart accepted. Priority 1: gap 0, use case 0, source 0, shape 1, risk -1.

CC (2026-11-06, Andrej): the arrival facts of the temporal split accepted (Review issue 2, B, through the cross-dataset item on arrival notes of temporal splits) and written into `splits_comment`; the split is unchanged. Each shopper is predicted on its offer day from purchases before it, and the repeat label arrives after a period the source does not state; a curation note records that no purchase after the offer reaches the features.

CC (2026-11-12, Andrej): decided (issues 1 and 3).
- A five-day gap, four windows (issue 1, b, the AI answer of 2026-11-06): where a test window continues an offer wave, the five days before it add ROC AUC 0.061 at equal training size (LightGBM; logistic regression 0.022 and 0.031; 0.001 to 0.008 where a window starts a new wave), outcomes not yet known at the window's start. Test windows 11-15, 16-20, 21-25 and 26-30 April 2013 (2,758 to 30,305 offers), each trained on the offers up to five days before it (90,387 to 110,396 rows, 56.5% to 69.0%); 6 to 10 April dropped. The no-gap exception proposed on 2026-11-04 falls away: every train side stays above half the rows. Labels of older waves may still be open, as the repeat period is not published.
- `Target: Later` (issue 3, B): the repeat purchase comes after the offer, counted over a window the source does not state.
- The definition's check pipeline on the shipped frame (the Kaggle download is refused, rules not accepted): 0 errors, 0 warnings; `dataset check` itself not run, README not regenerated; not rebuilt.

CC (2026-11-17, Andrej): Review issue 4, A, as implemented: Four expanding windows on `offerdate`, test 11-15, 16-20, 21-25 and 26-30 April 2013 (2,758 / 5,344 / 30,305 / 19,356 offers), each trained on offers up to 5 days before it (train shares 56.5 / 63.9 / 65.6 / 69.0%), 5-day gap, temporal.

CC (2026-11-17, Andrej): Review issue 5, A, as implemented: Four expanding windows on `offerdate`, test 11-15, 16-20, 21-25 and 26-30 April 2013 (2,758 / 5,344 / 30,305 / 19,356 offers), train shares 56.5 / 63.9 / 65.6 / 69.0%, 5-day gap.

CC (2026-11-17, Andrej): verdict ship (blind split walk).

CC (2026-11-17, Andrej): the declared split (temporal on `offerdate`, windows of 5 days, 4 windows, gap 5 days) is checked: split mark in the blind split walk.

CC (2026-11-19, Andrej): windows below the target count kept (Review issue 6, A as implemented): four five-day windows; the next (6-10 April) would train on 41.4%; the reason is in the splits comment.

CC (2026-11-26, Lennart): task-probe flag `drift_baseline` after the rebuild of 2026-11-26: kept as shipped (TP-1, TP-2). The newest rows' class shares come within 2% of the best log loss, but ROC AUC, the metric, ignores the shares, and all 21 tuned configurations beat 0.5 in 5 of 5 folds.

## Review

**Outcome:** added. Kaggle's Acquire Valued Shoppers Challenge (2014): 160,057 shoppers who got a discount offer on
one product between 1 March and 30 April 2013, each shopper's purchase history summarised into one row per offer
(TabReD's preprocessing, after a top solution); the target is whether the shopper bought the product again (27.1%),
scored by ROC AUC, the competition's metric, on four test windows of five days from 11 to 30 April, each trained on
the offers up to five days before it (issue 1, b, decided 2026-11-12; the AI first recommended no gap, as an
exception). Reviewed without a review panel, from the gathered
evidence: the record, the BeyondArena results and checks on the shipped data; one model run on 2026-11-06 measured
what the newest training offers add (issue 1). Validity: the definition
keeps the competition's task and metric; every feature is from before the offer; the five-day gap keeps the outcomes
of the test window's own offer wave out of training, while labels of older waves may still be open (issue 1). Value: weak separation, decided: on the five BeyondArena windows the methods reach ROC AUC 0.625
(linear model) to 0.654 (TabPFN-3.5-Fast), 12 of 21 configurations are tied with the best and the ranks change from
window to window (Kendall's W 0.39); Lennart kept it on 2026-10-06 as a real task with a low ceiling. Quality: nothing
open. Weighed: a real retailer's offers with the host's metric and a time split +, weak separation, an unknown repeat
period and better data found for the same task -.

**Main points:** Nothing open. Decided 2026-11-12: a five-day gap with four windows, since the five days before a
window carry its offer wave's outcome (issue 1, b); `Target: Later` in the record (issue 3, B). The arrival facts are
in the split comment (issue 2, resolved 2026-11-06). Decided 2026-11-17: the four windows with the 5-day gap stay, not Kaggle's history files (issues 4 and 5, A). Decided 2026-11-19: four windows, below the target count, as the next (6-10 April) would train on 41.4% (issue 6, A).

**Record judgment:** valid, and the record's fields match the definition. The use case is the competition's: a brand
aims its offers at shoppers who stay. The offer's product, chain and brand are not features (only the offer value and
date, and the shopper's past purchases of the offer's company, category and brand). A scouting run found
`ijcai15_repeat_buyers` (`TBD -> Yes`, priority 3, not added) as better data for the same repeat-buyer task; this
record keeps the verdict its own data earns until that one is added.

**Issues for Andrej:**

1. **Train each window on every earlier offer although the newest offers' repeat purchases would not be known yet, and
   record it as an exception?**

   * **Problem:**
     - A shopper's label is a repeat purchase after the offer, in a period the competition does not state, so a model
       refit at a window's start would not yet know the labels of the offers made in the days before.
     - The definition trains each window on every earlier offer with its final label, and the offers come in waves
       that span the cutoff (22 to 28 April: 44,866 offers, across the last two windows).
     - Keep the windows as they are and record why, or add a gap?
   * **Background:** checked on the shipped data. The newest offers show no sign of labels cut short: shoppers of the
     last week of April repeated at 36.8%, and within the most common offer value ($1) the rate is 35% to 43% through
     April, highest in the newest weeks (42.8% and 40.4%).
     The offers' rates differ widely (13% to 53% by week), and offer value with the
     date can tell offers apart, which is how a label not yet known could help. A training row whose label is not known
     at the prediction point must not be in train, with a gap of about the label's delay[^1a]; but the oldest window
     already trains on 56% of the rows (90,387), and a gap of one window (5 days) would leave 41%, below the floor of
     half the rows[^1b].
   * **Effect on the task:** without a gap the windows may score a model that learned an offer's repeat rate from
     shoppers whose outcome came after the window started; how much cannot be measured without the repeat period.
   * **Consistency:** follows the exceptions where a gap would break the half-the-rows floor:
     pricing_game_2016_french_fleet
     (no gap, Andrej, 2026-11-02), alfa_battle_2_0_task_2 and lending_club (Lennart, 2026-10-21); and
     melbourne_housing_market, where a gap is set only if the newest period shows selection (Lennart, 2026-10-21).
   * **Unknown:** the period in which a repeat purchase counts; the competition's data page does not state it.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | No gap, recorded as an exception (implemented) | five windows of 5 days, each trained on every earlier offer; the exception and the measured rates in the notes (the record line still to add) | keeps five windows above the floor; the newest offers show complete labels | in-flight offers' labels are in training |
     | B | A gap of one window, four windows | train each window on offers until 5 days before it; the oldest window (6 to 10 April) dropped | fewer in-flight labels | the gap is a guess, as the repeat period is unknown; one window fewer; offer waves still span it |

   * **Recommendation:** A, a gap cannot be set from a known delay and would cost a window, and the newest offers show
     no missing labels. **Decision:** no gap with the exception (A), or a 5-day gap with four windows (B)?

   **Notes for the AI:** on A, add to `curation_comments`: "No gap between training and test windows (SPLIT-10
   exception): the repeat period is not published; a 5-day gap leaves 41% of the rows for the oldest window (SPLIT-14);
   the last week of April repeats at 36.8%, offer value $1 at 35% to 43% through April and highest in the newest
   weeks, so the newest labels look complete"; add the row to the SPLIT-10 cases table of splits.md and a CC line.
   On B, `TemporalSplits(window=5,
   unit="days", n_windows=4, gap=5)` (check the API's gap unit) and rerun `dataset check`.

   **Answer (AI, 2026-11-06):** Measured now: where a test window continues an offer wave, the five days before it
   carry the wave's outcome into the window; take the five-day gap with four windows (B)?

   * **Problem:**
     - Where a test window continues a wave that began in the five days before it (26 to 30 April continues the wave of
       22 April, 6 to 10 April the wave of 1 April), those five days' offers add ROC AUC 0.061 at equal training size
       (LightGBM; logistic regression 0.022 and 0.031); where a window starts with a new wave, they add 0.001 to 0.008.
     - A repeat purchase of an offer made one to five days before a window is not known at the window's start, so the
       model learns the test window's own wave from outcomes that came later[^1c].
     - With the gap, four windows remain and every training side holds more than half the rows (B above), so the floor
       that made A an exception no longer stands in the way[^1d].
   * **Background:**
     - The offers come in waves: an offer mix starts on one day and tapers over a week (22 April 5,621 offers, 24 April
       9,044, 30 April 1,419; the offer values $2 and $3 first appear on 23 April); the newest window's 19,356 offers
       have the value mix of the 30,305 made on 21 to 25 April, and both repeat at 36%.
     - Under B the test windows are 11-15, 16-20, 21-25 and 26-30 April (2,758 to 30,305 offers), each trained on the
       offers up to five days before it (90,387 to 110,396 rows, 56% to 69%).
     - Five days removes the labels of the test window's own wave; labels of older waves may still be open at a window's
       start, since the repeat period is unknown.
   * **Experiments:** the shipped container (the definition's rows and features) on the definition's five windows,
     untuned LightGBM and logistic regression (LR), ROC AUC; "equal size" keeps the five days and drops as many random
     older offers (three seeds):

     | Test window (offers, repeat rate) | Offers in the 5 days before | No gap (implemented) | 5-day gap | Equal size, with the 5 days | Added by the 5 days | LR, added |
     |---|---|---|---|---|---|---|
     | 26-30 Apr (19,356; 36.1%) | 30,305 (36.4%) | 0.636 | 0.575 | 0.636 | +0.062 | +0.022 |
     | 21-25 Apr (30,305; 36.4%) | 5,344 (21.5%) | 0.585 | 0.576 | 0.584 | +0.008 | +0.001 |
     | 16-20 Apr (5,344; 21.5%) | 2,758 (29.7%) | 0.643 | 0.642 | 0.642 | +0.001 | +0.002 |
     | 11-15 Apr (2,758; 29.7%) | 11,907 (27.4%) | 0.690 | 0.688 | 0.690 | +0.002 | +0.001 |
     | 6-10 Apr (11,907; 27.4%) | 24,095 (27.5%) | 0.691 | 0.630 | 0.691 | +0.061 | +0.031 |

   * **Consistency:** lt_vehicle_loan_default_prediction kept no gap for +0.0026 that reached the test rows through
     codes shared by many borrowers and stayed flat across windows; here the shared code is the offer, and the effect is
     twenty times larger and sits in the windows that continue a wave. alfa_battle_2_0_task_2 removed +0.002 to +0.009.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | No gap, as an exception (implemented) | A above; the notes give the +0.061 | five windows | two of five windows scored partly on their own wave's later outcomes |
     | b | Five-day gap, four windows | B above | removes the same-wave outcomes; every training side above half the rows | one window fewer (6 to 10 April); labels of older waves may still be open |

   * **Recommendation:** b: the measurement shows the shortcut the gap guards against, and the gap now costs no rule.
     **Decision:** a or b?

   **Notes for the AI:** on b, `temporal = Temporal(on="offerdate", splits=TemporalSplits(window=5, unit="days",
   n_windows=4, gap=5))` (the gap counts in days); `splits_comment`: "Four test windows of five days, 11 to 30 April
   2013, each trained on the offers made up to five days before it (56% to 69% of the rows). Offers come in waves that
   run over a week, and a repeat purchase is not known within days of the offer, so a refit at a window's start does not
   know the outcomes of the wave it scores; without the gap the five newest days add ROC AUC 0.061 where a window
   continues a wave (LightGBM, equal training size). The repeat period is not published: the gap removes the same-wave
   outcomes, not every open label."; task summary `split` ("Four test windows of five days, 11 to 30 April 2013, each
   trained on the offers until five days before it") and `fit_reason` (the in-flight labels of older waves); the SPLIT-10
   cases row (a five-day gap, measured); CHANGELOG; `dataset check`.

   [^1a]: **SPLIT-9** (Must): a training row whose label is not yet known at the prediction point must not be in train.
     **SPLIT-10** (Should): when a label is known only some time after its row, train on the rows whose outcome is known
     by the window's start, with a gap of about the label's delay.
   [^1b]: **SPLIT-14** (Must): a temporal task has at least 3 windows, and no window's train side holds less than 50%
     of the data.
   [^1c]: **SPLIT-9** (Must): a training row whose label tells a test row's outcome and was not yet known at the
     prediction point must not be in train; labels that reach a test row only through codes shared by many entities
     fall under SPLIT-10, with their measured size in the notes. **LEAK-12** (Must): in a temporal task, training rows
     whose label is not yet known at the prediction point are filtered out by an as-of date.
   [^1d]: **SPLIT-10** (Should; amended 2026-11-04 and 2026-11-05): the measurements decide; a gap is set where a
     measurement shows a shortcut through recent labels or a selection by the outcome at the release end; where the gap
     breaks SPLIT-14's floor, the departure is an exception.

   **Resolved (2026-11-12, Andrej):** b ("Five-day gap, four windows"): `TemporalSplits(window=5, unit="days",
   n_windows=4, gap=5)` (the gap counts in days); the drafted `splits_comment` merged with the arrival text of issue 2;
   the task summary's `split` and `fit_reason` rewritten; a SPLIT-10 cases row in splits.md; record CC line.

   | Test window | Offers | Trained on offers up to | Training rows (share) |
   |---|---|---|---|
   | 26-30 Apr | 19,356 | 20 Apr | 110,396 (69.0%) |
   | 21-25 Apr | 30,305 | 15 Apr | 105,052 (65.6%) |
   | 16-20 Apr | 5,344 | 10 Apr | 102,294 (63.9%) |
   | 11-15 Apr | 2,758 | 5 Apr | 90,387 (56.5%) |

   `dataset check` could not run: the raw files are not in the warehouse and the Kaggle download is refused (403,
   competition rules not accepted on this account). The definition's check pipeline on the shipped frame as raw input
   (`check(write_report=False)`): 0 errors, 0 warnings, 2 info (23 duplicate rows, 7 conflicting);
   README not regenerated; not rebuilt.

2. **Time basis: keep the split temporal, with no prototype, and write in `splits_comment` how the offers and their
   labels arrive?**

   * **Problem:**
     - Each shopper is predicted on the day of its offer (1 March to 30 April 2013, in waves that run over a week), the
       features are its purchases before that day, and the label, a repeat purchase of the product, arrives after a
       period the source does not state and is final for every row of the release.
     - The record carries `Samples: Over Time` and `Time: Dated` (the offer date) and no target fact (issue 3); the
       split is temporal on the offer date, so no use-case prototype applies: time moves the target (repeat rates of
       13% to 53% by week), the use case scores later offers, and the dates allow windows[^2a].
     - The definition's split comment says only that a model is refit every five days; write the arrival facts there?
   * **Background:**
     - No prototype fits: not `Timeless` (the rate moves with the offer and the week), not `Snapshot` (the brand scores
       offers it has not yet seen), not `DelayedTarget` (no shared prediction moment: every offer day is one), and not
       `StationaryRelation` (the rate moves with the wave).
     - The study flagged the purchase history as possibly running past the offer: the aggregation counts every
       transaction with offer date minus purchase date below a window's length, so a later purchase would count in
       every window. Checked on the shipped data, none does: the 0.6% of shoppers who bought the offer's brand in the
       three days before the offer repeat at 42.6%, as those of the 7- and 14-day windows (40.3%, 40.0%), where a
       purchase after the offer would make them repeat nearly always; the 1-day windows, which would hold them, are
       dropped.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | As now (implemented) | temporal on `offerdate`, no time-basis tag; the split comment names only the refit cadence | no edit | the reason for the windows and the gap (issue 1) stays in the review only |
     | B | Arrival in the split comment | as A, and the comment states the prediction point, the label's unknown period, the waves and the checked history | the next reader sees why the split is temporal and what the gap guards | none found |
     | C | A prototype in place of the windows | `DelayedTarget` with a random split | none found | no shared prediction moment; the offer waves would sit on both sides |

   * **Recommendation:** B: the windows stay as issue 1 decides them, and the comment carries the facts behind them.
     **Decision:** A, B or C?

   **Notes for the AI:** on B, no `data_tags` change (a temporal split takes no time basis). Append to `splits_comment`:
   "Arrival: each shopper is predicted on its offer day (1 March to 30 April 2013), from purchases before that day; the
   offers come in waves of a week, and the repeat label arrives after a period the source does not state, final for
   every row of the release." Add a curation note: "- Purchase history before the offer: the aggregation does not
   filter by date, but no purchase after the offer reaches the features (the 0.6% of shoppers who bought the offer's
   brand in the 3 days before it repeat at 42.6%, those of the 7 and 14 days at 40%; checked 2026-11-06 on the shipped
   rows)." If issue 1 takes b, merge the comment with the one drafted there.

   [^2a]: **SPLIT-32** (Should): how the data was collected, when each sample, feature and target come into existence,
     is information for the split; the record carries the source's collection facts, and a definition with a split
     that is not temporal names its prototype or a forced tag; a temporal split needs neither.

   **Resolved (2026-11-06, Andrej):** B, accepted through the cross-dataset item "Accept the arrival notes on temporal
   splits with one mark?" The arrival text is in a new `splits_comment`, which also repeats the window layout the
   generated text gave, and the note on the purchase history is in `curation_comments`. If issue 1 changes the windows,
   its comment is merged with this one. The split, its gap and `data_tags` are unchanged; a temporal split takes no
   time-basis tag.

3. **Correct the record's collection facts: add `Target: Later`?**

   * **Problem:**
     - The label is a repeat purchase after the offer, counted over a period that starts at the offer day and is the
       same kind of window for every shopper, so the target comes into existence after the features.
     - The record has `Samples: Over Time` and `Time: Dated` but no target fact, which the tags reserve for a target that
       exists with the features[^3a].
     - Add `Target: Later`?
   * **Background:** `Target: Varying Delay` does not fit better: nothing in the release cuts the newest labels short
     (the last week repeats at 36.8%, the $1 offers at 42.8% and 40.4% in the two newest weeks), so the delay reads as
     one window per offer, not a settlement that differs by row.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | As now (implemented) | no target fact | none found | reads as a label known with the features |
     | B | `Target: Later` | the tag added to the record's `tags` | states the label's delay, which issue 1 rests on | the window's length stays unknown |

   * **Recommendation:** B. **Decision:** A or B?

   **Notes for the AI:** on B, add `'Target: Later'` to the record's `tags`, `Andrej` to `checked_by`, a CC line.

   [^3a]: **SPLIT-32** (Should): `Target: Later` is a target that comes after the features, at one shared date or after
     a fixed window; `Target: Varying Delay` a target after a delay that differs between samples; no target tag when the
     target exists with the features.

   **Resolved (2026-11-12, Andrej):** B ("Target: Later"): `Target: Later` added to the record's `tags`; `Andrej` in `checked_by`; record CC line.

4. **Split: measure the repeat rate by offer day, then keep the 5-day gap, drop it, or lengthen it?**

   * **Problem:**
     - The record already holds the measurement: shoppers offered in the last week of April repeat at 36.8%, and $1 offers at 35% to 43% through April, highest in the newest weeks (42.8%, 40.4%), so no open repeat period shows.
     - The repeat period is not published, so the gap cannot be set from a stated delay.
     - Where a test window continues an offer wave, the five days before it add ROC AUC 0.061 (LightGBM, equal training size); the shipped 5-day gap removes them.
   * **Background:** Each shopper is scored on the offer day and two months of dated offers give the windows. The repeat purchase is known only after a period longer than a day, so the leaf has a label-delay gap whose length the data must show. Confidence of the blind walk: medium.
   * **Walk:** the questions as answered without the current split[^tree]:
     - Will the model be used at a place or group the data does not hold? (use case): no. Evidence: Use case: a consumer brand aims its offers at shoppers likely to repeat; same shops and brands. Chains and markets exist in the source, but no new chain is named as the use.
     - Fill in the covered period, or predict forward? (use case): forward. Evidence: 'when it offers a shopper a discount ... wants to know whether the shopper will become a repeat buyer': offers after the data.
     - Do the dates give the rule[^split-14]/15 windows? (data): yes. Evidence: 160,057 shoppers, offerdate on 56 days from 2013-03-01 to 2013-04-30 (dossier feature table): three windows of about a week or more, each with thousands of rows and ~27% positives, the newest two training on >= 50%.
     - What sets off a prediction? (use case): a case arrives. Evidence: Each shopper is scored when given an offer (one offer per shopper).
     - Is the target known only after a delay longer than the time step? (data): yes, late labels. Evidence: The label is a repeat purchase of the product after the offer; a repeat takes at least days, longer than offerdate's one-day step. The repeat period is not stated by the source (dossier: 'the period in which a repeat purchase counts is not stated').
   * **The measurement:** Size of the delay: repeat rate by offerdate across the two months (a drop in the last weeks shows an open repeat period and its length); if every label is final at release with a fixed horizon per offer, the rule[^split-10] still keeps the delay, unless the curator writes an exception.
   * **What each outcome gives:** measured: newest weeks as complete as older ones and a written the rule[^split-10] exception → Temporal · arrival date (no gap); otherwise → Temporal · arrival date, label-delay gap.
   * **What the blind dossier lacked, and what it changes:** none on the leaf. The definition ships four 5-day windows (11-30 April 2013) with a 5-day gap; it measured that without the gap the five newest days add ROC AUC 0.061 where a window continues an offer wave, the measurement I asked for. The repeat period stays unpublished, so the gap removes same-wave outcomes, not every open label.
   * **What changes:** nothing in the definition until the measurement is run; then the leaf it gives decides, and only a split that differs from the shipped one needs a rebuild.
   * **Source split:** yes, competition (Kaggle 2014); TabRed benchmark re-splits the train file by time: predefined files: trainHistory (offers 1 Mar-30 Apr 2013, labelled) and testHistory (unlabelled; from memory a later offer period, May-Jul 2013, with largely different offers; not verified here, the… https://www.kaggle.com/competitions/acquire-valued-shoppers-challenge/data. Credible: partly, A test file of later offers fits the brand's use (score the next offers), but the construction is not documented on a page I could read and the test labels are not public, so only the train period can be used.. Against the tree's leaf: partly, Kaggle's test file is (from memory, unverified) a later offer period, the same direction as my leaf; the construction is not documented and its labels are not public.
   * **Blindness:** what the walker saw of the shipped split before deciding: saw: split_tree.md lists this dataset as an example of 'Temporal · arrival date' (no gap).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Four expanding windows on `offerdate`, test 11-15, 16-20, 21-25 and 26-30 April 2013 (2,758 / 5,344 / 30,305 / 19,356 offers), each trained on offers up to 5 days before it (train shares 56.5 / 63.9 / 65.6 / 69.0%), 5-day gap, temporal (implemented) | No change. | Training holds no offer of the test window's own wave, worth 0.061 ROC AUC where a window continues a wave; every train side above half of the rows. | Labels of older waves are final in training although in use some may still be open (the period is unpublished). |
     | B | If the newest days are as complete as older ones and the curator writes a the rule[^split-10] exception: five 5-day windows, test 6-30 April 2013, no gap (train shares 56.5 / 63.9 / 65.6 / 69.0 / 87.9%) | `TemporalSplits` gap 5 becomes 0 and n_windows 4 becomes 5 (6-10 April tested again); `splits_comment` records the exception. | One window more and the newest trains on 87.9% of the rows (140,701); the README's current table already shows this split. | Training then holds the outcomes of the test window's own offer wave (+0.061 ROC AUC); the curator chose the gap over this on 2026-11-12. |
     | C | If the repeat rate drops in the newest days: the four windows with a gap as long as the drop (a 10-day gap trains on 41 / 56.5 / 63.9 / 65.6%) | `TemporalSplits` gap becomes the measured length in days; `splits_comment` gives the measured drop. | Training would hold only offers whose repeat period has closed, as at a refit in use. | The record's rates show no drop to size it; a 10-day gap leaves the oldest window 41% of the rows, under half. |

   * **Recommendation:** A, because the record's rates show no drop in the newest weeks and the 5-day gap already removes the same-wave outcomes.. **Decision:** A or B or C?

   **Notes for the AI:** blind walk of 2026-11-17 (split tree at cd3877cb). On B: run the named check (CPU job), write the number into the `Time basis:` line, then apply the leaf it gives.

   [^split-14]: **SPLIT-14** (Must): A temporal task has at least 3 windows.

   [^split-10]: **SPLIT-10** (Should): When a label is known only some time after its row (a delivery time, a permit's processing time, an outcome after a follow-up), a model refit at a window's start knows only the rows whose label had arrived.

   [^tree]: **SPLIT-36** (Should): walk the decision tree from the record's collection type, answering each question as if no split had been decided; a split the source prescribes is evidence, not an answer.

   **Andrej (2026-11-17, ok):** as implemented.

   **Resolved (2026-11-17, Andrej):** A, as implemented: Four expanding windows on `offerdate`, test 11-15, 16-20, 21-25 and 26-30 April 2013 (2,758 / 5,344 / 30,305 / 19,356 offers), each trained on offers up to 5 days before it (train shares 56.5 / 63.9 / 65.6 / 69.0%), 5-day gap, temporal.

5. **Split: Kaggle's trainHistory/testHistory files instead of four 5-day windows on offerdate?**

   * **Problem:**
     - Kaggle's testHistory file has no public labels, so the competition's own split cannot be scored from our data.
     - trainHistory holds the 160,057 labelled offers of 1 March to 30 April 2013; testHistory's offer period was not verified (the walk recalled May-July 2013 from memory).
     - The shipped windows follow TabReD, which re-splits trainHistory by offer date with a 5-day test window.
   * **Source split:** yes, competition (Kaggle 2014); TabRed benchmark re-splits the train file by time: predefined files: trainHistory (offers 1 Mar-30 Apr 2013, labelled) and testHistory (unlabelled; from memory a later offer period, May-Jul 2013, with largely different offers; not verified here, the… https://www.kaggle.com/competitions/acquire-valued-shoppers-challenge/data. Credible: partly, A test file of later offers fits the brand's use (score the next offers), but the construction is not documented on a page I could read and the test labels are not public, so only the train period can be used.. Against the tree's leaf: partly, Kaggle's test file is (from memory, unverified) a later offer period, the same direction as my leaf; the construction is not documented and its labels are not public.
   * **Why it counts as chosen, not conventional:** A test file of later offers fits the brand's use (score the next offers), but the construction is not documented on a page I could read and the test labels are not public, so only the train period can be used.
   * **Background:** Each shopper is scored on the offer day and two months of dated offers give the windows. The repeat purchase is known only after a period longer than a day, so the leaf has a label-delay gap whose length the data must show. Confidence of the blind walk: medium.
   * **What changes on B:** the definition's split declaration is replaced by the source's own construction (its files, periods or groups), and the `splits_comment` records that the tree's leaf was not followed. The rows, features, target and metric do not change; the folds do, so the container is rebuilt.
   * **Blindness:** what the walker saw of the shipped split before deciding: saw: split_tree.md lists this dataset as an example of 'Temporal · arrival date' (no gap).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Four expanding windows on `offerdate`, test 11-15, 16-20, 21-25 and 26-30 April 2013 (2,758 / 5,344 / 30,305 / 19,356 offers), train shares 56.5 / 63.9 / 65.6 / 69.0%, 5-day gap (implemented) | No change; `splits_comment` names Kaggle's file split as the source's and why it is not used. | Tests later offers of the labelled period, the brand's use and TabReD's construction; four test windows. | Tests only within March-April 2013, not the later offers Kaggle's test file may hold. |
     | B | Kaggle's files: train on all 160,057 trainHistory offers, test on testHistory | Not buildable: testHistory has no public labels, and the download command deletes it. | Would test a separate offer file, possibly later offers. | No labels, so nothing can be scored; its period and construction are undocumented. |

   * **Recommendation:** A, because the source's test file carries no labels and cannot be rebuilt as a scored split.. **Decision:** A or B?

   **Notes for the AI:** blind walk of 2026-11-17 (split tree at cd3877cb). On B: replace the split declaration with the source's construction (name the files or periods it uses) and say in `splits_comment` why the tree's leaf is not followed; on A: name the source's split in `splits_comment` as a departure.

   **Andrej (2026-11-17, ok):** as implemented.

   **Resolved (2026-11-17, Andrej):** A, as implemented: Four expanding windows on `offerdate`, test 11-15, 16-20, 21-25 and 26-30 April 2013 (2,758 / 5,344 / 30,305 / 19,356 offers), train shares 56.5 / 63.9 / 65.6 / 69.0%, 5-day gap.

6. **Windows: 4 of the target's 9; which layout?**

   * **Problem:**
     - Four five-day windows ship where an IID split of 160,057 offers would get nine[^split15]; the splits comment does not say why there are fewer.
     - Today's windows (5-day gap before each):

       | Test window | Train side | Train share | Test offers | Repeat buyers |
       |---|---|---|---|---|
       | 26-30 Apr 2013 | 110,396 | 69.0% | 19,356 | 6,986 |
       | 21-25 Apr 2013 | 105,052 | 65.6% | 30,305 | 11,046 |
       | 16-20 Apr 2013 | 102,294 | 63.9% | 5,344 | 1,150 |
       | 11-15 Apr 2013 | 90,387 | 56.5% | 2,758 | 819 |

     - Fixed by the use case and earlier decisions: the five-day window is TabReD's test window (the competition gives no refit cadence, so the length is assumed), and the five-day gap keeps a test window's own offer wave out of training (issue 1, b, 2026-11-12). The data hold 61 days, 1 March to 30 April 2013.
     - What stops more windows: the next window back, 6-10 April, trains on 41.4% (66,292 offers), under half[^split14]; 1-5 April would train on 25.6%, under 30%. Issue 1 dropped 6-10 April with the gap; keeping it as the curator's exception was not offered then.
     - Stable test sizes are far off: the offers come in waves, and a five-day window holds 2,758 to 30,305 offers.
   * **Window counts:** counted on the shipped frame, the declared gap kept in every layout.

     | Layout | Windows | Train share | Test offers | Repeat buyers | Window length |
     |---|---|---|---|---|---|
     | A, shipped | 4 | 56.5-69.0% | 2,758-30,305 | 819-11,046 | 5 days |
     | B, 6-10 April added | 5 | 41.4-69.0% | 2,758-30,305 | 819-11,046 | 5 days |
     | C, equal offers, half the data or more | 8 | 51.0-73.1% | 5,170-9,044 | 1,932-3,215 | 1-11 days |
     | D, equal offers, down to 30% | 9 | 30.5-73.1% | 7,099-12,906 | 2,547-4,039 | 1-11 days |
     | E, overlapping five-day windows, a new one every 2 days | 9 | 53.9-69.0% | 3,134-35,193 | 857-12,941 | 5 days |

   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Four five-day windows (implemented) | adds the reason to the splits comment | the declared length and gap; every train side above half | 4 of 9 |
     | B | Five windows, 6-10 April as the curator's exception | `n_windows=5`; the under-half warning accepted with a CC line | adds the tail of the 1 April wave (11,907 offers, 3,257 repeat buyers) | trains on 41.4%; 5 of 9 |
     | C | Eight windows of about equal offers | day ranges cut so each window holds about the same offers | test sizes within a factor of 2; no exception | windows of 1 to 11 days, not the five-day horizon; five are single days of the 22-28 April wave |
     | D | Nine windows of about equal offers, down to 30% | C, reaching back to 2 April | reaches the target | three windows under half (45.3%, 36.8%, 30.5%); windows of 1 to 11 days |
     | E | Nine overlapping five-day windows | `step=2` | keeps the length, the gap and the floor; reaches the target | an offer is scored in up to three windows, so the windows are not independent; offered only because the target cannot be reached otherwise at five days[^split15] |

   * **Recommendation:** A: the window length and the gap come from the use case and a decision, and 61 days of data cannot hold nine such windows; 6-10 April adds no period the four windows lack (another wave's tail, the same April). **Decision:** A, B, C, D or E?

   **Notes for the AI:** on A, add to `splits_comment`: "Four of the nine windows an IID split of this size would get: the data hold 61 days, and with five-day windows and the five-day gap the next window (6-10 April) would train on 41.4% of the offers." On B: `TemporalSplits(window=5, unit="days", n_windows=5, gap=5)`, accept `splits_train_under_half` naming this decision, CC line, `split` and `splits_comment`. On C or D: `_make_splits` with explicit day ranges, each trained on offers before its start minus 5 days; C: 28-30, 27, 26, 25, 24, 23, 20-22 and 9-19 April; D: 28-30, 26-27, 25, 24, 23, 18-22, 7-17, 4-6 and 2-3 April. On E: `TemporalSplits(window=5, unit="days", step=2, gap=5, min_train_fraction=0.5)`.

   **Andrej (2026-11-19, ok):** As implemented (A).

   **Resolved (2026-11-19, Andrej):** A, as implemented: four five-day windows; the next (6-10 April) would train on 41.4%. The splits comment names the target count and what stops more windows; `splits_below_target` is accepted with that reason. The split is unchanged.

   [^split14]: **SPLIT-14** (Must): every window trains on at least half the data, lower only as the curator's exception down to 30%; every test window holds at least 33 scored units.
   [^split15]: **SPLIT-15** (Must for the newest window, Should for the others): the number of windows aims at the count an IID split would get, 9 here; the window length, step and gap follow the use case and are not shortened to reach it; fewer are accepted, never under 3, with the target, the count and what stops more in the splits comment; overlapping windows only as an offered option.

## Reference

DMDave, Todd B, and Will Cukierski. Acquire Valued Shoppers Challenge. https://kaggle.com/competitions/acquire-valued-shoppers-challenge, 2014. Kaggle.
