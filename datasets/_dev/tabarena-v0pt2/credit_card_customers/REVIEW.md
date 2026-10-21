# credit_card_customers

**Outcome:** added; recommended not to ship yet, until the standard for calling data generated without a source
statement (issue 1) is set: if this dataset meets it, `No (Retired)` with `AHDS` and `Missing source information`;
if not, ship as defined now. Kaggle's BankChurners.csv from teaching case 11 of Analyttica's LEAPS platform, a random
split of one undated snapshot: will a credit card customer close the account? Not built yet.

**Main points:** Are measured marks of generated data enough to retire without a source statement or a generator
(one standard for three datasets)? Then confirm the keep of the untraceable teaching source.

**Record judgment:** don't ship yet; issue 1 decides. Validity: SEL-1 holds; USE-1 holds with an approximate fit;
LEAK-10 maybe (the activity window may end at the closure), kept with a note, since the oldest quarter's count alone
gives ROC AUC 0.819; LEAK-30 weak, kept (Lennart, 2026-10-19); SPLIT-8 triggered, fixed with the
`ForcedIIDFromTemporal` tag and the split wording; PROV-1 kept on a screening-era call through a named first platform,
to be confirmed (issue 3); PROV-3 and SEL-16 maybe generated (issue 1). Value: no task-probe flag, but near the
ceiling (CatBoost with default settings, ROC AUC 0.9943); check against the tuned results when they exist. Quality:
the loose wording the panel found (the 12-month count, the profile columns, the clipped derived columns, "not missing
at random") is fixed in `dataset.py`. Weighed: an untraceable source and likely constructed columns against a real
churn use case; the ceiling does not add to the provenance doubt (independent failures are not conflicts).

**Issues for Lennart:**

1. **Are measured marks of generated data enough to retire it, with no source statement and no generator?**
   - Problem and effect: if the rows come from a teaching-case generator, the benchmark scores how well models fit
     that generator, not a bank's churn. PROV-3 (Must) and SEL-16 (Must) retire generated data, but the rules set no
     bar for "generated" when the source says nothing and no generator is written down. "Calibrated" below means the
     same test run on real tables of the same kind (the control column).
   - Evidence, reproduced by the claim auditor on the raw file:

     | Mark | This dataset | Control |
     |---|---|---|
     | Rows where the 12-month transaction count equals the Q4 count plus the Q1 count | 10,127 of 10,127 | 564-597 with shuffled totals; 9 of 8,920 in Home Credit |
     | Correlation (Spearman) of inactive months with the transaction count | -0.051 | -0.60 in Home Credit |
     | Correlation (Spearman) of spend with the credit limit | 0.028 | 0.447 in Home Credit |
     | How well a classifier tells real rows from rows with Education_Level shuffled within class (AUC; 0.5 = not at all) | 0.495 | 0.58-0.61 on two real credit tables |

     Also: in the 7,664 rows not at the filled-in 36 months, tenure in months is never above age - 4 and follows age
     in years (slope 1.006, r 0.893); 0 of 5,358 women earn above $60K. Q1 and Q4 cannot both be quarters (that
     leaves no Q2 or Q3 transactions for anyone); read as half-years, the 7 customers without a second-half
     transaction would have at least 6 inactive months, but they have 2-4, so that reading fails too.
     Total_Trans_Amt falls in clusters whose class mix changes: 3,000-5,000 is 98% existing customers, 6,000-7,000 is
     68% attrited, and the 746 customers above 12,000 include no attriter.
   - Against: the generated-data probe raises no flag; the label-free distance (whether the nearest neighbours,
     found without the label, predict it) gives AUC 0.559, against 0.923 for homeq_default_prediction. The mediator
     ran PROV-3 test 5 (a correlation between two columns that differs by class): within each class, 8 of 91 pairs
     of numeric columns differ by 0.3 or more in Spearman correlation and none changes sign, against 0 of 210 and 1
     of 45 pairs on two real credit tables. Most of the 8 follow from the zero balances (55% of attriters) and the Q4
     drop of attriters; one (number of products vs amount, 0.02 attrited, -0.39 existing) has no ready explanation.
     The advocate adds that the amount-bin class mix is what any strong feature shows (Total_Trans_Amt alone gives
     ROC AUC 0.876), not test 5 as written. So: more class dependence than in real credit tables, but circumstantial
     (EV-6). The trail ends at LEAPS case 11, which is offline with no archived copy, so no source statement can be
     had.
   - The rule question: the advocate read EV-3 as requiring a source statement, the critic as requiring it only
     "where possible". The mediator sides with the critic: EV-3 asks that the source be looked up and reported (done
     here: offline), and homeq_default_prediction was retired with no source statement. What stays open is the bar
     the marks must clear.
   - Precedent: every dataset retired under PROV-3 had a test that tied the marks to the label, a generator or a
     source statement (ecommerce_shipping, customer_satisfaction_in_airline: id cycles and labels flipped by a rule;
     homeq_default_prediction: artefacts that predicted the label). Here the label-linked tests are weak.
   - Implemented: kept, with the marks in the Anomaly bullet and the first decision (with the amount-bin class mix
     and the test-5 result), `fit="approximate"`. The `2ndTierData` tag (from the v1 migration) is dropped: the
     curator retired the tag on 2026-10-21 (cross-dataset item "Define `2ndTierData` or drop it?", option (b)); the
     fit label carries what it said.
   - Alternatives:
     - (a) a standard such as "N calibrated marks from at least two PROV-3 tests are enough without a generator":
       met here, so `No (Retired)`, `AHDS` + `Missing source information`; cost: the folder goes, and
       hepatitis_c_egypt and stroke_prediction are judged by the same bar (framingham_heart_study_fhs, where no test
       fires, passes either bar);
     - (b) a standard such as "without a generator, the marks must predict the label (test 5 or 7)": not met here,
       so ship, with "maybe generated" and the test that would settle it (the LEAPS case material, or a generator
       written down) recorded as a finding, as for first_principles_tully_fisher; cost: a dataset whose columns are
       likely constructed enters the benchmark.
   - Rule: PROV-3 (Must), SEL-16 (Must), EV-3 (Must), EV-6 (Should). Either choice is an amendment of PROV-3 and
     EV-3, recorded in the knowledge files (cross-dataset item "PROV-3 evidence standard").
   - Recommendation (AI): (b). Every dataset retired under PROV-3 so far had marks tied to the label, a generator or a
     source statement; here the label-linked tests are weak (distance AUC 0.559, no sign change), so (a) would retire
     on weaker evidence than any precedent. Set the standard once and apply it to the three datasets with measured
     marks.
   - Decision needed: which standard, (a) or (b), for this dataset, hepatitis_c_egypt and stroke_prediction.

3. **Confirm the screening-era keep of an untraceable teaching source?** Now follows issue 1: PROV-2 was amended
   (Lennart, 2026-10-21): "a named first platform (a course or teaching provider) counts as a known source when the
   data shows no PROV-3 marks". LEAPS case 11 is such a platform, so the source holds if issue 1 finds the measured
   marks not enough; if they are judged enough, the dataset is `No` (`AHDS`, `Missing source information`) under
   PROV-3 anyway. Nothing is left to decide here beyond issue 1.
   - Problem: the trail ends at LEAPS case 11, which is offline. No bank, country or period is named anywhere. The
     keep ("good to use for now. We can filter later") comes from screening, before the measurements of 2026-10-07; a
     later stage's measured finding supersedes it, so the keep needs confirming.
   - Effect: if kept, the benchmark carries a churn table nobody can check against its origin.
   - For keeping: PROV-1 counts "an identifiable first uploader" as traceable, and the Kaggle uploader names the
     LEAPS case URL. bank_customer_churn (data from a named data-science course) was kept the same way, and
     tour_travels_churn (a bare Kaggle upload with no named origin) on less.
   - Against: course churn data with signs of fakeness went `No` three times (customer_churn_dataset,
     predictive_analytics_for_customer_churn_dataset, ibm_telco_customer_churn). Whether the rows are real is no
     detail in the sense of PROV-2, so this side holds only if issue 1 goes toward "generated".
   - Implemented: kept, the unknown bank, place and period stated in the task summary. `source = "Other"` names the
     first publication (LEAPS); the record's `Company` counts as `Other`, so no field disagrees.
   - Alternatives: (a) confirm the keep and amend PROV-1/PROV-2: "a named course or teaching platform counts as a known
     source when the data shows no PROV-3 marks"; cost: a third keep under a Must becomes a rule (mobile_churn, from an
     unnamed operator, is not covered by this wording); (b) revise: `No` + `Missing source information`; cost: the
     decision differs from bank_customer_churn and tour_travels_churn unless they are reopened.
   - Rule: PROV-1 (Must), PROV-2 (Should). This is the third keep of a dataset with an untraceable source, so an
     amendment is due (cross-dataset item "Amend PROV-1/PROV-2 for a named course or teaching platform").
   - Decision: (a) taken as a rule (PROV-2 amended, 2026-10-21); the outcome follows issue 1.

**Review panel:** don't ship yet (mediator); the PROV-3 standard decides. Claim audit: 50 claims, 41 hold, 3 hold
with a caveat (wording fixed), 6 untested, 0 refuted. Blind review: include with changes; main concern the activity
window that may end at the closure. Debate: agreed on the window note, the `ForcedIIDFromTemporal` tag and the
wording fixes; disputed: whether the measured marks of generated data are enough (issue 1). The mediator's issue 1 is
issue 1 here and its issue 2 is issue 3; the precedent check's D1 and D2 are issues 1 and 3, and its D3 to D6
(window, clipping, filled values, ceiling) are consistent with precedent and need no decision.

<details><summary>Mediator</summary>

**Mediator: credit_card_customers (re-check, 2026-10-20)**

**Recommendation (judgment record)**

```text
Verdict: don't ship yet. The PROV-3 question (issue 1) decides it. If the marks are judged not enough: ship after
changes. If they are judged enough: No (Retired), AHDS + Missing source information.
Validity: SEL-1 holds; USE-1 holds (approximate fit, gaps named); LEAK-10 maybe, kept with a note (LEAK-11; Q1-only
AUC 0.819 comes before the closing); LEAK-30 weak, kept (CC 2026-10-19); SPLIT-8 triggered, fixed (ForcedIIDFromTemporal
tag + wording); SPLIT-29 holds; PROV-1 holds through a named first platform (LEAPS case 11), with the PROV-2 note
depending on issue 1; PROV-3/SEL-16 maybe generated: the marks are measured, but the rules set no evidence standard
without a generator (issue 1).
Value: TP-1, no flag; near the ceiling (CatBoost 0.9943); check against the tuned results when they exist.
Quality: wording fixes (see the changes below).
Weighed: source -, marks of a constructed table -, real churn use case +, near ceiling -.
For the curator: issue 1, the PROV-3 evidence standard (one decision for four datasets); issue 2, the PROV-1/PROV-2
amendment.
```

**Changes to make now (no decision needed)**

1. **SPLIT-8 (Must).**
   * Add `ForcedIIDFromTemporal` to `data_tags`.
   * Reword `split` and the IID bullet:
     * the split is forced;
     * its cost cannot be measured (the file order follows Total_Trans_Amt, Spearman 0.82; thirds by CLIENTNUM give 0.993, the same as a random split);
     * recover the dates if the LEAPS material turns up.
2. **LEAK-10/LEAK-11 note.** Add the window test to the "Potential leak, kept on purpose" bullet:
   * the Q1 count alone gives AUC 0.819, the same as Q4 alone;
   * profile + Credit_Limit + Q1 count gives 0.895;
   * the pure tails are 61 rows (54 with 6 contacts, 7 with a zero Q4 count).
3. **USE-5 wording in `predicted`.**
   * The label has no stated horizon.
   * Write "the source does not say whether closures by the issuer count". Do not write "mixes voluntary and issuer closures": that 50/50 figure is an industry figure from the practitioner, not a measurement on this file (EV-2, EV-7). The advocate's wording wins.
4. **PROV-8.** Align `source = "Other"` (definition) with `original_source: Company` (record), using one value for the first publication, Analyttica's LEAPS training platform.
5. **Wording fixes (P7; EV-7):**
   * Total_Trans_Ct equals the Q4 + Q1 counts in every row, so it cannot be both a 12-month count and a sum of quarters (claim 7);
   * name the "10 profile columns" behind AUC 0.625 (claim 23);
   * "not missing at random" holds for Income only (claim 28);
   * Avg_Open_To_Buy and Avg_Utilization_Ratio inherit both clips (LEAK-30 bullet);
   * add CLIENTNUM to `changes`;
   * mark the LEAPS date and the "dummy dataset" quote as unverified in the record.
