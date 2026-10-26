# african_credit_scoring_challenge

**Outcome:** added. Zindi's African Credit Scoring Challenge: one row is one lender's part of one loan in Kenya
(58,953 rows, 10 features, 1.99% defaults), the target is the loan's default, scored when the loan is paid out, and
the split has nine test windows of at most 30 days, each trained only on loans whose label had settled (30 days past
the due date) before the window starts.
The review panel recommends shipping it; two calls are yours: the filter on the lender's funded amount (issue 2) and
a task that spans two product eras (issue 1). Licence (a note, never a verdict reason, EV-4): the Zindi rules call
the data "private property of the client", and the copy we download is a participant's Kaggle upload made after the
competition closed.

```text
Verdict: ship after changes (the changes are in the definition).
Validity: USE-10 holds (repeat customers scored at disbursement). USE-8 approximate (the share columns are values
  at the data pull; the customer's history is known only through settled labels). USE-5 holds (the label is the
  loan's default: the two rows of a loan agree in 2,132 of 2,134 loans). LEAK-10 triggered twice, fixed: the
  repay amounts (they grow with days past due) and a count of the loan's other lenders (built from the rows at the
  pull, cannot be dated) are dropped. LEAK-24 holds at 30 days (per loan, 31-45 days past due default at 7.2%,
  later buckets 5.8-9.8%). LEAK-25 triggered by the rows of lenders that fund less than one unit, fixed by
  dropping them (issue 2). LEAK-34 holds for customer_id (5 of 13,890 test rows have a defaulted training loan).
  LEAK-38: a note for the two share columns. SPLIT-9/SPLIT-10 hold. SPLIT-20 departed from (two product eras),
  exception recommended (issue 1).
Value: TP-2, a small real signal; TP-9 holds (20-56 default rows per window); TP-1 open until tuned results. The
  task probes flag no_spread, drift_baseline and unstable: untuned LightGBM does not beat a guess of the training
  class shares on the oldest 2024 window (2024-07-11 to 08-09, skill -0.03) and does on the other 4 probed windows.
Quality: CLEAN-11, one impossible share set to missing.
Weighed: real lender task +, size +, two product eras -, near-chance 2024 windows -, a 2024 window where untuned
  models do not beat a guess (the unstable flag) -.
For the curator: issue 8 (ship the Type_1 task?). Issues 1, 2, 6 and 7 settled on 2026-10-26.
```

**Main points:** Ship the Type_1 task, which scores near chance (issue 8)? Settled on 2026-10-26: Type_1 only, ROC AUC over
Zindi's F1, the lender-amount drop, and the country test noted as not reproduced (issues 1, 6, 2, 7).

**Issues for Lennart:**

8. **Ship the Type_1 task, now that it scores near chance?** Issues 1, 6 and 7 are applied (2026-10-26): the task keeps the
   main product only (Type_1, 52,826 rows, 520 defaults, six windows of 1,821-2,446 rows with 18-22 default rows
   each), and the metric is ROC AUC. On it the task probes (5 of 6 windows) give ROC AUC 0.594 for a random forest,
   0.568 for LightGBM and 0.522 for a linear model; the random forest beats the class shares on 4 of 5 windows, and the
   probes flag `no_spread`, `drift_baseline` and `unstable` (TP-1, TP-2, TP-3, TP-5). The mixed task had 0.68 on its
   2022 windows, from telling the products apart.
   - Effect on the task: models are ranked on a weak signal with about 20 positives per window; tuned models may do
     better (the research run's history features reached 0.64), but the windows separate methods poorly.
   - Rule: TP-2 (a small real signal is a task), TP-9 (18-22 positives per window hold the floor), TP-3/TP-5 (a
     probe flag is a question, answered with tuned results, task_probes.md rules 1-3 and 9).
   - Options: (a) ship it with the flags noted, to be re-checked against tuned results (as for the flags before the
     cut); (b) don't ship: a near-chance task with few positives (`Too Small` or `No Good Target`), as digicow
     (recommended `No`, the same mechanism).
   - Recommendation: (a), since TP-2 keeps a small real signal and the windows meet TP-9; (b) if you read 0.59 as no
     usable task.
   - Decision: ship with the flags noted, or don't ship.

   **Lennart (2026-10-26, discuss):** can you check a tuned model and a TFM (run on a rtx gpu node as needed) for this? it
   would worry me if that happens now? Otherwise is the date split still correct or should we use random?

   **Answer (AI, 2026-10-26):** mostly the task, with one model gap; keep the temporal split. ROC AUC per window (newest
   first) on the shipped windows:

   | Model | 11-21 | 11-14 | 11-04 | 10-27 | 10-21 | 10-15 | Mean ± SE |
   |---|---|---|---|---|---|---|---|
   | LightGBM, untuned (probe settings) | .563 | .668 | .502 | .602 | .614 | .553 | .584 ± .023 |
   | LightGBM, tuned (100 Optuna trials per window) | .597 | .673 | .529 | .678 | .628 | .691 | .633 ± .025 |
   | CatBoost, tuned | .539 | .717 | .511 | .653 | .705 | .782 | .651 ± .043 |
   | CatBoost, default | .729 | .603 | .536 | .633 | .694 | .735 | .655 ± .032 |
   | TabPFN v2 (public weights, RTX PRO 6000, 10k-row training sample) | .576 | .586 | .540 | .662 | .581 | .616 | .594 ± .017 |

   - Each window has 18-22 defaults, so its AUC alone carries about ±0.065 of test noise: differences under about
     0.05 are noise, and the windows cannot rank close methods. Tuning lifts LightGBM (+0.049 ± 0.020) and adds nothing
     to CatBoost; nothing passes about 0.66 on the shipped features.
   - The one real gap: the signal is the customer's history, which the models reach only through `customer_id`
     (without it CatBoost falls to 0.550). The count of the customer's earlier loans, known at disbursement and built
     without labels, scores 0.719 ± 0.032 alone, above every model.
   - The split: a random split of the same rows scores 0.78 (CatBoost; 0.92 pooled over all rows), but only because
     98.3% of defaults fall on the customer's last loan in the data, so a random split shows a model whether the
     customer borrowed again later (the count of later loans alone reaches 0.95). Grouped by customer it falls to
     0.556. The lender scores at disbursement and trains on settled loans, so the temporal split stays (SPLIT-9; a
     validity reason, not a score).
   - Options: (a) ship it with a history feature a data scientist would build: the customer's number of earlier loans
     (and of earlier settled defaults) at disbursement (CLEAN-19, a history aggregated per prediction; the probe
     numbers above would move toward 0.72); (b) ship it as it is, with the flags noted; (c) don't ship (`Too Small`:
     18-22 defaults per window rank methods poorly).
   - Recommendation: (a), then re-run the probes; (c) if you read 18-22 defaults per window as too few even with the
     feature.

**Review panel:** ship after changes (mediator). Claim audit: 74 claims, 59 hold, 3 refuted, 11 untested, 1 not
reproduced; corrected in the definition: "no link to the outcome" for the count of a loan's other lenders (the count
is dropped), the period "2022 to 2024" (39 rows are from 2021) and the 0.98% default rate of July-November 2022 (the
Type_1 7-day rate; all rows 1.16%). Column audit: no kept column recorded after the outcome; the two share columns
have no recording time and stay with a LEAK-38 note; one impossible share, set to missing. Split audit: right with
notes; its question on the newest labels was settled by the mediator's count per loan (30 days kept). Blind review:
include with changes; main concern the uneven spread of the rows over time. Debate: agreed on the wording fixes and
the SPLIT-20 exception; disputed and settled by the mediator: the count of a loan's other lenders (dropped under
LEAK-10, a count we build from the rows at the data pull; the critic would have kept it with a note) and 30 or 45
days to settle a label (30 kept); left to the curator: the zero-share filter. The mediator's issue 1 is issue 2 here, its issue 2 is issue 1.

<details><summary>Claim audit</summary>

**Claim audit: african_credit_scoring_challenge (2026-10-20, re-check)**

Scripts and outputs: (panel run). Data: the definition's frame and split plan via `dataset_io.from_definition` (58,953 rows, 9 windows), raw
Train.csv / Test.csv. Models: untuned LightGBM (default params; 3 seeds with 0.8 row/col bagging where stated),
logistic regression with one-hot categoricals; ROC AUC mean over the 9 windows (EV-5, EV-8).

