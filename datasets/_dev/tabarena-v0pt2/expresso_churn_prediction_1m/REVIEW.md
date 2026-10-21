# expresso_churn_prediction

**Outcome:** added as `expresso_churn_prediction_1m`. Churn of Expresso's mobile customers in Senegal after an
observation window of about three months, from Zindi's full Train.csv (2,154,048 customers, shipped as a stratified
1.5 million), split at random as in the competition. The review panel (2026-10-20) recommends shipping it after
changes to the text and one tag; the changes are made and the data is unchanged.
Verdict: ship (the panel's text changes and tag are made).
Validity: SEL-16 holds; USE-1 and USE-5 hold (approximate fit); USE-8 fit text extended (most churners already dormant,
no customer under 3 months' tenure); LEAK-10 triggered, fixed (REGION dropped; the reason is now the measured
mechanism, issue 1); label timing not shown to leak, written as inferred (EV-2, issue 6); LEAK-16 met and LEAK-18
applied (natural repeats); SPLIT-1 holds; SPLIT-8 triggered, fixed (`ForcedIIDFromTemporal` tag, cost stated as not
measurable); PROV-9 holds (2020), PROV-10 fixed (the citation is now the 2020 UmojaHack Ghana release).
Value: TP-4 `one_feature` kept (untuned LightGBM beats active days alone on 3 of 3 shipped folds; no tuned results).
Quality: CLEAN-5 not triggered for ARPU_SEGMENT (issue 5); wording fixes.
Weighed: real operator task +, size +, one undated snapshot -, positives mostly dormant SIMs -.
For the curator: issue 1 (REGION against kick), issue 6 (label timing as a stated risk), issue 5 (ARPU_SEGMENT).

**Main points:** Confirm the REGION drop although kick (Carvana's used-car data) kept a field with the same release
facts (issue 1); ship the unknown start of the 90-day churn period as a stated risk (issue 6); keep ARPU_SEGMENT
(issue 5).

**Record judgment:** valid with concerns: a real operator churn task with a measured leak removed; the release has no
dates, so the split cannot follow time, and when the churn period starts is inferred.

**Issues for Lennart:**

1. **REGION is dropped, while kick kept `WheelType` on the same release facts. Confirm the drop?**
   - Problem: REGION is the customer's region (14 named regions of Senegal), missing for 39.4% of customers. Churn is
     44.8% when it is missing and 1.8% when it is present. The "missing flag" below is just whether the value is
     missing. If the flag came from the observation window, it would track activity like every column that summarises
     the window (top-ups, calls, revenue) does. It does not: among customers active on all 62 days, the flag alone
     separates churners at ROC AUC 0.936, while no window column's missing flag passes 0.59; among churners REGION is
     missing for 95% at 1 active day and 94% at 62, while every activity column's missing share falls with activity. So
     the region was most likely filled after the window, from what happened in the churn period (LEAK-10, Must:
     missingness that encodes the outcome).
   - Effect: keeping it gives models information from after the prediction point. ROC AUC is 0.930 with it and 0.901
     without (LightGBM, 400,000 customers, 3 folds). Its whole value is the flag: window plus flag 0.9309, window plus
     REGION 0.9311.
   - Precedent: kick (Lennart, 2026-10-01) kept `WheelType`, whose missingness also tracks the label, under LEAK-38
     (Should, narrows LEAK-10: anonymised fields that may be post-outcome, in a company's own competition release,
     stay with a `Potential leak, kept on purpose:` note). The release facts are the same: a named field, the
     company's own competition, an undocumented recording process, and the same missingness in the host's test set
     (Expresso 39.39% against 39.43%; kick 4.5% against 4.3%). The fact that sets Expresso apart is the conditional
     test above, a measured mechanism that kick never had. LEAK-38's own word "anonymised" contradicts its kick case.
   - Implemented: dropped, with the per-column contrast in the README's decision tables.
   - Alternative: keep REGION with a `Potential leak, kept on purpose:` note, as for kick. That ships a signal measured
     to be post-outcome.
   - Recommendation: confirm the drop. Amending LEAK-38 and re-testing kick's `WheelType` are a separate item in the
     working copy's REVIEW.md.
   - Decision: confirm the drop, or keep REGION with the note.

6. **When do the 90 days of churn start? Ship with the timing as a stated risk?**
   - Problem: a churner is a customer with "no transaction for 90 days" (Zindi). Zindi does not say when the 90 days
     start. The definition reads them as starting at the end of the window. The other reading is 90 days from each
     customer's last activity. Then, for a customer with few active days, part of the churn period lies inside the
     window, and REGULARITY (active days; ROC AUC 0.890 alone) partly measures the label itself.
   - Effect: under the other reading, the low-activity customers (61% of churners were active on at most 3 of the last
     62 days) are easier to score than at a real prediction point.
   - Evidence for the definition's reading: churn falls smoothly with activity (70.7% at 1 active day, 0.4% at 62);
     612 churners were active on all 62 days; ROC AUC is 0.90, against 0.986 for iranian_churn, whose window ends at
     churn (the LEAK-10 case). Against it: Zindi's codebook (`VariableDefinitions.csv`) defines REGULARITY as activity
     "pendant 90 jours" while its maximum is 62, and the 612 rule out an overlap only for active customers. The claim
     audit holds the timing "as consistency, not proof"; the blind reviewer raised it independently. Expresso's
     definition of the start would settle it.
   - Implemented: kept; the notes and the fit statement now write the start as inferred and name the other reading
     (USE-8, EV-2). LEAK-10 (Must) is not triggered on evidence. No data fix exists.
   - Alternative: hold the dataset until Expresso's definition is found; no source we checked gives it, so the hold
     has no end date.
   - Precedent: churn_telco_south_asia (churn timing kept as a stated risk).
   - Recommendation: confirm.
   - Decision: confirm that it ships with the timing as a stated risk, or hold it.

5. **ARPU_SEGMENT is REVENUE / 3 rounded in every row. Keep it?**
   - Problem: the codebook defines ARPU_SEGMENT as the 90-day income divided by 3, and it equals round(REVENUE / 3) in
     all rows, so it adds no information.
   - Effect: none on the task or the score (0.899 either way).
   - Rule: CLEAN-5 (Should) drops constant and duplicate columns. A rounded rescaling is not an exact copy, and
     2_month_survival_rate_prediction kept its `dzclass`, a deterministic coarsening of `dzgroup`, as "CLEAN-5 not
     triggered". The column audit prefers to drop it; the advocate and the critic keep it.
   - Implemented: kept as released.
   - Alternative: drop it, with a CLEAN-5 amendment covering deterministic copies, which reopens `dzclass`.
   - Recommendation: keep it (consistent with `dzclass`).
   - Decision: keep, or drop with the amendment.

**Review panel:** ship after changes (mediator). Claim audit: no validity claim refuted; three statements were stronger
than the data and are reworded. Blind review: include with changes; its main concerns are that active days carry most of
the signal and the label timing (issue 6). Debate: agreed on the REGION drop and the forced-IID tag; settled by the
mediator: the split's cost written as not measurable, the duplicates under LEAK-18 with no exception line, and the year
(2020, the Ghana release); left to the curator: REGION against kick (issue 1), the framing of the label timing (issue
6), ARPU_SEGMENT (issue 5). The mediator's issues 1, 3 and 4 are issues 1, 6 and 5 here; its issue 2 (the tag on the
other churn snapshots) is in the working copy's REVIEW.md. Earlier issue 4 (extract order) is settled by the split
audit. The sasol sibling (still `suggestion: 'Yes'`) is open in its own record.

<details><summary>Mediator</summary>

Both sides end at "ship after changes, no data change". Four disputes were left, and each is settled below. One
disputed fact, the first publication, is settled by a check of the Zindi API run today.

**Recommendation**

```text
Verdict: ship after changes (text and one tag; no data change).
Validity: SEL-16 holds; USE-1, USE-5 hold (approximate fit), USE-8 fit text extended (dormant churners, no tenure
  under 3 months); LEAK-10 triggered, fixed (REGION dropped; the measured mechanism replaces the wrong kick
  distinction); label timing not shown to leak, written as inferred (EV-2); LEAK-16 met, LEAK-18 applied (natural
  repeats, no LEAK-19 exception); SPLIT-1 holds; SPLIT-8 triggered, fixed (tag added; cost stated as not measurable);
  PROV-9 holds (2020, UmojaHack Ghana, same Train.csv), PROV-10 fixed (cite that release).
Value: TP-4 one_feature, kept (LightGBM beats REGULARITY on 3 of 3 shipped folds, 0.9025/0.9029/0.9022 against
  0.8901/0.8902/0.8896; untuned only).
Quality: CLEAN-5 not triggered for ARPU_SEGMENT (dzclass precedent); wording fixes.
Weighed: real operator task +, size +, one undated snapshot -, positives mostly dormant SIMs -.
For the curator: issue 1, the LEAK-38 consistency call (kick); issue 2, the forced-IID tag on the churn siblings;
  issue 3, label timing as a stated risk (confirm); issue 4, ARPU_SEGMENT (optional).
```

**Changes to make now (no decision needed)**

1. **Tag and split note (SPLIT-8, Must).** `data_tags = ("ForcedIIDFromTemporal",)`. One sentence in the IID note:
   a deployed model trains on an earlier window, with a gap of at least the 90-day label delay and the customers'
   history. The release has neither dates nor earlier windows, so the cost of the missing time axis cannot be
   measured. A hold-out by extract order (thirds 0.9026, 100k blocks 0.9028, random 0.9028) measures a customer
   sort, not time. Recover the dates and earlier windows if a later release has them. Settled for the critic: the
   note says "not measurable", not "zero". The rule asks for the cost "where the data allows", and here it does not.
2. **REGION reason (LEAK-10, Must; writing).** In the notes, the decision `why` and REVIEW.md, replace "not an
   anonymised host field like kick's" with the measured fact. Among customers active on all 62 days, the missing
   flag alone separates churners at AUC 0.936, and no window column passes 0.59. Among churners, REGION's missing
   share stays flat (0.952 to 0.944) while every activity column falls. Window + missing flag scores 0.9309,
   window + REGION 0.9311. Add the per-column AUC contrast to the decision table. "92-95% at every number of active
   days" becomes "90-96%".
3. **Label timing as inferred (EV-2, USE-8; LEAK-1).** Cite `VariableDefinitions.csv` in `download_description`.
   REGULARITY is "nombre de fois que le client est actif pendant 90 jours" (max 62 in the data), so the 62-day
   reading is inference. In the notes and `fit_reason`, write the label start as inferred and name the other reading
   (90 days from each customer's last activity). The 612 always-active churners rule out an overlap only for active
   customers. Settled for the critic on framing: the notes must not say "not a leak". The probes show no leak reading
   (AUC 0.90, churn falls smoothly from 70.7% to 0.4%; the iranian_churn signature is 0.986), so LEAK-10 is not
   triggered on evidence, and the uncertainty is written down. Precedent: churn_telco_south_asia (churn timing kept as
   a stated risk).
4. **Fit text (USE-8, Must).** In `fit_reason`: 80.9% of churners had no revenue in the window and hold 2.0% of its
   revenue, so the task mostly ranks SIMs that are already dormant. In `row`: almost all long-tenure customers (94.9%
   over 24 months, none under 3 months). The advocate left the second clause unanswered, and the practitioner and
   the column audit support it.
5. **Year and citation (PROV-9, PROV-10, Must).** Checked today in the Zindi API: "UmojaHack Ghana: Expresso Churn
   Prediction Challenge" (hackathon, 2020-06-27) lists Train.csv at 259,026,777 bytes. The 2021 competition lists the
   same size, and so does our file (sha256 matched). All five files have identical sizes. So the first publication is
   the 2020 Ghana hackathon, and `year = "2020"` stands. Point the BibTeX (year 2020) and `source_url` at
   `https://zindi.africa/competitions/umojahack-ghana-expresso-churn-prediction-challenge`, name the 2021 competition
   as the re-run, and drop "Senegal": no Senegal page resolves in the API. Add the Ghana page to the record's
   source links.
6. **Duplicates (LEAK-18, Should).** Cite LEAK-18 in the note: few effective features, distinct customers, natural
   repeats. Do not write an `Exception to LEAK-19`. Settled for the critic: LEAK-18 and LEAK-19 are both Should in
   the same part, LEAK-18 comes first and covers this case, and LEAK-19 does not narrow it. So nothing departs, and an
   exception line would wrongly count toward the amendment trigger. In the warning and the decision `why`, write
   "mostly (75.3%) described only by a tenure band and their active days" (167,726 copies carry activity values).
7. **Wording (writing, EV-8).**
   - The `ACTIVITY` docstring and note: "missing when the extract has no record; 0 is a record of none". Zeros and
     NaN coexist in six columns (ON_NET churn NaN 42.3%, 0 12.6%, >0 4.6%). Keep the values.
   - FREQUENCE: "number of times the client made revenue" (codebook), not "days with revenue".

**Issues for the curator (ranked)**

1. **P4, LEAK-10 (Must) against LEAK-38 (Should, narrows LEAK-10): REGION dropped, while kick's `WheelType` was
   kept.**
   - Effect: dropping REGION costs AUC 0.930 to 0.901.
   - Common to both sides: a named field in the company's own competition release, an undocumented recording
     process, the same missingness in the host's Test.csv (39.39% against 39.43%; kick 4.5% against 4.3%).
   - Best case for dropping: the conditional test above. The mechanism is measured, which kick never had, and REGION
     is outside LEAK-38's wording ("anonymised").
   - Best case for keeping: kick was kept on the same release facts, and LEAK-38's reason ("removing an unverified
     signal from host-designed data is arbitrary").
   - By rank, the drop wins: LEAK-38 narrows LEAK-10 only within its scope (anonymised, "may be" post-outcome), and
     REGION is neither. But kick contradicts LEAK-38's own wording, so that precedent is flagged.
   - Decision: (a) confirm the drop and amend LEAK-38's scope to fields whose timing cannot be tested;
     (b) keep REGION with a `Potential leak, kept on purpose:` note; (c) also reopen kick for the same conditional
     test; (d) amend LEAK-38's wording only. Recommended: (a), with (c) as a follow-up.
2. **P4, SPLIT-8 (Must), consistency across siblings.**
   - This dataset gets the tag now (change 1), following account_debt_south_africa (Lennart, 2026-10-12).
   - churn_telco_south_asia, mobile_churn, bank_customer_churn and tour_travels_churn have no `data_tags`.
   - Decision: tag all one-snapshot churn sets, or record why a churn snapshot is not "temporal in nature".
3. **P3/P4, label timing (LEAK-10 not triggered on evidence; USE-8).**
   - Change 3 writes the timing as an open risk. No data fix exists.
   - Critic's best evidence: the codebook says "90 days", and the claim audit holds the timing "as consistency, not
     proof".
   - Advocate's best evidence: smooth churn by activity, the 612 always-active churners, AUC 0.90 against 0.986 for
     iranian_churn.
   - What would settle it: Expresso's definition of when the 90 days start.
   - Decision: confirm that it ships as a stated risk (like churn_telco_south_asia).
4. **P7, CLEAN-5 (Should), optional: ARPU_SEGMENT = round(REVENUE/3) in 100% of rows.**
   - The column audit prefers to drop it, and dropping costs nothing (0.899 either way).
   - Both briefs keep it: not an exact copy, and the 2_month_survival `dzclass` precedent says "CLEAN-5 not
     triggered".
   - Decision: keep it (consistent, recommended), or drop it with a CLEAN-5 amendment covering deterministic copies,
     which reopens `dzclass`.

Not taken up:
- The blind review's "subsample to 100-200k": no rule asks for it, and the 1.5M budget is the v2 protocol.
- "Weight it low": TP-4 is not met, since the methods beat the single feature on every fold.

**Agreed facts**

- 2,154,048 customers, unique ids, 403,986 churners (18.75%). Churn = no transaction for 90 days (Zindi).
- Shipped: 1.5M stratified, 3 folds of 1M/500k, IID.
- user_id decodes as SHA-1 of the extract row. Zindi's Test.csv is a uniform 15% (84.8-85.2% of every 100k block in
  Train). The extract order is a customer/tenure sort, not time.
- REGION: 39.4% missing. Churn is 44.8% when missing and 1.8% when present. The missing flag alone gives AUC 0.936 at
  62 active days; window columns stay at or below 0.59. The values add nothing (0.913 against 0.912). The profile is
  the same in Test.csv.
- REGULARITY alone gives AUC 0.890, LightGBM 0.900 (probe), and 0.857 without REGULARITY. Shipped folds:
  0.9025/0.9029/0.9022 against 0.8901/0.8902/0.8896. No tuned results exist.
- 678,270 exact copies (31.5%). 75.3% of them have no activity value, and they hold 317,548 churners; dedup leaves
  5.9% churn. Copied test rows score lower (0.752 against 0.869). 1-NN agreement 0.653 is below chance (0.695). No
  hidden-group hit.
- 80.9% of churners had no revenue in the window. 94.9% of customers have tenure over 24 months; no band is under 3
  months.
- ARPU_SEGMENT = round(REVENUE/3) in all rows. MRG is "NO" in all rows.
- First release: UmojaHack Ghana, 2020-06-27, with the same Train.csv size as the 2021 competition (checked today).
- Zindi's rules forbid redistribution. This is a note only (EV-4).

**Consistency with precedent**

- REGION against kick (LEAK-38): departs. The distinguishing fact is the measured conditional test and that REGION
  falls outside LEAK-38's wording. kick itself contradicts that wording, so it is flagged and goes to the curator
  (issue 1).
- Duplicates: follows sepsis_survival and cdc_diabetes (LEAK-18). Set apart from jm1 by distinct customers, a gap of
  -0.000 against 0.016, and dedup changing the target.
- one_feature: follows sepsis_survival, california_house_prices_2020 and aps_failure, and this dataset's own TP-4 case
  row. Unlike fitness_club, the methods win on every fold and the data is real. Weaker test: untuned only.
- Split: follows account_debt_south_africa (the tag) and Lennart's CC (IID as in the competition). The siblings are
  inconsistent (issue 2).
- Label timing: follows churn_telco_south_asia (stated risk).
- ARPU_SEGMENT: follows 2_month_survival `dzclass`.
- Year: follows PROV-9. The REVIEW_before "same as pkdd" framing does not fit, because both candidate years are
  publication years.
- Siblings: `curation/records/sasol_customer_retention_recruitment_competition.md` still shows `suggestion: 'Yes'`,
  while the AI assessments say No/Duplicate (PROV-6, PROV-7). Settle it with this dataset.

</details>

<details><summary>Claim audit</summary>

**Verdict in one line**

No validity claim is refuted. The REGION drop survives the strongest test I could design (no window column shows its
signature; all of REGION's value is its missing flag). What fails is wording: three statements are stronger than the
data (REGION "92-95% at every number of active days", the copies "described only by tenure and active days",
REGULARITY "the last 62 days of the window"), and the duplicate keep is a departure from LEAK-19 (Should) without a
named exception.

**Table**

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 1, 4, 23 | churn = no transaction for 90 days; 403,986 (18.75%) churn | D task_summary, notes | count CHURN; Zindi page | holds | 403,986 / 2,154,048 = 0.18755; Zindi: "becoming inactive and not making any transactions for 90 days" | USE-5, EV-2 |
| 1, 3 | customers in Senegal | D task_summary | REGION values | holds | all 14 REGION values are Senegalese regions (DAKAR ... KEDOUGOU) | USE-1 |
| 3, 21 | every customer active in the window | D row, notes | min REGULARITY | holds | REGULARITY 1 to 62, no missing | USE-3 |
| 2, 19 | window of about three months | D use_case, notes | FREQUENCE max; ARPU/REVENUE | holds (inferred) | FREQUENCE max 91; ARPU = round(REVENUE/3) in 100% of rows; Zindi definition "income over 90 days / 3" (discussion) | EV-2 |
| 38 | REGULARITY counts active days in the last 62 days of the window | D notes | look for a source | untested, stated as fact | Zindi's variable definition (as quoted in its discussion 8742) reads "active for 90 days"; a participant's question why the max is 62 is unanswered. The 62-day reading is inference | EV-2, EV-7, writing |
| 22 | 612 churners active on all 62 days | D notes | count | holds | 612 of 166,477 customers at REGULARITY 62 | |
| 21 | label window follows observation window | D notes | consistency: churners active every day | holds as consistency, not proof | 612 churners at 62/62 days; churn 0.4% at 62 vs 70.7% at 1 day; cannot exclude a REGULARITY that counts non-transaction events | LEAK-22 to LEAK-26, EV-6 |
| 24 | user_id = SHA-1 of the extract's row number | D notes | sha1(str(i)) for i < 2.6M | holds | 2,154,048 of 2,154,048 decoded; indices 2 to 2,534,174 (Train + Test = the "2.5 million" clients of the page) | PROV-1 |
| 25 | 3rd place used the decoded order (discussion 9379) | D notes | fetch discussion | untested | page renders only "Zindi" without login | EV-7 |
| 26 | MRG "NO" in every row | D notes | value_counts | holds | {'NO': 2,154,048} | CLEAN |
| 27, 47, 53 | REGION missing for 92-95% of churners at every number of active days | D notes, decision, R | per exact REGULARITY value | refuted in the letter (minor) | at exact values 89.5% (REGULARITY 50, n=267) to 95.7% (52, n=255); 92-95% holds only for the bins of the decision table | writing, EV-8 |
| 27 | stayers 67% at 1 day to 7% at 62 | D notes | same | holds | 0.673 and 0.072 | |
| 28, 47, 59 | window columns' missingness falls with activity in both groups; REGION's does not | D notes, decision | missing share at REGULARITY 1 vs 62, churners/stayers, for all 13 ACTIVITY columns and REGION | holds (strongest test) | MONTANT 0.927->0.129 / 0.876->0.014; every activity column falls in both groups; REGION alone stays flat in churners (0.952 -> 0.944) while falling in stayers (0.673 -> 0.072). Tenure bands: churners 0.86-0.97, stayers 0.27-0.33 | LEAK-1, LEAK-10 to LEAK-12 |
| 29, 61 | dropping REGION lowers ROC AUC 0.930 -> 0.901 (LightGBM, 400k, 3-fold) | D notes | rerun, seed 0 | holds | 0.9311 -> 0.9026; window + REGION-missing flag alone 0.9309: REGION's whole value is its missing flag, i.e. the outcome-shaped part | LEAK-10 |
| 30, 31, 52 | IID as in the competition; Zindi's test is a uniform random 15% | D notes, R | decoded indices: share of each 100k block that is in Train | holds | share 0.8476-0.8519 per block (overall 0.8500; binomial SD 0.0011) | SPLIT-1 |
| 62 | churn varies along the decoded order 13-23% per 100k | REVIEW_before | same | holds | 0.131-0.226; REGION-missing 0.366-0.428 per block. Order dropped; test random in it, so harmless for the IID split | SPLIT |
| 6, 9, 43 | 1.5M stratified sub-sample, 3 folds, 1M / 500k | D | split plan | holds | 3 splits, 1,000,000 / 500,000, test union 1,500,000 unique, churn 0.18755 in every test fold | SPLIT |
| 32, 34, 35, 46 | 678,270 copies (31.5%), 75.3% without activity, holding 317,548 churners; dedup -> 5.9% | D notes, warning | recompute | holds | 678,270 (0.3149), 0.7527, 317,548, dedup churn 0.0586 | LEAK-16, LEAK-18 |
| 46, 48 | the copies are "customers described only by a tenure band and their active days" / "no or little activity" | D warning, decision | copies with any activity value | refuted in the letter (minor) | 167,726 copies (24.7%) carry activity values; the sentence then gives 75.3%, so the claim contradicts its own number | writing |
| implicit | no copy across the split that leaks | - | exact feature copies of test rows in train, shipped folds | holds as decided | 32.1-32.2% of test rows have an exact train copy (NaN-equal hashing; probe says 29.0% with its own key); 1-NN agreement in the closest tenth 0.653 < chance 0.695 (probe): copies are natural profiles, not reposts. Keeping exact same-label copies departs from LEAK-19 (Should) with no `Exception to LEAK-19` line | LEAK-18, LEAK-19 |
| 36 | TENURE 8 bands, TOP_PACK 140 packs | D notes | nunique | holds (full file) | 8 and 140 in the full file; 132 TOP_PACK values in the shipped 1.5M (hidden-group probe) | CLEAN |
| 39 | ARPU_SEGMENT = round(REVENUE/3) in every row | D notes | compare | holds | 100% of non-null rows, max deviation 0.333; null pattern identical | CLEAN |
| 40, 41 | one_feature; LightGBM 0.9023-0.9031 vs REGULARITY 0.8896-0.8902 on shipped folds | D notes | default LGBMClassifier on the three shipped folds | holds | LightGBM 0.9025 / 0.9029 / 0.9022; REGULARITY 0.8901 / 0.8902 / 0.8896. The checklist's "stale" concern is refuted: the numbers reproduce with an untuned default LightGBM; the probe's 0.899-0.902 is another configuration. Flag stands: skill 0.805 vs 0.780 | TP-4, EV-8 |
| 14 | sha256 and byte size of Train.csv | D download | sha256sum, stat | holds | matches | PROV |
| 13, 15 | Zindi API byte sizes; second Kaggle upload same sha | D download | not re-downloaded | untested | needs Kaggle/Zindi credentials | EV-7 |
| 17, 10 | competition 27 Aug-28 Nov 2021; first released for UmojaHack Senegal and Ghana 27 June 2020; year 2020 | D bibtex, year | Zindi page, search | holds for Ghana, untested for Senegal | page: 27 Aug 21 to 28 Nov 21; search: "UmojaHack Ghana Expresso Churn Prediction Challenge", 27 June 2020; no Senegal UmojaHack page found | PROV-10 |
| 11, 42 | licence "Zindi Competition Rules"; rules forbid redistribution incl. Kaggle/GitHub | D | Zindi rules page | holds | "You may not ... redistribute ... including uploading the data to any public site such as Kaggle or GitHub"; "sole property of Zindi and the competition host". A one-line note, not a verdict | EV-4, SEL |
| 8 | fit approximate: one undated snapshot, deployment trains on an earlier window, label timing inferred | D fit_reason | - | holds | nothing in the file dates rows; decoded order is not time | USE-8, USE-9 |
| 54, 60 | Azubian/DSN cuts are subsets; stayer-fit model predicts 11% missing for the 612 | R, REVIEW_before | - | untested | files not local; not rerun (the per-column signature test above is stronger evidence for the same point) | EV-7 |
| implicit | every remaining feature known at the prediction point | - | missingness signature per column (above) | holds as far as the data can test | no remaining column shows an outcome-shaped missingness; TENURE's timing cannot be tested | LEAK-1 |
| implicit | target is the real-world target | - | - | untested | whether every customer's 90 days were complete at extraction is not in the data | USE-5, LEAK-22 |

**Refuted and untested, ranked (principles.md: validity first, Must first)**

1. **P4, LEAK-19 (Should), procedure: duplicate keep without a named exception.** Substance holds (LEAK-18: natural
   profiles; dedup changes the task to 5.9% churn; 1-NN agreement below chance), but a departure from a Should needs an
   `Exception to LEAK-19` line naming the fact and the principle (P3). Changes: nothing in the data. Mildest remedy: add
   the exception line to the notes and record.
2. **P4 / writing, claim 38: REGULARITY "in the last 62 days of the window" is inference stated as fact** (Zindi's own
   definition says 90 days; unanswered on its forum). It carries the "label follows the window" argument (claim 21).
   Mildest remedy: write "REGULARITY ranges 1 to 62 (Zindi: active days over 90 days; the 62 maximum suggests the last
   62 days)".
3. **Writing, claims 27/47/53: "92% to 95% at every number of active days"** is 89.5%-95.7% at single values; 92-95% only
   in bins. Conclusion unchanged. Remedy: "90-96% at every number of active days".
4. **Writing, claims 46/48: copies "described only by a tenure band and their active days"** contradicts the 24.7% of
   copies (167,726) with activity values. Remedy: "mostly (75.3%) described only by ...".
5. **Untested, P5:** discussion 9379 (login), Zindi API byte sizes and the second upload's sha256 (credentials),
   UmojaHack Senegal release (only Ghana found), Azubian/DSN subsets. None changes a verdict.
6. **Untested, P3/P4:** completeness of every customer's 90-day label window at extraction; timing of TENURE. Already
   the "approximate" fit's stated gap.

Refuted for the checklist (not the definition): the `one_feature` note's per-fold numbers are not stale; they reproduce
within 0.0002 with a default LightGBM on the shipped folds.

Sources: https://zindi.world/competitions/expresso-churn-prediction (dates, churn definition, rules),
https://zindi.africa/competitions/expresso-churn-prediction/discussions/8742 (variable definitions as quoted, via
search), https://zindi.africa/hackathons/umojahack-ghana-expresso-churn-prediction-challenge (27 June 2020, via search).

