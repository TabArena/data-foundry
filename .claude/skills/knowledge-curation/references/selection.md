# What belongs in the benchmark

Part 1 of the curation rules, under P1 (ethics) and P2 (scope) in [principles.md](principles.md). The rules of earlier
parts win over this file's rules in a conflict; within this file a rule wins over the rules below it of the same
strength. How to weigh, exceptions and amendments: [principles.md](principles.md).

How we decide whether a dataset belongs in TabArena: the scope, the ethics and scope rules, the patterns that settle
most calls quickly, the verdict values and the decision markers. Adapted from the TabArena paper (Section 2, Section 4
and Appendix B.2) and extended by the curators' decisions since. The split regimes are in [splits.md](splits.md), the
use case and the prediction point in [use_case.md](use_case.md), sources and duplicates in
[provenance.md](provenance.md), leaks in [leak_checks.md](leak_checks.md), and whether a curated task is trivial or too
small in [task_probes.md](task_probes.md). Arguing a call (steelman the decision, argue from what the data is, surface
it, in both directions) is in [principles.md](principles.md).

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

## The five criteria

The paper's five selection criteria, which a dataset must all satisfy, are now principles P1-P6 of
[principles.md](principles.md). Criterion 1, unique (a unique original source, a task not already in the benchmark),
is P5, PROV-4 to PROV-8 in [provenance.md](provenance.md): re-uploads under new names are common, so the first job for
any candidate is to find where the data first came from. Criterion 2, an IID or non-IID tabular task, is P2 and P4,
with the regime in SPLIT-1 to SPLIT-3 of [splits.md](splits.md). Criterion 3, published for a predictive task, is P2:
SEL-3 to SEL-11 here. Criterion 4, representative of a real tabular-ML application, splits up: 4A (a non-tabular
modality) and 4B (not a real random draw: artificial, deterministic, simulated) are P2, SEL-12 to SEL-16 here; 4C
(trivial) is TP-4 in [task_probes.md](task_probes.md); 4D (an irreversible leak) is LEAK-27 in
[leak_checks.md](leak_checks.md); 4E (not enough information after a thorough search) is P5, PROV-1 and PROV-2 in
[provenance.md](provenance.md). Criterion 5, ethics, is P1: SEL-1.

Licence and redistribution terms (a non-commercial clause, a request-only download, a no-redistribution rule) are no
criterion and never the reason for a `No`, a `TBD -> 2nd Tier` or a marker (Lennart, 2026-09-23):
[evidence.md](evidence.md), EV-4.

## Rules

### Ethics

**SEL-1 (Must).** A task with ethical concerns is out, including data whose subjects or creators ask that it not be
used for ML. Marker: `Ethical Issue`. Cases: the Pima Indian Diabetes Dataset.

### How the scope rules are read

**SEL-2 (Must).** The rule stands in for the real-world use: when a rule seems to exclude a dataset, check how the
prediction is made in practice, and let the use case decide (Lennart, 2026-10-15). Every scope rule below is read this
way; it is how the use case (P3, [use_case.md](use_case.md)) informs the scope. Cases: breast_cancer_prediction,
heart_disease_cleveland (SEL-14).

### A predictive task

**SEL-3 (Must).** The dataset is published for a predictive task: explicitly a classification or regression task,
simulating a decision someone makes with the prediction (USE-1, [use_case.md](use_case.md)). The target is an observed
outcome or an expert annotation. A table without a genuine predictive target, such as a scientific-discovery or survey
table, is out. Marker: `No Good Target / Scientific Discovery`.

**SEL-4 (Must; narrows SEL-3).** A label from unsupervised learning is no real predictive task: a molecular subtype
defined by clustering (PAM50, expression subtypes, NMF clusters). Cases: brca_breast_cancer, glioblastoma,
ov_ovarian_cancer (Lennart, 2026-10-12).

**SEL-5 (Must; narrows SEL-3).** A label the source computes with a published, deterministic rule from the columns:
drop the rule's inputs when the rest still makes a real task; when the inputs are the whole task, it is `Trivial`
(TP-4). Marker: `Trivial`. Cases: account_debt_south_africa,
central_international_medical_college_and_hospital_health_risk_prediction (NEWS2).

