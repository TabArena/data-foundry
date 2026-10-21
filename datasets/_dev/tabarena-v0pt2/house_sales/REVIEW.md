# house_sales

**Outcome:** added. King County house sales of May 2014 to April 2015, each house rebuilt as the assessor recorded it
on the sale day, the sales the county flags as not at market value dropped, 9 three-week windows after a one-week gap;
the AI recommends shipping it. Validity: SEL holds; USE-1 holds with the actor reworded (the assessor's mass appraisal
or a valuation model working from public records); USE-5 triggered, fixed (1,061 non-market sales dropped; the
borderline codes are issue 8); LEAK-10 triggered, fixed (the as-of-sale rebuild, including the lot size); LEAK-11: the
few values still from July 2015 are kept with a note (masking them changes no score measurably); the fit is `direct`
with the remnant named in `fit_reason` (the curator, 2026-10-21: direct when the task without the leak would be
direct, approximate only when avoiding the leak needed large changes; USE-8); SPLIT-10 triggered, fixed (one-week gap); PROV-13 holds (repaired from the county's records); PROV-10 fixed
(cites the 2015 course release and the county). Value: TP holds (no probe flag; on the data after this review's changes, untuned LightGBM and a linear model remove
90% and 86% of the squared error of a dummy that predicts the training mean, skill +0.90 and +0.86 on 5 of the 9
windows).
Quality: CLEAN-11 fixed (5 placeholder living areas set to missing); CLEAN-10 departure on `yr_renovated` (issue 9).
Weighed: county source +, repair from the origin +, size +, one year of data -. Left for the
curator: issues 8 and 9 (the family's fit label and window length were settled on 2026-10-21).

**Main points:** Which county sale warnings mark a sale as not at market value (issue 8), and whether `yr_renovated` = 0
stays missing (issue 9). The fit label is settled (2026-10-21, the curator): `direct`, with the
measured-harmless July-2015 remnant named in `fit_reason`. The window length is settled too: the house-price datasets
keep their own horizons (no family-wide window).

**Record fields that disagree with the definition:**

- `year`: record `2016`, definition `2015`.

**Record judgment:** valid. King County's recorded sales with the assessor's record rebuilt as of each sale; the county's
own sale warnings remove the sales that are not at market value.

**Issues for Lennart:**

8. **Which county sale warnings mark a sale as not at market value?** The county attaches warning codes to each recorded
   sale, such as a short sale (the bank accepts less than the loan) or a sale between relatives. A valuation model is
   meant to predict the market price, so a sale under such a code is a different target.
   - Effect on the task: these sales sell below what the house is worth, so the model overestimates them and no input
     explains the error; keeping them adds noise to the low end of the target and rewards nothing a valuer needs.
   - Evidence: the panel matched 20,742 of the 20,967 sales before May 2015 to the county's sales on parcel, deed date
     and price, and measured the error of an untuned LightGBM per code (residual = log price minus the prediction, on
     the test rows; "sales" counts all matched sales; unflagged sales: +0.03):

     | code | meaning | sales | mean residual |
     |---|---|---|---|
     | 15 | no market exposure | 654 | -0.14 |
     | 46 | non-representative sale | 357 | -0.23 |
     | 60 | short sale | 199 | -0.23 |
     | 51 | related party | 91 | -0.20 |
     | 23, 13 | forced sale, bankruptcy | 23 | -0.22, -0.23 |
     | 12 | estate administrator | 43 | -0.06 |
     | 54 | affordable housing | 22 | -0.17 |
     | 10, 29 | teardown, segregation or merger | 426 | -0.02, +0.05 |
     | 22, 8, 32, 14, 16, 18 | partial interest, questionable, $1,000 or less, sheriff, government, quit claim | 14 | not measured |

   - Implemented: drop the 1,061 sales (5.1%) with code 15, 46, 60, 51, 23 or 13; keep every other code. Teardowns and
     segregations are priced like market sales of the land or the changed lot (measured), so they stay either way.
     Code 26 (improvements changed since the sale; 1,073 kept sales, mean residual -0.12) also stays. It flags a house
     that changed after the sale, not a price below market. 944 of these rows are not rebuilt because their changes
     come after July 2015, so the features are the record at the sale, and the low residual is a house bought to be
     improved later. This departs from california_house_prices_2020 (CC 2026-10-14, rows whose listing described
     another state of the house dropped); what sets it apart is that here the features hold the record at the sale.
   - Alternative: (a) also drop 54 and the rare codes 22, 8, 32, 14, 16, 18 (about 36 more sales), which the county's
     own names describe as non-market; codes with 1 to 4 sales have no measured residual, so (a) drops them on the
     county's wording alone. (b) Also drop 12 (estates,
     43 sales, -0.06), as the critic proposed. Either changes the score little; the list becomes the rule for the other
     house-price datasets, since no precedent on sale warnings exists yet.
   - Rule: USE-5 (P3, Must; the target is what the actor acts on). The filter itself is settled (the critic and the
     advocate agree, the mediator ruled a note would not resolve a Must); the scope is a weighing call.
   - Recommendation: (a), keep 12. Decision: the list of codes to drop.

9. **Keep a renovation year of 0 as missing?** In the source, `yr_renovated` = 0 means "never renovated", not an
   unknown year. The definition turns 0 into missing (19,087 of 19,906 rows, 95.9%), so a missing value means "never
   renovated".
   - Effect on the task: none for tree models; a linear model that read 0 as a year would fit a slope through it, while
     missing asks it to impute. After the rebuild nothing else is missing in the column, so the meaning stays clear.
   - Implemented: missing; the note says missing means "never renovated".
   - Alternative: keep 0 as published, or add a 0/1 `renovated` column and leave the year missing (one more column).
   - Rule: CLEAN-10 (P7, Should) converts placeholder codes for missing values but keeps a code that means something
     and says why. Precedents keep such codes: bank_marketing keeps `pdays = -1` ("not contacted"), house_prices_nominal
     keeps its no-remodel coding. The fact that sets this case apart: a 0 in a year column misleads a linear model, and
     missing has no other meaning here.
   - Recommendation: keep it missing and record an exception to CLEAN-10 with that fact. Decision: the exception, or
     keep 0, or the flag.

**Review panel:** ship after changes (mediator). Full tier: claim, column and split audits, domain practitioner, blind
review, precedent check, advocate and critic with one rebuttal each, mediator; their numbers are on the 20,967 rows
before this review's changes. Claim audit: 4 claims refuted (the lot size was not rebuilt, "the house as it was sold",
the resale error of 0.36, the target as a market price), all fixed; a few untested (the course file's table, unchanged
county events). Blind review: would include with changes; its main concern, the undocumented as-of-sale values, is met
by the definition's notes. Agreed: the rebuild, the lot-size fix, the one-week gap, the July-2015 values kept with a
note, the wording, citation and placeholder fixes. Settled by the mediator: the non-market sales are filtered, not
noted (USE-5, Must), and teardowns and segregations stay. To the curator: the mediator's issues 1 and 4 are issues 8 and 9 here; its issues 2 (fit label) and 3 (window
length) are in the working copy's REVIEW.md.

<details><summary>Mediator</summary>

Inputs: the audits (claim, column, split), practitioner, precedents, clean room, both briefs and both rebuttals,
`dataset.py`, README, record and the earlier REVIEW.md. New measurements reuse the claim audit's untuned LightGBM
predictions on the 9 shipped windows.

**Recommendation**

```text
Verdict: ship after changes.
Validity: SEL holds; USE-1 holds once the actor is reworded; USE-5 triggered, fixed (drop the sales the county flags
as non-market: 15, 46, 51, 60, 23, 13; borderline codes are issue 1); USE-8 approximate (remnants kept on purpose;
issue 2 can amend); LEAK-10 triggered, fixed (as-of-sale rebuild, plus the missed LandFootage lot changes);
LEAK-11 July-2015 remnants kept with a note; SPLIT-10 triggered, fixed (1-week gap); SPLIT-6/11/14/15/17 hold;
PROV-13 holds (repaired from the origin); PROV-10/PROV-11 citation fixed.
Value: TP holds (LightGBM skill +0.884, linear +0.852, drift baseline +0.002; no probe flag).
Quality: CLEAN-11 placeholders to missing; CLEAN-10 departure on yr_renovated (issue 4).
Weighed: source +, repair +, size +, familiarity -, one year of data -.
For the curator: issue 1 (which warning codes count as non-market), issue 2 (amend USE-8 or approximate for the
house-price family), issue 3 (window length, family call), issue 4 (yr_renovated 0 as missing).
```

The two sides agree on the verdict and on every remedy rung after the rebuttals. The one open dispute (the
non-market filter: Must fix vs. fallback note, and its code list) is settled by rank below; what remains is a
weighing on borderline codes.

**Disputed point settled: non-market sales in the target**

- Critic: USE-5 (P3, Must) is triggered and fixable from the origin, so a note does not resolve it. Advocate (rebuttal):
  concedes the filter, asks for a per-code scope because teardown (10) and segregation (29) may be arm's-length.
- It is a conflict only with convenience (a third county extract), which no rule protects. USE-5 wins; the remedy
  ladder gives "fix the definition" (drop the rows), not a note.
- Decisive experiment (run here; residual = log price minus the rebuilt-data LightGBM prediction, test rows):

| warning | rows | test | test RMSE | mean residual |
|---|---|---|---|---|
| none | 18,196 | 8,092 | 0.149 | +0.026 |
| 15 no market exposure | 654 | 388 | 0.296 | -0.140 |
| 46 non-representative | 357 | 214 | 0.308 | -0.229 |
| 60 short sale | 199 | 93 | 0.290 | -0.227 |
| 51 related party | 90 | 50 | 0.307 | -0.197 |
| 23 forced sale | 13 | 9 | 0.304 | -0.221 |
| 13 bankruptcy | 10 | 4 | 0.305 | -0.230 |
| 12 estate | 42 | 28 | 0.302 | -0.061 |
| 54 affordable housing | 22 | 15 | 0.228 | -0.171 |
| 10 tear down | 322 | 188 | 0.249 | -0.021 (median -0.004) |
| 29 segregation/merger | 104 | 61 | 0.243 | +0.051 |
| 26 imp. changed since sale | 1,225 | 681 | 0.250 | -0.118 |

- Result: the advocate is right on 10 and 29 (noisy but unbiased: priced like market sales of land or a changed lot;
  keep). 15, 46, 51, 60, 23, 13 sit 0.14-0.23 below the model and are non-market by the county's own definition:
  drop. Together 1,060 rows (5.1%), 605 test rows; test RMSE on the rest 0.1603 against 0.1717 on all (same model,
  not refit). 12, 54 and the rare codes (22, 8, 32, 14, 16, 18; 1-3 rows each) are the borderline set: issue 1.
- 225 kept rows do not match a county sale; their warnings are unknown and they stay.

**Changes to make now (no decision needed)**

1. **Lot size (LEAK-10, Must).** Add `("LandFootage", "SqFtLot"): "sqft_lot"` to `CHANGED_COLUMNS` (keep `Land`),
   re-run `_prepare_raw_files`; the 2,151 count and Decision 1 regenerate (about 81 lot rows).
2. **Non-market sales (USE-5, Must).** Add the county Real Property Sales extract (EXTR_RPSale, ~150 MB) as a raw
   input; drop the matched sales with warning 15, 46, 51, 60, 23 or 13 (1,060 rows); keep 10, 29, 26; a Decision
   table of rows dropped per code. Borderline codes per issue 1.
3. **Recording delay (SPLIT-10, Should, applying SPLIT-9/LEAK-12).** `TemporalSplits(..., gap=1)`. Checked: still 9
   windows, oldest train side 10,840 rows (51.7%, SPLIT-14 holds); gap=2 would lose a window. State in
   `splits_comment`: deed-to-recording delay median 6 days, 91% within 14.
4. **Fit (USE-8, Must).** `fit = "approximate"`: a potential leak is kept on purpose, which USE-8 names as approximate
   (case kick). Issue 2 is the only way back to direct.
5. **Remnants note (LEAK-11).** Turn the "We leave ..." bullet into `Potential leak, kept on purpose:` with: 143-145
   rows whose view/waterfront rating changed after the sale (39 gained a view), masking their view 0.2147 vs 0.2132;
   neighbours' areas at most +0.004 on changed rows; 5 bathroom rows, 10 blank old values, 24 rows with a full-record
   Bldg 1 event after the sale. Do not blank them (the missingness would mark "changed after the sale"). Warning 26:
   1,096 of 1,225 are not rebuilt because their changes come after the snapshot; they sit below the model (-0.118),
   so they are noise, not a flattering leak.
