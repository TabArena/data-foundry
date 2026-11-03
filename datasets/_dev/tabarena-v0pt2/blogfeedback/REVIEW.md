# blogfeedback

**Outcome:** added. The AI recommends shipping it after the panel's changes, now made; neither open issue
can turn it to `No`. The source is Krisztian Buza's crawl of Hungarian blogs, first released on his page in 2012 with
his chapter "Feedback Prediction for Blogs" (UCI's 2014 copy has the same bytes). A row is a post at a daily base time,
at most 72 hours after it was published; the target is the comments it receives in the next 24 hours (none for 65% of
the training rows and 70% of the test rows). The split is the source's: a training crawl of 2010-2011 and 60 test days
of February and March 2012, cut into three windows of 20 days. Your condition of 2026-10-30 ("Move to yes if you can
resolve the leak") is met. In a training row, the 50 blog statistics (mean, spread, minimum, maximum and median of the
counts of the blog's posts) included the same post's later counts; they are now recomputed from the blog's other posts.
The test rows' statistics come from the training crawl only, which is history on every test day, so the fix barely
moves the test score (untuned LightGBM: RMSLE 0.620 with the published, 0.622 with the recomputed statistics).
Validity: USE-1 holds, and the chapter names the actor (a proof of concept with Capgemini Magyarország for companies
that must react quickly to blog discussion); USE-8 approximate (the training crawl is undated); LEAK-10 fixed; LEAK-31
open (issue 1); SPLIT-15 departed, exception to confirm (issue 2); PROV-8 and PROV-9 fixed (2012, Buza's release).
Value: TP-2 and TP-10 hold (untuned LightGBM finds 6.6 of each day's 10 most-commented posts, a sort by the last day's
comments 5.6); MET-1 triggered, fixed: RMSE on the raw count ranks models against the source's daily top-10 measure (it
puts the Huber model, among the best on daily hits, last of the LightGBM models), so the score is now that measure,
Buza's Hits@10 per test day, as `mean_group_top_k_overlap` in the metric library (your call of 2026-11-02). Quality: a post length of 0 becomes missing (CLEAN-10). Weighed: source +, size +, signal +, age -, niche -
(Hungarian blogs). Left for Andrej: issues 1 and 2.

Changes made after the review panel (AI, 2026-11-01): the mediator's changes that need no decision are in the
definition, and every number in the notes was measured again. Two depart from a precedent, each with its fact. The
parents' comment columns lose their `Potential leak` label, unlike the later pulls dropped in
distribution_transformers_at_cauca_department and african_credit_scoring_challenge: with an unchanged set of parent
posts they only rise between a post's base times, so they are counted at each base time. The record's `Data Quality
Issue` marker is to go at hand-over, though other `Yes` records keep theirs: selection.md defines it as damage that
cannot be repaired, and the leak and the copies are repaired here.

**Main points:** the word flags and whether the task still holds without the post text (issue 1, answered); the
metric's name and scale (4, new). Settled: nine windows of 6 days (2, 2026-11-03); the score is the source's daily
top-10 measure (3, 2026-11-02); the record's `year` and source take the definition's values (2026-11-03).

**Issues for Andrej:**

1. **Drop the word flags, or keep them with a note?**

   * **Problem:**
     - The data has 178 yes/no word columns that Buza chose by their link to the comments, on posts his chapter does not
       name.
     - Had the test days of 2012 been among them, the columns would carry a hint of the test outcomes.
     - Drop them, or keep them with a note?
   * **Background:** the data has 200 yes/no columns, one per word, that say whether a post contains it (178 remain
     after copies were dropped); the words are not named. Footnote 1 of Buza's chapter says he chose them as "the 200
     most discriminative words": for each word, the gap in average comments between posts with and without it. That
     is a choice made with the target. Such a selection is measured, kept with a note when its effect is small and
     removed when we can; one the source published is decided case by case, so this is a weighing call[^1]. In the
     22% of rows without text (23% of training and 20% of test rows), a flag of 0 means unknown, not absent; the
     flags stay 0 there, and the missing `post_length` marks those rows.
   * **Effect on the task:** measured, the words add nothing (numbers below).
   * **Experiments:** per window (days 41-60 / 21-40 / 1-20; untuned LightGBM, 2 seeds, after the panel's changes),
     RMSLE is 0.674 / 0.570 / 0.621 with the words and 0.672 / 0.571 / 0.617 without; the daily top-10 hits are
     6.03 / 7.25 / 6.55 with and 6.30 / 7.25 / 6.68 without. In Buza's Table 1 the text features lower his top-10
     score for 6 of 7 models.
   * **Unknown:** which posts chose the words cannot be checked. Buza's word score, recomputed here, is positive for
     70.7% of the testable words on the training rows and 58.5% on the test rows. A word chosen on some posts shows
     its gap most often on those posts, so this leans toward a choice on the training crawl, but it is circumstantial
     evidence, not proof[^2]. Buza's word list would settle it.
   * **Consistency:** all three earlier cases of such a selection were removed[^3]. The closest, qsar_bioconcentration,
     dropped the authors' 9 chosen descriptors, worth +0.002 (2026-10-26).
   * **Panel:** the advocate argues to keep: the flags are the only text in the data, a monitoring desk reads the
     text, and qsar_bioconcentration still had RDKit descriptors of the same molecules after the 9 were dropped. The
     critic argues to drop: nothing sets this case apart from qsar_bioconcentration, and a note would record a
     suspicion nobody can check.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep with a note (implemented) | the 178 word flags stay as features, with a note on the selection named in `fit_reason` | the only text in the data | a note records a suspicion nobody can check; departs from qsar_bioconcentration |
     | B | Drop the 178 flags | 63 features remain, the `Anonymized` data tag goes; no score changes | follows qsar_bioconcentration | the data loses its only text |

   * **Recommendation:** B: the words add nothing measurable, and all three earlier selections of this kind were
     removed, qsar_bioconcentration the closest. A only if you take the training-crawl reading as the fact that sets
     this case apart; Buza's word list would settle it. **Decision:** A or B?

   **Notes for the AI:** A is in the definition as a `Potential leak, kept on purpose:` note (the selection, the drop
   test, revisit if Buza's word list becomes known), named in `fit_reason`. On B, drop the 178 word columns and the
   `Anonymized` data tag.

   [^1]: **LEAK-31** (Should): supervised feature selection on the full labelled set is measured, kept with a note
     when small and removed when we can; a selection the source published is decided case by case (Lennart,
     2026-10-21).
   [^2]: **EV-6** (Should): a claim is proven only by a test that could have refuted it; circumstantial evidence is
     named as such and reported as a "maybe", with the test that would settle it.
   [^3]: The **LEAK-31** cases: home_credit_default_risk (2026-10-19), qsar_bioconcentration (2026-10-26) and
     numerai_v5_2_1m (2026-10-26).

   **Andrej (2026-11-03, discuss):** Is the original post accessible as text and can be added as a column? I believe
   without the actual source, this is not a meaningful tabular task anymore, but rather text classification

   **Answer (AI, 2026-11-03):**

   * **Problem:**
     - The post text cannot be added: the release holds no post id, URL, blog name or date, so no post can be found
       again.
     - The question is whether the task still holds without it.
     - The measurements say yes, because the text carries almost none of the signal.
   * **Background:**
     - Buza's own zip of 2012, byte-identical to UCI's, holds only the 281 numbers per row. His chapter names no
       release of the crawled pages. Only he could say whether the crawl still exists, by asking him.
     - What predicts the next day's comments is how a post has been drawing comments so far: its comments in the
       last 24 and 48 hours, their change, the parents' comments, and the blog's history. The text came in only as
       the 178 word flags.
   * **Experiments** (untuned LightGBM, the three earlier 20-day windows):
     - A sort by the last 24 hours' comments alone finds 5.6 of each day's 10 most-commented posts; the model finds
       6.6 with or without the word flags (6.61 with, 6.74 without).
     - In Buza's own Table 1 the text features lower the score for 6 of 7 models.
     - So the task is to predict the comments from their dynamics: a tabular task. Text classification would need
       text that predicts, and here it does not.
   * **Options:** as above, plus retiring the dataset:

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep the flags with a note (implemented) | the 178 word flags stay | the only trace of the text | a selection made with the target; adds nothing |
     | B | Drop the flags | 63 features remain: comment dynamics, the blog's history, length, weekday | a tabular task of comment dynamics, no selection made with the target | the data keeps no trace of the text |
     | C | Don't ship | the record set to `No` | no task whose source data was text | loses a task whose signal is in the counts, not the text |

   * **Recommendation:** B: the comment dynamics carry the task, and the word flags add nothing and were chosen with
     the target. **Decision:** A, B or C?

   **Notes for the AI:** on B, drop the 178 word columns and the `Anonymized` data tag, re-run `dataset check`. On C,
   retire as records.md says.

   **Andrej (2026-11-03, change):** I choose option C for now and mark this dataset as 2nd Tier

   **Resolved (2026-11-03, Andrej):** C, not shipped for now: the record is `TBD -> 2nd Tier`, its `v2_path` cleared
   and its claim released; the folder leaves the working copy (copies of its last files in the run folder of
   2026-11-03, `blogfeedback_retired/`).

2. **Confirm three test windows of 20 days?**

   * **Problem:**
     - The definition cuts the 60 test days into 3 windows of 20 days, each trained on the 2010-2011 crawl and the
       earlier test days.
     - The rules give as many windows as an IID task of this size gets folds[^4]: 9 for 56,239 rows.
     - Confirm 3 as an exception?
   * **Background:** the 9 are 3 repeats of 3 folds. The builder's reason, that the source defines the split[^5],
     decides nothing: the source trains once and tests all 60 days, one window, and a temporal task needs at least
     3[^6]. `splits_comment` now gives the reasons below.
   * **Effect on the task:** each window tests a model refit up to 20 days earlier; nine windows would refit every 6
     days, closer to a daily service that retrains often. Nine windows add no test rows: the crawl has a single date
     value, so only the 7,036 rows of the test days can ever be test rows, and nine windows cut them into pieces of
     about 700.
   * **Experiments:** under Hits@10, the declared metric, a 20-day window measures a difference between two models
     with a standard error of 0.26 hits a day, a 6-day window with 0.48, while the gaps between models are about 0.5.
   * **Rules:** the rule that takes the horizon from the source, such as its own test period[^7], stands before the
     rule on the number of windows in splits.md and wins at equal strength. The source predicts 60 days from one
     training run, and 20 days is the longest window that still gives three.
   * **Panel:** the advocate and the critic both accept 3 windows; both dropped the argument from the heavy tail,
     which held only for RMSE on raw counts.
   * **Consistency:** onlinenewspopularity and zillow_prize ship 9 windows, but their data is dated over its whole
     range, so more windows add test rows. rossmann_store_sales takes its window length from the source's 6-week
     horizon, but at 844,392 rows the window-count rule also gives it 3 windows, so it is no precedent for fewer.
     This would be the first exception to the window-count rule.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | 3 windows of 20 days, with an exception (implemented) | the 60 test days in 3 windows, each a model refit up to 20 days earlier | mirrors the source's one training run; standard error 0.26 | the first exception to the window-count rule |
     | B | 9 windows of 6 days | the newest 54 test days in 9 windows, each a model refit up to 6 days earlier; days 1-6 untested | follows the window-count rule; closer to a service that retrains often | test pieces of about 700 rows; standard error 0.48 against gaps of about 0.5 |
     | C | 10 windows | the 60 test days in 10 windows of 6 days; as B, but all 60 days tested | follows the window-count rule; uses all 60 days | as B |

   * **Recommendation:** A, confirm the exception: it mirrors the source's one training run, and a 20-day window
     measures model differences with a standard error of 0.26 hits a day against 0.48 for 6 days. **Decision:** A, B
     or C?

   **Notes for the AI:** the exception for the record, as implemented: `Exception to SPLIT-15 (2026-11-01, Andrej):
   the training crawl is one undated time value, so only the 60 test days can be test rows, and the source predicts
   all 60 from one training run; 20 days is the longest window that gives SPLIT-14's three. Serves P4: the split
   mirrors the source's deployment (SPLIT-12).` On B: `TemporalSplits(window=6, unit="unique", n_windows=9)`.

   [^4]: **SPLIT-15** (Should): roll the windows back from the newest data, as many windows as an IID or grouped task
     of that size would get folds.
   [^5]: **SPLIT-19** (Should): when the source defines the split (a competition's or a paper's official periods),
     follow it; it is still a claim to check.
   [^6]: **SPLIT-14** (Must): a temporal task has at least 3 windows, and no window's train side holds less than 50%
     of the data.
   [^7]: **SPLIT-12** (Should): the horizon is a human judgment from the source (how far ahead the actor predicts,
     the competition's own test window, the refit cadence); choose the test windows to match it.

   **Andrej (2026-11-03, change):** With the given sample size we would prioritize 9 folds

   **Resolved (2026-11-03, Andrej):** (B), nine windows of 6 days over the newest 54 test days (train 49,835 to
   55,331 rows, test 621 to 908 rows per window). `splits_comment` and the task summary say so, and that the notes'
   measurements were taken on the earlier 20-day windows; no exception to SPLIT-15. `dataset check`: 0 errors, the
   one warning as before.

4. **The metric: is it Buza's Hits@10, and under which name?**

   * **Problem:**
     - You asked whether the declared metric is exactly the source's.
     - It is, apart from its scale and a tie rule: the library reports the share of the day's top 10 found (Hits@10 /
       10), where Buza reports the count (0 to 10).
     - Its name, `mean_group_top_k_overlap`, describes the computation, not the source.
   * **Background:**
     - Buza (Sec. 5.1): for each test day, the 10 posts predicted to draw the most comments; Hits@10 counts how many
       are among the day's 10 most-commented, averaged over the days. The library computes the same overlap per day
       and averages it, divided by 10.
     - At a tie at the 10th place, the library takes the expected overlap over the ways to break it. That rule is
       ours; without ties the score is exactly Buza's divided by 10 (a test checks it).
     - Only this dataset uses the metric, so a rename touches one definition, the library and its tests.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep `mean_group_top_k_overlap` (implemented) | the share, 0 to 1 | a name that says the computation; a scale like other shares | not the source's name or scale |
     | B | Rename to `hits_at_k`, report the count | `hits_at_k` with k = 10 returns Hits@10, 0 to 10 | the source's name and scale; numbers read as in Buza's Table 1 | a rename of a metric in the library |
     | C | Rename to `hits_at_k`, keep the share | the source's name, the share 0 to 1 | the source's name | the name says hits but the scale is a share |

   * **Recommendation:** B: the score then reads as in the source (6.6 hits a day, Buza's Table 1 on the same scale).
     **Decision:** A, B or C?

   **Notes for the AI:** on B, rename in `src/data_foundry/v2/metrics.py` (definition, docstring list of custom
   metrics), drop the division by k, update `tests/test_v2_metrics_custom.py` and blogfeedback's metric and notes.

   **Andrej (2026-11-03, metric mark, discuss):** Is this exactly the source metric? If yes, let's discuss
   alternative names for it, if not, why didn't you use the source metric?

   **Answer (AI, 2026-11-03):** this issue answers it: the bullets and the options above.

**Review panel:** ship after changes (mediator). Claim audit: 54 claims, 38 hold, 11 refuted (fixed), 2 partly refuted
(noted), 1 superseded, 1 weighing call (the metric, now the RMSLE stand-in) and 1 untested (when the parents' comments
were counted; the chapter is silent). Blind review: would include with changes; its main concern was the raw-count
score that a few viral posts decide, now replaced. Debate: agreed on the leak fix, the known-blog temporal regime, the
actor and provenance from Buza's chapter, and Hits@10 per day over RMSE (issue 3); disputed: the word flags (issue 1)
and the facts behind three windows (issue 2).

<details><summary>Mediator</summary>

**Mediator: blogfeedback (mediator, 2026-11-01)**

**Recommendation**

```text
Verdict: ship after changes.
Validity: SEL holds (public blog counts, no ids, CC BY 4.0); USE-1 holds, and the source names the actor (Buza's
  chapter: a proof of concept with Capgemini Magyarország for companies that must react quickly to blog discussion);
  USE-8 approximate holds (the undated crawl; "the actor is our example" goes); USE-10 holds for at least 90.6% of test
  rows (9.4% carry the all-zero blog vector, noted); LEAK-10 triggered, fixed (training statistics out of fold; the
  test rows' statistics are history, LEAK-29 holds); the small training-side remainder noted (alfa_battle_2_0_task_2 /
  lending_club tension row); LEAK-10 second clause not triggered for the parents (counts taken at each base time);
  LEAK-31 triggered by the 200 word flags (chosen with the label), a weighing call (issue 1); LEAK-19 applied;
  SPLIT-1/3/9/10/11/13/14/17 hold; SPLIT-15 departed (3 windows), SPLIT-12 wins by position, exception to confirm
  (issue 2); PROV-8/PROV-9 triggered, fixed in metadata (2012, Buza's release; UCI is a byte-identical copy); PROV-16
  misquote fixed.
Value: TP-2/TP-4 hold; TP-10 leg 1 holds in 3 of 3 windows on rmsle and on Hits@10, leg 2 under the summaries clause;
  MET-1 triggered: raw rmse misranks the daily top-10 decision (Must, over MET-5's Should): replaced by rmsle as a
  stand-in on a log1p target now; the source's Hits@10 per day needs a library metric (issue 3).
Quality: CLEAN-10 (post_length 0 to missing), CLEAN-16 with MET-3 (log1p target), CLEAN-5 comment corrected.
Weighed: source + (primary chapter and 2012 release), size + (56,239 rows), signal + (R² 0.60-0.70 on log1p; +1 hit a
  day over the desk's sort), age - (2010-2012), niche - (Hungarian blogs).
For the curator: issue 1, a weighing call (word flags: drop or keep with a note); issue 2, confirm an exception
  (3 x 20-day windows); issue 3, a yes/no (add the per-day top-k metric and declare Hits@10).
```

**Agreed facts** (both sides and the evidence reports; numbers from the shipped windows)

1. Buza's chapter is open (author's copy, gfkl2012_blogs.pdf). Abstract: "a proof-of-concept industrial application,
   developed in cooperation with Capgemini Magyarország Kft."; Sec. 5.1 scores, per test day, the 10 posts predicted
   to draw the most feedback (Hits@10, with AUC@10 beside it in Table 1).
2. The first release is `blogdata.zip` on Buza's page (2012-07-24, named in chapter Sec. 5.1); all 61 CSVs are
   byte-identical to UCI's 2014 upload.
3. The published training blog statistics equal the statistics over all of the blog's training rows (share 1.0), so
   they hold the post's own later counts. The test rows' statistics equal those over training rows only (1.0) and never
   those over test rows (0). Test ROC AUC is 0.908 with the published and with the recomputed statistics: the leak sat
   in the training rows only.
4. The 5-fold statistics still move slightly with the row's own outcome in small blogs (Spearman -0.23 in blogs with
   2-5 posts), training side only; inner-CV gain +0.058 to +0.061 against +0.048 on test.
5. 719 test rows (9.4%) carry the all-zero blog vector; 24.6% of them had comments before the base time, against 0% of
   the zero-vector training rows, so they are probably blogs without training rows. Predictions on them are calibrated
   (P(comment) 0.124 / 0.047 / 0.036 predicted, 0.116 / 0.059 / 0.035 observed).
6. The parents' max and mean only rise between base times while the parent set is unchanged (96 and 97 rises in 1,587
   pairs, no fall); every fall comes with a shrinking set (702 of 731 set changes are decreases). Dropping the four
   columns changes no score. `parent_comments_min` is 0 in all 249 one-parent rows where max = mean > 0 (a broken
   column, rightly dropped).
7. The word flags are "the 200 most discriminative words" (chapter footnote 1: the gap in mean feedback between
   documents with and without the word, over the sum of the two standard deviations), on documents the chapter does
   not name. They carry no test signal (fact 13).
8. `post_length` 0 (23.8% of rows) is a per-blog extraction gap: 100 blogs without text in any row hold 90% of the
   zero rows and stay text-less in the test files.
9. The temporal, known-blog regime is the only one with signal (grouped by blog, R² -0.672 on counts). Train sides
   hold 87.5-95.4%; test windows 2,564 / 2,225 / 2,247 rows; gap 0 is right (next day's last-24h count equals the
   target in 99.7% of pairs). The crawl is one undated time value, so only the 7,036 test-day rows can be test rows.
10. Raw rmse ranks the raw-count LightGBM first (23.95) though it is the worst LightGBM on Hits@10 (6.16), and rates
    the desk's sort by last-24h comments (5.63 hits a day) worse than the training mean (1.08). The top 1% of test rows
    carry 68-92% of the squared error.
11. TP-10 leg 1: rmsle 0.563-0.667 for LightGBM against 0.696-0.820 for the best scaled naive rule; on Hits@10,
    +0.70 to +1.35 posts a day over the last-24h sort (paired SE 0.27-0.29).
12. Several sentences are wrong: the UCI quotation, "554 blogs" (distinct statistic vectors; the chapter crawled
    "roughly 1200 sources"), "scores the same with no statistics" (AUC 0.892 against 0.908), 251 missing rows (250
    shipped), "closed access, not read", "frequent words", the parents' "Revisit" line.

**Decisive experiment (mediator, 2026-11-01).** Two questions were open: which metric already in the library tracks
Hits@10 best, and what the words do on the candidate metrics. Untuned LightGBM (400 trees; log1p with and without the
words, 2 seeds; raw L2, Poisson, Huber) and three naive rules on the three shipped windows:

13. Word flags, mean of 2 seeds, windows 41-60 / 21-40 / 1-20: rmsle 0.672 / 0.567 / 0.620 with the words, 0.673 /
    0.567 / 0.616 without; Hits@10 5.95 / 7.13 / 6.60 with, 6.03 / 7.18 / 6.70 without. Nothing in either direction
    beyond seed noise (about 0.1 hit).
14. Kendall tau with Hits@10 across predictors, per window: rmsle 0.84-0.86 (10 predictors) or 0.78-0.88 (7, one per
    kind); `normalized_gini` 0.76-0.81 or 0.90; per-day `mean_group_pearsonr` 0.57-0.78; raw rmse 0.25-0.80. Rmsle and
    the Gini track the daily decision about equally (their order flips with the predictor set), raw rmse does not. The
    agreed stand-in, rmsle, stands.

**Library check.** `src/data_foundry/v2/metrics.py` has no per-group top-k hit rate. `precision_at_k` is binary only
(share of positives among the k highest scores) and takes no group input; the per-group metrics (`mean_group_pearsonr`,
`par_k`, `hierarchical_balanced_accuracy`) compute something else. So the definition ships rmsle now and the library
metric goes to the curator (issue 3).

**Changes to make now (no decision needed)**

1. `use_case` and `fit_reason` from the chapter: a social-media monitoring service (Buza's proof of concept with
   Capgemini Magyarország) decides each morning which of the last 72 hours' posts its analysts follow, cited with
   section and quotation; drop "The source names no actor" and the first gap. The fit stays approximate (the undated
   crawl). USE-1, USE-8, PROV-16.
2. Metadata: `year = "2012"`, `source = "Other"`, `source_url` = Buza's release
   (`http://www.cs.bme.hu/~buza/blogdata.zip`); `download_description` names the UCI zip as the copy we download; the
   BibTeX cites the chapter (with the author's copy) and the 2012 release. PROV-8, PROV-9.
3. Metric: replace the fallback with `Metric.stand_in("rmsle", original=<Hits@10 per test day, chapter Sec. 5.1, p. 5,
   Table 1>, reason=<no per-group top-k metric in the library yet (MET-13); rmsle orders models close to Hits@10, tau
   0.78-0.88, where rmse on counts does not, 0.25-0.80>, reference=<the chapter>, target_transform="log1p")`, and ship
   the target as `log1p_comments_next_24h`. The reason cites the chapter directly, names AUC@10, and drops "closed
   access, not read" and "secondary source". MET-1 (Must, over MET-5), MET-3, MET-11, CLEAN-16. The origin is
   `stand_in`, not `context`: the source defines a metric (MET-11).
4. Leak notes. The "Not removed" bullet says the 5-fold statistics still shift a little with the row's own outcome in
   small blogs and that tuning on training rows is slightly optimistic (fact 4), and that the out-of-fold maximum sits
   below the test rows' value in about 22% of training rows. "Scores the same with published, recomputed or no
   statistics" becomes the numbers (lower without them). LEAK-10, EV-2.
5. Known blog: replace "Every test blog is in the training file" with fact 5 (at least 90.6% of test rows on a blog
   seen in training; 9.4% carry the all-zero vector, probably new blogs, encoded 0 on the test side and missing on the
   training side; predictions calibrated). USE-10, SPLIT-13, EV-6.
6. Parents: drop the `Potential leak, kept on purpose` label; a plain note with fact 6; replace "Revisit if Buza's
   chapter documents them" with "the chapter (Sec. 4.2) does not say when they were counted"; the `CONSTANT` comment
   calls `parent_comments_min` a broken source column. LEAK-10 (second clause not triggered).
7. Words: describe them as chosen with the label (footnote 1), in `curation_comments` and the `WORDS` comment. While
   issue 1 is open they stay, with a `Potential leak, kept on purpose:` note (mechanism, the drop test of fact 13,
   revisit if Buza's vocabulary or document set becomes known), and `fit_reason` names them as a kept leak. LEAK-31,
   USE-8.
8. `post_length` 0 becomes missing, after step 3 (the fold key reads the raw values); the anomaly bullet names the
   per-blog pattern. CLEAN-10.
9. `splits_comment`: replace the SPLIT-19 reason with the facts of issue 2 (SPLIT-12, the fixed test pool), and add
   that the crawl is one time value, so the training history cannot be trimmed (SPLIT-20). The record gets the
   proposed `Exception to SPLIT-15` line once the curator confirms it.
10. TP-10 line in the notes: leg 1 on rmsle and Hits@10 (fact 11); leg 2: `comments_24h_to_48h_before` and
    `comments_change_24h` are the source's window counts over a post's life of at most 72 hours (three rows), summaries
    of the series up to the prediction point, as the amended rule allows (g_research_crypto_forecasting,
    rain_in_australia). TP-10.
11. Wording: quote UCI verbatim ("we calculate all the features of the selected blog posts from the information that
    was available at the basetime"); "at least 554 blogs" with the chapter's "roughly 1200 sources"; 250 missing rows;
    the tuning-folds bullet gets its measured null effect (R² 0.581 on random and on post-grouped folds) or goes; trim
    `curation_comments` toward 400 words. PROV-16, EV-2, writing.md.
12. Record: an Assessment line that supersedes "closed access, not read" and the old figures (99.89%, 99.73%, 12,526
    posts); remove the `Data Quality Issue` marker, since selection.md defines it as damage that cannot be repaired and
    the leak and the copies are repaired here.

**Changes that need the curator**

1. Word flags (P4, LEAK-31 Should): drop the 178 columns, or keep them with the note of change 7. A weighing call.
2. Windows (P4, SPLIT-15 Should): confirm 3 windows of 20 days as an exception to SPLIT-15, or cut 9 windows of 6 days.
3. Metric (P6, MET-1 and MET-13 Must): add a general per-group top-k metric to the library and declare the source's
   Hits@10 per day as `Metric.source` (the main session implements it on a yes), or keep the rmsle stand-in.

**Disputed points**

*1. Word flags: keep with a note (advocate) or drop (critic).*
- Both rest on LEAK-31 (Should): "measure it; keep with a note when small, remove it when we can. A selection the
  source published is decided case by case (Lennart, 2026-10-21)." This is no conflict between rules, and the rule's
  last sentence leaves a source-published selection open. So it is a weighing call for the curator.
- Facts: the words carry nothing on test (fact 13; R² on log1p 0.6559 without, 0.6549 with; Buza's Table 1: the text
  features lower Hits@10 for 6 of 7 models). Which documents chose them cannot be settled: Buza's score is positive for
  70.7% of 147 testable words on training rows against 58.5% on test rows, which leans toward a training-period
  selection but is circumstantial (EV-6).
- Advocate's best evidence: the drop test is flat, so no test label reaches the score; the flags are the only text in
  the data, and a monitoring desk reads the text; qsar_bioconcentration had RDKit descriptors as a substitute.
- Critic's best evidence: all three LEAK-31 cases were removed (home_credit_default_risk, qsar_bioconcentration,
  numerai_v5_2_1m); qsar_bioconcentration is a source-published selection worth +0.002, dropped; a note would record a
  suspicion that can never be checked.
- Mediator's reading: the substitute in qsar_bioconcentration mattered because dropping cost nothing; here dropping
  also costs nothing, so it does not set the case apart. The training-period reading would (a selection on training
  documents is no leak), but it is circumstantial. The remedy ladder puts a fix in the definition (drop) before a kept
  note. Recommendation: drop, unless the curator accepts the training-period reading as the fact that sets the case
  apart.
- What would settle it: Buza's word list or the documents he scored (the author could be asked).

*2. Windows: which facts the exception to SPLIT-15 rests on.*
- Both sides accept 3 x 20 days in their rebuttals; they dispute the supports.
- By rank: SPLIT-12 (Should; the horizon from the source, "the competition's own test window") precedes SPLIT-15
  (Should) in splits.md. The source predicts all 60 test days from one training run; SPLIT-14 (Must) forbids one
  window, and 20 days is the longest horizon that gives three. Meeting SPLIT-15 would cut the horizon to 6 days, so
  the two conflict, and SPLIT-12 wins by position.
- Facts that hold: the source's single 60-day test period (SPLIT-12); the fixed test pool of 7,036 rows, since finer
  windows add no test rows (SPLIT-17's reason); if Hits@10 is adopted, resolution (paired SE of a model difference 0.26
  hits a day over 20 days, 0.48 over 6, model gaps about 0.5; MET-10).
- Facts that do not hold: SPLIT-19 (the source's design is one window, so it decides nothing between 3 and 9); the rmse
  heavy tail (rmse goes; under rmsle the top 5 rows hold 9-10% of a 20-day window and 16-25% of a 6-day one); "every
  fold can be scored" (6-day windows hold about 700 rows); "every test day is used" (10 windows of 6 days use all 60).
- The exception needs the curator's name, so it goes to him as a confirmation, with 9 x 6 days as the alternative.

*3. Metric: settled.* Both sides now put Hits@10 per day first and rmsle as the interim. Raw rmse fails MET-1 (Must),
which outranks MET-5 (Should): Table 1 reports Hits@10 and AUC@10 side by side, but the text argues from hits ("The
number of hits was around 5-6 ... This naive model achieved only 2-3 hits"), and AUC@10 scores the same top 10. The
library lacks the metric, so rmsle ships now (change 3) and the library metric is issue 3. MET-2: the day is the time
column and a feature; the repository accepts a metric input that is also the time column
(`task_metric_input_is_model_input`, info), and the split audit shows the day as a feature is harmless. A strict
reading of MET-2's "never a feature" would take it out of the features; say so in issue 3.

**Consistency with precedent**

- Leak fix: follows the curator's condition (CC 2026-10-30, Andrej: "Move to yes if you can resolve the leak");
  LEAK-29 as in sf_permit_time; the residual recorded as in alfa_battle_2_0_task_2 and lending_club.
- Parents: kept without the leak label. This departs in outcome from distribution_transformers_at_cauca_department and
  african_credit_scoring_challenge (values from a later pull, dropped). The fact that sets it apart: the values rise
  between a post's base times and fall only when the parent set shrinks, so they are counts at each base time, not a
  later pull. The same fact separates it from the crawl-time count in facebook_comment_volume's Assessment.
- Metric: follows numerai_v5_2_1m (RMSE misranked against the source's per-group measure; a per-group metric
  declared) and onlinenewspopularity (rmsle on a log1p engagement count). The origin differs from onlinenewspopularity
  (`stand_in`, not `context`) because this source defines a metric.
- Target scale: follows MET-3 and CLEAN-16 (Lennart, 2026-10-21) and nantucket_sound_sea_duck_aerial_survey_counts.
- Windows: departs from onlinenewspopularity and zillow_prize (9 windows; their data is dated over its whole range, so
  more windows add test rows); follows rossmann_store_sales (3 windows of the source's horizon, SPLIT-12). It would be
  the first exception to SPLIT-15.
- Word flags: dropping follows qsar_bioconcentration; keeping departs from it and needs the training-period reading
  as its fact (issue 1).
- Copies: LEAK-19 as in wine_quality and qsar_oral_toxicity; text-less look-alikes kept as in hiva_agnostic and
  qsar_tid_11.
- TP-10 leg 2: follows g_research_crypto_forecasting (trailing summaries) and the rain_in_australia amendment.
- `no_spread` kept under TP-2: follows acquire_valued_shoppers_challenge and hr_analytics.
- `Data Quality Issue` removed: other `Yes` records keep the marker (ieee_fraud_detection,
  loan_default_prediction_imperial_college); what sets this one apart is that its damage (the leak, the copies) is
  repaired, which the marker's definition excludes.
- `Two-Regime Zeros` tag: fits the policy call of 2026-10-30 (zero holds 65.5% of rows, the next value 10.8%).
- No drift and no third exception of one reason.

</details>

<details><summary>Claim audit</summary>

**Claim audit: blogfeedback (claim-auditor, 2026-11-01)**

**Verdict.** The data claims hold, and so does the leak fix on the test side. The biggest finding is about a source: Buza's chapter, which the definition and the record call "closed access, not read", is open as the author's copy (<http://www.cs.bme.hu/~buza/pdfs/gfkl2012_blogs.pdf>, linked as green open access by Semantic Scholar). Its first data release (<http://www.cs.bme.hu/~buza/blogdata.zip>, Last-Modified 2012-07-24) has the same bytes as the UCI files. Reading both refutes five claims: the use case's "the source names no actor", the description of the word columns as "frequent words", the metric reason's "not read, secondary source", the year and source (2014, UCI), and the record's "chapter not read". Separately, two data claims are refuted with numbers: "every test blog is in the training file" fails for up to 9.4% of test rows, and the 5-fold blog statistics still move a little with the row's own outcome, on the training side only. None of these blocks shipping. Two calls go to the curator: the word columns (note or drop) and the metric (rmse against the source's per-day top 10). 54 claims tested: 38 hold, 11 refuted, 2 partly refuted, 1 superseded, 1 weighing call (the metric against the decision) and 1 untested, plus two untested points inside claim 52.

**Scope and method.** I read dataset.py, the README, the record, the builder report and probes, principles.md, evidence.md and metrics.md. Outside sources: the UCI page and API text; Singh et al. 2015 (PDF, Sec. II and IV-E); Buza's chapter (author's copy, 8 pages); the original 2012 zip and its readme.txt. The frame and splits were rebuilt from the definition (`dataset_io.from_definition`). The container comes from `to_container()` and is scored with `data_foundry.v2.metrics.scorer`. Model numbers are untuned LightGBM (400 trees, lr 0.05) on the 3 shipped windows; drop tests use 2 seeds and the metric comparison 1 seed. Scripts and outputs are in the run folder.

**Claims table**

| # | claim | source | test | result | evidence | rule |
|---|---|---|---|---|---|---|
| 1 | Target = comments in the 24 h after the base time; zeros 65% train, 70% test, observed, no cap | task_summary.predicted; notes bullet 1 | re-count after copies dropped; next day's `comments_last_24h` against this row's target | holds | zeros 64.8% / 70.1%; equality in 99.73% of 3,730 consecutive test pairs | USE-5, LEAK-26 |
| 2 | Posts at most 72 h old at the base time | task_summary.row | range of `hours_since_publication`; chapter Sec. 4.1 | holds | 0-72 in both parts; chapter: "blog documents published in the last 72 hours" | USE-1 |
| 3 | "one of 554 Hungarian blogs" | task_summary.row; notes intro | distinct statistic vectors; all-zero vector; chapter Sec. 5.1 | **refuted (count)**; Hungarian holds | 554 distinct 50-statistic vectors. The all-zero vector alone holds 1,823 training rows over 596 post keys, so every blog without a comment or trackback is merged into it. The chapter crawled "roughly 1200 sources"; the 2012 readme says "Hungarian Blog Data" | EV-2, writing |
| 4 | Most posts appear at three base times | task_summary.row | rows per post (text-bearing) | holds | 94.9% of 12,526 training posts and 87.4% of 1,888 test posts have exactly 3 rows | - |
| 5 | Training crawl 2010-2011; 60 test days, Feb-Mar 2012 | task_summary.row; splits_comment | UCI summary; file dates | holds | UCI: "basetimes were in the years 2010 and 2011 ... February and March 2012"; files 2012-02-01 to 2012-03-31, 60 distinct days | - |
| 6 | "The source names no actor" | task_summary.use_case | read the chapter | **refuted** | Abstract: "a proof-of-concept industrial application, developed in cooperation with Capgemini Magyarország Kft."; Sec. 1: a company "might have to react quickly" to negative news in social media, and "analysis of all these documents by human experts is hopeless" | USE-1 |
| 7 | "Buza's chapter is described as an industrial proof of concept" | task_summary.use_case | chapter abstract | holds (now from the primary text) | quote above | EV-2 |
| 8 | Fit approximate; gaps: "the actor is our example" and training statistics from other posts, earlier and later | fit, fit_reason | chapter; data | **first gap refuted**, second holds, fit stays approximate | actor as in 6; the second gap is the undated crawl (USE-8) | USE-8 |
| 9 | 3 windows of 20 test days, each trained on the crawl plus earlier test days | task_summary.split; splits_comment | rebuilt splits | holds | train/test 53,675/2,564 (days 41-60), 51,450/2,225 (21-40), 49,203/2,247 (1-20) | SPLIT-14 |
| 10 | Published training statistics hold the post's own later counts | task_summary.changes; notes "Leak, fixed" | decision table; 24 h pairs; later rows | holds | published = over all training rows: share 1.0. Total 24 h later = total + target in 99.89% of 24,691 pairs; 67.07% of text-bearing training rows have a later row | LEAK-10 |
| 11 | Hungarian via Singh 2015, Sec. II, p. 2: "feedback prediction on Hungarian blogs" | notes intro | Singh PDF | holds (also primary now) | Singh p. 2: "fine-grained feedback prediction on Hungarian blogs"; chapter Sec. 5.1: "We crawled Hungarian blog sites" | PROV-16 |
| 12 | UCI: "Features are computed only from information available at that basetime" | notes bullet 1 | UCI text (API `additional_info.summary`) | **refuted as a quotation** | Not in UCI's text. UCI says: "we calculate all the features of the selected blog posts from the information that was available at the basetime" | EV-2, PROV-16 |
| 13 | Published statistics = mean, sd (ddof 0), min, max, median over the blog's training rows, copies included | notes bullet 2; decision 1 | decision table (dataset check); builder e6 | holds | share 1.0 at 0.1%; 99.59% of cells within 1e-5, the rest are float32 sd | LEAK-10 |
| 14 | OOF over 5 folds of whole posts; 251 rows of 69 blogs get missing values | notes bullet 2 | shipped frame | holds | 250 missing rows in the shipped frame (251 before the copies are dropped), all in the training crawl | CLEAN-7 |
| 15 | "Not leave-one-post-out, which would shift the statistics with the row's own target" (implied: 5-fold does not) | notes bullet 2 | within-blog Spearman of (OOF − full) mean against the row's own outcome; inner post-grouped CV on the crawl | **partly refuted (small)** | Spearman with own log1p target: −0.23 in blogs with 2-5 posts (1,811 rows), −0.05 to −0.14 in larger blogs; with the post's later total, −0.62 in small blogs. Inner-CV R² log1p: none 0.598, OOF 0.656-0.658, published 0.666. OOF gains +0.058-0.061 inside the crawl against +0.048 on the test windows: little to exploit, training side only | LEAK-10 (weak) |
| 16 | Test rows keep the published statistics = the blog's training statistics; none match the test files | notes bullet 3 | decision table; vector lookup | holds | 1.0 and 0; every test vector occurs in the training file | LEAK-10 |
| 17 | "Every test blog is in the training file (a known blog, USE-10)" | notes bullet 3; record; builder (hidden groups 99.9%) | rows whose 50 statistics are all zero, which match vacuously | **refuted for up to 9.4% (circumstantial)** | 719 test rows (9.4%) carry the all-zero vector. Of them, 24.6% have comments before the base time and 15.9% trackbacks. The zero-vector training rows have 0% of both (by construction), and known low-activity blogs have 11.9% with comments. So these are likely blogs without training rows, with 0 as a placeholder. The model stays calibrated on them: P(comment) 0.124 / 0.047 / 0.036 predicted against 0.116 / 0.059 / 0.035 observed | USE-10, SPLIT-13, CLEAN-10 |
| 18 | No post is in both parts | notes bullet 3; record Assessment | (statistics, text, publication weekday) key across the parts | holds in substance | 40 text-bearing test rows (8 keys, 4 blogs) share a key with training rows. They are templates: no frequent word, length 58-1,483, 92.5% zero target, max 1. The crawls are 2010-11 against 2012 and posts are at most 72 h old | LEAK-17 |
| 19 | "scores the same with published, recomputed or no statistics on ROC AUC (0.908, 0.908, 0.892) and R² on log1p (0.656, 0.657, 0.609)" | notes bullet 4 | re-run on the shipped windows, 2 seeds | numbers hold; **wording refuted** | shipped 0.908 / 0.655, none 0.892 / 0.609: "no statistics" is lower, not "the same". On the declared rmse the order flips (none 23.69 against shipped 24.02; builder e8: counts only 23.31, best), and the sentence does not say so | EV-8, writing |
| 20 | "the leak sat in the training rows only" | notes bullet 4 | 16 + published against OOF on test | holds | AUC 0.908 = 0.908; test statistics come from the training crawl only | LEAK-10 |
| 21 | Parents: change in 22% of 792 posts, down as often as up; 5% of rows; dropping them changes no score | notes bullet 5 | re-count; drop test | holds | 22.6% of 780; max up 125 / down 99; 5.3% train, 3.0% test; without them R² 0.6553 against 0.6549, AUC 0.9077 against 0.9083, Hits@10 6.53 against 6.56 | LEAK-10 (kept note) |
| 22 | "Revisit if Buza's chapter documents them" (parents) | notes bullet 5 | chapter Sec. 4.2 item 4 | untested; chapter now read and silent | defines "minimum, maximum and average number of feedbacks that the parents received", with no time | LEAK-10 |
| 23 | Copies: 3,194 training and 588 within-day test copies dropped; kept: 17 across days, 13 pairs, 410 rows (99.5% text-less); "most next to the original" | notes bullet 6; decision 2 | recount | holds | 3,194; 588. 17 groups (34 rows) 7-42 days apart, all target 0, 11 of them spanning two windows. 13 duplicates in the shipped frame, all text-less. 411 rows, 99.48% text-less. 55.5% of training copy groups adjacent, 70.3% within 2 rows | LEAK-19, LEAK-20 |
| 24 | Parents' statistics a stored 0 without a parent → missing | notes bullet 7 | raw | holds | `parent_comments_*` all 0 wherever `parent_posts` = 0 (train and test) | CLEAN-10 |
| 25 | 4 constant columns, 24 copies of another column | notes bullet 7 | raw | holds | each constant 0; each copy equal to its source; `word_003` set in the 4 rows that have all 200 words | CLEAN-5 |
| 26 | Weekday blocks Monday first | notes bullet 8 | base block against file dates; publication block against base − ceil(age/24) | holds | base 100%; publication 97.6% test / 98.1% train against ≤2.4% for every other rotation; UCI lists "Monday...Sunday" | CLEAN-12/13 |
| 27 | Word columns: "presence flags of frequent words the source does not name" | notes bullet 8 | 2012 readme; chapter Sec. 4.2 and footnote 1; drop test | **refuted (description)**; 0/1 and categorical hold | readme: "The 200 most significant bag of words features". Chapter: "the most discriminative bag of words features", picked by the mean and sd of "the number of feedbacks of documents" with and without the word: a selection that uses the label, on documents it does not name. Without the words: R² log1p 0.6559 against 0.6549, AUC 0.9073 against 0.9083, Hits@10 (log model) 6.63 against 6.56, rmse 23.12 against 24.02: no signal | LEAK-31, CLEAN-14 |
| 28 | Length 0 and no word: 24% train, 20% test | notes bullet 9 | raw | holds | 24.33% / 20.09%; every length-0 row has no word | - |
| 29 | `basetime_day` 1 = 1 Feb, 60 = 31 Mar 2012; 0 = crawl | notes bullet 10 | dates | holds | 60 distinct days, 2012 is a leap year | - |
| 30 | A temporal definition cannot declare a grouping | notes bullet 11 | code | holds | `src/data_foundry/v2/dataset.py:1321`: "a task is grouped or temporal, not both" | - |
| 31 | UCI: use "the provided, temporally disjoint train and test splits" | splits_comment | UCI text | holds (verbatim) | - | SPLIT-19 |
| 32 | The source trains once and tests on the test days; the oldest window is its design on days 1-20 | splits_comment | chapter Sec. 5.1 | holds (primary) | "we used the blog documents from 2010 and 2011 as train data and ... February and March 2012 as test data" | SPLIT-19 |
| 33 | A label is known at the next day's base time, so no gap | splits_comment | file times 00:00; window edges | holds | the last training day's labels close at the first test base time | SPLIT-9/10 |
| 34 | Nine folds for an IID task of this size | splits_comment | `recommended_dimensions` | holds | 56,239 rows → 3 repeats × 3 folds | SPLIT-15 |
| 35 | Metric reason: "UCI states no metric" | metric reason | UCI page and API | holds | no metric named | MET-1 |
| 36 | Metric reason: "Buza's chapter (Springer 2014, closed access, not read) ... according to Singh et al. 2015 ... from a secondary source" | metric reason; record screening | search once more (MET-1) | **refuted** | the author's copy is open (cs.bme.hu, Last-Modified 2013-02-04) | MET-1, MET-11, EV-7 |
| 37 | The chapter evaluates per test day with Hits@10 and AUC@10; two measures side by side | metric reason | chapter Sec. 5.1, p. 5; Table 1 | holds (primary) | "For each day of the test data we consider 10 blog pages ... We call this evaluation measure Hits@10 and we average Hits@10 for all the days"; AUC@10 with the true top 10 as positives. Table 1 reports both for every model and names neither as the criterion | MET-5 |
| 38 | Neither measure is in the metric library | metric reason | `METRICS` registry | holds | no per-group top k or per-group AUC for regression; `precision_at_k` is binary only | MET-13 |
| 39 | rmse can be computed on every fold | implied (MET-2) | scorer with a dummy on each fold | holds | dummy 29.393 / 32.061 / 33.230; 20 days per window, 79-209 rows a day; no scoring column needed | MET-2 |
| 40 | rmse scores the decision of the use case (MET-1 is cited for the fallback) | metric reason; use case "decides each day which recent posts to feature" | six predictors per window: rmse and rmsle against the source's per-day Hits@10 | **questioned (weighing call)** | Kendall tau between −rmse and Hits@10: 0.30, 0.30, 0.89 (rmsle 0.75, 0.60, 0.60). A rescaled naive forecast (same ranking) scores rmse 25.3 to 53.7. Window 1-20: naive × 0.5 at 25.29 ≈ LightGBM L2 at 25.17, and both beat LightGBM-log (26.58), which has the best Hits@10 (6.60 against 5.25). Window 21-40: Poisson LightGBM rmse 30.69, near the dummy's 32.06, with Hits@10 7.05. The top 1% of rows (23-26 per window) carry 68-92% of the squared error. In the drop tests rmse prefers "no blog statistics" while R², AUC and Hits@10 do not | MET-1, MET-10 |
| 41 | rmse on the source's scale | metric (identity) | spec | holds | `target_transform='identity'`, raw counts | MET-3 |
| 42 | README origin text "the source defines no metric" | generated README, Metric block | against the reason | **contradicts the reason** (template wording) | the source defines two measures | MET-11 |
| 43 | year "2014", source "UCI" | dataset.py metadata | compare with the 2012 release | **refuted** | all 61 CSVs are byte-identical to `blogdata.zip` (Last-Modified 2012-07-24, files dated 2012-07-24), which chapter Sec. 5.1 gives as "publicly available at http://www.cs.bme.hu/~buza/blogdata.zip"; UCI's 2014 donation is a re-upload | PROV-8, PROV-9 |
| 44 | Licence CC BY 4.0 | metadata | UCI page | holds (note only) | UCI: "licensed under a Creative Commons Attribution 4.0 International (CC BY 4.0) license"; the 2012 readme states no licence | EV-4 |
| 45 | 60,021 instances, 280 features, 64.0% / 70.2% zeros | record screening | raw | holds | 52,397 + 7,624; 281 columns; 64.05% / 70.19% | - |
| 46 | "the chapter not read"; "the earlier AI's reading that the chapter ranks by Hits@10 is unverified" | record screening and Assessment | chapter | **refuted / settled** | read; per-day Hits@10 and AUC@10 confirmed | EV-7 |
| 47 | Assessment figures: next-day a51 in "99.8%"; "a52 ... 99.9% of consecutive test pairs"; "0.1%"; "12,461 posts" | record Assessment | recount | **superseded** | 99.89%; 99.73% for test pairs (99.92% is the training figure); 0 in the decision table; 12,526 | EV-2 (later stage wins) |
| 48 | "The leak is resolved" | record Assessment; CC | 15, 16, 20 | holds for the test side | small residual shift on the training side (15) | LEAK-10 |
| 49 | LightGBM beats each post's best naive forecast | builder TP-10 | e9 script read (scale fitted on the train side) | holds | 22.5 / 23.9 / 25.2 against 28.3 / 26.8 / 25.9; small margin in window 1-20 | TP-10 |
| 50 | rmse on counts rests on about 1% of rows | builder issue 5 | 40 | holds | 68-92% of squared error in the top 1% of rows, for every predictor | MET-10 |
| 51 | Not leave-one-post-out keeps the training rows clean for tuning | implied by bullet 2 | 15 | partly refuted | as 15 | LEAK-10 |
| 52 | Every feature is known at the base time | implied | chapter and UCI; 21, 27 | holds except two untested points | words picked with the label (27; which documents is not stated); parents' counting time not stated (22). Both drop tests are flat | LEAK-10, LEAK-31 |
| 53 | The data are what the source evaluated (faithful) | implied | Hits@10 of untuned LightGBM against the chapter's Table 1 | holds | window 1-20 (the chapter's design): Hits@10 6.0 (L2) and 6.6 (log); chapter's models 5-6.2, its per-source naive 2-3 | PROV |
| 54 | No row is a copy across the split | implied | leak probe; copies across days | holds | 0.0% exact copies of test rows in train; the 11 cross-window copy groups differ only in `basetime_day` and are all target 0 | LEAK-16 |

**Refuted and untested claims, ranked (principles.md: validity first, then by strength)**

1. **P3, USE-1 (Must): "The source names no actor" (6, 8).** The chapter names the partner (Capgemini Magyarország Kft.) and the decision: a company that has to react quickly to negative news in social media, where reading every post is hopeless. *What it changes:* the use case can cite the source instead of "for example", and `fit_reason` loses its first gap. The fit stays approximate because the training statistics still come from the undated crawl. *Mildest remedy:* rewrite `use_case` and `fit_reason` from chapter Sec. 1 and the abstract; no data change.
2. **P4, LEAK-31 (Should): the 200 word flags were picked with the label, not as "frequent words" (27, 52).** Footnote 1 picks the 200 words with the largest standardised gap in feedback counts between documents with and without the word. The documents used are not named and may include February-March 2012; that cannot be tested without the full vocabulary (untested). Measured, the words carry nothing: R² log1p −0.001, AUC +0.001, Hits@10 −0.07 with them. *What it changes:* the notes' description, and a kept-leak note is needed. *Mildest remedy:* keep them with a `Potential leak, kept on purpose:` note citing footnote 1 and the drop test (LEAK-31: "keep with a note when small"). Or drop the 178 word columns: cheap, no loss, and the precedent of qsar_bioconcentration's 9 descriptors (+0.002, dropped). Curator's call.
3. **P4, USE-10 / SPLIT-13 (Should): "Every test blog is in the training file" (17).** For 719 test rows (9.4%) the all-zero statistics match vacuously, and their activity (24.6% with comments, 15.9% with trackbacks) points to blogs without training rows, where 0 stands for "no history". The evidence is circumstantial (EV-6), and the rows cannot be told apart one by one. *What it changes:* the notes' sentence and the hidden-groups reading ("99.9%"). It costs no score: untuned predictions are calibrated on these rows. *Mildest remedy:* rewrite the note: "90.6% of test rows carry statistics found in the training file; 9.4% carry the all-zero vector, which cannot tell a silent known blog from a blog without training rows."
4. **P4, LEAK-10 (weak, training side only): the 5-fold statistics still move with the post's own outcome (15, 51).** This is the k-fold version of the leave-one-out shift the notes reject. It is strongest in small blogs (Spearman −0.23 against the own target in blogs with 2-5 posts, where 5 folds amount to leaving one post out). It barely gives anything to exploit: inner-CV gain +0.058-0.061 against +0.048 on the test windows, and published statistics +0.067. *What it changes:* the claim's wording, and tuning folds on the training rows are slightly optimistic. Test scores are unaffected. *Mildest remedy:* say it in the note. More folds make it worse; statistics from a held-out half of each blog would cost training rows for no measured gain.
5. **P5, PROV-8 / PROV-9 (Must): year and source (43).** First published in 2012 on Buza's page with the same bytes, linked from the chapter. *What it changes:* `year = "2012"`, `source = "Other"` with `source_url` pointing to the 2012 release (or its page), the UCI zip named as the download copy, and the BibTeX for the chapter plus the release. Metadata only.
6. **P6, MET-1 / MET-11 (Must): the fallback's reason says "closed access, not read ... secondary source" (36, 46).** The chapter is readable and confirms per-day Hits@10 and AUC@10, reported side by side in Table 1. *What it changes:* the reason text. The fallback still stands on MET-5 from the primary text (gallstone_disease precedent: several metrics reported → fallback). *Mildest remedy:* cite chapter Sec. 5.1, p. 5 and Table 1, and drop "not read" and "secondary". The record's screening and Assessment lines get the same update (46, 47).
7. **P6, MET-1 / MET-10 (weighing call): does rmse score the decision? (40, 19).** The use case and the source both act on the top posts of each day. Raw-count rmse ranks predictors against Hits@10 at tau 0.30 in two of three windows. It moves with any rescaling of a forecast that leaves the ranking unchanged, 23-26 rows per window carry most of the score, and it prefers dropping the blog statistics where every ranking measure does not. *What it changes:* possibly the declared metric. *Options for the curator:* (a) keep the rmse fallback (MET-5's letter, precedent); (b) a per-day top-k metric added to the library (MET-13 work; MET-2 then needs the day as a scoring column, not a feature, while today `basetime_day` is also a feature); (c) a context metric such as rmsle (onlinenewspopularity precedent; rank agreement 0.60-0.75 here). Note that MET-11's `context` is for sources without a metric, and this source has two.
8. **Writing and evidence (EV-2, PROV-16; procedure): the misquote and the wording (3, 12, 19, 42).** The UCI quotation in bullet 1 is not in UCI's text. "554 Hungarian blogs" counts distinct statistic vectors, so it should read at least 554, with the chapter's "roughly 1200 sources". "Scores the same with ... no statistics" contradicts its own numbers and leaves out rmse. The generated origin line "the source defines no metric" contradicts the reason. *Mildest remedy:* quote UCI's actual sentence and fix the sentences. Item 42 is a template (the fallback origin text), possibly a code fix.
9. **Untested.** When the parents' comment counts were taken (the chapter is silent, and dropping the parents is flat, so the kept note stands; replace "Revisit if Buza's chapter documents them" with "the chapter (Sec. 4.2) does not say when"). Which documents picked the words (item 2). Whether every all-zero test row is an unseen blog (item 3).

**Files.** The scripts, their outputs and the texts read (the chapter, Singh et al. 2015, the 2012 readme, the UCI record) are in the run folder.

</details>

<details><summary>Column audit</summary>

**Column audit: blogfeedback (column-auditor, 2026-11-01)**

Inputs: `dataset.py` and `README.md` of `datasets/_dev/tabarena-v0pt2/blogfeedback/`, the record, the builder report and probes, UCI's attribute list (the UCI API, `variable_info` and `additional_info`; the zip ships no readme), and the frame rebuilt through `dataset_io.from_definition` (56,239 rows x 242 columns). Buza's chapter not read (closed access). Scripts and outputs (c1 to c8) are in the run folder.

```text
Verdict: ship after changes (notes and one cheap cleaning step; no column has to go).
Validity: LEAK-10 holds column by column: the blog-statistics fix holds, and the post key that sets the folds keeps a post's rows together (99.7%). The parents' columns behave like counts taken at the base time, so the kept-on-purpose note gives the wrong mechanism (fix the wording). UCI is misquoted in the prediction-point bullet.
Value: nothing at column level.
Quality: CLEAN-10 departure (post_length 0 is a text-extraction gap per blog); CLEAN-16 departure without a stated reason (raw count target, while this run's count siblings ship log1p).
For the curator: post_length 0 to missing (yes/no; word flags too?); target scale (log1p with target_transform, or say why raw).
```

**Column table**

Every column of the cleaned frame. Columns treated the same way share a row.

| column | meaning (UCI attribute list) | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| `blog_comments_total_{mean,std,min,max,median}`, `blog_comments_last_24h_{mean,std,min,max,median}`, `blog_comments_24h_to_48h_before_{mean,std,max,median}`, `blog_comments_first_24h_{mean,std,max,median}`, `blog_comments_change_24h_{mean,std,min,max,median}` (23) | a1-a25: mean, std, min, max, median of a51-a55 "for the source of the current blog post" (the blog) | Test rows: yes, these are the blog's statistics over its training rows (decision table: 100% match; 0% match with the test-only statistics). Training rows: recomputed out of fold from the blog's other posts in the undated crawl, so later posts are included (blog-level look-ahead; the post's own rows are out) | float64; 250 training rows (69 blogs) are missing; test rows never are. Out-of-fold max is below the all-rows max in 23% of training rows (mean ratio 0.91), a mild shift between training and test rows that comes with out-of-fold and is not a leak | fine: leak fixed, the weak remainder is named in `fit_reason` | LEAK-10, LEAK-34, USE-10 |
| `blog_links_total_{mean,std,min,max,median}`, `blog_links_last_24h_{mean,std,max,median}`, `blog_links_24h_to_48h_before_{mean,std,max,median}`, `blog_links_first_24h_{mean,std,max,median}`, `blog_links_change_24h_{mean,std,min,max,median}` (22) | a26-a50: the same for the trackback counts a56-a60 | as above | as above; `blog_links_24h_to_48h_before_median` and `blog_links_change_24h_median` are constant within the test rows (harmless) | fine | LEAK-10 |
| `comments_total` | a51: "Total number of comments before basetime" | yes: `comments_first_24h` never exceeds it, and equals it in every row of a post younger than 24 h | float64 holding integers 0-3,125; no missing values | fine | LEAK-10 |
| `comments_last_24h` | a52: comments in the 24 h before the base time | yes; equals the post's previous-day target (99.7% of 3,722 test pairs), the post's own history | float64 | fine | LEAK-34 |
| `comments_24h_to_48h_before` | a53: comments between 48 and 24 h before the base time | yes; 40 rows (0.07%) of posts under 24 h old have a value above 0, which reads as rounding of the hours | float64 | fine | |
| `comments_first_24h` | a54: comments in the first 24 h after publication, "but before basetime" | yes (checked as above) | float64 | fine | |
| `comments_change_24h` | a55: a52 minus a53 (exact in every row) | yes | float64; a derived source feature, not a copy | fine | CLEAN-5 |
| `links_total`, `links_last_24h`, `links_24h_to_48h_before`, `links_first_24h`, `links_change_24h` | a56-a60: the same for trackbacks | yes; first-24h never exceeds the total; change = a57 minus a58 exactly | float64, integers 0-30 | fine | |
| `hours_since_publication` | a61: "The length of time between the publication of the blog post and basetime" (no unit given) | yes | float64 holding the integers 0-72, so hours, matching the 72 h window; consistent with the weekdays (row below) | fine | |
| `post_length` | a62: "The length of the blog post" (no unit given) | yes | float64, 0-57,894. A value of 0 (23.8% of raw rows, never with a word set) means no text was extracted, and it clusters by blog: 100 of 554 blogs have no text in any row and hold 90% of the zero rows, and the same blogs stay text-less in the test files (31 of 32 that appear there). It is a proxy missing value, kept as 0 | cleaning problem | CLEAN-10 |
| `word_001` ... `word_200`, 178 kept (`word_011, 014, 018, 019, 032, 035, 068, 070, 087, 094, 099, 104, 107, 110, 117, 128, 136, 138, 150, 174, 181, 188` dropped as copies of `word_003`) | a63-a262: "bag of words features for 200 frequent words" (the words are not named) | yes (the post's text) | category; only 0 and 1 occur, even in posts of 50,000+ characters, so these are presence flags (the fingerprint-bit precedent). The vocabulary was chosen by frequency, which is unsupervised (CLEAN-8). In the text-less rows a 0 means "unknown", not "absent" (see `post_length`). `word_003` is set only in the 2 rows of one post that has all 200 words at length 3,501, probably an extraction artefact; 31 flags are constant within the test rows | fine (the missing-value question goes with `post_length`) | CLEAN-14, CLEAN-8 |
| `basetime_weekday` | a263-a269: one-hot weekday of the base time, Monday first | yes | category made from a one-hot block with exactly one flag per row; matches the weekday of the test file's date in 100% of test rows | fine | CLEAN-12, CLEAN-13 |
| `publication_weekday` | a270-a276: weekday of publication | yes | category; with a 00:00 base time it lags the base weekday by 1 / 2 / 3 days for ages 0-24 / 24-48 / 48-72 h in about 98% of rows, and the rest fall one day off at the boundaries. The block order is right, not reversed | fine | CLEAN-12, CLEAN-13 |
| `parent_posts` | a277: number of parents (P is a parent of B if B trackbacks to P) | yes; it falls as the post ages (702 of 731 changes between consecutive base times are decreases: parents leave a window), so it is known at each base time | float64 count 0-136 | fine | |
| `parent_comments_max`, `parent_comments_mean` | a279, a280: max and mean of the comments the parents received | evidence says yes. Within a training post whose parent set does not change, max and mean only rise between consecutive base times (96 and 97 rises in 1,587 pairs, no fall). They fall only when the set shrinks (325 of 702). That is the pattern of counts taken at each base time, not at one later crawl | float64; missing where `parent_posts` is 0 (the source stores 0 there), which is correct | fine; the note's mechanism needs correcting (problem 1) | LEAK-10 (second clause), CLEAN-10 |
| `basetime_day` | built from the test file names: day 1-60 (1 Feb to 31 Mar 2012); 0 for the undated training crawl | yes (the calendar) | int64; the time column and a feature. The 0 is a placeholder that a linear model reads as 31 Jan 2012, but a time column cannot hold missing values (`task_time_on_missing_values`), and the notes name it | fine, noted | CLEAN-3, SPLIT-7 |
| `comments_next_24h` (target) | a281: comments in the 24 h after the base time | the outcome | float64 holding integers 0-1,424; no cap; 65% zeros; skew 12.6 raw, 2.3 on log1p; shipped as a raw count | question | CLEAN-16 |
| dropped: 3 blog minimums (constant 0), `blog_comments_first_24h_min` and `blog_links_first_24h_min` (copies), `parent_comments_min`, the 22 word copies, the 14 weekday flags, `file` | | | `parent_comments_min` is a broken source column, not a true minimum: it is 0 in all 249 one-parent rows where max = mean > 0. Dropping it is right; the note's wording "a parent post's minimum of comments is 0 wherever there is a parent" hides the defect | right to drop | CLEAN-5 |

**Problems, ranked (principles.md: rank, then strength, then effect)**

1. **P4, LEAK-10 second clause (Must), documentation: the parents' kept-on-purpose note gives the wrong mechanism.**
   - What the note says: "may be counted when the parents were crawled ... they change between a post's base times in 22% of 792 training posts with a parent, down as often as up". It keeps the four columns because dropping them "scores the same". LEAK-10 says that test alone is no reason to keep.
   - What the data shows: over 1,106 text-bearing training posts that have a parent at some base time, consecutive base times 24 h apart show that with an unchanged parent set, max and mean only rise (96 and 97 of 1,587 pairs, no fall). Every fall comes with a shrinking set (702 of 731 set changes are decreases). Counts read at one later crawl could not rise between base times; counts read at each base time rise and never fall. So "down as often as up" mixes a shrinking parent set with the counts.
   - Mildest remedy: keep the columns and rewrite the bullet as a plain note with these numbers: "behave like counts at the base time; the parent set shrinks as the post ages". Drop the "Potential leak, kept on purpose" label, or keep it with the corrected evidence. Also reword the `CONSTANT` comment: `parent_comments_min` is a broken source column (0 even when the single parent has comments), not a true minimum of 0.
2. **P4, LEAK-1/USE-3 (Must), documentation: UCI is misquoted in the prediction-point bullet.**
   - The bullet's quotation "Features are computed only from information available at that basetime" is not in UCI's text. UCI writes: "we calculate all the features of the selected blog posts from the information that was available at the basetime".
   - Remedy: quote UCI verbatim.
   - A small number to fix at the same time: "251 rows of 69 blogs ... get missing values" is 251 before the copies are dropped and 250 in the shipped frame.
3. **P4, LEAK-10 (weak remainder, already named), confirming builder issue 2: the blog statistics hold column by column.**
   - The post key behind `post_folds` (blog, length, words, publication weekday) keeps a post together. Of 20,320 text-bearing training rows with a unique count-matched row 24 h later (same blog and publication weekday, hours +24, next total = total + target, next last-24h = target, next 24-48h = last-24h), 20,258 (99.7%) share the key. The 62 that differ all have a different length, so they are count twins of other posts, not edited posts. The own-outcome leak is gone. What remains is the named blog-level look-ahead.
   - Out-of-fold statistics run over 4/5 of a blog's rows and the test rows' over all of them, so the max columns sit lower in training (below the all-rows value in 23% of rows, mean ratio 0.91). That is a feature shift, not a leak.
   - No action. Optionally add one clause to the "Not removed" bullet.
4. **P7, CLEAN-10 (Should): `post_length` 0 is a proxy missing value.**
   - It is a text-extraction gap per blog, not empty posts. Evidence is in the table row. The notes call it "no text extracted" and keep 0 without a reason, which is a departure from CLEAN-10.
   - Cheap, safe remedy: in `_clean`, after step 3 (the fold key reads the raw values), set `post_length` to missing where it is 0, and name the per-blog pattern in the anomaly bullet.
   - Curator's call: whether the 200 word flags of those rows also become missing ("unknown") or stay 0 with the note. Tree models see the same information either way; linear models and neural nets do not.
5. **P7, CLEAN-16 (Should): the target ships as a raw count without a stated reason.**
   - This run's count datasets ship log1p targets and score on the count scale: `nantucket_sound_sea_duck_aerial_survey_counts` (`Metric.fallback(..., target_transform="log1p")`, "RMSE on the count") and `wadden_sea_sibes_macoma_abundance`. Lennart's CC on onlinenewspopularity reads "ship the target on the modelling scale, score on the original scale (target_transform)". Here the top 1% of test rows hold 84-86% of the dummy's squared error (builder).
   - Remedy: either `log1p_comments_next_24h` with `target_transform="log1p"` (the score stays RMSE on counts; what models fit changes), or one sentence in the notes on why the raw count stays.
   - This ties to builder issue 5 (metric), which the metric reviewers own.
6. **P7, minor, no action:**
   - `basetime_day`'s 0 is a placeholder, unavoidable for a time column and already noted.
   - The one post with all 200 words (2 rows) is probably an extraction artefact. It is the only reason `word_003` is not constant; harmless.
   - The parents' missing values (CLEAN-10) and the weekday merge (CLEAN-13) are correct.

**Checks that came back clean**

- Count consistency over all 60,021 raw rows: no first-24h above the total, no last-24h or 24-48h above the total, last-24h + 24-48h never above the total, and both change columns exact. Posts under 24 h old have first-24h = total in every row.
- Weekday blocks: Monday first, consistent with the file dates and with the age of each post.
- Missing blog statistics occur only in training rows and carry no outcome signal: 61.6% zeros against 64.8%.
- No object columns. No constant columns or numeric copies remain in the cleaned frame.
- No identifier encodes the label. The blog statistics work as a blog identity in the test rows, a known entity (USE-10, LEAK-34).


</details>

<details><summary>Split audit</summary>

**Split audit: blogfeedback (split-auditor, 2026-11-01)**

**Verdict: right with notes.** The regime is right: a temporal split on the source's own train/test split, with known blogs. The windows meet the Must rules. One Should departure is not yet recorded: three windows instead of the nine SPLIT-15 asks for. The reason given for it (SPLIT-19) is the weaker of the facts available. Nothing here needs a re-split, a gap or a filter.

```text
Verdict: right with notes.
Validity: SPLIT-1/SPLIT-3 hold (temporal, known blog; USE-10); SPLIT-5 checked against the data, holds; SPLIT-9 holds
  (no training label unknown at a window start); SPLIT-10 holds (gap 0 is correct); SPLIT-11 holds; SPLIT-14 holds
  (3 windows, train sides 87.5-95.4%); SPLIT-17 holds (2,225-2,564 test rows per window); SPLIT-13 holds (known posts
  across the window boundary are history). SPLIT-15 departed (3 windows, not 9): needs an exception line, with a better fact.
Value: n/a (the split costs 0.13 R^2 on counts against IID, so the split matters).
Quality: the post-grouped tuning note has no measured effect; basetime_day as a feature is harmless.
For the curator: issue 1, a weighing call (3 x 20 days with an exception to SPLIT-15, or 9 x 6 days).
```

All numbers below are mine, from the definition's frame and split plan loaded through `dataset_io.from_definition` (56,239 rows, 241 features), with untuned LightGBM (300 trees, lr 0.05, one seed) unless I say otherwise. Scripts and outputs are in the run folder.

**What I checked and found to hold**

- **Regime (SPLIT-1, SPLIT-3, USE-10).** The use case is a portal or monitoring service that ranks the recent posts of the blogs it follows, so the blog is known and the post is new. All 215 test blogs are in the training crawl (raw files: 100%; the probe's proxy column gives 99.9%). The decisive comparison over all rows, 3 folds:
  - IID random rows: R^2 0.560 on counts, 0.661 on log1p;
  - grouped by post: 0.577 and 0.658;
  - grouped by blog with the blog statistics dropped (a new blog has none): R^2 **-0.672** on counts, 0.502 on log1p;
  - the shipped temporal windows: 0.430 on counts (0.432, 0.431, 0.426), 0.654 on log1p.

  So a cold-start split would leave no signal on counts. On the source's data the known-blog temporal regime is the only one that fits. Against a random split it costs 0.13 R^2 on counts, so the split matters.
- **The prescribed split checked against the data (SPLIT-5, SPLIT-19).** UCI: "In the train data, the basetimes were in the years 2010 and 2011. In the test data the basetimes were in February and March 2012." No text-bearing post crosses from the crawl into the test files. 40 text-bearing test rows (8 post keys) share a key with the crawl, but these are template texts: no word set, a different age in 98% of the matched pairs, 92.5% zero targets. So they are not the same posts. A post without text cannot be identified, so the claim "no post is in both parts" cannot be checked for the 20% of test rows without text.
- **Windows (SPLIT-14, SPLIT-17).** Confirmed on the split plan:

  | Window (newest first) | Test rows | Train rows | Train share | Test days |
  |---|---|---|---|---|
  | 41-60 (12-31 March) | 2,564 | 53,675 | 95.4% | 41-60 |
  | 21-40 (21 February-11 March) | 2,225 | 51,450 | 91.5% | 21-40 |
  | 1-20 (1-20 February) | 2,247 | 49,203 | 87.5% | 1-20 |

  Each 20-day window holds 2 or 3 of every weekday, and the zero share is 69.6%, 72.0% and 68.9% (64.8% in the crawl). No window falls in an odd season: it is late winter, and 15 March, a Hungarian holiday, falls in the newest window. The `splits_comment` dates and counts are right.
- **Gap and late labels (SPLIT-9, SPLIT-10).** The test files are dated at 00:00 each day, and the next day's `comments_last_24h` equals a row's target in 99.7% of 3,722 consecutive test pairs. A row's label is complete at the next file's base time. The last training day before a window (day 20, day 40) therefore has its labels at the window's first base time, and the crawl (2010-2011) ended at least a month before the test. No training row has a label that is unknown at its window's start, so gap 0 is correct.
- **Known entities across the cut (SPLIT-13).** In windows 21-40 and 41-60, 6.5% and 6.0% of the text-bearing test rows belong to a post that also has a row on the train side (the earlier test days), mostly on the window's first two days. Window 1-20 has none. This is the post's own history, which a daily ranking has. It is legitimate.
- **Copies across the split (LEAK-16 to LEAK-19).** Leak probe 5 reads 0% exact copies, but that 0 comes from the recomputed crawl statistics. On the 280 published features, 80 test rows (1.1%) have an exact copy in the crawl. Of these, 78 have no text, all come from 8 blogs (43 rows from one), the median age is 13 h, and the counts are small. Their target equals a crawl copy's target in only 44%. These are natural repeats (LEAK-18), not leaked labels, so no action. The 588 copies dropped within a test day are the same post at the same base time (LEAK-19). Dropping them does not change what the test stands for.

**Problems, ranked (all P4; none is a Must)**

1. **Three windows instead of nine; the departure is not recorded and its reason is weak (SPLIT-15, Should).**
   - The rule: a frame of 56,239 rows would get 3 x 3 = 9 IID folds (`recommended_dimensions`). The `splits_comment` departs and cites SPLIT-19. A Should departure needs the fact that sets the case apart and an `Exception to SPLIT-15` line in the record (principles.md), and the record has no such line.
   - Why SPLIT-19 is weak: the source trains once on the crawl and tests all 60 days. That is one window, which SPLIT-14 forbids, so neither 3 nor 9 windows is the source's design.
   - The stronger facts, which I measured:
     - The test pool is fixed. The crawl is one undated time value (`basetime_day` 0), so windows can only be cut from the 7,036 rows of the test days. Finer windows add no test rows (SPLIT-17's reasoning). This differs from rain_in_australia, where more windows tripled the test rows.
     - Under the declared `rmse` the score rests on a handful of rows. Against the training mean, the top 5 rows hold 41-50% of the squared error of a 20-day window, but 62-83% in each of nine 6-day windows (the top 1% of rows hold 71-87%).
     - The source applies one 2010-11 model to all 60 days, so a 20-day refit horizon is not too long for this task (SPLIT-12).
   - Against the departure: the use case is a daily decision, and SPLIT-18 (short-lived quantities) would favour shorter windows.
   - For information only, since SPLIT-21 forbids choosing windows by score: nine 6-day windows (days 7-60) give a mean LightGBM R^2 of 0.423 (SE 0.043; per window 0.27-0.68) and log1p 0.659 (SE 0.017). The three shipped windows give 0.430 and 0.654.
   - Mildest remedy: keep 3 x 20 days, record `Exception to SPLIT-15` with the fixed-pool and heavy-tail facts, and put those facts in place of "closest to the source's protocol" in `splits_comment`. The alternative is `TemporalSplits(window=6, unit="unique", n_windows=9)`, which leaves days 1-6 untested. This is the curator's weighing call.

2. **The training history cannot be checked for breaks (SPLIT-20, Should).**
   - The crawl is one time value, so neither a recent stretch nor a full season can be chosen, and the break between the crawl and February 2012 cannot be located.
   - The break shows in the data: 554 blogs in the crawl against 215 in the test; zero share 64.8% against 69-72%; mean 6.71 against 5.26-5.92; maximum 1,424 against 480-657.
   - The test rows' blog statistics are at least a month old, while the crawl rows' statistics are contemporaneous.
   - `fit_reason` names the undated crawl but not the drift. Remedy: none to the split, which is the source's design. One clause in `splits_comment` (the crawl is a single time value, so the history cannot be trimmed) would say why SPLIT-20 is not applied.

3. **The training rows' recomputed statistics differ in kind from the test rows' (LEAK-29 holds; a note).**
   - Out of fold, the blog maximum is the maximum over 4 of 5 folds of posts. It is below the full-crawl maximum in 22% of crawl rows (mean 307 against 326 for `blog_comments_total_max`), and the test rows carry the full-crawl value. Means and medians are unbiased (OOF/published median ratio 1.00-1.01).
   - This is a small train/test shift that the fix creates. It is not a leak: both sides are computed from the crawl only, before the oldest window, so LEAK-29 holds.
   - The column auditor's call. No change proposed.

4. **The note on tuning folds has no measured effect (SPLIT-13; quality).** The note says a harness should keep a post's rows together. On window 1-20's train side (the crawl), 5-fold LightGBM gives R^2 0.581 on random rows and 0.581 on whole posts (log1p 0.660 and 0.659), even though 96.7% of a random fold's test rows have their post on its train side. Without a post id, the features of one post change between base times, so the recurrence gives no shortcut. Remedy: keep the bullet with this number, or drop it. Either way it changes no score.

5. **`basetime_day` is both the time column and a feature: harmless, but 0 stands for two years (a note).** It is constant on the oldest window's train side, so it has no effect there (R^2 0.426 with and without). Without it: window 21-40 R^2 0.421 against 0.431, window 41-60 0.464 against 0.432; log1p is unchanged (0.597/0.594, 0.700/0.701). It is known at the prediction point (USE-6) and the definition documents it. Remedy: none. I do not propose dropping it from these numbers either way (SPLIT-21).

**For other panel members (not split problems)**

- On the declared `rmse`, the shipped blog statistics cost score. RMSE is 23.81 with them and 23.17 without (R^2 0.430 and 0.459, temporal windows, one seed); the builder's e8 gives 24.09 and 23.51. They help on log1p (0.654 and 0.613) and ROC AUC. The `curation_comments` claim "scores the same with published, recomputed or no statistics" is shown only on AUC and log1p.
- This fits rmse resting on about 1% of the rows (issue 1) and is a metric question (MET), not a split one.

</details>

<details><summary>Domain practitioner</summary>

**Domain practitioner (blogfeedback): verdict**

I play the actor the source itself names: a social-media monitoring service for companies. Buza built the dataset as "a proof-of-concept industrial application, developed in cooperation with Capgemini Magyarország Kft." (chapter, abstract). His reason: "if negative news appear in social media about a company, the company might have to react quickly", and "analysis of all these documents by human experts is hopeless" (Sec. 1). Each morning I rank the posts published in the last 72 hours on the Hungarian blogs I monitor by the comments each will draw in the next 24 hours, and my analysts follow the top of that list. That is also how the chapter scores its models: "For each day of the test data we consider 10 blog pages that were predicted to have the largest number of feedbacks" (Sec. 5.1).

- **Fit: approximate.** The test frame is my daily decision: posts at most 72 hours old on blogs I already monitor, scored at that day's base time from what was known then, on later days than the training data. The undated training crawl is the gap. The training rows' blog statistics come from the blog's other posts at any time, and the test rows' statistics are frozen at the 2010-2011 crawl, where I would update mine every day. So the features do not fully mirror the use case (USE-8). The first gap in `fit_reason`, "the actor is our example", is wrong. The chapter names the setting, so drop that gap and take the actor from the source (USE-1). USE-9 does not lift the fit to direct, because any use case trains on past days and keeps the training-side gap.
- **Metric: partly.** RMSE separates models from the constant. Among good models it prefers the one I would rank last. I would choose Buza's Hits@10 per test day (MET-1, MET-7, MET-9). If the curator reads MET-5 strictly, the fallback should be `rmsle` from context (MET-11), not RMSE.

**Correction that changes several claims: Buza's chapter is readable**

`dataset.py` (metric reason, `curation_comments`), the README and the record all say the chapter is "closed access, not read". An open-access author copy is linked from Semantic Scholar (openAccessPdf, status GREEN): http://www.cs.bme.hu/~buza/pdfs/gfkl2012_blogs.pdf (8 pages). I downloaded it and read the text. What it settles:
- **The actor and the motivation.** The industrial partner is Capgemini Magyarország, and the chapter explains why a company needs fast automatic analysis of blog posts. `use_case` and `fit_reason` should cite this, not "The source names no actor".
- **The metric, from the primary source.** Hits@10 is defined in Sec. 5.1: of the 10 posts predicted to get the most feedback each test day, how many are among the 10 that actually got the most, averaged over all test days. AUC@10 is the same day's ROC AUC with the true top 10 as positives. Table 1 and Fig. 1 report both. The text argues from Hits@10: "The number of hits was around 5-6 for the examined models, which was much better than the prediction of a naive model, i.e., of a model that simply predicts the average number of feedbacks per source. This naive model achieved only 2-3 hits." The day as base time is stated for both periods: "In both time intervals we considered each day as baseTime".
- **The 200 words are not "frequent words".** Footnote 1 says they are "the most discriminative bag of words features". A word's score is the difference in average feedback between posts that contain it and posts that do not, divided by the sum of the two standard deviations, and the top 200 were kept. That is a selection by the target, on documents the chapter does not state. I measured it on the shipped windows: log1p LightGBM gives R^2 0.656 with the words and 0.657 without, and ROC AUC 0.901 either way (2 seeds x 3 windows). Buza's Table 1 agrees, since adding the textual features lowers Hits@10 for most models. So the selection carries no test-period signal. Still, `curation_comments` ("frequent words the source does not name") and the `WORDS` comment ("200 frequent words") should say how they were chosen.
- **Two open items the chapter does not settle.** It describes the blog statistics only as "aggregation of the above features by source", with no period. It describes the parent features as "minimum, maximum and average number of feedbacks that the parents received", with no counting time. The parents' bullet ("Revisit if Buza's chapter documents them") can be closed: the chapter has been read and does not document either.
- **Context for the split.** Fig. 2: "recent training intervals, such as the last one or two months of 2011, seem to be informative enough", and with more history "we did not observe a clear trend", which suggests drift. As a practitioner, I would retrain on recent weeks. The undated crawl prevents that, while the expanding windows over earlier test days allow it in part.
- **Scale.** The crawl was "37279 pages from roughly 1200 sources". The definition's "554 Hungarian blogs" is a count derived from the data; the claim auditor may want to say so.

**The five questions, as the monitoring analyst**

1. **Inputs at the prediction point (USE-3, USE-6).**
   - **What I have at the morning base time:** comment and trackback counts in the 24-hour windows, the post's age, its length and words, both weekdays, and the blog's history. The blog's history is a legitimate input, because I monitor known blogs (USE-10).
   - **The parents' comment counts:** probably known at the base time. Their counting time is unknown; they are kept as a potential leak, cover 5% of rows and do not change the score. This does not touch the fit (USE-8).
   - **What I would not have, or would have in another form:**
     - In training, the out-of-fold blog statistics include the blog's later posts. That is not leakage into the test, but it is not what I would have computed.
     - At test time the statistics are months old. I would recompute them every day over my archive up to yesterday, including January 2012 and the earlier test days.
   - **What I would always have and the data lacks:**
     - A blog identifier. The 50 statistics act as one anyway.
     - Finer comment timing, such as comments in the last hour or last 6 hours. Velocity is what tools like NewsWhip use to forecast the next 24 hours.
     - The post's title and text, beyond 200 anonymized flags.
     - Whether the post names my client.
   - Missing inputs do not make the fit approximate, and none can be recovered from the release.
2. **The target (USE-5).** Comments in the next 24 hours is the quantity I watch: discussion volume, Buza's "feedbacks". What I act on is its rank within the day, plus a possible alert above a level, so a number (the expected comments) is the right thing to predict and serves both. The count is not censored. The 65-70% zeros are real days without comments. On 60 test days the 10th-largest true count has a median of 8.5 and is at least 1 every day, so every day has a real top 10.
3. **One row against one decision.** A row is one candidate on one day's list: a post at one base time, re-ranked on each of up to three days. The decision is the day's list of 79-209 posts (median 116). So the unit I act on is the day, not the row. The test data is what I face: the next days' new posts, on blogs already in my archive (99.9% of test rows; USE-10). Training on the crawl plus the earlier test days in 20-day windows is like retraining every few weeks, which is plausible. A label is known at the next day's base time, so no gap is needed.
4. **Would I use it?** Yes, as a ranking aid.
   - Today's rule on a monitoring desk is to sort by the comments of the last 24 hours. It finds 5.63 of the day's true top 10.
   - Untuned log1p LightGBM finds 6.67, which is +1.03 posts a day (paired SE 0.14, 60 days). Buza's own baseline is the blog's average. Its closest proxy here, the blog's mean comments of the last 24 hours, finds 3.83.
   - Of the true top 10, 7.0 posts a day are younger than 24 hours at the base time. The model catches 4.85 of them, the velocity sort 3.67. Fresh posts are where the model earns its place.
   - It would lose my trust if it ranked old, comment-less posts high, or if its daily top 10 shifted with the seed.
5. **Does the metric score my decision?** Partly; see below.

**The metric, measured on the shipped windows**

- **Setup.** Untuned LightGBM (400 trees) on the three windows, 2 seeds. Four objectives (L2 on raw counts, L2 on log1p, Poisson, Huber) and three naive rules, each scored by RMSE and by the daily top-10 measures.
- **Result.**

| model | RMSE | RMSLE | Hits@10 per day | AUC@10 | NDCG@10 per day | ROC AUC any comment |
|---|---|---|---|---|---|---|
| LightGBM L2, raw counts | **23.95** (best) | 0.868 | 6.16 (worst LightGBM) | 0.932 | 0.755 | 0.853 |
| LightGBM L2, log1p | 24.02 | **0.619** | 6.68 | **0.949** | 0.775 | **0.901** |
| LightGBM Poisson | 24.51 | 0.737 | 6.43 | 0.947 | **0.779** | 0.892 |
| LightGBM Huber | 27.69 (worst LightGBM) | 0.651 | **6.70** | 0.948 | 0.762 | 0.894 |
| sort by comments of the last 24 h | 44.00 | 1.044 | 5.63 | 0.898 | 0.647 | 0.853 |
| the training mean | 31.56 | 1.842 | 1.08 | 0.500 | 0.056 | 0.500 |

- **What it shows.**
  - RMSE puts first the model that is last on every daily measure, and last the model that is first on Hits@10.
  - Paired by day (seed 0), the log1p model beats the raw-count model by 0.57 hits a day (SE 0.115; better on 33 days, worse on 7), while their pooled RMSE is tied (24.05 against 24.08).
  - RMSE rates the desk's velocity sort as worse than a constant, although the sort finds five times as many of the top posts.
  - The builder found that the top 1% of test rows hold 84-86% of the dummy's squared error. So RMSE mostly scores how well a model sizes a handful of viral posts, not how well it ranks the day.
- **Why the metric falls short (MET-1).** MET-1 asks for my decision at the unit I act on, and my unit is the day's top 10.
- **What I would pick: Hits@10 per test day, Buza's measure** (`Metric.source`, reference: the chapter, Sec. 5.1).
  - **MET-7 and MET-9:** the source fixes how many it acts on (k = 10 per day). AUC@10, reported beside it, scores the same top 10 and is not a competing criterion, so MET-5's concern about several generic metrics side by side applies only weakly. The curator decides how strictly to read MET-5.
  - **MET-2:** the day exists in our data. `basetime_day` holds 20 whole days per test window, and every day has at least 10 posts with a comment. A metric input that is also the time column is allowed (bundle info `task_metric_input_is_model_input`).
  - **MET-12 and MET-13:** this needs a new custom metric under a general name, for example a mean per-group top-k overlap with group = `basetime_day` and k = 10, with a reference implementation. Its tie rule at the 10th place must be stated: counting ties at the 10th place as hits gives 6.68, the strict version 6.52.
  - **MET-10:** the resolution held here. Seed spread is at most 0.2 hits a day, while model differences were about 0.5.
- **Smoother alternative.** NDCG@10 per day, weighted by comments. It is not the source's measure.
- **If MET-5 is read strictly (no unique original).** Declare `rmsle` from context (MET-11), like `onlinenewspopularity` (a heavy-tailed engagement count whose error matters relative to the count). It is in the library and needs no scoring column. On these windows it orders the LightGBM variants close to the daily measures: log1p first and raw counts last, as do AUC@10, Spearman per day and the share of the day's comments captured. RMSE gives the reverse.
- **The current metric reason should change.** It should cite the chapter itself, not "according to Singh et al. 2015", and say why the daily top 10 was or was not adopted.

**Gaps between the dataset and the real decision, ranked by how much they change the task**

1. **The metric pools rows; the decision ranks a day.** This changes which model wins (table above). It can be fixed in the definition (MET-1, MET-7).
2. **The undated training crawl.** The training rows' blog statistics are from the blog's other posts at any time, not point-in-time, and recency weighting is impossible, though Buza shows recent months suffice. This is the gap that keeps the fit approximate (USE-8). It is measured to leave the test score unchanged (AUC 0.908 published against 0.908 recomputed), so it is about realism more than bias.
3. **Stale blog statistics at test time.** They are frozen at the end of the crawl, where I would update them daily. This makes the task slightly harder than mine and is the source's design. Optional, low priority: recompute the test rows' statistics over the crawl plus the earlier test days.
4. **Inputs I would have that are absent.** Finer comment timing, the text, a client mention. They cannot be recovered and do not change the fit.
5. **Wording only.** "The source names no actor", "closed access, not read" and "200 frequent words" are contradicted by the chapter.

**What an expert in the domain would change**

- Take the actor from the chapter: Capgemini Hungary's social-media analysis prototype, for companies that must react fast to blog discussion. Then drop "the actor is our example" from `fit_reason` and keep the training-side gap as its only gap (USE-1, USE-8).
- Score the day's top 10 with Hits@10 per day (a new custom metric over `basetime_day`). Failing that, use `rmsle` from context. Do not use pooled RMSE (MET-1, MET-7, MET-11).
- Cite the open-access chapter in the bibtex note, the metric reason and `curation_comments`. Correct the word-selection description. Close the "revisit if the chapter documents" item for the parents and the aggregation period.

**Sources**

- Buza, K. "Feedback Prediction for Blogs", GfKl 2012 / Springer 2014, pp. 145-152, doi:10.1007/978-3-319-01595-8_16. Author copy: http://www.cs.bme.hu/~buza/pdfs/gfkl2012_blogs.pdf, found through https://api.semanticscholar.org/graph/v1/paper/DOI:10.1007/978-3-319-01595-8_16 (openAccessPdf). Read for: the abstract, Secs. 1, 4.1, 4.2 with fn. 1, 5.1, 5.2, Table 1, Fig. 2 and the conclusion.
- UCI 304, BlogFeedback: https://archive.ics.uci.edu/dataset/304/blogfeedback (attribute list, base time, the split advice).
- Singh, Kaur, Kumar 2015, "Comment Volume Prediction using Neural Networks and Decision Trees", UKSim 2015, Sec. II and Sec. III-E: https://www.stat.cmu.edu/~brian/valerie/617-2022/617-2021/project01/UCI%20ML%20data%20sets/facebook%20comment%20volume/published.pdf
- Current practice of engagement forecasting in media monitoring: NewsWhip, "Real-time Prediction", https://www.newswhip.com/prediction (forecasts each item's engagement up to 24 hours ahead from how fast interactions accumulate; users sort feeds by predicted interactions and set alerts); BrandMentions spike alerts, https://help.brandmentions.com/en/articles/12752526-what-are-spike-alerts-and-how-do-they-work. Vendor pages; they show the workflow, not its accuracy.
- Precedent: `datasets/_dev/tabarena-v0pt2/onlinenewspopularity/dataset.py` (`rmsle` from context for a heavy-tailed engagement count).
- My scripts and outputs (the metric comparison, the paired per-day comparison, the word flags with and without, the chapter's text) are in the run folder.

</details>

<details><summary>Blind review</summary>

**Verdict: include with changes.** The task is real, has clear signal and is honest in time. But scoring raw comment counts on three small Feb–Mar 2012 windows is decided by a few viral posts, and the source-level features of the training rows were recomputed without saying so.

**The task.** This is UCI BlogFeedback (Buza). At a daily basetime, take every blog post published in the last 72 h and predict how many comments it gets in the next 24 h. A blog portal or aggregator would make this prediction once a day, to pick posts for the front page, rank recommendations, or plan moderation. The use is real, but niche and dated (crawled 2010–2012). I recall that the original paper scored a top-10 ranking per basetime (Hits@10 / AUC@10), not RMSE. I could not confirm this because the paper is paywalled.

**What I checked against the UCI archive.** I downloaded the zip, which has 1 train file and 60 test files.
- **Training rows.** `blogData_train.csv` has 52,397 rows. Minus 3,194 exact duplicates, that leaves 49,203 rows, all with `basetime_day = 0`.
- **Test rows.** The 60 daily test files have 7,624 rows. Minus 588 duplicates within a file, that leaves 7,036 rows on days 1–60. Day 1 is 2012-02-01, a Wednesday, and `basetime_weekday` agrees.
- **Test fidelity.** The test-day rows match the UCI files exactly (0 of 7,036 differ).
- **Dropped columns, all justified:**
  - 4 columns that are constant in the source (attributes 13, 33, 38, 278, the last being parent min comments);
  - 2 exact copies of other columns (attribute 18 equals 3, and 43 equals 28);
  - 22 word indicators that occur in only 4 training rows and in no test row.
- **Other recoding, also sensible.** The weekday one-hots became two categoricals. Parent max/mean comments are NaN when `parent_posts = 0` (53,243 rows).
- **Leakage.** Every post-level feature counts activity before the basetime. Test rows' source statistics come from the 2010–2011 data, which is strictly before Feb 2012. I found no column that would be unknown at prediction time.

**Signal.** I built three expanding windows of 20 days each, training on everything before the window. LightGBM fit on log1p(y) reaches log-R² 0.60–0.71 and raw R² 0.34–0.54. The zero, mean and persistence baselines (y = comments_last_24h) all score raw R² ≤ 0. The top features by gain are hours_since_publication, comments_last_24h and the source's last-24 h mean and median. The task is neither trivial nor saturated.

**Concerns, most serious first**

1. **Scores will be noise-driven on raw counts.**
   - The target has 65.5% zeros, median 0, 99th percentile 154 and maximum 1,424.
   - Only 7,036 rows (12.5%) can be test rows, because day 0 cannot be split. Most posts appear on 3 consecutive days: of non-empty test posts, 1,658 are seen on 3 days, 85 on 2 and 72 on 1. So the test pool holds only about 2,350 distinct posts, and 3 windows give roughly 2,200–2,600 rows, or about 750 posts, each.
   - In window days 41–60, the top 1% of rows (26 rows) carry 82% of LightGBM's squared error.
   - A cluster bootstrap (resampling posts) gives a 90% interval of [0.33, 0.64] for raw R², against [0.56, 0.64] for log-R².
   - The ranking of methods flips between windows. Raw R² for the L2 / log / Poisson objectives is 0.43 / 0.34 / 0.49 in days 1–20 and 0.43 / 0.41 / 0.34 in days 21–40.
   - Change: score on log1p(target) or with Poisson deviance, use the widest windows possible, and treat repeated posts as clusters when computing intervals.

2. **The source features (attributes 1–50) were changed for training rows only, and task.md does not say so.**
   - In the UCI training file, these features are statistics over all training rows of the same blog. I checked that the source mean equals the mean of comments_total over every row sharing that vector in 100% of rows. So each row's statistics include the row itself and later snapshots of the same post. UCI test rows reuse these 2010–2011 values: 100% of test vectors appear in the training file. That makes them legitimate history at test time.
   - The prepared table keeps the test values. For training rows it replaces the values in 96.1% of rows (only 1,915 of 49,203 are unchanged) with what looks like 5-fold out-of-fold statistics:
     - the prepared max equals the out-of-fold max in 99.1% of fold groups, and the in-fold max in 6%;
     - each source gets up to 5 distinct vectors;
     - 250 rows are NaN, apparently sources whose rows all fall in a single fold.
   - This is a defensible anti-leak step, with three problems:
     - (a) It is undocumented.
     - (b) It is incomplete. With random folds, other snapshots of the same post usually stay in the other folds, and the next snapshot's comments_last_24h equals this row's target.
     - (c) It encodes "no source history" two ways: NaN in 250 training rows, but all-zero in 713 test rows. In 177 of those test rows comments_total > 0, so the zeros mean "unseen blog", not "blog with no comments".
   - The effect on scores is negligible. Test log-R² is 0.661 / 0.699 / 0.593 with the prepared values and 0.668 / 0.693 / 0.592 with the original UCI values.
   - Change: document the step (or revert to the UCI values), and encode unseen sources the same way in train and test, for example NaN plus a flag.

3. **`basetime_day` is a split key, not a time axis.**
   - Day 0 lumps two years (2010–2011, 49,203 rows, 87.5% of the table) into one value, while days 1–60 are calendar days.
   - If the harness passes it as a feature, it is constant for most training rows and extrapolated in test.
   - Change: exclude it from the features, record the mapping (0 = UCI train file, k = 2012-02-01 + k − 1), and make sure all test windows lie in days 1–60.

4. **Repeated posts (correlation, not leakage).**
   - A training row's target at day k equals the next day's comments_last_24h for the same post. That value is legitimately known at the later basetime, and the forward split keeps this one-directional.
   - No test row is feature-identical to a day-0 row. There were 80 such rows in UCI, mostly empty posts; the recomputed source statistics removed them.
   - The main cost is that the effective test size is about one third of the row count; see concern 1.

5. **Minor quality and age points.**
   - 22.2% of rows have post_length = 0 (no extracted text).
   - In the source, parent min comments is always 0, and parent max is 0 in 2,366 of the 2,996 rows that have parents, which is a source quirk.
   - The data is from 2010–2012 and the blogs are probably Hungarian. I recall the Hungarian origin but did not verify it.
   - No action needed beyond documentation.

**What I could not check**
- The Springer paper (doi 10.1007/978-3-319-01595-8_16) is paywalled, so the crawl details, language and original metrics are from memory.
- task.md says only "3 test windows", so I do not know the harness's window boundaries, or whether `basetime_day` is dropped from the features.
- I inferred the exact recomputation of the source features; I did not see the code that did it.
- The UCI release has no post or blog IDs, and the real basetimes inside 2010–2011 are not given. My clustering of repeated posts uses approximate fingerprints (word vector, length, source statistics).

</details>

<details><summary>Precedent check</summary>

**Precedent check (precedent-checker, 2026-11-01).** Verdict: mostly consistent. Four calls depart without a fact that
sets them apart. Two of these depart from precedents the curator decided: the four parent columns are kept (LEAK-10),
and the metric is the fallback on the raw count (MET-11; onlinenewspopularity). The other two have no curator
precedent and depart from the rule text: the target ships on the raw scale (CLEAN-16, MET-3), and the 3 windows rest
on SPLIT-19 (SPLIT-15). One scope question is not addressed: TP-10 leg 2, for a second lag of the target. I found no
drift and no third exception of one reason. Sources: the run's decision register, the
Cases tables of the knowledge files, sibling records, the definitions of the working copy.

**Per decision, in rank order**

| # | Decision (definition or builder draft) | Status | Closest precedents |
|---|---|---|---|
| 1 | Keep the task, verdict `Yes` once the leak is fixed | consistent | the curator's own CC (2026-10-30, Andrej: "Move to yes if you can resolve the leak, otherwise no"); `loan_default_prediction_imperial_college`, `nfip_redacted_flood_claims` (leaks sent on to be fixed, same page); principles.md tension "a real task against a leak" (kickstarter) |
| 2 | Fit `approximate`; `fit_reason` names the blog-statistics remainder as a gap and leaves out the kept parent columns | departs in wording (USE-8, Must) | `onlinenewspopularity`, `african_credit_scoring_challenge` (CC 2026-10-21, Lennart: a kept leak is named in `fit_reason` as kept, not as a gap) |
| 3 | TP-10: leg 1 tested; leg 2 not addressed | leg 1 consistent; leg 2 open (prompt S) | `rain_in_australia` (2026-10-26, leg 2 amended: only the last observation), `g_research_crypto_forecasting` (2026-10-22: trailing returns allowed), `ashrae_great_energy_predictor_iii` (method) |
| 4 | Training-row blog statistics recomputed out of fold, test rows keep the published ones | consistent | the CC above (the fix of the 2026-10-30 Assessment); LEAK-29/CLEAN-7 (`sf_permit_time`, 2026-10-19: statistics from history before the oldest test window; here the training crawl precedes every window); tension row `alfa_battle_2_0_task_2`/`lending_club` (2026-10-21: remove the shortcut you can measure, record the diffuse rest) |
| 5 | Parent comment statistics kept with a `Potential leak, kept on purpose` note | departs, no reason the rule accepts (prompt P) | `onlinenewspopularity` self-reference shares (kept 2026-10-26: the traced part shows no gain); `distribution_transformers_at_cauca_department` (dropped, 2026-10-21); `african_credit_scoring_challenge` `other_lenders_on_loan` (a count from a pull that cannot be dated, dropped; shipped 2026-10-26) |
| 6 | Official temporal split kept; expanding training side (SPLIT-11); no gap | consistent | SPLIT-19/SPLIT-5 checked on the data; gap: the `_1m` taxi and ETA cases (2026-10-21: a gap only where training labels arrive after the window start; the labels of day 40 are known at day 41's base time) |
| 7 | 3 windows of 20 test days, not 9 | departs, stated reason weak (prompt W) | 9 windows: `onlinenewspopularity` (shipped 2026-10-26), `zillow_prize`, `walmart_sales_in_stormy_weather` (draft); fewer, for the horizon or the floor: `rossmann_store_sales` (SPLIT-12), `noaa_afsc_bottom_trawl_survey_cpue` (draft), `avito_demand_prediction_1m`; `rain_in_australia` (2026-10-26, Lennart: 26 windows) |
| 8 | Known blog (99.9% of test rows) | consistent | USE-10, SPLIT-13, LEAK-34 (`ieee_fraud_detection` uid; ghana) |
| 9 | Exact copies dropped (3,194 training, 588 within a test day); 17 cross-day copies, 13 pairs made by the recomputation and the 410 conflicting rows kept | consistent | LEAK-19: `wine_quality`, `qsar_oral_toxicity` (copies of one entity go); `hiva_agnostic`, `qsar_tid_11` (2026-10-21, Lennart: distinct entities the features cannot tell apart stay) |
| 10 | Metric `Metric.fallback` (rmse on the raw count) | rejecting the source's measures: consistent; not using context: departs (prompt M) | MET-5 (`gallstone_disease`), MET-1 (`churn_telco_south_asia`, 2026-10-21: closed source not read, fallback); `onlinenewspopularity` (`rmsle` from context, Lennart 2026-10-21 and 2026-10-26) |
| 11 | `no_spread` flag kept (TP-2) | consistent | `acquire_valued_shoppers_challenge` (2026-10-06), `hr_analytics` (2026-10-14): kept |
| 12 | Target shipped as the raw count | departs, no reason (prompt T) | MET-3 and CLEAN-16 (Lennart, 2026-10-21, on `onlinenewspopularity`: "ship the target on the modelling scale, score on the original scale"); in this batch: `nantucket_sound_sea_duck_aerial_survey_counts`, `wadden_sea_sibes_macoma_abundance`, `pennsylvania_oak_hickory_regeneration_experiment` (log1p) |
| 13 | Observed zeros kept, no cap | consistent | Andrej, 2026-10-30 (policy question 2: "We don't care ...") |
| 14 | Parent statistics: stored 0 without a parent set to missing (CLEAN-10) | departs, with a reason the data shows but nobody wrote down | `house_sales` (`yr_renovated` 0 to missing, exception, 2026-10-22, Lennart) against `bank_marketing` (`pdays = -1` kept as a code) |
| 15 | Weekday blocks merged (CLEAN-12/13); 4 constant and 24 copied columns dropped (CLEAN-5); length-0 posts kept (CLEAN-11) | consistent | `mortgage`, `onlinenewspopularity` (2026-10-22: lossless merge when every row has one flag; checked here: row sums all 1) |
| 16 | Word flags typed categorical (CLEAN-14) | consistent | `qsar_oral_toxicity`, `hiva_agnostic`, `qsar_tid_11` (2026-10-21: fingerprint bits categorical) |
| 17 | `Data Quality Issue` marker kept on a `Yes` record | consistent with practice | `ieee_fraud_detection`, `loan_default_prediction_imperial_college`, `5g_energy_consumption` keep it on `Yes`; selection.md defines it as damage that cannot be repaired, which no longer fits once the leak and the copies are fixed |

**Notes on the consistent calls**

* Item 4: the 2026-10-30 Assessment shows up twice in the register, once under "scaling over all rows" (LEAK-30, line
  1792). That mechanism is wrong for this case. The mechanism is LEAK-10's "an aggregate that may include the row's own
  outcome" (online_shoppers `PageValues`). So LEAK-30's keep-with-a-note precedents (bioresponse and the others) do not
  apply, and neither does drift flag 4. The post key in `post_folds` is a composite key (blog, text, publication
  weekday), as in concrete_compressive_strength. It is not maternal_health_risk's barred hash: it is used for feature
  folds, not for the evaluation split. It cannot split one post across folds. It can only merge text-less posts, which
  makes the folds more conservative.
* Item 2: if the blog-statistics remainder is read as a gap of the undated crawl (USE-8's "a reconstructed time axis"
  kind), the fit text is defensible. The builder's issue 2 calls it a weak LEAK-10 remainder, though. Read that way,
  USE-8 wants it named as kept, and on its own it would not make the fit approximate. Pick one reading. Whichever way
  issue P is settled, a kept parent leak belongs in `fit_reason`.
* Item 9: the drop follows LEAK-19 because of a fact in the data: the training copies sit a median of 2 rows apart in
  the file, and 92% of them have non-zero comment counts, identical at the same age. That makes them one post recorded
  twice (builder probe e2). `jm1` (2026-10-01, Lennart) dropped every copy of a conflicting vector. Its copies
  straddled a random split, and it predates the 2026-10-21 decisions, which are newer and win.
* Item 14: what sets it apart from `bank_marketing` is visible in the data. A stored 0 in `parent_comments_max` or
  `parent_comments_mean` is also a possible real count (parents without comments), and `parent_posts` already says
  "no parent". These are the two facts `house_sales` rested on. Record it as an exception to CLEAN-10 like
  `house_sales`. It would be the second exception of this reason.
* Item 16: the 200 frequent words hold only 0 and 1 over 60,021 posts, so the columns are presence flags, not counts.
  Their meaning (the word is present) is known even though the words are not named. That is why they differ from the
  opaque descriptors reverted to numeric on 2026-10-21 (amex, ieee V columns, bioresponse, homesite).
* A note for the split and column auditors: `basetime_day` = 0 puts the whole undated 2010-2011 crawl on the day before
  the test period. This is the `house_sales` fact (a 0 in a time column reads as a time). The column carries the
  split, so it cannot become missing. Builder issue 1 covers it.
* Sibling: `facebook_comment_volume` has no definition. Its 2026-10-30 Assessment (AI, not decided) recommends
  dropping the in-sample page aggregates, which cannot be rebuilt from training history, and the crawl-time "talking
  about" count (costs about 0.003 ROC AUC). Its aggregates hold the test period, so blogfeedback's recomputation does
  not conflict with that drop. The crawl-time count is the same mechanism as issue P, which the AI decided the other
  way in the same batch.

**Drift and amendments**

* Drift: none. Andrej moved this record from 2nd Tier to conditional `TBD -> Yes` and then to `Yes` (2026-10-30). That
  is an answer to a consistency check, not drift. Lennart's `facebook_comment_volume` (`TBD -> Yes`, "time-split and
  leak needed") points the same way.
* Third exception: none due. CLEAN-10 (`house_sales`'s reason) would reach its second exception with item 14. SPLIT-15
  has no recorded exception, so this would be the first. The register's flags 8-14 concern other datasets.
* Register note: the register lists CLEAN-14 and CLEAN-11 as "not defined". Both are defined in cleaning_features.md;
  the long amendment text in their headings probably defeats the parser.

**Consistency checks for the curator**

**Consistency check (AI, 2026-11-01), P:** the draft keeps the four parent comment columns with a note (LEAK-10, second
clause). That differs from `distribution_transformers_at_cauca_department` (`power_kva`, `installation_type` dropped,
2026-10-21) and `african_credit_scoring_challenge` (`other_lenders_on_loan`, a count from a pull that cannot be dated,
dropped). It also does not meet the condition `onlinenewspopularity` met when its self-reference shares were kept
(2026-10-26: the traced part of the late cells shows no gain). The only reason given is that removing the columns
changes no score (ROC AUC 0.898 against 0.899). LEAK-10 says that is no reason to keep on its own. What sets
blogfeedback apart?
(a) No later pull is shown. UCI says every feature is computed from what was known at the base time, and the values
change between a post's base times in 22% of 792 posts. A single crawl-time snapshot would not change, so the second
clause is not triggered and the note only records a suspicion. Record this as the fact.
(b) Treat it like distribution_transformers: drop the four columns. The measured cost is zero.
(c) Reopen the two drops: does not fit, since both rested on a measured gain or a change of sign.
(d) Amend LEAK-10: late values that cannot be located stay with a note when removing them all changes no score.
Under (a) or (d), name the kept leak in `fit_reason` (USE-8).

**Consistency check (AI, 2026-11-01), W:** the draft cuts 3 windows of 20 test days, not the 9 that SPLIT-15 gives a
task of this size. Its reason is SPLIT-19, a Should placed below SPLIT-15 in splits.md. SPLIT-19 does not decide
between 3 and 9: both stay inside the source's 60 test days, and both refit on earlier test days, which the source
does not do. The precedents with fewer windows rest on the horizon (SPLIT-12: rossmann_store_sales, 3 x 42 days) or
on the 50% floor (SPLIT-14: avito_demand_prediction_1m, lending_club). The precedents cut at the source's test unit
ship 9 (onlinenewspopularity, zillow_prize, walmart_sales_in_stormy_weather), and rain_in_australia went to 26
(2026-10-26, Lennart). What sets blogfeedback apart?
(a) The horizon (SPLIT-12): the source predicts all 60 test days from one training run, and 20 days is the longest
horizon that still gives three windows. Record this as an exception to SPLIT-15 that cites SPLIT-12, not SPLIT-19.
(b) Follow SPLIT-15: nine windows of 6-7 days.
(c) Reopen nothing: no precedent shipped fewer windows on this reason.
(d) Amend SPLIT-15: a source's single test period is cut into the minimum three windows.

**Consistency check (AI, 2026-11-01), M:** the draft declares the fallback rmse on the raw count. That differs from
`onlinenewspopularity`, a target of the same kind: a heavy-tailed engagement count of web publications with no
source metric for the regression. There the curator kept `rmsle` from context on a log target (Lennart, 2026-10-21;
"oke keep regression", 2026-10-26). Here the top 1% of test rows hold 84-86% of the dummy's squared error. What sets
blogfeedback apart?
(a) The decision features the posts that will draw the most discussion, and the source's own measures (Hits@10,
AUC@10) look only at each day's top 10. So the error on the largest counts is what the decision reads: RMSE weights
those counts, while RMSLE would weigh a miss of 0 against 2 like one of 100 against 300. Write this in the metric's
reason.
(b) Treat it like onlinenewspopularity: `Metric.from_context("rmsle", target_transform="log1p")`.
(c) Reopen onlinenewspopularity to the fallback.
(d) Amend MET-11 with a rule for count targets.
Option (b) would also settle T.

**Consistency check (AI, 2026-11-01), T:** the target ships as the raw count, and the definition gives no reason. CLEAN-16
(Should) logs a skewed count case by case, and MET-3 quotes Lennart's "ship the target on the modelling scale, score
on the original scale" (2026-10-21). In this batch, `nantucket_sound_sea_duck_aerial_survey_counts` also declares the
fallback rmse scored on the count but ships log1p. The drafts that ship a raw target give a reason
(`rand_health_insurance_experiment_doctor_visits`: R2 in dollars, and a capitation pays the mean). What sets
blogfeedback apart?
(a) Rmse on the count is minimised by the conditional mean, which a model fit on log1p underestimates after the
inverse. This holds for nantucket as well, so it is a reason for the family, not for this dataset alone.
(b) Ship `log1p_comments_next_24h` with `target_transform="log1p"`, as nantucket does; the metric is unchanged.
(c) Reopen nantucket to ship the raw count.
(d) Amend CLEAN-16: raw scale when the declared metric is rmse on the raw scale.

**Consistency check (AI, 2026-11-01), S:** TP-10's leg 2, as amended on rain_in_australia (2026-10-26), allows one lag
of the target column: its last observation. `comments_last_24h` is that lag (it equals the previous day's target in
99.7% of pairs). `comments_24h_to_48h_before` is the lag before it, by UCI's attribute list, and `comments_change_24h`
is the difference of the two. Leg 1 holds in all 3 windows (RMSE 22.5 / 23.9 / 25.2 against the best per-post naive
28.3 / 26.8 / 25.9; the oldest window wins by 3%), as rain_in_australia did in 9 of 9. What sets blogfeedback apart?
(a) A post lives at most 72 hours, three rows, and the source defines these columns as window counts since
publication. They are trailing summaries like g_research's trailing returns, and no series is forecast. Record this
under TP-10.
(b) Drop the second lag and the difference, then re-run leg 1.
(c) Does not apply.
(d) Amend leg 2 to cover window counts over a short life.

</details>

<details><summary>Advocate</summary>

**Advocate's opening brief: blogfeedback (advocate, 2026-11-01)**

**Position: ship after changes.** On the shipped definition, every validity rule (P1-P5) holds or needs only a metadata or wording fix. The one material problem is the metric (P6). It is fixed in the definition, not by exclusion (remedy ladder, principles.md step 5). The phase A agents refuted many sentences. Almost none of those refutations changes a row, a split or a test score.

```text
Verdict: ship after changes.
Validity: USE-1 holds, more firmly than written (the chapter names the actor); USE-8 approximate holds; LEAK-10 triggered,
  fixed (training statistics out of fold, test side checked by three agents); LEAK-10 second clause not triggered for the
  parents; SPLIT-1/3/9/14 hold; PROV-8/9 triggered, fixed in metadata.
Value: TP-2/TP-4 hold; TP-10 leg 1 holds in 3 of 3 windows; MET-1 triggered (rmse misranks the daily top-10 decision): change the metric.
Quality: SPLIT-15 departure kept as an exception; CLEAN-10 (post_length 0) and CLEAN-16 (target scale) are cheap fixes;
  LEAK-31 word flags kept with a note.
Weighed: source + (primary chapter, 2012 release byte-identical), size +, signal +, age -.
```

**1. The task is real, and the source states its use case (P3; USE-1 Must, USE-8 Must, USE-12 Must).**
- Evidence. The chapter's abstract reads: "a proof-of-concept industrial application, developed in cooperation with Capgemini Magyarország Kft.". Sec. 1 says a company "might have to react quickly" to blog discussion. Sec. 5.1 evaluates once per test day at a daily base time. The domain practitioner, playing that actor, says: "Would I use it? Yes, as a ranking aid." Untuned log1p LightGBM finds 6.67 of each day's true top 10. The desk's sort by comments in the last 24 h finds 5.63, so the model gains 1.03 posts a day (paired SE 0.14, 60 days). On posts younger than 24 h it finds 4.85 against 3.67.
- What it answers. The claim auditor refuted "the source names no actor" (items 6 and 8). That finding removes a gap from `fit_reason`; it adds none. Remedy: take `use_case` and `fit_reason` from the chapter. The fit stays approximate because of the undated crawl (USE-8). The practitioner adds that USE-9 does not lift it to direct. P1/P2: the data is public counts of blog activity, with no ids and anonymised word flags, under CC BY 4.0. No agent raised ethics or scope.

**2. The curator's condition is met: the leak is fixed and the test side is clean (P4; LEAK-10 Must, LEAK-29 Must).**
- The condition. CC 2026-10-30 (Andrej): "Move to yes if you can resolve the leak, otherwise no."
- Evidence: the decision table.
  - The published training statistics equal the blog's statistics over all its training rows (share 1.0).
  - The test rows' statistics equal the statistics over training rows only (1.0) and never those over test rows (0).
  - So every test feature is history from before every test day, which is what LEAK-29 requires. The split auditor confirms that both sides are computed from the crawl only.
  - Test AUC is 0.908 with the published statistics and 0.908 with the recomputed ones (claim auditor item 20, builder).
  - The fold key keeps a post's rows together in 99.7% of 20,320 count-matched pairs (column auditor). So a row's own later counts are no longer in its statistics.
- What it answers.
  - The blind reviewer called the step "undocumented, incomplete (random folds)". It saw task.md only. The definition documents the step (notes bullet 2, decision 1), and the folds are whole posts, not random rows (EV-2: the measurement wins).
  - The claim auditor found that the 5-fold statistics still shift with the row's own outcome (item 15; Spearman -0.23 in blogs with 2-5 posts). The shift is on the training side only. The inner-CV gain is +0.058 to +0.061, against +0.048 on the test windows, and test scores do not change. No test label reaches a test feature, so P4's honest evaluation holds. What remains is a feature shift between training and test rows.
- Remedy: one sentence in the "Not removed" bullet. This follows the alfa_battle / lending_club tension row: remove the shortcut you can measure (done) and record the diffuse rest.

**3. The split is the source's own and mirrors the decision; every Must holds (P4; SPLIT-1, SPLIT-3, SPLIT-9, SPLIT-14 Must; SPLIT-19 Should).**
- Evidence (split auditor: "right with notes").
  - A temporal split over known blogs is the only regime with signal. Grouped by blog, with the statistics dropped, R² on counts is -0.672; the shipped temporal windows give 0.430.
  - Train sides hold 87.5-95.4% of the rows.
  - No gap is needed: the next day's last-24h count equals the row's target in 99.7% of pairs.
  - Each window has 2,225-2,564 test rows.
  - The split is UCI's "temporally disjoint" one, which chapter Sec. 5.1 confirms.
- What it answers: 3 windows instead of 9 (SPLIT-15 Should; split auditor problem 1, precedent prompt W). I concede that the stated reason, SPLIT-19, is weak. Keep 3 × 20 days with an `Exception to SPLIT-15` that rests on the facts the split auditor measured:
  - The test pool is fixed at 7,036 rows, because the crawl is a single time value. Finer windows add no test rows (SPLIT-17's reason).
  - The tail is heavy. The top 5 rows hold 41-50% of a 20-day window's squared error, against 62-83% in 6-day windows.
  - The source applies one 2010-11 model to all 60 days (SPLIT-12).
  - That gives a fact and a higher principle (P6: every fold can be scored), the form a Should departure needs.
- What it answers: "every test blog is in the training file" (claim auditor item 17, refuted for up to 9.4%).
  - The evidence is circumstantial (EV-6), and these rows cannot be told apart one by one.
  - Predictions on them are calibrated: P(comment) predicted 0.124 / 0.047 / 0.036 against observed 0.116 / 0.059 / 0.035.
  - Remedy: rewrite the sentence. The regime stays. At least 90.6% of test rows are on known blogs, and a monitoring service adds new blogs too.
- `basetime_day` as a feature is harmless: it is constant on the oldest window's train side (split auditor problem 5), and the notes already name it.

**4. The task is worth benchmarking, and it is a tabular task (P6, P2; TP-2 Should, TP-4 Must, TP-10 Must).**
- Evidence.
  - Untuned LightGBM reaches R² 0.431 on counts (RMSE 23.8 against the dummy's 31.6, better in 3 of 3 windows) and R² 0.60-0.70 on log1p.
  - The best single feature reaches R² 0.29 against 0.416 for all features, so the task is not trivial.
  - TP-10 leg 1: LightGBM scores 22.5 / 23.9 / 25.2 against 28.3 / 26.8 / 25.9 for each post's best naive forecast.
  - The frame has 56,239 rows.
  - It is faithful to the source: on window 1-20, the chapter's own design, Hits@10 is 6.0-6.6, against 5-6.2 for the chapter's models and 2-3 for its naive model (claim auditor item 53).
- What it answers: TP-10 leg 2 (precedent prompt S).
  - `comments_24h_to_48h_before` and `comments_change_24h` are the source's window counts over a life of at most 72 h (three rows). They are the "summaries of the series up to the prediction point" that the amended rule allows.
  - Under the rain_in_australia amendment, leg 1 "carries the test", and it holds in 3 of 3 windows.
  - 7.0 of each day's true top 10 are posts under 24 h old (practitioner), which have no lag at all. No series is being forecast. Record it as option (a).
- The `no_spread` flag is kept under TP-2, like acquire_valued_shoppers and hr_analytics.

**5. The data is faithful, unique and traced to its first publication (P5; PROV-8, PROV-9 Must; PROV-4; LEAK-19 Should).**
- Evidence.
  - The claim auditor found the 2012 first release (`blogdata.zip`, 2012-07-24). All 61 of its CSVs are byte-identical to UCI's.
  - The shipped test rows match the UCI files exactly (blind reviewer: 0 of 7,036 differ).
  - The counts are consistent in all 60,021 rows (column auditor).
  - `facebook_comment_volume` is other data (PROV-4).
  - The 3,194 training copies sit a median of 2 rows apart, and 92% have non-zero, identical counts. They are one post recorded twice and are dropped under LEAK-19 (wine_quality, qsar_oral_toxicity). Text-less vectors with two targets stay (hiva_agnostic, qsar_tid_11).
- What I concede: the year and source are wrong (claim auditor item 43). The fix is metadata only: year 2012, source Buza's release, UCI named as the download copy, and the chapter added to the BibTeX. It strengthens provenance and changes no data.

**6. The metric is a real problem, fixed in the definition (P6; MET-1 Must over MET-5 Should).**
- What I concede: rmse on raw counts does not score the decision.
  - In the practitioner's table, rmse ranks raw-count L2 first (23.95), although it is the worst LightGBM on Hits@10 (6.16). It also rates the velocity sort worse than a constant.
  - Kendall tau between rmse and Hits@10 is 0.30 in two of three windows (claim auditor item 40).
  - The top 1% of rows carry 68-92% of the squared error.
  - The blind reviewer's post bootstrap gives raw R² a 90% interval of [0.33, 0.64], against [0.56, 0.64] on log1p.
  - MET-1 is a Must, so it beats the fallback's reading of MET-5 at the same rank.
  - The metric reason's "closed access, not read" is refuted (claim auditor item 36).
- Why this does not hold back shipping: a metric problem is fixed in the definition, the second step of the remedy ladder. Exclusion is only for a Must that cannot be fixed.
- Mildest fix that resolves it: `Metric.from_context("rmsle", target_transform="log1p")`, with the target shipped as log1p.
  - It is in the library and needs no scoring column and no feature change.
  - Precedent: `onlinenewspopularity` (Lennart, 2026-10-21 and 2026-10-26), also a heavy-tailed engagement count.
  - It orders the LightGBM variants as the daily measures do (tau 0.60-0.75).
  - It settles CLEAN-16 and MET-3 (prompt T) in the same change.
  - The reason must cite the chapter's Hits@10 and AUC@10 and say why they were not adopted (MET-11).
- The faithful alternative: Hits@10 per day (MET-7: the source fixes k = 10 per day). It costs a new per-group top-k metric (MET-12, MET-13), and `basetime_day` moves from feature to scoring column (MET-2).
- This is a weighing call for the curator, and both options keep the dataset.

**7. The rest are independent quality and wording fixes, each cheap; none touches validity (P7; the tension row "a real task against imperfect cleaning").**
- Parents (precedent prompt P, LEAK-10 second clause). The column auditor's data settles it:
  - With an unchanged parent set, max and mean only rise between base times (96 and 97 rises in 1,587 pairs, no fall). Every fall comes with a shrinking set (702 of 731 set changes are decreases).
  - These are counts taken at each base time, not values read at a later pull, so the clause is not triggered.
  - Keep the columns and replace the "Potential leak" label with a plain note (option a).
  - This fact, not a test where dropping changes no score, is what sets the case apart from distribution_transformers and african_credit_scoring.
- Word flags (LEAK-31 Should; claim auditor problem 2).
  - Buza chose them with the label on documents he does not name. They carry nothing on the test windows: R² on log1p is 0.6559 without them and 0.6549 with them; AUC 0.9073 and 0.9083. Buza's Table 1 shows that the text features lower Hits@10.
  - LEAK-31 says "keep with a note when small", and a selection the source published is decided case by case (Lennart, 2026-10-21).
  - Keep them with a `Potential leak, kept on purpose:` note citing footnote 1. Dropping them, as for qsar_bioconcentration, is the curator's alternative.
- `post_length` 0 becomes missing (CLEAN-10 Should; column auditor problem 4). I accept this. It is an extraction gap per blog: the 100 blogs without text hold 90% of the zero rows. The fix is one line in `_clean`, placed after the fold key is computed.
- Wording fixes:
  - quote UCI's actual sentence;
  - "554 blogs" becomes "at least 554" (the chapter: "roughly 1200 sources");
  - "scores the same with no statistics" is false: without them the score is lower on AUC and log1p and better on rmse, so say that;
  - 251 becomes 250;
  - "frequent words" and "closed access, not read" go;
  - the parents' "Revisit" line closes, since the chapter is silent on the counting time;
  - the record's Assessment figures are updated;
  - the `Data Quality Issue` marker no longer fits (precedent checker item 17).
- Independent failures are not conflicts. The task being real rescues none of these: each is fixed on its own terms. None drops a row the use case needs, and none changes the split.

</details>

<details><summary>Critic</summary>

**Critic, opening brief: blogfeedback (2026-11-01)**

**Verdict: ship only after changes.** The task is real (it is the source's own daily ranking of blog posts), and the fix of the training-side leak holds, so nothing here calls for exclusion. But the definition was written without Buza's chapter, and the chapter is open: the author's copy is at <http://www.cs.bme.hu/~buza/pdfs/gfkl2012_blogs.pdf>. It changes the actor, the provenance, the description of the word columns and, above all, the metric. Point 6 has the largest effect: rmse on the raw count ranks models against the source's own decision. The points below are ordered by rank (P3 to P6), then by strength.

**1. The use case and the fit misstate the source (P3; USE-1 Must, USE-8 Must).**
- Problem: `use_case` says "The source names no actor", and `fit_reason` lists "the actor is our example" as a gap.
- Evidence: the chapter's abstract says "a proof-of-concept industrial application, developed in cooperation with Capgemini Magyarország Kft.". Sec. 1 says that a company "might have to react quickly" to negative news, and that "analysis of all these documents by human experts is hopeless". Sec. 5.1 scores, for each day, the 10 posts predicted to draw the most feedback (claim audit 6 and 8; domain practitioner).
- Effect: the use case sets the unit the metric has to score (point 6), and that unit is the top of each day's list, not pooled rows. The invented portal actor let the definition avoid that question.
- Remedy (text only): take the actor, the moment and the decision from the chapter: a social-media monitoring service decides each morning which of the posts from the last 72 hours its analysts follow. Drop the first gap from `fit_reason` and keep `approximate` because of the undated crawl. Any leak that stays (point 2) is named in `fit_reason` as kept (USE-8; african_credit_scoring_challenge, 2026-10-21).

**2. Four statements in the leak notes are contradicted by the data (P4; LEAK-10 Must, USE-10 Must).** No data change is needed, but the curator decides from these notes.
- Parents: the four columns are kept as "Potential leak, kept on purpose" because dropping them "scores the same". LEAK-10's second clause says that test alone is no reason to keep, and the precedents went the other way (distribution_transformers_at_cauca_department, african_credit_scoring_challenge; precedent check P). The column audit also shows that the note's mechanism is wrong:
  - when the parent set does not change, max and mean only rise between base times (96 and 97 rises in 1,587 pairs, no fall);
  - every fall comes with a shrinking set (702 of 731 changes in the set are decreases);
  - so the values are counts taken at the base time, not a later pull.

  Remedy:
  - rewrite the bullet with this evidence (option a of check P), and either drop the label or keep it with the corrected evidence and name the leak in `fit_reason`;
  - replace "Revisit if Buza's chapter documents them": the chapter (Sec. 4.2) has been read and does not say when the counts were taken;
  - fix the `CONSTANT` comment: `parent_comments_min` is a broken source column (0 in all 249 one-parent rows where max = mean > 0).
- Known blog: "Every test blog is in the training file" fails for up to 9.4% of test rows.
  - Evidence: 719 test rows carry the all-zero statistics, which match a training row trivially. 24.6% of them had comments before the base time. By construction, 0% of the zero-vector training rows have comments (claim audit 17). The blind reviewer found the same thing independently: 713 rows, 177 of them with comments.
  - Effect: these rows are probably blogs without training history, encoded as 0, while the training side encodes "no history" as missing (250 rows). The effect on the score is small, since the predictions stay calibrated on these rows.
  - Remedy: a note, worded as in the claim audit. The 99.9% hidden-group reading goes.
- Residual shift: the sentence "Not leave-one-post-out, which would shift the statistics with the row's own target" implies that 5 folds do not shift them. In blogs with 2-5 posts they do: Spearman −0.23 with the row's own log1p target. The inner-CV gain is +0.058 to +0.061, against +0.048 on test (claim audit 15). This is on the training side only. Remedy: say so in the note.
- Wording:
  - "scores the same with published, recomputed or no statistics" contradicts its own numbers (AUC 0.908 against 0.892, R² 0.656 against 0.609). It also omits that rmse prefers no statistics (23.69 against 24.02).
  - "554 blogs" counts distinct statistic vectors, and every silent blog is merged into one of them. The chapter says "roughly 1200 sources".

  Remedy: correct both sentences.

**3. The word flags were chosen with the label (P4; LEAK-31 Should), and `post_length` 0 is a missing value (P7; CLEAN-10 Should).**
- Evidence on the words:
  - Chapter footnote 1 ranks each word by the gap in "the number of feedbacks of documents" with and without it, and keeps "the 200 most discriminative words". The 2012 readme says "The 200 most significant bag of words features".
  - The chapter does not say which documents were used, so February-March 2012 cannot be ruled out.
  - The notes and the `WORDS` comment call them "frequent words".
- Measured, the words carry no signal. Without them: R² log1p 0.6559 against 0.6549, AUC 0.9073 against 0.9083, Hits@10 6.63 against 6.56, rmse 23.12 against 24.02 (claim audit 27; the practitioner finds 0.657 against 0.656). In the source's own Table 1, adding the textual features lowers Hits@10 for 5 of 7 models.
- Rule: LEAK-31 says "remove it when we can", and a selection the source published is decided case by case. The closest case is qsar_bioconcentration (2026-10-26): the authors' 9 descriptors added 0.002 and were dropped.
- Remedy: drop the 178 word columns, and the `Anonymized` tag goes with them. If the curator keeps them, add a `Potential leak, kept on purpose:` note that cites footnote 1 and the drop test.
- `post_length` 0 (23.8% of rows) is a gap in text extraction that belongs to the blog, not an empty post: 100 blogs have no text in any row, hold 90% of the zeros, and stay without text in the test files (column audit, problem 4). Remedy: set it to missing after step 3 (cheap and safe). This is a quality point, not a reason against the task.

**4. Three windows instead of nine, with no exception recorded and a reason that does not decide (P4; SPLIT-15 Should).**
- Problem: `splits_comment` cites SPLIT-19. But the source trains once and tests on all 60 days, which is one window, and SPLIT-14 forbids that. So SPLIT-19 favours neither 3 nor 9 windows (split audit, problem 1; precedent check W).
- The record has no `Exception to SPLIT-15` line. The precedents cut at the source's test unit ship 9 windows (onlinenewspopularity, zillow_prize).
- Remedy: the number of windows is the curator's weighing call, but the choice has to be recorded either way:
  - keep 3 windows of 20 days with an exception that names the facts that hold: the test pool is fixed at 7,036 rows, so finer windows add none, and the source applies one model to all 60 days (SPLIT-12);
  - or use `TemporalSplits(window=6, n_windows=9)`.

  The split audit also offers a heavy-tail fact for 3 windows. That fact is about rmse and falls away if point 6 is accepted. Add one clause on SPLIT-20: the crawl is a single time value, so the training history cannot be trimmed.

**5. Source, year and quotations (P5; PROV-8, PROV-9, PROV-16, all Must).**
- Problem: the data was first published in 2012, at <http://www.cs.bme.hu/~buza/blogdata.zip>, the copy chapter Sec. 5.1 points to (files dated 2012-07-24). I checked that all 61 CSVs are byte-identical to the UCI files, so UCI's 2014 upload is a re-upload.
- Remedy: set `year = "2012"`, set `source` to the author's release (the chapter's link), name UCI in `download_description` as the copy, and cite the chapter and the release in the BibTeX.
- PROV-16:
  - the notes quote UCI as saying "Features are computed only from information available at that basetime", which is not in UCI's text. UCI says: "we calculate all the features of the selected blog posts from the information that was available at the basetime";
  - the metric reason cites the chapter through Singh et al., "not read".

  Remedy: quote only what was read, with section and page. Update the lines in the record's screening and Assessment that say "closed access, not read".

**6. Rmse on the raw count does not score the decision (P6; MET-1 Must, MET-7 Should, MET-11 Must).** This point has the largest effect.
- The source and the use case act on each day's top 10. Sec. 5.1: "For each day of the test data we consider 10 blog pages that were predicted to have to largest number of feedbacks ... We call this evaluation measure Hits@10". The text argues from this measure: "The number of hits was around 5-6 ... This naive model achieved only 2-3 hits".
- Measured (practitioner, 3 windows × 2 seeds):
  - rmse puts the raw-L2 LightGBM first (23.95), although it is last of the LightGBM models on Hits@10 (6.16);
  - rmse puts the Huber model last (27.69), although it is first on Hits@10 (6.70);
  - rmse rates the desk's sort by comments of the last 24 hours as worse than the training mean (44.0 against 31.6), although the sort finds 5.63 hits a day and the mean 1.08.
- More from the other audits:
  - the top 1% of test rows carry 68-92% of the squared error;
  - Kendall's tau between rmse and Hits@10 is 0.30, 0.30 and 0.89 over the three windows (claim audit 40);
  - rmse is the only measure that prefers dropping the blog statistics (split audit).

  A benchmark scored this way rewards sizing about two dozen viral posts per window, not ranking the day.
- Rules: MET-1 (Must) outranks MET-5 (Should). The fallback in MET-11 applies only when "the task makes none obvious", and here the source fixes k = 10 per day (MET-7). The reason text is also wrong: "closed access, not read ... from a secondary source" (MET-11).
- Remedy, the mildest that works:
  - declare the source's per-day Hits@10 as `Metric.source`, built as a general custom metric (group = `basetime_day`, k = 10, a stated tie rule; MET-12, MET-13). The day exists in the data: 20 days per window, each with a real top 10. The repository accepts a metric input that is also the time column (`task_metric_input_is_model_input`, info), so MET-2 holds.
  - if the curator will not add a metric now, declare `rmsle` from context on a log1p target, as in onlinenewspopularity (precedent check M), with Hits@10 named as the original. Rmsle orders the models close to the daily measures (tau 0.60-0.75). It also settles the raw-scale target (CLEAN-16, MET-3; precedent check T).

  Raw rmse should not ship either way.

**7. Leg 2 of TP-10 is not addressed, and leg 1 is thin on the declared metric (P6; TP-10 Must).**
- Leg 2: `comments_24h_to_48h_before` is the target from two base times before (UCI attribute 53; the column audit's pairing), and `comments_change_24h` is the difference of two lags. Leg 2 allows only the last observation (rain_in_australia, 2026-10-26).
- Leg 1: on rmse, LightGBM beats the best per-post naive forecast in window 1-20 by only 3% (25.2 against 25.9). On the daily measure the margin is clear: +1.03 hits a day over the sort by last-24h comments (paired SE 0.14).
- Remedy: one TP-10 line in the notes: a post lives at most 72 hours and has three rows, and these columns are the source's window counts since publication, like g_research's trailing returns (precedent check S, option a). Measure leg 1 on the metric chosen in point 6.

</details>

<details><summary>Advocate rebuttal</summary>

**Advocate's rebuttal: blogfeedback (advocate, 2026-11-01)**

**Where we stand.** The critic and I agree on the verdict: ship after changes, with no exclusion. We agree on most of the fixes too. I concede points 1, 5 and the post_length half of 3 in full. On the metric (point 6) I now accept the critic's order. I narrow points 2, 4 and 7. I contest only the word flags, which LEAK-31 leaves to the curator, and the parents' label. I ran two new checks:
- r1: Buza's word score, computed on training rows and on test rows.
- r2: TP-10 leg 1 on rmsle and on Hits@10 per day, and how precisely Hits@10 separates models with 20-day against 6-day windows.

**Critic 1 (use case, USE-1, USE-8): conceded.**
- This is my own point 1. Take the actor, the moment and the decision from the chapter.
- I also accept the addition: any leak kept with a note is named in `fit_reason` as kept (USE-8; african_credit_scoring_challenge, 2026-10-21).
- Under my reading of point 2 that is only the word flags, if they stay. The parents are not a leak.

**Critic 2 (leak notes): conceded except one detail, the parents' label.**
- The "every test blog is in the training file" note, the residual 5-fold shift, the wording of "scores the same", the count of 554 blogs, the "Revisit" line and the `CONSTANT` comment are all text fixes. I concede each of them, with the remedies the critic gives.
- The parents' label: the critic offers either "drop the label" or "keep it with the corrected evidence and name the leak in `fit_reason`". I contest the second option.
  - LEAK-10's second clause applies to "a value read at a later pull". The column audit shows these values are not that: with an unchanged parent set, max and mean only rise between base times (96 and 97 rises in 1,587 pairs, no fall), and every fall comes with a shrinking set (702 of 731 changes).
  - With the clause not triggered, there is no kept leak to name. The label goes, and a plain note explains the mechanism.
  - The decision rests on that fact (option a of check P), not on the drop test. That is the point the critic rightly says the precedents require.

**Critic 3a (word flags, LEAK-31): narrowed. It is the curator's call, and I keep my preference for keeping them with a note.**
- What I concede: the description "frequent words" is wrong. They were chosen with the label (footnote 1), and the notes must say so.
- My check on which documents Buza used (r1) does not settle it.
  - Buza's footnote-1 score is positive for 70.7% of the 147 testable words on training rows, against 58.5% on test rows (comments before the base time: 78.9% against 64.6%). That leans toward a selection on training-period documents.
  - But the mean signed score on the target is slightly higher on test (0.019 against 0.014), and every score is tiny (mean |score| below 0.13).
  - So the test period cannot be ruled out (EV-6). Whatever documents were used, the words barely separate posts in either period.
- What decides LEAK-31's "measure it; keep with a note when small" is the drop test on the test windows. Without the words, R² on log1p is 0.6559 against 0.6549 with them, and AUC is 0.9073 against 0.9083. A selection that used test labels would show a gain on test. There is none.
- On "remove it when we can": the rule also says a selection the source published is decided case by case (Lennart, 2026-10-21).
- The precedent differs in one fact. qsar_bioconcentration dropped the authors' 9 descriptors because RDKit descriptors of the same structures carried the signal: a substitute existed. Here the flags are the only content of the post in the data, and the practitioner lists the text as an input every monitoring desk has.
- Keeping them costs nothing measured, and dropping them costs nothing measured. Both are defensible, so the curator decides.

**Critic 3b (post_length 0, CLEAN-10): conceded.** Set it to missing after step 3. This is my own point 7.

**Critic 4 (3 windows, SPLIT-15): narrowed.**
- What I concede:
  - the heavy-tail fact rests on rmse, and it falls away if raw rmse goes;
  - the stated reason, SPLIT-19, does not decide between 3 and 9 windows;
  - an `Exception to SPLIT-15` line must be recorded either way;
  - the SPLIT-20 clause (the crawl is a single time value) should be added.
- Facts for 3 × 20 days that survive point 6 (r2, plus the split audit):
  - Every test day is used. Nine 6-day windows leave days 1-6 untested: 54 of the 60 days, in a pool that cannot grow (SPLIT-17's reason).
  - Under a per-day metric, one window's Hits@10 has an SE of 0.24 over 20 days and 0.44 over 6 days. The model differences the practitioner found are about 0.5.
  - The source applies one model to all 60 days (SPLIT-12).
- Against my case: the main difference I measured, log1p against raw (+0.57 a day), keeps its sign in all nine 6-day blocks. So 9 windows would not break the benchmark either.
- This stays a weighing call for the curator. Both options keep the dataset.

**Critic 5 (source, year, quotations; PROV-8, PROV-9, PROV-16): conceded.** This is my own point 5 plus the wording list in my point 7.

**Critic 6 (metric, MET-1): conceded, and I move to the critic's order.**
- Raw rmse should not ship.
- Two corrections to my opening brief:
  - I said Hits@10 would need `basetime_day` moved from feature to scoring column (MET-2). The repository says otherwise. A metric input may be the time column (`bundle_checks.py`, `task_metric_input_is_model_input`, info), and declaring the time column as a scoring column is an error (`task_scoring_column_is_feature`). So Hits@10 needs no feature change. Its only cost is the new metric (MET-12, MET-13: a general per-group top-k, k = 10, with a stated tie rule and a reference implementation).
  - I called rmsle the mildest remedy that resolves the problem. It does not resolve MET-1, which asks for the unit the actor acts on. Rmsle pools rows and agrees with the daily measures only at tau 0.60-0.75.
- Hits@10 per day resolves MET-1 exactly. It is precise enough on our folds (MET-10): window SE is 0.24, and the log1p-raw difference of 0.57 holds in every window.
- So: Hits@10 as `Metric.source` first. If the metric cannot be built in this change, rmsle from context on a log1p target, with Hits@10 named as the original (MET-11).

**Critic 7 (TP-10): narrowed. Leg 1 is clear on both candidate metrics.**
- The 3% margin is a fact about raw rmse, which both briefs now drop. Measured (r2, one seed):

| Window | rmsle: LightGBM log1p | rmsle: best naive (last 24 h × 0.20) | Hits@10 a day: LightGBM | Hits@10 a day: best naive sort |
|---|---|---|---|---|
| Days 41-60 | 0.667 | 0.820 | 6.20 | 5.35 |
| Days 21-40 | 0.563 | 0.696 | 7.20 | 6.20 |
| Days 1-20 | 0.626 | 0.752 | 6.60 | 5.35 |

  - On rmsle, LightGBM is 18-19% better in every window. On Hits@10 it finds 0.85-1.25 more posts a day.
  - The naive rules tried are the last-24h count, the total and the 24-hour rate, each with its rmsle scale fitted on the training side.
- Leg 2: agreed, option (a). Add one TP-10 line to the notes.

**What is left for the curator.**
1. The word flags: keep with a note (my preference) or drop (the critic's). LEAK-31 leaves this case by case.
2. The windows: 3 × 20 days with an exception, or 9 × 6 days.
3. The metric: Hits@10 per day now, or rmsle as a stand-in until it is built.

Everything else both briefs ask for is text or metadata, plus one line of cleaning (`post_length`).

</details>

<details><summary>Critic rebuttal</summary>

**Critic, rebuttal: blogfeedback (2026-11-01)**

**Where we stand.** The advocate and I agree on the verdict (ship after changes) and on most of the remedies. Three disagreements remain:
- which metric replaces raw rmse;
- whether the word flags are dropped or kept with a note;
- which facts the SPLIT-15 exception may rest on.

I ran one check for the rebuttal (script and output in the run folder). It used untuned LightGBM on log1p on the shipped frame.

Two corrections to my opening brief:
- In Buza's Table 1, the textual features lower Hits@10 for 6 of 7 models, not 5. Only the REP tree rises, from 5.767 to 5.783.
- My point 7 called TP-10's leg 1 "thin". That is withdrawn; see A4.

**A1. The task is real and the source states the use case (USE-1, USE-8). Conceded.** Same remedy as my point 1: take `use_case` and `fit_reason` from the chapter, and keep `approximate` because of the undated crawl. One consequence: if the word flags stay with a `Potential leak` note (A7), USE-8 requires `fit_reason` to name them as kept.

**A2. The curator's condition is met and the test side is clean (LEAK-10, LEAK-29). Conceded.** No test label reaches a test feature, and the blind reviewer had not seen the definition. Narrowed on one detail: the sentence on the residual should also say that tuning on the training rows is slightly optimistic (inner-CV gain +0.058 to +0.061, against +0.048 on test; claim audit 15).

**A3. The split mirrors the decision and every Must holds. Conceded, except the facts of the SPLIT-15 exception, which I contest.**
- I accept the regime, the known-blog rewrite (at least 90.6% of test rows), `basetime_day` as a feature, and no data change for the encoding of "no history" (0 on the test side, missing on the training side), since predictions on those rows are calibrated.
- Exception to SPLIT-15: I accept 3 windows of 20 days, but two of the advocate's supports do not hold.
  1. The heavy tail is a fact about rmse, and the advocate's own A6 drops rmse. Share of squared error held by the top 5 rows of a window, crawl-only model:

     | windows | rmse | rmsle |
     |---|---|---|
     | 3 × 20 days | 39-54% | 9-10% |
     | 9 × 6 days | 65-92% | 16-25% |

     Under rmsle, no handful of rows decides a 6-day window.
  2. "P6: every fold can be scored" is not at stake. A 6-day window holds about 700 rows and six days that each have a real top 10.
- The facts that do hold, and that the exception should name:
  - the test pool is fixed at 7,036 rows (SPLIT-17's reason);
  - the source applies one model to all 60 days (SPLIT-12);
  - if Hits@10 is adopted, resolution (MET-10, TP-1): over 20 days the paired SE of a model difference is 0.26 hits a day, over 6 days 0.48, while the gaps between models are about 0.5.

**A4. The task is worth benchmarking and tabular (TP-2, TP-4, TP-10). Conceded.**
- My "thin" referred to rmse, where window 1-20 was won by 3%. On either replacement metric, leg 1 is clear in every window:

  | window | rmsle, LightGBM | rmsle, best scaled naive | Hits@10, gain over the last-24h sort |
  |---|---|---|---|
  | 41-60 | 0.667 | 0.817 | +0.70 (SE 0.29) |
  | 21-40 | 0.562 | 0.696 | +1.25 (SE 0.28) |
  | 1-20 | 0.619 | 0.754 | +1.35 (SE 0.27) |

- Leg 2: option (a) as the advocate states it. What is left of my point 7 is one TP-10 line in the notes, with leg 1 measured on the metric that is chosen.

**A5. The data is faithful, unique and traced to its first publication (PROV-8, PROV-9, LEAK-19). Conceded.** We agree on the metadata fix. I checked the byte identity myself: 61 of 61 files are identical. The PROV-16 quotation fixes are in the advocate's A7.

**A6. The metric is a real problem, fixed in the definition (MET-1). Agreed that raw rmse goes. Contested: rmsle is not the right replacement, and Hits@10 costs less than the advocate says.**
- **MET-11 (Must) gives rmsle no origin here.** "Context" is for a source that "defines no metric". This source defines Hits@10 and AUC@10 (Sec. 5.1). A stand-in needs an original that cannot be computed, and this one can be. What set onlinenewspopularity apart is that its source had no metric for the regression (precedent check M), and that fact is absent here.
- **MET-1 (Must) asks for the unit the actor acts on, the day's top 10.** Rmsle still pools rows across days. Its agreement with Hits@10 is partial: Kendall's tau 0.75, 0.60 and 0.60 (claim audit 40).
- **MET-7 and MET-5 point the same way.**
  - The source fixes k = 10 per day (MET-7).
  - The text compares models by hits: "The number of hits was around 5-6 ... This naive model achieved only 2-3 hits". AUC@10 scores the same top-10 set, so it does not compete as a criterion.
- **The cost.**
  - The advocate says `basetime_day` would have to move from feature to scoring column (MET-2). In this repository a time column cannot be a `ScoringColumn` (error `task_scoring_column_is_feature`). A metric input that is also the time column is accepted with an info (`task_metric_input_is_model_input`, `src/data_foundry/bundle_checks.py`, around line 1046). So no feature changes; the only work is a general per-group top-k metric (MET-12, MET-13).
  - That metric is not a one-off: Singh et al. 2015 (Sec. IV-E) score the sibling `facebook_comment_volume` with Hits@10 and AUC@10.
  - If the curator reads MET-2's "never a feature" strictly, the split audit shows the day as a feature is harmless (R² 0.432 with it, 0.464 without, in window 41-60).
- **Position.** Declare Hits@10 per day as `Metric.source`, with the tie rule stated (6.68 counting ties, 6.52 strict). Rmsle on a log1p target is acceptable only as an interim, if the metric work is deferred, and its reason must name Hits@10 as the original. This is the curator's weighing call, and both ways keep the dataset.

**A7. The rest are cheap fixes.**
- Parents: conceded. Option (a), a plain note with the column audit's evidence.
- `post_length` 0 to missing, the wording fixes, and removing the `Data Quality Issue` marker: agreed.
- **Word flags: contested (LEAK-31, Should).**
  - The rule reads "keep with a note when small, remove it when we can". All three of its cases were removed: home_credit_default_risk, qsar_bioconcentration and numerai_v5_2_1m (leak_checks.md, Cases table). None was kept with a note.
  - qsar_bioconcentration matches: a selection the authors published, worth +0.002, removed. The advocate names no fact that sets blogfeedback apart (principles.md: like cases alike).
  - Here the words are worth nothing or less: R² on log1p −0.001, AUC +0.001, and rmse 0.9 worse with them. The source's own Table 1 shows the text lowering Hits@10 for 6 of 7 models.
  - Which documents chose the words cannot be checked, so a note would record a suspicion that can never be settled.
  - Remedy: drop the 178 columns. This is a Should, so it is the curator's call and not a reason against shipping.

</details>
