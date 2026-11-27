---
unique_name: african_credit_scoring_challenge
name: african-credit-scoring-challenge
checked_by:
- Andrej
- Lennart
data_foundry_status:
- 'DF: Yes'
suggestion: 'Yes'
priority: 2
tags:
- Non-IID (Temporal)
- 'Samples: Over Time'
- 'Time: Dated'
- 'Target: Revised Later'
- 'Entities: Recur'
- Dated Event Log
collections:
- New (BeyondArena)
original_source: Zindi
collection_period: 2021-2024
domain: finance
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/african-credit-scoring-challenge/data
v2_path: datasets/_dev/tabarena-v0pt2/african_credit_scoring_challenge/dataset.py
source_row: 879
type_adapter_id: curation-record-v1
---

## Comments

**AI summary:**

Predict loan default for an African credit-scoring challenge; this is a canonical real-world tabular classification task with a clear, meaningful target in finance. The record is already partially curated (checked by Andrej, DF WIP, original_data_state One Table) and tagged both Grouped and Temporal, so the appropriate non-IID split must be respected. Credit default is exactly the kind of representative tabular ML task the benchmark wants. A human should confirm the row count, the precise split protocol (grouped by borrower and/or temporal), and that there is no target leakage from post-default fields.

---

predict loan default

**Assessment (AI, 2026-10-07):** Added as a temporal task (binary `default`, ROC AUC); the record's Grouped split and tag do not fit, since repeat customers are history known at disbursement. Three leaks are removed: the repay amounts, which grow with penalties after a default (AUC 0.907 with them, 0.639 without); 8,899 rows whose lender funds under one unit, all labelled 0 by construction; and 802 rows whose label was not settled at the data pull. Nine windows: six over the end of the 2022 Type_1 lending, three 30-day windows ending 2024-10-08; each trains only on loans settled 30 days before it starts. Linear AUC 0.649, CatBoost 0.672. Open: the window scheme, and the near-chance 2024 windows.

**Assessment (AI, 2026-10-20):** priority 1 for the review of the added dataset: gap -, use case -, source -, shape +, risk - (Issues 2-3: label set at data pull; zero-share rows labelled 0 by construction; the fix selects on a post-disbursement field). A real temporal credit-default task, but the signal is weak and mostly the customer's history, the 2024 windows are near chance, and the label is fragile.

