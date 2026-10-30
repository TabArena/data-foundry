# Cleaning and features

Part 7 of the curation rules, under P7 (The expert state) in [principles.md](principles.md). The rules of earlier parts
win over this file's rules in a conflict; within this file a rule wins over the rules below it of the same strength.
How to weigh, exceptions and amendments: [principles.md](principles.md).

How we process a dataset we keep: the cleaning an expert would ship, the encodings to undo, the dtypes, and which
features we build or leave alone. Adapted from the TabArena paper (Appendix B.3) and the curators' decisions. Leaks
are in [leak_checks.md](leak_checks.md); the rows a use case never sees in USE-7 of [use_case.md](use_case.md).
Damaged data is repaired or rebuilt from its origin before it is cleaned around: PROV-13 in
[provenance.md](provenance.md).

This is the lowest-ranked part. A quality problem is fixed when the fix is cheap and safe; otherwise it is kept with a
note. A very real task (P3) carries cleaning imperfections when they are written down (Lennart's example for the order
of the principles). Some rules here protect validity and stay Must: never build features from the labels, learned
embeddings or another model's scores (CLEAN-6), never compute a feature value from statistics over all rows (CLEAN-7,
applying LEAK-29), and no untyped object column survives (CLEAN-9).

## Rules

### The expert state

**CLEAN-1 (Should).** Clean to the state an expert would ship. Read what the source's top solutions and the data
owners did (unit fixes, removed anomalies, a published list of bad rows), adopt the rules that hold for the train and
the test period alike, and check them against such a list where one exists. Keep what a model can learn (a plant
switched off for the season). Cases: ashrae_great_energy_predictor_iii (2026-10-15).

**CLEAN-2 (Must).** Leave to the benchmark's pipeline what it does. The pipeline encodes categories, imputes, scales
and embeds text, so we do not: no one-hot encoding, no imputation, no scaling, no hand-made text features, no geocoding
of place names.

**CLEAN-3 (Should).** Drop uninformative identifiers (row ids, storage artefacts). Keep an identifier that carries
meaning (a time index, a group id) and process it into that meaning.

**CLEAN-4 (Must).** Hide the names behind a stable id when they are personal, never behind a random one.

**CLEAN-5 (Should).** Drop constant columns, all-missing columns and exact copies of another column.

### Validity guards

**CLEAN-6 (Must).** Never build features from the labels (target or mean encodings, label-based counts), learned
embeddings or another model's scores.

**CLEAN-7 (Must; applies LEAK-29).** Never compute a feature value from statistics over all rows: take the statistic
from the history before the oldest test window, or drop the feature (LEAK-29 in [leak_checks.md](leak_checks.md), with
its cases; a column the source already scaled is LEAK-30).

**CLEAN-8 (Must; narrows CLEAN-7).** Choosing which columns or categories to keep by counts over the whole table (the
most frequent codes, questions asked in one year only) is ordinary cleaning that follows the task's best practice. In a
temporal task, say that it is a pipeline choice that approximates the task. Cases: rosbank1, alfa_battle_2_0_task_2,
anes_voting_2026 (Lennart, 2026-10-19).

**CLEAN-9 (Must).** No untyped object column survives: every column gets a dtype by its meaning (CLEAN-14).

### Missing, impossible and proxy values

**CLEAN-10 (Should).** Convert proxy missing values (`?`, an empty string, `-1`, `-9`, `-999`, `999999`, `365243`) to
real missing values when the encoding can be inferred from the description and the context. Keep a code and say why
when it means something ("not previously contacted").

