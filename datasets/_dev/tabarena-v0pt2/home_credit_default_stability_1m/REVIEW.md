# home_credit_default_stability

**Outcome:** added as `home_credit_default_stability_1m`. Under the rule on choosing test windows, rewritten on
2026-11-10, the AI proposes to keep the newest window (1 September to 5 October 2020) and to replace May-June and
July-August 2020 with March-April 2020 and November-December 2019 (issue 1). `dataset.py` is unchanged until you
decide.

**Main points:** First the horizon sign-off (H), from the horizon audit of 2026-11-10: three-month windows instead of
two, spread before, across and after the March 2020 break? Issue 1 (the windows at two months) waits on it.

**Horizon:**

* **Verdict:** change the 2-month windows to 3 months (medium-low confidence): no source states a refit cadence; a
  scorecard serves for months and the competition scores one fit over the following weeks, so the length is the
  longest that keeps three windows above the floor.
* **Length:** the notes say "3 windows of 2 months replace TabRed's single 4.5-month test period", so 2 months came
  from cutting TabReD's test period into three, not from how often a lender refits a scorecard, and no source states
  that cadence. The competition fits once and scores every week after its training data; its hosts changed the test
  "to better represent customer scoring in production. When a model runs in production, it can only see past
  performance and predictions." The length of its hidden test period could not be found. A scorecard serves for
  months, so the longer the window the closer to that use, as long as three windows stay above the floor: four months
  already puts the oldest window under it (49.0%)[^h-split14], and one month leaves April 2020 with 179 defaults.
  Your question on issue 1 ("does this time window make sense?") comes down to this length.
* **Gap:** none: the weekly default rate stays at 1.8% to 2.8% to the end of the release, so the labels look final,
  as for lt_vehicle_loan_default_prediction.
* **Time frame:** 1 January 2019 to 5 October 2020; half the applications lie before 11 October 2019; a break in
  late March 2020 (March 60,748 applications at 4.6% defaults, April 8,289 at 2.2%). Three-month windows spread over
  the release score a scorecard over a quarter, before, across and after the break; today's windows are three
  two-month stretches after it, all in the release's last five months.
* **Statistics:** three-month windows, from the definition's frame:

  | Window | In | Applications tested | Defaults | Train share |
  |---|---|---|---|---|
  | 6 July-5 October 2020 | B | 143,332 | 2.11% | 90.6% |
  | 1 March-31 May 2020 | B | 97,762 | 3.67% | 80.7% |
  | 1 November 2019-31 January 2020 | B | 328,606 | 3.66% | 54.3% |
  | today's three 2-month windows, May to 5 October 2020 | A | 74,687, 79,743, 70,497 | 2.4%, 2.1%, 2.2% | 85.3%, 90.2%, 95.4% |

* **Options:**

  | | Option | What it does | Test windows | Pro | Con |
  |---|---|---|---|---|---|
  | A | Two months (implemented) | issue 1's windows at two months | 3 windows (issue 1's B) of 69,037 to 241,856 applications | no change of length | a length cut from another benchmark's test period, not from the use |
  | B | Three months, spread | 6 July-5 October 2020, March-May 2020, November 2019-January 2020; candidates run from November 2019 (54.3% train share) to July 2020 (90.6%), 1,900 to 12,000 defaults each | 3 windows of 97,762 to 328,606 applications | the longest length above the floor; the months before, across and after the break | the oldest trains on 54.3%; issue 1's proposal is replaced |

* **Recommendation:** B: the longest length that keeps three windows above the floor is the closest to a scorecard
  used for months, and the spread covers the break. **Decision:** A or B?

**Notes for the AI:** on B, `temporal = Temporal(on="date_decision", splits=TemporalSplits(window=3, unit="months",
cutoffs=("2020-07-06", "2020-03-01", "2019-11-01")))`: test 143,332, 97,762 and 328,606 applications (all under the
500k budget), train 1,383,327, 1,232,695 and 828,906 (90.6%, 80.7%, 54.3%). Then resolve issue 1 with these windows,
rewrite `task_summary.split`, `splits_comment` (the windows and the reason from the Horizon block) and the metric
stand-in's "5-10 week" wording, a CC line in the record with the CC line that the declared horizon is checked, a
dated CHANGELOG entry, `dataset check`.

[^h-split14]: **SPLIT-14** (Must): at least 3 windows, and no window's train side holds less than 50% of the data.

**Lennart (2026-11-11, discuss):** Please explain the argument of the scorecard to me here

**Answer (AI, 2026-11-11):** The scorecard argument, and four months now that the floor is amended?

