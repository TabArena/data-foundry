---
unique_name: melbourne_housing_market
name: Melbourne Housing Market
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
suggestion: 'Yes'
priority: 2
decision_markers:
- Needs extensive data wrangling
tags:
- Non-IID (Temporal)
collections:
- New (BeyondArena)
original_source: Kaggle
year: '2017'
required_split:
- Temporal (NON-IID)
problem_type: Regression
source_links:
- https://www.kaggle.com/datasets/anthonypino/melbourne-housing-market
- https://www.kaggle.com/datasets/dansbecker/melbourne-housing-snapshot
v2_path: datasets/_dev/tabarena-v0pt2/melbourne_housing_market/dataset.py
source_row: 726
type_adapter_id: curation-record-v1
---

## Comments

Similar to GOV data, no predictive task connected so far.

Unclear which version to use, scraped data in many cases.

Otherwise okay and another price prediction task for some cases.

**Assessment (AI, 2026-10-07):** Valid as a sale-price regression over Domain.com.au's weekly auction sheets, split by time. Version: Melbourne_housing_FULL.csv (Jan 2016 to Mar 2018): its realestate.com.au attributes lower RMSE in log price from 0.211 (the LESS file's columns) to 0.183. These were looked up after the sale, but close to it from late 2016 on: `Bedroom2` matches the sheet's bedroom count in 98.9-100% of each test window, against 85.2% for the Apr-Sep 2016 sales looked up in April 2017. Only S/SP/SA prices are sales; PI and VB prices are bids (4.3% and 6.6% below a sale-price model), dropped. dansbecker/melbourne-housing-snapshot (record melbourne_housing_snapshot) is a September 2017 subset of the full file. The Airbnb links belong to record melbourne_airbnb_open_data.

Related work, not a source: Melbourne Airbnb listings (https://www.kaggle.com/datasets/tylerx/melbourne-airbnb-open-data, from Inside Airbnb, https://insideairbnb.com/).

**Assessment (AI, 2026-10-20):** priority 3 for the review of the added dataset: gap -, use case -, source +, shape +, no known risk. Sizeable temporal, spatial house-price regression with mixed features; useful but adds to an already well-covered house-price domain.

**Assessment (AI, 2026-10-20):** review panel (full tier): ship after changes. Sale-price regression of the Melbourne properties that sell, predicted before the auction (USE-3 wording fixed in the definition); 21,266 sales, 9 windows of three weekly sheets. Passed-in and vendor-bid prices are bids (-4.1% and -6.5% against a sale model, sales +0.3%), so only sales stay (USE-5, LEAK-22 hold). LightGBM skill 0.840 over the dummy on 5 of 5 probed splits, best single feature 0.426. Known risk: post-sale lookup of six attributes, measured small: Bedroom2 equals the sheet's Rooms in 98.9-100% of each test window (85.2% in Apr-Sep 2016), the September 2017 snapshot fixes all six for the 2,728 test rows up to 23 Sep 2017, the other five have no pre-sale reference, and blanking the 495 mismatched 2016 sales moves the RMSE by -0.0005 to +0.0003 over 3 seeds, inside the run-to-run spread of 0.0007; the coordinates come from the same lookup. Kept under a `Potential leak, kept on purpose:` note; the panel recommends fit `approximate` like house_sales, the curator decides (REVIEW issue 3); year 2018 under PROV-9's growing-source clause (issue 9). Repairs: 86 impossible BuildingArea values set missing, one Distance per suburb, two suburb lookups filled. Priority 2: gap -, use case -, source +, shape +, risk - (no thin domain, problem type or regime; the use case is the curation's, not the source's, and the fit is in question; documented Kaggle scrape with a data card; the post-sale lookup is an open leak issue).

CC (2026-10-21, Lennart): Blank the attributes looked up after the sale for the rows before the lookup (the smallest fix, LEAK-7), rather than keep them because removing them changes no score; stay with direct fit; measure the newest months for a recording shortfall and take a gap only if it shows selection.

**Assessment (AI, 2026-10-21):** The uploader looked the six attributes up for all sales up to the sheet of 8 April 2017 at once, by 10 April 2017 (Kaggle thread 30748), up to 15 months after the sale; later sales were looked up by weekly runs. The six attributes of these 7,578 sales (6,065 had them) are now blank, so missingness follows the date. Bedroom2 equals Rooms in 84-88% of each month of April-September 2016 and 99.2-100% of each month from November 2016. Cost: RMSE +0.0011 to +0.0016 over 3 seeds (0.1813 to 0.1826, 6-7 of 9 windows worse). Fit stays `direct`. Recording shortfall: every weekly sheet of the full file from August 2017 to 17 March 2018 holds as many sales as the same sheet of the companion file read up to October 2018 (558 of 558 on 17 March 2018); March 2018 holds 1,121 sales in three sheets against 1,174 in the same sheets of 2017; the newest window's mean residual is +0.009 against -0.013 to +0.022 in the others. No shortfall, no gap. Dataset check: 0 errors, 0 warnings.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback rmse — Kaggle dataset without a task or metric; regression fallback rmse (on the log target, close to RMSLE).

**Assessment (AI, 2026-10-21):** metric now `Metric.from_context("rmsle", target_transform="log")` instead of the fallback rmse on the log target: a sale price's error matters relative to the price; the target still ships as log, and RMSLE is computed after the inverse, on the original scale (MET-3). Needs a rebuild to reach the container.

CC (2026-10-21, Lennart): ship the target on the modelling scale, score on the original scale (target_transform).

CC (2026-10-22, Lennart): verdict ship. Issue 9: use 2017.

**Assessment (AI, 2026-10-22):** `year` is 2017, the Kaggle upload's first version; PROV-9 now says a Kaggle upload that grew over its versions is one publication and takes its first version's year (the growing-source clause covers registers and archives we snapshot). The BibTeX keeps the version we use (2018). REVIEW.md removed (nothing left open). Not built yet.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `nsw_property_sales` (TBD -> Yes, priority 2). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-11, Lennart): REVIEW issue 10 (keep the nine windows or add July 2017), as implemented (A): the nine windows of three weekly sheets, 12 August 2017 to 17 March 2018, stay; 15-29 July 2017 is not added. The windows walk back from the newest because nine is the count of splits an IID task of this size gets and, further back, the train sides hold mostly the inner-suburbs-only file before 27 May 2017.

