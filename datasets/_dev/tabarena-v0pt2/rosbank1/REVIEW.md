# rosbank1

**Outcome:** added. Churn after the three-month introductory period of a Rosbank card (task 1 of the bank's 2018
competition), one row per client from its card transactions, tested on the clients whose period ends in October,
November or December 2017 after a three-month label gap. Verdict: ship; the panel's text changes are made in the definition.
Validity: USE-5 holds; fit approximate (USE-8) (how the label window was placed is not published; a test on the data
found no sign of a window fixed in calendar time), LEAK-10 holds (107 of the 479 clients with a card purchase more than three months after their first transaction still count as churned, so the file holds no transactions from the label window), LEAK-24 holds (periods ending from 2018 on are
cut), SPLIT-1, SPLIT-9 and SPLIT-10 hold. Value: TP-3 `no_spread` kept (three windows cannot separate model
families). Quality: the features depart from CLEAN-19 and the alfa_battle_2_0_task_2 precedent (issue 5), CLEAN-21 is not met for
mixed currencies (issue 7), CLEAN-8 accepted (Lennart, 2026-10-19). Weighed: source +, real use case +, drift +, small
test windows -, card transactions only -. For the curator: issue 1, the target; issues 5 and 7, two quality calls.

**Main points:** Keep churn as the only target (issue 1)? Keep the CoLES baseline features or search for the top
solutions as for alfa (issue 5)? Keep, filter or convert the mixed currencies (issue 7)?

**Issues for Lennart:**

1. **Churn only, or also a folder for the spend target?** The competition had two tasks on the same 5,000 clients:
   task 1, churn (no card purchase at a shop terminal, POS, in the three months after the period), and task 2, the
   amount of POS spend in those three months (`target_sum`). Churn is exactly `target_sum` = 0, so the two targets
   carry one signal.
   Effect on the task: a regression of spend over all clients is mostly the churn task again (44.8% of the targets
   are zero), and a second folder with a swapped target of the same rows is a duplicate (PROV-6, Must;
   arsenic_male_lung). The spend of the 2,645 clients who kept buying would be a task of its own (PROV-7, parkinsons:
   one source, two tasks), but two of its three test windows hold 40 and 74 clients, and the mediator's test shows spend relative to the period's spend rising with
   the cohort (0.28 to 0.61 in channel type1), so the amount's window is less certain than the churn flag's.
   Implemented: churn only, the task CoLES and pytorch-lifestream benchmark (USE-5). Alternative: a `rosbank1_reg`
   folder on the retained clients' spend; cost: tiny test windows, an uncertain label window and a second folder of
   the same clients. Neither the advocate nor the critic argued for it.
   Recommendation: churn only. Decision: churn only, or add a retained-spend folder with the note that its label window is less certain than the churn flag's?

5. **Features: keep the CoLES baseline, or build what the top solutions share, as for alfa_battle_2_0_task_2?** The
   features are the hand-crafted aggregates of the CoLES paper (Babaev et al. 2022, a benchmark of models on bank transaction sequences) as pytorch-lifestream configures them for this data:
   counts, means and standard deviations of the amounts per transaction category, currency and merchant category code
   (MCC, the 97 most frequent). CLEAN-19 (Should) asks that a transaction log be built into the features a data
   scientist on this task would build, which are the features the top solutions share. For alfa_battle_2_0_task_2, a
   bank competition on the same platform with the same kind of data, you replaced the organizers' baseline with the
   top solutions' features, 30 MCC codes among them (CC 2026-10-13). No search for rosbank1's top solutions is on record (the two GitHub repositories
   the definition names are copies of the data, not solutions).
   Effect on the task: not measured. The only comparison, 30 against 97 MCC codes (0.863 against 0.860 AUC, inside window standard errors of 0.02 to 0.04), tests the number of codes, not a top-solution feature set.
   Implemented: the CoLES baseline, a peer-reviewed tabular baseline for this data. Alternatives: (a) keep it as an
   exception to CLEAN-19 once a documented search of the 2018 write-ups and participant code finds no published
   solutions (cost: the search); (b) rebuild like alfa from what the top solutions share (cost: the search, a rebuild
   and a new review). The advocate holds that CoLES is peer-reviewed; the critic answers that this is not the fact alfa
   lacked and that the search must be written down first. As it stands, the definition departs from the alfa precedent
   without a fact that sets it apart.
   Recommendation: search the 2018 write-ups and participant code first; if none are published, keep CoLES as an exception to CLEAN-19 with that fact, otherwise rebuild like alfa. Decision: agree, or rebuild like alfa now?

7. **Mixed currencies in the amount statistics: keep, use rubles only, or convert?** `amount` is in each
   transaction's own currency, so `amount_sum`, `amount_mean`, `amount_std` and the per-category and per-MCC means add
   rubles, euros, Vietnamese dong, Indonesian rupiah and others as if they were one unit. CLEAN-21 (Should) asks for one
   unit per column, converted at the rate the source publishes; kickstarter converts its goals with the source's own
   rate, but this release has no rate.
   Effect on the task: 1,072 clients (22.4%) have a non-ruble transaction and for 92 of them `amount_sum` is mostly
   non-ruble; the largest amounts in the file are dong and rupiah, up to 35.8 million, so a traveller's spend looks
   far larger than it is. The effect on scores was not measured; the per-currency columns keep the currencies apart.
   Implemented: mixed, as in CoLES, now stated in the "Anomaly" note. Alternatives: (a) keep, recorded as an exception
   to CLEAN-21 (fact: the source has no rate; cost: the overall amount columns stay in mixed units); (b) compute the overall statistics over ruble transactions
   only (cheap and from the source; cost: departs from the CoLES layout); (c) convert at the Bank of Russia's daily
   rate of the transaction date (cost: data from outside the source and a pinned rate file).
   Recommendation: (b), a cheap and safe fix of a P7 problem (principles, "How to decide", step 3). Decision: (a), (b)
   or (c)?

**Review panel:** ship after changes (mediator). Claim audit: most claims hold; refuted were the label
timing for the newest clients, two source attributions (the label quote and the meaning of `channel_type` come from a
participant notebook), the CoLES sentence and stale `no_spread` numbers, all fixed in the text. Blind review: include
with changes; main concern the undocumented label definition. Agreed: no leak, the temporal split with its gap, the
cut at 2018, the text fixes. Settled by the mediator: whether the label uses one calendar window (a test on the data
found no cohort-age effect in channel type1, so rewording is enough). To the curator: the mediator's issues 1, 2 and 3
are this file's issues 1, 5 and 7; the panel settled the random split, the time column, the 2018 cut and the small windows as notes.

<details><summary>Mediator</summary>

**Recommendation**

```text
Verdict: ship after changes.
Validity: SEL holds (CoLES wording fixed); USE-5 holds, USE-8 approximate (label window's timing unpublished, now
  stated; EV-1 run: no calendar-window signature in type1); LEAK-10 holds (107 of 479 post-day-92 POS buyers churned);
  LEAK-24 holds (cut C); SPLIT-1/7/9/10/14/17 hold; SPLIT-20 noted; PROV-13 holds; EV-2/PROV-16 attributions fixed.
Value: TP-3 `no_spread` kept (3 windows; numbers refreshed).
Quality: CLEAN-19 departs from alfa (curator); CLEAN-21 currency mix (curator); CLEAN-8 accepted (Lennart, 2026-10-19);
  CLEAN-22 width argument dropped.
Weighed: source +, real use case +, drift +, test windows small -, inputs narrow (card transactions only) -.
For the curator: issue 1, the target choice (optional second folder); issue 2, CLEAN-19 against alfa;
  issue 3, CLEAN-21 currency.
```

**The disputed point, settled: does the label use one calendar window? (EV-1, then USE-5)**

The critic said that if the label's window is fixed in calendar time, "churn" means something different for each
cohort, and the dates carry cohort age. The advocate said rewording the text is enough. Both agreed that EV-1 decides.
The measurement, on the 4,791 kept clients:

| channel | churn 2017 Q1 / Q2 / Q3 / Q4 | logit slope per month of cohort age (boot SE) | with activity controls* |
|---|---|---|---|
| type1 (3,216, 67%) | 0.590 / 0.570 / 0.569 / 0.544 | +0.020 (0.012) | +0.006 (0.013) |
| type2 (1,397) | 0.252 / 0.162 / 0.147 / 0.101 | +0.118 (0.026) | +0.113 (0.032) |

*log transactions, log recency, log span.

* With a calendar window, a January 2017 cohort would sit about 12 months further from that window than a December one,
  and churn would rise with cohort age in every channel. In type1, two thirds of the rows, it does not (slope at zero
  once activity is controlled). The type2 slope fits the documented acquisition drift as well as it fits cohort age.
* The residuals of a date-free LightGBM (out of fold) by quarter are flat within type1 (-0.016 to +0.038) and type2
  (+0.080 in Q1, then -0.029 to +0.008). Without the dates, the shipped split scores 0.851 against 0.860 (split audit),
  so the dates add little, and that little need not be cohort age.
* Not settled: among non-churners, target_sum divided by the period's POS spend rises with the cohort in both channels
  (type1 0.28 to 0.61, type2 0.68 to 0.84). This fits a calendar-anchored *amount* or a rising trend in spend. It does
  not move the binary label (churn is flat in type1). It matters for the spend regression (issue 1), not for rosbank1.
* The 63 clients of April to June 2018 remain unexplained: the 37 non-churners have short histories (median span 48
  days) but full spend labels. Nothing published says how the window was placed.

Result: the critic's condition ("if the calendar reading holds, fit_reason must say the gap and the dates carry cohort
age") is not met for the churn label. The advocate's remedy, rewording plus recording this test, is enough. This is
change 1 below. No other point stayed disputed: both rebuttals concede the rest and ask for the same remedies.

**Changes to make now (no decision needed)**

1. **Label timing (USE-8, EV-1, EV-2, LEAK-24):**
   * Rewrite the "Cohort" bullet, the text of Decision 2 and the comment on `LABELS_COMPLETE_BEFORE`. Base them on the
     measured March 2018 anomaly (24 of 36 churned) and on a label construction that is not published, not on the claim
     "data ends 2 Apr, labels published 27 Apr". Keep cut C.
   * Start `fit_reason` with: "how the label window was placed is not published, and the newest rows contradict 'after
     the period'".
   * Record the EV-1 result: type1 churn flat with cohort age (slope +0.006 ± 0.013 per month, with activity
     controls).
2. **"Time" bullet (LEAK-10, SPLIT-9, SPLIT-10):** add two facts:
   * The estimate `max(last, first + 3 months)` is an upper bound of the true period end for the clients at first + 3
     months, so it errs on the safe side for the gap.
   * 107 of the 479 clients with a POS purchase after first + 3 months still churned, so the transactions in the file
     are not in the label window.
3. **Attributions (EV-2, PROV-16):**
   * Cite "Значение 0 соответствует отказу" as the kianya participant notebook, not the task text (record assessment
     of 2026-10-07).
   * Write `channel_type` as "undocumented; constant per client, read as the acquisition channel" in `known` and in
     curation_comments.
4. **CoLES sentence (SEL scope wording, EV-2):** replace "not clearly beaten by sequence models" with: 0.825, level with
   the supervised sequence model (0.817), above CPC/RTD/SOP (0.782 to 0.802), and below CoLES embeddings + LightGBM
   (0.843). Fix this in the definition and in the record.
5. **`splits_comment` and `use_case` (SPLIT-20, SPLIT-1, USE-1):**
   * Add a note on the client intake drop after July 2017.
   * Add the share of estimated period ends per window: 11% / 29% / 38%.
   * Add that every test label window spans the New Year and no training label window does.
   * Reword "stricter" so it applies to the design only: IID 3 x 3 scores 0.817 against 0.860 for the shipped split,
     and a random training side on the same test windows scores about 0.01 higher.
   * Write "for example" before the monthly refit.
