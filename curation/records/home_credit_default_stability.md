---
unique_name: home_credit_default_stability
name: Homecredit Default
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
priority: 3
tags:
- Non-IID (Temporal)
collections:
- TabArena Reject
- TabRed
original_source: Kaggle
year: '2024'
domain: finance
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.kaggle.com/competitions/home-credit-credit-risk-model-stability
- https://github.com/yandex-research/tabred/tree/main/preprocessing#homecredit-default-stability-homecredit-20
notebook_path: datasets/beyond_iid/temporal/home_credit_default_stability/home_credit_default_stability_1m.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/home_credit_default_stability_1m/dataset.py
source_row: 710
type_adapter_id: curation-record-v1
---

## Comments

Follow the preprocessing from TabRed as well. Verify that TabRed preprocessing gets similar feature sets to top solutions

Kaggle solutions used IID CV splits. There is also a problem with metric hacking on the Kaggle submissions.

TabRed uses 4/5 month as time horizon

CC (2026-10-21, Lennart): the declared metric documents the original use case's metric; overrule it only when it is biased or wrong (evidence from the paper); keep the note of the original metric (TP-6 amended).

**Assessment (AI, 2026-10-21):** metric stays the default `roc_auc`: the competition scored "Home Credit 2023 - Gini Stability" (Kaggle API), the mean weekly Gini with a penalty for a falling trend and for the spread around it; it needs the week of each row and is no listed metric, and ROC AUC is the per-week score it is built from (definitions.md, Field mapping, rule 4). The notes now name the original. Needs a rebuild to reach the container (notes only).

CC (2026-10-21, Lennart): "yes we should have one clear way to treat 0/1 flags": every 0/1 flag (a feature holding only 0 and 1, plus missing values; booleans too) is categorical (CLEAN-14, amended). Typed categorical here: isbidproduct_1095L (boolean) and 5 aggregates that hold only 0 and 1 (found on the data in `_feature_types`).

