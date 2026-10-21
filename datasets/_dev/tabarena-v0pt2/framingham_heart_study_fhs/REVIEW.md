# framingham_heart_study_fhs

**Outcome:** added. A binary task on the baseline exam (about 1956) of the NHLBI BioLINCC Framingham teaching
dataset: a first coronary heart disease (CHD) event within 10 years, IID, with the label rebuilt from the event
columns because MIT's `TenYearCHD` (the file of the Kaggle uploads) counts 265 deaths and losses among its 644
positives. The AI recommends shipping it after changes, which are made. Validity: USE-1, USE-5, USE-8 (direct, era
named), USE-11 (first exam), LEAK-1 and SPLIT-1 hold; LEAK-22 has no case for a competing death after the
prediction point (issue 2); PROV-13 applied (label repaired from the origin); PROV-3 and
PROV-14 were amended on 2026-10-21 and now answer issues 3 and 7 (kept, a repair under this record). Value: TP holds (logistic regression
ROC AUC 0.739, age alone 0.640, 126 positives per test fold). Quality: CLEAN-12 departure for `education` (issue 8).
Weighed: source +, use case + (the classic FHS risk score), label repair +, anonymisation -, era and no HDL -. Left for
you: the endpoint (issue 1), competing deaths (issue 2), then
`education` and the options (issues 8, 9, 10).

**Main points:** Choose the endpoint (any CHD or hard CHD); confirm competing deaths as No. The anonymised
teaching data (issue 3) and the record (issue 7) are settled by the amended PROV-3 and PROV-14.

**Record fields that disagree with the definition:**

- `year`: record `2013`, definition `2004`.

**Record judgment:** valid with concerns. All three Kaggle uploads are MIT's cut of the BioLINCC teaching dataset,
and its label is wrong for 41% of the positives, so the definition reads the teaching data. The record's `year` 2013
has no evidence (likely the course year of a copy); 2004 is the creation date of the teaching file (documentation
p. 8), its first release date is not stated.

**Issues for Lennart:**

1. **Endpoint: any CHD (ANYCHD, implemented) or hard CHD (MI_FCHD)?**
   - Problem: the label is a first CHD event within 3,652 days of the baseline exam. ANYCHD counts angina pectoris
     (chest pain), coronary insufficiency, myocardial infarction (heart attack) and death from CHD; hard CHD counts
     only hospitalised heart attack and CHD death.
   - Effect on the task: 188 of the 379 positives are angina or coronary insufficiency. A physician today treats on
     thresholds of hard CHD (ATP III) or hard cardiovascular disease, so ANYCHD ranks a softer outcome than the one
     acted on; hard CHD halves the positives and makes the scores noisier.
   - Evidence: both are outcomes of FHS risk functions. The FHS "Coronary Heart Disease (10-year risk)" page
     (https://www.framinghamheartstudy.org/fhs-risk-functions/coronary-heart-disease-10-year-risk/, based on Wilson
     et al. 1998): "Outcome Coronary Heart Disease", "*Hard CHD events exclude angina pectoris". The "Hard Coronary
     Heart Disease (10-year risk)" page, which the record links, has "myocardial infarction or coronary death". The
     Wilson paper itself was not read.
   - Implemented: ANYCHD, 379 Yes (9.0%), 126 per test fold; logistic regression ROC AUC 0.739.
   - Alternative: MI_FCHD, 191 Yes (about 64 per test fold); logistic regression ROC AUC 0.785, against 0.739 for
     ANYCHD on the same 3 x 3 stratified folds.
   - Rule: USE-5 (P3, Must); both endpoints satisfy it. P6 slightly favours ANYCHD (more positives). Precedent:
     cirrhosis_patient_survival_prediction took the endpoint of the clinical score its actor uses (2026-10-14); both
     candidates here are such scores.
   - Recommendation: ANYCHD, the outcome of the classic FHS 10-year CHD score, with twice the positives.
   - Decision: ANYCHD or MI_FCHD.

