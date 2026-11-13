---
unique_name: kick
name: kick / CAR_BAD_BUY_KICK
checked_by:
- Andrej
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
- WIP (DF)
claimed_by: Andrej
suggestion: 'Yes'
priority: 3
tags:
- Non-IID (Temporal)
- 'Samples: Over Time'
- 'Time: Dated'
- 'Target: Varying Delay'
- 'Features: Read Later'
collections:
- TabArena Reject
- TabSTAR
original_source: Kaggle
year: '2011'
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/c/DontGetKicked/overview
- https://www.openml.org/search?type=data&id=41162&sort=runs&status=active
notebook_path: datasets/beyond_iid/temporal/kick/kick.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/kick/dataset.py
source_row: 723
type_adapter_id: curation-record-v1
---

## Comments

CC: "Is from a competition, nice tabular data task. Might require temporal split or some time-invariant feature engineering; original data has more features that are interesting (like KickDate) but unclear if this makes it temporal; kickdate only in description in data. Need to check original data for more, but likely we could ignore time and group-based problems after preprocessing the original data; likely we can ignore temporal impact. No (after preprocessing)."

Old competition without clear restriction on data usage. Can assume public domain

The competition used a random split

CC (2026-10-01, Lennart): Leak audit:
- **Split:** the temporal split stays. The Kaggle train/test split was neither temporal nor grouped: both cover Jan 2009 - Dec 2010 (test is 36-44% of every quarter), and 78.9% of test rows sit at an auction location (Auction + VNZIP1) that is also in train (72 of 128 test locations). The earlier claim that the competition grouped by Auction and VNZIP1 came from a notebook check that compared train "Auction + VNZIP1" with test "VNZIP1" only (0 overlap by construction); the curation comments are corrected. A grouped split would test unseen auctions, but a model is deployed on future purchases at mostly known auctions.
- **WheelType, potential leak kept on purpose:** missing WheelType is likely blanked when a car is kicked back: missing for 24.9% of bad buys in every month vs 1.5% of good cars, erratically (Sep-Oct 2010: 1 good vs 218 bad). Dropping WheelType/WheelTypeID: LightGBM AUC on our temporal splits 0.757 -> 0.691. Kept because the company released the data this way for the competition (missing in 4.5% of Kaggle test rows vs 4.3% of train) and the recording process is not documented. Revisit if it is.
- The note above that "the competition used a random split" is closer to the truth than the old curation comment.

CC (2026-10-21, Lennart): "Reopen kick here": the LEAK-38 consistency check of WheelType against expresso's REGION drop (LEAK-10) is reopened; the open question is issue 1 of the record's Review.

**Assessment (AI, 2026-10-21):** expresso's conditional test on WheelType (training.csv, 72,983 cars): missing for 1.2-1.7% of good buys in every band of age, odometer and price, 21-39% of bad buys; a model fit on good buys from the auction-time covariates predicts 1.2% missing for bad buys, 24.9% observed (expresso: 11% vs 94%). The missing flag alone gives ROC AUC 0.617 overall, 0.60-0.63 in each shipped test window, pooled within auction 0.573, within auction and purchase date 0.572; by auction ADESA 0.734 (47.7% of bad vs 1.0% of good missing), OTHER 0.712, MANHEIM 0.522; Trim's and the MMR prices' missing flags stay at 0.49-0.54. LightGBM on the 9 shipped windows: 0.677 without WheelType/WheelTypeID, 0.750 with the flag only, 0.750 with both columns. Recommend dropping both under LEAK-10, as expresso dropped REGION; the curator has the call. Fit set to direct under the amended USE-8 (the fit_reason named only this kept leak); it stays direct if the columns are dropped. Aside: PRIMEUNIT/AUCGUART are filled from Oct 2010 mostly for good buys (Dec 2010: 51.9% of good, 12.4% of bad; the host's test file 46.0%), so their missing flag separates bad buys at 0.57-0.70 in the last months.