6. **Decision 1 evidence.** Add these to decision 1 whichever way issue 1 goes:
   * the amount-bin class mix: 3,000-5,000 is 98% existing; 6,000-7,000 is 68% attrited; above 12,000 are 746 rows with 0 attrited;
   * the test-5 result below.
7. **REVIEW.md correction.** `2ndTierData` is not "Implemented" by this review; it came from the v1 migration (commit 2475ea2). No knowledge file defines the tag, and it cannot carry a Must (both sides agree).
8. **TP-1.** When tuned results exist, check them against `solved`. If it trips, decide as for anneal or aps_failure.

**Issues for the curator, ranked**

**Issue 1 (P2/P5, Must: SEL-16, PROV-3). Are the measured marks enough to call the data generated without a source statement or generator?**

**Problem and effect.** If the rows come from a teaching-case generator, the benchmark scores how well models fit that generator, not a bank's churn.

**What the rules settle.**
* **No source statement is required.**
  * EV-3 sits in a sentence about reading probe flags. Its clause ("needs what the source says and, where possible, the generator written down") requires looking up and reporting what the source says. task_probes.md puts it the same way: "Before proposing a retirement, find what the source says".
  * PROV-3 decides through "the seven tests" with calibration. "When you can, write the generator down: that settles it" makes a generator sufficient, not necessary.
  * homeq_default_prediction (CC 2026-09-24) was retired on test-5 marks alone, with no source statement. Its hypothesis was marked "unverified, the book's text not read". Those marks were the label-free distance (AUC 0.923), number formats that differ by class, and missingness pure in the label.
  * precedents.md calls homeq a "mechanism"; that overstates it.
  * Here the source was looked up and is offline (no Wayback snapshot), so EV-3's requirement is met by reporting that.
* **The critic's EV-2 argument does not decide it.** EV-2 ranks evidence that disagrees, and no page disagrees here.
* **The rules set no bar for "generated" when there is no generator.** EV-6 (Should) has a borderline case reported as "maybe" for the curator to decide. That makes this a question of standard, i.e. an amendment (option d), not mine to settle.

**Agreed and measured marks** (calibrated, EV-9):

| Mark | This dataset | Calibration |
|---|---|---|
| Ct = Q4 + Q1 counts | 10,127/10,127 rows | shuffled 564-597; Home Credit 9 of 8,920 (not re-run) |
| Inactive months vs transaction count, Spearman | -0.051 | Home Credit -0.60 |
| Spend vs limit | 0.028 | Home Credit 0.447 |
| Education permutation discriminator | 0.495 | 0.58-0.61 on two real credit tables |

Also: tenure never above age-4, slope 1.006, r 0.893; 0 of 5,358 women above $60K; 7 customers with no Q4 transaction but only 2-4 inactive months, which refutes the half-year reading.

**Decisive experiment run by me: PROV-3 test 5, class-dependent correlations.**
* Method: Spearman correlation within each class for every numeric pair (more than 5 values).
* Result here: 0 sign flips (with |r| ≥ 0.1 in both classes). 8 of 91 pairs differ by |Δr| ≥ 0.3.
* Calibration: 0 of 210 (credit_card_clients_default), 1 of 45 (give_me_some_credit), 0 of 10 (bank_customer_churn).
* Most of the 8 trace to label-linked mechanisms (EV-9: a selection on the label changes correlations):
  * Credit_Limit vs utilization: -0.05 attrited / -0.53 existing. On non-zero balances it is -0.89 / -0.74, so the gap is the zero-balance mass (55% of attriters).
  * Q4/Q1 change vs amount: 0.50 attrited / 0.04 existing, consistent with the closure collapse.
  * One pair has no ready explanation: Total_Relationship_Count vs Total_Trans_Amt, 0.03 attrited / -0.39 existing.
* Reading: more class dependence than in real credit tables, no sign change, and largely explained without a generator. Circumstantial, not proof (EV-6).

**Best evidence on each side.**
* **For retiring (critic):**
  * several independent calibrated marks point the same way, including a proven constructed column and a refuted alternative reading;
  * PROV-3 also excludes "a real table someone reworked", so both readings land on the same Must;
  * the source cannot be traced, so this is where the rule should be strictest.
* **For keeping (advocate):**
  * every retired PROV-3 case had marks that themselves predicted the label (homeq: artefacts alone 0.953 of 0.975), or a generator, or a source statement;
  * here the label-link tests are weak or negative: distance 0.559 against a full model of 0.994, no sign flips;
  * the amount-bin flips are what any strong feature shows (single-feature AUC 0.876), not test 5 as written;
  * the reworked column is fixed by a wording change (remedy ladder: fix before exclude).

**Decision needed.** One standard, recorded as an amendment of PROV-3 / EV-3 / EV-6, applied alike to credit_card_customers, hepatitis_c_egypt, stroke_prediction and framingham_heart_study_fhs. For example: "N calibrated marks from at least two PROV-3 tests are enough without a generator", or "without a generator, generated data needs marks that predict the label (test 5 or 7)".
* If the bar is met: `No (Retired)`, `AHDS` + `Missing source information`.
* If not: ship after changes, with "maybe generated" and the settling test (the LEAPS case material, or a generator written down) recorded as a finding (as for first_principles_tully_fisher).
* Either way, `2ndTierData` is not the outcome: define it in a knowledge file or drop it.

**Issue 2 (P5: PROV-1 Must, PROV-2 Should). Confirm the screening-era keep, and amend PROV-1/PROV-2.**

**Problem.** The trail ends at LEAPS case 11, which is offline. No bank, country or period is named. The keep ("good to use for now") predates the 2026-10-07 measurements, and a later stage's measured finding supersedes it.

**Each side.**
* **Advocate:** PROV-1 counts "an identifiable first uploader" as traceable, and the Kaggle uploader quotes the LEAPS URL. Like bank_customer_churn and tour_travels_churn.
* **Critic:** whether the rows are real is no "detail" in the PROV-2 sense. Course churn data with signs of fakeness went `No` three times (customer_churn_dataset, predictive_analytics_for_customer_churn_dataset, ibm_telco_customer_churn).
* The critic's point holds only if issue 1 goes toward "generated", so decide issue 1 first.

**Decision needed.**
* Confirm or revise the keep.
* Adopt the amendment, now due as the third keep of this kind. Proposed: "a named course or teaching platform counts as a known source when the data shows no PROV-3 marks", worded to fit the issue 1 standard.

**Not an issue: near the ceiling (P6)**

No TP flag. A ceiling is no verdict (EV-3). It does not add to a P5 doubt (principles step 4: independent failures are not conflicts). Correction to the advocate: log loss is not shipped as a metric (roc_auc only), so it adds no leaderboard headroom.

**Agreed facts**

* One row per customer: CLIENTNUM unique, 0 duplicate rows, 0% near copies, no hidden-group hit. Folds stratified at 16.05-16.08% attrited.
* No dates and no second snapshot. The file order follows Total_Trans_Amt (Spearman 0.82). SPLIT-8 is triggered.
* Leak probe: all features 0.993-0.994; activity block 0.980; profile 0.629-0.636; Q1 alone 0.819 = Q4 alone; 1-NN agreement 0.886 (chance 0.730); label-free distance 0.559; no red flag. Generated probe: no flag.
* The window may end at the closure: Contacts 6 (54 rows) and zero Q4 count (7 rows) are all attrited; zero balance in 55% of attrited against 19% of existing. Not proven strong. Kept with a note, consistent with churn_telco_south_asia.
* Clipping at whole-file percentiles: Credit_Limit 507/508 rows, Total_Revolving_Bal 508. Kept by the CC of 2026-10-19.
* The generated-data marks in issue 1 are reproduced. No source statement exists, the source is offline, and no generator is written down.
* `2ndTierData` came from v1, is defined in no knowledge file, and cannot carry a Must.
* The PROV-1/PROV-2 amendment is due. The source fields disagree.

**Consistency with precedent**

* **LEAK-10:** follows churn_telco_south_asia (CC 2026-10-15). It differs from iranian_churn, whose paper states the window ends at churn; no such statement exists here.
* **LEAK-30:** follows the Tensions row of 2026-10-19 (bioresponse, taiwanese_bankruptcy_prediction, cooking_time). The register's drift flag does not apply: coad could be rebuilt from its origin; this dataset cannot.
* **SPLIT-8:** follows account_debt_south_africa and expresso_churn_prediction_1m.
* **PROV-3:**
  * Keeping would differ from ecommerce_shipping and customer_satisfaction_in_airline. The fact that sets it apart: no label-linked or mechanical mark (no id cycles, no label flips by a rule; distance 0.559, test 5 without sign flips).
  * Retiring would follow homeq in kind (statistics, no source statement), but on weaker label-linked evidence than homeq had.
  * Both choices need the standard in issue 1. Whichever standard is chosen also binds hepatitis_c_egypt, stroke_prediction and framingham_heart_study_fhs. The earlier review file's line citing stroke_prediction and hepatitis_c_egypt as precedents is wrong: those are AI recommendations, not decisions.
* **PROV-1:** this would be the third keep of an untraceable course dataset (after bank_customer_churn and tour_travels_churn), so the amendment in issue 2 is due.

**Files**

* Rules: .claude/skills/knowledge-curation/references/ (principles.md, evidence.md EV-3/EV-6/EV-9, provenance.md PROV-1 to PROV-3 and its Methods, task_probes.md "Generated data")
* Precedent: curation/records/homeq_default_prediction.md (CC 2026-09-24)
* Test 5 data: the column auditor's frame of this dataset, plus the cached BeyondArena containers of credit_card_clients_default, give_me_some_credit and bank_customer_churn. The 30,000-row samples use seed 0.

</details>

<details><summary>Claim audit</summary>

**Claim audit: credit_card_customers (2026-10-20)**

LightGBM on the 9 shipped splits and permutation discriminators on the frame rebuilt from the definition; CatBoost
with default settings; the Zenodo copy downloaded. Licence and pretraining overlap not used as evidence.

