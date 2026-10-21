# dataorg_financial_health_prediction_challenge

**Outcome:** added. Zindi's file of FinScope small-business surveys (Eswatini 2023, Malawi 2019, Zimbabwe 2022) as a
three-class task on the business's Financial Health Index (Low, Medium, High) with a random split, declared with
the competition's weighted F1, without Lesotho's 1,944 rows and without the 11 answers on financial products held (inputs of the index,
issue 2). The use case now names a development partner or government screening businesses for support. The Lesotho
decision now says its correlations leave out the placeholder codes 97/98/99 and that its answers are damaged too. Six
impossible business ages are made missing. The notes name the "not ticked" columns, the amounts' periods, the inputs
the release lacks and the cross-country score. The AI recommends shipping it; whether anyone acts on the index's class is the curator's
call (issue 5).

```text
Verdict: ship after changes.
Validity: SEL-3/USE-5 rest on the screening use case alone (the index's author and formula are unsourced; issue 5);
  USE-1 holds with use_case rewritten to the screening actor, fit approximate (USE-8); LEAK-10 triggered (the 11
  product answers are inputs of the index's access-to-finance dimension), fixed by dropping them (issue 2); LEAK-10
  for Malawi's insurance missingness moot after the drop; PROV-1/PROV-4 hold; PROV-13 open for the Lesotho drop:
  diagnosis completed, origin not yet asked of data.org or FinMark Trust (issue 1); SPLIT-1 holds, SPLIT-31 noted.
Value: TP-4 not met; TP-2, a small real signal after the drop (LightGBM log loss 0.694 against 0.796 for the class
  shares, macro ROC AUC 0.756, better on 9 of 9 splits; task probe re-run after the drop: best family random forest 0.685, no flags).
Quality: CLEAN-11 six impossible business ages made missing; CLEAN-10 and CLEAN-21 notes; wording corrected.
Weighed: source + (exact FinScope interview counts, licence), gap + (a multiclass survey task the collection lacks), use case - (index
  introduced by the challenge), signal - after the drop.
For the curator: issue 5 (does anyone act on the class), issue 2 (confirm the drop or amend LEAK-10), issue 1 (the
  Lesotho drop, decided alike with account_debt_south_africa).
```

**Main points:** Accept the screening use case or call the index `No Good Target` (issue 5); confirm the drop of the
11 product answers or amend LEAK-10 (issue 2); keep Lesotho dropped, decided alike with account_debt_south_africa's
issue 1 (issue 1).

**Record fields that disagree with the definition:**

- `domain`: record `business & marketing`, definition `finance`.

**Record judgment:** valid with concerns. Real FinScope survey interviews (Eswatini's rows match the survey's
interview count exactly), released under CC BY-SA 4.0 for a Zindi competition. The label is an index the competition
introduced without a published formula (issue 5); its access-to-finance inputs are now dropped (issue 2).

**Issues for Lennart:**