2. **Participants who died of other causes within 10 years: No (implemented) or dropped?**
   - Problem: 251 participants died without CHD within 10 years. Death is a competing event: once it happens, CHD
     cannot.
   - Effect on the task: as No, the label is the risk a patient actually faces of a CHD event within 10 years.
     Dropping them selects the cohort on an event after the prediction point and removes high-risk negatives (mean
     age 54.8, systolic BP 143.5, close to the CHD cases); logistic regression then rises from 0.739 to 0.751 (3 x 3
     stratified folds; the advocate's run gives 0.738 to 0.752) only because these hard negatives go.
   - Evidence: all 251 were followed for CHD up to their death (TIMECHD is not before TIMEDTH in any of them), so
     their label is known.
   - Implemented: No; 4,224 rows, 379 Yes.
   - Alternative: drop them, as the censoring of the FHS risk functions does in a Cox model: 3,973 rows, 379 Yes.
   - Rule: LEAK-22 (Must, follow the paper's cohort) has cases only for rows ruled out at the prediction point; this
     is the first decision on a competing event after it. Precedents: cirrhosis_patient_survival_prediction and
     mortgage dropped only the rows lost to follow-up, as here (16 dropped).
   - Recommendation: confirm No (advocate, critic and practitioner agree). Your answer then becomes a case of
     LEAK-22.
   - Decision: No, or drop them.

3. **Anonymised teaching data: keep it under a recorded PROV-3 case?** Answered by the rule: PROV-3 was amended
   (Lennart, 2026-10-21) so that values the owner perturbed for privacy, with no measurable damage, are kept with a
   note of what was checked; this dataset is its case. Your note asked for a selection-bias note too, now in the
   record and the definition (last bullet below).
   - Problem: the data is the teaching version of the Framingham cohort, not the research data. BioLINCC: "teaching
     datasets are completely unsuitable for publication purposes since specific statistical measures were used to
     create anonymous versions" (https://biolincc.nhlbi.nih.gov/teaching/). Which measures is not documented; Nahhas,
     *Introduction to Regression Methods for Public Health Using R*, App. A.6
     (https://www.bookdown.org/rwnahhas/RMPH/appendix-biolincc.html), names "permutations and/or random visit
     selection": swapping values between participants, or picking at random which exam a participant contributes.
     PROV-3 (P5, Must) excludes a real table whose values someone replaced.
   - Effect on the task: if values were swapped between participants, the link between risk factors and CHD is
     weaker or altered, and methods are compared on that altered data. It is no leak: no prediction gets better than
     in practice; the attainable score may be lower.
   - Evidence: no noise was added, since digit preference is intact (systolic BP ends in 0 for 22.5% of readings
     against 2-4% for an odd digit; noise would even it out). Within a person, BMI and systolic BP six years apart
     correlate at r 0.90 and 0.71, which swapping across people at one exam would weaken. Ages match the exam days in
     every later exam; the per-sex baseline means, minima and maxima equal the documentation's tables; the
     generated-data probe finds nothing. Swapping a small share of values, or visit selection, cannot be tested.
   - Implemented: kept; `fit_reason` and the Anomaly bullet say what was checked and what cannot be, and the notes
     give the reason for use despite the terms ("to compare learning methods, not to estimate clinical effects", as
     breast_cancer_prediction, Lennart 2026-10-15). No tag: `Anonymized` means masked names or values, which these
     are not, and `2ndTierData` is defined in no knowledge file.
   - Alternative: `No` with `Data Quality Issue`, as every PROV-3 case so far (customer_satisfaction_in_airline,
     ecommerce_shipping, homeq_default_prediction, video_game_fps_prediction). Each of those was retired on a test
     that fired; here none fires. Cost: the canonical CHD-risk task leaves, and there is no better origin (the
     research data needs a BioLINCC application and cannot be redistributed).
   - Panel: the advocate holds PROV-3 is not triggered, as no test fires; the critic holds the owner's statement
     triggers it and an untested method is not refuted. The mediator: neither is proven, no precedent covers an
     owner's disclosure control on a real cohort, so it needs your recorded decision.
   - Recommendation: keep it, recorded as a PROV-3 case: "owner's disclosure control on a real cohort, no
     measurable damage: kept with a note".
   - Selection (added 2026-10-21): the teaching file is "a subset of the data collected as part of the Framingham
     study" on 4,434 participants (documentation 2021a, p. 1), of the 5,209 enrolled in 1948; the 2005 NHLBI page
     says "a large subset of the original Framingham cohort participants". How the 4,434 were chosen is not
     documented. Period 1 is about 1956, some eight years after enrolment, so people who died or left before that
     exam are likely missing, and Nahhas names "random visit selection". The task stands for this subset, not for
     the whole cohort; no test can measure the selection.
   - Decision: settled by the amended PROV-3 (kept, with the notes); nothing left to decide unless you want `No`.

7. **Rebuilt label under the release's record: a repair (PROV-13) or a new dataset (PROV-14)?** Answered by the
   rule: PROV-14 was amended (Lennart, 2026-10-21): a repair (same units, same features, damaged values restored from
   the origin) stays under its record; only a rebuild from other sources gets a new one. This is a repair, kept here.
   - Problem: PROV-14 (P5, Must) said a rebuild that does not match the release exactly is a new dataset with its
     own record. The shipped table differs from MIT's release: 16 rows fewer and 249 labels turned from Yes to No.
   - Effect on the task: none. It decides under which record and name the task ships.
   - Evidence: the same participants with the same 15 feature values row for row (`_mit_rows` asserts a one-to-one
     match on 4,240 rows); only the damaged label is restored from the origin's own event columns, as PROV-13 (Must)
     requires. Precedents: SUPPORT2 (2_month_survival_rate_prediction) and cirrhosis_patient_survival_prediction were
     repaired in place; corporate_credit_rating became corporate_issuer_credit_rating (Lennart, 2026-10-16), new data
     from new sources.
   - Implemented: kept under this record.
   - Alternative: retire this record and open a new one for the rebuilt task. Cost: record bookkeeping only; what
     ships is the same.
   - Recommendation: record it as a PROV-13 repair, as SUPPORT2 and cirrhosis (advocate and critic agree).
   - Decision: settled by the amended PROV-14 (kept under this record); it is now one of the rule's cases.

8. **`education`: keep the numeric code 1-4, or map it to its labels?**
   - Problem: `education` is a 4-level code (1 = 0-11 years, 2 = high school or GED, 3 = some college or vocational
     school, 4 = college degree or more), stored as a number. CLEAN-12 (P7, Should) asks to turn ordinal codes into
     labelled categories.
   - Effect on the task: small. A numeric code keeps the order for every model; labels make the meaning visible and
     let a model treat the levels as categories.
   - Implemented: numeric, as breast_cancer_prediction keeps its density 1-4 (the order is the meaning); the note's
     reason "as it is ordered" becomes "bins of years of schooling" if the exception is recorded. Precedents
     the other way: ljubljana_primary_tumor, credit_g and coil_2000 mapped their codes to labels.
   - Alternative: map to the four labels as an ordered category. Cost: none beyond a line of code.
   - Recommendation: keep it numeric as a recorded exception to CLEAN-12 (the levels are bins of years of schooling);
     the second of its kind, so a third would call for an amendment.
   - Decision: exception (numeric), or map to labels.

9. **One row per participant, or every CHD-free exam grouped by participant?**
   - The teaching data has two later exams (about 6 and 12 years on) with 10 years of follow-up left:
     10,759 CHD-free exam rows (1,229 Yes) against 4,224, then split grouped by participant. On the same baseline
     test rows, logistic regression rises from 0.736 to 0.745 and HistGradientBoosting from 0.691 to 0.720. The use
     case says "a patient's first assessment", so one row per participant matches it (USE-11, as
     breast_cancer_prediction); the later exams are also older and selected survivors.
   - Implemented: one row per participant (neither the advocate nor the critic asks for the variant).
   - Recommendation: keep one row per participant.
   - Decision: keep, or add every exam with a split grouped by participant.

10. **`roc_auc` or `log_loss`?**
   - The physician treats above a risk threshold, so `log_loss` (scores calibrated probabilities) would mirror the
     decision more closely than `roc_auc` (scores the ranking only), the practitioner says; no brief argued it.
   - Implemented: `roc_auc`, the default for a binary task.
   - Recommendation: keep `roc_auc`.
   - Decision: `roc_auc` or `log_loss`.

**Review panel:** ship after changes (mediator; full panel). Claim audit: about 50 claims; 2 refuted (the row's "period
not stated", fixed; the record's `year` 2013, a field row), the Kaggle copies untested. Blind review: include with
changes; it found the label rebuild on its own (249 MIT positives No here, 16 dropped). Agreed by advocate and critic:
the rebuilt label, the 16 lost dropped, competing deaths as No, the IID split with one row per participant, fit
`direct` with the era named, and the text fixes (applied: first exam, about 1956, no HDL, the anonymisation stated as
measured, the terms sentence, relatives cannot be identified, cigsPerDay heaping). Settled by the mediator: the
endpoint's reason is the FHS 10-year CHD page, not MIT's course (applied). To the curator: the mediator's issues 1-6
are this file's 3, 7, 1, 2, 8, and 9 and 10; the critic's points 1, 4, 5, 6 are issues 1, 3, 7, 8.

<details><summary>Mediator</summary>

**Recommendation**

```text
Verdict: ship after changes.
Validity: SEL-1 holds (terms noted, as breast_cancer_prediction); USE-1 holds once the row states the period
  (about 1956); USE-5 holds (MIT's label repaired; ANYCHD is the outcome of the FHS 10-year CHD function, see change 6);
  USE-8 direct holds once the era is named (2_month precedent); USE-11 holds with "first exam" wording; LEAK-1 holds
  (15 baseline features, follow-up dropped); SPLIT-1 holds (IID, one row per participant); PROV-13 applied (label
  rebuilt from the origin's event columns); PROV-3 not shown to fire, needs the curator's case (issue 1); PROV-14
  wording triggered, needs the curator's call (issue 2).
Value: TP holds: LR ROC AUC 0.739, age alone 0.640, 126 positives per test fold (keep).
Quality: CLEAN-12 departure (education numeric), exception or mapping (issue 5); cigsPerDay heaping noted.
Weighed: source + (origin, sha-checked), use case + (canonical), label repair +, anonymisation -, era/no HDL -.
For the curator: issues 1-2 Must decisions on the record (both sides propose the same remedy); issue 3 a weighing
  call (endpoint); issues 4-6 confirmations.
```

**Changes to make now (no decision needed)**

All are text in `dataset.py` or the record; rows, features, label and split stay.

1. `task_summary.row`: replace "period not stated" with "the baseline exam, about 1956 (three exams roughly
   1956-1968, documentation 2021a p. 1)", and say "first exam". Rule: USE-1 (period), writing.md; claim 3 refuted.
2. `use_case`: "at a patient's first assessment" instead of "a routine exam". Rule: USE-11 (Must); breast_cancer
   precedent. Both sides concede.
3. `fit_reason`: name the era (before statins, 3.4% on BP medication) and replace "values may be slightly perturbed"
   with "no added noise (digit preference intact); permutation or visit selection cannot be checked". Rule: USE-8
   (2_month_survival_rate_prediction names its era), EV-6 ("slightly" is not measured).
4. Anomaly bullet: same rewording ("a perturbation, if any, is small" becomes the measured statement: digit preference,
   within-person r 0.90/0.71, ages match exam days). Rule: EV-6.
5. `known` or a bullet: HDL was measured only at the third exam, so it is missing though every current risk score uses
   it. Rule: USE-1 (gap named); practitioner gap 1.
6. Endpoint reason: drop "the CHD of MIT's task". Rule: PROV-15/EV-4 case (2026-10-15). Replace with the FHS page
   https://www.framinghamheartstudy.org/fhs-risk-functions/coronary-heart-disease-10-year-risk/ (read today):
   "Coronary Heart Disease (10-year risk). Based on Wilson PW ... Circulation. 1998 ... Outcome Coronary Heart
   Disease ... Population of interest Individuals 30 to 74 years old and without overt CHD at the baseline
   examination", footnote "*Hard CHD events exclude angina pectoris". Cite the page, not the paper (PROV-16: Wilson
   1998 is not read). Add this page to the record's `source_links`.
7. Note bullet: "the teaching data has no family identifiers, so spouses and relatives cannot be identified" instead of
   "the hidden-group probe finds no hidden group" as the reason. Rule: SPLIT-29, EV-6.
8. Terms: add "We use it to compare learning methods, not to estimate clinical effects." Rule: SEL-1/PROV-2,
   breast_cancer_prediction (Lennart 2026-10-15).
9. Cleaning bullet: "cigsPerDay heaps at 9 and 43, almost only at period 1; their coding is undocumented". Rule:
   CLEAN-1 (documented). Both sides accept.
10. Record: put the BioLINCC teaching page and documentation 2021a first in `source_links`, the Kaggle uploads after;
    `year` 2004 with the note "teaching file created 2004-03-02 (documentation p. 8); first release date not stated"
    in the definition. Rule: PROV-9 direction (airfoil, nikuradse 2026-10-20), PROV-8. 2013 has no evidence; both
    sides accept 2004 with that note.

**Issues for the curator, ranked**

1. **Anonymised teaching data under PROV-3 (P5, Must).**
   - Problem: BioLINCC says "specific statistical measures were used to create anonymous versions"; Nahhas names
     "permutations and/or random visit selection". PROV-3 excludes a real table with "values replaced".
   - Effect: if values were permuted across people, methods are compared on altered associations.
   - Advocate: no PROV-3 test fires; digit preference intact (no additive noise); within-person r 0.90/0.71 six years
     apart; ages match exam days in every exam; every PROV-3 case so far was retired on a test that fired (EV-1, EV-2).
   - Critic: the method the owner names was never tested; untested is not refuted; the owner's statement is the
     trigger.
   - Mediator: the measurements bound the alteration (additive noise ruled out, wholesale permutation unlikely), but a
     small permutation cannot be tested, so neither "fired" nor "refuted" is proven (EV-6). No precedent covers owner
     disclosure control on a real cohort, so this is new ground under a Must and needs your recorded decision before it
     ships. Both sides propose the same remedy. No better origin exists (the research data cannot be redistributed).
   - Decision: (a) record a PROV-3 case "owner's disclosure control on a real cohort, no measurable damage: kept with a
     note"; (d) amend PROV-3 to the same effect; or (b) `No` / `Data Quality Issue`. Recommended: (a), (d) if you
     expect more such datasets. Tags: `Anonymized` does not fit its definition (names and values keep their meaning);
     `2ndTierData` is defined in no knowledge file, so neither follows from a rule.
2. **Rebuilt label under the release's record (P5, PROV-14 Must).**
   - Problem: the shipped table differs from MIT's release (16 rows fewer, 249 labels flipped); PROV-14 says such a
     rebuild is a new dataset with its own record.
   - Not a conflict with PROV-13: repairing and opening a new record are compatible, so PROV-14 has to hold on its own.
     The precedents contradict its wording: SUPPORT2 and cirrhosis were repaired in place, corporate credit got a new
     record. A precedent that contradicts a rule is flagged, not followed.
   - Both sides: same 4,240 participants, same 15 feature values row for row (`_mit_rows` asserts it), only the
     damaged label restored from the origin's own columns; record it as a PROV-13 repair (a) or amend PROV-14 (d).
   - Decision: (a), (d), or (b) a new record. Recommended: (d), so the rule stops contradicting three cases.
3. **Endpoint: ANYCHD or hard CHD (P3, USE-5 Must; a weighing call between two valid labels).**
   - Effect: 188 of 379 positives are angina or coronary insufficiency, not MI or CHD death.
   - Fact settled here: both endpoints are FHS risk-function outcomes. The FHS "Coronary Heart Disease (10-year risk)"
     page (Wilson 1998) has outcome CHD with angina ("Hard CHD events exclude angina pectoris"); the "Hard Coronary
     Heart Disease (10-year risk)" page (ATP III 2001) has "myocardial infarction or coronary death". So the critic's
     condition (a source for ANYCHD from the actor's tools) is met by the FHS page; the paper itself remains unread.
   - Advocate: ANYCHD is the source's documented CHD and the total-CHD score; 379 Yes, 126 per test fold.
   - Critic: treatment guidelines act on hard CHD (ATP III), the page the record links; 191 Yes, about 64 per fold
     (LR 0.741-0.749 per REVIEW_before).
   - Decision: which endpoint. Settles it: whether the benchmark mirrors the classic Framingham score (ANYCHD) or
     today's treatment threshold (MI_FCHD). Both satisfy USE-5; P6 slightly favours ANYCHD.
4. **Competing deaths are No (P4, LEAK-22).** Both sides and the practitioner agree (cumulative-incidence risk;
   dropping 251 hard negatives lifts LR 0.737 to 0.752 by selection). First post-prediction competing-event decision:
   confirm, and it becomes a Cases row of LEAK-22 (or a Tensions row).
5. **`education` 1-4 numeric (P7, CLEAN-12 Should).** Second instance after breast_cancer density. Advocate: record an
   exception (bins of years of schooling, order is the meaning). Critic: mapping to labels is cheap and safe; either is
   fine. Decision: exception (a third would call for an amendment) or map to labelled categories.
6. **Options, not defects.** (i) A variant with every CHD-free exam grouped by RANDID (10,759 rows; LR 0.736 to
   0.745, HGB 0.691 to 0.720 on the same test rows); neither side asks for it (USE-11). (ii) The practitioner's
   `log_loss` for a threshold-on-risk decision; neither brief argued it. (iii) REVIEW_before issues 5-6 (raw-data
   route, SelectArena copy with MIT's label and the wrong domain) stand as written.

**Agreed facts**

- MIT/Kaggle `TenYearCHD` = TIMECHD < 3,652 in 4,240/4,240 rows; 265 of 644 positives had no CHD (249 died, 16
  lost). Blind reviewer found the same crosstab independently.
- Rebuilt label: ANYCHD within 3,652 days; no date on days 3,648-3,654; 4,224 rows, 379 Yes (9.0%); 251 competing
  deaths No, all CHD-observed up to death; 16 lost dropped.
- All 15 features are as of the baseline exam; follow-up columns, HDLC/LDLC (period 3 only), constants and RANDID
  dropped; no leak (missing indicators <= 0.512, best single feature age 0.640, 0 duplicate feature vectors).
- Split IID 3 x 3, 126-127 positives per test fold; no drift over RANDID; relatives cannot be identified.
- Signal: LR 0.739, HGB about 0.71, LightGBM 0.677; linear beats boosting.
- Raw file: CRAN rda identical in three versions, matches the documentation's tables.
- Exams ran roughly 1956-1968 (doc p. 1); BP medication 3.4% at baseline; HDL only at period 3.
- Anonymisation: additive noise refuted (digit preference); permutation and visit selection untestable.
- Fit `direct` (practitioner, both sides) once the era is named.

**Consistency with precedent**

Follows the precedent checker. Consistent: teaching data over the Kaggle file (SUPPORT2, cirrhosis), competing deaths
No and lost dropped (cirrhosis, mortgage), terms noted (breast_cancer_prediction), IID one row per person
(breast_cancer_prediction), fit direct with era named (2_month_survival_rate_prediction), year from the origin
(airfoil, nikuradse). Departures, each sent to the curator: PROV-3 (all cases `No`; set apart by no test firing and
the owner's own disclosure control; issue 1); PROV-14 wording against SUPPORT2/cirrhosis (issue 2); endpoint reason
against cirrhosis and the PROV-15 case (fixed by change 6, outcome in issue 3); `education` against
ljubljana/credit_g/coil_2000 (issue 5).

</details>

<details><summary>Claim audit</summary>

**Table**

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 1 | Question: first coronary event within 10 y for a person without CHD | D task_summary | cohort PREVCHD at p1 | holds | 4,240 cohort rows all PREVCHD = PREVAP = PREVMI = 0 | USE-1 |
| 2 | Use case: physician at a routine exam, prevention | D | reading | holds (wording) | "for example" used; actor, moment, decision named | USE-1 |
| 3 | Row: ... "period not stated" | D task_summary.row | read documentation p. 1 | **refuted** | Doc 2021a p. 1: "Participant clinic data was collected during three examination periods, approximately 6 years apart, from roughly 1956 to 1968"; baseline = period 1, so about 1956 | writing.md ("only facts from ... the source"), USE-8 |
| 4 | 9.0% have a first CHD event (ANYCHD components) | D | count; doc p. 4 ANYCHD definition | holds | 379/4,224 = 8.97%; ANYCHD = AP, MI, CI, fatal CHD (doc p. 4) | USE-5 |
| 5 | Known: the 15 risk factors | D | are flags baseline-only or ever-during-follow-up? pivot by period | holds | DIABETES 0->1 between p1 and p3 for 196, PREVSTRK 59, PREVHYP 1,061, never 1->0: values are as of the exam. Per-sex p1 means/min/max/N equal doc p. 10-12 exactly | USE-3, LEAK-1 |
| 6 | Split: random participants | D, README | load via dataset_io (rebuilt), check splits | holds | 3 repeats x 3 folds; test positives 126/126/127 per fold; no train/test index overlap | SPLIT-1 |
| 7 | 265 of 644 MIT positives had no CHD event within 10 y | D changes | match MIT to teaching, crosstab | holds | 644 positives; 379 CHD, 249 died, 16 lost | USE-5, PROV-13 |
| 8 | 16 lost participants dropped | D changes | count | holds | 16 rows, all DEATH = 0 with TIMEDTH = 8766 (vital status known, CHD follow-up ended 754-3,647 d) | USE-5 |
| 9-10 | fit direct; everything measured at the exam, fixed 10 y | D | see 5, 12 | holds on timing; **contested** on "direct" | Timing and label horizon hold. fit_reason itself names a gap (anonymised values) and the cohort is 1956 (BPMEDS 3.4% in the cohort, before statins), while the use case is today's prevention decision | USE-8, USE-9 (weigh) |
| 11 | values "may be slightly perturbed" | D fit_reason | digit preference (additive noise would erase it) | partly holds, rest untested | SYSBP x2 ends in 0 for 22.5% vs ~2-4% for odd digits; HEARTRTE last digit 0/5: 29.7%/26.8%; TOTCHOL 0: 17.8%, 5: 14.2%; CIGPDAY heaps at 20/30/15/10; all integers or .5 steps. No additive noise. Permutation or visit selection (Nahhas) cannot be tested; "slightly" stays inference | EV-6, PROV-3 |
| 12 | No date of the cohort on days 3,648-3,654; cut-off irrelevant | D TEN_YEARS | list TIMECHD/TIMEDTH/TIMEMIFC/TIMEAP/TIMEMI in 3,640-3,660; recount labels for cut-offs 3,647-3,655 | holds | dates present: ...3,647, then 3,655; CHD 379 and died 251 for every cut-off 3,647-3,654; 3,655 gives died 252 | |
| 13 | Features renamed as in MIT's cut | D | merge on the 15 names | holds | 4,240/4,240 matched one-to-one, same row order as teaching cohort | |
| 14 | Dropped-column reasons | D | unique values in cohort; HDLC/LDLC non-null by period | holds | PERIOD {1}, TIME {0}, PREV* {0}; HDLC non-null 0/0/3,027 by period, LDLC 0/0/3,026 | LEAK-10 |
| 15 | TIMECHD = event day or censor date; doc p. 4 quote | D _outcome | read doc p. 4 | holds | "Censor date may be end of followup, death or last known contact date if subject is lost to followup" (TIMEAP; TIMECHD "Defined as above") | EV-2 |
| 16, 35 | MIT matches one-to-one; no two rows share 15 features | D | duplicated() on cohort and kept rows | holds | 0 duplicates in 4,240 and 4,224 | LEAK-16 |
| 17 | year 2004 | D | doc p. 8 | holds | SAS PROC CONTENTS "Created: 14:50 Tuesday, March 2, 2004" | PROV-8 |
| 18, 48 | BioLINCC quote; riskCommunicator permission, GPL-3 | D license | fetch BioLINCC page; read DESCRIPTION and man/framingham.Rd | holds | page: "teaching datasets are completely unsuitable for publication purposes since specific statistical measures were used to create anonymous versions"; Rd: "provided with permission from the National Heart, Lung, and Blood Institute"; License: GPL-3 in all three versions | EV-4 (note only) |
| 19 | 11,627 x 39; rda identical in 0.1.0/1.0.0/1.0.1 (sha 8fdd578a...); matches doc counts and means | D download_description | download three tarballs, sha256; compare doc tables | holds | all three rda 8fdd578a...; CSV 11,627 x 39 (doc's 38 SAS vars + educ, listed on doc p. 2); SEX 5,022/6,605, BPMEDS 10,090/944, DIABETES 11,097/530 = doc p. 2-3; p1 table = doc p. 10, 12 | PROV-1 |
| 20 | write.csv gives same values; Kaggle shreyjain601 same 453,453 values | D | none (no R, Kaggle needs auth) | untested | | EV-7 |
| 21 | sha256 of both raw files; MIT byte-identical to aasheesh200 | D | sha256 local and fresh OCW download | holds (sha); Kaggle identity untested | both local sha match; OCW today 2c0e57dc... | |
| 22 | bibtex | D | read | holds | NHLBI 2004, Grembi riskCommunicator, Bertsimas OCW | |
| 23 | MIT file has CR line endings | D _load_raw | od -c | holds | `TenYearCHD\r1,39,...` | |
| 24, 40 | 4,434 p1, 194 prevalent CHD, 4,240 cohort, 16 lost, 4,224 kept, 379 Yes | D | count | holds | exactly these numbers; doc p. 12: prevalent CHD 124 + 70 = 194 | |
| 25-26 | prediction point baseline; read teaching data for the label | D | see 5, 7 | holds | | USE-3 |
| 27 | MIT TenYearCHD = TIMECHD < 3,652 exactly; MI_FCHD gives 191 | D | compute | holds | 4,240/4,240 equal; MI_FCHD within 3,652 d = 191 | USE-5 |
| 28 | 251 died without CHD are No; not CHD-censored before death | D | TIMECHD vs TIMEDTH in died group | holds | 0 of 251 have TIMECHD < TIMEDTH, so CHD was observed up to death; label is complete for them | USE-5 |
| 29 | 4,224 remain, 379 Yes | D | count | holds | | |
| 31 | male 1 = SEX 1; ints for age and full flags | D | dtypes of rebuilt frame; doc SEX coding | holds | doc p. 2: 1 = Men; age, flags int64; BPMeds float (61 missing at p1) | CLEAN |
| 32 | no sentinels; ranges match documentation | D | min/max vs doc p. 2-3 | holds | all within doc ranges (e.g. GLUCOSE 40-394 vs 39-478, BMI 15.54-56.8 vs 14.43-56.8); doc says missing = '.' | CLEAN |
| 33 | anonymisation perturbation, if any, small | D | see 11 | partly holds | additive noise refuted by digit preference; permutation/visit selection untestable | EV-6 |
| 34 | 3 CHD censor dates after death, No either way | D | DEATH = 1 & TIMECHD > TIMEDTH | holds | three participants: ANYCHD 0, TIMECHD 8,766, TIMEDTH 4,162/3,460/2,105; the two within 10 y are the 2 MIT-negative "died" rows of the decision table | |
| 36 | IID; no exam dates or family identifiers; no hidden group | D | columns; probe | holds as stated; relatedness untested | TIME is relative only; no family id. FHS original cohort recruited households (spouses); not checkable here | SPLIT-29 to SPLIT-31 |
| 37 | default IID 3 x 3 stratified | D | splits | holds | see 6 | |
| 38 | dataset check 0 warnings | checklist | rerun | holds | "0 error(s), 0 warning(s), 0 info (26 checks run)" | EV-7 |
| 39 | decision table counts | D _decisions | recompute | holds | CHD 379/379 MIT+, TIMECHD 26-3,640; died 251/249, 53-8,766; lost 16/16, 754-3,647; free 3,594/0, >= 3,655 | |
| 41-42 | record year 2013 | R | doc p. 8 | **refuted** | documentation dataset created March 2, 2004; no 2013 event in the trail | PROV-8 (metadata) |
| 43 | all three Kaggle uploads are MIT's file | R | none (Kaggle auth) | untested for christofel04 and shreyjain601 | aasheesh200 equality also not re-downloaded | EV-7 |
| 44-47 | MIT rows = baseline cohort; 249 died + 16 lost; 4,224 / 379 | R | see 7, 13 | holds | | |
| 49-50 | priority, 41% of Kaggle positives wrong | R | 265/644 | holds | 41.1% | |
| implied | target is the real-world target | — | doc p. 4 vs FHS risk functions | holds, with a choice | ANYCHD = "total CHD" of the original FHS 10-year CHD function; the record links the hard-CHD page (MI_FCHD, 191 Yes): a curator call already in REVIEW issue 1 | USE-5 |
| implied | every feature known at the prediction point | — | see 5, 14 | holds | | LEAK-1 |
| implied | no row copied across the split | — | 0 duplicate feature vectors; RANDID unique at p1 | holds | | LEAK-16 |
| implied | the signal is real and modest | — | LR / HGB on shipped splits | holds | LR mean ROC AUC 0.739 (0.717-0.768), HGB depth 3 0.706; matches probe 0.739 | TP |

**Refuted, ranked**

1. **Claim 3, task_summary.row "period not stated" (P3, Must USE-8 / writing.md).** The documentation states the
   exams ran "from roughly 1956 to 1968", so the baseline exam is about 1956. Changes: the row text, and it feeds a
   weighing call on the fit (claim 9): the use case is a physician deciding on blood-pressure or cholesterol treatment
   today, while the cohort is from the 1950s (BP medication 3.4% at baseline, before statins), on anonymised values.
   Mildest remedy: write "at the baseline exam, about 1956 (exams 1956-1968, documentation p. 1)"; name the era in
   fit_reason. Whether the era plus anonymisation makes the fit `approximate` is a curator call (USE-8, USE-9).
2. **Claim 41-42, record `year: 2013` (P5 metadata, PROV-8).** The documentation's SAS dataset was created on March 2,
   2004; nothing in the trail dates 2013. Remedy: set the record's year to 2004 (already listed under "Record fields
   that disagree").

**Contested / untested, ranked**

1. **Fit `direct` (claims 9-11, USE-8, weigh).** Not refuted by a test, but the fit_reason itself names a gap
   (anonymised values) and the era is 1956; USE-8 lists "a stand-in with a known gap" under approximate. Remedy: curator
   call; at least name the era.
2. **Anonymisation size (claims 11, 33; P5, PROV-3, EV-6).** Additive noise is refuted by intact digit preference
   (terminal 0 in BP, 0/5 in heart rate and cholesterol, cigarette heaping): proof against noise. Permutation across
   participants or random visit selection cannot be measured; "slightly" and "small" remain inference. Remedy: write
   "no added noise (digit preference intact); other methods cannot be checked" instead of "slightly perturbed".
3. **Relatedness across the split (claim 36; SPLIT-29 to 31, Should).** The FHS original cohort recruited households;
   spouses may sit in train and test. No identifier exists, so it cannot be checked; a household shares no label-
   carrying entity strongly enough to break IID. Remedy: one clause in the Note bullet ("relatives cannot be
   identified").
4. **Claims 20, 21 (Kaggle identity), 43 (P5, EV-7).** Kaggle copies and the R write.csv route not re-checked (Kaggle
   needs authentication; no R here). They do not change the task; the shipped route (CRAN rda, sha-verified in three
   versions) holds.

</details>

<details><summary>Column audit</summary>

**Column table**

| column | meaning (codebook) | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| male | SEX, 1 = men, 2 = women; mapped to 1/0 | yes; constant per person in all 11,627 rows | int64, 0 missing; mapping matches codebook | fine | CLEAN-14 |
| age | AGE, age at exam (years), 32-81 | yes | int64, 32-70 in cohort, 0 missing; whole years in the source | fine | |
| education | educ, attained education: 1 = 0-11 y, 2 = HS/GED, 3 = some college/vocational, 4 = college degree+ | yes in use (stable adult trait); when FHS asked it is not documented; one value per person across all periods (4,321 of 4,321 with a value) | float64 codes 1-4, 105 missing (2.5%), missing-indicator AUC 0.497 | fine; minor question: ordered code kept numeric, not an ordered category with labels | CLEAN-12, CLEAN-14 (precedent breast_cancer_prediction `birads_breast_density` kept numeric) |
| currentSmoker | CURSMOKE, current cigarette smoking at exam | yes | int64 0/1, 0 missing; 0 contradictions with cigsPerDay | fine | |
| cigsPerDay | CIGPDAY, cigarettes per day; 0 = not current smoker | yes | float64, 29 missing, all current smokers (real unknown amount, not a sentinel); value heaping at 9 (130 rows) and 43 (56 rows), and these values occur almost only at period 1 (43: 57/0/0, 9: 134/10/5 over periods 1/2/3): a period-1 recording convention (likely category codes), same in train and test | fine; note the heaping (unknown code meaning) | CLEAN-10 (not a proxy: no evidence), CLEAN-1 |
| BPMeds | BPMEDS, anti-hypertensive medication at exam | yes ("at exam") | float64 0/1, 53 missing (1.3%), indicator AUC 0.497; all 124 users have prevalentHyp = 1 | fine | |
| prevalentStroke | PREVSTRK, prevalent stroke at exam | yes: all 25 cases have STROKE = 1 with TIMESTRK = 0; absorbing across periods (no 1 -> 0) | int64, 0 missing; single AUC 0.500 | fine | |
| prevalentHyp | PREVHYP: treated, or the second exam with mean SBP >= 140 or DBP >= 90 | yes: PREVHYP = 1 iff TIMEHYP = 0 in the cohort (1,317 / 1,317), so the confirming exam is the baseline or earlier (FHS exams before period 1); 318 rows with high BP but PREVHYP = 0 got HYPERTEN later (median day 844), so the flag is not back-filled from later exams | int64, 0 missing | fine | LEAK-10 checked |
| diabetes | DIABETES: treated, or casual glucose >= 200 mg/dL, at that exam or earlier | yes: absorbing across periods (0 -> 1 only), all 34 with glucose >= 200 flagged; 71 of 109 diabetics have glucose < 200 (treated or earlier exam) | int64, 0 missing | fine | |
| totChol | TOTCHOL, serum total cholesterol mg/dL (107-696) | yes | float64, 49 missing; max 696 within codebook range | fine | CLEAN-11 (unusual, not impossible) |
| sysBP | SYSBP, mean of last two of three readings, mmHg | yes | float64 (half values from the mean), 0 missing, 83.5-295 | fine | |
| diaBP | DIABP, same, mmHg | yes | float64, 0 missing, 48-142.5; sysBP > diaBP in every row | fine | |
| BMI | BMI kg/m^2 | yes | float64, 19 missing, 15.54-56.8 | fine | |
| heartRate | HEARTRTE, ventricular rate, beats/min | yes | float64, 1 missing (the row is a Yes; 1 row, no signal), 44-143 | fine | |
| glucose | GLUCOSE, casual serum glucose mg/dL | yes | float64, 384 missing (9.1%); Yes rate 6.8% missing vs 9.2% present, indicator AUC 0.512: missingness at the exam, not caused by the outcome | fine | LEAK-10 (missingness) checked |
| chd_within_10_years (target) | ANYCHD = 1 and TIMECHD <= 3,652 | built from follow-up | category Yes/No, 379 Yes (9.0%); 16 lost-to-follow-up rows dropped; deaths without CHD = No | fine (endpoint and competing deaths are curator calls already in REVIEW) | LEAK-23, USE-5 |

Dropped columns (24): every one of the 39 source columns is either one of the 15 features or in `DROPPED_COLUMNS`.
Re-checked: RANDID (identifier, CLEAN-3); PERIOD, TIME, PREVCHD, PREVAP, PREVMI constant in the cohort (CLEAN-5);
HDLC, LDLC 100% missing at period 1 (CLEAN-5); DEATH, ANGINA, HOSPMI, MI_FCHD, ANYCHD, STROKE, CVD, HYPERTEN and the
eight TIME* columns are follow-up over 24 years, "added without regard for ... when examination data was collected"
(codebook p. 1): all post-prediction, correctly dropped (LEAK-10). No later-period measurement enters a row.

**Problems, ranked (principles.md)**

No P4 leak and no P7 cleaning error found. Probes agree: all features AUC 0.658, best single `age` 0.640, missing
indicators <= 0.512, 0% exact copies.

1. P5 (PROV-3, SEL-16), not a column defect, carried from REVIEW_before issue 3: every value is from BioLINCC's
   anonymised teaching copy ("specific methods were employed to ensure an anonymous dataset", codebook p. 1). Column
   level checks found nothing inconsistent: prevalent flags are absorbing across periods and agree with the event
   columns (PREVCHD = 1 iff ANYCHD with TIMECHD = 0 at period 1, 194/194; PREVHYP iff TIMEHYP = 0; PREVSTRK all
   TIMESTRK = 0), ages rise 4-8 years between periods. Remedy: already noted in the Anomaly bullet; the 2ndTierData tag
   stays the curator's call.
2. P7 (CLEAN-1, CLEAN-10), weak, question: `cigsPerDay` heaps at 9 and 43, almost only at period 1, so it looks like
   a coded category of the period-1 questionnaire (e.g., an open top class) and not a count. No sentinel evidence,
   same in train and test, and 43 has the expected high CHD rate (14.3%). Remedy: none needed; at most a one-line note
   in the cleaning bullet ("43 and 9 appear almost only at period 1; their coding is undocumented").
3. P7 (CLEAN-12, CLEAN-14), Should, question: `education` is an ordered 4-level code kept as float 1-4, not an
   ordered category with its codebook labels. Defensible (precedent breast_cancer_prediction keeps an ordered code
   numeric; the bullet states the reason). Remedy: keep with the existing note.
4. Procedure: `education`'s collection time is not documented (one value per person across all periods). An adult's
   attained education is known at the exam in practice, so no leak; no action.

</details>

<details><summary>Split audit</summary>

**Verdict: right with notes.** IID, 3 repeats x 3 stratified folds, one row per participant (the baseline exam of
4,224 CHD-free participants).

**Regime against the use case**

* Use case: a physician, at a routine exam, estimates a CHD-free patient's 10-year risk. The patient is a new entity:
  no earlier outcome of theirs is used and none would exist at a first exam (USE-10 cold start). With one row per
  participant at their first exam, USE-11 makes it IID without grouping. Declared IID: matches.
* Not temporal: TIME = 0 for every row; the teaching data has no calendar dates (original cohort enrolled 1948-1953,
  one enrolment wave). The label is a fixed 10-year window, complete for every kept row (the 16 lost-to-follow-up
  dropped), so there are no training rows with an unknown label (SPLIT-9 not engaged). Row order as time (SPLIT-22):
  the file is sorted by RANDID, and RANDID quintiles show no drift (CHD rate 0.098 / 0.078 / 0.083 / 0.096 / 0.093,
  mean age 49.3-49.7), so there is no hidden enrolment order to keep.
* Not grouped: one row per RANDID, so a grouped split by participant is the same as the shipped one.

**Split mechanics (measured)**

* 9 folds: train 2,816 / test 1,408 each, 126-127 positives per test fold, no train/test overlap.
* 0 duplicate feature vectors among 4,224; 0 duplicates even with glucose and heart rate removed (13 columns).
  Hidden-group probe: 4 candidates, no hits (top totChol gap -0.008); near copies 0.0% at 0.85 / 0.9.

**Notes, ranked (all P4 unless stated; none is a defect of the shipped split)**

1. **USE-11 (Must), P3/P4: the use case says "a routine exam", the rows are only the first exam.** USE-11: "take one
   row per entity only when the use case is that row: it loses rows and signal." The teaching data has two later
   exams (periods 2 and 3, about 6 and 12 years on) with 10 years of follow-up left: 10,759 CHD-free exam rows with a
   known 10-year status (1,229 Yes) against 4,224 (379 Yes). Quick fit, 3 seeds x 3 stratified folds on the shipped
   baseline test rows, training on the baseline rows only vs all exams of the training participants (no test
   participant in train): logistic regression ROC AUC 0.736 -> 0.745, HistGradientBoosting 0.691 -> 0.720. The baseline
   design is defensible (it is the documentation's population at risk, MIT's task, and keeps the cohort free of the
   "random visit selection" Nahhas names for the anonymisation). Mildest remedy: none needed for the split; either
   sharpen `use_case`/`row` to "the first exam" (wording), or, as the curator's option, a variant with every CHD-free
   exam grouped by RANDID (2.5x the rows; then the split must be grouped by participant, SPLIT-24, true id RANDID).
2. **SPLIT-25 / SPLIT-29 (Must): relatives cannot be checked.** The original cohort sampled households, so spouses
   (and some relatives) are in the data; the teaching file has no household or family id. Rule fires only when the
   shared entity carries the label strongly; spouses share little CHD risk, the probe finds no hidden group, and near
   copies are 0.0%. No remedy; say "cannot verify" rather than "no hidden group" in the Note bullet, which the
   checklist already does.
3. **Era shift, P3 rather than P4 (USE fit): the test set is the same 1948-1953 cohort.** A physician today predicts
   for patients of another era (treatment, smoking rates, cholesterol levels). No calendar time in the data, so no
   temporal split is possible (SPLIT-8 does not apply: the task is not temporal in nature, one enrolment wave). This is
   a fit caveat; `fit_reason` could name it beside the anonymisation. No split remedy.

**Checks with nothing to report**

* Gap against the label delay: not applicable (IID, complete fixed-window labels).
* Training history / season-shaped windows: not applicable.
* Grouped aggregation: not applicable (one row per participant).

</details>

<details><summary>Domain practitioner</summary>

Actor: a primary-care physician (or preventive cardiologist) at a routine exam of an adult free of coronary heart
disease, deciding on prevention (antihypertensive or lipid-lowering treatment, smoking cessation counselling) from the
patient's 10-year risk of a first CHD event.

**Fit: direct (agree with the definition)**

One row is one patient at one exam, every input is measured at that exam, the label is a first CHD event in a fixed
10-year window with complete follow-up for every kept row, and a random split stands for new patients of the same
population, which is how the Framingham risk functions themselves were derived and internally validated (USE-1, USE-3,
USE-5, USE-8, USE-11). The gaps below lower the ceiling or the transportability of the task; none of them makes the
task a stand-in (USE-8 approximate) or changes the decision.

**As the physician**

1. **Inputs at the moment.** I have all 15: age, sex, smoking and cigarettes/day, BP medication, history of stroke,
   hypertension, diabetes, total cholesterol, systolic/diastolic BP, BMI, heart rate, glucose. Education I would rarely
   record, but it is known then and is a legitimate input (USE-6). None of them is recorded after the exam (USE-3);
   HDLC/LDLC and all follow-up columns are dropped. What I would always have and is missing: **HDL cholesterol**. A
   lipid panel today always reports HDL, and every risk tool I use needs it (FHS hard-CHD 10-year function: age, total
   cholesterol, HDL, systolic BP, BP treatment, smoking; ATP III; Pooled Cohort Equations; SCORE2). In the teaching
   data HDL exists only at period 3 (0 non-null at periods 1 and 2, 3,027 at period 3), so it cannot be added without
   moving the prediction point. Missing glucose (9.2%), education (2.5%), BPMEDS (1.2%), total cholesterol (1.2%) are
   real missing values, as at a real exam.
2. **Target.** I act on a risk probability against a threshold (e.g. 7.5%, 10%, 20% 10-year risk), not on a class.
   The label (ANYCHD within 3,652 days) is the "total CHD" endpoint of the 1998 Wilson Framingham score: it includes
   angina pectoris and coronary insufficiency. Measured: 188 of the 379 positives are a first event that is not
   hospitalized MI or CHD death within 10 years (MI_FCHD gives 191). Treatment guidelines act on hard CHD (ATP III,
   the FHS page the record links) or hard ASCVD including stroke (ACC/AHA 2013). ANYCHD is a defensible, documented
   endpoint, not a proxy; hard CHD would be closer to what I act on today but halves the positives (64 per test fold).
   Competing deaths as No is the cumulative-incidence risk, the quantity a patient's absolute risk actually is; fine.
   The rebuilt label is a clear improvement over MIT's TenYearCHD, which counted 265 non-CHD deaths/losses as events
   (USE-5, case cirrhosis_patient_survival_prediction).
3. **Row and test data.** One row = one decision for one patient at one exam (USE-11: first assessment, one row per
   participant, IID without grouping). The test data is new patients of the same cohort: what an internal validation
   of a risk score uses (USE-10, cold start for a new patient). What I really face is a patient of the 2020s; the cohort
   was examined about 1956-1960 (teaching data: three exams about 6 years apart, roughly 1956 to 1968), before statins,
   with 3.0% on BP medication. That is a population/era shift a random split cannot test; it is the well-known reason
   Framingham equations overestimate risk in contemporary and non-US populations.
4. **Would I use it.** As a benchmark of how well a model ranks patients by risk from standard risk factors: yes, this
   is the canonical task of the domain. As a tool in my clinic: no, I would use a recalibrated published equation with
   HDL. What would make me trust a model: calibration (observed vs predicted risk by decile), not only ROC AUC. The
   metric `roc_auc` scores ranking only; a physician treating above a risk threshold needs calibrated probabilities,
   so `log_loss` would mirror the decision more closely (an EV question for the panel, not a fit gap). What would make
   me distrust it: the undocumented anonymization of the teaching data (values may be perturbed; consistency checks
   find no damage), and the lack of HDL.

**Gaps between the dataset and the real decision, ranked by how much they change the task**

1. **No HDL cholesterol** (feature gap, moderate). An input the actor always has and every guideline score uses; the
   teaching data has it only at period 3. It lowers the attainable discrimination but adds no leak and does not change
   the decision. It mirrors the historical Framingham profile of the 1970s (total cholesterol only), so the task is the
   real one at the source's era. Not fixable without moving the prediction point to period 3 (USE-4 style: offer the
   task at the stage the source has). An alternative definition at period 3 (HDL/LDL available, about 3,263 exams,
   follow-up to 24 years minus about 12, so 10-year windows still complete for most) would be the closer modern task,
   but older participants and those who survived to exam 3: a selected cohort. Keep period 1; name the missing HDL.
2. **Era and population shift** (transportability, moderate for use, none for the benchmark). 1956-era, mostly
   untreated, white Massachusetts cohort; the IID split stands for new patients of that cohort, not today's patients.
   This is how the risk equations were built and validated, so it does not lower the fit (USE-8 direct, USE-9: the
   well-defined use case is deriving a risk score in a cohort), but the task_summary `row` says "period not stated"
   although the BioLINCC documentation states it (exams roughly 1956-1968; baseline period 1 about 1956). USE-1 Methods
   item 1 asks for the period: write it.
3. **Endpoint softer than the one treated on** (target, small). ANYCHD includes angina and coronary insufficiency
   (188 of 379 positives are not hard CHD). Matches Wilson 1998 and MIT's task; hard CHD (MI_FCHD, 191 Yes) matches
   the linked FHS hard-CHD function and ATP III. Curator's call (REVIEW issue 1); both are real endpoints (USE-5).
4. **Metric scores ranking, not calibration** (evaluation, small). The decision is a threshold on absolute risk.
5. **Anonymized values** (data quality, small as far as measurable). Not a fit gap; it is named in fit_reason, which
   is the right place, though fit_reason mixes a quality caveat into the fit justification.

**What an expert in the domain would change**

- Write the period in `task_summary.row`: Framingham original cohort, baseline exam about 1956 (teaching data, three
  exams roughly 1956-1968), Framingham, Massachusetts. Replace "period not stated".
- Name the missing HDL in `known` or the curation_comments (measured only at the third exam), so a reader knows why the
  task differs from the clinical scores.
- In `use_case`, "for example" the endpoint: total CHD as in the 1998 Framingham CHD score; mention hard CHD as the
  alternative the curator weighed.
- Consider `log_loss` as the metric if the house rules allow it for a risk task (EV rules decide; not a USE rule).
- Keep competing deaths as No and the 16 lost participants dropped; keep IID with one row per participant (USE-11).
- Keep `fit = direct`; move the anonymization sentence out of fit_reason only if the house style wants fit_reason to
  speak to fit alone.

**Rules cited**

USE-1, USE-3, USE-4, USE-5, USE-6, USE-8, USE-9, USE-10, USE-11.

**Measured here (raw teaching CSV, period 1, PREVCHD = 0, 4,240 rows)**

HDLC non-null by period {1: 0, 2: 0, 3: 3,027}; missing share GLUCOSE 0.092, educ 0.025, BPMEDS 0.012, TOTCHOL 0.012;
age 32-70; BP medication 3.0%; diabetes 2.6%; prevalent hypertension 31.1%. Within 3,652 days: ANYCHD 379, MI_FCHD 191,
CVD 394, STROKE 124; ANYCHD positives without hard CHD in 10 years 188.

**Sources**

- `datasets/_dev/tabarena-v0pt2/framingham_heart_study_fhs/dataset.py`, README.md; record
  `curation/records/framingham_heart_study_fhs.md`; panel claims.md, checklist.md, probes, REVIEW_before.md.
- FHS hard CHD 10-year risk function: https://www.framinghamheartstudy.org/fhs-risk-functions/hard-coronary-heart-disease-10-year-risk/
  (inputs age, total cholesterol, HDL, systolic BP, BP treatment, smoking; endpoint MI or coronary death; Cox model;
  ATP III).
- BioLINCC teaching documentation 2021a: https://biolincc.nhlbi.nih.gov/media/teachingstudies/FHS_Teaching_Longitudinal_Data_Documentation_2021a.pdf
  and riskCommunicator `framingham` man page (https://rdrr.io/cran/riskCommunicator/man/framingham.html): 4,434
  participants, three exams about 6 years apart from roughly 1956 to 1968, 24 years of follow-up, data altered for
  confidentiality.
- Domain background (not fetched this run): Wilson et al. 1998, Circulation, "Prediction of coronary heart disease using
  risk factor categories" (total CHD endpoint, total or LDL cholesterol plus HDL); ATP III 2001 (hard CHD); Goff et al.
  2013 ACC/AHA Pooled Cohort Equations (hard ASCVD); known overestimation of Framingham equations in contemporary and
  European cohorts.

</details>

<details><summary>Blind review</summary>

**Verdict**
Include with changes. It is a real, classic 10-year CHD risk task with a modest but honest signal. Before it goes in, the target must be documented: it is not the public Kaggle `TenYearCHD` label, and its derivation has to be stated and checked.

**What the task is**
A clinician or a risk tool (like the Framingham / ASCVD risk scores) predicts a person's 10-year risk of coronary heart disease from data taken at one exam. The decision is about prevention (statins, blood-pressure treatment, lifestyle advice). This is a real and canonical use. All 15 features are measured at the baseline exam (demographics, smoking, BP medication, history of stroke or hypertension, diabetes, cholesterol, blood pressure, BMI, heart rate, glucose). None of them is measured after the outcome, so I see no leakage.

**Concerns (most to least serious)**

1. **The target differs from the public source, and the change is not documented.** I downloaded a public mirror of the Kaggle `framingham.csv` (4,240 rows, `TenYearCHD` positive 644 = 15.2%). It matches the documented missing counts exactly (glucose 388, education 105, BPMeds 53, totChol 50).
   - All 4,224 prepared rows match a Kaggle row exactly on all 15 features.
   - The 16 Kaggle rows that were dropped are all `TenYearCHD = 1`.
   - Of the remaining Kaggle positives, 249 are labelled "No" here. The prepared prevalence is 379/4,224 = 9.0%, against 15.2% on Kaggle.
   - Crosstab (prepared vs Kaggle): No/0 = 3,596, No/1 = 249, Yes/0 = 0, Yes/1 = 379.

   This looks like a deliberate re-derivation, probably from the BioLINCC teaching file (excluding prevalent CHD and using event time ≤ 10 years, or "hard CHD", given the hard-CHD risk-function link in task.md). That may even be an improvement, since the Kaggle label's 10-year window is poorly documented. But task.md does not say any of this.
   - Fix: document the exact rule (source file, event definition, the 3,652-day window, the exclusions, and how rows were matched without an ID), and cite where it comes from.
   - If the rule cannot be reproduced from public data, fall back to the Kaggle `TenYearCHD` label and the 4,240 rows.

   The two labels have similar learnability (LR AUC 0.740 prepared vs 0.726 Kaggle), so the benchmark does not hinge on the choice. Provenance does.

2. **The data is the anonymised FHS teaching data, not the research data.** The Kaggle file is widely understood to come from the NHLBI BioLINCC Framingham teaching dataset. BioLINCC says teaching datasets are not appropriate for publication because statistical measures (an R-methods textbook appendix says permutation and random visit selection) were used to make them anonymous. Values are plausible: sysBP ≥ diaBP everywhere, and `currentSmoker = 0` always has `cigsPerDay = 0`. The relationships are close to the real ones, so the data is fine for comparing methods. But it should be described as "FHS teaching data (anonymised)", not as the FHS cohort itself.

3. **Small and imbalanced, so scores are noisy.** There are 379 positives, about 126 per test fold. Under the 3x3 CV, AUC is LR 0.740 ± 0.019 and HistGB 0.716 ± 0.015. Age alone gets AUC 0.668. The signal is real but modest, and logistic regression beats boosting. That is a useful, non-trivial data point (a near-linear risk task), but method differences of about 0.01 AUC will not be significant. Use log-loss or AUC rather than accuracy, since the majority class is 91%.

4. **Preparation details (minor).**
   - `education` (1–4) is ordinal; keeping it numeric is fine.
   - Binary columns are int; `BPMeds` is float because of NaN; the target is a category with values No/Yes. All fine.
   - Missing values are left as NaN (glucose 9.1%, education 2.5%), which is appropriate.
   - The task is 13 years old and widely used, so it is heavily "seen", but that is acceptable.
   - There are no duplicate rows (0 duplicates on features).

5. **Split.** A random IID split is acceptable because each row is one person at one baseline exam, and there are no duplicates. The real deployment would be on a different cohort or era (calibration drift is well known for Framingham scores), and this split cannot test that.

**What I could not check**
- The exact derivation of `chd_within_10_years`. The prepared data has no ID, and I did not access BioLINCC's frmgham2 file (it needs registration).
- Whether the 16 dropped rows were excluded for prevalent CHD or for another reason.
- The Kaggle page text did not render, so I compared against a GitHub mirror of `framingham.csv`, assumed to be identical to the Kaggle file. Its row count and missing counts match the documented values.

**Sources**
- https://www.biolincc.nhlbi.nih.gov/teaching/
- https://www.bookdown.org/rwnahhas/RMPH/appendix-biolincc.html
- https://raw.githubusercontent.com/GauravPadawe/Framingham-Heart-Study/master/framingham.csv (mirror of the Kaggle file)
- The source links in task.md

</details>

<details><summary>Precedent check</summary>

**Summary**

| # | Decision | Verdict | Rules | Closest precedents |
|---|---|---|---|---|
| 1 | Read the BioLINCC teaching data, not the Kaggle/MIT file (against the CC "Likely use data from Kaggle") | consistent (departs from the CC with a stated reason) | PROV-13, PROV-15, stage precedence | SUPPORT2 / 2_month_survival_rate_prediction; corporate_credit_rating; cirrhosis (2026-10-14) |
| 2 | Rebuilt label, same record and unique_name | consistent with the in-place repairs; PROV-14's wording is literally triggered | PROV-13, PROV-14, PROV-11 | SUPPORT2 and cirrhosis (in place) against corporate_issuer_credit_rating (new record, 2026-10-16) |
| 3 | Endpoint ANYCHD, "the CHD of MIT's task" | outcome open (curator's call); the stated reason departs from precedent | USE-5, PROV-15 | cirrhosis (endpoint of the GLOBE score, 2026-10-14); PROV-15 case "TabSTAR's version" (Lennart, 2026-10-15) |
| 4 | Competing deaths (251) are No | consistent; no precedent on a post-prediction competing death | LEAK-22, LEAK-36, LEAK-23 | diabetes_130_us (case table); 2_month_survival_rate_prediction (day-3 deaths); cirrhosis |
| 5 | The 16 lost to follow-up dropped | consistent | LEAK-23, LEAK-25, CLEAN-15 | cirrhosis (5 lost dropped, 2026-10-14); mortgage (501 unrecorded exits dropped) |
| 6 | Anonymized teaching data shipped, no tag, issue 3 framed as a quality call | departs without a reason under the ranking: PROV-3 (Must) is the rule in play, and no precedent covers owner-perturbed values | PROV-3, SEL-16, LEAK-32, P7 | breast_cancer_prediction (teaching-only terms, shipped 2026-10-15); credit_card_customers (`2ndTierData`, legacy tag); PROV-3 cases (all `No`) |
| 7 | Terms "unsuitable for publication" noted, not a reason | consistent | SEL-1, PROV-2 | breast_cancer_prediction (BCSC "teaching tool only", Lennart 2026-10-15) |
| 8 | `education` numeric; 0/1 flags numeric | departs without a distinguishing reason (P7, Should); collection practice is mixed | CLEAN-12, CLEAN-14 | breast_cancer_prediction density numeric; apistox flags 0/1; caracas_cervical_cancer flags as yes/no categories (Lennart 2026-10-15); ljubljana, credit_g, coil_2000 reversed |
| 9 | `year` 2004 (record 2013) | direction consistent (the origin's year, not the copy's); the 2004 itself has no stated evidence | PROV-9, PROV-8 | airfoil_self_noise, first_principles_tully_fisher, nikuradse (2026-10-20) |
| 10 | IID split, one row per participant, no family ids | consistent | SPLIT-1, SPLIT-31 | breast_cancer_prediction (IID, one exam per woman, 2026-10-15); amazon_employee_access, bank_marketing |
| 11 | fit `direct`, perturbation named in fit_reason | consistent with 2_month_survival_rate_prediction; one gap unnamed | USE-8 | 2_month (direct, "the care is that of 1989-1994"); cirrhosis (approximate, treatment era) |
| 12 | Dropped columns (RANDID, constants, HDLC/LDLC, follow-up) | consistent | CLEAN-3, CLEAN-5, LEAK-10 | heart_failure_followup_survival `time`; 2_month follow-up columns |
| 13 | No accepted warnings, no splits_comment | consistent (nothing to check) | | |
| 14 | REVIEW issue 6 (SelectArena carries the defect) | consistent | PROV-15 | (own folder, not a third-party copy) |

No drift (case 3 of principles.md) and no third exception of one kind (case 4) found for this dataset. Decision 8 is
the second instance of "ordered codes stay numeric" (after breast_cancer_prediction); a third would make an amendment of
CLEAN-12/CLEAN-14 due.

**Details**

**1. The teaching data instead of the Kaggle file (CC "Likely use data from Kaggle ... we can use it")**

The record's two undated CC lines say to use the Kaggle data and accept the unclear origin. The definition reads the
teaching dataset (CRAN riskCommunicator). This departs from a curator decision, which ranks above an AI assessment, but
with a stated reason that ranks higher: the label of the Kaggle/MIT file is damaged (265 of 644 positives are not CHD,
measured, claim 39), so PROV-13 (Must) requires repair from the origin, and a later stage's measured finding supersedes
the screening reading (principles.md, "Stages"). The CC was about the unclear origin (PROV-2), which the AI resolved
(R, assessment 2026-10-07). Precedents that went the same way: SUPPORT2 restored from ICPSR 2957 in
`2_month_survival_rate_prediction` (PROV-13 case); `corporate_credit_rating` retired for the agencies' own histories;
`cirrhosis_patient_survival_prediction` label redefined (2026-10-14). REVIEW issue 1 offers "ship MIT's file as
published" as the alternative, so the curator sees the departure. Consistent.

**2. Same record and unique_name after the rebuild (PROV-14)**

PROV-14 (Must): "A rebuild that would not match the release exactly is a new dataset with its own record." The shipped
table does not match the MIT release (16 rows fewer, 265 labels changed). Precedents disagree with the wording:
`corporate_issuer_credit_rating` got a new record (PROV-11, Lennart 2026-10-16), while SUPPORT2
(2_month_survival_rate_prediction: blocks moved back to their patient) and cirrhosis (418 to 304 rows, a new target) were
repaired in place under their records. Framingham sits with the in-place group: the same 4,240 participants with the
same 15 feature values row for row (`_mit_rows` asserts a one-to-one match), only the label rebuilt; corporate credit
was new data from new sources. So the decision is consistent with the closest precedents; the open point is the rule
text, since the in-place precedents contradict it as worded ("a precedent that contradicts a rule is flagged").
Follow-on for the record: `source_links` still list the Kaggle uploads first and lack the BioLINCC page (PROV-8,
PROV-11), and `year` differs (decision 9).

**Consistency check (AI, 2026-10-20):** keeping framingham_heart_study_fhs under its record after rebuilding the label
departs from the wording of PROV-14 (a rebuild that does not match the release is a new dataset), as SUPPORT2 and
cirrhosis did, while corporate_credit_rating became corporate_issuer_credit_rating (2026-10-16). What sets this case
apart?
(a) the rows and feature values are the release's, row for row, and only the damaged label is rebuilt from the origin's
own columns: a repair (PROV-13), not a rebuild, recorded as such; (b) treat it like corporate_credit_rating: retire the
record and give the rebuild its own; (c) reopen SUPPORT2/cirrhosis to match corporate credit; (d) amend PROV-14 to
separate a repair (same units, same features, damaged values restored from the origin) from a rebuild (new sources).

**3. Endpoint: ANYCHD against hard CHD (USE-5)**

The outcome is the curator's call (REVIEW issue 1). The point here is the stated reason: D says "We keep ANYCHD, the CHD
of MIT's task". USE-5 (Must) asks what the actor acts on; the precedent `cirrhosis_patient_survival_prediction`
(2026-10-14) chose death or transplant because it is the endpoint of the GLOBE score the hepatologist uses, citing it.
Another version's framing is no reference for our label (PROV-15 case "TabSTAR's version of a dataset: another
collection's columns or labels are no reference for ours", Lennart 2026-10-15). The record links the FHS hard-CHD
10-year risk page (ATP III endpoint, MI_FCHD, 191 Yes). The physician's tool, not MIT's course, should carry the reason.
If ANYCHD stays, the reason could be the FHS total-CHD score (Wilson et al. 1998, Circulation, which to my recollection
used angina, coronary insufficiency, MI and CHD death; not read in this run, so PROV-16 needs a page and quote first).

**Consistency check (AI, 2026-10-20):** the endpoint ANYCHD is justified as "the CHD of MIT's task", where
cirrhosis_patient_survival_prediction (2026-10-14) took the endpoint of the clinical score the actor uses (USE-5) and
the 2026-10-15 PROV-15 case says another version's labels are no reference for ours. What sets this case apart?
(a) ANYCHD is the endpoint of an FHS risk function physicians use (Wilson 1998 total CHD, to be verified with a quote),
recorded as the reason instead of MIT; (b) treat it like cirrhosis and take the endpoint of the score the record links
(hard CHD, MI_FCHD, 191 Yes); (c) keep the MIT reason and reopen the PROV-15 case; (d) amend USE-5 to say a widely used
version's endpoint may stand in for the actor's.

**4. Competing deaths as No (LEAK-22)**

LEAK-22 (Must): "When the cohort holds rows that cannot have the outcome, follow the paper's cohort." Applied so far only
to rows ruled out at the prediction point: `diabetes_130_us` (encounters ending in death or hospice, known at discharge;
case table, Strack et al. 2014, Sec. 2.3), LEAK-36 ("a value known at prediction time that rules the outcome out is a
cohort question"), and `2_month_survival_rate_prediction` (138 patients dead on day 3, the prediction point). The 251
Framingham deaths happen after the baseline exam, so no rule or precedent asks to drop them, and dropping would select
on a post-prediction event (D, REVIEW issue 2, with the measured AUC gain from removing hard negatives). Cirrhosis is no
counter-case: death is its endpoint, not a competing event. Consistent. Two notes: (i) the FHS risk functions censor
non-CHD deaths in a Cox model, so "the paper's cohort" in LEAK-22 could be read the other way; the definition's
argument answers that reading; (ii) this is the first post-prediction competing-event decision in the register, so the
curator's answer should become a Cases row of LEAK-22 (or a Tensions row) so the next survival dataset follows it.

**5. The 16 lost to follow-up dropped**

Their 10-year status is unknown (TIMECHD 754-3,647 without an event): CLEAN-15 (Must, missing target) and LEAK-23
("over the rows followed that long"). Precedents: `cirrhosis_patient_survival_prediction` dropped its 5 patients lost
before 5 years (2026-10-14); `mortgage` dropped 501 unrecorded exits (LEAK-25, CLEAN-15). The definition's argument
against dropping deaths (selection on a post-prediction event) applies in form to the lost too; what sets them apart is
that their label is unknown, while the deaths' label (no CHD) is known. Consistent. The non-pair:
`heart_failure_followup_survival` keeps censored patients as survivors with fit approximate, because it has no horizon to
cut at; different facts, not a precedent against this one.

**6. Anonymized teaching data (REVIEW issue 3)**

The REVIEW and D treat the BioLINCC anonymization ("specific statistical measures were used to create anonymous
versions"; Nahhas: "permutations and/or random visit selection") as a quality question: ship, tag `2ndTierData`, or do
not ship. Under the ranking the rule in play is PROV-3 (Must, P5): "The data is real: not generated, and not a real table
someone reworked (relabelled, columns renamed, values replaced)" (the checklist also cites it). A Must has no exception;
"ship with a tag" is not a reasonable exception if the values were replaced. What the precedents give:

* PROV-3 cases, all `No`: customer_satisfaction_in_airline, ecommerce_shipping, homeq_default_prediction,
  video_game_fps_prediction. Each had measured manipulation (a PROV-3 test fired). Here the generated probe shows no
  flags and the consistency checks pass (BP r 0.78, within-person r 0.90/0.71 six years apart, ages match exam days in
  every row). That is the fact that sets it apart, but it bounds the perturbation; it does not show there is none.
* `breast_cancer_prediction` (CC Lennart 2026-10-15, shipped): BCSC "teaching tool only", but the caveat is about
  research use, not about altered values. It covers the terms half (decision 7), not this half.
* `credit_card_customers`: `2ndTierData` with marks of generated data. The tag was migrated from v1 (git: first in
  2475ea2, 2026-10-14), not a v2 curator decision, and `2ndTierData` is defined in no knowledge file. So "tag
  2ndTierData" has no curator precedent to follow.
* `Anonymized` tag: definitions.md says "Anonymized data: keep it as it is, tag `Anonymized`, and say what could not be
  determined", but defines the tag as "feature names or values carry no semantics or are masked"
  (ieee_fraud_detection, kdd_cup_09_appetency, amex; LEAK-32). Framingham's names and values keep their semantics, so
  no tag follows that definition; say so in the notes if the curator agrees.

No precedent covers values perturbed by the owner for privacy in a real cohort. Whatever the curator decides is new
ground and should be written down as a PROV-3 case (or an amendment narrowing PROV-3).

**Consistency check (AI, 2026-10-20):** shipping framingham_heart_study_fhs with values the owner says it anonymized by
"specific statistical measures" (permutations or random visit selection, undocumented) treats it as a quality call
(2ndTierData or not), but PROV-3 (Must) excludes a real table with values replaced, and every PROV-3 case so far was
retired (customer_satisfaction_in_airline, ecommerce_shipping, homeq_default_prediction, video_game_fps_prediction).
What sets this case apart?
(a) the alteration is the data owner's disclosure control on a real cohort, and every check we can run (generated
probe, within-person correlations, ages to exam days, HDL + LDL <= total) finds the structure intact, so it is real
data in the sense of PROV-3, recorded as a PROV-3 case; (b) treat it like the PROV-3 cases: `No` with `Data Quality
Issue`; (c) reopen the PROV-3 cases (unlikely: each had measured manipulation); (d) amend PROV-3: values perturbed by
the owner for privacy, with no measurable damage, are kept with a note (and say whether a tag applies).

**7. Terms "unsuitable for publication purposes"**

D's `license` quotes BioLINCC; REVIEW: "the terms are noted, not a reason". `breast_cancer_prediction` shipped under the
BCSC's "teaching tool only; they should not be used to conduct primary research" (Lennart 2026-10-15) with the note "We
use it to compare learning methods, not to estimate clinical effects". Consistent. D lacks that one-sentence reason; the
precedent has it. BioLINCC's teaching-request terms were not read (behind a login), so SEL-1 cannot be closed on
evidence; that is a fact gap, not a departure.

**8. `education` numeric and 0/1 flags numeric (CLEAN-12, CLEAN-14)**

CLEAN-12 (Should): "Reverse ordinal codes ... into categories with their labels". `education` 1-4 (documentation labels:
0-11 years, high school or GED, some college or vocational, college degree or more) stays numeric "as it is ordered".
Being ordered is what puts a code under CLEAN-12, so it does not set this case apart. Precedents both ways:
`breast_cancer_prediction` keeps density 1-4 numeric "since the order is the meaning" (shipped 2026-10-15);
`ljubljana_primary_tumor`, `credit_g`, `coil_2000` reversed their ordinal codes; `homesite_quote_conversion` keeps
ordinals numeric for another reason (anonymous codes, TabRed). The flags (`male`, `currentSmoker`, `diabetes`, ...)
stay 0/1: `apistox` does the same, while `caracas_cervical_cancer` (Lennart 2026-10-15) and `breast_cancer_prediction`
make yes/no flags categories. P7 only, so a quality point, but the collection has no single practice.

**Consistency check (AI, 2026-10-20):** keeping `education` 1-4 numeric departs from CLEAN-12 (reverse ordinal codes
into labelled categories), as breast_cancer_prediction's density did, while ljubljana_primary_tumor, credit_g and
coil_2000 reversed theirs; the 0/1 flags stay numeric like apistox, unlike caracas_cervical_cancer's yes/no categories
(2026-10-15). What sets this case apart?
(a) the four levels are bins of one quantity (years of schooling), so the numeric code keeps the order models need and
the labels go into the notes; recorded as an exception to CLEAN-12 (the second of this kind, after breast_cancer
density); (b) treat it like ljubljana: map `education` to its labels as a categorical, and the flags to Yes/No;
(c) reopen breast_cancer_prediction to match; (d) amend CLEAN-12/CLEAN-14 to say when ordered levels and 0/1 flags stay
numeric.

**9. `year` 2004 against the record's 2013 (PROV-9)**

The direction is consistent: the year is the origin's (the BioLINCC teaching dataset), not a copy's (MIT 15.071, Kaggle),
as in airfoil_self_noise, first_principles_tully_fisher and nikuradse (Lennart, 2026-10-20). But D gives no evidence for
2004: the bibtex cites the documentation as "version 2021a" under `year = {2004}`, and no note says when BioLINCC first
released the teaching file. The record's 2013 is probably the MIT/edX course year, a copy's year. A fact to settle
(EV-1) before the record is aligned; no judgment call, so no prompt.

**10. IID split**

One row per participant; the teaching data has no family ids or exam dates, and the hidden-group probe finds no group.
Spouses and relatives in the original cohort cannot be identified, so IID over possibly related people follows SPLIT-31
(IID that matches the framing; amazon_employee_access, bank_marketing) and the breast_cancer_prediction decision (one exam
per woman, IID, Lennart 2026-10-15). Consistent.

**11. fit `direct`**

Follows `2_month_survival_rate_prediction` (direct, with the era named: "The care is that of 1989-1994"). Cirrhosis went
`approximate` for its treatment era, but its decision (transplant evaluation) depended on that era (4 transplants of
107); prevention by BP or cholesterol treatment was also different at the FHS baseline, which D does not name ("period
not stated"). Consistent with the closer precedent; naming the era like SUPPORT would match it fully. USE-8's examples of
approximate do not include perturbed values, so the perturbation in fit_reason with `direct` breaks no precedent.

**12-14**

Dropped columns: RANDID (CLEAN-3), constants PERIOD, TIME, PREVCHD, PREVAP, PREVMI (CLEAN-5), HDLC/LDLC all missing at
period 1 (CLEAN-5), follow-up and time-to-event columns (LEAK-10; heart_failure_followup_survival `time`, 2_month's
follow-up columns). Consistent. No accepted warnings and no splits_comment: nothing to compare. Issue 6 (SelectArena
`datasets/_dev/feature_selection/framingham_heart_study/` with MIT's label and `domain_str="physics & astronomy"`) is
about our own folder, not a third-party copy, so PROV-15's "note, do not raise" does not bind it; raising it for
awareness is consistent.

</details>

<details><summary>Advocate</summary>

Position: ship as defined, after wording fixes in `task_summary`/notes and a recorded decision on two rule texts
(PROV-3, PROV-14). No change to rows, features, label or split is needed.

**1. The rebuilt label is the repair PROV-13 and USE-5 require (P5 and P3, Must)**

- Evidence: MIT's `TenYearCHD` equals `TIMECHD < 3,652` in 4,240 of 4,240 rows; TIMECHD is the censor date without an
  event (documentation p. 4). So 265 of 644 positives (41%) are 249 non-CHD deaths and 16 losses (claim audit 7, 27,
  39; the blind reviewer independently found 249 No/1 and 16 dropped, all MIT positives). Our label: ANYCHD within
  3,652 days, 379 Yes; no event date falls on days 3,648-3,654, so the cut-off is robust (claim 12).
- Precedents: SUPPORT2 and cirrhosis repaired in place (PROV-13 cases, USE-5 case).
- Objection answered, PROV-14 (Must, "a rebuild that would not match the release is a new dataset"): concede the
  wording is triggered. But the rows and all 15 feature values are the release's, row for row (`_mit_rows` asserts
  one-to-one on 4,240), and only the damaged label is restored from the origin's own columns. This is a record
  question, not a data-validity one; the two closest precedents (SUPPORT2, cirrhosis) went in place. Mildest remedy:
  precedents.md option (a), record it as a PROV-13 repair, or (d), amend PROV-14 to separate repair from rebuild.
  The alternative (ship MIT's label) breaks USE-5 and PROV-13, both Must; retiring the record for a new one changes
  bookkeeping, not what ships.

**2. Evaluation is honest (P4): no leak, and the split matches the use case**

- Evidence: all 15 features are as of the baseline exam: prevalent flags absorbing across periods, PREVHYP = 1 iff
  TIMEHYP = 0 (1,317/1,317), PREVSTRK all TIMESTRK = 0; HDLC/LDLC and all 16 follow-up columns dropped (column audit);
  missing indicators AUC <= 0.512; best single feature age 0.640; 0 duplicate feature vectors, 0 near copies (probes).
- Split: one row per participant, IID, 3 x 3 stratified, 126-127 positives per test fold (split audit). USE-11 (Must):
  a first assessment of a new patient is one row per entity, IID; precedent breast_cancer_prediction (earliest exam,
  Lennart 2026-10-15). RANDID quintiles show no drift.
- Objections answered: (a) USE-11's "only when the use case is that row" against the extra 10,759 later exams
  (LR 0.736 -> 0.745): fix the wording, not the data; say "at a patient's first assessment", as in breast_cancer. The
  baseline is also the documentation's population at risk (p. 5). A grouped all-exams variant is a curator option, not
  a defect. (b) Spouses (SPLIT-29/31): no household id exists; the probe finds no hidden group, near copies 0.0%, and
  spouses share little CHD label. Remedy: "relatives cannot be identified" in the Note bullet.

**3. The anonymization does not trigger PROV-3 on the evidence (P5, Must; EV-1, EV-2)**

- PROV-3 excludes a table "someone reworked (relabelled, columns renamed, values replaced)". Every PROV-3 case so far
  (airline, ecommerce_shipping, homeq, video_game_fps) was retired on a measured test that fired. Here none fires:
  the generated-data probe gives no flags; digit preference is intact (SYSBP x2 ends in 0 for 22.5% vs 2-4% for odd
  digits; heart rate 0/5 at 29.7%/26.8%; cigarette heaping), which refutes additive noise; per-sex period-1 means,
  minima, maxima and Ns equal the documentation's tables (p. 10-12) exactly; within-person BMI and SBP six years apart
  r 0.90 and 0.71 (permutation across people would weaken this); ages match exam days in every later exam; HDL + LDL
  never exceeds total cholesterol; sysBP > diaBP everywhere.
- Rule: facts first (EV-1); a measurement on the data outranks a page (EV-2). The owner's disclosure control on a real
  cohort with intact structure is real data, not a reworked table.
- Concede: permutation of a few values or visit selection cannot be measured, so "slightly perturbed" is inference.
  Mildest remedy: write "no added noise (digit preference intact); other methods cannot be checked", and record the
  curator's call as a PROV-3 case (precedents option a) or an amendment (d). Exclusion is for a Must that is shown to
  fail; the real FHS data cannot be redistributed, so there is no better origin to repair from.

**4. Fit `direct` holds (USE-8, Must); the era is a wording gap**

- Evidence: the practitioner agrees on direct: one patient at one exam, inputs at the exam, a fixed 10-year label with
  complete follow-up, a random split of new patients of the cohort, "which is how the Framingham risk functions were
  derived and internally validated". Precedent 2_month_survival_rate_prediction: direct, with "the care is that of
  1989-1994" named. Cirrhosis went approximate because its decision (transplant) depended on the era (4 transplants of
  107); here the prediction from risk factors does not.
- Concede: "period not stated" is refuted (documentation p. 1: exams "from roughly 1956 to 1968"). Remedy: write the
  baseline as about 1956 in `row` and name the era (pre-statin, BP medication 3.4%) in `fit_reason`. USE-8 lists no
  era or perturbation among the approximate examples.

**5. The endpoint is a real one; only its stated reason needs replacing (USE-5, Must)**

- ANYCHD is the documentation's CHD (angina, MI, coronary insufficiency, fatal CHD) and the "total CHD" endpoint of
  the 1998 Wilson Framingham score (practitioner). Hard CHD (MI_FCHD) gives 191 Yes, about 64 per test fold.
- Concede: "the CHD of MIT's task" is a weak reason (EV-4 case: another collection's labels are no reference for
  ours). Remedy: cite Wilson 1998 with a page and quote (PROV-16) as the reason. Which endpoint is the curator's
  weighing call (REVIEW issue 1); both satisfy USE-5.
- Competing deaths as No: the cumulative-incidence risk a patient faces (practitioner); dropping them selects on a
  post-prediction event (LR rises 0.738 -> 0.752 only from losing hard negatives). No rule asks to drop them
  (LEAK-22 cases are all at the prediction point). The 16 lost are dropped as unknown labels (CLEAN-15; cirrhosis,
  mortgage).

**6. Worth benchmarking (P6)**

- LR ROC AUC 0.739 (0.717-0.768), HGB 0.706-0.716, age alone 0.640-0.668: a real, modest, non-trivial signal where a
  linear model beats boosting, a useful data point (claim audit, blind review). 379 positives, 126 per test fold: not
  Too Small. The blind reviewer, without our notes, said "include".

**7. Quality items are notes, not blockers (P7; P3 over P7 tension)**

- `education` 1-4 kept numeric: bins of years of schooling; second instance after breast_cancer_prediction density.
  Record as a CLEAN-12 exception (Should). cigsPerDay heaping at 9/43: one-line note, same in train and test.
- Terms "unsuitable for publication": breast_cancer_prediction shipped under "teaching tool only" (Lennart
  2026-10-15); add its sentence "we compare learning methods, not estimate clinical effects".
- Record `year` 2013 -> 2004: the documentation's SAS file was created 2 March 2004 (doc p. 8, claim 17), which also
  gives the 2004 its missing evidence. Add the BioLINCC page to `source_links`.

**Rebuttal**

We agree on the outcome: ship after text and record changes, with no exclusion and no change to rows, features or
split. We disagree on two framings (points 1 and 4) and one fact (point 5).

**1. Endpoint (USE-5): concede the reason, dispute that the label is in doubt**

- Concede: "the CHD of MIT's task" has to go (EV-4/PROV-15 case, 2026-10-15). Replace it with the Wilson 1998 total-CHD
  quote and its page (PROV-16).
- Dispute: "the label may not be what the actor acts on" does not make the current label fail USE-5. ANYCHD is the
  source's own documented CHD endpoint (doc p. 4: AP, MI, CI, fatal CHD), and the practitioner calls it "a defensible,
  documented endpoint, not a proxy". Prevention covers angina as well. So both ANYCHD and MI_FCHD satisfy USE-5, and
  choosing between them is a weighing call (REVIEW issue 1). Factors: hard CHD matches ATP III, but it halves the
  positives to about 64 per test fold (P6 -). Cirrhosis does not decide this. There, the label the source built was
  wrong (time to death among patients who died). Here the label we built is a real endpoint.
- Follows: one text fix; the endpoint stays the curator's call.

**2. Era, period, HDL: concede in full**

- Same remedy as my point 4: write "about 1956" in `row`, name the pre-statin era in `fit_reason`, and add a bullet
  saying HDL was measured only at the third exam. I keep `direct` (practitioner, and the 2_month precedent), and the
  critic asks only that the gap be named. No dispute is left.

**3. "Routine exam" against the first exam: concede the wording**

- The remedy is the same as in my point 2 ("at a patient's first assessment"). The all-exams grouped variant is a
  curator option, and both sides say so.

**4. PROV-3: concede the recorded decision, dispute "without it the rule says No"**

- Concede: the curator should record the decision as a PROV-3 case or as an amendment. I also accept the critic's
  wording for `fit_reason`/Anomaly and the breast_cancer sentence on the terms.
- Dispute: PROV-3 is not shown to be triggered, so the default is not `No`. The rule is applied by its tests (the
  seven "Is the data generated?" tests, EV table), and none fires here. Every PROV-3 case was retired on a measured
  test that fired. Here the measured checks run the other way: the documentation's per-sex tables are matched exactly,
  the within-person correlations are 0.90/0.71, and digit preference is intact. Facts come first (EV-1), and a
  measurement outranks a page (EV-2). An owner's statement that "specific measures" were used, with no measurable
  effect, does not establish "values replaced" to the standard that retired the other four. Recording the decision
  writes this down as a case. It does not grant an exception to a Must that has fired.
- Follows: the same changes either way. The curator's decision is a confirmation, not a rescue.

**5. PROV-14 and the record: concede the record fixes; partly dispute the year**

- Concede: record it as a PROV-13 repair or amend PROV-14 (both briefs give the same options). Put the BioLINCC page
  first in `source_links`.
- Partly dispute: 2013 has no evidence at all; it is likely the MIT/edX course year, which is a copy's year (PROV-9
  direction, airfoil/nikuradse 2026-10-20). The SAS date 2004-03-02 in the documentation is the earliest dated trace of
  the teaching file (claim 17). Concede that it is a creation date, not a proven release date. Remedy: set 2004 with
  the note "teaching file created 2004-03-02 (doc p. 8); first release date not stated". That is better supported than
  keeping 2013.

**6. `education` numeric: concede it is a Should and the curator's call**

- Either remedy is acceptable. My preference is to keep the numeric code as a recorded exception to CLEAN-12. The four
  levels are bins of one quantity (years of schooling), so the order carries the meaning (the breast_cancer density
  reason). Mapping to labels would also be cheap and safe. This is P7, so it does not block shipping.

</details>

<details><summary>Critic</summary>

Position: do not ship as defined. Ship after changes 1-5. None of them needs exclusion. Point 4 has to become a
written curator decision under a Must; without that decision the rule says `No`.

**1. The endpoint rests on MIT's course, not on the actor's tool (P3, USE-5 Must)**

- Problem: `curation_comments` keeps ANYCHD because it is "the CHD of MIT's task". The record links the FHS hard-CHD
  10-year page (MI_FCHD). The physician acts on hard CHD (ATP III) or hard ASCVD. ANYCHD includes angina and coronary
  insufficiency: 188 of the 379 positives are not hard CHD (practitioner, measured).
- Effect: the label may not be what the actor acts on. The reason given is one that PROV-15 rejects: another
  collection's labels are no reference for ours (Lennart 2026-10-15). Cirrhosis took the endpoint of the clinical score
  (2026-10-14; precedents #3).
- Remedy (fix the definition): keep ANYCHD only with the physician's reason. That means Wilson et al. 1998 total-CHD
  score, quoted with page per PROV-16; nobody on the panel has read it yet. Otherwise switch to MI_FCHD (191 Yes, about
  64 per test fold). Replace the "MIT's task" reason in either case.

**2. The row says "period not stated", but the source states it, and the era gap goes unnamed (P3, USE-1 Must, USE-8 Must)**

- Problem: the documentation, p. 1, says the exams ran "from roughly 1956 to 1968", so the baseline is about 1956 (claim
  audit #3, refuted). USE-1 Methods item 1 asks for the period. The use case is a prevention decision today. The cohort
  is pre-statin (BP medication 3.0-3.4%) and has no HDL: HDLC exists only at period 3 (0 non-null at periods 1 and 2).
  Every guideline score uses HDL.
- Effect: a reader of the task_summary is told something false about the row and does not see why the task differs
  from today's risk scores.
- Remedy (fix the definition, text only): `row` gets "baseline exam, about 1956 (exams 1956-1968, documentation p. 1)".
  `fit_reason` names the era, as 2_month_survival_rate_prediction does ("the care is that of 1989-1994"). `known`, or
  a bullet, says HDL was measured only at the third exam. Whether era plus anonymisation make the fit `approximate` is
  the curator's call (USE-8, USE-9). I ask only that the gap be named.

**3. The use case says "a routine exam", but the rows are only the first exam (P3/P4, USE-11 Must)**

- Problem: USE-11 says to take one row per entity "only when the use case is that row: it loses rows and signal". The
  teaching data has 10,759 CHD-free exam rows with a known 10-year status (1,229 Yes) against the 4,224 used. Training on
  all exams raises LR 0.736 to 0.745 and HGB 0.691 to 0.720 on the same baseline test rows (split audit, note 1).
- Effect: the stated use case does not match the rows chosen.
- Remedy (mildest, wording): `use_case` and `row` say "the first exam". The alternative, every exam with a grouped split
  by RANDID, is a curator option and I do not demand it.

**4. Values replaced by the owner's anonymisation; no exception recorded (P5, PROV-3 Must; SEL-16)**

- Problem: PROV-3 excludes "a real table someone reworked (... values replaced)". BioLINCC: "specific statistical
  measures were used to create anonymous versions". Nahhas names "permutations and/or random visit selection". Every
  PROV-3 case so far is `No`. The definition treats this as a quality question (tag or not). Under a Must that framing
  is wrong (precedents #6).
- Evidence on the other side, which I accept: digit preference is intact, so there is no additive noise (claim audit
  #11). Within-person correlations are 0.90 and 0.71, ages match the exam days, and the prevalent flags agree with the
  event columns. Permutation and visit selection cannot be tested. So "slightly perturbed" and "small" are inference
  and not measured (EV-6).
- Effect: if values were permuted across participants, the benchmark measures methods on altered associations. BioLINCC
  itself calls the data unsuitable for publication, and a benchmark publishes results.
- Remedy (no exclusion): the curator records a PROV-3 case or an amendment. Suggested wording: owner disclosure control
  on a real cohort, no measurable damage, kept with a note. Rewrite `fit_reason` and the Anomaly bullet as "no added
  noise (digit preference intact); permutation or visit selection cannot be checked". Add the one-sentence reason for
  use despite the terms, as breast_cancer_prediction has ("to compare learning methods, not to estimate clinical
  effects"). If the curator will not record the exception, PROV-3 gives `No` / `Data Quality Issue`.

**5. A rebuilt label under the release's record (P5, PROV-14 Must; PROV-8)**

- Problem: PROV-14: "A rebuild that would not match the release exactly is a new dataset with its own record". The
  shipped table differs from MIT's release: 16 rows fewer and 249 labels flipped. SUPPORT2 and cirrhosis stayed in place
  and corporate credit did not, so the precedents contradict the rule as worded (precedents #2). The record still lists
  the Kaggle uploads first and has no BioLINCC page; its `year` is 2013 against the definition's 2004 (refuted, claim
  audit #41).
- Remedy (fix the record): the curator records this as a PROV-13 repair (same 4,240 participants, same feature values
  row for row) or amends PROV-14. Put the BioLINCC teaching page and documentation first in `source_links`. Set `year`
  only after the 2004 has evidence: the bibtex cites documentation version 2021a, and the SAS date of 2004-03-02 is a
  file date, not a release (precedents #9).

**6. `education` kept as a numeric code (P7, CLEAN-12 Should): quality, not a reason to exclude**

- The four documented levels stay as floats 1-4. "It is ordered" is what puts a code under CLEAN-12, so it does not set
  the case apart. Mapping to labels is cheap and safe. Otherwise record it as an exception, the second after
  breast_cancer_prediction density. With a third, CLEAN-12 would need an amendment.

Dropped: SEL-1 on the BioLINCC request terms (behind a login, unread, no evidence); relatives across the split (SPLIT-29,
cannot be measured, and the probe finds nothing); cigsPerDay heaping at 9 and 43 (no sentinel evidence).

**Rebuttal**

We agree on what ships. Rows, features, split and the rebuilt label stay. What is still open is whether three Must
points are settled now or only once their conditions are met.

1. **Rebuilt label; PROV-14.** Concede. The repair is what PROV-13 and USE-5 require, and MIT's label would break both.
   We ask for the same remedy: record a PROV-13 repair, option (a), or amend PROV-14, option (d). Fixing the record's
   `source_links` stays part of it.

2. **Honest evaluation; USE-11.** Concede. The wording fix ("the first assessment / first exam") is the remedy I asked
   for. The all-exams variant is the curator's option. Add "relatives cannot be identified" to the Note bullet.

3. **PROV-3 "not triggered".** Dispute the framing; the remedy is shared.
   - The advocate's tests rule out additive noise. The method the owner names, "permutations and/or random visit
     selection", was never tested. The advocate concedes it "cannot be measured".
   - EV-2 lets a measurement outrank a page only where the measurement covers the claim. Here it does not: untested is
     not refuted.
   - The owner's own statement that the values were altered is the fact that triggers PROV-3. No probe needed to fire.
   - Under a Must, the shipped verdict therefore needs the recorded case or amendment, option (a) or (d), before it ships.
     It is not an optional note. The advocate proposes the same record, so the difference is only whether it is
     required. I hold that it is.

4. **Fit `direct`.** Concede that USE-8 lists no era example, and that the 2_month precedent supports `direct` once the
   era is named. Still required: the `row` and `fit_reason` text, and the missing HDL named (measured only at period 3).

5. **Endpoint.** Partly dispute.
   - "Both satisfy USE-5" holds for ANYCHD only once Wilson 1998 is read and quoted (PROV-16 Must). Today nobody on the
     panel has read it; the practitioner listed it as "not fetched this run".
   - Until the quote is in, the only actor's tool on record is the hard-CHD page the record links. So the condition
     stands: quote Wilson, or switch to MI_FCHD.
   - Competing deaths as No and dropping the 16 lost: concede.

6. **Worth benchmarking.** Concede.

7. **Quality items.**
   - `education`, cigsPerDay and the terms sentence: concede, as notes and an exception.
   - `year` 2004: dispute. Doc p. 8 is a SAS PROC CONTENTS "Created" stamp, the date the file was made. It is not
     BioLINCC's release of the teaching dataset, and the bibtex cites documentation version 2021a. PROV-9 asks for the
     origin's year, so 2004 still needs a release date or a note that it is the file date. This is P5 metadata, not a
     blocker.

Net: ship after changes 1-5 of my brief. No exclusion if the PROV-3 case is recorded.

</details>
