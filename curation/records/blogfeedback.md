---
unique_name: blogfeedback
name: BlogFeedback / Blog comment volume prediction (Buza 2014, UCI 304)
checked_by:
- Andrej
data_foundry_status:
- WIP (DF)
claimed_by: Andrej
suggestion: 'Yes'
priority: 3
tags:
- Two-Regime Zeros
- Non-IID (Temporal)
- Many features
original_source: UCI
year: '2014'
domain: technology & internet
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://archive.ics.uci.edu/dataset/304/blogfeedback
- https://doi.org/10.24432/C58S3F
- https://doi.org/10.1007/978-3-319-01595-8_16
- http://www.cs.bme.hu/~buza/blogdata.zip
- http://www.cs.bme.hu/~buza/pdfs/gfkl2012_blogs.pdf
v2_path: datasets/_dev/tabarena-v0pt2/blogfeedback/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-20 from a web search for zero-inflated regression candidates, the source pages and, where the notes say so, the downloaded data. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `TBD -> Yes`, priority 2: comments on a blog post in the next 24 hours, with the
source's temporally disjoint test period and an observed zero regime (64.0% in train, 70.2% in test, earlier AI triage,
2026-10-20, measured); the design of `facebook_comment_volume`, on other data.
- Source: Krisztian Buza, UCI 304, "Donated on 5/28/2014", 60,021 instances, CC BY 4.0 (UCI page); the chapter "Feedback
  Prediction for Blogs" (GfKl 2012, Springer 2014, pp. 145-152; closed access, not read). As published: one train file
  with base times in 2010-2011 and 60 daily test files of February-March 2012, 280 features and the target; UCI: "The
  prediction task associated with the data is the prediction of the number of comments in the upcoming 24 hours".
- Use case: for example, a blog portal picks which posts to feature from their expected discussion over the next day
  (UCI names no actor; the chapter not read); fit approximate. Regime temporal, the source's split (UCI: "use the
  provided, temporally disjoint train and test splits"); posts recur at several base times, so tuning folds group by
  post (earlier AI triage).
- Siblings and duplicates: `facebook_comment_volume` (TBD -> Yes, Lennart) reuses this design on Facebook pages (Singh
  et al. 2015, earlier AI triage): other data, not a duplicate (PROV-4). External collections: none found.
