# Leak checks

Part 3 of the curation rules, under P4 (Honest evaluation) in [principles.md](principles.md). The rules of earlier parts
win over this file's rules in a conflict; within this file a rule wins over the rules below it of the same strength.
How to weigh, exceptions and amendments: [principles.md](principles.md).

What the BeyondArena leak audit (2026-09-24 to 2026-10-01, all 142 shipped datasets) and the reviews since taught us
about finding leaks and deciding what to do with them. Read it whenever the data can be loaded and before calling a
column a leak or a dataset leaky. The per-dataset detail is in each record's dated comments. The probes keep their
numbers (Methods); other files cite them as "probe N".

A leak is anything other than real signal that lets a model score well: a column that gives the target away or was
recorded after it, a generation or recording artefact that differs by class, copies across the split, a split that
does not match the task, a selection that depends on the outcome, or values computed with the test rows.

## Rules

### Fix the task before testing columns

**LEAK-1 (Must).** Write down the prediction point and the use case first (USE-1, USE-3, [use_case.md](use_case.md)).
Every test below asks whether a value existed at that point.

**LEAK-2 (Must).** Read the data dictionary or codebook column by column. A flagged column is rarely alone: when one
column turns out to be post-outcome, search the codebook for the marker that gave it away, sweep the use case for its
siblings, and drop every column carrying it. Cases: anes_voting_2026's flagged `VCF1005` led to 56 more items marked
"no Post IW" or "no post data" (1 to 57 columns); kickstarter `staff_pick`; sdss `plate` and `fiber_ID` next to
`redshift`.

**LEAK-3 (Should).** Read the source paper before making the call (PROV-16, [provenance.md](provenance.md)).
The paper settled or changed many audit calls: which class is a separate assay (biogeographical_ancestry_prediction),
that the observation window ends at churn (iranian_churn), that the incentive comes from the end-of-day report
(garments_worker_productivity), what the cohort is (diabetes_130_us), which duplicates the authors removed (emscad),
that the real groups are collection sites the file does not hold (maternal_health_risk).

**LEAK-4 (Must).** When a definition changes the target (merges or drops classes, bins or thresholds a number,
binarizes), run the probes against the source's original labels too, and check the shipped label the same way: a
depth-2 or depth-3 tree on its defining columns shows whether the target is a rule. A label the definition builds uses
a convention of the field ([task_probes.md](task_probes.md), TP-7). Why: a merge can hide a column that spells out the
fine label, or the fine label can turn out to be read off a few features. Cases: audiology_diagnosis's three merged
classes hid that its four cochlear diagnoses are set by two history answers, age over 60 and noise exposure (139 of
147 cases).

### Deciding on a suspect

**LEAK-5 (Must).** Never argue "not a leak" because models would predict the same: ask whether the stored values
depend on the test rows. The weight of such a leak then decides the action (LEAK-6, LEAK-30). Cases: coad's z-scores
over all patients were first called harmless (no labels; tree predictions unchanged), but the training rows alone give
each test fold's mean of every feature, so each split hands the model the test patients' distribution (Lennart,
2026-10-16).

**LEAK-6 (Must).** Measure before acting. A slight optimism with a known cause can stay with a note; a confirmed leak
goes even when small. Cases: santander `has_*` (+0.003 AUC).

**LEAK-7 (Should).** The smallest fix that keeps a valid signal beats dropping the column. Cases: lag `incentive`
(garments), drop the months where `PageValues` misbehaves (online_shoppers), cut the censored years (sf_permit_time),
re-source settled labels (consumer_complaints), blank the values looked up after the outcome (zillow_prize,
melbourne_housing_market; 2026-10-21).

**LEAK-8 (Should).** Retire rather than invent structure. Cases: guessed groups (maternal_health_risk, hazelnut;
SPLIT-25 in [splits.md](splits.md)), too few independent events (ghana: 626 farmer-days behind 10,928 rows). A
re-split with too few positives (seismic_bumps) is `Too Small`: [task_probes.md](task_probes.md), TP-9.

**LEAK-9 (Should).** Separate data leaks from evaluation leaks. An evaluation-level leak, where the test set holds
complete trajectories that end at the outcome, is fixed in the scoring (causal per-entity predictions, the task's own
utility), not in the data; document the prediction point. Cases: sepsis_prediction needs a scorer change, not
different data.

Repair or rebuild damaged data from its origin before keeping it: PROV-13 in [provenance.md](provenance.md).

### Values not known at the prediction point

