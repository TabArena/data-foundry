# mobile_churn

**Outcome:** added; recommended `No` (`Missing source information`) under PROV-1 as written, unless the curator amends
PROV-1/PROV-2 to cover an untraceable upload with an undefined label rule (issue 1); then ship as defined now.
Prepaid accounts of one unnamed operator at the end of June, July or August 2013: will the account churn after the
month? Random split over accounts (54,207 rows), the 12,262 SIM cards never activated dropped. Not built yet.

**Main points:** Keep a dataset whose source search ended with no upstream and whose churn rule is unknown, by an
amendment of PROV-1/PROV-2, or apply `No`? Then confirm the drop of the SIM cards never activated (issue 2).

**Record judgment:** don't ship under PROV-1 as written. Validity: SEL-1 and SEL-2 hold; USE-1 holds with an
approximate fit; USE-5 cannot be checked against a source, the same gap as PROV-1; USE-8 holds with the gap named and
a potential-leak note (the churn rule may be defined from the inactivity the recency columns measure); LEAK-10 holds
(the 100-day windows end at the snapshot); LEAK-22 applied, the never-activated SIM cards dropped (issue 2); SPLIT-1
holds; SPLIT-8 triggered, fixed with the `ForcedIIDFromTemporal` tag and the split wording (settled 2026-10-21); PROV-3 holds (no
marks of generated data); PROV-1 triggered, the search has ended with no upstream (issue 1). Value: LightGBM ROC AUC
0.848, 0.049 above a linear model, with 1,797 churners per test fold; no task-probe flag. Quality: the notes state the
measured numbers, name both default dates and note the missing values that the month's counts contradict. Weighed:
shape, signal and realism for; source and label definition against. Left for the curator: the PROV-1 rule (issue 1),
then the drop (issue 2).

**Issues for Lennart:**

