---
unique_name: california_house_prices_2020
name: CALIFORNIA_PRICES_2020
checked_by:
- Lennart
- Mustafa
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
decision_markers:
- Missing source information
tags:
- Non-IID (Temporal)
- Free Text (Sentences)
- 'Samples: Over Time'
- 'Time: Dated'
- 'Target: Varying Delay'
collections:
- AutoML_MM
- TabSTAR
- MulTaBench
- STRABLE
original_source: Other
year: '2021'
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.openml.org/search?type=data&id=46669
- https://www.kaggle.com/c/california-house-prices
notebook_path: datasets/beyond_iid/temporal/california_house_prices_2020/california_house_prices_2020.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/california_house_prices_2020/dataset.py
source_row: 734
type_adapter_id: curation-record-v1
---

## Comments

CC (2026-09-30, Lennart): **Split fixed: the "temporal" split ran on alphabetical address order.** The deduplication step (`groupby([Address, Zip, Year built]).idxmax()` + `df.loc[idx]`) returned rows in address order and `time_index` was then rebuilt from it (Spearman 1.000 with address rank, 0.003 with Listed On; leak audit 2026-09-24). Fix: sort back to the Kaggle Id before rebuilding `time_index`. The Id order is the sale order (checked on redfin.com earlier; in the data the latest listing date per Id decile rises from 2020-03-02 to 2020-12-30, Spearman(Id, Listed On) 0.745), so the split stays on it, not on Listed On: a house is listed before it sells, and a listing-date split could train on houses sold after the test period starts. Now: Spearman(time_index, address) 0.006, (time_index, Listed On) 0.757; in all 3 windows every training row precedes every test row. No target leak: Listed Price alone gives R^2 0.915 (legitimate, known before the sale). Leaderboard numbers on the old container come from an effectively random split.

California Houses 2020 Prices (Duplicate with calif_houses below).

Timestamp is missing! ....

Unclear if summary has an impact on predictions. A lot of spatial features, likely require spatial splits.

Very likely scraped from https://www.redfin.com/CA/Los-Altos/540-Pine-Ln-94022/home/1137626 / https://www.redfin.com/news/data-center/

Only data from redfin looks like this: https://www.kaggle.com/datasets/thuynyle/redfin-housing-market-data?select=neighborhood_market_tracker.tsv000
One could buy a scraped version: https://crawlfeeds.com/datasets/redfin-usa-properties-dataset

Summary contains free text that might not be super useful but still very much contains a lot to extract

---

Sold Price is target from the kaggle competition, the TextTabBench Paper considers Total interior livable area and Listed Price instead, data might be spatial and temporal. How do we deal with multi-categorical columns like Heating/Cooling/Parking? Also the Bedroom column is sometimes integer sometimes Text (multi-categorical), I feel like it could take a lot of preprocessing depending on what we do with columns like Heating/Cooling/Parking and similar

Unclear source of data, likely copied from somewhere with modifications. Used for teaching maybe? Data looks scraped

We need to find the original source... something from D2L website

MT: summary column feels like it makes more sense to be preprocessed into multiple columns, if it was to be converted to an embedding I can see the LM doing the conversion being confused by some fancy wording that may not mean a better apartment (like italian style of apartment) and leading to misleading results, so it makes sense just to be preprocessed in a real life scenario
Also in a real life scenario images would be used as well for such task

CC (2026-10-06, Lennart): Kept after the task-probe review (flag `one_feature`: `Listed Price`). The listing price is the natural core of predicting a sale price and is known before the sale, so its dominance is expected. On the three temporal windows of v0.2, predicting the sold price as the listed price gives R^2 0.89-0.91 (the 39 listings priced at $0 get the train mean), any curve rising with it (isotonic) 0.92, LightGBM on all numeric features 0.93, and BeyondArena's best with the text (on the old address-order split) 0.945: the methods cut the remaining error by about a fifth, so the task is not trivial. What is left to predict is the sale-to-list ratio (75% of homes sell within 10% of their list price). Data notes: 921 sales (2.2%) closed at under half or over twice their list price, some apparently one transaction booked on several houses (four listings at $1.1-1.45M each with a sold price of $8.75M).

**Assessment (AI, 2026-10-14):** 2,480 homes (6.0%) have a last sale on or after their listing date, so the listing describes an earlier sale; 125 of them give the predicted price as the last sale price. They are 5-6% of each test window but 50-54% of its squared error. LightGBM RMSE on the shipped windows: 0.196 with them, 0.140 without; also dropping 2,601 listings older than 6 months before the sale gives 0.117.

CC (2026-10-14, Lennart): Drop the 37 rows whose last sale is the sale itself and the 2,480 whose listing predates their last sale (the 37 are among them); keep listings older than 6 months. 39,048 rows.

CC (2026-10-21, Lennart): the declared metric documents the original use case's metric; overrule it only when it is biased or wrong (evidence from the paper); keep the note of the original metric (TP-6 amended).

