---
unique_name: income_prediction_challenge_for_azubian
name: income-prediction-challenge-for-azubian
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- Duplicate
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
domain: social science
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/income-prediction-challenge-for-azubian
- https://zindi.africa/competitions/umojahack-india-2022
source_row: 964
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 2: a Zindi re-run of UmojaHack India 2022 whose columns are those of the UCI Census-Income (KDD) data, so very likely a renamed copy of `census_income`; not a fast reject because the source never names its origin.
- Source: Zindi, "Income Prediction Challenge For Azubian" (knowledge challenge, 2022-11-07 to 2024-06-06, Senegal); the Zindi API gives `umojahack-india-2022` (2022-10-15, private, Indian citizens) as its parent, and both list the same files byte for byte (Train.csv 68,209,849 B, Test.csv 28,207,389 B, VariableDefinitions.csv 1,674 B). As published: "There are ~200 000 individuals in train and ~100 000 individuals in the test file ... predict if an individual earns above 50 000 of a specific currency", target `income_above_limit`; "This data has been collected from a random population."
- Use case: Zindi: "reduce the cost and improve the accuracy of monitoring key population indicators such as income level in between census years" for policymakers; fit approximate (the rows look like 1994-95 US CPS records, not the population the page speaks of). Regime IID (one row per person, no time index).
- Siblings and duplicates: the column names used by public notebooks on this data (GitHub `LewyseK/Income-predictor` dashboard.py, Hugging Face Space `Faith-theAnalyst/income_FastAPI`: `worker_class`, `industry_code`, `industry_code_main`, `occupation_code_main`, `total_employed`, `household_summary`, `vet_benefit`, `tax_status`, `gains`, `losses`, `stocks_status`, `citizenship`, `mig_year`, `country_of_birth_mother`, `importance_of_record`) are the KDD Census-Income attributes renamed (class of worker, industry / major industry code, num persons worked for employer, veterans benefits, tax filer status, capital gains / losses, dividends from stocks, migration year, instance weight), and the ~200k / ~100k rows and the 50,000 threshold match its 199,523 / 99,762 rows; so very likely a duplicate of `census_income` (TBD -> 2nd Tier, `Outdated`) and close to `adult`. `dlix_botswana` uses the same `income_above_limit` submission format (check it in the same pass). Not to be confused with `predictive_insights_youth_income_prediction_challenge` (South African youth survey).
- Papers and pages: the Zindi pages above; no paper. The UCI Census-Income (KDD) page is the likely origin.
- Metric: F1 on the hard 0/1 label (Zindi Evaluation page: "The error metric for this competition is the F1 score"); a leaderboard metric, deliberate (MET-4), threshold not fixed by the source beyond submitting labels (MET-6); inputs none.
- Risks for /add-dataset: confirm the duplicate by rows against UCI census-income (needs a Zindi login or a mirror), then the verdict follows `census_income` (PROV-4, PROV-5); `importance_of_record` is the CPS instance weight and never a feature; the old note "not a re-upload of a known income dataset" is the open question.
- Priority: gap + (social science thin), use case 0 (approximate), source 0 (Zindi names no origin), shape + (~300k rows, ~40 mixed columns), risk - (likely duplicate).

Zindi competition to predict whether an individual earns above or below an income threshold, an adult-census-style binary classification on socioeconomic/demographic tabular features. This is a genuine real-world predictive tabular task with a clear target, mapping well to the IID classification criterion. Plausibly a Yes but the record carries no size/feature details. A human must verify row count after cleaning, the exact feature set, the actual target column, and that it is not a re-upload of a known income dataset.

---

predict if an individual earns above or below an income threshold
