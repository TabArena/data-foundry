# infrared_thermography_temperature

**Outcome:** added. PhysioNet's FLIR file of an FDA fever-screening study at the University of Maryland Health
Center (2016-2018): regression of the oral temperature `aveOralM` from the first image's facial temperatures, the
room readings and a short intake, IID over 1,001 people. Verdict: ship once rebuilt; the review panel ran (full tier, 2026-10-20) and its fixes
are in the definition, which is not rebuilt yet. Validity: SEL-15 holds on the
panel's reading (the camera is used as a thermometer at fixed facial sites), for the curator to confirm (issue 3);
USE-7 triggered, fixed (the 17 people without a complete first image dropped, 1,018 to 1,001 rows); USE-8 direct
after the rewrite to the clinic triage setting (USE-9); LEAK-10 holds (`aveOralF`, rounds 2-4, `SubjectID`, `Date`
and one measurement stored under two subject codes dropped); SPLIT-4 holds (IID over people, the day's conditions are features). Value: TP-2
holds (an additive model 0.264 °C RMSE against a one-feature calibration 0.276 °C, better on 29 of 30 splits).
Quality: wording and numbers fixed; the `Distance` repair and the `Age` and target-grid anomalies kept with notes.
Weighed: size -, source +, use case +, shift between the study years - (small). For the curator: issue 3 (scope
and an amendment of SEL-15), issue 1 (a temporal variant, a weighing call).

**Main points:** Confirm that temperatures read through a thermal camera are measurements (SEL-15), recorded as an
amendment (issue 3); keep IID or add a temporal variant (issue 1).

**Issues for Lennart:**

3. **Are temperatures read through a thermal camera in scope as measurements (SEL-15)?**
   The record carries the marker `Wrong Domain / Source Modality`, and 27 of the 35 features are read from the
   thermal image. No curator has ruled on the scope (the record has no curator comment), and a Must allows no
   exception, so the keep needs a rule that covers it.
   - Effect: under SEL-13 the verdict is `No` with `Image` and the folder is removed; under SEL-15 the dataset is in
     scope as it stands.
   - Evidence for SEL-15 (the advocate, the critic, the practitioner and the precedent checker agree): each column
     is a blackbody-compensated temperature in °C at a named facial site (the maximum or the mean of the 4 warmest
     pixels), and the target is the same quantity measured by mouth. The source's model is a one-feature
     calibration on `T_Max1` (Wang et al. 2022, [Sensors 22(1):215](https://doi.org/10.3390/s22010215), Sec. 2.5).
     Fever-screening cameras output these readings, IEC 80601-2-59 names the inner canthi as the reference site,
     and the [release](https://doi.org/10.13026/3bhc-9065) holds no images.
   - Evidence for SEL-13: satimage and wilt (radiometric values from an imaging sensor) are `No`, and SEL-13 lists
     "remote-sensing spectra". The key points of the face were placed by hand for about half the images.
   - Implemented: in scope; the last curation note gives the SEL-15 reason (the camera as a thermometer at fixed
     sites, the target the same physical quantity, no images) and names satimage and wilt as the counter-cases,
     where the values serve to recognise what the image shows.
   - Alternative: exclude under SEL-13: `No`, `Image`, folder removed.
   - Rule: SEL-13 (Must) against SEL-15 and SEL-14 (Must). This is the third keep of quantities measured through an
     imaging device with no written reason, after biomechanical_orthopaedic_prediction and dementia_prediction, so
     an amendment is due (principles, consistent judgement).
   - Decision needed: (a) confirm SEL-15; the amendment the precedent checker drafted records the reason: "a physical
     quantity measured through an imaging device at defined sites (a temperature, a volume, an angle), used by the
     field as the instrument's reading, is a measurement (SEL-15), not an image descriptor (SEL-13)", with satimage
     and wilt as the counter-cases, and then re-read the two earlier keeps against it; or (b) exclude. The panel
     recommends (a).

1. **Split: keep IID over people, or add a temporal variant on the measurement date?**
   A calibration is fitted once and then used on people who come later; the task ships IID, so each test person
   was screened in the same period as the training people.
   - Effect: for "calibrate once, use later", IID may understate the error by about 0.5-7% RMSE on
     average (up to 29% in the first window of the second year). No leak is involved.
   - Evidence for IID: each row is a new person seen once, and the day's conditions (`T_atm`, `Humidity`,
     `Distance`, `T_offset1`) are recorded for every new person, so they are features. Folds grouped by day score
     as random ones do (random forest R^2 0.699 against 0.700, 10 x 3 folds). The measurement day explains about 3% of the target's
     variance (intraclass correlation 0.03). IID is the source's own split (a random 60/40, Wang 2022 Sec. 2.5, with its
     own upward-bias caveat in Sec. 4.5).
   - Evidence for temporal: the set-up changed between the study years (two locations, median distance 0.80 m to
     0.60 m). A first-year calibration over-predicts the second year by 0.06-0.09 °C and is worse on 12-15 of 15
     folds. In 6 expanding windows over the newest half of the days, past-only training costs +0.5% (ridge), +1.5%
     (forest) and +6.7% (LightGBM) RMSE against a random training set of the same size; the first window of the
     second year is 5-29% worse.
   - Implemented: IID over people, 10 x 3 random folds; the year change is stated in the task summary's split and
     in `splits_comment`. Cost: the year-to-year shift does not show in the score.
   - Alternative: `temporal = Temporal(on="Date", splits=TemporalSplits(window=None, unit="unique", n_windows=6,
     min_train_fraction=0.5))` with the date kept out of the features, no gap (the oral reading follows the image by minutes). Cost: only the newest half of the days is tested,
     and 2 of the 6 windows fall in the 2017-18 flu peak.
   - Rule: SPLIT-3 (one regime, the one the use case implies) and SPLIT-31 (an optimistic IID task that matches its
     framing is a candidate for a variant, not a fix); the size of the gap does not decide (SPLIT-4). Follows
     amazon_employee_access and bank_marketing (SPLIT-31).
   - Decision needed: is the use case "a new person at a calibrated station" (IID, the panel's recommendation, with
     temporal recorded as a candidate variant) or "a calibration deployed later" (temporal)?

**Review panel:** ship after changes (mediator). Claim audit: 36 claims, 25 hold, 8 refuted (6 fixed in the
definition, 2 in the record's assessment), 1 record field in another vocabulary, 2 untested. Blind review: would
include; its main concerns were round 1 only and an IID split that ignores time. Debate: the advocate and the critic
agree on the verdict and every fix; settled by rank: the 17 retake rows go (USE-7 over LEAK-11); a citation settled:
SPLIT-4, not SPLIT-21. The mediator's issues 1 and 2 are issues 3 and 1 here; the panel's numbers are from
the 1,018 rows before the 17 were dropped.

<details><summary>Mediator</summary>

The advocate and the critic agree on the verdict and on nearly every remedy. Two disputes remain. One is settled by
rank: the 17 retake rows go, and keeping them would need an amendment of USE-7. The other is a citation: SPLIT-4
applies, not SPLIT-21. Two calls go to the curator: the scope reading together with the SEL-15 amendment, and a
temporal variant.

**Judgment record**

```text
Verdict: ship after changes.
Validity: SEL-15 holds on the panel's reading (the camera works as a thermometer at fixed sites; the "exception"
  wording is removed; curator to confirm, amendment proposed, issue 1); USE-7 triggered, fixed (drop the 17 retake
  rows, 1,018 -> 1,001); USE-8 direct after the rewrite to the clinic triage / calibration setting (USE-9); LEAK-10
  holds (aveOralF, rounds 2-4, SubjectID, Date and the twin pair dropped); SPLIT-4 holds (IID over people, reason
  restated on the entity).
Value: TP-2 holds (additive model 0.265 against a one-feature calibration 0.277 °C RMSE, better on 28/30 splits).
Quality: text, number and record fixes; the Distance repair and the Age/grid anomalies are consistent (CLEAN-11).
Weighed: size -, source +, use case +, year-to-year shift - (small).
For the curator: issue 1, the scope reading and the SEL-15 amendment; issue 2, a temporal variant (weighing).
```

**Changes to make now (no decision needed)**

The data change (1) needs a rebuild, which happens only when the curator asks (rebuild.md). The rebuild then brings a
CHANGELOG entry and a new row count in the working copy's README table.

1. **Drop the 17 retake rows.** In `_clean`, keep only the subjects with a complete round-1 image. Remove the
   `first_complete_image` substitution, Decision 2 as written, and curation bullet 3. Restate the 17 as a dropped
   cohort: 5 of 111 at or above 37.5 °C, 4 at or above 38 °C. Rule: USE-7 (P3, Must). These rows lack the input the
   prediction acts on, which is the image taken before the thermometer. LEAK-11 (P4, Should) narrows LEAK-10, not
   USE-7. So it cannot keep the rows: a higher part beats a lower one, and a Must beats a Should. This is not a
   conflict. USE-7 fails on its own (principles step 4). Leaving the values missing also breaks USE-7, and the
   missingness would mark a group that is 29% febrile. Keeping the rows is no longer a curator option unless USE-7 is
   amended.
2. **Rewrite `use_case`, `row`, `changes`, `fit_reason`; keep `fit = "direct"`.** Rules: USE-8 (Must) and USE-9.
   - `use_case`: a clinic triage station, or an IRT maker calibrating a device, after the person has rested 15 min in
     the room, with a short intake.
   - `row`: the UMD University Health Center, College Park, Nov 2016 to May 2018, mostly students.
   - `changes`: true once change 1 is made.
   - `fit_reason`: Gender, Age, Ethnicity and Cosmetics are stated by the person at intake. Name the best-case
     conditions (acclimation, hand-placed key points for about half the images, blurred images excluded), as both
     papers do.
   - The person-stated inputs stay. Dropping them costs 0.004-0.009 R², and a clinic intake has them.
3. **Remove the "exception" wording.** In the last curation bullet, replace "an exception to the record's marker"
   with the SEL-15 reason: radiometric temperatures at fixed facial sites, the camera used as a thermometer, a target
   that is the same physical quantity, and no images released. Give satimage and wilt as the counter-cases (content
   recognition). Drop "since Lennart asked" from the review text. Rule: principles.md says "a Must has no
   exceptions". The wording of the reason waits on issue 1, but "exception" goes now.
4. **Split text.** Ground IID on the entity: each row is a new person, and the day's conditions (T_atm, Humidity,
   Distance, T_offset1) are recorded for every new row, so they are features (SPLIT-4). Drop the gap figures as the
   reason in bullets 9 and 10. Restate bullet 10 as evidence, not as the reason: about 0% on average, with the first
   year-2 window 2-16% worse across models and biased by +0.1 °C. Add the set-up change between the years to `split`
   and `splits_comment`: median distance 0.80 m to 0.60 m, two locations, and a year-1 calibration over-predicts year 2
   by 0.07-0.09 °C. Rules: SPLIT-4 and USE-8. SPLIT-21 governs the training history and the windows of a temporal
   task, not the choice of regime, so the advocate's citation stands.
5. **Wording.** Bullet 5: "the screening station records all four", not "a screening thermograph measures". Bullet
   11: "a one-feature segmented calibration in the source's style (our 4-knot spline)", since Wang 2022 gives no
   knots. Rules: writing.md, EV-2.
6. **Numbers.** Day-grouped against random: 0.707 against 0.709 (v2 protocol), or state the model and settings. The
   retake bias is moot after change 1. Rule: EV-8.
7. **Record sync.**
   - Reference: Sensors 22(1):215, 2022, not "2021, Italian National Conference on Sensors" (PROV-10).
   - Align `original_source` (`Website`) with the definition (`Other`).
   - Add an assessment line saying the 2026-10-07 measurement supersedes the comment "subject ID is not unique".
   - Update the 2026-10-07 assessment's "the 17 keep their later image".
   - Rule: records.md.

**Ranked issues**

**1. P2 scope: confirm SEL-15 for temperatures read through a thermal camera, and amend SEL-15 (Must; rule change)**

- **Problem.** The record carries `Wrong Domain / Source Modality`. 27 of 35 features are read from the thermal
  image. The definition keeps the dataset "as an exception", which no Must allows. The record has no CC line, so the
  scope has never been decided.
- **Effect.** If SEL-13 applies, the verdict is `No`, with `Image`, and the folder is removed. If SEL-15 applies, the
  dataset is in scope.
- **For SEL-15 (both sides agree, and so do the practitioner and the precedent checker).** Each column is a
  blackbody-compensated temperature in °C at a named site, the max or the mean of the 4 warmest pixels. The target is
  the same quantity measured by mouth. The source's model is a one-feature calibration on `T_Max1`. IRT devices
  output these readings, and IEC 80601-2-59 names the canthi as the reference site. No images are released.
- **For SEL-13.** satimage and wilt (radiometric values from an imaging sensor) are `No`. SEL-13 lists
  "remote-sensing spectra". Key points were placed by hand for about half the images.
- **Rules.** SEL-13 (Must) against SEL-15 and SEL-14 (Must). On the panel's reading SEL-13 does not apply. This is
  the third keep of image-measured quantities with no written reason, after biomechanical_orthopaedic_prediction and
  dementia_prediction, so an amendment is due (principles, consistency case 4).
- **Decision needed.** (a) Confirm SEL-15 and adopt the amendment the precedent checker drafted: "a physical quantity
  measured through an imaging device at defined sites (a temperature, a volume, an angle), used by the field as the
  instrument's reading, is a measurement (SEL-15), not an image descriptor (SEL-13)". Make satimage and wilt the
  counter-cases. (b) Exclude.
- **Follow-up for (a).** Re-read biomechanical and dementia against the amended rule. biomechanical's own discussion
  argues the other way.

**2. P4 split: a temporal variant on `Date` (SPLIT-3, SPLIT-31; weighing)**

- **Problem.** The task ships IID over people, with no temporal variant.
- **Effect.** IID may be a little optimistic for "calibrate once, use later". No leak is involved.
- **For IID.** Each row is a new person seen once (USE-11). The day's conditions are per-row features (SPLIT-4).
  Averaged over 6 windows, temporal and random training score alike: forest 0.282 against 0.282, ridge 0.310 against
  0.311. The day carries ICC 0.03 of the target. IID is the source's own split.
- **For temporal.** A calibration is fitted before it is used. The set-up changed between the years. A year-1 model
  over-predicts year 2 by 0.07-0.09 °C and is worse on 12-15 of 15 folds. The first year-2 window is up to 16% worse.
  If temporal is chosen, 2 of the 6 windows fall in the 2017-18 flu peak (SPLIT-20 note).
- **Rule.** SPLIT-3: one regime, the one the use case implies. SPLIT-31: an optimistic IID task that matches its
  framing is a candidate for a variant, not a fix. The gap does not decide (SPLIT-4).
- **What would settle it.** Whether the use case is "a new person at a calibrated station" (IID) or "a calibration
  deployed later" (temporal). The mediator recommends IID now and records temporal as a candidate variant.

**Agreed facts**

- **Data.** Raw file: 1,020 rows, SubjectID unique (yymmdd-n), date part equal to Date in 100% of rows. Shipped:
  1,018 rows after dropping the twin pair (170208-03 / 180228-01, 0.01 °C apart over 81 image values; the next pair is
  0.30 °C apart).
- **Retake rows (measured here, settling the blind reviewer's "16").** 17 raw rows have an incomplete round 1, and
  neither twin is among them. 17 shipped rows carry a later image: 13 from round 2, 4 from round 3. Filtering to round
  1 leaves 1,001 rows and 106 of 111 subjects at or above 37.5 °C. It removes 4 of the subjects at or above 38 °C.
- **Timing.** Rounds 2-3 were imaged after the oral thermometer (Zhou 2020 Fig. 2). Mouth sites read +0.41 °C warmer
  from round 2 on. The retake rows are over-predicted by +0.07 to +0.16 °C, depending on the model, and are hard to
  detect (AUC 0.58).
- **Target and leaks.** `aveOralF` is a second encoding of the target (r 0.885) and is dropped. No single input
  predicts the target (R² ≤ 0). `hidden_groups`: 0 hits. `dataset check`: 0/0/0.
- **Signal.** `T_Max1` alone: R² 0.616 (ridge), 0.649 for the best single feature. All features: about 0.70-0.71
  (forest, LightGBM). Target sd 0.51 °C. Fever ranking: AUC 0.96-0.97 at 37.5 °C.
- **Setting.** The study ran at the UMD Health Center, Nov 2016 to May 2018, with 15 min of acclimation. Both papers
  call it a best case.
- **Inputs.** Gender, Age, Ethnicity and Cosmetics are stated by the person, and dropping them costs 0.004-0.009 R².
- **Split measurements.** Grouped by day against random: no measurable difference. The set-up changed between the
  study years. 154 days. February 2018 holds 43 of the 111 febrile subjects.
- **Source copies.** The UCI copy averages rounds 1-4, so ours (round 1) is the source-faithful version (PROV-13).

**Consistency with precedent**

| Precedent | Here | Fact that sets the case apart, or follows |
|---|---|---|
| satimage, wilt (`No`, `Image`) | departs | The readings are the measured quantity (temperature at fixed sites), and the target is the same quantity. They do not serve to recognise image content. The amendment is due (issue 1) |
| biomechanical_orthopaedic_prediction, dementia_prediction (kept, no reason) | same outcome | Neither wrote a reason. Re-read them under the amendment |
| breast_cancer_prediction (SEL-14) | follows | The instrument's reading is what tabular calibrations use in practice |
| bias_correction_r_bias_correction_r_2 (USE-7: drop rows without the input) | follows | Change 1 |
| south_africa_coronary_heart_disease (LEAK-11 keep) | distinguished | There every row's value is post-outcome by design. Here the pre-point input exists for 98.3% of rows and is missing for 17. The issue is USE-7, not LEAK-11 |
| kick, south_africa (fit approximate) | distinguished | After change 1 no potential leak is kept, so `direct` holds under USE-8 and USE-9 |
| airfoil_self_noise, superconductivity (grouped despite a small gap) | distinguished | The query is a new person, not a new set-up. The day's conditions are features (SPLIT-4) |
| amazon_employee_access, bank_marketing (SPLIT-31) | follows | Temporal is a candidate variant (issue 2) |
| aeolus (SPLIT-21) | not applicable | It is about windows and history, not the choice of regime |
| LEAK-19 cases (keep one copy) | departs with a stated reason | The two codes conflict on date, ethnicity and room readings, so both are dropped. Kept |
| corporate_credit_rating (unit slip) | consistent | The Distance repair has strong same-day evidence |

</details>

<details><summary>Claim audit</summary>

Adversary of `datasets/_dev/tabarena-v0pt2/infrared_thermography_temperature/` (DEF = `dataset.py`, REC = the record).
Models: 30 shipped splits, RF 300 trees, LightGBM default, RidgeCV, a 4-knot linear spline of `T_Max1`, an
additive spline model; past-only against random training sets for the temporal claims. Papers: Zhou et al. 2020
(PMC7486803, incl. Fig. 2 flowchart), Wang et al. 2022 (PMC8749858), PhysioNet page.

**Table**

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 2 | Use case: an entrance camera images a person once; "(the FDA study's setting)" | DEF task_summary.use_case | Read Zhou 2020 Methods/Discussion, Wang 2022 Sec. 4.5 | **refuted (the parenthesis)** | The study ran at the UMD University Health Center; each subject waited 15 min to precondition, was seated, faces cleared, tripod adjusted, absorbing backdrop, blackbody; Zhou: "the results presented here likely indicate a best-case performance level"; Wang 2022: "our study may represent a best-case scenario". Not an entrance, not one look. | USE-1, USE-8 |
| 3 | Row: "place and years not stated" | DEF task_summary.row | Zhou 2020 Methods; `Date` | **refuted** | Zhou 2020: "Over the course of 18 months - from November 2016 to May 2018 - ... at the University Health Center of the University of Maryland (UMD) at College Park"; Date 2016-11-17 to 2018-05-14 | writing.md, EV-2 |
| 4 | Target sd about 0.5 °C | DEF predicted | std | holds | 0.510 | - |
| 5, 11 | Everything in `known` is known at the prediction point | DEF known, bullet 1 | Fig. 2 order; retake rows | **refuted for 17 rows (1.7%)** | Fig. 2 (Zhou 2020): round 1 = thermal imaging, then oral thermometer (reference), then NCITs; rounds 2-3 imaged after that thermometer. 17 shipped rows (13 round 2, 4 round 3) carry such an image. All other inputs: holds. | LEAK-10, USE-3, USE-7 |
| 7 | changes: "We keep only the first image, taken before the thermometer" | DEF task_summary.changes | `first_complete_image` | **refuted (wording)** | 17 rows carry a round-2/3 image taken after the first oral reading; the curation notes say so, the summary does not | writing.md |
| 8 | fit = direct | DEF fit | USE-8 definition against facts | **refuted** | USE-8 lists "a potential leak kept on purpose" as approximate (kick); the 17 post-thermometer images are kept on purpose. Also the controlled clinic setting (claim 2) and four inputs the camera does not see (claim 9). | USE-8 (Must) |
| 9 | fit_reason: "The camera has all these values at one look" | DEF fit_reason | Which inputs come from the camera; drop them | **refuted** | Gender, Age, Ethnicity, Cosmetics are stated by the person, not seen. Dropping them: R² -0.0047 (RF, SE 0.0005), -0.0087 (LGBM, SE 0.0021), -0.0036 (ridge, SE 0.0010); also dropping TimeOfDay: -0.0083 / -0.0105 / -0.0052 | USE-8, USE-3 |
| 10 | 1,020 subjects, four rounds, two oral readings | DEF intro | raw | holds | 1,020 rows, SubjectID unique | - |
| 12 | Round 1 kept; rounds 2-4 after the thermometer; both papers round 1 only; UCI `*_1` average the rounds | DEF bullet 2 | Fig. 2; paper quotes; UCI `data.csv` against raw | holds | Fig. 2 order; Zhou: "Images from the second to fourth rounds ... were omitted ... to better approximate a realistic screening scenario"; Wang 2022: "All analysis ... based on ... the first round". UCI `T_Max1` equals the nan-mean of rounds 1-4 to 3e-8 (differs from round 1 by up to 1.13 °C) | PROV-13, EV-2 |
| 13 | 17 retakes: over-predicted by 0.07-0.14 °C; RMSE 0.33-0.39 kept vs 0.77-0.90 missing; 5 febrile | DEF bullet 3 | 30 shipped splits, pooled over retake test rows | holds, range slightly off | bias ridge +0.071, RF +0.134, LGBM +0.158 (claim's upper end 0.14 exceeded by LGBM; depends on settings); RMSE kept 0.327/0.341/0.389, missing 0.782/0.817/0.882; 5 of 17 at ≥ 37.5 °C. Unwritten: missing round 1 goes with fever (5/17 vs 106/1001, Fisher p 0.030). Round-1 rows: bias -0.002 to -0.007 | EV-8, LEAK-11 |
| 14 | Target aveOralM monitor mode; aveOralF a re-measurement of the target | DEF bullet 4 | PhysioNet, Zhou | holds | PhysioNet: "only data from the monitor mode were used"; Zhou: Tref = mean of two monitor readings "during rounds 1 and 3"; corr(F, M) 0.885 | LEAK-10, USE-5 |
| 15 | "A screening thermograph measures all four" (T_atm, Humidity, Distance, T_offset1) | DEF bullet 5 | literature check | untested (no source for humidity/distance as a camera output) | Blackbody offset is a camera/setup reading (Zhou: BB compensation). Room T and RH are recorded by the deployment per ISO/TR 13154, not by the thermograph. Cost of dropping the four (2026-10-07 run, 30 splits): RF -0.005, LGBM -0.017, ridge -0.015 R² | USE-3, EV-7 |
| 16 | SubjectID = date + number; dropped with Date | DEF bullet 6 | raw | holds | date part equals Date in 100% | LEAK-10 |
| 17, 36 | 170208-03 / 180228-01 one measurement; both dropped | DEF bullet 7, Decision 4 | max abs diff over all 81 round-1-3 values, every raw pair | holds | twins 0.01 °C; next closest pair 0.30 °C (171013-10, 171205-08), then 0.36 | LEAK-16, SPLIT-29 |
| 18 | Distance 79.0 is cm | DEF bullet 8 | raw | holds | 170208-17, same day 0.60-0.77 | CLEAN |
| 19, 29 | Each subject once; source calibrated on random 60% | DEF bullet 9, splits_comment | Wang 2022 Sec. 2.5 | holds | "randomly separated ... 60% of the subjects, 612 and 606" | EV-2 |
| 21, 52 | Day-grouped folds score the same (RF 0.709 vs 0.711) | DEF bullet 9 | day-grouped probe | holds in direction, numbers not reproduced | 0.707 vs 0.709 (-0.003, SE 0.003); ridge +0.004 (SE 0.002) | EV-8, SPLIT-4 |
| 22 | hidden_groups finds no hit | DEF bullet 9 | probe | holds | 0 hits | - |
| 23 | Past-only training instead of random same-size set: RMSE -0.2% to +2.5% | DEF bullet 10 | re-run, 10 random draws per window | holds (approx.) | 6 windows: ridge -0.09%, RF -0.07% (3/6 worse); 10 windows: ridge -0.30%, RF +1.19% (7/10 worse). Year-1 calibration on year 2 vs a year-2 calibration: ridge +3.3%, RF +5.6% | SPLIT-4, SPLIT-7 |
| 24, 55 | Segmented calibration RMSE 0.277; additive 0.265, better on 28/30 | DEF bullet 11 | re-run | holds | 0.2774 vs 0.2647, 28/30. Caveat: "the source's" calibration is our 4-knot quantile linear spline; Wang 2022 gives no knots (its own test-set A_rms for T_max, IRT-1: 0.29) | TP-2, EV-8 |
| 25 | Age 21-30 for 10 subjects | DEF bullet 12 | counts | holds | 10 | CLEAN |
| 26 | aveOralM on 0.05 grid shifted -0.01 | DEF bullet 12 | residue of cents mod 5 | holds | all 1,018 end in 4 or 9 hundredths | - |
| 27 | Release holds no images | DEF bullet 13 | PhysioNet file list | holds | six CSVs, two tables, license | SEL-13 to SEL-15 (call open) |
| 30 | Wang 2022 Sec. 4.5 random split may bias upwards | splits_comment | text | holds | "the performance estimates may be biased (upwards)" | - |
| 31 | 96-99% of test subjects share their day with train | splits_comment | prep | holds | 95.9-99.4% | - |
| 33 | Decision 1: mouth warmer from round 2 because of the thermometer | Decision 1 | Fig. 2; rise of T_OR vs canthi | holds | T_OR +0.41 °C vs canthiMax +0.06 °C (difference 0.349, SE 0.013, 2026-10-07 run); thermometer sits between round-1 and round-2 images | EV-6 |
| 34 | Decision 2: source counted the 17 in its round-1 analysis (Zhou 2020 Table 5) | Decision 2 | which group the 17 are in; source counts | holds only circumstantially | Zhou analysed group 1 only (544; 47 febrile = FLIR_group1.csv's 47); 11 of the 17 are in group 1, 6 in group 2 (counted by Wang 2022's 1,020). Counts do not say which image the source used for them | EV-6 |
| 35 | Day table numbers | Decision 3 | generated by `_decisions` from the code | holds (by construction; 154 days, 1-15, median 6) | - | - |
| 37-42 | Metadata, licence, download, bibtex | DEF | prep | holds | - | PROV |
| 43 | REC `original_source: Website` | REC | vs DEF `Other` | mismatch (vocabulary) | - | - |
| 48 | "subject ID is not unique" | REC comment | raw | refuted (superseded by the 2026-10-07 assessment) | unique in 1,020 rows | - |
| 57 | REC Reference: 2021, "Italian National Conference on Sensors" | REC | bibtex / MDPI | refuted | Sensors 22(1):215, 2022 | PROV-10 |
| implied | No row is a copy across the split | definition | 81-value pair distance | holds | see 17 | LEAK-16 |
| implied | Each row a distinct person | row | - | untested | SubjectID is a visit code; one visit was stored twice; a repeat volunteer on another day cannot be detected from the release | LEAK-17 |
| implied | Target is the real-world target | definition | papers | holds | the reference the calibration and fever decision use | USE-5 |
| implied | The split is the one the use case needs | splits | 23 and 21 | holds for "new people, same set-up"; a calibration used later costs +3-6% (year shift) | SPLIT-7 call stays with the curator | SPLIT-4, SPLIT-7 |

**Refuted and untested, ranked (principles.md: validity first, Must first)**

1. **P3, USE-7 (Must) with LEAK-10 (Must) against the 17 retake rows (claims 5, 11, 13).** USE-7: "A row that lacks
   the input the prediction acts on is no task row: drop it rather than keep it as missing." The definition neither
   drops nor leaves them missing; it substitutes an image taken after the thermometer (Fig. 2), i.e. after the
   prediction point. LEAK-11 (Should, narrows LEAK-10) lets a post-outcome value that weakens the signal stay with a
   note, and it does weaken (bias +0.07 to +0.16 °C, retake RMSE 0.33-0.39 against 0.27), but LEAK-11 narrows LEAK-10,
   not USE-7, and the "source counted them" defence is circumstantial (claim 34). What it changes: 17 rows (5 of 111
   febrile). Mildest remedy: drop the 17 rows (fix the definition: filter `round == 1`), or keep them only with an
   explicit exception to USE-7 naming the fact (the source's cohort) and serving P3/P6. Curator call.
2. **P3, USE-8 (Must): `fit = direct` (claims 8, 9, 2).** By USE-8's own list, a potential leak kept on purpose is
   approximate; the study's controlled clinic (15-min acclimatisation, seated, backdrop; "best-case" per both papers)
   is not an entrance; four inputs are stated by the person, not seen by the camera. What it changes: the fit label
   and the use-case text, not the data. Mildest remedy: rewrite `use_case` to the study's setting (a screening station
   after acclimatisation, the person answers an intake question) and either set `fit = "approximate"` naming the
   retake rows (if kept) or drop the retakes and keep direct; fix `fit_reason`. Dropping the four person-stated inputs
   costs 0.004-0.009 R² if the curator prefers a camera-only task.
3. **Writing (procedure): `changes` (claim 7) and `row` (claim 3).** `changes` hides the 17 later images; `row` says
   place and years are not stated, while Zhou 2020 states UMD Health Center, Nov 2016 - May 2018. Remedy: edit the two
   strings.
4. **Untested: claim 15** ("a screening thermograph measures all four"). The room readings come from the deployment,
   not the camera; the claim needs rewording ("the screening station records"), and the inputs stay (USE-6). Effect
   of dropping them ≤ 0.017 R².
5. **Numbers (EV-8): claim 13** (bias 0.07-0.14; LGBM gives 0.158 here) and **claim 21** (0.709 vs 0.711; 0.707 vs
   0.709 under the v2 protocol). Remedy: give the model and settings, or the reproduced numbers.
6. **Untested implied: one person per row.** Not decidable from the release; note only.
7. **Record (claims 43, 48, 57):** Reference block year and venue wrong, `original_source` vocabulary, superseded
   screening comment. Remedy: a record sync.

Held under attack: no copy across the split (twins dropped, next pair 0.30 °C over 81 values), round 1 as the
prediction point, UCI averaging, target choice, day-grouping and temporal gaps small (-0.3% to +1.2%), non-trivial
(28/30). The split regime and the modality marker remain weighing calls (SPLIT-7; SEL-13 to SEL-15), not refuted.

</details>

<details><summary>Column audit</summary>

Frame: `dataset_io.from_definition` (origin `definition`, regime `iid`), 1,018 rows x 36 columns (35 features + target).

Prediction point (curation_comments bullet 1): a screening thermograph images a person once and estimates the oral
temperature from that image (facial temperatures, blackbody offset), the room, the distance, the time of day and what the
person states. `task_summary.use_case`: an entrance camera images a person once. `fit = direct`, `fit_reason`: "The
camera has all these values at one look".

Codebook: PhysioNet `_Table1.pdf` (26 facial variables) and `_Table2.pdf` (other variables).
Procedure: Zhou et al. 2020 (JBO 25:097002) Fig. 2 and Sec. 2.1-2.3: four rounds in about 15 min; round 1 = thermal
imaging, then the first oral reading (monitor mode after 3 min), then NCITs; round 2 imaging; round 3 imaging, then the
second oral reading; round 4 open mouth. Tref = mean of the monitor-mode readings of rounds 1 and 3. Every pixel is
already compensated with the blackbody offset (T_off = T_Bset - T_Bmeas, Sec. 2.3.1); Wang 2022 Sec. 2.1: "An IRT system
(also known as a screening thermograph) is composed of an IRT and an ETRS".

**Column table**

All 26 facial columns: °C, radiometric, blackbody-compensated, from the round-1 image (taken before the thermometer) for
1,001 rows and from the round-2 (13) or round-3 (4) image for 17 rows (see problem 2). None has missing values, proxy
codes or impossible values; the hierarchy maxima hold in every row (T_Max1 >= every other site max, *_Max >= the
4-pixel mean, T_RC1 >= max(Dry, Wet), etc.); unusual lows stay (T_FHTC1 27.7, aveAllR13_1 29.95, 4 rows, CLEAN-11).

| column | meaning (codebook) | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| T_offset1 | set minus measured blackbody temperature of the image (Table 2; Zhou 2020 Sec. 2.3.1); already added to every pixel | yes: read from the in-frame blackbody of the same image; part of a screening thermograph (Wang 2022 Sec. 2.1) | float, -0.76 to 3.58, no missing; retake rows carry their round's offset (consistent) | fine (v1 had dropped it as lab-only; the papers' definition of a screening thermograph includes it) | USE-6, LEAK-37 |
| Max1R13_1 | max in a 13-px circle, right canthus to centreline (T_CRmax) | yes (image), except 17 retake rows | float, ok | fine; retake rows: problem 2 | LEAK-10/11, USE-7 |
| Max1L13_1 | same, left (T_CLmax) | same | float, ok | fine; problem 2 | same |
| aveAllR13_1 | mean in the right 13-px circle | same | float, ok; one low 29.95 kept | fine; problem 2 | same, CLEAN-11 |
| aveAllL13_1 | mean in the left 13-px circle | same | float, ok | fine; problem 2 | same |
| T_RC1 | right canthus 24x24 square, mean of 4 hottest px | same | float, ok | fine; problem 2 | same |
| T_RC_Dry1 | right canthus dry area 16x24, 4 hottest px | same | float, ok (equals T_RC1 in 48% of rows, a by-construction overlap, not a copy) | fine; problem 2 | same, CLEAN-5 not triggered |
| T_RC_Wet1 | right canthus wet area 8x24, 4 hottest px | same | float, ok | fine; problem 2 | same |
| T_RC_Max1 | right canthus square, max | same | float, ok | fine; problem 2 | same |
| T_LC1 | left canthus square, 4 hottest px | same | float, ok | fine; problem 2 | same |
| T_LC_Dry1 | left canthus dry area, 4 hottest px | same | float, ok | fine; problem 2 | same |
| T_LC_Wet1 | left canthus wet area (codebook says 16x24, a typo for 8x24) | same | float, ok | fine; problem 2 | same |
| T_LC_Max1 | left canthus square, max | same | float, ok | fine; problem 2 | same |
| RCC1 | 3x3 px at the right canthus point, mean | same | float, ok | fine; problem 2 | same |
| LCC1 | 3x3 px at the left canthus point, mean | same | float, ok | fine; problem 2 | same |
| canthiMax1 | extended canthi area, max (T_CEmax) | same | float, ok; below T_RC_Max1 in 20 rows and T_LC_Max1 in 24 (different regions, not impossible) | fine; problem 2 | same |
| canthi4Max1 | extended canthi area, 4 hottest px | same | float, ok | fine; problem 2 | same |
| T_FHCC1 | forehead centre 3x3, mean (T_FC) | same | float, ok | fine; problem 2 | same |
| T_FHRC1 | forehead right 3x3, mean | same | float, ok; 3 lows near 30 kept | fine; problem 2 | same |
| T_FHLC1 | forehead left 3x3, mean | same | float, ok | fine; problem 2 | same |
| T_FHBC1 | forehead bottom 3x3, mean | same | float, ok | fine; problem 2 | same |
| T_FHTC1 | forehead top 3x3, mean | same | float, ok; min 27.7 (hairline) kept | fine; problem 2 | same |
| T_FH_Max1 | extended forehead area, max | same | float, ok | fine; problem 2 | same |
| T_FHC_Max1 | forehead centre 3x3, max | same | float, ok | fine; problem 2 | same |
| T_Max1 | whole face, max (T_max; the source's calibration input) | same | float, ok | fine (best single feature, R^2 0.649; the task's natural core, not a leak) | EV-3, TP-4; problem 2 |
| T_OR1 | mouth region, 4 hottest px | yes in round 1 (before the thermometer); in the 13 round-2 retakes after it (mouth +0.41 °C round 2 vs 1, Decision 1) | float, ok | fine for 1,001 rows; the column most affected in the retake rows | LEAK-10/11, problem 2 |
| T_OR_Max1 | mouth region, max | same as T_OR1 | float, ok | same as T_OR1 | same |
| aveOralM (target) | mean of the two monitor-mode oral readings (rounds 1 and 3) | target | float, 35.54-40.34, no missing; 0.05 °C grid shifted -0.01 (documented) | fine | USE-5 |
| Gender | male or female (Table 2) | stated, not imaged: an entrance camera does not have it | categorical, 2 levels, ok | question: fit (problem 1) | USE-1, USE-8 |
| Age | age range, HIPAA bins, >60 pooled (Table 2; PhysioNet Methods) | stated, not imaged | categorical, 8 levels, unordered; overlapping bin 21-30 (10 rows) kept with a note | question: fit (problem 1); cleaning: ordered bins stored unordered, overlap documented, no action | USE-8, CLEAN-14, CLEAN-12 |
| Ethnicity | 7-level list (Table 2; 6 present, Native Hawaiian absent) | stated, not imaged | categorical, 6 levels (one of 4 rows), ok | question: fit (problem 1) | USE-8 |
| T_atm | ambient temperature, °C | yes: room sensor at the time of imaging | float, 20.2-29.1, ok | fine; identifies the measurement day (ICC 0.81), see problem 3 | USE-6, SPLIT-31 |
| Humidity | relative humidity, % | yes: room sensor | float, 9.9-61.2, ok | fine; identifies the day (ICC 0.97), problem 3 | USE-6, SPLIT-31 |
| Distance | subject-to-IRT distance, m | yes: set-up, fixed before imaging | float, 0.54-0.92, 2 missing (target not related: 0 of 2 febrile); one 79.0 cm fixed to 0.79 m; 448 rows at exactly 0.60 (the set position, not a proxy code) | fine | CLEAN-21, CLEAN-10 not triggered |
| Cosmetics | "1" cosmetics applied, self-reported (Table 2) | stated, not imaged | float 0/1, 29 missing (3.4% febrile vs 11.1%, n = 29: weak, probe 3 not flagged); 278 of 589 women vs 34 of 400 men | question: fit (problem 1); dtype fine (binary numeric) | USE-8, LEAK-10 probe 3 |
| TimeOfDay | `Time`, "time when the data were collected", as decimal hour | yes: clock at the visit | float, 8.53-17.30, ok; corr. 0.14 with the target (circadian, real signal) | fine | CLEAN-14 |
| dropped: SubjectID, Date | yymmdd-n code from the date; date | yes, but SubjectID is an id (CLEAN-3); Date kept off under IID | dropped | fine (Date would be the time axis of a temporal variant, REVIEW issue 1) | CLEAN-3, LEAK-33 |
| dropped: aveOralF | fast-mode mean of the same two readings | no: a second measurement of the target | dropped | fine (leak removed) | LEAK-10 |
| dropped: rounds 2-4 | images after the first oral reading; round 4 open mouth | no | dropped (except the 17 retake rows) | fine | LEAK-10 |

**Problems, ranked (principles.md)**

**1. P3, use case and fit: four stated inputs against "the camera has all these values at one look" (question for the curator)**

`Gender`, `Age`, `Ethnicity`, `Cosmetics` are what the person states (Table 2: Cosmetics "self-reported"); the
prediction point in curation_comments bullet 1 includes "what the person states", but `use_case` ("a fever-screening
thermal camera images a person once") and `fit_reason` ("the camera has all these values at one look") do not, and
`fit = direct`. The written use case is the test of every column (USE-1); as written, these four are not known to the
actor. Not a leak: all four exist before the measurement and none predicts the target alone (leak probe R^2 <= 0).
Cost of dropping them: R^2 0.703 -> 0.698 (2026-10-07 run, 30 splits, forest).
Mildest remedy, in order: (a) write the use case as a screening with a short intake (sex, age group, cosmetics asked at
the desk) if that is a practice the curator accepts, without rephrasing only to excuse the gap (USE-9, weighed factor);
(b) keep the columns and set `fit = approximate`, naming the gap (USE-8); (c) drop the four (ethnicity is the least
plausible screening input). Rules: USE-1, USE-3, USE-8, USE-9.

**2. P4, prediction point: the 17 retake rows carry an image taken after the first oral reading (question; open issue 2, with one new rule)**

Code: `first_complete_image` in `_clean`. Raw: 16 of the 17 rows lack the whole round-1 image (27 of 27 values), one lacks
23 of 27 (its 4 present round-1 values are overwritten too, which keeps one image per row: fine). 13 rows take round 2,
4 take round 3; both were imaged after the thermometer had been under the tongue (Zhou 2020 Fig. 2), and the round-3
image falls between the two readings that make the target. Measured here (shipped splits, 3 repeats, OOF): forest
over-predicts them by +0.137 °C (others -0.003), ridge +0.073; RMSE 0.352 / 0.323 against 0.274 / 0.294 on the other
rows. So the post-reading values weaken the signal: LEAK-11 (Should, narrows LEAK-10) allows keeping them with a note,
which the definition does (Decision 2, bullet 3). Not raised before: USE-7 (Must) says a row that lacks the input the
prediction acts on is no task row and is dropped rather than kept as missing; for 16 rows the round-1 image is exactly
that input, and an entrance retake would not follow an oral thermometer, so the substituted image does not mirror the
use case. Leaving them missing is ruled out either way (29% febrile vs 10.6%: missingness that encodes the outcome,
LEAK-10). Mildest remedies: (a) keep with the LEAK-11 note and correct `task_summary.changes` ("we keep only the first
image, taken before the thermometer" is false for 17 rows; fit at most approximate); (b) drop the 17 (USE-7; loses 5 of
111 febrile subjects). The curator's call between LEAK-11 and USE-7.

**3. P4, split: the room columns identify the measurement day under IID (fine, no action)**

`Humidity` (day ICC 0.97), `T_atm` (0.81), `Distance` (0.66), `T_offset1` (0.37) fingerprint the day, and the day carries
part of the calibration offset (ICC 0.14 for aveOralM - T_Max1); 96-99% of test subjects share their day with a training
subject. Dropping `Date` therefore does not hide the day. Measured cost: none (day-grouped vs random, forest -0.003 +-
0.003, ridge +0.004 +- 0.002, v2 grouped protocol). All four are legitimately known at imaging (USE-6). This is
the regime question of REVIEW issue 1 (SPLIT-31), not a column leak.

**4. P7, cleaning (fine or noted; no change needed)**

* `Age`: ordered bins stored as an unordered category, with the overlapping source bin 21-30 (10 rows) kept and
  documented (CLEAN-14, CLEAN-12; a remap would invent information).
* `Distance`: the 79.0 cm fix is right (CLEAN-21); 448 rows at exactly 0.60 m are the set position, not a proxy code.
* `Cosmetics` 0/1 float is a lossless binary; its 29 missing stay missing (CLEAN-10, CLEAN-2).
* No identifier survives, no column is an exact copy of another (largest equal share 64.5%, T_LC1 vs T_LC_Dry1, by
  construction), no all-row statistic in `_clean` (CLEAN-7).
* Codebook typo: `T_LC_Wet` is described as 16x24 px (the right side says 8x24); nothing to do.

Judgment record:

```text
Verdict: ship after the curator's two calls.
Validity: USE-1/USE-8 question (four stated inputs against a camera-only use case and fit direct); LEAK-10 holds for
  aveOralF, rounds 2-4, SubjectID, Date (dropped); LEAK-11 vs USE-7 question for the 17 retake rows (measured: weakens,
  +0.07-0.14 °C bias); SPLIT-31 note (room columns identify the day; no gap measured).
Value: not re-examined here (TP probes: no flag).
Quality: CLEAN-11, CLEAN-14, CLEAN-21 hold; Age overlap kept with a note.
For the curator: problem 1 (fit wording or drop four columns), problem 2 (keep with note and fix `changes`, or drop 17).
```

</details>

<details><summary>Split audit</summary>

Verdict: **right with notes.** IID over subjects (10 x 3 random folds) is defensible: each person is in the file once
and the use case is a new person at an entrance (USE-10, USE-11). The open point is temporal against IID (SPLIT-1,
SPLIT-3): a screening calibration is fitted first and used on later people, and the set-up changed between the two
study years. On these data the regime costs almost nothing on average, and SPLIT-4 says the gap does not decide, so it
stays the curator's call. It is not a defect.

Models: ridge (one-hot, standardised), random forest (300 trees), LightGBM (300 rounds). Metric: RMSE in °C.

**Facts checked**

* **Regime declared:** IID, no `grouping`, no `temporal`. Shipped splits: 30 (10 x 3), train 678-679, test 339-340.
* **Entity:** `SubjectID` (yymmdd-n) is unique in all 1,020 raw rows. The one measurement stored under two codes
  (170208-03 and 180228-01, a year apart) is dropped, so no person appears on both sides. The hidden-group probe found
  0 candidates and near copies at 0.85 for 0.2% of rows. Exact feature copies across the split: 0.0% (leak probe).
* **Time axis:** the dropped `Date` (= the yymmdd of `SubjectID` in 100% of rows) runs from 2016-11-17 to 2018-05-14,
  over 154 days with 1-15 subjects each. Measurements happen only from October to May. Year 1 (2016-11 to 2017-04)
  has 394 subjects, year 2 (2017-10 to 2018-05) has 624.
* **Label delay:** none. The oral reading follows the image by minutes, so SPLIT-9 and SPLIT-10 (gap) do not apply
  under any regime.
* **Set-up drift by month:** the median distance falls from 0.80 m (2016-11/12) to 0.70 m (2017-02 to 04) and 0.60 m
  (from 2017-10). Wang 2022 Sec. 2.4 names two locations. February 2018 holds 173 subjects and 43 of the 111 febrile
  subjects (flu season).
* **Day as a session:** 95.9-99.4% of each fold's test subjects share their day with a training subject (claim
  checks). The day carries ICC 0.03 of the target and 0.14 of the calibration offset `aveOralM - T_Max1`, and the room
  readings identify it (Decision 3).

**Measurements**

1. **Random against grouped by day** (10 repeats with shuffled day-to-fold assignment, 3 folds; RMSE mean ± SE over
   30): ridge 0.296 ± 0.003 against 0.298 ± 0.002; forest 0.2733 against 0.2733; LightGBM 0.277 against 0.278. With
   the v2 grouped protocol, R² is 0.707 against 0.709 for the forest and 0.657 against
   0.653 for ridge. Grouping by day makes no measurable difference.
2. **Temporal, expanding**: 6 windows by unique day over the newest 77 of 154 days. Each window has 68-122 test rows
   and 3-27 febrile subjects (75 in total). Trained on all earlier days, compared with a random training set of the
   same size drawn from every row outside the window (5 draws):

   | window | n test | febrile | ridge | forest | LightGBM | bias (forest, °C) |
   |---|---|---|---|---|---|---|
   | 2017-10-27..11-21 | 86 | 9 | +2.5% | +5.0% | +16.3% | +0.10 |
   | 2017-11-27..2018-01-25 | 79 | 3 | -2.4% | -0.2% | +4.4% | +0.09 |
   | 2018-01-26..02-14 | 122 | 24 | -0.1% | -5.6% | -7.0% | +0.01 |
   | 2018-02-15..03-06 | 115 | 27 | -1.8% | +1.8% | +1.1% | +0.01 |
   | 2018-03-07..04-12 | 84 | 5 | +1.6% | +3.3% | -0.5% | +0.02 |
   | 2018-04-13..05-14 | 68 | 7 | 0.0% | -1.2% | -1.7% | +0.04 |

   Test-weighted RMSE over the windows, temporal against random training sets: ridge 0.310 against 0.311, forest
   0.282 against 0.282, LightGBM 0.291 against 0.287. On average the temporal regime costs about nothing. The first
   window after the set-up change (the start of year 2) is the exception: every model over-predicts it by 0.10-0.12 °C
   and is up to 16% worse.
3. **A year-1 calibration used on year 2** (year 2 split into 3 parts by day, 5 repeats; compared with a random
   training set of 394 rows drawn from outside the test part): ridge +1.9%, forest +2.3%, LightGBM +8.2%. The year-1
   model is worse on 12, 12 and 15 of 15 folds and over-predicts by 0.07-0.09 °C. This matches the earlier run's
   +3% to +9% and over-prediction of 0.06-0.08 °C.

**Problems, ranked**

1. **P4, SPLIT-1 / SPLIT-3 / USE-10 (Must, a weighing call on which regime): IID against temporal.** *Evidence:* the
   use case is a camera calibrated beforehand that screens people who come later. Under the IID split, 96-99% of test
   subjects have a same-day training subject. The set-up changed between years (distance 0.80 -> 0.60 m, two
   locations), and a year-1 calibration over-predicts year 2 by 0.07-0.09 °C and is worse on 12-15 of 15 folds.
   *Against:* each row is an independent person seen once (USE-11), not a signal stream (so SPLIT-7 does not apply).
   The source calibrated on a random 60% (Wang 2022 Sec. 2.5, with the upward-bias caveat of Sec. 4.5), which is a
   claim to check under SPLIT-5 and SPLIT-19 and holds on these data. Averaged over windows, temporal costs about 0%
   (measurement 2). Under SPLIT-4 the size of the gap does not decide either way. Under SPLIT-31, IID matching the
   source's framing while possibly a little optimistic makes this a candidate for a temporal variant, not a fix.
   *Mildest remedy if the curator picks temporal:* re-split with `Temporal(on="Date")` on the date from `SubjectID`,
   expanding windows over the newest half with no gap (zero label delay). Use about 6 windows of 68-122 rows each
   (SPLIT-14 and SPLIT-17 hold), and keep `Date` out of the features. With IID kept, no change is needed beyond the
   notes below.
2. **P4, SPLIT-20 / SPLIT-21 (Should): the evidence about time rests on few windows, and the claim is not robust.**
   `curation_comments` bullet 10 says expanding windows change RMSE by "-0.2% to +2.5%". With three models and the
   same window layout I get -7.0% to +16.3% (forest -5.6% to +5.0%). The range depends on the model and on the random
   pool. SPLIT-21 forbids deciding the regime from a few windows, and the bullet reads as if it did. *Remedy:* restate
   it as a range over models ("about 0% on average; the first year-2 window is 2-16% worse, bias +0.1 °C"), and
   ground "not temporal" in the use case (USE-11, SPLIT-4), not in the comparison.
3. **P4, SPLIT-20 (Should, only if temporal is chosen): a season-shaped test window.** Windows 3 and 4 (late January
   to early March 2018, the flu peak) hold 51 of the 75 febrile test subjects of the newest half, and February 2018
   alone holds 43 of all 111. Measurements only run from October to May. *Remedy:* keep 6 windows and say in
   `splits_comment` that two of them fall in the 2017-18 flu peak. Do not narrow the windows.
4. **P4, SPLIT-29 / SPLIT-30 (pass, note): the measurement day as a hidden session.** The day is not an entity with a
   label (target ICC 0.03, p 0.078). It identifies itself through the room readings, which are legitimate per-row
   features (SPLIT-4: new rows keep having them). Grouping by day changes RMSE by at most 0.002 (measurement 1). No
   re-split for the day. The `splits_comment` already states the day sharing (96-99%), which holds (95.9-99.4%).

**Claims in the split text checked**

* "96-99% of the test subjects of a fold share their day with a training subject": holds (95.9-99.4%).
* "folds grouped by day ... score the same": holds (forest RMSE 0.2733 against 0.2733; ridge 0.296 against 0.298).
* "random forest R^2 0.709 against 0.711" (curation_comments): the v2 grouped probe gives 0.707 random against 0.709
  by day. The direction holds and the exact numbers depend on the forest's settings.
* `task_summary.split` "new people screened with the same set-up": accurate. It is the IID framing, and it should
  say that the set-up changed between the two study years if IID stays (the summary currently mentions only the day
  sharing).
* Temporal "-0.2% to +2.5%": not reproduced with other models (problem 2).
* Year-1 calibration on year 2, "+3% to +9%, worse on 11-14 of 15" (REVIEW_before): reproduced, +1.9% to +8.2%,
  worse on 12-15 of 15.

</details>

<details><summary>Domain practitioner</summary>

Reviewer role: the person who calibrates and deploys a fever-screening infrared thermograph (IRT), for example a
device maker or an FDA evaluator fitting the mapping from facial temperatures to the reference oral temperature, and
the clinic that runs it to decide who goes to a second check with a contact thermometer.

**Verdict**

**Fit: direct, but for a clinic triage station, not for "an entrance".** The rows, the round-1 features and the oral
reference mirror exactly the calibration an IRT maker fits and the source evaluates (USE-8, USE-9); the written
`use_case` places it at an entrance, a setting the data does not mirror (15 min acclimation in a draft-free clinic
room, 95% of people under 30), so either the use_case is rewritten to the source's setting or the fit becomes
approximate.

**How the decision is made today (source and domain)**

- The study ran at the University of Maryland Health Center, College Park, Nov 2016 to May 2018; subjects were
  "preconditioned by waiting for at least 15 min in the draft free study area"; four rounds within about 15 min, each
  with two IRTs, six NCITs and a contact oral thermometer (Wang et al. 2022, Sec. 2).
- Calibration: oral temperature regressed on one skin temperature (constant offset, linear, Deming, weighted, binning,
  segmented), on a random 60/40 split. Evaluation: clinical bias, RMS difference, repeatability, and sensitivity /
  specificity at 37.5 °C with ROC AUC. Inner canthi and full-face maximum are best; forehead worse.
- Sec. 4.5: random splitting of one pool may bias estimates upward; "our study may represent a best-case scenario".
- IEC 80601-2-59 names the inner canthi as the reference site; ISO/TR 13154 asks for 20-24 °C ambient (the study ran
  20-29 °C). A blackbody (SR-33) is the drift reference: `T_offset1` is a value the device has.
- PhysioNet: 95% under 30, about half 18-21, "not representative of the age of the overall population"; 76 subjects
  with motion-blurred images and 56 with inconsistent oral readings were excluded before release.
- Key points were placed by image registration plus manual labelling (Wang 2022; Zhou 2020 Sec. 2.2 says about half by
  hand).

**The four questions, as the actor**

1. **Inputs at the prediction point (USE-3, USE-6).** The 26 facial temperatures, the blackbody offset, room temperature,
   humidity, distance and time are all on the device at the moment of the image: yes. Sex and age group I could
   estimate or ask. Ethnicity and cosmetics I would not ask at a screening point, though a clinic intake form might
   have them. My probe (3x3 CV) shows they do not matter: RF RMSE 0.273 with them,
   0.275 without, 0.279 from the image alone; ridge 0.296 / 0.298 / 0.305. Nothing I would always have is missing,
   except the visible-light image and the automatic face detector, whose errors the hand-placed key points hide. The
   17 retake rows (image after the oral thermometer) are the only timing problem; see gap 4.
2. **Target (USE-5).** I act on "above 37.5 °C: send to second check". The device displays an estimated body
   temperature and the operator applies the threshold, so a number in °C is what the device outputs and what the
   standard measures it on: the regression target is the right one, not a proxy. The monitor-mode oral mean is the
   clinical reference both papers use. A probability of fever would be a second, valid task; the regression keeps the
   information. On the shipped data the regression ranks fever well: AUC at 37.5 °C 0.96-0.97, sensitivity 0.71-0.77 at
   specificity 0.98-0.99 when the raw prediction is thresholded at 37.5 (11% febrile, 4.8% at 38 °C). RMSE weights the
   afebrile majority, which is what a calibration's bias and Arms do too.
3. **Row and test data (USE-10, USE-11).** One row is one person imaged once: one decision. Each person is new (cold
   start, no history), and each is in the file once, so IID over people is right. What I would face is a calibration
   fitted once and used next month or at another site; the curation's probes show a temporal or day-grouped split
   changes RMSE by -0.2% to +2.5% and R^2 by < 0.004, and a year-1 to year-2 transfer by +3% to +9%. A new site is not
   in the data. The IID split is acceptable, with the source's own best-case caveat.
4. **Would I use it?** As a calibration benchmark for a clinic-type deployment, yes: these are exactly the columns my
   device produces and the reference I calibrate against. I would trust a model that lives on the canthi and face
   maximum and on the blackbody offset; I would distrust one that leans on ethnicity, cosmetics or `T_atm` as a proxy for
   the study's two ambient groups and two rooms. I would not take the RMSE as what I get at a building entrance with
   people walking in from cold or hot weather.

**Gaps between the dataset and the real decision, ranked**

1. **The written setting is not the data's setting (USE-1, USE-8).** `use_case` says "at an entrance ... (the FDA
   study's setting)". The FDA study is a clinic with 15 min acclimation, controlled room, young students. Entrance
   screening has no acclimation, wider ambient range, motion; accuracy there is known to be much worse. Changes the
   task's claimed scope, not the data. Fix: rewrite to "a clinic's triage station (or a device maker calibrating an
   IRT), after the person has rested 15 min in the room, decides whether to measure by mouth", or keep entrance and set
   fit approximate. I prefer the rewrite (USE-9: the clinic use case is real, practitioners have it, and the data
   mirrors it; this is not a rephrasing to excuse a gap, it is the source's own setting).
2. **Population and site (USE-8).** One clinic, 2016-2018, 95% under 30. The `row` field says "place and years not
   stated"; they are stated (University of Maryland Health Center, Nov 2016 - May 2018, Wang 2022). Should be written
   in `row`. Does not change the task, only its honesty.
3. **Key points partly hand-placed.** A deployed system finds the canthi automatically; manual labelling plus the
   release's exclusion of 76 blurred images make the features cleaner than deployment. A known best-case gap; worth one
   phrase in `fit_reason`.
4. **The 17 retake rows (USE-3, USE-7).** Their image comes from round 2 or 3, after the thermometer was in the mouth;
   mouth sites (`T_OR`, `T_OR_Max`) read warmer from round 2 on. In practice a blurred first image is retaken at once,
   before any thermometer, so a retake is realistic but this retake's timing is not. 1.7% of rows, 5 of 111 febrile;
   the curation documents a 0.07-0.14 °C over-prediction. A practitioner would accept either keep or drop; leaving the
   image missing is the one option I would reject (no device scores a person without an image; USE-7 says drop such a
   row rather than keep it missing). Small effect on the benchmark.
5. **Ethnicity and cosmetics as inputs (USE-3).** Not available at a screening point, available at a clinic intake. With
   gap 1 fixed to the clinic setting they are legitimate; they add 0.002 °C RMSE. Leave them.
6. **Split (SPLIT-3 via USE-10).** Deployment is "calibrate once, use later / elsewhere"; the IID split is the source's
   own and the probes show it barely matters. Leave IID.

**What a domain expert would change**

- Rewrite `use_case` to the clinic triage / IRT calibration setting with acclimation, and fill `row` with the place and
  period (University of Maryland Health Center, College Park; Nov 2016 - May 2018; mostly students).
- Add to `fit_reason` that the study is a best case by the source's own words (controlled room, acclimation,
  hand-checked key points, blurred images excluded).
- Keep `aveOralM`, round 1, the blackbody offset and the room readings; keep the IID split.
- Optional: report sensitivity / specificity at 37.5 °C next to RMSE in the notes, since that is the decision; not
  needed as the benchmark metric.
- On the modality marker (REVIEW_before issue 3): from the user's side these are the device's own radiometric outputs
  per anatomical site, the tabular input every IRT calibration uses, not pixels; a practitioner sees no reason to
  exclude. The selection rule is for the curator.

**Sources**

- Wang Q. et al. (2022), Infrared Thermography for Measuring Elevated Body Temperature: Clinical Accuracy, Calibration,
  and Evaluation, Sensors 22(1):215, https://pmc.ncbi.nlm.nih.gov/articles/PMC8749858/
- PhysioNet, Facial and oral temperature data from a large set of human subject volunteers, v1.0.0,
  https://physionet.org/content/face-oral-temp-data/1.0.0/
- Definition, record, the earlier REVIEW.md, the panel's claims and probes.
- Own probe on the shipped table (feature subsets, AUC/sensitivity at 37.5 °C).

</details>

<details><summary>Blind review</summary>

**Verdict**
Include. It is a real clinical-measurement regression task with moderate, non-trivial signal and no leakage that I could find. The preparation is sound. The changes below are optional.

**The task**
The data come from an FDA/UMD study of infrared-thermography fever screening (Wang et al.; PhysioNet "Facial and Oral Temperature Data" v1.0.0, CC0). The question is whether a non-contact IR camera reading of the face (FLIR, round 1), plus ambient conditions and demographics, can estimate the oral thermometer reading in monitor mode. Such cameras are used for fever screening at airports, clinics and building entrances. The use is real and well documented.

**What I verified**
- I downloaded the raw `FLIR_groups1and2.csv` from PhysioNet: 1020 subjects and 125 columns (4 rounds of 26 facial temperatures plus T_offset, then aveOralF, aveOralM, demographics, ambient conditions, Time and Date).
- The prepared table keeps round 1 only, plus Gender, Age, Ethnicity, T_atm, Humidity, Distance, Cosmetics, and TimeOfDay (Time converted to hours). It drops SubjectID, Date and **aveOralF**. Dropping aveOralF is correct: it is a second oral reading of the same quantity (r = 0.885 with aveOralM in the raw file) and would leak the target.
- In the raw file, 17 subjects have round-1 values missing. The prepared table has no missing round-1 values. I matched rows back to the raw file, and for 16 of them round 1 was filled from the first later round that is present (e.g. 180209-09 got T_Max1 = 35.74, the value of T_Max3). This is a reasonable imputation, but it is undocumented. The 17th of these subjects is 170208-03, which is dropped altogether (next point).
- Two raw rows were removed: 170208-03 and 180228-01. They are near-identical records about a year apart: every feature in all rounds agrees within 0.01 and aveOralM is 37.09 in both. This looks like a data-entry copy, and dropping both is right. After the removal, the prepared table has no exact duplicates. On the 26 standardized IR features, the smallest nearest-neighbour distance is 0.78, against a median of 1.56, so no near-copies remain.
- The values are plausible:
  - Facial temperatures are about 33-38.5 C.
  - aveOralM runs from 35.5 to 40.3 C. 10.9% of rows are above 37.5 C, which matches the source's "about 11% fever".
  - T_atm is 20-29 C, which matches the source's two ambient groups.
- Signal (3 folds x 3 repeats):
  - Ridge on T_Max1 alone: R2 0.616, RMSE 0.311.
  - Ridge on all features: R2 0.649.
  - LightGBM: R2 0.700 ± 0.058, RMSE 0.273.
  - Target SD: 0.510.

  So there is real signal, it is not trivial, and nonlinear models leave headroom over linear ones.

**Concerns (most to least serious)**
1. **Only round 1 is used; rounds 2-4 are thrown away.** The raw data hold 4 repeated IR captures per subject, and T_Max1 correlates 0.90 with T_Max2 and 0.68 with T_Max4. In a real deployment you would have one capture, so using round 1 is defensible and keeps the task realistic. It also leaves the task noisier than the source study's setup. I would keep this choice and document it, together with the fill-from-later-round imputation for the 16 subjects. If you prefer fidelity to the source, average the rounds instead (but not both versions).
2. **The IID split ignores collection time.** The data span about 154 measurement days from 2016-11 to 2018/19, and Date was dropped. The ambient groups and the seasons shift over time, so a temporal split would better match deployment: calibrate on past subjects, then screen new ones. With one row per subject (SubjectIDs are unique), the IID split has no subject-level leak, so the scores are honest. I would accept IID.
3. **The Age encoding is messy.** It is an unordered category with overlapping levels: "21-30" (10 rows) alongside "21-25" (355) and "26-30" (67). The levels are also heavily imbalanced: 18-20 has 532 rows and >60 has 3. I would leave it as raw, or map it to an ordinal midpoint. Either way this is minor.
4. **The target is skewed** (skew 1.98, with a fever tail up to 40.3 C). RMSE will be driven by the roughly 11% febrile subjects. That is clinically the right emphasis, so no change is needed.
5. **The dataset is small and also on UCI** (UCI id 925, "Infrared Thermography Temperature"). 1018 rows is enough to score with 3-fold x 10 repeats, but the standard deviation across folds is about 0.05 R2. It may overlap with other suites, so check for duplicates of it within the benchmark.
6. Other small points:
   - Cosmetics has 29 missing values (2.8%) and Distance has 2, left as NaN. That is fine.
   - Cosmetics is float 0/1, which is fine.
   - Ethnicity is used as a feature. It is plausible physiologically (skin emissivity, and the authors list demographic effects as an intended analysis), so it is acceptable.

**What I could not check**
- Tables 1 and 2 (the PDFs that define the variables) and the T_offset definition. My understanding is that T_offset is the blackbody-based calibration offset, but I have not confirmed it.
- Whether the measurement procedure changed between the two ambient groups.
- The exact year range of the Date field beyond the first rows.
- The preparation code itself: everything above is inferred by matching rows to the raw file.

</details>

<details><summary>Precedent check</summary>

Consistency check (phase A) of the definition's choices, the record's curator decisions and the three open questions
of `REVIEW_before.md`, against the rules and the precedents.

Sources: DEF = `datasets/_dev/tabarena-v0pt2/infrared_thermography_temperature/dataset.py`; REC =
`curation/records/infrared_thermography_temperature.md`; register = the run's register of flags. Rules:
`.claude/skills/knowledge-curation/references/{principles,selection,splits,leak_checks,use_case,cleaning_features}.md`.

**Curator decisions in the record:** none. REC holds no `CC` line. Its decisions are imported values (Andrej's
comments, `suggestion: Disagreement`, `DF: Yes`, the marker; workbook import of 2026-06-23, commit 391cf7a) and two AI
assessments (2026-10-07, 2026-10-20). Andrej's grouping concern ("subject ID ... counts up with -1,-2") is answered by
a measurement: SubjectID is `yymmdd-n`, unique in all 1,020 rows. The later stage's finding supersedes it (principles,
"Stages"). What it really points at is the measurement day (issue 2 below).

The register raises no flag on this dataset. Its four flags (few_minority, one_feature, scaling drift, trivial) do not
touch it. The probe flags are all clear (checklist).

**Summary**

| # | Decision | Rule | Verdict |
|---|---|---|---|
| 1 | In scope despite `Wrong Domain / Source Modality`, written as "an exception to the record's marker" | SEL-12, SEL-13 (Must); SEL-14, SEL-15 | **Not reasonable under the ranking as framed.** The facts it gives point to SEL-15 or SEL-14, so it needs no exception. Third keep of image-measured numbers with no rule-based reason: an amendment is due |
| 2 | IID over subjects, not grouped by day or temporal | SPLIT-1, -3, -4, -29, -30, -31 | Consistent in outcome (no hit, day ICC of the target 0.03). The written argument leans on the gap, which SPLIT-4 forbids. airfoil_self_noise and superconductivity point the other way if a day is a set-up |
| 3 | 17 retake rows keep their round-2/3 image | LEAK-10 (Must), LEAK-11 (Should), USE-7 | Consistent with LEAK-11 (south_africa_coronary_heart_disease). "Leave missing" would break USE-7 and the mic precedent. "Drop" has its own precedent (bias_correction, USE-7) |
| 4 | `fit = "direct"` | USE-8 | **Departs without a reason** from south_africa_coronary_heart_disease and kick, where a kept post-outcome value or potential leak made the fit approximate. It also has inputs the camera does not see |
| 5 | Room readings, distance and `T_offset1` kept (v1 dropped them) | USE-6, LEAK-10 | Consistent. A reasoned reversal of a legacy v1 choice, which ranks lowest |
| 6 | Twin measurement 170208-03 / 180228-01: both rows dropped | LEAK-16, LEAK-19, LEAK-20 | Departs from LEAK-19 (drop the copies, keep one) **with a stated reason**: the two codes conflict on date, ethnicity and room readings. Reasonable; it costs 1 row |
| 7 | `Distance` 79.0 set to 0.79 m | CLEAN-11, remedy ladder | Consistent: repair is above making the value missing, and the same-day evidence is strong. corporate_credit_rating kept a weaker suspected unit slip, which fits the same logic |
| 8 | `aveOralF` dropped | LEAK-10 (cases: another encoding of the target) | Consistent |
| 9 | Overlapping `Age` bin and target grid kept | CLEAN-11 (unusual stays) | Consistent |
| 10 | Accepted check warnings | none declared; `dataset check` gives 0/0/0 | Nothing to check |
| 11 | Priority 4 (gap -, use case +, source +, shape +, no risk) | selection.md, Priority | Consistent with the table, but "use case +" needs a direct fit (see 4). If the fit becomes approximate the priority is 3 |

**1. Modality marker (REVIEW_before issue 3)**

**The decision.** DEF `curation_comments`, last bullet: "we keep the dataset as an exception to the record's marker
`Wrong Domain / Source Modality` (features measured from images)". REVIEW_before adds "since Lennart asked to add the
dataset".

**The rules.** SEL-12 and SEL-13 are Musts. Under principles.md ("Exceptions and amendments"), "A Must has no
exceptions: only a higher-ranked Must overrides it, and anything else is an amendment." Two things follow:

* "Exception" is the wrong instrument. The case is in scope only if SEL-13 does not apply, because SEL-14 or SEL-15
  (both Musts that narrow it or sit beside it) cover the columns, or if SEL-13 is amended.
* "Lennart asked to add the dataset" sets nothing apart. The request was the `_too_late_to_add` bucket, a request for
  work (2026-10-07 run, `new65/header.md`). It was not a scope decision: REC has no CC line, and the dataset sat under
  `_out_of_scope/`.

**The facts that matter.**

* 27 of 35 features are read from the thermal image: 26 site temperatures plus `T_offset1`, the blackbody offset.
* Each is a radiometric temperature in °C at a named facial site (ISO/TR 13154), the max or the mean of the 4 warmest
  pixels. None describes shape, texture or layout.
* The target is a physical quantity of the same person, not what the image shows.
* The source's own model is a one-feature calibration on `T_Max1` (Wang 2022 Sec. 2.5). Screening thermographs output
  these readings.
* Key points were placed by hand for about half the images (Zhou 2020 Sec. 2.2). A human locates the site; the
  temperature reading itself is not a human score.
* No images are released, so whether a vision model would be "clearly better" (SEL-12) cannot be measured.

**The precedents.**

| Dataset | Features | Decision | Date, who | Reason written |
|---|---|---|---|---|
| `satimage` (curation/records/satimage.md) | multispectral pixel radiances of a 3x3 neighbourhood; target the land-cover class | No, `Image` | workbook import (undated), Lennart and Andrej | "Features extracted from images" |
| `wilt` (curation/records/wilt.md) | spectral and texture values of image segments; target diseased trees | No, `Image` | workbook import (undated) | "Image data" |
| `internet_advertisements`, `breast_w` | image geometry plus URL tokens; a pathologist's grades of a slide | No (SEL-13 Cases) | selection.md Cases; breast_w confirmed 2026-10-15, Lennart | yes |
| `breast_cancer_prediction` (curation/records/breast_cancer_prediction.md) | BI-RADS readings of a mammogram plus risk factors | kept (SEL-14) | CC 2026-10-15, Lennart | "screening programmes run tabular risk models on them ... the real-world use decides" |
| `heart_disease_cleveland` | thallium-scan result | kept (SEL-14 Cases) | selection.md | yes |
| `tecator` (curation/records/tecator.md) | NIR absorbance spectrum | No for PCA preprocessing, not for modality; the CC says "the same models can be used ... interesting to include" | CC, undated | yes |
| `biomechanical_orthopaedic_prediction` (curation/records/biomechanical_orthopaedic_prediction.md) | spinopelvic angles and lengths measured on radiographs | Yes (Disagreement), same marker, v2 folder | Lennart and Andrej, undated (import) | **none**. The record's discussion even calls it "toy data" |
| `dementia_prediction` (curation/records/dementia_prediction.md) | 3 MRI brain-size numbers plus MMSE and demographics | Yes (Disagreement), same marker, v2 folder | Lennart, undated (import) | **none**. Andrej: "we need to quickly talk about how we proceed with medical image data" |

**Assessment.**

* The pair that needs a distinguishing fact is satimage and wilt against this case. Both have radiometric values from
  an imaging sensor, and both are out. SEL-13 even lists "remote-sensing spectra".
* The best fact that sets this case apart: in satimage and wilt the radiances are used to recognise what the image
  shows (a vision task, the content). Here the reading is the measured quantity: the camera works as a non-contact
  thermometer aimed at fixed sites, and the target is the same physical quantity measured another way.
* That is SEL-15 ("sensor readings measured on the entity directly"), or SEL-14 (the instrument's reading that a
  tabular calibration uses in practice, as in breast_cancer_prediction). It is not an exception to SEL-13.
* The written reasons in DEF ("radiometric temperature at a facial site, the input of the calibration the source
  studies, and the release holds no images") are these facts. Only the label "exception", and the "Lennart asked"
  reason in REVIEW_before, conflict with the ranking.
* **Third case of the same kind (principles, case 4).** biomechanical and dementia were kept with the same marker on
  numbers measured through an imaging device, and neither wrote a rule-based reason. This would be the third. An
  amendment is due: spell out in SEL-14 or SEL-15 that "a physical quantity measured through an imaging device at
  defined sites (a temperature, a volume, an angle), used by the field as the instrument's reading, is a measurement
  (SEL-15), not an image descriptor (SEL-13)". satimage and wilt would be the counter-cases.
* Those two older keeps should then be re-read against the amended rule. biomechanical's own discussion ("nowadays
  one would use MRI image data") argues the other way.

**Consistency check (AI, 2026-10-20):** the definition keeps infrared_thermography_temperature "as an exception to"
`Wrong Domain / Source Modality`, but SEL-12 and SEL-13 are Musts and have no exceptions. satimage and wilt (No,
`Image`, workbook import) also hold radiometric values from an imaging sensor. What sets this case apart?
(a) the columns are temperatures at fixed body sites, read by the camera as a thermometer, and the target is the same
physical quantity, not the image's content: SEL-15 or SEL-14 holds, SEL-13 does not apply, and the note says so
instead of "exception"; (b) treat it like satimage and wilt: `No`, `Image`, folder removed; (c) reopen satimage and
wilt to match; (d) amend SEL-14 or SEL-15 for quantities measured through an imaging device (third such keep after
biomechanical_orthopaedic_prediction and dementia_prediction, neither with a written reason).

**2. Split regime (REVIEW_before issue 1)**

**The decision.** IID over subjects, 10 x 3. The reasons in DEF:

* each subject is in the file once;
* the source calibrated on a random 60%;
* "folds grouped by day score the same as random ones" (forest -0.003 ± 0.003, ridge +0.004 ± 0.002);
* `hidden_groups.py` finds no hit.

**The rules and precedents.**

* SPLIT-29 and SPLIT-30 hold. No probe hit, and the day carries little of the label (ICC 0.03, permutation p 0.078),
  so the "entity carries the label" condition is weak.
* SPLIT-5: the source's random 60/40 split is a claim, not a reason. DEF does cite the source's own caveat (Sec. 4.5).
* SPLIT-4 (Must): "the gap never decides". The third reason is a gap argument. Under SPLIT-4 the question is whether
  the deployed calibration meets days or set-ups that new data would not contain.
  * airfoil_self_noise (CC 2026-10-20, Lennart): grouped by set-up because a new set-up is the query.
  * superconductivity (2026-10-06): grouped though random costs at most 0.009 R^2.
  * Both show a small gap does not keep IID when the deployment faces new set-ups.
* What sets this case apart: the predicted entity is a new person, not a new day. The day's conditions (T_atm,
  Humidity, Distance, T_offset1) are measured for every new row, so they are features. SPLIT-4: "If new rows keep
  having the value, the column is a feature and the split stays."
* SPLIT-31 (amazon_employee_access, bank_marketing): IID can match the framing while being optimistic, and the
  day-grouped and temporal versions are candidate variants. That fits.
* Temporal: the date survives, so SPLIT-7 and SPLIT-8 (account_debt_south_africa, 2026-10-12) are not the pattern.
  The rows are independent people, not a stream. SPLIT-3: one regime, the one the use case implies. "A calibration
  fitted once and used later" is a temporal reading of the use case, and the year-1 to year-2 check (+3% to +9% RMSE)
  is the only measured shift.
* No curator precedent decides a dated cohort of one-visit people in either direction.

**Verdict.** Consistent in outcome. Restate the reason on the entity (a new person; the day's conditions are
features) rather than on the gap.

**Consistency check (AI, 2026-10-20):** your call on the split (IID over subjects) rests partly on "grouped by day
scores the same". airfoil_self_noise (grouped by set-up, 2026-10-20) and superconductivity (grouped, 2026-10-06) were
grouped although the gap was small, because the deployment meets set-ups it has not seen. What sets this case apart?
(a) the prediction is for a new person, and the day's set-up is recorded as features on every new row (SPLIT-4's
"the column is a feature"), recorded as the reason instead of the gap; (b) treat it like airfoil: group by
measurement day; (c) temporal on `Date`, if "a calibration fitted once and used later" is the use case (SPLIT-3);
(d) change the rule.

**3. The 17 retake rows (REVIEW_before issue 2)**

**The decision.** Keep their round-2/3 image under the round-1 names, with a note.

**Precedents.**

* LEAK-11 (Should; narrows LEAK-10): "a value measured after the outcome that weakens the signal stays, with a note".
  south_africa_coronary_heart_disease (CC 2026-10-01, Lennart) is the case. The retakes weaken the signal: the 17 are
  over-predicted by 0.07-0.14 °C and are hard to detect (AUC 0.58). They do not give the target away, so LEAK-10's
  Must holds. **Consistent.**
* The "leave missing" alternative would break USE-7 (Must). bias_correction_r_bias_correction_r_2 (CC 2026-10-15,
  Lennart): "a row that lacks the input the prediction acts on is no task row: drop it rather than keep it as
  missing". It would also create missingness that marks a 29%-febrile group, the mic pattern (LEAK-10 cases). It should
  not be offered as an equal option.
* The "drop" alternative is the USE-7 reading: rows without a valid pre-reading image are no task rows. The definition
  departs from it with a stated reason: the source counted them in its round-1 cohort (Zhou 2020 Table 5), and the
  17 include 5 febrile subjects. That is a reasoned call between two precedents, so no prompt is needed. The curator
  picks.

**4. Fit `direct` (claims 8-9; checklist P3)**

**The decision.** `fit = "direct"`, and the fit_reason says "The camera has all these values at one look".

**Precedents.**

* south_africa_coronary_heart_disease: values measured after the outcome kept under LEAK-11, so `fit="approximate"`.
* kick (USE-8 Cases): a potential leak kept on purpose, so approximate.
* dementia_prediction (image summary numbers plus clinical scores): approximate.
* Here the post-reading images of 17 rows are kept on purpose, and `known` includes ethnicity, age group and cosmetics,
  which an entrance camera does not see. Dropping them costs about 0.005 R² (2026-10-07 run).
* The task also covers one study's cameras and rooms.
* Nothing in fit_reason addresses these gaps, so this **departs without a reason**.
* The fact that may set it apart: 17 rows are 1.7% of the data, against every case in south_africa.

**Consistency check (AI, 2026-10-20):** the fit is `direct`, while south_africa_coronary_heart_disease (2026-10-01)
and kick were made `approximate` because they keep values measured after the outcome or a potential leak on purpose.
This task keeps 17 post-reading images and inputs a camera does not see (ethnicity, age group, cosmetics). What sets
it apart? (a) the post-reading images are 1.7% of the rows, and the stated attributes are what an entrance check asks
or a booth form records, so the rows, features and split mirror screening; fit_reason should then say so; (b) make it
`approximate` like south_africa, naming the gaps (and the priority drops to 3); (c) drop the 17 rows and the three
unseen attributes to keep `direct`; (d) change USE-8.

**5-11. The other definition choices**

* **Room readings, distance, `T_offset1` (5).**
  * USE-6 (Must): anything known at the prediction point is an input.
  * The v1 notebook dropped them as lab "control parameters" (author and date unknown, legacy; lowest in "Who
    decides"). v2 reverses that with a reason: a screening thermograph measures all four.
  * The leak probe shows none predicts the target alone (R² ≤ 0).
  * **Consistent.** The reversal belongs in the curator's view because it changes what "known" means.
* **Twins (6).**
  * LEAK-19's cases (wine_quality, audiology_diagnosis) drop the extra copies.
  * Dropping both rows follows LEAK-20's "drop every copy" logic, for a pair whose non-image fields conflict.
  * **Departs with a stated reason** (neither code can be trusted). Reasonable; 1 extra row.
* **Distance (7).**
  * A repair, which is above "make it missing" on the remedy ladder. The same-day range is 0.60-0.77 m.
  * corporate_credit_rating kept a suspected unit slip because the evidence for it was weak.
  * **Consistent.**
* **`aveOralF` (8).** The same readings in fast mode, corr 0.885: a second encoding of the target (LEAK-10 cases).
  **Consistent.**
* **Age bin and target grid (9).** Unusual values stay (CLEAN-11). The bin follows the source (Wang 2022 Table 1).
  **Consistent.**
* **Accepted warnings (10).** None declared, and `dataset check` gives 0 errors, 0 warnings, 0 info.
* **Priority (11).** The arithmetic follows the table. "Use case +" requires a direct fit (selection.md, Priority),
  so it depends on decision 4.

**Drift and repeated reasons**

* No drift by one curator on this dataset's rules. Lennart's modality calls are consistent where they are written
  down: breast_cancer_prediction in, breast_w out, 2026-10-15, with the fact that sets them apart.
* Repeated reason: the third keep of numbers measured through an imaging device under the same marker without a
  written rule (biomechanical_orthopaedic_prediction, dementia_prediction, this one). See decision 1: an amendment of
  SEL-14 or SEL-15 is due rather than a third silent exception.

</details>

<details><summary>Advocate</summary>

Position: ship. The task is real and leak-free, the split is sound, and every problem the panel found can be fixed in
the definition's text or with one filter. None of them calls for exclusion. Sources: claim_audit.md (CA),
column_audit.md (COL), split_audit.md (SA), practitioner.md (PR), precedents.md (PREC), the blind review (BLIND).

**1. In scope under SEL-15 / SEL-14 (Must). The label "exception" is wrong; the keep is right.**

- Claim: the 27 image columns are measurements taken on the person (SEL-15), not descriptors of what an image shows
  (SEL-13).
- Evidence:
  - Each column is a blackbody-compensated radiometric temperature in °C at a named facial site, the max or the mean
    of the 4 warmest pixels (COL; PhysioNet `_Table1.pdf`).
  - The target is the same physical quantity measured by mouth.
  - The source's own model is a one-feature calibration on `T_Max1` (Wang 2022 Sec. 2.5).
  - IRT devices output these readings, and IEC 80601-2-59 names the canthi as the reference site (PR).
  - No images are released.
  - satimage and wilt are different: there the radiances serve to recognise the image's content (land cover,
    diseased trees). Here the camera works as a non-contact thermometer (PREC 1).
- Rule: SEL-15 (Must); SEL-14 (Must, narrows SEL-13) by the breast_cancer_prediction pattern. "P3 informs P2: let the
  use case decide" (principles.md, Lennart 2026-10-15). PR: "a practitioner sees no reason to exclude."
- Concession: a Must has no exceptions, so "kept as an exception" and "Lennart asked" are the wrong reasons
  (PREC). Mildest fix: rewrite the last curation bullet to cite SEL-15/SEL-14. This is the third keep of its kind
  (after biomechanical, dementia), so propose the SEL-15 amendment PREC drafts. Text only; the data stays.

**2. No leak survives (P4, LEAK-10 Must holds).**

- Evidence:
  - The definition drops `aveOralF` (a second encoding of the target, r 0.885), rounds 2-4, `SubjectID` and `Date`.
  - It drops the double-coded twin pair (0.01 °C over 81 values). The next closest pair is 0.30 °C apart (CA 17).
  - Leak probe: no input alone predicts the target (R² ≤ 0). `hidden_groups` finds 0 hits. `dataset check` reports
    0/0/0.
  - The blind reviewer found the same independently: "Include ... no leakage that I could find" (BLIND).
- Rule: LEAK-10, LEAK-16, LEAK-20. This outranks any P6/P7 point raised against it.

**3. The 17 retake rows: a fix in the definition, not a reason to exclude.**

- Concession: for these 17 rows (1.7%; 13 from round 2, 4 from round 3), the image was taken after the thermometer
  (Zhou 2020 Fig. 2). The `changes` text "we keep only the first image" is false for them (CA 5, 7).
- Why it is small: the later image weakens the signal rather than giving away the target. Models over-predict these
  rows by +0.07 to +0.16 °C, against ~0 elsewhere, and a model detects them only at AUC 0.58 (CA 13, PREC 3).
  LEAK-11 (Should, narrows LEAK-10) therefore permits keeping them with a note. That is the south_africa_coronary
  precedent.
- Rank: USE-7 (P3, Must) sits above LEAK-11. A row whose pre-thermometer image is missing lacks the input the
  prediction acts on. I accept that reading.
- Mildest fix that settles both: filter to `round == 1`. One line in `_clean`; the cost is 5 of 111 febrile rows.
  This also makes the `changes` text true and removes the "leak kept on purpose" that pushes the fit toward
  approximate (point 4).
- Not acceptable: leaving the image missing. That breaks USE-7, and the missingness would flag a group that is 29%
  febrile (PREC 3).

**4. The use case is real; the fit stays direct once the text matches the source (P3, USE-8 Must, USE-9 Should).**

- Concession: three statements in the definition are refuted:
  - "at an entrance ... (the FDA study's setting)". The study ran at the UMD Health Center with 15 minutes of
    acclimatisation, and both papers call it a best case (CA 2).
  - "place and years not stated". Zhou 2020 gives UMD, Nov 2016 to May 2018 (CA 3).
  - "the camera has all these values at one look". Gender, Age, Ethnicity and Cosmetics are stated by the person,
    not seen by the camera (CA 9).
- Why direct still holds: USE-9 asks whether the data mirrors another well-defined use case. It does: a clinic triage
  station, or a device maker calibrating an IRT against oral readings. This is the source's own setting, not a
  rephrasing to excuse a gap. PR: "Fit: direct, but for a clinic triage station"; "Would I use it? ... yes."
- The stated inputs fit a clinic intake and are worth little. Dropping them changes R² by 0.004 to 0.009 (CA 9) and
  RMSE by 0.002 °C (PR).
- Fix: rewrite `use_case`, `row`, `changes` and `fit_reason` (the best-case caveat).
- With the 17 rows dropped, `direct` matches USE-8. If the curator keeps them instead, set `fit = "approximate"` (the
  kick and south_africa precedents; priority 4 becomes 3). Either way the dataset ships.

**5. IID over subjects is the right split (P4, SPLIT-4 Must, USE-11).**

- Evidence:
  - Each row is a new person seen once. The day's conditions (`T_atm`, `Humidity`, `Distance`, `T_offset1`) are
    recorded for every new row, so they are features, and SPLIT-4 says "the split stays".
  - The day carries ICC 0.03 of the target (p 0.078).
  - Grouped by day and random score the same: forest RMSE 0.2733 against 0.2733 (SA 1).
  - Temporal, averaged over windows: ridge 0.310 against 0.311, forest 0.282 against 0.282 (SA 2).
  - The split auditor's verdict: "right with notes".
- Why airfoil and superconductivity do not apply: there the query is a new set-up; here it is a new person (PREC 2).
- Concessions, both text only:
  - Ground the IID choice in the entity (SPLIT-4), not in the gap.
  - Restate bullet 10. Across models the windows range from -7% to +16%, and the first year-2 window is worse with a
    +0.1 °C bias (SA problem 2, SPLIT-21).
- A temporal version is a candidate variant under SPLIT-31, not a fix.

**6. Worth benchmarking and faithful (P6, P5).**

- Not trivial (TP-2):
  - The source-style calibration of `T_Max1` alone reaches RMSE 0.277; an additive model of all features reaches
    0.265 and wins on 28 of 30 splits (CA 24).
  - LightGBM reaches R² 0.70 against 0.616 for `T_Max1` alone (BLIND). Target sd 0.51.
  - Fever is ranked well: AUC at 37.5 °C is 0.96-0.97 (PR).
- Faithful (PROV-13): the data is the CC0 PhysioNet original, checksum-verified. Round 1 follows both papers. The UCI
  copy averages the four rounds, including post-thermometer and open-mouth images (CA 12), so it is the worse version
  and we rightly avoid it.

**7. The remaining findings are independent text fixes, not conflicts.**

- Number fixes (EV-8):
  - Retake bias: LightGBM gives 0.158, so state the model behind the 0.07-0.14 range (CA 13).
  - Day-grouped result: 0.707 against 0.709 under v2 (CA 21).
  - "A screening thermograph measures all four" should read "the screening station records" (CA 15).
- Record sync: reference year and venue (Sensors 22(1):215, 2022), `original_source`, and the superseded screening
  comment (CA 43, 48, 57).
- None of these touches the data. principles.md step 4: each is fixed on its own, and none weighs against shipping.

Judgment record (advocate):

```text
Verdict: ship after changes.
Validity: SEL-15/SEL-14 hold (rewrite the "exception" note; propose the amendment); USE-7 triggered, fixed (drop
  the 17 retake rows); USE-8 direct after rewriting use_case/row/changes/fit_reason to the clinic setting (USE-9);
  LEAK-10 holds; SPLIT-4/USE-11 hold (IID; reason restated on the entity).
Value: TP-2, a real non-trivial signal (additive 0.265 vs calibration 0.277, 28/30).
Quality: CLEAN-11/14/21 hold; number and record fixes.
For the curator: drop vs keep the 17 (USE-7 vs LEAK-11; the latter makes the fit approximate); temporal as a variant.
```

**Rebuttal**

The critic and I reach the same verdict: ship after changes, with no exclusion. We agree on every remedy. I dispute
two framings, and neither changes a fix.

**1. Scope (SEL-12/13 against SEL-15/14): concede the wording, dispute one sentence**

- **Conceded.** "Exception" and "Lennart asked" are the wrong reasons. A Must has no exceptions. The note should
  give the SEL-15 reason, and the SEL-15 amendment is due as the third case of its kind.
- **Disputed.** The critic writes that satimage and wilt stand against this case "with nothing that sets this case
  apart". The critic's own Rule line then names the distinguishing fact: here the camera works as a thermometer at
  fixed sites, while satimage and wilt recognise image content (precedents.md, sec. 1).
- **What follows.** The fact that sets the case apart exists. Only the definition's note fails to state it. This is
  the point-1 remedy in both briefs.

**2. The 17 retake rows (USE-7 against LEAK-11): concede**

- USE-7 is a P3 Must and LEAK-11 is a Should that narrows LEAK-10, so LEAK-11 cannot rescue the rows. I said so in my
  opening point 3.
- **Fix.** Filter to the 1,001 subjects with a complete round-1 image, and drop the keep in Decision 2. The cost is 5
  of 111 febrile subjects.
- Leaving the values missing stays ruled out.

**3. Fit (USE-8/USE-9): concede, with one gloss**

- Rewrite `use_case` and `fit_reason` to the clinic or calibration setting. Then `direct` holds once point 2 is
  applied. If the rows stay, the fit is `approximate` and the priority falls to 3.
- **Gloss on "humidity and distance are not camera outputs".** The criticism is true of the wording only. Room
  readings and the set distance are known when the image is taken (USE-6, Must; column_audit rates them "fine").
  They stay as features, and only the text changes.

**4. Split (SPLIT-4, SPLIT-21): concede the remedy, dispute one rule cited**

- **Conceded.** SPLIT-4: base the IID choice on the entity (a new person, with the day's conditions as features), not
  on the gap. Also add the year-2 set-up change to `split` and `splits_comment`.
- **Disputed.** SPLIT-21 (splits.md l.120) governs "the training history" and "the windows" of a temporal task. It
  does not govern the choice between IID and temporal.
- **What follows.** SPLIT-4 alone already rules out the gap-based reason, so the remedy is unchanged. The precedent
  should cite SPLIT-4, not SPLIT-21.
- Temporal stays a curator call, as a variant under SPLIT-31.

**5-7. Text, numbers, record: concede all**

- These are independent quality fixes (principles.md, step 4).
- Neither brief weighs any of them against shipping.

Agreed record:

```text
Verdict: ship after changes.
Validity: SEL-15 holds (rewrite the note; propose the amendment); USE-7 fixed (drop 17 rows); USE-8 direct after the
  clinic rewrite (USE-9); LEAK-10 holds; SPLIT-4 holds (reason on the entity).
Value: TP-2 holds. Quality: text, number and record edits.
For the curator: temporal as a variant (SPLIT-3/SPLIT-31).
```

</details>

<details><summary>Critic</summary>

Position: **ship only after changes.** I do not argue for exclusion. The task is real and the data is faithful. But
the definition breaks two Musts in how it is written, and one Must in 17 rows. Points in rank order.

**1. P2, SEL-12/SEL-13 (Must): the scope is kept by an "exception" to a Must**

- **Problem.** `curation_comments` keeps the dataset "as an exception to the record's marker `Wrong Domain / Source
  Modality`". REVIEW_before adds "since Lennart asked to add the dataset". principles.md: "A Must has no exceptions".
  The request was a work queue entry, not a scope decision: the record has no CC line (precedents.md, sec. 1).
- **Effect.** As written, the dataset's scope rests on an instrument the rules do not allow. satimage and wilt
  (radiometric values from an imaging sensor, `No`, `Image`) stand against it with nothing that sets this case apart.
- **Evidence.** 27 of 35 features are read from the thermal image. Each is a radiometric °C at a named facial site.
  The target is the same physical quantity, measured by mouth. No images are released (precedents.md; claim_audit
  claim 27).
- **Rule.** SEL-13 (Must) against SEL-15 / SEL-14 (Must, narrowing). On these facts SEL-15 holds: the camera works as
  a thermometer at fixed sites, and these are not content descriptors.
- **Remedy (fix the note).** Replace "exception" with the SEL-15 (or SEL-14) reason, with satimage and wilt as the
  counter-cases, and drop "Lennart asked" from REVIEW. This is the third keep of this kind (after
  biomechanical_orthopaedic_prediction and dementia_prediction, neither with a written reason), so propose an
  amendment of SEL-15 (principles, consistency case 4).

**2. P3/P4, USE-7 (Must) and LEAK-10: 17 rows carry an image taken after the prediction point**

- **Problem.** `first_complete_image` gives 17 subjects a round-2 image (13 subjects) or a round-3 image (4) under the
  round-1 names. Both rounds were imaged after the oral thermometer had been under the tongue (Zhou 2020, Fig. 2). The
  round-3 image falls between the two readings that make up the target.
- **Effect.** These rows are not the prediction the task describes. Models over-predict them by +0.07 to +0.16 °C,
  against at most 0.01 °C elsewhere. The mouth sites read +0.41 °C warmer from round 2 on. In practice a blurred image
  is retaken before any thermometer (practitioner, gap 4).
- **Evidence.** claim_audit claims 5, 11 and 13; column_audit problem 2. The "source counted them" defence is
  circumstantial: Zhou analysed group 1 only, which holds 11 of the 17, and no table says which image was used for
  them (claim 34).
- **Rule.** USE-7 (Must): a row that lacks the input the prediction acts on is dropped. LEAK-11 (Should) narrows
  LEAK-10, not USE-7, so it cannot override a Must.
- **Remedy (fix the definition).** Filter to the subjects with a complete round-1 image (1,001 rows), and remove
  `first_complete_image` and Decision 2 as a keep. The cost is 5 of 111 febrile subjects, which the regression target
  carries without trouble. Leaving the values missing is ruled out (29% febrile vs 10.6%: missingness that encodes
  the outcome).

**3. P3, USE-8 (Must): `fit = direct` rests on a use case the data does not mirror**

- **Problem.** `use_case` says "at an entrance ... images a person once (the FDA study's setting)". The study was a
  university health centre: a 15-minute rest in a draft-free room, seated, a backdrop, a blackbody, and key points
  partly placed by hand. Both papers call it a best case. `fit_reason` says "the camera has all these values at one
  look", but Gender, Age, Ethnicity and Cosmetics are stated by the person, and room humidity and distance are not
  camera outputs.
- **Effect.** The task claims a scope (entrance screening) where accuracy is known to be worse. The fit label then
  misstates what a score here means.
- **Evidence.** claim_audit claims 2, 8, 9 and 15; practitioner gaps 1 and 3; precedents.md sec. 4 (south_africa and
  kick were made approximate on the same grounds).
- **Rule.** USE-8 (Must); USE-9 (Should) allows a direct fit for another real use case the data mirrors.
- **Remedy (fix the definition).** Rewrite `use_case` as the source's setting: a clinic triage station, or an IRT
  maker calibrating a device, after acclimation, with a short intake. Rewrite `fit_reason` to name the best-case
  conditions. With point 2 applied, `direct` then holds (practitioner verdict). If the 17 rows stay, the fit must be
  `approximate` (USE-8 lists "a potential leak kept on purpose"), and the priority falls to 3.

**4. P4, SPLIT-4 and SPLIT-21 (Must): the regime is argued from gaps**

- **Problem.** The comments argue for IID from "grouped by day scores the same" and argue "not temporal" from a
  -0.2% to +2.5% comparison over 6 windows.
- **Effect.** The reasoning would not survive a rerun. With three models on the same windows, the change is -7.0% to
  +16.3%. The first window of year 2 is 2-16% worse, with a +0.1 °C bias. The set-up also changed between the years:
  the median distance went from 0.80 m to 0.60 m, and the study used two locations. None of this is in
  `task_summary.split`.
- **Evidence.** split_audit, measurements 2 and 3 and problem 2; precedents.md sec. 2 (airfoil_self_noise and
  superconductivity were grouped despite small gaps).
- **Rule.** SPLIT-4 (Must: the gap never decides); SPLIT-21 (Must: no regime decided from a few windows).
- **Remedy (fix the definition text, not the split).** Ground IID on the entity: a new person, with the day's
  conditions recorded as features on every new row (SPLIT-4). Drop the gap figures as the reason. Add the year-2
  set-up change to `split` and `splits_comment`. Whether to switch to temporal stays the curator's call (SPLIT-3).

**5. Procedure (writing.md, EV-2): false statements in the task summary and comments**

- **`row`.** "place and years not stated" is false: Zhou 2020 names the UMD University Health Center, Nov 2016 to
  May 2018.
- **`changes`.** "We keep only the first image, taken before the thermometer" is false for 17 rows (moot if point 2
  is applied).
- **Bullet 5.** "a screening thermograph measures all four" is false: the room sensors belong to the screening
  station, not the camera.
- **Remedy.** Edit the strings. This is quality, not a reason to hold the task.

**6. EV-8 (Should): numbers not reproduced**

- **Day-grouped vs random.** The comments give R² 0.709 vs 0.711; the rerun gives 0.707 vs 0.709.
- **Bias of the retakes.** The comments give 0.07-0.14 °C; LightGBM gives 0.158.
- **Temporal range.** See point 4.
- **Remedy.** Give each number with its model and settings, or use the reproduced values. This is quality.

**7. Record (PROV-10, sync)**

- The Reference block says "2021, Italian National Conference on Sensors"; the paper is Sensors 22(1):215, 2022.
- `original_source: Website` disagrees with the definition's `Other`.
- **Remedy.** A record sync. This is quality.

Judgment record:

```text
Verdict: ship after changes.
Validity: SEL-13 not triggered on the facts, but the "exception" wording breaks the rule for Musts (fix: SEL-15
  reason, amendment due); USE-7 triggered by 17 post-thermometer rows (fix: drop them); USE-8 triggered by fit direct
  against an entrance use case (fix: rewrite to the clinic/calibration setting); SPLIT-4/SPLIT-21 triggered by
  gap-based reasons (fix: reason on the entity; temporal stays a curator call).
Value: TP-2 holds (additive model beats the one-feature calibration on 28/30 splits).
Quality: summary and comments carry false statements and unreproduced numbers (edit); record sync.
```

**Rebuttal**

The advocate and I agree on the verdict (ship after changes) and on almost every remedy. One real dispute remains:
whether keeping the 17 retake rows is still the curator's option. Two smaller points need precision.

**Point by point**

1. **Scope under SEL-15/SEL-14; "exception" is the wrong label.** Concede. The remedy is the same as my point 1:
   rewrite the note to cite SEL-15, and propose the amendment.

2. **No leak survives.** Concede for `aveOralF`, rounds 2-4, `SubjectID`, `Date` and the twin pair. One precision:
   the 17 retake rows still carry a post-thermometer image until point 3's filter is applied. "No leak" holds only
   after that filter. Before it, LEAK-11 covers them only with a note.

3. **Drop the 17 retake rows.** Concede the remedy. Filter to `round == 1`, which leaves 1,001 rows.
   - **Dispute.** The advocate's judgment record still offers the curator "drop vs keep the 17 (USE-7 vs LEAK-11)",
     and point 4 says "either way the dataset ships". That contradicts the advocate's own concession: USE-7 (P3, Must)
     outranks LEAK-11 (P4, Should). LEAK-11 narrows LEAK-10, not USE-7.
   - **Rule that wins.** principles.md: "Must wins over Should", and "A Must has no exceptions". So keeping the rows is
     not a weighing call. The only lawful keep is an amendment of USE-7.
   - **What the curator should be offered.** Drop the 17 rows (the fix), or amend USE-7 (a deliberate rule change).
     Keeping them as an option is not on the list.

4. **Fit is direct once the text matches the source.** Concede, given point 3's filter and the rewritten `use_case`,
   `row`, `changes` and `fit_reason` (USE-9). The "keep them and set approximate" fallback falls with the dispute in
   point 3.

5. **IID over subjects.** Concede that IID stays and that the reason should rest on the entity (SPLIT-4).
   - **One addition the advocate omits.** `task_summary.split` and `splits_comment` should state that the set-up
     changed between the two study years. Two facts show it:
     - the median distance fell from 0.80 m to 0.60 m, and the study used two locations (SA facts; Wang 2022
       Sec. 2.4);
     - a year-1 calibration over-predicts year 2 by 0.07-0.09 °C and is worse on 12-15 of 15 folds (SA measurement 3).
   - **Why it matters.** The summary's "the same set-up" is otherwise misleading. This is a text fix under USE-8, which
     requires the split to be described as it is.

6. **Worth benchmarking and faithful.** Concede. One precision for the text: "the source's segmented calibration" is
   our own 4-knot spline. Wang 2022 gives no knots (CA 24 caveat). Call it "a one-feature segmented calibration in the
   source's style" (EV-2).

7. **Number and record fixes.** Concede.

**Settled judgment record**

```text
Verdict: ship after changes.
Validity: SEL-15 holds (rewrite the note; amendment due). USE-7 triggered, fixed by dropping the 17 rows; keeping them
  needs an amendment of USE-7, not a curator weighing. USE-8 direct after the text rewrite. SPLIT-4: IID, with the
  reason on the entity and the year-2 set-up change stated.
Value: TP-2 holds.
Quality: text, number and record fixes.
```

</details>