**Assessment (AI, 2026-10-21):** metric stays the default RMSE: the competition scored RMSLE (Kaggle API) and the target is stored as log1p, so RMSE on it is RMSLE. The notes now say so. Needs a rebuild to reach the container (notes only).

CC (2026-10-21, Lennart): We want to keep real repeats, as houses can be sold several times; drop only exact copies of one sale.

**Assessment (AI, 2026-10-21):** Of the 63 homes that appear more than once (130 rows), 51 pairs give the same sold price a median 61 Kaggle IDs apart: one sale scraped twice; the newest entry stays. The other 28 rows (sales at another price, some of them other units at an address without a unit number) now stay instead of only the newest entry; 39,060 rows. The split also violated SPLIT-14 (Must): with min_train_fraction=0.25 the oldest of the three quarter-size windows trained on 25% of the rows. Now three windows of a sixth of the rows (6,510) from the newest half, training on 50%, 67% and 83%. Dataset check: 0 errors, 0 warnings.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source rmse — RMSLE, the competition's evaluation metric, as RMSE on log1p(Sold Price).

**Assessment (AI, 2026-10-21):** metric now `Metric.source("rmsle", target_transform="log1p")` instead of rmse on the log1p target: the competition's RMSLE on the sale price, computed after the inverse of the shipped log1p (MET-3); the score is the same number as before. Needs a rebuild to reach the container.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): ordinal scales shipped as numbers, left as numbers for the curator's review: `Elementary School Score`, `Middle School Score`, `High School Score`.

CC (2026-10-31, Lennart): marks on the review board of PR #37 (ordinal scales in the codebook's order, also when shipped as numbers; a state outside a scale missing when the column has no other missing value, else the lowest level; cycles ordered; codes shipped as numbers as categories): 3 ordinal scales shipped as numbers are ordered categories (point 3).