**Table**

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 1 | Kenya borrower default at disbursement | TS.question | country in Train, prediction-point columns | holds | Train.csv 100% Kenya | USE-1 |
| 2,23 | scored at disbursement from loan terms and settled earlier loans; monthly refit | TS.use_case, CC1 | train sides vs window start | holds | every train row settles before its window starts (all 9) | USE-3, SPLIT-9 |
| 3 | rows from 2022 to 2024 | TS.row | min date of kept frame | **refuted (minor)** | 39 kept rows from 2021-10-04 to 2021-12 | CLEAN (wording) |
| 4,42 | 54,163 of 58,953 in Jul-Nov 2022, mostly Type_1 7-day; "(0.98% defaults)" | TS.row, CC14 | count | holds; 0.98% is the Type_1 7-day rate, all Jul-Nov rows 1.16% | 54,163; 97.5% Type_1; 98.1% 7-day | writing |
| 5,30 | label = whether *that lender's part* defaulted; per-lender label (host) | TS.predicted, CC6 | label agreement in two-row loans | **untested, data leans the other way** | labels differ in 2 of 2,132 two-row loans (both shares >= 0.5); codebook: "1 means the customer defaulted on the loan" | USE-5, EV-2 |
| 6 | about 2% defaults | TS.predicted | rate | holds | 1.99% | - |
| 7 | label settled 30 days after due date; source states no other horizon | TS.predicted | codebook + Zindi page | holds | Zindi: "1 indicates a loan default", no days-past-due rule | SPLIT-10 |
| 8 | features known at disbursement | TS.known | New_versus_Repeat vs first appearance; ID check | holds except the share/count columns (see 15-16) | "New" never after a customer's first date, "Repeat" never on it (0 of 58,953) | LEAK-10 |
| 9,34,49,50 | 9 windows <= 30 days; train = settled before start | TS.split, CC8, SC | spans, overlap, max settle date | holds | spans 5-30 days, 0 overlap, max train settle = start - 1 day in all 9 | SPLIT-9, SPLIT-12 |
| 10,28,64 | repay amounts grow after default | TS.changes, CC5, D1 | D1 table | holds | repaid median charge 3.5% flat; defaulted 4.6% -> 33.9% with days past due | LEAK-10 |
| 11,29 | 8,899 rows < 0.5, none labelled 1 | TS.changes, CC6 | count | holds | 8,899 (8,520 = 0), 0 labelled 1 (about 105 expected at the period rate) | LEAK-22 |
| 31,66,67 | about 130 defaults hidden; 1.04% vs 0.40%; 89% | CC6, D2 | D2 table, charged dropped rows | holds (approx.) | 90/8,667 = 1.04%, 114/28,594 = 0.40%, 101/114 = 89%; 126 dropped rows with charge > 20% x 0.87 = about 110 | - |
| 12,33 | 802 unsettled rows dropped (84 labelled 1) | TS.changes, CC7 | count | holds | 802, 84 | LEAK-12 |
| 13,25 | competition split rows at random; we split by date | TS.changes, CC3 | not on data | untested (Zindi split not public) | - | SPLIT-5 |
| 14,15 | fit approximate; share/count columns are values at the pull | TS.fit | no timestamp of share changes in the data | untested (cannot be dated) | - | USE-8 |
| 16,45 | share columns "show no link to the outcome"; LGBM 0.639 with, 0.635 without | TS.fit_reason, CC15 | rates by value within period; single-feature AUC per window; ablation over 3 seeds | **refuted (the "no link")**; ablation number holds as "no gain" | other_lenders_on_loan=1: 7.2% default vs 1.05% in Jul-Nov 2022 (n 1,010 vs 53,169); 6.9% vs 1.0% on the 2022 test rows; single AUC 0.67/0.63 in W3/W4. Ablation: full 0.633, no share cols 0.640, also no other_lenders 0.664 (each seed higher) | LEAK-5, LEAK-38, EV-9 |
| 17,43 | sampling not stated | TS, CC14 | Zindi page | holds | page says nothing on sampling | PROV-2 |
| 18,19,20,48 | year/source/licence; login; Kaggle uploader | meta, DL, CC17 | not on data | untested (licence never evidence) | - | EV-4 |
| 21 | byte sizes | DL | ls -l | holds | 8,785,708 / 2,379,732 / 7,930 / 1,539 | PROV-1 |
| 22,24 | competition 2024-11-29 to 2025-01-12; F1 | bibtex, CC2 | Zindi page | holds | page: 29 Nov 2024 to 12 Jan 2025, F1 | - |
| 26 | other_lenders_on_loan 0/1 counted over both files | CC3 | value counts, partners | holds | {0: 54,537, 1: 4,416}; two rows of a loan share date, customer, Total_Amount (100%) | - |
| 27 | ID composite; country Kenya | CC4 | string check | holds | 100% | - |
| 35,37 | customer history legitimate; train holds settled loans only | CC9 | split check | holds | as 9 | LEAK-34 |
| 36 | a default usually ends a customer's history | CC9 | borrowed again after a row | holds | after label 1: 7.1%; after label 0: 89.3% | - |
| 38 | New_versus_Repeat differs in 133 of 2,134 two-row loans | CC10 | count | holds | 133 / 2,134 | - |
| 39 | due = disbursement + duration | CC11 | equality | holds | 100% | - |
| 40 | economic_indicators end at 2023 | CC12 | columns | holds | last column YR2023 | - |
| 41 | 275 extra identical copies, own tbl_loan_id, same date | CC13 | duplicated() on kept frame | holds | 275 (276 counting tbl_loan_id-free raw columns of kept rows); every duplicate group has distinct tbl_loan_ids | LEAK-16 |
| 47 | probes flag no_spread, drift_baseline | CC16 | (panel run) | holds | same flags; tuned results absent (panel run) | TP-1, TP-3 |
| 51-53 | window rows, loans, defaults, dates | SC | recomputed | holds | 2024: 500-677 rows, 296-394 loans, 32-56 default rows; 2022: 1,812-2,206 rows, 20-31 defaults, 5-10 days; first half-settled day 2022-10-20; last Type_1 2022-12-01; 9 non-Type_7 rows | SPLIT-14, TP-9 |
| 54,55,63 | 1,901 rows between; 6 long loans in no split | SC, AW | recount | holds | 1,901; 6 rows (2023-09-19, 2024-06-11 to 06-15, 60-365 days) | SPLIT-11 |
| 56 | 2022 windows lose 8-18% of their dates' rows | SC | recount | holds | 8.2-17.9% | - |
| 57 | equal-row buckets: one window 2022-12-16 to 2024-07-10 (573 days), 28% unseen products | SC | rebuilt the 9 buckets | holds | 573 days, 28.4% | SPLIT-21 |
| 58 | equal-distinct-date windows: Mar 2023-Oct 2024, 112-872 rows, 95% train only | SC | my 10-part reconstruction gives other windows | untested (the "as kick" scheme not specified enough to rebuild) | - | - |
| 59-62 | pure-value hits; July Type_1 0.37% vs 0.88-1.49%; charges 0.42%; no hit row in test; all but 4 on every train side | AW | bundle_checks `_pure_values` rerun; rates | holds | 11 + 10 hit values, 8,623 rows, 0 in test, 4 not on every train side (Type_4, 27-28 July); kept-share Type_1 Aug-Nov 0.88-1.49% | EV-3 |
| 65 | Lender_portion_to_be_repaid = Total x share | D1 | within 1 unit | holds | 98.9% | - |
| 68 | 2024 late-payment rates | D3 | table | holds | 19.6% / 15.3% / 11.6% vs 6.9-10.2% | LEAK-24 |
| 69 | seen customers 85-96% (2022), 12-44% (2024) | D4 | recount | holds | 0.85-0.96, 0.12-0.44 | - |
| 70 | Spearman 0.9999 tbl_loan_id vs date | CODE | spearman | holds | 0.99987 | - |
| 71 | data pull = max disbursement date | CODE | rows per day at the end of Train.csv | holds (no sign of a cut) | last day 2024-11-14: 33 rows vs median 21/day since July 2024 | - |
| 72,73 | Temporal split; grouped does not fit | RF, RA | see 9, 35 | holds | - | SPLIT-1, LEAK-34 |
| 74 | AUC 0.907 with repay amounts | RA | add both amounts back | holds | 0.901 | LEAK-10 |
| 75 | linear 0.649, CatBoost 0.672 | RA | logistic, one-hot | not reproduced (setup-dependent); CatBoost untested (not installed) | logistic with one-hot customer_id: 0.705 | EV-8 |
| 77,78 | signal mostly customer history; LGBM 0.639 / 0.527 without customer_id; count alone 0.682 | RA | ablation; count score | holds qualitatively; count exact | without customer_id 0.566 (1 seed) / 0.588 (3 seeds); count 0.682 exactly | TP-2 |

**Implied claims**

* Every feature known at disbursement: holds for all but `other_lenders_on_loan`, `Amount_Funded_By_Lender`,
  `Lender_portion_Funded` (values at the pull, cannot be dated; see 16).
* The split the use case needs: holds (temporal, settled-label as-of, windows <= 30 days; W8 train side 50.6% of rows,
  SPLIT-14 met narrowly).
* Target is the real-world target: approximately; it behaves as the loan's default (2 of 2,132 two-row loans disagree),
  not a per-lender outcome (see 5).
* No copy across the split: holds, 0 exact feature copies across any train/test pair; the two rows of a loan always
  fall on the same side (same date). Within a 2024 test window they double-count a loan (51 default rows = 28 loans).

**Refuted and untested, ranked (validity first)**

1. **16/45, "no link to the outcome" (P4, LEAK-5/LEAK-38, Should).** `other_lenders_on_loan` = 1 defaults 7x more
   often in the same months and on the 2022 test rows. Whether that is co-funding set at disbursement (rows of a loan
   share date, customer and amount; lender 245684 funds a flat 10,000) or a buy-out after default cannot be dated. It
   does not inflate scores: dropping it raises mean AUC 0.640 -> 0.664 on every seed. Changes: the note's
   justification is false as written; the column is our own construction from the pull-time row set, not an
   unverified host field, so the LEAK-38 precedent (kick) fits it less well. Mildest remedy: rewrite the note with
   these numbers; the curator decides keep (LEAK-38 note) or drop `other_lenders_on_loan` (costs nothing in AUC).
2. **5/30, per-lender label (P3, USE-5).** Untested; data agree with the codebook (customer/loan default). Remedy:
   word TS.predicted as the loan's default recorded per lender row, cite the 2 / 2,132 agreement; keep CC6's
   zero-share reasoning on the 0-of-8,899 fact.
3. **75, linear 0.649 (EV-8).** Not reproduced (0.705 with one-hot customer_id). Remedy: state the encoding with the
   number.
4. **3, "2022 to 2024" (writing).** 39 rows from late 2021. Remedy: "October 2021 to October 2024".
5. Untested, no action: 13, 14-15, 18-20, 48 (pages/licence), 58 (scheme not reproducible from the text).

</details>

<details><summary>Column audit</summary>

**Column audit: african_credit_scoring_challenge (2026-10-20, re-check)**

Prediction point (CC bullet 1): when a loan is disbursed, with the customer's settled earlier loans known. Codebook:
VariableDefinitions.txt (Zindi) (Zindi; one line per column, no
recording times). Frame: the definition's own frame, rebuilt through `dataset_io.load(..., built=False)`: 58,953 rows,
11 features + `default` (1,174 Yes, 1.99%). Scripts and outputs: (panel run).

**Column table**

| column | meaning (codebook) | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| customer_id | unique customer id | yes (an id) | category, 6,363 levels, raw int64 ids 145-312,737; same as ieee `uid` | fine: entity history under a temporal split; training sides hold settled loans only | LEAK-34, USE-10, CLEAN-14 |
| lender_id | lender or institution that issued the loan | yes | category, 4 levels (267278: 55,373 rows) | fine. Default rates 1.3% / 8.7% / 32% / 41% follow product: 267277 lends Type_9/Type_2, 245684 Type_14/11/12 (2021-10 to 2022-04 only) | LEAK-10 holds |
| loan_type | category of loan | yes | category, 19 levels (Type_1 52,826 rows, 2022-07-12 to 12-01 only) | fine; carries most of the period/product shift | CLEAN-14 |
| Total_Amount | total amount initially disbursed | yes ("initially") | float, 2 to 23,000,000; 31 rows < 50 (13 rows of 2-5, all Type_1 7-day, all 0) | fine; tiny amounts unusual, not impossible: keep | CLEAN-11 |
| disbursement_date | date paid out | yes (it is the prediction point) | datetime %Y-%m-%d, 2021-10-04 to 2024-10-08, frame sorted by it | fine (time index, CLEAN-23 holds) | CLEAN-14, CLEAN-23 |
| due_date | date by which repayment is due | yes | datetime; equals disbursement_date + duration in 58,953 of 58,953 rows | fine. The identity also shows no rescheduled (post-outcome) due dates. Redundant but not a copy of one column; kept as a source column | LEAK-10 holds; CLEAN-5 n/a |
| duration | loan term in days | yes | int64, 1-548 (7 days: 55,310 rows) | fine | |
| New_versus_Repeat | first loan or repeat | yes | category, 2 levels (New 524 rows, 22.1% default; Repeat 1.8%) | fine; read per lender (differs within 133 two-row loans); 59 "New" rows are not the customer's first row in the data, consistent with a per-lender or pre-2021 history | LEAK-10 holds |
| Amount_Funded_By_Lender | portion of the loan funded by the lender | unknown: codebook gives no time; the host says lenders can buy each other out, so possibly a value at the pull | float, 0.5 to 1,600,000 (filter >= 0.5) | potential leak, kept with note: weak. No outcome link within a product (Type_1 AUC 0.46, Type_1 rows of the 2022 test windows 0.34-0.62 on 12-26 positives); the full-frame link is product mix | LEAK-38 (kick precedent), LEAK-6 |
| Lender_portion_Funded | lender's share of the loan | as above | float, 0.0002 to 1.168; = amount / Total_Amount in every row (|diff| < 0.01). One row 1.168 with amount 2,627.1 > Total_Amount 2,249 | potential leak kept with note (weak, as above: Type_1 AUC 0.49; within-window Type_1 0.39-0.59). Cleaning: 1 impossible row | LEAK-38; CLEAN-11 |
| other_lenders_on_loan | built: count of the loan's other lender rows over Train.csv and Kenya rows of Test.csv | as the shares (values at the pull) | int64 0/1; 794 of 4,416 partner rows sit in Test.csv (ids only, no labels read) | fine / weak note. 8.0% vs 1.5% default marginally, but within each product the two-lender rows default the same or less (Type_4 11.0% vs 15.5%, Type_5 6.7% vs 9.7%, Type_10 2.2% vs 3.7%); Type_7 is 99.6% two-lender. Counts 2 rows whose partner was dropped (< 0.5): negligible | LEAK-38; LEAK-29 n/a (a per-loan count, no statistic) |
| default (target) | target 1 = customer defaulted on the loan | label settled 30 days after due date | category Yes/No | fine as filtered; the two rows of a two-lender loan share the label in 2,132 of 2,134 loans and the same date, so they are never split apart | LEAK-12, LEAK-24 |
| ID (dropped) | entry id = customer + loan + lender | id | dropped | fine | CLEAN-3 |
| country_id (dropped) | country | constant Kenya in Train.csv | dropped | fine | CLEAN-5 |
| tbl_loan_id (dropped) | loan id; sequence number (Spearman 0.9999 with date) | id | dropped; makes 275 extra copies exact (212 vectors with >1 row, 1 with both labels) | fine, duplicates decided (same date, so never across a split) | CLEAN-3, LEAK-16 |
| Total_Amount_to_Repay (dropped) | total expected repayment incl. interest and fees | no: grows with days past due at the pull (penalties) | dropped | leak removed (AUC 0.907 with, 0.639 without) | LEAK-10, LEAK-2 |
| Lender_portion_to_be_repaid (dropped) | lender's part of the above | no (sibling) | dropped | leak removed with its sibling | LEAK-2 |

Not joined: economic_indicators.csv (a function of the year for Kenya, no 2024 values): fine.

**Problems, ranked (principles.md)**

1. **P4, LEAK-38 / LEAK-10 (Should, weak; already documented): the share columns and the row filter rest on fields of
   unknown recording time.** Evidence: no outcome link within a product (above); Type_1 shares drift by month (25th
   percentile 0.101 in Sep 2022, 0.300 in the other months), consistent with shares that change after disbursement.
   The filter `Amount_Funded_By_Lender >= 0.5` selects rows on the same field (REVIEW issue 2); the kept tiny-amount
   rows (0.5-10) default at 0.6-1.3%, like Type_1 overall (1.0%), so the threshold does not leave the mechanism behind.
   Remedy: keep, with the note; the open call is issue 2. Wording fix (cheap): `fit_reason` and CC say the columns
   "show no link to the outcome"; the marginal link of `other_lenders_on_loan` is 8.0% vs 1.5% and of lender_id up
   to 41%; say "no link within a loan product".
