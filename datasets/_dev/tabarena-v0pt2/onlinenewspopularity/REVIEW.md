# onlinenewspopularity

**Outcome:** added. Not built yet. The AI recommends shipping it with the changes the panel agreed, which the definition
contains. A temporal regression of ln(shares) of Mashable articles: nine two-week test windows (August to
December 2014) after a one-week gap. Validity: SEL-12 holds (no text ships); USE-1 and USE-3 hold, fit `direct`
(USE-8 as amended 2026-10-21: the kept leaks are noted, not gaps); LEAK-10 triggered, fixed (`timedelta` and the weekday flags follow a later date: dropped, the date taken from
the URL); LEAK-30 fixed (LDA columns dropped; unlike the keep-with-note cases of 2026-10-19, because they carry no signal and
cannot be refitted without the texts); LEAK-24 not triggered (no share deficit in the newest weeks); the
keyword and self-reference columns, which hold share counts read at the crawl, are kept with a note (LEAK-6), which
departs from LEAK-10 (Must) as written and needs its amendment (issue 5);
SPLIT-1, SPLIT-10, SPLIT-11 and SPLIT-15 hold. Value: TP-2, a small real signal (LightGBM above the dummy on every
split). Quality: CLEAN-11 and CLEAN-5 fixed; CLEAN-13 open (issue 9). Weighed: the kept crawl-time counts (masking the young
ones changes R^2 by -0.0004) against the 15% and 9% of the signal the two groups carry. Left for the curator: issues
5, 8 and 9.

**Main points:** Keep the keyword and self-reference statistics with a note and amend LEAK-10 for them (issue 5);
remove the record's `Wrong Domain / Source Modality` marker (issue 8); decide `data_channel` with mortgage's CLEAN-13
amendment (issue 9).

**Record judgment:** valid with concerns: the crawl-time counts kept with a note (issue 5) and a modality marker the
data does not bear out (issue 8). The source's task is predictive by design (a decision-support system that
scores articles before publication, evaluated on rolling windows), no other record or folder holds the data, and the
release holds statistics of the text, not the text.

**Issues for Lennart:**