**Assessment (AI, 2026-11-01):** the benchmark MulTaBench (https://arxiv.org/abs/2605.10616) carries this record's data as "California Prices": Extended release (admitted on Joint Signal only), not one of the 40 benchmark datasets. Target binned by MulTaBench, not the source's own target. Text-tabular (OpenML 46669); the record ships the price as a regression. Tagged MulTaBench on 2026-11-01.

**Assessment (AI, 2026-11-01):** the benchmark STRABLE (https://arxiv.org/abs/2605.12292) carries this record's data as "California Housing": Mismatch: the paper describes the 1990 census California Housing (camnugent link), but the raw file is TextTabBench's cf_house_train.csv (Kaggle 'California House Prices' competition, 2020 Zillow listings) and the target is 'Total interior livable area', not the sale price. Records: california_house_prices_2020 (Yes, target Sold Price) and calif_houses (No, Duplicate of it, TexTabBench tag). Tagged STRABLE on 2026-11-01.

CC (2026-11-01, Lennart): the decode rule (a code whose codebook says in words what each level is carries the words; a score without them is a number): 3 scores are numbers (Elementary School Score, Middle School Score, High School Score).

CC (2026-11-11, Andrej): review marks applied (Review issues 1, 2, 4 and 5); the data changes from 39,060 to 38,991 sales.

- Issue 1 (B, "Agree."): `_clean` drops the 14 sales that share one sold price with another address of the same street and ZIP code and sold for more than 1.5 times their list price (eight condos of 321 and 327 S Elm Dr, Beverly Hills, "sold" for $35.8M each). A building's price booked on each unit is not a home's price, and the 8 of them in the newest window carried 36% of its squared error.
- Issue 2 (B, "Drop them. Also do a more thorough search since other more subtile leaks might be present."): the description written after the sale is dropped; the wider leak search (dollar amounts and prices per square foot in the text, tax values, last sale, listing fields filled after the sale, the id order) found no further leak.
- Issue 5 (B): that drop is the phrase "closed escrow" alone, 1 row. The other 12 texts state an asking price a buyer reads at the listing (a price cut, "buy it now", a probate auction's minimum overbid) or a loose bound, which is a feature, not a leak; "sold for" is no rule, as its 39 other descriptions speak of neighbours or earlier sales.
- Issue 4 (B): the scraped-twice rule is extended to a sale scraped under two spellings of its address: the same description (over 50 characters), sold price, ZIP code, living area and year built on two or more addresses within 600 Kaggle IDs, newest entry kept, 54 rows.
- The test windows shrink with the rows: a sixth of the sales is 6,498 rows, so `horizon` is 6,498. `dataset check` passes (0 errors). Issues 6 and 7 stay open.

**Assessment (AI, 2026-11-11):** split-row mark ("Why is there no planning gap, can this be justified?"), answered in Review issue 7, which covers the split. The gap itself was measured before: at equal training size a gap of a third or a whole window moves the RMSLE by -0.001 to +0.005 in no consistent direction, while a gap of the real listing-to-sale delay (about two thirds of a window) would push the oldest window's training share below half. New: the newest window is not selected by the outcome. Across the six sixths of the sale order the mean log(sold/list) runs -0.0004 to -0.0124 without a trend (Spearman of the sale order with the ratio -0.009), and the newest window sells slightly slower than the rest (days-on-market proxy median 53 against 46 to 48), not faster. The censoring shows only inside the window, where the homes listed in its last two months (69% of it) sold above list in 47% to 70% of cases against 10% to 20% for the homes listed in May to September that were still selling; the two groups balance. A gap would cut the recent listings out of the test side and leave the slow sellers, so it would create a selection rather than remove one. Recommendation unchanged: no gap (issue 7, A); the curator has the call.

## Review

**Outcome:** added. The Kaggle competition "California House Prices" of the Dive into Deep Learning course (2021):
homes sold in California in 2020 with their listing as scraped from Zillow (list price, listing date, description, home facts, last
sale, tax assessment, schools); the target is the log sale price, scored by the competition's RMSLE, on three windows
in sale order (the Kaggle row id), each trained on all earlier sales. 38,991 sales after the curators' fixes (the
descriptions that state the price, listings of an earlier sale, Arizona, one sale scraped twice, one price booked on
several homes; 2026-11-11). The AI recommends
shipping it after two small row fixes (issues 1 and 4). Reviewed without a panel, from the gathered evidence (the
record, the definition) and three checks of the rows. Validity: the competition's task with a reconstructed time axis
(fit approximate); the tax assessment is the value before the sale, not the county's value reset by the sale (checked,
below); 14 sales carry one price booked on several homes, a building's price on each unit, and 8 of them take 36% of
the newest window's squared error (issue 1); 54 sales appear twice under two spellings of the address (issue 4).
Value: not trivial (Lennart, 2026-10-06): the list price alone scores RMSLE 0.156 on the windows, LightGBM on the
numeric columns 0.143. Quality: 275 sales (0.7%) closed at under half or over twice their list price and carry half or
more of each window's squared error; apart from issue 1 nothing shows they are errors, so they stay. Weighed: real
sales with a rich listing and a real time order +; an undocumented scrape and a reconstructed time axis -.

**Main points:** Drop 5 more sales scraped twice, whose second copy lacks the year built (6; the new leak search finds
no further leak)? Keep the split without a planning gap, now measured (7)? Issues 1, 4 and 5 were resolved on
2026-11-11 (38,991 sales), 2 on 2026-11-10, 3 on 2026-11-06.

**Record judgment:** valid, with two small row fixes. The record's open points are settled: the sale order from the
Kaggle id (Lennart, 2026-09-30), the listings that describe an earlier sale (2026-10-14), real resales kept
(2026-10-21), the windows in the newest half (2026-10-21), the list price's dominance (not `Trivial`, 2026-10-06). The
tax assessment was checked against California's rule that a sale resets the assessed value to the price (Proposition
13): the assessed value is within 1% of the sale price for 1.5% of the homes and of the list price for 1.3%, its median
is 65% of the sale price, the share is flat across the sale order, and for homes last sold before 2012 it is within 1%
of the 2020 price for 0.7%; so it is the value before the sale, and dropping the two tax columns makes LightGBM worse
(RMSLE 0.144 against 0.143). The marker `Missing source information` stays: the host does not say where the rows come from
(the website is Zillow, by the generated text in the descriptions; 2026-11-11).

**Issues for Andrej:**

