---
unique_name: tour_travels_churn
name: Tour & Travels Customer Churn Prediction
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
- WIP (Triage)
claimed_by: Andrej
suggestion: No (Retired)
decision_markers:
- Missing source information
- AHDS (Artifical/Handmade/Deterministic/Simulated)
tags:
- Tiny Data
collections:
- New (BeyondArena)
- TabSTAR
original_source: Kaggle
year: '2021'
domain: business & marketing
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/tejashvi14/tour-travels-customer-churn-prediction/data
notebook_path: datasets/beyond_iid/new_iid/tour_travels_churn/tour_travels_churn.ipynb
source_row: 778
type_adapter_id: curation-record-v1
---

## Comments

We can add it for now. We are missing some information, but it seems reasonable. It might be trivial after we test it for the first time.

CC (2026-10-21, Lennart): option (a) of the consistency check on one-snapshot churn sets: tagged `ForcedIIDFromTemporal`; SPLIT-8 now covers a release with one stock month or one undated snapshot.

**Assessment (AI, 2026-10-21):** tag and one note line added; a dated window would test the model on a later season's customers; not measurable on one undated snapshot.

CC (2026-10-21, Lennart): an upload whose first platform cannot be traced is kept for now, case by case, when the data looks sound and there is a source to point to ("if the data looks good enough even without a good source but there is a source, we want to keep it for now and risk it"); PROV-1/PROV-2 amended, the gap written as an approximate fit with a note.

**Assessment (AI, 2026-10-21):** note added to `dataset.py` curation_comments; the generated-data probe raises no flag (no rule leaves, 71% of 21 column pairs dependent, no uniform column).

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — bare Kaggle upload with no competition, paper or stated metric.

**Assessment (AI, 2026-10-27):** The open questions for the curator are in the record's Review (review of the Tiny Data datasets, written from the earlier findings, no review panel); the AI recommends shipping it after changes. Priority 1: gap -, use case - (a generic churn use), source - (a bare Kaggle upload), shape -, risk - (marks of generated data, 53% duplicate rows).
**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): 1 ordinal scales typed as ordered categories in the codebook's order (CLEAN-14, amended): `AnnualIncomeClass` (the README lists their levels).

CC (2026-11-01, Lennart): the target rule (CLEAN-25) and the cut-end rule (CLEAN-14): the target ships as No/Yes, Yes the event (1 is the event).

**Assessment (AI, 2026-11-04):** reviewed for the BeyondArena v0.2 review page, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the record's Review. Retire as generated data (AHDS): the hand-found marks (empty income x frequent-flyer cells, no age 32) and a label-linked one (repeated profiles share one label, z 7.3) all fall far outside a real customer table of the same size, and the Kaggle source is a hackathon/exam file. Priority 1: gap 0, use case 0, source 0, shape 0, risk -1.

CC (2026-11-05, Andrej): retired as generated data (`No (Retired)`, `AHDS`, `Missing source information`; confirmed on the review page 2026-11-06). The table is a Kaggle upload of 954 "customers" whose page calls it "Private Hackathon/Examination Data" and names no company, period or churn window.
- **How it was generated:** a short program over the row number k (0 to 953, the order of the Kaggle file): every column but age is a rule of the kind "every n-th row" (frequent flyer "Yes" when k mod 4 = 1, "No Record" when k mod 11 = 1, else "No"; income, services, social media and hotel the same with periods 3 to 15), age is the only random draw (27 to 38, never 32), and churn is a rule too (k mod 12 = 9, or k mod 6 = 1 with a synced account, or any odd row at ages 27-28, plus two rules for ages 33 and over). These 22 rules give every one of the 5,724 cells besides age, all 954 labels included, without an exception.
- **The generator's optimal model vs the methods:** knowing the program, a customer's churn probability is the share of churning rows among the row numbers the program maps to that customer's features and age; on the 30 shipped splits it scores 1 - ROC AUC 0.0210 and beats all 40 benchmark methods on every split (best 0.0317, TabPFN-3.5 0.0360, median 0.0406), so the task ranks methods by how close they get to a row-number formula.
- **Other marks agree:** the six empty cells, the missing age 32, the 53% repeated rows and the repeated profiles that share one label (z 7.3, none of them in a real customer table of the same size) all follow from the rules, and 200 samples with the ages redrawn reproduce them (the same six empty cells, 54% repeats, z 7.7).
- **Why the keep of 2026-10-21 no longer holds:** it rested on the data looking sound because the automated generated-data probe raised no flag; that probe never looks at the file's row order, where every column but age is a formula of the row number.