Summary: 50 claims. 0 refuted. 41 hold, 3 hold with a caveat (7, 23, 28), 6 untested (2/18, 13 date, 19, 24, 43, 46
judgment). No implied claim refuted.

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 1 | Task: will the customer close the card | task_summary.question | Kaggle API description | holds | "predict ... who is gonna get churned" | USE-1 |
| 2, 18 | Snapshot scoring, manager contacts first | task_summary.use_case, CC bullet 1 | none possible on the data (no dates) | untested | Kaggle description names the manager; the snapshot/window timing is not in the data | USE-2, USE-3 |
| 3 | 10,127 customers, one row each | task_summary.row | shape, CLIENTNUM unique | holds | 10,127 rows, CLIENTNUM unique | SPLIT-29 |
| 4 | Teaching case of LEAPS; bank, place, period unstated | row | Kaggle API description; Wayback | holds | uploader quote names LEAPS; no bank/country/period anywhere | PROV-1 |
| 5 | 16% closed | predicted | value counts | holds | 1,627/10,127 = 16.07% | - |
| 6 | Closure timing vs window not stated | predicted | Kaggle description | holds | description silent on timing | LEAK-22 |
| 7 | Features incl. 12-month activity and quarter change | known | column list; Q4+Q1 identity | holds, caveat | 19 columns as listed; but Total_Trans_Ct = Q4 + Q1 count in 10,127 rows, so "12 months" and "quarters" cannot both be true (no Q2/Q3 transactions) | USE-6, PROV-3 |
| 8, 36 | Random customers, no dates, no repeats, no duplicates | split; CC IID | duplicates; dtypes; hidden-group probe | holds | 0 duplicate rows, 0 duplicate feature rows; no date column; probe 0 hits, near copies 0.0% | SPLIT-1, LEAK-16 |
| 9, 26 | Only change: drop NB posteriors (and CLIENTNUM) | changes; CC Dropped | read `_clean`; rebuilt frame | holds | 19 features + target; `changes` omits CLIENTNUM (an id, not a data change) | LEAK-13 |
| 10-12 | fit approximate; potential leak; marks of generated data | fit, fit_reason | rerun of AUCs (23) and identities (29-35) | holds | see 23, 32-35 | USE-8, PROV-3 |
| 13 | 2020; LEAPS case 11 dated 2020-04-19, offline | year, source_url | curl; Wayback availability API | holds (offline, not archived); date untested | HTTP 000 on leaps.analyttica.com; Wayback: no snapshot of sample_cases/11 | PROV-8 |
| 14 | Zenodo 4322342 holds the same file byte for byte | license/download | downloaded, sha256 | holds | sha256 c91b525a...b779 on both; Zenodo 2020-12-15, zhyli, cc-by-4.0 | EV-4 |
| 15 | Kaggle v1, 2020-11-19, never updated, one file, sha256 | download_description | Kaggle public API; sha256 local | holds | currentVersionNumber 1, lastUpdated 2020-11-19T07:38, 1,510,880 bytes; hash matches | - |
| 16 | Uploader quote | download_description | Kaggle API description | holds | verbatim match | PROV-1 |
| 17 | domain, 2ndTierData | metadata | read | holds | - | - |
| 19 | Kaggle topic 203290 asked, no answer | CC leak bullet | not re-fetched (Kaggle discussion needs JS) | untested | quoted in the earlier review file | EV-6 |
| 20 | 7 no-Q4, 54 with 6 contacts, all attrited | CC | counts | holds | 7/7 and 54/54 attrited | LEAK-10 |
| 21 | Revolving balance 0: 55% vs 19% | CC | shares | holds | 0.549 vs 0.186 | LEAK-10 |
| 22 | Median Q4/Q1 0.53 vs 0.72; window not months past closure | CC | medians; zero-Q4 count | holds | 0.531 vs 0.721; only 7 of 1,627 attriters with no Q4 transaction; their inactive months 2-4 | LEAK-11 |
| 23 | LightGBM AUC 0.980 activity, 0.625 profile, 0.994 all | CC | LightGBM default, 9 shipped splits | holds, caveat | 0.981 (6 activity), 0.629 (9 demographic + Credit_Limit; 0.601 for 9 alone), 0.993 all; the "10 profile columns" are not named | EV-5 |
| 24 | Kept: falling activity is the use-case signal | CC | weighing call | untested | not a fact the data can settle without the closure date | LEAK-22 |
| 25 | Target Attrition_Flag two values | CC | value counts | holds | Existing 8,500, Attrited 1,627 | - |
| 27 | 5 categorical, rest numeric | CC | container dtypes | holds | 5 categoricals, 14 numeric | CLEAN |
| 28 | Unknown stays; not missing at random | CC, decision 2 | Gender x Income; Unknown vs label | holds, caveat | Income Unknown 1,060 F vs 52 M; but Unknown carries no label signal (16.8-17.2% vs 16.0%) and no MNAR evidence is given for Education/Marital Unknown | CLEAN |
| 29 | Open_To_Buy = Limit - Bal, Util = Bal/Limit in every row | CC | exact recompute | holds | max abs diff 6e-14; utilisation 0 rows off at 3 decimals | PROV-3 |
| 30 | Credit_Limit clipped 507 at 1,438.3, 508 at 34,516; Rev_Bal 508 at 2,517 | CC | counts, percentiles | holds | exact counts; p5 1,438.51 (linear) vs min 1,438.3, p95 34,516; Rev_Bal p95 = max 2,517 | LEAK-27 |
| 31 | Months_on_book 36 for 24% | CC | value counts | holds | 2,463 (24.3%) vs 305-358 for 33-39 | CLEAN |
| 32, 39 | Q4+Q1 identity in every row; inactive unrelated | CC, decision 1 | integer search per row; shuffled control; Spearman | holds | 10,127/10,127 (one rounding tie); shuffled 564-597; Spearman -0.051, within class 0.025/0.012 | PROV-3 |
| 33, 38 | Tenure follows age: <= age-4, rarely < age-20, slope 1.006, r 0.89 | CC, decision 1 | on 7,664 non-36 rows | holds | 0 above, 42 below, slope 1.006, r 0.893; 445 of the 36s break the bound | PROV-3 |
| 34, 40 | No woman above $60K; Unknown 1,060 F, 52 M | CC, decision 2 | crosstab | holds | 0 F in $60K+ bands | PROV-3 |
| 35 | Total_Trans_Amt clusters | CC | bins | holds | 2 rows in 10.5-12K, 746 above 12K, 0 attrited above 12K | PROV-3 |
| 37 | No probe flag; CatBoost 0.9943, 3 of 9 >= 0.995 | CC | CatBoost default on 9 splits | holds | mean 0.9943; 0.9953, 0.9958, 0.9953 >= 0.995 | TP-1 |
| 41 | No splits_comment; no accepted warnings | definition | read; checklist | holds | dataset check 0 warnings | - |
| 42 | LEAPS down; paper uses, not source | record | curl | holds (URL down) | HTTP 000 | PROV-1 |
| 43 | LEAPS calls another case "a dummy dataset" | Assessment 10-07 | web search | untested | no LEAPS page found; not archived | EV-6 |
| 44 | Shuffled ~550 identity rows; Home Credit 9 of 8,920 | Assessment 10-07 | shuffled control (3 seeds) | holds (shuffle); Home Credit not re-run | 564-597 | PROV-3 |
| 45 | Spearman -0.05; education nothing beyond label; r 0.89; 0/5,358 women | Assessment 10-07 | Spearman; within-class permutation discriminator (GroupKFold by row) | holds | -0.051; Education AUC 0.490-0.502 (Marital 0.58, Inactive 0.53 for contrast); 0 of 5,358 | PROV-3 |
| 46 | Clipping kept (curator) | CC 10-19 | curator decision | not a fact | - | LEAK-27 |
| 47 | Priority 1, near-ceiling | Assessment 10-20 | AUCs | holds | 0.993-0.994 | TP-1 |
| 48 | original_source Company vs source Other | front matter | read | holds (the mismatch is real) | record `Company`, definition `Other` | PROV-8 |
| 49 | Spend vs limit 0.028; Edu V 0.028; single 45% vs 43% | the earlier review file 1 | Spearman, Cramer's V, shares | holds | 0.028; V 0.028 p 0.23 without Unknown (0.030, p 0.037 with it); 0.450 vs 0.426 | PROV-3 |
| 50 | Profile + balance AUC 0.803; log loss 0.078 | the earlier review file 2 | LightGBM on 9 splits | holds | 0.807; all-column log loss 0.075 | LEAK-11 |

**Implied claims**

* Every feature known at the prediction point: untested (no closure date); the 6 activity columns give 0.981 alone. LEAK-22.
* Split is the one the use case needs: IID holds as far as the file shows (no date, no repeats). SPLIT-1.
* Target is the real-world target: the data card's "account closed" matches; how the label was produced is unknown.
* No row copied across the split: holds (0 duplicates, near copies 0.0%).

**Refuted / untested, ranked**

No claim refuted. Untested, by rank:
1. P4 (Must, LEAK-22): window ends at the closure (claims 2, 18, 24, 19). Changes the leak verdict; mildest remedy
   stays the documented note; nothing on the data can settle it.
2. P5 (PROV-1/3): the LEAPS date and "dummy dataset" quote (13, 43) are not reproducible today; the generated-data
   finding rests on the reproduced identities, not on them. Remedy: mark them as unverified in the record.
3. Wording (P7): claim 7 calls Total_Trans_Ct a 12-month count while it equals Q4 + Q1; claim 23 should name its 10
   profile columns; claim 28's "not missing at random" holds only for Income; `changes` omits CLIENTNUM.

</details>

<details><summary>Column audit</summary>

**Column audit: credit_card_customers (2026-10-20)**

Frame: rebuilt from the definition through `dataset_io.load(..., built=False)`: 10,127 rows, 19 features + target,
IID 3 repeats x 3 folds.
Prediction point (LEAK-1, USE-3): a snapshot date; the bank scores each card customer from the profile and the last 12
months of activity. Codebook: the Kaggle data card only (LEAPS case material offline); nothing states when the
closure happened relative to the 12-month window or the snapshot of the point-in-time columns.
Base rate attrited 0.161. Single-feature AUCs from the leak probe; LightGBM numbers below are mine, mean over the 9
shipped splits (300 trees, lr 0.05).

**Column table**

| Column | Meaning (data card) | Known at prediction? | Dtype and cleaning | Verdict | Rule |
|---|---|---|---|---|---|
| CLIENTNUM (dropped) | masked client number | yes | dropped; unique; AUC 0.453 on the raw file | fine | CLEAN-3, LEAK-17 |
| Naive_Bayes_..._1, _2 (dropped) | posteriors of an NB classifier fit with the label | no (label-fit) | dropped, asserted 2 columns | fine (correctly removed) | LEAK-27, CLEAN-6 |
| Attrition_Flag (target) | account closed (Attrited) or not | outcome | category, 2 values, no missing | fine | CLEAN-15 |
| Customer_Age | age in years | yes (at snapshot) | int, 26-73, no impossible values | fine; generated-data mark: tenure follows it (r 0.893 off the 36s) | PROV-3 |
| Gender | F / M | yes | category | fine; no woman above $60K (0 of 5,358) is a generated-data mark | PROV-3 |
| Dependent_count | number of dependents | yes | int 0-5 | fine | |
| Education_Level | education | yes | category, 7 levels incl. Unknown (1,519); unordered | fine; Unknown kept as a category with a documented reason, attrited 0.169 (base 0.161) so not outcome-driven missingness | CLEAN-10, LEAK-10 |
| Marital_Status | marital status | yes | category, 4 levels incl. Unknown (749) | fine; Unknown attrited 0.172 | CLEAN-10 |
| Income_Category | income band | yes | category, 6 levels incl. Unknown (1,112); unordered | fine (optional: ordered levels) | CLEAN-14 |
| Card_Category | card type Blue/Silver/Gold/Platinum | yes | category; unordered | fine (optional: ordered) | CLEAN-14 |
| Months_on_book | tenure in months | yes (up to snapshot; unknown whether measured at closure) | int 13-56; 2,463 rows (24.3%) at 36, likely a filled missing value | cleaning question, kept with a note; 36s attrited 0.175, not outcome-driven | CLEAN-10, PROV-13 |
| Total_Relationship_Count | number of the bank's products held | likely yes (point-in-time, date not stated) | int 1-6 | fine; could fall at closure (1-2 products: 0.26-0.28 attrited) but no pure value | LEAK-10 (weak) |
| Months_Inactive_12_mon | inactive months in the last 12 | window timing unknown | int 0-6 | maybe-leak, kept with note; no post-closure pile-up: 6 months is 1.2% in both classes, so the window does not run past the closure | LEAK-10 |
| Contacts_Count_12_mon | contacts with the bank, last 12 months | window timing unknown | int 0-6 | maybe-leak, kept with note; value 6: 54 rows, 100% attrited (pure value, probe 4 needs >=100 rows, so not flagged); calls to close the card would look like this | LEAK-10 |
| Credit_Limit | credit limit | yes (point-in-time) | float; clipped at whole-file 5th/95th pct (507 at 1,438.3, 508 at 34,516) | weak transductive leak, kept by the curator 2026-10-19 | LEAK-30 |
| Total_Revolving_Bal | revolving balance | point-in-time; whether at snapshot or at closure is not stated | int 0-2,517; top-clipped (508 at 2,517); 2,470 zeros, attrited 0.362 | maybe-leak (a closed account is paid down to 0) plus LEAK-30 clip; drop of the three balance columns costs 0.002 AUC (0.9937 to 0.9917) | LEAK-10, LEAK-30 |
| Avg_Open_To_Buy | "average open to buy, last 12 months" | as Credit_Limit | float; equals Credit_Limit - Total_Revolving_Bal in every row (max diff 6e-14); max 34,516 = the clip | fine to keep; not an average, inherits both clips, which the clipping note does not name | CLEAN-5 (not an exact copy), LEAK-30 |
| Total_Amt_Chng_Q4_Q1 | Q4 over Q1 transaction amount | window timing unknown | float 0-3.397; 0 in 5 rows, all attrited | maybe-leak (same mechanism as the count) | LEAK-10 |
| Total_Trans_Amt | transaction amount, last 12 months | window timing unknown | int 510-18,484 | strongest single feature (0.876); class-specific clusters: 3,000-5,000 holds 4,256 existing vs 87 attrited, 6,000-7,000 holds 8 vs 17, 10,000-12,000 1 vs 10, >12,000 746 vs 0 (pure value, probe 4 threshold met) | PROV-3, SEL-16; LEAK-10 |
| Total_Trans_Ct | transaction count, last 12 months | window timing unknown | int 10-139 | equals the Q4 plus the Q1 count in all 10,127 rows (ratio matches within rounding 0.0005), so it is not a 12-month count; >100: 649 rows, 0 attrited | PROV-3; LEAK-10 |
| Total_Ct_Chng_Q4_Q1 | Q4 over Q1 transaction count | window timing unknown | float 0-3.714; 0 in 7 rows, all attrited | maybe-leak; see the Q1 test below | LEAK-10 |
| Avg_Utilization_Ratio | "average card utilization ratio" | as the balance | float 0-0.999; equals Total_Revolving_Bal / Credit_Limit to 3 decimals in every row | fine to keep; not an average, inherits the clips | CLEAN-5, LEAK-30 |

