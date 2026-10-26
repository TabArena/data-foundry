# alfa_battle_2_0_task_2

**Outcome:** added. Alfa-Bank's 963,811 issued credit products (AlfaBattle 2.0, task 2), target default, 508
aggregates of the client's card transactions of the year before plus the product type and the issue month, three
two-month test windows on the reconstructed issue month; the AI recommends shipping it. Validity: USE-1 and USE-5 hold
and the fit is approximate (USE-8: a reconstructed time axis, a default flag with no stated horizon); LEAK-1, LEAK-2
and LEAK-10 hold on measurement (every transaction is 1-359 days before the issue, the best single feature reaches ROC AUC 0.614
against 0.708 for all features (probe)); LEAK-24 is maybe triggered by a dip of the default rate in the newest two months (issue 4);
SPLIT-9 is triggered and fixed by the repeat-client filter (issue 1); SPLIT-14 holds (60-83% of the rows for training),
and SPLIT-10 is departed from for it (issue 3). Value: no task-probe flag, 3.6-3.8k defaults per test window. Quality:
CLEAN-5 triggered, four columns that copy another on every row are dropped; the hand-built transaction aggregates (CLEAN-19, 2026-10-13) and the codes chosen over
all rows (CLEAN-8, 2026-10-19) as Lennart decided.
Weighed: a transaction module the bank runs and a large sample +, the reconstructed time axis and the unknown label
horizon -. Left for Lennart: issues 4, 1 and 3, and one rule item at the end of the working copy's REVIEW.md.

**Main points:** Keep the newest months with a note on possible right-censoring (or drop month 23), ratify the
repeat-client filter against the ieee_fraud_detection precedent, and choose gap 0 (with a recorded exception to
SPLIT-10) or gap 1.

**Record judgment:** valid with concerns. The table aggregates event sequences as the competition's top solutions did;
the issue months are reconstructed from week codes; repeat clients are linked from shared transactions only; the
default flag has no stated horizon. The record has no curator line on shipping (its last CC is of 2026-10-13, its status `WIP (DF)`). That CC states 513
aggregates and LightGBM scores of an unnamed setup; the definition has 508, and LightGBM with default settings gives
ROC AUC 0.779 / 0.763 / 0.761 (AI Assessment of 2026-10-20). The CC is Lennart's to correct.

**Issues for Lennart:**

4. **Keep the newest months with a note on possible right-censoring, or drop month 23?** The target is the source's
   flag "the client defaulted on this product", with no horizon such as "within 12 months". If the bank extracted the
   labels on one date, the products issued shortly before it had less time to default, so some of their defaults are
   missing from the data (right-censoring). The newest test window (months 22-23) would then score the models against
   labels that are partly incomplete; the size of that effect is unknown.
   * Evidence: the default rate rises from 2.0-2.6% (months 1-12) to 3.4% (month 21), then falls to 3.1% and 3.0% in
     months 22-23. For products whose client had an earlier product the fall is 5.2% (month 20) to 4.0% (month 23),
     about 4.6 standard errors, and first products dip a little (2.85% to 2.6%). A product of month 23 cannot have a later
     product, so a grouping that also counts later products could make a dip by itself. Grouped by earlier products only
     (mediator), the dip stays.
   * The advocate reads it as a cluster of defaulting clients around months 20-21, after 20 months of rising rates;
     the critic answers that a client-level flag cut at the extraction date shows first in clients with several
     products. The data cannot separate the two (EV-6); labels from a later extraction would.
   * Implemented: the months stay, and the notes give the measured dip and both readings. Alternative: drop month 23 and shift the windows to 21-22,
     19-20 and 17-18; the oldest training side would keep about 55% of the rows after the filter (the mediator's
     estimate, not built). It costs the newest month and leaves month 22 just as uncertain.
   * Rule: LEAK-24 (Must), not shown violated without the later extraction (EV-1). Advocate and critic agree on the
     note.

   Recommendation: keep with the note. Decision: keep with the note, or drop month 23?

1. **Ratify the repeat-client filter, which departs from ieee_fraud_detection?** The data has no client id, but a
   client's products issued within a year share identical card transactions. We link two products when they share at
   least 3 identical transactions that make up 80% of the smaller product's transactions in the 28 days before an issue
   date, and call the linked products one client. When a client's earlier product defaulted, the later one defaults in
   95.1% of cases (2.3% otherwise), flat over lags of 1-10 months; of the later products that defaulted, only 45.5% had an earlier
   product that defaulted. That asymmetry fits
   a default of the client after both issues (a bank does not issue new credit to a client already in default), so the
   earlier product's flag was most likely not known when the later one was issued. Left in training, it tells a model
   which test-window clients will default.
   * Evidence (shipped features, equal training size): without the filter the window's ROC AUC rises by 0.002 (newest
     window) and 0.009 (oldest), that of the linked test products by 0.006 and 0.022. After the filter, 4 of about 3,640 test defaults in the newest window
     still have a linked defaulted training product.
   * Implemented (a): each training side loses the products of clients with a product in the test window (32,861-39,221
     rows; training keeps 60-83%). It stands in for an as-of filter on label dates, which the data does not have.
     Alternative (b): keep them, as ieee_fraud_detection kept the training labels of the same card holder's earlier
     transactions (Lennart, 2026-10-01: about 95% positive, worth under 0.01 AUC), with a `Potential leak, kept on purpose:` note; the shortcut above then stays in the
     scores. (c) Reopen ieee to match alfa (drop its training rows of card holders with a test
     transaction). (d) Amend SPLIT-9 or LEAK-34 to say when same-entity labels carried forward
     are history and when they are labels not yet known.
   * What sets alfa apart from ieee: it has no client feature, so this is a training-row question (SPLIT-9), not a
     feature question (LEAK-34); the 0.951 / 0.455 asymmetry; ieee has a one-month gap, alfa none.
   * Rule: SPLIT-9 (Must). The advocate and the critic both keep the filter; the precedent check flags the departure
     from ieee.

   Recommendation: (a), with the facts above recorded. Decision: (a), (b), (c) or (d)?

3. **Gap 0 with a recorded exception to SPLIT-10, or a one-month gap?** A gap is a stretch of months between the
   training side and the test window that neither uses, so that the training labels have time to mature. A default can
   be flagged months after the issue, so the training products of the months just before each window carry labels a
   model refit at the window start would not have had yet; every model's score is then somewhat optimistic. SPLIT-10
   (Should) asks for a gap of about the label delay.
   * Evidence: a 12-month gap leaves 13-27% of the rows for training and a 6-month gap 35-53%, both below the 50% floor
     (SPLIT-14, Must). At equal training size, gap 1 changes ROC AUC by +0.005 (standard error 0.003) on the newest window and
     +0.0004 on the oldest, and a
     6-month gap lowers it by 0.014-0.015, an upper bound on the optimism. Gap 1 keeps 55% for the oldest window.
   * The only sourced design (Alfa-Bank on Habr, 551130) trains on one period and tests on "the following period"
     and names no gap. The split auditor proposed gap 1 because the competition supposedly left one month unreleased; no
     source states that.
   * Implemented: gap 0; the notes give the 6-month bound. Alternative: `gap=1`, which costs one month of training data
     per window and shows no measurable score effect. Either way the departure from SPLIT-10 is recorded as
     `**Exception to SPLIT-10 (<date>, Lennart):** no label dates; a horizon gap breaks the 50% floor. Serves
     SPLIT-14.`
   * The advocate and the practitioner: one month does nothing against a delay of up to a year, and a bank's own validation on later issues than those it trained on has
     no gap. The critic: gap 1 is free and closer to the delay. ieee_fraud_detection and
     zillow_prize took one-month gaps because their sources defined a planning month; none is sourced here.
     lending_club made the same unrecorded departure; the rule side is the item "Record the SPLIT-9 / SPLIT-14 reading
     and the SPLIT-10 exceptions" at the end of the working copy's REVIEW.md.

   Recommendation: gap 0 with the exception. Decision: gap 0 with the exception, or gap 1?
   * Update (2026-10-21, Lennart, cross-dataset item on the SPLIT-9 / SPLIT-14 reading): the exception to SPLIT-10
     is now recorded in the notes, the record and splits.md's Cases, worded to hold for gap 0 or gap 1; only the
     length of the gap is open.

**Review panel:** ship after changes (mediator), full panel. Claim audit: 72 claims listed, tested in 35 rows: 4 numbers
refuted or partly refuted and 2 wordings off (all corrected in the definition), 1 maybe refuted (right-censoring,
issue 4), 5 untested (none changes a validity call), the licence not evidence (EV-4), the rest hold. Blind review: include with changes; its main concern, the hand-built aggregation, is
Lennart's CLEAN-19 decision. Agreed: the verdict, the filter, the four dropped copies and the text fixes. Settled by the
mediator: the censoring wording (a linking artefact ruled out) and the competition's design (the sourced "following period"; the unsourced unreleased month
dropped). To Lennart: issues 4, 1 and 3. The mediator's issues 1, 2 and 3 are this file's 4, 1 and 3; the
other reports' "issue 1" and "issue 3" (of the earlier REVIEW.md, "REVIEW_before") are this file's 1 and 3.

<details><summary>Mediator</summary>

**Recommendation**

```text
Verdict: ship after changes.
Validity: SEL-1, SEL-2 hold; USE-1, USE-5 hold, USE-8 approximate (holds); LEAK-1, LEAK-2, LEAK-10 hold (measured);
LEAK-24 maybe (not shown, cannot be settled without a later extraction: note, issue 1); LEAK-30 weak, decided (CLEAN-8,
Lennart 2026-10-19); SPLIT-9 triggered, fixed (client filter, shortcut measured gone; ratification, issue 2); SPLIT-14
holds (60.3 / 72.9 / 83.4%); SPLIT-10 departed from for SPLIT-14 (exception not yet recorded, issue 3); SPLIT-19 does
not ask for a gap (the sourced design is "the following period"); PROV holds.
Value: TP holds (no probe flag; 3.6-3.8k positives per test window; LightGBM beats the dummy on 3 of 3 splits).
Quality: CLEAN-5 triggered, drop 4 exact copies; CLEAN-19 and CLEAN-8 as the curator decided.
Weighed: source +, size +, real module (Habr 551130) +, reconstructed time axis -, unknown label horizon -.
For the curator: issue 1 (LEAK-24 note), issue 2 (ratify the filter against ieee), issue 3 (gap 0 with an exception,
or gap 1).
```

Advocate and critic agree on the verdict and on every change below. Two disputes remained, settled here:

