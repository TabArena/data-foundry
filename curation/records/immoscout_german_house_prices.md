---
unique_name: immoscout_german_house_prices
name: ImmoScout24 German-House-Prices
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
tags:
- New IID
- Free Text (Short)
- 'Samples: One Moment'
collections:
- TabSTAR
original_source: Kaggle
year: '2020'
domain: business & marketing
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.openml.org/search?type=data&id=43342&sort=runs&status=active (copy, uploaded 2022-03-23)
- https://www.kaggle.com/code/shritech1404/german-housing-price-prediction (Nov 2020 notebook reading the original file)
- 'Original source is a deleted Kaggle dataset: german-house-prices, file germany_housing_data_14.07.2020.csv, owner unknown'
notebook_path: datasets/beyond_iid/new_iid/immoscout_german_house_prices/immoscout_german_house_prices.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/immoscout_german_house_prices/dataset.py
source_row: 684
type_adapter_id: curation-record-v1
---

## Comments

Missing date column, but as it represents a snapshot of data at a certain time point (when scraped) it represents live data and could be used to fit a model for other houses at the same time

Moreover, this is not sold prices (as immoscout shows only prices you can ask to buy it for and how much it was sold for AFAIK), so the snapshot here represents a task where someone would want to predict the price I should offer for my house given other houses that are currently offered. Thus, it seems like a real task where someone would want to build a model to know how much they should offer the houses at in the current market (with the limitation that past trends are ignored)

**Assessment (AI, 2026-10-14):** the data first appeared on Kaggle as the dataset `german-house-prices` (the 2020 notebook above reads `/kaggle/input/german-house-prices/germany_housing_data_14.07.2020.csv`). It is deleted and its owner could not be found, so the source stays Kaggle and the download stays the OpenML copy (43342, collection date 14-07-2020, the Kaggle card's text). The year is now 2020, the scrape date, instead of 2019.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback rmse — A scraped Kaggle dataset (since deleted) and its OpenML copy; neither defines a task or metric. RMSE on the log price is the obvious choice for price prediction.

**Assessment (AI, 2026-10-21):** metric now `Metric.from_context("rmsle", target_transform="log")` instead of the fallback rmse on the log target: an asking price's error matters relative to the price; the target still ships as log, and RMSLE is computed after the inverse, on the original scale (MET-3). Needs a rebuild to reach the container.

CC (2026-10-21, Lennart): ship the target on the modelling scale, score on the original scale (target_transform).

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): 1 ordinal scales typed as ordered categories in the codebook's order (CLEAN-14, amended): `Energy_efficiency_class` (the README lists their levels); left unordered: `Furnishing_quality` (low confidence); `Condition` (a partial order); Condition and Furnishing_quality labels are permuted in the scrape ("dilapidated": 1,137 houses, median year built 2010, the highest median price; "as new": 11, 1870, the lowest; Furnishing "refined" the oldest and cheapest); the German labels are lost, so both stay unordered with a note. Options for the curator: swap the two clear levels, neutral codes, or keep..

CC (2026-10-31, Lennart): marks on the review board of PR #37: Condition, Furnishing_quality, Type and Heating relabelled with ImmoScout24's own codes, found by matching 3,548 houses to an April 2020 scrape that keeps them (each label permuted, the missing value swapped with a real level in each column); Furnishing_quality then ordered.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `rwi_geo_red_houses_for_sale` (TBD -> Yes, priority 3). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-01, Lennart): keep this dataset as fixed in PR #37 (ImmoScout24's codes restored); the April 2020 scrape it was matched against is a new record, germany_housing_rent_and_price_apr_20, screened as a candidate to replace this one.