**SEL-6 (Must; narrows SEL-3).** A label counted over one calendar window shared by all rows, instead of a fixed time
after each row, supports only a look back at which rows drew the outcome. Marker:
`No Good Target / Scientific Discovery`. Cases: analcatdata_supreme (Lennart, 2026-10-14).

**SEL-7 (Must; narrows SEL-3).** A label the respondent already knows, asked in the same interview as the features (a
past diagnosis), is predicted by nobody. A screening task needs positives that do not know yet, found by an independent
measurement such as a lab test. Cases: cdc_diabetes_health_indicators (Lennart, 2026-10-15), stroke_prediction (an
undated stroke the patient already had; 2026-10-26).

### The original task

**SEL-8 (Must).** The original task decides the scope. A re-upload often relabels a dataset into a different task, so
trace what the data was originally collected and used for, and judge that task. Cases:
yearprediction_the_million_song_dataset.

**SEL-9 (Must).** Recommendation, ranking, click-through-rate and information-retrieval tasks are out, also when a
mirror serves them as classification or regression. Marker: `Out-of-scope Task (CTR/RecSys/Ranking)`. Cases:
yearprediction_the_million_song_dataset.

**SEL-10 (Must).** Time-series forecasting, future values of a series (demand, sales or a price over a horizon), is
out: it needs other assumptions and another protocol, and it has its own community. Marker:
`Time-series (Forecasting)`. Cases: combined_cycle_power_plant, appliances_energy_prediction ([splits.md](splits.md),
Cases).

**SEL-11 (Must; narrows SEL-10).** A fixed predictive task that only needs a temporal split (a delay, a price) is in
scope. [splits.md](splits.md) has the split it gets (SPLIT-6), the missing-timestamp trap (SPLIT-7, SPLIT-8) and why a
prescribed split is a claim (SPLIT-5). A panel that looks like forecasting is in scope when it passes TP-10
([task_probes.md](task_probes.md), "A forecasting-like task"): a model on the features clearly beats each entity's
naive profile, and the source's top solutions used no lagged target.

### Real tabular data

**SEL-12 (Must).** Data from a non-tabular modality (image, text, audio) is out where modality-specific models are
clearly better, judged per dataset. Vectorized image, text, audio or time-series data is fine where tabular models are
competitive. Markers: `Image`, `NLP (Text)`, `Wrong Domain / Source Modality`.

**SEL-13 (Must; narrows SEL-12).** Features computed from an image or video to describe its content are a vision task
even when the columns are numeric: raw pixels, HOG, colour or texture histograms, morphological, geometric or spectral
descriptors from an image-analysis pipeline, video-derived kinematics, remote-sensing spectra. One more layer of
abstraction is still image-derived: descriptors of an image (its geometry, shape, layout) stay image-derived when mixed
with a few non-visual columns, and a human scoring what they see in an image is an image feature. Marker: `Image`.
Cases: the lists under Patterns, "Non-tabular modality".

**SEL-14 (Must; narrows SEL-13, applies SEL-2).** Readings that real tabular models take as inputs stay in scope: when
the human reading is the established clinical or operational result that tabular models are used on in practice, the
task is tabular. Cases: breast_cancer_prediction, heart_disease_cleveland; breast_w stays out.

**SEL-15 (Must; amended 2026-10-21, Lennart, on infrared_thermography_temperature).** Attributes measured on the
entity directly (lab values, sensor readings, questionnaire answers, transaction fields) are tabular. A physical
quantity measured through an imaging device at defined sites (a temperature, a volume, an angle), used by the field as
the instrument's reading, is a measurement, not an image descriptor (SEL-13); the counter-cases are satimage and wilt,
where an imaging sensor's values serve to recognise what the image shows. Decide on the columns, not on the dataset's
fame. Signals are judged case by case (Weighed factors). Cases: wbcatt, infrared_thermography_temperature.

**SEL-16 (Must).** Data that does not come from a real random distribution is out: artificial (synthetic, toy),
handmade or deterministic data, and simulated physics that has its own benchmarks. How to find out whether a table was
generated: PROV-3 in [provenance.md](provenance.md), "Is the data generated?". Marker:
`AHDS (Artifical/Handmade/Deterministic/Simulated)`. Cases: Higgs, sonar.

### Enough information to decide

Not enough information after a thorough search: PROV-1 and PROV-2 in [provenance.md](provenance.md). (SEL-17 was
merged into PROV-1 and PROV-2 on 2026-10-19.)

