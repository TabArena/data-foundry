# Evidence

Procedure: applies at every rank. How much a piece of evidence counts, how to settle a disputed fact, what a probe
flag can mean, and what is never evidence. The ranking of the rules, their strengths, exceptions and amendments:
[principles.md](principles.md).

The rules of the seven parts say what a fact means for a dataset; the rules here say when a fact is established. They
sit outside the ranking because every part depends on them. Within this file a rule wins over the rules below it of
the same strength. The checklist every workflow ends with is [verification.md](verification.md), and how evidence is
written for the curator is [writing.md](writing.md).

## Rules

**EV-1 (Must).** Facts before rules: settle a disputed fact with the decisive experiment before arguing about rules or
asking the curator. The comparison that settles a question (a naive forecast against a model, the score with and
without a column, a converted scale against the published one) answers it better than a question does. A rule applied
to a wrong fact gives a wrong verdict, and most first suggestions of the leak audit were revised. Measure before
acting, and test a claim the same way wherever it comes from (a record comment, a page, a prescribed split, a
curator's intuition), in both directions. How to design the test: "The decisive experiment" below. Cases: colleges,
mutual_funds_india, santander_customer_transaction_prediction, consumer_complaints, aeolus.

**EV-2 (Must).** Evidence ranks. When two pieces of evidence disagree, the higher one wins:

1. a measurement on the data: our own splits, probes, counts and comparisons, on the data we ship or the source's own
   files;
2. the source's primary documents: the paper's text, the codebook or data dictionary, the data owners' documentation;
3. the source's page: a dataset or competition page, a data card;
4. third-party pages: re-uploads and mirrors (Kaggle, OpenML, Hugging Face), other collections' descriptions and
   versions of the data;
5. inference: a reading or paraphrase of a source, a recollection of the field, a plausible guess.

A later stage's measured fact supersedes an earlier stage's reading: a measurement made while adding a dataset
supersedes a screening reading, and a screening verdict is provisional until the dataset is added and probed. A page
is a claim about the data, and copies carry their own errors (PROV-15, PROV-18, [provenance.md](provenance.md)), so each
is checked against the evidence above it. Read the record's comments first, since they usually hold the decisive fact
([selection.md](selection.md)), and re-check a claim in them with data. How to apply the ranks:

* A source counts in its own words. A paper is a primary document only as text you read, cited by section with the
  load-bearing sentence quoted; the title, the abstract or a recollection of the field is inference
  (PROV-16, [provenance.md](provenance.md)). Write "for example" for a use case the source does not state
  (USE-1, [use_case.md](use_case.md)), "not stated" rather than a guess ([writing.md](writing.md)), and "unverified" for
  a claim from a paper you could not read.
* A source's documents rank high on what the data is (how it was collected, the cohort, the stages, how the label was
  built). A choice the source made is a claim to check against the task design: the split a paper or a dataset page
  prescribes (SPLIT-5, [splits.md](splits.md)), a headline score.
* Discussion threads and public notebooks rank as third-party pages, but they are where a page's problems surface:
  read them, then confirm what they show on the data or in the source (PROV-18, [provenance.md](provenance.md)).
* A measurement counts for the question it tests. A single-column score does not test when a column was recorded: a
  column recorded after the prediction point goes whatever it scores alone, and one known at the prediction point
  stays whatever it scores ([writing.md](writing.md)). For a duplicate, a structural diff is weak evidence and a shared
  source strong (PROV-4, [provenance.md](provenance.md)); a measured overlap of ids and values then confirms it.
* A measurement on a third-party copy speaks for that copy, not for the source (hr_analytics).

Cases: kick, california_house_prices_2020, appliances_energy_prediction, intrusion_detection, kddcup99,
pkdd-15-taxi-trip-time-prediction-ii, hr_analytics.

**EV-3 (Must).** A probe flag or hit is a question, not a verdict. Read it by the readings table ("Reading a probe"
below): test the readings in the order given, the highest-ranked first, and the first reading that holds decides which
rule applies. A reading ranks as [principles.md](principles.md) ranks problems: validity readings first (a leak, a
broken target or split, generated data), then value readings (trivial, too small), and the benign reading last. The
probes fit untuned models on a few splits and flag patterns that real data shows too; their numbers compare the
shipped data with a suspected fix and are not leaderboard numbers. So a task-probe flag is checked against the
benchmark's tuned methods before anyone acts on it (TP-1); a hidden-group hit is decided by the context and the use
case, never by the gap alone (SPLIT-30, [splits.md](splits.md); Lennart, 2026-10-06); a generated-data mark needs
what the source says and, where possible, the generator written down (PROV-3, [provenance.md](provenance.md)); without
either, the marks are judged case by case: calibrated marks from at least two PROV-3 tests, or marks linked to the
label, can each be strong enough, counted on the columns we ship, and marks on the published file count when they
extend to the shipped version (amended 2026-10-21, Lennart: "either might be strong enough; on the columns we ship,
and if the marks on the published file leak/extend to the shipped version (which is again case-by-case)"); and a
near-saturated score alone is not a leak: run the probes and report what they found. No flag is no pass either: the
probes cover the mechanical part, and the prediction point and the source's entities need judgment
([verification.md](verification.md), the two halves). Cases: forest_fires, amazon_employee_access, superconductivity,
diamonds, splice, kickstarter, airfoil_self_noise, concrete_compressive_strength.

**EV-4 (Must).** Never evidence. None of these decides a verdict, a marker, a fix or a probe, and none of them is an
issue for the curator ([writing.md](writing.md)):

* A licence or redistribution terms (Lennart, 2026-09-23). A non-commercial clause, a request-only download or a
  no-redistribution rule is a one-line note in the record (what the terms are and where they are stated), never the
  reason for a `No`, a `TBD -> 2nd Tier` or a marker. Triage the data on its merits: JRC's terms forbid
  redistributing `lucas_topsoil`, and its record is still triaged on what the survey measures. Terms that bear on
  whether a collection may ship the data are items of the release checklist, checked before a release and not in
  curation: the Zindi Competition Rules' "private property of the client" (african_credit_scoring_challenge, digicow
  and the other Zindi datasets) and the Credit Risk Analytics terms of no commercial use and no redistribution
  (corporate_credit_rating_cat, mortgage, lgd) (Lennart, 2026-10-21).
