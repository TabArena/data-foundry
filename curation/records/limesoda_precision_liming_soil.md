---
unique_name: limesoda_precision_liming_soil
name: Precision Liming Soil Datasets (LimeSoDa)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
- Tiny Data
original_source: Other
year: '2025'
domain: environmental science & climate
problem_type: Regression
original_data_state: Other
source_links:
- https://doi.org/10.5281/zenodo.14932572
- https://doi.org/10.1016/j.geoderma.2025.117337
- https://github.com/JonasSchmidinger/LimeSoDa
- https://github.com/a11to1n3/LimeSoDa
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: LimeSoDa, 31 field- and farm-scale soil datasets (30 to 460 lab-analysed samples each) with SOC or SOM, pH and clay as targets and dataset-specific sensor features, published as an open ML benchmark collection with fixed folds; real and documented, but every set is tiny, 13 sets are raw spectra, and the sets to ship have to be picked.
- Source: Schmidinger et al., "LimeSoDa: A dataset collection for benchmarking of machine learning regressors in digital soil mapping", Geoderma 459:117337 (2025, https://doi.org/10.1016/j.geoderma.2025.117337; preprint arXiv 2502.20139, read); Zenodo "Precision Liming Soil Datasets (LimeSoDa) Zenodo Repository" (concept https://doi.org/10.5281/zenodo.14932572, v1.0.1 = 10.5281/zenodo.14936177, CC BY-SA 4.0), R and Python packages. As published: "In total, the combined datasets include 3,174 soil samples but sample sizes of individual datasets range from 30 to 460 samples", "pre-determined folds for cross validation (CV) are provided for each dataset"; Table 1 lists per set the location, area, samples, features, sensors and the study that used it before (BB.250: Brandenburg, 52 ha, 250 samples, 17 features from DEM, ERa, gamma, pH-ISE, RSS, VI; SSP.460: Sao Paulo, 460 samples, 830 vis-NIR bins). Inclusion criteria: "Precision liming context", targets by "wet chemistry", at least 30 samples, and "We excluded datasets where no learning algorithm outperformed the null model (i.e., with an R2 < 0)".
- Use case: precision liming, the source's inclusion criterion: after a field is sampled, an agronomist maps pH, organic matter and clay across it from the sensor layers to set variable lime rates. Fit direct for the mixed proximal-sensing sets. Regime: within one field the map interpolates between sampled points, so the source's random 10-fold CV mirrors it; the paper notes the spatial debate ("users of LimeSoDa can decide if they prefer other validation strategies that take into account the spatial dependency"), coordinates ship for more than half the sets.
- Siblings and duplicates: `limesoda_bb_250` (unscreened before this batch): the same Zenodo deposit and packages, proposed `No` (`Duplicate`, PROV-4) in this batch, its Zotero paper noted here; `lucas_topsoil` (`TBD -> Yes`, priority 3), `open_soil_spectral_library`, `africa_soil_property_prediction_challenge` (continental surveys and libraries, other sources); `open_soil_data` (`No`). External collections: LimeSoDa is itself a benchmark collection; the sets' earlier studies are named in its Table 1.
- Better data: from the curator's Zotero collection (item 235, arXiv 2608.00608, "From field-scale to large-scale spectral libraries: Tabular foundation models in soil spectroscopy", and, through `limesoda_bb_250`, item 30, arXiv 2508.09888, "Modern Neural Networks for Small Tabular Datasets: The New Default for Field-Scale Digital Soil Mapping?"); both moved here from the source links as papers that used the data (PROV-12); no further search this round.
- Papers and pages: the Geoderma paper (MLR, SVR, CatBoost and RF on 93 tasks); the two Zotero papers above (TabPFN and modern neural networks on the same 31 sets).
- Metric: the paper compares algorithms "on the R2 and the ordinally ranked root mean square error (RMSE)", tunes on "the lowest aggregated RMSE" and tests ranks on the RMSE; on one dataset R2 and RMSE order models the same, so `rmse` (MET-5; deliberate). Inputs: none.
- Risks for /add-dataset: tiny sets (TP-5 for regression: 25 test rows per fold on BB.250, 3 on the smallest); raw vis-NIR, NIR and MIR bins in 13 sets lean out (SEL-15, weighed -), and remote-sensing bands (RSS, VI) need a call under SEL-13 against SEL-15; three targets per set (one task per target, or `Multi-target`; CLEAN-18); a collection selected for predictability (the R2 < 0 exclusion); each set is its own task, so the curator picks which enter (BB.250, G.150, MG.112, SA.112 carry mixed proximal sensors).
- Priority: gap 0 (environmental regression is covered), use case + (precision liming named by the source), source + (Geoderma paper, Zenodo deposit with folds, packages), shape 0 (30 to 460 samples per set), risk - (tiny sets, spectra, the pick of sets).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 235: "From field-scale to large-scale spectral libraries: Tabular foundation models in soil ...".
- as published: 31 field- and farm-scale datasets (Brazil, Germany, Australia, Japan, US and others), one lab-analysed soil sample per row, 30 to 460 samples per dataset. Features vary per dataset: DEM, apparent ...; target: lab-measured soil organic carbon or organic matter, pH and clay content (three regression targets per dataset); access: open.
- Why: A documented, open benchmark of real field surveys for a soil-mapping task still done today. The field's own models are tabular learners (Cubist, RF, TabPFN), and coordinates allow a spatial grouped split.
- Adds: Field-scale soil mapping with mixed proximal-sensor features, distinct from the library-scale spectra in open_soil_spectral_library and lucas_topsoil. Risk: every dataset is small (the largest are SSP.460 vis-NIR and BB.250 mixed sensors), so Too Small (TP-5) has to be checked, and raw spectral bins weigh against the ...
