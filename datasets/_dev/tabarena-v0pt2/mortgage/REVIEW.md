# mortgage

**Outcome:** added. One row per loan and quarter of the Credit Risk Analytics mortgage panel, target the quarter's
status (active, default, payoff), temporal with three one-quarter test windows; the loan state and the macro columns
are lagged to what is known at the quarter's start. Review panel: full tier, 2026-10-20. The changes that needed no decision are made: the balance at the previous-but-one observation
is added (`balance_time_lag_2`), the last row of the 501 loans that leave early without an event is dropped (label not
recorded), the two ids that copy another id are dropped (23 rows), the 37.5% placeholder rate becomes missing, and the
notes give the re-run numbers, the GDP vintage caveat and the level effect's own reason.

```text
Verdict: ship after changes.
Validity: SEL holds; USE-1/USE-5 hold; USE-6/USE-8 triggered, fixed (balance_time_lag_2 added, fit stays direct);
  USE-3 triggered for the 8,132 rows with time == orig_time (24 in test), remedy open (issue 10); LEAK-10 holds
  (loan state and macro lags proven; GDP vintage a caveat with no measured effect); LEAK-25 triggered, fixed (the
  last row of the 501 loans that leave early without an event dropped); LEAK-20 departed from for 7 rows (issue 13);
  LEAK-34 by design (USE-10); SPLIT-1/3/9/11/12/14/19/21 hold.
Value: TP-2, a real signal over the previous quarter's class shares in 3 of 3 windows; the quarter's level is 74-83%
  of LightGBM's gain (issues 11 and 2).
Quality: LEAK-19 two copied ids dropped (23 rows); CLEAN-10/11 the 37.5% placeholder masked; LTVs above 300%
  kept (issue 15); CLEAN-13 wording (issue 12); notes corrected (EV-8).
Weighed: source +, 3-class signal over the previous quarter's shares +, use case +, level effect -, licence noted (EV-4).
For the curator: issue 10 (reword or drop the origination-quarter rows), issue 13 (LEAK-20 exception), issue 11
  (the balance ratio), issue 2 (3 classes or a default companion), issue 12 (CLEAN-13 wording), issue 15 (LTVs
  above 300%).
```

**Main points:** Reword the use case or drop the rows of a loan's origination quarter (issue 10); confirm the
period-51 exception to LEAK-20 (issue 13); ship the balance ratio as a built column (issue 11); keep the 3-class
target alone or add a default-only companion (issue 2); amend CLEAN-13's wording (issue 12); keep or mask the LTVs
above 300% (issue 15); a market mortgage rate (issue 14).

**Record judgment:** valid. Real loan-level US RMBS data from the book's data page, used by the book itself for a
competing-risks model and an out-of-time backtest; no larger source exists. The row's own loan state and the
quarter's own macro values leak, and the lags that fix them are proven (the periods match public house-price and
unemployment series in exactly one calendar alignment, 2000 Q2 onward). The open points are the origination-quarter rows (issue 10) and how much the quarter's overall
event rate drives the score (issues 11 and 2).

**Issues for Lennart:**

