# Leak checks

What the BeyondArena leak audit (24 Sep to 1 Oct 2026: all 142 shipped datasets, 38 needing action) taught us about
finding leaks and deciding what to do with them. Read it whenever the data can be loaded: `/check-candidate` step 4,
`/add-dataset` step 6 (the `dataset check` loop) and `/verify-dataset` items 4, 5, 6, 9 and 13. The curation
guidelines hold the selection criteria; this file holds the tests and the precedents. Per-dataset detail is in the
audit page (https://claude.ai/artifact/ENjKHNwVU7G9xNw1VoaKnn), in the records' dated `CC (2026-09-30 / 2026-10-01,
Lennart)` comments and in `datasets/_dev/tabarena-v0pt2/CHANGELOG.md`.

A leak here is anything other than real signal that lets a model score well: a column that gives the target away or
was recorded after it, a generation or recording artefact that differs by class, copies across the split, a split
that does not match the task, or a selection that depends on the outcome.

## 1. Fix the task before testing columns

* Write down the prediction point and the use case first: at launch (kickstarter), at admission (mic), at quote time
  (homesite), photometric classification (sdss_17), cold start for new respondents (in_vehicle_coupon_recommendation).
  Every column test below asks whether the value existed at that point. Naming "predict at launch" is what surfaced
  kickstarter's `staff_pick` next to the flagged `profile_blurb`.
* Read the data dictionary or codebook column by column. When one column turns out to be post-outcome, search the
  codebook for the marker that gave it away and drop every column carrying it: anes_voting_2026's flagged `VCF1005`
  led to 56 more items marked "no Post IW" or "no post data".
* Read the source paper before making the call (search rule: the curation guidelines, "Cite papers by location").
  The paper settled or changed many audit calls: which class is a separate assay (biogeographical_ancestry_prediction),
  that the observation window ends at churn (iranian_churn), that the incentive comes from the end-of-day report
  (garments_worker_productivity), what the cohort is (diabetes_130_us), which duplicates the authors removed (emscad),
  that the real groups are collection sites the file does not hold (maternal_health_risk).
* When the definition changes the target (merges or drops classes, bins or thresholds a number, binarizes), run the
  probes against the source's original labels as well as the shipped ones. A merge can hide a column that spells out
  the fine label, or the fine label can turn out to be read off a few features (probe 14). audiology_diagnosis's
  three merged classes hid that its four cochlear diagnoses are set by two history answers, age over 60 and noise
  exposure (139 of 147 cases). Check the shipped label the same way: a depth-2 or depth-3 tree on its defining columns
  shows whether the target is a rule (audiology's "conductive part: yes / no" is one depth-2 tree on the tympanogram,
  99% accurate).

## 2. Probes, cheapest first

`.venv/bin/python .claude/skills/verify-dataset/scripts/leak_probes.py <unique_name>` runs probes 2, 3, 5, 6 and 14 (a depth-2 and depth-3
tree on the label) on a v2 folder, and probe 1 for the three strongest single features (untuned LightGBM on the first
three shipped splits). The others take a few lines of pandas. Score with ROC AUC, log loss or
R², never accuracy against the majority class, and say how many splits a number comes from. The numbers compare the
shipped data with a suspected fix; they are not leaderboard-grade.

| # | Probe | Red flag | Audit cases |
|---|---|---|---|
| 1 | All features vs. without the suspect columns, on the shipped splits | the drop costs more than the column could know at prediction time | heart_failure `time`: AUC 0.90 → 0.75; anes 0.930 → 0.855 |
| 2 | Each feature alone | one column comes close to the full model | heart_failure `time` alone 0.84; sdss `redshift`, STAR vs rest 0.998; online_shoppers `PageValues` 0.974 (Feb-May) |
| 3 | Missing-value indicator alone; target rate when missing vs present | missingness predicts the label | mic: rows missing `NA_R_3_n` are 95% deaths (base rate 16%); kick: missing `WheelType` 70.5% bad buys (9.7% otherwise) |
| 4 | Pure values: bundle check `dataset_pure_feature_value` (a value, or present vs missing, with ≥ 100 rows and ≥ 99.5% one class) | a value that occurs with one class only | kickstarter `profile_blurb` (0 of 69,970 failed projects); hotel `RequiredCarParkingSpaces = 1` (0 cancellations); airline `Seat comfort = 0` (99.8% satisfied) |
| 5 | Share of test rows whose feature vector has an exact copy in train | a large share, above all with the same label | maternal_health_risk 74%; wine_quality 24% |
| 6 | 1-NN label agreement (closest tenth vs all vs chance); each row's distance to its nearest other row used as a label-free score | near-copies agree on the label almost always (reposts, re-scans); the distance alone comes close to the full model (class-conditional generation) | emscad 0.998 among near-copies; homeq distance alone 0.923 (full model 0.975) |
| 7 | Separate two subgroups that share a label (two sources, two clinical groups, donors vs patients) | they separate far better than the label does: a source or batch signal | prostate Benign vs NED 0.997; hepatitis_c donor vs patient 1.000 from four formatting flags |
| 8 | Features in a range where no signal can exist | they predict the label | prostate m/z < 1 Da: AUC 0.81-0.85 |
| 9 | Number formats by class (share of whole numbers, decimals, units) | formats differ by class | hepatitis_c `ALB`, `BIL` whole numbers in ~100% of patient rows, ~10% of donor rows |
| 10 | Row order: target by position in the raw file, next-row label match; a time index against the date and against any sort key | the order is temporal or sorted by the target, or the "time" index follows another key | seismic_bumps next-row match 2,583 of 2,583; california time index Spearman 1.000 with the address rank, 0.003 with `Listed On` |
| 11 | Entity overlap: share of test rows whose entity (respondent, company profile, location, CPU and GPU) is in train; IID score vs grouped score. For a v2 grouped task, read the "Group structure" section of its README (test groups per fold, label granularity, clustering against chance) and run `.claude/skills/verify-dataset/scripts/group_probes.py <name>` (the IID vs grouped gap, several models scored per group, a permutation test across groups) | large overlap and a large drop | in_vehicle 0.83 → 0.75; emscad 0.99 → 0.94; video_game_fps: every test CPU and GPU in train |
| 12 | Temporal: rows and minority-class rows per test window | a handful of positives, or under ~50 test rows | seismic_bumps 0-5 positives per window; ghana rain from 3-6 farmer-days per window; coffee monthly windows of 2-72 rows |
| 13 | Target by period (rows, p50, p90, max), and the same for two downloads of the source | the newest periods lose their slow or late cases: right-censoring | sf_permit_time 2025 p90 rose from 97 to 160 days between the Feb and Oct 2026 downloads; consumer_complaints Jan 2026: 318 rows, 87% one class |
| 14 | A simple formula or lookup for the target; a shallow tree on the label | R² near 1; a depth-2 or depth-3 tree close to the full model | video_game_fps: log FPS = game + CPU + GPU, R² 0.99998; audiology's cochlear diagnoses: two history answers decide 139 of 147 |
| 15 | The tests in [`../SKILL.md`](../SKILL.md), "Checking whether the data is generated" | see there | ecommerce_shipping, customer_satisfaction_in_airline, homeq_default_prediction |

Reading the probes:

* A drop-one test misses a column that has a copy. kick loses nothing without `WheelType` because `WheelTypeID` holds
  the same information; drop such columns together.
* The label-free distance score is above 0.5 on ordinary data too (heart_failure 0.64, against 0.73 for the full
  model). Compare it with the full model, not with 0.5.
* A pure-value flag on a heavily imbalanced target (base rates of 94-98%: amazon_employee_access, aps_failure) is
  usually an ordinary category effect.
* A near-saturated score alone is not a leak (diamonds R² 0.993 and splice AUC 0.99+ showed none). Run the probes and
  report what they found.
* A claimed problem gets a second check that tries to refute it with its own code. In the audit all 15 findings of
  the first sweep held, and the second checks corrected details and proposed better fixes.

## 3. Mechanisms and what we did

| Mechanism | Action | Cases |
|---|---|---|
| Column recorded after the outcome | drop it | heart_failure `time` (follow-up ends at death or censoring); anes post-election items; kickstarter `profile`, `staff_pick`; hotel `BookingChanges`, `AssignedRoomType`, `RequiredCarParkingSpaces` |
| Same-day value that depends on the day's outcome | lag it by one period when the earlier value is known at prediction time, else drop it | garments `incentive`: within teams its daily changes follow the same day's productivity (Spearman 0.53), not the previous day's (0.07) |
| Missingness that encodes the outcome | move the prediction point earlier and drop the columns that do not exist yet | mic: day-1..3 ICU columns are blank for patients who died earlier; now an admission-time task |
| Features summarise a window that ends at the outcome | retire when no common prediction point can be rebuilt | iranian_churn (Keramati & Ardabili 2011, Sec. 4.1; AUC 0.986) |
| Snapshot data: a feature computed from the window that defines the target | drop it, even though its value is known at snapshot time | mutual_funds_india `rating` (60% 5-year and 40% 3-year risk-adjusted return; the target is the 3-year return) |
| An aggregate that may include the row's own outcome | keep only the period where it behaves like history, and call the evidence circumstantial | online_shoppers `PageValues`: Feb-May every buyer has PV > 0 (AUC 0.974), Jun-Dec 27% of buyers have PV = 0 (0.814); Feb-May dropped |
| Fitted from the same measurement that gives the label | drop it for the task we frame | sdss_17 `redshift` (photometric task) |
| Targeting or pointing ids (they encode pre-selection or the observation date) | drop them | sdss_17 `plate`, `fiber_ID` (AUC 0.80 alone; they made log loss worse) |
| Label-aware features computed over all rows, test folds included | drop them; recommend the technique inside a pipeline, per fold | santander_customer_transaction_prediction `has_one`, `has_zero` (+0.003-0.004 AUC) |
| Supervised feature selection on the full labelled set | measure it; keep with a note when small | home_credit_default_risk |
| Class-specific recording conventions | harmonise (round every row to the shared precision, drop a column only one class has); first measure how much the fix removes | hepatitis_c_prediction (7 lab columns rounded, `ALP` dropped) |
| One class from a separate source or assay | drop that class once the paper confirms it | biogeographical_ancestry_prediction (Turkey, `rs3857620`) |
| Batch noise across the whole feature space, no batch id | retire; a feature subset does not help when it also separates same-label groups | prostate_cancer_detection (the paper's 7 features: Benign vs NED 0.92-0.97, the label 0.62-0.70) |
| Cohort holds rows that cannot have the outcome | follow the paper's cohort | diabetes_130_us: encounters ending in death (1,084) or hospice (461) removed (Strack et al. 2014, Sec. 2.3) |
| Selection on the outcome that the task states | keep it and record it | cirrhosis_patient_survival_prediction (time to death, deaths only, by design) |
| Right-censored target in the newest periods | cut where follow-up is complete, or re-source from an archive with settled labels; check a newer download first | sf_permit_time (permits filed before 2024); consumer_complaints (CFPB FOIA archive) |
| "No event" mixed with "not recorded" | a censoring bias: retire unless the recording process can be recovered | ghanas_indigenous_intel |
| Temporal: training rows whose label is not yet known at the prediction point | filter training rows by an as-of date in `_make_splits` | hotel_booking_demand: in-window cancellations in train were 100% cancelled (log loss 1.7 → 0.33); a filter on `ReservationStatusDate` keeps the shortcut |
| Evaluation-level leak: the test set holds complete trajectories that end at the outcome | fix the scoring (causal per-entity predictions, the task's own utility), not the data; document the prediction point | sepsis_prediction |
| Measured after the outcome, but it weakens the signal | keep it and note it | south_africa_coronary_heart_disease (ESL Sec. 5.2.2, p. 148; dropping `sbp`, `obesity`: AUC 0.774 → 0.778) |
| Target is a lookup of the inputs | retire (`Trivial`, often `AHDS`) | video_game_fps_prediction |
| A label we built that a few features spell out (classes merged or dropped by the definition) | use a convention of the field and check it with a shallow tree; run the probes on the source's labels too | audiology_diagnosis: three classes from names replaced by hearing loss with or without a conductive part |
| Features from a stage after the decision the task models (a biopsy after the examination) | offer the task at the source's earlier stage | eryhemato_squamous_disease: clinical features only (macro AUC 0.999 → 0.98) |
| Generated or manipulated data | retire (`AHDS`, `Data Quality Issue`) | ecommerce_shipping, customer_satisfaction_in_airline, homeq_default_prediction |

## 4. Not a leak

* An entity's own history under a temporal split is legitimate, also when it carries labels forward: ghana's reporter
  history, ieee_fraud_detection's `uid` (test rows whose uid had fraud in train are 95% fraud; dropping it costs
  0.001-0.007 AUC; kept).
* Text written together with the label is the task when it does not map one to one onto the score
  (coffee_rating_prediction review text: R² 0.25 → 0.67; kept).
* A value known at prediction time that rules the outcome out (diabetes "Expired") is a cohort question.
* IID over related entities (amazon_employee_access, concrete_compressive_strength, bank_marketing) is optimistic but
  matches how those tasks are framed: candidates for grouped or temporal variants, not fixes.
* Group-id columns shipped as features: declare the column in `Grouping(on=...)`. It is metadata, never a feature;
  the TabArena harness has to drop it before fitting (`BENCHMARK_CHANGES_TODO.md`: not every pipeline does yet).
* Anonymised fields that may be post-outcome, in data a company released for its own competition: keep them, with a
  `Potential leak, kept on purpose:` bullet in `curation_comments` giving the mechanism, the numbers, why they are
  kept and when to revisit. Removing an unverified signal from host-designed data is arbitrary. homesite
  (`PropertyField37` × `PersonalField12`, AUC 0.965 → 0.915) and kick (`WheelType`, 0.757 → 0.691).

## 5. Duplicates and groups

* Exact duplicates with the same label: drop them instead of grouping on the duplicate key (wine_quality: 1,177 rows).
* Feature vectors that occur with both labels: drop every copy (jm1: 176 rows; consumer_complaints).
* Reposts identical except an id or a location: drop them, as the source paper did (emscad, Vidros et al. 2017, Sec. 5).
* Group on a true group id, or on one constructed exactly from the data: identical profile text or a poster-specific
  masked contact (emscad, 4,441 groups), consecutive blocks of identical person-level answers in the raw file order
  (in_vehicle_coupon_recommendation, 587 respondents). No similarity-threshold clusters (the first emscad suggestion,
  TF-IDF cosine ≥ 0.95), and no hash of the feature vector standing in for an unknown entity (the first
  maternal_health_risk suggestion).
* When the real groups matter and cannot be recovered, retire the dataset and note in its record that the authors
  could be asked for the group labels: maternal_health_risk (six collection sites, not in the file),
  hazelnut_spread_contaminant_detection (re-scans of about ten set-ups).
* Decide cold start or warm start from the use case before grouping (in_vehicle: cold start, a model used before the
  recommender has data on a person).
* Judge whether a small grouped task is learnable across groups before calling it `Too Small`. Use several model
  families (a regularised logistic regression, a random forest, gradient boosting, kNN) on the shipped grouped splits,
  score per group (average each group's predicted probabilities) against the class-share baseline, and run a
  permutation test that shuffles the labels across groups and repeats the whole grouped CV
  (`.claude/skills/verify-dataset/scripts/group_probes.py` does all of this). A regression task whose models all score below the mean predictor
  on unseen groups has no signal across groups (telemonitoring_parkinsons, 42 subjects: R^2 -0.17 to -0.31 grouped
  against 0.75 IID, 2026-10-01): the use case has to allow known groups (warm start), or the dataset goes. Before
  recasting as warm start, compare a model against the group's known value carried forward (plus the mean drift of
  the training groups): telemonitoring scored 6.33 against 6.48 for that baseline, so it was retired (2026-10-02). One untuned
  gradient-boosting run, as in `leak_probes.py`, is not enough: on unseen groups its probabilities are overconfident,
  so its log loss can be worse than the baseline while the signal is real (mice_protein: LightGBM log loss 2.53
  against a baseline of 2.07, while a random forest reaches 1.12 and a macro AUC of 0.92 per mouse, p < 0.01; it was
  retired anyway, because its classes are the experimental design: real signal does not make a predictive task). With
  few groups, real signal is not enough: count the groups of each class in total and per test fold. parkinsons had real
  signal (AUC 0.86 per subject) and was still retired on 2026-10-05 as `Too Small`: its 32 subjects hold 8 healthy
  people, 2-3 per fold (`../../verify-dataset/references/task_probes.md`, rule 5). musk, with 13 musk and 21 non-musk
  molecules per fold, stays.
* Check the benchmark's own results for a dataset before retiring it for lack of signal: the probes found only a weak
  linear signal in pancreatic_cancer_mouse_detection (AUC 0.63 per mouse, tree models at chance), yet foundation models
  beat AUC 0.5 on all their BeyondArena folds (best 0.66), so it stays (`../../verify-dataset/scripts/tuned_results.py`
  runs this check).
* Check a claim about the source's split against the data: kick's comment called the Kaggle split grouped, yet 78.9%
  of its test rows are at a location also in train.
* Ids parsed as floats collapse: deduplicating sdss_17 on its rounded `obj_ID` removed 21,947 distinct objects; it is
  now deduplicated on the sky position.

## 6. Temporal order

* The raw file order can be the time order without a timestamp (seismic_bumps' mining shifts; california's Kaggle Id
  is the sale order). Keep it, and never shuffle such a file.
* A deduplication or merge can reorder rows (`df.loc[idx]` sorted california by address). Rebuild a row-order time
  index after such steps and check it against the date.
* Windows: the convention in the curation guidelines (as many splits as an IID task of that size, train ≥ 50%), then
  at least ~50 test rows per window (coffee: 13 two-month windows instead of 26 monthly ones) and enough positives
  per window, else `Too Small` (seismic_bumps).

## 7. What the first suggestions got wrong

The audit's first suggestion was revised for most of the 38 cases. The patterns behind the revisions:

* The smallest fix that keeps a valid signal beats dropping the column: lag `incentive` (garments), drop the months
  where `PageValues` misbehaves (online_shoppers), cut the censored years (sf_permit_time), re-source settled labels
  (consumer_complaints).
* A flagged column is rarely alone: sweep the codebook (anes: 1 → 57 columns) and the use case (kickstarter
  `staff_pick`; sdss `plate` and `fiber_ID` next to `redshift`).
* Retire rather than invent structure: guessed groups (maternal_health_risk, hazelnut), a re-split with too few
  positives (seismic_bumps), too few independent events (ghana: 626 farmer-days behind 10,928 rows).
* Measure before acting. A slight optimism with a known cause can stay with a note (home_credit's feature selection
  on the labelled set); a confirmed leak goes even when small (santander `has_*`: +0.003 AUC).
* Say which evidence is proof and which is circumstantial. Two overclaims were corrected in review: reporter history
  is legitimate under a temporal split (ghana), and "PageValues includes the session's own purchase" is likely, not
  shown (online_shoppers).
* Test the human's intuition with data, in both directions: "the rating would be known" was true, but the rating is
  computed from the target window (mutual_funds: dropped); "the features only use the Kaggle train file" missed that
  they use all its rows, our test folds included (santander: leak confirmed); "is this a survival task?" turned out
  to be censoring at download (consumer_complaints).
* Separate data leaks from evaluation leaks: sepsis needs a scorer change, not different data.
* Re-check a comment's claim with data: kick's "grouped" Kaggle split came from a buggy check, and california's
  "temporal" split ran on alphabetical order.
* Report a borderline case as "maybe leak" for the human to decide, not as "no leak".
* Do not call a small grouped task unlearnable from one quick model. mice_protein, parkinsons and pancreatic were first
  suggested as having no signal across groups from one untuned LightGBM run; several models and a permutation test
  showed real signal in the first two, and the BeyondArena results kept the third (2026-10-01). Real signal did not
  save parkinsons in the end: it was retired on 2026-10-05 for its size (8 healthy people), not its signal.

## 8. Recording

* `curation_comments`: one bullet per drop, filter or kept suspect, with the mechanism, the decisive numbers (with and
  without the column, its single-feature score, counts) and the location in the paper for any claim taken from it.
* A suspect kept on purpose: `Potential leak, kept on purpose:` with the mechanism, the numbers, why it is kept and
  when to revisit.
* The record: a dated `CC (YYYY-MM-DD, Name):` comment with the same substance, and a revisit condition when the call
  is provisional (ghana "retired for now", sf_permit_time "re-download in 1-2 years", homesite "if the fields are
  documented"). Planned outreach to authors goes into the record, not into `TODO.md`.
* A retirement: `No (Retired)` with its markers (`Data Quality Issue`, `AHDS`, `Too Small`, `Trivial`, ...), the
  folder removed from the v0.2 working copy and a `CHANGELOG.md` entry.
* An accepted bundle-check warning keeps its reason in `accepted_check_warnings` (emscad accepts
  `dataset_pure_feature_value` for large legitimate clients).
