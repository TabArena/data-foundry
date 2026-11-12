---
unique_name: santander_customer_transaction_prediction
name: Santander Customer Transaction Prediction
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: No (Retired)
decision_markers:
- Anonymized
- AHDS (Artifical/Handmade/Deterministic/Simulated)
tags:
- Larger IID Data
collections:
- TabArena Reject
original_source: Kaggle
year: '2019'
domain: finance
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/competitions/santander-customer-transaction-prediction
notebook_path: datasets/beyond_iid/new_iid/santander_customer_transaction_prediction/santander_customer_transaction_prediction.ipynb
source_row: 650
type_adapter_id: curation-record-v1
---

## Comments

CC (2026-09-30, Lennart): **Leak fixed: dropped the 400 `var_i_has_one`/`has_zero` features.** They follow the Kaggle #1 solution: for each var, does this row's value occur in another class-1 / class-0 row. The encoding is leave-one-out (a row never sees its own label), but it was computed over all 200k labelled rows before splitting, so every row's features encode the labels of the other rows in its test fold, which a deployment would not have. LightGBM ROC AUC (leak audit 2026-09-24, rechecked on other folds): 0.903 shipped, 0.899 with has_* recomputed from train-fold labels, 0.900 with label-free value counts, 0.896 raw 200 vars. We now ship `target` + `var_0..var_199` (200 features). The technique itself is worth applying inside a pipeline, computed per fold (or on unlabelled rows where a method may see them); this is noted in curation_comments.

