# Two-regime-zero candidates: triage summary (2026-10-19)

AI triage, under the `AI (UNVERIFIED)` convention, of the 69 candidates in
`curation/inputs/two_regime_zero_datasets_v4.xlsx` (sheet "Master datasets"; "row" below is the master row). Every new
record carries `AI (UNVERIFIED)`, `AI-Filled (Verify)` and the new vocabulary tag `Two-Regime Zeros`, so the dashboard
filter on that tag lists the family. Nothing here is a human decision.

Method. Each candidate was checked against the 1,290 existing records by name, alias, DOI, source URL and topic. Its
source was then traced (data host, paper text where reachable, licence), and public tables of moderate size were
downloaded into a scratch directory outside the repo and measured: rows, exact-zero share of the target, grouping and
time structure, and for the insurance tables a quick untuned LightGBM probe of the zero and positive parts. Dryad
refuses automated file downloads (API 401, web 403), so Dryad tables were judged from their metadata, README text and
papers and are marked "not downloaded"; row counts given for them are estimates. The workbook was treated as a lead
list. Where the evidence contradicted it, the record says so: UNISOLAR has no night-time zeros (night is coded
missing), the Svalbard DOI is drone imagery, the biotoxin target has no zeros at all (only below-LOQ codes), and the
freMPL tables are cuts of one portfolio rather than seven datasets.