CC (2026-11-11, Lennart): the declared horizon (three weekly sheets, no gap, windows starting 2018-03-03, 2018-02-10, 2018-01-20, 2017-11-25, 2017-11-04, 2017-10-14, 2017-09-23, 2017-09-03 and 2017-08-12) is checked, as a Melbourne auction campaign runs about four weeks, so a price estimated during it looks one to four sheets ahead, and three sheets give nine windows that each train on at least 55.3% of the sales.

**Assessment (AI, 2026-11-11):** applied in dataset.py: `temporal` unchanged (`window=3, unit="unique", n_windows=9, min_train_fraction=0.5`); test 1,119, 1,069, 93, 1,526, 1,033, 1,550, 868, 1,140 and 1,115 sales, train 20,147, 19,078, 18,985, 17,459, 16,426, 14,876, 14,008, 12,868 and 11,753 (94.7% to 55.3% of 21,266). The sales before 27 May 2017 (8,616, 40.5% of the rows) make up 79.2% of the train side of the tenth window (15-29 July 2017, 51.2%) and all of it from the window of 27 May to 17 June 2017 on (40.5%); the windows from 6-20 May 2017 back test the inner suburbs only, and three-sheet windows reach 30% of the rows back to 4-18 March 2017 (31.1%). `splits_comment` gives the campaign (Nelson Alexander) as the length's reason and these two reasons for walking back, without the "eight months of eligible history" of the issue's notes; `task_summary.split` and the decision table on the window length name the campaign. The issue's sentence that no dataset tests more windows than the IID folds is false: rain_in_australia tests 26 windows against 9 IID folds. `dataset check`: 0 errors, 0 warnings (README not regenerated).

## Review