CC: "Interesting dataset, but not on OpenML. License allows to use the data for research, but not distribute it - so we have an API issue."

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source roc_auc — Area Under Receiver Operating Characteristic Curve (https://www.kaggle.com/competitions/santander-customer-transaction-prediction (Kaggle API evaluationMetric)).

CC (2026-11-01, Lennart): the target rule (CLEAN-25) and the cut-end rule (CLEAN-14): the target ships as No/Yes, Yes the event (1 is the event).

**Assessment (AI, 2026-11-04):** reviewed for the BeyondArena v0.2 review page, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the record's Review. Retire as generated: within each class the 200 columns are independent at exactly the chance rate (5.1% and 0.1% of pairs outside the 95% and 99.9% bands) and real rows cannot be told from within-class shuffles (AUC 0.49); the shipped-data leak is already fixed in v0.2. Priority 1: gap 0, use case 0, source 0, shape 1, risk -1.

CC (2026-11-05, Andrej): retired as generated data (`No (Retired)`, `AHDS`). The data: the training file of Santander's Customer Transaction Prediction competition (Kaggle, 2019), 200,000 rows of 200 anonymised numbers and whether the customer made an unnamed transaction (10%).
- **Each row is 200 values drawn one column at a time given the label:** within each class the 200 columns are as independent as random draws (5.1% of the 19,900 column pairs outside the 95% noise band and 0.1% outside the 99.9% band, the rates chance gives), and a model cannot tell real rows from rows whose values were shuffled within the class (ROC AUC 0.49). Santander's real customer table (santander_customer_satisfaction) fails both tests by far (53% of pairs, ROC AUC 1.0).
- **So the best model is known in advance:** for rows drawn that way, naive Bayes, a sum of 200 one-column terms, is the right model by construction; it reaches ROC AUC 0.899, level with TabPFN-3.5 (0.897 to 0.902). The task ranks methods by how well they add up independent columns, a property of the generator, not of customers.
- **The release points the same way:** the host published nothing about the columns or the transaction, the earlier curation notes call the features generated or transformed for the competition, and competitors had to filter synthetic rows out of the test file.
- **Why the keep does not hold:** the leak fixed on 2026-09-30 is gone and masked columns alone are no reason to retire, but here the rows themselves are not records of customers.
Not changed: `Anonymized` stays.

**Assessment (AI, 2026-11-12):** re-check of the retirement on BeyondArena's 9 splits, at Lennart's dispute (Review, issue 1).
- BeyondArena still ships the 601-column container with the leaky `has_one`/`has_zero`, and its scores here are on that version: best the tuned GBM (0.9093), then RealMLP and TabM (0.898) and TabPFN-3.5 (0.894, split 0 only).
- With the 200 raw columns: Gaussian naive Bayes 0.888, naive Bayes on smoothed densities 0.894, 200 one-column LightGBMs summed 0.896, tuned LightGBM on all columns 0.894, with or without value counts.
- The Kaggle solution, one model per column over the value and its count with the logits summed: 0.9045 with counts from the training rows, 0.9101 with counts over the training and test rows (no labels), above the leaky tuned GBM on all 9 splits.
- The count signal is per column too: within each class, whether a value is unique in its column is independent across columns (4.97% and 4.89% of pairs outside the 95% band). The best known model is still a sum of 200 one-column terms.

CC (2026-11-12, Lennart): the retirement stands. I disputed it, since the data looks like an anonymized version of real data and the Kaggle count features are feature engineering a method may do itself. But the better model is still a sum of one-column terms and the rows are no customer records, so the task tests a pattern (adding up weak independent signals). It would fit a benchmark of such patterns, not TabArena.

## Review

**Outcome:** added; recommended `No` (AHDS). The training file of Santander's Customer Transaction Prediction
competition (Kaggle, 2019): 200,000 customers, 200 anonymised numbers, 10.05% made the unnamed transaction, random
split, ROC AUC as in the competition. The AI recommends retiring it: the rows are not records of customers (issue 1).
Reviewed on 2026-11-04 without a panel, from the gathered evidence (the record, the leak audit of 2026-09-24, a
model run on the shipped data) and two checks. Validity: the leak found earlier (every test label read off the
400 value-presence columns of the shipped version) does not hold in v0.2, which dropped those columns on 2026-09-30.
But within each class the 200 columns are as independent as random draws (5.1% of the 19,900 pairs outside the 95%
noise band, 0.1% outside the 99.9% band, the chance rates), and rows with all 200 columns shuffled within class cannot
be told from real rows (ROC AUC 0.49); Santander's real customer table (santander_customer_satisfaction) gives 53% and
1.0. Each row is a set of per-column draws given the class, so the task is a naive Bayes sum by construction. Value:
naive Bayes over the 200 columns alone reaches ROC AUC 0.899, as much as TabPFN-3.5 without the leaky columns (0.897
to 0.902). Quality: nothing beyond the generation. Weighed: Santander's own competition +, a clean test of summing
many weak independent signals +, rows that are not real records -, a known formula -.

**Main points:** Retired as generated data (2026-11-05, issue 1).

**Record judgment:** not valid as real data: the values may come from real customers, but their combination in a row
does not; the definition's own notes call the features generated or transformed.

**Issues for Andrej:**

1. **Retire as generated data: the columns are independent within each class?**

   * **Problem:**
     - Within each class the 200 columns are as independent of each other as random draws, and a model cannot tell the real rows from rows whose 200 values were shuffled within the class (ROC AUC 0.49), while Santander's real customer table fails both tests by far.
     - A row is then not a customer but 200 values drawn one column at a time given the label, so the best model is a naive Bayes sum of 200 one-column terms by construction.
     - Retire the dataset as generated, or keep it as a test of summing many weak signals?
   * **Background:** the host published no description of the columns or the transaction; the curation notes already
     say the data "seems to be generated or created for the competition" and that competitors had to filter fake
     samples from the test file. Values a data owner perturbed for privacy are kept only when no test measures
     damage[^d3-1a]; here the joint structure of the rows is gone. The automated probe did not flag it, because an
     overall share of dependent pairs alone is common in real data[^d3-1b]; the tests below are taken within each class
     and calibrated on a real Santander table.
   * **Experiments:**
     - Within-class Spearman correlations (check of 2026-11-04, 200 columns, 19,900 pairs per class): class 0
       (179,902 rows) 5.13% of pairs outside the 95% noise band and 0.10% outside the 99.9% band, largest |r| 0.0096
       (band 0.0046); class 1 (20,098 rows) 5.10% and 0.09%. santander_customer_satisfaction, measured the same way:
       52.9% and 54.1% of pairs outside the 95% band.
     - Shuffle test (values permuted within each class, LightGBM telling real from shuffled rows, 3-fold CV, 100,000
       rows): all 200 columns 0.487, `var_0` alone 0.498, `var_81` alone 0.497; santander_customer_satisfaction with all
       columns shuffled 1.0.
     - Model runs on the shipped data: naive Bayes over the 200 columns ROC AUC 0.899; TabPFN-3.5 without the
       value-presence columns 0.902 and 0.897 on two held-out splits; the leak audit's LightGBM 0.896 on the raw
       columns.
   * **Effect on the task:** the benchmark scores how well a method adds up 200 independent one-column effects, a
     property of the generator, not of how customers transact.
   * **Consistency:** follows the retirement of generated tables on calibrated marks tied to the label
     (credit_card_customers, hepatitis_c_egypt)[^d3-1a]. Judged like the other two Santander sets: masked columns alone
     are no reason to retire[^d3-1c]; santander_customer_satisfaction and santander_transaction_value have real rows
     (dependent columns, households, time-shifted snapshots), this one does not.
   * **Unknown:** whether Santander shuffled real values within each class or drew them from fitted distributions;
     either way no row is a real customer.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep (implemented) | 200,000 rows, 200 columns, random split | a large, clean test of many weak independent signals | rows are not records; a known formula is the answer |
     | B | Retire | record `No (Retired)` with `AHDS`; the folder is removed | follows the rule on generated data | one large binary task fewer |

   * **Recommendation:** B: the within-class independence sits exactly at the chance rate and real rows cannot be
     told from shuffled ones, both calibrated on a real Santander table. **Decision:** retire (B), or keep (A)?

   **Notes for the AI:** on B, the record gets `suggestion: No (Retired)`, marker `AHDS (Artifical/Handmade/
   Deterministic/Simulated)` beside `Anonymized`, `v2_path` cleared, a `CC` line with the numbers above; remove the
   folder with a CHANGELOG entry; add a PROV-3 case row and update the EV-9 case text in evidence.md and the
   calibration note in task_probes.md, which cite this dataset as real data with 5.4% dependent pairs.

   [^d3-1a]: **PROV-3** (Must): the data is real, not generated and not a real table someone reworked; values the data
     owner perturbed for privacy are no rework when no test measures damage; without a source statement or a
     generator, calibrated marks from at least two tests, or marks linked to the label, can be strong enough. Cases:
     credit_card_customers, hepatitis_c_egypt (2026-10-26, Lennart). **SEL-16** (Must): data that does not come from
     a real random distribution is out.
   [^d3-1b]: **EV-9** (Should): calibrate a statistic against the same statistic on a real dataset of the same kind
     before concluding from it; case: this dataset, 5.4% of its pairs dependent overall but no uniform column.
   [^d3-1c]: Selection guideline, "Anonymized data": the marker flags what the data cannot tell us, not a defect; it is no
     reason for `No` by itself, and the verdict comes from what can be checked.

   **Andrej (2026-11-05, change):** Retire it and add a good bullet point style argumentation to the curation record.

   **Resolved (2026-11-05, Andrej):** retired as generated data (B): the record is `No (Retired)` with `AHDS` beside
   `Anonymized`, and its CC line argues it in bullets: each row is 200 values drawn one column at a time given the label
   (independence within class at the chance rate, real rows not told from shuffled ones, both calibrated on
   santander_customer_satisfaction), so naive Bayes is the right model by construction and matches TabPFN-3.5 (0.899
   against 0.897 to 0.902). A PROV-3 case row added; the EV-9 case and the calibration note in task_probes.md no
   longer cite it as real data. The folder stays until this file is committed.

   **Lennart (2026-11-12, discuss):** "it seems to be just an anonymized version of the data. How good are the best
   model on BeyondArena compared to naive bayes? The top solutions on kaggle mirror a sum-up-like solution but this is
   feature engineering which we can make part of the solution to keep the real, anaomyinized task."

   **Answer (AI, 2026-11-12):**
   - Asked: does a model beat naive Bayes on the data without the leaky columns, and is the Kaggle count feature a
     reason to keep the task?
   - BeyondArena's scores are on its 601-column container, which still has the leaky `has_one`/`has_zero` (best: tuned
     GBM 0.9093; RealMLP and TabM 0.898; TabPFN-3.5 0.894, split 0 only). On its 9 splits with the 200 raw columns:
     Gaussian naive Bayes 0.888, naive Bayes on smoothed densities 0.894, 200 one-column LightGBMs summed 0.896, tuned
     LightGBM on all columns 0.894, with or without value counts.
   - The Kaggle solution, one model per column over the value and its count with the logits summed, beats naive Bayes:
     0.9045 with counts from the training rows, 0.9101 with counts over the training and test rows (no labels), above
     the leaky tuned GBM on all 9 splits.
   - That model is still a sum of 200 one-column terms, and the count signal is per column too: within each class,
     whether a value is unique in its column is independent across columns (4.97% and 4.89% of pairs outside the 95%
     band). The rows stay independent draws per column, so two PROV-3 tests measure damage and the clause for data the
     owner perturbed for privacy does not keep it.

   **Resolved (2026-11-12, Lennart):** the retirement (B) stands: "under this perspective and framing I am fine to
   exlcude it, it would rather just be for patterns arena again". Recorded in the record's CC line of 2026-11-12.

## Reference

Mercedes Piedra, Sohier Dane, and Soraya_Jimenez. Santander Customer Transaction Prediction. https://kaggle.com/competitions/santander-customer-transaction-prediction, 2019. Kaggle.