6. **Stale probe numbers (TP-3, writing.md):** replace `no_spread` "0.045 AUC, SE 0.036" with "0.017 AUC, skill gap
   0.034, paired SE 0.087". Do this in curation_comments and in the TP-2 Cases row (`task_probes.md` line 310).
7. **Currency facts (CLEAN-21, accuracy only):** the "Anomaly" bullet adds that 1,072 clients (22.4%) have a non-ruble
   transaction, and that the top amounts are VND and IDR, up to 35.8 million. The remedy itself is issue 3.
8. **REVIEW.md:**
   * Issue 2 (IID): close. SPLIT-1 and SPLIT-7 (Must) beat SPLIT-19 (Should); forest_fires tension.
   * Issue 3 (time column): close with the upper-bound note.
   * Issue 4 (cut B or C): close. Cut C stays (LEAK-24), and cut B rests on a draw date that the data contradicts.
   * Issue 6 (small windows): close as a note.
   * Issue 5: correct the precedent. alfa *replaced* its organizers' set. Drop the width argument (CLEAN-22, coad).
   * Carry issues 1, 2 and 3 below.

**Issues for the curator, ranked**

1. **Target: churn only, or also a spend folder (P3/P5; USE-5, PROV-6, PROV-7).**
   * Problem: REVIEW issue 1 offers `rosbank1_reg`.
   * Effect: regressing over all clients is the churn task again: 44.8% zeros, and PROV-6 makes it a duplicate
     (arsenic_male_lung). Spend of the 2,645 retained clients would be a distinct task (PROV-7), but:
     * two of its three windows hold 40 and 74 test clients;
     * EV-1 shows target_sum relative to period spend rising with the cohort, so the amount's window is less certain
       than the flag's.
   * Both sides: neither argued for the spend folder; both keep churn.
   * Decision: churn only (recommended), or add a retained-spend folder with that note.
2. **Feature set against the alfa precedent (P7; CLEAN-19 Should).**
   * Problem: rosbank1 ships the CoLES/ptls baseline. alfa_battle_2_0_task_2 (CC 2026-10-13) replaced its baseline
     with what the top solutions share. No search for rosbank1's top solutions is on record.
   * Effect: small. 30 against 97 codes differ by 0.003 AUC, within noise.
   * Advocate: CoLES is a peer-reviewed baseline. Critic: that is not the fact alfa lacked; the search must be written
     down first.
   * Settles it: a documented search of the 2018 write-ups.
   * Decision: (a) an exception to CLEAN-19 once the search finds no published solutions; (b) rebuild like alfa;
     (c) reopen alfa; or (d) amend CLEAN-19.
3. **Mixed currencies (P7; CLEAN-21 Should).**
   * Problem: overall amount statistics add rubles, euros, VND and IDR.
   * Effect: 22.4% of clients are touched, and 92 have an `amount_sum` that is mostly non-ruble. Trees are largely
     robust.
   * Both sides: P7, the curator's call. The release has no exchange rate, unlike kickstarter.
   * Decision:
     * (a) keep, recorded as an exception (fact: no rate in the source; the per-currency columns keep the rest);
     * (b) compute the overall statistics over ruble transactions only (cheap, from the source);
     * (c) convert at the Bank of Russia's daily rate (outside data).

**Agreed facts**

* train.csv is byte-identical to the 2018 GitHub copy (sha256 cd19fe25...e392): 490,513 transactions of 5,000 clients.
  Competition 27 Apr to 28 May 2018, AUC and RMSE. target_flag == (target_sum > 0) on all 5,000 clients.
* No leak:
  * 107 of 479 post-day-92 POS buyers churned;
  * the post-period POS sum has r = -0.02 with target_sum;
  * cl_id adds nothing beyond the features and is dropped;
  * 0.0% exact copies across the split;
  * the largest drop-one is -0.020 (`channel_type`).
* Split: 3 monthly windows with a 3-month gap equal to the label window.
  * Test windows 63 / 123 / 515 clients against 3,566 / 3,078 / 2,559 in training.
  * Churn drifts from 53.0% to 35.8% by quarter, and type2 grows from 17% to 41%.
  * Shipped split 0.860, gap cost about 0.007, IID 3 x 3 0.817.
* Probes: LightGBM AUC 0.859, skill 0.718, beats the dummy on 3/3 windows, smallest class 23. `no_spread` (gap 0.034,
  SE 0.087).
* The label quote and the meaning of `channel_type` come from a participant notebook. The boosters API has no file
  descriptions.
* The 63 clients of April to June 2018 have labels that a per-client window after the period could not produce by the
  opening. March 2018 churn is 24/36.
* EV-1 (this report): type1 churn shows no cohort-age effect; type2 falls with the cohort (drift). The spend ratio
  rises with the cohort.

**Consistency with precedent**

* Followed:
  * sf_permit_time (LEAK-24 cut; SPLIT-10 gap = delay) and brazilian_ecommerce (gap);
  * forest_fires (the split over the score);
  * alfa_battle_2_0_task_2 (USE-8 approximate);
  * coad (CLEAN-22: the width argument dropped);
  * CLEAN-8 (rosbank1's own case);
  * heart_disease_cleveland, electric_motor_temperature_prediction, african_credit_scoring_challenge (`no_spread`
    kept);
  * arsenic_male_lung (PROV-6, issue 1).
* Set apart by a fact: mutual_funds_india and iranian_churn (LEAK-10). Here the post-day-92 transactions are measured
  to lie outside the label window (107/479 churners), so no cut is needed.
* Departures without a fact, for the curator: alfa_battle_2_0_task_2 on CLEAN-19 (issue 2) and kickstarter on CLEAN-21
  (issue 3).
* No third exception of one kind.

</details>

<details><summary>Claim audit</summary>

Scope: `dataset.py` (D), the record (R). Data: the definition's frame and splits (4,791 x 348, 3 splits); the raw
train.csv.gz; the HF `test.csv.gz` (pinned revision) and the kianya GitHub `data/train.csv`; the boosters API JSON;
CoLES (arXiv 2002.08232, HTML); ptls-experiments `agg_feature.yaml`, `make-datasets-spark.sh` and
`ptls/make_datasets_spark.py`. Untuned LightGBM (300 trees, 15 leaves) on the shipped 3 windows; numbers are
probe-grade (EV-8), not leaderboard numbers.

**Table**

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 25, 45, 52, 4 | Label = no POS purchase in the three months *after the period* | D curation_comments "Task"; D `_decisions`; R | Clients whose reconstructed period had not ended when the file ends (period_end Apr-Jun 2018, first transaction Jan-Mar 2018, 63 clients): under this definition their label windows lie after 2 Apr 2018 (to Sep 2018), so they must be censored to churn | **refuted for these clients** | 37 of 63 are non-churners with target_sum median 121,887 (all non-churners: 76,081), a full spend no window after their period could have produced by the opening (27 Apr 2018); churn 41% vs 37% base (binomial p = 0.51). target_flag == (target_sum > 0) itself holds on 5,000 clients | USE-5, LEAK-24, EV-1 |
| 20, 31, 46 | Censoring mechanism: transactions end 2 Apr 2018, labels published 27 Apr, so periods ending from Jan 2018 cannot have complete labels; March 2018 churn shows it | D LABELS_COMPLETE_BEFORE comment; curation_comments "Cohort"; Decision 2 | Churn by period_end month after Dec 2017 should rise monotonically if labels were cut by one draw date | **partly refuted** | Mar 2018 24/36 = 66.7% (p = 0.0002 vs 35.5%) holds; but Jan 29.0%, Feb 39.6%, Apr 32%, May 44%, Jun 54% (25/25/13 clients): no monotone censoring; the calendar argument (data end vs opening) does not explain the rows. "Labels in train.csv at opening" is inference (API lists no files; the file we have is the Oct 2018 GitHub copy) | LEAK-24, EV-2, EV-6 |
| 30, 49, 7, 9 | period_end = max(last, first + 3 months) estimates the period end | D curation_comments "Time"; Decision 5 | (a) churners must have no POS after a true period end if the label window follows it; (b) recent clients above | holds as an approximation, errs late | 107 of 479 clients with POS after first + 3 months churned (so post-t3 POS is not inside the label window: the leak reading fails); the 63 recent clients imply period starts before the first transaction for some clients, so the estimate is late, which is conservative for the gap and the cut | SPLIT-1, USE-8 |
| implied | Every feature is known at the prediction point | D `aggregate_transactions` | Overlap of feature transactions with the label window: churn among clients with POS in each calendar month, and by days from last POS to period_end | holds (no overlap found) | No calendar month has churn near 0 among its POS buyers (min 17.9%, Oct 2017); last POS 0-7 days after first + 3 months: churn 9-14%, not 0 | LEAK-10, USE-3 |
| implied | No row is a copy across the split | probes | Exact duplicate client rows and their period_end | holds | 2 pairs (rows 948/949, 1466/1467), period_end 2017-03-05 and 2017-03-28, both in train of all 3 windows; probe 0.0% copies | LEAK-16..21 |
| implied | The split is the one the use case needs | D temporal | Train max period_end vs test window start | holds | Dec window: train <= 2017-08-31, test 2017-12-01..30; Nov: <= 07-31; Oct: <= 06-30 (exact 3-month gap) | SPLIT-9, SPLIT-10, LEAK-12 |
| 40 | Windows 63/23, 123/49, 515/179; train 3,566/3,078/2,559 | D splits_comment | Recount from the loaded splits | holds | identical | - |
| 41 | Sep window 44% of rows; two-month windows leave one above the floor | D splits_comment | Recount | holds | Sep: 2,131/4,791 = 44.5%; 2-month windows from Nov 64.2%, Sep 44.5%, Jul 32.6% | - |
| 44 | 524 clients of Sep 2017 fall in every gap | D accepted warning | Recount | holds | 524 | - |
| 3 | 4,791 clients | D row | Recount | holds | 4,791 | - |
| 31 (numbers) | 24/36 Mar; 35.5% Oct 2017-Feb 2018 | D curation_comments | Recount | holds | 0.3551 on 811 | - |
| 47 | Churn falls, type2 rises | D Decision 3 | By quarter | holds | churn 0.530/0.446/0.406/0.358; type2 0.170/0.272/0.374/0.409 | - |
| 33 | cl_id carries the label (alone AUC 0.728) | D curation_comments | AUC of cl_id; LightGBM with and without cl_id | holds, and redundant | AUC 0.7285; +cl_id 0.850 vs 0.858 without: no signal beyond the features. Note: the shipped rows are in cl_id order, so row position alone scores 0.728 | LEAK-10 (dropped correctly) |
| 36 | `no_spread`: LightGBM leads linear by 0.045 AUC, paired SE 0.036 | D curation_comments "Note" | Today's task probe | **refuted (stale)** | probe: AUC 0.859 vs 0.842 (0.017), skill gap +0.034, paired SE 0.087 | TP-3, EV-8, writing.md |
| 26, 53 | CoLES Sec. 4.1.2: aggregates 0.825, "not clearly beaten by sequence models"; sequence models 0.817-0.843 | D curation_comments; R | Read CoLES HTML Tables 6-7 | **partly refuted** | Designed features 0.825 +- 0.004; CoLES embeddings + LightGBM 0.843 +- 0.003 (Table 6), about 4.5 SD above; the range omits CPC 0.802, RTD 0.801, SOP 0.782 (Table 6). Holds for end-to-end supervised (0.817) and fine-tuned (0.810-0.827) | SEL (scope), PROV-16 |
| 16, 18, 27 | ptls config: count/mean/std per value; 7 categories, 1 currency, 97 MCC | D comment; curation_comments | Read agg_feature.yaml and the ptls encoder | holds | `trx_category in: 10`, `currency in: 4`, `mcc in: 100`; encoder codes start at 2 (`row_number + 1`), index 0 masked, top index clamps the rest: 7 / 1 / 97 own values. ptls also aggregates channel_type per value (D makes it one column: a documented deviation) | - |
| 28 | Top-97 MCC over all rows is a label-free pipeline choice | D curation_comments | Top-97 on training-only cohorts | holds, negligible | differs by 3, 2, 1 codes for train cohorts before Jul, Aug, Sep 2017 | LEAK-27..31 (accepted 2026-10-19) |
| 5, 29 | channel_type is how the client was acquired | D known; curation_comments | Boosters API, HF card | untested at source rank; third-party only | Neither the API nor the HF card defines the column; the meaning ("канал привлечения клиента") is in a participant notebook (kianya), EV-2 rank 4 | EV-2, EV-7 |
| 52 | "Значение 0 соответствует отказу" is "the task text" | R assessment | grep the boosters API JSON | **refuted as attributed** | Not in the API task text; it is in the kianya participant notebook, maybe copied from the data page (unreachable) | EV-2, PROV-16 |
| 19, 50 | "3 months of privileged usage", "next three months of usage of the product" | D constants; R | API `information_en.descriptionfull`, `tasks[].about` | holds | quoted verbatim | - |
| 12, 15 | Competition 27 Apr - 28 May 2018; AUC / RMSE; page is JS fed by the API | D download_description | API `date_start`/`date_end`, `tasks[].metric` | holds | 1524787200000 = 2018-04-27, 1527465600000 = 2018-05-28; metrics AUC, RMSE | - |
| 13 | Decompressed train.csv byte-identical to kianya/rosbank-competition | D download_description | sha256 of both | holds | both cd19fe25...e392, 33,672,402 bytes (Ikitan copy not re-checked) | PROV-13 |
| 14 | 490,513 transactions of 5,000 clients; test.csv.gz 518,376 / 5,217, no labels | D download_description | Load both | holds | as stated; test has no target columns | - |
| 43 | The competition's test file covers the same months | D splits_comment | period_end months of test.csv.gz | holds | test clients per month track train (e.g. Oct 2017 523 vs 515; cl_ids interleave, test share 0.49-0.53 per decile) | SPLIT-5 |
| 34, 35 | 2.6% non-ruble; 828 duplicate transaction rows | D curation_comments | Recount | holds | 0.0262; 828 | - |
| 17 | 810/978/840 = RUR/EUR/USD | D constant | ISO 4217 | holds | - | - |
| 30 (dates) | POS carry a date only | D curation_comments | Share of POS with a time | holds | 1.6% of POS rows have a time of day | - |
| 2, 38 | Model refit every month | D use_case, splits_comment | Source | untested: our framing, not the source's | not in API or HF card; written without "for example" | USE-1, EV-2 |
| 12 (Yandex) | Earlier Yandex Cloud zip, now removed | D download_description | - | untested | not fetched | EV-7 |

Additional measurement (not a claim): recency and span derived from the shipped dates add about 0.02 AUC
(0.858 -> 0.879 mean over the 3 windows; dropping the dates 0.854). Legitimate when period_end is the prediction point;
it means the estimated period_end carries signal, so its error is part of the task.

**Refuted and untested, ranked (principles.md: validity first, Must first)**

1. **P3/P4, USE-5 and LEAK-24 (Must): the label's timing is not what the definition says for the newest clients.**
   37 of the 63 clients whose period was still running when the transactions end have full positive spend labels
   (median 121,887), and churn after December 2017 is not monotone (Jan 29%, Feb 40%, Mar 67%, Apr-Jun 41%). So
   either the label window is not "the three months after the period" or the period does not start at the first
   transaction; the calendar argument for the cut (data end 2 Apr vs opening 27 Apr) does not explain the rows, and
   REVIEW issue 4 (cut B vs C by draw date) is framed on that premise. What it changes: the shipped cohort keeps its
   cut, which is conservative in every reading (the period_end estimate errs late), and the kept months show no
   censoring signature; the risk is that the target's real-world meaning for 2017 rows is less certain than stated.
   Mildest remedy: keep the cut; rewrite the "Cohort" bullet, Decision 2 text and the LABELS_COMPLETE_BEFORE comment to
   rest on the measured March anomaly and an unknown label construction, add "how the label window was placed is not
   published and the newest rows contradict 'after the period'" to fit_reason, and replace issue 4's draw-date
   framing.
2. **P2/P5, PROV-16 and EV-2 (Must): source attributions.** The label quote "Значение 0 соответствует отказу" and the
   meaning of channel_type ("how the client was acquired") come from a participant notebook, not the task text or a
   primary document. Remedy: cite them as third-party (kianya notebook) or write "not stated".
3. **P2 scope wording (CoLES):** "not clearly beaten by sequence models" overstates: CoLES embeddings + LightGBM
   0.843 +- 0.003 vs 0.825 +- 0.004 (Table 6). Does not change the tabular framing (end-to-end supervised 0.817).
   Remedy: "beaten by 0.018 by CoLES embeddings fed to LightGBM, level with the supervised sequence model (0.817)".
4. **P6, TP-3 / writing.md: stale `no_spread` numbers** (0.045 AUC, SE 0.036 vs today's 0.017 AUC, skill gap 0.034,
   SE 0.087). Remedy: update the bullet from the current probe.
5. **P3, USE-1 (untested):** "refit every month" is our framing; write "for example".
6. **Procedure (untested):** Yandex Cloud removal and the Ikitan byte match not re-checked (EV-7).

No refutation reached a leak: the post-period transactions are not in the label window (107/479 churners have POS
after first + 3 months), cl_id adds nothing beyond the features, no copies cross the split, and the split's gap holds.

</details>

<details><summary>Column audit</summary>

Frame: `dataset_io.from_definition` on `datasets/_dev/tabarena-v0pt2/rosbank1/dataset.py`: 4,791 rows, 347 features +
`churn`; dtypes 227 float64, 116 int64, 3 datetime64, 1 category (+ target); no object column, no all-missing, no
constant, no duplicated column.

Prediction point (curation_comments bullet 1): the end of the client's three-month grace period; known then: the
client's card transactions up to that day. Source codebook: none. The boosters.pro API (`champ?champname=rosbank1`,
fetched today) has an empty `filesdescription` for both tasks; the only text is "history of clients' transactions during
3 months of privileged usage", task 1 churn (AUC), task 2 POS volume of "the next three months". Every raw column's
meaning below is therefore read from its name, the values and CoLES/ptls, not from a codebook (LEAK-2 cannot be met
from the source; LEAK-38 is the applicable rule for any anonymised field).