</details>

<details><summary>Column audit</summary>

Inputs: the definition's cleaned frame (1,500,000 x 16) and the raw Train.csv (2,154,048 rows) for the dropped
columns and full-file rates. Codebook: Zindi's `VariableDefinitions.csv` (listed on the Zindi data page, 1.4 KB).
The definition never cites this file.

Prediction point (first bullet): end of an observation window of about three months; churn = no transaction for 90 days
after it. Zindi gives no dates.

**Column table**

| Column | Meaning (codebook, FR/EN) | Known at prediction? | Dtype and cleaning | Verdict | Rule |
|---|---|---|---|---|---|
| user_id (dropped) | no definition; SHA-1 of the extract's row number (record) | yes, but carries the extract order (churn 13-23% per 100k block; 3rd-place exploit) | dropped | fine (drop correct) | CLEAN-3, CLEAN-20 |
| REGION (dropped) | "la localité de chaque client" / location of each client | **no**: missingness follows the outcome, not the window | dropped | fine: leak correctly removed (strong) | LEAK-10 (attribute looked up after the outcome / missingness encoding the outcome) |
| MRG (dropped) | "un client qui fait du vas" = uses value-added services (the English "a client who is going" is a mistranslation) | yes | "NO" in all 2,154,048 rows; dropped | fine | CLEAN-5 |
| TENURE | "la durée dans le réseau" / duration in the network, 8 bands D (3-6 m) to K (>24 m) | probably; reference date unknown | category, 8 levels, 94.8% K; no bands A-C (< 3 months) | fine; question (see issue 5) | CLEAN-14 |
| MONTANT | top-up amount (window) | yes | float, 35.1% NaN (co-missing 100% with FREQUENCE_RECH), min 10, no zeros, no negatives | fine | CLEAN-10, CLEAN-14 |
| FREQUENCE_RECH | number of top-ups | yes | float count, max 133, same NaN as MONTANT | fine | CLEAN-14 |
| REVENUE | "revenu mensuel" / monthly income; but ARPU_SEGMENT = REVENUE/3 = "income over 90 days / 3", so REVENUE is the window total | yes | float, 33.7% NaN (co-missing with ARPU, FREQUENCE), min 1; MONTANT > REVENUE in 36% of rows (as released) | fine | CLEAN-14 |
| ARPU_SEGMENT | "revenu sur 90 jours / 3" | yes | float; equals round(REVENUE/3) in 100% of rows; 0 only where REVENUE = 1 | cleaning problem (minor): a deterministic, lossy copy of REVENUE | CLEAN-5 (Should) |
| FREQUENCE | "nombre de fois que le client a fait un revenu" / number of times the client made revenue | yes | float, max 91; the notes call it "days with revenue" (inference, not the codebook); exceeds REGULARITY in 2.5% of rows | fine; wording | LEAK-2, writing |
| DATA_VOLUME | "nombre de connexions" / number of connections (likely volume) | yes | float, 49.2% NaN, 222,844 zeros (14.9%) | fine; note wording (issue 3) | CLEAN-10 |
| ON_NET | calls within Expresso | yes | float, 36.5% NaN, 75,587 zeros | fine; note wording | CLEAN-10 |
| ORANGE | calls to Orange | yes | float, 41.6% NaN, 42,873 zeros | fine; note wording | CLEAN-10 |
| TIGO | calls to Tigo | yes | float, 59.9% NaN, 65,956 zeros | fine; note wording | CLEAN-10 |
| ZONE1 | calls to zone 1 | yes | float, 92.1% NaN, 41,627 zeros | fine; note wording | CLEAN-10 |
| ZONE2 | calls to zone 2 | yes | float, 93.7% NaN, 28,064 zeros | fine; note wording | CLEAN-10 |
| REGULARITY | "nombre de fois que le client est actif pendant 90 jours" / times active in 90 days | yes, if the label window starts after the window (issue 2) | int, 1-62, never missing; codebook says 90 days but the max is 62 (the notes' "last 62 days" is inference) | fine; question on label timing | USE-3, LEAK-10 |
| TOP_PACK | "les packs les plus activés" / most activated pack | yes | category, 140 values (132 in the 1.5M cut); 8 carry trailing tabs but stripping merges none; 2 numeric codes (`301765007`, `305155009`, 21 rows); `pack_chinguitel_24h` (5 rows, Chinguitel is Expresso's Mauritanian brand); 41 values with <= 5 rows | fine (as released) | CLEAN-14, CLEAN-8 |
| FREQ_TOP_PACK | times the top pack was activated | yes | float, max 713, NaN exactly with TOP_PACK | fine | CLEAN-14 |
| CHURN (target) | "variable à prédire" | label | 1/0 mapped to Yes/No; 18.75% Yes; no missing | fine | CLEAN-15 |

**Evidence behind the verdicts**

**REGION is the only column whose missingness follows the outcome.** Area under the curve of the missing flag alone,
within strata of active days (REGULARITY 1-3 / 30-50 / 62), full file:

| Column | 1-3 | 30-50 | 62 |
|---|---|---|---|
| REGION | 0.652 | 0.870 | **0.936** |
| MONTANT, FREQUENCE_RECH | 0.546 | 0.610 | 0.557 |
| REVENUE, ARPU, FREQUENCE | 0.546 | 0.604 | 0.553 |
| ON_NET | 0.561 | 0.597 | 0.576 |
| ORANGE | 0.536 | 0.615 | 0.562 |
| TIGO | 0.513 | 0.580 | 0.590 |
| TOP_PACK, FREQ_TOP_PACK | 0.530 | 0.601 | 0.559 |
| DATA_VOLUME | 0.544 | 0.465 | 0.452 |
| ZONE1 / ZONE2 | 0.50 | 0.50 / 0.49 | 0.51 / 0.45 |

Every window column's missing share falls with activity in both groups (MONTANT: churners 0.93 to 0.13, stayers 0.88
to 0.01); REGION's stays at 0.92-0.95 for churners in every band while it falls from 0.67 to 0.07 for stayers. Among
customers active on all 62 days, missing REGION alone separates churners at AUC 0.936; no window column passes 0.59.
That is the signature of a field looked up after the label period (a location from recent network events), LEAK-10.
LEAK-38 (keep anonymised host fields with a note) does not fit: REGION is a named field and the mechanism is measured,
not suspected. The drop stands; this replaces the "what would settle it" of REVIEW_before issue 1 with a measured
contrast that can go into the decision table.

**NaN is not "no activity".** The `ACTIVITY` docstring and the curation note say the columns "are missing when the
customer had none of that activity". Zeros coexist with NaN in DATA_VOLUME, ON_NET, ORANGE, TIGO, ZONE1, ZONE2, and the
two carry different churn: ON_NET NaN 42.3%, 0 12.6%, > 0 4.6%; DATA_VOLUME NaN 30.6%, 0 8.1%, > 0 7.0%. NaN means no
record in that aggregate, 0 a record with zero. Keeping them distinct is correct (CLEAN-2, CLEAN-10); only the wording
is wrong.

**ARPU_SEGMENT** equals round(REVENUE / 3) in all 1,428,000-odd non-missing rows (floor matches only 64.8%), and the
leak probe shows no loss without either (0.899). It adds nothing and splits REVENUE's importance in two.

**Label timing.** Churn is 70.7% at 1 active day, 53.3% at 2-3, 0.37% at 62 (612 of 166,477). The 612 always-active
churners show the 90 inactive days do not fall inside the window for them; they cannot tell whether the 90 days are
counted from the window's end or from each customer's last activity. Under the second reading, a customer last active
early in the window has part of the label period inside the window, and REGULARITY and the activity columns partly
measure it (the iranian_churn mechanism, LEAK-10 Cases). Nothing in the codebook or the data settles it.

**Problems, ranked (principles.md)**

1. **P3/P4, question for the curator (LEAK-10, USE-3): when do the 90 inactive days start?** Evidence above;
   REGULARITY carries the task (0.890 alone, 0.857 without it). If counted from last activity, the low-activity rows
   overlap the label period. Mildest remedy: keep, and say in `fit_reason`/notes that the 612 churners only show the
   label period is not inside the window for active customers, and that the start of the 90 days is not published
   (already "inferred"; make the alternative explicit). No data fix exists.
2. **P4, confirmed (LEAK-10, strong): REGION dropped correctly.** Missing-flag AUC 0.936 at 62 active days vs <= 0.59
   for every window column. Remedy: none to the data; add this per-column contrast to the decision table or notes so
   REVIEW issue 1 can close; state why LEAK-38 does not apply (named field, measured mechanism).
3. **P7, cleaning (CLEAN-5, Should): ARPU_SEGMENT is round(REVENUE/3) in 100% of rows.** Mildest remedy: drop it
   (cheap, safe, no score change); otherwise keep as an exception with the fact and higher principle named (none
   obvious, so the drop is preferred).
4. **P7/procedure (CLEAN-10 wording, writing.md): "missing when no activity" is wrong for six columns** (zeros coexist
   with NaN, churn differs: ON_NET 42.3% / 12.6% / 4.6%). Remedy: reword the `ACTIVITY` docstring and the note to
   "missing when the extract has no record of it; 0 is a record of none"; keep the values.
5. **Procedure (LEAK-2, EV-2): the codebook is not cited.** `VariableDefinitions.csv` exists on the Zindi data page and
   in the run folder; the notes describe FREQUENCE as "days with revenue" (codebook: number of times), REGULARITY as
   "active days in the last 62 days" (codebook: in 90 days, data max 62), and MRG only as a flag. Remedy: name the file
   in `download_description` and quote it where a note infers a meaning; mark the 62-day reading as inferred; note the
   codebook calls REVENUE monthly while ARPU = REVENUE/3 = 90-day income / 3.
6. **P7, question (CLEAN-14, LEAK-10 weak): TENURE has no band under 3 months** (D 3-6 m is the lowest, 770 rows of
   2.15M). Either the extract excludes customers under 3 months or tenure is taken at extraction, after the label
   period. Effect small (95% in K). Remedy: one line in the notes; no change.
7. **P7, fine as released: TOP_PACK** keeps 8 tab-suffixed values (no collisions on strip), 2 numeric codes and one
   Chinguitel (Mauritania) pack; 140 values, categorical. No change.

</details>

<details><summary>Split audit</summary>

**Verdict: right with notes.** IID over customers of one undated snapshot is the only split the release allows, it
mirrors the competition, and every alternative I could build from the data scores the same. What is missing is the
SPLIT-8 bookkeeping: the task is temporal in nature (the operator scores each window with a model trained on an earlier
one) and ships as forced IID, but it is not tagged that way.

Judgment record:

```text
Verdict: right with notes.
Validity: SPLIT-1 holds as far as the data allows; SPLIT-8 triggered, partly met (fit_reason names the gap; tag and
  measurement missing); SPLIT-29/30 hold (no hidden-group hit, no entity across the split); USE-10 known entity, history
  absent from the release (part of the SPLIT-8 gap).
Value: n/a here.
Weighed: competition split +, unmeasurable drift -.
For the curator: issue 1, a consistency call (tag ForcedIIDFromTemporal here and on the churn siblings, or on none).
```

**Facts checked (numbers)**

1. **Shipped folds.** 1,500,000 rows, regime `iid`, 1 repeat x 3 folds, each 1,000,000 train / 500,000 test, train and
   test disjoint, churn 18.75% on both sides of every fold. Matches `split` in `task_summary` and
   `version_comment`.
2. **Zindi's test set is a uniform random 15% of the extract (claim 31, confirmed by measurement, EV-2).** All 2,154,048
   user_ids decode as SHA-1 of `str(i)`, i from 2 to 2,534,174. So the extract held 2,534,175 customers and
   Test.csv is 380,127 of them (15.0%). In each of the 25 full blocks of 100,000 extract rows, Train.csv holds 84.8% to
   85.2%: the held-out share does not move along the extract. The competition's split is IID within the snapshot.
3. **The extract order is not time.** It has structure: short-tenure customers sit in runs (the share with tenure over
   24 months is 6% to 29% in extract rows 0-30k and 150-190k, 94% to 100% elsewhere), the heaviest data users all sit in
   rows 1,400-2,500, and churn per 100k block runs 13.1% to 22.6% (13% in rows 1.9M-2.2M), with rolling churn over 10k
   rows varying 7x more than chance (std 0.029 against 0.004). Lag-1 correlation of churn, REGULARITY and
   MONTANT along the order is 0.01. This reads as a customer-number or cohort sort, not an observation date: every row
   shares one window (REGULARITY is counted over the same last 62 days for everyone).
4. **Alternative splits cost nothing (600,000 random customers, untuned LightGBM, 300 trees, 3 folds each).**
   | Split | ROC AUC per fold | Mean |
   |---|---|---|
   | random, stratified | 0.9040, 0.9030, 0.9014 | 0.9028 |
   | contiguous thirds of the extract order | 0.8985, 0.9024, 0.9068 | 0.9026 |
   | 100k-row extract blocks, grouped | 0.9008, 0.9041, 0.9036 | 0.9028 |
   The best stand-in for "an earlier batch of customers" that the data offers gives the same score; the hidden-group
   probe agrees (12 candidates, no hit; near-copy clusters gap -0.000; composite keys none).
5. **Exact copies across the split do not inflate the score.** In a random fold 31.3% of test rows have an exact feature
   copy in train (the accepted sparse profiles). Those rows score lower, ROC AUC 0.752, against 0.869 on rows without a
   copy and 0.904 overall. They are distinct customers (unique user_id) with the same sparse profile, and a future
   window would hold the same profiles, so SPLIT-29 does not apply: no entity carries its label across the split.
6. **One prediction = one customer at the end of the window.** One row per customer (2,154,048 unique ids), so there is
   no group to keep together, and no aggregation question.

**Regime the use case implies**

The use case (the operator scores every active customer at the end of a window, for retention) is a known entity on a
stream over time: 94.85% of customers have tenure over 24 months, the operator has their earlier windows, and a
deployed model is trained on an earlier window whose 90-day labels have arrived. By USE-10 that is temporal, with each
customer's history (earlier activity and churn) as legitimate features, and with a gap of at least the 90-day label
delay between the training window's end and the scoring date. The release has one window, no dates and no history, so
none of that can be built: neither the temporal split, nor the gap, nor the season. SPLIT-9 (training rows whose label is
unknown at the prediction point) cannot arise inside one snapshot; whether every customer's 90 days were complete at
extraction is a target/leak question for the leak auditor, not testable from the split.

So IID is right by SPLIT-8 (temporal in nature, no dates at all, ships as IID), and the fit `approximate` with its
`fit_reason` already says what the timestamp would change.

**Problems, ranked (P4, then strength, then effect)**

1. **P4, SPLIT-8 (Must), partly met: no `ForcedIIDFromTemporal` tag and no measured cost of the missing time axis.**
   Evidence: `dataset.py` sets no `data_tags`; the split rationale is a class comment ("IID (one snapshot, no time
   index)") and the curation note "IID split, as in the competition". `definitions.md` reserves the tag for exactly
   this case, and account_debt_south_africa, home_credit_default_risk, aps_failure, food_delivery_time, forest_fires and
   distribution_transformers_at_cauca_department carry it. Mildest remedy: add `data_tags = ("ForcedIIDFromTemporal",)`
   and extend the IID note with one sentence: the window's dates and each customer's earlier windows would allow a
   temporal split with a 90-day gap and history features, and should be recovered if a later release has them; held out
   by extract-order thirds or 100k blocks, ROC AUC stays 0.903 (random 0.903), but the extract order is a customer sort,
   not time, so this does not measure drift between windows.
   **Consistency check:** the other one-snapshot churn definitions (churn_telco_south_asia, mobile_churn,
   bank_customer_churn) carry no tag either, while account_debt_south_africa (one extract standing in for the next) does.
   Either churn-at-a-snapshot is forced IID from temporal for all of them, or none; the curator should decide once.
   (a) tag all four; (b) tag none and record why a churn snapshot is not "temporal in nature" under SPLIT-8.
2. **P4, SPLIT-1 / USE-10 (Must), unfixable gap stated: training and test share one window.** A deployed model meets
   between-window drift and the 90-day-plus label delay; the benchmark cannot. Already said in `fit_reason`; no remedy
   in the data. Keep as is.
3. **Procedure (writing), minor: the split claim in notes is right but could cite its evidence.** "Zindi's test set is
   a uniform random 15% of the extract" is now measured (84.8%-85.2% of every 100k block of the decoded order in
   Train.csv); the record cites an adversarial AUC of 0.500. Optional: add the per-block share to the note, and say the
   decoded order shows tenure cohorts, which also answers earlier REVIEW issue 4 (extract order): it is not a time axis
   and holding it out costs nothing.

