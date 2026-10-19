---
unique_name: metro_manila_village_weekly_dengue
name: Weekly dengue incidence and environment, Metropolitan Manila villages 2009-2013 (Francisco et al. 2024)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
tags:
- AI-Filled (Verify)
- Two-Regime Zeros
- Non-IID (Temporal)
original_source: Other
year: '2024'
domain: medical & healthcare
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.5061/dryad.x3ffbg7ss
- https://doi.org/10.1371/journal.pntd.0012599
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

Village-week dengue incidence in Metropolitan Manila, 2009-2013 (cases from the National Epidemiology Center, DOH
Philippines), with temperature, IMERG precipitation, humidity, wind and NDVI each lagged 0-31 weeks, plus static land
use, flood risk and road density; no lagged dengue. The paper trains on 2009-2012 and tests on 2013 ("Data from 2009
to 2012 were used for training, and data from 2013 were used for model validation"), so it is a fixed
environmental-covariate task that needs a temporal split, not series forecasting. Not downloaded (Dryad blocks
automated downloads). 437 villages x 260 weeks is about 113,620 rows, which matches the paper's 90,896 training and
22,724 test observations.

Zero mechanism, from the paper only: no reported case in the village-week. The target `LogDenIncd` is log(n + 1) of
the incidence per 10,000 (Methods, Epidemiological data), so a week without cases is exactly 0; the paper says "70%
of the data was zero-inflated" (its training counts give 71.4%). This settles the workbook's open question about the
transform. To check: rows, columns and zero share in the file; the lags were chosen by cross-correlation over
2009-2013, test year included (a mild leak, although the model "did not have access to the 2013 data"); which
covariates enter at lag 0 (S2 Table, not read); the village as a group inside the temporal split. Licence: CC0.

## Reference

Francisco M.E., Carvajal T.M., Watanabe K. (2024). Hybrid machine learning approach to zero-inflated data improves
accuracy of dengue prediction. PLOS Neglected Tropical Diseases 18(10):e0012599. doi:10.1371/journal.pntd.0012599.

Lead: curation/inputs/two_regime_zero_datasets_v4.xlsx, Master row 11 (Dengue incidence environment).
