# perth_house_prices

**Outcome:** added. Ship after changes, which are applied in the definition. A regression of the log sale price of
33,090 Perth house sales scraped in January 2021 from house.speakingsame.com, for an automated valuation model (AVM:
a model that values a property from its record and location, used by lenders and agents) refit each month; nine
one-month test windows, April to December 2020, no gap. Validity: SEL-1 and SEL-2 hold; USE-5 holds (the sale price
is what the valuation acts on); USE-7 applied (the 563 sales dated before the build year are land or off-the-plan
sales, dropped; the 140 sales in the build year stay); USE-8 read as written gives `approximate` (truncated at $2.44M,
attributes as of the scrape, the school rank kept as a weak potential leak), unless the curator amends it (issue 1);
LEAK-26 met (the truncation documented); LEAK-10 triggered on training rows and fixed: the station and its distance
blanked for 147 sales before the station opened, and the school, its distance and its rank for the 58 sales before
Joseph Banks Secondary College opened (the rank belongs to that school, so it goes with the name); for the rooms,
bedrooms or bathrooms differ from a second scrape in only 0.7% of 2007-2016 sales; the other rows keep the rank with
a potential-leak note (ranking year unknown); SPLIT-21 met (the split note gives no score as a reason); SPLIT-10 open (issue 7); SPLIT-20 open (issue
6). Value: no task-probe flag (LightGBM R² 0.860 against 0.767 for a linear model; the task probe re-run on the changed
definition, 5 of the 9 windows; 284-628 sales per window).
Quality: CLEAN-11 impossible floor areas and bathroom counts set to missing; CLEAN-12 `Vic` split into its two
stations, the unit flag open (issue 5). Weighed: use case +, signal +, source (a scrape, truncated, one sale per
property) -, a single test year -.

**Main points:** The fit label follows the house-family USE-8 item (issue 1); a one-month gap or no gap follows
house_prices_nominal's issue 4 (issue 7); spaced monthly windows (`step=3`) or contiguous 2020 windows with a recorded
exception (issue 6); the training history from 1988 or from 2013 (issue 3); a `UNIT` flag from `ADDRESS` (issue 5).

**Record judgment:** valid with concerns. A real scrape of a property site (OpenML 43822 is the same table); each
property appears once with its latest sale, and the dearer sales are absent.

**Issues for Lennart:**

1. **The fit label: `approximate` under USE-8 as written, or `direct` if the house family amends it?**
   - Problem: the definition ships `fit="approximate"` with three named gaps: the data is truncated at $2,440,000
     (one sale at that price, none above, though the site lists dearer sales), the house attributes are the site's
     record of January 2021 rather than at the sale, and `NEAREST_SCH_RANK` stays with a `Potential leak, kept on
     purpose:` note (one ranking of 2019 or later, its year unknown). USE-8 (Must) lists "a potential leak kept on
     purpose" under an approximate fit, as for kick.
   - Effect: a one-word label; the rows, the split and the target do not change. The truncation removes about 1.5% of
     houses sold in 2015-2020 (75 of 5,072 in heptix/perth-property-prices, a second Kaggle upload of Perth sold
     listings, 2006-2024, used here only as a check), and 45 of the 4,132 test rows are in the suburbs the cut
     reaches. Dropping the rank changes
     mean RMSE from 0.1622 to 0.1623 (LightGBM, one seed, 9 windows).
   - For `approximate` (critic): USE-8 is a Must and rules win over precedents; house_sales, houses and zillow_prize
     read `approximate` for the same kinds of gap, and houses names its cap in `fit_reason`.
   - For `direct` (advocate, domain practitioner): the truncation and the stale records are not on USE-8's list of
     approximate patterns; they narrow the population or remove inputs, they do not make the task a stand-in. Drop
     the rank (no measurable cost) and no kept leak remains.
   - Implemented: `approximate` (mediator: the rule as written). The decision itself belongs to the working copy's
     items "Does a weak potential leak kept on purpose make a fit `approximate`?" and "The fit label of the
     house-price datasets with values kept from after the sale", which list perth; the truncation and the stale
     records fall outside even that item's amendment (b), so an amendment would have to name them.
   - Decision needed: if the family item keeps USE-8, perth stays `approximate` and this issue closes with it. If it
     amends USE-8 by option (b), decide here whether the amendment also names a documented truncation and attributes
     as of a later scrape: yes, perth goes `direct` with `NEAREST_SCH_RANK` dropped; no, perth stays `approximate`.

7. **A one-month gap, or no gap as the second exception to SPLIT-10?**
   - Problem: sales reach the site late. December 2020 holds 0.71 of November's count against 0.83-1.04 in
     2013-2019, and the file, scraped on 31 January 2021, has no January 2021 sale. SPLIT-10 (P4, Should) asks for a
     gap when the newest rows are recorded late.
   - Effect: no gap is mildly optimistic, since a refit at the start of a month sees less of the previous month than
     the scrape saw. The source dates sales by month only, so the smallest gap drops the whole previous month, more
     than the real delay of days (an archived Mount Lawley page of 14 April 2021 lists four April 2021 sales among its
     10 newest).
   - For the exception (advocate and critic agree): December's mean residual (actual minus predicted log price,
     LightGBM; positive means under-predicted) is +0.015 to +0.017, within July-November's +0.003 to +0.025, so the
     December sales that reached the site early are not priced differently; the same mechanism test as
     house_prices_nominal.
   - For `gap=1`: zillow_prize takes one month at the same resolution; house_sales takes a one-week gap for its
     recording delay. house_prices_nominal is the only sibling without a gap.
   - Implemented: no gap. The split note gives no score as a reason (SPLIT-21, Must). The split audit's draft
     exception: `**Exception to SPLIT-10 (<date>, Lennart):** the month resolution allows no gap shorter than the
     whole previous month, and the newest month present early (December 2020, 0.71 of November) shows no price
     selection (mean residual +0.017 against +0.003 to +0.025 in July-November); serves P4.` A third case would make
     an amendment of SPLIT-10 due.
   - Decision needed: decide house_prices_nominal's issue 4 (the working copy's item "One form of the recording-delay
     gap (SPLIT-10) for the house-price datasets"), and perth takes the same answer.