CC (2026-10-21, Lennart): the declared metric documents the original use case's metric; overrule it only when it is biased or wrong (evidence from the paper); keep the note of the original metric (TP-6 amended).

**Assessment (AI, 2026-10-21):** metric stays the default `roc_auc`: the competition scored the Gini index (Kaggle API: "Gini Index"), which for a binary target is a linear function of ROC AUC and ranks models the same. The notes now name the Gini. Needs a rebuild to reach the container (notes only).

CC (2026-10-21, Lennart): ok on the follow-up item: a strong kept leak does not make the fit approximate (USE-8 amended); the kept leak is named in `fit_reason` as kept, not as a gap.

**Assessment (AI, 2026-10-21):** fit stays `direct` (set earlier today); the kept missing WheelType is worth ROC AUC +0.066 (0.757 with, 0.691 without).

CC (2026-10-21, Lennart): "yes we should have one clear way to treat 0/1 flags": every 0/1 flag (a feature holding only 0 and 1, plus missing values; booleans too) is categorical (CLEAN-14, amended). Typed categorical here: IsOnlineSale.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source roc_auc — Gini index (Kaggle normalized Gini) (https://www.kaggle.com/competitions/DontGetKicked/overview/evaluation).

CC (2026-10-22, Lennart): issue 1: (a), drop `WheelType` and `WheelTypeID` under LEAK-10, consistent with expresso's REGION, and note it clearly. Issue 2: follow issue 1, so drop `PRIMEUNIT` and `AUCGUART` as well.

**Assessment (AI, 2026-10-22):** the four fields are dropped in `_clean`, with the conditional tests in the notes (WheelType: 1.2% predicted missing for bad buys, 24.9% observed; PRIMEUNIT/AUCGUART from October 2010: 42.3% predicted filled for bad buys, 7.8% observed) and why the host's test file does not keep them. LEAK-38's scope is amended (only fields whose timing cannot be tested) and a LEAK-10 mechanisms row names kick and expresso. LightGBM on the 9 windows: ROC AUC 0.750 with WheelType, 0.677 without (2026-10-21 run). REVIEW.md removed. Not built yet.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): left unordered: `Size` (a partial order).

CC (2026-11-01, Lennart): marks on the review board of PR #37: Size stays unordered (chains within body types), noted in the definition.

CC (2026-11-01, Lennart): the target rule (CLEAN-25) and the cut-end rule (CLEAN-14): the target ships as No/Yes, Yes the event (1 is the event).

**Assessment (AI, 2026-11-04):** reviewed for the BeyondArena v0.2 review page, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the record's Review. Ship after one change: drop the four MMR guide prices looked up 'as of current day' (after the outcome), which equal the purchase-time price for 23% of bad buys vs 10% of good ones and add no score. Priority 3: gap 0, use case 1, source 1, shape 1, risk -1.

CC (2026-11-10, Andrej): decided on the BeyondArena v0.2 review page; nothing is left open.

**Changes made** (the input data changed: 28 to 24 features, the same 72,983 rows; new splits):

