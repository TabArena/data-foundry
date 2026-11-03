---
unique_name: crms_phragmites_cover
name: Phragmites cover / CRMS herbaceous marsh vegetation, Louisiana coast (Phragmites australis cover per plot visit)
checked_by:
- Andrej
suggestion: 'No'
decision_markers:
- No Good Target / Scientific Discovery
- Needs extensive data wrangling
- Time-series (Forecasting)
tags:
- Two-Regime Zeros
original_source: GOV Website
year: '2026'
domain: environmental science & climate
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.lacoast.gov/crms2/
- https://cims.coastal.la.gov/RequestedDownloads/ZippedFiles/CRMS_Marsh_Vegetation.zip
- https://doi.org/10.1002/eap.70246
- https://cims.coastal.la.gov/RequestedDownloads/ZippedFiles/CRMS_Discrete_Hydrographic.zip
- https://cims.coastal.la.gov/RequestedDownloads/ZippedFiles/CRMS_Soil_Properties.zip
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `TBD -> 2nd Tier`, priority 2: Louisiana's coastal marsh monitoring with 75,418 plot
visits over 20 years; Phragmites cover is zero in 94% of visits, mostly at sites outside its range, and the source
analyses trends; abundance mapping from site covariates is the family's open question.
- Source: Coastwide Reference Monitoring System (CPRA with USGS), which "was designed to monitor the effectiveness of
  restoration actions at multiple spatial scales" at "Approximately 390 sites" (lacoast.gov CRMS home page); bulk
  vegetation download (link live on 2026-10-27, 10 MB zip). As published (earlier AI triage, 2026-10-19, measured on the
  full export): 594,288 rows of species by plot visit, 75,418 visits at 4,619 stations of 401 sites, July 2006 to July
  2026; Phragmites cover 0 in 94.1% of visits, recorded at 97 of 401 sites, 80% of the zero visits at sites that never
  had it.
- Use case: the paper the workbook cites (Guo et al. 2026, Ecological Applications, doi:10.1002/eap.70246; USGS abstract
  only, the publisher answers 403) builds basin-level cover trajectories for 2006-2023 and, by the abstract, recommends
  basin-specific early-warning monitoring of cover with soil and pore-water indicators to guide management. For example
  a coastal manager ranking stations for Phragmites control from soil and salinity; the source makes no per-plot
  prediction. Fit approximate. Regime grouped by site for mapping, or temporal for an early warning (one regime, by the
  use case, SPLIT-3).
- Doubt: the earlier pass set `No` (a monitoring table without a task). The aim is trend analysis, but the network is a
  broad survey with habitat covariates in its own database, so the open species-abundance-mapping question applies; no
  fast reject.
- Siblings and duplicates: no other CRMS record (searched CRMS, lacoast, Phragmites). External collections: none found.
- Papers and pages: the CRMS pages; Guo et al. 2026 (abstract on usgs.gov).
- Metric: none found (trend trajectories, USGS abstract); fallback `rmse` on percent cover.
- Risks for /add-dataset: soils, pore-water salinity and hydrology sit in other CIMS tables, joined by station and date
  (heavy joins); same-visit total cover, other species' cover and the community class are co-measurements of the target
  (LEAK-10); most zeros are structural, outside the species' range, which a site filter or a range covariate decides;
  CRMS does not tell the invasive lineage from the native one (USGS abstract).
- Priority: gap 0, use case 0 (no per-plot decision in the source), source + (state program and a paper), shape +
  (75,418 visits, 401 sites, 20 years), risk - (joins across CIMS tables, co-measured columns).