* **Problem:**
  - A credit scorecard is fit on applications whose default is known and then scores every new application until the
    next refit; Home Credit's competition ("Credit Risk Model Stability") fit one model and scored it on each week
    after its training data, rewarding a model whose quality decays least ("When a model runs in production, it can
    only see past performance and predictions").
  - So the horizon is how long one fit keeps scoring: the longer the window, the closer to that use; no source gives
    Home Credit's refit cadence, so the length is the longest that keeps the floor.
  - Under the amended floor (2026-11-11) four months gives three windows that all keep half the applications, and five
    months three with the oldest at 35.1%.
* **Options:**

  | | Option | What it does | Test windows | Pro | Con |
  |---|---|---|---|---|---|
  | a | Two months (implemented) | issue 1's windows | 3 windows of 69,037 to 241,856 applications | issue 1's choice | a length cut from another benchmark's test period |
  | b | Three months | 6 July-5 October 2020, March-May 2020, November 2019-January 2020 (90.6%, 80.7%, 54.3%) | 3 windows of 97,762 to 328,606 applications | before, across and after the March 2020 break | shorter than a scorecard's use |
  | c | Four months | July-5 October 2020, March-June 2020, November 2019-February 2020 (90.2%, 80.7%, 54.3%) | 3 windows of 143,724 to 403,789 applications | the longest length with every window above half; before, across and after the break | the windows tile the eligible span: no choice left |
  | d | Five months | June-5 October 2020, January-May 2020, August-December 2019 (87.1%, 70.1%, 35.1%) | 3 windows of 196,202 to 534,452 applications | the longest the amended floor admits | the oldest trains on 35.1% |

* **Recommendation:** c: a scorecard serves for months, and four months is the longest length whose three windows all
  keep half the applications. **Decision:** a, b, c or d?

**Issues for Lennart:**

1. **Which two-month windows: the three newest, or the newest, the change of March 2020 and the 2019 holidays?**

   * **Problem:**
     - The newest window (1 September to 5 October 2020) always stays, and since 2026-11-10 the other two are chosen
       from the use case and statistics of the data, preferring other years and seasons over the months just before
       the newest[^hc-split15].
     - Today's three windows (May to early October 2020) all fall after the change of late March 2020, when the
       applications dropped from 60,000-126,000 a month to 8,289 in April and the default rate fell from 4-5% to about
       2.2%, so they test one population three times.
     - A scorecard that should stay stable over time also has to hold through that change and in the busy months
       before it, which windows in March-April 2020 and November-December 2019 test.
   * **Background:**
     - By month the default rate is 2.6-3.3% from January to August 2019, 3.4-3.9% from September to December 2019
       and 4.1-4.7% from January to March 2020. By week it falls from 5.2% (the weeks of 3 and 10 March 2020) to 3.1%
       and 2.3% in the weeks of 24 and 31 March and stays at 1.8-2.8% until October. The applications fall at the
       same time, from 14,000-17,000 a week to 825-4,258 in April, and recover to 29,000-62,000 a month. Whether
       stricter approvals or payment holidays changed the population, the data does not say.
     - Two-month windows that keep at least half the applications for training start from 1 November 2019 (54.3%)
       to 1 September 2020[^hc-split14]; the length, two months for a scorecard refit every two months, stays as
       it is[^hc-split12].
     - Today's windows split TabReD's single test period (May to 5 October 2020), a choice of that benchmark; the
       competition's own test data are later and hidden.
     - PSI, the population stability index, compares a feature's distribution in the window with its train side.
       The largest PSI is 8.0 to 9.5 in every window, from `WEEK_NUM`, `MONTH` or a column of days to a response
       date, values that are always new, so the table gives the median over all 709 features. "New codes" is the
       largest share of the window's applications with a category code that no training row has, in any one column.
   * **Statistics:** defaults and applications from all rows; the median PSI from the candidate table (100,000-row
     samples of each side); the new codes counted on the full sides.

     | Window | In | Applications | Defaults | Train share | Median PSI | New codes |
     |---|---|---|---|---|---|---|
     | 1 Sep-5 Oct 2020 | A, B | 70,497 | 2.2% (1,521) | 95.4% | 0.071 | 0.2% |
     | Jul-Aug 2020 | A | 79,743 | 2.1% (1,654) | 90.2% | 0.073 | 4.5% |
     | May-Jun 2020 | A | 74,687 | 2.4% (1,763) | 85.3% | 0.060 | 53.0%, `description_5085714M` |
     | Mar-Apr 2020 | B | 69,037 | 4.3% (2,951) | 80.7% | 0.063 | 1.1% |
     | Nov-Dec 2019 | B | 241,856 | 3.5% (8,484) | 54.3% | 0.019 | 31.0%, `first_postype_4733339M` |

   * **Effect on the task:** Under A, the ROC AUC is measured three times on the population after the change, by
     models that trained mostly (85-95% of their rows) on the population before it. B keeps the newest window and
     adds one that runs through the change (March: 60,748 applications at 4.6% defaults; April: 8,289 at 2.2%) and
     one in the pre-COVID holiday season of 2019, the busiest two months of the data.
   * **Consistency:**
     - The note above `temporal` counts it against 5-month windows that the middle one "would span the April 2020
       drop in volume and default rate"; B puts a window on the drop on purpose, since the use case asks for a score
       that stays stable over time, and a break such as COVID-19 is what the history is checked for[^hc-split20].
     - aeolus_rebuilt_1m has the same question open under the rewritten rule; no dataset has decided under it yet.
   * **Sources:** the definition `datasets/_dev/tabarena-v0pt2/home_credit_default_stability_1m/dataset.py`
     (`temporal`, the note above it, `splits_comment`); the record `curation/records/home_credit_default_stability.md`;
     the candidate table `.venv/bin/python -m data_foundry.curation.cli dataset windows
     home_credit_default_stability_1m --root datasets/_dev/tabarena-v0pt2 --step 1` (11 windows, November 2019 to
     September 2020).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Three newest windows (implemented) | tests 1 Sep-5 Oct, Jul-Aug and May-Jun 2020 | the months closest to deployment; the population the newest window shows | one population three times (2.1-2.4% defaults); no window before or through the change of March 2020 |
     | B | Newest, the change, the 2019 holidays | tests 1 Sep-5 Oct 2020, Mar-Apr 2020 and Nov-Dec 2019 | scores the model before, through and after the change; another year and season; the windows start 4 and 6 months apart | the oldest window trains on 54.3% of the applications (10 months); Mar-Apr mixes two populations in one score |

   * **Recommendation:** B: the use case asks the scorecard to stay stable over time, and the largest change in the
     data, late March 2020, is the one a refit cannot see coming; B tests before, through and after it, where A tests
     three times after it. **Decision:** A or B?

   **Notes for the AI:** on B, `temporal = Temporal(on="date_decision", splits=TemporalSplits(window=2,
   unit="months", cutoffs=("2020-09-01", "2020-03-01", "2019-11-01")))`. Built with `TemporalSplits.splits` on the
   definition's frame: test 70,497, 69,037 and 241,856 applications (all kept, under the 500k budget), train
   1,456,162, 1,232,695 and 828,906 (95.4%, 80.7%, 54.3%). The default 1M sample then takes all 828,906 rows of the
   10 months before November 2019, a random 1M of the 1,094,102 rows of the year before March 2020, and the 12 to 14
   months before September 2020 as now. Rewrite `task_summary.split` ("from May to early October 2020", "the newest
   12 to 14 months"), `splits_comment` (the windows, the reasons and the numbers above, in place of "We follow
   TabRed's test period"; the train sides become 0.83M to 1.46M) and the note above `temporal`; add a CC line to the
   record and a dated CHANGELOG entry, and run `dataset check` (SPLIT-15, SPLIT-20). On A, write the reason into
   `splits_comment`: the three newest windows test the months after the change of March 2020, closest to
   deployment.

   [^hc-split15]: **SPLIT-15** (Must for the newest window, Should for the others; amended 2026-11-10, Lennart and
     Andrej): "The newest window is always a test window ... The other windows are the curator's choice, per dataset,
     argued from the use case ... The evidence is statistics of the data, never a model's score ... Prefer windows in
     other years, then other seasons, then other months, weeks or days, over the windows just before the newest."
   [^hc-split14]: **SPLIT-14** (Must): at least 3 windows, and no window's train side holds less than 50% of the
     data.
   [^hc-split12]: **SPLIT-12** (Should): the horizon is a human judgment from the source, such as the refit cadence.
   [^hc-split20]: **SPLIT-20** (Should): decide the history from the use case; "check the history for breaks
     (COVID-19, a change of rules or of the data collection)".

   **Lennart (2026-11-10, discuss):** does this time window make sense?

   **Answer (AI, 2026-11-10):**
   - Not as declared: the 2 months came from cutting TabReD's 4.5-month test period into three windows, not from a refit
     cadence, and no source states one (the Horizon block above).
   - The horizon sign-off (H) proposes 3 months, the longest length that keeps three windows above the floor; this
     issue waits on it and its windows are proposed again at the length you choose.

   **Answer (AI, 2026-11-11):**
   - The windows follow the length you choose in the horizon sign-off (H), which explains the scorecard argument and
     adds four and five months under the amended floor; at three, four or five months exactly three windows remain,
     so this issue closes with H's choice.
