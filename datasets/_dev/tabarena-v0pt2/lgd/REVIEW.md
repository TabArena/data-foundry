# lgd

**Outcome:** added. A regression of the loss given default (LGD: the share of a defaulted loan's outstanding amount
that the bank loses, from 0 to 1) of 2,545 loans of a European bank from the book Credit Risk Analytics, with two
inputs: the loan-to-value ratio (LTV: the outstanding amount over the value of the collateral) and whether the loan's
purpose is renting. Grouped splits by borrower block (a run of consecutive rows with one LTV value, most likely one
borrower's loans), scored with RMSE. The AI recommends shipping; two decisions remain, what `event` = 0 means
(issue 3) and the two-feature task (issue 4).

```text
Verdict: ship (the panel's changes are applied); the record's `problem_type` is a record-field row.
Validity: SEL-2 holds; USE-1 holds, fit approximate (USE-8: no dates, two inputs); USE-5 regression on the source's
  `lgd_time` (shipped as `lgd`) holds; USE-5 open on the 728 rows with `event` = 0 (the source's default-or-cure flag,
  dropped; the codebook read literally leans against the cure reading, the book's Tobit and censored beta code read them
  as cures; issue 3); LEAK-10 triggered and fixed (four transforms of the target and `event` dropped); SPLIT-24 and
  USE-10 hold (key built from the data, "most likely one borrower"); SPLIT-6 gap noted (no dates; a spline's R² on
  forward windows in file order 0.138 against 0.210 grouped, an upper bound); PROV-2 note ("slightly modified and
  anonymized" unexplained); PROV-3 not triggered (no sign the data was reworked; the probes find no HMEQ-style
  artefacts).
Value: TP-4 holds, not Trivial (a monotone fit on LTV loses to the spline on 30 of 30 splits); TP-2 keep (the best
  linear model removes 0.193 of the error of predicting the mean, its skill, and beats the mean on 100% of splits); TP-3
  not invoked (the probes' spread is untuned random forest overfitting, TP-1).
Quality: CLEAN-14 fixed (`purpose_renting` categorical); CLEAN-1 target bounds 0.00001 and 0.99999 kept with the
  note.
Weighed: size -, features - (2), source + (the book's own data page), use case + (LGD under the Basel capital
  rules and IFRS 9 provisioning).
Licence: textbook use only, no commercial use, no redistribution; a note (EV-4), as for mortgage and
  corporate_credit_rating_cat.
For the curator: issue 3 (validity: chapter 10 on `event` = 0); issue 4 (a weighing call: thin task, haberman_survival
  against sepsis_survival_minimal_clinical_records).
```

**Main points:** Read chapter 10 first, ship with the 728 `event` = 0 rows kept and the open risk stated in the notes,
or hold (issue 3); keep the two-feature task, or No as for haberman_survival (issue 4); take the definition's Regression
for the record's `problem_type`.

**Record fields that disagree with the definition:**

- `problem_type`: record `Binary Classification`, definition `Regression`.

**Record judgment:** valid with concerns. Real LGD data from the book's own data page (the same file as the Wayback
copy of 2017-09-27). The record's Binary Classification is the import value of 2026-06-23; the only binary column,
`event`, is part of the target, and the book's task (chapter 10) is the LGD regression. Concerns: two features only,
the unsettled meaning of `event` = 0, and the book's "slightly modified and anonymized" (chapter 1, p. 14) without
detail.

**Issues for Lennart:**

3. **What does `event` = 0 mean: read chapter 10 first, ship with the rows kept, or hold?** 728 loans (28.6%) have
   `event` = 0 (a 0/1 column of the source, dropped as part of the target) and sit at the floor of the target (stored as
   0.00001, an LGD of zero). If these loans defaulted and then cured (the borrower resumed paying, so the bank lost
   nothing), they are LGD observations of 0. If they never defaulted, they have no LGD at all.
   - Effect: under the second reading, the benchmark scores a mix of "did the loan default" and "how much was
     lost". The mass at zero and part of the LTV signal would come from that selection step: the share at the floor
     falls from 43% of loans with LTV below 0.5 to 6% above 1.2.
   - Evidence: the book's data page (http://www.creditriskanalytics.net/datasets-private2.html, behind Cloudflare;
     the Wayback copy of 2017-09-27 reads the same) says "event: Indicator variable for a default or cure event; 1 =
     event, 0 = no event". Read literally, a default and a cure are both the event (1), so 0 is neither; this leans
     against the cure reading (the critic, the mediator). The R code for the book's companion volume, as a third
     party transcribed it on GitHub (not text we read in the original), splits both ways. Its Tobit model and its
     censored beta model treat 0 as a real loss of zero, piled up at the lower bound, so they count these rows as an
     LGD of 0. Its Heckman model (which first models whether a loan enters the LGD data, then the loss) counts them
     as "not selected". All 728 rows carry the source's logit and probit transforms. The advocate reads this as the
     source counting them as LGD observations; the mediator ranks it as inference, since a placeholder for a Heckman
     or Tobit fit would look the same. The data does not decide: 245 of the 1,817 loans with `event` = 1 also lose less
     than 1%.
   - Implemented: the rows are kept as cures; the notes and `fit_reason` quote the codebook line and name the open
     risk.
   - Rule: USE-5 (Must, the target is the real-world target); EV-2 ranks the source's own codebook above inference.
     Precedents: corporate_credit_rating_cat was kept pending its chapter 8; a filter would follow
     cirrhosis_patient_survival_prediction (USE-5) and mortgage (LEAK-25).
   - What settles it: chapter 10 of the book (pp. 271-313). It would also say whether a row is a loan or a default
     episode, the country and period, whether LTV is taken at origination or at default, whether open workouts are
     in the data, and what "slightly modified" means. Whatever it says, the fix is one filter in the definition.
   - Alternatives: (a) read chapter 10 now, then keep or filter the 728 rows; cost: it needs the book. (b) Ship with the
     rows kept and the open risk stated in the notes, chapter 10 requested as a follow-up (as for
     corporate_credit_rating_cat); cost: 28.6% of the target may not be LGD until then. (c) Hold the dataset until
     chapter 10 is read; cost: it waits on a book that may not be obtained.
   - Recommendation: none from the mediator, who leaves the timing to you; the advocate and the critic both accept
     (b) with the open risk stated in the notes.
   - Decision: (a), (b) or (c).

4. **Two features only: keep as a thin task, or No as for haberman_survival?** The inputs are LTV and the renting
   flag, the two the book's models use. lgd is the thinnest dataset in the working copy; the next are
   sepsis_survival_minimal_clinical_records (3 features) and blood_transfusion (4).
   - Effect: strong methods land close together, so the task mostly measures how well a method regularises (avoids
     overfitting) a one-dimensional curve.
   - Evidence: not `Trivial` under TP-4: a monotone fit on LTV alone loses to a spline on both inputs on 30 of 30
     splits, and the best linear model removes 0.193 of the error of predicting the mean, its skill, and beats the
     mean on 100% of splits. On the 30 shipped splits
     (R²): spline 0.206, regularised LightGBM (4 leaves) 0.195, linear 0.189, random forest with at least 100 rows
     per leaf 0.186, with at least 50 rows 0.179; the spline beats each on 28 to 30 of 30 splits, by 0.012 to 0.028.
     Default LightGBM scores 0.130 and a default random forest -0.164. The book's 3-parameter fractional logit
     reaches 0.204 and tuned LightGBM 0.200. The blind reviewer says exclude: "it cannot tell tabular methods
     apart".
   - Precedents: sepsis_survival_minimal_clinical_records was kept with the source's own few inputs (2026-10-06);
     haberman_survival went to No, `Trivial`, on 2026-07-27 as "essentially two features". What sets lgd apart:
     2,545 rows against about 306, a current use case (LGD estimation for capital and provisions), and no `Trivial`
     proof under TP-4.
   - Rules: TP-2 (Should), TP-4 (Must); principles, "Consistent judgement" case 2 (two precedents
     with opposite outcomes: name the fact that sets this case apart). A weighing call.
   - Alternatives: (a) keep as a thin task, with the haberman distinction recorded; cost: a task that mostly
     measures regularisation. (b) No, as for haberman_survival; cost: the benchmark loses an LGD task with a
     current use. (c) Write a rule for tasks whose source has only a few inputs; cost: the decision waits on a new
     rule that also covers other datasets.
   - What would settle it: the benchmark's tuned results per fold, which show whether tuned methods separate.
   - Recommendation: none from the mediator (a weighing call); the advocate and the critic both keep it.
   - Decision: (a), (b) or (c).

