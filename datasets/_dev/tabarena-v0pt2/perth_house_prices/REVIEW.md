# perth_house_prices

**Outcome:** added. Under the rule on choosing test windows, rewritten on 2026-11-10, the AI recommends keeping the
nine one-month windows every third month from December 2018 to December 2020 that you chose on 2026-10-26 (issue
15): they already span three years and all four seasons and stay out of April and May 2020, the COVID months with the
fewest sales. One fix is due under either answer: a bullet of `curation_comments` still names the old windows
(April to December 2020). `dataset.py` is unchanged until you decide.

**Main points:** Keep the windows every third month from December 2018, or spread them every fourth month back to
April 2018 (issue 15)? Sign off the one-month horizon without a gap.

**Horizon:**

* **Verdict:** keep the one-month windows without a gap (medium confidence): the source dates sales by month, so a month
  is the shortest window the data allow, and Australia's main valuation service reports on its model monthly.
* **Length:** declared one calendar month. The source, a Kaggle scrape of house.speakingsame.com
  (https://www.kaggle.com/datasets/syuzai/perth-house-prices), names no task or horizon: none found on the data card
  or in its discussion. The monthly refit is our use case and the house-price family's convention (zillow_prize's
  one-month windows), and the data allow nothing shorter, since `DATE_SOLD` holds only the month. Cotality, the main
  Australian valuation provider, offers "dynamic, real-time estimates" with "monthly model performance and accuracy
  reporting" (https://www.cotality.com/au/products/avm): its estimates move continuously and its accuracy is
  checked each month, so a monthly refit is the slow end of practice.
* **Gap:** none: sales are dated by month, longer than the delay before a sale reaches the site, and December 2020,
  present early at 0.71 of November's count, shows no price selection (mean residual +0.017 against +0.003 to +0.025
  in July to November); your call of 2026-10-26, an application of the amended rule on late labels since 2026-11-04.
* **Time frame:** sales from April 1988 to December 2020, thin before 2013 (each property's latest sale only). 36
  one-month windows keep half the sales for training, January 2018 to December 2020 (51.1% to 98.8%); 12 of them lie
  on the every-third-month grid, back to March 2018. April and May 2020 hold 316 and 284 sales, the fewest of the
  eligible months; December 2020 is short.
* **Options:**

  | | Option | What it does | Pro | Con |
  |---|---|---|---|---|
  | A | One month, no gap (implemented) | one-month windows: 36 candidates above the floor, January 2018 to December 2020 (51.1% to 98.8%), 12 of them on the every-third-month grid | the shortest window the month-dated sales allow; the house-price family's convention (zillow_prize's one-month windows); Cotality checks its model's accuracy monthly | our use case, not a source's; the slow end of practice, as Cotality's estimates move continuously; April and May 2020 hold only 316 and 284 sales |
  | B | Three months | a quarterly refit: 12 windows above the floor, from January 2018; 974 to 1,619 sales in the newest nine | larger windows | a slower refit than a valuation service runs; no source |
  | C | Two months | 18 windows above the floor; the newest nine, back to July 2019, hold 658 to 1,197 sales each | larger windows than one month | no source; the newest nine fall in 2019 and 2020 only |

* **Recommendation:** A: a month is the shortest window the month-dated sales allow, and it matches the monthly accuracy
  checks of Australia's main valuation service and the family's one-month windows. **Decision:** A, B or C?

**Issues for Lennart:**