**LEAK-10 (Must).** A feature holds only what existed at the prediction point (LEAK-1) and never gives the target away.
Out: a column recorded after the outcome; attributes looked up after the outcome (a property's current record for a
past sale), unless the data shows they did not change; a part, a consequence or another encoding of the target; a
feature computed from the window that defines the target, even when its value is known at snapshot time; a value fitted
from the same measurement that gives the label; targeting or pointing ids that encode pre-selection or the observation
date; a same-day value that depends on the day's outcome; missingness that encodes the outcome; an aggregate that may
include the row's own outcome. Fix it in the definition the smallest way (LEAK-7), else drop it; when the features
summarise a window that ends at the outcome and no common prediction point can be rebuilt, retire. Test: the codebook
(LEAK-2) and probes 1 to 4. Cases: the Mechanisms table under Cases.

**LEAK-11 (Should; narrows LEAK-10).** A value measured after the outcome that weakens the signal stays, with a note.
Cases: south_africa_coronary_heart_disease.

**LEAK-12 (Must; applies SPLIT-9).** In a temporal task, training rows whose label is not yet known at the prediction
point are filtered out by an as-of date: SPLIT-9 in [splits.md](splits.md). Cases: hotel_booking_demand.

### Artefacts that differ by class

**LEAK-13 (Must; amended 2026-10-26, Andrej, on gallstone_disease).** Class-specific recording conventions are
harmonised: write every row at the precision of the measured values, computed columns and filled cells included, and
drop a column only one class has or one that was filled in for one class only. First measure how much the fix removes.
Test: probes 4, 9 and 17. Cases: hepatitis_c_prediction, gallstone_disease.

**LEAK-14 (Must).** A class that comes from a separate source or assay is dropped once the paper confirms it. Test:
probe 7. Cases: biogeographical_ancestry_prediction.

**LEAK-15 (Must; amended 2026-10-27, Andrej, on gallstone_disease).** A recording artefact that runs through several
features that would matter for prediction in practice, and that cannot be undone (no batch id to drop, no format to
harmonise, no route to align), retires the dataset: a feature subset does not help when it also separates same-label
groups. An artefact confined to features a practical model would not rely on is fixed (LEAK-13, LEAK-14, LEAK-39) or
kept with a note. Test: probes 7, 8 and 17, and the score without the affected features. Cases:
prostate_cancer_detection (retired), gallstone_disease (kept).

**LEAK-39 (Must; 2026-10-26, Andrej, on gallstone_disease).** Rows of one class recorded through a separate route, found
by a recording fingerprint (number formats, a derived column that follows another definition, a shifted measurement)
rather than a source column, are dropped when models recognise them and the route cannot be aligned with the other
rows: too few rows of the other class went through it to calibrate it. Find them as rows of one class that share the
formats the other class rarely has. Then score them against the other class out of fold, and score the other class's
rows of the same route: when those are predicted as the first class, models learn the route, not the target. Test:
probes 7, 9 and 17. Cases: gallstone_disease.

**LEAK-40 (Should; 2026-10-26, Andrej, on gallstone_disease).** Gaps the source filled from neighbouring rows
(interpolation, carried values) in a file sorted by class are tested, not assumed to leak: set the filled cells to
missing and re-impute them inside each training fold without the label. When that scores the same or higher, the fills
stay with a note. Setting them to missing is no fix when the gaps follow the classes: the missing values then mark a
class. Their written precision is harmonised (LEAK-13). Values filled from the label, such as an outcome group's mean,
are LEAK-10 and go back to missing. Test: probe 18. Cases: gallstone_disease (kept),
heart_failure_followup_survival (outcome-group means, set back to missing).

Marker, for a dataset where LEAK-13 to LEAK-15, LEAK-39 or LEAK-40 applied, kept or retired: `Class-dependent
Recording`. It says the classes were measured, formatted or filled differently, so the recording can give the label
away. `Selection Bias` is about which rows were sampled, with the measurements alike.

Generated or manipulated data is retired (`AHDS`, `Data Quality Issue`; SEL-16, PROV-3); how to tell (probe 15):
PROV-3 in [provenance.md](provenance.md), "Is the data generated?".

### Copies across the split

**LEAK-16 (Must).** Duplicate rows need a decision every time; shipped datasets range from 0% to 98% duplicates. Test:
probes 5 and 6.

**LEAK-17 (Must).** Repeated entities in different rows (the same patient, house, molecule or object) leak the target
across the split even when the rows differ: keep one row per entity when the use case is that row (USE-11,
[use_case.md](use_case.md)), or group (SPLIT-24, SPLIT-29, [splits.md](splits.md)). Parse ids as strings: sdss_17's
float-parsed `obj_ID` merged 21,947 distinct objects (it is now deduplicated on the sky position). Test: probe 11.

**LEAK-18 (Should).** Many degrees of freedom and an exact match: a collection artefact, drop it and give the share.
Few features and plausible repeats: natural, keep them and say so. Cases: sepsis_survival_minimal_clinical_records
keeps 110,204 rows over 975 distinct feature rows: three features, real patients, and predicting from them is the
source's question.

