---
unique_name: food_delivery_time
name: Food_Delivery_Time
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: No (Retired)
decision_markers:
- AHDS (Artifical/Handmade/Deterministic/Simulated)
tags:
- Random (IID)
original_source: Other
year: '2022'
domain: business & marketing
required_split:
- Random (IID)
problem_type: Regression
source_links:
- '# the first publication: HackerEarth hiring challenge for Amazon business research analysts, 26 Aug-5 Sep 2022'
- https://assessment.hackerearth.com/challenges/hiring/amazon-business-research-analyst-hiring-challenge/
- '# the challenge files as copied to Kaggle while it ran: one text file per order, 45,593 train, 11,399 test'
- https://www.kaggle.com/datasets/syednusrath/amazon-business-research-analyst
- '# the challenge files as two 20-column CSVs (2022); its provenance field names the HackerEarth competition'
- https://www.kaggle.com/datasets/gauravmalik26/food-delivery-dataset
- '# the 10-column cut of that train.csv we shipped (2023)'
- https://www.kaggle.com/datasets/rajatkumar30/food-delivery-time
notebook_path: datasets/beyond_iid/old_iid/food_delivery_time/food_delivery_time.ipynb
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Predict the time taken by the delivery person to deliver the food. Spatial. Requires special feature engineering. Might need to exclude delivery person ID. Might require temporal split; might require groups/temporal splits for delivery person ID

Potential issue: spatial data must be verifyied

Lennart: Yes, if we do some spatial feature engineering (like distance) and can ignore delivery person subgroups

Andrej: Special feature engineering necessary. Unclear whether the license is fine.

Split regime is ambiguous, so both tags are set. As shipped the dataset is IID, which contradicts the
`Non-IID (Temporal)` tag the record carried alone. The TabArena (v0.1) notebook
(`datasets/_maintenance/_old_collections/tabarena-v0pt1/food_delivery_time/food_delivery_time.ipynb`) sets
`data_tags=["IID"]`, shuffles the rows and exports the default IID splits; the BeyondArena copy under
`datasets/beyond_iid/old_iid/food_delivery_time/` is identical. The Kaggle release has no timestamp at all
(10 columns: delivery person ID/age/rating, restaurant and delivery lat/long, order type, vehicle type, and
the target), so a temporal split cannot be built from the shipped data without recovering a time index. The
only non-IID structure available is the delivery person grouping, 1320 IDs over 45,451 rows, which the
notebook records as an anomaly: using that ID as a feature may call for a cold-start (grouped or temporal)
split instead. The temporal tag reflects that open question, not the protocol the dataset actually ships with.

**Assessment (AI, 2026-10-14):** the delivery point is always the restaurant plus one of 12 equal offsets in latitude and longitude (0.01-0.14 degrees), so delivery addresses are synthetic. 424 rows (0.9%) have the restaurant latitude sign flipped (159 also the longitude); the same restaurants appear with positive coordinates. 3,630 rows (8%) have the restaurant at (0, 0), a missing code; their mean time is 26.1 min against 26.3. Blanking them costs about 0.09 RMSE, dropping them nothing.

CC (2026-10-14, Lennart): Flip the signs, keep the (0, 0) rows and document the synthetic offsets.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback rmse — Kaggle dataset without a competition or paper; the data card states the task but no metric.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `meituan_food_delivery_time` (TBD -> Yes, priority 4). Each is screened in its own record; this record's verdict stays the curator's.

**Assessment (AI, 2026-11-04):** reviewed for the BeyondArena v0.2 review page, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the record's Review. Retire as generated data: in the shipped file and its 20-column parent the minute within each 5-minute block is uniform noise, every other column changes only at block edges, and a courier ID holds a median of 17 different ages. Priority 1: gap 0, use case 0, source 0, shape 1, risk -1.