10. **Score a loan in the quarter it is originated, or drop those rows?** 8,132 rows after the drops (8,145 in the panel's reports; 24 in the test windows) have
   `time == orig_time`: the loan was originated during the quarter it is scored for. `use_case` says "At the start
   of each quarter, a lender scores every mortgage it holds", and the lender did not hold these loans at the
   quarter's start; their origination terms did not exist yet. Their payoff rate is 8.0%, against 4.3% overall.
   - Effect: under 0.1% of the test rows, but `use_case` and `known` are false for them as written.
   - Implemented: the rows are kept and `use_case` is unchanged.
   - Alternative (a), the advocate's: reword `use_case` and `known` to say that a loan is also scored in the quarter
     it joins the book, with a shorter horizon. Nothing on these rows postdates joining the book, and the same
     reasoning covers the first panel row of every loan (about 50,000 rows, 66 in test), when a loan enters the pool
     during the quarter.
   - Alternative (b), the critic's: drop the 8,132 rows. Cost: real early payoffs leave, and the other first panel
     rows keep the same question.
   - Rule: USE-3 (Must). Both remedies fix the definition and sit on the same rung of the remedy ladder, so this is a
     framing call. What settles it: does the holder of a mortgage book score a loan from the quarter it joins the
     book? US lenders must book an expected-loss allowance (CECL) from the day a
     loan joins the book, which suggests yes; then (a). The mediator leaves the choice to the curator;
     the AI recommends (a).
   - Decision: reword the use case (a), or drop the rows (b).

13. **Confirm the period-51 exception to LEAK-20?** Period 51 is doubled for 312 loans. For 7 loans the two copies
   differ only in the status (active and payoff), and the definition keeps the payoff copy.
   - Rule: LEAK-20 (Should) drops both copies of rows with the same features and different labels (jm1 dropped all
     copies).
   - The fact that sets it apart: all 7 loans end at period 51, so the second copy is damage to the file (PROV-13),
     not an ambiguous label. Effect: 7 rows, all in train.
   - Implemented: the payoff copy kept, with the fact in the notes. Alternative: drop both copies.
   - The same rule also covers 2 pairs of different ids that match in one quarter with different status (4 rows,
     kept as separate loans); the decision covers them too.
   - Recommendation: record the exception (the precedent checker calls it reasonable).
   - Decision: record it as an exception to LEAK-20, or drop both copies.

11. **Ship the ratio of the two lagged balances as a built column?** The data has no delinquency field. A balance
   that stops falling between two observations is a stand-in for a missed payment, and the definition now ships both
   balances (`balance_time_lag_1`, `balance_time_lag_2`), so a model can find it.
   - Effect: without the ratio, models rank loans' default risk weakly (AUC 0.57-0.66) and most of the score is
     the quarter's overall rate; a real lender would have the payment history.
   - Evidence (the mediator's runs, untuned LightGBM, periods 60 / 59 / 58): adding the raw `balance_time_lag_2`
     alone barely moves the log loss (0.1200 / 0.1321 / 0.1359 to 0.1201 / 0.1315 / 0.1357). Adding the ratio
     `balance_time_lag_1 / balance_time_lag_2` gives 0.1179 / 0.1271 / 0.1287, and the default ROC AUC rises from
     0.57-0.66 to 0.76 / 0.85 / 0.82; the per-loan gain over the previous quarter's class shares roughly doubles, to
     0.007-0.010.
   - Implemented: the raw `balance_time_lag_2` only (re-run of the changed definition: log loss 0.1200 / 0.1324 /
     0.1359).
   - Alternative: add the ratio (or the difference) as a column. For: it is what a credit modeller builds from the
     balance path, a stand-in for days past due (CLEAN-19, third bullet). Against: the information is already in the
     two raw lags, and our rule for expert-built columns is to add as few as possible; the benchmark could leave models to find it. The blind reviewer
     asks the same for loan age and remaining term.
   - Rule: CLEAN-19 (Should), a weighing call. USE-6 and USE-8 hold either way (fit direct).
   - Recommendation (the AI's own call): add the ratio. It is known at the quarter's start, it is the column a credit
     modeller would build, and it moves the task from the quarter's level toward ranking loans (default AUC
     0.76-0.85 against 0.57-0.66).
   - Decision: raw lag 2 only, or raw lag 2 plus the ratio or the difference.

2. **Target: 3 classes alone, or also a default-only companion?**
   - Implemented: `status` (active / default / payoff), the record's multiclass and the R Companion's chapter 11 model (not
     verified: we found no copy of the R Companion).
   - What the 3-class log loss measures (re-run of the changed definition; all-history class shares / previous
     quarter's class shares / LightGBM): 0.1461 / 0.1251 / 0.1200 in period 60, 0.1561 / 0.1385 / 0.1324 in 59,
     0.1567 / 0.1394 / 0.1359 in 58. So 74-83% of LightGBM's gain is the quarter's overall event rate, which the
     previous quarter's shares already give; the per-loan part is 0.0035-0.0061. Without `time`, LightGBM loses to
     the previous quarter's shares in 2 of 3 windows. With the ratio of issue 11 the level falls to 62-74% of the
     gain (mediator).
   - For keeping 3 classes alone: the practitioner wants calibrated probabilities for all three classes; the
     quarter's level is part of a PD model's job, and log loss is a proper score (EV-5). The notes now give this
     reason.
   - Alternative: a separate folder (for example `mortgage_default`), binary `default_time` scored by ROC AUC, the
     book's chapter 6 models and chapter 13 backtest. It ignores the level and treats payoffs as non-events; 43-77
     defaults per window, LightGBM default AUC 0.57 / 0.66 / 0.60 without the ratio. PROV-6/PROV-7 allow a companion
     as a distinct task.
   - Rule: USE-5 (Must) holds for both forms; TP-2 (Should), a weighing call. african_credit_scoring_challenge kept
     its drift flag because its metric (ROC AUC) ignores the level; that reason does not carry over to a log loss.
   - Recommendation: keep the 3 classes alone if issue 11 adds the ratio (the quarter's level then carries 62-74% of
     the gain); otherwise weigh the companion again. This issue depends on issue 11.
   - Decision: after issue 11, keep 3 classes alone, or add the companion.

12. **Amend CLEAN-13's wording for flag blocks with a reference level?** `real_estate_type` merges three property
   flags of which at most one is set; 19.5% of the rows have none and become `other`. The merge is lossless.
   CLEAN-13 (Must) allows a merge only when exactly one flag is set in every row. onlinenewspopularity
   (`data_channel`) uses the same reading, an AI decision of the 2026-10-07 run that no curator has decided yet.
   - A Must takes no exception, so both the advocate and the critic propose the wording "exactly one, or at most
     one with a reference level `other`".
   - Alternative: split both blocks (mortgage and onlinenewspopularity) back into separate yes/no columns.
   - Recommendation: amend CLEAN-13 (the advocate and the critic agree).
   - Decision: amend CLEAN-13, or split both blocks.

15. **Keep the 37 LTVs above 300%, or make them missing?** 37 values of `LTV_time_lag_1` lie above 300% (up to
   803.5%; 3 in the test windows). They come from 38 balances far above the loan's original balance (for example
   570,000 on an original 60,495), so the balance or the original balance is wrong, and the data cannot tell which.
   - Effect: a handful of rows with an implausible loan-to-value; no measurable effect on the score.
   - Implemented: kept as recorded, with that fact in the notes.
   - Alternative: make these LTVs (and the conflicting balances) missing, as caracas_cervical_cancer and
     churn_telco_south_asia did with implausible values.
   - Rule: CLEAN-11 (Should): impossible values become missing, unusual ones stay. The note's own reason (one of the
     two values is wrong) points to impossible.
   - Recommendation (the AI's own call): make them missing, following the CLEAN-11 cases.
   - Decision: keep, or make missing.

14. **Add a market mortgage rate as the refinance incentive?** Optional. Payoffs follow the gap between the loan's
   rate and the market rate, and the source has no market rate. Since the periods are dated, a FRED series
   (MORTGAGE30US), lagged to its publication, could be joined (the practitioner's third gap).
   - It is an addition from outside the source, and neither the advocate nor the critic argued for it.
   - Rule: none requires it; an outside column is the curator's call (practitioner, gap 3).
   - Implemented: not added. The AI recommends leaving it out.
   - Decision: add it, or leave it out.


**Review panel:** ship after changes (mediator). Full tier, 2026-10-20. Claim audit: 87 claims; refuted or out of
date: the loan key, "no known risk", the distance AUC and four numbers or wordings (all fixed); untested: the GDP
vintage and the R Companion code (both noted in the definition). Blind review: include with changes; main concern
the weak, imbalanced signal under strong drift. Debate: agreed on the task, the lags, the split, adding the
previous-but-one balance, dropping the unrecorded exits and the cleaning fixes; disputed: the origination-quarter
rows (issue 10). The mediator's issues 1-6 are issues 10, 11, 2, 12, 13 and 14 here; the reports' issue numbers
of the earlier REVIEW.md are the old ones (its issues 1, 3, 4, 5, 7 and 8 are closed).

<details><summary>Mediator</summary>

**mortgage: mediator (review panel, phase C, 2026-10-20)**

Inputs: the phase-A reports, both briefs and rebuttals, `dataset.py`, the README, the record and the earlier REVIEW.md.
New experiments, setup: the definition's
`_clean` on the raw file, the shipped windows (periods 60/59/58, each trained on all earlier periods), untuned
LightGBM with `n_jobs=4`, and thread caps of 4.

**Recommendation**

```text
Verdict: ship after changes.
Validity: SEL holds; USE-1/USE-5 hold; USE-6/USE-8 triggered, fixed by shipping the previous-but-one balance (fit
  stays direct); USE-3 triggered for the 8,145 rows with time == orig_time (24 in test), remedy open (issue 1);
  LEAK-10 holds (loan state and macro lags proven; GDP vintage a caveat with no measured effect); LEAK-25 triggered,
  fixed (drop the last row of the 501 loans that leave early without an event); LEAK-34 by design (USE-10);
  SPLIT-1/3/9/11/12/14/19/21 hold.
Value: TP-2, a real signal over the drift constant in 3 of 3 windows. With the balance change the level falls from
  76-86% to 62-74% of the gain (issue 2).
Quality: LEAK-19 drop 2 identical id pairs (23 rows); CLEAN-10/11 mask the 37.5% placeholder; CLEAN-13 wording
  (issue 4); notes corrected (EV-8).
Weighed: source +, multiclass gap +, use case +, level effect - (smaller after the fix), licence noted (EV-4).
For the curator: 1 drop or reword the time == orig_time rows; 2 ship the balance change as a built column;
  3 the 3-class target or a mortgage_default companion; 4 amend CLEAN-13; 5 confirm the LEAK-20 exception.
```

**Changes to make now (agreed by both sides, or settled by rule or measurement)**

1. **Add `balance_time_lag_2`**, the balance at the loan's previous-but-one observation. In `known`, say there is no
   delinquency field, so the payment history comes only through the two lagged balances. Keep `fit="direct"` and
   re-run the probes. Rules: USE-6, USE-8 (Must), CLEAN-19. The form of the column is issue 2.
2. **Drop the last row of every loan that leaves before period 60 without an event** (501 rows, 98 of them in test).
   Write it as "label not recorded, rows dropped (LEAK-25, CLEAN-15)", not as "recording process recovered". The
   codebook says that unrecorded exits exist, not which rows they are (EV-7). Remove the bullet "keep their last row
   `active` as recorded". Rules: LEAK-25, CLEAN-15 (Must).
3. **Drop the second id of 35309/35310 and of 3018/3020** (23 rows, all in train). The two ids match in every column
   over 15 and 8 quarters. Correct the duplicates bullet. Rules: LEAK-18/19 (audiology_diagnosis).
4. **Mask `interest_rate_time == 37.5` before the lag** (44 loans, all period 22, a placeholder). Keep the 37 LTVs
   above 300%, with a note that they come from 38 balances that conflict with the original balance. Rules: CLEAN-10,
   CLEAN-11.
5. **GDP vintage: a caveat, not a kept-leak note.** Add to `known`/`fit_reason`: "GDP figures may carry later
   revisions; vintage unknown". Keep `fit="direct"`. Measured: dropping `gdp_time_lag_2` changes log loss by -0.0007,
   -0.0004 and -0.0001, so the model does no better with it, and no revision signal reaches the score. This follows
   sberbank (fit direct, publication caveat in `fit_reason`). Rules: LEAK-10 (weak, untested), EV-1, EV-7.
6. **Level effect:** after change 1, write it in `curation_comments` with its own reason: the quarter's level is
   part of a PD model's job, and log loss is proper (EV-5). Do not borrow african_credit_scoring_challenge's reason.
   Update the TP-2 numbers from the re-run. In the record, replace "no known risk". Rules: TP-2, EV-8.
7. **Loan key:** fix the docstring and bullet. 59 ids carry two keys, and 44 of them are one mortgage with a revised
   origination field (all in train). Rules: PROV-4, writing.
8. **Numbers and wording** (EV-8, writing):
   - distance AUC 0.525, not 0.58;
   - LightGBM numbers from the re-run;
   - `LTV_time` is missing on the 270 zero *original*-balance rows;
   - 44/38 rows in the source columns, 41/37 in the shipped ones;
   - "previous observation", not "previous quarter";
   - in the origination-fields bullet, give the `Interest_Rate_orig_time` and `mat_time` numbers (freezing them
     changes log loss by -0.0001 to -0.0002);
   - mark the R Companion ch. 11/13 quotes unverified (PROV-16/17).
9. **Notes:**
   - SPLIT-20: train and test are a closed, ageing run-off cohort, with a seasoned pool added at period 52;
   - the source does not state its default definition;
   - the period-51 bullet names LEAK-20 and the fact: all 7 loans end at 51.
10. **REVIEW.md:**
    - close issue 1 (the lag is required: LEAK-10, LEAK-6);
    - close issue 3 (one-quarter windows: quarterly refit, SPLIT-12; scores may not decide, SPLIT-21);
    - close issue 4 (per-series lags; the alternative breaks LEAK-10);
    - close issue 5 (stale, settled 2026-10-19);
    - close issue 8 (consistent, alfa_battle_2_0_task_2);
    - replace issue 7 with changes 2 and 3.

**Issues for the curator (ranked)**

1. **`time == orig_time` rows (P3, USE-3 Must; small).**
   - Problem: 8,145 rows (24 in test, payoff 8.0% against 4.3%) are loans originated during the quarter they are
     scored for. Under the current `use_case` ("at the start of each quarter ... every mortgage it holds"), their
     origination terms did not exist at the prediction point.
   - Effect: under 0.1% of test rows, and `use_case`/`known` are false as written.
   - Critic: drop them, or reword. The lender did not hold them at the quarter's start.
   - Advocate: reword. A holder scores loans as they join the book, nothing on the row postdates joining, and the
     same logic covers all 50,002 first panel rows.
   - Both remedies fix the definition and sit on the same rung of the ladder, so this is a framing call.
   - What settles it: does the actor score a loan in the quarter it joins the book, for the rest of that quarter?
     CECL's day-1 allowance suggests yes. If so, reword and note the shorter horizon. If not, drop.
2. **Ship the balance change as a built column? (P3 fit / P7, CLEAN-19 Should; weigh).**
   - New measurement:
     - adding the raw `balance_time_lag_2` alone barely moves untuned LightGBM: log loss 0.1200/0.1321/0.1359 becomes
       0.1201/0.1315/0.1357;
     - adding the ratio `balance_time_lag_1 / balance_time_lag_2` gives 0.1179/0.1271/0.1287, and default AUC rises
       from 0.57-0.66 to 0.76/0.85/0.82;
     - the per-loan gain over the drift constant roughly doubles, to 0.007-0.010;
     - the stalled flag alone gives default AUC 0.58/0.75/0.72 (periods 60/59/58).
   - For the ratio: it is what a credit modeller builds from the balance path, a stand-in for days past due
     (CLEAN-19, third bullet).
   - Against it: the information is already in the two raw lags, and the benchmark could leave models to find it
     (expert state means minimal).
   - Decision: raw lag 2 only, or raw lag 2 plus the ratio or the difference.
3. **3-class target or a `mortgage_default` companion (P3 USE-5 / P6 TP-2; weigh).**
   - Both forms are the source's. PROV-6/7 allow a companion as a distinct task.
   - Against keeping 3 classes alone: the level carried 76-86% of the gain.
   - For it: with the ratio the level carries 62-74%, and the practitioner wants calibrated probabilities for all
     three classes.
   - What settles it: the per-loan share after issue 2 is decided.
4. **Amend CLEAN-13 (P7, Must wording).**
   - `real_estate_type` (at most one flag set; 19.5% `other`) and onlinenewspopularity are lossless dummy codings
     with a reference level, which the rule's text does not cover.
   - A Must takes no exception. Both sides propose the wording "exactly one, or at most one with a reference level
     `other`".
   - Decision: amend, or split both blocks into separate flags.
5. **Confirm the LEAK-20 exception (P4, Should; tiny).**
   - Period 51 keeps the payoff copy of 7 pairs that differ only in status.
   - The fact: all 7 loans end at 51. It is PROV-13 damage, not ambiguous labels (jm1 dropped all copies).
   - Decision: record it as an exception.
6. **Optional:** a publication-lagged market mortgage rate (FRED) as the refinance incentive (practitioner, gap 3).
   It is an addition from outside the source. Neither brief argued for it.

**Agreed facts**

- The data is real loan-level US RMBS data (50,000 borrowers, periods = 2000 Q2-2015 Q1). Only 1 of 9 alignments fits
  (Case-Shiller month 3, median difference 0.002; UNRATE month 1, 59/60 exact).
- `hpi_orig_time` equals `hpi_time` at origination on 100.00% of rows.
- The row's own loan state leaks: lagging it costs 0.003-0.005 log loss in every model family (LEAK-6).
- The temporal known-entity split is right. Train is exactly the earlier periods, and 99.4-99.9% of test rows have
  history in train. No lags in test are stale, and no exact copies cross the split.
- There are no hidden groups: IID and loan-grouped random splits tie at log loss 0.2607.
- Every class is scorable in every window: 43-77 defaults and 145-165 payoffs.
- Shipped LightGBM beats the previous quarter's shares in 3/3 windows (0.1192/0.1320/0.1363 against
  0.1251/0.1374/0.1391). Without `time` it loses in 2/3.
- `mat_time` and the other origination fields carry no leak: freezing them changes log loss by -0.0001 to -0.0002.
- 501 loans leave early without an event. 7.7% of their last rows have a zero balance, against 2 of 533,608 other
  active rows. 98 of them are in test.
- Ids 35309/35310 and 3018/3020 are identical (23 rows, all in train).
- 37.5% is a placeholder rate (44 loans, period 22).
- The label-free distance AUC is 0.525, against 0.92 for HMEQ.
- Both sides: ship after changes. No retirement and no change to the windows (SPLIT-21). The licence is noted, not
  weighed (EV-4).

**Consistency with precedent**

- **Followed:**
  - garments (lag a same-period state);
  - lending_club (quarterly windows);
  - aeolus (SPLIT-21);
  - audiology_diagnosis (drop identical copies);
  - the CLEAN-11 cases (caracas, churn_telco_south_asia: implausible values to missing);
  - alfa_battle_2_0_task_2 (undoing non-personal masking);
  - lucas_topsoil (licence);
  - sberbank (unknown publication timing as a caveat with fit direct; change 5).
- **ghanas_indigenous_intel** (LEAK-25, retired). What sets mortgage apart: about 0.08% of rows against 37%, and the
  unrecorded rows can be filtered, so the Must is met by fixing the definition, not by an exception.
- **african_credit_scoring_challenge:** its reason for keeping the drift flag (an AUC metric ignores the level) does
  not transfer, because mortgage is scored by log loss. Change 6 gives mortgage its own reason.
- **onlinenewspopularity / CLEAN-13:** the same reading for two datasets. That calls for an amendment, not a silent
  departure (issue 4).
- **jm1 (LEAK-20):** the departure is backed by a stated fact (issue 5).
- **Open on another dataset:** the precedent checker's consistency check on sberbank's unlagged macro columns.
  mortgage lags because its series and release lags are identified, and sberbank's are not. That is for sberbank's
  review and does not block mortgage.

</details>

<details><summary>Claim audit</summary>

**mortgage: claim audit (adversary, panel phase A, 2026-10-20)**

Scope: `datasets/_dev/tabarena-v0pt2/mortgage/dataset.py`, its README, `curation/records/mortgage.md`, the panel's
`claims.md` (87 claims), probes and prep measurements. Raw file: mortgage.csv
(sha256 matched by prep).

**Table**

| # | claim | source | test (could refute) | result | evidence | rule |
|---|---|---|---|---|---|---|
| 6, 57, 71 | periods are quarters 2000 Q2-2015 Q1 | task_summary.row, comments, record | match per-period `hpi_time` / `uer_time` against SPCS10RNSA / UNRATE for start 2000Q1/Q2/Q3 x month 1/2/3 of the quarter (9 alternatives) | holds (proof) | only 2000Q2 fits: hpi = month 3, median abs diff 0.002 (max 0.114); every other alignment median 1.47-6.79; UER = month 1, 59/60 exact; every other alignment 2-19 exact | EV-1, EV-2 |
| 33-35, 47, 87 | hpi = quarter's last month, UER = first month; lags uer t-1, gdp/hpi t-2 are the newest published at quarter start | MACRO_LAGS docstring, comments, decision 3 | the month mapping above (a wrong month would make the lag too short) | holds (mapping proven; release calendars are inference: Case-Shiller ~2 months after the month, BLS first Friday of the next month, BEA advance ~1 month after the quarter) | see row above | LEAK-10, USE-3 |
| 12, 15, 18 (GDP part) | GDP growth "as published by the quarter's start" | task_summary.known/changes/fit_reason | compare file values with a dated vintage | untested | file's period-60 GDP 2.84 vs FRED current 4.0 (prep, the earlier REVIEW.md 4); vintage of the file unknown, so values may carry later revisions | LEAK-10 (weak), EV-7 |
| 49 | `hpi_orig_time` is the origination quarter's index, published two quarters later | comments | `hpi_orig_time` == `hpi_time` at `orig_time` + k, k = -1, 0, 1 | holds | k=0: 100.00% of 605,991 rows; k=+-1: 0.0% | LEAK-10 |
| 18 (implied: every feature known at quarter start), 58 | origination fields that change within a loan carry no event information | fit_reason; comments "kept as recorded" | rows where a field differs from the loan's previous row: event share vs the share expected from each row's period | holds for FICO, rate, LTV_orig, property type; **maybe a weak leak for `mat_time`** | Interest_Rate_orig 4,775 rows 5.49% vs 6.13% expected; FICO 384 rows 8.07% vs 6.87%; REtype_SF 51 rows 7.84% vs 7.81%; **mat_time 959 rows 1.46% vs 4.96% expected, 63 of them in test periods 58-60** (a maturity change on the row itself, likely a modification recorded in its own quarter; when the source updates it is undocumented) | LEAK-10/LEAK-11, EV-6 |
| 32, 55 | "a few ids hold two mortgages", so a loan is id + orig_time + balance_orig_time | LOAN_KEY docstring, comments | per id with more than one key: do fragments share maturity and FICO (one mortgage) and overlap in time? | **refuted** | 59 ids with 2+ keys; 44 share `mat_time` and `FICO_orig_time` across fragments (one mortgage with a revised `orig_time` or balance, e.g. id 11422: orig 18 then -14, same balance 144,800, mat 106, FICO 716); 11 of these overlap in time (54 rows where an id appears twice in one period, none in 58-60); 56 of 59 first fragments end `active` while the loan continues under the other key | PROV-4/6 (one copy), LEAK-16, CLEAN-3; writing |
| 50, 51 | period 51 doubled for 312 loans; payoff copy kept because the loan leaves | comments | do the 7 (0,2) pairs' loans have rows after 51? do (0,0) pairs continue? | holds | all 7 (0,2) loans end at 51; 302/302 (0,0) loans continue after 51 | LEAK-16 |
| 31, 26, 5, 37 | status codes quoted; two SAS formats; 50,000 borrowers | STATUS docstring, download_description, row | read the data page | holds | page: "status_time: Default (1), payoff (2), and nondefault/nonpayoff (0) observation at observation time"; mortgage_9.4.rar, mortgage_earliersas.rar, mortgage_csv.rar; "50,000 residential U.S. mortgage borrowers over 60 periods"; "The periods have been deidentified" | EV-2 |
| 11, 43 | balance, rate, LTV "at the previous quarter" | task_summary.known (comments say "previous observation") | gap between a row and its loan's previous row | holds for 99.8%; wording loose | gaps: 1 quarter 570,872 rows; 2-9 quarters 1,250 rows | writing |
| 83, implied LEAK-24 | the quarter's status is known when the next starts; no right-censored labels at the end | splits_comment | default share per period near the panel end (a recognition lag would show a cliff in 59-60) | holds weakly (shape only; default definition not documented) | default share 2.34% (48), 1.62 (52), 0.95 (54), 0.66 (56), 0.56 (57), 0.91 (58), 0.64 (59), 0.54 (60): a gradual decline, no cliff | LEAK-24, SPLIT-9 |
| implied | no row is a copy across the split | — | leak probe exact-copy rate; same-id parallel rows in test | holds | test rows with an exact feature copy in train 0.0% (probe); 0 same-id duplicate-period rows in 58-60 | LEAK-16 |
| 82 | 99.4-99.9% of test rows have earlier quarters in train | splits_comment | prep count | holds | 99.93 / 99.88 / 99.38 (prep) | SPLIT, LEAK-34 |
| 65 | LightGBM (full train) beats previous-quarter shares in each window; period 60 0.1195 vs 0.1251 | comments | prep's full-train run | holds; number drifted | 0.1192/0.1320/0.1363 vs 0.1251/0.1374/0.1391; **without `time` it loses in 2 of 3** (0.1298 vs 0.1251; 0.1406 vs 0.1391) | TP-1, TP-2, EV-8 |
| 62 | label-free NN distance AUC 0.58 for default | comments | probe on the current definition | **refuted (stale number)** | 0.525 for default and payoff (first split, 50k cap, seed 0) | EV-8 |
| 53 | `LTV_time` missing on exactly the zero-balance rows | comments | prep cross-tab | **refuted as worded** | missing on the 270 zero *original*-balance rows, not the 324 zero current-balance rows | writing, EV-7 |
| 59 | rates > 25% 44 rows, LTV > 300% 38 rows | comments | prep count | holds for the source columns; shipped lagged columns 41 / 37 | prep | writing |
| 52 | zero -> missing 89,990 / 270 / 25 rows | comments | prep count after dedup | holds | prep | CLEAN |
| 80, 3, 20, 40 | the book's R Companion: ch. 11 competing risks, ch. 13 backtest `time < 60` vs `> 59` | splits_comment, use_case, comments | find the code text | untested | two web searches found no copy; not on the book's data page | PROV-16/17, EV-7 |
| 70 | no larger source exists; IFR site gone | record assessment | — | untested (not re-run) | the data page calls it "a randomized selection ... provided by International Financial Research" | PROV-1, EV-7 |
| 76 | "no known risk" (priority 5) | record assessment 2026-10-20 | compare with the folder's open issues | **refuted as worded** | the earlier REVIEW.md ships "with concerns" (level effect, macro vintage), and the same assessment names the level effect | writing, principles (judgment record) |
| 17, 19 | fit direct; outcome within the quarter | task_summary | — | holds (use-case mirror); the value caveat is TP-2 (level ~76-86% of the gain, prep) | — | USE-1, TP-2 |
| 68 | record tag Non-IID (Temporal) agrees with the definition | front matter | read | holds (the earlier REVIEW.md's "Grouped" disagreement is gone) | — | — |

All other claims (1, 2, 4, 7-10, 13-14, 16, 21-30, 36, 38-39, 41-42, 44-46, 48, 54, 56, 60-61, 63-64, 66-67, 69, 72-75,
77-79, 81, 84-86) were checked by the prep measurements or the checklist and I found nothing to add; I did not re-run them.

**Refuted, ranked (validity first, Must first)**

1. **Claims 32/55, the loan key (P5, PROV-4/6 and LEAK-16; Should-level by size).** Of 59 ids with two keys, 44 are one
   mortgage split by a revised `orig_time` or original balance (same maturity and FICO); 11 run in parallel (54 rows,
   all in train). Effect: the first fragment ends `active` although the loan continues (56 of 59), the second fragment's
   first row has no lags, and 54 train rows are near-copies. Under 0.01% of rows, none in the test windows, so no
   score effect. Mildest remedy: correct the docstring and the bullet ("59 ids carry two keys; 44 of them are one
   mortgage with a revised origination field"); optionally key loans on id + mat_time + FICO.
2. **Claim 76, "no known risk" (procedure).** It contradicts the folder's own concerns. Remedy: reword the assessment.
3. **Claim 62, AUC 0.58 (EV-8).** Measures 0.525 now. Remedy: update the number (conclusion unchanged).
4. **Claim 53, "zero-balance rows" (writing).** Remedy: "zero original-balance rows (270)".
5. **Claim 65 number (EV-8), claim 59 counts, claim 11 wording.** 0.1195 -> 0.1192; 44/38 are the source columns
   (shipped 41/37); "previous quarter" is "previous observation" for 1,250 rows. Remedy: wording.

**Untested or weak, ranked**

1. **`mat_time` updated on the row itself (P4, LEAK-10/11; maybe a weak leak).** 959 rows where maturity changes carry
   1.46% events against 4.96% expected for their periods; 63 are in the test windows. If a modification is recorded
   in the quarter it takes effect, the row shows part of that quarter. Settling test: score LightGBM with `mat_time` as
   shipped vs the loan's previous-row `mat_time` on the three windows. Mildest remedy: lag `mat_time` like the loan state
   (or keep with a `Potential leak, kept on purpose:` note).
2. **GDP vintage (P4, LEAK-10, weak).** The file's values are not the first release; the "as published" claim
   cannot be verified. Remedy: a note (already REVIEW issue 4).
3. **R Companion code (claims 3, 20, 40, 80; PROV-16/17).** Not readable; mark the quote "unverified" or cite the book
   text.
4. **Claim 70, no larger source.** Not re-checked.
5. **Value (TP-2, weigh, not a refutation):** the per-loan gain over the drift constant depends on `time`; without it
   LightGBM loses to the previous quarter's shares in 2 of 3 windows. This sharpens REVIEW issue 2.

**Held under a refuting test (the strong ones)**

Quarter dating and the month inside the quarter (only 1 of 9 alignments fits), therefore the macro lags; `hpi_orig_time`
mapping (100.00%); period-51 dedup choice (7/7 payoff loans end at 51); no label cliff at the panel end; no copies
across the split; origination fields other than `mat_time` carry no period-adjusted event signal.

</details>

<details><summary>Column audit</summary>

**mortgage: column audit (review panel, phase A, 2026-10-20)**

Frame: `dataset_io.from_definition` (origin `definition`), 622,177 rows x 18 columns. Prediction point (first bullet):
the start of each quarter, a lender scores every loan it holds. Codebook: the variable list on the book's data page
(http://www.creditriskanalytics.net/datasets-private2.html, fetched today).

Codebook notes that matter here (verbatim on the data page): "Loans may originate before the observation period
begins ... as in securitization"; "Observations may be censored when loans mature or borrowers refinance"; "The periods
have been deidentified".

**Column table**

| column | meaning (codebook) | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| `time` | "Time stamp of observation" (period 1-60) | yes, the quarter scored | int64 period number; split key | fine (carries the quarter's level, REVIEW issue 2) | LEAK-34, CLEAN-14 note |
| `orig_time` | "Time stamp for origination" (-40 to 60) | yes, except rows with `time == orig_time` (8,145 rows, 1.3%; 24 test rows): the loan is originated during the quarter, so it is not held at the quarter's start; payoff 8.0% there vs 4.3% base | int64 period; varies within 49 ids (89 rows) | question (cohort at the prediction point) | USE-3, LEAK-22 |
| `first_time` | "Time stamp for first observation" | yes; equals the id's first panel row on 100% of rows (a past fact). The first panel row (50,002 rows, payoff 6.1%, default 1.25%) is the quarter the pool acquires the loan: same cohort question as above, 66 test rows | int64 period; 45 rows (4 ids) with `first_time < orig_time` (observed before origination: impossible) | fine; 45 impossible rows minor | CLEAN-11 |
| `mat_time` | "Time stamp for maturity" | yes; changes within 814 ids (1,003 rows, modifications?), change rows not event-enriched (default 1.1%); lagging it changes nothing (below) | int64 period; 1 row with maturity = origination | fine | LEAK-10 tested |
| `balance_time_lag_1` | "Outstanding balance at observation time", at the loan's previous observation | yes | float64; missing on first rows (50,002) + 57 rows where the loan key restarts because `orig_time`/`balance_orig_time` change within an id; previous observation can be >1 quarter back (1,237 gap rows); 38 rows >3x the original balance (up to 570,000 on an original 60,495) | fine; 38 inconsistent rows | CLEAN-11 |
| `LTV_time_lag_1` | "Loan-to-value ratio at observation time, in %", recomputed from the previous balance and the index as published | yes (source formula reproduces `LTV_time` on 100% of non-missing rows, checklist) | float64; 37 rows >300% (max 803.5) all from the balance/original-balance inconsistency above | fine; 37 rows follow the balance problem | CLEAN-11 |
| `interest_rate_time_lag_1` | "Interest rate at observation time, in %", previous observation | yes | float64; zero -> missing (25). **41 rows of 37.5%, all in period 23**: the source holds 37.5 in period 22 for 44 loans (their first row, origination rate 0) and 6.1-6.5% from the next row on: a placeholder, not a rate | cleaning problem (placeholder kept) | CLEAN-10, CLEAN-11 |
| `hpi_time_lag_2` | "House price index at observation time" (Case-Shiller 10-city NSA, quarter's last month), two quarters back | yes (published ~2 months after the month) | float64; missing for periods 1-2 (812) | fine | LEAK-10, LEAK-7 |
| `gdp_time_lag_2` | "GDP growth at observation time, in %", two quarters back | yes (advance estimate ~1 month after the quarter); vintage unknown (REVIEW issue 4) | float64; missing for periods 1-2 | fine; vintage question stays | LEAK-10 |
| `uer_time_lag_1` | "Unemployment rate at observation time, in %" (quarter's first month), one quarter back | yes (lag 1 is even conservative) | float64; missing period 1 (283) | fine | LEAK-10 |
| `real_estate_type` | REtype_CO / PU / SF flags ("=1, otherwise=0"), `other` where none set (19.5%) | yes (origination) | category, 4 levels; no row has two flags, so lossless; `other` is our label, the codebook names no fourth type; status rates flat across levels | fine (letter of CLEAN-13 says "exactly one flag"; the merge loses nothing) | CLEAN-12, CLEAN-13 |
| `investor_orig_time` | "Investor borrower = 1, otherwise = 0" | yes; changes in 14 ids, never on an event row | int64 0/1 | fine | CLEAN-14 |
| `balance_orig_time` | "Outstanding balance at origination time" | yes | float64; zero -> missing (270); varies in 15 ids | fine | CLEAN-10 |
| `FICO_orig_time` | "FICO score at origination time" (codebook's "in %" is wrong) | yes; changes in 381 ids (median jump 30 points), not event-enriched | int64, 400-840 | fine | LEAK-10 tested |
| `LTV_orig_time` | "Loan-to-value ratio at origination time, in %" | yes; changes in 35 ids | float64, 50.1-218.5 (1,252 rows >100: unusual, possible) | fine | CLEAN-11 (unusual, stays) |
| `Interest_Rate_orig_time` | "Interest rate at origination time, in %" | mostly; but it is not a fixed origination value: changes in 3,540 ids (4,827 rows; 1,196 from 0 to a value), and on 2,703 change rows the new value is the row's own-quarter `interest_rate_time` (which we lag). 3,999 of 24,733 test rows hold a value other than the loan's first. Not event-enriched (default 1.3% on those rows vs 2.4% base). Measured: freezing it (and FICO, LTV_orig, mat_time) at the previous observation changes LightGBM log loss by -0.0002/-0.0001/-0.0002 (60/59/58: 0.11973 -> 0.11955, 0.13218 -> 0.13205, 0.13598 -> 0.13581) | float64; zero -> missing (89,990, 14.5%; zeros are 97% whole-loan, payoff 6.9%/default 3.0% vs 4.3%/2.4%; missing-indicator AUC 0.504 per leak probe) | fine, with a note (sibling of the lagged rate, LEAK-2; no measurable leak) | LEAK-2, LEAK-6, LEAK-11 |
| `hpi_orig_time` | "House price index at origination time" | yes after publication: equals `hpi_time` of `orig_time` on 100% of 605,679 checkable rows; masked while `time - orig_time < 2` (16,290 rows) | float64 | fine | LEAK-7 |
| `status` (target) | `status_time`: "Default (1), payoff (2), and nondefault/nonpayoff (0) observation at observation time" | outcome within the quarter | category active/default/payoff. 501 loans leave before period 60 without an event; their last row stays `active`. On those last rows 7.7% have a zero balance and 26.6% a balance >5% below the previous one (ordinary active rows: 0.0% and 1.0%; even payoff rows 1.2%/2.8%); 93 are at maturity. The codebook says observations are censored when borrowers refinance. Test rows: period 58: 23 (3 zero balance, 9 down >5%; window has 145 payoffs), period 59: 75 (2, 5; 165 payoffs) | question: some `active` last rows are unrecorded payoffs | LEAK-25, USE-5 |

Dropped and correctly so: `id` (borrower id in file order, CLEAN-3; no label encoding), `default_time`/`payoff_time`
(encodings of the target, LEAK-10), the own-quarter `balance_time`, `LTV_time`, `interest_rate_time`, `hpi_time`,
`gdp_time`, `uer_time` (replaced by lags; decision tables 1 and 3).

**Problems, ranked (principles.md)**

1. **P4, LEAK-25 (Must, weak here): "no event" mixed with "not recorded" on the last row of early leavers.** Evidence:
   codebook "Observations may be censored when loans mature or borrowers refinance"; the 455 measurable last rows of
   the 501 early-leaving loans look like payoffs (zero balance 7.7%, balance down >5% 26.6%, against 0.0% / 1.0% on
   other active rows); 98 such rows in the test windows (58: 23, 59: 75), of which about 12-19 show the payoff
   signature, next to 145-165 recorded payoffs per window. Already in the earlier REVIEW.md issue 7 as censoring; new is the
   codebook quote and the balance signature, which says part of it is a wrong label, not only a missing row. Mildest
   remedy: drop the last row of loans that leave before period 60 without an event (label not recorded, like a
   missing target, CLEAN-15; 501 rows, 0.08%), or keep with a note quoting the codebook. Not a reason to retire
   (recording process is known and the share is small).
2. **P3/P4, USE-3 (question): rows the lender does not hold at the quarter's start.** 8,145 rows with
   `time == orig_time` (originated during the quarter; payoff 8.0%) and, more broadly, a loan's first panel row
   (50,002 rows, entering the pool during the quarter). 24 and 66 test rows. Remedy if the curator agrees: drop
   `time == orig_time` rows, or write in the use case that loans are also scored in the quarter they join the book.
   Otherwise a note.
3. **P4, LEAK-2 sibling (note, no leak measured): `Interest_Rate_orig_time` is updated within loans and on 2,703 rows
   copies the own-quarter rate the definition lags.** Lagging it (with FICO, LTV_orig, mat_time) changes LightGBM log
   loss by at most 0.0002 (better, not worse). Remedy: none needed; sharpen the "Kept as recorded: origination fields
   that change within a loan" bullet with the numbers (3,540 loans; new value equals the own-quarter rate on 2,703
   rows; lagged: -0.0001 to -0.0002 log loss), which also answers the checklist's open "when does the source update
   them".
4. **P7, CLEAN-10/CLEAN-11 (Should): the 37.5% rate is a placeholder.** 44 loans, all period 22, their first row,
   then normal rates; shipped as 41 rows of `interest_rate_time_lag_1 = 37.5` in period 23 (none in test). The
   definition's "interest rates above 25% (44 rows) kept as recorded" should read as a proxy value: mask
   `interest_rate_time == 37.5` (or > 25) before the lag. Cheap and safe.
5. **P7, CLEAN-11 (Should, keep with note): balance far above the original balance.** 38 rows with
   `balance_time_lag_1` >3x `balance_orig_time` (e.g. 570,000 on 60,495), producing all 37 LTVs >300%; 3 test rows.
   One of the two balances is wrong and the data cannot tell which: keep with a note (current bullet does), or mask
   `LTV_time_lag_1` there.
6. **P7, CLEAN-11 (minor):** 45 rows (4 ids) with `first_time < orig_time`; 57 non-first rows with a missing lag
   because the loan key restarts when `orig_time`/`balance_orig_time` change within an id. Note only.
7. **Procedure (writing.md):** notes vs data, already in the checklist: distance AUC 0.58 vs 0.525 measured; "zero-balance
   rows" should be "zero original-balance rows"; 44/38 source rows vs 41/37 shipped.
8. **P7, CLEAN-13 wording / CLEAN-14 (curator questions, no action needed):** `real_estate_type` merges flags of which at
   most one is set, with an inferred `other` (lossless); the four period columns could become quarter dates only via
   the Case-Shiller re-identification (the earlier REVIEW.md issue 8), so keeping period numbers is defensible.

No column found that should leave whatever it scores: every kept feature exists at the start of the quarter, apart
from the cohort question in item 2.

</details>

<details><summary>Split audit</summary>

**mortgage: split audit (review panel, phase A, 2026-10-20)**

Scope: the split of `datasets/_dev/tabarena-v0pt2/mortgage/dataset.py` (temporal on `time`, 3 one-quarter windows,
expanding train, no gap, horizon 1 step). Data loaded through `dataset_io` (container rebuilt from the definition, and
the definition's frame with the loan key kept in memory for the loan-level checks).

**Verdict**

**Right with notes.** Temporal, known entity, expanding train, no gap: this is the regime the use case implies, and it
is built correctly. The notes are weighing calls already open in the earlier REVIEW.md (window length, level effect) plus two
small facts to write down (censored `active` rows in test, a closed run-off cohort).

Judgment record:

```text
Verdict: right with notes.
Validity: USE-10 holds (known entity; the loan's history is legitimate); SPLIT-1/2/3 hold (temporal, one regime);
  SPLIT-9/10 hold (every train label known at the cutoff, no gap needed); SPLIT-11 holds (expanding, newest first);
  SPLIT-14 holds (3 windows, train 96.0-98.7%); SPLIT-19 holds (the book's period-60 backtest); SPLIT-29/30 no hit.
Notes: SPLIT-12/17 window length (a weighing call, the earlier REVIEW.md issue 3); LEAK-25 censored `active` rows in test
  window 59 (0.91%); SPLIT-20 history is a shrinking closed cohort with a pool added at period 52 (note only).
```

**Checks, with numbers**

**Regime (USE-10, SPLIT-1 to SPLIT-4, SPLIT-13)**

* Use case: a lender at a quarter's start scores the loans it holds. The entity is known; its history is legitimate,
  so temporal with loans recurring across the cut is correct (USE-10, SPLIT-13). Declared: temporal. Match.
* Test rows whose loan has earlier rows in train: 99.93% / 99.88% / 99.38% (periods 58 / 59 / 60); rows with no
  previous observation: 6 / 10 / 50.
* Record: `tags: Non-IID (Temporal)`, `required_split: Temporal (NON-IID)`. the earlier REVIEW.md's "record says Grouped" is
  stale; record and definition agree now.
* **Alternative 1, loan-grouped temporal (cold start)**: train on rows before the window minus every loan present in
  the window. LightGBM log loss 2.586 / 2.599 / 3.174 (periods 60 / 59 / 58) against 0.1197 / 0.1315 / 0.1357 shipped.
  The cold train side holds only loans that already exited (each ends in an event or censoring), so its class shares are
  event-heavy and the model is badly miscalibrated. This is not a usable alternative; it confirms that a grouped split
  answers a different, unreal question here (a lender never scores a book with no surviving loans). Default-only AUC is
  similar either way (0.58 / 0.70 / 0.55 cold against 0.56 / 0.67 / 0.60), so the per-loan ranking does not depend on
  recurrence.
* **Alternative 2, IID by row against grouped by loan** (3-fold, whole frame, same LightGBM): log loss 0.2607 both,
  default AUC 0.767 / 0.768. Recognising a loan gives nothing (no hidden-group shortcut; consistent with the
  hidden-group probe: no entity-like column, near copies 2.0%).

**Temporal mechanics**

* Time column: `time` is the observation quarter (period 1 = 2000 Q2, period 60 = 2015 Q1, dated by Case-Shiller and
  UNRATE in the panel's prep measurements); the label is the status during that quarter, the features are at its start
  (lagged loan state, macro lags t-1/t-2). One column, one meaning.
* Windows (verified on the split indices): repeat 0 tests period 60 (8,004 rows: 7,814 active, 147 payoff, 43 default),
  train = all of periods 1-59 (614,173 rows, 98.7%); repeat 1 period 59 (8,247; 165 payoff, 53 default), train 97.4%;
  repeat 2 period 58 (8,482; 145 payoff, 77 default), train 96.0%. Train equals exactly the rows with `time` below the
  window in every repeat. Newest first (SPLIT-11), at least 3 windows, train above 50% (SPLIT-14).
* Gap against label delay (SPLIT-9, SPLIT-10): the status of quarter t-1 is settled by the start of quarter t, and no
  row follows an event within a loan (0 rows). Every training label is known at the cutoff; no gap is needed. Residual
  doubt, not measurable: when the source's default flag is set relative to the missed payments (a 90-days-past-due
  default could be stamped late). The newest window's event shares match periods 56-59 (checklist), so there is no sign
  of late-arriving labels.
* Lag freshness: no test row has its previous observation more than one quarter back (0 in all three windows), so the
  `*_lag_1` features of test rows are one quarter old as stated. Over the whole panel 1,181 loans have gaps (1,246 rows
  right after a gap, event share 9.1% against 6.7%), all in train.
* Season (SPLIT-20): the windows are Q3, Q4, Q1 (no Q2). The quarter-of-year effect is small: deviation from a
  5-quarter rolling mean over periods 21-60, payoff +0.28 pp in Q3, -0.26 pp in Q1, default within +-0.12 pp. Not an
  atypical-season problem.
* Horizon (SPLIT-12): one quarter, the book's backtest period and a quarterly refit. Defensible.

**Training history (SPLIT-20, SPLIT-21)**

* Train goes back to period 1 (283 rows); the panel grows to 25,906 rows at period 30 and shrinks to 8,004 at period
  60. It is a closed cohort run off over time: test loans have median age 34-36 quarters and only 2.4-2.7% were
  originated within the last 8 quarters. A lender's real book would hold new loans too; the split cannot fix this, it is
  the source's sample (note, P3 fit rather than P4).
* At period 52 a pool of 1,728 seasoned loans enters (median origination period 24; rows jump 8,650 -> 10,116). It sits
  in the train side of every window; its event share declines from 4.9% (52) to 2.1% (60), in line with the rest.
* The history spans the 2007-2009 crisis (default shares up to about 3% per quarter in periods 40-44, 0.5-0.9% in the
  test quarters). Keeping all history follows the book's backtest (SPLIT-19). SPLIT-21 forbids trimming it on a
  comparison over three windows, so I make no recommendation to cut it.

**Window size and what the score measures**

* 43-77 defaults and 145-165 payoffs per window: every class scorable (TP-9 passes), well above SPLIT-17's 50 rows.
* The default-only AUC swings by window (0.56 / 0.67 / 0.60 here; 0.61 / 0.66 / 0.57 in the panel's full-train run),
  a sign that 43-77 defaults per window make a per-window comparison noisy. The previous quarter's class shares carry
  76-86% of LightGBM's gain over the all-history dummy (the earlier REVIEW.md issue 2), so per-window log loss mainly measures
  how a method extrapolates the quarter's level from `time`. That is an evaluation-value question (P6) and a target
  framing question (P3); the split itself is right.

**Problems, ranked (principles.md: rank, then strength, then effect)**

1. **P4, LEAK-25 / SPLIT-9 (Should, small).** Censored `active` labels inside test windows: 23 rows in period 58 (0.27%)
   and 75 in period 59 (0.91%) are the last row of a loan that leaves the panel without an event (prep measurements;
   the 75 leave together after 59, a pool exit). Their true status is unknown, yet they are scored as `active`.
   Mildest remedy: a filter that drops a loan's last row when it leaves before period 60 without an event (98 test rows,
   about 500 train rows), or keep with a note in `curation_comments`. Effect on the score is tiny; it is about a label
   that is not an observation.
2. **P4, SPLIT-12 / SPLIT-17 (Should; weighing call, the earlier REVIEW.md issue 3).** One-quarter windows match the book's
   backtest and a quarterly refit, but with 43-77 defaults each the per-window scores are noisy and dominated by the
   quarter's level. Alternative already measured by the earlier run: three four-quarter windows (periods 49-52, 53-56,
   57-60; 222-678 defaults, train still above 50%). Do not decide it from scores (SPLIT-21); decide from the refit
   cadence the use case implies. Mildest remedy: none required; if changed, a re-split to `window=4, unit="unique"`
   with a matching horizon.
3. **P3/P4 note, SPLIT-20 (Weigh).** The train side and the test are a closed, ageing cohort (2.4-2.7% of test loans
   originated within 8 quarters) with a seasoned pool added at period 52. Not a split defect; write it into the
   `splits_comment` or `task_summary.row` so the test is read as "a run-off book", not a live lender's full book.
4. **Writing (no rule broken).** the earlier REVIEW.md issue 5 ("record lists Grouped and Temporal") is out of date: the record
   has only `Non-IID (Temporal)`. Close the issue.

Not problems: no hidden groups (IID and loan-grouped random splits tie at 0.2607), no stale lags in test, no train
labels unknown at the cutoff, no season-shaped test window, loan recurrence across the cut is by design (USE-10).

</details>

<details><summary>Domain practitioner</summary>

**mortgage: practitioner review (panel phase A, 2026-10-20)**

Actor: a credit-risk modeller at a US mortgage holder (bank portfolio or RMBS investor/servicer) who, at the start of
each quarter, needs per-loan default and payoff probabilities for the next quarter, the building block of a CECL /
IFRS 9 lifetime-loss projection and of a prepayment cash-flow forecast.

**Fit: direct, with one input gap that I would fix (keep `direct` only if the gap is fixed; otherwise approximate)**

One row is one loan-quarter I score, the label falls inside the quarter, the test quarters come after training, and
the known-entity temporal design matches how I score the book I hold (USE-1, USE-3, USE-8, USE-10); but the shipped
frame withholds the loan's payment history, which I always have at the quarter's start.

**1. Inputs at the prediction point (USE-3, USE-6)**

Have, as shipped: origination terms (FICO, LTV, rate, balance, property type, investor), loan dates (origination,
panel entry, maturity), previous-quarter balance, rate and LTV, and macro figures as published. The lag fix on the
loan state and the per-series macro lags are right: in production I never see the quarter's own balance or GDP.

Would not have: nothing remaining that I can find. `time` is a period number; in deployment it is always one beyond
the training range, which only matters for how a model extrapolates (that is the level effect, gap 2).

Missing that I would always have (ranked):

1. **Payment history / delinquency status.** The servicer tape reports days past due every month; it is the
   strongest single predictor of default in the next quarter (a loan 60 days down is one missed payment from the
   90-day default). The source has no delinquency field, but a proxy is computable from data known at the quarter
   start: did the balance fail to fall between the loan's two previous observations. Measured
   (raw file, same dedup and loan key): the stalled-balance share is 45% on
   default rows against 27% on active rows over all periods; in periods 58-60, 53% against 14%, and this one binary
   flag alone gives default ROC AUC 0.70, above untuned LightGBM on all 17 shipped features (0.57-0.66 per window,
   the panel's full-train run). The shipped frame keeps only `balance_time_lag_1`, so no model can rebuild it.
   Interest-only loans also stall (27% of active rows), so the flag is a proxy, not a delinquency status.
2. **The market mortgage rate (refinance incentive).** Payoff is driven by the gap between the loan's rate and the
   current market rate; industry multinomial payoff/default models use it (the MathWorks example uses the 12-month
   change in the average mortgage rate). The source has no market rate. The periods are re-identified as calendar
   quarters, so a FRED series (MORTGAGE30US, lagged to publication) could be joined; this is an addition from outside
   the source and the curator's call.
3. Refreshed credit score: not in the source, cannot be added. Origination FICO only; a known, accepted limit.

**2. Target (USE-5)**

`status` (active / default / payoff) is what I act on: default drives provisions, payoff drives the cash-flow and
duration of the book; the competing-risks form is the book's own (R Companion ch. 11) and the industry standard. I
want calibrated probabilities for all three, so log loss is the right score. The horizon is one quarter: regulatory
PD is 12-month (Basel) or lifetime (CECL), but the quarterly conditional probability is exactly what a lifetime
transition model chains, so the horizon is fine. Default here is the source's own definition; neither the book page
nor the data page states it (likely 90+ days past due or foreclosure), a documentation gap, not a target problem.

**3. Rows and test data (USE-10, USE-11)**

One row = one loan in one quarter = one score I produce. The test quarters (2014 Q3 - 2015 Q1) are "next quarter"
for loans already on book (99.4-99.9% have history in train), which is what I face. Loans enter the panel a median
two quarters after origination (seasoned RMBS loans), so the actor is better described as the holder of the
portfolio than the originating lender; it does not change the task. 1,237 loan-quarters follow a gap of 2+
quarters, so for them `*_lag_1` is older than one quarter; negligible.

**4. Would I use it? (trust / distrust)**

Trust: real loan-level RMBS data, a lag design that removes the event-recording balance and the post-quarter macro
values, a backtest that mirrors the book's own. Distrust: (a) without payment history, the per-loan part of the
score is small (0.003-0.006 log loss over the previous quarter's shares; default AUC 0.57-0.66), so a benchmark win
mostly measures how a model carries the quarter's event level forward (the earlier REVIEW.md issue 2); a real model with
delinquency would rank loans far better, so the benchmark under-represents what matters to me; (b) 43-77 defaults
per test quarter make the default part of the score noisy.

**Gaps ranked by how much they change the task**

1. No payment-history input (gap 1 above): changes the task from "rank my loans" to "guess the quarter's level";
   fixable within the source by shipping `balance_time_lag_2` (or the lagged balance change) alongside lag 1.
2. Level effect of the 3-class log loss with one-quarter windows (the earlier REVIEW.md 2-3): partly a consequence of gap 1.
3. No market-rate / refinance incentive for payoff (fixable with an external, publication-lagged series).
4. Origination-only FICO, unstated default definition (not fixable; document).

**What a domain expert would change**

- Add the previous-but-one balance (or the t-2 -> t-1 balance change, or an "amortised last quarter" flag) as a
  feature; it is known at the quarter start and so is legal under USE-3 / USE-6. Re-run the task probes after.
- Consider a lagged market mortgage rate column and the loan's rate spread to it.
- Keep 3 classes and log loss; keep the known-entity temporal split; keep the lag fixes.
- State in `known` that payment history is unavailable (except through the added lag), and in `curation_comments`
  that default is the source's definition, not stated.
- Fit: `direct` is defensible after the payment-history fix; as shipped, I would call it approximate under USE-8
  (the inputs omit what the actor always has), though no listed USE-8 example covers a missing input exactly.

**Sources**

- `datasets/_dev/tabarena-v0pt2/mortgage/dataset.py`, `README.md`; `curation/records/mortgage.md`
- `.claude/skills/knowledge-curation/references/use_case.md`
- Deep Credit Risk data page (same RMBS panel, International Financial Research, 50,000 borrowers, 60 quarters):
  https://www.deepcreditrisk.com/data--code.html
- MathWorks, "Fit MNR model to payoff and default data" (industry 3-state default/payoff/survival per period with
  mortgage-rate change and unemployment as predictors):
  https://www.mathworks.com/help/risk/fit-mnr-model-to-payoff-and-default-data.html

</details>

<details><summary>Blind review</summary>

**Review: mortgage (status, multiclass, temporal split)**

**Verdict**
Include with changes. This is a real, well-known panel of US RMBS mortgage loans with a sensible next-period default/payoff/active target. It uses lagged time-varying covariates and a temporal split. The signal is modest but real. The changes are minor: document the grouping and the class imbalance, and fix a few data-quality points.

**What the task is**
The source is the Baesens/Roesch/Scheule "Credit Risk Analytics" mortgage panel (creditriskanalytics.net). The page calls it "a randomized selection of mortgage-loan-level data" from US RMBS portfolios: 50,000 borrowers over 60 deidentified periods. The data are real and not generated. One row is one borrower-period, and `status` is the outcome in that period: active, default or payoff. A lender, servicer or RMBS investor makes this prediction every period for PD/prepayment modelling, provisioning (IFRS 9/CECL) and stress testing. That is a real and central use.

**Evaluation honesty**
- The time-varying loan covariates are lagged by 1 period: `balance_time_lag_1`, `LTV_time_lag_1` and `interest_rate_time_lag_1`. The macro covariates `hpi`/`gdp` are lagged by 2 periods and `uer` by 1. This removes the obvious leak of the raw `balance_time`/`LTV_time`, which can reflect the event in the same period (a payoff takes the balance to 0, a default changes the LTV). Raw `default_time`, `payoff_time` and `id` are absent. Good.
- The remaining columns are origination attributes, `mat_time`, `first_time` and `time`, which are all known ex ante. I found no leak.
- The temporal split matches the use: fit on past periods, score future periods. Borrowers recur across train and test because there is no id column. In this sample the static origination attributes give about 49.3k distinct pseudo-borrowers. This is legitimate for panel forecasting because earlier rows are almost all "active", so memorisation cannot reveal the terminal event. Still, it should be documented as grouped data.
- I found 3 exact duplicate rows, which is negligible.

**Concerns (most to least serious)**
1. **Weak, imbalanced signal with strong temporal drift.** In the sample, active is 93.3%, payoff 4.2% and default 2.4%. Default rates move from about 1% (t≈20) to about 5% (t≈36) and down to about 0.5% (t≈56–60). Payoff rates fall from about 10% to about 2%. Results from my LightGBM on the 200k sample (300 trees):
   - Train t≤48, test t>48: one-vs-rest AUC is 0.58 for active, 0.66 for default and 0.66 for payoff. Log loss is 0.183 against a prior of 0.201.
   - Test window t in 41–46: macro AUC 0.61. Window t in 55–60: macro AUC 0.64.
   - Late test windows contain few events (about 430 defaults in t>48 in the 200k sample, or roughly 1.3k in the full data). Metric variance will be high.
   - Change: use log loss or macro metrics rather than accuracy, which is about 95% for a constant prediction. Make sure each test window holds enough events.
2. **The `time` variable is an absolute period index and has to be extrapolated.** Dropping time, age and remaining-term features lowered AUC by about 0.03 at every cutoff. So models gain from period effects that trees cannot extrapolate to future periods. This is fine as a test of temporal robustness, but consider adding loan age (`time - orig_time`) and remaining term (`mat_time - time`) as columns, or at least document the point.
3. **Missing values need documenting.**
   - `Interest_Rate_orig_time` is NaN in 14.5% of rows, `hpi_orig_time` in 2.6% (only for loans with orig_time ≥ 1) and `balance_orig_time` in 80 rows. These appear to be zeros or blanks in the source that were recoded to NaN, which is reasonable but should be stated.
   - The lag features are NaN in 8% of rows. These are the first observations, where `time == first_time` (16,046 rows), plus 18 rows with gaps in the panel.
4. **Small consistency issues.** 12 rows have orig_time > first_time, 20 active rows have time ≥ mat_time, `LTV_time_lag_1` reaches 787 and `balance_orig_time` reaches 8.0M. These are plausible quirks of the source and I would keep them. 622,177 rows against roughly 622.5k in the original file implies about 300 rows were dropped. The reason should be documented.
5. **The licence is unclear.** The page asks for a citation of Baesens et al. (2016) or Scheule et al. (2017) and links a separate Terms & Conditions page whose content I did not see. Confirm that redistribution is allowed.

**What I could not check**
- The full 622k table and the exact 3 test windows. I saw only the 200k sample, and task.md does not give the window boundaries.
- How the lags were constructed: whether they were taken per borrower over consecutive periods. Within this sample I could not verify this without an id.
- Which rows were dropped from the original, and the source Terms & Conditions.

</details>

<details><summary>Precedent check</summary>

**mortgage: precedent check (review panel, phase A, 2026-10-20)**

Checked: the definition's choices (`datasets/_dev/tabarena-v0pt2/mortgage/dataset.py`), the record
(`curation/records/mortgage.md`) and the questions of the earlier REVIEW.md, against the knowledge files' rules and Cases
tables, sibling definitions and the decision register. The register raises no flag on
mortgage. Its five mortgage decisions are two AI assessments (2026-10-07, 2026-10-20), the open issues and two Cases
rows (TP-2, EV-8, both 2026-10-07). The record has **no `CC` line**. The only curator decision touching it is the bulk
record fix of 2026-10-19 (Lennart, `datasets/_dev/tabarena-v0pt2/CHANGELOG.md`: tags that contradict the definition
removed; commit 58ee235). So there is no curator drift to check, and no rule has reached a third exception.

Measurements made for this check (raw mortgage.csv, sha256 matches; period-51
duplicates removed as the definition does) are marked **(new)**.

**Summary**

| # | Decision | Verdict | Rules | Closest precedents |
|---|---|---|---|---|
| 1 | Loan state (balance, rate, LTV) from the previous observation (issue 1) | consistent; the alternative would break a Must | LEAK-10, LEAK-7, LEAK-6 | garments `incentive_lag_1`; santander `has_*` (+0.003 dropped) |
| 2 | Macro columns lagged per series (issue 4) | consistent; the "all one quarter back" alternative breaks LEAK-10 for GDP and HPI | LEAK-10 | sberbank_housing_market_forecasting (decided the other way, with a reason) |
| 3 | 3-class target (issue 2) | open call, no departure; one precedent's reasoning does not transfer | USE-5, TP-2, EV-5 | african_credit_scoring_challenge (2026-10-07) |
| 4 | One-quarter windows (issue 3) | consistent | SPLIT-12, SPLIT-17, SPLIT-21, TP-9 | lending_club (quarterly), home_credit_default_stability_1m, aeolus |
| 5 | Temporal regime (issue 5) | consistent; **already settled 2026-10-19**, issue and field line are stale | SPLIT-3, USE-10 | Lennart 2026-10-19 bulk record fix |
| 6 | Loans leaving without an event keep their last row `active` (issue 7) | **not reasonable under the ranking as stated**: new evidence that some are unrecorded payoffs | LEAK-25 (Must) | ghanas_indigenous_intel (retired 2026-10-01) |
| 7 | Feature-duplicate rows kept as "separate loans" (issue 7) | **departs; the stated reason is contradicted by the data** | LEAK-18, LEAK-19 | audiology_diagnosis, wine_quality |
| 8 | Period 51: the payoff copy kept where two copies differ only in the status | departs from LEAK-20, with a stated reason that the data confirms | LEAK-20, PROV-13 | jm1 (all copies dropped) |
| 9 | Re-identified quarters in the notes (issue 8) | consistent | SEL-1, CLEAN-12 | alfa_battle_2_0_task_2 (restored ruble amounts, Lennart 2026-10-13) |
| 10 | `real_estate_type` with `other` where no flag is set | follows a precedent; departs from CLEAN-13's literal wording | CLEAN-12, CLEAN-13 (Must) | onlinenewspopularity (2026-10-14); caracas_cervical_cancer (2026-10-15) |
| 11 | Rates above 25% and LTVs above 300% kept as recorded | **departs without a stated reason** | CLEAN-11 | caracas, churn_telco_south_asia, heart_disease_va_long_beach, thyroid_discordant |
| 12 | Zero rates and balances become missing; `id` dropped | consistent | CLEAN-10, CLEAN-3, LEAK-33 | heart_disease_va_long_beach `chol == 0` |
| 13 | Keep despite `drift_baseline` | consistent | TP-1, TP-2, EV-3 | mortgage itself (2026-10-07), african_credit_scoring_challenge |
| 14 | Loans recurring across the cut | consistent | LEAK-34, USE-10, SPLIT-13 | ieee_fraud_detection `uid`, corporate_credit_rating |
| 15 | Licence (no redistribution) noted, not weighed | consistent | EV-4, SEL licence | lucas_topsoil (2026-09-23) |
| 16 | HMEQ distance note "ROC AUC 0.58" | procedure: the number no longer matches (0.525) | EV-8 | - |

**Per decision**

**1. Loan state lagged (REVIEW issue 1): consistent**

* Precedent: garments_worker_productivity `incentive`. It is a same-day value that depends on the day's outcome, so
  it is lagged within the entity (LEAK-10, LEAK-7; `leak_checks.md`, Mechanisms table). The definition cites it. The
  mechanism is the same: a row's own balance records the event (0.02% zero balance on active rows against 5.3% on
  payoff rows, periods 58-60).
* The alternative in issue 1 ("the raw columns as the book uses them") would keep a confirmed leak. That leak gains
  0.003-0.005 log loss out of time in every model family. LEAK-6 (Must): "a confirmed leak goes even when small"
  (santander `has_*`, +0.003 AUC). The book's practice is a SPLIT-19 / LEAK-3 Should and cannot outrank LEAK-10 (Must,
  P4).
* So issue 1 is not a free choice. It can be presented as settled by LEAK-10 and LEAK-6. Keeping the raw columns
  would be an amendment, not an exception.

**2. Macro lags per series (REVIEW issue 4): consistent; a sibling pair decided the other way**

* Under LEAK-10, a value not published at the prediction point is out.
* The per-series lags rest on identified series. `hpi_time` is Case-Shiller 10-city NSA of the quarter's last month
  (max difference 0.114), and `uer_time` is UNRATE of the quarter's first month (59 of 60 exact).
* The "all one quarter back" alternative leaves GDP and HPI one to two months before their release. The issue states
  this itself, so the alternative breaks a Must. Only "per series" is consistent.
* **Pair decided differently:** sberbank_housing_market_forecasting (accepted, shipped).
  * It joins `macro.csv` on the sale date. Monthly and quarterly statistics take effect on the first day of their
    period, and "the source does not say when each figure was published, so some may postdate the sale" (its
    `curation_comments` and `fit_reason`).
  * It is kept unlagged, with that note.
  * The fact that sets mortgage apart, written down: its series are identified and their release lags are public.
    sberbank's are not.
  * The mechanism is the same: a period's own statistic is joined to rows inside that period. It is the stricter case
    that would need a reason, not mortgage.
  * No `CC` covers sberbank's macro columns. It was an AI note the curator accepted with the dataset.

**Consistency check (AI, 2026-10-20):** mortgage lags each macro series to its release (LEAK-10), while
sberbank_housing_market_forecasting (accepted, macro values of the sale's own month or quarter, release dates unknown)
keeps them unlagged with a note. What sets sberbank apart?
(a) the release dates of sberbank's ~100 macro series are unknown, so no lag can be rebuilt, recorded as a
`Potential leak, kept on purpose:` note; (b) treat sberbank like mortgage (lag monthly and quarterly series by one
period); (c) reopen mortgage to match sberbank (not available: it would break LEAK-10); (d) amend LEAK-10 for
statistics whose release date is unknown.

**3. Target: 3 classes (REVIEW issue 2): an open call, no departure**

* USE-5 (Must) asks for the target the actor acts on. The competing-risks status is the R Companion's chapter-11 form,
  and default alone is the book's chapter 6/13 form. Both are source framings, so either is consistent with USE-5.
* Precedent to watch: african_credit_scoring_challenge (TP-1/TP-2/TP-3, kept 2026-10-07).
  * Its `drift_baseline` flag was dismissed because "the drift flag is about log loss (the default rate moves ...),
    which ROC AUC, the metric, ignores".
  * mortgage is scored by log loss (multiclass), so that reason **does not transfer**.
  * Here the level is 76-86% of LightGBM's gain. If the curator keeps the 3-class log-loss task, the reason has to be
    its own: the quarter's level is part of what a lender's PD model must get right (EV-5: log loss is a proper
    score). It cannot be "like african_credit".
* No rule forces either option. A separate `mortgage_default` folder (ROC AUC) would be a distinct task under the same
  source, which PROV-6/PROV-7 allow ("a shared source with distinct tasks is not a duplicate").

**4. Window length (REVIEW issue 3): consistent**

* One-quarter windows match a quarterly refit (SPLIT-12). Siblings take their window from the refit cadence too:
  * lending_club: three quarters, "refit every quarter";
  * home_credit_default_stability_1m: two months;
  * african_credit_scoring_challenge: at most 30 days.
* SPLIT-17 holds: 8.0-8.5k test rows per window. TP-9 holds: 43-77 defaults and 145-165 payoffs per window.
* Caution, SPLIT-21 (Must; aeolus, Lennart 2026-10-12): the windows are not decided from a comparison over a few test
  windows. Issue 3's table of LightGBM scores and level shares for one-year windows is that kind of comparison. A
  change to four-quarter windows should rest on the use case (a yearly refit, or a horizon the source gives), not on
  the steadier scores.

**5. Regime (REVIEW issue 5): consistent; already decided**

* The record's `Non-IID (Grouped)` tag and `Grouped (NON-IID)` split were removed on 2026-10-19 by Lennart, in the bulk
  fix "tags that contradict the definition removed" (`CHANGELOG.md`; commit 58ee235).
* The record now says `Non-IID (Temporal)` / `Temporal (NON-IID)`.
* the earlier REVIEW.md's line "Record fields that disagree with the definition: tag" and issue 5 are therefore stale and
  can be closed as settled. They need no new decision.

**6. Censored loans kept `active` (REVIEW issue 7, second bullet): not reasonable under the ranking as stated**

* Rule: LEAK-25 (Must) treats "no event" mixed with "not recorded" as a censoring bias. Retire unless the recording
  process can be recovered.
* Precedent: ghanas_indigenous_intel, retired on 2026-10-01 (Lennart, `No (Retired); Too Small, Data Quality Issue`).
  There, 22 of 43 farmers never recorded rain in the rainy season.
* The definition keeps the last row "as recorded". The reason in the earlier REVIEW.md (F4) is that the 75 loans leaving
  after period 59 are "a pool leaving the data rather than missed defaults", and the whole group is under 0.1% of rows.
* **(new) The data supports that reason for the period-59 pool only.** The last rows of the 501 loans that leave
  before period 60 without an event (455 have a previous row):

  | Rows | n | balance 0 | balance down > 5% |
  |---|---|---|---|
  | censored last rows, all | 455 | 7.69% (35 rows) | 26.6% |
  | of them, period-59 pool | 75 | 2.67% | 6.7% |
  | of them, period 58 (test window) | 23 | 13.0% | 39.1% |
  | active rows that are not such last rows | 533,608 | 0.0004% (2 rows) | 1.0% |
  | payoff rows, periods 58-60 | 451 | 5.32% | 14.9% |
  | active rows, periods 58-60 | 24,043 | 0.02% | 2.6% |

  Outside the period-59 pool, these last rows look like payoffs (a zero or sharply reduced balance more often than
  payoff rows), not like active quarters. So "no event" is mixed with "event not recorded" for a few hundred rows. That
  is LEAK-25's mechanism, at a scale far below ghana's.
* What sets the case apart from ghana is the scale and the remedy. The rows can be removed cheaply, which LEAK-25's
  "unless ... recovered" and the remedy ladder ("fix the definition: drop, filter") allow. Retirement is not
  indicated.
* Keeping the rows "as recorded" with no fix is a departure from a Must, and no higher-ranked Must supports it.

**Consistency check (AI, 2026-10-20):** your call on mortgage would keep the last `active` row of loans that leave the
panel without an event. This differs from ghanas_indigenous_intel (retired 2026-10-01, the same mechanism: "no event"
mixed with "not recorded", LEAK-25 Must). Outside the period-59 pool, 7.7% of those last rows have a zero balance (other
active rows: 2 of 533,608). What sets mortgage apart?
(a) the affected rows are few (455 of 622k; 23 in test window 58) and can be dropped: filter the last row of every loan
that leaves before period 60 without an event, or only those with a zero or sharply reduced balance, so LEAK-25 is
fixed in the definition rather than excepted; (b) treat mortgage like ghana (retire), which the scale does not
suggest; (c) reopen ghana to match a keep-with-note, which its scale (37% of rows) does not suggest; (d) amend LEAK-25
to allow a keep with a note below a stated share.

**7. Feature-duplicate rows kept (REVIEW issue 7, first bullet): departs; the stated reason is contradicted**

* The definition says the 58 duplicate rows (8 borrower-id pairs) are "mostly separate loans on the same terms".
* **(new)** On the raw file, ids 35309/35310 match in every column over all 15 of their quarters (periods 27-41):
  balance path, rates, FICO, LTV, macro and status. Ids 3018/3020 do the same over all 8 of their quarters (24-31).
  These two pairs produce 23 of the 29 duplicate groups.
  * Fifteen consecutive identical balances, alongside FICO and LTV, are not two loans on the same terms. They are one
    loan listed twice.
  * The third raw pair (23502/26281) is a single row and plausibly a coincidence.
* Rules: LEAK-18 (Should): "many degrees of freedom and an exact match: a collection artefact, drop it". LEAK-19
  (Should): exact copies with the same label are dropped.
* Precedents: audiology_diagnosis ("27 copies of the same findings and diagnosis on different patient ids", dropped)
  and wine_quality.
* The effect is negligible (all these quarters are in train), which is why the panel may still keep them. The fact
  given for keeping them does not hold for the two pairs, though.

**Consistency check (AI, 2026-10-20):** your call on mortgage keeps the duplicate rows of ids 35309/35310 and
3018/3020. This differs from audiology_diagnosis (copies of the same findings on different patient ids dropped, LEAK-19).
Here the two ids share every value over 15 and 8 quarters. What sets mortgage apart?
(a) the copies all fall in periods 24-41, in every training side and no test window, so they cannot leak across the
split and only reweight two loans, recorded as an exception to LEAK-18/19 with that fact; (b) treat mortgage like
audiology: drop the second id of each fully identical pair (23 rows) and correct the note; (c) reopen audiology to
keep its copies; (d) amend LEAK-19.

**8. Period-51 doubles: the payoff copy kept: departs from LEAK-20, with a reason the data confirms**

* LEAK-20 (Should): feature vectors with both labels are dropped (jm1).
* Here the 7 conflicting pairs are one loan-period record doubled by the release (PROV-13 damage), not two units with
  ambiguous labels.
* **(new)** All 7 loans (ids 36833, 36910, 37351, 37528, 37558, 37580, 37637) have their last row in period 51, so the
  loan leaves the panel there and the payoff copy is the consistent one. The definition states this ("the loan leaves
  the panel").
* A reasonable exception (repair from the data's own record, P5 over P7). The note could name LEAK-20 and the fact.

**9. Quarters re-identified (REVIEW issue 8): consistent**

* The mapping of periods to 2000 Q2-2015 Q1 comes from matching public macro series. It identifies calendar time,
  not a person, so SEL-1 is not touched.
* The precedent for undoing a source's masking of non-personal values is alfa_battle_2_0_task_2's restored ruble
  amounts (CC, Lennart, 2026-10-13).
* The shipped columns stay period numbers. Only the notes state the quarters.

**10. `real_estate_type` with `other`: follows a precedent; departs from CLEAN-13's wording**

* CLEAN-13 (Must, 2026-10-15): "A block is one-hot only when every row has exactly one flag set". Here at most one
  flag is set, and 19.54% of rows have none.
* Its case, caracas_cervical_cancer, is about flags set **together** (multi-label). mortgage's block is dummy coding
  with a dropped reference level: lossless, never two flags at once.
* The same reading was shipped for onlinenewspopularity on 2026-10-14 (`data_channel`, "`other` when no flag is set";
  its code raises if two flags are set). That was before CLEAN-13's wording.
* Two cases now rest on a reading the rule's text does not cover. Since a Must has no exceptions, the clean way out is
  an amendment of the wording ("exactly one, or at most one with a reference level `other`"), not an exception.

**Consistency check (AI, 2026-10-20):** mortgage and onlinenewspopularity merge a flag block with no row holding two
flags into one category with `other` for none. CLEAN-13 (Must) as written allows a merge only when exactly one flag
is set. What sets these two apart?
(a) the block is k-1 dummy coding (never two flags set), so the merge is lossless and the rule's reason (multi-label
answers) does not apply: amend CLEAN-13's wording to cover a reference level; (b) treat both like the rule's text
(keep the three flags as separate yes/no columns); (c) reopen caracas_cervical_cancer (not indicated: its flags do
co-occur); (d) leave the wording and record nothing (not available for a Must).

**11. Rates above 25% and LTVs above 300% kept: departs without a stated reason**

* CLEAN-11 (Should): impossible values become missing, and unusual ones stay.
* The definition lists them under "Kept as recorded": 44 source rows with a rate above 25%, up to 37.5%, and 38 with
  an LTV above 300%, up to 803.5% (41 and 37 in the shipped lagged columns).
* It gives no fact for "unusual rather than impossible". Every CLEAN-11 case on file made the doubtful value missing:
  * caracas_cervical_cancer;
  * churn_telco_south_asia;
  * heart_disease_va_long_beach;
  * thyroid_discordant;
  * sdss_17.
* The checklist (P7 row) already raises it for the panel. Low stakes: P7 and about 80 rows.

**Consistency check (AI, 2026-10-20):** your call on mortgage keeps US mortgage rates up to 37.5% and LTVs up to 803.5%
"as recorded". This differs from the CLEAN-11 cases (caracas, churn_telco_south_asia, heart_disease_va_long_beach,
thyroid_discordant), where implausible values became missing. What sets mortgage apart?
(a) LTVs above 300% are possible for underwater loans after 2008, since the source's own formula reproduces `LTV_time`
on 100% of rows, and rates above 25% may be penalty or default rates on distressed loans: kept as unusual, with that
fact in the note; (b) treat them like the precedents (rates above a stated cap, for example 25%, to missing); (c) not
applicable; (d) amend CLEAN-11.

**12. Zero proxies and `id`: consistent**

* Origination rate, original balance and current rate of 0 become missing: 89,990, 270 and 25 rows (CLEAN-10; like
  heart_disease_va_long_beach `chol == 0`).
* `id` is dropped (CLEAN-3; LEAK-33). The loan key is used only for the lag.
* Minor wording point: the "`LTV_time` is missing on exactly the zero-balance rows" note holds for a zero **original**
  balance (270 rows), not a zero current balance (324 rows) (checklist).

**13. `drift_baseline` kept: consistent**

* This follows mortgage's own Cases rows (TP-2 and EV-8, 2026-10-07, AI run).
* The numbers match today's re-run: full-train LightGBM 0.1192 / 0.1320 / 0.1363 against previous-quarter shares
  0.1251 / 0.1374 / 0.1391.
* african_credit_scoring_challenge was kept the same way.
* No curator decision exists yet on either, so there is no drift.

**14. Loans recurring across the cut: consistent**

LEAK-34 (Must; a known entity's history under a temporal split), USE-10 and SPLIT-13 apply. The precedents are
ieee_fraud_detection `uid` and corporate_credit_rating (USE-10: known entity).

**15. Licence: consistent**

The no-redistribution clause is noted, not weighed (EV-4; selection.md "Ethics, licence"). The precedent is
lucas_topsoil (licence rule, Lennart, 2026-09-23).

**16. HMEQ distance note: procedure**

The note says "ROC AUC 0.58 for default", but today's run gives 0.525. EV-8 asks for the
note to say which run the number comes from, or to use the current value. The conclusion (far from HMEQ's 0.92) is
unchanged.

**Not checked here**

* REVIEW issue 9 (probe and framework notes): no curation decision.
* The R Companion code behind SPLIT-19's citation (checklist: not readable).

</details>

<details><summary>Advocate</summary>

**mortgage: advocate, opening brief (panel phase B, 2026-10-20)**

Position: ship, after four small definition fixes and some rewording. Every validity problem the panel found has a fix
in the definition. Nothing found calls for retirement. Sources: the phase-A reports.

**1. A real task, real data, the source's own design (P2, P3; USE-1, USE-5, USE-8 Must)**

- Evidence: real loan-level US RMBS panel, "a randomized selection of mortgage-loan-level data" (data page), 50,000
  borrowers. The blind reviewer, who saw no notes, reached "Include with changes" and called the use "real and
  central" (IFRS 9/CECL provisioning). The practitioner says the target is "what I act on" (default drives provisions,
  payoff drives cash flow) and that log loss is the right score. The 3-class form is the R Companion's ch. 11 model.
  The split follows the book's own period-60 backtest.
- Generation artefacts are ruled out: label-free distance AUC 0.525 now (HMEQ, retired: 0.92).
- Answers: any argument that the task is not worth benchmarking. P3 outranks P6 and P7.

**2. The evaluation is honest, checked by tests that could have refuted it (P4; LEAK-10, LEAK-34, SPLIT-1/3/9/11/14/19)**

- The quarters are dated by matching against FRED. Only 1 of 9 alignments fits (HPI median diff 0.002; UER 59/60
  exact), which proves the per-series macro lags. `hpi_orig_time` equals `hpi_time` at origination on 100.00% of rows.
- Lagging the loan state removes a confirmed leak worth 0.003-0.005 log loss (precedents, LEAK-6; garments).
- The split audit's verdict is "right with notes". Train is exactly the rows before the window. Test lags are never
  stale (0 rows). No exact copies cross the split.
- No hidden groups: an IID split and a loan-grouped split tie at log loss 0.2607 (default AUC 0.767/0.768).
- The claim audit's `mat_time` worry is settled by measurement (EV-1). Freezing `mat_time`, FICO, LTV_orig and the
  origination rate at their previous values changes LightGBM log loss by -0.0001 to -0.0002, so the model does slightly
  better without the row's own values (column audit). No leak.

**3. LEAK-25 is real, and the fix is a filter, not retirement (LEAK-25 Must; remedy ladder)**

- I concede the problem. 501 loans leave before period 60 without an event, and their last row is labelled `active`.
  Outside the period-59 pool these rows look like payoffs: 7.7% have a zero balance, against 2 of 533,608 other
  active rows. 98 of these rows are in test.
- The mildest remedy that resolves it is to fix the definition: drop the last row of each loan that leaves before
  period 60 without an event (501 rows, 0.08%). LEAK-25 says "retire unless the recording process can be recovered".
  The process is recovered: the codebook says "censored when loans mature or borrowers refinance", so these rows are
  missing labels (CLEAN-15).
- ghanas_indigenous_intel differs in scale (about 37% of rows) and had no row-level fix. With the filter there is no
  Must left standing.

**4. The level effect is a value question, and the signal is real (P6; TP-1 Must, TP-2 Should; SPLIT-21 Must)**

- Full-train LightGBM beats the previous quarter's class shares in 3 of 3 windows: 0.1192/0.1320/0.1363 against
  0.1251/0.1374/0.1391. This repeats the TP-2 case on file for mortgage (2026-10-07).
- Every class can be scored in every window: 43-77 defaults and 145-165 payoffs (TP-9).
- I concede that the per-loan part is small, and that without `time` LightGBM loses in 2 of 3 windows. But predicting
  the quarter's level is part of a lender's PD job, and log loss is a proper score (EV-5). TP-2: "a small but real
  signal is no reason to retire".
- Do not lengthen the windows because the scores would be steadier. SPLIT-21 forbids choosing windows from scores. A
  quarterly refit is the use case (lending_club precedent).
- Remedy that raises the per-loan signal (USE-6 Must): add `balance_time_lag_2`, or the change from t-2 to t-1. It is
  known at the quarter's start and works as a proxy for delinquency. On its own, the flag gives default AUC 0.70,
  above LightGBM on all 17 shipped features (0.57-0.66) (practitioner). Re-run the probes afterwards. This also keeps
  fit `direct`. Without it, I concede that fit should read `approximate` (USE-8).

**5. The remaining data problems are P7 or below, and each fix is cheap (CLEAN-11, LEAK-18/19 Should; tension "real task against imperfect cleaning")**

- 37.5% interest rate: a placeholder on 44 loans' first rows, all in period 22, none in test. Mask it before the lag
  (CLEAN-11). This replaces "rates above 25% kept as recorded" without a stated reason.
- Fully identical id pairs 35309/35310 and 3018/3020 (23 rows, all in train). Drop the second id (LEAK-19,
  audiology). Fix the "separate loans" note.
- LTV above 300% (37 rows) comes from 38 balance rows that conflict with the original balance, and the data cannot say
  which value is wrong. Keep with a note (CLEAN-11 allows this).
- Loan key: 44 of the 59 ids with two keys are one mortgage with a revised origination field. This is under 0.01% of
  rows and none are in test. Correct the docstring. Keying loans on id + mat_time + FICO is optional.
- 24 test rows with `time == orig_time` are scored in the quarter the loan is originated. Add a note, or drop them if
  the curator wants a strict "held at the quarter's start".

**6. The remaining items are wording, not substance (writing.md, EV-8)**

- Stale numbers: the distance AUC is 0.58 in the note and 0.525 measured. LightGBM log loss is 0.1195 in the note and
  0.1192 measured.
- "Zero-balance" should read "zero original-balance".
- "Previous quarter" should read "previous observation" (true for 99.8% of rows).
- The assessment says "no known risk", which contradicts the concerns raised in the folder.
- The R Companion quote is unverified; mark it so.
- GDP vintage is unknown (weak, LEAK-10): keep the note.
- The licence restricts redistribution. It is noted and not weighed (EV-4; lucas_topsoil).
- CLEAN-13: `real_estate_type` is lossless dummy coding with a reference level, as in onlinenewspopularity. Amend the
  rule's wording. Do not split the flags.

**Judgment record**

```text
Verdict: ship after changes.
Validity: SEL holds; USE-1/5 hold; USE-8 direct if balance_time_lag_2 is added, else approximate; LEAK-10 fixed
  (loan-state and macro lags); LEAK-25 triggered, fixed by filtering the last row of non-event early leavers;
  SPLIT-1/3/9/11/14/19 hold; LEAK-34 by design (USE-10).
Value: TP-2, a small real signal over a drift constant (3/3 windows); keep, windows from the use case (SPLIT-21).
Quality: CLEAN-11 mask the 37.5% placeholder; LEAK-19 drop the 2 identical id pairs; CLEAN-13 wording amendment.
Weighed: source +, gap (multiclass) +, use case +, level effect -, licence noted.
For the curator: add balance_time_lag_2 (USE-6); 3-class vs separate mortgage_default folder (PROV-6/7) stays open.
```

**mortgage: advocate, rebuttal (panel phase B, 2026-10-20)**

The two briefs agree on the verdict (ship after changes) and on most of the remedies. Below are the critic's points
one by one. I raise no new points.

1. **Payment history withheld (USE-6, USE-8): concede.** This was already my point 4. Add `balance_time_lag_2`, or the
   change from t-2 to t-1, then re-run the probes. If it is not added, `fit` becomes `approximate` and `known` names
   the gap. One caution: the AUC of 0.70 comes from one flag built on the raw file. It needs to be confirmed on the
   rebuilt container before it goes into the notes (EV-8).

2. **Censored `active` last rows (LEAK-25): concede.** This was my point 3. Drop the last row of each loan that leaves
   before period 60 without an event (501 rows). With that filter, LEAK-25 holds and retirement is off the table.

3. **Rows with `time == orig_time` (USE-3): partly disputed.** I accept the problem. I dispute that dropping the rows
   is the mildest fix.
   - These rows are the quarter in which a loan joins the book. A holder of the portfolio does score loans it
     originates or buys during the quarter, from their origination terms (the practitioner calls the actor the
     portfolio holder).
   - Nothing on these rows is unknown when the loan joins the book: the lags are missing and the origination fields
     are known at origination.
   - Dropping them would remove real early payoffs (8.0%). It would also only half-solve the problem: the same logic
     covers all 50,002 first panel rows, not just these 8,145.
   - The rewording the critic offers ("also scored in the quarter it joins the book") resolves USE-3 without touching
     the data. It sits lower on the remedy ladder. Take the rewording.

4. **The level effect (TP-2, EV-5): concede the framing, dispute nothing.** Order of work: fix point 1, measure the
   per-loan share again, then write the level effect into `curation_comments` with its own reason, not with
   african_credit_scoring_challenge's reason. Remove "no known risk" from the record. Whether to add a
   `mortgage_default` folder is the curator's call.

5. **Copies and the loan key (LEAK-19, PROV-4): concede.** Drop the second id of 35309/35310 and of 3018/3020
   (23 rows). Correct the `LOAN_KEY` docstring and the duplicates bullet.

6. **The 37.5% placeholder (CLEAN-10/11): concede.** Mask it before the lag. Keep the LTVs above 300% with a note
   (we agree).

7. **Notes out of date (EV-8, writing): concede all the corrections.** One qualification on GDP:
   - A `Potential leak, kept on purpose:` note would make the fit `approximate` under USE-8.
   - The vintage claim is untested (EV-7). The macro lags themselves are proven, and only the revision state of one
     series is unknown.
   - I would word it as a caveat ("figures may carry later revisions; vintage unknown") and keep the fit `direct`.
     Whether a possible revision counts as a kept leak is a weighing call for the curator.

The verdicts match: ship after changes. Two open calls remain for the curator: whether to reword or drop the
`time == orig_time` rows, and how to word the GDP note.

</details>

<details><summary>Critic</summary>

**mortgage: critic's opening brief (panel phase B, 2026-10-20)**

**Position: do not ship as defined; ship after the changes below.** Nothing here calls for exclusion: the task is
real (USE-1), the regime is right (split audit), and the leak fixes already in the definition hold (claim audit). The
case is about a withheld input, mislabelled rows, and notes that do not match the data.

Dropped for lack of support: `mat_time` as a leak (column audit: lagging it with the other origination fields changes
LightGBM log loss by at most -0.0002, and in the better direction); the licence (EV-4: a note, never a reason).

**1. The frame withholds the payment history the lender always has, so `fit="direct"` is not earned (P3; USE-6, USE-8, Must)**

* Problem: the definition swaps the row's balance for `balance_time_lag_1` and keeps nothing older. Whether the balance
  stalled between t-2 and t-1 (a missed-payment proxy) is known at the quarter start, but no model can rebuild it from
  the shipped columns.
* Effect: per loan, the task becomes "guess the quarter's level" instead of "rank my loans". This is what makes
  point 4 so large.
* Evidence: the practitioner's script builds the flag from the t-2 and t-1 balances only. It is set on
  53% of default rows against 14% of active rows in periods 58-60. Alone it gives default ROC AUC 0.70. Untuned
  LightGBM on all 17 shipped features gives 0.57-0.66 per window. The practitioner
  calls the fit approximate as shipped.
* Rule: USE-6 (Must): a known input is legitimate, and leaving it out changes the task. USE-8 (Must): the fit must
  match what is shipped.
* Remedy (fix the definition): add `balance_time_lag_2`, or the t-2 to t-1 balance change, and re-run the task
  probes. Failing that, set `fit="approximate"` and name the gap in `known`.

**2. Some `active` labels are unrecorded exits (P4; LEAK-25, Must)**

* Problem: 501 loans leave before period 60 without an event, and their last row stays `active`. The codebook says
  observations "may be censored when ... borrowers refinance".
* Evidence (column audit, precedents table 6): on the 455 measurable last rows, 7.7% have a zero balance and 26.6% a
  balance more than 5% below the previous one. Other active rows: 2 of 533,608 rows with a zero balance, and 1.0%
  with a drop of more than 5%. 98 of these rows are scored in the test windows (23 in period 58, 75 in period 59).
  The period-58 rows carry the payoff signature most strongly (13% zero balance, 39% down more than 5%).
* Rule: LEAK-25 (Must): retire unless recoverable. Precedent: ghanas_indigenous_intel was retired, but here the scale
  is much smaller and the rows can be removed.
* Remedy (filter): drop the last row of every loan that leaves before period 60 without an event (501 rows, 0.08%).
  Keeping these rows as recorded departs from a Must, and no rule ranked above LEAK-25 supports that.

**3. Rows the lender does not hold at the quarter's start (P3; USE-3, Must; small)**

* Problem: the use case says "at the start of each quarter, a lender scores every mortgage it holds". Yet 8,145 rows
  have `time == orig_time`, so the loan was originated during the quarter it is scored for. Their payoff rate is 8.0%
  against a 4.3% base. 24 of these rows are in the test windows.
* Remedy (the mildest that works): either drop these rows, or reword `use_case` and `known` to say a loan is also
  scored in the quarter it joins the book.

**4. The 3-class log loss mostly scores the quarter's level (P6 with a P3 framing; TP-2 Should, EV-5)**

* Problem: method rankings depend on how a method extrapolates `time`, not on ranking loans.
* Evidence: the previous quarter's class shares carry 76-86% of LightGBM's gain. The per-loan part is 0.003-0.006
  log loss. Without `time`, LightGBM loses to the previous quarter's shares in 2 of 3 windows (claim audit:
  0.1298 vs 0.1251, 0.1406 vs 0.1391). Note that african_credit_scoring_challenge's reason for keeping its
  `drift_baseline` flag does not transfer here: it is scored by AUC, mortgage by log loss (precedents, item 3).
* Not a reason to retire (TP-2). Remedy: first fix point 1 and re-measure the per-loan share. Then state the level
  effect in `curation_comments` with its own reason (the level is part of what a PD model must get right). A
  `mortgage_default` folder scored by ROC AUC is the curator's call (PROV-6/7 allow it). The record's "no known risk"
  must go, because it contradicts the folder's own concerns.

**5. Copies kept for a reason the data refutes; the loan key is misdescribed (P4/P5; LEAK-18, LEAK-19 Should; PROV-4)**

* Evidence (precedents, item 7): ids 35309/35310 match in every column over 15 quarters, and ids 3018/3020 over 8.
  These two pairs make 23 of the 29 duplicate groups. That is one loan listed twice, not "separate loans on the same
  terms". Separately, 44 of the 59 ids with two loan keys are one mortgage with a revised `orig_time` or balance, and
  56 of the 59 first fragments end `active` while the loan goes on (claim audit). All of these rows are in train, so
  the effect on the score is negligible.
* Remedy: drop the second id of each identical pair (23 rows), following audiology_diagnosis. Correct the `LOAN_KEY`
  docstring and the duplicates bullet. Optionally, key loans on id, `mat_time` and FICO.

**6. The 37.5% rate is a placeholder, not a rate (P7; CLEAN-10, CLEAN-11 Should)**

* Evidence (column audit): 44 loans have 37.5% on their first row, all in period 22 and all with an origination rate
  of 0. From the next row on, their rate is 6.1-6.5%. This ships as 41 rows of `interest_rate_time_lag_1 = 37.5`.
  The "kept as recorded" bullet gives no fact for it (precedents, item 11).
* Remedy (cheap and safe): mask `interest_rate_time == 37.5` before the lag. Keep the LTVs above 300% with a note
  saying they come from the balance inconsistency.

**7. Notes that do not match the data (procedure; EV-8, writing)**

* The distance AUC is 0.525, not 0.58.
* `LTV_time` is missing on the zero **original**-balance rows (270), not on the 324 zero current-balance rows.
* Of the rows above the caps, 44/38 are in the source columns and 41/37 in the shipped columns.
* The LightGBM log loss for period 60 is 0.1192, not 0.1195.
* Loan state comes from the "previous observation", not the "previous quarter", for 1,250 rows.
* The R Companion quotes (ch. 11, ch. 13 `time < 60`) are unverified (PROV-16/17).
* The GDP figures are not the first release, and their vintage is unknown. Add a `Potential leak, kept on purpose:`
  note (LEAK-10, weak).
* Remedy: correct the text. Close REVIEW issue 5, which is stale.

```text
Verdict: ship after changes.
Validity: USE-6/USE-8 triggered (payment history withheld; add the t-2 balance or call the fit approximate);
  LEAK-25 triggered, fixable (drop the last rows of early leavers); USE-3 triggered, small (time == orig_time rows).
Value: TP-2, mostly a level signal; re-measure after the fix.
Quality: LEAK-19 copies (23 rows), CLEAN-10 placeholder 37.5, notes out of date.
For the curator: the 3-class target vs a mortgage_default companion (weighing call).
```

**mortgage: critic's rebuttal (panel phase B, 2026-10-20)**

The two briefs now agree on the verdict ("ship after changes") and on every fix to the definition. What is left is
three points of wording and one condition.

**Advocate 1: a real task, real data (concede)**

USE-1 and USE-5 hold, and I never argued for exclusion. One condition: "direct" holds only once the t-2 balance ships.
The advocate concedes this in their point 4.

**Advocate 2: honest evaluation (concede)**

The quarter dating, the macro lags, the `hpi_orig_time` masking, the split and the absence of hidden groups all held
under tests that could have refuted them. I had already dropped `mat_time` on the column audit's measurement.

**Advocate 3: LEAK-25, fixed by a filter (concede the remedy; dispute the reasoning)**

* The codebook line ("censored when loans mature or borrowers refinance") does not recover the recording process. It
  only says that unrecorded exits exist. It does not say which last rows were payoffs, and the balance signature
  cannot say either (only 7.7% have a zero balance).
* The filter works because it removes every row whose label is unknown. Under the remedy ladder that is fixing the
  definition, and it needs no claim that the process was recovered.
* Wording ask: the note should say "label not recorded, rows dropped (LEAK-25, CLEAN-15)", not "process recovered".

**Advocate 4: the level effect is a value question (concede, with one requirement)**

* TP-2 holds, and I asked for no retirement and no change to the windows (SPLIT-21).
* Requirement: `curation_comments` must give the level effect its own reason, namely that the quarter's level is part
  of a PD model's job (EV-5).
* That reason cannot borrow african_credit_scoring_challenge's: that dataset is scored by AUC, mortgage by log loss
  (precedents, item 3).
* Re-measure the per-loan share after `balance_time_lag_2` is added.

**Advocate 5: P7 fixes (concede, with one dispute)**

* I concede the 37.5% mask, dropping the second id of each identical pair, the LTV note and the loan-key docstring.
* Dispute: the `time == orig_time` rows are not a P7 matter. The use case says the lender scores the loans it holds
  "at the start of each quarter", and these 8,145 rows (24 in test) are loans it did not yet hold.
* That is USE-3 (Must, P3), which outranks the CLEAN tension the advocate cites. A note alone leaves `use_case` and
  `known` false.
* Remedy: either drop the rows, or reword `use_case` and `known` to say that loans are also scored in the quarter
  they join the book.

**Advocate 6: wording (concede)**

I agree with every item, including the CLEAN-13 amendment, which follows from the onlinenewspopularity precedent.

Final: ship after changes. The open calls for the curator are the `time == orig_time` remedy (drop the rows or reword
the use case) and the 3-class target against a separate `mortgage_default` folder.

</details>