5. **Is the index's class a target someone acts on?** The label is the Financial Health Index (FHI), a composite score
   that sorts each business into Low, Medium or High. The competition page says the challenge "introduces a
   data-driven Financial Health Index (FHI) for SMEs - a composite measure that classifies businesses into Low,
   Medium, or High financial health across four key dimensions: savings and assets, debt and repayment ability,
   resilience to shocks, and access to credit and financial services". It names no author, method or weights;
   FinMark Trust appears only as the owner of the survey data.
   - Effect: if no one acts on the class, a better score means reproducing an index nobody uses, not a better
     screening decision.
   - Rule: SEL-3 (Must) admits a survey table only with a genuine target, an observed outcome or an expert
     annotation. No source we have makes the FHI either, so the task stands only if someone acts on its class. If
     "data-driven" means the classes come from a clustering, SEL-4 excludes it.
   - For keeping (advocate): the page names "development partners and governments" who "identify vulnerable
     businesses and target support". That is the proxy-means-test pattern of social programmes: a short interview
     predicts the class a fuller assessment would give. The classes behave like thresholds on a score, not like
     clusters (no business with an insurance product is Low).
   - Against (critic): who built the index, and how, is unsourced. account_debt_south_africa's label is observed bad
     debt and central_international_medical_college_and_hospital_health_risk_prediction's a published clinical score;
     this label is neither, so SEL-3 rests on the use case alone.
   - Implemented: `use_case` and the prediction-point note name the screening actor; `fit_reason` says the
     competition introduced the index and published neither its formula nor who acts on it; fit `approximate`
     (USE-8). Alternative: `No Good Target` (SEL-3), at least until data.org or FinMark Trust describe the index.
   - What would settle it: a method note from data.org or FinMark Trust (the same request as in issue 1).
   - Recommendation: accept the screening use case with fit approximate (the panel's joint view).
   - Decision: accept the screening use case, or `No Good Target`.

2. **Confirm the drop of the 11 product answers, or amend LEAK-10?** The 11 columns say which financial products a
   business holds: four insurance answers (any, funeral, medical, motor), credit card, loan account, debit card,
   internet banking, mobile money, saving with friends or family, and an informal lender. The owner gives them at the
   same interview as everything else, but the page names "access to credit and financial services" as one of the
   FHI's four dimensions, so they are inputs of the label.
   - Effect: with them, a model scores well by recomputing one of the index's four dimensions, which a screening
     form run before the product questions could not do; most of the task is rebuilding the index from its own inputs. With the same LightGBM on the
     shipped splits, country plus the 11 answers reach log loss 0.255 against 0.266 for all 37 columns (better on 9
     of 9 splits), and none of the 1,896 businesses with an insurance product is Low. Without them, the 26 remaining
     columns reach 0.694 (macro ROC AUC 0.756) against 0.796 for the class shares, better on 9 of 9.
   - Implemented: the 11 columns are dropped. LEAK-10 (Must) puts out "a part ... of the target" even when it is
     known at the prediction point. This follows account_debt_south_africa (the label's rule inputs dropped, the rest
     kept; that rule was not deterministic either, 371 exceptions), mutual_funds_india `rating` and the
     student-performance grades G1/G2.
   - Alternative: keep them through a deliberate amendment of LEAK-10 for inputs of an unpublished, non-deterministic
     index. A Must has no exceptions, and the amendment would mean reopening those three precedents (the critic's
     point, upheld by the mediator).
   - A smaller call on the scope: the page speaks of "formal financial services". Dropping only the 8 formal products
     would leave log loss 0.678 (macro ROC AUC 0.771). Mobile money and the two informal sources probably feed the
     debt or access dimensions, but no source says so; the panel drops all 11.
   - Recommendation: confirm the drop of all 11.
   - Decision: confirm the drop (all 11, or only the 8 formal products), or amend LEAK-10.

1. **Lesotho's label runs against the index: keep its 1,944 rows dropped?** In Lesotho every formal-finance answer
   (loan account, debit card, internet banking, motor insurance, income-tax compliance) goes with a lower class; in
   Eswatini, Malawi and Zimbabwe each goes with a higher one (the decision table in README.md). The class also falls
   with income, expenses and turnover: Spearman -0.12, -0.11 and -0.11 once the placeholder codes 97, 98 and 99 are
   left out (-0.055, -0.073 and -0.052 as released), against +0.14 to +0.24 elsewhere.
   - The answers are damaged too: 12 columns are missing for every Lesotho business (among them three insurance
     columns, the credit card and record keeping), and 86% say they used to have an informal lender.
   - Models trained on the other countries rank Lesotho at ROC AUC 0.43 to 0.50, against 0.62 to 0.95 for the other
     countries (claim audit); swapping Low and Medium in Lesotho's labels does not repair it (ROC AUC 0.54).
   - Effect: kept, Lesotho would teach a model the opposite direction for the same answers, on a fifth of the rows.
   - Implemented: the 1,944 rows are dropped; country is a column, so the other rows are unaffected. Alternative:
     keep Lesotho as released with an `Anomaly:` note, or retire the dataset.
   - Rule: PROV-13 (Must) asks to check the origin before cutting around damage. Neither data.org nor FinMark Trust
     has been asked how Lesotho's FHI was computed; a data request (with the FHI method of issue 5) would do it.
   - Precedent: account_debt_south_africa dropped the 20% of its file where debt was not recorded, and its issue 1
     (keep the drop, keep the rows or retire) is still open; caracas_cervical_cancer and
     biogeographical_ancestry_prediction dropped a block recorded differently. The two open cases should be decided
     alike.
   - Recommendation: keep the drop, the same way for both datasets.
   - Decision: keep the drop, keep Lesotho with an `Anomaly:` note, or retire (in each case the same for
     account_debt_south_africa); and whether to send the data request to data.org / FinMark Trust.

**Review panel:** ship after changes (mediator). Claim audit: 23 claims, 15 hold, 3 hold in part, 3 refuted (all
fixed: the tree-against-LightGBM comparison, the dtype count, the impossible ages), 2 untested. Blind review: include
with changes; main concern the product columns that feed the index (now dropped). Debate: agreed on dropping the 11
product answers, the screening use case, the Lesotho drop and the random split; disputed and settled: "the FHI is
FinMark Trust's expert-built measure" (unsourced). The mediator's issues 1, 2 and 3 are issues 5, 2 and 1 here; the
earlier issue 4 (the year) is settled by PROV-9 (the competition's launch year, 2025).

<details><summary>Mediator</summary>

**Recommendation**

```text
Verdict: ship after changes.
Validity: SEL-3/USE-5 hold only through the screening use case (the label's authorship is unsourced; issue 1);
USE-1 holds with use_case rewritten to the screening actor, fit approximate (USE-8); LEAK-10 triggered (the 11 product
columns are inputs of the index's "access to credit and financial services" dimension), fixed by dropping them;
LEAK-10 (Malawi insurance missingness, weak) is moot after the drop; PROV-1/PROV-4 hold; PROV-13 holds for the Lesotho
drop, with the diagnosis completed and a data request; SPLIT-1 holds, with a SPLIT-31 note.
Value: TP-4 not met (no single raw feature matches); TP-2 keeps a small real signal after the drop (log loss 0.694
against 0.796, macro AUC 0.756, better than the class shares on 9 of 9 splits).
Quality: CLEAN-11 (6 impossible business ages to missing); CLEAN-10 and CLEAN-21 notes; wording.
Weighed: source + (exact FinScope interview counts, licence), gap + (multiclass survey task), use case - (index
introduced by the challenge), signal - after the drop.
For the curator: issue 1, does a real actor act on the FHI class (SEL-3, USE-5, SEL-4); issue 2, confirm the drop or
amend LEAK-10; issue 3, decide the Lesotho drop alike with account_debt_south_africa.
```

**Changes to make now (no decision needed)**

1. **Drop the 11 product columns** (has_insurance, funeral_, medical_, motor_vehicle_insurance, has_credit_card,
   has_loan_account, has_debit_card, has_internet_banking, has_mobile_money, uses_friends_family_savings,
   uses_informal_lender). Replace the `Potential leak, kept on purpose` bullet and decision 2 by a drop decision that
   cites the Zindi Description page ("four key dimensions: ... access to credit and financial services") and the
   matched comparison (country + products 0.255 against all columns 0.266, products better on 9 of 9; the rest 0.694
   against 0.796). Rule: LEAK-10 (Must, "a part of the target"), as in account_debt_south_africa (SEL-5 Cases),
   mutual_funds_india `rating`, student performance G1/G2; EV-1. The `Potential leak` form is not valid for a Must
   (both sides agree).
2. **Rewrite `use_case`, the prediction-point bullet and `fit_reason`**: a development partner or government screens a
   small business from one interview to target support (the Zindi page's second user); fit `approximate`. Name the
   gaps: the index is introduced by the challenge with an unpublished formula; questionnaires differ by country; the
   test stands for the same surveys. Do not call the FHI FinMark's expert-built measure (no source, see the facts).
   Drop the 0.285 against 0.260 comparison (it measures model capacity). Rules: USE-1, USE-5, USE-8, EV-1.
3. **Decision 1 (Lesotho)**: say the Spearman figures exclude the 97/98/99 sentinels (as released -0.055 / -0.073 /
   -0.052); add the feature damage (12 all-missing columns, among them the insurance columns and the credit card;
   "Used to have" an informal lender 86%). Rules: PROV-13, EV-1.
4. **Split note**: a model trained on Malawi 2019 and Zimbabwe 2022 scores Eswatini 2023 at log loss 0.669 against
   0.346 under IID; the split stays. Rule: SPLIT-31 (Should).
5. **Set `business_age_years` and `business_age_months` to missing in the 6 rows where the business is older than the
   owner.** Rule: CLEAN-11 (Should; cheap and safe).
6. **Notes**: in Zimbabwe (motivation_make_more_money, current_problem_cash_flow) and Eswatini
   (problem_sourcing_money, marketing_word_of_mouth), missing means "not ticked" (CLEAN-10); the amounts' periods may
   differ by country (CLEAN-21); the page names inputs that the release lacks (traded commodities, firm size,
   location).
7. **Wording**: the counts after the drop (26 features); the competition metric is "F1" (Zindi Evaluation page; API
   `f1_multiclass`), "weighted" only from a discussion thread. Rule: writing.md, EV-2.
8. **Record**: `domain: finance`; a data request to data.org / FinMark Trust (the FHI method, Lesotho). Rule: PROV-13.
   A dated `CHANGELOG.md` entry and a `dataset check` to regenerate the README (house rule).

**Issues for the curator, ranked**

1. **P2/P3, Must (SEL-3, USE-5; SEL-4 open): is the FHI class a target someone acts on?**
   - Problem: the label is a composite index the challenge itself introduces ("This challenge introduces a
     data-driven Financial Health Index", Zindi Description page). No author, method or user of the index is named.
   - Effect: if no actor acts on the class, the task is `No Good Target`; if "data-driven" means a clustering, SEL-4
     excludes it.
   - Keep (advocate): Zindi names development partners and governments who "identify vulnerable businesses and target
     support"; the proxy-means-test pattern fits; the index has four named dimensions with thresholds (0 Low among
     1,896 insured), which looks like a score, not a cluster.
   - Doubt (critic): authorship and formula are unsourced; a composite index of unknown construction is neither an
     observed outcome nor an expert annotation; SEL-3 then rests on the use case alone (P3 informs P2).
   - What settles it: data.org's or FinMark Trust's method note. Decision: accept the screening use case with fit
     approximate (the panel's joint view), or `No Good Target` pending the request.
2. **P4, Must (LEAK-10): confirm the drop of the product columns, or amend LEAK-10.**
   - The drop is the rule's remedy and is listed as change 1. An amendment (inputs of an unpublished, non-deterministic
     index may stay) is the only other route, since a Must has no exceptions. It is not an equal option: it would
     depart from account_debt_south_africa (also non-deterministic: 371 exceptions), mutual_funds_india and student
     performance unless those are reopened (critic, upheld).
   - Scope, a minor call: the page speaks of "formal financial services". Dropping only the 8 formal products leaves
     log loss 0.678 (AUC 0.771), the 11: 0.694 (AUC 0.756). Mobile money and the two informal sources are probably
     parts of the debt or access dimensions, but no source says so. The panel drops 11.
3. **P5, Must (PROV-13): decide the Lesotho drop alike with account_debt_south_africa's open issue 1.** Both sides keep
   the drop; the measurement (labels and features damaged, transfer AUC 0.43-0.50 against 0.62-0.95) supports it.
   The decision needed: drop (both) or retire (both).

**Agreed facts**

- Train.csv sha256 and byte size match the Zindi API; a Kaggle mirror is identical; CC-BY SA 4.0; 2025-12-12 to
  2026-03-15. Eswatini 2,674 + 669 = 3,343 interviews (FinScope MSME 2023); Malawi 2,985 of 2,993. Test.csv is a random
  20% of every country, 0 ID overlap.
- 7,674 rows after the Lesotho drop; Low 66.5%, Medium 27.4%, High 6.1%; smallest class 154 rows per test fold.
- None of the 1,896 insured businesses is Low; majority class within identical product profiles 93.8%.
- Same learner: country + 11 products 0.255, all columns 0.266 (products better on 9 of 9); the rest 0.694; class
  shares 0.796. The definition's 0.260 is not reproduced (default LightGBM 0.283).
- Lesotho: Spearman -0.055 / -0.073 / -0.052 as released, -0.12 / -0.11 / -0.11 without sentinels; 12 columns all
  missing; transfer AUC 0.43-0.50 against 0.62-0.95.
- Split: no hidden group, 0 exact copies, 0.4% near copies, neighbour agreement at chance; unseen-country log loss
  0.669 / 0.504 / 0.225 against IID 0.346 / 0.323 / 0.149.
- Malawi asked the insurance block of 147 businesses (91% not Low against 14%); the missingness-only effect is
  +0.002 log loss, mixed on 6 of 9 splits.
- 6 rows have a business older than its owner.

Disputed facts, settled:

- "The FHI is FinMark Trust's expert-built measure" (advocate): **not supported.** The Zindi API texts
  (the API's page texts) say the challenge "introduces a data-driven Financial Health Index"; FinMark Trust
  appears only in an "About" paragraph as the data organisation. The critic's reading stands (EV-1, EV-2).
- "Not Trivial because a depth-6 tree on the products loses to LightGBM on 9 of 9" (advocate): **wrong evidence**,
  right conclusion. The matched learner reverses it; TP-4 is unmet because the best single feature scores 0.508
  against 0.268 (task probe).

On rank: USE-6 (P3, "anything known at the prediction point") does not outrank LEAK-10 here. It is no conflict: LEAK-10
names "a part ... of the target" even when known at the time, and the tension row "a real task against a leak" (fix
the leak, keep the task) applies. Both sides agree.

**Consistency with precedent**

- Product columns dropped: follows account_debt_south_africa (SEL-5 Cases, CC 2026-10-12), mutual_funds_india
  (2026-10-01) and student performance G1/G2. The definition's current keep departs from them without a fact that
  sets the case apart; the drop removes the departure.
- Lesotho drop: consistent with account_debt_south_africa, caracas_cervical_cancer, biogeographical_ancestry_prediction
  (a block of rows recorded differently, country a column); paired with account_debt's open issue (issue 3).
- Log loss instead of F1: consistent with african_credit_scoring_challenge, zillow_prize.
- Domain `finance`: consistent with account_debt_south_africa, african_credit_scoring_challenge.
- Fit `approximate` with a named gap: consistent with kick and account_debt_south_africa.
- No curator decision exists on this dataset (no `CC` line), so no drift to report.

</details>

<details><summary>Claim audit</summary>

**Table**

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 3,4,7 | 7,674 rows; Low 66.54 / Medium 27.42 / High 6.05; Lesotho 1,944 dropped | D task_summary | counts on the definition frame | holds | 7,674; 0.6654/0.2742/0.0605; raw Lesotho 1,944 | EV-1 |
| 3,37 | Eswatini 2023 FinScope MSME, exact interview counts | D, R | Train+Test per country vs FinMark | holds (Eswatini) | 2,674+669 = 3,343 = interviews in FinScope MSME Eswatini 2023; Malawi 2,388+597 = 2,985 | PROV-1 |
| 9,20,32 | "the task partly recovers that formula (small tree on those columns 0.285; all columns 0.260)"; tree worse on 9/9 | D fit_reason, comments, decision 2 | same model family on country + 11 product columns vs all columns, shipped 9 splits | **refuted in substance** | LightGBM (lr 0.03, 400 trees, 15 leaves): products 0.2548 vs all 0.2658, products better on **9/9** (mean diff 0.011, sd 0.005); logistic regression on products 0.272 beats default LightGBM on all columns (0.283) on 8/9; country + the 26 other columns 0.694 (prior 0.796). The 0.260 is not reproduced by default LightGBM (0.283 here, probe 0.303). The tree-vs-LightGBM gap is model capacity, not information in other columns. | EV-1, USE-8, LEAK-10, SEL-3/SEL-5 |
| 20 | none of the 1,896 insured businesses is Low | D comments | crosstab | holds | 1,503 Medium, 393 High, 0 Low | EV-1 |
| 32 | majority class within identical product profiles 93.8% | D decision 2 | groupby 840 profiles | holds | 0.938 | EV-1 |
| 19,31,39 | Lesotho: formal answers go with lower class; Spearman -0.12/-0.11/-0.11; transfer AUC 0.63-0.68 vs Lesotho 0.46 | D comments, decision 1, R | Spearman on raw; LightGBM trained on 2 countries, Low vs not-Low | holds in direction, numbers conditional | Spearman as released -0.055/-0.073/-0.052; -0.124/-0.113/-0.105 only after excluding the 97/98/99 sentinels (274/220/235 Lesotho rows), which the text does not say. Transfer AUC on all columns 0.81-0.95 vs Lesotho 0.50; on the columns Lesotho has 0.62-0.71 vs Lesotho 0.43-0.48. | EV-1, PROV-13 |
| (implied by 19) | Lesotho's damage is in the label | D comments ("a recording problem") | per-country value counts | incomplete | Lesotho has 12 all-missing columns, among them has_insurance, funeral_insurance, medical_insurance, has_credit_card, keeps_financial_records (the index's main inputs); its codes look garbled: uses_informal_lender "Used to have" 1,677 of 1,944 (86%), friends/family 1,302, loan "Used to have" 454 vs "Never had" 16. Features damaged as well; strengthens the drop. | PROV-13 |
| 21 | Columns a country did not ask are missing for all its rows; Malawi insurance asked of 147, 91% vs 14% | D comments | missingness by country; Malawi routing | holds, with nuance | 147, 0.912 vs 0.140. 117 of the 147 hold some insurance (routing on holding). Asked but no insurance: 17 of 30 non-Low vs 12% of unasked uninsured, so the asked-flag carries label signal beyond the answers on 30 rows (weak). Other partial missingness not mentioned: Zimbabwe has_mobile_money only "Have now" (440) or missing (2,172); Malawi friends/family 78% missing. | LEAK-10 (missingness), CLEAN-14 |
| 22,29 | seven "Don't know" and two "Used to have" spellings; one spelling per column per country | D comments, docstring | enumerate raw values | holds | 7 + 2 spellings; 0 column-country pairs with two spellings | EV-1 |
| 23,30 | Eswatini Yes/"0", Malawi Yes/No, Zimbabwe Yes/missing | D comments, code | crosstab | holds (counts); meaning of "0" inferred | Eswatini 1,265 "0"/1,409 Yes; Zimbabwe 2,162 missing/450 Yes; Lesotho also Yes/missing | EV-2 |
| 24 | 225 Malawi businesses with months, years missing, set to 0, as Eswatini/Zimbabwe record them | D comments | raw counts | holds | 225; Malawi rows with years never have months; Eswatini 208 and Zimbabwe 222 rows years 0 & months>0 | EV-1 |
| 26,30 | ID random "ID_"+6 chars | D | ID format | holds | 9 chars, unique | |
| 27,14 | competition test set random 20% of every country; Test.csv has no labels | D comments | Test.csv from Kaggle mirror | holds | 2,405 rows, no Target; shares 0.2001/0.2/0.2/0.2; 0 ID overlap | SPLIT-5 |
| 28 | "country and the 31 answer columns are categorical" | D comments | dtype count | **refuted (wording)** | 31 categorical features including country, i.e. 30 answer columns + country; 6 numeric holds | writing.md |
| 16 | "37 survey answers" | D comments | raw columns | holds loosely | 37 columns besides ID and Target, country included | writing.md |
| 10,11,12,15,18,38 | dates 2025-12-12 to 2026-03-15, CC BY-SA 4.0, Train.csv 2,126,637 bytes, sha256, 9,618 rows, metric F1 | D, R | Zindi API (api.zindi.world), sha256sum, wc | holds | API: start 2025-12-12, end 2026-03-15, rules "CC-BY SA 4.0", Train.csv 2,126,637, error_metric f1_multiclass ("weighted" not on the page, from the discussion: unverified); local sha256 matches; 9,619 lines | PROV-1, EV-2 |
| 13 | three other uploads hold the same Train.csv | D | Kaggle amishamanga Train.csv sha256 | holds for 1 of 3; 2 untested | identical sha256 | PROV-4 |
| 17, implied | every feature known at the prediction point; no column after the label | D comments | codebook + model comparison | holds for timing; the product columns are parts of the target | all answers from the same interview; the index is computed from them (competition page: four dimensions incl. "access to credit and financial services") | USE-3, USE-6 vs LEAK-10 |
| 6,27, implied | IID split is what the use case needs; no copies across the split | D | duplicate scan; hidden-group probe | holds | 0 duplicated feature rows; near copies 0.4%; no hidden-group hit | SPLIT-1, LEAK-16 |
| 2, implied | the target is the real-world target an actor acts on | D use_case | source page, record | untested (no data test); weak | the FHI is a constructed survey index with an unpublished formula; no lender acting on it is cited (record: use case -) | SEL-3, USE-5 |
| implied | cleaned to the expert state | D | impossible values | refuted (minor) | 6 rows business_age_years > owner_age, kept and not noted | CLEAN-11 |
| 33,34 | no splits_comment; 0 warnings | D README | README bundle checks | holds | 0/0/0 | |
| 35 | domain record vs definition | R | compare | holds (a mismatch) | business & marketing vs finance | |
| 43,45 | FinScope Lesotho p.53 quote; LightGBM with Lesotho 0.317 | the earlier REVIEW.md | | untested | report not read; not re-run | EV-2 |

**Refuted and untested, ranked (principles.md: validity first, Must first)**

1. **P2/P4, Must (SEL-3 via SEL-5's logic, LEAK-10 "a part of the target", USE-5, USE-8): the fit_reason and decision 2
   understate how much of the task is the index formula.** With the same learner, country + the 11 product columns
   beat all 37 columns on 9 of 9 splits (0.255 vs 0.266); the other 26 columns add nothing once the products are in.
   The definition's 0.285-vs-0.260 compares a depth-6 tree with a LightGBM, i.e. capacity, and its 0.260 is not
   reproduced by default LightGBM (0.283). What it changes: issue 2 is no longer "partly recovers"; the measured task
   is "recover an unpublished index from its own inputs, plus noise". Not `Trivial` under TP-4 (no single raw
   feature matches), and SEL-5 is not met literally (unpublished, 93.8% not 100%), so it stays the curator's weighing
   call. Mildest remedy: rewrite fit_reason and decision 2 with the matched comparison (keep with note). Next rung:
   drop the 11 product columns (remaining task 0.694 vs 0.796 class shares, a small real signal, TP-2). Last: `No
   Good Target` (SEL-3), if no actor acts on the FHI class.
2. **P3, Must (USE-5, SEL-3): untested that anyone acts on the FHI class.** The use case "a lender assesses" has no
   source; a lender holding the answers would compute the index, not predict it. Remedy: name an actor from FinMark
   or data.org material, or accept the gap explicitly in fit_reason (USE-8).
3. **P5 (PROV-13): Lesotho drop holds, but the diagnosis is incomplete.** The features are also damaged (12 columns
   absent incl. three insurance columns and credit card; "Used to have" 86% for informal lender), and the Spearman
   figures hold only after excluding 97/98/99 sentinels. Remedy: add both facts to decision 1; no change to the drop.
4. **P4, weak (LEAK-10, missingness): Malawi insurance-block missingness.** Routing mostly on holding insurance
   (benign), but 30 asked-yet-uninsured rows are 57% non-Low vs 12%. Keep with the existing Anomaly note; add the
   routing fact.
5. **P7 (CLEAN-11, CLEAN-14):** 6 rows with business age above owner age kept unnoted; Zimbabwe has_mobile_money is
   "Have now"/missing (missing probably "not held"), like current_problem_cash_flow, undocumented. Remedy: set the 6
   ages to missing or note them; add one line on the Yes/missing coding.
6. **Writing:** "31 answer columns" is 30 plus country; "weighted" F1 not on the Zindi page (the API says
   f1_multiclass). Remedy: correct the wording.

Untested: 2 of 3 mirrors (claim 13), the FinScope Lesotho p.53 quote (43), Zimbabwe/Lesotho interview counts (37),
LightGBM with Lesotho 0.317 (45).

</details>

<details><summary>Column audit</summary>

Frame: the definition rebuilt, 7,674 rows x 38 columns (37 features + `financial_health`), read against the competition's VariableDefinitions.csv. Prediction point (first curation bullet): an institution such as a lender assesses the business from one interview; the FHI describes the business at the same interview. FHI formula: unpublished (a web search found no FinScope "financial health index" definition; LEAK-3 could not be completed).

"Med/High" below = share of rows not Low (base 33.5%).

**Column table**

| column | meaning (codebook) | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| country | country of the business | yes | category, 3 levels | fine | CLEAN-14 |
| owner_age | owner age, years | yes | float, 18-103, no NA; 5 owners >= 90 (max 103, Eswatini) | fine (103 unusual, not impossible) | CLEAN-11 |
| attitude_stable_business_environment | expects a stable environment | yes (attitude at interview) | category Yes/No/Don't know; 2 NA (the 2 near-empty Zimbabwe rows) | fine | |
| attitude_worried_shutdown | worried the business shuts | yes | category; 2 NA | fine | |
| compliance_income_tax | complies with income tax | yes | category incl. `Refused` (8 rows, kept as a category: a real non-answer) | fine | CLEAN-10 |
| perception_insurance_doesnt_cover_losses | perception | yes | category, 5 NA | fine | |
| perception_cannot_afford_insurance | perception | yes | category, 5 NA | fine | |
| personal_income | owner's monthly personal income, local currency | yes | float; 109 NA; Zimbabwe value 99 x2 (a Lesotho sentinel code, plausible here); period appears to differ by country (see problem 6) | fine / note | CLEAN-10, CLEAN-21 |
| business_expenses | "monthly or annual" expenses, local currency | yes | float; 229 NA; Eswatini 98 x1 | fine / note (period ambiguous in the codebook) | CLEAN-21 |
| business_turnover | annual turnover, local currency | yes | float; 216 NA; Eswatini 97 x1 (with expenses 400: maybe a sentinel) | fine / note | CLEAN-10 |
| business_age_years | years running the business | yes | float; Malawi under-a-year set to 0 (225, correct); 27 NA; **6 rows exceed owner_age** (e.g. owner 20, business 25; owner 23, business 40), 33 started before the owner was 10 | cleaning problem | CLEAN-11 |
| business_age_months | additional months beyond full years | yes | float 0-11; Malawi has it only for under-a-year businesses (90.6% NA), consistent with the years fix | fine | |
| motor_vehicle_insurance | business has motor insurance | yes, but an input of the FHI | category; Malawi asked of 147 only; "Have now" 276 rows, 100% Med/High | potential leak kept on purpose (curator's call, problem 1); Malawi missingness (problem 2) | LEAK-10 / USE-6 |
| has_mobile_money | uses mobile money | yes | category; **Zimbabwe only "Have now" (440) or NA (2,172)**: NA = not selected, not "not asked" (Med/High 0.27 vs 0.53) | cleaning question (problem 3) | CLEAN-10 |
| current_problem_cash_flow | currently has cash-flow problems | yes | category; Eswatini "0" -> "No" (1,265); Zimbabwe Yes/NA kept (documented) | fine, but inconsistent with the siblings (problem 3) | CLEAN-10 |
| has_cellphone | business uses a cellphone | yes | category | fine | |
| owner_sex | owner sex | yes | category | fine | |
| offers_credit_to_customers | sells on credit | yes | category | fine | |
| attitude_satisfied_with_achievement | attitude | yes | category | fine | |
| has_credit_card | business uses a credit card | yes, FHI input | category; "Have now" 281 rows, 96.4% Med/High | potential leak kept on purpose (problem 1) | LEAK-10 / USE-6 |
| keeps_financial_records | keeps records | yes | category; Malawi Yes/No, Eswatini/Zimbabwe "Yes, always"/"Yes, sometimes"/No: scale differs by country, recoverable with `country` | fine | CLEAN-14 |
| perception_insurance_companies_dont_insure_businesses_like_yours | perception | yes | category | fine | |
| perception_insurance_important | perception | yes | category, 11 NA | fine | |
| has_insurance | business has any insurance | yes, FHI input | category Yes/No; "Yes" 287 rows, **100% Med/High**; contradicts the product columns (869 Eswatini and 602 Zimbabwe businesses with `has_insurance` No hold funeral cover "Have now"): it reads as business insurance, not "any kind" | potential leak kept on purpose (problem 1); codebook meaning doubtful | LEAK-10; question |
| covid_essential_service | essential service during COVID | yes (retrospective; Malawi 2019 not asked, all NA) | category | fine | |
| attitude_more_successful_next_year | expectation for next year | yes (expectation, not outcome) | category; Zimbabwe not asked | fine | |
| problem_sourcing_money | problem sourcing money at start | yes (past) | category; **Eswatini Yes (1,699) / NA (975)**: NA = not selected; Zimbabwe not asked | cleaning question (problem 3) | CLEAN-10 |
| marketing_word_of_mouth | markets by word of mouth | yes | category; **Eswatini Yes (2,049) / NA (625)**: NA = not selected | cleaning question (problem 3) | CLEAN-10 |
| has_loan_account | formal loan account | yes, FHI input | category; Zimbabwe not asked; "Have now" 92.6% Med/High | potential leak kept on purpose (problem 1) | LEAK-10 / USE-6 |
| has_internet_banking | internet banking | yes, FHI input (likely) | category; Zimbabwe not asked | as above | LEAK-10 / USE-6 |
| has_debit_card | debit card | yes, FHI input (likely) | category; Zimbabwe not asked | as above | LEAK-10 / USE-6 |
| future_risk_theft_stock | expects theft risk | yes (expectation) | category; Eswatini not asked (all NA; the missing-indicator AUC 0.623 is the country effect) | fine | |
| medical_insurance | medical aid | yes, FHI input | category; Malawi asked of 147; "Have now" 404 rows, 100% Med/High | potential leak kept on purpose (problem 1); problem 2 | LEAK-10 / USE-6 |
| funeral_insurance | funeral cover | yes, FHI input | category; Malawi asked of 147; "Have now" 1,608 rows, 100% Med/High; alone AUC 0.790, the strongest column; without it 0.869 vs 0.951 | potential leak kept on purpose (problem 1); problem 2 | LEAK-10 / USE-6 |
| motivation_make_more_money | motivation to start | yes (past) | category; Eswatini not asked; **Zimbabwe Yes (995) / NA (1,617)**: NA = not selected | cleaning question (problem 3) | CLEAN-10 |
| uses_friends_family_savings | informal: friends/family | yes | category; Zimbabwe not asked; Malawi asked of 518 (Med/High 0.24 vs 0.17, mild) | fine | |
| uses_informal_lender | informal moneylender | yes | category; as above | fine | |
| financial_health (target) | FHI class | the label | category Low/Medium/High; no NA | fine | |

ID dropped (random `ID_` + 6 chars, CLEAN-3): correct. No residual alternate spellings of the answers (curly
apostrophes, `?`, U+200E) after the cleaning. No object column (CLEAN-9). No column computed from all rows (CLEAN-7).

**Problems, ranked (principles.md: rank, then strength, then effect)**

**1. P4 (and P3/P6): the product columns are inputs of the target (question for the curator; earlier issue 2)**

* Evidence: every business with any insurance answer "Have now"/"Yes" (has_insurance, funeral, medical, motor) is
  Medium or High (has_insurance Yes 287/287, funeral 1,608/1,608, medical 404/404, motor 276/276); credit card "Have
  now" 96.4%, loan account 92.6%. funeral_insurance alone AUC 0.790 (the best single column); dropping it 0.951 -> 0.869
  macro AUC (leak probe, 3 splits). Earlier panel numbers: depth-6 tree on country + 11 product columns 0.285 vs
  LightGBM all columns 0.260, worse on 9/9 splits.
* Timing: all are answered at the same interview, so they pass USE-3/USE-6/LEAK-37 (known at the prediction point).
  The problem is not time but construction: LEAK-10 (Must) lists "a part, a consequence or another encoding of the
  target: sub-scores that add up to it" as out. The definition records it as `Potential leak, kept on purpose:`, which
  is the form of LEAK-38/LEAK-30; neither fits (LEAK-38 is anonymised, possibly post-outcome company fields; LEAK-30 is
  all-row scaling). A Must has no exceptions, so keeping them needs either the argument that a composite-index input
  known at the prediction point is not "a part of the target" in LEAK-10's sense (the residual is the task, TP-4 not
  met) or an amendment.
* Mildest remedy: keep, but rewrite the note to name the rule it departs from (LEAK-10, "a part of the target") and the
  fact that sets it apart (inputs answered at the prediction point; the index also uses answers not released; TP-4
  not met); the curator decides. The alternative (drop the 11 product columns: 0.695 vs 0.796 class shares) is in
  the earlier REVIEW.md issue 2.
* Also: `has_insurance` does not mean "any kind of insurance" as the codebook says (1,471 businesses with `has_insurance`
  No hold funeral cover now). Reword in the notes if the column stays ("business insurance", inferred).

**2. P4, weak: Malawi's insurance block is asked of 147 businesses, and being asked goes with the label**

* Evidence: Malawi asked 147 vs not 2,241; Med/High 91% vs 14%; "asked" alone AUC 0.646 within Malawi. Not a skip on
  has_insurance (47 Malawi has_insurance Yes not asked; 95 has_insurance No asked). 117 of the 147 hold a product
  (100% Med/High); the 30 asked without one are 57% Med/High against 12% of not-asked has_insurance No.
* Measured (LightGBM, 200 trees, 9 shipped splits): blanking the block for all Malawi costs +0.0175 log loss (9/9), but
  most of that is the product answers themselves; blanking only the 30 asked-without-product rows (the missingness-only
  signal) costs +0.0019 (6/9 worse, mixed). So missingness encodes the label only weakly.
* Rule: LEAK-10 (missingness that encodes the outcome), weak, mechanism unknown (subsample of the questionnaire, not
  shown to be outcome-caused). Remedy: keep with the existing `Anomaly:` bullet; add the measured +0.002 so the note
  says how weak it is. No change to data.

**3. P7: "not selected" stored as missing in five columns, only one of them documented**

* Single-tick answers whose unticked value is NA, not "not asked": Zimbabwe `has_mobile_money` (Have now 440 / NA
  2,172), `motivation_make_more_money` (Yes 995 / NA 1,617), `current_problem_cash_flow` (Yes 450 / NA 2,162); Eswatini
  `problem_sourcing_money` (Yes 1,699 / NA 975), `marketing_word_of_mouth` (Yes 2,049 / NA 625). The definition turns
  Eswatini's cash-flow "0" into "No" and keeps Zimbabwe's NA, and says so only for cash flow.
* Not a leak: the NA is caused by the answer, not by the outcome (has_mobile_money Zimbabwe NA 0.27 vs 0.53 Med/High
  is the answer's own signal). A model separates them through `country`.
* Rule: CLEAN-10 (Should) in reverse (a real answer stored as missing). Mildest remedy: extend the cash-flow bullet to
  the five columns ("Yes or missing in country X: missing means not ticked") rather than recode, since the
  questionnaires are not at hand to prove NA = No.

**4. P7: impossible business ages**

* 6 rows with `business_age_years` > `owner_age` (e.g. owner 20 / business 25 years; 23 / 40; 29 / 47), 33 rows where
  the business started before the owner was 10. Rule CLEAN-11 (Should): impossible values become missing, row stays.
  Remedy (cheap and safe): set `business_age_years` (and months) missing where it exceeds `owner_age`; leave the
  merely unusual rows. owner_age 103 stays (unusual, not impossible).

**5. P7: possible stray sentinels in the amounts**

* After the Lesotho drop: Eswatini business_expenses 98 (1 row) and business_turnover 97 (1 row, with expenses 400),
  Zimbabwe personal_income 99 (2 rows). These were Lesotho's codes; here they are ambiguous. CLEAN-10 (Should) only when
  the encoding can be inferred: no change; at most the turnover 97 row. Negligible.

**6. P7: the amounts' periods differ by country**

* Median personal_income / business_turnover: Eswatini 0.33, Malawi 0.33, Zimbabwe 0.06 (~1/12); expenses/turnover
  0.5-0.56 everywhere. The codebook calls income monthly, turnover annual and expenses "monthly or annual". So at least
  one amount's period differs between Zimbabwe and the others (or Malawi's income is annual: median 270,000 MWK).
  CLEAN-21 (Should, one unit and scale per column); mitigated as the currency is, by `country` being a column. Remedy:
  extend the "local currency" bullet to say the periods may differ by country (question for the curator; no recode
  without the questionnaires).

**7. Procedure (notes vs data)**

* dtypes bullet: "country and the 31 answer columns are categorical" — 31 categorical features including country (30
  answers). Intro "37 survey answers" counts country. Fix the wording (writing.md).
* Two Zimbabwe rows (2869, 7329) are near-empty interviews (both Low): kept, harmless (CLEAN-11 weighed factor), no
  action.

No column was recorded after the label; no identifier encodes the label; no all-row statistic (CLEAN-7, LEAK-29); no
proxy codes remain in owner_age.

Sources: [FinScope MSME Eswatini 2023 report](https://finmark.org.za/Publications/Eswatini_2023_Report_web.pdf) (search
hit, not read in full).

</details>

<details><summary>Split audit</summary>

**Verdict: right with notes**

The IID split mirrors the use case as written. One row is one business interviewed once in a one-off national
cross-section; the actor (a lender) assesses a business it has not seen, and nothing about that business is known
before the interview, so there is no history to exploit and no entity recurs (USE-10, USE-11: first and only event per
entity -> IID without grouping). No time axis exists inside a survey (one interview wave per country), so SPLIT-7/8 do
not force a temporal regime. Country is a feature every new row keeps (SPLIT-4), not a group.

**Measured facts**

* Shipped splits: 3 repeats x 3 folds, train 5,116 / test 2,558, no train/test overlap, each repeat's test sets cover
  all 7,674 rows once. Stratified by class (test shares Low 0.665, Medium 0.274, High 0.060-0.061 in every fold);
  country shares per test fold 0.296-0.362 against 0.311-0.348 overall (not stratified by country, close enough).
* Raw file order carries no structure: IDs random and unsorted; 7,192 country runs in 9,618 rows (file shuffled);
  within each country, neighbour label agreement equals chance (Eswatini 0.419 vs 0.415, Malawi 0.690 vs 0.683,
  Zimbabwe 0.545 vs 0.555) and neighbour feature agreement equals a random pairing (0.558/0.557, 0.556/0.557,
  0.599/0.600). No block or enumeration-area order to recover (SPLIT-22 not applicable).
* Hidden-group probe: no hits; top candidates business_expenses (gap +0.008), business_turnover (+0.005), owner_age
  (+0.002) are features new rows keep. Composite keys (all but one or two columns): none. Exact copies across the split
  0.0%; near copies at 0.85 similarity 0.4% of rows, largest cluster 3. No hidden entity (SPLIT-29 not triggered).
* Alternative split, unseen country (untuned LightGBM 200 trees, lr 0.05):

  | Held-out country | unseen-country log loss | train class shares | IID on the same rows | its own class shares |
  |---|---|---|---|---|
  | Eswatini (2023, newest survey) | 0.669 | 1.106 | 0.346 | 0.958 |
  | Malawi (2019) | 0.504 | 0.686 | 0.323 | 0.580 |
  | Zimbabwe (2022) | 0.225 | 0.735 | 0.149 | 0.706 |

  Shipped IID: 0.283 +- 0.011 over 9 splits. Class shares differ strongly by country (High 11.5% Eswatini, 4.0% Malawi,
  2.3% Zimbabwe; Low 51.4 / 81.2 / 68.6%), and the countries asked different questions (columns missing for a whole
  country), so an unseen-country split is a domain-shift test over 3 groups, which the "only a few groups" factor in
  splits.md (covertype) argues against. The Eswatini column also stands for "train on older surveys, test the newest":
  the score more than doubles.

**Problems, ranked**

1. **P4 / SPLIT-31 (Should), SPLIT-5 (Must) - the score is optimistic for any deployment outside the surveyed
   cross-sections; note, not a fix.** Evidence: the table above (Eswatini 0.346 IID vs 0.669 trained on the two older
   surveys; Malawi 0.323 vs 0.504). A lender would use the model on businesses interviewed later or in another country,
   not on held-out rows of the same survey wave. With three surveys, each its own country and year, time and country
   are confounded and only 3 groups exist, so neither a temporal nor a grouped split is sound (SPLIT-14 needs 3 windows
   with >= 50% train; the few-groups factor). The IID split matches the task as framed and as the competition set it.
   Remedy: none to the split; add one sentence to `split` or the curation comments that the test stands for other
   businesses of the same survey waves, and that a model trained on Malawi 2019 + Zimbabwe 2022 scores Eswatini 2023 at
   log loss 0.669 against 0.346 under IID (candidate for a cross-country variant, SPLIT-31). The task_summary `split`
   already says "other businesses of the same surveys", so this is a note, not a correction.
2. **P4 / SPLIT-5 (Must) - the competition's split claim is not re-verified.** The comment says the Zindi test set is "a
   random 20% of every country". Test.csv is not in the local warehouse (only Train.csv and VariableDefinitions.csv), so
   the per-country share could not be checked; the claim does not change the shipped split (we split Train.csv
   ourselves). Remedy: unzip Test.csv once and record its per-country counts, or soften to "the competition's test set
   is random rows" with the source cited.
3. **P4 / SPLIT-24, SPLIT-25 - FinScope samples by enumeration area; the cluster id is not released.** Businesses of one
   sampled area could share location effects across the split. Evidence that it does not matter here: shuffled file,
   no hidden-group hit, 0.4% near copies, neighbour agreement at chance. Rule SPLIT-24 bars grouping on a guessed
   cluster, and nothing suggests the area carries the label beyond country. Remedy: none; mention only if FinMark
   Trust's microdata with area codes are ever used.

Not problems: no temporal checks apply (no time column, no label delay: the index is set at the same interview, so no
training row has an unknown label at the prediction point, SPLIT-9/10); no grouping declared and none needed (one row
per business, USE-11); class stratification is fine (smallest class per test fold 154 rows, task probe).

</details>

<details><summary>Domain practitioner</summary>

**Fit**

**Approximate (agree with the definition).** The label is a survey-built index (FHI) whose "access to credit and
financial services" dimension is computed from the very product columns we ship, and nobody acts on the FHI class
itself: a lender acts on repayment, a programme on need. The task stands in for "screen a business's financial health
from a short interview" with a named gap (USE-5, USE-8: a potential leak kept on purpose).

**Who I am and what I decide**

The definition's actor is "an institution, such as a lender". The Zindi page names two users: financial institutions
assessing credit risk, and development partners or governments finding vulnerable businesses to direct support. I
read it as both and found the second fits better.

1. **Inputs at the prediction point (USE-3, USE-6).** All 37 columns are answers from one interview, so all are
   known when I decide; nothing is recorded after the label. What I would not have or not trust:
   - As a lender, I would not take self-reported attitudes ("worried the business will shut down", "will be more
     successful next year") at face value in an application; they are gamed once they affect the decision.
   - Each deployment uses one questionnaire. Here Zimbabwe has no loan account, debit card or internet banking
     answers (100% missing), Eswatini no theft risk, Malawi no COVID question, and Malawi has insurance answers for
     only 6% of its businesses (measured on Train.csv without Lesotho). Pooling three questionnaires is a benchmark
     artefact, not my setting. Malawi's insurance block (147 businesses, 91% Medium or High against 14%) ties
     missingness to the label in a way no real form would.
   - What I would always have but is missing: sector or traded commodity, location (urban or rural), number of
     employees, formal registration. The Zindi page itself says the FHI is predicted "from traded commodities, trade
     activity, demographics, firm size and location", and none of these is in the release. As a lender I would also
     have credit-bureau or mobile-money transaction history.
2. **Target (USE-5).** The FHI has four dimensions (Zindi page): savings and assets, debt and repayment ability,
   resilience to shocks, and access to credit and financial services. The fourth is the 11 product columns, which is
   why a depth-6 tree on them reaches log loss 0.285 against 0.260 for all columns. The residual comes from the other
   three dimensions, whose questions were not released. For a lender the FHI is a proxy for repayment, and a distant
   one. For a programme officer the FHI class is close to what I act on (who gets support). Either way I want a
   probability of Low to rank businesses for outreach, not a hard class, so log loss over the three ordered classes
   suits me better than the competition's weighted F1.
3. **Row and test data (USE-10, USE-11).** One row is one business at one interview, and one decision is one
   business: it matches. A business appears once, so it is a cold start for a new business, and IID is right for
   that. But what I would face is the next survey wave or a screening round a year later, not a random 20% of the
   same cross-section. The surveys date from 2019 to 2023, and no later wave is in the data. Under the factor "a use
   case rephrased only to excuse a gap", the random split stays approximate.
4. **Would I use it?** Not as a lender: the target is not repayment, and I have better data. As a programme officer,
   only if I could not get the FHI formula. Anyone holding the full FinScope answers and FinMark's formula would
   compute the index, not predict it. The real case is a short screening form (fewer questions than the full
   survey) that predicts the class the full module would give. This is the proxy-means-test pattern of social
   protection targeting. I would trust it with a published formula, calibration checked per country, and a check on
   a later wave. Two things make me distrust it: Lesotho's labels run against the index's own parts (dropped), which
   says the label pipeline is not verified, and the FHI's construction is unpublished.

**Gaps, ranked by how much they change the task**

1. **The label partly equals a function of the features (USE-5, USE-8, USE-12).** The task is "reproduce the
   access-to-finance dimension and impute the three unreleased dimensions". The definition names this as a potential
   leak kept on purpose. The Zindi page's four dimensions make it firmer than "computed from survey answers, among
   them the insurance and credit products": one of the four dimensions is these columns.
2. **The actor in `use_case` is the weaker of the two the source names (USE-1, USE-5).** For a lender the FHI is a
   proxy for repayment. For a development partner or government screening businesses for support (the Zindi page's
   second use), the FHI class is close to what is acted on. USE-9 does not make the fit direct: the split and the
   pooled questionnaires still differ from that use.
3. **Pooled questionnaires (USE-3).** No single actor faces the pattern where whole columns are missing for one
   country, or Malawi's insurance block, which is linked to the label. It is kept and named in the `Anomaly:` bullet.
   For the benchmark it is a fair property of the data; for the use case it is a gap.
4. **Random split of one cross-section per country (USE-10, SPLIT).** The test set stands for other businesses of
   the same survey, not the next wave. A known, named gap; no newer data exists to fix it.
5. **Missing inputs a practitioner would have.** Sector, location, size and registration are named by the source but
   not released. This lowers the ceiling but does not change the task.

**What a domain expert would change**

- Rewrite `task_summary.use_case` around the source's second user: "a development partner or government agency
  screens a small business from one interview, to decide whether it gets support (for example, a short FinScope-style
  form standing in for the full Financial Health Index)". Keep "a lender" only as a secondary reading. Keep the fit
  approximate (USE-8, USE-9 weighed against the rephrasing factor).
- In the "Potential leak, kept on purpose" bullet and in `fit_reason`, name the FHI's four dimensions from the
  competition page and say the fourth (access to credit and financial services) is the product columns. Today's
  wording ("computed from survey answers, among them...") understates it.
- Optionally (curator's call, not required): a variant without the 11 product columns would be "predict financial
  health from business characteristics". It is a weaker task (log loss 0.695 against 0.796 for the class shares,
  the earlier REVIEW.md issue 2) but closer to a screen run before the products are known. I would not make it the main
  task: the products are known at the interview (USE-6).
- Mention in the comments that the competition page lists firm size, location and traded commodities as inputs that
  the released Train.csv does not contain, so a reader does not look for them.

**Sources**

- Zindi competition page: https://zindi.world/competitions/dataorg-financial-health-prediction-challenge (four FHI dimensions, intended uses, F1 metric).
- Zindi discussions 31219 and 31765 (no organiser information on how the FHI was computed).
- FinScope Eswatini 2023 report and UNDP pages (survey scope): https://finmark.org.za/Publications/Eswatini_2023_Report_web.pdf, https://www.undp.org/eswatini/publications/finscope-blended-msme-survey-findings-report-eswatini-2023

</details>

<details><summary>Blind review</summary>

**Verdict**

Include with changes. The data is real SME survey data with a real use case and a reasonable size. However, the target is a composite index computed from survey answers, and several of the inputs to that index are columns in this table. A large part of the benchmark therefore measures how well a model can reconstruct the index formula. Document this, and either drop the features that feed the index or label the task as formula reconstruction. Also state why Lesotho is missing.

**Task**

- 7,674 rows and 37 features. The target is `financial_health` with three classes: Low 5106, Medium 2104 and High 464.
- The data comes from SME surveys in Eswatini, Zimbabwe and Malawi.
- Zindi says the users would be "financial institutions ... assess credit risk" and "development partners and governments ... target support".
- The Financial Health Index (FHI) is "a composite measure ... across four dimensions: savings and assets, debt and repayment ability, resilience to shocks, access to credit and financial services". It is "derived from survey and business data". The weights and thresholds are not published.

**Concerns, most serious first**

1. **The target is built from feature columns.** The index's "access to credit and financial services" dimension shows up directly in the features, so the task partly reproduces a deterministic scoring rule.
   - Owning any insurance gives 0 Low out of 1,896 rows: `has_insurance`=Yes, or funeral, medical or motor insurance "Have now". Without any insurance, 5,106 of 5,778 rows are Low.
   - `funeral_insurance`="Have now" gives 0% Low. `has_loan_account`="Have now" gives 7% Low against 71% for "Never had".
   - LightGBM with 5-fold CV reaches accuracy 0.919, macro-F1 0.842 and log loss 0.252, against a prior log loss of 0.796. The top features by gain are funeral_insurance (by far the largest), has_loan_account, has_credit_card, has_insurance and motor_vehicle_insurance.
   - With the 11 financial-access and insurance columns removed, macro-F1 falls to 0.44 and accuracy to 0.68, against a majority-class accuracy of 0.665.
   - The competition was set up this way, so this is not a leak in the strict sense: it is the stated task. But it is circular, and real-world value for credit scoring is limited, since anyone who has these answers can just compute the FHI.
   - Change: document it at minimum. Better, also offer a variant without the index-component columns. That variant is not trivial but has weak signal.

2. **Missingness is set by country and questionnaire.** Many columns are 100% missing for whole countries:
   - has_loan_account, has_debit_card and has_internet_banking are 100% missing in Zimbabwe.
   - covid_essential_service is 100% missing in Malawi.
   - future_risk_theft_stock is 100% missing in Eswatini.
   - The insurance columns are 94% missing in Malawi.

   So NaN encodes the country or survey wave. This is not leakage, but say it in the notes. Consider an explicit "not asked" category.

3. **Money columns are in local currencies and not comparable.** personal_income, business_expenses and business_turnover have medians of 2,250, 5,000 and 10,000 and maxima of 1.5e8, 5e8 and 4.2e8. They mix the currencies of three countries (SZL, MWK and ZWL/USD) and contain extreme outliers. Tree models can cope through `country`, but note it, or add log or per-country normalisation as a documented choice.

4. **The population differs from the source.** Zindi lists four countries, including Lesotho, but this table has only three. I could not verify whether Lesotho was dropped on purpose (for example, if it appears only in the test file) or whether rows were lost. The Zindi files list Train.csv at 2 MB, and the row count could not be checked without logging in. State the reason in the dataset notes.

5. **Minor issues:**
   - business_age_years and business_age_months are two parts of one quantity. Months is missing in 2,167 rows, mostly in Zimbabwe. A combined age could be derived.
   - keeps_financial_records mixes "Yes" with "Yes, always" and "Yes, sometimes", which shows different questionnaire wordings.
   - There are no duplicate rows, including when the target is ignored.
   - The column types are sensible (category and float).
   - Owner age runs from 18 to 103, which is plausible.

**Split**

A random IID split with 3 repeats and 3 folds is fine for a cross-sectional survey, and no time column is present. Country is a feature, so a country-grouped split would be a harder alternative. It is not needed.

**Signal and size**

There is enough rows and signal. The High class has 464 rows, about 155 per test fold under 3-fold CV. That is acceptable but makes macro-F1 noisy. Use log loss or AUC for ranking.

**Could not check**

- The original row counts in Train.csv and whether there was any filtering or deduplication (Zindi requires a login).
- The exact FHI formula.
- The full VariableDefinitions.csv.
- Whether the Zindi test labels were ever released.

</details>

<details><summary>Precedent check</summary>

**What there is to check.** The record holds no `CC` line: the only curator text is the imported "Evaluation: F1". All
decisions below are the AI's (the definition and the 2026-10-07 / 2026-10-20 assessments), not yet accepted by a
curator, so there is no drift and no curator self-contradiction to report. The register raises no flag that involves
this dataset; it files issue 2 under the mechanism "trivial" as an open issue only (the "trivial" opposite-outcomes
flag is about anneal, haberman, fitness_club, aps_failure and others, not this dataset).

**Summary**

| # | Decision | Verdict | Closest precedents |
|---|---|---|---|
| 1 | Keep the 11 product columns although the FHI is computed from such answers ("Potential leak, kept on purpose") | **not reasonable under the ranking** as written (departs from LEAK-10, a Must, and from the SEL-5 remedy; the reasons given name no higher Must) | account_debt_south_africa (rule inputs dropped, 2026-10-07/12), central_international_... (NEWS2, `No`, 2026-10-12), mutual_funds_india `rating` (dropped 2026-10-01), UCI student performance G1/G2 (LEAK-10 Cases) |
| 2 | Drop Lesotho's 1,944 rows (label built differently) | consistent, with a stated reason; PROV-13 origin check still open | account_debt_south_africa (20.2% unrecorded runs dropped; its issue 1 also still open), biogeographical_ancestry_prediction (Turkey dropped, 2026-09-30), caracas_cervical_cancer (108 unrecorded patients, 2026-10-15), zillow_prize (biased months dropped) |
| 3 | Malawi's insurance block asked of 147 businesses, 91% Medium/High, kept as an `Anomaly:` | departs without a stated reason (LEAK-10, missingness that encodes the outcome) | mic (prediction point moved, LEAK-10 Cases), kick `WheelType` (kept under LEAK-38, 2026-10-01), caracas (unrecorded rows dropped, 2026-10-15) |
| 4 | 6 rows with business_age_years > owner_age left as they are | departs without a stated reason (CLEAN-11, Should), likely a reasonable exception | caracas_cervical_cancer, churn_telco_south_asia, thyroid_discordant (impossible values to missing) |
| 5 | Log loss instead of the competition's weighted F1 | consistent | african_credit_scoring_challenge (F1 -> ROC AUC), zillow_prize (MAE -> RMSE), huntprohibited_1m, g_research_crypto_forecasting_1m |
| 6 | `year = "2025"` (competition launch; surveys 2019-2023) | consistent with PROV-9; the "open year-convention question" is answered by PROV-9, and the only open point is a PROV-8 fact | PROV-9 (Lennart, 2026-10-12 / 10-14); airfoil_self_noise, first_principles_tully_fisher (2026-10-20) |
| 7 | `domain`: record `business & marketing`, definition `finance` | definition consistent with siblings; the record should follow | account_debt_south_africa, african_credit_scoring_challenge, home_credit_default_risk (all `finance` in both) |
| 8 | IID split, country a feature | consistent | the competition's random 20% per country; SPLIT-1; hidden-group probe no hits |
| 9 | Spellings unified, Eswatini "0" -> "No", Zimbabwe's missing kept missing, Malawi's months -> years 0, ID dropped, amounts in local currency | consistent | CLEAN-2 (no imputation: Zimbabwe's missing stays), CLEAN-3, CLEAN-12, CLEAN-21 |
| 10 | Fit `approximate` with a kept potential leak as the named gap | consistent in form | kick, account_debt_south_africa (USE-8 Cases) |
| 11 | No accepted check warnings | nothing to compare | |

**1. Product columns kept (issue 2): LEAK-10, SEL-5, USE-5**

**What the definition does.** The 11 product columns (insurance, credit and other formal products) stay, with a
`Potential leak, kept on purpose:` bullet. Measured: none of the 1,896 insured businesses is Low; a depth-6 tree on
country + 11 products reaches log loss 0.285 against 0.260 for LightGBM on all columns, LightGBM on country + products
alone 0.255 (better than all columns on 7 of 9 splits), the 26 other columns 0.695, class shares 0.796. Reasons given:
the business reports them at the assessment; the competition predicts from all columns; the formula is unpublished.

**Precedents.**

* account_debt_south_africa (AI assessment 2026-10-07; CC 2026-10-12, Lennart; SEL-5 Cases "applied"): the label is a
  rule of `total90debt`, `totalwriteoff`, `debtbillingratio` (all but 371 rows), so the columns were dropped and the
  rest kept as a real task (ROC AUC 0.874). Also a finance task from Africa with fit `approximate`.
* central_international_medical_college_and_hospital_health_risk_prediction (CC 2026-10-12, Lennart): the label is the
  NEWS2 chart of the shipped vital signs, a published rule whose inputs are the whole task: `No`, `Trivial` (SEL-5).
* mutual_funds_india (CC 2026-10-01, Lennart): `rating` dropped, though known at snapshot time, because it is computed
  from the window that defines the target (LEAK-10 Cases, "Snapshot data").
* UCI student performance (LEAK-10 Cases): G1 and G2, parts of the final grade, dropped although known before G3.
* The other `Potential leak, kept on purpose` notes in the collection (kick, homesite, african_credit_scoring,
  aeolus_1m, onlinenewspopularity, zillow_prize, distribution_transformers, phiusil, the LEAK-30 notes) all keep a
  suspect whose measured effect is small (at most 0.05 AUC) or is covered by a narrowing rule (LEAK-11, LEAK-30 weak,
  LEAK-38 anonymised host fields). churn_telco_south_asia (CC 2026-10-15, Lennart) kept an unverified window-timing
  suspicion. None keeps a component of the target with an effect of this size (log loss 0.695 -> 0.260).

**Comparison.** The facts that matter for LEAK-10 ("a part ... or another encoding of the target ... drop it", Must)
are the same as in account_debt and student performance: the label is built from answers that are columns. The
differences the definition offers:

* the formula is unpublished and the products do not decide the class alone (depth-6 tree worse on 9 of 9 splits).
  This keeps the case out of SEL-5's letter ("published, deterministic"), and keeps it from `Trivial` (TP-4), but
  LEAK-10's "a part of the target" has no such condition, and account_debt's rule was not deterministic either (371
  exceptions);
* the products are known at the interview (USE-6, LEAK-37). mutual_funds `rating` and G1/G2 were known too and were
  dropped: knowing a component at prediction time does not make it a non-leak under LEAK-10;
* the competition uses all columns. That is no higher principle: CLEAN-20 copies a competition's preprocessing, not
  its exploits, and LEAK-38 (the host-design carve-out) covers anonymised, possibly post-outcome fields, not inputs of
  the label.

So keeping the columns departs from a P4 Must, and no higher-ranked Must is named. Under "Exceptions and amendments" a
Must has no exceptions: this is either treated like account_debt (drop the product columns; the remaining task scores
0.695 against 0.796, a small real signal that TP-2 keeps) or the curator amends LEAK-10 / SEL-5 deliberately.

**A fact to settle first (EV-1, PROV-16).** "The FHI is computed from survey answers, among them the insurance and
credit products" carries no source reference in the definition or the record (no page, section or quote from
data.org, Zindi or FinMark). The measurement (0 Low among 1,896 insured) is circumstantial. If data.org's methodology
names the FHI's inputs, cite it; if it does not, the call is between "inputs of the index" (LEAK-10) and "strong
ordinary predictors of financial health" (USE-6), and the second would let the columns stay without any exception.
This fact decides which precedent applies.

**A second question the precedent raises (USE-5, SEL-3).** account_debt's label is an observed outcome (bad debt) and
central_international's a published clinical score; this label is a survey index with an unpublished formula, neither
an observed outcome nor an expert annotation (SEL-3). The checklist marks P2 and P3 as concerns. That is a validity
question above issue 2, for the curator to weigh, and it is where the record's "use case -" sits.

```text
**Consistency check (AI, 2026-10-20):** your call on dataorg_financial_health_prediction_challenge (keep the 11 product
columns, a departure from LEAK-10, a Must) differs from account_debt_south_africa (2026-10-12: the label's rule inputs
dropped, the rest kept as a task) and mutual_funds_india (2026-10-01: `rating` dropped although known at snapshot
time), the same mechanism: features that are inputs of the label. What sets dataorg apart?
(a) the FHI's formula is unpublished and the products are not shown to be its inputs (only "0 Low among the insured"),
    so they count as ordinary predictors a lender sees (USE-6), recorded with the source that settles it;
(b) treat it like account_debt: drop the 11 product columns (log loss 0.695 against 0.796 for the class shares; TP-2);
(c) reopen account_debt_south_africa to match;
(d) change the rule: amend LEAK-10 / SEL-5 so that inputs of an unpublished, non-deterministic index may stay with a
    note (a deliberate change, with this case in the Cases table).
```

**2. Lesotho dropped (issue 1): PROV-13, LEAK-14 by analogy, CLEAN-11 ("a row leaves only when...")**

**Precedents.**

* account_debt_south_africa (definition; AI 2026-10-07, CC 2026-10-12): 27,938 rows (20.2%) in seven runs where debt
  was not recorded dropped, measured by a label pattern that differs from the rest. Its REVIEW issue 1 ("retire is an
  alternative") is still open for the curator (assessment 2026-10-20).
* biogeographical_ancestry_prediction (CC 2026-09-30, Lennart): the Turkey class dropped for a genotyping artefact of
  its source (LEAK-14).
* caracas_cervical_cancer (CC 2026-10-15, Lennart): 108 patients whose results look unrecorded dropped.
* zillow_prize: months the source calls a biased sample dropped.
* ghanas_indigenous_intel (CC 2026-10-01, Lennart): a recording problem that could not be recovered retired the whole
  dataset ("Revisit if ... the organisers can say").

**Comparison.** Same kind of decision as account_debt and caracas: a block of rows whose label was recorded
differently, identified by measurement (direction of every formal-finance answer reversed, cross-country AUC 0.46
against 0.63-0.68) and backed by the source's own document (FinScope Lesotho report, p. 53, quoted). The block is one
country with country as a column, so the drop is clean and the rest is unaffected (unlike ghana, where the problem ran
through the whole table). **Consistent, with a stated reason.**

Two notes, not departures:

* PROV-13 (Must) asks to check the origin before keeping or cutting around damage. The definition says FinMark Trust
  and data.org were not asked ("Revisit if ... explain"). Same state as ghana's and account_debt's revisit notes; a
  `Data Requested` marker would make it trackable if a request is sent.
* account_debt's similar drop is still an open curator question. The two should be decided alike: if the curator
  prefers "retire rather than cut" for one, the other follows (LEAK-8, "retire rather than invent structure", is the
  rule that would argue the other way; a whole country identified by a column is not invented structure).

**3. Malawi's insurance block (LEAK-10, missingness that encodes the outcome)**

Malawi asked the three insurance products of 147 of its businesses: 91% of them Medium or High against 14% of the
others. The definition keeps this as an `Anomaly:` and gives no reason why the missingness is not outcome-coded.
Precedents: mic (LEAK-10 Cases: missingness that encodes the outcome; prediction point moved), kick `WheelType`
(missing 70.5% bad buys, kept under LEAK-38 as a host-designed field, CC 2026-10-01), caracas (unrecorded rows dropped,
2026-10-15). The likely distinguishing fact is questionnaire routing: if the insurance questions were asked only of
businesses that answered yes to `has_insurance` (a feature), the missingness repeats a known answer and is not caused
by the label. That is not written down. **Departs without a stated reason.**

```text
**Consistency check (AI, 2026-10-20):** your call on dataorg_financial_health_prediction_challenge (keep Malawi's
insurance answers, missing for all but 147 businesses, 91% of those Medium/High) departs from LEAK-10 (missingness that
encodes the outcome) as applied to mic (prediction point moved) and caracas_cervical_cancer (2026-10-15: unrecorded
rows dropped). What sets it apart?
(a) the questionnaire routes the insurance questions by the `has_insurance` answer, itself a feature, so the
    missingness repeats a known input, recorded as the reason (check the Malawi 2019 questionnaire);
(b) treat it like caracas or mic: set Malawi's three insurance columns to missing for all its rows, or drop them for
    Malawi;
(c) reopen the precedents;
(d) change the rule.
```

**4. business_age_years > owner_age in 6 rows (CLEAN-11, Should)**

Caracas (a first intercourse after the current age), churn_telco (a negative network age) and thyroid_discordant (age
455) made impossible values missing. The definition is silent on the 6 rows. A business older than its owner is
possible when it was inherited or taken over, so these may be unusual rather than impossible ("values that are only
unusual stay"). Small and a quality matter (P7). **Departs without a stated reason**; the likely reason makes it
consistent.

```text
**Consistency check (AI, 2026-10-20):** your call on dataorg_financial_health_prediction_challenge (leave 6 businesses
older than their owner as they are) differs from caracas_cervical_cancer, churn_telco_south_asia and
thyroid_discordant (impossible values made missing, CLEAN-11). What sets it apart?
(a) a business can be older than its owner when it was inherited or bought, so the values are unusual, not impossible;
    recorded as a one-line note;
(b) treat it like caracas: set business_age_years (and months) to missing in these rows;
(c) reopen the precedents;
(d) change the rule.
```

**5. Metric: log loss instead of weighted F1**

african_credit_scoring_challenge (F1 -> ROC AUC), zillow_prize (MAE -> RMSE), huntprohibited_1m (AP@32500 -> ROC AUC)
and g_research_crypto_forecasting_1m (weighted Pearson -> RMSE) all keep the collection's default and say so.
**Consistent.** TP-6 lists "the scoring it uses" as part of a better version the source defines; no shipped dataset has
applied that to the metric, since the collection supports only its three metrics. Not a departure.

**6. Year 2025**

PROV-9 (Must; Lennart, 2026-10-12 and 2026-10-14) sets the year of a competition to its launch, "not the collection
period": 12 December 2025 gives 2025. **Consistent.** The REVIEW's "open year-convention question" is answered by
PROV-9. What is open is a PROV-8 fact: if FinMark Trust published the FinScope MSME microdata with the FHI class before
the competition (a data portal release), the source and year would be that release, as for a re-upload of a
government survey. If the FHI class was made for the competition, Zindi 2025 stands.

**7. Domain**

The record says `business & marketing`, the definition `finance`. The finance tasks of the copy (account_debt_south_africa,
african_credit_scoring_challenge, home_credit_default_risk) are `finance` in both places, and the FinScope sibling
records (financial_inclusion_in_africa_for_botswana, indabax_tanzania_mobile_banking_prediction_challenge, both AI
unverified) are `finance`. The definition is consistent; the record field is the one to align.

**8-11. Split, cleaning steps, fit, warnings**

* IID as in the competition (random 20% per country), one business per row, hidden-group probe without hits: SPLIT-1,
  consistent with the cross-section surveys of the collection.
* Keeping Zimbabwe's missing `current_problem_cash_flow` missing while recoding Eswatini's "0" to "No" is consistent:
  turning a missing value into "No" would be imputation (CLEAN-2, Must), recoding a code is not.
* Malawi's under-a-year businesses set to 0 years from their months: one unit per column (CLEAN-21), consistent.
* Fit `approximate` naming a kept potential leak follows kick and account_debt (USE-8 Cases); it stands or falls with
  decision 1.
* No accepted check warnings; nothing to compare.

**Drift and third exceptions**

* No curator decision on this dataset yet, so no drift.
* If decision 1 is kept as written, it would be the first keep of an asserted (not merely suspected) target component
  with a large effect. Counting the looser family, "a LEAK-10 suspect kept with a note outside LEAK-11/30/38", it would
  be the second curator-approved case after churn_telco_south_asia (2026-10-15); a third of that kind would call for an
  amendment of LEAK-10.

</details>

<details><summary>Advocate</summary>

Position: ship. Data, split and signal hold. One real problem: the product columns under LEAK-10. It is fixed in the
definition, not by excluding the dataset.

**1. The data is what it claims to be (P5, PROV-1/PROV-4/PROV-13, Must: holds)**

- Evidence (claim audit): the Train.csv sha256 matches. Its byte size matches the Zindi API. An independent Kaggle
  mirror is byte-identical. Eswatini Train+Test is 2,674+669 = 3,343, exactly the interview count of FinScope MSME
  Eswatini 2023. Malawi has 2,985 of 2,993 interviews. Test.csv is a random 20.0% of every country, with 0 ID overlap.
  The licence (CC-BY SA 4.0) and the dates are confirmed from the API.
- The Lesotho drop is stronger than the definition says. Besides the inverted label, Lesotho lacks 12 columns (among
  them three insurance columns and the credit card). Its codes look garbled ("Used to have" an informal lender: 86%).
  Its transfer AUC is 0.43-0.50, against 0.62-0.95 for the other countries.
- Precedents: account_debt_south_africa, caracas_cervical_cancer and biogeographical_ancestry each drop a block whose
  label was recorded differently (precedent checker: "consistent").
- Mildest remedy for the gaps found: add both facts to decision 1, and say that the Spearman figures exclude the
  97/98/99 sentinels. The data does not change.

**2. A real use case exists, named by the source (P3/P2, USE-1, USE-5, SEL-3, Must)**

- Evidence: the Zindi page names two users. One is "development partners and governments ... target support"
  (clean-room report, practitioner). For that user the FHI class is "close to what I act on" (practitioner). The task
  is the proxy-means-test pattern of social-protection targeting: a short form predicts the class that the full
  module would give.
- The FHI is FinMark Trust's expert-built measure with four named dimensions. It is not an unsupervised cluster
  (SEL-4) and not a published deterministic rule (SEL-5).
- Concession: no source shows a lender acting on the FHI class, so the lender framing is unsupported.
- Mildest remedy: rewrite `use_case` around the screening actor and keep the fit `approximate` (USE-8, USE-9 weighed).
  This is a text change. The weak lender framing is a writing fault, not a missing use case, so it does not call for
  `No Good Target`.

**3. The split mirrors the application (P4, SPLIT-1/SPLIT-5, Must: holds)**

- Evidence (split audit, "right with notes"): one interview per business, one cross-section per country. The hidden-
  group probe has no hits. There are 0 exact copies across the split and 0.4% near copies. Neighbour agreement in file
  order is at chance. The split matches the competition's random 20% per country.
- A country-held-out split scores worse (Eswatini 0.669 against 0.346 under IID). With 3 groups that confound country
  and year, that is a note under SPLIT-31, not a re-split (the few-groups factor in splits.md).
- Remedy: one sentence in `split`.

**4. Worth benchmarking and not Trivial (P6, TP-4 Must, TP-2)**

- Evidence: the task probe raises no flags (best skill +0.663). No single raw feature matches the best models. The
  majority class within identical product profiles covers 93.8%, not 100%. A depth-6 tree on the products is worse
  than LightGBM on 9 of 9 splits. High has about 154 rows per test fold.
- TP-4 needs proof, and the panel has none.

**5. The product columns: concede the departure, fix it in the definition (P4, LEAK-10, Must)**

- The real problem, conceded. The claim audit refutes "partly": with the same learner, country plus the 11 product
  columns beat all columns on 9 of 9 splits (0.255 against 0.266). The Zindi page lists "access to credit and
  financial services" as one of the four FHI dimensions. The fit_reason and decision 2 understate this.
- USE-6 (P3, "anything known at the prediction point") does not rescue the columns. The tension row "a real task
  against a leak" says fix the leak and keep the task. The precedents mutual_funds_india `rating` and the student
  performance G1/G2 were known at prediction time and were still dropped.
- Remedy that keeps the dataset: rung 2 of the remedy ladder, as in the account_debt_south_africa precedent (SEL-5
  Cases, "applied"). Drop the 11 product columns. The rest is a small real signal, which TP-2 (Should) keeps: log loss
  0.694 against 0.796 for the class shares, macro AUC 0.752. It also fits the screening use case of point 2 (a form
  run without the product module).
- Alternative, the curator's call: keep the columns through a deliberate amendment of LEAK-10/SEL-5 for inputs of an
  unpublished, non-deterministic index (precedent checker, option d). An exception cannot do it, because a Must has
  none.
- Either way, exclusion is not warranted. The Must can be fixed.

**6. Malawi's insurance missingness is weak (P4, LEAK-10 graded as weak)**

- Evidence: the routing follows holding insurance (117 of the 147 asked hold a product). Blanking only the
  missingness signal (the 30 rows that were asked and hold none) costs +0.0019 log loss, mixed on 6 of 9 splits
  (column audit).
- Remedy: keep the `Anomaly:` bullet, add the routing fact and the +0.002. If point 5's drop is taken, the three
  insurance columns go and this point is moot.

**7. The quality items are cheap, and independent of shipping (P7, CLEAN-10/11/21, Should)**

- Items:
  - Set business age to missing in the 6 rows where it exceeds the owner's age (CLEAN-11), or note them as
    inherited.
  - Document the five Yes/missing "not ticked" columns (CLEAN-10).
  - Note that the amount periods may differ by country (CLEAN-21).
  - Fix the wording: 30 answer columns plus country; `has_insurance` reads as business insurance.
  - Align the record's `domain` to `finance`.
- These are independent failures, not conflicts: each is fixed on its own rung and none excludes. The tension row
  "a real task against imperfect cleaning" applies.

Judgment record (proposed):

```text
Verdict: ship after changes.
Validity: PROV-1/PROV-13 hold (Lesotho drop, notes extended); SEL-3/USE-5 hold with use_case rewritten to the
screening actor; LEAK-10 triggered, fixed by dropping the 11 product columns (or a curator amendment); SPLIT-1 holds.
Value: TP-4 not met; TP-2 small real signal after the drop (0.694 vs 0.796).
Quality: CLEAN-11 six ages to missing; CLEAN-10/21 notes.
```

**Rebuttal**

The critic and I agree on the verdict ("ship only after changes") and on every remedy rung. No point calls for
exclusion. One partial dispute remains (point 2). Point 4 is a correction of a fact in my brief.

1. **LEAK-10, the product columns: conceded.**
   - What follows: drop the 11 product columns and cite the Zindi four-dimension text (EV-1). The account_debt
     precedent applies. TP-2 keeps the rest (0.694 against 0.796).
   - The curator may instead amend LEAK-10. A `Potential leak, kept on purpose` note is not a valid form here; agreed.

2. **USE-5 and SEL-3, the actor: the remedy is conceded, one premise is disputed.**
   - Conceded: no lender is cited, and `use_case` moves to development partners and governments screening businesses
     for support. The fit stays `approximate`.
   - Disputed: "neither an observed outcome nor an expert annotation". The FHI is FinMark Trust's expert-built measure
     with four named dimensions (Zindi page). That makes it an expert construct, not a clustering label (SEL-4) or a
     convenient label (USE-5).
   - What the dispute changes: it is the reason SEL-3 holds once the actor is fixed. The curator's open call is only
     the critic's own fallback ("only if no one acts on the class").
   - Rule that wins: SEL-3 is met by an expert annotation and an acting actor. EV-2 ranks the source's page above an
     inference.

3. **USE-8 and EV-1, fit_reason and decision 2: conceded.**
   - The 0.285 against 0.260 comparison measures capacity, not information in the other columns. Use the matched
     comparison (0.255 against 0.266, products better on 9 of 9).
   - In decision 1, state the sentinel exclusion: the Spearman figures are -0.055/-0.073/-0.052 as released.

4. **Malawi's insurance missingness: conceded, with a correction.**
   - I wrote that the routing follows holding insurance. The column audit shows it is not a skip on `has_insurance`
     (47 Malawi businesses answer Yes and were not asked). What holds is that 117 of the 147 asked hold a product.
   - The effect is unchanged (+0.002). The point is moot under point 1.

5. **PROV-13, the Lesotho diagnosis: conceded.**
   - Add the feature damage to decision 1.
   - Record a data request to FinMark Trust.
   - Decide this alike with account_debt's open issue 1.

6. **SPLIT-31, the optimistic IID score: conceded.** Add one sentence with the cross-country numbers. The split stays.

7. **P7, quality and wording: conceded in full.** That includes the metric wording (f1_multiclass, "weighted"
   unverified) and the `has_insurance` meaning.

Joint judgment record:

```text
Verdict: ship after changes.
Validity: LEAK-10 fixed (11 product columns dropped) or a curator amendment; SEL-3/USE-5 hold with use_case rewritten to
the screening actor; PROV-13 holds (Lesotho drop, notes extended, data request); SPLIT-1 holds, SPLIT-31 note.
Value: TP-4 not met; TP-2 keeps 0.694 vs 0.796.
Quality: CLEAN-11 six ages; CLEAN-10/21 notes; wording.
```

</details>

<details><summary>Critic</summary>

Position: **ship only after changes.** Point 1 is a Must that the definition can fix. Points 2 and 3 are fixes to the
definition's text. Points 4 to 7 are notes or cheap cleaning, and none of them is a reason to exclude the task.

**1. P4, LEAK-10 (Must): the 11 product columns are a part of the target, and the definition keeps them**

- **Problem.** The FHI has four dimensions. One of them is "access to credit and financial services" (Zindi page,
  quoted in blind review and practitioner), and the shipped insurance and credit columns measure exactly
  that. LEAK-10 puts "a part ... or another encoding of the target" out, and it makes no exception for a column known at
  the prediction point. mutual_funds_india `rating` and UCI G1/G2 were also known at prediction time and were dropped
  (precedent check §1).
- **Effect.** Most of the measured task is rebuilding the index from its own inputs. With the same learner, country
  plus the 11 product columns beats all 37 columns on 9 of 9 splits (log loss 0.255 vs 0.266). The other 26 columns
  alone score 0.694, against 0.796 for the class shares (claim audit, row 9). None of the 1,896 insured businesses is
  Low. funeral_insurance alone reaches AUC 0.790 (leak probe).
- **Why the stated reasons fail.**
  - "A business reports them at the assessment" is LEAK-37. That rule covers inputs, not parts of the label.
  - "The competition uses all columns" is not a higher Must. CLEAN-20 copies a competition's preprocessing, not its
    exploits.
  - LEAK-38 covers anonymised fields that may be post-outcome. These are named inputs of the label.
  - No higher-ranked Must is named, and a Must has no exceptions.
  - The closest precedent, account_debt_south_africa (CC 2026-10-12), dropped its label's rule inputs and kept the
    rest.
- **Remedy (fix the definition).** Drop the 11 product columns and cite the Zindi four-dimension text as the source
  (EV-1). What remains is a small real signal, which TP-2 keeps (0.694 vs 0.796). The task stays (USE-12). The
  alternative is that the curator amends LEAK-10 on purpose. A `Potential leak, kept on purpose` note is not a valid
  form for this case.

**2. P3, USE-5 and SEL-3 (Must): no cited actor acts on the FHI class**

- **Problem.** The label is a constructed survey index whose formula is unpublished. It is neither an observed outcome
  nor an expert annotation. The use case "a lender assesses" has no source. A lender acts on repayment, and anyone who
  holds the answers would compute the index rather than predict it (practitioner, gaps 1 and 2; claim audit,
  item 2).
- **Remedy (fix the definition).** Move `use_case` to the actor that Zindi itself names: development partners or
  governments screening businesses for support. That is a proxy-means-test pattern, where the FHI class is close to
  what gets acted on. Keep the fit `approximate` and name the gap. Exclusion (`No Good Target`) applies only if the
  curator finds that no one acts on the class.

**3. P3, USE-8 (Must) and EV-1: fit_reason and decision 2 misstate the evidence**

- **Problem.** "Partly recovers ... 0.285 vs 0.260, worse on all 9 splits" compares a depth-6 tree with LightGBM. That
  gap measures model capacity, not information in the other columns. The 0.260 is not reproduced either: default
  LightGBM gets 0.283 and the probe 0.303. With matched learners, the products alone win 9 of 9 (claim audit).
- **Problem.** Decision 1 gives Spearman -0.12/-0.11/-0.11. These hold only after excluding the 97/98/99 sentinels.
  As released, the values are -0.055/-0.073/-0.052, and the text does not say so.
- **Remedy (fix the text).** If point 1 is adopted, rewrite both with the matched comparison. Otherwise, say plainly
  that the task is the index formula plus a residual. State the sentinel exclusion in decision 1.

**4. P4, LEAK-10, weak (missingness that encodes the outcome): Malawi's insurance block**

- **Evidence.** Malawi asked the block of only 147 businesses, and 91% of them are Medium or High, against 14% of the
  others. The routing is not on `has_insurance`. The missingness-only effect is small: +0.002 log loss, worse on 6 of 9
  splits (column audit §2).
- **Remedy.** This goes away with point 1, since the three insurance columns go. Otherwise, add the routing fact and
  the +0.002 to the `Anomaly:` note.

**5. P5, PROV-13 (Must): the Lesotho drop holds, but the diagnosis and the origin check are incomplete**

- **Evidence.**
  - Lesotho's features are damaged as well as its labels: 12 columns are all-missing, among them the insurance
    columns and credit card, and 86% of its businesses answer "Used to have" for the informal lender (claim audit).
    This strengthens the drop.
  - FinMark Trust and data.org were not asked about the data.
- **Remedy (a note).** Add the feature damage to decision 1. Record a data request to FinMark Trust, as in
  account_debt and ghana. Decide this alike with account_debt's open issue 1. I do not ask to keep Lesotho.

**6. P4, SPLIT-31 (Should): the IID score is optimistic for any later survey wave or another country**

- **Evidence.** A model trained on Malawi 2019 and Zimbabwe 2022 scores Eswatini 2023 at log loss 0.669, against 0.346
  under IID (split audit). With only three country-years, a grouped or temporal split is not sound.
- **Remedy (a note).** Add one sentence with these numbers. The split itself stays.

**7. P7, quality (CLEAN-11, CLEAN-10, CLEAN-21, writing): cheap fixes and notes**

- **Impossible ages.** 6 rows have business_age_years > owner_age (e.g. a 20-year-old owner with a 25-year-old
  business). Set those values to missing, or note them.
- **Missing that means "not ticked".** Five Yes/missing columns store "not ticked" as missing, and only cash flow is
  documented: has_mobile_money, motivation_make_more_money, problem_sourcing_money, marketing_word_of_mouth. Extend
  the note to all of them.
- **Amounts.** The period of the amounts appears to differ by country (income/turnover median 0.06 in Zimbabwe vs 0.33
  elsewhere). Add a note.
- **Wording.**
  - "31 answer columns" should read 30 answer columns plus country.
  - Zindi's API gives the metric as f1_multiclass. "Weighted" comes only from a discussion thread.
  - `has_insurance` reads as business insurance, not "any insurance": 1,471 businesses answer No yet hold funeral
    cover.
  - The record's domain should be `finance`.
- None of these is a reason to exclude the task.

**Rebuttal**

We now agree on the verdict: ship after changes. Drop the 11 product columns, rewrite `use_case` around the screening
actor, and add the notes. Two of the advocate's arguments do not hold, and I dispute both below.

**1. Provenance and the Lesotho drop: concede**

The facts are the ones I cited (claim audit). One addition: PROV-13 asks for an origin check, so record a data
request to FinMark Trust.

**2. Use case: concede the remedy, dispute one argument**

- **Conceded.** Rewrite `use_case` around the screening actor and keep the fit `approximate`.
- **Disputed.** "FinMark Trust's expert-built measure" has no source.
  - The column audit found no FinScope definition of a financial health index.
  - The formula is unpublished. Who built the index (FinMark, data.org or Zindi) is not shown.
- **Why it matters.** SEL-3 asks for an observed outcome or an expert annotation. A composite index of unknown
  construction is neither. What carries SEL-3 here is the screening use case (P3 informs P2), not the label's
  pedigree.
- Write the rewritten `use_case` on that basis. Do not claim expert authorship without a source (EV-1).

**3. Split: concede**

The note under SPLIT-31 is enough.

**4. Not Trivial: concede the conclusion, dispute the evidence**

- **Conceded.** TP-4 is not met, so the task is not `Trivial`.
- **Disputed.** "A depth-6 tree on the products is worse than LightGBM on 9 of 9 splits" is no evidence for that.
  - The comparison measures model capacity.
  - With matched learners, the products alone beat all columns on 9 of 9 splits (0.255 vs 0.266; claim audit).
- **Which rule wins.** USE-8 and EV-1 require that the fit_reason and decision 2 do not reuse this comparison. If
  point 5's drop is taken, the matter is moot for the shipped task, but the decision text must still report the
  matched comparison.

**5. Product columns: concede the drop, dispute the amendment option**

- **Conceded.** Drop the 11 product columns.
- **Disputed.** The advocate offers amending LEAK-10/SEL-5 as an equal "either way". It is not.
  - The rule does not limit a component to a published or deterministic formula: LEAK-10 puts out "a part of the
    target" with no such condition.
  - account_debt_south_africa (CC 2026-10-12) dropped rule inputs that were not deterministic either (371
    exceptions).
  - An amendment would break the treat-like-cases-alike rule against that case and against mutual_funds_india and
    student performance, unless those are reopened.
- **What I ask.** Ship with the drop. If the curator wants the amendment, it has to come with those precedents
  reopened (principles.md, "Consistent judgement").

**6. Malawi's insurance missingness: concede**

The point is moot once the drop is taken.

**7. Quality items: concede**

I agree, including setting the 6 impossible ages to missing.

</details>
