---
unique_name: carbonfluxbench_flux_tower_upscaling
name: CarbonFluxBench / CarbonBench (daily eddy-covariance fluxes of 479 towers, spatial upscaling benchmark)
checked_by:
- Andrej
suggestion: TBD -> Yes
priority: 2
decision_markers:
- Needs extensive data wrangling
tags:
- Non-IID (Grouped)
original_source: Other
year: '2026'
domain: environmental science & climate
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://huggingface.co/datasets/alexroz/CarbonFluxBench
- https://github.com/alexxxroz/CarbonFluxBench
- https://arxiv.org/abs/2603.09868
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (v4 of 2026-10-19, a list of 69 candidates, not in the repository), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `TBD -> Yes`, priority 2: daily carbon fluxes at eddy-covariance towers never seen in
training, from weather and MODIS drivers, a benchmark built for a site-grouped split on which LightGBM is competitive
for GPP; not zero-inflated, and the MODIS inputs need a modality call.
- Source: Rozanov, Renganathan, Zhang and Kumar (2026), "CarbonBench: A Global Benchmark for Upscaling of Carbon Fluxes
  Using Zero-Shot Learning", arXiv:2603.09868 (v1 10 March 2026, v2 13 August 2026; v2 HTML read), data on Hugging Face
  `alexroz/CarbonFluxBench`, code on GitHub. v2 abstract: "over 1.1 million daily observations from 474 flux tower sites
  globally (2000-2024)" (v1: 1.3 million and 567 sites). Targets GPP, RECO and NEE from FLUXNET, AmeriFlux, ICOS and
  JapanFlux processed with ONEFlux (Sec. 4.1); drivers: 150 ERA5-Land variables (Sec. 4.3), MODIS MOD09GA bands averaged
  over "a 2 km × 2 km window ... centered on the tower location" (Sec. 4.2), IGBP and Köppen classes, latitude and
  longitude. Earlier AI triage (2026-10-19) measured `target_fluxes_v2.parquet`: 1,262,112 site-days; exact zeros 0.000%
  for GPP and NEE and 0.53% for RECO; NEE negative on 49% of days.
- Use case: Sec. 1: upscaled flux fields are "needed for climate policy, carbon accounting, and calibration and
  validation of Earth system models"; for example a carbon-budget team estimating daily GPP where no tower measures. No
  actor or decision named; fit approximate (a tower footprint stands for a grid cell). Regime grouped by site: "a
  hold-out strategy that partitions sites rather than time steps" (Sec. 2.1.1), stratified by IGBP (371 training and 103
  test sites) or Köppen (379 and 95) (Sec. 5.2). No tower at a new site, so no lagged flux; lagged drivers are fine.
- Siblings and duplicates: none in the records (searched flux, FLUXNET, eddy, GPP); FLUXNET2015 and AmeriFlux have no
  record of their own. External collections: none found (the paper is itself a benchmark).
- Papers and pages: arXiv:2603.09868; the Hugging Face card and README, whose counts differ (card 573 sites and
  1,405,813 rows, README 474 and 1.1M, per the earlier triage). Sec. 6.1: "LightGBM is competitive with temporal models
  on GPP under both splits"; TAM-RL and a CT-LSTM lead the median GPP and RECO results.
- Metric: R², RMSE and normalised MAE computed per site and reported as quartiles over the test sites (Sec. 5.1), none
  named as the ranking criterion: the fallback `rmse` (MET-5); a per-site score would need the site id as a scoring
  column (MET-2). Test rows are only "high-quality observations" (`NEE_VUT_USTAR50_QC = 1`, Sec. 5.1).
- Risks for /add-dataset: whether MODIS reflectance averaged around the tower falls under the remote-sensing exclusion
  (SEL-13 against SEL-15 and SEL-2: upscaling is done in practice with tree models on such per-site drivers; a curator
  call; ERA5 and site metadata alone still make a task); the target: NEE is measured, GPP and RECO come from night-time
  partitioning, a model of night NEE against temperature, so RECO is close to a function of the temperature drivers
  (USE-5, SEL-5); joins of the target file with MODIS (474 MB) and ERA5 (5.0 GB) by site and day; the QC filter on test
  rows. Not a two-regime-zero target.