**CLEAN-11 (Should; amended 2026-10-21, Lennart, on ames_housing, mercedes_benz_greener_manufacturing and
qsar_tid_11).** Impossible values become missing, and the row stays. Values that are only unusual stay. A row leaves
only when it is no task row (USE-7, [use_case.md](use_case.md)) or a copy ([leak_checks.md](leak_checks.md), Copies
across the split (LEAK-16 to LEAK-21)). A row whose target the source names as not the task's quantity may leave, with
the source's words. A single extreme target in the training period only may leave with the source's words or where
experts of the field drop such a value by default, decided case by case. Rows that are a sentinel in every
feature are a decision of their own (Weighed factors). Cases: caracas_cervical_cancer, churn_telco_south_asia,
heart_disease, thyroid_discordant, sdss_17, ames_housing, mercedes_benz_greener_manufacturing,
qsar_tid_11.

### Undo destroyed meaning

**CLEAN-12 (Should).** Reverse ordinal codes and one-hot blocks into categories with their labels, join dates split
across columns, and split ids that encode a group and a session. This kind of reconstruction is always welcome.

**CLEAN-13 (Must; narrows CLEAN-12; amended 2026-10-22, Lennart, on mortgage and onlinenewspopularity).** A block is
one-hot only when every row has exactly one flag set, or at most one with a reference level: the rows with no flag set
become one more category (such as `other`), and the merge stays lossless. Yes/no flags that can be set together are
multi-label answers and stay separate columns; one column per flag is the lossless form. Cases:
caracas_cervical_cancer (Lennart, 2026-10-15); mortgage, onlinenewspopularity (reference level, 2026-10-22).

### Dtypes by meaning

**CLEAN-14 (Should; amended 2026-10-21, Lennart, on qsar_oral_toxicity, hiva_agnostic and qsar_tid_11, then on
every 0/1 flag of the working copy: "we should have one clear way to treat 0/1 flags"; amended again the same day,
when the literal reading had typed counts and anonymized descriptors categorical: "no if we can infer from the
semantic context, keep it a number, this is a real-world bias. We want to make things categorical if we know from the
context they are indeed such"; amended 2026-10-30, Lennart, on bank_marketing and qsar_biodeg: "ordinal scales are
case-by-case, they could be either but generally we know they are not numeric so categorical might be the safer
bet").** Categorical for a fixed, finite set of values (inferred from the description and the
context), string for free text and high-cardinality values, datetime for dates (`YYYY-MM-DD` where possible;
reconstruct numerically encoded dates as far as the information allows), numeric for everything else. A 0/1 column is
categorical when its meaning (the codebook, its name, the source) says it is a yes/no flag (`waterfront`,
`IsOnlineSale`, `FLAG_DOCUMENT_2`, a fingerprint bit), after checking on the data that it holds only 0 and 1 (plus
missing values); a boolean column too. A count or a measured quantity stays numeric even when only 0 and 1 occur (an
RDKit fragment count, `NoOfURLRedirect`, `mosque_count_500`, an aggregate over a history). With no semantic context
(anonymized or opaque descriptors) a 0/1 column stays as the source ships it, numeric. A constant column is no flag.
An ordinal scale (a grade, a stage, binned ranges, answers on a survey scale) is no measured quantity: it is decided
case by case, categorical by default. A column whose meaning is unknown is looked up (the codebook, the paper, the
descriptor software's manual) before it is typed: qsar_biodeg's two atom-centred fragments were typed categorical as
"no idea what this might be", and they are counts. Test: the dtype probe (`dtype_probes.py`,
[checks_and_probes.md](../../knowledge-data-foundry/references/checks_and_probes.md)) lists the columns whose dtype
disagrees with their values, their name or the source's codebook; the meaning decides.

### The target

**CLEAN-15 (Must).** Drop rows with a missing target.

**CLEAN-16 (Should).** Log a skewed positive target (prices, durations, counts) when the source has not, case by case,
and name the column after the transform (`log_days_to_death`).

**CLEAN-17 (Should).** Keep rare classes of the source's labels (TP-8), and merge classes only by an established
convention of the field, with the merge tested (TP-7): [task_probes.md](task_probes.md). Cases: audiology_diagnosis, force_2020 (a class in one group only).

**CLEAN-18 (Should).** Remove a `Multi-target` tag when the dataset predicts one target ([selection.md](selection.md),
"Reading decision markers and optional fields").

### Features we build

**CLEAN-19 (Should).** We build a feature when one of these holds:

* It removes a leak with the least loss of information (a same-day value lagged by one period; LEAK-7 in
  [leak_checks.md](leak_checks.md)).
* It restores meaning the source destroyed (CLEAN-12).
* It is what a data scientist on this task would build, because the raw data cannot be used as it is: a transaction
  log or a history aggregated to one row per prediction. Take the best of the organizers' or a published baseline and
  the top solutions' features, or a reasonable combination of them, not their union (amended 2026-10-21, Lennart, on
  alfa_battle_2_0_task_2 and rosbank1: "we want to take the best of both, or a reasonable combination, and not a
  union. so here we take the best for alfa as it is the top-solution").
* It is an input the actor reads at the prediction point from other rows of the same release, such as the other
  stations' readings of the same morning, kept only where they are known by then (amended 2026-10-26, Lennart, on
  rain_in_australia: "add the features to do this task as it looks good with only 9am is not later setting").

