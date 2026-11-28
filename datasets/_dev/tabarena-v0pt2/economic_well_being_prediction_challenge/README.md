---
report_format: data-foundry-report-v2
unique_name: economic_well_being_prediction_challenge
container_format: 2
checksum: v2:8be24a0eb9315391e3cc96c101247760752a90b8d880aeb5aea1c533b40f7e81
build:
  uuid: 01a1ae48-ee3d-73ae-bf99-a2b037658716
  checksum: v2:67814a2cb764b9b4774b509d02aeb05b24c17f34e225e371229d3163fcf821f3
  built_at: '2026-11-06T00:36:18+00:00'
  path: economic_well_being_prediction_challenge/01a1ae48-ee3d-73ae-bf99-a2b037658716
  data_foundry_version: 0.0.5
  git_sha: b4ac95ff0f853de54117555ae24bd013c3630fd4
  libraries:
    python: 3.12.3
    pandas: 3.1.0
    numpy: 2.5.4
    pyarrow: 26.0.0
    scikit-learn: 1.7.2
    polars: 2.0.0
build_stale: true
data:
  n_rows: 28618
  n_features: 16
  dtypes:
    category: 2
    float64: 15
    int64: 1
  n_test_dataset_rows: null
task:
  target: Target
  problem_type: regression
  metric: rmse
  metric_origin: source
  scoring_columns: null
  split_regime: grouped_non_iid
  stratify_on: null
  time_on: null
  group_on: country
  group_labels: per_sample
  group_time_on: null
  grouping:
    prediction_unit: row
    aggregation: null
    context: none
    n_groups: 25
    test_groups_per_fold:
      min: 2
      max: 3
splits:
  n_repeats: 1
  n_folds: 9
  random_state: 4267
  time_horizon: null
  time_horizon_unit: null
  time_gap: null
  time_gap_unit: null
  n_train:
    min: 24505
    max: 26709
  n_test:
    min: 1909
    max: 4113
bundle_checks:
  ok: true
  errors: []
  warnings: []
  infos:
  - dataset_conflicting_duplicate_rows
  accepted:
    groups_test_groups_few: 'Accepted (Andrej, 2026-11-25): a test country stands
      for a country without surveys of its own, so two or three whole countries per
      fold is the task (9 folds, each of the 25 countries tested once). The signal
      carries over to unseen countries: over 20 draws of the 9 folds LightGBM scores
      RMSE 0.1138 against 0.1230 for night lights alone, and leave one country out
      over all 25 gives 0.1123 against 0.1218 (2026-11-25).'
    splits_dimensions_off_protocol: 'Accepted (Andrej, 2026-11-25): 1 x 9 country
      folds instead of the protocol''s 3 x 3. Over 20 draws each, 1 x 9 lands closer
      to leave one country out over all 25 (bias +0.0010 to +0.0024 RMSE against +0.0020
      to +0.0044 for 3 x 3, which trains on a third fewer countries) and keeps its
      model ranking in 90% of draws against 85%; the splits comment says why.'
decisions:
- Test.csv's 7 countries added with labels recovered from the source table
- Rows per country and file, and the fold that tests each country
---

# economic_well_being_prediction_challenge

> Generated from [`dataset.py`](dataset.py) by `dataset check` (or `build`). Do not edit this page: change `dataset.py` and re-run the check.

Regression of `Target`, scored with `rmse` on grouped splits by `country`. 28,618 rows and 16 features. Source: Zindi (2021).

