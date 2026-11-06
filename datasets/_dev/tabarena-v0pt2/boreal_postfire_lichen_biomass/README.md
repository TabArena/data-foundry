---
report_format: data-foundry-report-v2
unique_name: boreal_postfire_lichen_biomass
container_format: 2
checksum: v2:9d001835166aca67bf4e6b51a8c18649be3afa44a81c1e6c64802d07cfbf9e15
build: null
build_stale: false
data:
  n_rows: 2010
  n_features: 7
  dtypes:
    category: 5
    float64: 3
    int64: 1
  n_test_dataset_rows: null
task:
  target: forage_lichen_biomass_kg_ha
  problem_type: regression
  metric: rmse
  metric_origin: fallback
  scoring_columns: null
  split_regime: grouped_non_iid
  stratify_on: null
  time_on: null
  group_on: burn_area
  group_labels: per_sample
  group_time_on: null
  grouping:
    prediction_unit: row
    aggregation: null
    context: none
    n_groups: 216
    test_groups_per_fold:
      min: 72
      max: 72
splits:
  n_repeats: 10
  n_folds: 3
  random_state: 4267
  time_horizon: null
  time_horizon_unit: null
  time_gap: null
  time_gap_unit: null
  n_train:
    min: 982
    max: 1711
  n_test:
    min: 299
    max: 1028
bundle_checks:
  ok: true
  errors: []
  warnings: []
  infos: []
  accepted:
    dataset_duplicate_rows: '532 exact copies, 518 of them at 0: quadrats of one plot
      (482) or of sibling plots that share every input (36), since every input is
      a plot attribute. Each copy stays in one group, so no test row has a copy in
      training (LEAK-18: few features, natural repeats; Andrej, 2026-11-03).'
    dataset_conflicting_duplicate_rows: Quadrats of one plot share their inputs and
      differ in lichen. 32.5% of the target's variance lies within identical inputs
      (28.8% within a plot), a floor no model can go below. Each input vector stays
      in one group (Andrej, 2026-11-03).
decisions:
- The target is the volume-based biomass; the cover-based one is dropped
- Three NT plots take the site sheet's coordinates
---

# boreal_postfire_lichen_biomass

> Generated from [`dataset.py`](dataset.py) by `dataset check` (or `build`). Do not edit this page: change `dataset.py` and re-run the check.

Regression of `forage_lichen_biomass_kg_ha`, scored with `rmse` on grouped splits by `burn_area`. 2,010 rows and 7 features. Source: Other (2021).

Not built yet. The current definition gives checksum `v2:9d001835166aca67bf4e6b51a8c18649be3afa44a81c1e6c64802d07cfbf9e15`.

## In brief

**Question.** How much caribou forage lichen (kg/ha) grows on the ground of a boreal stand of known type, location and time since the last stand-replacing fire, in a burn or unburned area that was not surveyed?

**Use case.** A caribou habitat biologist with the Northwest Territories government or Saskatchewan's Ministry of Environment revises a boreal caribou range plan: today every burn under 40 years counts as disturbed, while NWT monitoring found that forage lichens need 45 to 70 years to recover. From fire records and the forest inventory, the biologist estimates the forage of stands of a given type, ecoprovince and fire age in burns nobody surveyed.

**One row.** One ground quadrat of a survey plot (2,010 quadrats of 516 plots): five 1 x 1 m quadrats per plot in the Northwest Territories (2016-2018), two 2 x 2 m quadrats per plot in Saskatchewan (2015-2016).

**Predicted.** The live biomass of the forage Cladonia lichens in the quadrat, in kg/ha, as the authors estimated it from the lichens' measured cover and height with their allometric equation; 0 in 40% of the quadrats.

**Known at prediction time.** The years since the last stand-replacing fire, the stand type, the plot's coordinates and its ecoprovince, ecozone and jurisdiction, the same for every quadrat of a plot. The age is the survey's own, dated in the field where no fire is recorded, and the stand type the crew's class; a planner has the inventory's coarser values.

**What the test data stands for.** Whole burn scars or unburned areas of the Northwest Territories are held out, and each Saskatchewan plot on its own (its name carries no burn key), so a test quadrat stands for a stand in a burn with no survey; test quadrats lie a median 22 km (NT) and 3.7 km (SK) from the nearest training plot.

