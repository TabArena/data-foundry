---
unique_name: metro_manila_village_weekly_dengue
name: Weekly dengue incidence and environment, Metropolitan Manila villages 2009-2013 (Francisco et al. 2024)
checked_by:
- Andrej
suggestion: 'Yes'
priority: 3
tags:
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
- '# Dryad deposit: one CSV and a README (the version shown is of 2025-12-04)'
- https://doi.org/10.5061/dryad.x3ffbg7ss
- '# The paper that defined the task and cites the deposit'
- https://doi.org/10.1371/journal.pntd.0012599
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (v4 of 2026-10-19, a list of 69 candidates, not in the repository), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `TBD -> Yes`, priority 3: weekly dengue incidence of 437 Manila villages from lagged
satellite weather and static land use, with the source's own split (train 2009-2012, test 2013) and an actor the source
names; TP-10 decides at /add-dataset whether the panel is in scope.
- Source: Francisco, Carvajal and Watanabe (2024), PLOS NTD 18(10):e0012599 (published 2024-10-21), with the table on
  Dryad (doi:10.5061/dryad.x3ffbg7ss; the landing page shows only the version of 2025-12-04, version 4, while the paper
  already cites the DOI). Cases: "The total numbers of weekly reported dengue cases from January 2009 to December 2013
  for each of the 437 villages were obtained from the National Epidemiology Center, Department of Health, Philippines"
  (Methods, "Epidemiological data"). As published (Dryad README, one CSV of 31.3 MB): ID, Year, week, City, Village, the
  target `LogDenIncd`, eight satellite covariates at one lag each (tmin_L16, tmax_L17, tmean_L17, ndvi_L0, gpm_L6,
  nw_L5, ew_L11, rh_L4), 23 land-use shares, road density and flood risk; no lagged dengue. The target is the incidence
  per 10,000 "converted to the natural logarithm [log (n + 1)]" (Methods). Rows from the paper (Table 1, week-village):
  90,896 training (64,917 zeros, 71.4%) and 22,724 test (14,957 zeros, 65.8%). Not downloaded: Dryad answers 401 to file
  downloads through its API.
- Use case: named by the source: "a binary prediction of the presence or absence of dengue can be instrumental for local
  health authorities in planning targeted interventions" (Methods): a city health office, some weeks ahead, deciding
  where to send vector control. The fit is direct once `ndvi_L0` is lagged or dropped; the lead time is not stated, and
  the smallest other lag (4 weeks) sets it. Regime temporal: "Data from 2009 to 2012 were used for training, and data
  from 2013 were used for model validation" (Abstract), and a model serves later weeks of the same villages (SPLIT-6;
  known entities, USE-10, SPLIT-13).
- Siblings and duplicates: `opendengue_case_counts` (a case-count compilation without predictors, `No`, the reject check
  stands) stops at admin level 2, so it does not hold these village-weeks; `outsmarting_outbreaks_challenge` (TBD -> 2nd
  Tier) is another disease panel (Tanzanian hospital-months). Related work, not a record: Carvajal et al. 2018 (BMC
  Infect Dis, doi:10.1186/s12879-018-3066-0) on Manila's weekly dengue from weather. External collections: none found.
- Papers and pages: the paper above (read via PMC11527386: Methods, Tables 1 and 4, the review history); no other user
  of the Dryad table found.
- Metric: the paper scores the quantitative models by RMSE, R^2 and its own standardized adjusted R^2 (S-Ra^2, to
  compare resolutions), the presence models by AUC, and the hybrid by HAI, "a novel weighted average measure that
  combines the AUC and S-Ra 2 measures" (Methods; Tables 1 and 4). Several metrics with none chosen for one resolution,
  so the fallback `rmse` on the shipped log(n + 1) scale, the scale of the paper's RMSE (MET-3, MET-5); inputs none.