1. **Drop the 14 sales whose price is one transaction booked on several homes?**

   * **Problem:**
     - In five groups, neighbouring homes close in sale order carry the same sale price at 1.5 to 19 times their list
       prices, such as eight condos of 321 and 327 S Elm Dr, Beverly Hills, each listed at $1.9-3.9M and each "sold"
       for $35.8M: one price for a whole building or several lots, booked on each home.
     - Such a price is not the home's price, the quantity the task predicts, and no model can find it from one
       listing[^1a].
     - Drop these sales, keep them, or drop every sale far from its list price?
   * **Background:** the groups are found without a model: the same sale price on at least two addresses within 30
     Kaggle ids, every one of them sold for more than 1.5 times its list price (14 sales). A looser rule, any sale above
     twice its list price that shares its price with a neighbour, finds 41. Beyond them, 275 sales closed under half
     or over twice their list price; some may be wrong list prices, some real, and nothing in the data tells which.
   * **Effect on the task:** the score of the oldest window is mostly these few rows: the benchmark then ranks
     methods by how they miss a price no listing explains.
   * **Experiments:** an earlier check, untuned LightGBM on the three v0.2 windows (oldest first): the 14 sales are 8,
     2 and 2 test rows and carry 41%, 5% and 1% of the window's squared error (RMSLE 0.157 to 0.121 without them in
     the oldest window); the 275 far-from-list sales carry 64%, 57% and 48%.
   * **Consistency:** follows house_sales, where sales whose price is not the house's alone were dropped (Lennart,
     2026-10-22, its issue 10).
   * **Unknown:** whether the other far-from-list sales are errors; the Redfin pages would show it.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep them (implemented) | 39,060 sales | no rule to maintain | a building's price scored as a home's; one window's score mostly 8 rows |
     | B | Drop the 14 | the five groups go (39,046 sales) | only rows shown not to be one home's price; rule reads no model | the other far-from-list sales stay |
     | C | Drop all 275 far from the list price | every sale under half or over twice its list price goes | scores no longer dominated by outliers | drops real sales by their label; changes the task |

   * **Recommendation:** B, drop the 14: their price is shown not to be a home's, while the other outliers have no
     such evidence. **Decision:** drop the 14 (B), keep them (A), or drop all far-from-list sales (C)?

   **Notes for the AI:** on B, in `_clean` after the other filters: group by `Sold Price`, cluster rows of at least
   two distinct addresses within 30 `time_index` steps, drop the clusters where every row has
   `Sold Price / Listed Price > 1.5`; assert 14 rows; add a curation note and update `changes`. Re-run `dataset check`.

   **Answer (AI, 2026-11-06):** a correction to the evidence above, found while checking the time axis. The checks ran
   on the BeyondArena container, whose `time_index` is still the address order of the bug fixed on 2026-09-30
   (Spearman with `Listed On` 0.003 in the container, against 0.757 for the Kaggle id): the "neighbouring homes close
   in sale order" are close in address order (the units of one building sort together), and the window counts (8, 2
   and 2 test rows, 41% of the oldest window's squared error) and the shares of the 275 far-from-list sales are those
   of address-order sixths, which mix the year like random folds, not of the definition's sale-order windows. The
   finding itself stands: one price on several units of one building is a building's price. The rule in the notes,
   though, groups within 30 steps of `time_index`, which in the definition is the sale order, so it may find another
   set than these 14: on B, group the equal prices by ZIP code and street name instead (321 and 327 S Elm Dr share
   both), recount on the definition's rows, and recompute the window shares there. The Kaggle file is not on this machine (the
   download needs the competition's rules accepted on this account), so these numbers are not redone here.

   [^1a]: **USE-5** (Must): predict what the actor would act on; check how the source built its label.
     **CLEAN-11** (Should): a row whose target is not the task's quantity may leave; values that are only unusual
     stay.

   **Andrej (2026-11-10, discuss):** So what do you recommend with the evidence correction now?

   **Answer (AI, 2026-11-10):** still B, drop the 14. Redone on the definition's rows in sale order, the case is
   stronger, and the rows sit in the newest window instead of the oldest.

   * **What changed:** the Kaggle file is now on this machine. The groups are found by ZIP code and street name instead
     of 30 steps of the old address order: equal sale prices on two or more addresses of one street, every one sold for
     more than 1.5 times its list price.
   * **Same 14 rows, now in 4 groups:** 8 condos of S Elm Dr, Beverly Hills ($35.8M each, 9 to 19 times the list price),
     and 2 sales each on Aster St (93562), Alderpoint Rd (95511) and Woodrow Wilson Dr (90046). 4 of the 14 fall in the
     training-only half.
   * **Their weight in each window** (untuned LightGBM on log price, the three sale-order windows; Slurm job 1376291):

     | Window (train share) | Test rows | The 14: rows | The 14: share of squared error | RMSLE | RMSLE without the 14 | Far-from-list sales: rows, share |
     |---|---|---|---|---|---|---|
     | Newest (83%) | 6,510 | 8 | 36% | 0.162 | 0.129 | 50, 66% |
     | Middle (67%) | 6,510 | 0 | 0% | 0.130 | 0.130 | 48, 47% |
     | Oldest (50%) | 6,510 | 2 | 2% | 0.133 | 0.132 | 39, 53% |

   * **Before** (address-order sixths): 8, 2 and 2 rows in the oldest-first windows, with 41%, 5% and 1% of the error.
     Now the 8 Elm Dr condos make a third of the newest window's error, so the newest window ranks methods by a
     building's price.
   * The 271 far-from-list sales (under half or over twice the list price) still carry about half of each window's
     error, but nothing shows they are errors, so they stay (C stays not recommended).
   * **Recommendation:** B, with the rule by ZIP code and street name (asserting 14 rows). **Decision:** B (drop the
     14), A (keep) or C (drop all far-from-list sales)?

   **Andrej (2026-11-11, change):** Agree.

   **Resolved (2026-11-11, Andrej):** B, by ZIP code and street name: `_clean` drops, after the other filters, the sales
   that share one sold price with another address of the same street and ZIP code, each sold for more than 1.5 times
   its list price; 14 rows asserted (the same 14). Curation note and `changes` updated; `dataset check` passes.

