---
unique_name: open_soil_data
name: open-soil-data
checked_by:
- Andrej
- Lennart
suggestion: 'No'
decision_markers:
- Data Quality Issue
- Too Small
tags:
- Multi-target
- Non-IID (Grouped)
collections:
- New (BeyondArena)
original_source: Github
year: '2023'
domain: environmental science & climate
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.isda-africa.com/isdasoil/open-soil-data/
- https://github.com/iSDA-Africa/open-soil-data/tree/main
- https://github.com/iSDA-Africa/open-soil-data/blob/main/data/iSDA_soil_data.csv
- https://doi.org/10.1038/s41598-021-85639-y
- https://zindi.world/competitions/rhea-soil-nutrient-prediction-challenge/data
- https://registry.opendata.aws/afsis/
- https://doi.org/10.34725/DVN/QXCWP1
- https://doi.org/10.34725/DVN/66BFOB
- https://doi.org/10.34725/DVN/XUDGJY
- https://doi.org/10.34725/DVN/SPRSFN
- https://github.com/iSDA-Africa/isdasoil-tutorial
source_row: 632
type_adapter_id: curation-record-v1
---

## Comments

Also hosted as a zindi competition: https://zindi.africa/competitions/rhea-soil-nutrient-prediction-challenge/data

Competition evaluation: RMSE of the following elements—Ca, Cu, Fe, K, Mg, Mn, N and Na—accounts for 10% of the total score. B and P each contribute 5%, while S and Zn are weighted at 2.5% each.

CC (2026-09-23, Lennart): **No.** Reasons: (1) 96% of the values are outputs of a MIR-spectroscopy calibration model, not measurements, so the targets are model predictions (`Data Quality Issue`); (2) the wet-chemistry subset that carries real B/P/S/Zn values is ~2,100 rows (`Too Small`); (3) no per-sample dates and no covariates ship, so the only honest framing is spatially grouped digital soil mapping after joining external layers. Temporal tag and split dropped for (3); grouped (spatial) is the applicable regime. What it is: the iSDA "open soil data" GitHub release is one file, `data/iSDA_soil_data.csv`, single commit 2023-03-16, never updated: 49,225 rows x 24 columns (lon, lat, start/end date, source, two depth bounds, 17 Mehlich-3 / combustion soil properties), 37,643 distinct locations, two layers (0-20 cm, 20-50 cm), CC BY 4.0 per the iSDA page. It is not the ~130K/150K iSDAsoil training set: Hengl et al. 2021 (Sci Rep 11:6130, Methods) compiled "more than 100,000 soil sites (unique locations) from over 20 datasets", and this release contains only the AfSIS part.

Decisive facts from the file: (1) `source` has two values, `afsis_spectral` (47,068 rows, 95.6%) and `afsis_wetchem` (2,157). The bulk of the "measurements" are MIR-spectroscopy calibration-model predictions, so a model trained on this file learns to imitate another model, and predicting one nutrient from its siblings means predicting one output of a spectrum from other outputs of the same spectrum. (2) Boron, phosphorus, sulphur, zinc, sodium and EC exist only for the ~2,111 wet-chemistry rows; everything else has ~49k. (3) Every row carries the same date span, 01/01/2008 to 31/12/2018; there is no per-sample date, so a temporal split is impossible and the `Non-IID (Temporal)` tag is unsupported. The natural regime is spatial grouped (Hengl et al. use "spatial fivefold Cross-Validation" with points "<30 km" kept on one side). (4) No covariates ship; the only features are coordinates and depth, so any task is digital soil mapping after joining remote-sensing layers. (5) 42 exact duplicate rows, 1,557 duplicate (location, depth, source) rows.

Zindi "Rhea Soil Nutrient Prediction Challenge" (Feb-Mar 2026, now at zindi.world): 44,298 training samples whose features are "the geo-location, the date, the depth and the extractable amount of each nutrient", i.e. ~90% of this file (inferred from the sizes and columns; the Zindi files and discussions sit behind a login and were not read). Its rule that missing reference values "are denoted with zeroes" and must be predicted as 0 is the wet-chem-only coverage of B/P/S/Zn showing through. Related by provenance, not a duplicate: the 2014 Kaggle "Africa Soil Property Prediction Challenge" (AfSIS MIR spectra -> 5 properties), no record in the backlog.

CC (2026-09-23, Lennart): **Provenance of the spectral predictions, and what "open" covers.** Bounding-box split of the 49,225 rows: Tanzania 28,029 (all but 3 spectral), Ghana 3,991 (all spectral), rest of Africa 17,205 (15,051 spectral + 2,154 wet chem at 9,384 locations). That matches three AfSIS releases on the ICRAF Dataverse, all CC BY 4.0: AfSIS Phase I sentinel-site MIR spectra, "approximately 18,500 soil samples" from 19 countries (DOI 10.34725/DVN/QXCWP1); TanSIS, "29,300 soil samples collected at both 0-20cm, 20-50cm" with ZnSe MIR for 26,772 and a 461-sample wet-chem reference set (DOI 10.34725/DVN/XUDGJY); GhaSIS, 3,433 collected, 3,069 spectra, 210 reference (DOI 10.34725/DVN/SPRSFN). The `afsis_wetchem` rows match the 2,002 archived Phase I samples analysed at Rothamsted 2017-18 (DOI 10.34725/DVN/66BFOB). The same Phase I material sits on AWS (`s3://afsis/`, ODC-By): 1,843 georeferenced samples that have both spectra and wet chemistry (ICRAF, CROPNUTS, RRES labs) plus a `tansis/` prefix; the AWS README says "we only include samples for which there exist both wet and dry chemistry measurements", so the ~48k spectra-only samples are on the Dataverse, not AWS. OSSL compiles AFSIS1 + AFSIS2 paired spectra and reference values as well.

So the inputs (MIR spectra) and the calibration data (~2.7k paired reference samples) are open; the calibration model itself is ICRAF's and not published (Hengl et al. 2021: "iSDA was supported by ICRAF to leverage their extensive spectral calibration libraries"). The iSDA CSV has no sample IDs, so re-joining spectra to rows would go via coordinates and depth. Rebuilding a measured dataset from this means a spectroscopy calibration task: ~1,700 wavenumber bins -> nutrients on ~2.7k reference samples, which is a signal modality with its own benchmark (OSSL) and too small, so it does not change the verdict. On "all data is open": true for the 30 m map layers (AWS `isdasoil` bucket via STAC, CC BY per Hengl et al.), for this 49k point file (CC BY 4.0), and for the AfSIS raw data above; the "over 130,000 soil samples" behind the maps are not released as a set, only "part of the training datasets" are listed (Hengl et al. 2021, Data availability).

CC (2026-09-23, Lennart): Follow-up candidates drafted for the measured-data parents of this family: `open_soil_spectral_library` (spectra -> properties, settles the spectroscopy policy), `africa_soil_property_prediction_challenge` (Kaggle 2014 AfSIS), `africa_soil_profiles_database`, `lucas_topsoil`, `wosis_soil_profiles` (points + covariates -> properties, spatially grouped).