2. **P7, CLEAN-11 (Should, 1 row): impossible share.** Row with Lender_portion_Funded 1.168 and
   Amount_Funded_By_Lender 2,627.1 above Total_Amount 2,249 (Type_1, label 0). Remedy: set the two values to missing,
   or leave it with no note; negligible.
3. **Question (no rule broken): `due_date` is fully determined by `disbursement_date + duration`.** Kept as a source
   column (CC); harmless. No action.

No column is post-outcome among the kept ones; no proxy missing values (0 missing anywhere); no encoding to reverse.
Judgment: Validity: LEAK-10 holds for kept columns (repay amounts dropped), LEAK-38 note stands (weak); LEAK-12/24 hold
(30-day settled rule). Quality: CLEAN-11 one row; CLEAN-14 dtypes by meaning hold.

</details>

<details><summary>Split audit</summary>

**Split audit: african_credit_scoring_challenge (2026-10-20, re-check)**

Scripts and outputs: (panel run) (definition frame
rebuilt through `dataset_io.definition`; untuned LightGBM, 300 trees, thread caps 2). Raw pull date (max disbursement in
Train.csv): 2024-11-14; last kept disbursement 2024-10-08.

**Verdict: right with notes**

Temporal on `disbursement_date` is the regime the use case implies (USE-10, SPLIT-6, SPLIT-13): a lender scores new
and repeat customers at disbursement and refits monthly; repeat customers' settled history is legitimate. The per-row
gap (`due_date + 30 < window start`) implements SPLIT-9/SPLIT-10 correctly. One open question on the newest edge.

**Facts per window (shipped plan)**

| w | test days | test rows / defaults | train rows (share) | last train disb. to start | rows before start not in train | test label age at pull (min / median, days past due) | test rows: customer in train / with any earlier loan |
|---|---|---|---|---|---|---|---|
| 0 | 2024-09-09..10-08 | 677 / 51 | 57,573 (0.977) | 38 d | 703 | 30 / 43 | 0.44 / 0.70 |
| 1 | 2024-08-10..09-08 | 593 / 56 | 57,076 (0.968) | 38 d | 607 | 55 / 75 | 0.25 / 0.67 |
| 2 | 2024-07-11..08-09 | 500 / 32 | 56,938 (0.966) | 59 d | 245 | 90 / 105 | 0.12 / 0.41 |
| 3-8 | 2022-10-20..12-01 (5-10 d each) | 1,812-2,206 / 20-31 | 29,819-41,843 (0.506-0.710) | 32-38 d | 11,308-13,343 | 351-505 / 712-747 | 0.85-0.96 / 0.97-0.99 |

Type_7 rows on the training side of the 2024 windows: 688 / 216 / 98 (first Type_7 loan 2023-07-27); the rest is
mostly 2022 Type_1. 2022 Type_1 weekly default rate in the test weeks 0.48-1.35%, inside the Sep-Oct range
0.57-1.71%: the end of the Type_1 lending is not an atypical stretch by rate (volume falls to 622 rows in the last week).

**Alternative splits (LightGBM AUC, mean over windows)**