**Column table (by family; 347 features)**

| Column (family, n) | Meaning | Known at prediction? | Dtype and cleaning | Verdict | Rule |
|---|---|---|---|---|---|
| `n_transactions` | number of the client's transactions in the file (828 duplicate transaction rows counted) | yes, history up to period_end | int64; no missing | fine | LEAK-10, LEAK-16 (decided) |
| `amount_sum`, `amount_mean`, `amount_std` | sum/mean/std of `amount` over all transactions | yes | float64; std missing for 28 one-transaction clients (correct, not 0). **Mixed units**: `amount` is in the transaction currency (VND 704 and IDR 360 POS amounts up to 35,835,000; EUR median 25 vs RUB 500); 1,072 of 4,791 clients (22.4%) have a non-ruble transaction, 92 clients' `amount_sum` is over half non-ruble amounts | cleaning problem (note understates it) | CLEAN-21 |
| `channel_type` | unknown in the source; constant per client (asserted), read as acquisition channel by the definition | probably (static per client; type2 share rises over time as a client-mix attribute would; churn by channel stable per quarter: type1 0.59/0.57/0.57/0.54, type2 0.25/0.16/0.15/0.10) | category, 5 levels + 23 missing kept as NaN (no proxy) | fine; question on the wording | LEAK-38, LEAK-2, USE-6 |
| `count_trx_<cat>` (10) | transactions per category (POS, DEPOSIT, ATM kinds, C2C in/out, BACK_TRX refunds, CAT, CASH_ADV) | yes | int64, 0 when none | fine | LEAK-10 |
| `mean_amount_trx_<cat>`, `std_amount_trx_<cat>` (20) | amount mean/std per category | yes | float64; missing exactly when count 0 (mean) or count <= 1 (std), checked on POS; mixed currencies within POS, CAT, BACK_TRX. `std_amount_trx_CASH_ADV` has 2 non-missing values, `mean_amount_trx_CASH_ADV` 20 | fine (near-empty kept: CLEAN-22; not constant, so CLEAN-5 does not apply); currency mix as above | CLEAN-5, CLEAN-22, CLEAN-21 |
| `count_currency_{810,978,840,other}` (4) | transactions in rubles / euros / dollars / any other of ~40 ISO codes | yes | int64 | fine | |
| `mean_amount_currency_*`, `std_amount_currency_*` (8) | amount stats per currency | yes | float64; the three named currencies are one unit each; `*_other` mixes ~40 currencies (CZK, THB, VND, IDR, GBP ...) in one mean/std | cleaning problem (minor, inherent in the CoLES layout) | CLEAN-21 |
| `count_mcc_<code>`, 97 codes + `other` (98) | transactions per merchant category code; top 97 by frequency over all 5,000 clients | yes | int64; every MCC count column has >= 56 nonzero rows in the kept frame | fine; selection over all rows is the curator's accepted pipeline choice | CLEAN-8 (Lennart, 2026-10-19) |
| `mean_amount_mcc_*`, `std_amount_mcc_*` (196) | amount stats per MCC | yes | float64; missing semantics as above; sparsest `std_amount_mcc_9222` 20 non-missing; hotel/travel MCCs (7011, 4722) mix currencies | fine (currency mix noted) | CLEAN-22, CLEAN-21 |
| `nunique_mcc` (top single feature, 0.738) | distinct raw MCC codes (not the collapsed 98) | yes | int64, 1-57 | fine: breadth of use, legitimate history | LEAK-10 |
| `nunique_currency`, `nunique_trx_category` | distinct currencies (1-8) / categories (1-9) | yes | int64 | fine | |
| `first_transaction` | date of the first transaction (time-of-day normalised: POS carries no time, 98.4% at 00:00) | yes | datetime64 | fine | CLEAN-14 |
| `last_transaction` | date of the last transaction | yes, by construction (period_end >= last) | datetime64 | fine; see check 1 | LEAK-10 |
| `period_end` (time column, also a feature) | estimated grace-period end: max(first + 3 months, last) | yes (it is the prediction point) | datetime64; a deterministic function of the two dates above, so redundant, not leaking | fine | SPLIT-9 |
| dropped: `cl_id` | client id, carries the label (AUC 0.728 alone) | n/a | dropped; row order after `_clean` is content order then stable sort by period_end, so its order does not survive | fine | LEAK-10, CLEAN-3, CLEAN-23 |
| dropped: `PERIOD` | month of TRDATETIME (equal on 100% of rows, checked) | n/a | dropped, no information lost | fine | CLEAN-5 |
| dropped: `target_sum`, `target_flag` | POS spend of the next three months / its > 0 flag | no (post-outcome, defines the label) | dropped; `churn` = target_flag 0 | fine | LEAK-10 |
| `churn` (target) | no POS purchase in the three months after the period | outcome | category Yes/No | fine | USE-5 |

**Checks run on the columns the probes single out**

1. **Do the transactions reach into the label window? (LEAK-10, the window that defines the target.)** If the label
   window started at first + 3 months, any POS transaction after that date would force target_flag 1 (target_flag ==
   target_sum > 0 holds on all 5,000 clients). 479 clients have a POS transaction after first + 3 months, and 22.3% of
   them churned (107 clients); by the day of the last POS: 92-95 days 11.1% churn (162), 95-100 9.9% (71), 100-150 32.5%
   (126), over 150 50.0% (52). So for those churners the label window starts after their last transaction in the file:
   no evidence that features overlap the outcome window. The low churn at 92-100 days is recency (activity at the
   very end of the history), which the actor knows. Holds; residual risk is only for non-churners, which this test
   cannot see, and it rests on the period_end reconstruction (REVIEW_before issue 3), not on a column.