**Our changes to the source.** We stack the two regional surveys, repair three plots' coordinates from the authors' site sheet, drop the authors' cover-based biomass, its presence flag and the quadrat labels, and split by burn area where the source fits models to all plots.

> **Use case fit: approximate (a stand-in with a known gap).** The paper's own aim, a forecast of forage lichen for caribou management, but the label is an allometric estimate (one pooled equation; SK's live height taken as 0.76 of the total); rows are quadrats where the planner acts on stands; the survey is a stratified chronosequence with no NT burn younger than 29 years; and the age and stand type are field values, sharper than an inventory's.

## Files in this folder

| file | what it is |
|---|---|
| [`dataset.py`](dataset.py) | The definition, and the only file edited by hand: metadata, reading and cleaning the raw files, feature types and splits. |
| [`REVIEW.md`](REVIEW.md) | The open questions for the curator, removed once they are settled. Not needed to rebuild. |
| [`README.md`](README.md) | This page, generated by `dataset check` and `dataset build`. |

- The curation record, with the triage decision and its sources: [`curation/records/boreal_postfire_lichen_biomass.md`](../../../../curation/records/boreal_postfire_lichen_biomass.md)
- The original source: <https://doi.org/10.5061/dryad.t1g1jwt15>
- The collection this folder belongs to: [`tabarena-v0pt2/README.md`](../README.md) and [`tabarena-v0pt2/CHANGELOG.md`](../CHANGELOG.md)

## Rebuild

`dataset.py` reads its raw files from `local-data-warehouse/boreal_postfire_lichen_biomass/`. To get them:

```text
The data is the two Dryad deposits of Greuel et al. (2021), CC0: doi:10.5061/dryad.t1g1jwt15 (Northwest Territories, version 5 of 2026-05-18) and doi:10.5061/dryad.tb2rbnzzj (Saskatchewan, version of 2021-02-18). Dryad's per-file API answers 401 without a token, but the version download of its API redirects without a token to a zip of each version; the SHA-256 digests below equal those Dryad lists (checked 2026-11-01). The two lichen sheets are also on Zenodo, byte-identical (records 4499194 and 4552434); the NT site sheet is only on Dryad.
mkdir -p local-data-warehouse/boreal_postfire_lichen_biomass && cd local-data-warehouse/boreal_postfire_lichen_biomass
curl -L -o dryad_t1g1jwt15_v20260518.zip https://datadryad.org/api/v2/versions/442103/download
curl -L -o dryad_tb2rbnzzj_v20210218.zip https://datadryad.org/api/v2/versions/105865/download
unzip dryad_t1g1jwt15_v20260518.zip  # All_site_info_NT.xlsx, Destructive_biomass_sample_NT.xlsx, Lichen_data_NT.xlsx, Quadrat_cover_data_NT.xlsx
unzip dryad_tb2rbnzzj_v20210218.zip  # Destructive_biomass_sample_SK.xlsx, Lichen_data_SK.xlsx
sha256sum Lichen_data_NT.xlsx  # 03a3f3f497415fe1843d140aff621941ae2079db3437ef4186699f463d856b90
sha256sum Lichen_data_SK.xlsx  # 74ad1fe59d2a3364e0b78f552a8b0581e8f37cd085ddcf9b222c42bcd81292a6
sha256sum All_site_info_NT.xlsx  # 24493a7427adeecb04c694f515729d90c2a831d44ad2d8fccd453a781e7cdf6c
```

Then, from the repository root:

```bash
.venv/bin/python -m data_foundry.curation.cli dataset check datasets/_dev/tabarena-v0pt2/boreal_postfire_lichen_biomass   # pipeline and checks, no UUID; rewrites this page
.venv/bin/python -m data_foundry.curation.cli dataset build datasets/_dev/tabarena-v0pt2/boreal_postfire_lichen_biomass   # also saves the container and records its UUID
```

Only curators run `build`, when the dataset ships.

## Dataset and task

