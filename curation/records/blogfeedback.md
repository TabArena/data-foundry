---
unique_name: blogfeedback
name: BlogFeedback / Blog comment volume prediction (Buza 2014, UCI 304)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
decision_markers:
- Data Quality Issue
tags:
- AI-Filled (Verify)
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
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-20 from a web search for zero-inflated regression candidates, the source pages and, where the notes say so, the downloaded data. A human must verify the suggestion, the metadata and the notes before relying on them.**

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

## Reference

Buza, K. (2014). Feedback Prediction for Blogs. In: Spiliopoulou M., Schmidt-Thieme L., Janning R. (eds), Data
Analysis, Machine Learning and Knowledge Discovery. Studies in Classification, Data Analysis, and Knowledge
Organization, Springer, pp. 145-152. doi:10.1007/978-3-319-01595-8_16.

Buza, K. (2014). BlogFeedback [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C58S3F.

Lead: web search 2026-10-20 for zero-inflated regression candidates (not in the v4 workbook).