**Not problems**

* Hidden groups / near copies: no hit, gap 0 (SPLIT-29, SPLIT-30).
* Exact copies: distinct customers, lower score on copied rows (finding 5); the accepted warning stands.
* Sub-sample: 1.5M stratified, folds stratified and disjoint (finding 1). My replication of the sub-sample from the raw
  file did not reproduce the shipped rows (the pipeline's input order differs from the raw file order), so the
  alternative-split fits use their own 600k random sample of the raw file, not the shipped rows.

</details>

<details><summary>Domain practitioner</summary>

Role: a churn/CVM (customer value management) analyst at a prepaid mobile operator in Senegal who scores the base each
month and hands a target list to the retention team. Read: `dataset.py` (task_summary, curation_comments), the record,
the Zindi competition page, `use_case.md`, the panel's claims/checklist/probes. Own analysis on the raw Train.csv
(2,154,048 rows).

**Fit: approximate (agree)**

The rows are window aggregates of existing customers and the label is the operator's own 90-day dormancy churn after the
window, so the decision is real (USE-1, USE-2 pass); but it is one undated snapshot split at random, while I would train
on last quarter and score next month, and the label's horizon relative to the window is inferred, not published
(USE-8 "one snapshot standing in for a forecast"; USE-9 does not turn it direct, per the weighed factor "a use case
rephrased only to excuse a gap").

**The four questions, as the actor**

1. **Inputs at the prediction point (USE-3, USE-6).** Everything kept is something I would have at month end: tenure
   band, top-ups (MONTANT, FREQUENCE_RECH), revenue, ARPU, data volume, on-net/off-net/zone minutes, top package, active
   days. Nothing kept looks post-window (leak probe: no reading). What I would *not* trust is REGION as released: its
   missingness follows the outcome (92-95% missing among churners at every activity level); dropping it is right
   (USE-3/LEAK-10, USE-12: fix and keep the task). What I would always have and is missing: **recency** (days since last
   event / last top-up), the month-by-month trend inside the window (a falling customer vs a steady low one), main
   balance, multi-SIM / dual-SIM indicators, handset, complaints, porting requests, and the region computed from the
   window's own cell sites. Recency in particular is the single feature every prepaid churn model I know is built
   around; REGULARITY (active days in the last 62) is a partial stand-in for it, which is why it alone gives AUC 0.890.
2. **Target (USE-5).** The 90-day no-transaction rule is the operator's (and regulators') definition of prepaid churn
   (see ICASA/NCC sources), so it is the outcome I report. It is a proxy for what I act on, though: I act on
   *preventable loss of value*. Churners hold only 2.0% of the window's revenue; 80.9% of churners had no revenue at all
   in the window; 61% of churners were active on at most 3 of the last 62 days (churn 71% at 1 active day, 0.4% at 62).
   Most positives are SIMs that are already dormant (often secondary SIMs in a multi-SIM market) that no retention offer
   would target. I want a probability (Zindi asks for raw probabilities so the client can set thresholds), so ROC AUC /
   log loss fit; value-weighted or uplift scoring is what I would really optimise, but no benchmark data supports that.
3. **One row = one decision; test data.** One customer scored once at the window's end matches my monthly batch (an
   existing, known customer: USE-10 is satisfied by the window aggregates being the history; USE-11 one row per entity
   is the use case here). The test data is not what I face: I score the *next* month's base after campaigns, price
   changes and seasonality (Tabaski, Ramadan, school year), not a random 1/3 of the same month. Customers with < 3
   months' tenure are absent (bands A-C missing; 94.9% are > 24 months), so the early-life churn that dominates
   prepaid churn volume is out of scope; the task_summary's row ("customer active in the window") should say so.
