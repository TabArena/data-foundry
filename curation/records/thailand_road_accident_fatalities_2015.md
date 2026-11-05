---
unique_name: thailand_road_accident_fatalities_2015
name: Thai road-accident fatalities / Thailand road accidents 2015, deaths per accident (DDPM; PLOS ONE S1 File)
checked_by:
- Andrej
suggestion: TBD -> 2nd Tier
priority: 2
tags:
- Two-Regime Zeros
original_source: GOV Website
year: '2022'
domain: social science
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- '# First publication: DDPM (Ministry of Interior), 2015 crashes, on Open Government Data of Thailand (403 from here, not verified)'
- https://data.go.th/en/dataset/item_71aa612f-adaf-4b0d-b81b-ccdfd97efeef
- '# S1 File of Simmachan et al. 2022: the 20,229 complete cases, CSV'
- https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0269022.s002&type=supplementary
- '# The paper that released S1 File'
- https://doi.org/10.1371/journal.pone.0269022
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (v4 of 2026-10-19, a list of 69 candidates, not in the repository), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `TBD -> 2nd Tier`, priority 2: DDPM's 2015 crash table is another source than
`thailand_road_accident_register_2019_2022` but the same task (deaths per crash in Thailand), with six coded covariates
and one year; /add-dataset should take the register.
- Source: the Department of Disaster Prevention and Mitigation (DDPM), Ministry of Interior, released as S1 File of
  Simmachan et al. (PLOS ONE, published 2022-11-17). Methods, "Data": "In 2015, DDPM reported 25,586 RTAs from emergency
  aid requests for crash accident victims at the provincial and district levels. Complete data were available for 20,229
  cases." The Data Availability statement says "the entire data set is publicly available at the Open Government Data of
  Thailand"; that page returned 403, so whether it holds all 25,586 crashes (and its year, PROV-9) is not checked. As
  published: 20,229 crashes x 8 columns (ID, Month, Death, Roadway_Class, Road_surface, Road_section, Weather_condition,
  Light_condition; header checked on a preview today), coded per S1 Table. Earlier AI triage, 2026-10-19, measured 72.4%
  crashes without a death and 1,165 distinct covariate cells.
- Use case: for example a road authority choosing road sections to treat from expected deaths per crash; the paper names
  no actor (its aim: "This study investigated the factors that contribute to RAFs using various count regression
  models", Abstract), so the fit is approximate. Regime: temporal by nature (a model serves later crashes, SPLIT-6),
  possible only on the month of one year (three monthly windows at the year's end); the record's IID would be forced
  from temporal (SPLIT-8).
- Siblings and duplicates: `thailand_road_accident_register_2019_2022` (TBD -> Yes, priority 3, AI draft) is the
  Ministry of Transport's TRAMS register of crashes on its own network, 2019-2026, with province, vehicle, cause and
  coordinates. Another agency (not the same ministry), other years and other columns: not the same original source
  (PROV-4) and not a cut of one dataset (PROV-6). It is the same task, though, so the 2015 table adds no distinct task
  and only one of the two should ship: the register (81,735 dated crashes; earlier AI probes gave AUC 0.83 and Poisson
  D^2 0.26 there against 0.71 and 0.12 here). Other crash-severity candidates: `nhtsa_crss_crash_severity`,
  `chicago_traffic_crashes`, `nyc_motor_vehicle_collisions` (TBD -> Yes, AI drafts); `us_accidents` is `No` (Lennart).
  External collections: none found.
- Papers and pages: Simmachan, Wongsai, Wongsai and Lerdsuwansri (2022), PLOS ONE 17(11):e0269022, the paper that
  released the rows (read via PMC9671366); papers using the table not searched.
- Metric: the paper compares count models in sample: "Two of the most extensively used measures are the log-likelihood
  value and Akaike Information Criterion (AIC)" (Methods, "Goodness of fit and model comparison"), with Pearson
  chi-squared and likelihood-ratio tests; no held-out score, so the fallback `rmse` (MET-1, MET-5, MET-11); inputs none.
- Risks for /add-dataset: the complete-case cut drops 5,357 of 25,586 crashes by an unstated rule (the upstream may hold
  them); how long after the crash a death counts is not stated for this table (the Introduction says Thai RAFs are
  "defined for an unlimited period following a crash", for the national reports); no location. None of the family's open
  policy questions applies: a zero is an observed crash without a death.
- Priority: gap + (social science is thin in the coverage snapshot), use case 0 (no actor named), source + (the paper
  documents the data, S1 Table codes it), shape 0 (20,229 crashes, but six coded covariates in 1,165 cells and one
  year), risk - (a richer sibling holds the same task).

**Assessment (AI, 2026-10-30):** to the curator's question ("Is this a duplicate or not?"): not by the rules. DDPM's
emergency-aid records of 2015 and the Ministry of Transport's TRAMS register of 2019-2026 come from different agencies,
years and columns, so neither PROV-4 (the same original source) nor PROV-6 (a cut of one dataset) applies. It is the
same task, though (deaths per crash in Thailand), and `thailand_road_accident_register_2019_2022` (Yes, priority 5,
Andrej, 2026-10-30) holds it with more rows, dates, locations and a stronger signal (AUC 0.83 against 0.71). Recommend
2nd Tier as screened: a second table for the same task adds nothing the register lacks.

CC (2026-10-30, Andrej): `TBD -> 2nd Tier`, priority 2 (the AI screening had `TBD -> 2nd Tier`, priority 2;
zero-inflated screening review page, after the AI's answer to the curator's question). "We do second tier because we
have better data for the same task already )name it=" The better data: `thailand_road_accident_register_2019_2022` (Yes,
priority 5).

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

Lead: the two-regime-zero workbook (v4, 2026-10-19), Master row 17 (Thai road-accident fatalities).