5. **Keep the keyword and self-reference statistics, whose share counts were read at the crawl, with a note?** The
   nine `kw_*` columns summarize the shares of earlier articles that share a keyword with the article; the three
   `self_reference_*` columns summarize the shares of the earlier Mashable articles it links to. Both hold the counts
   of the crawl of 2015-01-08, not the counts when the article was published. Some come from articles only days
   older, whose shares an editor would have seen lower. A value is traced when it equals a share count of 5,000 or
   more that exactly one article in the release holds, which identifies the article it comes from. At least 0.9% of
   the test rows hold the count of an article from the gap week (the week between the last training date and the
   start of the test window, left out of training) or from the same test window, and 0.4% that of an earlier test
   article of the same window (lower bounds: untraced values cannot be checked).
   - Effect on the task: a slight optimism on those rows; the model sees settled counts where a deployed one would see
     younger ones. For 80% of the test rows the authors' date lies 1 to 5 days after the URL date, so their keyword pool
     also holds same-day articles published later; that part brings no measurable gain (difference in squared-error
     gain -0.008, SE 0.008).
   - Evidence: the mediator traced the counts and masked the young ones (LightGBM, the 9 windows, 3 seeds):

     | Measurement | R^2 |
     |---|---|
     | All columns | 0.1553 (seeds 0.1543-0.1563) |
     | Cells traced to an article under 8 days older masked (2,907 cells; 55 test rows) | 0.1549 |
     | Under 28 days masked (7,296 cells; R^2 rises, so the younger counts do not help) | 0.1571 |
     | Without `kw_*` / without `self_reference_*` / without both | 0.1311 / 0.1414 / 0.1089 |

     Per test row, the two groups reduce the squared error by 0.112 (SE 0.081, 55 rows) where the source article is
     under 8 days older, against 0.045 (SE 0.019, 818 rows) where it is 28 days or older; the difference, +0.067 (SE
     0.083), is not distinguishable from 0.
   - Implemented: kept, with two `Potential leak, kept on purpose:` notes that name the mechanism and the measurement;
     the fit reads `direct` (USE-8 as amended, Lennart, 2026-10-21: a kept leak does not make the fit approximate).
   - Alternatives: mask the traced cells (changes nothing measurable, reaches only the traceable cells, and its pattern
     of missing values would come from other rows' labels, test rows included); or drop both groups (R^2 0.155 to
     0.109; the paper's most important feature is `kw_avg_avg`).
   - Rule: LEAK-6 (Must: measure before acting; a slight optimism with a known cause can stay with a note); LEAK-10
     (Must: a value looked up after the outcome goes unless the data shows it did not change); LEAK-34 (Must: a
     newsroom's own history is legitimate under a temporal split); LEAK-7 (Should: the smallest fix that keeps a valid
     signal). A Must takes no exception, so the keep needs an amendment of LEAK-10: "a value read at a later pull stays
     with a note when its effect is measured small". Its cases would be house_sales, aeolus and this dataset, plus
     melbourne_housing_market and african_credit_scoring_challenge unless they are fixed instead, all AI decisions so
     far. Decide it together with the working copy's item "Keep a post-outcome lookup because removing it changes no
     score?": its option (a) blanks the values in those two datasets, which cannot be done here because only traced
     cells can be found, and its option (b) amends LEAK-11; one amendment, of LEAK-10, should cover both.
   - Precedent: departs from santander_customer_transaction_prediction (Lennart, 2026-09-30: features that encode the
     labels of other rows of the test fold dropped at +0.003 AUC). What sets it apart: these values come only from
     earlier articles, in time order, and masking the young ones changes R^2 by -0.0004. The critic asked for the mask,
     the advocate for the keep; the mediator ruled the keep after the measurement. The 2026-10-07 review page holds no
     mark on this dataset.
   - Recommendation: keep with the note and adopt the LEAK-10 amendment.
   - Decision: keep and amend LEAK-10; keep without the amendment; or drop both groups, as santander.

8. **Remove the record's `Wrong Domain / Source Modality` marker?** The marker says the dataset belongs to another
   modality (text). The release holds statistics of each article, not its text: the 19 text-derived columns add 0.004
   R^2 (0.1515 to 0.1553), word counts of the URL's title part (the slug, weighted by TF-IDF) lower R^2 to 0.1517, and
   no text column ships. It comes after issue 5 because its effect on the task is none.
   - Effect on the task: none; the marker is the record's.
   - Implemented: nothing; markers are the curator's.
   - Alternative: keep it. `NLP (Text)` can stay as a note on the provenance; neither side contests it.
   - Rule: SEL-12 (Must) holds; a marker is argued from the feature composition (principles, "Arguing a call",
     internet_advertisements). Records with `Yes` keep this marker elsewhere (cardiotocography,
     electric_motor_temperature_prediction), so keeping it is not inconsistent.
   - Recommendation: remove it.
   - Decision: remove the marker, or keep it.

9. **Ship `data_channel` merged, or as six yes/no columns until CLEAN-13 is amended?** The six `data_channel_is_*`
   flags become one categorical `data_channel`. 6,134 rows (15.5%) have no flag and become the category `other`, which
   takes the place of a seventh flag; no row has two, so the merge loses nothing. CLEAN-13 (Must) allows a merge only when exactly one flag is set in every row.
   - Effect on the task: none on the score; a question of the rule's wording.
   - Implemented: merged.
   - Alternative: six separate yes/no columns, lossless and within the rule as written.
   - Rule and precedent: CLEAN-13 (Must). mortgage's `real_estate_type` uses the same reading, and mortgage's issue 12
     proposes the amendment "exactly one, or at most one with a reference level `other`"; both are AI decisions, not
     a curator precedent. The critic holds that the Must stands until amended; the advocate asks to avoid converting
     now and reverting later.
   - Recommendation: decide it with mortgage's issue 12 and ship the form chosen there; if the amendment is declined,
     or not decided before this dataset ships, six flags.
   - Decision: keep the merge and let mortgage's issue 12 settle it (that issue recommends the amendment), or ship six
     flags now and merge again if the amendment passes.

**Review panel:** ship after changes (mediator). Claim audit: of the definition's and the record's claims, 4 are
refuted or understated (`known` said the earlier articles' shares are known before publication; "a quarter of the
articles"; the record's `Wrong Domain` marker; the old comment that the LDA columns make random splits unusable), the
definition's ones fixed in it; the gain on links to articles at most 3 days old is untested (25 rows). Column audit: the
1.59 share count and `rate_negative_words` (fixed in the definition), `data_channel` (issue 9). Split audit: right with
notes (stated in `splits_comment`). Domain practitioner: fit `approximate`, as the definition says; a real
pre-publication task with a weak signal, capped by inputs the release lacks (author, headline, hour). Precedent check:
consistent on the target, the date repair, the windows and the fit; the LDA drop departs from the keep-with-note
pattern with a stated reason; the kept counts depart from santander (issue 5) and are a further case for a LEAK-10
amendment. Blind review: would include with changes; its main concern, the shorter exposure of the newest
articles to the crawl, is a season in both years, not a deficit. Debate: agreed on the task, the target, the split, the
drops and the fixes; disputed the remedy for the crawl-time counts (settled by the mediator's measurement, issue 5) and
when to settle CLEAN-13 (issue 9). The mediator's issues 1 and 2 are issues 5 and 9 here, its record change 8 is
issue 8. The reports cite the earlier REVIEW.md's numbers: 1 target, 2 dates, 3 LDA, 4 windows, 5 and 6 the kept
statistics (now issue 5), 7 text, 8 record fixes (now issue 8).

<details><summary>Mediator</summary>

**Judgment record**

```text
Verdict: ship after changes.
Validity: SEL-12 holds (no text ships; remove the Wrong Domain marker); USE-1/USE-3 hold, USE-8 approximate (stated);
  LEAK-10 triggered, fixed (timedelta, weekday flags dropped, date from the URL, PROV-13); LEAK-30 fixed (LDA dropped);
  LEAK-24 not triggered (no age deficit, measured); LEAK-6 kw_*/self_reference_* kept with a note (immature crawl
  counts measured: masking the traced young cells changes R² by -0.0004, within seed noise); SPLIT-1/10/11/15 hold.
Value: TP-2, a small real signal (R² 0.155-0.158, above the dummy on 100% of splits).
Quality: CLEAN-11 fix (mask 1.59); CLEAN-5 fix (drop rate_negative_words); CLEAN-13 pending (mortgage issue 12).
Weighed: none decisive.
For the curator: issue 1 (confirm the keep against santander; LEAK-10 amendment), issue 2 (CLEAN-13 with mortgage).
```

**Changes to make now (no decision needed)**

1. **`known`** (and the first curation bullet, "the shares of earlier Mashable articles are known"): change to "their shares at the crawl of 2015-01-08". The claim audit refuted the current wording (claim 6). Rule: USE-8 (Must), EV-8.
2. **`fit_reason` and the keyword bullet**: replace "a quarter of the articles" with "80% of the test rows (6,627 of 8,289; windows 0-2 entirely)". Rule: EV-8.
3. **Keyword bullet figures**: replace the 15-window numbers (0.0245 / 0.0172, SE 0.006) with the 9-window ones: shifted 0.0187, unshifted 0.0264, difference -0.008, SE 0.008. Rule: EV-8.
4. **Rewrite the two "Potential leak, kept on purpose" bullets** to name the mechanism and the measurement:
   - The values are the share counts at the crawl, including counts of articles from the gap week and from earlier in the same test window. That covers at least 0.9% and 0.4% of test rows.
   - Masking the 2,907 cells traced to an article under 8 days old moves R² from 0.1553 to 0.1549.
   - Optional, from the column audit: the page counts (`num_hrefs`, `num_imgs` and the rest) are also read at the crawl.
   - Rule: LEAK-6 (Must), writing.md.
5. **`splits_comment`**: add one sentence saying that labels are crawl-time counts for train and test alike, so the gap stands in for settling time only. Also state the paper's sliding window (W = 10,000) and why we expand instead (R² 0.146 vs 0.158). Rule: SPLIT-10, SPLIT-19 (note).
6. **The 1.59 share count**: mask `== 1.59` in `kw_max_min` (111 rows) and in `self_reference_min_shares`/`_max_shares` (10 / 3 rows). Also mask the matching averages where their min or max is 1.59. The notes already claim this is done; the code does not do it. Rule: CLEAN-11 (Should).
7. **Drop `rate_negative_words`**: it equals 1 - `rate_positive_words` in every defined row. Dropping it treats it the same as `n_non_stop_words`. Rule: CLEAN-5 (Should).
8. **Record**:
   - Remove the `Wrong Domain / Source Modality` marker: refuted on the data (text-derived columns +0.004 R², slug TF-IDF 0.1517 vs 0.1553, no text ships). Rule: SEL-12, "Arguing a call".
   - Add OpenML 4545 to `source_links`. Rule: PROV.
   - Keeping `NLP (Text)` is a record-field choice for the curator; neither side contests it.
9. **Rebuild and log**: README regenerated, a dated CHANGELOG entry, and REVIEW.md updated. These follow the house rules.
10. **mortgage REVIEW.md issue 12**: correct "shipped 2026-10-14". That merge was an AI decision from the 2026-10-07 run and is not a curator precedent (precedent checker, section 9).

**Issues for the curator (ranked)**

**1. P4, LEAK-6 / LEAK-10 (Must): keep the `kw_*` and self-reference crawl-time shares with a note**

- **Problem.** The values are share counts from the 2015-01-08 crawl, not counts as of publication. A few come from articles less than 8 days older than the row, including earlier test articles of the same window (at least 36 test rows).
- **Effect.** A slight optimism.

I ran the decisive experiment both sides asked for: LightGBM as in the claim audit, 9 windows, 3 seeds, 2 threads. Counts were traced through unique share counts of 5,000 or more.

| Measurement | Result |
|---|---|
| Traced cells under 8 days old | 2,907 cells in all rows; 55 test rows (0.7%) |
| Mask those cells | R² 0.1553 -> 0.1549 |
| Mask those cells, whole group in the row | R² 0.1550 |
| Mask under 28 days (7,296 cells) | R² 0.1571 |
| Mask under 28 days, whole group | R² 0.1557 |
| Seed range of the full model | 0.1543-0.1563 |
| Per-row gain of both groups, source under 8 days | 0.112 (SE 0.081, n 55) |
| Per-row gain, source 8-27 days | -0.110 (SE 0.074, n 55) |
| Per-row gain, source 28 days or older | 0.045 (SE 0.019, n 818) |
| Young minus old | +0.067, SE 0.083; young above old in 6 of 9 windows |

- **Reading.** The young-source part is not distinguishable from 0. Its upper bound is about 55 × 0.07 / 8,289 in MSE, about 0.0005 R², which agrees with the masking result.

**Ruling.** The facts are now settled, so the dispute is about the remedy, and it is settled by the rules:
- LEAK-6 (Must, the earliest rule of the part) applies: "measure before acting; a slight optimism with a known cause can stay with a note". The measurement shows that is what this is.
- Dropping costs R² 0.024 (`kw_*`) and 0.014 (self-reference) and removes valid history. LEAK-7 (Should) rules it out.
- The mask is not a "fix the definition" step on the ladder:
  - it changes nothing measurable;
  - it reaches only traceable cells, so it does not remove the mechanism;
  - its pattern of missing values would be computed from other rows' labels, test rows included.
- So keeping the columns with a note is the mildest remedy that resolves the problem.

This is not an independent failure:
- What remains of LEAK-10 is "looked up after the outcome unless the data shows they did not change". The values did change, but the change carries no measurable signal.
- LEAK-34 (Must, narrows LEAK-10) makes the newsroom's own history legitimate under a temporal split. Only the maturity of the count falls outside it.
- A Must takes no exception, so the clean form is an **amendment of LEAK-10** rather than an exception.
  - Proposed wording: "a value read at a later pull stays with a note when its effect is measured small".
  - Cases: house_sales, melbourne_housing_market, african_credit_scoring_challenge, aeolus, this dataset. The precedent checker's amendment watch, item 11, covers this.

| | Best evidence |
|---|---|
| Advocate (keep with a note) | Every value comes from an earlier article, which is history the editor has; the paper's top feature is `kw_avg_avg`; dropping costs 15% and 9% of the signal. |
| Critic (mask, then keep) | 36 test rows carry a same-window test label; `known` was false as written; mechanism (ii) was unmeasured. Now measured: the mask changes R² by -0.0004. |

- **Decision needed.**
  - (a) keep with the note and adopt the LEAK-10 amendment (recommended);
  - (b) keep with the note and leave LEAK-10 unamended, which gives a Must with an unrecorded departure;
  - (c) treat it like santander and drop the columns (R² 0.155 -> 0.109 for both groups).

**2. P7, CLEAN-13 (Must as written): `data_channel` with `other`**

- **Problem.** 6,134 rows (15.5%) have no channel flag. No row has two, so the merge is lossless, but it breaks the rule's wording "exactly one flag".
- **Effect.** None on the score. It is a rule-wording question.
- **Advocate:** decide it with mortgage issue 12 to avoid churn.
- **Critic:** a pending amendment is not a rule; six flags are a free, lossless fix.
- **Ruling by rank.** Until the rule is amended, the Must stands, so the critic is right on the rule. Which comes first is the curator's call.
- **Decision needed.** Amend CLEAN-13 to "exactly one, or at most one with a reference level `other`", which keeps both datasets as they are. Or split both blocks (mortgage and this dataset) into yes/no columns. If the amendment is declined, or not decided before this dataset ships, use six flags.

**Agreed facts**

- **Task and data.**
  - A real pre-publication task: an editor estimates shares before publishing (paper abstract). Fit `approximate`.
  - 39,643 articles, 2013-01-07 to 2014-12-27.
  - Target ln(shares) at the 2015-01-08 crawl. Regression rather than the 1,400 cut, consistent with brazilian_ecommerce. A second binary folder would be a PROV-6 duplicate.
- **Split.**
  - 9 two-week windows, Sunday to Saturday, from 2014-08-24 to 12-27; test 769-1,001 rows; expanding train covering 78-97% of rows.
  - Last train date 8 days before each window.
  - Temporal is right: a random split overrates (0.188 vs 0.158).
  - Gap 0 / 1 / 3 weeks gives 0.161 / 0.158 / 0.156.
- **Drops already made, all right.**
  - `timedelta` and weekday flags: shifted 23.9%, outcome-linked, +0.0076 R².
  - LDA: +0.0001 temporal.
  - `n_non_stop_words`: a copy.
  - One failed row.
- **Label maturity.** No age deficit in labels; the 2014 decline is seasonal (LEAK-24 not triggered).
- **R² ablations (re-run).**

  | Model | R² |
  |---|---|
  | Full | 0.1553 |
  | Without `kw_*` | 0.1311 |
  | Without self-reference | 0.1414 |
  | Without both | 0.1089 |

- **Same-day keyword pool.** It touches 80% of test rows and brings no measurable gain (difference -0.008, SE 0.008).
- **Probes.** Task probes: LightGBM skill +0.158, above the dummy on all splits, no flags. Hidden groups: none. Near copies: 0.6% of test rows.
- **Agreed fixes.** The 1.59 artefact (120 rows) and `rate_negative_words` = 1 - `rate_positive_words` are real and fixable.
- **Text.** No text ships; text-derived columns add 0.004 R².

**Consistency with precedent**

- **Target, date repair, windows, `approximate` fit:** consistent with brazilian_ecommerce, PROV-13 repairs, SPLIT-10/15, and the USE-8 cases.
- **LDA drop:** departs from the LEAK-30 keep-with-note pattern (Lennart, 2026-10-19), with a stated fact: no signal, and it cannot be refitted without the texts. Reasonable; add it as a LEAK-30 Cases row once the curator accepts.
- **`kw_*`/self-reference keep vs santander (dropped, +0.003 AUC):**
  - What sets this case apart: the values come only from earlier articles, in time order (LEAK-34 history), and their measured effect is -0.0004 R² on masking.
  - santander's `has_*` encoded labels of the same fold's rows with no time order.
  - The curator confirms this in issue 1.
- **Amendment watch (precedent checker, item 11):** this is the fifth pending "later-read value kept with a note" case. If the curator accepts issue 1(a), the LEAK-10 amendment is due.
- **CLEAN-13:** treat it like mortgage. The two are AI decisions only; there is no curator precedent yet.
- **Not checked:** the 2026-10-07 review-page db (`reviews/onlinenewspopularity`). The main session should look there before the curator decides.

My experiment reuses the claim auditor's LightGBM setup.

</details>

<details><summary>Claim audit</summary>

Data: the raw CSV (sha256 checked) and the definition's frame via `dataset_io.from_definition`.
Model for the R² re-runs: LightGBM (400 trees, lr 0.03, 31 leaves, min_child 50, subsample/colsample 0.8) on the 9
shipped windows, 3 seeds, R² per window averaged; date parts = days since start, weekday, month. A second run with
LightGBM defaults checks that the deltas do not depend on those settings. Note: the definition's frame is reordered within a date
relative to the raw CSV; the first run of the raw-joined variants (+LDA, +raw date, binary, slug, diff-in-diff) was
misaligned and was redone after matching rows on all feature columns (the numbers below are the redone ones).

**Table**

| # | claim (short) | source | test | result | evidence | rule |
|---|---|---|---|---|---|---|
| 1-2 | question / use case: editor estimates shares before publishing | D task_summary | paper abstract and Sec. 2-3 | holds | "analyzes articles prior to their publication" (p.1); perturbation of day and keywords (p.6-7) | USE-1, USE-3 |
| 3 | 39,643 articles, 2013-01-07..2014-12-27 | D | count, URL dates | holds | 39,644 raw minus 1; URL range 2013-01-07..2014-12-27 | PROV |
| 4, 26 | target ln(shares at the 2015-01-08 crawl) | D | code + raw | holds | `log_shares = log(shares)`; flags = weekday(2015-01-08 - timedelta) in 100% of rows | USE-5 |
| 5, 70 | popular cut at 1,400; binary ROC AUC 0.733 (paper 0.73) | D, R | re-run binary LightGBM on the 9 windows | holds | AUC 0.7328 (seeds 0.733/0.734/0.732); paper Table 4 RF 0.73 (over its own 29 windows, not the same test sets) | EV-5 |
| 6 | "the shares of earlier Mashable articles it links to or shares keywords with" are known at prediction time | D `known` | do the values equal crawl counts, and how old is the article they come from | **refuted (in part)** | 97.3% of self_reference_max >= 10,000 (8,269 rows) equal a share count in the release (crawl counts, not counts at publication; the paper's "known before publication" is not what was stored); of 895 articles tracing to a unique count >= 50k, 153 cite an article 1-5 days older (not converged at publication, paper p.3: < 4 days) and 26 a same-day one; kw_max_max of 2,055 rows is the crawl count of an article 1-6 days older; 76 of 8,289 test rows (0.9%) hold the crawl count of a gap-week or same-window article, 36 (0.4%) that of an earlier test article of their own window (a lower bound, unique counts >= 5,000 only) | LEAK-10, USE-6 |
| 7, 42, 43 | 9 two-week windows Sun-Sat, 2014-08-24..12-27, 769-1,001 test, train 30,967-38,385 (>= 78%), 1-week gap | D | print the splits | holds | test 769..1,001; train 30,967..38,385 (78.1%); train max = window start - 8 days | SPLIT-11, SPLIT-14 |
| 8, 21, 27, 48 | date from URL; all URLs match; Mashable pages carry the URL date | D | regex on all rows; one Wayback snapshot | holds | 0 non-matching URLs; snapshot 20141231 of star-wars-the-force-awakens-character-names: `datetime="Thu, 11 Dec 2014 21:11:08"`, authors' date 2014-12-15 | PROV, EV-2 |
| 9, 28, 48 | weekday flags/timedelta follow a date 1-5 days later for 24%, all of Dec 2014 | D | flags vs both dates | holds | shift 0:30,181, 1:7,059, 2:1,464, 3:677, 4:235, 5:28 (23.9%); Dec 2014 100% shifted; flags match URL weekday in 76.1% | LEAK-10 |
| 49 | within a date, shifted articles have more shares | D decisions | ln shares minus same-URL-date mean | holds | shifted +0.032 (SE 0.009), unshifted -0.010; dates with both: +0.071; pre-Apr-2014 427 shifted +0.205 (the earlier REVIEW.md says +0.038; I get +0.032) | LEAK-10 |
| 66 | raw date columns raise R² 0.158 -> 0.166 | R | +timedelta +8 flags | holds | 0.1553 -> 0.1629 (+0.0076); with LightGBM defaults 0.1470 -> 0.1514 | LEAK-6 |
| 10, 33, 50, 51, 67 | LDA from one model over all texts; no signal (0.158 with and without) | D, R | channel x year argmax; +LDA temporal | holds | every channel has the same top topic in 2013 and 2014; +LDA 0.1553 -> 0.1554 (defaults 0.1470 -> 0.1470) | LEAK-29, LEAK-30 |
| 11-14, 24, 36, 38 | R² 0.158 full, 0.135 without kw_*, 0.143 without self_reference_* | D | independent re-run | holds | full 0.1553 (0.1573 without date parts); no kw 0.1311 (-0.024, claimed -0.023); no self 0.1414 (-0.014, claimed -0.015); both dropped 0.1089. With LightGBM defaults 0.147 / 0.121 / 0.131 (same deltas) | EV-8 |
| 12, 34 | the same-day keyword pool affects "a quarter of the articles" | D | share of shifted rows among the scored test rows | holds literally, **understates** | 6,627 of 8,289 test rows (80%) are shifted; windows 0-2 are 100% shifted | EV-8 |
| 35, 68 | same-day keyword articles bring no measurable gain (0.0245 vs 0.0172, SE 0.006) | D, R | diff-in-diff of per-row squared-error gain from kw_* on the 9 shipped windows | conclusion holds; exact numbers not reproduced (they came from 15 windows) | shifted 0.0187 (SE 0.0033, n 6,627), unshifted 0.0264 (SE 0.0076, n 1,662): diff -0.008, SE 0.008 | LEAK-6, EV-9 |
| 13, 37 | links added after publication are rare: 4 of 906 cite a 1-2 day newer article | D | redo the matching on unique counts >= 50k, permutation baseline | holds (counts differ slightly) | 167 unique counts, 895 articles, 4 newer by 1-2 days; chance (permuted owner dates) 2.8, 95th pct 7, so not separable from chance. Also 26 same-day matches (publication order within the day unknown) | LEAK-10 |
| - | gain of self-reference columns where the link is <= 3 days away | (implied by 13) | per-row gain diff-in-diff | **untested** | n = 25 test rows, gain 0.148 +- 0.139; too few to decide | EV-7 |
| 15, 39, 52 | newest articles show no share deficit; 481 from 2014-12-18 | D | weekly ln-share mean/median, count | holds | 481 rows; last weeks mean 7.37/7.53 vs 7.31-7.43 the 8 weeks before | LEAK-24 |
| 16 | year 2015, UCI, DOI, licence | D | paper text | holds (year/source); licence not evidence | EPIA 2015 paper | EV-4 |
| 17 | zip 7,476,401 bytes, sha256 dba2ae52... | D | `sha256sum`, `ls` | holds | identical | PROV |
| 18, 62, 64 | the release holds no text | D, R | CSV columns | holds | only `url` is a string | SEL-12 |
| 19 | bibtex | D | paper text header | holds (title, authors, EPIA 2015); LNCS volume/pages not checked | | - |
| 20 | UCI acquisition date 2015-01-08 anchors timedelta | D | flags vs 2015-01-08 - timedelta | holds | 100% match (the paper says data collected to 2015-01-07) | PROV |
| 22, 29 | no article has two channel flags; `other` when none | D | sum of flags | holds | 0 with two; 6,134 with none (the paper's 7th channel "viral" is not in the release, so `other` is mostly unlabelled/viral) | CLEAN |
| 23 | 58 features, UCI 332 | D | CSV | holds | 61 columns = url + timedelta + 58 + shares | - |
| 25 | prediction point before publication | D | paper | holds | abstract, p.1 | USE-3 |
| 30 | one failed article dropped | D | `n_unique_tokens > 1` | holds | 1 row (ukraine-civilian-convoy-attacked, 701, LDA 0, subjectivity 0) | CLEAN |
| 31, 55 | proxy missing values | D | value counts | holds | self_ref max 0: 7,175 rows, real min >= 1; kw_max_max 0: exactly the 79 first-day articles; kw negatives: kw_min_min 22,980 (-1), kw_avg_min 833, kw_min_avg 6 | CLEAN |
| 32 | n_non_stop_words repeats n_tokens_content > 0 | D | compare | holds | 100% equal after rounding (1.0: 38,462, 0: 1,181; the 1,042 is the dropped row) | CLEAN |
| 40 | no duplicate rows, unique URLs | D | duplicated() | holds | 0 duplicates (also 0 without url); 0 exact feature copies; 714 slugs share a stem (series such as ces-challenge-nike-fuelband-N, not copies) | LEAK-16 |
| 41 | slug TF-IDF does not help (0.152) | D | TF-IDF(1-2 gram)+SVD32 | holds | 0.1553 -> 0.1517 | SEL-12 |
| 44, 47 | 1,000 articles are 2-3 weeks of output | D | articles per week | holds | about 450/week in late 2014 (2.2 weeks), 360/week in 2013 (2.8 weeks) | SPLIT-12 |
| 45 | one-week gap keeps training labels to settled shares | D | paper p.3 | holds (paper: < 4 days not converged); note: test-row features still carry settled counts of gap-week articles (row 6) | | SPLIT-9 |
| 46 | 9 windows = the 3 x 3 an IID task of this size gets | D | the `iid_split_size` rule of the v2 splits | holds | n_train 26k < 250k -> 3 repeats x 3 folds | SPLIT-15 |
| 53, 54 | header spaces; shares 1..843,300 | D | header, min/max | holds | 60 ", " in the header; min 1, max 843,300 | - |
| 56 | no check warnings | D | README build record | holds (not re-run: `dataset check` rewrites README.md) | README: 0 errors, 0 warnings | EV-7 |
| 57 | record front matter | R | read | holds as written; the `Wrong Domain / Source Modality` marker see row 58 | | - |
| 58 | "actually might be an NLP task" / marker Wrong Domain / Source Modality | R CC, front matter | text-derived columns ablation, slug TF-IDF | **refuted** (as a statement about this data) | text-derived 19 columns add 0.004 R² (0.1515 -> 0.1553); the slug's TF-IDF lowers R² (0.1517); no text ships | SEL-12 |
| 59 | platform grows over time | R CC | articles per quarter, median shares | partly holds | articles per quarter 4,654 (2013Q1) -> 5,855 (2014Q4); median shares flat (1,300-1,600) | - |
| 60 | LDA "likely introduced leaks making the dataset unusable with random splits" | R CC | 5-fold random CV with and without LDA | **refuted** | random CV 0.1803 -> 0.1836 (+0.003); temporal +0.000: a weak transductive transform, not a leak that ruins random splits | LEAK-30, LEAK-6 |
| 61 | rejected from TabArena for text and time; not that old | R | - | untested (history / opinion) | | - |
| 63 | paper: W=10,000, L=1,000, 29 iterations, D1=1,400, balanced first training set | R | paper p.7; first 10,000 articles of the release | quote holds | release's first 10k: 57.1% >= 1,400 (52.9% > 1,400) | - |
| 65 | assessment of 2026-10-07: setup | R | as rows 7, 42 | holds | | - |
| 69 | text-derived columns add 0.003 | R | ablation | holds | +0.004 | - |
| 71 | priority 2 grades | R | - | untested (judgment) | | - |
| 72 | weak signal R² 0.16 | R | re-run | holds | 0.155-0.158 | TP-2 |
| impl. | every feature known at the prediction point | implied | rows 6, 9, 10 | refuted for kw_*/self_reference_* (crawl counts, disclosed as potential leaks); holds for the rest after the drops | | LEAK-10 |
| impl. | the split is the one the use case needs | implied | windows, gap, train side | holds | expanding train, 2-week horizon, 1-week label lag | SPLIT-1, SPLIT-9 |
| impl. | the target is the real-world target | implied | label age | holds approximately | labels are shares at one crawl (12 days to 2 years after publication); no deficit for the newest | USE-5, LEAK-24 |
| impl. | no row is a copy across the split | implied | exact copies, near copies (hidden_groups probe) | holds | 0 exact, near copies 0.6% | LEAK-16, LEAK-17 |

**Refuted, ranked (validity first, Must first)**

1. **Claim 6, `known` (P4, LEAK-10 Must).** The definition says the shares of earlier linked or keyword-sharing articles
   are known before publication; they are the crawl's counts (97.3% equal a release count), and some come from articles 1-6
   days old at publication (2,055 rows via kw_max_max; 153 of 895 traceable self-reference rows). The comments and
   fit_reason already say "use the crawl's share counts"; the `known` field does not. Measured exposure on the test
   rows is small (0.9% hold a gap-week or same-window count; the recent-link gain cannot be measured, n = 25).
   Changes: wording, not the verdict. Mildest remedy: write "their shares at the crawl of 2015-01-08" in `known`.
2. **Claim 58 / marker `Wrong Domain / Source Modality` (P2, SEL-12 Must).** The data holds no text and its text
   statistics add 0.004 R²; the slug adds nothing. Remedy: drop the marker (REVIEW issue 8); keep `NLP (Text)` if the
   curator wants the provenance note.
3. **Claim 60, CC "LDA ... unusable with random splits" (P4, LEAK-30 Should).** LDA adds +0.003 under random CV and
   nothing under the temporal split. Changes nothing (the columns are dropped); remedy: none, or a one-line note.
4. Understated (holds literally): claims 12/34 "a quarter of the articles". 80% of the scored test rows are shifted
   (windows 0-2 entirely). Remedy: say "80% of the test rows" in the curation comment.

**Untested**

- Gain of self-reference columns on rows that link to an article <= 3 days away: 25 test rows, not enough to decide (EV-7).
- Claim 35's exact figures (0.0245 / 0.0172, from 15 windows): the conclusion holds on the 9 shipped windows, not the numbers.
- Claim 56: `dataset check` not re-run (it rewrites README.md); README's record shows 0 warnings.
- Claim 19 LNCS volume and pages; claims 61, 71 (history and judgment); licence (never evidence, EV-4).

</details>

<details><summary>Column audit</summary>

Frame: `dataset_io.load(..., built=False)` (origin `rebuilt`), 39,643 rows x 41 columns (39 features, target, time
column). Prediction point: before publication (first `curation_comments` bullet). Codebook: UCI
`OnlineNewsPopularity.names`; paper Fernandes et al. 2015. Test windows 2014-08-24 to 2014-12-27 (8,289 rows).

**Column table**

| column | meaning (codebook) | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| publication_date | date in the URL (time column) | yes, the planned date | datetime; 720 dates | fine. It also fixes exposure to the crawl (12-731 days; test 12-137); monthly median log shares 7.31-7.38 in early 2014, 7.17 Sep-Dec 2014: a trend or a deficit, for the split auditor | USE-5, LEAK-24 |
| data_channel | channel from six flags; `other` = no flag | yes | category, 7 levels, `other` 6,134 (15.5%); no row has two flags (the code raises) | question: lossless, but departs from CLEAN-13's literal "exactly one flag" (amendment pending, mortgage review) | CLEAN-12, CLEAN-13 |
| n_tokens_title | words in title | yes | float64 2-23 | fine | |
| n_tokens_content | words in body | yes (page at crawl) | float64; 1,181 zeros kept (real empty bodies) | fine | |
| n_unique_tokens | rate of unique words | yes | NaN for empty bodies; failure row dropped | fine | CLEAN-11 |
| n_non_stop_unique_tokens | rate of unique non-stop words | yes | NaN for empty bodies | fine | |
| average_token_length | mean word length | yes | NaN for empty bodies (was 0) | fine | CLEAN-10 |
| num_hrefs | links | yes, but read from the page at the crawl | 0-304 | question: same mechanism as the self-reference links (edits after publication); not measurable without publication-time HTML | LEAK-2, LEAK-10 |
| num_self_hrefs | links to Mashable articles | as num_hrefs | 0-116 | question, as num_hrefs | LEAK-2 |
| num_imgs, num_videos | images, videos | as num_hrefs | counts | question, as num_hrefs (weak) | LEAK-2 |
| num_keywords | keywords in metadata | yes | 1-10 | fine | |
| kw_min_min | worst keyword, min shares of earlier articles | partly (crawl counts) | -1 -> NaN (23,058, 58%). -1 is 0% of rows to 2013Q3, 35.5% in 2013Q4, 99.8-100% from 2014Q1: a pool article with share count -1 entered then; NaN in 100% of test rows | fine (masking right); an era indicator, no test signal | CLEAN-10, CLEAN-11 |
| kw_max_min | worst keyword, max shares | partly | 0 kept (740); **1.59 in 111 rows** (a non-integer share count, parse artefact) not masked | cleaning problem | CLEAN-11 |
| kw_avg_min | worst keyword, avg shares | partly | negatives -> NaN (912); 69 positive values below 4 still carry the -1 or 1.59 | kept with note (cannot be repaired) | CLEAN-11 |
| kw_min_max | best keyword, min shares | partly | 0 kept (17,102; "a keyword with no earlier article", 61% in 2013Q1 to 36% in 2014Q4): a meaningful code | fine | CLEAN-10 |
| kw_max_max | best keyword, max shares | partly | 0 (first day, 79) -> NaN; 843,300 in 8,285 of 8,289 test rows (a 2013 article) | fine; near-constant in test | |
| kw_avg_max, kw_min_avg, kw_max_avg, kw_avg_avg | keyword share aggregates | partly | first day NaN; kw_min_avg also 6 negatives NaN | potential leak kept on purpose (see problem 1) | LEAK-10 (weak), LEAK-7 |
| self_reference_min_shares / _max_shares / _avg_sharess | shares of linked Mashable articles | partly (links and counts at crawl) | max==0 -> NaN (7,174; 1,825 of them have self links that resolve to no count); **1.59 in 10 / 3 / 3 rows** not masked | potential leak kept on purpose; cleaning problem for 1.59 | LEAK-10, CLEAN-11 |
| global_subjectivity, global_sentiment_polarity | text subjectivity, polarity | yes | NaN for empty bodies | fine | |
| global_rate_positive_words, global_rate_negative_words | rate of positive/negative words | yes | NaN for empty bodies; 0 kept | fine | |
| rate_positive_words | positive among polar words | yes | NaN when no polar words (1,185) | fine | |
| rate_negative_words | negative among polar words | yes | **= 1 - rate_positive_words in 100% of defined rows** | cleaning problem: a copy | CLEAN-5 |
| avg/min/max_positive_polarity | polarity of positive words | yes | NaN without positive words (1,216) | fine | CLEAN-10 |
| avg/min/max_negative_polarity | polarity of negative words | yes | NaN without negative words (2,549) | fine | CLEAN-10 |
| title_subjectivity, title_sentiment_polarity | title sentiment | yes | 0 kept (pattern lexicon gives 0 for neutral titles) | fine | |
| abs_title_subjectivity | "absolute subjectivity level" | yes | = abs(0.5 - title_subjectivity) in 100% of rows | fine (source's per-row feature, lossy, not a copy) | CLEAN-5, CLEAN-22 |
| abs_title_sentiment_polarity | "absolute polarity level" | yes | = abs(title_sentiment_polarity) in 100% | fine, as above | CLEAN-22 |
| log_shares (target) | ln(shares at crawl) | outcome | 0-13.65; counts of 1,000 or more are rounded to hundreds (99.99%), below 1,000 exact | fine; precision worth a sentence in the notes | CLEAN-16 |
| dropped: url, timedelta, weekday flags, is_weekend, LDA_00-04, n_non_stop_words, shares | | | | drops right (later date; transform on all texts; copy; target) | LEAK-10, LEAK-30, CLEAN-5 |

**Problems, by rank**

1. **P4, LEAK-10 (weak; kept with note), keyword and self-reference statistics.** They use the crawl's share counts,
   and the one-week gap that protects the training labels does not protect them. Traced through share counts of 50,000
   or more held by one article: in the test windows, 9 rows of `kw_min_max` and 22 of 132 matched rows of
   `self_reference_max_shares` hold the count of an article 0-7 days older. Across all rows, 51 self-reference matches
   point to a newer article (some are other pages with the same count). `kw_max_max` holds a 2013 article in 8,285 of
   8,289 test rows. The leak is small and the existing note is right. Remedy: keep, and add to the note that the
   counts of the week before also come from the crawl.
2. **P4, LEAK-2 sweep (question).** `num_hrefs`, `num_self_hrefs`, `num_imgs`, `num_videos` and the text statistics
   are read from the page at the crawl, the same mechanism as the self-reference links. Most likely stable, but there
   is no test for it. Remedy: say it in the self-reference bullet.
3. **P7, CLEAN-11 (Should), the 1.59 share count.** A non-integer count sits in `kw_max_min` (111 rows),
   `self_reference_min_shares` (10), `_max_shares` and `_avg_sharess` (3), 120 rows in all. The notes say "impossible
   share counts" are set to missing, but `_clean` does not do it, so the notes and the code disagree. Remedy: mask
   `== 1.59` in the min/max columns, and the averages where their min/max is 1.59. Otherwise reword the bullet.
4. **P7, CLEAN-5 (Should), `rate_negative_words` = 1 - `rate_positive_words`** in every defined row: a copy, like the
   dropped `n_non_stop_words`. Remedy: drop it.
5. **P7, CLEAN-13 (question), `data_channel` = `other`** for 6,134 rows. Flags never co-occur, so the category loses
   nothing, but it departs from the rule's literal wording. Remedy: the pending amendment, or a one-line exception.
6. Notes only: `kw_min_min` is NaN in every test row and `kw_max_max` is near-constant there (era indicators, no
   action: CLEAN-22). The target is rounded to hundreds above 1,000. The declining 2014 target level goes to the
   split auditor (LEAK-24).

</details>

<details><summary>Split audit</summary>

Data loaded with `dataset_io.load(..., built=False)` (rebuilt from the definition; 39,643 rows, 41 columns). LightGBM
(400 trees, lr 0.03, 2 seeds) on the 9 shipped windows unless stated.

**Verdict: right with notes**

**Regime (SPLIT-1 to SPLIT-4, SPLIT-13, USE-10)**

Temporal is right. The prediction point is before publication; every article is a new row (no author or story id in
the release), so there is no recurring entity to hold out; `data_channel` is known for every new article (a feature,
SPLIT-4). Hidden-group probe: no entity-like column, no composite key, near copies 0.3% of rows / 0.6% of test rows
seen in train. The alternative IID split overrates: random 900 test rows from the same Aug-Dec 2014 period, trained on
all other rows, R^2 0.188 (0.181 without the day index) against 0.158 (0.153) for the shipped windows; a random 9-fold
over all rows 0.184 (0.172). A random split would reward same-period neighbours (SPLIT-1, Patterns "the same data, two
applications").

**Windows (SPLIT-11, SPLIT-12, SPLIT-14, SPLIT-15, SPLIT-17)**

Measured on all 9 splits: test windows Sunday-Saturday 2014-08-24 ... 2014-12-27, 769 to 1,001 rows; expanding train
from 2013-01-07, 30,967 to 38,385 rows (78.1% to 96.8%); last train date 8 days before the first test date in every
split; no index overlap. Matches `splits_comment`. Two-week windows match the paper's L = 1,000 predictions per
iteration. Per-window R^2 0.099 to 0.206, no empty or degenerate window.

**Gap and late labels (SPLIT-9, SPLIT-10, LEAK-22 to LEAK-26)**

The target is shares at the single crawl of 2015-01-08 (article ages 12 to 731 days). A model refit at a window's
start would have seen each training article's shares as of that date, not as of the crawl, so every training label
is, strictly, from after the prediction point; one crawl cannot undo that. Measured whether it matters:

* No exposure effect: monthly channel-adjusted mean log shares move between -0.26 and +0.19 with a season (summer dip
  in both 2013 and 2014, high in spring), not with age; 2013 articles (1-2 years of exposure) are not above 2014 ones.
  In the last 20 weeks the newest bucket (age 12-20 days) is +0.06, ages 20-34 days -0.13 / -0.10, older -0.07 to
  +0.03: no monotone deficit. Shares settle within days, as the paper says.
* Gap alternatives (with day index / without): no gap 0.161 / 0.155, one week (shipped) 0.158 / 0.153, three weeks
  (the paper's discard rule) 0.156 / 0.150. The gap choice moves R^2 by at most 0.005; one week is a reasonable
  reading of "some articles younger than 4 days had not settled".

**Training history (SPLIT-19, SPLIT-20)**

No break in collection: weekly counts 199 to 515 (lowest in the Christmas weeks), volume up about 18% from 2014Q2;
channel mix drifts (world 13% -> 33%, tech 21% -> 13%). Train covers a full year before the first test window, so the
test season (late August to December, holiday week included in the newest window) is in training a year earlier. The
paper's rolling train window of W = 10,000 articles: R^2 0.146 / 0.148 against 0.158 / 0.153 expanding; training on
2014 only: 0.155 / 0.154. Expanding train (SPLIT-11) is not worse and keeps a full season.

**Problems, ranked**

1. **P4, SPLIT-10 / LEAK-22 (note).** Training labels are crawl-time counts, not counts at each refit date; the
   one-week gap is nominal for the labels. Evidence above shows no measurable effect (no age deficit; gap 0 / 1 / 3
   weeks: 0.161 / 0.158 / 0.156). Remedy: none to the split; one sentence in `splits_comment` that labels are
   crawl-time counts for train and test alike and the gap simulates the settling time only.
2. **P4, LEAK-10 (note, belongs to the leak audit).** The gap protects the training labels, not the features: the
   `kw_*` and self-reference columns of a test article use crawl-time shares of articles published in the days just
   before it (inside the gap week), which a deployed model would see immature. Already kept on purpose with a note
   (REVIEW issues 5, 6); no split remedy.
3. **P4, SPLIT-19 (note).** Departs from the paper's sliding W = 10,000 train window in favour of an expanding window
   (SPLIT-11); measured 0.146 sliding vs 0.158 expanding. Remedy: say it in `splits_comment` (the paper's W and why
   expanding).

No problem with the regime, the windows' sizes or hidden groups.

</details>

<details><summary>Domain practitioner</summary>

Actor: an editor / social-media lead at Mashable in late 2014, deciding before an article goes out whether to rework
it (headline, keywords, images, links) and on which day to run it; and, in the newsroom as it really worked, which
stories to push hardest on social channels (USE-1).

**Fit: approximate (agrees with the definition, USE-8)**

One sentence: the row, the actor and the expanding two-weekly split mirror a pre-publication popularity estimate, but
the label is shares at one crawl date with no stated horizon and two input groups use the crawl's share counts (kept
potential leaks), which are the two USE-8 "approximate" patterns. USE-9 does not lift it to direct: no other real use
case is mirrored better (any post-publication use would have early share counts, which the release lacks).

**1. Inputs at the prediction point (USE-3, USE-6)**

Have, at the moment of decision:
- Text and page statistics (word counts, title length, links, images, videos, sentiment, keywords count): yes, I wrote them.
- Channel: yes. Planned publication date and so the weekday: yes (now only through `publication_date`; the default
  encoders derive the weekday, README issue 2).
- Keyword statistics (`kw_*`) and self-reference shares: I have the shares of earlier articles *as of now*. The
  dataset gives the 2015-01-08 crawl counts, so articles of the last days look more settled than they would to me,
  and for the 24% shifted rows the pool contains same-day later articles (README issues 5, 6). Measured gain from
  the same-day part is not distinguishable from 0; the crawl-count optimism is unmeasured but probably small because
  the newest weeks show no share deficit. Correctly flagged as kept potential leaks (LEAK-10 via USE-3, USE-12).

Would NOT have but the data has: nothing serious left after dropping `timedelta`, weekday flags and LDA.

Missing, that I would always have (ranked by expected signal):
1. Author / byline and that author's track record (a known-entity history, USE-10): in practice the strongest prior
   an editor uses. Not in the release.
2. Headline text and hook (only its length is here; slug TF-IDF added nothing, README issue 7).
3. Publication hour (time of day matters for social sharing; only the date survives).
4. Planned promotion (homepage slot, social push), which the newsroom itself decides and which drives shares.
5. Topic / news-cycle context (breaking event, trending story) beyond channel.

**2. Target (USE-5)**

What I act on: "will this be one of today's big stories?", a rank or probability of landing in the top few percent,
at a horizon of a few days (news shares settle in days; Szabo and Huberman). The dataset gives ln(shares) at a single
crawl, 12 days to 2 years after publication. Log shares is a reasonable proxy and keeps the order I care about; the
source's 1,400 cut (about the median) is a worse match than the regression, since "above median" is not a decision
anyone takes. Regression on log shares is the better of the two framings; a top-decile class would match the
promotion decision more closely but is not the source's task.

**3. Row and test data (USE-10, USE-11)**

One row = one article = one decision: matches. Every article is new (cold start for the article), but the newsroom
is a known entity whose recent articles feed the `kw_*`/self-reference features, which is the right structure. Test
= the next two weeks of articles after a refit, with a one-week label-settling gap: this is what I would face.
Nine windows Aug-Dec 2014 is fine; December holiday traffic is in the last window, which is realistic.

**4. Would I use it?**

As a pre-publication score: only as a weak prior. R^2 about 0.14-0.16 (LightGBM skill 0.158 over the dummy, linear
0.120, `data_channel` alone 0.083): most of what it learns is channel and keyword popularity, things an editor already
knows. Mashable's own tool (Velocity) predicted from social signals in the first minutes/hours after publication, which
is where real accuracy comes from (Szabo and Huberman: two hours of Digg data gave the 30-day forecast). I would trust
it more with author history and publish hour; I would distrust any "change the title length to gain shares"
suggestion from it (the source's optimisation step), since these features are correlates, not levers.

For a benchmark this is fine: a real, documented decision, an honest temporal split, low but stable signal (beats the
dummy on 100% of splits). Low signal is not a USE rule failure.

**Gaps ranked by how much they change the task**

1. No author / headline / hour (inputs always known, missing from the release): caps the achievable accuracy; the
   task is "popularity from page statistics", narrower than the real decision. Cannot be fixed without a scrape.
2. Label at one crawl, no fixed horizon (USE-5, USE-8 approximate): ages vary 12 days to 2 years; mitigated by
   settled shares in the newest weeks.
3. `kw_*` and self-reference statistics use crawl-time counts (kept potential leaks, USE-8, USE-12): small, measured
   (R^2 0.158 vs 0.135 / 0.143 without; no measurable same-day gain).
4. Real-world prediction is mostly post-publication with early shares (Velocity); the pre-publication version is the
   source's framing and real but secondary.
5. Target granularity: a top-k / viral probability would match the promotion decision better than log shares or the
   1,400 cut.

**What an expert would change**

- Keep the regression on ln(shares); do not ship the 1,400 binary as the main task. If a classification variant is
  ever made, cut at a high quantile per training window (viral), not the median.
- Keep the drops (`timedelta`, weekday flags, LDA) and the one-week gap.
- Word the `task_summary.fit_reason` to name the horizon gap first (label at one crawl) and add that author, headline
  and hour are not in the release, so a reader knows the ceiling is a data limit, not a modelling one.
- Optional: an ablation without `kw_*` and self-reference columns is a cleaner "strictly pre-publication" variant;
  not needed given the measurements.

**Sources**

- D: the definition; R: the curation record; the earlier REVIEW.md, the panel's claim list and the task probes;
  OnlineNewsPopularity.names (UCI).
- Fernandes, Vinagre, Cortez 2015, EPIA, doi 10.1007/978-3-319-23485-4_53 (as quoted in the record and README).
- Mashable Velocity: https://www.journalism.co.uk/inside-velocity-how-mashable-s-predictive-social-analytics-tool-fits-in-the-newsroom/ ;
  https://www.thedrum.com/news/2014/08/11/mashable-cro-seth-rogin-unveils-branded-content-road-map-calls-ban-term-native ;
  https://mrmagazine.me/2014/06/20/robyn-peterson-reveals-the-secret-sauce-that-makes-mashable-thrive-and-survive-the-mr-magazine-interview/
- Szabo and Huberman, Predicting the popularity of online content: https://arxiv.org/abs/0811.0405
- Rules: use_case.md (USE-1, USE-3, USE-5, USE-6, USE-8, USE-9, USE-10,
  USE-11, USE-12).

</details>

<details><summary>Blind review</summary>

Verdict: include with changes. It is a real, well-known pre-publication task (an editor predicts an article's shares before posting it and edits or schedules it), with weak but real signal. Two time-related issues should be fixed or documented.

**Use case**
Mashable articles from 2013-01 to 2014-12 (39,643 rows). The source paper (Fernandes et al. 2015) frames it as a decision support system that predicts popularity before publication and suggests changes. The prediction is made at publication time and is used to choose content and timing. That is a real use.

**Concerns, most serious first**
1. **Target horizon is not constant.** Shares were all counted once, when the data was collected (about January 2015). An article from 2013 has had about 2 years to collect shares; one from late December 2014 has had about 8 days (UCI: "timedelta ... days between the article publication and the dataset acquisition", and articles younger than 8 days were removed). With a temporal split, the test windows hold the articles with the shortest windows. Monthly mean log_shares falls from 7.64 (2014-03) to 7.36 (2014-12). Change: put days-since-publication (or the original `timedelta`) back as a feature, or drop the last ~1-2 months, or document it.
2. **Share-based features use share counts from the future.** The kw_* (shares of earlier articles with the same keyword) and self_reference_* (shares of linked Mashable articles) features look only at earlier articles; I checked this: kw_max_max rises over time and reaches 843,300 only after the 2013-07-03 article that has 843,300 shares. But they use share counts measured in 2015, not counts known at publication time. This is a mild look-ahead, and the paper's own design has it. These features add about 5 points of R2 (LightGBM, last 20% of rows in time: R2 0.139 with all features, 0.091 without kw/self_ref). Keep them, but document the issue; a strict variant could drop them.
3. **Signal is low.** Test R2 is about 0.14 (RMSE 0.84 on a target with std 0.93). The data is not trivial, but noise dominates, and a benchmark built on it separates methods poorly. The size (about 40k rows) is good.
4. **Preparation (mostly fine).** No exact duplicates, not even on features only. The target is log(shares); only 1 row is 0. The -1 sentinels are now NaN; kw_min_min is 58% missing, and for 1,181 rows with n_tokens_content = 0 the text features are NaN. The LDA topics (fitted on the whole corpus) and the weekday dummies were removed. The date is kept at day resolution, so the model can rebuild day of week. data_channel is 7 categories, including "other". rate_positive_words + rate_negative_words = 1, and the abs_title_* columns are derived from title_*. These are redundant columns, but harmless.
5. **Related datasets.** OpenML 46652 and 46662 hold copies of this data. Make sure only one version enters the benchmark.

**Could not check**
- The exact date each share count was collected for each article.
- Whether the URL (dropped here) would reveal titles that are copies of each other.
- Exactly how the paper computed the keyword statistics.
- The exact 9-window split boundaries.

</details>

<details><summary>Precedent check</summary>

Inputs: the decision register of 2026-10-20 (808 decisions, 4 flags), the earlier REVIEW.md, the verification
checklist, `dataset.py`, the record, the Cases tables of leak_checks.md, splits.md, use_case.md, cleaning_features.md,
provenance.md, sibling records (grep over `curation/records/` for popularity / engagement / shares / crawl).

No curator decision exists yet on this dataset's issues: the record holds Lennart's old CC (screening: "add it as a good
temporal dataset", LDA suspected) and two AI assessments; the folder came from the 2026-10-07 run (committed
2026-10-14) and REVIEW.md is unchanged since. I could not read the 2026-10-07 review page's db (no artifact tool here):
the main session should check `reviews/onlinenewspopularity` there before the curator decides.

None of the register's 4 flags (few_minority, one_feature, scaling drift, trivial) involves this dataset. Flag 3 (scaling
over all rows: exclude up to 2026-10-16, keep from 2026-10-19) touches decision 3 below; it does not change the reading.

**Summary**

| # | Decision (current definition / open issue) | Verdict | Closest precedents |
|---|---|---|---|
| 1 | Target: regression on ln(shares) (issue 1) | consistent | brazilian_ecommerce (Lennart, 2026-10-15); USE-5 |
| 1b | Alternative: a second folder `onlinenewspopularity_clf` | not reasonable under the ranking as written (PROV-6, Must) | spotify_popularity (`No`, `Duplicate`); arsenic_male_lung; amex_iid / amex_non_iid (PROV-7) |
| 2 | `timedelta` and weekday flags dropped, date from the URL (issue 2) | consistent | PROV-13 repairs (ashrae units, coad); aeolus (contrast) |
| 3 | LDA columns dropped (issue 3) | departs from the keep-with-note pattern, with a stated reason | LEAK-30 cases (Lennart, 2026-10-19): bioresponse, taiwanese, home_credit building columns kept |
| 4 | 9 x 2 weeks, one-week gap (issue 4) | consistent | brazilian_ecommerce, sf_permit_time, house_sales (SPLIT-10); SPLIT-15 |
| 5 | Newest articles kept, unlike the paper's 3-week discard | departs from the source's cohort, with a stated (measured) reason | sf_permit_time, consumer_complaints (LEAK-24) |
| 6 | Crawl-date target (12-731 days exposure), `fit="approximate"` | consistent | alfa_battle_2_0_task_2, account_debt_south_africa (USE-8); cirrhosis (LEAK-23, contrast) |
| 7 | `kw_*` kept as a potential leak (issue 5) | departs without a reason for part of the mechanism | santander (dropped, Lennart 2026-09-30); house_sales, melbourne, african_credit (kept, AI, pending) |
| 8 | Self-reference statistics kept (issue 6) | follows the LEAK-10 "did not change" branch for the links; no measurement for the values | house_sales, melbourne_housing_market |
| 9 | `data_channel` with `other` (CLEAN-13) | departs from a Must's wording; same reading as mortgage; amendment pending | mortgage REVIEW.md issue 12 (2026-10-20); caracas_cervical_cancer (Lennart, 2026-10-15) |
| 10 | Markers `NLP (Text)` / `Wrong Domain` (issues 7, 8); scope against siblings | consistent either way; record call for the curator | cardiotocography, electric_motor_temperature_prediction (Yes with the marker); internet_advertisements; sibling engagement records |
| 11 | Possible third exception: values read after the prediction point, kept with a note | amendment candidate, not yet due | house_sales, melbourne, african_credit, aeolus, this dataset |

**1. Target: regression on ln(shares)**

* Precedent: brazilian_ecommerce, `CC (2026-10-15, Lennart)`: the continuous delivery time ships, "a late-delivery flag
  would be a variant of it". forest_fires ships `log1p(area)` (Lennart, 2026-10-06). The same choice here: the count,
  log-scaled, with the paper's cut named in `predicted`.
* USE-5 (Must, "at the resolution they act on it") could argue for the binary: the paper's DSS optimises the
  probability of "popular". The fact that sets the threshold apart from an actor's threshold is in the record's own CC
  quote: D1 = 1,400 was chosen because it "resulted in a balanced popular/unpopular class distribution in the first
  training set", a statistical cut, not an editor's decision rule. That supports the regression under USE-5 as in
  brazilian_ecommerce.
* Verdict: consistent.

**1b. The alternative "binary target in a second folder `onlinenewspopularity_clf`"**

* PROV-6 (Must) names "a swapped target" among the cuts that are duplicates when they add no distinct task; a
  threshold at 1,400 of the same count on the same rows and windows is the same task at a lower resolution.
  spotify_popularity is `No` with `Duplicate` ("Duplicate of spotify tracks dataset with different target column",
  Lennart). PROV-7's exception needs a distinct task (parkinsons detection vs progression; amex IID vs grouped regime).
* Verdict: not reasonable under the ranking as written. Choosing the binary *instead of* the regression in this folder
  is fine; shipping both needs a distinct task named, or a PROV-6 amendment.

**Consistency check (AI, 2026-10-20):** a second folder with the 1,400 cut (issue 1's alternative) would ship the same
rows and windows with a swapped target, which PROV-6 (Must) calls a duplicate, as for spotify_popularity (`No`,
`Duplicate`). What sets the binary task apart? (a) the paper's published task is the binary one, so it is the source's
own benchmark task and the regression is ours: ship the binary only, in this folder (no duplicate); (b) keep only the
regression, as recommended; (c) reopen spotify_popularity if a target swap is to count as a distinct task; (d) amend
PROV-6 to allow a source-defined binary companion.

**2. `timedelta` and the weekday flags dropped, the date from the URL**

* Repair from the origin before cleaning around damage (PROV-13; Tensions row "Repair against cleaning around damage":
  coad, corporate_credit_rating, SUPPORT2, ashrae units). The URL date is the origin's date (Mashable's archived pages);
  the weekday stays derivable from `publication_date`.
* Contrast, aeolus (AI, 2026-10-12, kept with a note): the release's weather join is misaligned too, but only 1.94% of
  flights read weather after departure, costing 0.0003-0.0004 ROC AUC. Here 24% of rows carry the later date, it goes
  with the outcome (+0.038 vs -0.010 log shares within a URL date) and adds R^2 0.008. The size and the available
  repair set the cases apart; both decisions follow LEAK-6 (measure, then act).
* Verdict: consistent. The alternative (keep the published flags) would depart from LEAK-10 (Must) for a measured
  outcome-linked later date.

**3. LDA columns dropped**

* LEAK-30 (Should when weak): rebuild when the source has the raw values, "otherwise keep the dataset with a note".
  Lennart's cases of 2026-10-19 keep all-row transforms with a `Potential leak, kept on purpose:` note (bioresponse,
  taiwanese_bankruptcy_prediction, credit_card_customers, cooking_time_1m, delivery_eta_1m, maps_router_eta_1m,
  lung_cancer_epithelial_genexp, home_credit_default_risk's 43 building columns). Closest pair: home_credit's building
  columns, a column block (not the whole feature space) kept with a note.
* The departure has its fact in the README and REVIEW.md: the five LDA columns carry no measurable signal (R^2 0.1580
  with, 0.1582 without, 3 seeds; leak probe -0.004 to +0.002) and cannot be refitted per window (no texts). Dropping is
  "fix the definition", which the remedy ladder ranks above "keep with a note", and the Tensions row says "fix it when we
  can". Lennart's screening CC already suspected the LDA leak.
* Not drift: Lennart's 2026-10-19 change was from exclude to keep for whole datasets; dropping a zero-signal block
  excludes nothing.
* Verdict: departs from the keep-with-note pattern with a stated reason; reasonable. When the curator accepts, the
  LEAK-30 Cases row can name it as a drop ("no signal, cannot be rebuilt").

**4. Windows and gap**

* SPLIT-10: a gap of about the label's delay: brazilian_ecommerce one month (Lennart, 2026-10-15), sf_permit_time six
  months, house_sales one week (AI panel, 2026-10-20). Here one week, after the paper's "younger than 4 days had not
  settled". The CHANGELOG entry of the gap rendering lists onlinenewspopularity with the other stated gaps.
* SPLIT-15: as many windows as an IID task of that size gets folds (9 = 3 x 3), as stated in `splits_comment`.
* Verdict: consistent.

**5. Newest articles kept (the paper discarded those under three weeks)**

* LEAK-24 (Must): a target right-censored in the newest periods is cut where follow-up is complete (sf_permit_time:
  permits after 2024 cut; consumer_complaints re-sourced). The rule applies only when censoring is present; the
  definition states the measured reason it is not (the 481 articles from 2014-12-18: median 1,600, 65% at 1,400 or more,
  against 1,100-1,400 and 42-52% in the 8 weeks before). LEAK-22 (follow the paper's cohort) is about rows that cannot
  have the outcome and does not apply.
* The evidence is weaker than in the precedents: one crawl, so no two-download comparison (probe 13), and the checklist
  notes the per-window check against the training years was not re-run.
* Verdict: departs from the source's practice with a stated, measured reason; consistent with LEAK-24 as long as the
  "no deficit" claim holds per window (the claim auditor's re-run settles it).

**6. The crawl-date target and `fit="approximate"`**

* USE-8 cases: alfa_battle_2_0_task_2 "approximate: a reconstructed time axis or a label without a stated horizon",
  account_debt_south_africa "approximate: one snapshot stands in for a forecast". A cumulative count at one crawl with
  12-731 days of exposure is the same kind of gap, named in `fit_reason`.
* Contrast: cirrhosis (LEAK-23) re-targeted to a fixed horizon, which needs per-row follow-up; one crawl date gives none.
* Verdict: consistent.

**7. Keyword statistics kept as a potential leak**

What the kept columns hold, by mechanism:

* (i) same-day articles published later (shifted 24%): measured, diff-in-diff 0.007 (SE 0.006), no measurable gain;
* (ii) the earlier articles' share counts as of the 2015 crawl, not as of publication: true by construction, not
  measured;
* (iii) new, measured for this check (the raw CSV, the 9 test windows): of the 735 test rows whose
  `kw_min_max` equals a share count >= 10,000 held by exactly one article, 11 take it from an article earlier in the
  same test window (a test row's label, at its crawl value), 724 from before the window, 0 from the same day or later.
  (`kw_max_max` matches before the window in all 8,289 test rows: it is the global maximum.) So test labels enter other
  test rows' features, rarely.

Precedents:

* Dropped: santander `has_one`/`has_zero` (Lennart, 2026-09-30): features encoding the labels of other rows in the test
  fold, +0.003 AUC, dropped under LEAK-6 ("a confirmed leak goes even when small") and LEAK-28. Mechanism (iii) is the
  same kind, at a far smaller rate and through history only. online_shoppers `PageValues` (Lennart, 2026-10-01): an
  aggregate of share-like values kept only where it behaves like history (Feb-May dropped).
* Kept with a note: house_sales July-2015 values (AI panel 2026-10-20, masking measured: RMSE 0.2147 vs 0.2132);
  melbourne_housing_market looked-up attributes (provisional, pending the curator; checked against the sheet);
  african_credit_scoring_challenge values at the data pull (AI, 2026-10-07); kick `WheelType` and homesite (curator
  accepted, under LEAK-38, which covers anonymised fields of a company's own competition and does not reach this
  dataset). LEAK-34 (own history under a temporal split is legitimate) covers history, not its later-measured values.
* Each kept precedent measured the part it kept. Here (i) is measured; (ii) and (iii) are not, so LEAK-6's "slight
  optimism with a known cause" is asserted, not shown, for them.

Verdict: departs without a stated reason for mechanisms (ii) and (iii); the reason given covers (i) only.

**Consistency check (AI, 2026-10-20):** your call on onlinenewspopularity's `kw_*` (keep, a LEAK-10/LEAK-6 departure)
differs from santander_customer_transaction_prediction (dropped 2026-09-30: features that encode other test-fold rows'
labels, +0.003 AUC); here 11 of 735 traceable test rows take a test article's crawl-time shares. What sets it apart?
(a) the keyword statistics only look back in time, like a history a deployed system has in an as-of version, and the
paper's most important feature (`kw_avg_avg`) is part of the task; recorded as an exception to LEAK-10 once mechanism
(ii) is measured (e.g. the keyword gain for test articles whose pool is mostly older than 4 weeks against younger
pools); (b) treat it like santander: drop the nine `kw_*` (R^2 0.158 -> 0.135); (c) reopen santander's drop; (d) amend
LEAK-10 for history aggregates measured at a later date.

**8. Self-reference statistics kept**

* LEAK-10 Mechanisms row "attributes looked up after the outcome: drop them, or keep them where the data shows they did
  not change" (house_sales; melbourne_housing_market kept provisionally, `Bedroom2` = `Rooms` in 98-100%). The links:
  4 of 906 traceable cases point to a newer article, so the data shows they rarely changed: follows the keep branch.
* The values are the linked articles' crawl-time shares (mechanism (ii) of decision 7), which changed by construction
  and are not measured; house_sales measured the masking effect of its changed rows.
* Verdict: consistent for the links; the value part shares decision 7's gap (one measurement settles both).

**Consistency check (AI, 2026-10-20):** your call on the self-reference statistics (keep) follows house_sales and
melbourne for the links, but those precedents kept values the data showed unchanged, while these are share counts as of
the crawl. What sets it apart? (a) the linked articles are mostly weeks older, so their crawl counts had settled (a
measurement by the linked article's age would show it), recorded as an exception; (b) drop them (R^2 0.158 -> 0.143);
(c) revisit house_sales' July-2015 values; (d) amend LEAK-10's row to "keep when the effect is measured small".

**9. `data_channel` with `other` when no flag is set**

* CLEAN-13 (Must, Lennart 2026-10-15, caracas_cervical_cancer): "A block is one-hot only when every row has exactly one
  flag set". 6,134 rows (15.5%) have none; no row has two (the code raises). mortgage's `real_estate_type` was decided
  alike, and mortgage's REVIEW.md issue 12 (2026-10-20) holds the consistency check and proposes amending CLEAN-13 to
  cover a reference level; advocate and critic agree there.
* A Must has no exceptions: the way out is the amendment, or splitting both blocks into yes/no columns. Decide the two
  datasets together.
* A correction to mortgage's REVIEW.md: it cites onlinenewspopularity as "shipped 2026-10-14". The merge is the 2026-10-07
  run's AI decision (committed 2026-10-14) and no curator has decided it; it is a pair of AI decisions, not a curator
  precedent (principles: only a precedent "an AI recommendation a curator accepted" counts).
* Verdict: departs from the Must's wording; the amendment in mortgage issue 12 settles both. No new prompt here.

**10. Markers and scope against the sibling engagement datasets**

* `Wrong Domain / Source Modality` sits on `Yes` records elsewhere (cardiotocography, electric_motor_temperature_prediction),
  so keeping it is not inconsistent; principles "Arguing a call" (internet_advertisements) says to argue the marker
  from the feature composition: no text column, slug TF-IDF R^2 0.152 vs 0.158. Removing it is a record-field call.
* Siblings (content popularity / engagement): facebook_live_sellers_in_thailand `No` (no predictive target, scientific
  discovery); books_goodreads `No` (no target); spotify_popularity `No` (`Duplicate`); buzzinsocialmedia_twitter and
  google_play_store_apps `2nd Tier` (data quality, no target yet); facebook_comment_volume `TBD -> Yes`, not added
  (temporal split in its paper); kickstarter `Yes` (predict at launch, post-launch `profile`/`staff_pick` dropped,
  Lennart 2026-09-30). onlinenewspopularity is set apart from the `No` siblings by a source-stated actor, moment and
  decision (the paper's pre-publication DSS, USE-1 to USE-3) and follows kickstarter's pattern (prediction point at
  publication, later columns dropped). The `TabArena Reject` collection reflects the older decision (text, temporal);
  the newer curator CC (Yes) wins. Consistent.
* facebook_comment_volume is the nearest unadded sibling: when it is added, its crawl-time page features face the same
  question as decision 7.

**11. A third exception of the same kind (amendment watch)**

"A value read after the prediction point, kept with a `Potential leak, kept on purpose:` note because its measured
effect is small": house_sales (July-2015 values), melbourne_housing_market (looked-up attributes), african_credit_scoring
(values at the data pull), aeolus_1m (weather after departure), and onlinenewspopularity twice. All are AI
recommendations pending the curator, except kick and homesite, which have their own rule (LEAK-38). LEAK-10's text
allows only "unless the data shows they did not change". If the curator accepts three of these, the next pass should
propose amending LEAK-10 (or a narrowing rule beside LEAK-38): "a value read at a later pull stays with a note when its
effect is measured small", with these cases.

**Not checked**

* The review-page db of 2026-10-07 (Lennart's marks, if any, on this dataset).
* Decision 5's per-window maturity and decision 7's mechanism (ii) are not measured here; the probes that would settle
  them are named in the prompts.

</details>

<details><summary>Advocate</summary>

Position: ship the definition as it stands. The task, target, split and the three drops hold under every audit. What
the auditors found is wording (two claims) and three P7 items; none of them is a validity failure that the definition
leaves unfixed. Seven points, strongest first.

**1. A real use case, with the prediction point the source states (P3; USE-1, USE-3, USE-8 Must): holds**

* Evidence: the paper's system "analyzes articles prior to their publication" and perturbs day and keywords (claim
  audit rows 1-2, 25). The practitioner agrees on actor, row and target: "a real, documented decision, an honest
  temporal split" (fit `approximate`, which agrees with the definition, USE-8). The blind reviewer, without our notes,
  calls it "a real, well-known pre-publication task" and would include it.
* Precedent: kickstarter (predict at launch, post-launch columns dropped, Lennart 2026-09-30) is the same pattern; the
  `No` siblings (facebook_live_sellers, books_goodreads) lack an actor and a target, which this one has (precedents 10).
* Answers: "it is really an NLP task" (record CC, marker `Wrong Domain / Source Modality`). Refuted on the data: the
  19 text-derived columns add 0.004 R² and the slug's TF-IDF lowers it (0.1553 -> 0.1517); no text ships (SEL-12;
  principles "Arguing a call"). Remedy: drop the marker in the record; the definition is untouched.

**2. The split mirrors the application (P4; SPLIT-1, SPLIT-11, SPLIT-10, SPLIT-15): holds**

* Evidence (split audit, verdict "right with notes"): 9 Sunday-Saturday windows 2014-08-24..12-27, 769-1,001 test
  rows, expanding train 78-97%, train ends 8 days before each window, no overlap. No entity to group by; near copies
  0.6% of test rows. A random split over the same period overrates (R² 0.188 vs 0.158), so temporal is the honest
  regime. Gap 0 / 1 / 3 weeks: 0.161 / 0.158 / 0.156; the paper's sliding W = 10,000 is worse (0.146), so expanding
  loses nothing.
* Answers: the split auditor's three notes (crawl-time labels, gap protects labels not features, departure from W) are
  sentences for `splits_comment`, not changes; the auditor itself proposes "no remedy to the split".

**3. The leaks that were measured as leaks are already fixed in the definition (P4; LEAK-10 Must, LEAK-30)**

* `timedelta` and the 8 weekday flags follow a date 1-5 days after the URL date for 23.9% of rows (100% of December
  2014); within a URL date the shifted articles carry more shares (+0.032, SE 0.009) and the columns add R² +0.0076.
  Dropped, with the date repaired from the URL, which a Mashable page snapshot confirms (claim audit rows 8-9, 49, 66).
  This is "repair from the origin" (PROV-13), the top of the remedy ladder.
* LDA: one model over all texts, +0.0001 R² under the temporal split; dropped. The precedent checker calls the drop a
  departure from the keep-with-note pattern of LEAK-30, but with its fact stated (no signal, cannot be refitted
  without the texts), and "fix the definition" ranks above "keep with a note" on the ladder.
* Answers: the blind reviewer's suggestion to put `timedelta` back as an exposure feature. It would reintroduce the
  shifted, outcome-linked date (LEAK-10, Must, measured), so it loses by strength; the exposure concern is point 4.

**4. The crawl-date target is settled, not censored (P4; LEAK-24 Must, SPLIT-10; P3, USE-5, USE-8)**

* Evidence: split audit finds no age deficit: monthly channel-adjusted log shares follow a season (summer dip in 2013
  and 2014), 2013 articles (1-2 years of exposure) are not above 2014 ones, the newest bucket (12-20 days) is +0.06.
  Claim audit: the 481 articles from 2014-12-18 average 7.37/7.53 vs 7.31-7.43 in the 8 weeks before.
* LEAK-24 cuts the newest periods only where censoring is present; it is measured absent. The remaining gap (one crawl,
  no fixed horizon) is what `fit="approximate"` already says, as for alfa_battle_2_0_task_2 and
  account_debt_south_africa (USE-8 Cases).
* Answers: the blind reviewer's concern 1 (mean falls 7.64 in 2014-03 to 7.36 in 2014-12). That drop is the season the
  split auditor measured in both years, not exposure: the measurement on the data outranks the inference (EV-2).
* Target choice: regression on ln(shares) is consistent with brazilian_ecommerce (Lennart, 2026-10-15) and USE-5: the
  paper's 1,400 cut was picked for class balance, not an editor's rule; the practitioner prefers the regression. A
  second binary folder would be a PROV-6 duplicate (spotify_popularity), so it should not be added.

**5. The kept keyword and self-reference statistics are a slight optimism with a known cause (P4; LEAK-6 Must, USE-12 Must, LEAK-7 Should)**

* What is real (conceded): they hold crawl-time share counts (97.3% of self-reference maxima >= 10,000 equal a release
  count). The `known` field says they are known before publication; the claim auditor refutes that in part. Remedy:
  write "their shares at the crawl of 2015-01-08" in `known`, and "80% of the test rows" instead of "a quarter of the
  articles" in the keyword bullet (claim audit refuted 1 and understated 4). Wording, not the verdict.
* Why keep, by measurement (LEAK-6 lets "a slight optimism with a known cause" stay with a note): the same-day pool
  gives no measurable gain (diff-in-diff -0.008, SE 0.008, on the 9 shipped windows); 0.9% of test rows hold a
  gap-week or same-window count and 0.4% an earlier test article's count; links to newer articles are 4 of 895,
  against 2.8 expected by chance (95th percentile 7). The column auditor: "the leak is small and the existing note is
  right".
* Why they belong to the task: each value is the share count of an article published before this one, which the
  editor's own analytics show as of now (practitioner: "I have the shares of earlier articles as of now"); the paper's
  most important feature is `kw_avg_avg`. Only the maturity of the count differs, not what it measures. Dropping costs
  R² 0.024 (kw) and 0.014 (self-reference), 15% and 9% of the signal, which LEAK-7 (smallest fix that keeps a valid
  signal) and the remedy ladder (keep with a note before drop) both weigh against.
* Answers the santander precedent (LEAK-6 "a confirmed leak goes even when small"). santander's `has_*` encoded other
  test rows' labels in the same fold, with no time order. Here every value comes from an earlier article: history the
  actor has, at a younger age. That is optimism with a known cause, not a label of the row or a later row. The
  precedent checker asks for mechanism (ii) to be measured; the split audit's no-age-deficit result (point 4) is that
  measurement in aggregate (counts settle within days), and the share of exposed test rows bounds it at about 1%. If
  the curator reads mechanism (iii) (36 test rows) as confirmed, it is a curator call between keep-with-note and drop;
  it does not touch the rest of the definition.

**6. Worth benchmarking (P6; TP-2 Should, TP-3)**

* Evidence (task probes): LightGBM skill +0.158, beats the dummy on 100% of splits; LightGBM minus linear +0.038
  (paired SE 0.008); `data_channel` alone +0.083, so the model uses more than one feature; no probe flags.
* Precedent: forest_fires kept at R² 0.013 (TP-2 Cases). Low signal is no reason to retire; the blind reviewer's
  concern 3 is a weight, not a rule. 39,643 rows, 9 scorable windows.

**7. The cleaning items are real and cheap; fix them without reopening anything (P7; CLEAN-11, CLEAN-5, CLEAN-13)**

* Conceded, column audit: the 1.59 share count in 120 rows is not masked although the notes say "impossible share
  counts" are (CLEAN-11 Should; notes and code disagree): mask it, or reword. `rate_negative_words` = 1 -
  `rate_positive_words` in every defined row: drop it, as `n_non_stop_words` was (CLEAN-5 Should).
* `data_channel` with `other` (15.5% of rows, never two flags): lossless; it departs from CLEAN-13's wording, and the
  amendment pending in mortgage issue 12 settles both datasets together. A quality item cannot block a valid task
  (principles step 3; Tensions row "a real task against imperfect cleaning").
* These are independent fixes, not conflicts with points 1-6 (principles step 4): none of them changes the target, the
  split or a validity verdict.

**Judgment record (as argued)**

```text
Verdict: ship (definition as is), with wording fixes and two cheap P7 fixes.
Validity: SEL-12 holds (no text; drop the record's Wrong Domain marker); USE-1/3 hold, USE-8 approximate (stated);
  LEAK-10 triggered, fixed (timedelta, weekday flags); LEAK-30 fixed (LDA dropped); LEAK-24 not triggered (no deficit);
  LEAK-6 kw_*/self_reference_* kept with a note (measured small; `known` wording to fix); SPLIT-1/10/11 hold.
Value: TP-2, small real signal (R² 0.158, 100% of splits above the dummy).
Quality: CLEAN-11 (1.59) and CLEAN-5 (rate_negative_words) to fix; CLEAN-13 via the mortgage amendment.
For the curator: issue on kw_*/self_reference_* (keep with note vs drop; santander precedent).
```

</details>

<details><summary>Critic</summary>

Position: **ship only after changes.** The task is real (pre-publication estimate, source-stated actor and moment,
USE-1 to USE-3) and the split is right (split audit). I do not argue for exclusion. I argue that one kept leak is
shipped on half a measurement, that the definition's own text misstates what the features are, and that three
cleaning steps the notes promise or the rules require are missing.

**1. Test labels reach other test rows through `kw_*` and `self_reference_*` (P4, LEAK-10 / LEAK-6, Must)**

* Problem: these columns hold the share counts of the 2015-01-08 crawl, not the counts at publication. The definition
  keeps them as "potential leaks" on the strength of one mechanism only (same-day pool articles, diff-in-diff
  -0.008, SE 0.008). Two other mechanisms are not measured: (ii) earlier articles' counts are final rather than
  as-of, and (iii) a test article's label enters another test row's features.
* Evidence: 97.3% of `self_reference_max_shares` >= 10,000 equal a share count in the release (claim audit, row 6).
  (iii) is confirmed. 36 test rows (0.4%, a lower bound: unique counts >= 5,000 only) hold the crawl count of an
  earlier test article of their own window, and 76 (0.9%) one from the gap week or the window (claim audit). The
  precedent checker counted 11 of 735 traceable `kw_min_max` test rows. 153 of 895 traceable self-reference rows cite
  an article 1-5 days old, which the paper says had not settled (< 4 days, p. 3). The gain on rows linking to an
  article <= 3 days old is untested (n = 25, EV-7).
* Effect: a small optimism of unknown size on the very feature group that carries the signal (R² 0.158 -> 0.109
  without both groups). The size of mechanism (ii) is not shown, so LEAK-6's "slight optimism with a known cause" is
  asserted, not measured.
* Rule: LEAK-6 (Must): "a confirmed leak goes even when small"; santander `has_*` was dropped at +0.003 AUC for the
  same kind of leak (other test-fold labels inside features, Lennart 2026-09-30). LEAK-10 (Must) keeps looked-up
  values only "where the data shows they did not change"; here they changed by construction.
* Remedy (mildest first, LEAK-7): (a) fix the definition: set to missing the `kw_*` / `self_reference_*` cells whose
  value is the unique share count of an article published less than 8 days before the row (gap week, same window,
  later), then re-run R²; (b) run the measurement the precedent checker names, the keyword and self-reference gain for
  test rows whose matched source article is younger than 4 weeks against older ones. If (b) shows no gain, keep the
  columns with a curator exception to LEAK-10 that names that measurement. Drop the columns (R² 0.158 -> 0.135 /
  0.143) only if neither works.

**2. The task summary misstates the inputs and the exposure (P3/P4, USE-8 Must; writing)**

* Problem: `known` says the shares of earlier articles are "known" before publication. In fact they are the crawl
  counts (refuted, claim audit row 6). `fit_reason` says the same-day pool affects "a quarter of the articles". It
  affects 80% of the scored test rows (6,627 of 8,289), and windows 0-2 are 100% shifted. The curation comment says
  "the R^2 values below are LightGBM on our 9 windows", but the 0.0245 / 0.0172 / SE 0.006 figures come from 15 windows
  and are not reproduced on the 9 (shifted 0.0187, unshifted 0.0264).
* Effect: a reader of the fit underrates the leak exposure exactly where the score is computed.
* Rule: USE-8 (Must, the fit is written as it is); EV-8.
* Remedy: reword `known` to "their shares at the crawl of 2015-01-08". Say "80% of the test rows" in `fit_reason` and
  the keyword bullet. Replace the 15-window figures with the 9-window ones.

**3. Training labels are crawl-time counts; the gap is nominal for labels and features (P4, SPLIT-10 Should, note)**

* Problem: every label, including training labels, is the 2015-01-08 count, so a refit at a window's start "sees"
  later shares. The one-week gap does not protect the features (point 1).
* Evidence: the split audit measured no monotone age deficit and gap 0 / 1 / 3 weeks giving 0.161 / 0.158 / 0.156. The
  blind reviewer saw monthly means fall from 7.64 (2014-03) to 7.36 (2014-12). The split audit reads this as seasonal.
* Remedy: a note only. One sentence in `splits_comment` saying that labels are crawl-time counts for train and test
  alike, and that the gap simulates settling time only. Add the paper's sliding W = 10,000 window and why expanding
  is used (0.146 vs 0.158).

**4. `data_channel` with `other` breaks CLEAN-13 as written (P7, CLEAN-13 Must)**

* Evidence: 6,134 rows (15.5%) have no flag. CLEAN-13 makes a block one-hot "only when every row has exactly one flag
  set". A Must has no exceptions. The mortgage precedent is an AI decision, not a curator precedent (precedent
  checker, section 9).
* Remedy: decide it together with mortgage's pending CLEAN-13 amendment. Until then, ship the six flags as separate
  columns. That form is lossless and needs no amendment. This is a quality point and is no reason to hold the task.

**5. The notes promise a cleaning step the code does not do: the 1.59 share count (P7, CLEAN-11 Should; notes match the code)**

* Evidence: a non-integer share count of 1.59 sits in `kw_max_min` (111 rows), `self_reference_min_shares` (10),
  `_max_shares` and `_avg_sharess` (3 each). The README stats show a minimum of 1.59. The curation comment says
  "impossible share counts" are set to missing, but `_clean` does not do it (column audit, problem 3).
* Remedy: mask `== 1.59` in the min/max columns, and the averages where their min/max is 1.59. Otherwise remove the
  claim from the bullet.

**6. `rate_negative_words` is an exact copy (P7, CLEAN-5 Should)**

* Evidence: it equals 1 - `rate_positive_words` in 100% of defined rows (column audit). The definition already drops
  `n_non_stop_words` for the same reason.
* Remedy: drop it, so the treatment is consistent.

**7. Record fixes (P5 / SEL-12)**

* Evidence: the `Wrong Domain / Source Modality` marker is refuted by the data. The text-derived columns add 0.004
  R², the slug TF-IDF lowers it (0.152), and no text ships (claim audit rows 41, 58). OpenML 4545 (the same data) is
  missing from `source_links`.
* Remedy: drop the marker, add OpenML 4545, and keep `NLP (Text)` if the curator wants it.

Not raised: the target choice (regression is consistent with brazilian_ecommerce and USE-5; the 1,400 cut is
statistical). The LDA, `timedelta` and weekday drops are measured and right.

</details>

<details><summary>Advocate rebuttal</summary>

The critic and I agree on the task, the target, the split and the three drops. We also agree that this is "ship after
changes", not exclusion. I concede points 2, 3, 5, 6 and 7 in full and point 4 in part. Point 1 is the one dispute.
I agree with its facts and dispute its remedy order.

**1. `kw_*` / `self_reference_*`: the facts are conceded; the remedy is disputed**

* Conceded: mechanism (iii) is confirmed. In 36 test rows (0.4%, a lower bound) the value is the crawl count of an
  earlier article in the same window. Mechanism (ii) is not measured per row. My opening point 5 leaned on the split
  audit's no-age-deficit result, which is an aggregate over labels and not a test of these features. So LEAK-6's
  "slight optimism" is not yet shown for (ii). I withdraw "measured small" for (ii).
* Disputed: that this is "the same kind of leak" as santander. santander's `has_*` were computed over the test fold's
  rows with no time order (LEAK-28 territory). Here every value comes from an article published **before** the row.
  The editor sees that outcome at prediction time, only at a younger count. That is newsroom history carried forward,
  the case LEAK-34 (Must, narrows LEAK-10) allows. The only defect is the maturity of the count, which is mechanism
  (ii). So the deciding question is a measured one: does the immature part add gain? It is not a categorical "test
  labels in features".
* Disputed: remedy (a), masking the cells whose value matches a unique count of an article under 8 days old. It is not
  the mildest valid fix:
  - It can only find values that trace to a unique count. The claim audit traced 895 articles of 39,643 and says its
    test-row figure is a lower bound, so the leak it targets would stay in the untraced rows.
  - It makes the missingness depend on how recent the source article is. That is a new signal the deployed system
    would not have, and LEAK-10 forbids "missingness that encodes" the target side.
* What I accept: remedy (b) first. Facts come first (principles step 1, EV-1). Measure the gain of these columns for
  test rows whose matched source article is under 4 weeks old against older ones, on the 9 shipped windows.
  - No measurable gain: keep the columns with a `Potential leak, kept on purpose:` note and a curator exception to
    LEAK-10 that names this measurement (LEAK-6, LEAK-7, USE-12).
  - A gain: drop the self-reference group first (0.4% of rows traced, R² cost 0.014), then reconsider `kw_*`.
* The n = 25 limit (EV-7) applies to rows with a link at most 3 days old. A 4-week cut gives far more rows, so (b) can
  be decided.

**2. Wording of `known`, `fit_reason` and the 15-window figures: conceded**

* Fix: write "their shares at the crawl of 2015-01-08" in `known`, "80% of the test rows" in `fit_reason` and the
  keyword bullet, and the 9-window diff-in-diff (shifted 0.0187, unshifted 0.0264, difference -0.008, SE 0.008)
  instead of the 15-window figures (USE-8, EV-8). The conclusion does not change.

**3. Crawl-time labels and the gap: conceded (note only)**

* We agree on the remedy: one sentence in `splits_comment`, plus the paper's W = 10,000 sliding window and why the
  split expands (0.146 vs 0.158). The blind reviewer's 7.64 -> 7.36 drop is seasonal (split audit, both years). We
  both read it that way.

**4. `data_channel` and CLEAN-13: conceded in part**

* Conceded: a Must as written has no exception, and the mortgage pairing is two AI decisions, not a curator
  precedent.
* Disputed: splitting into six flags now. The mortgage amendment is already before the curator, and both forms are
  lossless. Converting now and possibly reverting after the amendment is churn on a quality item.
* Proposed: decide it with mortgage issue 12 in the same review, and ship whichever form the curator picks for both
  (principles: treat like cases alike). If the amendment is declined, the six flags it is.

**5. The 1.59 share count: conceded**

* Mask `== 1.59` in the min/max columns and mask the averages where their min or max is 1.59 (CLEAN-11). The notes
  then match the code.

**6. `rate_negative_words`: conceded**

* Drop it (CLEAN-5), consistent with `n_non_stop_words`.

**7. Record fixes: conceded**

* Drop `Wrong Domain / Source Modality` (SEL-12, refuted on the data) and add OpenML 4545 to `source_links`.

**Where this leaves the panel**

The agreed changes are wording (2, 3), two P7 fixes (5, 6) and the record fixes (7). CLEAN-13 (4) goes to the curator
together with mortgage. The one open point is 1. Its decisive experiment is the gain by source-article age (b).
Whatever (b) shows, the result is keep-with-exception or drop columns, never exclusion (USE-12).

</details>

<details><summary>Critic rebuttal</summary>

No new facts. The advocate's brief and mine differ on one validity point, A5 (my point 1), and on one quality point,
A7 on CLEAN-13 (my point 4). The rest is agreed.

**A1. Real use case; drop the `Wrong Domain` marker: concede**

Agreed (USE-1, USE-3, USE-8; SEL-12). This is the same as my point 7.

**A2. The split mirrors the application: concede**

Agreed (SPLIT-1, SPLIT-11, SPLIT-15). The advocate also accepts the split auditor's sentences for `splits_comment`,
which is all my point 3 asks for. Point 3 is settled as a note.

**A3. `timedelta`, the weekday flags and LDA are dropped: concede**

Agreed. Putting `timedelta` back would reintroduce a measured, outcome-linked later date (LEAK-10). I do not ask for
it.

**A4. The crawl-date target is settled, not censored; regression over binary: concede**

Agreed for the labels (LEAK-24 not triggered, by the split audit's measurement, EV-2). The target choice is agreed too
(USE-5, PROV-6). It does not carry over to the features; see A5.

**A5. `kw_*` / `self_reference_*` as "a slight optimism with a known cause": concede in part, dispute the remedy**

Conceded:

* The values come from earlier articles, in time order, unlike santander's `has_*`. The santander analogy is weaker
  than I put it.
* Mechanism (iii) (36 test rows hold an earlier same-window test article's count) is the extreme case of (ii), a
  history value read too late. It is not a label of the row itself.
* The wording fixes (`known`, "80% of the test rows") are agreed by both sides (USE-8).

Disputed, with evidence:

* "The split audit's no-age-deficit result is that measurement in aggregate." It is not. That result covers labels
  aged 12 days or more: the youngest test article is 12 days old at the crawl. The features in question come from
  articles 0-7 days old at the row's publication. In 153 of 895 traceable self-reference rows the source article is
  1-5 days old (claim audit, row 6), and 2,055 `kw_max_max` values come from articles 1-6 days old. The paper says
  shares under 4 days old had not settled (p. 3). That age range is the one no audit measured. The gain on links to
  articles <= 3 days old is untested (n = 25, EV-7).
* "The share of exposed test rows bounds it at about 1%." The 0.9% and 0.4% are lower bounds: only unique counts of
  5,000 or more could be traced (claim audit, row 6). They are not a bound.
* The remedy ladder favours my remedy. LEAK-7 (Should): "the smallest fix that keeps a valid signal beats dropping the
  column". The remedy ladder (principles step 5) ranks "fix the definition" above "keep with a note". Masking only the
  cells traced to an article under 8 days old touches about 1-2% of test cells. It keeps the 15% / 9% of signal that the
  advocate rightly wants to keep, and it removes the part LEAK-6 cannot call "known" until it is measured.
* Remedy unchanged: mask the traced cells and re-run R². Alternatively, run the measurement by source-article age.
  If it shows no gain, keep with a curator exception that names it (LEAK-10 / LEAK-6). Dropping the columns is the
  last resort, as both sides agree.

**A6. Worth benchmarking: concede**

Agreed (TP-2; forest_fires). I raised no value point.

**A7. Cleaning items: concede CLEAN-11 and CLEAN-5; dispute CLEAN-13 in part**

* 1.59 masking (CLEAN-11) and dropping `rate_negative_words` (CLEAN-5): agreed by both sides.
* CLEAN-13: I agree it cannot block the task (principles step 3), and I never asked for that. But CLEAN-13 is a Must,
  and a Must has no exceptions (principles, Strengths). A pending amendment is not yet a rule. Until the curator amends
  it, the Must is "fixed in the definition when it can be". Six separate flag columns are a lossless fix that costs
  nothing. Remedy: ship the flags now, or the curator decides the mortgage amendment first and both datasets follow it.
  The choice of order is a curator call.

**Where we stand**

| Point | Status | Remedy |
|---|---|---|
| Points 2, 3, 5, 6, 7 | agreed | wording, `splits_comment` note, 1.59 mask, drop `rate_negative_words`, record fixes |
| A5 / point 1 | open | the remedy for the keyword and self-reference values read too young: mask the traced cells (my ask) or keep with a note (advocate). The decisive experiment is the gain by source-article age. |
| A7 / point 4 | open, a curator ordering call | CLEAN-13 |

</details>
