---
unique_name: meps_total_healthcare_expenditure
name: MEPS healthcare expenditure / Medical Expenditure Panel Survey Full Year Consolidated file (HC-251, 2023), TOTEXP
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
decision_markers:
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
- Two-Regime Zeros
- Non-IID (Grouped)
original_source: GOV Website
year: '1996'
domain: medical & healthcare
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://meps.ahrq.gov/mepsweb/data_stats/download_data_files.jsp
- https://meps.ahrq.gov/data_files/pufs/h251/h251dta.zip
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

AHRQ's Medical Expenditure Panel Survey, the standard US source for person-level healthcare spending; one Full Year
Consolidated file per year since 1996. Downloaded the 2023 file (HC-251, Stata) on 2026-10-19: 18,919 persons x
1,374 columns from two panels in 8,914 dwelling units, with survey strata and PSUs. Target `TOTEXP23`: no missing
values, 2,655 zeros (14.0%; 13.3% among persons with a positive weight), median $1,816, maximum $574,675. A quick
probe on 34 demographic, insurance, health-status and condition features (household-grouped 5-fold, histogram
gradient boosting): ROC AUC 0.84 for any spending, R^2 0.32 on log1p spending among the positives.

Zero mechanism, confirmed from the data: no healthcare use in the year. The file is full of target copies: 279
columns with the year suffix split expenditure by event type and payer and sum to `TOTEXP23`, and 10 utilisation
counts (office visits, outpatient, ER, inpatient discharges and nights, prescriptions, dental, home health) are zero
for at least 99.5% of the zero-spending persons; all must go. Workbook pushback: one file holds about 19k persons
from two panels, not "~10k/panel". Split: group by household (persons in one dwelling share insurance and access).
To check: concurrent (same-year health status) or prospective (year-1 features, year-2 spending from the panel
files) framing, which round-specific variables are known at prediction time, and the survey weights. It would be the
real-data counterpart of `healthcare_insurance_expenses`, retired as generated. Licence: AHRQ public-use terms (not
re-read).

## Reference

Agency for Healthcare Research and Quality (2025). MEPS HC-251: 2023 Full Year Consolidated Data File. Medical
Expenditure Panel Survey, https://meps.ahrq.gov/.

Lead: curation/inputs/two_regime_zero_datasets_v4.xlsx, Master row 5 (MEPS healthcare expenditure).
