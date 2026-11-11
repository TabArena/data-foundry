---
unique_name: miami_housing
name: miami_housing
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: 'Yes'
tags:
- 'Samples: Over Time'
- 'Time: Dated'
- Non-IID (Temporal)
original_source: OpenML
year: '2021'
domain: business & marketing
required_split:
- Temporal (NON-IID)
source_links:
- https://www.openml.org/search?type=data&id=43093&sort=runs&status=active
- https://www.openml.org/search?type=data&id=44983
notebook_path: datasets/beyond_iid/old_iid/miami_housing/miami_housing.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/miami_housing/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

housing datasets with a lot of spatial information but all within one yea

Potential issue: spatial and semi temporal

Lennart: We can likely ignore temporal and spatial influences for this housing predictive task with the given data / features

Andrej: We need to write down the reason why we consider some housing datasets as random split data and others as temporal

**Assessment (AI, 2026-10-14):** The file first appeared on OpenML 43093 (MiamiHousing2016, uploaded 2021-09-24, creator and contributor Steven C. Bourassa, citing Mayer, Bourassa, Hoesli and Scognamiglio 2021, SSRN 3924412), so the source is OpenML, 2021; the definition said Kaggle and now says OpenML. The Kaggle dataset deepcontractor/miami-housing-dataset (last updated 2022-01-30) copies the OpenML description and names openml.org as its source; OpenML 44983 (2022-12-22) is a copy of that Kaggle dataset. All three describe the same 13,932 sales of 2016.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback rmse — Mayer et al. 2021 (SSRN) could not be read; the abstract names only 'predictive performance'. rmse on the log sale price is the regression fallback.

**Assessment (AI, 2026-10-21):** metric now `Metric.from_context("rmsle", target_transform="log")` instead of the fallback rmse on the log target: a sale price's error matters relative to the price; the target still ships as log, and RMSLE is computed after the inverse, on the original scale (MET-3). Needs a rebuild to reach the container.

CC (2026-10-21, Lennart): ship the target on the modelling scale, score on the original scale (target_transform).

CC (2026-10-31, Lennart): marks on the review board of PR #37 (the order comes from the context and logic, not from the target): structure_quality, a 1-5 quality code without labels, is an ordered category in the order of its codes.

CC (2026-11-01, Lennart): marks on the review board of PR #37: month_sold stays a number (a position in the year's continuous cycle, shipped as a number: the curator's cycle rule).

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `florida_dor_property_sales` (TBD -> Yes, priority 2). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-01, Lennart): the decode rule (a code whose codebook says in words what each level is carries the words; a score without them is a number): 1 scores are numbers (structure_quality).

CC (2026-11-11, Andrej): BeyondArena v0.2 review page, miami_housing:
- Issue 1 (split), reply (c): five monthly test windows, August to December 2016, each trained on all earlier months (58% to 92% of the sales), no gap; `sale_month` (2016-MM-01) from `month_sold` is the time column. Repeat sales of a home stay (13,932 rows, was 13,776); there are no exact copies. `required_split` Temporal (NON-IID), tag `Non-IID (Temporal)`. Measured cost of the change at equal training size: +0.001 RMSLE (2026-11-06).
- Issue 2 (domain), B: `business & marketing`, as the other house prices, in the definition and here.

## Review

**Outcome:** added. Single-family homes sold in Miami in 2016, released on OpenML by the data's creator, Steven
Bourassa (2021): land and living area, the value of special features such as pools, age, structure quality, the
month of sale, airplane noise, and distances to the ocean, water, rail, highway and the centres; the target is the log
sale price, scored by RMSLE on the price, with a random split. 13,776 sales after keeping one sale per parcel. The AI
recommends shipping it after one change: split by month, as the other dated house sales are (issue 1). Reviewed
without a panel, from the gathered evidence (the record, the definition, a model run on the TabArena v0.1 copy
of the same rows) and one check of the rows. Validity: real sales of a documented release; no leak found; the random
split rests on a mass-appraisal reading that no other house-price dataset of the benchmark uses (issue 1). Value: the
methods separate widely (RMSE in dollars on the TabArena copy: LimiX-2 70,400, TabPFN-3.5 74,200, CatBoost 78,400, KNN
101,000 to 120,000, linear regression 176,000 to 191,000), and a hedonic kriging model ranks 8th of 95. Quality: no
open point. Weighed: the creator's own release with distances he built, real sale prices, wide method separation +;
one year and one county, and better data under screening (florida_dor_property_sales) -.

**Main points:** No open issue. Split by month into five monthly windows (issue 1, resolved 2026-11-11); domain
`business & marketing` (issue 2, resolved 2026-11-11).