4. **Would I use it?** As a ranking of the base, yes: AUC 0.90 is plausible for this feature set. But the model's lift
   over my existing rule ("flag customers with few active days") is small: LightGBM 0.900 vs REGULARITY alone 0.890.
   Among customers active on >= 30 of the last 62 days (the ones worth retaining; 967k customers, 1.4% churn),
   REGULARITY alone falls to AUC 0.716, so the benchmark's headroom lives mainly in that segment, which is a fine test of
   models but only 3.4% of the positives (13,757 churners). I would trust it more with a dated out-of-time test and a
   recency feature; I would distrust it for value targeting, since the metric is dominated by already-dormant SIMs.

**Gaps between the dataset and the real decision, ranked by how much they change the task**

1. **Positives are mostly already-dormant SIMs (task mostly "is it dormant now").** 81% of churners have no revenue in
   the window, they hold 2% of revenue, and REGULARITY alone reaches 0.890. The task as shipped measures how well a model
   refines an activity count, not how well it finds at-risk valuable customers. This is the operator's churn definition,
   so it is not a wrong target (USE-5 pass), but it should be named in `fit_reason` / `predicted` as part of the gap.
   Not a reason to change the data: restricting to active customers would be a different task (the record's 5.9% note
   is about duplicates, not this) and a curator's call. Rules: USE-5, USE-8; links to the TP-4 `one_feature` flag.