**Review panel:** ship after changes (mediator). Claim audit: about 40 claims, none refuted; weakened and fixed: the
within-run correlation (0.42, 0.35 without the exact repeats), the drift wording and the uncited `event` codebook
line; untested: the book's pages and the sas7bdat file. Blind review: exclude; main concern the two features. Debate:
agreed on the regression, the grouped split, the dropped columns and the note and number fixes; disputed: how
strongly the codebook line leans against the cure reading (issue 3) and whether the probes' linear-minus-forest
spread is skill (settled by the mediator's experiment: overfitting). The reports number an earlier draft: their issues 3 and 4 and the mediator's issues 1 and 2 are issues 3
and 4 here; their issue 1 is the `problem_type` row, and the rest are settled as notes or moved to the cross-dataset
review.

<details><summary>Mediator</summary>

**Mediator: lgd**

**Recommendation (judgment record)**

```text
Verdict: ship after changes.
Validity: SEL-2 holds; USE-1 holds, fit approximate (USE-8: no dates, two inputs); USE-5 regression on lgd_time
holds (the record's Binary is the 2026-06-23 import, no curator mark); USE-5 open on the 728 rows with event = 0
(the codebook read literally leans against the cure reading, the R code's Tobit and censored beta read it as a
cure; settle with chapter 10, then filter or keep); LEAK-10 triggered and fixed (4 target transforms and event
dropped); SPLIT-24 and USE-10 hold (key built from the data, "most likely one borrower"); SPLIT-6 gap noted
(no dates, forward bound 0.138 vs 0.210); PROV-2 note (PROV-3 not shown).
Value: TP-4 holds (not Trivial: isotonic LTV loses on 30/30); TP-2 keep (best linear skill 0.193, beats the
dummy on 100% of splits); TP-3 not invoked (the +0.218 is untuned RF overfitting, TP-1).
Quality: CLEAN-14 fix (purpose_renting categorical); CLEAN-1 bounds optional, kept with the note.
Weighed: size -, features - (2), source +, use case + (Basel/IFRS 9 LGD).
For the curator: issue 1 (validity: chapter 10 on event = 0); issue 2 (a weighing call: thin task, haberman vs sepsis).
```

**Changes to make now (no decision needed)**

1. **Problem type.** Set the record's `problem_type` to Regression and list it as a field row. The import value is the lowest tier under "Who decides", and the main session found no curator mark. Rule: USE-5.
2. **Issue 1.** Drop the CreditICL bullet and keep CreditICL only as the provenance lead (issue 8). Rule: EV-4, Must.
3. **Stale split wording.** Remove "instead of the record's random split" (`task_summary.changes`) and "against the record's 'Random (IID)'" (`curation_comments`). Delete REVIEW issue 2 and its `required_split` row, keep the grouping evidence as notes, and renumber the issues (there is no issue 7). Reason: the record has said Grouped since 58ee235. Rules: writing.md; "Who decides" (the curator's mark is applied).
4. **`event` text.** Quote the codebook line "event: Indicator variable for a default or cure event; 1 = event, 0 = no event" in the `event` note of `curation_comments`, in `fit_reason` and in the REVIEW issue. Replace "No text we read says ...". The wording should follow the settlement of dispute 1 below. Rules: EV-2, EV-7.
5. **`splits_comment` and the grouping bullet.** Write "most likely one borrower (a run of one LTV value)" in place of "a borrower the model has not seen" (dataset.py lines 52 and 145). Say the test stands for new borrowers in the same undated period, not next year's defaults. Give the forward bound: spline R² 0.138 against 0.210 grouped, which is an upper bound because the row order is not shown to be time. Rules: SPLIT-24, SPLIT-6, USE-8, writing.md.
6. **Numbers.**
   - Within-run residual correlation: 0.42, or 0.35 without the 120 exact repeats.
   - Drift: write that the median LTV and the mean LGD "rise over the first four fifths of the file".
   - HMEQ note: add one line saying 6- and 7-decimal LTVs are in excess at LTV > 1 but do not predict the LGD (R² 0.2064 vs 0.2057).
   - Rule: EV-9.
7. **`purpose_renting`.** Add it to `FeatureTypes(categorical=...)`. Rule: CLEAN-14.
8. **Target bounds.** Map 1e-5 and 0.99999 to 0 and 1, or keep them with the current note. Either is acceptable. Rule: CLEAN-1, Should, weak.
9. **Issue 4 (two features).**
   - Name haberman_survival (No, Trivial, 2026-07-27) next to sepsis_survival_minimal_clinical_records.
   - Give the facts that set lgd apart: 2,545 rows against about 306, a current Basel/IFRS 9 use case, and no `Trivial` proof under TP-4.
   - Say the task mostly measures regularisation.
   - Do not cite +0.218 as spread; use the measured numbers under dispute 2.
   - Rule: principles, "Consistent judgement" case 2.
10. **Contingent fix.** If chapter 10 says the 728 loans never defaulted, filter them in `_clean`. Precedents: cirrhosis (USE-5) and mortgage (LEAK-25). This is a definition fix, not an exclusion.

**Disputed points, settled**

**Dispute 1: how strongly the codebook line points against the cure reading, and what the keep text says meanwhile**

- **The fact is open, and settling it is not cheap.** EV-1 asks for the decisive experiment, but here that is reading chapter 10 (pp. 271–313), which nobody on the panel could reach. The data cannot decide:
  - The floor share falls with LTV, which fits both readings (column audit).
  - I checked one more measurement. Among the 1,817 `event` = 1 rows, 245 have an LGD below 0.01 and 24 below 0.001. Near-zero losses therefore exist with `event` = 1 too. That fits cures with small workout costs coded as 1 (the critic) as well as exact-zero cures coded as 0 (the advocate). It does not decide.
- **How the evidence ranks (EV-2):**
  - **The codebook line** is the source's own data dictionary, tier 2. Read literally, both "default or cure" fall under "1 = event", so 0 is neither. The critic's reading is the literal one. The advocate's alternative ("1 = a loss event") reads in words the line does not contain, which is inference, tier 5.
  - **The R code.** The Tobit and censored-beta code read 0 as a cure; the Heckman code reads it as "not selected". This code comes from a third-party GitHub transcription of the companion book (dpicone1), not text we read in the original. It counts at most as tier 2 and splits both ways.
  - **The stored transforms.** The advocate notes that all 728 rows carry squeezed transforms. That fact was measured, but what it means is inference: a placeholder for a Heckman or Tobit fit would look the same.
  - **The practitioner's "mostly cures"** is domain inference, tier 5. It also rests on a misquote, which the advocate withdrew.
- **Result.** The critic wins on emphasis: the highest-ranked text that speaks to the point leans against the cure reading. It does not lean far enough to settle the fact.
- **What the keep text says meanwhile.** Both sides already accept this wording:
  - quote the line;
  - say that, read literally, it puts cures at 1 and so leans against the cure reading;
  - say that the R code's Tobit and censored-beta models treat these rows as LGD 0, and its Heckman model as not selected;
  - name it an open USE-5 risk on 28.6% of the target, until chapter 10 is read.
  - "Follows the book's code" alone does not meet EV-2.
- **Keeping the rows meanwhile follows precedent.** corporate_credit_rating_cat was kept pending its chapter 8. Under the remedy ladder, either outcome is one filter. This is not a conflict between rules but an open fact under one Must (USE-5). Whether to wait for chapter 10 before shipping is a question for the curator (issue 1 below).

**Dispute 2: is the +0.218 linear-minus-RF spread skill or RF overfitting?**

- **Rule.** TP-1 (Must) says the probes are untuned, so a probe number is not evidence that tuned methods spread (TP-3). The critic's side holds by rule.
- **Decisive experiment.** I ran it on the 30 shipped splits with 2 threads each, comparing every method with the spline. "Spline wins" counts the splits where the spline scores higher.

| Model | R² | Spline minus model (paired SE) | Spline wins |
|---|---|---|---|
| spline | 0.206 | | |
| LightGBM, regularised (4 leaves, min_child 100) | 0.195 | +0.012 (0.001) | 30/30 |
| linear | 0.189 | +0.017 (0.002) | 28/30 |
| RF, min_samples_leaf 100 | 0.186 | +0.020 (0.002) | 29/30 |
| RF, min_samples_leaf 50 | 0.179 | +0.028 (0.002) | 30/30 |
| LightGBM, default | 0.130 | +0.076 (0.004) | 30/30 |
| RF, default | -0.164 | +0.371 (0.012) | 30/30 |

- **Settled.** With regularisation, the random forest closes almost the whole gap, so the +0.218 is overfitting.
- **A real but small spread remains.** Among the regularised methods the gaps are 0.012–0.028, and they are stable: the spline wins 28–30 of 30 splits.
- **TP-3 is not the basis of the keep.** These are hand-regularised models, not the benchmark's tuned results, and there was no `no_spread` flag. The keep rests on TP-2 and TP-4.
- **Issue 4** should cite the stable gap of 0.01–0.03 among regularised methods and say the task mostly measures regularisation.

**Issues for the curator, ranked**

1. **What `event` = 0 means. Validity (P3, USE-5, Must).**
   - **Problem.** 728 rows (28.6%) sit at the floor of the target. If those loans never defaulted, the benchmark scores a mix of "did it default" and "how much was lost".
   - **Critic's best evidence.** The codebook line, "default or cure event; 1 = event, 0 = no event". The Heckman "not selected" and the chapter 10 heading fit the same reading.
   - **Advocate's best evidence.** The Tobit and censored-beta code treat the rows as LGD censored at 0. Every row carries an LGD with transforms, which a non-default would not need.
   - **Not decisive:** the data itself (one more check above).
   - **What settles it.** Chapter 10, pp. 271–313.
   - **Decision needed.** (a) Read chapter 10 now, then keep or filter. (b) Ship with the rows kept and the risk written as above, with chapter 10 requested (as for corporate_credit_rating_cat). (c) Hold until chapter 10 is read.
2. **Two features: keep as a thin task, or retire. Value (P6). A weighing call; consistency case 2.**
   - **For keeping.** Not Trivial under TP-4: isotonic LTV loses on 30/30 splits. The signal is real: skill 0.193 on 100% of splits. The two inputs are the book's own. It has 2,545 rows and a current use. The precedent is sepsis_survival_minimal_clinical_records (kept 2026-10-06).
   - **Against.** Tuned smooth methods sit within 0.01–0.03 of each other (spline 0.206–0.208, tuned LightGBM 0.200, fractional logit 0.204). The blind reviewer says exclude. haberman_survival went to No on 2026-07-27 as "essentially two features".
   - **Rules.** TP-2, TP-4; principles "Consistent judgement" case 2.
   - **What would settle it.** The curator's weighing, or the benchmark's tuned per-fold results to see whether tuned methods separate.
   - **Decision needed.** (a) Keep, with haberman distinguished as in change 9 above. (b) Treat it like haberman: No. (d) Write a rule for tasks whose source has only a few inputs.

**Agreed facts**

- **Data.** 2,545 rows; inputs LTV and `purpose1` only; no dates.
- **Raw file.** sha256 2e3f964a...e07e, the same as the Wayback copy of 2017-09-27 and the GitHub copy.
- **Target.**
  - 728 rows (28.6%) at 1e-5, 143 (5.6%) at 0.99999.
  - `event` = 0 exactly on the 728 floor rows.
- **Dropped columns** are exact transforms of the target: `Recovery_rate`, logit, lnrr, probit. Dropping them and `event` is correct (LEAK-10).
- **Grouping.**
  - 1,958 runs; 488 have several loans (up to 7); 70 mix both purposes; no LTV value occurs in two runs.
  - Within-run residual correlation 0.42 (0.35 without the exact repeats), against 0.02 between neighbouring runs.
- **Shipped splits.** 30 splits; 0 groups shared between train and test; 0% of test LTVs seen in train. Under IID, 31% would share an exact LTV with a train row.
- **Duplicates.** All 120 exact and 397 feature-only duplicates sit inside runs.
- **Probes.**
  - Best linear skill 0.193 (SE 0.005); LightGBM 0.119; RF -0.026; single feature 0.069; no flags.
  - Isotonic LTV loses to the spline on 30 of 30 splits.
  - Generated probes find no HMEQ artefacts.
- **Row order.**
  - The order carries LTV and LGD, rising over the first four fifths of the file.
  - The last 234 rows look like a second segment.
  - The order is not shown to be time. The rows are shuffled and the group id is a hash.
- **Forward windows.** Spline R² 0.138 against 0.210 grouped.
- **Record.** `problem_type` Binary is the 2026-06-23 import with no curator mark. `required_split` has been Grouped since 58ee235.
- **Blind reviewer's 29.5% / 6.8%** is outranked by the measured 28.6% / 5.6% (EV-2).

**Consistency with precedent**

From the precedent checker's report, every recommendation follows a precedent:

| Point | Precedents followed |
|---|---|
| Regression on `lgd_time` | definitions.md; coad (`problem_type` updated in 58ee235) |
| Grouping key | SPLIT-24: in_vehicle_coupon_recommendation, concrete_compressive_strength. Not the barred maternal_health_risk: one column plus contiguity, and purpose varies inside runs |
| Keeping despite small gaps | SPLIT-4: superconductivity |
| Shuffle without `ForcedIIDFromTemporal` | emscad; SPLIT-8: account_debt_south_africa |
| Unexplained modification | PROV-2: bad_customer_detection; corporate_credit_rating_cat |
| Open `event` reading | corporate_credit_rating_cat (kept pending a chapter); a filter would follow cirrhosis and mortgage |
| Licence in `license` only | mortgage; lucas_topsoil |

- **One departure is fixed now:** the CreditICL bullet goes from issue 1 (EV-4).
- **One opposite-outcome pair goes to the curator:** haberman_survival against sepsis. The distinguishing facts are named (issue 2). The curator has not drifted on these rules, and there is no third exception.

**Files**

- `datasets/_dev/tabarena-v0pt2/lgd/dataset.py`
- `datasets/_dev/tabarena-v0pt2/lgd/REVIEW.md`
- `curation/records/lgd.md`

</details>

<details><summary>Claim audit</summary>

**lgd: claim audit (2026-10-20, re-check)**

Data: the raw `lgd.csv` (sha256 verified) and the definition rebuilt through `dataset_io.load` (origin `rebuilt`; no built container), 30 shipped splits.
Licence and pretraining overlap are not used as evidence (EV-4).

| # | claim | source | test | result | evidence | rule |
|---|---|---|---|---|---|---|
| 1 | predicts loss share of a defaulted loan | D task_summary | codebook (Wayback data page) | holds | "lgd_time: Loss rate given default (LGD)" | EV-2 |
| 2 | prediction at default; ch. 10 task | D | codebook; book not read | holds (codebook) / ch.10 untested | book p.4 not accessible | EV-7 |
| 3,19 | 2,545 loans, European bank, "slightly modified and anonymized" | D | codebook + row count | holds | codebook: "kindly provided by a European bank ... slightly modified and anonymized. It includes 2,545 observations"; 2,545 rows. Page number (p.14) untested | EV-2 |
| 4,26 | 28.6% at 0, 5.6% at 1; stored as 1e-5 / 0.99999 | D | count on raw | holds | 728 = 28.61% at 1e-5, 143 = 5.62% at 0.99999; min 1e-5, max 0.99999 | - |
| 5,20 | only LTV and purpose; known at default | D | codebook; columns | holds | the other columns are target transforms and `event`; LTV>1 for 17.5% of loans, consistent with a current (at-default) LTV | LEAK |
| 6,41,40 | groups held out whole; test loan from unseen block | D | group overlap and exact-LTV overlap on 30 splits | holds | 0 shared groups; 0.0% of test rows share an LTV with train; 1,958 groups | SPLIT |
| 7,24 | dropped columns are target transforms | D | recompute | holds | Recovery_rate = 1-lgd (err 1e-16); y_logistic = logit(lgd) (1e-6); lnrr = log(1-lgd) (1e-5); Y_probit = probit(lgd) (2e-7) | LEAK-10 |
| 9 | no dates; row order drifts | D | file; quintiles of row index | holds (wording loose) | no date column. Spearman(index, LTV) 0.27, (index, LGD) 0.24; LTV median 0.43/0.57/0.79/0.87/0.69, LGD mean 0.08/0.14/0.27/0.34/0.30, so the rise is not monotone (the last fifth drops). The container shuffles rows and the group id is a hash, so the order does not reach the model | EV-6 |
| 10,34 | event=0 read as a cure; ch. 10 not read | D | codebook line for `event` | untested (open) | codebook: "event: Indicator variable for a default or cure event; 1 = event, 0 = no event". Read literally, a cure is an *event* (1), so event=0 is neither default nor cure, which argues against the "cure" reading; read as "1 = default, 0 = cure" it supports it. The definition does not quote this line. Chapter 10 was not reached | EV-2, EV-7 |
| 11 | year 2016, finance, source_url | D | codebook page | holds | the data page is the book's site (Cloudflare today, Wayback 2018) | - |
| 12 | licence/terms text | D | Wayback terms.html | holds (text only) | "Republish material ...", "Redistribute content ..." present | EV-4 (not evidence) |
| 13 | file link needs no login | D | HEAD on file URL | holds | HTTP 200 text/csv, 191,134 bytes; the data page itself sits behind a Cloudflare challenge | - |
| 14 | sas7bdat same rows, full precision | D | not downloaded | untested | page behind Cloudflare | EV-7 |
| 15 | GitHub copy same sha256 | D | download raw.githubusercontent | holds | 2e3f964a...e07e | PROV |
| 16 | no OpenML / Kaggle re-upload | D | OpenML API by name; web search | holds | OpenML "No results" for lgd/LGD; no Kaggle hit | PROV |
| 17 | sha256 and Wayback 2017-09-27 same | D | hash local and Wayback id_ copy | holds | both 2e3f964a...e07e | PROV |
| 18 | bibtex | D | Wiley / search | holds | ISBN 978-1-119-14398-7 on Wiley pages | - |
| 21,22 | regression, RMSE; mass at both bounds | D | counts | holds | 28.6% at floor, 5.6% at cap | - |
| 23 | only binary column is `event`, part of the target | D | crosstab | holds | purpose1 also binary but a feature; event 0 = 728 floor rows exactly, 1 = 1,674 between + 143 cap | LEAK-10 |
| 25,45 | event=0 exactly the 728 floor loans | D | crosstab | holds | 0 off-diagonal rows | LEAK-10 |
| 27 | LTV a share although "in %" | D | range; codebook | holds | LTV 0.0014-1.98, median 0.66; codebook "in %" (lgd_time also "in %" yet 0-1) | - |
| 28,38,44 | a run's LTV occurs in no other run | D | groupby LTV, nunique runs | holds | 0 LTV values in >1 run | - |
| 29,37 | 1,958 runs, 488 multi (2-7), 70 mixed purpose | D | recount | holds | 1,958 / 488 / max 7 / 70 | - |
| 30 | LGD residual corr 0.42 within runs, 0.02 between neighbours | D | spline(LTV)+purpose+spline(index) residuals; 1st vs 2nd loan of 488 runs; last of run k vs first of k+1 | holds, but partly from exact repeats | 0.424 within, 0.007 neighbours, -0.04 random pairs (calibration, EV-9). Without the 120 exact repeat rows the within-run value is 0.347 (395 runs) | EV-9 |
| 31,39 | a borrower's loans default together; LGD defined by obligor default | D | not testable on the file; book not read | untested | consistent with 120 exact repeats inside runs; also consistent with loans on one collateral (LTV computed per collateral) - same grouping either way | EV-7 |
| 32,42,43 | 120 exact repeats (103 floor, 16 cap, 1 partial at 0.0109972412), all inside runs; 397 rows differ only in LGD | D | duplicated() on raw | holds | 120 / 103 / 16 / [0.0109972412]; all 120 inside their run; 397 feature-duplicates that are not exact | - |
| 33 | median LTV and mean LGD rise along the file | D | quintiles | holds loosely | see 9: rise over the first four fifths, drop in the last | EV-6 |
| 35 | no jittered copies; LTV number format does not predict LGD | D | nearest distinct LTVs; LGD multisets of runs; format flag added to a spline on 30 splits | holds, with an undocumented format anomaly | 3 run pairs within 1e-6 in LTV have different LGDs; runs sharing an LGD multiset are all-floor/all-cap only. Short formats are in excess (6 decimals: 10 vs ~0.2 expected from trailing zeros, 7: 16 vs ~2.3), 77% of them at LTV>1 (17.5% overall); adding the flag changes R^2 0.2064 -> 0.2057 | EV-6 |
| 36 | monotone LTV fit beats the spline on 0 of 30; not Trivial | D | isotonic(LTV) vs spline(LTV)+purpose, ridge, 30 shipped splits | holds | isotonic 0.186, spline 0.206, linear 0.189; isotonic wins 0/30 | task-probe rule 4 |
| 46 | decision tables | D | reproduced counts (29, 25) | holds | - | - |
| 47 | record front matter | R | read record | holds as written; conflicts with D | record still `problem_type: Binary Classification` while D is regression (REVIEW issue 1) | SEL |
| 48 | "provided by a European bank" | R | codebook | holds | quote on the data page | - |
| 49 | ch. 10 errata "MODEL lgd_time ~ GENERAL(ll)" | R | not fetched (Cloudflare) | untested | - | EV-7 |
| 50 | Assessment 2026-10-07 facts | R | as 23-35 | holds | - | - |
| 51 | "thin task" judgment | R | spline R^2 0.206 vs isotonic 0.186 on one feature; RF grouped -0.17 vs IID -0.05 | holds (judgment) | strong methods differ mainly in overfitting a 1-D curve | - |

**Unwritten claims**

* Every feature known at the prediction point: holds (LTV, purpose; no post-default column survives).
* The split is the one the use case needs: holds as far as the file allows; row order leaks nothing (container rows shuffled; `borrower_block` is a hash and not a feature, `n_features: 2`). A temporal split is impossible (no dates).
* No copy across the split: holds (0 shared groups; 0% test LTV in train; all 120 exact repeats inside one run). IID would leak: random forest R^2 -0.05 IID vs -0.17 grouped (6 splits).
* The target is the real-world target: open, see claim 10/34.

**Refuted**

None.

**Untested or weakened, ranked (validity first)**

1. Claims 10/34 (Must, target validity): the meaning of `event` = 0. The data page's own line, "Indicator variable for a default or cure event; 1 = event, 0 = no event", is not cited in the definition and, read literally, puts cures at event = 1, which is against reading the 728 floor rows as cures. Changes: whether 28.6% of rows are LGD observations. Mildest remedy: quote the line in `curation_comments` and REVIEW issue 3; settle with chapter 10 before shipping, else keep the rows and say the reading is open.
2. Claim 30 (Should, evidence wording): 0.42 falls to 0.35 without exact repeats. Remedy: state both numbers.
3. Claims 9/33 (wording): the drift is not a monotone rise. Remedy: "rises over the first four fifths of the file".
4. Claim 35 (note): excess of 6-7-decimal LTVs at LTV>1, not predictive. Remedy: one line in the HMEQ note.
5. Claims 2, 14, 31, 39, 49 (book pages, sas7bdat): untested here (site behind Cloudflare, book not available).

</details>

<details><summary>Column audit</summary>

**Column audit: lgd (column-auditor, 2026-10-20, re-check)**

Prediction point (first `curation_comments` bullet, `task_summary`): a loan has just defaulted; the bank estimates the
share of the outstanding amount it will lose. Codebook: the book's data page
(http://www.creditriskanalytics.net/datasets-private2.html, quoted below) and the R Companion's chapter-10 code
(github.com/dpicone1/Credit-Risk-Anaytics-The-R-Companion, `Ch10_LossGivenDefault_and_RecoveryRates.R`). Frame loaded
with `dataset_io.load("lgd", ..., built=False)` (origin `rebuilt`): 2,545 rows, columns `loan_to_value` float64,
`lgd` float64, `purpose_renting` int64, `borrower_block` category; no missing values.

**Column table**

| column | meaning (codebook) | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| `loan_to_value` (source `LTV`) | "Loan-to-value ratio, in %" (values are shares: median 0.66, 0.0014 to 1.98; 446 rows > 1). Whether at origination or indexed at default: unknown | yes either way (origination or default). Not a post-workout ratio: max(0, 1 - 1/LTV) correlates 0.33 with the LGD and its RMSE (0.369) exceeds the target SD (0.329), so LTV is not the realised collateral value | float64, raw values (16-digit decimals, no z-score or bins: not scaled over all rows); rename to a share is right, the "in %" of the page is wrong. LTV > 1 is plausible for defaulted mortgages (underwater), not impossible | fine | LEAK-10 holds; LEAK-30 n/a; CLEAN-11 holds |
| `purpose_renting` (source `purpose1`) | "Indicator variable for the purpose of the loan; 1 = renting purpose, 0 = other" (185 of 2,545 = 7.3%) | yes: the purpose is set at origination | int64 0/1. A fixed two-value set: CLEAN-14 says categorical, and the siblings mark such flags categorical (2_month_survival_rate_prediction: `diabetes`, `dementia`). Numerically equivalent for most models | cleaning nit: list it in `FeatureTypes(categorical=...)` (optionally labels "renting"/"other") | CLEAN-14 (Should, weak) |
| `borrower_block` (built) | not in the source: a run of consecutive rows with one LTV value, hashed with `anonymize_ids` (1,958 groups) | split metadata, not a feature (README: `n_features: 2`) | category; stable hash, not random (CLEAN-4 holds); hash does not preserve file order, so it carries no row-order drift | fine as group id | LEAK-33 holds; CLEAN-3 holds |
| `lgd` (target, source `lgd_time`) | "Loss rate given default (LGD), in %" (shares 0 to 1) | target | float64. Source bounds kept: 728 rows (28.6%) at 0.00001, 143 (5.6%) at 0.99999, 24 more below 0.001. Truncation to [0, 1] is the source's (documented, LEAK-26 holds). The 1e-5 / 0.99999 values are the source's squeeze for the logit/probit, not data: restoring 0 and 1 is cheap and lossless (RMSE changes by < 1e-5) | target meaning open for 728 rows (see problem 1); bounds a cleaning nit | USE-5 / LEAK-22 (question); CLEAN-1 (Should, weak) |
| `Recovery_rate` (dropped) | "Recovery rate, in %" | outcome | = 1 - `lgd_time` exactly (max abs diff 1.1e-16) | leak, correctly dropped | LEAK-10 |
| `y_logistic` (dropped) | "Logistic transformation of the LGD" | outcome | = logit(`lgd_time`) (max diff 1e-6) | leak, correctly dropped | LEAK-10 |
| `lnrr` (dropped) | "Natural logarithm of the recovery rate" | outcome | = log(1 - `lgd_time`), set to 0 at the floor (max diff 1e-5) | leak, correctly dropped | LEAK-10 |
| `Y_probit` (dropped) | "Probit transformation of the LGD" | outcome | = Phi^-1(`lgd_time`) (max diff 2.3e-7) | leak, correctly dropped | LEAK-10 |
| `event` (dropped) | "Indicator variable for a default or cure event; 1 = event, 0 = no event" | outcome: 0 exactly for the 728 rows at the LGD floor (asserted in `_clean`) | int64 | leak (a part of the target), correctly dropped | LEAK-10 |

No column was dropped that should stay: the source has only `LTV` and `purpose1` as inputs (CLEAN-22 holds). No proxy
missing codes (CLEAN-10 n/a), no constant or copied kept column (CLEAN-5 holds), no untyped object column (CLEAN-9
holds).

**Problems, ranked (principles.md: rank, then strength)**

1. **P3/P4, question for the curator: what the 728 floor rows are (USE-5, LEAK-22, Must if they never defaulted).**
   Evidence: the codebook says `event` is "Indicator variable for a default or cure event; 1 = event, 0 = no event".
   Read literally, `event` = 0 is neither a default nor a cure, and all 728 such rows sit at the placeholder 0.00001;
   the book's ch. 10 heading ("LGD models that condition on the selecting default event", ch. 1 p. 4) and the R
   Companion's Heckman model also treat `event` as the selection. Against: the Tobit and censored-beta code treat them as
   LGD censored at 0. The data cannot decide (the floor share falls with LTV, 43% below LTV 0.5 to 6% above 1.2, which
   fits both a cure and a non-default). REVIEW.md issue 3 says "No text we read says that event = 0 is a cure"; it should
   quote this codebook line, which leans the other way. Mildest remedy: ask for ch. 10 (pp. 271-313); if the rows never
   defaulted, filter them (fix the definition), else keep and note.
2. **P7, `lgd` bounds (CLEAN-1, Should, weak).** 0.00001 and 0.99999 are a transform artefact of the source; an expert
   ships 0 and 1. Remedy: map them in `_clean` with a note, or keep with the existing note (current choice is
   documented and harmless for RMSE).
3. **P7, `purpose_renting` dtype (CLEAN-14, Should, weak).** A two-value flag stored as int64; mark it categorical as
   the siblings do. Remedy: add it to `FeatureTypes(categorical=...)`.

No leak in the kept features: both inputs exist at the default, and the four transforms and `event` are dropped.
Verdict for the columns: fine, with one open target question (problem 1) and two cleaning nits.

</details>

<details><summary>Split audit</summary>

**lgd: split audit (2026-10-20, re-check)**

**Verdict: right with notes.** Grouped by borrower block (run of identical LTV) is the best split the file allows for
"a loan has just defaulted, estimate its LGD" (USE-10 cold start: the borrower's other losses are not known at
default). No re-split. Two notes for the curator: the task is temporal in nature but the file has no dates (its row
order drifts in the outcome), and the group key is inferred, not a source id.

Data via `dataset_io.load(..., built=False)` and the raw `lgd.csv` for the file order.

**Facts measured**

* Shipped splits: 10 repeats x 3 folds, train 1,669-1,719 rows, test 826-876 rows, 652-653 test groups per fold, 0
  groups on both sides, 0.000 of test rows with an LTV value seen in train (all 30 splits). Blocks map 1:1 to raw runs.
* Groups: 1,958 runs; sizes 1: 1,470, 2: 415, 3: 52, 4: 18, 5: 2, 7: 1. 70 multi-loan runs mix both purposes. No LTV
  value occurs in two runs (asserted in `_clean`).
* Same models, alternative splits (R^2, 3-fold x 5 for IID / grouped; row-order splits cut at run boundaries):

| split | linear | spline | LightGBM | RF |
|---|---|---|---|---|
| IID random | 0.190 | 0.210 | 0.152 | -0.026 |
| grouped by run (shipped regime) | 0.190 | 0.210 | 0.134 | -0.156 |
| row-order blocks, 3 folds | 0.007 | 0.038 | -0.053 | -0.511 |
| forward, 3 expanding windows over the newest half | 0.100 | 0.138 | 0.062 | -0.115 |
| forward, first 2,311 rows only | 0.034 | 0.064 | -0.020 | -0.222 |

* File order: median LTV per 250 rows 0.36 -> 1.00 over rows 1-2,250, then 0.27 (Spearman LTV~position 0.59 on rows
  < 2,311): the file is close to sorted by something tied to LTV. Net of a spline in LTV and purpose, the mean LGD
  residual per 250 rows still runs -0.06 -> +0.07 (Spearman 0.05, p = 0.01).
* Forward windows (spline): bias of the forward model +0.063, +0.118, +0.045; but the same model fit on all other rows
  scores 0.071, 0.113, 0.283 on those windows against 0.068, 0.063, 0.283 forward. Most of the row-order drop is the
  narrow LTV range inside a window (less variance to explain), not a time effect; the level bias is the part the
  order carries beyond LTV.

**Problems, ranked**

1. **P4, SPLIT-6 / SPLIT-7 / SPLIT-8 / SPLIT-22 (Must / Should): the time axis is missing, and the file order carries
   some outcome.** LGD at default is a task banks validate out of time (SPLIT-6 names "a default"). The file has no
   dates; its order drifts in LTV and, net of LTV, in LGD (+0.05 to +0.12 bias forward). Whether the order is the
   default date, two portfolios (rows 2,312+ have no renting loans) or a sort is not documented, so SPLIT-22 ("keep
   the file order as time") has no evidence to stand on, and a row-order split would mainly measure an LTV range
   shift (table above). SPLIT-3: one regime; grouped is the dependency the data shows. Mildest remedy: keep the
   grouped split; state in `splits_comment` (as `fit_reason` already does) that out-of-time is the domain standard,
   what a default date would change (forward spline R^2 0.138 vs 0.210 grouped, an upper bound on the cost since the
   order is not known to be time), and recover dates if the book's chapter 10 or the authors give them. Not decided
   from this window comparison (SPLIT-21).
2. **P4, SPLIT-24 / SPLIT-25 (Must): the group key is constructed, not a source id.** It is the kind SPLIT-24 allows
   (consecutive blocks of identical values in the raw order, cf. in_vehicle_coupon_recommendation), not a similarity
   cluster or a hash: 16-digit-equal LTV only inside a run, residual LGD correlation 0.428 within runs vs 0.024 between
   neighbours (prep). Whether a run is one borrower, one collateral or one loan's repeated defaults is unknown, but
   each reading is an entity a new default would not bring with its other losses, so the split is right under all of
   them. A borrower spread over non-adjacent runs would be invisible; neighbouring-run correlation 0.024 gives no
   sign of it. Remedy: none; the definition's word "most likely" is the right hedge.
3. **P4, SPLIT-4 / SPLIT-29: the grouped split matters only for memorising models.** Smooth models are unchanged
   (linear 0.190/0.190, spline 0.210/0.210); LightGBM 0.152 -> 0.134, RF -0.026 -> -0.156. Under IID, 31% of test
   rows would share an exact LTV with train (REVIEW issue 2). The gap does not decide (SPLIT-4); the use case does,
   and it supports grouping. Remedy: none.
4. **Record field (procedure, SPLIT-5):** `required_split` in the record says Grouped in the front matter but REVIEW
   issue 2 says the record reads Random (IID); check which the record holds and align the REVIEW text. Curator.

**Checks with no problem**

* Prediction unit: one row, `labels="per_sample"`, `context="none"`: right, the loans of a block default together,
  so no sibling LGD is known at scoring (SPLIT-23).
* Near copies across the split: none (0 shared LTV values; the 120 exact and 397 feature-only duplicates sit inside
  runs).
* Groups per test fold (~652) are plenty; no few-groups domain-shift issue.
* Temporal checks (gap, label delay, training history, season windows): not applicable; no time column.

</details>

<details><summary>Domain practitioner</summary>

**lgd: domain practitioner (2026-10-20)**

Actor: a credit-risk modeller at a European retail bank who builds the LGD model for IRB capital (EBA/GL/2017/16) and
the stage-3 loss allowance under IFRS 9. Moment: a loan has just entered default. Decision: the LGD assigned to the
exposure (capital, provision, and whether the case goes to workout or collateral sale). USE-1 holds as written in
`task_summary.use_case`.

**Fit: approximate (agree with the definition)**

One sentence: the target and the moment are the real LGD decision, but with two inputs, no dates, an unverified meaning
of the zero-loss rows and no out-of-time test, the data is a textbook stand-in for the model I would build (USE-8).

**1. Inputs at the prediction point (USE-3, USE-6)**

* Have, and legitimate: `loan_to_value` (if it is LTV at default or indexed LTV; if it is origination LTV it is also
  known, only weaker) and `purpose_renting` (known from origination). No leak in either (USE-3 holds).
* Missing that I would always have at default (EBA/GL/2017/16 lists transaction, obligor, institution and external
  risk drivers): exposure at default and loan size, collateral type and region, seniority/lien, time on book and time
  since origination, months in arrears at default, borrower type and income, the date of default (vintage, the
  economic cycle / downturn indicator), the house-price index. A real retail mortgage LGD model has 5-15 drivers. Two
  inputs is the book's teaching model, not a bank model.
* Not available that should not be: none found. The dropped `event` would be a leak (it is the zero-loss part of the
  target), so dropping it is right (USE-3, LEAK-10).

**2. Target (USE-5)**

* `lgd_time`, realised workout LGD as a share of the outstanding amount: this is what I act on. Regression with RMSE
  fits: for capital and provisioning I need the expected LGD (a number per exposure, then a mean per pool), not a class.
  The record's Binary Classification would be the cure-vs-loss sub-model of a two-stage model, a component, not the
  decision; regression is the right primary task (USE-5).
* Gap: what the zero rows are. The data page labels `event` as a "Default or cure indicator" (1 = event, 0 = no event).
  In practice the 0 LGDs of retail mortgages are mostly cures (the borrower returns to performing), and regulators
  require cures inside the LGD (cure rate times LGD of cures plus (1 - cure rate) times loss LGD). Under that reading
  the 728 rows belong in the target and the definition is right. If they are "not selected" (never defaulted), they
  do not. The data page wording leans to the cure reading, but it is not settled (`fit_reason` says so correctly).
* Gap: incomplete workouts. A bank's LGD file mixes closed and open cases; the source does not say whether open
  workouts were removed or how the 0/1 bounds were cut. For a modeller this decides the bias of the target.
* Gap: discounting and costs. Whether `lgd_time` is discounted economic loss (as IRB requires) is not stated.

**3. Rows and test data (USE-10, USE-11)**

* One row = one defaulted loan = one LGD assignment: matches the decision. The borrower block as a group is plausible
  (the book defines default at the obligor level, so a borrower's loans default together and their losses are not
  known at scoring time); the grouped split is the right choice under USE-10 over IID.
* What I would face: next year's defaults (validation in practice is out-of-time and on the downturn period). The file
  has no dates, so the test set stands in for "new borrowers, same period". The row order shows a drift (mean LGD from
  0.06 to 0.49 along the file, and a second segment in the last 234 rows), which suggests time or portfolio order; a
  random-group split averages over it. This is the largest gap in the split, and the weighed factor of `use_case.md`
  ("a credit model scores future applicants, so a random split of undated applications stays approximate") applies
  directly. USE-9 does not lift it to direct: no other use case fits better.

**4. Would I use this model?**

No, not as built: two features, no vintage, no EAD, no collateral type, and an R^2 of about 0.19 (linear) would not
pass a model validation unit, and the regulator would ask for the downturn LGD and the cure treatment, which this file
cannot give. As a benchmark task it is a real, small, clean LGD regression with a known answer from the book (fractional
logit / beta / Tobit). What would make me trust it: the chapter-10 text confirming event = 0 as cures, LTV at default,
closed workouts only. What makes me distrust it: "slightly modified and anonymized" without saying how, and the
unexplained ordering drift.

**Gaps ranked by how much they change the task**

1. Two features where a real LGD model has many (EAD, collateral, seniority, vintage, arrears, macro). The task is a
   one-dimensional curve fit; methods mostly differ by how much they overfit (USE-8 approximate; probe: linear 0.193,
   random forest -0.026, LightGBM 0.119).
2. No dates: no out-of-time test, while the row order carries a drift in LGD (USE-8, weighed factor on undated credit
   data).
3. Meaning of the 728 zero-LGD rows (cure vs never defaulted): settles whether 29% of rows belong in the target (USE-5).
   The data page's "Default or cure indicator" favours keeping them.
4. Unknown treatment of open workouts, bounds and discounting (USE-5, target construction).
5. Origination vs default LTV unknown (USE-3: both are known at default, so no leak, only a weaker driver).

**What an expert would change**

* Keep regression on `lgd` with RMSE; do not switch to the record's binary (the cure/loss model is a component).
* Keep the grouped split; say in `fit_reason` that the test is "new borrowers in the same undated period", not the
  next year's defaults.
* Add to the curation comments the data page's own label for `event` ("Default or cure indicator"), which supports
  the cure reading.
* If the curator has the book, read ch. 10 for event, LTV timing and workout closure before deciding; if the cure
  reading fails, drop the 728 rows (they would not be LGD observations).
* Accept it only as a thin task; a richer public LGD set (for example a mortgage workout dataset with EAD and dates)
  would be the better LGD representative.

**Sources**

* `datasets/_dev/tabarena-v0pt2/lgd/dataset.py`, `REVIEW.md`, `curation/records/lgd.md`, the panel's claim list and task probes.
* Credit Risk Analytics data page: http://www.creditriskanalytics.net/datasets-private2.html (column list: `event`
  "Default or cure indicator", LTV "in %").
* EBA/GL/2017/16 Guidelines on PD and LGD estimation:
  https://www.eba.europa.eu/documents/10180/2033363/6b062012-45d6-4655-af04-801d26493ed0/Guidelines%20on%20PD%20and%20LGD%20estimation%20%28EBA-GL-2017-16%29.pdf
* GARP whitepaper on retail mortgage LGD under the EBA guidelines:
  https://www.garp.org/hubfs/Whitepapers/a2r1W0000015PpKQAU_Whitepaper.RiskIntell.LGD.Sept6.pdf
* Rules: `.claude/skills/knowledge-curation/references/use_case.md` (USE-1, USE-3, USE-5, USE-6, USE-8, USE-9,
  USE-10, weighed factors).

</details>

<details><summary>Blind review</summary>

**Blind review: lgd (Credit Risk Analytics LGD data, Baesens/Roesch/Scheule)**

**Verdict: exclude.** With two features, a single dominant monotone signal and a constructed grouping, this is a textbook example. It cannot tell tabular methods apart.

**Task**
A bank's credit-risk team predicts loss given default for defaulted loans (Basel IRB LGD model, provisioning). That is a real use. The source says the data are real ("slightly modified and anonymized" data from a European bank): 2,545 rows, the same count as here.

**Concerns, most serious first**
1. **Too little to benchmark.** There are only 2 features: `loan_to_value` and the binary `purpose_renting`. Under 3-fold GroupKFold, linear regression gets R2 of 0.17/0.16/0.22 and LightGBM gets 0.19/0.14/0.20. Any method that fits a smooth curve in LTV ties. The task measures noise, not model quality. Change: drop it, or keep it only as a low-dimensional sanity task.
2. **The grouping is an artefact.** `borrower_block` corresponds one-to-one with distinct `loan_to_value` values: 1,958 blocks and 1,958 distinct LTVs, each with exactly one LTV per block. The source has no borrower ID. The repeated LTVs (415 pairs, up to 7 rows) may be the same loan/collateral or a coincidence. The grouped split is defensible against copies, but calling it a "borrower" group is not documented anywhere.
3. **Duplicates.** 120 rows are exact duplicates on all columns. Most have `lgd` = 1e-5. The group split keeps them on one side, so this is fine.
4. **Target shape.** 29.5% of rows sit at 1e-5 and 6.8% at 0.99999. These are clipped bounds from the source's transformation, not true values. That is acceptable for regression, but it says nothing on tail behaviour, and a fractional/zero-one-inflated model would fit it better.
5. **Leakage handled.** The source columns Recovery_rate, lgd_time, y_logistic, lnrr, Y_probit and event (cure/default) are all outcome-derived. They have been correctly removed. `lgd` presumably equals lgd_time rescaled from percent, which I could not verify.

**Could not check**
I could not download the raw lgd.csv to confirm the column mapping, the units, or the origin of the duplicates. There are no dates, so I could not test a temporal split.

</details>

<details><summary>Precedent check</summary>

**lgd: precedents**

Precedent check for the review panel (re-check), 2026-10-20.

**What I read:**
- The panel's inputs: the earlier REVIEW.md of lgd and the verification checklist.
- The decision register (808 decisions, 4 flags).
- The definition, `datasets/_dev/tabarena-v0pt2/lgd/dataset.py`.
- Records: lgd and the same book's siblings (mortgage, corporate_credit_rating_cat_data_set_ratings_raitings, homeq_default_prediction), plus haberman_survival and sepsis_survival_minimal_clinical_records.
- Today's sibling panels: mortgage (precedent check, mediator) and corporate_credit_rating_cat (precedent check).
- Knowledge files: `principles.md`, `splits.md`, `evidence.md`, `provenance.md`, `use_case.md`, and `definitions.md` / `pipeline.md` of knowledge-data-foundry.
- Git history: commit 58ee235 of 2026-10-20 (#11, the curator's review), which changed lgd's `required_split`.

I could not read Lennart's marks on the review-page artifacts (no ArtifactData tool). Where a mark exists, it comes first.

**Verdict per decision or issue**

| # | Decision / issue | Status | Closest precedents |
|---|---|---|---|
| 1 | Regression on `lgd_time`; record says Binary | consistent; one piece of evidence departs from EV-4 | definitions.md / records.md (the record follows what ships); coad `problem_type` updated in 58ee235 (2026-10-20); sarcoma (same kind of mismatch, open); USE-5; EV-4 (TabSTAR, Lennart 2026-10-15) |
| 2 | Grouped by borrower block; record said IID | consistent; already decided, issue is stale | record changed to Grouped in 58ee235 (2026-10-20, curator's review), like airfoil_self_noise and superconductivity in the same commit; SPLIT-24: in_vehicle_coupon_recommendation, concrete_compressive_strength (2026-10-14); SPLIT-4: superconductivity (2026-10-06); barred: maternal_health_risk |
| 3 | `event` = 0 read as a cure, unverified | consistent (open fact, EV-1) | cirrhosis_patient_survival_prediction (USE-5, target redefined); mortgage (LEAK-25, rows with no recorded label dropped, panel 2026-10-20) |
| 4 | Two features only; keep as a thin task | consistent with sepsis; the opposite precedent is not named | sepsis_survival_minimal_clinical_records (keep, 2026-10-06); haberman_survival (No, Trivial, 2026-07-27); fitness_club (No, 2026-10-05); register flags 2 and 4 |
| 5 | "Slightly modified and anonymized" not explained; kept | consistent | PROV-2: bad_customer_detection (keep with a note, 2026-10-14); corporate_credit_rating_cat (same book, same question, kept with notes, panel 2026-10-20); homeq_default_prediction (retired 2026-09-24 for artefacts that the probes do not find here) |
| 6 | Row order carries the outcome; shuffled; no `ForcedIIDFromTemporal` | consistent | emscad (grouped, temporal in nature, no dates, no tag); SPLIT-8: account_debt_south_africa (2026-10-12, IID only); SPLIT-22: seismic_bumps (the order is shown to be time) |
| 8 | CreditICL as a provenance lead | consistent | EV-4: "name it only for provenance or a duplicate" (Lennart, 2026-10-15) |
| 9 | Framework note (hidden_groups.py) | not a curation decision | none |
| lic | Licence in `license` only, no issue | consistent | mortgage panel 2026-10-20 ("licence noted (EV-4)"); lucas_topsoil (2026-09-23) |
| dup | 120 exact and 397 feature-only duplicates kept, accepted checks | consistent | sepsis (duplicates are real patients, 2026-10-06); jm1's dedup (2026-10-01) was under an IID split, while here the grouped split keeps copies on one side |

**Details**

**1. Problem type (issue 1)**

**Follows.** `definitions.md` says the record's `problem_type` follows the framing that ships, with a second `_clf` folder when both framings are wanted. The issue offers exactly that as its alternative, so it matches the house route (pva_revenue_prediction_kddcup98).

The record's "Binary Classification" is not a considered decision of the curator. It is an import value from 2026-06-23 (commit 391cf7a), and no comment of Lennart's speaks to the target. Under "Who decides" it is the lowest tier, imported or legacy values. Regression is the book's own task (USE-5). The sibling mismatches were handled the same way:
- coad: `problem_type` updated in 58ee235 on 2026-10-20;
- sarcoma: Binary vs Multiclass, put to the curator in the same review;
- corporate_credit_rating_cat: regression vs classes, put to the curator in today's panel.

**Departs from EV-4, with no reason given.** The issue's fourth bullet says "KU Leuven's CreditICL treats a table with the same column and bounds as an LGD regression". EV-4 (Must; Lennart, 2026-10-15) says another collection's version of the data is "no reference for ours; name it only for provenance or a duplicate". Using it in issue 8 as a provenance lead is allowed. Using it as support for the framing is not. The other three bullets (ch. 1 p. 4, the ch. 10 errata, the R Companion's `lm(lgd_time ~ …)`) carry the point without it.

```text
**Consistency check (AI, 2026-10-20):** issue 1 of lgd cites CreditICL's treatment of the table as support for the
regression framing; EV-4 (your rule of 2026-10-15, TabSTAR's version) says another collection's version is no
reference for ours. What sets this case apart?
(a) nothing: the book's own chapter 1, errata and R Companion carry the framing, so drop the CreditICL bullet from
issue 1 and keep it only in issue 8 as a provenance lead;
(b) keep it as context, marked as not evidence;
(c) -;
(d) amend EV-4 to let another collection's framing count as supporting evidence.
```

**Open point I cannot verify.** In 58ee235 the curator's review changed lgd's `required_split` but not its `problem_type`, while coad's `problem_type` was changed in the same commit. If Lennart marked `fields.problem_type = keep` on the 2026-10-07 review page, the regression definition departs from his decision, and issue 1 should quote that mark. If the issue was left open or marked discuss, nothing departs. Check the page's `reviews/lgd` marks before finalising.

**2. Split (issue 2): settled, so drop it**

The record has said `Grouped (NON-IID)` since 58ee235 (2026-10-20, "changes from the curator's review"). airfoil_self_noise and superconductivity were switched to Grouped in the same commit. That is the curator's field mark applied, so the alternative ("IID as the record says") is stale. The prep was right to call it stale.

**The key follows SPLIT-24.** A run of consecutive rows with an LTV equal in all 16 digits, occurring in no other run, is "constructed exactly from the data". Two cases cover it:
- in_vehicle_coupon_recommendation: "consecutive blocks of identical person-level answers in the raw file order";
- concrete_compressive_strength (2026-10-14): identical values in the columns that define the entity, with the rows differing in another column (age there, purpose here: 70 of the 488 multi-loan runs mix both purposes).

It is not the barred case of maternal_health_risk. Here the key is one column plus file contiguity, not a hash of the whole feature vector, and purpose varies within runs.

**The model gaps the issue lists do not decide** (SPLIT-4, superconductivity: grouped although a random split cost at most 0.009 R²). The issue's lead evidence is the entity: the 0.42 vs 0.02 residual correlation and the book's obligor-level definition. That is the right basis. Keep the gap numbers as information only.

**3. What `event` = 0 means (issue 3)**

This is an open fact, so facts come first (EV-1). Shipping the cure reading in the meantime, with the gap named in `fit_reason`, matches how corporate_credit_rating_cat leaves its scale question (kept, with a request for chapter 8).

If chapter 10 says those loans never defaulted, two precedents point the same way: drop the 728 rows as non-observations of the target. They are cirrhosis (USE-5, the target redefined to the real one) and mortgage (LEAK-25, today: rows whose label is not recorded are dropped). Nothing departs yet.

**4. Two features (issue 4)**

**Follows sepsis_survival_minimal_clinical_records** (Lennart, 2026-10-06, kept "valid by design"). The facts match:
- The features are the source's own question. Here they are the book's models' two inputs.
- The second feature adds a small, consistent gain. Here LTV alone has skill 0.069 against 0.193 for the best linear model, and the monotone-LTV fit loses to the spline on 30 of 30 splits.
- Methods gain by smoothing.

**The opposite precedent is not named.** haberman_survival (Lennart CC, 2026-07-27) went to No with `Trivial` / `Outdated` / `Not Representative`, partly because it was "essentially two features plus a temporal component". The register flags trivial and one_feature as having opposite outcomes (flags 2 and 4). The facts that set lgd apart are on record or measured:
- 2,545 rows against ~306;
- a current use case (LGD estimation under Basel and IFRS 9, the book's chapter 10) against a 1950s-1970 survival study the curator called not representative;
- no `Trivial` finding by the task-probe rule.

So keeping lgd is consistent once those facts are written in. The issue should cite haberman as the case it departs from, not only sepsis.

```text
**Consistency check (AI, 2026-10-20):** keeping lgd (two features) follows sepsis_survival_minimal_clinical_records
(kept 2026-10-06) but differs from haberman_survival (No, Trivial, 2026-07-27: "essentially two features"). What sets
lgd apart from haberman?
(a) 2,545 rows and a current LGD use case (the book's own model inputs, Basel/IFRS 9), not a dated, unrepresentative
study, and not Trivial by the task-probe rule, recorded in issue 4 and the notes;
(b) treat it like haberman: No;
(c) reopen haberman;
(d) write a rule on minimal-feature tasks (when the source's own inputs are few).
```

**5. "Slightly modified and anonymized" (issue 5)**

**Follows PROV-2** (Should; bad_customer_detection, Lennart 2026-10-14): a plausible source, unclear in a detail, stays with a note of what to clarify. The same book's corporate_credit_rating_cat carries the same question and is kept with notes (today's panel).

PROV-3 (Must) would apply only if the modification were shown to be a rework, meaning relabelled or replaced values. The test that caught homeq_default_prediction (retired 2026-09-24: label-pure near-copy clusters, distance AUC 0.92) finds no such artefacts here. The 120 exact copies sit in borrower runs at the floor or the cap.

mortgage's data page says "a randomized selection" and its panel raised no modification question. That is a different statement on the page, not an inconsistency. The phrase on p. 14 concerns the LGD data only.

**6. Row order (issue 6)**

**Follows emscad**, a grouped task that is temporal in nature but has no dates, and carries no `ForcedIIDFromTemporal`. SPLIT-8 (account_debt_south_africa, 2026-10-12) reserves that tag for IID.

SPLIT-22 (Should; seismic_bumps) keeps the file order as time only when the order is shown to be time. Here the order tracks LTV and looks like two segments, so it is not established as time. Shuffling departs from nothing. If chapter 10 shows the order is the default date, SPLIT-3 and SPLIT-22 reopen the regime question.

**Licence (EV-4)**

lgd puts the terms ("[...] Redistribute content from Credit Risk Analytics") in `license` only and raises no issue. That is the same as mortgage (today's panel: "licence noted (EV-4)") and lucas_topsoil (2026-09-23). The sibling that departs is corporate_credit_rating_cat, which raises a licence issue; its own precedent report flags this. lgd needs no change.

**Issue numbering**

Issue 7 is missing (the prep skipped it), so the list runs 6, 8, 9. Renumber, or note the gap. This is procedure (writing.md), not a precedent question.

**Drift and third exceptions**

- **No drift by the curator** on the rules involved:
  - SPLIT-24 keys from 2026-10-06 to 2026-10-20 are consistent. airfoil's re-grouping on 2026-10-20 made the entity coarser for its use case and does not touch lgd.
  - Lennart's licence and EV-4 calls are uniform.
  - The haberman (2026-07-27) vs sepsis (2026-10-06) pair is not drift: the facts were stated and differ.
- **No third exception of one kind.** lgd is the only definition in the working copy that accepts `dataset_conflicting_duplicate_rows`. Keeping duplicates under a grouped split is an application of the rule, not an exception to it.

**Files**

- `datasets/_dev/tabarena-v0pt2/lgd/dataset.py`
- `datasets/_dev/tabarena-v0pt2/lgd/REVIEW.md`
- `curation/records/lgd.md`
- `curation/records/haberman_survival.md`
- `curation/records/sepsis_survival_minimal_clinical_records.md`
- `curation/records/homeq_default_prediction.md`
- `.claude/skills/knowledge-curation/references/splits.md` (SPLIT-24, lines 139-143; Cases, lines 216-220)
- `.claude/skills/knowledge-curation/references/evidence.md` (EV-4, lines 71-90)

</details>

<details><summary>Advocate</summary>

**Advocate: lgd**


**1. A real use case with the target the actor acts on (P3; USE-1, USE-5 Must; USE-8 Must).**
- **Evidence.**
  - The codebook says "lgd_time: Loss rate given default (LGD)" (claim audit, row 1).
  - The task is chapter 10 of the book. The R Companion fits `lgd_time ~ LTV + purpose1`.
  - The practitioner, playing an IRB/IFRS 9 LGD modeller: "this is what I act on. Regression with RMSE fits". The binary version "would be the cure-vs-loss sub-model ..., a component, not the decision".
  - The practitioner agrees with `fit="approximate"` (USE-8, approximate fit stated).
- **Answers** the record's `Binary Classification`. Precedents shows that value is an import from 2026-06-23 (commit 391cf7a), not a curator decision. That is the lowest tier under "Who decides".
- **Fix that keeps the dataset:** set the record's `problem_type` to Regression. If the curator also wants the classification framing, add an `lgd_clf` folder (definitions.md).

**2. Honest evaluation: no leak, and the split mirrors a new default (P4; LEAK-10, SPLIT-24, USE-10, SPLIT-4, all Must).**
- **Evidence, leak.** Each dropped column was recomputed from the target:
  - `Recovery_rate` = 1 - lgd (error 1e-16);
  - logit (1e-6), log(1 - lgd) (1e-5), probit (2e-7);
  - `event` = 0 exactly on the 728 rows at the floor, asserted in `_clean`.
  - Only LTV and purpose remain, and both are known at default (column audit).
- **Evidence, split.**
  - All 30 splits share 0 groups, and 0.0% of test rows have an LTV seen in train.
  - All 120 exact duplicates sit inside a single run.
  - Under IID, 31% of test rows would share an exact LTV with a train row.
- **Answers** the blind reviewer's "the grouping is an artefact":
  - SPLIT-24 allows a key "constructed exactly from the data". The precedents are in_vehicle_coupon_recommendation (consecutive blocks in file order) and concrete_compressive_strength.
  - This is not the barred maternal_health_risk case: the key is one column plus contiguity, and purpose varies inside runs.
  - The split auditor finds the split right whether a run is one borrower, one collateral or repeated defaults: "each reading is an entity a new default would not bring with its other losses".
  - The blind reviewer itself calls the split "defensible against copies".
  - By SPLIT-4, the small gap for smooth models does not decide.

**3. Worth benchmarking: not Trivial, a real signal, methods spread (P6; TP-4 Must, TP-2 Should, TP-1 Must).**
- **Evidence.**
  - Task probes raise no flags on 30 splits.
  - The best linear model beats the dummy on 100% of splits (skill 0.193, SE 0.005).
  - A monotone fit on raw LTV loses to the spline on 30 of 30 splits, so TP-4's proof of `Trivial` fails.
  - The spread between linear and random forest is +0.218 (paired SE 0.009).
  - Untuned GBDTs score 0.047 to 0.135 against 0.208 for the spline.
- **Precedent:** sepsis_survival_minimal_clinical_records was kept with the source's own few inputs (2026-10-06). It differs from haberman_survival (No, 2026-07-27) on facts precedents lists: 2,545 rows against about 306, a current Basel/IFRS 9 use, and no Trivial finding.
- **Answers** the blind reviewer's "exclude: too little to benchmark". TP-2 says no cutoff on skill and no retiring without a concrete reason in the task, and none is shown.
- **I concede** that tuned smooth methods land close together (fractional logit 0.204, tuned LightGBM 0.200, spline 0.208). The task mostly tests regularisation on small, low-dimensional data. That is a thin task, not an invalid one.
- **Fix:** write the haberman distinction into issue 4 (precedents' option (a)).

**4. `event` = 0 is an open fact, and its worst case is a definition fix, not exclusion (P3; USE-5 Must; EV-1, EV-7 Must; remedy ladder).**
- **Evidence for the cure reading.**
  - The data page calls `event` "Indicator variable for a default or cure event".
  - The book's Tobit and censored-beta code treat the 728 rows as LGD censored at 0.
  - The practitioner: in retail mortgages, zero LGDs "are mostly cures", and regulators require cures inside the LGD.
- **Evidence against.** The Heckman code treats event 0 as "not selected". Read literally, the codebook's "1 = event, 0 = no event" puts cures at 1 (claim audit, column audit).
- **What can settle it.** The data cannot decide either way (column audit). Only chapter 10 settles it, and nobody on the panel could reach it.
- **Rule.** Shipping the plausible reading with the gap named, while the decisive source is requested, is what EV-1 allows. corporate_credit_rating_cat was kept with a request for chapter 8.
- **Why the dataset stays.** If chapter 10 says those loans never defaulted, the remedy is to filter the 728 rows (precedents cirrhosis, USE-5, and mortgage, LEAK-25). That is still a definition fix.
- **Fix now:** quote the codebook line in `curation_comments` and in REVIEW issue 3, and correct "no text we read". Keep the rows; `fit_reason` already says the reading is unverified.

**5. Faithful data (P5; PROV-2 Should, PROV-3 Must).**
- **Evidence.**
  - The sha256 matches the Wayback copy of 2017-09-27 and the GitHub copy.
  - No HMEQ artefacts:
    - no jittered copies;
    - the only run pairs within 1e-6 in LTV have different LGDs;
    - runs that share an LGD multiset are all at the floor or the cap;
    - the number format of LTV changes R² only from 0.2064 to 0.2057.
  - Generated probes raise no flags.
- **Why PROV-3 does not apply.** It needs the data shown to be reworked, and nothing shows that. "Slightly modified and anonymized" without details is PROV-2: keep with a note.
- **Precedents:** bad_customer_detection (2026-10-14) and the same book's corporate_credit_rating_cat.
- **I concede** the excess of 6- and 7-decimal LTVs at LTV > 1. Fix: one line in the HMEQ note, since it does not predict the LGD.

**6. No dates; the row order carries the outcome (P4; SPLIT-6, SPLIT-22 Should; SPLIT-3; USE-8).**
- **Evidence.**
  - SPLIT-22 keeps file order as time only when the order is shown to be time. Here it tracks LTV, and the last 234 rows look like a second segment.
  - Split auditor: "most of the row-order drop is the narrow LTV range inside a window ..., not a time effect". The level bias that remains net of LTV (+0.05 to +0.12) is not shown to be time.
  - Rows are shuffled, and the group id is a hash, so the order does not reach the model.
- **Precedent:** emscad (grouped, temporal in nature, no dates, no `ForcedIIDFromTemporal`). The tag is reserved for IID (account_debt_south_africa).
- **Concession and fix:** the missing out-of-time test is the largest gap, and `fit_reason` already names it. Mildest fix: one sentence in `splits_comment` saying the test means "new borrowers in the same undated period".

**7. The remaining findings are P7 or wording; none is a failing Must (P7; CLEAN-1, CLEAN-14 Should; principles step 3 and "independent failures").**
- **Cheap fixes:**
  - Map 1e-5 and 0.99999 to 0 and 1, or keep them with the existing note. RMSE changes by less than 1e-5.
  - Mark `purpose_renting` as categorical (CLEAN-14).
  - State both residual correlations: 0.42 with the exact repeats, 0.35 without.
  - Say the drift "rises over the first four fifths".
  - Drop the CreditICL bullet from issue 1 (EV-4) and keep it in issue 8 as a provenance lead only.
  - Drop issue 2 as stale: the record says Grouped since 58ee235.
  - Renumber the issues (7 is missing).
- **Answers** the blind reviewer's target-shape figures (29.5% / 6.8%). They differ from the measured 728 = 28.6% and 143 = 5.6%, and a measurement wins (EV-2).
- Every Must holds or is fixable in the definition: LEAK-10 is fixed, SPLIT-24 and USE-10 hold, TP-4 does not trigger, PROV-3 is not shown. So exclusion is not on the remedy ladder.

**Judgment record (advocate's):**
- Verdict: ship after documentation changes.
- Validity: SEL-2 holds; USE-1 holds (approximate fit, USE-8); USE-5 open on `event` = 0, keep with the codebook quote (worst case: filter 728 rows); LEAK-10 triggered and fixed; SPLIT-24 and USE-10 hold; PROV-2 note.
- Value: TP-2 and TP-4: a real signal, not Trivial.
- Quality: CLEAN-1 bounds and CLEAN-14 purpose dtype, cheap.
- Weighed: size -, features -, source +, use case +.
- For the curator: chapter 10 for `event`; the thin-task keep against haberman.

</details>

<details><summary>Advocate rebuttal</summary>

**Advocate rebuttal: lgd**


**1. The 728 floor rows (USE-5): I accept the remedy and dispute how strongly the codebook leans.**
- **Conceded.**
  - The literal codebook line is "Indicator variable for a default or cure event; 1 = event, 0 = no event". The practitioner's "Default or cure indicator" paraphrases it and is not the page's text. My opening point 4 leaned on that paraphrase too far, and I withdraw "the data page favours keeping them".
  - REVIEW issue 3 is wrong to say "no text we read". The line belongs in `curation_comments`, `fit_reason` and issue 3.
  - Chapter 10 should be requested (EV-1, EV-7).
- **Disputed:** that the line leans against the cure reading. It is ambiguous, not contrary.
  - "1 = event, 0 = no event" does not say which event the 0 lacks. The same line also fits "1 = a loss event, 0 = the default cured".
  - The file itself argues the other way. All 728 rows carry an `lgd_time`, stored at the source's floor of 0.00001 rather than missing. Each also has every transform (`Recovery_rate`, `y_logistic`, `lnrr`, `Y_probit`), since the source squeezed 0 so that the logit and probit exist (claim audit, row 7; column audit).
  - A loan that never defaulted has no loss given default to squeeze. Building LGD transforms for it only makes sense if the source counts it as an LGD observation of 0.
  - The book's Tobit and censored-beta code treat these rows as LGD censored at 0. That is a primary source (the book's own code), so it ranks above the third-party reading (EV-2 order).
  - The Heckman "not selected" and the chapter 10 heading fit a cure-versus-loss selection model as well as a default-versus-non-default one.
- **What follows.**
  - The fact is open, not tilted.
  - While it is open, keep the rows and name the reading as an open validity risk. I accept the critic's wording on that, and I accept keeping "follows the book's Tobit and censored-beta code" next to the codebook line rather than in place of it.
  - If chapter 10 says the loans never defaulted, filter the 728 rows (cirrhosis; mortgage, LEAK-25). That is a definition fix, not exclusion.
- **Whether it blocks shipping:** shipping before the curator reads chapter 10 is the curator's call on timing. No rule requires holding the dataset for an unread source when the fix on either outcome is one filter.

**2. Stale record-split wording and stale REVIEW issue 2: conceded in full.**
- The record says Grouped (NON-IID) since 58ee235.
- Remove "instead of the record's random split" from `task_summary.changes` and "against the record's 'Random (IID)'" from `curation_comments`.
- Drop issue 2 and its `required_split` line, keeping the grouping evidence as notes. Renumber the issues (there is no issue 7).

**3. Problem type: conceded.**
- Drop the CreditICL bullet from issue 1 (EV-4 Must) and keep it in issue 8 as a provenance lead.
- I accept checking the 2026-10-07 page marks. If a `problem_type = keep` mark exists, it ranks above the AI assessment ("Who decides"), and issue 1 must quote it as a consistency check.
- Without a mark, the field is the 2026-06-23 import (391cf7a), and regression stands on USE-5.

**4. The split is described as more than it is: conceded as a note, with no re-split.**
- Both briefs agree that SPLIT-24 and USE-10 hold and that SPLIT-22 does not apply, because the order is not shown to be time.
- Change `splits_comment` to "most likely one borrower (a run of one LTV value)".
- Say the test stands for new borrowers in the same undated period, not next year's defaults.
- Give the forward bound: spline R² 0.138 against 0.210 grouped. This is an upper bound on what a dated split would cost, since the order is not shown to be time.

**5. The keep rests on one precedent (consistency rule 2): conceded. My opening point 3 asked for the same fix.**
- Put haberman_survival into issue 4 with the facts that set lgd apart: 2,545 rows against about 306, a current Basel/IFRS 9 use, and no `Trivial` proof under TP-4 (isotonic LTV loses on 30 of 30 splits).
- One correction to "the best methods tie": that holds for tuned smooth methods (0.200 to 0.208). Across model families the probes do spread (linear minus random forest +0.218, paired SE 0.009).
- Neither side asks for exclusion, so this stays the curator's weighing call.

**6. Overstated numbers: conceded.**
- State the within-run correlation as 0.42, or 0.35 without the 120 exact repeats.
- Write "rise over the first four fifths of the file".
- Add one line to the HMEQ note: 6- and 7-decimal LTVs are in excess at LTV > 1, but they do not predict the LGD (R² 0.2064 vs 0.2057).

**7. Cleaning nits: conceded.**
- Add `purpose_renting` to `FeatureTypes(categorical=...)` (CLEAN-14).
- The target bounds can be mapped to 0 and 1 or kept with the current note (CLEAN-1). Either is fine.

**Where this leaves the panel.** The only disagreement is how strongly the `event` line points one way. Both briefs prescribe the same remedy for it. No new fact came up, so I add no new points.

Agreed verdict: ship after changes.
- **Validity:** USE-5 open, quote the codebook line, keep the rows and name the risk, filter if chapter 10 says non-default; LEAK-10 fixed; SPLIT-24 and USE-10 hold, SPLIT-6 gap noted; EV-4 bullet removed.
- **Value:** TP-4 and TP-2: thin but real, with the haberman check for the curator.
- **Quality:** CLEAN-14 fix; CLEAN-1 optional.
- **Procedure:** stale record-split text removed, issue 2 dropped, numbers corrected.

</details>

<details><summary>Critic</summary>

**lgd: critic's opening brief (2026-10-20)**

**Position: ship only after changes.** Not an exclusion: no Must fails that cannot be fixed. But point 1 is a
validity question that the definition and REVIEW.md describe wrongly. It decides whether 28.6% of the rows belong in
the target, so the definition should not ship before the curator has seen the evidence in the right light.

**1. The 728 floor rows may not be LGD observations, and the definition hides the one text on it (P3, USE-5 Must; EV-2)**

* Problem: the definition reads `event` = 0 as a cure (a default with no loss). REVIEW issue 3 says "No text we read
  says that event = 0 is a cure". The data page's own codebook does speak to it, and it leans the other way. Wayback
  copy (re-extracted by me): "event: Indicator variable for a default or cure event; 1 =
  event, 0 = no event". Read literally, a cure is an *event* (1), so the 728 rows with `event` = 0 are neither a
  default nor a cure. The book's Heckman code ("not selected") and the ch. 10 heading ("LGD models that condition on
  the selecting default event", ch. 1 p. 4) fit that reading. Only the Tobit and censored-beta code fit the cure reading.
* The practitioner's quote "Default or cure indicator", and its conclusion that the page "favours keeping them", is
  not the page's text. The claim and column auditors quote the literal line, and the Wayback HTML confirms it.
* Effect: if those loans never defaulted, 28.6% of the target is not LGD. The mass at zero and much of the LTV signal
  then come from a selection step, not from a loss (the floor share falls from 43% at LTV < 0.5 to 6% above 1.2,
  column audit). The benchmark would score a mixture of "did it default" and "how much was lost".
* Remedy (mildest first): quote the codebook line in the `event` note of `curation_comments`, in `fit_reason` and in
  REVIEW issue 3, and correct "no text we read". Ask the curator for ch. 10 (pp. 271-313). If it says non-default,
  fix the definition by filtering the 728 rows (USE-5; precedents cirrhosis and mortgage, LEAK-25). If it says cure,
  keep them. If it stays open, keep them with the reading named as an open validity risk, not as "follows the book's
  code".

**2. The definition misstates the record's split, and REVIEW issue 2 is stale (procedure; writing.md; EV-2)**

* Since 58ee235 (the curator's review, 2026-10-20) the record says `required_split: Grouped (NON-IID)`. Three places
  still argue against "the record's random split": `task_summary.changes`, the grouping bullet of `curation_comments`
  ("against the record's 'Random (IID)'"), and REVIEW issue 2 with the summary line "record `Random (IID)`". So the
  definition states something false about the record, and REVIEW asks the curator to decide something they have
  already decided (precedent checker; split audit, problem 4).
* Remedy: drop "instead of the record's random split" and "against the record's ..." from the definition. Remove
  issue 2 and the `required_split` line from REVIEW and keep the grouping evidence as notes. Also renumber the issues
  (there is no issue 7).

**3. Problem type: REVIEW issue 1 rests partly on a source EV-4 bars (EV-4 Must; USE-5)**

* The record still says `Binary Classification`. Regression is right: the book's task (ch. 1 p. 4, the ch. 10 errata,
  the R Companion), the practitioner (the decision needs an expected LGD) and USE-5 all support it. But issue 1 cites
  KU Leuven's CreditICL framing as support, and EV-4 (Lennart, 2026-10-15) allows another collection only "for
  provenance or a duplicate" (precedent checker, issue 1).
* The precedent checker could not see whether the curator marked `problem_type = keep` on the 2026-10-07 page, while
  58ee235 changed coad's `problem_type` and not lgd's. If such a mark exists, the definition departs from a decision
  of the curator.
* Remedy: drop the CreditICL bullet from issue 1 (keep it in issue 8 as a provenance lead). Check the 2026-10-07 marks
  and quote any mark in issue 1. Then align the record to Regression on the curator's word.

**4. The split is presented as more than it is: undated, inferred groups, and an outcome that drifts with file order (P4, SPLIT-6 / SPLIT-22 / SPLIT-24; USE-8)**

* Facts: the file has no dates. Its order carries the outcome, beyond LTV too: forward-window bias +0.05 to +0.12, and
  the mean LGD residual per 250 rows runs from -0.06 to +0.07 (split audit). LGD models are validated out of time in
  practice (practitioner; SPLIT-6). The group key is constructed (SPLIT-24 allows it, so the regime stands), but
  `splits_comment` states "a borrower the model has not seen" as a fact. The blind reviewer flagged exactly this ("calling
  it a 'borrower' group is not documented anywhere").
* Remedy, a note and no re-split: in `splits_comment`, say "most likely one borrower (a run of one LTV value)", and say
  that the test stands for new borrowers in the same undated period, not next year's defaults. Give the bound:
  forward spline R^2 0.138 against 0.210 grouped, an upper bound since the order is not shown to be time.

**5. Value: the precedent the "keep" rests on is one-sided (P6; TP-3, TP-4; consistency rule 2)**

* Facts: two features. The best methods tie (fractional logit 0.204, tuned LightGBM 0.200, spline 0.208). Default tree
  ensembles score 0.047-0.135 and RF below zero. The blind reviewer, which read no notes, says "exclude: cannot tell
  tabular methods apart". By the rules it is not `Trivial` (isotonic LTV loses on 30 of 30 splits, TP-4) and there is
  no probe flag. So I do **not** ask for exclusion.
* Problem: issue 4 cites only sepsis_survival_minimal_clinical_records (kept). It does not cite haberman_survival (No,
  `Trivial`, 2026-07-27: "essentially two features"). The register flags this pair as having opposite outcomes
  (precedent checker).
* Remedy: put the haberman case and the facts that set lgd apart (2,545 vs ~306 rows, a current Basel/IFRS 9 use case,
  no `Trivial` proof) into issue 4 as a consistency check. It remains the curator's weighing call.

**6. Evidence numbers overstated in the notes (EV-9, writing.md; Should)**

* The within-run residual correlation is 0.42 with the 120 exact repeats and 0.35 without them (claim audit, claim 30).
  The definition cites only 0.42, in `curation_comments` and `grouping.definition`.
* "The median LTV and the mean LGD rise along the file" is not monotone: they rise over the first four fifths and then
  drop in the last segment (claims 9 and 33).
* Remedy: state both correlations, and write "rise over the first four fifths". Add one line to the HMEQ note on the
  excess of 6- and 7-decimal LTVs at LTV > 1, which does not predict the LGD (R^2 0.2064 vs 0.2057; claim 35).

**7. Cleaning nits (P7; CLEAN-14 Should, CLEAN-1 Should; weak, not a reason to hold the task)**

* `purpose_renting` is a two-value flag stored as int64. CLEAN-14 and the siblings
  (2_month_survival_rate_prediction) make it categorical. Add it to `FeatureTypes(categorical=...)`.
* The target's 0.00001 and 0.99999 are the source's squeeze for the logit and probit, not data. Mapping them to 0 and
  1 is lossless for RMSE (< 1e-5), or keep them with the current note. Either way is fine. I list this for completeness
  only.

**Judgment record (critic's view)**

```text
Verdict: ship after changes.
Validity: USE-5 open (728 floor rows, codebook line not cited; settle with ch. 10, else filter or keep with the risk
named); LEAK-10 holds (transforms and event dropped); SPLIT-24 holds (constructed key), SPLIT-6 gap noted; EV-4
departure in issue 1.
Value: TP-4 holds (not Trivial); thin task, haberman precedent to answer.
Quality: CLEAN-14 fix (purpose categorical); CLEAN-1 bounds optional.
Procedure: stale "record's random split" in the definition and REVIEW issue 2; 0.42 -> 0.42/0.35.
For the curator: issue 3 (event = 0) with the codebook line; issue 4 with haberman.
```

</details>

<details><summary>Critic rebuttal</summary>

**lgd: critic's rebuttal (2026-10-20)**

We agree on the verdict: ship after changes, no exclusion. We also agree on most of the fixes: drop stale issue 2 and
the "record's random split" wording, drop the CreditICL bullet (EV-4), cite haberman in issue 4, give 0.42/0.35 and
"first four fifths", add the format line to the HMEQ note, CLEAN-14 for `purpose_renting`, and renumber the issues.
I dispute three things.

**Advocate 1 (problem type): concede, with one check kept**

Regression is right (USE-5), and the record's Binary is an import (lowest tier). I keep one request: check the curator's
marks of 2026-10-07 on lgd's `problem_type` before the record is changed. The precedent checker could not read them,
and 58ee235 changed coad's `problem_type` but not lgd's. A mark of the curator outranks an import ("Who decides").

**Advocate 2 (leak and split): concede, except one wording point**

The regime is right (SPLIT-24, USE-10), and LEAK-10 is fixed. But `splits_comment` says "a borrower the model has not
seen" as a fact, while the key is inferred: a run could be a borrower, a collateral or repeated defaults (split audit,
problem 2). Remedy: write "most likely one borrower" in `splits_comment`, as `task_summary.split` already does.
This is a wording change (writing.md), not a re-split.

**Advocate 3 (value): concede the keep, dispute one piece of evidence**

Not `Trivial` (TP-4), and no probe flags. But the spread the advocate cites (+0.218, linear vs RF) is RF overfitting a
one-dimensional curve and falling below the dummy (-0.026). It is not a spread in skill. Tuned strong methods sit at
0.200-0.208 (the advocate concedes this). So issue 4 should say the task mostly measures regularisation, as the
advocate's own concession says, and should not present the +0.218 as evidence of spread. It stays a weighing call
for the curator.

**Advocate 4 (`event` = 0): dispute how the evidence is weighed; agree on the remedy ladder**

* The advocate's first piece of evidence "for the cure reading" truncates the codebook line. The full text
  (the Wayback copy of the data page, extracted by me) is: "event: Indicator variable for a default or cure event; 1 =
  event, 0 = no event". Both default and cure are the event (1). The 728 rows are "no event". So the page does not
  support the cure reading. At best it is neutral, and read literally it is against it.
* The practitioner's "mostly cures in retail mortgages" is general domain knowledge, not a statement about this file.
  Under EV-2 it ranks below the source's own page. And the practitioner relied on a misquote ("Default or cure
  indicator"), which the page does not contain.
* So the documented evidence is the codebook line and the Heckman code against, and the Tobit/censored-beta code for.
  The data cannot decide (column audit).
* The remedy we both name is the same: quote the line, ask for ch. 10, and filter the 728 rows if they never
  defaulted. Where we differ is the text: `fit_reason` and the `event` note must not say the reading "follows the
  book's code" without adding that the codebook leans the other way. Keeping the rows for now is acceptable only with
  that stated. It is a USE-5 (Must) risk on 28.6% of the target, so it is the curator's lead issue, ranked above the
  two-feature question (validity before value).
* The corporate_credit_rating_cat parallel (kept pending a chapter) holds only if the note there is just as candid.

**Advocate 5 (provenance): concede**

PROV-2 with a note. PROV-3 is not shown (no HMEQ artefacts, the sha256 matches the Wayback and GitHub copies).

**Advocate 6 (row order): concede**

The order is not shown to be time (SPLIT-22), so the shuffle is right (emscad). One addition to the advocate's
`splits_comment` sentence: give the bound, forward spline R^2 0.138 against 0.210 grouped, labelled as an upper bound.
Then the curator can see the size of the gap (USE-8).

**Advocate 7 (P7 and wording): concede**

The bounds mapping is optional. The blind reviewer's 29.5%/6.8% is outranked by the measured 28.6%/5.6% (EV-2).

</details>