2. **Drop the 11 descriptions that state the sale price in other words?**

   * **Problem:**
     - The definition drops the 5,413 listings whose description says "last sold for", since the sold price is the
       target; 11 more descriptions give a dollar amount within 0.5% of the sale price that is not the list price,
       such as "Property has closed escrow for $1,500,000" or an auction's minimum bid.
     - These descriptions were written or edited after the sale.
     - Drop them as the others, or keep them?
   * **Experiments:** under LightGBM they carry no measurable share of the windows' error (2, 2 and 0 test rows); 10
     further descriptions name an amount equal to both the list and the sale price and stay.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep them (implemented) | 39,060 sales | no new rule | a known leak stays in 11 rows |
     | B | Drop them | the 11 sales go | the earlier fix applied to every phrasing | 11 rows fewer; a rule on dollar amounts in text |

   * **Recommendation:** B: a confirmed leak goes even when small, and the earlier fix already set the rule[^2a].
     **Decision:** drop the 11 (B), or keep them (A)?

   **Notes for the AI:** on B, drop rows whose `Summary` holds a dollar amount within 0.5% of `Sold Price` that is not
   within 0.5% of `Listed Price` (11 rows on the BeyondArena rows; recount on v0.2), in the same step as the "last
   sold for" filter, and extend that curation note.

   [^2a]: **LEAK-6** (Must): measure before acting; a confirmed leak goes even when small. **LEAK-10** (Must): a
     feature holds only what existed at the prediction point.

   **Andrej (2026-11-10, change):** Option B: Drop them. Also do a more thorough search since other more subtile leaks
   might be present.

   **Answer (AI, 2026-11-10):** applied, and the search finds no further leak. Two findings get their own issues: one
   sale scraped twice under two spellings of its address (issue 4), and most of the 13 dropped texts state an asking
   price, not the sale (issue 5).

   | Where a leak could hide | Test on the 39,060 rows | Result |
   |---|---|---|
   | Any dollar amount in the text near the sold price, not the list price | within 0.5% | 13 rows (not 11 on these rows): 1 "closed escrow", 7 asking prices after a cut or an auction's minimum bid, 5 loose bounds ("under $500K") |
   | Price per square foot in the text, times the living area | within 2% of the sold, not the list price | 3 rows (2 homes), all a reduced asking price per square foot |
   | Price-cut phrases ("reduced", "now offered") | count | 423 rows; a cut is known before the sale, no leak |
   | Tax assessed value | within 0.5% of sold / of list | 0.76% / 0.66% of rows; correlation of log(tax/list) with log(sold/list) 0.12; the value before the sale (record judgment) |
   | Annual tax | within 0.5% of sold | 0 rows |
   | Last sale price | within 0.5% of sold / of list | 152 / 137 rows; median 822 days before the listing, real earlier sales |
   | Listing fields filled after the sale | list price equal to the sold price, by tenth of the sale order | 8.0% to 10.1%, flat; no listing date after the scrape |
   | IDs or order that track the price | Spearman of the sale order with log(sold/list) | -0.008; neighbours with equal prices 160, against 148 when shuffled |
   | One home across sales | the same description, price, ZIP, area and year built, addresses spelled differently | 54 pairs (108 rows), each within 500 Kaggle ids; none crosses from training into a test window (issue 4) |

   **Resolved (2026-11-10, Andrej):** B: in the same step as the "last sold for" filter, `_clean` drops the descriptions
   with a dollar amount within 0.5% of the sold price and not within 0.5% of the list price: 13 sales on the
   definition's rows, 39,047 left. The curation note and `changes` are updated, and `dataset check` passes.

   **Answer (AI, 2026-11-11):** the rule was narrowed to the one "closed escrow" text (issue 5). A second, model-based
   leak search ran on the rows after issues 1, 4 and 5: issue 6.

