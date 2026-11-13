---
unique_name: climate_model_weather_forecasting
name: Weather
checked_by:
- Lennart
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
- 'Entities: Recur'
collections:
- TabArena Reject
- TabRed
- tabular-dl-more-data
original_source: Kaggle
year: '2024'
domain: environmental science & climate
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/pcovkrd84mejm/tabred-weather
- https://github.com/yandex-research/tabred/tree/main/preprocessing#weather
notebook_path: datasets/beyond_iid/temporal/climate_model_weather_forecasting/climate_model_weather_forecasting_1m.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/climate_model_weather_forecasting_1m/dataset.py
source_row: 715
type_adapter_id: curation-record-v1
---

## Comments

Was downsampled/filtered by TabRed via preprocessing

Maybe not a super relevant task for tabular models.... need to make a judgment call. Given it was used in TabRed, I would say we can go for it now but might need to remove it later

TabRed uses 1 month refit horizon. For weather this is a bit much. I would argue for one or two weeks at most?

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source rmse — RMSE, Rubachev et al. 2025, TabReD (ICLR), https://arxiv.org/abs/2406.19380; Shifts weather (Malinin et al. 2021) also uses RMSE.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `shifts_weather_temperature` (TBD -> 2nd Tier, priority 3). Each is screened in its own record; this record's verdict stays the curator's.