CC (2026-11-05, Andrej): retired as generated data (`No (Retired)`, `AHDS`). The data: 45,451 food deliveries of an unnamed Indian platform (Kaggle, rajatkumar30, 2023), a 9-column cut of an earlier 20-column upload with no documented origin (gauravmalik26, "Food Delivery Dataset", https://www.kaggle.com/datasets/gauravmalik26/food-delivery-dataset).
- **The delivery time is drawn as a 5-minute block plus a random minute:** the minute within each block is uniform (19.6% to 21.2% of the orders in every block) and no feature predicts it (LightGBM R² -0.074 against -0.075 for shuffled minutes), while every other column changes only at the block edges (of the courier age's variance across delivery minutes, 0.0006 of 0.103 lies within blocks).
- **The couriers are not people:** none of the 1,320 courier IDs keeps one age, rating or vehicle (medians of 17 ages, 9 ratings and 3 vehicle types over 41 orders), and a courier's age follows the delivery time of the order (4.2 years below the courier's mean at 10-14 minutes, 3.0 above it at 50-54).
- **Other parts were already known to be made, and the larger file shares the marks:** delivery points are the restaurant plus one of 12 equal offsets (2026-10-14); in the 20-column file age 29 and rating 4.6 fill the missing entries, and its weather, traffic and order times follow the same block rule, so a rebuild from it is no way out.
Record fields `problem_type` (Regression) and `domain` (business & marketing) set from the definition. A real source for the task, `meituan_food_delivery_time`, is screened in its own record.

**Assessment (AI, 2026-11-12):** source found. The rows were first published as the data of a HackerEarth hiring challenge for Amazon business research analysts ("Business Research Analyst Assessment", 26 August to 5 September 2022, https://assessment.hackerearth.com/challenges/hiring/amazon-business-research-analyst-hiring-challenge/), so `original_source` is now `Other` and `year` 2022 (PROV-8, PROV-9).
- **The challenge:** its statement, as copied to Kaggle while the challenge ran (syednusrath, 2022-08-27): "You are working as a data scientist at a food delivery company. [...] Develop a machine learning model that can calculate the time taken by the delivery person to deliver the order", scored by 100 × R². The files hold one text file per order, 45,593 training orders and 11,399 test orders without labels. The statement names no company whose orders these are, so "an unnamed Indian platform" and "no documented origin" in the CC of 2026-11-05 no longer hold. The challenge page shows the dates but not the statement; the statement is quoted from the Kaggle copies. Nothing in the origin says how the rows were made (no company, place, period or collection method, and no word on real or generated data), so the `AHDS` call rests on the tests above alone.
- **The chain to the file we shipped:** gauravmalik26 joined the challenge files into two 20-column CSVs (2022; Kaggle provenance field: "This dataset is gathered from machine learning competition conducted by HackerEarth."). rajatkumar30's 10-column file (2023) is that train.csv row for row: all 45,593 rows keep the courier, the restaurant latitude and the delivery time, and 1,565 IDs were turned into numbers by a spreadsheet (0x3e60 became 3E+60).
- **The 142 rows the definition dropped as duplicate IDs were distinct orders:** their IDs are unique in the challenge file and collided only after the spreadsheet conversion. The source changes nothing in the `AHDS` evidence above.

## Review

**Outcome:** added; recommended `No` (`AHDS (Artifical/Handmade/Deterministic/Simulated)`). The 45,451 food deliveries
of an unnamed Indian platform (Kaggle, rajatkumar30, 2023): the delivery time in minutes from the courier's ID, age,
rating and vehicle, the order type and the restaurant and delivery coordinates. Reviewed on 2026-11-04 without a review
panel, from the gathered evidence (the record, model runs on the TabArena v0.1 task of the same rows) and
three checks of today on the shipped file and the earlier 20-column Kaggle file it was cut from. Validity: the rows
carry the marks of a generator, not of deliveries (issue 1): the minute within each 5-minute block of the delivery time
is uniform and unrelated to every feature, every other feature's distribution is constant within a block and jumps at
its edges, and a courier ID holds a median of 17 different ages over its orders, older on slow deliveries. Two parts
were already known to be made: the delivery point is the restaurant plus one of 12 offsets (2026-10-14), and age 29 and
rating 4.6 fill the earlier file's missing entries. Value: on the TabArena v0.1 task of the same rows the benchmark
methods
spread modestly (RMSE 7.20 best, 7.48 median, 8.28 to 8.56 for linear models), and a lookup over four banded drivers
ranks first of 94. Quality: the shipped file drops the order date and time, weather, traffic, festival and city of the
file it was cut from, which lift R² from 0.35 to 0.79. Weighed: a common, real task +, data that fails the test of being
real -, a cut-down copy -; a real source for the task (`meituan_food_delivery_time`, 568,546 Meituan orders) is screened
in its own record.

**Main points:** Retired as generated data (2026-11-05, issue 1); record fields set.

**Record judgment:** not valid as real data. The table is a 9-column cut of an earlier Kaggle upload (gauravmalik26,
"Food Delivery Dataset", 20 columns, orders dated 11 February to 6 April 2022) whose own origin is not documented: at
least 44,028 of the 45,451 shipped rows (96.9%) appear there under the same ID with the same time, coordinates, age and
rating. The generator's marks run through both files.

**Issues for Andrej:**

1. **Retire as generated data?**

   * **Problem:**
     - In the shipped file and in the 20-column file it was cut from, the minute within each 5-minute block of the
       delivery time is uniform and unrelated to every column, while every other column changes only at the block
       edges, as when a generator draws a time block, then the columns for it, then the minute.
     - The courier columns behave the same way: no courier ID keeps one age (a median of 17 ages over 41 orders), and a
       courier's age and rating move with the delivery time of the order.
     - Retire as generated data, keep it, or rebuild it from the 20-column file?
   * **Background:** a dataset is real, not generated and not a real table reworked, and data that does not come
     from a real distribution is out[^d2-1a]. Real delivery times would let traffic, distance, weather and the courier
     shift the time smoothly; here each column's mix is the same for 25 and 29 minutes and changes between 29 and 30.
     The rating does change inside a block, at a fixed cut: ratings below 4.5 are 4% of the orders taking 30 minutes
     and 56% of those taking 31. The delivery point is the restaurant plus one of 12 equal offsets
     in latitude and longitude (2026-10-14, Lennart: the offsets documented as synthetic).
   * **Experiments:** today's checks, on all rows:
     - The minute within the block, U (0 to 4): each value holds 19.6% to 21.2% of the orders in every block; LightGBM
       predicting U from all shipped features scores R² -0.074 against -0.075 for shuffled U (3 folds), while the block
       itself is predicted at R² 0.35.
     - The share of a column's variance across delivery minutes that lies within blocks: courier age 0.0006 of 0.103,
       the distance offset 0.0005 of 0.121, and in the 20-column file traffic density 0.0007 of 0.042, weather 0.0010
       of 0.048, vehicle condition 0.0007 of 0.077. The share of orders in low traffic falls block by block from 0.61
       (10-14 minutes) to 0.00 (45 minutes and more).
     - Per courier ID (1,320 IDs, a median of 41 orders): none has a single age, rating or vehicle type (medians 17
       ages, 9 ratings, 3 vehicle types); within a courier the age is 4.2 years below the courier's mean on 10-14
       minute deliveries and 3.0 above it on 50-54 minute ones, and the rating 0.08 above the mean at 30 minutes and
       0.25 below it at 31.
     - The 20-column file's extra columns lift LightGBM from R² 0.35 (RMSE 7.57) to 0.79 (RMSE 4.25) on the same rows
       (3 seeds x 3 folds), with the same block pattern.
   * **Effect on the task:** a model scores by recovering the generator's block rule, not how deliveries take time;
     the uniform minute adds 2.0 min² of variance that no input can predict.
   * **Consistency:** follows churn (retired 2026-10-06, Lennart: artificial data, its distributions shared across
     call periods) and customer_satisfaction_in_airline (retired 2026-10-01, Lennart: ratings copied within customer
     segments)[^d2-1b]. The record's `Duplicate` copy (`food_delivery_time_duplicate`) is no precedent either way.
   * **Unknown:** who made the 20-column file; its Kaggle page names no platform, and an alternative reading (real
     5-minute bands with noise added by an uploader) fails on the couriers' changing ages and on the rating's cut
     inside a block.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep as defined (implemented) | 45,451 orders, 9 columns, random split, RMSE | a common task with a real shape; methods spread a little | the rows are generated: the minute is noise and the columns follow a block rule |
     | B | Retire | the record gets `No (Retired)` with the `AHDS` marker and a CC line; the folder goes | no generated data in the benchmark; the real Meituan orders are screened for the same task | one fewer delivery task until a real one is added |
     | C | Rebuild from the 20-column file | order date for a temporal split; weather, traffic, festival, city and order times as features | the columns the cut dropped; a split by date | the same generator's marks run through the extra columns |

   * **Recommendation:** B: the data fails the test of being real data, and the richer file shares the same marks.
     **Decision:** keep (A), retire (B), or rebuild from the 20-column file (C)?

   **Notes for the AI:** on B, set the record's `suggestion` to `No (Retired)`, add `AHDS (Artifical/Handmade/
   Deterministic/Simulated)` to `decision_markers`, write a `CC (<date>, Andrej)` line with the numbers of this issue
   and the 20-column file's link (https://www.kaggle.com/datasets/gauravmalik26/food-delivery-dataset), add `Andrej` to
   `checked_by`, remove the folder, clear `v2_path`, and add a CHANGELOG entry.

   [^d2-1a]: **PROV-3** (Must): the data is real: not generated, and not a real table someone reworked (relabelled,
     columns renamed, values replaced). **SEL-16** (Must): data that does not come from a real random distribution is
     out: artificial (synthetic, toy), handmade or deterministic data.
   [^d2-1b]: The two precedents are in the records of churn (CC 2026-10-06, Lennart) and
     customer_satisfaction_in_airline (CC 2026-10-01, Lennart).

   **Andrej (2026-11-05, change):** Retire it and articulate the reason in the record.

   **Resolved (2026-11-05, Andrej):** retired as generated data (B): the record is `No (Retired)` with `AHDS`, and its CC
   line gives the generator's marks (the uniform minute within each 5-minute block, the other columns changing only at
   the block edges, couriers whose age follows the delivery time) and why the 20-column file is no way out. Record
   fields `problem_type` and `domain` set from the definition. The folder stays until this file is committed.

## Reference

HackerEarth, Amazon Business Research Analyst hiring challenge ("Business Research Analyst Assessment"), 26 August to 5 September 2022:
https://assessment.hackerearth.com/challenges/hiring/amazon-business-research-analyst-hiring-challenge/

Kaggle copies: the challenge files (2022), the 20-column CSVs (2022), the 10-column file we shipped (2023):
https://www.kaggle.com/datasets/syednusrath/amazon-business-research-analyst
https://www.kaggle.com/datasets/gauravmalik26/food-delivery-dataset
https://www.kaggle.com/datasets/rajatkumar30/food-delivery-time
