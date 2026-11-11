# mortgage

**Outcome:** added. You shipped it on 2026-10-26. Under the rule on choosing test windows, rewritten on 2026-11-10,
the AI recommends testing 2015 Q1, 2012 Q2 and 2009 Q3 instead of the three newest quarters, so the windows cover
the calm years, the recovery and the crisis in three different quarters of the year (issue 16). The one-quarter
horizon is kept. `dataset.py` is unchanged until you decide.

**Main points:** Test on 2015 Q1, 2012 Q2 and 2009 Q3 instead of 2014 Q3 to 2015 Q1 (issue 16)? Sign off the
one-quarter horizon.

**Horizon:**

* **Verdict:** keep the one-quarter windows (medium confidence): a quarter is the book's own backtest window and the
  label's own horizon, and the use case scores the book at every quarter's start; no source gives a refit cadence.
* **Length:** the definition cites the book's out-of-time backtest, which fits on the periods before 60 and tests on
  period 60 ("`mortgage[mortgage$time < 60, ]` against `mortgage[mortgage$time > 59, ]`", R Companion, chapter 13, as
  quoted in `splits_comment`); still unverified: no copy of the R Companion was found (web search for the book and its
  companion), and the data page (http://www.creditriskanalytics.net/datasets-private2.html) gives only the files. Each
  row's label is the loan's status at the end of its quarter, so one quarter is also how far ahead the lender looks.
  Refit cadence: none found for this book; banks with internal PD models must "review their estimates when new
  information comes to light but at least on an annual basis" (EU CRR Art. 179(1)(c),
  https://www.legislation.gov.uk/eur/2013/575/article/179), so a model refit once a year and scored every quarter is
  the other common practice.
* **Gap:** none needed: the status of a quarter is known when the next one starts, and every feature is lagged to
  what was published by the quarter's start.
* **Time frame:** periods 1 to 60, 2000 Q2 to 2015 Q1, a closed book that ages, with 1,728 seasoned loans added in
  2013 Q1 (period 52). The 26 quarters from 2008 Q4 (period 35, 51.8% train share) to 2015 Q1 keep half the rows for
  training; they span the crisis (default rates of 4.4% to 5.1% a quarter in 2009), the recovery and the calm of
  2014-2015 (0.5% to 0.9%).
* **Options:**

  | | Option | What it does | Test windows | Pro | Con |
  |---|---|---|---|---|---|
  | A | One quarter (implemented) | windows of one period, no gap: 26 candidates above the floor, 2008 Q4 to 2015 Q1 | 3 windows (issue 16's B) of 8,004 to 15,921 loan-quarters | the book's own backtest window and the label's own horizon; the use case scores the book at every quarter's start | no source gives a refit cadence; the backtest quote is still unverified |
  | B | Four quarters | a model refit once a year: 6 candidates above the floor, back to 2009 Q2-2010 Q1 | 6 candidates of 33,328 to 62,004 loan-quarters | one model serves a year, as under an annual review | the book tests one quarter and the use case scores every quarter |
  | C | Two quarters | 13 candidates above the floor | 13 candidates of 16,176 to 37,895 loan-quarters | more loan-quarters per window | no source for it |

* **Recommendation:** A: the book tests one quarter, the label looks one quarter ahead, and the use case scores the book
  every quarter. **Decision:** A, B or C?

**Issues for Lennart:**

16. **Which quarters should the test windows be?**

   * **Problem:**
     - The three test windows are the three newest quarters (2014 Q3, 2014 Q4 and 2015 Q1), while 26 quarters, from
       2008 Q4 on, keep half the rows for training.
     - Since 2026-11-10 the newest window always stays and the others are chosen from the use case and statistics of
       the data, preferring other years, then other seasons, over the quarters just before the newest[^mo-split15].
     - The eligible quarters run from the crisis to the calm years, with default rates from 0.5% to 5.1% a quarter,
       but today's three windows all lie in the calm (0.5% to 0.9%).
   * **Background:** Period 1 is 2000 Q2, so period 60 is 2015 Q1, 49 is 2012 Q2 and 38 is 2009 Q3. The book is a
     closed panel that ages: an older window holds more and younger loans (8,004 in 2015 Q1, 15,921 in 2009 Q3), and
     its train side covers fewer years. The macro columns hold one value per quarter, so every window shows a value
     its train side never had (largest PSI 8.5 to 9.7 in every candidate); the median PSI over the loan columns is the
     drift to read. PSI, the population stability index, compares a feature's distribution in the window with its
     train side; above 0.25 is usually read as a large shift. Option B spaces the windows 11 quarters apart, so they
     fall in three different years and three different quarters of the year.
   * **Statistics:** from the candidate table (100,000-row samples of each side for the drift).

     | Period | Quarter | In | Test rows | Default / payoff, test | Default / payoff, train side | Train share | Median PSI | Largest PSI |
     |---|---|---|---|---|---|---|---|---|
     | 60 | 2015 Q1 | A, B, C | 8,004 | 0.5% / 1.8% | 2.4% / 4.3% | 98.7% | 0.25 | 8.7 |
     | 59 | 2014 Q4 | A | 8,172 | 0.6% / 2.0% | 2.4% / 4.4% | 97.4% | 0.32 | 8.6 |
     | 58 | 2014 Q3 | A | 8,459 | 0.9% / 1.7% | 2.5% / 4.3% | 96.0% | 0.35 | 8.6 |
     | 49 | 2012 Q2 | B | 9,431 | 2.1% / 1.9% | 2.6% / 4.6% | 82.6% | 0.23 | 9.7 |
     | 48 | 2012 Q1 | C | 9,812 | 2.3% / 1.8% | 2.7% / 4.8% | 81.1% | 0.46 | 8.7 |
     | 38 | 2009 Q3 | B | 15,921 | 4.4% / 2.4% | 2.5% / 5.8% | 60.6% | 0.60 | 8.5 |
     | 36 | 2009 Q1 | C | 18,384 | 4.8% / 1.9% | 2.3% / 6.1% | 54.9% | 0.43 | 9.1 |

   * **Effect on the task:** Under A a model is ranked on a seasoned book in three calm quarters, where the default
     rate is a quarter of the train side's and the quarter's overall event rate already carries most of the score
     (curation notes). B adds a recovery quarter close to the train side's level and a crisis quarter whose default
     rate is almost twice the train side's, a quarter a lender's model has to get through.
   * **Consistency:** Every option keeps period 60, the book's own backtest quarter[^mo-split19]. No dataset has chosen
     windows in a crisis under the rewritten rule yet; numerai_v5_2_1m keeps its newest years for a reason mortgage
     lacks (the features were built on the older eras).
   * **Sources:** the definition `datasets/_dev/tabarena-v0pt2/mortgage/dataset.py` (`splits_comment`, `temporal`);
     the record `curation/records/mortgage.md`; the candidate table `.venv/bin/python -m data_foundry.curation.cli
     dataset windows mortgage --root datasets/_dev/tabarena-v0pt2` (30 windows listed, 26 above the floor).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Newest three quarters (implemented) | tests 2015 Q1, 2014 Q4 and 2014 Q3 | the book's backtest quarter and the two before it; the most training data (oldest 96.0%) | three calm quarters in a row; nothing of the crisis or the recovery |
     | B | Three years, three seasons | tests 2015 Q1, 2012 Q2 and 2009 Q3 | the calm, the recovery and the crisis; three different quarters of the year; spread over the 26 candidates | the oldest trains on 60.6% and on a younger book |
     | C | Three first quarters | tests 2015 Q1, 2012 Q1 and 2009 Q1 | three years three years apart | one season only; the oldest trains on 54.9% |

   * **Recommendation:** B: it spreads the windows over the eligible history in other years and other seasons, as the
     rule prefers, and puts one window in each regime the book went through, while each train side keeps at least
     60.6% of the rows. **Decision:** A, B or C?

   **Notes for the AI:** on B, `temporal = Temporal(on="time", splits=TemporalSplits(window=1, unit="unique",
   cutoffs=(60, 49, 38)), horizon=1, horizon_unit="steps", time_unit="quarters")`: test 8,004, 9,431 and 15,921
   rows, train 613,649, 513,686 and 376,900 (98.7%, 82.6%, 60.6%). On C, `cutoffs=(60, 48, 36)`: test 8,004, 9,812
   and 18,384 rows, train 613,649, 503,874 and 341,354 (98.7%, 81.1%, 54.9%). Then rewrite `task_summary.split`,
   `splits_comment` (the windows, the reasons and the numbers above; recount the share of test rows whose loan has
   earlier quarters in train, today 99.4-99.9%), the windows table in `_decisions` (`df["time"] >= 58`), and the
   curation notes that quote LightGBM numbers for periods 60 / 59 / 58 (mark them as measured on the earlier
   windows); add a CC line to the record and a dated CHANGELOG entry, and run `dataset check` (SPLIT-15).

   [^mo-split15]: **SPLIT-15** (Must for the newest window, Should for the others; amended 2026-11-10, Lennart and
     Andrej): "The newest window is always a test window ... The other windows are the curator's choice, per dataset,
     argued from the use case ... The evidence is statistics of the data, never a model's score ... Prefer windows in
     other years, then other seasons, then other months, weeks or days, over the windows just before the newest."
   [^mo-split19]: **SPLIT-19** (Should): "When the source defines the split (a competition's or a paper's official
     periods), follow it."
