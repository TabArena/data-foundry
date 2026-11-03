---
unique_name: chicago_nmmaps_cvd_mortality
name: NMMAPS daily mortality, weather and pollution for Chicago 1987-2000 (chicagoNMMAPS)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- Time-series (Regression)
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
original_source: Other
year: '2004'
domain: environmental science & climate
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://journal.r-project.org/articles/RN-2004-011/RN-2004-011.pdf
- https://search.r-project.org/CRAN/refmans/dlnm/html/chicagoNMMAPS.html
- https://biostats.bepress.com/jhubiostat/paper44
- https://search.r-project.org/CRAN/refmans/gamair/html/chicago.html
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: one city's daily death counts against same-day weather and pollution (5,114 days), cut from a study built to estimate pollution effects; a single daily series with the open scope question of `rmftsa_ladata`, and the pollutant columns are reconstructions.
- Source: the National Morbidity, Mortality, and Air Pollution Study (Johns Hopkins; Samet et al. 2000), distributed as the NMMAPSdata R package (Peng and Welty, R News 4(2), September 2004): "NMMAPS was a large multi-city time series study of the short-term effects of ambient air pollution on daily mortality and morbidity in the United States"; 108 cities, 1987-2000. The Chicago cut ships in the CRAN package dlnm (`chicagoNMMAPS`): 5,114 rows x 14 columns (date, time, year, month, doy, dow, death, cvd, resp, temp, dptp, rhum, pm10, o3). The full data "used to be available at the Internet-based Health and Air Pollution Surveillance System", and NMMAPSdata and NMMAPSlite are archived (dlnm page).
- Use case: the record's framing (a health agency estimates the cardiovascular deaths expected on a day from its weather and pollution, for heat and smog warnings) is ours; the source estimates effects, not predictions (SEL-3, SEL-8). Fit approximate at best. Regime temporal; one series, no group.
- Siblings and duplicates: `rmftsa_ladata` (`TBD -> Yes` by Lennart, with `Time-series (Forecasting)` and `Wrong Domain / Source Modality`: "seems like a multivariate forecasting task. Unclear if this is the line or borderline, need to finalize") is the record it was found for, the same kind of task (Los Angeles, 1970-1979, six-day averages), so this record should follow that call; `pollution` (`TBD -> 2nd Tier`, 60 areas, 1959-1961) is cross-sectional. gamair's `chicago` data is another cut of the same source (PROV-6). External collections: none known.
- Better data: found as better data for `rmftsa_ladata`; no further search this round.
- Papers and pages: Samet et al. 2000a and 2000b (cited by Peng and Welty, not read); Peng and Welty 2004; the Johns Hopkins Biostatistics working paper 44 (not read); the dlnm and gamair pages.
- Metric: none found (the R News article, the dlnm page; NMMAPS reports effect estimates, not predictions). The fallback `rmse`; inputs none.
- Risks for /add-dataset: scope first: a single daily series with season and trend, where a model can learn the calendar (SEL-10, SEL-11, TP-10); `pm10` and `o3` are "an approximated reconstruction of the original series ... adding the de-trended values and the median of the long term trend. This is the reason they include negative values" (dlnm), a rework that cannot be repaired from the origin while the database is offline (PROV-3, PROV-13); death, cvd and resp are nested counts, so one is the target and the others go (LEAK checks).
- Priority: gap 0, use case 0 (not the source's), source + (NMMAPS documented), shape 0 (5,114 days, but one series), risk - (time-series scope, reconstructed pollutants).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `rmftsa_ladata`.
- as published: Chicago: 5,114 days (1987-2000) x 14 columns (date fields, death, cvd, resp, temp, dptp, rhum, pm10, o3); the full NMMAPS (108 US cities, 1987-2000) is no longer distributed: iHAPSS is offline and ...; target: daily cardiovascular deaths (cvd); all-cause and respiratory deaths also ship; access: open (CRAN dlnm package, GPL).
- Why: same task as rmftsa_ladata (Shumway's Los Angeles cardiovascular mortality from temperature and pollutants): same target and the same kinds of same-day features in a US metro
- Adds: 10x the rows (5,114 daily values against 508 six-day averages), later years (1987-2000 against 1970-1979), daily resolution, three mortality targets. Same SEL-10/TP-10 concern as the old record (a single daily series); pm10 and o3 are reconstructions (NMMAPS de-trended series plus the median trend, can be negative), ...