**LEAK-19 (Should).** Exact copies with the same label: drop them rather than group on the duplicate key. Cases:
wine_quality (1,177 rows); audiology_diagnosis (27 copies of the same findings and diagnosis on different patient
ids).

**LEAK-20 (Should).** Feature vectors that occur with both labels: drop every copy, unless they are genuine label
ambiguity the task has. Cases: jm1 (176 rows); consumer_complaints. Exception: mortgage (7 loans, Lennart, 2026-10-22)
keeps the payoff copy where period 51 is doubled, because every such loan ends at period 51: the other copy is damage
to the file (PROV-13), not an ambiguous label.

**LEAK-21 (Should).** Reposts identical except an id or a location: drop them, as the source paper did. Cases: emscad
(Vidros et al. 2017, Sec. 5).

### Selection and censoring

**LEAK-22 (Must).** When the cohort holds rows that cannot have the outcome, follow the paper's cohort. Cases:
diabetes_130_us. A competing event after the prediction point (a death from another cause within the horizon) is no such row:
the row stays with the label it had, No, since the risk a patient faces includes it; dropping it selects the cohort
on the future (framingham_heart_study_fhs, 251 deaths, Lennart, 2026-10-22).

**LEAK-23 (Must).** A target over only the rows with the event, with follow-up ending on one date (right truncation),
becomes an outcome within a fixed horizon, over the rows followed that long. Cases:
cirrhosis_patient_survival_prediction.

**LEAK-24 (Must).** A target right-censored in the newest periods (a duration or a final status cut by the download
date) is cut where follow-up is complete, or re-sourced from an archive with settled labels; compare two downloads
first (probe 13). Cases: sf_permit_time, consumer_complaints.

**LEAK-25 (Must).** "No event" mixed with "not recorded" is a censoring bias: retire unless the recording process can
be recovered. Recovered includes unrecorded rows located by a rule that does not read the label, and dropped (amended
2026-10-21, Lennart, on caracas_cervical_cancer, account_debt_south_africa and
fraud_detection_in_electricity_and_gas_consumption_1m). Cases: ghanas_indigenous_intel (retired: the unrecorded rows
could not be located); the three located and dropped (Mechanisms table).

**LEAK-26 (Must).** A target capped at a maximum (a price of 500001, a timeout): drop the capped rows or document the
cap. Cases: the house-price and runtime datasets.

### Statistics and transforms over all rows