* Scores other benchmarks published (TALENT, leaderboards): their random splits are wrong for most of our tasks
  (Lennart, 2026-10-15). Evidence comes from our own splits, probes and the sources; the benchmark's own tuned results
  on the shipped splits are ours (TP-1). The source's own competition is no other benchmark: the model families at the
  top of its leaderboard are a modality signal, and its top solutions' preprocessing is adopted (CLEAN-1, CLEAN-20,
  [cleaning_features.md](cleaning_features.md)).
* Whether a dataset is in some model's pretraining data (Lennart, 2026-10-12).
* Another collection's version of the data (TabSTAR's columns or labels): no reference for ours; name it only for
  provenance or a duplicate (Lennart, 2026-10-15).
* A model's input limit, feature cap or runtime, in a curation decision or in a probe (Lennart, 2026-10-15:
  coad_colon_adenocarcinoma ships 36,355 features; its report had weighed one model's 50,000-feature cap). Width itself
  is no reason to drop columns (CLEAN-22, [cleaning_features.md](cleaning_features.md)).

None of them is a fact about the task we ship. A problem of someone else's copy is noted in the record of the dataset
it concerns and raised only when it changes one of our decisions (PROV-15, [provenance.md](provenance.md)).

**EV-5 (Must).** Score with ROC AUC, log loss or R², never accuracy against the majority class. Under class imbalance
accuracy is no evidence in either direction (Lennart, 2026-09-23): judge learnability with ROC AUC or log loss against
the class prior, and when the data loads, fit a quick gradient-boosting model on the features known at prediction
time. On an imbalanced target, always predicting the majority class already scores a high accuracy. Cases:
us_accidents.

**EV-6 (Should).** Proof against circumstantial evidence. A claim is proven by a test that could have refuted it, so a
claimed problem gets a second check that tries to refute it with its own code. Say which evidence is proof and which is
circumstantial, and report a borderline case as "maybe a ..." ("maybe a leak", not "no leak") with the test that would
settle it, for the curator to decide. In the leak audit all 15 findings of the first sweep held, and the second checks
corrected details and proposed better fixes; two overclaims were corrected in review. A test that cannot come out the
other way proves nothing: "models would predict the same" does not test whether the stored values depend on the test
rows (LEAK-5, [leak_checks.md](leak_checks.md)), while a generator written down settles that a table is generated
(PROV-3, [provenance.md](provenance.md)). Cases: ghanas_indigenous_intel, online_shoppers, coad_colon_adenocarcinoma,
fitness_club.

**EV-7 (Must).** Never claim a check you did not run. Each check is a pass, a concern or cannot-verify, with one line
of evidence: a quote from the source, a line of the definition, a number from a check or a probe. "Looks fine" is no
evidence, and cannot-verify is never upgraded to pass: it goes to the curator as what a human must still check
([verification.md](verification.md)). If a source could not be reached, say so; name a step you skipped and why; mark
a claim from a paper you could not read as unverified rather than paraphrasing the abstract as if it were the text
(PROV-17, [provenance.md](provenance.md)). The automated checks are run, and their findings are not re-derived by eye.

**EV-8 (Should).** Say where a number comes from: how many splits, which models (an untuned probe or the tuned
methods), and which version of the data (another split, other columns, other scoring, a probe under older rules). A
number from another version may not hold for the shipped one, and probe sweeps under older rules are not comparable
([task_probes.md](task_probes.md), the flags). Cases: breast_cancer_prediction, mortgage.

**EV-9 (Should).** Calibrate a statistic before concluding from it: read it against the same statistic measured the
same way on a reference (a real dataset of the same kind, the full model, the dummy on the same splits), not against
its value without signal. A selection on the label also changes correlations, and a probe statistic can sit far from
that value on ordinary data. The thresholds of the hidden-group and generated-data probes were calibrated this way
([task_probes.md](task_probes.md)). Cases: heart_failure, santander_customer_transaction_prediction,
homesite_quote_conversion.

## Patterns

Quick ways to apply the rules; a pattern never overrides a rule, and the dataset at hand wins over the pattern.

* Cheapest first. The leak probes are ordered cheapest first ([leak_checks.md](leak_checks.md)), and so are the tests
  for generated data (PROV-3, [provenance.md](provenance.md)); stop at the first test that settles the decision (EV-1).
* Measure the fix as well as the problem: compare the shipped data with the suspected fix, and measure how much a fix
  removes before applying it (hepatitis_c_prediction's rounding) (EV-1).
* Argue from what the data is (the feature composition, the true source, the size, the actual target), not from a
  dataset's fame or from how someone might solve the broader problem today ([principles.md](principles.md), arguing a
  call; SEL-15 in [selection.md](selection.md)) (EV-2).