| field | value |
|---|---|
| source | Other: https://doi.org/10.5061/dryad.t1g1jwt15 |
| year | 2021 |
| domain | biology & life sciences |
| license | CC0 1.0 |
| data_tags | Non-IID, Grouped, Spatial |
| reference | greuel2021predicting |
| rows x columns | 2,010 x 9 |
| task.target | forage_lichen_biomass_kg_ha |
| task.problem_type | regression |
| task.metric | rmse |
| task.split_regime | grouped_non_iid |
| task.group_on | burn_area |
| task.group_labels | per_sample |

**Metric**

| field | value |
|---|---|
| name | `rmse` (standard; takes value; lower is better) |
| origin | fallback: the default for the problem type: the source defines no metric |
| definition | sqrt(mean((y - p)^2)) |
| reason | The paper judges its combined hurdle model in sample by the R2 of a regression of observed on predicted biomass (0.18; Results, 'Combined predictions'), a squared correlation that ignores a bias of the predictions, and reports no held-out error; RMSE on kg/ha, the planner's unit, is kept (Andrej, 2026-11-03). |

<details>
<summary>Feature types: 5 categorical, 0 string, 0 datetime</summary>

- categorical (5): `burn_area`, `stand_type`, `jurisdiction`, `ecozone`, `ecoprovince`
- string (0): none
- datetime (0): none

</details>

<details>
<summary>BibTeX</summary>

```bibtex
@article{greuel2021predicting,
  title = {Predicting patterns of terrestrial lichen biomass recovery following boreal wildfires},
  author = {Greuel, Ruth J. and Degr{\'e}-Timmons, Genevi{\`e}ve {\'E}. and Baltzer, Jennifer L. and Johnstone, Jill F. and McIntire, Eliot J. B. and Day, Nicola J. and Hart, Sarah J. and McLoughlin, Philip D. and Schmiegelow, Fiona K. A. and Turetsky, Merritt R. and Truchon-Savard, Alexandre and van Telgen, Mario D. and Cumming, Steven G.},
  journal = {Ecosphere},
  volume = {12},
  number = {4},
  pages = {e03481},
  year = {2021},
  doi = {10.1002/ecs2.3481},
  note = {Data: \url{https://doi.org/10.5061/dryad.t1g1jwt15} (Northwest Territories) and \url{https://doi.org/10.5061/dryad.tb2rbnzzj} (Saskatchewan), CC0}
}
```

</details>

## Sample rows

The first 5 of 2,010 rows of the final frame (random rows: the frame is shuffled). Cells are cut at 40 characters.

| forage_lichen_biomass_kg_ha | years_since_fire | stand_type | latitude | longitude | jurisdiction | ecozone | ecoprovince | burn_area |
|---|---|---|---|---|---|---|---|---|
| 556.876 | 34 | Jack pine | 58.0974 | -104.373 | SK | Boreal shield | Athabasca Plain and Churchill River Upl… | area_083 |
| 9.47498 | 43 | Jack pine | 62.67 | -116.18 | NT | Taiga plains | Great Bear Plains | area_011 |
| 37.8999 | 66 | Jack pine | 60.77 | -116.56 | NT | Taiga plains | Hay and Slave River Lowlands | area_012 |
| 0 | 36 | Deciduous | 62.98 | -115.83 | NT | Taiga shield | Coppermine River and Tazin Lake Uplands | area_015 |
| 12.6333 | 40 | Conifer mix | 60.69 | -115.93 | NT | Taiga plains | Hay and Slave River Lowlands | area_014 |

## Curation notes