6. **Where the nine monthly windows fall: contiguous in 2020, or spaced every three months?**
   - Problem: all nine windows are April-December 2020. April and May are COVID months (316 and 284 sales against
     421 and 440 in 2019), and 2020 is in the stale-record regime: bedrooms or bathrooms differ from the sold listings
     of heptix in 27.0% of the shared 2020 sales (0.7% in 2007-2016, 12.1% in 2019), mostly with fewer rooms in the
     file. SPLIT-20 (P4, Should) asks that most windows fall outside an atypical season.
   - Effect: the benchmark measures one market year. In 2020 the record is older than the sale, so the stale values
     are noise, not a leak.
   - Option (a), `step=3` (the mediator's lean; no exception needed): `TemporalSplits(window=1, unit="months",
     n_windows=9, step=3)`, where `step` is how far each window moves back. It keeps one-month windows and the
     monthly refit but samples every third month: December, September, June and March of 2020, December, September,
     June and March of 2019, and December 2018. 367-569 test sales per window, train share 0.667-0.988 (SPLIT-14
     holds); 5 of 9 windows before COVID and 2-3 before the mid-2019 rise of stale records. rain_in_australia spaces
     its windows the same way (`step=42`) to cover seasons. Cost: older windows bring back attributes dated after
     the sale into test rows (2.8% differ in 2017-2018) and survivor-thinned suburbs (11 of 321 have no rows yet by
     December 2018). Only counts were computed, no scores.
   - Option (b), contiguous 2020 windows (implemented) with a recorded `**Exception to SPLIT-20**` that rests on the
     use case (P3) and on no test row carrying a post-sale value, with the COVID and stale-record numbers. The critic
     holds that SPLIT-12 (the monthly cadence) has the same rank (P4) as SPLIT-20 and is no higher principle, so it
     cannot carry the exception alone.
   - Option (c), wider windows: 9 x 2 months from July 2019 (658-1,197 sales, train share from 76%) or 9 x 3 months
     from October 2018 (974-1,619, from 64%); the advocate objects that they score a refit cadence the use case does
     not run.
   - Decision needed: (a), (b) or (c), chosen without scores (SPLIT-21) and together with the working copy's item
     "One window length for the house-price datasets", where the `step=3` option is listed.

3. **The training history: all sales from 1988, or from 2013 on?**
   - Problem: each property appears once, with its latest sale, and each suburb holds only its newest sales (1-231
     rows, mean 103; busy suburbs start in 2018-2020). The years before 2013 hold 2,263 sales, mostly of quiet suburbs
     and of houses not resold since, with attributes as of the scrape. Baldivis's first sales are in May 2020, so its
     11 sales in the May window have no training rows.
   - Effect: the test rows (all 2020) do not change; only what a model learns from does. The pre-2013 rows are
     survivor-biased (only houses not resold since appear) and carry attributes as of the scrape, but they are the
     history a monthly refit would have, with no break in how the data was collected.
   - Implemented: keep all rows (SPLIT-20, Should). Alternative: keep sales from 2013 on (the blind reviewer's
     change), with a use-case reason. A score comparison is no reason either way (SPLIT-21).
   - Decision needed: keep all, or cut at 2013 with the reason.

5. **Add a `UNIT` flag derived from `ADDRESS`?**
   - Problem: the property type (house or unit), the first input a valuer uses, survives only as the "/" of a unit
     number in `ADDRESS` (1,060 unit rows, median price $404,000 against $540,000 for plain street numbers).
   - Effect: a model that reads `ADDRESS` as text may or may not recover the type; a flag states it.
   - Implemented: `ADDRESS` kept as text, as melbourne_housing_market and california_house_prices_2020. Alternative:
     add `UNIT` and keep `ADDRESS` (the mediator's lean), a new CLEAN-12 Cases row, since no case covers a flag
     derived from free text. Rule: CLEAN-12 (P7, Should) calls rebuilding destroyed meaning "always welcome" (critic).
     Neither the flag's score gain nor how one model's text encoding treats the "/" is a reason (SPLIT-21,
     CLEAN-22, EV-4).
   - Decision needed: add `UNIT` and keep `ADDRESS`, or keep the text only.

**Review panel:** ship after changes (mediator). The panel's numbers are on the definition before this review's
changes, which applied the mediator's changes 1-12 (the fit label, the station and school blanking, the impossible
values, the `Vic` split, the notes), and one step beyond them: for the 58 Joseph Banks rows `NEAREST_SCH_RANK` is
blanked too, because the rank of a school that had not opened is the same anachronism as its name (the mediator
blanked only the name and the distance). The mediator's issues 1, 2, 3, 4 and 5 are issues 1, 7, 6, 3 and 5 here;
"REVIEW issue N" in the other reports is the numbering of this file before the run, where issues 2 (stale records),
4 (the build-year drop), 8 (December 2020) and 9 (implausible values) were settled into these issues or the changes.
Claim audit: 67 claims; four refuted or partly refuted, all fixed (the house_sales gap citation, the 0.23 log-unit
figure, the Baldivis and duplicate-pair wording); three untested (judgment calls, Kaggle versioning). Blind review: include with changes; main concern the thin, survivor-biased early
years. Debate: agreed on shipping, on every cleaning and leak fix, on the USE-7 drop of the 563 sales and on no gap as a
recorded exception (issue 7, pending house_prices_nominal); disputed: the fit label (issue 1), the window
placement (issue 6) and the unit flag (issue 5).

<details><summary>Claim audit</summary>

**perth_house_prices: claim audit (2026-10-20, full tier re-check)**

Scripts and outputs: (panel run) (basic.py, dups.py, dups2.py, heptix.py, models.py, misc.py). Data: the
definition's frame and split plan via `dataset_io.from_definition` (33,090 rows, 9 splits); raw file sha256 checked;
heptix match done independently (address + suburb + sale month, 1,856 shared rows; prices equal in 98.4%).
LightGBM: 500 trees, lr 0.05, 63 leaves, ADDRESS dropped, DATE_SOLD as days, native categoricals, 2 threads.
Licence and pretraining overlap are not evidence and were not weighed.

**Table**

| # | claim | source | test | result | evidence | rule |
|---|---|---|---|---|---|---|
| 1-2 | monthly refit valuation task | TS | prediction point vs columns and split | holds | every feature is a listing/location attribute; windows are calendar months trained on all earlier months | LEAK-1, SPLIT-4 |
| 3,15,50,53 | 33,656 rows, 19 cols, 321 suburbs, Apr 1988-Dec 2020, sha256, speakingsame | TS, CC, DL, META | recompute | holds | 33,656 x 19; 321; 1988-04..2020-12; sha256 matches | PROV |
| 4,20,58 | each property once (latest sale) | TS, CC, REC | address+suburb repeats in curated frame | holds | 0 repeated address+suburb; 172 rows share an address string but in different suburbs | LEAK-30 |
| 5 | 33,090 sales | TS | row count | holds | 33,090 | - |
| 6,19 | target ln(PRICE) | TS, CC | code + values | holds | log_PRICE = ln(PRICE) | - |
| 7,22,44,59 | cap at $2.44M; site lists dearer (McNeil St $5.2M Jun 2013); 1.5% of 2015-20 houses above in heptix | TS, CC, DEC, REC | max price; archived page; heptix | holds | raw max 2,440,000, 0 above; wb/other_14.html "Sold $5,200,000 in Jun 2013"; heptix 75/5,072 = 1.48% | LEAK-26 |
| 8,12 | all features known at sale | TS | column by column; leak probe | holds (with staleness caveat) | no post-sale column; exact copies across split 0.0%; missing indicators R2 <= 0.01; probe flags none | LEAK-1 |
| 9,17,37,39 | 9 monthly windows Apr-Dec 2020, train on all earlier, 88-99%, 284-628 rows | TS, CC, SC | split plan | holds | windows 316,284,374,487,483,569,628,579,412; train share 87.5-98.8%; train max = previous month | SPLIT-4 |
| 10,23,45a | 563 pre-build sales dropped, sold 1988-2016, 1-23 years before build, all training rows | TS, CC, DEC | recompute | holds | 563; 1988-2016; gap 1-23 | CLEAN-22 |
| 45b | cross-fitted LightGBM prices them 0.23 log too high | DEC | 5-fold cross-fit on raw | partly: direction holds, number not reproducible | +0.53 with them out of training, +0.11 with them in; 0.23 sits between and depends on the setup | EV-1 |
| 11,13 | fit direct; each month predicted from earlier sales only | TS | split plan | holds | train max date < test month in all 9 | SPLIT-9 |
| 14,29,60 | test-period records stale: 27.0% differ in 2020, 0.7% in 2007-16; 23% fewer | TS, CC, REC | independent heptix match | holds | 2020: 27.0% differ, 23.0% fewer (448 rows); 2007-16 0.7%; 2017-18 2.7%; 2019 12.0%; GARAGE missing 4-5% in 2015-18, 14.1% in 2020 | LEAK-1 (noise, not leak) |
| 16 | prediction point | CC | as 1-2 | holds | - | LEAK-1 |
| 18 | DATE_SOLD "09-2018\r" parsed to month start | CC | raw tokens | holds | values like "10-2020\r"; parsed dates are month starts | - |
| 21,46 | suburbs keep only newest sales; busy ones start 2018-20 | CC, DEC | first sale per suburb; rows per suburb | holds | Butler 2018-09, Ellenbrook 2019-07, Baldivis 2020-05; rows per suburb 1-231, mean 103 | SEL |
| 24,31 | attributes are the record at scrape; affects training rows only (school/station) | CC | - | holds for school/station (scrape is 1-10 months after test sales); the stale bed/bath record also hits test rows (claim 14) | - | LEAK-1 |
| 25 | 3 coordinate copies dropped; two pairs "differ only in the address" stay | CC | duplicated() on subsets | refuted (wording, minor) | 3 dropped holds; 0 rows are identical except ADDRESS; the two pairs (1/11 Gaffin Way; 2/5 207 Manning Rd) also differ in LONGITUDE/LATITUDE and NEAREST_SCH_DIST | EV-6 |
| 26 | only "NULL"/empty mean missing; 999999 and 99 proxies | CC | non-numeric tokens per column | holds | tokens: GARAGE NULL 2,478, BUILD_YEAR NULL 3,155, SCH_RANK empty 10,952; LAND 999999 x3, GARAGE 99 x1 | CLEAN |
| 27 | other scrape errors stay, up to 50 car spaces | CC | max | holds | GARAGE max 50 (7 rows > 20) | - |
| 28 | no build year after 2017; 9.5% missing | CC | max, share | holds | max 2017; 9.53% | - |
| 30 | SCH_RANK missing for unranked schools | CC | missingness per school | holds | 0 of 160 schools mixed; OpenML description says the same | - |
| 32,48,65a | ADDRESS as text; 1,060 unit rows (median $404k vs $540k), 2,615 lettered | CC, DEC, REVIEW | regex counts | holds | 1,060 / $404,000 / $540,000; 2,615 | CLEAN-12 |
| 65b | UNIT flag lowers mean RMSE 0.161 -> 0.158 (7 of 9) | REVIEW 5 | LightGBM with/without flag | holds (stronger) | 0.1622 -> 0.1592, better in 9 of 9 | CLEAN-12 |
| 33 | four categoricals | CC | dtypes | holds | SUBURB, POSTCODE, NEAREST_STN, NEAREST_SCH category | - |
| 34 | 52 sales since 2012 < $120k | CC | count | holds | 52 | - |
| 35,41 | Dec 2020 0.71 of Nov vs 0.83-1.04 in 2013-19; ~80% of usual share | CC, SC | counts | holds | 0.71; 0.83-1.04; 0.71/0.92 = 0.77 | SPLIT-10 |
| 38 | dated by month only | SC | raw | holds | "MM-YYYY" only | - |
| 40 | Mount Lawley page of 14 Apr 2021 lists four Apr 2021 sales | SC | archived page + CDX | holds | CDX 20210414170123; page lists 4 "in Apr 2021" among first sold entries | SPLIT-10 |
| 42 | 1-month gap raises mean RMSE 0.159 -> 0.162 | SC | LightGBM, train drops last month | holds (direction, size) | 0.1622 -> 0.1643 (+0.002) | SPLIT-4 |
| 43 | horizon warning is an artefact of month-start dates | AW | split plan | holds | each test window holds one date | - |
| 47,67 | Dec prices vs suburb median in line (+0.048 / +0.027 / +0.023) | DEC, REVIEW 8 | rel. to suburb median | holds in direction; numbers not reproduced (method-dependent) | all-period median: Oct +0.010, Nov +0.014, Dec +0.037; 2020 median: +0.006/+0.012/+0.029; Dec not lower | EV-1 |
| 49 | year, domain, tags | META | - | untested (judgment) | - | - |
| 51 | one Kaggle version, not served by number | DL | - | untested (no Kaggle call made) | - | PROV |
| 52 | OpenML 43822 same table | DL | OpenML API qualities | holds | 33,656 instances; 16,585 missing = 2,478+3,155+10,952 exactly | PROV |
| 54 | regression, temporal | REC | task metadata | holds | - | SPLIT-3 |
| 55-57 | real site; G-NAF coordinates, bettereducation ranks | REC | archive pages; OpenML description | holds | archive pages exist; description names data.gov.au and bettereducation | PROV |
| 61 | LightGBM R2 0.86, no probe flags | REC | all 9 windows | holds | mean R2 0.872 (probe 0.861 on 5 splits); flags [] | TP |
| 62 | priority 1 etc. | REC | - | untested (judgment) | - | - |
| 63 | shared test rows: RMSE 0.138 file vs 0.126 listing; differing 0.154 vs 0.123; under-predict 0.045 | REVIEW 2 | LightGBM, swap in heptix bed/bath | holds in direction, smaller gap | 351 rows: 0.142 vs 0.136; 91 differing: 0.157 vs 0.134; mean residual -0.036 | EV-1 |
| 64 | pre-2013 2,263 sales; Baldivis has no training rows for the April window; 2013+ gives 0.1612 -> 0.1607 | REVIEW 3 | counts; LightGBM | 2,263 holds; RMSE holds (0.1622 -> 0.1615); Baldivis refuted as worded | Baldivis has 0 test rows in April too (first sale May 2020); the May window has 11 Baldivis test rows and 0 training rows | EV-6 |
| 66 | no gap "as house_sales and house_prices_nominal" | REVIEW 7 | sibling definitions | refuted | house_sales now has `gap=1` (one week, recording delay); only house_prices_nominal has none | SPLIT-4/SPLIT-10 (precedent) |

**Implied claims**

* Every feature known at the prediction point: holds; no post-sale column. Caveat: in 2019-2020 the bed/bath/garage
  record is often older than the sale (stale, so noise not leak); GARAGE missingness triples in 2020 (14.1%), a test
  period shift.
* No copy across the split: holds (exact copies 0.0%, address+suburb unique, near-copy clusters 2.7% of test rows
  seen in train at 0.85 similarity).
* The split matches the use case: holds; the late-label question (December 2020 at ~77% a month later) is a
  weighing call, gap costs +0.002 RMSE.
* The target is the real-world target: partly; it is the price of a sale up to $2.44M (documented, LEAK-26).

**Refuted and untested, ranked**

1. Claim 66 (REVIEW issue 7, precedent): house_sales has a one-week gap now. Changes the precedent argument for "no
   gap", not the split. Remedy: reword issue 7 ("as house_prices_nominal; house_sales takes a one-week recording
   gap"), keep the question for the curator.
2. Claim 45b (0.23 log units): direction holds, number depends on whether the rows are in training (0.11-0.53).
   Remedy: state the setup or say "priced too high on average (0.1-0.5 log units by setup)".
3. Claim 64 (Baldivis): reword to "Baldivis's 11 May 2020 sales have no training rows".
4. Claim 25: reword to "two pairs that differ in the address and its coordinates stay".
5. Claims 63, 67: directions hold, numbers are setup-specific; cite as approximate.
6. Untested: 49, 62 (judgment), 51 (Kaggle versioning, no API call).

</details>

<details><summary>Column audit</summary>

**perth_house_prices: column audit (re-check, full tier, 2026-10-20)**

Prediction point (first `curation_comments` bullet, `task_summary`): a house sells in month m; a valuation model refit
at the start of m on all earlier sales prices it from the listing, the address and the location. Frame: the
definition rebuilt through `dataset_io.load(..., built=False)` (33,090 rows, 19 columns; 4,132 test rows, Apr-Dec
2020). Codebook: the Kaggle data card (syuzai/perth-house-prices) and the definition's notes; the scrape is of
house.speakingsame.com in January 2021, with G-NAF coordinates and bettereducation school ranks added by the uploader.
Scripts and the cached frame: (panel run) (`load.py`, `stations.py`). LightGBM numbers: 400 trees, lr 0.05, 63
leaves, one seed, the 9 shipped windows, ADDRESS left out; shipped mean RMSE 0.1622.

**Column table**

| Column | Meaning | Known at prediction? | Dtype and cleaning | Verdict | Rule |
|---|---|---|---|---|---|
| `log_PRICE` (target) | ln of the sale price, AUD | target | float64; ln(PRICE), no missing; min $51k, max exactly $2,440,000 | fine, documented truncation: only 1 row sits at $2,440,000 and the five next values are distinct ($2.425-2.437M), so the dearer sales were removed (truncation), not set to the cap; in train and test alike | LEAK-26 (documented), CLEAN-16 |
| `DATE_SOLD` | sale month ("09-2018") | yes | datetime, first of month (no day in source); CR stripped | fine; time column and feature. Each property's latest sale only (selection on "not resold since", training rows only; REVIEW issue 3) | CLEAN-14, SPLIT |
| `ADDRESS` | street address, unit numbers and lettered lots | yes | string, 33,004 distinct; 0.24% of test values in train | fine as kept; CLEAN-12 unit flag open (REVIEW issue 5) | CLEAN-3, CLEAN-12 |
| `SUBURB` | suburb (321) | yes | category | fine (alone R^2 0.615; location, not a leak) | CLEAN-14 |
| `POSTCODE` | postcode (114) | yes | category | fine | CLEAN-14 |
| `LATITUDE`, `LONGITUDE` | G-NAF geocode of the address | yes (static) | float64 | fine; 3 multi-geocode copies dropped | LEAK-21 |
| `CBD_DIST` | distance to Perth CBD, metres | yes (static) | int64 | fine | |
| `BEDROOMS` | bedrooms, site record at scrape | train rows: no (record of Jan 2021); test rows: record often older than the sale (REVIEW issue 2) | int64, 1-10 | fine with the existing note (stale direction: noise, not a leak) | LEAK-10 / LEAK-11 note |
| `BATHROOMS` | bathrooms, same record | as BEDROOMS | int64, 1-16 | cleaning problem: 16 bathrooms in a 95 m2 four-bedroom house, 7 bathrooms with 1 bedroom: impossible, should be missing | CLEAN-11 |
| `GARAGE` | car spaces, same record | as BEDROOMS | float64; 99 -> NaN done; no 0 in the data (min 1), 6.9% missing; 75 rows above 10 (max 50) | fine; question: NaN may mean "no garage" as well as unknown (also the stale-record marker); 13-50 spaces are strata-complex totals, unusual not impossible, keep | CLEAN-10, CLEAN-11 |
| `LAND_AREA` | land m2, same record | as BEDROOMS | float64; 999999 -> NaN (3 rows); 1,811 rows > 1 ha, 66 > 10 ha (strata whole-complex areas, rural lots) | fine (unusual, not impossible; noted) | CLEAN-10, CLEAN-11 |
| `FLOOR_AREA` | internal floor m2, same record | as BEDROOMS | int64, 1-870 | cleaning problem: 19 houses with 2+ bedrooms at 1-40 m2 (one at 1 m2): impossible, should be missing | CLEAN-11 |
| `BUILD_YEAR` | year built, same record; none after 2017 | yes where <= sale year (563 later-built dropped); the record can describe a rebuild | float64, 9.5% missing | fine with note. Missingness is flat by sale year (7.7-12.3%), so not caused by post-sale rebuilds; 140 rows built in the sale year stay (REVIEW issue 4); no remodel year exists, so a renovation after the sale is invisible (the cross-dataset LEAK-10 build/remodel item: nothing more to remove) | LEAK-10 |
| `NEAREST_STN` | nearest train station at scrape | train rows: no for 147 rows (0.44%, 1988-2014) whose station had not opened (Mandurah line Dec 2007: Canning Bridge 36, Kwinana 35, Murdoch 28, Wellard 13 ...; Clarkson 2004: 11; Butler Sep 2014: 11); test rows: yes | category, 68 | leak (weak, training rows only) plus cleaning problem: `Vic` merges Victoria Street (Mosman Park, 98 rows) and Victoria Park (198 rows), 14 km apart, mean log price 14.13 against 13.46, 33 test rows; `Madding`, `Shen`, `Canning` are truncated names of single stations (Maddington, Shenton Park, Cannington) | LEAK-10; CLEAN-12 |
| `NEAREST_STN_DIST` | distance to that station, metres | as NEAREST_STN | int64 | leak (weak, train only), as NEAREST_STN | LEAK-10 |
| `NEAREST_SCH` | nearest secondary school at scrape | train rows: no for sales before the school opened (Joseph Banks Secondary College opened 2015; 58 sales of 1990-2014 name it) | category, 160 | leak (weak, train only) | LEAK-10 |
| `NEAREST_SCH_DIST` | distance to it, km (other distances are metres; one unit per column) | as NEAREST_SCH | float64 | fine dtype; same timing as NEAREST_SCH | CLEAN-21 |
| `NEAREST_SCH_RANK` | bettereducation rank of that school; NaN = unranked (32%) | one rank per school (0 of 160 schools have two), so a single snapshot; Joseph Banks (opened 2015, first Year 12 about 2019) is ranked, so the ranking is from 2019 or later: after nearly every training sale; for the test rows, possibly a ranking published after the sale (2020 ATAR results, late Dec 2020) | float64 | question for the curator (weak; dropping it: 0.1623 against 0.1622) | LEAK-10, USE-3 |

**Problems, ranked (principles.md)**

1. **P3/P4, LEAK-10 (Must) and USE-8: the location attributes are the scrape's, not the sale's, for training rows; the
   fit claim says otherwise.** Evidence: 147 training sales (0.44%) name a station that had not opened; 58 name a school
   that had not opened; school ranks are one 2019+ snapshot; house attributes are the January 2021 record (REVIEW issue
   2). No test window is affected beyond months, and the effect is noise-level: blanking `NEAREST_STN` and
   `NEAREST_STN_DIST` for the 147 rows gives mean RMSE 0.1615 against 0.1622 (one seed). This is not a test-score leak,
   but `fit_reason` ("Everything the model sees is known when a house sells") and `known` are wrong as written, and
   LEAK-10's "unless the data shows they did not change" fails for these rows. Mildest remedy: blank the two station
   columns for sales before the station opened (22 opening dates; zillow_prize precedent, cross-dataset item option (a)),
   rewrite `fit_reason`, and decide the fit label with the house-family USE-8 item (as written: `approximate`). Schools
   and ranks: keep with a `Potential leak, kept on purpose:` note, since no opening list is in hand.
2. **P4, LEAK-10 (question): `NEAREST_SCH_RANK` year unknown.** If the uploader took bettereducation's ranking of
   January 2021, it rests on 2020 results released after every test sale. Effect nil (0.1623 without it). Ask: keep
   with a note naming the ranking year as unknown, or drop it (costs nothing).
3. **P4, LEAK-26 (Must, met): the target is truncated, not capped.** One row at $2,440,000; rows above were removed in
   train and test alike. Documented; suggest the notes say "truncated at $2.44M (dearer sales absent)" rather than
   "capped", since no value was set to the ceiling. Fit question stays REVIEW issue 1.
4. **P7, CLEAN-12 (Should): `Vic` merges two stations.** Victoria Street (Mosman Park, west of 115.8 E) and Victoria
   Park, 14 km apart, 0.67 log units apart in mean price, 33 test rows. Remedy: split the label by longitude into the
   two station names; optionally write out `Madding`, `Shen`, `Canning` (cosmetic).
5. **P7, CLEAN-11 (Should): impossible values kept.** 19 houses with 2+ bedrooms at 1-40 m2 of floor area; bathrooms 16
   (95 m2) and 7 (one bedroom). The note's reason ("nothing marks them missing") is not a CLEAN-11 reason. Remedy: set
   these to missing, row kept (RMSE 0.1624 against 0.1622, neutral). Garage 13-50 and strata land areas stay as
   unusual.
6. **P7, CLEAN-10 (question): `GARAGE` has no zero.** Missing may mean "no garage"; keep as missing (safe), say so in
   the notes.

Everything else holds: no identifier encodes the label, no feature is computed over all rows (LEAK-29), proxies
999999 and 99 converted, dtypes by meaning (CLEAN-14), `BUILD_YEAR` missingness not outcome-driven, the 563 pre-build
drops are training rows.

</details>

<details><summary>Split audit</summary>

**perth_house_prices: split audit (re-check, 2026-10-20)**

Scripts and outputs: (panel run) (windows from `dataset_io.from_definition`), (panel run)
and (panel run) (500-tree LightGBM, ADDRESS replaced by a unit flag, 3 seeds, 9 shipped windows).

**Verdict: right with notes**

Temporal on `DATE_SOLD`, 9 x 1 calendar month (Apr-Dec 2020), expanding train side, no gap. The regime matches the use
case (a valuation model refit monthly predicts this month's sales; SPLIT-1, SPLIT-6). Every count rule holds. The one
open point is the gap (SPLIT-10, Should), which waits on the same curator decision as house_prices_nominal issue 4.

**Facts checked**

| Check | Result | Rule |
|---|---|---|
| Regime against use case | Sale price of a sale this month from earlier sales: temporal (SPLIT-6). Each property appears once (0 duplicated ADDRESS+SUBURB rows), so no repeat sale crosses the cutoff; SUBURB recurs (99.6% of test rows seen) but new sales keep it, a feature (SPLIT-4, SPLIT-13). | SPLIT-1, SPLIT-4, SPLIT-6, SPLIT-13 |
| Time column | Sale month, parsed to its first day; data 1988-04 to 2020-12, no 2021 row. | SPLIT-2 |
| Windows | 9 windows, 284-628 test rows (Apr 316, May 284, Jun 374, Jul 487, Aug 483, Sep 569, Oct 628, Nov 579, Dec 412); train share 0.875-0.988; train always ends the month before the test month. | SPLIT-11, SPLIT-14, SPLIT-15, SPLIT-17 |
| Horizon | Monthly refit, as zillow_prize; the source dates by month only, so one month is also the finest window. | SPLIT-12 |
| IID comparison | Random 3-fold (3 seeds), scored on the Apr-Dec 2020 rows: RMSE 0.155 against 0.160 temporal; the temporal split is the honest one and costs about 0.005. | SPLIT-1, SPLIT-5 |
| Training history | All of 1988-2020; years before 2013 hold 2,263 rows, growing to 5,000+ per year from 2017 (latest sale per property, newest sales per suburb). 2.6% of test rows are in suburbs first seen in 2020; 3.0% in suburbs with fewer than 20 training rows before April 2020. Not a split fault (survivor sampling, REVIEW issue 3). | SPLIT-20, SPLIT-21 |

**Problems, ranked**

1. **P4, SPLIT-10 (Should): no gap although sales reach the site late. Note; the decision carries from
   house_prices_nominal.**
   - Evidence: the scrape is dated 31 January 2021 but the file holds no January 2021 sale, and December 2020 holds
     412 sales (Dec/Nov 0.71 against 0.83-1.04 in 2013-2019). A refit at the start of a month, at 0 days after the
     previous month ends, would see less of that month than the scrape saw of December after a full month. The
     shipped split trains on the whole previous month, so it is mildly optimistic.
   - Size (500-tree LightGBM, 3 seeds, mean of 9 windows): no gap 0.1596, previous month at a random 50% 0.1602, at
     25% 0.1612, one-month gap 0.1622 (+0.0025, SE about 0.0015; the gap is worse in 6 of 9 windows, by up to 0.013
     in June). Mean residual +0.009 with no gap, +0.014 with the gap: in a rising late-2020 market a gap adds
     under-prediction.
   - Mechanism (what SPLIT-10 guards against): December's residual +0.017 lies within the +0.003 to +0.025 of July to
     November, so the sales present early show no price selection; December is test-only, never trained on.
   - The month resolution has no gap shorter than one month, which removes the previous month entirely, more than
     the real delay (days to weeks); the truth lies between the two splits.
   - Wrong citation: REVIEW issue 7 says "no gap, as house_sales and house_prices_nominal"; house_sales now has a
     one-week gap. The splits_comment itself does not cite them.
   - Mildest remedy: follow the curator's answer on house_prices_nominal issue 4. If (b), write the exception with
     this dataset's fact: `**Exception to SPLIT-10 (2026-10-20, Lennart):** the month resolution allows no gap
     shorter than the whole previous month, and the newest month present early (December 2020, 0.71 of November)
     shows no price selection (mean residual +0.017 against +0.003 to +0.025 in July-November); serves P4.` If (a),
     `TemporalSplits(..., gap=1)` (train 86.3-97.0%). Either way, drop the house_sales citation from REVIEW issue 7.

2. **P4, SPLIT-20 (Should): all nine windows fall in 2020, a COVID year and the stale-record regime. Note.**
   - Evidence: April-May 2020 hold 316 and 284 sales against 421 and 440 in 2019 (lockdown); the mean residual moves
     from -0.014 (April) to +0.017 to +0.025 (July-December), a market turning up; REVIEW issue 2 has the house
     records stale in 27% of 2020 sales. The windows cover nine months of one atypical year.
   - Rule: SPLIT-20 asks to check for an atypical season and widen the windows so most are not in it. Wider windows
     (9 x 2 months from July 2019, or 9 x 3 months from October 2018, REVIEW issue 6) would put half or more before
     COVID, but leave the monthly cadence of the use case (SPLIT-12). Do not choose between them from their scores
     (SPLIT-21).
   - Mildest remedy: keep the monthly windows and state in the splits_comment that the test year is 2020 (COVID,
     rising late-2020 prices); the curator's call between REVIEW issue 6's options stands.

3. **Procedure: the splits_comment says "88-99% of the rows"; measured 87.5-98.8%.** Rounds to 88-99; fine.

No SPLIT-9 problem (a sale's price is known at the sale), no hidden group (SPLIT-29 does not apply to a temporal task;
near copies 2.7%), no repeat sales across the split.

</details>

<details><summary>Domain practitioner</summary>

**perth_house_prices: domain practitioner (2026-10-20, re-check, full tier)**

Actor: I run an automated valuation model (AVM) for Perth residential property, for a lender's loan
check or an agent's appraisal. Today in Australia this is a vendor AVM (CoreLogic IntelliVal, PropTrack,
Hometrack, Valocity, Domain). It values a property from its attributes, its sales history and the comparable
sales nearby in place and time, and attaches a confidence score. The model is refit or recalibrated often,
and accuracy is reported as the share of estimates within 10% / 20% of the sale price, by price band.

**Fit: direct (narrowly), not approximate**

One row is one sale = one valuation I make. The target is the sale price, which is what I act on (USE-5).
The split refits on all earlier sales and predicts the next month (USE-3, USE-10: an AVM back-test on
subsequent sales). None of the USE-8 "approximate" patterns applies (no snapshot standing in for a
forecast, no leak kept on purpose, no reconstructed time axis, no label without a horizon). The gaps
below narrow the population or remove inputs; they do not turn the task into a stand-in for another
one. So `fit="direct"` holds, but `fit_reason` should name the missing property type and sales history.

**1. Inputs at the prediction point**

I would have, and the data has: suburb, postcode, address, coordinates, beds, baths, car spaces, land
and floor area, build year, distances to the CBD, station and school, and the month. All are known
before the sale (USE-3, USE-6).

Stale test-period records (REVIEW issue 2): for an AVM this is realistic, not a defect. My AVM also
works from the last-known attributes in the property database and misses renovations; CoreLogic
says this outright in its help centre. A valuer who inspects would have the current state. The noise
fits the AVM actor, so it does not change the fit.

What I would always have and the data lacks, ranked:

1. **Property type** (house / unit / townhouse / land). Every AVM and valuer uses it first. The upload
   dropped it, and only the `/` in `ADDRESS` partly recovers it (REVIEW issue 5). A derived `UNIT` flag
   lowers LightGBM RMSE from 0.161 to 0.158, which shows the input matters.
2. **Previous sale price and date of the same property.** These are the strongest single input of a
   repeat-sales or hybrid AVM, and a known entity's history is a legitimate feature (USE-10). This
   source keeps only the latest sale per property, so the history cannot be rebuilt. It is a structural
   gap of the source, not a curation error.
3. **Exact sale (contract) date.** I have only the month; minor for monthly windows.
4. **Listing data** (asking price or price guide, days on market, sale method: auction or private
   treaty). These are known before the sale. A lender's AVM often does not use them; an agent's
   appraisal does. A moderate gap.
5. **Sale type / non-arm's-length flag.** It is needed to exclude transfers (the 52 sales below
   $120k, REVIEW issue 9). I would filter these before training and before scoring.

Nothing in the data is unknown at the prediction point. The school rank and station as of the scrape
affect training rows only (CC bullet).

**2. Target**

The sale price is what I act on (USE-5). Log price with RMSE is close to the percentage-error metrics AVM
vendors report, so the scale is right. I want a number plus an uncertainty (the forecast standard
deviation / confidence score every vendor ships); the benchmark scores only the point estimate,
which is acceptable.

The $2.44M cap (REVIEW issue 1) is selection on the target. A deployed AVM must value the dear houses,
and a model trained here never predicts above about $2.44M. But the test windows lack them as well,
and vendors report accuracy by price band and flag the top band as low-confidence (Microburbs:
"built and tested primarily on the sub-$800K segment"). So "price of a sale up to about $2.44M" is a
real, narrower population, about 1.5% of houses missing. It is a stated gap of the population, not a
stand-in.

**3. Row, decision, test data**

One row matches one valuation. The test months are what I face: next month's sales, with the model refit
at month start, and with comparables from the months just before (no gap, which matches an AVM fed by
listings within days; REVIEW issue 7). Sampling (latest sale per property, newest per suburb) thins the
old training years. That hurts history depth but not the test realism, since 2020 is nearly complete per
suburb. All 9 windows sit in 2020 (COVID year, the stimulus-driven upswing in Perth from mid-2020): a single
market regime, which an AVM vendor would not use as its only back-test. Longer windows (issue 6,
9 x 3 months) would cover more regimes, at the cost of the train share.

**4. Would I use it?**

As a benchmark of an AVM's core hedonic-plus-location component: yes. Trust comes from the forward split,
coordinates and the dense 2020 coverage. Distrust comes from no property type, no repeat-sales history, the
truncated top end, and unflagged non-market sales. A model built here would be weaker than a production AVM
(LightGBM RMSE about 0.16 in log, roughly 85% within 20%), but the task it measures is real.

**Gaps ranked by how much they change the task**

1. Price cap at $2.44M: changes the population, i.e. what "a Perth house" means (USE-5, USE-8: document it in `fit_reason`).
2. Missing property type: removes the first input any valuer has; partly recoverable from `ADDRESS` (CLEAN-12).
3. No sales history per property: removes the strongest AVM input (USE-10); unrecoverable from this source.
4. Non-market sales unflagged: noise in the train and test targets; unrecoverable without a sale type.
5. All test windows in one year and regime: narrows what the back-test shows.
6. Stale attributes in the test period: realistic for an AVM, so the smallest change.

**What an expert would change**

- Add a derived `UNIT` (strata) flag from `ADDRESS` (unit number) and keep `ADDRESS` (REVIEW issue 5,
  CLEAN-12). This rebuilds the property-type input the source destroyed.
- Rewrite `fit_reason` to say the actor is an AVM (stale database attributes are its normal condition). It
  should also say that property type and sales history are missing, and that the population is sales up
  to $2.44M.
- Consider 3-month windows (issue 6) so the back-test spans more than the 2020 regime.
- Keep the backlog note: heptix/perth-property-prices (property type, exact dates, no cap) is the better
  source for this use case. It could also give a previous-sale feature by joining sales of one address.

**Sources**

- datasets/_dev/tabarena-v0pt2/perth_house_prices/dataset.py, README.md, REVIEW.md; curation/records/perth_house_prices.md
- .claude/skills/knowledge-curation/references/use_case.md
- https://www.kaggle.com/datasets/syuzai/perth-house-prices
- https://www.microburbs.com.au/research/avm-accuracy-whitepaper (AVM inputs, metrics, price bands)
- https://auhelpcentre.corelogic.com.au/hc/en-au/articles/11038733839119-I-ve-updated-the-attributes-but-the-Estimated-Value-dropped-why (AVM works from database attributes)
- https://www.corelogic.com.au/news-research/news/2022/machine-learning-transforms-property-valuations (attributes, sales history, comparables, confidence)
- https://www.prres.org/uploads/780/1665/Rossini_Automated_Valuation_Model_Accuracy_Some_Empirical_Testing.pdf (Adelaide AVM accuracy)

</details>

<details><summary>Blind review</summary>

**Blind review: perth_house_prices (log_PRICE, regression, temporal split on DATE_SOLD)**

**Verdict: include with changes.** It is a real and useful house-price (AVM) task with good signal. The temporal split is defensible if the early years are dropped, but the snapshot nature of the scrape should be documented.

**Task**
A valuer, lender or portal estimates a Perth house's sale price from its attributes and location, before or at listing. This is a real, common use. OpenML 43822 / Kaggle syuzai: "scraped from http://house.speakingsame.com/ ... 322 Perth suburbs". Lat/long come from data.gov.au. School ranks come from bettereducation.

**Concerns (most to least serious)**
1. **The data is a snapshot of last sales, so early years are thin and survivor-biased.** Every ADDRESS+SUBURB pair appears exactly once (0 repeats), so this is one (latest) sale per property, scraped around 2020. Rows by year: 1988-2008 together hold about 860 rows (5-136 per year), 2013 has 1,048, and 2015-2020 have 3,000-5,600 each. A sale from 1990 means the house has not been resold since, and its attributes (FLOOR_AREA, GARAGE, BUILD_YEAR) are as scraped, not as at the sale date. Change: restrict to DATE_SOLD >= 2013 (or >= 2014), so the test windows come from the dense period and the training rows are more contemporaneous.
2. **NEAREST_SCH_RANK is anachronistic.** It is a single bettereducation ranking from around the scrape date, applied to every sale. This is a small leak or anachronism for older sales. With the date restriction above it is acceptable. Document it.
3. **Some values are implausible.** GARAGE goes up to 50 (75 rows have more than 10), BATHROOMS up to 16, 14 rows have FLOOR_AREA below 30, LAND_AREA goes up to 983,690 m2, and the minimum price is $51k. These are scrape errors, but they are few. Keep them as-is or set the extremes to NaN. Do not drop rows.
4. **Preparation.** ADDRESS (33,004 unique values) is a free-text near-ID and should be dropped as a feature. DATE_SOLD is month-granular (always the 1st of the month), which is fine. POSTCODE is an int but is categorical in nature. SUBURB, station and school are categories (321 / 68 / 160 levels), which is fine. NaNs in GARAGE (2,273), BUILD_YEAR (3,153) and SCH_RANK (10,717) are left as-is, which is fine. The target is the log of price, which is sensible.

**Signal**
LightGBM on the last 20% by date (excluding ADDRESS) gets R2 = 0.85, RMSE 0.18 log. That is clearly non-trivial, with room left between methods. The most important features are SUBURB, LAND_AREA, FLOOR_AREA and time. There are 10 exact feature duplicates (ignoring date and address), which is negligible.

**Could not check**
- The Kaggle page text (the page did not render); I used the OpenML description instead.
- Whether DATE_SOLD really is the last sale.
- The year of the school rankings.
- How the 9 windows are placed.

</details>

<details><summary>Precedent check</summary>

**perth_house_prices: precedents**

Inputs I read:
- the register (panel run) (the perth entries are open AI issues, with no curator line for the house family);
- the REVIEW.md files of house_sales, house_prices_nominal, melbourne_housing_market and zillow_prize, and their `dataset.py`;
- `houses/dataset.py`;
- the working copy's REVIEW.md: "Rules from the house_sales / house_prices_nominal / zillow_prize / distribution_transformers review" and the sarcoma item on USE-8;
- the rule texts USE-8, LEAK-6/7/10/11/26, SPLIT-10/12/14/15/21 and CLEAN-11/12, with their Cases tables.

All family precedents are from 2026-10-20 (AI panels, not yet decided by the curator) unless a date says otherwise.

**Per decision**

**1. Price cap at $2.44M, kept and documented (issue 1). Consistent.**
- LEAK-26 (Must) says "drop the capped rows or document the cap". Perth documents it with an `Anomaly:` bullet and a decision table.
- The closest precedent is `houses` (California, migrated 2026-10-14). It drops the rows clamped at 500,001.
- The fact that sets perth apart is in the data: its sales above the cap are missing, not clamped, so there is no row to drop. Documenting is the only option LEAK-26 leaves.
- REVIEW issue 1 cites cirrhosis "as a precedent for a recorded selection". That is a weak match: cirrhosis is a USE-5 relabelling over a follow-up cohort, not a cut on the target. houses is the closer precedent, and the LEAK-26 Cases row itself names "the house-price datasets".
- houses names its cap as a gap in `fit_reason` and reads `approximate`. That bears on decision 2.

**2. `fit="direct"`. Departs, without a stated reason.**
- USE-8 (Must) defines direct as rows, features, label timing and split all mirroring the use case. Approximate means "a stand-in with a known gap, named as such".
- Perth's `fit_reason` names two gaps itself: "Sales above about $2.44M are missing" and "the site's house record is often older than the sale".
- Precedents on the other side:
  - house_sales reads `approximate`, for values kept from after the sale.
  - houses reads `approximate`; one of its named gaps is the dropped capped rows.
  - zillow_prize reads `approximate` (USE-6).
- melbourne_housing_market still reads `direct`, but its own panel recommends `approximate` (its issue 3).
- house_prices_nominal reads `direct`. That is consistent: its record describes the house at the sale and it has no cap.
- This belongs with the family item "The fit label of the house-price datasets with values kept from after the sale" and the sarcoma item "Does a weak potential leak kept on purpose make a fit `approximate`?". Perth should be added to that item. Its gaps are a cap and stale records, not only a post-sale remnant, so even amendment (b) of that item would not cover it.

```text
**Consistency check (AI, 2026-10-20):** the fit of perth_house_prices (direct, a departure from USE-8) differs from
house_sales and houses (approximate 2026-10-20 / 2026-10-14, the same kind of named gap: values not as at the sale, the
dearest sales missing), and perth's fit_reason names both gaps itself. What sets perth apart?
(a) the gaps add noise but change neither the actor, the prediction point nor the label (an exception, recorded with
    the measured effect: stale records cost 0.012 RMSE on the 349 shared test rows; 45 of 4,132 test rows in the
    suburbs the cap hits); (b) treat perth like house_sales: `approximate`; (c) reopen house_sales and houses to
    `direct`; (d) amend USE-8 so that noise in the features or a documented cap does not by itself make a fit
    approximate (decide with the family fit item).