2. **Missingness caused by the outcome.** Means/stds are missing exactly when the client has no (or one) transaction of
   the value, computed from the history; the best missing indicator (`std_amount_mcc_5812`, restaurants, 0.694) is
   activity breadth, not a post-outcome blank. Holds.
3. **`channel_type` (single 0.738, drop-one -0.020, the strongest).** No codebook. Constant per client, the type2 share
   rises over period_end months as an acquisition mix would, and its churn rates are stable within each channel across
   quarters (above), which argues against a status written after the outcome. LEAK-38 (company competition data,
   anonymised field) keeps it in any case; the AUC drop when removed is small (0.844 to 0.824).
4. **Identifier encoding the label.** `cl_id` dropped; the stored row order is not cl_id order (content order + stable
   time sort, `src/data_foundry/v2/preprocessing.py` `order_rows`). Holds.
5. **Proxy and impossible values.** `amount` min 0.04, no zero or negative values (refunds and outgoing transfers are
   positive, so `amount_sum` adds inflows and outflows, as in CoLES; a meaning note, not a cleaning error). MCC 742-9405,
   no sentinel. `channel_type` NaN is a real missing. No proxy found (CLEAN-10, CLEAN-11 hold).

**Problems, ranked (principles.md: P4 before P7, Must before Should)**

1. **P4, question for the curator (LEAK-2, LEAK-38; not a finding of a leak).** `channel_type`'s meaning is the
   definition's inference: the source publishes no column descriptions, yet `task_summary.known` says "how the client
   was acquired" and curation_comments "the client's acquisition channel" as fact. Evidence: empty `filesdescription`
   in the boosters.pro API; the drift and per-channel stability above support the reading. Mildest remedy: keep the
   column; word it as "channel_type (undocumented; constant per client, read as the acquisition channel)" in
   curation_comments and the `known` field. No code change.
2. **P7, cleaning problem (CLEAN-21, Should).** Amounts mix currencies in `amount_sum/mean/std`, the per-category and
   per-MCC means/stds, and `*_currency_other`. The "Anomaly" bullet says "2.6% of transactions", which is right
   (12,869 of 490,513) but understates the effect: 22.4% of clients (1,072) have a non-ruble transaction, 92 clients'
   `amount_sum` is mostly non-ruble, and VND/IDR transactions put single amounts at 5-36 million (the top 8 amounts in the
   file are all VND or IDR). Remedies, mildest first: (a) keep, faithful to the CoLES/ptls baseline (CLEAN-1), but rewrite
   the bullet with the client share and the VND/IDR example; (b) the CLEAN-21 fix: convert `amount` to rubles with the
   Bank of Russia's official daily rates before aggregating (a pinned rate file; changes the baseline features, so the
   curator's call). Tree models are mostly robust to it; it is a quality, not a validity, problem.
3. **P7, note only (CLEAN-22, CLEAN-5).** Near-empty columns: `std_amount_trx_CASH_ADV` (2 non-missing of 4,791),
   `mean_amount_trx_CASH_ADV` (20), `std_amount_mcc_9222` (20). Not constant or all-missing, so they stay; no action.
4. **P7, note only.** The history window differs by row: 452 kept clients have 93 to 480 days of transactions
   (period_end = last transaction), so their counts cover a longer window than three months. Already a written decision
   (decision 5); counts are not per-day rates, as in CoLES. No action beyond the open period_end question.
5. **Writing, outside the columns (for the mediator).** curation_comments' `no_spread` note quotes "0.045 AUC, paired
   standard error 0.036"; today's task probe gives a skill gap 0.034, paired SE 0.087 (checklist P6). Refresh the numbers.

No column is a leak. Judgment: Validity: LEAK-10 holds (check 1: 107 churners have POS after first + 3 months, so the
history does not overlap their label window); LEAK-38 applies to `channel_type` (keep). Quality: CLEAN-21 departure, keep
with a corrected note or convert to rubles (curator); CLEAN-8 accepted (Lennart, 2026-10-19).

</details>

<details><summary>Split audit</summary>

Verdict: **right with notes.** Temporal on `period_end`, 1-month windows (Dec / Nov / Oct 2017), 3-month gap, expanding
train side, 50% floor.
Data: the definition's frame (4,791 x 348) and the raw transactions for the time column checks.

**Regime (USE-10, USE-11, SPLIT-1 to SPLIT-3)**

* One row per client, one prediction per client at the end of its introductory period; no client recurs. The entity is
  new at every prediction, and the use case is that one row (USE-11), so no grouping is needed: a temporal split already
  tests unseen clients. Stream of new clients over time with drift (churn 57% for Jan-2017 period ends to 35-40% in
  Q4 2017; type2 channel 16% to 44%): temporal is the regime the use case implies. Holds.
* Hidden groups: probe no hits; near copies 0.5% of test rows; the two identical client pairs share `period_end`, so
  they sit on one side of every split. No IID question arises.

**Temporal checks**

* Time column meaning: the estimated end of the 3-month period, `max(last, first + 3 months)`. Analytic check: if the
  file holds only the period's transactions, the true end is `true_start + 3m <= first + 3m`, and `>= last`, so the
  estimate is an upper bound of the true end for the 4,435 clients at `first + 3m`. A late estimate makes a training
  label look known later than it was: conservative for the gap (train loses a few rows; never gains one with an unknown
  label). For the 565 clients at `last`, the estimate equals the last activity; it could be early only if the true period
  ran past the last transaction, which nothing in the file can tell.
* Do the transactions past `first + 3m` sit in the label window (a SPLIT-9 / LEAK-10 shortcut)? No: 479 clients have a
  POS transaction after `first + 3m`, and 107 of them (22%) are still churners (target_flag 0); their summed POS amount
  after `first + 3m` has correlation -0.02 with `target_sum` and never equals it. The label window is not in the file.
* Windows and train side (rebuilt splits):

  | test window | test rows | churn | train rows (share) | train period_end range |
  |---|---|---|---|---|
  | 2017-12-01 to 12-30 | 63 | 0.365 | 3,566 (0.744) | 2017-01-07 to 2017-08-31 |
  | 2017-11-01 to 11-30 | 123 | 0.398 | 3,078 (0.642) | 2017-01-07 to 2017-07-31 |
  | 2017-10-01 to 10-31 | 515 | 0.348 | 2,559 (0.534) | 2017-01-07 to 2017-06-30 |

  Matches the splits_comment. Gap = 3 months = the label delay (SPLIT-10): the newest training label (period end
  2017-08-31) closes 2017-11-30, before the December window opens. No training row has an unknown label at the window
  start (SPLIT-9 holds). 3 windows, train >= 50% (SPLIT-14 holds); smallest window 63 > ~50 (SPLIT-17 holds).
* Cohort: period ends from 2018-01 dropped (label windows past the data, March 2018 churn 24/36): the test windows'
  labels close by 2018-03-31, inside the transactions (end 2018-04-02). Holds whatever the label draw date after that.

**Model comparison (LightGBM, 300 trees, untuned; ROC AUC per split, mean)**

| split | with the date features | without them |
|---|---|---|
| shipped: temporal, gap 3 months | 0.873 / 0.872 / 0.834 = 0.860 | 0.859 / 0.860 / 0.833 = 0.851 |
| temporal, no gap | 0.858 / 0.881 / 0.863 = 0.867 | 0.873 / 0.864 / 0.854 = 0.864 |
| IID, 3 x 3 stratified | 0.817 (0.805-0.833) | 0.807 |
| same test windows, random train of equal size | 0.855 / 0.890 / 0.864 = 0.870 | |

Bootstrap SE of the window AUCs: 0.044 (Dec, 63), 0.031 (Nov, 123), 0.018 (Oct, 515).
The gap costs ~0.007 AUC; on the same test rows a random (future-including) train side scores ~0.01 higher. The IID
3 x 3 score is lower (0.817) because the later clients are easier to score, not because the temporal split is lenient.

**Problems, ranked (principles.md)**

1. **P4, SPLIT-20 (Should): season of the test windows / short training history.** All three test windows' label
   windows (Nov-Jan, Dec-Feb, Jan-Mar) span the December and New Year holidays; no training label window does (train
   period ends 2017-01-07 to 2017-08-31, label windows to 2017-11-30), and the history is 8 months, not a full season.
   Churn shows no visible step (Sep 37.6%, Oct 34.8%, Nov 39.8%, Dec 36.5%), so the effect looks small. The data holds
   nothing earlier or later with complete labels. Remedy: none possible; a note in `splits_comment`.
2. **P4, SPLIT-1/SPLIT-12 (Should): the newest two windows are a different slice of clients.** The client intake ends
   with the July 2017 starts (first transactions 400-800 a month to 2017-07, then 109, 50, 54, ...), so the Nov and Dec
   windows are a trickle (123 and 63) with 29% and 37% of clients whose period end is the last transaction (spans over
   92 days), against 7-16% in earlier months; median transactions 58 and 41 against ~90-100. A side effect of the
   estimated time column and the sampling, not of the split rule. Their AUCs carry SE 0.03-0.04. Remedy: a note (the
   splits_comment could name the intake drop); no re-split is better (two-month windows fall below the floor, per the
   splits_comment).
3. **P4, SPLIT-10 detail (Weigh): the time column is estimated.** Shown to be conservative for the clients at
   `first + 3m` (upper bound of the true end); unverifiable for the 565 at `last`. Already in fit_reason and
   REVIEW_before issue 3. Remedy: keep with the note; consider adding the upper-bound argument to curation_comments
   ("Time") so the gap's safety is stated, not implied.
4. **Writing (procedure): "this split is stricter".** In score terms it is not: IID 3 x 3 scores 0.817, the shipped
   split 0.860. Stricter holds for design only (same test rows, random train: 0.870). Remedy: reword to "mirrors the
   refit; on its test windows a random training side scores ~0.01 higher".
5. **P4, LEAK-27 (accepted):** the 97 MCC columns are chosen over all rows, test windows included; curator kept it
   (2026-10-19). Listed for completeness; label-free.

Not problems: SPLIT-9 (no unknown-label training rows), SPLIT-10 (gap = delay), SPLIT-14, SPLIT-17, SPLIT-21 (windows
not picked from a comparison), SPLIT-29 (no hidden groups), the cut at 2018-01-01 (cut B is a label-date question,
REVIEW_before issue 4, not a split one).

</details>

<details><summary>Domain practitioner</summary>

Role played: a retention analyst at Rosbank's retail card business in 2018. At the end of a new cardholder's
three-month "privileged" (льготный) period I score who will stop using the card, and the CRM team sends retention
offers (fee waiver extension, cashback) to the top of the list. Numbers below are from my own
runs on the raw train.csv.gz.

**Fit: approximate (agree with the definition)**