**Assessment (AI, 2026-10-30):** The family's question on species-abundance mapping is settled without a new rule
(Andrej, 2026-10-30, policy question 1 of the zero-inflated review: "I don't think there is new rule to build here.
These are per dataset judgement calls and if a dataset is useful for a predictive application although the data was
collected for something else, then this is fine"), as SEL-2 already reads the scope rules: this record is judged on its
own use case. The verdict and priority stay.

CC (2026-10-30, Andrej): `Yes`, priority 4 (the AI screening had `TBD -> 2nd Tier`, priority 2; zero-inflated screening
review page).

Louisiana's Coastwide Reference Monitoring System (CPRA with USGS): vegetation of 4 m2 marsh plots. Downloaded the
full export on 2026-10-19 (10 MB zip, 250 MB long CSV, one row per species per plot visit): 594,288 rows, 75,418
plot visits at 4,619 stations of 401 sites, July 2006 to July 2026, about 3,800 visits a year. A monitoring table
without a prediction task; the 2026 study the workbook cites analyses expansion trends and impacts (abstract summary
only, text not read). A plot-level model would need site hydrology and soils joined from other CIMS tables, and the
same-visit columns (total cover, other species, community class) are co-measurements of the target.

Zero mechanism, confirmed from the data: Phragmites cover is exactly 0 in 94.1% of visits (4,476 visits with cover).
Only 97 of 401 sites ever record it, and 80% of the zero visits are at sites that never had it, so most zeros are
structural absence from the species' range and the rest absence from the plot; 2,576 "Out" rows (seen near the
plot) carry no cover. Workbook pushback: the table is downloadable, and no zero-inflated beta model was found in the
2026 paper's summary. No licence stated beyond a CPRA disclaimer.

**Assessment (AI, 2026-11-01):** added as `datasets/_dev/tabarena-v0pt2/crms_phragmites_cover/` by /add-dataset with the full review panel; the open questions are in its `REVIEW.md`. Recommend `No` (`Time-series (Forecasting)`) under TP-10 as written, after first testing CRMS site hydrology as inputs, unless you amend TP-10: against forecasts fitted on the station series the random forest is only 1.0-1.1% better (its issue 1). Changes after the panel: soil lagged three seasons and joined per variable, a dense-stand flag and estimate, the use case reworded to next-season cover forecasting. Corrections to the screening above: absence from habitat inside the range, not "mostly at sites outside its range"; 4,488 rows, not 4,476. Two CIMS source files are added to the links. The marker `No Good Target / Scientific Discovery` stays until your mark (decided with the other four `Yes` records). Priority 2: gap 0, use case 0, source + (CPRA), shape +, risk - (recommendation not to ship).

CC (2026-11-02, Andrej): TP-10 stays as written (issue 1, (b)): the model must clearly beat the forecasts built from each station's series, fitted ones included, and the random forest comes within 1.1% of a three-number shrinkage of the last value (0.9 standard errors over the windows), so the task is forecasting: `No` (`Time-series (Forecasting)`). The folder leaves the working copy with the dataset's verdict on the review page.

CC (2026-11-02, Andrej): the update is correct (review page verdict): `No` (`Time-series (Forecasting)`) under TP-10 as written; the record takes the definition's `year` (2026, the CIMS download the definition pins) and `required_split` (`Temporal (NON-IID)`). The paper: https://esajournals.onlinelibrary.wiley.com/doi/10.1002/eap.70246.

**Assessment (AI, 2026-11-02):** the paper's page still answers 403 (third attempt), so its claims stay marked as read from the USGS abstract only; with the `No` the question is moot. The folder leaves the working copy (last committed in 902011b3 and before), `v2_path` cleared, the claim released.

## Reference

Coastwide Reference Monitoring System (CRMS), Coastal Protection and Restoration Authority of Louisiana,
https://www.lacoast.gov/crms2/. Guo Y., Roberts B.J., Nyman J.A., Plumlee J.D., Davenport T.M., Hopper G.W., La Peyre
M. (2026). Expansion trends and impacts of Phragmites australis on the Louisiana Gulf Coast. Ecological
Applications. doi:10.1002/eap.70246.

Lead: curation/inputs/two_regime_zero_datasets_v4.xlsx, Master row 9 (Phragmites cover / CRMS).
