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
goes even when small. Cases: santander `has_*` (+0.003 AUC). One narrowing (amended 2026-10-26, Lennart, with LEAK-10):
late values that cannot be located row by row stay with a note when the part that can be traced shows no gain
(LEAK-10, second clause below). A column the task uses as a weight or as a rate's denominator never stays with a note
(LEAK-41).

**LEAK-7 (Should).** The smallest fix that keeps a valid signal beats dropping the column. Cases: lag `incentive`
(garments), drop the months where `PageValues` misbehaves (online_shoppers), cut the censored years (sf_permit_time),
re-source settled labels (consumer_complaints), blank the values looked up after the outcome (zillow_prize,
melbourne_housing_market; 2026-10-21).

**LEAK-8 (Should).** Retire rather than invent structure. Cases: guessed groups (maternal_health_risk, hazelnut;
SPLIT-25 in [splits.md](splits.md)), too few independent events (ghana: 626 farmer-days behind 10,928 rows). A
re-split with too few positives (seismic_bumps) is `Too Small`: [task_probes.md](task_probes.md), TP-9.

**LEAK-9 (Should; amended 2026-11-05, Lennart, on medical_facility_operational_data).** Separate data leaks from
evaluation leaks. An evaluation-level leak, where the test set holds complete trajectories that end at the outcome or
a model can read other test rows, is fixed in the scoring (causal per-entity predictions, the task's own utility) or by
a protocol line the benchmark checks, not in the data; document the prediction point. A method that learns from the
test block is called out and not benchmarked (Lennart, 2026-11-05: "we investigate models, and would find out if they
do transductive learning which we can call out and not benchmark"). Cases: sepsis_prediction_1m,
5g_energy_consumption, medical_facility_operational_data, fremtpl2, bank_marketing (protocol lines).

Repair or rebuild damaged data from its origin before keeping it: PROV-13 in [provenance.md](provenance.md).

### Values not known at the prediction point

**LEAK-10 (Must).** A feature holds only what existed at the prediction point (LEAK-1) and never gives the target away.
Out: a column recorded after the outcome; attributes looked up after the outcome (a property's current record for a
past sale), unless the data shows they did not change; a part, a consequence or another encoding of the target; a
feature computed from the window that defines the target, even when its value is known at snapshot time, unless the
data shows the window's values do not move with the outcome given the covariates known at the prediction point; a value
fitted from the same measurement that gives the label; targeting or pointing ids that encode pre-selection or the
observation date; a same-day value that depends on the day's outcome; missingness that encodes the outcome; an aggregate
that may include the row's own outcome. Fix it in the definition the smallest way (LEAK-7), else drop it; when the
features summarise a window that ends at the outcome and no common prediction point can be rebuilt, retire. Test: the
codebook (LEAK-2) and probes 1 to 4. Cases: the Mechanisms table under Cases. Two clauses, amended 2026-10-26 (Lennart),
each a case-by-case judgment of the curator, never a default:
* A window sum stays when the data shows it does not move with the outcome once the covariates known at the
  prediction point are accounted for (account_debt_south_africa's billing totals; "keep them, amend it but make clear
  this needs case by case curator judgement"). A value that encodes the target's own quantity, or that falls in the
  outcome's period, still goes (mutual_funds_india, iranian_churn).
* A value read at a later pull goes where its late cells can be located: they are blanked (zillow_prize,
  melbourne_housing_market, aeolus_1m's weather after departure); where they cannot be located row by row, the values
  go when they may carry a gain (distribution_transformers_at_cauca_department) and stay with a note only when the
  part that can be traced shows none (onlinenewspopularity's keyword and self-reference counts, "go with (a)"). This
  narrows LEAK-6 for that one case; a "removing it changes no score" test alone is still no reason to keep
  (2026-10-21). A column the task uses as a weight or as a rate's denominator is LEAK-41's, never kept with a note.

**LEAK-11 (Should; narrows LEAK-10).** A value measured after the outcome that weakens the signal stays, with a note.
Cases: south_africa_coronary_heart_disease.

**LEAK-41 (Must; narrows LEAK-6, LEAK-10 and LEAK-11; 2026-11-06, Lennart, on fremtpl2 and bemtpl97; amended 2026-11-08,
Lennart, on pricing_game_2016_french_fleet).** A column the task uses as a weight (the metric's row weight, the training
weight, a rate target's denominator) whose value is set or cut after the prediction point is never a model input,
whatever it scores, and neither is a column that encodes it: an earned premium (ship it annualised to the planned term,
or not at all), a length corrected on some rows and realized on others, a sum of a group's exposures, a value whose
precision marks the cut. A part known at the start ships as its own column (LEAK-7, LEAK-37). A column is judged by its
timing, as under LEAK-10: a feature known at the prediction point that predicts the weight through risk selection stays
(USE-6). For each suspect column the definition reports its gain on the declared metric with an L2 fit on the shipped
scale and with the weighted actuarial fit, and decides on the worse; it states the score of 1/weight alone as the
ceiling a leak would reach. No model is trained or scored on rows selected by the realized weight (such as full-year
rows only); a row with no amount at risk may go under USE-7, its claims counted in the notes; a selection the source
made before release, the same in train and test, that cannot be undone, defines the task's population and is sized in
the notes. Test: probe 22. Cases: pricing_game_2016_french_fleet (the organisers left out every period of cover under 30
days before release, in the 2014 file the game priced too: about 15% of the periods and 1.5% of the vehicle-years, the
same on both sides of the split; no other insurance table of PR #47 has such a floor, their released lengths run down to
a day); fremtpl2 (`Exposure` as weight and feature scores 0.24341, as a free feature 0.24343: the weight alone does not
stop the leak); frempl_french_motor_personal_line (1/length alone scores 0.184, the honest model 0.183 under the
weighted Tweedie fit of D9, also on the identity scale and the widened folds of 2026-11-08, 0.176 before D9; the length
to 31 December, the part known at the start, stays its own column, which settled the scale as the identity: 2026-11-08,
Lennart, issue 7 (b)); spanish_motor_insurance_coverage_level_2022_2024 (earned premiums annualised: +0.0096 under a
weighted Tweedie fit, Spearman 0.025 with the exposure; its 49 rows without exposure; the annualised premiums still mark
a cut year by their precision, a part-year's quotient falling back on the tariff's 5-decimal grid: ROC AUC 0.965 for the
located cancellations, rounded to the cent since 2026-11-08 (review issue 7, Lennart): 0.565 after); a simulated partial
correction (renewals reset to a full year, new business left realized) still beats the oracle (0.46490 against 0.46799,
with 30% of claims followed by a cancellation).

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
source's question. ai4d_lab_tanzania_tourism_classification_challenge keeps its 965 exact copies: 17 of 19 inputs are
coarse survey answers with 2 to 10 levels, and 361 repeated profiles are `Alone` travellers, 67.8% of copy groups larger
than their party, so the copies are distinct respondents (Lennart, 2026-11-05; LEAK-19 unchanged).

**LEAK-19 (Should).** Exact copies with the same label: drop them rather than group on the duplicate key. Cases:
wine_quality (1,177 rows); audiology_diagnosis (27 copies of the same findings and diagnosis on different patient ids).
Copies of one compound go (qsar_oral_toxicity's 477 exact copies; qsar_tid_11's 37 salt forms of one ChEMBL parent);
distinct compounds that the descriptors cannot tell apart stay, with the reason in the notes (hiva_agnostic: 23 repeated
vectors, every NSC number distinct; qsar_tid_11: stereoisomers and analogs with their own measured potency) (Lennart,
2026-10-21).

**LEAK-20 (Should).** Feature vectors that occur with both labels: drop every copy, unless they are genuine label
ambiguity the task has. Cases: jm1 (176 rows); consumer_complaints. Exception: mortgage (7 loans, Lennart, 2026-10-22)
keeps the payoff copy where period 51 is doubled, because every such loan ends at period 51: the other copy is damage
to the file (PROV-13), not an ambiguous label.

**LEAK-21 (Should).** Reposts identical except an id or a location: drop them, as the source paper did. Cases: emscad
(Vidros et al. 2017, Sec. 5).

### Selection and censoring

**LEAK-22 (Must).** When the cohort holds rows that cannot have the outcome, follow the paper's cohort. Cases:
diabetes_130_us. A competing event after the prediction point (a death from another cause within the horizon) is no such
row: the row stays with the label it had, No, since the risk a patient faces includes it; dropping it selects the cohort
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
fraud_detection_in_electricity_and_gas_consumption_1m). A mix whose recording follows a reporting unit shipped as a
feature may be kept, case by case, with a note giving the unit's spread and drift and fit approximate, when the task
keeps a measured signal beyond the reporting unit, the period and the place; the source's own 'not recorded' flag is
dropped where it is used (amended 2026-11-02, Andrej, on noaa_storm_events_damage). Cases: ghanas_indigenous_intel
(retired: the unrecorded rows could not be located); the three located and dropped and noaa_storm_events_damage
(Mechanisms table).

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
(2026-10-19), qsar_bioconcentration (the authors' 9 Dragon descriptors dropped: RDKit's descriptors of the same
structures and the measured logKOW carry the signal, and the 9 add 0.002 macro ROC AUC; 2026-10-26), numerai_v5_2_1m
(Numerai's 372 Faith features, chosen with the targets of test eras 1080-1191, dropped: they carried about 28% of the
signal in eras 1080-1131; 2026-10-26).

**LEAK-32 (Should).** Masked or anonymised features that may hide such a transform are a known risk of anonymised
data, covered by its tag and the `Anonymized` marker: no action. Cases: ieee_fraud_detection, kdd_cup_09_appetency
(Lennart, 2026-10-19).

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

**LEAK-38 (Should; narrows LEAK-10; scope amended 2026-10-22, Lennart, on kick and expresso_churn_prediction; amended
2026-11-05, Lennart, on medical_facility_operational_data and tunisian_fraud_detection_challenge).** Fields that may be
post-outcome, anonymised or named, whose timing the source leaves undocumented and no test can establish, in data the
data owner released for its own competition or challenge, stay, with a `Potential leak, kept on purpose:` note giving
the mechanism, the numbers, why they stay and when to revisit, and are named in `fit_reason` as kept (USE-8). A field
whose timing is known to be late (a value looked up at extraction) is LEAK-10's, not this rule's. Why:
removing an unverified signal from host-designed data is arbitrary. The rule covers only fields whose timing cannot be
tested. When a conditional test measures the mechanism (the field's missingness or fill, given the covariates known at
the prediction point, differs by outcome), LEAK-10 applies and the field is dropped, even if the host's test file
carries it the same way: that file is a holdout of the same snapshot, not deployment data. Cases: homesite
(`PropertyField37` x `PersonalField12`, AUC 0.965 to 0.915, kept); kick's `WheelType` was kept here on 2026-10-01 and
dropped under LEAK-10 on 2026-10-22, with `WheelTypeID`, `PRIMEUNIT` and `AUCGUART` (expresso's REGION the same way);
fraud_detection_in_electricity_and_gas_consumption_1m cuts its invoice history at 2013-01-01 on the same kind of
measured step (2026-10-26, Lennart). Named fields kept: african_credit_scoring_challenge `Amount_Funded_By_Lender`,
medical_facility_operational_data's expected-delay table, tunisian_fraud_detection_challenge's refund and
regularisation fields, sendy_logistics_challenge `Distance (KM)` (tested: not measured between the rider's two taps; a
GPS total recorded after delivery not excluded) (2026-11-05, Lennart).

Also not a leak, with their home elsewhere:

* IID over related entities is optimistic but can match how a task is framed: a candidate for a grouped or temporal
  variant, not a fix (SPLIT-31 in [splits.md](splits.md); amazon_employee_access; bank_marketing until it was split by
  time on the file's date order on 2026-11-08, since a client's later record gave an earlier one's label away across
  the random split).
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
| 5 | The share of test rows whose feature vector has an exact copy in train, on every shipped split, without and with the string and datetime columns, split by label (the same label only, another label only, each with one copy or two or more, both labels); for long string columns, the share of test values seen in train (`leak_probes.py`) | a large share, above all with the same label | maternal_health_risk 74%; wine_quality 24%; qsar_bioconcentration 5.4% on the nine descriptors but 0% with the SMILES (isomers the descriptors do not tell apart) |
| 6 | 1-NN label agreement (closest tenth, all, chance); each row's distance to its nearest other row as a label-free score | near-copies agree on the label almost always (reposts, re-scans); the distance alone comes close to the full model (class-conditional generation) | emscad 0.998 among near-copies; homeq distance alone 0.923 (full model 0.975) |
| 7 | Separate two subgroups that share a label (two sources, two clinical groups, donors and patients) | they separate far better than the label does: a source or batch signal | prostate Benign against NED 0.997; hepatitis_c donor against patient 1.000 from four formatting flags |
| 8 | Features in a range where no signal can exist | they predict the label | prostate m/z < 1 Da: AUC 0.81-0.85 |
| 9 | Number formats by class (share of whole numbers, decimals, units) | the formats differ by class | hepatitis_c `ALB`, `BIL` whole numbers in about 100% of patient rows, 10% of donor rows |
| 10 | Row order: the target by position in the raw file, next-row label match (`leak_probes.py --raw`); a time index against the date and against any sort key | the order is temporal or sorted by the target, or the "time" index follows another key | seismic_bumps next-row match 2,583 of 2,583; california time index Spearman 1.000 with the address rank, 0.003 with `Listed On` |
| 11 | Entity overlap: the share of test rows whose entity (respondent, company profile, location, CPU and GPU) is in train; the IID score against the grouped score | a large overlap and a large drop | in_vehicle 0.83 to 0.75; emscad 0.99 to 0.94; video_game_fps: every test CPU and GPU in train |
| 12 | Temporal: rows and minority-class rows per test window | a handful of positives ([task_probes.md](task_probes.md), TP-9), or under about 50 test rows ([splits.md](splits.md), SPLIT-17) | seismic_bumps 0-5 positives per window; ghana rain from 3-6 farmer-days per window; coffee monthly windows of 2-72 rows |
| 13 | The target by period (rows per day, an event rate, the class shares, p50 and p90, a count's zero share) against the band of the earlier periods (`leak_probes.py`), and the same for two downloads of the source | the newest periods lose their slow or late cases: right-censoring | sf_permit_time 2025 p90 rose from 97 to 160 days between the Feb and Oct 2026 downloads; consumer_complaints Jan 2026: 318 rows, 87% one class |
| 14 | A simple formula or lookup for the target; a shallow tree on the label | R^2 near 1; a depth-2 or depth-3 tree close to the full model | video_game_fps: log FPS = game + CPU + GPU, R^2 0.99998; audiology's cochlear diagnoses: two history answers decide 139 of 147 |
| 15 | The generated-data tests of PROV-3 ([provenance.md](provenance.md), "Is the data generated?"; the scope is SEL-16) | see there | ecommerce_shipping, customer_satisfaction_in_airline, homeq_default_prediction |
| 16 | Every block of columns: mean 0 and SD 1, or min 0 and max 1, over the whole table | the source scaled over all rows, test rows included | coad_colon_adenocarcinoma (z-scores over 260 patients); credit_card_customers (clipped at whole-file percentiles) |
| 17 | The number format alone: the decimals each value of a float column is written with, all columns together and the best three alone (`leak_probes.py`) | the format scores far above chance | gallstone_disease 0.949 (best alone: GFR 0.802, two decimals for 80% of those without gallstones and 15% of those with; CRP 0.783; obesity % 0.708, another definition in the second route); 0.666 after LEAK-13 and LEAK-39, nearly all from CRP's exact zeros (0.682), real low values |
| 18 | Cells on a straight line between the cells above and below, per column and class, in the raw file's order (`leak_probes.py`) | many such cells, in one class more than the other: gaps filled by interpolation. Runs of round values are found too; the values tell them apart | gallstone_disease: vitamin D 77 cells, all without gallstones; visceral muscle area 36, all with; GFR 14. Also flagged, and measured: ECF/TBW 8 (each equals the rounded 100 x ECW / TBW) |
| 19 | The rows `_clean` removes, against the kept ones: the class shares, or the target's median and mean shift (`leak_probes.py --raw`) | the removed rows differ by their target: a filter on the outcome | protein_model_quality_rf_pcp: the 4,893 native references removed all score GDT_TS 1 (mean shift +3.0 SD), by design |
| 20 | Each raw column the definition drops, alone against the shipped target on the shipped splits (`leak_probes.py --raw`) | a dropped column scores well alone: say why it is out, and check that no kept column carries it | protein_model_quality_rf_pcp: `TM` R^2 0.87 and `RMSD` 0.84, other quality scores of the same model, rightly dropped |
| 21 | Exact copies in the raw table, before `_clean`: rows equal in every column but the target and the identifiers, by label (`leak_probes.py --raw`) | copies the definition removed, or the source's own repeats it kept (set against probe 5) | ai4d_lab_tanzania_tourism_classification_challenge: 2,018 of 18,506 rows in 718 groups, 370 with more than one label |
| 22 | Weight proxy: the realized weight (a time on risk) fitted on the features; the declared metric with the weight added as a feature against the honest fit; each top feature's gain through the weight; for a Gini, 1/weight alone (`leak_probes.py --weight-proxy`) | a feature whose gain through the weight is above noise: decide by its timing (LEAK-41, LEAK-10) | australian_vehicle_insurance_2004_2005: the rating factors predict the exposure at R^2 0.06 (the study's folds) and 0.074 (the shipped splits); frempl_french_motor_personal_line: 1/length alone 0.184 Gini against the honest model's 0.183 (weighted Tweedie, 2026-11-06; 0.176 under the metric of 2026-11-03), the length as a feature 0.256 |

### The raw state (probes 10, 18 to 21)

These probes read the table `_load_raw` returns, before `_clean`, in the source's row order. Through the lineage of
`process(lineage=True)`, the raw position of each curated row, they also read what `_clean` did: the rows it removed
and the columns it dropped. The trace is a column added to a one-table raw frame, or its index when `_clean` selects
columns. It counts only when the traced run returns the same frame as the plain one. A raw frame of several tables, or
a `_clean` that loses both (a merge that resets the index), gives no lineage, and the output says so. Probe 10 needs
the raw order only; probes 19 and 20 need the lineage.

### Probes 5 and 13

Probe 5 compares exact profiles on every shipped split, each test row against the training side, over the model inputs
without and with the string and datetime columns (the target, the groups and the scoring columns are never inputs),
unrounded, with missing values equal to each other. A test row in several repeats counts each time, so the shares are of
test evaluations, not of entities, and an equal profile does not show that two rows are one entity (LEAK-17 asks for the
id). Copies of the same label are what a lookup memorises; copies of another label are a label ambiguity or too few
inputs (LEAK-20); many repeats of a few coarse features can be natural (LEAK-18). Where a lookup shortcut is suspected,
score a train-only lookup of the profile against the model on the same folds and metric.

Probe 13 (`target_by_period`) puts the rows in periods and sets each statistic of the newest periods against the band
the earlier ones give: the median and the spread of every run of as many consecutive earlier periods, so a drop is
read against the history's own variation. Dates that all fall on 1 January are years, and a rank (an integer time
column with about one row per value, such as an arrival order) is cut into equal-count periods by its order. It
follows the vintage curves of credit risk, the claims development of insurance (incurred but not reported) and the
administrative censoring of survival data: a label known only some time after the prediction point is missing in the
newest periods, so an event rate, an upper quantile or the row count falls at the end and nowhere else. Act on a fall at
the end: cut before the first period out of band, or compare a second download (LEAK-24). A clean result answers
censoring at the release end only; whether a model refit at a window's start would have known each training label is
SPLIT-10's question, and a changing case mix can hide or mimic a drop.

### Probe 22

Probe 22 (`weight_proxy`) asks whether the features carry a realized weight: the time on risk of a rate target, cut
short when a claim causes a cancellation (LEAK-41). The weight is the task's sample weight, or the column
`--weight-column` names. A cross-fitted LightGBM of the weight on the features gives the R^2, the Spearman correlation
and the top features. The leak reference is the declared weighted metric with the weight added as a feature, against
the honest fit: what a perfect proxy would gain. For each top feature, the weight-mediated gain is its gain without the
weight minus its gain when the weight is a feature, with the SD over folds and seeds; a feature that stands in for the
weight loses its gain once the weight is there. For a Gini metric the probe also scores 1/weight alone, the ceiling a
leak would reach. A gain above noise flags a feature; it does not decide. The call is on timing (LEAK-41, LEAK-10): a
feature known at the quote stays, even when it predicts the weight through risk selection (USE-6).

## Cases

Precedents: how a rule was applied. They never change a rule; an exception is listed with the fact that set it apart.
The cases of the rules outside this table are named in the rules.

### Mechanisms and what we did

| Rule | Mechanism | Action | Cases |
|---|---|---|---|
| LEAK-4 | A label we built that a few features spell out (classes merged or dropped by the definition) | use a convention of the field and check it with a shallow tree; run the probes on the source's labels too | audiology_diagnosis: three classes from names replaced by hearing loss with or without a conductive part |
| LEAK-9 | An evaluation-level leak: the test set holds complete trajectories that end at the outcome | fix the scoring (causal per-entity predictions, the task's own utility), not the data; document the prediction point | sepsis_prediction |
| LEAK-9 | Queue fields are history at each row's own arrival; a method that reads the other test rows of a block would see the future | no per-row scorer; a protocol line in the definition that a model may not use other test rows, and the benchmark checks models for it (2026-11-04, Lennart: "we can check if the model cheats"); also sepsis_prediction's and 5g_energy_consumption's protocol lines | medical_facility_operational_data |
| LEAK-10 | A column recorded after the outcome | drop it | heart_failure `time` (follow-up ends at death or censoring); anes post-election items; kickstarter `profile`, `staff_pick`; hotel `BookingChanges`, `AssignedRoomType`, `RequiredCarParkingSpaces` |
| LEAK-10 | Attributes looked up after the outcome (a property's current record for a past sale) | drop them, or keep them where the data shows they did not change | house_sales (the King County lesson); melbourne_housing_market: kept for the sales looked up by the weekly runs within weeks of the sale (`Bedroom2` equals the sheet's `Rooms` in 98.9-100% of the rows of each test window), blanked for the 7,578 sales looked up at once by 10 April 2017, up to 15 months after the sale (LEAK-7 row below; Lennart, 2026-10-21) |
| LEAK-10 (decision, Lennart, 2026-10-21) | Attributes looked up after the outcome that changed for an unknown subset of the positives, with no record that isolates the change | drop them; LEAK-10 as written, no amendment for a gain that may sit on the changed rows | distribution_transformers_at_cauca_department: `power_kva` and `installation_type` from an inventory taken during or after 2020 dropped (none of the 163 replacement-marked first burns of 2020 is rated 5 kVA, against 9% of the other 277; no replacement log; ROC AUC 0.701 to 0.639) |
| LEAK-10 (applied, Lennart, 2026-11-05) | Registry attributes looked up at extraction (constant within each entity), with no mechanism that ties a change of the attribute to the outcome | keep them with a note; drop a status that records a later event of the entity | tunisian_fraud_detection_challenge: the 22 registry fields that stay (tax office, category, legal form, activity and obligation codes) kept, no mechanism ties a registry change to the tax adjustment; `CTR_CESSAT` dropped, as a firm that ceased later carries "ceased" on its earlier years (+0.015 RMSE) |
| LEAK-7, LEAK-10 (Lennart, 2026-10-21) | Values looked up after the outcome, where the rows with a changed or later value can be located (a snapshot date, a mismatch with a record made at the sale) | smallest fix: blank the values looked up after the outcome for those rows; a lookup is not kept merely because removing it changes no score (no LEAK-11 keep) | zillow_prize: the tax delinquency snapshot of about September 2016 blanked for the sales before it (1.5% flagged then, against 3.1-4.7% a month after); melbourne_housing_market: the six scraped attributes blanked for the 7,578 sales before the uploader's batch lookup of 10 April 2017 (RMSE +0.0011 to +0.0016 over 3 seeds) |
| LEAK-10 | A part, a consequence or another encoding of the target: sub-scores that add up to it, weight and height when the target is body mass, earlier grades not yet known at the prediction point when the target is the final grade (amended 2026-10-21, Lennart), a current-status column, award notes inside a description | drop it | the UCI student performance data: G1 and G2 are the period grades of the final grade G3, not yet known at its prediction point |
| LEAK-10 | Earlier grades known at the prediction point, when the target is the final grade, and the actor acts on them | keep them | predict_students_dropout_and_academic_success: the first-year grades (Lennart and Andrej, TabArena v0.1); open_university_learning_analytics_dataset: the assessment marks returned by day 60, 10-30% of the continuous-assessment weight of the final result (Lennart, 2026-10-21) |
| LEAK-10, LEAK-7 | A same-day value that depends on the day's outcome | lag it by one period when the earlier value is known at prediction time (shift within each entity in time order), else drop it | garments `incentive`: within teams its daily changes follow the same day's productivity (Spearman 0.53), not the previous day's (0.07); `incentive_lag_1` per team |
| LEAK-10, LEAK-7 (Lennart, 2026-10-21) | Official statistics joined to a row by the period they describe, published after it | lag each series to its release; when the release dates are unknown, by one period of its own frequency; daily market prices keep the row's date | mortgage (each macro series lagged to its release); sberbank_housing_market_forecasting (its monthly, quarterly and yearly series one period back; RMSE 0.2528 to 0.2520 over its 5 windows) |
| LEAK-10, LEAK-7 | Missingness that encodes the outcome | move the prediction point earlier and drop the columns that do not exist yet | mic: the day-1..3 ICU columns are blank for patients who died earlier; now an admission-time task |
| LEAK-10 | Features summarise a window that ends at the outcome | retire when no common prediction point can be rebuilt | iranian_churn (Keramati & Ardabili 2011, Sec. 4.1; AUC 0.986) |
| LEAK-10 | Snapshot data: a feature computed from the window that defines the target | drop it, even though its value is known at snapshot time | mutual_funds_india `rating` (60% 5-year and 40% 3-year risk-adjusted return; the target is the 3-year return) |
| LEAK-10 (amended 2026-10-26, Lennart) | Snapshot data: a window sum that the data shows does not move with the outcome, given the covariates known at the prediction point | keep it with a note, case by case | account_debt_south_africa `TotalBilling`, `AverageBilling`: within file blocks and property-value bins their residuals separate the classes at ROC AUC 0.509 / 0.501 / 0.496 |
| LEAK-10, LEAK-6 (amended 2026-10-26, Lennart) | Values read at a later pull whose late cells cannot be located row by row | keep them with a note only when the traceable part shows no gain; blank located cells; drop when a gain may sit on them | onlinenewspopularity `kw_*`, `self_reference_*` (crawl-time share counts: only counts unique above 5,000 can be traced; masking the traced young cells changes R^2 by -0.0004) |
| LEAK-10, LEAK-6 (applied, Lennart, 2026-11-05) | Schedule fields that count the final schedule, not the plan at the prediction point (no-shows missing, visits booked later counted), the late cells not locatable row by row | keep them with a note: the whole-field worth is an upper bound on the late part, and it sits within about two seed SDs, so the late part shows no gain | medical_facility_operational_data: nine schedule fields (`AheadCount`, `IsFirst`, `IsLast`, `FutFlowCount2/4`, `NumScheduledNext*`, `SumTimeToCompleteNext*`) match the visits that took place in 99.9-100% of rows; dropping them changes LightGBM's MAE by +0.08 to +0.16 against seed noise of 0.07 (42-53-day windows) and +0.05 against 0.05 (14-day windows; +0.14 with an L2 model). Unlike distribution_transformers_at_cauca_department, where the dropped fields carried ROC AUC 0.701 against 0.639 |
| LEAK-10, LEAK-7, LEAK-41 (Andrej, 2026-11-02; amended 2026-11-06, Lennart; applied 2026-11-08, Lennart) | Time on risk or another amount at risk cut short by the outcome (a policy or period that ends early after a claim or a cancellation) | where the data locates the cut row by row, fix it to the length known at the start (which may stay a feature) or remove it; where it cannot be located and the amount is the denominator of a count or amount target, the target ships as the rate and the recorded amount as its weight scoring column and the task's sample weight, never as a feature (MET-14, MET-15, LEAK-41; the proportional part stays, LEAK-7); where the decision is per unit of an equal-area map, the rate is scored unweighted and no sample weight is declared (MET-15), the notes naming the cut's bias; where it cannot be located and is no denominator, LEAK-10's second clause applies | located: frempl_french_motor_personal_line (25,131 early ends without a continuation given the start-known length, the dates locate them; since 2026-11-06 the length to 31 December stays a feature and the realized length is the rate's weight; the rate on the identity scale since 2026-11-08, so the length stays (CLEAN-16)); pricing_game_2016_french_fleet (every period's length to 31 December, a feature; since 2026-11-06 the realized period is the rate's weight and no window trains on periods admitted by their early end). Denominator: fremtpl2 (`Exposure` as a free feature gains 0.0040, 25% of the skill, and is never better at quotation); bemtpl97 (`expo`: +0.0043, 17%, on the count deviance of the old target with `expo` a free feature; on the declared metric over 9 folds +0.0047 under the weighted Poisson fit and +0.0051 under L2); australian_vehicle_insurance_2004_2005 (`exposure`: the rate's weight since 2026-11-06, a feature on 2026-11-02 because the traced part lowered the row Gini; on claim counts 47 to 82% of a free model's gain over the null is the leak, and on the weighted rate Gini reading it adds +0.09 to +0.12 on 9 of 9 shipped splits); spanish_motor_insurance_coverage_level_2022_2024 (since 2026-11-06 `actual_exposure` is the metric's and the training weight, the earned premiums are annualised and `total_exposure`, corrected on some rows and realized on others, leaves the features under LEAK-41; the annualised premiums still mark the located cancellations, at ROC AUC 0.81 by their values and 0.965 by their decimals (a part-year's quotient falls back on the tariff's 5-decimal grid) until they were rounded to the cent on 2026-11-08 (review issue 7, Lennart: 0.795 by their values and 0.565 by their decimals after), and gain nothing above noise through them on the declared metric, and dropping `total_exposure` costs 0.0176 weighted Gini under a weighted Tweedie fit, the planned time of late starts it also carried) Equal-area map, unweighted (2026-11-08, Lennart): noaa_afsc_bottom_trawl_survey_cpue (the area swept released and left out as a weight; the cut not located row by row: 149 of the 256 tows under half the median duration carry performance code 0); wadden_sea_sibes_macoma_abundance (the subsample fraction, set after the sample is seen, not released). |
| LEAK-10, LEAK-37 (2026-11-06, Lennart) | A span or extent whose start or end the source defines by the outcome | read the source's definition of the start and end; where the outcome alone draws it (damage alone, "the rain that led to damage"), blank or drop it for those types; where it is drawn by the outcome or an outcome-free criterion, keep it with a `Potential leak, kept on purpose:` note giving its worth | noaa_storm_events_damage `duration_hours`: NWSI 10-1605 App. A times the span by the damage alone for Strong Wind and Heavy Rain (Sec. 45, 21: blanked 2026-11-06, Lennart) and starts a Seiche by it (Sec. 41: blanked at the re-review of 2026-11-06), and by the damage or a criterion without it for Thunderstorm Wind, High Wind, Coastal Flood, Lakeshore Flood, Storm Surge/Tide, Dust Storm and Volcanic Ashfall (Sec. 46, 24, 4, 27, 44, 11, 51); within Thunderstorm Wind and High Wind, `magnitude_type` and the measured speed, first-report features, locate the spans only the damage can have timed (a speed estimated from the damage, EG or ES, or Thunderstorm Wind measured under 50 kt: 241,523 rows), blanked like Strong Wind's (2026-11-08, Lennart, review issue 7; the blank cost +0.023 to +0.036 RMSLE on those rows under a larger LightGBM, 12 of 12 seeds); the other 78,843 rows of the seven types are kept with a note; on the declared metric since 2026-11-08 (the mean Tweedie deviance on the dollars, review issue 8) their worth has no consistent sign (-41% to +99% of the deviance on their test rows over 15 fits, median -5%; the measured Thunderstorm Wind spans positive in 35 of 45 fits), where under RMSLE it was -0.02 to +0.12 (median about +0.04; the measured Thunderstorm Wind spans +0.03 to +0.18 in 30 of 30 fits); a Flash Flood is timed by a threat, but one of its four example onsets is water that "comes in contact, flowing into, or causes damage to an above ground residence or public building" (Sec. 14), so the damage can set some starts, and no field records the onset (6.8% of its narratives name water at or damage to a building): kept with a note (2026-11-08, Lennart, review issue 11), worth +31% to +102% of the deviance on its test rows (+9% to +27% on all rows) under a 100-tree Tweedie LightGBM; Flood starts and ends with a threat to life or property (Sec. 15; its definition's damage is the entry criterion, not the clock), Hurricane (Typhoon) and Tropical Storm with the storm's direct effects (Sec. 25, 49): read as outcome-free and kept (the Flood duration worth +0% to +43% of the deviance on its rows); under RMSLE the Flood and Flash Flood durations had no consistent sign (-0.09 to +0.09); the blank of Strong Wind and Heavy Rain cost nothing measurable (the study measured 0.020 to 0.038 on the seven damage-timed types, trained from 2016); a tornado's duration is blanked on a fact of its own, not on this row's reading: the damage survey sets the vortex's ground contact (Sec. 47) and the duration tracks the dropped path length (Spearman 0.83 with `TOR_LENGTH`; `TOR_LENGTH` and `TOR_WIDTH` dropped). bank_marketing `campaign` (the calls of this campaign, counted up to the last one; they end at a subscription or when the bank stops calling): dropped, after the prediction point (before the campaign's first call; the span starts there, as heart_failure_followup_survival's `time`); it was worth 0.006 to 0.008 ROC AUC under the random split and 0.0013 to 0.0016 once the period was known, and on the five time windows +0.0065 to logistic regression (higher in 5 of 5) and -0.014 to LightGBM (2026-11-08, Lennart, issue 2; kept with a note on 2026-11-06) |
| LEAK-10, LEAK-7 | An aggregate that may include the row's own outcome | keep only the period where it behaves like history, and call the evidence circumstantial | online_shoppers `PageValues`: Feb-May every buyer has PV > 0 (AUC 0.974), Jun-Dec 27% of buyers have PV = 0 (0.814); Feb-May dropped |
| LEAK-10, LEAK-7 (applied, Lennart, 2026-11-05) | A rating factor that looks recorded after the row's own outcome in some periods only, the periods located by the record ids, with no source statement of when it was recorded | blank it in the periods where it does not behave like history, keep it where it does | fremtpl2 `BonusMalus`: blanked in `IDpol` blocks 0-4 (597,998 rows, 88%), where it is frozen across the two years and claimants pile on the first malus step 62-63, kept in blocks 5-6, where it follows the previous year's claims (LightGBM Poisson mean deviance 0.2327 to 0.2435, 3 folds; dropping it too costs another 0.0009 in blocks 5-6). bemtpl97 `bm` kept: its source registers the rating factors at the start of the policy period |
| LEAK-10 (exception, Andrej, 2026-11-03) | Aggregates of the same hidden value as measured leaking aggregates, with no sign of a leak in tests without labels | drop them with the leaking ones as one block, and still measure each next to it (the tests without labels, and its worth with labels where the data allows), both in the notes: the judgement rests on the block and the measurements together | loan_default_prediction_imperial_college: f529-f531, f533-f535, f537 dropped with f527/f528; sets it apart from online_shoppers `PageValues` and account_debt_south_africa: aggregates of the same hidden x as two measured leaks (f527, f528), and with anonymised fields a test without labels is indirect |
| LEAK-10 | Fitted from the same measurement that gives the label | drop it for the task we frame | sdss_17 `redshift` (photometric task) |
| LEAK-10 | Targeting or pointing ids (they encode pre-selection or the observation date) | drop them | sdss_17 `plate`, `fiber_ID` (AUC 0.80 alone; they made log loss worse) |
| LEAK-10, LEAK-38 (precedent, Lennart, 2026-10-22) | A named field whose missingness or fill, given the covariates known at the prediction point, differs by outcome (a conditional test), although the host's test file carries it the same way | drop it | expresso_churn_prediction REGION (flag AUC 0.936 among customers active all 62 days); kick `WheelType`/`WheelTypeID` (1.2% predicted missing for bad buys, 24.9% observed) and `PRIMEUNIT`/`AUCGUART` (42.3% predicted filled, 7.8% observed) |
| LEAK-11 | Measured after the outcome, but it weakens the signal | keep it and note it | south_africa_coronary_heart_disease (ESL Sec. 5.2.2, p. 148; dropping `sbp`, `obesity`: AUC 0.774 to 0.778) |
| LEAK-12 (SPLIT-9) | Temporal: training rows whose label is not yet known at the prediction point | filter training rows by an as-of date | hotel_booking_demand: in-window cancellations in train were 100% cancelled (log loss 1.7 to 0.33); a filter on `ReservationStatusDate` keeps the shortcut |
| LEAK-13 | Class-specific recording conventions | harmonise (round every row to the shared precision, drop a column only one class has); first measure how much the fix removes | hepatitis_c_prediction (7 lab columns rounded, `ALP` dropped) |
| LEAK-14 | One class from a separate source or assay | drop that class once the paper confirms it | biogeographical_ancestry_prediction (Turkey, `rs3857620`) |
| LEAK-15 (amended 2026-10-27, Andrej) | A recording artefact through several features that matter for prediction, that cannot be undone | retire; a feature subset does not help when it also separates same-label groups | gallstone_disease, kept: after LEAK-13 and LEAK-39 the suspected artefacts left (AST lower with gallstones, the fatty-liver grades on two scales) do not carry the score (TabPFN 3.5 0.826 without AST, 0.827 with it; 0.834 without the grade, 0.838 with it). prostate_cancer_detection, retired (the paper's 7 features: Benign against NED 0.92-0.97, the label 0.62-0.70) |
| LEAK-13 (amended 2026-10-26, Andrej) | Precision that differs by class, filled cells with many decimals, a column filled in for one class only | write every row at the measured precision; drop the one-class column | gallstone_disease: GFR, vitamin D, visceral muscle area, CRP and creatinine at their measured precision (with LEAK-39, probe 17 from 0.949 to 0.666); `Hyperlipidemia` dropped (8 with gallstones, none without, though high cholesterol is as common without) |
| LEAK-13 (applied, Lennart, 2026-11-05) | A time column coarsened in the split step, after the framework has sorted the rows by its finer values, so the order inside each period still carries them | coarsen it in `_clean`, before the sort; a check that needs the finer value reads a flag computed from it there | chicago_traffic_crashes: the hour floor moved from `_make_splits` to `_clean`; a row's rank in its hour had lowered log loss by 0.00098 (positive on all 9 splits), and the injury share by tenth of the hour went from 9.9-18.6% to a flat 15.1-15.5%; `dataset check` no longer warns `definition_time_changed_in_split` (813,133 rows) |
| LEAK-39 | Part of one class recorded through a second route, found by a format fingerprint | drop the route's rows | gallstone_disease: 77 rows (72 with gallstones, 5 without); before the drop TabPFN 3.5 separates them from those without gallstones at 0.993, the other cases at 0.842, and scores the route's 5 without gallstones 0.77 (0.22 for the others) |
| LEAK-40 | Gaps filled by interpolation down a class-sorted file | keep the fills when a label-free re-imputation inside each fold scores the same or higher | gallstone_disease: 134 fills kept (re-imputed, TabPFN 3.5 0.864; with the fills 0.838) |
| PROV-3 ([provenance.md](provenance.md)) | Generated or manipulated data | retire (`AHDS`, `Data Quality Issue`) | ecommerce_shipping, customer_satisfaction_in_airline, homeq_default_prediction |
| LEAK-22 | The cohort holds rows that cannot have the outcome | follow the paper's cohort | diabetes_130_us: encounters ending in death (1,084) or hospice (461) removed (Strack et al. 2014, Sec. 2.3) |
| LEAK-23 | Only rows with the event, follow-up ending on one date (right truncation) | an outcome within a fixed horizon, over the rows followed that long | cirrhosis_patient_survival_prediction (time to death over deaths only until 2026-10-14; now death or transplant within 5 years) |
| LEAK-24 | A right-censored target in the newest periods (a duration or a final status cut by the download date) | cut where follow-up is complete, or re-source from an archive with settled labels; compare two downloads first | sf_permit_time (permits filed before 2024); consumer_complaints (CFPB FOIA archive) |
| LEAK-25 | "No event" mixed with "not recorded" | a censoring bias: retire unless the recording process can be recovered | ghanas_indigenous_intel (retired, 2026-10-01: the unrecorded rows could not be located, and the task was `Too Small`) |
| LEAK-25 (amended 2026-10-21, Lennart) | "No event" mixed with "not recorded", the unrecorded rows located by a rule that does not read the label | recovered: drop the located rows and ship the rest | caracas_cervical_cancer (shipped 2026-10-15: 108 patients who skipped the contraceptive question dropped, 0 positive results where 11.8 were expected); account_debt_south_africa (eight file runs without debt data, 28,124 rows: none of their 12,167 billed never-payers is a bad debt, against 91.9% elsewhere); fraud_detection_in_electricity_and_gas_consumption_1m (19,133 clients who left before 2013, 21 frauds or 0.11%, and 2,343 who left in 2013-2014, 4.7%, against 7.8% for the clients kept; dropped by last invoice date) |
| LEAK-25 (amended 2026-11-02, Andrej) | "No event" mixed with "not recorded", not located, the recording following a reporting unit shipped as a feature | kept, case by case: the unit's spread and drift in the notes, fit approximate, the source's own "not recorded" flag dropped; only when the task keeps a measured signal beyond the unit, the period and the place | noaa_storm_events_damage (an office enters $0 for 7-91% of its thunderstorm wind entries; given the office, period and place, the other features lower RMSLE by a further 0.17-0.21 per window; the blanks dropped). Differs from us_accidents (`No`, 2026-09-23), whose label was a provider's code |
| LEAK-26 | A target capped at a maximum (a price of 500001, a timeout) | drop the capped rows or document the cap | the house-price and runtime datasets |
| LEAK-27 | A supervised transform fit on the whole labelled set (a discriminant score, a target encoding, a model's prediction) | irreversible: `Data Quality Issue`, `No` | yeast's discriminant-analysis score |
| LEAK-28 | Label-aware features computed over all rows, test folds included | drop them; recommend the technique inside a pipeline, per fold | santander_customer_transaction_prediction `has_one`, `has_zero` (+0.003-0.004 AUC), the #1 solution's features |
| LEAK-29 (CLEAN-7) | Our own cleaning computes a feature value from statistics over all rows | compute it from the history before the oldest test window, or drop it | sf_permit_time `DescriptionIsStandardPhrase` (counted before 2020, the history before the oldest test window); home_credit_default_risk `NEW_INC_BY_ORG` and a mean fill (dropped) (2026-10-19, Lennart) |
| LEAK-30 | Features the source transformed with statistics over all rows, test rows included (z-scores, min-max, quantile bins, ranks, PCA, batch correction, a variance filter): a transductive leak, labels or not | rebuild from unprocessed values when the source has them; otherwise keep with a `Potential leak, kept on purpose:` note; `No` only for a strong suspected leak (Lennart, 2026-10-19). Per-row transforms and fixed published scales are fine | rebuilt: coad_colon_adenocarcinoma (MLOmics z-scores over the 260 patients; retired 2026-10-16 for tcga_coad_molecular_subtype), sarcoma's methylation (next pass). Kept with a note: bioresponse, taiwanese_bankruptcy_prediction, credit_card_customers, cooking_time_1m, delivery_eta_1m, maps_router_eta_1m, lung_cancer_epithelial_genexp (RMA), home_credit_default_risk's building columns |
| LEAK-31 | Supervised feature selection on the full labelled set | measure it; keep with a note when small, remove it when we can | home_credit_default_risk (the kernel's importance-based selection removed, 2026-10-19); qsar_bioconcentration (the authors' 9 Dragon descriptors removed, 2026-10-26); numerai_v5_2_1m (the 372 Faith features removed, 2026-10-26) |
| LEAK-32 | Masked or anonymised features that may hide such a transform | a known risk of anonymised data, covered by its tag and the `Anonymized` marker; no action | ieee_fraud_detection, kdd_cup_09_appetency (Lennart, 2026-10-19) |
| LEAK-37, LEAK-10 (precedent, Lennart, 2026-10-21) | A known input that tracks a dropped post-outcome column | kept, with a `Potential leak, kept on purpose:` note in LEAK-38's format (the mechanism, the numbers, why it stays, when to revisit) | digicow_farmer_training_adoption_challenge `topics_list` (the day's topics) predicts the dropped `has_topic_trained_on` at ROC AUC 0.885-0.902 |
| [task_probes.md](task_probes.md), TP-4 | The target is a lookup of the inputs | retire (`Trivial`, often `AHDS`) | video_game_fps_prediction |
| USE-4 ([use_case.md](use_case.md)), TP-6 | Features from a stage after the decision the task models (a biopsy after the examination) | offer the task at the source's earlier stage | eryhemato_squamous_disease: clinical features only (macro AUC 0.999 to 0.98) |

## In Data Foundry

How to run the probes on a definition (`leak_probes.py`, `group_probes.py`) and read their output:
[checks_and_probes.md](../../knowledge-data-foundry/references/checks_and_probes.md). How to record a drop, a kept
suspect or a retirement (`curation_comments` bullets, `CC` lines, `accepted_check_warnings`):
[definitions.md](../../knowledge-data-foundry/references/definitions.md), "Recording decisions", and
[records.md](../../knowledge-data-foundry/references/records.md).
