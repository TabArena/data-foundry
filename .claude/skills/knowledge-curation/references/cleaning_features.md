# Cleaning and features

How we process a dataset we keep: the cleaning an expert would ship, the encodings to undo, the dtypes, and which
features we build or leave alone. Adapted from the TabArena paper (Appendix B.3) and the curators' decisions. Leaks
are in [leak_checks.md](leak_checks.md); the rows a use case never sees in [use_case.md](use_case.md).

## Clean to the state an expert would ship

Read what the source's top solutions and the data owners did (unit fixes, removed anomalies, a published list of bad
rows), adopt the rules that hold for the train and the test period alike, and check them against such a list where
one exists. Keep what a model can learn (a plant switched off for the season). ashrae_great_energy_predictor_iii
(2026-10-15): the readings in kWh from the data owners' raw release (the competition kept each site's own unit), and
meters at 0 for 48 hours or more in their operating season and readings stuck for a week or more dropped; 94.5% of the
2016 rows dropped are on the first-place team's hand-made list of bad readings.

* Copy the top solutions' preprocessing, not their exploits: no step that uses a test-set leak, a metric quirk or a
  feature computed over all rows with their labels, even when it won the competition (santander's `has_one`).
* One unit and one scale per column. When a feature's scale changes over time, put it on one scale the way an analyst
  would at the time, with the conversion the source or the measuring body publishes. college_scorecard: the SAT was
  redesigned in 2016, so from the 2017 cohort on an institution's scores jump while its students stay the same; the
  College Board's concordance tables put SATMT25, SATMT75 and SAT_AVG back on the old scale (median change 2016 to
  2017 within an institution: 0 instead of +30; Lennart, 2026-10-16). A section without a conversion table stays
  dropped.
* Drop uninformative identifiers (row ids, storage artefacts). Keep an identifier that carries meaning (a time index,
  a group id) and process it into that meaning. Hide the names behind a stable id when they are personal, never a
  random one.
* Drop constant columns, all-missing columns and exact copies of another column.

## Missing, impossible and proxy values

* Convert proxy missing values (`?`, an empty string, `-1`, `-9`, `-999`, `999999`, `365243`) to real missing values
  when the encoding can be inferred from the description and the context. Keep a code and say why when it means
  something ("not previously contacted").
* Impossible values become missing, and the row stays: a first intercourse after the current age, an STD diagnosed
  longer ago than the patient's age (caracas_cervical_cancer), a negative network age or an undocumented code
  (churn_telco_south_asia), `chol == 0` (heart_disease_va_long_beach), `age = 455` (thyroid_discordant), `-9999`
  (sdss_17). Values that are only unusual stay. A row leaves only when it is no task row ([use_case.md](use_case.md))
  or a copy ([leak_checks.md](leak_checks.md), section 5).
* Rows that are a sentinel in every feature (heloc: 588 rows of `-9`, no bureau record) are a decision of their own:
  they can be the real population (an applicant without a credit file) or empty records.

## Undo destroyed meaning

Reverse ordinal codes and one-hot blocks into categories with their labels, join dates split across columns, and
split ids that encode a group and a session. This kind of reconstruction is always welcome.

A block is one-hot only when every row has exactly one flag set. Yes/no flags that can be set together are
multi-label answers and stay separate columns (caracas_cervical_cancer: each STD type is its own question, and 9
patients have two or three; one category per flag is the lossless form, since one category of combinations would
need 14 levels, 9 of them with 1-3 patients; Lennart, 2026-10-15).

## Dtypes by meaning

* Categorical for a fixed, finite set of values (inferred from the description and the context), string for free text
  and high-cardinality values, datetime for dates (`YYYY-MM-DD` where possible; reconstruct numerically encoded dates
  as far as the information allows), numeric for everything else. No untyped object column survives.
* A molecule's structure (SMILES) ships as RDKit's 2D descriptors from one pinned RDKit for every dataset, and the
  SMILES string is dropped; descriptors the source ships stay next to them. As text the SMILES adds nothing to the
  descriptors (2026-10-14: -0.025 to +0.010 ROC AUC on apistox, drug_induced_autoimmunity_prediction and
  qsar_bioconcentration), and the benchmark needs no chemistry step of its own. Check for rows that become copies
  once the stereochemistry is gone (stereoisomers share every 2D descriptor).

## The target

* Log a skewed positive target (prices, durations, counts) when the source has not, case by case, and name the
  column after the transform (`log_days_to_death`).
* Drop rows with a missing target.
* Keep rare classes of the source's labels; a short class is a question about that class, not about the task
  ([task_probes.md](task_probes.md), rule 8). Merge classes only by an established convention of the field and test
  the merge (rule 7; audiology_diagnosis).
* Remove a `Multi-target` tag when the dataset predicts one target ([selection.md](selection.md)).

## Features we build, and features we leave to the model

The benchmark's pipeline encodes categories, imputes, scales and embeds text, so we do not: no one-hot encoding, no
imputation, no scaling, no hand-made text features, no geocoding of place names.

We build features when one of these holds:

* It removes a leak with the least loss of information (a same-day value lagged by one period;
  [leak_checks.md](leak_checks.md)).
* It restores meaning the source destroyed (above).
* It is what a data scientist on this task would build, because the raw data cannot be used as it is: a transaction
  log or a history aggregated to one row per prediction. Take the features the top solutions share.
  alfa_battle_2_0_task_2: the features the 1st, 4th and 9th place solutions have in common (513 aggregates over the
  restored ruble amounts) replace the organisers' 127 (untuned LightGBM 0.787 / 0.771 / 0.772 against 0.774 / 0.757 /
  0.763 on the three windows; Lennart, 2026-10-13).

Never build features from the labels (target or mean encodings, label-based counts), learned embeddings or another
model's scores, and never compute a feature value from statistics over all rows: take a statistic from the history
before the oldest test window, or drop the feature (sf_permit_time, home_credit_default_risk; Lennart, 2026-10-19).
Choosing which columns or categories to keep by counts over the whole table is ordinary cleaning (in a temporal task,
say it is a pipeline choice that approximates the task).

## Keep every relevant feature

Width is no reason to drop a block or to propose a narrower version, and no model's input limit or runtime is an
argument in a curation decision or a probe (Lennart, 2026-10-15: coad_colon_adenocarcinoma ships 36,355 features; its
report had weighed one model's 50,000-feature cap). Columns leave for what they are (a leak, an identifier, a copy, the
measurement that defines the label), never for how many there are.

## Order

The rows of an IID or grouped task are shuffled with a fixed seed so no method can exploit their order, and the rows
of a temporal task are sorted by the time index. The stored columns are not shuffled: the benchmark permutes the
feature order when it runs.

## In Data Foundry

The order of these steps in `_clean`, the helpers (`drop_columns`, `rdkit_descriptors`, `anonymize_ids`) and the
bundle checks that catch what is missed: [definitions.md](../../knowledge-data-foundry/references/definitions.md),
"The preprocessing recipe".
