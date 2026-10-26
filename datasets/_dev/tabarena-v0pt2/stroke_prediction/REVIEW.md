# stroke_prediction

**Outcome:** added; recommended `No` (`No Good Target / Scientific Discovery`). The label is a stroke the patient
has already had, at a time not stated, and no decision is made with that prediction (SEL-7 and SEL-3, both Must;
issue 5); keeping the dataset needs an amendment of SEL-7. Validity otherwise: the source is traced, the training
file of the 2018 McKinsey Analytics hackathon (43,400 patients, 783 strokes), of which the record's Kaggle file is a
cut (PROV-1, PROV-8); bmi is dropped because a missing BMI follows the stroke (LEAK-10; the notes say why kick's keep
does not apply); ever_married, work_type and Residence_type are dropped because they carry nothing beyond age
(PROV-3); the glucose and age marks left in shipped columns wait on the PROV-3 evidence standard (issue 1); patients
are split at random (SPLIT-1). Value: a regularised LightGBM beats age alone on 9 of 9 splits, but by only 0.010 ROC
AUC (TP-4). Quality: ages under 2 written in months and the over-full ages 78 to 82 are kept with notes. Weighed: a
traced clinical file against a small margin over age and no atrial fibrillation or blood-pressure value. The folder
stays until Lennart decides.

**Main points:** Retire under SEL-7 as cdc_diabetes_health_indicators was, or amend SEL-7 to keep it (issue 5); only
if it stays, the PROV-3 bar for the marks left in the shipped columns (issue 1).

**Record judgment:** traced source, no good target. The record's Kaggle link is a cut of the contest file (the first
249 strokes and the first 4,861 other rows); the record's "might be fake" concern is borne out for three columns,
which are dropped, and marks remain in glucose and age (issue 1); the label is a stroke already had (issue 5).

**Issues for Lennart:**

5. **A stroke the patient has already had: retire under SEL-7, or amend SEL-7 to keep the dataset?**
   - Problem: the label is "1 - suffered stroke" (data dictionary) with no date, so a positive may have had the
     stroke before or after the record. SEL-7 (Must, narrows SEL-3) retires a label the patients who have it already
     know, predicted from features of the same time; SEL-3 (Must) needs a decision someone makes with the prediction.
   - Effect on the task: a model learns which patients have a stroke history, not who will have a stroke. The contest
     asked for "the probability of stroke happening to their patients" so that doctors "take proactive health
     measures"; the domain practitioner (a primary-care clinician) acts on a first stroke within 5 or 10 years among
     patients without one, would not use this model, and rates the fit "approximate, at the border of none".
   - For keeping (advocate): the label comes from a hospital chain's record, not from a respondent in an interview,
     which is SEL-7's wording; the contest framed the task as prediction; no trace of the stroke shows in the shipped
     features (patients who quit smoking after a stroke would make former smokers more common among strokes, and
     they are not: odds ratio 1.04, former against never smokers); hypertension (odds ratio 1.38) and heart disease
     (1.83) look like ordinary risk factors.
   - Against (critic, mediator): cdc_diabetes_health_indicators is the precedent the other way. Lennart retired it
     under SEL-7 on 2026-10-15 although its sources also framed it as screening, because positives already know and
     "no decision is made with that prediction"; that reason does not depend on how the label was recorded. A missing
     BMI follows the stroke (with the other columns held fixed, a stroke multiplies the odds of a missing BMI by
     3.68), which suggests some records were written at the stroke; the claim auditor leaves this open, since stroke
     rows assembled apart from the rest would show the same. SEL-3 fails on its own: no decision is made with an
     undated has-had label, and no other use case fits these columns (USE-9). USE-8 (P3) calls a label without a
     stated horizon approximate, but it cannot lift a Must, and here the label may come before the features.
   - No fix in the definition: the file has no dates to re-target the label on. Dated records would settle it.
   - Implemented: the folder stays, built as if kept.
   - (a) Apply SEL-7 as written: `No` + `No Good Target / Scientific Discovery` (replaces `Missing source
     information`), as cdc. Cost: a traced clinical file of 43,400 patients leaves.
   - (b) Amend SEL-7 to cover any past diagnosis known from the record. Same result, with the rule made explicit.
   - (c) Amend SEL-7 to exclude labels from clinical records in a contest framed as prediction. Keeps the dataset
     (then issue 1). The wording must say how SEL-3's decision is met and whether it holds for other datasets whose
     label is a diagnosis the patient already has (the wording goes once into selection.md). A Must takes no
     exception.
   - (d) Reopen cdc_diabetes_health_indicators to match. Cost: undoes a decision of 2026-10-15.
   - Recommendation (mediator): (a). Decision needed: (a), (b), (c) or (d).

   **Lennart (2026-10-26, discuss):** So in short, the problem is that the label might be before or after the collection of
   the feature. And we retired cdc diabetes as a result. That makes sense as the use case to take action would be
   wrong and we could not recover it. However, there could be a use cases where we want to know about people if they
   ever had or ever will have a stroke based on the information (or similiar) and use this for some action on
   screening. Could this be a reasonable task? also for cdc?

   **Answer (AI, 2026-10-26):** not as a screening task; the two halves of "had or will have" are two decisions.
   - A stroke already had is known: the patient and the doctor have it in the history, and the care that follows
     (secondary prevention) starts from that diagnosis, not from a prediction.
   - Screening acts on people who do not have the event yet: who gets a blood-pressure check, a statin or an
     anticoagulant. Its label is a first event within a horizon (a first stroke within 10 years, as QRISK or the
     Framingham stroke score predict), or a present condition only a test finds.
   - A model trained on a mixed label learns mostly the history (here a missing BMI follows the stroke, odds x3.68),
     and a screener cannot use it on people without one. The file has no dates to separate the halves, so the label
     stays a stroke already had (SEL-7), and issue 5's recommendation (a) holds.
   - cdc alike: its label is "ever told by a doctor you have diabetes", known to the respondent. The screening task
     there is undiagnosed diabetes, with a label from a lab test, as in NHANES (fasting glucose or HbA1c; CDC
     estimates about a fifth of adults with diabetes are undiagnosed). That would be a real task and a candidate for a
     later search, not a reason to keep cdc or this file.

1. **Only if issue 5 keeps the dataset: do the marks left in the shipped columns retire it under PROV-3?**
   - Problem: three columns carried nothing beyond age and are dropped (PROV-3, Must; fixing the definition comes
     before exclusion). Marks remain in two kept columns, all of PROV-3 test 4 (distributions a real record would not
     show): glucose has no value below 55.00 and a spike at 65 (721 patients at 65.xx against 320 to 386 per unit at
     55 to 64), and ages 78 to 82 hold more patients per year than 70 to 77 (435 to 698 against 336 to 446).
   - Effect: if more of the file is generated, models are scored on values nobody measured. None of the marks is
     linked to the stroke (the spike at 65 is no larger among patients with a stroke than among those without,
     p 0.45), so the label is not touched.
   - Evidence on the ages: ages 78 to 82 hold 2,756 patients, about 1,029 more than the trend of ages 73 to 77 gives,
     and 255 strokes against 238.7 expected from a fit on ages 50 to 77. The extra rows carry the higher risk of older
     ages, which fits the owner folding ages above 82 into this range (disclosure control) better than padding blind
     to the class; it points one way and does not prove it (mediator). The glucose floor may be a lab or export limit
     (advocate).
   - Rules: PROV-3 and SEL-16 (Must), EV-6 (Should). The PROV-3 retirements (customer_satisfaction_in_airline,
     ecommerce_shipping, homeq_default_prediction, churn) each had a generator, a source statement or marks linked
     to the label, so they are not like for like.
   - Implemented: the glucose and age marks kept with a note (cost: ships a file of unknown making).
   - Alternative: `No` + `AHDS` / `Data Quality Issue`, the critic's reading of option (a) of the cross-dataset item
     (cost: retires a dataset on marks not linked to the label).
   - Recommendation: apply the cross-dataset items "PROV-3 evidence standard" (which also asks whether marks count on
     the file as published or on the shipped columns) and "Amend PROV-3 for an owner's disclosure control", decided in
     one pass with credit_card_customers and hepatitis_c_egypt; the panel does not choose between their options.
     Decision needed: keep with a note or retire, as those items decide.

   **Lennart (2026-10-21):** on the cross-dataset item "PROV-3 evidence standard": "either might be strong enough;
   on the columns we ship, and if the marks on the published file leak/extend to the shipped version (which is
   again case-by-case)".

   **Answer (AI, 2026-10-21):** the standard is set (PROV-3 and EV-3 amended): marks count on the shipped columns,
   and marks of the published file only when they extend to the shipped version. The strongest marks left with the
   three dropped columns; what remains in shipped columns is PROV-3 test 4 only (the glucose floor at 55 and spike
   at 65, the extra ages 78 to 82), none linked to the stroke (p 0.45). Still open, only if issue 5 keeps the
   dataset: whether the dropped columns' marks extend to the kept ones, and whether the test-4 marks are enough.

   **Lennart (2026-10-26, discuss):** So I understand that some columns are fake, while others seem real. What do we take
   from this? can we keep the real data and still use it or is this enough info to understand it as fake.

   **Answer (AI, 2026-10-26):** the file is a mix: its owner altered or generated part of it before the contest.
   - Three columns (`Residence_type`, `ever_married`, `work_type`) carry nothing beyond age and look generated; they
     are dropped. The kept columns show only weaker marks: no glucose below 55.00 with a spike at 65, and more
     patients per year at ages 78-82 than at 70-77. Those fit an export limit and ages above 82 folded into the range
     (disclosure control) as well as generation, and none is linked to the stroke (p 0.45).
   - Keeping the columns that look real is allowed (PROV-3 as amended on 2026-10-21: marks count on the columns we
     ship), so the marks alone would not retire it.
   - But issue 5 retires it whatever issue 1 decides: the label is a stroke already had. So issue 1 needs no decision;
     with (a) on issue 5 the dataset leaves as `No` + `No Good Target / Scientific Discovery`, and `Data Quality Issue`
     can be added for the altered columns if you want the record to say both.

**Review panel:** don't ship unless the curator amends SEL-7 (mediator); if it is amended, ship after the changes
made in the definition. Claim audit: 59 claims, 47 hold, 2 refuted (the use-case wording and the record's year, both
fixed), 10 untested. Blind review: include with changes; main concerns the cited source and the dropped bmi, both
answered in the definition. Debate: agreed on the source, the bmi drop under LEAK-10, the split and dropping the three
columns; disputed: SEL-7 (issue 5) and the PROV-3 bar (issue 1). The mediator's issues 1 and 2 are this file's issues
5 and 1. The precedent check's issues 2, 3, 4 and 6, and its consistency question on bmi against kick, are settled in
the definition or the record-field rows.

<details><summary>Mediator</summary>

**Mediator: stroke_prediction**
**Recommendation (judgment record)**
```text
Verdict: don't ship (No + `No Good Target / Scientific Discovery`), unless the curator amends SEL-7 (issue 1);
  in that case, ship after the changes below.
Validity: SEL-1 holds. SEL-7 (Must, narrows SEL-3) triggered on its mechanism: a stroke the patient has already
  had, no stated time, positives already known (cdc). SEL-3 fails on its own (no decision is made with the
  prediction). No fix in the definition (no dates to re-target on). USE-8 approximate, "at the border of none"
  (practitioner). USE-3 risk cannot be tested; noted. LEAK-10 triggered, fixed (bmi dropped; a Case of LEAK-10,
  LEAK-38 does not reach). SPLIT-1/19/29 hold. PROV-1/PROV-8 hold (contest file traced). PROV-3 triggered on three
  columns, fixed (dropped); the remaining test-4 marks wait on the open evidence standard.
Value: TP-4 not Trivial (strong models above age on 9 of 9 splits, +0.010). Weighed against.
Quality: ages under 2 and the folding at 78-82 kept with notes (P7).
Weighed: traced source +, real clinical columns +, 43,400 rows and 261 strokes per fold +; small margin over age -,
  no atrial fibrillation or blood-pressure value -, the practitioner would not use the model -.
For the curator: issue 1 (apply SEL-7 or amend it); issue 2 (PROV-3 bar, only if issue 1 keeps the dataset).
```