1. **Problem:** the four MMR guide prices "as of current day" (the Manheim Market Report's auction and retail values) were looked up when the data was pulled, after every purchase and its outcome. The current auction price equals the purchase-time price for 23.0% of bad buys against 10.4% of good ones. **Change:** the four dropped; the four purchase-time prices stay; `Andrej` added to `checked_by`.
2. **Problem:** the split had no gap, although a kick (a car returned to the auction) is known only after the auction's return window, 10 calendar days in Manheim's arbitration guide. Its oldest window also trained on 48.7% of the cars. **Change:** 9 test windows of 35 days, each trained on the purchases made more than 14 days before it starts (the 10 days plus a margin). Every training side holds 52.6% or more; the test windows hold 3,028 to 4,515 cars, 33,054 in all.

## Review

**Outcome:** added. The AI recommends shipping it; both issues were resolved on 2026-11-10. Reviewed on 2026-11-04 without a
panel, from the evidence already gathered (the record, the leak audit of 2026-10-01 and the conditional tests of
2026-10-21) and two checks on the source rows; no model run exists for it. The data are Kaggle's "Don't Get
Kicked!" competition (2011, hosted by Carvana): 72,983 used cars bought at US auctions in 2009-2010, with the car,
its auction and retail price guides (MMR, the Manheim Market Report), the purchase price, the auction, the buyer and
the warranty cost; the target is whether the purchase turned out to be a bad buy ("kick", 12.3%). Validity: a real
decision (buy the car at the auction or not); `WheelType`, `WheelTypeID`, `PRIMEUNIT` and `AUCGUART`, filled in after
the outcome, are dropped (Lennart, 2026-10-22, consistently with expresso's `REGION`). The four MMR prices "as of
current day", looked up when the data was pulled, are dropped too (issue 1, 2026-11-10). The split is temporal (9 windows of 35 days with a 14-day gap since 2026-11-10; before, 9 windows of 28 purchase dates), since the
competition's own split was neither temporal nor grouped; the newest months show no shortfall of kicks (newest window
14.7% bad, December 2010 15.1%, within the 7.6% to 15.8% of earlier months), so the labels look settled. Value:
LightGBM reaches ROC AUC 0.66 to 0.68 on the 9 windows, a moderate signal; no benchmark spread is measured on this
definition. Weighed: the host's own competition and a direct decision +, the post-outcome fields found and tested +,
a modest signal and no measured spread -.

**Main points:** nothing open. The four current MMR prices were dropped (1), and the split now has 9 windows of 35 days
with a 14-day gap (2), both on 2026-11-10.

**Record judgment:** valid, ship after the change. Every point of the record is settled in the definition: the split
(2026-10-01), the four post-outcome fields (2026-10-22), the metric (the competition's Gini, which ranks models as ROC
AUC does), the 0/1 flag and the unordered `Size` (2026-11-01). The newest-month check: bad-buy rate per purchase month
from the shipped container's 72,983 rows (Slurm job 1344878), 0.076 to 0.158 by month, 0.107 to 0.152 per v0.2
window, newest window 0.147, so no sign that late kicks were still missing at the snapshot. The licence `Public
Domain` is the record's assumption for an old competition without stated terms (a note only). Nothing in the record
disagrees with the definition.

**Issues for Andrej:**

1. **Drop the four MMR prices looked up "as of current day"?**

   * **Problem:**
     - The competition's data dictionary gives four "current" guide prices (auction and retail, average and clean condition) as of the day the data was pulled, after every purchase and its outcome.
     - The current auction price equals the purchase-time price for 23.0% of the bad buys against 10.4% of the good ones, so whether it was refreshed depends on the outcome.
     - Drop the four columns, as the other fields filled in after the outcome were, or keep them?
   * **Background:** the dictionary: `MMRAcquisitionAuctionAveragePrice` "Acquisition price for this vehicle in average
     condition at time of purchase"; `MMRCurrentAuctionAveragePrice` "... as of current day" (and so the three other
     current prices). The purchase-time prices stay; they are what the buyer sees at the auction. A value looked up
     after the outcome goes when it may carry a gain, and stays with a note only when the traced part shows none[^1a].
   * **Effect on the task:** a model that compares the two prices can tell part of the bad buys by a lookup that a
     buyer at the auction does not have.
   * **Experiments:** shipped container, v0.2 columns, LightGBM on the 9 v0.2-style windows (Slurm job 1344953):
     ROC AUC 0.660 with the current prices and 0.660 without, so they add nothing a tree finds; their equality with
     the purchase-time price is the pattern (alone it would give about 0.56). The ratio of current to purchase-time
     price ranks bad buys at 0.51 overall and 0.32 to 0.65 by month.
   * **Consistency:** follows the drop of `WheelType`, `WheelTypeID`, `PRIMEUNIT` and `AUCGUART` (2026-10-22): fields
     whose recording depends on the outcome go.
   * **Unknown:** whether the equality differs by class within the same age, mileage and price band; the conditional
     test used for `WheelType` would settle it, but the drop costs no score either way.
   * **Sources:** the data dictionary (Carvana_Data_Dictionary.txt of the competition), read in a course copy:
     <https://users.phhp.ufl.edu/rlp176/Courses/PHC6089/data/Carvana_Data_Dictionary_formatted.txt>; the
     competition: <https://www.kaggle.com/competitions/DontGetKicked/data>.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep (implemented) | 28 features | the release as the host gave it | a lookup from after the outcome, refreshed less often for bad buys |
     | B | Drop the four current prices | 24 features; the four purchase-time prices stay | only what exists at the auction; consistent with the 2026-10-22 drops; no loss of score (0.660 both) | none found |

   * **Recommendation:** B: the columns are looked up after the outcome by the source's own description, their
     refresh follows the outcome, and dropping them costs nothing. **Decision:** keep (A) or drop (B)?

   **Notes for the AI:** on B, add `MMRCurrentAuctionAveragePrice`, `MMRCurrentAuctionCleanPrice`,
   `MMRCurrentRetailAveragePrice` and `MMRCurrentRetailCleanPrice` to `drop_columns` in `_clean`, add a curation note
   with the numbers above, update `known` and `fit_reason`, re-run `dataset check`, note it in the CHANGELOG and add a
   `CC (2026-11-04, Andrej):` line to the record.

   [^1a]: **LEAK-10** (Must): a feature holds only what existed at the prediction point; attributes looked up after
     the outcome go unless the data shows they did not change, and a value read at a later pull goes when it may carry
     a gain (clause amended 2026-10-26, Lennart).

   **Resolved (2026-11-10, Andrej):** B: the four `MMRCurrent*` prices are added to `drop_columns`; the four
   purchase-time prices stay. A curation note gives the numbers; `known` and `fit_reason` are updated. 24 features,
   72,983 rows; `dataset check` passes.

