# melbourne_housing_market

**Outcome:** added. A regression of the log sale price of Melbourne properties that sell, predicted before the
auction (Melbourne_housing_FULL.csv of the Kaggle upload, 21,266 sales from January 2016 to March 2018), tested on 9
temporal windows of three weekly result sheets. The review panel (all roles, 2026-10-20) recommends shipping after
changes; the changes that need no decision are in the definition. Settled 2026-10-21 (the curator, cross-dataset
items): the attributes of the April 2017 batch lookup are blanked and the fit is `direct`; the newest sheets were
measured for a recording shortfall and need no gap. One question remains: the year (issue 9).

```text
Verdict: ship after changes.
Validity: SEL holds; USE-1/USE-5 hold (sale price; passed-in and vendor-bid prices are bids, -4.1% and -6.5% against
  a sale model, sales +0.3%); USE-3 triggered, fixed (prediction point "before the auction, for a property that
  sells"); LEAK-22 holds (sold cohort, as every house-price sibling); LEAK-10 triggered, fixed
  (the six attributes of the 7,578 sales looked up in the batch of April 2017 blanked, LEAK-7; 2026-10-21); USE-8
  direct (2026-10-21); SPLIT-1/9/11/14/17 hold;
  SPLIT-10 measured, no gap (every sheet of the full file holds as many sales as in the companion file read up to
  October 2018; newest window's mean residual +0.009, inside the other windows' range); SPLIT-12 horizon stated as three sheets, up
  to 7 calendar weeks; PROV-4/6/13 hold; PROV-9 year (issue 9).
Value: TP holds (LightGBM skill 0.834 over the dummy, 0.840 after the changes; beats it on 5 of 5 probed splits; best
  single feature 0.426).
Quality: CLEAN-11 fixed (86 impossible BuildingArea values set missing); CLEAN-21 fixed (one Distance per suburb);
  CLEAN-1 non-Saturday sheet dates noted; two suburb lookups filled.
Weighed: source +, size +, real actor +; post-sale scrape -, high missingness of the scraped block -.
For the curator: issue 9 (2018 or 2017).
```

**Main points:** Keep the year 2018 under PROV-9's clause for a growing source (issue 9)?

**Record judgment:** valid with concerns. A scrape of Domain.com.au's weekly auction-result sheets, first published
on Kaggle, whose established use is sale-price regression. The concern was the lookup on realestate.com.au made after
the sale (six attributes and the coordinates); the attributes of the sales looked up months later are blanked.

**Issues for Lennart:**

9. **Year: 2018 or 2017?** The upload grew over 27 Kaggle versions: public by 27 March 2017 (thread 30748, the first
   forum post), the September 2017 snapshot, the full file to March 2018 and the companion file to October 2018 in
   version 27 (2018-10-14), the current version, whose files the download's md5s identify.
   - Effect: metadata only.
   - Implemented: `year = "2018"` (code comment: the snapshot we pin; the source grew from 2017 to 2018), under
     PROV-9's clause "A source that grows over time (a
     public register, a scraped site, a monthly archive) takes the year of the snapshot we pin".
   - Alternative: 2017, the year of first distribution. house_sales uses that convention, but it is a fixed file, so
     it does not apply here.
   - Rule: PROV-9 (Must); precedents for the growing-source clause sf_permit_time, consumer_complaints_1m and
     kickstarter.
   - Recommendation: 2018 (the mediator and every role agree).
   - Decision: confirm 2018, or 2017.

**Review panel:** ship after changes (mediator). All roles, 2026-10-20; the mediator's issues 1 and 2 are issues 3 and 9
here. Claim audit: 51 claims, most hold; refuted: the 3-week horizon, the signed +0.0004 and -0.0004 effects, the
record's "no known risk" (all fixed). Column audit: no column to drop; the coordinates belong to the post-sale scrape;
impossible BuildingArea values, Distance on two scales, two missing lookups (fixed). Split audit: right with notes.
Domain practitioner: fit direct. Blind review: include with changes. Debate: agreed on the sold-only rows, the split and
the repairs; disputed: whether LEAK-10's exception is shown, which sets the fit (issue 3).

<details><summary>Claim audit</summary>

**Claim audit: melbourne_housing_market (2026-10-20, re-check, full tier)**

Data: the definition's frame rebuilt via `dataset_io.load(..., built=False)` (21,266 rows, 9 temporal splits); raw files
md5 match; the dansbecker snapshot downloaded for the comparison.
Model: LightGBM (600 trees, lr 0.03, 63 leaves, bagging 0.8, colsample 0.8), mean of the 9 window RMSEs, 3 seeds.

| # | Claim (short) | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 1-2 | question / use case: sale price at listing, refit on earlier sales | D task_summary | read features against the listing moment; check train = all earlier rows | holds | every split's train set equals all rows dated before the window's first date | USE-1, USE-3 |
| 3 | 21,266 sales, Jan 2016 - Mar 2018 | D | count | holds | 21,266 rows; 2016-01-28 to 2018-03-17 | EV-1 |
| 4 | target = ln(AUD price) | D | code + values | holds | `np.log(Price)` | USE-5 |
| 5 | known features (incl. six scraped) | D | columns; LEAK-10 tests below | holds (with limits, see 10/46) | 18 features + Address | LEAK-10 |
| 6, 36 | 9 windows of 3 consecutive sheets, 3-17 Mar 2018 back to 12-26 Aug 2017, horizon 3 weeks | D | list test dates per window | dates hold; "horizon 3 weeks" partly refuted | window 2 trains to 16 Dec 2017 and tests 20 Jan - 3 Feb 2018 (5-7 weeks ahead); window 3 tests 25 Nov, 9 Dec, 16 Dec (no 2 Dec sheet: 4 calendar weeks); window 7 holds 3 Sep 2017, a Sunday | SPLIT-10, SPLIT-17 |
| 7 | PI/VB and Method dropped; test on later sheets | D | code, counts | holds | 5,939 PI/VB rows with a price dropped; no Method column | LEAK-10, USE-5 |
| 8-9 | fit direct | D | USE-8 against LEAK-10's exception | untested (weighing) | direct is defensible only through LEAK-10's "data shows they did not change"; that evidence is Bedroom2 only (10/46) plus the snapshot for 2,728 of 9,513 test rows; kick's precedent for a kept potential leak is `approximate` | USE-8, LEAK-10 |
| 10, 24 | blanking the scraped block of 495 mismatched 2016 sales changes RMSE by +0.0004 | D fit_reason, CC | rerun, 3 seeds | count holds (495); the figure is refuted as a signed effect, the conclusion (negligible) holds | delta -0.0005, +0.0003, -0.0004 by seed; seed spread of the baseline 0.0007 | EV-1, EV-6 |
| 11 | year 2018, domain, licence, tag Spatial | D | Kaggle API metadata | year: untested as a convention (first public 2017 per REVIEW_before issue 9); Spatial holds (coordinates); licence not evidence | lastUpdated 2018-10-14 | PROV-9 |
| 12 | last updated 2018-10-14 | D | Kaggle API `datasets/view` | holds | 2018-10-14T23:33:37Z | EV-2 |
| 13-14 | FULL 34,857 x 21, md5 06cc...; LESS 63,023 x 13, md5 cc46... | D | md5sum, shape | holds | exact | PROV-4 |
| 15 | bibtex: Jan 2016 - Oct 2018 | D | LESS date range | holds | LESS to 2018-10-13 | |
| 16 | FULL = results of properties scheduled for auction | D | none feasible offline | untested | data card: "S - property sold" does not say auction; whether the sheets' S rows include private-treaty sales was not checked | USE-1 |
| 17 | prediction point at listing | D | feature timing | holds | Rooms, Type, Agent, Date, location all on the listing | LEAK-1 |
| 18, 45 | RMSE 0.183 with scraped, 0.211 LESS columns | D, R | rerun | holds (direction and size) | 0.182 (3 seeds 0.1816-0.1823); without scraped 0.200; LESS columns 0.206; worse in 9 of 9 windows | TP-6 |
| 19 | before 27 May 2017 inner suburbs only; training from 27 May raises 0.183 -> 0.188 | D | coverage table; rerun | holds | share of LESS results in FULL before/after: 0-5 km 1.00/1.00, 5-10 0.997/1.0, 10-15 0.658/1.0, 15-20 0.019/1.0, >20 0/1.0; RMSE 0.182 -> 0.185 | SPLIT-20 |
| 20, 31, 41, 47 | PI/VB prices are bids, median 4.3%/6.6% below a sale model, sales 0.1% above | D, R | per-window LightGBM on sales, PI/VB rows of the test dates cleaned by `_clean` | holds | PI -4.1% (1,418), VB -6.5% (1,345), sales +0.3% (9,513) | USE-5 |
| 21, 32 | 787 rows dated 6 Jan 2018 = sheet of 16 Dec 2017; LESS holds the same 787 on 16, 23, 30 Dec, 6, 8 Jan | D | key match | holds | LESS 787 of 787 on each date; FULL 786 of 787 match on the 7-column key (one address spelt differently) | PROV-13 |
| 22, 33 | repeats <60 d: same price keep first, two prices drop both; resales 63-679 d kept | D | recompute gaps | holds | 36 same-price repeats 0-35 d; 3 conflicting pairs (4, 14, 35 d); no gap 36-62 d; 45 resales 63-679 d. 9 resales are 63-126 d apart, 8 within 11% of the first price (possible re-reports; 30 resales have the later sale in a test window) | SPLIT-24 |
| 23 | six 2016 sales with YearBuilt 2017/2018, scraped block blanked | D | raw count | holds | 6 rows, all sold 2016 | LEAK-10 |
| 25 | YearBuilt < 1835 and zeros to missing; Landsize 0 kept, mostly units | D | counts | holds | 2 / BA 49 / Bath 26 / Bed 14 zeros; Landsize 0: 1,420 rows, 1,179 units, 127 houses (2 houses in test) | CLEAN-11 |
| 26 | 92 BuildingArea 1-29 m2 | D | count | holds | 92 | CLEAN-11 |
| 27 | Distance switches on 27 May 2017 for 140 of 142 suburbs; harmonising -0.0004 | D | per-suburb values; rerun 3 seeds | holds (count, date); figure within noise | 140/142; one value per suburb in each period; old values last 20 May, new from 27 May; delta -0.0008, 0.0000, -0.0004 | EV-6 |
| 28 | spelling variants mapped to the most frequent spelling | D | raw counts; residual variants after case/punct normalisation | holds | every mapping goes to the more frequent form; no variants remain | CLEAN-8 |
| 29 | renames, Type words, dtypes | D | schema | holds | Postcode category, Address string, Date datetime | |
| 30, 48 | snapshot is a Sept 2017 subset | D, R | merge on 8 key columns | holds | 13,580 of 13,580 rows in FULL, scraped values identical (100%), newest sale 23 Sep 2017 | PROV-6 |
| 34 | scraped from realestate.com.au after the sale (thread 53664) | D | data card; resale pairs | holds in part, forum text untested | data card: "Bedroom2: Scraped # of Bedrooms (from different source)"; 22 of 32 resale pairs with values on both sides differ: lookups were per sale, not one current record per address | LEAK-10 |
| 35 | from 27 May 2017 FULL holds every result | D | coverage | holds | 99.99%, min per sheet 0.999 | |
| 37 | train on all earlier sales (55-95%), no gap | D | splits | holds | 0.553-0.947 | SPLIT-9 |
| 38 | IID of this size gets 3 x 3 | D | `recommended_dimensions` | holds | 14,177 train rows -> 3 repeats | |
| 39-40 | no sheet 16 Dec - 20 Jan; 18 Jan sales; month 18, 4 weeks 9; window of 93; others 868-1,550 | D | layouts rerun | holds | exact | SPLIT-17 |
| 42 | 4 sheets: 2 of 9 windows train below half | D | layout rerun | holds | train shares 0.405, 0.484 | |
| 43 | early comments (no task, unclear version) | R | none | untested (opinions, superseded by the definition) | | |
| 44, 46 | valid; Bedroom2 matches Rooms 98.9-100% per test window vs 85.2% Apr-Sep 2016 | R | recompute | holds; "looked up in April 2017" untested | per window 0.989-1.000; Apr-Sep 2016 0.852 (3,107); by quarter 2016Q4 0.981, 2017-18 0.993-0.998; snapshot (Sept 2017) fixes the values of the 2,728 test rows up to 23 Sep 2017 | LEAK-10 |
| 49, 51 | Airbnb not a source; front matter | R | read | holds | | PROV-12 |
| 50 | priority 3, "no known risk" | R | compare with the definition | refuted (wording) | the definition itself keeps a documented post-sale lookup (LEAK-10 risk, measured small) | LEAK-10, writing |