One row per new cardholder scored at the end of the introductory period on its card transactions is a real decision I
make (USE-1, USE-3), but the time axis is reconstructed, the label's horizon is not stated and is not uniform across
cohorts, and the inputs are a narrow slice of what I hold then (USE-8: "a reconstructed time axis or a label without a
stated horizon", the alfa_battle_2_0_task_2 precedent). USE-9 offers no direct alternative: no other use case makes the
label timing well defined.

**1. Inputs at the prediction point**

Have, and legitimate (USE-3, USE-6): all transaction aggregates (counts/sums/means/stds by category, currency, MCC),
first/last transaction date, acquisition channel. Recency is the strongest signal I would use myself: clients whose
transactions span 0-30 days churn 83%, 80-92 days 32% (my run); it is known at period end, not a leak.

Would not have, or have differently:
* The 97 MCC columns picked by frequency over all clients including test windows (accepted, Lennart 2026-10-19): in
  production I pick from history. Minor, label-free.
* `period_end` as computed: I would never estimate it; I know it (below).

Missing that I would always have (ranked by what they add):
1. The card open date and the contractual end of the privileged period (and the tariff that starts after it). The
   dataset rebuilds them from first and last transactions; I never would.
2. Balances, salary inflow regularity, other products (deposits, loans, salary project), digital-banking activity: the
   standard churn feature layers in bank practice (Habr churn article). DEPOSIT and C2C transactions partly stand in.
3. Demographics/KYC (age, region, income band).
The benchmark is honest as "card transactions only", the competition's frame, so these are scope limits, not defects.

**2. Target**

Churn = target_flag 0 = no POS spend in the label window (assert target_flag == (target_sum > 0) holds). That is an
activity-churn proxy: a client who keeps the card for ATM withdrawals or deposits but buys elsewhere counts as churned.
For a card business whose income after the promo is interchange plus fee, "no POS purchases" is close to what I act on
(USE-5). I would want a calibrated probability (ROC AUC only ranks; a ranked list is the first use, so AUC is fine) and,
ideally, uplift: who responds to the offer, which this data cannot give (no treatment record).

The weaker point is the label window. My checks:
* Clients with a reconstructed period end in April-June 2018 (63, dropped) still have labels, 32-54% churn, and the 37
  non-churners among the 2018Q2 ones have a median target_sum 1.6 times their own period's POS spend. The labels were
  released 2018-04-27, so for them the label cannot be "POS spend in the three months after the period" as
  reconstructed. Either the reconstruction is wrong for those clients or the label window is not tied to each client's
  period.
* Among non-churners and churners together, the median ratio of target_sum to period POS spend rises monotonically with
  the period-end quarter: 2017Q1 0.40, Q2 0.53, Q3 0.67, Q4 0.72. Churn falls within acquisition channel type2 from
  25% (2017Q1) to 10% (2017Q4), flat in type1 (59% to 54%).
* This fits genuine drift, but it equally fits a label measured over a common calendar window (activity decays with
  cohort age). If the window is calendar-fixed, the temporal split's three-month gap rests on a wrong timing model and
  the time columns carry "months since the promo" relative to a fixed date. Nothing published settles which. The cut C
  (periods ending before 2018-01-01) is the safe choice under the per-client reading; under a calendar reading it does
  not hurt either. I would name this in the fit_reason as "the label's window is not stated" rather than only "when the
  labels were drawn".

**3. Row and test data**

One row = one client at period end = one decision of mine (USE-11 holds: the use case is each client's first and only
promo end, so one row per entity is right; USE-10: a new client, no prior outcome exists). Test windows Oct/Nov/Dec 2017
are "the clients whose period ends next month", the population I would score: right in kind (SPLIT by time, gap =
label window).

But the newest windows are the least representative and the most reconstructed:

| period_end month | clients | period_end = last tx (estimate shaky) | median tx count | churn |
|---|---|---|---|---|
| 2017-08 | 488 | 16% | 89 | 42.8% |
| 2017-09 | 524 (gap) | 12% | 104 | 37.6% |
| 2017-10 (test) | 515 | 11% | 98 | 34.8% |
| 2017-11 (test) | 123 | 29% | 58 | 39.8% |
| 2017-12 (test) | 63 | 38% | 41 | 36.5% |

New acquisition collapses after July 2017 in this sample (first transactions per month: 519 in July, 109 in August, 50
in September), so November and December are a thin tail of late or irregular clients, not a normal month's intake. The
October window (515) is the one that looks like my monthly intake; the other two are noise at 63 and 123 clients.

**4. Would I use it?**

I would trust a model on these aggregates to rank clients at period end: the signal is strong and plausible (recency,
transaction count, channel, salary-like deposits), and LightGBM at ~0.84-0.86 AUC matches CoLES and the competition
(winners 0.87 private, likely with cl_id or the unlabelled test file). I would distrust it for (a) calibrated budget
decisions, since the base rate drifts (53% to 36% by quarter) and the label window is unclear, and (b) clients the
period-end estimate gets wrong. Before deployment I would rebuild it with the true contract dates and add balance/
salary features.

**Gaps, ranked by how much they change the task**

1. Label window not stated and possibly not per-client (positive labels for periods that end after the release date;
   target_sum/period spend rising with cohort). Changes what "churn" means across rows and whether the 3-month gap is
   the right gap. USE-5, USE-8; LEAK-22 to LEAK-26 for the censoring side.
2. Reconstructed period end, worst in the test windows (29% and 38% of Nov/Dec clients take period_end = last
   transaction vs 11-16% earlier). The split axis is least reliable exactly where it is scored. USE-8, SPLIT-1.
3. Thin, atypical test windows (63 and 123 clients, a shrinking intake tail); only October is a normal month. TP-3
   `no_spread` follows. USE-1 (test data stands for next month's intake only loosely).
4. Missing inputs the bank always has (contract dates, balances, products, demographics). Scope limit of the source,
   not a cleaning error; fine under "card transactions only". USE-6.
5. Activity proxy (no POS) vs commercial churn (fee-paying, closure). Acceptable proxy. USE-5.

**What a domain expert would change**

* State the label as "no POS purchase in the label window, whose timing the release does not give" and make fit_reason
  lead with it (USE-8). Keep fit approximate.
* Consider the October 2017 window as the main test and report Nov/Dec as small; or consider the alternative the
  REVIEW_before issue 2 names (IID 3x3, the competition's protocol) given that the temporal axis is itself an estimate
  in the windows that matter. I lean to keeping temporal (drift is real within channel type2), but the curator should
  see the table above.
* Prediction point: in practice I would score two to four weeks before the promo ends to leave time for an offer; the
  full three months is the competition's frame and acceptable (USE-3).
* Feature width: 97 MCC columns is faithful to CoLES; an analyst would use 10-30 plus recency features (days since last
  transaction, last-month vs first-month activity). REVIEW_before issue 5 shows 10-30 codes do as well. Not a
  correctness issue.
* Curation_comments `no_spread` bullet quotes stale probe numbers (checklist): update.

**Sources**

* Competition page and API text (task: "history of clients' transactions during 3 months of privileged usage";
  task 1 churn AUC; dates 27.04-28.05.2018; leaderboard private AUC ~0.87):
  https://boosters.pro/api/champ/champ?champname=rosbank1 (fetched 2026-10-20).
* Data mirror: https://huggingface.co/datasets/pytorch-lifestream/rosbank-churn (pinned revision in dataset.py).
* CoLES, Babaev et al. 2022, arXiv 2002.08232 (as cited by the definition; not re-read).
* Bank churn practice (activity labels, feature layers, uplift, calibration): https://habr.com/ru/articles/1010188
* FAS warning to Rosbank on free-servicing conditions (context only): https://www.akm.ru/news/fas_vydala_rosbanku_preduprezhdenie/
* Repository: datasets/_dev/tabarena-v0pt2/rosbank1/dataset.py, curation/records/rosbank1.md,
  .claude/skills/knowledge-curation/references/use_case.md, panel claims.md, checklist.md, REVIEW_before.md.

</details>

<details><summary>Blind review</summary>

**Verdict**
Include with changes. It is a real bank churn task with good, non-trivial signal (LightGBM AUC about 0.87 on temporal folds). But the churn definition behind the label is not documented, `period_end` is a column the preparer built, and the three datetime columns need a deliberate encoding.

**What the task is**
Rosbank (boosters.pro, 2019) released 3-month card transaction histories for about 10K retail clients. About 5K of them have a churn label. A retention team would score clients at the end of an observation window and decide whom to target with offers. This is a real and common use. Here each row is one client: 343 aggregates (counts and mean/std of amounts per transaction category, currency and MCC, plus nunique counts), `channel_type`, three dates and the target `churn` (Yes 2146 / No 2645, 44.8%). There is no client id.

**Concerns, most to least serious**

1. **The label definition is unverified, and recency drives much of the signal.** I could not get a churn definition from either source page. The boosters page renders empty. The HF page shows only the raw schema (PERIOD, cl_id, MCC, channel_type, currency, TRDATETIME, amount, trx_category). The gap `period_end - last_transaction` predicts the label strongly: churn rate is 25% at gap 0 days and 82% at gap of 30 days or more. Median gap is 0 for non-churners and 12.5 for churners. On its own, the gap gives AUC 0.78. This is fair if churn means "inactive after the window". It is leakage if the label was derived from inactivity inside the observed window, for example because the history of churners was cut at their churn date.
   - Change: find and quote the organiser's definition of `target_flag` before including the dataset. If the definition is window-internal, drop the gap-carrying date columns.

2. **`period_end` is built by the preparer, not given by the source.** It matches `max(first_transaction + 3 months, last_transaction)` on 100% of rows. The temporal split is therefore on a synthetic anchor tied to each client's first transaction, not on the source's `PERIOD`. For the 10.9% of clients with history longer than 3 months, `period_end = last_transaction`, so their gap is forced to 0. Their churn rate is 24% against 45% overall.
   - Change: document the rule in the task description. Derive the window from the source's `PERIOD` field if possible. Check that each label's outcome horizon in the training rows ends before the test window starts. Training windows overlap the test windows in time, and the length of the churn horizon is unknown.

3. **The split and drift are acceptable but should be stated.** Churn rate falls over time: 57% in January 2017 and 35–40% in September–December 2017. Fold test sets have 43%, 38% and 36% positives (about 719 rows each). Month counts are uneven: April has 151 rows and December 63. The original competition used a random client split. A temporal split is defensible, but it is the preparer's choice.

4. **Datetime columns.** `first_transaction`, `last_transaction` and `period_end` are raw datetime64. Many methods will drop or mishandle them. Converting them to ordinal days or day-of-year plus gap/span adds about 0.04 AUC (0.832 to 0.872). Absolute dates also encode the trend in item 3.
   - Change: ship derived numeric features (recency gap, history span) or drop the dates. Do not leave the encoding to each method.

5. **Missing rows and duplicates.** There are 4,791 rows, but the source reports about 5K labelled clients. The reason for dropping about 200 clients is undocumented. There are 2 exact duplicate pairs (single tiny-transaction clients, all labelled Yes). These are probably genuine distinct clients, so they are harmless.

6. **Minor preparation issues.**
   - The feature space is very sparse: many mean/std MCC columns are 99% NaN. NaN is used consistently (mean is NaN exactly when count is 0) and is acceptable. Dropping MCC columns with fewer than about 1% non-zero values would cut the width a lot.
   - `amount_sum`/`amount_mean` add amounts across currencies without converting them, but about 2.6% of transactions are non-RUB.
   - `channel_type` has 3 very rare levels (46–56 rows each).

**Signal check (LightGBM, 3 expanding temporal folds on period_end, 718–719 test rows each)**
- All features, dates as day numbers: AUC 0.863 / 0.864 / 0.888 (mean 0.872)
- Without any date-derived features: mean 0.832
- Gap only: 0.783
- Time only: 0.50

The task is neither trivial nor noise, and it is big enough to score.

**Could not check**
- The official churn and `target_flag` definition and its outcome horizon. The boosters page is empty without login or JavaScript, and the HF card text was not shown.
- Whether `PERIOD` in the source would give a different window anchor.
- Why about 200 labelled clients are missing.
- Whether the aggregates were computed only on transactions up to `period_end`. This looks consistent: every last_transaction is at or before period_end by construction.

</details>

<details><summary>Precedent check</summary>

Consistency check of the decisions in `datasets/_dev/tabarena-v0pt2/rosbank1/` (dataset.py, the earlier REVIEW.md)
and `curation/records/rosbank1.md` against the rules and their Cases tables
(`.claude/skills/knowledge-curation/references/*.md`), the register (`../../register.txt`) and the closest sibling,
`alfa_battle_2_0_task_2`.

The record has **no `CC` lines**: the only curator decision on rosbank1 is the CLEAN-8 case (Lennart, 2026-10-19, in
curation_comments and in the CLEAN-8 Cases row). Everything else is the AI's draft. So "drift" (case 3) cannot arise on
this dataset; the checks are case 1 (a departure without a fact) and case 2 (a sibling decided the other way).

**Summary**

| # | Decision | Rule(s) | Result |
|---|---|---|---|
| 1 | Features = the CoLES / pytorch-lifestream baseline (97 MCC codes), "as alfa_battle_2_0_task_2 kept its organizers' set" (REVIEW issue 5) | CLEAN-19 (Should) | **departs without a reason; the cited precedent is misstated** |
| 2 | REVIEW issue 5's alternative "10 or 30 codes" argued from width ("294 of 347 features, mostly empty") | CLEAN-22 (Must) | **the alternative as framed is not reasonable under the ranking** |
| 3 | Overall amount statistics mix currencies (2.6% non-ruble), "as in CoLES" | CLEAN-21 (Should) | departs; the reason given is a precedent, not a fact |
| 4 | `period_end` = last transaction when later than first + 3 months (565 clients), those transactions stay in the features | LEAK-10 (Must), LEAK-7 | open question: the leak side is not argued |
| 5 | MCC codes chosen by counts over all rows, noted as a pipeline choice | CLEAN-8 (Must) | consistent (it is the rule's own case) |
| 6 | Cut C: periods ending before 2018-01-01 kept; cut B (keep January) as the alternative | LEAK-24 (Must) | consistent with sf_permit_time; cut B would need a fact (the draw date) |
| 7 | Temporal split with a 3-month gap = the label window; competition's random split not followed | SPLIT-1, SPLIT-5, SPLIT-10, SPLIT-19 | consistent (sf_permit_time, brazilian_ecommerce); the IID alternative of REVIEW issue 2 would break SPLIT-1/SPLIT-7 |
| 8 | Monthly windows (63/123/515), 3 windows, 50% floor, September in the gap (accepted `splits_rows_unused`) | SPLIT-14, SPLIT-17, SPLIT-21 | consistent; differs from alfa's 2-month no-gap windows for a stated fact |
| 9 | Target churn (task 1); `rosbank1_reg` offered (REVIEW issue 1) | USE-5, PROV-6, PROV-7 | churn consistent; the `_reg` alternative over all clients would be a PROV-6 duplicate (arsenic_male_lung) |
| 10 | `no_spread` kept | TP-2, TP-3, EV-3 | consistent; the note and the TP-2 Cases row carry stale numbers |
| 11 | `target_sum`, `cl_id` dropped; mean/std over 0-1 transactions missing; `channel_type` categorical; duplicate client pairs kept | LEAK-10, CLEAN-10, CLEAN-14, CLEAN-22, LEAK-16 to LEAK-21 | consistent |
| 12 | fit `approximate` for a reconstructed time axis | USE-8 | consistent with alfa_battle_2_0_task_2 |

Third exception of one kind: none found (no recorded exception to CLEAN-19, CLEAN-21 or LEAK-24 elsewhere).

**Details**

**1. Feature set: CoLES baseline against the alfa_battle_2_0_task_2 precedent (CLEAN-19, Should) - departs without a reason**

* Decision: `aggregate_transactions` builds "the hand-crafted features of the CoLES paper ... as pytorch-lifestream
  configures them" (dataset.py; curation_comments "Tabular framing"). REVIEW issue 5: "Implemented: 97, faithful to the
  published baseline (as alfa_battle_2_0_task_2 kept its organizers' set)".
* Rule: CLEAN-19, third bullet: a transaction log aggregated to one row per prediction is built as "a data scientist on
  this task would build ... Take the features the top solutions share." Case: alfa_battle_2_0_task_2 (Lennart,
  2026-10-13).
* Precedent: `curation/records/alfa_battle_2_0_task_2.md`, CC (2026-10-13, Lennart): "Features like the top solutions of
  the competition, what a data scientist would build, **instead of the organizers' 127-feature baseline**: 513
  aggregates ..." (also the CLEAN-19 Cases row, `cleaning_features.md` line 157). alfa did **not** keep its organizers'
  set: the AI assessment of 2026-10-07 had chosen the baseline, and the curator overturned it.
* Same facts: both are a bank competition on boosters.pro, a card-transaction log per client, one label per row, a
  published baseline of aggregates (organizers' 127 for alfa; the CoLES/ptls config for rosbank1).
* Distinguishing fact: none written. Candidates, not checked: the rosbank1 competition's top solutions may not be
  published (the definition names only two participant repos, kianya/rosbank-competition and
  Ikitan/ML-Rosbank-competition, as copies of the data, not as solutions); CoLES is a peer-reviewed tabular baseline
  where alfa's was an organizers' notebook. Neither is recorded, and nothing says the top solutions were searched for.
* Side note: alfa's top-solution set uses the 30 most frequent `mcc` codes (alfa dataset.py, curation_comments), one of
  the alternatives REVIEW issue 5 lists.

**Consistency check (AI, 2026-10-20):** the rosbank1 features follow the CoLES baseline (pytorch-lifestream config),
while alfa_battle_2_0_task_2 (CC 2026-10-13, Lennart; CLEAN-19 case) replaced its organizers' baseline with the
features the top solutions share; REVIEW.md issue 5 cites alfa as keeping its organizers' set, which it did not. What
sets rosbank1 apart? (a) the competition's top solutions are not published, so the peer-reviewed CoLES baseline is the
best record of what a data scientist would build on this data, recorded as an exception to CLEAN-19 (once the search is
documented); (b) treat rosbank1 like alfa: search the 2018 leaderboard's write-ups and participant code, and build the
features they share; (c) reopen alfa to match rosbank1; (d) amend CLEAN-19 (a peer-reviewed baseline counts as "what a
data scientist would build").

The issue text of REVIEW.md issue 5 should be corrected either way: its precedent is the reverse of what was decided.

**2. The narrower alternatives of REVIEW issue 5 (CLEAN-22, Must) - not reasonable as framed**

* REVIEW issue 5 is titled "Feature width" and motivates the alternative with "294 of the 347 features, mostly empty"
  and scores over the shipped windows (0.860 for 97 codes against 0.863 for 30).
* CLEAN-22 (Must): "Width is no reason to drop a block or to propose a narrower version." Case:
  coad_colon_adenocarcinoma (Lennart, 2026-10-15); Tensions row "Width against model limits". Also SPLIT-21's spirit and
  TP-1: a 0.003 AUC difference over three windows of 63-515 clients is noise (the panel's own probe: paired SE 0.087).
* A different number of MCC columns is legitimate only as a CLEAN-19 argument (what the top solutions do; alfa: 30).
  As written, the alternative departs from a Must and has no higher-ranked Must behind it.

**Consistency check (AI, 2026-10-20):** REVIEW issue 5 offers 10 or 30 MCC codes because 97 make the table wide and
mostly empty; coad_colon_adenocarcinoma (2026-10-15, Lennart; CLEAN-22) ships 36,355 features on the rule that width is
no reason to propose a narrower version. What sets rosbank1 apart? (a) nothing on width; the number of codes is decided
under CLEAN-19 by what the top solutions use (alfa: 30), and the issue is rewritten that way; (b) treat it like coad: keep
97 and drop the alternative; (c) reopen coad; (d) amend CLEAN-22.

**3. Mixed currencies in the overall amount statistics (CLEAN-21, Should) - departs, reason is a precedent**

* curation_comments, "Anomaly": "amount is in the transaction's currency, so the overall amount statistics mix
  currencies for the 2.6% of transactions not in rubles, as in CoLES." Kept.
* Rule: CLEAN-21: "One unit and one scale per column ... with the conversion the source or the measuring body
  publishes." Cases: college_scorecard (2026-10-16, Lennart). Sibling practice: kickstarter converts `goal` to USD with
  the source's `usd_exchange_rate` (kickstarter dataset.py, curation_comments); alfa_battle_2_0_task_2 restores rubles
  before aggregating.
* "As in CoLES" names a source that did it, not a fact that sets the case apart. A possible fact: the release has no
  exchange rate, and a rate from outside the source (the Bank of Russia's daily rate, by transaction date) would be our
  own addition. The per-currency blocks keep the separate currencies visible, which limits the damage. A cheap and safe
  fix (P7, "fixed when the fix is cheap and safe") would be the overall statistics over ruble transactions only, or a
  conversion at the Bank of Russia's rate of the transaction date.

**Consistency check (AI, 2026-10-20):** rosbank1 keeps overall amount statistics that add rubles, euros and dollars
(2.6% of transactions), "as in CoLES"; CLEAN-21 asks for one unit per column, and kickstarter converts its goals to USD
with the source's rate. What sets rosbank1 apart? (a) the release has no exchange rate and the per-currency columns
carry the rest, recorded as an exception to CLEAN-21 (serves P5: no values from outside the source); (b) treat it like
kickstarter: convert at the Bank of Russia's rate of the transaction date, or compute the overall statistics over ruble
transactions only; (c) -; (d) amend CLEAN-21 to say when an external published rate is required.

**4. Transactions after the nominal three months in the features (LEAK-10, Must) - the leak side is not argued**

* Decision (decision table "The period end is three months after the first transaction, or the last transaction when
  later"): 565 clients get `period_end` = their last transaction; their transactions past first + 3 months stay in
  every aggregate and in `last_transaction`. The reason given is descriptive ("most clients transact over 80 to 92
  days"); whether those extra transactions fall in the label window is not discussed.
* Rule: LEAK-10 (Must): out is "a feature computed from the window that defines the target" and "an aggregate that may
  include the row's own outcome"; LEAK-7: the smallest fix. Cases: mutual_funds_india `rating`; iranian_churn (retired,
  features summarise a window ending at the outcome).
* Fact from the README decision table: churn share is 0.168 for the 268 clients with 93-100 days of history (all with
  `period_end` = last), against 0.323 at 80-92 days and 0.332 at over 100 days. Post-period POS purchases would be
  exactly the "no churn" evidence; the over-100 bucket does not show the drop, so the data is mixed. The leak probe found
  no flag (drop-one at most -0.020, on `channel_type`).
* This is not a departure from a curator's precedent (there is none on this dataset), but a Must the draft does not
  address. Suggested question for the panel/curator: truncate each client's transactions at first + 3 months (LEAK-7)
  and measure, or record why transactions past day 92 belong to the grace period (the source says the history is "during
  3 months of privileged usage").

**Consistency check (AI, 2026-10-20):** rosbank1 keeps transactions past the nominal three months in the features of
565 clients; LEAK-10 excludes aggregates that may hold the outcome window (mutual_funds_india, iranian_churn), and the
93-100-day clients churn at 0.168 against 0.323. What sets rosbank1 apart? (a) the source says all transactions are of
the privileged period, so a longer span is a longer period, not the label window, recorded with that citation; (b) treat
it like the LEAK-10 cases: cut the features at first + 3 months; (c) -; (d) -.

**5. MCC codes by counts over all rows (CLEAN-8, Must) - consistent**

The rule's own case (Lennart, 2026-10-19; `cleaning_features.md` lines 48-50 and 149; also LEAK-29 cross-reference,
`leak_checks.md` line 204). The temporal note the rule requires is in curation_comments. Same as alfa_battle_2_0_task_2
and anes_voting_2026.

**6. Censoring cut C (LEAK-24, Must) - consistent**

* LEAK-24: a target right-censored in the newest periods "is cut where follow-up is complete". Cases: sf_permit_time
  (permits filed before 2024), consumer_complaints. Cut C keeps only label windows that close inside the data (by
  2018-03-31), the reading that holds whatever the unpublished draw date: follows sf_permit_time.
* Cut B (keep January 2018, REVIEW issue 4) is complete only if the labels were drawn at the end of April. January's
  churn (29.0%) shows no censoring sign (censoring would raise churn), February (39.6%) slightly, March (66.7%) clearly.
  Choosing B is not an exception (LEAK-24 is a Must); it is a reading of the fact "follow-up is complete", and would need
  the evidence written as such (EV-2: the measurement on the data is the only evidence; the source is silent).

**7. Temporal with a 3-month gap; the competition's random split not followed - consistent**

* SPLIT-10 (Should): gap of about the label's delay. Cases: sf_permit_time (6 months), brazilian_ecommerce (1 month).
  rosbank1's gap equals the 3-month label window: follows them.
* SPLIT-19 (Should) would follow the competition's random split; SPLIT-5 (Must) makes it a claim to check, and SPLIT-1
  (Must) wins. The drift (churn 53.0% in 2017Q1 to 35.8% in 2017Q4, type2 share up) is the fact that sets it apart; the
  Tensions row "The right split against the score" (forest_fires) covers the cost in test size.
* REVIEW issue 2's IID alternative: SPLIT-7 (Must, "A missing or hidden timestamp does not make a task IID") and SPLIT-1
  argue against it; the only IID-kept precedents (SPLIT-31: amazon_employee_access, bank_marketing) rest on the task's
  framing, not on test size. Choosing IID would need such a framing fact; window size alone is the forest_fires
  tension, decided for the split.
* Sibling difference: alfa_battle_2_0_task_2 has no gap (its default has no stated horizon and a 12-month gap would
  breach the 50% floor, alfa splits_comment). rosbank1's label window is stated (3 months), so the difference has its
  fact.

**8. Window design - consistent**

SPLIT-14 (3 windows, 50% floor) holds; the September 2017 window is left out by the floor, not by a score comparison
(SPLIT-21, aeolus). SPLIT-17 (about 50 test rows): smallest window 63 clients (23 churned); coffee_rating_prediction
widened only below this (2-72 reviews). Two-month windows would breach SPLIT-14 (splits_comment). TP-9: 23 positives in
the smallest window is far from seismic_bumps (0-5). The accepted `splits_rows_unused` matches alfa's accepted warning
of the same kind (rows unused by design).

**9. Target churn; `rosbank1_reg` (USE-5, PROV-6, PROV-7)**

* Churn (task 1) is what CoLES and pytorch-lifestream benchmark and what the bank acts on (retention): USE-5 holds.
* A second folder for task 2 over all clients (log1p(target_sum), 44.8% zeros, "mostly the churn task again") is a
  swapped target of the same cohort: PROV-6 (Must), case arsenic_male_lung (the lung-cancer version of the bladder
  data: a duplicate). The spend of the 2,645 retained clients is closer to a distinct task (PROV-7: parkinsons, one
  source two tasks), but its windows hold 40-74 test clients in two of three. REVIEW issue 1 should say which of the two
  it means and cite PROV-6/PROV-7.

**10. `no_spread` kept (TP-2, TP-3, EV-3) - consistent, numbers stale**

* Kept like heart_disease_cleveland, electric_motor_temperature_prediction, african_credit_scoring_challenge (few
  windows; evidence.md line 171 lists rosbank1 itself under "the noise of ... few windows").
* The curation_comments note and the TP-2 Cases row (`task_probes.md` line 310) say "LightGBM leads linear by 0.045 AUC,
  paired SE 0.036"; today's probe gives a skill gap of 0.034 with paired SE 0.087
  (AUC 0.859 vs 0.842). The conclusion is unchanged; the numbers need updating in both places (writing.md).
* TP-1 asks to check the flag against tuned methods; none exist for this new dataset, so the keep rests on the window
  count. Not a departure.

**11. Other choices - consistent**

* `target_sum` dropped: another encoding of the target (LEAK-10 Cases: "a part, a consequence or another encoding").
* `cl_id` dropped: an identifier carrying the label (alone AUC 0.728); LEAK-10 targeting/pointing ids (sdss_17
  `plate`), CLEAN-22 "an identifier".
* Mean/std over 0 or 1 transactions as missing rather than the config's 0: CLEAN-10 (real missing values).
* `channel_type` one categorical column (CLEAN-14), asserted one value per client.
* Two identical client pairs kept, each pair on one side of every split (LEAK-16 to LEAK-21: no copy across the split;
  probe 0.0%).
* Date features (`first_transaction`, `last_transaction`, `period_end`): common in the working copy (kickstarter,
  hotel_booking_demand, brazilian_ecommerce).

**12. fit `approximate` (USE-8) - consistent**

Same reason class as the USE-8 case alfa_battle_2_0_task_2 ("approximate: a reconstructed time axis or a label without
a stated horizon").

**Precedents cited**

* alfa_battle_2_0_task_2: `curation/records/alfa_battle_2_0_task_2.md` (CC 2026-10-13, Lennart);
  `datasets/_dev/tabarena-v0pt2/alfa_battle_2_0_task_2/dataset.py` (split, accepted warning, ruble restoration, 30 MCC).
* CLEAN-8, CLEAN-19, CLEAN-21, CLEAN-22 Cases: `.claude/skills/knowledge-curation/references/cleaning_features.md`
  (lines 48-50, 97-105, 112-114, 117-120, 149-160).
* LEAK-10, LEAK-24 Cases: `.claude/skills/knowledge-curation/references/leak_checks.md` (lines 71-85, 135-137, 279-297).
* SPLIT-1, -5, -7, -10, -14, -17, -19, -21, -31 Cases: `.claude/skills/knowledge-curation/references/splits.md`.
* PROV-6, PROV-7 Cases: `.claude/skills/knowledge-curation/references/provenance.md` (lines 43-49, 205-207).
* TP-2 rosbank1 row: `.claude/skills/knowledge-curation/references/task_probes.md` line 310; evidence.md line 171.
* kickstarter currency conversion: `datasets/_dev/tabarena-v0pt2/kickstarter/dataset.py` lines 78, 121-123.

</details>

<details><summary>Advocate</summary>

Position: ship as defined, after text-only changes. No phase A report found a leak, a wrong split or damaged data. The
real problems are in the wording (label timing, attributions, stale numbers) and in P7 cleaning. Each has a remedy that
keeps the definition's data and splits.

**1. No leak: every feature is known at the period end (P4, LEAK-10 Must, holds)**

* Evidence: 479 clients have POS purchases after first + 3 months, and 107 of them (22%) are still churners. Their POS
  sum after that date correlates -0.02 with `target_sum` and never equals it (split audit). Among each calendar month's
  POS buyers, churn is never near 0 (lowest 17.9%, Oct 2017; claim audit). So the label window lies outside the file
  for every client, whichever way it was placed. Drop-one costs at most -0.020 (`channel_type`). There are no exact
  copies across the split (0.0%). `cl_id` (AUC 0.728 alone) and `target_sum` are dropped.
* Objections answered: the blind review's "the history of churners may be cut at the churn date" (gap-only AUC 0.78)
  and precedents #4 (the 565 clients with history past day 92). Both are inferences, and the measurement above outranks
  them (EV-2: measurement > inference). Recency is what the practitioner says they would use at period end (churn 83% at
  0-30 days of span vs 32% at 80-92). It is legitimate (USE-3).

**2. The split mirrors the application (P4, SPLIT-1 Must, SPLIT-10 Should, hold)**

* Evidence: the population drifts. Churn falls from 53.0% (2017Q1) to 35.8% (2017Q4), and the type2 channel grows from
  17% to 41%. Within type2, churn falls from 25% to 10% (practitioner). The 3-month gap equals the label window: the
  newest training label (period end 2017-08-31) closes on 2017-11-30, before the December window opens. SPLIT-14
  (3 windows, train >= 53%) and SPLIT-17 (smallest window 63) hold. Precedents: sf_permit_time and
  brazilian_ecommerce (gap = delay).
* Objections answered: the IID alternative (REVIEW issue 2, practitioner) and "small windows". SPLIT-1 and SPLIT-7
  (Must) beat SPLIT-19 (Should). The Tensions row "the right split against the score" (forest_fires) settles size
  against regime.
* Concede, as notes in splits_comment (Should, no re-split possible): every test label window spans the New Year while
  no training one does (SPLIT-20). Nov and Dec are a thin tail of the client intake (123 and 63 clients, 29-38% with
  period_end = last). Also reword "stricter": IID scores 0.817 vs 0.860 temporal.

**3. Label timing: a real wording problem, and the cut already handles it (P3/P4, USE-5, LEAK-24 Must)**

* Concede: the claim audit refutes "three months after the period" for the 63 dropped Apr-Jun 2018 clients (37
  non-churners with full spend). The calendar argument (data end 2 Apr vs opening 27 Apr) does not explain those rows.
* Why the definition still stands: the shipped cohort is cut at 2018-01-01, which is conservative in every reading
  (claim audit, practitioner: "under a calendar reading it does not hurt either"). The kept test months show no
  censoring signature: Sep-Dec 2017 churn is 37.6 / 34.8 / 39.8 / 36.5%. The target (no POS purchase) is what a card
  business acts on (practitioner, USE-5). fit is already `approximate`, the USE-8 outcome for "a label without a stated
  horizon" (alfa_battle_2_0_task_2 precedent).
* Mildest remedy, text only: rewrite the "Cohort" bullet, Decision 2 and the LABELS_COMPLETE_BEFORE comment so they rest
  on the measured March anomaly and an unpublished label construction. Lead fit_reason with "the label window's timing
  is not published, and the newest rows contradict 'after the period'". Reframe REVIEW issue 4 so it no longer depends
  on the draw date.

**4. Faithful data (P5, PROV-13 holds); attributions fixed by wording (PROV-16, EV-2)**

* Evidence: train.csv is byte-identical (sha256 cd19fe25...) to the kianya 2018 GitHub copy. The pinned HF revision
  resolves and its sha matches. 490,513 transactions of 5,000 clients, as stated. Competition dates and metrics were
  checked against the API.
* Concede: two items come from a participant notebook, not from the source: the label quote and the meaning of
  `channel_type`. Remedy: cite them as third party, or write "undocumented; constant per client, read as the
  acquisition channel". `channel_type` stays (LEAK-38). Its per-channel churn is stable across quarters, as a static
  attribute's would be (column audit).

**5. Worth benchmarking (P6, TP-2/TP-3, keep)**

* Evidence: LightGBM AUC 0.859 (skill 0.718). It beats the dummy on 3 of 3 windows, and the smallest class per fold is
  23. `no_spread` (skill gap 0.034, paired SE 0.087) comes from three windows. Like cases kept it:
  heart_disease_cleveland, african_credit_scoring_challenge, electric_motor_temperature_prediction.
* Remedy: refresh the stale numbers (0.045 / SE 0.036) in curation_comments and in the TP-2 Cases row.

**6. In scope as a tabular task (P2, SEL holds); one sentence overstated**

* Evidence: in CoLES Table 6 the designed aggregates score 0.825, above the end-to-end supervised sequence model (0.817)
  and CPC/RTD/SOP (0.782-0.802). Concede: CoLES embeddings + LightGBM reach 0.843. Remedy: rewrite "not clearly beaten"
  to say that, as the claim audit proposes. The tabular framing is a published benchmark's, so scope is unaffected.

**7. Cleaning and feature set are P7: fix cheaply or note, never a reason to drop (principles step 3)**

* CLEAN-21 (Should): amounts in mixed currencies. 22.4% of clients have a non-ruble transaction, and VND/IDR amounts
  run up to 36M. Remedies in order: rewrite the bullet with the client share, or convert to rubles at the Bank of
  Russia's daily rate. Which one is the curator's call. Trees are largely robust to this; it is quality, not validity.
* CLEAN-19 consistency check (precedents #1): concede that REVIEW issue 5 states the alfa precedent backwards. The
  dataset survives either way: (a) an exception once the 2018 top-solution search is documented (CoLES is the
  peer-reviewed baseline), or (b) rebuild like alfa. Both are definition-level changes. The width alternative
  (10/30 codes) is dropped under CLEAN-22 (Must; coad). The scores differ by 0.003, within noise.
* Blind review's "about 200 missing clients": 5,000 - 4,791 = 209, the censoring cut, which is documented. Its
  datetime-encoding point: datetime features are a format the container supports and siblings ship (kickstarter,
  brazilian_ecommerce), so this is not a defect.

**Judgment record (as argued)**

Verdict: ship after text changes.
Validity: SEL holds (wording fix); USE-5 holds, USE-8 approximate (label timing restated); LEAK-10 holds (measured);
LEAK-24 holds (cut C conservative); SPLIT-1/10/14/17 hold; PROV-13 holds, PROV-16 wording fix.
Value: TP-3 `no_spread` kept (three windows; numbers refreshed).
Quality: CLEAN-21 note or conversion (curator); CLEAN-19 exception or alfa-style rebuild (curator); CLEAN-8 accepted.

**Rebuttal**

The critic and I agree on the verdict ("ship only after changes", no exclusion, no leak) and on almost every remedy.
I dispute only the "Effect" paragraph of point 1. The rest I concede.

**1. Label window: concede the text and the test; dispute part of the effect**

* Concede: the definition presents the per-client window as fact, and the newest rows contradict it. The rewrites
  the critic lists are the ones in my point 3: the Cohort bullet, Decision 2, the LABELS_COMPLETE_BEFORE comment,
  fit_reason leading with "not published, newest rows contradict", and REVIEW issue 4. I also accept adding the
  upper-bound argument and the 107/479 test to "Time".
* Concede the EV-1 test (churn against cohort age within channel and month). It is cheap, and USE-5 is a Must, so it
  should run before the text is final.
* Dispute "the gap rests on the wrong timing model":
  - A calendar window inside the file is already ruled out. Among each calendar month's POS buyers, churn stays at or
    above 17.9% (claim audit). Under such a window, buyers in its months would all be non-churners.
  - That leaves a window after the file ends. Then no training label was known any earlier than a test label. The gap
    cannot leak in either reading; at worst it is unnecessary and costs about 0.007 AUC (split audit). A wrong timing
    model makes the split more conservative, not less honest (SPLIT-9 still holds).
* Dispute the cohort-age reading of the date features. Within type1, churn is flat (59% to 54%); the critic accepts
  this too. Without the dates, the AUC is still 0.851 (split audit). The dates add 0.01-0.02 AUC on the shipped split.
  The blind review's 0.04 came from IID-like folds.
* What follows: if the EV-1 test shows churn tracking cohort age within type1, I would concede that "churn" means
  something different for each cohort. The remedy would then be to state the target as "no POS purchase in an
  unpublished window", not exclusion: fit stays `approximate`, as in the USE-8 case alfa_battle_2_0_task_2.

**2. Attributions and CoLES: concede**

This matches my points 4 and 6. Cite the label quote and the `channel_type` meaning as third party. Use the critic's
`channel_type` wording. Correct the CoLES sentence (0.843 vs 0.825; name CPC/RTD/SOP).

**3. Thin, atypical test windows: concede**

This matches my point 2. Add a note to splits_comment covering the intake drop, the share of estimated period ends per
window (11% / 29% / 38%) and the New Year season. No re-split (SPLIT-1, SPLIT-14).

**4. CLEAN-19 against alfa: concede**

REVIEW issue 5 states the alfa precedent backwards and must be corrected. Drop the width argument (CLEAN-22). The
choice between an exception (after a documented top-solution search) and an alfa-style rebuild is the curator's
call. Both keep the dataset.

**5. Currency mixing: concede**

Rewrite the note with the 22.4% client share and the VND/IDR example. Ruble-only overall statistics are an acceptable
cheap fix (P7). The choice between them is the curator's call.

**6. Stale numbers and wording: concede**

Refresh `no_spread` in curation_comments and in the TP-2 Cases row (task_probes.md line 310). Reword "stricter" so it
applies to the design only. Write "for example" for the monthly refit (USE-1).

**Joint position**

Verdict: ship after changes. Every change is to text, except the EV-1 test, which is to be run, and two P7 options for
the curator (CLEAN-19, CLEAN-21). No Must fails: LEAK-10 and SPLIT-9 hold in both label readings, LEAK-24 is met by
cut C, and USE-5 depends on the EV-1 result, with rewording as the remedy.

</details>

<details><summary>Critic</summary>

Position: **ship only after changes.** No leak was found and the task is real; I do not ask for exclusion. The
definition states as fact a label timing that the data contradicts, and several of its texts are wrong or stale.

**1. The label's window is not what the definition says (P3/P4; USE-5 Must, USE-8, LEAK-24 Must)**

* Problem: the definition says churn is "no POS purchase in the three months after the period" and justifies the cut by
  "transactions end 2 Apr, labels published 27 Apr". The rows contradict both. The 63 clients whose period ends
  between April and June 2018, after the transactions stop, still have labels. 37 of them are non-churners with
  full spend (median target_sum 121,887 against 76,081 for all non-churners), which no window after their period
  could have produced by the opening. Churn after December 2017 is not monotone (Jan 29%, Feb 40%, Mar 67%, Apr-Jun
  41%) (claim_audit rows 25 and 20). The practitioner finds that target_sum divided by the period's POS spend rises
  steadily with the cohort (0.40, 0.53, 0.67, 0.72 by 2017 quarter), which also fits a label measured over one
  calendar window.
* Effect: if the window is calendar-fixed, "churn" means something different for each cohort. The three-month gap
  then rests on the wrong timing model, and the date features (worth 0.02-0.04 AUC: claim_audit, blind review item 4)
  partly measure how old the cohort is at a fixed date.
* Counter-evidence I accept: the cut is conservative under either reading. 107 of the 479 clients with POS after
  first + 3 months still churned, so the post-period transactions are not in the label window (no LEAK-10 leak). Churn
  within type1 is flat (59% to 54%), which argues against pure age decay.
* Remedy (fix the definition's text, then decide): keep cut C. Run the test that tells the two readings apart (EV-1),
  e.g. churn against cohort age within each channel and month, and record the result. Rewrite the "Cohort" bullet,
  Decision 2 and the LABELS_COMPLETE_BEFORE comment so they rest on the measured March anomaly, not on the draw date.
  fit_reason should start with "the label's window is not published, and the newest rows contradict a per-client
  window". Reword REVIEW issue 4, whose framing assumes the draw-date premise. Add the upper-bound argument for
  period_end (split_audit) and the 107/479 test to the "Time" bullet, so the LEAK-10 question the precedents raise
  (item 4) is answered in writing.

**2. Evidence attributed to the wrong source (P5; EV-2, PROV-16)**

* The quote "Значение 0 соответствует отказу" is not in the task text (boosters API). It comes from a participant
  notebook (kianya). The meaning of `channel_type` ("how the client was acquired") also comes only from that notebook.
  The API's `filesdescription` is empty (claim_audit, column_audit problem 1).
* CoLES: "not clearly beaten by sequence models" overstates. CoLES embeddings with LightGBM score 0.843 +- 0.003
  against 0.825 +- 0.004 (Table 6), and the cited range 0.817-0.843 leaves out CPC, RTD and SOP.
* Remedy: cite these as third-party, or say "not stated". Write `channel_type` as "undocumented, constant per client,
  read as the acquisition channel" in `known` and curation_comments. Correct the CoLES sentence.

**3. The test windows are thin and atypical, and nothing says so (P4; SPLIT-1, SPLIT-20 Should)**

* Client intake collapses after July 2017 (519, 109, 50 first transactions a month). November (123) and December (63)
  are a tail of late or irregular clients: period_end is the last transaction for 29% and 38% of them, against 11-16%
  in earlier months, and their median transaction counts are 58 and 41 against about 98. So the split axis is least
  reliable in the windows that are scored. All three test label windows span the New Year; no training window does
  (split_audit 1-2; practitioner section 3).
* Remedy: add a note to splits_comment naming the intake drop, the share of estimated period ends per window, and the
  season. No re-split.

**4. The feature set departs from its own precedent without a reason (P7; CLEAN-19 Should)**

* Problem: REVIEW issue 5 says the definition keeps the 97 CoLES codes "as alfa_battle_2_0_task_2 kept its organizers'
  set". alfa did the reverse. The curator replaced the organizers' baseline with the features the top solutions share,
  including 30 MCC codes (CC 2026-10-13; precedents item 1). Nothing records a search for rosbank1's top solutions.
  Issue 5's width argument for 10 or 30 codes breaks CLEAN-22 (Must; coad).
* Remedy: correct issue 5. Then either record an exception to CLEAN-19 with its fact (no top solutions published,
  once the search is written down) or build what the top solutions share. Drop the argument from width.

**5. Amount statistics mix currencies more than the note admits (P7; CLEAN-21 Should)**

* Problem: "2.6% of transactions" is correct, but 22.4% of clients (1,072) have a non-ruble transaction, and 92
  clients' `amount_sum` is mostly in other currencies. The 8 largest amounts in the file are VND or IDR, up to 35.8
  million (column_audit problem 2). kickstarter and alfa convert to one currency (precedents item 3).
* Remedy (mildest): rewrite the note with the client share and the VND/IDR example and record it as an exception
  with a fact. A cheap fix is to compute the overall statistics over ruble transactions only. This is a quality issue,
  not a reason to exclude.

**6. Stale or wrong numbers in the text (writing.md; TP-3)**

* The `no_spread` note says 0.045 AUC with SE 0.036; today's probe gives 0.017 AUC, a skill gap of 0.034 and SE 0.087.
  The same old numbers are in the TP-2 Cases row (task_probes.md line 310).
* "This split is stricter" does not hold for the scores: IID 3 x 3 gives 0.817 and the shipped split 0.860. It holds
  only for the design: on the same test windows, a random training side scores about 0.01 higher (split_audit 4).
* "Refit every month" is our own framing and is written as fact (USE-1).
* Remedy: update the numbers in both places, reword the split sentence, and write "for example" for the refit.

**Rebuttal**

We now differ on one point only: whether text changes are enough for the label timing (advocate 3). On everything
else I concede, or the two briefs already ask for the same remedy.

1. **No leak (LEAK-10).** I concede. My point 1 accepted the same measurement (107 of 479 churners have POS after
   first + 3 months). I only ask that this test and the upper-bound argument go into the "Time" bullet. The advocate
   does not object to that.
2. **Split.** I concede that SPLIT-1 and SPLIT-10 hold, that IID loses, and that SPLIT-20 and the thin tail become
   notes. This matches my point 3.
3. **Label timing. Disputed in part.** I agree on the text rewrite and that cut C stays. I dispute "the cut already
   handles it". The cut protects against censoring. It does not settle what the target measures. Under a calendar-fixed
   window, which the practitioner's rising ratio (0.40 to 0.72 by quarter) fits, two things change:
   * The three-month gap mirrors a refit that does not exist (SPLIT-10).
   * The date features, worth 0.02-0.04 AUC, partly measure how old the cohort is at that fixed date (USE-5).

   The churn rates for Sep-Dec 2017 test censoring, not this. Which rule wins: EV-1 (facts first) before the USE-5
   Must. This is cheap to settle. Measure churn against cohort age within each channel and period-end month, and
   record the result in the definition. If the calendar reading holds, fit_reason must say the gap and the dates
   carry cohort age. That is still a note, not exclusion. If the per-client reading holds, the advocate's text-only
   remedy is enough.
4. **Provenance and attributions.** I concede. We ask for the same remedy.
5. **Value.** I concede. Only the numbers need refreshing.
6. **CoLES scope sentence.** I concede. We ask for the same remedy.
7. **CLEAN-21 and CLEAN-19.** I concede that both are P7 and the curator's call (a or b). Both briefs drop the width
   argument. One addition: for the CLEAN-19 exception the top-solution search must actually be written down first. A
   peer-reviewed baseline alone is not the fact that alfa lacked. The blind review's 209 missing clients and its
   datetime point: I concede, the advocate is right.

Verdict: ship after changes. These are the advocate's text changes plus one measurement (point 3) with its result
written into fit_reason.

</details>
