---
unique_name: fiat_500
name: Another-Dataset-on-used-Fiat-500-(1538-rows) / fiat_500
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: 'Yes'
tags:
- 'Samples: One Moment'
- 'Entities: Recur'
- Database Snapshot
- Non-IID (Grouped)
original_source: Kaggle
year: '2020'
collection_period: Unknown
domain: business & marketing
required_split:
- Grouped (NON-IID)
problem_type: Regression
source_links:
- https://www.openml.org/search?type=data&id=43828
- https://www.kaggle.com/datasets/paolocons/another-fiat-500-dataset-1538-rows
notebook_path: datasets/beyond_iid/old_iid/fiat_500/fiat_500.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/fiat_500/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Some guy crawled data in Fiat cars - target is to predict the price, is a self-constructed application, but useful; only time-invariant features, some spatial information

Potential issue: spatial information

Lennart: impact of spatial data can be likely ignored, otherwise dataset fits criteria even if crawled

Andrej: Is crawled data, but one could imagine people to be interested in estimating whether some cars are overpriced

**Assessment (AI, 2026-10-14):** the duplicates are not natural. Most of the 18 exact copies sit 12-14 rows after their first copy (one results page), so the crawler saw the listing twice. The same car (model, age in days, an odd km reading such as 9,248, owners) appears at up to 9 places a median 396 km apart, mostly at one price: 104 rows repeat another car (78 at the same price); among the 753 rows with a non-round km reading, 681 distinct age-km pairs, so a shared odd reading by chance is very unlikely.

CC (2026-10-14, Lennart): Keep one row per car, its first listing (1,434 rows).

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback rmse — Kaggle dataset without a competition or paper; the data card names no metric.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): left unordered: `model` (a partial order).

CC (2026-11-01, Lennart): marks on the review board of PR #37: model stays unordered (pop below lounge and sport, which are not ranked), noted in the definition.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `autoscout24_car_listings_2025` (TBD -> Yes, priority 1). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-05, Andrej): domain `business & marketing` (Review issue 5, B), in the definition and the record, as for the other asking prices listed on a website (mercari_price_suggestion, immoscout_german_house_prices, the used-car records).

CC (2026-11-17, Andrej): the declared split (random, 10x3 folds, `Retrospective`) is checked: the split decision tree, walked without the current split, reaches the split it ships (blind split walk, cross-dataset item).

CC (2026-11-26, Andrej): review issue 6, B: the split's time basis is a fill-in of one crawl, declared as `RetrospectiveFillIn` (the prototype the issue called `Snapshot`).

CC (2026-11-26, Andrej): review issue 1, C ("I go with your recommendation"): the one-row-per-car key drops the owner count (trim, engine power, age and mileage), 1,420 rows (14 fewer than with the owner count); dealers disagree on the owner count, so 8 cars stayed twice under the old key.

CC (2026-11-26, Andrej): review issue 2, A ("I keep that since it is a valid pattern in real data and not a leak"): the mileage 56,779 km stays as recorded in its 12 listings; the definition notes it.

CC (2026-11-26, Andrej): review issue 3 ("a random split that still makes sure that no car ends up on the same side of train and test", read as: no car on both sides): random splits grouped by car, `car_id` on equal engine power, age and mileage, which also joins the 14 cars whose trim two dealers entered differently; the time basis stays `RetrospectiveFillIn` (issue 6), the split leaf is the fill-in by unit.

CC (2026-11-26, Andrej): review issue 7, A (ok, as implemented): fiat_500 is kept next to craigslist_used_vehicles_f150, which tests the later market on another model; issue 4 closes with it. Verdict ship; nothing open in the review. The build is stale until rebuilt.

**Assessment (AI, 2026-11-26):** on the Kaggle file in its order, the key without the owner count keeps 1,420 of 1,538 listings (mean price 8,576 before, 8,498 after; median 9,000 and 8,900). On those rows 1,406 cars: 1,392 of one row and 14 of two, all differing only in trim (one certain copy, 39,162 km listed as pop and as sport at the same two places and prices; 3 more with an odd mileage, 10 with a round one). Under random 3-fold splits (10 repeats) 1.3% of the test rows had such a twin in training (0.39% with an odd mileage); grouped by `car_id`, none.

## Review

**Outcome:** added. Used Fiat 500s listed on the Italian site automobile.it, one crawl uploaded to Kaggle in 2020:
trim, engine power, age in days, mileage, previous owners and the seller's location; the target is the asking price,
scored by RMSE, with random splits grouped by car. The definition keeps one row per car on trim, engine power, age and
mileage (Lennart, 2026-10-14; the owner count left the key on 2026-11-26): 1,420 of 1,538 listings, and groups the 14
cars whose trim two dealers entered differently, so no car is on both sides (2026-11-26). The placeholder mileage
56,779 km stays as recorded (2026-11-26). Reviewed without a panel, from the gathered evidence (the record, the
definition, model runs on the shipped BeyondArena data and the TabArena v0.1 copy, both the 1,538 listings) and checks
of the rows. Value: the benchmark methods separate (RMSE on the shipped data: LimiX-2 686, TabPFN-3.5 695, CatBoost
730, linear regression 764 to 791), and a leak-free depreciation model with dealer effects ranks 9th of 41. Weighed:
real listings with a use case anyone can name +; one crawl of unstated date and filter, a small table, and better data
for the same task under screening -.

**Main points:** Verdict ship (2026-11-26); nothing open. Kept next to `craigslist_used_vehicles_f150` (issue 7, A; issue 4 closes with it). Issues 1 to 3 are decided (2026-11-26): the one-row-per-car key without the owner count (1, C), the
56,779 km mileage kept as recorded (2, A), and a random split grouped by car on engine power, age and mileage (3; the
time basis stays `RetrospectiveFillIn`, issue 6, B). The domain is settled (issue 5, 2026-11-05). Open: the
replacement by a dated used-car listing table (issue 4) and the better-data check of 2026-11-25 (issue 7): keep
fiat_500 until a Craigslist one-model record (Ford F-150, windows by scrape) replaces it.

**Record judgment:** valid, small, superseded soon. The crawl is real (the copies of one car at several dealers show a
live market) and the use case is direct. The definition's domain, technology & internet, follows the site; the other
price datasets of the benchmark use business & marketing, which fits the task better. A scouting run found a larger,
dated listing table (autoscout24_car_listings_2025), screened in its own record.

**Issues for Andrej:**