2. **Windows of 27 purchase dates, so that the oldest one trains on half of the cars, still with no gap?**

   * **Problem:**
     - The nine windows of 28 purchase dates keep half of the dates for training, but not half of the cars: the oldest window (13 January to 19 February 2010) trains on 35,514 of 72,983 cars (48.7%), as the early dates hold fewer purchases.
     - A kick shows up weeks or months after the purchase and the split has no gap, yet the release holds every kick: the 28 purchase dates before each window are 10.7% to 15.2% bad buys, against 11.5% to 12.3% for the older training cars.
     - Windows of 27 dates with no gap, the same with a gap of 28 dates, or as now?
   * **Background:**
     - How the data arrives: one car per row, bought on its purchase date with the car, auction, buyer, price and guide prices of that day (the four "current" prices aside, issue 1); the kick is known only after the car has been inspected, resold or returned, an undocumented delay. The record's collection facts say this (`Samples: Over Time`, `Time: Dated`, `Target: Varying Delay`), and a temporal split carries no time-basis tag[^2a].
     - Every training side needs half of the data or more[^2b]. The definition's `min_train_fraction=0.5` counts purchase dates (51.3% for the oldest window), not rows.
     - A gap is needed where the newest training labels give a shortcut or the release end is short of outcomes; no car recurs, and the buyer and auction codes are shared by many cars, as for lt_vehicle_loan_default_prediction, where no gap was kept and the notes give the effect[^2c].
   * **Experiments:** shipped container, the definition's columns without the four current prices, LightGBM (300 trees, three seeds), the nine windows as now:
     - The newest 28 training dates add ROC AUC 0.0054 at equal training size (0.6555 trained up to the window against 0.6501 with a 28-date gap and as many older cars; 7 of 9 windows higher, the largest 0.015); no gap scores 0.6562.
     - With 27-date windows the oldest window trains on 36,963 cars (50.6%), the test windows hold about 4,000 cars each, and 26 dates give 52.7%.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | 28 dates, no gap (implemented) | nine windows of 28 purchase dates, trained on every earlier car | the most test cars | the oldest window trains on 48.7% of the cars; the newest training labels were not all known at a refit |
     | B | 27 dates, no gap | `TemporalSplits(window=27, unit="unique", n_windows=9)`; the note gives the 0.0054 the newest labels add | every training side at 50.6% or more; same treatment as lt_vehicle_loan_default_prediction | 1,449 fewer test cars (36,020); the newest labels still count |
     | C | 27 dates, a gap of 28 dates | as B, the 28 dates before each window left out of training | no label unknown at a four-to-six-week refit | 0.006 lower score for a delay nobody documented; the oldest training side falls back to 46.4% |

   * **Recommendation:** B: it meets the floor by rows with the smallest change, and the measurements show no shortcut or late shortfall that a gap would remove. **Decision:** A, B or C?

   **Notes for the AI:** on B, `temporal = Temporal(on="PurchDate", splits=TemporalSplits(window=27, unit="unique", n_windows=9), horizon=27, horizon_unit="days")`, the comment above it ("9 windows of 27 purchase dates, at least half of the cars for training"); a curation note: "No gap (2026-11-06): the kick delay is not documented, but the 28 purchase dates before each window are 10.7% to 15.2% bad buys, against 11.5% to 12.3% for older training cars, so the release holds every kick; the newest 28 dates add ROC AUC 0.0054 at equal training size (LightGBM, nine windows), through codes shared by many cars (buyer, auction), as no car recurs."; `dataset check`, rebuild, report the train shares; record `CC` line. On C, add `gap=28` and the same note with the gap's reason. No time-basis tag under any option.

   [^2a]: **SPLIT-32** (Should): how the data was collected (the record's facts on samples, time and target) is information for the split; a definition names a use-case prototype only for a split that is not temporal.
   [^2b]: **SPLIT-14** (Must): a temporal task has at least 3 windows, and no window's train side holds less than 50% of the data. Case: california_house_prices_2020, moved to train on at least 50% (2026-10-21).
   [^2c]: **SPLIT-10** (Should, amended 2026-11-05): a gap is set where a measurement shows a shortcut through recent labels or a selection by the outcome at the release end; with neither, no gap, and the notes give what the newest labels add at equal training size. **SPLIT-9** (Must), case lt_vehicle_loan_default_prediction: recent default rates of shared codes, no borrower recurring, are not a shortcut (2026-11-05, Lennart).

   **Andrej (2026-11-10, discuss):** Why no gap? We can do splits such that train is more than 50% everywhere but also
   keep the gap that would be reasonable in practice while also keeping sufficient test sizes. How can we achieve this?

   **Answer (AI, 2026-11-10):** a gap of 4 weeks with test windows of 5 weeks fits: 9 windows, every training side 50.5%
   or more, at least 3,028 test cars each.

   * **The gap the use case implies:** the data dictionary defines a kick by `KickDate`, "Date the vehicle was kicked
     back to the auction", a column the release does not include. So a kick is a return through the auction's
     arbitration, which runs days after the sale; Manheim's current guide gives 10 calendar days[^2d] for digital sales.
     Title problems and the time to record the return add some time. Four weeks covers that with margin.
   * **The data agrees that kicks arrive fast:** the newest weeks show no shortfall of bad buys, as late kicks would
     make them look clean.

     | Purchases in the release's last | Cars | Bad buys |
     |---|---|---|
     | 2 weeks | 502 | 18.7% |
     | 4 weeks | 2,233 | 15.8% |
     | 13 weeks | 10,463 | 12.2% |
     | All | 72,983 | 12.3% |

   * **How it fits:** windows in calendar weeks, a gap in weeks, and `min_train_fraction=0.5`, which counts rows for a
     calendar unit. The windows walk back until the next one would train on less than half of the cars. Measured with
     the definition's own splitter on the 72,983 cars:

     | Setting | Windows | Training share (oldest to newest) | Test cars per window | Test cars in all |
     |---|---|---|---|---|
     | Now: 28 purchase dates, no gap | 9 | 48.7% to 94.9% | 3,605 to 5,164 | 37,469 |
     | 4 weeks, gap 4 weeks | 11 | 51.7% to 91.9% | 2,233 to 3,759 | 32,200 |
     | 5 weeks, gap 4 weeks | 9 | 50.5% to 90.8% | 3,028 to 4,515 | 33,054 |
     | 6 weeks, gap 6 weeks | 7 | 51.7% to 86.8% | 3,922 to 5,716 | 30,775 |

   * **Cost:** the earlier run (issue text) put the gap's cost at ROC AUC 0.006 for a 28-date gap, against 0.0054 that
     the newest labels add at equal training size.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | As now (implemented) | 9 windows of 28 dates, no gap | most test cars | the oldest window trains on 48.7%; the newest labels were not all known at a refit |
     | b | 5 weeks, gap 4 weeks | `TemporalSplits(window=5, unit="weeks", n_windows=9, gap=4, min_train_fraction=0.5)` | the practical gap; every training side 50.5% or more; 9 windows of 3,028+ cars | 4,415 fewer test cars; about 0.006 lower ROC AUC |
     | c | 4 weeks, gap 4 weeks | the same with `window=4`, 11 windows | the refit cadence equals the gap | smallest windows (2,233 cars) |
     | d | 6 weeks, gap 6 weeks | `window=6, gap=6`, 7 windows | the most margin on the delay | 7 windows, fewest test cars |

   * **Recommendation:** b. It keeps the 9 windows, sets a gap longer than the auctions' return windows and meets the
     floor of half. In `dataset.py`: `temporal = Temporal(on="PurchDate", splits=TemporalSplits(window=5, unit="weeks",
     n_windows=9, gap=4, min_train_fraction=0.5))`. The `horizon=28` line goes, since a fixed window states the horizon.
     **Decision:** a, b, c or d?

   [^2d]: Data dictionary: `Carvana_Data_Dictionary.txt` of <https://www.kaggle.com/competitions/DontGetKicked/data>.
   Manheim Buyer Arbitration Guide: <https://site.manheim.com/?p=34981>.

   **Andrej (2026-11-10, discuss):** Since we have 10 days as a real reference, we can use 14 days to cover the margin
   while not being too conservative. 14days is more realistic and closer to the information we have.

   **Resolved (2026-11-10, Andrej):** a 14-day gap with 9 test windows of 35 days, from the definition's own splitter:
   `TemporalSplits(window=35, unit="days", n_windows=9, gap=14, min_train_fraction=0.5)`, with `horizon=28` removed. The
   gap is the auction's 10-day return window plus a margin. `splits_comment`, the task summary's split text and
   `changes` are updated; `dataset check` passes. The 35-day window keeps the 9 windows and every training side above
   half.

   | Setting (gap 14 days) | Windows | Oldest training share | Test cars per window | Test cars in all |
   |---|---|---|---|---|
   | Before: 28 purchase dates, no gap | 9 | 48.7% | 3,605 to 5,164 | 37,469 |
   | 4-week windows | 11 | 53.6% | 2,233 to 3,759 | 32,200 |
   | 5-week windows (applied) | 9 | 52.6% | 3,028 to 4,515 | 33,054 |
   | 6-week windows | 7 | 55.9% | 3,922 to 5,716 | 30,775 |
   | 8-week windows | 5 | 57.8% | 5,224 to 6,903 | 29,274 |

## Reference

faysal, Will Adams, and Will Cukierski. Don't Get Kicked!. https://kaggle.com/competitions/DontGetKicked, 2011. Kaggle.