## Weighed factors

* **Engineered acoustic measures the field uses as the instrument** (+, SEL-15): jitter and shimmer in the Parkinsons
  voice data can be in scope.
* **Raw spectral bins** (−, SEL-15): they lean out.
* **Clear provenance** (+): a strong sign of a good dataset; the factor is weighed under PROV-1
  ([provenance.md](provenance.md), Weighed factors).

## Priority

Every record that is not rejected carries a priority from 1 (look at it last) to 5 (look at it first): how urgently a
curator should act on it at its stage. Screening sets it from the source, to order the review of the screening; adding
the dataset sets it again from what was measured, to order the review of the added datasets (a later stage's measured
finding supersedes an earlier reading). It is a weighing of factors, never a verdict, and a curator may change it.
Start at 1 and add one point for each factor that holds; take one point off for a known risk; never go below 1 or
above 5 (first version, 2026-10-19, to be tuned; it orders the review of added datasets since 2026-10-20):

| Factor | One point when |
|---|---|
| A gap in the benchmark | the dataset's domain, problem type or regime is thin among the accepted datasets (screening: the coverage snapshot; once added: counted over the accepted definitions) |
| A clear use case | the source names who acts on the prediction and the decision, and the fit is direct (USE-1, USE-8, [use_case.md](use_case.md)); a use case the curation wrote ("for example a lender") does not count |
| A strong source | the first publisher documents the data (a paper, a codebook, an institution's page) (PROV-1, PROV-8, [provenance.md](provenance.md)) |
| A good shape | comfortably above `Too Small` (about 1,000 units and 5 features or more, a first guess), with a mix of feature types or a grouped or temporal structure |
| A known risk (minus one) | a likely leak, heavy joins across tables, or an unclear target; once added, also an open issue that raises one of these or damage that may not be repairable, a duplicate, or the recommendation not to ship |

A rejected record (`No`) has no priority. The factors only order the queue: a record with priority 1 is still a
candidate, and a high priority never stands in for a check of the rules. Within one priority the review of added
datasets takes the record with the fewest open decisions first, so quick decisions do not wait behind long ones.

## Patterns

Quick ways to apply the rules; a pattern never overrides a rule, and the dataset at hand wins over the pattern. Each
gives the usual markers and verdict for a recurring signal. A signal is often in the name alone
(`*-recommendation-challenge`, `*-forecasting-*`).

### Read the comments first

Read the record's comments first and understand what they mean. They usually hold the decisive fact (the true
source, a leak mechanism, the setup). `jannis` looks like anonymised numeric columns, but its comment ("From AutoML
challenge ... SAIAPR-TC12") shows it is image-derived, so `Image`, `No` (SEL-13). `sonar`'s comment shows an outdated
handcrafted toy experiment: out on its setup (SEL-16), not merely on its acoustic features.

### Scope by the original task

Trace the original task (SEL-8). `yearprediction_the_million_song_dataset` is the trap: OpenML 4352 serves it as a
regression, but it is the Million Song Dataset Challenge, a song-recommendation task, so it is
`Out-of-scope Task (CTR/RecSys/Ranking)`, `No`, and the regression re-framings are duplicates.

Recommendation, ranking and CTR tasks are `Out-of-scope Task (CTR/RecSys/Ranking)`, `No` (SEL-9), also when a
mirror serves them as classification or regression.

### Forecasting or a temporal task

Future values of a series are `Time-series (Forecasting)`, `No` (SEL-10). A delay or a price as a fixed task with a
temporal split is in scope, and a forecasting-like panel is in scope when it passes the naive-profile test (SEL-11,
TP-10).

### Artificial, generated or simulated

Synthetic, toy, handmade or deterministic data, and simulated physics with its own benchmarks, are
`AHDS (Artifical/Handmade/Deterministic/Simulated)`, `No` (SEL-16; the detection is PROV-3).

### Non-tabular modality

Raw images, audio or text where modality models dominate are `Image`, `NLP (Text)` or
`Wrong Domain / Source Modality`, usually `No` (SEL-12). Vectorized features where tabular models are competitive can
be in scope.

Image-derived features (SEL-13) cover recognition sets (`letter`, `mfeat_*`, `gina`, `gtsrb_*`, `optdigits`,
`pendigits`, `usps`, `semeion`, `texture`, `one_hundred_plants_*`) and measured-from-image tables
(`magic_gamma_telescope` shower geometry, `wdbc` nuclei descriptors, `image_gesture_phase_segmentation`, `dry_bean`,
`raisin`, `pumpkin_seeds`, `rice`, `satimage`, `wilt`, `banknote_authentication`).

One more layer of abstraction is still image-derived (SEL-13):

* `internet_advertisements` "encode the geometry of the image (if available) as well as phrases occurring in the URL,
  the image's URL and alt text" (UCI): an is-this-an-ad-image task, `Image`, `No`.
* `breast_w`'s 1-10 cytology grades are a pathologist's scoring of cell morphology under a microscope: `No`.
* The exception (SEL-14, applying SEL-2): the BI-RADS assessment and density of a screening mammogram, which risk
  models such as the BCSC Risk Calculator combine with risk factors (`breast_cancer_prediction`), or the thallium-scan
  result of `heart_disease_cleveland`, stay in scope. `breast_w` stays out because its grades describe the slide for a
  call pathology makes from the image itself.

Measured attributes and signals (SEL-15): `wbcatt` (expert-annotated white-blood-cell morphology) sits on the
`breast_w` boundary and is kept only provisionally.
`infrared_thermography_temperature` (facial temperatures at fixed sites, read through a thermal camera used as a
thermometer, the target the same quantity by mouth) is a measurement under SEL-15, not image-derived.

### Duplicates and versions

A re-upload or processed copy of a known dataset is a `Duplicate` (PROV-4, PROV-5; [provenance.md](provenance.md) has
the method). Different cuts of one dataset are duplicates too when neither adds a distinct task (PROV-6;
`arsenic_male_lung` is the lung-cancer version of the same exposure data as `arsenic_male_bladder`). A shared source is
not a duplicate when it yields different tasks (PROV-7; `parkinsons_biomedical_voice_measurements` detects a disorder,
`telemonitoring_parkinsons_biomedical_voice_measurements` tracks its progression; `amex_iid` and `amex_non_iid` are
the IID and grouped versions of one competition).

### Survey and discovery tables

A table without a genuine predictive target is `No Good Target / Scientific Discovery`, `No` or `TBD -> 2nd Tier`
(SEL-3).

### Trivial, too small, empty

`Trivial` (one feature or a simple rule matches the best methods, or the task is solved perfectly) is `No` (TP-4), and
`Too Small` (a handful of units of a class per test fold) is `No` or `TBD -> 2nd Tier` (TP-5). Both need evidence from
the task's own splits; the rules are in [task_probes.md](task_probes.md). A small but real signal, or methods that tie
on a hard task, is not trivial and no reason to retire (TP-2). Under class imbalance, accuracy against the majority
class is no evidence in either direction ([evidence.md](evidence.md), EV-5; Lennart, 2026-09-23): judge learnability
with ROC AUC or log loss against the class prior, and fit a quick gradient-boosting model on the features known at
prediction time when the data loads (`us_accidents`: its published "78% accuracy" settled nothing).

### Selection bias

When the rows are not drawn from the population the use case predicts for, a class looks different than it would
there: cases and controls collected apart or in different periods (`hepatitis_c_prediction`, `website_phishing`), only
typical or confirmed cases (`sarcoma`; `superconductivity` holds only superconductors), a teaching or volunteer
collection (`audiology_diagnosis`, `obesity_estimation`), or objects picked for measurement when the use case predicts
for the objects that were not picked (`sdss_17`: picked by colour for a spectrum, classified without one). Mark it
`Selection Bias`; the verdict is usually still `Yes` (Andrej, 2026-10-20). It is a concern flag: name the gap in the
definition's `fit_reason`, give the evidence in the record (the class mix, or a feature against a reference series),
and judge the model comparison on the data, not on the marker. The marker does not by itself make the fit
approximate: the fit is direct when the real-world setting of the use case has the same bias, and approximate when it
does not (USE-8 in [use_case.md](use_case.md)). The marker stays either way, since it says something special about the
data (Lennart, 2026-10-27). `eryhemato_squamous_disease` is the example: 93% of its lichen planus patients have mouth
lesions and no other patient does, against 19% to 63% in clinic series; kept, with an approximate fit.

No marker when:

* the selection is how the label comes to exist, so every dataset of the task has it (only granted loans have a
  repayment outcome, Andrej 2026-10-15; only patients referred for angiography have its result,
  `heart_disease_cleveland`);
* one class was oversampled from the same population, which changes only the class shares (`credit_g`,
  `churn_telco_south_asia`);
* tested compounds stand for the candidates a screen would test (the QSAR sets): how far a new candidate lies from the
  tested ones is a question for the split;
* the rows come from another population altogether (`pancreatic_cancer_mouse_detection`: mice of one lab for
  patients), a question of the use-case fit.

`Not Representative` is a different flag: the task or its setup is not the real application (features practitioners no
longer use, a prediction no decision rests on). A record carries both when both hold (`audiology_diagnosis`). The
clause on objects picked for measurement and the cases without a marker were added on the review of PR #16 (Lennart,
2026-10-27).