```

**3. Attributes recorded after the sale on training rows (LEAK-10). Consistent in substance; departs from melbourne on the note.**
- LEAK-10 (Must) allows looked-up attributes when the data shows they did not change.
- Perth has that evidence for rooms:
  - bedrooms or bathrooms differ from heptix's sold listings in 0.7% of the shared 2007-2016 sales. melbourne's `Bedroom2` equals `Rooms` in 98.9-100% of rows, the precedent in the LEAK-10 Cases row.
  - In the test period the record is older than the sale, not newer (issue 2), so no test row carries a value from after the sale. house_sales and melbourne cannot say this.
- What is missing:
  - The definition states none of this as a LEAK-10 point. It mentions only "the school and station columns are as of the scrape, which affects training rows only".
  - Land area, floor area, garage, build year and school rank are not checked against a value from before the sale. melbourne has the same gap for five columns, and it writes a `Potential leak, kept on purpose:` note.
- The working copy's item "Keep a post-outcome lookup because removing it changes no score?" (with the onlinenewspopularity LEAK-10 amendment) would cover perth either way. Perth has no blanking measurement, so it cannot claim the "no measurable effect" wording.

```text
**Consistency check (AI, 2026-10-20):** perth_house_prices keeps its scraped house record without a LEAK-10 note,
while melbourne_housing_market (2026-10-20, the same mechanism: attributes scraped after the sale) writes a
`Potential leak, kept on purpose:` note. What sets perth apart?
(a) the data shows the record did not change for the rooms (0.7% differ in 2007-2016) and predates the sale in the
    test period, so LEAK-10's "did not change" clause is met; write that as the note; (b) treat perth like melbourne:
    the same note, other columns unchecked; (c) drop melbourne's note to match; (d) amend LEAK-10 (the
    onlinenewspopularity proposal).
