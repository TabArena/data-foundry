# ashrae_great_energy_predictor_iii

**Outcome:** added as `ashrae_great_energy_predictor_iii_1m`. Under the rule on choosing test windows, rewritten on
2026-11-10, the AI recommends keeping the three four-month windows that tile 2017 (issue 1): at the declared length
they are the only three windows that do not overlap, and they test each season once. They cannot test another year,
and the oldest trains on 49.5% of the rows. `dataset.py` is unchanged until you decide.

**Main points:** Keep January-April, May-August and September-December 2017 as the test windows, the only choice at
four months (issue 1)?

**Issues for Lennart:**

1. **Keep the three four-month windows that tile 2017, the only choice at this length?**

   * **Problem:**
     - The newest window (September-December 2017) always stays[^as-split15], and at the declared length of four
       months the only two windows that overlap neither it nor each other are January-April and May-August 2017,
       today's windows.
     - The oldest window trains on 2016 alone, 49.5% of the rows (19,325,311 of 39,062,170), half a point under the
       floor of half the rows, which the floor's amendment of 2026-11-08 allows for a third window when the test
       entities are known from training, as every meter here is[^as-split14].
     - No choice of windows can test another year or a baseline used for a whole year, because every test month is in
       2017, 2018 is not public, and each window starts right after its train side.
   * **Background:**
     - The savings of a retrofit are the readings set against what the building would have used, so the model has to
       predict every season: steam and hot water peak in winter, chilled water in summer. Today's windows test each
       season once: January-April (mean air temperature 5.7 to 16.3 °C by month), May-August (19.1 to 26.1 °C) and
       September-December (22.1 down to 5.0 °C).
     - With a step of one month, the four-month windows that keep half the rows for training start from February
       2017 (53.7%). Two windows besides September-December that do not overlap must both fit into January-August,
       which only January-April and May-August do; February-May would overlap May-August.
     - The length: the competition asked for the two years after its training year, and four months is the longest
       window that gives three windows inside 2017[^as-split12]. With the 500k test budget every window ships
       500,000 readings whatever its length.
     - PSI, the population stability index, compares a feature's distribution in the window with its train side;
       above 0.25 is usually read as a large shift. Here only the weather drifts; the meter mix stays at 58-60%
       electricity in every month.
   * **Statistics:** from the candidate tables (100,000-row samples of each side for the target and the drift; the
     readings and train shares from all rows).

     | Window (2017) | In | Readings | Train share | Mean log1p reading, test / train | Largest drift (PSI) |
     |---|---|---|---|---|---|
     | Sep-Dec | A | 6,635,375 | 83.0% | 4.58 / 4.61 | 0.06, air temperature |
     | May-Aug | A | 6,628,356 | 66.0% | 4.64 / 4.61 | 1.47, air temperature |
     | Jan-Apr | A | 6,473,128 | 49.5% | 4.59 / 4.62 | 0.51, dew point |
     | Oct-Dec | B | 4,992,088 | 87.2% | 4.54 / 4.62 | 0.30, air temperature |
     | Jun-Aug | B | 4,957,226 | 70.3% | 4.69 / 4.59 | 2.20, air temperature |
     | Feb-Apr | B | 4,809,420 | 53.7% | 4.60 / 4.63 | 0.33, dew point |

   * **Effect on the task:** Under either option the benchmark scores a meter's reading at most four (B: three)
     months after the last reading a model saw, in 2017 only. A savings estimate rests on a baseline fit once before
     the retrofit and used for a year or more, so the error that builds up over a year, and a change from one year to
     the next (occupancy, equipment), stay unmeasured; the score reads as the error of a model refit shortly before.
   * **Consistency:**
     - The oldest window is the competition's own setting (train on 2016, predict early 2017), which the splits
       comment keeps on purpose; your call of 2026-10-15 split by time because savings are measured on the same
       buildings after the cutoff.
     - The floor's amendment came from wisconsin_local_government_property_insurance_fund: two windows above the
       floor and one at 40.6%, with 97.6-98.8% of each test year's members known from training. Here every test
       meter is known from training (`building_id` 100%).
     - aeolus_rebuilt_1m has the window question open under the rewritten rule; no dataset has decided under it yet.
   * **Sources:** the definition `datasets/_dev/tabarena-v0pt2/ashrae_great_energy_predictor_iii_1m/dataset.py`
     (`temporal`, `splits_comment`); the record `curation/records/ashrae_great_energy_predictor_iii.md` (CC
     2026-10-15); the candidate tables `.venv/bin/python -m data_foundry.curation.cli dataset windows
     ashrae_great_energy_predictor_iii_1m --root datasets/_dev/tabarena-v0pt2 --step 1`, and with `--window 3 --unit
     months --step 1` for B.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Three four-month windows tile 2017 (implemented) | tests Jan-Apr, May-Aug and Sep-Dec 2017 | every month and season of 2017 once; the only windows at the declared length that do not overlap; the oldest is the competition's setting | the oldest trains on 49.5%, admitted only by the floor's amendment; no other year |
     | B | Three three-month windows | tests Feb-Apr, Jun-Aug and Oct-Dec 2017 | every train side above the floor (53.7% to 87.2%); still winter, summer and autumn | January, May and September untested; a shorter window chosen for the floor alone, not from the use case |

   * **Recommendation:** A: the use case needs every season, A tests all of 2017 once, and the amended floor admits
     its oldest window; B gives up a quarter of the year to gain half a point of training share. **Decision:** A or
     B?

   **Notes for the AI:** on A, in `splits_comment`: replace "49.12% of the rows" with 49.47% (19,325,311 of
   39,062,170 rows on the current frame); give the reason for the windows (the newest, and the only four-month
   windows that do not overlap, one per season) and the floor's amendment (two windows above it, every test meter
   known from training). The amendment asks the notes for the score on the two valid windows next to all three and
   what the oldest window changes: that needs a run on the shipped splits, separate from the choice of windows. Add a
   CC line to the record, a dated CHANGELOG entry and an ashrae row under SPLIT-14 in the Cases table of
   `knowledge-curation/references/splits.md` (SPLIT-14 amended 2026-11-08, SPLIT-15). On B,
   `temporal = Temporal(on="timestamp", splits=TemporalSplits(window=3, unit="months", cutoffs=("2017-10-01",
   "2017-06-01", "2017-02-01")))`. Built with `TemporalSplits.splits` on the definition's frame: test 4,992,088,
   4,957,226 and 4,809,420 readings (500k of each kept), train 34,070,082, 27,469,569 and 20,989,019 (87.2%, 70.3%,
   53.7%). Then rewrite `task_summary.row` and `task_summary.split`, `splits_comment` and the row-budget bullet
   (every reading before October 2017 and 500k of October-December), add the CC line and the CHANGELOG entry, and run
   `dataset check`.

   [^as-split15]: **SPLIT-15** (Must for the newest window, Should for the others; amended 2026-11-10, Lennart and
     Andrej): "The newest window is always a test window ... The other windows are the curator's choice, per dataset,
     argued from the use case ... The evidence is statistics of the data, never a model's score ... Prefer windows in
     other years, then other seasons, then other months, weeks or days, over the windows just before the newest."
   [^as-split14]: **SPLIT-14** (Must; amended 2026-11-08, Lennart, on
     wisconsin_local_government_property_insurance_fund): at least 3 windows, and no window's train side holds less than 50% of the data. "A release with two windows
     above the floor may add one older window that trains on at least 40% of the rows, when most test entities recur
     (the actor re-rates entities it knows) and folds by entity would test unseen ones; the notes give the score on
     the valid windows next to all windows and what the short window changes."
   [^as-split12]: **SPLIT-12** (Should): the horizon is a human judgment from the source: how far ahead the actor
     predicts, the competition's own test window, the refit cadence.
