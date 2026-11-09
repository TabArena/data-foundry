---
unique_name: beef_marbling_nir
name: Near-infrared data for the prediction of beef marbling (handheld SCiO, French and Italian slaughterhouses)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
- Spectral Data
original_source: Other
year: '2023'
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.57745/FRDOJC
- https://doi.org/10.1016/j.meatsci.2023.109169
- https://arxiv.org/abs/2605.21544
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: 832 beef carcasses with a handheld NIR spectrum (331 bands) and the grader's marbling score, from an INRAE deposit with a Meat Science paper; the raw spectra the curator asked for on `tecator`, but small and without the slaughterhouse column.
- Source: Hocquette, Kombolo-Ngah, Goi, Santinello et al. (INRAE, University of Padova), "Near-infrared data for the prediction of beef marbling", Recherche Data Gouv, doi 10.57745/FRDOJC, published 2023-11-04, Etalab 2.0; cited by Kombolo-Ngah et al., "Across countries implementation of handheld near-infrared spectrometer for the on-line prediction of beef marbling in slaughterhouse", Meat Science 200:109169, 2023. As published: one file `Data NIR Marbling.tab`: `AnimalNumber`, `Marbling(MSAscore)` (a second header row reads "Score from 0 to 1100"; the description says the 3G protocol, 100 to 1190 in steps of 10) and reflectance at 740-1070 nm in 1 nm steps, each "the average of the 5 scans" on the Longissimus thoracis; "832 animals from 2 slaughterhouses in France and Italy" (829 in the paper's abstract). A preview of the file shows no slaughterhouse or country column.
- Use case: a slaughterhouse grades each carcass for marbling in the chiller with a handheld scanner instead of a trained grader; the grade sets the carcass's class and price (the paper's conclusion, per its indexed abstract: moderate accuracy, potentially useful for sorting carcasses into MSA marbling classes); fit direct, the target is the grader's score the actor acts on (USE-5). Regime: grouped by slaughterhouse would mirror a new plant, but the group does not ship (check whether `AnimalNumber` ranges separate the two); IID otherwise.
- Siblings and duplicates: `tecator` (`No`, Data Quality Issue; the curator: "rather search for another spectra dataset"); NIR candidates of this run `milk_nir_composition` and `mango_dmc_nir`; spectra records `open_soil_spectral_library` and `lucas_topsoil` (`TBD -> Yes`). No duplicate (grep for marbling, scio, FRDOJC). External collections: possibly the 66-dataset NIR benchmark of Reiter et al. 2026 (arXiv 2605.21544); its dataset list was not read.
- Better data: from the run's search, found as better data for `tecator`, and in the curator's Zotero collection (item 227); no further search this round.
- Papers and pages: Kombolo-Ngah et al. 2023 (abstract: "R2 in external validation between 0.46 and 0.59 and a standard error of prediction between 83.1 and 105.5"); Reiter et al., "Tabular foundation models for robust calibration of near-infrared chemical sensing data", 2026.
- Metric: the paper reports R2 and the standard error of prediction side by side (abstract; the full text was not reachable), so no single deliberate choice: the fallback `rmse` (MET-5, MET-8); inputs none.
- Risks for /add-dataset: raw spectral bins lean out of scope (SEL-15, weighed factor), against the curator's request for a spectra dataset; 832 rows; the missing slaughterhouse column for a grouped split (SPLIT); the target's scale (MSA 0-1100 header against 3G 100-1190 description, USE-5); how the paper formed its external validation set was not read.
- Priority: gap 0 (regression and the domain are not thin), use case + (the paper names on-line grading in the slaughterhouse), source + (an INRAE deposit with a journal paper), shape 0 (832 rows, one feature type), risk - (raw spectra lean out of scope; the grouping column is missing).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `tecator`; the curator's Zotero collection, item 227: "Tabular foundation models for robust calibration of near-infrared chemical sensing data".
- as published: 832 carcasses from 2 slaughterhouses (France, Italy) x a SCiO reflectance spectrum 740-1070 nm at 1 nm (331 bands, mean of 5 scans on the Longissimus thoracis) + marbling score; one file 'Data NIR ...; target: beef marbling score by the 3G (Global Grading Guaranteed) protocol, 100-1190 in steps of 10 (regression); access: open.
- Why: A meat NIR task with raw spectra, the domain of tecator (meat composition from NIR), for which the curator asked for another spectra dataset; open with a journal paper.
- Adds: Raw (not PCA) spectra from a cheap handheld device in an industrial setting; a natural grouped regime (two slaughterhouses, two countries); 3.5x tecator's samples. Caveats: raw spectral bins lean out (SEL-15); the target is a human visual grade, not a chemical fat content; 832 rows; check whether the file carries the ...