**Assessment (AI, 2026-10-20):** review panel (re-check): ship after changes; the changes are in the definition. `other_lenders_on_loan` is dropped (LEAK-10: a count of the loan's lender rows at the data pull that cannot be dated; its link to the outcome changes sign between eras); the one impossible share (1.168) is set to missing; 58,953 rows, 10 features. The label is the loan's default (the two rows of a loan agree in 2,132 of 2,134 loans), not a per-lender outcome. Counted per loan, 2024 loans 31-45 days past due default at 7.2% against 5.8-9.8% later, so the 30-day settlement holds (LEAK-24). The 0.649 linear score of 2026-10-07 is not reproduced (0.705 with one-hot customer_id). Open for Lennart (the Review): the zero-share filter (issue 2) and an exception to SPLIT-20 for the two product eras (issue 1). Priority 2: gap -, use case - (fit approximate: pull-time share columns, history known only through settled labels), source + (Zindi page and codebook), shape +, risk - (the zero-share filter selects rows on a pull-time field, an open LEAK-25 / SPLIT-9 reading).

CC (2026-10-21, Lennart): the declared metric documents the original use case's metric; overrule it only when it is biased or wrong (evidence from the paper); keep the note of the original metric (TP-6 amended).

**Assessment (AI, 2026-10-21):** metric set to `f1`, the competition's metric (was the default ROC AUC). F1 scores hard labels at a threshold; no evidence from the source that it is biased or wrong. Needs a rebuild to reach the container.

CC (2026-10-21, Lennart): ok on the follow-up item: a strong kept leak does not make the fit approximate (USE-8 amended); the kept leak is named in `fit_reason` as kept, not as a gap.

**Assessment (AI, 2026-10-21):** fit stays `approximate` for the label-only history and the unstated sampling; the funded-amount columns left `fit_reason` (their potential-leak note stays).

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source f1 — F1 Score (https://zindi.africa/competitions/african-credit-scoring-challenge (evaluation section)).

CC (2026-10-26, Lennart): issue 2: keep dropping the 8,899 rows whose lender funds less than 0.5 (LEAK-25).

**Assessment (AI, 2026-10-26):** answers to the review issues. Type_1 exists only from 2022-07-12 to 2022-12-01 (52,826 rows, 520 defaults); the six 2022 windows cut to Type_1 hold 18-22 defaults each, and the mixed windows' higher ROC AUC (0.68 against 0.60 untuned) comes from telling products apart (issue 1). Zindi's leaderboard was won with leaks and a hand-written Ghana rule, and its goal asked for default probabilities binned into risk grades; F1 per shipped window is 0.00-0.16 with about 20 defaults (issue 6, a consistency check against CC 2026-10-21). Zindi's Ghana test part cannot be reproduced: no labels, products absent from training (issue 7).

CC (2026-10-26, Lennart): issue 1: "Do that then": keep the Type_1 loans only (six 2022 windows).

CC (2026-10-26, Lennart): issue 6: "Yes do (a)": ROC AUC instead of Zindi's F1, under MET-4's overrule clause (the host asked for default probabilities binned into risk grades; the forum shows the F1 was gamed; one default moves F1 by about 0.05 on our windows). The metric mark: "See other issue to resolve this".

CC (2026-10-26, Lennart): issue 7 as implemented: the competition's Ghana test and its new applicants are not reproduced; `changes` and `fit_reason` say so.

**Assessment (AI, 2026-10-26):** applied: Type_1 only (52,826 rows, 520 defaults, 5,040 customers), lender_id, loan_type and duration dropped (constant), six windows of 1,821-2,446 rows and 18-22 default rows (2022-10-15 to 2022-12-01), horizon 7 days, `Metric.fallback` with F1 named as the rejected original. `dataset check` clean. Task probes (5 of 6 windows): random forest ROC AUC 0.594, LightGBM 0.568, linear 0.522; flags no_spread, drift_baseline, unstable. New REVIEW issue 8 asks whether to ship it.

CC (2026-10-26, Lennart): issue 8, option (a): add the history feature a data scientist would build, the customer's number of earlier loans at disbursement (CLEAN-19). "also remember to never run v2 again but v3.5 by default" (TabPFN).

**Assessment (AI, 2026-10-26):** issue 8 (a) applied: `earlier_loans`, the customer's loans in the release disbursed on an earlier day (Train.csv and Test.csv's Kenyan rows, any product, no label read); a count of earlier settled defaults is 0 in every row and is not added. ROC AUC over the six windows: the count alone 0.724; tuned LightGBM 0.698 (before 0.633); CatBoost default 0.673 (0.655), tuned 0.655 (0.651); TabPFN v3.5 0.724 (0.675 without the feature). Task probes: linear 0.704, LightGBM 0.660, random forest 0.647; the `unstable` flag is gone, `no_spread` and `drift_baseline` remain. Leak probes: nothing new. Recommendation on the page: ship.

CC (2026-10-26, Lennart): verdict ship (with earlier_loans, issue 8).

CC (2026-11-08, Lennart): text fix (cross-dataset item, go ahead): one row per loan. The `row` text no longer says that a loan funded together with a second lender gives two rows, and the notes no longer say that `New_versus_Repeat` can differ between a loan's two rows; the same claim is gone from the splits comment ("A row is one lender's part of a loan, so a two-lender loan counts twice") and from decision table 4 ("A row is one loan"). Text only; the `row` text changes the checksum (not built).

**Assessment (AI, 2026-11-08):** the kept product has one lender: the shipped frame has 52,826 rows and 52,826 loan ids, and Train.csv's Type_1 rows 61,723 rows, 61,723 loan ids and one lender_id; the loans with two rows (4,268 rows) are all of other products (Type_7, Type_4, Type_5, ...). `dataset check`: 0 errors, 0 warnings, 2 info.

CC (2026-11-19, Andrej): windows below the target count kept (Review issue 1, A as implemented): six windows of about a week, with the reason corrected: a label settles 37 days after disbursement, so only the loans from 15 October 2022 have half the rows settled before them; the reason is in the splits comment.

## Review

**Outcome:** added. Reopened on 2026-11-19 by the split check: the definition ships fewer windows than the target count for its size, and its splits comment gives a reason the window rules no longer accept. Settled on 2026-11-19 (issue 1, A): six windows of about a week kept, with the reason corrected in the splits comment.

**Main points:** Which window layout (issue 1, resolved).

**Issues for Andrej:**

1. **Windows: 6 of the target's 9; which layout?**

   * **Problem:**
     - Six windows ship where an IID split of 52,826 loans would get nine[^split15]. The splits comment's reason, "more windows would leave some with 8 default rows", is not one the rules accept: few positives are part of the task, and only a window without a positive is a problem for ROC AUC[^split16].
     - Today's windows (each trained on the loans whose label settled before it):

       | Test window | Days | Train side | Train share | Test loans | Defaults |
       |---|---|---|---|---|---|
       | 21 Nov-1 Dec 2022 | 11 | 39,722 | 75.2% | 2,427 | 21 |
       | 14-20 Nov | 7 | 37,453 | 70.9% | 1,952 | 20 |
       | 4-13 Nov | 10 | 33,785 | 64.0% | 2,446 | 21 |
       | 27 Oct-3 Nov | 8 | 31,043 | 58.8% | 2,274 | 18 |
       | 21-26 Oct | 6 | 28,746 | 54.4% | 2,184 | 20 |
       | 15-20 Oct | 6 | 26,490 | 50.1% | 1,821 | 22 |

     - Fixed: a label counts as known 30 days after the 7-day due date, so each window trains only on loans disbursed more than 37 days before it (the curation's conservative cut). The windows of about a week follow the declared horizon of 7 days, the curator's choice; the use case's refit "at least once a month" is assumed, as Zindi gives no cadence.
     - What stops more windows: half the rows are settled only before 15 October, so the half-data floor[^split14] leaves the 48 days from 15 October to 1 December for testing, which hold six windows of about a week. Calendar months, the use case's cadence, give November (62.2%) and October (40.0%) only: two windows, under the minimum of three.
   * **Window counts:** counted with the definition's own window builder (equal loans per window, cut at days).

     | Layout | Windows | Train share | Test loans | Defaults | Window length |
     |---|---|---|---|---|---|
     | A, shipped | 6 | 50.1-75.2% | 1,821-2,446 | 18-22 | 6-11 days |
     | B, nine windows, half the data or more | 9 | 50.1-76.8% | 1,186-1,705 | 8-22 | 3-8 days |
     | C, nine windows of about a week, down to 30% | 9 | 30.9-74.1% | 2,343-2,734 | 19-41 | 7-13 days |
     | D, calendar weeks back from 1 December | 6 | 54.4-77.4% | 1,244-2,627 | 9-22 | 7 days |

   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Six windows of about a week (implemented) | the reason in the splits comment corrected | the declared horizon; every train side above half | 6 of 9 |
     | B | Nine windows over the same 48 days | `N_WINDOWS = 9` | reaches the target with no exception; same test loans | windows of 3 to 8 days, shorter than the declared week, which the rules do not allow to reach the count; 8 defaults in two windows |
     | C | Nine windows of about a week from 17 September | the floor in `_make_splits` lowered to 30%, `N_WINDOWS = 9` | reaches the target at the declared length; steady test sizes; the higher default rate of September and early October tested | four windows under half (45.0%, 40.0%, 34.8%, 30.9%), each the curator's exception |
     | D | Calendar weeks | fixed 7-day windows back from the last loan | the horizon exactly | same count as A; test sizes vary more (1,244-2,627) |

     Overlapping windows are not offered: B and C reach the target without them.
   * **Recommendation:** A, with the corrected reason: the 37 days to a settled label and the week-long horizon leave room for six windows above half the data; B shortens the week to reach the count, and C needs four exceptions. **Decision:** A, B, C or D?

   **Notes for the AI:** on A, replace "more windows would leave some with 8" in `splits_comment` (and the `N_WINDOWS` docstring) with: "Six of the nine windows an IID split of this size would get: a label settles 37 days after disbursement, so only the loans from 15 October 2022 have half the rows settled before them, and those 48 days hold six windows of about a week." On B: `N_WINDOWS = 9`. On C: in `_make_splits`, `n_settled >= 0.3 * len(df)` and `N_WINDOWS = 9`, accept `splits_train_under_half` naming this decision, CC line. On D: 7-day calendar windows from 2022-11-25 back to 2022-10-21. Each: rewrite `split` and `splits_comment`, `dataset check`.

   **Andrej (2026-11-19, ok):** As implemented (A).

   **Resolved (2026-11-19, Andrej):** A, as implemented: six windows of about a week, with the reason corrected: a label settles 37 days after disbursement, so only the loans from 15 October 2022 have half the rows settled before them. The splits comment names the target count and what stops more windows; `splits_below_target` is accepted with that reason. The split is unchanged.

   [^split14]: **SPLIT-14** (Must): every window trains on at least half the data, lower only as the curator's exception down to 30%; every test window holds at least 33 scored units.
   [^split15]: **SPLIT-15** (Must for the newest window, Should for the others): the number of windows aims at the count an IID split would get, 9 here; the window length, step and gap follow the use case and are not shortened to reach it; fewer are accepted, never under 3, with the target, the count and what stops more in the splits comment; overlapping windows only as an offered option.
   [^split16]: **SPLIT-16** (Must): few positives in a test window are part of the task; only a window without a positive is a problem, and only for a ranking metric.
