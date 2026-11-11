# rain_in_australia

**Outcome:** added. Shipped on your verdict of 2026-10-26; on 2026-11-11 you kept the 14-day windows without a gap
(Horizon, ok) and spread the 26 windows one every 16 weeks from May 2018 to January 2026 (issue 7, B); both are applied
and nothing is left open. The review file of October (issues 2 to 6, settled on 2026-10-26) was removed then and stays
in git; this file numbers on from it.

**Main points:** Settled on 2026-11-11: 26 fortnights spread over the eight years open, so the score meets the dry and
the wet years, with the test rows of the 26 fortnights of the last year kept.

**Horizon:**

* **Verdict:** keep the 14-day windows without a gap (medium confidence): no source gives a refit cadence, and two weeks
  is the house convention for weather.
* **Length:** 14 days, a model refit every two weeks and used each morning in between; each prediction is for the next
  24 hours (rain from 9 am to 9 am). No source names a refit cadence: rattle's documentation calls weatherAUS a "sample
  dataset for illustrating analytics, data mining, and data science" that is "regularly updated" from the Bureau of
  Meteorology ([rattle, weatherAUS](https://rdrr.io/cran/rattle/man/weatherAUS.html)), and the source defines no task.
  The two weeks are copied from climate_model_weather_forecasting, where you wrote "For weather this is a bit much. I
  would argue for one or two weeks at most?" against TabReD's month. The actor (a farmer or local forecaster at 9 am)
  could refit every day, since each label is read the next morning.
* **Gap:** none. The label of the last training day is the rain up to 9 am on the first test day, read at that 9 am
  observation, before the first prediction; no late labels or revisions are documented.
* **Time frame:** the data runs from 1 November 2007 to 30 January 2026, with no rows from 27 January 2016 to 28
  February 2017 (nor in April 2011, December 2012 and February 2013). The 208 fortnights that keep half the rows for
  training start from 10 February 2018, all after that break, so every candidate meets the same recording (Sunshine and
  Evaporation missing in 66-79% of the rows). Today's windows cover one year, February 2025 to January 2026.
* **Options:**

  | | Option | What it does | Test windows | Pro | Con |
  |---|---|---|---|---|---|
  | A | 14 days (implemented) | 14-day windows, no gap: 208 candidates above the floor, from 10 February 2018 | 26 windows of 606 to 669 location-days (issue 7's B; today's 26: 619 to 642) | the one to two weeks you set for weather (climate_model_weather_forecasting); 619 to 642 location-days per window | no source names a refit cadence; the actor could refit every day |
  | B | 7 days | a weekly refit: 416 candidates from February 2018, 280 to 340 location-days each | 416 candidates of 280 to 340 location-days | within the one to two weeks you set for weather | halves the rows per window; no documented cadence |
  | C | One calendar month | a monthly refit: 95 candidates, 1,223 to 1,472 location-days each | 95 candidates of 1,223 to 1,472 location-days | more location-days per window | leaves up to a month of next-morning labels unused; a month mixes weeks of different weather; longer than the one to two weeks you set for weather |

* **Recommendation:** A: two weeks is the length you set for weather, and no source names a cadence that would set
  another. **Decision:** A, B or C?

**Lennart (2026-11-11, ok):** As implemented (A).

**Resolved (2026-11-11, Lennart):** A, the 14-day windows without a gap stay. `splits_comment` gives the reason from
this block: no source names a refit cadence (rattle's file is a sample dataset and defines no task), so the length is
the one or two weeks set for weather; the no-gap sentence stays. The record has the horizon CC line. `dataset check`:
0 errors, 0 warnings (README not regenerated).

**Issues for Lennart:**

7. **Which fortnights should the 26 test windows be?**

   * **Problem:**
     - The 26 test windows are the fortnights of the last year (1 February 2025 to 30 January 2026), as you decided on
       2026-10-26 for the count of test rows, while fortnights that keep half the rows for training reach back to
       February 2018.
     - Since 2026-11-10 the newest window always stays and the others are chosen from the use case and statistics of
       the data, preferring other years over the windows just before the newest[^ra-split15].
     - The share of rain days moves between years, from 17.8% (February 2019 to January 2020) to 27.2% (February 2022
       to January 2023), while the tested year sits at 21.5%, so the score meets neither a dry nor a wet year.
   * **Background:**
     - Your decision of 2026-10-26 (issue 2 of the October file) chose 26 back-to-back fortnights over nine spaced six
       weeks apart, both within one year, because 16,457 test rows halve the standard error of the mean score. B keeps
       the count, the length and the test rows (16,484) and moves only the dates.
     - The Bureau of Meteorology called 2019 "Australia's warmest and driest year on record"
       ([Annual Climate Statement 2019](https://media.bom.gov.au/releases/739/annual-climate-statement-2019-periods-of-extreme-heat-in-2019-bookend-australias-warmest-and-driest-year-on-record)),
       and the three twelve-month blocks from February 2020 to February 2023, the Bureau's La Niña years, hold the most
       rain days of the candidates (23.1% to 27.2%).
     - One window every 16 weeks (112 days) moves the season by about 3.7 months each time, so B's 26 windows start in
       every calendar month two or three times, as A's do.
     - PSI, the population stability index, compares a feature's distribution in the window with its train side; above
       0.25 is usually read as a large shift. Here it does not tell the candidates apart: a fortnight of one season
       against all earlier years gives a median PSI of 0.59 to 1.47 and a largest one of 4.7 to 10.2 (on the other
       locations' 9 am readings) in every candidate, and no test row has a category its train side lacks.
   * **Statistics:** from the candidate table, grouped into twelve-month blocks of 26 fortnights (February to
     January); rain days from every test row, the train side's from a 100,000-row sample.

     | Twelve months | Fortnights in A | Fortnights in B | Test rows | Rain days, test | Rain days, train side | Train share | Largest PSI |
     |---|---|---|---|---|---|---|---|
     | Feb 2025-Jan 2026 | 26 | 4 | 16,457 | 21.5% | 21.7-22.1% | 93.8-99.8% | 5.7-9.2 |
     | Feb 2024-Jan 2025 | 0 | 3 | 16,212 | 20.5% | 21.7-22.1% | 87.7-93.5% | 6.2-9.1 |
     | Feb 2023-Feb 2024 | 0 | 3 | 16,317 | 20.7% | 21.8-22.2% | 81.5-87.4% | 6.8-10.1 |
     | Feb 2022-Feb 2023 | 0 | 3 | 16,170 | 27.2% | 21.6-22.3% | 75.4-81.3% | 7.7-10.2 |
     | Feb 2021-Feb 2022 | 0 | 4 | 15,985 | 24.6% | 21.3-21.8% | 69.3-75.1% | 4.7-10.1 |
     | Feb 2020-Feb 2021 | 0 | 3 | 16,681 | 23.1% | 21.1-21.5% | 63.0-69.1% | 4.8-10.2 |
     | Feb 2019-Feb 2020 | 0 | 3 | 17,077 | 17.8% | 21.1-21.8% | 56.6-62.8% | 5.5-10.2 |
     | Feb 2018-Feb 2019 | 0 | 3 | 17,112 | 19.4% | 21.5-21.9% | 50.1-56.3% | 6.4-9.9 |

   * **Effect on the task:** A ranks models on one year of near-average rain, so a model that does well in that year's
     weather and worse in a drought or a wet year is not seen. B scores as many fortnights spread over eight years, the
     2019 drought and the wet La Niña years among them, with each refit trained on 51.8% to 99.8% of the rows instead
     of 93.8% to 99.8%.
   * **Consistency:** B departs from your call of 2026-10-26 only in "over the last year"; its reason, the count of test
     rows, stays. climate_model_weather_forecasting_1m, the other weather task, tests its three newest weeks
     (`n_windows=3`).
   * **Sources:** the definition `datasets/_dev/tabarena-v0pt2/rain_in_australia/dataset.py` (`temporal`,
     `splits_comment`, the window decision table in `_decisions`); the record `curation/records/rain_in_australia.md`
     (CC 2026-10-26, issue 2); the candidate table `.venv/bin/python -m data_foundry.curation.cli dataset windows
     rain_in_australia --root datasets/_dev/tabarena-v0pt2` (208 fortnights).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | The last year (implemented) | tests the 26 fortnights from 1 Feb 2025 to 30 Jan 2026 | the year closest to deployment; each refit trains on 93.8% or more | one year of near-average rain; no dry or wet year |
     | B | One every 16 weeks over eight years | tests 26 fortnights from 19 May 2018 to 30 Jan 2026, every eighth candidate | the same count and test rows; the 2019 drought and the wet 2020-2022 years; every month two or three times | departs from "over the last year" of your call; the oldest refit trains on 51.8% |

   * **Recommendation:** B: it keeps what your call of 2026-10-26 was for, 26 fortnights and their test rows, and
     spreads them over the eight years open, so the score covers the dry and the wet years a deployed forecaster meets.
     **Decision:** A or B?

   **Notes for the AI:** on B, `temporal = Temporal(on="Date", splits=TemporalSplits(window=14, unit="days",
   cutoffs=("2026-01-17", "2025-09-27", "2025-06-07", "2025-02-15", "2024-10-26", "2024-07-06", "2024-03-16",
   "2023-11-25", "2023-08-05", "2023-04-15", "2022-12-24", "2022-09-03", "2022-05-14", "2022-01-22", "2021-10-02",
   "2021-06-12", "2021-02-20", "2020-10-31", "2020-07-11", "2020-03-21", "2019-11-30", "2019-08-10", "2019-04-20",
   "2018-12-29", "2018-09-08", "2018-05-19")))` (the same windows as `n_windows=26, step=112`). From the candidate
   table, newest first: test 622, 640, 633, 625, 623, 641, 625, 641, 628, 612, 609, 615, 617, 606, 617, 606, 635,
   627, 664, 656, 663, 660, 652, 655, 669 and 643 rows (16,484); train 263,940, 258,901, 253,817, 248,740, 243,747,
   238,730, 233,729, 228,777, 223,729, 218,696, 213,746, 208,721, 203,707, 198,800, 193,990, 189,053, 184,058,
   179,005, 173,861, 168,710, 163,429, 158,199, 152,958, 147,681, 142,432 and 137,157 (99.8% to 51.8%). Then rewrite
   `task_summary.split` ("26 test windows of 14 days, one after the other from February 2025 to January 2026"),
   `splits_comment` (the windows, the reasons and the yearly rain shares above; the no-gap sentence stays; the
   2016-2017 break lies before every window) and the window decision in `_decisions` (its shipped row and title), add a
   CC line to the record and a dated CHANGELOG entry, and run `dataset check`.

   [^ra-split15]: **SPLIT-15** (Must for the newest window, Should for the others; amended 2026-11-10, Lennart and
     Andrej): "The newest window is always a test window ... The other windows are the curator's choice, per dataset,
     argued from the use case ... The evidence is statistics of the data, never a model's score ... Prefer windows in
     other years, then other seasons, then other months, weeks or days, over the windows just before the newest."

   **Lennart (2026-11-11, change):** Option B: One every 16 weeks over eight years.

   **Resolved (2026-11-11, Lennart):** B. `temporal` declares the 26 cutoffs of the notes above, from 2026-01-17 back to
   2018-05-19: test 606 to 669 location-days per window (16,484 in all, 55 to 202 rain days each), train 137,157 to
   263,940 rows (51.8% to 99.8%). `task_summary.split` and `splits_comment` name the spread and its reason (the yearly
   rain shares from 17.8% in 2019-20 to 27.2% in 2022-23, every calendar month two or three times) and say why 26
   windows rather than the nine folds a random split of this size gets: a 14-day window, the rule on short weather
   windows, holds about 630 location-days, so 26 windows keep the test rows. The window decision in `_decisions` shows
   the shipped spread and, as its own row, the 26 back-to-back fortnights of 2026-10-26; the standard errors of the
   CC of 2026-10-26 and the AUC figures of the notes are dated to the windows they were measured on. The record has the
   decision CC line. `dataset check`: 0 errors, 0 warnings.