3. **Time basis and split: keep the windows cut in sale order, although a home is predicted at its listing, or set a
   gap of about the time from listing to sale?**

   * **Problem:**
     - A home is predicted when it is listed, but the windows are cut in sale order, the time its label arrives, so a
       test home listed before its window began is scored by a model trained on sales that closed after its listing.
     - The record's facts fit (`Samples: Over Time`; `Time: Dated`, as the Kaggle id tracks the sale order;
       `Target: Varying Delay`, a sale closing days to months after the listing), and the split is temporal, so no
       use-case prototype applies[^3a].
     - Keep the sale-order windows and write this down, or set a gap?
   * **Background:**
     - The sale order is the definition's choice for a reason: a cut on the listing date would train on homes that sold
       after the test period began, and since a home enters the data only once sold, the newest listings are the fast
       sellers (4,442 listings in October 2020, 2,204 in November, 264 in December); in sale order every training label
       precedes the window and no window is selected by how fast its homes sold.
     - A gap in sale order would leave the oldest window, which trains on exactly half the rows, below the floor of half,
       unless the windows shrink or move[^3b].
     - The scrape's later values were checked: the tax assessment is the value before the sale (record judgment), and so
       is the annual tax (median 1.26% of the assessed value, 0.82% of the sale price, the rate on the old assessment);
       descriptions rewritten after the sale are issue 2.
   * **Unknown:** how many test homes of each window were listed before it began, and what the training sales closed
     after their listing add; it needs the Kaggle file's sale order, which is not on this machine (the BeyondArena
     container keeps the old address order).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Sale-order windows (implemented), the facts in the split comment | as now; the comment states that the cut is the sale and the prediction the listing | no window selected by how fast its homes sold; every training label before the window | test homes listed before their window meet later sales; the size unmeasured |
     | B | A gap in sale order | train on sales up to about the listing-to-sale delay before each window | closer to a model refit at the listing | the gap's size unknown without sale dates; costs the floor or a window |
     | C | Windows by listing date | test the homes listed in each window | the prediction point is the cut | trains on homes that sold after the window began; the newest listings are the fast sellers |

   * **Recommendation:** A now, and measure once the Kaggle file is placed; B only if the training sales closed after
     a test home's listing add a clear share of the score. **Decision:** A, B or C?

   **Notes for the AI:** on A, no `data_tags` change (a temporal split takes no time basis); append to `splits_comment`:
   "The windows are cut in sale order, the time the label arrives, while a home is predicted at its listing: a test
   home listed before its window began meets training sales that closed after its listing (not measured; the data has
   no sale dates). A home enters the data only once sold, so a cut on the listing date would make the newest listings
   the fast sellers." The measurement, with `train.csv` in `local-data-warehouse/california_house_prices_2020/`: for
   each window, the latest `Listed On` of its training rows bounds its start from below; count the test rows listed
   before it; LightGBM at equal training size with and without the newest training sales (a third of a window), on the
   test rows listed before and after the bound.

   [^3a]: **SPLIT-32** (Should): how the data was collected, when each sample, feature and target come into existence,
     is information for the split; the record carries the source's collection facts, and a split that is not temporal
     names a prototype or a forced tag; a temporal split needs neither.
   [^3b]: **SPLIT-10** (Should; amended 2026-11-04 and 2026-11-05): train on the rows whose outcome is known by the
     window's start, with a gap of about the label's delay; the measurements decide, and where the gap breaks the floor
     the departure is an exception. **SPLIT-14** (Must): at least 3 windows, none trained on less than half of the data.

   **Resolved (2026-11-06, Andrej):** A, accepted through the cross-dataset item "Accept the arrival notes on temporal
   splits with one mark?" The arrival text (cut in sale order, predicted at the listing, the effect not measured) is
   appended to `splits_comment`. The measurement in the notes waits for the Kaggle file in the warehouse; B only if the
   training sales closed after a test home's listing add a clear share of the score. The split, its gap and `data_tags`
   are unchanged; a temporal split takes no time-basis tag.

4. **Drop the second copy of 54 sales scraped under two spellings of their address?**

   * **Problem:**
     - 54 pairs of rows share the description, sale price, ZIP code, living area and year built, while the address is spelled two ways ("270 Hames Rd SPACE 34" and "SPC 34", "1922-1924 Warren St" and "1922 Warren St"), within 500 Kaggle ids of each other.
     - The definition already keeps only the newest entry of a sale scraped twice, but it matches on the exact address, so these 54 pass.
     - Extend the rule to these pairs?
   * **Effect on the task:** no pair crosses from training into a test window, so no test price is in training. 24 pairs fall inside one test window (7, 10 and 7, newest window first) and score one sale twice. The other 30 are in the training-only half.
   * **Experiments:** found in the leak search of issue 2 on the definition's rows. 4 more groups with ids more than 500 apart are left out: they look like separate units of one development (four units at 900 S Dwight Ave at one price).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep (implemented) | 54 sales counted twice | no new rule | one sale scored twice in 24 test pairs; the rule applied by spelling |
     | B | Keep the newest of each pair | 54 rows go | the existing scraped-twice rule applied to every spelling | a rule on descriptions and facts, not on the address alone |

   * **Recommendation:** B: it is the existing rule, matched on what identifies the sale. **Decision:** A or B?

   **Notes for the AI:** on B, before the scraped-twice step, group by `Summary` (over 50 characters), `Sold Price`, `Zip`, `Total interior livable area` (missing as one value) and `Year built`. Within each group, mark the rows with two or more distinct addresses and a Kaggle id span of at most 500, and keep the newest. Assert 54 rows, extend the curation note and `changes`, and re-run `dataset check`.

   **Andrej (2026-11-11, change):** Option B: Keep the newest of each pair.

   **Resolved (2026-11-11, Andrej):** B: `_clean` keeps the newest entry of each group with the same description (over
   50 characters), sold price, ZIP code, living area and year built on two or more addresses within 600 Kaggle IDs; 54
   rows asserted. The step runs after the listing-predates-last-sale filter, as the count of 54 was made there (66
   before it), and the span is 600 IDs, not 500: the review counted steps of the shipped order, and the pair "1754
   Lebec Oaks Rd" / "1754 Lebec Rd" is 517 IDs apart. Curation note and `changes` updated; `dataset check` passes.