CC (2026-11-06, Andrej): the 507 repeated rows (53.1%; 419 distinct profiles, 28 with both labels) stay with a note in the definition (issue 2, B); they follow from the generator's row-number rules over six coarse columns.
To do: the v2 folder leaves the working copy once its Review is committed.

## Review

**Outcome:** added; recommended `No` (`AHDS`, `Missing source information`). A bare Kaggle upload (2021) of 954
"customers" of an unnamed tour and travel company with six coarse features and a churn flag of no stated time frame;
its source field reads "Private Hackathon/Examination Data". The table was written by a short program: in the order of
the Kaggle file every column but age is a formula of the row number (frequent flyer "Yes" on every fourth row, and so
on), churn included, and age is the only random draw; the program, used as a classifier, beats all 40 benchmark
methods on each of the 30 shipped splits (1 - ROC AUC 0.021 against 0.032 for the best). The AI recommends retiring it
as generated data (issue 1). Reviewed without a panel, from the gathered evidence: the record, the earlier experiments
of October, the model runs on the shipped data, two checks on 2026-11-04 that calibrate the marks against a real
customer table of the same size, and the row-order check of 2026-11-05 that found the program. Validity: kept on
2026-10-21 under the rule for untraced uploads because the automated generated-data probe raised nothing, but that
rule asks that the data look real, and the probe does not look at the row order. The marks found by hand (two empty
income and frequent-flyer cells where about 100 customers each are expected, no customer aged 32) and the one tied to
the label (repeated profiles share one label far more often than independent customers would) all follow from the
program, and samples redrawn from it reproduce them. The split is forced from temporal (CC 2026-10-21). Value: methods
spread (benchmark best 0.968, median 0.959, logistic regression 0.834 ROC AUC), but they spread on how close they get
to the program's formula. Quality: 53% of the rows repeat another row, with no decision recorded (issue 2, only if it
stays). Weighed: the generator written down, reproducing every cell and beating every method -, calibrated marks of
generation -, no traceable source -; a spread of methods +. Left for Andrej: issue 1 (he disputes Lennart's keep; his
note of 2026-11-05 is answered there), then issue 2 if it stays.

**Main points:** Retired as generated data (2026-11-06, issue 1); the repeated rows kept with a note (issue 2).

**Record judgment:** an untraced churn table whose marks of generated or exam data are now calibrated: a real customer
table of similar size shows none of the three. The use case is generic (a company targets retention offers) and the
churn has no time frame. `Missing source information` stands; `AHDS` follows if issue 1 goes to retirement.

**Issues for Andrej:**

