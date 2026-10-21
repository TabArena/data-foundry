# zillow_prize

**Outcome:** added. The AI recommends shipping it. The home sales of round 1 of the Zillow Prize (Los Angeles, Orange
and Ventura counties, January 2016 to July 2017), each with the county facts of the property file of its year; the
target is the log error of the Zestimate (Zillow's automated home value estimate); 9 monthly test windows after a
one-month gap, scored with MAE (the competition's metric). Validity: SEL holds; USE-1 and USE-5 hold; USE-6 and USE-8 triggered, so the fit to
Zillow's real task is `approximate` (the Zestimate, the listing data and the last sale price were never released);
LEAK-10 triggered for the tax delinquency of the sales before September 2016 (looked up after the sale), fixed by
blanking it there (LEAK-7); the building facts and tax values meet LEAK-10's "did not change" clause (measured,
noted); USE-3 rests on a Kaggle FAQ no one could read (issue 3); SPLIT-1 and SPLIT-10 hold. Value: TP-2, a small real
signal, kept; the tuned results decide (TP-1, in the record). Quality: CLEAN-10 fixed (garage areas of 0 for a garage
with cars set to missing); two departures need an exception (issues 6, 9). Weighed: signal size -, an RMSE that a few
rows dominate -, source and use case +, size +. If tuned methods do not beat the train mean window by window, the
dataset goes to `TBD -> 2nd Tier`. The window length and the gap are part of the house-price items of the working
copy's REVIEW.md.

**Main points:** Confirm the prediction point from Kaggle's FAQ (issue 3); the metric is settled by the amended TP-6 (`mae`); two cleaning exceptions (issues 6, 9).

**Record judgment:** valid with concerns. A real task of Zillow's, approximated from the county facts it released;
the signal is small, and a few extreme rows (mostly miskeyed prices, by Zillow's account) dominate the squared
error.

**Issues for Lennart:**

3. **Is the prediction point the first day of the sale month?** The definition predicts each sale from the first day
   of its month (`transaction_month`), because the Kaggle FAQ, as the definition's notes quote it, says Zillow pairs
   each sale with the Zestimate of that day. No panel member could read the FAQ or the Data page (Kaggle shows them
   only after a login).
   - Effect on the task: if Zillow took the Zestimate on another day, such as the sale day, the time column and the
     task summary describe the wrong moment of prediction; the rows and the monthly windows stay the same.
   - Evidence: the day of the month barely relates to the logerror (rank correlation -0.013 over the kept sales);
     that is what either reading predicts, so the data cannot settle it and only the FAQ can.
   - Implemented: `transaction_month`. Alternative: the sale date `transactiondate` as the time column; the rows,
     features and windows stay, so only the time column and the task summary change. Precedent: perth_house_prices
     also predicts from the first day of the sale month (there because its source gives no day).
   - Rule: USE-3 (P3, Must; name the prediction point); EV-7 (a source no one read leaves the claim untested).
   - Recommendation: read the FAQ and the Data page with a Kaggle login and keep the month if they confirm it;
     take the author list of Kaggle's "Cite" box for the BibTeX in the same visit. Decision: confirm the prediction
     point, or reopen the time column.

6. **Put `buildingqualitytypeid` on one scale without a published conversion?** The column rates the building's
   condition (lower is better). properties_2017 uses another scale: the same parcel has the same code in both files
   for 0.8% of the parcels. The definition maps each 2017 code onto the 2016 code it comes from, read off the parcels
   in both files (the README's decision table: 9 to 1 for 4,843 of 4,843 parcels, 8 to 4 for 31,217 of 31,219; the
   weakest, 1 to 10, for 37 of 40). The mapped column holds 8 values.
   - Effect on the task: one meaning per code in the 2016 training rows and the 2017 test rows; with the raw codes a
     code means one thing in training and another in test. The score does not settle it (CLEAN rules decide by
     meaning, not by score), so the choice is about meaning.
   - Rule: CLEAN-21 (P7, Should; college_scorecard, Lennart, 2026-10-16) puts a changed scale on one scale "with the
     conversion the source or the measuring body publishes". Zillow publishes none; the fact that sets this case
     apart is that the data shows a many-to-one map.
   - Alternative: keep the raw codes (a code means one thing in the 2016 training rows and another in the 2017 test
     rows), or drop the column (loses the only condition rating).
   - Recommendation: record an exception to CLEAN-21 with that fact. Decision: the exception, the raw codes, or the
     drop.

9. **Keep the census tract-and-block numbers numeric?** `rawcensustractandblock` and `censustractandblock` are
   county, tract and block codes with 55,601 and 55,348 distinct values, stored as numbers. Every other location code
   of the definition (county, city, ZIP region, neighbourhood, zoning, land use) is a category, as the postcodes are
   in house_sales, melbourne_housing_market and perth_house_prices.
   - Effect on the task: as numbers, trees split on ranges of the code, and neighbouring tracts share their leading
     digits, so a range is an area; as categories they are two columns of about 55,000 levels each.
   - Rule: CLEAN-14 (P7, Should; a fixed set of codes is categorical). Precedent: brazilian_ecommerce keeps its zip
     prefixes numeric because "their order follows geography"; the definition's note gives the same reason. The
     advocate and the critic both accept the exception.
   - Implemented: numeric. Alternative: categories, two columns of about 55,000 levels each that most models must
     hash or drop.
   - Recommendation: record an exception to CLEAN-14 with that reason. Decision: the exception, or categories.

**Review panel:** ship after changes (mediator). Full tier: claim, column and split audits, domain practitioner,
blind review, precedent check, advocate and critic with one rebuttal each, mediator; their numbers are on the
definition without the mediator's changes (the delinquency blanked before September 2016, the garage areas). Claim
audit: 64 claims; refuted and corrected in the definition: "keeps later edits out", the signal numbers, "5 levels",
"repeats the sale year", the room-count note; untested: the claims that rest on Kaggle's pages (the prediction
point, issue 3). Blind review: would exclude (tuned LightGBM R^2 at most 0.007; the outliers decide RMSE). Debate:
agreed on the fit `approximate`, blanking the delinquency, the notes and the garage fix; disputed: the tuned check as
a condition for shipping (the mediator: a follow-up, not a gate) and the metric (issue 1).

<details><summary>Mediator</summary>

Inputs: claim, column and split audits, practitioner, precedents, blind review, checklist,
both briefs and rebuttals, the earlier REVIEW.md. Decisive experiment: the delinquency columns as-is, blanked or
dropped (threads capped at 2).

**Judgment record**

```text
Verdict: ship after changes.
Validity: SEL holds (licence noted only); USE-1, USE-5 hold; USE-6/USE-8 triggered, fixed (fit `approximate`: the
  Zestimate, listing data and last sale price were never released); LEAK-10 triggered for the Jan-Aug 2016 training
  rows (tax delinquency looked up after the sale, the "did not change" clause fails), fixed by LEAK-7 (blank both
  columns for sales before Sep 2016); LEAK-10 holds for the building facts and tax values under its own clause
  (measured, note to add); SPLIT-1, SPLIT-10 hold.
Value: TP-2, a small real signal (keep); TP-1 tuned check is a follow-up, not a gate (fails -> TBD -> 2nd Tier).
Quality: CLEAN-10 fixed (garage zeros); CLEAN-21 (spa flags) and CLEAN-5 near copies kept with notes; CLEAN-21
  method (quality map) and CLEAN-14 (numeric tract codes) need the curator's exceptions.
Weighed: signal size -, outlier-dominated RMSE -, source and use case +, size +.
For the curator: issue 1 (confirm the FAQ prediction point), issue 2 (metric, in the cross-cut), issue 3 (two exceptions).
```

**Agreed facts (both sides, measured)**

1. Test rows (Nov 2016-Jul 2017) carry no value from after their prediction point that changes the score: the
   delinquency snapshot (about Aug-Sep 2016) predates every test window; tax values of 2017 sales show no reset
   (share moved 0.204-0.217, flat by sale month); building facts differ between files for 3.2-3.7% of 2017-only
   parcels, flat by month (COL T1, T2, T4).
2. The Jan-Aug 2016 training rows carry post-sale values: delinquency flagged 1.54% (months 1.2-2.5%) against
   3.1-4.7% from Sep 2016; building-fact edits 1.4-2.3% for Jan-May 2016 sales against about 1.1% later (CA rows 7,
   10). "Keeps later edits out" overclaims.
3. Fit is `approximate` (USE-6, USE-8): the advocate conceded in rebuttal.
4. Signal: L1 LightGBM beats the train mean in 8-9 of 9 windows, R^2 about 0.001-0.012; Huber 6-8 of 9; L2 3-4 of 9;
   the median constant loses to the mean 9 of 9 and L1 beats the median 9 of 9, so the gain is in the features. The
   written 0.003-0.021 and "Huber 9 of 9" do not reproduce.
5. 0.38% of rows (|logerror| > 1) hold 49.9% of the squared error; the source scored MAE.
6. Split: temporal, 9 monthly windows, one-month gap, oldest train share 53%; right with notes. Nov/Dec 2016 are
   Kaggle's remnant sample (about 18% of a month); the Nov 2016 tail deficit is not significant after correction
   (p about 0.12).
7. Cleaning: `garagetotalsqft` = 0 on 14,981 rows with 1-3 spaces; spa flags halve between files; three near copies
   (98.9-99.98%, not exact); writing slips (8 quality values not 5; `assessmentyear` = sale year - 1; roomcnt zeros
   masked in every county).
8. Claim 18 (the Zestimate of the first of the month, FAQ) is untested: no agent could read Kaggle's pages.

**Decisive experiment: does the delinquency weaken the signal? (settles the LEAK-11 question)**

Delinquency columns as-is, blanked for sales before Sep 2016, or dropped; L1 LightGBM, two configs, seeds 0-2, the
definition's 9 windows, R^2 skill against the train mean.

| config | as-is (mean of 3 seeds) | blanked before Sep 2016 | dropped | seed spread within a variant |
|---|---|---|---|---|
| l1_default | 0.00555 (wins 8, 9, 9) | 0.00566 (9, 9, 9) | 0.00555 (9, 9, 9) | up to 0.0005 |
| l1_slow | 0.00560 (9, 9, 9) | 0.00562 (9, 9, 9) | 0.00535 (9, 9, 9) | up to 0.0003 |

* No variant differs from another by more than the seed spread: no measured weakening, no measured inflation.
* The model leans on the columns twice as much once the post-sale values are blanked (gain share 0.4-0.6% as-is,
  1.2-1.4% blanked): the post-sale values dilute the column, consistent with the "sale clears the arrears" story
  but not a measured effect on the score.
* Flag vs target: flagged minus unflagged mean logerror 0.031 before Sep 2016, 0.014 after; the column means
  something different in the two periods.

**Disputed points, settled by rank**

**A. Tax-delinquency columns (P4): blank before Sep 2016. Settled, no curator decision needed.**

* Advocate: LEAK-11 (Should, narrows LEAK-10) keeps a post-outcome value that weakens the signal, with a note.
* Critic: LEAK-10 and LEAK-6 (Must); blank (LEAK-7) or drop.
* Ruling. LEAK-11 needs a weakening; the experiment measures none on the score, so its scope is not reached and
  there is no conflict: LEAK-10 (Must) applies alone. The values are "attributes looked up after the outcome" and
  the "did not change" clause fails (1.5% against 3.8% flagged). LEAK-10 says fix it the smallest way (LEAK-7):
  blanking the pre-Sep 2016 rows removes every post-sale value, keeps the pre-sale signal for all test rows and
  costs nothing measurable; dropping is a larger remedy than needed (LEAK-7 prefers the smaller fix). Remedy ladder:
  fix the definition before keep with a note. Both sides accept this remedy (advocate rebuttal 2, critic rebuttal 2).
* Detail: September 2016 (3.1% flagged) already looks post-snapshot. Blanking September too is a free margin (all
  September rows are training rows); the tested cut is before 1 Sep 2016.

**B. Tuned check as a condition for shipping (P6): not a gate. Settled.**

* Critic: TP-1 (Must) requires the tuned check; untuned L2 loses, unlike the pending-tuned precedents.
* Advocate: TP-1 applies "before acting on" a flag; keeping is not acting; TP-2 keeps the task until a concrete
  reason is found.
* Ruling. TP-1 governs acting on the flag (retiring or tiering). TP-2 keeps the task while no concrete reason is
  found, and the features beat the median constant on 9 of 9 windows, which is real signal. So the dataset ships;
  the tuned check is a recorded follow-up whose failure moves it to `TBD -> 2nd Tier` (the earlier REVIEW.md's issue 2). The
  blind reviewer's "exclude, R^2 <= 0.007" is the skill cutoff TP-2 rejects. Both rebuttals end on this same remedy;
  what is left is wording.

**Changes to make now (no decision needed)**

1. `fit = "approximate"`; `fit_reason` names the gap: Zestimate, listing data and last sale price never released
   (USE-6, USE-8).
2. Blank `taxdelinquencyflag` and `taxdelinquencyyear` for sales before 2016-09-01 (LEAK-10 via LEAK-7); replace the
   `Potential leak, kept on purpose:` bullet with the fix and the numbers above.
3. Replace "keeps later edits out" in `changes`, the curation bullet and `fit_reason` with the measured statement:
   properties_2016 is a snapshot of about Sep 2016, properties_2017 postdates every 2017 sale; building facts differ
   for 1.4-2.3% (Jan-May 2016) and 3.2-3.7% (2017-only) of parcels, flat by sale month in 2017; tax values show no
   reset (LEAK-10 "did not change" clause, as melbourne).
4. Correct the signal numbers: "L1 LightGBM beats the train mean in 8-9 of 9 windows (R^2 about 0.001-0.012);
   squared-error fits do not"; drop "Huber 9 of 9"; name the config (EV-8, TP-2).
5. Mask `garagetotalsqft == 0 & garagecarcnt > 0` to missing (CLEAN-10).
6. Notes: the spa/hot-tub flags are recorded for about half as many parcels in properties_2017 (CLEAN-21); the three
   near copies stay because they differ on some rows (CLEAN-5 covers exact copies only); Nov and Dec 2016 are
   Kaggle's remnant sub-samples (SPLIT-17); `buildingqualitytypeid` holds 8 values, lower is better.
7. Writing: `assessmentyear` is the sale year minus one; roomcnt zeros are masked in every county; "5 levels" -> 8.
8. List zillow in the metric cross-cut of `tabarena-v0pt2/REVIEW.md` as a case the TP-6 amendment would flip to `mae`,
   with the L2-wins-4-of-9 fact; leave the metric open (both sides).
9. Record line for TP-1: tuned results pending; if tuned methods do not beat the dummy window by window,
   `TBD -> 2nd Tier`.

**Issues for the curator (ranked)**

1. **Prediction point rests on an unread FAQ (P3, USE-3 Must; EV-7).** Problem: "the Zestimate of the first of the
   month" (claim 18) could not be read. Effect: if wrong, `transaction_month` is the wrong time column. Evidence: day
   of month vs logerror Spearman -0.013 (consistent, not proof). Decision: read the FAQ and Data page with a Kaggle
   login and confirm, or reopen the time column.
2. **Metric: RMSE (house rule) or MAE (the source's scoring) (P6, TP-6 Must vs definitions.md "Field mapping").**
   Problem: under RMSE 0.38% of rows hold half the error; untuned L2 wins 4 of 9 windows, L1 8-9 of 9. Advocate: a
   robust loss is part of fitting a heavy tail; features rank models under either metric. Critic: TP-6 names the
   source's scoring as the better version. Decision: in the collection cross-cut, not here (treat like cases alike).
3. **Two exceptions to record (P7, Should).** `buildingqualitytypeid` mapped by a crosstab read off the data, no
   published conversion (CLEAN-21 method; R^2 within 0.001 for raw, mapped, dropped); tract-and-block codes kept
   numeric (CLEAN-14; order follows geography, 55k values; brazilian_ecommerce). Decision: record each as an
   exception, or change the column.
4. **Amendment candidate (collection, LEAK-6/LEAK-11).** african_credit and melbourne keep post-outcome lookups
   because removing them "changes nothing" (PC decision 3). With fix A, zillow leaves that pattern, so it is not the
   third case; the amendment question stays open for the other two.
5. **Licence (SEL, note only).** No redistribution outside the competition; matters only if the container is
   published. BibTeX `{Zillow}` can take the Kaggle "Cite" authors.

Not raised again (both sides and the split audit keep the implemented choice): 9 monthly windows with a one-month
gap, the month as time column, the Aug-Sep 2017 drop, the extreme rows kept.

**Consistency with precedent**

* Fit `approximate`: follows african_credit_scoring_challenge, kick, churn_telco_south_asia (USE-8).
* Building facts and tax values kept with a measured note: follows melbourne_housing_market (LEAK-10 clause met);
  house_sales differs on the fact that its record changed after 10% of sales and flattered the model.
* Delinquency blanked: departs from the keep-with-no-effect drafts (african_credit, melbourne). Fact that sets it
  apart: here the "did not change" clause measurably fails (1.5% vs 3.8%) and a lag-style fix removes every
  post-sale value at no cost (LEAK-7). Neither precedent is a curator decision.
* Small signal kept pending tuned results: follows forest_fires (CC 2026-10-06), sf_permit_time, bias_correction.
  Distinguishing fact noted, not decisive: here untuned L2 loses; the features still beat the median constant 9 of 9.
* Metric under the house rule: follows dataorg_financial_health and african_credit; open in the cross-cut.
* One-month gap: follows brazilian_ecommerce (Lennart, 2026-10-15). Garage zeros: follows house_sales and
  churn_telco_south_asia (CLEAN-10).

</details>

<details><summary>Claim audit</summary>

Auditor: claim-auditor, review panel phase A. Data: the definition's frame and split plan rebuilt from the raw files
through `dataset_io.from_definition` (153,108 rows, 9 splits), plus the raw zips (md5 of all five match). Models: LightGBM 4.6, untuned
(`subsample=0.8`, `colsample_bytree=0.8`), configs `default` (100 trees) and `slow` (400 trees, lr 0.02,
min_child_samples 200), seeds 0 and 1, on the 9 shipped windows; skill = 1 - SSE(model)/SSE(train mean) on the test
window. No repository file was edited.

Claim numbers refer to the panel's list of claims. D = dataset.py, R = record, RB = the earlier REVIEW.md.

**Table**

| # | Claim (short) | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 1-2 | Question / use case: Zillow predicts, before a month, how far the Zestimate misses the sale price | D task_summary | Source text (Kaggle pages render no text; kaggle CLI absent) | untested | Target formula confirmed by third-party pages only; FAQ not readable | USE-1, EV-7 |
| 3 | Row: one sale, LA/Orange/Ventura, Jan 2016-Jul 2017, 153,108 sales | D | Count rows, fips, months on the frame | holds | 153,108; fips 6037/6059/6111 = 99,476/41,354/12,278; months 2016-01..2017-07 | PROV-1 |
| 4 | 2.1% beyond 0.4, "mostly data errors" | D | Share on frame; cause untestable without prices | holds (share); untested (cause) | 2.10% | USE-5 |
| 5 | Known: sale month and home facts of the sale year's property file | D | assessmentyear per file; tax-value jump 2016->2017 by 2017 sale month; building-fact edit rate by sale month | holds for test rows | properties_2016 assessmentyear 2015 for all 90,275 2016 sales, properties_2017 2016 for all 2017 sales; parcels sold Jan-Sep 2017 show the same share of |dlog taxvalue|>0.1 in every sale month (9.3-9.8%) and building-fact edit rates 0.9-1.3% (unsold 1.36%): no trace of the 2017 sale in properties_2017 | LEAK-1, USE-3 |
| 6 | Split: 9 one-month windows Nov 2016-Jul 2017, newest first; train ends before the preceding month | D | Inspect plan | holds | test months 2017-07 ... 2016-11 in order; each train max = test month - 2 | SPLIT-1 |
| 7, 22 | Each sale takes its year's property file, "which keeps later edits out" (of the 2016 rows) | D | Delinquency agreement between files; edit rate by 2016 sale month | partly refuted | properties_2016 is itself a snapshot of about Sep 2016: delinquency flags agree in both files for 4,525 parcels, differ for 8; building-fact edit rate (2016->2017 file) 1.4-2.3% for parcels sold Jan-May 2016 against 1.0-1.2% Jun-Dec 2016 and 1.36% unsold. So Jan-Aug 2016 training rows still carry facts recorded after the sale; the year-matched file removes only the edits made after the 2016 snapshot. Test rows (Nov 2016 on) are not affected | LEAK-1 (Should here: training rows only, effect small), writing |
| 8-9 | fit direct; prediction before the sale month from facts on file | D | See 5, 6 | holds (data side); use-case reality for the practitioner | | USE-8 |
| 10, 30 | Delinquency snapshot postdates Jan-Aug 2016 training sales; dropping it changes nothing (R^2 0.0069 vs 0.0068) | D | Flag share by month; L1 LightGBM with and without both columns, 2 configs x 2 seeds | holds (substance); numbers not reproduced | share Jan-Aug 2016 1.54% (months 1.24-2.50%), Sep 2016-Jul 2017 3.12-4.69%; mean skill with/without: default 0.0058/0.0056 (s0), 0.0056/0.0057 (s1); slow 0.0056/0.0053 both seeds. 0.0069/0.0068 is from another config (EV-8) | LEAK-10, EV-8 |
| 11, 21, 56 | Signal beats the train mean in all nine windows; L1 R^2 0.003 to 0.021 | D fit_reason, CC, R | L1 per window, 4 runs; constant train median; paired t on squared errors | holds narrowly (L1 only); range refuted | L1 wins 9/9 in 3 runs, 8/9 in one (Mar 2017 -0.0001); per-window skill 0.0008-0.0123 (panel probe 0.002-0.017), never 0.021; paired t per window 0.45-3.99, below 2 in 4 of 9 windows (Jul, May, Feb 2017, Dec 2016). The features carry it: the train-median constant loses to the mean in 9/9 (-0.001 to -0.005), L1 beats the median constant 9/9. fit_reason does not say the win needs an absolute-error loss: L2 wins 3/9, Huber 6-7/9 | TP-2, EV-6, EV-8 |
| 12 | year, source, url, domain, tags | D | Source page | holds (year, source); domain a judgment | | PROV-2 |
| 13, 57 | Licence: competition use only, no redistribution | D, R | Rules page unreadable | untested (and never evidence) | | EV-4, EV-7 |
| 14 | md5 sums; dictionary read by no code | D | md5sum; grep | holds | all five match; no code reads the xlsx | |
| 15 | BibTeX author {Zillow} | D | Kaggle Cite box unreadable | untested | | PROV-10 |
| 16, 19 | Target logerror, regression, RMSE; 4 decimals as source | D | Check rounding | holds | all values equal their 4-decimal rounding | |
| 17 | Files and counties | D | Raw files | holds | | |
| 18 | Prediction point: Zestimate of the first day of the sale month (FAQ) | D | FAQ unreadable | untested | day of month vs logerror Spearman -0.013 (consistent with a month-level Zestimate, not proof) | USE-3, EV-7 |
| 20, 42, 55 | 2.1% (|y|>0.4) hold 74% of the squared error; 0.4% (|y|>1) hold half | D, R | Frame | holds | 2.10% / 74.3%; 0.38% / 49.9% | USE-5 |
| 23, 35, 54 | Aug-Sep 2017 dropped, 14,737 rows, "biased sample" | D | Count; quote unreachable | holds (count); untested (quote) | 9,936 + 4,801 = 14,737 | SPLIT, EV-7 |
| 24 | After 15 Oct 2016 a partial sample, looks random (2.2% vs 2.0% beyond 0.4) | D | Shares; per-month tail | holds as stated; weak doubt | 2.21% vs 2.03%. But Nov 2016 (a test window, 1,826 rows) has 1 row with |y|>1 (0.05%) where the other months have 0.32-0.52% (about 7 expected; Poisson P(<=1) about 0.006, one month of 21 checked). Nov 2016 >0.4 share 1.59%, Dec 2.70% | SPLIT, EV-6 (maybe a thinned tail) |
| 25 | 24 sales of 2017 without home facts dropped, as Zillow did for 2016 | D | Count; 2016 file | holds (data); untested (discussion 34667) | 34 such 2017 sales, 24 before Aug 2017; 0 in 2016 (consistent with Zillow having removed them) | |
| 26 | 19 sales within 31 days of a sale of the same parcel dropped, as the competition does | D | Recompute | holds (count); untested (Data page) | 19; 0 same-day; 2,185 repeat-parcel rows stay | LEAK-16 |
| 27, 36, 41 | 2017 quality codes each come from one 2016 code; mapping as listed; stays ordinal | D | Crosstab of parcels in both files | holds approximately | each 2017 code has one dominant 2016 code matching the map: 9->1 (4,843/4,843), 7->4 (12,662/12,663), 8->4 (31,217/31,219), 3->7 (673/674), 4->7, 5->7, 6->7 (28,593/28,595), 10->10 (595/615, 97%), 11->10 (2,015/2,015), 12->12 (220/232, 95%), 1->10 (37/40, 93%), 2->10 (13/13) | CLEAN |
| 28, 37 | Presence flags hold one value or nothing (True, "Y", 1, 66, 7) | D | Unique non-null values per file | holds | 'true', 'Y', 1, 66, 7 in both files; the assert in `_clean` passes | CLEAN |
| 29 | taxdelinquencyyear 3-15 and 99 -> four-digit years | D | Raw and frame values | holds | raw {3,4,6..15,99}; frame 1999, 2003, 2006-2015 | |
| 31 | Zero means not recorded in roomcnt (99,475 of 99,476 LA rows), bathroomcnt, bedroomcnt with bath 0 | D | Zeros by county in raw sales; derived counts | holds; note incomplete | LA 99,475 of 99,476 NaN after cleaning (holds). The code masks zeros in every county: 19,949 Orange sales (44% of Orange) and 448 Ventura sales also had roomcnt 0 and become missing, not mentioned in the note (Orange zero rows: median 3 bedrooms, 2.5 baths, so "not recorded" fits there too). Bath 0 rows have no calculatedbathnbr/fullbathcnt (0 of 1,842 / 1,403). Bedroom NaN rows: median 2,188 sqft vs 1,540 overall; 480 bedroom zeros with bath > 0 stay | CLEAN, writing |
| 32 | Dropped: parcelid, regionidcounty (recoding of fips), assessmentyear ("repeats the sale year"), transactiondate | D | Crosstabs | holds except one phrase | regionidcounty 3101/1286/2061 = fips 6037/6059/6111 one-to-one. assessmentyear is the sale year minus one (2015 for every 2016 sale, 2016 for every 2017 sale with facts), not the sale year; still a function of the file, so dropping it is right | writing |
| 33, 38 | Codes categorical; census tract numbers numeric | D | Feature types in README | holds | 12 categoricals | CLEAN |
| 34 | 7 exact duplicates and 39 feature duplicates, separate sales of separate parcels | D | Groups with parcelid kept | holds | 14 rows in exact pairs, 14 distinct parcels; 39 feature-duplicate groups (85 rows), none with a repeated parcel | LEAK-16 |
| 39 | Property files have 2,985,217 rows each | D | Line count | holds | 2,985,218 lines each including the header | |
| 40, 63 | Aug-Sep 2017 hold about twice the share of extreme errors (0.72%/0.77% vs 0.32-0.43%) | D, RB | Monthly shares | holds | 0.72%, 0.77% vs 0.32-0.43% Jan-Jul 2017 | |
| 43 | One prediction per home and month, before the month; round 1 scored Oct-Dec 2017 with data of 2 Oct | D | Source unreadable | untested | the competition asked for six month columns at once (a horizon up to three months), so "before the month starts" is our framing; the 1-month window with a 1-month gap is a defensible simplification, not the source's protocol | SPLIT-5, USE-3 |
| 44, 45 | 9 windows, newest first; gap one month | D | Plan | holds | | SPLIT |
| 46 | Oldest window trains on 53% | D | 81,731 / 153,108 | holds | 53.4% | |
| 47 | Accepted warning: each window holds one date | D | Plan | holds | each test window has a single `transaction_month` | |
| 48-51 | Screening comments, front matter | R | | holds as opinions; "multiple targets for horizons" is resolved by one month column | | |
| 52 | Target is Zillow's own residual (FAQ, discussion 33899) | R | Source unreadable | untested | | USE-5, EV-7 |
| 53 | properties_2017 differs for 1.2-2.0% of parcels sold Jan-May 2016, 0.81% unsold | R | Edit rate on 5 building facts | holds in direction; baseline not reproduced | sold Jan-May 2016 1.44-2.29%, unsold 1.36% on sqft/bed/bath/yearbuilt/lot (column set differs from the record's) | EV-8 |
| 58 | Priority 3; signal tiny | R | see 11 | holds | | TP-2 |
| 59 | L1 skill 0.0069-0.0073 9/9; Huber 9/9 (0.0096-0.0101); L2 4/9; L1 beats the median in MAE 8/9 | RB | 4 L1 runs, 2 Huber, 2 L2 | refuted for Huber and the L1 level | L1 mean 0.0053-0.0058 (8-9/9); Huber 6/9 and 7/9 (mean 0.0028, 0.0054), panel probe 8/9; L2 3/9; L1 MAE vs median 8-9/9 | TP-2, EV-8 |
| 60 | Public LB MAE 0.064 vs 0.066 for zero; on 4,605 late-2016 sales 0.0704 / 0.0696 / 0.0693 | RB | Recompute constants; LB is another benchmark's score | holds (constants); LB untested and never evidence | 4,605 rows; 0.0704 zero, 0.0696 median, 0.0693 mean | EV-4 |
| 61 | transactiondate day: Spearman 0.01 | RB | Spearman on kept sales | holds | -0.013 | |
| 62 | 3-month windows: 31,413 / 24,407 / 10,580 rows | RB | Frame | holds | exactly these | |
| 64 | 2016 scale of buildingqualitytypeid has 5 levels | RB | Unique values | refuted | properties_2016 (sold parcels) holds 8 values: 1, 4, 6, 7, 8, 10, 11, 12; the frame holds the same 8 (6, 8, 11 on 8 rows); only the mapped 2017 rows have 5 | writing |

Implied claims (nobody wrote them down):

| Implied claim | Test | Result | Evidence | Rule |
|---|---|---|---|---|
| Every feature is known at the prediction point of the test rows | assessment years; tax-value and building-fact changes by 2017 sale month; delinquency identity | holds | see rows 5, 7 | LEAK-1 |
| Every feature is known at the prediction point of the training rows | same | refuted for Jan-Aug 2016 (documented for delinquency only) | delinquency and building facts of properties_2016 postdate those sales; delinquency documented, building-fact edits not (edit rate up to 2.3% vs 1.1%) | LEAK-1, LEAK-10 |
| No row is a copy across the split | duplicates with parcelid | holds | all duplicates are distinct parcels; repeat sales (2,185 rows) are real re-sales | LEAK-16 to LEAK-21 |
| The split is the one the use case needs | source protocol | untested (source) | competition: six months predicted at once (horizon to 3 months); ours: 1-month windows, 1-month gap | SPLIT-5 |
| The target is the real-world target | source | untested (source); the RMSE/MAE question stays | 0.38% of rows hold 49.9% of the squared error | USE-5 |
| The signal is in the features, not a location shift | constant train median vs mean; L1 vs median | holds | median constant loses 9/9; L1 beats it 9/9 | TP-2 |

**Refuted and untested, ranked (principles.md: validity first, Must first)**

1. **Claims 7 and 22, "keeps later edits out" (P4, LEAK-1; Should-strength here).** properties_2016 is itself a
   snapshot of about September 2016 (its delinquency flags equal those of properties_2017 for all but 8 of 4,533
   flagged parcels), so the Jan-Aug 2016 training rows carry building facts and delinquency recorded after the sale;
   building-fact edits run 1.4-2.3% for parcels sold Jan-May 2016 against about 1.1% later. Test rows (Nov 2016 on)
   are clean, and no test target leaks. What it changes: the wording of `changes` and the CC bullet, not the data.
   Mildest remedy: reword to "keeps the edits made after the 2016 snapshot out; the 2016 file is itself a snapshot of
   about September 2016, after the sales of January to August 2016 (training rows only)".
2. **Claims 11, 21, 56, 59: the signal numbers (P6, TP-2; EV-8).** The direction holds for an absolute-error loss
   only (L1 8-9 of 9 windows; Huber 6-7 of 9, not 9 of 9; L2 3 of 9), and the per-window paired t is below 2 in 4 of 9
   windows. The R^2 range 0.003-0.021 is not reproduced (0.0008-0.0123 here, 0.002-0.017 in the panel's probe), nor
   the L1 mean 0.0069-0.0073 (0.0053-0.0058). What it changes: the evidence for the TP-2 keep is thinner than written;
   tuned results (TP-1) remain the decider. Mildest remedy: write "LightGBM with an absolute-error loss beats the
   train mean in 8 or 9 of 9 windows depending on the seed (R^2 about 0.001 to 0.012); squared-error fits do not",
   name the config, and drop the Huber 9/9 statement from the review issue.
3. **Claim 24, "the share looks random" (P4, weak; EV-6).** Holds on the 0.4 threshold, but the Nov 2016 test window
   has 1 row beyond |1| where about 7 are expected (p about 0.006 before correcting for 21 months). Maybe a thinned
   tail in the public-leaderboard holdout; it would make that window easier under RMSE. Mildest remedy: a note; the
   test that would settle it is the |y|>1 share in Oct 15-Dec 31 2016 against the same weeks of 2017.
4. **Claim 64, "5 levels" (P7, writing).** The 2016 scale has 8 values (1, 4, 6, 7, 8, 10, 11, 12). Remedy: fix the
   REVIEW wording.
5. **Claim 32, assessmentyear "repeats the sale year" (P7, writing).** It is the sale year minus one. Remedy: "it is
   constant within each property file (2015, 2016)".
6. **Claim 31, roomcnt zeros (P7, writing).** The note names only Los Angeles; the code also makes 20,397 Orange and
   Ventura zeros missing (44% of Orange sales). The cleaning is right; the note should say "in every county (all of
   Los Angeles, 44% of Orange)".
7. **Untested (source text unreachable: Kaggle pages render no text, no kaggle CLI; EV-7):** claims 1-2, 18 (the
   FAQ's Zestimate timing), 23 and 54 ("a biased sample"), 25 (discussion 34667), 26 (the 31-day rule on the Data
   page), 43 (the round-1 protocol), 52 (discussion 33899), 13 (licence), 15 (BibTeX), 60 (leaderboard MAE, never
   evidence, EV-4), and "mostly data errors" in claim 4. A human with Kaggle access should read the FAQ and Data
   page; claim 18 matters most, since the prediction point rests on it (USE-3).

</details>

<details><summary>Column audit</summary>

Frame: the definition's own frame and split plan (`dataset_io.from_definition`, origin `definition`), 153,108 rows,
56 features + `logerror`. Codebook: `zillow_data_dictionary.xlsx` (sheet "Data Dictionary" plus 7 code-label tabs).
Prediction point (first `curation_comments` bullet): the first day of the sale month.

**Timing facts the column verdicts rest on (measured)**

* T1. Both property files hold the *same* tax-delinquency snapshot: `taxdelinquencyflag`/`taxdelinquencyyear` agree
  100% on the 165k sold parcels in both files, same missing share (0.973), latest year 2015. Flag share by sale month:
  1.2-2.5% Jan-Aug 2016, 3.1% Sep, 4.7% Oct, 3.4-4.7% Nov 2016-Jul 2017. So the snapshot is about Aug-Sep 2016
  (claim 30 holds), **before every test window** (the oldest is Nov 2016). The post-sale values sit only in the
  training rows of Jan-Aug 2016.
* T2. Tax values: properties_2016 has assessment year 2015, properties_2017 has 2016. The share of parcels whose
  `taxvaluedollarcnt` moved by more than the Prop-13 factor (1.01525) between the files is 0.23-0.26 for parcels sold
  Jan-May 2016 and 0.19-0.21 for Oct-Dec 2016, so the 2017 file carries some 2016 sale reassessments (taking the
  own-year file avoids them, claim 22). For parcels sold only in 2017 it stays flat at 0.204-0.217 from Jan to Sep
  2017: the own-year file shows no sign of holding the row's own sale. That answers the checklist's draft issue 3: no
  evidence that the own-year tax values hold the sale price.
* T3. `taxamount` in properties_2017 equals properties_2016 for 91.5% of parcels (the 2015-16 bill, taxamount/value
  0.01264 against the 2016 values), while the three value columns changed for 94-95%. A stale but pre-sale value; no
  leak.
* T4. Building facts (13 main columns) differ between the files for 2.8-4.5% of parcels sold in 2016 and 3.2-3.7% of
  parcels sold only in 2017, falling slightly with the sale month in both years (Jan 2017 3.66%, Jul 2017 3.19%).
  properties_2017 (released October 2017) is a post-sale snapshot for every 2017 row, so for 2017 rows the own-year
  file does *not* keep later edits out; the measured scale is small (`calculatedfinishedsquarefeet` changed for 69 of
  60,472 parcels sold only in 2017).
* T5. Recording drift between the files: `pooltypeid10` is set for 1,191 parcels in properties_2016 that lack it in
  properties_2017 (15 the other way); `hashottuborspa` 1,189 vs 54. Share in the frame: `pooltypeid10` 1.1-1.5% per
  month in 2016, 0.44-0.76% in 2017; `hashottuborspa` 2.2-3.1% vs 1.5-2.3%. `buildingqualitytypeid` agrees on 0.8%
  of parcels (the scale change the definition maps). All other columns agree on 99.2-100%.

**Column table**

| column | meaning (codebook) | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| `logerror` (target) | log(Zestimate) - log(sale price) | target | float, rounded to 4 decimals; 902 zeros, range -4.66 to 5.26 | fine (metric weighing is the target auditor's) | USE-5 |
| `transaction_month` | first day of the sale month (built from `transactiondate`) | yes, it is the prediction point | datetime, 19 values | fine | USE-3, CLEAN-14 |
| **Location** | | | | | |
| `fips` | county FIPS code (3: 6037 LA, 6059 Orange, 6111 Ventura) | yes | category (Int64 codes) | fine; `regionidcounty` (a recoding) dropped correctly | CLEAN-5, CLEAN-14 |
| `latitude`, `longitude` | parcel centre in degrees x 1e6 | yes | float, 0% missing | fine; optional cosmetic: divide by 1e6 to degrees | CLEAN-21 (cosmetic) |
| `rawcensustractandblock` | state+county+tract+block group (+block), as a decimal number | yes | float, 55,601 values | fine as numeric (hierarchical code: trees can split prefix ranges); a departure from CLEAN-14 already documented (claim 33) | CLEAN-14 |
| `censustractandblock` | same code, 14 digits, the dictionary's text is word for word the raw one's | yes | float, 55,348 values, 0.5% missing; equals `rawcensustractandblock` x 1e6 on its leading digits in 98.9% of rows | cleaning problem, minor: near copy | CLEAN-5 |
| `regionidcity`, `regionidneighborhood`, `regionidzip` | Zillow region ids (city 178, neighbourhood 505, ZIP-region 389 values; not postal ZIPs, max 399675) | yes | category | fine | CLEAN-14 |
| `propertycountylandusecode` | county land-use code (89 values) | yes | category, codes read as text (leading zeros kept) | fine | CLEAN-14 |
| `propertyzoningdesc` | zoning description, LA only (35% missing = Orange/Ventura) | yes | category, 2,292 values | fine; at 2,292 values CLEAN-14 would allow string; question for the curator only if a model handles high-cardinality categories badly (not a curation argument, EV-4) | CLEAN-14 |
| `propertylandusetypeid` | land-use type (14 values; tab "PropertyLandUseTypeID" has labels) | yes | category of codes | fine; the labels could replace the codes | CLEAN-12 (Should, cheap) |
| **Building type codes** (dictionary tabs with labels) | | | | | |
| `airconditioningtypeid` | cooling system type (6 values, 68% missing; Ventura none) | yes | category of codes | fine; labels available in the tab "AirConditioningTypeID" | CLEAN-12 |
| `architecturalstyletypeid` | architectural style (0.3% filled) | yes | category | fine; labels available | CLEAN-12 |
| `buildingclasstypeid` | framing type (2 values, 30-ish rows filled) | yes | category | fine (near-empty, not constant) | CLEAN-5 |
| `heatingorsystemtypeid` | heating type (12 values; missing in Orange 91%, Ventura 100%) | yes | category | fine; labels available | CLEAN-12 |
| `typeconstructiontypeid` | construction material (4 values, 0.3% filled) | yes | category | fine; labels available | CLEAN-12 |
| `buildingqualitytypeid` | condition, "best (lowest) to worst (highest)"; LA only | yes | float ordinal; 2017 codes mapped onto the 2016 scale (agreement between files 0.8% before mapping, T5); after mapping 8 values (1, 4, 7, 10, 12 plus 6, 8, 11 on 8 rows), not the 5 levels the earlier REVIEW.md's issue 6 states | fine; wording fix in REVIEW (8 values, 3 rare); say "lower is better" in the note | CLEAN-21 applied; writing.md |
| **Rooms and baths** | | | | | |
| `bathroomcnt` | bathrooms incl. fractional | yes | float; 0 -> missing (claim 31; 0 zeros left) | fine | CLEAN-10 |
| `calculatedbathnbr` | bathrooms incl. fractional (dictionary text equal to `bathroomcnt`'s) | yes | float; equals `bathroomcnt` on 99.98% of rows, and `fullbathcnt + 0.5 x threequarterbathnbr` on 100% | cleaning problem, minor: a near copy of `bathroomcnt` | CLEAN-5 |
| `fullbathcnt` | full bathrooms | yes | float | fine | |
| `threequarterbathnbr` | 3/4 bathrooms (13% filled) | yes | float | fine | |
| `bedroomcnt` | bedrooms | yes | float; 0 -> missing where bathrooms also 0; 480 zeros left: 402 condominiums (land use 266), median 649 sqft, so studios | fine | CLEAN-10, CLEAN-11 |
| `roomcnt` | total rooms; LA records 0 for all (masked) | yes | float; 0 -> missing everywhere; 77% missing | fine | CLEAN-10 |
| **Living area** | | | | | |
| `calculatedfinishedsquarefeet` | total finished living area | yes | float; equals coalesce(sqft12, 15, 13, 6) on 100% of rows (a derived column, not a copy); 9 values below 200 sqft (2, 40, 66, ...) | fine; 9 implausible values could become missing (negligible) | CLEAN-11 (minor) |
| `finishedsquarefeet12` | finished living area | yes | float; equals the calculated area on 95.5% | fine (the calculated one is its coalesce, not a copy) | CLEAN-5 |
| `finishedsquarefeet13`, `finishedsquarefeet15`, `finishedsquarefeet6` | perimeter area; total area; base unfinished+finished area | yes | float, 96-100% missing | fine | |
| `finishedfloor1squarefeet`, `finishedsquarefeet50` | both "finished living area on the first floor" (Ventura only) | yes | float; equal on 99.5% of rows | cleaning problem, minor: near copy | CLEAN-5 |
| `basementsqft`, `storytypeid` | basement area; story type (only code 7, basement) | yes | float; bool presence | fine | CLEAN-13 |
| `numberofstories` | stories (LA none) | yes | float | fine | |
| `unitcnt` | units in the structure | yes | float (max 237) | fine | |
| `yearbuilt` | year built (1824-2016) | yes | float | fine | CLEAN-14 |
| **Lot, garage, outdoor** | | | | | |
| `lotsizesquarefeet` | lot area | yes | float; 36 below 500 sqft (condos), max 7.0M | fine | CLEAN-11 |
| `garagecarcnt` | garages / car spaces (LA none) | yes | float; 480 zeros (Orange), real "no garage" | fine | |
| `garagetotalsqft` | garage area | yes | float; **0 for 30.7% of Orange and 29.8% of Ventura garage records, of which 14,981 rows have 1-3 cars** (1 car: 7,082 of 11,304 are 0; 2 cars: 7,861 of 37,144) | cleaning problem: proxy missing (0 = area not recorded) | CLEAN-10 (Should) |
| `poolcnt` | pools (only 1 or nothing) | yes | bool | fine; 1,268 parcels gain a pool in the 2017 file (real) | CLEAN-13 |
| `poolsizesum` | pool area | yes | float, 1% filled | fine | |
| `pooltypeid7`, `pooltypeid2` | pool without spa; pool with spa | yes | bool | fine | CLEAN-13 |
| `pooltypeid10`, `hashottuborspa` | spa or hot tub; has hot tub or spa | yes | bool; recorded for about half as many parcels in properties_2017 (T5): a recording change between the train-heavy 2016 rows and the 2017 test windows | cleaning problem, minor (one meaning per column across years) | CLEAN-21 (Should) |
| `fireplacecnt`, `fireplaceflag` | fireplaces; fireplace present | yes | float; bool. The 368 flagged rows all lack a count, the 16,350 counted rows are all unflagged: two disjoint recordings of one fact | fine (keep both; a model can read either); note only | CLEAN-13 |
| `decktypeid` | deck (only code 66) | yes | bool | fine | CLEAN-13 |
| `yardbuildingsqft17`, `yardbuildingsqft26` | patio area; shed area | yes | float, 97-100% missing | fine | |
| **Tax** | | | | | |
| `structuretaxvaluedollarcnt`, `landtaxvaluedollarcnt`, `taxvaluedollarcnt` | assessed values of the own-year file (assessment year 2015 for 2016 rows, 2016 for 2017 rows) | yes (T2: no sign of the row's own sale) | float; total = structure + land on 99.999% (a derived column) | fine | LEAK-10 tested |
| `taxamount` | property tax of the assessment year | yes; in properties_2017 it is still the 2015-16 bill (T3) | float | fine; note that it lags the values by a year in 2017 rows | |
| `taxdelinquencyflag`, `taxdelinquencyyear` | taxes past due, and the year they were due; one snapshot of about Aug-Sep 2016 in both files (T1) | for every test row yes; post-sale only for the 72,157 training rows of Jan-Aug 2016 | bool; float years 1999-2015 (two-digit years expanded; flag and year always together) | fine for evaluation; wording problem in the definition (below, issue 1) | LEAK-10, USE-8 |
| Dropped | `parcelid` (id; 4,330 rows are repeat sales, near copies across the split 0.2-3.8%), `regionidcounty` (recoding of fips), `assessmentyear` (sale year - 1), `transactiondate` (day not known at the prediction point) | | | all correct | CLEAN-3, CLEAN-5, USE-3 |

No column holds a value created by the logerror itself, none is an id that encodes the label, and no column is blank
because of the outcome in a test row. The leak probe agrees (no feature or missing indicator alone above R^2 0.0).

**Problems, ranked (principles.md)**

1. **P4/P3, consistency of the delinquency note with the fit (LEAK-10, USE-8; Must, weak).** The definition calls
   `taxdelinquencyflag`/`taxdelinquencyyear` a "Potential leak, kept on purpose" while `fit = "direct"`; USE-8 names a
   potential leak kept on purpose as an *approximate* fit, so the two statements conflict. The measurement (T1)
   resolves it the other way: the snapshot (about Aug-Sep 2016) predates every test window (Nov 2016 onward), so no
   test row carries a post-sale value; the post-sale values (flag share 1.2-1.6% Mar-Aug 2016 against 3.1-4.7% after,
   the sale paying the arrears) sit in training rows only. That is a train-test shift in one column, not a leak into
   the evaluation. Mildest remedy: reword the bullet and `fit_reason` (b) to say so ("the snapshot predates every test
   window; for the Jan-Aug 2016 training rows it was taken after the sale, so their flag is lower; dropping both
   changes R^2 from 0.0069 to 0.0068") and keep `direct`. Alternative if the curator wants the training rows clean:
   set the two columns to missing for sales before September 2016 (a lag-style fix, LEAK-7).
2. **P4, overclaim on later edits for 2017 rows (LEAK-10; Should, weak, documentation).** `changes` and claim 22 say
   the own-year file "keeps later edits out". True for 2016 rows; properties_2017 was released in October 2017, after
   every 2017 sale, so the 6 test windows of 2017 use a post-sale snapshot (T4). Measured scale small (facts change
   rate 3.2-3.7% over a year, slight fall with the sale month; living area changed for 69 of 60,472; tax values show
   no reset for 2017 sales, T2). Remedy: a sentence in `curation_comments` (LEAK-11-style note: post-sale edits
   possible in 2017 rows, measured rare); no data change. If the curator wants it stricter, the alternative (taking
   properties_2016 for 2017 sales) brings the 2016 sale reassessments of T2 in, which is worse.
3. **P7, `garagetotalsqft` zeros as missing (CLEAN-10, Should).** 14,981 rows carry 0 sqft with 1-3 garage spaces (all zeros: Orange 11,958,
   Ventura 3,500; 30% of each county's garage records), i.e. a garage that exists with no recorded area. Remedy: mask
   `garagetotalsqft == 0 & garagecarcnt > 0` to missing in `_clean`, one line next to the room-count masks; keep the
   479 rows with 0 cars and 0 sqft.
4. **P7, recording change of `pooltypeid10` and `hashottuborspa` between the files (CLEAN-21, Should).** About half
   of the 2016 spa/hot-tub entries are absent in properties_2017 (T5), so the share halves exactly at the 2016/2017
   boundary where most test windows sit. Effect on scores likely negligible (2% of rows). Mildest remedy: a note;
   cheap fix: for 2017 rows, OR the flag with properties_2016 (pre-sale, so allowed).
5. **P7, near copies (CLEAN-5, Should).** `calculatedbathnbr` = `bathroomcnt` on 99.98% of rows;
   `finishedsquarefeet50` = `finishedfloor1squarefeet` on 99.5%; `censustractandblock` = `rawcensustractandblock` on
   its leading digits for 98.9%. Not exact copies, so keeping them is defensible; remedy: drop the three or write one
   line why they stay (they differ on a few rows).
6. **P7, code labels (CLEAN-12, Should).** The data dictionary's tabs give labels for `airconditioningtypeid`,
   `architecturalstyletypeid`, `buildingclasstypeid`, `heatingorsystemtypeid`, `propertylandusetypeid`,
   `storytypeid`, `typeconstructiontypeid`; the definition keeps numeric codes and reads no code from the dictionary.
   Remedy: map codes to labels (a lookup; no information change for trees). Low priority.
7. **P7, small items.** 9 living areas below 200 sqft (2, 40, 66 ...) could become missing (CLEAN-11, negligible);
   `buildingqualitytypeid` has 8 values after mapping, not 5 (the earlier REVIEW.md's issue 6 wording), and its direction
   (lower is better) belongs in the note; `latitude`/`longitude` are degrees x 1e6 (cosmetic).

Not problems: tax values (T2, checklist draft issue 3 closed with evidence), `taxamount` staleness (T3, pre-sale),
`bedroomcnt` zeros (studios), `fireplaceflag` vs `fireplacecnt` (disjoint recordings), all dropped columns,
`transaction_month`.

</details>

<details><summary>Split audit</summary>

**Verdict: right with notes.** Temporal, 9 one-month windows (Jul 2017 back to Nov 2016), expanding train side, a
one-month gap. No Must of SPLIT or USE-10 is broken; the notes are Should-level choices, all kept.

Numbers: the rebuilt frame, the raw sales files, and an L1 LightGBM (300 trees, seed 0, R^2 skill against the
train mean). Thread caps on every run.

**What was checked**

| Check | Result |
|---|---|
| Regime (SPLIT-1, SPLIT-3, USE-10) | Temporal is right. Zillow scores every home every month; the future sales are whatever homes sell, mostly ones with no earlier sale in the data. Test rows whose parcel sold in an earlier training month: 2.9-3.8% (2017 windows), 0.2-0.7% (Nov/Dec 2016). A known parcel's history would be legitimate (known entity), and `parcelid` is dropped anyway. No grouping needed. |
| Time column | `transaction_month` = first day of the sale month = the prediction point (Zillow pairs the sale with that day's Zestimate). The accepted `meta_time_horizon_mismatch` is correct: each window is one date. |
| Windows and sizes (SPLIT-14, -15, -17) | Verified: test Jul..Jan 2017 = 9,484 / 11,448 / 10,481 / 8,676 / 9,323 / 6,408 / 7,015; Dec 2016 1,739; Nov 2016 1,826. Train shares 0.863 down to 0.534 (claim "53%" holds; >= 50%). 9 windows, all > 50 rows. |
| Train side / history (SPLIT-11, SPLIT-20) | Expanding from Jan 2016. The five newest windows train on >= 12 months (a full season); the oldest four on 8-11 months. No break in the history except the Kaggle sub-sampling after 15 Oct 2016 (below). |
| Gap vs label delay (SPLIT-9, SPLIT-10) | Train ends one full month before the window (Jul window: train to May). Delay evidence from the 2 Oct 2017 release: Aug 2017 9,936 rows (95% of Aug 2016's 10,476; Jul 2017 9,490), Sep 2017 4,801 (~half). So most labels arrive within a month; the one-month gap is mildly conservative, and no training row has a label unknown at the window start. Cost of the gap: mean skill 0.0053 (gap 1) against 0.0059 (gap 0), 9/9 wins in both. |
| Season | Monthly mean logerror 0.007-0.022, higher in winter (Dec-Feb 0.019-0.022) than in spring (Apr-May 0.007-0.011). Windows cover Nov-Jul; none in Aug-Oct, but none is all one season either. Train-mean vs test-mean RMSE differ by <= 0.0003 per window: the drift is tiny next to RMSE 0.14-0.19. |
| Hidden groups / near copies | Probe: no entity-like column (only `propertycountylandusecode`, a feature new rows keep, SPLIT-4). Near copies at 0.85: 15.3% of test rows have one in train (units of one building, the same parcel in both property files); under a temporal split with known buildings this is legitimate (SPLIT-13). |

**Notes, ranked (all P4, SPLIT, Should; none needs a change)**

1. **Horizon (SPLIT-12, SPLIT-19, Should).** The competition's horizon was 1-3 months after a data cut whose newest
   month was partial (predict Oct, Nov, Dec 2017 from the 2 Oct release). The shipped design predicts the month after
   a one-month gap, i.e. two months after the last training month: inside the source's range, and the monthly refit
   matches the use case ("before a month starts"). The alternative, 3 windows of 3 months with gap 1 (31,413 /
   24,407 / 10,580 test rows), gives mean skill 0.0044 (3/3 wins) against 0.0053 (9/9). Per SPLIT-21 this comparison
   decides nothing; it shows only that the signal does not hinge on the choice. Mildest remedy: none; state in
   `splits_comment` that the competition predicted up to three months ahead and the monthly windows are the refit
   cadence (curator's weighing call, REVIEW issue 4).
2. **The gap is slightly larger than the measured delay (SPLIT-10, Should).** The `splits_comment` says the release
   "lacked part of the two newest months"; by count, Aug 2017 is ~95% complete and Sep ~50%, so the delay is mostly
   under one month (Aug's rows are, however, a biased share: twice the |logerror| > 1 rate). A gap of one month is the
   right rounding for whole-month windows; it costs 0.0006 skill. Keep. Optional wording fix: "lacked half of the newest
   month and a biased part of the one before".
3. **The two oldest windows are Kaggle's remnant sample (SPLIT-17, Should; noise, not bias).** Nov and Dec 2016 hold
   1,826 and 1,739 rows, ~18% of a normal month, because Kaggle held the rest out for its public leaderboard (weekly
   counts drop from ~2,100 to ~450 after week 41 of 2016). They are above the 50-row floor, and the curation note finds
   the share random, but they are noisier (Dec 2016 RMSE 0.190 against 0.140-0.173 elsewhere) and carry 1/9 of the
   weight each. Keep; optional: note in `splits_comment` that these two windows are sub-samples.
4. **Training sides of the oldest windows lack a full season (SPLIT-20, Should).** Windows Nov 2016 - Feb 2017 train
   on 8-11 months, so the winter months in test have one or no winter month in train. This follows from the data
   starting in Jan 2016; the 50% floor and 9 windows leave no better choice. Keep.

**Outside the split (for the leak auditor, not decided here)**

Each sale takes the property file of its year; `taxdelinquencyflag/year` are a ~Aug-Sep 2016 snapshot, after the sale
for Jan-Aug 2016 training rows (curation note, LEAK-10). The test rows of 2017 likewise use properties_2017, whose
extract date may postdate the sale month. The split does not change this.

</details>

<details><summary>Domain practitioner</summary>

Actor: a data scientist on Zillow's Zestimate team (the source's own actor: "improve the Zestimate", Kaggle Zillow
Prize round 1). Decision: before a month starts, decide for which homes, and by how much, the published Zestimate will
miss the sale price, so the estimate can be corrected or the home flagged for review.

**Fit: approximate (the dataset says direct)**

One-sentence reason: the rows, prediction point and monthly split mirror the round-1 task, but the shipped data keeps a
potential leak on purpose (tax delinquency, which USE-8 names as approximate, case kick), lacks the one input Zillow
always holds when it models its own residual, the Zestimate itself (USE-6), and the target is a diagnostic proxy whose
variance is mostly miskeyed prices that nobody acts on (USE-5).

**1. Inputs at the prediction point (USE-3, USE-6)**

What I have and the data gives me: the county assessor facts (location, size, rooms, quality, age, lot, pool, garage),
the assessed tax values of the previous roll, and the sale month. All of these are known on the first of the month.

- Assessed values: `assessmentyear` is 2015 in properties_2016 and 2016 in properties_2017 (my check), so each sale sees
  the roll of the year before its sale: known in time. The median ratio of the 2017 to the 2016 tax value is 1.015 for
  every sale month of 2016 and 2017, so no sign that the 2016 roll carries 2016 sale prices into the rows. (Minor
  wording point for the claim auditor: `assessmentyear` is the sale year minus one, not "the sale year".)
- Building facts in properties_2017 for 2017 sales: the share of parcels whose facts changed between the two files is
  flat over the 2017 sale months (2.0-2.4%, against 2.1% for parcels sold only in 2016), so I see no post-sale edits in
  the 2017 rows.
- What I would NOT have: `taxdelinquencyflag`/`taxdelinquencyyear` for January to August 2016 sales, a snapshot taken
  after those sales (the definition says so; 1.5% flagged against 3.1-4.7% later). Harmless to skill, but a known leak
  kept on purpose.
- What I would ALWAYS have and is missing (USE-6, largest gap):
  - the Zestimate on the first of the month (the number the target is the error of); a residual model without its
    own forecast is "predict the error without knowing the estimate" (the bias_correction precedent: the forecast the
    task corrects is the input);
  - the listing data: list price, days on market, listing description/photos, MLS facts. List price is the strongest
    single predictor of sale price and hence of the Zestimate's miss for homes on the market;
  - the parcel's last sale price and date from the county deed records, and the Zestimate's own history.
  None of these were released (round 1 withheld them on purpose), so this gap cannot be fixed by curation; it has to be
  named in the fit.
- Previous outcome of a known entity (USE-10): 2,669 parcels sell more than once; only 1.4% of the rows have an
  earlier sale more than 62 days before, with Spearman -0.15 between the two logerrors.
  Dropping `parcelid` loses almost nothing; not worth adding.

**2. Target (USE-5)**

- What I act on is the home's value (Zillow's round 2 switched the target to the sale price itself and the round-2
  score top-coded the error). The log error is a diagnostic: it is the gap between a model and a recorded price, so it
  moves when the Zestimate model is retrained (target drift that no feature sees, consistent with the
  `drift_baseline` flag).
- 2.1% of the rows beyond |0.4| hold 74% of the squared error and are mostly data errors (miskeyed prices, non-arm's-
  length transfers). Nobody "acts" on those; what I would want is either the error on clean arm's-length sales, or a
  probability that a sale's error exceeds a threshold (a flag for review). As shipped, RMSE mostly scores how a
  model handles recording errors; the competition scored MAE (REVIEW issue 1). I would take MAE, or keep the target
  clipped at +-0.4 as in round 2 if the metric must stay RMSE.
- Number, not class: a number is right for the round-1 use, but a classification "|logerror| > 0.1" is the version a
  review team would use.

**3. Row and test data (USE-1, USE-10)**

- One row = one sale = one evaluation of one Zestimate. Zillow publishes estimates for all ~3M parcels but can only
  score them on sales, so evaluating on sales is how Zillow itself measures the Zestimate: matches.
- Test = next month's sales, trained on all sales up to the month before (one-month recording gap). This is what I
  would face. The competition horizon was 1-3 months after the data cut-off; a one-month gap is the short end but
  reasonable. Nine windows from November 2016 on are fine.
- Known homes, not cold start: correct as a temporal split, no grouping needed (USE-10).
- August and September 2017 dropped: right (Zillow calls them a biased sample).

**4. Would I use the model?**

No, not for the Zestimate: R^2 0.003-0.021 (robust LightGBM, 9 of 9 windows), and the untuned probes lose to the mean
(no_signal, unstable; L2 LightGBM wins 4 of 9 windows). Without the Zestimate and the listing data the model sees only
what the Zestimate already used, so the remaining signal is where the Zestimate is systematically biased by area or
property type. I would trust it only if the gain over the training median held per window in MAE and survived on
the sales with |logerror| < 0.4. As a benchmark it is a legitimate real task (a company residual on facts on file),
testing heavy-tailed, near-noise regression with drift; that is a fair task but not a direct mirror of Zillow's work.

**Gaps, ranked by how much they change the task**

1. The Zestimate (and listing data, last sale price) missing as inputs (USE-6). Zillow always has them; without them
   the task is "find where the Zestimate is biased from public assessor facts". Unfixable from the source; name it in
   `fit_reason`.
2. Target proxy with recording-error tails scored by RMSE (USE-5). The metric choice decides whether the benchmark
   ranks robustness to miskeyed prices or skill on real misses. MAE (source metric) or clipping at +-0.4.
3. Potential leak kept on purpose: tax delinquency snapshot after the January-August 2016 sales (USE-8, case kick:
   "a potential leak kept on purpose" is approximate). Alone this sets the fit to approximate; dropping both columns
   would cost nothing (R^2 0.0069 vs 0.0068) and would remove the reason.
4. Target drift from Zestimate model updates (USE-5): no feature captures the model version; a monthly refit handles
   it, which the split already does.
5. Previous outcome of repeat-sold parcels not offered (USE-10): 1.4% of rows, weak relation; negligible.

**What a domain expert would change**

- Set `fit = "approximate"` and write in `fit_reason` that the Zestimate and the listing data, which Zillow has at the
  prediction point, were not released (USE-6, USE-8).
- Either drop `taxdelinquencyflag`/`taxdelinquencyyear` (no skill lost; then the leak no longer counts against the
  fit) or keep them and leave the fit approximate (USE-12, USE-8).
- Score with MAE as the competition did (task_probes rule 6 precedent `allstate_claims_severity`), or ship RMSE on the
  round-2 style clipped target; the current RMSE mainly measures robustness to data-entry errors.
- Keep: per-year property files, the monthly windows with a one-month gap, the August-September 2017 drop, the
  sale-month prediction point.
- USE-9 does not rescue a direct fit: every nearby use case (an iBuyer or lender flagging homes whose automated value
  is off) also needs the automated value as input, so a rephrasing would only excuse the gap.

**Sources**

- Dataset definition and README: datasets/_dev/tabarena-v0pt2/zillow_prize/dataset.py, README.md; record
  curation/records/zillow_prize.md; the panel's claims, the earlier REVIEW.md, the task and leak probes and the robust
  LightGBM windows.
- Rules: .claude/skills/knowledge-curation/references/use_case.md (USE-3, USE-5, USE-6, USE-8, USE-9, USE-10, USE-12).
- Kaggle Zillow Prize round 1: https://www.kaggle.com/competitions/zillow-prize-1 (page not readable through fetch;
  content via the definition's quotes of the Data, Evaluation and FAQ pages).
- NYC Data Science Academy write-ups of the competition (target definition, MAE scoring, round 2 on sale price):
  https://nycdatascience.com/blog/student-works/machine-learning/zillow-prize-competing-improve-zestimate ,
  https://nycdatascience.com/blog/student-works/data-study-on-the-zillow-zestimate-kaggle-competition
- My checks on the raw files: assessment years, fact edits by sale month, tax ratios, repeat sales.

</details>

<details><summary>Blind review</summary>

**Verdict: exclude.** The target is the residual of Zillow's own model and has almost no learnable signal: tuned LightGBM gets R2 <= 0.007 on a temporal holdout, and a handful of outliers decide the squared-error score. A benchmark score here would mostly measure noise and how a method handles the tails, not tabular learning.

**What the task is**
logerror = log(Zestimate) - log(SalePrice) for homes sold in 2016-2017 in LA, Orange and Ventura counties (Kaggle Zillow Prize round 1). Zillow wanted to know where its Zestimate goes wrong so it could improve it, which is an internal model-diagnostics use. That use is real for Zillow, but the Zestimate itself is not among the features. So the task asks you to predict the error of a model you cannot see, from the same property attributes that model already used. Little systematic error is left. This is known from the competition: leaderboard MAEs were bunched around 0.074-0.075, barely below a constant.

**Concerns, most serious first**

1. **Almost no signal, and the score is driven by outliers (main reason to exclude).**
   - Training up to 2017-03 and testing on 2017-04..07: L2 LightGBM R2 = 0.004-0.007 when regularized, and -0.002 with default-ish settings. An L1 model gets MAE 0.0666 against 0.0671 for a constant median, a 0.7% gain.
   - Testing on 2016-10..12: L1 MAE 0.0650 against 0.0660 for the median; the L2 model is worse than the constant.
   - The target has kurtosis 128 and ranges from -4.66 to 5.26. The top 1% of rows carry 64% of the squared error.
   - The method ranking under RMSE would come from how methods treat a few hundred extreme rows. I see no change to the data that fixes this. The only options would be to switch the metric to MAE, clip the target, or redefine the task, and none of them makes it a good benchmark task.

2. **The test windows are not a clean temporal shadow of the competition.**
   - Monthly counts fall from about 10k to 4,977 / 1,826 / 1,739 for Oct, Nov and Dec 2016. Kaggle held most Q4-2016 sales back for its own test set, so these windows are a non-random subsample.
   - 2017 stops in July.
   - The 2016 and 2017 rows come from different property snapshots. The median taxamount/taxvalue ratio is 0.0126 in 2016 and 0.0123 in 2017, and the share of round ($1000-multiple) tax values is 16% against 13.5%. That gives a shift at the year boundary.
   - What I would change: if kept, document this, and avoid test windows in Q4 2016.

3. **Possible leak through tax values (not verified).**
   - Under California Prop 13, a sale triggers reassessment to roughly the sale price. If any row's property snapshot is dated after its sale, taxvaluedollarcnt encodes the denominator of the target.
   - Signs in the data: rows with a round tax value have mean |logerror| 0.056, against 0.071 for the others. One repeat-sold parcel had taxvalue 177,418 in its 2016 row and exactly 350,000 in its 2017 row, with the same taxamount.
   - The 2016/2017 tax ratio shift suggests the per-year files were matched to the right year, which is correct. Even so, the Kaggle discussions reported a leak from 2017 tax values for 2016 sales. I could not open the Kaggle data page (it renders empty) to confirm the snapshot rule.
   - What I would change: confirm the 2016 rows use properties_2016 and the 2017 rows use properties_2017.

4. **Repeat sales and duplicates, with no parcel id to group on.**
   - There are 7 exact duplicate rows and 431 rows whose features are identical to another row (target aside).
   - 7,775 lat/long/tract keys appear more than once. parcelid was dropped, so a temporal split cannot keep the same parcel out of both train and test, and repeat sellers (flips) can show up on both sides.
   - Some lat/long are rounded (for example 33354200/-118331000 repeats with different houses), so I could not dedupe reliably.
   - What I would change: keep parcelid as a group key and drop the exact duplicates.

5. **Preparation details (minor).**
   - The identifier-like columns fips, propertylandusetypeid and regionidcity/zip/neighborhood are stored as numeric (int or float) rather than categorical.
   - censustractandblock duplicates rawcensustractandblock.
   - propertyzoningdesc has 2,292 levels and takes most of the split gain, a likely overfit route.
   - Several columns are 99-100% missing: buildingclasstypeid, finishedsquarefeet13, basementsqft, architecturalstyletypeid.
   - Converting the *typeid flags to bool (decktypeid, pooltypeid*, storytypeid) is fine.
   - Lat/long are scaled by 1e6, which is fine.

6. **Licence.** Kaggle competition data falls under the competition rules, which generally limit use to the competition and non-commercial research. Redistributing it inside a benchmark needs checking.

**What I could not check**
- The Kaggle data page and forum: whether properties_2016/2017 were matched by transaction year, and the official note on the tax-value leak.
- Exact parcel identity, because parcelid is absent.
- The licence terms in full.
- How the 9 split windows are defined. I reproduced 2 temporal cuts of my own.

Source: https://www.kaggle.com/competitions/zillow-prize-1 ; press coverage (https://zillow.mediaroom.com/2017-05-24-Zillow-Launches-1-Million-Zestimate-Competition-for-Data-Scientists) confirms logerror = log(Zestimate) - log(SalePrice).

</details>

<details><summary>Precedent check</summary>

Scope: the choices of `datasets/_dev/tabarena-v0pt2/zillow_prize/dataset.py`, the record
`curation/records/zillow_prize.md`, and issues 1-8 of the earlier REVIEW.md. The record holds **no CC line**. Its
comments are unprefixed screening notes plus two AI assessments (2026-10-07, 2026-10-20). So nothing here is a curator
decision yet, and there is no drift of the curator's own calls on this dataset. The precedent register has 4 flags (few_minority, one_feature, trivial: opposite outcomes; scaling over all rows: drift).
None of them touches zillow_prize or a house-price dataset. zillow appears only as open issues and the 2026-10-20
priority assessment under `no_signal`, `drift_baseline` and `unstable`.

Status of the sibling precedents: house_sales, house_prices_nominal, melbourne_housing_market and perth_house_prices are
AI drafts with open REVIEW.md issues. Curator decisions in the family are california_house_prices_2020 (CC 2026-09-30,
2026-10-06, 2026-10-14, Lennart) only. The house_sales precedent report
already cites zillow as the source-based precedent for the gap (its decision 4) and the zero-as-missing rule (its
decision 10).

**Summary**

| # | Decision | Rule | Result |
|---|---|---|---|
| 1 | Building facts and tax values from the property file of the sale's year (still a post-sale lookup for most rows) | LEAK-10 (Must), Mechanisms row "property's current record for a past sale" | **departs without a stated reason** for the in-year remainder; the data probably supports a melbourne-style keep |
| 2 | `fit = "direct"` with a `Potential leak, kept on purpose:` bullet | USE-8 (Must) | **not reasonable under the ranking as written** (USE-8 lists a kept potential leak under Approximate) |
| 3 | Tax delinquency snapshot kept because dropping it "changes nothing" | LEAK-6, LEAK-11 | consistent in outcome (african_credit_scoring_challenge, melbourne); third case of an unwritten reason, amendment candidate |
| 4 | Metric RMSE, the competition's MAE in the notes (issue 1) | TP-6 (Must) vs definitions.md "Field mapping" | follows the house rule and dataorg / african_credit; part of the open cross-cut in `tabarena-v0pt2/REVIEW.md` |
| 5 | Small signal kept, tuned results missing (issue 2) | TP-1 (Must), TP-2 (Should) | consistent (sf_permit_time, bias_correction kept pending tuned results); closest fact pattern forest_fires |
| 6 | Extreme logerror rows kept | CLEAN-11, USE-7 | consistent, with a stated distinguishing fact against california (2026-10-14) and house_prices_nominal |
| 7 | `transaction_month` (first day) as the time column; accepted `meta_time_horizon_mismatch` (issue 3) | LEAK-1, USE-3 | consistent (perth_house_prices, same accepted warning) |
| 8 | 9 monthly windows, gap of 1 month (issue 4) | SPLIT-10, SPLIT-12, SPLIT-15, SPLIT-19 | consistent, with a stated reason; the pair with house_sales goes the other way and is house_sales' to answer |
| 9 | August-September 2017 dropped (issue 5); thinned Oct-Dec 2016 kept | EV-5, LEAK-22 family | consistent (house_sales May 2015, house_prices_nominal July 2010; Ames June 2010 kept) |
| 10 | `buildingqualitytypeid` mapped onto the 2016 scale (issue 6) | CLEAN-21 (Should) | departs in method (a mapping read off the data, not a published one), with a stated reason; minor |
| 11 | Census tract-and-block numbers stay numeric | CLEAN-14 (Should) | departs without a stated reason; precedent brazilian_ecommerce gives one; minor |
| 12 | Zeros as missing in rooms, bathrooms, bedrooms-with-no-bathrooms | CLEAN-10, CLEAN-11 | consistent (house_sales, churn_telco_south_asia) |
| 13 | Repeat sales kept, those within 31 days dropped; duplicates kept | LEAK-17, LEAK-20, SPLIT-13 | consistent (melbourne, house_sales) |
| 14 | 24 sales without home facts dropped | CLEAN-11 / USE-7 | consistent (follows the source, discussion 34667) |
| 15 | Drops `parcelid`, `regionidcounty`, `assessmentyear`, `transactiondate` | CLEAN-3, CLEAN-5 | consistent |
| 16 | Licence "no redistribution", noted only (issue 7) | SEL (selection.md, licence: no reason, no marker) | consistent |
| 17 | BibTeX `{Zillow}` (issue 8) | PROV-10 | consistent with the other Kaggle competition entries |

**Per decision**

**1. The property file of the sale's year: departs from LEAK-10 without a stated reason (in-year remainder)**

LEAK-10 (Must) excludes "attributes looked up after the outcome (a property's current record for a past sale), unless
the data shows they did not change". The Mechanisms table in `leak_checks.md` gives two precedents:

* house_sales ("the King County lesson"): the record changed after 2,151 of 20,967 sales, and the post-sale values
  flatter the model (RMSE 0.156 against 0.208 on those rows). The fix was a rebuild from the county's change log (AI
  draft, issue 1).
* melbourne_housing_market: kept, because the looked-up `Bedroom2` equals the sheet's `Rooms` in 98-100% of the rows
  of each window, and blanking the mismatches changes the error by 0.0004 (AI draft, `fit_reason`).

zillow's definition takes each sale's row from properties_2016 or properties_2017. The notes say this "keeps later
edits out". It keeps out only the edits made after the year's snapshot, not those between the sale and that snapshot.

* properties_2017 was released with the round-1 data in October 2017. It is a post-sale lookup for every kept 2017
  sale (January-July 2017).
* The definition itself dates the 2016 delinquency snapshot to about August-September 2016. If properties_2016 is of
  that date, it is a post-sale lookup for the January-August 2016 sales.
* The 2026-10-07 assessment measured the mechanism. Building facts differ between the two files for 1.2-2.0% of the
  parcels sold January-May 2016, against 0.81% of unsold ones. Records change more often after a sale, as in King
  County, but about 98-99% stay the same. That is the melbourne range.

So the facts likely support a keep under LEAK-10's "did not change" clause. But neither the definition nor `fit_reason`
says so: no share of changed rows for the 2017 sales, and no effect measured. The only post-sale remnant the
definition names is the tax delinquency (decision 3). The checklist's draft issue 3 (2016 tax values for late-2016
sales) is the same question for the tax columns.

Decisive experiment, for the column or leak auditor: compare properties_2016 and properties_2017 for parcels sold
January-July 2017 against parcels sold only in 2016. Then refit with the changed building columns set to missing for
the affected 2017 rows, as melbourne did.

```text
**Consistency check (AI, 2026-10-20):** your call on zillow_prize (each sale takes the property file of its year,
which for most sales is still a lookup after the sale, kept without a note; LEAK-10) differs from house_sales (the
record rebuilt as of the sale, 2026-10-20 draft) and leans on melbourne_housing_market (kept because 98-100% of the
looked-up values match) without measuring it. What sets zillow_prize apart?
(a) the data shows the facts did not change: about 98-99% of sold parcels have the same building facts in both
files (assessment 2026-10-07), and Zillow publishes no change log to rebuild from; write that share and its effect
on the error into the notes as melbourne does (LEAK-10's own clause, no exception needed);
(b) treat it like house_sales: set the building facts that differ from the earlier file to missing for the rows
sold before the later snapshot;
(c) reopen house_sales to keep its file values; (d) amend LEAK-10 for released property snapshots.
```

**2. `fit = "direct"` next to a kept potential leak: not reasonable under the ranking as written**

USE-8 (Must) lists under Approximate "a potential leak kept on purpose", with kick as its case. The definition's
bullet is literally `Potential leak, kept on purpose:` (tax delinquency), yet `fit = "direct"`.

* Post-outcome or unverified fields kept with that bullet are `approximate`: kick, homesite_quote_conversion,
  african_credit_scoring_challenge (no measurable effect, 0.635 vs 0.639: the closest fact pattern),
  churn_telco_south_asia (CC 2026-10-15, Lennart).
* Datasets with a `direct` fit and the bullet are the LEAK-30 all-row scaling cases (bioresponse, cooking_time_1m,
  delivery_eta_1m, maps_router_eta_1m, lung_cancer_epithelial_genexp, qsar_bioconcentration).
* The house-price siblings melbourne, house_sales, house_prices_nominal and perth all say `direct` with post-sale
  remnants. The house_sales report (its decision 16) flags the same family tension.

A departure from a Must cannot be an exception, so the choice is an amendment or a change of the fit.

```text
**Consistency check (AI, 2026-10-20):** your call on zillow_prize (fit `direct` with a "Potential leak, kept on
purpose" bullet; USE-8, a Must, lists that under Approximate) differs from african_credit_scoring_challenge (fit
`approximate`, the same kind of post-pull snapshot with no measurable effect, 2026-10-07). What sets zillow apart?
(a) the delinquency snapshot only weakens the signal (sold homes lose a flag the sale cleared), so it is a LEAK-11
note, not a potential leak: reword the bullet and keep `direct` (no rule change needed);
(b) treat it like african_credit: `fit = "approximate"`;
(c) reopen african_credit to `direct`; (d) amend USE-8 so that a kept field with no measurable effect does not
make the fit approximate.
```

**3. Tax delinquency kept because dropping it changes nothing: consistent in outcome, third case of an unwritten reason**

The measured effect is R^2 0.0069 with the field and 0.0068 without. The mechanism, a lower flag share before the
snapshot (1.2-2.5% against 3.1-4.7%; checklist), most likely blanks information for sold homes. That fits LEAK-11
(Should; narrows LEAK-10): a post-outcome value that weakens the signal stays with a note. Its precedent is
south_africa_coronary_heart_disease (CC 2026-10-01, Lennart).

Three AI drafts keep a post-outcome lookup on the same reason, "removing it does not change the score":

* african_credit_scoring_challenge (2026-10-07: 0.635 against 0.639);
* melbourne_housing_market (blanking changes the error by 0.0004);
* zillow_prize.

LEAK-6 (Must) says "a confirmed leak goes even when small". None of the three is settled by the curator. This is the
"third exception of the same kind" signal of principles.md. Proposal: amend LEAK-11, or add a rule, to read "a
post-outcome lookup with no measurable effect stays with a note naming the effect", so these stop being argued one
by one. That is for the curator; it also settles decision 2's wording.

**4. Metric RMSE, the competition's MAE in the notes: follows the house rule; part of an open cross-cut**

* definitions.md ("Field mapping"): "A competition with its own metric keeps our default, and the notes name the
  original metric". zillow follows it. So do dataorg_financial_health_prediction_challenge (F1 at the source, log
  loss kept) and african_credit_scoring_challenge (F1 at the source, ROC AUC kept).
* TP-6 (Must) names "the scoring it uses" as a better version that replaces ours. allstate_claims_severity (`mae`,
  though on a log target, so not the competition's metric either), 5g_energy_consumption (`mape`), amex_non_iid_1m,
  porto_seguro and sepsis_prediction_1m set their own metric.
* None of these is a dated curator decision. The cross-cut is already filed in
  `datasets/_dev/tabarena-v0pt2/REVIEW.md` ("TP-6 and definitions.md disagree on a competition's metric", force_2020
  panel, 2026-10-20). Its proposed criterion is that a competition metric replaces ours "when it scores what the use
  case needs and can rank the models' outputs". MAE meets both, so under that amendment zillow would switch to MAE.
* nyc_taxi_trip_duration matched its competition's RMSLE through the target transform. No such transform turns RMSE
  into MAE. Top-coding at +-0.4, Zillow's round-2 score, changes the target, and TP-6 says a fix of our own invention
  is no better version.

No separate prompt: the answer belongs to the cross-cut, and zillow should be listed there as a case that the
amendment would flip. Note that the adapter falls back to RMSE (`BENCHMARK_CHANGES_TODO.md`, "Dataset-specific
metrics"). That is a tooling limit, not a curation reason.

**5. Small signal kept without tuned results: consistent**

* TP-2 (Should) keeps a small real signal. TP-1 (Must) asks for the tuned check.
* Precedents kept pending tuned results: sf_permit_time (2026-10-12, "no tuned results in the cache, re-check") and
  bias_correction_r_bias_correction_r_2 (2026-10-07/15). african_credit (2026-10-07) is another.
* The closest fact pattern is forest_fires (CC 2026-10-06, Lennart): a heavy-tailed regression target where every
  untuned model lost to the mean, kept because tuned TabPFN-3.5 beat it on 26 of 32 folds.
* zillow differs from the pending-tuned precedents in one fact: the untuned L2 fits lose to the mean (4 of 9 windows),
  and only L1 or Huber fits win. Those precedents beat the dummy untuned. the earlier REVIEW.md's issue 2 already makes the keep
  conditional ("if they do not, this is a `TBD -> 2nd Tier` case"), which matches the precedents.
* Factual note for the claim auditor: today's re-run gives Huber 8 of 9, not 9 of 9. `fit_reason`'s "all nine
  windows" holds for L1 only.

**6. Extreme logerror rows kept: consistent, with a stated distinguishing fact**

* california_house_prices_2020 (CC 2026-10-14, Lennart) dropped 2,480 rows whose listing describes another sale.
  Those rows are identifiable non-task rows (USE-7).
* house_prices_nominal drops 3 partial sales on the source's own word (De Cock, p. 4).
* zillow's extreme rows cannot be identified row by row: Zillow says "mostly" miskeyed prices, and the file has no flag.
  The competition's test kept them, and CLEAN-11 keeps values that are only unusual.

Both siblings follow their source, and so does zillow. The metric question (decision 4) is where the weight of these
rows bites, not the row decision.

**7. `transaction_month` and the accepted warning: consistent**

* The prediction point follows the source: Zillow pairs each sale with the Zestimate of the month's first day (FAQ),
  LEAK-1 and USE-3.
* perth_house_prices accepts the same `meta_time_horizon_mismatch` warning for the same reason (a first-of-month date).
* Side finding: house_prices_nominal's REVIEW issue 4 says its prediction point "a house sells" is "as in house_sales
  and zillow_prize". zillow's point is the first day of the sale month, so that cross-reference is inexact. It is for
  house_prices_nominal's panel.

**8. Monthly windows with a one-month gap: consistent, with a stated reason**

* SPLIT-10 (Should) asks for a gap of about the label's delay. zillow's reason comes from the source: Zillow receives
  the sales from the county recorders with a delay, and its 2017 release lacked part of the two newest months.
  Precedents: brazilian_ecommerce (gap of one month, 2026-10-15, Lennart) and sf_permit_time (6 months).
* house_sales, house_prices_nominal, melbourne and perth use no gap. The house_sales report already raises that pair
  as house_sales' departure (the same county-recording mechanism, 24% of a month recorded by mid-month). zillow is the
  one with the source fact, so no prompt here.
* SPLIT-15: 9 windows, as an IID task of this size gets folds. SPLIT-14: oldest train side 53%. SPLIT-17: the smallest
  windows are 1,739-1,826 rows.
* SPLIT-12/SPLIT-19: the competition scored a 3-month horizon (October-December 2017). The definition argues per month
  from Zillow's "one prediction per home and month". That is a reasonable reading. REVIEW issue 4 offers the 3 x 3
  months alternative. Of the house-price family, zillow is the only window length taken from the source (house_sales
  report, decision 5).

**9. August-September 2017 dropped; the thinned October-December 2016 kept: consistent**

* Same direction: house_sales drops May 2015 (extract cut mid-month, 24% coverage, AI draft) and house_prices_nominal
  cuts from July 2010.
* zillow's fact is stated and measured: the source calls the months "a biased sample", and they hold twice the share
  of |logerror| > 1.
* The thinned late-2016 months (public-leaderboard holdout) are kept with a measured "looks random" share (2.2% vs 2.0%).
  That parallels house_prices_nominal's June 2010, kept with the cause unknown.

**10. `buildingqualitytypeid` harmonised: departs from CLEAN-21's method, with a stated reason; minor**

CLEAN-21 (Should; college_scorecard, Lennart 2026-10-16) puts a changed scale on one scale "with the conversion the
source or the measuring body publishes". Zillow publishes none. The definition reads the map off the parcels in both
files (crosstab decision table) and shows it is a many-to-one map. The fact that sets it apart is stated: no published
conversion exists, and the data shows a deterministic map. LightGBM R^2 is within 0.001 for raw, mapped or dropped.
That makes it a reasonable exception to the method clause. If kept, record it as
`**Exception to CLEAN-21 (date, curator):** no published conversion; the map is read off parcels in both files. Serves
P7.`

Wording only (checklist): after mapping the column holds 8 values (3 rare), not the 5 levels issue 6 states.

**11. Census tract-and-block numbers stay numeric: departs from CLEAN-14 without a stated reason; minor**

CLEAN-14 (Should): categorical for a fixed set of codes, string for high cardinality. The definition makes every other
location code categorical (`fips`, the region ids, the zoning and land-use codes), as the siblings do with ZIP or
postcode (house_sales `zipcode`, melbourne and perth `Postcode`). The tract numbers stay numeric with no reason given.
Precedent with a reason: brazilian_ecommerce keeps zip prefixes numeric because "CEPs are assigned by region, so their
order follows geography".

```text
**Consistency check (AI, 2026-10-20):** your call on zillow_prize (census tract-and-block numbers kept numeric, a
departure from CLEAN-14) differs from house_sales, melbourne and perth (ZIP/postcode categorical) and gives no reason,
unlike brazilian_ecommerce (numeric zip prefixes, "their order follows geography"). What sets it apart?
(a) the number is the FIPS county + tract + block code, so its order follows geography and its cardinality (tens of
thousands) is too high for a category; write that as brazilian_ecommerce does, recorded as an exception to CLEAN-14;
(b) make them categorical like the other codes; (c) reopen brazilian_ecommerce; (d) amend CLEAN-14 for hierarchical
geographic codes.
```

**12-17. Consistent**

* **12. Zeros as missing:** CLEAN-10/CLEAN-11. zillow is narrower than house_sales: a zero `bedroomcnt` becomes
  missing only when the bathrooms are also 0. house_sales' report suggests copying zillow's condition. Precedent
  churn_telco_south_asia (impossible values made missing).
* **13. Repeat sales and duplicates:** repeat sales are kept (USE-10, SPLIT-13), and those within 31 days are dropped
  as the competition's Data page does. melbourne merges re-reports within 60 days for the same reason. The 7 exact and
  39 conflicting duplicates are kept as separate parcels (LEAK-20), as house_sales does with its townhouse pairs.
  california's newest-only deduplication is the outlier (house_sales report, decision 7).
* **14.** The 24 2017 sales with no home facts are dropped, as Zillow did for 2016 (discussion 34667): they are no task
  rows.
* **15.** The drops follow CLEAN-3 (`parcelid`) and CLEAN-5 (`regionidcounty` recodes `fips`; `assessmentyear` repeats
  the year).
* **16. Licence:** selection.md: a no-redistribution rule is "no reason and no marker", only a note. 15 other
  definitions say "Kaggle Competition Rules" without the parenthetical. Harmless.
* **17. BibTeX:** `{Zillow}` @misc with the competition URL, as definitions.md asks for Kaggle sources.

</details>

<details><summary>Advocate</summary>

The data and the split stay as they are. Every real problem the phase A agents found is fixed by wording, by a
note, or by a cheap P7 change. None of them needs a change to the task, the split or the rows.

**1. P4 holds for every scored row: no test row carries a value from after its prediction point**

- **Evidence.**
  - Each sale is joined to the property file of its year. The tax roll it sees is the year before the sale
    (assessmentyear 2015 for all 2016 sales, 2016 for all 2017 sales; claim audit row 5).
  - For parcels sold only in 2017, the share of tax values that moved stays flat over the sale months (0.204-0.217).
    The building-fact edit rate does not rise with the sale month either (3.66% in Jan 2017, 3.19% in Jul 2017;
    column audit T2 and T4; practitioner 2.0-2.4%, flat). So no 2017 row shows a trace of its own sale.
  - The delinquency snapshot dates from about Aug-Sep 2016, before the oldest test window (Nov 2016; column audit T1).
  - The leak probe finds no feature or missing indicator alone above R^2 0. The split audit says "right with notes;
    no Must of SPLIT or USE-10 is broken".
- **Rule.** LEAK-1 and LEAK-10 (Must), SPLIT-1 (Must). All of them hold for the evaluation.
- **Why it outranks the objection.** The blind reviewer's concern 3 (2017 tax values leaking the sale price) was
  checked by the decisive experiment (EV-1). The result answers it: no sign of a reset for 2017 sales (T2). Its
  concern 4 (repeat sales and no parcel id) is a known-entity case. Under USE-10 (Must) a known entity's history is
  legitimate in a temporal split, and SPLIT-13 agrees. The duplicate rows are distinct parcels (claim audit row 34).
  Repeat sales are 2.9-3.8% of the test rows.

**2. The remaining post-sale values sit in training rows only, are measured, and pass LEAK-10's own clause**

- **Evidence.**
  - Building facts of Jan-May 2016 sales were edited after the sale in 1.4-2.3% of parcels, against about 1.1% later
    (claim audit row 7). About 98% of rows are unchanged.
  - The delinquency flag is lower before the snapshot (1.2-2.5% flagged against 3.1-4.7% later). A sale clears the
    arrears, so the post-sale values blank information rather than add it.
  - Dropping both delinquency columns leaves the skill unchanged. The claim auditor's runs give 0.0058 with and 0.0056
    without; the definition reports 0.0069 against 0.0068.
- **Rule.** LEAK-10 (Must) excludes a post-outcome lookup "unless the data shows they did not change". LEAK-11
  (Should, narrows LEAK-10) keeps a value that weakens the signal, with a note. The melbourne_housing_market precedent
  kept 98-100% matching values the same way.
- **Concession and mildest remedy.** The phrase "keeps later edits out" overclaims (claim audit, refuted in part).
  Reword `changes` and the curation_comments bullet:
  - properties_2016 is itself a snapshot of about Sep 2016;
  - the 2017 file postdates the 2017 sales;
  - the measured edit rates are small and touch training rows (2016) or show no trend (2017).
  Rename the delinquency bullet from "Potential leak, kept on purpose" to a LEAK-11 note, as option (a) of the
  precedent checker's prompt. This is the first rung of the remedy ladder (keep with a documented note), and no data
  changes.

**3. A real use case, and the practitioner keeps every structural choice (P3)**

- **Evidence.**
  - Zillow's own task: predict the Zestimate's miss per home and month, before the month starts. The practitioner
    agrees that "one row = one sale = how Zillow itself measures the Zestimate: matches".
  - The practitioner keeps the per-year property files, the monthly windows with a one-month gap, the Aug-Sep 2017
    drop and the prediction point at the start of the sale month.
  - Its verdict: "a legitimate real task ... a fair task".
- **Rule.** USE-1 and USE-5 (Must) hold. The target is the source's own target, and round 1 scored exactly this
  quantity.
- **Concession.** The practitioner rates the fit as approximate for two reasons:
  - the delinquency wording, which point 2 fixes and with it USE-8's "potential leak" clause;
  - the Zestimate and the listing data are not in the data. Zillow withheld both in round 1, so curation cannot fix
    this.

  Whether the missing Zestimate alone makes the fit `approximate` is a weighing call for the curator. Either answer
  changes one field of text. An approximate fit is shippable (USE-8 sends only `none` back to triage), so it is no
  reason to change or hold the dataset. Precedent: african_credit_scoring_challenge shipped as approximate.

**4. A small signal is real and lives in the features: TP-2 keeps it, and TP-1 asks for the tuned check, not exclusion**

- **Evidence.**
  - LightGBM with an L1 loss beats the train mean on 8-9 of 9 windows over 4 runs (claim audit row 11).
  - The train-median constant loses to the mean on 9 of 9 windows, and L1 beats the median constant on 9 of 9. So the
    gain comes from the features, not from a shift in location.
  - The split auditor gets 9 of 9 at gap 0 and at gap 1, and 3 of 3 under 3-month windows. The signal does not hinge
    on the design.
- **Rule.** TP-2 (Should): "a small but real signal is no reason to retire, and neither is a cutoff on the best
  skill". TP-1 (Must): a flag is checked against tuned methods. The precedent forest_fires (R^2 0.013, kept, Lennart
  2026-10-06) fits, and so does the tension row "the right split against the score" (P4 over P6).
- **Why it outranks the objection.** The blind reviewer says exclude because R^2 is at most 0.007. That is exactly
  the skill cutoff TP-2 rejects, and the reviewer reads no rules by design. REVIEW issue 2 already makes the keep
  conditional on tuned results (TBD -> 2nd Tier if they fail). That matches the pending-tuned precedents sf_permit_time
  and bias_correction.
- **Concession.** The written numbers are too high:
  - the R^2 range is about 0.001-0.012, not 0.003-0.021;
  - Huber wins 6-8 of 9 windows, not 9 of 9;
  - the paired t is below 2 in 4 of 9 windows.

  Mildest remedy: correct the numbers, and say the win needs an absolute-error loss (claim audit remedy 2).

**5. Metric RMSE follows the house rule; MAE is a one-line switch that the open cross-cut decides for all datasets**

- **Evidence.**
  - definitions.md "Field mapping": "A competition with its own metric keeps our default, and the notes name the
    original metric". The definition does this, as dataorg_financial_health and african_credit do.
  - The TP-6 against house-rule conflict is already filed collection-wide in `tabarena-v0pt2/REVIEW.md` (force_2020
    panel).
  - Under RMSE the robust fits still win 8-9 of 9 windows. The extreme rows (0.38% of rows, 49.9% of the squared
    error) cannot be identified row by row, and the competition's test kept them.
- **Rule.** TP-6 (Must) against definitions.md. "Treat like cases alike" (principles.md), so this is settled for all
  datasets in the cross-cut, not here. CLEAN-11 keeps values that are only unusual, and the precedent checker rates
  this choice consistent (its decision 6).
- **Why it outranks the objection.**
  - Clipping at +-0.4 (practitioner, blind reviewer) changes the target. TP-6 calls a fix of our own invention no
    better version.
  - MAE is the source's scoring. If the cross-cut amendment passes, `metric = "mae"` is the remedy: a field change,
    and the dataset ships.
  - Neither path excludes the dataset.

**6. The split mirrors the application, with source-based choices (P4)**

- **Evidence.**
  - 9 monthly windows, newest first. The oldest window trains on 53.4% of rows, and every window has more than 1,700
    rows.
  - The gap is grounded in the source's recording delay. Aug 2017 was 95% complete in the 2 Oct release and Sep about
    50%.
  - The gap costs 0.0006 of skill.
  - Seasonal drift moves the RMSE by at most 0.0003 per window (split audit).
- **Rule.** SPLIT-10 (Should): a gap of about the label delay. Precedent: brazilian_ecommerce, a one-month gap
  (Lennart, 2026-10-15). SPLIT-12 and SPLIT-19 are satisfied: the horizon falls inside the competition's 1-3 months.
  SPLIT-17 (Should) holds: no window is near the floor.
- **Concession.** Two points stand:
  - Nov and Dec 2016 are the thinned Kaggle remnant: about 18% of a normal month, and noisier.
  - Nov 2016 has 1 row with |y| > 1 against about 7 expected. That is p about 0.006 for one month, and about 0.12
    after the 21 months checked, so it is not significant after correction.

  The blind reviewer's "avoid Q4 2016 windows" would cut windows or change their count. The mildest remedy is a note
  in `splits_comment` that these two windows are sub-samples (split audit note 3). Both are Should-level, and
  "independent failures are not conflicts" does not apply because no Must is broken.

**7. The cleaning findings are P7: fix the cheap ones, note the rest. None is a reason to hold the dataset**

- **Evidence (column audit problems 3-7).**
  - `garagetotalsqft` is 0 for 14,981 rows that have 1-3 garage spaces.
  - The `pooltypeid10`/`hashottuborspa` recording halves between the files.
  - Three near copies: 99.98% / 99.5% / 98.9% equal.
  - Code labels are not mapped.
  - The tract numbers stay numeric without a stated reason.
  - Writing slips: "5 levels" should be 8; `assessmentyear` is the sale year minus 1; the roomcnt note omits Orange
    and Ventura.
  - The licence is noted only, as selection.md asks.
- **Rule.** Principles step 3: a quality problem "is fixed when the fix is cheap and safe, and otherwise kept with a
  note". The tension row "a real task against imperfect cleaning (P3 over P7)" applies. CLEAN-10, CLEAN-5, CLEAN-12
  and CLEAN-14 are Should.
- **Mildest remedies.**
  - Conceded as a cheap, safe fix: mask `garagetotalsqft == 0 & garagecarcnt > 0` to missing. One line, CLEAN-10.
  - Write notes for the spa flags and the near copies (they differ on a few rows).
  - Record an exception for the numeric tract codes, like brazilian_ecommerce (the order follows geography, and
    55k values is too many for a category).
  - Fix the writing.

  None of these touches validity (P1-P5).

**Judgment record (advocate's view)**

Verdict: ship as defined, with wording fixes and one optional one-line P7 fix.
Validity: USE-1 and USE-5 hold. USE-8: direct once the delinquency is noted under LEAK-11 (whether the missing Zestimate makes it approximate is a curator call; text only). LEAK-1 and LEAK-10 hold for test rows; the training-row remnants pass LEAK-10's "did not change" clause and LEAK-11, noted. SPLIT-1 and SPLIT-10 hold.
Value: TP-2 keeps a small real signal (L1 8-9/9, features beat the median constant 9/9); TP-1 tuned check pending, with REVIEW issue 2's 2nd-Tier fallback.
Quality: CLEAN-10 garage zeros (cheap fix), CLEAN-5/12/14/21 notes or an exception.
For the curator: the metric (the collection cross-cut); the fit label (the missing Zestimate).

**Rebuttal**

The critic does not ask to exclude the dataset. We agree on points 3, 6 and 7, agree in substance on point 4, and
the remedies overlap. Two real disputes remain:
- point 2: drop the delinquency columns, or keep them with a note;
- point 5: whether the tuned check gates shipping.

**1. The fit label: conceded**

- **What I concede.** USE-8 (Must) defines direct as "the rows, the features, the label's timing and the split
  mirror the use case". The features do not. Zillow holds the Zestimate, and under USE-6 (Must) the company's own
  estimate is an input. Here it is missing, and the source cannot supply it (PR §1; BL).
- **What follows.** Even after point 2 is fixed, the fit is approximate on the USE-6 gap alone. In my brief I left
  this to the curator. On reflection, the rule's wording decides it, so it is not a weighing call.
- **Remedy.** Set `fit = "approximate"` and name the gap in `fit_reason`. This is a text change, and an approximate
  fit ships (USE-8 sends only `none` back).

**2. The delinquency columns: disputed on the rule, accepted on the remedy**

- **Dispute.** LEAK-11 (Should; it narrows LEAK-10 and wins within its scope) keeps "a value measured after the
  outcome that weakens the signal". That is the mechanism measured here:
  - the post-sale rows lose a flag that the sale cleared (1.2-2.5% flagged against 3.1-4.7% later; COL T1);
  - no test row is affected.
  So LEAK-6's "confirmed leak goes" does not apply: nothing inflates the score (CA row 10: 0.0058 against 0.0056).
- **Concession.** The remedy ladder puts "fix the definition" above "keep with a note". Dropping the columns costs no
  measured skill (CA row 10) and ends the third-case question (PC decision 3). So I do not oppose dropping them.
- **Remaining choice.** Drop, blank (LEAK-7), or keep under LEAK-11. The choice also feeds the amendment PC proposes.
  It no longer moves the fit (see point 1).

**3. "Keeps later edits out": agreed**

- This is the same remedy as my point 2: the measured melbourne-style note under LEAK-10's "did not change" clause.
- I concede the FAQ timing claim (CA claim 18) is untested (EV-7). A human with Kaggle access should confirm it.
- The measurement still supports the prediction point: day of month against logerror gives Spearman -0.013.

**4. Metric: agreed on the remedy, disputed on one effect**

- **Agreed.** List zillow in the cross-cut in `tabarena-v0pt2/REVIEW.md` as a case the TP-6 amendment would flip to
  `mae`, and leave the metric open, not settled.
- **Disputed: "rewards a choice of loss function, not tabular learning".** For a heavy-tailed target, choosing a
  robust loss is part of fitting it well, and tuned pipelines make that choice. The L1 fits still beat the median
  constant on 9 of 9 windows (CA row 11), so the features rank models under either metric.
- **Weight.** This is a weighing remark. It does not change the remedy.

**5. Signal: the numbers are conceded; gating shipping on the tuned check is disputed**

- **Conceded.** Correct the numbers as the critic and I both wrote them (CA ranked item 2).
- **Disputed: "ship only once tuned results beat the dummy".**
  - TP-1 (Must) says to check a flag against tuned methods "before acting on it". The action at stake is retiring the
    task, not shipping it.
  - TP-2 (Should) says the task stays "until a concrete reason is found in the task itself".
- **Precedents.** sf_permit_time and bias_correction were kept pending tuned results. The critic's distinguishing
  fact is that untuned L2 fits lose here. That holds, but it is a fact about one loss, not about the task. The
  features beat the median constant on 9 of 9 windows, and that is real signal.
- **Remedy.** Ship with REVIEW issue 2's condition attached: if the tuned results fail, move to TBD -> 2nd Tier.
  That is the remedy the critic also names.

**6. The thinned Q4 2016 windows: agreed**

- I accept the note in `splits_comment`.
- The Nov 2016 tail gives p ≈ 0.006 for one month out of the 21 checked, about 0.12 after correction. That calls
  for a note, not a re-split (SPLIT-17, Should; EV-6).

**7. Cleaning and writing: agreed**

- Mask the garage zeros (CLEAN-10).
- Drop the three near copies or give their reason (CLEAN-5).
- Fix the three wrong statements.
- These are all P7 changes and none holds the dataset back.

**Where this leaves the dataset**

The verdict is ship after changes, all of them text except:
- the garage mask;
- possibly the delinquency drop.

The open items for the curator are:
- delinquency: drop, blank or keep (LEAK-11 against the ladder);
- the metric (the cross-cut);
- whether shipping waits for the tuned results (TP-1 against TP-2).

</details>

<details><summary>Critic</summary>

**Position: ship only after changes.** None of the points below calls for excluding the task. Points 1-3 are about
validity and are fixed in the definition or its notes. Point 4 is the metric. Point 5 is a precondition from TP-1.
Points 6-7 are quality and notes. Evidence is cited by report: CA = claim_audit.md, COL = column_audit.md,
SA = split audit, PR = practitioner, BL = blind review, PC = precedent check, probes = the panel's probes.

**1. The fit is labelled `direct` although the data has two named gaps (P3, USE-8 Must; USE-6 Must)**

- **Problem.** `fit = "direct"`, but USE-8 lists "a potential leak kept on purpose" under Approximate, and the
  definition's own bullet is `Potential leak, kept on purpose:` (tax delinquency). Separately, the input that Zillow
  always has at the prediction point is missing: the Zestimate of the first of the month. The target is that
  estimate's error. The listing data and the last sale price are missing too.
- **Effect.** The task as shipped is "find where the Zestimate is biased, using public assessor facts and without
  the Zestimate". That is a stand-in for Zillow's task, not a mirror of it. A `direct` label tells benchmark users
  the opposite.
- **Evidence.** PR §1 and the gaps ranked there (fit: approximate). PC decision 2: kick, african_credit_scoring_challenge
  (the closest facts: no measurable effect, still `approximate`) and churn_telco_south_asia (CC 2026-10-15) all keep
  such a field as approximate. USE-6 cases bias_correction and brazilian_ecommerce: the company's own forecast is the
  input. BL "What the task is" makes the same point on its own.
- **Remedy (fix the definition).** Set `fit = "approximate"`. In `fit_reason`, say that the Zestimate, the listing
  data and the previous sale price were not released, and that this gap cannot be fixed from the source. USE-9 does
  not rescue `direct`: every nearby use case also needs the automated value (PR, "What a domain expert would change").

**2. Tax delinquency is post-sale in 72,157 training rows. Drop it rather than argue about it (P4, LEAK-10 Must, LEAK-6 Must; LEAK-7)**

- **Problem.** `taxdelinquencyflag` and `taxdelinquencyyear` are one snapshot from about Aug-Sep 2016, and the same
  snapshot appears in both property files. For the Jan-Aug 2016 sales it was taken after the sale: 1.2-2.5% of those
  rows are flagged, against 3.1-4.7% later, presumably because the sale paid off the arrears.
- **Effect.** No test row is affected, because the snapshot predates the Nov 2016 window (COL T1). The training rows,
  however, encode an outcome-linked change in one column. This shifts the column between train and test, and it is
  the only reason the definition gives for a "potential leak". LEAK-6 says a confirmed leak goes even when it is small.
- **Evidence.** COL T1 and problem 1. CA rows 10 and 30: with the columns, mean skill is 0.0058/0.0056; without them,
  0.0056/0.0057. The definition's 0.0069/0.0068 comes from another config. PC decision 3: this is the third draft
  that keeps a post-outcome lookup with "dropping changes nothing" as the reason.
- **Remedy (fix the definition, the mildest that works).** Drop both columns. That costs nothing measurable and
  removes the leak, the `Potential leak` bullet and one of the two grounds of point 1. The alternative, blanking the
  columns for sales before Sep 2016 (LEAK-7), also works, but it keeps a column whose meaning changes with the
  row's date.

**3. "Keeps later edits out" is not true. The data supports keeping the facts, but the note must say why (P4, LEAK-10 Must, clause "unless the data shows they did not change")**

- **Problem.** `changes`, the CC bullet and `fit_reason` all say that taking the property file of the sale's year
  "keeps later edits out". The facts are these:
  - properties_2017 was released in Oct 2017, so it is a post-sale lookup for every 2017 row, including all six 2017
    test windows.
  - properties_2016 is itself a snapshot from about Sep 2016, so it is post-sale for the Jan-Aug 2016 training rows.
- **Effect.** Small but undocumented. Building facts differ between the two files for 3.2-3.7% of the parcels sold
  only in 2017, and the rate is flat across sale months. For parcels sold Jan-May 2016 the edit rate is 1.4-2.3%,
  against about 1.1-1.4% for the others. Tax values show no reset after a 2017 sale. This is melbourne's
  "did not change" range, not King County's.
- **Evidence.** COL T2 and T4, and problem 2. CA rows 7 and 22 (partly refuted) and the implied claim "known at the
  prediction point of the training rows: refuted". PC decision 1 (a consistency check against house_sales and
  melbourne). PR §1 (2.0-2.4%, flat). One more point: the prediction point rests on the FAQ ("the Zestimate of the
  first of the month"), which no agent could read (CA claim 18, untested, EV-7).
- **Remedy (a note).** Replace "keeps later edits out" with the measured statement: the files are snapshots taken
  after some sales; facts changed for about 2-4% of sold parcels, the rate is flat by sale month, and tax values show
  no reset. Write it as melbourne does. A curator with Kaggle access should confirm the FAQ quote.

**4. Under RMSE the score mainly ranks how models handle miskeyed prices; the source scored MAE (P6, TP-6 Must; USE-5 Must)**

- **Problem.** 0.38% of rows (|logerror| > 1) hold 49.9% of the squared error, and 2.1% of rows (> 0.4) hold 74.3%.
  Zillow traces these rows mostly to data errors. The competition scored MAE.
- **Effect.** Under RMSE, a method's rank depends on a few hundred rows that nobody acts on. Untuned L2 LightGBM
  loses to the train mean in 5-6 of 9 windows; L1 and Huber win. So the benchmark rewards a choice of loss function,
  not tabular learning.
- **Evidence.** CA rows 20, 42 and 55; probes/robust_lgbm_windows.txt (L2 wins 4 of 9, mean -0.0022); PR §2 ("RMSE
  mostly scores how a model handles recording errors"); BL concern 1 (kurtosis 128). TP-6 says that a better version
  the source defines, including "the scoring it uses", replaces ours.
- **Remedy (fix the definition, or decide it in the cross-cut).** Set `metric = "mae"`, the source's scoring. If the
  house rule in definitions.md ("keep our default") stands until the open cross-cut in `tabarena-v0pt2/REVIEW.md` is
  settled, list zillow there as a case the amendment would flip, and do not mark the metric as settled. Clipping the
  target at +-0.4 is our own invention and not a better version under TP-6, so I do not ask for it.

**5. The signal is thinner than written, and the keep rests on numbers that do not reproduce (P6, TP-1 Must, TP-2 Should; EV-8)**

- **Problem.**
  - The R^2 range in `fit_reason` and the CC bullet, 0.003-0.021, does not reproduce. The re-runs give 0.0008-0.0123,
    and the panel's probe gives 0.002-0.017.
  - "All nine windows" holds for an L1 loss only, and only in 3 of 4 runs.
  - Huber wins 6-8 of 9, not the 9 of 9 claimed. L2 wins 3-4 of 9.
  - The paired t is below 2 in 4 of 9 windows.
  - Every task probe flags it (no_signal, drift_baseline, unstable).
- **Effect.** The blind reviewer, with no notes, says "exclude: almost no signal". TP-2 keeps a small real signal,
  but TP-1 (Must) requires the tuned check before a flag is set aside, and no tuned results exist.
- **Evidence.** CA rows 11, 21, 56 and 59, and ranked item 2; probes/task/summary.md (best skill -0.007); BL concern
  1; PC decision 5. Unlike the pending-tuned precedents, the untuned L2 fits lose to the mean here.
- **Remedy (fix the notes; keep conditionally).** Correct the numbers: "L1 beats the train mean in 8-9 of 9 windows,
  R^2 about 0.001-0.012; squared-error fits do not". Ship only once tuned results beat the dummy window by window. If
  they do not, the outcome is `TBD -> 2nd Tier`, as the earlier REVIEW.md's issue 2 already says. This is not a reason to
  exclude the task.

**6. The two oldest test windows are Kaggle's remnant sample, and Nov 2016 looks thinned in the tail (P4, SPLIT-17 Should; EV-6)**

- **Problem.**
  - Nov and Dec 2016 hold only 1,826 and 1,739 rows, about 18% of a normal month, because Kaggle held the rest back
    for its leaderboard.
  - Nov 2016 has 1 row with |logerror| > 1, where about 7 are expected (Poisson p of about 0.006, one month among 21).
  - Each of these windows weighs 1/9 of the score.
- **Effect.** Under RMSE, a window missing its extreme rows is easier and less noisy than the others. Dec 2016 is
  the opposite, with RMSE 0.190. The note "the share looks random" is checked only at the 0.4 threshold.
- **Evidence.** CA claim 24 and ranked item 3; SA note 3; BL concern 2 ("avoid test windows in Q4 2016").
- **Remedy (a note).** In `splits_comment`, say that these two windows are sub-samples, and give the |y| > 1 count.
  If the curator wants a test, compare the share in Oct 15-Dec 31 2016 with the same weeks of 2017. I do not ask for
  a re-split.

**7. Cleaning gaps and wrong statements in the notes (P7, CLEAN-10 Should, CLEAN-5 Should; writing)**

- **Problem.**
  - `garagetotalsqft` is 0 for 14,981 rows with 1-3 garage spaces (30% of the Orange and Ventura garage records), so
    0 stands for "area not recorded".
  - `calculatedbathnbr`, `finishedsquarefeet50` and `censustractandblock` are near copies (98.9-99.98%), kept without
    a reason.
  - Notes that are wrong:
    - The roomcnt bullet names only Los Angeles, but the code also blanks 20,397 Orange and Ventura zeros.
    - The note says `assessmentyear` "repeats the sale year"; it is the sale year minus one.
    - the earlier REVIEW.md's issue 6 says the 2016 quality scale has "5 levels"; it has 8.
- **Effect.** Small. These do not change the task.
- **Evidence.** COL problems 3, 5 and 7; CA claims 31, 32 and 64.
- **Remedy (repair and fix the notes).**
  - Mask `garagetotalsqft == 0 & garagecarcnt > 0` to missing (one line, next to the room-count masks).
  - Drop the three near copies, or write one line on why they stay.
  - Correct the three statements.
  - None of this is a reason to hold the dataset back.

**Not raised**

- Licence: under SEL it is a note, not a reason.
- Duplicates and repeat sales: consistent with LEAK-20 and SPLIT-13 (CA claim 34).
- The 1-month window with a 1-month gap: within the source's horizon (SA note 1).
- The Aug-Sep 2017 drop: correct.

**Rebuttal**

Where the advocate and I already agree:

- No change to the rows, the split or the target.
- No exclusion.
- These fixes:
  - correct the "keeps later edits out" wording;
  - correct the signal numbers;
  - mask the garage zeros to missing;
  - add a note on the sub-sampled windows;
  - fix the writing slips.

That is "ship after changes", not "ship as defined". What is left in dispute is the fit label and the label on the
delinquency columns.

**Advocate 1 (P4 holds for every scored row): concede**

COL T1, T2 and T4 measure it: the delinquency snapshot predates every test window, and the tax and building facts
of the 2017 rows show no trend by sale month. That satisfies LEAK-10's "did not change" clause for the test rows, as
melbourne does. My point 3 asks only for the note that says so, and the advocate concedes that note in its point 2.

**Advocate 2 (training-row remnants pass LEAK-10/LEAK-11): concede the building facts, dispute the LEAK-11 label for delinquency**

- **Building facts: concede.** About 98% of rows are unchanged (CA row 7). A note under LEAK-10's own clause is enough.
- **Delinquency: dispute.** LEAK-11 (Should) applies only to a value that "weakens the signal". Nobody has measured
  that.
  - The only measurement is that dropping the columns changes nothing in either direction: 0.0058 with and 0.0056
    without (seed 0); 0.0056 with and 0.0057 without (seed 1); CA row 10.
  - "A sale clears the arrears" is an untested mechanism. Under EV-6 an untested claim is a question, not a finding.
  - What is measured is a column whose distribution differs between the training rows before Sep 2016 and every test
    window (1.2-2.5% flagged against 3.1-4.7%; COL T1). That is a post-outcome value (LEAK-10, Must), and LEAK-6
    (Must) says a confirmed post-outcome value goes even when its effect is small.
  - PC decision 3 counts this as the third draft to keep a post-outcome lookup because "dropping changes nothing".
    Relabelling it LEAK-11 here would settle that pattern by wording, not by evidence.
- **Remedy.** I still ask for the mildest remedy that settles it: blank the two columns for sales before Sep 2016
  (LEAK-7), or drop them. Both cost nothing measurable. If the curator prefers to keep them with a LEAK-11 note, the
  note has to name the measured effect, and the case goes into the amendment question that PC raises.

**Advocate 3 (a real use case; the missing Zestimate is a curator's weighing call): concede that the task is real and shippable, dispute that the label is a weighing call**

- **Concede.**
  - USE-1 and USE-5 hold.
  - An approximate fit ships (USE-8 sends only `none` back to triage).
  - My remedy is one field of text.
- **Dispute.**
  - USE-8 is a Must, and its definition of Direct is that "the rows, the features ... mirror the use case".
  - USE-6 (Must) says what removing the company's own estimate does: it "changes the task into 'predict without the
    company's estimate'".
  - The only rule that could restore `direct` is USE-9, and the practitioner tested it and rejected it: every nearby
    use case also needs the automated value (PR, "What a domain expert would change").
  - So the label follows from the rules, independent of the delinquency question. Fixing point 2 removes one ground
    for `approximate`, not both.
  - A Weigh factor cannot override a Must (principles.md, Strengths). Calling this a weighing call does not change
    that.

**Advocate 4 (TP-2 keeps a small real signal; TP-1 tuned check pending): concede**

The evidence that the features beat the median constant on 9 of 9 windows (CA row 11) answers the blind reviewer's
call to exclude, under TP-2 and the forest_fires precedent. We now ask for the same things:

- correct the numbers;
- state that the win needs an absolute-error loss;
- ship conditional on tuned results, with TBD -> 2nd Tier as the fallback.

**Advocate 5 (RMSE follows the house rule; the cross-cut decides): mostly concede**

- **Concede.** A collection-wide conflict between TP-6 and definitions.md belongs in the cross-cut ("treat like
  cases alike"), and my remedy already offered that path. I also do not ask for clipping (TP-6, our own invention).
- **Hold one thing.** List zillow in the cross-cut in `tabarena-v0pt2/REVIEW.md` as a case the amendment would flip,
  and leave the metric marked open, not settled.
- **Why it matters here.** The advocate's evidence that robust fits win under RMSE also shows the opposite for the
  default loss most regressors use. L2 LightGBM wins only 4 of 9 windows (probes/robust_lgbm_windows.txt), so under
  RMSE the ranking partly reflects each method's choice of loss. That fact belongs in the cross-cut's evidence.

**Advocate 6 (the split mirrors the application): concede**

- Correcting for the 21 months checked gives p about 0.12, so the thinned tail in Nov 2016 is not significant. I
  withdraw it as evidence of bias.
- A note in `splits_comment` that Nov and Dec 2016 are Kaggle's sub-sample (SA note 3) is all I asked for, and the
  advocate concedes it.

**Advocate 7 (cleaning is P7): concede**

- We agree on the one-line garage mask (CLEAN-10), the notes and the writing fixes.
- I accept the numeric tract codes kept as an exception to CLEAN-14 with the brazilian_ecommerce reason, instead of
  my "drop or explain" for that column.

**For the mediator**

Two points remain open:

1. **Fit label.** The advocate says it is a curator's weighing call. I say USE-8 and USE-6 (Must) decide it:
   `approximate`.
2. **Delinquency columns.** The advocate wants a LEAK-11 note. I want the columns blanked or dropped (LEAK-10 and
   LEAK-6, Must), because LEAK-11 requires a weakening of the signal that has not been measured. The experiment that
   would settle it: refit with the columns blanked for sales before Sep 2016 only, and compare skill and feature
   importance in the Nov 2016 to Jan 2017 windows.

</details>
