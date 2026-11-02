# thailand_road_accident_register_2019_2022

**Outcome:** added. The data are the Ministry of Transport's TRAMS crash register, the yearly files of 2019-2022
(snapshot of 2026-10-30): 81,059 crashes on the national highways, rural roads and expressways. The target is the
crash's deaths (87.5% zero). The task is the severity part of road-network screening: a road agency estimates the
expected deaths of each recorded crash from where, when and how it happened, and sums them per road section. The split
is temporal: nine two-month windows, July 2021 to December 2022, each trained on the crashes at least two months older
that were in the register when the window starts. The metric is RMSE (the source has none). The AI recommends shipping
it after the review panel's text changes, which are made.

Validity:
* SEL-2 holds: your `Yes` of 2026-10-30; deaths are an injury outcome, unlike us_accidents' delay code.
* USE-3 was broken in the text (issue 3): "a crash has been recorded; its deaths are predicted" is the fact
  glioma_grading_clinical_and_mutation_features was set to `No` on (a label already on file). The definition now names
  what sets this task apart: the agency acts on the expected deaths given a crash's circumstances, as the relative
  severity index of the Highway Safety Manual (ch. 4) does, and no record holds that expectation. The fit stays
  approximate: one crash against a decision per section and year, no traffic exposure, the death-counting window
  stated nowhere, and deaths revised in place (41 of 3,210 crashes of 2022 changed when the ministry re-coded them
  in 2024).
* LEAK-10 holds for 24 of the 26 features: the injuries, the report date and time (fatal crashes reach the register
  sooner) and the accident code are dropped. The officer's cause and collision type are kept under its case-by-case
  clause with a note (issue 1). The gaps of incomplete records (a highway crash without a km post, a rural-road crash
  without a first vehicle: almost never fatal) stay with a note, mechanism open (LEAK-6).
* SPLIT-9, SPLIT-10 and SPLIT-14 hold: no training crash was reported after its window starts, the two-month gap is the
  median reporting delay, and the oldest window trains on 58% of the rows.
* PROV-8 and PROV-13 hold: built from the ministry's files, not the Kaggle copy. The 2022 file writes a crash date as
  day/month when both parts are 12 or less and as month/day otherwise; the repaired dates agree with the Kaggle copy on
  17,179 of 17,179 and put the holiday peaks on 1-3 January and in Songkran. EV-7 was triggered in the notes (an XLSX
  check claimed for the 2022 report dates that was never run) and fixed: they now cite the checks that were run.