2. **Random split of one snapshot instead of next-month scoring.** Already in `fit_reason`; no dates exist, so nothing
   can fix it (USE-8 approximate, SPLIT regime stated). The extract-order effect (churn 13-23% per 100k block, earlier
   issue 4) hints the extract has structure a next-month test would expose; with user_id dropped it is not usable.
3. **Missing inputs I would always have: recency, within-window trend, region from the window.** These make the
   benchmark harder than the real task, not leakier; acceptable for an approximate fit (USE-6: not a leak, just absent).
   Dropping REGION (USE-3, LEAK-10) is correct; the practitioner's version would carry a window-derived region.
4. **Label horizon inferred.** The source says only "inactive ... for 90 days"; the 612 churners active on all 62 last
   days support that the label window follows the observation window, but whether all 90 days were complete at
   extraction cannot be checked (checklist "cannot verify"). Stated in `fit_reason`.
5. **Population: no customers under 3 months' tenure, 95% over 24 months.** Minor; worth one clause in `row`.

**What a domain expert would change**

* Keep the task and the `approximate` fit; keep REGION dropped.
* Extend `fit_reason` (or `predicted`) by one clause: most churners were already nearly dormant in the window (81% with
  no revenue, 2% of revenue), so the task ranks dormancy more than the at-risk value a retention offer targets.
* Add to `row`: the base is almost all long-tenure customers (no tenure under 3 months).
* Optional (curator's call, not a fix): a value-focused variant on customers with revenue in the window (1.43M rows,
  5.4% churn) would be the closer retention task; it is a different dataset, not a cleaning step.
* Refresh the stale `one_feature` per-fold numbers (checklist issue 2) since the TP-4 argument rests on them.

**Sources**

* Zindi competition page: churn = "becoming inactive and not making any transactions for 90 days", metric AUC, raw
  probabilities so "the client can set its own thresholds": https://zindi.world/competitions/expresso-churn-prediction
* Zindi discussion 8922 (REGULARITY 1-62, NaN = no activity; no official answer):
  https://zindi.world/competitions/expresso-churn-prediction/discussions/8922
* Zindi discussion 8742 (ARPU_SEGMENT = 90-day income / 3; MONTANT unclear):
  https://zindi.africa/competitions/expresso-churn-prediction/discussions/8742