```

**4. The 563 sales before the build year are dropped (issue 4). Departs, with a stated reason that is not the one the rules ask for.**
- Precedents for the same mechanism (a record that describes a later building):
  - melbourne_housing_market blanks the scraped block of its 6 sales with `YearBuilt` after the sale year, and keeps the rows (LEAK-7, smallest fix).
  - house_prices_nominal sets one remodel year from after the sale to missing.
  - house_sales rebuilds the record as of the sale day (22 `yr_built` values).
- CLEAN-11 (Should) lets a row leave only when it is not a task row (USE-7) or is a copy.
- Perth's reason ("describe a house that did not exist at the sale", priced 0.23 log too high) is a LEAK-10 reason, and LEAK-10 calls for blanking.
- The fact that would allow dropping the row, that a land or off-the-plan sale is no house sale under the use case (USE-7), is not stated. The 140 build-year sales stay by the same reasoning.
- The 0.0004 RMSE effect is no distinguishing fact (the forest_fires tension).

```text
**Consistency check (AI, 2026-10-20):** your call on perth_house_prices (drop the 563 sales dated before the build
year) differs from melbourne_housing_market (2026-10-20, the same mechanism: YearBuilt after the sale; the scraped
block blanked, rows kept). What sets perth apart?
(a) these are land or off-the-plan sales, not the house sales the use case values (USE-7), recorded as the reason,
    with the 140 build-year sales stated as kept; (b) treat perth like melbourne: blank BUILD_YEAR and the house
    attributes, keep the rows; (c) reopen melbourne to drop its 6 rows; (d) amend CLEAN-11/LEAK-7 for sales before
    construction.