**Implied claims**

* Every feature known at the prediction point: holds for the sheet columns; the scraped block rests on LEAK-10's
  exception, shown for bedrooms only (Bathroom, Car, Landsize, BuildingArea, YearBuilt have no pre-sale reference
  after Sept 2017).
* The split is the one the use case needs: holds (expanding window, train = all earlier sales).
* The target is the real-world target: holds (sale price; PI/VB are bids, measured).
* No row is a copy across the split: exact copies including Address and Date 0%; 8 short-gap resales with near
  prices may be re-reports of one sale (8 of 9,513 test rows at most; no effect).

**Refuted, ranked**

1. (P4, Should, small) Claim 36 "horizon 3 weeks": window 2 predicts 5-7 weeks ahead, window 3 spans 4 calendar weeks.
   Remedy: say in `splits_comment` that the horizon is three sheets, up to 7 weeks across the January lull.
2. (EV-6, wording) Claims 10/24 (+0.0004) and 27 (-0.0004): single-seed effects inside the seed noise (spread
   0.0007; signs flip). Remedy: write "within run-to-run noise (|delta| <= 0.0008 over 3 seeds)".
3. (writing) Claim 50 "no known risk": change to "known risk: post-sale lookup of six attributes, measured small".

**Untested**

* Claim 16: whether S rows include private-treaty sales (not "scheduled for auction").
* Claim 34 / 46: the forum's step 4 and "looked up in April 2017" (forum text not read).
* Claim 9: `direct` vs `approximate` is a weighing call under USE-8 / LEAK-10 (kick precedent).
* Claim 11: year 2018 vs first distribution 2017 (convention, curator's call); licence not evidence.

</details>

<details><summary>Column audit</summary>

**Column audit: melbourne_housing_market (re-check, full tier, 2026-10-20)**

Frame: the definition's cleaned frame (`dataset_io.load(..., built=True)` fell back to `rebuilt`: 21,266 rows, 20
columns). Prediction point (first `curation_comments` bullet): a property is listed for auction; a model refit on all
earlier sales predicts its sale price from the listing and the auction date. Codebook: the Kaggle data card
("Some Key Details")
and the uploader's pipeline (forum thread 53664: 1) Domain PDF sheet, 3) parsed to CSV, 4) "extra data from
realestate.com", 5) "another excel file with melbourne postcodes/distances and other extras, vlookup").

**Column table**