* 90-day inactivity as the prepaid churn/dormancy rule: ICASA 2026 (https://technext24.com/2026/07/02/south-africans-to-lose-inactive-phone-no/,
  https://innovation-village.com/south-africa-to-recycle-inactive-prepaid-numbers-after-90-days/); NCC Nigeria
  (https://consumer.ncc.gov.ng/articles/118-all-you-need-to-know-about-churned-lines-in-the-telecom-industry-in-nigeria)
* Prepaid churn practice, early-life churn: https://www.telecoms.com/oss-bss-cx/the-pre-paid-market-needs-to-learn-how-to-say-yes;
  Customer Churn in Mobile Markets (arXiv 1607.07792): https://arxiv.org/pdf/1607.07792

</details>

<details><summary>Blind review</summary>

**Verdict: include with changes.** This is a real telecom churn task with honest IID evaluation, as far as I can check. But one feature, REGULARITY, carries almost all of the signal, so methods will differ very little. The row count also differs from the public source and has to be explained.

**What the task is**
Expresso is a telecom operator in Senegal and Mauritania. A retention or marketing team would score its prepaid customers on their recent activity and then target the ones likely to stop. Zindi defines churn as becoming "inactive and not making any transactions for 90 days". This is a real use, and the data comes from an operator, not a generator. Plausibility checks:
- ARPU_SEGMENT is about REVENUE/3, with a median ratio of 0.3333, as the definitions say.
- TOP_PACK names are real Expresso bundles, e.g. "All-net 500F=2000F;5d".
- The churn rate is 18.7%.
- REGULARITY ranges from 1 to 62. Missing activity values mean "no activity".

**Concerns (most serious first)**

1. **One feature nearly decides the task.** Analysis on the 200k sample, 2/3 train and 1/3 test:
   - REGULARITY alone gives AUC 0.890.
   - LightGBM on all 15 features gives AUC 0.901, log loss 0.296.
   - REGULARITY takes 78% of the gain importance.
   - Churn falls steadily as REGULARITY rises: 70% at REGULARITY=1, 4% at 10 or more.

   There is little room left for methods to differ. In the original competition the top log-loss scores were also packed close together. **Change:** keep the task, but weight it low or flag it as near-saturated. Use log loss, not accuracy, to separate methods.

2. **Possible time overlap between REGULARITY and the label.** REGULARITY is "the number of times the client is active for 90 days", and the churn label is "inactive for 90 days". The public pages do not say whether these two 90-day windows are separate, i.e. whether the features come strictly before the label period. If the windows overlap, the label is partly built from REGULARITY. Some signs point that way:
   - 24% of rows have every activity column missing, and their churn rate is 53%.
   - Among those rows, churn is 74% at REGULARITY=1.

   This is also what a genuine "dormant customer" signal looks like, so I cannot decide it from the data. **Change:** record the open question. If Zindi's VariableDefinitions.csv or the host can confirm the timing, cite it.

3. **Row count and columns differ from the source.**
   - The main Zindi page says Train.csv covers "2 million customers", and the original file has about 2.15M rows. task.md says 1.5M rows.
   - The original columns user_id, REGION and MRG are absent here. Dropping user_id is right. MRG is constant in the original, so dropping it is right too. REGION is a legitimate feature with about 40% missing.

   **Change:** document which edition or file the 1.5M rows come from, and why REGION was dropped. If it was dropped by accident, put it back.

4. **Many copies of the same feature vector.**
   - 29% of rows in the sample are exact feature duplicates of another row: 58k duplicated rows, covering only 2,082 distinct vectors.
   - 30% of test rows have an identical feature vector in train.

   These are mostly customers with every activity column missing, identified only by TENURE and REGULARITY. They are distinct customers (in the source each has its own user_id), so this is not leakage. It is how dormant users look. It does mean the effective information is lower than 1.5M rows suggests. **Change:** none needed. Mention it in the description.

5. **Size.** 1.5M rows is far more than needed to score this task, and it is costly for slow methods. **Change:** subsample to around 100k to 200k rows, stratified on CHURN. I saw no loss in signal at 200k.

6. **Preparation is fine.**
   - TENURE is categorical. It is ordinal, and 95% of rows are "K > 24 month".
   - TOP_PACK is categorical with 101 levels in the sample, with a long tail. FREQ_TOP_PACK has exactly the same missing rows as TOP_PACK.
   - Missing values are kept as NaN, which is correct, because they mean no activity.
   - A minor point: REVENUE is roughly MONTANT, so the two are redundant. That is not a problem.

**What I could not check**
- The 90-day timing between features and label, because VariableDefinitions.csv is not shown on the page.
- Where the 1.5M rows come from, versus the 2.15M rows in the original Train.csv.
- The full 1.5M rows; I only had the 200k sample.
- Whether Zindi's own split was by time. No date column is present, so IID is the only option and seems acceptable.

Sources: https://zindi.world/competitions/expresso-churn-prediction/data , https://zindi.africa/competitions/expresso-churn-prediction

</details>

<details><summary>Precedent check</summary>

Folder F = `datasets/_dev/tabarena-v0pt2/expresso_churn_prediction_1m/`, record R = `curation/records/expresso_churn_prediction.md`.
The precedent register raises no flag on this
dataset; the pairs below come from reading the cases behind the rules.

Who decided what: the only curator decision in R is Lennart's CC (undated, screening). It says IID as in the
competition and asks for a check of train-test region drift. Every other choice (REGION dropped, duplicates kept,
one_feature kept, user_id dropped, year) is an AI decision (assessment 2026-10-07, the definition and REVIEW.md)
that the curator has not confirmed yet. The checks below therefore look at the AI's draft and at the curator's
pending call on REVIEW issue 1.

**Summary**

| # | Decision | Verdict | Closest precedents |
|---|---|---|---|
| 1 | REGION dropped (outcome-driven missingness, LEAK-10) | **departs with a stated reason, but the reason misreads the closest precedent** (kick) | kick `WheelType` kept (Lennart, 2026-10-01); homesite kept (Lennart, 2026-10-01); 2_month_survival `adls`/`adlsc` dropped (Lennart, 2026-10-12); mic (LEAK-10 case) |
| 2 | Exact duplicate rows (31.5%) and 6,986 conflicting rows kept (LEAK-16, LEAK-18, LEAK-20) | consistent | cdc_diabetes (2026-10-07), sepsis_survival (2026-10-06) kept; jm1 deduplicated (2026-10-01): told apart by facts |
| 3 | one_feature kept, REGULARITY the natural core (TP-4) | consistent; procedural note | sepsis_survival, california (2026-10-06); own TP-4 case row (2026-10-07) |
| 4 | IID split, one undated snapshot, fit `approximate` (SPLIT, USE-8) | consistent | Lennart's CC; account_debt_south_africa (USE-8 approximate, one snapshot) |
| 5 | `user_id` dropped (extract order used by the 3rd place) (CLEAN-3, CLEAN-20, LEAK-10 ids) | consistent | sdss_17 `plate`/`fiber_ID`; huntprohibited (ids) |
| 6 | `MRG` constant dropped (CLEAN-5) | consistent | rule text |
| 7 | `ARPU_SEGMENT` = round(REVENUE/3) kept (CLEAN-5) | consistent | 2_month_survival `dzclass` (deterministic coarsening, "CLEAN-5 not triggered") |
| 8 | year 2020 (UmojaHack release), BibTeX 2021 competition (PROV-9, PROV-10) | year consistent with PROV-9; the BibTeX is a small open point under PROV-10; the "same as pkdd" framing does not fit | PROV-9 text (Lennart, 2026-10-12/14); pkdd REVIEW issue 10 |
| 9 | Sibling cuts (Azubian, DSN, Sasol, indabax) as duplicates (PROV-6, PROV-7) | consistent; one sibling record still out of step | indabax_eswatini_2022 No/Duplicate (Lennart, 2026-10-12); customer_churn_prediction_challenge_for_azubian No/Duplicate; sasol still `suggestion: 'Yes'` |

**1. REGION dropped: departs from the closest precedent; the stated reason does not hold for it**

**The decision.** The definition drops REGION under LEAK-10 ("missingness that encodes the outcome"). REVIEW
issue 1 gives the precedent: "The precedent is mic's outcome-driven missingness. REGION is not an anonymised host
field like kick's or homesite's."

**The rules.** LEAK-10 (Must) puts "missingness that encodes the outcome" out. LEAK-38 (Should, narrows LEAK-10)
reads: "Anonymised fields that may be post-outcome, in data a company released for its own competition, stay, with a
`Potential leak, kept on purpose:` note". Its cases are homesite and kick (`.claude/skills/knowledge-curation/references/leak_checks.md`,
LEAK-38; also `evidence.md`, probe-3 row: "2. an anonymised field in data a company released for its own
competition (kick: missing `WheelType` ...)").

**The closest precedent is kick, not mic.** From `curation/records/kick.md`, CC (2026-10-01, Lennart):

> **WheelType, potential leak kept on purpose:** missing WheelType is likely blanked when a car is kicked back:
> missing for 24.9% of bad buys in every month vs 1.5% of good cars ... Dropping WheelType/WheelTypeID: LightGBM AUC
> ... 0.757 -> 0.691. Kept because the company released the data this way for the competition (missing in 4.5% of
> Kaggle test rows vs 4.3% of train) and the recording process is not documented. Revisit if it is.

Fact by fact:

| Fact | kick `WheelType` (kept) | expresso `REGION` (dropped) |
|---|---|---|
| Field anonymised? | **no**: a named field (Alloy, Covers, Special) | no: named regions (DAKAR, ...) |
| Missingness against the label | 24.9% of bad buys against 1.5% of good cars | 44.8% churn when missing against 1.8% when present |
| Suspected mechanism | blanked when the car is kicked back (post-outcome) | filled after the window (post-outcome) |
| Mechanism documented? | no | no ("what would settle it is how Expresso fills REGION") |
| Company released it this way for its own competition? | yes (Carvana on Kaggle) | yes (Expresso on Zindi) |
| Same missingness in the host's test set | 4.5% test against 4.3% train | **39.39% test against 39.43% train**, and the same profile by active days (1 day 0.872/0.870, 62 days 0.073/0.075). Measured today on Expresso's Test.csv (380,127 rows) |
| Cost of dropping | AUC 0.757 to 0.691 | AUC 0.930 to 0.901 |
| Evidence of the mechanism | an erratic month pattern (Sep-Oct 2010: 1 good against 218 bad) | a conditional test: among churners the share missing is flat (92-95%) across activity, tenure and revenue, while the window's own columns fall with activity in both groups; a model fit on stayers predicts 11% missing for the 612 always-active churners, and 94% of them have no region; the region values add nothing when present (0.913 against 0.912) |

So the distinguishing fact REVIEW.md gives ("REGION is not an anonymised host field like kick's") does not set the
case apart: kick's `WheelType` is not anonymised either. Every reason the curator gave for keeping kick (company
release, the same missingness in the host's test set, an undocumented recording process) also holds for REGION.

**Precedents on the other side.**

* mic (LEAK-10/LEAK-7 Mechanisms row; `leak_checks.md` Cases): day-1..3 ICU columns blank for patients who died
  earlier. The mechanism is known from the domain (a dead patient has no day-2 reading). It is not a company
  competition release.
* 2_month_survival_rate_prediction `adls`, `adlsc` dropped (CC Lennart, 2026-10-12, `curation/records/2_month_survival_rate_prediction.md`):
  "the surrogate interview's gaps depend on whether the stay lasted until the interview, which is after the
  prediction point". The method there is the one used here: the curator compared missingness across the outcome
  (46% against 24%) and kept the columns whose missingness did not depend on it (`edu`, `income`). But the timing
  was documented (interviews on study days 2-7), and the data come from a research study, not a company's
  competition.

**What could really set Expresso apart.** The evidence for a post-outcome mechanism is a conditional measurement
(EV-1, EV-2), stronger than kick's month pattern: REGION's missingness does not follow the window's activity among
churners, while every column taken from the window does. The region's values carry no signal of their own. Under
LEAK-6 ("a confirmed leak goes even when small") and LEAK-10 (Must), a measured leak is dropped. A curator could
also say that LEAK-38 covers only fields whose meaning cannot be checked ("Why: removing an unverified signal from
host-designed data is arbitrary"). A named field lets us test whether it belongs to the window, and here it does
not. That reading would make kick the odd case: `WheelType` is named too, and its missingness was tested only by
month.

**Kind of departure.** LEAK-38 is a Should that narrows a Must. Dropping a column that LEAK-38 would keep is not
unreasonable under the ranking (P4, LEAK-10 Must is served), but it needs a distinguishing fact. The one written
down is wrong for kick. There is a second inconsistency in the rules themselves: LEAK-38 says "anonymised", while
its own case (kick `WheelType`) is a named field. A precedent that contradicts its rule is flagged, not followed
(principles.md, "Conflicts between rules"). One of the two has to change, whatever is decided here.

**Drift and count.** There is no drift by one curator on one rule yet: Lennart kept kick and homesite on 2026-10-01
and dropped `adls` on 2026-10-12, on different facts. If Expresso is kept with a note, it is the third LEAK-38
keep, and the first that comes after a conditional test pointing to post-outcome. If it is dropped, the LEAK-38
wording should be amended so that kick and Expresso are both explained.

**Reflection prompt:**

```text
**Consistency check (AI, 2026-10-20):** the draft for expresso_churn_prediction_1m (REGION dropped under LEAK-10,
a departure from LEAK-38) differs from kick (`WheelType` kept as "potential leak, kept on purpose", Lennart
2026-10-01). The mechanism is the same: a named field in a company's own competition release, whose missingness
tracks the label (44.8% against 1.8% churn; kick 24.9% against 1.5% bad buys), with an undocumented recording
process and the same missingness in the host's test set (Expresso Test.csv 39.39% against 39.43%; kick 4.5%
against 4.3%). REVIEW.md tells them apart as "not an anonymised host field like kick's", but kick's WheelType is
not anonymised either. What sets Expresso apart?
(a) the conditional test: among churners REGION is missing at 92-95% at every activity level, while the window's
    own columns (and REGION among stayers) fall with activity, and the values add nothing (0.913 against 0.912).
    That is a measured post-outcome mechanism, which kick never had, so LEAK-10 (Must) applies. Record it as the
    distinguishing fact and amend LEAK-38's scope to "fields whose meaning or timing cannot be tested";
(b) treat Expresso like kick: keep REGION with a `Potential leak, kept on purpose:` note (mechanism, 0.930 to 0.901,
    revisit if Expresso documents REGION);
(c) reopen kick to match Expresso: run the same conditional test on `WheelType` (missingness by an in-window
    covariate, separately for good and bad buys) and drop it if it shows the same pattern;
(d) change the rule: amend LEAK-38 (drop "anonymised" or define its scope), since its kick case already
    contradicts the wording.
```

**2. Duplicate rows kept: consistent**

**The decision** (accepted check warning, decision table): 678,270 exact copies (31.5%) are kept, and so are the
6,986 rows (0.5%) whose feature vector occurs with both labels. Every row is a distinct customer (unique user_id).
75.3% of the copies have no activity value. Deduplicating would remove 317,548 of the 403,986 churners (18.75% churn
to 5.9%).

**Rules.** LEAK-16 (Must: a decision every time) is met. LEAK-18 (Should): "Few features and plausible repeats:
natural, keep them and say so." LEAK-20 (Should): drop vectors that occur with both labels "unless they are genuine
label" ambiguity that the task has.

**Precedents.**

* Followed: sepsis_survival_minimal_clinical_records (CC Lennart, 2026-10-06): 110,204 admissions over 975
  distinct vectors, "the duplicates are real patients", kept. cdc_diabetes_health_indicators (assessment
  2026-10-07, accepted): "every row is a distinct respondent, so the 23,899 duplicate rows are natural".
* Decided the other way: jm1 (CC Lennart, 2026-10-01), "deduplicated to be on the safe side": 25% copies, 88
  conflicting vectors, LightGBM 0.743 IID against 0.727 grouped by identical vector. The facts that set the cases
  apart: (i) jm1's copies may be one function reused (an entity repeated, LEAK-17), while Expresso's rows are
  verified distinct customers; (ii) the measured inflation: jm1 lost 0.016 AUC when grouped by vector, while
  Expresso's near-copy grouping gap is -0.000 (`probes/hidden_groups.txt`); (iii) in Expresso, dropping the copies
  changes the population and the target (79% of churners removed), which is a P3 question jm1 did not have.

The decision follows the precedents. No prompt.

**3. one_feature kept: consistent; the numbers in the note are stale**

**Rule.** TP-4 (Must): `Trivial` needs proof. Read the meaning first ("the natural core of a task ... is expected to
dominate"), then the raw feature must match or beat the methods fold by fold.

**Precedents.** The own case row, TP-4 Cases in `task_probes.md` (2026-10-07): "active days ... natural core of a
churn task; untuned LightGBM beats it 3 of 3". It follows sepsis_survival (age; kept 2026-10-06) and
california_house_prices_2020 (listed price; kept 2026-10-06). fitness_club, retired (2026-10-05), differs: the
single feature beat all 37 configurations, and the data was generated.

Consistent. Two procedural notes, neither a departure:

* The sepsis and aps_failure cases tested against tuned configurations. Expresso has no tuned results
  (`checklist.md`: no hpo_results), so the test ran against untuned LightGBM only. The direction is clear (0.900
  against 0.890 today), but it is a weaker test than the precedents used.
* The note's per-fold numbers (0.9023-0.9031 against 0.8896-0.8902) do not match today's probe (best per-split
  0.8989-0.9015). The note should say which run they come from, or be refreshed (writing.md).

**4. IID split, snapshot fit approximate: consistent**

Lennart's CC: "solved with IID in the competition, and all features are set up to be IID". The AI assessment
(2026-10-07) checked the region drift the CC asked for: adversarial AUC 0.500, Test.csv a random 15%. The profile of
REGION missingness by active days measured today is the same in Train and Test, which also answers the drift
question for REGION. The `approximate` fit with "one snapshot" follows USE-8 and its case account_debt_south_africa
("one snapshot stands in for a forecast", `use_case.md` Cases). The temporal-against-grouped tension does not apply,
because there is no time index and no group (hidden-groups probe: no hits). Consistent.

**5-7. user_id, MRG, ARPU_SEGMENT: consistent**

* `user_id`: an identifier (CLEAN-3) whose decoded order the 3rd place exploited. CLEAN-20 (Must) says to copy the
  top solutions' preprocessing, not their exploits. The extract order is like the pointing ids of sdss_17
  `plate`/`fiber_ID` (LEAK-10 Mechanisms row, dropped). Consistent.
* `MRG` constant "NO": CLEAN-5. Consistent.
* `ARPU_SEGMENT` = round(REVENUE / 3): rounded and rescaled, so not an "exact copy" in CLEAN-5's words. It follows
  2_month_survival `dzclass`, a deterministic coarsening of `dzgroup`, kept with "CLEAN-5 not triggered" (that
  dataset's REVIEW.md). Consistent. If the curator wants deterministic copies dropped, it is an amendment of
  CLEAN-5, and it would reopen `dzclass` too.

**8. Year 2020 and the BibTeX: year consistent; the citation is a small PROV-10 point**

* PROV-9 (Must; Lennart 2026-10-12/14): "the year of that first publication: a competition's launch ... not the
  BibTeX year of a later citation". The data was first released for UmojaHack on 27 June 2020, so `year = "2020"`
  follows PROV-9. REVIEW issue 5 calls this "the same year-semantics question as pkdd". It is not: pkdd's question
  was collection year against publication year (2013 against 2015, its REVIEW issue 10), and PROV-9 has settled it
  since. Here both candidates are publication years, and PROV-9 picks the first.
* PROV-10 (Must): "The citation is the work that published the data". The BibTeX cites the 2021 competition and
  names the 2020 release only in its note, and `source_url` points to the 2021 competition. That fits PROV-10 only
  if the 2021 competition counts as the publication. Then the year should be 2021, which contradicts PROV-9's 2020.
  Year and citation should name the same first publication. One more caveat: the 2020 UmojaHack release is not
  among the record's `source_links`, so the 2020 date rests on the BibTeX note alone (EV-2). This is minor and not
  a departure from a precedent, so there is no prompt. The panel should treat it as a PROV-9/PROV-10 coherence
  point.

**9. Siblings: consistent, one record out of step**

indabax_eswatini_2022 (Lennart, 2026-10-12, No/Duplicate) and customer_churn_prediction_challenge_for_azubian
(No/Duplicate) are handled alike. `curation/records/sasol_customer_retention_recruitment_competition.md` still has
`suggestion: 'Yes'`, priority 1 and a `Non-IID (Temporal)` tag. The AI assessments of 2026-10-07 and 2026-10-20
recommend No + Duplicate (a renamed 70% sample; Expresso's Test.csv itself). This is no departure by a curator: the
curator's call is pending. It should be settled with this dataset so the family is treated alike (PROV-6, PROV-7).

**Files**

* `curation/records/kick.md` (CC 2026-10-01, WheelType)
* `curation/records/homesite_quote_conversion.md` (CC 2026-10-01)
* `curation/records/2_month_survival_rate_prediction.md` (CC 2026-10-12, adls)
* `curation/records/jm1.md` (CC 2026-10-01)
* `curation/records/sasol_customer_retention_recruitment_competition.md`
* `.claude/skills/knowledge-curation/references/leak_checks.md` (LEAK-10, LEAK-38, Mechanisms table)
* `.claude/skills/knowledge-curation/references/evidence.md` (probe-3 row naming kick "anonymised")

</details>

<details><summary>Advocate</summary>

Position: ship as defined, after wording fixes and one tag. No phase A report refutes a validity claim (claim audit:
"No validity claim is refuted"); every real problem found has a fix at the "fix the definition" or "note" rung of the
remedy ladder, none that touches the data.

**1. A real task on real operator data (P2, P3; SEL-16, USE-1, USE-5 Must): holds**

- Evidence: actor (Expresso), moment (end of the window), decision (retention list). The target is the operator's own
  definition, "becoming inactive and not making any transactions for 90 days" (Zindi page), which the practitioner
  confirms is the industry and regulator definition of prepaid churn (ICASA, NCC). 403,986 / 2,154,048 = 18.75%
  reproduced. Generated probe: no flags; TOP_PACK messy as real data (140 packs, tab-suffixed spellings). Practitioner:
  "As a ranking of the base, yes"; fit `approximate` agreed by practitioner, split audit and blind reviewer.
- Against "positives are mostly dormant SIMs" (practitioner gap 1): that is the target the operator defines and reports,
  so USE-5 passes (the practitioner says so: "not a wrong target"). A value-weighted variant is a different dataset, not
  a fix. Mildest remedy: one clause in `fit_reason` (81% of churners had no revenue in the window).

**2. Dropping REGION is a measured LEAK-10 fix, and LEAK-10 (Must) outranks LEAK-38 (Should)**

- Evidence: among customers active on all 62 days, missing REGION alone separates churners at AUC 0.936; no window
  column passes 0.59 (column audit). Every activity column's missing share falls with activity in both groups; REGION's
  stays flat for churners (0.952 to 0.944) while falling for stayers (0.673 to 0.072) (claim audit, strongest test).
  REGION's whole value is its missing flag: window + flag 0.9309 against window + REGION 0.9311 (claim audit); the
  values add nothing (0.913 against 0.912).
- Rule: P4, LEAK-10 Must ("missingness that encodes the outcome"); LEAK-6, a confirmed leak goes even when small.
  Tension row "A real task against a leak": fix the leak and keep the task.
- Against the precedents point (kick kept under LEAK-38): concede that REVIEW.md's distinguishing fact ("not
  anonymised like kick") is wrong, since `WheelType` is named too. The right fact is the one kick never had: a
  conditional test showing a post-outcome mechanism. LEAK-38 is a Should narrowing a Must for fields "that may be
  post-outcome"; once the mechanism is measured, the Must applies. Fix: rewrite the distinguishing fact in the notes and
  REVIEW.md, and offer the curator the LEAK-38 amendment (precedents option (a)). Keeping REGION would ship a measured
  leak; that is the one choice the rules forbid.

**3. The IID split is the only split the release allows, and its cost is measured as zero (P4; SPLIT-1, SPLIT-8 Must)**

- Evidence: all 2,154,048 user_ids decode; Zindi's Test.csv takes 15.0% of every 100k block of the extract (Train share
  84.8% to 85.2%), so the competition split is IID. No dates exist. Stand-ins for an earlier batch score the same:
  random 0.9028, contiguous thirds 0.9026, 100k blocks grouped 0.9028; hidden-group probe no hits, near-copy gap -0.000.
  REGION's missing profile is identical in Zindi's Test.csv (39.39% against 39.43%), answering the curator's drift check.
- Concede: SPLIT-8 is partly met; `data_tags` lacks `ForcedIIDFromTemporal`. That is a Must on bookkeeping, fixed in
  the definition: add the tag and one sentence (what a dated window and customer history would change; recover them if
  released; extract-order holdout 0.903 but the order is a customer sort, not time). The sibling-consistency question
  (churn_telco_south_asia, mobile_churn, bank_customer_churn) is a curator call; it does not block this dataset.

**4. The duplicates are natural profiles of distinct customers (P4; LEAK-18 Should, LEAK-16 Must met)**

- Evidence: 2,154,048 unique ids; 75.3% of the 678,270 copies have no activity value; copied test rows score lower
  (AUC 0.752 against 0.869 without a copy), so they do not inflate the score; 1-NN agreement 0.653 below chance 0.695.
  Deduplicating removes 317,548 of 403,986 churners and turns the task into 5.9% churn among active customers, a
  different population and target (P3, USE-5). Precedents: sepsis_survival and cdc_diabetes kept; jm1 differs by fact
  (repeated entity, measured 0.016 inflation).
- Rule: LEAK-18 is the earlier rule of equal strength and covers this case ("few features and plausible repeats:
  natural, keep them and say so"). Concede the procedure point: add an `Exception to LEAK-19` line naming the fact
  (distinct customers; dedup changes the target) and the principle (P3). Also fix the wording "described only by a
  tenure band and their active days" to "mostly (75.3%)".

**5. one_feature is the natural core, and the methods beat it on every shipped fold (P6; TP-4 Must)**

- Evidence: on the three shipped folds, default LightGBM 0.9025 / 0.9029 / 0.9022 against REGULARITY 0.8901 / 0.8902 /
  0.8896 (claim audit reran it; the checklist's "stale numbers" concern is refuted). Among customers active on 30+ of
  62 days, REGULARITY alone falls to 0.716 (practitioner): real headroom for models. Same call as sepsis_survival,
  california_house_prices_2020, aps_failure (kept), unlike fitness_club (single feature beat all configs, generated).
- Against "weight it low" (blind review): TP-4 decides `Trivial` only with proof that the feature matches the
  methods; it does not. Concede that no tuned results exist, so the test is weaker than for the precedents; the
  direction can only widen with tuning.

**6. Label timing is an open question, not a leak (P4; LEAK-1 holds; USE-5, USE-8)**

- Evidence: every kept column summarises the window and is known at its end (column audit: "Known at prediction? yes"
  for all kept columns). 612 churners were active on all 62 last days and churn is 0.4% at 62 days, so the label
  period does not sit inside the window for active customers. This is not iranian_churn (LEAK-10 case: window ends at
  churn, AUC 0.986); here AUC is 0.90.
- If the 90 days count from each customer's last activity, part of the label period has elapsed at scoring time; that
  is how dormancy churn works for the operator too (recency is "the single feature every prepaid churn model is built
  around", practitioner), so it changes what the target means at most, not what is known. No data fix exists; mildest
  remedy: name the alternative reading in `fit_reason`, mark the 62-day reading of REGULARITY as inferred (Zindi
  codebook: "active for 90 days"), and cite `VariableDefinitions.csv`.

**7. The rest is P7 and procedure: notes, not reasons to hold the dataset**

- ARPU_SEGMENT = round(REVENUE/3): rounded, so not an exact copy under CLEAN-5 (Should); follows the 2_month_survival
  `dzclass` precedent ("CLEAN-5 not triggered"). Dropping it is cheap too; either is fine, a quality call.
- "Missing when no activity" is wrong for six columns where 0 and NaN coexist; the values are right, the docstring
  and note need rewording.
- Zindi's no-redistribution rule: EV-4 (Must) and selection.md say a licence is "no reason and no marker"; note only.
- Year 2020 follows PROV-9 (first release); align the BibTeX/source link under PROV-10. Wording: "92-95% at every
  number of active days" becomes "90-96%".
- The blind reviewer's "subsample to 100-200k" and its row-count/REGION questions are answered by the definition
  (`version_comment`, the REGION decision table); the 1.5M budget is the v2 protocol.

Judgment record:

```text
Verdict: ship after changes (no data change).
Validity: SEL-16 holds; USE-1, USE-5 hold (approximate fit); LEAK-10 triggered, fixed (REGION dropped), LEAK-38
  distinguishing fact to be corrected; LEAK-16/18 met, Exception to LEAK-19 to be written; SPLIT-1 holds; SPLIT-8
  partly met, add the ForcedIIDFromTemporal tag and sentence.
Value: TP-4, one_feature answered (LightGBM beats REGULARITY on 3 of 3 shipped folds).
Quality: CLEAN-5 ARPU_SEGMENT kept as released (or dropped, curator's call); wording fixes.
For the curator: LEAK-38 amendment (kick vs Expresso); forced-IID tag across the churn siblings.
```

**Rebuttal**

The critic and I reach the same verdict: ship after changes, with no data change and no exclusion. Most of the critic's
points are concessions I already made. What is left in dispute is how strong the problems are.

**1. SPLIT-8: concede in full**

I agree with the tag, the sentence and the curator's consistency call on the churn siblings. This is the only Must
whose fix is required before shipping, and the fix is in the definition alone.

**2. Label timing: concede the text, dispute the rank**

- Conceded: cite `VariableDefinitions.csv`, write the 62-day reading and the label start as inferred, and name the
  "90 days from last activity" reading in the notes and `fit_reason`.
- Disputed: this is not an open LEAK-10 Must.
  - LEAK-1 asks whether the features are known at the prediction point. Every kept column summarises the window and
    is known at its end. The column audit marks every kept column "yes"; on REGULARITY, the only conditional "yes",
    it rests its condition on this same label-start question.
  - Under the alternative reading, the label is partly determined at scoring time. That is what dormancy churn is for
    the operator too (the practitioner's point on recency). The question is about what the target means (USE-5,
    already "inferred" in the approximate fit), not about information leaking from the future.
  - The LEAK-10 case for a window that ends at churn (iranian_churn, AUC 0.986) has a different signature. Here AUC is
    0.90, and churn varies smoothly with activity, from 70.7% at 1 active day to 0.4% at 62.
- What follows: a note, as the critic's own remedy says. It is not a blocking Must.

**3. REGION's written reason: concede**

- Replace the kick sentence with the conditional test, put the per-column AUC contrast in the decision table, and give
  the curator the LEAK-38 prompt, options (a) or (c).
- The drop itself is agreed: the critic writes "the drop is right".

**4. The fit statement: concede the clauses, dispute "Must"**

- Conceded: add the dormancy clause to `fit_reason` and the long-tenure population to `row`.
- Disputed: the critic writes "USE-5 holds", so no Must fails. This is the writing rule (the task summary should say
  what the positives are), and it is fixed with a note.

**5. Year and citation: concede**

- Add the UmojaHack Ghana page as a source and drop "Senegal" unless a page for it is found.
- Year and citation must name one first publication. PROV-9 picks 2020. The fix is text in the definition.

**6. Wording: concede every item, and take the critic's remedy on the duplicates**

- LEAK-18 comes before LEAK-19 at the same strength and covers natural repeats. Citing LEAK-18 is cleaner than the
  `Exception to LEAK-19` line I proposed. Either one closes the procedure gap.
- The other wording fixes stand as the critic lists them: "90-96%", "mostly (75.3%)", 0 against NaN, and FREQUENCE as
  "number of times".

**Net result**

- Verdict: ship after changes, with no data change.
- Must fixes before shipping:
  - SPLIT-8: add the tag and the sentence.
  - PROV-9/10: make year and citation coherent.
- Notes and text fixes:
  - REGION: the reason, the decision table and the LEAK-38 prompt.
  - Label timing marked as inferred.
  - The fit clauses.
  - The wording.
- For the curator:
  - the LEAK-38 amendment;
  - the forced-IID tag on the churn siblings.

</details>

<details><summary>Critic</summary>

**Position: do not ship as defined; ship after the changes below.** No point here is a reason to exclude: the task is
real (USE-1, USE-2 hold), the REGION leak is fixed, the split mirrors the competition. What fails is one Must of P4
left half done, an inferred label timing written as fact, and a leak decision whose written reason is wrong.

**1. P4, SPLIT-8 (Must): forced IID from temporal, not tagged, cost not stated**

- Problem: the use case is temporal (the operator trains on an earlier window and scores the next one, with a 90-day
  label delay); the release has one undated window. SPLIT-8 requires the `ForcedIIDFromTemporal` tag, the cost of the
  missing time axis measured where the data allows, and a sentence on what a timestamp would change.
- Effect: the benchmark presents a forecast task as plain IID; a reader cannot see that between-window drift is
  untested.
- Evidence: `dataset.py` sets no `data_tags` (README: `data_tags | IID`); the split note says only "IID split, as in
  the competition". Split audit s8: extract-order thirds 0.9026, 100k blocks 0.9028, random 0.9028; the extract order
  is a tenure/cohort sort, not time. Precedent account_debt_south_africa carries the tag (Lennart, 2026-10-12).
- Remedy (fix the definition): `data_tags = ("ForcedIIDFromTemporal",)` and one sentence in the IID note (holding
  out extract blocks costs nothing, but the order is not time, so drift between windows is unmeasured; recover the
  window dates and earlier windows if a later release has them). Curator consistency call: the same for
  churn_telco_south_asia, mobile_churn, bank_customer_churn, or record why none of them is temporal.

**2. P3/P4, USE-3 and LEAK-10 (Must), EV-2: the label timing is inferred but written as fact**

- Problem: the notes say "the label window follows the observation window" and REGULARITY counts "the active days in
  the last 62 days of the window". Neither is published. Zindi's codebook (`VariableDefinitions.csv`, not cited)
  defines REGULARITY as active "pendant 90 jours"; the 62 maximum is unexplained (discussion 8922, unanswered).
- Effect: if the 90 inactive days count from each customer's last activity, low-activity rows have part of the label
  period inside the window, and REGULARITY (0.890 alone; 0.857 without it) partly measures the label. The 612
  always-active churners rule this out only for active customers, not for the 61% of churners active on at most 3 days.
- Evidence: column audit issue 1; claim audit claims 21 and 38 ("holds as consistency, not proof"; "untested, stated
  as fact"); blind review concern 2 raised it independently.
- Remedy (a note, plus a definition fix of the text): cite `VariableDefinitions.csv` in `download_description`;
  write the 62-day reading and the label start as inferred; name the alternative (90 days from last activity) and
  that nothing in the release settles it, in the notes and in `fit_reason`. No data change exists, so no exclusion.

**3. P4, LEAK-10 (Must) against LEAK-38 (Should): the drop is right, its written reason is false**

- Problem: REVIEW.md tells REGION apart from kick as "not an anonymised host field like kick's". kick's `WheelType` is
  a named field too, released by the company for its own competition, with the same missingness in the host's test
  set (Expresso Test.csv 39.39% against 39.43% in Train). So the stated distinguishing fact does not hold, and the
  curator is asked to decide on a wrong premise.
- Effect: a departure from a Should (LEAK-38) without a valid distinguishing fact; kick and Expresso are decided
  differently on the same written facts.
- Evidence: precedents section 1; the real distinguishing fact is measured: missing-REGION alone separates churners at
  AUC 0.936 among customers active all 62 days, against at most 0.59 for every window column (column audit); among
  churners REGION missingness stays 0.95 to 0.94 from 1 to 62 active days while every activity column falls (claim
  audit 28); the values add nothing (0.913 against 0.912).
- Remedy (fix the definition's evidence and REVIEW text): replace the kick sentence with the conditional test, put the
  per-column AUC contrast in the decision table, and give the curator the consistency prompt: (a) amend LEAK-38's
  scope to fields whose timing cannot be tested, or (c) run the same test on kick's `WheelType`. LEAK-38's own
  "anonymised" wording contradicts its kick case; flag it either way.

**4. P3, USE-5 and USE-8 (Must): the fit statement hides what the positives are**

- Problem: 80.9% of churners have no revenue in the window and hold 2.0% of its revenue; customers under 3 months'
  tenure are absent (no bands A-C; 94.9% over 24 months). The task largely ranks SIMs already dormant, not the
  at-risk customers a retention offer targets.
- Effect: the target is the operator's own churn definition (USE-5 holds), but `predicted`, `row` and `fit_reason` do
  not say that most positives are already dormant and that early-life churn is out of scope.
- Evidence: practitioner, gaps 1 and 5; column audit issue 6.
- Remedy (a note): one clause in `fit_reason` (most churners were already nearly dormant in the window) and one in
  `row` (long-tenure base, no customer under 3 months).

**5. P5, PROV-9 and PROV-10 (Must): year and citation name different publications**

- Problem: `year = "2020"` rests on the BibTeX note "first released for the UmojaHack Africa hackathons in Senegal and
  Ghana on 27 June 2020"; the citation and `source_url` are the 2021 competition.
- Evidence: claim audit claims 10/17: the Ghana UmojaHack page (27 June 2020) found, no Senegal page; the 2020 release
  is not among the record's source links (precedents section 8).
- Remedy (fix the definition): add the UmojaHack Ghana page as a source, drop "Senegal" unless a page is found, and
  make year and citation name the same first publication.

**6. Procedure (writing.md, EV-8): statements contradicted by the data**

- "92% to 95% at every number of active days": 89.5% to 95.7% by value (claim audit 27).
- The duplicate warning and decision say copies are "described only by a tenure band and their active days", yet
  24.7% of copies (167,726) carry activity values (claim audit 46/48).
- "Activity columns are missing when the customer had none of that activity": wrong for six columns where 0 and NaN
  coexist with different churn (ON_NET NaN 42.3%, 0 12.6%, >0 4.6%) (column audit issue 4).
- FREQUENCE "the days with revenue": the codebook says number of times.
- The duplicate keep cites no rule; cite LEAK-18 (natural repeats, which precedes LEAK-19) so it is not read as an
  undeclared departure from LEAK-19.
- Remedy: reword each; no data change. Quality and procedure only: no reason to withhold the task beyond the fix.

**Not argued**

Duplicates kept (LEAK-18; cross-split copies score lower, 0.752 against 0.869), one_feature (TP-4: the per-fold
numbers reproduce), the 1.5M size (the protocol's budget; the blind review's 100-200k is not a rule), ARPU_SEGMENT
(CLEAN-5 not triggered by the dzclass precedent), the licence (EV-4: a note, never a reason).

**Rebuttal**

We agree on the verdict: ship after changes, with no data change and nothing to exclude. Most of what remains is
concession. Four points stay in dispute, on what the changes must say.

1. **Real task, USE-5: concede.** The target is the operator's. The fit clause on dormant churners is agreed. The
   advocate does not answer the second half of my point 4: `row` should say the base has no customer under 3 months'
   tenure (bands A-C absent, 94.9% over 24 months; practitioner gap 5, column audit issue 6). That needs one clause.
   It is a USE-8 statement of the fit, not a fix to the data.

2. **REGION, LEAK-10 against LEAK-38: concede in full.** We agree on the drop, on the corrected distinguishing fact
   and on offering the LEAK-38 amendment.

3. **Split, SPLIT-8: dispute the words "its cost is measured as zero".** The 0.903 held out by extract order measures
   a customer sort, not time (split audit fact 3). The cost of the missing time axis, drift between windows plus the
   90-day label delay, is unmeasurable here, not zero. SPLIT-8 (Must) asks for the cost "where the data allows". The
   note must say the data does not allow it, not that the cost is zero. The advocate's own proposed sentence says
   this; the heading should match it. The tag and the sentence are agreed.

4. **Duplicates: dispute the `Exception to LEAK-19` line.** The advocate also says LEAK-18 is the earlier rule of
   equal strength and covers the case. Then the keep applies LEAK-18 and departs from nothing (principles.md: at
   equal strength the earlier rule wins). An exception line would record a departure that did not happen, and it
   would count toward the three-exception amendment trigger. Remedy: cite LEAK-18 in the note, and fix the
   "mostly (75.3%)" wording, which is agreed.

5. **one_feature, TP-4: concede.** The numbers reproduce on the shipped folds.

6. **Label timing: concede the remedy, dispute the framing.** "Not a leak" is not established. It holds only as
   consistency (claim audit claim 21: "holds as consistency, not proof"; claim 38: "untested, stated as fact"). Under
   the last-activity reading, part of the label period lies inside the window for low-activity customers, and
   REGULARITY partly measures it (column audit issue 1). Saying it is how dormancy works for the operator does not
   settle when the 90 days start. EV-2 (Zindi's codebook says "90 days"; nothing gives the 62-day maximum) decides
   how it must be written: as an open question in `fit_reason`, as the advocate also proposes. We agree on the text.
   The record must not say "not a leak".

7. **P7 and procedure: concede, except the year.** ARPU_SEGMENT, the licence and the wording fixes are agreed.
   PROV-9 picks the first publication, but the evidence for a 2020 release in Senegal is missing. The claim audit
   found only the UmojaHack Ghana page (27 June 2020) and no Senegal page, and the 2020 release is not among the
   record's source links. Remedy, as in my point 5: link the Ghana page, drop "Senegal" unless a source is found, and
   make the year and the citation name the same publication (PROV-10, Must).

Judgment record:

```text
Verdict: ship after changes (no data change).
Validity: USE-5 holds, USE-8 fit text extended (dormant churners, no tenure under 3 months); LEAK-10 fixed, LEAK-38
  fact corrected; label timing open, written as inferred (EV-2); SPLIT-8 tag plus "cost not measurable", not "zero";
  LEAK-18 applied (no LEAK-19 exception); PROV-9/10 year and citation aligned on a sourced 2020 release.
Value: TP-4 holds.
Quality: wording fixes; ARPU_SEGMENT is the curator's call.
For the curator: the LEAK-38 amendment; the forced-IID tag across the churn siblings.
```

</details>
