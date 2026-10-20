# onlinenewspopularity

**Outcome:** added. A temporal regression of ln(shares) of Mashable articles: nine two-week test windows (August to
December 2014) with a one-week gap. The weekday flags, `timedelta` and the LDA columns are dropped; the keyword and
self-reference statistics are kept as potential leaks. The AI recommends shipping it, with the concerns below.

**Main points:** A regression of log shares instead of the paper's binary task. The LDA columns are dropped; the
keyword statistics are kept as a potential leak.

**Record judgment:** valid with concerns. The source's task is predictive by design (rolling windows, Sec. 2.3 and
3.1), and no other record or folder holds the data. The text-derived columns add R^2 0.003, so the `NLP (Text)` marker
the curator accepted fits; `Wrong Domain / Source Modality` is not borne out (issue 8).

**Issues for Lennart:**

1. **Target: regression or the paper's binary task?** The paper and UCI frame "popular" as shares above D1 = 1,400
   (Sec. 3.1, p. 7; UCI's class table counts 1,400 itself as popular, the paper's text says "higher than"; 1,592
   articles have exactly 1,400). Implemented: regression on ln(shares), which keeps that split and the order within
   each class (R^2 0.158; OpenML 4545 and AutoML_MM also use the count). Alternative: binary target in a second folder
   `onlinenewspopularity_clf` (ROC AUC 0.733 on the same windows; the paper's random forest 0.73).

2. **UCI's `timedelta` and weekday flags do not follow the publication date.** The flags are the weekday of 2015-01-08
   minus `timedelta` in 100% of the rows, but that date falls 1 to 5 days after the date in the URL for 9,463 articles
   (24%; every article of December 2014; in late 2014 it looks like the next working day of the authors' pipeline: all
   60 articles of Friday 2014-12-05 carry Monday 12-08). Mashable's own pages carry the URL date (Wayback snapshots of
   2014-12-31: star-wars-the-force-awakens-character-names "Thu, 11 Dec 2014 21:11:08 +0000", authors' date Dec 15;
   rape-threats-contact-mothers "Mon, 01 Dec 2014 08:20:04 +0000", authors' date Dec 3; three current pages agree).
   The shift goes with the outcome (within a URL date, shifted articles +0.038 log shares, unshifted -0.010; before
   April 2014 +0.205 for 427 articles), and adding the flags and `timedelta` raises R^2 from 0.158 to 0.166.
   Implemented: dropped; the weekday comes from `publication_date` (skrub `DatetimeEncoder(add_weekday=True)` in
   `tabarena_default`, `dayofweek` in AutoGluon's generator). Alternative: keep the published flags. Every copy of this
   dataset (UCI, OpenML 4545, benchmarks built on them) carries this.

3. **LDA columns: dropped (verifier's finding 2).** The paper: LDA "was applied to all Mashable texts (known before
   publication)" (Sec. 2.1, p. 4); each channel loads on the same topic in both years (business 0.64-0.67 on LDA_00 in
   every quarter, world 0.65-0.72 on LDA_02, tech 0.67-0.71 on LDA_04), so one model, by the paper's wording fitted on
   all texts, test windows included: a transform fitted on the full set (rubric item 6). The five columns carry no
   measurable signal (R^2 0.1580 with, 0.1582 without, 3 seeds; in the untuned model of the leak probe -0.004 to
   +0.002).
   Alternative: keep them with a note (my first version; the record's first comment suspected a leak).

4. **Windows and gap.** Implemented: 9 x 2 weeks with a one-week gap, after the paper's rolling test sets of 1,000
   articles (two to three weeks) and its remark that shares of some articles younger than 4 days had not settled (Sec.
   2.1, p. 3). Alternatives and R^2: no gap 0.160; a three-week gap (the paper's discard rule) 0.153; monthly windows
   would put the oldest test window in April 2014 (not run).

5. **Keyword statistics: kept as a potential leak (verifier's finding 1).** They summarize the articles with an
   earlier authors' date (issue 2), so for the 24% of shifted articles they include same-day articles, some published
   hours later: yahoo-qwiki-brief (2013-07-03 13:37 UTC, authors' date 07-04) holds `kw_max_max` 843,300, the shares
   of low-cost-iphone (19:07 UTC that day), and none of the 66 unshifted articles of that day holds it. Never a later
   day. 4,031 of 8,289 test rows (49%) have same-day articles in their pool (median 32, at most 94). Diff-in-diff over
   15 two-week windows of 2014: the keyword columns lower the MSE by 0.0245 for shifted and 0.0172 for unshifted test
   articles, difference 0.007 (SE 0.006, 8 of 15 windows above 0; the verifier's run on the first version: 0.0007, SE
   0.0044), against an MSE of about 0.66: not distinguishable from 0. They also use the 2015 crawl's share counts.
   Alternative: drop the nine `kw_*` columns (R^2 0.158 -> 0.135); the paper's most important feature is `kw_avg_avg`.

6. **Self-reference statistics: kept as a potential leak.** They come from the page at the crawl, so a link added after
   publication can point to a newer article: ionut-budisteanu-self-driving-car (2014-04-08) holds 663,600, the shares
   of first-100-gilt-soundcloud-stitchfix (2014-04-09). Of 906 articles whose self-reference minimum or maximum equals
   one of the 136 share counts of 50,000 or more held by one article, 4 are 1-2 days older than it (47 more are 6+ days
   older, likely other pages with the same count). Alternative: drop them (R^2 0.158 -> 0.143).

7. **Text.** Every URL still resolves (to mashable.com/archive/<slug>), the slug holds title words, and AutoML_MM's
   OpenML 46662 has full titles for 24,007 articles. A TF-IDF of the slug adds nothing (R^2 0.152 vs 0.158), so no text
   column. A text variant (titles or bodies) would need a scrape of Mashable's pages (Mashable holds the rights).

8. **Record fixes to consider:** add OpenML 4545 as a link (the record's OpenML links are AutoML_MM's derived
   tasks), and the modality markers (the data does not support `Wrong Domain / Source Modality`). The `.names` file
   says 39,797 instances; the CSV and its class table hold 39,644 (the paper rounds to 39,000). Label maturity was
   checked: the 481 articles under three weeks old at the crawl show no deficit of shares (last week median 1,600, 65%
   at 1,400 or more; the 8 weeks before: 1,100-1,400, 42-52%).