**LEAK-27 (Must).** A feature that is the output of a supervised transform fit on the whole labelled set (a
discriminant score, a target encoding, a model's prediction) is irreversible: `Data Quality Issue`, `No`. Marker:
`Data Quality Issue`. Cases: yeast's discriminant-analysis score.

**LEAK-28 (Must).** Label-aware features computed over all rows, test folds included, are dropped; recommend the
technique inside a pipeline, per fold. Cases: santander_customer_transaction_prediction `has_one`, `has_zero`.

**LEAK-29 (Must).** Our own cleaning never computes a feature value from statistics over all rows: compute it from the
history before the oldest test window, or drop it. Cases: sf_permit_time, home_credit_default_risk (Lennart,
2026-10-19).

**LEAK-30 (Must when strong, Should when weak; narrows LEAK-6).** Scaling over all rows is a weak leak. Features the
source transformed with statistics over all rows, test rows included (z-scores, min-max, quantile bins or a quantile
transform, ranks, PCA, RMA, batch correction, a variance filter), carry the test rows into every value: a transductive
leak, labels or not, and one that real data often come with. Rebuild from the unprocessed values when the source has
them (PROV-13); otherwise keep the dataset with a `Potential leak, kept on purpose:` note. Only a strong suspected leak
makes it a reason for `No` (Lennart, 2026-10-19: "not a strong leak and often happens in reality"). Per-row transforms
(a log, a ratio within the row, per-sample TPM or beta values) and fixed published scales are fine. Test: probe 16.
Cases: coad_colon_adenocarcinoma (rebuilt); bioresponse and the others kept with a note (Mechanisms table).

**LEAK-31 (Should; narrows LEAK-6 and LEAK-28).** Supervised feature selection on the full labelled set: measure it;
keep with a note when small, remove it when we can. A selection the source published (the authors' descriptors, a
feature set the host released) is decided case by case (Lennart, 2026-10-21). Cases: home_credit_default_risk
(2026-10-19).

**LEAK-32 (Should).** Masked or anonymised features that may hide such a transform are a known risk of anonymised
data, covered by its tag: no action. Cases: ieee_fraud_detection, kdd_cup_09_appetency (Lennart, 2026-10-19).

### Not a leak

These rules protect against removing real signal.

**LEAK-33 (Must).** A group id column is split metadata, never a feature.

**LEAK-34 (Must; narrows LEAK-10).** An entity's own history under a temporal split is legitimate, also when it
carries labels forward (a known entity: USE-10). Cases: ghana's reporter history; ieee_fraud_detection's `uid` (test
rows whose uid had fraud in train are 95% fraud; dropping it costs 0.001-0.007 AUC; kept).

**LEAK-35 (Must; narrows LEAK-10).** Text written together with the label is the task when it does not map one to one
onto the score. Cases: coffee_rating_prediction's review text (R^2 0.25 to 0.67; kept).

**LEAK-36 (Must).** A value known at prediction time that rules the outcome out is a cohort question (LEAK-22), not a
feature leak. Cases: diabetes "Expired".

**LEAK-37 (Must; applies USE-6).** An input the actor knows at the prediction point is not a leak, even one the
company computed itself (the promised delivery date, the forecast being corrected): USE-6 in [use_case.md](use_case.md).
Such an input that tracks a dropped post-outcome column stays with a note (Mechanisms table: digicow `topics_list`).

**LEAK-38 (Should; narrows LEAK-10; scope amended 2026-10-22, Lennart, on kick and expresso_churn_prediction).**
Anonymised fields that may be post-outcome, in data a company released for its own competition, stay, with a
`Potential leak, kept on purpose:` note giving the mechanism, the numbers, why they stay and when to revisit. Why:
removing an unverified signal from host-designed data is arbitrary. The rule covers only fields whose timing cannot be
tested. When a conditional test measures the mechanism (the field's missingness or fill, given the covariates known
at the prediction point, differs by outcome), LEAK-10 applies and the field is dropped, even if the host's test file
carries it the same way: that file is a holdout of the same snapshot, not deployment data. Cases: homesite
(`PropertyField37` x `PersonalField12`, AUC 0.965 to 0.915, kept); kick's `WheelType` was kept here on 2026-10-01 and
dropped under LEAK-10 on 2026-10-22, with `WheelTypeID`, `PRIMEUNIT` and `AUCGUART` (expresso's REGION the same way).

Also not a leak, with their home elsewhere:

* IID over related entities is optimistic but can match how a task is framed: a candidate for a grouped or temporal
  variant, not a fix (SPLIT-31 in [splits.md](splits.md); amazon_employee_access, bank_marketing).
  concrete_compressive_strength was one until it was grouped by mix on 2026-10-14 (SPLIT-24).
* Choosing which columns or categories to keep by counts over the whole table (the most frequent codes, questions asked
  in one year only) is ordinary cleaning that follows the task's best practice: CLEAN-8 in
  [cleaning_features.md](cleaning_features.md) (rosbank1, alfa_battle_2_0_task_2, anes_voting_2026; Lennart,
  2026-10-19).

## Patterns

Quick ways to apply the rules; a pattern never overrides a rule, and the dataset at hand wins over the pattern.

Reading the probes:

* A drop-one test misses a column that has a copy. kick loses nothing without `WheelType` because `WheelTypeID` holds
  the same information; drop such columns together (probe 1; LEAK-2).
* The label-free distance score is above 0.5 on ordinary data too (heart_failure 0.64, against 0.73 for the full
  model). Compare it with the full model, not with 0.5 (probe 6; [evidence.md](evidence.md), EV-3).
* The string overlap compares exact values: the same molecule written as two SMILES strings, or the same text with
  other whitespace, does not count. Canonicalise (RDKit for SMILES) before comparing when the overlap matters (probe
  5; LEAK-16).
* A pure-value flag on a heavily imbalanced target (base rates of 94-98%: amazon_employee_access, aps_failure) is
  usually an ordinary category effect (probe 4; EV-3).
* A near-saturated score alone is not a leak (diamonds R^2 0.993 and splice AUC 0.99+ showed none). Run the probes and
  report what they found (EV-3).
* A claimed problem gets a second check that tries to refute it with its own code (EV-6). In the audit all 15 findings
  of the first sweep held, and the second checks corrected details and proposed better fixes.

From the reviews (most first suggestions of the audit were revised, and the reviews since added more):

* Say which evidence is proof and which is circumstantial, and report a borderline case as "maybe a leak" for the
  curator to decide, not as "no leak" (EV-6). Two overclaims were corrected in review: reporter history is legitimate
  under a temporal split (ghana; LEAK-34), and "PageValues includes the session's own purchase" is likely, not shown
  (online_shoppers).
* Test the human's intuition with data, in both directions ([evidence.md](evidence.md), EV-1): "the rating would be
  known" was true, but the rating is computed from the target window (mutual_funds: dropped; LEAK-10); "the features
  only use the Kaggle train file" missed that they use all its rows, our test folds included (santander: leak
  confirmed; LEAK-28); "is this a survival task?" turned out to be censoring at download (consumer_complaints;
  LEAK-24).
* Re-check a comment's claim with data (EV-1): kick's "grouped" Kaggle split came from a buggy check, and california's
  "temporal" split ran on alphabetical order (probes 10 and 11).
* Do not call a small grouped task unlearnable from one quick model (SPLIT-27 in [splits.md](splits.md)).

## Methods

### Probes, cheapest first

Score with ROC AUC, log loss or R^2 ([evidence.md](evidence.md), EV-5), and say how many splits a number comes from.
The numbers compare the shipped data with a suspected fix; they are not leaderboard numbers.

| # | Probe | Red flag | Cases |
|---|---|---|---|
| 1 | All features against all but the suspect columns, on the shipped splits | the drop costs more than the column could know at prediction time | heart_failure `time`: AUC 0.90 to 0.75; anes 0.930 to 0.855 |
| 2 | Each feature alone | one column comes close to the full model | heart_failure `time` alone 0.84; sdss `redshift`, STAR against the rest 0.998; online_shoppers `PageValues` 0.974 (Feb-May) |
| 3 | A missing-value indicator alone; the target rate when missing and when present | missingness predicts the label | mic: rows missing `NA_R_3_n` are 95% deaths (base rate 16%); kick: missing `WheelType` 70.5% bad buys (9.7% otherwise) |
| 4 | Pure values: a value, or present against missing, with at least 100 rows and at least 99.5% one class | a value that occurs with one class only | kickstarter `profile_blurb` (0 of 69,970 failed projects); hotel `RequiredCarParkingSpaces = 1` (0 cancellations); airline `Seat comfort = 0` (99.8% satisfied) |
| 5 | The share of test rows whose feature vector has an exact copy in train, without and with the string and datetime columns; for long string columns, the share of test values seen in train | a large share, above all with the same label | maternal_health_risk 74%; wine_quality 24%; qsar_bioconcentration 5.4% on the nine descriptors but 0% with the SMILES (isomers the descriptors do not tell apart) |
| 6 | 1-NN label agreement (closest tenth, all, chance); each row's distance to its nearest other row as a label-free score | near-copies agree on the label almost always (reposts, re-scans); the distance alone comes close to the full model (class-conditional generation) | emscad 0.998 among near-copies; homeq distance alone 0.923 (full model 0.975) |
| 7 | Separate two subgroups that share a label (two sources, two clinical groups, donors and patients) | they separate far better than the label does: a source or batch signal | prostate Benign against NED 0.997; hepatitis_c donor against patient 1.000 from four formatting flags |
| 8 | Features in a range where no signal can exist | they predict the label | prostate m/z < 1 Da: AUC 0.81-0.85 |
| 9 | Number formats by class (share of whole numbers, decimals, units) | the formats differ by class | hepatitis_c `ALB`, `BIL` whole numbers in about 100% of patient rows, 10% of donor rows |
| 10 | Row order: the target by position in the raw file, next-row label match; a time index against the date and against any sort key | the order is temporal or sorted by the target, or the "time" index follows another key | seismic_bumps next-row match 2,583 of 2,583; california time index Spearman 1.000 with the address rank, 0.003 with `Listed On` |
| 11 | Entity overlap: the share of test rows whose entity (respondent, company profile, location, CPU and GPU) is in train; the IID score against the grouped score | a large overlap and a large drop | in_vehicle 0.83 to 0.75; emscad 0.99 to 0.94; video_game_fps: every test CPU and GPU in train |
| 12 | Temporal: rows and minority-class rows per test window | a handful of positives ([task_probes.md](task_probes.md), TP-9), or under about 50 test rows ([splits.md](splits.md), SPLIT-17) | seismic_bumps 0-5 positives per window; ghana rain from 3-6 farmer-days per window; coffee monthly windows of 2-72 rows |
| 13 | The target by period (rows, p50, p90, max), and the same for two downloads of the source | the newest periods lose their slow or late cases: right-censoring | sf_permit_time 2025 p90 rose from 97 to 160 days between the Feb and Oct 2026 downloads; consumer_complaints Jan 2026: 318 rows, 87% one class |
| 14 | A simple formula or lookup for the target; a shallow tree on the label | R^2 near 1; a depth-2 or depth-3 tree close to the full model | video_game_fps: log FPS = game + CPU + GPU, R^2 0.99998; audiology's cochlear diagnoses: two history answers decide 139 of 147 |
| 15 | The generated-data tests of PROV-3 ([provenance.md](provenance.md), "Is the data generated?"; the scope is SEL-16) | see there | ecommerce_shipping, customer_satisfaction_in_airline, homeq_default_prediction |
| 16 | Every block of columns: mean 0 and SD 1, or min 0 and max 1, over the whole table | the source scaled over all rows, test rows included | coad_colon_adenocarcinoma (z-scores over 260 patients); credit_card_customers (clipped at whole-file percentiles) |
| 17 | The number format alone: the decimals each value of a float column is written with, all columns together and the best three alone (`leak_probes.py`) | the format scores far above chance | gallstone_disease 0.949 (best alone: GFR 0.802, two decimals for 80% of those without gallstones and 15% of those with; CRP 0.783; obesity % 0.708, another definition in the second route); 0.666 after LEAK-13 and LEAK-39, nearly all from CRP's exact zeros (0.682), real low values |
| 18 | Cells on a straight line between the cells above and below, per column and class, in the raw file's order (`leak_probes.py`) | many such cells, in one class more than the other: gaps filled by interpolation. Runs of round values are found too; the values tell them apart | gallstone_disease: vitamin D 77 cells, all without gallstones; visceral muscle area 36, all with; GFR 14. Also flagged, and measured: ECF/TBW 8 (each equals the rounded 100 x ECW / TBW) |

## Cases

Precedents: how a rule was applied. They never change a rule; an exception is listed with the fact that set it apart.
The cases of the rules outside this table are named in the rules.

### Mechanisms and what we did

| Rule | Mechanism | Action | Cases |
|---|---|---|---|
| LEAK-4 | A label we built that a few features spell out (classes merged or dropped by the definition) | use a convention of the field and check it with a shallow tree; run the probes on the source's labels too | audiology_diagnosis: three classes from names replaced by hearing loss with or without a conductive part |
| LEAK-9 | An evaluation-level leak: the test set holds complete trajectories that end at the outcome | fix the scoring (causal per-entity predictions, the task's own utility), not the data; document the prediction point | sepsis_prediction |
| LEAK-10 | A column recorded after the outcome | drop it | heart_failure `time` (follow-up ends at death or censoring); anes post-election items; kickstarter `profile`, `staff_pick`; hotel `BookingChanges`, `AssignedRoomType`, `RequiredCarParkingSpaces` |
| LEAK-10 | Attributes looked up after the outcome (a property's current record for a past sale) | drop them, or keep them where the data shows they did not change | house_sales (the King County lesson); melbourne_housing_market: kept for the sales looked up by the weekly runs within weeks of the sale (`Bedroom2` equals the sheet's `Rooms` in 98.9-100% of the rows of each test window), blanked for the 7,578 sales looked up at once by 10 April 2017, up to 15 months after the sale (LEAK-7 row below; Lennart, 2026-10-21) |
| LEAK-10 (decision, Lennart, 2026-10-21) | Attributes looked up after the outcome that changed for an unknown subset of the positives, with no record that isolates the change | drop them; LEAK-10 as written, no amendment for a gain that may sit on the changed rows | distribution_transformers_at_cauca_department: `power_kva` and `installation_type` from an inventory taken during or after 2020 dropped (none of the 163 replacement-marked first burns of 2020 is rated 5 kVA, against 9% of the other 277; no replacement log; ROC AUC 0.701 to 0.639) |
| LEAK-7, LEAK-10 (Lennart, 2026-10-21) | Values looked up after the outcome, where the rows with a changed or later value can be located (a snapshot date, a mismatch with a record made at the sale) | smallest fix: blank the values looked up after the outcome for those rows; a lookup is not kept merely because removing it changes no score (no LEAK-11 keep) | zillow_prize: the tax delinquency snapshot of about September 2016 blanked for the sales before it (1.5% flagged then, against 3.1-4.7% a month after); melbourne_housing_market: the six scraped attributes blanked for the 7,578 sales before the uploader's batch lookup of 10 April 2017 (RMSE +0.0011 to +0.0016 over 3 seeds) |
| LEAK-10 | A part, a consequence or another encoding of the target: sub-scores that add up to it, weight and height when the target is body mass, earlier grades not yet known at the prediction point when the target is the final grade (amended 2026-10-21, Lennart), a current-status column, award notes inside a description | drop it | the UCI student performance data: G1 and G2 are the period grades of the final grade G3, not yet known at its prediction point |
| LEAK-10 | Earlier grades known at the prediction point, when the target is the final grade, and the actor acts on them | keep them | predict_students_dropout_and_academic_success: the first-year grades (Lennart and Andrej, TabArena v0.1); open_university_learning_analytics_dataset: the assessment marks returned by day 60, 10-30% of the continuous-assessment weight of the final result (Lennart, 2026-10-21) |
| LEAK-10, LEAK-7 | A same-day value that depends on the day's outcome | lag it by one period when the earlier value is known at prediction time (shift within each entity in time order), else drop it | garments `incentive`: within teams its daily changes follow the same day's productivity (Spearman 0.53), not the previous day's (0.07); `incentive_lag_1` per team |
| LEAK-10, LEAK-7 | Missingness that encodes the outcome | move the prediction point earlier and drop the columns that do not exist yet | mic: the day-1..3 ICU columns are blank for patients who died earlier; now an admission-time task |
| LEAK-10 | Features summarise a window that ends at the outcome | retire when no common prediction point can be rebuilt | iranian_churn (Keramati & Ardabili 2011, Sec. 4.1; AUC 0.986) |
| LEAK-10 | Snapshot data: a feature computed from the window that defines the target | drop it, even though its value is known at snapshot time | mutual_funds_india `rating` (60% 5-year and 40% 3-year risk-adjusted return; the target is the 3-year return) |
| LEAK-10, LEAK-7 | An aggregate that may include the row's own outcome | keep only the period where it behaves like history, and call the evidence circumstantial | online_shoppers `PageValues`: Feb-May every buyer has PV > 0 (AUC 0.974), Jun-Dec 27% of buyers have PV = 0 (0.814); Feb-May dropped |
| LEAK-10 | Fitted from the same measurement that gives the label | drop it for the task we frame | sdss_17 `redshift` (photometric task) |
| LEAK-10 | Targeting or pointing ids (they encode pre-selection or the observation date) | drop them | sdss_17 `plate`, `fiber_ID` (AUC 0.80 alone; they made log loss worse) |
| LEAK-10, LEAK-38 (precedent, Lennart, 2026-10-22) | A named field whose missingness or fill, given the covariates known at the prediction point, differs by outcome (a conditional test), although the host's test file carries it the same way | drop it | expresso_churn_prediction REGION (flag AUC 0.936 among customers active all 62 days); kick `WheelType`/`WheelTypeID` (1.2% predicted missing for bad buys, 24.9% observed) and `PRIMEUNIT`/`AUCGUART` (42.3% predicted filled, 7.8% observed) |
| LEAK-11 | Measured after the outcome, but it weakens the signal | keep it and note it | south_africa_coronary_heart_disease (ESL Sec. 5.2.2, p. 148; dropping `sbp`, `obesity`: AUC 0.774 to 0.778) |
| LEAK-12 (SPLIT-9) | Temporal: training rows whose label is not yet known at the prediction point | filter training rows by an as-of date | hotel_booking_demand: in-window cancellations in train were 100% cancelled (log loss 1.7 to 0.33); a filter on `ReservationStatusDate` keeps the shortcut |
| LEAK-13 | Class-specific recording conventions | harmonise (round every row to the shared precision, drop a column only one class has); first measure how much the fix removes | hepatitis_c_prediction (7 lab columns rounded, `ALP` dropped) |
| LEAK-14 | One class from a separate source or assay | drop that class once the paper confirms it | biogeographical_ancestry_prediction (Turkey, `rs3857620`) |
| LEAK-15 (amended 2026-10-27, Andrej) | A recording artefact through several features that matter for prediction, that cannot be undone | retire; a feature subset does not help when it also separates same-label groups | gallstone_disease, kept: after LEAK-13 and LEAK-39 the suspected artefacts left (AST lower with gallstones, the fatty-liver grades on two scales) do not carry the score (TabPFN 3.5 0.826 without AST, 0.827 with it; 0.834 without the grade, 0.838 with it). prostate_cancer_detection, retired (the paper's 7 features: Benign against NED 0.92-0.97, the label 0.62-0.70) |
| LEAK-13 (amended 2026-10-26, Andrej) | Precision that differs by class, filled cells with many decimals, a column filled in for one class only | write every row at the measured precision; drop the one-class column | gallstone_disease: GFR, vitamin D, visceral muscle area, CRP and creatinine at their measured precision (with LEAK-39, probe 17 from 0.949 to 0.666); `Hyperlipidemia` dropped (8 with gallstones, none without, though high cholesterol is as common without) |
| LEAK-39 | Part of one class recorded through a second route, found by a format fingerprint | drop the route's rows | gallstone_disease: 77 rows (72 with gallstones, 5 without); before the drop TabPFN 3.5 separates them from those without gallstones at 0.993, the other cases at 0.842, and scores the route's 5 without gallstones 0.77 (0.22 for the others) |
| LEAK-40 | Gaps filled by interpolation down a class-sorted file | keep the fills when a label-free re-imputation inside each fold scores the same or higher | gallstone_disease: 134 fills kept (re-imputed, TabPFN 3.5 0.864; with the fills 0.838) |
| PROV-3 ([provenance.md](provenance.md)) | Generated or manipulated data | retire (`AHDS`, `Data Quality Issue`) | ecommerce_shipping, customer_satisfaction_in_airline, homeq_default_prediction |
| LEAK-22 | The cohort holds rows that cannot have the outcome | follow the paper's cohort | diabetes_130_us: encounters ending in death (1,084) or hospice (461) removed (Strack et al. 2014, Sec. 2.3) |
| LEAK-23 | Only rows with the event, follow-up ending on one date (right truncation) | an outcome within a fixed horizon, over the rows followed that long | cirrhosis_patient_survival_prediction (time to death over deaths only until 2026-10-14; now death or transplant within 5 years) |
| LEAK-24 | A right-censored target in the newest periods (a duration or a final status cut by the download date) | cut where follow-up is complete, or re-source from an archive with settled labels; compare two downloads first | sf_permit_time (permits filed before 2024); consumer_complaints (CFPB FOIA archive) |
| LEAK-25 | "No event" mixed with "not recorded" | a censoring bias: retire unless the recording process can be recovered | ghanas_indigenous_intel (retired, 2026-10-01: the unrecorded rows could not be located, and the task was `Too Small`) |
| LEAK-25 (amended 2026-10-21, Lennart) | "No event" mixed with "not recorded", the unrecorded rows located by a rule that does not read the label | recovered: drop the located rows and ship the rest | caracas_cervical_cancer (shipped 2026-10-15: 108 patients who skipped the contraceptive question dropped, 0 positive results where 11.8 were expected); account_debt_south_africa (eight file runs without debt data, 28,124 rows: none of their 12,167 billed never-payers is a bad debt, against 91.9% elsewhere); fraud_detection_in_electricity_and_gas_consumption_1m (19,133 clients who left before 2013, 21 frauds or 0.11%, and 2,343 who left in 2013-2014, 4.7%, against 7.8% for the clients kept; dropped by last invoice date) |
| LEAK-26 | A target capped at a maximum (a price of 500001, a timeout) | drop the capped rows or document the cap | the house-price and runtime datasets |
| LEAK-27 | A supervised transform fit on the whole labelled set (a discriminant score, a target encoding, a model's prediction) | irreversible: `Data Quality Issue`, `No` | yeast's discriminant-analysis score |
| LEAK-28 | Label-aware features computed over all rows, test folds included | drop them; recommend the technique inside a pipeline, per fold | santander_customer_transaction_prediction `has_one`, `has_zero` (+0.003-0.004 AUC), the #1 solution's features |
| LEAK-29 (CLEAN-7) | Our own cleaning computes a feature value from statistics over all rows | compute it from the history before the oldest test window, or drop it | sf_permit_time `DescriptionIsStandardPhrase` (counted before 2020, the history before the oldest test window); home_credit_default_risk `NEW_INC_BY_ORG` and a mean fill (dropped) (2026-10-19, Lennart) |
| LEAK-30 | Features the source transformed with statistics over all rows, test rows included (z-scores, min-max, quantile bins, ranks, PCA, batch correction, a variance filter): a transductive leak, labels or not | rebuild from unprocessed values when the source has them; otherwise keep with a `Potential leak, kept on purpose:` note; `No` only for a strong suspected leak (Lennart, 2026-10-19). Per-row transforms and fixed published scales are fine | rebuilt: coad_colon_adenocarcinoma (MLOmics z-scores over the 260 patients; retired 2026-10-16 for tcga_coad_molecular_subtype), sarcoma's methylation (next pass). Kept with a note: bioresponse, taiwanese_bankruptcy_prediction, credit_card_customers, cooking_time_1m, delivery_eta_1m, maps_router_eta_1m, lung_cancer_epithelial_genexp (RMA), home_credit_default_risk's building columns |
| LEAK-31 | Supervised feature selection on the full labelled set | measure it; keep with a note when small, remove it when we can | home_credit_default_risk (the kernel's importance-based selection removed, 2026-10-19) |
| LEAK-32 | Masked or anonymised features that may hide such a transform | a known risk of anonymised data, covered by its tag; no action | ieee_fraud_detection, kdd_cup_09_appetency (Lennart, 2026-10-19) |
| LEAK-37, LEAK-10 (precedent, Lennart, 2026-10-21) | A known input that tracks a dropped post-outcome column | kept, with a `Potential leak, kept on purpose:` note in LEAK-38's format (the mechanism, the numbers, why it stays, when to revisit) | digicow_farmer_training_adoption_challenge `topics_list` (the day's topics) predicts the dropped `has_topic_trained_on` at ROC AUC 0.885-0.902 |
| [task_probes.md](task_probes.md), TP-4 | The target is a lookup of the inputs | retire (`Trivial`, often `AHDS`) | video_game_fps_prediction |
| USE-4 ([use_case.md](use_case.md)), TP-6 | Features from a stage after the decision the task models (a biopsy after the examination) | offer the task at the source's earlier stage | eryhemato_squamous_disease: clinical features only (macro AUC 0.999 to 0.98) |

## In Data Foundry

How to run the probes on a definition (`leak_probes.py`, `group_probes.py`) and read their output:
[checks_and_probes.md](../../knowledge-data-foundry/references/checks_and_probes.md). How to record a drop, a kept
suspect or a retirement (`curation_comments` bullets, `CC` lines, `accepted_check_warnings`):
[definitions.md](../../knowledge-data-foundry/references/definitions.md), "Recording decisions", and
[records.md](../../knowledge-data-foundry/references/records.md).
