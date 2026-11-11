---
unique_name: santander_transaction_value
name: Santander_transaction_value
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
decision_markers:
- Anonymized
tags:
- Non-IID (Grouped)
- 'Samples: Over Time'
- 'Time: Lost'
- 'Time: Within Entity'
- 'Target: Later'
- 'Entities: Recur'
collections:
- TabArena Reject
- TabSTAR
original_source: Kaggle
year: '2018'
domain: finance
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/competitions/santander-value-prediction-challenge
notebook_path: datasets/beyond_iid/new_iid/santander_transaction_value/santander_transaction_value.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/santander_transaction_value/dataset.py
source_row: 663
type_adapter_id: curation-record-v1
---

## Comments

CC: "From Kaggle competition. Original task was rather time-series & some weird feature engineering was applied in the competition. It is very likely that there are leaks. Might rather use the preprocessed version of Tschalzev et al. Not included in TabRepo. Various issues in the dataset, but with the right preprocessing might be usable"

Follow preprocessing of Tschalzev et al. and check if splits are usable as IID

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source rmse — Root Mean Squared Logarithmic Error (RMSLE) (https://www.kaggle.com/competitions/santander-value-prediction-challenge/overview/evaluation).

**Assessment (AI, 2026-10-21):** metric now `Metric.source("rmsle", target_transform="log1p")` instead of rmse on the log1p target: the competition's RMSLE on the raw transaction value, computed after the inverse of the shipped log1p (MET-3); the score is the same number as before. Needs a rebuild to reach the container.

CC (2026-11-11, Andrej): review marks, applied on the newer framework, which still had the random split. Issue 1 (D, "Customers by the exact key and confirmed sparse matches"): the customer is rebuilt in `_customer_key` from the raw lag columns (exact links need 3 or more non-zero shifted values no other row shares, 34,635 links; sparse links count when a later row's lag column holds an earlier row's exact target and neither row has another match at that shift, 4,371 links), and the split is `Grouping(on="customer", ...)` with `ForcedGroupedFromTemporal`: 710 customers over 4,447 rows. Issue 2 (B): a `Time basis: ForcedGroupedFromTemporal:` bullet says what dated snapshots would change. Issue 3 (B plus `Time: Within Entity`): the record's facts are `Time: Lost` in place of `Time: Dated`, plus `Time: Within Entity`; `required_split` Grouped (NON-IID) and the tag `Non-IID (Grouped)` in place of `New IID`. `dataset check`: 0 errors, 0 warnings; not rebuilt.

## Review

**Outcome:** added. The training file of Santander's Value Prediction Challenge (Kaggle, 2018): 4,459 customers with
4,991 anonymised columns, reduced to 540 row summaries over groups of columns (the preprocessing of Tschalzev et al.,
"A Data-Centric Perspective on Evaluating Machine Learning Models for Tabular Data", NeurIPS 2024 Datasets and
Benchmarks, https://arxiv.org/abs/2407.02112), 4,447 rows after dropping copies; the target is the transaction value,
scored by the competition's RMSLE. The AI recommends shipping it only after one change, grouping the rows by customer
(issue 1); without it, not shipping. Reviewed on 2026-11-04 without a panel, from the gathered evidence (the record,
a model run on the shipped data, which has the same 540 summaries and random split as v0.2) and two checks on
the raw file. Validity: the rows are snapshots of the same customers at different times, and a later snapshot holds
this row's target among its lag columns. In the raw file 72% of the rows have such a later snapshot; the summaries
keep enough of the link for a model to cut the error by 8.8%. An exact key from the shifted columns groups
the snapshots of each customer and leaves no linked snapshot on the other side. Value: the benchmark methods range from
RMSLE 1.306 (LimiX-2) over 1.345 (median) to 1.40-1.49 (linear models) against a target spread of 1.75. Quality:
the target's unit and time window are not stated, and the columns are anonymised (marker set). Weighed: Santander's
own data and metric +, a real time structure +, a strong cross-row leak under the random split -, an exact key that
removes it +, no dates and a small file -.

**Main points:** Grouped by customer (issue 1, decided: D, the exact key and the confirmed sparse matches);
ship (Andrej, 2026-11-06), with the split and the metric checked as declared; the container is not rebuilt yet. Settled on
2026-11-10: the `Time basis:` bullet on what dated snapshots would change (issue 2), and the record's facts `Time:
Lost` and `Time: Within Entity` (issue 3).

**Record judgment:** valid as data (real snapshots of real customers, anonymised by the host); the random split of
the review let a later snapshot give the target away, and the split holds out whole customers since 2026-11-06.

**Issues for Andrej:**

1. **Group the rows by customer through the shifted columns, or retire?**

   * **Problem:**
     - The training file holds several snapshots of one customer, one or more time steps apart, and a later snapshot carries this row's target among its lag columns (the time-shift leak of the competition).
     - The 540 summaries keep enough of it that a model read the target of about a quarter of the test rows and cut the error by 8.8%, and under the random split most test rows have a later snapshot in training.
     - Group the splits by customer, with the groups built from exact shifted values, or retire the dataset?
   * **Background:** 40 columns hold a customer's past transaction values, two to 41 steps back; the definition's own
     search finds 11 more ordered groups of 40 columns. Two snapshots k steps apart agree on every group once it is
     shifted by k columns, which gives an exact key without labels. The file has no dates, so the split is forced
     from temporal, and a forced split ships only when nothing crosses it[^1a]. The competition asks for the value of
     potential customers, so a customer the model has seen does not stand for the use case.
   * **Experiments:**
     - Raw file (checks of 2026-11-04): for k = 1 to 39, rows whose 12 groups match another row's after a shift of k
       columns (unique keys with at least 3 non-zero values): 1,436 one-step pairs and 33,199 pairs with k of 2 or
       more. In 33,195 of these the later row's lag column equals the earlier row's target exactly, against 284 when
       the target is a random other row's. 3,202 of 4,459 rows (72%) have such a later snapshot.
     - Under random 3-fold splits (3 repeats) 66.5% to 69.6% of test rows have a later snapshot in training. Grouped
       by the one-step chains the definition already computes, still 66.4% (they miss snapshots with a step
       missing between them). Grouped by the components of all k-step links, 0%: 1,196 groups, 957 single rows, 239
       customers with 2 to 104 snapshots.
     - Model runs on the shipped data (same summaries, random split): a generator that rebuilds the chain from
       the summaries takes TabPFN-3.5 from RMSLE 1.319 to 1.202 on all three climb splits (held out: -7.5% on 6 of 6
       splits), exact for the 521 rows whose next two snapshots are both in the file, and puts it first of the 38
       benchmark methods, 7.6% ahead of the best; no generator without the leak improved the model.
   * **Effect on the task:** under the random split a method gains by recovering the target from later snapshots,
     which do not exist when a new customer is scored.
   * **Consistency:** a forced grouped split follows nba_players_2016_2019 and open_university_learning_analytics,
     which are stacked periods grouped by entity[^1b]; retiring follows how_much_did_it_rain, where the leak across
     the forced split could not be removed[^1a].
   * **Unknown:** whether the summaries leave a route through rows that the key cannot link (lag columns with fewer
     than 3 non-zero values); rerunning the chain feature found earlier on the grouped splits would settle it.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random customers (implemented) | random 3x3 folds; tag forced IID from temporal | the BeyondArena task unchanged | about 69% of test rows have a later snapshot in training; target read exactly for some |
     | B | Grouped by customer | components of the exact k-step links as groups; tag forced grouped from temporal | no linked snapshot crosses the split; new customers, as the competition asks | the key is built in the definition from the raw columns; the leak test on the summaries is still to run |
     | C | Retire | record `No`, folder removed | no leaky task in the benchmark | loses a real regression with a time structure that can be grouped |

   * **Recommendation:** B: the key is exact and needs no labels, it removes every target-revealing snapshot found,
     and new customers are the competition's question; retire (C) only if the rerun of the chain generator still
     finds the target on the grouped splits. **Decision:** group by customer (B), keep random customers (A) or retire
     (C)?

   **Notes for the AI:** on B, build the groups in `_clean` from the raw frame, before the summaries: after the three
   passes of `add_new_feature_sets`, take the 12 ordered groups (the 40 listed columns and `extra_features`); for k in
   1..39 hash each row's values `g[:-k]` and `g[k:]` over all groups, keep keys that are unique on their side and hold
   at least 3 non-zero values, join, and take the connected components (the check of 2026-11-04 did exactly this
   and gave 1,196 groups on the raw file). Carry the group through
   `drop_duplicates` as a `customer` column, declare `grouping = Grouping(on="customer", labels="per_sample",
   prediction_unit="row", context="none", definition=...)`, set `data_tags = ("Anonymized",
   "ForcedGroupedFromTemporal")`, rewrite the `ForcedIIDFromTemporal` note, the task summary's `split` and
   `fit_reason`. Record: `required_split` to `Grouped (Non-IID)`, a `CC` line. Rebuild, then rerun the chain feature
   (a customer's earlier snapshots linked by the shifted columns) on the new splits as the leak test.

   [^1a]: **SPLIT-8** (Must): a task temporal in nature whose release cannot give the windows ships in the closest
     regime that keeps the rows, tagged as forced from temporal, IID or grouped by the entity; a forced split ships
     only when a leak test across the split finds none, and where it finds one, as in how_much_did_it_rain, the
     dataset is `No`. **LEAK-17** (Must): repeated entities in different rows leak the target across the split even
     when the rows differ; group them.
   [^1b]: **SPLIT-24** (Must): group on a true group id or on one constructed exactly from the data, never on a
     similarity threshold. SPLIT-8 cases: nba_players_2016_2019 and open_university_learning_analytics_dataset,
     stacked and grouped by player or module-presentation, `ForcedGroupedFromTemporal` (2026-10-21, Lennart).

   **Andrej (2026-11-05, discuss):** B sounds right, but how many groups would we get and how many samples per group
   would there be. Also, did the original competition use the same split?

   **Answer (AI, 2026-11-05):**

   * **Your question:** how many customers B's key finds in the 4,447 shipped rows and how many rows each holds, what
     that does to the folds, and whether the competition split its files by customer too.
   * **Groups:** the key exactly as the notes describe it, rebuilt on the raw training file and carried through the
     definition's removal of copies:
     - 1,184 customers: 945 with one row (21% of the rows) and 239 with 2 to 104 rows, which hold the other 79%.
       Median 1 row per customer, mean 3.8, maximum 104; among the 239, median 6 and mean 14.7. Half of the rows
       belong to customers with 25 rows or more.
     - The 12 rows dropped as copies are all one-row customers whose copy belongs to another customer, so the 239
       customers with several rows keep all their rows.
     - The key leaves sparse customers apart (see what B's key misses, below); a fuller key (D) joins them and
       gives 710 customers, 414 of them with one row (9% of the rows).

     | Rows per customer | B: customers | B: rows | D: customers | D: rows |
     |---|---|---|---|---|
     | 1 | 945 | 945 | 414 | 414 |
     | 2 | 53 | 106 | 57 | 114 |
     | 3 to 5 | 64 | 241 | 81 | 306 |
     | 6 to 10 | 34 | 254 | 54 | 413 |
     | 11 to 25 | 40 | 706 | 52 | 865 |
     | 26 to 50 | 32 | 1,107 | 36 | 1,242 |
     | 51 to 104 | 16 | 1,088 | 16 | 1,093 |
     | all | 1,184 | 4,447 | 710 | 4,447 |

   * **Folds:** 3 repeats of 3 folds. Each row has its own target, so the protocol counts rows: 2,964 on the
     training side gives 3 repeats (counted in customers it would be 10 under B and 20 under D).
     - A fold gets a third of the customers (394 or 395 under B), not a third of the rows, so its size follows the
       large customers it draws: 1,289 to 1,621 test rows on the protocol's three seeds against 1,482 for equal
       folds, and 987 to 2,111 over 1,000 seeds (90% of folds between 1,219 and 1,751). The largest customer is 4% to
       8% of a test fold, at most 10% over the 1,000 seeds. D gives the same spread (1,213 to 1,920 on the
       protocol's seeds, 236 or 237 customers per fold).
     - No test row has a linked later snapshot in training in any of the 9 folds, under B or D. Under random
       splits 69% to 71% of test rows have one.
   * **What B's key misses:** it links two rows only on shifted values that hold 3 or more non-zero values and that
     no other row shares, so a customer with one or two values in the 480 lag columns stays apart from its other
     snapshots.
     - Reading a test row's target from the lag column of a training row that matches it at any shift, as the
       competitors did, gives the exact target of 103 to 145 test rows per grouped fold (7% to 11%; 6 to 9 by
       chance), against about 1,100 per random fold (72% to 75%). These are sparse rows: the 528 rows read in any
       of the 9 folds have a median of 2 non-zero lag values, and 379 of them are one-row customers under B.
     - Joining every sparse match puts 75% of the rows into one customer, because a single value such as 2,000,000
       matches many unrelated rows. D joins a sparse match only when the later row's lag column holds the earlier
       row's exact target and neither row has another such match at that shift: 4,371 links, 85 to 110 when the
       targets are shuffled. The largest customer stays at 104 rows, and the readable test rows fall to 19 to 32 per
       fold (1% to 3%; 5 to 10 by chance).
     - These counts are on the raw columns; whether the 540 summaries keep the route is the leak test still to run.
   * **The competition's split:** by customer, as in B.
     - The files: train.csv with 4,459 rows and test.csv with 49,342 rows, both with 4,991 anonymised columns. 31,792
       test rows (64%) hold values with more than two decimals and no training row does (counted on the files);
       the winners report that 27,477 test rows, found by such values, counted on neither leaderboard[^a1]. The
       checks below use the 17,550 test rows without such values (all rows give the same result).
     - The same key built over both files finds 111,552 links between snapshots, 12 of them across the files: 4
       customers have rows in both (124 training rows, 3%; 131 test rows, under 1%). D's target check, applied to
       links from a training row to a test row, finds 221, against 114 to 153 with shuffled targets, so few sparse
       customers cross either. The two files hold different customers, apart from about 3% of the training rows.
     - The leak worked inside each file. A later test snapshot shows the target of 6,991 real test rows (40%) through
       the definition's 12 column groups, and a training row shows it for 4. Competitors, with about 100 column
       groups, read 7,800 to 8,000 test targets this way, and Tschalzev et al. moved those rows into their training
       set (12,296 rows, 4,459 + 7,837)[^a2].
     - The leaderboards: participants cite the leaderboard page as 49% public and 51% private (the page could not
       be read here). On 2018-07-17 Kaggle let the competition run on with the leak, at Santander's decision;
       submissions with the leak scored about 0.5 RMSLE on the private board, models without it 1.29 to 1.35[^a3].
   * **What it means for B:**
     - B follows the host's own split: the competition put different customers in its training and test files[^a4].
     - B also keeps the route the competitors used. A test fold holds every snapshot of its customers, and 68% to
       75% of test rows have a later snapshot in the same fold that shows their target. A model that predicts each
       test row from the training rows cannot use it; a method that compares the test rows with each other at
       prediction time can, as the competitors did with the test file.
     - The use case supports grouping: Santander asks for "the value of transactions for each potential customer",
       a customer the model has not seen in training, which is what a held-out customer stands for.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random rows (implemented) | random 3x3 folds | the BeyondArena task unchanged | 69% to 71% of test rows have a later snapshot in training |
     | B | Customers by the exact key | 1,184 customers from shifted values with 3 or more non-zero values | built without the target; the competition's split | 7% to 11% of test rows have their target in a training row's lag column |
     | D | Customers by the exact key and confirmed sparse matches | 710 customers, the largest 104 rows | 1% to 3% of test rows readable, under 1% by chance; the competition's split | the key reads the target; about 2% of its sparse links are chance and join two customers |
     | C | Retire | record `No`, folder removed | no leaky task | loses a real regression whose customers can be held out |

   * **Recommendation:** D: it is B with the sparse customers joined, it keeps the competition's split and the use
     case, and it cuts the test rows whose target a training row shows from about 9% to 2%. Ship it only if the
     leak test on the summaries (the chain feature rerun on D's splits, built from the training rows only) finds
     no gain, and retire (C) if it does[^a5]. **Decision:** D, B or C?

   **Notes for the AI:** the rebuild reproduced the check of 2026-11-04 on the raw file: 12 groups of 40 columns,
   1,436 one-step and 33,199 longer links, the later row's `features[k-2]` equal to the earlier target in 33,196
   (the issue says 33,195), 3,202 rows whose target a later snapshot shows (3,262 with any later snapshot), 1,196
   groups (957 single, largest 104). Keep `customer` out of the `drop_duplicates` subset: with it all 4,459 rows
   stay. On D, after the exact links: for k in 2..39 take every shift match whose key holds at least one non-zero
   value (shared keys allowed), keep it when the later row's `features[k-2]` equals the earlier row's raw `target`,
   drop a kept match when its earlier or its later row has another kept match at the same k, add the rest to the
   exact links and take the connected components: 4,371 extra links, 710 groups on the 4,447 rows (414 single,
   largest 104). `Grouping(labels="per_sample")` keeps 3 repeats. Folds above are `GroupKFold(shuffle=True)` with
   seeds 4267 to 4269 on components numbered by first raw row; other labels give other folds of the same spread.
   The readable-row counts take the mode of the matched rows' `features[k-2]` values per test row. Competition:
   train and test linked on the 17,550 test rows without long decimals (the result is the same with all rows); the
   27,477 figure comes from a comment on the winners' write-up and Giba's reply there (his rule: more values with
   more than two decimals than with exactly two; not reproduced), the 49/51 split from a participant in the thread
   on leaks in the public board. Threads read with `kaggle competitions topics show <id>`, which returns the
   comments but not the opening post. The leak test should build the chain feature from training rows only and
   report, apart, what it gains when it may also read the test fold's rows.

   [^a1]: Test size confirmed by Kaggle in
     https://www.kaggle.com/competitions/santander-value-prediction-challenge/discussion/59789; the filler rows:
     https://www.kaggle.com/competitions/santander-value-prediction-challenge/discussion/61288 (31,792 rows) and the
     winners' write-up, https://www.kaggle.com/competitions/santander-value-prediction-challenge/discussion/63907
     (27,477 rows; setting them to zero changed neither leaderboard).
   [^a2]: Giba's "Data Property" (rows and columns are time series),
     https://www.kaggle.com/competitions/santander-value-prediction-challenge/discussion/61329; counts of leaky rows,
     https://www.kaggle.com/competitions/santander-value-prediction-challenge/discussion/61472; Tschalzev et al.
     2024, https://arxiv.org/abs/2407.02112, Table 1 (12,296 / 49,342 rows) and Appendix A.2 ("We moved these samples
     from the test to the training dataset").
   [^a3]: 51% private: https://www.kaggle.com/competitions/santander-value-prediction-challenge/discussion/61515;
     Kaggle's response, https://www.kaggle.com/competitions/santander-value-prediction-challenge/discussion/61314;
     scores without the leak, https://www.kaggle.com/competitions/santander-value-prediction-challenge/discussion/63757.
     The competition's aim: https://www.kaggle.com/competitions/santander-value-prediction-challenge/overview.
   [^a4]: **SPLIT-19** (Should): when the source defines the split (a competition's or a paper's official periods),
     follow it; a prescribed split is still a claim to check.
   [^a5]: **SPLIT-24** (Must): group on a true group id or on one constructed exactly from the data, never on a
     similarity threshold; D's links are exact equalities of shifted values and of the target. **SPLIT-8** (Must): a
     forced split ships only when a leak test across the split finds none.

   **Andrej (2026-11-05, change):** I go with your recommendation. Make sure that you document this correctly with the
   information you provided to me, e.g. that the competition split was similar and the keys how they are reconstructed

   **Andrej (2026-11-11, discuss):** Reply (D): Customers by the exact key and confirmed sparse matches

   **Resolved (2026-11-06, Andrej):** D, customers by the exact key and the confirmed sparse matches. `dataset.py`
   builds the key in `_customer_key` from the raw lag columns before the summaries: exact links need 3 or more
   non-zero shifted values that no other row shares (34,635 links, no target used); sparse links count when the later
   row's lag column holds the earlier row's exact target and neither row has another such match at that shift (4,371
   links, 85 to 110 with shuffled targets). The key is kept as `customer`, left out of the copy check, and declared as
   `Grouping(on="customer", labels="per_sample", prediction_unit="row", context="none")` with the tag
   `ForcedGroupedFromTemporal`; the target decides only which rows belong together and is never a feature. 710
   customers (414 with one row, the largest 104 rows); 3 x 3 folds with 236 or 237 customers and 1,213 to 1,920 test
   rows each. The curation notes, the task summary, the grouping definition and the splits comment say how the key
   is built, give these numbers and the readable test rows (1% to 3% against 7% to 11% with the exact links alone and
   72% to 75% under the random split), and state that Kaggle's own training and test files hold different customers
   (4 customers in both) with the leak running inside the test file, with the sources. Leak test on the summaries: a
   chain feature built from training rows only finds the exact target of no test row on the 9 grouped folds (28 to
   44 per random fold) and gives untuned LightGBM no gain there (mean 0.1%, against 0.5% to 2.2% on 9 of 9 random
   folds); LightGBM's RMSLE is 1.504 grouped and 1.387 random. `dataset check`: 0 errors, 0 warnings. Record:
   `required_split` Grouped (NON-IID), tag `Non-IID (Grouped)` in place of `New IID`, `Andrej` in `checked_by`, a CC
   entry. Not rebuilt.

2. **Time basis: keep `ForcedGroupedFromTemporal` and write what dated snapshots would change?**

   * **Problem:**
     - Each row is a customer's snapshot at its own step, the target is the value two steps after the newest lag column, and the release has no calendar date, so the steps of different customers cannot be put on one time line; only each customer's own snapshots can be ordered, through the shifted columns.
     - The split by customer and the tag `ForcedGroupedFromTemporal` were decided on 2026-11-06 (issue 1), and the rule's questions lead to the same tag: the target comes after the features, transaction values can move with the period, the time is lost, and the customers recur.
     - The definition says that "the grouped split stands in for a temporal one" but not what a dated release would change: add a `Time basis:` bullet that says it?
   * **Background:**
     - The rule asks a forced definition to say what the timestamp would change and that it should be recovered if a later release has it[^2a]; the definition has the tag and the grouping text, but no line on the time.
     - What dated snapshots would change: windows by calendar step would test later steps, as Santander meets them; and the snapshots of different customers in one month may share a shock (a market-wide change), which a split by customer leaves on both sides and which cannot be tested without dates.
     - The prototypes do not fit: the target lies after the features, so not `Timeless` or a `Snapshot`; the snapshots have no shared prediction moment, so not a `DelayedTarget`; transaction values move with the period, so not a `StationaryRelation`.
   * **Experiments:** the time probe of 2026-11-06 finds no order of the target along the raw rows (p = 0.085) and no column that encodes a period (the positions of the first and last non-zero value, p = 1.0), so no calendar time can be recovered.
   * **Effect on the task:** none on the data or the scores; the line tells a reader what the grouped split cannot test.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | The tag as is (implemented) | `ForcedGroupedFromTemporal` and the grouping text | already decided and documented | does not say what a dated release would change |
     | B | The tag with a `Time basis:` bullet | the same split and tag, one curation bullet on the time | states the untested part (later steps, shocks shared within a month) in the one place a reader looks | one more bullet in a long note |

   * **Recommendation:** B: the split stays as decided, and the bullet completes what the forced tag asks the definition to say. **Decision:** A or B?

   **Notes for the AI:** on B, a curation bullet `- Time basis: ForcedGroupedFromTemporal: snapshots of customers at
   different steps, the target two steps after the newest lag column, no calendar date: the steps of different
   customers cannot be aligned, only a customer's own snapshots are ordered, through the shifted columns. A dated
   release would allow windows by calendar step, testing later steps and the shocks that the customers of one month
   share, which the split by customer leaves on both sides; it should be used if Santander releases the dates.` No tag
   or `splits_comment` change; `dataset check`.

   [^2a]: **SPLIT-8** (Must): a task temporal in nature or by its use case whose release cannot give the windows ships
     in the closest regime, tagged as forced from temporal; say what the timestamp or a dated window would change and
     that it should be recovered if a later release has it. **SPLIT-32** (Should): when time affects the target and is
     lost, the split is forced, `ForcedGroupedFromTemporal` when the entities recur, and the definition says what a
     dated release would change.

   **Andrej (2026-11-11, change):** Option B: The tag with a Time basis: bullet.

   **Resolved (2026-11-10, Andrej):** B: the drafted `Time basis: ForcedGroupedFromTemporal:` bullet is in
   `curation_comments`; tag, grouping and `splits_comment` unchanged.

3. **Correct the record's collection facts?**

   * **Problem:**
     - The record carries `Time: Dated`, but the only time the release keeps is the order of each customer's own snapshots, found through the shifted columns; no calendar date, period or step length ships.
     - The rule counts an order found only within each entity as no time.
     - Set `Time: Lost` in place of `Time: Dated`?
   * **Background:** `Samples: Over Time` (snapshots at different steps) and `Target: Later` (the value two steps after the newest lag, a fixed window) fit[^3a]. The arrival study of 2026-11-04 read the shifted columns as recoverable time; they order the snapshots within a customer only.
   * **Effect on the task:** none; the facts describe the source.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep `Time: Dated` (implemented) | the record unchanged | none found | reads as if a split by date were possible; departs from the rule's wording |
     | B | `Time: Lost` | the tag replaced | follows the rule; matches the forced tag | none found |

   * **Recommendation:** B. **Decision:** A or B?

   **Notes for the AI:** on B, in the record's `tags` replace `'Time: Dated'` by `'Time: Lost'`; `Andrej` is already in
   `checked_by`.

   [^3a]: **SPLIT-32** (Should): `Time: Dated` when the release or its source keeps the time or lets us recover it,
     else `Time: Lost`; a time order found only within each entity (a policy's terms) does not count. `Target: Later`
     when the target comes after the features, at one shared date or after a fixed window.

   **Answer (AI, 2026-11-09):** Andrej added the fact `Time: Within Entity` (electric_motor_temperature_prediction,
   issue 3, b): an order that runs only inside each entity.

   * The shifted columns order each customer's own snapshots, and nothing orders customers against each other.
   * So the facts are `Time: Lost` across customers and `Time: Within Entity` inside each one.
   * **Recommendation:** B, plus `Time: Within Entity`. **Decision:** B with the new fact, or B alone?

   **Andrej (2026-11-10, discuss):** Agree.

   **Andrej (2026-11-11, discuss):** Agree.

   **Resolved (2026-11-10, Andrej):** B plus `Time: Within Entity`: the record's `tags` have `Time: Lost` in place of
   `Time: Dated` and gain `Time: Within Entity`, in the working copy and in the PR #50 worktree's copy of the record.

   **Answer (AI, 2026-11-11):** the three decisions are now in the definition and the record of the branch that
   carries the newer framework (`Source(...)`), which still had the random split: the customer key and the grouped
   split (issue 1, D), the `Time basis: ForcedGroupedFromTemporal:` bullet (issue 2, B) and the record's facts
   `Time: Lost` and `Time: Within Entity` (issue 3). `dataset check` on that branch: 0 errors, 0 warnings, 710
   customers over 4,447 rows. Not rebuilt.

## Reference

https://www.kaggle.com/competitions/santander-value-prediction-challenge
