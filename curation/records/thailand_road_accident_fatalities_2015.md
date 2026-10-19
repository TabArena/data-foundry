---
unique_name: thailand_road_accident_fatalities_2015
name: Thai road-accident fatalities / Thailand road accidents 2015, deaths per accident (DDPM; PLOS ONE S1 File)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
tags:
- AI-Filled (Verify)
- Two-Regime Zeros
original_source: GOV Website
year: '2022'
domain: social science
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0269022.s002&type=supplementary
- https://doi.org/10.1371/journal.pone.0269022
- https://data.go.th/en/dataset/item_71aa612f-adaf-4b0d-b81b-ccdfd97efeef
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

Road accidents in Thailand in 2015 from the Department of Disaster Prevention and Mitigation (Ministry of Interior),
the supplement of a count-regression paper (Simmachan et al. 2022): "Complete data were available for 20,229 cases"
of 25,586 reported. Downloaded and measured on 2026-10-19: 20,229 rows x 8 columns (ID, month, deaths, roadway
class with 4 levels, road surface 2, road section 3, weather 3, light 3); no location; the covariates form only
1,165 distinct cells. A quick 5-fold histogram gradient boosting gives ROC AUC 0.71 for any death and a Poisson
deviance reduction (D^2) of 0.12. The paper's aim is descriptive ("using count regression models to investigate the
distribution of RAFs"), but deaths per crash from scene conditions is the crash-severity task the log keeps open in
`nhtsa_crss_crash_severity` and `chicago_traffic_crashes`; `us_accidents` does not transfer (its target was a delay
code).

Zero mechanism, confirmed from the data: a crash without deaths, 72.4% (14,641 rows; 5,218 with one death, 370 with
two or more), stochastic given an accident; the paper finds that "Neither the ZIP model nor the ZICMP model captured
the excess zeros". 2nd tier because six coarse covariates are thin and the table is an extract of a public register:
a richer sibling, the Ministry of Transport register 2019-2022 (Kaggle `thaweewatboy/thailand-road-accident-2019-2022`,
81,735 rows with province, vehicle, cause, accident type, fatalities, injuries and coordinates, CC0), is not in the
log and could be opened as its own candidate. The data.go.th upstream returned 403 and was not compared. Licence:
CC BY 4.0 (article and supplement).

## Reference

Simmachan T., Wongsai N., Wongsai S., Lerdsuwansri R. (2022). Modeling road accident fatalities with underdispersion
and zero-inflated counts. PLOS ONE 17(11):e0269022. doi:10.1371/journal.pone.0269022.

Lead: curation/inputs/two_regime_zero_datasets_v4.xlsx, Master row 17 (Thai road-accident fatalities).