No missing values, no impossible values (balance never above limit; tenure never above (age - 18) x 12), no untyped
object column (CLEAN-9), no constant column. The raw file is sorted roughly by Total_Trans_Amt (decile medians 1,420 to
14,212; position AUC 0.608); the container shuffles (CLEAN-23), so no action.

**The decisive window test (new)**

Splitting Total_Trans_Ct into its Q1 and Q4 counts (Q1 = Ct / (1 + ratio)): medians existing / attrited Q1 41 / 29,
Q4 29 / 14. Q1 alone AUC 0.819, Q4 alone 0.819, the 12-month count 0.835. Profile + Credit_Limit + Q1 count only:
0.895 (all features 0.994). So the attrited customers already transacted less in the oldest quarter of the window; the
separation is not only a collapse at the closing. Whatever the closure timing, a large part of the signal sits in
values 9-12 months back. The pure tails (Contacts 6, zero Q4) are the part that looks like the closing itself, and they
are 61 rows. Circumstantial, not proof either way (EV-6).

**Problems, ranked (principles.md)**

1. **P2/P5, SEL-16 and PROV-3 (Must if confirmed): marks of generated data, now with a class-conditional one.** Beyond
   the marks already in the definition (Ct = Q4 + Q1 in 10,127/10,127; tenure follows age; no woman above $60K),
   Total_Trans_Amt is a mixture of clusters whose class mix flips from bin to bin (3,000-5,000: 98% existing;
   6,000-7,000: 68% attrited; >12,000: 100% existing over 746 rows). PROV-3 test 5 (class-conditional generation) and
   test 6 (structure the world would show) point the same way; `generated_probes` found no flag, and it does not test
   per-bin class flips. Remedy: none by cleaning; it is the curator's call between keep with the note (current) and
   `No` + `AHDS` (the 2026-10-07 assessment). Question for the curator. Suggest adding the amount-bin numbers to the
   first decision so the evidence is complete.
2. **P4, LEAK-10 (Must if strong; currently a maybe): the activity window may end at the closure.** Evidence for:
   Contacts 6 (54 rows), zero Q4 count (7), zero Q4 amount (5) are all attrited; balance 0 in 55% of attrited vs 19%
   of existing (rows at 0: 36% attrited). Evidence against a strong leak: Q1 count alone 0.819 = Q4 alone; inactive months show no post-closure
   pile-up; drop-one tests barely move (Contacts+Inactive 0.9937 to 0.9925; the three balance columns to 0.9917).
   Mildest remedy: keep with the existing `Potential leak, kept on purpose` note (in place). Consistency: iranian_churn
   was retired only once its paper confirmed the window ends at churn (LEAK-3, LEAK-10 Cases); here nothing confirms
   it, so keeping is consistent. Suggest adding the Q1-count result to the note as the evidence the signal predates the
   closing.
3. **P4, LEAK-30 (Should, weak): clipping at whole-file percentiles.** Curator kept it on 2026-10-19; consistent. Small
   documentation gap: Avg_Open_To_Buy (max 34,516) and Avg_Utilization_Ratio are computed from the clipped values, so
   they carry the clip too; the bullet names only Credit_Limit and Total_Revolving_Bal. Remedy: one clause in the note.
4. **P7, CLEAN-10 (Should): Months_on_book = 36 as a probable fill.** Kept with a note; true 36s cannot be told apart
   and the 36s are not outcome-related (attrited 0.175). Fine as is; an alternative is a NaN for 36 (loses the true
   36s). No change recommended.
5. **P7, CLEAN-14 (Should, optional): ordinal categories stored unordered** (Income_Category, Card_Category,
   Education_Level). The categories carry their labels, so meaning is not lost; ordering is optional and Unknown has no
   place in the order. No change needed.

Fine with no action: the two NB columns and CLIENTNUM dropped (LEAK-27, CLEAN-3); the Unknown categories (documented,
not outcome-driven); Avg_Open_To_Buy and Avg_Utilization_Ratio kept as published (derived, not exact copies; CLEAN-5).

</details>

<details><summary>Split audit</summary>

**Split audit: credit_card_customers (2026-10-20, re-check)**

Verdict: **right with notes.** The IID split stays; the definition misses the SPLIT-8 tag and wording.

Model: LightGBM, 400 trees, all 19 features.

**What was checked**

* Declared: IID, 3 repeats x 3 folds, no grouping, no time column. Folds are disjoint, every repeat covers all 10,127
  rows, test sizes 3,375-3,376, attrited share 0.1605-0.1608 in every fold (stratified).
* Use case: at a snapshot date the bank scores its customers for closing the card account. A known entity
  (USE-10), but the release holds one row per customer and no earlier outcome, so there is no history to use; a
  random split over customers of one snapshot is the closest the data allows (USE-11).
* Defined splits: ROC AUC 0.9938 (0.9899-0.9955).

**Problems, ranked**

1. **P4, SPLIT-8 (Must; narrows SPLIT-7): temporal in nature, shipped IID without the tag.** The deployed model trains
   on one snapshot (customers whose closing is already known) and scores the next; the release has no dates and no
   second snapshot. SPLIT-8 asks for IID tagged forced IID from temporal, with the cost of the missing time axis
   measured where the data allows. The definition has `data_tags = ("2ndTierData",)` and `split` = "Random customers
   of the same snapshot". The cost cannot be measured: the raw file order is a sort on `Total_Trans_Amt` (Spearman
   0.82 with the row number; `Total_Trans_Ct` 0.68; age, tenure, limit within +-0.03), so a hold-out by file order
   measures extrapolation on a feature, not time (thirds 0.8876, train first 2/3 -> last 1/3 0.8185, 10 blocks
   0.9687; attrition by file decile 0.05-0.25). `CLIENTNUM` is no time proxy either: thirds by `CLIENTNUM` 0.9932,
   the same as random. A tenure cohort hold-out (train > 30 months, test <= 30, 2,220 rows) gives 0.9905.
   Remedy (mildest): add `ForcedIIDFromTemporal` to `data_tags`; reword `split` and the IID bullet of
   `curation_comments` to say the split is forced (a model trained on one snapshot scoring the next, a gap of the
   label horizon), that the cost cannot be measured (file order is a sort on `Total_Trans_Amt`, CLIENTNUM thirds
   0.993), and that dates should be recovered if the LEAPS material turns up. No re-split. Precedent:
   expresso_churn_prediction_1m (tagged, same wording), account_debt_south_africa. Note for the precedent checker:
   bank_customer_churn, churn_telco_south_asia, mobile_churn, tour_travels_churn and rosbank1 are untagged churn
   snapshots too.
2. **P4, cross-reference to LEAK (not a split fix).** The gap a temporal split would carry against the label delay
   cannot be set: when the closing happened relative to the 12-month window is unknown (the definition's first
   potential-leak note). That is the leak auditor's question; no split change resolves it.

**Rules that hold**

* SPLIT-29 / SPLIT-30: no hidden groups. `CLIENTNUM` unique for all 10,127 rows, 0 exact duplicate feature rows, 0
  near copies at similarity 0.85; the hidden-group probe has no hit (largest gap +0.002 on `Months_on_book`, fold sd
  0.003; composite keys: none of 190).
* SPLIT-24 / SPLIT-4: no group id exists; no column names an entity new data would lack.
* SPLIT-3, USE-10, USE-11: one regime; one row per customer, no history; IID over customers fits the data as shipped.

Judgment: Validity: SPLIT-1 holds (IID is the closest available); SPLIT-8 triggered, fix = tag and wording;
SPLIT-29 holds.

</details>

<details><summary>Domain practitioner</summary>

**Domain practitioner: credit_card_customers (2026-10-20)**

Actor: the retention analytics team of a card issuer that, once a month, scores every open card account for the risk
of voluntary closure in the next months and hands the top of the list to relationship managers or a retention offer
campaign (USE-1).

**Fit: approximate**

The rows and the inputs are the kind I score every month, but the label has no stated horizon and its timing relative
to the 12-month activity window is unknown, so the task may be "recognise a closing account" rather than "foresee one"
(USE-8, approximate: a potential leak kept on purpose plus a label without a stated horizon). The definition's
`fit="approximate"` is right; I would not call it direct under USE-9: no other well-defined use case fits a random
split of undated customers whose activity may run up to the closure.

**The four questions, as the actor**

1. **Inputs at the prediction point (USE-3, USE-6).** Profile (age, gender, dependents, education, marital status,
   income band, card type, tenure, product count) and 12 months of card activity: yes, I have all of these on any
   scoring date, with the caveat that education and income come from the application and go stale. What I would not
   have: activity that already reflects the closure. If the window ends at the closure, the zero Q4 transactions
   (7 customers, all attrited), the 6 contacts in 12 months (54, all attrited; the closing call is itself a contact)
   and the revolving balance of 0 (55% of attrited vs 19%: a customer pays off before closing) are partly the closing
   itself (LEAK-10 via USE-3). What I always have and is missing: month-by-month activity rather than one Q4/Q1 ratio,
   payment and delinquency history, fees, interest rate and APR changes, rewards redemption, recent credit limit
   changes, competitor balance transfers seen in bureau data, complaints, digital channel use, and the scoring date.
   Their absence makes the task weaker, not wrong.
2. **Target (USE-5).** I act on "will this customer ask to close the card in the next 3 to 6 months" (voluntary
   attrition, a performance window after the observation window). Attrition_Flag is "the account is closed", with no
   horizon and no split between voluntary closures and issuer closures (charge-off, fraud, inactivity), which in
   industry numbers are about half of gross attrition. So it is a proxy. I want a probability (ROC AUC fits: I rank
   and work the top deciles under a contact budget); a class is not what I use.
3. **Row and test data (USE-10, USE-11).** One row per customer at one snapshot matches one scoring decision. But my
   test is next month's book of existing customers, scored with a model trained on earlier months: a temporal
   out-of-time test. The random split of one undated snapshot is the only option here (no dates), and is what the
   USE-8 "one snapshot stands in for a forecast" pattern names. The entity is known (my own customers), so in reality
   their earlier scores and outcomes would be features; here each customer appears once.
4. **Would I use this model?** Not as is. An AUC of 0.98 to 0.994, with 0.98 from the six activity columns alone, is
   what I would expect from a label that leaks the closing, not from a retention model; real attrition models of
   issuers sit far lower, and I would distrust it at once and ask when the closure happened relative to the window. The
   marks of generated data (Q4+Q1 counts adding to the 12-month count in every row, tenure tracking age, no woman above
   $60K, clustered amounts, 24% of tenure at 36) tell me this is a teaching case, not a book of accounts. I would
   trust it only with an observation window that ends before a stated performance window and a source I can trace.

**Gaps between the dataset and the real decision, ranked by how much they change the task**

1. **Label timing (USE-3, USE-5, USE-8).** No horizon and possibly a window ending at the closure: the task may be
   detection, not prediction. This decides the near-ceiling score and changes the task most.
2. **Data origin.** Likely constructed teaching data from an untraceable, offline source; the joint distribution of
   the activity columns is not that of real card books, so the benchmark measures how models fit the generator.
3. **Split (USE-10, SPLIT-3).** Random over one snapshot instead of out-of-time; acceptable as approximate, cannot be
   fixed without dates.
4. **Target definition (USE-5).** Voluntary and involuntary closure mixed; cannot be fixed from the file.
5. **Missing inputs.** Monthly activity, payment and pricing history; makes the task easier to game by the summary
   columns but does not change its nature.
6. **Derived and clipped columns.** Avg_Open_To_Buy and Avg_Utilization_Ratio are point-in-time derivations of
   Credit_Limit and the balance, not 12-month averages; clipping of Credit_Limit at file percentiles. Small.

**What an expert would change**

* Rebuild the task with an observation window that ends one month before a stated performance window (e.g. closure in
  the next 6 months), voluntary closures only, out-of-time test. Not possible from this file; it is the reason to look
  for a real issuer dataset to replace it (e.g. a public bank churn table with dated snapshots).
* As a stress test of the leak, not a change to ship: score on the 10 profile columns plus the Q1-only and pre-Q4
  information (drop Total_Ct_Chng_Q4_Q1, Total_Amt_Chng_Q4_Q1, Contacts_Count_12_mon, Total_Revolving_Bal); if the AUC
  falls toward the 0.6 to 0.8 range real attrition models report, the activity columns carry the closing. LEAK-*
  rules and USE-12 decide the remedy: the use case is real, so a leak alone is no reason to reject.
* My recommendation as the actor: the use case is real and common (USE-1 holds; USE-2 does not apply), but this file
  is a weak stand-in for it. Keep `fit="approximate"` and the honest fit_reason; whether the generated-data marks plus
  an untraceable source warrant `No` is the curator's call, not a use-case question. I would weigh it toward not
  shipping, or shipping with a low weight, since the near-ceiling AUC leaves little room to rank methods.

