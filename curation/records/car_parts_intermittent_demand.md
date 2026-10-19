---
unique_name: car_parts_intermittent_demand
name: Car Parts (expsmooth carparts) / Car Parts Dataset with and without Missing Values (Monash archive)
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Time-series (Forecasting)
tags:
- AI-Filled (Verify)
- Two-Regime Zeros
original_source: Other
year: '2008'
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: Other
source_links:
- https://zenodo.org/records/4656022
- https://zenodo.org/records/4656021
- https://cran.r-project.org/package=expsmooth
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

Monthly sales of 2,674 slow-moving parts of a US car company, January 1998 to March 2002 (51 months), from Hyndman
et al. (2008) and the R package expsmooth; the Monash forecasting archive ships it twice on Zenodo. Both were
downloaded and compared on 2026-10-19. Record 4656022 keeps 6,122 missing cells (4.5%), all in 165 series that stop
after month 13-15, and has 71.4% zeros (74.8% of the observed cells). Record 4656021 is identical except that those
6,122 cells are set to 0 (75.9% zeros), which invents about 37 months of zero demand for each truncated series. The
workbook is right to prefer 4656022.

Zero mechanism, confirmed from the data: months without demand, plus the artificial zero-fill in 4656021. Either way
these are univariate series with no covariates, used for 6-step-ahead forecasting (Turkmen et al. 2021, Sec. 5.2).
Licence: CC BY 4.0 (Zenodo), GPL (>= 2) (expsmooth).

## Reference

Hyndman R.J., Koehler A.B., Ord J.K., Snyder R.D. (2008). Forecasting with Exponential Smoothing: The State Space
Approach. Springer. Monash Time Series Forecasting Archive release (Godahewa R. et al.), doi:10.5281/zenodo.4656022.

Lead: curation/inputs/two_regime_zero_datasets_v4.xlsx, Master row 50 (Car Parts intermittent-demand benchmark).
