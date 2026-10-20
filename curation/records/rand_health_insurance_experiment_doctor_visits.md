---
unique_name: rand_health_insurance_experiment_doctor_visits
name: RAND Health Insurance Experiment doctor visits (statsmodels randhie / Cameron & Trivedi extract), 1974-1982
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target  / Scientific Discovery
- Outdated
tags:
- AI-Filled (Verify)
- Two-Regime Zeros
- Non-IID (Grouped)
original_source: Other
year: '1995'
domain: medical & healthcare
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.statsmodels.org/dev/datasets/generated/randhie.html
- http://cameron.econ.ucdavis.edu/mmabook/mmadata.html
- https://doi.org/10.3886/ICPSR06439.v1
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-20 from a web search for zero-inflated regression candidates, the source pages and, where the notes say so, the downloaded data. A human must verify the suggestion, the metadata and the notes before relying on them.**

Person-year extract of the RAND Health Insurance Experiment (1974-1982, six US sites) from Cameron and Trivedi's
Microeconometrics data page (randdata.dta, 20,190 rows x 45 columns); statsmodels' `randhie` keeps the visit count and
9 of the covariates. ICPSR 6439: "The main purpose of the experiment was to assess how the cost of health services
affected individuals' use of services, their satisfaction with health care, the quality of their care, and the state
of their health." The covariates are the randomised plan (coinsurance, deductible, participation incentive,
maximum-expenditure offer) plus baseline demographics and health, so a visit model is the demand equation behind a
price-elasticity estimate, on data now 50 years old. Same call as `health_insurance` (an econometrics study of the
1993 CPS).

Measured: 5,912 persons (most with 3 or 5 years); `mdvis` has 31.2% zeros (max 77), medical spending `meddol` 22.1%.
The 9 statsmodels covariates are constant within a person and take only 2,760 distinct vectors over 20,190 rows,
so a split must group by person (`zper`, in the extract only). Untuned LightGBM grouped by person:
AUC 0.69 for any visit and R^2 0.02 on log1p visits among users with the 9 columns; 0.75 and 0.08 with the 30 columns
that are not utilisation or spending; 0.79 and 0.27 with the previous year's visits and spending added. The same-year utilisation and
spending columns (`meddol`, `outpdol`, `drugdol`, `suppdol`, `mentdol`, `inpdol`, `totadm`, `inpmis`, `mentvis`,
`notmdvis`, `lnmeddol`, `binexp`) are outcomes. The ICPSR public-use files add expenditure and health detail but no
other purpose; `meps_total_healthcare_expenditure` is the current version of this task. statsmodels: "This is in the
public domain"; ICPSR lists no access restriction for 6439.

## Reference

Newhouse J.P. RAND Health Insurance Experiment [in Metropolitan and Non-Metropolitan Areas of the United States],
1974-1982. ICPSR 6439, version 2005-11-04. doi:10.3886/ICPSR06439.v1. Extract: Cameron A.C., Trivedi P.K. (2005).
Microeconometrics: Methods and Applications. Cambridge University Press; data randdata.dta at
http://cameron.econ.ucdavis.edu/mmabook/mmadata.html.

Lead: web search 2026-10-20 for zero-inflated regression candidates (not in the v4 workbook).
