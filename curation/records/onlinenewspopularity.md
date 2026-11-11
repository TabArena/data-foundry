---
unique_name: onlinenewspopularity
name: OnlineNewsPopularity
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
suggestion: 'Yes'
priority: 2
decision_markers:
- Wrong Domain / Source Modality
- NLP (Text)
tags:
- Non-IID (Temporal)
collections:
- TabArena Reject
- TabSTAR
- AutoML_MM
- MulTaBench
original_source: UCI
year: '2015'
required_split:
- Temporal (NON-IID)
problem_type: Regression
source_links:
- https://doi.org/10.24432/C5NS3V
- https://www.semanticscholar.org/paper/A-Proactive-Intelligent-Decision-Support-System-for-Fernandes-Vinagre/ad7f3da7a5d6a1e18cc5a176f18f52687b912fea
- https://www.openml.org/search?type=data&id=46652&sort=runs&status=active
- https://www.openml.org/search?type=data&id=46662&sort=runs&status=active
- https://www.openml.org/search?type=data&id=4545&sort=runs&status=active
v2_path: datasets/_dev/tabarena-v0pt2/onlinenewspopularity/dataset.py
source_row: 720
type_adapter_id: curation-record-v1
---

## Comments

CC: "Predict how often news were shared from statistics. Actually might be an NLP task, but could as well be still solved as a tabular data task; temporal impact as platform might grow over time. Some features are from LDA which likely introduced leaks making the dataset be unusable with random splits"

In TabArena was rejected due to text and temporal. But it might still be a valid task nowadays and is not that old. 

Might be a cool text-based task if we get the original text (or parts of it), plus using a subset of the features?
From researching, it seems the raw data is not published."

"we performed a
robust rolling windows evaluation of five state of the art models"
"For the prediction experiments, we adopted the rolling windows scheme with
a training window size of W = 10, 000 and performing L = 1, 000 predictions at each iteration. Under this setup, each classification model is trained
29 times (iterations), producing 29 prediction sets (each of size L). For defining
a popular class, we used a fixed value of D1 = 1, 400 shares, which resulted
in a balanced "popular"/"unpopular" class distribution in the first training set
(first 10, 000 articles)."

I think we cannot get the original text but this is still fine. It is not too old and it had some well made features that might even beat LLM preprocessing or be used next to it. Thus I think we can add it as a good temporal dataset!

**Assessment (AI, 2026-10-07):** Added as a temporal regression of log shares (9 two-week windows, Aug-Dec 2014, one-week gap), after the paper's rolling test sets of 1,000 articles (Sec. 3.1). UCI's `timedelta` and weekday flags follow a date 1-5 days after the publication date in the URL for 24% of the articles (Mashable's archived pages carry the URL date) and raise LightGBM's R² from 0.158 to 0.166: dropped. The LDA columns come from one model fitted on all texts and carry no signal: dropped. The keyword statistics of shifted articles include same-day articles published later (no measurable gain): kept with a note. Text-derived columns add 0.003 R². Binary framing (shares ≥ 1,400): ROC AUC 0.733 (paper: 0.73).

**Assessment (AI, 2026-10-20):** priority 2 for the review of the added dataset: gap -, use case -, source +, shape +, risk - (Issues 5, 6: keyword and self-reference statistics kept as potential leaks using crawl-time share counts). Temporal regression on a documented source, but weak signal (R2 0.16) and kept potential leaks make it a modest addition.

**Assessment (AI, 2026-10-20):** re-checked by the review panel: ship after changes, now made in the definition (the `known` wording names the crawl-time counts, the 1.59 share count is masked, `rate_negative_words` dropped as a copy, the notes give the 9-window figures). Masking the keyword and self-reference counts traced to articles under 8 days older changes R² by -0.0004 (0.1553 to 0.1549), so they stay with a note; keeping them needs a LEAK-10 amendment (Review issue 5). The release holds no text: the 19 text-derived columns add 0.004 R² and the slug's TF-IDF lowers it, which does not bear out `Wrong Domain / Source Modality` (issue 8). Priority 2: gap -, use case - (fit approximate: one crawl date, crawl-time counts), source + (the EPIA 2015 paper and UCI's page), shape +, risk - (the kept crawl-time counts await the LEAK-10 amendment, issue 5).

