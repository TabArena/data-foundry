# What belongs in the benchmark

How we decide whether a dataset belongs in TabArena: the scope, the five selection criteria, the patterns that
settle most calls quickly, the verdict values and how to read decision markers. Adapted from the TabArena paper
(Section 2, Section 4 and Appendix B.2) and extended by the curators' decisions since. The split regimes are in
[splits.md](splits.md), the use case and the prediction point in [use_case.md](use_case.md), sources and duplicates
in [provenance.md](provenance.md), leaks in [leak_checks.md](leak_checks.md), and whether a curated task is trivial or
too small in [task_probes.md](task_probes.md).

## Scope at a glance

We include real-world tabular datasets published for a predictive classification or regression task, where a random
(IID), temporal or grouped split is the appropriate protocol and tabular models are competitive. We exclude
time-series forecasting; recommendation, ranking, click-through-rate and information-retrieval tasks; non-predictive
scientific-discovery or survey tables; non-tabular data (image, text, audio) where modality-specific models clearly
win; artificial, deterministic or simulated data; trivial tasks; data with irreversible quality issues or target
leakage; duplicates and re-uploads; and anything with ethical concerns.

Datasets come from earlier tabular benchmark studies (accepted ones are re-evaluated, and those rejected for being
non-IID, too small or for data issues are looked at again), from non-IID and multimodal benchmarks, and from browsing
public repositories and competition sites (UCI, OpenML, Hugging Face, Kaggle, Zindi, ASlib) and government data
portals. Curation is manual and human-verified: the criteria need judgment, so the reasoning goes into the record
with the verdict.

## The selection criteria

A dataset must satisfy all five.

1. Unique. It has a unique original source, and its task is not already in the benchmark. Re-uploads under new
   names are common, so the first job for any candidate is to find where the data first came from
   ([provenance.md](provenance.md)).
2. An IID or non-IID tabular task. A random, temporal or grouped split is the appropriate validation protocol
   ([splits.md](splits.md)).
