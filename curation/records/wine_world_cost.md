---
unique_name: wine_world_cost
name: wine_cost
checked_by:
- Lennart
- Alex
- Mustafa
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
tags:
- New IID
- Free Text (Sentences)
- 'Samples: One Moment'
collections:
- TexTabBench
- STRABLE
original_source: Kaggle
year: '2023'
domain: business & marketing
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/elvinrustam/wine-dataset
notebook_path: datasets/beyond_iid/new_iid/wine_world_cost/wine_world_cost.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/wine_world_cost/dataset.py
source_row: 682
type_adapter_id: curation-record-v1
---

## Comments

Need to check description for leakage; need to preprocess price; need to preprocess capacity; make secondary grape a description?; fix/normalize by unit; think about multi-cat column like characteristics; filter to per bottle price, make percentage a percentage, handle double year and parse to be number/date

Scraped from the web

**Assessment (AI, 2026-10-14):** the description check asked above is done. No description states the wine's own price (one quotes a stale price of the same wine, 17 compare with other wines). R² over the 9 splits: all text and tabular columns 0.724; with every sentence holding price or value words removed 0.721; everything except the description 0.700. The shop is most likely Majestic Wine (UK): 78 descriptions and 18 titles name it.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback rmse — scraped Kaggle dataset with no competition, paper or stated metric.

**Assessment (AI, 2026-10-21):** metric now `Metric.from_context("rmsle", target_transform="log")` instead of the fallback rmse on the log target: a bottle price's error matters relative to the price; the target still ships as log, and RMSLE is computed after the inverse, on the original scale (MET-3). Needs a rebuild to reach the container.

CC (2026-10-21, Lennart): ship the target on the modelling scale, score on the original scale (target_transform).

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `alko_wine_price_list` (TBD -> Yes, priority 2). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-10, Andrej): review page marks: the shop's sales copy stays as part of the task, fit approximate (issue 1, option B: `fit_reason` names the copy written for priced wines and the unnamed shop); the whisky and the tequila (ABV 30% or more) are dropped, 1,277 wines (issue 2, ok, B); the random split is named `Snapshot` of the 2023 scrape (issue 3, B; the `Time basis:` bullet is in `curation_comments`, the tag enters `data_tags` once PR #50 is in the working copy); the sentence quoting "Majestic Loves Rose 2019"'s own earlier price (£5.99) is removed from its description (issue 4, B).

CC (2026-11-11, Andrej): record field set from the definition (review page field mark): `original_source` Kaggle (was Other).