Merges. The 69 rows map to 56 new records and 3 existing ones. Rows 6 (`fremtpl2`), 28-29 (`nyc_taxi_green_dec_2016`)
and 53 (`online_retail`) were already in the log; they got a dated `AI note (two-regime-zero audit, 2026-10-19)` in
their comments and no field changes. Rows 30 and 61 are one table (dataCar = ausprivauto0405, compared row by row),
rows 55 and 56 one source (HDtweedie's `auto` is the `IN_YY` subset of AutoClaim), rows 37 and 38 one study in two
releases, and rows 63-69 one insurer's 2004 portfolio. None of the records touched was claimed by anyone.

| Row | Workbook candidate | Record | Verdict | Split | Rows / zero share | Reason |
|---|---|---|---|---|---|---|
| 1 | New Brunswick depth-to-bedrock | `new_brunswick_depth_to_bedrock` | TBD -> 2nd Tier | Grouped (NON-IID) | not downloaded (no deposit) | Outcrop zeros are structural but 77% come from one survey programme; table not deposited, data statement unread |
| 2 | Sweden depth-to-bedrock | `sweden_depth_to_bedrock` | TBD -> 2nd Tier | Grouped (NON-IID) | not downloaded (no deposit) | Only code is public; `HKDepth` may be an existing depth model (leak) and censored depths need a rule |
| 3 | US FIA forest biomass | `fia_plot_aboveground_biomass` | No | Grouped (NON-IID) | not downloaded (no task table) | Multi-table inventory; plot biomass is an allometric sum of the tree tally; the cited study is county-level estimation |
| 4 | SAV biomass - Upper Mississippi River | `upper_mississippi_sav_rake_biomass` | No | Grouped (NON-IID) | not downloaded (ScienceBase 403) | Method-calibration release; the rake density score is a direct proxy for the weight |
| 5 | MEPS healthcare expenditure | `meps_total_healthcare_expenditure` | TBD -> Yes | Grouped (NON-IID) | 18,919 / 14.0% (2023 file) | Real person-level spending; 289 target-copy columns to drop; probe AUC 0.84 for any spending |
| 6 | freMTPL2 | `fremtpl2` (existing, note added) | Yes | Random (IID) | 678,013 / 96.3% (aggregate amount) | Already in the log; note: 9,116 claimed policies lack a severity row, so the amount target needs a rule |
| 7 | NOAA GHCN-D precipitation | `ghcn_daily_precipitation` | No | Temporal (NON-IID) | 57,632 / 66.7% (one station) | Station observation archive; any target forecasts the station's own series; trace stored as 0 |
| 8 | PV generation / UNISOLAR | `unisolar_la_trobe_pv_generation` | No | Temporal (NON-IID) | 2,731,946 / 0.0% (night is NA) | Generation forecasting; the claimed night-time zeros do not exist in the release |
| 9 | Phragmites cover / CRMS | `crms_phragmites_cover` | No | Grouped (NON-IID) | 75,418 visits / 94.1% | Monitoring table without a prediction task; most zeros are sites outside the species' range |
| 10 | Vernal wetland vegetation | `vernal_pool_restoration_plant_cover` | No | Grouped (NON-IID) | not downloaded (Dryad) | 2 x 2 management experiment with 15 pools |
| 11 | Dengue incidence environment | `metro_manila_village_weekly_dengue` | TBD -> Yes | Temporal (NON-IID) | not downloaded (Dryad); ~113,620 / ~71% from the paper | Village-week incidence from lagged environment, temporal split; target is log(n + 1) of incidence |
| 12 | Bee-sting injuries | `korea_bee_sting_injuries_district_year` | No | Temporal (NON-IID) | not downloaded (not released) | Restricted NEDIS outcome; association study |
| 13 | Western bluebird prospecting | `western_bluebird_nest_box_prospecting` | No | Grouped (NON-IID) | 110 / 16.4% | Playback experiment in 10 vineyards; zeros are a treatment effect |
| 14 | Alpine treeline seedlings | `treeline_seedling_emergence_experiment` | No | ? | not downloaded (Dryad) | Single-site sowing experiment |
| 15 | Magellanic woodpecker / beetle abundance | `magellanic_woodpecker_beetle_emergence` | No | ? | not downloaded (Dryad) | Case-control indicator test |
| 16 | Plains-wanderer abundance | `plains_wanderer_spotlight_counts` | No | Grouped (NON-IID) | not downloaded (Dryad); 249 / ~84% from the paper | Explanatory study; 16 sites, 41 positive surveys |
| 17 | Thai road-accident fatalities | `thailand_road_accident_fatalities_2015` | TBD -> 2nd Tier | Random (IID) | 20,229 / 72.4% | Valid crash-severity task but 6 coarse covariates (1,165 cells); a richer 2019-2022 register exists |
| 18 | Cape Floristic Region plant cover | `cape_floristic_region_family_cover` | TBD -> 2nd Tier | Random (IID) | 180 / 48.9% and 30.6% | Real signal on a tiny methods-paper table; covers pile up at 0.99 and exceed 1 in 21 plots |
| 19 | Lichen percent cover | `athabasca_forage_lichen_cover` | No | Grouped (NON-IID) | not downloaded (not released) | No table released; zero share set by preferential sampling |
| 20 | Wadden Sea Macoma abundance | `wadden_sea_sibes_macoma_abundance` | TBD -> Yes | Grouped (NON-IID) | 59,463 / 56.2% (SIBES) | Paper released no data; re-pointed to the public SIBES survey; grouped R^2 0.36 |
| 21 | OpenDengue | `opendengue_case_counts` | No | Temporal (NON-IID) | 29,873 / 32.6% (national); 2,821,791 / 55.1% (spatial) | Case counts without predictors; some zeros are documented fills |
| 22 | Wildlife Insights camera traps | `wildlife_insights_camera_trap_detections` | No | ? | not downloaded (platform) | Platform of image identifications; no site-level count table |
| 23 | iWildCam / LILA | `iwildcam_2020_camera_trap_species` | No | Grouped (NON-IID) | not downloaded (images) | Image classification; workbook link dead |
| 24 | Freiburg urban wildlife camera traps | `freiburg_urban_mammal_camera_trap_events` | No | Grouped (NON-IID) | not downloaded (Dryad); ~6,884 events | Detection events only (no zeros); the paper's target is an unreleased survey |
| 25 | CarbonFluxBench | `carbonfluxbench_flux_tower_upscaling` | TBD -> Yes | Grouped (NON-IID) | 1,262,112 / 0.0% (GPP, NEE) | Large site-grouped upscaling task; not a zero-regime dataset; MODIS features need a modality call |
| 26 | Marine biotoxin benchmark | `basque_offshore_bivalve_biotoxins` | No | ? | 5,446 raw / 0.0% (93.6% below-LOQ) | Broken benchmark derivative (2 stations, 24 toxins pooled); non-detects coded at the LOQ |
| 27 | Hydrographic benchmark | `basque_offshore_ctd_chlorophyll` | No | Grouped (NON-IID) | 8,195 raw, 4,653 after pipeline / 0.0% | Sensor cross-prediction within casts; no zeros |
| 28 | Taxi tip amount / NYC TLC | `nyc_taxi_green_dec_2016` (existing, note added) | No | - | 581,835 / 15.2% (OpenML 42729) | Already in the log (TLC trip records); card-only copy, so zero tips are real |
| 29 | Taxi green/NYC tip-percentage subsets | `nyc_taxi_green_dec_2016` (existing, note added) | No | - | same as row 28 | Same TLC source and target as row 28 |
| 30 | Insurance ausprivauto0405 | `australian_vehicle_insurance_2004_2005` (merged) | TBD -> Yes | Random (IID) | 67,856 / 93.2% | Same table as dataCar (row 61), compared row by row |
| 31 | Insurance norauto | `norwegian_automobile_insurance_norauto` | TBD -> 2nd Tier | Random (IID) | 183,999 / 95.4% | Four rating factors form 142 cells; 145,367 exact duplicate rows |
| 32 | PV utility-scale dataset (2017-22) | `utility_scale_pv_generation_2017_2022_unidentified` | No | ? | not downloaded (no source) | No traceable source |
| 33 | Dutch vegetation-plot plant cover (OZAB) | `dutch_vegetation_plot_species_cover` | No | ? | not downloaded (Dryad) | Three-species trend estimation; ordinal cover |
| 34 | Palaearctic rear-edge forest birds | `morocco_forest_bird_transect_counts` | No | ? | not downloaded (Dryad) | Biogeographic hypothesis test on ~100-200 transects |
| 35 | Great Lakes marsh birds | `great_lakes_marsh_bird_point_counts` | No | Grouped (NON-IID) | not downloaded (Dryad); ~70-80k rows est. | Trend estimation over a rotating panel |
| 36 | Non-breeding shorebirds in subtropical wetland | `la_paz_shorebird_abundance_disturbance` | No | Grouped (NON-IID) | not downloaded (Dryad) | Disturbance inference at 12 sampling units |
| 37 | Terrestrial lichen - Northwest Territories | `boreal_postfire_lichen_biomass` | No | Grouped (NON-IID) | not downloaded (Dryad) | Fire-recovery chronosequence; biomass is allometric from cover and height |
| 38 | Terrestrial lichen - Saskatchewan | `boreal_postfire_lichen_biomass` (merged) | No | Grouped (NON-IID) | not downloaded (Dryad) | Second regional release of the row-37 study |
| 39 | Fish carcass / Yellowstone Lake benthic invertebrates | `yellowstone_lake_benthic_invertebrates_carcass_experiment` | No | Grouped (NON-IID) | not downloaded (Dryad) | BACI experiment at 4 sites |
| 40 | Green Sturgeon abundance | `sacramento_green_sturgeon_sonar_counts` | No | ? | not downloaded (Dryad) | N-mixture population estimate without covariates |
| 41 | Riparian bird communities / aquatic insect emergence | `south_nation_riparian_birds_insect_emergence` | No | Random (IID) | not downloaded (Dryad) | 24 sites, one visit, community analysis |
| 42 | Oak-hickory forest regeneration | `pennsylvania_oak_hickory_regeneration_experiment` | No | Grouped (NON-IID) | not downloaded (Dryad) | Factorial experiment; the target is a change score |
| 43 | Spontaneous plant diversity in urban wastelands | `qtp_urban_wasteland_plant_diversity` | No | Grouped (NON-IID) | 585 / 56.4% (non-native richness) | Driver analysis; predictors constant within 38 wastelands |
| 44 | Mammal predator-prey camera-trap co-abundance | `southeast_asia_predator_prey_camera_trap_counts` | No | Grouped (NON-IID) | 416 units x 40 occasions / 67.7-98.7% | Species-interaction inference with three covariates |
| 45 | Species abundance from occurrence + presence-only data | `chesapeake_bay_bird_banding_zi_isdm` | No | ? | not downloaded (Dryad) | Public part is presence-only; the zeros (eBird) are withheld |
| 46 | Clarkia sister-species greenhouse fitness | `clarkia_greenhouse_reciprocal_transplant_fitness` | No | Random (IID) | not downloaded (Dryad) | Greenhouse experiment; every feature is a treatment code |
| 47 | Precipitation fusion - Shaoxing | `shaoxing_hourly_precipitation_fusion` | No | Grouped (NON-IID) | not downloaded (not released) | Data statement: not public, on request |
| 48 | Bee brood parasitism | `monte_desert_solitary_bee_brood_parasitism` | No | Grouped (NON-IID) | 529 / 78.2% | All predictors are site-level: 9 effective units |
| 49 | M5 Forecasting - Accuracy (Walmart) | `m5_forecasting_accuracy` | No | Temporal (NON-IID) | 30,490 series x 1,941 days / 68.0% | 28-day sales forecasting of 30,490 series |
| 50 | Car Parts intermittent-demand benchmark | `car_parts_intermittent_demand` | No | Temporal (NON-IID) | 2,674 x 51 months / 71.4% (75.9% zero-filled copy) | Univariate series; one release zero-fills truncated series |
| 51 | Auto intermittent-demand benchmark | `auto_intermittent_demand` | No | Temporal (NON-IID) | 3,000 x 24 months / 22.0% | Univariate series forecasting |
| 52 | RAF aerospace-parts demand | `raf_aerospace_parts_demand` | No | Temporal (NON-IID) | 5,000 x 84 months / 89.8% | Univariate series forecasting |
| 53 | UCI retail-item demand benchmark | `online_retail` (existing, note added) | TBD -> Yes | Temporal (NON-IID) | 541,909 transactions (4,070 items) | Already in the log; the demand series are built from UCI Online Retail |
| 54 | Weather4cast 2023 | `weather4cast_2023_rain_movie_prediction` | No | Custom | not downloaded (registration) | Satellite-image rain nowcasting; workbook link dead |
| 55 | HDtweedie auto insurance | `autoclaim_sas_motor_insurance` (merged) | TBD -> 2nd Tier | Temporal (NON-IID) | 2,812 / 68.3% (the IN_YY subset) | HDtweedie's auto is the IN_YY subset of AutoClaim (row 56) |
| 56 | AutoClaim / cplm motor insurance | `autoclaim_sas_motor_insurance` | TBD -> 2nd Tier | Temporal (NON-IID) | 10,296 / 73.4% | Clear signal (AUC 0.82) but SAS sample data with an unnamed insurer; generated-data checks mixed |
| 57 | Ghana schistosomiasis egg counts | `ghana_schoolchildren_schistosoma_egg_counts` | No | Grouped (NON-IID) | 1,345 / 94.1% | Model-comparison study; 80 positives in 12 communities |
| 58 | Nantucket Sound sea-duck abundance | `nantucket_sound_sea_duck_aerial_survey_counts` | TBD -> 2nd Tier | Temporal (NON-IID) | not downloaded (990 MB zip on Dryad) | Predictive framing with rich covariates, in-sample validation only; zip contents unknown |
| 59 | Svalbard reindeer total-count pixels | `svalbard_reindeer_total_count_pixels` | No | Grouped (NON-IID) | not downloaded (Dryad); >=94% from the paper | Workbook DOI is drone imagery; the pixel table is a population estimate with 4 features |
| 60 | Finnish large-carnivore FWTS | `finland_protected_area_carnivore_track_density` | No | Grouped (NON-IID) | not downloaded (Dryad) | Matched causal design, controls reused |
| 61 | dataCar / insuranceData | `australian_vehicle_insurance_2004_2005` | TBD -> Yes | Random (IID) | 67,856 / 93.2% | Real policy data, zeros observed as no claim; weak signal (AUC 0.64) |
| 62 | swmotorcycle / CASdatasets | `swedish_motorcycle_insurance_wasa` | TBD -> 2nd Tier | Random (IID) | 64,548 / 99.0% | Rating-factor cells, 670 with a claim |
| 63 | freMPL2 | `frempl_french_motor_personal_line` | TBD -> Yes | Random (IID) | 38,300 / 94.7% (freMPL2) | freMPL2 overlaps freMPL1/3/4 (same policies, other guarantee) |
| 64 | freMPL3 | `frempl_french_motor_personal_line` (merged) | TBD -> Yes | Random (IID) | 20,600 / 95.9% (freMPL3) | Same 20,594 policy-years as freMPL1 under another guarantee |
| 65 | freMPL5 | `frempl_french_motor_personal_line` (merged) | TBD -> Yes | Random (IID) | 16,000 / 89.7% (freMPL5) | One of five disjoint tables with one schema (freMPL5-9: 115,200 rows) |
| 66 | freMPL6 | `frempl_french_motor_personal_line` (merged) | TBD -> Yes | Random (IID) | 32,400 / 89.0% (freMPL6) | As freMPL5 |
| 67 | freMPL7 | `frempl_french_motor_personal_line` (merged) | TBD -> Yes | Random (IID) | 26,600 / 89.2% (freMPL7) | As freMPL5 |
| 68 | freMPL8 | `frempl_french_motor_personal_line` (merged) | TBD -> Yes | Random (IID) | 24,000 / 89.9% (freMPL8) | As freMPL5 |
| 69 | freMPL9 | `frempl_french_motor_personal_line` (merged) | TBD -> Yes | Random (IID) | 16,200 / 91.8% (freMPL9) | As freMPL5 |

## Counts

| Verdict | New records (56) | Workbook rows that went into new records (65) |
|---|---|---|
| TBD -> Yes | 6 | 13 |
| TBD -> 2nd Tier | 8 | 9 |
| No | 42 | 43 |

The four rows that went into existing records keep those records' own verdicts: `fremtpl2` Yes (an earlier AI draft),
`nyc_taxi_green_dec_2016` No (Lennart; rows 28 and 29), `online_retail` TBD -> Yes (Andrej).

Markers on the 42 No records (a record can have several): `No Good Target  / Scientific Discovery` 28,
`Time-series (Forecasting)` 8, `Too Small` 7, `No Good Target (yet)` 4, `Not Available (from Paper))` 3, `Image` 3,
`Needs extensive data wrangling` 3, `Data Quality Issue` 1, `Trivial` 1, `Missing source information` 1.

## Not resolved, and why

* Row 32 (utility-scale PV 2017-22): no source could be identified, and the workbook's own deep review failed too.
* Rows 1 and 2 (depth to bedrock): no deposited table, and the data availability statements of both 2026 papers could
  not be read (ScienceDirect and Wiley returned 403). Get the PDFs (Google the exact title plus "pdf") or request the
  tables. Sweden also needs `HKDepth` explained before any rebuild (possible target leak).
* Row 11 (Metro Manila dengue): the Dryad CSV could not be fetched; rows and zero share come from the paper. A manual
  download settles it.
* Row 58 (Nantucket sea ducks): whether the 990 MB Dryad zip holds a segment x survey table with covariates is unknown,
  and it decides between 2nd tier and No.
* Rows 55-56 (AutoClaim): the insurer behind the SAS Enterprise Miner sample is unnamed, Yip and Yau (2005) is
  paywalled, and the quick generated-data checks were mixed.
* Row 25 (CarbonFluxBench): the ERA5 (5 GB) and MODIS (474 MB) feature files were not downloaded, and whether
  tower-pixel reflectance falls under the remote-sensing exclusion is a curator call.
* Row 18 (Cape Floristic Region): what the pile of exact 0.99 values means is undocumented.
* Rows 10, 14-16, 24, 33-42, 45, 46, 59 and 60: Dryad tables not measured. Their verdicts rest on the study design,
  which the row counts would not change.

## Shortlist for the curator

1. `meps_total_healthcare_expenditure`: large, public, measured (18,919 persons, 14.0% zero spending), a real two-part
   target. The work is dropping the 289 expenditure and utilisation columns that copy the target and choosing a
   concurrent or prospective framing.
2. `frempl_french_motor_personal_line`: freMPL5-9 concatenated give 115,200 disjoint policy-years with 89.7% zero claim
   amount and four years of claim history; the negative amounts need a rule.
3. `australian_vehicle_insurance_2004_2005`: the de Jong and Heller car data, 67,856 policies, zeros observed as no
   claim; a weak signal (AUC 0.64 for a claim), as in `forest_fires`.
4. `wadden_sea_sibes_macoma_abundance`: 59,463 SIBES samples at 5,105 stations, 56.2% zeros, a grouped split, but a
   thin feature set.
5. `metro_manila_village_weekly_dengue`: about 113,620 village-weeks with a temporal split; needs the manual download.
6. `carbonfluxbench_flux_tower_upscaling`: a large site-grouped regression, though not a zero-regime dataset.

Next in line: `autoclaim_sas_motor_insurance` (clear signal, provenance open) and the Thai crash table. Its richer
sibling, the Ministry of Transport register 2019-2022 (Kaggle `thaweewatboy/thailand-road-accident-2019-2022`, 81,735
rows), is not in the log and could be opened as a candidate of its own.

## Policy questions the batch raises

* Should zero-inflated regression be a named sub-family? The tag now exists. The probes show what such a slice
  measures: on the six insurance tables an untuned model ranks claimants at AUC 0.64-0.82, but on five of them it
  explains almost none of the amount (R^2 at most 0.03 on log1p and at most 0 on the raw scale; AutoClaim reaches 0.25
  and 0.02), while an oracle that knows which rows are zero reaches R^2 0.96-0.99 on log1p. RMSE on raw amounts is then driven by a few large claims, so the metric (RMSE on the
  raw or the log1p target, or a Tweedie or Poisson deviance) matters more here than elsewhere, and the hurdle check of
  `task_probes.md` (the `forest_fires` case) should be run on any member that is accepted.
* How should below-detection-limit and other coded zeros be treated? The batch has every variant: values below the LOQ
  stored as the LOQ with a "<" flag (biotoxins, 93.6% of rows), trace precipitation stored as 0 next to a "missing
  presumed zero" flag (GHCN), a release that zero-fills truncated series (Car Parts, Zenodo 4656021), documented
  zero-filling of reporting gaps (OpenDengue), night coded as missing instead of 0 (UNISOLAR), and claimed policies
  without a severity row that become false zeros (freMTPL2). A proposal: a zero counts as a zero only when the source
  records it as an observed absence; censored or filled values go back to missing or get a flag, and a target that is
  mostly censored is out.
* Several tables of one portfolio (freMPL1-10; the same Australian car data in two R packages) were listed as separate
  candidates. The rule applied here is one record per underlying data, with the choice of table in the comments.
* Ecology: of the 31 ecological field-study rows, nearly all are hypothesis tests, experiments or trend estimates.
  The open question is whether species-abundance mapping from habitat covariates counts as a prediction task. The
  precedents went No; SIBES, the Great Lakes marsh birds and the Nantucket sea ducks are the cases to settle it on.
* Insurance targets need one convention for the family: exposure as a feature, a weight or an offset, and what to do
  with negative claim amounts (recoveries).

## Checks

Commits on `zero_inflated`: d8fe3e8, 0c3e0ba, 5a181c3, 9db7148 and 137c169, plus the commit that adds this file. After
each batch, `python -m data_foundry.curation.cli validate` found every dropdown value in the vocabulary and
`tests/test_records_integrity.py` passed (23 tests). Before the final push, `pytest -q` passed (780 passed, 177
skipped). `ruff check .` fails with 6,234 errors and `ruff format --check .` would reformat 308 files (ruff 0.15.15;
0.17.1 gives 6,234 and 311). All of them are in notebooks under `datasets/` and in two test files that this branch does
not touch; its diff against `main` is limited to `curation/`. The CI lint step (ruff 0.15.15 on the v2 `dataset.py`
files) passes.