CC (2026-10-21, Lennart): ok on the follow-up item: a strong kept leak does not make the fit approximate (USE-8 amended); the kept leak is named in `fit_reason` as kept, not as a gap.

**Assessment (AI, 2026-10-21):** fit set to `direct`; the two kept crawl-time leaks (R² 0.158 with both, 0.135 and 0.143 without each) are named in `fit_reason` as kept; the Review outcome and issue 5 updated.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback rmse — The paper scores a binary task (shares >= 1,400 threshold) with accuracy/F1/AUC; we ship a regression on log shares, so the original target is not ours; rmse on the log target is the regression fallback.

**Assessment (AI, 2026-10-21):** metric now `Metric.from_context("rmsle", target_transform="log")` instead of the fallback rmse on the log target: shares are a heavy-tailed count (1 to 843,300) whose error matters relative to the count; the target still ships as log, and RMSLE is computed after the inverse, on the original scale (MET-3). Needs a rebuild to reach the container.

CC (2026-10-21, Lennart): ship the target on the modelling scale, score on the original scale (target_transform).

**Assessment (AI, 2026-10-22):** CLEAN-13 was amended on mortgage's issue 12 (Lennart, 2026-10-22): a block with at most one flag set merges with a reference level, so `data_channel` (`other` when no flag is set) now meets the rule as written; a Cases row names both datasets.

CC (2026-10-26, Lennart): issue 8: keep the `Wrong Domain / Source Modality` and `NLP (Text)` markers, "to make clear that the original task behind this dataset would likely nowadays not be solved with tf-idf but raw embeddings with LLMs or similar. we can still keep the dataset for now as it is fine, but it is not perfect".

CC (2026-10-26, Lennart): issue 9: keep `data_channel` merged; CLEAN-13 as amended on 2026-10-22 (mortgage's issue 12: exactly one flag, or at most one with a reference level) covers it.

**Assessment (AI, 2026-10-26):** issues 8 and 9 are settled. Issue 5 waits for the wording of a LEAK-10 amendment (consistency check); issue 10 answers the question on the target: the source's decision acts on a score, its 1,400-share cut was set for class balance, and the regression ranks the articles as well as a classifier (ROC AUC 0.727 against 0.730 on the paper's label). The texts now say more than 1,400 shares, as the paper does.

CC (2026-10-26, Lennart): issue 5: "go with (a)": LEAK-10 and LEAK-6 amended for values read at a later pull whose late cells cannot be located row by row: they stay with a note only when the traceable part shows no gain; located cells are blanked.

CC (2026-10-26, Lennart): issue 10: "oke keep regression": the share count stays the target, RMSLE as declared.

**Assessment (AI, 2026-10-26):** both settled; no open issue is left, so the folder's REVIEW.md is removed.

