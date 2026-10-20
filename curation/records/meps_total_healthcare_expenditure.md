---
unique_name: meps_total_healthcare_expenditure
name: MEPS healthcare expenditure / Medical Expenditure Panel Survey longitudinal files, Panels 27 and 28 (HC-252, HC-257), next-year TOTEXP
checked_by:
- Andrej
suggestion: 'Yes'
decision_markers:
- Needs extensive data wrangling
tags:
- Two-Regime Zeros
- Non-IID (Grouped)
- Many features
original_source: GOV Website
year: '1996'
domain: medical & healthcare
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://meps.ahrq.gov/mepsweb/data_stats/download_data_files.jsp
- https://meps.ahrq.gov/mepsweb/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-252
- https://meps.ahrq.gov/mepsweb/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-257
- https://meps.ahrq.gov/data_files/pufs/h252/h252dta.zip
- https://meps.ahrq.gov/data_files/pufs/h257/h257dta.zip
- https://meps.ahrq.gov/data_files/pufs/h251/h251dta.zip
type_adapter_id: curation-record-v1
---

## Comments

* AHRQ's Medical Expenditure Panel Survey, the standard US source for person-level healthcare spending; one
  longitudinal file per panel follows the same persons over two years. Licence: AHRQ data use agreement (HC-252
  Sec. A), "for statistical reporting and analysis" only, no re-identification.
* Zero mechanism: no healthcare use in the year (14.0% zeros in the 2023 file). Each year's expenditure and use
  columns copy that year's target (279 of them sum to `TOTEXP23`).
* Real-data counterpart of `healthcare_insurance_expenses` (retired as generated);
  `rand_health_insurance_experiment_doctor_visits` is the 1970s precursor.

CC (2026-10-20, Andrej): Yes, as a prospective task.

* Use case: predict next year's spending from what is known at the end of this year, as in risk adjustment and care
  management. CMS-HCC "is prospective, meaning that diagnoses collected in a base year (1999) are used to predict
  expenditures in the following year (2000)" (Pope et al. 2004, section "CMS-HCC Model Calibration").
* Possible use cases: payers setting next year's per-member payments and reserves (CMS-HCC capitation); care
  management picking likely high spenders for outreach (health plans, provider groups paid per patient, self-insured
  employers); health policy research on who stays a high spender. Self-rated health, income and education are survey
  items a payer's claims lack, so for payers the task is an approximation; for survey-based research it fits as is.
* Data: HC-252 (Panel 27, 2022-2023) and HC-257 (Panel 28, 2023-2024) stacked on their common columns, persons in
  scope in both years (`YEARIND` = 1): 16,818 persons in 8,328 households. Target `TOTEXPY2`, 14.7% zeros.
* The concurrent framing leaks through skip patterns (-1: "Question was not asked due to skip pattern", HC-251 Sec. C
  2.2): `PMEDUP4` is answered only by persons with a prescription that year. Year-2 answers alone give AUC 0.946.
* Features: constant demographics, all `Y1` columns (year-1 spending and use included) and rounds 1-2. Drop round 3
  (interviewed in year 2, HC-252 Sec. C 2.1.1 note 2), rounds 4-5 and all `Y2` columns.
* Probe (untuned LightGBM, household-grouped 5-fold, 1,077 features): AUC 0.905 for any spending, R^2 0.530 on log1p
  spending; prior-year spending alone 0.844 and 0.425.
* Weights: drop `LONGWT`, `LSAQWT`, `VARSTR`, `VARPSU` and score unweighted. They correct for nonresponse and rake to
  CPS totals (HC-251 Sec. 3.3.2); no minority oversampling since 2016 (HC-252 Sec. B 1.0).
* Split: grouped by household (`DUID`); one respondent reports for the whole household (HC-252 Sec. B 1.0).
* For `/add-dataset`: keep the reserved codes (-1, -7, -8, -15) as values and the persons who die in year 2. Older
  panels would add rows but have changed questionnaires and COVID years.

## Reference

Agency for Healthcare Research and Quality (2025). MEPS HC-252: Panel 27 Longitudinal Data File, 2022-2023. Medical
Expenditure Panel Survey, https://meps.ahrq.gov/.

Agency for Healthcare Research and Quality (2026). MEPS HC-257: Panel 28 Longitudinal Data File, 2023-2024. Medical
Expenditure Panel Survey, https://meps.ahrq.gov/.

Agency for Healthcare Research and Quality (2025). MEPS HC-251: 2023 Full Year Consolidated Data File. Medical
Expenditure Panel Survey, https://meps.ahrq.gov/.

Pope, G. C., Kautter, J., Ellis, R. P., Ash, A. S., Ayanian, J. Z., Iezzoni, L. I., Ingber, M. J., Levy, J. M., and
Robst, J. (2004). Risk Adjustment of Medicare Capitation Payments Using the CMS-HCC Model. Health Care Financing
Review 25(4), 119-141. PMC4194896.