| split | all features | without customer_id |
|---|---|---|
| shipped temporal (9 windows) | 0.631 (0.488-0.838) | 0.563 |
| shipped, test rows of w0 limited to labels >= 45 days past due | 0.635 (w0: 0.637 -> 0.673, 302 rows) | - |
| IID 5-fold stratified (the competition's random split) | 0.853 | 0.805 |

The random split overrates by about 0.22 AUC (it mixes eras with default rates of 1% and 7-70% and rewards
"the customer's last loan"); the temporal regime stands (SPLIT-1, SPLIT-5). No grouped alternative is warranted: the
use case predicts for known customers (USE-10), and the gap already removes their unsettled loans (in w0-w2, 70/67/41%
of test rows have an earlier loan but only 44/25/12% a settled one in training).

**Problems, ranked (all P4)**

1. **Labels at the newest edge may be unsettled at 30 days (SPLIT-9, SPLIT-10; question, EV-3).** Type_7 2024 rows
   30-37 days past due at the pull default at 14.1% (31/220) against 1.8-11.3% in every later bucket (pooled 31-120
   days: 7.4%); the last two disbursement days (2024-10-07/08, 30-31 days past due) at 13/66 = 20%, against 2/50 on
   10-01/02. This is the pattern of decision table 3 (19.6% at 1-7 days), just past the 30-day cut. Weekly rates
   are noisy (1/142 to 20/183), so the evidence is moderate. Mildest remedy: LABEL_SETTLED_DAYS = 45 (drops about 390
   newest rows; w0's AUC moves 0.637 -> 0.673 on the settled rows), or keep 30 and state the edge in the splits
   comment.
2. **Training labels are the labels at the pull, not as known at the window start (SPLIT-10, note).** A lender refit
   at a window start would see loans 31-60 days past due with labels still moving; the data has one pull, so this
   cannot be simulated. Mild optimism, write it in `predicted`/splits comment; no remedy.
3. **Two populations in one task (SPLIT-11, SPLIT-15, SPLIT-20; open REVIEW issue 1).** The six 2022 windows walk back
   19 months past the sparse period; the three 2024 windows test Type_7 loans (7% defaults) with 98-688 Type_7
   training rows and score near chance (0.488-0.637). Documented and reasoned; training history keeps the product
   break (SPLIT-20) but a history cut must not be chosen from these few windows (SPLIT-21). No change asked.
4. **Window 8's train side is 50.6% of rows**, at the SPLIT-14 floor (passes; any extra 2022 window would break it).
5. **Test windows exclude rows filtered on a field at the pull** (Amount_Funded_By_Lender < 0.5, 8-18% of 2022 test
   dates; REVIEW issue 2, LEAK-10): a selection of test rows on a post-disbursement value. Column auditor's call; the
   rows are labelled 0 by construction, so dropping is the lesser harm.

Checked and fine: horizon 30 days and no window longer (SPLIT-12); expanding train (SPLIT-11); >= 3 windows, >= 500
test rows each (SPLIT-14, SPLIT-17); exact copies and both lender rows of a loan share a date, so never cross the split;
6 long loans in no split (accepted warning) verified.

</details>

<details><summary>Domain practitioner</summary>

**Practitioner review: african_credit_scoring_challenge (2026-10-20, re-check)**

Actor: the credit team of a Kenyan digital lender (the unnamed "private asset manager" of the Zindi page and its
co-funding lenders) that approves and disburses small, mostly 7-day loans to repeat customers (USE-1).

**Fit**

**Approximate** (USE-8): the row, the moment and the label are a real lending decision, but the strongest input a
lender has at that moment, the outcome of the customer's loan that has just been repaid, is held back 30+ days by the
settlement rule, the sample is 99% repeat customers of one product in six weeks of 2022, and the share columns are
pull-time values kept on purpose. I agree with the definition's `approximate`; a direct fit under USE-9 does not apply,
since no other use case removes these gaps.

**1. Inputs at the prediction point (USE-3, USE-6, USE-10)**

What I would have, and the dataset gives: customer (as an id), product, amount, duration, disbursement and due dates,
lender, new/repeat. Correct to drop `Total_Amount_to_Repay` and `Lender_portion_to_be_repaid` as recorded: they grow
with penalties (LEAK-10). Note that the *contracted* repay amount (the price I set) is known at disbursement and is a
legitimate input I lose with them (USE-6); it cannot be recovered from the pull-time value.

What I would not have: `Amount_Funded_By_Lender`, `Lender_portion_Funded`, `other_lenders_on_loan` are values at the data
pull and lenders can buy each other out (CC15). Kept on purpose with a measured null effect (0.639 vs 0.635); acceptable
under USE-8 as a named gap, not verified by me. The row filter on `Amount_Funded_By_Lender >= 0.5` also selects test rows
on a pull-time field (REVIEW issue 2).

What I would always have and is missing, ranked:
1. **The customer's repayment record up to today.** In my data ((panel run), on the shipped rows):
   89% of rows have an earlier loan of the same customer, 36% have an earlier loan already due before this
   disbursement, but only 2.2% have one due 30 or more days before. The previous loan's label is the strongest signal
   there is: 80% of rows after a defaulted loan default (248 rows), against 1.1% after a repaid one. A lender knows a
   repaid loan the day it is repaid, and knows a loan is overdue the day after the due date; the 30-day rule (plus
   window lengths up to 30 days) keeps exactly that knowledge out of training. The rule is right for the *label*
   (late payers do pay later, decision table 3), but it makes the benchmark weaker than the real decision, where
   "days past due on the current/previous loan" is a feature, not a label.
2. **Engineered history**: number of earlier loans, days late on each, time since last loan, limit utilisation. The
   dataset offers only the raw `customer_id` as a categorical; a model must rebuild history from a high-cardinality id,
   which favours target-encoding models (CatBoost 0.672 vs LightGBM 0.639 with id; 0.606 / 0.527 without).
3. **External data**: credit reference bureau (CRB) listing and score, mobile-money transaction summaries, the loan limit
   offered. Every Kenyan digital lender has at least the bureau check; none is in the source. A source gap, not a
   curation error.

**2. Target (USE-5)**

What I act on is "will this customer not repay this loan (within some grace period)", as a probability, to approve,
size the limit and price. The label is close to that, but: (a) its horizon is not stated by the source (default as
recorded at the pull; the 30-day settlement is the curator's choice); (b) the row label follows one lender's share,
while the codebook says "1 means the customer defaulted" (CC6 cites the host, unverifiable without login); (c) the
zero-share rows were labelled 0 by construction and are dropped. A probability is what I would want; ROC AUC ranks it,
so it fits; a lender would also check calibration in the top risk bins (the Zindi finalists had to bin scores into risk
grades).

**3. Rows, test data (USE-10, USE-11)**

One row is one lender's part of one loan: two rows for 2,134 loans (about 4% of rows). My decision is per loan, not per
co-funder; small mismatch. The decision I actually make is approval *before* disbursement, and the data holds only
approved, disbursed loans (no declined applicants, so no reject inference): normal for credit benchmarks, but it
means the model learns on the population an existing policy already filtered. Test data: next 5-10 days of one 7-day
product in late 2022 (six windows), and three 30-day windows of 2024 dominated by Type_7 loans to customers mostly
unseen (12-44% seen). The first is what I face weekly; the second is a product launch with almost no history, where
every model is near chance (CatBoost 0.484-0.619). The source promises "existing customers and new applicants", but
99.1% of rows are repeat loans, so the new-applicant case is absent.

**4. Would I use it?**

I would use this as a baseline ranking of repeat 7-day loans, not as my scorecard. Trust: a temporal split, a settled
label, the leaky repay amounts gone. Distrust: (1) the near-chance 2024 windows show the model does not transfer to a
new product; (2) the signal is mostly "who is this customer" (count of training rows alone 0.682 vs CatBoost 0.672);
(3) sampling of loans unknown (CC14; 54,163 of 58,953 rows in five months of 2022); (4) a pull-time share filter on the
test rows.

**Gaps, ranked by how much they change the task**

1. Lagged customer history: the last loan's outcome, known to a lender at once when repaid, is missing from training
   for nearly all test rows (settlement rule + window length). Changes the task from "score with my full ledger" to
   "score with a ledger 30-60 days old". (USE-3, USE-10)
2. Customer history given only as a raw id, no engineered features; benchmark measures id-encoding as much as risk.
   (USE-10)
3. Population: 99% repeat loans of one product over six weeks, plus a near-chance 2024 product; unknown sampling.
   (USE-8, USE-1 row/period)
4. Label horizon not stated; per-lender-share label vs per-customer codebook. (USE-5)
5. Pull-time share columns kept and used as a row filter. (USE-8, LEAK-10)
6. Contracted price lost with the dropped repay amounts; no bureau/mobile-money data. (USE-6; source gap)

**What a credit expert would change**

* Add, per row, features a lender has at disbursement and computable without leak from the shipped rows: the
  customer's count of earlier loans disbursed, and the outcome of earlier loans whose due date passed (repaid on time /
  overdue at disbursement). This is a feature-engineering choice the benchmark may prefer to leave to the model; if it
  stays out, say in `fit_reason` that the history is "known only through settled labels on the training side".
* Consider a shorter settlement for the training side of *repaid* loans (a repayment is final once made), keeping 30
  days only for the default label; or state why not. The REVIEW numbers (0.676 with due date only) show how much this
  matters.
* Report calibration or a top-decile default capture next to ROC AUC for the user who sets limits (not a change to the
  objective metric).
* Keep the 2022 windows as the core task; flag the 2024 windows as a product-launch / cold-start test in the
  splits comment rather than as the same task.

**Sources**

* `african_credit_scoring_challenge` dataset.py, record, panel `REVIEW_before.md`,
  `claims.md`, `checklist.md`.
* VariableDefinitions.txt (Zindi).
* (panel run): history timing and previous-loan signal on the shipped rows.
* Zindi competition page: https://zindi.world/competitions/african-credit-scoring-challenge (provider "a private asset
  manager", "existing customers and new applicants", F1, risk-bin scoring function for finalists).
* Kenyan digital-credit context: https://www.businessdailyafrica.com/bd/corporate/companies/digital-mobile-defaulters-out-of-platforms-3282988 ,
  https://www.findevgateway.org/paper/2017/03/where-credit-due-customer-experience-digital-credit-kenya ,
  https://www.nation.co.ke/oped/opinion/Regulate-digital-loans-sector/440808-4648284-v55la6z/index.html (CRB days-in-arrears
  scoring, daily re-scoring of digital loans).
* Rules: use_case.md` (USE-1, 3, 5, 6, 8, 9, 10, 11), LEAK-10.

</details>

<details><summary>Blind review</summary>

**Blind review: african_credit_scoring_challenge**

**Verdict: include with changes** - a real, application-time loan-default task with honest features, but the time split is dominated by a two-quarter burst and a lender/period shift, which needs fixing before scores mean much.

**Task**
A digital lender (Kenya, Zindi challenge "African Credit Scoring") scoring a short-term loan at disbursement: approve or not, at what amount. Real use. All 11 features (amount, lender share, loan type, duration, dates, new/repeat, co-lenders) are known at disbursement; due_date - disbursement_date == duration on every row (redundant, not leaky). Default rate 1.99% (1,174 positives).

**Concerns (most to least serious)**
1. **Time distribution is extremely uneven, so the 9 temporal windows are unbalanced and confounded.** 54,441 of 58,953 rows (92%) were disbursed in 2022Q3-Q4; other quarters hold 39-1,655 rows. Default rate swings from 1.1-1.4% (2022Q3-Q4) to 8-54% elsewhere. Lender 267278 has 55,373 rows at 1.3% default; the other three lenders run 8.7-41%. Equal-width or equal-count windows will either give tiny test sets with a handful of positives or let one lender's regime decide the score. Change: report the window sizes and positives per fold; set a minimum positives per test window (e.g. >=50) or merge sparse windows; consider restricting to the dense 2022-07..2022-12 period, or a random/grouped split if the time axis cannot carry 9 folds.
2. **Repeated customers and multi-lender loans.** 6,363 customers over 58,953 rows; 75% of late-test rows belong to customers already seen in training. The source says one loan "can appear with different lender IDs" (multiple rows); the loan id was dropped, so co-funded loans become near-duplicates (276 exact feature duplicates). Under a time split this is realistic (repeat borrowers), but customer_id as a numeric feature adds AUC (0.779 with vs 0.752 without, holdout of last 20%, 452 positives) - likely an ID-encodes-onboarding-time effect. Change: drop customer_id as a feature (or keep it only as a group key), and dedupe rows of the same loan id if available.
3. **Dates as features.** Without disbursement/due dates, AUC drops to 0.652; much of the signal is regime/period. Under a forward split raw dates extrapolate badly; prefer derived calendar features (month, weekday) or drop.
4. **Rows vs source.** The source Train.csv (Kenya) is larger than 58,953 rows (I recall ~68.6k); I could not verify which filter (dedupe, country, ID) produced this count. Ghana test rows have no labels, so they are rightly absent. Document the filter.
5. Minor: Total_Amount max 23,000,000 vs median 5,279 and Lender_portion_Funded max 1.168 (>1) - plausible data entry quirks; leave but note. Target stored as category "Yes"/"No" - fine.

**Signal**
LightGBM forward holdout AUC 0.65-0.78 depending on ID/date use: real, non-trivial signal; enough rows, but only ~1.2k positives total.

**Not checked**
Could not download Train.csv/VariableDefinitions.txt (login needed), so exact target definition (days past due), the row filter, and licence terms are unverified. Exact fold boundaries of the 9 windows were not given.

</details>

<details><summary>Precedent check</summary>

**Precedents: african_credit_scoring_challenge (2026-10-20)**

**Inputs**
- the precedent register of the panel run
- The panel's `REVIEW_before.md` (same text as `african_credit_scoring_challenge` REVIEW.md) and `checklist.md`
- `dataset.py` and the record
- The Cases tables of `splits.md`, `leak_checks.md`, `task_probes.md`, `use_case.md` and `evidence.md`
- Sibling definitions and records: Zindi (digicow, expresso_churn_prediction_1m, fraud_detection_in_electricity_and_gas_consumption_1m, dataorg, alvin_smart_money) and credit (alfa_battle_2_0_task_2, lending_club, mortgage, rosbank1, home_credit_*, amex_non_iid_1m)

**Status of the decisions.** The record has no `CC` line, so every decision below is an AI decision. That includes the 2026-10-07 `task_probes.md` Cases row "kept", which the CHANGELOG 2026-10-07 batch of 59 definitions wrote. The curator has not confirmed any of it, and under "Who decides" these rows rank below a curator's call. The drift check (case 3) does not apply to this dataset. Lennart's own decisions on the same rules elsewhere are consistent with each other (D4).

**Register flags.** None of the 4 flags (few_minority, one_feature, scaling over all rows, trivial) involves this dataset.

**Per decision**

| # | Decision (where) | Rules | Verdict | Closest precedents |
|---|---|---|---|---|
| D1 | Temporal only, not Grouped+Temporal; the competition's random Train/Test split replaced (record, splits) | SPLIT-3, SPLIT-5, SPLIT-19, USE-10 | **consistent** | SPLIT-3 "one regime" (Lennart, 2026-10-12). kick CC (Lennart, 2026-10-01): the Kaggle split was neither temporal nor grouped, so the temporal split stays and models are deployed on known entities. corporate_credit_rating, USE-10 known entity. The Zindi siblings follow one pattern: with dates the split is temporal (digicow); without dates it follows the competition (expresso_churn_prediction_1m IID). |
| D2a | Window scheme: 6 equal-row windows at the end of Type_1 lending plus 3×30-day windows in 2024; 2022-12..2024-07 used for training only (issue 1) | SPLIT-12, 14, 15, 17, 20, 21 | **departs from SPLIT-15 with a stated reason** (about 100 rows a month are too few for 30-day windows, SPLIT-17); **departs from SPLIT-20 without a stated reason** (see D2b) | SPLIT-14 holds by construction (the first window starts on the first day by which half the rows are settled). SPLIT-17 holds (≥500 rows a window; coffee_rating_prediction). No precedent leaves a middle stretch untested. A refit horizon asserted rather than sourced has precedents: alfa_battle (2 months), lending_club and mortgage (a quarter). The shorter 30 days is set apart by 7-day loans. |
| D2b | Windows test two product eras across a 19-month sparse gap, and the alternatives offered are all two-era | SPLIT-20 (Should: "check the history for breaks … a change of rules or of the data collection") | **departs without a stated reason**. The splits comment names the product change but never weighs it as a break. | aeolus CC (Lennart, 2026-10-12): history from 2023 on. lending_club CC (Lennart, 2026-10-01): kept only 36-month loans up to 2015. sf_permit_time CC (Lennart, 2026-10-01/14): cut where labels are complete. In each, the curator cut to one coherent stretch. Here 28% of a long window's rows fall in products with no training row (alternative c), and the 2024 windows run on Type_7 while training is mostly Type_1. |
| D2c | Issue 1 lists linear/forest/LightGBM/CatBoost AUC per window scheme as "Numbers" | SPLIT-21 (Must) | **would break a Must** if it decided the scheme. As drafting, the evidence offered does not fit the rule. | aeolus, the case of SPLIT-21 (Lennart, 2026-10-12): "decide neither the training history nor the windows from a comparison over a few test windows". Spans, rows, defaults and product coverage are the admissible numbers. |
| D3 | Drop 8,899 rows with Amount_Funded_By_Lender < 0.5, all labelled 0 by construction (issue 2) | LEAK-25, LEAK-22, LEAK-36, SPLIT-9 check | **departs with a stated reason** (reasonable): the rows mix "no event" with "not recorded", and the field recovers the recording process. A weighing call remains. | LEAK-25: ghanas_indigenous_intel was retired because its recording process could not be recovered; here it can, so the remedy ladder puts dropping the rows ahead of retiring the dataset. digicow (same mechanism, not recoverable) is kept with a Data Quality note. LEAK-36/diabetes_130_us selected on a value known at prediction time; here the field is recorded at the pull, which sets this case apart and is why it is an issue. hotel_booking_demand (SPLIT-9 case): a filter on a post-outcome field must be checked to remove the shortcut rather than create one. The issue gives that check (0 of 8,899 labelled 1; charged-loan rates 1.04% against 0.40%). Two caveats. LEAK-22 says "follow the paper's cohort", and there is none; the competition kept the rows, and "the author's filter" (zero shares only) has no named source. The premise "a lender row's label follows that lender's repayment" is attributed to the host and is unverified (EV-5). |
| D4 | Labels count as settled 30 days after the due date; 802 rows dropped; training holds rows with due+30 < window start (issue 3) | SPLIT-9, SPLIT-10, LEAK-12, LEAK-24 | **consistent** | brazilian_ecommerce (1-month gap, Lennart, 2026-10-15). sf_permit_time (6-month gap, Lennart, 2026-10-01/14). lending_club (cut to completed labels, Lennart, 2026-10-01). lending_club trains on labels known only later, with a stated reason (a 36-month term). The fact that sets this case apart: terms of 7-365 days make the gap cheap. Lennart's SPLIT-10 decisions have not drifted: a gap of about the label's delay unless it would leave too little data. Caution: issue 3's AUCs (0.639 / 0.676 / 0.685) fall under SPLIT-21 like D2c. The default-rate-by-days-past-due table is the evidence that fits the rule. |
| D5 | `customer_id` kept as a categorical (issue 4a) | LEAK-34, USE-10, SPLIT-13, SPLIT-30, CLEAN-3 | **consistent**, now with a measured distinguishing fact against alfa_battle | ieee_fraud_detection `uid` (LEAK-34 case). Ghana's reporter history. aeolus flight number as a categorical (CC 2026-10-12). The `task_probes.md` "Hidden groups" text cites this dataset (69%) as a reading against the use case. The nearest credit sibling, alfa_battle_2_0_task_2 (panel 2026-10-20), removes repeat clients from training because the earlier default flag carried the later outcome (95.6%). I measured that mechanism on the shipped splits; result below the table. CLEAN-3 ("process it into that meaning") would allow history features in place of the raw id. That is optional and not a departure. |
| D6 | Keep the dataset despite no_spread and drift_baseline and near-chance 2024 windows; re-check with tuned results (issue 4b) | TP-1, TP-2, TP-3, TP-9 | **consistent** | TP-2 keeps: forest_fires, acquire_valued_shoppers (best AUC 0.654), hr_analytics (0.62-0.63, 2026-10-14), rosbank1 (2026-10-07). drift_baseline: mortgage (kept 2026-10-07). "Re-check with tuned results" with none in the cache: sf_permit_time (2026-10-12) and bias_correction (2026-10-15). TP-9 holds: 20-56 default rows a window. alvin_smart_money (Too Small, 2026-10-12) differs: rare classes of 2-8 rows from 5-12 users in a multiclass task. This is the third dataset held on the same "no tuned results yet" condition. That is a process gap (TP-1 cannot close), not a third exception: TP-2 makes keeping the default. |
| D7 | Amount_Funded_By_Lender, Lender_portion_Funded, other_lenders_on_loan kept as "Potential leak, kept on purpose" | LEAK-38 (Should), LEAK-10 | **consistent** | kick `WheelType` (Lennart, 2026-10-01; AUC 0.757→0.691). homesite. The case here is weaker than kick (0.639 against 0.635), so keeping is easier to justify. LEAK-38 covers "data a company released for its own competition". A Zindi release for an unnamed client lender fits approximately. The same field also drives D3's row filter. That is not inconsistent (LEAK-38 is about features), but the curator should see both together. |
| D8 | Total_Amount_to_Repay and Lender_portion_to_be_repaid dropped | LEAK-10 | **consistent** | heart_failure `time`, kickstarter `staff_pick` (LEAK-10 Mechanisms table). AUC 0.907→0.639. |
| D9 | ROC AUC rather than the competition's F1; 275 exact copies kept as separate loans | metric convention; LEAK-16..21 | **consistent** | aeolus (ROC AUC, CC 2026-10-12). digicow duplicates kept (different units of one session). |
| D10 | Licence raised as REVIEW issue 5 | EV-4 (Must: a licence "is a one-line note … none of them is an issue for the curator") | **departs from a Must (AI drafting); 4th instance, so an amendment is due** | numerai_v5_2_1m issue 1, corporate_credit_rating_cat_data_set_ratings_raitings issue 5, aeolus_1m issue 5 (its precedent check of 2026-10-20 already flagged this). digicow has the same licence ("Zindi Competition Rules") and the same kind of source (a participant's copy of Zindi files). It raised no issue, so two like cases were treated differently. The same goes for expresso_churn_prediction_1m and fraud_detection_..._1m. |
| D11 | Download from an unversioned Kaggle participant upload, byte sizes only | definitions.md pinning ("pin … where one exists") | **departs without a stated reason** (procedure, minor) | digicow pins a participant copy by GitHub commit (byte-identical git blobs). numerai_v5_2_1m and aeolus_1m record SHA-256 prefixes. |
| D12 | REVIEW block "Record fields that disagree with the definition" | writing.md | **stale**, a writing fix | The record now has `required_split: Temporal (NON-IID)` and the tag `Non-IID (Temporal)` (checklist). |

**D5 measurement** (script (panel run))

| Test rows by the customer's training side | Rows (all 9 windows) | Default rate, 2022 windows | Default rate, 2024 windows |
|---|---|---|---|
| The customer has a defaulted training loan | 5 of 13,890 | 3 of 4 | 0 of 1 |
| The customer was seen, with no defaulted training loan | | 0.5-1.2% | 4.7-6.7% |
| The customer is unseen | | 3.1-10.0% | 6.6-10.4% |

- The 3 of 4 is in window 4 alone.
- The signal is "a repeat customer with settled, repaid history". That is history a lender has at disbursement, not a carried label.
- What sets this case apart from alfa: the as-of settlement filter (due date + 30 days < window start), which alfa's data could not support.
- This can go into the `customer_id` bullet as evidence.

**Reflection prompts (one per departure without a reason)**

**Consistency check (AI, 2026-10-20):** the window scheme (issue 1) tests two product eras (Type_1 2022 and Type_7 2024) across a 19-month sparse gap. That departs from SPLIT-20 ("check the history for breaks"). aeolus (history from 2023, Lennart, 2026-10-12), lending_club (36-month loans up to 2015, Lennart, 2026-10-01) and sf_permit_time (cut where labels are complete) were each cut to one coherent stretch. What sets this case apart?
(a) The 2024 era alone has too few rows (≈1,770 test rows, 3 windows) to stand as a task, and the 2022 era alone would drop the newest data. Two eras in one task then serve P3 (the lender scores both products), recorded as an exception to SPLIT-20.
(b) Treat it like aeolus and lending_club: offer the 2022 Type_1 era only (54k rows) as a further alternative in issue 1.
(c) Reopen aeolus and lending_club to match.
(d) Amend SPLIT-20 to allow tasks that span a product change when the windows sit on both sides of it.

**Consistency check (AI, 2026-10-20):** issues 1 and 3 give model AUCs per window scheme and per label-settlement rule (0.649-0.708; 0.639 / 0.676 / 0.685) as their numbers. SPLIT-21 (Must; aeolus, Lennart, 2026-10-12) bars deciding the windows or the training history from such comparisons. What sets this case apart?
(a) Nothing. The scores are shown only as context, and the decision rests on spans, rows, defaults, product coverage and the default-rate-by-days-past-due table. Move the scores out of "Numbers", or mark them "not a decision reason".
(b) Treat it like aeolus: remove the scores from issues 1 and 3.
(c) Reopen aeolus to allow scores.
(d) Amend SPLIT-21.

**Consistency check (AI, 2026-10-20):** issue 5 raises the licence as a curator issue. EV-4 (Must) makes a licence a one-line note and never an issue, and digicow, under the same "Zindi Competition Rules" with a participant's copy, raised none. It is the 4th such issue (numerai_v5_2_1m 1, corporate_credit_rating 5, aeolus_1m 5). What sets this case apart?
(a) The Zindi rules call the data "private property of the client" and ask participants to report unauthorised transmission. That is a stronger redistribution bar than digicow's, worth a release-time question but not a dataset issue: keep it as the licence bullet and a release-checklist item.
(b) Treat it like digicow: a note only.
(c) Reopen digicow (and expresso_churn_prediction_1m, fraud_detection_..._1m) to add the same release question.
(d) Amend EV-4 to allow one "release note" issue per dataset that is never a verdict reason. Four instances now show that is what the working copy does.

**Consistency check (AI, 2026-10-20):** the download is an unversioned Kaggle participant upload identified only by byte sizes. digicow pins its participant copy to a GitHub commit, and numerai_v5_2_1m and aeolus_1m record SHA-256 prefixes. What sets this case apart?
(a) No pinned copy exists. If so, add SHA-256 prefixes of the four files to `download_description`, as numerai did.
(b) Treat it like digicow: find a pinned copy (a top solution's repository) and download from it.
(c) No change to the others.
(d) Amend definitions.md to require hashes when no version exists.


</details>

<details><summary>Checklist</summary>

**Checklist: african_credit_scoring_challenge (2026-10-20, panel prep)**

Re-check of the existing folder; no curation decision changed. Evidence: `dataset check` (README regenerated: only the
generator's template lines `time_gap: null`, `time_gap_unit: null` and the REVIEW.md row of the files table were added;
checksum `v2:8a4e8ac7...` unchanged), the probes under (panel run), and (panel run).

**Automated checks**

* `dataset list`: imports, `temporal_non_iid`, checked. `uvx ruff@0.15.15 check dataset.py`: clean.
* `dataset check`: 0 errors, 0 warnings, 2 info (`dataset_duplicate_rows` 275, `dataset_conflicting_duplicate_rows` 1),
  2 accepted (`dataset_pure_feature_value`, `splits_rows_unused`), both reasons still match the data.
* `sync-notebooks --check`: clean (v2_path matches).

**Probes (untuned, EV-8)**

* Leak probes (first 3 shipped splits = the three 2024 windows): all features AUC 0.598; depth-2/3 tree 0.502/0.500;
  best single feature customer_id 0.561, New_versus_Repeat 0.559; exact copies across the split 0.1% (0.0% with dates);
  1-NN agreement below chance (0.897 vs 0.961); NN distance alone 0.591. No leak flag.
* Task probes (5 of 9 splits): LightGBM AUC 0.609, skill +0.218 +- 0.155, beats dummy on 5/5; linear 0.595, RF 0.603;
  single feature 0.567 (loan_type 3x, customer_id 2x); smallest class per test fold 28. Flags: `no_spread` (TP-3),
  `drift_baseline` (TP-1, TP-2). Same flags as the 2026-10-07 decision (task_probes.md Cases: kept, re-check with tuned
  results). No tuned results in the cache (`tuned_results.py`: no hpo_results.parquet), so TP-1 cannot be closed.
* Hidden groups (temporal): customer_id seen on the training side for 69.2% of test rows; composite key and near copies
  0.0%. Decided by the use case (SPLIT-30): repeat customers' settled history is known at disbursement.
* Generated-data probes: no flags (84% of column pairs dependent, no rule leaves, no uniform columns).

**The checks, rank order**

| Rank | Check | Result | Evidence | Rule |
|---|---|---|---|---|
| P1 | Ethics | pass | Credit default scoring of anonymised customer ids; no objection stated by the host. Fairness of credit scoring is a field-wide caveat, not a stated objection. | SEL-1 |
| P2 | Scope | pass | Zindi competition to predict loan default (codebook: "1 means the customer defaulted on the loan"); a lending decision at disbursement. | SEL-2 to SEL-15 |
| P2, P5 | Real data | pass (circumstantial) | Generated probes: no marks; skewed real-world structure (54,163 of 58,953 rows in Jul-Nov 2022, 97.5% Type_1). Sampling of loans not stated by the source. | SEL-16, PROV-3 |
| P3 | Use case and fit | concern | fit `approximate` names the gap (share columns at the data pull, unknown sampling). But the 2024 windows are near chance (leak probe all-features 0.598 on them) and most signal is customer history (REVIEW issue 4); the 2022 windows cover one product's 6 weeks. | USE-1, USE-2, USE-8, USE-9 |
| P3, P4 | Target and metric | concern | Label is "as recorded at the data pull"; 30-day settlement rule drops 802 rows (84 labelled 1, verified). 2024 default rate by days past due (19.6% at 1-7 days vs 6.9-10.2% from 31 days) shows late labels; whether 30 days is enough is untested beyond that table. Codebook says the target is the customer's default, while the definition says a row's label follows the lender's repayment (cited as "host", not reachable without login): cannot verify the host statement. ROC AUC fits; competition scored F1. | USE-5, LEAK-22 to LEAK-26, EV-5 |
| P4 | Available at prediction time | concern | Repay amounts dropped (grow with days past due: decision table 1). Amount_Funded_By_Lender, Lender_portion_Funded, other_lenders_on_loan are kept although recorded at the data pull (curation comments, "Potential leak, kept on purpose"); the 0.639 vs 0.635 claim is untested here. Dropping rows on Amount_Funded_By_Lender < 0.5 selects rows on a field recorded at the pull (REVIEW issue 2). Training sides hold only rows settled before the window (code: `settled < start`). | USE-3, LEAK-1, LEAK-10 to LEAK-12, SPLIT-9, SPLIT-10 |
| P4 | Irreversible and all-row leakage | pass | `other_lenders_on_loan` counts rows per loan over Train.csv and Test.csv (label-free, by loan id); no label-aware or fitted feature. | LEAK-13 to LEAK-15, LEAK-27 to LEAK-31 |
| P4 | Copies across the split | pass | 275 extra exact copies (verified), kept as separate loans with their own tbl_loan_id; exact copies across split 0.1% (leak probe 5). Repeat customers decided as legitimate history. | LEAK-16 to LEAK-21, SPLIT-29 |
| P4 | Split regime | concern | Temporal on disbursement_date with a 30-day settlement gap; 9 windows (6 in 5-10 days of Oct-Dec 2022, 3 x 30 days in 2024). 1,901 rows of 2022-12-02 to 2024-07-10 are training only (verified). The window scheme is REVIEW issue 1 and open. | SPLIT-1 to SPLIT-31 |
| P5 | Source | concern | Trail ends at the Zindi competition, but the files come from a participant's Kaggle upload; byte sizes match the Zindi listing (verified locally: 8,785,708 / 2,379,732 / 7,930 / 1,539). Original lender not named. | PROV-1, PROV-2, PROV-8 to PROV-12 |
| P5 | Uniqueness | cannot verify | Not compared against other records in this pass (precedent checker / claim auditor). | PROV-4 to PROV-7 |
| P5 | Damage and repair | pass | No damage found; Train.csv country_id Kenya in all 68,654 rows; Test.csv has 3,525 Ghana rows (unused). | PROV-13 to PROV-15 |
| P6 | Worth benchmarking | concern | `no_spread` and `drift_baseline` flagged again; smallest class per fold 28 (20-56 default rows per window). Prior decision kept it pending tuned results (task_probes.md cases, TP-1 to TP-3); no tuned results exist yet. | TP-1 to TP-10 |
| P7 | Dtypes and cleaning | pass | ID (= "ID_"+customer_id+tbl_loan_id+lender_id, 100%), tbl_loan_id (Spearman 0.99987 with date), country_id dropped; duration = due - disbursement in 100% of rows; customer_id, lender_id, loan_type, New_versus_Repeat categorical; dates datetime. | CLEAN-1 to CLEAN-24 |
| procedure | Notes match the code | concern (minor) | All counts verified (58,953; 54,163; 8,899/8,520; 802; 133 of 2,134; 275; 1,901; 9 non-Type_7 rows in 2024). "Anomaly ... (0.98% defaults)": 0.98% is the Type_1 rate; all Jul-Nov 2022 rows default at 1.16%. Lender_portion_to_be_repaid = TAR x share within 1 unit in 98.9% of rows ("rounded" is approximate). REVIEW_before's "Record fields that disagree" block is stale: the record now has `required_split: Temporal (NON-IID)` and tag `Non-IID (Temporal)`. | writing.md |
| procedure | Licence and citation | pass (note) | License "Zindi Competition Rules"; rules call the data the client's private property; Kaggle copy a participant's upload (REVIEW issue 5, EV-4: never a verdict reason). Citation names the competition. | EV-4, PROV-10 |
| procedure | Reproducibility | concern | Kaggle download pinned to kaggle==2.2.2 but the dataset is an unversioned participant upload; Zindi page needs login. | |

</details>

<details><summary>Advocate</summary>

**Advocate: african_credit**

The definition is `african_credit_scoring_challenge` dataset.py.

**1. The task is real, and the split is the one the application implies (P3 and P4)**

- **Claim:** a lender scores a loan when it is paid out and refits monthly on the loans whose outcome it knows. That is what the definition builds.
- **Evidence:**
  - Every panel agent accepts the use case. The practitioner calls the fit "approximate", the same as `fit`. The blind reviewer calls it "a real, application-time loan-default task".
  - Claim audit: in all 9 windows every training row settles before its window starts. The latest training settle date is the window start minus 1 day. Spans are 5-30 days and no windows overlap.
  - Split audit: shipped temporal split 0.631 AUC, IID 5-fold 0.853. The random split overrates the task by about 0.22 because it rewards "the customer's last loan".
  - Precedents D1 and D4 are consistent: kick (temporal, replacing the Kaggle split), brazilian_ecommerce and sf_permit_time (label gap), lending_club (cut to completed labels).
- **Rules:** USE-10 (Must), SPLIT-9, SPLIT-10 (Should), SPLIT-5, LEAK-24 (Must).
- **Why it outranks the objections:**
  - The blind reviewer offers "a random/grouped split if the time axis cannot carry 9 folds". That would break a P4 Must for a P6 convenience, and the tension row "the right split against the score" settles it for the split.
  - The practitioner says the 30-day rule hides the last loan's outcome. That makes the task harder, not leakier. The rule exists because late payers do pay later: 19.6% of 2024 rows 1-7 days past due are labelled 1, against 6.9-10.2% from 31 days on (decision table 3).
  - Mildest remedy: one sentence in `fit_reason` saying history is "known only through settled labels on the training side".

**2. Three leaks were removed with the mildest remedy that works (P4, remedy ladder)**

- **Evidence:**
  - **Repay amounts.** The defaulted median charge grows from 4.6% to 33.9% with days past due, while repaid loans stay flat at 3.5%. AUC is 0.901 with these columns and 0.639 without (claim audit 10, 74).
  - **Unsettled labels.** 802 rows (84 labelled 1) are dropped.
  - **Zero-share rows.**
    - 0 of 8,899 are labelled 1, where about 105 would be expected at the period rate.
    - For the same customers and months, 1.04% of these rows carry a default-size charge against 0.40% of their other loans. Such a charge means label 1 in 89% of cases.
    - So about 90-130 defaults sit under label 0.
  - The count reconciles: Train.csv has 68,654 Kenya rows, minus 8,899 and 802, gives 58,953. That answers the blind reviewer's "~68.6k, filter undocumented".
- **Rules:** LEAK-10 (Must), LEAK-24 (Must), LEAK-25 (Must: "retire unless the recording process can be recovered").
- **Why it outranks the objections:**
  - LEAK-25 would retire the dataset if the recording process were lost. Here it is recovered: the field identifies the rows. So the ladder puts "fix the definition" (filter) ahead of exclusion. The ghanas precedent differs on exactly that fact (precedents D3).
  - The objection is REVIEW issue 2: the filter selects test rows on a field recorded at the pull.
    - The alternative, keeping the rows, ships about 90-130 known-false labels. That is a USE-5 / P3 target error, which is worse than a selection.
    - Kept rows with tiny amounts (0.5-10) default at 0.6-1.3%, like Type_1 overall at 1.0%. So the threshold does not leave the mechanism behind (column audit).
  - I concede this remains a weighing call for the curator, and that the LEAK-22 "paper's cohort" has no source to follow here.

**3. `customer_id` is legitimate history, not a carried label (P4)**

- **Evidence:**
  - Precedents D5 measured the pathway that leaked in alfa_battle. Only 5 of 13,890 test rows belong to a customer with a defaulted training loan.
  - The signal is "a repeat customer with settled, repaid history". Seen customers without a default run 0.5-1.2% in 2022 against 3.1-10.0% for unseen ones.
  - The as-of settlement filter is the fact that sets this case apart from alfa.
  - Column audit: `New_versus_Repeat` is never "New" after a customer's first date, and never "Repeat" on it (0 of 58,953).
- **Rules:** LEAK-34 (Must; narrows LEAK-10), USE-10 (Must), SPLIT-30 (a hidden-group hit is a question, decided by the use case). Precedent: ieee_fraud_detection `uid`.
- **Why it outranks the objections:**
  - The blind reviewer's "drop customer_id" rests on a numeric encoding ("ID encodes onboarding time"). The definition ships it as a categorical, so that mechanism does not apply.
  - Dropping it would turn a known-entity task into cold start, which is a different use case than the one USE-10 prescribes.
  - "Signal is mostly history" is what a lender's scorecard looks like (practitioner: 80% default after a defaulted loan, 1.1% after a repaid one). It is not a leak.

**4. The signal is small but real, and every window can be scored (P6)**

- **Evidence:**
  - Task probes: LightGBM skill +0.218 ± 0.155, beats the dummy on 5 of 5 splits. Linear 0.595 and RF 0.603 are both above chance.
  - The smallest class per fold has 28 rows, and each window has 20-56 default rows.
  - Leak probes find no leak: depth-2/3 trees score 0.50, and 1-NN agreement is below chance.
  - Precedents D6: acquire_valued_shoppers (best AUC 0.654) and hr_analytics (0.62-0.63) were kept as real tasks with a low ceiling. rosbank1 and mortgage were kept under the same flags.
- **Rules:**
  - TP-2 (Should): "a small but real signal is no reason to retire".
  - TP-9 (Must) holds.
  - Tension row "P4 over P6" (forest_fires): the split follows the application, and a small signal under it is no reason to retire.
- **Why it outranks the objections:**
  - The near-chance 2024 windows (0.488-0.637) are a real product launch with 12-44% seen customers, not a broken fold.
  - TP-1 cannot close without tuned results, but that is a process gap (precedents D6, the third dataset held on it). It is not a concrete reason found in the task, which TP-2 requires for retiring.

**5. The window scheme is reasoned. Two writing gaps and one edge risk are conceded, each with a mild fix (P4)**

- **Evidence:**
  - Windows are at most 30 days (SPLIT-12).
  - Window 8 trains on 50.6% of rows, which meets SPLIT-14. Every window has at least 500 rows (SPLIT-17).
  - The 1,901 rows from 2022-12 to 2024-07, about 100 a month, are too few for 30-day windows. That is the stated reason for departing from SPLIT-15.
  - The rejected alternative (c) has a 573-day window with 28.4% of rows in unseen products (claim audit 57).
  - The 2022 test weeks default at 0.48-1.35%, inside the Sep-Oct range of 0.57-1.71%. They are not an atypical stretch (split audit).
  - The code picks windows from settlement and the end of Type_1 lending, not from scores.
- **Concessions and fixes:**
  - **(a) SPLIT-20 (Should).** The product break is named but never weighed. Fix: record an exception. The 2024 era alone is about 1,770 test rows in 3 windows, and the 2022 era alone drops the newest data. This is option (a) of the precedent checker's prompt and serves P3.
  - **(b) SPLIT-21 (Must).** REVIEW issues 1 and 3 list model AUCs as "Numbers". Fix: move them out of "Numbers" or mark them "not a decision reason". The decision rests on spans, rows, defaults and product coverage, so the scheme itself does not change.
  - **(c) Newest edge.** 2024 Type_7 rows 30-37 days past due default at 14.1% (31 of 220) against 7.4% pooled at 31-120 days. The split auditor calls this evidence moderate: weekly rates swing from 1/142 to 20/183.
    - Mildest fix: state the edge in the splits comment and keep 30 days.
    - Raising `LABEL_SETTLED_DAYS` to 45 is the curator's option. Its case must rest on the default-rate table, not on window 0's AUC moving from 0.637 to 0.673, because SPLIT-21 forbids that.
- **Why it outranks the critic's likely remedy:** "Restrict to the 2022 era" (blind reviewer, precedent option b) is one rung up the ladder from a documented exception. A Should departure with a stated fact is kept with a note.

**6. Keeping the share columns follows LEAK-38. The note's wording is wrong and is fixed by a sentence (P4, Should)**

- **Concession:**
  - "Show no link to the outcome" is refuted for `other_lenders_on_loan`: 7.2% against 1.05% in Jul-Nov 2022 (claim audit 16).
  - The column is built by us from the pull-time row set, so the kick precedent fits it less closely.
- **Evidence for keeping:**
  - Within a product there is no link. Type_1 AUC is 0.46 for `Amount_Funded_By_Lender` and 0.49 for `Lender_portion_Funded`.
  - Two-lender rows default the same or less within Type_4, Type_5 and Type_10 (column audit). The marginal gap is product mix: Type_7 is 99.6% two-lender.
  - The two rows of a loan share date, customer and amount in 100% of loans, which fits co-funding set at disbursement.
  - The columns do not inflate scores. Dropping `other_lenders_on_loan` raises mean AUC from 0.640 to 0.664 on every seed. That is the opposite of a leak's signature.
- **Rules:** LEAK-38 (Should; narrows LEAK-10). Precedent: kick, whose effect was stronger (0.757 to 0.691) and which was still kept.
- **Fix:** rewrite `fit_reason` and the CC bullet as "no link within a loan product", with the numbers above. Whether to drop `other_lenders_on_loan` is the curator's weighing call, and either way costs nothing in validity.

**7. The remaining findings are wording and procedure, and none changes the data (P7 and writing; EV-4)**

These are each fixed by an edit:

- `row`: "2022 to 2024" becomes "October 2021 to October 2024" (39 rows are from 2021).
- CC anomaly: 0.98% is the Type_1 7-day rate; all Jul-Nov rows default at 1.16%.
- `predicted`: the label behaves as the loan's default (2 of 2,132 two-row loans disagree). Say "the loan's default, recorded per lender row" and keep the zero-share reasoning on the 0-of-8,899 fact.
- The linear 0.649 needs its encoding stated (0.705 with one-hot `customer_id`).
- Add SHA-256 prefixes to `download_description`, as numerai and aeolus do.
- Remove the stale "Record fields that disagree" block.
- One impossible share of 1.168: set it to missing or leave it (CLEAN-11, negligible).
- Licence issue 5 becomes a one-line note. EV-4 (Must) makes a licence never an issue, and digicow, under the same Zindi rules, raised none.

On the blind reviewer's raw dates: `disbursement_date` is the time index and a legitimate feature (CLEAN-23 holds). How a model extrapolates it is the model's problem, not the dataset's.

**Judgment record (advocate's view)**
- Verdict: ship after the writing changes above; no change to the data or the split.
- Validity:
  - USE-10 and USE-8 hold (approximate).
  - LEAK-10, LEAK-24 and LEAK-25 were triggered and fixed in the definition.
  - LEAK-34 holds.
  - LEAK-38 is kept with a corrected note.
  - SPLIT-10 holds. SPLIT-20 gets an exception. SPLIT-21 is met once the scores leave "Numbers".
- Value: TP-2 keep, TP-9 holds, TP-1 open until tuned results exist.
- Quality: CLEAN-11 is one row.
- For the curator, two weighing calls: issue 2 (the filter) and whether to drop `other_lenders_on_loan`.

</details>

<details><summary>Critic</summary>

**Critic: african_credit_scoring_challenge (opening brief, 2026-10-20)**

**Position: ship only after changes.** The task is real (temporal, at disbursement, repay amounts gone, settled-label
gap in place). None of my points asks for exclusion. Two validity points need a change to the definition, one a true
statement of the target, one a stated exception, the rest are notes and writing.

**1. The newest test labels are not yet settled at 30 days (P4; LEAK-24 Must, SPLIT-9 Must via SPLIT-10)**

- Problem: window 0 (2024-09-09 to 10-08) tests rows 30-43 days past due at the pull (min 30, median 43). Their
  labels still include late payers who will pay.
- Effect: the newest window scores models against labels that will flip from 1 to 0; it is the window that most
  resembles "now".
- Evidence (split_audit.md, problem 1): Type_7 2024 rows 30-37 days past due default at 14.1% (31/220) against
  1.8-11.3% in every later bucket (pooled 31-120 days 7.4%); the last two disbursement days 13/66 = 20% against 2/50 a
  week earlier. Same shape as decision table 3 (19.6% at 1-7 days), just past the cut. Evidence moderate (weekly rates
  noisy). The window's AUC shift (0.637 to 0.673) is not my reason (SPLIT-21).
- Remedy: fix the definition, `LABEL_SETTLED_DAYS = 45` (drops about 390 newest rows; the gap of every training side
  moves with it). If the curator keeps 30, state the edge and these rates in the splits comment.

**2. `other_lenders_on_loan` is a pull-time value we built ourselves, and the "no link" note is false (P4; LEAK-10 Must, LEAK-5 Must; LEAK-38 does not cover it)**

- Problem: the note says the share/count columns "show no link to the outcome". Refuted: rows with another lender
  default at 7.2% against 1.05% in the same months (Jul-Nov 2022), 6.9% vs 1.0% on the 2022 test rows, single-feature
  AUC 0.67 / 0.63 in windows 3 / 4 (claim_audit.md, claim 16/45). Lenders can buy each other out (host), and the
  column counts the loan's rows as of the pull, so a buy-out after default would show here; it cannot be dated.
- Rule: LEAK-10 puts out "attributes looked up after the outcome, unless the data shows they did not change"; the data
  cannot show that. LEAK-38 keeps *anonymised host fields* in a company's competition data; this column is our own
  construction from the pull-time row set across both files, so the kick precedent fits it poorly (claim audit,
  precedents D7). The ablation (0.639 vs 0.635) is not an argument that it is no leak (LEAK-5).
- Effect on the task: dropping it costs nothing; mean AUC rises 0.640 to 0.664, on every seed (claim audit).
- Remedy: drop `other_lenders_on_loan` from the definition (keep `Amount_Funded_By_Lender` and `Lender_portion_Funded`
  under LEAK-38, which shows no link within a product: Type_1 AUC 0.46 / 0.49, column_audit.md). Rewrite the
  `Potential leak` bullet and `fit_reason` to "no link within a loan product", with these numbers.

**3. The target is described as a per-lender outcome; the data says it is the loan's default (P3; USE-5 Must, USE-8 Must, EV-2)**

- Problem: `predicted` says "whether that lender's part of the loan defaulted"; CC6 attributes per-lender labels to
  the host (unverified). The two rows of a two-lender loan share the label in 2,132 of 2,134 loans; the codebook says
  "1 means the customer defaulted on the loan".
- Effect: the curator and users read the wrong target; the zero-share drop rests on that premise.
- Remedy (a note): reword `predicted` to "the loan's default, recorded on each lender row"; ground the zero-share drop
  on the measured facts (0 of 8,899 labelled 1, about 105 expected; charged rows 1.04% vs 0.40%) instead of the host
  claim. The drop itself stays.

**4. Two product eras across a 19-month gap, without a stated reason (P4; SPLIT-20 Should)**

- Problem: six windows test Type_1 7-day loans of late 2022; three test Type_7 loans of 2024 with 98-688 Type_7
  training rows and 12-44% of test rows from seen customers. The 2024 windows are near chance (LightGBM 0.488-0.637).
  SPLIT-20 asks to check the history for breaks (a change of product is one); the splits comment names the change but
  does not weigh it (precedents D2b; aeolus, lending_club, sf_permit_time each cut to one stretch).
- Effect: one mean over two different tasks, a repeat-customer ranking and a product cold start.
- Remedy: record the exception with its reason (the 2024 era alone is too small to stand, P3: the lender scores both),
  and name the 2024 windows as a new-product test in the splits comment; offer "2022 Type_1 only" as an alternative in
  REVIEW issue 1. Not a reason to exclude.

**5. REVIEW issues 1 and 3 offer model scores as the deciding numbers (SPLIT-21 Must)**

- Problem: the "Numbers" for the window scheme and the settlement rule are mean AUCs per scheme (0.649-0.708; 0.639 /
  0.676 / 0.685). SPLIT-21 bars deciding windows or training history from such comparisons (aeolus).
- Remedy: mark them "context, not a decision reason" or remove them; lead with spans, rows, defaults, product
  coverage and the default rate by days past due.

**6. Fit statement misses the lagged history (P3; USE-8 Must, note)**

- Problem: 36% of rows have an earlier loan already due at disbursement, only 2.2% one due 30+ days before; after a
  defaulted loan 80% of rows default, after a repaid one 1.1% (practitioner.md). A lender knows a repayment the day it
  happens; the settlement gap hides it. Correct for the label (SPLIT-10), but it is a gap of the fit.
- Remedy: one sentence in `fit_reason`: the customer's history is known only through labels settled before the window.
  I do not ask for a shorter gap for repaid loans: admitting recent repaid loans but not recent defaults selects
  training rows on the outcome.

**7. Quality and procedure (P7 and house rules; no verdict weight)**

- `row` says "2022 to 2024": 39 kept rows are from Oct-Dec 2021 (claim 3). Say "October 2021 to October 2024".
- CC14 "(0.98% defaults)" is the Type_1 7-day rate; all Jul-Nov rows are 1.16% (claim 4).
- One impossible row: `Lender_portion_Funded` 1.168, funded 2,627.1 > Total_Amount 2,249 (CLEAN-11 Should): set both
  to missing.
- "linear 0.649" not reproduced (0.705 with one-hot customer_id, EV-8): state the encoding or drop the number.
- Download is an unversioned participant upload pinned only by byte sizes: add SHA-256 prefixes (definitions.md
  pinning; numerai_v5_2_1m, aeolus_1m).
- Licence raised as issue 5 departs from EV-4 (Must: a one-line note, never an issue; digicow, same licence, raised
  none): move it to a release note.
- REVIEW's "Record fields that disagree" block is stale (record now `Temporal (NON-IID)`).

</details>

<details><summary>Advocate rebuttal</summary>

**Advocate rebuttal: african_credit**

**New facts.** I ran two short scripts on the raw Train.csv and Test.csv, applying the definition's filters. Both are in (panel run):
- Type_7 default rate by disbursement week in 2024.
- Default rate by loan type and `other_lenders_on_loan` in Jul-Nov 2022.

**Critic 1: `LABEL_SETTLED_DAYS = 45`. Disputed; I keep 30 days and add a note.**

**The facts.** Kept Type_7 rows of 2024 by disbursement week. "Days past due" is counted at the pull, 2024-11-14.

| Days past due | Rows | Defaults | Rate |
|---|---|---|---|
| 32-38 | 183 | 20 | 10.9% |
| 39-45 | 142 | 1 | 0.7% |
| 46-52 | 158 | 6 | 3.8% |
| 53-59 | 126 | 11 | 8.7% |
| 60-73 (2 weeks) | | | 10.8-11.9% |
| 74-129 (8 weeks) | | | 4.8-11.8% |

- If labels were still settling after 30 days, the rate would fall steadily with days past due, as it does before 30 days in decision table 3 (19.6% falling to 11.6%).
- It does not. The two weeks just past the cut (39-52 days) are the lowest of the year. The bucket of 30-44 days pools to about 8.7%, against 7.4% for 31-120 days.
- Week-to-week swings of ±5 percentage points occur at every age. The split auditor's 14.1% for 30-37 days and 20% for the last two days are inside that noise. The split auditor itself rated this evidence "moderate".

**The rules.**
- LEAK-24 (Must) asks to cut where follow-up is complete. SPLIT-9 (Must) and SPLIT-10 (Should) ask for a gap of about the label's delay.
- The measurement (EV-2, rank 1) puts the end of the delay at about 30 days, not 45. So the Musts are met.
- SPLIT-21 also applies: moving the cut on the strength of one window's elevated week would choose the training history from a few test windows. The critic rightly sets aside the window-0 AUC change; the 14.1% bucket is the same kind of evidence.

**What follows.** The mildest remedy on the ladder is the critic's own fallback: keep 30 days, and state the newest edge and the week table in the splits comment. If the curator prefers 45 days, it costs about 390 rows and no validity, so it is a weighing call and not a Must fix.

**Critic 2: drop `other_lenders_on_loan`. Conceded, with a correction to my own brief.**

**The new measurement.** Jul-Nov 2022, kept rows, default rate with one co-lender against none, within a product:

| Product | No co-lender | One co-lender |
|---|---|---|
| Type_4 | 11.9% (n 67) | 15.2% (n 165) |
| Type_5 | 2.1% (n 145) | 5.4% (n 481) |
| Type_6 | 1.4% (n 70) | 8.8% (n 204) |

- Type_1, which makes up the 2022 test windows, never has a co-lender, so it cannot show the link either way.
- The column audit reported the opposite direction. It used the whole frame, which mixes eras.

**What I withdraw.**
- My point 6 said "no link within a loan product". That holds for the two share columns (Type_1 AUC 0.46 and 0.49). It does not hold for the count.

**What still stands, and why it does not change the outcome.**
- The host's buy-out mechanism predicts the opposite sign: a buy-out removes a co-lender, so it should not raise defaults among two-lender rows. The column may well have been set at disbursement.
- But that is inference (EV-2, rank 5) and cannot be dated. LEAK-10 (Must) keeps "attributes looked up after the outcome" only "where the data shows they did not change", and the data cannot show it.
- LEAK-38 (Should) covers the host's anonymised fields. This column is our own construction, so it cannot override a Must.
- Dropping it costs nothing: mean AUC goes from 0.640 to 0.664, higher on every seed (claim audit).

**Where I differ on the rule.** The critic cites LEAK-5. That rule is about stored values depending on the test rows. The count is label-free and per loan, and both rows of a loan share a date, so LEAK-5 does not apply. LEAK-10 decides this point alone.

**What follows.**
- Remove `other_lenders_on_loan` from `_labelled_rows`. Test.csv is then no longer read: delete the line in `_load_raw` and the CC3 bullet.
- Keep `Amount_Funded_By_Lender` and `Lender_portion_Funded` under LEAK-38, with the note rewritten as "no link within a loan product (Type_1 AUC 0.46 / 0.49)". Correct `fit_reason` to match.

**Critic 3: target wording. Conceded.**

- `predicted` should read "the loan's default, recorded on each lender row". The evidence is that 2,132 of 2,134 two-row loans share their label, and the codebook says the customer defaulted on the loan (USE-5, EV-2).
- Ground the zero-share drop on the measured facts: 0 of 8,899 rows labelled 1 where about 105 were expected, and charged rows at 1.04% against 0.40%. Drop the unverified host claim.
- The drop itself stays. The critic agrees, and the curator still has REVIEW issue 2.

**Critic 4: two product eras. Conceded; this matches my point 5(a).**

- Record an exception to SPLIT-20. The reason: the 2024 era alone is about 1,770 test rows in 3 windows, and the lender scores both products (P3).
- Name the 2024 windows as a new-product test in the splits comment.
- Offer "2022 Type_1 only" as an alternative in issue 1, as an option and not a recommendation.

**Critic 5: scores used as deciding numbers. Conceded (SPLIT-21, Must).**

- Mark the AUCs in issues 1 and 3 as "context, not a decision reason".
- Lead with spans, rows, defaults, product coverage and the default rate by days past due.

**Critic 6: the fit statement misses the lagged history. Conceded (USE-8).**

- Add one sentence to `fit_reason` saying the history is known only through labels settled before each window.
- I agree with the critic against a shorter gap for repaid loans only. Admitting recent repaid loans but not recent defaults would select training rows on the outcome (SPLIT-9).

**Critic 7: quality and procedure. Conceded; these match my point 7.**

- Fix "October 2021"; correct 1.16%; set the one impossible share row to missing (CLEAN-11); state the encoding behind the linear AUC or drop the number; add SHA-256 prefixes to the download.
- Licence issue 5 becomes a one-line note (EV-4, Must).
- Remove the stale record-fields block.

**Where the two sides now stand**

**Agreed:**
- Ship after changes.
- The definition changes in one way: drop `other_lenders_on_loan`, which stops the definition reading Test.csv.
- One row's share is set to missing.
- The rest is notes, the SPLIT-20 exception, and SPLIT-21 and EV-4 fixes to the review file.

**Still open:**
- Critic 1: 30 or 45 days. My side: the weekly table, with no decay after 30 days. The critic's side: the 30-37-day bucket.
- Issue 2: the zero-share filter. This is a weighing call for the curator.

</details>

<details><summary>Critic rebuttal</summary>

**Critic: rebuttal to the advocate (2026-10-20)**

**Conceded**

- **A1, real task and temporal split.** Agreed. Adding the history sentence to `fit_reason` settles my point 6.
- **A2, three leaks removed.** Agreed, including the zero-share filter as the curator's weighing call (issue 2). The
  advocate's row count (68,654 - 8,899 - 802 = 58,953) answers the blind reviewer.
- **A3, `customer_id`.** Agreed: it is entity history (LEAK-34, USE-10). The as-of filter is what sets it apart from
  alfa.
- **A4, value.** Agreed (TP-2, TP-9). I never asked for retirement.
- **A5a/b, the SPLIT-20 exception and taking the scores out of "Numbers" (SPLIT-21).** These are my points 4 and 5,
  with the same remedy.
- **A6, the share columns and `other_lenders_on_loan`.** Conceded, because of a new fact I checked on
  (panel run). Type_1 rows never have another lender (52,826 rows, all 0). In every product that has
  both kinds of row, the two-lender rows default *less*: Type_7 7.4% vs 12.5% (n=8), Type_4 11.0% vs 15.5%, Type_5
  6.7% vs 9.7%, Type_10 2.2% vs 3.7%. So the 7.2% vs 1.05% link from the claim audit is product mix. A buy-out
  after default would push the other way. LEAK-10 is not shown to be broken, and the LEAK-38 note with "no link
  within a loan product" is enough. Dropping the column stays a free option for the curator, not a demand. I
  withdraw my point 2 as a required change. One caveat on the advocate's reasoning: "dropping it raises AUC" is no
  argument against a leak (LEAK-5). The fact above is.
- **A7, wording and procedure.** Agreed, item for item. These are my point 7.

**Disputed**

- **A5c, the newest edge: keep 30 days with a note.** This is a Must, not a Should. LEAK-24 (Must) says a target
  right-censored in the newest periods "is cut where follow-up is complete". By principles.md, a Must is fixed in the
  definition when it can be, and a note is the rung for a Should exception. The fix here is cheap: about 390 rows
  (0.7%) and one constant. The evidence is the default-rate table, not window 0's AUC (SPLIT-21):
  - 30-37 days past due: 14.1% (31/220);
  - every later bucket: 1.8-11.3% (pooled 31-120 days: 7.4%);
  - last two disbursement days: 13/66 against 2/50 a week before.

  This is the shape of decision table 3, just past the cut. I grant that the evidence is moderate (split audit). So
  the facts should come first (EV-1). Run the decisive check: the default rate by days past due at the pull in 5-day
  buckets from 25 to 60 days, Type_7 2024 rows, with binomial intervals.
  - If the 30-44-day rate is above the 45-120-day rate beyond noise, LEAK-24 requires 45.
  - If not, I concede, and 30 days stays with the edge stated in the splits comment.

**Net:** ship after changes. Left in dispute: `LABEL_SETTLED_DAYS`, which the check above settles. My point 3 (the
`predicted` wording, USE-5) matches the advocate's A7 item, so it is agreed.

</details>

<details><summary>Mediator</summary>

**Mediator: african_credit**

**Decisive experiments**
Run on the definition's kept rows ((panel run), 58,953 rows) and on the raw Train.csv, with thread caps of 4.

**1. `other_lenders_on_loan`: default rate by era, product and co-lender count (0 against 1)**

| Era | Type_4 | Type_5 | Type_6 | Type_10 |
|---|---|---|---|---|
| Oct 2021 - Jun 2022 | 19.7% vs 20.0% | 11.6% vs 4.9% | 38% vs 100% (n 3) | 8.0% vs 0.0% |
| Jul - 1 Dec 2022 | 11.9% vs 16.1% (p 0.54) | 2.1% vs 5.3% (p 0.12) | 1.4% vs 8.6% (p 0.05) | 0% vs 1.4% |
| Dec 2022 - 2023 | 11.1% vs 9.0% | 23% vs 10.3% | 33% vs 14% | 3.2% vs 3.2% |

- **Pooled over eras:** two-lender rows default less in every product (Type_4 15.5% vs 11.0%, Type_5 9.7% vs 6.7%). That is the critic's figure.
- **Within Jul-Nov 2022:** they default more. That is the advocate's figure.
- **Mantel-Haenszel odds ratio** over era × product strata: 0.96 overall; 0.60 / 2.26 / 0.67 by era. This is Simpson's paradox, not a consistent link either way.
- **Test windows:**
  - In the 2022 windows the column varies only on 424 non-Type_1 rows (Type_1 is always 0).
  - In the 2024 windows it is 1 on all 1,761 Type_7 rows, so it is constant there.
- **What the column measures:** 99.7% of rows with no co-lender have `Lender_portion_Funded` < 0.99 (median 0.30 for Type_1). The rest of these loans is funded by lenders who are not in the files. The count records which lender rows reached the release, not whether the loan was co-funded at disbursement.

**2. Settlement: Type_7 loans of 2024, counted per loan**
- Rows are doubled by two-lender loans; the two rows of a loan never disagree (0 of 1,600 loans). Days past due are counted at the pull, 2024-11-14.

| Days past due | 1-7 | 8-14 | 15-20 | 21-25 | 26-30 | 31-35 | 36-40 | 41-45 | 46-50 | 51-55 | 56-60 | 61-75 | 76-90 | 91-120 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Loans | 92 | 74 | 64 | 54 | 75 | 79 | 57 | 72 | 66 | 57 | 44 | 180 | 184 | 287 |
| Default rate | 19.6% | 14.9% | 6.2% | 11.1% | 17.3% | 15.2% | 5.3% | 0.0% | 1.5% | 12.3% | 2.3% | 11.1% | 7.1% | 7.7% |

- 31-45 days: 15/208 = 7.2%, against 46-120 days: 64/818 = 7.8% (Fisher p = 0.88). The critic's narrower bucket, 31-38 days: 11.5% against 7.2% (p = 0.10).
- Spearman correlation of default with days past due: −0.003 over 31-120 days (p = 0.93), and −0.055 even over 1-30 days (p = 0.30). So the "late payers pay later" decay is itself weak when counted per loan.

**Rulings on the disputed points**
1. **`other_lenders_on_loan`: drop it (LEAK-10, Must).**
   - It is not a conflict. LEAK-38 (Should, narrows LEAK-10) covers anonymised fields in host-released data. This count is built by the definition from the row set at the pull, across both files, so LEAK-38 does not reach it.
   - LEAK-10 keeps an attribute looked up after the outcome only "where the data shows it did not change". The data cannot show that, and the column does not mean what its name says.
   - The remedy ladder gives "fix the definition": drop it. "No link within a loan product" holds only for the two share columns, which stay under LEAK-38.
   - The model-score arguments on both sides do not count (LEAK-5).
2. **`LABEL_SETTLED_DAYS`: keep 30.**
   - LEAK-24 and SPLIT-9 (Must) and SPLIT-10 hold: the measurement shows no excess default past 30 days. The critic's 14.1% was a row count over one noisy week.
   - The critic set this test in the rebuttal and conceded in advance if it failed.
   - The window AUCs were not used (SPLIT-21).

**Changes to make now (no decision needed)**
1. Drop `other_lenders_on_loan` (LEAK-10): remove its construction from `_labelled_rows`, the CC bullet on Test.csv, and the mentions in `known` and `fit_reason`.
   - Correction to the advocate's plan: `_decisions` (table 2, "customer borrowed again") still reads `raw["test"]`. Keep the Test.csv load for that table, or rework the table; do not just delete the line in `_load_raw`.
2. Rewrite the "Potential leak" bullet and `fit_reason` for the two share columns as "no link within a loan product (Type_1 AUC 0.46 / 0.49)", and drop the 0.639/0.635 ablation as an argument (LEAK-38, LEAK-5).
3. Keep 30 days, and state the newest edge in the splits comment with the per-loan table above (LEAK-24, SPLIT-10).
   - Recount decision table 3 per loan, or note that rows double-count two-lender loans.
   - Describe the 30-day delay as a conservative cut, not a measured end of settlement (EV-2).
4. `fit_reason`: add one sentence saying the customer's history is known only through labels settled before each window (USE-8).
5. `predicted`: "the loan's default, recorded on each lender row" (USE-5). Ground the zero-share bullet on the measured facts (0 of 8,899 rows labelled 1, about 105 expected; charged rows 1.04% against 0.40%), not on the unverified host claim (EV-5).
6. `row`: "October 2021 to October 2024". Correct the anomaly rate to 1.16%. Set the impossible share row (1.168; funded 2,627.1 > total 2,249) to missing (CLEAN-11).
7. Writing fixes:
   - State the encoding behind linear 0.649, or drop the number (EV-8).
   - Add SHA-256 prefixes to `download_description` (pinning; numerai, aeolus).
   - Make the licence a one-line note, not an issue (EV-4, Must).
   - Remove the stale record-fields block.
   - Mark the model AUCs in issue 1 "context, not a decision reason" (SPLIT-21). Close issue 3 with the table above.
8. Splits comment: name the 2024 windows as a new-product test (Type_7, with 98-688 Type_7 training rows).

**Judgment record**
```text
Verdict: ship after changes.
Validity: SEL holds; USE-10 holds, USE-8 approximate (history-lag sentence added), USE-5 wording fixed; LEAK-10
triggered twice, fixed (repay amounts dropped; other_lenders_on_loan dropped); LEAK-24 holds at 30 days (measured:
7.2% vs 7.8%, p 0.88); LEAK-25 triggered, fixed by the zero-share filter (curator issue 1); LEAK-34 holds
(customer_id, settled history only); LEAK-38 note for the two share columns; SPLIT-9/10 hold; SPLIT-20 departure,
exception pending the curator (issue 2); SPLIT-21 met once the scores leave "Numbers".
Value: TP-2, a small real signal (keep); TP-9 holds (20-56 defaults per window); TP-1 open until tuned results.
Quality: CLEAN-11 one row to missing.
Weighed: real lender task +, size +, two product eras -, near-chance 2024 windows -.
For the curator: issue 1, the zero-share filter (validity, LEAK-25/SPLIT-9); issue 2, the two eras (SPLIT-20 exception).
```

**Issues for the curator (ranked)**
1. **The zero-share filter (P4; LEAK-25 Must, SPLIT-9, USE-5).** This is a weighing call between two harms.
   - **Problem:** 8,899 rows whose lender funds less than 0.5 are labelled 0 whatever the customer did. Dropping them selects the rows on a field recorded at the pull.
   - **Effect:** keeping them ships about 90-130 false labels. Dropping them removes 8-18% of the rows on the 2022 test-window dates.
   - **Best evidence for dropping:** 0 of 8,899 rows are labelled 1. Charged rows are 1.04% against 0.40%. The kept tiny-amount rows (0.5-10) default at 0.6-1.3%, like Type_1 overall.
   - **Best evidence against:** the filter field has no recording time, and no source cohort defines this filter (LEAK-22).
   - **Decision needed:** drop all rows below 0.5 (as now), only the zero-share rows, or keep the rows and drop both share columns.
   - **What would settle it:** the host's statement of when the shares are recorded.
2. **Two product eras in one task (P4; SPLIT-20 Should).**
   - **Problem:** six 2022 Type_1 windows and three 2024 Type_7 windows sit across a 19-month sparse stretch.
   - **Effect:** one mean over a repeat-customer ranking and a product cold start.
   - **For the exception:** the 2024 era alone is about 1,770 test rows in 3 windows, and the lender scores both products (P3).
   - **Against:** aeolus, lending_club and sf_permit_time were each cut to one coherent stretch.
   - **Decision needed:** record the exception, or ship "2022 Type_1 only". Decide on spans, rows and product coverage, not on scores (SPLIT-21).
   - The panel recommends the exception; both sides agree.

**Agreed facts**
- 58,953 kept rows = 68,654 Kenya rows − 8,899 low-share rows − 802 unsettled rows; 1,174 defaults (1.99%).
- The repay amounts grow with days past due: AUC 0.907 with them, 0.639 without. Dropped.
- The two rows of a loan share date, customer, amount and label in 2,132 of 2,134 loans.
- Every training row settles before its window starts. Spans are 5-30 days; 2024 windows have ≥ 500 test rows and the 2022 windows 1,812-2,206; window 8 trains on 50.6% of the rows.
- `customer_id`: 5 of 13,890 test rows belong to a customer with a defaulted training loan. The signal is settled repaid history.
- Type_1 never has a co-lender. Type_7 has one on 99.6% of its rows.
- The random split overrates the task by about 0.22 AUC (0.853 against 0.631).

**Consistency with precedent**
- **D4, settlement:** consistent (brazilian_ecommerce, sf_permit_time, lending_club).
- **D5, `customer_id`:** consistent with ieee `uid`. The settlement filter sets it apart from alfa_battle.
- **D7, the share columns:** follow kick under LEAK-38. For `other_lenders_on_loan`, my recommendation departs from kick. What sets it apart: we built the column, and it does not record co-funding (99.7% of single rows have a share below 1).
- **D2b, two eras:** departs from aeolus and lending_club. That is curator issue 2.
- **D10, licence:** treat it like digicow, a note only. This is the 4th such issue, so an EV-4 amendment is due.
- **D11, download pin:** treat it like numerai and aeolus (SHA-256 prefixes).


</details>