CC (2026-10-26, Lennart): verdict ship.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `news_popularity_multiple_social_media` (TBD -> Yes, priority 2). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-11, Lennart): REVIEW issue 11 (which two-week windows), B ("Option B: One window every five weeks."), with nine windows ("Reply (a): Nine, every five weeks (your B)" to the AI's answer on more windows): nine two-week windows, one every five weeks from 9 March to 27 December 2014, with the one-week gap, in place of the newest nine (24 August to 27 December 2014), so the test covers spring, summer, autumn and early winter of 2014. Every train side keeps more than half the articles (53.6% to 96.8%).

CC (2026-11-11, Lennart): the declared horizon (2 weeks, a one-week gap, windows starting 2014-12-14, 2014-11-09, 2014-10-05, 2014-08-31, 2014-07-27, 2014-06-22, 2014-05-18, 2014-04-13 and 2014-03-09) is checked, as two calendar weeks are the calendar form of the paper's rolling test sets of 1,000 articles and the gap is longer than the under four days the paper gives shares to settle.

**Assessment (AI, 2026-11-11):** applied in dataset.py: `temporal` declares the nine cutoffs (2 weeks, gap 1 week); test 769, 1,003, 988, 902, 877, 855, 763, 785 and 699 articles (7,641), train 38,385, 36,031, 33,583, 31,354, 29,269, 27,020, 24,996, 23,035 and 21,234 (96.8% to 53.6% of 39,643); mean log shares 7.37 to 7.45 in the windows of June to December and 7.53 to 7.60 in those of March to May. The articles with the shifted authors' date are 3,880 of the 7,641 test articles (51%; 6,627 of 8,289, 80%, on the newest nine). The 489 articles of 7-13 December 2014 fall in the newest window's gap and in no test window; `accepted_check_warnings` accepts `splits_rows_unused` with that reason. `task_summary.split` and `splits_comment` are rewritten; the figures of `fit_reason` and `curation_comments` measured on the newest nine windows (R² 0.158, 0.135 and 0.143; ROC AUC 0.727 against 0.730; the masking test; the 0.9% and 0.4% of test rows; expanding against sliding) are dated as measured on the windows used until 2026-11-11, not measured again; `fit_reason` drops its rule reference to stay under 70 words. `dataset check`: 0 errors, 0 warnings (README not regenerated).

CC (2026-11-11, Lennart): accepted `splits_feature_missing_in_test` with a note naming the columns (cross-dataset item "Accept splits_feature_missing_in_test where a column starts or stops being recorded within the history?", A: the data as the deployed model met it).

**Assessment (AI, 2026-11-11):** `kw_min_min` is missing for 0% to 2% of the articles in 2013 Q1-Q3, 35% in Q4 and 100% in 2014.

## Review

**Outcome:** added. On 2026-11-11 you chose nine two-week windows, one every five weeks from 9 March to 27 December
2014, with the one-week gap (issue 11, B, nine windows by reply (a)), every train side above half, and kept the
two-week horizon (Horizon, A).

**Main points:** Settled on 2026-11-11: nine windows spread over March to December 2014 (issue 11) and the two-week
horizon with its one-week gap. Nothing is left open.

**Horizon:**

* **Verdict:** keep the two-week windows with the one-week gap (medium confidence): two weeks are the calendar form of
  the paper's rolling test sets of 1,000 articles, and the gap is longer than the time the paper gives shares to settle.
* **Length:** declared two calendar weeks (Sunday to Saturday). The paper: "we adopted the rolling windows scheme with
  a training window size of W = 10, 000 and performing L = 1, 000 predictions at each iteration. Under this setup,
  each classification model is trained 29 times" (Fernandes, Vinagre and Cortez 2015, Sec. 3.1,
  https://doi.org/10.1007/978-3-319-23485-4_53; quoted in the record). 1,000 articles are about 2.2 weeks of
  Mashable's output in late 2014 (about 450 a week) and 2.8 weeks in 2013. The editor scores an article just before
  it is published, so the window says how long one fitted model serves, which the paper sets through L; it states no
  refit cadence in days.
* **Gap:** one week. The labels are the shares at the crawl of 8 January 2015 for training and test rows alike, so
  the gap only stands in for the time young articles' shares take to settle: under four days in the paper (Sec. 2.1,
  as the definition cites it), which also dropped the articles under three weeks old.
* **Time frame:** articles from 7 January 2013 to 27 December 2014. The paper's 29 test sets hold the articles after
  the first 10,000, about 16 July 2013 to mid-December 2014 by the URL date. Two-week windows keep half the articles
  for training back to 23 February 2014 (22 candidates, 51.8% to 96.8%). Off: Mashable's output grew from about 1,500
  articles a month in 2013 to 2,215 in October 2014, and the authors' date runs after the URL date for a growing
  share of the articles (13% in April 2014, all from November 2014 on), which the definition already handles.
