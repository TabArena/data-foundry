---
unique_name: diamonds
name: diamonds
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
- WIP (DF)
claimed_by: Andrej
suggestion: 'Yes'
priority: 2
tags:
- 'Samples: One Moment'
- 'Entities: Recur'
- Non-IID (Grouped)
original_source: Other
year: '2007'
domain: business & marketing
required_split:
- Grouped (NON-IID)
problem_type: Regression
source_links:
- https://www.openml.org/search?type=data&id=42225
- https://ggplot2.tidyverse.org
notebook_path: datasets/beyond_iid/old_iid/diamonds/diamonds.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/diamonds/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Depending on what the actual task is, might require temporal split. R2 as metric is not representative as all methods perform strong on R2 for this dataset; potential temporal confounder but only the target is time-related if at all, newer version: https://www.kaggle.com/datasets/hrokrin/the-largest-diamond-dataset-currely-on-kaggle - no source on these dataset include date information but it seems obvious that there might be temporal conneciton, however the task ignores this / does not matter. unclear if the price got adjsuted or computed post hoc

Potential issue: temporal dependence

Lennart: We can likely ignore the impact of time for the task

Andrej: Fulfills requirements

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback rmse — a ggplot2 teaching dataset; the source defines no task or score.

CC (2026-10-21, Lennart): diamonds ships the price in dollars and is scored by RMSLE, a metric obvious from the task (new origin `context`: a price's error matters relative to the price).

**Assessment (AI, 2026-10-21):** the price ships on a log scale again (`np.log` in `_clean`, as before today's change) and is scored by RMSLE on the dollar price after the inverse (`Metric.from_context("rmsle", target_transform="log")`, MET-3). Needs a rebuild to reach the container.

CC (2026-10-21, Lennart): ship the target on the modelling scale, score on the original scale (target_transform).

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): 3 ordinal scales typed as ordered categories in the codebook's order (CLEAN-14, amended): `cut`, `color`, `clarity` (the README lists their levels).

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `brilliant_earth_diamond_prices` (TBD -> Yes, priority 2). Each is screened in its own record; this record's verdict stays the curator's.

**Assessment (AI, 2026-11-04):** reviewed for the BeyondArena v0.2 review page, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the record's Review. Ship after splitting by stone: 40% of rows are a stone listed twice at two prices, and under the random split 27% of test rows have their stone in training, which a lookup method exploits (4.6% RMSE for TabPFN-3.5). Priority 2: gap 0, use case 0, source 1, shape 1, risk -1.

CC (2026-11-11, Andrej): BeyondArena v0.2 review page, diamonds:
- Issue 2 (time basis), B: the split is named a `Snapshot` of the one diamondse.info scrape of February 2007; the `Time basis:` line is in the definition's notes (not tested: prices after 2007). The tag enters `data_tags` once PR #50 is in the working copy.
- Record fields set to the definition's values: `original_source` Other, `domain` business & marketing.

CC (2026-11-12, Andrej): BeyondArena v0.2 review page, diamonds:
- Issue 3 (better diamond price data), A: diamonds stays. No public table of single stones priced at several dates was found; `brilliant_earth_diamond_prices` stays a candidate in its own record.
- Metric and split marked `ok`: RMSLE on the dollar price stays; the split stays random while issue 1 (split by stone) is open.

CC (2026-11-12, Andrej): split by stone (Review issue 1, B).
- 40% of the rows are one stone listed twice (a few up to six times) in two price lists of the February 2007 scrape; the dearer price is the cheaper one times a fixed factor of the price band, so under random folds a stone's other listing in training gave its price.
- `stone_id` (the group number of carat, colour, clarity, depth, table and z: 43,000 stones) is the group and no model input; grouped 3 x 3 folds; all 53,940 rows stay, both price lists with them. `required_split` Grouped (NON-IID), tag `Non-IID (Grouped)`.

## Review

**Outcome:** added. The diamonds table of the ggplot2 R package: 53,940 round diamonds with their grading (carat,
cut, colour, clarity, depth and table in percent, length, width and depth in millimetres) and their price, which
Hadley Wickham scraped from the search site diamondse.info in February 2007; the target is the log price, scored by
RMSLE on the dollar price, split by stone since 2026-11-12 (random before). The AI recommended shipping it after one change: split by stone, since
40% of the rows are two listings of the same stone and under the random split 27% of the test rows have their stone's
other listing in training (issue 1). Reviewed without a panel, from the gathered evidence (the record, the definition, a
model
run on the TabArena v0.1 copy of the same rows) and two checks of the rows. Validity: real prices from a named site;
the repeat listings are a repeated-entity leak that a method able to find the other listing exploits (issue 1); no
other leak. Value: the methods separate widely (RMSE in dollars on the TabArena copy: LimiX-2 486, TabPFN-3.5 492,
CatBoost 520, KNN 668 to 957, linear regression 1,140 to 1,654), and an explicit price-list model without the
partner listing ranks 15th to 38th of 94. Quality: 146 exact copies (features and price) remain; they fall into one
group under issue 1. Weighed: real prices with a documented scrape and wide method separation +; a 2007 table of one
search site, its seller unknown, and better data for the same task under screening (brilliant_earth_diamond_prices)
-.

**Main points:** Nothing open. Split by stone, so a stone's listings stay on one side (issue 1, B, resolved
2026-11-12). The split is named a `Snapshot` of the February 2007 scrape (issue 2, resolved 2026-11-11). Diamonds
stays over other diamond price data (issue 3, resolved 2026-11-12, A).