15. **Keep the windows every third month, or spread them every fourth month back to April 2018?**

   * **Problem:**
     - The nine windows are every third month from December 2018 to December 2020, as you chose on 2026-10-26 to keep
       most of them out of the COVID months and the period of stale records.
     - Since 2026-11-10 the newest window always stays and the others are chosen from the use case and statistics of
       the data, preferring other years, then other seasons, over the windows just before the newest[^php-split15].
     - One-month windows keep half the sales for training back to January 2018, and that oldest open year holds one
       of today's nine windows.
   * **Background:** A takes the last month of each quarter (March, June, September, December), so it covers Perth's
     four seasons, once in 2018 and four times each in 2019 and 2020. B takes every fourth month back from December
     2020 (April, August, December), three windows in each of 2018, 2019 and 2020, but no spring month, and it tests
     April 2020. The windows differ little in price (mean log price 13.17 to 13.30 against 13.25 to 13.26 on the train
     sides) or in drift: PSI, the population stability index, compares a feature's distribution in the window with
     its train side (above 0.25 is usually read as a large shift), and its largest value is 0.42 to 0.75 in every
     month, always on a location code (postcode, suburb, nearest school or station) as sales move between suburbs.
     At most 3.6% of a window's sales have a suburb, school or station its train side never shows.
   * **Statistics:** from the candidate table at a step of one month (all rows).

     | Month | In | Sales | Mean log price, test | Train side | Train share | Largest PSI | Unseen category |
     |---|---|---|---|---|---|---|---|
     | Dec 2020 | A, B | 412 | 13.17 | 13.25 | 98.8% | 0.61 postcode | 0% |
     | Sep 2020 | A | 569 | 13.21 | 13.25 | 93.4% | 0.42 suburb | 0% |
     | Aug 2020 | B | 483 | 13.22 | 13.25 | 91.9% | 0.46 postcode | 0% |
     | Jun 2020 | A | 374 | 13.17 | 13.25 | 89.3% | 0.52 postcode | 0% |
     | Apr 2020 | B | 316 | 13.20 | 13.26 | 87.5% | 0.75 postcode | 0% |
     | Mar 2020 | A | 387 | 13.26 | 13.26 | 86.3% | 0.54 postcode | 0.26% |
     | Dec 2019 | A, B | 367 | 13.30 | 13.25 | 83.0% | 0.62 school | 0% |
     | Sep 2019 | A | 416 | 13.20 | 13.25 | 78.9% | 0.64 suburb | 3.61% |
     | Aug 2019 | B | 458 | 13.18 | 13.26 | 77.5% | 0.56 suburb | 0.44% |
     | Jun 2019 | A | 475 | 13.20 | 13.26 | 74.5% | 0.55 school | 1.05% |
     | Apr 2019 | B | 421 | 13.27 | 13.26 | 71.9% | 0.52 suburb | 0.95% |
     | Mar 2019 | A | 434 | 13.21 | 13.26 | 70.5% | 0.70 suburb | 0% |
     | Dec 2018 | A, B | 479 | 13.28 | 13.26 | 66.7% | 0.64 suburb | 0.42% |
     | Aug 2018 | B | 478 | 13.25 | 13.26 | 60.7% | 0.55 school | 2.09% |
     | Apr 2018 | B | 456 | 13.23 | 13.26 | 55.1% | 0.64 postcode | 3.51% |

   * **Effect on the task:** Both test a monthly refit in three calendar years. A weighs 2019 and 2020 and covers
     every season, with June, September and December of the COVID year; B weighs the three years alike but repeats
     three calendar months and tests April 2020, the first COVID month and the second smallest of the eligible ones.
   * **Consistency:** you chose A on 2026-10-26 over nine contiguous months of 2020, from counts, not
     scores[^php-split20]; B would depart from that call only to test 2018 more often, which the rewritten rule's
     first preference (other years) supports, while A's spread over the seasons serves its second.
   * **Sources:** the definition `datasets/_dev/tabarena-v0pt2/perth_house_prices/dataset.py` (`temporal`,
     `splits_comment`, `curation_comments`); the record `curation/records/perth_house_prices.md` (CC 2026-10-26,
     issue 6: "Do (a)"); the candidate tables `.venv/bin/python -m data_foundry.curation.cli dataset windows
     perth_house_prices --root datasets/_dev/tabarena-v0pt2` (12 windows every third month) and the same with
     `--step 1` (36 monthly windows).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Every third month (implemented) | tests Dec, Sep, Jun and Mar of 2020 and 2019, and Dec 2018 | all four seasons; three years; April and May 2020 left out; your call of 2026-10-26; the oldest trains on 66.7% | one window in 2018; December three times |
     | B | Every fourth month | tests Dec, Aug and Apr of 2020, 2019 and 2018 | three windows in each eligible year; spread over all 36 eligible months | no spring month; tests April 2020; the oldest trains on 55.1% |

   * **Recommendation:** A: it already spreads over three years and every season, the two things the rule asks for
     first, and keeps the reason you gave on 2026-10-26; B adds 2018 windows at the cost of a season and a COVID
     month. **Decision:** A or B?

   **Notes for the AI:** under either option, the bullet "Temporal split on `DATE_SOLD`: 9 monthly test windows, April
   to December 2020 (splits comment)" in `curation_comments` is stale since 2026-10-26: replace it with the windows
   decided. On A, add the reason under the rewritten rule to `splits_comment` (the windows span 2018 to 2020 and the
   four seasons; 36 one-month candidates keep half the sales, from January 2018), a CC line in the record and a dated
   CHANGELOG entry (SPLIT-15). On B, `temporal = Temporal(on="DATE_SOLD", splits=TemporalSplits(window=1,
   unit="months", cutoffs=("2020-12-01", "2020-08-01", "2020-04-01", "2019-12-01", "2019-08-01", "2019-04-01",
   "2018-12-01", "2018-08-01", "2018-04-01")))`: built with `TemporalSplits.splits` on the definition's frame (33,090
   sales), test 412, 483, 316, 367, 458, 421, 479, 478 and 456 sales, train 32,678, 30,419, 28,958, 27,462, 25,660,
   23,776, 22,065, 20,075 and 18,241 (98.8% to 55.1%); then rewrite `task_summary.split` ("every third month from
   December 2018 to December 2020"), `splits_comment` and the comment above `temporal`, add a CC line and a CHANGELOG
   entry, and run `dataset check`.

   [^php-split15]: **SPLIT-15** (Must for the newest window, Should for the others; amended 2026-11-10, Lennart and
     Andrej): "The newest window is always a test window ... Prefer windows in other years, then other seasons, then
     other months, weeks or days, over the windows just before the newest. Walking back from the newest is one choice
     among others and needs its reason too."
   [^php-split20]: **SPLIT-20** (Should), case perth_house_prices: "one-month windows every third month back from
     December 2020 (`step=3`) instead of nine contiguous months in 2020, so most windows fall outside the COVID months
     and the stale-record period; chosen from counts, not scores (2026-10-26, Lennart)".
