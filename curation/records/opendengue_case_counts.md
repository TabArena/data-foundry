---
unique_name: opendengue_case_counts
name: OpenDengue (global compilation of reported dengue case counts)
checked_by:
- Andrej
suggestion: 'No'
decision_markers:
- No Good Target (yet)
- Time-series (Forecasting)
tags:
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
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (v4 of 2026-10-19, a list of 69 candidates, not in the repository), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `No` (`Time-series (Forecasting)`, SEL-10): a global compilation of reported dengue case
counts by place and period, with no predictors; the only prediction its rows support is a case series' future values,
the use its source names first.
- Source: OpenDengue, Clarke et al. (2024), Scientific Data 11:296 (published 2024-03-14; "The first version (version
  1.0) of this dataset has also been publicly available since June 2023", so the year is 2023 by PROV-9, not the
  record's 2024); data on opendengue.org, GitHub and Figshare under CC BY-SA ("Citation and data licence"). As
  published, the codebook (Data Records) lists place names and codes (adm_0_name to adm_2_name, ISO_A0, FAO_GAUL_code,
  RNE_iso_code, IBGE_code), calendar_start_date, calendar_end_date, Year, Dengue_total, case_definition_standardised,
  S_res, T_res and the source UUID: counts and their place and period, nothing else. Earlier AI triage, 2026-10-19,
  measured V1.3: national extract 29,873 rows (32.6% zeros), spatial extract 2,821,791 rows over 7,110 admin-2 units
  (55.1% zeros).
- Deciding quote: Usage Notes, "Choice of extract": "Applications that explore changes in dengue dynamics over time
  including time series analysis, forecasting and national programme evaluation should use the temporal extract"; the
  other uses it names are "identifying worst affected areas and years, understanding drivers of transmission such as
  climate factors and interventions and predicting future trends and outbreak risk", and burden estimation for the
  national extract (https://doi.org/10.1038/s41597-024-03120-7, Usage Notes; codebook under Data Records). With no
  column besides place, period and count, a model can only predict a count from the place's own series: forecasting
  (SEL-10). The panel exception (SEL-11, TP-10) needs "a model on the features" to beat each entity's naive forecast,
  and the release has no features. A driver task needs covariates joined from other sources, a rebuild with its own
  origin (PROV-11), which is what `metro_manila_village_weekly_dengue` already is for one city.
- Use case: for example a health ministry forecasting the coming weeks' cases for outbreak response: a forecasting task;
  the source names no actor.
- Siblings and duplicates: `metro_manila_village_weekly_dengue` (TBD -> Yes, priority 3) is the dengue task with
  covariates, at village-week level (OpenDengue stops at admin level 2, so it does not hold those rows). External
  collections: none found.
- Papers and pages: the data descriptor above (read via PMC10940302: Background & Summary, Methods, Data Records, Usage
  Notes).
- Metric: none; the descriptor defines no task (Usage Notes, Data Records and Methods read).
- Risks if reopened: documented zero-filling of reporting gaps (Methods: "We proceeded to replace NAs with zero incident
  cases by leveraging these annual counts, a process we call "zero filling"") and cubic-spline interpolation of gaps
  under six weeks: the coded-zeros policy question; mixed case definitions (suspected, probable, confirmed) across
  countries and years.
- Reject check (AI, 2026-10-27): stands. SEL-10 (Must). The codebook has only place, date and count fields (place names
  and codes, `calendar_start_date`, `calendar_end_date`, `Year`, `Dengue_total`, `case_definition_standardised`,
  `S_res`, `T_res`, `UUID`), and the Usage Notes name forecasting: the temporal extract is for "time series analysis,
  forecasting and national programme evaluation" (https://pmc.ncbi.nlm.nih.gov/articles/PMC10940302/). SEL-3 is a second
  ground: driver or burden uses need covariates from other sources, a rebuild (PROV-11), which
  `metro_manila_village_weekly_dengue` already is.

**Assessment (AI, 2026-10-30):** The family's open question on coded and censored zeros is settled (Andrej, 2026-10-30,
policy question 2 of the zero-inflated review: "We don't care. We want to add any relevant predictive task, independent
if it is zero inflated or not"), so how the source codes its zeros is no reason for a No or a lower priority. The
zero-filled reporting gaps are a cleaning choice; the `No` rests on SEL-10 (a case series without predictors), not on
the zeros, so it stands.

CC (2026-10-30, Andrej): `No`, as screened (verified on the zero-inflated screening review page).

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

Lead: the two-regime-zero workbook (v4, 2026-10-19), Master row 21 (OpenDengue).