**How the disputes were settled**
**1. SEL-7 (P2, Must).** Both sides rest on the same rule and disagree on how far it reaches, so this is not a conflict between rules. The rule's text and its one case decide it:
- **Contest framing.** The advocate's fact (ii) does not set this case apart. The cdc CC quotes sources that framed that task as screening, and Lennart retired it anyway (critic rebuttal).
- **Clinical record, not interview.** Fact (i) matches SEL-7's literal wording, "respondent ... same interview". But the rule's own reason, and the CC's, is that "positives already know", and a screening task "needs positives that do not know yet". That reason does not depend on how the label was recorded:
  - the data dictionary says "1 - suffered stroke";
  - the definition says the stroke may come "before or after the record";
  - the BMI pattern suggests some records were made at the stroke itself.
- **SEL-3 fails on its own.** Even on the narrow reading of SEL-7, SEL-3 still needs "a decision someone makes with the prediction". The practitioner says no decision is made from an undated has-had label, and USE-9 offers no other use case. Every Must has to hold on its own, so this is an independent failure.
- **USE-8 cannot lift it.** USE-8 is P3, below P2, and its "label without a stated horizon" covers a label that comes after the features. Here the label may come before them.
- **"P3 informs P2" cuts against keeping.** The use case, screening for future strokes, is exactly what this label cannot serve.
- **What remains.** Keeping the dataset is an amendment and not an exception, because a Must has no exceptions. Both sides agree on this. The amendment is the curator's call.

**2. PROV-3 remaining marks (P5, Must).** This ranks below issue 1 and decides nothing unless issue 1 keeps the dataset.
- The remedy ladder puts fixing the definition before exclusion, so dropping the three columns comes first. Both sides agree.
- The strongest marks leave with those columns: test 6, the dependence real NHANES data shows, and test 4, married 45.0% / 45.0% for women and men.
- What remains in kept columns is test-4 marks only: the glucose floor at 55, the spike at 65, and the extra ages at 78-82. None is linked to the class (glucose spike p 0.45).
- Whether option (a) of the open item retires the dataset depends on wording the curator has not written: does (a) count marks on the file as published, or on the columns we ship? The critic's "under (a), `No`" assumes the first. That wording question is open.
- My check (thread-capped) on the age folding:
  - ages 78-82 hold 2,756 patients, about 1,029 more than the 73-77 years would give;
  - they hold 255 strokes, against 238.7 expected from an age trend fit on ages 50-77;
  - so the extra rows carry the higher risk of older ages. That fits top-coding of ages above 82, the open "disclosure control" item, better than padding blind to the class. This points one way but does not prove it.

**Changes to make now (no decision needed)**
1. Record: change `year` from 2021 to 2018, set `source_links` to the contest page and Mendeley doi:10.17632/x8ygrw87jw.1, and remove `Missing source information` (PROV-8, PROV-9, PROV-1).
2. Drop `ever_married`, `work_type` and `Residence_type` instead of "kept as published" (PROV-3, fix in the definition; AUC 0.8505 vs 0.8501, each split within ±0.002). Update `changes`, `fit_reason`, the "Partly generated" bullet and the third Decision.
3. bmi bullet: write "one possible reason" for the admission mechanism, add the N1 id fact, and record the dataset as a Case of LEAK-10. Name what sets it apart from kick: the leak is measured in every age band, BMI is a named field, and the host was not the data owner (LEAK-10, LEAK-38).
4. `use_case`: use the contest's wording, "the probability of stroke happening ... proactive health measures", and add that the label records a past stroke. Claim audit #2 refuted the current wording (USE-2).
5. `fit_reason` and the prediction-point bullet: the features may have been recorded at the stroke admission (BMI pattern), and the glucose window is not stated. Also name what is missing: atrial fibrillation, a blood-pressure value, diabetes and cholesterol (USE-3, USE-8).
6. Cite the NHANES calibration (n 35,850; married p 3e-52; 50.7% / 38.0% at ages 25-29) in place of the BRFSS figures, which can no longer be checked because the file is gone (EV-2, EV-3).
7. Reconcile the counts: "5 of 9" compares age with the untuned probe; "9 of 9, +0.010" compares it with the regularised LightGBM (TP-4, EV-3).
8. REVIEW.md: put the SEL-7 issue first, remove cdc as supporting evidence (it was retired), and remove the `2ndTierData` fallback (a tag cannot stand in for a Must; root REVIEW.md Tags item). Optionally add one sentence on the drift along the id to the IID bullet.

**Issues for the curator (ranked)**
**1. SEL-7 / SEL-3: a stroke the patient has already had (P2, Must).**
- **Problem:** positives already had the outcome at an unknown time; no decision is made with the prediction.
- **Effect:** the benchmark would measure association with a known history, not risk.
- **Advocate's best evidence:**
  - the label is a hospital chain's record, not a self-report;
  - the contest asked for "the probability of stroke happening";
  - no measured trace of the stroke shows in the shipped features (former vs never smoker OR 1.04);
  - the odds ratios look like plausible risk factors (hypertension 1.38, heart disease 1.83).
- **Critic's best evidence:**
  - the cdc framing was the same and did not decide;
  - the BMI pattern (adjusted OR 3.68) points to records written at the stroke;
  - the practitioner rates the fit "at the border of none".
- **Decision needed:**
  - (b) treat like cdc: `No` + `No Good Target / Scientific Discovery` (recommended);
  - (d1) amend SEL-7 to cover any past diagnosis known from the record, however recorded (same result, rule made explicit);
  - (d2) amend SEL-7 to exclude labels from clinical records in a contest framed as prediction. The wording must also say how SEL-3's "decision someone makes" is met, and whether the same holds for other datasets with has-had labels;
  - (c) reopen cdc.
- **What would settle the facts:** dated records. The file has none.

**2. PROV-3: what bar the remaining marks must meet (P5, Must). Only if issue 1 keeps the dataset.**
- **Problem:** after the drop, the glucose floor and spike and the age folding remain. All are test-4 marks, none linked to the class.
- **Critic:** under option (a) the dataset is `No` + `AHDS` / `Data Quality Issue`.
- **Advocate:** none of these marks is linked to the class. The floor may be a lab or export limit. The folding may be the owner's top-coding (my check: 255 strokes observed vs 238.7 expected, which fits that reading).
- **Decision needed:** choose (a) or (b) of the open "PROV-3 evidence standard" item. For (a), also say whether marks count on the file as published or on the shipped columns. Decide the "disclosure control" item (framingham) in the same pass, together with credit_card_customers and hepatitis_c_egypt.

**3. Weighing, if kept (P6, value).** The model adds +0.010 over age alone, atrial fibrillation and blood-pressure values are missing, and the practitioner would not use it. On the other side are the traced source and real clinical columns at 43,400 rows. None of these decides alone.

**Agreed facts**
- The source is the 2018 McKinsey / Analytics Vidhya training file: 43,400 rows, 783 strokes. It is byte-identical to the Mendeley deposit, and the Kaggle file is a cut of it (5,110 rows, 0 mismatches).
- Missing BMI follows the stroke: adjusted OR 3.68 (2.98-4.54), in every age band. The BMI values add nothing beyond the missingness. Smoking missingness is not linked to the stroke (OR 0.91-0.96).
- One row per patient. The contest split patients at random. Hidden-group probe: 0 candidates. 1-NN agreement 0.965 is chance level.
- Not Trivial: 0.8505 vs 0.8404 for age alone, on 9 of 9 splits. The smallest test fold has 261 strokes.
- The three columns carry nothing beyond age (LR p 0.39-0.88; NHANES p 3e-52). Glucose has a floor at 55 and a spike at 65 that is not linked to the class (p 0.45). Ages 78-82 are over-full. Label-free distance AUC is 0.690 against 0.826; no generated-data flag.
- The label is "suffered stroke", with no date.
- `2ndTierData` is no substitute for a Must.

**Consistency with precedent**
- **cdc_diabetes_health_indicators (SEL-7):** followed. Neither offered fact sets this case apart under the CC's reason.
- **kick (LEAK-38):** departed from on purpose. The distinguishing facts are recorded and the dataset becomes a Case of LEAK-10; both sides agree.
- **PROV-3 retirements (airline, ecommerce_shipping, homeq, churn):** not like for like, since each had a generator, a source statement or marks linked to the label. The deferral to the open item is consistent with this.
- **hr_analytics:** consistent. The first appearance is shipped over the Kaggle copy.
- **sepsis_survival vs fitness_club (TP-4):** consistent.
- **breast_cancer_prediction ("P3 informs P2"):** applied. Here it argues against keeping.

Files: `dataset.py`, `REVIEW.md`, the stroke_prediction record, the cdc_diabetes_health_indicators record, the cross-dataset REVIEW.md (PROV-3 evidence standard, disclosure control, Tags), `selection.md` (SEL-3, SEL-7).

</details>

<details><summary>Claim audit</summary>

**stroke_prediction: claim audit (claim-auditor, 2026-10-20)**
Tests on the raw contest file; LightGBM on the 9 shipped splits (raw rows aligned to the shipped frame, 0 label
mismatches); a real-data calibration on NHANES 1999-2018. Earlier evidence reused only for files (Kaggle cut, contest
test file, Mendeley copy, problem statement) of the run of 2026-10-07. LightGBM spec here: 400 trees, lr 0.02, 8 leaves,
min_child 100, lambda 10. Licence and pretraining overlap are not used as evidence.

Summary: 59 claims; 47 hold, 2 refuted (both wording/record, not validity), 10 untested (6 judgment or precedent, 4
external sources). The two load-bearing claims hold under refutation attempts: PROV-3 (three columns carry nothing
beyond age) and the missing-BMI leak (OR 3.68). New finding: missing BMI is a row-counter pattern among non-strokes only.

**Table**