* Before triaging a dataset from Kaggle or a similar platform, skim its discussion threads and public notebooks by
  votes for leak threads, "hack" baselines and the uploader's answers, and confirm what they show
  (PROV-18, [provenance.md](provenance.md)) (EV-2).
* Bound what a marker can explain before calling it the signal (pancreatic_cancer_mouse_detection: the `t` file suffix
  separates some control spectra at AUC 0.67, but its class shares explain at most AUC 0.56 of a label that reaches
  0.63-0.66) (EV-6).
* Run the probes again after a fix: a flag that stays has another reading (mortgage: `one_feature` before the macro-lag
  fix, `drift_baseline` after) (EV-3).

## Reading a probe

How to read a probe's flags (EV-3). Each row is one flag of a probe, or one red flag of the leak probes (numbered as in
[leak_checks.md](leak_checks.md)). The readings are ranked validity first, then value, the benign reading last; test
them in that order, and the first that holds decides which rule applies. The Rule column names the rule of each reading
in the same order, by ID with its strength, and its action. What each probe computes and its thresholds:
[task_probes.md](task_probes.md), the flags, and the docstrings in
[scripts/curation_probes/](../scripts/curation_probes/).

Before the readings, check the flag itself. A task-probe flag is checked against the tuned methods (TP-1). A flag the
probe made is no reading of the data: the probe left the text out (mercari_price_suggestion: R² 0.06 without, 0.67
with), sampled the rows (mortgage: the class shares matched untuned models on 50k sampled rows; on the full training
side LightGBM beats them in 3 of 3 quarters; since 2026-10-21 the probe keeps a temporal task's newest 200,000 train
rows, and mortgage raises no flag), ran a model that diverged (force_2020: untuned LightGBM at log loss 2.77,
while random forest reached 0.744 against the class shares' 1.284), picked its single feature by chance
(clock_protein_toxicity: a selection effect), or ran under older rules (EV-8).

### Task probes (`task_probes.py`)

| Flag | Readings, highest rank first | How to tell them apart | Rule |
|---|---|---|---|
| `one_feature`: the best single feature, chosen on each split's training side, reaches 95% of the best family's skill and leaves at most 1.25 times its remaining error | 1. a column recorded after the outcome, or built from the outcome's window or measurement (heart_failure `time`; sdss_17 `redshift`; online_shoppers `PageValues`; mutual_funds_india `rating`) · 2. a label derived from the feature: a published rule, a definition, another encoding of the target · 3. a shortcut with no domain reason: generated or edited data · 4. a trivial task (fitness_club) · 5. the natural core of the task: a listed price for a sale price, age for survival (california_house_prices_2020, sepsis_survival_minimal_clinical_records, expresso_churn_prediction_1m) | the prediction point and the codebook: when the column is recorded, whether the label is computed from it; the generated-data tests when no domain reason exists; then the raw feature, chosen on each split's training side, against the tuned methods fold by fold (`tuned_results.py --feature auto`); and the raw feature without a model (`Listed Price`: R² 0.64 until the 39 listings at $0 were set aside, then 0.89-0.91) | 1. LEAK-10 (Must; a column recorded after the outcome, fitted from the same measurement, an aggregate that may include the row's own outcome, snapshot data): drop, or keep only the period where it behaves like history (LEAK-7) · 2. SEL-5 (Must): drop the rule's inputs, or `Trivial` when they are the whole task; LEAK-10 (Must; a part or another encoding of the target): drop · 3. PROV-3 (Must; scope SEL-16): `AHDS`, `No` · 4. TP-4 (Must): `Trivial` when the raw feature matches or beats the methods fold by fold · 5. none: keep, a note (TP-4) |
| `solved`: ROC AUC, macro ROC AUC or R² of at least 0.995 | 1. a leak · 2. features from a stage after the decision the task models (eryhemato_squamous_disease's biopsy) · 3. a trivial task: a lookup, a formula or a simple rule reaches the score (video_game_fps_prediction) | the leak probes and a shallow tree; a formula or lookup for the target (leak probe 14); a stage the source describes, and the task tested there (eryhemato: "first evaluated clinically with 12 features. Afterwards, skin samples were taken"; macro AUC 0.999 after the biopsy, 0.98 before). A near-saturated score alone is not a leak (diamonds R² 0.993, splice AUC 0.99+) | 1. the LEAK rule of the mechanism found (LEAK-10 to LEAK-32), with the smallest fix (LEAK-7, Should): drop, lag or filter · 2. USE-4 (Must; a stage after the decision): offer the task at the earlier stage; TP-6 (Must) · 3. TP-4 (Must; the paper's criterion 4C): `Trivial`, often `AHDS` (PROV-3, test 7; leak_checks.md Mechanisms, the target is a lookup of the inputs) |
| `no_signal`: the best family's mean skill is not above twice its standard error (or 0.02) | 1. a bug in the target or the cleaning · 2. a split that removes the signal the use case has: no signal across unseen groups (telemonitoring_parkinsons) · 3. untuned models that overfit noise, or a small real signal (forest_fires, clock_protein_toxicity, asp_potassco_classification) | the target's distribution against the source; the tuned results: do the strongest regularised methods beat the dummy fold by fold; for a grouped task, several families scored per group with a permutation test (`group_probes.py`); for a zero-inflated target, the oracle bound and a hurdle model (forest_fires: 48% zeros, neither stage learnable) | 1. PROV-13 (Must; repair or rebuild from the origin), CLEAN-1 (Should): fix · 2. SPLIT-28 (Must): the use case has to allow known groups, or the dataset goes · 3. TP-2 (Should): keep |
| `no_spread`: the best and worst family differ by less than twice the standard error of their per-split difference (or 0.01) | 1. a target the definition built (audiology_diagnosis's own 3-class merge) · 2. a handful of units of a class (parkinsons_biomedical_voice_measurements) · 3. tuned methods spread · 4. strong methods converge on a large, low-noise dataset (amex_non_iid_1m), or the noise of a small task or of few windows (heart_disease_cleveland, retired as part of heart_disease; rosbank1, electric_motor_temperature_prediction) | the tuned results: ties with the best (paired per fold, a lower bound) and Kendall's W; the units of each class per test fold; the gap against the paired standard error the windows allow | 1. TP-7 (Must): a convention of the field, tested · 2. TP-5 (Must): `Too Small` · 3. TP-3 (Must): keep · 4. TP-2 (Should), TP-3 (Must): keep |
| `drift_baseline` (temporal tasks): a constant from the newest train rows has a loss within 2% of the best family's (log loss, or squared error) | 1. a target censored by the download date, or late labels trained on without a gap · 2. drift in the level that the task carries | the target by period (rows, p50, p90, max) and in two downloads (leak probe 13; sf_permit_time: 2025 p90 from 97 to 160 days between the Feb and Oct 2026 downloads); the label's delay; the windows' class shares or means over time; the full training side (mortgage); the task's metric: a moving level shows in log loss, which ROC AUC ignores (african_credit_scoring_challenge: a default rate from 1-1.4% to 6.4-9.4%) | 1. LEAK-24 (Must; a right-censored target): cut where follow-up is complete, or re-source settled labels; SPLIT-10 (Should; labels that arrive late): a gap · 2. TP-1 to TP-3: keep, re-check with tuned results (mortgage, african_credit_scoring_challenge) |
| `unstable`: the best family beats the dummy on fewer than 80% of the splits, or the standard error of its mean skill is above 0.05 (temporal tasks: the standard error counts only when it loses to the dummy on a window, since 2026-10-15) | 1. a handful of units per test fold · 2. window-to-window variation of a small temporal task, or one atypical window · 3. a small real signal | the units per test fold; the share of splits on which the models beat the dummy and the standard error of the mean skill, not the spread of one split's score (coffee_rating_prediction: 13 of 13 windows, standard error 0.03); whether tuned methods are robust over all splits | 1. TP-5, TP-8 (Must; TP-9 for the windows of a temporal task): `Too Small` (parkinsons_biomedical_voice_measurements: 8 healthy people, 2-3 per fold) · 2. TP-2 (Should): keep (consumer_complaints_1m, apistox; bias_correction_r_bias_correction_r_2: below the mean in the oldest window only) · 3. TP-2 (Should): keep (pancreatic_cancer_mouse_detection, garments_worker_productivity) |
| `few_minority`: a probed test fold holds fewer than 5 rows (groups, for a task scored per group) of a class; also leak probe 12, the rows and minority-class rows per test window | 1. too few units to score: a handful per test fold, carrying a large share of the score · 2. classes the definition built, which a convention of the field merges · 3. a class a grouped split leaves out of a fold because few groups hold it · 4. a rare class of the source's labels carrying about its share of the loss | the units of each named class in total and per test fold; the share of the log loss its rows carry; whether the classes are the source's or ours; how many groups hold the class | 1. TP-5, TP-8, TP-9 (Must): wider windows (SPLIT-17), else `Too Small` (alvin_smart_money_management_classification_challenge: 51-54% of a window's log loss; seismic_bumps: 0-5 positives per window) · 2. TP-7 (Must) · 3. none (TP-8: not a small class): accept `splits_test_class_missing` (force_2020) · 4. TP-8 (Must): keep (mic: 0.7% of the test rows, 4.8% of the log loss) |

### Leak probes (`leak_probes.py`; numbers as in leak_checks.md)

| Flag | Readings, highest rank first | How to tell them apart | Rule |
|---|---|---|---|
| One feature alone close to the full model, or a large drop without it (probes 1, 2) | as `one_feature` | as `one_feature`; a drop-one test misses a column that has a copy (kick: `WheelType` and `WheelTypeID`), so drop such columns together | as `one_feature` |
| A missing-value indicator predicts the label (probe 3) | 1. missingness caused by the outcome (mic: rows missing `NA_R_3_n` are 95% deaths, base rate 16%) · 2. an anonymised field in data a company released for its own competition (kick: missing `WheelType` 70.5% bad buys, 9.7% otherwise) · 3. a real process known at prediction time | when the field gets filled (the codebook, the collection process); the target rate when missing and when present | 1. LEAK-10 (Must; missingness that encodes the outcome): move the prediction point earlier and drop the columns that do not exist yet · 2. LEAK-38 (Should; not a leak: anonymised fields): keep with a `Potential leak, kept on purpose:` note · 3. none |
| A pure value: at least 100 rows and at least 99.5% one class (probe 4) | 1. a value recorded after the outcome (hotel_booking_demand `RequiredCarParkingSpaces = 1`; kickstarter `profile_blurb`) · 2. an ordinary category effect on a heavily imbalanced target (base rates of 94-98%: amazon_employee_access, aps_failure) | the column's source and recording time; for each suspicious value, label rates within that value versus all other values, their difference or ratio, and binary-membership mutual information, with supporting counts and training-only lookup behavior; substantial supported information gain is a potential leakage/memorization signal, not evidence against leakage; high cardinality alone does not explain it away, and mixed labels or partial coverage do not clear it; absolute majority purity alone is weak evidence under extreme imbalance | 1. LEAK-10 (Must; a column recorded after the outcome): drop · 2. none: accept with the reason |
| Exact copies across the split (probe 5) | 1. a collection artefact or copies of one entity: many degrees of freedom and an exact match, the same findings on other ids (audiology_diagnosis: 27 copies), reposts identical except an id (emscad) · 2. feature vectors that occur with both labels (jm1: 176 rows) · 3. natural repeats: few features, plausible (sepsis_survival_minimal_clinical_records: 110,204 rows over 975 distinct) | the number of features; the label of each copy; entity ids parsed as strings; the share with and without the string and datetime columns (qsar_bioconcentration: 5.4% on nine descriptors, 0% with the SMILES); strings canonicalised before comparing (RDKit for SMILES) | 1. LEAK-16 (Must), LEAK-18, LEAK-19, LEAK-21 (Should): drop them and give the share, or group when the rows are one entity (LEAK-17, Must; SPLIT-24) · 2. LEAK-20 (Should): drop every copy, unless it is a label ambiguity the task has · 3. none (LEAK-18): keep and say so |
| Near copies agree on the label, or the label-free distance score comes close to the full model (probe 6) | 1. reposts or re-scans across the split (emscad: 0.998 agreement among near copies) · 2. class-conditional generation (homeq_default_prediction: distance alone 0.923, full model 0.975) · 3. a panel: the nearest neighbour is the same entity in another period, with a sticky status and a large majority class, so the agreement measures the repetition, not a leak (mortgage, loan-quarters: 0.957 against chance 0.873, distance AUC 0.525; 2026-10-21) · 4. ordinary data | the distance score against the full model, not against 0.5 (heart_failure: 0.64 against 0.73; EV-9); what the near copies share in the source; on a panel, whether the neighbour is the same entity, and the agreement against the class shares, not against 1 | 1. LEAK-21 (Should): drop the reposts, as the source paper did, or group on the entity (LEAK-17, Must; SPLIT-24) · 2. PROV-3 (Must; scope SEL-16): `AHDS`, `No` · 3. none when the use case scores known entities (SPLIT-13, USE-10) · 4. none |
| A long string column alone scores close to the full model (`string_alone`) | 1. text that carries the outcome (award notes inside a description) · 2. text written together with the label that does not map one to one onto it (coffee_rating_prediction's review text: R² 0.25 to 0.67) | when the text is written, against the prediction point | 1. LEAK-10 (Must; a part or another encoding of the target): drop · 2. LEAK-35 (Must; not a leak): keep |
| Two subgroups that share a label separate, features where no signal can exist predict it, or number formats differ by class (probes 7-9) | 1. one class from a separate source or assay (biogeographical_ancestry_prediction: Turkey) · 2. class-specific recording conventions (hepatitis_c_prediction: `ALB`, `BIL` whole numbers in about 100% of patient rows, 10% of donor rows) · 3. batch noise across the whole feature space, no batch id (prostate_cancer_detection: Benign against NED 0.997; m/z < 1 Da AUC 0.81-0.85) · 4. a marker that can explain only part of the label (pancreatic_cancer_mouse_detection) | the paper: which class is a separate assay; how much a fix removes; whether a feature subset still separates same-label groups; the bound on what the marker can explain | 1. LEAK-14 (Must; one class from a separate source): drop that class once the paper confirms it · 2. LEAK-13 (Must; class-specific recording conventions): harmonise · 3. LEAK-15 (Must; batch noise): retire · 4. none: keep, the question noted in the record |
| Row order: the target by position, the next-row label match, a time index against the date (probe 10) | 1. an order sorted by the target, or an index that follows another key after a merge or lookup (california_house_prices_2020: Spearman 1.000 with the address rank, 0.003 with `Listed On`) · 2. a row counter that drives the columns (ecommerce_shipping: `Warehouse_block` is the id modulo 6) · 3. the file order is the time order (seismic_bumps: next-row match 2,583 of 2,583; california's Kaggle id is the sale order) | the index against the date and against any sort key; each categorical column against the id modulo k | 1. SPLIT-22 (Should; row order as time): rebuild the index after such steps · 2. PROV-3 (Must; scope SEL-16): `AHDS`, `No` · 3. SPLIT-22 (Should): keep it as the time index |
| A shallow tree close to the full model, or a formula or lookup for the target (probe 14) | 1. a label the source computes from the columns by a published rule (NEWS2) · 2. a label the definition built that a few features spell out (audiology_diagnosis: two history answers decide 139 of 147 cochlear diagnoses) · 3. a lookup of the inputs (video_game_fps_prediction: log FPS = game + CPU + GPU, R² 0.99998) | the source's label definition; the probes on the source's labels too, when the definition changed the target | 1. SEL-5 (Must; a label computed by a deterministic rule): drop the rule's inputs, or `Trivial` · 2. TP-7, LEAK-4 (Must; a label we built): a convention of the field, checked with a shallow tree · 3. TP-4 (Must): `Trivial`, often `AHDS` |
| Every block of columns has mean 0 and SD 1, or min 0 and max 1, over the whole table (probe 16) | 1. the source transformed with statistics over all rows (coad_colon_adenocarcinoma: z-scores over 260 patients; credit_card_customers: clipped at whole-file percentiles) · 2. a per-row transform or a fixed published scale | the source's processing; whether the unprocessed values exist | 1. LEAK-30 (Must when strong, Should when weak; statistics over all rows): rebuild from unprocessed values (PROV-13), otherwise keep with a `Potential leak, kept on purpose:` note; `No` only for a strong suspected leak · 2. none |

### Group, hidden-group and generated-data probes

| Flag | Readings, highest rank first | How to tell them apart | Rule |
|---|---|---|---|
| Hidden-group hit (`hidden_groups.py`: a column, a composite key `(all but X)`, `(near copies)` or a text key `(text: X)`); also leak probe 11, entity overlap. A near-copy line that reads `not run` (no row has 10 informative columns) is no evidence either way, not 0% | 1. an entity new data would not have (superconductivity: compositions) · 2. one entity measured more than once, a composite key (concrete_compressive_strength: 428 mixes; airfoil_self_noise: wind-tunnel runs) · 3. near copies or a repeated normalised text, a pointer to an entity (the salt forms of one parent structure, one company inspected again, one client's invoices, an ad posted again) · 4. a feature new rows keep (amazon_employee_access `MGR_ID`, covertype `Soil_Type`, mutual_funds_india `sub_category`) · 5. coincidence | what the column means in the source (the source calls it an id) and whether the use case predicts for new entities; whether new rows keep the value; the gap never decides alone, since holding out any useful feature opens one | 1. SPLIT-29, SPLIT-30 (Must; hidden groups): re-split on the true group id, taken from the source's data (SPLIT-24, SPLIT-26) · 2. SPLIT-24 (Must): group on the key when it is what one row's entity is · 3. SPLIT-24 (Must): the key from the source, never the clusters (a normalised text key is an exact key and may be one); exact copies: LEAK-16 to LEAK-21 (copies across the split) · 4. none (SPLIT-4: a feature) · 5. none |
| `test_rows_seen` (temporal tasks: the share of test rows whose entity is on the training side) | 1. the use case is a new entity · 2. the model predicts for known entities (ashrae_great_energy_predictor_iii_1m `building_id`: 100%) | the use case | 1. SPLIT-13 (Should; grouped structure inside a temporal task), USE-10: a question for the curator · 2. none (SPLIT-13: part of the task) |
| Group probe `split_gap` (a grouped task: untuned LightGBM on IID folds against the grouped folds) | 1. rows of a group inform each other: a clear drop under grouped splits · 2. a gap within the fold spread: the grouping changes little | the gap against the spread over folds; the use case | 1. SPLIT-29 (Must): keep the grouped split · 2. SPLIT-4, SPLIT-30 (Must): the split still follows the use case, not the size of the gap (superconductivity: at most 0.009 R², grouped) |
| Group probe `learnability` and `permutation` (a grouped task) | 1. no signal across groups: every model below the baseline on unseen groups (telemonitoring_parkinsons: R² -0.17 to -0.31 grouped, 0.75 IID) · 2. a handful of groups of a class per test fold · 3. an untuned model overconfident on unseen groups (mice_protein: LightGBM log loss 2.53 against a baseline of 2.07, random forest 1.12) | several families scored per group against the class-share baseline; the permutation p-value; the groups of each class per fold; before a warm start, a model against the group's known value carried forward (telemonitoring: 6.33 against 6.48) | 1. SPLIT-28 (Must): the use case has to allow known groups, or the dataset goes · 2. TP-5 (Must): `Too Small` · 3. none (SPLIT-27): judge with the other families |
| Generated-data marks (`generated_probes.py`: `formula`, `rule_leaves`, `independent_columns`, `uniform_within_class`); also leak probe 15 | 1. generated data (healthcare_insurance_expenses: 1,220 of 1,338 charges follow one formula; churn: rule leaves) · 2. a target legitimately computed from the features: a score, a label defined by thresholds · 3. a leak (gives `formula` and `rule_leaves` too) · 4. inputs set by a design: a uniform grid, a Latin hypercube (gives the two independence marks) · 5. coincidence: either independence statistic alone is common in real data (santander_customer_transaction_prediction: 5.4% of pairs dependent, no uniform column; bank_customer_churn: one uniform column) | what the source says ("simulated", "artificial", "generated", a textbook example); marks the probe does not test (dependence the world would show, several columns with one distribution, every row of a group following a rule); the dependence the domain must show, checked directly (AST and ALT in liver patients, size and equity in banks); the uploads traced; the generator written down, which settles it | 1. PROV-3 and SEL-16 (Must; the paper's criterion 4B): `AHDS`, `No` · 2. SEL-5 (Must; a label computed by a deterministic rule): drop its inputs, or `Trivial` · 3. the LEAK rule of the mechanism found (LEAK-10 to LEAK-32) · 4. none · 5. none |

## The decisive experiment

The decisive experiment is the cheapest test whose outcome would change the decision (EV-1). Name the verdict or the
fix each outcome would lead to, then run the cheapest test that tells them apart. Examples from the curators' work:

| Question | Decisive experiment | Case |
|---|---|---|
| Is a forecasting-like panel a tabular task? | a model on the features against each entity's best naive forecast on the shipped windows | ashrae_great_energy_predictor_iii: naive 1.393 / 1.273 / 1.372, LightGBM with 1,000 trees 1.261 / 1.176 / 1.223 (2026-10-15) |
| Does a column leak? | the score with and without it on the shipped splits | heart_failure `time`: AUC 0.90 to 0.75 |
| Is a same-day value known in time? | its daily changes against the same day's outcome and the previous day's | garments_worker_productivity `incentive`: Spearman 0.53 against 0.07 |
| Did a scale change over time? | a converted scale against the published one | college_scorecard: median change 2016 to 2017 within an institution 0 instead of +30 (Lennart, 2026-10-16) |
| Is the task trivial? | the raw feature, chosen on each split's training side, against the methods fold by fold | fitness_club: AUC 0.822, above all 37 configurations (retired); sepsis_survival_minimal_clinical_records: 0.704, below the best on every fold (kept) |
| Is a record a duplicate? | the named original's ids and values against ours | colleges: all 7,804 institution ids, values agreeing for 97-99% (Lennart, 2026-10-12) |
| Is the target censored by the download date? | the target by period in two downloads | sf_permit_time: 2025 p90 from 97 to 160 days |
| Is a stage the source describes the better task? | the task at that stage | eryhemato_squamous_disease: macro AUC 0.999 after the biopsy, 0.98 before |
| What does a missing time axis cost? | the data held out by file position | account_debt_south_africa: ROC AUC 0.877 to 0.843 and 0.786 (Lennart, 2026-10-12) |
| Does the gap for late labels matter? | the score with and without the gap | brazilian_ecommerce: R² 0.353 with, -0.054 without (Lennart, 2026-10-15) |
| Did a looked-up attribute change after the outcome? | the looked-up value against the one recorded at the time, per test window | melbourne_housing_market: `Bedroom2` equals `Rooms` in 98-100% of the rows |
| Is the data generated? | the generator written down | healthcare_insurance_expenses: one formula for 1,220 of 1,338 charges |
| Can a recording marker explain the label? | the most the marker's class shares can explain | pancreatic_cancer_mouse_detection: at most AUC 0.56, against 0.63-0.66 |
| Is a small grouped task unlearnable? | several families per group with a permutation test; before a warm start, the carried-forward baseline | mice_protein: random forest 1.12 against a baseline of 2.07; telemonitoring_parkinsons: 6.33 against 6.48 |

Not decisive:

* A test whose outcome cannot change the decision. A comparison over a few test windows changes with the kind of
  window, so it measures the windows, not the design (aeolus; Lennart, 2026-10-12). A hidden-group gap opens for any
  useful feature (SPLIT-4, [splits.md](splits.md)). Unchanged predictions do not test whether the stored values depend
  on the test rows (EV-6). A single-column score does not test when a column was recorded (EV-2).
* One quick model: one untuned gradient-boosting run does not show that a small grouped task is unlearnable
  (SPLIT-27, [splits.md](splits.md)).
* A question to the curator about a fact the data can settle (EV-1).

## Where evidence is written

How evidence is written for the curator: [writing.md](writing.md). Record comments hold the long evidence for a
dataset we keep and the dataset's notes the short decisions, each with the number that decides it; an issue for the
curator gives the evidence with numbers only where they decide; a report says which evidence proves a mechanism and
which is circumstantial (EV-6). A check in the verification report carries one line of evidence
([verification.md](verification.md); EV-7). A paper is cited as `Sec. 6.1, p. 12: "..."`, and a problem found in a
competition's threads or notebooks with the thread or notebook link (PROV-16, PROV-18, [provenance.md](provenance.md)).

## Cases

Precedents: how a rule was applied. They never change a rule; an exception is listed with the fact that set it apart.

| Rule | Dataset | Decision (date, curator) | Kind |
|---|---|---|---|
| EV-1 | colleges (OpenML 42727) | marked a duplicate of college_scorecard only after its named original (a Colleges.txt file) proved to be the College Scorecard file of 2013-14: all 7,804 institution ids, faculty salary, size and admission rate agreeing for 97-99% (2026-10-12, Lennart asked for the check) | applied |
| EV-1 | mutual_funds_india | "the rating would be known" was true, but the rating is computed from the target window: dropped | applied |
| EV-1 | santander_customer_transaction_prediction | "the features only use the Kaggle train file" missed that they use all its rows, our test folds included: leak confirmed | applied |
| EV-1 | consumer_complaints | "is this a survival task?" turned out to be censoring at download | applied |
| EV-1 | aeolus | the training history (flights from 2023 on, two-week windows) chosen from the use case, not from a comparison over a few test windows (2026-10-12, Lennart) | applied |
| EV-2 | kick | the comment's Kaggle split "grouped by auction location" came from a buggy check: 78.9% of its test rows are at a location also in train | applied |
| EV-2 | california_house_prices_2020 | the "temporal" split ran on alphabetical order: an index lookup had sorted the rows by address | applied |
| EV-2 | appliances_energy_prediction | the authors' random split on 10-minute readings over 4.5 months is a claim; the task is forecasting, `No` | applied |
| EV-2 | intrusion_detection | the paper's own framing decided over its headline ">99.8%" (Shafi et al. 2025, Sec. 6.1: "our focus is on developing a profiling system, not a detection system"): `No Good Target / Scientific Discovery` | applied |
| EV-2 | kddcup99 | the paper text refuted the claim about to be made: Tavallaee et al. (CISDA 2009, Sec. III) state that the simulation artifacts do not affect the 41 KDD features | applied |
| EV-2 | pkdd-15-taxi-trip-time-prediction-ii | only the notebooks showed why a public snippet scores well: the test polylines are truncated prefixes of the trips (de Brebisson et al. 2015), a trajectory task | applied |
| EV-2 | hr_analytics | rebuilt from the hackathon's own train file: Kaggle's copy had added 2,623 test rows labelled 1 and gave 0.80, the real labels ROC AUC 0.62-0.63 (2026-10-14) | applied |
| EV-3 | amazon_employee_access | `MGR_ID` hit: no action, a request's manager is known when it is made (2026-10-06) | applied |
| EV-3 | superconductivity | grouped by composition although the gap is at most 0.009 R²: the use case decided, not the gap (2026-10-06) | applied |
| EV-3 | diamonds, splice | near-saturated scores (R² 0.993, AUC 0.99+) showed no leak in the probes | applied |
| EV-3 | forest_fires | `no_signal` (R² 0.013) answered by tuned results: TabPFN-3.5 beats the mean on 26 of 32 folds; kept (2026-10-06) | applied |
| EV-3 | mercari_price_suggestion | `no_spread` came from the probe leaving the text out: R² 0.06 without, 0.67 with; kept (2026-10-06) | applied |
| EV-3 | kickstarter | the written prediction point ("predict at launch") found `staff_pick`, which no probe flagged | applied |
| EV-3 | airfoil_self_noise | the wind-tunnel runs were found by reading the source; the probe had no hit until composite keys were added (2026-10-14), and its single-column check skips non-integer floats, so the thickness column that alone separates 104 of 106 runs was never a candidate (review panel, 2026-10-19); since 2026-10-21 the check takes floats and the thickness is a hit (105 values for 106 runs, gap 0.123) | applied |
| EV-3 | concrete_compressive_strength | 428 mixes behind 1,030 tests, missed by the column and near-copy checks until 2026-10-14 | applied |
| EV-4 | lucas_topsoil | JRC's terms forbid redistribution; the record is triaged on what the survey measures (licence rule: 2026-09-23, Lennart) | applied |
| EV-4 | numerai_v5_2, aeolus, corporate_credit_rating_cat, african_credit_scoring_challenge | earlier reviews raised the licence as an issue; it is a one-line note, and the Zindi "private property of the client" and the Credit Risk Analytics terms are release-checklist items (2026-10-21, Lennart) | applied |
| EV-4 | (general) | scores other benchmarks published (TALENT, leaderboards) are no evidence: their random splits are wrong for most of our tasks (2026-10-15, Lennart) | applied |
| EV-4 | (general) | whether a dataset is in some model's pretraining data changes no decision (2026-10-12, Lennart) | applied |
| EV-4 | TabSTAR's version of a dataset | another collection's columns or labels are no reference for ours (2026-10-15, Lennart) | applied |
| EV-4 | coad_colon_adenocarcinoma | ships 36,355 features; its report had weighed one model's 50,000-feature cap (2026-10-15, Lennart) | applied |
| EV-5 | us_accidents | its published "78% accuracy" settled nothing; learnability is judged with ROC AUC or log loss against the class prior (2026-09-23, Lennart) | applied |
| EV-6 | (the leak audit) | all 15 findings of the first sweep held their second check, which corrected details and proposed better fixes (2026-09-24 to 2026-10-01) | applied |
| EV-6 | ghanas_indigenous_intel | an overclaim corrected in review: reporter history is legitimate under a temporal split | applied |
| EV-6 | online_shoppers | "PageValues includes the session's own purchase" is likely, not shown: Feb-May dropped, the evidence called circumstantial | applied |
| EV-6 | coad_colon_adenocarcinoma | z-scores over all patients first called harmless (no labels, tree predictions unchanged); the training rows alone give each test fold's mean of every feature (2026-10-16, Lennart) | applied |
| EV-6 | fitness_club | `Trivial` proven: `months_as_member` alone, chosen on all 30 training sides, AUC 0.822, above all 37 configurations; retired (2026-10-05) | applied |
| EV-8 | breast_cancer_prediction | before 2026-10-15 the linear probe read categories as integer codes: ROC AUC 0.80 with codes, 0.92 one-hot | applied |
| EV-8 | mortgage | the class shares matched untuned models on 50k sampled rows; on the full training side LightGBM beats them in 3 of 3 quarters; kept (2026-10-07). At the 50,000-row random cap LightGBM (+0.113) fell below `time` alone (+0.123) and raised `one_feature`; on the newest 200,000 rows of each train side no flag (LightGBM +0.151, drift +0.122, one feature +0.117; 2026-10-21) | applied |
| EV-9 | heart_failure | the label-free distance score is 0.64 on this ordinary data: read against the full model's 0.73, not against 0.5 | applied |
| EV-9 | santander_customer_transaction_prediction, homesite_quote_conversion | one independence statistic alone is common in real data: 5.4% of pairs dependent but no uniform column; 13 of 42 columns uniform but 45% of pairs dependent | applied |

## In Data Foundry

* How to run the probes and where their output goes:
  [checks_and_probes.md](../../knowledge-data-foundry/references/checks_and_probes.md). The entry points are in
  [scripts/](../../knowledge-data-foundry/scripts/): `leak_probes.py` (leak probes 1-6 and 14), `task_probes.py` (the
  task flags), `group_probes.py` (the split gap, learnability and the permutation test), `hidden_groups.py` (the hits,
  and `test_rows_seen` for a temporal task), `generated_probes.py` (the four marks) and `tuned_results.py` (the tuned
  methods fold by fold; `--feature auto` for the raw-feature test). The probe methods are this skill's
  [scripts/curation_probes/](../scripts/curation_probes/).
* Where evidence is recorded: `curation_comments` bullets with the deciding number, `_decisions` tables in the README,
  a `Potential leak, kept on purpose:` note
  ([definitions.md](../../knowledge-data-foundry/references/definitions.md), "Decisions" and "Recording decisions"),
  and an `**Assessment (AI, YYYY-MM-DD):**` line in the record
  ([records.md](../../knowledge-data-foundry/references/records.md)).
* The stages, and when a screening verdict gives way to the add stage's findings:
  [pipeline.md](../../knowledge-data-foundry/references/pipeline.md).
* The house rules ([knowledge-data-foundry](../../knowledge-data-foundry/SKILL.md)) repeat EV-4 as a limit on every
  workflow.
