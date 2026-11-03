---
unique_name: liberty_mutual_property_inspection
name: 'Liberty Mutual Group: Property Inspection Prediction (Kaggle 2015)'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 4
decision_markers:
- Anonymized
tags:
- AI-Filled (Verify)
original_source: Kaggle
year: '2015'
domain: insurance
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/competitions/liberty-mutual-group-property-inspection-prediction
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 4: an insurer's own task with a stated actor, moment and decision (which newly insured homes need an inspection), about 51,000 labelled homes, a Kaggle Featured competition with 2,232 teams; the predictors are anonymised.
- Source: Liberty Mutual Group, Kaggle Featured competition "Liberty Mutual Group: Property Inspection Prediction", 2015-07-06 to 2015-08-28, $25,000, 2,232 teams (Kaggle API). Data page: "Each row in the dataset corresponds to a property that was inspected and given a hazard score ("Hazard") ... The total score for a property is the sum of the individual hazards. The aim of the competition is to forecast the hazard score based on anonymized variables which are available before an inspection is ordered." Files: train.csv.zip (988 KB), test.csv.zip (952 KB), sample_submission.csv.zip; train about 51,000 rows (50,999 by the usual count; the file was not opened) with Id, Hazard and 32 predictors T1_V1-T1_V17 and T2_V1-T2_V15 (numeric and letter-coded); the test file has no labels.
- Use case: the Description: newly insured properties "receive a home inspection ... The results of an inspection help Liberty Mutual determine if the property is one they want to insure", and the model helps "identify high risk homes that require additional examination to confirm their insurability"; the prediction is made before an inspection is ordered; fit direct. Regime IID: no date or group column ships and no split statement was found.
- Siblings and duplicates: `homesite_quote_conversion` (`Yes`, DF: Yes; anonymised Homesite quotes, a conversion task in the same insurance line); `fio_homeowners_insurance_zip_2018_2022` (AI `TBD -> 2nd Tier`, ZIP-level aggregates); `allstate_claims_severity`, `porto_seguro` (other insurance tasks). No duplicate (grep liberty, property inspection, hazard). External collections: none found.
- Better data: found as a related task next to `homesite_quote_conversion`; no further search this round.
- Papers and pages: the competition's Description, Data, Evaluation and Rules pages (read through the Kaggle API); the winning solutions were not read.
- Metric: "Submissions are evaluated on the normalized Gini coefficient ... only the order of your predictions matters" (Evaluation page), a competition's choice (MET-4). On a count-like target it is not ROC AUC (the porto_seguro identity holds only for a binary target), so it needs a custom metric with a general name such as `normalized_gini` (MET-12, MET-13), not yet in the metric library. Inputs none.
- Risks for /add-dataset: the predictors are anonymised (`Anonymized`; their meaning and timing cannot be checked, LEAK-32), though the page says they are "available before an inspection is ordered"; "a transformed count of hazards" (Description), the transform not stated (MET-3: the target ships as given); only the training file has labels; check duplicate rows.
- Priority: gap + (insurance has 3 accepted datasets, thin), use case + (actor, moment and decision stated by the insurer), source + (the insurer's competition pages define the target, its timing and the metric), shape + (about 51,000 homes, 32 mixed predictors), risk - (anonymised predictors, a transformed target).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through a related task next to `homesite_quote_conversion`.
- as published: one row per newly insured, inspected home; train about 51,000 rows x 32 anonymised predictors (T1_V1..T2_V15) + Hazard (not counted); test about 51,000; target: Hazard: transformed count of hazards or pre-existing damages found by the inspection (normalized Gini); access: registration.
- Why: a different real task in homeowners insurance (the line Homesite quotes), with a named insurer, a stated actor, moment and decision, and over 1,000 units
- Adds: a second homeowners-insurance underwriting task (inspection triage) in a thin domain; anonymised like Homesite
