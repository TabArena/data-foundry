# Leak checks

What the BeyondArena leak audit (24 Sep to 1 Oct 2026, all 142 shipped datasets) and the reviews since taught us about
finding leaks and deciding what to do with them. Read it whenever the data can be loaded and before calling a column
a leak or a dataset leaky. The per-dataset detail is in each record's dated comments.

A leak is anything other than real signal that lets a model score well: a column that gives the target away or was
recorded after it, a generation or recording artefact that differs by class, copies across the split, a split that
does not match the task, a selection that depends on the outcome, or values computed with the test rows.

## 1. Fix the task before testing columns

* Write down the prediction point and the use case first ([use_case.md](use_case.md)). Every test below asks whether
  a value existed at that point.
* Read the data dictionary or codebook column by column. When one column turns out to be post-outcome, search the
  codebook for the marker that gave it away and drop every column carrying it: anes_voting_2026's flagged `VCF1005`
  led to 56 more items marked "no Post IW" or "no post data".
* Read the source paper before making the call ([provenance.md](provenance.md), "Citing papers"). The paper settled
  or changed many audit calls: which class is a separate assay (biogeographical_ancestry_prediction), that the
  observation window ends at churn (iranian_churn), that the incentive comes from the end-of-day report
  (garments_worker_productivity), what the cohort is (diabetes_130_us), which duplicates the authors removed
  (emscad), that the real groups are collection sites the file does not hold (maternal_health_risk).
* When a definition changes the target (merges or drops classes, bins or thresholds a number, binarizes), run the
  probes against the source's original labels too. A merge can hide a column that spells out the fine label, or the
  fine label can turn out to be read off a few features: audiology_diagnosis's three merged classes hid that its four
  cochlear diagnoses are set by two history answers, age over 60 and noise exposure (139 of 147 cases). Check the
  shipped label the same way: a depth-2 or depth-3 tree on its defining columns shows whether the target is a rule.

## 2. Probes, cheapest first

Score with ROC AUC, log loss or R^2, never accuracy against the majority class, and say how many splits a number comes
from. The numbers compare the shipped data with a suspected fix; they are not leaderboard numbers.

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
| 12 | Temporal: rows and minority-class rows per test window | a handful of positives, or under about 50 test rows | seismic_bumps 0-5 positives per window; ghana rain from 3-6 farmer-days per window; coffee monthly windows of 2-72 rows |
| 13 | The target by period (rows, p50, p90, max), and the same for two downloads of the source | the newest periods lose their slow or late cases: right-censoring | sf_permit_time 2025 p90 rose from 97 to 160 days between the Feb and Oct 2026 downloads; consumer_complaints Jan 2026: 318 rows, 87% one class |
| 14 | A simple formula or lookup for the target; a shallow tree on the label | R^2 near 1; a depth-2 or depth-3 tree close to the full model | video_game_fps: log FPS = game + CPU + GPU, R^2 0.99998; audiology's cochlear diagnoses: two history answers decide 139 of 147 |
| 15 | The generated-data tests ([provenance.md](provenance.md), "Is the data generated?") | see there | ecommerce_shipping, customer_satisfaction_in_airline, homeq_default_prediction |
| 16 | Every block of columns: mean 0 and SD 1, or min 0 and max 1, over the whole table | the source scaled over all rows, test rows included | coad_colon_adenocarcinoma (z-scores over 260 patients); credit_card_customers (clipped at whole-file percentiles) |

Reading the probes:

* A drop-one test misses a column that has a copy. kick loses nothing without `WheelType` because `WheelTypeID` holds
  the same information; drop such columns together.
* The label-free distance score is above 0.5 on ordinary data too (heart_failure 0.64, against 0.73 for the full
  model). Compare it with the full model, not with 0.5.
* The string overlap compares exact values: the same molecule written as two SMILES strings, or the same text with
  other whitespace, does not count. Canonicalise (RDKit for SMILES) before comparing when the overlap matters.
* A pure-value flag on a heavily imbalanced target (base rates of 94-98%: amazon_employee_access, aps_failure) is
  usually an ordinary category effect.
* A near-saturated score alone is not a leak (diamonds R^2 0.993 and splice AUC 0.99+ showed none). Run the probes and
  report what they found.
* A claimed problem gets a second check that tries to refute it with its own code. In the audit all 15 findings of the
  first sweep held, and the second checks corrected details and proposed better fixes.