6. **Use case wording (USE-1, USE-3).** "The assessor's record on the sale day", not "the house as it was sold"
   (refuted: residual +0.079 on rebuilt rows, shift-residual corr 0.59). Actor: the assessor's mass appraisal or a
   public-record AVM before the sale is recorded. Add "without the assessed value or the previous sale price".
7. **Placeholder areas (CLEAN-11, Should).** The 6 rows with `sqft_living` 8-200 and bedrooms recorded: set
   `sqft_living` and `sqft_above` to missing; rows stay (cases heart_disease_va_long_beach, sdss_17). Leave the 290
   sq ft row.
8. **Citation (PROV-10, PROV-11, Must; Must has no exception).** Cite the origin (King County Department of
   Assessments extracts) and the first publication (UW Machine Learning Specialization, 2015), not the 2016 Kaggle
   re-upload; keep the Kaggle copy in the comments. Record `year` 2016 -> 2015.
9. **Pins (definitions.md, `download_description`).** md5 of `house_sales_changes.csv`, `house_sales_bath_counts.csv`
   and the sales extract's filtered output, so a rebuild shows unchanged inputs.
10. **Numbers and wording (writing, EV-8).** Resales RMSE 0.27 vs 0.17 (not 0.36); "share every feature but the
    date"; bathrooms 913 rebuilt / 869 changed; `yr_renovated` 0 means "never renovated", not "unrecorded";
    `sqft_basement` is the finished basement; May: the bulk stops 15 May, 5 rows recorded to 2 June; waterfront is a
    county attribute (`WfntLocation`), view is not. `splits_comment`: the window length follows the window count, not
    a cited refit cadence (SPLIT-12); windows cover late October to April and history is under a year (SPLIT-20).

**Issues for the curator (ranked)**

1. **Which warning codes count as non-market (P3, USE-5 Must; a weighing of scope).**
   - Problem: the filter is settled; the borderline codes are not. 12 estate (42 rows, -0.06), 54 affordable
     housing (22, -0.17) and the rare codes (22 partial interest, 8 questionable, 32 $1,000 sale, 14 sheriff,
     16 gov-to-gov, 18 quit claim; ~15 rows).
   - Effect: ~40 rows; small on the score, sets the rule for the house-price family.
   - Critic: valuers use validated market sales only; list 15, 46, 60, 51, 12, 13, 23 (+10). Advocate: decide per
     code; 10 and 29 are arm's-length. Measured: 10 and 29 unbiased (keep); 12 mildly low.
   - Decision: the code list (recommended: add 54 and the rare price-distorting codes 22, 8, 32, 14, 16, 18; keep 12).
