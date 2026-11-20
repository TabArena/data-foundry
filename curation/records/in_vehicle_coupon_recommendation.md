---
unique_name: in_vehicle_coupon_recommendation
name: in_vehicle_coupon_recommendation
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: 'Yes'
decision_markers:
- Selection Bias
tags:
- 'Samples: Over Time'
- 'Time: Lost'
- 'Entities: Recur'
- Survey
original_source: Other
year: '2017'
required_split:
- Grouped (NON-IID)
source_links:
- https://www.researchgate.net/publication/318645502_in-vehicle_coupon_recommendation
- https://doi.org/10.24432/C5GS4P
notebook_path: datasets/beyond_iid/old_iid/in_vehicle_coupon_recommendation/in_vehicle_coupon_recommendation.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/in_vehicle_coupon_recommendation/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

CC (2026-09-30, Lennart): **Re-split as a cold-start task, grouped by survey respondent; ROC AUC 0.83 random -> 0.75 grouped.** Wang et al. 2017 (JMLR 18), Sec. 6.2: MTurk survey, 652 accepted surveys, 12,684 rows; "In the first part of the survey, we asked users to provide their demographic information and preferences. In the second part, we described 20 different driving scenarios ... to each user"; evaluated with random 5-fold testing (Table 3), i.e. warm start. The file has 22 scenarios per person from 19 fixed questionnaire versions, answered in one sitting without timestamps, so there is no interaction history to simulate a warm start; a random split lets a model learn each person's tendency to say yes from their other hypothetical answers. We simulate a cold-start model (as used before a recommender has history for a user): new people, known profile and stated habits (the visit-frequency columns are the base preference). The respondent id is not shipped; the raw file lists each respondent's answers as one consecutive block with identical first-part answers (13 columns), giving 587 groups (517 of 22 rows; a few blocks likely merge two adjacent respondents with identical profiles, which is stricter). The audit's profile-only id (567 groups) merged different people. LightGBM on the grouped splits: AUC 0.75 (0.742-0.764 over 6 folds). TabArena v0.1 dataset: results on the old IID container are not comparable.

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

data was collected via a survey on Amazon Mechanical Turk. The survey describes different driving scenarios including the destination, current time, weather, passenger, etc., and then ask the person whether they will accept the coupon if they are the driver. features might be time invariant, but need to check

Potential issue: "faked" data via a survey

Lennart: Leaning towards yes, features seem time invariant; but data source might be fake

Andrej: Need to test whether time-invariant; Mechanical turk data might be interesting to include

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source roc_auc — AUC (out-of-sample, 5-fold, Table 3) (Wang et al. (2017), A Bayesian framework for learning rule sets for interpretable classification, JMLR 18(70), Sec. 6.2 and Table 3).

CC (2026-10-27, Lennart): marker Selection Bias, from the AI review of PR #16: the respondents are Amazon Mechanical Turk workers, a volunteer sample rather than the drivers of an in-vehicle recommender, as the web volunteers of obesity_estimation; the stated intentions about imagined trips are a separate gap, already in the fit_reason.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): 8 ordinal scales typed as ordered categories in the codebook's order (CLEAN-14, amended): `age`, `education`, `income`, `Bar`, `CoffeeHouse`, `CarryAway`, `RestaurantLessThan20`, `Restaurant20To50` (the README lists their levels).

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `tianchi_o2o_coupon_redemption` (TBD -> Yes, priority 2). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-01, Lennart): the decode rule (a code whose codebook says in words what each level is carries the words; a score without them is a number): 1 coded columns carry their words.

CC (2026-11-18, Andrej): time basis `ForcedGroupedFromTemporal` in place of `Timeless` (Review issue 2, B; full-information split check): the recommender serves drivers after the survey, which keeps no interview order, so the forced step holds out whole respondents. The split is unchanged.

CC (2026-11-18, Andrej): collection facts `Samples: Over Time` and `Time: Lost` in place of `Samples: No Time Dimension`, with the time basis `ForcedGroupedFromTemporal`: the respondents answered one by one during the 2017 survey, and the release keeps no interview date or order.

CC (2026-11-18, Andrej): the forced tag stays (Review issue 3, A; stationarity reasoning, SPLIT-32 as amended today): no reason to take later samples as interchangeable. A consumer-offer task from a 2017 MTurk sample used on later real drivers, with file-order structure; Andrej moved it to forced today and nothing in the mechanism argues for interchangeability.

## Review

**Outcome:** added. Full-information split check of 2026-11-18: the time basis tag disagreed with the split tree; decided below.

**Main points:** Tag the respondent folds `ForcedGroupedFromTemporal` instead of `Timeless`?

**Issues for Andrej:**

