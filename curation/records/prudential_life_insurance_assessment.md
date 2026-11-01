---
unique_name: prudential_life_insurance_assessment
name: Prudential Life Insurance Assessment (Kaggle competition)
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
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/competitions/prudential-life-insurance-assessment
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 4: Prudential's featured Kaggle competition (2015-2016, 2,610 teams): life-insurance applications with over a hundred applicant features and an 8-level ordinal risk class, scored by quadratic weighted kappa; a direct underwriting task in two thin areas (insurance, multiclass), with the feature names anonymised.
- Source: Prudential Financial on Kaggle, "Prudential Life Insurance Assessment" (Featured, opened 2015-11-23, deadline 2016-02-15, 2,610 teams, $30,000; Kaggle API). As published (Data page, read through the Kaggle API): `train.csv` with `Response` and an unlabelled `test.csv`; "over a hundred variables describing attributes of life insurance applicants": Product_Info_1-7, Ins_Age, Ht, Wt, BMI, Employment_Info_1-6, InsuredInfo_1-6 (the nominal list also names InsuredInfo_7), Insurance_History_1-9, Family_Hist_1-5, Medical_History_1-41 (each group "A set of normalized variables relating to ..."), Medical_Keyword_1-48 (dummies); the page lists which are nominal, continuous and discrete. `Response`: "an ordinal variable relating to the final decision associated with an application", 8 levels. Row counts (59,381 train, 19,765 test) from the scout, not counted.
- Use case: the insurer, when an application arrives, classifies the applicant's risk to quote without the medical exams that take "an average of 30 days" (Description: "a predictive model that accurately classifies risk using a more automated approach"); fit direct; regime IID (no date ships).
- Siblings and duplicates: `the_zimnat_insurance_assurance_challenge` (`TBD -> Yes`, policy lapse, another task); the accepted insurance datasets (`allstate_claims_severity`, `homesite_quote_conversion`, `porto_seguro`) are other tasks; no duplicate. External collections: not searched (the web search budget ran out).
- Better data: from the gap scouts for insurance and for multiclass tasks, and found as a related task next to `the_zimnat_insurance_assurance_challenge` (the data-scouting run of 2026-10-30/31); no further search this round.
- Papers and pages: the competition's Description, Data and Evaluation pages (read through the Kaggle API); discussions and top solutions not read.
- Metric: quadratic weighted kappa on the 8 ratings (Evaluation page; API `evaluationMetric` QuadraticWeightedKappa), the leaderboard metric (MET-4): declare it, on hard labels; inputs none.
- Risks for /add-dataset: `Anonymized` (names numbered within groups and values normalised: what each medical item measures, and whether it is known before the medical exam, cannot be checked; LEAK-32, LEAK-38); only `train.csv` has labels (we split it ourselves); what the 8 levels are (risk classes, or decisions such as a decline) is not documented; check `Product_Info_2` codes and missingness by class.
- Priority: gap + (insurance and multiclass are thin), use case + (named by the insurer), source + (a featured competition with documented field groups), shape + (tens of thousands of applications, mixed nominal, continuous, discrete and dummy features), risk - (anonymised features: timing and leaks cannot be checked; the levels are undocumented).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through a related task next to `the_zimnat_insurance_assurance_challenge`; the gap scout for insurance; the gap scout for multiclass tasks.
- as published: about 59,381 applications in train.csv (test.csv about 19,765, unlabelled) x 128 columns: Product_Info_1-7, Ins_Age, Ht, Wt, BMI, Employment_Info_1-6, InsuredInfo_1-7, Insurance_History_1-9, ...; target: Response, an 8-level ordinal risk class 'relating to the final decision associated with an application'; access: registration.
- Why: a real insurer's underwriting decision, a strong competition source with a deliberate metric (quadratic weighted kappa, Evaluation page), mixed feature types; underwriting is named in the area and absent from the benchmark | Company data from a featured competition (2,610 teams) with a direct underwriting use case; ...
- Adds: underwriting and an ordinal multiclass target (multiclass is 24 of 173); life insurance, none accepted. Risks: values normalized and names grouped but anonymised within groups (likely `Anonymized` marker), only the train file has labels, IID only (no date) | Multiclass and insurance at once (both thin), with mixed ...
