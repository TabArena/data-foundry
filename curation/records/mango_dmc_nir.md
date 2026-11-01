---
unique_name: mango_dmc_nir
name: Mango DMC and NIR spectra (Anderson et al.)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
original_source: Other
year: '2020'
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.1016/j.postharvbio.2020.111202
- https://doi.org/10.17632/46htwnp833
- https://data.mendeley.com/datasets/46htwnp833/3
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: about 11,000 NIR spectra of intact mangoes with the measured flesh dry matter, over several seasons, cultivars and regions, published as a benchmark with a season holdout; raw spectral bins (SEL-15 leans out) and replicate scans per fruit are the open points.
- Source: Anderson, Walsh, Subedi and Walsh (Central Queensland University), "Achieving robustness across season, location and cultivar for a NIRS model for intact mango fruit dry matter content", Postharvest Biology and Technology 168:111202, 2020 (Elsevier pages not read); data on Mendeley Data 10.17632/46htwnp833 (v1 2020-03-30; v3 2024-02-06 adds a season used by Walsh et al. 2024, Spectrochimica Acta A 311:124003; v4-v6 of 2024-2026 add `MangoDMC_NIR_Data_v4.csv`, 260 MB, with more instruments and seasons from J. Walsh's 2024 thesis; CC BY 4.0). Previewed (first 6 KB of each file): v3 has `Set, Season, Region, Date, Type, Cultivar, Pop, Temp, DM` and 306 absorbance bands from 285 to 1200 nm (3 nm steps), about 11,300 rows by file size (35 MB); v4 adds `partition_*`, `outlier_flag_1`, `origin`, `population`, `physio_stage`, `reference_no`, `instrument`, `spectra_no`, about 82,000 rows by size.
- Use case: a grower or packhouse measures dry matter with a handheld NIR instrument to judge maturity and eating quality before harvest or sorting; the Mendeley page frames the original as "a real-world case study, where several years of data were used to develop a model and performance was then evaluated using data from the final year"; the actor is not named on the pages read, so fit approximate. Regime temporal by season, as the source prescribes (SPLIT-19).
- Siblings and duplicates: `tecator` (Lennart `No`, `Data Quality Issue`: PCA-preprocessed spectra, "rather search for another spectra dataset"); `beef_marbling_nir` (AI `TBD -> Yes`, priority 2), `milk_nir_composition` (a candidate of this run), `bloodsai_blood_spectroscopy_classification_challenge` (AI `TBD -> 2nd Tier`), `lucas_topsoil`, `open_soil_spectral_library`: other spectra tasks; `mango_mass` (MulTaBench, an image task) is another dataset. No duplicate. External collections: none checked; the curator's Zotero item 227 (NIR calibration with tabular foundation models) may use it (not read).
- Better data: found as a related task next to `tecator`; no further search this round.
- Papers and pages: Anderson et al. 2020; Walsh et al. 2024 (a 1D CNN on the same partition); the Mendeley description (read through its public API).
- Metric: the papers report RMSEP on the held-out season (the chemometrics habit; not read here), the same as the fallback `rmse` on dry matter in percent (MET-1, MET-8); inputs none.
- Risks for /add-dataset: raw spectral bins lean out (SEL-15, a weighed factor); "Each fruit was scanned TWICE ... A subset of 744 samples was scanned at THREE fruit temperatures" (Mendeley): the rows of one fruit stay in one fold (LEAK-17, SPLIT-23), and v3 has no fruit id while v4 has `reference_no`, so v4 may be the file to ship (PROV-6, the curator's choice); `Set` and the `partition_*` columns are the authors' split, not features.
- Priority: gap 0 (no thin domain), use case 0 (actor not named on the pages read), source + (paper and a versioned Mendeley deposit), shape + (about 11,000 spectra over several seasons), risk - (raw spectral bins, replicates without an id in v3).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through a related task next to `tecator`.
- as published: NIR absorbance spectra 309-1149 nm of intact mango fruit with the measured dry matter content, several harvest seasons, cultivars and locations; v3 file NAnderson2020MendeleyMangoNIRDataV3.csv 35 ...; target: dry matter content (%) of the fruit flesh; access: open.
- Why: the curator's comment on tecator asks for another spectra dataset: this is a large, raw (not PCA-reduced) NIR regression of a food composition quantity with a real decision behind it
- Adds: raw spectra instead of PCA scores, tens of times more samples than tecator's 240, a published season-based train/test split (the authors warn against random splits: replicate scans of a fruit)