## 3. Mechanisms and what we did

| Mechanism | Action | Cases |
|---|---|---|
| A column recorded after the outcome | drop it | heart_failure `time` (follow-up ends at death or censoring); anes post-election items; kickstarter `profile`, `staff_pick`; hotel `BookingChanges`, `AssignedRoomType`, `RequiredCarParkingSpaces` |
| Attributes looked up after the outcome (a property's current record for a past sale) | drop them, or keep them where the data shows they did not change | house_sales (the King County lesson); melbourne_housing_market kept: the looked-up `Bedroom2` equals the sheet's `Rooms` in 98-100% of the rows of each test window |
| A part, a consequence or another encoding of the target: sub-scores that add up to it, weight and height when the target is body mass, earlier grades when the target is the final grade, a current-status column, award notes inside a description | drop it | the UCI student performance data: G1 and G2 are the period grades of the final grade G3 |
| A same-day value that depends on the day's outcome | lag it by one period when the earlier value is known at prediction time (shift within each entity in time order), else drop it | garments `incentive`: within teams its daily changes follow the same day's productivity (Spearman 0.53), not the previous day's (0.07); `incentive_lag_1` per team |
| Missingness that encodes the outcome | move the prediction point earlier and drop the columns that do not exist yet | mic: the day-1..3 ICU columns are blank for patients who died earlier; now an admission-time task |
| Features summarise a window that ends at the outcome | retire when no common prediction point can be rebuilt | iranian_churn (Keramati & Ardabili 2011, Sec. 4.1; AUC 0.986) |
| Snapshot data: a feature computed from the window that defines the target | drop it, even though its value is known at snapshot time | mutual_funds_india `rating` (60% 5-year and 40% 3-year risk-adjusted return; the target is the 3-year return) |
| An aggregate that may include the row's own outcome | keep only the period where it behaves like history, and call the evidence circumstantial | online_shoppers `PageValues`: Feb-May every buyer has PV > 0 (AUC 0.974), Jun-Dec 27% of buyers have PV = 0 (0.814); Feb-May dropped |
| Fitted from the same measurement that gives the label | drop it for the task we frame | sdss_17 `redshift` (photometric task) |
| Targeting or pointing ids (they encode pre-selection or the observation date) | drop them | sdss_17 `plate`, `fiber_ID` (AUC 0.80 alone; they made log loss worse) |
| A supervised transform fit on the whole labelled set (a discriminant score, a target encoding, a model's prediction) | irreversible: `Data Quality Issue`, `No` | yeast's discriminant-analysis score |
| Label-aware features computed over all rows, test folds included | drop them; recommend the technique inside a pipeline, per fold | santander_customer_transaction_prediction `has_one`, `has_zero` (+0.003-0.004 AUC), the #1 solution's features |
| Supervised feature selection on the full labelled set | measure it; keep with a note when small, remove it when we can | home_credit_default_risk (the kernel's importance-based selection removed, 2026-10-19) |
| Features the source transformed with statistics over all rows, test rows included (z-scores, min-max, quantile bins, ranks, PCA, batch correction, a variance filter): a transductive leak, labels or not | rebuild from unprocessed values when the source has them; otherwise keep with a `Potential leak, kept on purpose:` note. Only a strong suspected leak makes it a reason for `No` (Lennart, 2026-10-19: "not a strong leak and often happens in reality"). Per-row transforms (a log, a ratio within the row, per-sample TPM or beta values) and fixed published scales are fine | rebuilt: coad_colon_adenocarcinoma (MLOmics z-scores over the 260 patients; retired 2026-10-16 for tcga_coad_molecular_subtype), sarcoma's methylation (next pass). Kept with a note: bioresponse, taiwanese_bankruptcy_prediction, credit_card_customers, cooking_time_1m, delivery_eta_1m, maps_router_eta_1m, lung_cancer_epithelial_genexp (RMA), home_credit_default_risk's building columns |
| Our own cleaning computes a feature value from statistics over all rows | compute it from the history before the oldest test window, or drop it | sf_permit_time `DescriptionIsStandardPhrase` (counted before 2020); home_credit_default_risk `NEW_INC_BY_ORG` and a mean fill (dropped) |
| Masked or anonymised features that may hide such a transform | a known risk of anonymised data, covered by its tag; no action | ieee_fraud_detection, kdd_cup_09_appetency (Lennart, 2026-10-19) |
| Class-specific recording conventions | harmonise (round every row to the shared precision, drop a column only one class has); first measure how much the fix removes | hepatitis_c_prediction (7 lab columns rounded, `ALP` dropped) |
| One class from a separate source or assay | drop that class once the paper confirms it | biogeographical_ancestry_prediction (Turkey, `rs3857620`) |
| Batch noise across the whole feature space, no batch id | retire; a feature subset does not help when it also separates same-label groups | prostate_cancer_detection (the paper's 7 features: Benign against NED 0.92-0.97, the label 0.62-0.70) |
| The cohort holds rows that cannot have the outcome | follow the paper's cohort | diabetes_130_us: encounters ending in death (1,084) or hospice (461) removed (Strack et al. 2014, Sec. 2.3) |
| Only rows with the event, follow-up ending on one date (right truncation) | an outcome within a fixed horizon, over the rows followed that long | cirrhosis_patient_survival_prediction (time to death over deaths only until 2026-10-14; now death or transplant within 5 years) |
| A right-censored target in the newest periods (a duration or a final status cut by the download date) | cut where follow-up is complete, or re-source from an archive with settled labels; compare two downloads first | sf_permit_time (permits filed before 2024); consumer_complaints (CFPB FOIA archive) |
| A target capped at a maximum (a price of 500001, a timeout) | drop the capped rows or document the cap | the house-price and runtime datasets |
| "No event" mixed with "not recorded" | a censoring bias: retire unless the recording process can be recovered | ghanas_indigenous_intel |
| Temporal: training rows whose label is not yet known at the prediction point | filter training rows by an as-of date | hotel_booking_demand: in-window cancellations in train were 100% cancelled (log loss 1.7 to 0.33); a filter on `ReservationStatusDate` keeps the shortcut |
| An evaluation-level leak: the test set holds complete trajectories that end at the outcome | fix the scoring (causal per-entity predictions, the task's own utility), not the data; document the prediction point | sepsis_prediction |
| Measured after the outcome, but it weakens the signal | keep it and note it | south_africa_coronary_heart_disease (ESL Sec. 5.2.2, p. 148; dropping `sbp`, `obesity`: AUC 0.774 to 0.778) |
| The target is a lookup of the inputs | retire (`Trivial`, often `AHDS`) | video_game_fps_prediction |
| A label we built that a few features spell out (classes merged or dropped by the definition) | use a convention of the field and check it with a shallow tree; run the probes on the source's labels too | audiology_diagnosis: three classes from names replaced by hearing loss with or without a conductive part |
| Features from a stage after the decision the task models (a biopsy after the examination) | offer the task at the source's earlier stage | eryhemato_squamous_disease: clinical features only (macro AUC 0.999 to 0.98) |
| Generated or manipulated data | retire (`AHDS`, `Data Quality Issue`) | ecommerce_shipping, customer_satisfaction_in_airline, homeq_default_prediction |

## 4. Not a leak

* An entity's own history under a temporal split is legitimate, also when it carries labels forward: ghana's reporter
  history, ieee_fraud_detection's `uid` (test rows whose uid had fraud in train are 95% fraud; dropping it costs
  0.001-0.007 AUC; kept).
* Text written together with the label is the task when it does not map one to one onto the score
  (coffee_rating_prediction's review text: R^2 0.25 to 0.67; kept).
* A value known at prediction time that rules the outcome out (diabetes "Expired") is a cohort question.
* An input the actor knows at the prediction point, even one the company computed itself (the promised delivery
  date, the forecast being corrected; [use_case.md](use_case.md)).
* IID over related entities (amazon_employee_access, concrete_compressive_strength, bank_marketing) is optimistic but
  can match how a task is framed: candidates for grouped or temporal variants, not fixes.
* A group id column is split metadata, never a feature.
* Choosing which columns or categories to keep by counts over the whole table (the most frequent codes, questions
  asked in one year only) is ordinary cleaning that follows the task's best practice. In a temporal task, say that it
  is a pipeline choice that approximates the task (rosbank1, alfa_battle_2_0_task_2, anes_voting_2026; Lennart,
  2026-10-19).
* Anonymised fields that may be post-outcome, in data a company released for its own competition: keep them, with a
  `Potential leak, kept on purpose:` note giving the mechanism, the numbers, why they stay and when to revisit.
  Removing an unverified signal from host-designed data is arbitrary: homesite (`PropertyField37` x `PersonalField12`,
  AUC 0.965 to 0.915) and kick (`WheelType`, 0.757 to 0.691).

## 5. Copies across the split

Duplicate rows need a decision every time; shipped datasets range from 0% to 98% duplicates.

* Many degrees of freedom and an exact match: a collection artefact, drop it and give the share. Few features and
  plausible repeats: natural, keep them and say so (sepsis_survival_minimal_clinical_records keeps 110,204 rows over
  975 distinct feature rows: three features, real patients, and predicting from them is the source's question).
* Exact copies with the same label: drop them rather than group on the duplicate key (wine_quality: 1,177 rows;
  audiology_diagnosis: 27 copies of the same findings and diagnosis on different patient ids).
* Feature vectors that occur with both labels: drop every copy (jm1: 176 rows; consumer_complaints), unless they are
  genuine label ambiguity the task has.
* Reposts identical except an id or a location: drop them, as the source paper did (emscad, Vidros et al. 2017,
  Sec. 5).
* Repeated entities in different rows (the same patient, house, molecule or object) leak the target across the split
  even when the rows differ: keep one row per entity when the use case is that row, or group ([splits.md](splits.md)).
  Parse ids as strings: sdss_17's float-parsed `obj_ID` merged 21,947 distinct objects (it is now deduplicated on the
  sky position).

## 6. What the first suggestions got wrong

Most first suggestions of the audit were revised, and the reviews since added more. The patterns:

* The smallest fix that keeps a valid signal beats dropping the column: lag `incentive` (garments), drop the months
  where `PageValues` misbehaves (online_shoppers), cut the censored years (sf_permit_time), re-source settled labels
  (consumer_complaints).
* A flagged column is rarely alone: sweep the codebook (anes: 1 to 57 columns) and the use case (kickstarter
  `staff_pick`; sdss `plate` and `fiber_ID` next to `redshift`).
* Retire rather than invent structure: guessed groups (maternal_health_risk, hazelnut), a re-split with too few
  positives (seismic_bumps), too few independent events (ghana: 626 farmer-days behind 10,928 rows).
* Measure before acting. A slight optimism with a known cause can stay with a note; a confirmed leak goes even when
  small (santander `has_*`: +0.003 AUC).
* Say which evidence is proof and which is circumstantial. Two overclaims were corrected in review: reporter history
  is legitimate under a temporal split (ghana), and "PageValues includes the session's own purchase" is likely, not
  shown (online_shoppers).
* Test the human's intuition with data, in both directions: "the rating would be known" was true, but the rating is
  computed from the target window (mutual_funds: dropped); "the features only use the Kaggle train file" missed that
  they use all its rows, our test folds included (santander: leak confirmed); "is this a survival task?" turned out to
  be censoring at download (consumer_complaints).
* Separate data leaks from evaluation leaks: sepsis needs a scorer change, not different data.
* Re-check a comment's claim with data: kick's "grouped" Kaggle split came from a buggy check, and california's
  "temporal" split ran on alphabetical order.
* Report a borderline case as "maybe a leak" for the curator to decide, not as "no leak".
* Never argue "not a leak" because models would predict the same: ask whether the stored values depend on the test
  rows. coad's z-scores over all patients were first called harmless (no labels; tree predictions unchanged), but the
  training rows alone give each test fold's mean of every feature, so each split hands the model the test patients'
  distribution (Lennart, 2026-10-16). The weight of such a leak then decides the action (section 3).
* Do not call a small grouped task unlearnable from one quick model ([splits.md](splits.md), "Grouped tasks").
* Before keeping damaged data, check whether it can be repaired or rebuilt from its origin: SUPPORT2's phase II
  physiology restored from ICPSR 2957, ashrae's readings put in kWh from the data owners' release, coad and
  corporate_credit_rating retired for rebuilds from the GDC and the agencies' disclosures.

## In Data Foundry

How to run the probes on a definition (`leak_probes.py`, `group_probes.py`) and read their output:
[checks_and_probes.md](../../knowledge-data-foundry/references/checks_and_probes.md). How to record a drop, a kept
suspect or a retirement (`curation_comments` bullets, `CC` lines, `accepted_check_warnings`):
[definitions.md](../../knowledge-data-foundry/references/definitions.md), "Recording decisions", and
[records.md](../../knowledge-data-foundry/references/records.md).
