---
unique_name: ptb_xl_plus_arrhythmia
name: PTB-XL+, a comprehensive electrocardiographic feature dataset (with the PTB-XL statements)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
tags:
- AI-Filled (Verify)
original_source: Other
year: '2023'
domain: medical & healthcare
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.1038/s41597-023-02153-8
- https://physionet.org/content/ptb-xl-plus/1.0.1/
- https://doi.org/10.1038/s41597-020-0495-6
- https://physionet.org/content/ptb-xl/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: ECG measurements (intervals in ms, amplitudes in mV per lead) from three algorithms for the PTB-XL ECGs (about 21,800 ECGs of 18,900 patients), with the cardiologists' rhythm statements as a target; open and large, but ECG-derived features of the kind the curator turned down in `arrhythmia` as a time-series source.
- Source: Strodthoff, Mehari, Nagel et al., "PTB-XL+, a comprehensive electrocardiographic feature dataset", Scientific Data 2023 (doi 10.1038/s41597-023-02153-8; abstract read); PhysioNet physionet.org/content/ptb-xl-plus/1.0.1/ (2023-06-27, CC BY 4.0). Built on PTB-XL (Wagner et al., Scientific Data 2020, doi 10.1038/s41597-020-0495-6: "21837 records from 18885 patients of 10 seconds length"; 21,799 of 18,869 in a later version per the scout). As published: `features/12sl_features.csv` (GE Marquette 12SL), `unig_features.csv` (Glasgow Uni-G), `ecgdeli_features.csv` (open-source ECGDeli, median and IQR over beats), one row per ECG keyed by the PTB-XL id, with `feature_description.csv` (units, LOINC); `labels/ptbxl_statements.csv` (the cardiologists' statements, SNOMED-mapped) and `12sl_statements.csv` (machine statements); Uni-G statements are left out "because of usage restrictions"; age, sex, patient id and the recommended folds are in PTB-XL's metadata.
- Use case: ECG software or a clinician reading a resting 12-lead ECG flags atrial fibrillation or another rhythm for work-up; the paper: the features "still form the basis of most automatic ECG analysis algorithms and are critical for cardiologists' decision processes" (abstract); fit direct for resting-ECG interpretation, approximate for the wearable task it was found for; regime grouped by patient (PTB-XL's folds keep a patient's ECGs together).
- Siblings and duplicates: `cardiac_arrhythmias_prediction_challenge_by_lifeq` (`TBD -> 2nd Tier`, priority 1: raw RR series, the record this was found for), `arrhythmia` (`No`, `Wrong Domain / Source Modality`, `Outdated`, `Time-series (Classification)`: UCI's ECG measurements, "source domain is time-series not tabular"); no duplicate. External collections: PTB-XL's waveforms are a standard ECG benchmark (Strodthoff et al. 2020); none found for the feature tables.
- Better data: found as better data for `cardiac_arrhythmias_prediction_challenge_by_lifeq` (the data-scouting run of 2026-10-30/31); no further search this round.
- Papers and pages: Wagner et al. 2020; Strodthoff et al., "Deep Learning for ECG Analysis: Benchmarks and Insights from PTB-XL", IEEE JBHI (doi 10.1109/JBHI.2020.3022989; arXiv 2004.13701, text read: waveform CNNs reach a macro AUC of about 0.96 in the rhythm category); the PTB-XL+ PhysioNet page.
- Metric: the PTB-XL benchmark ranks by term-centric macro-averaged AUC ("macro-averaging is preferred, since we expect class imbalance", Sect. II-C; "we focus on macro AUC" in the results), a deliberate choice (MET-5): `roc_auc` for a binary rhythm target, macro `roc_auc` for a multiclass one; inputs none (the patient id ships for grouping).
- Risks for /add-dataset: the scope call comes first: are ECG measurements the clinical readings tabular models use (SEL-14, SEL-15) or signal-derived features where waveform models win (SEL-12, SEL-13)? The `arrhythmia` precedent says the latter for similar columns (a consistency question for the curator). The target must come from the cardiologists' statements, not the 12SL statements computed from the same 12SL measurements (SEL-5); rhythm statements can co-occur (binary AF or flutter against the rest, or a multiclass rhythm task); the recordings are from 1989-1996 (`Outdated`?); three feature tables to merge, with gaps.
- Priority: gap 0 (medical and binary are not thin), use case 0 (ECG interpretation, no actor or decision named beyond it), source + (Scientific Data, PhysioNet), shape + (about 21,800 ECGs, three feature sets, patient groups), risk - (the `arrhythmia` scope precedent may apply).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `cardiac_arrhythmias_prediction_challenge_by_lifeq`.
- as published: One row per 10-second 12-lead ECG, PTB-XL's 21,799 ECGs of 18,869 patients (from memory of Wagner et al. 2020). Three feature tables (12SL, Uni-G, ECGDeli): intervals in ms and amplitudes in mV per ...; target: an arrhythmia rhythm statement on the ECG, e.g. atrial fibrillation or flutter against sinus rhythm (binary), from the PTB-XL cardiologist statements, not the ...; access: open.
- Why: Same target as the LifeQ challenge (an arrhythmia class from heart-rhythm measurements), and the measurements are already tabular, which is the LifeQ record's main problem (raw RR series, Time-series marker, needs wrangling). The fit is approximate: a resting 12-lead ECG in a clinic, not a night of wearable or PSG RR ...
- Adds: Over 21,000 ECGs against 349 labelled sessions. Open CC BY 4.0 instead of a private hackathon with a secret code. Published, traceable features and cardiologist labels instead of an unnamed private metric. Patient IDs allow a grouped split. Watch the 12SL features against the 12SL statements (leak) and use the ...