**Record judgment:** valid, with one leak, fixed by the split by stone (issue 1). The record's open point, "the seller and the date of the prices are
not stated", is answered: Wickham created the data in February 2007 by scraping diamondse.info with a Ruby script
(his post to R-help, April 2023, https://stat.ethz.ch/pipermail/r-help/2023-April/477277.html), which fits the
record's year 2007. The record's earlier worry that every method scores high is met by the RMSLE metric (Lennart,
2026-10-21). A scouting run found a larger diamond price table, brilliant_earth_diamond_prices, screened in its own
record.

**Issues for Andrej:**

1. **Split by stone, so the two listings of one stone stay on one side?**

   * **Problem:**
     - 21,493 rows (40%) share carat, colour, clarity, depth, table and z (the height in millimetres) with another row,
       mostly in pairs whose width and length are swapped: the same stone listed twice, at two prices.
     - Under the random split 27% of the test rows have their stone's other listing in training, so a method that
       finds it reads the price off it instead of pricing a new stone[^1a].
     - Group the split on these six columns, keep one listing per stone, or keep the random split?
   * **Background:** of the 10,296 pairs, 94.7% have x and y exactly swapped and 36% differ in cut by a grade; the
     record with x greater than y is dearer in 92% of pairs, by a factor that falls with the price (median 1.28 below
     $1,000, 1.07 at $1,000-2,000, 1.018 at $2,000-8,000, 1.009 above), and only 1.2% of pairs have the same price.
     So the pairs are one stone in two price lists (two sellers or two feeds of the search site), each record with its
     own measured width, length and cut grade. Grouping on columns that define the entity is allowed when the key is
     built exactly from the data, as here[^1b].
   * **Effect on the task:** the use case prices a newly listed stone from its grading; a stone's other listing is
     not part of that, unless a seller prices a stone a competitor already lists, which the definition does not name.
     With the random split the benchmark rewards recognising the stone.
   * **Experiments:** a model run on the TabArena copy (same rows, RMSE in dollars): features that give
     TabPFN-3.5 the partner listing's price cut its error by 4.6-4.7% on 6 of 6 held-out splits (rank 4 to 1 of 94),
     and an explicit price-list model ranks 1st of 94 with the partner lookup and 15th without. An earlier check on
     the same rows (untuned LightGBM, 3 x 3 folds, RMSLE): random split 0.0853, split by stone 0.0860; on test rows
     whose stone is in training 0.060 against 0.093 for the rest; one listing per stone, random split, 0.091. So a
     boosted tree barely uses the partner, while a method that looks up similar rows gains a lot.
   * **Consistency:** fiat_500 keeps one row per car (Lennart, 2026-10-14), where the copies mostly share one price;
     here the two listings carry two prices of two price lists, so grouping keeps both and departs from it for that
     reason.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random split (implemented) | 53,940 rows, 3 x 3 random folds | no change | 27% of test rows have their stone in training; rewards a lookup the use case lacks |
     | B | Split by stone | all rows stay; a stone id built from the six columns is the group, never a feature; 3 x 3 grouped folds | no stone on both sides; keeps both price lists; costs a boosted tree 0.0007 RMSLE | a group id built by us; a few different stones may share the key by chance and stay together |
     | C | One listing per stone | about 10,700 rows dropped, one listing kept per stone, random split | no copy at all | loses a fifth of the rows and one of the two prices; which list to keep is arbitrary |

   * **Recommendation:** B, split by stone: it removes the lookup at no measurable cost to a boosted tree and keeps
     every price. **Decision:** split by stone (B), keep one listing per stone (C), or keep the random split (A)?

   **Notes for the AI:** on B, add a `stone_id` from `groupby(["carat", "color", "clarity", "depth", "table",
   "z"]).ngroup()` as the group (not a feature), switch the split to grouped 3 x 3, keep the 146 exact copies (they
   share a group; say so in the notes), and write into `row`/`fit_reason` the scrape (diamondse.info, February 2007,
   Wickham's R-help post) and that 40% of the rows are a stone's second listing. Re-run `dataset check` and the task
   probes.

   [^1a]: **LEAK-17** (Must): repeated entities in different rows leak the target across the split even when the
     rows differ: keep one row per entity when the use case is that row, or group. **SPLIT-29** (Must): an IID split
     is wrong when many rows share an entity that new data would not have and the entity carries the label.
   [^1b]: **SPLIT-24** (Must): group on a true group id or on one constructed exactly from the data, such as
     identical values in the columns that define the entity; never on a similarity cluster.

   **Answer (AI, 2026-11-06):**

   * **Verdict under the new entity-leakage rules: entity fix, grouped (B).** The two listings are one stone with two
     prices from two price lists: several observations of one unit, each with its own label, which the rules group
     rather than cut to one row (C is their remedy for a record entered twice)[^1c].
   * **Is the link real?** 10,206 pairs match on the six key columns with width and length exactly swapped. Moving one
     key column by one step of its resolution, everything else equal and the swap kept, finds 4 pairs for depth (0.1),
     2 for the height z (0.01 mm), 59 for carat (0.01) and 174 for table (1). The exact matches are far above that
     chance rate, so the key joins one stone, not look-alikes.
     - The swap alone would not be enough: 5,257 pairs of the same carat, colour and clarity have their width and
       length exactly swapped but differ in depth, table or z (median 0.5 in depth); they are different stones, and
       the key keeps them apart.
   * **Does the price travel?** Yes. With the mean price of their carat, colour, clarity, cut and price list (whether
     the width is above the length) taken out, the two listings' prices still move together (correlation 0.46), against -0.02 for two different stones of
     the same carat, colour and clarity from the two lists; the partner's price cuts TabPFN-3.5's error by 4.6%.
   * **Is there an order?** No: one scrape of February 2007 (issue 2), so there is no time to split on.
   * **The small gap for a boosted tree (0.0007 RMSLE) does not decide it:** the rules set the verdict by the link, not
     by the size of a score gap[^1d].
   * **Recommendation stays B:** split by stone on the six columns.

   [^1c]: **LEAK-42** (Must, draft PR #62): repeats of a unit the data does not record get one of four verdicts:
     natural, entity fix, temporal fix or not recoverable; in an entity fix copies of one record go down to one row
     per unit, and several observations of one unit, each with its own label (a stone listed with two prices among
     the examples), are grouped; a key rebuilt from the features is the curator's call. **SPLIT-24** (Must): a key
     constructed from the data by a calibrated link whose chance rate shows that most links are real.
   [^1d]: **LEAK-43** (Should, draft PR #62): three tests set the verdict, not the size of a score gap: is the link
     above a chance rate that keeps the data's structure (values moved by their measurement step among the nulls),
     does the label travel with it beyond what the shared features predict, is there an order.

   **Andrej (2026-11-12, discuss):** I am unsure about the true origin of the duplicates. Is it really the same stone?
   Why is it listed at a different price? By how much does the price differ? If it is an artefact of missing temporal
   order, can we reconstruct it? Could the dataset also be synthetically generated?

   **Answer (AI, 2026-11-12):** the same stone in two price lists of the same two days: in 98% of the 9,747 pairs with
   width and length swapped, the dearer price is the cheaper one times one of eight fixed factors, exact to the dollar,
   and the factor follows the price band (between $2,800 and $7,000 also the carat). There is no date to reconstruct,
   and the table carries the marks of a real scrape, not of a generator.

   | Pair column (10,296 pairs sharing the six key columns) | Result |
   |---|---|
   | carat, colour, clarity, depth, table, z | equal (the key) |
   | x and y (length, width) | swapped exactly 9,747; equal 334; other 215 (median 0.02 mm apart) |
   | depth = 2z/(x+y) | holds within rounding for both listings in 9,731 of 9,747 swapped pairs |
   | cut | differs in 36%, almost always one way: Premium to Very Good (2,292), Very Good to Good (778), Ideal to Very Good (396) |
   | price, swapped pairs | never equal; listing with x > y dearer in 94.6%; difference median $127 (10th to 90th percentile $65 to $209) |
   | price, all pairs | equal in 120 (1.2%), all among pairs without the swap |

   | Factor (dearer / cheaper price) | Pairs | Cheaper price | Matches to $1 |
   |---|---|---|---|
   | 1.2823 | 4,085 | $334 to $877 | 100% |
   | 1.0684 | 733 | $877 to $1,169 | 100% |
   | 1.0746 | 614 | $1,141 to $1,710 | 100% |
   | 1.0526 | 559 | $1,715 to $2,279 | 100% |
   | 1.0091 | 810 | $2,282 to $18,653 | 99.9% |
   | 1.0182 | 1,985 | $2,774 to $10,995 | 100% |
   | 0.9824 | 518 | $2,853 to $6,889 | 100% |
   | 1.0469 | 233 | $1,179 to $16,059 | 93% |
   | none of these | 210 | | |

   * **Same stone, two lists:** every measurement matches; one list writes the larger diameter first (x > y), uses its
     own cut names and charges its own markup, which is why the price differs.
   * **Not time:** a price that moved between two dates would spread the ratio and go both ways; here it sits on eight
     values set by the price band, so both prices are markups on one base price; the 526 pairs where the x > y
     listing is cheaper are, but for 8, one of these factors (0.9824). Wickham's write-up ("Diamonds in the
     rough", 17 September 2007, attached to his R-help post of April 2023) dates the scrape to 6-7 February 2007 and
     says the data are "provided exactly as extracted from the website".
   * **No order to recover:** the CSV, the ggplot2 documentation and the paper give no listing date. The file is 164
     runs, each sorted by price and a multiple of 30 rows long (144 runs of 330), with the runs' top price rising from
     $2,812 to $18,823, then from $658 to $2,757: the trace of price-sorted search pages, not of time.
   * **Not generated:** carat heaps at the sizes cutters aim for (0.99 ct: 23 stones, 1.00: 1,558, 1.01: 2,242; 1.49:
     11, 1.50: 793); depth matches 2z/(x+y) within rounding in 99.1% of rows, and the misfits are typing slips of the
     kind the paper describes (y = 58.9, the depth value; 31.8 mm for 3.18; 20 zero sizes); no price falls in $1,455
     to $1,545 against about 900 in each $90 band beside it, which Wickham calls "a known data collection problem".
     Price last digits are evenly spread (5,012 to 5,751 per digit), as computed markups are.
   * **For issue 1:** a stone's other listing gives its price to the dollar once the band factor is known, so under the
     random split 27% of test rows can be priced by lookup. Grouping removes that and keeps both lists, whose markups a
     model can still learn from other stones (the x > y order tells the list).

   | | Option | What it does | Pro | Con |
   |---|---|---|---|---|
   | A | Random split (implemented) | 53,940 rows, random folds | no change | 27% of test rows have their stone's other listing in training, which gives the price to the dollar |
   | B | Split by stone | the six-column stone id as the group, grouped folds | no stone on both sides; both lists kept | a key built by us |
   | C | One listing per stone | about 10,700 rows dropped | no copy at all | a fifth of the rows and one list's price for those stones lost |

   * **Recommendation:** B, unchanged: the pairs are one stone under two markups of the same scrape, with no time
     between them. **Decision:** split by stone (B), one listing per stone (C) or the random split (A)?

   **Andrej (2026-11-12, discuss):** Reply (B): Split by stone

   **Resolved (2026-11-12, Andrej):** B: `stone_id`, the group number of carat, colour, clarity, depth, table and z
   (43,000 stones of 1 to 6 rows), is the group and no model input; grouped 3 x 3 folds; all 53,940 rows stay, the 146
   exact copies each inside one stone (said in the notes). The task summary's `row`, `split`, `fit_reason` and a new
   `changes` name the scrape (diamondse.info, February 2007, Wickham's R-help post) and the repeat listings; a curation
   bullet gives the evidence. Issue 2's `Time basis:` line holds as written. Record: `required_split` Grouped (NON-IID),
   tag `Non-IID (Grouped)`, CC line. `dataset check` (Slurm job 1380062): 0 errors, 0 warnings, 2 info (the 146 exact
   copies, 199 rows with the same features and another price), 9 features, test folds of 17,954 to 18,029 rows
   (14,333 to 14,334 stones). Task probes on the 9 grouped splits, no flags:

   | Model (untuned) | RMSE on the log price |
   |---|---|
   | LightGBM | 0.089 |
   | Random forest | 0.095 |
   | Linear | 0.146 |
   | Best single feature (carat or y) | 0.253 |
   | Mean (dummy) | 1.015 |

   Not rebuilt.

2. **Time basis: name the split a `Snapshot` of the February 2007 scrape?**

   * **Problem:**
     - Every row is a listing's grading and asking price at one scrape of diamondse.info in February 2007, so every price is of the same moment and no row lies after another.
     - The record's collection fact fits (`Samples: One Moment`, no target tag), and the split carries no time basis; issue 1 asks to group it by stone.
     - Name the split, random or by stone, a `Snapshot`?
   * **Background:** a split that only fills in a moment the data covers is a `Snapshot`; its line names the moment,
     and no row of the same moment may carry a test row's target[^2t1]. The rows that do are a stone's other listing
     at the same scrape, which issue 1 keeps on one side; past that, the use case prices a stone against the same
     day's price list. What the split cannot test: prices after February 2007.
   * **Effect on the task:** none on rows, splits or scores.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | No time basis (implemented) | as now | none found | the score's time meaning is not stated; `dataset check` notes the missing basis |
     | B | Named `Snapshot`, with the split issue 1 settles | `data_tags` gain `Snapshot`; a `Time basis:` line names the scrape | states that every price is of one moment | later prices are not tested |
     | C | Forced from temporal | `data_tags` gain `ForcedIIDFromTemporal`, reading the use case as pricing later listings | marks the forward reading | the amended rule gives a release of one moment a prototype, not the forced tag[^2t2] |

   * **Recommendation:** B. **Decision:** A, B or C?

   **Notes for the AI:** once PR #50 is in, on B: `data_tags = ("Snapshot",)` (no tag is listed now; under issue 1's
   B the grouping adds `Non-IID` and `Grouped` itself) and the curation bullet "- Time basis: Snapshot: one scrape of
   the search site diamondse.info in February 2007 (Wickham); each row a listing's grading and its asking price at
   that moment; the use case prices a stone against the same day's price list. Not tested: prices after 2007.";
   `dataset check`. The record's facts stay.

   [^2t1]: **SPLIT-32** (Should): a definition can name the use-case prototype it follows, with a `Time basis:` line
     stating the fact. A `Snapshot` only fills in a time the data covers (one census, one scrape); its line names the
     moment, and no row of a test row's time may carry its target, else the split groups by that time unit.
   [^2t2]: **SPLIT-8** (Must; reworded 2026-11-05): a release that is one moment (one extract, one stock month, one
     exam round) is not forced; SPLIT-32 gives it `Snapshot` or `DelayedTarget`.

   **Resolved (2026-11-11, Andrej):** B: the `Time basis: Snapshot:` bullet is in `curation_comments` (one scrape of
   diamondse.info, February 2007; not tested: prices after 2007); rows, split and `data_tags` are unchanged. The line
   assumes the implemented random split, since issue 1 has no mark yet; its wording holds for a split by stone too,
   and under the random split a stone's other listing at the same scrape is the one same-moment target issue 1 still
   decides. The tag `Snapshot` enters `data_tags` once PR #50 is in the working copy. Record fields `original_source`
   (Other) and `domain` (business & marketing) set to the definition's values (mark `update`).

3. **Replace diamonds with better public diamond price data, possibly dated?**

   * **Problem:**
     - No public table of single stones with prices at several dates was found: every listing-level set is one
       scrape; dated series exist only as price indexes or as paid auction records.
     - Andrej's dataset note (2026-11-11): "Might there be a better dataset for diamonds price prediction, possibly
       one that also respect the temporal dimension?"
     - Two larger listing tables exist; each has a weakness diamonds does not have.
   * **Found (web search and the Kaggle files, 2026-11-11):**

     | Data | Stones | Date | Source | Features | Licence | Weakness |
     |---|---|---|---|---|---|---|
     | diamonds (shipped) | 53,940 | one scrape, Feb 2007 | diamondse.info (Wickham) | 4 Cs, depth, table, x/y/z | MIT | 40% are a stone's second listing (issue 1) |
     | brilliant_earth_diamond_prices (record, TBD -> Yes) | 119,307 (48,994 lab-grown) | one fetch, 2020-11-29 | brilliantearth.com (Corral, scraper on GitHub) | shape, 4 Cs, grading lab, natural or lab-grown | CC BY-NC 4.0 | no depth, table or size; 74% of rows share every feature with another row (39% also the price) |
     | Kaggle hrokrin, "largest diamond dataset" | 219,703 | none (uploaded 2023-03-16) | not named | 25: shape, cut grade, polish, symmetry, lab, fluorescence, girdle, culet, sizes, fancy colour | CDLA-Permissive 1.0 | unknown seller and date |
     | Price indexes (Biz Data Lab, Caratlytics, thediamondprice.com, OpenFacet) | none | daily to monthly | retail listings | aggregates per grade cell | unclear | no stone rows |
     | Auction results (Rapaport; Rocks International) | lots | dated | Christie's, Sotheby's | lot grading | commercial | not public |

   * A temporal version would need our own repeated scrape (for example the published DiamondScraper run each month),
     which gives usable history only after months and depends on the site's terms.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep diamonds (implemented) | no change; brilliant_earth_diamond_prices stays a candidate in its own record | documented scrape; measurements | 2007, one moment |
     | B | Replace with brilliant_earth_diamond_prices | retire diamonds once the candidate is built | 2.2 x the stones, 2020 prices, lab-grown vs natural | one moment too; few features, many identical rows; non-commercial licence |
     | C | Replace with the hrokrin table | build it in place of diamonds | most stones and features | seller and date unknown (fails the source rules) |
     | D | Build a dated scrape ourselves | collect monthly snapshots for a later temporal task | a real time dimension | not public data; months before use |

   * **Recommendation:** A: no candidate is dated, and none is better on every count; brilliant_earth_diamond_prices
     is screened on its own merits. **Decision:** A, B, C or D?

   **Resolved (2026-11-12, Andrej):** A: diamonds stays; no public table of single stones priced at several dates was
   found, and `brilliant_earth_diamond_prices` stays a candidate in its own record. The definition is unchanged; a CC
   line is in the record.

## Reference

Ggplot2: Elegant Graphics for Data Analysis