Value: TP-2, a real signal (skill 0.15-0.19 over the training mean, ROC AUC 0.84 for any death). MET-5: RMSE is the
fallback: the one paper on the register (Ratanawimon and Tanawongsuwan, EECSS 2024,
https://doi.org/10.11159/cist24.179) reports five metrics side by side. MET-10 factor: crashes with three or more
deaths (0.3%) hold 14-34% of each window's squared error, so close models are hard to tell apart. A Poisson deviance
(the domain practitioner's and the blind reviewer's choice) needs a library metric and a floor on the predictions, a
decision for all count targets of the run (MET-13).

Quality: CLEAN-10, CLEAN-11 and CLEAN-12 hold (impossible values made missing, the site code split into layout and
slope); CLEAN-21: two coding breaks in the newest test months (finer cause codes from November 2022, no route name in
December 2022) kept with a note, neither reaches a training set; CLEAN-22 keeps `route` (the blind reviewer's drop not
adopted).

Weighed: the ministry's own register, repaired and checked +; severity screening is a real practice +; approximate fit
-; test windows that end in 2022 - (issue 2).

For the curator: issue 3 (the severity-screen reading against glioma_grading_clinical_and_mutation_features, a validity
call), issue 1 (keep the officer's fields under LEAK-10's case-by-case clause), issue 2 (the year range, a weighing
call). The panel's changes are text only (rows, target, split and metric unchanged) and are made. In the record: an
`Assessment (AI, 2026-11-01)` line (the EECSS 2024 paper; AUC 0.840/0.833 replace the screening's 0.83/0.81), and
`Two-Regime Zeros` removed under your definition of 2026-10-30: a count model given the features predicts 89.2% zeros
against 89.0% observed, as for how_much_did_it_rain_ii (a CC restores it).

**Main points:** Accept the severity screen as what sets this task apart from
glioma_grading_clinical_and_mutation_features (issue 3), keep the officer's presumed cause and collision type with a
note (issue 1), and ship 2019-2022 or rebuild to 2025 (issue 2).

**Issues for Andrej:**

3. **Accept the severity screen as what sets this task apart from glioma_grading_clinical_and_mutation_features?** When
   a crash is in the register, its deaths are in the same record, so read literally the model predicts a count already
   on file. glioma_grading_clinical_and_mutation_features was set to `No` on that fact (Lennart, 2026-10-26: "a model
   can only cross-check a label that already exists"). The definition now reads the task as the severity part of
   network screening: a road agency needs the expected deaths of a crash given where, when and how it happened, and no
   record holds that expectation, only one realised count.
   * What it changes: this reading makes every field entered with the crash an input, the officer's cause included
     (issue 1), with an approximate fit (one crash against a decision per section and year, no traffic exposure). A
     first-report reading (deaths not yet known) would drop the cause and needs an actor no source names.
   * Evidence: the Highway Safety Manual's relative severity index (ch. 4) and the rural roads department's equivalent
     accident number rank sites by expected severity; the domain practitioner would use the model "as a severity
     screen", and the blind reviewer reached the same reading on its own. The register has no first-report snapshot:
     every field is entered in one record, a median 53 days after the crash.
   * Rule: USE-1 and USE-3 (Must). Precedent: departs from glioma_grading_clinical_and_mutation_features with the fact
     named. noaa_storm_events_damage (same run, not yet decided) puts its prediction point at the first report and
     drops the fields written with the outcome; the mediator separates them by when the actor acts (a storm damage
     estimate before the survey, a road agency after the crash is recorded). Your call becomes the Cases row for
     incident registers.
   * The critic first asked for a first-report point and accepted the severity screen as the milder remedy.
   * Implemented: the severity screen in the prediction-point bullet, `use_case`, `known` and `fit_reason`.
   * Alternative: a first-report prediction point, dropping `presumed_cause` (R^2 0.171 to 0.166); or `No` (No Good
     Target / Scientific Discovery), as glioma_grading_clinical_and_mutation_features.

   Recommendation: accept the severity screen. Decision: accept it, move to a first report, or retire?

1. **Keep the officer's presumed cause and collision type?** The reporting officer enters the presumed cause (53
   codes, such as speeding or drunk driving) and the kind of collision in the same record as the deaths, a median 27
   days after a fatal crash. If knowing that someone died changes what the officer writes, a model learns the
   officer's habit, and an agency ranking road sections by it would rank how crashes were written up, not how they
   happened. The question arises under the severity-screen reading (issue 3); a first-report reading drops the cause
   anyway.
   * What it changes: R^2 0.171 with both fields, 0.166 without the cause, 0.162 without both (ROC AUC for any death
     0.840, 0.838, 0.833; 9 windows, untuned LightGBM).
   * The trace: on the highways, outside the New Year and Songkran campaign days (when police test drivers for alcohol
     widely), crashes coded drunk driving are fatal in 21% of cases against 11% for the rest; on campaign days, 12%
     against 12%. That fits alcohol tests made because someone died.
   * Against a leak: given the crash's hour, weekend, year, first vehicle, collision type, road layout and vehicle
     count, the off-campaign odds ratio falls from 2.10 to 1.17 (95% CI 0.88-1.57, approximate). Blanking the two
     drunk-driving codes on the 530 crashes that carry them off the campaign days loses nothing (R^2 +0.001 to +0.003
     over 3 seeds); the most those rows could carry is R^2 0.0015 (an oracle bound), about one standard error, so the
     gain at stake is small either way. The cause's gain comes from codes read at the scene (cutting in, running a
     signal, illegal overtaking, driving the wrong way: fatal in 20-48%). Speeding is the default code (75% of crashes
     without a death, 69% with one). The collision type is a fact of the scene; its blanks follow the agency.
   * Rule: LEAK-10 (Must). Its second clause (2026-10-26) keeps values whose late part cannot be located row by row
     only when the part that can be traced shows no gain, and leaves each such keep to you. Precedents:
     onlinenewspopularity (kept on that test) and distribution_transformers_at_cauca_department (dropped: the gain
     could sit on the changed rows). This call sets the precedent for the contributing-factor fields of
     nyc_motor_vehicle_collisions, chicago_traffic_crashes and nhtsa_crss_crash_severity.
   * The advocate and the critic agree on keeping; the critic asked to drop the cause and withdrew after his own
     conditional test.
   * Implemented: both kept, with a `Potential leak, kept on purpose:` note (the mechanism, these numbers, and a
     revisit if the task moves to the first report of a crash, before the deaths are known, or a TRAMS codebook dates
     the cause).
   * Alternative: drop `presumed_cause` (R^2 0.171 to 0.166), or both fields (0.162).

   Recommendation: keep both. Decision: keep, drop the cause, or drop both?

2. **Ship 2019-2022, or rebuild to 2019-2025?** The dataset holds the years the record names. The ministry's snapshot
   also holds 2023 to 2025, about 70,000 more crashes, so the test windows end almost four years before the snapshot.
   * What it changes: an agency refitting today would train on 2019-2025 and score 2026 crashes; the 2021-2022
     windows stand in for that. Two of the nine fall in the low-traffic months of 2021 (about 1,250 crashes a month
     against 1,450-1,640 in 2022).
   * For extending (the advocate's lean): 2024 and 2025 use the 2019-2022 codes (99.9-100% of labels), about 47,700
     crashes. 2023 recodes only the site and the cause (7.5% and 20% of its labels exist earlier, against 94% of its
     collision types), so it can join with those fields blank for the year, as
     force_2020_well_well_log_and_lithofacies_dataset_for_machine_learning_competition masked values without a checked
     conversion (CLEAN-21). Its 1,641 crashes entered two or three times agree on deaths in every case. The newest
     windows would be 2024-2025. noaa_storm_events_damage and crms_phragmites_cover (this run, not yet decided) test
     on their newest years.
   * For keeping (the critic's lean): this version meets every Must, and the record you marked `Yes` is named
     2019-2022 (its links list the 2019-2026 files, and the screening measured 2025). The extension is a new dataset:
     a new name, new windows and a new review, with a year of road layout, slope and cause blank, 448 conflicting dates
     among the 2023 repeats to resolve, and late-2025 crashes still arriving at the snapshot (10% of crashes reach the
     register after eight months, mostly without a death), which the rebuild must check (LEAK-24).
   * Rule: SPLIT-11 and SPLIT-20 (Should) want the newest, most representative windows and a history chosen from the
     use case; no rule fixes which years of a growing register to take, so this is a weighing call. Dropping 2019 is
     no way out: the two oldest windows would train on 49% and 46% of the rows (SPLIT-14, Must).
   * Implemented: 2019-2022; the notes give this reason and say the extension is open.
   * Alternative: rebuild as a 2019-2025 dataset (2023's site and cause blank, its repeats dropped, windows in
     2024-2025), which replaces this one.

   Recommendation: rebuild to 2019-2025 now: the extension is feasible and the notes leave it open, and after shipping
   it would replace a shipped dataset and need the same review (PROV-6). The panel is split (advocate: extend now;
   critic: ship this, extend later). Decision: keep 2019-2022, or rebuild to 2025?

**Review panel:** ship after changes (mediator). Claim audit: 48 claims, 38 hold, 5 refuted or refuted in part (all
about the notes, all fixed), 4 untested, 1 superseded. Blind review: would include with minor changes; its main
concerns were the 2019 file's missing columns, RMSE on a count with many zeros and the redundant `route` column, none
adopted (without 2019 the oldest windows fall below the training floor, SPLIT-14; a Poisson deviance is a decision for
all count targets, MET-13; a model overfitting `route` is no reason to drop it). Debate: agreed on the severity-screen
reading, the temporal split with its reporting filter and gap, the fallback metric, the text corrections and, after the
critic's own tests, keeping `presumed_cause` with a kept-leak note; left to the curator: the severity-screen reading
(issue 3), that keep (issue 1, a case-by-case call under LEAK-10) and the year range (issue 2); the `Two-Regime Zeros`
tag, which both debaters left to you, the mediator removed under your definition of 2026-10-30.

<details><summary>Mediator</summary>

**Mediator (2026-11-01): thailand_road_accident_register_2019_2022**

**Recommendation**

```text
Verdict: ship after changes (text in dataset.py and the record; rows, target, split and metric unchanged).
Validity: SEL-2 holds (CC `Yes`, priority 5, 2026-10-30; deaths are an injury outcome, not us_accidents' delay code).
  USE-1/USE-3 broken in the text: "a crash has been recorded; its deaths are predicted" is glioma_grading's fact.
  Fixed by naming the severity screen: the expected deaths of a crash given its type, place and vehicles (the
  severity part of network screening, HSM ch. 4), which no record holds. USE-5 holds with a note (counting window
  unstated; deaths revised in place). USE-8 approximate, fit_reason rewritten. LEAK-10 holds for the 26 features
  (injuries, report date and time, acc_code dropped). presumed_cause and collision_type kept under LEAK-10's second
  clause and LEAK-6 (the traced part, masked, shows no gain); that clause is the curator's case-by-case call
  (issue 1). SPLIT-6/SPLIT-13 temporal with known roads; SPLIT-9 holds (0 late training rows in 9 of 9 windows);
  SPLIT-10 holds (gap = median delay); SPLIT-14 holds (oldest train 58.4%); SPLIT-12 and SPLIT-20 reasons to write.
  PROV-8 holds (the ministry's files, MD5 4 of 4); PROV-13 holds (2022 repair, three independent checks). EV-7
  broken in the text (an XLSX check claimed for the 2022 report dates that was not run), fixed.
Value: TP-2 a real signal (skill 0.15-0.19, beats the dummy in 9 of 9, ROC AUC 0.84 for any death).
  MET-1/MET-5 fallback rmse (the one paper reports five metrics side by side); MET-11 reason corrected.
  MET-10 factor: crashes with 3+ deaths (0.3%) hold 14-34% of each window's squared error.
Quality: CLEAN-3/5/10/11/12 hold; CLEAN-21 two coding breaks in the newest test months, noted; CLEAN-22 keeps
  `route`.
Weighed: source + (the ministry's own register, repaired and checked); use case + (severity screening is a real
  practice); fit - (one crash against a section-year decision, no exposure, death window unstated); size +
  (81,059 crashes, 256-449 fatal per test window); recency - (test windows end in 2022).
For the curator: issue 1 (keep presumed_cause with a kept-leak note, LEAK-10 second clause); issue 2 (2019-2022,
  or a rebuild to 2025: a weighing call).
```

The advocate and the critic reach the same verdict. After the rebuttals they agree on every change below, including
the keep of `presumed_cause`: the critic withdrew the drop after his own conditional test and masking runs. Two points
stay open, and both are calls the rules give to the curator: the LEAK-10 clause on `presumed_cause` ("each a
case-by-case judgment of the curator") and the year range (a weighing call). Neither side asks for exclusion. No Must
is unmet once the text changes are made.

Decisive checks of mine:
* The `splits_comment` RMSE triple, which the split auditor traced to a pre-definition frame, rerun on
  the shipped frame with the builder's model. Without the two route-name columns (the builder's feature set): 0.3616
  trained on every earlier crash, 0.3619 on those reported by the window start, 0.3628 with the gap (builder:
  0.3613 / 0.3619 / 0.3630). With every shipped feature: 0.3670 / 0.3673 / 0.3688. Filter against all prior +0.0002
  (paired SE 0.0009); filter and gap +0.0011 (SE 0.0012). The date-built gap design has exactly the shipped train
  sizes in 9 of 9 windows. The claim "change little" holds; the numbers need the shipped frame.
* The "swapped" coordinate pair the column auditor would swap back is (100.0, 13.0), whole degrees
  with no province: a placeholder, not a position. Blanking it stands; the nit is not adopted.

**Agreed facts**

* 81,061 rows of the four 2026-10-30 CSVs (MD5 4 of 4), 2 exact duplicates dropped, 81,059 ship. Yearly deaths match
  the ministry: 3,223, 3,301, 2,715, 2,619. Agencies: DOH 92.8%, DRR 6.3%, EXAT 0.8%.
* Target: 70,958 zeros (87.5%), 8,794 ones, 1,307 with 2-13. A Poisson model given the features predicts 89.2%
  zeros on the test windows against 89.0% observed; a negative binomial with the target's mean and variance and no
  extra zeros gives 87.9% against 87.5%. No excess zeros.
* The count given a death is weakly predictable: R^2 +0.032 on the fatal crashes (regularised Poisson LightGBM),
  positive in 9 of 9 windows. The note's -0.049 is an untuned model overfitting.
* Reporting delay: median 53 days (27 for a fatal crash, 57 otherwise); 10.1% after 240 days. Of crashes reported
  within a week 17.8% had a death, against 8.1% after 120 days. The report date and time are rightly dropped.
* Splits: 9 two-month windows, Nov-Dec 2022 back to Jul-Aug 2021; 2,492-3,978 test and 47,333-69,688 train crashes
  (58.4-86.0%); no training row reported on or after its window start; gap at least 2 months; 177 rows in no split
  (reported Dec 2022-Jun 2023). Routes recur for 92.7% of test rows, provinces for 100%. Crashes 2-4 months before a
  start are 48-96% reported, fatal share 0.113-0.146 among the reported against 0.100-0.124 among all. Mean
  prediction over truth 0.96-0.98: no bias measured.
* The 2022 crash-date repair holds: Kaggle agrees on 6,088 of 6,088 changed dates and 11,091 of 11,091 others; the
  XLSX cells agree on 8,135 of 8,135 ambiguous dates; the holiday peaks fall on 1-3 January and in Songkran. For the
  2022 report dates the XLSX gives the opposite reading for 6,823 dates; the shipped CSV reading leaves 0 crashes
  reported before they happen (1,579 under the XLSX reading), and Kaggle agrees on 99.98%. The builder's XLSX script
  covered 2023-2025 only.
* Duplicates: the 2020 pair has consecutive codes, the 2022 pair codes 15 apart in adjacent rows. 4 more pairs share
  crash time and exact coordinates with equal deaths; each falls in one window.
* Years: in 2023 only 7.5% of site labels and 20.0% of cause labels exist in 2019-2022, against 94.0% of collision
  types; 1,641 codes are held two or three times (1,702 extra rows), and their copies agree on deaths in 1,641 of
  1,641 (448 differ in the date text). 2024 and 2025 use the older labels (99.9-100%), about 47,700 crashes.
  Dropping 2019 puts the two oldest windows at 49.4% and 45.5% of the rows (below SPLIT-14).
* `presumed_cause`: the column adds R^2 +0.0077 (SE 0.0021), RMSE -0.0017 (SE 0.0005), helping in 8 of 9 windows.
  Trace: on DOH roads off the New Year and Songkran campaign days, the drunk-driving code is fatal in 0.213 of 315
  crashes against 0.113; on campaign days 0.116 against 0.118. Masking the traced part (530 crashes) changes R^2 by
  +0.0011 to +0.0033 over 3 seeds (no gain lost); the oracle bound of what that part could carry is 0.0015 on average,
  about one paired SE (0.0013): the test is weak, and so is the gain at stake. Conditional logit (DOH, given hour,
  weekend, year, first vehicle, collision type, layout, vehicles): off-campaign odds ratio 1.17 (95% CI 0.88-1.57)
  against 2.10 raw; on campaign days 0.68 (0.50-0.93). The Newton fit warned of non-convergence; BFGS gives the same
  estimates, so the intervals are approximate. "Speeding" is the code of 75% of non-fatal and 69% of fatal crashes.
  The column's gain sits on codes read at the scene (cutting in 0.200, running a signal 0.245, illegal overtaking
  0.277, wrong way 0.479 fatal).
* `collision_type` blanks follow the agency: within DOH blank rows are fatal 0.047 against 0.111, within DRR 0.300
  against 0.352; the DRR stopped recording the field after 2019 (3,425 of 3,547 blank in 2020-2022).
* Gaps in incomplete records: 213 DOH crashes without km, 4 fatal (0.019 against 0.114); 73 DRR crashes without a
  first vehicle, none fatal (DRR base 0.30). Masking them costs R^2 0.0028 (SE 0.0009). Mechanism open.
* Agencies record differently: property-damage-only crashes are 10-12% of DRR records, 43-48% of DOH and 65-76% of
  EXAT; DRR fatal share 0.28-0.32 against 0.10-0.12. Every EXAT crash lacks `presumed_cause`.
* Coding breaks: records entered from November 2022 use finer cause codes (591 crashes, 577 reported Nov 2022 or
  later); 1,527 crashes entered in December 2022 have no route name but keep `route_code`. Neither reaches a training
  set; 64 of 3,537 rows of the newest window carry a cause code unseen in training.
* Deaths are revised in place: 41 of 3,210 re-keyed 2022 crashes changed deaths between the Kaggle copy and today
  (32 down, 9 up). The counting window is stated nowhere searched.
* Metric: no source metric. Ratanawimon and Tanawongsuwan (EECSS 2024, CIST 179, DOI 10.11159/cist24.179) classify
  fatal against injured on the 81,735 Kaggle-era records, random 80/20, reporting precision, recall, F1, balanced
  accuracy and ROC AUC side by side. RMSE ranks six models as the per-section Spearman does (tau 1.0); top models
  differ by 0.0010-0.0015 with paired SE 0.0013-0.0020.

**Changes to make now (no decision needed)**

1. Prediction point (USE-1, USE-3, Must). Rewrite the first `curation_comments` bullet, `use_case` and `known`: the
   moment is a road agency screening its recorded crashes; the quantity is the expected deaths of a crash given its
   circumstances, which no record holds (each holds one realised count). Name the severity part of network screening
   (HSM ch. 4 relative severity index; DRR's equivalent accident number). Drop "and enforcement" from `use_case`
   (the highway police's decision, not the engineer's). This is the fact that sets the task apart from glioma_grading.
2. `fit_reason` (USE-8, USE-5, Must). Keep approximate. Name: one crash against a decision per section and year, with
   no crash frequency or exposure; the unstated death-counting window; deaths revised in place (41 of 3,210). Name
   `presumed_cause` and `collision_type` as kept, not as a gap (USE-8 as amended, kick and eight others). Drop "the
   source names no user".
3. Officer's fields (LEAK-10, LEAK-6; implements issue 1's default). Replace the "Note:" bullet with `Potential leak,
   kept on purpose:` giving the mechanism (entered when the outcome is known), the drunk-code trace, the conditional
   and masking numbers above, that the column's gain sits on codes read at the scene, and a revisit condition (a
   first-call framing, or a TRAMS codebook that dates the cause). Add a `_decisions` table (trace and masking).
   Remove "they carry little of the signal" as a reason (LEAK-10: not a reason alone).
4. Gaps and agencies (LEAK-6, LEAK-10 "missingness that encodes the outcome"; USE-5). In "Missing values": the km and
   first-vehicle gaps are almost never fatal (numbers above, mechanism open, kept); the blank collision types are the
   DRR's; the agencies record to different thresholds (property-damage-only shares) and every EXAT crash lacks a
   cause.
5. Time bullet and `DATE_ORDER` comment (EV-7 Must, PROV-13). Replace "checked against the XLSX files" for the 2022
   report dates by the evidence that was run: 0 crashes reported before they happen against 1,579 under the XLSX
   reading, the accident-code order (172 against 518 dates more than 30 days off their neighbours), Kaggle 99.98%.
   Say the 2022 XLSX (revised 2025-07-23) swaps day and month for 6,823 report dates.
6. Duplicates bullet (PROV-6, LEAK-19). "Adjacent rows", not "consecutive accident codes". Name the 4 near pairs and
   that each falls in one window; no drop (not exact copies; 4 of 81,059 rows, no copy across the split).
7. Years bullet (EV-7, PROV-9). The site and the cause changed scheme in 2023, not the collision type (94% of its
   labels carry over); 1,641 crashes are held two or three times. State the true reason for stopping at 2022: the
   scope of the approved record. Say that 2024-2025 use the older scheme and that an extension with 2023's site and
   cause masked is possible and open (issue 2). Do not claim it needs a crosswalk of our own.
8. Zero-inflation bullet (EV-6). Count given a death: weakly predictable (R^2 0.03, positive in 9 of 9 windows; an
   untuned model overfits to -0.05). No excess zeros: 89.2% predicted against 89.0% observed.
9. Metric reason (MET-11 Must, MET-5, MET-10). Add the EECSS 2024 paper (binary, random split, five metrics side by
   side: fallback under MET-5) in place of "no paper was found". Add: crashes with 3+ deaths, 0.3% of test rows, hold
   14-34% of each window's squared error, and the top models differ within their paired SE.
10. `splits_comment` (SPLIT-10, SPLIT-12, SPLIT-20, Should; EV-8).
    * The gap is about the median delay; crashes 2-4 months old are still partly reported and more often fatal, as at
      a real refit; no bias measured (prediction over truth 0.96-0.98).
    * The cadence is ours (no source horizon): two-month windows are the shortest that fill 9 windows and cover every
      season once; quarterly windows keep the floor for only 7.
    * The full expanding history is kept, with its breaks: 2019 lacks per-type counts and route codes, April 2020
      halved (COVID-19, no Songkran), deaths per crash fall from 0.168 (2019) to 0.127 (2022), the two oldest test
      windows fall in the 2021 low-traffic months.
    * Replace the RMSE triple with the shipped-frame numbers (+0.0002 and +0.0011 against training
      on every earlier crash, paired SE 0.0009 and 0.0012).
11. Coding breaks (CLEAN-21). One sentence each on the November 2022 cause codes and the December 2022 blank route
    names, both only in test rows.
12. Record. An `Assessment (AI, 2026-11-01)` line: the EECSS 2024 paper exists (supersedes "no paper found"), the
    screening's AUC 0.83/0.81 superseded by 0.840/0.833, the severity-screen reading, and the tag below.
13. Record tag. Remove `Two-Regime Zeros` under the curator's definition of 2026-10-30 ("independent of the remaining
    target distribution"): the zero share is what one count model gives (89.2% against 89.0%), and the hurdle adds
    R^2 0.003. Same facts as how_much_did_it_rain_ii (removed 2026-10-30). The dataset ships either way (policy 2).

Not adopted: drop `route` (blind reviewer; a model overfitting a high-cardinality column is no reason, CLEAN-22, EV-4;
my run shows LightGBM loses 0.005 RMSE with it, a model limit); drop 2019 (SPLIT-14); swap back the (100, 13) pair
(m2); a Poisson deviance for this dataset alone (MET-13: a decision for all count targets of the run, not this one);
archiving the snapshot (MD5 pinned; no precedent asks more).

**Changes that need the curator**

1. **Keep `presumed_cause` and `collision_type` with a kept-leak note?** (P4; LEAK-10 Must, second clause of
   2026-10-26, with LEAK-6's narrowing.)
   * Problem: the officer writes both when the deaths are known. If a death changes what gets written, the model
     learns the recording, and a section ranking would follow the officer's coding.
   * Advocate's best evidence: the trace sits on one code; masking it loses nothing (R^2 +0.0011 to +0.0033), and
     the most that part could carry is R^2 0.0015; the conditional test removes the off-campaign trace (OR 1.17, CI
     0.88-1.57). Both fields are the agency's own inputs (USE-6; breast_cancer_prediction's reading).
   * Critic's best evidence (withdrawn after his checks): the column's gain is real (R^2 +0.0077, 3-4 SE), and the rows
     a late reading may affect cannot be located beyond the one code (distribution_transformers was dropped on that).
   * The rule settles which test applies (the traced part shows no gain, onlinenewspopularity) but leaves the call to
     the curator. It becomes the precedent for the contributing-factor fields of nyc_motor_vehicle_collisions,
     chicago_traffic_crashes and nhtsa_crss_crash_severity.
   * Implemented: keep both with the note. Alternative: drop `presumed_cause` (R^2 0.171 to 0.166, AUC 0.840 to
     0.838), or both (0.162, 0.833). Recommendation: keep.
2. **Ship 2019-2022, or rebuild to 2019-2025?** (P4; SPLIT-11, SPLIT-20, Should; a weighing call.)
   * Problem: the test windows end in December 2022, four years before the snapshot, because the record names
     2019-2022.
   * For extending (the advocate's lean): 2024-2025 use the older coding, about 47,700 crashes; 2023 can join with
     its site and cause masked (CLEAN-21, force_2020) and its repeats dropped (deaths agree in 1,641 of 1,641); the
     newest windows would be 2024-2025 and none in the 2021 low-traffic months; the same-run noaa_storm_events_damage
     and crms_phragmites_cover test on their newest years.
   * For keeping (the critic's lean): the shipped version meets every Must; the `Yes` was given on the 2019-2022
     record; extending is a rebuild with a new name and a new review, with a year of road layout, slope and cause
     masked, 448 conflicting dates to resolve, and late-2025 crashes still being reported at the snapshot (10.1% of
     crashes arrive after 8 months, 2.8% after a year, mostly non-fatal), which a rebuild would have to check
     (LEAK-24).
   * What would settle it: the curator's weight on recency against a second build and review. Either version ships;
     only one can (PROV-6).

**Disputed points, settled**

* Prediction point (USE-3 against the glioma precedent). Critic: name a first-report point or the fact that sets the
  task apart; advocate: the severity screen is that fact. Settled for the severity screen, both agreeing: it is the
  mildest remedy, two agents found the practice independently (domain practitioner with HSM ch. 4 and DRR's EAN;
  blind reviewer), and no practitioner predicts deaths from a first TRAMS report (USE-9 needs a use case
  practitioners have). The critic's narrowing (the first bullet must change too) is adopted in change 1.
* `presumed_cause` (LEAK-10). Settled as a keep by both after the critic's conditional test; it stays an issue only
  because the clause leaves the call to the curator.
* Years bullet (EV-7). The critic: it must not claim 2023 needs a crosswalk of our own. The advocate conceded; change 7
  writes the true reason. The range itself is issue 2.
* The `Two-Regime Zeros` tag. Both called it the curator's call. The facts are agreed (no excess zeros), and the
  curator's definition with the how_much_did_it_rain_ii precedent decides it, so it is change 13, reversible by a CC.

**Consistency with precedent**

* glioma_grading_clinical_and_mutation_features (`No`, Lennart, 2026-10-26): departed from, with the fact named
  (change 1): the actor acts on expected deaths per crash type and section, which no record holds; there the model
  could only reproduce a diagnosis on file.
* distribution_transformers_at_cauca_department (dropped) against onlinenewspopularity (kept): the keep follows
  onlinenewspopularity, because here the traced part is located and shows no gain. Issue 1 asks the curator, as the
  clause requires.
* noaa_storm_events_damage (same run, undecided) puts its prediction point at the first report and drops fields
  written with the outcome. What sets this case apart: the road agency acts after the crash is recorded, on expected
  severity; a storm damage estimate is needed before the survey. Once decided, both become Cases rows for incident
  registers.
* kick and eight others (USE-8 as amended): followed (change 2).
* house_sales and brazilian_ecommerce (gap about the median delay): followed. sf_permit_time widened its gap for a
  measured bias; none is measured here.
* fremtpl2 (Andrej, injuries next to the target dropped), 2_month_survival and kick (report timing dropped):
  followed. avito_demand_prediction_1m (labels in the source's language): followed.
* churn_telco_south_asia and gallstone_disease (fallback; a paper with several metrics side by side): followed.
* how_much_did_it_rain_ii (tag removed under Andrej's definition): followed (change 13).
* No drift in Andrej's calls; no third exception; the open SPLIT-10 amendment is untouched (a gap is kept).
* Cases rows due when the curator decides: the officer's reading in a crash register (LEAK-10), and the year range of
  a growing register whose coding changed (SPLIT-20).

</details>

<details><summary>Claim audit</summary>

**Claim audit (claim-auditor, 2026-11-01): thailand_road_accident_register_2019_2022**

Verdict: no validity claim (P1-P5) is refuted. The shipped data, the splits and the metric are what the definition says
they are. Of 48 claims, 38 hold, 5 are refuted or partly refuted, 4 are untested and 1 is superseded by a later
measurement. All 5 refutations are about documentation or how a probe was read, and none changes the frame or the
splits. The declared metric (fallback `rmse`)
holds. Its reason says no paper was found, but there is one (EECSS 2024). That paper reports five metrics side by side,
so MET-5 still sends the task to the fallback. The metric scores on all 9 test folds.

Tests were run on the definition's own frames: `_load_raw`, `_clean`, `process` and `to_container`, rebuilt from the
2026-10-30 CSVs (MD5 sums match 4 of 4). They were checked against the Kaggle copy, the ministry's XLSX files, the
CKAN metadata and the 2023-2025 files. Model numbers come from untuned LightGBM on the 9 shipped windows
(EV-8).

**Claims table**

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 1 | Deaths per crash on the ministry's highways, rural roads and expressways | task_summary.question | agency counts in the shipped frame | holds | Department of Highways 92.8%, Rural Roads 6.3%, Expressway Authority 0.8% | USE-1 |
| 2 | A safety engineer ranks road sections from expected deaths per crash ("for example") | task_summary.use_case | the source names no actor | untested | CKAN `objective`: "to serve the public" only; this is a call for the domain practitioner | USE-1 |
| 3 | One crash per row, 81,059 crashes | task_summary.row | row count after cleaning | holds | 81,061 raw rows, 2 duplicates dropped, 81,059 left | |
| 4 | Most crashes have no death; how long a death still counts is not stated | task_summary.predicted | zero share; one more search | holds | 87.54% are zero. No definition on the CKAN page (16 resources, no codebook) or in the MOT 2565 PDF; the OTP 2020 analysis returned 403 | USE-5 |
| 5 | Features known at prediction time, including counts by vehicle type from 2020 | task_summary.known | shipped columns; missing values by file | holds | 26 features as listed. Counts by type and route_code are missing for all 19,194 crashes of 2019 and for none from 2020 | LEAK-1 |
| 6 | Two-month test windows from Jul 2021 to Dec 2022; training crashes at least 2 months older and already in the register | task_summary.split, splits_comment | every split, recomputed from report times aligned to `process()` | holds | In 9 of 9 windows: every training crash was reported before the window starts, the newest training crash is at least 2 months before the start, the test set is every crash of the 2 months, and train and test share no row | SPLIT-6, SPLIT-9 |
| 7 | Changes: the ministry's files, the 2022 repair, injury counts dropped, a reporting filter | task_summary.changes | code and frame | holds | See rows 17-22 | |
| 8a | The source names no user | fit_reason | CKAN metadata | holds | `objective` is ["to serve the public"] | USE-1 |
| 8b | The officer records the presumed cause and the collision type when the outcome is known | fit_reason, curation note | report delay | untested (circumstantial) | Records are entered a median of 27 days (fatal) and 57 days (other) after the crash. Whether the officer's reading depends on the outcome cannot be tested on this data | USE-3, LEAK-10 |
| 8c | Roads and provinces recur | fit_reason | hidden-group probe | holds | 92.7% of test routes and 100% of test provinces appear in train | SPLIT-13 |
| 9 | Licence Open Data Common; open access | `license` | CKAN package_show | holds | `license_id` is "Open Data Common"; `accessible_condition` is "no restriction" | EV-4 |
| 10 | Files revised in place (2019 on 2026-05-26, 2020-2022 on 2024-06-14); MD5 sums | download_description | CKAN `last_modified`; md5sum | holds | Both dates match the CSV resources and the 4 MD5 sums match. Not stated: the 2022 XLSX was revised again on 2025-07-23, after the CSV | PROV-9 |
| 11 | Domain social science, as the 2015 sibling | `domain` | sibling records | holds | thailand_road_accident_fatalities_2015, nhtsa_crss_crash_severity and chicago_traffic_crashes are all social science | |
| 12 | Nothing recorded with the crash's other outcomes is a feature | curation, prediction point | dropped columns | holds | Dropped: injuries (serious, minor, total), the vehicles-and-pedestrians total, report date and time, and `acc_code` (it follows the order of entry, so it carries the report delay) | LEAK-10 |
| 13 | TRAMS is published by the ICT Centre with no codebook, task or metric | curation, Source | CKAN metadata | holds | `data_source` is TRAMS; all 16 resources are yearly CSV and XLSX files | MET-1 |
| 14 | 21,040 of 21,239, 19,869 of 20,062 and 17,180 of 20,566 crashes carry a Kaggle code; on those, deaths agree in every row | curation, Source | merge on acc_code | holds | 21,040, 19,869 and 17,179 after the duplicate drop; deaths equal 1.000. Not stated: the June 2024 revision re-keyed 3,210 of the 3,386 new 2022 codes (same crash time and coordinates as a dropped Kaggle row). On those, deaths changed for 41 (32 down, 9 up) | PROV-9, LEAK-24 |
| 15 | 2023 codes the site, the cause **and the collision type** in another scheme | curation, Years | share of 2023 crashes whose label exists in 2019-2022 | partly refuted | Site 7.5% and cause 20.0% (another scheme, holds). Collision type 94.0% (the same scheme in substance). "Straight, no slope" is 50 in 2023 against 13,409-16,810 in other years (holds) | PROV-9 |
| 16 | 2023 holds 1,641 crashes twice; 2024-2025 use the older scheme | curation, Years | repeated codes in 2023; label overlap for 2024-2025 | holds (wording) | 1,641 codes repeat, with 1,702 extra rows, so some appear three times. 2024-2025 share 99.9-100% of the old labels | PROV-6 |
| 17 | Date order per file (2019 d/m/Y, 2020-2022 m/d/Y), one 2020 Excel day number, "checked against the XLSX files and the Kaggle copy" | curation, Time; `DATE_ORDER` comment | parse each file; compare with the XLSX date cells and with Kaggle | data holds; the XLSX part is refuted for 2022 report dates | The shipped orders give 0 unparsed dates and 0 crashes reported before they happened in each file; the other order leaves 11,631-14,329 dates unparsed. The XLSX agrees on 100% of the 2019-2021 crash dates and the 2019 report dates. But the 2022 XLSX date cells give the opposite day/month reading for 6,823 report dates. The shipped CSV reading is the right one: 172 report dates are more than 30 days off their accident-code neighbours against 518 for the XLSX, and 0 crashes are reported before they happened against 1,579. Kaggle agrees with the shipped reading on 99.98%. The builder's XLSX comparison loops over 2023-2025 only | PROV-13, EV-7 |
| 18 | 2022 repair: 2,472 crashes reported before they happen under the naive reading, 7,268 dates change, Kaggle agrees on 6,088 of 6,088 and 10,345 of 10,345 | curation, Repair; Decision 2 | recomputed | holds | 6,088 of 6,088 changed dates agree with Kaggle, and so do all 11,091 others (10,345 plus 746 dates whose day equals the month). The XLSX date cells agree on all 8,135 ambiguous crash dates as well | PROV-13 |
| 19 | The 2019 file ends in 21,052 empty rows | curation | raw read | holds | 40,246 rows; the last 21,052 are all empty | |
| 20 | Two crashes entered twice under consecutive accident codes, one record of each kept | curation, Duplicates | exact duplicates; same crash time and exact coordinates | partly refuted | The 2020 codes are consecutive (7678227 and 7678228). The 2022 codes are 15 apart (7508085 and 7508100, adjacent rows). 4 more pairs share crash time and exact coordinates with equal deaths: 1 differs only in collision type, 2 only in report time plus km, weather or vehicle_1, and 1 in 6 fields. Each pair falls in a single window | PROV-6 |
| 21 | Route class copies the agency; vehicles-and-pedestrians = vehicles + pedestrians; bus and farm-vehicle counts are 0 and counted under other vehicles | curation, Dropped | crosstab; sums; rows whose first vehicle is a bus or farm vehicle | holds | The route class maps 1:1 to the agency (missing in 2019). The sum identity holds in 100% of 2020-2022 rows. Bus and farm counts are 0 in all 61,867 rows. n_other_vehicle ≥ 1 in 275 of 275 large-bus rows and 53 of 53 farm-vehicle rows | CLEAN |
| 22 | Report date: median 27 and 57 days; 15-20% fatal within a week, 8% after four months | curation; Decision 3 | recomputed | holds | 27.0 and 56.8 days; 17.8% fatal within 7 days, 8.1% after 120 days | LEAK-10 |
| 23 | Site split into layout and slope; slope present for 70,154 crashes | curation, Site | count | holds | 70,154 | CLEAN-12 |
| 24 | 4 coordinate pairs out of range (one swapped), 211 missing; 86 vehicle counts made missing; 20 pedestrian-first crashes keep 0; collision type missing for 50 crashes in 2019 and about 1,200 a year after | curation, Missing values | recomputed | holds | 4 pairs (including 100/13); 211; 86 and 20; collision type missing 50, 1,198, 1,186 and 1,317 | CLEAN |
| 25 | Cause and collision type carry little signal (R² 0.171/0.166/0.162, AUC 0.840/0.838/0.833) | curation, Note | second check on the declared metric: Poisson LightGBM RMSE with and without the two fields | holds | RMSE 0.3632 / 0.3644 / 0.3661 against 0.4022 for the train mean, so the two fields carry 7% of the gain | LEAK-10, EV-6 |
| 26 | 70,958 zeros, 8,794 crashes with one death, 1,307 with two to thirteen | curation, Zero inflation | value counts | holds | Exact | |
| 27 | "How many die once someone does is not predictable from these fields (R² −0.049 on the fatal crashes)" | curation, Zero inflation | second model on the fatal crashes: a regularised Poisson LightGBM (7 leaves, at least 200 rows per leaf, 200 trees) against the train mean | **refuted** | R² +0.032, positive in 9 of 9 windows (0.006-0.111); Poisson D² 0.048; Spearman 0.16; the train mean scores −0.003. The −0.049 comes from the untuned model (400 trees, 50 rows per leaf) overfitting 6-9k positives | EV-6, EV-3 |
| 28 | Hurdle R² 0.174 against 0.171; an oracle that knows which crashes are fatal reaches 0.820 | curation | the builder's hurdle probe | holds (not re-run) | Matches the probe | |
| 29 | How long a death counts is not stated anywhere we looked | curation, Note | looked again | holds as a search report | See row 4 | EV-7 |
| 30 | Report delay median 53 days, 27 fatal and 57 other; one in ten after more than eight months | splits_comment | recomputed | holds | 53.3, 27.0, 56.8; 10.1% after more than 240 days | |
| 31 | 941-4,790 crashes left out; 2,492-3,978 test and 47,333-69,688 train crashes (58-86%) | splits_comment; Decision 1 | recomputed | holds | Exact | |
| 32 | The 2-month gap leaves out the months where the reported share is lowest | splits_comment | the builder's reporting probe by window | holds | 7-59% of crashes 0-2 months old are reported, against 48-96% at 2-4 months. The newest training month is still skewed: deaths per crash, all against reported, are 0.111 / 0.146 in the 2022-11 window | SPLIT-10 |
| 33 | RMSE 0.3613 (all earlier crashes), 0.3619 (reported only), 0.3630 (with the gap) | splits_comment | independent Poisson LightGBM on the shipped splits | holds | 0.3632 on the shipped design | EV-8 |
| 34 | Metric reason: the dataset page has no task, codebook or metric | metric reason | CKAN | holds | Row 13 | MET-1 |
| 35 | Metric reason: the Kaggle copy has no competition, discussion or notebook | metric reason; screening | Kaggle API `kernels list --dataset` | untested (consistent) | The API answers "Not found" for this upload but lists notebooks for both sibling uploads; the web page could not be read | MET-1 |
| 36 | Metric reason: "no paper on the register was found at screening" | metric reason; screening block | web search, paper read | **refuted (fallback unchanged)** | Ratanawimon and Tanawongsuwan, EECSS 2024, CIST 179 (DOI 10.11159/cist24.179): "81,735 accident records from the road network of the Ministry of Transport", fatal against injured, random 80/20 split, "Precision, Recall, F1-Score, Balanced Accuracy, and the ROC-AUC" side by side, none named as the criterion. A binary severity task with several metrics, so MET-5 gives the fallback | MET-1, MET-5, MET-11 |
| 37 | Poisson deviance is not in the library and needs strictly positive predictions | metric reason | `metrics.py` | holds | No Poisson or Tweedie metric is registered | MET-13 |
| 38 | rmse is computable on our data and folds | metric | `scorer(container)` on a dummy and on the train mean, every fold | holds | 9 of 9 folds score (dummy 0.57-0.62, train mean 0.37-0.43). Per test fold: 256-449 fatal crashes. Caveat: 6-16 crashes with 3 or more deaths per fold carry 15-29% of the train mean's squared error (MET-10 resolution factor) | MET-2, MET-10 |
| 39 | Target on the source scale | metric | `target_transform` | holds | identity; deaths per crash | MET-3 |
| 40 | Warning splits_rows_unused: 177 crashes reported after the newest window starts, older than the oldest test window | proposed acceptance | unused rows | holds | Crashes from 2020-01-16 to 2021-05-29, reported 2022-12-09 to 2023-06-23 (656-1,254 days later) | SPLIT-9 |
| 41 | Warning task_target_value_dominant: the zeros are observed | proposed acceptance | raw deaths | holds | The target is int64 with no missing value after `to_numeric(errors="coerce")`, so no blank deaths were filled | TP |
| 42 | Screening: Kaggle 81,735 × 18; its 2019 equals the ministry's (19,194 crashes, 3,223 deaths); 2025 has 38 columns; zeros 87.6% and 89.9%; median delay 49 days | record | recomputed | holds | 81,735 × 18; 19,194 / 3,223; 38; 0.876 / 0.899; 48.7 days | |
| 43 | Screening: AUC 0.83, 0.81 without cause and collision type | record | later measurement | superseded | The builder measured 0.840 and 0.833 on the ministry's data (EV-2: a later stage wins) | EV-2 |
| 44 | Screening: the Kaggle card links a Ministry of Tourism and Sports page by mistake | record | the Kaggle metadata | holds | It links mots.go.th | PROV-15 |
| 45 | Implied: no copy across the split | (implied) | exact and near copies | holds | 0.2% of test rows have an exact feature copy in train; the 4 near-duplicate pairs share a crash time, so each falls in one window | SPLIT-1 |
| 46 | Implied: the target is the real-world deaths | (implied) | how deaths are counted | untested | No counting window is documented. 41 of 3,210 re-keyed 2022 crashes changed deaths in the 2024 revision, so labels are revised in place | USE-5, LEAK-24 |

**Refuted claims, ranked (principles.md: P5 before P6; none are validity failures of the data)**

1. **Time bullet and `DATE_ORDER` comment, "checked against the XLSX files" (P5, PROV-13 and EV-7, row 17).** The
   shipped readings are right. But for the 2022 report dates the XLSX contradicts them on 6,823 dates, and the
   builder's XLSX script covered only 2023-2025. *What it changes:* nothing in the data. The evidence for the 2022
   report dates is the accident-code order (172 dates off against 518) and the negative-lag count (0 against 1,579),
   not the XLSX. *Mildest remedy:* one clause in the Time bullet: "2022 report dates: the XLSX date cells swap day and
   month for 6,823; the CSV's month/day reading follows the accident-code order and leaves no crash reported before
   it happened (the XLSX's leaves 1,579)."
2. **Duplicates bullet (P5, PROV-6, row 20).** The 2022 pair's codes are not consecutive, and 4 more pairs share crash
   time and exact coordinates with equal deaths. The pair that differs only in collision type is almost certainly
   one crash. *What it changes:* at most 4 of 81,059 rows. Each pair sits in a single window, so there is no copy
   across the split. *Mildest remedy:* reword to "adjacent rows", and either name the 4 near pairs in the note or drop
   the 2 that differ only in report time and one field.
3. **Years bullet, "collision type in another scheme" (P5, PROV-9, row 15).** 94% of 2023 crashes carry a 2019-2022
   collision label. Only the site (7.5%) and the cause (20%) changed scheme. *What it changes:* the stated reason to
   stop at 2022 still holds through site and cause, so the decision stands. The wording overstates it, and this
   bears on draft issue 3 (extend to 2024-2025). *Mildest remedy:* "codes the site and the cause in another scheme".
   Also "1,641 crashes held two or three times".
4. **Zero inflation, "how many die once someone does is not predictable (R² −0.049)" (P6, EV-6, row 27).** A
   regularised Poisson model reaches R² +0.032 on the fatal crashes, positive in all 9 windows (D² 0.048, Spearman
   0.16). *What it changes:* the second regime is weak but real, which supports the record's "Two-Regime Zeros" tag
   rather than undermining it. A curator weighing the count target against a binary "any death" target should not
   read the count part as noise. *Mildest remedy:* "weakly predictable from these fields: R² 0.03 on the fatal crashes
   with a regularised Poisson model, positive in 9 of 9 windows; an untuned model overfits to −0.05".
5. **Metric reason and screening block, "no paper on the register was found" (P6, MET-1 and MET-11, row 36).** A
   2024 paper uses the 81,735 records. *What it changes:* the fallback stays `rmse`: the paper's task is binary,
   its split random, and it reports five metrics side by side (MET-5). Only the "where we looked" text is wrong.
   *Mildest remedy:* add to the reason: "Ratanawimon and Tanawongsuwan (EECSS 2024) classify fatal against injured
   crashes in the Kaggle-era 81,735 records on a random split and report precision, recall, F1, balanced accuracy and
   ROC AUC side by side, none named as the criterion (MET-5)."

**Untested claims, ranked**

1. **The target is the real-world deaths count, and how long deaths are counted (P3, USE-5; rows 4, 29, 46).** No
   counting window is documented anywhere I looked (CKAN, the MOT 2565 PDF; the OTP 2020 analysis was blocked). The
   2024 revision changed deaths on 41 of 3,210 re-keyed 2022 crashes, so labels are revised in place, both up and
   down. *What would settle it:* the Department of Highways' TRAMS reporting manual or a question to motoc@mot.go.th.
   *For now:* keep "not stated", and add that deaths are revised in place (41 of 3,210 re-keyed crashes).
2. **The officer's cause and collision readings follow the outcome (P4, USE-3 and LEAK-10; row 8b).** The data can
   only show circumstantial evidence (records entered weeks after the crash). The measured cost of dropping both
   fields is 7% of the model's RMSE gain, so draft issue 1 is a framing choice rather than a leak to fix.
3. **The Kaggle upload has no notebooks (P6, MET-1; row 35).** The evidence is consistent with none but does not prove
   it. Two other public notebooks on the same register exist (a binary "is fatal" LightGBM with ROC AUC on a
   2019-2026 copy, October 2026). They are third-party (EV-2 rank 4) and do not change the metric.
4. **The actor of the use case (P3, USE-1; row 2).** Written as "for example". A question for the domain
   practitioner.

**Metric, in one judgment line**

MET-1 holds (looked again: no source metric; the one paper reports several metrics). MET-2 holds (per row, no
inputs, 9 of 9 folds score, 256-449 fatal crashes per fold). MET-3 holds (identity scale). MET-5 sends the paper's
metrics to the fallback. MET-11 needs one clause added to the reason. MET-10 factor: 15-29% of squared error per fold
comes from 6-16 crashes with 3 or more deaths, so RMSE leans on the multi-death crashes, the least predictable part.

</details>

<details><summary>Column audit</summary>

**Column audit (column-auditor, AI, 2026-11-01): thailand_road_accident_register_2019_2022**

```text
Verdict: ship after documentation changes. No column has to go; one call on the officer's fields goes to the curator.
Validity: LEAK-10 holds for the 26 features under the written prediction point ("the crash has been recorded"); the
  injuries, the report date and time and the accident code are dropped as they should be (checked). presumed_cause:
  maybe outcome-dependent ascertainment (the drunk-driving code), small, keep with a `Potential leak, kept on purpose:`
  note (USE-3, curator's call). Missingness in incomplete records: maybe (R^2 -0.003 when masked), keep with a note
  (LEAK-6). LEAK-13 holds: time, km and coordinate precision do not differ by outcome.
Quality: CLEAN-12 (site split) holds; CLEAN-10, CLEAN-11 hold (proxy 0 and out-of-range coordinates made missing);
  CLEAN-5 drops checked (bus and farm counts are 0 in every row, and those vehicles sit in n_other_vehicle in 100% of
  the rows where one is the first vehicle); CLEAN-14 holds. Two coding breaks inside the test period, kept with notes.
For the curator: issue 1 (keep or drop presumed_cause), issues 2-4 are notes to add.
```

**How I worked.** The cleaned frame came from the definition through `dataset_io.from_definition` (81,059 rows, 27 columns). The frame with `report_datetime` came from `ds.df`, and the raw yearly files were read through `_load_raw`. No codebook exists (the ministry publishes none, as the definition says), so meanings come from the Thai headers, the values and the data. The model numbers are untuned LightGBM (Poisson, 300 trees) on the 9 shipped windows, with the paired SE over windows. Agencies: DOH = Department of Highways (75,252 crashes), DRR = Department of Rural Roads (5,141), EXAT = Expressway Authority (666).

**Column table**

| column | meaning | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| `deaths` | people killed in the crash as recorded (ผู้เสียชีวิต); how long after the crash a death counts is unknown | target | int64, 0-13, none missing; 87.5% zeros | fine (target) | CLEAN-15 |
| `crash_datetime` | crash date and time | yes | datetime; per-file date order plus the 2022 repair; 0 rows reported before the crash after the repair, 0 missing; crash year equals file year in every row; 117 at 00:00 (0.14%), too few to treat as a proxy | fine | CLEAN-14, PROV-13 |
| `agency` | recording agency (DOH, DRR, EXAT) | yes | category, 3 levels, none missing | fine. It carries each agency's reporting threshold (issue 3) | LEAK-10 holds; note |
| `province` | province of the crash | yes | category, 77 levels, 19 missing; coordinates within 144 km of the province's median point for 99.9% of rows, none over 300 km | fine | CLEAN-14 |
| `route` | road or control-section name (Thai text) | yes | string, 3,885 values, 1,701 missing; 1,527 of the missing are crashes entered in December 2022 (DOH), which still have `route_code` | fine; the December 2022 blanks fall on test rows only (issue 4) | CLEAN-14 |
| `route_code` | road number: DOH highway number (`7`, `2300`), DRR province plus number (`ชม.3035`), EXAT section (`E002S014\|U`) | yes | string, 2,337 values; missing for all 19,194 crashes of 2019 (the column is not in that file) | fine | CLEAN-14 |
| `km` | kilometre post on the route | yes | float, 0-1,310 (DOH), 0-127 (DRR); no raw value failed to parse, no negatives; 447 missing (213 DOH, 53 DRR, 181 EXAT) | fine; its missingness is almost never fatal on DOH roads (issue 2) | CLEAN-11 |
| `latitude`, `longitude` | crash coordinates | yes | float; 4 pairs outside Thailand made missing, 211 missing in all (199 EXAT) | fine. Nit: the swapped pair (100, 13) could be swapped back instead of blanked (one row) | CLEAN-11 |
| `vehicle_1` | type of the first party (16 types, pedestrian included) | yes | category, 15 levels shipped, 550 missing (462 EXAT, 73 DRR, 15 DOH) | fine; the missing DRR and DOH rows are never fatal (issue 2). A pedestrian as first party is fatal 0.699 against 0.579 for the collision type "pedestrian hit" (219 rows): maybe a recording habit, too small to act on | CLEAN-14 |
| `vehicles` | vehicles involved, the first included | yes | float count, 0-27; 0 with no first vehicle (86) made missing, 20 pedestrian-first crashes keep 0; equals the sum of the type counts in every 2020-2022 row; distribution in 2019 matches the later years (57.8% one vehicle against 55.2-60.2%) | fine | CLEAN-10, CLEAN-14 |
| `n_motorcycle` ... `n_other_vehicle` (10 columns) | vehicles of each type involved | yes | float counts; missing for the 19,194 crashes of 2019 (not in the file); header alignment checked: every first-vehicle type has its own count at 1 or more in 100% of its rows; bus, bicycle, tricycle and farm vehicles count under `n_other_vehicle` (100%) | fine | CLEAN-14 |
| `n_pedestrian` | pedestrians involved | yes (a fact of the scene) | float count, missing in 2019 | fine | CLEAN-14 |
| `road_layout` | road layout at the site (straight, curve, junction types, accesses), from the site code | yes | category, 18 levels, 7,517 missing (no site code) | fine | CLEAN-12 |
| `road_slope` | slope (sloped or flat), the second part of the site code | yes | category, 2 levels, 10,905 missing: 7,517 without a site code and 3,388 whose layout carries no slope (junctions, accesses, a bare "straight"). Not applicable and not recorded share one missing value; `road_layout` tells them apart | fine | CLEAN-12 |
| `weather` | weather at the crash | yes | category, 7 levels, 63 missing (2022). "Overcast" (368) and "other" (95) occur only in DRR rows, so their fatal shares (0.44, 0.45) are the DRR's | fine | CLEAN-14 |
| `collision_type` | kind of collision (rollover, rear-end, head-on, pedestrian hit) | yes (seen at the scene), entered with the report | category, 11 levels, 3,751 missing. 3,425 of the missing are DRR crashes of 2020-2022: the DRR stopped recording it (1,594 of 1,594 recorded in 2019, 25-66 a year after). Missing means DRR, fatal share 0.23-0.32 | keep; document what the missing value means (issue 3) | LEAK-10 holds; note |
| `presumed_cause` | the cause the reporting officer presumed (มูลเหตุสันนิษฐาน) | yes under the written point; no at a first-call point; entered with the report, when the deaths are known | category, 53 levels, 685 missing (666 = every EXAT crash). Codes change for records entered from November 2022 (issue 4) | question for the curator: keep with a `Potential leak, kept on purpose:` note (issue 1) | LEAK-10, USE-3, LEAK-6 |
| `report_datetime` (split only) | when the record was entered | no: a median 27 days after a fatal crash and 57 days after a non-fatal one | used in `_make_splits` for the as-of filter, then dropped; 4 rows NaT stay out of training | fine | LEAK-10, SPLIT-9 |
| dropped: `acc_code`, `file_year`, `route_class`, `vehicles_and_pedestrians`, `n_bus`, `n_farm_vehicle`, `injuries`, `serious_injuries`, `minor_injuries`, raw date and time text, `site` | identifier; crash year; agency copy; sum; all-zero counts; the crash's other outcomes; replaced by parsed or split columns | n/a | every raw column of the four files is either renamed and kept or in this list | fine | CLEAN-3, CLEAN-5, LEAK-10 |

**Problems, ranked (principles.md: P4 before P7, then strength, then effect size)**

1. **P4, LEAK-10 / USE-3, Should-level call: `presumed_cause` (and, weaker, `collision_type`) are entered by the officer with the outcome known.** Under the written prediction point they are known, and they carry little of the signal: R^2 0.171 to 0.166 and AUC 0.840 to 0.838 without the cause, 0.162 and 0.833 without both. I checked these numbers against the builder's hurdle probe. New, circumstantial evidence that the cause code partly follows the outcome comes from the drunk-driving code on DOH roads. Outside the New Year and Songkran campaign days (27 Dec-4 Jan, 10-18 Apr), crashes coded drunk are fatal in 0.210 of cases against 0.113 for the rest (314 crashes). On the campaign days, when alcohol testing is broad, the figures are 0.116 against 0.118 (458 crashes). That pattern fits testing that is triggered by a death. Also, "vehicle equipment defect" goes to fatal crashes less often in every reporting-delay band (fatal share 0.044-0.070 against 0.087-0.166), which is either signal or blame moving to the driver once someone has died. Neither can be proven from the file ("maybe a leak"). The collision type is a fact of the scene (pedestrian hit 0.579 fatal, head-on 0.332), so it is the weaker suspect. Mildest remedy: keep both, and turn the "Note:" bullet into a `Potential leak, kept on purpose:` note in LEAK-38's format (mechanism, the two numbers above, why they stay: crash-severity models of the field use collision type and contributing factors, and the gain is small; revisit if a first-call framing is wanted). Reword `fit_reason` so it names the fields as kept, not as a gap (USE-8: a kept potential leak does not make the fit approximate; the fit stays approximate for the unnamed user and the unstated death window). Alternative: drop `presumed_cause` only (R^2 -0.005, AUC -0.002). That is the builder's draft issue 1.

2. **P4, LEAK-10 ("missingness that encodes the outcome") with LEAK-6, weak: gaps in incomplete records are almost never fatal.** DRR crashes with no first vehicle: 73, none fatal (DRR base 0.30). DOH crashes with no km: 213, 4 fatal (0.019 against 0.114). DOH crashes with no first vehicle: 15, none fatal. Masking these gaps (mode or median fill on DOH and DRR rows) costs R^2 0.0028 (paired SE 0.0009) and AUC 0.0007 (SE 0.0002) over the 9 windows (my masking run). The mechanism is open: a crash with no identified vehicle may really be harmless (the vehicle left and the damage was found later), or fatal crashes may simply get complete records. Mildest remedy: keep, and add one sentence to the "Missing values" bullet with these numbers. No row or column change.

3. **P4 / P3, weighed, a documentation gap: `agency` and the missing `collision_type` carry the agencies' reporting thresholds.** DRR records are mostly casualty crashes: property-damage-only crashes are 10-12% of DRR records against 43-48% for the DOH and 65-76% for EXAT. DRR fatal share is 0.28-0.32 against 0.10-0.12, and the DRR reports in a median 1-10 days against 52-62. The ~1,200 crashes a year with no collision type from 2020 are the DRR's, so that missing value means "DRR" (fatal share 0.23-0.32). Under the use case, a model is not leaking when it learns this: the agency is known and a road agency ranks its own network. But the zero means "recorded without a death under that agency's threshold", and the notes do not say so. Masking the missing collision type: R^2 -0.0031 (SE 0.0016), AUC -0.0001; dropping `agency`: R^2 -0.0007 (SE 0.0020). Mildest remedy: in the "Missing values" bullet, say the missing collision types are the DRR (3,425 of 3,547 of its 2020-2022 crashes) and that DRR records are mostly casualty crashes. Every EXAT crash also lacks `presumed_cause` (666 of 685 missing).

4. **P7, CLEAN-21 (one coding per column), keep with a note: two coding breaks tied to the entry date, both inside the test period.** (a) Records entered from November 2022 use finer cause codes: tyre, brakes, slippery road, loss of control and reckless crossing replace "vehicle equipment defect" and "other". 591 crashes of 2022 carry them, 577 of them reported in November 2022 or later, with a fatal share of 0.052 against 0.099 for other late reports. (b) 1,527 crashes entered in December 2022 have no route name, though they keep `route_code`. Every window trains only on crashes reported before it starts (November 2022 at the latest), so neither break reaches a training set and neither gives a shortcut. Only the newest window has rows with a cause code unseen in training (64 of 3,537 test rows). The source publishes no crosswalk, and one of our own would be invention. Mildest remedy: one sentence each in `curation_comments`.

5. **P7 nits.** The swapped coordinate pair (100, 13) could be swapped back rather than blanked (one row, CLEAN-11 / PROV-13). `road_slope` mixes "not applicable" and "not recorded" in one missing value; `road_layout` separates them, so no change is needed.

**Claims checked against the data (all hold):** 70,154 crashes with a slope; 211 missing coordinate pairs; 86 vehicle counts made missing and 20 zeros kept; 19,194 crashes of 2019 without type counts, pedestrians or route code; collision type missing for 50 in 2019 and 1,198 / 1,186 / 1,317 later; `vehicles_and_pedestrians` = vehicles + pedestrians and `route_class` = agency in every row; bus and farm counts all 0; target counts 70,958 / 8,794 / 1,307; the officer-field and hurdle numbers in `curation_comments`; two duplicate crashes (81,061 to 81,059).

</details>

<details><summary>Split audit</summary>

**Split auditor (AI, 2026-11-01): thailand_road_accident_register_2019_2022**

**Verdict: right with notes.** The regime is temporal by crash date, with known roads (SPLIT-3, SPLIT-13, USE-10). The windows meet SPLIT-11, SPLIT-14, SPLIT-15 and SPLIT-17. The reporting filter keeps every training row whose deaths were on record at the refit (SPLIT-9), and the two-month gap follows SPLIT-10 as brazilian_ecommerce, house_sales and zillow_prize applied it. Nothing has to change before shipping. The notes are about wording: the gap leaves some selection in place, the cadence is our own choice, and the comment does not explain the training history.

All numbers come from the definition's own frame and splits, rebuilt from the raw files through `dataset_io.from_definition` (81,059 rows, 9 splits), unless a line names another source. The models are untuned LightGBM (Poisson, 300 trees), so the numbers are probe numbers, not leaderboard numbers (EV-8).

**What holds (checked)**

- Regime (SPLIT-1, SPLIT-3, USE-10): pass. The register is a stream of dated crashes, and the use case is an agency scoring new crashes on its own network. Provinces recur for 100% of test rows and routes for 92.7% (76.6-98.5% by window; the builder's hidden-group probe). For a road agency these are known entities, so they are part of the task (SPLIT-13), not hidden groups. Test rows with a near copy in training (30.9% at 0.85) are the natural repeats of known roads (evidence.md, probe 6, reading 3). A random 3x3 split gives the same skill as the shipped windows (0.174 against 0.175; RMSE 0.394 against 0.365 on test sets with different death rates). So the temporal regime costs no skill, and it rests on the use case (SPLIT-4).
- Time column: pass. `crash_datetime` is the crash date and time: no value is missing, the frame is sorted, and no crash is reported before it happens. Two checks of the date parsing, independent of the builder's (EV-6):
  - Report dates agree with the Kaggle copy of 2023 on 100% of matched crashes for 2020 and 2021, and on 99.98% for 2022. The 3 disagreements are crashes with no report date. Ambiguous day/month report dates agree too.
  - Daily counts peak on the holidays in every year. In 2022: 1 January 310, 2 January 225 and 3 January 221 crashes, against a median of 50 a day; 13 April 233. Under the month/day reading, 2 and 3 January would fall on 1 February and 1 March. So the 2022 repair puts crashes in the right windows.
- Windows (SPLIT-11, SPLIT-14, SPLIT-15, SPLIT-17): pass. Nine calendar windows of two months, newest first, from November-December 2022 back to July-August 2021. Each window holds 2,492-3,978 test crashes, about 250-450 of them fatal. Training sides hold 47,333-69,688 crashes, 58.4%-86.0% of the rows. Nine windows is what `recommended_dimensions` gives for 81k rows (3x3). No test row falls outside its window, and every crash of a window is in its test set.
- Gap: pass. In every split the newest training crash is two months before the window (for example, training ends 2022-08-31 for the November window).
- Reporting filter (SPLIT-9): pass. No training row has a report date on or after its window's start (0 in all 9 splits).
  - Delays match the comment. The median is 53.3 days: 27.0 for fatal crashes and 56.8 for the others. 10.1% are reported after 240 days and 2.8% after a year.
  - The comment's 941 to 4,790 left-out crashes per window are reproduced exactly.
- Unused rows: pass. The 177 rows in no split are crashes from 16 January 2020 to 29 May 2021, reported between 9 December 2022 and 23 June 2023. They were reported after the newest window starts, so no window trains on them, and they happened before the oldest test window, so none tests on them. Accepting `splits_rows_unused` is right. Four crashes of 2022 have no report date. They stay in their test windows and never train a later window, which costs nothing.

**Notes, ranked (all P4; Should, then Weigh)**

1. **The gap is the median delay, and some selection by outcome stays in the newest training months (SPLIT-10, Should; the gap's length is a weighing call).**
   - Evidence: in each window, crashes 2-4 months before the start are 48%-96% reported. Among the reported ones the fatal share is 0.113-0.146, against 0.100-0.124 among all of them. The worst case is the July 2022 window: 48% reported, fatal share 0.146 against 0.113.
   - The delay is long-tailed: the 75th percentile is 97-140 days by year and the 90th 167-277 days.
   - The selection does not bias the predictions measurably. The mean prediction over the mean truth is 0.96 on the shipped splits (0.79-1.32 by window), and 1.03 without the time features. A four-month gap gives no better fit in the builder's run (RMSE 0.3646 against 0.3630). Its oldest window would still train on 53.8% of the rows.
   - How it differs from sf_permit_time, whose longer gap was set because a short one censored the label: here a reported crash carries its final count (as far as can be checked, note 5). The residual selection is the one a real refit faces.
   - Remedy, the mildest: keep the gap, and add a sentence to `splits_comment`: "the gap is about the median delay; crashes two to four months old are still partly reported and more often fatal, as at a real refit". Choosing four months instead is a call for the curator, made from the delay and not from the scores (SPLIT-21).
2. **The two-month cadence is ours, and the comment does not say why (SPLIT-12, Should).**
   - Evidence: no source states a horizon. The stated use case, ranking sections for safety works, would refit on a programme cycle that the data cannot serve. Yearly windows would train the 2020 window on 2019 alone (at most 24%, below SPLIT-14's floor).
   - Counted alternatives with the same filter:
     - Quarterly windows with a two-month gap: 7 windows keep the 50% floor, fewer than the 9 recommended.
     - Monthly windows: 9 windows that cover only April-December 2022 and miss January-March.
     - The two-month windows are the shortest that fill 9 windows and cover every season once (18 months: Songkran in March-April 2022, New Year in three windows).
   - Remedy: one sentence in `splits_comment` saying the cadence is ours and giving this count-based reason. No re-split.
3. **The training history is not discussed (SPLIT-20, Should).**
   - Evidence, the breaks in the history:
     - 2019 has no vehicle counts by type and no route code.
     - April 2020 has 1,423 crashes against 2,662 in April 2019 (the COVID-19 period, with no Songkran peak).
     - Deaths per crash fall from 0.168 (2019) to 0.155, 0.135 and 0.127 (2022). The fall is inside the Department of Highways (0.154 to 0.119), while rural roads stay at 0.32-0.35.
   - Training sides average 0.151-0.161 deaths per crash, against 0.118-0.145 in the test windows. The constant from the newest training rows adds only +0.005 skill (the builder's task probe), so the level shift costs little.
   - The two oldest test windows (July-October 2021) fall in a low-traffic stretch: 1,233-1,268 crashes a month in July-September 2021, against 1,454-1,640 in the same months of 2022. Seven of the 9 windows are outside it, as in the perth_house_prices precedent.
   - The newest window (November-December 2022) holds the New Year run-up and the highest death rate of the 9 (0.145).
   - Remedy: a sentence saying the full expanding history is kept (SPLIT-11) and naming these breaks. Do not choose the history from a comparison over the windows (SPLIT-21).
4. **The prediction point says "recorded", but the time index is the crash (SPLIT-1, holds; I measured the alternative because I doubted the choice).**
   - The literal alternative indexes by report date: refit at T on every crash reported before T, test on the crashes reported in the next two months, with no gap needed. It scores higher: skill 0.215 against 0.175, and 0.207 against 0.169 without the time features.
   - But its test sets are another population: 41%-81% of each report-date window are crashes from before the window. Its test rows would also come before some training rows in event time.
   - The crash-date index is the clearer and more conservative choice, so keep it. Whether "recorded" is the right prediction point, given the presumed cause and collision type are written when the outcome is known, is the use-case question (builder's issue 1) for the other roles. Under that question the crash-date index fits an earlier prediction point even better.
5. **Cannot verify: are deaths revised after the report (SPLIT-9)?**
   - If a death that came days later was added to a crash already reported, a training row reported before T would carry a count not yet known at T.
   - The 2023 and 2026 copies agree on deaths in every matched row (builder), and on the report date in every matched row (above). So the report date is not a last-edit stamp moved by the 2024 revision.
   - Edits between the report and August 2023 cannot be seen, and the window in which a death counts is not stated. This is for the curator, alongside the `predicted` field's existing note.
6. **Where the RMSE triple comes from (EV-8, writing).**
   - The `splits_comment` RMSEs (0.3613 / 0.3619 / 0.3630) come from the builder's gap experiment. That script ran on a pre-definition frame (the builder's harmonised table, with the old `site` and `accident_type` columns), whose training sides differ from the shipped ones by about one row per window.
   - The qualitative claim holds. On the shipped frame and splits my run gives RMSE 0.365, skill 0.175 and ROC AUC 0.841 for any death.
   - Remedy: name the frame, or rerun on the shipped one.

**Claims checked against the data**

- `task_summary.split`: pass.
- `splits_comment`: pass on the delays, the left-out counts, the window range, the sizes and the train shares. The RMSE triple is from another frame (note 6).
- Decision 1's table: pass (rebuilt).
- `splits_rows_unused` as proposed for acceptance: pass.
- The builder's claim "Hidden groups none (routes recur, SPLIT-13)": pass. It is part of the task, not a hidden group.

**Alternative splits run**

| design | windows | training rows (mean) | test rows (mean) | RMSE | skill | ROC AUC any death | mean prediction / truth |
|---|---|---|---|---|---|---|---|
| shipped: crash date, reporting filter, 2-month gap | 9 | 58,516 | 3,269 | 0.3654 | 0.175 | 0.841 | 0.96 |
| report date, no gap (prediction at the recording) | 9 | 59,656 | 2,913 | 0.3439 | 0.215 | 0.854 | 0.99 |
| random 3x3 | 9 | 54,039 | 27,020 | 0.3944 | 0.174 | 0.839 | 0.96 |

</details>

<details><summary>Domain practitioner</summary>

**Domain practitioner: thailand_road_accident_register_2019_2022**

Actor: a road-safety engineer at the Department of Highways (DOH) or the Department of Rural Roads (DRR) who ranks road sections and crash types for safety works.

**Verdict.** Fit: **approximate**, as declared, but for a different reason than `fit_reason` gives. One row is a crash whose deaths are entered in the same record as its features. My decision is made per road section and per year, after the deaths are known. The model stands in for the severity part of network screening (the expected deaths of a crash given its type and place, as the HSM relative severity index assigns a cost to each crash by its type). That is a real practice, so the fit is not none (USE-2). It is not direct, because I never need to predict the deaths of a crash that is already recorded (USE-8; USE-9 does not apply, since the label is known when I would use the model). Metric: **partly**. RMSE scores the right quantity (the mean deaths per crash, which I would sum per section), and on six models it ranks them as a section-level ranking does. But 0.3% of the test crashes (those with 3+ deaths) hold 25% of the squared error, and the good models differ by less than their paired SE. I would use the Poisson deviance with a floor on the predictions (MET-1, MET-11 context), which the metric library does not have yet.

**How the decision is made today (sources below)**

- TRAMS is the ministry's accident reporting system ("ระบบรายงานข้อมูลอุบัติเหตุของกระทรวงคมนาคม (TRAMS)"), run by the Transport Safety Operations Centre. It feeds next-morning festival dashboards: the New Year 2565 summary covers 29 Dec - 4 Jan and was "processed 5 January 2022, 10:00". The same report gives "speeding" as the presumed cause of 65.07% of crashes.
- DRR black spots: Treeranurat & Suanmali (2021) rank sections by an Equivalent Accident Number. It weights fatal, serious, minor and damage-only crashes and uses three years of DRR investigation records. DOH uses a frequency criterion; per the 2009 IRTAD paper this is at least three crashes in a year at a location, but I saw only a search snippet because the PDF returned 403.
- HSM network screening, chapter 4, the relative severity index: "Monetary crash costs are assigned to each crash type and the total cost of all crashes is calculated for each site. An average crash cost per site is then compared to an overall average crash cost for the site's reference population." A per-crash model of expected deaths given collision type, vehicles, place and time is a learned, many-input version of this index. The HSM also notes that this measure does not account for regression to the mean or traffic volume.
- Per-crash death counts are an established Thai research model. Simmachan et al. (2022) model DDPM's 2015 crashes with Poisson, CMP and zero-inflated count models, compare them by log-likelihood and AIC (no held-out score), and note that Thai fatality figures "are particularly vulnerable to underreporting". Se et al. (2021) use DOH-style severity models with a binary outcome (no/minor against severe/fatal).

**1. Inputs at the moment of the prediction**

When I rank sections, I have every shipped feature: time, agency, province, route, km, coordinates, road layout and slope, weather, first vehicle, vehicles by type, pedestrians, collision type and presumed cause. All of them are entered with the crash. Dropping the report date and the injury counts is right (LEAK-10): the report delay follows the outcome, and injuries are the crash's other outcomes.

- **Collision type and presumed cause are inputs for me, not a gap.** The relative severity index is built on the crash type, and DRR's black-spot work names collision type and speeding. Under USE-8 a kept potential leak is named as kept, not counted as a gap. The builder measured what keeping them adds: R^2 0.171 against 0.162 without both, and ROC AUC 0.840 against 0.833. They are a gap only for a first-call dispatcher, who would not have the presumed cause. The task does not claim that use case.
- **Inputs I would always have that are missing:**
  - traffic volume (AADT) and the road inventory (lanes, median, speed limit, lighting, shoulder) from the DOH/DRR asset databases, which could be joined by route and km;
  - per-type vehicle counts, the pedestrian count and the route code for 2019 (missing for its 19,194 crashes, 23.7% of the rows).
  
  These limit the ceiling but are not a defect of this source.
- **The presumed cause is mostly a default code.** "Speeding" is the presumed cause of 75.2% of the non-fatal and 69.3% of the fatal crashes, my count on the shipped frame. I would keep it as recorded (USE-6) but would not choose countermeasures by it.

**2. Target**

Deaths is the ministry's headline indicator, and per-crash deaths add up to a section's deaths, so the target matches what I sum (USE-5). Two reservations:

- **The counting window is unknown.** TRAMS serves next-morning counts, so its deaths are probably those the road agency knows when it reports. That is likely fewer than the deaths the national three-database integration counts (health, police and insurance; Simmachan et al. 2022). The undercount probably differs by road user: a motorcyclist who dies days later in hospital may be missed more often than a car occupant killed at the scene. That shifts the severity model, not only its level. This is a real label gap (USE-5, USE-8), and `fit_reason` names it correctly.
- **For ranking I would rather use a severity-weighted target.** DRR's Equivalent Accident Number and the international KSI/FSI convention weight deaths and serious injuries together because deaths alone are rare and noisy. The serious-injury count ships in the raw files from 2020. Deaths is still a defensible single target for this collection, so this is no blocker.

**3. Row and test data**

- **One row is not one decision.** I decide per section (about a kilometre of a route) per year, from tens of crashes. The model provides the severity component. Crash frequency and exposure, the other half of screening, are not in the data. This is the largest gap, and `fit_reason` does not name it.
- **The test data are what I would face.** They are later crashes on my own network: the route is seen in training for 92.7% of the test rows (probe). Training only on the crashes reported before a window starts mirrors what I would have at a refit.
- **The cadence is not mine.** I rank on the fiscal-year budget cycle, not every two months. The builder measured that the cadence and the gap change little (RMSE 0.3613, 0.3619 and 0.3630). It is a benchmark device and does not change the task (SPLIT-12 belongs to the split auditor).

**4. Would I use this model?**

As a severity screen, yes: summed per section, it would flag sections whose crashes are deadlier than their crash mix predicts (ROC AUC 0.84 for any death). It is not a replacement for frequency-based black-spot lists.

What would make me trust it:

- calibration by agency and vehicle type;
- stable results across years (Se et al. report that severity factors are unstable over time in Thai data).

What makes me distrust it:

- the unknown death window;
- the default "speeding" cause;
- **collision type is blank much more often for fatal crashes.** It is missing for 13.6%, 15.1% and 13.2% of the fatal crashes in 2020, 2021 and 2022, against 4.4%, 4.7% and 5.6% of the non-fatal ones, mostly for motorcycles (my count). A model learns "blank means fatal", which holds only as long as the form is filled in the same way. Whether the field is blank because of the outcome (USE-3) is untested. I pass it to the column auditor.

**5. Does the metric score my decision? Partly.**

I ran six models on the nine windows: train mean, the first vehicle's means, LightGBM with L2 loss (400 and 50 trees), LightGBM Poisson, and a hurdle model.

| | LightGBM Poisson | hurdle | LightGBM L2 | L2, 50 trees | vehicle_1 means | dummy |
|---|---|---|---|---|---|---|
| RMSE | 0.3632 | 0.3642 | 0.3647 | 0.3648 | 0.3878 | 0.4022 |
| Poisson deviance (floor 1e-6) | 0.414 | 0.421 | 0.489 | 0.429 | 0.520 | 0.586 |
| ROC AUC, any death | 0.844 | 0.840 | 0.835 | 0.836 | 0.694 | 0.500 |
| share of squared error from 3+ death crashes | 25.3% | 25.2% | 24.8% | 25.3% | 23.9% | 22.4% |
| Spearman, predicted vs observed deaths per 1-km section | 0.381 | 0.377 | 0.374 | 0.369 | 0.220 | 0.010 |

- **The quantity is right.** Squared error is strictly consistent for the mean, and the mean deaths per crash is what I add up per section. Over these six models RMSE orders them the same as the section-level Spearman (Kendall tau 1.0) and close to the Poisson deviance (0.867).
- **The resolution is weak among good models.** Crashes with 3+ deaths (0.3% of the test rows; 283 in the whole frame, led by pickups, cars, motorcycles, heavy trucks and vans) carry 14-34% of each window's squared error. Paired RMSE differences between the top models are 0.0010-0.0015, with SE 0.0013-0.0020. RMSE and Poisson deviance pick the same best model in 5 of 9 windows.
- **The metric I would choose is the Poisson deviance.** It is the count-model likelihood that Thai severity studies and HSM safety performance functions select by (Simmachan et al. compare by log-likelihood and AIC). It also elicits the mean, and it does not let a few bus or van crashes dominate. It needs a declared floor for the predictions: the L2 model's zero-clipped predictions score 0.489 against 0.429 for the same model with fewer trees, so the floor changes the ranking. That needs a library metric (MET-13) and an origin of `context` (MET-11).
- **No threshold or top-k metric.** The source fixes no k (the size of a black-spot list is set by the budget) and no costs, so no threshold or top-k metric is declared (MET-6, MET-7). ROC AUC on any death would score where the signal is, but it changes the problem type (MET-8, MET-9 do not call for it here).
- **The unit gap stays.** A section-level score would need section keys as scoring columns (MET-2). With two-month windows most sections hold one or two crashes, so it adds little over the per-crash score.

**Gaps, ranked by how much they change the task**

1. A row is a crash recorded together with its deaths, while the decision is per section and year. The model covers severity only, without frequency or exposure (USE-1, USE-5, USE-8; the nearest rule against the task is SEL-7, "a label already known with the features is predicted by nobody". It does not bind, because the expected value given the crash mix is what screening uses, but this is why the fit is not direct).
2. The death-counting window is unstated and probably shorter than the national count, with an undercount that likely differs by road user (USE-5, USE-8).
3. Missing exposure and road inventory, and 2019 lacks the per-type counts (ceiling, not validity).
4. Collision type is blank more often for fatal crashes (13-15% against 4-6%); whether the outcome causes the blank is untested (USE-3).
5. The two-month refit cadence is not the yearly budget cycle (small; measured to change little).

**What an expert would change**

- Rewrite `fit_reason`, keeping approximate. Name the unit and moment gap: a crash whose deaths are recorded with it stands in for the severity part of section screening, without frequency or exposure. Name the unstated death window. Name collision type and presumed cause as kept, with their measured cost, rather than as a gap (USE-8 amendment of 2026-10-21). Drop "the source names no user": the "for example" use case answers that (USE-1 Methods).
- Optionally sharpen the `use_case` sentence: the expected deaths of each crash, summed per road section, ranks the sections whose crashes are deadlier than their mix predicts. "Enforcement" belongs to the highway police, not to DOH or DRR engineers.
- Add a curation note on the collision-type blanks by outcome (numbers above).
- Metric: keep `rmse` as the fallback for now (MET-8, MET-11). Add to the reason that 0.3% of the crashes hold a quarter of the squared error. Propose `mean_poisson_deviance` with a fixed floor as the `context` metric once the library has it (MET-11, MET-13).
- Later, not now: the 2024-2025 files (the older coding scheme) would allow yearly windows like the budget cycle (PROV-9); a deaths-plus-serious-injuries variant is the practitioner's ranking target.

**Sources**

- Ministry of Transport, TRAMS New Year 2565 summary: https://datagov.mot.go.th/dataset/1e476099-be5e-4625-8523-d43b4936a1b3/resource/e9336e7b-74e5-455f-bcd1-6650fbf54f93/download/-2565.pdf (read: TRAMS, processing time, speeding 65.07%)
- AASHTO Highway Safety Manual, 1st ed., ch. 4 Network Screening (NHDOT copy): https://ftp.granit.unh.edu/submissions/NHDOTOUT/craig/HSM/Chapter%204_NetworkScreening.pdf (RSI definition, lines 291-298 and 892-898 of the text)
- Treeranurat & Suanmali (2021), black spots by Equivalent Accident Number on DRR roads, EMJ 13(4): https://ideas.repec.org/a/vrs/ecoman/v13y2021i4p57-71n7.html
- Simmachan et al. (2022), PLOS ONE 17(11):e0269022: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0269022
- Chayanan, DOH Bureau of Highway Safety, IRTAD 2009: https://www.itf-oecd.org/sites/default/files/docs/6-chayanan.pdf (403; search snippet only)
- FHWA, Screening Your Network: https://highways.dot.gov/sites/fhwa.dot.gov/files/2022-06/fhwasa17008.pdf (search result only)
- Se et al. (2021), temporal stability of severity factors in Thai single-vehicle crashes (search result only)
- Repository: `dataset.py`, README, record, builder report and the builder's probes (hurdle, hidden groups, task)

</details>

<details><summary>Blind review</summary>

**Verdict: include with minor changes.** This is a real crash register from Thailand's Ministry of Transport (TRAMS), and the target matches the source row by row. I found no leakage or copies, and the signal is real but not trivial. The changes I would make are about preparation and scoring: the schema break in 2019, a redundant free-text column, and a metric that suits counts. None of them is about honesty.

**What the task is**

Each row is one crash on the road network the Ministry of Transport manages. That network covers national highways (DOH), rural roads (DRR) and expressways (EXAT). The target is the number of deaths in that crash. In practice this is retrospective crash-severity modelling. Road agencies and road-safety researchers use it to find risk factors and rank black spots by expected deaths. It is not a forecast made before the outcome is known. Severity modelling on police and highway crash registers is a well-established real use.

**Concerns, most serious first**

1. **Schema break in 2019 (23.7% of rows).**
   - The 2019 source file `accident2019.csv` has 19 columns. The files for 2020 onward have 38.
   - So in 2019 (19,194 rows), all 11 `n_*` vehicle and pedestrian counts and `route_code` are 100% missing. From 2020 on they are 0% missing.
   - `road_layout` and `road_slope` for 2019 also come from a different combined field, "บริเวณที่เกิดเหตุ/ลักษณะทาง".
   - Under the temporal split, 2019 is always training data. Every model therefore trains on a block where 12 columns are missing by design and is tested on rows where they never are. This is not dishonest, but it is an avoidable artefact.
   - The same source now publishes 2023, 2024 and 2025 with the identical 38-column schema; I checked the headers. 2023 alone has 23,841 rows.
   - Change: rebuild on 2020 to 2025 (or 2020 to 2024). That gives about 130k rows with one schema and more recent test windows. If you keep 2019, record the gap in the task card.

2. **The target is a zero-inflated count, so RMSE is not a good fit.**
   - `deaths` is 0 in 87.5% of rows. 12.5% of crashes are fatal, and the maximum is 13.
   - Crashes with 2 or more deaths are 1.4% of rows but carry 48% of the total sum of squares around the mean. Crashes with 3 or more are 0.35% of rows and carry 25%.
   - In nine expanding windows of about 4,050 rows each, the 5 largest rows make up 9% to 21% of each window's squared error.
   - Deaths per crash also depend on how many people were in the vehicles, which is not recorded. That matters for buses and pickups carrying passengers.
   - The choice of metric changes which model wins. On nine temporal windows, LightGBM with L2 loss had the lower RMSE (0.360 against 0.362 for Poisson loss). Poisson loss had the lower Poisson deviance (0.417 against 0.470).
   - Change: score with Poisson deviance, either alone or next to RMSE. Alternatively, also offer the standard crash-severity version, a binary target `deaths > 0`, where the fatal-crash AUC is about 0.84.

3. **The outcome is known before the record is complete, and one feature is a judgement call.**
   - The source report dates show that records are entered a median of 48 to 59 days after the crash (10th to 90th percentile: 1 to 280 days).
   - `presumed_cause` is the officer's judgement. It is "ขับรถเร็วเกินอัตรากำหนด" (speeding) in 74.5% of rows, which looks like a default code.
   - None of this is leakage. The outcome columns were removed, as listed under "what checks out" below.
   - Still, the task card should say this is retrospective severity analysis, not prediction in real time.
   - Dropping `presumed_cause` hardly changes performance: on the 2022 holdout, the AUC goes from 0.8436 to 0.8420. A version without it would be easy to justify.

4. **The three agencies report differently, so the table is not a census.**
   - Share of crashes that were fatal, by year:
     - DRR (rural roads): 0.29 / 0.32 / 0.31 / 0.28.
     - DOH (highways): 0.12 / 0.12 / 0.11 / 0.10.
     - EXAT (expressways): 0.04 / 0.006 / 0.016 / 0.004, from only 666 rows over four years.
   - This suggests different thresholds for what gets recorded. DRR mostly records serious crashes, and EXAT barely records at all.
   - Missing values follow the agency, not the outcome:
     - From 2020 on, DRR leaves `collision_type` empty in 3,425 of 3,547 rows. Within DRR, the fatal share is 0.30 when it is missing and 0.35 when it is present.
     - EXAT leaves `vehicle_1` empty in 462 of 666 rows.
   - The register also covers only the Ministry's roads. It has about 2.6k to 3.3k deaths per year, against roughly 15k to 17k road deaths in Thailand nationally.
   - This is acceptable for a benchmark, but the task card should say so.

5. **Redundant, high-cardinality text columns.**
   - `route` is free Thai text stored as a string: 3,885 unique values and 1,701 missing. It largely repeats `route_code` (2,337 codes) together with latitude and longitude.
   - On the 2022 holdout, removing both `route` and `route_code` slightly improved the score: Poisson deviance went from 0.4189 to 0.4133, and AUC from 0.837 to 0.844. That points to overfitting of high-cardinality categories, not to useful information.
   - From 2020 on, `vehicles` equals the sum of the `n_*` counts in 99.9% of rows.
   - Change: drop `route`, or at least store it as a categorical column. Keep `route_code` as a categorical column.

6. **Minor quirks (no action needed).**
   - The source columns for bus and farm-vehicle counts are all zero in every year, and the preparation correctly dropped them. Yet `vehicle_1` names a large bus as the first vehicle 425 times, so buses are probably counted in `n_other_vehicle`.
   - 20 rows have `vehicles = 0`.
   - Crash times cluster on whole and half hours: 47% fall at :00 or :30.
   - 4 pairs of rows share the same time, latitude and longitude.

**What checks out**

- **Real data, right target.**
  - The table matches the current Ministry CSVs. Yearly death totals are identical: 3,223, 3,301, 2,715 and 2,619.
  - Joining on latitude, longitude and km matched 18k to 20k rows per year, and `deaths` agreed on 100% of them.
  - Row counts per year are 19,194, 21,238, 20,062 and 20,565. That is the source minus 21,052 blank rows in the 2019 file and 2 unparseable rows, one of which is an Excel serial number ("44178") in 2020.
  - The Kaggle mirror, a 2023 snapshot, reports 81,735 rows. The prepared table has 81,059. So the register is revised over time.
- **Dates parsed correctly, which was not trivial.**
  - The date format in the source differs by year: day/month in 2019, month/day in 2020 and 2021.
  - 2022 mixes the two: day/month when the day is 12 or less, month/day otherwise. Songkran settles it: "12/04/2022" has 201 rows and "04/12/2022" only 32.
  - The prepared `crash_datetime` agrees with the correct reading 100% of the time for 2019 to 2021.
  - In 2022 it shows the Songkran peak on 11 to 18 April (156 to 233 crashes a day, against about 45 normally). That is consistent with correct parsing of the mixed format; I did not run a row-level check under the mixed reading.
- **No leakage columns.**
  - The source outcome columns (serious, minor and total injuries), the report date and time, `ACC_CODE`, and the combined count of vehicles and persons were all removed.
  - There are no exact duplicate rows and no duplicate feature vectors.
- **Signal that is worth scoring.**
  - On the 2022 holdout, LightGBM with Poisson loss reached a Poisson deviance of 0.414, against 0.586 for a constant prediction (29% lower).
  - RMSE was 0.363 against 0.404, and the fatal-crash AUC was 0.84.
  - Over nine expanding windows, R² ranged from 0.09 to 0.25.
  - Six core features alone (first vehicle, collision type, agency and three counts) reach an AUC of 0.79.
  - The strongest effects are plausible: a pedestrian as the first vehicle is fatal 70% of the time, a motorcycle 31%, and a head-on collision 33%. The rate in the full table is 12.5%.
- **Plausible values and real drift.**
  - All coordinates fall inside Thailand, and only 2 rows lie more than 1.5 degrees from their province's median location.
  - The fatal share falls from 13.8% in 2019 to 10.9% in 2022, which is real temporal drift.
  - Holiday peaks (Songkran, New Year) appear in the data, and the fatal share during holidays (12.7%) is close to the rest of the year (12.4%).

**What I could not check**

- Whether "deaths" means deaths at the scene or within 30 days. The Ministry's open-data page has no data dictionary, and I found no TRAMS documentation.
- Whether a record's death count is updated after it is first entered. The register is revised (the 2019 file was modified on 2026-05-26), but I cannot see the history of individual records.
- Whether officers fill in `presumed_cause` or `collision_type` after learning the outcome.
- The exact boundaries of the 9 test windows. I used my own nine equal-size expanding windows over the last 45% of rows, plus a 2022 holdout.
- The Kaggle web page itself; I read its metadata through the public Kaggle API instead.
- I worked only from the clean-room folder, the Ministry's CKAN API and CSVs, and the Kaggle metadata. I opened no other local files.

Sources: https://datagov.mot.go.th/dataset/roadaccident (CKAN `package_show`, and the CSVs `accident2019.csv` to `accident2023.csv`, plus the headers for 2024 and 2025); https://www.kaggle.com/datasets/thaweewatboy/thailand-road-accident-2019-2022 (Kaggle API metadata); https://www.nationthailand.com/thailand/general/40023780 (national total of 14,737 road deaths in 2022).

</details>

<details><summary>Precedent check</summary>

**Precedent check (precedent-checker, AI, 2026-11-01): thailand_road_accident_register_2019_2022**

```text
Verdict: consistent with its precedents on 18 of 23 decisions. Three depart without a written fact that sets them
  apart and need the curator (prompts 1-3); two are small (prompt 4, wording; prompt 5, a tag).
Validity: USE-1/USE-3 the written prediction point ("a crash has been recorded") is the moment the register holds the
  deaths, the fact glioma_grading was retired on (Lennart, 2026-10-26); the definition implies but does not name what
  sets this task apart (prompt 1). LEAK-10/LEAK-6 presumed_cause and collision_type kept: the precedents split
  (distribution_transformers dropped, Lennart, 2026-10-21; house_sales and onlinenewspopularity kept with a note); the
  stated reason leans on "little of the signal", which LEAK-10 bars as a sole reason, and the note is not in the
  kept-leak form (prompt 2). The drops of the injuries (fremtpl2, Andrej) and the report date (2_month_survival, kick,
  Lennart) are consistent. SPLIT-9/SPLIT-10 consistent (brazilian_ecommerce, house_sales); SPLIT-12 and SPLIT-20
  consistent, their reasons not written. PROV-8, PROV-9, PROV-13/14 consistent. 2024-2025 left out for a procedural
  reason only (prompt 3).
Value: MET-11 fallback rmse consistent (churn_telco_south_asia, blogfeedback, the 2015 sibling's screening); a
  Poisson deviance would be a decision for the whole family, not for this dataset.
Quality: CLEAN-3, CLEAN-5, CLEAN-10/11, CLEAN-12, LEAK-19 consistent; Thai labels kept as avito_demand_prediction_1m
  keeps Russian ones.
Drift: none in Andrej's calls. Third exception: none; the open SPLIT-10 amendment proposal is not touched.
For the curator: prompts 1-3; prompts 4 and 5 are small.
```

What the evidence is: the run's decision register (1,620 decisions; none of its 14 flags concerns a rule this definition departs from), the Cases tables of `use_case.md`, `leak_checks.md`, `splits.md`, `provenance.md`, `metrics.md` and `cleaning_features.md`, the records of the precedents named below, the sibling definitions of this run (noaa_storm_events_damage, blogfeedback, frempl_french_motor_personal_line, australian_vehicle_insurance_2004_2005, wadden_sea_sibes_macoma_abundance, pennsylvania_oak_hickory_regeneration_experiment, noaa_afsc_bottom_trawl_survey_cpue, crms_phragmites_cover), the builder's probes, and the phase A reports already in this panel folder (split, column, claim and domain). One small computation of my own: the oldest window's training share under wider gaps, and the zero share a Poisson and a negative binomial with the target's mean and variance give. Precedents that are AI drafts of this run, not yet decided by a curator, are marked "same run".

**Per decision**

| Decision (rule) | Standing | Closest precedents | What sets it apart, or not |
|---|---|---|---|
| `Yes`, priority 5, a crash register as a prediction task (SEL-2, USE-2) | consistent | us_accidents (`No`, Lennart, 2026-09-23: its Severity is a delay code; he opened nhtsa_crss_crash_severity, chicago_traffic_crashes and nyc_motor_vehicle_collisions as the injury-severity counterparts); thailand_road_accident_fatalities_2015 (2nd Tier, Andrej, 2026-10-30: "better data for the same task already") | Deaths are an injury outcome, not a delay code; the same curator's two calls of 2026-10-30 point the same way. |
| Use case and prediction point: a road agency ranks with expected deaths of each recorded crash; the prediction point is the recorded crash (USE-1, USE-3, USE-8) | departs without a written fact | glioma_grading_clinical_and_mutation_features (`No`, Lennart, 2026-10-26, Cases row of `use_case.md`: "a model can only cross-check a label that already exists"); noaa_storm_events_damage (same run: the prediction point is the first report, "before any damage survey, claim or damage estimate", and every field written from or with the outcome is dropped) | At the written prediction point the record already holds the deaths (the domain practitioner: "I never need to predict the deaths of a crash that is already recorded"). What makes the task real is that the agency acts on expected deaths per crash type and section, which no record holds; `use_case` implies this, but nothing names it as the fact that sets the task apart from glioma. The fit stays approximate either way. Prompt 1. |
| Source: the ministry's yearly CSVs, not the Kaggle copy (PROV-8, PROV-15) | consistent | PROV-8 (Lennart, 2026-10-12: Kaggle is the source only when the data first appeared there); airfoil_self_noise (Lennart, 2026-10-20: NASA RP-1218, not UCI's copy); SUPPORT2 restored from the study data | The Kaggle copy serves only as a check on dates and labels, which PROV-15 allows (provenance). |
| `year = "2026"`, the snapshot (PROV-9) | consistent | PROV-9 ("a source that grows over time (a public register ...) takes the year of the snapshot we pin"); sf_permit_time and crms_phragmites_cover (2026) | The register grows yearly and its files are revised in place. |
| Years: 2026 left out, 2023 left out rather than crosswalked (LEAK-24; PROV-13, CLEAN-21) | consistent | sf_permit_time (LEAK-24: cut where follow-up is complete); the Tensions row "a better version against our own fix" (eryhemato: "a fix of our own invention does not" replace the data); force_2020 (CLEAN-21, Lennart, 2026-10-21: values without a checked conversion "are masked, not converted") | 2026 is still being reported. The ministry publishes no crosswalk for the 2023 coding, and 1,641 crashes of 2023 are entered twice. |
| Years: 2024 and 2025 left out (SPLIT-11, SPLIT-20) | departs; the reason is procedural ("the years the record names") | noaa_storm_events_damage (same run: tests on 2023-2025 and starts its history after the 2006 format change); crms_phragmites_cover (same run: tests 2017-2025); SPLIT-11 ("the first split is the newest window ... the most representative") | By the definition's own notes, 2024 and 2025 use the older scheme: about 47,700 more crashes (the builder's harmonised frame). No precedent restricts a growing register to its older years for the record's name alone. A data reason is evident (a year-long hole), but it is not written. Prompt 3. |
| 2022 date repair (PROV-13, PROV-14) | consistent | SUPPORT2, ashrae (repair from the origin); force_2020 (CLEAN-21, Lennart, 2026-10-21: a conversion inferred from the data, checked against a second curve); PROV-14 (a repair stays under its record) | The repair is inferred from the file and checked two ways: no crash reported before it happens, and agreement with the Kaggle copy on 16,433 of 16,433 dates. The split auditor adds the holiday peaks. |
| Empty rows and 2 duplicate crashes dropped (LEAK-19) | consistent | wine_quality, audiology_diagnosis (exact copies dropped); noaa_storm_events_damage (same run: keeps 0.6% duplicates) | Here: consecutive accident codes, identical in every field, so entry errors. In NOAA: separate zone entries with their own narratives. |
| Identifier, copy and constant drops: `acc_code`, `file_year`, `route_class`, the vehicles-and-pedestrians total, `n_bus`, `n_farm_vehicle` (CLEAN-3, CLEAN-5, CLEAN-22) | consistent | CLEAN-5 as written; CLEAN-22 ("a copy") | The column auditor checked each one. |
| Injuries dropped (LEAK-10) | consistent | fremtpl2 (CC, Andrej, 2026-10-20: `ClaimNb` dropped next to the claim amount); noaa_storm_events_damage (same run: injuries, deaths and crop damage dropped); the screening lines of nyc_motor_vehicle_collisions and chicago_traffic_crashes | Another outcome of the same crash, recorded with the target. |
| Report date and time used for the as-of filter, then dropped (LEAK-10; LEAK-38 as amended) | consistent | 2_month_survival_rate_prediction (Lennart, 2026-10-12 and 2026-10-26: fields whose gaps follow the death are dropped); kick, expresso_churn_prediction (LEAK-38 amended 2026-10-22: a mechanism measured by outcome goes to LEAK-10); brazilian_ecommerce, sf_permit_time (completion date used only to filter training rows) | Measured: of the crashes reported within a week, 15-20% had a death, against 8% of those reported after four months. |
| `presumed_cause` and `collision_type` kept, set by the officer when the deaths are known (LEAK-10, LEAK-6, USE-6) | departs; the stated reason does not set it apart | distribution_transformers_at_cauca_department (dropped, Lennart, 2026-10-21: values set after the outcome for an unknown subset, "no amendment for a gain that may sit on the changed rows"); onlinenewspopularity (LEAK-10/LEAK-6 amended 2026-10-26, Lennart: keep with a note only when the traceable part shows no gain; a "removing it changes no score" test alone is no reason to keep); house_sales and digicow (Lennart, 2026-10-21: kept as `Potential leak, kept on purpose:` with a revisit condition); breast_cancer_prediction (the radiologist's reading is the actor's own input); noaa_storm_events_damage (same run: the office's estimated winds kept in the kept-leak form) | Keeping is defensible under LEAK-6 (a small optimism with a known cause), but three things depart. (i) The reason given leans on the small gain (R^2 0.171 against 0.162, AUC 0.840 against 0.833 without both), which LEAK-10's amended clause says is not enough alone. (ii) The column auditor found a trace of the mechanism: off the New Year and Songkran campaign days, crashes coded drunk driving are fatal in 0.210 of cases against 0.113 for the rest; on campaign days, 0.116 against 0.118. That moves the case toward distribution_transformers. (iii) The bullet starts "Note:" with no revisit condition and no `_decisions` table (definitions.md, "Recording decisions"; 27 definitions use the kept-leak form). The builder's issue 1 calls this a "Should" call; LEAK-10 and USE-3 are Musts, so the keep can rest only on LEAK-6's narrowing, never on an exception. Prompt 2. |
| Missing values (coordinates outside Thailand; a vehicle count of 0 with no first vehicle) and the site code split into layout and slope (CLEAN-10, CLEAN-11, CLEAN-12) | consistent | churn_telco_south_asia, heart_disease_va_long_beach (impossible values made missing); perth_house_prices (CLEAN-12, Lennart, 2026-10-26: a flag split from a compound field) | Same mechanisms. |
| Category labels kept in Thai; 2019's missing columns left missing (CLEAN-12, P7) | consistent | avito_demand_prediction_1m (Russian categories and text kept); brazilian_ecommerce (translated with the source's own translation file) | The ministry publishes no translation. The Kaggle English is a third party's, made on an earlier version, so a mapping from it would be our own. |
| Target `deaths`, a raw count, regression (USE-5, CLEAN-16, TP-6) | consistent | frempl (same run: the amount kept although only the claim part carries signal); forest_fires (TP-2, 2026-10-06: zero-inflated target kept); blogfeedback (same run: a raw count); wadden_sea, pennsylvania_oak_hickory and noaa_afsc (same run: log1p for long-tailed abundances) | CLEAN-16 is decided case by case. 98.6% of crashes have 0 or 1 death and the maximum is 13, so a log changes little: an evident fact. |
| The zero-inflation reading and the record's tag `Two-Regime Zeros` (Andrej's definition, policy question 4, 2026-10-30) | not checked against the curator's definition | how_much_did_it_rain_ii (tag removed 2026-10-30 under that definition: the mode is "the first step of one count of tips"); the triage summary's list of count targets to check at /add-dataset (korea_bee_sting_injuries_district_year, rand_health_insurance_experiment_doctor_visits) | The zero is by far the most frequent value (87.5%, then 10.8%, 1.3%, 0.24%). But a negative binomial with the same mean (0.146) and variance (0.188) and no extra zeros gives 87.9% zeros, so the zero may be only the first step of an overdispersed count. Prompt 5 (a tag; no verdict depends on it). |
| Temporal regime; routes recur as known entities (SPLIT-6, SPLIT-13, USE-10) | consistent | the screening (SPLIT-6); SPLIT-13 (an entity recurring across the cutoff is part of the task when the model predicts for known entities) | An agency ranks its own network. The split auditor finds the same skill under a random 3x3 split, so the regime rests on the use case (SPLIT-4). |
| As-of filter on the report date plus a 2-month gap (SPLIT-9, SPLIT-10) | consistent | brazilian_ecommerce (Lennart, 2026-10-15: a 1-month gap plus delivered-by-start); house_sales (review of 2026-10-20: a gap of about the median recording delay); zillow_prize (1 month); melbourne_housing_market (Lennart, 2026-10-21: a gap only if the newest months show selection); sf_permit_time (widened to 6 months because a 1-month gap "still censored the slow permits": LightGBM predicted 0.58 log days too fast) | Selection exists, so a gap is due (melbourne): crashes reported in the two months before a start are more often fatal in 17 of 18 cells (the builder's reporting probe). The gap is the median delay, as in house_sales. Selection remains in the 2-4-month band (9 of 9 cells, by 0.001-0.033). Unlike sf_permit_time, no bias in predictions is measured: mean prediction over mean truth is 0.983 with the gap and 1.017 without (the builder's gap experiment, epoch as a feature). Also, a 6-month gap would put the oldest window at 49.7% of the rows, below SPLIT-14's floor (4 months: 53.8%; my script). This is the fact that sets it apart, but it is not written in `splits_comment`. |
| Two-month windows, nine of them (SPLIT-12, SPLIT-15) | consistent; the reasoning is not written | the SPLIT-12 family case (Lennart, 2026-10-21: "we dont need to force the same split"; each keeps its own horizon or refit cadence); zillow_prize (9 windows, "the number of splits an IID task of this size gets"); coffee_rating_prediction (two-month windows, SPLIT-17) | The source gives no horizon. `splits_comment` asserts a two-monthly refit but does not say why two months rather than one or three (SPLIT-12: "write the reasoning down"). |
| Training history from 2019, including COVID-19; 2 of 9 windows in the 2021 lockdown months (SPLIT-20, SPLIT-21) | consistent; the check is not written | aeolus (Lennart, 2026-10-12: history from 2023, after the collapse in flights); perth_house_prices (Lennart, 2026-10-26: `step=3` so most windows fall outside the COVID months) | 7 of 9 windows lie outside the lockdown. Monthly crash counts in 2020 stay within 2019's range except April, when Songkran was cancelled (1,423 against 2,662 in 2019 and 2,789 in 2021). The oldest window needs 2019-2020 to keep 58.4% (SPLIT-14). These facts set it apart from aeolus, but SPLIT-20 asks to "say why", and `splits_comment` does not. |
| Proposed warnings: `splits_rows_unused` (177 crashes), `task_target_value_dominant` | consistent | brazilian_ecommerce (4 orders) and sf_permit_time (193 permits), accepted for the same mechanism; australian_vehicle_insurance_2004_2005 (same run) for an observed zero | Same mechanisms. |
| Metric: fallback `rmse`; Poisson deviance not added (MET-1, MET-5, MET-11, MET-13) | consistent | churn_telco_south_asia (fallback kept, Lennart, 2026-10-21); gallstone_disease (MET-5: a paper with several metrics side by side means fallback; the claim auditor's EECSS 2024 paper reports five); blogfeedback (same run: raw count, fallback `rmse`); thailand_road_accident_fatalities_2015 (screening: fallback `rmse`). Context metrics elsewhere: diamonds (`rmsle`, Lennart, 2026-10-21), noaa_storm_events_damage (`rmsle`, same run), the insurance Gini (AI suggestions of 2026-10-30) | Evident facts set it apart from the context calls. Deaths run from 0 to 13 and an extra death counts the same in any crash, so there is no relative-error argument. RMSE separates models here (R^2 0.17; families spread +0.027, paired SE 0.006), unlike the insurance amounts. RMSE and Poisson deviance are both minimised by the conditional mean. Not adding the deviance follows the family reasoning of 2026-10-30 (it needs positive predictions, so it is no benchmark metric without a clipping rule) and MET-13 (a metric only one definition holds is never shipped). |
| `fit_reason` lists the officer's fields as a gap (USE-8) | departs, wording | kick, homesite_quote_conversion, house_sales, zillow_prize and five others (CCs of Lennart, 2026-10-21: a kept leak is named in `fit_reason` "as kept, not as a gap") | The fit stays approximate for its other two reasons: the death-counting window is not stated (differentiated_thyroid_cancer_recurrence), and no user is named (mobile_churn). australian's precedent check raised the same wording in this run (frempl and spanish share it). Prompt 4. |

**Drift and amendments**

* Andrej's calls: on 2026-10-30 he gave this record `Yes` and the 2015 sibling 2nd Tier "because we have better data for the same task". On fremtpl2 (2026-10-20) he dropped the sibling outcome next to the target, as the injuries are dropped here. I see no drift.
* SPLIT-10: the register flags an amendment as due, on five datasets. The proposed wording in `splits.md` (ames_housing, perth_house_prices) needs two facts: a delay shorter than the time column's resolution, and no selection in the newest period. This definition keeps a gap, so it adds no exception. The "no gap" alternative in builder issue 2 would meet neither fact: the delay is weeks against times dated to the minute, and the newest months show selection. It would be a departure without a reason.
* Third exception: none. The definition records no `Exception to` line.
* Cases rows due once the curator decides: (1) the officer's reading in a crash register under LEAK-10. nyc_motor_vehicle_collisions, chicago_traffic_crashes and nhtsa_crss_crash_severity (AI drafts, `TBD -> Yes`) carry the same kind of field (contributing factors, `PRIM_CONTRIBUTORY_CAUSE`), so this decision becomes their precedent. (2) The prediction point of an incident register whose description and outcome are entered together. This dataset and noaa_storm_events_damage, from the same run, currently set it two ways.

**The builder's draft issues against precedent**

1. Keep or drop the officer's fields: the precedents split (prompt 2). The issue's strength label is wrong: LEAK-10 and USE-3 are Musts, so this is a LEAK-6 call and cannot be an exception to a Should.
2. Two-month windows and gap, or no gap or quarterly: the gap follows SPLIT-10 as applied (house_sales, brazilian_ecommerce). "No gap" would depart without the facts of the proposed amendment. Quarterly windows are a SPLIT-12 choice with no precedent against them. The label "Weigh" should read Should (SPLIT-10, SPLIT-12).
3. Extend to 2024-2025: prompt 3. The 2023 crosswalk would go against the eryhemato row and force_2020 (CLEAN-21).
4. Archive the 2026 snapshot: pinning with MD5 sums matches the working copy's practice. No precedent decides whether to archive a copy; sf_permit_time's revisit line ("re-download in 1-2 years") is the closest.
5. `rmse` or a Poisson deviance with a clipping rule: `rmse` is consistent. A deviance would ship once in `data_foundry.v2.metrics` (MET-13) and raise the same question for noaa_afsc_bottom_trawl_survey_cpue (its source also reports Poisson deviance explained), wadden_sea, pennsylvania_oak_hickory, blogfeedback and rand_health. Decide it once for the family; the domain practitioner would prefer the deviance.
6. Thai labels and the 2019 gaps: consistent (avito_demand_prediction_1m; columns a year lacks stay missing).

**Reflection prompts**

1. **Consistency check (AI, 2026-11-01):** the draft's prediction point, "a crash on the ministry's network has been recorded", is the moment the register holds that crash's deaths, so the model predicts a label already on record. glioma_grading_clinical_and_mutation_features was retired on that fact (`No`, Lennart, 2026-10-26: "a model can only cross-check a label that already exists"). noaa_storm_events_damage, from this run, puts its prediction point at the first report, before the outcome is estimated. What sets this task apart?
   (a) The agency acts on expected deaths per crash type and road section, which no record holds, since each holds one realised count. This is the severity part of network screening, the relative severity index of HSM chapter 4, as the domain practitioner describes it. Named in `use_case` and `fit_reason` as the fact that sets it apart from glioma; the fit stays approximate.
   (b) Treat it like noaa_storm_events_damage: a first-report prediction point (a dispatcher, or TRAMS's next-morning summary), dropping `presumed_cause` and any other field entered with the outcome.
   (c) Reopen glioma_grading_clinical_and_mutation_features to match.
   (d) Amend USE-3 for registers whose description and outcome are entered together.
2. **Consistency check (AI, 2026-11-01):** the draft keeps `presumed_cause` and `collision_type`, which the officer sets when the deaths are known, "because they describe the crash a road agency acts on ... and they carry little of the signal". That differs from distribution_transformers_at_cauca_department (dropped, Lennart, 2026-10-21: values set after the outcome for an unknown subset). LEAK-10 as amended on 2026-10-26 also says a "removing it changes no score" test alone is no reason to keep. The column auditor's trace: off the campaign days the drunk-driving code is fatal in 0.210 of crashes against 0.113 for the rest, and on them 0.116 against 0.118. What sets it apart?
   (a) The officer's reading is the input the agency itself acts on (speeding, drink-driving, rollovers), as the radiologist's reading is in breast_cancer_prediction (USE-6). The trace sits on one code of 53 and is circumstantial. So the fields stay under LEAK-6, written as `Potential leak, kept on purpose:` with the trace, the numbers and a revisit condition (house_sales, digicow, noaa_storm_events_damage's estimated winds), plus a `_decisions` table.
   (b) Treat it like distribution_transformers: drop both fields (R^2 0.171 to 0.162), or `presumed_cause` only (to 0.166).
   (c) Reopen distribution_transformers_at_cauca_department to keep its inventory fields with a note.
   (d) Amend LEAK-10 for an event description that the reporting actor records after the outcome.
3. **Consistency check (AI, 2026-11-01):** the draft stops at 2022 because those are "the years the record names", although the 2024 and 2025 files use the older coding (about 47,700 crashes). noaa_storm_events_damage and crms_phragmites_cover, from this run, test on their newest years, and SPLIT-11 makes the newest window the most representative one. What sets this dataset apart?
   (a) Using 2024-2025 needs either our own crosswalk of 2023 (a fix of our own invention: the eryhemato row of the Tensions table, and CLEAN-21 with no published conversion) or a year-long hole in the history of every newer window. Your `Yes` was given on the 2019-2022 record. Recorded as the reason in the "Years" bullet.
   (b) Treat it like the siblings: add 2024-2025 with 2023 left out, rename the dataset, and move the windows to 2024-2025.
   (c) Reopen the siblings' choice of their newest years.
   (d) Amend SPLIT-20 to say when a coding break ends the usable history.
4. **Consistency check (AI, 2026-11-01):** `fit_reason` lists "the officer records the presumed cause and the kind of collision when the outcome is known" as a gap. That differs from kick, homesite_quote_conversion, house_sales, zillow_prize and five others, which name a kept leak in `fit_reason` as kept, not as a gap (USE-8 as amended, Lennart, 2026-10-21). What sets it apart?
   (a) If prompt 1 ends in a first-call reading of the use case, the two fields are a gap of the data against that moment, not a kept leak, and the sentence stands.
   (b) Treat it like kick: name the two fields as kept. frempl and australian in this run use the same wording.
   (c) Reopen the nine cases of the amendment.
   (d) Amend USE-8.
5. **Consistency check (AI, 2026-11-01):** the record keeps `Two-Regime Zeros` and the notes call the target zero-inflated. Under your definition of 2026-10-30 ("by far the most frequent one and independent of the remaining target distribution"), the tag left how_much_did_it_rain_ii, whose mode is the first step of a count. Here a negative binomial with the target's mean and variance and no extra zeros gives 87.9% zeros, against 87.5% observed. The hurdle result (R^2 -0.049 for the count given a death) is also what such a count gives, since only 12.9% of fatal crashes have two or more deaths. What sets it apart?
   (a) A crash without a death belongs to another severity class (injury or damage only), so whether anyone dies is a mechanism of its own: the hurdle probe ranks it at AUC 0.840. The tag stays.
   (b) Treat it like how_much_did_it_rain_ii: remove the tag and describe the target as a count with many zeros (the accepted warning stands).
   (c) Reopen how_much_did_it_rain_ii.
   (d) Sharpen the tag's definition, for example to zeros in excess of a fitted count model.

</details>

<details><summary>Advocate</summary>

**Advocate, opening brief (AI, 2026-11-01): thailand_road_accident_register_2019_2022**

Position: ship after documentation changes. One field-level call is open, and the dataset ships whichever way it
goes. No evidence agent found a validity failure in the data, the splits or the metric. The blind reviewer: "None of
them is about honesty". What is open: a P3 wording question (what sets this task apart from glioma), a LEAK-6 call on
`presumed_cause`, and notes. Two new measurements of mine are below (the blanks by agency and the years; the drink-driving code
masked).

**1. The task is a real decision, so USE-2 does not bind (P3; USE-1, USE-2, Must). This answers precedent prompt 1 (glioma) and the blind reviewer's "retrospective".**
- Evidence. The domain practitioner, the role that judges the use case, rates the fit approximate, not none. A model
  of the expected deaths of a crash, given its type, vehicles, place and time, is a learned version of the relative
  severity index in HSM chapter 4 ("Monetary crash costs are assigned to each crash type ..."). The DRR also ranks
  black spots by a severity-weighted count (Treeranurat & Suanmali 2021). Summed per section, the model flags the
  sections whose crashes are deadlier than their mix predicts. The practitioner's answer to whether it would use the
  model: "As a severity screen, yes". The blind reviewer: "Severity modelling on police and highway crash registers is
  a well-established real use."
- What sets it apart from glioma_grading (`No`, Lennart, 2026-10-26). There the model reproduces the label already
  on file, and nothing acts on a predicted grade. Here the decision uses the expected deaths given the circumstances,
  which no record holds. Each record holds one realised count, and that count is noisy: 87.5% zeros, and a negative
  binomial with the same mean gives 87.9% zeros (precedent checker). Screening uses expected severity because the
  severity observed per section is mostly noise. That is the fact prompt 1 asks for (its option a).
- The curator gave `Yes`, priority 5, on 2026-10-30. The us_accidents question was written in the screening block
  when he did, and on the same day he set the 2015 sibling to 2nd Tier because "we have better data for the same
  task". A curator's decision ranks above an AI reading.
- Why this wins. SEL-7 and glioma are about a label nobody needs predicted. The practitioner's sources show that the
  expected value is needed. The fit stays approximate (USE-8). Mildest remedy, a wording change: `use_case` and
  `fit_reason` name the severity part of section screening, without crash frequency or exposure.

**2. The evaluation is honest, and three agents measured it (P4; LEAK-10, SPLIT-9, SPLIT-14, Must; SPLIT-10, Should).**
- The outcome columns are gone: injuries (serious, minor, total), the report date and time, `acc_code` (it follows
  the order of entry) and the vehicles-and-persons total. The column auditor finds that LEAK-10 holds for all 26
  features. In the leak probe the best single feature reaches R^2 0.087, and 0.2% of test rows have an exact copy in
  training.
- The as-of filter works: in 9 of 9 windows no training row was reported on or after the window starts (split and
  claim auditors). The gap is at least 2 months in 9 of 9, and the oldest training side holds 58.4% of the rows
  (SPLIT-14). The gap equals the median reporting delay, as in house_sales and brazilian_ecommerce. The mean
  prediction over the mean truth is 0.96-0.98, so no bias is measured, unlike sf_permit_time.
- The domain practitioner's concern 4, that a blank collision type means fatal, comes from the mix of agencies, not
  from the outcome. Within each agency, crashes with a blank collision type are *less* often fatal: DOH 0.047 against
  0.111, DRR 0.300 against 0.352 (2020-2022, my check). The overall gap (blank for 13.9% of fatal crashes
  against 4.9% of non-fatal ones) is the DRR: its fatal share is 0.30, and 96% of its records have no collision type.
  The agency is known at the prediction point. What is left is that complete records are slightly more often fatal.
  It is worth R^2 0.003 when masked (column auditor), a LEAK-6 note.
- Why this wins. These are the Musts the critic would have to break, and all of them hold. The other split items are
  Shoulds: the reason for the cadence (SPLIT-12), the breaks in the history (SPLIT-20), and the selection the gap
  leaves. Every agent's remedy for them is a sentence in `splits_comment`.

**3. `presumed_cause` and `collision_type` can stay under LEAK-6: the part of the trace that can be located carries no gain (P4; LEAK-6, Must, as narrowed on 2026-10-26; LEAK-10's second clause; USE-6, Must). This answers precedent prompt 2 and column-auditor issue 1.**
- Both fields are known at the written prediction point, and both are the agency's own inputs. The severity index
  is built on crash type, and the DRR's black-spot work names collision type and speeding (USE-6; compare
  breast_cancer_prediction, where the reader's reading is the actor's own input). The collision type is a fact of the
  scene: a pedestrian hit is fatal in 0.58 of cases, a head-on collision in 0.33.
- New measurement (EV-1). The trace is the drink-driving code off the campaign days. I reproduced it: on DOH roads
  the 314 drink-driving crashes off the campaign days are fatal in 0.210 of cases against 0.113 for the rest; on
  campaign days, 0.116 against 0.118. Masking exactly that part changes nothing on the 9 windows: R^2 +0.0011 (SE
  0.0013), ROC AUC +0.0003, RMSE -0.0002 (SE 0.0003). Masking the code on every day costs R^2 0.0026, and dropping the
  field costs 0.0077 (my run, untuned LightGBM, Poisson loss).
- LEAK-6 as narrowed, and LEAK-10's second clause, keep late values that cannot be located row by row "with a note
  only when the part that can be traced shows none" (onlinenewspopularity). That is this case.
  distribution_transformers lost its fields because the late part may carry a gain. So the reason to keep is no longer
  "little signal", which LEAK-10 does not accept on its own. It is that the part that can be traced shows no gain.
- Remedy. Rewrite the "Note:" bullet as `Potential leak, kept on purpose:` with the trace, these numbers and a
  revisit condition (a first-call framing), and add a `_decisions` table. In `fit_reason`, name the two fields as
  kept, not as a gap (the USE-8 amendment; I concede prompt 4).
- If the curator reads it the other way, the fix is to drop `presumed_cause` only (R^2 -0.005 to -0.008, AUC
  -0.002). The dataset ships either way. Independent failures are not conflicts: this field call does not touch the
  task.

**4. The data is the ministry's, repaired from its origin and checked independently (P5; PROV-8, PROV-13, PROV-14, Must).**
- It is built from the first publication, not from the Kaggle copy. The MD5 sums match for 4 of 4 files, and the
  yearly death totals match the source exactly: 3,223, 3,301, 2,715 and 2,619 (blind reviewer). The claim auditor
  finds that 38 of 48 claims hold, that no validity claim is refuted, and that the frame, the splits and the metric
  are what the definition says.
- Three independent checks confirm the 2022 date repair:
  - the Kaggle copy agrees on 6,088 of 6,088 changed dates and on all 11,091 others;
  - the XLSX cells agree on all 8,135 ambiguous crash dates;
  - the holiday peaks fall where they should: 310, 225 and 221 crashes on 1-3 January 2022, against a median of 50
    a day, and the Songkran peak in April.
  The naive reading has 2,472 crashes reported before they happened; the repaired reading has none.
- I concede the 5 refutations. All are about documentation:
  - the 2022 report dates were not checked against the XLSX (the CSV reading is right: no crash is reported before
    it happened, against 1,579 under the XLSX reading);
  - the duplicate codes are not "consecutive", and 4 near-duplicate pairs exist, each inside one window;
  - "collision type in another scheme" overstates it (94% of the 2023 labels overlap, though site and cause did
    change);
  - the count given a death is weakly predictable after all (point 6);
  - the EECSS 2024 paper is missing from the metric reason (point 6).
  Each is an edit of one clause, in the claim auditor's wording. Optionally, drop the near-duplicate pair that differs
  only in collision type.

**5. Stopping at 2022 and keeping 2019 follow from the data, not only from the record's name (P5 over P7; the Tensions row "a better version against our own fix", eryhemato; CLEAN-21, Should; SPLIT-14, Must). This answers precedent prompt 3 and the blind reviewer's concern 1.**
- 2023 recodes the site and the cause: only 7.5% and 20.0% of its labels exist in 2019-2022. It also holds 1,641
  crashes two or three times. The blind reviewer matched the headers, which says nothing about the codes. Using
  2024-2025 needs either a crosswalk of 2023 of our own making or a year-long hole before every new window. The
  precedents are against our own crosswalk: force_2020 (without a checked conversion, mask rather than convert) and
  eryhemato (our own fix does not replace the data). A 2024-2025 rebuild would be a new dataset to screen later (the
  domain practitioner: "Later, not now").
- Dropping 2019, to remove its 12 columns that are missing by design, breaks SPLIT-14: the two oldest windows would
  train on 49.4% and 45.5% of the rows (my check). Columns missing in older training years are an honest
  artefact that a model has to handle. The column auditor finds that 2019's `vehicles` distribution matches the
  later years.
- Remedy: write this reason in the "Years" bullet (prompt 3, option a). No rebuild.

**6. The dataset is worth benchmarking, and the fallback scores it correctly (P6; TP-2, Should; MET-5, Should; MET-11, Must; MET-13, Must).**
- The signal: skill +0.146 to +0.175, the model beats the dummy in 9 of 9 windows, the model families spread by
  +0.027 (paired SE 0.006), and ROC AUC for any death is 0.84. Each window has 2,492-3,978 test crashes, 256-449 of
  them fatal, and every fold can be scored.
- The metric. The source defines none. The one paper (EECSS 2024) reports five metrics side by side on a binary
  task with a random split. Under MET-5 that sends the task to the fallback, as for gallstone_disease. RMSE is
  minimised by the mean, the quantity that is summed per section. Over six models it orders them exactly as the
  Spearman correlation per section does (Kendall tau 1.0, domain practitioner).
- I concede two weaknesses (MET-10 factors). The top models are hard to tell apart: their paired differences are
  0.0010-0.0015 with SE 0.0013-0.0020. Crashes with 3 or more deaths carry about 25% of the squared error. A Poisson
  deviance needs a floor on the predictions and a library metric (MET-13), and it would apply to the whole family of
  count targets (blogfeedback, noaa_afsc, wadden_sea). That is a decision for the family, not a reason to change this
  dataset. Remedy: add the 25% and the paper to the metric reason.
- Zero inflation. The claim auditor finds the count given a death weakly predictable: R^2 +0.032, positive in 9 of 9
  windows. So the second regime is real; correct the -0.049 sentence. Prompt 5 (the tag) changes no verdict.
- The blind reviewer's concern 5 (drop `route`). A model that overfits a high-cardinality column is no reason to drop
  it (CLEAN-22, Must; EV-4). The route is the road identity that the agency ranks.

**7. The label's gaps are named, and USE-5 allows them with an approximate fit (P3; USE-5, USE-8, Must).**
- How long after a crash a death counts is stated nowhere: not on CKAN, in the MOT 2565 PDF, on Kaggle or in a
  search. Deaths are revised in place: the deaths changed for 41 of 3,210 re-keyed 2022 crashes (32 down, 9 up).
  Otherwise the 2023 and 2026 copies agree on deaths in every matched row.
- USE-5 lets a label whose construction is undocumented ship with an approximate fit and a note (diabetes_3,
  alfa_battle_2_0_task_2, differentiated_thyroid_cancer_recurrence). The declared fit is approximate already and
  names this gap. Deaths are the ministry's headline indicator and the quantity summed per section.
- Remedy. Add two facts to the notes:
  - the revision in place;
  - the agencies' reporting thresholds: DRR records are mostly casualty crashes, with a fatal share of 0.28-0.32
    against 0.10-0.12 for the DOH.
  The agency is a feature, so the model learns each threshold, as a road agency ranking its own network would.

```text
Verdict: ship after documentation changes.
Validity: SEL-3/USE-2 hold (severity screen, the HSM severity index; fit approximate); USE-3 holds once the reason
  is named (prompt 1, a); LEAK-10 holds (injuries, report time, acc_code dropped); LEAK-6 keep of presumed_cause and
  collision_type with a kept-leak note (traced part: R^2 +0.001, SE 0.001); SPLIT-9 and SPLIT-14 hold; SPLIT-10 holds
  (gap = median delay); PROV-8 and PROV-13 hold (2022 repair, three checks).
Value: TP-2, a real signal (skill 0.15-0.18, spread +0.027); MET-5/MET-11 fallback rmse.
Quality: 5 documentation corrections; SPLIT-12 and SPLIT-20 reasons to write; CLEAN-22 keeps route.
For the curator: prompt 1 (name the fact), prompt 2 (keep with a note, or drop presumed_cause only), prompt 3
  (write the reason).
```

</details>

<details><summary>Critic</summary>

**Critic, opening brief (AI, 2026-11-01): thailand_road_accident_register_2019_2022**

```text
Verdict: not as defined; ship after changes.
Validity: USE-3/USE-1 triggered (the prediction point is the moment the deaths are on record), fix the definition;
  LEAK-10 triggered (presumed_cause follows the outcome and carries a measured gain), drop it; SPLIT-11/12/20 departed
  from without written reasons; EV-7 (a check claimed that was not run).
Value: MET-11 (the metric reason misstates the search); MET-10 factor (RMSE leans on 0.3% of crashes); EV-6 (the
  zero-inflation reading is wrong both ways).
Quality: nothing raised as a reason to hold the task back.
```

The data is faithful and the split mechanics hold (claim, column and split audits). My case is about what the task
claims to be, one column, and the reasons the notes give. My one new measurement is in point 2: untuned LightGBM, Poisson
loss, 300 trees, on the 9 shipped windows and the column auditor's frame (EV-8).

**1. The prediction point is the moment the deaths are already on record (P3; USE-3 and USE-1, Must).**
- Problem: `curation_comments` puts the prediction point at "a crash on the ministry's network has been recorded ...;
  its deaths are predicted". In TRAMS the deaths are a field of that same record, entered a median 27 days after a
  fatal crash and 57 after any other (claim auditor, row 22). The source names no actor (CKAN objective: "to serve the
  public"). The domain practitioner, speaking as the actor: "I never need to predict the deaths of a crash that is
  already recorded."
- Effect on the task: the benchmark scores a model that reproduces a count the actor already holds. It also makes
  every field written together with the outcome a legitimate input by timing (point 2).
- Precedent: glioma_grading_clinical_and_mutation_features, `No` (Lennart, 2026-10-26; use_case.md Cases, USE-1): "a
  model can only cross-check a label that already exists ... the source names no clinical setting". In this run,
  noaa_storm_events_damage (not yet decided) puts its prediction point at the first report, before the outcome exists.
- Remedy (fix the definition: text, plus the drop in point 2). Write a prediction point at which the label does not
  yet exist. I ask for the first report of the crash. At that point the scene facts are known: where, when, the road,
  the vehicles and pedestrians, the kind of collision. The deaths and the officer's presumed cause are not. USE-9 asks
  for a reading like this, where the features are known and the label is not, before settling. If the curator prefers
  the severity-screening reading that the domain practitioner describes (HSM ch. 4, relative severity index), then
  `use_case` and `fit_reason` must name it as the fact that sets this task apart from glioma, and point 2 still
  applies. If neither is written, glioma's precedent gives `No` (`No Good Target / Scientific Discovery`).
- Under either reading `fit_reason` is rewritten (USE-8, Must):
  - name the unit gap: one crash against a section-year decision, with no frequency or exposure;
  - name the unstated death window;
  - say that deaths are revised in place: 41 of the 3,210 re-keyed 2022 crashes changed between the Kaggle copy and
    today, 32 down and 9 up (claim auditor, row 14; USE-5);
  - drop the officer's fields as a "gap" (USE-8 as amended: a kept field is named as kept);
  - drop "the source names no user" (the use case answers that).

**2. `presumed_cause` follows the outcome and carries a measured gain (P4; LEAK-10, Must, with LEAK-6 as narrowed).**
- Problem: the officer writes the cause when the deaths are known. The trace was found by the column auditor and
  rechecked by me on the shipped frame. On DOH roads, off the New Year and Songkran campaign days, crashes coded drunk
  are fatal in 0.213 of cases (315 crashes) against 0.113 for the rest. On campaign days, when testing is broad, the
  figures are 0.116 (458 crashes) against 0.118. Put the other way: off the campaign days the drunk code is twice as
  common among fatal crashes (0.92% against 0.43%); on them it is equally common (4.17% against 4.26%). This fits
  drink-driving being recorded because someone died. It is circumstantial (EV-6: "maybe a leak"), and the file cannot
  locate the affected rows.
- Effect on the task: a section ranking built on this model rewards the officer's outcome-coloured coding, not the
  crash's circumstances.
- Gain (my run): RMSE 0.3662 with the column against 0.3679 without (paired SE 0.0005); R^2 +0.0077 (SE 0.0021); ROC
  AUC +0.0023 (SE 0.0007); the column helps in 8 of 9 windows. The note's "little of the signal" is a gain at 3-4 SE,
  not zero.
- Rule: LEAK-10's clause of 2026-10-26 covers values whose late cells cannot be located: they "go when they may carry
  a gain (distribution_transformers_at_cauca_department) and stay with a note only when the part that can be traced
  shows none"; and "a 'removing it changes no score' test alone is still no reason to keep". The precedent is
  distribution_transformers (dropped, Lennart, 2026-10-21). The builder's issue 1 calls this a Should call, but
  LEAK-10 is a Must and has no exceptions.
- Remedy: drop `presumed_cause` (the builder's probe: R^2 0.171 to 0.166). Two related findings need no drop:
  - `collision_type` stays: its blanks follow the agency, not the outcome. The advocate's check shows that within DOH
    and within DRR the blank rows are less often fatal.
  - Other gaps track the outcome: 213 DOH crashes without km, fatal 0.019 against 0.114; 73 DRR crashes without a first
    vehicle, none fatal against a DRR base of 0.30. Masking them costs R^2 0.0028 (SE 0.0009; column auditor).
    Keep them with a `Potential leak, kept on purpose:` note that says the mechanism is open (LEAK-6).
- This call becomes the precedent for the contributing-factor fields of nyc_motor_vehicle_collisions,
  chicago_traffic_crashes and nhtsa_crss_crash_severity.

**3. The years and windows rest on reasons that are not written or do not hold (P4; SPLIT-11, SPLIT-12, SPLIT-20, Should).**
- Problem: the definition stops at 2022 because those are "the years the record names", a procedural reason.
  - The 2026 snapshot holds 2024 and 2025 in the older coding: 99.9-100% of their labels exist in 2019-2022 (claim
    auditor, row 16). That is about 47,700 crashes (precedent checker).
  - The builder's reason against 2023, "needs our own crosswalk", is not the only path. Only the site and the cause
    changed scheme: 7.5% and 20% of their 2023 labels exist in earlier years, against 94% for the collision type (claim
    auditor, row 15; the "collision type in another scheme" in the Years bullet is refuted). CLEAN-21, as applied in
    force_2020, masks values that have no checked conversion. So 2023 can ship with its site and cause blank and its
    1,641 repeated codes (1,702 extra rows) deduplicated.
- Effect on the task:
  - The test windows (July 2021 to December 2022) end three to four years before the snapshot, and two of the nine
    fall in the 2021 low-traffic months (split auditor).
  - The 19,194 crashes of 2019 (23.7% of rows) lack 12 columns by design, and they train every window (blind
    reviewer).
  - An agency refitting today would train on 2019-2025.
- Also not written in `splits_comment`:
  - Why the windows are two months long (SPLIT-12: "write the reasoning down"). The split auditor's count supplies a
    reason: they are the shortest windows that fill 9 and cover every season once.
  - The breaks in the history (SPLIT-20): April 2020, and deaths per crash falling from 0.168 to 0.127.
  - The selection the gap leaves (SPLIT-10): in the 2-4-month band, the fatal share is 0.113-0.146 among the reported
    crashes against 0.100-0.124 among all of them.
  - Where the RMSE triple comes from: 0.3613 / 0.3619 / 0.3630 were computed on a pre-definition frame (EV-8).
- Remedy:
  - Write these reasons and the triple's source into `splits_comment` (text).
  - For the years: extend to 2019-2025, with 2023's site and cause masked and its repeats dropped, and rename the
    dataset. Or record an exception to SPLIT-11 that names a fact about the data. I find none in the evidence: the
    precedent checker's candidate (a crosswalk or a year-long hole) is answered by masking. This is the curator's call,
    since the name changes.

**4. Provenance claims that were not checked or do not hold (P5; EV-7, Must; LEAK-19, Should).**
- The `DATE_ORDER` comment and the Time bullet say the date orders were "checked against the XLSX files". For the 2022
  report dates, no such check was run: the builder's XLSX comparison loops over 2023-2025, and his ambiguity check covers
  crash dates only. The 2022 XLSX cells also give the opposite day/month reading for 6,823 of those report dates. The
  shipped reading is still right on other evidence: no crash is reported before it happens, against 1,579 under the
  XLSX reading, and Kaggle agrees on 99.98% (claim auditor, row 17). Remedy: name that evidence in the Time bullet.
- Duplicates: "consecutive accident codes" holds only for 2020; the 2022 pair is 7508085 and 7508100. Four more pairs
  share crash time and exact coordinates with equal deaths, and one of them differs only in collision type. Each pair
  falls in one window, so no copy crosses the split. Remedy: reword, and drop the pair that differs only in collision
  type or name the four pairs in the note.
- Not stated in `download_description`: the 2022 XLSX was revised again on 2025-07-23.
- Effect: none on the frame. The point is that the curator's evidence for the repair must be what was actually run.

**5. The metric reason misstates its search and says nothing of weak resolution (P6; MET-11, Must; MET-10, Weigh).**
- The reason says no paper on the register was found. One exists: Ratanawimon and Tanawongsuwan (EECSS 2024, DOI
  10.11159/cist24.179) classify fatal against injured crashes in the 81,735 Kaggle-era records on a random 80/20 split
  and report five metrics side by side. MET-5 keeps the fallback, but MET-11 asks the notes to name the original.
- Resolution:
  - Crashes with three or more deaths are 0.3% of the test rows and carry 14-34% of each window's squared error.
  - The top models differ by 0.0010-0.0015 RMSE, with a paired SE of 0.0013-0.0020.
  - RMSE and the Poisson deviance pick the same best model in only 5 of 9 windows (domain practitioner). In the blind
    reviewer's run, L2 won on RMSE and Poisson on deviance.
- Effect: the ranking among good models leans on a few hundred multi-death crashes.
- Remedy: add the paper and one sentence on resolution to the reason, and keep `rmse`. A Poisson deviance would be a
  decision for the whole family of datasets (MET-13). Not a reason to exclude.

**6. The zero-inflation reading is wrong in both directions (P6; EV-6, Should).**
- "How many die once someone does is not predictable (R^2 -0.049)" is refuted. A regularised Poisson LightGBM gives R^2
  +0.032 on the fatal crashes, positive in all 9 windows (0.006-0.111), with D^2 0.048. The -0.049 comes from the
  untuned model overfitting (claim auditor, row 27).
- The record's `Two-Regime Zeros` tag is also in doubt:
  - A negative binomial with the target's mean (0.146) and variance (0.188) and no extra zeros gives 87.9% zeros,
    against 87.5% observed (precedent checker).
  - The hurdle model adds only R^2 0.003 (0.174 against 0.171).
  - The zero share alone does not show a second regime.
- Effect: the curator weighs a count target against a binary one, and files the dataset in the zero-inflated
  collection, on these two lines.
- Remedy: correct the bullet with the regularised numbers and the negative binomial comparison. The tag is the
  curator's call under the definition of 2026-10-30 (precedent: how_much_did_it_rain_ii).

</details>

<details><summary>Advocate rebuttal</summary>

**Advocate, rebuttal (AI, 2026-11-01): thailand_road_accident_register_2019_2022**

The critic and I agree on the verdict: ship after changes. We differ on two things: whether `presumed_cause` goes,
and how much the choice of years weighs. I ran three new checks, all on the column auditor's shipped frame and the 9
windows with untuned LightGBM (Poisson loss, 300 trees; EV-8): the traced part masked, the zeros a count model predicts, and the 2023 repeats.

**Critic 1, the prediction point (USE-3, USE-1). Narrowed: we agree on the fix, and I concede the `fit_reason` items.**
- The critic accepts the severity-screening reading as enough, provided `use_case` and `fit_reason` name it as the
  fact that sets this task apart from glioma. That was my point 1, so on this point we agree.
- I contest the first-report reading as the main one. USE-9 asks for a use case "that practitioners have", and none
  is in the evidence for this one:
  - The domain practitioner names no actor who predicts deaths from a first TRAMS report. TRAMS's next-morning
    festival summaries count deaths that are already known; they predict nothing.
  - The register has no first-report snapshot. All fields are entered in one record, a median 53 days after the
    crash. A first-report reading would therefore be a stand-in with the same timing question about the fields.
  - USE-9 also weighs against "a use case rephrased only to excuse a gap".
- I concede all five `fit_reason` items: name the unit gap (one crash against a decision per section and year, with
  no frequency or exposure); name the unstated death window; say that deaths are revised in place (41 of 3,210); name
  the officer's fields as kept, not as a gap; and drop "the source names no user". The fit stays approximate (USE-8).

**Critic 2, `presumed_cause` (LEAK-10 with LEAK-6 as narrowed). Contested, with a check.**
- The critic's gain belongs to the whole column: R^2 +0.0077 (SE 0.0021). The amended clause tests something else.
  It keeps late values that cannot be located row by row "with a note only when the traceable part shows no gain"
  (Cases row: onlinenewspopularity, where masking the traced cells changed R^2 by -0.0004, and the values were kept).
  "Removing it changes no score" is the test the clause rejects. The critic's whole-column gain is the same test with
  the sign reversed, so it cannot decide the keep either.
- My check masks two parts and compares the score with the full column:

  | masked part | R^2 | RMSE | RMSE worse than with the full column |
  |---|---|---|---|
  | both drink-driving codes off the campaign days (530 crashes), the part the trace locates | +0.0011 (SE 0.0013) | -0.0002 (SE 0.0003) | 2 of 9 windows |
  | the same, plus the second suspected code, equipment defect (2,438 crashes) | +0.0019 (SE 0.0011) | -0.0004 (SE 0.0002) | 1 of 9 windows |

  Masking either part costs nothing. The column's gain sits on codes with no trace: cutting in (fatal share 0.200),
  running a signal (0.245), illegal overtaking (0.277) and driving the wrong way (0.479). These are behaviours an
  officer reads at the scene. Speeding, the default code, has a fatal share of 0.116, the base rate.
- Why distribution_transformers does not apply. Its values changed "for an unknown subset ... with no record that
  isolates the change", so the gain could sit on the changed rows. Here the trace isolates the mechanism to one code
  (alcohol tests triggered by a death), and those rows carry no gain. The rows that are not coded drunk are 98% of
  the data, so any reverse signal they carry is negligible.
- I concede that the trace is real and that LEAK-10 is a Must with no exceptions. The keep rests on the clause's
  narrowing, not on an exception. It needs the `Potential leak, kept on purpose:` note with the trace, both masking
  results and a revisit condition (a first-call framing), plus a `_decisions` table. If the curator reads the case as
  closer to distribution_transformers, drop `presumed_cause` only. The dataset ships either way.
- On `collision_type` and the km and first-vehicle gaps we agree: keep them with notes (LEAK-6).
- Because this call becomes the precedent for the contributing-factor fields of nyc, chicago and nhtsa, the note
  should state the test (the traced part, masked), not "little signal".

**Critic 3, years and windows (SPLIT-11, SPLIT-12, SPLIT-20, Should). The `splits_comment` items are conceded. On the years I concede the reason and narrow the rest to a weighing call.**
- I concede the four text items: the reason for the cadence, the breaks in the history, the selection the gap leaves,
  and the source of the RMSE triple (or a rerun on the shipped frame).
- I concede that "the years the record names" is not a data reason. My opening point 5 argued "our own crosswalk or a
  year-long hole", and the critic's path answers it: mask 2023's site and cause (CLEAN-21, force_2020). My check
  supports that path. The 1,641 repeated codes of 2023 (1,702 extra rows) agree on deaths in 1,641
  of 1,641. They differ in the crash-date text for 448, which is resolvable by the 2022 method. So the extension is
  feasible.
- What still stands:
  - SPLIT-11 and SPLIT-20 are Shoulds, and the shipped split passes every Must (SPLIT-9, SPLIT-14).
  - Extending means a rebuild: a new name and year range, new windows, and a new review.
  - In the extended version, our own handling would mask a full year of `road_layout`, `road_slope` and
    `presumed_cause`, and choose 448 dates.
  - The curator's `Yes` was given on the 2019-2022 record.
- Weighed. For extending: the newest windows (2024-2025, SPLIT-11), no test windows in the 2021 low-traffic months,
  about 70k more crashes, and the history an agency refitting today would use. Against: a masked year, a
  deduplication of our own, and a review to redo. The weight leans toward extending. It is the curator's call, and I
  no longer claim a data fact for stopping at 2022. Either version ships. Keeping 2019 still stands, because without
  it the two oldest windows train on 49.4% and 45.5% of the rows (SPLIT-14).

**Critic 4, provenance claims (EV-7). Conceded.** The Time bullet and the `DATE_ORDER` comment must name the
evidence that was actually run for the 2022 report dates: no crash reported before it happens (against 1,579 under
the XLSX reading), the accident-code order, and Kaggle's 99.98% agreement. Reword the duplicates bullet, and drop the
pair that differs only in collision type or name the four pairs. Add the 2022 XLSX revision of 2025-07-23 to
`download_description`. None of this changes the frame.

**Critic 5, the metric reason (MET-11; MET-10 a factor). Conceded.** Add the EECSS 2024 paper and one sentence on
resolution: crashes with 3 or more deaths carry 14-34% of each window's squared error, and the top models differ
within their SE. Keep `rmse`. A Poisson deviance is a decision for the whole family (MET-13).

**Critic 6, the zero-inflation reading (EV-6). Conceded, and I retract a sentence of my opening.**
- In my point 6 I said that R^2 +0.032 on the fatal crashes shows "the second regime is real". It does not. It shows
  that the count is weakly predictable, which a single count with a mean that varies by crash also gives.
- New check. Given the features, a Poisson model predicts 89.2% zeros on the test windows, against
  89.0% observed. It predicts 9.1% ones against 9.7% observed, and 1.6% with two or more deaths against 1.3%. There
  are no zeros in excess of the count model, consistent with the precedent checker's negative binomial (87.9% against
  87.5%).
- Correct the bullet with these numbers. Under the curator's definition of 2026-10-30 the evidence favours removing
  `Two-Regime Zeros` (how_much_did_it_rain_ii). That is the curator's call, and no verdict depends on it: the task is
  a count with many zeros, and the `task_target_value_dominant` warning stands.

```text
Verdict: ship after changes.
Validity: USE-1/USE-3 hold once the severity-screening fact is named (agreed); USE-8 fit_reason rewritten, five items
  (conceded); LEAK-10 holds with presumed_cause kept under the LEAK-6/LEAK-10 narrowing (the traced part masked:
  R^2 +0.001 to +0.002, RMSE not worse), else drop presumed_cause only; SPLIT-9 and SPLIT-14 hold.
Value: MET-5/MET-11 rmse kept, reason corrected; the zero-inflation bullet corrected, no excess zeros (a4).
Quality: EV-7 and duplicate wording fixed; SPLIT-12/SPLIT-20/SPLIT-10 reasons written.
For the curator: presumed_cause (keep with a note, or drop); the years (extend to 2019-2025 with 2023 masked,
  favoured on SPLIT-11, or keep 2019-2022); the Two-Regime Zeros tag.
```

</details>

<details><summary>Critic rebuttal</summary>

**Critic, rebuttal (AI, 2026-11-01): thailand_road_accident_register_2019_2022**

```text
Verdict: ship after changes, all of them text. I withdraw the drop of presumed_cause (my point 2): my own checks
  support the advocate.
Agreed: severity-screen reading (prompt 1, a) with the prediction-point bullet rewritten; LEAK-6 keep of
  presumed_cause with a kept-leak note; the EV-7, MET-11 and EV-6 corrections; the splits_comment reasons.
Still disputed: (1) the Years bullet must not say 2023 "needs our own crosswalk": masking (CLEAN-21) needs none;
  (2) the `Two-Regime Zeros` tag (curator's call).
```

New checks, all on the column auditor's frame and the 9 shipped windows (untuned LightGBM, Poisson loss, 300 trees;
EV-8): power and masking, the conditional test (Newton fit), and the same test refitted with BFGS.

**Advocate 1 (the task is a real decision; glioma distinguished). Concede, with a narrowing.**
- The severity-screen reading has evidence behind it: the HSM ch. 4 relative severity index, DRR's equivalent accident
  number, and the practitioner's "as a severity screen, yes". It is the mildest remedy for my point 1 (the remedy
  ladder), so I drop my preference for a first-report point.
- The narrowing: the prediction-point bullet in `curation_comments` must change too, not only `use_case` and
  `fit_reason`. It now reads "a crash ... has been recorded ...; its deaths are predicted", which is glioma's fact
  word for word. It should name the screening moment and the quantity: the expected deaths given the circumstances,
  which no record holds (USE-3, Must).
- On "a curator's decision ranks above an AI reading": I do not contest the `Yes`. It was a screening call, and it did
  not set the prediction point. A screening verdict is provisional until the dataset is built and probed
  (principles.md, Stages).

**Advocate 2 (the evaluation is honest). Concede.**
- The as-of filter, the gap, SPLIT-14's floor and the outcome drops hold.
- The collision-type blanks follow the agency; I conceded that in my opening.
- The SPLIT-10, SPLIT-12 and SPLIT-20 items are sentences in `splits_comment`. I add the source of the RMSE triple
  (a pre-definition frame, EV-8).

**Advocate 3 (`presumed_cause` stays under LEAK-6). Concede. My checks decide it for the advocate.**
- **Conditional test**. The test is a logistic regression of the drunk code on DOH crashes, given the
  crash's hour, weekend, year, first vehicle, collision type, road layout and vehicle count.
  - Off the campaign days, a fatal crash is not significantly more often coded drunk: odds ratio 1.17 (95% CI
    0.88-1.57), against 2.10 without the covariates.
  - The campaign difference remains (interaction OR 0.58, p 0.01), but it sits on the campaign days, where fatal
    crashes are coded drunk less often (OR 0.68, CI 0.50-0.93). That fits checkpoints catching drunk drivers in minor
    crashes. It does not fit testing triggered by a death.
  - The point estimates are the same under a second optimiser (BFGS). The SEs come from the Newton fit, which
    warned that it did not converge. The BFGS refit converged but gives no covariance (a singular Hessian, most likely
    from one of the grouped categories). So read the interval as approximate.
  - I withdraw my opening reading that the code is recorded "because someone died".
- **Masking the traced part improves the score**:
  - R^2 +0.0011 to +0.0033 in 3 of 3 seeds, whether the code is masked as missing or as the default code.
  - On the 158 traced test crashes, the unmasked model predicts 0.16 deaths per crash against 0.30 observed (0.21-0.22
    when masked). So the model does not use the code as a marker of a death.
- **The test could have come out the other way.** A model that knew the traced group's own mean on each test window
  would gain R^2 0.0015 on average (up to 0.0039). That is about the size of the SE, so the test can detect a gain of
  the size the trace allows. Its "shows none" is not a test that cannot fail (EV-6).
- **So:** LEAK-10's clause of 2026-10-26 (onlinenewspopularity: keep with a note when the traceable part shows no gain)
  applies.
- **Remedy, agreed:** a `Potential leak, kept on purpose:` note with a revisit condition and a `_decisions` table. The
  note needs:
  - the trace, and the conditional and masking numbers (the advocate's and mine);
  - a statement that the column's gain (R^2 +0.0077, SE 0.0021) comes from codes whose timing cannot be traced. "Little
    signal" alone is no reason under LEAK-10.
  - The km and first-vehicle gaps go into the same kind of note (LEAK-6), which both sides agree on.

**Advocate 4 (the data is the ministry's, repaired and checked). Concede.**
- The edits are required, not optional: EV-7 is a Must on what the notes claim. The advocate already lists them as
  edits.
- Dropping the near-duplicate pair stays optional on both sides (LEAK-19, Should).

**Advocate 5 (stopping at 2022 follows from the data). Partly concede; one claim disputed.**
- Agreed: keep 2019. I never asked to drop it, and SPLIT-14 would break (49.4% and 45.5%, the advocate's check). Agreed
  too: no rebuild now. It is a Should (SPLIT-11), and since the name changes, it is the curator's call.
- Disputed: that using 2024-2025 "needs either a crosswalk of 2023 of our own making or a year-long hole".
  - The advocate cites force_2020 against a crosswalk. Its CLEAN-21 Cases row says "curves without such a check are
    masked, not converted". Masking 2023's site and cause is therefore neither a crosswalk nor a hole.
  - What carries over from 2023: 94% of its collision types and every other column. Its 1,641 repeated codes can be
    identified (claim auditor, rows 15-16).
  - The advocate's own defence of 2019 applies here too: columns missing in a training year are "an honest artefact
    that a model has to handle".
  - "Headers say nothing about the codes" is true of 2023. It is not true of 2024-2025: 99.9-100% of their labels
    exist in 2019-2022 (claim auditor, row 16).
- Remedy: the Years bullet gives the true reason. The dataset keeps the 2019-2022 scope the record was approved on.
  2023 could join with its site and cause masked, and an extension to 2025 is a follow-up for the curator. Writing
  "needs our own crosswalk" would state a reason that does not hold (EV-7).

**Advocate 6 (worth benchmarking; the fallback metric). Concede, except on the tag.**
- Agreed: the signal, `rmse` as the fallback, and adding the paper and the 25% figure to the reason (MET-11). Route:
  no dispute (I did not raise it).
- Narrowed: R^2 +0.032 on the fatal crashes shows the count given a death is predictable. It does not show a second
  regime, because the positive part of one overdispersed count is predictable too. The relevant fact is the negative
  binomial comparison: 87.9% zeros against 87.5% observed, with no extra zeros. The tag stays the curator's call
  (prompt 5; how_much_did_it_rain_ii).

**Advocate 7 (the label's gaps are named). Concede.**
- Both facts go into the notes: the revision in place, and the agencies' reporting thresholds. This matches the
  `fit_reason` changes in my point 1.

</details>
