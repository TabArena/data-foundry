---
unique_name: opendengue_case_counts
name: OpenDengue (global compilation of reported dengue case counts)
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target (yet)
- Time-series (Forecasting)
tags:
- AI-Filled (Verify)
- Two-Regime Zeros
original_source: Github
year: '2024'
domain: medical & healthcare
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://opendengue.org/
- https://github.com/OpenDengue/master-repo
- https://doi.org/10.1038/s41597-024-03120-7
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

OpenDengue (Clarke et al. 2024): publicly reported dengue case counts by place and period. Downloaded the V1.3
extracts on 2026-10-19. National: 29,873 rows from 129 countries, 1924-2025, 32.6% zeros. Spatial: 2,821,791 rows
over 7,110 admin-2 units, 55.1% zeros (mostly Brazilian weekly counts). A row holds location, dates, case definition
and resolution and no predictors; the Usage Notes point to "time series analysis, forecasting". Without features there
is no tabular task, and adding drivers would turn it into forecasting of case series.

Zero mechanism, confirmed from the data: reported zero cases, plus documented zero-filling of gaps (Methods: "replace
NAs with zero incident cases by leveraging these annual counts"). Rows flagged "Zero filling" in their id hold 10.1%
of the national zeros and 0.14% of the spatial ones. Licence: CC BY-SA (Usage Notes).

## Reference

Clarke J., Lim A., Gupte P., Pigott D.M., van Panhuis W.G., Brady O.J. (2024). A global dataset of publicly available
dengue case count data. Scientific Data 11:296. doi:10.1038/s41597-024-03120-7.

Lead: curation/inputs/two_regime_zero_datasets_v4.xlsx, Master row 21 (OpenDengue).
