---
unique_name: brazilian_ecommerce
name: brazilian-ecommerce/
checked_by:
- Andrej
data_foundry_status:
- 'DF: Yes'
suggestion: 'Yes'
decision_markers:
- Needs extensive data wrangling
tags:
- Non-IID (Temporal)
- 'Samples: Over Time'
- 'Time: Dated'
- 'Target: Varying Delay'
- 'Entities: Recur'
- Dated Event Log
collections:
- New (BeyondArena)
original_source: Kaggle
year: '2018'
collection_period: Sep 2016 - Oct 2018
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce/data
v2_path: datasets/_dev/tabarena-v0pt2/brazilian_ecommerce/dataset.py
source_row: 705
type_adapter_id: curation-record-v1
---

## Comments

Data seems to be from a real company (Olist), a previous version even was classified. Possible tasks: predict future sales, optimize delivery times.
Multiple tables, requires feature engineering.
Uploaders commit to answering questions (awesome!)
Contains text fields (reviews)

**Assessment (AI, 2026-10-07):** Added as delivery time at checkout: log days from purchase to delivery (regression), with Olist's promised date as a feature and monthly temporal windows (March-July 2018). The data card suggests delivery performance; the uploader's own notebook frames review score instead, predicted from order data "up to delivery phase" (kaggle.com/code/andresionek/predicting-customer-satisfaction, 2018-10-24), the open alternative. Olist released "a simple random sample of all orders that received a customer review" (Kaggle discussion 66466); the last survey was sent on 2018-08-31, so August 2018 orders lost their slow deliveries and are cut. First published on Kaggle 2018-09-21 (the record says 2019). Licence: CC BY-NC-SA 4.0 (Kaggle card).

CC (2026-10-15, Lennart): Ship (review of the 2026-10-07 run) as implemented: the delivery time promised at checkout is the use case (a late-delivery flag would be a variant of it, the review score a satisfaction task); the one-month gap keeps the labels a refit would have; Olist's promised date stays an input known at checkout; the selection on answered reviews stays an anomaly note.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback rmse — A Kaggle dataset, not a competition: the data card suggests the delivery-time question but defines no metric; the task is our own.

**Assessment (AI, 2026-10-21):** metric now `Metric.from_context("rmsle", target_transform="log")` instead of the fallback rmse on the log target: a delivery time's error matters relative to the time; the target still ships as log, and RMSLE is computed after the inverse, on the original scale (MET-3). Needs a rebuild to reach the container.

CC (2026-10-21, Lennart): ship the target on the modelling scale, score on the original scale (target_transform).

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `jd_com_msom_2020_delivery_time` (TBD -> Yes, priority 3). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-17, Andrej): the declared split (temporal on `order_purchase_timestamp`, horizon 1 month, 5 windows, gap 1 month) is checked: the split decision tree, walked without the current split, reaches the split it ships (blind split walk, cross-dataset item).

## Review

**Outcome:** added as `brazilian_ecommerce`; re-audited 2026-11-27 against a fresh Kaggle v2 download (all 9 CSVs byte-identical, archive md5 matches): 88,721 rows, LightGBM RMSLE 0.483 against 0.642 for the dummy on all 5 monthly windows.

**Main points:** One decision: issue 1 (the gap's length). The split's leaf, the floor (56% to 87%) and the 33-unit minimum hold; the newest orders are not censored (undelivered share 1.2% to 2.9% by month, flat). Text fixes for the next edit: accept the new `splits_below_target` warning (5 windows against 9; the use case is a monthly refit, and 15-day windows would give 11); one sentence in `curation_comments` on the July cut (239 delivered July orders, 3.9%, promised after 2018-08-24 are dropped, median 11.3 days against 7.4 kept); `task_summary.predicted` says a median of 7.5 to 9 days, measured 7.4 to 9.2; the split bullet's "gap costs 0.04 to 0.06 R^2" measures about 0.03.

**Issues for Andrej and Lennart:**

1. **Shorten the gap from one month to 15 days?**

   * **Problem:**
     - Train ends one month before each test window; a delivery is known within 10.7 days at the median, 23.8 at p90 and 30.1 at p95, so the month covers p95.
     - Without a gap, a model that reads the purchase time as a number collapses (R^2 -0.036), so a gap is needed, but 15 days scores higher than the month.
   * **Effect on the task:** The month trains on older orders than a refit would have; it costs 0.03 to 0.06 R^2 against 15 days.
   * **Experiments:** untuned LightGBM, 300 trees, mean of the 5 windows.

     | Gap | R^2 with time as a feature | R^2 without |
     |---|---|---|
     | 0 days | -0.036 | 0.349 |
     | 15 days | 0.416 | 0.339 |
     | 30 days (now) | 0.354 | 0.315 |

   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | One month (implemented) | nothing changes | covers p95 of the label delay | older training data than the delay needs |
     | B | 15 days | `gap=15, gap_unit="days"` | covers p75 to p90, scores higher | about 10% of the last training orders are still in transit at a refit; rebuild and its own PR |

   * **Recommendation:** A: the gap stands for the labels a refit has, and only the month covers nearly all of them; the score is not a reason to shorten it. **Decision:** A or B?

   **Notes for the AI:** full audit and the horizon options in `local-data-warehouse/_runs/2026-11-26_review33/brazilian_ecommerce/findings_audit.md`. Unchecked: whether Olist revised a promise after purchase (one date per order).

## Reference

?