1. **Retire as likely generated data, or keep under the untraced-upload rule?**

   * **Problem:**
     - In the order of the Kaggle file every column but age, churn included, is a formula of the row number (frequent
       flyer "Yes" on every fourth row, high income where the row number is 5 or 9 modulo 12, and so on), so a short
       program wrote the table, and that program used as a classifier beats all 40 benchmark methods on each of the 30
       shipped splits (1 - ROC AUC 0.021 against 0.032 for the best).
     - The Kaggle page gives no company, place, period or churn window and calls the data "Private
       Hackathon/Examination Data", the curators kept it on 2026-10-21 only because the data looked real, and the marks
       found by hand (empty cells, a missing age, repeated profiles that share one label), absent from a real customer
       table of the same size (South German Credit, 1,000 loans), all follow from the program.
     - Retire it as generated data, or keep it under the rule for untraced uploads?
   * **Background:**
     - The marks: ages run only from 27 to 38 and no customer is 32 (103 are 31, 236 are 30, 29 are 33); high income
       occurs only with frequent flyer "Yes"; frequent flyer "Yes" never occurs with middle income.
     - The automated generated-data probe of 2026-10-21 raised no flag (no rule leaves, 71% of the 21 column pairs
       dependent, no uniform column), which is why Lennart's keep reads the data as sound. That probe looks for other
       marks (uniform columns, independent columns, label rules); it does not test empty cells, gaps or repeats.
     - The file of 2026-10-27 recommended calibrating the marks first; the checks below do that on a real table we
       have locally, since a churn file (bank_customer_churn, mobile_churn) would need a download.
   * **Effect on the task:** if the table is generated, the benchmark scores how well a model recovers the
     generator's rules, not customer churn.
   * **Experiments:** checks of 2026-11-04 on the raw Kaggle file, the same statistic on South German Credit:
     - Empty cells of two-column tables (columns of at most 6 values) where independence expects 20 or more
       customers: 6 in this file (high income without frequent flyer: 101 expected, middle income with frequent
       flyer: 123, high income with 2 or 3 services: 29 and 21, 6 services with a synced account: 24, 6 services
       without a hotel booking: 39); 0 of 120 pairs in South German Credit, none even at 10 expected.
     - Gaps inside the age range: age 32 is empty while its neighbours average 66 customers, a chance of 2e-29 for a
       smooth count; South German Credit's gaps lie only among the oldest ages, with 0 to 2 loans next to them.
     - Label agreement of repeated profiles (a mark tied to the label): of the 203 profiles held by two or more
       customers, 175 carry one label, against 135 expected if each customer churned independently at the rate a
       main-effects logistic regression gives (z = 7.3); on 40 random sets of six coarse columns of South German
       Credit the same z has median 0.4 and maximum 2.5.
     - Model runs on the shipped data describe churn as a near lookup of the full profile: full profiles
       are 98% pure outside one segment, and some cells are pure (no churn among 291 non-flyers with 1 or 3
       services, churn for all 28 customers aged 27 or 28 with 2 services). Their simple models of that lookup rank
       12th to 32nd of 41: they did not find the formula behind it (the answer of 2026-11-05 below does).
     - October 2026, 30 splits: TabPFN beats logistic regression on 30 of 30 (by 0.06 ROC AUC on average) and reaches
       0.95 on profiles it never saw in training.
   * **Consistency:** credit_card_customers was kept under the same amended rule on 2026-10-21 and retired as
     `AHDS` on 2026-10-26 on calibrated marks without a label link, among them a structural zero (no woman earns
     above $60K); customer_satisfaction_in_airline was retired on direct proof of rework. mobile_churn and
     bank_customer_churn stay under the same rule with no mark found.
   * **Unknown:** whether a churn file shows such marks; a download of bank_customer_churn or mobile_churn would
     settle it.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep under the untraced-upload rule (implemented) | as defined; `fit_reason` says the curator "would not be surprised if it were artificial" | the decision of 2026-10-21 stands | the rule asks that the data look real, and the calibrated marks say it does not |
     | B | Retire as generated | `No (Retired)` with `AHDS` added to `Missing source information`, a CC line, the folder removed | follows credit_card_customers; no generator's rules scored as churn | a task with a spread of methods leaves; the reference table is credit data, not churn |
     | C | Keep, marks in `fit_reason` | as A, with the three marks and their calibration written into `fit_reason` | the risk is taken knowingly and documented | scores a likely generator as churn |
     | D | Calibrate on a churn file first | run the same three statistics on bank_customer_churn or mobile_churn (a download), then decide | a reference of the same kind | one more round for marks that a real customer table already does not show |

   * **Recommendation:** B: calibrated marks from two kinds of test, one of them tied to the label, are the evidence
     the rule asks for, and the source gives nothing to set against them[^1a][^1b][^1c][^1d]. **Decision:** A, B, C
     or D?

   **Notes for the AI:** on B, record `suggestion: No (Retired)`, `decision_markers` add `AHDS`, CC line (Andrej,
   with the three calibrated numbers) and `checked_by` Andrej; remove the folder, CHANGELOG entry, and a Cases row
   under PROV-3 in `provenance.md`.

   [^1a]: **PROV-3** (Must): the data is real, not generated; without a source statement, calibrated marks from at
     least two tests, or marks linked to the label, can be strong enough.
   [^1b]: **PROV-2** (Should, amended 2026-10-21): an untraced upload is kept for now, case by case, when the data
     looks sound (it passes the generated-data tests) and there is a source to point to.
   [^1c]: **SEL-16** (Must): data that does not come from a real random distribution (artificial, synthetic,
     handmade) is out.
   [^1d]: **EV-9** (Should): calibrate a statistic before concluding from it, on a real dataset of the same kind.

   **Andrej (2026-11-05, discuss):** I want to retire this dataset, but please articulate clearly why we know now this
   is generated and what the optimal model knowing the generation process would have been.

   First, add the explanation you would use to the curation record

   **Answer (AI, 2026-11-05):**

   - You asked how we know the table is generated, what the best model for someone who knows the generation process
     would be, and for the explanation in the record first.
   - The generator, found by sorting the Kaggle file in its own row order (the shipped table is shuffled) and
     cross-tabulating each column against the row number k (0 to 953) modulo small numbers[^a2]: every column but age
     is a fixed rule of k, checked in order, of the kind "every n-th row":
     - frequent flyer "Yes" when k mod 4 = 1, else "No Record" when k mod 11 = 1, else "No";
     - income Low when k mod 3 = 1, else High when k mod 4 = 1, else Low when k mod 7 = 1, else Middle;
     - services 6 when k mod 15 = 0, else 5 when k mod 13 = 1, else 4 when k mod 7 = 6, else 2 when k mod 4 = 3, else
       3 when k mod 6 = 2, else 1;
     - social media synced when k mod 5 = 2, k mod 9 = 1 or k mod 10 = 6; hotel booked when k mod 5 = 0, k mod 6 = 0
       or k mod 8 = 0.
   - Age is the only random draw: 27 to 38 with uneven weights, never 32, unrelated to k (tested against k modulo 2 to
     60, smallest p 0.017 of 59 tests). It switches a few rules: frequent flyer is also "Yes" when k mod 7 = 1 from
     age 33 on, and the hotel rule k mod 8 = 0 holds from age 28 on.
   - Churn is a rule as well: yes when k mod 12 = 9, or k mod 6 = 1 with a synced account (153 churners), or on any odd
     row at ages 27 and 28 (49 more), or k mod 13 = 1 at ages 35 to 37 (12), or k mod 42 = 8 from age 33 on (10).
   - With the file's ages these 22 rules give every one of the 5,724 cells besides age, all 954 labels included,
     without an exception; random data does not repeat exactly every 84 rows (income) or every 90 rows (social media).
   - The optimal model for someone who knows the program: a customer's churn probability is the share of churning rows
     among the row numbers that the program maps to the customer's features at the customer's age (age is drawn
     independently of k, so its weights cancel and nothing is left to fit). It is 0 for 623 of the 954 customers, 1
     for 132, and about 0.5 for most of the rest, mainly high income with one service, where churn depends on k mod 3,
     which no feature shows.
   - Scored on the 30 shipped splits (10 repeats of 3 folds) with the task's metric, it reaches 1 - ROC AUC 0.0210 (SD
     0.0051; ROC AUC 0.979) and beats all 40 benchmark methods on every one of the 30 splits: best method 0.0317,
     TabPFN-3.5 0.0360, median method 0.0406, logistic regression 0.166. Its rules were read off the whole file, so it
     is the ceiling for a model that knows the generator, not a model trained on the training rows; the methods are
     ranked by how close they get to its probability table.
   - The other marks follow from the rules: high income falls only on rows with k mod 4 = 1, where frequent flyer is
     "Yes"; 6 services fall on every 15th row, where the hotel is always booked and the account never synced; age 32
     is not among the ages drawn. 200 samples with the ages redrawn reproduce them: the same six empty cells in every
     sample, no age 32, 54% repeated rows (file 53%), 412 profiles (file 419), repeated profiles sharing one label at
     z 7.7 (file 7.3).
   - Why it was missed: the automated probe, the earlier experiments and the checks of 2026-11-04 treat the rows as a
     set; only the row order shows the rules.
   - The record now carries this explanation as a CC line of 2026-11-05 (How it was generated, the generator's optimal
     model against the methods, the other marks, why the keep of 2026-10-21 no longer holds), with `Andrej` in
     `checked_by`; `suggestion`, the markers and the folder are unchanged until you confirm.
   - Recommendation: B, retire as generated data; the program is written down, reproduces every cell and beats every
     method on every split, which settles the question[^a1][^a3]. **Decision:** confirm B (retire), or keep it (A or C)?

   **Notes for the AI:** on B, apply the notes above (record `suggestion: No (Retired)`, `AHDS (Artifical/Handmade/
   Deterministic/Simulated)` added, CHANGELOG entry, folder removed once this file is committed); the CC line of
   2026-11-05 already explains the generator, so the retirement line only records the decision. The PROV-3 Cases row
   in `provenance.md` names test 2 (row-counter patterns) and the written-down program, next to ecommerce_shipping;
   the program could also join bank_customer_churn as an example under "When you can, write the generator down".
   Never cite the evidence's local folder in a repo file.

   [^a1]: **PROV-3** (Must): the data is real, not generated; its detection says "When you can, write the generator
     down: that settles it, and it leads the report".
   [^a2]: Test 2 of "Is the data generated?" (row-counter patterns): sort by the id or the file order and
     cross-tabulate each categorical column against the id modulo k. Case: ecommerce_shipping, `Warehouse_block` the
     id modulo 6 and `Mode_of_Shipment` a 137-id cycle, retired.
   [^a3]: **SEL-16** (Must): data that does not come from a real random distribution (artificial, synthetic,
     handmade) is out.

   **Andrej (2026-11-05, change):** Agree. Good, document this well and retire.

   **Resolved (2026-11-06, Andrej):** retired as generated data (B): the record is `No (Retired)` with `AHDS` beside
   `Missing source information`; its CC line of 2026-11-05 gives the generator (every column but age a rule of the
   row number, reproducing all 5,724 non-age cells) and its optimal model (1 - ROC AUC 0.0210, ahead of all 40
   benchmark methods on 30 of 30 splits). A Cases row under PROV-3 in provenance.md. The folder stays until this
   file is committed.