- Papers and pages: Buza 2014; Singh et al. 2015.
- Metric: none found (UCI states none; the earlier AI's reading that the chapter ranks by Hits@10 is unverified), so the
  fallback `rmse`; a top-10 per day would need the day as a scoring column, which only the test files give.
- Risks for /add-dataset: the blog-level aggregates (features 1-50) cover an undocumented period that may reach past the
  base time (LEAK-10 to check); 3,194 exact duplicate rows, 355 feature vectors with two targets and 24% of train rows
  without text (earlier AI triage; `Data Quality Issue` kept as in the sibling, though it reads as a cleaning question);
  every test blog is in train (a known entity, USE-10). No open family question applies (no comment is an observed
  zero).
- Priority: gap 0 (technology & internet 4, regression and temporal not thin), use case 0 (none named), source + (UCI's
  documentation and the chapter), shape + (60,021 rows, 280 features, dated test files), risk - (aggregates of unknown
  period, duplicates).

**Consistency check (AI, 2026-10-30):** the review page sets 2nd Tier ("Leaks are very likely so we rather prioritize
other datasets"). `facebook_comment_volume` has the same design (Singh et al. 2015 reused Buza's) and stands at TBD ->
Yes, and on the same page leaks in `loan_default_prediction_imperial_college` and `nfip_redacted_flood_claims` were sent
on to be fixed. What may set it apart: the aggregates cover an undocumented period, so the leak cannot be located and
removed (LEAK-10). Options: 2nd Tier with that fact (and `facebook_comment_volume` reconsidered), or TBD -> Yes like
facebook.

CC (2026-10-30, Andrej): `TBD -> Yes`, priority 2 (the AI screening had `TBD -> Yes`, priority 2; zero-inflated
screening review page, after the AI's consistency check). "Move to zes if zou can resolve the leak, otherwise no"

**Assessment (AI, 2026-10-30):** the leak check the curator asked for ("Move to zes if zou can resolve the leak,
otherwise no"), on the UCI files and attribute list (Buza's chapter not read). Located: the 50 source aggregates (avg,
std, min, max, median of a51-a60 per blog) are the statistics over all rows of the blog in the training file, duplicates
included (avg, min, max and median match 100%), so a training row's aggregates contain the same post at later basetimes:
the next day's a51 equals a51 plus the target in 99.8% of pairs. The test rows carry the same 2010-11 values (they match
the test rows' own statistics 0.1% of the time), history known before every Feb-Mar 2012 basetime, so the leak sits on
the training side and does not reach the official test. The comment windows a52/a53 are adjacent to the target window,
not overlapping (a52 of the next day equals the target in 99.9% of consecutive test pairs). No post crosses from train
to test. Fix: keep the official split, recompute the training rows' aggregates out of fold (5 folds grouped by post,
exact from a51-a60; not leave-post-out, which makes a leave-one-out encoding leak), drop the 3,194 exact duplicates and
group tuning folds by post (355 vectors carry two targets). Untuned LightGBM on the official test, 3 seeds: pre-basetime
counts alone AUC 0.892 for any comment and R^2 0.594 on log1p; as published 0.906 and 0.653; aggregates dropped 0.898
and 0.607; aggregates recomputed out of fold 0.913 and 0.653. The leak is resolved.

CC (2026-10-30, Andrej): `Yes`, priority 2, by the curator's rule on the page ("Move to zes if zou can resolve the leak,
otherwise no"): the leak is resolved (Assessment above).

Krisztian Buza's crawl of Hungarian blog posts (UCI 304; Singh et al. 2015, Sec. II, p. 2: "feedback prediction on
Hungarian blogs"). A row is a post at a base time with 280 features known then (earlier comments and trackbacks, blog
aggregates, length, 200 unnamed word counts, weekdays); the target is the comments in the next 24 h, zero when none
came. Distinct data from `facebook_comment_volume`, which reused this design on Facebook (citing it as [5]).
Measured: train 52,397 rows (base times 2010-2011, no date column), 64.0% zero; 60 daily test files
(Feb-Mar 2012), 7,624 rows, 70.2% zero. Split: the provided temporal one (UCI: train base times "may temporally
overlap"); windows can only be cut from the test days. Probe on it: ROC AUC 0.906 for any comment, R^2 0.517 on
log1p among positives; the last 24 h of comments alone give AUC 0.859 and R^2 0.33.

Each text-bearing train post appears at a median of 3 base times (12,461 posts). No post is in both train and test,
so only tuning folds need grouping by post. The blog aggregates are constant per blog and every test blog is in
train; the period they cover is undocumented. 3,194 exact duplicate rows, 355 feature vectors with two targets and
12,750 train rows (24%) without text are the `Data Quality Issue`, as in the sibling. To check: Buza's chapter (closed
access, not read) for the crawl, the aggregates and its top-10 metric (Hits@10). Licence: CC BY 4.0.

**Assessment (AI, 2026-11-01):** added as `datasets/_dev/tabarena-v0pt2/blogfeedback/` by /add-dataset with the full review panel; the open questions are in its `REVIEW.md`. Recommend shipping; none of its three open issues can turn it to `No`. Your condition of 2026-10-30 is met: the 50 blog statistics of the training rows, which included the post's own later counts, are recomputed from the blog's other posts (the test rows' statistics were already history; untuned LightGBM RMSLE 0.620 with the published, 0.622 with the recomputed ones). Changes after the panel: scored by RMSLE as a stand-in until the source's Hits@10 per day is in the metric library (its issue 3); a post length of 0 made missing. Superseding readings above: Buza's chapter was read (author's copy added to the links): it names the actor (a proof of concept with Capgemini Magyarorszag for companies that must react quickly to blog discussion), scores Hits@10 per day, and chose the 200 word flags by their gap in comment counts, not as frequent words (its issue 1), so "closed access, not read" and "Metric: none found" no longer hold; Buza's `blogdata.zip` of 2012 is byte-identical to UCI's files; on the shipped data the 99.8%, 99.9% and 12,461 posts above are 99.89%, 99.73% and 12,526. `Data Quality Issue` removed: the leak and the duplicate rows are repaired, and selection.md keeps the marker for damage that cannot be repaired. `year` and `original_source` wait for your marks on the field rows. Priority 3: gap 0, use case + (actor named by the source), source + (author's release and chapter), shape + (56,239 rows, temporal), risk - (word flags possibly chosen on the test crawl; the metric is a stand-in).

CC (2026-11-02, Andrej): metric (REVIEW.md issue 3, cross-dataset item zi-hits10): "add the metric and the MET-2 note". Buza's Hits@10 per test day is the metric, with the test day as its group; MET-2 does not cover the time column used as the metric's group.

**Assessment (AI, 2026-11-02):** applied. `mean_group_top_k_overlap` (per group, the share of the k highest true values among the k highest predictions, averaged over the groups; ties at a cut-off counted by their expected share, so the score does not depend on row order) is in `data_foundry.v2.metrics`, tested against Buza's definition as a loop (equal without ties, and equal to the mean over every tie-break on a small case). The definition declares it as the source's metric, `Metric.source("mean_group_top_k_overlap", params={"k": 10}, inputs={"group": "basetime_day"})`, replacing the RMSLE stand-in; the score is Hits@10 / 10. Check on the shipped windows: a sort by the last 24 hours' comments finds 5.25, 6.02 and 5.29 of each day's top 10, a constant prediction 0.8-0.9 (the issue's 5.6 counted ties at the 10th place as hits). MET-2 amended in metrics.md (Cases row, kind `amendment`). `dataset check`: 0 errors.

## Reference

Buza, K. (2014). Feedback Prediction for Blogs. In: Spiliopoulou M., Schmidt-Thieme L., Janning R. (eds), Data
Analysis, Machine Learning and Knowledge Discovery. Studies in Classification, Data Analysis, and Knowledge
Organization, Springer, pp. 145-152. doi:10.1007/978-3-319-01595-8_16.

Buza, K. (2014). BlogFeedback [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C58S3F.

Lead: web search 2026-10-20 for zero-inflated regression candidates (not in the v4 workbook).