2. **Direct or approximate with measured-weak remnants (P3, USE-8 Must; a rule question).**
   - Problem: USE-8 names "a potential leak kept on purpose" as approximate. melbourne_housing_market and zillow_prize
     (AI drafts) say direct with the same kind of remnant.
   - Advocate: the remnants are measured weak, so direct describes the task. Critic: a Must has no exception;
     approximate unless USE-8 is amended.
   - Decision: keep USE-8 (house_sales approximate, siblings follow) or amend it ("a remnant measured to carry no
     signal keeps direct"), applied to all three.
3. **Window length (P4, SPLIT-12 Should; weighing, family-level).** 9 three-week windows (3 x 3 convention, 659-1,565
   rows) against 6 calendar months (monthly refit, 978-2,231). No source cadence for either; SPLIT-21 forbids picking
   by score. melbourne and perth cite house_sales. Decision: the window length for the house-price family.
4. **`yr_renovated` 0 as missing (P7, CLEAN-10 Should).** 0 means "never renovated", a meaningful code; the
   definition sets 95.7% to missing. Precedents keep such codes (bank_marketing `pdays = -1`, house_prices_nominal).
   Fact that could set it apart: after the rebuild NaN means only "never renovated" (no other missingness), and a 0 in
   a year column misleads linear models. Decision: record that as an exception, or keep 0 / add a renovated flag.

**Agreed facts**

- Rows are King County recorded sales (21,386 of 21,613 match on parcel, date, price); `date` is the deed date
  (= `DocumentDate`), not the recording date (the practitioner's "recording date" is refuted by the split audit).
- The file's house features are the assessor's record of 18-19 July 2015 (17 July 0/29 old==file, 20 July 55/55); the
  change log's value is the old value.
- Strong leak, fixed by the rebuild: 2,151 rows changed; LightGBM on them 0.156/0.148 with file values vs
  0.208/0.194 rebuilt (definition, claim audit), 0.156 vs 0.193 (clean room, blind).
- `sqft_lot` is not rebuilt: lot changes live under `LandFootage` (0/139 before, 127/130 after); 81 rows; score
  effect nil.
- 6.8% of rows carry non-market or non-representative county warnings; per-code effect above.
- Recording delay median 6 days, 91% within 14; shortcut about 0.6% RMSE; gap=1 keeps 9 windows.
- July-2015 remnants carry no measurable post-sale signal (view mask 0.2147 vs 0.2132; neighbours +0.004).
- Split: temporal regime right; parcel grouping changes nothing (0.1619 vs 0.1632); SPLIT-11/14/15/17 hold.
- Probes: no flags; skill +0.884, linear +0.852, drift +0.002.
- 6 placeholder living areas 8-200 sq ft; resale RMSE 0.27 vs 0.17; 160 repeated houses.
- Untested: the Coursera SFrame holds the same table; the 2014-2015 log events stay unchanged across downloads.

**Consistency with precedent**

- Rebuild (PROV-13, LEAK-10): follows SUPPORT2, ashrae, zillow_prize; the LEAK-10 Cases row already names house_sales.
- Warning 26 kept vs california_house_prices_2020 (rows dropped): set apart by the measured fact that 1,096 of 1,225
  are not rebuilt because their changes postdate the snapshot, and they sit below the model (-0.118), so the file
  holds the at-sale record; in california the listing described another sale. Record as the answer to the
  consistency check.
- View/waterfront kept vs melbourne (blanked): set apart because blanking 145 rows would make missingness mark a
  post-sale change, and masking shows no signal. Record the fact.
- Gap: change 3 aligns with zillow_prize (gap for the same county-recording delay); carry it to perth_house_prices and
  melbourne_housing_market, which cite house_sales for "no gap".
- Fit: siblings melbourne and zillow say direct with remnants; rules beat precedents, so they follow issue 2.
- Citation: nyc_taxi_trip_duration shares the Kaggle-bibtex pattern; airfoil_self_noise cites the original. Change 8
  follows airfoil; flag nyc_taxi.
- Placeholders: change 7 follows heart_disease_va_long_beach, sdss_17 and the definition's own 0-bedroom rule.
- Repeated sales kept: consistent (melbourne, zillow); california's newest-only dedup is the outlier to reopen, and
  its `min_train_fraction=0.25` contradicts SPLIT-14 (flag, do not follow).
- May 2015 dropped: consistent (house_prices_nominal, zillow), set apart from perth/Ames by measured 24% coverage.
- Non-market filter: no curator precedent on sale warnings yet; this sets one for the house-price family (USE-5 cases
  corporate_credit_rating, california's dropped rows).

</details>

<details><summary>Claim audit</summary>

Data: the definition's frame and splits before this review's changes (20,967 rows, 9 windows), its raw files, and three
county extracts downloaded for this audit: `Real Property Sales.zip` (EXTR_RPSale.csv, 2026-10-19), `Parcel.zip`
(EXTR_Parcel.csv), `Lookup.zip` (sale warning codes). The full change log was rescanned for every (record, attribute)
of the file's parcels in 2014-2015. Models: untuned LightGBM (400 trees, lr 0.05), mean of 3 seeds, on the 9 shipped
windows, RMSE of log price.

**Claim table**

| # | claim | source | test | result | evidence | rule |
|---|---|---|---|---|---|---|
| 3, 41 | 20,967 sales; price $75,000 to $7.7M | D task_summary, notes | count, exp(min/max) | holds | 20,967; 75,000 / 7,700,000 | - |
| 7, 45, 47 | 9 three-week windows, late Oct 2014 to Apr 2015, newest first; oldest trains on 54% | D | shipped splits | holds | train 11,253-19,402, test 659-1,565; 11,253/20,967 = 53.7% | SPLIT-14 |
| 46 | 9 windows = the 3 x 3 an IID task of this size gets | D splits_comment | `recommended_dimensions`: n_train 13,978 < 250k -> 3 repeats x 3 folds | holds | src/data_foundry/v2/splits.py:92 | SPLIT-15 |
| 48 | monthly windows: 6 of 978-2,231 | D splits_comment | monthly counts + 50% floor | holds | Nov 2014-Apr 2015 = 1,411..2,231 (min 978 Jan); Oct window would train on 47% | SPLIT-14 |
| 8, 25, 50 | the file's house features are the assessor's record of 18-19 July 2015 | D constants, Decision 2 | per-day share of change old value == file value, 6-27 July 2015 | holds | 17 July: 0/29; 20 July: 55/55; 21-22 July 0.77-0.80; 23-27 July 0.95-1.00 | LEAK-10, EV-1 |
| (implied) | `AttributeValue` in the change log is the OLD value | D `_parse_changes` | latest bath change per parcel vs today's count in the building file | holds | equal in 9.4% of 11,556 (a new value would be ~100%) | EV-1 |
| 26 | 2,151 of 20,967 rows changed between sale and snapshot | D notes, Decision 1 | rerun `_as_of_sale` | holds for the columns it reads; understated overall | stats reproduce (2,151; baths 913/5; blank 10); but see claim 28 (81 lot rows missed) | LEAK-10 |
| 27, 57, 62 | file values flatter the model: 0.156 vs 0.208 on the rebuilt rows; all rows 0.1727 vs 0.1761, 8 of 9 windows | D notes, R, REVIEW | LightGBM file vs rebuilt, same windows | holds (direction and size; numbers differ slightly, EV-8) | rebuilt test rows (849): 0.148 vs 0.194; all: 0.1676 vs 0.1717, rebuilt worse in 8/9 | LEAK-10 |
| 28 | sqft_lot is rebuilt like the other columns | D notes, `CHANGED_COLUMNS` | rescan the change log for every record holding `SqFtLot` | **refuted** | lot size changes live under record `LandFootage` (269 events 2014-15), not `Land` (191). Snapshot test on LandFootage: before 18 July 0/139 old==file, after 127/130 (97.7%): it is the file's source. 81 kept rows have a LandFootage change between sale and snapshot with old != file (55 lots shrank, segregations); the rebuild changes 0 | LEAK-10 (Must) |
| 29, 49 | bathrooms rebuilt for 913 rows, kept for 5 | D notes, Decision 1 | rerun | holds | 913 / 5 (869 net changes) | - |
| 30 | sqft_above = sqft_living - sqft_basement in every file row | D notes | checklist measured | holds | (checklist) | - |
| 11 | "the features describe the house as it was sold" | D fit_reason | residual of the rebuilt-data model on rebuilt rows; correlation of (file-pred - rebuilt-pred) with the rebuilt residual | **refuted (wording)** | rebuilt rows without warning 26 (2,022; 798 test): mean residual +0.079 vs +0.009 on untouched rows; corr(shift, residual) = 0.586: the post-sale changes move toward the price, i.e. the record at the sale understated the house that sold (stale record corrected after the sale). The features are the assessor's record on the sale day, not the house as sold | USE-3, writing |
| 33 | yr_built rebuilt for 24 rows, mostly teardowns | D notes | inspect the 24 | holds | 16/24 show a house built in or after the sale year replacing an older one (county flags only 1 with warning 10) | - |
| 34 | 6 houses under construction, living area 8-200 sq ft | D notes | count | holds | 8, 33, 44, 56, 100, 200 | CLEAN |
| 35, 12 | 1,225 sales flagged warning 26, kept as noise | D notes, fit_reason | county sales extract, match on parcel+date+price | holds | 1,225 of 20,742 matched kept rows; 1,096 of them not rebuilt, their first tracked change mostly 2015-2017 (after the snapshot); residual -0.124 (bought as fixers, improved later): noise, not leak | LEAK-11 |
| 15, 56 | 21,386 of 21,613 rows match a county sale on parcel, date, price | D download_description, R | merge with EXTR_RPSale | holds | 21,386 (21,440 on parcel+date) | PROV-1 |
| 22, 36, 51 | May 2015 incomplete, the sales list extracted mid-May; 646 rows (3.0%) | D constants, notes, Decision 3 | recording dates of the matched rows | holds in substance | 646 (2.99%); recordings run to 15 May (134 that day), then 2 on 18 May and 1 each on 28 May, 1 and 2 June: the extract is no earlier than 2 June, the bulk stops 15 May | LEAK-24 |
| 51 | 24% of May's sales made it in vs 80-89% earlier | Decision 3 | proxy: matched / county sales PrincipalUse 6, price > 0 | untested as stated (the "kind the table holds" filter is not given); proxy agrees in direction | proxy 18.5% May vs 53-68% May 2014-Apr 2015 | EV-8 |
| 37 | 159 houses sold twice, one three times | D notes | id counts | holds | {2: 159, 3: 1} | LEAK-17 |
| 38 | resales RMSE 0.36 vs 0.17 | D notes | LightGBM rebuilt data, test resales | **refuted (number)** | 151 test resales: 0.270 vs 0.170 others; the direction holds, 0.36 does not reproduce | EV-8 |
| 43, 44 | no duplicate rows; 9 pairs of different parcels share every feature | D notes | duplicated() | holds, wording loose | 0 full duplicates; 2 rows share all features incl. date; 318 rows in 158 groups share all features but the date (mostly resales of an unchanged house) | LEAK-16 |
| 40 | zeros to missing | D notes | counts | holds | 13 bedrooms, 18 bathrooms, 20,112 yr_renovated now missing. GeoDa quote not checked | CLEAN |
| 32, 64, 6 | view, waterfront, neighbours' areas left as of July 2015; 154 rows had a view/waterfront attribute changed | D notes, REVIEW | change log rescan; mask view on those rows | holds (count differs by method) | 143 rows with a Land view attribute changed sale->snapshot (183 incl. waterfront detail attributes); masking their view: RMSE 0.2147 vs 0.2132 kept: no signal from the post-sale value | LEAK-11 |
| 32 (implied) | waterfront cannot be rebuilt | D notes | today's parcel `WfntLocation > 0` vs file `waterfront` | refuted in passing, no effect | 99.2% agree: waterfront is a county attribute; 2 rows changed WfntLocation post-sale. `view` is not an exact function of the county view scores (max matches 93.2%, 69% on view > 0): its claim holds | - |
| 10 | fit direct | D | USE-8 categories against the measured leftovers | holds, conditional on 11 being reworded | the leftovers (view, lot, neighbours) carry no measurable post-sale signal (LEAK-11, kept with a note) | USE-8 |
| 61 | changes after a sale come a median 112 days after it | REVIEW | days sale -> first post-sale change (rebuilt rows) | holds approx. | median 109 days | - |
| 17 | md5 b1e7bdf4... | D | md5sum | holds | b1e7bdf4f3e61792c0979a5697dc7145 | PROV |
| 16, 21, 54 | first distributed with the UW Coursera course (2015); year 2015 (record: 2016) | D bibtex, R | Coursera repo file (Git LFS pointer -> media download) | year holds; "same table" untested | `kc_house_data.gl.zip` (930,178 B) holds an SFrame dated 2015-11-06; SFrame not readable here. Record `year: 2016` disagrees and is the weaker value | PROV-8 |
| 18 | change log 1.8 GB, updated weekly | D | file size | size holds; weekly untested | 1,836,988,142 bytes | - |
| 65 | the 2014-2015 events do not change | REVIEW | needs a second download of the 1.8 GB log | untested | only the Oct 7 copy is on disk | reproducibility |
| 63 | 1,957 rows with a rebuilt main column | REVIEW | "main column" not defined | untested | - | - |
| 14 | CC0 | D | Kaggle (checklist) | holds for Kaggle; county terms unchecked | EV-4: not evidence either way | EV-4 |
| (implied) | every training row's label is known at the refit ("trained on all earlier sales") | D use_case, split | county recording lag; training filtered to sales recorded before each window | **maybe refuted, small** | lag median 6 d, 90.8% within 14 d, 98.3% within 28 d; the as-of-recording filter drops 217-501 training rows per window; RMSE 0.1717 -> 0.1733, worse in 7/9 (a full 14-day gap: 0.1742, 9/9) | SPLIT-9 / LEAK-12 (Must) |
| (implied) | the target is the market price an AVM estimates | D question, predicted | county sale warnings on the kept rows | **refuted in part** | 1,420 kept rows (6.8%) carry a non-market or non-representative warning: 15 no market exposure 654, 46 non-representative 357, 10 tear down 322, 60 short sale 199, 29 segregation 104, 51 related party 90, 12 estate 42. Test RMSE 0.25-0.31 vs 0.151 unflagged, residual -0.14 to -0.23 (sold below the model). Not mentioned anywhere | USE-5 (Must), CLEAN |
| (implied) | no row is a copy across the split | - | duplicates excluding date | holds as designed | 158 groups identical but for the date, mostly resales whose earlier sale is in train: a known-entity AVM sees the earlier sale (USE-10) and the definition documents it | LEAK-17, USE-10 |
| (implied) | every feature is known at the prediction point | - | above | holds except sqft_lot (81 rows) and the documented weak leftovers | - | LEAK-10 |

**Refuted and untested, ranked (validity first, Must first)**

1. **sqft_lot is not rebuilt (P4, LEAK-10 Must; claims 26, 28, Decision 1 table).** `CHANGED_COLUMNS` maps
   `("Land", "SqFtLot")`, but the file's lot size follows the `LandFootage` record (snapshot test 0% before / 97.7%
   after 18 July). 81 kept rows (35 in test) keep a post-sale lot, 55 of them smaller than at the sale (segregations).
   Effect on the score is nil (those test rows 0.322 shipped vs 0.326 rebuilt), so it is a correctness bug, not a
   strong leak. Changes: the "2,151 rows" count, the sqft_lot row of Decision 1 (0 -> ~81), the notes' claim.
   Mildest remedy: add `("LandFootage", "SqFtLot"): "sqft_lot"` (keep `Land` too) and re-run `_prepare_raw_files`.
2. **The target includes non-market sales (P3, USE-5 Must; implied).** 6.8% of rows carry county warnings for no
   market exposure, short sales, related parties, non-representative and teardown sales; they are the worst-predicted
   rows and systematically below the model. A lender's or the assessor's AVM targets market value; the county itself
   flags these sales. Changes: what the target means for 1 in 15 rows. Mildest remedy: a note naming the share
   (keep, as label noise) or, better, drop the rows with the non-market warnings (15, 46, 60, 51, 12, 13, 23, 10), which
   needs the 150 MB sales extract as a raw input; curator's weighing call.
3. **"The features describe the house as it was sold" (P3/P4, USE-3; claims 11, 33 wording).** The rebuilt record is
   what was known on the sale day, but for the rebuilt rows it understated the house that sold (residual +0.079; the
   post-sale shift correlates 0.59 with the residual). The data choice stands (LEAK-10); the text overclaims, and the
   use case's "lenders or property sites" work from listing data that the post-sale record resembles more. Mildest
   remedy: reword fit_reason/use_case to "the assessor's record on the sale day" and an AVM or mass appraisal working
   from public assessor records.
4. **Labels not yet recorded at the refit (P4, SPLIT-9/LEAK-12 Must; implied by "trained on all earlier sales").**
   Recording lag median 6 days; an as-of-recording filter costs 0.0016 RMSE (7/9 windows). Maybe a leak, small, and it
   depends on whether the actor sees recordings (county) or closings (MLS). Mildest remedy: one sentence in
   splits_comment; a 2-week `time_gap` if the use case is the county-record AVM.
5. **Resale RMSE 0.36 vs 0.17 (claim 38; EV-8).** Reproduces as 0.27 vs 0.17. Remedy: restate with how it was measured.
6. **Wording (writing):** "9 pairs share every feature" holds only without the date; "extracted mid-May" holds for the
   bulk but 5 rows were recorded 18 May-2 June; waterfront is a county attribute (`WfntLocation`), 2 rows changed.
7. **Untested:** the Coursera SFrame holds the same table (claim 16; SFrame unreadable here, file dated 2015-11-06
   supports year 2015 over the record's 2016); weekly updates and unchanged 2014-2015 events (claims 18, 65: need a
   second 1.8 GB download); the 24% vs 80-89% shares (claim 51, filter not stated; proxy agrees); 1,957 rows (claim 63,
   "main column" undefined); GeoDa quote (claim 40); county licence terms (EV-4, not evidence).

</details>

<details><summary>Column audit</summary>

Prediction point (first `curation_comments` bullet): a house sells; the price is predicted from the assessor's record
on the sale day and the location, by a model trained on all earlier sales (AVM). Frame loaded through
`dataset_io.from_definition` (20,967 rows x 20 columns, temporal on `date`, 9 windows). Codebook: GeoDa
"KingCounty-HouseSales2015" page (the Kaggle discussion 207885 repeats it); county meanings from the change-log
attribute names the definition maps.

**Column table**

| column | meaning | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| `date` | date sold (GeoDa) | yes, the prediction day | datetime `%Y%m%dT%H%M%S`, time column and feature; 355 days, 2014-05-02..2015-04-30 | fine | CLEAN-14, SPLIT |
| `log_price` (target) | log of the sale price | outcome | float, log of a positive skewed price, renamed; 11.23..15.86, no cap | fine | CLEAN-16, LEAK-26 |
| `bedrooms` | number of bedrooms (county `Bedrooms`) | yes after the rebuild | float; 0 -> NaN (13 rows); max 11 (the Kaggle 33-bedroom typo is rebuilt to 2 from the log) | fine | LEAK-10 fixed, CLEAN-10 |
| `bathrooms` | full + 0.75 x three-quarter + 0.5 x half baths (county counts) | yes, rebuilt for 913 rows; 5 rows keep the July 2015 value | float, all multiples of 0.25; 0 -> NaN (18 rows, mostly new construction) | fine (5 residual rows noted) | LEAK-10, CLEAN-10 |
| `sqft_living` | total living area, county `SqFtTotLiving` | yes, rebuilt (676 rows; file higher in 585) | int; 6 rows 8-200 sq ft with 3-5 bedrooms (placeholders of houses under construction) | cleaning problem | CLEAN-11 |
| `sqft_lot` | lot area, county Land `SqFtLot` | yes in practice: listed as rebuilt but 0 rows change (2 post-sale Land changes, both blank) | int, 520..1.65M | fine (note wording) | LEAK-10 |
| `floors` | stories (county `Stories`) | yes, rebuilt | float 1..3.5 in halves | fine | |
| `waterfront` | 1 if waterfront (GeoDa) | July 2015 value; 2 rows had `WfntLocation` change between sale and snapshot | int 0/1, 160 ones | weak leak, keep with note | LEAK-10 (weak), LEAK-11 |
| `view` | index 0-4 of how good the view was (GeoDa); not a county attribute, derived from the Land view ratings | July 2015 value; 145 rows (0.7%) had a Land view rating changed between sale and snapshot, 39 of them gained a rating from blank/0 and show view > 0 | int 0-4 | weak leak, keep with note | LEAK-10 (weak) |
| `condition` | condition 1-5 (county `Condition`, Poor..Very Good) | yes, rebuilt | int ordinal | fine | CLEAN-14 |
| `grade` | construction quality 1-13 (county `BldgGrade`) | yes, rebuilt | int ordinal | fine | CLEAN-14 |
| `sqft_above` | living area above ground | yes, recomputed per row as `sqft_living - sqft_basement` (holds in 100% of file rows) | int; inherits the placeholders (8-200) | fine; follows `sqft_living` | CLEAN-11 |
| `sqft_basement` | finished basement area (county `SqFtFinBasement`; GeoDa says "square feet below ground") | yes, rebuilt | int, 0 = no finished basement (real zero) | fine (meaning note) | |
| `yr_built` | year built (county `YrBuilt`) | yes, rebuilt for 24 rows (teardowns); 414 rows built in the sale year, 5 rows yr_built 2015 for a 2014 sale (presales) | int | fine | |
| `yr_renovated` | year renovated, "0 if never renovated" (GeoDa) | yes, rebuilt; after rebuild 0 rows renovated after the sale year (6 in the file) | float; 0 -> NaN (95.7%); NaN means "never renovated (or none recorded)", the notes call it "unrecorded" | fine (wording) | CLEAN-10 |
| `zipcode` | 5-digit ZIP | yes | categorical (text, leading zeros kept), 70 levels, all seen in train | fine | CLEAN-14 |
| `lat` | latitude | yes | float | fine | |
| `long` | longitude | yes | float | fine | |
| `sqft_living15` | average living area of the closest 15 houses (GeoDa) | July 2015 record of the neighbours | int (multiples of 10); not computed from the file's rows (15-NN over the file: corr 0.80, exact 1.2%), so no transductive leak from our test rows | weak leak, keep with note | LEAK-10 (weak) |
| `sqft_lot15` | average lot area of the closest 15 houses (GeoDa) | July 2015 | int | weak leak, keep with note | LEAK-10 (weak) |

Dropped by the definition: `id` (parcel number; read as text, used for the rebuild and the resale table): correct
(CLEAN-3, not a group column under the temporal split).

**Measurements**

* Ablation on the 9 shipped windows, LightGBM 400 trees, RMSE on the 2,151 rebuilt rows / the other rows:
  all features 0.1989 / 0.1705; without `sqft_living15`, `sqft_lot15` 0.2026 / 0.1710 (+0.0037 / +0.0005); without
  `view`, `waterfront` 0.2035 / 0.1820 (+0.0046 / +0.0115); without all four 0.2080 / 0.1825. View and waterfront help
  the other rows more than the changed rows: no sign of a post-sale signal. The neighbours' areas help the changed rows
  7x as much as the others, but by 0.004: weak at most. Excluding the placeholders, `sqft_living15` is as close to the
  rebuilt living area as to the file's (median |log ratio| 0.199 both): it does not track the house's own post-sale
  change.
* View and waterfront in the county change log (full 1.8 GB scan, Land view ratings and `WfntLocation`, 2014-2016,
  file parcels): 145 kept rows changed between the sale and 18 July 2015 (Territorial 85, Puget Sound 45, Olympics 24,
  Lake Washington 22, ...; 2 `WfntLocation`), 60 before the sale, 397 after the snapshot. 73 of the post-sale changes
  had a blank old value; 39 rows gained a rating after the sale and show `view` > 0 in the file.
* Full-record events: 47 kept rows have a Bldg 1 event logging 10+ attributes at once between the sale and the
  snapshot; 23 of them are rebuilt, the other 24 are not because the logged value equals the file (25 of 47 are new
  construction). These look like a record entered or re-entered after the sale (e.g. a 2014-10-31 sale with
  yr_built 2014, every attribute logged 2015-06-05); whether the house was in the record at the sale cannot be told
  from the log.
* New construction (yr_built >= sale year): 419 rows, 87 rebuilt; 144 of the others have no change-log event at all.

**Problems, ranked (principles.md)**

1. **P3/P4 question for the curator: `fit = "direct"` with post-sale values kept (USE-8, LEAK-10, LEAK-11).**
   `view`, `waterfront`, `sqft_living15`, `sqft_lot15`, the 5 bathroom rows, the 10 blank old values and the 1,225
   rows the county flags with warning 26 stay as of July 2015. USE-8 lists "a potential leak kept on purpose" as
   approximate; LEAK-10 keeps a looked-up attribute only "where the data shows they did not change", and 145 rows'
   view or waterfront did change after the sale. Evidence that the remnant is weak: the ablation above (no
   disproportionate gain on changed rows; at most +0.004 RMSE). Mildest remedy: turn the "We leave ..." bullet into a
   `Potential leak, kept on purpose:` bullet with these numbers (145 view/waterfront rows, 39 gained a view; ablation)
   and either set the fit to approximate or state why direct holds (the remnant is measured as weak). Do not blank the
   145 view values: the missingness would itself mark "changed after the sale".
2. **P4 question: the 1,225 warning-26 rows (LEAK-10).** How many of them the rebuild repaired is not stated and cannot
   be measured here (the sales extract is not in the raw folder). If most are unrepaired, their features still hold
   post-sale improvements. Remedy: report the overlap with the 2,151 rebuilt rows in the notes; keep as noise when the
   unrepaired share is small.
3. **P4, small: 24 rows with a full-record Bldg 1 event after the sale that the rebuild leaves (LEAK-10).** Possibly a
   building record entered after the sale. 0.1% of rows; remedy: mention in the notes, or treat a post-sale full-record
   event as "unknown at sale" and leave the row as noise. No action needed beyond a note.
4. **P7 cleaning: placeholder living areas (CLEAN-11).** 6 rows (sqft_living 8, 33, 44, 56, 100, 200 with 3-5 bedrooms;
   `sqft_above` follows) are impossible as areas: the record of a house under construction. Mildest remedy: set
   `sqft_living` and `sqft_above` to missing where the living area is under ~300 sq ft with bedrooms recorded (the
   290 sq ft row with 0 bedrooms and 0 baths may be a real cabin: leave it). The missingness is known at the sale, so
   it is not a leak. Cheap and safe; or keep with the existing note (earlier issue 5).
5. **P7 wording (writing.md):** `yr_renovated` 0 means "never renovated" per GeoDa; the notes call it "unrecorded"
   (the NaN is right, the reason is not). `sqft_basement` is the finished basement area (the definition maps
   `SqFtFinBasement`), not "below ground" as GeoDa says. `sqft_lot` is named among the rebuilt columns but no row
   changes.

Fine without remarks: `date`, `log_price`, `bedrooms`, `floors`, `condition`, `grade`, `yr_built`, `zipcode`, `lat`,
`long`; `id` correctly dropped.

</details>

<details><summary>Split audit</summary>

**Verdict: right with notes.** The temporal regime fits the use case. The windows match every claim. One Should is
open: there is no gap for the delay before a sale is recorded (SPLIT-10), and the measured effect is small.

Scope: `dataset.py` before this review's changes (20,967 rows, regime `temporal_non_iid`, time column `date`). The
recording dates come from the county's `EXTR_RPSale.csv`. The model is LightGBM with 600 trees and lr 0.05, untuned,
3 seeds unless stated otherwise.

**Regime (USE-10, SPLIT-1, SPLIT-3, SPLIT-6): holds**

- The use case is an AVM that values a house on its sale day and is trained on earlier sales. That is a fixed
  predictive task with a sale price as its label, which SPLIT-6 names explicitly, so a temporal split is required.
  Declared: Temporal on `date`, with an expanding train side. This matches.
- New entity or known entity: an AVM values any house, including houses that sold before. The previous sale is
  legitimate history (USE-10). Resales are 0.4-2.5% of the test rows per window (5 to 30 rows). `id` is dropped, so
  the earlier price is not a feature, and a resale can only be recognised through the house's features.
- Comparison with the alternative splits, 3 x 3 folds:
  - IID: RMSE 0.1632 +- 0.0016.
  - Grouped by parcel: 0.1619 +- 0.0007.
  - Grouping by parcel does not change the score, so there is no hidden-entity effect.
- On the same 9 test windows (1 seed):
  - temporal train: RMSE 0.1729;
  - a random train of the same size that includes later sales: 0.1711.
  - The temporal split costs about 1% RMSE, which is the real drift. The split follows the application regardless
    (SPLIT-4).
- Hidden-group probe: `zipcode` is seen for 100% of the test rows. It is a feature that every new sale has (SPLIT-4),
  not an entity. Near copies at 0.85: 8.0% of the test rows have one in train (townhouses of one development). These
  are comparable sales an AVM legitimately uses. No action.

**Time column and windows: the claims hold**

- `date` is the deed date: it equals the county's `DocumentDate`, and 21,386 of the 21,613 sales match on parcel, date
  and price. It is not the recording date, so it is the right moment for the prediction point.
- Windows, as rebuilt (claims 45 and 47):

| window | test dates | test rows | train rows | train share |
|---|---|---|---|---|
| 0 | 2015-04-10 to 04-30 | 1,565 | 19,402 | 92.5% |
| 1 | 03-20 to 04-09 | 1,459 | 17,943 | 85.6% |
| 2 | 02-27 to 03-19 | 1,137 | 16,806 | 80.2% |
| 3 | 02-06 to 02-26 | 995 | 15,811 | 75.4% |
| 4 | 01-16 to 02-05 | 711 | 15,100 | 72.0% |
| 5 | 2014-12-26 to 2015-01-15 | 659 | 14,441 | 68.9% |
| 6 | 12-05 to 12-24 | 940 | 13,501 | 64.4% |
| 7 | 11-14 to 12-04 | 1,048 | 12,453 | 59.4% |
| 8 | 10-24 to 11-13 | 1,200 | 11,253 | 53.7% |

- In every window the newest training date is before the oldest test date, and no day is split between train and
  test.
- SPLIT-14 holds: there are at least 3 windows, and the smallest train side is 53.7%.
- SPLIT-11 holds: the train side expands and the newest window comes first.
- SPLIT-17 holds: the smallest window has 659 rows, far above 50.
- SPLIT-15: 9 windows equal the 3 x 3 an IID task of this size would get.

**Problems, ranked (all under P4; none is a Must)**

**1. SPLIT-10 (Should): no gap for the delay before a sale is recorded**

- **Evidence.** A refit AVM learns a sale's price once the deed is recorded. Over the 21,106 sales with a recording
  number, the delay from the deed date to the recording date is:
  - median 6 days, 90th percentile 14, 99th percentile 26;
  - 68% of sales recorded within 7 days, 91% within 14, 96.5% within 21.
- The delay is stable by month: the median is 5-6 days. The definition's own Decision 3 shows the same delay, since
  the mid-May extract held only 24% of May's sales.
- With gap 0, each window trains on 223 to 503 sales (2-4% of train) that were not yet recorded when the window
  opened. Those are the newest sales, the ones closest to the test window.
- **Effect.** LightGBM, 3 seeds, 9 windows, mean RMSE (R^2), with `date` as a feature:

| variant | RMSE | R^2 |
|---|---|---|
| no gap (shipped) | 0.1729 | 0.8925 |
| train only on sales recorded before the window starts | 0.1740 | 0.8911 |
| 14-day gap | 0.1748 | 0.8901 |
| 21-day gap | 0.1742 | 0.8908 |

  Without `date`, the variants give 0.1743, 0.1748, 0.1749 and 0.1754. The shortcut is worth about 0.6% RMSE. It is
  small but consistent: the shipped split is the best variant in 6 of 9 windows with `date`.
- **Mildest remedy.** Add a one-week gap with `TemporalSplits(window=3, unit="weeks", n_windows=9,
  min_train_fraction=0.5, gap=1)`. Precedent: `aeolus_1m` and `bias_correction` use `gap=1`. One week covers the
  median delay; two weeks (`gap=2`) covers 91%. State the gap and the recording delay in `splits_comment`.
  - Alternative: keep gap 0 with a note. The effect is within 1% RMSE, and a real AVM also sees listing (MLS) data
    before the deed is recorded. This keep needs the curator's call as an exception to SPLIT-10, with that fact named.

**2. SPLIT-20 (Should): the training history and seasons (note only)**

- **Season of the test windows.** All 9 windows fall between late October and April, the low season.

| month | sales | median price |
|---|---|---|
| June-July 2014 | about 2,200 | $465k |
| January 2015 | 978 | $438k |
| April 2015 | 2,231 | $477k |

  April 2015 is above every training month: the 2015 Seattle price rise. Summer is never tested.
- **Training history.** The oldest window trains on May-October 2014 only. Even the newest window has about 11 months
  of history, not a full season before it.
- These limits are inherent to 12 months of data under the 50% floor of SPLIT-14. No re-split fixes them.
- **Remedy.** One sentence in `splits_comment`: the windows cover autumn to spring, and the history is under one
  year.

**3. SPLIT-12 (Should): the horizon is justified by the window count (wording only)**

- The three-week window comes from the 3 x 3 convention (SPLIT-15). It is presented as "a model refit every three
  weeks", but no source cadence is cited.
- The alternative of 6 calendar months (978 to 2,231 rows) would be equally valid. Per SPLIT-21, do not choose between
  them from scores.
- **Remedy.** Say in `splits_comment` that the window length follows the window count, not a cited refit cadence.
  The split stays.

**Checked and fine**

- **SPLIT-9:** every training label is known at the prediction point, apart from the recording delay under
  problem 1. No outcome is censored: a sale price is final when the deed is signed.
- **SPLIT-13:** grouped structure inside the temporal task is limited to the resales above. They are part of the
  task, since an AVM values known houses.
- **SPLIT-22:** `_clean` sorts by date. The frame is date-monotone, and the split uses the date, not the row order.
- **Dropping May 2015** helps the split: a fast-recorded, cheaper partial month would have been the newest window.
- **Out of scope for the split, for the leak auditor (LEAK-10):** `sqft_living15`, `sqft_lot15`, `view` and
  `waterfront` remain as of July 2015. Changes logged on the sale day itself are counted as before the sale
  (`updated.normalize() > sale`).

</details>

<details><summary>Domain practitioner</summary>

Reviewer role: a valuer who would use the predictions. I am thinking of the King County assessor's residential
appraiser, who keeps this record and values every parcel each year from recent sales, or an analyst who runs an
automated valuation model (AVM) for an iBuyer or a property site. Read: `dataset.py` (task_summary, curation_comments),
the record, `use_case.md`, the panel's claims, checklist and probes, and the earlier REVIEW.md. Measured on the raw CSV: sale
dates by weekday (Mon-Fri 3,685-4,715 sales each, Sat 287, Sun 230) and prices (min $75,000; 173 sales under $150,000).

**Fit**

**Direct; the stated fit holds (USE-8).** Each row is one recorded sale. The inputs are the assessor's record of the
house as it stood at the sale, plus its location. The label is the price that was recorded, and the split tests the next three weeks of
sales with a model trained on everything before them. This is how a hedonic valuation model is used: the assessor's own
mass-appraisal model, or an AVM that works from public records. The parts left from July 2015 are small and named in
`fit_reason`: view and waterfront (154 rows changed), the neighbours' areas, and 10 blank old values plus 5 bathroom rows.

**The four questions, as the valuer**

1. **Inputs at prediction time (USE-3, USE-6).** I have every input in the dataset. After the rebuild, the house
   features describe the record on the day of the sale, which is what the leak rules ask for. Two inputs I would always
   have are missing. The first is **the assessor's own appraised value** (land plus improvements, set for the tax year
   before the sale). The second is **the house's previous sale price and date**, which come from the county sales history
   going back decades. Every AVM uses both, either as an input or as the baseline it must beat. Neither is in the Coursera
   file. Per USE-6 an estimate made before the outcome is a legitimate input. Adding it would turn the task into "refine
   the assessor's value", which is a different task. The task without it (value from characteristics and location) is
   still a real use: it is the model the assessor runs to produce that value. So this gap does not break the fit, but
   the summary should name it. View and the neighbours' areas are July 2015 values. I would have the earlier ones, but
   they barely move.
2. **Target (USE-5).** The sale price is what I act on: an assessed value, an offer, a collateral check. Log price at
   one-dollar resolution is right. RMSE on the log is about a percentage error, which matches how AVM accuracy is judged.
   The industry reports median absolute percentage error, the share within 10% (PPE10) and the bias. I want a number,
   not a class.
3. **One row = one decision; test = what I face (USE-10, USE-11).** One sale is one valuation, and the next three weeks of
   sales are what I face. Most houses in a window are new to the model (160 resales in the year). That is right for a
   one-year file, although in practice nearly every house has an earlier sale on record (see gap 1). Two timing details
   matter. (a) `date` is the deed's recording date: sales cluster on weekdays (287 and 230 on Saturday and Sunday), and
   the price was agreed weeks earlier. (b) A refit on the first day of a window would not yet have every sale that closed
   just before it. The curation's own May 2015 evidence shows this: two weeks into the month, only 24% of the month's
   sales had been recorded, against 80-89% in the earlier months. The split trains on every sale up to the day before
   the window, so it is slightly optimistic.
4. **Would I use it?** As a benchmark of hedonic valuation, yes. I trust it because of the temporal split, the as-of-sale
   rebuild, the dropped truncated month and the resale table. I would distrust a model from it in production for four
   reasons: it covers one year (no second seasonal cycle), it has no earlier sale or assessed value to anchor on, the
   sales were never validated as market sales, and the error is not reported by price band, where AVMs fail at the top
   end.

**Gaps between the dataset and the real decision, ranked by how much they change the task**

1. **Two inputs a valuer always has are missing: the assessor's appraised value and the house's previous sale (USE-6).**
   This changes the task the most. With them, the task becomes "refine an existing estimate" (higher R^2, a different
   difficulty). The source file never had them, so the curation did not remove anything. The county's extracts would
   provide both (the definition already downloads two county extracts). Recommendation: keep the task as a model from
   characteristics only, and say so in `use_case`/`fit_reason` ("without the assessor's value or the previous sale
   price"). Adding them is the curator's choice. It would be a second, equally real use case.
2. **The actor and the moment in `use_case` (USE-1, USE-9).** The text says "lenders or property sites ... estimate a
   house's price on the day it sells". A lender financing a purchase knows the contract price, so it uses an AVM only as
   a check, and property sites mostly value houses that are not for sale. Two actors hold exactly these inputs: the
   county assessor's mass appraisal, and an iBuyer or site estimate made before the sale is recorded. Recommendation:
   reword to "estimates the price a house will sell for from the public record and its location, before the sale is
   recorded". The fit stays direct (USE-9, a well-defined use case), and the "on the day it sells" claim, which the
   recording date does not support, goes away.
3. **Recording lag is not in the split (USE-3, SPLIT).** At a real refit, the last two to four weeks of closed sales
   are not yet in the training data. The effect is probably small: the drift baseline scores skill +0.002, so prices move
   slowly within a three-week window. A gap of about three weeks between training and test would mirror it. Worth one
   probe. I would not block on it.
4. **The sales are not validated as market sales.** An expert values against market transactions only, which means
   excluding sales between relatives, foreclosure and bank sales, estates, partial interests and sales the county flags
   with warnings. Nothing shows whether the course file filtered these out. There are 173 sales under $150,000 (min
   $75,000). The 1,225 rows with warning 26 suggest that warnings were not filtered. This run cannot check it, because the
   county sales extract with its warning and instrument codes is not in the raw folder. It changes the noise in the tails,
   not the task. At the least, name it in the notes. Better, read the sales extract and drop sales that were not at
   market value, as the assessor does.
5. **The parts left from July 2015 (USE-8).** View and waterfront (154 rows), the neighbours' areas, and 15 values
   left as in the file. These are named in `fit_reason` and small. They do not move the fit away from direct.
6. **Wording.** `sqft_lot` is listed among the rebuilt columns, but no row changes (checklist). Decision 1 says "913
   bathrooms rebuilt", but its table shows 869 rows with a changed value. "9 pairs share every feature" should be "every
   feature but the date". None of these change the task.

**What a domain expert would change**

- Reword `use_case` as in gap 2. Add "without the assessor's appraised value or the previous sale price" to `known` or
  `fit_reason`.
- If the county sales extract is downloaded, keep the market sales only: the assessor's validated sales, with no
  warnings that exclude a sale. If not, name the open question.
- Optionally probe a three-week train-test gap for the recording lag.
- For readers: name MdAPE, PPE10 and the bias by price band as the measures an AVM is judged by. RMSE on log price stays
  the benchmark metric.
- Keep the as-of-sale rebuild. Many of the changes after a sale come from the sale itself: the sale prompts a re-inspection, or the new owner
  renovates. Neither is known when the house is valued for that sale.

**Rules cited**

USE-1, USE-3, USE-5, USE-6, USE-8, USE-9, USE-10, USE-11 (`.claude/skills/knowledge-curation/references/use_case.md`).

**Sources**

- `dataset.py`, the curation record, the panel's claims list, checklist and probes, the earlier REVIEW.md.
- `kc_house_data.csv`: weekday counts and price tail, measured in this review.
- King County Assessor data download: https://info.kingcounty.gov/assessor/DataDownload/default.aspx
- King County Assessor property look-up and records: https://kingcounty.gov/es-es/dept/assessor/buildings-and-property/property-value-and-information/look-up-property-information
- AVM accuracy metrics (PPE10, MdAPE, bias): https://valuations.andrewgadsden.com/knowledge/accuracy-metrics
- AVM inputs (public records, MLS, comparable sales; hedonic regression): https://batchdata.io/blog/data-accuracy-vs-avm-reliability
- Sales validation and ratio-study practice in a neighbouring county: https://www.snohomishcountywa.gov/DocumentCenter/View/3832

</details>

<details><summary>Blind review</summary>

**Verdict**
Include with changes. The task is a real, well-understood valuation problem with strong but non-trivial signal and an honest temporal split. However, about 10% of the rows carry house attributes that differ from the cited public source, and nothing in the clean room documents where those values come from. That provenance has to be documented, and a handful of implausible values have to be fixed, before the dataset goes in.

**What the task is**
This is automated valuation (AVM). Assessors, lenders and iBuyers predict a home's sale price from its physical attributes and location at listing or sale time, for taxation, underwriting or offer pricing. It is a real use. The temporal split (9 test windows after their training rows) matches deployment, since you price new sales with a model trained on past sales.

**Concerns (most to least serious)**

1. **The attribute values do not match the cited source for about 10% of rows, and the change is undocumented.**
   - I downloaded OpenML 42731 (the source named in task.md; 21,613 rows, identical to Kaggle). I matched every prepared row exactly on lat, long, date and price: all 20,967 rows matched.
   - 2,144 rows (10.2%) differ in at least one attribute:
     - condition: 1,202 rows
     - bathrooms: 861
     - sqft_living: 676
     - bedrooms: 582
     - sqft_basement: 544
     - grade: 395
     - sqft_above: 301
     - floors: 95
     - yr_renovated: 61
     - yr_built: 24
   - sqft_lot, sqft_living15, sqft_lot15, view, waterfront, location and price never differ.
   - The differences are systematic, not noise. Prepared values are mostly lower (sqft_living lower in 87% of changed cells, by a median of 400 sqft; yr_built earlier by a median of 67 years). The mismatch rate falls from about 11-14% in 2014 months to about 4-6% in Feb-Apr 2015.
   - Examples look like teardown and rebuild cases:
     - Row 196, sold 2014-05-06. Prepared: built 1964, 100 sqft, grade 7. Kaggle: built 2014, 2,690 sqft, grade 10.
     - Row 3551, sold 2014-06-25. Prepared: built 1957, 900 sqft. Kaggle: built 2015, 3,570 sqft.
   - The Kaggle/OpenML table is a 2015 assessor snapshot. It describes the house as rebuilt after the sale, which leaks the future into the features. The prepared table seems to hold characteristics as of the sale date.
   - This is plausibly an improvement in honesty. With the original attributes, 5-fold LightGBM RMSE on the changed rows is 0.156. With the prepared attributes it is 0.193, which is consistent with the snapshot leaking the post-sale rebuild.
   - Change: document the source of these as-of-sale values (for example a King County Assessor history extract) and the matching procedure in task.md, and link it. If the source cannot be named and verified, revert to the published values and note the snapshot leak instead. As things stand, the data is not "what the cited source claims".

2. **Some values are implausible.**
   - sqft_living takes the values 8, 33, 44, 56, 100 and 200. Kaggle has 3,310, 3,060, 4,000, 3,230, 2,690 and 2,950 for the same rows. The original minimum is 290. These rows sell for $430k to $980k, so the values are probably placeholders from parcels under construction.
   - Row 3753 has sqft_above 22 and sqft_basement 11.
   - 5 rows have yr_built later than the sale year (pre-construction sales). That is acceptable, but should be stated.
   - Change: set sqft values below about 250 to NaN, or drop those rows. Seven rows have sqft_living below 300.

3. **Some features are still post-sale snapshot data.**
   - sqft_living15 and sqft_lot15 are identical to Kaggle. Kaggle describes them as neighbours' values in 2015, so they are partly measured after the sale.
   - yr_renovated equals the sale year in 63 rows. A renovation in the same year could fall after the sale date.
   - The leakage is mild. Change: note it in task.md, or drop the *15 columns. They are of minor importance, given lat/long.

4. **Treatment of zeros, rows and repeat sales.**
   - The cleaning itself is sensible. Bedrooms=0 (13 rows) and bathrooms=0 became NaN. The 33-bedroom row (bedrooms 33 in Kaggle) is now 3, consistent with the as-of-sale source. yr_renovated=0 became NaN (855 non-missing values). zipcode is categorical (70 levels). sqft_above + sqft_basement equals sqft_living in 100% of rows.
   - Rows: 21,613 - 20,967 = 646, exactly the May 2015 rows. Dropping them is fine (a partial month), but the reason should be stated.
   - Repeat sales: 160 houses appear twice. They can fall in both train and test. That is realistic under a temporal split and not a leak, but the house id was removed, so nobody can group by house.
   - There is one exact duplicate feature vector.
   - About 9 bedrooms/bathrooms values were set to NaN where Kaggle has non-zero values (bathrooms 2.5 to 3.5). That is part of the as-of-sale change.

5. **Familiarity.**
   - This is one of the most widely used regression datasets: on Kaggle, on OpenML, and in the Grinsztajn et al. benchmark (OpenML 44989 "house_sales").
   - It adds little diversity. Pretrained or LLM-based methods may have memorised it, although the changed 10% partly mitigates this.

**Signal and difficulty**
- The target std is 0.525. With the last 20% of time as test, LightGBM reaches R2 0.882 (RMSE 0.180), with a positive bias of 0.06 from price drift. A log-linear model on 4 features reaches R2 0.65.
- So the signal is strong and the task is not trivial. The temporal drift makes the split meaningful.
- 21k rows is enough to score reliably.

**What I could not check**
- The true source of the as-of-sale attribute values. Nothing public that I found (Kaggle, OpenML, the KingCountyHouses CRAN package, GeoDa) contains them.
- Whether the changes came from a principled join with assessor history or from a processing error.
- The exact 9 window boundaries, which are not given in the clean room.
- The Kaggle page content: it rendered empty, so I relied on the OpenML copy.

Sources: https://www.openml.org/d/42731 , https://data.openml.org/datasets/0004/42731/dataset_42731.pq , https://cran.r-project.org/web/packages/KingCountyHouses/refman/KingCountyHouses.html , https://www.kaggle.com/datasets/harlfoxem/housesalesprediction

</details>

<details><summary>Precedent check</summary>

Scope: the choices of `dataset.py`, the record's CC line, and issues 1-7 of the earlier REVIEW.md.
Decision register: none of its 4 flags touches house_sales or a house-price dataset; the only house_sales
entry is the LEAK-10 Cases row ("the King County lesson"). No curator decision on house_sales besides the undated CC,
so no drift and no third exception. Measured here on the Kaggle CSV (kept rows, before May 2015): 160 repeated houses,
resale intervals 61-315 days (none within 60); 13 rows with 0 bedrooms, 10 with 0 bathrooms, 7 with both.

Status of the precedents: only CC lines are curator decisions. melbourne_housing_market, perth_house_prices,
house_prices_nominal and zillow_prize are AI drafts with open REVIEW.md issues; two of them cite house_sales as their
own precedent (melbourne issue 5 "like house_sales' 3-week windows"; perth issue 7 "no gap, as house_sales and
house_prices_nominal"; perth issue 8 cites house_sales' May drop). The curator's answer here therefore sets the
house-price family.

**Summary**

| # | Decision | Rule | Result |
|---|---|---|---|
| 1 | Rebuild the features as of the sale (issue 1, option a) | PROV-13, LEAK-10 | consistent |
| 2 | 1,225 sales with county warning 26 kept "as noise" | LEAK-10, LEAK-11 | departs without a reason |
| 3 | `view`/`waterfront` kept for the 154 rows whose attribute changed (issue 4) | LEAK-10 | departs without a reason |
| 4 | No gap despite a measured recording lag | SPLIT-10 | departs without a reason |
| 5 | 9 windows of 3 weeks (issue 2) | SPLIT-12, SPLIT-15 | consistent (family call open) |
| 6 | May 2015 dropped (issue 6) | LEAK-22..26 family, EV-5 | consistent, with a distinguishing fact |
| 7 | Repeated sales kept (issue 7) | LEAK-17, USE-10, SPLIT-13 | consistent; the counter-precedent is the one to reopen |
| 8 | `yr_renovated` = 0 set to missing | CLEAN-10 | departs; the stated reason contradicts the definition |
| 9 | Placeholder living areas 8-200 sq ft kept (issue 5) | CLEAN-10, CLEAN-11 | departs; the stated reason does not set it apart |
| 10 | 0 bedrooms / 0 bathrooms set to missing | CLEAN-10 | consistent in kind, broader than zillow_prize (minor) |
| 11 | Identical-feature parcel pairs and the conflicting duplicate kept | LEAK-16, LEAK-20 | consistent |
| 12 | Temporal only, spatial as a tag (the CC) | SPLIT-3, USE-10 | consistent |
| 13 | `source` GOV Website, `year` 2015 (record 2016) | PROV-8, PROV-9, PROV-11 | consistent; record field stale |
| 14 | `bibtex` = the Kaggle re-upload (2016) | PROV-10 | departs, shared with nyc_taxi_trip_duration |
| 15 | County extracts unpinned (weekly updated) | definitions.md (`download_description`), PROV-9 | departs with an untested reason |
| 16 | `fit = "direct"` with July-2015 remnants | USE-8 | consistent with siblings; family-level tension |

**Per decision**

**1. Rebuild as of the sale (issue 1, option a): consistent**

Follows PROV-13 (Must: repair from the origin before keeping damage) and the remedy ladder (repair > fix > note >
exclude). Precedents: SUPPORT2 (wrong-patient physiology restored from ICPSR), ashrae (readings put in kWh from the
owners' raw files), zillow_prize (each sale takes the property file of its year; AI draft). The LEAK-10 Cases row in
`leak_checks.md` already names house_sales. Repairs that restore true values stayed in the same record (SUPPORT2,
ashrae); only a changed target got a new record (corporate_credit_rating -> corporate_issuer_credit_rating, PROV-11,
Lennart 2026-10-16), so PROV-14 does not apply. Option (c), keeping the file's values with a `Potential leak, kept on
purpose:` bullet, would not be a reasonable exception: that tension row covers weak transductive leaks (LEAK-30,
Lennart 2026-10-19), and this leak is strong and measured (RMSE 0.156 vs 0.208 on the affected rows), so LEAK-10
(Must) holds. Option (b), dropping 1,957 rows, sits lower on the ladder than the repair.

**2. The 1,225 warning-26 sales kept as noise: departs without a reason**

The county flags these sales "IMP. CHARACTERISTICS CHANGED SINCE SALE": the data shows that the record changed after
the outcome. LEAK-10 keeps a looked-up attribute only "unless the data shows they did not change". LEAK-11 keeps a
post-outcome value only when it weakens the signal, but the measured direction for this mechanism in this dataset is
the reverse: post-sale values flatter the model (0.156 vs 0.208). Precedents: california_house_prices_2020, CC
2026-10-14, Lennart: the 2,480 rows whose listing describes another sale were dropped after measuring that they were
5-6% of each window and 50-54% of its squared error. perth_house_prices keeps its stale records as noise, but those are
older than the sale (no leak), the opposite direction. The definition does not say how many of the 1,225 rows the
rebuild already covers (the 2,151 rebuilt rows). The sales extract that would answer this is not in the raw folder.

```text
**Consistency check (AI, 2026-10-20):** your call on house_sales (keep the 1,225 sales the county flags as changed
since the sale, "as noise", under LEAK-10/LEAK-11) differs from california_house_prices_2020 (CC 2026-10-14: rows whose
record describes another state of the house dropped after measuring their error share), and the measured effect of
post-sale values here strengthens the model rather than weakening it. What sets house_sales apart?
(a) nearly all 1,225 rows are among the 2,151 already rebuilt from the change log, so the flag is no longer a leak
(to be measured on the county sales extract), recorded as an exception; (b) treat them like california: measure their
error share and set the changed attributes missing or drop the rows; (c) reopen california to keep its rows as noise;
(d) change LEAK-10/LEAK-11 (an amendment).
```

**3. `view`/`waterfront` kept for the 154 rows that changed after the sale (issue 4): departs without a reason**

The definition explains why these cannot be rebuilt (the 0-4 view index is not a county attribute) but not why the
values known to be post-sale stay. LEAK-10's exception needs data showing no change, and for these 154 rows the data
shows the opposite. Precedent: melbourne_housing_market (AI draft, 2026-10-07, REVIEW issue 3): the six scraped
attributes of 6 sales whose record describes a later building are set to missing, and blanking 495 more mismatched
rows was offered to the curator. Setting `view` and `waterfront` to missing for the 154 rows is the mild fix in that
precedent. `sqft_living15`/`sqft_lot15` (neighbours, July 2015) were not measured. The 5 bathroom rows and the 10
blank old values are small and named, so keeping them with the note is reasonable.

```text
**Consistency check (AI, 2026-10-20):** your call on house_sales (keep view and waterfront for 154 rows where the
county log shows they changed after the sale, LEAK-10) differs from melbourne_housing_market (scraped attributes set
to missing for the sales whose record describes a later building). What sets house_sales apart?
(a) the 154 changes are corrections of an earlier error rather than changes of the house, so the July 2015 value is
also the value at the sale (recorded as an exception, LEAK-10 "did not change"); (b) treat it like melbourne: set
view and waterfront to missing for the 154 rows; (c) reopen melbourne to keep its values; (d) amend LEAK-10.
```

**4. No gap between train and test: departs without a reason**

SPLIT-10 (Should): when a label arrives with a delay, train only on what is known at the window's start, with a gap.
The definition's own decision 3 measures the delay: by the mid-May 2015 extract only 24% of May's sales were in the
county's records, against 80-89% of earlier months. With 3-week windows and no gap, each window trains on the 2-3
weeks just before it, which a refit at the window's start would mostly not have. Precedent: zillow_prize (AI draft,
REVIEW issue 4): a one-month gap, "Zillow receives the sales from the county recorders with a delay". That is the same
mechanism (US county recording). perth_house_prices (no gap) cites house_sales as its precedent, so it does not count
on its own. The REVIEW does not raise the gap as an issue.

```text
**Consistency check (AI, 2026-10-20):** your call on house_sales (9 three-week windows with no gap, a departure from
SPLIT-10) differs from zillow_prize (a one-month gap for the same county-recording delay), while house_sales' own
decision table shows that only 24% of a month's sales are recorded by mid-month. What sets house_sales apart?
(a) the AVM operators of the use case (lenders, property sites) get closed-sale prices from MLS feeds within days,
not from the county record, recorded as an exception with that source; (b) treat it like zillow: add a gap (about 3
weeks, one window) and state it; (c) reopen zillow_prize's gap; (d) amend SPLIT-10 for sale-price tasks.
```

**5. 9 windows of 3 weeks (issue 2): consistent, family call open**

Follows SPLIT-15 (as many windows as an IID task gets folds, 3 x 3), SPLIT-14 (oldest train side 54%) and SPLIT-17
(659-1,565 rows per window). melbourne_housing_market uses the same layout (3 weekly sheets x 9). SPLIT-12 asks for the
horizon from the source (the refit cadence), and none of the house-price siblings cites one: house_sales 3 weeks,
perth 1 month, house_prices_nominal 2 months (size-driven), zillow 1 month + gap (Zillow's monthly ask, the only
source-based one), sberbank 6 months. No curator decision on a house-price window exists yet (the register lists
"Window length" as open for house_prices_nominal and others). It is not a departure, but the answer will be the
precedent for the family; the curator may want to decide melbourne/perth/Ames/house_sales together.

**6. May 2015 dropped (issue 6): consistent, with a distinguishing fact**

Precedents in the same direction: house_prices_nominal drops July 2010 onward (`FIRST_INCOMPLETE_MONTH`), and
zillow_prize drops August-September 2017 (a biased sample). Precedents that kept a short last month:
perth_house_prices December 2020 (0.71 of November, prices in line) and house_prices_nominal June 2010 (82 vs 97-112
sales, cheaper, cause unknown). The fact that sets house_sales apart is stated and measured: the extract date is known
(mid-month), coverage is 24% against 80-89%, and the recorded part is price-selected. The Ames June 2010 case (about 80%
coverage) is milder.

**7. Repeated sales kept (issue 7): consistent; the counter-precedent is the outlier**

LEAK-17 asks for one row per entity only when the use case is that row; USE-10 and SPLIT-13 make a known entity's
history legitimate under a temporal split. Same choice: melbourne_housing_market (resales 63-679 days apart kept,
same-sale re-reports within 60 days merged), zillow_prize (repeat sales kept, those within 31 days dropped per the
competition). house_sales has no resale within 60 days (measured: 61-315), so neither precedent's drop rule bites.
Counter-precedents: california_house_prices_2020 keeps only the newest entry of 63 houses "to avoid group-related
target leakage". This is a legacy step that no CC re-decided, and its reason does not hold under its temporal split. The
other is miami_housing, which removes repeated parcels under an IID split (LEAK-17 applies there). The REVIEW's
alternative ("as in california_house_prices_2020") would copy the outlier. If anything, california is the one to
reopen.

**8. `yr_renovated` = 0 set to missing: departs; the stated reason contradicts the definition**

CLEAN-10 (Should): convert proxy missing values, but "keep a code and say why when it means something ('not
previously contacted')". The definition quotes GeoDa, "'0' if never renovated", and its own `BLANK_IS_ZERO` comment says
a blank YrRenovated "means none". The bullet then calls 0 "unrecorded" and sets 95.7% of the rows to missing.
Precedents: bank_marketing keeps `pdays = -1` (never contacted) as a code; house_prices_nominal keeps the construction
year as "no remodel" ("kept as recorded"). Tree models are indifferent; the meaning in the notes is wrong either way.

```text
**Consistency check (AI, 2026-10-20):** your call on house_sales (yr_renovated = 0, documented as "never renovated",
set to missing, against CLEAN-10) differs from bank_marketing (pdays = -1, "not previously contacted", kept as a code)
and house_prices_nominal (no-remodel coding kept as recorded). What sets house_sales apart?
(a) a 0 in a year column misleads linear models, so missing is the analyst's encoding of "none", recorded as an
exception with the note corrected to say "never renovated" rather than "unrecorded"; (b) treat it like bank_marketing:
keep 0 (or add a renovated flag); (c) reopen the others; (d) amend CLEAN-10.
```

**9. Placeholder living areas of 8-200 sq ft kept (issue 5): departs; the stated reason does not set it apart**

"Kept as the record stood" would also keep the 0 bedrooms and 0 bathrooms that the same definition sets to missing as
"unrecorded values". A living area of 8 sq ft is a placeholder (CLEAN-10) or an impossible value for a house (CLEAN-11:
missing, row stays); cases heart_disease_va_long_beach `chol == 0`, sdss_17 `-9999`. Closest sibling:
sberbank_housing_market_forecasting, CC 2026-10-14, Lennart: sales of flats before completion kept. That decision kept
the rows and a real value (the build year). Keeping the rows here agrees with it, and the values are a separate
question. melbourne_housing_market sets the attributes of a not-yet-built house to missing.

```text
**Consistency check (AI, 2026-10-20):** your call on house_sales (keep the 6 placeholder living areas of 8-200 sq ft,
a departure from CLEAN-10/CLEAN-11) differs from the same definition's 0 bedrooms and 0 bathrooms (set to missing as
unrecorded) and from melbourne_housing_market (attributes of a not-yet-built house set to missing). What sets them
apart?
(a) the placeholder marks "under construction", which tells the model the sale is of an unfinished house (a
real signal, as in sberbank's pre-completion sales), recorded as an exception; (b) set the 6 areas (and the derived
`sqft_above`) to missing, keeping the rows as sberbank did; (c) reopen the 0-bedroom rule to keep zeros as recorded;
(d) amend CLEAN-11.
```

**10. 0 bedrooms / 0 bathrooms set to missing: consistent in kind, minor**

The same mechanism as zillow_prize ("zero means not recorded"). zillow is narrower: `bedroomcnt` = 0 becomes missing
only where the bathrooms are also 0 ("no studios"). house_sales does it for all 13 + 10 rows (7 overlap). This affects
6 bedroom-only rows. It is not worth a prompt, but the zillow condition could be copied.

**11. Identical-feature pairs and the conflicting duplicate kept: consistent**

zillow_prize keeps 7 exact and 39 feature-equal rows ("separate sales of separate parcels, such as units of one
building"). The 9 townhouse pairs are the same case, so LEAK-20's genuine-ambiguity clause applies. Wording point from
the checklist: they share every feature but the date.

**12. CC "Time split required. Also spatial data." (undated): consistent**

The split is temporal, spatial is a `data_tags` entry, and there is no spatial grouping. This follows the tension row
"Temporal against grouped: one regime, the one the use case implies" (Lennart, 2026-10-12): an AVM values houses in
known places.

**13. `source` GOV Website, `year` 2015: consistent; record stale**

The source follows the convention entry in CHANGELOG (Lennart's `source` rule, applied to house_sales with
rain_in_australia and nyc_taxi_trip_duration: "to their government publishers"), and PROV-11 now also applies, since
features come from the county extracts. The year 2015 is the first distribution (Coursera) under PROV-9, as with
airfoil_self_noise, first_principles_tully_fisher and nikuradse (2026-10-20, Lennart: the original's year, not the
re-upload's). The record's `year: '2016'` is the Kaggle copy's year and is the field to align. rain_in_australia took
the year of its pinned live snapshot (2026). That does not transfer: house_sales' rows are the 2015 table, and only 2014-2015
events of the log are read.

**14. `bibtex` = harlfoxem (Kaggle, 2016): departs, shared with nyc_taxi_trip_duration**

PROV-10 (Must) cites the work that published the data, and definitions.md repeats it. The definition's own text says
the table was first published with the UW Coursera course (2015). Its bibtex year (2016) disagrees with `year`
(2015). nyc_taxi_trip_duration uses the same pattern (GOV source, Kaggle bibtex with a note), so this is a family
habit, not a house_sales slip. airfoil_self_noise (2026-10-20, Lennart) cites the original, not the re-upload.

```text
**Consistency check (AI, 2026-10-20):** your call on house_sales (bibtex the Kaggle re-upload of 2016, with year 2015
and source King County) differs from PROV-10 and from airfoil_self_noise (the original publication cited, not the
re-upload). What sets it apart?
(a) the course materials have no citable entry, so the re-upload with a note naming the course is the best available
citation, recorded as an exception (and the same for nyc_taxi_trip_duration); (b) cite the UW course
(learnml/machine-learning-specialization, 2015) or King County; (c) reopen airfoil to cite UCI; (d) amend PROV-10 for
uncitable first publications.
```

**15. County extracts unpinned: departs with an untested reason**

definitions.md, `download_description`: "Pin a DOI or an archived release where one exists". Precedent:
rain_in_australia pins an Internet Archive capture of its live file (2026-10-05, byte-identical, with sha256).
sf_permit_time states the snapshot it pins. house_sales downloads two weekly-updated county zips with no checksum or
archived copy, and also reads today's bathroom counts. Its reason, "the 2014-2015 events it reads do not change", is
asserted, not tested (checklist, reproducibility row). Whether an archive of a 1.8 GB zip exists is unknown, so this is
a question rather than a prompt. A cheap pin is the md5 of the two prepared CSVs (`house_sales_changes.csv`,
`house_sales_bath_counts.csv`), so that a rebuild can show its inputs are unchanged.

**16. `fit = "direct"` with July-2015 remnants: consistent with siblings, family-level tension**

melbourne_housing_market (scraped attributes looked up after the sale) and zillow_prize (tax-delinquency snapshot
after some sales) both say `direct` with post-outcome remnants named in `fit_reason`. USE-8 lists "a potential leak
kept on purpose" under Approximate. If decisions 2 and 3 end with the remnants kept, all three datasets face the same
question. This is not a house_sales departure.

**Side findings on siblings (not house_sales decisions)**

* california_house_prices_2020: `min_train_fraction=0.25`, so the oldest of its 3 windows trains on 25% of the rows.
  This contradicts SPLIT-14 (Must: no window's train side below 50%). It is a precedent that contradicts a rule, so
  flag it and do not follow it.
* california_house_prices_2020: the newest-only deduplication (decision 7) is the outlier among the temporal
  house-price tasks.
* perth_house_prices (issues 7, 8) and melbourne_housing_market (issue 5) take house_sales as their precedent for
  the gap, the short last month and the window length, so a change here should be carried to them.

</details>

<details><summary>Advocate</summary>

Position: ship after changes. Every real problem the evidence agents found sits on the "fix the definition" or
"keep with a note" rung of the remedy ladder; none needs exclusion.

**1. The dataset's one strong leak is already repaired from the origin (P5 PROV-13 Must; P4 LEAK-10 Must)**

- Claim: the famous flaw of `kc_house_data` (the assessor's record of July 2015 attached to sales of 2014-15) is
  fixed by rebuilding each house as of its sale day from the county's own change log.
- Evidence: snapshot dating holds per day (17 July 0/29 old == file, 20 July 55/55; claim audit). The leak is real and
  strong: LightGBM on the changed rows 0.156 vs 0.208 (definition), reproduced as 0.148 vs 0.194 (claim audit) and,
  independently and blind, 0.156 vs 0.193 (clean room, which called the rebuild "plausibly an improvement in honesty").
  21,386 of 21,613 rows match a recorded county sale; the change log's `AttributeValue` is confirmed as the old value.
- Rule: PROV-13 (Must) repair before keeping damage; the remedy ladder puts repair first. Precedents SUPPORT2, ashrae;
  the LEAK-10 Cases row already names house_sales. Option (c) (keep with a note) is no reasonable exception: the
  LEAK-30 tension row covers weak transductive leaks only (precedents, decision 1).
- Against the clean room's "undocumented source" concern: the clean room saw only the data. `download_description`,
  `curation_comments` and Decision 1 name the extracts, the URLs and the procedure. That concern is met.

**2. A real task, a direct fit, an honest split and real signal (P3 USE-1/USE-8 Must; P4 SPLIT-6; P6)**

- Practitioner: "Direct; the stated fit holds", "As a benchmark of hedonic valuation, yes". Clean room: "a real use".
- Split audit: regime right (SPLIT-6 names a sale price as a temporal task); SPLIT-11/14/15/17 hold; `date` is the deed
  date (= county `DocumentDate`), the right prediction moment; grouping by parcel changes nothing (0.1619 vs 0.1632).
- Probes: LightGBM skill +0.884, linear +0.852 (paired spread +0.032, SE 0.001), drift baseline +0.002, single
  feature +0.463; no leak, task, hidden-group or generated flag. Not trivial, not solved, every fold scorable.
- Familiarity (clean room concern 5) is no rule; and 10% of rows now differ from the public copy, which weakens
  memorisation.
- Fix (wording only, USE-1): the practitioner's rewording of `use_case` (the assessor's mass appraisal or an estimate
  from the public record before the sale is recorded) and "without the assessor's value or the previous sale price"
  in `known`. The task stays.

**3. Concede: `sqft_lot` is not rebuilt (P4 LEAK-10 Must). Fix the definition**

- Evidence: lot changes live under record `LandFootage` (snapshot test 0/139 before, 127/130 after); 81 kept rows
  (35 test) keep a post-sale lot. Effect nil (those test rows 0.322 vs 0.326).
- Remedy: add `("LandFootage", "SqFtLot"): "sqft_lot"` to `CHANGED_COLUMNS`, re-run `_prepare_raw_files`, update the
  2,151 count and Decision 1. A correctness bug with a one-line fix, not a reason to stop.

**4. Concede in part: non-market sales in the target (P3 USE-5 Must). Fix by filtering, the curator's call**

- Evidence: 1,420 rows (6.8%) carry county warnings for non-market sales (no market exposure 654, non-representative
  357, teardown 322, short sale 199, ...); test RMSE 0.25-0.31 vs 0.151, sold below the model (claim audit).
- Why it does not exclude: the label is the recorded sale price for every row, which is what both named actors act
  on; for 93% it is an arm's-length price, and the county flags the rest, so the defect is fixable from the origin.
- Mildest remedy that resolves it: drop the rows with the non-market warnings (15, 46, 60, 51, 12, 10, ...) from the
  county sales extract, as an assessor's sales validation does (practitioner gap 4). That adds a third county
  extract to a definition that already reads two. Keeping them with a note is the fallback, a weighing call.
- Warning 26 is a different case and stays: 1,096 of the 1,225 are not rebuilt because their tracked changes come
  mostly in 2015-2017, after the snapshot, so the file holds the at-sale record; residual -0.124 (fixers improved
  later). That is noise, not a leak (LEAK-11, claim audit). This answers the precedents' consistency check on
  decision 2 with option (a)'s fact.

**5. The recording delay is small; a one-week gap fixes it (P4 SPLIT-10 Should, applies SPLIT-9)**

- Evidence: deed-to-recording delay median 6 days, 91% within 14; effect 0.1729 -> 0.1740 (recorded-before filter),
  0.6% RMSE (split audit); claim audit 0.1717 -> 0.1733.
- Remedy: `gap=1` (precedents aeolus_1m, bias_correction; zillow_prize has a gap for the same county mechanism), one
  sentence in `splits_comment`. The alternative, gap 0 as an exception, needs the MLS fact; I would not argue for it.
  Either way the split audit's verdict is "right with notes", with no Must open once the gap is in.

**6. The July-2015 remnants are measured weak: keep with a note (P4 LEAK-11 Should, narrows LEAK-10)**

- Evidence: masking `view` for the 143 changed rows: 0.2147 vs 0.2132 kept, no post-sale signal (claim audit).
  Ablation: dropping view/waterfront hurts the unchanged rows more (+0.0115) than the changed (+0.0046); the
  neighbours' areas move the changed rows by 0.004 and do not track the house's own change (column audit).
- Rule: LEAK-11 narrows LEAK-10 within its scope; blanking the 145 values would make missingness itself mark "changed
  after the sale" (column audit), so the melbourne precedent's blanking would add a leak here, which sets it apart.
- Remedy: turn the "We leave ..." bullet into a `Potential leak, kept on purpose:` bullet with these numbers. On fit,
  USE-8 lists this under Approximate; I concede the label should follow the rule unless the curator accepts "measured
  as weak" as the reason for direct.

**7. The quality and record points are cheap fixes (P5 PROV-10 Must; P7 CLEAN-10/11 Should; writing)**

- Placeholder areas 8-200 sq ft (6 rows): set `sqft_living`/`sqft_above` to missing, rows stay (CLEAN-11; cases
  heart_disease_va_long_beach, sdss_17).
- `yr_renovated` 0: the NaN stays, the note says "never renovated", not "unrecorded" (CLEAN-10).
- Citation: cite the first publication (the UW course, 2015) or King County, not the 2016 re-upload (PROV-10 Must,
  airfoil_self_noise); record `year` 2016 -> 2015.
- Reproducibility: pin md5s of the two prepared CSVs so a rebuild shows unchanged inputs.
- Numbers: resales 0.36 -> 0.27 vs 0.17 (EV-8); "share every feature but the date"; bathrooms 913 rebuilt / 869 changed.

**Judgment record**

```text
Verdict: ship after changes.
Validity: SEL holds; USE-1 holds (reword actor); USE-5 triggered, fix by dropping county-flagged non-market sales
(or note: curator); USE-8 approximate unless the curator accepts measured-weak remnants; LEAK-10 triggered, fixed
(rebuild) plus the LandFootage fix; LEAK-11 remnants kept with a note; SPLIT-10 triggered, fix gap=1; PROV-13 holds
(repaired); PROV-10 fix citation.
Value: TP holds (skill +0.884, linear +0.852, drift +0.002; no flags).
Quality: CLEAN-11 placeholders to missing; CLEAN-10 wording.
Weighed: source +, repair +, size +, familiarity -, one year of data -.
For the curator: non-market filter vs note; direct vs approximate.
```

**Rebuttal**

The critic and I agree on the verdict (ship after changes; no exclusion) and on every remedy rung. One point remains
open: the exact warning list in point 1. Nothing new is added.

1. **Non-market sales (USE-5 Must): concede.** What follows: a Must is triggered, so the mildest remedy that resolves
   it is to fix the definition (read Real Property Sales, drop the flagged sales). A note alone does not resolve a
   Must, so I withdraw "note as fallback" as an equal option. It stays only if the curator rules the flagged sales
   are within what the actor acts on. Open on scope: the list should be checked code by code. Teardown (10, 322
   rows) and segregation (29, 104) are arm's-length sales whose price reflects the land or a changed lot; they are
   not non-market in the sense of 15/51/60. The audit gives one pooled RMSE (0.25-0.31) and no per-code residuals,
   so I cannot show that they behave differently. I ask that the filter be decided per code with per-code residuals,
   not that it be dropped.
2. **sqft_lot (LEAK-10 Must): concede.** Fix: the `LandFootage` mapping; the counts regenerate. No dispute.
3. **Recording gap (SPLIT-10 Should): concede.** `gap=1` with a sentence in `splits_comment`. Since perth and melbourne
   cite house_sales, the change carries to them (precedents.md).
4. **Fit and remnants (USE-8 Must; LEAK-11): concede.** What follows: a `Potential leak, kept on purpose:` bullet with
   the counts and the ablation, the 24 full-record events and the warning-26 explanation. The fit becomes
   `approximate` unless the curator records "measured weak" as the reason for direct. USE-8's list puts this case
   under approximate, so the default is approximate.
5. **Wording of the use case (USE-3/USE-1): concede.** Use "the assessor's record on the sale day", the
   mass-appraisal or public-record AVM actor, and "without the assessed value or previous sale price". The residual
   +0.079 says the record lagged the house, which is what an assessor-record AVM faces. That supports the reworded
   task; it does not weaken it.
6. **Citation and pinning (PROV-10 Must): concede.** Cite the UW course release (or record an exception if it cannot
   be cited), pin md5s of the two prepared CSVs, and set the record `year` to 2015.
7. **Quality (CLEAN-10/11 Should; EV-8): concede.** All are cheap and safe fixes.

Joint judgment: ship after changes. These are definition fixes under P3-P5 with no exclusion rung reached. Two calls
go to the curator: the per-code scope of the non-market filter, and direct against approximate.

</details>

<details><summary>Critic</summary>

Position: **ship only after changes.** The task is real and the as-of-sale rebuild is the right repair (PROV-13,
LEAK-10). I do not argue for exclusion. Six changes, one quality batch. Validity first, Must first.

**1. The target includes non-market sales (P3, USE-5 Must)**

- Problem: 1,420 kept rows (6.8%) carry county sale warnings for non-market or non-representative sales: no market
  exposure 654, non-representative 357, teardown 322, short sale 199, segregation 104, related party 90, estate 42.
- Effect: the AVM and the assessor value against market sales; the county itself flags these. They are the
  worst-predicted rows (test RMSE 0.25-0.31 against 0.151 unflagged) and sit 0.14-0.23 below the model. The label
  means something else for 1 row in 15, and nothing in the definition says so.
- Evidence: claim_audit.md, implied claim "the target is the market price" (EXTR_RPSale matched on parcel, date,
  price); practitioner.md gap 4 (valuers use validated market sales only).
- Remedy: add the county sales extract (Real Property Sales, ~150 MB) as a raw input and drop sales with the
  non-market warnings (15, 46, 60, 51, 12, 13, 23, 10), as the assessor's sales validation does. If the curator judges
  this a weighing call, the minimum is a note stating the share and the effect.

**2. sqft_lot is listed as rebuilt but is not (P4, LEAK-10 Must)**

- Problem: `CHANGED_COLUMNS` maps `("Land", "SqFtLot")`, but the file's lot size follows the `LandFootage` record
  (snapshot test: 0/139 before 18 July, 127/130 after). 81 kept rows (35 in test) keep a post-sale lot size, 55 of
  them smaller (segregations). Decision 1 reports 0 rows rebuilt.
- Effect: score effect nil (0.322 against 0.326 on those rows), but the rows hold a value recorded after the sale, and
  the "2,151 rows" count and Decision 1 are wrong.
- Evidence: claim_audit.md claim 28.
- Remedy (repair): add `("LandFootage", "SqFtLot"): "sqft_lot"` (keep `Land`), re-run `_prepare_raw_files`, let the
  counts regenerate.

**3. No gap for the recording delay (P4, SPLIT-10 Should, applying SPLIT-9 Must)**

- Problem: a refit at a window's start knows only recorded sales. Deed-to-recording delay: median 6 days, 91% within
  14. Each window trains on 223-503 sales not yet recorded.
- Effect: small but consistent shortcut: RMSE 0.1729 shipped against 0.1740 (as-of-recording filter) and 0.1748
  (14-day gap); shipped is best in 6-7 of 9 windows.
- Evidence: split_audit.md problem 1; claim_audit.md implied claim (0.1717 -> 0.1733, 7/9). Precedent: zillow_prize
  uses a gap for the same county-recording delay (precedents.md 4); perth and melbourne cite house_sales for "no gap",
  so this choice sets the family.
- Remedy: `gap=1` (or 2) in `TemporalSplits` and a sentence in `splits_comment`. The alternative, gap 0, needs a
  recorded exception naming the fact (an AVM sees MLS closings before recording).

**4. Fit "direct" with known post-sale values kept and not labelled as such (P3, USE-8 Must; LEAK-10/LEAK-11)**

- Problem: `view`/`waterfront` changed after the sale for 143-145 rows (39 gained a view rating from blank),
  `sqft_living15`/`sqft_lot15` are July 2015, 24 rows have a full-record Bldg 1 event after the sale that the rebuild
  leaves. USE-8 lists "a potential leak kept on purpose" under approximate; LEAK-10 keeps a looked-up attribute only
  where the data shows it did not change.
- Effect: measured weak: masking view on those rows 0.2147 against 0.2132; dropping the neighbours' areas +0.004 on
  changed rows. So keeping is defensible, but only as a stated, measured exception.
- Evidence: column_audit.md problem 1 and measurements; claim_audit.md claims 32, 64; precedents.md 3 and 16
  (melbourne blanked its post-sale attributes).
- Remedy: turn the "We leave ..." bullet into a `Potential leak, kept on purpose:` bullet with these counts and the
  ablation, and either set `fit = "approximate"` or state why direct holds (measured weak). Do not blank the 145 view
  values (the missingness would mark "changed after sale"). Warning 26 is settled: 1,096 of 1,225 are not rebuilt
  because their changes come after the snapshot (claim_audit claim 35); say that in the note.

**5. The use case and fit text overclaim (P3, USE-3 Must / USE-1; writing)**

- Problem: "the features describe the house as it was sold" is refuted: on rebuilt rows the record at the sale
  understated the house (residual +0.079; post-sale shift correlates 0.59 with the residual). "Lenders or property
  sites ... on the day it sells" names actors who do not hold this moment (a lender knows the contract price). The
  task also lacks the assessed value and previous sale a valuer always has (USE-6), which is fine but unstated.
- Evidence: claim_audit.md claim 11; practitioner.md gaps 1-2.
- Remedy: reword to "the assessor's record on the sale day"; the actor to the assessor's mass appraisal or a
  public-record AVM before the sale is recorded; add "without the assessed value or previous sale price".

**6. Provenance: citation and reproducibility (P5, PROV-10 Must; definitions.md pinning)**

- Problem: `bibtex` cites the 2016 Kaggle re-upload while the definition itself says the table was first published
  with the UW Coursera course in 2015 (and `year = 2015`). The two county extracts are weekly-updated and unpinned;
  "the 2014-2015 events do not change" is untested.
- Evidence: precedents.md 14, 15 (airfoil_self_noise cites the original); claim_audit.md claims 16, 65.
- Remedy: cite the UW course release (or record an exception if it is not citable, as for nyc_taxi_trip_duration);
  record md5s of the two prepared CSVs in `download_description`. Align the record's `year` to 2015.

**7. Quality (P7; not a reason to hold the task)**

- 6 placeholder living areas of 8-200 sq ft (CLEAN-11 Should): set `sqft_living`/`sqft_above` to missing; the same
  definition already does this for 0 bedrooms.
- `yr_renovated` 0 means "never renovated" (GeoDa, `BLANK_IS_ZERO`), not "unrecorded" (CLEAN-10): fix the note.
- Resale RMSE "0.36 against 0.17" reproduces as 0.27 against 0.17 (EV-8); "9 pairs share every feature" is "every
  feature but the date".
- Evidence: column_audit.md 4-5, precedents.md 8-9, claim_audit.md 38, 43.

**Rebuttal**

The two briefs agree on the verdict (ship after changes) and on almost every remedy. One dispute remains, on
point 4.

1. **Rebuild repaired from the origin (PROV-13, LEAK-10).** Concede. The clean room's "undocumented source" concern
   is met by `download_description`, the notes and Decision 1. The rebuild is what I argued for too.
2. **Real task, direct fit, honest split, real signal.** Concede the task, the regime and the value (probes, split
   audit). The fit label is settled under 6 below. The wording fix matches my point 5.
3. **sqft_lot (LEAK-10 Must).** Agreed: the LandFootage mapping, then regenerate the counts.
4. **Non-market sales (USE-5 Must).** Concede the filter remedy. I dispute the fallback. The advocate files "keep with
   a note" as a weighing call, but USE-5 is a Must, and under "Strengths" in principles.md a Must violation "is fixed
   in the definition when it can be". It can be: the county sales extract is public, it was already downloaded and
   matched for this audit (21,386 rows on parcel, date and price), and the warning codes are in the Lookup extract.
   The advocate argues that the label is the recorded price that both named actors act on. That does not hold for
   the actors the advocate itself proposes in point 2. The assessor's mass appraisal values against validated market
   sales (practitioner gap 4), and a pre-recording AVM estimates market value. A short sale or a related-party
   transfer is not what either acts on. Rule that wins: USE-5 (P3, Must) over the convenience of not adding a raw
   input (no rule). A note is right only if the curator finds that the extract cannot be pinned or read. Then it is
   kept as a documented limit, not as a choice. The open curator question is which warning codes count as
   non-market, not whether to filter.
5. **Recording gap (SPLIT-10).** Concede `gap=1`. It covers the median delay of 6 days, which is "about the label's
   delay", and has precedents (aeolus_1m, bias_correction). State the 91%-within-14-days figure in `splits_comment`.
6. **July-2015 remnants (LEAK-11).** Concede: keep them with a `Potential leak, kept on purpose:` note and do not
   blank them. That blanking would add a missingness leak is the right fact to set this case apart from melbourne. On
   fit, the advocate concedes that USE-8 (Must) puts a kept potential leak under approximate. A Must has no
   exceptions, so "measured as weak" cannot keep `direct` unless the curator amends USE-8. Set
   `fit = "approximate"`.
7. **Quality, citation, pinning, numbers.** Agreed point by point (CLEAN-11, CLEAN-10 wording, PROV-10, md5 pins,
   EV-8 restatements).

No new facts, so no new points.

</details>