We start with `Lichen_data_NT.xlsx` (1,630 quadrats) and `Lichen_data_SK.xlsx` (380 quadrats), the quadrat sheets of the two Dryad deposits of Greuel et al. (2021), and the NT deposit's site sheet `All_site_info_NT.xlsx`, from Dryad's version downloads (NT version 5 of 2026-05-18, SK version of 2021-02-18).
- Prediction point: a caribou habitat biologist revising a boreal caribou range plan wants the forage lichen of a stand in a burn nobody surveyed, from its location, ecoprovince, stand type and years since fire. A range needs 65% undisturbed habitat and every burn under 40 years counts as disturbed ([federal fact sheet](https://www.canada.ca/en/environment-climate-change/services/species-risk-public-registry/recovery-strategies/woodland-caribou-boreal-population-fact-sheet.html)), while NWT monitoring found that forage lichens need 45 to 70 years to recover ([CIMP](https://climatelibrary.ecc.gov.nt.ca/dataset/4bcc94fc-cb61-400e-858a-1bac4526ffcf)). The source names managers, not one actor: its goal is "accurately predicting the availability of lichen forage under current and future fire regimes" (Introduction), and its relationships "support the development of the first landscape level and regional level, spatial predictions of forage lichen biomass for several boreal and barren-ground caribou herds"; "Managers should consider these regional and stand-type differences when developing strategies for caribou habitat management" (Discussion). The paper was read from the publisher's PDF (Wayback Machine copy of 2021-07-16; Andrej read the HTML on 2026-11-03).
- The rows: Northwest Territories, "Lichen communities data collected in boreal forests from 2016-2018", "5, 1 m x 1 m quadrats at each plot"; Saskatchewan, "collected 2015-2016", "2, 2 m x 2 m quadrats at each plot" (the sheets' metadata). The sheets hold 326 NT and 190 SK plots, against the 346 and 221 of the Dryad abstracts. The 20 missing NT plots are in the deposit's `Quadrat_cover_data_NT.xlsx` (346 plots), so the authors left them out of the lichen sheet (already in its 2021 version); they stay out, since adding them back would need a target from our inferred formula. Anomaly: the 31 missing SK plots are explained neither in the files nor in the paper, whose analysis counts "n = 2014 samples across 567 sites" (Results, "Predicting lichen biomass accumulation"), close to the 2,010 quadrats here, so the missing plots may have had no quadrat data.
- Version: we ship the authors' 2022 revision of the NT sheet (Dryad version 4 of 2022-06-23, unchanged since). Against the 2021 file it drops five extra zero quadrats of plot CG2-5A, which had 10 rows, and adds the missing fifth quadrat of F6-7B (`F6-7B-6`, 0) and the constant `species` column; the other 1,629 quadrats are identical. The year stays 2021, the first publication.
- Target: `forage_lichen_biomass_kg_ha` is the published `kgha.volperm2`, "Biomass of live lichen species, estimated by standardize live lichen volume", the pooled forage groups (C. mitis and C. arbuscula, C. rangiferina and C. stygia, C. stellaris, C. uncialis). For NT it reproduces as 12.633 x the sum of percent cover x live depth over the four forage groups (median ratio 12.6333 over the 945 quadrats with forage cover in `Quadrat_cover_data_NT.xlsx`); SK has no cover sheet. One pooled allometry serves both regions: biomass = 0.013 x live volume (R^2 0.88 on 203 destructive samples; 12.633 is that slope in kg/ha per percent cover x cm), as "the allometric relations did not vary among ecoprovinces for the pooled Cladonia spp." (P = 0.66; Results, "Allometric equations"). SK crews measured total lichen height only; the authors took live height as 0.76 of it, "the mean ratio of live to total lichen biomass in the sorted SK samples" (Methods, "Lichen biomass allometry"), which the SK files cannot reproduce. The destructive samples (`Destructive_biomass_sample_*.xlsx`) are the allometry's calibration data, not task rows. Chosen over the cover-based `kgha.areaperm2` because the authors' presence flag `non_zero` equals volume biomass > 0 in all 2,010 quadrats, while cover biomass > 0 differs in 2 SK quadrats (plot 2015-054).
- Kept on kg/ha, not logged, for this task's own reasons (Andrej, 2026-11-03, review issue 5): the planner needs forage in kg/ha, and trained on log1p and back-transformed, every probed family falls below the training mean on RMSE in kg/ha (30 shipped splits, untuned; skill against the training mean, raw against log1p: random forest +0.097 against -0.045, small LightGBM +0.103 against -0.030, means; ridge's log1p model is worse on 27 of 30 splits).
- Dropped `kgha.areaperm2`: it is 61.934 kg/ha times the quadrat's percent cover in every row (NT on a 0.5% grid, SK on 0.1%), the same survey's measurement of the target's own cover, unknown for an unsurveyed stand (LEAK-10, a part of the target). Dropped `non_zero`, the indicator of a positive target (LEAK-10).
- Dropped the quadrat label (`quadrat`, `plot.quadrat`: positions 0, 6, 12, 18, 24 in NT, `nw` and `se` in SK), an identifier within a plot; `species`, constant (`Cladonia spp.`, NT only); `acronym` and `acronym1`, one-to-one recodings of `ecoprovince` (CLEAN-5). Kept `ecozone` and `jurisdiction` (the published `design`), coarser levels of the ecoprovince; `jurisdiction` also marks the protocol, 1 m2 quadrats in NT and 4 m2 in SK.
- Anomaly: plot F8-3A labels one quadrat `8` where every other plot has `6`; it is the plot's fifth quadrat, and the label is dropped anyway.
- Repair (2026-11-01): a plot whose task-sheet coordinate differs from the authors' site sheet by more than 0.01 degree takes the site sheet's, rounded to 0.01 degree; three NT plots, 15 rows (Decisions). CG3-31A carries CG2-35A's coordinate (62.22, -116.33), 162 km from its site-mates; the site sheet puts it at 60.77, -116.56 with them, so it also takes their ecoprovince, Hay and Slave River Lowlands for Great Bear Plains (the ecozone stays Taiga plains). F13-5A and F13-5B move 7.8 and 7.9 km, from 63.03, -114.35 to 63.00, -114.21. The other 323 NT plots equal the site sheet rounded to 0.01 degree; that grid stays, since the coordinate links rest on it.
- Every input is constant within a plot, so the quadrats of a plot share one feature vector and differ only in the target; they stay as the source's rows (SPLIT-26) and are scored one by one. A quadrat score ranks models like a stand score weighted by quadrats (Kendall tau 0.91 on the former site splits), with an NT plot weighing 5 quadrats against 2 for SK (SPLIT-23). 32.5% of the target's variance lies within identical inputs (28.8% within a plot), a floor no model can go below. Hence 532 exact duplicate rows (518 at 0: 482 quadrats of one plot and 36 of sibling plots that share every input) and the 980 rows the check counts as sharing their inputs with a row of another target (1,671 rows sit in an input group with more than one target). No feature vector occurs in two groups, so the split keeps every copy on one side (LEAK-18: few features, natural repeats).
- Zeros: 813 of 2,010 quadrats (40.4%; NT 40.7%, SK 39.5%) have a target of 0, the presence part of the authors' hurdle model ("to account both for the heterogeneous nature of lichen presence (zero-inflation)", Dryad abstract). 811 have no forage-lichen cover; 2 in plot 2015-054 have cover but volume 0 and stay 0, as the authors' presence flag has them.
- Note: `years_since_fire` (`TSSRF`, "Time since stand replacing fire") is the survey's stand age per plot, not a fire-map value. The 145 NT control plots (725 rows, 36%) lie in areas with "no recorded burn history" (Dryad NT methods) and carry ages of 33 to 241 years, so theirs were dated in the field: from four (SK) or five (NT) tree cores or disks per site, "the time since stand-replacing fire based on clusters of tree ages (<20-yr range)" and, "at sites without a clear cohort of similar-aged trees, and with no recorded fire history", "the ring count of the oldest sampled tree" (Methods, "Forest stand composition and structure"). The sites were chosen by fire-record age class (NT: 37-38 and 46-49 years after fire, and controls ">70 yr" with no recorded burn; Methods, "Site selection"); only 26 of 110 multi-plot NT sites share one age. A planner has an inventory age or "older than the fire record". Capping the age at assumed fire-record horizons (51 years in NT, 70 in SK, our assumption) costs 0.01 to 0.03 R^2 on the shipped splits (random forest 0.007, ridge 0.024, small LightGBM 0.032; SE 0.016 to 0.021). Kept: a stand age is known at the prediction point (USE-6), and the gap is named in the fit. `stand_type` is likewise the crew's class ("Stand types, Hart et al. 2019"), where a planner has the inventory's.
- Grouped by burn area. A group is an NT burn scar or unburned area, the plot-name prefix (`F1` of `F1-22A`; the codebook: "Plot location: Burn Scar or Unburned area -xxx"), merged with any area that shares an exact recorded coordinate: only CG2 and F2 join (CG2-4A and F2-22A/B lie about 0.5 km apart in the site sheet). Each SK plot is its own group, since SK names ("Year -xxx") carry no burn key. 216 groups, 26 NT and 190 SK; the largest, CG2 with F2, holds 200 rows (10.0%). Burn areas hold 18.4% of the NT target's sum of squares. The use case predicts for burns nobody surveyed (SPLIT-1, SPLIT-4); under the former site split, 94.3% of NT test quadrats had another site of their own burn area in training.
- Note: a test quadrat lies a median 22.0 km from the nearest training plot in NT (2.4 km under the former site split), against 95 km for a random point in the NT study hull; in SK, split per plot, 3.7 km (15.6 km for a point in the SK hull). SK plot means (log1p) still correlate with other plots nearby (r = 0.73 under 1 km on 16 pairs, 0.42 at 2 to 5 km, about 0.2 out to 50 km), so SK stays the laxer region; between plots of different NT areas r peaks at 0.21 (5 to 10 km) and is about 0 beyond 10 km.
- Note: ridge loses its skill under this split (-0.085 against the training mean, below it on 8 of 30 splits; +0.13 under the former site split), while the random forest keeps +0.097. Its ecoprovince effects, learned from a handful of burns (Great Bear Plains has 5 NT areas, with means from 270 to 3,453 kg/ha), do not reach a new burn: without the three region labels ridge scores +0.064. Each label is known for every stand and the source names ecoprovince as a predictor, so they stay.
- The source's model and metric: a hurdle model, a binomial GLM of presence on stand age, stand type and ecoprovince and a nonlinear mixed-effects logistic growth model of biomass given presence, chosen by AICc and ANOVA; the combined model is judged in sample by "the R2 of a linear regression between measured lichen biomass and predicted lichen biomass" (Methods, "Modeling site-level mean biomass"), "a relatively weak but significant fit (R2 = 0.18, P < 0.001)" (Results, "Combined predictions"). No held-out error is reported. That R^2 is a squared correlation, blind to a biased forecast, so it cannot rank models; the fallback `rmse` on kg/ha, the planner's unit (Andrej, 2026-11-03, review issue 6: "We can keep RMSE in this case").
- Probes (2026-11-01, untuned, the 30 shipped splits): random forest skill +0.120 against the training mean (above it on 93% of the splits), LightGBM +0.033, linear -0.075 (it swings with the fold draw); no task-probe flag, no leak-probe flag (no feature alone above the mean, no exact feature copy across the split). A random split by quadrat would give LightGBM R^2 0.440 against 0.015 by burn area.

## Splits

Grouped splits on the burn area: every plot of a burn scar or unburned area of the Northwest Territories (merged where two areas share a coordinate, only CG2 and F2) stays on one side with all its quadrats, and each Saskatchewan plot on its own, since SK plot names carry no burn key. 216 groups, 72 per test fold; test folds hold 299 to 1,028 rows, since the largest group holds 200. A test quadrat lies a median 22.0 km from the nearest training plot in NT and 3.7 km in SK, against 95 km for a random point in the NT study hull, so stands far from any survey may still be harder than the folds show, SK most. Ridge falls below the training mean on 8 of 30 splits, because ecoprovince effects learned from a handful of burns do not reach a new burn; the random forest keeps its skill.

10 repeat(s) x 3 fold(s) with seed 4267; train 982 to 1,711 rows, test 299 to 1,028 rows.

<details>
<summary>Show all 30 splits</summary>

| repeat | fold | n_train | n_test |
|---|---|---|---|
| 0 | 0 | 1407 | 603 |
| 0 | 1 | 1267 | 743 |
| 0 | 2 | 1346 | 664 |
| 1 | 0 | 1711 | 299 |
| 1 | 1 | 1003 | 1007 |
| 1 | 2 | 1306 | 704 |
| 2 | 0 | 1029 | 981 |
| 2 | 1 | 1449 | 561 |
| 2 | 2 | 1542 | 468 |
| 3 | 0 | 1351 | 659 |
| 3 | 1 | 1485 | 525 |
| 3 | 2 | 1184 | 826 |
| 4 | 0 | 1475 | 535 |
| 4 | 1 | 1322 | 688 |
| 4 | 2 | 1223 | 787 |
| 5 | 0 | 1222 | 788 |
| 5 | 1 | 1383 | 627 |
| 5 | 2 | 1415 | 595 |
| 6 | 0 | 1122 | 888 |
| 6 | 1 | 1426 | 584 |
| 6 | 2 | 1472 | 538 |
| 7 | 0 | 1465 | 545 |
| 7 | 1 | 1309 | 701 |
| 7 | 2 | 1246 | 764 |
| 8 | 0 | 1221 | 789 |
| 8 | 1 | 1445 | 565 |
| 8 | 2 | 1354 | 656 |
| 9 | 0 | 1334 | 676 |
| 9 | 1 | 982 | 1028 |
| 9 | 2 | 1704 | 306 |

</details>

## Group structure

One group is a burn scar or unburned area of the Northwest Territories (the plot-name prefix, `F1` of `F1-22A`; the codebook's "Plot location: Burn Scar or Unburned area -xxx"), merged with any area that shares an exact recorded coordinate (only CG2 and F2 join, about 0.5 km apart), with all its plots and quadrats; each Saskatchewan plot is its own group, as SK plot names carry no burn key. 216 groups: 26 NT of 10 to 200 quadrats and 190 SK of 2. The use case is a stand in a burn nobody surveyed: a range-plan biologist estimates forage across a caribou range, where most stands have no plot. Quadrats of one plot share every input, and plots of one area stand in the same burn scar or unburned area (18.4% of the NT target's sum of squares lies between areas), so all stay on one side. Stricter than the source, which fits its models to all plots. Each quadrat is one prediction.

| field | value |
|---|---|
| group column | `burn_area` |
| labels | per_sample |
| order inside a group | none |
| prediction unit | row |
| known about a group when predicting | none |

| statistic | value |
|---|---|
| groups | 216 |
| rows per group (min / median / max) | 2 / 2.0 / 200 |
| largest group | 10.0% of the rows |
| test groups per fold | 72 |
| groups of two or more rows with a single label | 26.4% |
| nearest neighbour in the same group | 100.0% of the rows (chance: 4.1%) |
| label variance explained by the group | 0.35 (shuffled groups: 0.11) |

The nearest neighbour is computed on the standardised numeric features of a sample of up to 20,000 rows; chance is the share expected if the groups were unrelated to the features. The model-based diagnostics run with `.claude/skills/knowledge-data-foundry/scripts/group_probes.py`.

## Decisions

### 1. The target is the volume-based biomass; the cover-based one is dropped

The authors' presence flag follows the volume estimate in every quadrat, and the cover estimate is a fixed multiple of the quadrat's percent cover, a part of the target.

| jurisdiction | quadrats | non_zero = (volume biomass > 0) | non_zero = (cover biomass > 0) | cover biomass / 61.934 on a 0.1% grid | Spearman volume vs cover biomass |
|---|---|---|---|---|---|
| NT | 1630 | 1630 | 1630 | 1630 | 0.994 |
| SK | 380 | 380 | 378 | 380 | 0.99 |

### 2. Three NT plots take the site sheet's coordinates

In the task sheet CG3-31A carries CG2-35A's coordinate, 162 km from its site-mates, and F13-5A and F13-5B sit about 8 km from where the authors' site sheet puts them. The other 323 NT plots equal the site sheet's coordinates rounded to 0.01 degree.

| plot | task sheet | task sheet ecoprovince | site sheet | km apart | shipped | shipped ecoprovince |
|---|---|---|---|---|---|---|
| CG3-31A | 62.22, -116.33 | Great Bear Plains | 60.76557, -116.56150 | 162.2 | 60.77, -116.56 | Hay and Slave River Lowlands |
| F13-5A | 63.03, -114.35 | Coppermine River and Tazin Lake Uplands | 63.00338, -114.20687 | 7.8 | 63.00, -114.21 | Coppermine River and Tazin Lake Uplands |
| F13-5B | 63.03, -114.35 | Coppermine River and Tazin Lake Uplands | 63.00266, -114.20566 | 7.9 | 63.00, -114.21 | Coppermine River and Tazin Lake Uplands |

## Bundle checks

0 error(s), 0 warning(s), 0 info (26 checks run, plus the dataset's own checks).


Accepted on purpose:

- `dataset_duplicate_rows`: 532 exact copies, 518 of them at 0: quadrats of one plot (482) or of sibling plots that share every input (36), since every input is a plot attribute. Each copy stays in one group, so no test row has a copy in training (LEAK-18: few features, natural repeats; Andrej, 2026-11-03).
- `dataset_conflicting_duplicate_rows`: Quadrats of one plot share their inputs and differ in lichen. 32.5% of the target's variance lies within identical inputs (28.8% within a plot), a floor no model can go below. Each input vector stays in one group (Andrej, 2026-11-03).

## Data checks

### Feature summary

| index | dtype | n_missing | pct_missing | n_unique | examples |
|---|---|---|---|---|---|
| stand_type | category | 0 | 0 | 7 | Jack pine, Well-drained spruce, Conifer mix, Poorly-drained spruce, Deciduous-c… |
| jurisdiction | category | 0 | 0 | 2 | NT, SK |
| ecozone | category | 0 | 0 | 3 | Taiga plains, Taiga shield, Boreal shield |
| ecoprovince | category | 0 | 0 | 4 | Hay and Slave River Lowlands, Coppermine River and Tazin Lake Uplands, Athabasc… |
| burn_area | category | 0 | 0 | 216 | area_011, area_012, area_013, area_010, area_023, area_022, area_014, area_021,… |
| forage_lichen_biomass_kg_ha | float64 | 0 | 0 | 847 | 0.0, 9.475, 6.3167, 12.6333, 18.95, 11.5805, 8.4222, 25.2666, 15.7916, 13.6861 |
| latitude | float64 | 0 | 0 | 274 | 60.7, 61.06, 62.65, 62.51, 61.13, 62.66, 60.72, 60.71, 61.14, 60.73 |
| longitude | float64 | 0 | 0 | 321 | -115.83, -115.9, -116.17, -116.58, -116.18, -116.32, -116.25, -116.15, -113.78,… |
| years_since_fire | int64 | 0 | 0 | 137 | 40, 39, 42, 34, 35, 33, 43, 71, 41, 32 |

### Target distribution

| index | y_missing_count | non_positive_pct | skew_y | skew_log | var_y | var_log | log_used | aic_exponential | aic_lognormal | dist_hint |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 40.45 | 4.005 | 0.266 | 1.44724e+06 | 9.243 | log1p | 18618.3 | 17802.6 | lognormal |

### Numeric features

| index | count | mean | std | min | max |
|---|---|---|---|---|---|
| forage_lichen_biomass_kg_ha | 2010 | 522.126 | 1203.01 | 0 | 13126 |
| years_since_fire | 2010 | 72.8741 | 41.8146 | 1 | 241 |
| latitude | 2010 | 61.1059 | 2.25854 | 55.4786 | 65.9 |
| longitude | 2010 | -114.266 | 5.42363 | -128.24 | -102.009 |

### Categorical features

<details>
<summary>Show the table (19 rows)</summary>

| column | rank | value | count | pct |
|---|---|---|---|---|
| burn_area | 1 | area_011 | 200 | 9.95 |
| burn_area | 2 | area_012 | 150 | 7.46 |
| burn_area | 3 | area_013 | 135 | 6.72 |
| burn_area | 4 | area_010 | 120 | 5.97 |
| burn_area | 5 | area_023 | 110 | 5.47 |
| ecoprovince | 1 | Hay and Slave River Lowlands | 730 | 36.32 |
| ecoprovince | 2 | Coppermine River and Tazin Lake Uplands | 620 | 30.85 |
| ecoprovince | 3 | Athabasca Plain and Churchill River Uplands | 380 | 18.91 |
| ecoprovince | 4 | Great Bear Plains | 280 | 13.93 |
| ecozone | 1 | Taiga plains | 1010 | 50.25 |
| ecozone | 2 | Taiga shield | 620 | 30.85 |
| ecozone | 3 | Boreal shield | 380 | 18.91 |
| jurisdiction | 1 | NT | 1630 | 81.09 |
| jurisdiction | 2 | SK | 380 | 18.91 |
| stand_type | 1 | Jack pine | 640 | 31.84 |
| stand_type | 2 | Well-drained spruce | 581 | 28.91 |
| stand_type | 3 | Conifer mix | 295 | 14.68 |
| stand_type | 4 | Poorly-drained spruce | 243 | 12.09 |
| stand_type | 5 | Deciduous-conifer mix | 121 | 6.02 |

</details>

## Build

Not built yet. `dataset build` saves the container to the warehouse and records its UUID, checksum and provenance here.
