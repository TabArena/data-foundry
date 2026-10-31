---
unique_name: global_dams_database
name: Global Dams Database
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
tags:
- AI-Filled (Verify)
collections:
- STRABLE
original_source: Website
year: '2019'
domain: environmental science & climate
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.energydata.info/dataset/global-dams-database
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/global-dams-database
- https://arxiv.org/abs/2605.12292
- https://energydata.info/dataset/83d6a759-ed05-4f23-91ab-a8007d91adaa/resource/e40c7995-672d-4a0c-93e7-afac29bcfb93/download/globaldamsdatabase_global_coverage_november_2020.csv
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source pages, the STRABLE release and a preview of its files; a human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: the World Bank's dam database for floating-solar assessments, compiled from World Bank hydropower projects, the IHA's India data, FAO AQUASTAT and GRanD; reservoir capacity from dam height, reservoir area and site data is an estimate hydrologists make to fill gaps, but no decision is named and the Notes column states capacities.
- Source: World Bank Group (ESMAP), "Global - Dams Database" on energydata.info (https://energydata.info/dataset/global-dams-database), created 2019-12-16, CC BY 4.0, with globaldamsdatabase_global_coverage_november_2020.csv and a metadata workbook (read through the portal's API; the page answers 403 to scripts). The description: "This database contains parameters gathered after an assessment of the technological potential for development of floating solar photovoltaic (PV) projects on existing hydropower dams and other reservoirs ... It also includes data gathered from the FAO's public Aquastat database for Africa ... This dataset also contains data gathered from the public Global Reservoir and Dam Database (GRanD) for Africa." As read by STRABLE: 3,978 dams x 57 columns (127 countries): name, country, river, basin, purpose, status, dam height, reservoir area, year, hydropower and PV fields, the contributing database (FAO, WB, GRanD / FAO and others), notes; target Res_capacityM3 (log1p by STRABLE).
- Use case: none named; the source's purpose is the Floating Solar Atlas, "to enable potential developers or stakeholders to quickly navigate to the site of interest and obtain information about the potential for development of a floating solar PV project". Estimating a reservoir's storage where no survey value exists is the nearest use, approximate. Regime: IID over dams, or grouped by country or basin.
- Siblings and duplicates: none among the records (searched dams, reservoir capacity, GRanD). Many rows come from GRanD and FAO AQUASTAT, the first publications of their capacities (PROV-8, to trace per row). External collections: STRABLE ("Global Dams Database", App. C.2: "to predict dam capacity").
- Better data: a candidate of the benchmark STRABLE (the run searched no further).
- Papers and pages: the energydata.info page and its metadata workbook; GRanD (Lehner et al. 2011) for the GRanD rows; STRABLE (arXiv 2605.12292, App. C.2 and D.1).
- Metric: none found (the World Bank page defines no prediction task), so the fallback `rmse` on log capacity; STRABLE scores R^2 (App. D.1) (MET-1).
- Risks for /add-dataset: Notes states capacities in text ("Does not retain water but initial capacity = 6.13 million m3") (LEAK); zeros stand for unknown in Dam_hgt, Res_area_km2 and other numeric fields (CLEAN); the description says Africa and India while the 2020 file spans 127 countries (to check); capacities copied from FAO and GRanD (PROV-8); encoding damage in names ("Electricit?? de Guin??e").
- Priority: gap 0 (environmental science & climate), use case 0, source + (World Bank page with a metadata workbook), shape + (3,978 dams, 56 mixed columns), risk - (the Notes leak and zeros for unknown).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 3,978 rows x 57 columns incl. target (STRABLE parquet); target: Res_capacityM3.
- Why: Predict a dam's reservoir capacity (m3) from its structural and location record
- Notes: Raw file globaldamsdatabase_global_coverage_november_2020.csv (energydata.info). The original compiler of the database is not pinned down here.