**Assessment (AI, 2026-11-10):** priority for the review of the test windows (PR #78), which this record never had. Priority 3: gap 0, use case 0 (written by the curation, 'for example'), source + (the TabReD paper), shape +, risk 0 (the open issue is the choice of windows).

CC (2026-11-11, Lennart): Review issue 1, B ("Option B: July, May, February.", confirmed again after the answer of 2026-11-10): the test weeks are 24-30 July, 1-7 May and, with the 3-day gap of the horizon sign-off, 13-19 February 2023, in place of the last three weeks of July.

CC (2026-11-11, Lennart): the declared horizon (7 days, a 3-day gap, windows starting 2023-07-24, 2023-05-01 and 2023-02-13) is checked, as one week is a conservative refit that still spans several weather situations while a forecast is issued up to three days before its measurement, so each window trains only on what was measured when its forecasts were issued (Review horizon, B: "Option B: A 3-day gap.").

**Assessment (AI, 2026-11-11):** applied issue 1 (B) and the horizon (B): `temporal` declares 7-day windows from 2023-07-24, 2023-05-01 and 2023-02-13 with a 3-day gap; test 377,992, 385,508 and 270,717 rows, train 16,429,730, 11,733,079 and 8,739,284 (96.9%, 69.2% and 51.6% of the 16,951,828 rows); 19.7%, 21.8% and 21.3% of the windows' forecasts were issued before the window starts, and the gap covers the 99.2% issued at most 72 hours ahead. With the gap 6-12 February would train on 49.95%, which SPLIT-14 as amended on 2026-11-11 admits; 13-19 February is the curator's pick, as the splits comment says. The 144,106 rows of 21-23 July 2023 lie in no split. `dataset check`: 0 errors, 0 warnings.

## Review

**Outcome:** added as `climate_model_weather_forecasting_1m`. On 2026-11-11 you chose a 3-day gap before each one-week
window (H, B) and the weeks of 24-30 July, 1-7 May and 13-19 February 2023 (issue 1, B); both are applied and nothing
is left open.

**Main points:** Settled on 2026-11-11: three one-week windows from February to July 2023, each trained on what was
measured three days before it, as a forecast is issued up to three days ahead.

**Horizon:**

* **Verdict:** keep the 7-day windows (high confidence) and add a 3-day gap (medium confidence): no source gives
  Yandex's refit cadence and post-processing models are re-estimated daily on the last 30-60 days, so one week is a
  conservative refit that still spans several weather situations, while a forecast is issued up to three days before
  its measurement.
* **Length:** the week goes back to your record note ("one or two weeks at most?"), which became the rule on short
  windows for weather; TabReD itself tests one month ("1 month in the test set (01.07.2023 -- 30.07.2023)",
  https://github.com/yandex-research/tabred/tree/main/preprocessing) and states no refit cadence. The Shifts paper
  says the data "is used by Yandex for real-time weather forecasts" (https://arxiv.org/abs/2107.07455); the
  post-processing literature trains on "the most recent 30–60 d only" and re-estimates "every day"
  (https://npg.copernicus.org/articles/27/23/2020/). One day (about 175 candidates) would test one weather situation
  per window and be shorter than the 3-day lead; 14 days (12 candidates) is the upper bound of the rule on weather
  windows.
* **Gap:** none today, but a forecast is issued up to 74 hours before its measurement (`apply_time_rl`, median 31.5
  hours): 19% to 24% of each window's rows were issued before the window starts, and their train side holds readings
  of their own station taken up to 3.1 days after the forecast was issued. A station's daily error carries over for
  days (the daily forecast error of a station, minus its mean, correlates 0.34, 0.23 and 0.18 at lags of one, two and
  three days, against 0.14 at seven days and 0.08 at thirty), so these readings tell a model what the forecast at the
  issue time could not know. A forecast made ahead of time is a planning gap: the model that corrects it can only
  have been trained on what was measured when it was issued[^h-split10]. Of the forecasts, 99.2% are issued at most
  72 hours ahead, so a 3-day gap covers them. Without the gap, a model is scored on forecasts whose station it has
  seen measured up to three days later, which a post-processing model at the issue time could not; the effect is
  largest for the longest lead times. How much the score moves is unknown: measuring it would need a model, which
  this choice does not rest on.
* **Time frame:** TabReD's year, 1 July 2022 to 30 July 2023; windows that keep half the rows for training run from
  February to July 2023, so no other year can be tested. With the gap your February week of issue 1, 6-12 February,
  would train on 49.95% of the rows, under the floor[^h-split14]; the week after, 13-19 February, keeps your choice
  of a late-winter week.
* **Statistics:** your windows of issue 1 with a 3-day gap, from the definition's frame:

  | Window | Rows tested | Train side | Train share | Mean temperature, test and train |
  |---|---|---|---|---|
  | 24-30 July 2023 | 377,992 | 16,429,730 | 96.9% | 27.26, 26.86 |
  | 1-7 May 2023 | 385,508 | 11,733,079 | 69.2% | 28.10, 26.54 |
  | 13-19 February 2023 | 270,717 | 8,739,284 | 51.6% | 26.18, 26.33 |

* **Options:**

  | | Option | What it does | Test windows | Pro | Con |
  |---|---|---|---|---|---|
  | A | No gap (implemented) | 7-day windows without a gap; your windows of issue 1: 24-30 July, 1-7 May, 6-12 February | 3 windows of 264,711 to 385,508 forecasts | your pick as marked | a fifth of each window's forecasts have later readings of their station in training |
  | B | A 3-day gap | 7-day windows with a 3-day gap: 24-30 July, 1-7 May, 13-19 February (96.9%, 69.2%, 51.6%) | 3 windows of 270,717 to 385,508 forecasts | training holds only what was measured when each forecast was issued; your months stay | February moves one week; about 3 days fewer of training per window |

* **Recommendation:** B: the gap mirrors what the corrector knows at the issue time, and it keeps your choice of
  seasons. **Decision:** A or B?

**Notes for the AI:** on B, `temporal = Temporal(on="fact_time", splits=TemporalSplits(window=7, unit="days",
cutoffs=("2023-07-24", "2023-05-01", "2023-02-13"), gap=3, gap_unit="days"))`: test 377,992, 385,508 and 270,717
rows, train 16,429,730, 11,733,079 and 8,739,284. Then resolve issue 1 with these windows, rewrite
`task_summary.split` and `splits_comment` (the windows, the gap and the reason from the Horizon block), a CC line in
the record with the CC line that the declared horizon is checked, a dated CHANGELOG entry, `dataset check`. On A,
issue 1's B as marked (cutoffs 2023-07-24, 2023-05-01, 2023-02-06, no gap) and the reason for no gap in the notes.

[^h-split10]: **SPLIT-10** (Should): when a label is known only some time after its row, train on the rows whose
  outcome is known by the window's start; "a forecast made a day ahead is a gap too".
[^h-split14]: **SPLIT-14** (Must): at least 3 windows, and no window's train side holds less than 50% of the data.

**Lennart (2026-11-11, change):** Option B: A 3-day gap.

**Resolved (2026-11-11, Lennart):** B. `temporal` declares 7-day windows starting 2023-07-24, 2023-05-01 and
2023-02-13 with `gap=3, gap_unit="days"`. `task_summary.split`, `changes`, `splits_comment` and the row-budget note
give the windows and why each, the gap and its reason (19.7%, 21.8% and 21.3% of the windows' forecasts were issued
before the window starts; a station's error carries over for days) and the week's reason from this block; the splits
comment also says that SPLIT-14 as amended on 2026-11-11 would admit 6-12 February (49.95%), and that 13-19 February
is your pick. Test 377,992, 385,508 and 270,717 rows, train 16,429,730, 11,733,079 and 8,739,284 (96.9%, 69.2%,
51.6% of 16,951,828); the 144,106 rows of 21-23 July 2023, the newest window's gap, lie in no split. The record has
the horizon CC line. `dataset check`: 0 errors, 0 warnings (README not regenerated).

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

   **Lennart (2026-11-10, change):** Option B: July, May, February.

   **Answer (AI, 2026-11-10):**
   - The week holds (the Horizon block above), but the audit found that a fifth of each window's forecasts were issued
     before the window starts while their train side holds later readings of the same station; the horizon sign-off (H)
     asks for a 3-day gap.
   - With that gap your February week (6-12 February) would train on just under half the rows; 13-19 February keeps your
     pick above the floor. This issue waits on the horizon sign-off (H).

   **Lennart (2026-11-11, change):** Option B: July, May, February.

   **Resolved (2026-11-11, Lennart):** B, with the 3-day gap of the horizon sign-off (H, B): the test weeks are 24-30
   July, 1-7 May and 13-19 February 2023 (`cutoffs=("2023-07-24", "2023-05-01", "2023-02-13")`); February moves one
   week from the notes above so that its train side keeps half the rows with the gap. `task_summary.split` and
   `splits_comment` name the windows and why each: the newest; the warmest month (mean measured temperature 28.06
   against 26.55 on its train side); late winter, when the upper-air forecasts differ most from training. Test 377,992,
   385,508 and 270,717 rows, train 96.9%, 69.2% and 51.6%. The record has the decision CC line. `dataset check`: 0
   errors, 0 warnings.

## Reference

TabRed