2. **Keep the 53% duplicate rows, or drop them? Only if the dataset stays.**

   * **Problem:**
     - 954 customers show 419 distinct feature profiles: 53% of the rows repeat another row exactly, and 28 profiles
       occur with both labels.
     - The definition keeps every row and records no decision about them.
     - Keep them with a note, or drop the copies?
   * **Background:** the six features are coarse (11 ages, 3 frequent-flyer values, 3 income classes, 6 service
     counts, two yes/no answers: 2,376 possible profiles), so real customers would share profiles often. The copies'
     positions in the file look like a random shuffle, so they are not appended blocks. The repeated profiles agree
     on the label more often than independent customers would (issue 1), which fits copied rows and a label that is a
     lookup of the profile alike.
   * **Effect on the task:** on random splits 70% of the test rows have their profile in the training rows. If the
     copies are real customers, that is what a new customer looks like; if they are resampled rows, the score
     includes recall of the same row.
   * **Experiments:** October 2026, 30 splits: dropping exact copies lowers TabPFN from ROC AUC 0.962 to 0.912 and
     the random forest from 0.946 to 0.857, so the choice changes the task and the ranking, though no rule reads the
     size of a drop as the reason.
   * **Consistency:** sepsis_survival_minimal_clinical_records keeps 110,204 rows over 975 distinct profiles (three
     features, real patients); audiology_diagnosis dropped 27 copies of the same findings and diagnosis.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep all rows, no note (implemented) | 954 rows | as published | the decision the duplicates need is not recorded |
     | B | Keep them with a note | 954 rows; `curation_comments` say why (few coarse features, plausible repeats) | how often a profile occurs stays part of the task | if the rows were resampled, the score includes recall of the same row |
     | C | Drop the copies | exact copies with the same label dropped, and every copy of a profile seen with both labels; about 419 rows | no recall of a copied row | the task no longer reflects how often a profile occurs; assumes the rework that would retire the dataset (issue 1) |

   * **Recommendation:** B: if the dataset stays, it stays as real customers, and then repeats over six coarse
     features are natural; dropping them assumes the rework that issue 1 would retire it for[^2a][^2b][^2c].
     **Decision:** A, B or C?

   **Notes for the AI:** on B, a `curation_comments` bullet: 507 exact duplicate rows (53.1%), 419 distinct
   profiles, 28 with both labels, kept as natural repeats of six coarse features; accept the bundle-check warnings
   with that reason. On C, `drop_duplicates()` and drop every profile seen with both labels, then re-run the checks.

   [^2a]: **LEAK-16** (Must): duplicate rows need a decision every time.
   [^2b]: **LEAK-18** (Should): few features and plausible repeats are natural, kept with a note; many degrees of
     freedom and an exact match are a collection artefact, dropped.
   [^2c]: **LEAK-19** and **LEAK-20** (Should): exact copies with the same label are dropped, and feature vectors that
     occur with both labels lose every copy unless the ambiguity is genuine.

   **Andrej (2026-11-05, change):** Add the note as suggested

   **Resolved (2026-11-06, Andrej):** kept with a note (B): a `curation_comments` bullet gives the 507 repeated
   rows, the 419 profiles and the 28 with both labels, and says they follow from the generator; the dataset is
   retired (issue 1).

## Reference

Kaggle
