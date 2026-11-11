# onlinenewspopularity

**Outcome:** added. Under the rule on choosing test windows, rewritten on 2026-11-10, the AI proposes to keep the
two-week windows and the one-week gap, but to spread the nine windows over March to December 2014, one every five
weeks, instead of testing the newest nine (24 August to 27 December 2014) (issue 11): the paper evaluated on rolling
test sets over 17 months, and the share level falls through 2014. `dataset.py` is unchanged until you decide.

**Main points:** Test on nine two-week windows spread over March to December 2014 instead of the newest nine
(issue 11)? Sign off the two-week horizon with its one-week gap.

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

  | | Option | What it does | Pro | Con |
  |---|---|---|---|---|
  | A | Two weeks, one-week gap (implemented) | two-week windows (Sunday to Saturday), each a week after its train side: 22 candidates above the floor, back to 23 February 2014 (51.8% to 96.8%) | the calendar form of the paper's test sets of 1,000 articles (about 2.2 weeks in late 2014); the gap is longer than the under four days the paper gives shares to settle | not the paper's L exactly (1,000 articles are 2.8 weeks in 2013); the paper states no refit cadence in days |
  | B | 1,000 articles | `unit="rows"`, the paper's L exactly: about 19 windows above the floor | the paper's own test set size | windows of uneven calendar length |
  | C | One week | about 450 articles per window | twice as many candidates | no source; half the paper's test set |
  | D | Four weeks | 11 candidates above the floor | more articles per window | twice the paper's test set; half as many candidates |

* **Recommendation:** A: two calendar weeks are the paper's test set of 1,000 articles in late 2014, in whole weeks, and
  the one-week gap covers the time the paper gives shares to settle. **Decision:** A, B, C or D?

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