- Priority: gap 0, use case 0 (no actor), source + (paper with a data section), shape + (about 1.2M site-days at 474
  sites, 150+ drivers, grouped), risk - (modality call, partitioned targets, heavy joins).

**Assessment (AI, 2026-10-30):** tag `Two-Regime Zeros` removed under the curator's definition of the tag (Andrej,
2026-10-30, policy question 4 of the zero-inflated review: "If the low value is by far the most frequent one and
independent of the remaining target distribution, then we can treat it as two regime zero, otherwise not"). Measured on
`target_fluxes_v2.parquet` (1,262,112 site-days): no value of GPP, NEE or RECO holds more than 1.1% of the site-days,
and NEE is negative on about half of them, so the target has no low-value regime. The record stays a candidate on its
merits (policy question 2: any relevant predictive task, zero-inflated or not). New for /add-dataset: -9999 is a
missing-value code on 4.43% of the GPP and RECO rows and 1.39% of the NEE rows.

**Assessment (AI, 2026-10-30):** to the curator's question ("Is this a tabular dataset or is the actual task better
solved with another modality model?"): tabular. A row is a tower-day with numeric drivers: ERA5-Land weather of the day,
MODIS reflectance and indices averaged over the tower's footprint (numbers, not images) and site metadata (IGBP class,
coordinates). The paper's competitors are temporal deep models over the daily sequence, not image models, and it finds
LightGBM "competitive with temporal models on GPP" (Sec. 6.1); flux upscaling in practice runs tree ensembles and small
networks on such tables. The one open point is the MODIS columns: SEL-13 counts remote-sensing spectra as image-derived,
while SEL-15 and SEL-2 argue for instrument readings used as tabular inputs; ERA5 and site metadata alone still make the
task. Recommend TBD -> Yes as screened, with the MODIS columns a call at /add-dataset.

CC (2026-10-30, Andrej): `TBD -> Yes`, priority 2 (the AI screening had `TBD -> Yes`, priority 2; zero-inflated
screening review page, after the AI's answer to the curator's question).

Daily eddy-covariance fluxes (GPP, RECO, NEE) of 479 towers from AmeriFlux, FLUXNET2015, ICOS and JapanFlux,
1991-2024, with MODIS reflectance and ERA5-Land drivers (University of Minnesota). The paper builds it for "zero-shot
spatial transfer in carbon flux upscaling" (abstract) with "a hold-out strategy that partitions sites" (Sec. 2.1.1),
i.e. a regression grouped by site, and finds LightGBM "competitive with temporal models on GPP" (Sec. 6.1).
Downloaded `target_fluxes_v2.parquet` on 2026-10-19: 1,262,112 site-days, -9999 for missing (4.4% for GPP and RECO,
1.4% for NEE). The feature files (MODIS 474 MB, ERA5 5.0 GB) were not downloaded.

Not a zero-regime dataset: exact zeros are 0.000% for GPP and NEE and 0.53% for RECO, and NEE is negative on 49% of
the days. The paper's "zero at night" is about the sub-daily cycle. It stays a candidate on its merits, not as part of
this family. To check: whether MODIS reflectance at the tower pixel falls under the remote-sensing exclusion (ERA5
and site metadata alone still make a task); the target (NEE is measured, GPP and RECO come from partitioning); testing
on QC = 1 rows as the paper does (Sec. 5.1); site and row counts, which differ between the card (573 sites,
1,405,813 rows), the README (474, 1.1M) and the file. Licence: MIT on the repository; the flux data keep their
networks' policies (AmeriFlux requires site citations).

## Reference

Rozanov A., Renganathan A., Zhang Y., Kumar V. (2026). CarbonBench (released as CarbonFluxBench). arXiv:2603.09868.

Lead: the two-regime-zero workbook (v4, 2026-10-19), Master row 25 (CarbonFluxBench).