1. **Refine the one-row-per-car key: match odd mileages whatever the owner count, and stop merging round ones?**

   * **Problem:**
     - The definition drops a listing that repeats the trim, engine power, age, mileage and owner count of another;
       8 cars escape it because two dealers entered different owner counts, such as a lounge of 397 days with
       11,997 km at 9,999 in two cities, so 1.2% of test rows still have their car in training[^1a].
     - The same key also drops 30 listings with a mileage that is a multiple of 1,000, 14 of them at another price
       (up to 7% apart), where two different cars of the same trim and month can match by chance[^1b].
     - Match on the odd mileage alone (whatever the owners), and keep round-mileage cars unless the whole row repeats?
   * **Background:** the age is on a monthly grid and 37% of mileages are multiples of 1,000, so a round reading is
     shared by chance; an odd reading such as 11,997 km is not (Lennart's own argument on 2026-10-14: 681 distinct
     age-mileage pairs among 753 rows with an odd reading). Of the 104 listings the key drops, 74 have an odd mileage
     (61 at the same price) and 30 a round one (16 at the same price).
   * **Experiments:** model runs on the 1,538 listings: matching a test car to its copies under trim, age
     and mileage was worth 1.1% RMSE to TabPFN-3.5, and LimiX-2's whole lead over TabPFN-3.5 sat on the 11% of test rows
     with such a copy. An earlier check applied the v0.2 key to the shipped rows: 16 rows of copies remain, and under
     random 3-fold splits 1.2% of the test rows have their car in training.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Key with the owner count (implemented) | 1,434 rows | Lennart's key as decided | 8 cars stay twice; up to 14 different cars merged |
     | B | Odd mileage alone, round only as exact copies | trim, power, age and an odd mileage identify a car; round-mileage listings drop only as whole-row copies | follows the evidence that identifies a car; no copy across the split | a few more rows to explain; round-mileage copies at another dealer stay |

   * **Recommendation:** B: it applies the decision of one row per car by the evidence that identifies a car.
     **Decision:** refine the key (B), or keep it (A)?

   **Notes for the AI:** on B, drop duplicates on `["model", "engine_power", "age_in_days", "km"]` where `km % 1000
   != 0` (keep first), and on all columns where `km % 1000 == 0`; recount the rows, update the curation note and the
   task summary's `changes`, re-run `dataset check`.

   [^1a]: **LEAK-17** (Must): repeated entities in different rows leak the target across the split even when the rows
     differ: keep one row per entity when the use case is that row, or group.
   [^1b]: **LEAK-18** (Should): few features and plausible repeats are natural: keep them and say so.

   **Andrej (2026-11-04, discuss):** I don't understand what you mean. Give me numbers. How many rows are actually
   near duplicates and what would change exactly with each suggestion? Also, how could we reconstruct a grouped or
   temporal split?

   **Answer (AI, 2026-11-05):**

   * You asked how many listings are near duplicates, what each option changes in the rows, and how a grouped or a
     temporal split could be built.
   * What counts as one car: the same trim, engine power, registration month (`age_in_days` steps by month) and a
     mileage that is not a multiple of 1,000, such as 11,997 km. A round mileage such as 15,000 km can be shared by
     two cars of one month by chance. Counted on the Kaggle file in its own order (1,538 listings):

     | Kind of repeat | Groups | Listings in them | Listings a key removes |
     |---|---|---|---|
     | Exact copies (all 8 columns equal) | 15 | 33 | 18 (8 with an odd mileage, 10 with a round one) |
     | Same trim, power, month and odd mileage: one car | 43 | 125 | 82 (8 of them exact copies) |
     | Same trim, power, month, owner count and round mileage: removed by the key now | 21 | 51 | 30 (10 of them exact copies) |

   * The key now removes 104 listings: 74 of the 82 odd-mileage repeats and all 30 round ones. Left in its 1,434 rows:
     8 cars twice (two dealers gave different owner counts), 3 more if a different trim counts as the same car (such
     as a car of 39,162 km listed as pop and as sport), and 6 pairs with a round mileage.
   * The repeats come from the crawl: 42 of the 82 odd-mileage repeats sit within 15 rows of the previous copy (two
     random rows sit that close 4% of the time), and the car of 9,248 km appears every 14 or 28 rows from row 903 to row 1015, at
     nine places, always at 10,000.
   * The owner count cannot tell two cars apart. The uploader's second file of the same crawl (Kaggle, "Small dataset
     about used Fiat 500 sold in Italy", 380 listings, uploaded 2020-04-05) holds 41 of these listings with the same
     place, month, mileage and price, and gives another owner count for 25 of them (mostly 2 where this file says 1).
     That is why 8 cars escape the key.
   * Three groups:

     | Group | Listings | Key now keeps | Key without owners keeps | What it is |
     |---|---|---|---|---|
     | lounge, 397 days, 11,997 km | 5, in Milan, Florence, near Bari, Rome and Treviso, all at 9,999; owners 2, 1, 1, 1, 1 | 2 | 1 | one car at five dealers |
     | lounge, 366 days, 9,248 km | 9, at nine places, all at 10,000, owners 1 | 1 | 1 | one car, repeated every 14 rows |
     | lounge, 366 days, 15,000 km | 3 at one place at 10,500 (owners 1, 2, 1) and 1 at another place at 10,900 | 2 | 1 | one car three times; the fourth may be another car |

   * Each option on the rows, and the share of test rows whose car is in training under the benchmark's splits (3
     folds, 10 repeats). "Their car" is the same trim, power, month and odd mileage; a round-mileage twin has the same
     trim, power, month and round mileage and may be another car. So the file holds between 1,420 and 1,446 cars.

     | Option | Rows | Against the key now | Test rows with their car in training | With a round-mileage twin in training |
     |---|---|---|---|---|
     | A, key with the owner count (implemented) | 1,434 | none | 0.84% | 0.53% |
     | B, odd mileage without owners, round only as exact copies | 1,446 | 8 listings go, 20 round-mileage listings come back | 0% | 2.37% |
     | C, key without the owner count | 1,420 | the same 8 go, and 6 round-mileage listings | 0% | 0% |
     | D, odd mileage without owners, round only at the same price | 1,437 | 10 go, 13 come back | 0% | 1.56%, none at the same price |

     The issue's 1.2% was counted on the BeyondArena copy, whose rows are shuffled, with a key of month and mileage
     only; the table counts on the Kaggle file in its own order, as the definition reads it.

   * Of the 20 listings B brings back, 7 repeat a kept listing's trim, month, round mileage and price at another place,
     likely the same car again; 13 ask another price and may be other cars. B, recommended on 2026-11-04, would put
     those 7 on both sides of the split.
   * A grouped or a temporal split:
     - By car: possible, on the key above, which is built exactly from the data[^a2]. Over all 1,538 listings it keeps
       every advert and puts the copies of a car on one side; once each car is one row it is a random split. Issue 3
       measures it.
     - By seller: not possible. There is no seller id, and latitude and longitude are a geocode, often a city's centre:
       Rome's point holds 153 of the 1,420 cars, from several dealers. A split by place is possible (issue 3).
     - Temporal: not possible. There is no listing date, and the file is one crawl. Its date can be recovered: the ages
       step by the length of each month (31, 28, 31 days and so on, with 29 in February 2016), and only 1 April 2020
       fits all 140 values (31 March if a month counts from its last day). The uploader's second file gives the same
       date, so it is the same crawl, not a second one. The registration month of every car follows (July 2007 to
       April 2019), but it is the car's age, not the time of the listing. The file order is no time order either: it
       follows neither price, age, mileage nor place (rank correlations within 0.06 of zero), and the 41 listings both
       files share come in unrelated orders (0.03)[^a3].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Key with the owner count (implemented) | 1,434 rows | Lennart's key as decided | 8 cars twice; 0.84% of test rows have their car in training |
     | B | Odd mileage without owners, round only as exact copies | 1,446 rows | no odd-mileage car twice; keeps round-mileage cars that may differ | 7 listings come back that repeat a kept car's month, mileage and price |
     | C | Key without the owner count | 1,420 rows; one column leaves the key | no car twice; the smallest change; drops the field that fails | 17 round-mileage listings at another price merged (14 now) |
     | D | Odd mileage without owners, round only at the same price | 1,437 rows | no car twice; keeps round-mileage cars at another price | a rule with two cases; 1.6% of test rows meet a round-mileage twin at another price |

   * **Recommendation:** C: the owner count is the field that fails, and taking it out of the key removes every car
     seen twice with one change; the round-mileage merges stay as decided on 2026-10-14 and cost at most 17 rows, no
     leak[^a1]. **Decision:** key without the owner count (C), B, D, or keep A?

   **Notes for the AI:** on C, `subset=["model", "engine_power", "age_in_days", "km"]` in `_clean`; 1,420 rows. The 14
   listings that go beyond A are rows 93, 252, 343, 483, 584, 789, 1050, 1270, 1272, 1276, 1302, 1370, 1467 and 1470
   (0-based, Kaggle file order). Update the curation note (118 listings repeat the trim, power, age and mileage of
   another; the owner count differs for 25 of 41 listings between the uploader's two files), the task summary's `row`
   and `changes`, and re-run `dataset check`. On D: odd mileage (not 56,779) on the four columns, round mileage on the
   four plus `price`, 56,779 only as whole-row copies. All counts: the Kaggle CSV in file order, `keep="first"`; the
   overlap shares over `RepeatedKFold(3, 10, random_state=4267)`.

   [^a1]: **LEAK-17** (Must): repeated entities in different rows leak the target across the split even when the
     rows differ: keep one row per entity when the use case is that row, or group. **LEAK-18** (Should): many degrees
     of freedom and an exact match is a collection artefact: drop it; few features and plausible repeats are natural.
   [^a2]: **SPLIT-24** (Must): group on a true group id, or on one constructed exactly from the data (identical values
     in the columns that define the entity), never on a similarity-threshold cluster.
   [^a3]: **SPLIT-22** (Should): the raw file order can be the time order without a timestamp; keep it.

   **Answer (AI, 2026-11-06):** the new entity-leakage rules applied to the key; the recommendation (C) stays.

   * **Verdict: entity fix, copies of one listing on an exact key.** A repeat is one car listed by several dealers or
     crawled twice, so it goes down to one row per car; there is no time order to recover[^e1].
   * **Is the link real?** Mileages shuffled among cars of the same trim, power and half-year of age, one row per key,
     1,000 draws:
     - Odd mileages: distinct cars share trim, power, month and mileage 1.3 times per draw (at most 5), against 82
       repeats in the file.
     - Round mileages: 10.2 per draw (at most 18) against 36, so about 10 of the 36 round matches that C merges are
       likely different cars.
   * **Does the price travel with the link?** Two listings with one key and an odd mileage ask the same price in 86% of
     pairs; cars of the same trim, power and month with another mileage, in 8%. With a round mileage, 49%.
   * **Is there an order?** No: one crawl of 1 April 2020, and the file order follows no column. 42 of the 82 repeats sit
     within 15 rows of their first copy (4% of random pairs): listed or crawled together, not later.
   * **What the drop does to the price:** C removes 118 of the 1,538 listings (7.7%; 14 more than the key now), mostly
     young lounges near 10,000.
     - Dropped: median price 9,980, median age 686 days, 79% lounge; kept: 8,900, 1,066 days, 70.5% lounge.
     - Price before and after: mean 8,576 over all listings, 8,513 under the key now, 8,498 under C; median 9,000,
       8,980 and 8,900; share between 10,000 and 12,000: 24.5%, 24.1% and 23.7%.
     - Does the target still stand for the use case? The AI reads yes: the drop removes dealer stock repeated across
       dealers, a price model meets each car once, and the price spread barely moves.
   * **Recommendation:** C stays. The 10 or so different cars it merges at a round mileage (under 1% of the rows) cost
     little, and a rule that keeps round matches at another price (D) would let the target decide which rows go.

   **Notes for the AI:** the numbers come from an entity check on the Kaggle CSV in file order. The nulls run on one row per key, because the copies' repeated
   mileages re-match by themselves when the full file is shuffled. On C, the curation note adds the chance rates (82
   against 1.3, 36 against 10.2) and the price before and after.

   [^e1]: **LEAK-41** (Must; draft PR #62): repeats of a unit the data does not record get one of four verdicts:
     natural, entity fix, temporal fix or not recoverable; an entity fix takes copies of one record down to one row
     per unit, and every drop gives the target's distribution before and after and asks whether it still stands.
     **LEAK-42** (Should; draft PR #62): three tests set the verdict: a link far above a chance rate that keeps the
     data's structure (round values against odd ones), a label that travels with the link beyond what the shared
     features predict, and an order. **SPLIT-24** (Must; draft PR #62): a key built exactly from the columns that
     define the entity.

   **Andrej (2026-11-11, discuss):** Park it until we decide on checking in with better suited datasets for this task.

   **Answer (AI, 2026-11-25):** the park ends: the better-data check of 2026-11-25 asks in issue 7 of this review whether another dataset replaces this one, so this issue is open again and waits for a decision. It is written as it stood when it was parked; nothing in it was re-measured today.

   **Andrej (2026-11-26, change):** I go with your recommendation

   **Resolved (2026-11-26, Andrej):** C, the key without the owner count. `_clean` drops duplicates on trim, engine power, age and mileage (`keep="first"`): 1,420 of 1,538 listings, the 14 listings the 2026-11-05 answer named go beyond the old key's 1,434, and no car with an odd mileage is left twice under the key. The curation note gives the 118 repeats, the owner counts that differ between the uploader's two files (25 of 41), the chance rates (82 odd-mileage repeats against 1.3 per draw, 36 round ones against 10.2) and the price before and after (mean 8,576 and 8,498, median 9,000 and 8,900); the task summary's `row` and `changes` say 1,420 cars and 118 repeats.

2. **Treat the mileage 56,779 km as missing?**

   * **Problem:**
     - Twelve listings at seven sellers give exactly 56,779 km for cars from 1 to 13 years old, priced from 4,490 to
       10,900: a value typed in for an unknown reading, not a reading.
     - One seller lists three such cars at 10,900 whatever the age, including a car of 12.7 years; that one row was
       3.7% of TabPFN-3.5's squared error in model runs.
     - Set the mileage of the twelve to missing, or keep it?
   * **Background:** no other odd mileage recurs at more than one age except 14,500 (4 rows); 56,779 recurs at 11
     ages. A value that stands for "not known" becomes missing when the context shows it[^2a]; the rows stay, with
     their prices, since the price itself is what the seller asked.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep (implemented) | 56,779 stays a mileage | no change | a fake reading teaches a mileage effect that is not there |
     | B | Missing | `km` missing in 12 rows | a model sees an unknown reading as unknown | a rule on one value |
     | C | Drop the rows | the 12 listings go | no fake reading at all | loses real asking prices for a missing input |

   * **Recommendation:** B, the mileage is unknown and the asking prices are real. **Decision:** missing (B), keep
     (A), or drop (C)?

   **Notes for the AI:** on B, `df.loc[df["km"] == 56779, "km"] = np.nan` in `_clean` after the de-duplication, and a
   curation note with the counts.

   [^2a]: **CLEAN-10** (Should): convert proxy missing values to real missing values when the encoding can be
     inferred from the description and the context.

   **Andrej (2026-11-04, discuss):** Where exactly does this come from? Maybe because it is temporal data but not
   properly defined?

   **Answer (AI, 2026-11-05):**

   * You asked where 56,779 km comes from, and whether it is a time quantity that was defined badly.
   * In this file: 12 listings at 7 places, spread over the file (rows 124 to 1132, so not one broken results page):
     4 at Rome's city point, 3 at one seller near Mantua (45.25 N, 10.67 E), and one each near Venice, Pescara, Padua,
     Treviso and west of Turin. Their trims, engine power and owner counts look like any other row's.
   * In the uploader's other file of the same crawl (Kaggle, "Small dataset about used Fiat 500 sold in Italy", 380
     listings, uploaded 2020-04-05): 11 listings with 56,779 km at 8 places, 3 of them the same adverts as here. Seven
     are cars 91 days old asking 10,950 to 15,900, the prices of nearly new cars: 56,779 km in three months would be
     228,000 km a year.
   * No date or time mix-up: the ages of the 12 lie on the same monthly registration grid as every other row's, so
     their dates are intact; read as days, 56,779 is 155 years, read as a spreadsheet date it is June 2055; and the
     same number stands for cars of 1.2 to 12.8 years. Nor is it an average the uploader filled in: the mean mileage is
     53,396 km in this file, 102,196 in the other and 63,065 over both (medians 39,031, 112,000 and 49,038).
   * The prices say the hidden readings are not typical: 10 of the 12 ask more than the median price for their age, 6
     more than the 90th percentile. The seller near Mantua asks 10,900 for three such cars of 1.8, 4.1 and 12.8 years
     (other cars of 12.8 years ask 3,900 to 5,000), while its two cars with a reading ask 9,100: a template more than a
     priced car.
   * So it is one fixed number written where an advert gave no mileage, by the crawler or by the uploader before the
     two files were cut from the crawl (it is in both). Which of the two cannot be shown: no crawler code is published,
     and neither data card nor the uploader's five notebooks on these files mention it. It means "not known".
   * Measured on issue 1's rows (key without the owner count, 1,420 rows; 3 folds x 10 repeats, RMSE): with the 12 set
     to missing, untuned LightGBM moves from 784.6 to 783.8, a random forest from 775.6 to 775.3, ridge regression
     from 776.5 to 769.0.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep (implemented) | 56,779 stays a mileage | no change | a stand-in teaches a mileage effect that is not there |
     | B | Missing | `km` missing in 12 rows | an unknown reading is read as unknown | a rule on one value |
     | C | Drop the rows | the 12 listings go | no stand-in at all | loses 12 real asking prices for a missing input |
     | D | Missing, and drop the seller's three template listings | `km` missing in 9 rows; the 3 listings at 10,900 near Mantua go | no listing whose price is a template too | a rule on one seller; the prices for 1.8 and 4.1 years are plausible |

   * **Recommendation:** B, as before: an impossible value becomes missing and the row stays, and a row leaves only
     when it is no task row[^b1]; a template price is shown only for the 12.8-year car. **Decision:** missing (B), D,
     keep (A) or drop (C)?

   **Notes for the AI:** on D, drop rows with `km == 56779` at latitude 45.251308, longitude 10.6687 (raw rows 936,
   1020 and 1034) before setting the rest to missing. The other file: Kaggle
   `paolocons/small-dataset-about-used-fiat-500-sold-in-italy`, `Used_fiat_500_in_Italy_dataset.csv` (engine power in
   horsepower, a transmission column, two queries each sorted by price).

   [^b1]: **CLEAN-11** (Should): impossible values become missing, and the row stays; a row leaves only when it is no
     task row or a copy. **CLEAN-10** (Should): convert proxy missing values to real missing values when the encoding
     can be inferred from the description and the context.

   **Andrej (2026-11-11, discuss):** Park it until we decide on checking in with better suited datasets for this task.

   **Answer (AI, 2026-11-25):** the park ends: the better-data check of 2026-11-25 asks in issue 7 of this review whether another dataset replaces this one, so this issue is open again and waits for a decision. It is written as it stood when it was parked; nothing in it was re-measured today.

   **Andrej (2026-11-26, change):** I keep that since it is a valid pattern in real data and not a leak

   **Resolved (2026-11-26, Andrej):** A, kept as recorded (the implemented option): all 12 listings with 56,779 km stay with that mileage under issue 1's key. `dataset.py` changes only by a curation note that keeps the value and says what it likely stands for.

3. **Which split instead of IID? Mark the random split as forced from temporal?**

   * **Problem:**
     - The definition splits the cars at random, standing for new listings in the same market, and Andrej asks for a
       split that is not IID.
     - The file is one crawl of 1 April 2020 with no listing date and no seller id, so no temporal split can be built,
       and the grouped splits it allows either equal a random split once each car is one row (by car) or test a task
       other than pricing a new listing (by place, by registration month).
     - Keep the random split and mark it as forced from temporal, or split by place, by car or by registration month?
   * **Background:**
     - A split mirrors the real use, and a non-IID split is either grouped, on a key built exactly from the data, or
       temporal, on a time index[^3a]. An asking price set against the market is temporal by its use: a model trained
       on today's listings prices tomorrow's, after prices have moved[^3b].
     - A release without dates ships in the closest regime that keeps the rows, marked as forced from temporal, and
       only when a leak test across the split finds nothing: no row sharing its outcome with the other side, no
       hidden group, no order dependence[^3c].
     - What the file holds (issue 1's answer): one crawl, dated by the monthly grid of the ages; each car's
       registration month; latitude and longitude, often a city's centre (Rome's point holds 153 of 1,420 cars, from
       several dealers; 230 places hold one listing each); and copies of a car, which issue 1 removes.
     - A place is in every new listing, so it is a feature a model may use, not a group to hold out[^3d].
   * **Effect on the task:** a random split over one crawl scores a model on pricing a car against the market of the
     same day. It cannot show how prices move after the crawl, which only a dated listing table can test (issue 4).
   * **Experiments:** untuned LightGBM, a random forest (300 trees) and ridge regression (one-hot trim, scaled
     numbers), RMSE in the price's unit (the mean as a baseline: about 1,960). Random and grouped splits are 3 folds x
     10 repeats; the windows are 3 expanding windows whose training side holds 50% to 84% of the rows, each compared
     with the random folds' predictions for the same test rows.

     | Split | Rows | LightGBM | Random forest | Ridge | Test rows with a twin / their place in training |
     |---|---|---|---|---|---|
     | Random, all listings (as shipped in BeyondArena) | 1,538 | 761 | 747 | 765 | 9.8% / 81% |
     | Random, key now (implemented) | 1,434 | 779 | 773 | 775 | 1.4% / 79% |
     | Random, key without owners (issue 1, C) | 1,420 | 785 | 776 | 777 | 0% / 78% |
     | Grouped by car, all listings | 1,538 | 775 | 762 | 765 | 0% / 80% |
     | Grouped by place (exact latitude and longitude) | 1,420 | 840 | 822 | 784 | 0% / 0% |
     | Windows by registration month, youngest cars last (same rows at random) | 1,420 | 802 (563) | 799 (572) | 641 (634) | not applicable |
     | Windows by file position (same rows at random) | 1,420 | 841 (813) | 836 (808) | 830 (829) | not applicable |

     - A twin is a training listing with the same trim, power, month and mileage. Grouping by car over all listings
       costs the tree models what the copies gave them (14 to 15 RMSE) and ridge nothing.
     - Grouping by place costs the tree models 6% to 7% and ridge 1%, so the ranking turns to the linear model: the
       score then measures a seller nobody has seen.
     - Windows by registration month ask the tree models to price cars younger than any in training: about 40% worse
       than at random on the same rows, ridge 1%.
     - The leak test of the random split: no car on both sides after issue 1; no order dependence (the random folds'
       residuals in file order: lag-1 correlation 0.03, no trend over the ten tenths of the file; ridge scores the
       same on windows by file position as at random); no hidden group, as the place is a feature.
   * **Consistency:**
     - mobile_churn and the other churn snapshots (one undated extract each) ship random, marked as forced from
       temporal, and porto_seguro gets the same mark (2026-11-04, Andrej): B follows them.
     - immoscout_german_house_prices, the other one-day snapshot of asking prices, ships random without the mark; under
       B it should get the mark too.
     - The dated price tables (house_sales, ames_housing, perth_house_prices, melbourne_housing_market, zillow_prize,
       california_house_prices_2020) split in time; a dated used-car listing table would too.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random (implemented) | 3 folds x 10 repeats over the cars | prices a car against the same day's market, the use case | not marked as a stand-in for a temporal split |
     | B | Random, marked forced from temporal | as A, with the data tag `ForcedIIDFromTemporal` and a split note: one crawl of 1 April 2020, no listing dates | says what the score stands for; follows mobile_churn and porto_seguro; the leak test finds nothing | still no test on later listings |
     | C | Grouped by place | each place on one side; LightGBM 840 against 785 at random | tests a seller or a city not seen | a new listing's place is known; Rome's point mixes dealers; turns the ranking to the linear model |
     | D | Grouped by car, all listings | every advert kept, the copies of a car on one side; LightGBM 775 | no listing dropped | a car counts as often as it was advertised; issue 1 does the same with one row per car |
     | E | Windows by registration month | train on older cars, test on the youngest | uses the only date the data hold | tests younger cars, not later listings; tree models about 40% worse |

   * **Recommendation:** B: the data allow no temporal split and no grouping that matches pricing a new listing, so the
     random split is the closest regime, and the mark says so; a temporal split needs a dated listing table (issue 4).
     **Decision:** random marked as forced from temporal (B), random as now (A), grouped by place (C), grouped by car
     (D), or windows by registration month (E)?

   **Notes for the AI:** on B, `data_tags = ("ForcedIIDFromTemporal",)`, as in mobile_churn (the data hold latitude
   and longitude, so `"Spatial"` belongs there too, which the definition lacks); a split note in `curation_comments` in
   mobile_churn's form (a deployed model prices new listings against the current market; one crawl, dated 1 April 2020
   or 31 March by the age grid; no listing dates; the leak test above; a dated release would allow a temporal split),
   the task summary's `split`, then `dataset check`. The record's `required_split` stays `Random (IID)`. Setup of the
   numbers: the Kaggle CSV in file order; LightGBM 4.7 defaults; scikit-learn 1.9 `RandomForestRegressor(300)` and
   `Ridge(1.0)` with median imputation and scaling; `RepeatedKFold(3, 10, random_state=4267)` and
   `GroupKFold(3, shuffle=True, random_state=4267 + repeat)`; windows cut at 50%, 67% and 83% of the rows (ties of a
   month kept together).

   [^3a]: **SPLIT-1** (Must): the split mirrors the real-world application. **SPLIT-2** (Must): IID, temporal (a time
     index, test after train) or grouped (a group index, each group on one side). **SPLIT-24** (Must): group on a true
     id or one constructed exactly from the data.
   [^3b]: **SPLIT-6** (Must): a fixed predictive task that only needs a temporal split (a delivery time, a default, a
     sale price) gets a temporal split. **SPLIT-7** (Must): a missing or hidden timestamp does not make a task IID.
   [^3c]: **SPLIT-8** (Must): a task temporal in nature or by its use case whose release cannot give the windows
     (one extract with no dates at all) ships in the closest regime that keeps the rows, tagged as forced from
     temporal; a forced split ships only when a leak test across the split finds none. Cases: mobile_churn,
     account_debt_south_africa.
   [^3d]: **SPLIT-4** (Must): if new rows keep having the value, the column is a feature and the split stays.

   **Andrej (2026-11-04, change):** This should not be IID.

   **Answer (AI, 2026-11-06):** The time framing: one crawl gives no temporal split and, under the amended rules, no
   forced tag, so random cars named a `Snapshot` in issue 6 (a), or grouped by place (c) or registration-month windows
   (e) if the split must not be IID?

   * **Problem:**
     - Every listing is read at one crawl (1 April 2020 by the age grid), with no posting date, and the asking price is part of the listing, so the file holds one moment and no listing lies after another.
     - Since 2026-11-05 the split rules give a release of one moment a use-case prototype, here `Snapshot`, not the forced tag, so B's tag moves to issue 6[^3ta].
     - Your mark asks for a split that is not IID: in this file time cannot give one, and the splits left that are not IID test an unseen seller (C) or younger cars (E), not a later market.
   * **Background:** a later market is what a forward use case needs, and only a dated listing table tests it
     (issue 4); within this crawl, a random split prices a car against the same day's market, which is the
     snapshot's use case.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Random cars (A), named in issue 6 | 3 folds x 10 repeats over the cars; the time basis names the crawl | prices a car against the same day's market | does not test a later market |
     | c | Grouped by place (C) | as above | a split that is not IID | a new listing's place is known; tests an unseen seller; LightGBM 840 against 785 |
     | e | Windows by registration month (E) | as above | uses the only date the data hold | tests younger cars, not later listings; tree models about 40% worse |

   * **Recommendation:** a, with the forward test left to a dated listing table (issue 4). **Decision:** a, c or e?

   [^3ta]: **SPLIT-8** (Must; reworded 2026-11-05): a release that is one moment (one extract, one stock month, one
     exam round) is not forced; SPLIT-32 gives it `Snapshot` or `DelayedTarget`. **SPLIT-32** (Should): a `Snapshot`
     fills in a time the data covers, such as one scrape.

   **Andrej (2026-11-11, discuss):** Park it until we decide on checking in with better suited datasets for this task.

   **Answer (AI, 2026-11-25):** the park ends: the better-data check of 2026-11-25 asks in issue 7 of this review whether another dataset replaces this one, so this issue is open again and waits for a decision. It is written as it stood when it was parked; nothing in it was re-measured today.

   **Andrej (2026-11-26, change):** I would say that what we need here would be a random split that still makes sure that no car ends up on the same side of train and test.

   **Resolved (2026-11-26, Andrej):** a random split grouped by car, so no car is on both sides; the time basis stays `RetrospectiveFillIn` (issue 6). After issue 1's key, 14 cars still have two rows, all differing only in the trim a dealer entered: a car of 701 days and 39,162 km is listed as pop and as sport at the same two places and prices, and 13 more pairs share engine power, age and mileage (3 odd mileages, one of them 56,779 km, and 10 round ones). So the plain random split did not satisfy the note: 1.3% of its test rows had such a twin in training (0.39% with an odd mileage). `_clean` adds `car_id`, the group number of engine power, age and mileage (1,406 cars: 1,392 of one row, 14 of two), declared as `grouping` (per-row labels and predictions, no model input) with a `splits_comment`; `split_leaf` moves from the random fill-in to the fill-in by unit; the record's `required_split` is `Grouped (NON-IID)` with the tag `Non-IID (Grouped)`. `dataset check`: 0 errors, 0 warnings, 1 info (the grouping is not clustered: the car pairs are too few to show, which is expected when 14 of 1,406 cars have two rows); 1,420 rows, 1,406 groups, 3 folds x 10 repeats, 468 to 478 test rows (468 or 469 cars) per fold.

4. **Better data for the same task: keep fiat_500 until a used-car listing table replaces it?**

   * **Problem:**
     - The better-data check (a larger or newer public table with the same target, use case and kind of features) ran
       for this record on 2026-10-30/31 and found `autoscout24_car_listings_2025`, and five more used-car listing
       tables are screened as candidates, none of them checked by a curator or added.
     - Read today, the AutoScout24 file holds 118,382 listings of November 2025 in eight countries (21,658 used cars in
       Italy) but of a few makes (BMW, Porsche, Mercedes-Benz, Audi, Alfa Romeo, Suzuki and Volvo are 96% of the rows,
       no Fiat), and no listing date.
     - Keep fiat_500 until one of these tables is added and then retire it as replaced, keep it as it is, retire it
       now, or keep both?
   * **Background:**
     - The check is screening's search for better data: a hit becomes its own record and is screened; the old record
       keeps the verdict its own data earn, and the curator decides which enters[^4a]. A valid task stays until
       then[^4b].
     - fiat_500 against such tables: one model of one brand, 7 features, 1,420 cars, one crawl of 1 April 2020 with an
       unstated filter (no car under a year old, while the uploader's other file has cars from three months) and 12
       stand-in mileages. It is the only used-car price table of the benchmark.
     - The candidates, all screened `TBD -> Yes` from their data cards and not yet verified:

       | Record | Data | Adds over fiat_500 | Split it allows | Concerns |
       |---|---|---|---|---|
       | autoscout24_car_listings_2025 (priority 1) | 118,382 listings, AutoScout24, 8 countries, 8 November 2025 | 25 makes, about 80 columns (version, registration date, fuel, gearbox, equipment, accident and service history), a listing id | random over one snapshot, or grouped by seller (its name is in the data) | a few makes only; personal fields to drop; a net price computed from the target |
       | dvm_car_uk_used_car_adverts (priority 3) | over 250,000 UK adverts, DVM-CAR (IEEE Big Data 2022, figshare DOI) | a documented dataset with each advert's year and month | temporal | CC BY 4.0 on figshare, CC BY-NC on the project page; platforms not named |
       | us_used_cars_cargurus (priority 1) | 3 million US listings, CarGurus, September 2020 | listing date, 66 columns with history flags | temporal by listing date | research-only terms; 10 GB; undocumented crawler |
       | used_cars_pakistan, pakwheels_used_cars_2022, used_cars_saudi_arabia (priorities 1, 2 and 1) | 72,655 (PakWheels, 2021), about 90,000 (PakWheels, 2022) and 8,035 (syarah.com, 2021) listings | more rows and fields; a last-updated date in the 2022 file | random; possibly temporal for the 2022 file | other markets; scrapes |

   * **Effect on the task:** none on this definition. A replacement keeps the use case (an asking price from the advert)
     on a newer and richer table; only a dated one (DVM-CAR, CarGurus) gives the temporal split that issue 3 cannot.
   * **Experiments:** the AutoScout24 file was read for its markets, makes, ids and dates (the counts above; the file
     was not kept). The other candidates rest on their records, not their files.
   * **Consistency:** body_density_prediction is the same case, kept until nhanes_dxa_body_fat is added and then
     retired as replaced (recommended on 2026-11-04, open). The scouting run found better data for five of the eight
     price tables, so the choice applies to the family.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep (implemented) | fiat_500 ships; the candidates are screened in their own records | the record keeps the verdict its data earn | the small one-model crawl ships with no plan to replace it |
     | B | Keep until replaced | fiat_500 ships; once a used-car listing table is added, it is retired as replaced | the task stays in the benchmark meanwhile; a dated replacement gives the temporal split | waits for a candidate to be verified and added |
     | C | Retire now | `No (Retired)`; the folder leaves the working copy | no small one-model crawl in the benchmark | no used-car price task until a candidate is added |
     | D | Keep both | fiat_500 stays next to the replacement | a small-data case next to a large one | one use case twice |

   * **Recommendation:** B, with DVM-CAR screened first: it is documented and dated, so it gives the temporal split
     asked for under issue 3, while AutoScout24 holds a few makes only. **Decision:** keep until replaced (B), keep (A),
     retire now (C) or keep both (D)?

   **Notes for the AI:** on B, a dated CC line in the record ("keep until a used-car listing table is accepted, then
   retire as replaced"); when one is accepted, retire this one (`No (Retired)`, folder removed, CHANGELOG entry). The
   AutoScout24 record calls the file all brands: it holds 25 makes, 96% of the rows from seven of them, and no Fiat;
   118,382 unique listing ids, 40,222 rows with a VIN (37,578 distinct); registration dates by month; correct its
   Assessment at its next screening. Counts from the Kaggle file `autoscout24_dataset_20251108.csv` (columns
   `country_code`, `make`, `is_used`, `id`, `vin`, `registration_date`), read on 2026-11-05.

   [^4a]: Pattern "Small or dated, and the task is still done today" (selection.md): a larger or newer public dataset
     with the same target and use case, and features of the same kind; a hit from another source is its own record,
     not a `Duplicate`; the old record is not rejected automatically and keeps the verdict its own data earn. Cases:
     body_density_prediction, hepatitis_c_egypt.
   [^4b]: **TP-6** (Must): keep two questions apart: is the task valid, and is it the best version? A valid task stays.

   **Andrej (2026-11-04, discuss):** I can't believe there is no better dataset for this. We have a check, apply it.

   **Andrej (2026-11-05, discuss):** Is there a used car dataset that also targets one particular type of car and allows
   for getting the temporal component right? For the use case as outlined, we would need to make sure that all the
   included cars are from one time snapshot, possbly multiple sites, and possibly included past cars from other
   snapshots, but with a time component still. Can we find something better for this task or is this dataset already
   good if we fix duplicates?

   **Answer (AI, 2026-11-05):**

   * You asked for asking prices of one car model with a time component (listing dates or repeated scrapes, so that a
     model trained on earlier listings is tested on a later scrape, from one or several sites), and whether fiat_500
     is good enough once its duplicates are fixed.
   * One public table meets all three, though from a single site: the Craigslist used-vehicle scrapes. Their uploader
     scraped every US car listing on Craigslist again every few months and kept each scrape as a version of one Kaggle
     dataset (CC0, scraper code on GitHub). The nine versions read here run from October 2019 to May 2021, about one a
     quarter, plus one of October 2026. Filtered to one model, the Ford F-150, each scrape holds 6,600 to 13,400
     distinct trucks (5,700 in 2026), and the listings of two scrapes do not overlap, except for two scrapes taken two
     weeks apart. Windows by scrape meet the rule of three windows, each training on more than half the rows[^c1].
   * DVM-CAR, which this issue recommended screening first, does not give a temporal split: all 16,132 of its adverts
     created in 2020 and 2021 are cars registered in 2019, against 108 such cars among the earlier 252,123 adverts. A
     split by advert date there tests a new registration year, not a later market[^c2]. Its Fiat 500 subset (2,770
     UK adverts) is the same car as fiat_500, but without trim, place or owner count.
   * The candidates, downloaded and counted on 2026-11-05 except the CarGurus crawl of 2020 (licences noted only[^c5]):

     | Dataset | One model: rows | Dates and span | Sites | Licence | Temporal split? |
     |---|---|---|---|---|---|
     | Craigslist used vehicles (Kaggle, 11 versions) | Ford F-150: 6,600 to 13,400 trucks per scrape; Honda Civic: 4,400 to 6,100 listings | one scrape per version, about every three months from October 2019 to May 2021, and October 2026; a posting date in three versions, each spanning about the month before its scrape | Craigslist, all US regions | CC0 | yes, by scrape |
     | Illinois dealer listings (Kaggle sample of the data vendor AutoDealerData.com) | Toyota Camry: 8,246 cars; Ford F-150: 17,798; Fiat 500: 350 | first and last day each car was seen, daily, June 2018 to May 2020 | about 1,200 dealer websites | CC BY-NC-SA 4.0 | yes, by quarter; but the mileage is 0 in 49% of used-car rows |
     | DVM-CAR adverts (Huang et al. 2022) | Fiat 500: 2,770 adverts | month the advert was created: 2,395 up to 2019 (99% from 2017 to August 2018), 375 in 2020 and 2021, all cars of 2019 | UK platforms, not named | CC BY 4.0 on figshare, CC BY-NC in the paper | no: the later adverts are one registration year, and within 2017-2018 one monthly window passes the rule |
     | otomoto.pl, two scrapes (Kaggle, 2021 and 2023) | VW Golf: 3,849 and 3,745; Fiat 500: 454 and 541 | date of publication: 93% from 26 April to 5 May 2021, 99% from 10 to 23 April 2023 | otomoto.pl (Poland) | CC0; CC BY-SA 4.0 | two time points from two scrapers with different columns (25 and 243) |
     | eBay-Kleinanzeigen 2016 (Kaggle copies; the first upload is gone) | VW Golf: 28,821; Fiat 500: 909 | ad created and crawled, 5 March to 7 April 2016 | one site (Germany) | CC0 on a copy | only within five weeks; mileage in 13 bins, 65% at the cap of 150,000 km |
     | European used-car market (Kaggle sample of a data vendor) | Fiat 500: 15,308, of them 5,375 in Italy | first seen by the vendor's crawler, 20 September to 15 October 2026 | AutoScout24, mobile.de, Marktplaats, willhaben and two more | CC BY-NC-SA 4.0 | no: one crawl (93% of the Italian Fiat 500s first seen from 9 to 11 October) |
     | CarGurus US 2020 (record us_used_cars_cargurus) | not counted: 10 GB, not downloaded | listing date, one crawl of September 2020 | CarGurus | research use only | perhaps, by listing date within one crawl |

   * Not usable for this task: the daily CarGurus sample on Kaggle hides the price ("[PREMIUM]" in all 30,000 rows);
     the Malaysian daily snapshots (July to October 2026) hold 13,683 adverts of all makes; Toyota Corolla (1,436
     cars, Netherlands) and Fiat Egea (997, Turkey) are one model without dates; AutoScout24 2025 has no Fiat and no
     listing date; "10 Million Used Car Listings" is synthetic by its uploader's own words; and the 2.7 million
     Chilean adverts scraped weekly from 2020 to 2023 were not released, only price indices built from them (Diaz and
     Lefort 2025).
   * What the time component changes, on the Craigslist F-150:
     - The median asking price of comparable trucks (model years 2013 to 2015, 60,000 to 120,000 miles) falls from
       22,999 (October 2019) to 20,900 (June 2020) and rises to 26,700 (May 2021): 28% in eleven months, while the
       trucks age.
     - Untuned LightGBM trained on all earlier scrapes and tested on the next one (September 2020, December 2020,
       April-May 2021) scores RMSE 6,207, 5,509 and 6,510; on the same trucks, a random split over all scrapes scores
       5,094, 4,826 and 5,708, and a random split within the one scrape 5,092, 4,900 and 5,183. So a model used
       after prices have moved errs 12% to 26% more than a split within one scrape, such as fiat_500's, shows.
   * What the Craigslist table lacks against fiat_500: one site and the US market; fields typed in by the poster (the
     trim only inside the model name, 600 to 900 spellings per scrape; the condition; the mileage); 5% to 10% of F-150
     rows priced 0 or a placeholder such as 12345; no owner count; 1% to 38% of a scrape's VINs listed in an earlier
     scrape (50% for the scrape taken two weeks after another), so a relisted truck brings its earlier price into
     training, as a dealer would know it[^c6]; the posting text to drop (73% of the F-150 texts of May 2021 hold a
     phone number).
   * fiat_500 with issue 1's key (1,420 cars) is good for the one-day task: each car once, no car on both sides of the
     split, and issue 3's leak test finds nothing. It can only ship as one snapshot, the random split marked forced
     from temporal (issue 3, B)[^c3]: it holds one crawl of 1 April 2020 without listing dates, and the uploader's
     other file is the same crawl, so no fix dates it. It scores pricing a car against the same day's market, not
     after prices have moved.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Keep fiat_500, fixed (implemented) | ships with issues 1 to 3 applied (1,420 cars, random split marked forced from temporal); no other record | keeps the verdict its data earn; nothing to wait for | no used-car task tests a later market |
     | b | Keep fiat_500 until a Craigslist record replaces it | a new record for the Craigslist scrapes filtered to one model, split by scrape; once it is added, fiat_500 is retired as replaced | the temporal test asked for, on one model over 2019 to 2021; one used-car task in the benchmark | another market and typed-in fields to clean; one site |
     | c | Keep both | as b, and fiat_500 stays | a small one-day case next to a large dated one | one use case twice, the older one without the temporal test |
     | d | Replace with DVM-CAR's Fiat 500 | 2,770 UK adverts, split by the month of the advert | the same car; a dataset paper with a DOI | the later adverts are one registration year; no trim, place or owner count |
     | e | Keep fiat_500 until an Illinois dealer record replaces it | as b with the Illinois dealer listings of one model, split by quarter | daily dates over two years; dealer listings with a hashed VIN | the mileage missing in about half the rows; Camry prices flat over the span; a vendor's sample |

   * **Recommendation:** b: the Craigslist scrapes give the split by time that fiat_500 cannot, on one model, from a
     public source with its scraper published, and fiat_500 stays valid until they are added and checked[^c4]. It is
     this issue's B with the replacement named, and the Craigslist table takes DVM-CAR's place as the first candidate.
     **Decision:** keep fiat_500 until a Craigslist record replaces it (b), keep fiat_500 alone (a), keep both (c),
     DVM-CAR's Fiat 500 (d) or the Illinois dealers (e)?

   **Notes for the AI:** records to create and screen (none exists): `craigslist_used_vehicles` (Kaggle
   `austinreese/craigslist-carstrucks-data`; a version downloads as `austinreese/craigslist-carstrucks-data/<N>` with
   the Kaggle CLI; read here: versions 2 and 4 to 11, uploaded 2019-10-14, 2020-01-07, 2020-03-22, 2020-06-17,
   2020-09-16, 2020-12-03, 2021-04-20, 2021-05-06 and 2026-11-05; `posting_date` only in 8, 10 and 11; version 2 has
   the model in `make` and the place in `city`; versions 9 and 10 share 27% of their listing ids; Zenodo record
   10457828 is someone else's CC BY 4.0 copy of one version) and `illinois_dealer_listings` (Kaggle
   `cisautomotiveapi/large-car-dataset`, 5,695,015 rows; `msrp` equals `askPrice` in 55% of used rows, drop it; 68% of
   VINs appear at more than one dealer id, keep one row per VIN). F-150 filter: `manufacturer == "ford"`
   and the model matching `^f-?150`, price 1,000 to 150,000, one row per VIN, then repeats of year, odometer, price and
   region dropped: 13,347, 12,882, 13,445, 10,308, 6,616, 8,967, 8,295 and 8,293 trucks in versions 2 and 4 to 10.
   Baseline: LightGBM 4.7, 400 trees, learning rate 0.05, 63 leaves, on the log price, features year, odometer,
   latitude, longitude, condition, cylinders, fuel, title, transmission, drive, size, type, colour, region and the
   first word after "f-150"; versions 9 and 10 merged into one window; random split `RepeatedKFold(3, 3,
   random_state=4267)`. On b: a dated CC line in this record naming `craigslist_used_vehicles` as the replacement. The
   DVM-CAR record (`dvm_car_uk_used_car_adverts`) needs at its next screening: the 2020-2021 adverts are 2019
   registrations only; figshare's API states CC BY 4.0 for version 2, the paper (Section IV) CC BY-NC; figshare's
   download was refused from this machine, the counts come from the Kaggle copy `mexwell/dvm-car`
   (`Ad_table (extra).csv`, 268,255 adverts, the same advert ids as `Ad_table.csv`).

   [^c1]: **SPLIT-14** (Must): a temporal task has at least 3 windows, and no window's train side holds less than
     50% of the data; each window trains on what is known before it starts.
   [^c2]: **SPLIT-8** (Must): a release with a few cohort months of one base cannot give windows; a split by those
     months tests a change of cohort, not of time. References: Huang, J., Chen, B., Luo, L., Yue, S. and Ounis, I.,
     "DVM-CAR: A large-scale automotive dataset for visual marketing research and applications", IEEE International
     Conference on Big Data 2022, pp. 4130-4137, doi:10.1109/BigData55660.2022.10020634 (arXiv:2109.00881); Table II
     defines `Adv_year` and `Adv_month` as the advertisement's creation year and month.
   [^c3]: **SPLIT-8** (Must): a task temporal by its use case whose release cannot give the windows ships in the
     closest regime that keeps the rows, tagged as forced from temporal, once a leak test across the split finds none;
     say what a dated window would change.
   [^c4]: Pattern "Small or dated, and the task is still done today" (selection.md): a hit from another source is its
     own record; the old record keeps the verdict its own data earn, and the curator decides which one enters.
     **TP-6** (Must): keep two questions apart: is the task valid, and is it the best version? A valid task stays.
   [^c5]: **EV-4** (Must): a licence or redistribution terms are a one-line note, never the reason for a verdict.
     Reference for the Chilean adverts: Diaz, F. and Lefort, F., Data and codes for "Analyzing Price Efficiency Using
     Machine Learning Generated Price Indices: the Case of the Chilean Used Car Market", Mendeley Data, V1, 2025,
     doi:10.17632/jxby8pkww5.1.
   [^c6]: **SPLIT-13** (Should): an entity that recurs across the cutoff is part of the task when the model predicts
     for known entities, and a question when the use case is a new entity.

   **Deferred (2026-11-11):** parked on Andrej's note ("Park it until we decide on checking in with better suited datasets for this task.").

   **Note (AI, 2026-11-25):** the question moved to issue 7 of this review, which restates it with the candidates checked on their files on 2026-11-25; this issue stays parked and that one carries the decision.

   **Resolved (2026-11-26, Andrej):** closed by issue 7, A: fiat_500 is kept and ships next to the Craigslist F-150 record.

5. **Domain: `technology & internet`, or `business & marketing` as the other listing prices?**

   * **Problem:**
     - Andrej's field mark of 2026-11-04 takes the definition's `domain`, `technology & internet`, which follows the
       website the listings were crawled from.
     - Asking prices listed on a website are `business & marketing` everywhere else in the benchmark: mercari_price_suggestion
       (shipped), immoscout_german_house_prices (a portal crawl), california_house_prices_2020, and every used-car record
       (autoscout24_car_listings_2025, dvm_car_uk_used_car_adverts, pakwheels_used_cars_2022, us_used_cars_cargurus, the
       used_cars_* records).
     - Take `technology & internet`, or change the definition so that the record follows?
   * **Background:** the domains are kept one per family of siblings (Lennart, 2026-10-21, the ten QSAR records), and a
     record takes its definition's value (Lennart, 2026-10-26, aeolus). The same question is open for miami_housing
     (`finance` against the house prices' `business & marketing`, its issue 2).
   * **Effect on the task:** none on the data; the domain groups the datasets in the benchmark's summaries.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | `technology & internet` (the field mark) | the definition and the record say `technology & internet` | the record follows the definition | the only listing price outside `business & marketing` |
     | B | `business & marketing` | the definition's `domain` changes, the record follows | one domain for asking prices | a definition edit |
     | C | Move the marketplace siblings to `technology & internet` | mercari_price_suggestion and immoscout_german_house_prices change too | a domain by where the data was crawled | more records and definitions change |

   * **Recommendation:** B: nothing sets fiat_500 apart from the other listing prices. **Decision:** A, B or C?

   **Notes for the AI:** the record's `domain` was left empty until this is decided; `problem_type` is set
   (Regression). On B: `domain = "business & marketing"` in `dataset.py` and the record, `dataset check`.

   **Andrej (2026-11-05, change):** I choose B

   **Resolved (2026-11-05, Andrej):** `business & marketing` (B), in `dataset.py` and the record, as the other listing
   prices; `dataset check` 0 errors, 0 warnings.

6. **Time basis: name the split a `Snapshot` of one crawl?**

   * **Problem:**
     - Every listing was read at one crawl of automobile.it (1 April 2020 by the age grid), the asking price exists with the listing, and the age counts to the crawl, so the rows are one moment.
     - The record's collection fact fits (`Samples: One Moment`, no target tag), and the split carries no time basis.
     - Name it a `Snapshot`, whichever split issue 3 settles?
   * **Background:** a split that only fills in a moment the data covers is a `Snapshot`; its line names the moment,
     and no row of the same moment may carry a test row's target[^6t1]. The listings were posted on unrecorded
     earlier dates, so a price may predate the crawl or have been revised before it; the release shows only the price
     at the crawl. The rows of the same moment that carry a test row's price are a car's copies at other dealers,
     which issue 1 removes. The forward use case, pricing a listing after prices have moved, is not tested, which is
     issue 4's dated table.
   * **Effect on the task:** none on rows, splits or scores.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | No time basis (implemented) | as now | none found | the score's time meaning is not stated; `dataset check` notes the missing basis |
     | B | Named `Snapshot` | `data_tags` gain `Snapshot` (and `Spatial`, as issue 3's notes say); a `Time basis:` line names the crawl | states that every price is of one moment | a later market is not tested |
     | C | Forced from temporal (issue 3's B) | `data_tags` gain `ForcedIIDFromTemporal` | marks the forward use case | the amended rule gives a release of one moment a prototype, not the forced tag[^6t2] |

   * **Recommendation:** B. **Decision:** A, B or C?

   **Notes for the AI:** on B: `data_tags = ("Spatial", "Snapshot")` (no tag is listed now; under
   issue 3's C the grouping adds the regime tags itself) and the curation bullet "- Time basis: Snapshot: one crawl of
   automobile.it, uploaded to Kaggle on 2020-04-07 (1 April 2020 by the monthly grid of the ages); no posting or crawl
   date in the file; the asking price is part of the listing, read with the trim, power, age to the crawl, mileage,
   owners and place; the use case prices a car against the same day's market. Not tested: a later market (a dated
   listing table would)."; `dataset check`. The record's facts stay.

   [^6t1]: **SPLIT-32** (Should): a definition can name the use-case prototype it follows, with a `Time basis:` line
     stating the fact. A `Snapshot` only fills in a time the data covers (one census, one scrape); its line names the
     moment, and no row of a test row's time may carry its target, else the split groups by that time unit.
   [^6t2]: **SPLIT-8** (Must; reworded 2026-11-05): a release that is one moment (one extract, one stock month, one
     exam round) is not forced; SPLIT-32 gives it `Snapshot` or `DelayedTarget`.

   **Andrej (2026-11-11, discuss):** Park it until we decide on checking in with better suited datasets for this task.

   **Answer (AI, 2026-11-25):** the park ends: the better-data check of 2026-11-25 asks in issue 7 of this review whether another dataset replaces this one, so this issue is open again and waits for a decision. It is written as it stood when it was parked; nothing in it was re-measured today.

   **Andrej (2026-11-26, change):** Option B: Named Snapshot.

   **Resolved (2026-11-26, Andrej):** B, the split is named as a fill-in of one crawl. The rules renamed the `Snapshot` prototype `RetrospectiveFillIn` after this issue was written, and the definition already declares it (`time_basis = TimeBasis("RetrospectiveFillIn", ...)`, one crawl of listings published on Kaggle in 2020, crawl date not stated, a later market not tested), so nothing changed in the definition.

7. **Keep fiat_500 until a Craigslist Ford F-150 record (split by scrape) replaces it, or keep it as it is?**

   * **Problem:**
     - With the placeholder prices and the relisted trucks taken out, untuned LightGBM trained on earlier Craigslist scrapes and tested on the next F-150 scrape still errs 15% to 25% more than a random split within that scrape, so the time component the curator asked for survives both concerns.
     - fiat_500 is one crawl of 1 April 2020 (1,420 cars with the refined one-row-per-car key, 1,434 as defined), so it can only test pricing against the same day's market.
     - Keep fiat_500 until a Craigslist F-150 record replaces it, keep it as it is, keep both, or retire it now?
   * **Background:**
     - The curator asked on 2026-11-05 for one car model, a time component (a later scrape tested on a model trained on earlier ones) and one or several sites. The answer of 2026-11-05 (fiat_500 issue 4) compared eight used-car tables, downloaded and counted, and recommended keeping fiat_500 until a Craigslist one-model record replaces it; its table and numbers stand and are not repeated here beyond the summary below.
     - Left open then: whether a European dated multi-scrape table of one model exists, and whether the Craigslist pick survives its placeholder prices (5% to 10% of raw F-150 rows) and its relisted VINs (1% to 38% of a scrape's VINs seen before).
     - Candidates, with the verdicts of 2026-11-05 kept and the new ones added:

       | Candidate | One model: rows | Time component | Sites | Licence | Verdict |
       |---|---|---|---|---|---|
       | Craigslist used vehicles (Kaggle austinreese/craigslist-carstrucks-data, 11 versions) | Ford F-150: 6,600 to 13,400 trucks per scrape, 78,955 over 2019-2021 | one scrape about every three months, October 2019 to May 2021, plus October 2026 | Craigslist, all US regions | CC0 | better: the only table with the asked-for time component on one model; checked again below |
       | European Used Cars: 670k Sold Listings (Kaggle automarketapicom, new in this check) | Fiat 500 family 7,507 (plain 500: 4,453; Italy 1,204) | first seen 20 September to 11 October 2026 (three weeks); 44% of rows delisted the moment they were first seen | 97% AutoScout24, 3% mobile.de | CC BY-NC-SA 4.0 | not better: one three-week crawl of the vendor already rejected on 2026-11-05, no later market to test |
       | Egyptian Automotive Market (Kaggle shamsfathalla, new in this check, from its data card) | not counted: 13.7 GB with images | a monthly price history of model averages, not of listings | five Egyptian sites | CC BY-NC 4.0 | not better: the history is aggregated, and the used-car file carries model price averages as features |
       | Illinois dealer listings (2026-11-05) | Ford F-150 17,798; Fiat 500 350 | first and last day seen, June 2018 to May 2020 | about 1,200 dealer sites | CC BY-NC-SA 4.0 | not better: mileage 0 in 49% of used-car rows |
       | DVM-CAR UK adverts (2026-11-05) | Fiat 500 2,770 | advert month; the later adverts are 2019 registrations only | UK platforms, not named | CC BY 4.0 / CC BY-NC | not better: a split by advert month tests a new registration year |
       | otomoto.pl 2021 and 2023, eBay-Kleinanzeigen 2016, European 2M listings, Malaysian daily snapshots, AutoScout24 2025, CarGurus 2020 (2026-11-05) | see issue 4 | two scrapes from two scrapers, five weeks, one crawl, all makes, no date, or not downloaded (10 GB) | | | not better (reasons in issue 4) |

     - A short search of Kaggle on 2026-11-25 (used-car snapshots, daily or weekly scrapes, AutoScout24, mobile.de, Fiat 500, Craigslist) found no other dated multi-scrape table of one model from European sites.
   * **Effect on the task:** none on this definition. The replacement keeps the use case (an asking price from the advert) and adds the later-market test; it moves the task to the US market, one site, and typed-in fields.
   * **Experiments:** on the F-150 table built on 2026-11-05 (versions 2 and 4 to 10, the two scrapes two weeks apart merged into one window; one row per VIN and per year, mileage, price and region within a scrape), run on 2026-11-25. Untuned LightGBM (400 trees, learning rate 0.05, 63 leaves) and a ridge regression on the log price; RMSE in dollars.

     - What the cleaning leaves: the price filter of 1,000 to 150,000 already removes the zero and one-dollar placeholders. Left in the table: 341 of 78,955 rows (0.4%) with a sequence or repeated-digit price (12345, 99999, 11111) or under 5,000 for a 2015 or newer truck (a down payment posted as the price). Relisted: 5,236 rows (6.6%) carry a VIN seen in an earlier scrape; only 47.5% of rows carry a VIN at all.

     | Variant | Test scrape | Test trucks | GBM, earlier scrapes → this one | GBM, random within this scrape | Gap | Linear, earlier → this one |
     |---|---|---|---|---|---|---|
     | as on 2026-11-05 | Sep 2020 | 6,616 | 6,207 | 5,092 | +22% | 7,215 |
     | as on 2026-11-05 | Dec 2020 | 8,967 | 5,509 | 4,900 | +12% | 7,013 |
     | as on 2026-11-05 | Apr-May 2021 | 13,390 | 6,510 | 5,183 | +26% | 7,208 |
     | placeholders dropped | Sep 2020 | 6,577 | 5,942 | 4,781 | +24% | 7,057 |
     | placeholders dropped | Dec 2020 | 8,927 | 5,185 | 4,479 | +16% | 6,787 |
     | placeholders dropped | Apr-May 2021 | 13,335 | 6,323 | 5,003 | +26% | 7,072 |
     | placeholders and relisted VINs dropped | Sep 2020 | 6,449 | 5,944 | 4,794 | +24% | 7,143 |
     | placeholders and relisted VINs dropped | Dec 2020 | 8,472 | 5,110 | 4,428 | +15% | 6,823 |
     | placeholders and relisted VINs dropped | Apr-May 2021 | 12,952 | 6,308 | 5,043 | +25% | 7,109 |

     - Relisted trucks are priced better than fresh ones in two of three windows, so an earlier listing works as a near-copy:

     | Test scrape | Relisted test trucks | GBM RMSE, relisted | GBM RMSE, fresh |
     |---|---|---|---|
     | Sep 2020 | 128 | 4,190 | 6,241 |
     | Dec 2020 | 455 | 5,614 | 5,504 |
     | Apr-May 2021 | 383 | 4,934 | 6,551 |

     - The tree model beats the linear one by 10% to 25% in every window, so the task separates methods. Scripts and log: the run's evidence folder, out/f150_1411437.log (and the 2026-11-05 evidence in the run's evidence folder).
   * **Consistency:** body_density_prediction takes the same decision in this batch (keep until nhanes_dxa_body_fat is added, then retire as replaced); both follow the pattern that a better dataset is its own record and the old one keeps the verdict its own data earn[^better].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep as is (implemented) | fiat_500 ships; no replacement planned | keeps the verdict its own data earn; nothing to wait for | no used-car task tests a later market |
     | B | Keep until a Craigslist F-150 record replaces it | a new record for the Craigslist scrapes filtered to the F-150, windows by scrape; fiat_500 retired as replaced once it is accepted | the later-market test asked for, on one model over 2019 to 2021; one used-car task in the benchmark | the US market and one site; typed-in fields to clean; waits for the new record |
     | C | Keep both | as B, and fiat_500 stays | a small one-day case next to a large dated one | one use case twice, the older one without the time test |
     | D | Retire now | No (Retired), folder removed | no small one-crawl table | no used-car price task until the Craigslist record is added |

   * **Recommendation:** B: it restates the answer of 2026-11-05. No newer table meets the ask better, and the Craigslist pick survives its two concerns: the placeholders left after the price filter are 0.4% of rows, and with them and the relisted trucks dropped the later-market gap stays at 15% to 25%. fiat_500 stays valid until the replacement is checked and accepted[^valid]. **Decision:** A, B, C or D?

   **Notes for the AI:** On B: a dated CC line in fiat_500's record naming `craigslist_used_vehicles_f150` (or the name the record gets) as the replacement; when it is accepted, fiat_500 becomes No (Retired), folder removed, CHANGELOG entry. Create and screen the new record (none exists): Kaggle austinreese/craigslist-carstrucks-data, versions via `kaggle datasets download austinreese/craigslist-carstrucks-data/<N>`; versions 2 and 4 to 10 (uploaded 2019-10-14 to 2021-05-06) and 11 (2026-11-05, a five-year gap that would be a further window); posting_date only in 8, 10 and 11; version 2 has the model in `make` and the place in `city`. Filter as in the run's evidence folder (manufacturer ford, model `^f-?150`, price 1,000 to 150,000, one row per VIN within a scrape, repeats of year, odometer, price and region dropped); merge versions 9 and 10 into one window. Two questions for that record's own review: drop the 341 sequence or down-payment prices (minimal preprocessing: they separate for non-target reasons), and whether a truck relisted across the cutoff stays (a dealer knows its earlier price[^entity]) or is dropped. Drop the posting text (phone numbers), url, id, VIN and image fields. The cleaning flags are in f150_sens.py (`placeholder`, `relisted`). The European sold-listings file read here: Kaggle automarketapicom/european-used-cars-sold-days-on-market, european_used_cars_sold_days_on_market.parquet, 679,148 rows, read on 2026-11-25.

   [^better]: Pattern "Small or dated, and the task is still done today": a larger or newer public dataset with the same target and use case is its own record; the old record is not rejected automatically and keeps the verdict its own data earn until the curator decides.
   [^valid]: Keep two questions apart (TP-6): is the task valid, and is it the best version? A valid task stays.
   [^entity]: SPLIT-13: an entity that recurs across the cutoff is part of the task when the model predicts for known entities, and a question when the use case is a new entity.

   **Andrej (2026-11-26, ok):** As implemented (A).

   **Resolved (2026-11-26, Andrej):** A: fiat_500 ships as it is, next to `craigslist_used_vehicles_f150`, judged on its own data: after issues 1 to 3 it holds one row per car and is split grouped by car, and its 1,420 Italian listings of one model test another size, market and split than the 97,291 US F-150 listings split by scrape. Issue 4 (the same question, 2026-11-05) closes with it. No definition change.

## Reference

https://www.kaggle.com/datasets/paolocons/another-fiat-500-dataset-1538-rows
