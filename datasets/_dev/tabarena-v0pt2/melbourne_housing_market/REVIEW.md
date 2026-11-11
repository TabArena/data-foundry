# melbourne_housing_market

**Outcome:** added. Under the rule on choosing test windows, rewritten on 2026-11-10, the AI recommends keeping the
nine windows of three weekly result sheets, 12 August 2017 to 17 March 2018 (issue 10): they cover every eligible
window but one, 15-29 July 2017, a second winter window whose train side holds only six sheets of the full file's
suburbs. `dataset.py` is unchanged until you decide.

**Main points:** Keep the nine windows, or add the tenth eligible one, 15-29 July 2017 (issue 10)? Sign off the
horizon of three weekly sheets without a gap.

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