| # | Claim (short) | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 1 | question: has the patient had a stroke | DS task_summary | label vs data dictionary | holds | dictionary "1 - suffered stroke" | USE-1 |
| 2 | "the contest asked whether a patient has had a stroke" | DS use_case | read contest problem statement | **refuted (wording)** | statement: "predict the probability of stroke happening to their patients. This will help doctors take proactive health measures"; the contest framed risk prediction, the dictionary a prevalent label | USE-1, USE-2 |
| 3 | 43,400 patients; place and period not stated | DS row | count; read statement | holds | 43,400; statement says only "over the last few years", no place | PROV-2 |
| 4 | stroke 1.8% | DS predicted | count | holds | 783/43,400 = 1.80% | - |
| 5 | known: 9 features | DS known | shipped columns | holds | 9 features, no bmi/id | - |
| 6, 36, 42 | IID, random patients, one row per patient | DS split, bullet, regime | id unique; id vs label; model with id; id order | holds | id unique; AUC(id->stroke) 0.506; stroke rate flat over 22 id blocks (1.4-2.6%); LightGBM with id 0.848 vs 0.850 | SPLIT-1, LEAK-16 |
| 7 | whole training file, bmi dropped | DS changes | shipped frame | holds | 43,400 rows, bmi absent | - |
| 8, 9 | fit approximate: no dates, label at any time, facts may postdate | DS fit | look for date columns; read statement | holds (judgment) | no time column; dictionary label is prevalent | USE-8 |
| 10, 22, 47 | Residence, married, work_type carry nothing beyond age (adult LR p 0.39-0.88; sex 7e-145) | DS fit_reason, bullet; REC | LR: each column ~ 1-year age vs + all other columns incl. stroke, adults | **holds** | married p 0.50, urban 0.39, self-emp 0.82, govt 0.63; also not on each other given age (p 0.86, 0.19, 0.17, 0.97); sex control 1.8e-144; hypertension 3e-85, heart 1e-120; for stroke given age+clinical the three add nothing (p 0.43) | PROV-3, SEL-16, EV-1 |
| 23, 51 | real survey (BRFSS 2015) shows the dependence | DS bullet; REVIEW | BRFSS file gone (the earlier run's scratch folder was deleted); substitute calibration on NHANES 1999-2018 adults, n 35,850 | BRFSS numbers untested; **direction holds on NHANES** | NHANES married ~ others beyond 1-year age: LR 251, p 3e-52 | PROV-3 (calibrate), EV-3 |
| 24, 41, 48 | married alike by sex at every age; 45.0/45.0 at 25-29; BRFSS 53.8/40.3 | DS bullet, decision 3 | rate by band x sex; NHANES as calibration | holds (data); BRFSS figures untested | 25-29: 45.0/45.0; all bands within 1.6 pts; NHANES 25-29: 50.7% women / 38.0% men; work types by sex: govt 15.2/15.2, private 66.1/64.8, self-emp 18.6/19.9 | PROV-3 |
| 48 | Residence a coin flip, independent | REC | urban share by work type; LR | holds | 49.3-52.5% in every work type; LR p 0.39 | PROV-3 |
| 25 | glucose none below 55.00, spike at 65 | DS bullet | histogram per unit, by class | holds; not label-linked | min 55.0; 721 at 65.xx vs 320-386 at 55-64; spike ratio 1.69 class No, 1.52 class Yes (binom p 0.45) | PROV-3 test 4/5 |
| 26 | no statement of how the file was made | DS bullet | absence claim; no search run here | untested | - | EV-7 |
| 27 | three columns add nothing (LightGBM 0.850 with and without) | DS bullet | LightGBM, 9 shipped splits | holds | 0.8505 vs 0.8501; per split -0.0019 to +0.0016 | TP |
| 28 | missing BMI OR 3.69 (2.99-4.57) given all columns | DS bullet | logit nobmi ~ stroke + 1-year age + all columns; spline variant; + id | **holds** | 3.68 (2.98-4.54); spline 3.66 (2.97-4.52); with id spline 4.10 (3.29-5.11); reverse direction OR 3.74 | LEAK-2, LEAK-10, EV-1 |
| 29 | likely reason: record made at stroke admission (hypothesis) | DS bullet | NHANES calibration; id trend by class | untested (ambiguous) | real stroke survivors miss BMI more (NHANES OR 1.86, 1.62-2.13): a real mechanism is plausible; but see new finding N1 | EV-6 |
| 30 | BMI values add nothing beyond missingness (0.847 without, 0.846 random) | DS bullet | LightGBM variants | holds | without 0.8505; missing at random 0.848; flag only 0.8647 >= bmi values 0.8629 | LEAK-10 |
| 40 | per age band 16.5-20.8% / 9.3-14.5% / 1.6-3.6%; adjusted OR 3.7 | DS decision 2 | recompute | holds | 20.8/19.2/19.8/16.5; 14.5/9.3/10.5/9.6; 1.6/2.2/3.6/3.3 | LEAK-2 |
| 54 | OR exceeds hypertension 2.50, heart 2.19; holds at 2.95-4.12 in every adult band | REVIEW | same model; per band (20-40, 40-60, 60-70, 70-83) | holds in direction; range not reproduced | hyp 2.45, heart 2.20; bands 7.85 (2.4-25.8), 5.21 (3.4-8.0), 2.96, 3.37 | EV-1 |
| 55 | bmi kept 0.861 (+0.014) | REVIEW | LightGBM | holds | 0.8629 (+0.0125, 9 of 9 splits) | - |
| 11, 16 | 43,400 / 783; sha256 540986ae... | DS constants | count; sha256sum | holds | identical sha256 for warehouse, S3 and Mendeley copies | PROV-8 |
| 12, 21, 46 | Kaggle file = first 249 strokes + first 4,861 others; 8.5x rows, 3.1x strokes | DS constants, bullet; REC | match Kaggle file by id and every column | **holds** | 5,110 ids all in the contest file, same set and order as the head-cut, 0 value mismatches; 8.49x / 3.14x | PROV-13 |
| 13 | year 2018, contest 2018-04-14 | DS | contest metadata | holds | startDate 2018-04-14 | - |
| 14 | licence | DS | not evidence | not assessed | - | EV-4 |
| 15 | test file 18,601 rows, no labels | DS download | read file | holds | 18,601 rows, no stroke column, 0 ids shared with train | - |
| 17 | byte-identical Mendeley dataset.csv; Python extraction tested 2026-10-06 | DS download | sha256 | identity holds; extraction untested | same sha256 | PROV-8 |
| 18 | Mendeley deposit = data of Liu et al. AIM 101:101723 | DS bibtex | DataCite record | holds | 101723 in the DataCite JSON | PROV-10 |
| 19, 20 | start file; prediction point; dictionary label | DS bullets | statement | holds | - | LEAK-1 |
| 31, 39 | id unique, says nothing about the label | DS bullet, code | uniqueness; AUC | holds | unique; AUC 0.506 (but AUC 0.70 for missing BMI, see N1) | - |
| 32 | dtypes as published, target No/Yes | DS | frame dtypes | holds | 5 categoricals, 0/1 ints, target No/Yes | CLEAN |
| 33 | smoking blank 30.6%, all under-10s; OR 0.96 | DS bullet | count; logit | holds | 30.6%, 100% of under-10s; OR 0.91 (0.76-1.10) | LEAK-2 |
| 34, 58 | ages under 2 in 0.08 steps; 78-82 over-full; strokes at 1.32 and 14 | DS bullet; REVIEW | values | holds | 0.08...1.88; 698/626/543/454/435 at 78-82 vs 336-446 at 70-77; strokes under 20 at 1.32, 14 | - |
| 35 | 62 repeats without bmi, none a stroke, distinct in BMI | DS bullet | duplicated() | holds | 62, 0 strokes, 0 with bmi | LEAK-16 |
| 37, 56 | age alone 0.840; LightGBM 0.850; 9 of 9 above age | DS note; REVIEW | LightGBM, raw age | holds | 0.8404; 0.8505; 9 of 9, mean +0.0101 | TP-1 |
| 38 | work_type children: 6,156, ages 0.08-16, 2 strokes | DS accepted warning | count | holds | 6,156; 0.08-16; under-13 not "children" only 2 rows | - |
| 49 | clinical columns look real | REC | LR of each on the others beyond age | holds | hypertension p 3e-85, heart 1e-120, sex 2e-144 | PROV-3 |
| 52 | test file LR p 0.24-0.85; work by sex p 0.64-0.79 | REVIEW | same LR on test file | holds | test file p 0.21-0.85 (urban 0.21); sex control 5e-60 | PROV-3 |
| 53 | male x heart disease age-adjusted OR 2.28 | REVIEW | logit | holds | 2.28 | - |
| 57 | 261 strokes per test fold (83 Kaggle) | REVIEW | split counts | holds | smallest 261; 249/3 = 83 | EV-5 |
| 43 | record year 2021, source Kaggle | REC | contest metadata | **refuted (stale record)** | data date 2018-04-14; 2021 is the Kaggle re-upload | PROV-1 |
| 44, 45 | Kaggle discussion: maybe fake; educational use only | REC | thread not fetched | untested | - | EV-7 |
| 1, 50 | priority and use-case judgment | DS, REC | judgment | not testable | - | - |
| 59 | precedents (churn, airline retired; AV siblings 2nd tier) | REVIEW | precedent-checker's remit | untested | - | - |

**Implied claims (not written down)**

| Implied claim | Test | Result | Evidence | Rule |
|---|---|---|---|---|
| Every shipped feature is known at the prediction point | needs dates | untested (cannot be) | no time column; hypertension, heart disease, glucose, smoking may be post-stroke; disclosed in fit_reason | LEAK-1, USE-3 (Must) |
| No other shipped feature has outcome-driven missingness | only smoking has NA | holds | smoking OR 0.91 (0.76-1.10) | LEAK-2 |
| No row is a copy across the split | exact feature copies, 9 splits | holds | 244 test rows with a train copy over 9 splits (about 0.19%), all non-strokes | LEAK-16 |
| The split is the one the use case needs | id-order trends | holds | label flat over id; features almost flat (glucose rho -0.04) | SPLIT-1 |
| The target is the real-world target | statement vs dictionary | approximate, disclosed | risk prediction asked, prevalent label given | USE-5, USE-8 |

**New finding N1: missing BMI is a row-counter pattern among non-strokes only (PROV-3 test 2 and 5)**
- Missing BMI falls with id for non-strokes and not for strokes: no stroke, no comorbidity 6.9% -> 1.7 -> 1.1 -> 0.5 ->
  0.3% by id quintile (Spearman p 2e-192); comorbid non-strokes 15.0% -> 7.1% (p 2e-13); strokes 20.7, 19.2, 16.9,
  14.6, 18.1% (p 0.38). AUC of id for missing BMI 0.70 (0.52 among strokes). The test file shows the same fall (8.1%
  -> 1.3%).
- So the crude OR grows from 3.1 to 18.4 across id quintiles; the adjusted OR is 1.79 (1.09-2.95) for ids below
  10,000. Adjusting for id raises the pooled OR to 4.1. No other column has a class-specific id trend (all |rho| < 0.07).
- What it changes: the drop of bmi stands (stronger with id). The admission hypothesis (claim 29) does not explain why
  non-stroke records get more complete with id while stroke records do not; equally consistent with stroke rows
  assembled or generated separately. It is a label-linked mark on the bmi column (dropped), not on a shipped column.
  Calibration: NHANES shows a real stroke-BMI missingness link (OR 1.86), smaller than here.

**Refuted and untested, ranked (principles.md: validity first, Must first)**
1. Untested, Must (LEAK-1/USE-3): features known at the prediction point. Cannot be tested without dates; already
   disclosed (`fit="approximate"`). Mildest remedy: none beyond the current wording.
2. Untested, PROV-3 calibration (claims 23, 41, 51): the BRFSS figures; the BRFSS file is gone. The NHANES
   calibration reproduces the direction (married depends on the others, p 3e-52; 50.7% / 38.0% at 25-29). Mildest
   remedy: cite NHANES next to BRFSS, or restore the BRFSS subset into the run folder.
3. Untested (claim 29, hypothesis): see N1. Mildest remedy: write "one possible reason" and add the id fact: "among
   patients without a stroke a missing BMI becomes rarer with the Patient ID (6.9% to 0.3%), among strokes it does not".
4. Refuted, wording (claim 2): the contest did ask for stroke risk to act proactively; the use case matches the
   contest. Remedy: "the contest asked for the probability of a stroke, for proactive care; the label records a
   stroke the patient has had". The checklist's USE concern ("framing the contest did not state") falls with it.
5. Refuted, record (claim 43): record `year` 2021 and `source_links` point to the Kaggle re-upload. Remedy: record
   year 2018 and the contest link (already listed in REVIEW.md "Record fields that disagree").
6. Untested, low stakes: claims 17 (extraction run), 26 (absence of a generator statement), 44-45 (Kaggle thread),
   59 (precedents).

No claim that bears on validity is refuted. PROV-3 holds harder than written: the three columns are independent also
of each other and of stroke given age, where real NHANES data show strong dependence.

</details>

<details><summary>Column audit</summary>

**stroke_prediction: column audit (review panel, 2026-10-20)**
Frame: `dataset_io.load(..., built=False)` (origin `rebuilt`), 43,400 x 10, target `stroke` (No 42,617 / Yes 783).
Raw: the contest's training file. Prediction point (first curation bullet): a
patient's record, undated, written before or after the stroke; the label is "has had a stroke" (USE-3). The contest
page no longer shows its data dictionary; meanings are from the Kaggle cut's codebook (fedesoriano), which uses the
same columns.

**Column table**

| column | meaning | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| `id` (raw) | patient id, unique per row | n/a | dropped; AUC vs label 0.506 | fine | CLEAN-3 |
| `bmi` (raw) | body-mass index | no: missingness follows the stroke (adj. OR 3.6-3.7, prep re-measured) | dropped; values add nothing beyond the missingness (0.847 without, 0.846 random-filled) | fine (leak, correctly removed; no milder fix: any imputed value becomes the marker) | LEAK-10, LEAK-6, LEAK-7 |
| `gender` | Female / Male / Other | yes | category, 3 levels; Other = 11 rows, 0 strokes, kept | fine | CLEAN-14, CLEAN-11 |
| `age` | age in years; under 2 written as years + 0.08 per month | yes | float64, 0.08-82; no fractions at 2+; 78-82 over-full (698 at 78 vs 336-446 at 70-77): top-coded or folded ages | fine; anomaly documented (PROV-3 evidence, see problem 2) | CLEAN-11, CLEAN-21 |
| `hypertension` | 0/1, has hypertension | unknown: undated, may be diagnosed at or after the stroke | int64 0/1, no missing | question (shared with the label's timing) | LEAK-10, LEAK-11, USE-3 |
| `heart_disease` | 0/1, has heart disease | unknown, as above | int64 0/1, no missing | question (same) | LEAK-10, USE-3 |
| `ever_married` | Yes / No | yes (static) | category; none married under 17 | fine as a column; carries nothing beyond age (generated) | PROV-3, SEL-16 |
| `work_type` | Private / Self-employed / Govt_job / children / Never_worked | yes | category; `children` = ages 0.08-16 (6,156 rows, 2 strokes: accepted warning, age effect) | fine as a column; carries nothing beyond age (generated) | PROV-3, SEL-16 |
| `Residence_type` | Urban / Rural | yes | category, 50.1 / 49.9, independent of every column | fine as a column; a coin flip (generated) | PROV-3, SEL-16 |
| `avg_glucose_level` | average blood glucose, mg/dL (unit and window not stated) | unknown: averaging window not stated, could include post-stroke values | float64, 55.00-291.05, 2 decimals, no missing; nothing below 55.00, flat ~350 per mg/dL at 55-64, 721 at 65; stroke share at 55-70 is ordinary (1.3-1.7%), so not class-linked | question (window) + data-quality evidence | LEAK-10, PROV-3 |
| `smoking_status` | never smoked / formerly smoked / smokes; blank = unknown | mostly yes; "formerly" could follow a stroke | category, blank kept as missing (30.6%; 98.3% under age 10); missingness alone AUC 0.562 is age, adj. OR 0.95-0.96 | fine; post-stroke quitting not seen: adj. OR former vs never 1.04 (bootstrap 0.85-1.27, ages 30+) | CLEAN-10, LEAK-10 |
| `stroke` (target) | 0 no stroke / 1 suffered stroke | the label | 0/1 -> No/Yes category; no missing | fine | CLEAN-15, USE-5 |

Duplicates: 62 rows repeat an earlier row without bmi (124 in groups, ages 1.88-67, none with a stroke), each pair
differs in raw BMI: nine coarse features and plausible repeats, keep (LEAK-18, LEAK-16). No column holds statistics
over all rows (LEAK-29/30) and no id encodes the label.

**Problems, ranked (principles.md)**
1. **P4, question: timing of the clinical columns (LEAK-10, USE-3; Should-level, unmeasurable).** `hypertension`,
   `heart_disease` and `avg_glucose_level` are undated; with a "has had a stroke" label they may be recorded at or
   after the stroke (adj. ORs in ages 30+: hypertension 1.38, heart disease 1.83, both plausible for risk factors,
   not inflated). The one testable post-stroke trace, quitting smoking, is absent (OR 1.04). Mildest remedy: none in
   the data; the prediction-point bullet and `fit = approximate` already document it (LEAK-11 style). Add to the
   bullet that the glucose averaging window is not stated.
2. **P5, generated or altered data (PROV-3, SEL-16; Must).** Three columns carry nothing beyond age, glucose has a
   hard floor at 55.00 and a doubled bin at 65, ages 78-82 are over-full. None is linked to the label (glucose bins
   carry the base rate), so it is a provenance verdict, not a leak. Remedy: as REVIEW.md issue 1 (retire `No` +
   `AHDS` / `Data Quality Issue`; if kept, `2ndTierData` and drop the three columns). Add the 65 spike counts and
   the age-78 count to the curation bullet if the folder stays.
3. **P4, bmi (LEAK-10; resolved).** The drop is right and minimal; no action.
4. **P7, cleaning (CLEAN-14; minor, optional).** `hypertension` / `heart_disease` stay int64 0/1: acceptable, the
   bullet states it. No proxy missing values, impossible values or reversed encodings found; dtypes match meaning.

</details>

<details><summary>Split audit</summary>

**stroke_prediction: split audit (re-check, 2026-10-20)**
**Verdict: right with notes.** IID 3x3 (seed 4267) mirrors the task: one row per patient (id unique), a model scores
new patients, the label is undated, and the contest itself split at random over ids.

**Regime (SPLIT-1 to SPLIT-5, USE-10, USE-11)**
- Entity: one patient per row (43,400 unique ids, 1 to 72,943). The use case is a new patient's record: cold start,
  one row per entity, so IID without grouping (USE-11). No second visit of a patient is in the file.
- No time column; the label is "has had a stroke" at a time not stated. Not a stream or forecasting (SPLIT-6/7 do not
  apply). No windows, gap or label delay can be built (SPLIT-9/10 not applicable); the undated label is a fit gap
  already written in `fit_reason` (USE-3), not a split defect.
- Source split (SPLIT-19, SPLIT-5 checked against the data): the contest test file (`test_v2akXPA.csv`, 18,601 rows,
  downloaded to the scratchpad only) has ids 2 to 72,942, no overlap with train, and makes up 29.3% to 31.1% of every
  id decile of the 62,001 ids: a random split over patients. The shipped IID split follows it.

**Shipped folds (EV-5, TP-9)**
- 9 splits, train 28,933-28,934, test 14,466-14,467, 261 strokes in every test fold (stratified), no train/test
  overlap.

**Problems, ranked**
1. **P4, SPLIT-7 / SPLIT-22 (note, no change): the id carries an order, likely the record order.** Along the id,
   BMI missingness falls from 14.6% (lowest id twentile) to 1.4% (highest), mean glucose rises 103.1 to 106.1
   (Kruskal p 1e-14), smoking_status and work_type shift (chi2 p 0.0007, 0.007); the same BMI trend holds in the
   contest test file (6.0% / 2.3% / 1.3% by id tercile). Row order carries nothing (shuffled; Spearman id-row -0.001).
   The stroke share does not move with the id (chi2 over terciles p 0.41; 1.4% to 2.5% per twentile, no trend).
   Alternative split measured (same models, bmi dropped):

   | split | linear AUC | LightGBM (regularised) | age alone | strokes per test |
   |---|---|---|---|---|
   | random 3x3 (shipped design) | 0.850 (min 0.839) | 0.849 (min 0.838) | 0.840 | 261 |
   | id-ordered, oldest 2/3 -> newest 1/3 | 0.836 | 0.836 | 0.828 | 259 |
   | id-ordered, 3 expanding windows | 0.837 (0.811-0.850) | 0.838 | 0.828 | 80-92 |
   | id-ordered, newest 2/3 -> oldest 1/3 | 0.869 | 0.869 | 0.857 | 247 |

   The score moves with age alone in both directions (margin over age 0.008-0.013 in every split), so the id-ordered
   difference is test-set composition, not drift that random splitting hides. The id meaning is not stated (it could
   be time, a site or an export order) and the contest split at random over it. Rule: SPLIT-30 / SPLIT-4 (the gap
   never decides; the context does). Mildest remedy: none to the split; optionally one sentence in the IID bullet that
   the id order shows a collection drift in BMI recording and glucose, and an id-ordered split scores 0.836 against
   0.850 with the same margin over age. Side note for the leak auditor: within strokes BMI stays missing at 15.8% to
   19.8% across id terciles while other patients fall from 6.1% to 1.2%, which supports dropping `bmi` (LEAK-11).

2. **P4, SPLIT-29 / LEAK-16 to LEAK-21 (pass): hidden groups and copies.** Hidden-group probe: 0 candidates, 0.0% of
   rows in near-copy clusters at 0.7-0.9. Exact feature duplicates: 124 rows in 62 sets, 0 strokes, 0 conflicting
   labels; in the raw file each pair differs in BMI (different patients). Test rows with an exact copy in train: 0.2%;
   1-NN agreement 0.965 = chance. Rows sharing gender, age and glucose to the cent: 1,350, of them 13 strokes; too few
   to inflate a fold scoring 261 strokes. No remedy.

3. **P3, USE-3 / SPLIT-8 (already documented): no prediction point in time.** Whether the record precedes the stroke
   is unknown, so neither a temporal split nor a gap can be built; this is not a "forced IID from temporal" case
   (the task is a status classification, not a temporal stream). Written in `fit_reason`; no split remedy.

**Judgment record**
Validity: SPLIT-1 holds (IID, matches a new-patient use and the contest split); SPLIT-19 holds; SPLIT-29 holds (no
hidden groups); SPLIT-7 checked: id order shows feature drift, label flat, id-ordered split 0.836 vs 0.850 with the
same margin over age.
For the curator: optional note on the id-order drift in `curation_comments` (IID bullet); no re-split.

</details>

<details><summary>Domain practitioner</summary>

**stroke_prediction: domain practitioner (re-check, 2026-10-20)**
Actor: a primary-care clinician (or the hospital chain's population-health team) who, at a routine visit or a
record review, decides whether to start or intensify stroke prevention (antihypertensive treatment, statin,
anticoagulation for AF, smoking cessation). What I want: the probability of a first stroke within a stated horizon
(5 or 10 years), as QStroke and the Framingham Stroke Risk Profile give it.

**Fit: approximate, at the border of none (USE-8)**
One sentence: the label is "has suffered a stroke" with no date, so it is prevalent stroke at an unknown time
relative to the features, not the first-stroke risk I act on, and the inputs lack the strongest predictors I always
have; it is a stand-in with named gaps, so approximate is the right word, but the gap is wide.

Why not none: the contest framed it as stroke prediction for a hospital chain, the clinical columns look real
(age, sex, hypertension, heart disease, glucose, smoking), and a model trained on prevalent cases ranks risk-factor
burden in a way that correlates with incident risk. The definition names the gap in `fit_reason` (USE-8 lists "a
label without a stated horizon" as approximate; precedent alfa_battle_2_0_task_2). USE-9 offers no rescue: no
well-defined use case predicts an undated past stroke from these columns. "Has this patient had a stroke?" is a
fact I read in the problem list; the only real version would be finding uncoded stroke history (case finding /
phenotyping), and for that I would use diagnosis codes, imaging and medications, none of which are here.
Rephrasing toward it would be the "use case rephrased only to excuse a gap" factor.

**1. Inputs at the prediction point (USE-3, USE-6)**
Have, legitimately: age, sex, hypertension diagnosis, heart disease, smoking status, glucose.

Would not have, or would not be clean:
- Every feature may postdate the stroke (no dates). Hypertension and heart disease are often first coded at the
  stroke work-up; smoking status is often recorded (or changed to "formerly") after the event. This is the reverse
  of my prediction point (USE-3). The BMI case already showed the record is partly written at the stroke admission
  (adjusted OR 3.7 for a missing BMI), so the other fields can share that timing.
- "avg_glucose_level" is undefined: fasting, random, HbA1c-derived? I act on a diabetes diagnosis or HbA1c, not on
  an unexplained average.

Missing that I would always have (ranked by weight in QStroke / Framingham):
1. Atrial fibrillation: the strongest single modifiable stroke predictor; folded into "heart disease" or absent.
2. Systolic blood pressure value and antihypertensive treatment (I have a number, not a 0/1).
3. Diabetes diagnosis, cholesterol/HDL ratio.
4. Prior TIA, chronic kidney disease, family history, ethnicity, deprivation.
5. BMI (dropped here for a correct reason, LEAK-10 via USE-3; I would have it at a routine visit).

Columns I would not use: ever_married, work_type, Residence_type. No risk score uses them, and the curation shows
they carry nothing beyond age (likely generated). Keeping them is harmless to a model but is not a clinical input.

**2. Target (USE-5)**
Proxy. I act on the risk of a first stroke within a horizon, among patients without a prior stroke (QStroke excludes
prior stroke/TIA at baseline). This label mixes the patients who already had a stroke, whom I would not screen at all
(they are on secondary prevention), with everyone else. The resolution I want is a calibrated probability; the
binary label and ROC AUC are fine for ranking, but the prevalence of 1.8% is a lifetime-ever figure in a hospital
population, not a 10-year incidence, so a model's probabilities would not transfer.

**3. Row and split (USE-10, USE-11)**
One row per patient matches one screening decision per patient; IID on random patients matches "new patients of the
same chain" (USE-10, cold start for a new patient; USE-11 not needed). Place and period are unknown, so I cannot say
which population the test stands for. Ages 78-82 being over-full and ages under 2 coded oddly make me doubt the
sample is a clean extract.

**4. Would I use it? (USE-1)**
No. I would use QStroke, the Framingham profile or the Pooled Cohort Equations, which give a dated horizon on
inputs I have. What would make me distrust this model: (a) the label is not "first stroke within N years"; (b) the
features can postdate the outcome; (c) AF and blood pressure values are missing; (d) three columns look synthetic,
which makes me doubt the rest; (e) age alone gets 0.840 and the full model 0.850, so it adds almost nothing beyond
what I see at a glance. What would make me trust one: dated records, exclusion of prior stroke at baseline, incident
stroke within a horizon, AF and SBP values, external validation.

**Gaps between the dataset and the decision, ranked by how much they change the task**
1. Label: prevalent, undated stroke instead of incident stroke within a horizon among stroke-free patients (USE-5,
   USE-8). Changes the task from prediction to retrospective association.
2. Feature timing: comorbidities and smoking may be recorded at or after the stroke (USE-3); bmi already showed it.
3. Missing core inputs: AF, SBP value, treatment, diabetes, cholesterol (USE-1, the checklist item "what is known").
4. Three columns that look generated and are not clinical inputs (data quality; SEL-16 / PROV-3 in the record).
5. Unknown place, period and glucose definition: I cannot say which population the test stands for (USE-1 Method 1).

**What an expert would change**
- Keep fit approximate and keep `fit_reason` as written; it names gap 1 and 4. Add gap 3 to `fit_reason` or the
  prediction-point bullet: "no AF, blood pressure value, diabetes or cholesterol".
- Rewrite `use_case` honestly: "e.g. a hospital chain screens records for high stroke risk; the label is a stroke at
  any time, so the data stand in weakly for that". The current wording is fine but optimistic.
- If the dataset stays, drop ever_married, work_type and Residence_type (not clinical inputs, likely generated).
- On the record's evidence, I agree with the run's recommendation to reject (No + Data Quality Issue): the use case
  is real (USE-12 would protect a real task from a leak), but here the data do not mirror it and are partly
  generated. A real replacement exists in this domain (framingham_heart_study_fhs, incident outcomes with dates).

**Sources**
- `dataset.py` (task_summary, curation_comments), REVIEW.md
- the stroke_prediction record; the panel's claims list and task probe (age 0.831-0.840, linear 0.851)
- `use_case.md` (USE-1, USE-3, USE-5, USE-6, USE-8, USE-9, USE-10, USE-12)
- Hippisley-Cox et al., QStroke, BMJ 2013;346:f2573 (https://www.bmj.com/content/346/bmj.f2573.full): inputs incl.
  AF, SBP, cholesterol ratio, BMI, diabetes; derived on patients without prior stroke/TIA
- Wolf et al., Framingham Stroke Risk Profile, Stroke 1991 (https://pubmed.ncbi.nlm.nih.gov/2003301/): 10-year
  risk from age, SBP, antihypertensive therapy, diabetes, smoking, CVD, AF, LVH
- Liu, Fan, Wu, Artif Intell Med 2019, 101723 (doi:10.1016/j.artmed.2019.101723): the same file used as an
  "incomplete and imbalanced" benchmark, no dated outcome
- Contest page (https://www.analyticsvidhya.com/datahack/contest/mckinsey-analytics-online-hackathon/): problem
  statement not visible without login

</details>

<details><summary>Blind review</summary>

**Blind review: stroke_prediction**
**Verdict: include with changes.** It is a real, if weakly documented, stroke-risk screening table with honest IID evaluation. Before it goes in, the provenance and the cited source must be corrected, and the dropping of `bmi` has to be explained or reversed.

**Task**
This is a screening task. From demographics and comorbidities, it flags patients at risk of stroke so that a clinician or payer can follow up. The use is plausible. The label is "has had a stroke" and comes from a cross-sectional record, so the task is really association and not a forecast of the future.

**Concerns (most to least serious)**
1. **Provenance does not match the cited source.** task.md links the fedesoriano Kaggle dataset. That dataset is about 5,110 rows, with `id` and `bmi`, and smoking recorded as "Unknown". This table has 43,400 rows, 783 positives (1.8%), no `bmi`, and smoking stored as NaN. Those figures match, from memory, the 2018 McKinsey/Analytics Vidhya "Healthcare Analytics" hackathon train set. That hackathon has no public data card and its original origin is unclear; the fedesoriano version only says "confidential source". Fix: cite the actual origin and state its licence. If no verifiable source exists, use the 5k Kaggle version instead.
2. **`bmi` was dropped.** BMI is a standard stroke risk factor and is present in every public version of this data. It is roughly 3% missing in the hackathon data, which can be kept as NaN. Fix: restore it, or document why it was removed.
3. **The task is weak and dominated by age.** LightGBM reaches a 3-fold AUC of 0.846. Age alone with logistic regression reaches 0.840. There is little headroom for comparing methods, and with 783 positives the AUC will be noisy across folds. It is acceptable as an "easy, imbalanced" dataset but should not be counted as a hard one.
4. **Duplicates.** There are 62 rows that repeat exactly, including the target, and 124 rows involved in duplicated feature vectors. This is minor (0.3%), but some copies will fall across train and test. Fix: keep the duplicates but document them, or deduplicate.
5. **Preparation is fine.** The categorical columns are typed as category. Smoking is missing in 31% of rows, structurally so for children (mean age 29 among the missing vs 48 among the rest), and it is correctly left as NaN. `gender` has 11 rows of "Other". Ages below 2 come in 0.08 steps, which look like a months-based encoding; this is plausible. I found no leaking column.

**What I could not check**
- The real collection origin, the time period and the label definition. The Kaggle page gives none of these.
- Whether the values are synthetic. The distributions look natural, but this cannot be verified from the data.
- That this table is the hackathon file. I matched it on row count and positive count from memory only; no public page confirmed it.

</details>

<details><summary>Precedent check</summary>

**stroke_prediction: precedents**
Precedent check for the review panel (re-check), 2026-10-20. I read `principles.md`, `provenance.md` (PROV-1/3/8/9, Methods, Cases), SEL-3/7/16, LEAK-10/38 and the Mechanisms table, TP-4, EV-3/6, and the run's register of probe flags. The register raises no flag that names stroke_prediction. The two flags nearby (`one_feature` opposite outcomes, drift on scaling over all rows) don't touch its issues. I also read the sibling records and the earlier REVIEW.md and the verification checklist. Nothing in this run sets a verdict, and the curator has not decided any of the six issues. They are AI drafts, so this checks them against past decisions.

**Issue 1: partly generated or altered, recommend `No` + `AHDS` / `Data Quality Issue`**
**Verdict: departs with a stated reason, but the reason rests on a standard that is still open.** It is not unreasonable under the ranking: PROV-3 and SEL-16 are Musts.

- **Decided PROV-3 retirements** (Cases table in `provenance.md`):
  - customer_satisfaction_in_airline (Lennart, 2026-10-01): traced through the chain of uploads, with 14,659 labels flipped by a rule.
  - ecommerce_shipping (Lennart, 2026-10-01): columns follow the row counter.
  - homeq_default_prediction: label-free distance AUC 0.92.
  - video_game_fps_prediction (Lennart, 2026-09-29): a deterministic target.
  - churn (Lennart, 2026-10-06, the churn record): MLC++ itself calls the data "artificial", and pure rules predict the label. It is retired as AHDS but is missing from the PROV-3 Cases table.
  - Every one had a generator, a source statement, or marks that predict the label.
- **Stroke has none of these.** Its marks are calibrated against BRFSS (test 4, marginals too even; test 6, structure the world would show) but are not linked to the label. The checklist reports label-free distance 0.690 against 0.826 and no generated-probe flag.
- **The citation is not like for like.** Issue 1 cites "churn and customer_satisfaction_in_airline were retired", but both had more evidence than stroke. The like cases are credit_card_customers (open, `datasets/_dev/tabarena-v0pt2/credit_card_customers/REVIEW.md` issue 1) and hepatitis_c_egypt (AI recommendation 2026-10-07, the hepatitis_c_egypt record). Its marks are stronger: no column depends on another, and the label can't be predicted.
- **The open item binds stroke.** the cross-dataset REVIEW.md, "PROV-3 evidence standard", names stroke_prediction explicitly:
  - Option (a), enough calibrated marks from two tests: stroke goes `No`.
  - Option (b), the marks must predict the label: stroke likely stays.
  - Issue 1 should defer to that item and not imply the precedents already decide it.
- **The "Analytics Vidhya siblings are held at 2nd tier" claim is imprecise.**
  - Held at `TBD -> 2nd Tier` (all screening calls by Lennart, from the June 2026 import, no PROV-3 tests run): insurance (with an `AHDS` marker), loan_predication, black_friday, cross_sell_insurances, banking_marketing_leads_conversion_data. That last one is the McKinsey Analytics Online Hackathon II, the closest sibling, with Lennart's note: "Data looks real enough ... But other dataset from this source is very likely fake."
  - Not held there: loan_prediction_problem_dataset is `No`, lt_vehicle_loan_default_prediction is `TBD -> Yes`, and hr_analytics is `Yes` and shipped in v0.2 (AV first appearance traced, AI 2026-10-14).
  - So the siblings are mixed and none of them was measured. Stroke is the first Analytics Vidhya file with measured marks.
- **The fallback "if kept: add `2ndTierData`" conflicts with the open tag item.** The open item in the root `REVIEW.md` (Tags, from the credit_card_customers review, 2026-10-20) says a tag cannot stand in for a Must: a dataset is retired or shipped with its doubts written down. The "2nd Tier" of the siblings is a `suggestion` value, not this `data_tags` tag. That makes it an AI proposal, not a precedent, so there is no prompt here. Note it in the issue.
- **Where the two cases differ, if kept.** On the remedy ladder ("fix in the definition when it can be"), dropping the three columns matches no PROV-3 precedent. Airline also had a real part (distances) and was retired whole, but its labels were touched. Stroke's label and clinical columns look real (male x heart disease OR 2.28 against BRFSS 1.87). However, the glucose floor at 55 and the over-full ages 78-82 sit in columns that would be kept. Dropping the three columns therefore does not clear PROV-3, and the issue should say so.
- **Drift: none.** The screening line "use it for now and filter later" predates the 2026-10-01/06 retirements. The precedence rule makes a screening verdict provisional until the dataset is probed.

**Issue 2: the contest's full training file instead of the Kaggle cut**
**Verdict: consistent.**
- PROV-8 (Must): the source is the first publication, here the 2018 hackathon.
- hr_analytics (AI 2026-10-14, accepted `Yes`) shipped the AV first appearance over the Kaggle copy.
- The tension "a better version against our own fix" (eryhemato): a version the source defines wins.
- Record work this implies, all consistent with PROV-8/9 and with the D9 fixes in diabetes_3:
  - `year` 2021 → 2018 (PROV-9).
  - `source_links` should name the contest and Mendeley doi:10.17632/x8ygrw87jw.1 (PROV-8).
  - The `Missing source information` marker no longer fits a traced source (PROV-1 holds) if the dataset is kept.
- The Kaggle uploader's "educational purposes" note is a licence term. It is never a reason for a verdict (Lennart, 2026-09-23, selection.md).

**Issue 3: bmi dropped because a missing BMI follows the stroke**
**Verdict: departs without a written reason from the closest precedent.**
- **The rule supports the drop.** LEAK-10 (Must) puts "missingness that encodes the outcome" out, and the tension "a real task against a leak" says fix the leak and keep the task. In mic, the missingness was fixed by moving the prediction point, which isn't possible here.
- **The closest precedent was decided the other way.**
  - kick (CC Lennart, 2026-10-01, the kick record): a missing `WheelType` is "likely blanked when a car is kicked back" (24.9% of bad buys against 1.5% of good cars). It was **kept** with a "Potential leak, kept on purpose" note because "the company released the data this way for the competition".
  - It became a Case of LEAK-38 (Should, narrows LEAK-10), with homesite as the other Case.
  - Stroke is also competition data, with a named field, a post-outcome missingness, and the "keep" alternative written as an option (+0.014 AUC).
- **Facts that may set stroke apart** (none written in the definition):
  - The mechanism is measured with an adjusted model and holds in every age band (OR 3.69, 2.95-4.12 by band). LEAK-38's rationale covers an *unverified* signal.
  - The values add nothing beyond the missingness.
  - The host was a consultancy hackathon whose data owner is confidential, not "a company ... for its own competition".
  - The cost is small: 0.014 against kick's 0.066.
- Smoking missingness (OR 0.96) was rightly kept.

**Consistency check (AI, 2026-10-20):** your call on stroke_prediction (drop `bmi`, missingness that follows the stroke, LEAK-10) differs from kick (kept, CC 2026-10-01, the same mechanism: a named field blanked after the outcome, in competition data, kept with a note under LEAK-38). What sets stroke_prediction apart?
(a) the mechanism is measured, not suspected (adjusted OR 3.69 in every age band), the BMI values add nothing beyond the missingness, and the data owner did not release it for its own competition, so LEAK-38 does not reach it; record this as a Case of LEAK-10; (b) treat stroke like kick: keep `bmi` with a "Potential leak, kept on purpose" note; (c) reopen kick to match; (d) amend LEAK-38 to say when a measured missingness leak in competition data is dropped.

**Issue 4: age dominates, not `Trivial`**
**Verdict: consistent.**
- TP-4 (Must): `Trivial` needs the raw feature to match or beat the methods fold by fold.
- sepsis_survival_minimal_clinical_records was kept on 2026-10-06 (age 0.704 below the best on every fold). fitness_club, the opposite outcome in the register, was retired because the raw feature beat all 37 configurations.
- Stroke: the strong models beat age on 9 of 9 splits.
- Caveat: the checklist's probe line reads "age alone 0.831, 5 of 9 splits", which seems to be against the untuned probe models (LightGBM 0.829). Reconcile that count with the 9 of 9 in the issue before citing sepsis.

**Issue 5: cross-sectional label, "documented ... (as cdc_diabetes_health_indicators does)"**
**Verdict: departs without a reason, and it is not reasonable under the ranking as written.**
- cdc_diabetes_health_indicators was **retired**: CC Lennart 2026-10-15, `No`, `No Good Target / Scientific Discovery`. The reason: "the label is 'ever told you have diabetes', a diagnosis the respondent already has ... no decision is made with that prediction". This became **SEL-7 (Must, narrows SEL-3; P2)**.
- Stroke's definition asks "Has a patient had a stroke?", with the label "at a time not stated, before or after the record". That is the same "has had it" label.
- The bmi finding (issue 3) is itself evidence that records were written after the stroke.
- The screening use case ("screens ... for a high stroke risk, to offer prevention") needs future strokes, as the cdc CC said of screening. The checklist already marks it as loose (USE-1/USE-8).
- SEL-7 is P2, above PROV-3 (P5). If it applies, it decides before issue 1. Under "the summary leads with the highest-ranked issue", it would also come first.
- Possible distinguishing facts: hospital records instead of a self-report interview (SEL-7 says "respondent ... same interview"), and the contest framed it as "predict whether a patient will get a stroke".

**Consistency check (AI, 2026-10-20):** the draft keeps stroke_prediction's cross-sectional "has had a stroke" label with a note, citing cdc_diabetes_health_indicators as precedent. But cdc was retired (2026-10-15, SEL-7, the same mechanism: a known past diagnosis predicted from a record of the same time, no decision made with it). What sets stroke_prediction apart?
(a) the label comes from a hospital record, not a respondent's interview, and the contest framed it as a prediction of stroke, so SEL-7's wording does not reach it; record this as an exception to SEL-3, naming the higher principle it serves; (b) treat stroke like cdc: `No` + `No Good Target / Scientific Discovery` (this would settle the dataset before issue 1); (c) reopen cdc to match; (d) amend SEL-7 to cover or exclude clinical records.

**Issue 6: anomalies kept as published**
**Verdict: consistent with P7** (keep with a note when a fix is not cheap and safe; tension "a real task against imperfect cleaning", churn_telco_south_asia).
- Cross-link: the ages folded in at 78-82 and the glucose floor are possible PROV-3 marks, not only cleaning anomalies. If the folding is the owner's privacy top-coding, it falls under the open item "Amend PROV-3 for an owner's disclosure control" (framingham_heart_study_fhs, root `REVIEW.md`).

**Third exceptions and drift**
- No third exception of one kind: LEAK-38 has two Cases, and PROV-3, a Must, allows no exceptions.
- No drift by Lennart on PROV-3, SEL-7 or LEAK-10 in the register.
- Uniqueness: no other record ships the McKinsey stroke file or the fedesoriano Kaggle cut. The searches by Kaggle slug, Mendeley DOI, hackathon name and "stroke" found only banking_marketing_leads_conversion_data (a different hackathon) and stroke_risk_prediction_dataset_based_on_symptoms (`No`, AHDS, a generated file by its own card).

**Files**
- `REVIEW.md` (issues 1, 3, 5)
- `dataset.py` (task_summary, Prediction point, Leak bullets)
- the stroke_prediction record (year, source_links, marker)
- the cdc_diabetes_health_indicators record (CC 2026-10-15)
- the kick record (CC 2026-10-01, WheelType)
- the churn record (CC 2026-10-06)
- the banking_marketing_leads_conversion_data record
- the hr_analytics record
- the hepatitis_c_egypt record
- the cross-dataset REVIEW.md (PROV-3 evidence standard; 2ndTierData; disclosure control)
- `selection.md` (SEL-7)
- `leak_checks.md` (LEAK-10, LEAK-38)

</details>

<details><summary>Advocate</summary>

**Advocate: stroke_prediction**
Evidence: the panel's reports and `dataset.py`.

**1. The source is traced, and we ship the version the source defines (PROV-1, PROV-8 Must; PROV-13)**
- **Claim:** this is the contest's own training file, not an anonymous re-upload.
- **Evidence:**
  - The S3 copy, the Mendeley copy (doi:10.17632/x8ygrw87jw.1, the data of Liu et al., AIM 2019) and the warehouse copy have the same sha256 (claim audit #11, #17).
  - The Kaggle file is exactly the first 249 strokes and the first 4,861 non-strokes of this file. That is 5,110 ids in the same order with 0 value mismatches (#12).
  - Using the contest file gives 8.5 times the rows, and 261 strokes per test fold instead of 83.
  - Precedent: hr_analytics shipped the Analytics Vidhya first appearance over the Kaggle copy.
- **Objection answered:** the blind reviewer asked to "cite the actual origin, or use the 5k Kaggle version". The origin is now cited.
- **Why it wins:** the tension "a better version against our own fix" says a version the source defines replaces any other (P5). The Kaggle uploader's "educational use" note is a licence term and never a reason for a verdict (selection.md, Lennart 2026-09-23).
- **Concession:** the record is stale. `year` should be 2018, not 2021 (PROV-9). `source_links` should name the contest and the DOI. The `Missing source information` marker no longer fits. These are fixes to the record, not to the dataset.

**2. The one measured leak is fixed by the mildest remedy (LEAK-10 Must, USE-12 Must)**
- **Claim:** dropping `bmi` is correct, and the task survives the drop.
- **Evidence:**
  - With every column fixed, a stroke multiplies the odds of a missing BMI by 3.68 (2.98-4.54). A spline for age gives 3.66; adding the id raises it to 4.10 (claim audit #28).
  - The effect appears in every age band (#40).
  - The BMI values add nothing beyond the missingness: 0.8505 without the column, 0.848 with missing values drawn at random (#30).
  - Smoking missingness is not linked to the outcome (OR 0.91, 0.76-1.10), so smoking stays.
  - No other shipped column has outcome-driven missingness. Exact copies across the split are 0.2%, all non-strokes.
- **Objections answered:**
  - The kick precedent (LEAK-38, keep with a note): LEAK-38 is a Should that narrows LEAK-10. It covers "unverified" signals in data "a company released for its own competition". Here the signal is measured in every band, and the data owner is a confidential hospital chain, not the host. So LEAK-38 does not reach this case, and LEAK-10, a Must, applies. This is option (a) of the precedent check: record stroke_prediction as a Case of LEAK-10.
  - The blind reviewer's "restore bmi": a measurement on the data outranks a reading (EV-1, EV-2).
- **Why it wins:** the tension "a real task against a leak" says to fix the leak and keep the task. Dropping one column is the mildest fix on the remedy ladder.
- **Concession (finding N1):** among non-strokes, missing BMI falls with the id. The "stroke admission" reason is therefore a hypothesis. Write "one possible reason" and add the id fact. A recording drift in routine records next to strokes that stay undocumented fits that hypothesis. N1 sits on the dropped column, and no shipped column has a class-specific id trend (all |rho| < 0.07).

**3. The split mirrors the application (SPLIT-1, SPLIT-19, SPLIT-29; all hold)**
- **Evidence:**
  - Each patient appears once (the id is unique), and the use case is a new patient, so cold start fits.
  - The contest's test file takes 29-31% of every id decile, so the contest itself split patients at random. The shipped IID 3x3 split follows it.
  - The hidden-group probe finds 0 candidates. 1-NN agreement is 0.965, which is chance.
  - The stroke share is flat along the id. An id-ordered split moves the score with test-set composition (0.836 or 0.869), but the margin over age stays at 0.008-0.013 (split audit).
- **Why it wins:** the split auditor's verdict is "right with notes". At most, the IID bullet gets one sentence on the id-order drift. Under SPLIT-4 and SPLIT-30, the size of a gap never decides a split; the context does.

**4. PROV-3 does not decide this dataset as the rule stands (PROV-3, SEL-16 Must; EV-3 Must; EV-6 Should)**
- **Conceded fact:** the data has measured marks.
  - Residence_type, ever_married and work_type carry nothing beyond age (likelihood-ratio p 0.39-0.88), where NHANES shows a strong dependence (p 3e-52).
  - Women and men aged 25-29 are married alike (45.0% / 45.0%).
  - Glucose has a floor at 55 and a spike at 65.
- **Claim:** these marks do not reach the bar set by any past PROV-3 retirement.
  - Every past retirement had a generator, a source statement, or label-linked marks: airline (14,659 labels flipped by a rule), ecommerce_shipping (columns follow the id modulo k), homeq (distance AUC 0.92), churn ("artificial" by its source).
  - Stroke has none of these. Label-free distance is 0.690 against 0.826. The generated-data probes raise no flag. The glucose spike is not linked to the class (binomial p 0.45). The three columns are independent of stroke given age (p 0.43).
  - The label and the clinical columns are real. Male x heart disease gives an age-adjusted OR of 2.28 (BRFSS: 1.87). Hypertension (p 3e-85) and heart disease (p 1e-120) depend on the other columns as real data would.
  - The precedent check finds that the "churn and airline" citation is not like for like.
- **The rule that wins:** the root REVIEW.md item "PROV-3 evidence standard" names stroke_prediction and leaves the bar open:
  - option (a): calibrated marks from two tests are enough;
  - option (b): the marks must predict the label.
  - Until the curator decides, EV-6 makes this a "maybe" for the curator. A retirement now would decide an amendment by the back door.
- **Mildest remedy if the curator picks (a):** fix the definition by dropping the three columns. They change nothing: 0.8505 against 0.8501, per split -0.002 to +0.002. Retiring comes only if the remaining marks are judged enough. The age folding at 78-82 may be the owner's top-coding, which is the open "disclosure control" item.
- **Concession:** dropping the three columns does not clear the glucose floor or the age folding, as the precedent check says. A `2ndTierData` tag cannot stand in for a Must, so that fallback in the earlier REVIEW.md should go.

**5. SEL-7 does not reach a clinical-record label from a contest framed as prediction (SEL-7 Must; USE-8 Must; "P3 informs P2")**
- **Threat:** this is the highest-ranked threat to the dataset (P2), so it is answered before PROV-3.
- **Claim:** SEL-7 is worded for "a label the respondent already knows, asked in the same interview". Its one case, cdc_diabetes_health_indicators, was told a diagnosis a median of 10 years earlier, with the undiagnosed among the negatives.
- **Evidence:**
  - Here the label comes from a hospital chain's records.
  - The contest asked to "predict the probability of stroke happening to their patients ... proactive health measures" (claim audit #2).
  - No shipped feature shows a measured post-stroke trace. Former vs never smoker gives OR 1.04 (0.85-1.27). Hypertension 1.38 and heart disease 1.83 are plausible risk-factor sizes, not inflated ones (column audit).
  - USE-8 lists "a label without a stated horizon" as an approximate fit (case alfa_battle_2_0_task_2). The practitioner rates the fit approximate, not none.
  - Principles: "P3 informs P2 ... let the use case decide" (breast_cancer_prediction).
- **Why it wins:** this is option (a) of the precedent check's consistency question. It is a distinguishing fact plus the rule text. It is not a silent departure.
- **Concession:**
  - The practitioner would not use the model, and calls the fit "at the border of none".
  - The precedent check's own option (a) records it as an exception to SEL-3, a Must, and a Must allows no exceptions. So if the curator keeps it, option (d), amending SEL-7 to cover or exclude clinical records, is the cleaner route.
  - If the curator reads SEL-7 broadly, it decides before PROV-3, and no fix in the definition exists, because there are no dates to re-target on.
  - This is a weighing call for the curator, not a settled point.

**6. Worth benchmarking: not trivial, and every fold can be scored (TP-4 Must; TP-9)**
- **Evidence:**
  - Regularised LightGBM scores 0.8505 against 0.8404 for age alone, and beats age on 9 of 9 splits (mean +0.0101; claim audit #37).
  - The smallest test fold has 261 strokes.
  - Precedent: sepsis_survival was kept with age below the best on every fold. fitness_club was retired only because the raw feature beat every configuration.
- **Concession:** the checklist's "5 of 9" compares age with an untuned probe model (0.829). TP-4 asks about the strong methods. Say this in the issue.
- **Why it wins:** under the tension "the right split against the score", a small real signal is no reason to retire a dataset (P6 is value, ranked below validity).

**7. What remains is wording and notes, not validity (USE-8, P7, writing.md)**
- **The gaps are already disclosed:** `fit="approximate"` and `fit_reason` name the undated label, the possible timing of the features, and the generated-looking columns.
- **The anomalies are kept with notes:** the ages under 2 in steps of 0.08 and the folded ages at 78-82. Tension: "a real task against imperfect cleaning" (churn_telco_south_asia).
- **Fixes that keep the dataset:**
  - (i) Change use_case to the contest's own wording: probability of a stroke, for proactive care. The label records a stroke the patient has had.
  - (ii) Cite NHANES (n 35,850, married p 3e-52; 50.7% / 38.0% at ages 25-29) next to BRFSS, since the BRFSS file is gone.
  - (iii) Write "one possible reason" for the BMI mechanism, plus the id fact.
  - (iv) Add to fit_reason: no atrial fibrillation, blood pressure value, diabetes or cholesterol; the glucose averaging window is not stated.
  - (v) Optionally add one IID sentence on the id-order drift.
  - (vi) Fix the record's year, link and marker.
- **Why they are enough:** no claim that bears on validity is refuted (claim audit: 47 hold, 2 refuted on wording or record only). Independent failures are not conflicts, but none of these is a failure of a Must. Each is a documentation fix.

**Judgment record (advocate's view)**
```text
Verdict: ship after changes (wording and record only), pending two open curator calls.
Validity: SEL-1 holds; SEL-7 not reached by its wording (clinical record, contest framed as prediction; curator call, amend SEL-7 if needed); USE-8 approximate, disclosed; LEAK-10 triggered, fixed (bmi dropped; Case of LEAK-10, LEAK-38 does not reach); SPLIT-1/19/29 hold; PROV-1/PROV-8 hold; PROV-3 open under the root "PROV-3 evidence standard" item (no label-linked mark; if (a), drop the three columns first).
Value: TP-4 not Trivial (9 of 9 above age, +0.010); 261 strokes per fold.
Quality: anomalies kept with notes (P7).
For the curator: the SEL-7 reading for a clinical "has had" label; the PROV-3 evidence standard (a) or (b).
```

</details>

<details><summary>Critic</summary>

**stroke_prediction: critic, opening brief (2026-10-20)**
Position: **do not ship.** Point 1 is a P2 Must that changes to the definition cannot fix. If the curator finds a fact
that sets this case apart from cdc, ship only after the changes in points 2 to 6.
Evidence is this panel's reports (claim_audit, column_audit, split_audit, practitioner, precedents, blind_review,
probes) and `dataset.py`.

**1. The label is a known past diagnosis, and no one makes a decision with it (SEL-7, Must; SEL-3, Must; P2)**
- Problem: the target is "has had a stroke" at an unstated time. The data dictionary says "1 - suffered stroke". The
  definition's own `predicted` says "before or after the record". This is the same kind of label as
  cdc_diabetes_health_indicators, which Lennart retired on 2026-10-15 as `No Good Target / Scientific Discovery`: "a
  diagnosis the respondent already has ... no decision is made with that prediction". That decision is the case
  behind SEL-7.
- Effect on the task: the screening use case in `use_case` needs future first strokes. The positives here are
  patients already on secondary prevention, whom a clinician would not screen (practitioner, gap 1: "changes the task
  from prediction to retrospective association"). The prevalence of 1.8% is an ever-had figure, not an incidence.
  USE-9 offers no rescue either: finding uncoded stroke history needs codes, imaging and medications, and none are
  here (practitioner).
- The data show that some records postdate the stroke. A missing BMI follows the stroke (adjusted OR 3.68, 2.98-4.54,
  claim audit #28). Among strokes the share of missing BMI stays flat along the id while it falls among other
  patients (N1).
- Distinguishing facts that are claimed: this is a hospital record, not an interview, and the contest framed the task
  as risk prediction (precedents, issue 5). Neither changes the mechanism SEL-7 names: the positives already know.
  SEL-7 is a rule (P2), and the PROV-3 question (P5) ranks below it. "A summary leads with the highest-ranked issue",
  yet the current REVIEW.md lists this point fifth and cites cdc as support. The precedent checker shows it points the
  other way.
- Remedy: none in the definition, because there are no dates to re-target with. `No` + `No Good Target / Scientific
  Discovery`. Otherwise the curator records the distinguishing fact as an exception to SEL-3 (option (a) in
  precedents, issue 5).

**2. The features may be recorded after the outcome (USE-3, Must; LEAK-10, Must; P4)**
- Problem: no column is dated. Hypertension, heart disease and the average glucose (its window is not stated) may be
  coded at the stroke work-up. BMI shows that some records were written then (point 1).
- Effect: a model can learn post-stroke documentation and not risk. This cannot be measured. The adjusted ORs
  (hypertension 1.38, heart disease 1.83) look plausible, and the one testable trace, quitting smoking, is absent (OR
  1.04; column audit). So this is a risk that cannot be tested, not a proven leak.
- Rule: USE-8 "approximate" covers "a label without a stated horizon". It does not cover features that may postdate
  the outcome, and the tension table says a real task "does not carry a leak".
- Remedy, if kept: write in `fit_reason` and in the prediction-point bullet that the missing-BMI pattern shows part of
  the records were made at the stroke admission, and that the glucose window is not stated.

**3. Partly generated data is shipped knowingly (PROV-3, Must; SEL-16, Must; P5)**
- Problem: `ever_married`, `work_type` and `Residence_type` carry nothing beyond age, not even on each other (LR p
  0.19-0.97). The claim audit finds this "holds harder than written". Real NHANES adults show the dependence (p 3e-52).
  Women and men are married alike at 45.0/45.0 at ages 25-29, where NHANES gives 50.7/38.0. Columns the definition
  keeps also carry marks: glucose has a hard floor at 55.00 and a doubled bin at 65, and ages 78-82 are over-full.
- Effect: `fit_reason` itself says three columns "look generated", and the dataset ships them anyway. The marks in the
  kept columns mean that dropping the three does not clear PROV-3 (precedents, issue 1).
- Limits I concede: no mark predicts the label (label-free distance AUC 0.690 against 0.826, no generated-probe flag).
  The root REVIEW.md item "PROV-3 evidence standard" names this dataset and is open.
- Remedy: decide this dataset in the same pass as that item. Under option (a): `No` + `AHDS` / `Data Quality Issue`.
  Under option (b), fix the definition at the least. Drop the three columns (no AUC cost: 0.8505 against 0.8501) in
  place of "kept as published", and note the glucose and age marks. `2ndTierData` is no substitute for a Must (root
  REVIEW.md, Tags item).

**4. The bmi drop departs from kick without a written reason (LEAK-10, Must, against LEAK-38, Should; P4)**
- Problem: the drop is right on LEAK-10. The measured OR holds in every age band, the values add nothing beyond the
  missingness, and N1 makes it stronger. But kick kept a field blanked after the outcome in the same way, under
  LEAK-38, and the definition does not say what sets stroke apart.
- Remedy (a note): record the distinguishing facts. BMI is a named field, not an anonymised one. The host was not the
  data owner running its own competition. The leak is measured, not suspected. Record stroke as a Case of LEAK-10.
  Reword claim 29 ("likely reason: admission") to "one possible reason" and add the N1 id fact.

**5. Little value beyond age (TP-1, TP-2, Weigh; P6)**
- Evidence: age alone scores 0.840 and regularised LightGBM 0.850, a margin of 0.010 (9 of 9 splits). In the task
  probe, the single feature (0.831) beats the untuned LightGBM (0.829), and only the linear model is clearly above it
  (0.851). Three of the nine features are noise (point 3).
- This is not `Trivial` (TP-4 holds) and not a reason to exclude. It is a factor against the borderline keep, and it
  adds to points 1 and 3.
- Remedy: reconcile the checklist's "5 of 9" with the "9 of 9" in the `Note:` bullet.

**6. Wording and record repairs (USE-2, PROV-9, EV-3; procedure)**
- `use_case`: "the contest asked whether a patient has had a stroke" is refuted (claim audit #2). The contest asked
  for "the probability of stroke happening", for proactive care. Write that, together with the fact that the label
  records a past stroke. The mismatch is itself the point-1 gap.
- The record's `year` is 2021 and its `source_links` point to the Kaggle cut. Change them to 2018, the contest and the
  Mendeley DOI (claim audit #43, PROV-8/9).
- The BRFSS 2015 figures (53.8/40.3) cannot be checked, because the file is gone. Cite the NHANES calibration or
  restore the subset (EV-3).

Judgment record (critic's draft):
Verdict: do not ship (SEL-7); if a distinguishing fact is recorded, ship only after the changes in points 2-6.
Validity: SEL-7/SEL-3 triggered, no fix in the definition; USE-3/LEAK-10 risk that cannot be tested (note); PROV-3
triggered, waiting on the open evidence standard (drop the three columns at the least); LEAK-10 bmi fixed, exception
to kick not written.
Value: TP-2, a margin of 0.010 over age (weighed against).
Weighed: real clinical columns +, contest provenance traced +, generated columns -, no horizon -, AF/SBP absent -.

</details>

<details><summary>Advocate rebuttal</summary>

**Advocate rebuttal: stroke_prediction**
**Critic 1: SEL-7 / SEL-3, a known past diagnosis**
**Partly conceded.**

What I concede:
- The label is prevalent, not incident. The practitioner's gap 1 stands.
- SEL-7 ranks highest (P2). REVIEW.md must lead with it, and it must drop the cdc citation as support: cdc was retired, so it points the other way.
- If the curator reads SEL-7 as "any past diagnosis in the record", the dataset goes `No` + `No Good Target / Scientific Discovery`. No fix in the definition exists.

What I dispute:
- **That the rule as written decides it.** SEL-7 says "a label the respondent already knows, asked in the same interview as the features". Its one case had the diagnosis given a median of 10 years before, with undiagnosed people among the negatives. Here:
  - (i) The label is a clinical record of a hospital chain, not a self-report.
  - (ii) The contest asked for "the probability of stroke happening ... proactive health measures" (claim audit #2).
  - (iii) No elapsed time is measured. USE-8, a Must, names "a label without a stated horizon" as an approximate fit (alfa_battle_2_0_task_2).
  - (iv) Principles say "P3 informs P2 ... let the use case decide" (breast_cancer_prediction).
- **That the BMI pattern proves the records postdate the stroke.** N1 cuts the other way too. The claim auditor rates the admission reason "untested (ambiguous)". A record made at the admission would also be contemporaneous with the stroke, not written ten years later as in cdc.
- **The critic's fallback is not available.** The critic offers "an exception to SEL-3". SEL-3 is a Must, and principles.md says "A Must has no exceptions ... anything else is an amendment". So if the curator keeps the dataset, the route is option (d): amend SEL-7 to cover or exclude clinical-record labels, with this case. Otherwise it is option (b): retire.
- This is a weighing call that goes to the curator, not a settled `No`.

**Critic 2: features may postdate the outcome (USE-3, LEAK-10)**
**Conceded as a note. Disputed as a leak.**

What I dispute:
- The critic concedes the risk "cannot be measured". The traces we can measure are clean:
  - former vs never smoker OR 1.04 (0.85-1.27);
  - hypertension 1.38 and heart disease 1.83, plausible risk-factor sizes (column audit).
- EV-6 makes an untested suspicion a "maybe", not a triggered Must. The tension line "a real task does not carry a leak" is about a leak that has been shown. LEAK-10 was triggered once here, by `bmi`, and was fixed.

What I accept, with one correction:
- Add the note to `fit_reason` and to the prediction-point bullet, together with the unstated glucose window.
- Word it "may have been made at the stroke admission", not "shows". N1 leaves that reading open (claim audit, claim 29).

**Critic 3: partly generated data (PROV-3, SEL-16)**
**Mostly conceded.**

What I concede:
- The three columns should be dropped and not "kept as published". `fit_reason` itself calls them generated-looking, a P5 Must is at stake, and the fix costs nothing (0.8505 against 0.8501, per split within plus or minus 0.002). On the remedy ladder this is the mildest remedy, and I withdraw "ship as defined" on this one line.
- `2ndTierData` is no substitute for a Must.
- The decision belongs in the same pass as the open "PROV-3 evidence standard" item.

What I dispute:
- **That option (a) means retiring automatically.** The remedy ladder puts "fix the definition" before "exclude". The marks left in kept columns are weaker than the ones that justify dropping:
  - The glucose floor at 55 and the spike at 65 are not class-linked (spike ratio 1.69 in class No against 1.52 in class Yes, p 0.45). A floor like this fits an export or lab lower limit as well as a generator.
  - The folding at ages 78-82 may be the owner's top-coding. That falls under the open item "Amend PROV-3 for an owner's disclosure control" (framingham_heart_study_fhs).
- Under (a), the curator should judge whether these residual marks alone reach the bar. They are not the three columns' marks.

**Critic 4: the bmi drop departs from kick without a written reason**
**Conceded.** The same facts appear in my point 2:
- the field is named, not anonymised;
- the host is not the data owner;
- the leak is measured, not suspected.

Record stroke_prediction as a Case of LEAK-10. Reword claim 29 to "one possible reason" and add the N1 id fact.

**Critic 5: little value beyond age (TP-1, TP-2, Weigh)**
**Conceded as a factor. Disputed as a comparison.**
- The "0.831 beats LightGBM 0.829" figure uses the untuned probe model. EV-3 says probe numbers "are not leaderboard numbers".
- TP-4 is about strong methods, and those beat age on 9 of 9 splits (+0.010).
- A Weigh factor cannot decide on its own, and the tension "the right split against the score" says a small real signal is no reason to retire.
- I agree that the 5-of-9 and 9-of-9 counts should be reconciled in the notes.

**Critic 6: wording and record repairs**
**Conceded in full.** These match my point 7:
- the contest's own wording in `use_case`;
- the record's `year` set to 2018, with the contest link and the Mendeley DOI;
- NHANES cited for the BRFSS figures, or the BRFSS subset restored.

**Revised judgment record (advocate)**
```text
Verdict: ship after changes, if the curator does not read SEL-7 to cover clinical "has had" labels.
Validity: SEL-7 curator call (keep needs amendment (d), not an exception; else No + No Good Target / Scientific
Discovery); USE-3 untestable, noted (smoking OR 1.04); LEAK-10 bmi fixed, Case recorded vs kick (LEAK-38 does not reach);
SPLIT-1/19/29 hold; PROV-1/8 hold; PROV-3: drop ever_married, work_type, Residence_type now; residual glucose/age marks
decided with the open evidence-standard and disclosure-control items.
Value: TP-4 not Trivial (9 of 9, +0.010); weighed -.
Quality: anomalies noted (P7); wording and record fixes per critic 6.
For the curator: SEL-7 scope (b or d); PROV-3 standard (a or b) for the residual marks.
```

</details>

<details><summary>Critic rebuttal</summary>

**stroke_prediction: critic, rebuttal (2026-10-20)**
I keep my position: **do not ship under the rules as they stand.** If the curator amends SEL-7 to exclude clinical
records, ship only after the changes below.

**Conceded**
- **Advocate 1 (source traced, PROV-1/PROV-8):** conceded in full. The contest file is the right version, and the
  record fixes (year 2018, contest link, Mendeley DOI, drop `Missing source information`) are repairs.
- **Advocate 2 (bmi as a Case of LEAK-10, LEAK-38 does not reach):** conceded. This was my point 4. The remedy is the
  same: write the distinguishing facts and the N1 wording into the definition.
- **Advocate 3 (split):** conceded. I raised no split point. The id-drift sentence is optional.
- **Advocate 6 (not Trivial, TP-4):** conceded. My point 5 already said it is a factor, not a reason.

**Disputed**
**Advocate 5: SEL-7 "not reached by its wording" (SEL-7 Must, P2)**
- **The two distinguishing facts are not new.**
  - "The contest framed it as prediction": the cdc sources framed theirs the same way. The CC quotes Xie et al.,
    "initial population screening for type 2 diabetes", and Teboul. Lennart retired it anyway, because the label is a
    diagnosis already held and "no decision is made with that prediction" (cdc record, CC 2026-10-15). The framing
    was in front of him and did not decide.
  - "A hospital record, not an interview": the CC's reason does not depend on how the label was recorded. It depends
    on the positives already having the outcome.
  - Here the data show that the record often comes at or after the stroke. Missing BMI has an adjusted OR of 3.68 in
    every band, and among strokes it stays flat along the id (N1). The advocate's "no post-stroke trace in shipped
    features" is true, but it is no defence, because the trace sits on the record's timing, not on a column.
- **The advocate concedes the governing points.**
  - A Must takes no exception, so option (a) of the precedent check is not open.
  - The clean route to keep the dataset is amending SEL-7 (option (d)).
  - The practitioner puts the fit "at the border of none".
  - Until an amendment is made, the rule as written and its one case apply (principles: "treat like cases alike"; a
    precedent with the same facts is followed unless a fact sets the new case apart).
- **USE-8 "label without a stated horizon" (alfa_battle):** this covers a future label with an unstated window. It
  does not cover a label that may lie before the features. That case is the subject of SEL-7, which narrows SEL-3 and
  ranks P2, above USE-8 (P3).
- **"P3 informs P2" (breast_cancer_prediction):** that tension lets the use case decide whether a scope pattern
  applies. Here the use case (screening for future strokes) is exactly what this label cannot serve (practitioner, gap
  1). It cuts against the advocate.
- **Rule that wins:** SEL-7 (Must, P2). The verdict is `No` + `No Good Target / Scientific Discovery`, unless the
  curator amends SEL-7. That amendment is the curator's call. It cannot be settled by an approximate fit.

**Advocate 4: PROV-3 remedy under option (a)**
- I agree the item is open and binds this dataset (EV-6), and I make no back-door retirement.
- I dispute the advocate's remedy for option (a). Option (a) says the calibrated marks "are enough" to retire. The
  advocate concedes that dropping the three columns leaves the glucose floor and the age folding, both in kept
  columns. So under (a) the verdict is `No` + `AHDS` / `Data Quality Issue`. Dropping the columns is the remedy under
  (b), where the marks do not decide.
- Either way, the definition should stop shipping the columns its own `fit_reason` calls generated. "Kept as
  published" is not the mildest remedy that resolves a PROV-3 finding; dropping them costs nothing (0.8505 against
  0.8501).

**Advocate 7: "none of these is a failure of a Must; the gaps are disclosed"**
- Disclosure cures neither of these:
  - SEL-7 (above).
  - The feature-timing risk (USE-3/LEAK-10, my point 2). `fit_reason` says "some facts may be recorded after it" but
    not that the BMI pattern shows part of the records were written at the stroke. The tension "a real task against
    a leak" says a real task "does not carry a leak".
- I accept the advocate's fixes (i) to (vi) as needed in any case. Add to them:
  - the BMI-timing sentence in `fit_reason`;
  - dropping the three columns;
  - moving the SEL-7 issue to the top of REVIEW.md (P2 leads).

**Net**
- Agreed: source, bmi drop, split, value and all the wording and record repairs.
- Open for the curator, in rank order:
  1. SEL-7: either apply it as written (`No`) or amend it.
  2. The PROV-3 standard: under (a) `No`; under (b) drop the three columns.

</details>