CC (2026-11-11, Andrej): split grouped by producer (review page issue 5, a, the issue's C), random before. The data have no producer column: a `Producer` key is read from the title by a rule and two hand-made tables fix what the rule gets wrong; all 1,277 titles were checked by hand. Brands, ranges and second wines join their house when the title or the shop's copy names it as their maker; the shop's own-label ranges are one group each; 613 producers. `required_split` Grouped (NON-IID) (was Random (IID)). Grouping costs every model 0.03 to 0.04 RMSLE (TabPFN-3.5 0.345 to 0.375). Use case reassessment opened as issue 6.

CC (2026-11-11, Andrej): use case reframed (review page issue 6, B): the actor is a producer or importer estimating the UK shelf price of a wine it offers, or a buyer judging whether a wine is good value, not the shop, which prices from its costs (supplier price, duty, VAT, margin) that the data do not hold. `use_case` and `question` rewritten; `fit_reason` adds that the model stands for someone who does not know the price (fit stays approximate; its price-tier numbers moved to `curation_comments`); the grouping definition and the split bullet name the new actor. Text only, data unchanged.

## Review

**Outcome:** added. The AI recommends shipping it after two small changes (issues 1 and 2). Reviewed on 2026-11-04
without a panel, from the evidence already gathered (the record, Andrej's dispute of Lennart's `Yes` on 2026-10-15
with its column ablations, a model run on the shipped data). The data are 1,279 wines sold by the bottle in a
UK online wine shop, scraped in 2023 and uploaded to Kaggle by Elvin Rustamov ("Wine Dataset", source given as "From
Internet"; most likely Majestic Wine, which 78 descriptions and 18 titles name); the target is the bottle price in
pounds, shipped as its log and scored by RMSLE on the price. Validity: the shop's description is sales copy written
for a wine the shop had already priced; it never states the price, but its wording follows the price tier, so it is
text written together with the label, which the curation rules keep as part of the task (as for
coffee_rating_prediction), and the fit should then read approximate (issue 1); two rows are spirits, not wine
(issue 2). Value: the benchmark methods spread on the shipped splits (RMSE on the log price 0.327 for LimiX-2, 0.353 for
TabPFN-3.5, 0.379 for tuned gradient boosting, 0.41 to 0.46 for linear regression), and the text adds a real +0.09 R²
over the tabular columns. Quality: 67 rows are 30 wines in other sizes or vintages; a split that keeps each product
family on one side lowers R² only from 0.741 to 0.733. Weighed: methods separate and the text carries real signal +,
an unnamed shop and an uploader's own licence -, one shop at one time -, better data may exist (Alko's price list,
not screened yet) -.

**Main points:** Issues 1 to 4 settled (2026-11-10): the shop's copy stays with an approximate fit (1), the two spirits are dropped (2), the random split is named a `Snapshot` of the 2023 scrape (3), and the sentence quoting a wine's own earlier price is removed (4). Record `original_source` set to Kaggle (2026-11-11). Split settled (2026-11-11): grouped by a hand-checked producer key, 613 producers (5). Use case reframed (2026-11-11): a producer, importer or buyer estimating the UK shelf price of a wine not on the list, not the shop, which prices from its costs (6). No open issues.

**Record judgment:** valid, ship after the changes. Andrej disputed Lennart's `Yes` on 2026-10-15; his strongest
points were the licence and provenance of scraped shop copy and that the copy is written for wines already priced. The
licence is a note, not a reason to retire or a decision here: the uploader marks the data CC0, which the uploader
cannot grant for a retailer's sales copy. The provenance is a known gap, not an unknown source: the first upload is
named and the shop can be read off the text. The use-case point is issue 1. The data-scouting run of 2026-10-30/31
found `alko_wine_price_list` (the Finnish monopoly's catalogue, about 7,600 wines) as better data for the same task;
it is screened in its own record and does not change this verdict. The record has no `CC (...)` line yet; its undated
to-do notes are done.

**Issues for Andrej:**

1. **Keep the shop's sales copy as part of the task, and call the fit approximate?**

   * **Problem:**
     - The title and description are the shop's own sales copy, written for a wine it had already priced, and their wording follows the price tier without naming the price.
     - The definition calls the fit direct, as if a merchant pricing a newly listed wine had this copy before setting the price.
     - Keep the copy with an approximate fit, keep it as it is, drop the description, or retire the dataset?
   * **Background:** copy with "value", "favourite", "exclusive" or "we" has median prices of £13 to £15, copy that
     names "Parker" (an influential wine critic), "points" (critic scores) or "premier cru" (a top vineyard
     classification) £31 to £48, against £17 overall. Text written together with the label stays part of the task
     when it does not map one to one onto the target[^1a]. The uploader names no shop, but the first upload is known
     and the shop can be read off the text; such a source stays, and the gap is stated as an approximate fit[^1b].
   * **Effect on the task:** a model partly reads the shop's own pricing decision from its copy; a merchant pricing a
     new listing would have the buyer's tasting note and the wine's attributes, not the finished marketing text.
   * **Experiments:** an earlier check (2026-10-15; ridge regression on TF-IDF of the text plus one-hot categories,
     random 3 folds x 10, mean R² on log price): all columns 0.741, no text 0.651, title only 0.629, description only
     0.522, size, ABV and vintage only 0.319. Removing every sentence with price or value words changes R² by 0.003
     (record, 2026-10-14), so no description gives the price away. The benchmark methods on the shipped
     splits (10 x 3): RMSE 0.327 (LimiX-2), 0.353 (TabPFN-3.5), 0.379 (tuned gradient boosting), 0.413 to 0.463
     (linear regression); a hand-built kernel ridge on the catalogue plus a producer-range term ranks 3 of 41 (0.331).
   * **Consistency:** follows coffee_rating_prediction, whose reviewer text, written with the score, is kept with an
     approximate fit. Lennart marked three other wine-price sets (`wina_poland`, `winevivino`, `wine_rating_price`)
     `No Good Target (yet)`; they are other tables and set no precedent for this one.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Copy kept, fit direct (implemented) | no change | none found | overstates the use case: the copy follows the pricing; the unnamed shop is not stated as a gap |
     | B | Copy kept, fit approximate | `fit` and `fit_reason` name the copy written for priced wines and the unnamed shop | keeps the text task the data offers (+0.09 R²); the gap is stated; as coffee | the score includes reading the shop's positioning words |
     | C | Drop `Description` | catalogue columns, title and grapes only | closer to what a buyer's listing sheet holds | loses most of the text task; the title still carries producer and range words |
     | D | Retire | record `No (Retired)`, folder removed | no scraped shop copy in the benchmark | loses a small text-and-table task on which methods separate |

   * **Recommendation:** B: the copy never states the price and adds real signal, so it stays as the task, and the
     fit names the two gaps the data has. **Decision:** copy kept with an approximate fit (B), as is (A), description
     dropped (C), or retire (D)?

   **Notes for the AI:** on B, set `fit="approximate"` and a `fit_reason` such as "The title and description are the
   shop's sales copy, written for wines it had already priced: they never state the price, but their wording follows
   the price tier (value wording at a median £13-15, critic and cru wording at £31-48). The shop is not named by the
   uploader (most likely Majestic Wine); one shop's range at one time." Add a `CC (2026-11-04, Andrej):` line to the
   record with the decision.

   [^1a]: **LEAK-35** (Must): text written together with the label is the task when it does not map one to one onto
     the score; coffee_rating_prediction's review text is its case.
   [^1b]: **PROV-2** (Should): an upload whose first platform cannot be traced is kept, case by case, when the data
     looks sound and there is a source to point to; the gap is written as an approximate fit (**USE-8**, Must).

   **Andrej (2026-11-11, change):** Option B: Copy kept, fit approximate.

   **Resolved (2026-11-10, Andrej):** B: `fit="approximate"` with the drafted `fit_reason` (sales copy written for
   priced wines, its wording following the price tier, the shop not named); a curation bullet says why the copy stays;
   a CC line in the record.

2. **Drop the whisky and the tequila?**

   * **Problem:**
     - Two of the 1,279 rows are spirits, not wine: a 12-year-old single malt whisky and a tequila, both at 30% alcohol or more.
     - Their prices follow other rules than a wine's, and the task predicts the price of a bottle of wine.
   * **Background:** the alcohol-free wines (three at 0.5% and two at 0.0%) and about 25 fortified wines (sherries,
     Madeiras, a Marsala) are wine products the shop prices on the same shelf, and stay either way.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep (implemented) | no change | no rows lost | two rows outside the task's population |
     | B | Drop the two spirits | rows with ABV of 30% or more dropped in `_clean` (1,277 rows) | every row is a wine | none found |

   * **Recommendation:** B, the rows are not the product the task prices. **Decision:** keep (A) or drop (B)?

   **Notes for the AI:** on B, drop `df["ABV%"] >= 30` in `_clean` after parsing ABV, check that exactly the whisky
   and the tequila go, add a curation note, re-run `dataset check`, and note the change in the CHANGELOG.

   **Resolved (2026-11-10, Andrej):** B: `_clean` drops the rows with ABV 30% or more after parsing ABV, exactly the
   Macallan Sherry Oak 12 Year Old and VIVIR Tequila Blanco (1,277 wines); a curation bullet and the task summary's row
   count follow. `dataset check` re-run.

3. **Time basis: name the random split a `Snapshot` of the 2023 scrape?**

   * **Problem:**
     - Every row is a wine at one scrape of a UK shop's range in 2023, with its shelf price and the shop's copy of that moment, so the rows share one moment and none lies after another.
     - The record's collection fact fits (`Samples: One Moment`, no target tag), and the random split carries no time basis.
     - Name it a `Snapshot`, with the line below?
   * **Background:** a split that only fills in a moment the data covers is a `Snapshot`; its line names the moment,
     and no row of the same moment may carry a test row's target[^3t1]. The vintage is a wine's attribute, not a time.
     The copy was written before the scrape, once at another price (issue 4). The rows of the same moment closest to a
     test wine are the 30 wines in other sizes or vintages (67 rows); a split that keeps each family on one side moves
     R² only from 0.741 to 0.733. What the split cannot test: prices after 2023.
   * **Effect on the task:** none on rows, splits or scores.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random, no time basis (implemented) | as now | none found | the score's time meaning is not stated; `dataset check` notes the missing basis |
     | B | Random, named `Snapshot` | `data_tags` gain `Snapshot`; a `Time basis:` line names the scrape | states that every price is of one moment | later prices are not tested |
     | C | Random, forced from temporal | `data_tags` gain `ForcedIIDFromTemporal`, reading the use case as pricing wines listed later | marks the forward reading | the amended rule gives a release of one moment a prototype, not the forced tag[^3t2] |

   * **Recommendation:** B. **Decision:** A, B or C?

   **Notes for the AI:** once PR #50 is in, on B: `data_tags = ("Snapshot",)` (no tag is listed now) and the curation
   bullet "- Time basis: Snapshot: one scrape of a UK online wine shop's range (most likely Majestic Wine) in 2023;
   the shelf prices, sales copy and catalogue attributes of that moment; the vintage is a wine attribute, not a time.
   Not tested: prices after 2023."; `dataset check`. The record's facts stay.

   [^3t1]: **SPLIT-32** (Should): a definition can name the use-case prototype it follows, with a `Time basis:` line
     stating the fact. A `Snapshot` only fills in a time the data covers (one census, one scrape); its line names the
     moment, and no row of a test row's time may carry its target, else the split groups by that time unit.
   [^3t2]: **SPLIT-8** (Must; reworded 2026-11-05): a release that is one moment (one extract, one stock month, one
     exam round) is not forced; SPLIT-32 gives it `Snapshot` or `DelayedTarget`.

   **Andrej (2026-11-11, change):** Option B: Random, named Snapshot.

   **Resolved (2026-11-10, Andrej):** B: the drafted `Time basis: Snapshot:` bullet is in `curation_comments`, ending
   with what the split cannot test (prices after 2023). Split and record facts unchanged; `Snapshot` enters `data_tags`
   once PR #50 is in the working copy.

   **Resolved (2026-11-11, Andrej):** the tag is set: this branch's framework carries PR #50, so
   `data_tags = ("Snapshot",)` now stands in the definition beside the `Time basis:` bullet; `dataset check`
   passes (0 errors, 0 warnings).

4. **Remove the one sentence that quotes the wine's own earlier price?**

   * **Problem:**
     - The description of "Majestic Loves Rose 2019" (shelf price £6.99) opens with "Our mission was to find the best tasting wines at £5.99", the range's earlier price, so this one row states its own price within a pound.
     - The definition's note says that no description states the wine's own price, and issue 1 rests on the copy never naming it.
     - Remove the sentence, or keep the row as published and correct the note?
   * **Background:** 14 descriptions name a price in pounds; the other 13 name other wines' prices (a neighbour's
     £50 a bottle, a sister wine's £660), positioning copy that issue 1 keeps as the task. A part or another encoding
     of the target is out of the features, and the smallest fix keeps the rest of the text[^4t1]. The record's
     assessment of 2026-10-14 saw the row ("one quotes a stale price of the same wine"), but the note did not keep it.
   * **Effect on the task:** one row of 1,279; a method that reads the text can take the number.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep (implemented) | as now | the copy as published | one row states its own earlier price; the note says no row does |
     | B | Remove the sentence | the sentence goes from that one description; the note names the row | no description states its wine's price | an edit of the shop's text |
     | C | Keep, correct the note | the note names the row | the copy as published; the note true | one row keeps its price in the text |

   * **Recommendation:** B, the smallest fix of a stated price. **Decision:** A, B or C?

   **Notes for the AI:** on B, in `_clean` after the parsing, remove "Our mission was to find the best tasting wines at
   £5.99." from the `Description` of the row titled "Majestic Loves Rose 2019" (check that exactly one row changes),
   and replace the curation note "No description states the wine's own price." by one that names the removed sentence;
   on C, only the note; `dataset check`, a CHANGELOG entry. Data: the Kaggle file `WineDataset.csv`.

   [^4t1]: **LEAK-10** (Must): a feature never gives the target away; out are a part, a consequence or another
     encoding of the target. **LEAK-7** (Should): the smallest fix that keeps a valid signal beats dropping the
     column. **LEAK-35** (Must): text written together with the label is the task when it does not map one to one
     onto the score.

   **Andrej (2026-11-11, change):** Option B: Remove the sentence.

   **Resolved (2026-11-10, Andrej):** B: `_clean` removes "Our mission was to find the best tasting wines at £5.99."
   from the one description that holds it ("Majestic Loves Rose 2019", asserted to be exactly one row), and the curation
   note "No description states the wine's own price." is replaced by one that names the removed sentence. `dataset
   check` re-run.

5. **Split: group the wines by producer, to price a wine from a producer the shop does not list yet?**

   * **Problem:**
     - The data hold no listing date or order, so no split forward in time can be built and the random split is a `Snapshot` (issue 3).
     - A random split already tests unseen wines, but 49% of its test wines have a wine of the same producer in training.
     - Group by producer to test a wine from a producer the shop does not list yet, or by another key?

   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random (implemented) | as now, `Snapshot` | no constructed key | half the test wines have their producer in training |
     | B | Grouped by product family | the title without vintage and size as the group | an exact key from the data; a new vintage or size is never tested against its own wine | changes almost nothing (+0.003) |
     | C | Grouped by producer | a `Producer` key read from the title, hand-checked, as the group; `Time basis: Snapshot` stays | tests the listing of a wine from a new producer, the harder case of the real use | a constructed key to check by hand; a new wine of a known producer is tested as if the producer were new |
     | D | Newer vintages tested | train on older vintages, test the newer | looks forward | vintage is no listing time; the third window breaks the 50% floor |

   * **Recommendation:** C: the closest real-world use the data can test is a wine from a producer the shop does not list yet, and it costs every model 0.013 to 0.025 RMSLE; prices after 2023 stay untested. **Decision:** random (A), product family (B), producer (C) or newer vintages (D)?

   **Andrej (2026-11-10, discuss):** I don't think the task in the real world would be iid random, what can we do to make it closer to the real world?

   **Answer (AI, 2026-11-11):**
   - The data hold no listing date and no listing order: the raw order is the shop's default sort, best sellers first (The Guv'nor, Oyster Bay, Whispering Angel). A forward split in time cannot be built; issue 3's `Snapshot` stays.
   - The real use is pricing a wine new to the shop's list. A random split already tests unseen wines: only 4% of the test wines have the same wine in another size or vintage in training.
   - What it does not hold out is the producer: under the random split 49% of the test wines have a wine of the same producer in training. A new listing often comes from a producer the shop does not sell yet.
   - Grouping by producer (786 producers, 215 with more than one wine) raises the error by 0.013 to 0.025 RMSLE for all three models; the order of the models stays.
   - The data have no producer column. The key used here is read from the title by a rule (the words before the quoted cuvée name, else before the grape, place or vintage) and still splits a few producers (Villa Maria's ranges); to ship it, the 786 names need a hand check[^5a].
   - Vintage is no listing time: training on older vintages and testing on newer ones tests young wines from aged ones, and the third window trains on 38% of the rows[^5b]. Region (107) and country (23, France 40%) folds test a shop's first wine from a new region, a domain shift the shop rarely faces.

   | Split | Test rows (groups) per fold | TabPFN-3.5 | LightGBM | Ridge, TF-IDF |
   |---|---|---|---|---|
   | Random (implemented) | 426 | 0.345 | 0.383 | 0.365 |
   | Grouped by product family | 426 (413 families) | 0.348 | 0.384 | 0.359 |
   | Grouped by producer | 426 (262 producers) | 0.361 | 0.396 | 0.390 |
   | Newer vintages tested (3 windows) | 330 / 264 / 197 | 0.368 (0.259 / 0.387 / 0.458) | 0.408 | 0.360 |
   | Popularity order, tail tested (3 windows) | 212 / 212 / 217 | 0.408 | 0.462 | 0.407 |
   | Grouped by region | 426 (36 regions) | 0.497 | 0.518 | 0.535 |
   | Grouped by country | 426 (1 to 11 countries) | 0.498 | 0.531 | 0.534 |

   RMSE on the log price (RMSLE), mean over folds; 1,277 wines as shipped; 3 folds, 3 repeats (TabPFN) or 10 (the others). TabPFN and LightGBM read the title and description through 32 TF-IDF components each.

   **Andrej (2026-11-11, discuss):** What split would be the most realistic and interesting benchmark use case?

   **Answer (AI, 2026-11-11):** Grouped by producer: pricing a wine from a producer the shop does not list yet.

   * **Problem:**
     - The real use is the shop's buyer pricing a wine new to the list; the data can test it only by what is held out, since they hold no listing date.
     - A random split mixes the two kinds of new listing about half and half: under it the test wines of a known producer score 0.323 RMSLE for TabPFN, those of a new producer 0.363.
     - Grouping by producer tests only the harder half, keeps two thirds for training, and keeps the order and spread of the models (TabPFN ahead by 0.03 to 0.04).
   * **Background:** a new vintage or size of a listed wine is no benchmark here: only 30 wines have one (2% of the rows), and a model would mostly read the sibling's price. Region or country folds test a first wine from a new region, which a shop rarely lists, and change the order of the models (issue table above).

     | Use case (split) | Train share | Test wines | TabPFN-3.5 | LightGBM | Ridge, TF-IDF | Spread |
     |---|---|---|---|---|---|---|
     | New listing, any producer (random) | 67% | 426 | 0.345 | 0.383 | 0.365 | 0.038 |
     | of which producer in training | | 49% | 0.323 | 0.367 | 0.340 | 0.044 |
     | of which producer new | | 51% | 0.363 | 0.397 | 0.386 | 0.034 |
     | New producer (grouped by producer) | 67% | 426 (262 producers) | 0.361 | 0.396 | 0.390 | 0.035 |
     | New vintage or size of a listed wine | 98% | 30 | 0.412 | 0.466 | 0.320 | 0.146 |
     | Predicting the mean | | | 0.694 | | | |

     RMSLE, mean over 3 folds x 3 repeats (TabPFN) or 10 (the others); the new-vintage row is one hold-out of the newest row of each of the 30 families, too few rows to rank models. Evidence: `~/claude_jobs/marks_1111/wine_world_cost/splits2.py`, `splits2_*.csv`.

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Grouped by producer (issue's C) | a hand-checked `Producer` key from the title as the group | the new-producer listing, the case a price list cannot look up; every model loses 0.013 to 0.025 | a constructed key to check by hand (786 names) |
     | b | Random (implemented) | as now, `Snapshot` | both kinds of new listing, in a mix the data cannot confirm | half the test wines borrow their producer's price level |
     | c | New vintage or size of a listed wine | hold out one row per family | the everyday repricing task | 30 test rows |
     | d | Grouped by region | regions held out | a hard shift | a rare case; the order of the models changes |

   * **Recommendation:** a: the producer is the one real structure the data hold that a random split leaks, and holding it out is the harder half of the real task. **Decision:** producer (a), random (b), new vintage (c) or region (d)?

   **Notes for the AI:** on C, add a `Producer` key in `_clean` from the title (text before the first quote mark; else the words before the grape, appellation, region, country, a style word such as Brut, Champagne or Rosé, or the vintage; lower-cased), hand-check the 786 names and merge the ranges of one producer (e.g. Villa Maria's), use it as the group of the split and drop it from the features; the task summary's `split` becomes "Wines of producers not seen in training, from the same shop and time."; a curation bullet; `dataset check`; a CHANGELOG line. On B, the same with the family key (lower-cased title before the comma, without vintage, bottle size, and punctuation). Evidence: `~/claude_jobs/marks_1111/wine_world_cost/` (splits.py, producer_keys.csv, splits_*.csv).

   [^5a]: **SPLIT-24** (Must): group on a true group id, or on one constructed exactly from the data, never on a guess; **SPLIT-4** (Must): when the deployed model predicts for an entity new data would not contain, the test entities are new, however small the gap.
   [^5b]: **SPLIT-14** (Must): a temporal split has at least 3 windows, and no window's train side holds less than 50% of the data.

   **Andrej (2026-11-11, discuss):** Reply (a): Grouped by producer (issue's C)

   **Resolved (2026-11-11, Andrej):** a (the issue's C): grouped by producer.
   - `_clean` adds a `Producer` column (group of the split, no feature): a rule reads it from the title, and two tables in `dataset.py` fix what the rule gets wrong (47 titles that start with an appellation, a second wine or a brand; 339 rows of spelling variants, name forms, brands and ranges of one producer). All 1,277 titles were checked by hand.
   - One producer = the house, estate, winery or cooperative selling under its name, with its brands, ranges and second wines when the title or the shop's copy names it as their maker (Tio Pepe with Gonzalez Byass, The Ned and the King's series with Marisco, Armand de Brignac with Cattier). Separately named estates and corporate owners are not merged (Lynch-Moussas and Batailley, Dom Pérignon and Moët). The shop's own-label ranges (Definition, Chosen by Majestic, Selected by Majestic, Parcel Series, Winemaker Series) are one group each.
   - The draft's 786 keys become 613 producers (250 with more than one wine, the largest Definition with 35); the curation comments describe the method; `assert` on 613.
   - Task summary `split` and `changes`, `grouping` with its definition, `splits_comment`; record `required_split` Grouped (NON-IID). `dataset check`: 0 errors, 0 warnings.
   - With the checked key the random split gave 64% of the test wines their producer in training (49% with the draft key), and the draft's finding that those wines are easier no longer holds; the grouped split still costs every model 0.03 to 0.04:

   | Split | TabPFN-3.5 | LightGBM | Ridge, TF-IDF |
   |---|---|---|---|
   | Random | 0.345 | 0.383 | 0.365 |
   | Grouped by producer (checked key) | 0.375 | 0.410 | 0.403 |

   RMSLE, 3 folds x 3 repeats (TabPFN) or 10; `~/claude_jobs/marks_1111/wine_world_cost/splits3.py`, `producer_key.py`, `producer_keys_checked.csv`.

6. **Use case: who would predict a wine's shelf price from these columns?**

   * **Problem:**
     - The shop sets its own prices, mostly from what the wine costs it (supplier price, UK duty and VAT per bottle, margin); none of that is in the data.
     - The definition's actor, "a wine merchant sets the shelf price of a newly listed wine", is the one actor who never needs the model; and on the shop's page a listed wine's price is a lookup, a prediction only for a wine not on the list.
     - Keep, reframe to an actor who does not know the price, or retire?
   * **Background:**
     - Source: one scrape of Majestic Wine's web shop in 2023 (78 descriptions name it), uploaded to Kaggle "From Internet"; no paper, no stated use.
     - Actors without the price: a producer or importer offering a wine to a UK merchant estimates the shelf price it would sell at; a buyer or a price-comparison site judges whether a wine is good value against similar wines (hedonic price models of wine are an established field[^6a]). Both price a wine absent from the list, which the producer split now tests (issue 5).
     - The same frame ships elsewhere: diamonds (a seller's list price from grading, fit direct) and immoscout_german_house_prices (asking prices from one scrape, fit direct).
     - The copy is the shop's, written after pricing (issue 1); a producer would have its own tasting note instead.

     | Inputs (grouped by producer) | RMSLE | Typical miss |
     |---|---|---|
     | Mean price only | 0.69 | factor 2.0 |
     | Catalogue + copy, TabPFN-3.5 | 0.375 | factor 1.45 |
     | Catalogue + copy, LightGBM | 0.410 | factor 1.5 |

   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep as is (implemented) | the merchant prices a new listing | no change | the actor knows its costs and would not use the model |
     | B | Reframe | `use_case`: a producer, importer or buyer estimates the UK shelf price of a wine not on the list; fit stays approximate | an actor without the price, as diamonds | the shop's copy stands in for a producer's tasting note |
     | C | Reframe, drop the copy | as B, catalogue columns only | inputs a producer really has | reopens issue 1 (copy kept, 2026-11-10); loses the text task |
     | D | Retire | `No (Retired)`, `No Good Target` | no task without a clear user | loses a valuation task on which methods separate |

   * **Recommendation:** B: valuing a wine that is not on the list is a real task with real actors; only the actor named now is wrong[^6b]. **Decision:** keep (A), reframe (B), reframe without the copy (C) or retire (D)?

   **Notes for the AI:** on B, `use_case` = "For example, a producer or importer offering a wine to a UK merchant estimates the shelf price it would sell at, or a buyer judges whether a wine is good value against similar wines, from its catalogue entry and description."; append to `fit_reason` "The shop sets its prices from its costs, which the data do not hold; the model stands for someone who does not know the price."; CC line. On C, also drop `Description` (and decide on `Title`) in `_clean`, `dataset check`. On D, the brief's retirement steps (`No Good Target` marker, folder kept).

   [^6a]: e.g. Combris, Lecocq and Visser (1997), "Estimation of a hedonic price equation for Bordeaux wine: does quality matter?", The Economic Journal 107(441), 390-402.
   [^6b]: **USE-1** (Must): a use case is an actor, a moment and a decision. **USE-9** (Should): ask whether the data mirror another well-defined use case practitioners have, weighed against a use case rephrased only to excuse a gap.

   **Resolved (2026-11-11, Andrej):** B: reframed. `use_case` = "For example, a producer or importer offering a wine to a UK merchant estimates the shelf price it would sell at, or a buyer judges whether a wine is good value against similar wines, from its catalogue entry and description."; `question` = "What would a bottle of wine sell for in a UK wine shop, given its description?"; `fit_reason` appends "The shop sets its prices from its costs, which the data do not hold; the model stands for someone who does not know the price." (fit stays approximate; the price-tier numbers moved to the curation bullet on the copy to keep the field under 70 words); the grouping definition and the split bullet name the new actor; a curation bullet; record CC line. Text only, data unchanged.