**Rules cited**

USE-1, USE-2, USE-3 (with LEAK-10), USE-5, USE-6, USE-8, USE-9, USE-10, USE-11, USE-12; SPLIT-3.

**Sources**

* `datasets/_dev/tabarena-v0pt2/credit_card_customers/dataset.py` (task_summary, curation_comments)
* `curation/records/credit_card_customers.md`
* `.claude/skills/knowledge-curation/references/use_case.md`
* Observation and performance windows in bank attrition models: https://www.listendata.com/2016/08/observation-and-performance-window.html
* Daily attrition scoring of card accounts (Fahner, FICO): https://cer.business-school.ed.ac.uk/wp-content/uploads/sites/55/2017/02/Stochastic-Gradient-Boosting-Approach-to-Daily-Attrition-Scoring-Based-on-High-Dimensional-RFM-Features-Gerald-Fahner.pdf
* Visa Consulting & Analytics, cardholder retention: https://navigate.visa.com/$/v/5/cemea/m/x/11176 VCA Investing in Cardholder Retention Paper_S7.pdf
* Voluntary vs involuntary card attrition (R.K. Hammer figures): https://www.cuinsight.com/?p=22634

</details>

<details><summary>Blind review</summary>

**Blind review: credit_card_customers (BankChurners)**

**Verdict: include with changes. It is a widely used churn table that is cleanly prepared, but its timing is not documented, its origin is unverified and it scores near the ceiling (LightGBM ROC AUC 0.993). Flag it as a weak, low-headroom dataset, or exclude it if the benchmark needs real data with a known timing.**

**Task**
A card issuer wants to predict which customers will close their accounts, so it can target them with retention offers. That is a real use. Target: Attrition_Flag, with 1,627 "Attrited" out of 10,127 (16.1%).

**Concerns (most serious first)**
1. **The activity features may be measured at the same time as the churn, or after it.** Total_Trans_Ct, Total_Trans_Amt, Total_Ct_Chng_Q4_Q1, Total_Amt_Chng_Q4_Q1 and Months_Inactive_12_mon cover the last 12 months or the Q4-versus-Q1 change. No snapshot date or outcome window is given, so a customer who already left would show a drop in Q4 activity as a result of leaving. Each of these columns is strong on its own (single-feature LightGBM AUC: Trans_Amt 0.876, Trans_Ct 0.834, Ct_Chng 0.751), and all features together reach AUC 0.993. A model like this may be detecting churn that has already happened rather than predicting it.
   *Change:* document it as "concurrent behaviour", or run a variant without the Q4 and 12-month activity columns.
2. **The origin is unverified and the data may be simulated.** The Kaggle uploader credits the Analyttica LEAPS teaching platform. There is no bank, date or collection method, and no primary source says whether the data is real. Credit_Limit has two point masses: 34,516 (508 rows) and 1,438.3 (507 rows). These look like a cap and a floor, which fits either policy limits or a generator. *Change:* label the provenance as "unverified".
3. **There is little room between methods.** At AUC 0.993, strong tabular methods will all score close together. It is still usable with log loss, but it separates methods poorly.
4. **One column is an exact function of two others.** Avg_Open_To_Buy = Credit_Limit - Total_Revolving_Bal holds exactly (0% of rows deviate). This is harmless but adds no information.

**Preparation (fine)**
CLIENTNUM and the two leaked Naive_Bayes_Classifier_* columns from the source file are removed. There are no NaNs and no duplicate rows. "Unknown" is kept as a category level in Education, Marital status and Income, which is reasonable. Income_Category is ordinal but stored as an unordered category, which is acceptable. A random IID split matches the source, since there are no IDs or dates to group by.

**Not checked**
The Kaggle page did not render, so I could not quote the text. I also could not check the true snapshot and outcome timing, or whether the data is real.

Sources: https://www.kaggle.com/datasets/sakshigoyal7/credit-card-customers ; https://zenodo.org/record/4322342 ; https://nycdatascience.com/blog/student-works/analyzing-data-to-predict-credit-card-churner

</details>

<details><summary>Precedent check</summary>

**Precedents: credit_card_customers (re-check, 2026-10-20)**

Inputs:
- the register of past decisions
- the open issues of the earlier review file
- the record: `curation/records/credit_card_customers.md`
- the knowledge files' Cases tables: `provenance.md`, `selection.md`, `task_probes.md`, `cleaning_features.md`, `principles.md` (Tensions)
- the sibling records

The register's flags about this dataset:
- **Drift, "scaling over all rows".** This one involves credit_card_customers' 2026-10-19 keep. Section D4 below covers it.
- **The "generated data" and "Missing source information" groups.** These are where the precedents below come from.

**D1. Issue 1: the data looks constructed (PROV-3 / SEL-16, both Must; marker AHDS)**

**Current state.** The folder stays and carries `data_tags = ("2ndTierData",)`. The AI recommends `No` + `AHDS` + `Missing source information`. You have not decided after the evidence came out on 2026-10-07. Your only source comment is from screening and comes before that evidence.

**Precedents.** Every dataset you retired as generated had a source statement or a written-down mechanism:

| Dataset | Date | What settled it |
|---|---|---|
| ecommerce_shipping | 2026-10-01 | test 2: `Warehouse_block` is the id mod 6, `Mode_of_Shipment` a 137-id cycle (mechanism) |
| customer_satisfaction_in_airline | 2026-10-01 | tests 1, 3, 6: ratings copied within segments, labels flipped by a rule (mechanism) |
| homeq_default_prediction | 2026-09-24 | test 5: the classes were generated differently (mechanism) |
| video_game_fps_prediction | 2026-09-29 | test 7: a lookup formula (generator) |
| churn | 2026-10-06 | MLC++ calls it "artificial" (source statement); probe flag `rule_leaves` |
| healthcare_insurance_expenses | 2026-10-06 | the generator was recovered |
| corporate_credit_rating_..._duplicate | 2026-10-12 | a simulated copy of the book's rows (source) |

These are in `.claude/skills/knowledge-curation/references/provenance.md` (Cases, PROV-3) and `task_probes.md` (Generated data). `evidence.md` (around line 64) adds: "a generated-data mark needs what the source says and, where possible, the generator written down."

**This case.**
- The evidence is PROV-3 tests 4 and 6, calibrated against real tables (Home Credit, Taiwan): constant-sum counts, independence where the world shows dependence, a tenure band set by age, no woman above $60K.
- It includes one partial mechanism: the 12-month count equals Q4 + Q1 in all 10,127 rows.
- There is no source statement. The LEAPS "dummy dataset" remark is about another case, so it is circumstantial.
- There is no full generator, and `generated_probes` raises no flag.

**Open cases of the same kind, to decide alike** (all undecided: suggestion still `Yes`, no CC):
- **hepatitis_c_egypt** (AI assessments of 2026-10-07 and 2026-10-20): independent columns, AI recommends No + AHDS. It was not added.
- **stroke_prediction** (same dates): partly generated or altered, AI recommends No + AHDS / Data Quality Issue. The folder exists.
- **framingham_heart_study_fhs**: an open review (2026-10-20) of teaching data with values permuted by the owner, also a PROV-3 question.

**Correction to the earlier review file.** Its alternative says "retire ... as for ecommerce_shipping, customer_satisfaction_in_airline, churn, and in this run stroke_prediction and hepatitis_c_egypt". The last two are AI recommendations, not decisions, so they are not precedents.

**About the `2ndTierData` tag.**
- the earlier review file lists it under "Implemented". It actually came from the v1 migration (`git log -S`: first in 2475ea2; `datasets/_dev/tabarena-v0pt2/framingham_heart_study_fhs/REVIEW.md` lines 745-747 already notes this).
- No knowledge file defines it. Only `src/data_foundry/schema.py:96` does: "not of the highest quality but still a reasonable task".
- The only other dataset with the tag is coffee_rating_prediction.
- Tagging is not a remedy for a Must. "Ship as 2nd tier with generated-data marks" would be an amendment to PROV-3, not something a precedent supports.
- The nearest similar call: gym_customers_features_and_churn, screening, undated: "too likely that it is fake", no source → `TBD -> 2nd Tier`.

**Verdict.**
- Pending, no departure yet.
- If you keep it: departs from PROV-3 (Must) with no stated fact, so it is not reasonable under the ranking. The only legitimate route is to reject the evidence on facts: say the marks don't prove generation, as first_principles_tully_fisher was judged "real measurements, so not AHDS" (2026-10-20). That is a finding, not an exception.
- If you retire it: consistent with PROV-3 and its retired cases, but on a weaker kind of evidence than any of them. Record which test settled it, and decide hepatitis_c_egypt and stroke_prediction the same way.

```text
**Consistency check (AI, 2026-10-20):** keeping credit_card_customers (measured PROV-3 marks: Total_Trans_Ct = Q1 + Q4
in 10,127/10,127 rows, inactivity and spend independent of activity, a tenure band set by age) would differ from
ecommerce_shipping and customer_satisfaction_in_airline (retired 2026-10-01, AHDS + Missing source information, the
same pattern: untraceable source plus constructed columns). What sets it apart?
(a) no source statement and no full generator, unlike every retired PROV-3 case, so the marks are judged
circumstantial (a finding on the evidence, recorded with the test that would settle it; hepatitis_c_egypt and
stroke_prediction then get the same standard); (b) treat it like ecommerce_shipping: No (Retired), AHDS + Missing
source information; (c) reopen the retired cases to match (not suggested: they rest on mechanisms); (d) amend PROV-3 /
evidence.md to state what evidence suffices without a source statement (e.g. two calibrated PROV-3 tests), or define
`2ndTierData` as the place for data with unproven generated marks.
```

**D2. Issue 3: the source is an untraceable teaching case (PROV-1 Must, PROV-2 Should)**

**Your decision.** Screening comment, undated, from before the v2 audit: "We have no real source information, but I think it is good to use for now. We can filter later". the earlier review file treats it as accepted, so the dataset was added.

**Precedents that keep it:**
- **bank_customer_churn** (shipped in TabArena v0.1; workbook comments: "Given the heavy usage of this data from this course, we keep the data source as is", "Lennart: No objection", Andrej: "Licence & data source unclear"; licence CC 2026-10-14). The closest sibling: a bank churn table, course origin, no bank or period named.
- **tour_travels_churn** (undated): "We are missing some information, but it seems reasonable".
- **bad_customer_detection** (PROV-2 case, 2026-10-14, Lennart): "a plausible source unclear in a detail: kept, with a note".

**Precedents that exclude:**
- **PROV-1 cases** (water_quality_and_potability, 3d_estimation_using_rssi_..., calendardow): every link ends at an anonymous re-upload → No.
- **Screening calls on course or teaching churn data that looked fake** (undated):
  - customer_churn_dataset ("Looks super artificial", educational source) → No
  - predictive_analytics_for_customer_churn_dataset (Coursera, "looks fake") → No
  - ibm_telco_customer_churn ("Sample data set, not real") → No
  - gym_customers_features_and_churn → `TBD -> 2nd Tier`