3. Published for a predictive task: explicitly a classification or regression task, simulating a decision someone
   makes with the prediction ([use_case.md](use_case.md)). Out: scientific-discovery or survey tables, CTR,
   ranking and recommender tasks. The target is an observed outcome or an expert annotation:
   * A label from unsupervised learning is no real predictive task: a molecular subtype defined by clustering (PAM50,
     expression subtypes, NMF clusters; brca_breast_cancer, glioblastoma, ov_ovarian_cancer, Lennart 2026-10-12).
   * A label the source computes with a published, deterministic rule from the columns: drop the rule's inputs when
     the rest still makes a real task (account_debt_south_africa); when the inputs are the whole task it is `Trivial`
     (central_international_medical_college_and_hospital_health_risk_prediction, NEWS2).
   * A label counted over one calendar window shared by all rows, instead of a fixed time after each row, supports
     only a look back at which rows drew the outcome: `No Good Target / Scientific Discovery` (analcatdata_supreme,
     Congress's responses in 1979-1988 to Supreme Court rulings of 1953-1988; Lennart, 2026-10-14).
   * A label the respondent already knows, asked in the same interview as the features (a past diagnosis), is
     predicted by nobody. A screening task needs positives that do not know yet, found by an independent measurement
     such as a lab test (cdc_diabetes_health_indicators: "ever told you have diabetes", told a median of 10 years
     earlier, with the undiagnosed in the negative class; Lennart, 2026-10-15).
4. Representative of a real tabular-ML application. Out are datasets that:
   * (A) come from a non-tabular modality where modality-specific models are clearly better, judged per dataset.
     Vectorized image, text, audio or time-series data is fine where tabular models are competitive.
   * (B) do not come from a real random distribution: artificial or deterministic data, and simulated physics that
     has its own benchmarks (Higgs).
   * (C) are trivial: one feature or a simple rule gives the score the best methods reach, or the task is solved
     perfectly. A small but real signal, or methods that tie on a hard task, is not trivial ([task_probes.md](task_probes.md)).
   * (D) have irreversible quality issues that leak the target, such as a feature that is the output of a supervised
     transform fit on the whole dataset ([leak_checks.md](leak_checks.md)). An unsupervised transform over all rows
     (scaling, PCA) is a weak leak and no reason for exclusion on its own (below).
   * (E) lack the information needed to decide after a thorough search; then it is the curation team's call.
5. Ethically unambiguous. Out: tasks with ethical concerns, including data whose subjects or creators ask that it
   not be used for ML (the Pima Indian Diabetes Dataset).

Licence and redistribution terms are not a criterion (Lennart, 2026-09-23). A non-commercial clause, a request-only
download or a no-redistribution rule is noted in the record (what the terms are and where they are stated) and is
never the reason for a `No`, a `TBD -> 2nd Tier` or a marker. `lucas_topsoil` is the example: JRC's terms forbid
redistribution, and the record is still triaged on what the survey measures.

## Quick decision patterns

Recurring signals and the usual markers and verdict. They speed up triage; the dataset still wins over the pattern.
A signal is often in the name alone (`*-recommendation-challenge`, `*-forecasting-*`).

Read the record's comments first and understand what they mean. They usually hold the decisive fact (the true
source, a leak mechanism, the setup). `jannis` looks like anonymised numeric columns, but its comment ("From AutoML
challenge ... SAIAPR-TC12") shows it is image-derived, so `Image`, `No`. `sonar`'s comment shows an outdated
handcrafted toy experiment: out on its setup, not merely on its acoustic features.

### Scope by the original task

A re-upload often relabels a dataset into a different task. Trace what the data was originally collected and used
for and let that decide the scope. `yearprediction_the_million_song_dataset` is the trap: OpenML 4352 serves it as a
regression, but it is the Million Song Dataset Challenge, a song-recommendation task, so it is
`Out-of-scope Task (CTR/RecSys/Ranking)`, `No`, and the regression re-framings are duplicates.

Recommendation, ranking and CTR tasks are `Out-of-scope Task (CTR/RecSys/Ranking)`, `No` (criterion 3), also when a
mirror serves them as classification or regression.

### Forecasting or a temporal task

Time-series forecasting (future values of a series: demand, sales or a price over a horizon) is
`Time-series (Forecasting)`, `No`. A fixed predictive task that only needs a temporal split (a delay, a price) is in
scope; [splits.md](splits.md) has the distinction, the missing-timestamp trap and why a prescribed split is a claim.
A panel that looks like forecasting is in scope when a model on the features clearly beats each entity's naive
profile ([task_probes.md](task_probes.md), "A forecasting-like task").

### Artificial, generated or simulated

Synthetic, toy, handmade or deterministic data, and simulated physics with its own benchmarks, are
`AHDS (Artifical/Handmade/Deterministic/Simulated)`, `No` (criterion 4B). How to find out whether a table was
generated is in [provenance.md](provenance.md).

### Non-tabular modality

Raw images, audio or text where modality models dominate are `Image`, `NLP (Text)` or `Wrong Domain / Source
Modality`, usually `No`. Vectorized features where tabular models are competitive can be in scope (criterion 4A).

Features computed from an image or video to describe its content are a vision task even when the columns are
numeric: raw pixels, HOG, colour or texture histograms, morphological, geometric or spectral descriptors from an
image-analysis pipeline, video-derived kinematics, remote-sensing spectra. That covers recognition sets (`letter`,
`mfeat_*`, `gina`, `gtsrb_*`, `optdigits`, `pendigits`, `usps`, `semeion`, `texture`, `one_hundred_plants_*`) and
measured-from-image tables (`magic_gamma_telescope` shower geometry, `wdbc` nuclei descriptors,
`image_gesture_phase_segmentation`, `dry_bean`, `raisin`, `pumpkin_seeds`, `rice`, `satimage`, `wilt`,
`banknote_authentication`).

One more layer of abstraction is still image-derived:

* Descriptors of an image (its geometry, shape, layout) stay image-derived when mixed with a few non-visual columns.
  `internet_advertisements` "encode the geometry of the image (if available) as well as phrases occurring in the URL,
  the image's URL and alt text" (UCI): an is-this-an-ad-image task, `Image`, `No`.
* A human scoring what they see in an image is an image feature. `breast_w`'s 1-10 cytology grades are a
  pathologist's scoring of cell morphology under a microscope: `No`.
* The exception: readings that real tabular models take as inputs. When the human reading is the established
  clinical or operational result that tabular models are used on in practice, the task stays in scope: the BI-RADS
  assessment and density of a screening mammogram, which risk models such as the BCSC Risk Calculator combine with
  risk factors (`breast_cancer_prediction`), or the thallium-scan result of `heart_disease_cleveland`. The rule
  stands in for the real-world use: when a rule seems to exclude a dataset, check how the prediction is made in
  practice, and let the use case decide (Lennart, 2026-10-15). `breast_w` stays out because its grades describe the
  slide for a call pathology makes from the image itself.

Attributes measured on the entity directly (lab values, sensor readings, questionnaire answers, transaction fields)
are tabular. Signals are judged case by case: engineered acoustic measures the field uses as the instrument (jitter
and shimmer in the Parkinsons voice data) can be in scope, raw spectral bins lean out. `wbcatt` (expert-annotated
white-blood-cell morphology) sits on the `breast_w` boundary and is kept only provisionally. Decide on the columns,
not on the dataset's fame.

### Duplicates and versions

A re-upload or processed copy of a known dataset is a `Duplicate` ([provenance.md](provenance.md) has the method).
Different cuts of one dataset are duplicates too when neither adds a distinct task (`arsenic_male_lung` is the
lung-cancer version of the same exposure data as `arsenic_male_bladder`). A shared source is not a duplicate when it
yields different tasks (`parkinsons_biomedical_voice_measurements` detects a disorder,
`telemonitoring_parkinsons_biomedical_voice_measurements` tracks its progression; `amex_iid` and `amex_non_iid` are
the IID and grouped versions of one competition).

### Survey and discovery tables

A table without a genuine predictive target is `No Good Target / Scientific Discovery`, `No` or `TBD -> 2nd Tier`.

### Trivial, too small, empty

`Trivial` (one feature or a simple rule matches the best methods, or the task is solved) is `No` (criterion 4C), and
`Too Small` (a handful of units of a class per test fold) is `No` or `TBD -> 2nd Tier`. Both need evidence from the
task's own splits; the rules are in [task_probes.md](task_probes.md). A small but real signal is no reason to retire.
Under class imbalance, accuracy against the majority class is no evidence in either direction (Lennart, 2026-09-23):
judge learnability with ROC AUC or log loss against the class prior, and fit a quick gradient-boosting model on the
features known at prediction time when the data loads (`us_accidents`: its published "78% accuracy" settled nothing).

### Leakage and irreversible damage

A feature that is the output of a supervised transform fit on the whole dataset (a discriminant-analysis score, a
target or mean encoding, a model's own prediction) bakes label information into every row and cannot be recomputed
per split: `Data Quality Issue`, `No` (criterion 4D). `yeast` ships a "Score of discriminant analysis of the amino
acid content of vacuolar and extracellular proteins", fit on the full dataset.

An unsupervised transform over all rows (z-scores, min-max, a quantile transform, RMA, PCA, batch correction) also
carries the test rows into every value, but it is a weak leak that real data often come with. Rebuild from the
unprocessed values when the source has them (coad_colon_adenocarcinoma, retired for a rebuild from the GDC);
otherwise keep the dataset with a note. It is a reason for `No` only when a strong leak is suspected (Lennart,
2026-10-19). [leak_checks.md](leak_checks.md) has the cases.

### Ethics, licence

An ethical concern (sensitive use, creators who ask that the data not be used for ML) is `Ethical Issue`, `No`. A
licence or redistribution restriction is no reason and no marker: note it and triage the data on its merits.

### Clear cases

A genuine real-world tabular classification or regression task with a clear target and adequate size is `Yes` (well
known, strong) or `TBD -> Yes` (plausible, unverified).

### Unknown or unclear source

When following every link ends at an anonymous re-upload with no documentation and no traceable upstream (paper,
competition, institution, an identifiable first uploader), we cannot tell what the data is: `Missing source
information`, `No` (criterion 1; `water_quality_and_potability`, `3d_estimation_using_rssi_of_wlan_dataset_complete_1_target`,
`calendardow`). A live link is not a known source, and clear provenance is itself a strong sign of a good dataset.
A source that is plausible but unclear in a detail stays, with a note of what to clarify (bad_customer_detection;
Lennart, 2026-10-14).

A record with too little information while the dataset's origin is known (a bare link, no description) is not
rejected for that: use `TBD -> Yes` or `TBD -> 2nd Tier` and write down what to inspect (the size after cleaning, the
real target, the split).

## Verdict values

The verdict (`suggestion`) is what we suggest for the dataset now; it can change later (a shipped dataset can be
excluded).

* `Yes`: include. `TBD -> Yes`: likely include, pending verification.
* `TBD -> 2nd Tier`: plausible but secondary. `No`: exclude.
* `No (Retired)`: excluded, but it shipped in a collection before the verdict changed (later found trivial, an
  ethical concern surfaced). The collection tag stays, and the record says why it was retired. A never-shipped
  record gets plain `No`.
* `Disagreement`: curators disagree; not shipped, needs resolution.
* `Yes (Disagreement)`: shipped on purpose with an open disagreement to re-evaluate. It counts as accepted.

A dataset shipped in a collection carries `Yes`, `Yes (Disagreement)` or `No (Retired)`.

## Reading decision markers and optional fields

Records are sparse on purpose; a missing field is usually fine.

* Decision markers flag issues. A clean dataset has none, and a `Yes` or a `No` without a marker can be right.
* A marker can be a provisional guess of a concern ("watch out for `Trivial`"), so `Yes` with a concern marker is not
  a contradiction: read the comments.
* `problem_type`, `required_split`, `original_data_state`, `domain` and `year` are optional metadata; their absence is
  no problem to flag. Only the verdict is required.
* `problem_type` can be a choice of task. A table can support a regression target or a classification one where
  taking one means dropping the other: `pva_revenue_prediction_kddcup98` has the donation amount and the donated-at-all
  flag, two framings of one signal. Then the field records the task we ship, and the other framing goes into the
  comments (or its own `_clf` dataset).
* `Multi-target` is for several distinct targets predicted at once (next-day minimum and maximum temperature, several
  soil nutrients). Remove it when the dataset has one target or when the targets are framings of one signal
  (caracas_cervical_cancer: four results from one work-up, the folder predicts the biopsy; Lennart, 2026-10-15).

## Arguing a call

A documented decision is not a correct one. When the evidence contradicts the stated reasoning, say so and argue the
case.

* Argue from what the data is (the feature composition, the true source, the size, the actual target), not from how
  someone might solve the broader problem today. Features that are mostly URL and text tokens plus a few geometry
  numbers are not an image task because the objects pictured were ads; a vision model could not see the dominant
  features.
* Steelman the existing decision first, then give a concrete counter-argument that can be checked: numbers, the
  feature breakdown, what a model can or cannot access.
* Surface it, do not override it: the curator has the call. How to record a counter-argument is in the Data Foundry
  [records.md](../../knowledge-data-foundry/references/records.md).
* It cuts both ways: argue for keeping an exclusion the curator is inclined to overturn when the evidence says so.

## In Data Foundry

The verdicts, markers and tags are fields of the curation record, with their vocabulary, the ship invariant and the
review queue: [records.md](../../knowledge-data-foundry/references/records.md).