5. **Keep all 13 text-price drops of issue 2, now that 12 of them state an asking price?**

   * **Problem:**
     - Issue 2 described the 13 as written after the sale, but only one is ("Property has closed escrow for $1,500,000").
     - 7 state an asking price that a buyer sees before the sale ("Just reduced to $509,000", "Buy it now price - $749,000", a probate auction's minimum overbid), and 5 a loose bound ("under $500K", "comps going for more than $1M").
     - Keep the drop of all 13, or drop only the one written after the sale?
   * **Background:** the list price column holds the first asking price; a cut shows only in the text. A price known before the sale is a feature, not a leak[^5a]. Dropping a row because its text is close to its own label selects rows by the label.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Drop all 13 (implemented) | as resolved in issue 2 | a simple rule; 13 rows of 39,060 | drops 12 rows with pre-sale information, chosen by their label |
     | B | Drop only the "closed escrow" row | 12 rows return | only text written after the sale goes | a hand-picked row instead of a rule |

   * **Recommendation:** B: only one text is from after the sale. The other 12 are what a buyer reads at the listing. **Decision:** A or B?

   **Notes for the AI:** on B, replace the amount rule with the phrase "closed escrow" (and "sold for") in `Summary`, assert 1 row, and update the note and `changes`.

   [^5a]: **LEAK-10** (Must): a feature holds only what existed at the prediction point. **LEAK-37** (Must): an input the actor knows at the prediction point is not a leak.

   **Andrej (2026-11-11, change):** Option B: Drop only the "closed escrow" row.

   **Resolved (2026-11-11, Andrej):** B: the dollar-amount rule is replaced by the phrase "closed escrow" in `Summary`, 1
   row asserted; the 12 asking-price and bound texts return. "sold for" was left out of the rule: it matches 39 other
   descriptions (neighbours' sales, earlier sales, "sold for land value"). Curation note and `changes` updated;
   `dataset check` passes.

6. **Drop 5 more sales scraped twice, whose second copy has no year built?**

   * **Problem:**
     - The second leak search finds no further price leak, but 5 pairs of one sale under one address, at one price,
       with the same living area, where one copy lacks the year built (four units of 555 Fulton St, San Francisco, and
       750 Van Ness Ave #706).
     - The scraped-twice rule matches on the year built, so a missing year lets them pass, and each of these sales is
       scored twice (both copies in one test window: 4 in the middle, 1 in the newest).
     - Keep them, or keep the newest of each pair?
   * **Leak search** (38,991 rows; untuned LightGBM on each column alone, three windows, Slurm job 1377370):

     | Test | Result |
     |---|---|
     | Each column alone, on the sale-to-list ratio (what is left after the list price) | best R² 0.155 for the list price itself; every other column ≤ 0.002 |
     | Each column alone, on the log price | list price R² 0.96; then ZIP 0.52, annual tax 0.48, tax assessed value 0.47: location and the old assessment |
     | Text (TF-IDF ridge) on the ratio | R² 0.065, 0.056, -0.005; top words "auction", "short sale", "reduced": known at the listing |
     | Status written during marketing ("in escrow", "pending", "sold with multiple offers") | about 50 texts, 35 in test windows; median log(sold/list) 0.00 against 0.00: no price in them |
     | Exact copies, copies but for the price | 0, 0 |
     | Last sale, tax value within 0.5% of the price | 152 and 298 rows, as many near the list price (137, 257): no sign of the sale |

   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep (implemented) | 38,991 sales | no new rule | 5 sales scored twice |
     | B | Keep the newest of each pair | the scraped-twice rule counts a missing year built as a match; 5 rows go | the rule of issue 4 applied to a missing value | one more condition |

   * **Recommendation:** B. **Decision:** A or B?

   **Andrej (2026-11-11, discuss):** Also do a more thorough search since other more subtile leaks might be present.

   **Answer (AI, 2026-11-11):** done above: no column, text or listing field carries the sale price; the 5 pairs are the
   only finding.

   **Notes for the AI:** on B, in the scraped-twice step, match on `Address`, `Zip` and `Sold Price`, and on `Year built`
   only where both copies have it, with the same `Total interior livable area`; keep the newest; set `SAME_SALE_ROWS`
   to the new count (51 + 5, recount), update the note, `changes` and re-run `dataset check`.

7. **Split: keep the windows without a planning gap?**

   * **Problem:**
     - The windows have no gap between training and test, while a home is predicted at its listing.
     - 80-96% of each window's test homes were listed before the window began, so they meet training sales that closed
       after their listing[^7a].
     - Keep the split without a gap, or set one?
   * **Background:**
     - The windows are cut in sale order, so every training label is known when a window starts; the open point is
       only the listing as the prediction point.
     - The delay from listing to sale is long: a median of about 4,400 sales in sale order (two thirds of a window), the
       90th percentile two windows (rough, as the data has no sale dates).
     - A gap of one window leaves the oldest window 33% of the data, under the floor of half.
   * **Experiments** (LightGBM, equal training size with and without the newest training sales; Slurm job 1377452):

     | Window | Test homes listed before the window | No gap | Gap of 1/3 window | Gap of 1 window (no gap at equal size) |
     |---|---|---|---|---|
     | Newest | 96% | 0.1310 | 0.1324 | 0.1351 (0.1306) |
     | Middle | 89% | 0.1294 | 0.1348 | 0.1325 (0.1335) |
     | Oldest | 80% | 0.1327 | 0.1319 | 0.1343 (0.1357) |

     The later sales help in the newest window (up to 0.005 RMSLE), are mixed in the middle one and do not help in the
     oldest.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | No gap (implemented), the measurement in `splits_comment` | the split stays | keeps the floor and 3 windows; the effect is measured and small | test homes meet sales closed after their listing |
     | B | A gap of one window | train up to a window before each test window; windows shrink to keep the floor | closer to a model refit at the listing | smaller windows; the score moves by at most 0.005 |

   * **Recommendation:** A, and write the measurement into `splits_comment`. **Decision:** A or B?

   **Notes for the AI:** on A, replace "(not measured; the data has no sale dates)" in `splits_comment` with "(80-96% of
   each window's test homes; a gap of a third or a whole window at equal training size changes the RMSLE by -0.001 to
   +0.005, in no consistent direction, 2026-11-11)".

   **Andrej (2026-11-11, discuss):** Why is there no planning gap, can this be justified?

   **Answer (AI, 2026-11-11):** yes, now measured. The sale-order cut already keeps every training label before the
   window. What a gap would add, removing sales closed after a test home's listing, changes the score by at most 0.005
   RMSLE and in no consistent direction (table above), while a gap of the real delay breaks the floor of half.

   **Andrej (2026-11-11, discuss):** Why is there no planning gap, can this be justified?

   **Answer (AI, 2026-11-11):** the same mark on the split row, answered in two parts: what a gap would buy (above),
   and whether the newest window is selected by the outcome, since a home enters the data only once sold. It is not.

   * **How the sales are dated:** the data has no sale date, only the listing date and the Kaggle id, which is the
     sale order. For each sale we take the latest listing date among the sales up to it in the order as a lower bound
     on its sale date; the difference to its own listing date is a days-on-market proxy.
   * **The windows do not differ in the outcome** (38,991 sales; the ratio leaves out 25 sales with a list price of 0):

     | Window (sale order) | Test rows | Listed in the last 2 months of the data | Days on market (proxy), median | Sold / list, median | Mean log(sold/list) | Sold above list |
     |---|---|---|---|---|---|---|
     | Newest | 6,498 | 69% | 53 | 1.000 | -0.0103 | 45.7% |
     | Middle | 6,498 | 36% | 48 | 1.000 | -0.0052 | 47.7% |
     | Oldest | 6,498 | 1% | 47 | 1.000 | -0.0041 | 47.5% |
     | Training half | 19,497 | 0% | 46 | 1.000 | -0.0074 | 46.1% |

     Over the six sixths of the sale order the mean log(sold/list) runs -0.0004, -0.0124, -0.0093, -0.0041, -0.0052,
     -0.0103, with no trend (Spearman of the sale order with the ratio -0.009). The newest window sells slightly
     slower, not faster, than the rest.
   * **Where the censoring shows, it cancels out:** a fast sale does go with a high price (fastest quarter by the
     proxy: 73% above list, slowest quarter 17%; Spearman -0.52), and 69% of the newest window was listed in its last
     two months, which can only be there because it sold fast. Inside the newest window, the homes listed in October
     to December 2020 sold above list in 47% to 70% of cases against 10% to 20% for the homes listed in May to
     September that are still selling. The two groups balance, so the window's outcome distribution matches the
     earlier windows'.
   * **What this means for a gap:** a gap would cut the recent listings out of the test side and leave the slow
     sellers, which is the one composition the data does not mix. So the gap would not remove a selection, it would
     create one.
   * **Recommendation:** unchanged, A. Script: `~/claude_jobs/marks_b2/calif_gap/selection2.py`.

   [^7a]: **SPLIT-10** (Should): train on the rows whose outcome is known by the window's start, with a gap of about the
     label's delay; the measurements decide, and where the gap breaks the floor the departure is an exception.
     **SPLIT-14** (Must): at least 3 windows, none trained on less than half of the data.

## Reference

Kaggle