2. **Tag the respondent folds `ForcedGroupedFromTemporal` instead of `Timeless`?**

   * **Problem:**
     - `Timeless` is for a fixed property of an item with no time dimension[^s32q1]; a driver's answer to a coupon is neither, and the tree's survey branch has no `Timeless` leaf.
     - The use case is a recommender that meets new drivers after the survey, which the survey branch walks as later respondents with no interview order: forced, held out by respondent.
     - The folds stay as they are (587 respondents rebuilt from the file's blocks); the tree's example list puts the dataset under `Retrospective` (sampling cluster), the reading in which the survey's own respondents are filled in.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Grouped by respondent, `Timeless` (implemented) | No change | | No leaf gives it |
     | B | The same folds, `ForcedGroupedFromTemporal` | The Time basis line names the undated 2017 survey and later drivers as untested | Matches the recommender's forward use | |
     | C | The same folds, `Retrospective` | The line names the survey's own time | Matches the tree's example list | Reads the recommender as filling in the survey |

   * **Recommendation:** B, because the recommender serves drivers after the survey, as ai4d's trip planner did. **Decision:** A, B or C?

   [^s32q1]: **SPLIT-32** question 1 (Should): `Timeless` only when "the target is a fixed property of the item, the same whenever it is measured ..., and the data has no time dimension".

   **Andrej (2026-11-18, change):** Option B: The same folds, ForcedGroupedFromTemporal.

   **Resolved (2026-11-18, Andrej):** B. `data_tags` names `ForcedGroupedFromTemporal` in place of `Timeless`, and the `Time basis:` line opens with it: the recommender meets new drivers after an undated survey with no interview order, so whole respondents are held out. The folds are unchanged (587 respondents).

3. **Keep `ForcedGroupedFromTemporal`, or tag `AssumedStationaryRelation`?**

   * **Problem:**
     - Time: The 2017 MTurk survey is undated and keeps no interview order; the file order is the 19 questionnaire versions (Coffee House share 38-43% of the first deciles to 13.5% of the last), so order measures design, not time.
     - Use: An in-vehicle recommender shows coupons to new drivers after the survey, years later if deployed today.
     - Mechanism: Stated acceptance depends on scenario (venue, distance, time, weather, expiry) and on the person's habits; venue habits, prices and coupon economics change (e.g. dining out and commuting after 2020), and stated intent stands in for redemption.
   * **Background:** similar datasets[^asr].

     | Similar dataset or source | What was measured | Verdict | Why similar |
     |---|---|---|---|
     | online_shoppers_purchasing_intention_dataset | v3 stationary-relation test over the visit months; December trained on June-November costs 0.009 ROC AUC; purchase share 10% (June) to 25% (November) | not flat | consumer purchase behaviour scored for a later period |
     | Gama et al. 2014, 'A survey on concept drift adaptation', ACM Computing Surveys 46(4) | review of drift in deployed predictors; customer profiling, marketing and telecom are named application areas with changing populations and behaviour | not flat (domain-level) | same use: scoring customers of a later period |

   * **For a stationary use case:**
     - Situational factors (detour distance, expiry, passengers, weather) have a plausibly durable effect on accepting an offer.
     - One sitting per respondent: within-survey order effects are small (3-4 pp residual drift over the file, Spearman -0.034).
   * **Against:**
     - Coupon response is consumer behaviour under prices and markets; venue habits changed markedly after 2020.
     - MTurk respondents of 2017 stand in for drivers of a deployed system (changed intake).
     - Structure in the file order (questionnaire versions; residual 3-4 pp acceptance drift).
     - Stated intent, not redemption.
   * **Earlier views:**
     - CC (2026-09-30, Lennart): re-split as cold start, grouped by respondent (0.83 random -> 0.75 grouped).
     - CC (2026-11-18, Andrej): ForcedGroupedFromTemporal in place of Timeless (issue 2, B), collection facts Samples: Over Time, Time: Lost.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep `ForcedGroupedFromTemporal` (implemented) | The folds stay; the Time basis line names the reasoning below | Claims only what is known | The split stands for later samples only as far as the use case is stationary |
     | B | `AssumedStationaryRelation` | The folds stay; you give the reason (eight words or more) | Documents why random folds stand for later samples | Coupon response is consumer behaviour under prices and markets; venue habits changed markedly after 2020.; MTurk respondents of 2017 stand in for drivers of a deployed system (changed intake). |

   * **Recommendation:** A, a consumer-offer task from a 2017 MTurk sample used on later real drivers, with file-order structure; Andrej moved it to forced today and nothing in the mechanism argues for interchangeability. Confidence: high. **Decision:** A or B?

   [^asr]: **SPLIT-32** (Should; amended 2026-11-18, Andrej): "where it holds none, the review reasons whether the use case can be taken as stationary, from the domain's mechanism and from similar datasets ..., where the AI offers `AssumedStationaryRelation` with a recommendation for a person to decide." `AssumedStationaryRelation` keeps the forced split's folds and replaces only the tag; its line opens `AssumedStationaryRelation (<person>, <date>): <reason>`.

   **Andrej (2026-11-18, ok):** as implemented.

   **Resolved (2026-11-18, Andrej):** A, as implemented: the forced tag stays; the `Time basis:` line gives the reasoning (A consumer-offer task from a 2017 MTurk sample used on later real drivers, with file-order structure; Andrej moved it to forced today and nothing in the mechanism argues for interchangeability.)

## Reference

A Bayesian framework for learning rule sets for interpretable classification By Wang, Tong, Cynthia Rudin, Finale Doshi-Velez, Yimin Liu, Erica Klampfl, and Perry MacNeille. 2017
 Published in The Journal of Machine Learning Research 18, no. 1
