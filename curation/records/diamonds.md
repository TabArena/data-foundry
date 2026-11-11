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
suggestion: 'Yes'
tags:
- 'Samples: One Moment'
original_source: Other
year: '2007'
domain: business & marketing
required_split:
- Random (IID)
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

CC (2026-11-11, Andrej): BeyondArena v0.2 review page, diamonds:
- Issue 2 (time basis), B: the split is named a `Snapshot` of the one diamondse.info scrape of February 2007; the `Time basis:` line is in the definition's notes (not tested: prices after 2007). The tag enters `data_tags` once PR #50 is in the working copy.
- Record fields set to the definition's values: `original_source` Other, `domain` business & marketing.
- Issue 1 (split by stone) stays open: marked `discuss`, answered with the link evidence; the random split is unchanged.

## Review

**Outcome:** added. The diamonds table of the ggplot2 R package: 53,940 round diamonds with their grading (carat,
cut, colour, clarity, depth and table in percent, length, width and depth in millimetres) and their price, which
Hadley Wickham scraped from the search site diamondse.info in February 2007; the target is the log price, scored by
RMSLE on the dollar price, with a random split. The AI recommends shipping it after one change: split by stone, since
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

**Main points:** Split by stone so a stone's two listings stay on one side (issue 1)? The split is named a
`Snapshot` of the February 2007 scrape (issue 2, resolved 2026-11-11).

**Record judgment:** valid, with one leak to fix. The record's open point, "the seller and the date of the prices are
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

   [^1c]: **LEAK-41** (Must, draft PR #62): repeats of a unit the data does not record get one of four verdicts:
     natural, entity fix, temporal fix or not recoverable; in an entity fix copies of one record go down to one row
     per unit, and several observations of one unit, each with its own label (a stone listed with two prices among
     the examples), are grouped; a key rebuilt from the features is the curator's call. **SPLIT-24** (Must): a key
     constructed from the data by a calibrated link whose chance rate shows that most links are real.
   [^1d]: **LEAK-42** (Should, draft PR #62): three tests set the verdict, not the size of a score gap: is the link
     above a chance rate that keeps the data's structure (values moved by their measurement step among the nulls),
     does the label travel with it beyond what the shared features predict, is there an order.

   **Andrej (2026-11-11, discuss):**

   **Answer (AI, 2026-11-11):** Nothing new was measured; the choice is the same three, and the evidence already
   gathered decides it. Split by stone (b)?

   * **Problem:**
     - 10,296 pairs of rows are one stone in two price lists: they match on carat, colour, clarity, depth, table and
       the height z, 94.7% with width and length exactly swapped, and only 1.2% carry the same price.
     - The link is far above chance: moving one key column by one step of its resolution, everything else equal,
       finds 2 to 174 matches against the 10,296 exact ones, and the two listings' prices still move together
       (correlation 0.46) once their carat, colour, clarity, cut and price list are taken out (-0.02 for two
       different stones)[^1e].
     - Under the random split 27% of the test rows have their stone's other listing in training, and the partner's
       price cuts TabPFN-3.5's error by 4.6% on 6 of 6 held-out splits.
   * **What is not decisive:** the cost to a boosted tree (0.0853 against 0.0860 RMSLE, random against grouped),
     which is the gap of a method that does not look up its neighbours; the rules set the verdict by the link, not
     by the size of a score gap.
   * **What a split by stone does not fix:** different stones may share the six-column key by chance and stay
     together; the calibration above puts that at well under a percent of the pairs.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Random split (implemented) | 53,940 rows, 3 x 3 random folds | no change | 27% of test rows have their stone in training; rewards a lookup the use case lacks |
     | b | Split by stone | a `stone_id` from the six columns as the group, never a feature; 3 x 3 grouped folds | no stone on both sides; keeps both price lists and all rows | a group id built by us |
     | c | One listing per stone | about 10,700 rows dropped, random split | no copy at all | loses a fifth of the rows and one of the two prices |

   * **Recommendation:** b, unchanged. **Decision:** a, b or c?

   [^1e]: **LEAK-41**, **LEAK-42** and **SPLIT-24** as in the footnotes above.

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

   **Andrej (2026-11-11, change):** Option B: Named Snapshot, with the split issue 1 settles.

   **Resolved (2026-11-11, Andrej):** B: the `Time basis: Snapshot:` bullet is in `curation_comments` (one scrape of
   diamondse.info, February 2007; not tested: prices after 2007); rows, split and `data_tags` are unchanged. The line
   assumes the implemented random split, since issue 1 has no mark yet; its wording holds for a split by stone too,
   and under the random split a stone's other listing at the same scrape is the one same-moment target issue 1 still
   decides. The tag `Snapshot` enters `data_tags` once PR #50 is in the working copy. Record fields `original_source`
   (Other) and `domain` (business & marketing) set to the definition's values (mark `update`).

## Reference

Ggplot2: Elegant Graphics for Data Analysis