- Risks for /add-dataset: TP-10 leg 1 is open: the land-use columns are constant per village, so the model may not beat
  each village's own seasonal profile (the paper's best week-village R^2 is 0.117, Table 1); leg 2 holds (no lag of the
  target among the columns, tabular models). The lags were chosen by "A cross-correlation analysis using the entire data
  from 2009–2013" (Methods), test year included: a weak selection leak to note or redo on the training years (LEAK-30).
  `ndvi_L0` is the same week's NDVI (LEAK-10 at a forecast moment). Population denominators are interpolated from the
  2010 and 2015 censuses. A zero is a week without a notified case in passive surveillance, mostly suspected or probable
  cases: the coded-zeros policy question applies only weakly (a reported absence, not a filled gap). The satellite
  covariates are physical quantities per village (degrees C, mm/h, an index), measurements rather than image descriptors
  (SEL-15 against SEL-13), for the curator to confirm. Rows, columns and zero share to verify on the file.
- Priority: gap 0 (medical, regression and temporal are not thin), use case + (the source names local health authorities
  and targeted interventions), source + (the paper's methods and the Dryad README document every column), shape + (about
  113,600 village-weeks, 33 covariates, temporal with recurring villages), risk - (TP-10 leg 1 untested, the selection
  leak, the file not measured).

**Assessment (AI, 2026-10-30):** TP-10 leg 1, which the curator asked to test before deciding ("Test the leg, then
decide."), could not run: the table is only on Dryad (doi:10.5061/dryad.x3ffbg7ss, version of 2025-12-04, CC0;
`Weekly_dengue_incidence_env_data.csv`, 31,284,423 bytes, and a README), and Dryad's download routes need a login (HTTP
401 without a bearer token). No other copy exists: Zenodo, the paper's supplement (figures, documents and videos only)
and the author's GitHub (`Micanaldo/Hybrid-Machine-Learning-Model`, a README only). The paper does not answer the leg:
it reports no naive, seasonal or persistence baseline, and its best village-week result (RMSE 0.161, R^2 0.117, Table 1)
is measured against the 2013 mean, not each village's own history. Leg 2 holds (no lag of the target among the columns).
Next: download the CSV by hand from https://datadryad.org/dataset/doi:10.5061/dryad.x3ffbg7ss; the test (village-level
naive forecasts against LightGBM on the 2011-2013 test years) is scripted and runs once the file is there.

CC (2026-10-30, Andrej): `TBD -> Yes`, priority 3, as screened (verified on the zero-inflated screening review page).
"Test the leg, then decide."

CC (2026-10-30, Andrej): `TBD -> 2nd Tier`, priority 3, in chat: "Put the manila dataset to a 2nd tier if we need to
manually download it". The Dryad file needs a manual download (see the Assessment above).

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

CC (2026-11-02, Andrej): "try the Dryad route and, if it works, put it back to Yes"

**Assessment (AI, 2026-11-02):** The Dryad route works without a login or token: the version download of Dryad's API,
https://datadryad.org/api/v2/versions/411989/download (version 4 of 2025-12-04, found through
`/api/v2/datasets/doi%3A10.5061%2Fdryad.x3ffbg7ss/versions`), redirects to a zip of both files, the route of
`pennsylvania_oak_hickory_regeneration_experiment` and `boreal_postfire_lichen_biomass`.
`Weekly_dengue_incidence_env_data.csv` is 31,284,423 bytes with SHA-256
a7ba83fc8cdb1b0533420e2d29f9d6100652ca9524b75b223c982cceb3a89865, equal to the size and digest Dryad lists; the README
also matches its digest. 113,620 data rows and 36 columns (437 villages x 260 weeks). Raw in
`local-data-warehouse/metro_manila_village_weekly_dengue/dryad_x3ffbg7ss_v20251204/`. The manual-download reason for
2nd Tier no longer holds; TP-10 leg 1 is still to test at /add-dataset.

## Reference

Francisco M.E., Carvajal T.M., Watanabe K. (2024). Hybrid machine learning approach to zero-inflated data improves
accuracy of dengue prediction. PLOS Neglected Tropical Diseases 18(10):e0012599. doi:10.1371/journal.pntd.0012599.

Lead: the two-regime-zero workbook (v4, 2026-10-19), Master row 11 (Dengue incidence environment).