**Comparison.**
- On the source alone, it follows bank_customer_churn. The fact that sets it apart from the PROV-1 cases: the first uploader names an upstream (Analyttica's LEAPS, case 11), and PROV-1 counts "an identifiable first uploader" as traceable.
- But the same-family precedents split on whether the data also looks fake. bank_customer_churn had no such marks (one uniform column, `estimated_salary`, which task_probes.md lists as ordinary). credit_card_customers now has measured marks.
- So course origin plus fakeness signs has gone to `No` three times and to `2nd Tier` once. credit_card_customers is still in the folder.
- That is a real pair decided differently, but your keep predates the evidence. The precedence table says "a later stage's measured finding supersedes an earlier stage's reading", so the screening keep needs to be confirmed or revised.

**Third keep under PROV-1.** bank_customer_churn, tour_travels_churn and credit_card_customers (mobile_churn is open on the same question) all keep a dataset whose source cannot be traced. PROV-1 is a Must, which allows no exceptions. Per principles.md, "Exceptions and amendments", an amendment is due, for example: PROV-2 widened to "a named first platform (a course or teaching provider) counts as a known source when the data shows no PROV-3 marks".

**Smaller inconsistency.** The definition has `source = "Other"` and the record has `original_source: Company` (checklist P5). bank_customer_churn uses `source = "Kaggle"`.

**Verdict.** Departs without a stated reason (it was a screening-era keep), and is not reasonable under the ranking as an exception to a Must.

```text
**Consistency check (AI, 2026-10-20):** your call on credit_card_customers (keep with no traceable source, a departure
from PROV-1) matches bank_customer_churn and tour_travels_churn but differs from customer_churn_dataset,
predictive_analytics_for_customer_churn_dataset and ibm_telco_customer_churn (No: course or teaching churn data that
looks generated). It is the third keep of an untraceable course dataset under a Must. What sets it apart?
(a) the Kaggle uploader names the upstream (Analyttica LEAPS case 11), an identifiable first platform, so PROV-2
applies; recorded only if issue 1 is settled as "not generated"; (b) treat it like customer_churn_dataset: No +
Missing source information (+ AHDS); (c) reopen bank_customer_churn and tour_travels_churn to match; (d) amend PROV-1/
PROV-2 so a named teaching or course platform with no PROV-3 marks counts as a known source (third case: amendment due).
```

**D3. Issue 2: the window may end at the account closure (USE-3, LEAK-10 to LEAK-12, LEAK-22 to LEAK-26)**

**Current handling.** Kept with a "Potential leak, kept on purpose" bullet and a revisit condition.

**Precedents:**
- **churn_telco_south_asia** (CC 2026-10-15, Lennart): neither paper dates the churn; kept "although the task may be problematic", stated as a potential leak kept on purpose, "revisit if the churn can be dated". This is the Tensions row "A real task against imperfect cleaning".
- **iranian_churn** (CC 2026-10-01, retired, Data Quality Issue): the paper states the window ends at the churn month (Keramati & Ardabili 2011, Sec. 4.1).

**Comparison.** This case follows churn_telco_south_asia: no source statement, so keep with a note. One difference to state, not a departure: the circumstantial signal here is much stronger than in south_asia.

| | credit_card_customers | churn_telco_south_asia | iranian_churn |
|---|---|---|---|
| AUC | activity block 0.980, all columns 0.994 | 0.815 | 0.986 |
| Other signs | all 7 zero-Q4 customers and all 54 with 6 contacts attrited | | |

So the facts sit closer to iranian_churn, but they do not meet its stated basis (a source statement).

Not dropping the activity block follows the Tensions row "A better version against our own fix" (eryhemato) and task_probes rule 6.

**Verdict.** Consistent (churn_telco_south_asia, 2026-10-15).

**D4. Clipping of Credit_Limit and Total_Revolving_Bal at whole-file percentiles (LEAK-30)**

**Your decision.** CC 2026-10-19, keep with a note.

**The register's drift flag.** It pairs coad_colon_adenocarcinoma (retired 2026-10-16) with seven keeps on 2026-10-19, this one included. This is not drift for this dataset:
- The Tensions row was set deliberately on 2026-10-19: "keep with a note; a strong suspected leak makes it `No`; fix it when we can".
- coad's origin can be rebuilt (it was rebuilt, 2026-10-19). credit_card_customers has no origin to rebuild from.

**Verdict.** Consistent (bioresponse, taiwanese_bankruptcy_prediction, cooking_time and others, all 2026-10-19).

**D5. Issue 4: Months_on_book = 36 and "Unknown" kept as published (CLEAN-10, CLEAN-11)**

- **The 36s.** CLEAN-10 converts proxy codes only "when the encoding can be inferred". About 340 true 36s cannot be told apart from the filled ones, so keeping them with an Anomaly note follows the rule. No case in the Cases tables has a filled value that looks like a real one.
- **"Unknown".** It stays a category because the data card lists it as a value. pva_revenue_prediction_kddcup98 maps "U" to "Unknown" the same way (`datasets/_dev/tabarena-v0pt2/pva_revenue_prediction_kddcup98/dataset.py` lines 413 and 420).

**Verdict.** Consistent.

**D6. Near the ceiling (TP-1, `solved`)**

The task-probe flags are not triggered, so there is no decision to compare yet. If tuned runs trip `solved`, the precedents are:
- anneal: retired, Trivial (2026-07-27)
- aps_failure: kept after a TP-1 check (2026-10-06)

A ceiling score alone does not justify retirement (evidence.md, EV-3).

**Amendments due**

1. **PROV-1/PROV-2.** Third keep of an untraceable course-sourced dataset under a Must (D2).
2. **PROV-3 / evidence.md.** No stated standard for calibrated marks without a source statement or generator. Settle it once, for credit_card_customers, hepatitis_c_egypt, stroke_prediction and framingham_heart_study_fhs together (D1).
3. **`2ndTierData`.** Used as a decision but defined in no knowledge file (D1).

**Files**

- curation/records/credit_card_customers.md
- curation/records/bank_customer_churn.md
- curation/records/churn_telco_south_asia.md
- curation/records/iranian_churn.md
- curation/records/ecommerce_shipping.md
- curation/records/customer_churn_dataset.md
- curation/records/gym_customers_features_and_churn.md
- .claude/skills/knowledge-curation/references/provenance.md
- .claude/skills/knowledge-curation/references/evidence.md
- datasets/_dev/tabarena-v0pt2/framingham_heart_study_fhs/REVIEW.md

</details>

<details><summary>Advocate</summary>

**Advocate: credit_card_customers (opening brief, 2026-10-20)**

Position: **ship with the mildest fixes.** Keep the task, the 19 features and the IID 3x3 split. Add the SPLIT-8 tag and correct some wording. Nothing is dropped, nothing is re-split, nothing is retired.

**1. The possible closure-window leak is handled at the right level: kept with a note, and the signal comes before the closing (P4; LEAK-10 Must, LEAK-11 Should narrows LEAK-10, USE-12 Must)**

- **Evidence.**
  - Column audit, "The decisive window test": the Q1 count alone gives AUC 0.819 and the Q4 count alone 0.819.
  - Profile + Credit_Limit + the Q1 count alone gives 0.895. That count covers 9-12 months back.
  - So attrited customers already transacted less in the oldest quarter of the window (median Q1 count 29 vs 41).
  - The rows that look like the closing itself are 61: Contacts = 6 (54 rows) and zero Q4 (7 rows).
  - Drop-one tests barely move the score: contacts + inactive months 0.9937 to 0.9925; the three balance columns 0.9937 to 0.9917.
  - Inactive months show no pile-up after the closure (6 months is 1.2% in both classes).
  - The median Q4/Q1 ratio of attrited customers is 0.53 (claim 22, holds). So the window does not run months past the closure.
- **Precedents.**
  - churn_telco_south_asia (curator comment, 2026-10-15): no date for the churn, kept as "Potential leak, kept on purpose" with a condition to revisit. That is this exact handling.
  - iranian_churn was retired only because its paper states the window ends at the churn. Nothing here states that (Kaggle topic 203290 is unanswered).
- **Why it outranks the objection.**
  - USE-12: a leak is no reason to reject a task whose use case is real. The practitioner confirms USE-1 holds.
  - LEAK-10 is a Must only for a leak that is shown. Here it is "maybe a leak" (EV-6). The measured part that would weaken the signal, if it is post-closure, is small. That is LEAK-11, kept with a note.
  - Dropping the activity block would be a fix of our own invention (task_probes rule 6; the Tensions row with eryhemato). It would also remove the 9-12-month signal that the use case asks for.
  - Remedy ladder: "keep with a documented note" is already in place.
  - **Cheap fix:** add the Q1-only numbers (0.819, and 0.895 with the profile) to the leak bullet, as evidence that the signal comes before the closing.

**2. The split is right; the only gap is a missing tag (P4; SPLIT-8 Must, SPLIT-1, SPLIT-29/30)**

- **Evidence (split audit).**
  - One row per customer: CLIENTNUM is unique, there are 0 duplicate feature rows and 0% near copies, and the hidden-group probe has no hit.
  - Folds are stratified (16.05-16.08% attrited).
- **Concession.** SPLIT-8 is triggered: this is a churn snapshot standing in for a forecast.
- **The mildest fix.**
  - Add `ForcedIIDFromTemporal` to `data_tags`.
  - Reword `split` and the IID bullet: the split is forced, and its cost cannot be measured. The file order is a sort on Total_Trans_Amt (Spearman 0.82), and splitting into thirds by CLIENTNUM gives 0.993, the same as random.
  - Precedents: account_debt_south_africa and expresso_churn_prediction_1m.
- **Why this is enough.** SPLIT-8 is itself the remedy SPLIT-7 prescribes when no dates exist: ship IID with the tag. No re-split is possible or needed.

**3. "Generated" is not established to the standard PROV-3 has been held to (P2/P5; PROV-3 and SEL-16 Must, read with EV-3 Must, EV-6 Should, EV-9 Should)**

- **What I concede (EV-1, facts first).** The marks are real and reproduced:
  - Total_Trans_Ct = Q4 + Q1 in all 10,127 rows;
  - tenure tracks age (slope 1.006, r 0.893);
  - 0 of 5,358 women have an income above $60K;
  - the Total_Trans_Amt clusters flip class mix from bin to bin;
  - inactivity is unrelated to the transaction count (Spearman -0.05, against -0.60 on Home Credit).
- **What has not been shown.**
  - EV-3: "a generated-data mark needs what the source says and, where possible, the generator written down." There is no source statement. The LEAPS "dummy dataset" remark is about another case and is untested (claim 43).
  - There is no generator written down, and `generated_probes` raises no flag (0 rule leaves).
  - EV-6: a generator written down settles it; the marks without one are circumstantial.
  - Every PROV-3 retirement in the Cases table rested on a mechanism or a source statement (precedents D1): ecommerce_shipping (id mod 6), customer_satisfaction_in_airline (labels flipped by a rule), homeq (near-copy clusters pure in the label, AUC 0.92), video_game_fps (R² 0.99998 formula), churn ("artificial" per MLC++).
- **The marks have other readings.**
  - The Q4 + Q1 identity fits a teaching-case author deriving the summary columns from half-years. That is a reworked column, not proof the rows are drawn from a generator.
  - Tenure bounded by age is a product-eligibility pattern a real portfolio can show.
  - The column audit itself grades this "Must if confirmed".
- **Why it outranks the objection.**
  - Retiring on circumstantial marks would depart from the PROV-3 precedents, which needed a mechanism, with no fact that sets this case apart.
  - Treat like cases alike: hepatitis_c_egypt, stroke_prediction and framingham are open on the same kind of evidence and have to be decided the same way.
  - The honest state is "maybe generated", with the test that would settle it: the LEAPS case material, or a written-down generator. That goes to the curator (EV-6). The definition already says so in `fit_reason`, in the Anomaly bullet and in decision 1.
- **Cheap fix:** add the amount-bin class mix (3,000-5,000: 98% existing; above 12,000: 746 rows, 0 attrited) to decision 1, so the evidence is complete.
- **Further concession.** `2ndTierData` is not a remedy for a Must (precedents D1). If the curator judges the calibrated marks to be enough, that is a change to PROV-3/EV-3 (option d of the consistency check). It should not be a quiet keep.

**4. The source is traceable to a named first platform (P5; PROV-1 Must, PROV-2 Should narrows PROV-1)**

- **Evidence.**
  - PROV-1 counts "an identifiable first uploader" as a traceable upstream.
  - The trail ends at a named platform and case, not an anonymous re-upload: Analyttica LEAPS, sample case 11, dated 2020-04-19 (claim 13: offline, date untested).
  - The Kaggle uploader quotes the LEAPS URL (claim 16, verbatim).
  - The file is byte-identical on Zenodo (claim 14), pinned by sha256.
- **Precedents.**
  - bank_customer_churn: course origin, no bank named, shipped in v0.1.
  - tour_travels_churn.
  - bad_customer_detection (PROV-2, Lennart 2026-10-14): a plausible source that is unclear in a detail is kept with a note.
- **Why it outranks the objection.**
  - The water_quality, calendardow and 3d_estimation cases each end at an anonymous re-upload. This one does not.
  - The missing bank, country and period are a detail in the PROV-2 sense, and the definition states them as unknown.
- **Concessions.**
  - This is the third keep of this kind, so a PROV-1/PROV-2 clarification is due (precedents D2, option d).
  - The source field disagrees: `source = "Other"` in the definition, `original_source: Company` in the record. Align them (claim 48).

**5. The clipping at whole-file percentiles is a weak leak the curator has already kept (P4; LEAK-30 Should when weak)**

- **Evidence.** Credit_Limit has 507 rows at 1,438.3 and 508 at 34,516; Total_Revolving_Bal has 508 at 2,517 (claim 30, holds).
- **Decision and precedents.** The curator kept it on 2026-10-19, and the Tensions row was set the same day. The same call was made for bioresponse, taiwanese_bankruptcy_prediction and cooking_time. There is no origin to rebuild from, and the register's drift flag does not apply (D4).
- **Cheap fix:** one clause saying Avg_Open_To_Buy and Avg_Utilization_Ratio are computed from the clipped values and carry the clip.

**6. The task is worth benchmarking: no flag, and a ceiling score is no verdict (P6; TP-1 Must, TP-2 Should, EV-3 Must)**

- **Evidence.**
  - Task probe: skill +0.987, no flag. CatBoost default 0.9943, with 3 of 9 splits at or above 0.995 (claim 37, holds).
  - LightGBM log loss 0.075 leaves room on a second metric.
- **Rules.**
  - TP-1: a flag is checked against the tuned methods before anyone acts. Here no flag exists yet.
  - EV-3: a near-ceiling score alone is no verdict, and not a leak either.
  - Precedent: aps_failure, kept after a TP-1 check.
- **Concession.** Headroom is limited. If tuned runs trip `solved`, TP-1 decides then. That is not a reason to block it now.

**7. The remaining findings are wording, and fixing them is cheap and safe (P7; CLEAN rules, writing.md)**

- Claim 7: Total_Trans_Ct equals Q4 + Q1, so do not call it a plain 12-month count without that caveat.
- Claim 23: name the "10 profile columns" (re-measured as 0.601 or 0.629 depending on the set).
- Claim 28: "not missing at random" is shown for Income only.
- Add CLIENTNUM to `changes`.
- Mark the LEAPS date and the "dummy dataset" quote as unverified in the record (EV-7).
- Already consistent, no change: Months_on_book = 36 kept with a note, "Unknown" kept as a category, ordinal categories left unordered (precedents D5; column audit items 4-5).

**Judgment record (advocate)**

```text
Verdict: ship after changes (tag and wording only).
Validity: SEL-1 holds; USE-1 holds, USE-8 approximate (named gaps); LEAK-10 maybe, LEAK-11 kept with note (Q1-only
AUC 0.819 predates the closing); LEAK-30 weak, kept (curator 2026-10-19); SPLIT-8 triggered, fixed by the
ForcedIIDFromTemporal tag; SPLIT-29 holds; PROV-1 holds via a named first platform (PROV-2 note); PROV-3 not
established (no source statement, no generator, no probe flag: EV-3, EV-6).
Value: TP-1, no flag; near ceiling, log loss as a second metric.
Quality: wording fixes (claims 7, 23, 28; CLIENTNUM; clip clause; source field).
For the curator: whether the calibrated PROV-3 marks without a generator are enough to retire it (a change to PROV-3/EV-3,
to be decided alike for hepatitis_c_egypt, stroke_prediction, framingham_heart_study_fhs).
```

Files read:
- datasets/_dev/tabarena-v0pt2/credit_card_customers/dataset.py
- .claude/skills/knowledge-curation/references/principles.md (also provenance.md, evidence.md, leak_checks.md, splits.md, use_case.md, task_probes.md)
- the panel's reports (claim audit, column audit, split audit, practitioner, blind review, precedents, checklist) and the earlier review file

</details>

<details><summary>Critic</summary>

**Critic, opening brief: credit_card_customers (2026-10-20)**

Position: **do not ship** (point 1, a Must that no cleaning fixes). If the curator rejects point 1 on the facts, ship
only after the changes in points 3, 4 and 6, with point 2 settled by an amendment, not by silence.

**1. The data looks generated (P2/P5; SEL-16 Must, PROV-3 Must)**

* Problem: the joint distribution of the columns is not that of a card book. With no source to check against, the
  benchmark would score how well models fit a teaching-case generator. That is not a bank's churn task.
* Evidence (all reproduced on the raw file by claim_audit 29-35, 44-45 and checklist P2/P5):
  * Total_Trans_Ct = Q4 + Q1 count in 10,127/10,127 rows. A shuffled control gives 564-597 rows and Home Credit's real
    card statements 9 of 8,920. So Q1 and Q4 cannot be quarters of a 12-month window.
  * Some columns are independent where real tables are not. Inactive months vs count: Spearman -0.051, Home Credit
    -0.60. Spend vs limit: 0.028 vs 0.447. Education permutation discriminator: AUC 0.495 vs 0.58-0.61 on two real
    credit tables.
  * Tenure in months is set by age in years: never above age-4 in 7,664 rows, slope 1.006, r 0.893. No woman earns
    above $60K: 0 of 5,358, against 3,664 of 4,769 men.
  * New (column_audit, problem 1): the class mix of Total_Trans_Amt flips from bin to bin. 3,000-5,000 is 98%
    existing, 6,000-7,000 is 68% attrited, and above 12,000 sit 746 existing customers and no attriter. That is
    PROV-3 test 5 (class-conditional generation) on top of test 6.
* The case against this, stated fairly: there is no source statement and no full generator (evidence.md asks for them
  "where possible"), and `generated_probes` raises no flag (it does not test per-bin class flips). The source statement
  is not possible here: LEAPS is offline and not archived. The Q1+Q4 identity is a partial mechanism. Several
  calibrated tests point the same way, and a measurement outranks the missing page (EV-2).
* Remedy: `No (Retired)`, markers `AHDS` + `Missing source information`, following ecommerce_shipping and
  customer_satisfaction_in_airline. Cleaning cannot fix generated data, so exclusion is the mildest remedy that works.
  The only other legitimate route is a recorded finding, with the test that would settle it, that the marks do not
  show generation. hepatitis_c_egypt, stroke_prediction and framingham_heart_study_fhs must then get the same standard
  (precedents D1). `2ndTierData` is not a remedy: no knowledge file defines it, and a tag cannot carry a Must (precedents D1).

**2. The source is kept under a Must on a screening-era call (P5; PROV-1 Must, PROV-2 Should)**

* Problem: the trail ends at LEAPS case 11, whose material is gone. No bank, country or period is named anywhere
  (claim 4, 13; Kaggle topic 215382 unanswered). Nobody can check what the data is, so nobody can answer point 1.
* Evidence: the keep ("good to use for now. We can filter later") predates the 2026-10-07 measurements. By the
  precedence of stages, a later measured finding supersedes it. Course churn data with fakeness signs went to `No` in
  three cases (customer_churn_dataset, predictive_analytics_for_customer_churn_dataset, ibm_telco_customer_churn).
  bank_customer_churn was kept, but it had no PROV-3 marks (precedents D2).
* What I concede: PROV-1 names "an identifiable first uploader" as a traceable upstream, so on its own this point is
  not a reason to exclude.
* Remedy: no change to the definition. The curator confirms or revises the keep. If kept, this is the third keep of an
  untraceable course dataset, so the PROV-1/PROV-2 amendment from precedents D2 is due. Also fix the mismatch between
  `source = "Other"` and `original_source: Company` (PROV-8, claim 48).

**3. The activity window may end at the closure, and the target has no horizon (P3/P4; LEAK-10 Must if strong, USE-5, USE-8)**

* Problem: if the window ends at the closure, part of the task is recognising a closed account rather than foreseeing
  one. The label also mixes voluntary and issuer closures and has no horizon (practitioner, gaps 1 and 4).
* Evidence: 54 customers with 6 contacts, 7 with no Q4 transaction and 5 with no Q4 amount, all attrited. A balance of
  0 in 55% of attriters vs 19% of the others. The 6 activity columns alone reach AUC 0.981 (claims 20-23).
  Against a strong leak: the Q1 count alone gives 0.819 (the same as Q4 alone), and profile + limit + Q1 count gives
  0.895 (column_audit, window test).
* Rule: not proven strong, so LEAK-10 does not force retirement. Consistent with churn_telco_south_asia (precedents D3).
* Remedy: a note. Add the Q1-count result to the "Potential leak" bullet as the evidence that the signal predates the
  closing. In `predicted`, say the label mixes voluntary and issuer closures and has no horizon.

**4. A temporal task shipped as IID without the tag (P4; SPLIT-8 Must, narrows SPLIT-7)**

* Problem: the deployed model trains on one snapshot and scores the next. The definition says only "Random customers
  of the same snapshot".
* Evidence (split_audit, problem 1): there are no dates and no second snapshot. The cost cannot be measured: the file
  order is a sort on Total_Trans_Amt (Spearman 0.82), and thirds by CLIENTNUM give 0.993, the same as random.
* Remedy: fix the definition. Add `ForcedIIDFromTemporal` to `data_tags`. Reword `split` and the IID bullet to say the
  split is forced, that the cost cannot be measured and why, and that dates should be recovered if the LEAPS material
  turns up. No re-split. Precedents: expresso_churn_prediction_1m, account_debt_south_africa.

**5. Little room to rank methods (P6; TP-1 Must as procedure, weighed)**

* Problem: near the ceiling, strong methods tie, so the dataset adds noise rather than signal to a leaderboard.
* Evidence: CatBoost default 0.9943, with 3 of 9 splits at or above the 0.995 of `solved`. LightGBM 0.993, log loss
  0.075 (claims 37, 50).
* Rule: no probe flag yet, and a ceiling alone is no reason to retire (EV-3). It weighs against shipping data whose
  validity is already in doubt (points 1 and 3).
* Remedy: before shipping, run the TP-1 check against the tuned methods. If `solved` trips, decide as for anneal or
  aps_failure.

**6. Notes that say more than the data shows (P7 and writing; quality only, no reason to exclude)**

* The 12-month count is Q4 + Q1 in every row, but `known` calls it a 12-month count and its change "between quarters"
  (claim 7).
* The "10 profile columns" behind AUC 0.625 are not named. Reproduced: 0.629 for 9 demographic columns + Credit_Limit
  (claim 23).
* "Not missing at random" holds only for Income; the Unknown of Education and Marital has no such evidence (claim 28).
* The clipping bullet omits that Avg_Open_To_Buy and Avg_Utilization_Ratio inherit both clips (column_audit,
  problem 3; LEAK-30).
* the earlier review file lists `2ndTierData` as "Implemented", but the tag came from the v1 migration (precedents D1).
* Remedy: reword these in `dataset.py` and in the review file. No change to the data.

Judgment: Validity: SEL-16/PROV-3 triggered, cannot be fixed (exclude); PROV-1 kept on a superseded call
(amendment due); LEAK-10 possible, kept with a note (add evidence); SPLIT-8 triggered, fixed by tag and wording.
Value: TP-1 check due (near ceiling). Quality: wording fixes.

</details>

<details><summary>Advocate rebuttal</summary>

**Advocate, rebuttal: credit_card_customers (2026-10-20)**

**Critic 1, the data looks generated (SEL-16, PROV-3): disputed**

The marks are measured and calibrated, and I conceded them in my point 3 (EV-1). Two of the critic's steps do not hold.

**(a) The class-mix flips are not PROV-3 test 5.**
- Test 5 asks for one of three things:
  - a correlation between two features that differs by class or changes sign;
  - a label-free nearest-neighbour distance that predicts the label;
  - number formats that differ by class.
- A class mix that changes across bins of one feature is what any predictive feature shows. Total_Trans_Amt has a single-feature AUC of 0.876, so its bins must differ in class mix.
- 746 customers above 12,000 with no attriter fits the leak reading the critic accepts in point 3: high spenders do not close. It does not need a generator.
- The test-5 statistic was measured, and it is negative. The leak probe's label-free distance AUC is 0.559 (checklist, probes). The retired homeq case had 0.92.
- So the one new piece of evidence turns into a test that could have refuted "maybe generated" and did not support it (EV-6).

**(b) "A measurement outranks the missing page" (EV-2) is the wrong rule.**
- EV-2 ranks two pieces of evidence that disagree. Here no page disagrees with the marks.
- The question is how much proof PROV-3 needs. EV-3 (Must) answers it: "a generated-data mark needs what the source says and, where possible, the generator written down."
- "Where possible" qualifies only the generator. The source statement is required outright.
- The critic concedes that a source statement is impossible here (LEAPS is offline and not archived). So the Must's evidence condition is not met. It is not waived.
- Every PROV-3 retirement in the Cases table had a mechanism or a source statement (precedents D1).

**What follows.**
- The Q4 + Q1 identity is a partial mechanism. It shows the counts were derived from two periods, not that the rows were drawn from a generator. A teaching-case author reworking the summary columns would leave the same mark.
- PROV-3 is "maybe" with the test that would settle it: the LEAPS case material or a generator written down.
- If the curator judges four or more calibrated tests to be enough without a source statement, that is a change to EV-3/PROV-3. It should be made once, for hepatitis_c_egypt, stroke_prediction and framingham_heart_study_fhs as well (option d of the consistency check).
- I agree with the critic that `2ndTierData` cannot carry a Must. If the curator finds the data generated, the dataset is retired, not tagged.

**Critic 2, the source is kept on a screening-era call (PROV-1, PROV-2): conceded**

- The critic concedes that PROV-1 holds through a named first platform. Our positions are the same.
- I agree the screening keep predates the measurements and needs the curator's confirmation (stage precedence).
- I agree the PROV-1/PROV-2 amendment is due, as the third keep of this kind.
- I agree the mismatch between `source = "Other"` and `original_source: Company` gets fixed (PROV-8, claim 48).

**Critic 3, window and horizon (LEAK-10, USE-5, USE-8): conceded, with one wording limit**

- Same remedy as my point 1: add the Q1-count result to the "Potential leak" bullet. The critic agrees it is consistent with churn_telco_south_asia.
- On `predicted`: I accept adding that the label has no stated horizon (already partly there).
- I do not accept writing that the label "mixes voluntary and issuer closures" as a fact. The data card only says "if the account is closed". The 50/50 split is an industry figure from the practitioner, not a measurement on this file (EV-7).
- Write instead: "the source does not say whether issuer closures count".

**Critic 4, SPLIT-8 tag: conceded**

This is identical to my point 2. Add `ForcedIIDFromTemporal`, reword `split` and the IID bullet, no re-split.

**Critic 5, little room to rank methods (TP-1): partly conceded**

- I agree to run the TP-1 check against the tuned methods when their results exist. If `solved` trips, decide as for anneal or aps_failure.
- I dispute that a ceiling "weighs against shipping data whose validity is already in doubt".
  - "Independent failures are not conflicts" (principles, step 4): each Must is judged on its own facts.
  - A doubt under P5 is settled by P5's own evidence, not by adding up concerns from P6.
  - TP-2: until a concrete reason is found in the task itself, the task stays.
  - EV-3: a ceiling score is no verdict.
  - Log loss 0.075 still separates methods.

**Critic 6, notes that say more than the data shows: conceded**

- All five items match my point 7. Make the wording fixes in `dataset.py`, plus the clipping clause.
- Correct the earlier review file: `2ndTierData` came from the v1 migration, not from this review.

**Net position**

- Ship after these changes: the SPLIT-8 tag, the leak note with the Q1 evidence, the horizon wording, the source-field fix and the wording fixes.
- One open question for the curator: whether calibrated PROV-3 marks without a source statement are enough to retire. That is a change to EV-3/PROV-3, and it applies to four datasets.

Evidence cited:
- the verification checklist (label-free distance 0.559)
- .claude/skills/knowledge-curation/references/evidence.md (EV-2, EV-3, EV-6, EV-7)
- .claude/skills/knowledge-curation/references/provenance.md (PROV-3, tests 5 and 6, Cases)

</details>

<details><summary>Critic rebuttal</summary>

**Critic, rebuttal: credit_card_customers (2026-10-20)**

I agree with the advocate on every point except point 3. Point 3 is the only real dispute, and it decides the verdict.

**A1. The window leak, kept with a note: concede**

* Same remedy as my point 3: add the Q1-only numbers (0.819, and 0.895 with the profile) to the leak bullet.
* I still ask for one clause in `predicted`: the label has no horizon and mixes voluntary and issuer closures
  (practitioner, gap 4; USE-5). It is a note, not a block.

**A2. Split, SPLIT-8 tag and wording: concede**

The advocate's fix is the same as my point 4.

**A3. "Generated is not established": dispute**

The advocate argues that PROV-3 needs a source statement or a written-down generator. The rules do not say that.

* **What the rules require.**
  * PROV-3 (Must) defines the detection as "the seven tests under Methods" and calibration against a real dataset of
    the same kind.
  * "When you can, write the generator down: that settles it" (provenance.md, Methods) makes a generator sufficient,
    not necessary.
  * EV-3 asks for the source statement and the generator only "where possible". LEAPS is offline and not archived
    (claim 13, Wayback has no snapshot), so neither is possible.
  * Reading "where possible" as "required" turns PROV-3 into a rule that can never apply to an untraceable source.
    That is backwards: PROV-1 and PROV-3 together should be strictest exactly there.
* **The precedents do not all rest on a mechanism.** homeq_default_prediction was retired on test 5 alone: near-copy
  clusters pure in the label, distance AUC 0.92 (provenance.md, Cases). That is a statistic, the same kind of evidence
  as the class flips here (column_audit, problem 1). Above 12,000, 746 rows sit with 0 attriters, at a base rate of
  16%. 6,000-7,000 is 68% attrited.
* **The marks were tested so that they could have failed, and they were calibrated (EV-6, EV-9).**
  * Shuffled control: 564-597 rows satisfy the identity, against 10,127/10,127 in the data.
  * Real card books: Home Credit gives 9 of 8,920 for the identity, -0.60 for inactivity vs count and 0.447 for spend
    vs limit.
  * Real credit tables give 0.58-0.61 on the education permutation test.
  * These are proofs of each mark, not circumstance. The one inference left is that the marks together mean a
    generator, and four calibrated tests (5 and 6) agree on it.
* **The advocate's other readings are refuted on the data.**
  * Half-years for the Q4 + Q1 identity: the 7 customers with no second-half transaction have only 2-4 inactive
    months, where a half-year reading needs at least 6 (the earlier review file, issue 1).
  * Product eligibility for tenure and age: eligibility gives an upper bound. It does not make tenure in months rise
    with age in years (slope 1.006, r 0.893), with a lower bound at age-20 holding in 7,622 of 7,664 rows. Real tenure
    ranges are not 13-56 months across ages 26-73.
  * "Reworked columns, not generated rows": that is still PROV-3, which also excludes "a real table someone reworked"
    (`Data Quality Issue`). Either reading lands on the same Must.
* **`generated_probes` with no flag:** EV-3 says "no flag is no pass either". The probe does not test per-bin class
  flips (column_audit, problem 1).
* **Concessions.**
  * The verdict is the curator's call (who-decides precedence).
  * hepatitis_c_egypt, stroke_prediction and framingham_heart_study_fhs must be decided alike.
  * Adding the amount-bin numbers to decision 1 is right either way.
  * If the curator keeps the dataset, that is an amendment of PROV-3, not a quiet keep. The advocate agrees.
* **Winning rule:** PROV-3 and SEL-16 (Must, P5 and P2) with EV-1 and EV-2 (a calibrated measurement outranks a
  missing page). EV-6 is a Should and only governs how the result is reported. My remedy stands: `No` + `AHDS` +
  `Missing source information`.

**A4. The source traces to a named first platform: concede in part**

* PROV-1 alone does not exclude it, which I conceded in my point 2. The `source` / `original_source` mismatch and the
  amendment that is due are shared ground.
* I dispute only "a detail in the PROV-2 sense". PROV-2 keeps a source that is plausible but unclear in a detail.
  Here the unknown part is whether the rows are real (A3), and that is not a detail. So PROV-2 applies only if A3
  goes the advocate's way.

**A5. Clipping, LEAK-30: concede**

Kept by the curator on 2026-10-19. The extra clause on the two derived columns matches my point 6.

**A6. Worth benchmarking: concede in part**

* A ceiling alone does not block it (EV-3), and no TP flag is raised.
* One correction: the metric is `roc_auc` alone. Log loss is not shipped as a second metric, so the 0.075 adds no
  headroom to the leaderboard (EV-5 only allows it).
* It stays a weighed factor against a dataset whose validity is in dispute.

**A7. Wording: concede**

* Same list as my point 6, plus the two additions I accept: CLIENTNUM in `changes`, and the LEAPS date and the
  "dummy dataset" quote marked unverified (EV-7).

</details>

<details><summary>Verification checklist</summary>

**Checklist: credit_card_customers (re-check, 2026-10-20)**

Automated: `dataset list` imports the class; `ruff@0.15.15 check` and `format --check` clean; `dataset check`: 0 errors,
0 warnings, 0 info (26 checks); `sync-notebooks --check` clean; explore.ipynb has no outputs. README diff explained by
the 2026-10-19 comment edit (clipping bullet), the new `time_gap` split fields and the REVIEW.md file row; checksum now
`v2:82e449d1...` (was `v2:f4415027...`). Nothing fixed.

Probes: leak: all features 0.993, depth-2/3 tree 0.862/0.920, best single Total_Trans_Amt 0.876, no exact
copies, 1-NN agreement 0.886 (chance 0.730), label-free distance 0.559; no red flag. Task: best LightGBM skill +0.987, no
flag. Hidden groups: 5 candidates, no hit (top Months_on_book gap +0.002, near copies 0%). Generated: no flag (0 rule
leaves; 37.1% of column pairs dependent, 0 uniform).

| Rank | Check | Verdict | Evidence | Rules |
|---|---|---|---|---|
| P1 | Ethics | pass | anonymised bank customers (CLIENTNUM masked and dropped); churn retention, no harmful use | SEL-1 |
| P2 | Scope | pass | binary churn classification that informs a retention contact | SEL-2 to SEL-15 |
| P2, P5 | Real data | concern | re-measured on the raw file: Total_Ct_Chng_Q4_Q1 splits Total_Trans_Ct into two whole counts in 10,127/10,127 rows; tenure <= age-4 in 7,664/7,664 non-36 rows, slope 1.006, r 0.893; 0 of 5,358 women above $60K; Total_Trans_Amt > 12,000: 746 rows, 0 attrited; 2 rows in 10,500-12,000. generated_probes finds no flag. Source is a teaching case (LEAPS), cannot be traced. Prior AI recommendation: `No` + `AHDS` | SEL-16, PROV-3 |
| P3 | Use case and fit | pass | actor (bank manager), moment (snapshot), decision (contact first); fit `approximate` names the gap (window/closure, generated marks, untraceable source) | USE-1, USE-2, USE-8, USE-9 |
| P3, P4 | Target and metric | concern (cannot verify timing) | Attrition_Flag 16.07% positive; ROC AUC fits; when closure happened relative to the 12-month window is not stated (Kaggle topic 203290 unanswered) | USE-5, LEAK-22 to LEAK-26, EV-5 |
| P4 | Available at prediction time | concern | Q4 count zero: 7 rows, all attrited; 6 contacts: 54 rows, all attrited; zero revolving balance 54.9% attrited vs 18.6% existing; LightGBM 5-fold (own reproduction): activity 6 cols 0.980, profile 10 cols 0.636 (claim 0.625; column set guessed), all 0.994. Median Q4/Q1 count ratio 0.531 vs 0.721. Kept on purpose with a note | USE-3, USE-6, LEAK-10 to LEAK-12 |
| P4 | Irreversible / all-row leakage | pass (noted) | NB posterior columns (supervised, label-fit) dropped (LEAK-13). Credit_Limit clipped: 507 rows at min 1,438.3, 508 at max 34,516 (5th/95th pct 1,438.51/34,516); Total_Revolving_Bal 508 at 2,517. Scaling over all rows is weak; curator kept it 2026-10-19 | LEAK-13 to LEAK-15, LEAK-27 to LEAK-31 |
| P4 | Copies across the split | pass | 0 duplicate rows (without CLIENTNUM); CLIENTNUM unique; leak probe: 0.0% exact copies | LEAK-16 to LEAK-21, SPLIT-29 |
| P4 | Split regime | pass | IID 3x3; no date column, one row per client; hidden-group probe no hit | SPLIT-1 to SPLIT-31 |
| P5 | Source | concern | trail ends at an offline teaching platform (leaps.analyttica.com unreachable today, HTTP 000); no bank, country or period; definition `source = "Other"`, record `original_source: Company` disagree | PROV-1, PROV-2, PROV-8 to PROV-12 |
| P5 | Uniqueness | pass | no other record names BankChurners.csv or credit_card_customers; not the Taiwan default data (credit_card_clients_default) | PROV-4 to PROV-7 |
| P5 | Damage and repair | cannot verify | no origin to rebuild from; Months_on_book = 36 in 2,463 rows (24.3%) looks filled, kept | PROV-13 to PROV-15 |
| P6 | Worth benchmarking | concern | no task-probe flag; LightGBM skill +0.987, all-feature AUC 0.993-0.994; prior note: CatBoost default 0.9943, 3 of 9 splits >= 0.995 (not re-run here); near ceiling | TP-1 to TP-10 |
| P7 | Dtypes and cleaning | pass | 5 categoricals declared, 14 numeric; "Unknown" kept as category (data card value, not MAR: 1,060 F vs 52 M); 36s kept; identifier dropped | CLEAN-1 to CLEAN-24 |
| proc | Notes match the code | pass | `_clean` drops CLIENTNUM and the 2 NB columns (asserted), nothing else; every numeric claim in curation_comments and the decisions reproduced on the raw file (except 0.625, see above) | writing.md |
| proc | Licence and citation | pass | CC0-1.0 per Kaggle; Zenodo copy CC BY 4.0 noted; bibtex names the Kaggle upload and the LEAPS case | EV-4, PROV-10 |
| proc | Reproducibility | pass | local sha256 c91b525a... matches the stated hash; Zenodo pinned link returns HTTP 200, 1,510,880 bytes = local size | |

</details>
