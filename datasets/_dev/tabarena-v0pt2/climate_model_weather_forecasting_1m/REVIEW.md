# climate_model_weather_forecasting

**Outcome:** added as `climate_model_weather_forecasting_1m`. Under the rule on choosing test windows, rewritten on
2026-11-10, the AI proposes to keep the newest week (24-30 July 2023) and to replace the two other July weeks with a
week in May and one in February 2023 (issue 1). `dataset.py` is unchanged until you decide.

**Main points:** Test on 24-30 July, 1-7 May and 6-12 February 2023 instead of the last three weeks of July (issue 1)?

**Issues for Lennart:**

1. **Which weeks of 2023 should the test windows be?**

   * **Problem:**
     - The three test windows are the last three weeks of July 2023, so the score measures one month, while a weather
       service corrects the forecasts every week of the year.
     - Since 2026-11-10 the newest window always stays and the others are chosen from the use case and statistics of
       the data, preferring other seasons over the weeks just before the newest[^split15].
     - The data run from July 2022 to July 2023, and one-week windows from 6 February 2023 on keep at least half the
       rows for training, so late winter, spring and summer are open to choose from, while no other year is[^split14].
   * **Background:** The stations lie between 28 degrees south and 32 degrees north (half the rows between 4 south and
     17 north), so the seasons are mild: the monthly mean of the measured temperature runs from 25.4 in January 2023 to
     28.0 in May, and is 27.3 in July. What changes most with the season are the models' upper-air temperature forecasts
     (`gfs_temperature_5000`, `gfs_temperature_7000`). `apply_time_rl` is the forecast's time in epoch seconds, always
     newer in a test window, so its drift (PSI 8.28 in every window) says nothing about the season and is left out
     below. PSI, the population stability index, compares a feature's distribution in the window with its train side;
     above 0.25 is usually read as a large shift. The length stays one week[^split18]. B's windows are 12 weeks apart.
   * **Statistics:** the target from all rows; the drift from the candidate table (100,000-row samples of each side);
     265k to 396k rows per window.

     | Window (2023) | In | Mean temperature, test | Train side | Train share | Largest drift (PSI) |
     |---|---|---|---|---|---|
     | 24-30 Jul | A, B | 27.22 | 26.87 | 97.8% | 1.61, `gfs_temperature_7000` |
     | 17-23 Jul | A | 27.15 | 26.87 | 95.8% | 1.27, `gfs_temperature_7000` |
     | 10-16 Jul | A | 27.21 | 26.86 | 93.4% | 1.09, `gfs_temperature_7000` |
     | 1-7 May | B | 28.06 | 26.57 | 70.2% | 0.71, `cmc_0_3_5_500` |
     | 6-12 Feb | B | 26.47 | 26.36 | 50.7% | 3.34, `gfs_temperature_5000` |

   * **Effect on the task:** A ranks models on three near copies of mid-summer (mean 27.15 to 27.22, the same drift). B
     adds the warmest weeks of the year, 1.5 degrees above the training mean, and late-winter weeks whose upper-air
     forecasts differ most from training.
   * **Consistency:** The one-week length follows your note in the record (TabReD's month is "a bit much" for
     weather). No dataset has chosen windows under the rewritten rule yet.
   * **Sources:** the definition `datasets/_dev/tabarena-v0pt2/climate_model_weather_forecasting_1m/dataset.py`
     (`splits_comment`, `temporal`); the record `curation/records/climate_model_weather_forecasting.md`; the candidate
     table `.venv/bin/python -m data_foundry.curation.cli dataset windows climate_model_weather_forecasting_1m --root
     datasets/_dev/tabarena-v0pt2` (25 weeks, 6 February to 30 July 2023).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Last three weeks (implemented) | tests 24-30, 17-23 and 10-16 Jul 2023 | the weeks right after a refit | one month only; three near copies |
     | B | July, May, February | tests 24-30 Jul, 1-7 May and 6-12 Feb 2023 | summer, the warmest weeks and late winter; evenly spread | the February window trains on 50.7%, just above half |

   * **Recommendation:** B: it keeps the newest week and spreads the others over the half year open to choose from,
     where the target (+1.5 in May) and the upper-air forecasts (PSI 3.34 in February) shift most. **Decision:** A or
     B?

   **Notes for the AI:** on B, `temporal = Temporal(on="fact_time", splits=TemporalSplits(window=7, unit="days",
   cutoffs=("2023-07-24", "2023-05-01", "2023-02-06")))`. Built on the definition's frame: test 377,992, 385,508 and
   264,711 rows, train 16,573,836, 11,900,488 and 8,588,380 (97.8%, 70.2%, 50.7%). Then rewrite `task_summary.split`
   ("Each of the last three weeks of July 2023") and `splits_comment` (the windows, the reasons and the numbers above),
   add a CC line to the record and a dated CHANGELOG entry, and run `dataset check` (SPLIT-15).

   [^split15]: **SPLIT-15** (Must for the newest window, Should for the others; amended 2026-11-10, Lennart and
     Andrej): "The newest window is always a test window ... The other windows are the curator's choice, per dataset,
     argued from the use case ... The evidence is statistics of the data, never a model's score ... Prefer windows in
     other years, then other seasons, then other months, weeks or days, over the windows just before the newest."
   [^split14]: **SPLIT-14** (Must): at least 3 windows, and no window's train side holds less than 50% of the data.
   [^split18]: **SPLIT-18** (Should): short-lived quantities need short windows: weather test windows of one to two
     weeks at most (case: this dataset).
