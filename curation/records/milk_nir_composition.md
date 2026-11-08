---
unique_name: milk_nir_composition
name: Near-infrared spectra dataset of milk composition in transmittance mode (on-farm, Hooibeekhoeve, 2017)
checked_by:
- Lennart
data_foundry_status:
- WIP (Triage)
claimed_by: Lennart
suggestion: 'Yes'
priority: 3
tags:
- AI-Filled (Verify)
original_source: Other
year: '2023'
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.5281/zenodo.8263430
- https://doi.org/10.1016/j.dib.2023.109767
- https://arxiv.org/abs/2605.21544
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: 1,224 raw-milk samples from 41 cows over eight weeks, each with a raw on-farm NIR transmittance spectrum (256 wavelengths, 960-1690 nm) and lab reference values for fat, protein, lactose, urea and somatic cells; the raw spectra the curator asked for on `tecator`, with a cow id and timestamps for a grouped or temporal split.
- Source: Diaz-Olivares, van Nuenen, Gote, Fonseca Díaz, Saeys, Adriaens, Aernouts, "Near-infrared spectra dataset of milk composition in transmittance mode", Zenodo, doi 10.5281/zenodo.8263430, published 2023-08-18, CC BY 4.0; data paper in Data in Brief, December 2023 (doi 10.1016/j.dib.2023.109767, PMC10700509). As published: one file `data_table.csv` (11 MB), 1,224 rows x 1,038 columns: `Cow_ID`, `Fat`, `Prot`, `Lact`, `SCC`, `Urea`, `Milk_yield`, `Milk_Interv`, `SET`, five timestamps (`Time_Dark`, `Time_Milk`, `Time_PrevMilk`, `Time_Sample`, `Time_White`), and four blocks of 256 columns (`Trans_Dark`, `Trans_White`, `Trans_Sample` in digital counts; `Trans_Tot`, the "Normalized sample transmittance spectra" in %), per the file header and Table 1 of the paper. "all milk samples being taken from 41 cows", milked by an automatic milking system at the Hooibeekhoeve farm (Geel, Belgium); lab references by MCC-Vlaanderen "following ISO 9622 and ISO 13366-2:2006".
- Use case: the milking robot reads each milking with the on-farm NIR sensor and predicts its composition in real time instead of waiting for the lab ("Monitoring of milk composition can support several dimensions of dairy management such as identification of the health status of individual dairy cows and the safeguarding of dairy quality", abstract); fit direct. One target per task (fat as for `tecator`; protein and lactose are other framings, CLEAN-18). Regime temporal (eight weeks; the paper asks for calibration models that hold "in time"), with the same cows throughout, or grouped by `Cow_ID` (SPLIT-13; decide at /add-dataset).
- Siblings and duplicates: `tecator` (`No`, Data Quality Issue, PCA-preprocessed spectra; the curator: "rather search for another spectra dataset"); `beef_marbling_nir` (`TBD -> Yes`, priority 2, 832 carcasses) and `mango_dmc_nir` (this run), NIR records of other products; `open_soil_spectral_library` and the RamanBench records are other spectra. No other record links 8263430. External collections: the NIR benchmark of Reiter et al. 2026 (arXiv 2605.21544) carries it as Milk_Fat, Milk_Lactose and Milk_Urea (255 bands, Kennard-Stone split; its dataset table).
- Better data: found as better data for `tecator`, and in the curator's Zotero collection (item 227); no further search this round.
- Papers and pages: the Data in Brief paper (read in Europe PMC); Diaz-Olivares, Adriaens, Stevens, Saeys, Aernouts, "Online milk composition analysis with an on-farm near-infrared sensor", Comput Electron Agric 178:105734, 2020 (the related research article, not read); Reiter et al. 2026 (dataset table read).
- Metric: none found: the data paper fits no models and the research article was not read, so the fallback `rmse` in % (MET-1, MET-8); inputs none.
- Risks for /add-dataset: raw spectral bins lean out of scope (SEL-15, weighed factor), against the curator's request for a spectra dataset; pick one spectrum block (`Trans_Tot`; the dark and white blocks are the instrument's reference readings); the other lab values are measured with the target and are not known when the sensor reads (drop, LEAK-10); `Milk_yield`, `Milk_Interv` and the times are known at milking; Reiter et al. list Milk_Fat with 402 samples against 1,224 for lactose and urea, so fat may have missing or removed values (check).
- Priority: gap 0 (regression is not thin), use case + (the source names real-time on-farm monitoring), source + (a deposit with a data paper and a research article), shape + (1,224 samples with a cow id and timestamps), risk - (raw spectra lean out of scope).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `tecator`; the curator's Zotero collection, item 227: "Tabular foundation models for robust calibration of near-infrared chemical sensing data".
- as published: 1,224 raw milk samples x NIR transmittance spectrum 960-1690 nm (255 bands in the NIR benchmark) + lab reference values; collected on-farm over 8 weeks in 2017 at the Hooibeekhoeve experimental ...; target: milk fat, protein or lactose content (%), urea, somatic cell count (lab reference); one target per task; access: open.
- Why: The curator's comment on tecator asks for another spectra dataset without PCA preprocessing. This is a raw NIR calibration of a food composition quantity (fat, as in tecator) with lab reference values, open under CC BY 4.0, with a data paper.
- Adds: Raw spectra instead of PCA scores; 5x tecator's 240 samples; several lab targets on the same spectra (fat, protein, lactose, urea, SCC); a dated on-farm collection. Caveats: raw spectral bins lean out (SEL-15); samples are likely repeated per cow over 8 weeks (check for a cow id and date for a grouped or temporal ...

CC (2026-11-08, Lennart): accepted for adding (`Yes`) in the screening review of the large candidates (most rows, most features).