**Record judgment:** valid. The source is settled (OpenML 43093, uploaded by Bourassa on 2021-09-24, citing Mayer,
Bourassa, Hoesli and Scognamiglio 2021, https://doi.org/10.2139/ssrn.3924412). The definition's domain is finance;
the other house-price datasets use business & marketing. Andrej's note in the record, "We need to write down the
reason why we consider some housing datasets as random split data and others as temporal", is what issue 1 answers.
A scouting run found Florida's statewide sales and assessment rolls (florida_dor_property_sales), screened in its own
record with a temporal split.

**Issues for Andrej:**

1. **Split the 2016 sales by month, as house_sales splits its year?**

   * **Problem:**
     - The definition splits Miami's 2016 sales at random, reading the task as an appraiser valuing homes with the
       same year's sales; the other dated house sales of the benchmark are split in time, and the rules name a sale
       price among the tasks that need a temporal split[^1a].
     - The month of each sale is in the data, enough for five monthly test windows (August to December) that each
       train on all earlier months, 58% to 92% of the sales.
     - Split by month, or keep the random split with the appraisal reading written down?
   * **Background:** sales per month run from 831 (January) to 1,373 (June); the median price rises from $290,000 in
     January to $320,000 by June and stays there. A county appraiser values every home as of 1 January from the sales
     of the year before, which a random split within the year mirrors; a lender or a valuation site prices the next
     sale from the earlier ones, which a split in time mirrors. About 1% of parcels sold twice in 2016; the definition
     keeps the first sale, and with a split in time the later sale could stay as history, as the California sales do
     (Lennart, 2026-10-21).
   * **Experiments:** an earlier check (untuned LightGBM, 3 seeds, RMSLE), each of the last three months as a test
     window: trained on the earlier months 0.1285 / 0.1390 / 0.1398 (December, November, October), trained on as many
     sales drawn from all other months 0.1288 / 0.1394 / 0.1396. The split changes no score measurably, so the choice
     rests on the use case and on consistency.
   * **Consistency:** house_sales (King County, one year of sales) is split into three-week windows, ames_housing into
     two-month windows, california_house_prices_2020 by sale order; the candidate florida_dor_property_sales plans a
     split by sale year and month.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random split (implemented) | 13,776 sales, 3 x 3 random folds | the appraiser's reading; no change | the only dated house-sale table split at random; trains on later months |
     | B | Five monthly windows | test August to December 2016, each trained on all earlier months; resales kept | the same regime as the other house sales; a lender's or valuation site's task | month resolution only; under one year of history; five test windows of about 1,040 to 1,260 sales |

   * **Recommendation:** B, split by month: the same task gets the same regime as house_sales, and the measured cost is
     nil. **Decision:** split by month (B), or keep the random split with the appraisal reading in `fit_reason` (A)?

   **Notes for the AI:** on B, build a date `sale_month` (2016-MM-01) from `month_sold` as the time column, keep
   `month_sold` as a feature, `Temporal(on="sale_month", splits=TemporalSplits(window=1, unit="months", n_windows=5,
   min_train_fraction=0.5))`; keep repeat sales of a parcel and drop only exact copies; rewrite `split`, `fit_reason`
   and `splits_comment`, set the record's `required_split` to Temporal; re-run `dataset check`. On A, write the
   appraisal reading and this check into `fit_reason`.

   [^1a]: **SPLIT-6** (Must): a fixed predictive task that only needs a temporal split (a delivery time, a default,
     a sale price) gets a temporal split. **SPLIT-4** (Must): the split follows what the task does in reality, not the
     size of the gap. **SPLIT-14** (Must): at least 3 windows, none training on less than half of the data.

   **Answer (AI, 2026-11-06):** The sale month is information for the split: split by month, or keep the random split
   as a stationary relation or as a snapshot?

   * **Problem:**
     - A sale price depends on the date of the sale, `month_sold` dates every sale of 2016 to its month, and a lender or
       a valuation site prices later sales, so the month is information for the split, and a random split can name
       the use-case prototype it follows, with its measured check[^1b].
     - The definition's own reading, an appraiser valuing the year's unsold homes from the same year's sales, fills in
       values inside the period the data covers, which is the snapshot prototype[^1c].
     - The cost of the random split is now measured on the v0.2 rows with two model families, and it is nil.
   * **Background:** 831 (January) to 1,373 (June) sales a month; the median price rises from $290,000 in January to
     $305,000 by March and $320,000 by June. Five monthly windows, August to December, train on 58% to 92% of the
     sales; the issue's earlier check compared only the last three months, with LightGBM.
   * **Experiments:** the 13,776 shipped sales and 15 features (`month_sold` kept), untuned LightGBM and ridge
     regression (one-hot categories), RMSLE on the price (Slurm job 1365897):
     - Shipped random split (3 x 3): LightGBM 0.151 (0.142 to 0.158), ridge 0.273.
     - The five monthly windows, each trained on all earlier months: LightGBM 0.139 on December (the newest) and 0.146
       to 0.152 on August to November; ridge 0.260 to 0.277.
     - Same test sales and same training size (each window's sales in 3 folds, 3 seeds; earlier months only against
       sales drawn from all other months): LightGBM 0.1473 against 0.1462 over the five windows (+0.001; -0.001 to
       +0.003 per window), ridge 0.2675 against 0.2670. Training on later months is worth nothing measurable.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Random split as a stationary relation | as now; the definition gets the tag `StationaryRelation` and a `Time basis:` line: the sale month is in the data, and a split by month costs +0.001 RMSLE (0.147 against 0.146 at equal training size) | no change to the splits; the measured check is written down | the target is not flat (median price $290,000 in January, $320,000 by June), so the prototype rests on the nil cost alone |
     | b | Random split as a snapshot | as now, definition tag `Snapshot`; `Time basis:` the appraiser values 2016's unsold homes from 2016's sales | no change to the splits | the only house-sale table read as a fill-in; a valuation as of 1 January is already a date after the sales |
     | c | Five monthly windows | B above: August to December 2016, each trained on all earlier months | tests later sales, as a lender prices them; the regime of the other dated house sales | month resolution only; under a year of history |

   * **Recommendation:** c, the five monthly windows: the time is in the data and the use case prices later sales,
     they match house_sales and ames_housing, and neither random option buys anything, since
     the measured cost is nil. **Decision:** a, b or c?

   **Notes for the AI:** on c, B's notes above, without a gap: the windows are calendar months, longer than the time
   from a sale to its record[^1d]; record tag `Non-IID (Temporal)`. Once PR #50 is in: on b, `data_tags = ("Spatial",
   "Snapshot")` and a curation bullet `- Time basis: one year of sales (2016); the appraiser values the year's unsold
   homes from the same year's sales, so the test sales stand for homes of the same year.`; on a, `data_tags =
   ("Spatial", "StationaryRelation")` and a curation bullet `- Time basis: StationaryRelation: every sale is dated to
   its month of 2016 (month_sold); not split by month, because <the curator's reason>; five monthly windows (August to
   December, each trained on all earlier months) cost +0.001 RMSLE at equal training size (untuned LightGBM 0.147
   against 0.146; ridge 0.268 against 0.267), though the median price rises from $290,000 to $320,000 by June.` The
   frame has no date column, so no `meta_time_present_unused` warning to accept. Under every option the record gets
   the tags `Samples: Over Time` and `Time: Dated`.

   [^1b]: **SPLIT-32** (Should): how the data was collected is information for the split; the record's collection
     facts and, where one fits, the definition's use-case prototype with its `Time basis:` line.
     **SPLIT-14** (Must): at least 3 windows, none training on less than half of the data.
   [^1c]: **SPLIT-32** (Should), its prototypes: a use case that only fills in values for a time the data already
     covers is a `Snapshot`, and the line names the moment or the period.
   [^1d]: **SPLIT-10** (Should, amended 2026-11-04): no gap is needed where the time column's smallest step (sales
     dated by month) is longer than the label's delay; ames_housing and perth_house_prices.

   **Andrej (2026-11-11, change):** Reply (c): Five monthly windows

   **Resolved (2026-11-11, Andrej):** c, five monthly windows: `sale_month` (2016-MM-01, from `month_sold`) is the
   time column, `Temporal(on="sale_month", splits=TemporalSplits(window=1, unit="months", n_windows=5,
   min_train_fraction=0.5))`, no gap; test August to December 2016, trained on 58% to 92% of the sales. Repeat sales
   stay (13,932 rows, was 13,776; no exact copies). `split`, `use_case`, `row`, `fit_reason`, `splits_comment` and the
   notes rewritten; the record's `required_split` is Temporal (NON-IID) with the tag `Non-IID (Temporal)`.
   `dataset check`: 0 errors, 0 warnings (the 1-day span of each month-start window accepted, as perth_house_prices).

2. **Domain: `finance`, or `business & marketing` as the other house prices?**

   * **Problem:**
     - The record took the definition's `domain`, `finance`, by Andrej's field mark of 2026-11-04, while every other
       house-price record and definition uses `business & marketing`, including those whose use case names a lender.
     - The domains are kept one per family of siblings (Lennart, 2026-10-21, the ten QSAR records), and a record takes
       its definition's value (Lennart, 2026-10-26, aeolus).
     - Keep `finance` here, or change the definition so that the record follows?
   * **Background:** `business & marketing` is the domain of houses ("a lender or housing agency"), perth_house_prices
     ("for a lender or an agent"), sberbank_housing_market_forecasting ("lenders"), ames_housing, house_sales,
     california_house_prices_2020, melbourne_housing_market, zillow_prize and immoscout_german_house_prices.
   * **Effect on the task:** none on the data; the domain groups the datasets in the benchmark's summaries.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | `finance` (the field mark) | the definition and the record say `finance` | the record follows the definition | the only house sale outside `business & marketing` |
     | B | `business & marketing` | the definition's `domain` changes, the record follows | one domain for the house prices | a definition edit |
     | C | Move the lender-framed siblings to `finance` | houses, perth_house_prices and sberbank_housing_market_forecasting change too | a domain by use case | three more records and definitions change |

   * **Recommendation:** B: nothing sets Miami apart from the other house sales. **Decision:** A, B or C?

   **Notes for the AI:** the record's `domain` was left empty until this is decided; `problem_type` is set
   (Regression). On B: `domain = "business & marketing"` in `dataset.py` and the record, `dataset check`.

   **Andrej (2026-11-11, change):** Option B: business & marketing.

   **Resolved (2026-11-11, Andrej):** B: `domain = "business & marketing"` in `dataset.py` and the record.

## Reference

https://doi.org/10.1177/0042098020982508