Built as `01a1ae48-ee3d-73ae-bf99-a2b037658716` on 2026-11-06, but `dataset.py` has changed since: it now gives checksum `v2:8be24a0eb9315391e3cc96c101247760752a90b8d880aeb5aea1c533b40f7e81`, so the build is stale. See [Build](#build).

## In brief

**Question.** What is a survey cluster's wealth index in a country without surveys of its own?

**Use case.** An agency maps local wealth today for the past survey years of a country without surveys of its own, filling the gaps between the more expensive surveys to inform geographic targeting of support. It holds every map layer as read today. A model trained on the surveys of other countries is evaluated on every survey of a held-out country.

**One row.** One survey cluster: 28,618 rows, 25 countries, 1994–2016; 21,454 from the released training file and 7,164 from the source's test file, whose labels are recovered from the source's cluster table.

**Predicted.** The source's cluster-average, asset-related wealth index, from zero to one with higher values indicating greater wealth. It describes the survey year, not future income.

**Known at prediction time.** The survey year, urban/rural context, built-up area by epoch through 2014, land cover, water, population density, nighttime lights and distances, each as read today: one read of each layer serves every row, whatever its survey year, as the source released them. The prediction point is today, so later reads are known.

**What the test data stands for.** Whole countries held out with all their survey years, in 9 folds of 2 or 3 countries: each of the 25 countries is tested once and the other 22 or 23 train; the source's own 7 test countries are among them.

**Our changes to the source.** We add the source's 7 test countries, with labels recovered from the source's cluster table, and keep the training file's rows and labels as released; 30 test rows whose cluster cannot be told apart from a neighbour's are left out. We hold out whole countries and drop the row ID. We keep the source's feature values, the later reads of the layers included.

> **Use case fit: approximate (a stand-in with a known gap).** The source documents neither its label (a pooled asset index, rescaled) nor several layer epochs; recovered test-file labels differ from the hidden ones by up to about 0.0013, the source's per-row deviation. Every layer is the read the agency holds today (Andrej, 2026-11-24). The test stands for a country never surveyed, not for the gap between two surveys of one country.

## Files in this folder

| file | what it is |
|---|---|
| [`dataset.py`](dataset.py) | The definition, and the only file edited by hand: metadata, reading and cleaning the raw files, feature types and splits. |
| [`README.md`](README.md) | This page, generated by `dataset check` and `dataset build`. |

- The curation record, with the triage decision, its sources and the review: [`curation/records/economic_well_being_prediction_challenge.md`](../../../../curation/records/economic_well_being_prediction_challenge.md)
- The original source: <https://zindi.world/competitions/aims-data-science-hackathon>
- The collection this folder belongs to: [`tabarena-v0pt2/README.md`](../README.md) and [`tabarena-v0pt2/CHANGELOG.md`](../CHANGELOG.md)

## Rebuild

`dataset.py` reads its raw files from `local-data-warehouse/economic_well_being_prediction_challenge/`. To get them:

```text
Obtain Train.csv and Test.csv from the Economic Well-Being Prediction Challenge data page:
https://zindi.world/competitions/economic-well-being-prediction-challenge/data
(login or acceptance of the source terms may be needed; an independent publisher checksum is unavailable).
Train.csv is 5,829,604 bytes, SHA-256 caf159ff5c84630ca3ec61793ab362073cfed396e348ecca12f60f4d13efa93c; public
copies on GitHub have the same SHA-256 (checked 2026-11-21). Test.csv is 1,805,196 bytes, SHA-256
e1d61ea14428f23643547b5a322ffc9015e4df0fc9bb798ec675cf2475c149ab, equal to the public copy at
https://raw.githubusercontent.com/simiel/economic-well-being-prediction-competition/226eb21c40bb46b7d24319c0ee0a5b896e01ee4a/Test.csv
Then the source's cluster table (Yeh et al. 2020, MIT) and the Natural Earth coastline, both at pinned commits:

d=local-data-warehouse/economic_well_being_prediction_challenge && mkdir -p $d
curl -sSfL -o $d/dhs_wealth_index.csv https://raw.githubusercontent.com/sustainlab-group/africa_poverty/cb769c744872e52c35f9c60e94b0dc2a696d389a/data/dhs_wealth_index.csv
curl -sSfL -o $d/ne_50m_coastline.geojson https://raw.githubusercontent.com/nvkelso/natural-earth-vector/a726d63745ff99cf26a03ae1c7cfb0d4f12fa517/geojson/ne_50m_coastline.geojson

dhs_wealth_index.csv is 5,073,675 bytes, SHA-256 e68c0466599a6fa3cfc6bcfaa9e5626276ed1e50f184deed7ed4f89c2e0efba8;
ne_50m_coastline.geojson is 1,640,858 bytes, SHA-256
271f1c4c1908312bac6b29d158ea1356544beafc129f260005300913aa5ea283. `_prepare_raw_files` checks all four hashes and
writes Test_labelled.csv and join_check.csv next to them (no coordinates, no survey or cluster ids); the build
reads only local files. The original AIMS task and the public rerun describe the same task; no byte-for-byte
comparison against the original AIMS download has been made.
```

On first use, `_prepare_raw_files` writes `Test_labelled.csv`, `join_check.csv` into the same folder.

Then, from the repository root:

```bash
.venv/bin/python -m data_foundry.curation.cli dataset check datasets/_dev/tabarena-v0pt2/economic_well_being_prediction_challenge   # pipeline and checks, no UUID; rewrites this page
.venv/bin/python -m data_foundry.curation.cli dataset build datasets/_dev/tabarena-v0pt2/economic_well_being_prediction_challenge   # also saves the container and records its UUID
```

Only curators run `build`, when the dataset ships.

## Dataset and task

| field | value |
|---|---|
| source | Zindi: https://zindi.world/competitions/aims-data-science-hackathon |
| year | 2021 |
| domain | social science |
| license | CC BY-SA 4.0 (competition rules); the labels are cluster-level wealth indices from DHS surveys, whose terms of use bar commercial use; used for non-commercial academic research only. |
| data_tags | Non-IID, Grouped, Spatial, UnseenGroup |
| reference | Zindi2021EconomicWellBeing |
| rows x columns | 28,618 x 18 |
| task.target | Target |
| task.problem_type | regression |
| task.metric | rmse |
| task.split_regime | grouped_non_iid |
| task.group_on | country |
| task.group_labels | per_sample |

**Metric**

| field | value |
|---|---|
| name | `rmse` (standard; takes value; lower is better) |
| origin | source: the source's metric |
| original | Root Mean Squared Error |
| reference | https://zindi.world/competitions/economic-well-being-prediction-challenge |
| definition | sqrt(mean((y - p)^2)) |

<details>
<summary>Feature types: 2 categorical, 0 string, 0 datetime</summary>

- categorical (2): `country`, `urban_or_rural`
- string (0): none
- datetime (0): none

</details>

<details>
<summary>BibTeX</summary>

```bibtex
@misc{Zindi2021EconomicWellBeing,
  author = {{Zindi} and {AIMS} and {Microsoft}},
  title = {AIMS Data Science Hackathon and Economic Well-Being Prediction Challenge},
  year = {2021},
  howpublished = {\url{https://zindi.world/competitions/aims-data-science-hackathon}},
  note = {Public Economic Well-Being challenge rerun on Zindi}
}
```

</details>

## Sample rows

The first 5 of 28,618 rows of the final frame (random rows: the frame is shuffled); 12 of 18 columns, the target first. Cells are cut at 40 characters.

| Target | country | year | urban_or_rural | ghsl_water_surface | ghsl_built_pre_1975 | ghsl_built_1975_to_1990 | ghsl_built_1990_to_2000 | ghsl_built_2000_to_2014 | ghsl_not_built_up | ghsl_pop_density | landcover_crops_fraction |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.616366 | Nigeria | 2008 | Urban | 0.000341631 | 0.293853 | 0.144908 | 0.0397309 | 0.136431 | 0.384735 | 435.914 | 4.18952 |
| 0.225305 | Lesotho | 2014 | Rural | 0 | 0 | 0 | 0 | 4.2865e-05 | 0.999957 | 0.206114 | 18.3624 |
| 0.289198 | Cameroon | 2004 | Rural | 0 | 0.00167953 | 0.00546071 | 0.00113835 | 0 | 0.991721 | 8.43047 | 2.12163 |
| 0.358282 | Tanzania | 2004 | Rural | 0 | 0 | 0 | 0 | 0 | 1 | 1.1919 | 40.0469 |
| 0.181243 | Sierra Leone | 2013 | Rural | 0.000406174 | 0.0032171 | 0.00121157 | 0.00252168 | 0.00736384 | 0.98528 | 2.83238 | 6.56059 |

## Curation notes

We start with the curator-provided Train.csv and Test.csv from Zindi's Economic Well-Being Prediction Challenge, and recover the labels of Test.csv, which Zindi never released, from the source's cluster table.

- Test.csv joined (Andrej, 2026-11-24, review issue 9, option b): the competition's rows are the clusters with coordinates of the africa_poverty cluster table of Yeh et al. 2020 (`data/dhs_wealth_index.csv` of github.com/sustainlab-group/africa_poverty at commit cb769c74, MIT); Train.csv and Test.csv together hold 28,648 of its 28,649 clusters with coordinates, in 25 countries (cluster counts equal in 95 of 96 country-years; Nigeria 2008 rural has one source cluster more). `_prepare_raw_files` assigns each Zindi row one-to-one to a cluster within country x year x urban: the distance to the capital is recomputed at the table's coordinates on the WGS84 ellipsoid from a capital point fitted per country to Zindi's released distances (every pair agrees within 0.002 km), and the distance to Natural Earth's 50 m coastline (pinned commit), which differs from Zindi's shoreline by a median 2.4 km, only breaks near-ties. The coordinates, survey ids and cluster ids stay in the raw folder and are never shipped.
- Recovered labels: Target = 0.245034 x wealthpooled + 0.343664, refit on Train.csv (21,336 rows within 0.01 of the first fit). On Train.csv the join finds the right cluster (recovered label within 0.0014 of Target) for 21,321 of 21,454 rows (99.38%); Zindi's Target is the rescaled index plus a per-row deviation spread over about +-0.0013 (sd 0.0007 and mean 0 in every country-year), so the recovered Test.csv labels differ from Zindi's hidden values by up to about 0.0013. The 133 Train.csv misses are 131 Central African Republic 1994-95 rows at shared locality points, which no distance separates, and one Cameroon 2004 pair 0.0012 km apart in distance to the capital.
- The bar, matched to the data (Andrej, 2026-11-24): a match is accepted only where it is unambiguous, the distance to the capital within 0.002 km, no other cluster of the cell within 0.002 km of it as well, and no other cluster of the cell at the same coordinate. On Train.csv the accepted matches are 21,146 rows, and all 21,146 give the right cluster; the build stops if this share falls below 99.9%. Train.csv rows keep their released Target whatever the match. Of Test.csv's 7,194 rows, 7,164 are accepted and added (none at a shared coordinate; 30 rows of Angola, Benin, Burkina Faso, Uganda and Zimbabwe have a second cluster within 0.002 km and are left out). No source indicator column ships: the framework has no non-input column besides the target, the group and the metric's scoring columns, and a row's file follows from its country.
- Prediction point: today. The agency maps the past survey years of a country without surveys of its own (the source's aim, "filling in the gaps between the more expensive surveys"), with a model fitted to the surveys of other countries, and holds every layer as read today. So every input is used as the source released it, one read of each layer on rows of every survey year, as the source itself did (its 2015-2019 land cover on rows from 1998). This replaces, for this use case, Myunghwan's rule of 2026-10-31 against fields that describe a later state than the survey (Andrej, 2026-11-24, review issue 4). Calendar-year timing stays the accepted approximation (Myunghwan, 2026-11-02).
- Target: Myunghwan accepted prediction of the supplied source index with approximate fit when approving ship (2026-11-02). Retain all 21,454 supplied labels of Train.csv unchanged. They are a cluster-average wealth index on 0–1, not currency or a poverty probability: the source table's `wealthpooled` (an asset index from one principal component pooled over all surveys, averaged per cluster), min-max rescaled over the 25 countries, plus Zindi's per-row deviation of about +-0.0013 (review issue 9).
- Potential leak, kept on purpose: the index was rescaled with one min-max over the whole release, rows of later years included (exactly one 0, Ethiopia 2005, and one 1, Nigeria 2013, both Train.csv rows; in those two countries' splits one test label sets an end of the scale). An affine rescale passes no row-level information; revisit if the source documents a per-survey normalisation.
- Keep the four landcover_* columns (crops, urban, permanent and seasonal water within 10 km): the source links a 2015-2019 Copernicus product without saying which epoch was sampled, so for rows before 2015 they are a later read, which the agency mapping today holds. Built-up by epoch (GHSL, through 2014) is kept unmasked on every row for the same reason: it is today's layer, also where an epoch ends after the survey year.
- Water, population density and nighttime lights are each one read used on every row; their represented epochs are not documented. Water describes stable water bodies, and at the same place it does not change between surveys. Potential leak, kept on purpose: ghsl_pop_density is most likely GHS-POP's 2015 epoch (it responds to 2000-2014 construction like the 2015-2019 land cover, log coefficient 0.46 against 0.32) and is used on the 24,196 rows before 2015; kept because the agency maps today with today's layers (review issue 4). Potential leak, kept on purpose: nighttime_lights is one read of an undated layer (values up to 383, so VIIRS from 2012 or a radiance-calibrated DMSP composite) used on rows from 1994 on; kept because the agency maps today with today's read (review issue 5). At the same place it does not change over 13 or more years (log change -0.016) while the target rises by +0.158, so it carries no later state of the label; revisit if the source names the product.
- Same-place check (2026-11-21, on Train.csv): 1,204 pairs of clusters of one country at the same place (both distances within 0.3 km, pre-1975 built-up within 0.005), surveyed up to 22 years apart. Water, population and lights do not change between them (population and lights: mean log change within ±0.035 in every band of years), while the target rises by +0.158 at 13 or more years. The country-year means of these inputs differ in all 52 consecutive comparisons only because each survey samples different clusters; the fixed 2000-2014 layer differs in all 52 for the same reason.
- dist_to_capital and dist_to_shoreline are distances in km to the official capital and to the shoreline: coastal clusters lie about 210 km from it in Côte d'Ivoire, 480 km in Nigeria and 350 km in Tanzania (Yamoussoukro, Abuja and Dodoma, not Abidjan, Lagos or Dar es Salaam), and within a few km in Senegal and Sierra Leone.
- Decode the source’s R/U urban_or_rural codes to Rural/Urban categorical labels (CLEAN-12, current main). Meanings are unchanged; unknown codes raise. Keep it as a category: the source starter notebook explicitly uses it. Generic metadata boilerplate does not identify this field as prohibited. Country is the group, not an input; ID is dropped; year remains a numeric input. No country/year frequency encodings or full-data statistics are added.
- Keep all rows and numeric scales. Original labels are unique, and repeated predictor profiles are not established collection errors. 129 rows share all inputs with a row of another target value: they are Central African Republic clusters of 1994-95, whose positions are locality points (41 exact location groups, 205 rows, some holding a Rural and an Urban row at one point); Test.csv has no clusters at a shared coordinate. Country groups keep them on one side. Zero numeric measurements remain zero; the source documents no alternative missing-code convention (population density is 0 on 2,262 rows, 2,250 of them with no built-up in any GHSL epoch).
- Licence: the competition grants CC BY-SA 4.0. The labels are cluster means of DHS and Malaria Indicator Surveys (the competition does not name DHS; the africa_poverty cluster table of Yeh et al. 2020 holds the same index), and the DHS terms of use (https://dhsprogram.com/data/terms-of-use.cfm) bar any marketing or commercial venture and the redistribution of DHS micro-level data; the shipped rows are cluster-level indices, not micro-level data, and carry no coordinates, survey ids or cluster ids (the join of review issue 9 reads coordinates only in the raw folder). The benchmark uses the data for non-commercial academic research only (Andrej, 2026-11-24, review issue 10).
- Scope: the inputs are mapped quantities aggregated to 5 km (built-up fractions, modelled population, calibrated lights, water, land-cover fractions) plus GIS distances, read as measurements of a place, as for covertype, the GeoAI NO2 challenge and AirQo; no raw reflectance is used to recognise image content (the reason crop-type datasets were rejected).
- Metric: RMSE, the source's metric, scores the wealth level. With one country per split, one offset for the whole country was 0.1-53% of a split's squared error for a random forest (Lesotho lowest, Malawi highest; mean 17%, measured 2026-11-24 on the earlier one-country splits of 16 countries), while geographic targeting acts on the ranking of places within a country, which RMSE scores only in part.
- Temporal limitation: survey year orders label content. Target harmonization using future actual states cannot be ruled out. Label publication dates are absent, a limitation on literal historical deployment claims rather than an extra acceptance gate for this task, whose prediction point is today.
- Split walk (the split decision tree, SPLIT-36, from the record's collection type Survey): [SUR.meets] the model estimates wealth for a country without surveys of its own, a place outside what the training surveys covered → Place step → [PLACE.several] the data holds 25 countries: yes → leaf L-PLACE.groups, Grouped · `UnseenGroup`, whole countries held out with all their survey years. The definition ships this leaf's split (Andrej, 2026-11-24), in 9 folds of 2 or 3 countries, each of the 25 countries tested once (the source's own 7 test countries among them), as the source tests unseen countries over all years (Andrej, 2026-11-25).
- Time basis: UnseenGroup: survey clusters of 25 countries, 1994-2016; a test country stands for a country without surveys of its own, mapped for the years the other countries' surveys cover, which are all in training. Not tested: a later year.

## Splits

Whole countries in 9 folds, one repeat (Andrej, 2026-11-25): each of the 25 countries is held out once with
all its survey years, two or three countries per fold (seven folds of 3, two of 2), assigned by the framework's
grouped k-fold with shuffled countries and its fixed seed; each split trains on the other 22 or 23 countries.
This replaces leave one country out over the 16 countries surveyed in 2014-2016 (2026-11-24), which never
tested 9 countries, Benin, one of the source's own test countries, among them; under a prediction point of
today an older survey is as valid a test as a newer one. Folds of several countries were chosen over one
country per split for larger test sides (about 3,200 rows per fold against 1,150), and one repeat over 3 x 3
because the repeats of repeated folds share most of their training countries. Measured (2026-11-25, 20 draws
of the country folds per design, four models, mean RMSE over splits; reference: leave one country out over all
25): 1 x 9 is off the reference by +0.0010 to +0.0024 and ranks the models as the reference does in 90% of
draws; 3 x 3, which trains on 16-17 countries, is off by +0.0020 to +0.0044, in 85%, and halves the gap
between LightGBM and a random forest (-0.0021 against -0.0039 on the reference; 1 x 9: -0.0034). Its scores
vary less between draws (SD 0.0008-0.0013 against 0.0010-0.0017), less than its bias. All 7 of the source's own test
countries (Test.csv, 1998-2016) are tested, with their recovered labels. The split decision tree reaches
L-PLACE.groups for this survey (Survey: a country without surveys of its own lies outside what the training
surveys covered; the place step: several countries). A test country's clusters of every year are on the test
side; no later year is tested.

1 repeat(s) x 9 fold(s) with seed 4267; train 24,505 to 26,709 rows, test 1,909 to 4,113 rows.

| repeat | fold | n_train | n_test |
|---|---|---|---|
| 0 | 0 | 25555 | 3063 |
| 0 | 1 | 26709 | 1909 |
| 0 | 2 | 25990 | 2628 |
| 0 | 3 | 24505 | 4113 |
| 0 | 4 | 24581 | 4037 |
| 0 | 5 | 24982 | 3636 |
| 0 | 6 | 24731 | 3887 |
| 0 | 7 | 26204 | 2414 |
| 0 | 8 | 25687 | 2931 |

## Group structure

One group is a country, held out with all its survey years: a test country stands for a country without surveys of its own, as in the source's test of 7 countries over 1998-2016, which the dataset holds too. Every country is tested once, in 9 folds of 2 or 3 countries.

| field | value |
|---|---|
| group column | `country` |
| labels | per_sample |
| order inside a group | none |
| prediction unit | row |
| known about a group when predicting | none |

| statistic | value |
|---|---|
| groups | 25 |
| rows per group (min / median / max) | 231 / 984.0 / 2,695 |
| largest group | 9.4% of the rows |
| test groups per fold | 2 to 3 |
| groups of two or more rows with a single label | 0.0% |
| nearest neighbour in the same group | 84.6% of the rows (chance: 5.4%) |
| label variance explained by the group | 0.15 (shuffled groups: 0.00) |

The nearest neighbour is computed on the standardised numeric features of a sample of up to 20,000 rows; chance is the share expected if the groups were unrelated to the features. The model-based diagnostics run with `.claude/skills/knowledge-data-foundry/scripts/group_probes.py`.

## Decisions

### 1. Test.csv's 7 countries added with labels recovered from the source table

Zindi's Train.csv and Test.csv are the coordinate-bearing clusters of the africa_poverty table; each Zindi row is assigned to its cluster within country x year x urban by the recomputed distance to the capital, the shoreline breaking near-ties, and kept only where the match is unambiguous. On Train.csv the accepted matches give the released Target up to Zindi's per-row deviation (right_cluster: within 0.0014); Test.csv rows get the refit rescale of wealthpooled.

| part | status | rows | right_cluster |
|---|---|---|---|
| test | accepted | 7164 | nan |
| test | near-tie in the distance to the capital | 30 | nan |
| train | accepted | 21146 | 21146 |
| train | near-tie in the distance to the capital | 135 | 133 |
| train | shared coordinate | 173 | 42 |

### 2. Rows per country and file, and the fold that tests each country

Whole countries in 9 folds of 2 or 3, one repeat: every country is tested once, all its years.

| country | Test.csv | Train.csv | test_fold |
|---|---|---|---|
| Angola | 846 | 0 | 2 |
| Benin | 740 | 0 | 5 |
| Burkina Faso | 995 | 0 | 7 |
| Cameroon | 0 | 1041 | 0 |
| Central African Republic | 0 | 231 | 3 |
| Cote d'Ivoire | 0 | 481 | 8 |
| Democratic Republic of Congo | 785 | 0 | 4 |
| Ethiopia | 0 | 1721 | 6 |
| Ghana | 0 | 1419 | 7 |
| Guinea | 0 | 593 | 6 |
| Kenya | 0 | 2626 | 5 |
| Lesotho | 0 | 794 | 1 |
| Malawi | 0 | 1957 | 4 |
| Mali | 0 | 1295 | 4 |
| Mozambique | 0 | 879 | 2 |
| Nigeria | 0 | 2695 | 3 |
| Rwanda | 0 | 984 | 0 |
| Senegal | 0 | 903 | 2 |
| Sierra Leone | 0 | 785 | 1 |
| Swaziland | 0 | 270 | 5 |
| Tanzania | 0 | 2450 | 8 |
| Togo | 0 | 330 | 1 |
| Uganda | 1573 | 0 | 6 |
| Zambia | 1038 | 0 | 0 |
| Zimbabwe | 1187 | 0 | 3 |

## Bundle checks

0 error(s), 0 warning(s), 1 info (28 checks run, plus the dataset's own checks).

- **info** `dataset_conflicting_duplicate_rows`: 129 row(s) (0.5%) share all features with another row but carry a different target. (hint: Either the rows differ in a dropped column, or the label is noisy — this caps the achievable score.)

Accepted on purpose:

- `groups_test_groups_few`: Accepted (Andrej, 2026-11-25): a test country stands for a country without surveys of its own, so two or three whole countries per fold is the task (9 folds, each of the 25 countries tested once). The signal carries over to unseen countries: over 20 draws of the 9 folds LightGBM scores RMSE 0.1138 against 0.1230 for night lights alone, and leave one country out over all 25 gives 0.1123 against 0.1218 (2026-11-25).
- `splits_dimensions_off_protocol`: Accepted (Andrej, 2026-11-25): 1 x 9 country folds instead of the protocol's 3 x 3. Over 20 draws each, 1 x 9 lands closer to leave one country out over all 25 (bias +0.0010 to +0.0024 RMSE against +0.0020 to +0.0044 for 3 x 3, which trains on a third fewer countries) and keeps its model ranking in 90% of draws against 85%; the splits comment says why.

## Data checks

### Feature summary

<details>
<summary>Show the table (18 rows)</summary>

| index | dtype | n_missing | pct_missing | n_unique | examples |
|---|---|---|---|---|---|
| country | category | 0 | 0 | 25 | Nigeria, Kenya, Tanzania, Malawi, Ethiopia, Uganda, Ghana, Mali, Zimbabwe, Came… |
| urban_or_rural | category | 0 | 0 | 2 | Rural, Urban |
| ghsl_water_surface | float64 | 0 | 0 | 6102 | 0.0, 0.0906, 0.0985, 0.0109, 0.134, 0.02, 0.0371, 0.0005, 0.0505, 0.0158 |
| ghsl_built_pre_1975 | float64 | 0 | 0 | 17405 | 0.0, 0.3018, 0.0209, 0.0237, 0.0164, 0.0407, 0.0507, 0.0738, 0.0001, 0.0429 |
| ghsl_built_1975_to_1990 | float64 | 0 | 0 | 20601 | 0.0, 0.0009, 0.002, 0.0122, 0.0003, 0.0707, 0.0117, 0.0007, 0.004, 0.0088 |
| ghsl_built_1990_to_2000 | float64 | 0 | 0 | 22631 | 0.0, 0.0726, 0.0013, 0.0021, 0.0003, 0.0249, 0.0136, 0.0059, 0.0059, 0.0419 |
| ghsl_built_2000_to_2014 | float64 | 0 | 0 | 24004 | 0.0, 0.0129, 0.0009, 0.0048, 0.0125, 0.0694, 0.0006, 0.0035, 0.008, 0.001 |
| ghsl_not_built_up | float64 | 0 | 0 | 25248 | 1.0, 0.522, 0.976, 0.9674, 0.9743, 0.8433, 0.9988, 0.9255, 0.8371, 0.7907 |
| ghsl_pop_density | float64 | 0 | 0 | 26173 | 0.0, 358.9101, 44.3966, 38.398, 40.5331, 35.611, 60.9827, 20.4011, 12.4686, 29.… |
| landcover_crops_fraction | float64 | 0 | 0 | 28416 | 1.9923, 0.0, 8.1643, 15.6315, 14.6089, 12.0862, 9.6488, 17.9384, 11.7873, 15.77… |
| landcover_urban_fraction | float64 | 0 | 0 | 27887 | 0.0, 44.4383, 9.4504, 7.7564, 14.7865, 14.3596, 3.7043, 8.2476, 4.3022, 3.7017 |
| landcover_water_permanent_10km_fraction | float64 | 0 | 0 | 15179 | 0.0, 4.8691, 0.0817, 0.377, 0.2425, 5.266, 0.7517, 0.9136, 7.2495, 0.2932 |
| landcover_water_seasonal_10km_fraction | float64 | 0 | 0 | 23636 | 0.0, 1.7199, 0.4529, 0.6447, 0.0032, 0.4626, 0.0005, 0.0006, 0.0466, 1.8641 |
| nighttime_lights | float64 | 0 | 0 | 14466 | 0.0, 12.6971, 0.6865, 1.5813, 2.1482, 1.311, 1.2285, 1.5654, 0.9671, 0.2251 |
| dist_to_capital | float64 | 0 | 0 | 28454 | 4.4694, 278.6301, 261.5968, 307.522, 430.6334, 303.8057, 83.0055, 369.8154, 304… |
| dist_to_shoreline | float64 | 0 | 0 | 28454 | 969.5297, 1223.3273, 895.4535, 660.5836, 729.6785, 685.1395, 899.9594, 682.5467… |
| Target | float64 | 0 | 0 | 28617 | 0.7193, 0.3084, 0.523, 0.6257, 0.0337, 0.2189, 0.153, 0.1329, 0.1403, 0.5682 |
| year | int64 | 0 | 0 | 19 | 2014, 2011, 2015, 2010, 2013, 2012, 2008, 2016, 2009, 2006 |

</details>

### Target distribution

| index | y_missing_count | non_positive_pct | skew_y | skew_log | var_y | var_log | log_used | aic_exponential | aic_lognormal | dist_hint |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0.73 | 0.523 | 0.039 | 0.02 | log1p | -3601.7 | -11352.8 | lognormal |

### Numeric features

<details>
<summary>Show the table (16 rows)</summary>

| index | count | mean | std | min | max |
|---|---|---|---|---|---|
| year | 28618 | 2010.27 | 4.55507 | 1994 | 2016 |
| ghsl_water_surface | 28618 | 0.0269854 | 0.0951832 | 0 | 0.9911 |
| ghsl_built_pre_1975 | 28618 | 0.0407348 | 0.118094 | 0 | 0.894608 |
| ghsl_built_1975_to_1990 | 28618 | 0.0277642 | 0.0728322 | 0 | 0.68501 |
| ghsl_built_1990_to_2000 | 28618 | 0.0136771 | 0.0341543 | 0 | 0.515534 |
| ghsl_built_2000_to_2014 | 28618 | 0.0183299 | 0.0402042 | 0 | 0.649159 |
| ghsl_not_built_up | 28618 | 0.872509 | 0.242156 | 0.00085934 | 1 |
| ghsl_pop_density | 28618 | 94.7125 | 209.457 | 0 | 1902.88 |
| landcover_crops_fraction | 28618 | 21.1072 | 16.3107 | 0 | 80.0649 |
| landcover_urban_fraction | 28618 | 14.0339 | 23.8639 | 0 | 98.7841 |
| landcover_water_permanent_10km_fraction | 28618 | 1.66287 | 7.13876 | 0 | 99.164 |
| landcover_water_seasonal_10km_fraction | 28618 | 0.694467 | 2.38471 | 0 | 56.2016 |
| nighttime_lights | 28618 | 9.18167 | 25.736 | 0 | 403.456 |
| dist_to_capital | 28618 | 300.707 | 269.087 | 0.105306 | 1908.11 |
| dist_to_shoreline | 28618 | 473.749 | 355.804 | 0.11208 | 1769.52 |
| Target | 28618 | 0.345418 | 0.198482 | 0 | 1 |

</details>

### Categorical features

| column | rank | value | count | pct |
|---|---|---|---|---|
| country | 1 | Nigeria | 2695 | 9.42 |
| country | 2 | Kenya | 2626 | 9.18 |
| country | 3 | Tanzania | 2450 | 8.56 |
| country | 4 | Malawi | 1957 | 6.84 |
| country | 5 | Ethiopia | 1721 | 6.01 |
| urban_or_rural | 1 | Rural | 18669 | 65.24 |
| urban_or_rural | 2 | Urban | 9949 | 34.76 |

## Build

| field | value |
|---|---|
| uuid | 01a1ae48-ee3d-73ae-bf99-a2b037658716 |
| checksum | v2:67814a2cb764b9b4774b509d02aeb05b24c17f34e225e371229d3163fcf821f3 |
| built_at | 2026-11-06T00:36:18+00:00 |
| path | economic_well_being_prediction_challenge/01a1ae48-ee3d-73ae-bf99-a2b037658716 |
| data_foundry_version | 0.0.5 |
| git_sha | b4ac95ff0f853de54117555ae24bd013c3630fd4 |
| libraries | {'python': '3.12.3', 'pandas': '3.1.0', 'numpy': '2.5.4', 'pyarrow': '26.0.0', 'scikit-learn': '1.7.2', 'polars': '2.0.0'} |
| stale | yes: the definition now gives checksum `v2:8be24a0eb9315391e3cc96c101247760752a90b8d880aeb5aea1c533b40f7e81` |