### Leakage and irreversible damage

A feature that is the output of a supervised transform fit on the whole dataset (a discriminant-analysis score, a
target or mean encoding, a model's own prediction) bakes label information into every row and cannot be recomputed
per split: `Data Quality Issue`, `No` (LEAK-27, [leak_checks.md](leak_checks.md)). `yeast` ships a "Score of
discriminant analysis of the amino acid content of vacuolar and extracellular proteins", fit on the full dataset.

An unsupervised transform over all rows (z-scores, min-max, a quantile transform, RMA, PCA, batch correction) is a
weak leak and no reason for `No` on its own, unless a strong leak is suspected (Lennart, 2026-10-19): rebuild or note
it as LEAK-30 in [leak_checks.md](leak_checks.md) says (coad_colon_adenocarcinoma, retired for a rebuild from the GDC).

### Ethics, licence

An ethical concern (sensitive use, creators who ask that the data not be used for ML) is `Ethical Issue`, `No`
(SEL-1). A licence or redistribution restriction is no reason and no marker: note it (what the terms are and where
they are stated) and triage the data on its merits ([evidence.md](evidence.md), EV-4).

### Anonymized data

When the source hid what the features are, by replacing their names or values on purpose, we cannot check what a
column measures, whether it is known at the prediction point, or rule out a leak: symbols (`credit_approval`: Quinlan
replaced all names and values), `var_<n>` (the Santander competitions), coded sensor names (`aps_failure`), unnamed
descriptors (`bioresponse`, `hiva_agnostic`). Mark the record `Anonymized`, set `data_tags = ("Anonymized",)` in its
definition ([definitions.md](../../knowledge-data-foundry/references/definitions.md)), and say in a comment what
could not be determined; the marker and the tag go together (Andrej, 2026-10-20). The marker flags what the data
cannot tell us, not a defect: it is no reason for `No` by itself, and the verdict comes from what can be checked (the
source, the task, the probes; masked fields that may be post-outcome are LEAK-32 and LEAK-38 in
[leak_checks.md](leak_checks.md)).

No marker when:

* the source documents the codes: decode them (CLEAN-12 in [cleaning_features.md](cleaning_features.md));
* only ids were replaced while the features keep their meaning (a patient, customer or molecule id);
* every column is described and only the values of some categories are codes (`amazon_employee_access`: role and
  department ids; `home_credit_default_stability`: district, employer or contract status as masked codes, each column
  defined in the competition's `feature_definitions.csv`);
* the features are numbered measurements of a documented kind (`musk`: distances along rays; spectrum bins;
  fingerprint bits such as `ecfp_<n>`).

The cases without a marker were added on the review of PR #17 (Lennart, 2026-10-27).

### Clear cases

A genuine real-world tabular classification or regression task with a clear target and adequate size is `Yes` (well
known, strong) or `TBD -> Yes` (plausible, unverified).

### Unknown or unclear source

When following every link ends at an anonymous re-upload with no documentation and no traceable upstream (paper,
competition, institution, an identifiable first uploader), we cannot tell what the data is:
`Missing source information`, `No` (PROV-1, [provenance.md](provenance.md); `water_quality_and_potability`,
`3d_estimation_using_rssi_of_wlan_dataset_complete_1_target`, `calendardow`). A live link is not a known source. A
source that is plausible but unclear in a detail stays, with a note of what to clarify (PROV-2;
bad_customer_detection; Lennart, 2026-10-14). An upload whose first platform cannot be traced stays for now, case by
case, when the data passes PROV-3 and there is a source to point to; the gap goes into an approximate fit with a note
(PROV-2 as amended, Lennart, 2026-10-21; tour_travels_churn, mobile_churn).

A record with too little information while the dataset's origin is known (a bare link, no description) is not
rejected for that (PROV-2): use `TBD -> Yes` or `TBD -> 2nd Tier` and write down what to inspect (the size after
cleaning, the real target, the split).

## Verdicts and markers

### Verdict values

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

### Reading decision markers and optional fields

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
  (CLEAN-18 in [cleaning_features.md](cleaning_features.md); caracas_cervical_cancer: four results from one work-up,
  the folder predicts the biopsy; Lennart, 2026-10-15).

### Decision markers

The 25 decision markers of the vocabulary, spelled as there. "None" means no rule of the curation files leads to the
marker; its meaning comes from its name and how records use it, and the comments say why a record carries it. A state
marker records where a record stands, not an issue of the data.

| Marker | Meaning | Rule |
|---|---|---|
| `Wrong Domain / Source Modality` | the data comes from another modality or domain (images, audio, signals, control), where other models are the tool | SEL-12 |
| `AHDS (Artifical/Handmade/Deterministic/Simulated)` | artificial, handmade, deterministic or simulated data, including generated tables | SEL-16; PROV-3 ([provenance.md](provenance.md), "Is the data generated?") |
| `Duplicate` | a re-upload, processed copy or cut of a recorded dataset that adds no distinct task | PROV-4 to PROV-7 ([provenance.md](provenance.md)) |
| `Missing source information` | no traceable first source after a thorough search | PROV-1 (PROV-2 for a source unclear only in a detail; [provenance.md](provenance.md)) |
| `Time-series (Classification)` | classification of a series or signal (readings over time, a recording), where time-series models are the tool | none (SEL-12 on vectorized time-series data) |
| `Outdated` | an old dataset or experiment: today the task would use other data, features or models | none |
| `No Good Target (yet)` | real data without a predictive target so far (a listing, a survey, a table built for another purpose); one may be defined later, and such records mostly wait as `TBD -> 2nd Tier` | none |
| `No Good Target / Scientific Discovery` | no genuine predictive target: a discovery, survey or look-back table, a label no decision fits | SEL-3, SEL-4, SEL-6, SEL-7; USE-2, USE-8 ([use_case.md](use_case.md)) |
| `Data Quality Issue` | damage that cannot be undone or repaired: a supervised transform fit on the whole labelled set, a manipulated real table | LEAK-27 ([leak_checks.md](leak_checks.md)); PROV-3 ([provenance.md](provenance.md)) |
| `Trivial` | one feature or a simple rule matches the best methods, or the task is solved perfectly | TP-4; SEL-5 |
| `Image` | an image or video task, including features computed from an image to describe its content | SEL-12, SEL-13 |
| `Time-series (Forecasting)` | future values of a series over a horizon | SEL-10 |
| `NLP (Text)` | a raw-text task where language models dominate | SEL-12 |
| `Needs extensive data wrangling` | the release is far from one task table (tables to join, a target to build, a collection to split into datasets); an effort flag, found on `Yes` records too | none |
| `Out-of-scope Task (CTR/RecSys/Ranking)` | a recommendation, ranking, click-through-rate or information-retrieval task | SEL-9 (SEL-8) |
| `Ethical Issue` | an ethical concern, such as subjects or creators who object to ML use | SEL-1 |
| `Too Small` | a handful of units of a class per test fold and in total | TP-5 (TP-8 for a short class, TP-9 for the windows of a temporal task) |
| `Not Representative` | the task or its setup does not represent the real application (features practitioners no longer use for the task, a prediction no decision rests on); a selective sample is `Selection Bias` | none |
| `Selection Bias` | the rows are not drawn from the population the use case predicts for (cases and controls collected apart, only typical or confirmed cases, a volunteer or teaching collection, objects picked for measurement when the use case predicts for the others); a concern flag, usually on `Yes` records | none (Patterns, "Selection bias") |
| `Anonymized` | feature names or values replaced on purpose (symbols, `var_<n>`, hashed codes), so what a column measures, its timing and leaks cannot be checked; a concern flag, no exclusion reason; goes with the definition's `Anonymized` data tag | none (Patterns, "Anonymized data") |
| `Not Available (from Paper))` | a paper's data that is not public and cannot be obtained | none |
| `Data Requested` | state marker: the data or its source was requested from the authors or owners, and the answer is pending | none |
| `Time-series (Regression)` | regression on a stream of readings (hourly or per-minute measurements), between a temporal task and forecasting | none (SEL-10 and SEL-11 decide which; SPLIT-7 in [splits.md](splits.md) when no timestamp survived) |
| `Robotics (RL)` | data of a control task (a robot arm, an aircraft), solved with control or reinforcement learning rather than as a prediction | none |
| `TBD` | state marker: the markers are still to be decided; found on `TBD -> Yes` and `TBD -> 2nd Tier` records | none |

## Cases

Precedents: how a rule was applied. They never change a rule; an exception is listed with the fact that set it apart.

| Rule | Dataset | Decision (date, curator) | Kind |
|---|---|---|---|
| SEL-1 | Pima Indian Diabetes Dataset | out: its subjects or creators ask that it not be used for ML | applied |
| SEL-4 | brca_breast_cancer, glioblastoma, ov_ovarian_cancer | labels are molecular subtypes defined by clustering: no real predictive task (2026-10-12, Lennart) | applied |
| SEL-5 | account_debt_south_africa | the deterministic rule's inputs dropped; the rest still makes a real task | applied |
| SEL-5 | central_international_medical_college_and_hospital_health_risk_prediction | the label is NEWS2, and its inputs are the whole task: `Trivial` | applied |
| SEL-6 | analcatdata_supreme | Congress's responses in 1979-1988 to Supreme Court rulings of 1953-1988, counted over one shared window: `No Good Target / Scientific Discovery` (2026-10-14, Lennart) | applied |
| SEL-7 | cdc_diabetes_health_indicators | "ever told you have diabetes", told a median of 10 years earlier, with the undiagnosed in the negative class (2026-10-15, Lennart) | applied |
| SEL-7 | stroke_prediction | a stroke the patient already had, undated, in a hackathon release rather than an interview: retired as cdc_diabetes_health_indicators, since no decision is made with it (a screening task would need a first stroke within a horizon, from dated records); with `Data Quality Issue` for the columns that look generated; SEL-7 not amended (2026-10-26, Lennart: "This looks too bad, dont ship it") | applied |
| SEL-8, SEL-9 | yearprediction_the_million_song_dataset | the Million Song Dataset Challenge, a song-recommendation task, though OpenML 4352 serves it as a regression; the regression re-framings are duplicates | applied |
| SEL-13 | internet_advertisements, breast_w | image descriptors with a few non-visual columns, and a pathologist's grades of a slide: `No` | applied |
| SEL-14 (SEL-2) | breast_cancer_prediction, heart_disease_cleveland | the BI-RADS assessment and density, and the thallium-scan result, stay inputs: tabular models use them in practice | applied |
| SEL-15 | wbcatt | expert-annotated white-blood-cell morphology, on the `breast_w` boundary: kept only provisionally | applied |
| SEL-15 | infrared_thermography_temperature | blackbody-compensated facial temperatures at named sites, read through a thermal camera used as a thermometer, the target the same quantity by mouth: kept as a measurement, not an image descriptor; the counter-cases satimage and wilt hold values that recognise image content (SEL-13) (2026-10-21, Lennart) | applied |
| SEL-16 | Higgs, sonar | simulated physics with its own benchmarks; an outdated handcrafted toy experiment: out | applied |
| EV-4 | lucas_topsoil | JRC's terms forbid redistribution; the record is still triaged on what the survey measures | applied |
| EV-5 | us_accidents | its published "78% accuracy" settled nothing | applied |
| LEAK-27 ([leak_checks.md](leak_checks.md)) | yeast | a discriminant-analysis score fit on the full dataset: `Data Quality Issue`, `No` | applied |
| LEAK-30 ([leak_checks.md](leak_checks.md)), PROV-13 | coad_colon_adenocarcinoma | values scaled over all rows: retired for a rebuild from the GDC | applied |

The cases of the former SEL-17 are under PROV-1 and PROV-2 in [provenance.md](provenance.md), Cases.

## In Data Foundry

The verdicts, markers and tags are fields of the curation record, with their vocabulary, the ship invariant and the
review queue: [records.md](../../knowledge-data-foundry/references/records.md).