Cases: alfa_battle_2_0_task_2 (Lennart, 2026-10-13; reason added 2026-10-21), rain_in_australia (2026-10-26),
african_credit_scoring_challenge and rosbank1 (2026-10-26). Exceptions (a per-entity history kept as rows that a row model uses):
amex_non_iid (2026-10-02), fraud_detection_in_electricity_and_gas_consumption_1m (2026-10-26).

**CLEAN-20 (Must).** Copy the top solutions' preprocessing, not their exploits: no step that uses a test-set leak, a
metric quirk or a feature computed over all rows with their labels (LEAK-28), even when it won the competition. Cases:
santander_customer_transaction_prediction.

**CLEAN-21 (Should).** One unit and one scale per column. When a feature's scale changes over time, put it on one
scale the way an analyst would at the time, with the conversion the source or the measuring body publishes. Cases:
college_scorecard (Lennart, 2026-10-16), rosbank1 (exchange rates of the central bank, 2026-10-26).

### Keep every relevant feature

**CLEAN-22 (Must).** Columns leave for what they are (a leak, an identifier, a copy, the measurement that defines the
label), never for how many there are. Width is no reason to drop a block or to propose a narrower version. A model's
input limit or runtime is no argument in a curation decision or a probe: EV-4 in [evidence.md](evidence.md). Cases:
coad_colon_adenocarcinoma (Lennart, 2026-10-15).

### Order

**CLEAN-23 (Must).** The rows of an IID or grouped task are shuffled with a fixed seed so no method can exploit their
order, and the rows of a temporal task are sorted by the time index. Never shuffle the stored columns: the benchmark
permutes the feature order when it runs.

### Molecules

**CLEAN-24 (Should).** A molecule's structure (SMILES) ships as RDKit's 2D descriptors from one pinned RDKit for every
dataset, and the SMILES string is dropped; descriptors the source ships stay next to them. As text the SMILES adds
nothing to the descriptors, and the benchmark needs no chemistry step of its own. Check for rows that become copies
once the stereochemistry is gone (stereoisomers share every 2D descriptor). Cases: apistox,
drug_induced_autoimmunity_prediction, qsar_bioconcentration (2026-10-14).

## Weighed factors

* **Rows that are a sentinel in every feature** (keep or drop): they can be the real population (an applicant without
  a credit file) or empty records. heloc: 588 rows of `-9`, no bureau record.

## Cases

Precedents: how a rule was applied. They never change a rule; an exception is listed with the fact that set it apart.