| Column | Meaning (codebook) | Known at prediction? | Dtype and cleaning | Verdict | Rule |
|---|---|---|---|---|---|
| log_price | target: ln of "Price in Australian dollars", sale results S/SP/SA only | target | float64, 11.63-15.85, no NaN | fine (selection on a sale: see problem 2) | CLEAN-15, CLEAN-16 |
| Suburb | suburb (sheet) | yes | category, 340; spelling variants merged | fine | CLEAN-14 |
| Address | street address (sheet) | yes | string, 21,089 unique; carries street and unit marker ("1/10 ..."); resales are history | fine | CLEAN-3, CLEAN-14, LEAK-34 |
| Rooms | "Number of rooms" (sheet; bedrooms on Domain's sheet) | yes | int64, 1-16 | fine | |
| Type | h/u/t codes -> house/unit/townhouse | yes | category, 3 | fine | CLEAN-12 |
| Agent (SellerG) | "Real Estate Agent" (agency) | yes | category, 302; spelling merged; business names, not personal | fine | CLEAN-4 not triggered |
| Date | "Date sold": the weekly sheet date | yes (auction date known at listing) | datetime; holiday copy re-dated; 11 sheets (2,034 rows) are dated 1-3 days after their Saturday (download day: e.g. 2017-09-03 Sun, 2016-07-26 Tue), same in LESS | fine, minor note (problem 5) | CLEAN-1 |
| Distance | "Distance from CBD in Kilometres" (uploader's lookup, step 5) | yes (static) | float64; 0 km = 39 rows of suburb Melbourne (plausible); 1 NaN (Fawkner Lot row); two tables, switch on 27 May 2017 (140/142 suburbs) | cleaning problem, weak | CLEAN-21 |
| Postcode | postcode (lookup) | yes | category (string), 208; 1 NaN (Fawkner Lot) | fine | CLEAN-14 |
| Bedroom2 | "Scraped # of Bedrooms (from different source)" | looked up after the sale (step 4) | float64; 0 -> NaN; 23% NaN | potential leak, kept by measurement | LEAK-10 |
| Bathroom | "Number of Bathrooms" (scrape) | after the sale | float64; 0 -> NaN; 1-9 | as Bedroom2 | LEAK-10 |
| Car | "Number of carspots" (scrape) | after the sale | float64; 0 kept (859 houses; plausible); max 18 | as Bedroom2 | LEAK-10, CLEAN-11 |
| Landsize | "Land Size in Metres" (scrape) | after the sale | float64; 0 kept (units); units also carry the whole strata lot (246 units > 1,000 m2) | as Bedroom2; meaning differs by Type, keep | LEAK-10, CLEAN-11 |
| BuildingArea | "Building Size in Metres" (scrape) | after the sale | float64; 0 -> NaN; 61% NaN; impossible values at both ends remain | as Bedroom2 + cleaning problem (problem 3) | LEAK-10, CLEAN-11 |
| YearBuilt | "Year the house was built" (scrape) | after the sale | float64; < 1835 -> NaN; > sale year blanks the block (6 rows) | as Bedroom2 | LEAK-10, CLEAN-11 |
| CouncilArea | "Governing council for the area" (lookup) | yes | category, 33; 2 NaN (Fawkner Lot, one Footscray row) | fine | |
| Latitude | "Self explanitory"; source: the realestate.com.au scrape (co-missing, see problem 1) | after the sale, but location does not change | float64, 22% NaN; precision changes on 27 May 2017 (4 to 5 decimals) | fine; documentation mismatch | LEAK-10, writing |
| Longitude | as Latitude | as Latitude | as Latitude | as Latitude | |
| Regionname | "General Region" (lookup) | yes | category, 8; 2 NaN | fine | |
| Propertycount | "Number of properties that exist in the suburb" (lookup; reference year unknown) | yes (static suburb attribute, no label) | float64; constant per suburb in both periods; 2 NaN | fine | LEAK-29 not triggered |
| (dropped) Method | auction result S/SP/PI/VB/SA... | no, post-auction | dropped | correct | LEAK-10 |

**Problems, ranked (principles.md)**

1. **P4, LEAK-10 (Must, weak by measurement): the realestate.com.au block is a post-sale lookup.** Kept under the
   rule's own clause "unless the data shows they did not change": Bedroom2 == Rooms in 98.9-100% of each test window
   (checklist); missingness of the block is time-driven (11.9%-35.6% by quarter), not outcome-driven (mean residual
   log price within suburb x type x rooms x quarter: -0.007 missing vs +0.002 present). Consistent with the
   precedent row already in the LEAK-10 Mechanisms table. New fact: **Latitude/Longitude belong to the same scrape**
   (4,760 of 4,915 rows without the block also lack coordinates; 14 of 16,351 with it do), yet `task_summary.known`
   lists the coordinates with the listing data and `SCRAPED_ATTRIBUTES` omits them. A location does not change, so no
   leak; remedy: correct the wording (coordinates come from the post-sale scrape) and keep them, including for the
   six blanked rows.
2. **P3/P4 cross-reference (not a column): Method's removal is right, but keeping only S/SP/SA conditions the target
   on a sale** (a property passed in is not in test). For the split/domain auditors (USE-5, LEAK-22); no column
   remedy.
3. **P7, CLEAN-11 (Should): impossible BuildingArea values kept.** 47 dwellings of 1-10 m2 (median 3 rooms; 15
   houses, 22 townhouses, 9 units at 0-5 m2) and about 30 rows above 200 m2 per room, several equal to Landsize
   (673/673, 805/808, 44,515 on a 44,500 m2 lot, 6,791 m2 on a 732 m2 lot, a 1-room unit of 999 m2). The note
   "92 sales of 1-29 m2, kept" departs from CLEAN-11 without a fact. Mildest remedy: set BuildingArea to missing below
   10 m2 and where it exceeds 1,000 m2 or equals Landsize for a house. Question for the curator: values of 10-29 may
   be in "squares" (9.29 m2, the Australian unit), which would be a CLEAN-21 unit mix; circumstantial only.
4. **P7, CLEAN-21 (Should): Distance on two scales.** The suburb table switches on 27 May 2017. Against the
   straight-line km from the coordinates to the GPO (suburb medians), the earlier table is off by MAE 0.62 km, the
   later by 1.46 km (median -1.2 km; Airport West 13.5 -> 10.4 with 12.6 straight-line). The kept-with-a-note
   departure cites only the effect (-0.0004 RMSE), not a fact that sets the case apart. Remedy: one value per suburb
   (the later table, which all test windows use), or keep and state it as an exception.
5. **P7, CLEAN-1 (Weigh): Date of 11 sheets is the download day** (2,034 rows, 1-3 days after the sheet's Saturday;
   the companion file has the same dates). No effect on the windows (unit="unique"); a derived weekday is an
   artefact. Optional remedy: snap to the preceding Saturday, or one line in the notes.
6. **P7, repair (Weigh): two rows lose their suburb lookup.** The "Fawkner Lot" row (now Fawkner) lacks Postcode,
   Distance, CouncilArea, Regionname, Propertycount; one Footscray row lacks CouncilArea, Regionname, Propertycount.
   Optional: fill from the suburb's own lookup values (deterministic, not imputation).

No column found that should be dropped; no identifier encodes the label; no proxy missing codes remain (Car 0 and
Landsize 0 are real values).

</details>

<details><summary>Split audit</summary>

**Split audit: melbourne_housing_market (re-check, 2026-10-20)**

**Verdict: right with notes.** Temporal on `Date`, 9 expanding windows of 3 weekly sheets, is the regime the use case
needs (a sale price of a coming auction: SPLIT-6, SPLIT-1). One note on the gap, the rest pass.

Analyses: windows, dates and addresses; sheet counts FULL vs LESS; LightGBM (fixed parameters, Address dropped, Date
as days; shipped vs gap vs IID). Built container rebuilt through
`dataset_io.load(..., built=True)` (origin `rebuilt`), 21,266 rows.

**Regime (USE-10, SPLIT-3, SPLIT-6, SPLIT-13)**

- Entity: the property. 45 addresses sell twice; 0.0-0.52% of each window's test addresses occur in train (resales,
  legitimate history under a temporal split). Each auction is effectively a new property; suburb, postcode, agent and
  council are features new rows keep (SPLIT-4). Known-entity vs cold start does not change the regime: temporal.
- Hidden-group probe (temporal): no hits; Propertycount/Suburb seen 99.6% in train = suburb features (SPLIT-4). Near
  copies at 0.85: 8.6% of test rows have one in train (2.2-14.4%): units of one building or street, which new listings
  also have; not an entity new data lacks (SPLIT-29/30: pass).

**Windows (SPLIT-11, SPLIT-14, SPLIT-15, SPLIT-17)**

| window | train rows | train share | train ends | test sheets | test rows |
|---|---|---|---|---|---|
| 0 | 20,147 | 0.947 | 2018-02-24 | 3, 10, 17 Mar 2018 | 1,119 |
| 1 | 19,078 | 0.897 | 2018-02-03 | 10, 17, 24 Feb | 1,069 |
| 2 | 18,985 | 0.893 | 2017-12-16 | 20, 27 Jan, 3 Feb | 93 |
| 3 | 17,459 | 0.821 | 2017-11-18 | 25 Nov, 9, 16 Dec | 1,526 |
| 4 | 16,426 | 0.772 | 2017-10-28 | 4, 11, 18 Nov | 1,033 |
| 5 | 14,876 | 0.700 | 2017-10-07 | 14, 21, 28 Oct | 1,550 |
| 6 | 14,008 | 0.659 | 2017-09-16 | 23, 30 Sep, 7 Oct | 868 |
| 7 | 12,868 | 0.605 | 2017-08-26 | 3 (Sun), 9, 16 Sep | 1,140 |
| 8 | 11,753 | 0.553 | 2017-07-29 | 12, 19, 26 Aug | 1,115 |

Every test window lies strictly after its train side; all lie after the coverage change of 27 May 2017; smallest
train share 0.553 (SPLIT-14 pass), smallest window 93 rows (SPLIT-17 pass). The `unique` unit counts sheets: after 27
May 2017 every date is one weekly sheet (one Sunday date, 3 Sep 2017, 567 rows, the sheet of that weekend). Small
sheets are real lulls, also small in the LESS file: 30 Sep 2017 (AFL Grand Final, 15 FULL / 16 LESS sales), 4 Nov
(Melbourne Cup, 66/77), 20 and 27 Jan 2018 (9/10, 9/9), 10 Mar (Labour Day, 98/117). Sheets of 10 Jun, 5 Aug, 2 Dec
2017 and 13 Jan 2018 are absent in both files, so windows 3 and 8 span 4 calendar weeks (already REVIEW issue 5).

**Season and training history (SPLIT-20, SPLIT-21)**

Test windows run Aug 2017 - Mar 2018: the spring peak, the summer lull (one window) and the autumn start; no window
is atypical as a whole. Train holds Jan 2016 onward (over one full year before every window). Break: before 27 May
2017 only inner suburbs; kept, measured on all 9 windows (0.183 vs 0.188), a design argument as well (more history of
the same market), so SPLIT-21 is not violated. Note: window 8 has only 9 weekly sheets of full coverage in train.

**Gap and late labels (SPLIT-9, SPLIT-10, SPLIT-12)**

A price is published in the sheet of its auction weekend, so no training row lacks its label at the window start
(SPLIT-9 pass). The prediction point, however, is "when a property is listed for auction"; a Melbourne auction
campaign is about four weeks (Collings guide; 2-3 weeks in hot markets, Real Estate Business 2021). At listing the
newest known sale is ~4 weeks before the auction, while the shipped split trains on sales up to 1 week before the
first test sheet. Measured (LightGBM, mean RMSE log price over 9 windows):

| setting | RMSE | vs shipped |
|---|---|---|
| shipped, no gap | 0.1841 | - |
| no Date feature | 0.1851 | +0.0010, worse 6/9 |
| gap 14 days | 0.1850 | +0.0009, worse 5/9 |
| gap 28 days | 0.1865 | +0.0024, worse 8/9 |
| gap 28 days, no Date | 0.1878 | +0.0037, worse 8/9 |
| IID 3x3, all rows | 0.1851 | +0.0010 |
| IID 3x3, rows from 27 May 2017 | 0.1849 | +0.0008 |

The gap matters little in size (1.3%) but consistently (8 of 9). The IID score is not better than the temporal one:
the market drifts slowly over a few weeks, and the temporal split costs nothing in learnability.

**Problems, ranked (P4)**

1. **Prediction point vs gap (P4, SPLIT-10 / SPLIT-12, Should; USE-3).** The use case says "when listed", the split
   evaluates "the week before the auction". Evidence: 4-week campaign norm; 28-day gap +0.0024 RMSE, worse in 8/9.
   Mildest remedy: either add `time_gap` of 4 weeks (train on sheets dated at least 28 days before each window's
   start), or keep the split and state the prediction point as "before the auction, refit weekly" (a buyer's or
   agent's estimate in the campaign) in `task_summary.use_case` and `splits_comment`. The second is not only an excuse
   for the gap (USE-9 pattern): buyers do estimate during the campaign. Curator's choice; either way say it.
2. **Nominal horizon (SPLIT-12, Should; note).** `horizon=3 weeks` but windows 3 and 8 span 4 calendar weeks and window
   2 opens 5 weeks after its train side ends (holiday). Already disclosed (REVIEW issue 5); no change needed beyond
   the comment saying "3 sheets, up to 4 calendar weeks".
3. **Thin full-coverage history for the oldest window (SPLIT-20, note).** Window 8 trains on 9 full-coverage sheets
   plus the inner-suburb years; measured and kept; no remedy needed.

No problem found with: regime choice, late labels, window count and sizes, hidden groups, resales across the split.

</details>

<details><summary>Domain practitioner</summary>

**Domain practitioner: melbourne_housing_market**

Actor: a Melbourne buyer's advocate (or a listing agent, or an automated-valuation desk) who is about to see a property
go to auction. The actor wants an independent estimate of the sale price, usually to check it against the agent's
price guide.

**Fit: direct**

What I have when a property is listed, plus the sales before it, predicts the price at the auction a few weeks later.
The test windows are the coming auctions in later weeks. That matches what I decide (USE-1, USE-3, USE-8).

**The four questions, as the actor**

1. **Inputs at the prediction point.** I have all of the sheet's fields: suburb, address, postcode, council, region,
   type, rooms, agent, the auction date and the suburb's property count. I also have the earlier sales. Bedrooms,
   bathrooms, car spaces and land size are on every listing. The scraped copies were looked up after the sale, but the
   README shows Bedroom2 = Rooms in 98.9-100% of each test window, so they stand in well (USE-3, LEAK-10 checked).
   What I would always have but the data does not:
   - (a) The agent's indicative selling price. In Victoria it has been on the Statement of Information since
     1 May 2017, which covers every test window.
   - (b) Coordinates for every property. 22% are missing here, but I would geocode the address.
   - (c) Building area and year built more often. They are 61% and 56% missing; the listing's floor plan and photos
     usually show them.
   - (d) The listing text and photos, and the property's earlier sale price.

   Nothing in the features is something I would not have. Method, the auction outcome, is dropped correctly.
2. **Target.** I act on the sale price in dollars and on a range around it. Log price is the right scale for an error
   relative to the price. A point estimate is what I would compare with the guide, though an interval would serve me
   better (USE-5 met).
3. **One row = one decision?** Yes: one auction listing gets one estimate. The test data stands for next month's
   auctions, mostly properties new to the model. The 45 resales use their earlier sale as history, which is right for
   a known property (USE-10). Small difference from practice: a listing goes up about four weeks before the auction,
   while the windows train right up to the window start (0-2 weeks of gap). Melbourne prices in 2017 moved about 1% a
   month, so this barely matters.
4. **Would I use it?** Yes, as a comparison point against the agent's guide. LightGBM reaches about 0.187 RMSE in log
   price, roughly ±19%. Desks that do this for a living report median errors of about 5-10%. I would trust it more
   with full coordinates and building size. I would distrust it for 2016-sourced history in the outer suburbs (not in
   the file before 27 May 2017) and for prestige homes whose price was withheld (rows without a price are dropped,
   which removes more of the top end).

**Gaps, ranked by how much they change the task**

1. **No agent price guide.** This is the strongest input in practice. Without it the task is "price it independently
   of the guide". USE-9 makes that a real use case (a buyer checking for underquoting, an AVM), not a stand-in, so the
   fit stays direct. If the guide were kept, USE-6 would count it as a legitimate input. The source does not have it,
   so this is no fault of the curation.
2. **Selection on outcome.** Only results that sold are kept; passed-in and vendor-bid results are dropped. At listing
   time I do not know whether the property will sell, so the test set leaves out the about 20-30% of auctions that pass
   in. Industry valuation models are also validated on sales only, so this is standard. It should be named in
   fit_reason or changes. It already appears in `changes`.
3. **Missingness I would not face.** Coordinates are 22% missing and building area and year built 56-61%. This is an
   artefact of the scrape, not of the decision, so the task is harder than in practice. It does not change the
   ranking of models.
4. **Scraped attributes are post-sale lookups.** They are close in time for the test windows and the effect is
   measured at ±0.0004 RMSE. This is a negligible gap.
5. **Horizon.** There is no gap of about four weeks between listing and auction, and the market moves little in that
   time. This is a negligible gap.

**What a domain expert would change**

- Add the indicative price if a source for it is ever found (Domain or REIV listings). Today none exists in this file.
- Geocode the 22% of addresses without coordinates from Address + Suburb + Postcode. This is optional, and the
  benchmark can keep the missing values as they are.
- Optionally note in `fit_reason` that the population is auction listings that ended in a sale with a disclosed
  price.
- Keep log price, Method dropped, the temporal windows and the scraped block. These are the choices a valuation team
  would make.

**Sources**

- D: datasets/_dev/tabarena-v0pt2/melbourne_housing_market/dataset.py (task_summary, curation_comments)
- README.md and REVIEW.md of the folder (Bedroom2/Rooms agreement, missingness table, coverage table)
- panel/probes/task_stdout.txt (LightGBM RMSE 0.187), hidden_stdout.txt
- Rules: .claude/skills/knowledge-curation/references/use_case.md (USE-1, USE-3, USE-5, USE-6, USE-8, USE-9, USE-10)
- Consumer Affairs Victoria, underquoting and Statement of Information (indicative price, from 1 May 2017):
  https://consumer.vic.gov.au/licensing-and-registration/estate-agents/running-your-business/understanding-underquoting
- https://www.apartments.com.au/news/victoria-underquoting-laws-start-may-1
- Kaggle data card: https://www.kaggle.com/datasets/anthonypino/melbourne-housing-market
- The figures for the clearance rate (about 20-30% passed in) and the AVM error (5-10%) are domain knowledge, not
  checked against a cited source here.

</details>

<details><summary>Blind review</summary>

**Blind review: melbourne_housing_market (log_price, regression, temporal)**

**Verdict: include with changes.** This is a real and useful task: valuing a Melbourne home at or before auction. The temporal split is honest. The changes are small preparation fixes.

**Use case**
Buyers, agents, banks and automated valuation tools estimate a sale price from the listing details before the sale. The data comes from public auction results that Tony Pino scraped from Domain.com.au, so it is real data.

**Concerns, most serious first**
1. **`Address` is a free-text identifier.** It is unique for almost every row; only 90 rows are repeat sales of 45 addresses, for example "12 McGuire Cr, Williamstown" in 2016-05 and again in 2018-03. As a feature it either adds noise or lets a model memorise repeat sales. Fix: drop it, or keep it only as a group id.
2. **Row filtering is not documented.** The source has about 27k priced rows (34,857 in total); this table has 21,266. The `Method` column (S/SP/PI/VB/SA) was also dropped. Prices for PI (passed in) and VB (vendor bid) are not sale prices, so filtering them out would be correct. Fix: state the filter in the task description.
3. **Implausible values.**
   - 1,420 rows have `Landsize == 0`; units genuinely have no land, so these are not obviously wrong.
   - `BuildingArea` goes up to 44,515 m2 and `Landsize` up to 89,030.
   - `YearBuilt` goes back to 1850.
   - `Rooms` and `Bedroom2` are two scrapes of the same thing (r=0.97).
   - Fix: set obvious errors (e.g. BuildingArea > 2,000) to NaN.
4. **Missing values are heavy but real:** BuildingArea is 61% missing, YearBuilt 56%, Latitude/Longitude 22%. They are correctly stored as NaN. I would leave them.
5. **The time windows are uneven.** 2016Q1 has only 27 rows and the data ends at 2018-03. Prices drifted in 2017, which makes a temporal split meaningful.

**Signal check**
I trained LightGBM on the first 80% of rows by date and tested on the last 20%, without `Address`. It reached R2 = 0.84 (RMSE 0.19 in log price; the standard deviation of the target is 0.48). Using only Rooms, Type, Distance and Regionname gave R2 = 0.80. So there is strong signal, but the task is not trivial and it is big enough to score.

**Not checked**
- The exact row filter the preparer used.
- Whether the snapshot and full Kaggle versions were merged.
- How the 9 split windows are defined.

</details>

<details><summary>Precedent check</summary>

**Precedents: melbourne_housing_market (re-check, 2026-10-20)**

Inputs: `register.json` / `register.txt` (808 decisions), the Cases tables of `leak_checks.md` and `provenance.md`,
`records.md` (duplicates), and the sibling house-price definitions in `datasets/_dev/tabarena-v0pt2/`: `house_sales`
(King County), `perth_house_prices`, `zillow_prize`, `house_prices_nominal` (Ames), `california_house_prices_2020`.
None of the register's four flag groups (few_minority, one_feature, scaling drift, trivial) touches this dataset or a
housing rule. No curator decision on this dataset exists yet. The only curator line is the CC on
`melbourne_housing_snapshot` (2026-10-12).

**Per decision**

| # | Decision (definition / REVIEW issue) | Verdict | Closest precedents |
|---|---|---|---|
| 1 | FULL file rather than LESS (issue 1) | consistent | No rule decides between "more rows" and "more columns" within one source. Like house_sales (assessor extracts added for the record as of the sale), the choice rests on a measured gain (0.183 vs 0.211). Both files are cuts of one upload, so PROV-6 is met by shipping one. |
| 2 | Sale prices only, PI/VB dropped (issue 2) | consistent on the rows, departs on the framing (prompt A) | house_sales drops 1,061 non-market sales whose price sits 0.14-0.23 below the model. PI/VB bids are the same kind of case: a price that is not a market sale, here 4.3%/6.6% below the model. Every sibling ships sold properties only: house_sales, perth, zillow, Ames. LEAK-22 (follow the cohort that can have the outcome). **But** every sibling sets the prediction point at "a property sells" (house_sales fit text; perth `curation_comments` l.78; Ames issue 4 "an automated valuation model, as in house_sales and zillow_prize"). Melbourne alone says "listed for auction" (`question`, `use_case`, first bullet). A property listed for auction can be passed in, so the sold-only cohort fits the siblings' point and not the one written here. No written fact explains why melbourne differs. |
| 3 | Scraped attributes kept, 6 rows blanked, 495 not (issue 3) | consistent in substance, departs from the house rule on the note (prompt B) | LEAK-10 Cases row "Attributes looked up after the outcome", remedy "drop them, or keep them where the data shows they did not change" (house_sales). house_sales rebuilt each row as of its sale and kept the residue (~145 view/waterfront rows) because "blanking them would make the missing value mark a change after the sale". That is the same argument as for the 495 here, with an effect of the same size (0.2147 vs 0.2132). house_sales also rebuilt `yr_built` for teardowns: "the record at the sale describes what was sold". Melbourne blanks the 6 later buildings for the same reason. **Two points.** (i) house_sales labels its residue `Potential leak, kept on purpose:` (definitions.md l.488; leak_checks.md l.193). Melbourne's bullet ("Other late lookups stay") has no such label and no revisit condition. (ii) The LEAK-10 Cases row already says "melbourne_housing_market kept". It was added in #11 (58ee235, 2026-10-20) by the AI's work on this dataset while issue 3 is still open for Lennart. It is not a curator precedent and should not be cited as one until he decides. Also, the 2016 training rows match only 85.2%, so they are not rows "where the data shows they did not change". The keep rests on house_sales' residue argument, not on the row's remedy as worded. |
| 4 | Coverage change on 27 May 2017, all rows kept (issue 4) | consistent | house_sales dropped May 2015 because the incomplete month lay in the test period and was biased (cheaper, quickly recorded sales). Here every test window lies after the switch, and the trade-off was measured (0.183 vs 0.188). The facts that differ are written down. EV-1 aeolus (training history from the use case) is not contradicted: the use case "refit on all earlier sales" keeps them. |
| 5 | 9 windows of 3 weekly sheets, no gap (issue 5) | consistent, with stated reasons | house_sales: 9 windows of 3 weeks, `min_train_fraction=0.5`, "the 3 x 3 an IID task of this size gets". Melbourne copies it. `unit="unique"` instead of weeks has a stated fact: missing sheets and the January lull. The missing gap (house_sales `gap=1` for the recording delay, zillow `gap=1`) has a stated fact: "a price is published in the sheet of its week". Ames uses no gap for the same reason (issue 4). |
| 6 | Re-dated holiday sheet (issue 6) | consistent | PROV-13 to PROV-15 repair with an asserted count, as in the california_house_prices_2020 re-sort (SPLIT-22 Cases). |
| 7 | Snapshot record (issue 7) | consistent; the issue text is stale | `curation/records/melbourne_housing_snapshot.md` already carries `No` + `Duplicate` (+ `No Good Target (yet)`) with Lennart's CC of 2026-10-12. REVIEW issue 7 still describes it as lacking the marker. The rename to `melbourne_housing_market_duplicate` is not required: records.md l.130 lets "an existing record keep its name". colleges (2026-10-12) and arsenic_male_lung kept their names with the `Duplicate` marker. The leftover `No Good Target (yet)` marker is the only difference from colleges. The vitticeps extraction would be out under PROV-3 (simulated attributes). |
| 8 | Repeated reports within 60 days (issue 8) | consistent | house_sales keeps resales as history under a temporal split (LEAK-34). Melbourne keeps resales 63-679 days apart for the same reason. Dropping same-price re-reports is de-duplication of one event. house_sales' kept "conflicting duplicate" is two different parcels, not one address at two prices, so it is no counter-case. |
| 9 | `year = "2018"` (issue 9) | consistent under PROV-9's last clause; the REVIEW cites the wrong precedent | PROV-9: a Kaggle dataset's first version, **but** "a source that grows over time (a public register, a scraped site, a monthly archive) takes the year of the snapshot we pin". This upload grew across versions: public by Mar 2017, the dansbecker cut ends Sep 2017, FULL ends Mar 2018, LESS ends Oct 2018. The siblings that use the clause: sf_permit_time, consumer_complaints_1m and kickstarter (`year = "2026"  # the snapshot we pin; the source grows over time`). house_sales (2015, first distribution) is a fixed file, so it does not argue for 2017 here. Two gaps: the download is not pinned to a Kaggle version (checklist), and the code comment gives "last updated", not the PROV-9 reason. |
| 10 | Licence CC BY-NC-SA 4.0, scraped source (issue 10) | consistent | perth_house_prices ships under the same licence. EV-4 (lucas_topsoil): licence terms are noted and do not decide the triage. |

**Drift and third exceptions**

* Drift: none found. Lennart has no decision yet on LEAK-10 lookups for melbourne. His house_sales choice was to
  rebuild as of the sale and keep a small residue with a note, which matches the implementation here.
* Third exception: no. Keeping post-sale lookups where blanking would encode the change has two cases: house_sales
  (view/waterfront) and melbourne (2016 rows). If a third housing dataset needs it, the LEAK-10 row should be amended
  to say "or keep the residue with a note when blanking would mark the change and the effect is within noise".

**Reflection prompts (departures without a stated reason)**

**A. Prediction point (issue 2; USE-5, LEAK-22).**

```text
**Consistency check (AI, 2026-10-20):** your call on melbourne_housing_market (prediction point "listed for
auction", rows: sales only) differs from house_sales, perth_house_prices and house_prices_nominal (all "a property
sells", sold rows only; house_sales also drops non-market prices). Same mechanism: a sale-price model over sold
properties. What sets melbourne apart?
(a) the auction listing is the moment a buyer or agent uses the estimate, and the passed-in 22% have no sale price to
    learn, recorded as an exception to the siblings' framing; (b) treat it like them: reword the task_summary to
    "a property sells (at or around its auction)" and keep the rows as they are; (c) reopen the siblings to an
    earlier point; (d) change the rule (an amendment).
```

**B. Kept post-sale lookups without the note (issue 3; LEAK-10, LEAK-11, definitions.md "Recording decisions").**

```text
**Consistency check (AI, 2026-10-20):** your call on melbourne_housing_market (keep the realestate.com.au lookups,
including the 495 2016 sales whose Bedroom2 differs from Rooms) is written as a plain bullet, while house_sales
(view, waterfront, neighbours' areas as of July 2015, same argument: blanking marks the change, effect ~0.0015)
carries a `Potential leak, kept on purpose:` note with a revisit condition. What sets melbourne apart?
(a) nothing: label the bullet `Potential leak, kept on purpose:` with the 85.2% / 98.9-100% figures and a revisit
    condition (a dated attribute history becomes available); (b) blank the 495, departing from house_sales; (c)
    reopen house_sales to blank its residue; (d) amend LEAK-10's Cases row to name this residue remedy.
```

Also, outside the prompts: the LEAK-10 Cases row "melbourne_housing_market kept" should wait for Lennart's answer to
issue 3 (or be marked provisional), and REVIEW issue 7 should say the `Duplicate` marker is already set.

</details>

<details><summary>Advocate</summary>

**Advocate: melbourne_housing_market (opening brief, 2026-10-20)**

Position: ship as defined. The validity rules (P1-P5) hold. What the evidence agents found is wording, one notes label
and P7 cleaning. Each has a mild fix that keeps the dataset.

**1. A real task with a direct fit (P3: USE-1, USE-5, USE-8 Must; USE-9 Should)**

* Evidence: the practitioner (a buyer's advocate, listing agent or AVM desk) gives `direct`: "Nothing in the features
  is something I would not have", and "Keep log price, Method dropped, the temporal windows and the scraped block.
  These are the choices a valuation team would make". The blind reviewer, without our notes, calls it "a real and
  useful task" and says include. Claim audit 1-4 and 17 hold: every train side is all earlier sales, and the target
  is `ln(price)`.
* The missing agent price guide does not lower the fit. USE-9 names a real use case that works without it: an
  independent check against underquoting, as an AVM does it. The source never had the guide (practitioner gap 1).
* Answers: "approximate" or "no clear actor". P3 is the highest-ranked principle in play after P1-P2, and both pass
  it.

**2. Worth benchmarking (P6: TP-1 to TP-10)**

* Evidence: LightGBM skill +0.834 (SE 0.014). The model beats the dummy on 5 of 5 splits. The best single feature
  (Postcode) reaches only 0.426, and no probe flags. The leak probes find no drop-one loss above 0.004 and a depth-2
  tree at R² 0.10. The smallest window has 93 rows and a non-constant target.
* Answers: "trivial" or "too small". Neither has evidence behind it.

**3. The split is the right regime and costs nothing (P4: SPLIT-1, SPLIT-6, SPLIT-11, SPLIT-14, SPLIT-17)**

* Evidence (split audit): the split is temporal with expanding windows. Every test window lies strictly after its
  train side and after the coverage change of 27 May 2017. Train shares are 0.553-0.947. The hidden-group probe has
  no hits.
* The temporal score is not harder than an IID one: IID 3x3 gives 0.1851, shipped 0.1841. So the split matches the
  application without making the task artificially hard (Tensions: "the split follows the application").
* The layout is the house_sales precedent (9 windows of 3 weeks, `min_train_fraction=0.5`). `unit="unique"` rests on
  a measured fact: calendar windows would leave a window of 9-18 sales.
* Gap objection (SPLIT-10, Should). SPLIT-10 is about labels that arrive late. Here no label is late: a price is
  published in the sheet of its own week (SPLIT-9 passes). The remaining point is a planning gap, because listing
  happens about 4 weeks before the auction.
  * Its effect is small: +0.0024 RMSE (1.3%) with a 28-day gap. I concede it is consistent (worse in 8 of 9 windows).
  * Mildest fix: state the prediction point as "during the auction campaign, refit weekly". Buyers do estimate at that
    point (split audit: "not only an excuse for the gap"). The alternative is `time_gap` of 4 weeks. Either fix keeps
    the dataset; the curator chooses.
* Horizon wording: window 2 predicts 5-7 weeks ahead, and windows 3 and 8 span 4 calendar weeks. I concede this.
  Write "3 sheets, up to 7 calendar weeks across the January lull" (SPLIT-12, Should; writing only).

**4. Sold-only rows are the correct target, not a cohort leak (P3/P4: USE-5 Must, LEAK-22 Must)**

* Evidence: PI and VB prices are bids. A sale model places them 4.1% and 6.5% below its prediction, and sales +0.3%
  (claim audit 20). Training on them would put a different quantity into the target, which breaks USE-5, a Must.
* Precedent: every sibling ships sold rows only (house_sales also drops non-market prices; perth, zillow, Ames). The
  practitioner confirms that industry AVMs are validated on sales.
* LEAK-22 says to follow the source's cohort, and that cohort is sales. Nothing in the rows needs to change.
* Concession: the framing differs from the siblings (precedents prompt A). Mildest fix, wording only: "a property
  listed for auction that sells; its sale price", or prompt A option (b). `changes` already names the filter.

**5. The scraped attributes fall under LEAK-10's own exception (P4: LEAK-10 Must, read in full)**

* Rule text: LEAK-10 rules out lookups after the outcome "unless the data shows they did not change". The data shows
  exactly that:
  * `Bedroom2 == Rooms` in 98.9-100% of every test window.
  * The dansbecker snapshot (Sept 2017) carries identical scraped values for the 2,728 test rows up to 23 Sept 2017
    (100% match).
  * Missingness does not follow the outcome: within suburb x type x rooms x quarter, the mean residual is -0.007 for
    missing rows and +0.002 for present rows.
  * The six 2016 rows with a later YearBuilt are blanked.
  * Blanking the 495 mismatched 2016 sales changes RMSE by -0.0005 to +0.0003 across 3 seeds, inside the noise.
* Precedent: house_sales keeps a residue of the same size for the same reason (blanking would mark the change).
* Concessions, all on the notes:
  * Label the bullet `Potential leak, kept on purpose:` and give a revisit condition (precedents prompt B, option a).
  * Mark the LEAK-10 Cases row "melbourne kept" as provisional until Lennart decides.
  * Say that the coordinates come from the same scrape. A location does not change, so they stay (column audit 1).
* `direct` vs `approximate` (USE-8): kick is approximate because its kept field encodes the outcome through
  missingness. Here the data shows no change and no outcome-driven missingness. If the curator prefers
  `approximate`, that is a label change, not a reason to hold the dataset back.

**6. Faithful and unique data (P5: PROV-4, PROV-6, PROV-9, PROV-13)**

* The md5 of both raw files match.
* The copied holiday sheet is repaired from the companion file with an asserted count: 787 of 787 rows (PROV-13,
  repair first).
* FULL over LESS is measured: 0.182 vs 0.206, worse in 9 of 9 windows.
* The snapshot is a subset (13,580 of 13,580 rows). Its record already carries `Duplicate` from Lennart's CC of
  2026-10-12, so REVIEW issue 7 is out of date.
* `year = "2018"` follows PROV-9's clause for a growing source (precedents 9).
* Remaining gap: pin the Kaggle version. This is a reproducibility note, not a validity issue.

**7. The P7 findings are notes or cheap fixes, not blockers (step 3; remedy ladder; "independent failures are not conflicts")**

* BuildingArea: 47 rows are 1-10 m², and some equal the Landsize. CLEAN-11 is a Should, and I concede the fix:
  BuildingArea below 10 m², or equal to the Landsize for a house, becomes missing. The row stays.
* Distance on two tables, CLEAN-21 (Should): put each suburb on the later table, which every test window uses. The
  effect is within noise (-0.0008 to 0.0000).
* The download-day dates of 11 sheets and the two rows missing suburb lookups are Weigh-level items. A note covers
  them.
* EV-6 and writing fixes:
  * Write the ±0.0004 effects as "within run-to-run noise".
  * Change "no known risk" to "known risk: post-sale lookup of six attributes, measured small".
* Blind review on Address: a resale's earlier sale is legitimate history (LEAK-34, a Must that narrows LEAK-10).
  Address alone as text scores R² -0.093, so it carries no shortcut. Keep it.

Judgment record (proposed):
Verdict: ship; the changes are wording, a notes label and two cheap P7 fixes.
Validity: USE-1/5/8 hold (direct); LEAK-10 holds through its stated exception (note label); LEAK-22 holds (sold cohort,
reworded); SPLIT-1/9/11 hold; SPLIT-10/12 Should: the prediction point and horizon stated (or a 4-week gap); PROV holds.
Value: TP passes (skill 0.834).
Quality: CLEAN-11 fix (BuildingArea), CLEAN-21 fix or exception (Distance), other notes.
For the curator: the prediction point wording vs `time_gap` (issue 1); `direct` vs `approximate` (issue 2).

</details>

<details><summary>Critic</summary>

**Critic: melbourne_housing_market (opening brief, 2026-10-20)**

**Position: ship only after changes.** The task is real and the evidence shows no strong leak, so I do not argue for
exclusion. My points are about the definition saying something the data and the split do not do, a kept post-sale
lookup without the note the house rules require, and claims the audits refuted. All the remedies are text or small
code changes.

**1. The written prediction point does not match the cohort or the split (P3/P4; USE-3 Must, LEAK-22 Must, SPLIT-10 Should)**

- **Problem.** `question`, `use_case` and the first `curation_comments` bullet say "when a property is listed for
  auction". The rows are sales only (S/SP/SA). The 5,939 passed-in and vendor-bid results with a price are dropped,
  about 22% of the 27,247 priced results (claim audit 7; checklist P3/P4 "concern"). So the test set holds only
  properties that turned out to sell, which nobody knows at listing. The split also trains up to the week before
  each test window. At listing, the newest known sale is about 4 weeks old (the campaign length).
- **Effect on the task.** The task as written ("at listing") is not the one we evaluate ("a sale at or just before
  its auction"). The score is a little better than what the stated use would see. A 28-day gap costs +0.0024 RMSE
  and is worse in 8 of 9 windows (split_audit, gap table).
- **Evidence.** precedents.md decision 2: every sibling (house_sales, perth_house_prices, house_prices_nominal,
  zillow_prize) sets the prediction point at "a property sells" with sold rows only. Melbourne alone says "listed",
  and no fact is written down to explain the difference (consistency prompt A). split_audit problem 1.
- **Remedy (fix the definition, wording only).** Restate the prediction point as the siblings' one: an estimate
  before the auction, refit weekly, for a property that sells. Name the sold-only cohort in `fit_reason`, and in
  `splits_comment` say why there is no gap. The other option is `time_gap` of 4 weeks while keeping "at listing".
  That option still does not settle the cohort under LEAK-22, so I ask for the rewording.

**2. The post-sale lookup is kept without its note, and the coordinates are left out of it (P4; LEAK-10 Must, definitions.md "Potential leak, kept on purpose")**

- **Problem.** The six realestate.com.au attributes were looked up after the sale. LEAK-10 keeps them only "where the
  data shows they did not change". That is shown for `Bedroom2` alone, as agreement with `Rooms`: 98.9-100% per test
  window, but 85.2% for the 3,107 training sales of Apr-Sep 2016 (claim audit 44/46). Bathroom, Car, Landsize,
  BuildingArea and YearBuilt have no pre-sale reference after Sept 2017 (claim audit, implied claims).
  - The keep is written as a plain bullet ("Other late lookups stay"). It has no `Potential leak, kept on purpose:`
    label and no condition for revisiting it. house_sales, the precedent for the same mechanism, has both
    (precedents decision 3, prompt B).
  - Latitude and Longitude come from the same scrape: 4,760 of 4,915 rows without the block also lack coordinates
    (column_audit problem 1). Yet `task_summary.known` lists them with the listing data.
  - The LEAK-10 Cases row already cites "melbourne_housing_market kept" as a precedent, before the curator has
    decided REVIEW issue 3.
- **Effect.** Small as measured: blanking the 495 mismatched 2016 sales changes the RMSE by noise only. The issue is
  the honesty of the record, not the score.
- **Remedy (a note plus a wording fix).** Label the bullet `Potential leak, kept on purpose:` with the 85.2% and
  98.9-100% figures, the scope (Bedroom2 checked, the other five assumed), and the revisit condition (a dated
  attribute history). Say in `known` that the coordinates come from the post-sale scrape. Mark the LEAK-10 Cases row
  provisional until Lennart decides. Weigh `fit = "approximate"` against `direct`: the kick precedent for a kept
  potential leak is `approximate` (claim audit 8-9). That is the curator's call.

**3. Refuted claims in the definition and the record (EV-1, EV-6; SPLIT-12 Should)**

- **Problem.**
  - "horizon 3 weeks": window 2 trains to 16 Dec 2017 and tests 20 Jan - 3 Feb 2018, 5-7 weeks ahead. Windows 3
    and 8 span 4 calendar weeks (claim audit 36; split_audit table).
  - "+0.0004" (fit_reason, CC) and "-0.0004" (Distance): single-seed figures inside the seed spread of 0.0007, and
    the signs flip across seeds (claim audit 10/24, 27).
  - The record's "no known risk" contradicts the definition's own kept post-sale lookup (claim audit 50).
- **Effect.** A reader takes noise as a measured effect, and the horizon as tighter than it is.
- **Remedy (repair the text).** Write "3 sheets, up to 7 weeks across the January lull"; "within run-to-run noise
  (|delta| <= 0.0008 over 3 seeds)"; in the record, "known risk: post-sale lookup of six attributes, measured
  small".

**4. Impossible BuildingArea values kept (P7; CLEAN-11 Should)**

- **Problem.** 47 dwellings of 1-10 m2 (median 3 rooms, including 15 houses). About 30 rows above 200 m2 per room,
  several equal to Landsize (673/673, 44,515 m2 on a 44,500 m2 lot), and a 1-room unit of 999 m2 (column_audit
  problem 3; blind review concern 3). The note "92 sales of 1-29 m2, kept" departs from the rule without a fact that
  sets the case apart.
- **Effect.** Noise in a feature; a quality issue, not a reason to exclude.
- **Remedy (cheap fix).** Set BuildingArea to missing below 10 m2, above 1,000 m2, or where it equals Landsize for a
  house. Note the 10-29 m2 "squares" question as circumstantial.

**5. Distance on two scales (P7; CLEAN-21 Should)**

- **Problem.** The suburb distance table changes on 27 May 2017 for 140 of the 142 suburbs present in both periods.
  Against the straight-line distance from the coordinates, the old table is off by MAE 0.62 km and the new one by
  1.46 km (Airport West 13.5 -> 10.4, straight-line 12.6) (column_audit problem 4). The kept-as-is note cites only
  an effect inside the noise, not a fact.
- **Effect.** One feature means two things across train and test; small in score.
- **Remedy.** Give each suburb one value: the later table, which every test window uses. Otherwise record it as an
  exception to CLEAN-21 with the fact.

**6. Small repairs (P7; CLEAN-1 Weigh)**

- **Problem.**
  - 11 sheets (2,034 rows) are dated 1-3 days after their Saturday: the download day (column_audit problem 5).
  - The "Fawkner Lot" row and one Footscray row lack their suburb lookup values (column_audit problem 6).
  - REVIEW issue 7 is stale: `melbourne_housing_snapshot` already carries `Duplicate` (precedents decision 7).
- **Remedy.** Snap to the sheet's Saturday, or add one line in the notes. Fill the two rows from the suburb's own
  lookup. Update the REVIEW text.

**Judgment record**

```text
Verdict: ship after changes.
Validity: USE-3/LEAK-22 triggered, fix the definition (prediction point "before the auction, for a property that
sells"); LEAK-10 kept by measurement, needs its `Potential leak, kept on purpose:` note and the coordinates named;
SPLIT-10 gap stated or added.
Value: TP holds (LightGBM skill 0.834, beats the dummy on all 5 probed splits).
Quality: CLEAN-11 fix BuildingArea; CLEAN-21 one Distance per suburb or an exception; CLEAN-1 date note.
For the curator: direct vs approximate (LEAK-10 residue, kick precedent).
```

</details>

<details><summary>Advocate rebuttal</summary>

**Advocate: rebuttal to the critic (2026-10-20)**

The critic and I agree on the verdict: ship, with every remedy at the "fix the definition" or "keep with a note" step
of the ladder. No point argues for exclusion. We differ only in how two of the fixes are justified.

**1. Prediction point vs cohort and split: concede the rewording; dispute part of the framing**

* **Conceded.** The wording "when listed for auction" does not match a sold-only test set or a split without a gap.
  Rewording to the siblings' point is the mildest fix that settles both. I drop my alternative of `time_gap`: the
  critic is right that a gap leaves the cohort question open.
* **Disputed: "LEAK-22 triggered".** The rows are already correct. Dropping PI/VB is required by USE-5 (Must):
  * their prices are bids, 4.1% and 6.5% below a sale model (claim audit 20);
  * keeping them would mix two quantities in the target;
  * the source's cohort for a sale price is sales, which is what LEAK-22 asks for.
  So this is a wording fix to `question`, `use_case` and the first bullet, not a cohort fix.
* **Disputed: "the score is a little better than the stated use would see".** That is only true of the old wording.
  Under the reworded point (an estimate in the campaign, refit weekly), the shipped split is the application.
  * The +0.0024 for a 28-day gap is what "at listing" would cost. Nobody evaluates "at listing" after the rewording.
  * The split audit says this framing is more than an excuse for the gap: buyers do estimate during the campaign
    (USE-9).

**2. Post-sale lookup: concede the note, the coordinates and the provisional Cases row; dispute "the other five assumed"**

* **Conceded.**
  * Label the bullet `Potential leak, kept on purpose:` with the 85.2% and 98.9-100% figures and a revisit condition.
  * Name the coordinates as part of the scrape in `known`.
  * Mark the LEAK-10 Cases row provisional until Lennart decides.
* **Disputed: the other five attributes rest on assumption alone.** Two measurements cover all six attributes:
  * The dansbecker snapshot, taken in Sept 2017, matches FULL on all six scraped values for 13,580 of 13,580 rows
    (claim audit 30). This includes the 2,728 test rows up to 23 Sept. So the lookups did not change between that
    snapshot and the final upload.
  * 22 of 32 resale pairs carry different values for the same address (claim audit 34). The lookups were made per
    sale, not a single current record per address.
  Neither is a pre-sale reference after Sept 2017, and the note should say so. But "assumed" understates what the
  data shows.
* **Disputed: direct vs approximate.** kick's kept field encodes the outcome through missingness: missing
  `WheelType` is 70.5% bad buys against 9.7% otherwise. Here missingness is neutral: the residual is -0.007 when the
  block is missing and +0.002 when present (column audit). The facts differ, so kick's precedent does not carry over
  ("treat like cases alike" applies to like facts only). This stays the curator's call. Either label ships.

**3. Refuted claims: concede all three**

* The horizon becomes "3 sheets, up to 7 weeks across the January lull" (SPLIT-12).
* The ±0.0004 figures become "within run-to-run noise (|delta| <= 0.0008 over 3 seeds)" (EV-6).
* The record's risk line is corrected. These were already conceded in my brief, points 3 and 7.

**4. BuildingArea: concede, with one narrowing**

* CLEAN-11 applies. Set to missing: values below 10 m², and values equal to Landsize for a house.
* For the 1,000 m² cut, set a value to missing only where it also exceeds the lot or is above 200 m² per room. Large
  houses on big lots exist in the outer suburbs, and CLEAN-11 keeps values that are "only unusual". This only narrows
  the fix; I do not dispute the rest.

**5. Distance: concede**

Use one value per suburb from the later table, which every test window uses (CLEAN-21). It is cheap and safe (P7, step
3), and its effect is within noise.

**6. Small repairs: concede**

* Snap the 11 sheet dates to their Saturday, or add a one-line note.
* Fill the two rows from their suburb's lookup values.
* Update the stale text of REVIEW issue 7.

**What follows**

* The verdict is ship after changes. There is no validity failure left.
* The disputes under points 1 and 2 change how the fixes are justified in the record, not the fixes themselves.
* The curator decides two things: `direct` vs `approximate`, and the exact wording of the prediction point.

</details>

<details><summary>Critic rebuttal</summary>

**Critic: rebuttal to the advocate (melbourne_housing_market, 2026-10-20)**

**Where we stand.** The advocate concedes every change I asked for: the prediction-point wording, the
`Potential leak, kept on purpose:` label, the coordinates, the provisional Cases row, the horizon and noise wording,
the BuildingArea fix, one Distance per suburb, and the record's "no known risk". We disagree on the verdict only. The
advocate writes "ship" while listing changes. Two of them are not optional:

- USE-3 (Must) requires the written prediction point to be the one evaluated.
- The house rule (definitions.md l.488) requires the note label for a suspect kept on purpose.

So the verdict is **ship after changes**, not "ship as defined". No point calls for exclusion.

**Point by point**

1. **Real task, direct fit (USE-1, USE-5, USE-8).** Concede. I never disputed that the task is real. The one open
   item, `direct` vs `approximate`, is under point 5.
2. **Worth benchmarking (TP).** Concede: skill 0.834, beats the dummy on all 5 probed splits, no flags.
3. **Split.** I concede the regime, the windows, the horizon fix and the IID comparison (0.1841 vs 0.1851).
   - I dispute one claim: that "SPLIT-10 is about labels that arrive late". The rule's text says: "A planning gap the
     use case has (a forecast made a day ahead) is a gap too." A 4-week gap from listing to auction is such a gap.
     With the definition as written, SPLIT-10 applies: the 28-day gap costs +0.0024 RMSE, worse in 8 of 9 windows.
   - The fix the advocate offers (state the prediction point as "during the campaign, refit weekly") is the one I
     asked for, and it removes the trigger. Either that or `time_gap` must land before shipping, because the current
     text and the split disagree (USE-3, Must).
4. **Sold-only rows (USE-5, LEAK-22).** Concede on the rows: PI/VB are bids (-4.1%, -6.5%), and every sibling ships
   sales. The rows stay.
   - I dispute "nothing needs to change". LEAK-22 follows the cohort that can have the outcome. Under "listed for
     auction", a passed-in property belongs to the cohort but has no sale price. The cohort is right only once the
     prediction point says "a property that sells".
   - The advocate concedes that wording. It is a required fix of the definition, not a style choice.
5. **Scraped attributes (LEAK-10).** Concede the keep, the snapshot match (2,728 test rows, 100%) and the missingness
   residuals (-0.007 vs +0.002).
   - Concede that kick differs: its missingness follows the outcome (LEAK-38), and here it does not. That weakens my
     `approximate` suggestion. I leave `direct` vs `approximate` to the curator as a Weigh.
   - Still true: the "did not change" evidence covers Bedroom2 only. The other five attributes rest on inference, and
     the 2016 training rows match at 85.2%. That is why the note label with its scope and revisit condition is a
     requirement (precedents prompt B, house_sales), and the advocate concedes it.
6. **Provenance (PROV).** Concede all.
   - PROV-9: the year "2018" holds under the clause for a growing source.
   - REVIEW issue 7 is stale. This is my point 6; we agree.
   - The version pin is a reproducibility note. The stated md5s already fix the files.
7. **P7 findings.** Concede that they are fixes, not blockers. This is my position too (steps 3 and 5). We agree on
   CLEAN-11 and CLEAN-21. On the dates and the lookups, a note is enough.
   - Address (LEAK-34): I did not raise it, and I agree it stays.

**Judgment record (critic, after rebuttal)**

```text
Verdict: ship after changes.
Validity: USE-3/LEAK-22 fix the definition (prediction point "before the auction, refit weekly, for a property that
sells"; or a 4-week time_gap); SPLIT-10 then not triggered; LEAK-10 holds via its exception, with the required
`Potential leak, kept on purpose:` note (scope: Bedroom2 checked, five attributes and the coordinates from the same
scrape), Cases row provisional.
Value: TP holds.
Quality: CLEAN-11 BuildingArea fix; CLEAN-21 one Distance per suburb; CLEAN-1 date note; text repairs (horizon, noise,
"no known risk", REVIEW issue 7).
For the curator: wording vs time_gap; direct vs approximate (Weigh).
```

</details>

<details><summary>Mediator</summary>

**Mediator: melbourne_housing_market (2026-10-20, re-check, full tier)**

Agents that ran: claim-auditor, column-auditor, split-auditor, domain-practitioner, blind-reviewer, precedent-checker, advocate and critic (one opening brief and one rebuttal each), mediator.

**Judgment record**

```text
Verdict: ship after changes.
Validity: SEL holds; USE-1/USE-5 hold (sale price; PI/VB are bids, -4.1% / -6.5% vs +0.3% for sales);
USE-3 triggered, fixed (prediction point reworded to "before the auction, for a property that sells");
LEAK-22 holds (sold cohort, as every sibling); LEAK-10 kept with a `Potential leak, kept on purpose:` note
(Bedroom2 checked against Rooms, the other five scraped attributes and the coordinates not checked against a
pre-sale value); USE-8 approximate recommended (issue 1); SPLIT-1/9/11/14/17 hold; SPLIT-10 not triggered once
reworded; SPLIT-12 horizon wording fixed; PROV-4/6/9/13 hold.
Value: TP holds (LightGBM skill 0.834, beats the dummy on 5 of 5 probed splits, best single feature 0.426).
Quality: CLEAN-11 fix (BuildingArea, 86 rows); CLEAN-21 fix (one Distance per suburb, later table); CLEAN-1 date
note or snap; two suburb lookups filled.
Weighed: source +, size +, real actor +; post-sale scrape -, high missingness -.
For the curator: issue 1, the LEAK-10 exception shown or not (decides note and fit); issue 2, year 2018 vs 2017.
```

**Changes to make now (need no decision)**

1. **Prediction point (USE-3, Must).**
   - What to change: `question`, `use_case`, the first `curation_comments` bullet and `splits_comment` should say "before the auction, for a property that sells". `fit_reason` should name the sold-only cohort.
   - Avoid "refit weekly". The split refits once per window and then predicts three sheets ahead, up to 7 calendar weeks across the January lull. Write that instead.
   - No `time_gap` is needed. The advocate withdrew it, and SPLIT-10 is not triggered once the point is reworded.
2. **Scraped block (LEAK-10; house rule `definitions.md` l.488).**
   - Relabel the bullet `Potential leak, kept on purpose:`.
   - Give the numbers: Bedroom2 equals Rooms in 98.9-100% of rows per test window, against 85.2% for the 3,107 sales of Apr-Sep 2016.
   - Give the scope (wording settled under dispute B).
   - State that missingness is neutral: mean residual -0.007 where the block is missing, +0.002 where present.
   - State the blanking effect: within run-to-run noise, |delta| <= 0.0008 over 3 seeds.
   - Revisit when a dated attribute history becomes available.
3. **Coordinates (column audit problem 1; writing).** In `task_summary.known`, say the coordinates come from the post-sale scrape: 4,760 of the 4,915 rows without the block also lack coordinates. Keep them, because a location does not change.
4. **Rows that cite this dataset before Lennart has decided.**
   - The LEAK-10 Mechanisms row (`leak_checks.md` l.280) cites "melbourne_housing_market kept". The `evidence.md` l.218 row also uses this dataset as its example.
   - Mark the leak_checks.md row provisional until Lennart decides issue 1. The evidence.md row only shows the test, so it may stay.
5. **Refuted claims (EV-1, EV-6, SPLIT-12).**
   - Horizon: "3 sheets, up to 7 calendar weeks across the January lull".
   - "+0.0004" and "-0.0004": "within run-to-run noise (|delta| <= 0.0008 over 3 seeds)".
   - Record: "no known risk" becomes "known risk: post-sale lookup of six attributes, measured small".
6. **BuildingArea (CLEAN-11).**
   - Set to missing: values below 10 m², above 1,000 m², and values exactly equal to Landsize for a house. This is 86 rows (47 + 7 + 32) of 8,285 present values.
   - Replace the note "92 sales of 1-29 m², kept". Note the 10-29 m² "squares" (9.29 m², an Australian unit) question as circumstantial.
7. **Distance (CLEAN-21).** Give each suburb one value, from the later table that every test window uses.
8. **Small repairs (CLEAN-1, Weigh).**
   - Snap the 11 download-day sheet dates (2,034 rows) to their Saturday, or add one line in the notes.
   - Fill the lookups of the "Fawkner Lot" row and the Footscray row from their suburbs.
   - Update the stale REVIEW issue 7: `melbourne_housing_snapshot` already carries `Duplicate`.
   - Cite PROV-9's growing-source clause for the year, not "last updated".
   - Pin the Kaggle version (reproducibility).

**Disputed points**

**A. Is LEAK-22 triggered by dropping passed-in and vendor-bid results?**
- Facts both sides accept:
  - 5,939 PI/VB rows with a price are dropped, about 22% of the 27,247 priced results.
  - PI/VB prices are bids: 4.1% and 6.5% below a sale model.
  - Every sibling (house_sales, perth, zillow, Ames) ships sold rows with "a property sells" as the prediction point.
- Rules:
  - Advocate: USE-5 (Must) requires the sold rows, and LEAK-22 (follow the source's cohort) holds.
  - Critic: under "listed for auction" the cohort includes properties that cannot have a sale price, so LEAK-22 is triggered.
- Settled:
  - The rows are right (USE-5, LEAK-22 hold).
  - The violation is USE-3 (Must): the written prediction point is not the one evaluated.
  - The fix is the same rewording both sides accept, and it is required, not optional. Record it as "USE-3 triggered, fixed", not as LEAK-22.

**B. Are the five other scraped attributes shown unchanged?**
- The facts are not in dispute, only how to state them:
  - Bedroom2 is the only attribute with a pre-sale reference (Rooms).
  - The Sept 2017 snapshot matches FULL on all six attributes for 13,580 of 13,580 rows, including 2,728 test rows up to 23 Sep 2017. So those values were recorded within weeks of the sale and never changed afterwards.
  - 22 of 32 resale pairs differ, so the lookups were made per sale, not one current record per address.
  - Nothing measures Bathroom, Car, Landsize, BuildingArea or YearBuilt against their value before the sale, and nothing covers test rows after 23 Sep 2017.
- Settled on the facts:
  - The note says "Bedroom2 checked against the sheet; all six recorded within weeks of the sale for the test rows up to 23 Sep 2017 (snapshot); the other five not checked against a pre-sale value".
  - The critic's "assumed" understates the evidence; the advocate's "covers all six" overstates it.
  - No cheap experiment exists, because the data holds no pre-sale reference for the five.
- This leaves a question of rules, which is issue 1.

**C. BuildingArea cut threshold.**
- Critic: above 1,000 m². Advocate: above 1,000 m² only where the value also exceeds the lot or is above 200 m² per room.
- **Decisive experiment** (on the cleaned frame, thread caps set): all 7 rows above 1,000 m² meet the advocate's extra condition. Both rules blank the same 86 rows, so the outcome is identical either way.
  - The 7 rows are: 1,022 on a 531 m² lot; 1,041 on 343; a 2-room unit of 1,561; 3,112 on 730; 3,558 on 2,778; 6,791 on 732; 44,515 on 44,500.
- Write the cut so it states its reason (impossible against the lot or the room count) and it covers future rebuilds: the advocate's wording, which narrows the critic's in line with CLEAN-11's "only unusual stays".
- Near-equal BuildingArea and Landsize for a house is not clearly impossible.
  - Within 2%: 84 rows, down to 106 m² on a 108 m² lot. A house filling a small inner-city lot is plausible.
  - So only exact equality is cut.

**D. Fit: `direct` or `approximate`?**
- Not a free weighing call. USE-8 (Must) defines approximate as including "a potential leak kept on purpose". Point 2 of the changes adds exactly that label.
- The closest precedent, house_sales, has the same LEAK-10 mechanism, the same label and a residue measured as noise, and is `approximate`.
- The advocate's distinguishing fact (missingness does not follow the outcome, unlike kick's `WheelType`) separates this case from kick, not from house_sales.
- Recommendation: `approximate`, unless the curator rules that the evidence meets LEAK-10's "the data shows they did not change" (issue 1). In that case the label goes and `direct` follows.
- Aside: bioresponse, cooking_time_1m, delivery_eta_1m, maps_router_eta_1m, qsar_bioconcentration and lung_cancer_epithelial_genexp are `direct` while carrying the label, for LEAK-30 scaling. That is a different mechanism, but it does not follow USE-8's wording. It is worth a separate consistency check, not this dataset's issue.

**Issues for the curator, ranked**

1. **Do the measurements show that the scraped block did not change after the sale? (P4, LEAK-10 Must; USE-8 Must)**
   - Problem: six attributes were looked up after the sale. Only Bedroom2 can be checked against a pre-sale value.
   - Effect: the score barely moves. The question is whether the task is described honestly, and the answer sets the note and the fit.
   - Advocate's best evidence:
     - Bedroom2 equals Rooms in 98.9-100% of rows per test window.
     - The snapshot shows all six recorded within weeks of the sale for 2,728 test rows.
     - Missingness is neutral (-0.007 vs +0.002).
     - Blanking the 495 mismatched 2016 rows changes the score by noise only.
     - The practitioner calls the fit direct.
   - Critic's best evidence:
     - No pre-sale reference exists for five attributes or for test rows after 23 Sep 2017.
     - 2016 training rows agree only 85.2%.
     - house_sales has the same mechanism and is `approximate` with the label.
   - Rule: LEAK-10's exception clause against USE-8's wording.
   - Decision needed:
     - (a) The exception is not fully shown: label it `Potential leak, kept on purpose:` and set fit `approximate`, like house_sales. This is the panel's recommendation.
     - (b) The exception is shown: use a plain evidenced note and fit `direct`. Record what sets this case apart from house_sales.
   - Either way the attributes stay. Nobody argues for dropping them, because the measured effect is noise-level.
2. **Year: 2018 or 2017 (P5, PROV-9, Should).**
   - "2018" follows PROV-9's clause for a growing source: public by Mar 2017, the dansbecker cut ends Sep 2017, FULL ends Mar 2018, LESS ends Oct 2018.
   - The precedent for that clause is sf_permit_time, consumer_complaints_1m and kickstarter. house_sales uses 2015, but it is a fixed file, so it does not apply.
   - Recommendation: keep 2018 with the PROV-9 reason in the code comment. Confirm it.

The other REVIEW issues (which file, sale-price target, the coverage change, windows, the re-dated sheet, repeated reports, licence) are agreed and measured. They need only Lennart's acknowledgement.

**Agreed facts**

- **Size and target:** 21,266 sales from 28 Jan 2016 to 17 Mar 2018; the target is ln(price); the md5s of both raw files match.
- **Signal:**
  - LightGBM RMSE 0.182 with the scraped attributes, 0.200 without them, 0.206 with the LESS columns (worse in 9 of 9 windows).
  - Skill 0.834. Best single feature: Postcode, 0.426.
- **Split:**
  - 9 expanding windows of 3 sheets, with train shares 0.553-0.947.
  - The smallest window has 93 rows. Every test window lies after the coverage change of 27 May 2017.
  - The hidden-group probe has no hits.
  - IID 3x3 scores 0.1851 against 0.1841 shipped.
  - A 28-day gap adds 0.0024 (worse in 8 of 9 windows).
  - Window 2 predicts 5-7 weeks ahead; windows 3 and 8 span 4 calendar weeks.
- **Repairs and duplicates:**
  - The holiday sheet is repaired, 787 of 787 rows.
  - The snapshot is a subset (13,580 of 13,580) and its record already carries `Duplicate`.
- **Coverage before 27 May 2017:** only inner suburbs. Keeping all rows scores 0.182 against 0.185 when training from 27 May.
- **Distance:** the table switches for 140 of 142 suburbs. Harmonising it changes the score by noise only.
- **Address** stays: a resale's earlier sale is legitimate history (LEAK-34), and Address alone scores R² -0.093.
- **Blind reviewer:** include with changes. Its concerns (the Address identifier, the undocumented row filter, implausible values) are covered by the facts above and changes 1 and 6.

**Consistency with precedent**

- **Followed:**
  - house_sales: window layout, resales kept as history, non-market prices dropped, and the LEAK-10 residue kept with a note. Fit `approximate` is recommended to match.
  - perth, zillow, Ames: the sold-only cohort and the prediction point after the rewording.
  - california_house_prices_2020: repair with an asserted count (PROV-13).
  - sf_permit_time and kickstarter: PROV-9 year for a growing source.
  - colleges: an existing duplicate record keeps its name.
- **Departure if the curator picks 1(b):** a fit of `direct` with the residue would depart from house_sales. The fact that sets it apart would have to be recorded: the snapshot shows recording within weeks for 29% of the test rows, which house_sales lacks.
- **No drift, no third exception.** If a third housing dataset needs the "keep the residue when blanking would mark the change" remedy, amend the LEAK-10 Mechanisms row (precedent checker).

</details>

<details><summary>Checklist</summary>

**Checklist: melbourne_housing_market (re-check, 2026-10-20)**

Definition: `datasets/_dev/tabarena-v0pt2/melbourne_housing_market/dataset.py` (unchanged in this run).

Automated: `dataset list` imports the class (temporal_non_iid, checked); `uvx ruff@0.15.15 check` clean, `format --check`
clean; `dataset check`: 0 errors, 0 warnings, 0 info (26 checks); `accepted_check_warnings` empty. README rewritten: the
checksum `v2:6d58d4bd70e971ed80ce86d...` is unchanged; the diff only adds the generator's new fields (`time_gap: null`,
`time_gap_unit: null`) and the `REVIEW.md` row in the file table. `sync-notebooks --check` clean. Raw md5 match the
`download_description` (FULL 06cc5316..., LESS cc467c28...).

Probes (JSON under `probes/`): leak probes (3 splits) all features R² 0.814, depth-2/3 tree 0.102/0.258, best single
feature Postcode 0.366, no drop-one loss above 0.004; exact feature copies across the split 11.0% without string and
date columns, 0.0% with them; Address alone as text -0.093; 1-NN R² 0.714 (closest tenth 0.421). Task probes (5 of 9
splits): LightGBM skill +0.834 (SE 0.014), beats the dummy on 5 of 5, best single feature 0.426 (Postcode), no flags.
Hidden groups (temporal): no hits; Propertycount seen 99.6%, near copies seen 8.6%. Generated-data probes: no marks
(81.3% of column pairs dependent, 0 of 9 uniform). Tuned results: none cached for this dataset (new to BeyondArena).
Group probes: not applicable (temporal task, no grouping).

| Rank | Check | Verdict | Evidence | Rule |
|---|---|---|---|---|
| P1 | Ethics | pass | Public auction results of properties; no persons beyond addresses and agency names; scraped from Domain.com.au and realestate.com.au (an open forum question whether Domain allows it, earlier REVIEW issue 10; not an objection to ML use) | SEL-1 |
| P2 | Scope | pass | Sale-price regression from listing attributes, a valuation decision before an auction; not forecasting of a series | SEL-2 to SEL-15, TP-10 |
| P2, P5 | Real data | pass | Real weekly result sheets; generated-data probes no marks; the simulated-attribute "vitticeps" extraction is a different upload, not used | SEL-16, PROV-3 |
| P3 | Use case and fit | pass | `task_summary` names the actor (buyer or agent), the moment (listing for auction) and the target; fit `direct` with the reason for the scraped attributes | USE-1, USE-2, USE-8, USE-9 |
| P3, P4 | Target and metric | concern | Target log sale price of S/SP/SA results only, no NaN (21,266 rows, 11.63-15.85); PI/VB bids dropped (5,939 rows with a price). RMSE on log price fits. Concern for the panel: dropping PI/VB conditions the target on the auction outcome (a property passed in is not in test), which the use case "a property listed for auction" does not see in advance; earlier REVIEW issue 2 | USE-5, LEAK-22 to LEAK-26, EV-5 |
| P4 | Available at prediction time | concern | `Method` dropped (post-auction). The six scraped attributes were looked up after the sale: `Bedroom2 == Rooms` in 98.9-100% of each test window (measured here: 0.989-1.000), six 2016 rows with a later YearBuilt blanked. Kept by measurement (blanking the 495 mismatching 2016 rows: +0.0004 RMSE); still a post-outcome lookup by construction (King County precedent), earlier REVIEW issue 3 | USE-3, USE-6, LEAK-1, LEAK-2, LEAK-10 to LEAK-12 |
| P4 | Irreversible and all-row leakage | pass | `Propertycount` and `Distance` are suburb-level constants from the uploader, not label-aware; no supervised transform. `Distance` table changes on 27 May 2017 (140 of 142 suburbs), kept with a measured -0.0004 | LEAK-13 to LEAK-15, LEAK-27 to LEAK-31 |
| P4 | Copies across the split | pass | 11.0% of test rows (first split) have an exact feature copy in train once Address and Date are left out, 0.0% with them; the copies are rows with the scraped block missing (Bedroom2/Landsize/BuildingArea/YearBuilt 100% missing; 89 units, 21 houses, 13 townhouses of 123) whose log price differs from the train copy's mean by 0.185 on average (the model's RMSE): natural repeats of few features (reading 3). Repeated reports within 60 days dropped (36 + conflicting); 0.45% of test addresses occur in train (resales, kept as history) | LEAK-16 to LEAK-21, SPLIT-29 |
| P4 | Split regime | pass | Temporal on `Date`, 9 windows of 3 weekly sheets, 93-1,550 test rows, training share 0.553-0.947, each test window strictly after its training rows (measured); all windows after the coverage change of 27 May 2017. Hidden-group probe: no hits; Propertycount seen 99.6% is a suburb feature new rows keep (reading 4, SPLIT-4). Open choice: windows span up to 4 calendar weeks where a sheet is missing (earlier REVIEW issue 5) | SPLIT-1 to SPLIT-31, USE-10, USE-11 |
| P5 | Source | concern | Trail ends at the Kaggle upload by Tony Pino, a scrape of Domain.com.au; no first publication beyond Kaggle exists. `year = "2018"` (last update) against first public 2017 (earlier REVIEW issue 9) | PROV-1, PROV-2, PROV-8 to PROV-12, PROV-16 to PROV-18 |
| P5 | Uniqueness | concern | `melbourne_housing_snapshot` (dansbecker) is a September 2017 subset of the FULL file (earlier REVIEW issue 7: all 13,580 rows match); its record needs the `Duplicate` marker, not decided yet | PROV-4 to PROV-7 |
| P5 | Damage and repair | pass | The copied holiday sheet (787 rows dated 6 Jan 2018) re-dated to 16 Dec 2017 with an asserted count; spelling variants merged | PROV-13 to PROV-15 |
| P6 | Worth benchmarking | pass | Task probes no flags; LightGBM +0.834 skill against the dummy, single feature 0.426; every window has a non-constant target (smallest window 93 rows, 20 Jan - 3 Feb 2018) | TP-1 to TP-10 |
| P7 | Dtypes and cleaning | pass | Suburb, Type, Agent, Postcode, CouncilArea, Regionname categorical; Address string; Date datetime; YearBuilt < 1835 and 0 in BuildingArea/Bathroom/Bedroom2 to missing (YearBuilt min now 1850); Landsize 0 kept (1,420 rows, units); 92 BuildingArea 1-29 m² kept as noted. Missing: BuildingArea 61%, YearBuilt 56%, Landsize 34%, coordinates 22% | CLEAN-1 to CLEAN-24 |
| procedure | Notes match the code | pass | Each `curation_comments` bullet maps to a step in `_clean` or a `_decisions` table; the 92 BuildingArea, 18 January sales, 93-1,550 window sizes and 55-95% training share were re-measured and hold. The RMSE numbers (0.183, 0.211, 0.188, ±0.0004) were not re-run here (claim auditor) | writing.md |
| procedure | Licence and citation | cannot verify | `license = "CC BY-NC-SA 4.0"`; the Kaggle page did not render for WebFetch and the kaggle CLI is not installed, so the licence could not be read this run. Citation names the Kaggle upload (bibtex `pino2018melbourne`) | EV-4, PROV-10 |
| procedure | Reproducibility | pass | The kaggle download commands recreate the two files; md5 of both raw files match the stated checksums. Not pinned to a version (Kaggle datasets are versioned, the version is not named) | |

**Draft issues (rank order, carried from REVIEW_before unless new)**

1. Target conditioned on a sale (PI/VB dropped): the panel should say whether a "listed for auction" use case can
   accept that unsold properties are absent (earlier issue 2; USE-5, LEAK-22).
2. Post-sale lookups of the six scraped attributes kept (earlier issue 3; LEAK-10).
3. Which file (FULL vs LESS) (earlier issue 1).
4. Duplicate record `melbourne_housing_snapshot` (earlier issue 7; PROV-4).
5. Year 2018 vs 2017 (earlier issue 9; PROV-10); licence not re-read this run (EV-7).

</details>