1. **Keep a dataset with no traceable source and no churn definition?** I recommend (a), `No`, unless you adopt the
   wider amendment in (b) for all the untraceable keeps at once. Update (2026-10-21): PROV-2 was amended only for a
   named first platform ("a named first platform (a course or teaching provider) counts as a known source when the
   data shows no PROV-3 marks", Lennart). This dataset names no platform, so the amendment does not cover it: under
   the rules as they stand it is (a), `No` with `Missing source information`, and that needs your explicit call
   (or the wider wording of (b)).
   - Problem: every link ends at the Kaggle upload `dimitaryanev/mobilechurndataxlsx` (2019-10-31): empty
     description, licence "Unknown", no other datasets or notebooks by the uploader. OpenML 44231 is a cell-for-cell
     copy that points back to it ("No description available", creator "UNK"). Neither page defines churn: no rule,
     no horizon, no operator.
   - Effect: we cannot tell whether the label means "deactivated by the operator" or "inactive N more days", two
     different targets. The study the practitioner cites (Radosavljevik, van der Putten and Larsen, "The Impact of
     Experimental Setup on Prepaid Churn Modeling") finds that the churn definition changes how predictable prepaid
     churn is more than any other choice in the setup.
   - What the data settle: the label falls after the month's snapshot for both classes, and it is not "inactive N
     days at the snapshot" (in June the churn rate is 4.6% at 0-5 days without activity and 61% at 60-75 days, with
     no cutoff). No single feature restates it (best ROC AUC 0.779 against 0.844 for all features). The data look
     like a real system export (default dates, refunds, sentinels contradicted by counts); the generated-data probes
     raise no flag.
   - The search has ended (review panel's source search, 2026-10-20): exact-string web searches for the column names
     and the file name; a GitHub code search (only later users: the TabSTAR annotation, student projects, a 2025
     hiring case with the same columns and no origin); the Kaggle notebooks on the dataset (they call it "an
     anonymous telecommunications company"); the CTGAN-ENN paper (Journal of Big Data 11:121, 2024), which cites the
     Kaggle page; and the OpenML upload batch 44228-44231, none of which names an origin. Left unread: the one Kaggle
     discussion topic, which needs a logged-in browser
     (https://www.kaggle.com/datasets/dimitaryanev/mobilechurndataxlsx/discussion); its question of 2021-12-27, "can
     you give me the time frame of the collected data, and its provenance", had no answer when the review of
     2026-10-07 read it.
   - A clue that does not hold: on-net calls are rare (0.3 per account and month against 16.3 off-net), which the
     earlier review read as a small operator or a virtual operator; but the calls by destination add up to the total
     in only 10.8% of rows, so a fourth destination is likely and the clue proves nothing.
   - Rule: PROV-1 (Must: an untraceable source is `No`), PROV-2 (Should), USE-5 (Must, the label checked against the
     source). An uploader handle with no description identifies nothing about the data's origin; PROV-3 passing says
     the data are real, not what they are. Nothing ranked above PROV-1 needs the keep.
   - Precedent: water_quality_and_potability went `No` under PROV-1 although its data were judged sound.
     bank_customer_churn (data from a named data-science course) and tour_travels_churn (a bare Kaggle upload with no
     named origin) were kept; that contradicts the rule, so it is no precedent to follow. churn_telco_south_asia kept
     an undated label with a note, but it has two source papers. Your screening keep ("data looking very good and
     real") was made knowing the source was missing, but it departs from a Must without a fact that sets the case
     apart, so the way out is an amendment, not an exception.
   - Implemented: kept, with the gaps in `fit_reason` (no stated churn rule or horizon, operator unknown) and a
     `Potential leak, kept on purpose:` note in the form churn_telco_south_asia uses; cost: it ships against PROV-1 as
     written unless (b) is adopted.
   - Alternatives:
     - (a) apply PROV-1: `No` with `Missing source information`; cost: a large, real-looking prepaid churn task
       leaves, and the decision differs from tour_travels_churn and bank_customer_churn unless they are reopened;
     - (b) amend PROV-1/PROV-2 once for bank_customer_churn, tour_travels_churn, credit_card_customers and
       mobile_churn, and decide newspaper_churn the same way. The wording proposed for credit_card_customers ("a
       named course or teaching platform counts as a known source when the data shows no PROV-3 marks") does not
       cover this dataset, which has no named platform. A wider wording would, for example: "an untraceable first
       upload stays when the data passes PROV-3, the prediction point and label timing are measured on the data, and
       the gaps (source, label rule) are written as an approximate fit with a potential-leak note". It must also say
       whether an undefined label rule is allowed. Cost: a Must gives way for a class of datasets whose origin nobody
       can check, and the benchmark carries a churn label whose rule is unknown;
     - (c) reopen tour_travels_churn and bank_customer_churn (and credit_card_customers) to match
       water_quality_and_potability; cost: up to four churn datasets leave, bank_customer_churn among them, which
       shipped in TabArena v0.1.
   - The cross-dataset item "Amend PROV-1/PROV-2 for a named course or teaching platform" was decided on 2026-10-21
     with the narrow wording (credit_card_customers, bank_customer_churn); (b) would widen it further.
   - Decision needed: (a) `No`, (b) the wider amendment, or (c) reopen the earlier keeps.

2. **Confirm the drop of the SIM cards never activated?** I recommend confirming it; the panel agrees.
   - Problem: 12,262 rows have neither the intake flag nor an activation date. Only 0.34% of them used calls, SMS
     or data in 100 days (4 of the 35 July rows did), they come in batches of consecutive ids (3,662 runs against
     about 10,000 expected at random), and they held 8,515 of the 13,907 churners (61%). Their label says the SIM was
     never used, not that a customer left.
   - Effect if kept: a random split lets a model learn each batch's churn rate (ROC AUC 0.908 on all rows, 0.87-0.89
     with batches of consecutive ids held together), so the score rewards the batches, not churn prediction.
   - Implemented: dropped in every month; kept 54,207 rows with 9.9% churn, LightGBM 0.848. Cost: the churn rate falls
     from 20.9% to 9.9%, and the task becomes churn among activated accounts.
   - Alternatives: (a) drop only after June: 59,189 rows, 13.7% churn, 0.870; it keeps 4,982 June SIM cards of the
     same kind (churn 54.3%). (b) June only, `month` dropped: 57,656 rows, 0.872, with the same June SIM cards. (c)
     all rows: 66,469 rows, 0.908, inflated by the batches.
   - Rule: LEAK-22 (Must), USE-7. Precedent: follows california_house_prices_2020 and bias_correction; differs from
     expresso_churn_prediction_1m (which keeps its inactive customers) by a written fact: these rows carry no
     activation date and come in batches of ids, while every expresso row is a customer with a tenure.
   - Decision needed: confirm the drop in every month, or one of (a), (b), (c).

**Review panel:** don't ship under PROV-1 as written (mediator); ship after the changes only if the curator amends
PROV-1/PROV-2 to cover this case. Claim audit: most claims hold; 1 refuted (six columns with negative amounts are seven)
and 2 not reproduced (13.8%, and the 0.882 with batches held together), all fixed in the notes; 3 untested. Blind
review: include with changes; main concern the unknown provenance and churn definition. Source search: ended with no
upstream and no churn definition. Debate: agreed on the forced-IID tag, the potential-leak note and the wording fixes;
disputed: whether an untraceable upload with an undefined label can stay (issue 1). The mediator's issue 1 is issue 1
here, its issue 2 is issue 4, and its "not an issue" (the never-activated SIM cards) is issue 2. The roles' "REVIEW
issue 3" (small column choices such as keeping `month`) is not raised: it changes the ROC AUC by 0.0007, and the choices
are in the notes.

<details><summary>Mediator</summary>

**Mediator: mobile_churn (re-check, 2026-10-20)**

**Recommendation (judgment record)**

```text
Verdict: don't ship (No, Missing source information) under PROV-1 as written; ship after changes only if the curator
adopts a PROV-1/PROV-2 amendment that covers this case (issue 1).
Validity: SEL-1/SEL-2 hold; USE-1 holds (approximate fit); USE-5 cannot be checked against a source (part of issue 1);
USE-8 approximate, gap named, plus a `Potential leak, kept on purpose:` line; LEAK-10 holds (windows end at the
snapshot, 0 of 2,498 joiners); LEAK-22 applied (never-activated SIMs dropped); SPLIT-1 holds; SPLIT-8 triggered, fixed
(tag + sentence); PROV-3 holds (no generated-data flags, signs of a real system export); PROV-1 triggered, search
ended 2026-10-20 with no upstream (issue 1).
Value: TP holds (LightGBM 0.848, +0.049 over linear, SE 0.003; 1,797 minority rows per test fold).
Quality: CLEAN-10/CLEAN-11 notes; wording fixes (EV-1).
Weighed: shape +, signal +, realism +, source -, label definition -.
For the curator: issue 1, a standard question: amend PROV-1/PROV-2 once for the untraceable keeps, or apply No.
```

**Changes to make now (no decision needed)**

All of these are agreed by both sides. They become moot if issue 1 ends in `No`.

1. **SPLIT-8 (Must).**
   - Add `data_tags = ("ForcedIIDFromTemporal",)`.
   - Add one sentence to the IID bullet: the release has one stock month; the measured cost on the 1,533 later rows is 0.690 (IID) against 0.661 (trained on June), gap +0.028, CI [0.004, 0.056], and this gap mixes cohort with time; more months should be recovered.
   - Change the task_summary `split` sentence so it says the split stands for a random part of one month's base, not for next month.
2. **USE-8 / LEAK-24-25 (Must).**
   - Add a `Potential leak, kept on purpose:` line in the churn_telco_south_asia form: churn may itself be defined from the inactivity that the recency columns measure; revisit if the churn definition is found.
   - Have `fit_reason` name the undefined churn rule as well as the missing horizon.
3. **EV-1 and writing.md, wording fixes.**
   - Write "0.87-0.89 with batches of consecutive ids held together" in place of 0.882, which used a month x last-top-up-day key. This also applies to alternative D in REVIEW.md.
   - Replace 13.8% with the measured 10.0% or 12.7%, together with its definition.
   - Change "six" columns with negative amounts to "seven".
   - Limit the "over 99% no use" claim to June and August. In July, 4 of the 35 dropped rows (11.4%) used something.
4. **CLEAN-10 (Should).** Say in the notes that both default dates, 2010-01-01 and 2012-09-28, become missing, and that 2012-09-28 is unexplained. It covers 29-136 rows per column and its churn rates differ from the other default.
5. **CLEAN-11 (Should).** Add one note line: some missing inactive-days values are contradicted by the month's counts, under 0.4% of rows each. Keep the values.
6. **REVIEW.md, issue 1.**
   - Qualify the "small operator or MVNO" clue: the calls by destination add up to the total in only 10.8% of rows.
   - Replace the "budget ran out" caveat with the search's end (source_search.md: exact-string web searches, GitHub code search, Kaggle notebooks, the CTGAN-ENN paper, the OpenML 44228-44231 batch, none with an origin).

**Issues for the curator, ranked**

**Issue 1 (P3 + P5, Must: USE-5, PROV-1; PROV-2 Should). Keep a dataset with no traceable source and no churn definition?**

**The problem.**
- Every link ends at Kaggle `dimitaryanev/mobilechurndataxlsx` (2019-10-31): empty description, licence "Unknown", and no other datasets or notebooks by the owner.
- OpenML 44231 is a cell-for-cell copy of that upload.
- Neither page defines churn: no rule, no horizon, no operator.

**The effect.** We cannot tell whether the label means "deactivated by the operator" or "inactive N more days". The cited study finds that the churn definition moves prepaid churn predictability more than anything else in the setup.

**What the rules settle.**
- **PROV-1 is triggered.**
  - The search has ended, which settles the earlier "search not finished" dispute.
  - "An identifiable first uploader" does not apply: a handle with no description, and an unanswered provenance question, identify nothing about the data's origin. PROV-8 decides which source to cite, not whether the source is known (critic's point; it holds).
  - PROV-3 passing answers "is it real?", not "what is it?". Both sides concede this.
  - Nothing ranked above PROV-1 needs the keep. The real use case (P3) does not rescue a separate P5 failure (principles, step 4).
- **Precedents.**
  - The rule's own case, water_quality_and_potability, was rejected even though the data were judged sound. tour_travels_churn was kept on the same facts. That contradicts the rule, so it is flagged, not followed (rules win over precedents).
  - So by rank, the critic's side wins.
- **The curator's screening keep** ("data looking very good and real") was made knowing the source was missing; on this the advocate is right. But it departs from a Must without a fact that sets the case apart. That is consistency case 1, and the route it offers is an amendment, not an exception.
- **USE-8 versus USE-5.**
  - USE-8's text names "a label without a stated horizon" and "a potential leak kept on purpose". It does not name a label whose rule is unknown.
  - The data settle the parts that bear on P4: the label falls after the snapshot for both classes; it is not "inactive N days at the snapshot" (4.6% churn at 0-5 days, 61% at 60-75 days, no cutoff); and no single feature restates it (best 0.779 against 0.844).
  - What is left is USE-5's check against the source, which is the same gap as PROV-1. So this is not a separate failure. It is part of the amendment's wording.

**Each side's best evidence.**
- **Keep (advocate):**
  - every validity test that can be measured holds (LEAK-10, SPLIT-1, PROV-3, label timing);
  - tour_travels_churn was kept with no upstream (Lennart);
  - churn_telco_south_asia (CC 2026-10-15) kept an undated label with a note.
- **`No` (critic):**
  - the literal text of PROV-1 and water_quality_and_potability;
  - no earlier keep had both an unknown source and an undefined target (churn_telco_south_asia has two source papers);
  - this would be the fourth untraceable keep under a Must.

**Decision needed (a standard question, so it is yours).** Choose one:
- (a) Apply PROV-1: `No` with `Missing source information`.
- (b) Amend PROV-1/PROV-2 once for bank_customer_churn, tour_travels_churn, credit_card_customers and mobile_churn, and decide newspaper_churn the same way. The amendment proposed for credit_card_customers ("a named course or teaching platform counts as a known source when the data shows no PROV-3 marks") does not cover mobile_churn: it has no named platform. A wider wording would be needed, for example: "an untraceable first upload stays when the data passes PROV-3, the prediction point and label timing are measured on the data, and the gaps (source, label rule) are written as approximate fit with a potential-leak note". The amendment must also say whether an undefined label rule is allowed.
- (c) Reopen tour_travels_churn and the others to match water_quality_and_potability.

**What else could settle it.** One leftover gap is cheap to close: the Kaggle discussion page (one topic; it needs a logged-in browser). REVIEW.md already quotes it as the unanswered provenance question of 2021-12-27, so it is unlikely to change anything.

**Issue 2 (P4, SPLIT-8 Must, low effect). Does a release with a few cohort months count as "no dates at all"?**

Both sides applied the tag, consistent with expresso_churn_prediction_1m and account_debt_south_africa. Only the scope of SPLIT-8's wording is open. Confirm the tag, or amend SPLIT-8 to say so. The answer also affects the untagged churn siblings: bank_customer_churn, churn_telco_south_asia and tour_travels_churn.

**Not an issue: dropping the never-activated SIMs (REVIEW.md issue 2)**

Both sides agree. The precedent checker finds the drop consistent with california_house_prices_2020 and bias_correction (USE-7). It is set apart from expresso by a written fact: those rows carry no activation date and come in batches; 99.7% used nothing. It stays in REVIEW.md for confirmation only.

**Agreed facts**

- 66,469 raw rows; `user_account_id` is unique, so there are no repeated customers. The record months are June, July and August 2013.
- The 12,262 never-activated SIMs are dropped:
  - 0.34% used anything in 100 days;
  - they come in batches of consecutive ids (3,662 runs);
  - they held 61.2% of the churners.
- Kept: 54,207 rows with 9.9% churn.
- The 100-day windows end at the snapshot (0 of 2,498 joiners exceed it). Both classes share each month's snapshot date.
- Leak checks:
  - best single feature 0.779 against 0.844 for all features; dropping any one feature changes the score by at most 0.001;
  - 0.1% of test rows have an exact copy in train;
  - no hidden groups; consecutive-id grouping gives 0.847-0.849 against 0.848 for the shipped split.
- Split: IID is the only split the release supports. A split by month would leave 2.8% of rows, all new joiners, on the test side.
- The forced-IID cost is +0.028 (CI [0.004, 0.056]) on 1,533 rows, mixed with a cohort change.
- Task probes raise no flags; the generated-data probes raise no flags.
- The source search has ended with no upstream and no churn definition (source_search.md).
- Lesser findings, all agreed: the wording errors in change 3, the two default dates, and the contradicted values under 0.4%.

**Consistency with precedent**

- **PROV-1.** Recommending `No` follows water_quality_and_potability and the rule. A keep would match tour_travels_churn, which contradicts the rule, so it needs the amendment in issue 1, not an exception (a Must takes none). This is consistent with the credit_card_customers mediator, which also sent the PROV-1/PROV-2 amendment to the curator. Its wording does not cover this case.
- **USE-8 / LEAK.** The leak note follows churn_telco_south_asia (CC 2026-10-15). The shared snapshot date sets this case apart from churn_telco_europa (`No`).
- **SPLIT-8.** The tag follows account_debt_south_africa (CC 2026-10-12), expresso_churn_prediction_1m and credit_card_customers (both panel, 2026-10-20).
- **Never-activated drop.** It follows california_house_prices_2020 and bias_correction. It is set apart from expresso by a written fact (no activation date, batches).
- **Kept duplicates.** They follow LEAK-18, sepsis_survival_minimal_clinical_records and expresso.

</details>

<details><summary>Source search</summary>

**mobile_churn: PROV-1 source search (2026-10-20)**

**Result: no upstream source and no churn definition found. The search has ended.**

**What the links say**

- Kaggle `dimitaryanev/mobilechurndataxlsx` (Kaggle API `datasets/view`): title `mobile-churn-data.xlsx`, owner
  "DimitarYanev", one version ("Initial release", 2019-10-31), empty description and subtitle, licence "Unknown",
  usability 0.29, 1 discussion topic (not readable without a browser; JS page), no other datasets by this owner
  (`datasets/list?user=dimitaryanev` returns only this one), no public notebooks by this owner.
- OpenML 44231 (API `data/44231`): description "No description available", citation "unknown author", creator "UNK",
  `original_data_url` = the Kaggle page above. Uploaded 2022-10-05T19:35. The batch: 44228 Churn_Telco_Europa
  (Kaggle `raumonsa11/churn-telco-europa`), 44229 and 44230 (Kaggle competition `dsntelecomschurn2018`); none
  names a further origin. The uploader id is not exposed by the API. OpenML points back to Kaggle, so it is a copy.

**Searched, nothing upstream**

- Web, exact strings: `"user_no_outgoing_activity_in_days"`, `"mobile-churn-data.xlsx"`,
  `"user_account_id" "user_lifetime" "user_intake"`, `"calls_outgoing_to_onnet_inactive_days"` /
  `"last_100_calls_outgoing_to_abroad_duration"` / `"user_account_balance_last"`, the row count 66,469, the uploader
  name with Kaggle / Bulgaria, prepaid churn 2013 theses. Only unrelated pages.
- GitHub code search `user_no_outgoing_activity_in_days`: only downstream copies (TabSTAR annotation from OpenML
  44231, our own repo, OpenML tag caches, student churn projects) and one recruiting case:
  `MehmetAnil/Technical_Case/README_teknasyon.md` (2025, Teknasyon data-scientist case study) that hands out the same
  columns with its own one-line descriptions ("`user_no_outgoing_activity_in_days`: Number of consecutive days with no
  outgoing activity"), no churn definition and no origin. It postdates the 2019 upload, so it is a reuse, not a source.
- Kaggle notebooks on the dataset (kaggle CLI `kernels list --dataset`): kerneler starter (2019-10-31), sd2beatles
  (2019-11-13), ammiyacine and adilimadeddinehosni (2023). Their markdown cells call it "a public dataset of 66,469
  customers from an anonymous telecommunications company"; none names a source or defines churn.
- Paper using it: Adiputra and Wanchai, "CTGAN-ENN ...", Journal of Big Data 11:121 (2024). Sec. "Data description",
  p. 11: "This research uses six datasets that are published in the Kaggle platform, which are ... mobile dataset
  [24]"; ref. 24: "mobile-churn-data.xlsx | Kaggle. https://www.kaggle.com/datasets/dimitaryanev/mobilechurndataxlsx".
  Downstream user only (PROV-10/12), no origin or churn rule.

**Conclusion**

Every path ends at the anonymous 2019 Kaggle upload with no description, no traceable first publisher (the uploader
has no other datasets, notebooks or profile information tying the file to an operator, course or competition), no
paper, and no churn definition or window. Under PROV-1 the origin is unknown and the search is finished. Not checked:
the text of the single Kaggle discussion topic (page needs a browser); a curator with a logged-in browser could open
https://www.kaggle.com/datasets/dimitaryanev/mobilechurndataxlsx/discussion in one step to close that gap.

</details>

<details><summary>Claim audit</summary>

**mobile_churn: claim audit (2026-10-20)**

Data loaded through the definition's `_load_raw` and `_clean`; the OpenML 44231 parquet for the copy check. LightGBM default, 3-fold stratified, 2-3 repeats,
n_jobs=2. Licence and pretraining overlap are not evidence and were not weighed.

**Table**

| # | Claim (source) | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|
| 1-2 | Prepaid churn; monthly scoring use case (task_summary) | read data: prepaid fields (reloads, balance), month snapshots | holds (as far as the data show) | top-up columns, snapshot per month | USE-1 |
| 3 | 54,207 accounts each once (task_summary) | nunique id in kept | holds | 54,207 / 54,207; raw 66,469 distinct too | SPLIT-1 |
| 4, 37 | churn 9.9%, Yes 5,392 | count | holds | 5,392 / 54,207 | - |
| 5, 16, 60 | no definition / no paper | OpenML API: "No description", creator UNK | holds (absence) | api/v1/json/data/44231 | PROV-1 |
| 6 | data place churn after month end | churn rate by inactivity; snapshot shared | holds | June churn 4.6% at 0-5 days inactive rising to 61% at 60-75 and 71% with no activity on record | LEAK-22 |
| 7 | inputs known at the snapshot | inactive-days count back to the snapshot (default value constant per month, both classes) | holds where testable; month aggregates cannot be dated | decision table: one value per month (1276/1307/1338) | LEAK-1, USE-3 |
| 8, 26 | July/Aug rows = new joiners (527, 1,006) | user_intake share | holds | 1.0 and 1.0; June 0.022 | SPLIT |
| 9, 10, 23 | 12,262 dropped, 8,515 of 13,907 churners (61%) | count | holds | 61.2% | PROV-13 |
| 11 | their label only says "never used" | usage in 100 days | holds (inference) | 0.34% used anything overall | PROV-13 |
| 13 | 66,469 rows | count | holds | | - |
| 14 | OpenML 44231 identical, same order | downloaded parquet, compared all 66 columns | holds | 0 differing cells, ids in same order | PROV-4 |
| 15, 28 | June-Aug 2013; year constant | values | holds | month 6/7/8; year 2013 | - |
| 17 | prediction point end of month | default inactive-days values = 2010-01-01 + 1276/1307/1338 = 30 Jun/31 Jul/31 Aug | holds | | USE-6 |
| 18 | 52.6% of June churners active in 30 days were last active 0-5 days ago | count | holds | 0.5262 of 3,702 (stayers 0.872) | LEAK-22 |
| 19 | churn rate rises with inactivity, no cutoff | binned rate | holds, not strictly monotone | 0.046, 0.167, 0.250, 0.360, 0.415, 0.497, 0.611, 0.577 (75-92), 0.000 (92-100, n=5) | LEAK-22 |
| 20, 46 | both classes share the month's snapshot | crosstab of no-activity value by month and class | holds | one value per month, both classes present | LEAK-23 |
| 21 | never-activated = intake 0 and no activation date | definition | holds (definitional) | | - |
| 22 | provisioning batches of consecutive ids | runs of never-activated rows in id order | holds | 3,662 runs vs about 10,000 expected at random; longest run 987; 7,232 of 12,262 rows in runs of 10+ | PROV-13 |
| 24 | LightGBM 0.908 all rows, 0.882 batch-held | rerun | number 0.908 holds (0.909); 0.882 depends on the batch key | consecutive-id keys give 0.891 (gap 10), 0.888 (gap 100), 0.870 (gap 1000); 2026-10-07 key was month x last top-up day with all no-top-up SIMs of a month as one group, which that run's own issues.md calls a cohort shift for the 0.857 number. The text calls them "batches of consecutive ids" but the 0.882 was not computed on ids. The direction (random split inflates) holds | EV-1, writing |
| 25 | IID: distinct ids | | holds | | SPLIT-1 |
| 27 | split by month tests cohort, not time | churn by month in kept | holds | 0.097 / 0.169 / 0.202; July/Aug all joiners | SPLIT, USE-10 |
| 29 | id numbered in creation order | Spearman id vs activation date (real lifetimes) | holds approximately, not strictly | rho 0.79 | - |
| 30 | six per-destination inactive-days copies | equality | holds | 100% each | CLEAN |
| 31 | lifetime >= 15,856 counts from 1970; 15,856-15,947 | range | holds (raw); largest real 1,986, nothing between | kept max 15,946 | CLEAN |
| 32 | sentinel remains for 1,295 kept, all joined in month | count | holds | intake 1.0 | CLEAN |
| 33 | 13.8% of those 1,295 active before the day it counts to | recomputed: any real inactive-days value older than (snapshot - day counted to) | NOT REPRODUCED | 10.0% (strict >), 12.7% (>=), 2.4% using the most recent activity; the 2026-10-07 run has the comment but no computation. The decision (set to missing, not rebuild) stands for any nonzero share | EV-1, writing |
| 34 | >100 values: 2010-01-01 (1,271-1,338) or 2012-09-28 (270-337) | ranges | holds | no value in 101-269 | CLEAN |
| 35 | real max 92 June (100 for no-outgoing), 30 after | per month max in kept | holds | July/Aug max 10-30 | CLEAN |
| 36 | default dates would encode the snapshot | one value per month | holds (month is a feature anyway) | | LEAK |
| 38 | 57 features, all numeric | dtypes | holds | | CLEAN |
| 39 | user_spendings = sum of three | arithmetic | holds up to rounding | 41 rows differ, max 0.01 (checklist said 100%) | - |
| 40, 41 | 9 copies; 8 conflicting vectors | duplicated | holds | 9 extra copies; 8 vectors / 16 rows | LEAK-16 |
| 42 | negatives in SIX spending and top-up columns | count columns with <0 | REFUTED | seven: user_spendings 7, reloads_sum 55, sms_outgoing_spendings 2, sms_outgoing_to_offnet_spendings 2, sms_incoming_spendings 10, gprs_spendings 51, last_100_reloads_sum 37 (same in raw) | writing |
| 43, 51 | licence unknown | OpenML API "Unknown" | holds (not evidence for the verdict) | | EV-4 |
| 44, 50 | year 2019 = upload; data 2013 | | holds | | - |
| 45, 56 | never-activated used nothing in 100 days in >99% (0.2-0.5%) | share used | holds overall and for June/Aug; July differs | June 0.52%, Aug 0.17%, July 11.4% (4 of 35) | - |
| 47 | Kaggle upload 2019-10-31, one file | - | untested | no Kaggle CLI in env; metadata only | - |
| 48 | OpenML uploaded 2022-10-05 | API | holds | upload_date 2022-10-05 | - |
| 49 | sha256 | sha256sum | holds | ebc820fa...271a1 | - |
| 53-55 | ids unique, year constant | | holds | | - |
| 57 | never-activated churn 54% June, 80% Aug | | holds | 0.543, 0.800 (July 0.371, n=35) | - |
| 58 | churners' last activity bunches before snapshot | see 18 | holds, but stayers bunch more (0.872 vs 0.526 at 0-5 days) | | - |
| 59 | no overlap with SATO, DSN, Europa files | - | untested | those files not at hand; different schemas per the 2026-10-07 run | PROV-5 |
| 62 | activations start 2008-01-22 (2,929, then 1,725) | snapshot - lifetime | holds | | - |
| 63 | on-net 0.3, off-net 16.3, abroad 1.5 calls | means | holds on all raw rows | kept rows: 0.39 / 20.0 / 1.81 | - |
| 64 | alternatives: A 59,189 13.7% 0.870; C 57,656 0.872; all 0.908 | rerun | holds | A 0.8716, C 0.8737, all 0.9091 | - |
| 65 | month drop 0.8479 vs 0.8481 | rerun | holds | 0.8474 vs 0.8481 | - |
| 12, 52, 54, 61 | fit approximate; curator opinion; front matter; priority | not testable on data | n/a | | - |

**Unwritten claims attacked**

| Claim | Test | Result |
|---|---|---|
| No hidden group by activation day in kept rows | LightGBM grouped by activation day vs random | holds: 0.8488 vs 0.8481 |
| No copy across the split | exact copies 9 rows; probes 0.1% of test rows | holds |
| No feature defines the label | best single feature 0.779 vs 0.844 all (probe); inactivity bins non-deterministic (61% at 60-75 days) | holds as far as testable; churn window unknown (USE-5, cannot verify) |
| Target is the real-world target | no definition anywhere | untested (cannot be tested; issue 1) |

**Refuted / not reproduced, ranked**

1. Claim 24 (validity of the evidence for the drop, Should): the 0.882 batch-held AUC is attributed to "batches of
   consecutive ids" but was computed with a month x last-top-up-day key that lumps each month's no-top-up SIMs into one
   group. Consecutive-id keys give 0.870-0.891. Changes nothing in the decision (drop holds on the usage evidence:
   99.7% of the SIMs used nothing). Mildest remedy: write "0.88-0.89 with batches of consecutive ids held together".
2. Claim 33 (writing, Must for numbers in notes): 13.8% not reproduced (10.0% / 12.7% by the two readings). Decision
   unchanged. Remedy: replace with the measured share and its definition, or "about 10%".
3. Claim 42 (writing): "six" columns should read "seven". Remedy: text fix.
4. Minor precision: claim 39 holds to rounding (41 rows off by up to 0.01); claim 45/56 do not hold for July's 35
   never-activated rows (11.4% used something); claim 63 numbers are for all raw rows, not the kept ones.

Untested: 47 (Kaggle metadata, no CLI), 59 (sibling churn files not local), target definition (no source).

</details>

<details><summary>Column audit</summary>

**mobile_churn: column audit (re-check, 2026-10-20)**

Frame: rebuilt from the definition through `dataset_io.load(..., built=True)` (origin `rebuilt`), 54,207 rows x 58
columns (57 features + `churn`). Raw: `mobile-churn-data.xlsx`.

Prediction point (first `curation_comments` bullet): the end of the record month (30 June, 31 July or 31 August 2013).
There is no codebook: every meaning below comes from the column name and the data, so "meaning" is inferred and the
churn definition is unknown (USE-5, PROV-1; REVIEW issue 1).

**Decisive measurement: do the windows end at the snapshot?**

If a `last_100_*` or month window ran past the snapshot, it would include post-snapshot activity (LEAK-10). The
accounts that joined in their month (user_intake = 1, lifetime 0-30 days) have no history before the month, so a window
ending at the snapshot must give last_100 == month value:

| column pair | joiners with activity | l100 == month | l100 > month | l100 < month |
|---|---|---|---|---|
| last_100_calls_outgoing_duration / calls_outgoing_duration | 2,498 | 77.4% | 0.0% | 22.6% |
| last_100_sms_outgoing_count / sms_outgoing_count | 2,199 | 73.5% | 0.2% | 26.3% |
| last_100_reloads_sum / reloads_sum | 2,521 | 96.3% | 0.7% | 3.1% |
| last_100_gprs_usage / gprs_usage | 369 | 73.7% | 1.1% | 25.2% |

The 100-day window never holds more call minutes than the month for a new account: it ends at or slightly before the
snapshot, not after. For the stock accounts the ratio l100/month has median 3.0 (about 100/30 days). The
`last_100_reloads_count` exceeds `reloads_count` for 76.5% of joiners while the sums agree in 96.3%: the two counts use
different counting rules, not a later window. Inactive-days maxima are 92 in June and 30 in July and August, which also
places them at the snapshot. No feature is post-outcome as far as the data show (LEAK-10 holds).

**Column table**

Known = known at the prediction point. "class NA" = share missing among churners / stayers.

| column | meaning (inferred; no codebook) | known? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| month | record month (6, 7, 8); in the cleaned frame 7 and 8 hold only new joiners (527, 1,006; churn 0.169, 0.202 vs 0.097 in June) | yes | int64, 3 values; numeric is fine (ordinal) | fine; cohort marker, constant when one month is scored (REVIEW issue 3) | USE-6, CLEAN-14 |
| user_lifetime | days since activation, to the snapshot (max 1,986 = 2008-01-22 to 2013-07-01) | yes | float64; >=10,000 (1970-01-01 default) set to NaN: 1,295 rows, all user_intake = 1; 34 June rows with intake 0 and lifetime < 31 (unusual, kept) | fine | CLEAN-10, CLEAN-11 |
| user_intake | 1 = joined in the record month | yes | int64 0/1; 2,683 ones | fine | CLEAN-14 |
| user_no_outgoing_activity_in_days | days since the last outgoing call or SMS; equals min(call, SMS inactive days) in 97.8% | yes | float64; >100 set to NaN (707 rows; class NA 9.3% / 0.4%, the pre-snapshot "no activity on record" state; indicator AUC 0.544) | fine; see problem 3 | LEAK-10, CLEAN-10 |
| user_account_balance_last | prepaid balance at the month's end | yes (end-of-month balance) | float64, 0 to 1,775.71, no negatives; 0 in 4.6% (churn 0.279) | fine | |
| user_spendings | total spend in the month; = calls + SMS + GPRS spendings in 100% of rows | yes | float64; 7 negatives (-30.06 to -0.10), kept | fine (derived, not a copy) | CLEAN-5, CLEAN-11 |
| user_has_outgoing_calls | flag = calls_outgoing_count > 0 (exact in every row) | yes | int64 0/1 | fine (derived) | CLEAN-5 |
| user_has_outgoing_sms | flag = sms_outgoing_count > 0 (exact) | yes | int64 0/1 | fine (derived) | CLEAN-5 |
| user_use_gprs | flag = gprs_session_count > 0 (exact; 18 rows with usage > 0 and flag 0) | yes | int64 0/1 | fine | CLEAN-5 |
| user_does_reload | flag = reloads_count > 0 (exact) | yes | int64 0/1 | fine (derived) | CLEAN-5 |
| reloads_inactive_days | days since the last top-up | yes | float64; >100 to NaN (26.0%; class NA 57.9% / 22.5%; indicator AUC 0.677); 215 NaN rows have top-ups in the month; 51 exceed user_lifetime | fine; problems 3, 4 | CLEAN-10, CLEAN-11 |
| reloads_count | top-ups in the month | yes | int64 | fine | |
| reloads_sum | top-up amount in the month | yes | float64; 55 negatives (-17.24 to ...; churn 0.182), kept | fine; note count (problem 5) | CLEAN-11 |
| calls_outgoing_count | outgoing calls in the month; not the sum of the three destination counts (equal in 10.8%; residual median 10, min -147) | yes | int64 | fine | |
| calls_outgoing_spendings | spend on outgoing calls | yes | float64 | fine | |
| calls_outgoing_duration | minutes of outgoing calls | yes | float64 | fine | |
| calls_outgoing_spendings_max | largest single-call spend | yes | float64; never above the total | fine | |
| calls_outgoing_duration_max | longest call, minutes; capped at 60 (150 rows) | yes | float64 | fine (a source cap of a feature, not of the target) | |
| calls_outgoing_inactive_days | days since the last outgoing call | yes | float64; >100 to NaN (1.9%); 90 NaN rows have calls in the month; 73 June rows have calls in the month but > 30 days | fine; problem 4 | CLEAN-10, CLEAN-11 |
| calls_outgoing_to_onnet_count | calls to the same network | yes | int64 | fine | |
| calls_outgoing_to_onnet_spendings | spend, on-net calls | yes | float64 | fine | |
| calls_outgoing_to_onnet_duration | minutes, on-net calls | yes | float64 | fine | |
| calls_outgoing_to_offnet_count | calls to other networks | yes | int64 | fine | |
| calls_outgoing_to_offnet_spendings | spend, off-net | yes | float64 | fine | |
| calls_outgoing_to_offnet_duration | minutes, off-net | yes | float64 | fine | |
| calls_outgoing_to_abroad_count | calls abroad | yes | int64 | fine | |
| calls_outgoing_to_abroad_spendings | spend, abroad | yes | float64 | fine | |
| calls_outgoing_to_abroad_duration | minutes, abroad | yes | float64 | fine | |
| sms_outgoing_count | SMS sent in the month | yes | int64 | fine | |
| sms_outgoing_spendings | spend on SMS; destinations sum to it in 81.3% | yes | float64; 2 negatives; max 1,234.30 on 505 SMS whose destinations sum to 1.56 (unusual, kept) | fine | CLEAN-11 |
| sms_outgoing_spendings_max | largest single-SMS spend (22 values) | yes | float64; above the total in 2 rows (the negative-total rows) | fine | |
| sms_outgoing_inactive_days | days since the last SMS | yes | float64; >100 to NaN (15.7%; class NA 46.0% / 12.4%); 160 NaN rows sent SMS in the month | fine; problem 4 | CLEAN-10, CLEAN-11 |
| sms_outgoing_to_onnet_count | SMS on-net | yes | int64 | fine | |
| sms_outgoing_to_onnet_spendings | spend, SMS on-net | yes | float64 | fine | |
| sms_outgoing_to_offnet_count | SMS off-net | yes | int64 | fine | |
| sms_outgoing_to_offnet_spendings | spend, SMS off-net | yes | float64; 2 negatives (same rows as the total) | fine | CLEAN-11 |
| sms_outgoing_to_abroad_count | SMS abroad | yes | int64 | fine | |
| sms_outgoing_to_abroad_spendings | spend, SMS abroad | yes | float64 | fine | |
| sms_incoming_count | SMS received | yes | int64 | fine | |
| sms_incoming_spendings | charges on received SMS (non-zero in 3.7%) | yes | float64; 10 negatives (-3.70 to -1.85) | fine | CLEAN-11 |
| sms_incoming_from_abroad_count | SMS received from abroad | yes | int64 | fine | |
| sms_incoming_from_abroad_spendings | charges on them (18 values, 0 in 99.9%) | yes | float64 | fine | |
| gprs_session_count | data sessions | yes | int64 | fine | |
| gprs_usage | data volume (unit unknown) | yes | float64 | fine | |
| gprs_spendings | data spend | yes | float64; 51 negatives (-38.90 to ...) | fine | CLEAN-11 |
| gprs_inactive_days | days since the last data session | yes | float64; >100 to NaN (90.6%); 102 NaN rows had sessions in the month | fine; problem 4 | CLEAN-10 |
| last_100_reloads_count | top-ups in the 100 days to the snapshot | yes (window ends at the snapshot, table above) | int64; counts differ in rule from reloads_count | fine | LEAK-10 |
| last_100_reloads_sum | top-up amount, 100 days | yes | float64; 37 negatives | fine | CLEAN-11 |
| last_100_calls_outgoing_duration | call minutes, 100 days | yes | float64 | fine | LEAK-10 |
| last_100_calls_outgoing_to_onnet_duration | on-net minutes, 100 days | yes | float64 | fine | |
| last_100_calls_outgoing_to_offnet_duration | off-net minutes, 100 days | yes | float64 | fine | |
| last_100_calls_outgoing_to_abroad_duration | minutes abroad, 100 days | yes | float64 | fine | |
| last_100_sms_outgoing_count | SMS, 100 days | yes | int64 | fine | |
| last_100_sms_outgoing_to_onnet_count | SMS on-net, 100 days | yes | int64 | fine | |
| last_100_sms_outgoing_to_offnet_count | SMS off-net, 100 days | yes | int64 | fine | |
| last_100_sms_outgoing_to_abroad_count | SMS abroad, 100 days | yes | int64 | fine | |
| last_100_gprs_usage | data volume, 100 days | yes | float64 | fine | |
| churn (target) | churned after the record month; definition and horizon unknown | the label | 0/1 mapped to Yes / No, 9.9% Yes | question for the curator (REVIEW issue 1) | USE-5, LEAK-24, LEAK-25 |

Dropped columns: `year` (2013 everywhere; CLEAN-5, right), `user_account_id` (unique per row, numbered in creation
order, so it carries activation order that user_lifetime already holds; CLEAN-3, right), the six per-destination
inactive-days columns (equal to the call or SMS inactive days in every row; CLEAN-5, right).

Signs of generated data: none. user_spendings is an exact sum in every row, the flags match their counts in every row,
cents end in 0 or 5 more often (13.7%, 15.8% vs about 8.8% for other digits: tariff prices), and the frame carries the
inconsistencies of a real billing export (default dates, refunds, sentinels contradicted by counts). The generated
probes have no flags.

**Problems, ranked (principles.md)**

1. **P3/P4, question for the curator: the target is undefined (USE-5; LEAK-24, LEAK-25 untestable).** No source
   defines churn or its horizon. If churn means "no activity for N days after the month", the recency columns lead
   into the label, but they are known at the snapshot and their windows end there (measured above), so they are inputs
   (LEAK-37, USE-6), not a leak. Whether "No" mixes "stayed" with "not yet observed" cannot be checked. Remedy: none
   in the definition; it stays REVIEW issue 1.
2. **P4: no column leaks.** Windows end at the snapshot (joiners: last-100 call minutes above the month value in 0 of
   2,498). Class-dependent missingness in the inactive-days columns (user_no_outgoing NaN 9.3% of churners vs 0.4% of
   stayers) is the pre-snapshot "no activity on record" state; the strongest missing indicator alone gives AUC 0.677.
   Drop-one changes the score by at most 0.001. Verdict fine (LEAK-10 holds).
3. **P7, cleaning (CLEAN-10): two sentinels merged into one NaN.** Values > 100 encode two default dates: 2010-01-01
   ("no activity on record") and 2012-09-28 (meaning unknown; 275, 306, 337 in June, July, August). Their churn rates
   differ: user_no_outgoing 0.726 (678 rows) vs 0.345 (29); calls 0.594 (959) vs 0.304 (46); reloads 0.223 (13,974)
   vs 0.081 (136). The 2012 code covers 29 to 136 rows per column, so the loss is small. Mildest remedy: keep, add one
   clause to the inactive-days note that both defaults become missing and the 2012-09-28 one is unexplained.
4. **P7, data quality (CLEAN-11): sentinels contradicted by counts.** Inactive-days missing although the month shows
   the activity: calls 90, top-ups 215, SMS 160, data 102 rows; 73 June rows with calls in the month but calls inactive
   days > 30; inactive days longer than the lifetime in 5 to 51 rows; 34 June rows with intake 0 and lifetime < 31.
   These are unusual, not provably impossible, and under 0.4% of rows each. Remedy: keep, add a note.
5. **P7, notes (writing.md): "six" should read "seven" columns with negative amounts.** user_spendings 7,
   reloads_sum 55, sms_outgoing_spendings 2, sms_outgoing_to_offnet_spendings 2, sms_incoming_spendings 10,
   gprs_spendings 51, last_100_reloads_sum 37. Keeping them is right (refunds or corrections, CLEAN-11). Remedy: the text fix.
6. **P7, meaning (no rule broken): the destination columns do not add up to the totals.** Calls count equals on-net +
   off-net + abroad in 10.8% of rows (residual median 10, min -147); SMS in 57.1%. A fourth destination (service or
   fixed-line numbers) is likely. No action, but the REVIEW clue "on-net calls are rare: a small operator or an MVNO"
   rests on these columns and should say that the breakdown is partial.
7. **P3, small (REVIEW issue 3): month is a cohort marker** in the cleaned frame (7 and 8 = joiners only). Known at the
   snapshot and within 0.002 AUC; fine as kept.

Dtypes: all 57 features numeric, no object column (CLEAN-9 holds); the 0/1 flags and the 3-valued month as numeric
are acceptable under CLEAN-14.

</details>

<details><summary>Split audit</summary>

**mobile_churn: split audit (re-check, 2026-10-20)**

LightGBM 300 trees, lr 0.05, untuned, thread caps 2). Data: the
definition's container rebuilt through `dataset_io.load` (54,207 rows, 3 x 3 IID folds, 36,138 / 18,069), rows mapped
back to the raw `user_account_id` (all 54,207 matched).

**Verdict: right with notes**

A random split over accounts is the only split the release supports and it costs nothing measurable against id or
cohort grouping. But the use case is a monthly scoring stream, which is temporal in nature, and the definition ships it
as plain IID without saying so (no `ForcedIIDFromTemporal` tag, README `data_tags | IID`).

**Regime the use case implies**

`task_summary.use_case`: "At the end of each month, a mobile operator scores its activated prepaid accounts". The
entity is known (an existing account, USE-10), and a deployed model is refit on an earlier month's accounts whose churn
label has arrived, then scores this month's stock: a temporal task (SPLIT-1, SPLIT-6), with a gap of the (unknown)
churn horizon (SPLIT-10).

What the data allow: one stock snapshot only. June 52,674 rows (churn 9.7%, 2.2% joined in June); July 527 and August
1,006 rows, all `user_intake` = 1 (new joiners, churn 16.9% / 20.2%); `user_account_id` unique in the raw file (66,469
rows), so no account recurs across months. A temporal split would have one window whose test side is 2.8% of the
rows and only new joiners: below SPLIT-14 (3 windows), and a test of a cohort change rather than of time.

**Alternative splits run**

| Split | ROC AUC |
|---|---|
| Shipped IID, all rows (3 repeats) | 0.8480 / 0.8484 / 0.8473 |
| Shipped IID, scored on June rows | 0.850 |
| Shipped IID, scored on Jul+Aug new joiners (1,533 rows, 292 churners) | 0.690 / 0.697 / 0.689 |
| Shipped IID, scored on June joiners (1,150, 191 churners) | 0.638 / 0.633 / 0.629 |
| Train June -> test Jul+Aug | 0.661 (Jul 0.632, Aug 0.675; without `month` 0.661) |
| Train Jun+Jul -> test Aug | 0.675 |
| Paired bootstrap, IID minus month split on the same 1,533 rows | +0.028, 95% CI [0.004, 0.056] |
| Grouped by blocks of 200 / 1,000 / 5,000 consecutive account ids | 0.847-0.849 (one run 0.840) |
| Grouped by `user_lifetime` value (activation-day cohort per month) | 0.849 |
| June test rows: train with vs without the Jul/Aug rows | 0.8505 vs 0.8484 |

Reading: the month split costs about 0.03 on the new joiners, but those rows are hard under either split (0.63-0.69
against 0.85 for the stock) and the gap mixes cohort with time. It cannot be measured on the stock, which is the use
case's population. Training rows from a later month (Jul/Aug in train when June is tested, SPLIT-9) change June scores
by 0.002.

**Hidden groups and near copies**

Hidden-group probe: 14 candidates, no hits; near copies 0.7% of rows; exact copies across the split 0.1% (9 exact
duplicate rows, 8 conflicting). The account id runs in creation order (Spearman with `user_lifetime` -0.79) and block
churn rates are overdispersed (sd 0.050 for blocks of 1,000 against 0.0095 binomial), but tenure is a feature known for
every new row (SPLIT-4): grouping by id blocks leaves the AUC at 0.847-0.849. The provisioning batches that did carry
the label (0.908 vs 0.882) are the never-activated SIMs the definition already drops. No group id is needed (SPLIT-29,
SPLIT-30).

**Problems, ranked**

1. **P4, SPLIT-8 (Must, by analogy), SPLIT-1: temporal task shipped as plain IID without the forced-IID tag.**
   Evidence: monthly scoring use case; one stock snapshot (June), later months are 2.8% new joiners only; no window
   structure possible. Precedent: expresso_churn_prediction_1m (one-snapshot churn, tagged `ForcedIIDFromTemporal`,
   gap of the label delay named), distribution_transformers_at_cauca_department (dates present but too few windows,
   tagged by analogy). Mildest remedy: `data_tags = ("ForcedIIDFromTemporal",)` and one sentence in the IID bullet
   saying a deployed model trains on an earlier month's stock with a gap of the churn horizon, that the release has
   one stock month so this cannot be built, the measured cost on the only later rows (0.690 IID vs 0.661 trained on
   June, new joiners only, CI of the gap [0.004, 0.056]), and that further months of the stock should be recovered.
   No re-split. SPLIT-8 is worded for "no dates at all"; here a month exists but holds one snapshot of the stock, so
   the curator may want the pending amendment (working-copy REVIEW.md, "Rules from the NBA review") to cover it.
2. **P4, SPLIT-10 / LEAK-22 (cannot verify): label horizon unknown.** The gap a deployed model would need is the
   churn window, which the source does not state (REVIEW issue 1). New joiners' churn is higher in August (20.2%) than
   July (16.9%) or June joiners (16.6%), so the later months do not look censored by the export date; weak evidence.
   No remedy beyond the note.
3. **P7 note: `month` as a feature.** Under IID, `month` = 7/8 marks the new-joiner cohort; dropping it changes
   nothing (0.6614 with and without on the month split; 0.8479 vs 0.8481 in REVIEW issue 3). Keep or drop, no effect.

The notes' statement "a split by record month would test a change of cohort, not of time" holds (measured above).

</details>

<details><summary>Domain practitioner</summary>

**mobile_churn: domain practitioner (re-check, 2026-10-20)**

Actor: the retention / CVM analyst of a prepaid mobile operator who, at the end of each month, scores the active
prepaid base and hands the top-risk list to a retention campaign (bonus credit, tariff offer) (USE-1).

**Fit: approximate**

The inputs are exactly the monthly usage snapshot I would have at month end, but the label has no stated definition or
horizon, so I cannot tell whether it measures "will leave in the window I can still act on" or "has already gone
silent" (USE-8, USE-5). Agrees with the definition's `fit = "approximate"`; no well-defined alternative use case makes it
direct (USE-9).

**1. Inputs at the prediction point (USE-3, USE-6)**

- I have all 57 kept features at month end: tenure, balance, the month's calls/SMS/data/top-ups split by destination,
  the 100-day history and the recency (inactive-days) columns. These are standard CDR/billing aggregates in any
  operator's data warehouse. Nothing looks recorded after the snapshot; the checklist's leak probes back this (best
  single feature 0.779 vs 0.844 all; drop-one at most +0.001).
- Recency is not the label: churn rate rises smoothly with `user_no_outgoing_activity_in_days` (1-3 days 4.3%, 15-30
  days 31%, 61-100 days 59%), so churn is not "inactive >= N days at the snapshot".
- What I would always have and is missing: tariff/plan, device/handset, region or home cell, incoming call volume
  (only incoming SMS is present), customer-care contacts and complaints, number-portability requests, recharge channel,
  bonus/promotion history and responses to earlier campaigns, network quality (dropped calls). Their absence makes the
  task harder than mine, not different (minor gap).
- `month` (6/7/8) I would have, but in deployment it is constant within a scoring run; it only flags the new-joiner
  cohort here (REVIEW issue 3; harmless, 0.0002 AUC).

**2. Target (USE-5)**

- What I act on: "will this active subscriber stop using us within the next N days (commonly 30-90 days of
  inactivity, or the SIM's deactivation), while an offer can still reach them". The label here is a binary with no
  stated window, rule or definition of activity. Radosavljevik, van der Putten and Larsen show that the churn
  definition is the setup choice that moves prepaid churn predictability the most, more than the sample or extra
  features. So the unknown definition is the main gap, not a detail.
- The dropped never-activated SIMs (12,262 rows, 61% of the original churners) were correct to drop: I never run
  retention on a SIM nobody has used; their "churn" is a provisioning artefact (USE-7 spirit, PROV-13).
- I would want a probability (ranking for a campaign with a fixed budget/capacity), so ROC AUC on a 9.9% positive rate
  is a reasonable proxy; in practice I would read lift or precision in the top decile.

**3. Row and test data (USE-10, USE-11)**

- One row = one account at one month end = one scoring decision. Matches.
- But I score the same base every month (a known entity with history, USE-10's weighed factor). Here each account
  appears once: June is the full active base, July and August only the newly joined accounts (527, 1,006; churn 17%
  and 20% vs 9.7% in June). The test set is therefore "a random slice of one month's base", not "next month's base".
  Real use is a temporal step (train on months to t, score t+1); the data cannot support that because the stock
  accounts are not repeated after June. That is a second, smaller gap: a random split within one snapshot standing in
  for next-month scoring (USE-8 "one snapshot standing in for a forecast", as account_debt_south_africa).
- The mixed population (stock + two months of new joiners) is not one I score as such, but it is 2.8% of rows.

**4. Would I use the model?**

Yes, as a first-pass ranking: the features are the ones my own models use, and recency/balance/top-up decline are the
known strongest churn signals in prepaid. I would trust it more if I knew (a) the churn rule and window, (b) that the
label window starts after the snapshot for every row (the data suggest it: 52.6% of June churners active in 30 days were
last active 0-5 days before the snapshot, both classes share the snapshot date), and (c) that it holds on a later month.
I would distrust it for unknown operator/market (small on-net share suggests an MVNO or small operator) and because I
cannot check whether customers already silent for 60-100 days are retainable at all.

**Gaps, ranked by how much they change the task**

1. Churn definition and horizon unknown (USE-5, USE-8): could be anything from "30 more days of inactivity" to
   "deactivated by the operator"; changes what the model learns and whether it is actionable. Already REVIEW issue 1;
   with no source this cannot be repaired, only named (done in `fit_reason`).
2. Random split within one snapshot instead of next-month scoring of a recurring base (USE-10, USE-8): no remedy in
   this data (accounts not repeated); acceptable as named approximate.
3. Already-dormant accounts in the scored base (60-100 days silent, 535 rows; 707 with no outgoing activity on record):
   many operators exclude these or treat them as already churned before scoring. Small (2.3% of rows), keep.
4. Missing standard inputs (plan, device, care contacts, MNP, incoming calls): makes it harder, does not change it.
5. Unknown operator/market and licence (PROV): not a use-case gap, but limits how far an expert would generalise.

**What an expert would change**

- Nothing to fix in the data that the data allow. Keep the never-activated drop (REVIEW issue 2, implemented choice).
- Name the second gap in the definition text: the split stands for scoring a random part of one month's base, not the
  next month (the `split` sentence says "Random accounts" but not what that stands in for). Optional.
- Optionally consider dropping `month` (REVIEW issue 3): it is a cohort flag, not something that varies in deployment;
  0.0002 AUC either way, so a curator's call.
- If the source is ever found, take the churn rule and window from it and record them (USE-5).

</details>

<details><summary>Blind review</summary>

**Blind review: mobile_churn (OpenML 44231)**

**Verdict: include with changes** - a realistic prepaid-telecom churn task with real signal and no obvious leak, but its provenance is undocumented and the `month` mix probably hides repeated customers and a time shift that a random split ignores.

**Task**
A mobile operator scores prepaid subscribers each month from that month's usage (calls, SMS, GPRS, reloads, balance, rolling "last_100" windows) to choose who gets a retention offer. This is a real, common use. Its size is 54,207 x 57 features, with 10.0% positives (5,392 "Yes").

**Concerns (most serious first)**
1. **Provenance unknown.** On Kaggle (dimitaryanev/mobilechurndataxlsx, 2019) the description is empty and the license is "Unknown". The OpenML page says "No description available." There is no definition of churn: no horizon, no rule for prepaid inactivity, no operator or country. The values look real: heavy tails, refunds that show up as negative spendings (min -30.06), and plausible missingness (`gprs_inactive_days` is 90.6% NaN, matching non-users). Still, we cannot confirm what the target means or whether redistribution is allowed. *Change:* document what is known, and exclude the dataset if the license matters.
2. **`month` mixes cohorts and probably repeats customers.** month=6 has 52,674 rows (9.7% churn), month=7 has 527 (16.9%) and month=8 has 1,006 (20.2%). The original xlsx most likely had a user id and year, which were dropped. The same subscriber could appear in months 6, 7 and 8 with overlapping "last_100" windows, so a random split could put that person in both train and test. I could not verify this without an id. *Change:* keep only month 6, or split by time (train on 6, test on 7 and 8), and drop `month`. Either way, check the source xlsx for an id.
3. **Duplicates.** 17 rows have identical features (9 of them also have the same label). This is minor. *Change:* dedupe.
4. **Signal is fine.** LightGBM 3-fold AUC is 0.85. The best single feature has AUC about 0.78 (recent call and spend activity). No feature looks like the target restated, and the task is not trivial.
5. **Preparation is fine.** Every column is numeric, the binaries are 0/1 ints, and NaN means "never active". The target is a category No/Yes.

**Not checked**
The original xlsx columns (id or year), the churn definition, the operator, and whether rows are customer-month repeats.

</details>

<details><summary>Precedent check</summary>

**Precedents: mobile_churn (re-check, 2026-10-20)**

**Inputs:** the run's precedent register (4 flags, none involving mobile_churn), the REVIEW.md before this run, the checklist, the record and the definition, the Cases tables of the knowledge files, today's precedent checks of credit_card_customers and expresso_churn_prediction, and the sibling churn records and every record marked `Missing source information` with a suggestion other than No.

**Where the curator's call comes from.** The only curator text on mobile_churn is the screening comment: "Another case of missing data but data looking very good and real." It is undated; the line was in the record when it was imported on 2026-06-23 (commit 391cf7a).
- It comes before the 2026-10-07 assessment, which found that the churn definition is undocumented too.
- So under "a later stage's measured finding supersedes an earlier stage's reading", it is a screening-era keep, not a decision taken with the evidence in view. This is the same situation as credit_card_customers (D2 of that report).

**D1. Issue 1: keeping a dataset whose source and churn definition are unknown (PROV-1 Must, PROV-2 Should, USE-5 Must)**

**The rule.**
- PROV-1 (Must): when every link ends at an anonymous re-upload with no traceable upstream, the result is `Missing source information`, `No`. It adds that "only the end of a search counts".
- PROV-2 narrows it: a source that is plausible but unclear only in a detail stays, with a note.

**Precedents that exclude:**

| Dataset | Date, who | Facts | Outcome |
|---|---|---|---|
| water_quality_and_potability | undated, workbook (Lennart, Andrej) | Lennart: "Enough info about data to see the features are invariant ... But still unclear source" | No, the PROV-1 case |
| 3d_estimation_using_rssi_..._1_target, calendardow | undated | no source found after a search | No, PROV-1 cases |
| sunborn_customer_churn | undated | churn data, no source, "looks super fake" | No + AHDS |
| ecommerce_shipping, customer_satisfaction_in_airline | 2026-10-01, Lennart | untraceable source plus generated columns | No (Retired), AHDS + Missing source information |

**Precedents that keep:**

| Dataset | Date, who | Facts |
|---|---|---|
| bank_customer_churn | workbook era; licence CC 2026-10-14 | names an upstream (the SuperDataScience course): "Given the heavy usage ... we keep the data source as is" |
| tour_travels_churn | undated, Lennart | no upstream: "We are missing some information, but it seems reasonable". Shipped (DF: Yes) |
| credit_card_customers | screening, undated | names an upstream (Analyttica LEAPS case 11). Still open, with today's report |
| bad_customer_detection | PROV-2 case, 2026-10-14 | "a plausible source unclear in a detail" |
| newspaper_churn | undated, screening | "Data looks real and good, but we have no source information. Unclear if we want to use it." TBD -> Yes, not added |

**Comparison.**
- **Closest pair decided the other way: water_quality_and_potability.** The curator also judged that data sound and still rejected it on the source alone. The facts that differ in mobile_churn favour keeping it:
  - it looks like a real system export (sentinel dates of 1970-01-01, 2010-01-01 and 2012-09-28, SIM provisioning batches of consecutive ids, refunds);
  - the generated-data probes raise no flags;
  - it has no copy or duplicate problem.

  These facts answer PROV-3 (is the data real?), not PROV-1 (can we tell what it is?). Neither the operator nor the churn definition is known, so USE-5 ("check how the source built the label") cannot be met either.
- **Closest keeps.** tour_travels_churn has no upstream at all, like mobile_churn. bank_customer_churn and credit_card_customers name an upstream; mobile_churn names none.
  - The amendment proposed in today's credit_card_customers report ("a named teaching or course platform with no PROV-3 marks counts as a known source") would not cover mobile_churn.
  - Keeping mobile_churn needs a wider amendment.
- **No precedent has both gaps: unknown source and undefined target.** churn_telco_south_asia (CC 2026-10-15, Lennart) kept an undated churn label, but its source is two papers. mobile_churn would be the first keep with neither a source nor a label definition.
- **The search is not finished.** The REVIEW's caveat says the WebSearch budget ran out and a Google search for `"user_no_outgoing_activity_in_days"` or `"mobile-churn-data.xlsx"` is still to run. PROV-1 says "only the end of a search counts", and EV-1 says facts come first. So neither the keep nor the `No` is final yet.
  - One more lead, not tested (my inference): OpenML 44228-44231 were uploaded together on 2022-10-05 and are all telco churn sets (44228 churn_telco_europa, 44229/44230 DSN, 44231 this file). Whoever assembled that batch may cite an origin.
- **Drift.** I cannot measure it. Every PROV-1 keep and every source-only exclusion by Lennart is undated or from the workbook era. All the dated exclusions (2026-10-01) also had generated-data marks. The de facto pattern, "untraceable plus generated is No; untraceable plus real-looking is kept", is not what PROV-1 says. A precedent that contradicts a rule is flagged, not followed (principles.md).
- **Third exception of the same kind.** This would be the fourth keep (bank_customer_churn, tour_travels_churn, credit_card_customers, mobile_churn). PROV-1 is a Must, so these cannot be recorded as exceptions; an amendment is due (principles.md, "Exceptions and amendments").

**Verdict.**
- Departs from PROV-1 without a stated fact.
- Not reasonable under the ranking as an exception: PROV-1 is a Must, and nothing ranked above it calls for the keep.
- The legitimate routes:
  - finish the search;
  - or amend PROV-1/PROV-2 on purpose;
  - or apply the rule (`No`).

```text
**Consistency check (AI, 2026-10-20):** your call on mobile_churn (keep, a departure from PROV-1) matches
tour_travels_churn (kept, no upstream) but differs from water_quality_and_potability (No, PROV-1 case: the data
judged sound, the source unclear). It would be the fourth keep of an untraceable dataset under a Must, and the
first with an undefined target (USE-5). What sets it apart?
(a) the first Kaggle upload is the earliest publication found and the data carry system-export artefacts (sentinel
dates, provisioning batches, refunds) that pass PROV-3. Since PROV-1 is a Must, record this as an amendment
("an untraceable source stays when the data pass PROV-3 and the gap is written down"), after the unfinished search
(Google for the column names; the OpenML 44228-44231 uploader) has ended; (b) treat it like
water_quality_and_potability: No + Missing source information; (c) reopen tour_travels_churn (and
bank_customer_churn, credit_card_customers) to match water_quality_and_potability; (d) change the rule: amend
PROV-1/PROV-2 once for all four cases, saying whether an undefined target is still allowed.
```

**D2. Issue 2: never-activated SIM cards dropped in every month (USE-1, USE-5, USE-7; PROV-13; LEAK-18)**

**What is implemented.** 12,262 rows with `user_intake` = 0 and no activation date are dropped. Their churn rate is 69.4%, and they hold 8,515 of the 13,907 churners. This decision is the AI's and is still open for the curator.

**Precedents that follow.** Dropping rows that are not instances of the use case:
- california_house_prices_2020 (CC 2026-10-14, Lennart): dropped 2,480 listings that describe an earlier sale.
- bias_correction_r_bias_correction_r_2 (USE-7, 2026-10-15, Lennart): dropped days without the forecast the task corrects.
- cirrhosis_patient_survival_prediction (USE-5 case): narrowed the population to the target the actor acts on.

**A sibling that looks opposite but is set apart.** expresso_churn_prediction_1m (panel 2026-10-20, AI, applied) keeps inactive customers and their copies, because dropping them would turn an 18.75% churn task into a 5.9% "active customers" one. mobile_churn shrinks its churn rate in the same way (20.9% to 9.9%). The written fact that sets it apart:
- Expresso's rows are customers: every row has a tenure band, none under 3 months.
- mobile_churn's dropped rows have no activation date, no intake flag, at most 0.2-0.5% usage, and come in provisioning batches.
- Under a random split those batches also act as hidden groups: LightGBM 0.908 on all rows against 0.882 with batches held together (SPLIT/LEAK hidden-groups reasoning).

**Weighed factor.** cleaning_features.md "Rows that are a sentinel in every feature" (real population or empty records). Its heloc case (588 rows of -9) is still undecided (AI, 2026-10-19), so it gives no precedent in either direction.

**The kept duplicates.** 9 exact copies and 8 feature vectors that occur with both labels stay. This is consistent with LEAK-18 and with sepsis_survival_minimal_clinical_records (CC 2026-10-06, Lennart) and expresso. Alternative A would bring back 4,021 copies and 235 vectors with both labels.

**Verdict.** Consistent, with the reason stated in the definition (the decision table). No prompt.

**D3. Issue 3: small column choices**

| Choice | Rule | Precedent | Verdict |
|---|---|---|---|
| `user_account_id` dropped | CLEAN-3 | TabSTAR drops it too; its creation-order meaning is already in `user_lifetime` and the batches are dropped (D2) | consistent |
| `year` (constant) and the six per-destination inactive-days copies dropped | CLEAN-5 | ordinary cleaning | consistent |
| Default-date day counts set to missing | CLEAN-10 / CLEAN-11 | sdss_17 (-9999), heart_disease_va_long_beach (chol 0), churn_telco_south_asia (negative network age) | consistent |
| Negative amounts kept | CLEAN-11 ("values only unusual stay") | churn_telco_south_asia kept its other anomalies (CC 2026-10-15) | consistent; but the note says "six" columns and the data have seven (checklist): a writing fix |
| `month` kept as a feature | CLEAN-22 (columns leave for what they are) | no direct precedent; 0.8479 against 0.8481 | consistent with the rule |
| `year = "2019"`, `source = "Kaggle"` | PROV-9, PROV-8 ("Kaggle is the source only when ... no other source can be found", Lennart 2026-10-12) | same as tour_travels_churn and bank_customer_churn | consistent |

**D4. The undefined churn window (USE-3, USE-8, LEAK-22 to LEAK-26)**

**Precedents:**
- churn_telco_south_asia (CC 2026-10-15, Lennart): churn undated, kept, fit `approximate`. A `Potential leak, kept on purpose:` line states the risk and a condition to revisit it.
- credit_card_customers: the same treatment for its window that may end at the closure.
- iranian_churn (CC 2026-10-01): retired, because the source states the window ends at the churn.

**Comparison.** mobile_churn follows churn_telco_south_asia in substance (kept, fit `approximate`), and has more evidence than south_asia had:
- the label is measured after the snapshot for both classes;
- both classes share the snapshot date, which sets it apart from churn_telco_europa (No, 2026-10-12);
- the churn rate rises with the days of inactivity with no cutoff.

One difference in form, not a departure: its notes lack a `Potential leak, kept on purpose:` line for the remaining risk that churn is itself defined from inactivity (the checklist says this cannot be verified). Both siblings carry such a line.

**Verdict.** Consistent. Optionally, add the line, in the form churn_telco_south_asia uses, with "revisit if the churn definition is found".

**D5. The IID split with no `ForcedIIDFromTemporal` tag (SPLIT-7, SPLIT-8)**

**Precedents:**
- account_debt_south_africa (CC 2026-10-12, Lennart; the SPLIT-8 case): one extract of a task that is temporal in nature, shipped as IID with the tag.
- expresso_churn_prediction_1m (panel 2026-10-20, applied; not yet confirmed by the curator): a churn snapshot shipped as IID with the tag. Its reason: a deployed model trains on an earlier window.

**The untagged churn siblings.** bank_customer_churn, churn_telco_south_asia and tour_travels_churn carry no tag. None of them was reviewed under SPLIT-8 after it was written.

**This case.**
- The definition explains why no split by month was made: the July and August rows are new joiners, so such a split would test a change of cohort.
- It does not explain why the tag is absent. The 52,674 June rows are one snapshot of the customer base, and the operator's monthly scoring is temporal in nature.
- SPLIT-8 is written for releases with "no dates at all". mobile_churn has record months, which could be a fact that sets it apart; nobody has stated it.

**Verdict.** Departs from expresso and account_debt_south_africa without a stated reason. It is a real pair of similar cases decided differently, but low in effect: a tag, not a split change.

```text
**Consistency check (AI, 2026-10-20):** mobile_churn ships IID without `ForcedIIDFromTemporal`, unlike
account_debt_south_africa (tagged, 2026-10-12, SPLIT-8 case) and expresso_churn_prediction_1m (tagged, 2026-10-20):
the same mechanism, one snapshot of a customer base scored monthly. What sets it apart?
(a) the release has record months, so SPLIT-8's "no dates at all" does not apply, and a split by month would test a
cohort change (June stock against July/August joiners), recorded in the notes as the reason for no tag; (b) treat it
like expresso: add the tag and say what a second snapshot month would change; (c) reopen expresso to match
(untag it); (d) amend SPLIT-8 to say whether a release with a few cohort months counts as "no dates".
```

**Amendments due**

1. **PROV-1/PROV-2.** mobile_churn would be the fourth keep of an untraceable source. It has no named upstream and an undefined target, so the narrower amendment proposed for credit_card_customers would not cover it. Settle the wording once for bank_customer_churn, tour_travels_churn, credit_card_customers and mobile_churn, and decide newspaper_churn the same way.
2. **SPLIT-8 scope.** Say whether a single-snapshot customer base with a few record months counts as having "no dates" (D5). This also affects the untagged churn siblings.

</details>

<details><summary>Advocate</summary>

**mobile_churn: advocate's opening brief (ship as defined), 2026-10-20**

Evidence: the panel's reports (claim_audit, column_audit, split_audit, practitioner, blind_review, precedents, checklist). Definition: `datasets/_dev/tabarena-v0pt2/mobile_churn/dataset.py`.

**1. The evaluation is honest: no column leaks, and the label comes after the snapshot (P4; LEAK-10 Must, LEAK-16 to LEAK-21, SPLIT-29)**

- **Claim:** every kept feature is known at the prediction point, which is the end of the record month, and nothing crosses the split.
- **The windows end at the snapshot.** The column audit's decisive test looked at the accounts that joined in their month, which have no earlier history.
  - Their `last_100_calls_outgoing_duration` exceeds the month value in 0 of 2,498 accounts.
  - SMS, top-ups and data exceed it in 0.2%, 0.7% and 1.1%.
  - So the 100-day windows end at or before the snapshot.
- **Both classes share the snapshot date.** The "no activity" value is one per month (1276, 1307 and 1338 days after 2010-01-01, which is 30 June, 31 July and 31 August). Both classes appear at each value. This is the claim audit's crosscheck (claims 20 and 46), and it is what sets this case apart from churn_telco_europa (`No`).
- **No single feature restates the label.**
  - Best single feature 0.779 against 0.844 for all features.
  - Removing any one feature changes the score by at most 0.001.
  - A depth-3 tree reaches 0.804.
- **The label is not "inactive N days at the snapshot".** The churn rate climbs gradually with inactivity: 4.6% at 0-5 days, 61% at 60-75 days. There is no cutoff.
- **Copies and groups:**
  - 0.1% of test rows have an exact copy in train.
  - The hidden-group probe found nothing among 14 candidates.
  - Grouping by blocks of consecutive ids gives 0.847-0.849 against 0.848 for the shipped split.
- **The blind reviewer's "repeated customers" worry is refuted on the data.** `user_account_id` is unique across all 66,469 raw rows (claim audit, claims 3 and 25).
- **Why it outranks the objection:** P4 is the highest-ranked rule the dataset could fail on the data itself, and it holds by measurement (EV-2: a measurement on the data beats a page).

**2. The use case is real, and its one gap is named the way the rules prescribe (P3; USE-1 Must, USE-8 Must, USE-5 Must)**

- **Claim:** at month end, an operator ranks its prepaid base for retention offers. The domain practitioner, acting as that analyst, says the inputs are "exactly the monthly usage snapshot I would have at month end". Asked whether they would use the model: "Yes, as a first-pass ranking".
- **The blind reviewer** (no notes) calls it "a realistic prepaid-telecom churn task with real signal and no obvious leak" and would include it.
- **The objection is USE-5:** the source never defines churn.
- **Why it does not exclude the dataset:**
  - USE-8 lists "a label without a stated horizon" as a standard case of an approximate fit. The definition already writes that gap into `fit_reason`.
  - The Tensions table keeps a real task over an imperfection when the imperfection is written down.
  - Precedent churn_telco_south_asia (CC, Lennart, 2026-10-15) kept an undated churn label with fit approximate. The precedent checker finds mobile_churn has more evidence for the label's timing than that dataset had.
  - USE-5 asks to redefine a badly built target when that is possible. Here nothing contradicts the label: the data place it after the snapshot (point 1).
- **Mildest remedy (I concede it):** add a `Potential leak, kept on purpose:` line for the one untestable risk, that churn is itself defined from later inactivity. Add "revisit if the churn definition is found", in the form churn_telco_south_asia uses. This is a note, not a change to the data.

**3. Dropping the never-activated SIMs repairs real damage and should stay (P5; PROV-13 Must; LEAK-22 Must)**

- **Claim:** the 12,262 rows with no intake flag and no activation date are not customers.
  - Only 0.34% used minutes, SMS or data in 100 days.
  - They come in provisioning batches: 3,662 runs of consecutive ids against about 10,000 expected at random, and 7,232 rows sit in runs of 10 or more.
  - They held 61.2% of all churners.
- **What keeping them would do:** a random split would learn each batch's churn rate. All rows give 0.909, against 0.870-0.891 with consecutive-id batches held together (claim audit).
- **Support:**
  - LEAK-22 (follow the cohort that can have the outcome).
  - The practitioner: "I never run retention on a SIM nobody has used."
  - The precedent checker judges the drop consistent with california_house_prices_2020 and bias_correction (USE-7), and finds it set apart from expresso by a written fact: Expresso's rows all carry a tenure, these have none.
- **Concessions:**
  - The 0.882 figure was computed with a month x last-top-up-day key, not with consecutive ids. Fix: write "0.87-0.89 with batches of consecutive ids held together".
  - July's 35 dropped rows used something in 11.4% of cases (4 rows). Say "June and August" for the over-99% claim.
- **Why this outranks the alternative of keeping them:** both fixes are wording only. The usage evidence decides the drop, and the AUC gap only confirms it.

**4. The task is worth benchmarking (P6; TP-1 to TP-10)**

- **Evidence:**
  - Task probes raise no flags.
  - LightGBM ROC AUC 0.848; the gap to a linear model is +0.049 (SE 0.003).
  - The smallest class has 1,797 rows in a test fold.
  - 54,207 rows and 57 numeric features.
  - Not trivial (best single feature 0.779) and not hopeless.
- **Answers:** nobody on the panel raised a value objection. It also fills the "Larger IID Data" tag the record carries.

**5. IID is the only split this release supports; the missing tag is a one-line fix (P4; SPLIT-1, SPLIT-8 Must, SPLIT-14, USE-10)**

- **Claim:** a random split over accounts is right.
  - Accounts never recur: all ids are unique.
  - A split by month would have one window whose test side is 2.8% of the rows, all new joiners. That is below SPLIT-14's three windows, and it tests a change of cohort, not of time.
  - The split audit's verdict is "right with notes".
  - Training on June and testing on July and August gives 0.661, against 0.690 under IID on the same 1,533 rows. But those rows are hard under either split, and the gap mixes cohort with time.
- **Concession:** the use case is monthly scoring, so the task is temporal in nature. account_debt_south_africa (SPLIT-8 case, Lennart) and expresso_churn_prediction_1m carry `ForcedIIDFromTemporal`.
- **Mildest remedy, no re-split:**
  - set `data_tags = ("ForcedIIDFromTemporal",)`;
  - add one sentence: the release has one stock month; the measured cost on the later rows is 0.690 vs 0.661; more months should be recovered.
- **Why that is enough:** the remedy ladder. A tag and a sentence settle the departure, and the split itself stays because it follows what the data can support (SPLIT-4 tension: "the right split against the score").

**6. The source: PROV-1 cannot yet exclude this dataset, and the facts weigh towards the keep the curator already made (P5; PROV-1 Must, PROV-2 Should, PROV-3 Must, PROV-8 Must)**

- **Concession:**
  - No paper, operator or competition has been found.
  - PROV-1 is a Must.
  - The closest exclusion, water_quality_and_potability, was also judged sound data and still rejected.
  - No earlier keep had both an unknown source and an undefined target.
- **Three facts that hold:**
  1. **The search has not ended.** PROV-1 says "only the end of a search counts". The REVIEW's own caveat says the WebSearch budget ran out before a Google search for `"user_no_outgoing_activity_in_days"` or `"mobile-churn-data.xlsx"`. The precedent checker adds the untested lead of the OpenML 44228-44231 batch uploader. So a `No` under PROV-1 is not yet available either (EV-1: facts first).
  2. **PROV-1's own list counts "an identifiable first uploader" as a traceable upstream, and PROV-8 makes Kaggle the source "when the data first appeared there".**
     - The 2019-10-31 Kaggle upload is the earliest publication found.
     - OpenML 44231 is a cell-for-cell copy of it: 0 differing cells, same order.
     - Whether a named Kaggle account counts as "identifiable" is arguable. I do not claim it settles the point.
  3. **What PROV-1 protects, "so we can tell what it is", is largely established by measurement.**
     - The snapshot dates, the prediction point and the window ends are all measured.
     - The data carry a real billing export's artefacts: sentinel dates 1970-01-01, 2010-01-01 and 2012-09-28; provisioning batches; refunds; tariff-price cent endings.
     - The generated-data probes raise no flags.
     - PROV-3 (Must) passes.
- **The curator's decision:** the curator kept it, writing "data looking very good and real". A curator's decision outranks an AI assessment. The later finding (no churn definition) adds a USE-5 gap, already handled in point 2. It does not change the source facts the curator saw.
- **Precedent:** tour_travels_churn was shipped with no upstream at all (Lennart).
- **Remedy:** keep the dataset with the `Missing source information` marker and the written gap, and finish the search.
  - If the search ends with nothing, the curator either amends PROV-1/PROV-2 once for the four cases (bank_customer_churn, tour_travels_churn, credit_card_customers, mobile_churn), as the precedent checker proposes, or takes the `No`.
  - That is a curator's call, not something the panel can settle by rank.
- **What I do not claim:** "independent failures are not conflicts" applies. Nothing ranked above PROV-1 rescues it. My case is that the rule has not been triggered to its end yet.

**7. The cleaning is the expert state; the errors found are in the notes, not the data (P7; CLEAN-3, CLEAN-5, CLEAN-10, CLEAN-11, CLEAN-22; LEAK-18; EV-4)**

- **Evidence:**
  - Each dropped column is right: a constant year, the creation-order id, and six exact copies.
  - The default-date sentinels become missing with a clean cut: no values between 101 and 269.
  - The refunds stay as published (CLEAN-11).
  - The 9 duplicate rows and 8 conflicting feature vectors stay (LEAK-18; consistent with sepsis and expresso).
  - `month` changes AUC by 0.0007 and stays (CLEAN-22).
  - The licence is never evidence (EV-4), which answers the blind reviewer's licence concern.
- **Concessions, all text fixes (writing.md):**
  - "six" columns with negative amounts should read "seven";
  - 13.8% should be the measured 10.0% or 12.7%, with its definition;
  - the 0.882 key (point 3);
  - one clause saying the unexplained 2012-09-28 default also becomes missing;
  - a note on the sentinels contradicted by counts, under 0.4% of rows each;
  - say that the destination breakdown is partial behind the "MVNO" clue.
- **Why they do not block shipping:** these are P7 quality items, fixed cheaply in the notes. None changes a number in the data or a decision.

**Judgment record (advocate's view)**

```text
Verdict: ship after changes (text and tag only), with the source as the curator's call.
Validity: SEL-1/SEL-2 hold; USE-1 holds (approximate, gap named, USE-8); USE-5 cannot verify, add the
`Potential leak, kept on purpose:` line; LEAK-10 holds (windows end at the snapshot); LEAK-22 applied (never-activated
SIMs dropped); SPLIT-1 holds, SPLIT-8 tag to add; PROV-3 holds; PROV-1 open until the search ends (issue 1).
Value: TP holds (0.848, spread +0.049, 1,797 per test fold).
Quality: notes fixes (six to seven, 13.8%, 0.882 key, 2012-09-28 default).
Weighed: shape +, signal +, realism +, source -, label definition -.
For the curator: issue 1, finish the search, then amend PROV-1/PROV-2 for the four keeps or apply No.
```

</details>

<details><summary>Critic</summary>

**mobile_churn: critic, opening brief (2026-10-20)**

Position: **do not ship yet.** Finish the source search first. If it ends without an upstream, the rules say `No`
(`Missing source information`), unless the curator amends PROV-1 on purpose. If it ships, make the changes in
points 3 to 6 first. Points are in rank order. Points 1 to 3 are validity Musts; points 4 to 6 are procedure and
quality issues, and none of them is a reason to exclude.

**1. The label is undefined and cannot be checked against its source (P3, USE-5 Must)**

- **Problem.** USE-5 says to "check how the source built its label before accepting it". Here that check is
  impossible: there is no definition, no horizon, no activity rule and no operator. Kaggle has an empty description,
  OpenML says "No description available", creator "UNK", and the one discussion thread asking for provenance is
  unanswered (claim_audit 5, 16, 60; REVIEW_before issue 1).
- **Effect on the task.** The practitioner calls this "the main gap, not a detail". The label could mean anything from
  "30 more days of inactivity" to "deactivated by the operator". The cited study (Radosavljevik, van der Putten and
  Larsen) finds that the churn definition moves prepaid churn predictability more than anything else in the setup.
  The data narrow it down only partly:
  - Holds: the label falls after the snapshot for both classes (claim_audit 17-20).
  - Untestable: whether churn is itself defined from inactivity, and whether "No" mixes "stayed" with "not yet
    observed" (column_audit problem 1; checklist P3/P4 "cannot verify").
- **Precedent.** No kept dataset lacks both a source and a label definition (precedents D1). churn_telco_south_asia
  kept an undated label, but it has two source papers.
- **Remedy (mildest).** USE-8's "label without a stated horizon" covers the missing window, so on its own this is
  approximate fit, not exclusion. It does not cover a label whose meaning is unknown, so it depends on point 2:
  - (a) If the search in point 2 finds the source, take the churn rule and window from it.
  - (b) Otherwise add a `Potential leak, kept on purpose:` line, in the form churn_telco_south_asia uses: churn may be
    defined from the inactivity that the recency columns measure; revisit if the definition is found. Both churn
    siblings carry such a line (precedents D4).

**2. Untraceable source, and the search is not finished (P5, PROV-1 Must)**

- **Problem.**
  - Every link ends at an anonymous Kaggle upload from 2019 with no upstream. OpenML 44231 is a byte-identical copy
    (claim_audit 14).
  - PROV-1 says such a dataset "is `No`", and "only the end of a search counts". The search has not ended: the WebSearch
    budget ran out before a Google search for `"user_no_outgoing_activity_in_days"` / `"mobile-churn-data.xlsx"`
    (REVIEW_before caveat).
  - One lead is untested: OpenML 44228-44231 were uploaded together as one batch of telco churn sets (precedents D1).
- **Evidence against keeping.** water_quality_and_potability is the closest pair: the curator judged its data sound
  and still made it `No` on the source alone.
  - The real-export artefacts (sentinel dates, provisioning batches, refunds) answer PROV-3, "is it real?". They do
    not answer PROV-1, "can we tell what it is?" (precedents D1).
  - The curator's keep ("data looking very good and real") is from screening. A later stage's measured finding
    supersedes it (principles.md, Precedence: Stages).
  - This would be the fourth keep of an untraceable source under a Must. A Must takes no exceptions, so an amendment
    is due.
- **Remedy.**
  - Run the search: Google the column names and file name, and look up who uploaded OpenML 44228-44231.
  - Then either apply PROV-1 (`No`, `Missing source information`), or amend PROV-1/PROV-2 once for bank_customer_churn,
    tour_travels_churn, credit_card_customers and mobile_churn, and say whether an undefined target is allowed.
  - Do not ship on the screening comment alone.
  - Also correct the REVIEW search clue "on-net calls are rare: small operator or MVNO". It rests on a destination
    breakdown that is partial: the calls add up in only 10.8% of rows (column_audit problem 6).

**3. A temporal task ships as plain IID without the forced-IID tag (P4, SPLIT-8 Must, narrows SPLIT-7)**

- **Problem.** The use case is monthly scoring of a recurring base, which is temporal. The release holds one stock
  snapshot, and July and August hold new joiners only. The definition ships IID with `data_tags` absent (split_audit
  problem 1).
- **Effect on the task.** Even with a cohort mix, the measured cost of skipping the time step is real:
  - On the 1,533 later rows, the IID split gives 0.690 and a model trained on June gives 0.661.
  - The paired bootstrap gap is +0.028, 95% CI [0.004, 0.056] (split_audit).
- **Precedent.** account_debt_south_africa (Lennart, 2026-10-12) and expresso_churn_prediction_1m are both tagged.
  Nothing written sets this case apart (precedents D5).
- **Remedy (definition fix, no re-split).**
  - Add `data_tags = ("ForcedIIDFromTemporal",)`.
  - Add one sentence to the IID bullet: a deployed model trains on an earlier month's stock with a gap of the churn
    horizon; the release has one stock month; the measured cost above; further months should be recovered.
  - Have the task_summary `split` sentence say that it stands for a random part of one month's base, not next month
    (practitioner).
  - If the curator reads SPLIT-8's "no dates at all" as not covering a few cohort months, settle that as an amendment,
    not by omission.

**4. Numbers in the notes that do not reproduce (procedure, EV-1 Must; writing.md)**

- **Problem.** The claim audit could not reproduce several numbers or wordings:
  - "LightGBM 0.882 with each batch held together", described as batches of consecutive ids, was computed with a
    month x last-top-up-day key. Holding consecutive-id batches together gives 0.870-0.891 (claim_audit 24).
  - "13.8% of them were active before the day it counts to" measures 10.0% or 12.7%, depending on the reading, and the
    script that produced it has no computation (claim 33).
  - "negative amounts in six ... columns": the data have seven (claim 42).
  - "no ... use in 100 days in over 99% of cases" fails for July's 35 rows, of which 11.4% used something (claim 45).
- **Effect on the task.** None on the data. The drop holds on the usage evidence: 99.7% of the dropped SIMs used
  nothing. But the decision tables and notes are what the curator decides on.
- **Remedy (text fix).** Write "0.87-0.89 with batches of consecutive ids held together", give the measured share
  together with its definition, change "six" to "seven", and add the qualifier for July.

**5. Two default dates merged into one missing value (P7, CLEAN-10 Should)**

- **Problem.** Inactive-days values above 100 encode two different defaults, and both become NaN:
  - 2010-01-01, "no activity on record";
  - 2012-09-28, meaning unknown.
- **Effect on the task.** Their churn rates differ: user_no_outgoing 0.726 against 0.345, calls 0.594 against 0.304,
  reloads 0.223 against 0.081. The 2012 code covers only 29 to 136 rows per column, so the effect is small
  (column_audit problem 3).
- **Remedy (note).** Say in the inactive-days bullet that both defaults become missing and that 2012-09-28 is
  unexplained. Quality only; no reason to exclude.

**6. Missing values contradicted by the month's counts (P7, CLEAN-11 Should)**

- **Problem.** Some inactive-days values are missing although the month shows the activity: calls 90 rows, top-ups
  215, SMS 160, data 102.
  - 73 June rows have calls in the month but more than 30 inactive days.
  - Inactive days exceed the lifetime in 5 to 51 rows.
  - 34 June rows have intake 0 and a lifetime under 31 days.
  Each is under 0.4% of rows (column_audit problem 4).
- **Remedy (note).** Keep the values and add one line to the notes. Quality only.

</details>

<details><summary>Advocate rebuttal</summary>

**mobile_churn: advocate's rebuttal (2026-10-20)**

**Critic 1. The label is undefined (USE-5 Must): remedy conceded, extent disputed**

- **I concede:**
  - USE-5's check against the source cannot be done.
  - Remedy (b) should be applied now: a `Potential leak, kept on purpose:` line saying churn may be defined from the inactivity the recency columns measure, and to revisit it if the definition is found. I offered the same line in my point 2.
- **I dispute:** that the label's meaning is unknown, beyond its horizon. EV-2 says a measurement on the data beats a missing page, and the data pin down the parts of the meaning that bear on validity:
  - **It is churn after the snapshot, for both classes.** One no-activity value per month, with both classes present (claim audit, claims 17-20).
  - **It is not "inactive N days at the snapshot".** The churn rate rises step by step: 4.6% at 0-5 days, 61% at 60-75 days, 58% at 75-92 days. No cutoff makes it deterministic.
  - **It is not a restated feature.** Best single feature 0.779 against 0.844 for all; drop-one changes at most 0.001.
- **On the critic's "anything from 30 more days of inactivity to deactivated by the operator":** both readings are churn after the snapshot, which an operator acts on. They differ in horizon and rule, and USE-8 names "a label without a stated horizon" as an approximate fit. The fit is approximate already.
- **The rule that wins:** USE-8 (Must) tells us how to ship a label with a known gap. USE-5 asks for a redefinition only where a better target exists, and none is on offer here.
- **The "no precedent has both gaps" argument** reduces to point 2. The label question on its own is settled by the churn_telco_south_asia treatment.

**Critic 2. Untraceable source, search unfinished (PROV-1 Must): mostly conceded, one premise disputed**

- **I concede:**
  - Run the search: Google `"user_no_outgoing_activity_in_days"` and `"mobile-churn-data.xlsx"`, and find the uploader of OpenML 44228-44231.
  - PROV-1 is a Must. If the search ends with nothing, the outcome is either `No` or an amendment made on purpose, settled once for the four keeps.
  - The real-export artefacts answer PROV-3, not PROV-1.
  - Correct the "small operator or MVNO" clue: the calls by destination add up to the total in only 10.8% of rows (column audit, problem 6).
  - What follows: the verdict on issue 1 waits for the search's end. I no longer argue "ship now regardless".
- **I dispute** that "a later stage's measured finding supersedes" the curator's keep on the source.
  - That precedence rule covers a later finding about the same fact. Nothing measured since screening changes the source facts the curator saw. The comment "Another case of missing data" shows the missing source was known when they kept it.
  - The later finding, the undefined churn, is a USE-5 matter, handled in point 1.
  - So the curator's call still stands on the source question (Precedence: who decides, curator > AI). The open part is only the PROV-1 consistency check, which the curator answers.
- **I dispute** that water_quality_and_potability forces `No`.
  - The keep of tour_travels_churn has the same facts (no upstream, data judged real), and was decided the other way by the same curator.
  - The precedents conflict, so neither decides. That is why an amendment or a curator's call is needed, not a panel ruling by rank.

**Critic 3. Forced-IID tag missing (SPLIT-8 Must): conceded**

- Add `data_tags = ("ForcedIIDFromTemporal",)`, the IID sentence and the task_summary `split` wording, as the critic proposes.
- One qualification on the evidence. The +0.028 gap (CI [0.004, 0.056]) is measured on 1,533 new joiners who score 0.63-0.69 under any split, and it mixes cohort with time (split audit). It supports the tag. It does not support a re-split, which the critic does not ask for.

**Critic 4. Numbers that do not reproduce (EV-1, writing.md): conceded**

The same four text fixes as my points 3 and 7:
- "0.87-0.89 with batches of consecutive ids held together";
- the measured share with its definition in place of 13.8%;
- "seven" in place of "six";
- the July qualifier.

None of them changes a decision. The drop rests on the usage evidence (99.7% of the dropped SIMs used nothing in 100 days).

**Critic 5. Two default dates merged into one missing value (CLEAN-10 Should): conceded**

Add a note that both defaults become missing and that 2012-09-28 is unexplained. It covers 29 to 136 rows per column, so a note is the right remedy, not re-encoding.

**Critic 6. Missing values contradicted by the month's counts (CLEAN-11 Should): conceded**

Keep the values and add one line to the notes. Each case is under 0.4% of rows.

**Where the panel stands**

- **Agreed changes:**
  - the forced-IID tag and sentence;
  - the `Potential leak, kept on purpose:` line;
  - the text fixes in the notes;
  - the default-date note and the contradicted-values note;
  - the corrected REVIEW clue.
- **Agreed facts:** no column leak, IID is the only split this release supports, and dropping the never-activated SIMs is right.
- **Still disputed (for the curator, issue 1):** after the search ends, keep under an amendment of PROV-1/PROV-2 covering the four untraceable keeps, or `No` with `Missing source information`.
  - My side: tour_travels_churn, the curator's informed keep, and the measured validity (P3, P4, PROV-3).
  - The critic's side: water_quality_and_potability and the literal text of PROV-1.

</details>

<details><summary>Critic rebuttal</summary>

**mobile_churn: critic, rebuttal (2026-10-20)**

Summary: we agree on every change: the tag, the leak note, and the text fixes. What is left in dispute is one point
(advocate 6): whether the dataset ships before the source search ends.

| Advocate point | Response |
|---|---|
| 1. Honest evaluation (LEAK-10) | **Concede.** The windows end at the snapshot (0 of 2,498 joiners), the snapshot is shared by both classes, ids are unique, and there are no hidden groups. I raised no leak. One caveat: LEAK-24 and LEAK-25 stay untestable without the churn definition (column_audit problem 1). That is why the leak note below is needed, not a new point. |
| 2. Real use case, gap named (USE-1, USE-8, USE-5) | **Concede the remedy:** the `Potential leak, kept on purpose:` line, which is my point 1(b). **Dispute one reading.** USE-8 names "a label without a stated horizon", which is an unknown window. It does not cover a label whose meaning is unknown: "deactivated by the operator" and "inactive N more days" are different targets (practitioner, gap 1). churn_telco_south_asia had two source papers behind its label; this dataset has none (precedents D1, D4). So the USE-5 gap is acceptable only if the PROV-1 question is settled. It does not stand alone. |
| 3. Never-activated drop (PROV-13, LEAK-22) | **Concede.** I did not contest the drop. The two wording fixes (0.87-0.89 with consecutive-id batches held together; "June and August" for the over-99% claim) match my point 4. |
| 4. Worth benchmarking (TP) | **Concede.** No value objection. |
| 5. IID plus tag (SPLIT-8) | **Concede.** This is the same remedy as my point 3: the tag, one sentence, no re-split. |
| 6. Source (PROV-1) | **Dispute the order: keep now, search later.** (a) PROV-1 is a Must and "only the end of a search counts". If the search is open, the dataset is not cleared either. Shipping before the search ends ships with an open Must. Both sides agree the search is cheap (two Google queries and the OpenML 44228-44231 uploader), so the mildest remedy is to finish it first, then ship or apply `No`. (b) "Identifiable first uploader": the Kaggle account `dimitaryanev` has posted no description, and the one provenance question (2021-12-27) has gone unanswered (REVIEW_before issue 1). A handle that cannot say where the data came from is the "anonymous re-upload with no documentation" that PROV-1 describes. PROV-8 decides which source to cite, not whether the source is known. (c) The curator's "data looking very good and real" is an undated screening comment, made before the 2026-10-07 finding that churn is undefined (precedents D1). Under principles.md, Precedence: Stages, a later measured finding supersedes a screening reading. So it is not a decision taken with this evidence. (d) PROV-3 passing answers "is it real?", not "what is it?". water_quality_and_potability was judged sound and still went `No`. tour_travels_churn is a precedent that conflicts with the Must, so it is flagged, not followed. **Agreed:** if the search ends empty, the choice is between amending PROV-1/PROV-2 once for the four keeps and `No`. That choice is the curator's. |
| 7. Cleaning (P7) | **Concede.** These are the same text fixes as my points 4 to 6: "seven", the measured 10.0%/12.7% share with its definition, the 0.882 key, the 2012-09-28 clause, and the note on sentinels contradicted by counts. All are quality fixes; none is a reason to exclude. |

**Joint position for the mediator**

Ship after changes: the SPLIT-8 tag and sentence, the `Potential leak, kept on purpose:` line, and the note fixes. All
of these hold only once the PROV-1 search has ended. If it finds nothing, the curator takes the amendment or the `No`.

</details>