**Outcome:** added. On 2026-11-11 you kept the nine windows of three weekly result sheets, 12 August 2017 to
17 March 2018, without a gap (issue 10 and the horizon, A); the splits comment now gives the four-week auction
campaign as the length's reason and the count of nine and the inner-suburbs-only file before 27 May 2017 as the
reasons for walking back from the newest.

**Main points:** Settled on 2026-11-11: the nine windows of three sheets stay (issue 10, A), and the declared
horizon of three weekly sheets without a gap is checked.

**Horizon:**

* **Verdict:** keep the windows of three weekly sheets without a gap (medium confidence): a Melbourne auction campaign
  runs about four weeks, so a price estimated during the campaign looks one to four sheets ahead, and three sheets keep
  nine windows above the floor.
* **Length:** declared three auction dates (`unit="unique"`, one weekly sheet each), stated as a three-week horizon;
  up to 7 calendar weeks where sheets are missing (10 June, 5 August and 2 December 2017, 13 January 2018) or over
  the holiday break (no sheet from 16 December 2017 to 20 January 2018). The Kaggle upload
  (https://www.kaggle.com/datasets/anthonypino/melbourne-housing-market) names no task or horizon: none found on the
  data card or in the forum threads the definition cites. A real campaign: "Before the auction takes place, there is
  a sales campaign that runs for approximately four weeks" (Nelson Alexander, a Melbourne agency,
  https://www.nelsonalexander.com.au/news/auction-private-sale-and-expressions-interest-explained). The three sheets
  were chosen for the window count, not from a source: four sheets leave two of nine windows below half the rows for
  training.
* **Gap:** none, measured: a price appears in the sheet of its auction week, and every sheet from August 2017 to
  17 March 2018 holds as many sales as the same sheet read up to October 2018 (558 of 558 on 17 March 2018); your
  call of 2026-10-21.
* **Time frame:** sales from January 2016 to 17 March 2018; before 27 May 2017 the file holds only the inner suburbs.
  Windows of three sheets keep half the sales for training from 15 July 2017 (51.2%): ten windows within eight
  months, so no other year can be tested. The January lull leaves one window of 93 sales (20 January to 3 February
  2018).
* **Options:**

  | | Option | What it does | Test windows | Pro | Con |
  |---|---|---|---|---|---|
  | A | Three weekly sheets, no gap (implemented) | windows of three auction dates, up to 7 calendar weeks where sheets are missing or over the holiday break; ten keep half the sales for training, from 15 July 2017 (51.2%) | 9 windows of 93 to 1,550 sales | within the campaign of about four weeks, so a price estimated during it looks one to four sheets ahead; room for the nine windows an IID task of this size gets | chosen for the window count, not from a source; the January lull leaves one window of 93 sales |
  | B | Four weekly sheets | the campaign's length: 7 windows above the floor, training on 53.8% to 92.2%, 620 to 1,717 sales each; the January lull joins a window with December | 7 candidates above the floor, 620 to 1,717 sales each | closer to the campaign; no window as small as 93 sales | 7 windows, two fewer than nine |
  | C | One calendar month | monthly windows | 8 candidates above the floor, 18 to 1,930 sales each | a fixed calendar length, where three sheets span up to 7 calendar weeks | January 2018 would hold 18 sales (the definition's decision table), too few for a window |

* **Recommendation:** A: three sheets stay within the four-week campaign and leave room for nine windows above the
  floor, where four sheets leave seven. **Decision:** A, B or C?

**Lennart (2026-11-11, ok):** As implemented (A).

**Resolved (2026-11-11, Lennart):** A, three weekly sheets without a gap, kept: a Melbourne auction campaign runs
about four weeks, so a price estimated during it looks one to four sheets ahead, and three sheets give nine windows
that each train on at least 55.3% of the sales; the Kaggle upload names no task or horizon. `splits_comment` now gives
the campaign as the length's reason, with its source, `task_summary.split` names the campaign and the 55% to 95% train
sides, and the decision table "Test windows of three weekly sheets" leads with the campaign. The no-gap call of
2026-10-21 stays as measured. `temporal` is unchanged. The record has the horizon CC line. `dataset check`: 0 errors,
0 warnings (README not regenerated).

**Issues for Lennart:**

10. **Keep the nine windows, or add the tenth eligible one, July 2017?**

   * **Problem:**
     - The nine windows are the newest nine of three weekly sheets (12 August 2017 to 17 March 2018), and one more
       window keeps half the sales for training: 15 to 29 July 2017, at 51.2%.
     - Since 2026-11-10 the newest window always stays and the others are chosen from the use case and statistics of
       the data, preferring other years and seasons[^mhm-split15].
     - The eligible history is eight months, so no other year can be tested, and today's windows already span winter,
       the spring auction season, the summer lull and early autumn.
   * **Background:** The July window is a second winter window after 12-26 August. Its prices are low (mean log price
     13.56 against 13.73 on its train side), and its train side holds only six sheets of the full file's suburbs
     (27 May to 8 July 2017). PSI, the population stability index, compares a feature's distribution in the window
     with its train side (above 0.25 is usually read as a large shift): the scraped attributes (bedrooms, bathrooms,
     car spaces) drift most in the oldest windows (1.58 to 2.25), as their train sides hold more of the sales before
     April 2017, whose attributes are blank. 2.3% of the July window's sales have a category its train side never
     shows. Ten windows would be one more than the nine folds an IID task of this size gets.
   * **Statistics:** from the candidate table (all rows; the target is the natural log of the price).

     | Sheets | In | Sales | Mean log price, test | Train side | Train share | Largest PSI | Unseen category |
     |---|---|---|---|---|---|---|---|
     | 3-17 Mar 2018 | A, B | 1,119 | 13.71 | 13.71 | 94.7% | 0.57 `Landsize` | 0.45% |
     | 10-24 Feb 2018 | A, B | 1,069 | 13.65 | 13.71 | 89.7% | 0.33 `Landsize` | 0.56% |
     | 20 Jan-3 Feb 2018 | A, B | 93 | 13.46 | 13.71 | 89.3% | 2.48 `Agent` | 2.15% |
     | 25 Nov-16 Dec 2017 | A, B | 1,526 | 13.64 | 13.72 | 82.1% | 0.31 `Latitude` | 0.66% |
     | 4-18 Nov 2017 | A, B | 1,033 | 13.68 | 13.72 | 77.2% | 0.53 `Longitude` | 0.58% |
     | 14-28 Oct 2017 | A, B | 1,550 | 13.74 | 13.72 | 70.0% | 0.55 `Bedroom2` | 0.58% |
     | 23 Sep-7 Oct 2017 | A, B | 868 | 13.60 | 13.72 | 65.9% | 0.85 `Bedroom2` | 0.92% |
     | 3-16 Sep 2017 | A, B | 1,140 | 13.73 | 13.72 | 60.5% | 1.58 `Bedroom2` | 1.05% |
     | 12-26 Aug 2017 | A, B | 1,115 | 13.74 | 13.72 | 55.3% | 1.77 `Bedroom2` | 0.72% |
     | 15-29 Jul 2017 | B | 873 | 13.56 | 13.73 | 51.2% | 2.25 `Car` | 2.29% |

   * **Effect on the task:** B adds a tenth score from a winter window whose model has seen six weeks of the outer
     suburbs, with the lowest prices after the January lull and the largest share of sales with an unseen category
     (2.3%); A ranks the models on the nine windows that cover the rest of the eligible period.
   * **Consistency:** the three-sheet windows and the measured no-gap call date from 2026-10-21, when each
     house-price dataset kept its own horizon[^mhm-split12]; no dataset tests more windows than the folds an IID task
     of its size would get.
   * **Sources:** the definition `datasets/_dev/tabarena-v0pt2/melbourne_housing_market/dataset.py` (`temporal`,
     `splits_comment`, the decision table "Test windows of three weekly sheets"); the record
     `curation/records/melbourne_housing_market.md` (CC 2026-10-21); the candidate tables `.venv/bin/python -m
     data_foundry.curation.cli dataset windows melbourne_housing_market --root datasets/_dev/tabarena-v0pt2` (13
     windows: the tool counts sheets for the floor, and by rows 10 keep half the sales for training) and the same
     with `--window 4` (four sheets).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Nine windows (implemented) | tests the nine windows of three sheets from 12 Aug 2017 to 17 Mar 2018 | every season the eligible period holds; the number of folds an IID task of this size gets; each train side at least 55.3% | July 2017 untested |
     | B | Ten windows | adds 15-29 Jul 2017 as a tenth window | every eligible window tested | a second winter window; its train side holds six sheets of the outer suburbs and 51.2% of the sales; one window more than the IID count |

   * **Recommendation:** A: the nine windows already cover every season of the eligible period, and the tenth adds a
     second winter window on the thinnest train side. **Decision:** A or B?

   **Notes for the AI:** on A, add to `splits_comment` why the windows walk back from the newest: the eligible
   history is eight months (from 15 July 2017 at 51.2%), and the nine windows cover all of it but July 2017, across
   winter, spring, the summer lull and early autumn; a CC line in the record and a dated CHANGELOG entry (SPLIT-15).
   On B, `temporal = Temporal(on="Date", splits=TemporalSplits(window=3, unit="unique", cutoffs=("2018-03-03",
   "2018-02-10", "2018-01-20", "2017-11-25", "2017-11-04", "2017-10-14", "2017-09-23", "2017-09-03", "2017-08-12",
   "2017-07-15")), horizon=3, horizon_unit="weeks")`: built with `TemporalSplits.splits` on the definition's frame
   (21,266 sales), test 1,119, 1,069, 93, 1,526, 1,033, 1,550, 868, 1,140, 1,115 and 873 sales, train 20,147, 19,078,
   18,985, 17,459, 16,426, 14,876, 14,008, 12,868, 11,753 and 10,880 (94.7% to 51.2%); then rewrite
   `task_summary.split` ("Nine test windows ... from August 2017"), `splits_comment` (10 windows, 51% to 95% of the
   rows), the comment above `temporal`, a CC line, a CHANGELOG entry and `dataset check`.

   [^mhm-split15]: **SPLIT-15** (Must for the newest window, Should for the others; amended 2026-11-10, Lennart and
     Andrej): "The newest window is always a test window ... Prefer windows in other years, then other seasons, then
     other months, weeks or days, over the windows just before the newest. Walking back from the newest is one choice
     among others and needs its reason too, such as a history too short for others ... as many windows as an IID or
     grouped task of that size would get folds."
   [^mhm-split12]: **SPLIT-12** (Should), case house_sales, perth_house_prices, ames_housing, zillow_prize,
     melbourne_housing_market: "no window length for the whole family: each keeps the horizon of its own source or
     refit cadence (three weeks; one month, spaced; two months; one month after a one-month gap; three weekly
     sheets)" (2026-10-21, Lennart).

   **Lennart (2026-11-11, ok):** As implemented (A).

   **Resolved (2026-11-11, Lennart):** A, as implemented: the nine windows of three sheets, 12 August 2017 to 17 March
   2018, stay (test 1,119, 1,069, 93, 1,526, 1,033, 1,550, 868, 1,140 and 1,115 sales; train 20,147 down to 11,753,
   94.7% to 55.3%, none under half). `splits_comment` now says why they walk back from the newest: nine is the count of
   splits an IID task of this size gets, and further back the train sides hold mostly the sales before 27 May 2017,
   when the file holds only the inner suburbs (79.2% of the tenth window's train side, all of it from the window of
   27 May 2017 on), while a window before 27 May 2017 tests the inner suburbs only. It does not say that the eligible
   history is eight months: since the amendment of SPLIT-14 of 2026-11-11 a window may train on down to 30%, which
   reaches back to March 2017 (31.1%). A correction to the issue: the sentence "no dataset tests more windows than the
   folds an IID task of its size would get" is false, as rain_in_australia tests 26 two-week windows where an IID task
   of its 264,562 rows gets nine folds. `temporal` is unchanged. The record has the decision and the horizon CC lines.
   `dataset check`: 0 errors, 0 warnings (README not regenerated).