| Rule | Dataset | Decision (date, curator) | Kind |
|---|---|---|---|
| CLEAN-1 | ashrae_great_energy_predictor_iii | the readings in kWh from the data owners' raw release (the competition kept each site's own unit); meters at 0 for 48 hours or more in their operating season and readings stuck for a week or more dropped; 94.5% of the 2016 rows dropped are on the first-place team's hand-made list of bad readings (2026-10-15) | applied |
| CLEAN-2 | nyc_taxi_trip_duration_1m, pkdd_15_taxi_trip_time_prediction_ii_1m | no hour column, though the pickup hour carries much of the signal (nyc: LightGBM RMSE 0.357-0.381 with the hour, 0.414-0.441 with AutoGluon's date parts): a datetime's encoding is the pipeline's, and the v0.2 runs keep the hour; nothing to change while they do (2026-10-21, Lennart) | applied |
| CLEAN-7 | sf_permit_time, home_credit_default_risk | under LEAK-29 in [leak_checks.md](leak_checks.md), Cases | applied |
| CLEAN-8 | rosbank1, alfa_battle_2_0_task_2, anes_voting_2026 | columns or categories kept by counts over the whole table, as ordinary cleaning (2026-10-19, Lennart) | applied |
| CLEAN-10 | house_sales | `yr_renovated` = 0 ("never renovated" in the source) set to missing, so missing means never renovated; the fact that sets it apart from bank_marketing's `pdays = -1` and ames_housing's no-remodel coding: a 0 in a year column misleads a linear model as a year, and after the as-of-sale rebuild missing has no other meaning in the column (2026-10-22, Lennart) | exception |
| CLEAN-11 | caracas_cervical_cancer | a first intercourse after the current age, an STD diagnosed longer ago than the patient's age: missing | applied |
| CLEAN-11 | churn_telco_south_asia | a negative network age or an undocumented code: missing | applied |
| CLEAN-11 | heart_disease (Long Beach, first as heart_disease_va_long_beach) | `chol == 0`: missing | applied |
| CLEAN-11 | thyroid_discordant | `age = 455`: missing | applied |
| CLEAN-11 | sdss_17 | `-9999`: missing | applied |
| CLEAN-11 | ames_housing (record house_prices_nominal until 2026-10-26) | De Cock's three partial sales over 4,000 sq ft, which he calls "Partial Sales that likely don't represent actual market values" (2011, p. 4), all in the training rows: dropped with his words; the case that prompted the amendment (2026-10-21, Lennart) | applied |
| CLEAN-11 | mercedes_benz_greener_manufacturing | one testing time of 265.3 s against a next highest of 169.9 s (mean 100.7, sd 12.7), car 883 of 4,209 in ID order, inside the first 1,000 cars that every window trains on: dropped as a single extreme target in the training period only; the competition host does not name it; it leaves as the field's default for a single extreme time (the curator's call; the competition's public exploration notebook points it out as the one outlier); the case that made the second clause "the source's words or the experts' default, case by case" (2026-10-21, Lennart) | applied |
| CLEAN-11 | qsar_tid_11 | one pXC50 of -6.24, a half-effect concentration of about 1.7 million mol/L: impossible, so the target is missing and the row leaves by CLEAN-15; the training-period clause does not apply to a random split (2026-10-21, Lennart) | applied |
| CLEAN-11 | mortgage | 38 balances that put the source's own LTV above 300% (570,000 on an original 60,495): impossible, missing before lagging, so the 37 lagged LTVs above 300% and the balances and ratios built from them are missing (2026-10-22, Lennart) | applied |
| CLEAN-12 | perth_house_prices | a `UNIT` flag from the address's unit number ("10/23 ..."), the property type the upload dropped; `ADDRESS` kept as text; the first flag derived from free text (2026-10-26, Lennart) | applied |
| CLEAN-13 | caracas_cervical_cancer | each STD type is its own question, and 9 patients have two or three: one category per flag; one category of combinations would need 14 levels, 9 of them with 1-3 patients (2026-10-15, Lennart) | applied |
| CLEAN-13 | mortgage, onlinenewspopularity | `real_estate_type` (three property flags, 19.5% of rows with none) and `data_channel` (six channel flags) merged into one category with the reference level `other` for rows with no flag; at most one flag is set in every row, so the merge is lossless (2026-10-22, Lennart; the rule's wording amended) | applied |
| CLEAN-14 | qsar_oral_toxicity, hiva_agnostic, qsar_tid_11 | fingerprint bits and binary structure descriptors, checked to hold only 0 and 1, typed categorical (int64, category and float64 before) (2026-10-21, Lennart) | applied |
| CLEAN-14 | every 0/1 flag of the working copy (35 definitions, e.g. framingham_heart_study_fhs, phiusil_phishing, bioresponse, home_credit_default_risk, zillow_prize) | first applied on the data: every feature holding only 0 and 1 typed categorical, counts and anonymized descriptors included; revised the same day by meaning: flags kept categorical (`waterfront`, `male`, `Promo`, `FLAG_DOCUMENT_*`, santander's `ind_var*` indicators, zillow's presence flags), counts reverted to numeric (RDKit fragment counts, `NoOfURLRedirect`, `mosque_count_*`, coil_2000's policy counts, cardiotocography's `DS`, home credit aggregates), anonymized descriptors reverted (amex_non_iid_1m, ieee_fraud_detection's V columns, bioresponse, homesite_quote_conversion's fields); the case that prompted the second amendment (2026-10-21, Lennart) | applied |
| CLEAN-14 | zillow_prize | the census tract-and-block code as one categorical `census_tract` (11-digit tract ID, 3,030 levels); the block group and block parts (8,334 and 55,601 levels) dropped as near-identifiers, the county part being `fips` (2026-10-26, Lennart) | applied |
| CLEAN-14 | bank_marketing | `campaign` and `previous`, the contacts with a client in this and in earlier campaigns (1-63 and 0-275), typed categorical by the BeyondArena notebook (48 and 41 levels): counts, so numeric, as the UCI description gives them; the 0/1 sweep of 2026-10-21 looked only at columns holding 0 and 1 (2026-10-30, Lennart, issue #34) | applied |
| CLEAN-14 | qsar_biodeg | `N073_chemical_substructure` and `C026_chemical_substructure`, the atom-centred fragments N-073 and C-026 (counts of atoms of that type, 0-3 and 0-12), typed categorical while their meaning was unknown: counts, so numeric; found by the dtype probe's sweep (2026-10-30, Lennart) | applied |
| CLEAN-17 | audiology_diagnosis | classes merged by a convention of the field, and the merge tested (TP-7) | applied |
| CLEAN-17 | force_2020_well_well_log_and_lithofacies_dataset_for_machine_learning_competition | the Basement class (103 rows, all in well 16/4-1) dropped: a class that lives in one group cannot be on the train and the test side of a split by that group; the other 11 classes occur in at least 4 wells; the first class dropped for living in one group (2026-10-21, Lennart) | applied |
| CLEAN-19 | alfa_battle_2_0_task_2 | the features the 1st, 4th and 9th place solutions have in common (513 aggregates over the restored ruble amounts) replace the organisers' 127 (untuned LightGBM 0.787 / 0.771 / 0.772 against 0.774 / 0.757 / 0.763 on the three windows) (2026-10-13, Lennart); the top solutions' features are the better of the two, so they are taken and not merged with the organisers' (CLEAN-19 as amended 2026-10-21, Lennart) | applied |
| CLEAN-19 | mortgage | a column joined from outside the source: Freddie Mac's 30-year mortgage rate (FRED MORTGAGE30US), the mean of the previous calendar quarter, and the loan's lagged rate minus it (the refinance incentive a payoff model uses); dated periods make the join exact; the first such join, so siblings with dated periods take the same treatment (2026-10-22, Lennart) | applied |
| CLEAN-19 | rain_in_australia | the other locations' 9 am Rainfall, Pressure9am and Humidity9am of the same day (143 columns), each kept only where that location's 9 am comes no later than the row's own under both clock and standard time; ROC AUC 0.850 to 0.870 on the 9 windows then shipped (paired SE 0.0045, better in 8 of 9) (2026-10-26, Lennart; the rule amended) | applied |
| CLEAN-19 | african_credit_scoring_challenge | `earlier_loans`, the customer's loans in the release disbursed on an earlier day (Train.csv and the Kenyan rows of Test.csv, any product), known at disbursement and built without labels; the models reached the customer's history only through `customer_id`, and the count alone ranks defaults at ROC AUC 0.72 on the six windows; the 6th-place solution builds a close variant (the rank of the loan's date among the customer's dates) (2026-10-26, Lennart) | applied |
| CLEAN-19 | rosbank1 | the CoLES baseline aggregates plus the time block of the 1st place of task 1 (Khrylchenko 2018; active days: span, spread, position and gaps, overall and per category, the last month, days per month), rewritten from his code: untuned LightGBM 0.896 against 0.857 for CoLES alone on the three windows; his full set scored lower (0.882) and his money and MCC blocks added nothing, so the combination, not the union (2026-10-26, Lennart) | applied |
| CLEAN-19 | fraud_detection_in_electricity_and_gas_consumption_1m | the invoice rows stay, one prediction per client (the mean of its invoice predictions), instead of one row per client with aggregates: each invoice is a full observation of the client (LightGBM on the invoices 0.682 against 0.675 on simple aggregates), and the top solutions' aggregates rest on the full history, which the 2013 cut removes (2026-10-26, Lennart) | exception |
| CLEAN-19 | amex_non_iid | the raw statements stay, one prediction per customer from its latest statement with every statement available (`aggregation="last"`), although the top solutions aggregated (CC 2026-10-02, Lennart; recorded here 2026-10-26) | exception |
| CLEAN-20 | santander_customer_transaction_prediction | `has_one` won the competition and is not copied | applied |
| CLEAN-21 | college_scorecard | the SAT was redesigned in 2016, so from the 2017 cohort on an institution's scores jump while its students stay the same; the College Board's concordance tables put SATMT25, SATMT75 and SAT_AVG back on the old scale (median change 2016 to 2017 within an institution: 0 instead of +30); a section without a conversion table stays dropped (2026-10-16, Lennart) | applied |
| CLEAN-21 | force_2020_well_well_log_and_lithofacies_dataset_for_machine_learning_competition | no unit in the files or the LAS headers, so the conversion is inferred from the data and checked against a second curve or a second group of wells: ROP in ft/h in two wells (x 0.3048; ROPA / ROP 0.31 there, about 1 in 26 other wells, 1.0 after), MUDWEIGHT in bar/m in 19 wells (/ 0.0980665, per row below 0.5; per-well medians land in the range of the g/cm3 wells); curves without such a check are masked, not converted (2026-10-21, Lennart) | applied |
| CLEAN-21 | zillow_prize | `buildingqualitytypeid` of 2017 mapped onto the 2016 scale with the map the data shows, confirmed on all 1.94M parcels with a code in both files; no published conversion exists (2026-10-26, Lennart) | exception |
| CLEAN-21 | rosbank1 | amounts in each transaction's own currency (57 codes, up to 35.8 million dong) converted to rubles at the Bank of Russia's official rate in force on the transaction's day, the measuring body's conversion; the ISO numeric reading of the codes checked on the data (converted, the median POS purchase is 355-3,346 rubles in every currency, against 500 in rubles); the 0.3% of transactions in currencies the Bank did not quote then are masked, not converted from another source (2026-10-26, Lennart) | applied |
| CLEAN-22 | coad_colon_adenocarcinoma | ships 36,355 features; its report had weighed one model's 50,000-feature cap (2026-10-15, Lennart) | applied |
| CLEAN-24 | apistox, drug_induced_autoimmunity_prediction, qsar_bioconcentration | the SMILES as text next to the descriptors: -0.025 to +0.010 ROC AUC; the string is dropped (2026-10-14) | applied |

## In Data Foundry

The order of these steps in `_clean`, the helpers (`drop_columns`, `rdkit_descriptors`, `anonymize_ids`) and the
bundle checks that catch what is missed: [definitions.md](../../knowledge-data-foundry/references/definitions.md),
"The preprocessing recipe".