* **Gap 0 vs gap 1 (SPLIT-19).** The critic is right that the definition cannot keep the "unreleased month" claim and
  ignore it. But that claim is untested (claim 51), and EV-7 (Must) does not let it stand as a fact. The only sourced
  design is Habr 551130: "тестовая ... за последующий период в K дней", the period that follows (claim 60; EV-2, the
  source's own document beats our inference). Read that way, SPLIT-19 asks for no gap. So the critic's outcome (b)
  holds: remove the claim and keep gap 0 with an exception to SPLIT-10. `gap=1` stays allowed under SPLIT-10 (Should),
  so the choice goes to the curator (issue 3).
* **Censoring wording (LEAK-24, EV-6).** The advocate's alternative was a client cluster around months 20-21, plus an
  artefact of forward client links (a product in month 23 cannot link forward). I tested it with a backward-only
  definition (a product with an earlier product of the same client):

  | month | 18 | 19 | 20 | 21 | 22 | 23 |
  |---|---|---|---|---|---|---|
  | has an earlier product | 4.30% | 4.50% | 5.24% | 4.95% | 4.50% | 4.03% |
  | first product of the client | 2.75% | 2.80% | 2.80% | 2.85% | 2.67% | 2.59% |

  The dip survives without forward links (5.24% to 4.03%, about 4.6 SE), and first products dip a little too (2.85% to
  2.59%, about 2.4 SE). The forward-link artefact is ruled out. The cluster reading is not, so the finding stays "maybe
  right-censoring" (EV-6). The test that would settle it: labels from a later extraction (probe 13). Neither "no sign"
  nor "the test labels are censored" is supported.

**Changes to make now (no decision needed)**

All of them are edits to dataset.py text, except change 6. Change 6 alters the data, so it needs a rebuild (on the
curator's ask) and a CHANGELOG entry.

1. Replace the curation_comments Note ("no sign of right-censoring", "the competition labelled 7 later months"). Use
   the measured dip and "maybe right-censoring of months 22-23; a later extraction would settle it". (EV-6, EV-7;
   LEAK-24)
2. In the splits_comment, replace "tested on the 7 months after a month that was not released" with the sourced "the
   competition tested on the issues of the following period (Habr 551130)", or cite a source for it. Change "less than
   half of the data" to "58%, 27% and 6%". (EV-7; writing.md)
3. Change "were not known" / "was not known" (splits_comment, README decision 2 text in dataset.py) to "most likely
   not known". Give the evidence: P(later = 1 | earlier = 1) 0.951, flat over 1-10 month lags, against
   P(earlier = 1 | later = 1) 0.455. Replace "as in hotel_booking_demand" with "an evaluation stand-in for an as-of
   filter, which cannot be built without label dates". (EV-6; writing.md)
4. Fix the numbers:
   * whole rubles: "about 70% whole rubles (within 0.01), the rest real kopeck prices; the share peaks at this scale",
     not 98.8%;
   * the summaries in `known`: 512, and 508 after change 6;
   * the inflow median: 5,000 rubles, not 5,600, and add that `income_flag` 3 is rare, undocumented and counted as
     spending;
   * "the others in 2.5%": "the other linked ones 2.5%, unlinked 2.7%";
   * the untuned LightGBM AUCs 0.787 / 0.771 / 0.772: name the config, or give the defaults 0.779 / 0.763 / 0.761.

   (EV-7, EV-8; writing.md)
5. Use case and row: the practitioner's wording, "adds a score from the client's card transactions to its existing
   scorecards (bureau, application) to decide on the product and its terms", plus "issued products only". The fit
   stays approximate. (USE-1, USE-9; writing.md)
6. Drop the four exact copies `out_sum_30d`, `mean_rub_income_flag_2`, `share_mcc_17` and `mean_rub_mcc_17`
   (514 -> 510 features). (CLEAN-5, cheap and safe)
7. REVIEW.md: drop the 127-feature effect sizes and use the split audit's numbers. Without the filter the window gains
   +0.002 / +0.009 AUC, and the linked test products +0.006 / +0.022. (EV-8)
8. Record: add an AI Assessment line that says the 2026-10-07 assessment (127 features) is superseded. Flag to the
   curator that the CC of 2026-10-13 states 513 and the unnamed-config AUCs; that is the curator's line, so do not
   edit it. (records.md)

**Issues for the curator (validity first, Must first)**

1. **Maybe right-censoring of the newest months (P4, LEAK-24 Must; part 3).**
   * Problem: the flag has no horizon, and the default rate falls in months 22-23. That holds without forward links
     (table above).
   * Effect: the newest test window may score against labels that are partly incomplete. The size is unknown.
   * Advocate: a client cluster explains it as well; the rate rose for 20 months, the opposite of censoring.
   * Critic: a client-level flag censored at the cut hits multi-product clients first.
   * Decision: (a) keep with the note from change 1 (both sides; recommended). (b) The definition step: drop month 23
     and shift the windows to 21-22 / 19-20 / 17-18. My estimate from the month counts, not built: the oldest train
     side keeps about 55% after the filter.
   * What settles it: a later extraction of the labels.
2. **The repeat-client filter: ratify, against ieee_fraud_detection (P4, SPLIT-9 Must).**
   * Both sides keep the filter. Measured: it removes a shortcut worth +0.002 / +0.009 AUC; 4 of about 3,640 test
     defaults remain.
   * Consistency check: ieee (CC 2026-10-01) kept same-entity labels at about 95%. The facts that set alfa apart:
     * there is no client feature, so this is a training-row rule (SPLIT-9), not LEAK-34;
     * the 0.951 / 0.455 asymmetry: the earlier flag was most likely set after the later issue;
     * ieee has a one-month gap, alfa none.
   * Decision: (a) keep the filter and record these facts (recommended). (b) Treat it like ieee and keep the products
     with a `Potential leak, kept on purpose:` note. (c) Reopen ieee. (d) An amendment to SPLIT-9 / LEAK-34.
3. **Gap 0 vs gap 1 (P4, SPLIT-10 Should against SPLIT-14 Must).**
   * Gaps of 12 and 6 months break the 50% floor (13.5-26.7%, 35-53%).
   * Gap 1 keeps 55.2% and changes AUC by +0.0051 (SE 0.0032) and +0.0004.
   * A 6-month gap costs 0.014-0.015 AUC, an upper bound on the maturity optimism.
   * Advocate: one month does nothing against a delay of up to 12 months (the practitioner agrees), and the sourced
     design has no gap.
   * Critic: gap 1 is free and closer to the label delay.
   * Decision: (a) gap 0, with `**Exception to SPLIT-10 (date, curator):** no label dates; a horizon gap breaks the
     50% floor. Serves SPLIT-14.` and a `Potential leak, kept on purpose:` sentence with the 6-month bound
     (recommended). (b) `gap=1`, with the same sentence.
   * Either way:
     * Add a Tensions row: SPLIT-9 is met by the filter for the measurable shortcut, and the diffuse rest falls under
       SPLIT-10.
     * This is the second unrecorded case after lending_club; record both, and the third case triggers an amendment.

**Agreed facts**

* **Prediction point and inputs.**
  * Every transaction is 1-359 days before the issue (all 50 parts), and no post-issue card appears in the window.
  * The fields that date the issue are dropped, and `client_key` is split metadata only.
  * No column is post-issue or label-derived. The best single feature scores 0.614 against 0.708; drop-one never
    lowers the score; 0 exact copies across the split; near copies 0.3%.
* **Time axis.** `issue_month` is reconstructed from week codes. The calendar agreement is 1.000, against 0.857-0.859
  for the next best gap, and the gaps show two non-leap years. Dropping `issue_month` changes the AUC by -0.0013
  (SE 0.0029).
* **Repeat clients.** Over 169,096 pairs: P(later | earlier defaulted) is 0.951, flat over lags of 1-10 months;
  otherwise 2.28%. P(earlier | later) is 0.455. The filter removes 32,861-39,221 rows per split; training keeps
  60.3-83.4%.
* **Windows.** 108-121k test rows and 3.6-3.8k positives per window. Seven-month windows would keep 58 / 27 / 6% for
  training.
* **Features.** They are the curator's decided build (CLEAN-19, 2026-10-13). Pivot codes chosen over all rows were
  kept (CLEAN-8, 2026-10-19). The code columns are `category` in the container. `RUBLE_SCALE` is right (sharp peak),
  but the 98.8% is not.
* **Value.** The task probe has no flag (LightGBM 0.744 on 50k-row probes). The use case is real: Habr 551130
  describes the transaction module as an additive supplement to the existing scorecards.
* **Cannot verify.**
  * the default horizon;
  * the competition's test design beyond "the following K days";
  * the 39,240 unlabelled `app_id`s, spread over all months (PROV-13, open);
  * the licence for redistribution (EV-4, not a verdict reason).

**Consistency with precedent**

* **Follows:**
  * CLEAN-19 and CLEAN-8 (this dataset's own Cases rows);
  * the two-month windows (home_credit_default_stability_1m);
  * the dropped ids (african_credit_scoring_challenge, sdss_17);
  * the proxy codes (CLEAN-10);
  * the fit (USE-8 row);
  * the accepted warning (rosbank1).
* **Departs from ieee_fraud_detection on the filter.** The facts that set it apart are listed in issue 2. The
  curator's decision is needed (Consistent judgement, case 2).
* **The gap.**
  * ieee_fraud_detection and zillow_prize took one-month gaps because their sources defined a planning month. Here no
    sourced month exists: that is the fact that sets alfa apart.
  * Lennart's gap decisions (brazilian_ecommerce, college_scorecard: gap = the label delay) are not contradicted: here
    the full delay breaks a Must (SPLIT-14).
  * With lending_club this is the second unrecorded exception to SPLIT-10 for the same reason (issue 3).
* **Record state.** The record has no CC for the 2026-10-15 ship decision; its last curator line is from 2026-10-13
  and its status is `WIP (DF)`. Add the CC when issues 2 and 3 are settled.

</details>

<details><summary>Claim audit</summary>

Data: the prepared `train_features.parquet` (963,811 x 519, full) + `train_target.csv`, splits rebuilt with the
definition's own `SPLIT_WINDOWS` and client filter (counts match the README exactly). Raw transactions: full passes for
partition disjointness, `days_before`, pivot codes and residual links; 10 of 50 partitions (every 5th) for the
ruble/inflow/`hour_diff` checks, and every 10th for the scale scan. LightGBM runs on the full data.

**Table**

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 18 | 98.8% of restored amounts are whole rubles | D `RUBLE_SCALE` docstring; CC bullet 3 | expm1(amnt*17.8209) on 10 partitions, several tolerances | **refuted** (number); scale holds | whole within 0.01 rub: 70.3%; 0.05: 75.3%; 0.1: 78.8%; rel 1e-3: 91.8%; whole kopecks (0.1 kop): 79.3%. Scale scan 17.8207-17.8211: share peaks sharply at 17.8209 (71.9% vs 39% at +-0.00005); remaining amounts carry real kopecks (.50, .90, .80 most common) | EV-7, EV-2; PROV-3 support stays (scale peak) |
| 5, 67 | "513 summaries" / "513 aggregates" | D task_summary.known; R CC 2026-10-13 | count of feature columns of the prepared table | **refuted** (off by one) | 513 columns besides id/target/time/link fields = `product` + 512 aggregates; README 514 features = 512 + `product` + `issue_month` | writing.md, EV-7 |
| 19 | inflow 8% of transactions, median 5,600 rubles; 1 is spending | D `INFLOW_CODE` docstring | 10 partitions | **partly refuted** | share 7.7% (holds); median 5,000.0 rub (8.1% of inflows are exactly 5,000), not 5,600; `income_flag` also takes value 3 (3-66 rows per partition), treated as spending by the code | writing.md |
| 46 | "no sign of right-censoring" | D CC Note | default rate by month, product-standardised and single-product clients | **maybe refuted** (circumstantial both ways) | product-standardised rate rises to 3.53% (m21) then falls to 3.23% (m22) and 3.09% (m23), about 4-5 SE (n~60k/month); raw 3.36 -> 3.07 -> 2.97%. Single-product (unlinked) clients are flat 2.6-2.75% throughout (m21 2.75, m22 2.58, m23 2.59). The flag behaves as a client-level event after issue (row 43), so the newest products have had the least time for it. "7 later months labelled" is not a test on this data | USE-5, LEAK-24, SPLIT-10, EV-6 |
| 52 | 3 windows of 7 months leave less than half the data for training | D splits_comment | cumulative month counts | **partly refuted** | train share 58.3% (test 17-23), 26.7% (10-16), 5.8% (3-9): true for 2 of 3 windows, not the newest | writing.md |
| 42 | linked test products: 95.6% vs "the others in 2.5%" | D CC Repeat clients; _decisions | recompute | holds, wording ambiguous | split 0: 502 linked with defaulted earlier product, 95.62%; linked non-defaulted 2.46%; unlinked 2.69%; all non-flagged test 2.63%. Splits 1/2: 96.3%/93.7% | writing.md |
| 33 | pivot codes over all transactions: "not a value computed from test rows" | D CC bullet; curator CC 2026-10-19 | choose codes on months 0-17 only (split 2's train) vs all | holds literally; effect measured | 10 codes differ: operation_type +12 vs 20,22; payment_system +5; country 11,13 only in train; mcc 21,38 vs 44,46; card_type 3,22 vs 42,51. Decided by the curator; numbers for the record | LEAK-30 (weak, decided) |
| 32, 69 | untuned LightGBM 0.787 / 0.771 / 0.772 | D CC; R CC 2026-10-13 | full-data LightGBM on the shipped windows | holds only for an unstated config | LGBM defaults: 0.7794 / 0.7634 / 0.7614 (0.7781 with `issue_month`); 1000 trees, lr 0.02, subsample 0.8, colsample 0.5, with `issue_month`: 0.7871 on window 22-23. "Untuned" without the config is not reproducible | EV-8 |
| 44, 50, 58 | the filter removes the training products of the test window's clients | D `_make_splits`, splits_comment | split 0: identical-transaction keys (definition's `transaction_keys`) between test products and KEPT training products of months 10-21, over the whole calendar range [day(m10), day(m21)) | holds (residual negligible) | 743 test products still meet 3 shared / 80% under the wider window; 4 of them have a defaulted kept training product, all 4 default (4 of ~3,640 test defaults). Looser links carry no concordance: n>=3 any share 5.4% vs base 3.0%; n>=10 4.3% | LEAK-16 to LEAK-21, SPLIT-29 |
| 43 | the earlier flag was most likely set after the later issue | D CC | within-client consecutive pairs | holds (supported) | P(later=1 / earlier=1) 0.951, flat over gaps 1-10 months (0.94-1.0); P(earlier=1 / later=1) 0.455: the asymmetry fits a client-level default after both issues flagging still-open products; an earlier default known at the later issue would make the later issue rare | LEAK-10, SPLIT-10 |
| 40 | products of one client less than a year apart share transactions | D CC | client month spans | holds | 301,657 products, 132,561 clients; spans 1-11 months dominate (7.6k-14.4k each), spans 12-23 exist only via chains (12,000 clients); one client spans 0 months | |
| implied | no row is a copy across the split | — | row hashes | holds | 0 duplicate rows (with or without month/target), 0 exact feature copies test vs kept train in all 3 splits | LEAK-16 |
| 47 | no duplicate rows | D CC | full hash | holds | 0 (the bundle check was skipped by budget; this is the full run) | CLEAN |
| implied | every feature is known at the prediction point | — | (a) `days_before` range; (b) does a new `card_type` first appear just before the issue (the new product's own card)? | holds | (a) 1-359 over all 50 partitions; (b) first appearances of a card type after history start (137,241 in 10 partitions) have flat daily density: 0.0029/day in days 1-7, 0.0024 in 8-14, 0.0026 in 15-30, 0.003 in 120-300; rate by product type the same in the last 14 days as in days 151-164. No post-issue card in the window | LEAK-1, LEAK-2, USE-3 |
| implied | the issue date is a real per-month date | — | `issue_day` gaps | holds, with a nuance | gaps 31,28,31,30,31,30,31,31,30,31,30,31 twice: calendar months from a January, two non-leap Februaries. Every product of a month shares one reference date: a monthly snapshot, not the product's own issue day. Test (b) above shows no post-issue spending, so the window ends at or before the issue | USE-2 |
| 21 | `days_before` runs 1-359 | D `RECENT_DAYS` | all partitions | holds | min 1, max 359 | |
| 22 | `hour_diff` -1 marks the first transaction | D docstring | 10 partitions | holds | 198,387 values -1 = 198,387 products; agreement with "first by transaction_number" 1.000; `amnt` 0.0 is 0.41% | CLEAN |
| 23 | each partition holds all transactions of its products | D `_prepare_raw_files` | app_id overlap across 50 parts | holds | 0 overlap, 963,811 products | |
| 26 | every labelled product has transactions | D `_clean` assert | merge | holds | 963,811 = 963,811 | |
| 36, 57 | 24 runs; 11 of 12 week codes recur; months 7, 16 mix two codes | D CC, Decision 1 | recompute | holds | codes y1 [1,48,32,18,2,13,3,37,12,17,45,38], y2 the same except 44 at month 16; share 0.782 (m7), 0.741 (m16), 1.0 elsewhere | |
| 24 | months 7 and 16 issued on a Tuesday | D `calendar_months` docstring | — | untested | week codes are anonymised; weekday not recoverable here | EV-7 |
| 25 | one gap fits per month pair, second best far below | D `issue_calendar` | issue_calendar.csv | holds | agreement 1.000 every pair; second best 0.857-0.859 | |
| 37, 38 | 292 products moved; `app_id` 0-4 in month 0 | D CC | `rolling_months` vs `issue_month` | holds | 292; month 0 starts at app_id 0; no app_id overlap between months | |
| 45 | default rate 2.0-2.6% (m1-12), 3.0-3.4% (m18-23) | D CC Note | per month | holds | 1.99-2.61% and 2.97-3.36%. New fact: the rise is all in multi-product clients; single-product clients stay at 2.3-2.75% | |
| 54 | 12-month gap leaves 13-27% for training | D splits_comment | cumulative counts | holds | 13.5% / 19.9% / 26.7% | |
| 56 | unused rows are months 0-17 clients in all three windows | D accepted warning | recompute | holds | 219 rows, months 0-17 | |
| 72 | 963,811 rows; n_train 581,221-804,162 | README | recompute | holds | 804,162 / 702,678 / 581,221 kept; removed 39,221 / 32,861 / 32,928 | |
| 15 | target sha256 and byte counts | D download_description | sha256, sizes | holds | 470ea19c...3d74, 10,498,134; 50 parts, 4,242,459,450 bytes | PROV |
| 12, 13 | boosters links 404; ODS.ai re-host of Nov 2020 files | D download_description | curl; dir mtime | holds | boosters 302 -> "404" loop; ODS.ai 200, 10,498,134 bytes; unzipped dir dated 2020-11-21 | PROV |
| 29 | one year of transactions before issue; flag = default on a credit product, no horizon | D CC | Habr 551130 | holds | "историей клиентских транзакций глубиной в год"; "флагу дефолта по кредитному продукту"; no horizon; 1.5M issuances in the full release | USE-2, USE-5 |
| 60 | train N days, test the following K days | R | Habr 551130 | holds | "Обучающая выборка состоит из выдач за период в N дней, тестовая ... за последующий период в K дней" | |
| 51 | the competition tested on 7 months after an unreleased month | D splits_comment | — | untested | test files not held; consistent with the unlabelled app_id range after 1,003,050 but not checked | EV-7 |
| 16 | Kaggle mirror byte-identical | D | — | untested today | not re-downloaded | |
| 17 | competition dates | D bibtex | web search | untested | dates not found in the sources searched | PROV-16 |
| 30, 62, 68 | top boosting 0.774-0.780 private; organizers 0.737 / RNN 0.760; slides | D CC; R | — | untested | slides not re-read | EV-7 |
| 11, 66 | licence | D | — | not evidence | EV-4 | EV-4 |

**Refuted and untested, ranked (validity first, Must first)**

1. **Claim 46, "no sign of right-censoring" (P3/P4, USE-5, LEAK-24, SPLIT-10; maybe, EV-6).** The product-standardised
   default rate falls from 3.53% (month 21) to 3.23% and 3.09% (months 22-23), about 4-5 SE, after rising for 20 months;
   single-product clients show no dip, so the evidence is mixed. Changes: the sentence is not supported as written, and
   the fit_reason's "newest training products may not yet show a default" is the honest reading. Mildest remedy:
   replace the sentence with the measured dip ("maybe right-censoring of the newest months"); the gap question stays
   with the curator (REVIEW issue 3); a 1-month gap would be the next step if the curator wants it.
2. **Claim 18, "98.8% whole rubles" (P5 support, writing; EV-7).** Measured 70-79% (absolute tolerances), 92% at a
   relative 1e-3. The scale is still right (sharp peak at 17.8209), so the features do not change. Remedy: correct the
   number in `RUBLE_SCALE` and the bullet (for example "about 70% whole rubles, the rest real kopeck prices; the share
   peaks at this scale").
3. **Claims 5/67, "513 summaries" (writing).** 512 aggregates + `product` (+ `issue_month` as the 514th feature).
   Remedy: say 512 in task_summary.known (and the CC wording is the curator's; flag it, do not edit).
4. **Claim 19, "median 5,600 rubles" (writing).** Measured 5,000 (8% of inflows are exactly 5,000); `income_flag` 3 also
   exists. Remedy: correct the docstring.
5. **Claim 52 (writing).** "less than half" holds for 2 of 3 seven-month windows only (newest 58%). Remedy: "would leave
   58%, 27% and 6% of the data for training".
6. **Claim 32/69 (EV-8).** Reproduced only with a slow-learning config (0.7871); LightGBM defaults give 0.779 / 0.763 /
   0.761. Remedy: name the config next to the numbers.
7. **Claim 42 wording (writing).** "the others in 2.5%" is the linked-but-not-defaulted group (2.46%); unlinked test
   products default at 2.69%. Remedy: "the other linked ones in 2.5%, the unlinked 2.7%".
8. **Claim 33 (decided, LEAK-30 weak).** Holds literally; choosing on the training months would change 10 pivot codes.
   Numbers only, for the record of the curator's decision.

Untested: 16 (Kaggle re-compare), 17 (bibtex dates), 24 (Tuesday), 30/62/68 (slides and leaderboard numbers), 51
(competition test design). None of them changes a validity call.

Nothing found against the prediction point, the client filter or copies across the split: the strongest attacks (a new
card in the last days, residual identical-transaction links after the filter, exact copies) all came out clean.

</details>

<details><summary>Column audit</summary>

Frame: rebuilt from the definition through `dataset_io.load(..., built=True)` (README `build: null`, so origin
`rebuilt`): 963,811 rows, 514 features + `default`. 500 float32, 13 categorical (`product`, 6 `mode_*`, 6 `last_*`;
category dtype confirmed on `ds.df`, `plan.df` and the container), `issue_month` int64. Per column: dtype, missing share, distinct values, univariate AUC on all rows, Spearman with
`issue_month` on 200k rows, target rate when missing / present.

Prediction point (first curation_comments bullet): a credit product is issued; known are the product type and the
card transactions of the year before. Every transaction has `days_before` 1-359 (checked on part_000 and in the
definition), so every aggregate is pre-issue by construction. The source codebook (organizers' feature table, quoted
in the definition) gives: `amnt` normalised amount (0.0 = missing), `hour_diff` hours since the previous transaction
(-1 on the first: confirmed, 100% of -1 are the product's first transaction, every first transaction is -1),
`days_before` days before the issue, `transaction_number` order of the transaction (checked: contiguous 1..n, and
`days_before` never increases with it, so "last by number" is the newest transaction, as `last_*`, `balance_*` and
`latest_*` assume), `income_flag` 1 out / 2 in, `product` the credit product type. Codes of `mcc`, `card_type`,
`city`, `country`, `currency`, ... are anonymised integers (meaning unknown beyond the column name; `Anonymized` tag).

**Column table (families; 514 features)**

| Column / family (n) | Meaning | Known at prediction? | Dtype and cleaning | Verdict | Rule |
|---|---|---|---|---|---|
| `issue_month` (1) | reconstructed issue month 0-23 from week codes (no label used) | yes, the bank knows the issue date | int64, time column, kept as a feature; test months 18-23 lie beyond every training month | fine; question (low): it ships as a feature whose test values are always out of the training range | SPLIT-7, USE-6 |
| `product` (1) | credit product type (codebook) | yes | category, 5 codes; code 4 appears from month 9 (new product, 9.5% of month 23); default rate 2.0-7.1% by code | fine | USE-6, CLEAN-14 |
| `default` (target) | "1 - факт ухода в дефолт", no horizon | outcome | category Yes/No | fine (horizon is a split question, REVIEW_before 3) | USE-5 |
| `rub_*` stats and quantiles (12), `rub_*_30d/90d` (6) | restored ruble amounts over the year / last 30, 90 days | yes | float32; `amnt` 0.0 -> NaN before aggregating; 3 rows with no known amount are NaN (2 of 3 default: n too small to matter) | fine | CLEAN-10, LEAK-10 |
| `n_transactions*`, `share_no_amount`, `hour_*`, `share_night`, `days_before_*` (11) | counts, timing, recency, history length | yes | float32; `days_before_min` equals the dropped `latest_days_before` (newest transaction) | fine; `share_no_amount` rises 0.3% (months 0-11) to 1.0% (month 23): the source's zero-amount code drifts, pre-issue, no action | LEAK-10 |
| `hour_diff_*` (7), `share_hour_diff_*` (5) | gaps between transactions | yes | -1 -> NaN (first transaction), confirmed on raw | fine | CLEAN-10 |
| `share_<col>_<code>` (145), `amount_share_<col>_<code>` (85), `mean_rub_<col>_<code>` (145) | per-code count share, amount share, mean amount; 10 coded columns (codes >= 0.1% of transactions) + top-30 `mcc`, `card_type` | yes | float32; codes chosen over all transactions incl. test windows: CLEAN-8 applied (Lennart, 2026-10-19, bullet present); `mean_rub_*` NaN when the code is absent (structural, up to 99.9%) | fine; 4 exact copies, see problem 2 | CLEAN-8, CLEAN-5 |
| `n_distinct_*` (16) | distinct codes | yes | float32 | fine | |
| `mode_*` (6), `last_*` (6), `share_mode_*` (6) | most frequent and newest code, mode share | yes | category (codes, not quantities); ties to the lower code | fine; `mode_card_type`/`last_card_type` drift with month (rho -0.20/-0.18), single AUC 0.59-0.60 in the probe: a client's card portfolio, legitimate history | LEAK-34, CLEAN-14 |
| `out_*`, `in_*`, `out_in_ratio`, `n_salary_inflows`, `in_block_*`, `n_blocks_with_income` (16) | money in (`income_flag` 2) against out | yes | float32; ratio NaN when denominator 0; `income_flag` 3 (undocumented, 66 of 5.4M on part_000, 2 of 5.4M on part_049) counts as spending | fine (note only) | CLEAN-10 |
| `out_sum_block_k`, `share_out_block_k` (24) | spending per 30-day block | yes | NaN when the block is older than the product's history: missing iff `days_before_max` <= 30k (100%); probe missing-indicator max 0.573 | fine: real process known at issue | LEAK-10 (not triggered) |
| `active_days*`, `daily_*`, `gap_days_*`, `transactions_per_active_week` (13) | daily activity | yes | float32; `active_weeks` dropped (internal) | fine | |
| `balance_*` (6) | running in-minus-out sum, transaction order | yes | float32; a proxy without starting balance | fine | CLEAN-19 |
| `out_ratio_*`, `count_ratio_30d_90d` (3) | recent vs year | yes | NaN on zero denominators | fine | |
| dropped: `app_id`, `latest_week_code`, `latest_days_before` | issue order / issue-week code | `app_id` encodes time (now `issue_month`) | dropped in `_clean` | fine | CLEAN-3 |
| dropped: `client_key` | linked-client id built from shared transactions | split metadata | removed in `_make_splits`, never a feature | fine | LEAK-33 |

Strongest single columns (full data, rows present): `mean_rub_country_5` 0.650 (7% present; rho -0.35 with month),
`mean_rub_operation_kind_1` 0.650, `mean_rub_operation_type_1` 0.645. Probe: best single 0.614 against 0.708 for all
features; drop-one never lowers the score; exact copies across the split 0.0%. Strongest month drift:
`share_payment_system_3` rho -0.42, `amount_share_payment_system_3` -0.38, `share_mcc_12` +0.33: card-scheme and
merchant mix changing over two years, pre-issue facts. No column is post-issue, label-derived, outcome-missing or an
id that encodes the label. No constant column; two near-constant (`amount_share_operation_type_group_3`,
`mean_rub_operation_type_group_3`, 99.95% one value, kept: CLEAN-5 drops only constants).

**Problems, ranked (principles.md)**

P1-P4: no column-level leak. The prediction point holds for every column (all transactions are 1-359 days before the
issue; the issue-dating fields are dropped; `client_key` is split metadata). The `amnt` normalisation by the source,
which may have used the maximum over all rows (LEAK-30), is undone by the fixed restoring constant: the stored rubles do
not depend on test rows (the constant peaks sharply: 66% whole rubles at 17.8209 against 2.5% at 17.80 and 1.7% at
17.84, part_049).

1. **P5 / procedure, a claim that does not reproduce (EV-1; writing.md).** "98.8% of the restored amounts are whole
   rubles" (`RUBLE_SCALE` docstring, bullet 3, record CC 2026-10-13). Measured with |r - round(r)| < 0.01: 71.1% on
   part_000, 66.3% on part_049 (by size on part_049: 70% for 10-1,000 rubles, 38% for 10k-100k, 0.2% above 100k, where
   the 4-digit constant's precision moves the value by a few rubles); 100% within 0.5 ruble. The restoration itself is
   right; the number is not. Remedy: restate the measure behind 98.8% (tolerance, subset) or replace the number; no
   data change.
2. **P7, exact copies (CLEAN-5, Should).** Four column pairs are identical on all 963,811 rows:
   `out_sum_block_0` = `out_sum_30d` (block 0 is days 1-30); `mean_rub_income_flag_2` = `in_mean`;
   `share_mcc_17` = `share_mcc_category_15` and `mean_rub_mcc_17` = `mean_rub_mcc_category_15` (mcc 17 is the only
   pivoted code in category 15). Remedy (cheap, safe): drop one of each pair in `aggregate_transactions`
   (e.g. `out_sum_30d`, `mean_rub_income_flag_2`, `share_mcc_17`, `mean_rub_mcc_17`); 514 -> 510 features. The
   probe's drop-one could not see this (LEAK-2 pattern: a copy hides the other).
3. **Procedure, feature count in the notes (writing.md).** `task_summary.known` and the CC say "513 summaries"; the
   frame has 512 aggregates (500 float32 + 12 `mode_*`/`last_*`) + `product` + `issue_month` = 514. With problem 2
   fixed it would be 508. Remedy: state the count from the frame.
4. **P7, note only.** `income_flag` has an undocumented code 3 (66 of 5.4M transactions on part_000), counted as
   spending; `INFLOW_CODE` docstring says "1 is spending". Remedy: one clause in the docstring ("3, rare and
   undocumented, counts as spending"). Effect negligible.
5. **Question for the curator (low).** `issue_month` is the time column and also a feature; every test window's
   values (18-23) lie beyond the training range, so a model can only extrapolate (default rate drifts 2.0-2.6% to
   3.0-3.4%). Known at issue (USE-6), so no leak; whether time columns ship as features is a collection convention.

Not re-examined here (split level, other panel members): REVIEW_before issues 1 (repeat-client filter) and 3 (window
and gap / label maturity, LEAK-24, SPLIT-10).

</details>

<details><summary>Split audit</summary>

Definition: `datasets/_dev/tabarena-v0pt2/alfa_battle_2_0_task_2/dataset.py` (temporal on `issue_month`, 3 windows of
2 months, no gap, training sides without the products of the test window's clients). Models: untuned LightGBM, 500 trees, lr 0.05, 63 leaves; every variant trained on a
random 250,000-row sample of its training pool so that the variants differ in which rows, not how many; full test
windows; bootstrap SE of the paired AUC difference over 200 resamples. Numbers are probe numbers, not leaderboard
numbers (EV-8).

**Verdict: right with notes**

The regime (temporal), the windows and the repeat-client filter are right. One P4 note: the training sides carry
labels that mature after the window start (no gap). Mildest remedy: a one-month gap, which follows the source's own
design, costs no score and keeps the 50% floor; state the measured optimism of the remaining months in the notes.

Validity: SPLIT-1/SPLIT-6 hold (temporal, the use case scores future issues); SPLIT-9 holds for the repeat-client
channel (filter removes the shortcut, measured); SPLIT-9/SPLIT-10 triggered, weak, for the general label maturity
(remedy: gap 1 + note); SPLIT-12/SPLIT-19 departed from for SPLIT-14 (Must), justified; SPLIT-14 holds (60.3-83.4%
after the filter); SPLIT-20 holds; SPLIT-29 not triggered (near copies 0.3%).

**Regime**

* Use case: a bank scores each new credit product at issue (task_summary). The products are future issues; the
  clients are card holders, 20.8% / 22.8% / 23.6% of the test products (windows 18-19 / 20-21 / 22-23) have an earlier
  product of the same client, the rest are first products. A stream over time with recurring entities: temporal is the
  right regime (SPLIT-6, SPLIT-3, USE-10); grouping by client is not the use case (the bank scores known clients too),
  and the recurring clients are handled by the filter (SPLIT-13).
* IID optimism for reference (same model, 250k training rows): random split 0.765, random split grouped by client
  0.754, shipped temporal windows 0.759 (22-23) and 0.746 (18-19). The temporal choice costs 0.006-0.019 AUC; it is
  the application, not the score, that decides (SPLIT-4).

**Time column and windows**

* `issue_month` (0-23) is reconstructed from the week codes (decision 1: calendar agreement 1.000 at one gap per pair
  against 0.857-0.859 for the next best). The days between issue dates read 31, 28, 31, 30, 31, 30, 31, 31, 30, 31,
  30, 31, 31, 28, ...: two non-leap calendar years, so months 0-23 are two consecutive years (Jan-Dec or Dec-Nov,
  depending on whether the date is the first or last of the month). Monotone in `app_id`; 292 products moved at the
  edges. Sound as a time index (SPLIT-7, SPLIT-22).
* Windows (rows; positives): 22-23 120,428; 3,637 / 20-21 107,844; 3,628 / 18-19 121,390; 3,792. Training after the
  filter: 804,162 / 702,678 / 581,221 = 83.4% / 72.9% / 60.3% (SPLIT-14 holds). Rows in no split: 219 (accepted
  warning, correct).
* Training history: expanding, at least 18 months (more than one season) before every window (SPLIT-11, SPLIT-20).
  No break visible; the default rate rises from 2.0-2.6% (months 1-12) to 3.0-3.4% (18-23), smoothly.
* Season: all three windows lie in the second half of the second year. The first year shows no seasonal swing of the
  default rate (2.2-2.6% in its second half against 2.0-3.1% in its first), and the newest window (year end) has 3.07% /
  2.97%, not atypical. Pass (SPLIT-20), with the note that no window covers the first half of a year.
* `issue_month` is a feature of the shipped frame. Dropping it changes the newest window's AUC by -0.0013 (SE 0.0029):
  no time shortcut.

**Problems, ranked (all P4)**

**1. Label maturity: no gap (SPLIT-9 Must, graded by SPLIT-10 Should; SPLIT-19 Should) - note, mild remedy**

* Fact: the default flag has no stated horizon (Habr 551130: only "флаг дефолта по кредитному продукту"). Every
  training product issued within the horizon before a window carries a label a model refit at the window start would
  not have had. The splits_comment says so in words; nothing measures it.
* Measured, equal training size (250k), AUC difference against the shipped gap 0:

  | window | gap 1 | gap 3 | gap 6 | no client filter |
  |---|---|---|---|---|
  | 22-23 | +0.0051 (SE 0.0032) | -0.0049 (0.0030) | -0.0145 (0.0030) | +0.0020 (0.0033) |
  | 18-19 | +0.0004 (0.0031) | +0.0001 (0.0030) | -0.0140 (0.0030) | +0.0087 (0.0027) |

  The newest one to three months add nothing (no sharp shortcut of the hotel_booking_demand kind); a 6-month gap
  costs 0.014-0.015 AUC on both windows. That is an upper bound on the optimism if the horizon is 6 months or more
  (it mixes staleness, which the deployed model would also suffer, with post-cutoff label information). Two windows
  only, so it informs the note and decides nothing about the history (SPLIT-21).
* Conflict: a gap of the full horizon (12 months) leaves 13-27% for training, below the SPLIT-14 floor (Must); a gap of
  6 months leaves 35-53% (fails on the two older windows); gap 2 leaves 72.8 / 60.9 / 50.0% (borderline); gap 1 leaves
  77.6 / 67.0 / 55.2%.
* The source's own design (claim 51, splits_comment) is a test period after a month that was not released. A gap of
  1 month follows it (SPLIT-19), passes SPLIT-14 and costs no score.
* Mildest remedy: `TemporalSplits(window=2, unit="unique", n_windows=3, gap=1)` with
  `Temporal(on="issue_month", horizon=2, horizon_unit="months", gap=1, gap_unit="months")`, and a
  `Potential leak, kept on purpose:` sentence in the splits_comment with the measured bound (a 6-month gap at equal
  training size lowers untuned LightGBM by 0.014-0.015 AUC; the full horizon would break the 50% floor). Keeping
  gap 0 with only that note is also defensible (SPLIT-10 is a Should, the effect is weak); a weighing call for the
  curator (REVIEW_before issue 3).

**2. Repeat-client filter (SPLIT-9 Must) - right, keep**

* The flag is client-level: of 169,096 earlier/later product pairs, the later product defaults in 95.1% of the pairs
  whose earlier product defaulted (3,318 pairs) against 2.28% otherwise, and the concordance does not decay with the
  lag (94.1% at 1 month, 95.5% at 3, 95.8% at 6, 94.4% at 8). A bank would not issue a new product to a client already
  in default, so the earlier flag was set after the later issue: not known at the prediction point. Removing those
  training products is SPLIT-9 applied.
* The filter removes the shortcut (the check SPLIT-9 asks for): with the filter, the linked test products score below
  the others (0.742 vs 0.762 on 22-23; 0.734 vs 0.747 on 18-19); without it, the linked products gain +0.006 / +0.022
  and the window +0.002 / +0.009. (REVIEW_before measured +0.0045 on the newest window with the 127 features, full
  data.)
* The client key is built from identical transactions (exact matches, at least 3 and 80% of the smaller product's in
  a 28-day window), not from a similarity cluster or a feature hash: acceptable under SPLIT-24 for a filter. Clients
  the rules miss stay in training; the hidden-group probe finds near copies for 0.3% of the test rows, so the residual
  is small. The filter uses the test window to choose the dropped training rows, but drops only rows, never adds test
  information.
* Note for the wording (writing.md, also in the checklist): "the others in 2.5%" is the linked products whose earlier
  product did not default (0.0246); the unlinked test products default in 2.69%.

**3. Window length against the source's test period (SPLIT-12, SPLIT-19 Should against SPLIT-14 Must) - right**

* 7-month windows like the competition would train on 58.3% / 26.7% / 5.8% of the rows: SPLIT-14 fails, so the
  departure is forced by a Must and is written down. Two-month windows hold 108-121k test rows and 3.6-3.8k positives
  each. One-month windows (months 21-23) would also pass (79-91% training) but cover only 3 months; the 2-month choice
  spreads the test over half a year. Keep. `horizon=2` is our refit cadence, not a source fact; the splits_comment
  says so implicitly ("refit ... used for the next two months"), fine.

**4. Unsourced claim about the competition's test period (EV-7, writing.md) - note**

* "Tested on the 7 months after a month that was not released" has no citation in the definition or the record. Habr
  551130 gives only N training days and the following K test days, and 1.5M issuances in total. 1.5M minus the
  1,003,051 ids of our range is about 0.5M, about 7-8 months at the late issue rate (58-62k per month): consistent, not
  proven. Cite the source (slides, test file) or soften it.
* The 39,240 unlabelled `app_id`s inside the range are spread over all 24 months (2.6-7.5% of each month's id span),
  so they are not a held-out month; what they are is unknown (PROV-13 question, not a split problem).

**Cannot verify today**

* The default horizon and the competition's test period (claim 51): no primary source found.
* The residual of clients the link rules miss (needs the transaction files; only the near-copy probe speaks to it).

</details>

<details><summary>Domain practitioner</summary>

Role: a credit-risk modeller at a retail bank (Alfa-Bank's risk team) who builds the transaction-based score that
enters the bank's credit decision. Measured on the clean-room sample (200,000 rows).

**Fit**

**Approximate (USE-8), as declared.** One row is one issued credit product scored from the client's year of card
transactions before the issue, which is exactly the transaction module Alfa-Bank runs, but the default flag has no
stated horizon and the issue months are reconstructed, so the label's timing and the split only approximate the
bank's own out-of-time validation.

**What the source says the bank does (domain)**

* Habr 551130 (Alfa-Bank, 2021): one object = one issuance of a credit product ("1.5 млн выдач кредитных
  продуктов"), with "история клиентских транзакций глубиной в год" and the type of the issued product; the target is
  "флаг дефолта по кредитному продукту", no horizon. Classic models use "в том числе транзакции и данные бюро
  кредитных историй"; the transaction model "встраивается в бизнес-процесс в виде аддитивной добавки к действующим
  моделям" (an additive supplement to the existing models). Train: issues over N days, test: the following K days.
* ODS.ai 2022 re-host: "Предсказание выхода в дефолт по данным карточных транзакций", "кредитный скоринг", metric
  ROC AUC, test on the following K days.
* So the real decision is: at application/issue of a credit product (credit card, cash loan, etc.) to an existing
  card client, the bank combines bureau, application-form and internal-history scorecards with a transaction score;
  this dataset trains that transaction score. Banks report Gini (= 2 AUC - 1) for such modules and validate them
  out-of-time on later vintages.

**The four questions, as the modeller**

1. **Inputs at prediction time.** I have every input: the product type and transactions up to the day before the
   issue (`days_before` 1-359; `days_before_min` median 2). Nothing here comes after the issue (probes: best single
   feature AUC 0.614, no post-outcome column). What I would always have and do not see: the bureau file, the
   application form (income, age, requested amount/limit and term), and the status of the client's other Alfa
   products at the issue (current days past due). Since Habr says the transaction model is an additive module on top
   of models that hold those, their absence is the module's design, not a gap (USE-6, USE-9 reasoning). One small
   timing doubt: if the score is used at application rather than at issue, the last days of transactions (between
   application and issue) would not yet exist (USE-3); the source names the issue, so I accept it.
2. **Target.** I act on default, the right target (USE-5), but I would want it defined as in our policy, e.g.
   90+ days past due within 12 months on book. Without a horizon I cannot tell whether a product issued 2 months
   before the data cut had a full observation window. The default rate rises from 2.0-2.6% (months 1-12) to
   3.0-3.4% (months 18-23; sample: 0.0311-0.0340 in months 18-21), the opposite of right-censoring, which reassures
   me but proves nothing (it may be a risk-appetite or product-mix change). I want a probability: for the decision
   ranking (AUC/Gini) is what I validate on, and for terms/pricing I need a calibrated PD; ROC AUC is the metric my
   team would use (fits P4), log loss is worth reporting beside it.
3. **Row and test data.** One row = one product decision, yes. Test = the next two issue months, which is what I
   face. The product mix moves: product 4 does not exist in months 0-11 and is 8-16% of the test months
   (sample: 0.0% in month 6, 16.3% in month 18, 9.9% in month 23), and product 0 rises from 35% to 50-60%. Per-product
   default rates differ a lot (sample: product 2 7.1%, product 3 1.9%, overall 2.8%). That drift is realistic and a
   good reason to keep the temporal split. The repeat-client filter matches what I could know: at a new issue I do
   not yet know whether the client's earlier product will default (the 95.6% vs 2.5% contrast shows it would be a
   leak).
4. **Would I use it?** Yes, as the transaction module. Trust: the features are what my team builds (the top
   solutions' aggregates), test is out-of-time, AUC 0.77-0.79 is in the range of real transaction modules (Gini
   0.54-0.58). Distrust: (a) the labels of the training products of the 12 months before each window were not
   mature at the window start; in my practice the development sample ends 12+ months before deployment (a vintage
   with full performance), so a model refit on "all products issued so far" (splits_comment) is not what we deploy.
   However, our own out-of-time validation does exactly what this split does (train on earlier vintages, test on the
   newest matured vintage, no gap), so the split mirrors validation rather than deployment. (b) The month axis is
   inferred, not given; the calendar evidence (agreement 1.000 at one gap per month pair) convinces me it is right.

**Gaps, ranked by how much they change the task**

1. **Label horizon and maturity unknown** (USE-5, USE-8; LEAK-24/SPLIT-10 for the split). The task is "default ever
   flagged by the data cut" rather than a fixed-window default; the newest training months carry less-observed
   labels than older ones, and the split simulates validation, not deployment. Changes how optimistic the scores are,
   not what is predicted. Already named in fit_reason; keep approximate.
2. **Population is issued products only** (no rejected applicants; reject inference). Every credit dataset shares
   it; the test population matches the training population, so the benchmark is consistent, but the model's AUC on
   all applicants is unknown. Not named in the task_summary; worth one clause.
3. **Missing bureau, application and internal-history inputs.** The full credit decision uses them; the module
   does not (Habr: additive supplement). Changes the use case wording more than the task (see the expert change).
4. **Reconstructed issue month** (USE-8). Strong evidence it is right; risk is only at month edges (292 products
   moved). Small effect.
5. **Product-mix drift** (product 4 appears in month 12). Realistic, a feature of the task, not a gap; worth a line
   in the notes for users who see per-window differences.
6. **Prediction point at issue vs application** (USE-3). The source names the issue; if the bank scores at
   application, the last few days of transactions would be unknown. Not measurable from the data; minor.

**What an expert would change**

* Rewrite the use case to the source's own framing (USE-1): "When a client applies for a credit product, the bank
  adds a score from the client's card transactions to its existing scorecards (bureau, application), to decide on
  the product and its terms." The current wording reads as if transactions alone drive the decision. This is the
  USE-9 question: it makes the missing bureau and application inputs part of the design, but does not lift the fit
  to direct because the horizon remains unknown (and rephrasing only to excuse a gap is the weighed factor against).
* Keep the split (3 two-month windows, no gap): it mirrors a bank's out-of-time validation; a 12-month gap would be
  closer to deployment but leaves 13-27% for training (REVIEW_before issue 3). I would not add `gap=1`: it changes
  little about maturity (the issue is 12 months, not 1).
* Keep the repeat-client filter (REVIEW_before issue 1, option a): the earlier product's final flag is not known at
  the new issue.
* State the population (issued products of Alfa card clients) in `row` or `fit_reason`.
* Report log loss or a calibration check beside ROC AUC if the collection allows it, since terms and pricing need a
  calibrated PD (P4 side note; metric choice stays ROC AUC like the competition).
* Writing detail seen on the way: the shipped frame has 500 float + 12 code summaries + `product` + `issue_month`
  = 514 features, so "513 summaries" in `known` likely counts one of them as a summary; worth a recount by the
  writing reviewer.

**Sources**

* Alfa-Bank on Habr, 2021: https://habr.com/ru/companies/alfa/articles/551130/ (fetched 2026-10-20)
* ODS.ai 2022 competition page: https://ods.ai/competitions/dl-fintech-card-transactions (fetched 2026-10-20)
* Boosters overview (record): https://boosters.pro/championship/alfabattle2/overview
* Behavioural-scoring write-up on the same data: https://habr.com/ru/post/680346 (search result, not read in full)
* alfa_ct data card (field `flag`, `product`, `app_id`): https://huggingface.co/datasets/mllab/alfa_ct/blob/main/README.md
  (search result)

</details>

<details><summary>Blind review</summary>

**Verdict**
Include with changes. The task is real (a bank scoring card-credit applications), there is no leakage, and the signal is realistic. The changes: mark the code columns as categorical, drop columns that are almost all missing, and document where `issue_month` comes from and how the 500 aggregate features were built.

**What the task is**
Alfa-Bank's AlfaBattle 2.0 (2021), task 2: predict default on a credit product application from the applicant's card transactions in the year before the application. A bank's underwriting system would make this prediction at the moment of application, to approve or decline the credit. ODS states the split as "the training sample covers N days, and the test sample covers the following K days" and uses AUC. This is a genuine, high-value use case.

**Evidence gathered (200k-row sample, seed 0)**
- Columns: 514 features (500 float32, 13 int32 incl. issue_month and product, 1 categorical target). Target `default` is Yes/No with 2.77% Yes (5,530 of 200k), so roughly 26.6k positives in the full 963,811 rows. 963,811 matches the size of the competition's labelled train set.
- `issue_month` runs 0-23 and never decreases along the row order (100% monotone), i.e. it follows app_id order. That fits the organisers' time-ordered application IDs. The default rate drifts from about 2.0% (months 3-4) to 3.4% (month 21), a realistic drift that a temporal split should test.
- Leakage check: `days_before_min` is at least 1 in every row (0% are 0) and `days_before_max` is at most 359. So all transactions come strictly before the application date and cover one year. LightGBM (400 trees, default-ish settings):
  - trained on months <18, tested on months 18-20: AUC 0.760
  - trained on months <21, tested on months 21-23: AUC 0.780
  - random 80/20 split: AUC 0.774
  - `product` alone: 0.613; `issue_month` alone: 0.50.
  These numbers are in line with the public leaderboard (for example, the SlayZar solution reached 0.7766 private, 15th place). No single feature dominates: the top gains are mean amount by operation kind, daily_count_std and hour_std. I see no sign of leakage.
- Amounts look like real rubles (de-normalised): the most common `rub_min` values are 100, 1, 10 and 20; `rub_max` values cluster at 40,000, 50,000 and 200,000. The plausibility is good. A small float32 artefact remains (10000.0098 instead of 10000). The official release gave `amnt` normalised, so somebody applied an inverse transform. I could not confirm whether that was the curator or the Kaggle mirror.
- There are no exact duplicate feature rows. No column is constant.

**Concerns (most to least serious)**
1. **The table is a hand-engineered aggregation of a sequence dataset.** The original data is about 270M transaction events; the 514 columns (shares, means, block sums, a "balance" path, 30/90-day windows) were built by the preparer. A benchmark on this table measures models on one particular feature set, and the provenance must be clear. "balance_*" is not a real account balance: it is presumably a running in-minus-out sum, and `balance_mean` is negative on average (-5e5 for `balance_min`). Change: document the feature code in the README and rename or describe `balance_*` as a cumulative net flow.
2. **The provenance of `issue_month` cannot be checked.** The public target file, as I know it, has only app_id, product and flag. The month must come from app_id rank or from transaction week-of-year plus days_before. Its monotonicity in row order supports a correct construction, but the README should state exactly how it was derived. If it is an app_id quantile rather than a calendar month, say "time bucket" instead.
3. **Code columns are stored as integers.** `product` (5 levels), and `last_/mode_` of mcc, mcc_category, card_type, operation_type, city and country (up to 175 levels), are label-encoded IDs stored as int32. Change: cast them to categorical. Keep `issue_month` as the time column, not as a feature, or at least note it.
4. **Many nearly empty columns.** 281 columns have missing values; 43 are more than 90% missing (`mean_rub_operation_type_group_3` 99.95%, `mean_rub_country_16` 99.1%, many `mean_rub_card_type_*` about 98%). This is semantically correct, since the mean is undefined when the share is 0. But these columns add width with little value. Change: drop columns that are more than 99% missing, or merge rare card types and countries.
5. **Size and cost.** 963,811 x 514 is heavy for a broad benchmark. With 3 temporal windows, and about 26k positives in total, a subsample (for example 200-300k rows, keeping the time order) would still score reliably. The base rate of 2.8% is fine for AUC or log-loss.
6. **Repeat applicants.** The same customer can hold several app_ids (different products), and the transaction histories would then overlap. The temporal split limits the damage, but there is no client ID to check or group on.
7. **Licence.** This is competition data from Alfa-Bank, mirrored on Kaggle. The terms for redistribution are not stated on the pages I could reach.

**What I could not check**
- The full 963,811 rows (I used the 200k sample) and the exact split windows used by the benchmark.
- How `issue_month` was derived, and how the de-normalisation of amounts was done. The Kaggle, Boosters and ODS pages did not render their data descriptions.
- Repeat customers across train and test, since there is no client ID.
- Licence terms.

</details>

<details><summary>Precedent check</summary>

D is the definition (`dataset.py`), R the record. Register flags: none of the four flags touches this dataset (few_minority, one_feature, trivial, scaling drift). Its
register rows are CLEAN-8 (2026-10-19), CLEAN-19 (2026-10-13), USE-8 (case table) and the two open issues; I read
the cases behind each.

On the ship decision: the caller says the curator shipped it on 2026-10-15 with issues 1 and 3 left open. R has no `CC`
line of 2026-10-15 (its last curator line is the CC of 2026-10-13; the status is `WIP (DF)`, suggestion `Yes`), and I
found no local copy of that verdict. So the two open issues are still decisions the AI made and the curator has not
ratified. records.md expects a curator's verdict as a `CC` line. Worth adding when the issues are settled.

**Summary**

| # | Decision | Verdict | Closest precedents |
|---|---|---|---|
| 1 | Repeat-client filter (REVIEW issue 1; SPLIT-9 / LEAK-12) | departs from the closest same-facts precedent (ieee) **with a stated reason**; reasonable under the ranking, but the reason is an inference and the curator has not decided | ieee_fraud_detection CC 2026-10-01 (kept, 95%); hotel_booking_demand CC 2026-09-30; african_credit_scoring_challenge AI 2026-10-07 |
| 2 | No label-maturity gap (REVIEW issue 3; SPLIT-10 vs SPLIT-14) | departs from SPLIT-10 (Should) with a stated reason (the 50% floor, SPLIT-14 Must): reasonable, but **not written as an exception**; second case after lending_club | lending_club (no gap, same reason); rosbank1, sf_permit_time, brazilian_ecommerce (gap = label delay) |
| 3 | No partial gap of one month (REVIEW issue 3; SPLIT-19, SPLIT-10) | **departs without a reason**: the competition left one month unreleased, a one-month gap fits the floor, and ieee takes the competition's month | ieee_fraud_detection (gap 1, "planning gap"); zillow_prize (gap 1); SPLIT-19 |
| 4 | Two-month windows, horizon 2 (SPLIT-12, SPLIT-14, SPLIT-19) | consistent | home_credit_default_stability_1m (2-month refit windows) |
| 5 | Features: 513 top-solution aggregates (CLEAN-19, CLEAN-6, CLEAN-20) | consistent: it is the CLEAN-19 case (Lennart, 2026-10-13) | CLEAN-19 Cases row; santander (CLEAN-20) |
| 6 | Pivot codes chosen over all transactions (CLEAN-8) | consistent: it is a CLEAN-8 case (Lennart, 2026-10-19) and carries the required temporal note | rosbank1, anes_voting_2026 |
| 7 | Proxy codes to missing: `amnt` 0.0, `hour_diff` -1 (CLEAN-10) | consistent | CLEAN-10 text; the source documents both codes |
| 8 | Drop `app_id` and latest-transaction fields (LEAK-10 ids that date the issue; CLEAN-22) | consistent | african_credit_scoring_challenge `tbl_loan_id`; sdss_17 `plate`, `fiber_ID` |
| 9 | Fit `approximate` (USE-8) | consistent: the USE-8 case row is this dataset | account_debt_south_africa, kick, coffee_rating_prediction |
| 10 | Accepted warning `splits_rows_unused` | consistent | rosbank1 (accepted for rows in its label gap) |
| 11 | `horizon_unit="months"` on an int month index (info) | consistent | anes_voting_2026, apistox, college_scorecard (`years` on an int year); california, mortgage use `steps` where the index is no calendar unit |

Drift: Lennart has no decision on this dataset's split, and his gap decisions on other datasets all go one way (gap =
the label delay: brazilian_ecommerce 2026-10-15, college_scorecard 2026-10-16; sf_permit_time and rosbank1 were
implemented that way). No drift. Third exception: none yet (see decision 2: two cases of the same departure, neither
recorded as an exception).

**1. Repeat-client filter (open issue 1)**

**What D does.** It links a client's products by identical transactions (no client id in the source). From each
training side it removes every product of a client that also has a product in the test window (32,861-39,221 rows).
Why: test products whose client's earlier product defaulted default in 93.7-96.3% of cases (README decision 2), and
"that earlier flag was most likely set after the test product was issued" (D, curation_comments).

**Precedents.**

* ieee_fraud_detection, `CC (2026-10-01, Lennart)` in `curation/records/ieee_fraud_detection.md` and LEAK-34 Cases
  (`leak_checks.md`): same entity, labels carried across a temporal split, test rows whose uid had fraud in train
  "about 95% fraud", worth -0.001 to -0.007 AUC. **Kept** as "legitimate history under the host's labelling rule".
  This is the closest pair on the numbers: 95% vs 95.6%, and 0.001-0.007 vs 0.0045 AUC. It was decided the other way.
* hotel_booking_demand, `CC (2026-09-30, Lennart)` in `curation/records/hotel_booking_demand.md` and SPLIT-9 / LEAK-12
  Cases: training rows whose label was not known at the prediction point are filtered out (100% cancelled). D cites
  it.
* african_credit_scoring_challenge, `**Assessment (AI, 2026-10-07)**` and D's notes (`datasets/_dev/tabarena-v0pt2/
  african_credit_scoring_challenge/dataset.py`): credit default, repeat customers, temporal. Repeat customers are
  **kept**, `customer_id` too (citing ieee). Only labels not settled by the window start are removed, using an as-of
  date (due date + 30 days).

**Comparison.**

* Against ieee: D and REVIEW issue 1 give a distinguishing fact. In ieee the later label follows from an earlier
  reported chargeback, so the earlier label is known; here the earlier product's default most likely comes after the
  new issue. Two other facts also set it apart. (i) ieee is a feature question: `uid` is an input, under LEAK-34
  (narrows LEAK-10). alfa has no client feature at all, so this is a training-row question under SPLIT-9 (Must,
  P4), a different rule. (ii) ieee has a one-month gap, which covers part of the chargeback delay. alfa has no gap.
  So the departure has a reason, and it serves a Must of P4. Not an exception that breaks a higher Must.
* How strong the reason is: the timing claim is inference (EV-2, lowest tier). The best evidence is circumstantial: a
  bank does not issue new credit to a client already in default, and defaults move together across a client's
  products at 95%. The README decision text states it as a fact ("was not known"), while the curation bullet says
  "most likely". Also, REVIEW's claim that the earlier label is known in ieee is not shown either: chargebacks are
  reported with a delay. The two cases may be closer than REVIEW says.
* Against hotel_booking_demand: the citation is loose. Hotel filters every row by an as-of date. alfa filters by
  membership of the test window: the training side depends on which clients apply in the next two months, which a
  deployed model cannot know. It is an evaluation construction that stands in for the as-of filter, which cannot be
  built (no label dates). Defensible, but worth saying so, not "as in hotel_booking_demand".
* Against african_credit: same domain and mechanism, with a different remedy. The fact that sets alfa apart is
  written down: there are no label dates, so no maturity filter can be built.
* The effect sizes in REVIEW issue 1 (0.7774 vs 0.7729; random removal 0.7775) were measured with the old 127
  features, before the CC of 2026-10-13. They are not re-measured for the shipped 513.

**Verdict:** departs from ieee_fraud_detection with a stated reason. Reasonable under the ranking (SPLIT-9 Must, P4).
It stays an open curator call. Prompt, because a curator precedent with near-identical numbers went the other way:

```text
**Consistency check (AI, 2026-10-20):** dropping the products of a test window's clients from training (alfa, open
issue 1) differs from ieee_fraud_detection (kept 2026-10-01, the same mechanism: same-entity labels across a temporal
split, about 95% positive, worth under 0.01 AUC). What sets alfa apart?
(a) the earlier product's default is a client-level event after the new issue (a bank does not lend to a client in
default), so the training label was not known at the prediction point: SPLIT-9, recorded as the reason; also ieee
keeps a feature (LEAK-34) and a one-month gap, alfa neither; (b) treat alfa like ieee: keep the products with a
`Potential leak, kept on purpose:` note; (c) reopen ieee to match alfa; (d) change the rule: write in SPLIT-9 or
LEAK-34 when same-entity labels carried forward are history and when they are unmatured labels.
```

**2. No label-maturity gap (open issue 3, first half)**

**What D does.** No gap. D's splits_comment admits that training products of the 12 months before a window "hold
labels a deployed model would not have had yet, as in the competition", because a 12-month gap would leave 13-27% of
the rows for training.

**Precedents.**

* SPLIT-10 (Should; applies SPLIT-9): a gap of about the label's delay. Applied: rosbank1 (3 months = the label
  window; `splits_rows_unused` accepted for it), sf_permit_time (6 months), brazilian_ecommerce (1 month,
  Lennart 2026-10-15), college_scorecard (5 years, Lennart 2026-10-16), african_credit_scoring_challenge (as-of,
  settled labels only).
* lending_club (`datasets/_dev/tabarena-v0pt2/lending_club/dataset.py`, splits_comment): the same departure for the
  same reason. Unmatured labels stay in train, and "a gap of a full 36-month term would ... leave too little data".
  Its record has a curator line on the cohort (CC 2026-10-01), not on the gap.

**Comparison.** The departure has a reason: SPLIT-14 (Must, the 50% floor) outranks SPLIT-10 (Should). It is
reasonable. Two loose ends:

* It is not written as an exception. principles.md asks for `**Exception to SPLIT-10 (date, curator):** <fact>.
  Serves SPLIT-14.` in R, in the notes, and as a Cases row. lending_club is not recorded either. With alfa this is the
  second case of the same reason, so the next one triggers an amendment.
* There is an unlisted tension. SPLIT-9 is a **Must** placed before SPLIT-14 and says a row whose label is not yet
  known "must not be in train". Read literally, it wins over the floor. D's implicit reading is: SPLIT-9 targets a
  measurable shortcut (filtered, decision 1), and the diffuse rest falls under SPLIT-10 (Should). That reading is
  sensible but written nowhere. principles.md says a new tension gets a row.
* A fact to settle first (EV-1, LEAK-24 Must): the default rate rises to 3.36% in months 20-21 and dips to 3.07% and
  2.97% in months 22-23 (README decision 1). That is mild, but it is the shape probe 13 looks for. The Kaggle card
  gives "within a year" as the horizon (2026-10-07 run report). D's "no sign of right-censoring" rests on the
  competition's 7 later labelled months, which is circumstantial (EV-6, as the checklist says).

**Verdict:** departs from SPLIT-10 with a stated reason, reasonable (SPLIT-14 Must over SPLIT-10 Should). Not
recorded as an exception; second case of its kind (lending_club).

**3. No partial gap of one month (open issue 3, second half)**

**What D does.** Gap 0. splits_comment says the competition "tested on the 7 months after a month that was not
released". It explains why the 7-month windows are not followed (the floor) but not why the unreleased month is not
followed.

**Precedents.** SPLIT-19 (Should): follow the source's split. SPLIT-10: a planning gap is a gap too.
ieee_fraud_detection: gap 1 month, "the planning gap" like its competition. zillow_prize: gap 1 month.

**Comparison.** A one-month gap fits the floor. From README decision 1, months 0-16 hold about 562,000 products. Less
the window's clients (about 33,000, as with gap 0), that leaves about 529,000 of 963,811, or about 55% (estimated
from the tables, not built). So SPLIT-14 does not rule it out, and no other fact against it is written down.

**Verdict:** departs from SPLIT-19 / SPLIT-10 (Should) without a stated reason.

```text
**Consistency check (AI, 2026-10-20):** alfa splits with no gap (open issue 3), while its competition left one month
unreleased between train and test, and ieee_fraud_detection and zillow_prize take a one-month gap; a one-month gap
keeps about 55% of the rows for the oldest window (above the 50% floor). What sets alfa apart?
(a) one month removes little of a default delay of up to a year while costing the freshest month, so gap 0 is kept
and SPLIT-10's remaining departure is recorded once (decision 2); (b) treat alfa like ieee: `gap=1`, the competition's
month; (c) reopen ieee and zillow to drop their gaps; (d) change the rule: write in SPLIT-19 whether a competition's
unreleased month is a gap to follow.
```

**4-11. The other choices (consistent)**

* **Windows.** Three 2-month windows. 3-month windows would leave about 48% for the oldest train side (my sum of
  months 0-14 from README decision 1), so 2 months is the widest window above the SPLIT-14 floor. D gives the 7-month
  reason, not this one. Consistent with SPLIT-12 and SPLIT-14, and with home_credit_default_stability_1m's 2-month
  refit windows.
* **Features.** D is the CLEAN-19 Cases row (Lennart, 2026-10-13). Label encodings, embeddings and model scores stay
  out (CLEAN-6, CLEAN-20, as santander). Fixed constants (`RUBLE_SCALE`, `SALARY_RUB`) are published scales or
  thresholds, not statistics over all rows (LEAK-30: "fixed published scales are fine"; CLEAN-7 not triggered).
* **Pivot codes.** CLEAN-8 Cases row with rosbank1 and anes_voting_2026 (Lennart, 2026-10-19; extra_crosscut t0-5).
  The temporal note is present in D.
* **Proxy codes.** `amnt` 0.0 ("corresponds to missing values") and `hour_diff` -1 (first transaction, no gap
  defined) become missing: CLEAN-10, the codes documented by the source. Settled with the feature rebuild (the
  2026-10-07 issue 4 no longer stands).
* **Dropped ids.** `app_id` orders and dates the issue. It is dropped like african_credit's `tbl_loan_id` (Spearman
  0.9999 with the date) and the sdss_17 pointing ids (LEAK-10 Mechanisms row). `client_key` is split metadata
  only (LEAK-33).
* **Fit.** `approximate` matches the USE-8 Cases row (this dataset). USE-10 is met implicitly: known clients, history
  legitimate, no unmatured earlier outcome as a feature. The 2026-10-13 changelog removed the Grouped tag for the same
  reason.
* **Accepted warning.** `splits_rows_unused`: rosbank1 accepts the same warning for its gap rows. The text matches the
  design.
* **Horizon unit.** `meta_time_horizon_unit` info: calendar units on an int calendar index, as anes_voting_2026,
  apistox and college_scorecard (`years`).

**Not consistency findings, noted for the mediator**

* README decision 2 says "was not known", the curation bullet says "most likely". The two should agree (writing.md).
* R's Assessment of 2026-10-07 still says the folder uses the 127 baseline aggregates. The CC of 2026-10-13
  supersedes it (checklist, notes row).

</details>

<details><summary>Advocate</summary>

Position: ship as defined (temporal, 3 two-month windows, gap 0, repeat-client filter), with text fixes and one cheap
column fix. No finding of the panel is a validity failure that the definition leaves unfixed.

**1. A real task, scored the way the bank scores it (P3: USE-1, USE-5, USE-8 Must, all hold)**

* Evidence: Habr 551130 (Alfa-Bank): one row = one issue of a credit product, a year of card transactions, target
  "флаг дефолта по кредитному продукту"; the transaction model is "аддитивная добавка к действующим моделям". The
  practitioner: "Would I use it? Yes, as the transaction module"; AUC 0.76-0.79 (Gini 0.54-0.58) is in the range of
  real modules. The blind reviewer, without our notes: "a genuine, high-value use case", "include".
* Fit `approximate` is the USE-8 Cases row for this dataset; the unknown horizon is already named in fit_reason.
* Answers: "bureau and application inputs are missing". The source says the module is an add-on to models that hold
  them, so their absence is the design (USE-9 reasoning). Mildest remedy if wanted: the practitioner's use-case
  wording ("adds a score ... to its existing scorecards") and one clause on the population (issued products only).
  Text only.

**2. No feature crosses the prediction point (P4: LEAK-1, LEAK-2, LEAK-10 Must, hold)**

* Evidence: `days_before` is 1-359 on all 50 partitions; a card type first seen in the last 7 days is no more common
  than in days 120-300 (0.0029 vs 0.003 per day), so no post-issue card enters the window; 0 duplicate rows, 0 exact
  copies test vs kept train in all 3 splits; best single feature 0.614 against 0.708 (probe), drop-one never lowers
  the score; dropping `issue_month` changes the newest window by -0.0013 (SE 0.0029). The issue-dating fields
  (`app_id`, `latest_*`) and `client_key` are dropped. Column audit: "No column is post-issue, label-derived,
  outcome-missing or an id that encodes the label." Claim audit: the strongest attacks "all came out clean".
* This is the rank that would decide a `No`, and it holds on measurements (EV-2, first tier).

**3. The repeat-client filter is SPLIT-9 applied, and it is measured to work (P4: SPLIT-9 Must)**

* Evidence: of 169,096 earlier/later pairs, the later product defaults in 95.1% when the earlier one defaulted,
  2.28% otherwise, flat over lags of 1-10 months (94.1-95.8%); P(earlier=1 | later=1) is 0.455. A bank does not
  issue new credit to a client in default, so the earlier flag was set after the later issue: a training label not
  known at the prediction point. The filter removes the shortcut, which SPLIT-9 asks us to check: without it the
  linked test products gain +0.006 / +0.022 AUC; with it they score below the others (0.742 vs 0.762). Residual after
  the filter: 4 of about 3,640 test defaults.
* Answers the ieee_fraud_detection precedent (kept, about 95%, under 0.01 AUC). Rules win over precedents, and two
  facts set the case apart: ieee keeps a `uid` feature under LEAK-34, alfa has no client feature, so this is a
  training-row question under SPLIT-9 (Must); and the timing asymmetry above. The filter costs 60.3-83.4% training
  share, still above the SPLIT-14 floor. Concede: the README says "was not known" and the bullet "most likely"; make
  the README say "most likely" (writing fix). Curator ratification of issue 1 is still open; the argument is for (a).

**4. Gap 0 is forced by a Must and costs nothing measurable (SPLIT-14 Must over SPLIT-10 / SPLIT-19 Should)**

* Evidence: a 12-month gap leaves 13.5 / 19.9 / 26.7% for training, a 6-month gap 35-53%: both break SPLIT-14 (Must).
  At equal training size, gap 1 changes AUC by +0.0051 (SE 0.0032) and +0.0004; gap 3 by -0.0049 and +0.0001: the
  newest months carry no sharp shortcut of the hotel_booking_demand kind. The practitioner: our own out-of-time
  validation "does exactly what this split does"; one month "changes little about maturity (the issue is 12 months,
  not 1)". lending_club made the same departure for the same reason.
* On SPLIT-19 (the competition's unreleased month): the claim is unsourced (claim 51 untested, split audit problem 4),
  so it cannot carry a Should against the definition; ieee and zillow had a sourced planning month.
* Concede: the departure is not recorded as an exception (precedents, decision 2). Mildest remedy: write
  `**Exception to SPLIT-10 (date, curator):** no label dates; a horizon gap breaks the 50% floor. Serves SPLIT-14.`
  plus a `Potential leak, kept on purpose:` sentence with the measured bound (a 6-month gap lowers untuned LightGBM by
  0.014-0.015 AUC, mixing staleness). `gap=1` is an acceptable alternative (55.2% floor, no score cost) if the curator
  prefers SPLIT-19; either keeps the dataset.

**5. Right-censoring is not shown; the remedy is a sentence, not exclusion (LEAK-24 Must, EV-1, EV-6)**

* Evidence: the product-standardised default rate dips 3.53% -> 3.23% -> 3.09% in months 21-23, but single-product
  clients are flat (2.75 / 2.58 / 2.59%) and the rise and fall sit in multi-product clients, whose flag is a
  client-level event (point 3). A censored "default ever" would cut single-product clients too. The months 1-23 rise
  from 2.0% to 3.4% is the opposite of censoring. The claim audit grades it "maybe ... circumstantial both ways".
* Concede: "no sign of right-censoring" is not supported as written. Mildest remedy (claim audit): replace it with the
  measured dip and "maybe right-censoring of the newest months". LEAK-24 asks first for the fact (probe 13, two
  downloads); without it, a Must is not shown violated. If the curator wants more, the ladder's next step is the
  definition (gap or dropping the newest month), not exclusion.

**6. The features are the curator's decided build, not a defect (CLEAN-19, CLEAN-8; curator decisions)**

* Evidence: CLEAN-19 Cases row (Lennart, 2026-10-13): the aggregates the 1st, 4th and 9th place shared; pivot codes
  over all rows decided by Lennart (CLEAN-8, 2026-10-19) with the temporal note present; `RUBLE_SCALE` is right (the
  whole-ruble share peaks sharply at 17.8209: 71.9% vs 39% at +-0.00005). The curator's decision outranks an AI
  reading (precedence table). The blind reviewer's "hand-engineered aggregation" concern is answered by these records.
* Blind-review concerns refuted by measurement on the shipped frame: code columns are `category` in the container
  (column audit; the sample lost the dtype); mostly-missing `mean_rub_*` is structural and CLEAN-5 drops only constant
  and all-missing columns; width and size are no reason to drop features ("Width against model limits" tension, coad).

**7. The real problems are P7 and writing: fix them in the definition, keep the dataset**

* Concede, with the cheap fix (CLEAN-5 Should; P7 is "fixed when the fix is cheap and safe"): four exact copies,
  drop `out_sum_30d`, `mean_rub_income_flag_2`, `share_mcc_17`, `mean_rub_mcc_17` (514 -> 510 features).
* Concede, text fixes (EV-7, EV-8, writing.md): "98.8% whole rubles" (measured about 70%, 92% at relative 1e-3);
  "513 summaries" (512 aggregates); "median 5,600" (5,000; `income_flag` 3 exists, counted as spending); "less than
  half" (58% / 27% / 6%); name the LightGBM config behind 0.787 / 0.771 / 0.772 (defaults give 0.779 / 0.763 /
  0.761); "the others in 2.5%" (linked non-defaulted 2.46%, unlinked 2.69%). None changes data or a validity call.
* Value holds (P6): 108-121k test rows and 3.6-3.8k positives per window, AUC 0.76-0.79, best single feature 0.614.

Judgment record, as argued:
Verdict: ship after changes.
Validity: USE-5, USE-8 hold (approximate); LEAK-10 holds; SPLIT-9 triggered, fixed (client filter, measured);
SPLIT-14 holds; SPLIT-10 departed from for SPLIT-14 (record the exception); LEAK-24 not shown (rewrite the claim).
Value: TP holds. Quality: CLEAN-5 triggered, drop 4 copies; writing fixes listed.
For the curator: issue 1 (filter, argued for a), issue 3 (gap 0 with exception, or gap 1), weighing calls.

**Rebuttal**

The critic and I agree on the verdict (ship after changes, no exclusion) and on every remedy except the open choices
for the curator. Point by point:

**1. Right-censoring (LEAK-24): concede the note, dispute the stated effect**

* Conceded: the sentence "no sign of right-censoring" goes; "7 later months labelled" is unsourced (claim 51) and is
  cut or cited; the measured dip goes into the notes as "maybe right-censoring of months 22-23"; LEAK-24 goes to the
  curator as an open call. Conceded also that cutting months is off the table (SPLIT-14).
* Disputed: "test No rows include future defaults" is stated as the likely mechanism, but the panel's data points the
  other way. Censoring of a "default ever" flag hits every product of the newest months. Single-product clients show
  no clear dip (2.75 / 2.58 / 2.59%, claim audit); the dip sits in multi-product clients, whose rate rose to month 21
  first (3.53%) and then fell back to about the month 18-20 level. That pattern fits a client-level cluster around
  months 20-21 as well as censoring. EV-1: settle the fact before ruling. The critic's own remedy (a note plus the test
  that would settle it) is the right rung of the ladder, so the remaining difference is wording only: write "a dip of
  4-5 SE in multi-product clients, none clear in single-product clients", not "test labels partly censored".

**2. No gap: concede the missing record, keep gap 0 as the default**

* Conceded: an `Exception to SPLIT-10` line with the 6-month bound (0.014-0.015 AUC) is required (principles.md,
  Strengths: a Should departure is recorded), and the "unreleased month" claim is cited or softened (EV-7). Conceded
  that the reading "SPLIT-9 Must applies to the measurable shortcut, which the filter removes; the diffuse remainder
  falls under SPLIT-10" belongs in a Tensions row. This is the second case after lending_club, so the next one triggers
  an amendment.
* Disputed: the critic's "against the source's own design" claim. SPLIT-19 needs a source that defines the split, and
  the only source for the unreleased month is our own unsourced sentence (split audit problem 4: "consistent, not
  proven"). ieee and zillow had a sourced planning month. The reason for gap 0 is therefore: SPLIT-19 is not shown to
  apply; one month does not address a delay of up to 12 months (practitioner); gap 1 measures +0.0051 (SE 0.0032) and
  +0.0004, which is noise. `gap=1` stays an acceptable choice for the curator; neither choice affects shipping.

**3. Repeat-client filter: concede**

* Conceded in full: write "most likely" in the README with the claim-43 asymmetry (0.951 vs 0.455) as the evidence;
  call the filter an evaluation stand-in for an as-of filter rather than "as in hotel_booking_demand"; put the
  precedents.md consistency check (ieee) to the curator; re-measure the effect with the shipped features or drop the
  127-feature numbers from REVIEW. The critic keeps the filter, so this is about wording and ratification, not
  validity.

**4. Wrong numbers: concede**

* Same list as my point 7. Text fixes in `dataset.py`, no data change.

**5. Use-case wording: concede**

* Same remedy as my point 1: the practitioner's wording plus one clause on the population (issued products only).
  Fit stays `approximate`.

**6. Duplicate columns: concede**

* Drop the four copies (514 -> 510) and update the count in `known` (with the 512 -> 508 aggregates correction).

Net: no disagreement on verdict or validity. For the curator: issue 1 (filter, (a)), issue 3 (gap 0 with the
exception, or gap 1), and LEAK-24 as an open call with the wording above.

</details>

<details><summary>Critic</summary>

Position: ship only after changes. The task is real (USE-1 holds) and nothing I found is an unfixable Must, so I do not
ask for exclusion. But the definition states as settled two P4 facts that the panel's measurements do not support, and
it carries one Should departure with no reason and several wrong numbers. Most fundamental first.

**1. "No sign of right-censoring" is not what the data shows (P4; LEAK-24 Must, EV-6 Should)**

* Problem: the curation note says the rising default rate and "7 later months labelled" show no right-censoring. The
  test windows are the newest months, so if their labels are incomplete, test "No" rows include future defaults.
* Evidence: claim_audit claim 46: the product-standardised rate rises to 3.53% (month 21), then falls to 3.23% and
  3.09% (months 22-23), about 4-5 SE at ~60k rows a month; raw 3.36 -> 3.07 -> 2.97%. Single-product clients are flat
  (so the evidence is mixed, "maybe"). The flag acts as a client-level event after issue (claim 43: P(later | earlier
  defaulted) 0.951, flat over 1-10 month lags), so the newest products had the least time for it. "7 later months
  labelled" is itself unsourced (split_audit problem 4, claim 51 untested). precedents.md: the Kaggle card gives
  "within a year" as the horizon.
* Effect: the newest test window may score against a partly censored label; the bias is unmeasured.
* Remedy (note, not exclusion; no settled archive exists and cutting months would break SPLIT-14): replace the sentence
  with the measured dip as "maybe right-censoring of months 22-23", name the test that would settle it (labels from a
  later extraction), and put LEAK-24 to the curator as an open call.

**2. No gap, against the source's own design and without a written reason (P4; SPLIT-19 and SPLIT-10 Should, under SPLIT-9 Must)**

* Problem: splits_comment says the competition tested after an unreleased month, yet uses gap 0 and gives no reason.
  The departure from SPLIT-10 (12-month maturity) is reasoned (SPLIT-14 floor) but not recorded as an exception, and
  the SPLIT-9 Must vs SPLIT-14 Must reading is written nowhere.
* Evidence: split_audit problem 1: gap 1 keeps 77.6 / 67.0 / 55.2% for training (floor holds) and changes AUC by
  +0.0051 (SE 0.0032) / +0.0004; a 6-month gap costs 0.014-0.015, an upper bound on maturity optimism. precedents.md
  decision 3: ieee_fraud_detection and zillow_prize take a one-month gap; decision 2: second unrecorded case after
  lending_club.
* Remedy: `gap=1` in `SPLIT_WINDOWS` and `Temporal`, or a stated reason for gap 0; in either case an
  `Exception to SPLIT-10` line with the measured 6-month bound, and cite or soften the "unreleased month" claim (EV-7).

**3. The repeat-client filter is stated as fact and not ratified (P4; SPLIT-9 Must, EV-6 Should, precedent consistency)**

* Problem: README decision 2 says the earlier flag "was not known"; curation_comments says "most likely". The closest
  curator precedent (ieee_fraud_detection, ~95% same-entity concordance, kept) went the other way; the record has no CC
  on this choice. The hotel_booking_demand citation is loose: here the training side depends on which clients apply in
  the test window, which a deployed model cannot know.
* Evidence: precedents.md decision 1; split_audit problem 2 (filter removes the shortcut: without it +0.002 / +0.009
  AUC; residual links negligible, claim 44/50/58). REVIEW_before effect sizes used the old 127 features.
* Remedy: I do not ask to remove the filter (the measurements back it). Align the wording to "most likely" with the
  claim-43 asymmetry as the evidence, call it an evaluation stand-in for an as-of filter, and put the precedents.md
  consistency check to the curator.

**4. Wrong or unreproducible numbers in the definition (procedure; EV-7 Must, EV-8 Should, writing.md)**

* 98.8% whole rubles: measured 70-79% (claim 18; column_audit 66-71%). 513 summaries: 512 aggregates plus `product`
  (claims 5/67). Inflow median 5,600: measured 5,000, and an undocumented `income_flag` 3 counts as spending (claim 19).
  "Less than half" for 7-month windows: 58 / 27 / 6% (claim 52). Untuned LightGBM 0.787 / 0.771 / 0.772: defaults give
  0.779 / 0.763 / 0.761, so the config must be named (claim 32). "The others in 2.5%": that is linked-not-defaulted,
  unlinked is 2.69% (claim 42).
* Remedy: correct each in `dataset.py` text; no data change.

**5. Use-case wording omits the module's place and population (P3; USE-9 Should, writing)**

* Practitioner: Habr 551130 says the transaction model is an additive supplement to existing bureau and application
  scorecards, and the rows are issued products only (no rejects). The current use_case reads as if transactions alone
  decide. Remedy: reword use_case and row as the practitioner proposes; fit stays approximate.

**6. Four exact duplicate columns (P7; CLEAN-5 Should)**

* column_audit problem 2: `out_sum_block_0` = `out_sum_30d`, `mean_rub_income_flag_2` = `in_mean`, `share_mcc_17` =
  `share_mcc_category_15`, `mean_rub_mcc_17` = `mean_rub_mcc_category_15`, identical on all 963,811 rows. Quality
  only, not a reason to hold the task. Remedy: drop one of each in `aggregate_transactions` (514 -> 510 features) and
  update the count.

Dropped for lack of support: licence (EV-4, never a verdict reason); clean-room's "drop >99% missing columns" and
"subsample" (CLEAN-22, width and cost are no reason); `issue_month` as a feature (drop-one -0.0013, SE 0.0029).

**Rebuttal**

We agree on the verdict, "ship after changes", and on most of the remedies. Two points stay in dispute; neither is a
reason to exclude.

**Advocate 1 (real task, USE-1/5/8 hold): concede**

My point 5 asked only for text; the advocate offers the same wording and the population clause. Settled as a text fix.

**Advocate 2 (no feature crosses the prediction point): concede**

I raised no column leak. The measurements (days_before 1-359, no late new card, 0 copies across the split) stand.

**Advocate 3 (repeat-client filter): concede on substance**

I did not ask to remove the filter. The advocate concedes the "most likely" wording, and the fact that the curator
has not ratified it. The distinguishing facts against ieee (no client feature, the claim-43 asymmetry) answer
the consistency check, but the curator still has to record them (principles.md, "Consistent judgement"). One thing is
still open: the hotel_booking_demand citation should say the filter stands in for an as-of filter, which cannot be
built here (precedents.md decision 1). This is text only.

**Advocate 4 (gap 0 forced by SPLIT-14): dispute in part**

* Concede: a 12- or 6-month gap breaks SPLIT-14 (Must), so SPLIT-10 cannot be met in full; the exception line plus
  the measured 0.014-0.015 bound is the right record.
* Dispute: the advocate argues that the unreleased month is unsourced and so cannot carry SPLIT-19. Then the
  definition must not assert it. splits_comment states it as a fact ("tested on the 7 months after a month that was
  not released"). Under EV-7 (Must), it is cited, softened or removed. If it stays, SPLIT-19 (Should) applies, and
  the advocate gives no fact against `gap=1`: it keeps 55.2% (SPLIT-14 holds) and costs nothing (+0.0051, SE 0.0032).
  The ranking leaves two consistent outcomes: (a) cite the month and set `gap=1`; (b) remove the claim and keep gap 0
  with the exception. Keeping gap 0 and the claim together is not one of them. This is the curator's call between
  (a) and (b).

**Advocate 5 (right-censoring not shown): dispute the reading, agree the remedy**

* The advocate says a censored "default ever" would also cut single-product clients. That does not follow from
  the advocate's own point 3. The flag behaves as a client-level event, and multi-product clients have more products
  that can carry it. So censoring at the extraction date would show first and most in multi-product clients, which
  is where the dip is (claim 46). The data does not separate the two readings: the dip is "maybe right-censoring" (EV-6,
  Should). It is neither "not censoring" nor "no sign".
* Agree: LEAK-24 is not shown violated without a second extraction (EV-1). The remedy is the measured sentence and an
  open LEAK-24 note for the curator, not exclusion.

**Advocate 6 (features are the curator's decided build): concede**

I raised no point against CLEAN-19 or CLEAN-8 and dropped the blind-review width and missingness points myself.

**Advocate 7 (CLEAN-5 copies, text fixes): concede**

The remedies are the same as my points 4 and 6.

Remaining for the curator: issue 3 as (a) or (b) above; issue 1 ratified with its distinguishing facts; the LEAK-24
note.

</details>