CC (2026-11-11, Andrej): the review page's marks of 2026-11-11 applied (review issues 1 and 2).
- Issue 1 ("Agree.", option B): one listing per house. `_clean` drops duplicates on living space, lot, year built, state, city and place (keep first): 219 listings in 105 groups are one house listed twice (0.3 to 0.5 such rows by chance; the same price in 94 groups, a different house type in 78), and 114 rows go (10,317 to 10,203). The price distribution does not move (quartiles EUR 250,000, 400,000 and 650,000 before and after; mean log price 12.877 both).
- Issue 2 ("Option B: Random, named Snapshot"): `data_tags = ("Snapshot",)` and a `Time basis:` bullet naming the scrape of 14 July 2020, the asking prices of that day and what the split cannot test (prices after July 2020). The record's collection facts stay.
- `dataset check`: 0 errors, 0 warnings, 10,203 rows.

## Review

**Outcome:** added. Houses for sale on the German portal ImmoScout24, one scrape of 14 July 2020 (a deleted Kaggle
upload, copied to OpenML): 10,317 houses with their type, areas, rooms, build and renovation years, condition,
furnishing, heating, energy certificate and place; the target is the log asking price, scored by RMSLE on the price,
with a random split. The scrape's permuted labels carry ImmoScout24's own codes since PR #37, and Lennart kept the
dataset as fixed (2026-11-01). The AI recommends shipping it, with one small clean-up: 105 houses are listed twice
(issue 1). Reviewed without a panel, from the gathered evidence (the record, the definition, a model run on the
shipped BeyondArena data, the same rows) and one check of the rows. Validity: a direct fit (an asking price set against
the houses on the market the same day); the origin is ImmoScout24, shown by matching 3,548 houses to an April 2020
scrape with the portal's codes, while the uploader is unknown; the relistings cross the split for 1.5% of test rows
and move no measured score (issue 1). Value: the benchmark methods separate (RMSE on the log price on the shipped data:
LimiX-2 0.321, TabPFN-3.5 0.338, CatBoost 0.352, linear regression 0.470 to 0.473), and a hedonic model with nested
location effects ranks 7th to 28th of 41. Quality: settled by PR #37. Weighed: a real portal snapshot, a direct fit,
16 states and wide method separation +; an anonymous uploader, an unknown licence and better data under screening -.

**Main points:** settled on 2026-11-11: one listing per house, 10,203 rows (issue 1); the random split named a
`Snapshot` of the 14 July 2020 scrape (issue 2).

**Record judgment:** valid, with a provenance caveat. The origin is ImmoScout24, but the first upload is a deleted
Kaggle dataset of an unknown owner, so the licence is OpenML's CC BY-NC-SA 4.0 and the original's is unknown; the
record says so. Two candidates for the same task are screened in their own records: the April 2020 scrape with the
portal's codes (germany_housing_rent_and_price_apr_20) and RWI-GEO-RED, ImmoScout24's documented research archive
(rwi_geo_red_houses_for_sale). Lennart kept this one as fixed until then (2026-11-01).

**Issues for Andrej:**