CC (2026-10-21, Lennart): on which 0/1 columns are flags: "no if we can infer from the semantic context, keep it a number, this is a real-world bias. We want to make things categorical if we know from the context they are indeed such" (CLEAN-14, amended again). Kept categorical: isbidproduct_1095L (explicit). Reverted: posfpd10lastmonth_333P, posfpd30lastmonth_3976960P, posfstqpd30lastmonth_3976962P, mean_contaddr_smempladdr_334L, mean_safeguarantyflag_411L (aggregates) stay numeric.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: stand_in roc_auc — stands in for Home Credit 2023 - Gini Stability: mean weekly Gini + 88 * min(0, slope) - 0.5 * std(residuals): Our test windows hold 5, 9 and 10 weeks (week 78 split between two windows, week 69 partial); the weekly Gini has SE about 0.04, so the 88 x slope term has SE about 1.2 / 0.5 / 0.43, larger than the Gini differences between methods: per window the score is noise (MET-2). ROC AUC per window is the per-week building block. (https://www.kaggle.com/competitions/home-credit-credit-risk-model-stability/overview/evaluation).

CC (2026-10-21, Lennart): the metric is roc_auc as a stand-in for the competition's Gini Stability, whose slope term is noise on our 5-10 week test windows.

**Assessment (AI, 2026-10-27):** no `Anonymized` marker (review of PR #17). Kaggle masked the values of the columns ending in `M` (116 of the 718 merged columns: district, zip code, employer, education, contract status, reject and cancel reasons), but every column is described in the competition's `feature_definitions.csv`, so what a column measures and when it is known can be checked; other categories are readable (`OWNED`, `MARRIED`). This is the selection.md case of documented columns with coded category values, as amazon_employee_access. The definition's `known` now says which categories are masked instead of "the categories are anonymized codes".

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): 1 ordinal scales typed as ordered categories in the codebook's order (CLEAN-14, amended): `first_empl_employedtotal_800L` (the README lists their levels); codes shipped as numbers, left for the curator's review: `max_persontype_1072L`.

CC (2026-10-31, Lennart): marks on the review board of PR #37 (ordinal scales in the codebook's order, also when shipped as numbers; a state outside a scale missing when the column has no other missing value, else the lowest level; cycles ordered; codes shipped as numbers as categories): max_persontype_1072L a category.

CC (2026-11-01, Lennart): the target rule (CLEAN-25) and the cut-end rule (CLEAN-14): the target ships as No/Yes, Yes the event (1 is the event).

**Assessment (AI, 2026-11-10):** priority for the review of the test windows (PR #78), which this record never had. Priority 3: gap 0, use case 0 (the fit is approximate), source + (Home Credit's competition), shape +, risk 0 (the open issue is the choice of windows).

CC (2026-11-11, Lennart): Review issue 1 ("Agree.", to the answer that the windows follow the length of the horizon sign-off): the test windows are July to 5 October 2020, March to June 2020 and November 2019 to February 2020, after, across and before the drop of late March 2020, in place of the three two-month windows from May 2020.

CC (2026-11-11, Lennart): the declared horizon (4 months, no gap, windows starting 2020-07-01, 2020-03-01 and 2019-11-01) is checked, as a scorecard serves for months between refits and no source gives Home Credit's cadence, so the window is the longest whose three windows all keep half the applications for training (Review horizon, c: "Reply (c): Four months").

**Assessment (AI, 2026-11-11):** applied the horizon (c) and issue 1: `temporal` declares `TemporalSplits(window=4, unit="months", cutoffs=("2020-07-01", "2020-03-01", "2019-11-01"))`. Test 150,240, 143,724 and 403,789 applications (3,175, 4,714 and 15,541 defaults; 2.1%, 3.3%, 3.8%), all kept under the 500k test budget; train 1,376,419, 1,232,695 and 828,906 (90.2%, 80.7%, 54.3% of 1,526,659), so no window trains on less than half. The default 1M sample takes the newest 1M rows before July 2020 (from 11 June 2019; the year before holds 937,675), a random 1M of the 1,094,102 of the year before March 2020, and all 828,906 before November 2019. The windows hold 14, 19 and 18 weeks of WEEK_NUM; the Gini Stability's 88 x slope term has SE about 0.23, 0.17 and 0.08 there (Hanley-McNeil at an AUC of 0.8), about 20 times the SE of the mean weekly Gini, so the ROC AUC stand-in's reason holds and now gives these figures in place of "5-10 week". `dataset check`: 0 errors, 0 warnings.

CC (2026-11-11, Lennart): accepted `splits_feature_missing_in_test` with a note naming the columns (cross-dataset item "Accept splits_feature_missing_in_test where a column starts or stops being recorded within the history?", A: the data as the deployed model met it).

**Assessment (AI, 2026-11-11):** 12 columns recorded for 65% to 99% of the decisions until August 2019 stop by November 2019; 15 start in April to June 2020 (53% to 99% recorded from July 2020).

## Review

**Outcome:** added as `home_credit_default_stability_1m`. On 2026-11-11 you chose four-month windows (H, c), which
also settles the windows (issue 1): July to 5 October 2020, March to June 2020 and November 2019 to February 2020,
each trained on at least half the applications; both are applied and nothing is left open.

**Main points:** Settled on 2026-11-11: three four-month test windows after, across and before the drop of late March
2020, as a scorecard serves for months between refits.

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

**Lennart (2026-11-11, discuss):** Reply (c): Four months

**Resolved (2026-11-11, Lennart):** c, four-month windows with no gap: a scorecard serves for months between refits,
no source gives Home Credit's cadence, and four months is the longest length whose three windows all keep half the
applications for training. `temporal` declares `TemporalSplits(window=4, unit="months", cutoffs=("2020-07-01",
"2020-03-01", "2019-11-01"))`: test 150,240, 143,724 and 403,789 applications (3,175, 4,714 and 15,541 defaults), all
under the 500k test budget; train 1,376,419, 1,232,695 and 828,906 (90.2%, 80.7%, 54.3%), so no window is under half.
`task_summary.split` and `changes`, `splits_comment` (the length's reason from this block, the windows, the counts, the
default 1M sample), the note above `temporal`, the metric stand-in's reason (14, 19 and 18 weeks, where the slope term's
SE is 0.23, 0.17 and 0.08, in place of "5-10 week") and its curation note are rewritten. The record has the horizon CC
line. `dataset check`: 0 errors, 0 warnings (README not regenerated).

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

   **Lennart (2026-11-11, discuss):** Agree.

   **Resolved (2026-11-11, Lennart):** closed with the horizon's choice (c): the test windows are July to 5 October
   2020, March to June 2020 and November 2019 to February 2020, after, across and before the drop of late March 2020,
   which at four months tile the months from the oldest start that keeps half the applications to the release end.
   The same edits as the horizon's (`temporal`, `task_summary.split`, `splits_comment`, the note above `temporal`);
   the record has the CC line. `dataset check`: 0 errors, 0 warnings.

## Reference

Daniel Herman, Tomas Jelinek, Walter Reade, Maggie Demkin, and Addison Howard. Home Credit - Credit Risk Model Stability. https://kaggle.com/competitions/home-credit-credit-risk-model-stability, 2024. Kaggle.