```

**5. No planning gap (issue 7). Follows house_prices_nominal's pending exception, and departs from house_sales and zillow_prize.**
- How the family handles the delay:
  - house_sales takes a one-week gap (it measured a median delay of 6 days).
  - zillow_prize takes a one-month gap.
  - house_prices_nominal takes no gap, an exception proposed in its issue 4 that rests on the mechanism, not on the effect.
- Perth runs the same mechanism test: December 2020's residual is +0.015, against +0.007 to +0.024 in July to November; relative to suburb medians it is +0.048, against +0.027/+0.023. This follows the house_prices_nominal item ("measure their newest months the same way or take a gap").
- It would be the second exception for this reason, so no amendment is due. A third would make one due.
- Two departures:
  - (i) `splits_comment` argues against the gap with "raises LightGBM's mean test RMSE from 0.159 to 0.162". SPLIT-21 (Must; aeolus, Lennart 2026-10-12) and the forest_fires tension rule a score out as the reason. house_prices_nominal's precedent check removed the same argument. The sentence should go, or be marked as context only.
  - (ii) REVIEW issue 7 says "no gap, as house_sales and house_prices_nominal". house_sales now has a one-week gap, so that citation is out of date.
- The dates are monthly, so the smallest possible gap is one month (as zillow_prize). That is a fact for the alternative, not against it.

```text
**Consistency check (AI, 2026-10-20):** perth_house_prices ships no gap, which differs from house_sales (one-week gap,
2026-10-20) and zillow_prize (one-month gap), and rests on house_prices_nominal's exception, which is still open. What
sets perth apart?
(a) the December 2020 sales present show no price selection (residual +0.015 against +0.007 to +0.024), the same
    mechanism test as house_prices_nominal; recorded as the second exception of that reason; (b) treat perth like
    zillow_prize: a one-month gap (month-resolution dates); (c) reopen house_sales/zillow to drop their gaps; (d) amend
    SPLIT-10 for a short newest period without price selection (due at the third case).
```

**6. December 2020 kept (issue 8). Consistent, with a stated distinguishing fact.**
- house_sales dropped its May 2015 because the extract stopped mid-month and "its quickly recorded sales are cheaper": it showed price selection.
- Perth's short December shows no price selection, so it is the same test with the opposite result.

**7. Window length of 9 x 1 month (issue 6). Consistent, with a stated fact.**
- The family item proposes house_sales' 3 x 3 weeks "where the size allows it".
- Perth's source dates sales by month only, so weekly windows cannot be built. zillow_prize (dated by month) also uses one month.
- SPLIT-14 holds (train share 88% or more). SPLIT-15 holds (the 3 x 3 count).
- The 2- and 3-month alternatives must be picked from the use case or the stale-record step, not from scores (SPLIT-21).

**8. ADDRESS kept as text (issue 5). Consistent.**
- melbourne_housing_market (`Address` string) and california_house_prices_2020 do the same.
- The UNIT-flag alternative has no precedent. CLEAN-12's Cases cover codes, split dates and ids, not a flag derived from free text. If adopted it would be a new Cases row.
- The 0.161 to 0.158 gain must not be the reason.

**9. Implausible values kept (issue 9). Departs, without a distinguishing fact.**
- CLEAN-11 (Should) says impossible values become missing and the row stays.
- melbourne sets 86 `BuildingArea` values to missing (under 10 m², a house's area equal to its lot, and others) without any source marker. house_sales sets 5 placeholder living areas to missing.
- Perth keeps floor areas of 1-40 m² for houses with 2-4 bedrooms, and one house of 95 m² with 16 bathrooms, because "nothing marks them missing". melbourne had no marker either, so that is not a distinguishing fact.
- Keeping the 52 sales under $120,000 is consistent: house_sales and house_prices_nominal drop non-market sales only on a source marker, and perth has none.

```text
**Consistency check (AI, 2026-10-20):** your call on perth_house_prices (impossible floor areas and room counts kept)
differs from melbourne_housing_market (2026-10-20, the same mechanism: scraped BuildingArea below 10 m2 or equal to the
lot, set to missing) and house_sales (placeholder areas to missing). What sets perth apart?
(a) perth's thresholds cannot be told from small real dwellings without the property type the upload dropped
    (recorded as the exception); (b) treat perth like melbourne: the same plausibility limits to missing (CLEAN-11);
    (c) reopen melbourne; (d) amend CLEAN-11.