* **Options:**

  | | Option | What it does | Test windows | Pro | Con |
  |---|---|---|---|---|---|
  | A | Two weeks, one-week gap (implemented) | two-week windows (Sunday to Saturday), each a week after its train side: 22 candidates above the floor, back to 23 February 2014 (51.8% to 96.8%) | 9 windows of 769 to 1,001 articles (issue 11's B: 9 of 699 to 1,003) | the calendar form of the paper's test sets of 1,000 articles (about 2.2 weeks in late 2014); the gap is longer than the under four days the paper gives shares to settle | not the paper's L exactly (1,000 articles are 2.8 weeks in 2013); the paper states no refit cadence in days |
  | B | 1,000 articles | `unit="rows"`, the paper's L exactly: about 19 windows above the floor | 19 candidates above the floor, 1,000 articles each | the paper's own test set size | windows of uneven calendar length |
  | C | One week | about 450 articles per window | 45 candidates above the floor, 313 to 516 articles each | twice as many candidates | no source; half the paper's test set |
  | D | Four weeks | 11 candidates above the floor | 11 candidates above the floor, 1,398 to 1,989 articles each | more articles per window | twice the paper's test set; half as many candidates |

* **Recommendation:** A: two calendar weeks are the paper's test set of 1,000 articles in late 2014, in whole weeks, and
  the one-week gap covers the time the paper gives shares to settle. **Decision:** A, B, C or D?

**Lennart (2026-11-11, ok):** As implemented (A).

**Resolved (2026-11-11, Lennart):** A, two-week windows with the one-week gap, kept: two calendar weeks are the
calendar form of the paper's rolling test sets of 1,000 articles (about 2.2 weeks in late 2014), and the gap is longer
than the under four days the paper gives shares to settle. `splits_comment` gives these reasons; the windows are issue
11's B. The record has the horizon CC line. `dataset check`: 0 errors, 0 warnings (README not regenerated).

**Issues for Lennart:**

11. **Which two-week windows should the test windows be?**

   * **Problem:**
     - The nine test windows are the newest 18 weeks (24 August to 27 December 2014), while windows that keep half
       the articles for training reach back to February 2014 and the paper's own rolling test sets ran from July 2013
       to December 2014.
     - Since 2026-11-10 the newest window always stays and the others are chosen from the use case and statistics of
       the data, and walking back from the newest needs its own reason[^onp-split15].
     - The mean log shares falls through 2014, from 7.53 to 7.60 in the windows of March to May to 7.31 to 7.44 in
       today's windows, so the newest 18 weeks test the low end of the year.
   * **Background:** B places a two-week window every five weeks from 9 March to 27 December 2014, so the test
     covers spring, summer, autumn and early winter of 2014; two of its windows (14-27 December and 5-18 October) are
     also in A. The articles whose authors' date runs after the URL date have keyword statistics that include
     same-day articles published later, a potential leak kept with a note; they are 80% of A's test articles (6,627
     of 8,289) and 51% of B's (3,880 of 7,641). PSI, the population stability index, compares a feature's
     distribution in the window with its train side (above 0.25 is usually read as a large shift); one keyword
     statistic, `kw_min_min`, drifts in every window (3.6 to 6.2) and more the older the window, while the median
     over the features is 0.05 to 0.13.
   * **Statistics:** from the candidate tables (all rows; the target is the natural log of the shares).

     | Window | In | Articles | Mean log shares, test | Train side | Train share | Largest PSI (`kw_min_min`) | Median PSI |
     |---|---|---|---|---|---|---|---|
     | 14-27 Dec 2014 | A, B | 769 | 7.41 | 7.48 | 96.8% | 3.60 | 0.13 |
     | 9-22 Nov 2014 | B | 1,003 | 7.40 | 7.49 | 90.9% | 3.89 | 0.10 |
     | 5-18 Oct 2014 | A, B | 988 | 7.37 | 7.49 | 84.7% | 4.24 | 0.09 |
     | 31 Aug-13 Sep 2014 | B | 902 | 7.41 | 7.50 | 79.1% | 4.62 | 0.09 |
     | 27 Jul-9 Aug 2014 | B | 877 | 7.39 | 7.50 | 73.8% | 5.03 | 0.07 |
     | 22 Jun-5 Jul 2014 | B | 855 | 7.45 | 7.50 | 68.2% | 5.57 | 0.05 |
     | 18-31 May 2014 | B | 763 | 7.57 | 7.50 | 63.1% | 6.17 | 0.05 |
     | 13-26 Apr 2014 | B | 785 | 7.53 | 7.50 | 58.1% | 5.55 | 0.05 |
     | 9-22 Mar 2014 | B | 699 | 7.60 | 7.49 | 53.6% | 6.21 | 0.05 |
     | A's other seven, 24 Aug-13 Dec 2014 | A | 875 to 1,001 each | 7.31 to 7.44 | 7.48 to 7.50 | 78.1% to 94.7% | 3.70 to 4.69 | 0.08 to 0.13 |

   * **Effect on the task:** A ranks the models on autumn 2014 alone, the months with the lowest shares and the
     most articles with a shifted authors' date. B scores a model refit every two weeks across ten months of 2014, so
     the score also covers spring's higher share level and the summer, as the paper's rolling evaluation does, with
     smaller train sides for the older windows (53.6% for March).
   * **Consistency:** the length already follows the paper's test sets; the paper's test period spans July 2013 to
     December 2014, which B follows more closely within the floor[^onp-split19]. aeolus (one window in the holiday
     peak, Lennart 2026-10-12) and airqo (windows over both seasons, Lennart 2026-11-05) spread their windows over
     seasons[^onp-split20].
   * **Sources:** the paper (https://doi.org/10.1007/978-3-319-23485-4_53, Sec. 3.1 as quoted in the record); UCI's
     page (https://doi.org/10.24432/C5NS3V); the definition `datasets/_dev/tabarena-v0pt2/onlinenewspopularity/dataset.py`
     (`temporal`, `splits_comment`, `fit_reason`, `curation_comments`); the record
     `curation/records/onlinenewspopularity.md`; the candidate tables `.venv/bin/python -m data_foundry.curation.cli
     dataset windows onlinenewspopularity --root datasets/_dev/tabarena-v0pt2` (22 windows) and the same with
     `--step 5` (B's windows); the shifted dates from the release's `timedelta` against the URL date.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Newest nine windows (implemented) | tests the two-week windows from 24 Aug to 27 Dec 2014 | the largest train sides (78% to 97%); the notes' figures were measured on these windows | one season of one year; the lowest share level of 2014; 80% of the test articles carry the shifted authors' date |
     | B | One window every five weeks | tests nine two-week windows from 9 Mar to 27 Dec 2014, five weeks apart | spring, summer, autumn and early winter; closer to the paper's rolling evaluation; 51% of the test articles carry the shifted date | the oldest trains on 53.6%; 648 fewer test articles (7,641); the notes' figures need measuring again |

   * **Recommendation:** B: nothing in the use case ties the editor's model to the autumn, the paper evaluates over
     17 months, and five-week spacing covers the seasons the floor leaves open while every train side keeps more than
     half the articles. **Decision:** A or B?

   **Notes for the AI:** on B, `temporal = Temporal(on="publication_date", splits=TemporalSplits(window=2,
   unit="weeks", gap=1, cutoffs=("2014-12-14", "2014-11-09", "2014-10-05", "2014-08-31", "2014-07-27", "2014-06-22",
   "2014-05-18", "2014-04-13", "2014-03-09")))`. Built with `TemporalSplits.splits` on the definition's frame (39,643
   articles): test 769, 1,003, 988, 902, 877, 855, 763, 785 and 699 articles, train 38,385, 36,031, 33,583, 31,354,
   29,269, 27,020, 24,996, 23,035 and 21,234 (96.8% to 53.6%); each train side ends 8 days before its window. Then
   rewrite `task_summary.split` ("two weeks of articles (24 August to 27 December 2014)"), `splits_comment` (the
   windows, the reasons and the numbers above, in place of "from 2014-08-24 to 2014-12-27 ... 78% of the data or
   more"), and the figures measured on today's nine windows in `fit_reason` and `curation_comments` (R² 0.158, 0.135
   and 0.143; 80% of the test rows, 6,627 of 8,289, which becomes 3,880 of 7,641; the masking test, -0.0004; ROC AUC
   0.727 against 0.730; the 0.9% and 0.4% of test rows): measure them again on the new windows or date them as
   measured on the windows of October 2026. Add a CC line to the record and a dated CHANGELOG entry, and run `dataset
   check` (SPLIT-15, SPLIT-19).

   [^onp-split15]: **SPLIT-15** (Must for the newest window, Should for the others; amended 2026-11-10, Lennart and
     Andrej): "The newest window is always a test window ... Prefer windows in other years, then other seasons, then
     other months, weeks or days, over the windows just before the newest. Walking back from the newest is one choice
     among others and needs its reason too, such as a history too short for others, or a use case that only cares
     about the weeks after a refit."
   [^onp-split19]: **SPLIT-19** (Should): "When the source defines the split (a competition's or a paper's official
     periods), follow it. A prescribed split is still a claim to check."
   [^onp-split20]: **SPLIT-20** (Should), cases: aeolus, "two-week windows with one of three in the holiday peak
     (2026-10-12, Lennart)"; airqo_low_cost_air_quality_monitor_calibration_challenge, "five monthly windows from
     October 2020 ... so the test covers both seasons" (2026-11-05, Lennart, issue 1).

   **Lennart (2026-11-11, change):** Option B: One window every five weeks. ; we could also use more windows?

   **Answer (AI, 2026-11-11):** Keep nine windows, or test more of the two-week windows the amended floor admits?

   * **Problem:**
     - Two-week windows with the one-week gap give 22 candidates whose train side holds at least half the articles, and
       12 more down to 30% that the amended floor admits[^a-14].
     - A random split of 39,643 articles gets 3 repeats of 3 folds, nine splits, which is what B's nine windows match.
     - More windows test more weeks of the year but repeat a fit for each, and neighbouring windows hold similar weeks.
   * **Options:**

     | | Option | What it does | Test windows | Pro | Con |
     |---|---|---|---|---|---|
     | a | Nine, every five weeks (your B) | 9 March to 27 December 2014 | 9 of 699 to 1,003 articles | as many splits as a random split of this size; spread over the year | nine of the 22 weeks above half |
     | b | Seventeen, about every three weeks | down to the 30% bound, 17 windows | 17 of about 700 to 1,000 articles | almost twice the test articles; every season more than once | nearly twice the fits; neighbouring windows alike |

   * **Recommendation:** a: nine windows already match a random split of this size and cover the year.
     **Decision:** a or b?

   [^a-14]: **SPLIT-14** (Must; amended 2026-11-11, Lennart): the newest window and at least one other train on at least 50% of the data; further windows down to 30%, and at most as many windows under 50% as at or above it.

   **Lennart (2026-11-11, change):** Reply (a): Nine, every five weeks (your B)

   **Resolved (2026-11-11, Lennart):** B with nine windows: `temporal` declares the cutoffs 2014-12-14, 2014-11-09,
   2014-10-05, 2014-08-31, 2014-07-27, 2014-06-22, 2014-05-18, 2014-04-13 and 2014-03-09 (two weeks, one-week gap):
   test 769, 1,003, 988, 902, 877, 855, 763, 785 and 699 articles (7,641), train 38,385 down to 21,234 (96.8% to
   53.6%), so every train side keeps half and no window needs a sign-off. The 489 articles of 7-13 December 2014 fall
   in the newest window's gap and in no test window: `accepted_check_warnings` accepts `splits_rows_unused` with that
   reason. `task_summary.split` and `splits_comment` (the windows, why, the counts and shares) are rewritten. The
   figures of `fit_reason` and `curation_comments` measured on the newest nine windows (R² 0.158, 0.135 and 0.143; ROC
   AUC 0.727 against 0.730; the masking test; the 0.9% and 0.4% of test rows; expanding against sliding) are dated as
   measured on the windows used until 2026-11-11; the share of test articles with the shifted authors' date is now 51%
   (3,880 of 7,641). The record has the decision and the horizon CC lines. `dataset check`: 0 errors, 0 warnings
   (README not regenerated).

## Reference

A Proactive Intelligent Decision Support System for Predicting the Popularity of Online News
By Kelwin Fernandes, Pedro Vinagre, P. Cortez. 2015

Published in Portuguese Conference on Artificial Intelligence