1. **Keep one row per house for the 105 houses listed twice?**

   * **Problem:**
     - 219 listings (2.1%) in 105 groups share living space, lot, build year, state, city and place; 89% of the groups
       have one asking price, 61 differ in one other column only, and 78 differ in the house type: one house listed
       twice, often under two types.
     - With the random split 1.5% of the test rows have their house in training[^1a].
     - Keep one listing per house, as fiat_500 keeps one per car, or keep all?
   * **Effect on the task:** a seller prices a house against other houses on the market, not against its own second
     listing; the copies give a model the answer for those rows.
   * **Experiments:** an earlier check (untuned LightGBM, 3 x 3 folds, RMSE on the log price): random split 0.3851,
     split by house 0.3854; on test rows whose house is in training 0.230 against 0.387 for the rest. A
     relisting lookup gained 0.4% (0.3466 to 0.3453) for its hedonic model.
   * **Consistency:** follows fiat_500 (one row per car, its first listing; Lennart, 2026-10-14).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep all listings (implemented) | 10,317 rows | no change; no measured effect on scores | a house on both sides of the split for 1.5% of test rows |
     | B | One listing per house | the first listing of each group stays (about 114 rows go) | no house twice; same rule as fiat_500 | a key built by us; two different houses with the same areas, year and place would merge |

   * **Recommendation:** B, one listing per house: the rule is the one fiat_500 follows and the cost is about 1% of
     the rows. **Decision:** one listing per house (B), or keep all (A)?

   **Notes for the AI:** on B, drop duplicates on `["Living_space", "Lot", "Year_built", "State", "City", "Place"]`
   (keep first) after the existing de-duplication, treating a missing build year as a value (21 rows of the groups
   have none); recount, add a curation note and update `changes`; re-run `dataset check`.

   [^1a]: **LEAK-17** (Must): repeated entities in different rows leak the target across the split even when the
     rows differ: keep one row per entity when the use case is that row, or group. **LEAK-6** (Must): measure before
     acting; a slight optimism with a known cause can stay with a note.

   **Answer (AI, 2026-11-06):**

   * **Verdict:** entity fix, copies: each group is one house listed twice, so it goes down to one row (B)[^1e1].
     - Link far above chance: 219 rows match on the six columns, against 0.3 to 0.5 by chance (one listing per house
       kept, each place's living spaces, lots and build years shuffled; at most 4 rows in 100 shuffles).
     - The price travels with the link: both listings ask the same price in 94 of the 105 groups, far closer than the
       columns explain: a model misses by 0.387 on the log scale on houses without a copy in training, and by 0.230
       on houses with one (the issue's experiments).
     - No order: one day's scrape without listing dates, and the two listings sit a median 2,798 rows apart in the
       file (none within 10 rows), so neither is the earlier one.
     - Not caught by the key: 25 more pairs of one place and build year whose living space and lot differ by 5% or
       less, 9 of them at the same price, perhaps relistings with an edited area; 0.5% of the rows, left as they are.
   * **What the drop does to the target:** 114 rows go (1.1%), the later listing of each group in file order.
     - The kept listing asks the same price as the dropped one in 100 of the 114; in the other 14 they differ by a
       median 6.7%, the dropped one higher in 6.
     - The dropped rows are dearer than average (median €487,000 against €400,000; 28, 21, 29 and 36 of them in the
       four price quarters), but the distribution does not move: quartiles €250,000, €400,000 and €650,000 before and
       after, mean log price 12.877 both, its standard deviation 0.848 before and 0.847 after.
     - **Question:** does the target still stand for the use case? The AI thinks so: a seller prices each house once,
       against the day's other houses, and the drop changes neither the price range nor its spread.
   * **Recommendation:** unchanged, B. **Decision:** one listing per house (B), or keep all (A)?

   [^1e1]: **LEAK-41** (Must; draft PR #62): repeats of a unit the data does not record get one verdict (natural,
     entity fix, temporal fix or not recoverable); copies of one record go down to one row per unit, and every drop
     gives the share dropped and the target's distribution before and after. **LEAK-42** (Should; draft PR #62):
     three tests set the verdict: a link above a chance rate that keeps the data's structure, a label that travels
     with the link beyond what the shared features predict, and an order.

   **Andrej (2026-11-11, change):** Agree.

   **Resolved (2026-11-11, Andrej):** B (agreeing with the answer of 2026-11-06): `_clean` drops duplicates on living
   space, lot, year built, state, city and place (keep first; a missing year built counts as a value) after the
   existing de-duplication; 114 rows go (10,317 to 10,203); `row` and `changes` recounted, a curation note with the
   link, the price before and after (quartiles and mean log price unchanged) and the fiat_500 precedent;
   `dataset check` re-run (see the CHANGELOG).

   **Resolved (2026-11-11, Andrej):** B, now applied on this branch: `_clean` drops duplicates on living space, lot,
   year built, state, city and place (keep first) after the existing de-duplication, 114 rows go (10,317 to 10,203);
   `row` and `changes` of the task summary follow, and a curation bullet gives the link, the chance rate, the price
   before and after and the fiat_500 precedent. `dataset check`: 0 errors, 0 warnings.

2. **Time basis: name the random split a `Snapshot` of the 14 July 2020 scrape?**

   * **Problem:**
     - Every row is a house live on ImmoScout24 on one day, 14 July 2020, with the asking price shown that day and no listing date, so the rows are one moment and none lies after another.
     - The record's collection fact fits (`Samples: One Moment`, no target tag), and the random split carries no time basis.
     - Name it a `Snapshot`, with the line below?
   * **Background:** a split that only fills in a moment the data covers is a `Snapshot`; its line names the moment,
     and no row of the same moment may carry a test row's target[^2t1]. A price was set when its house was listed,
     before the scrape, and may have been lowered since; a one-day scrape holds the houses still unsold that day, so
     houses that sit long on the market weigh more than among a period's new listings. The use case prices against
     the same day's market, which is that stock. The rows of the same moment that carry a test row's price are the
     relistings of issue 1. What the split cannot test: prices after July 2020, which RWI-GEO-RED, with listing dates,
     would.
   * **Effect on the task:** none on rows, splits or scores.
   * **Consistency:** fiat_500 is the other one-crawl listing table; its split issue carries Andrej's mark that the
     split should not be IID, and its time framing of 2026-11-06 (one moment, so no temporal split and no forced tag)
     applies here the same way.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random, no time basis (implemented) | as now | none found | the score's time meaning is not stated; `dataset check` notes the missing basis |
     | B | Random, named `Snapshot` | `data_tags` gain `Snapshot`; a `Time basis:` line names the scrape | states that every price is of one day | later prices are not tested |
     | C | Random, forced from temporal | `data_tags` gain `ForcedIIDFromTemporal`, reading the use case as pricing later listings | marks the forward reading | the amended rule gives a release of one moment a prototype, not the forced tag[^2t2] |

   * **Recommendation:** B, decided the same way as fiat_500's. **Decision:** A, B or C?

   **Notes for the AI:** once PR #50 is in, on B: `data_tags = ("Snapshot",)` (no tag is listed now) and the curation bullet "- Time basis: Snapshot: one scrape of the houses live on
   ImmoScout24 on 14 July 2020; the asking prices of that day, set at listing and possibly lowered since, without
   listing dates; the use case prices a house against the same day's market. Not tested: prices after July 2020.";
   `dataset check`. The record's facts stay.

   [^2t1]: **SPLIT-32** (Should): a definition can name the use-case prototype it follows, with a `Time basis:` line
     stating the fact. A `Snapshot` only fills in a time the data covers (one census, one scrape); its line names the
     moment, and no row of a test row's time may carry its target, else the split groups by that time unit.
   [^2t2]: **SPLIT-8** (Must; reworded 2026-11-05): a release that is one moment (one extract, one stock month, one
     exam round) is not forced; SPLIT-32 gives it `Snapshot` or `DelayedTarget`.

   **Resolved (2026-11-11, Andrej):** B: the `- Time basis: Snapshot: ...` bullet of the notes is in
   `curation_comments` (ending "Not tested: prices after July 2020."); the `Snapshot` tag enters `data_tags` once PR #50
   is in the working copy. The record's facts stay.

   **Andrej (2026-11-11, change):** Option B: Random, named Snapshot.

   **Resolved (2026-11-11, Andrej):** B, now applied on this branch, which already carries the time-basis tags:
   `data_tags = ("Snapshot",)` and the `- Time basis: Snapshot: ...` bullet in `curation_comments`, ending "Not
   tested: prices after July 2020." Rows and splits are unchanged by this issue; the record's facts stay.
   `dataset check`: 0 errors, 0 warnings.

## Reference

Kaggle / OpenML