```

**10. Scrape sampling: all rows kept (issue 3). Consistent.**
- Only the latest sale per property comes from the source and cannot be undone. This is unlike california_house_prices_2020's own newest-only dedup, which the family item asks to reopen.
- The "from 2013 on" alternative cites 0.1612 to 0.1607. Under SPLIT-21 (aeolus, Lennart 2026-10-12) the history must come from the use case, not that comparison.

**11. Citation and licence. Consistent.**
- Like melbourne, the citation is the Kaggle upload with a note naming the scraped site, and the licence is CC BY-NC-SA with the site's terms unstated.
- The house_sales and nyc_taxi PROV-10 item is about a government publisher. It does not apply here: the site never published this table.

**12. Other points. Consistent.**
- The accepted `meta_time_horizon_mismatch` matches zillow_prize. The unpinned download has no precedent against it.

**Drift and third exceptions**

- **Drift.** There is no curator decision on these rules for the house family yet, so there is no curator drift. The AI drafts disagree on the fit (approximate: house_sales, zillow_prize, houses; direct: house_prices_nominal, melbourne (pending), perth) and on the gap (one week, one month, none). Both are already open family items, and perth should be listed in each.
- **Third exceptions.**
  - SPLIT-10 "short newest month without price selection": 2 cases (house_prices_nominal, perth).
  - LEAK-10 "post-sale lookup kept on measurement": already the subject of the onlinenewspopularity amendment (house_sales, melbourne, aeolus, onlinenewspopularity); perth would join it.
  - Nothing else reaches three.

**Files**
- datasets/_dev/tabarena-v0pt2/perth_house_prices/dataset.py
- datasets/_dev/tabarena-v0pt2/perth_house_prices/REVIEW.md (issue 7, line 91, carries the out-of-date house_sales citation)
- datasets/_dev/tabarena-v0pt2/REVIEW.md (house-family items, lines 238-310)
- datasets/_dev/tabarena-v0pt2/melbourne_housing_market/dataset.py (lines 138-144, 185, 231-233)
- datasets/_dev/tabarena-v0pt2/house_sales/dataset.py (lines 200, 263, 278)
- datasets/_dev/tabarena-v0pt2/houses/dataset.py (lines 29-38)

</details>

<details><summary>Verification checklist</summary>

Prep checklist; it describes the definition before this review's changes.

**perth_house_prices: verification checklist (re-check, 2026-10-20)**

Automated: `dataset list` imports the class; `uvx ruff@0.15.15 check` and `format --check` clean. `dataset check`: 0
errors, 0 warnings, 26 checks, 1 accepted (`meta_time_horizon_mismatch`: month-start dates make a one-month window read
as one day; correct as it is). README diff: template only (`time_gap: null`, `time_gap_unit: null`, a `REVIEW.md` row);
checksum `v2:562faf8c...` unchanged. Raw sha256 `e9f33458...` matches the definition. `sync-notebooks --check` clean.

Probes (panel run): leak all features R² 0.842, best single SUBURB 0.615, depth-2/3 tree 0.414/0.493, missing indicators
<= 0.01, 0.0% exact copies across the split, ADDRESS as text 0.051; task flags none (LightGBM skill 0.863 +- 0.022,
linear 0.766, single feature POSTCODE 0.473, drift 0.010); hidden groups (temporal) SUBURB seen in train for 99.6% of
test rows, near copies 2.7%; generated probes no flags.

Own measurement (500-tree LightGBM, one seed, shipped windows): RMSE 0.139-0.181 (mean 0.162); mean residual by
window Dec +0.015, Nov +0.020, Oct +0.024, Sep +0.020, Aug +0.007, Jul +0.018, Jun -0.005, May -0.013, Apr -0.018.

| Rank | Check | Verdict | Evidence | Rules |
|---|---|---|---|---|
| P1 | Ethics | pass | Public sale records of a property site; no objection found, not a harmful task. | SEL-1 |
| P2 | Scope | pass | Price of a sale from the house and location; regression for a valuation decision, not a forecast of a series. | SEL-2 to SEL-15 |
| P2, P5 | Real data | pass | Scraped sales; generated probes no flags (exact formula 0.7% = shuffled 0.7%, 0 of 11 columns uniform). | SEL-16, PROV-3 |
| P3 | Use case and fit | concern | `fit="direct"`, yet the target is capped at $2.44M and test-period house records are stale (REVIEW issues 1, 2). The house-family item "fit label with values kept from after the sale" (house_sales -> `approximate` under USE-8) applies: perth's attributes (BUILD_YEAR, rooms, school rank, station) are the record at the scrape, after the training sales. | USE-1, USE-2, USE-8 |
| P3, P4 | Target and metric | concern | No sale above $2,440,000 (11 rows at $2.40-2.44M, max exactly 2,440,000): a capped target the source does not state. RMSE on log price fits. | LEAK-26, USE-5 |
| P4 | Available at prediction time | concern | Attributes are the site's record at the scrape (Jan 2021): for training rows later than the sale (LEAK-10 cross-dataset item on post-sale values, as house_sales/melbourne); the 563 pre-build sales dropped (0 remain). No planning gap although Dec 2020 is short (412 sales, 0.71 of Nov): the SPLIT-10 exception question raised by house_prices_nominal carries here. The mechanism test of that item: Dec 2020's present sales show no price selection (mean residual +0.015 against +0.007 to +0.024 in Jul-Nov). Perth cites house_sales/house_prices_nominal for "no gap", but house_sales now has a one-week gap. | USE-3, LEAK-10, SPLIT-10 |
| P4 | Irreversible and all-row leakage | pass | No supervised or all-row feature; NEAREST_SCH_RANK is an outside ranking, missing indicators carry nothing (<= 0.01). | LEAK-13 to LEAK-15, LEAK-27 to LEAK-31 |
| P4 | Copies across the split | pass | 3 geocoding copies dropped; 0.0% exact copies across the split with and without string/datetime; 0.2% of test ADDRESS values in train (each property once, by source). | LEAK-16 to LEAK-21 |
| P4 | Split regime | concern | Temporal, 9 x 1 month (Apr-Dec 2020), train shares 87.5-98.8% of rows. Window length differs from the family (house-family item "one window length"); all windows in the stale-record regime (REVIEW issue 6). Suburb-wise sampling thins old years (issue 3). | SPLIT-12, SPLIT-14, SPLIT-15 |
| P5 | Source | concern | Trail ends at a Kaggle scrape of house.speakingsame.com (plus G-NAF coordinates, school ranks); no first publication beyond the uploader; bibtex cites the Kaggle upload with the site in a note. | PROV-1, PROV-2, PROV-10 |
| P5 | Uniqueness | pass | OpenML 43822 is the same table (noted); heptix/perth-property-prices a separate scrape, separate candidate. No other working-copy folder uses it (grep of records). | PROV-4 to PROV-7 |
| P5 | Damage and repair | cannot verify | The cap and stale records cannot be repaired from this source; heptix comparison from the earlier review not re-run (external data not downloaded here). | PROV-13 to PROV-15, EV-7 |
| P6 | Worth benchmarking | pass | Task flags none; LightGBM beats dummy on 100% of splits; spread to linear +0.097 (SE 0.012); 284-628 rows per window. | TP-1 to TP-10 |
| P7 | Dtypes and cleaning | concern | Proxies converted (LAND_AREA 999999 and GARAGE 99: 0 left). Implausible values kept (GARAGE max 50, tiny floor areas, strata land areas) without marking missing (CLEAN-11 keeps rows; impossible values are a CLEAN question). ADDRESS as string with unit/lot meaning, CLEAN-12 alternative (UNIT flag) open (issue 5). | CLEAN-1 to CLEAN-24 |
| procedure | Notes match the code | pass | 33,656 raw rows (33,657 lines with header); 563 + 3 dropped -> 33,090; 321 suburbs; BUILD_YEAR max 2017, missing 9.5%; 52 sales < $120k since 2012; Dec/Nov 412/579 = 0.71; dates 1988-04 to 2020-12. All match. | writing.md |
| procedure | Licence and citation | cannot verify | CC BY-NC-SA 4.0 per the definition; Kaggle page did not render and the CLI is not installed here, so not re-read today. Citation names the Kaggle upload (no earlier publication exists). | EV-4, PROV-10 |
| procedure | Reproducibility | concern | The commands reproduce the sha256 locally; the Kaggle download is not version-pinned (`/1` returns 404 per the earlier review); OpenML 43822 is an alternative pinned copy. | |

</details>

<details><summary>Advocate</summary>

**Advocate: perth_house_prices**

Evidence folder: (panel run). Definition: `datasets/_dev/tabarena-v0pt2/perth_house_prices/dataset.py`.

**1. The task is real and the test is honest (P3, P4: USE-5, LEAK-1/LEAK-10, SPLIT-1/4/6/11; all Must or Should held)**
- **Claim:** this is a real automated-valuation (AVM) task with no leak into the test score.
- **Use case:** the practitioner says "One row is one sale = one valuation I make", and of the benchmark: "As a benchmark of an AVM's core hedonic-plus-location component: yes."
- **No leak:**
  - Claim audit: no column is recorded after the sale.
  - The leak probe flags nothing. Missing-value indicators reach R2 ≤ 0.01.
  - 0.0% exact copies cross the split. Each address+suburb pair occurs once, so no repeat sale crosses the cutoff.
- **Split:** nine calendar-month windows, April to December 2020. Training always ends the month before the test month. The split audit's verdict is "right with notes".
- **Value (P6):**
  - LightGBM R2 0.863 ± 0.022 against linear 0.766, and it beats the dummy on 100% of splits.
  - The windows hold 284-628 sales each, and no task flags were raised.
- **Why it wins:** every validity Must holds. The points below are Shoulds or quality issues, and none of them is a Must that cannot be fixed.

**2. The $2.44M cut meets LEAK-26 (Must), which allows "document the cap"**
- **Evidence:**
  - Raw maximum is exactly $2,440,000, with nothing above.
  - Column audit: only one row sits at the cut, and the next five prices are distinct ($2.425-2.437M). So dearer sales were removed, not clamped, and there is no capped row to drop.
  - This is documented in an `Anomaly:` bullet and a decision table.
  - About 1.48% of houses are affected (75 of 5,072 in heptix), and the cut applies to train and test alike.
- **Precedents:** the precedents agent says documenting "is the only option LEAK-26 leaves". `houses` drops clamped rows, but perth has none.
- **Practitioner:** AVM vendors report accuracy by price band and flag the top band. "Price of a sale up to about $2.44M" is a narrower real population, not a stand-in.
- **Mildest remedy:** reword "capped" to "truncated at $2.44M (dearer sales absent)", as the column audit suggests.

**3. Attributes as of the scrape: noise in the test rows, weak and training-only otherwise (LEAK-10 Must, fixed or kept the smallest way per LEAK-7)**
- **Test rows:**
  - The house record is older than the sale, not newer: 27.0% of 2020 sales differ from heptix's sold listings, and "fewer" dominates. Nothing from after the sale reaches a test row.
  - The practitioner calls this the normal condition of an AVM (CoreLogic's help centre says the AVM works from database attributes).
- **Training rows:**
  - Bedrooms and bathrooms differ in only 0.7% of 2007-2016 sales. That meets LEAK-10's "unless the data shows they did not change", the same test as the melbourne Cases row (98-100% agreement).
  - 147 rows (0.44%) name a station that had not yet opened, and 58 name a school that had not yet opened.
  - Blanking the two station columns for those 147 rows gives mean RMSE 0.1615 against 0.1622, which is no gain.
  - Dropping `NEAREST_SCH_RANK` gives 0.1623 against 0.1622.
- **Concession:** `fit_reason` ("Everything the model sees is known when a house sells") overstates this for training rows.
- **Mildest remedy:**
  - Write a LEAK-10 note citing the 0.7% agreement.
  - Blank the 147 station values; this is cheap and uses the zillow_prize option (a).
  - Add a `Potential leak, kept on purpose:` note for the school columns and the rank year.
- **Why it wins:** the remedy ladder. A weak, training-only effect that changes no score is fixed in the definition or noted. The dataset is not excluded.

**4. The fit label does not block shipping (USE-8 Must: the label must be stated)**
- **Case for direct:** the practitioner argues direct: "None of the USE-8 'approximate' patterns applies … the gaps narrow the population or remove inputs."
- **Against:** precedents house_sales, houses and zillow_prize read approximate. The precedents agent raises a consistency check.
- **Concession:** if the `Potential leak, kept on purpose:` note from point 3 is written, the kick case under USE-8 makes the label approximate.
- **What follows:** this is a one-word label decided by the open house-family fit item. It is a weighing call for the curator, not a reason to hold the data. Under either label, the rows, split and target stay the same.

**5. No gap is defensible, and it is the second instance of a known exception (SPLIT-10 Should; SPLIT-12)**
- **Mechanism test (the one SPLIT-10 guards against):** December 2020's mean residual is +0.017, inside the +0.003 to +0.025 of July-November. The short newest month shows no price selection.
  - Contrast: house_sales dropped its May 2015 because it did show price selection.
- **Resolution:** dates are given by month only, so the smallest possible gap is the whole previous month. The real delay is days: an archived Mount Lawley page of 14 April 2021 lists four April 2021 sales among its 10 newest.
- **Exception count:** this would be the second exception for this reason (after house_prices_nominal), so no amendment is due. The split audit drafts the exception text.
- **Concessions (cheap):**
  - Remove the RMSE argument (0.159 → 0.162) from `splits_comment`, because SPLIT-21 (Must) rules a score out as the reason.
  - Fix REVIEW issue 7, which cites house_sales, and house_sales now has a one-week gap.
- **SPLIT-20 (COVID year):** keep the monthly cadence the use case sets (SPLIT-12) and state in `splits_comment` that all test months are in 2020. Widening the windows stays as REVIEW issue 6 for the curator, and must not be chosen from scores (SPLIT-21).

**6. Dropping the 563 pre-build sales serves the use case (USE-7 Must over CLEAN-11 Should)**
- **Evidence:**
  - The 563 sales describe a building put up 1-23 years after the sale. They are land or off-the-plan sales, not the house sale the valuation acts on.
  - LightGBM, trained without them, prices them too high: +0.11 to +0.53 log units depending on setup (claim audit).
  - All are training rows from 1988-2016. The effect on test RMSE is 0.0004.
- **Rule:** USE-7 (Must, part 2) says a row lacking the input the prediction acts on is no task row. That outranks CLEAN-11 (Should, part 7), which keeps rows.
- **Why melbourne differs:** melbourne blanked 6 such rows. Blanking here would keep land sales labelled as house sales with no house attributes.
- **Mildest remedy:**
  - State the USE-7 reason in the note, and say the 140 sales in the build year are kept.
  - Replace "0.23 log units" with "0.1-0.5 by setup".

**7. The cleaning gaps are cheap fixes, not reasons to hold (P7 CLEAN-11/12 Should; principles step 3: "fixed when the fix is cheap and safe")**
- **Concessions:**
  - 19 houses with 2+ bedrooms have 1-40 m² of floor area, and two bathroom counts are impossible (16 baths in 95 m²; 7 baths with 1 bedroom). These should be set to missing with the rows kept: RMSE 0.1624 against 0.1622, neutral. "Nothing marks them missing" is no CLEAN-11 reason, and melbourne did the same without a marker.
  - `Vic` merges two stations 14 km apart (33 test rows). Split it by longitude.
- **ADDRESS:**
  - Keeping it as text follows melbourne_housing_market and california_house_prices_2020.
  - A UNIT flag (CLEAN-12) is an optional improvement. It gives 0.1622 → 0.1592, but that gain cannot be the reason to add it.
- **Kept as is:** the 52 sales below $120k stay, consistent with house_sales and house_prices_nominal, which drop non-market sales only on a source marker. A price floor of our own would filter on the target.
- **Why it wins:** these are quality issues (P7) that the definition fixes in a few lines. Independent of the above, they do not combine into a validity failure.

**Judgment record (advocate's view)**
```text
Verdict: ship after small changes.
Validity: SEL-1/2 hold; USE-5 holds; USE-8 label open (family fit item); LEAK-26 met (documented, reword "truncated");
LEAK-10 triggered weakly on training rows, fixed (blank 147 station values) + note; SPLIT-10 departure kept as the
2nd exception (no price selection in Dec 2020); SPLIT-21: drop the score sentence from splits_comment.
Value: TP holds (R2 0.86, +0.097 over linear, 284-628 rows per window).
Quality: CLEAN-11 impossible floor areas/bathrooms to missing; CLEAN-12 split `Vic`; UNIT flag optional.
Weighed: use case +, signal +, coverage of 2020 +; source (scrape, truncation) -, single test year -.
For the curator: fit label (family item), gap exception, window length (issue 6).
```

</details>

<details><summary>Critic</summary>

**perth_house_prices: critic, opening brief (2026-10-20)**

Position: ship only after the changes below. The task is real (practitioner, blind review, probes) and no point here
is a reason to exclude it; points 1-2 are Musts that are fixable in the definition, points 3-5 are Should departures
without a recorded exception, points 6-7 are quality.

**1. The fit label and its text say more than the data holds (P3, USE-8 Must)**

- Problem: `fit="direct"`, and `fit_reason` opens "Everything the model sees is known when a house sells". But the same
  `fit_reason` names two gaps (no sale above $2.44M; stale house records in the test months), and for training rows
  the house, station, school and rank columns are the record of January 2021, after the sale (point 2).
- Effect: the label tells the benchmark user the task mirrors an AVM back-test with no known gap; it does not. The
  population is "sales up to $2.44M" (1.48% of 2015-2020 houses missing per heptix; 45 of 4,132 test rows in the
  suburbs the cut hits).
- Evidence: column_audit problem 1 (147 station and 58 school anachronisms); claim_audit row 7 and row 14 (27.0% of
  2020 shared sales differ in bed/bath); precedents decision 2: house_sales and houses read `approximate` for the same
  kinds of gap (values not as at the sale; dearest sales missing), zillow_prize too; houses names its cap in
  `fit_reason`.
- Counter-evidence I accept: the practitioner argues direct (stale database attributes are the AVM's normal state).
  That covers the test-row staleness, not the training-row anachronisms nor the cut population.
- Remedy (fix the definition, text only): `fit="approximate"` with the gaps named (truncated population, attributes as
  of the scrape), and rewrite `known`/`fit_reason` so they are true. Or, if the curator prefers direct, record it as
  the exception of the open house-family fit item (precedents' consistency check (a)/(d)); it cannot stay direct
  silently. Also say "truncated at $2.44M (dearer sales absent)" instead of "capped": only one row sits at $2,440,000
  (column_audit, target row).

**2. Training rows carry attributes from after the sale, with no LEAK-10 treatment (P4, LEAK-10 Must; LEAK-7 Should)**

- Problem: 147 training sales (1988-2014) name a nearest station that had not opened (Mandurah line Dec 2007,
  Clarkson 2004, Butler 2014), with its distance; 58 sales of 1990-2014 name Joseph Banks Secondary College (opened
  2015); `NEAREST_SCH_RANK` is one snapshot of 2019 or later, possibly published after every test sale (2020 ATAR
  results, late December 2020). LEAK-10 excludes "attributes looked up after the outcome ... unless the data shows they
  did not change"; for these rows the data shows they did change.
- Effect: weak, training rows only (blanking the 147 station rows: RMSE 0.1615 vs 0.1622; dropping the rank: 0.1623).
  Not a test-score leak, but a Must is not waived by a small effect, and the notes say "affects training rows only"
  without the LEAK-10 note melbourne_housing_market writes for the same mechanism.
- Evidence: column_audit table rows NEAREST_STN, NEAREST_SCH, NEAREST_SCH_RANK and problems 1-2; precedents decision 3.
- Remedy (smallest fix, LEAK-7): blank `NEAREST_STN` and `NEAREST_STN_DIST` for sales before the station opened (22
  opening dates; zillow_prize precedent); a `Potential leak, kept on purpose:` note for the school columns and the
  rank, naming the ranking year as unknown; and write the rooms fact as the LEAK-10 "did not change" evidence (0.7% of
  shared 2007-2016 sales differ).

**3. The 563 pre-build sales are dropped for a reason that calls for blanking (P4/P7, LEAK-7 Should, CLEAN-11 Should; USE-7 Must)**

- Problem: the stated reason ("the row describes a house that did not exist at the sale") is a LEAK-10 reason, whose
  smallest fix is to blank the record and keep the row (LEAK-7); CLEAN-11 lets a row leave only when it is no task row
  (USE-7) or a copy. The 140 sales in the build year, with the same mechanism, stay.
- Evidence: precedents decision 4 (melbourne blanks its 6 such rows; house_prices_nominal blanks one remodel year).
  The supporting number "priced 0.23 log units too high" does not reproduce: 0.11 to 0.53 by setup (claim_audit 45b,
  EV-1 Must).
- Remedy (fix the definition or record the reason): either state the USE-7 reason (land and off-the-plan sales are no
  house sale the use case values) and say why the 140 build-year sales stay, or blank `BUILD_YEAR` and the house
  attributes for these rows and keep them. Replace 0.23 with the range and its setup.

**4. No gap, and the case against one rests on a score (P4, SPLIT-10 Should; SPLIT-21 Must)**

- Problem: sales reach the site late (December 2020 at 0.71 of November against 0.83-1.04 in 2013-2019, no January
  2021 row although scraped 31 January), yet the split has no gap; the `splits_comment` argues against a gap with
  "raises LightGBM's mean test RMSE from 0.159 to 0.162". SPLIT-21 forbids deciding the windows from such a
  comparison. REVIEW issue 7 cites house_sales for "no gap", but house_sales now has a one-week gap.
- Evidence: split_audit problem 1 (no gap 0.1596, one-month gap 0.1622, worse in 6 of 9 windows); claim_audit row 66;
  precedents decision 5 (zillow_prize one-month gap at month resolution).
- Remedy (a note or a definition change, per the curator's answer on house_prices_nominal issue 4): delete the RMSE
  sentence from `splits_comment`; then either `gap=1` or a recorded SPLIT-10 exception resting on the mechanism
  (December's residual +0.015 to +0.017 within July-November's range: no price selection). Fix the house_sales
  citation in REVIEW issue 7.

**5. All nine test windows fall in one atypical stretch (P4, SPLIT-20 Should)**

- Problem: April-December 2020 is the COVID year (April-May 316 and 284 sales against 421 and 440 in 2019) and the
  stale-record regime (bed/bath differ in 27.0% of 2020 sales against 0.7% in 2007-2016). SPLIT-20 asks to widen the
  windows so most do not fall in an atypical season. No exception is recorded.
- Effect: the benchmark measures one market regime; the practitioner says an AVM vendor would not use it as its only
  back-test.
- Evidence: split_audit problem 2; practitioner section 3; REVIEW issue 6 has the alternatives (9 x 2 months from July
  2019; 9 x 3 months from October 2018, train share from 64%).
- Remedy: choose the window length from the use case, not from scores (SPLIT-21): either widen (9 x 2 or 9 x 3 months)
  or record the exception (monthly refit cadence, SPLIT-12) in the `splits_comment` with the COVID and stale-record
  facts.

**6. Impossible values kept (P7, CLEAN-11 Should)**

- Problem: 19 houses with 2+ bedrooms at 1-40 m2 floor area (one at 1 m2); 16 bathrooms in a 95 m2 four-bedroom house;
  7 bathrooms with 1 bedroom. The reason given, "nothing marks them missing", is not a CLEAN-11 reason; melbourne set
  86 unmarked impossible `BuildingArea` values to missing.
- Evidence: column_audit problem 5 (neutral: RMSE 0.1624 vs 0.1622); precedents decision 9.
- Remedy (repair, cheap): set these values to missing, rows kept. Garage 13-50 and strata land areas stay as unusual.
  Quality only; not a reason to hold back the task by itself.

**7. Destroyed meaning left unrebuilt (P7, CLEAN-12 Should)**

- Problem: the station label `Vic` merges Victoria Street (Mosman Park) and Victoria Park, 14 km apart, 0.67 log units
  apart in mean price, 33 test rows. The property type (unit / house), the first input every valuer uses, survives only
  as the "/" in `ADDRESS`; CLEAN-12 calls this reconstruction "always welcome".
- Evidence: column_audit problem 4; practitioner gap 2; claim_audit row 65 (1,060 unit rows, median $404k vs $540k).
- Remedy (repair): split `Vic` by longitude into the two station names; add a derived `UNIT` flag from the unit number
  in `ADDRESS` (kept as text too) for the curator's decision, justified by the lost property type, not by its score.
  Smaller wording fixes from the claim audit ride along: claim 25 (the two kept pairs also differ in coordinates),
  claim 64 (Baldivis: the May window, not April).

</details>

<details><summary>Advocate rebuttal</summary>

**Advocate rebuttal: perth_house_prices**

The critic's brief is the critic's brief above.

**Shared ground.** The critic says "no point here is a reason to exclude it". Both briefs end on ship after changes, so the remaining differences are about which fix, not whether to ship.

**1. Fit label and wording (USE-8 Must): conceded in part**
- **I concede:**
  - `fit_reason` and `known` must be rewritten so they are true. "Everything the model sees is known when a house sells" is false for 147 station rows and 58 school rows in training.
  - "capped" should become "truncated at $2.44M (dearer sales absent)".
  - The fit label cannot stay direct silently.
- **I dispute that `approximate` is the only answer:**
  - USE-8's approximate list is: a snapshot standing in for a forecast, a potential leak kept on purpose, a reconstructed time axis, a label without a horizon, or one judge standing in for a rating.
  - The truncation and stale test records are on neither list. The practitioner says they "narrow the population or remove inputs; they do not turn the task into a stand-in".
  - The one trigger that does apply is the `Potential leak, kept on purpose:` note for school and rank (point 2 below). Under kick's case that makes the label approximate.
- **What follows:** if that note is written, `approximate` is correct and I accept it. If the curator instead drops `NEAREST_SCH_RANK`, which costs nothing (0.1623 against 0.1622), and blanks the school anachronisms the way the stations are blanked, direct could be defended. That choice belongs to the house-family fit item, with the precedents agent's consistency check (a) or (d) recorded. Either label ships the same data.

**2. Training-row anachronisms (LEAK-10 Must): conceded**
- **I concede:** this is the same remedy as my point 3.
  - Blank `NEAREST_STN` and `NEAREST_STN_DIST` for sales before the station opened.
  - Write a `Potential leak, kept on purpose:` note for the school columns and the rank, saying the ranking year is unknown.
  - Write the 0.7% figure (bed/bath differ in 0.7% of shared 2007-2016 sales) as LEAK-10's "did not change" evidence for the rooms.
- **I agree** with the critic that a small effect does not waive a Must. The size only shows that the fix is cheap and safe.

**3. The 563 sales dated before the build year (USE-7 Must against LEAK-7 / CLEAN-11 Should): disputed on the remedy**
- **I concede:**
  - The note gives a LEAK-10-style reason, when the reason that justifies a drop is USE-7. It should say: "land or off-the-plan sales, not the house sale the use case values".
  - The note must say why the 140 sales in the build year stay. They are the boundary case: a house finished in the year of its sale can be a sale of a finished house.
  - "0.23" must become "0.1-0.5 log units by setup" (EV-1).
- **I dispute blanking as the better fix:**
  - Blanking `BUILD_YEAR` and the house attributes keeps rows whose label is the price of land or of a contract to build. That label has a different meaning from every other row.
  - USE-7 (Must, part 2) outranks CLEAN-11 (Should, part 7) and LEAK-7 (Should). So the drop is the rule-consistent fix once its reason is stated.
- **Melbourne is a different case:** it had 6 rows and did not test their prices. Here the rows are measurably priced too high in every setup (+0.11 to +0.53), which supports "not a house sale".
- **Effect:** all 563 are training rows and the test RMSE changes by 0.0004, so either fix is safe. The curator should pick between my USE-7 reason and blanking (precedents check (a) or (b)).

**4. No gap and the score argument (SPLIT-10 Should, SPLIT-21 Must): conceded**
- **I concede:**
  - Delete the RMSE sentence from `splits_comment`.
  - Fix the house_sales citation in REVIEW issue 7.
  - Record the SPLIT-10 exception on the mechanism (December's residual +0.015 to +0.017, inside July-November's +0.003 to +0.025, so no price selection), or take `gap=1` if the curator's answer on house_prices_nominal issue 4 goes that way.
- **One fact to add to the exception:** the month resolution allows no gap shorter than the whole previous month, while the observed delay is days (the Mount Lawley page). This is the case the split audit's draft exception already names.

**5. All test windows in 2020 (SPLIT-20 Should): conceded on the exception, disputed on widening**
- **I concede:** the departure needs a recorded exception in `splits_comment` that names COVID and the stale-record regime.
- **I dispute widening as the fix:**
  - The use case is a model refit monthly (SPLIT-12, the horizon set from the actor). Two- or three-month windows score a refit cadence nobody in this use case runs.
  - The 9 x 3 option drops the oldest train share to 64%.
  - Wider windows also do not escape the stale-record step: per REVIEW issue 2, only 3 of the 9 three-month windows fall before mid-2019.
- **What follows:** keep monthly windows with the SPLIT-20 exception: "the use case refits monthly (SPLIT-12); the source has dense coverage only from 2019-2020; serves P3". Widening stays the curator's call in issue 6, and must not be decided from scores (SPLIT-21).

**6. Impossible values (CLEAN-11 Should): conceded**
Set the 19 floor areas of 1-40 m² and the two impossible bathroom counts to missing, and keep the rows. The effect is neutral (0.1624 against 0.1622), and melbourne is the precedent. Garage counts of 13-50 and strata land areas stay as unusual values.

**7. Destroyed meaning (CLEAN-12 Should): `Vic` conceded, the UNIT flag left to the curator**
- **I concede:** split `Vic` by longitude into its two stations. The claim-audit wording fixes ride along: claim 25 (the two kept pairs also differ in coordinates) and claim 64 (Baldivis's missing training rows are in the May window, not April).
- **The UNIT flag:** I do not oppose it. Its reason is the lost property type, not the 0.1622 → 0.1592 gain. But keeping `ADDRESS` as text matches melbourne and california_house_prices_2020, and the flag has no CLEAN-12 Cases precedent, so it is an addition for the curator to decide, not a condition for shipping.

**Net position**
```text
Verdict: ship after changes (both sides agree).
Agreed fixes: fit_reason/known rewritten; "truncated"; station blanking + school/rank note + rooms LEAK-10 evidence;
0.23 -> range; RMSE sentence out of splits_comment; house_sales citation; impossible values to missing; `Vic` split;
claim 25/64 wording.
For the curator: fit label (approximate if the school/rank note stays, family item); 563 rows: drop under USE-7
(advocate) or blank (critic); gap=1 or SPLIT-10 exception (house_prices_nominal issue 4); monthly windows with a
SPLIT-20 exception (advocate) or widen (issue 6); UNIT flag.
```

</details>

<details><summary>Critic rebuttal</summary>

**perth_house_prices: critic, rebuttal (2026-10-20)**

We now agree on most points. Both briefs say ship after changes and neither asks for exclusion. Three disputes remain:
the fit label, the COVID-year windows and the UNIT flag. Only the fit label is a Must.

**Advocate 1 (real task, honest test): concede**

No column is recorded after the sale, the test rows get nothing from after the sale, and the value holds (claim_audit,
probes). The one possible exception is `NEAREST_SCH_RANK`, whose ranking may postdate test sales. That is covered by
the note both briefs ask for.

**Advocate 2 (LEAK-26, "truncated" wording): concede**

The remedy is the one in my point 1.

**Advocate 3 (LEAK-10 remedies): concede**

Blank the 147 station values. Add a LEAK-10 note citing the 0.7% agreement. Add a `Potential leak, kept on purpose:`
note for the school columns and the rank year. This is my point 2. The advocate also concedes that `fit_reason`
overstates what is known, so `known` and `fit_reason` must be rewritten as part of this fix.

**Advocate 4 (the fit label is a curator call that does not block): dispute in part**

- The advocate concedes that once the point-3 note is written, the kick case under USE-8 makes the fit `approximate`.
- USE-8 is a Must, and rules win over precedents and open items (principles, "Conflicts between rules").
- So the definition cannot ship with `direct` while it carries that note. It must read `approximate` with the gaps
  named, or the curator must record an exception or an amendment through the house-family fit item.
- I agree the rows, the split and the target do not change, so this alone does not hold back the data. But the label
  is not optional: "open" is not a valid shipped state under a Must.

**Advocate 5 (no gap as the second SPLIT-10 exception; SPLIT-20 kept with a statement): concede the gap, dispute SPLIT-20 in part**

- **Gap: concede.** Removing the score sentence (SPLIT-21) and recording the exception on the mechanism is the mildest
  remedy SPLIT-10 allows. December 2020's residual of +0.017 lies within July to November (+0.003 to +0.025), and this
  would be the second case. Fix the house_sales citation as well.
- **SPLIT-20: dispute the remedy.** A Should departure needs "the fact that sets the case apart and the higher
  principle it serves, recorded as an exception" (principles, Strengths). The sentence "all test months are in 2020"
  states the problem; it is not an exception.
- The advocate's own reason, the monthly cadence of SPLIT-12, is a rule in the same part, not a higher principle.
- What can carry the exception is the use case (USE-1, P3): a monthly refit back-test. Record that as a
  `**Exception to SPLIT-20 ...**` with the COVID facts and the stale-record facts (316 and 284 sales in April and May
  against 421 and 440; 27.0% stale). Otherwise widen the windows per REVIEW issue 6, chosen without scores (SPLIT-21).

**Advocate 6 (drop the 563 pre-build sales under USE-7): concede, with one condition**

- USE-7 (Must, part 2) outranks LEAK-7 and CLEAN-11 (Should). A land or off-the-plan sale is not the house sale the
  valuation acts on.
- The advocate's reason against blanking holds: blanking would leave land sales labelled as house sales.
- Condition: the note must state the USE-7 reason and why the 140 sales in the build year stay. The rule cannot tell
  them apart from completed houses, even though 9-13% of them are priced more than 0.5 log units too high (REVIEW
  issue 4). The note should also replace 0.23 with "0.1-0.5 by setup" (EV-1).

**Advocate 7 (cleaning): concede CLEAN-11 and `Vic`; dispute "UNIT flag optional" in part**

- CLEAN-12 (Should) calls rebuilding destroyed meaning "always welcome".
- Property type is the first input any valuer uses (practitioner, gap 2), and the upload dropped it.
- Leaving the flag out is a departure, so it needs a stated reason. Keeping `ADDRESS` as text is not one: the probe's
  tokenisation drops the "/" (REVIEW issue 5).
- Precedents note that CLEAN-12's Cases do not cover a flag derived from free text. So I accept that the curator
  decides it as a new Cases row, with the reason being the lost property type, not the 0.003 gain.
- This is quality (P7) only, and not a reason to hold back the data.

**The judgment record I would sign**

```text
Verdict: ship after changes.
Validity: LEAK-26 met (truncated, reworded); LEAK-10 fixed (147 station values blanked) + notes; USE-8 approximate
  (kick case) unless the curator records an exception or an amendment; USE-7 drop of the 563 stated (with the 140 build-year sales);
  SPLIT-10 exception (2nd case, mechanism); SPLIT-20 exception on the use case, or wider windows; SPLIT-21 score
  sentence removed.
Value: TP holds.
Quality: CLEAN-11 impossible values to missing; CLEAN-12 `Vic` split; UNIT flag for the curator.
```

</details>

<details><summary>Mediator</summary>

**Mediator: perth_house_prices**

**Recommendation (judgment record)**

```text
Verdict: ship after changes.
Validity: SEL-1/2 hold; USE-5 holds; USE-7 applied (563 pre-build sales dropped as land/off-the-plan sales, 140
build-year sales kept and stated); USE-8 approximate (school/rank potential leak kept on purpose, the kick case; the gaps
named: truncated at $2.44M, attributes as of the January 2021 scrape) unless the curator amends USE-8 (issue 1);
LEAK-26 met (cap documented, reworded "truncated"); LEAK-10 triggered on training rows, fixed (147 station values
blanked, 58 school values blanked) + note (rooms 0.7% "did not change" evidence; rank year unknown); SPLIT-21:
the score sentence leaves splits_comment; SPLIT-10 open (issue 2: 2nd mechanism exception or gap=1); SPLIT-20 open
(issue 3: spaced monthly windows or a recorded exception).
Value: TP holds (LightGBM R2 0.863 +- 0.022, linear 0.766, 284-628 rows per window, beats dummy on 100% of splits).
Quality: CLEAN-11 impossible floor areas/bathrooms to missing; CLEAN-12 `Vic` split; UNIT flag open (issue 5).
Weighed: use case +, signal +, source (a scrape, truncated, one sale per property) -, single test year -.
For the curator: issue 1 (USE-8, family fit item), issue 2 (gap), issue 3 (window placement), issue 4 (history
from 2013), issue 5 (UNIT flag).
```

**Changes to make now (no decision needed)**

1. **`fit="approximate"` (USE-8, Must).** Name the gaps in `fit_reason`: the population is truncated at $2.44M, the attributes are as of the scrape, and a potential leak is kept on purpose. Rewrite `known`/`fit_reason` so they are true; "Everything the model sees is known when a house sells" goes. If the curator amends USE-8 (issue 1), the label is revisited then.
2. **Write "truncated at $2.44M (dearer sales absent)" instead of "capped" (LEAK-26, Must; EV-2).** Only one row sits at $2,440,000.
3. **Station anachronisms (LEAK-10, Must; LEAK-7).** Blank `NEAREST_STN` and `NEAREST_STN_DIST` for the 147 sales before the station opened. Use the 22 opening dates (zillow_prize option (a)).
4. **School and rank.**
   - Blank `NEAREST_SCH` and its distance for the 58 sales before Joseph Banks Secondary College opened (2015). This is my addition. It is the same mechanism with a known opening date, so the remedy ladder (fix the definition before keeping with a note) and the station fix call for the same treatment.
   - The `Potential leak, kept on purpose:` note stays for `NEAREST_SCH_RANK` (ranking year unknown, possibly after the test sales) and for school assignments not checked.
5. **Rooms (LEAK-10 "did not change").** Write the evidence: bedrooms/bathrooms differ in 0.7% of the shared 2007-2016 sales. In the test period the record is older than the sale, not newer.
6. **The 563 pre-build sales (USE-7, Must, outranks LEAK-7/CLEAN-11, Should).**
   - Reason: land or off-the-plan sales are not the house sale the valuation acts on.
   - State that the 140 build-year sales stay, and why: they are the boundary case, and 9-13% of them are priced more than 0.5 log too high.
   - Replace "0.23 log units" with "0.1-0.5 log units by setup" (EV-1).
7. **Delete the RMSE sentence (0.159 → 0.162) from `splits_comment` (SPLIT-21, Must).**
8. **Fix the house_sales citation in REVIEW issue 7.** house_sales now has a one-week gap.
9. **Impossible values to missing, rows kept (CLEAN-11; melbourne precedent).**
   - The 19 floor areas of 1-40 m² for houses with 2+ bedrooms.
   - 16 bathrooms in a 95 m² house; 7 bathrooms with 1 bedroom.
   - Garage counts of 13-50 and strata land areas stay as unusual values.
10. **Split `Vic` by longitude** into Victoria Street (Mosman Park) and Victoria Park (CLEAN-12; 14 km apart, 33 test rows).
11. **Wording:**
    - claim 25: the two kept pairs also differ in coordinates;
    - claim 64: Baldivis's missing training rows are in the May window.
12. **Keep the 52 sales below $120k.** There is no source marker, and a price floor would filter on the target (consistent with house_sales and house_prices_nominal).

**Issues for the curator (ranked)**

**1. Fit label: amend USE-8 or not (P3, USE-8 Must; family items "Does a weak potential leak kept on purpose make a fit `approximate`?" and "The fit label of the house-price datasets").**
- **Problem:** once the agreed school/rank note is in, USE-8 as written makes the fit `approximate` (the kick case). Most LEAK-30 keeps read `direct`. That is the open family question.
- **Effect:** a one-word label. Rows, split and target do not change.
- **Critic's best evidence:**
  - USE-8 is a Must, and rules win over precedents.
  - house_sales, houses and zillow_prize read `approximate` for the same kind of gap. houses names its cap in `fit_reason`.
- **Advocate's best evidence:**
  - The truncation and stale test records are on none of USE-8's listed patterns. They narrow the population or remove inputs; they do not turn the task into a stand-in (the practitioner's view).
  - Drop the rank (0.1623 vs 0.1622) and blank the school anachronisms, and no kept leak remains.
- **Ruling:** under the rule as written, `approximate` (shipped now, change 1).
- **Decision needed:** answer the family item.
  - Keep USE-8: perth stays `approximate`.
  - Amend it so that a weak keep, a documented cap and stale records do not make a fit approximate: perth may go `direct`. Note that the cap and stale records sit outside even amendment (b) of the house_sales item, so the amendment would have to say so.
  - Precedent check options (a)-(d) apply.

**2. Gap: one month, or no gap as the second SPLIT-10 exception (P4, SPLIT-10 Should).**
- **Problem:** sales reach the site late. December 2020 is 0.71 of November, against 0.83-1.04 in 2013-2019.
- **Effect:**
  - No gap is mildly optimistic.
  - A one-month gap removes more than the real delay, which is days (Mount Lawley page, 14 April 2021).
  - The source dates sales by month only, so a one-month gap is the smallest possible.
- **For the exception:** December's residual (+0.015 to +0.017) lies within July-November's (+0.003 to +0.025), so there is no price selection. This is the same mechanism test as house_prices_nominal.
- **For `gap=1`:** zillow_prize uses one month at the same resolution, and house_sales uses one week.
- **Decision needed:** decide house_prices_nominal issue 4, and apply the same answer here. The split audit has drafted the exception text. A third case would make an amendment due.

**3. Where the nine monthly windows fall (P4, SPLIT-20 Should vs SPLIT-12 Should).**
- **Problem:** all nine windows are in 2020.
  - April and May are COVID months (316 and 284 sales, against 421 and 440 in 2019).
  - The year is in the stale-record regime (27.0% of shared sales differ).
- **New fact from my run:** the two rules do not conflict. `TemporalSplits(window=1, unit="months", n_windows=9, step=3)` keeps the monthly refit and spaces the windows Dec 2020, Sep, Jun, Mar 2020, Dec 2019, Sep, Jun, Mar 2019, Dec 2018.
  - 367-569 test rows per window.
  - Train share 0.667-0.988, so SPLIT-14 holds.
  - 5 of 9 windows are before COVID, and 2-3 are before the mid-2019 stale-record step.
  - rain_in_australia spaces its windows (`step=42`) for the same purpose, to cover seasons.
  - Only counts were computed, no scores (SPLIT-21).
- **For contiguous 2020 windows:**
  - In 2020 the record predates the sale, so no test row carries a post-sale value.
  - Older windows reintroduce scrape-dated attributes into test rows (2.8% differ in 2017-2018, 0.7% earlier).
  - Older windows hold survivor-thinned suburbs: 11 of 321 suburbs have no rows yet by December 2018.
  - Contiguous windows also match the family's contiguous windows.
- **For spaced windows:**
  - SPLIT-20 asks that most windows fall outside an atypical season, and the monthly-refit reason no longer distinguishes the case, since spaced windows keep it.
  - The critic's point holds: SPLIT-12 is a same-part rule, not a higher principle, so it cannot carry an exception alone.
- **Decision needed:** `step=3` (my lean; no exception needed), or contiguous windows with a recorded `**Exception to SPLIT-20**`. The exception would rest on the use case (P3) and the no-post-sale-values fact, with the COVID and stale-record numbers. The 2- or 3-month windows of REVIEW issue 6 remain an option. Choose without scores, and together with the family item "One window length for the house-price datasets".

**4. Training history: all of 1988-2020, or 2013 on (P4, SPLIT-20 Should; REVIEW issue 3; blind review).**
- **Problem:** the years before 2013 hold 2,263 sales, mostly houses never resold, with attributes as of the scrape.
- **For keeping everything:** no break in the data collection; it is the history a refit would have.
- **For 2013 on:** the blind review argues for it (survivor bias, anachronistic attributes).
- **Rule:** decide from the use case, not from 0.1612 vs 0.1607 (SPLIT-21).
- **Decision needed:** keep all (implemented), or cut, with a use-case reason.

**5. UNIT flag from `ADDRESS` (P7, CLEAN-12 Should).**
- **Problem:** the property type, the first input a valuer uses, survives only as the "/" in `ADDRESS` (1,060 unit rows, median $404k against $540k).
- **Critic:** CLEAN-12 calls such reconstruction "always welcome".
- **Advocate:** keeping the text matches melbourne and california_house_prices_2020, and no CLEAN-12 case covers a flag derived from free text.
- **Not a reason either way:**
  - the 0.1622 → 0.1592 gain (SPLIT-21 / forest_fires tension);
  - that the probe's tokeniser drops the "/". A model's limits are never an argument (CLEAN-22, EV-4).
- **Decision needed:** add `UNIT` and keep `ADDRESS` (my lean, a new CLEAN-12 Cases row), or keep the text only.

**Agreed facts**

- **Task and leakage:**
  - A real AVM task: one row is one sale, valued from attributes and location.
  - No column is recorded after the sale. Leak probe clean, missing indicators R² ≤ 0.01, 0.0% exact copies across the split.
  - Each ADDRESS+SUBURB pair occurs once.
- **Target:** the maximum is exactly $2,440,000, with one row at it. The dearer sales are absent, not clamped: 1.48% of heptix houses in 2015-2020, and 45 of 4,132 test rows are in the affected suburbs.
- **Stale records:**
  - Bed/bath differ from heptix in 0.7% of 2007-2016, 2.8% of 2017-2018, 12.1% of 2019 and 27.0% of 2020 sales, mostly "fewer".
  - In the test period the record predates the sale.
- **Anachronisms:**
  - 147 sales name a station not yet open; 58 name a school opened in 2015.
  - The rank is one snapshot from 2019 or later.
  - Effects are weak and in training rows only (0.1615 / 0.1623 vs 0.1622).
- **Pre-build sales:** 563 dated before the build year, all training rows 1988-2016. Priced 0.1-0.5 log too high by setup. Effect on test RMSE 0.0004.
- **Split:**
  - 9 contiguous monthly windows, April-December 2020, 284-628 rows each, train share 0.875-0.988.
  - December's residual is within July-November's.
  - Gap effect +0.0025 RMSE (no reason either way).
- **Value:** LightGBM R² 0.863, linear 0.766.
- **Cleaning:**
  - 19 impossible floor areas and 2 impossible bathroom counts.
  - `Vic` merges two stations 14 km apart.
- **Both sides:** ship after changes, and neither asks for exclusion.

**Consistency with precedent**

- **Fit:** `approximate` follows house_sales, houses, zillow_prize and kick. It departs from melbourne (`direct`, its panel recommends `approximate`) and from the LEAK-30 `direct` group that the sarcoma item flags. That is the open family item, not a perth fact.
- **LEAK-10 note and blanking:** follows melbourne (note) and zillow_prize (blanking by date).
- **563 drop:** departs from melbourne's blanking of 6 rows. The fact that sets perth apart is the USE-7 reason: these are land or off-the-plan sales, measurably mispriced in every setup. Melbourne never tested its rows. Precedent check (a).
- **No gap:** the second instance of house_prices_nominal's pending exception, against house_sales (one week) and zillow_prize (one month). It waits on house_prices_nominal issue 4. Not yet a third exception.
- **Spaced windows:** rain_in_australia (step=42) is the precedent. The house family uses contiguous windows, so adopting `step=3` should be decided with the family window-length item.
- **Impossible values to missing:** follows melbourne and house_sales.
- **Cap documented:** consistent with LEAK-26. houses drops clamped rows, but perth has no clamped row.
- **Below-$120k sales kept:** consistent with house_sales and house_prices_nominal.
- **ADDRESS as text:** consistent with melbourne and california_house_prices_2020. A UNIT flag would be a new CLEAN-12 Cases row.

Files read: everything in (panel run), plus `datasets/_dev/tabarena-v0pt2/perth_house_prices/dataset.py` and `datasets/_dev/tabarena-v0pt2/REVIEW.md` (the house-family and sarcoma items).

</details>
