---
report_format: data-foundry-report-v2
unique_name: genomic_prediction_soy_yield
container_format: 2
checksum: v2:f39b3809511e5eb336382c515761fe9063298f319f46791e2fddd8a2bb8c4ea1
build: null
build_stale: false
raw_files:
  data.line.qa.csv: ade35f885d05cbf7d4be05149c4ff274117e8463209e5a87c146cea06311b111
  data.check.qa.csv: 7d0f20376083cb709d8235851e3c0e35084c36b13502b48f3980ab498e51f43c
  gen.qa.csv: ef2ba68429e04ca439d220bb0bd3afd5e85811ff023e87685c94369b85b5eb18
  data.line.in.csv: b73908f5d0d2464d67d1c5829bd01184f7bcace1679948d76183559b58fb16cd
  data.check.in.csv: f270b44eb85a087a61074508a00519b0b3ad566cf2122f247486ac8e16119548
data:
  n_rows: 5143
  n_features: 4312
  dtypes:
    float32: 4312
    float64: 1
    int16: 1
  n_test_dataset_rows: null
task:
  target: yield_kg_ha
  problem_type: regression
  metric: mean_group_pearsonr
  metric_origin: context
  scoring_columns: null
  split_regime: grouped_non_iid
  stratify_on: null
  time_on: null
  group_on: family
  group_labels: per_sample
  group_time_on: null
  grouping:
    prediction_unit: row
    aggregation: null
    context: all_rows
    n_groups: 39
    test_groups_per_fold:
      min: 13
      max: 13
splits:
  n_repeats: 20
  n_folds: 3
  random_state: 4267
  time_horizon: null
  time_horizon_unit: null
  time_gap: null
  time_gap_unit: null
  n_train:
    min: 3367
    max: 3501
  n_test:
    min: 1642
    max: 1776
bundle_checks:
  ok: true
  errors: []
  warnings: []
  infos:
  - task_metric_input_is_model_input
  accepted:
    groups_test_groups_few: '39 families, 13 per test fold and about 1,714 lines scored
      per fold. The signal across groups is measured, not assumed: GBLUP, ridge, random
      forest and LightGBM all beat the dummy on the declared metric on 100% of the
      folds (the dummy scores exactly 0 under it); per-family r has SD 0.10 to 0.11,
      so the standard error of the metric over 39 families is 0.010 to 0.015 against
      a mean of 0.12 to 0.23, 12 to 21 standard errors from zero; a null that shuffles
      the labels inside each test family (500 runs, each scored over the 60 folds
      as the models are) gives mean +0.00003, SD 0.0029, max 0.0082, so the measured
      scores sit 41 to 78 null SDs above it at the p = 0.002 floor of 500 runs; and
      38 or 39 of the 39 families score positive under each of the four.'
decisions:
- The line value corrects each plot for its environment and its field block, on the
  check plots alone
- Missing marker calls stay missing
---

# genomic_prediction_soy_yield

> Generated from [`dataset.py`](dataset.py) by `dataset check` (or `build`). Do not edit this page: change `dataset.py` and re-run the check.

Regression of `yield_kg_ha`, scored with `mean_group_pearsonr` on grouped splits by `family`. 5,143 rows and 4,312 features. Source: Other (2015).

Not built yet. The current definition gives checksum `v2:f39b3809511e5eb336382c515761fe9063298f319f46791e2fddd8a2bb8c4ea1`.

## In brief

**Question.** How much grain will a soybean line yield in the Midwest trial network, from its SNP genotype alone?

**Use case.** A soybean breeder ranks the inbred progeny of a cross before the field season and picks which lines to put into yield trials, from the genotype alone (genomic selection), without having grown any of them.

**One row.** One recombinant inbred line of the SoyNAM population (5,143 lines of 39 biparental families, all sharing the parent IA3023), with its quality-assured SNP calls and its yield over the 2011-2014 trials.

**Predicted.** The line's grain yield in kilograms per hectare, as the trials measured it: the mean of its plots after each is corrected for its environment and its field block, both measured on the check plots.

**Known at prediction time.** Which copy of each of 4,312 SNP markers the line carries (0, 1 or 2; a marker the line's cross does not segregate for is not scored and stays missing), and which cross the line comes from.

**What the test data stands for.** Whole crosses are held out: the test lines are the progeny of a cross whose yields nobody has measured, which is what a breeder faces with a new cross.

**Our changes to the source.** We compute the line's yield value from the plot yields, since the source publishes plots, not line values; the agronomic traits measured in the same plots (height, maturity, lodging, protein, oil, seed size) are left out, as they are not known before the season.

> **Use case fit: approximate (a stand-in with a known gap).** The inputs are the genotype a breeder holds before the season and the target is the yield the trials measured, on the scale the breeder selects on. The gap is the germplasm: SoyNAM is an unselected research panel with seven exotic founders, so the level reached here is not a breeder's at-home accuracy. The breadth costs about 0.06 of within-family ability rather than flattering the score (the notes measure it).

## Files in this folder

| file | what it is |
|---|---|
| [`dataset.py`](dataset.py) | The definition, and the only file edited by hand: metadata, reading and cleaning the raw files, feature types and splits. |
| [`README.md`](README.md) | This page, generated by `dataset check` and `dataset build`. |

- The curation record, with the triage decision, its sources and the review: [`curation/records/genomic_prediction_soy_yield.md`](../../../../curation/records/genomic_prediction_soy_yield.md)
- The original source: <https://cran.r-project.org/package=SoyNAM>
- The collection this folder belongs to: [`tabarena-v0pt2/README.md`](../README.md) and [`tabarena-v0pt2/CHANGELOG.md`](../CHANGELOG.md)

## Rebuild

`dataset.py` reads its raw files from `local-data-warehouse/genomic_prediction_soy_yield/`. To get them:

```text
The SoyNAM project's data, as the CRAN package publishes it. The three `soybase` R objects (the
quality-assured release) and the two phenotype objects of `soyin` (the Purdue trial) are converted to CSV
once; the definition reads the CSVs.

mkdir -p local-data-warehouse/genomic_prediction_soy_yield && cd local-data-warehouse/genomic_prediction_soy_yield
curl -L --fail https://cran.r-project.org/src/contrib/SoyNAM_1.6.2.tar.gz -o SoyNAM_1.6.2.tar.gz
# once a newer version is on CRAN, 1.6.2 moves to
# https://cran.r-project.org/src/contrib/Archive/SoyNAM/SoyNAM_1.6.2.tar.gz
# sha256 0bd87f7b101456006a42a11679809349f7545b95dee0b43d954aa5b642995aaa
tar xzf SoyNAM_1.6.2.tar.gz SoyNAM/data/soybase.RData SoyNAM/data/soyin.RData
uvx --from rdata==1.1.0 --with pandas==2.3.3 --with numpy python -I -c "
import numpy as np, pandas as pd, rdata
d = rdata.read_rda('SoyNAM/data/soybase.RData')
for name in ('data.line.qa', 'data.check.qa'):
    d[name].reset_index(drop=True).to_csv(name + '.csv', index=False)
g = d['gen.qa']
pd.DataFrame(np.asarray(g), index=np.asarray(g.coords['dim_0'].values),
             columns=np.asarray(g.coords['dim_1'].values)).rename_axis('strain').astype('Int8').to_csv('gen.qa.csv')
d = rdata.read_rda('SoyNAM/data/soyin.RData')
for name in ('data.line.in', 'data.check.in'):
    d[name].reset_index(drop=True).to_csv(name + '.csv', index=False)
"
rm -r SoyNAM SoyNAM_1.6.2.tar.gz
Expected SHA-256: data.line.qa.csv ade35f885d05cbf7d4be05149c4ff274117e8463209e5a87c146cea06311b111,
data.check.qa.csv 7d0f20376083cb709d8235851e3c0e35084c36b13502b48f3980ab498e51f43c,
gen.qa.csv ef2ba68429e04ca439d220bb0bd3afd5e85811ff023e87685c94369b85b5eb18,
data.line.in.csv b73908f5d0d2464d67d1c5829bd01184f7bcace1679948d76183559b58fb16cd,
data.check.in.csv f270b44eb85a087a61074508a00519b0b3ad566cf2122f247486ac8e16119548.
```

| file | source | bytes | rows | sha256 (start) |
|---|---|---|---|---|
| `data.line.qa.csv` | Other publication | 3,589,716 |  | `ade35f885d05cbf7` |
| `data.check.qa.csv` | Other publication | 600,002 |  | `7d0f20376083cb70` |
| `gen.qa.csv` | Other publication | 39,077,782 |  | `ef2ba68429e04ca4` |
| `data.line.in.csv` | Other publication | 1,297,826 |  | `b73908f5d0d2464d` |
| `data.check.in.csv` | Other publication | 159,987 |  | `f270b44eb85a087a` |

Then, from the repository root:

```bash
.venv/bin/python -m data_foundry.curation.cli dataset check datasets/_dev/tabarena-v0pt2/genomic_prediction_soy_yield   # pipeline and checks, no UUID; rewrites this page
.venv/bin/python -m data_foundry.curation.cli dataset build datasets/_dev/tabarena-v0pt2/genomic_prediction_soy_yield   # also saves the container and records its UUID
```

Only curators run `build`, when the dataset ships.

## Dataset and task

| field | value |
|---|---|
| source | Other: https://cran.r-project.org/package=SoyNAM |
| year | 2015 |
| domain | biology & life sciences |
| license | GPL-3 |
| data_tags | Non-IID, Grouped, UnseenGroup |
| reference | xavier2015soynam |
| rows x columns | 5,143 x 4,314 |
| task.target | yield_kg_ha |
| task.problem_type | regression |
| task.metric | mean_group_pearsonr |
| task.split_regime | grouped_non_iid |
| task.group_on | family |
| task.group_labels | per_sample |

**Metric**

| field | value |
|---|---|
| name | `mean_group_pearsonr` (custom; takes value; higher is better) |
| origin | context: obvious from the task: the source defines no metric |
| definition | mean over groups of the Pearson correlation within the group; method='numerai_corr' transforms first as Numerai's CORR |
| reason | The decision is which lines of one new cross to advance, a ranking inside the cross, and the split holds out whole crosses. The field's own criterion, which the papers on this population report (Xavier et al. 2016, 'predictive ability'; Azodi et al. 2019 rank by Pearson's r 'as it is the standard metric for GP performance'), is the correlation pooled over the held-out lines; it is the original here. 55.7% of the variance of the line values lies between the 39 families (Diers et al. 2018 publish 0.57 from their own trials), and a pooled correlation scores that ranking of the crosses, which a breeder reads off the parents, more than the ranking inside a cross that genomic selection is bought for: on the first 6 shipped splits, giving every test line the true mean of its own cross and nothing else scores a pooled r of 0.69 (RMSE 234 kg/ha) against 0.23 (360 kg/ha) for ridge on the markers, while the same blind predictor scores 0 within the family. The breeder reads that ranking for free: the non-recurrent parent's own yield in the same trials predicts its family's mean at r = 0.94 over the 38 families. Pooled, the markers themselves are worth almost nothing (R^2 +0.0016 over 3 grouped folds, -0.0245 over 5) while the mask of unscored calls alone is worth +0.1629, so a pooled score would rank models by their handling of missing values; within a family the mask is worth r -0.028 against the calls' +0.213. Ridge itself scores 0.236 pooled and 0.239 per family, so the declared metric does not flatter it. The mask and ridge figures of the last two sentences were measured before IN_2014 joined the correction, on line values the shipped ones follow at a within-family r of 0.970; the variance share, the oracle and the parent fact are measured on what ships. |
| inputs | group: `family` |

<details>
<summary>Feature types: 0 categorical, 0 string, 0 datetime</summary>

- categorical (0): none
- string (0): none
- datetime (0): none

</details>

<details>
<summary>BibTeX</summary>

```bibtex
@manual{xavier2015soynam,
  title = {{SoyNAM}: Soybean Nested Association Mapping Dataset},
  author = {Xavier, Alencar and Beavis, William and Specht, James and Diers, Brian and Mian, Rouf
            and Howard, Reka and Graef, George and Nelson, Randall and Schapaugh, William and Wang,
            Dechun and Shannon, Grover and McHale, Leah and Cregan, Perry and Song, Qijian and Lopez,
            Miguel and Muir, William and Rainey, Katy},
  year = {2015},
  note = {R package, version 1.6.2 (2022-01-04); data of the SoyNAM project funded by the United
          Soybean Board, downloaded 2015-11-16 from soybase.org/SoyNAM},
  url = {https://cran.r-project.org/package=SoyNAM},
}
```

</details>

## Sample rows

The first 5 of 5,143 rows of the final frame (random rows: the frame is shuffled); 12 of 4,314 columns, the target first. Cells are cut at 40 characters.

| yield_kg_ha | family | Gm01_3321482_T_C | Gm01_4755976_C_T | Gm01_8340015_T_C | Gm01_9714061_A_G | Gm01_10510009_G_T | Gm01_28793495_C_T | Gm01_34588039_T_C | Gm01_38475026_A_C | Gm01_38891638_T_C | Gm01_38919120_C_T |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2779.69 | 42 | nan | 2 | 2 | 2 | 2 | nan | 2 | 2 | 2 | 2 |
| 3566.65 | 4 | 0 | 0 | nan | nan | nan | 0 | 0 | 0 | 0 | 0 |
| 3495.25 | 9 | nan | nan | nan | 2 | 2 | 2 | 2 | 2 | 2 | 2 |
| 3723.41 | 30 | nan | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |
| 4102.91 | 29 | nan | 0 | 0 | 0 | 0 | nan | 0 | nan | nan | nan |

## Curation notes

We start with the quality-assured `soybase` release of the SoyNAM R package: `data.line.qa` (62,572 plots of
the lines), `data.check.qa` (10,721 plots of the checks and parents) and `gen.qa` (5,180 x 4,312 SNP calls),
and take the one environment of the package's third release object, `soyin` (the Purdue trial at West
Lafayette), that the quality-assured tables do not already hold: `data.line.in` (12,790 line plots over
IN_2013, IN_2014 and IN_2015) and `data.check.in` (1,650 check plots) contribute IN_2014.

- Where the data first appeared (PROV-8, PROV-9): the SoyNAM project released it on SoyBase, whose page the
  package cites ("downloaded on November 16th 2015 from soybase.org/SoyNAM") and which now answers 404. The
  CRAN package of the project's own members is the surviving publication: version 1.0 of 2015-07-29, 1.2 of
  2015-11-18 right after that download, 1.4 of 2018-02-02 with the Indiana 2013-2014 trials, and the pinned
  1.6.2 of 2022-01-04. Hence the year 2015. Diers et al. 2018 (G3 8(10):3367, doi:10.1534/g3.118.200332)
  describe the trials, Song et al. 2017 (Plant Genome 10(2)) the SNP chip, Xavier et al. 2016 (G3 6(8):2611)
  genomic prediction in this panel.
- Prediction point: before the field season, when the cross has been made and its inbred progeny genotyped,
  and before any of them has been grown. Everything measured in the plots is after it: the yield is the
  target, and height, maturity (R8), lodging, protein, oil and seed size are left out (LEAK-10). They are
  the largest thing the definition keeps out, so the size is worth stating: line values of the six traits,
  built as the target was before 2026-11-26, score +0.391 on the declared metric (R^2 0.191) against the
  markers' +0.213 (R^2 0.057), R8 alone +0.168, and markers with the six traits stacked +0.332, which is
  +0.12 (+56%) over the markers alone (honest five-fold cross-validation inside each family; measured
  against the line values of that day, before IN_2014 joined the correction).
- Maturity is the first thing a breeder asks of a soybean yield model. Within a family the line value
  correlates 0.266 with an R8 line value built the same way, and ridge's within-family ability falls only
  from 0.198 to 0.182 when that maturity component is taken out of the yield inside the family, while a
  genomic prediction of R8 alone correlates 0.110 with the yield (3 grouped folds; all four measured on the
  line values before IN_2014 joined the correction, which the shipped ones follow at a within-family r of
  0.970). A maturity component is there; the task is yield, not maturity.
- The release ships plot yields, not line values, so the line value is ours to compute (one row per line is
  what the breeder decides on, SPLIT-23). Each of the 62,478 plots that carry a yield is corrected for its
  environment and for its field block, both measured on the check plots alone, and a line's corrected plots
  are averaged, so the value keeps the kg/ha scale and is not shrunk toward the mean (MET-3). That is model
  1 of Diers et al. 2018, which takes the block effects from the checks and shrinks them toward 0 as BLUPs;
  here the shrinkage is the variance ratio `vb / (vb + ve / n)`, 0.42 to 0.92 over the 1,867 blocks (median
  0.74 at 4 check plots). The package's own `BLUP()` builds its `CHECK()` index from check rows only in the
  same spirit. Two departures from the paper remain true: its second stage has the entry random and no
  environment term at all, while ours averages the line's own corrected plots and carries a centred
  environment effect, the largest term; and its block effects come from 10 check varieties with a
  planting-date covariate, where we have the six checks grown across this trial and no planting date, which
  is not in the quality-assured release at all (in the original it takes 0 to 3 values per environment, 1.02
  per environment x set block, so the environment term absorbs it). Neither release supports the paper's
  exact model, since the block set is only in the quality-assured objects and the planting date only in the
  original ones. Measured on the shipped data: the environment effects run from -1,460 (MI 2012) to +1,519
  (NE 2011) kg/ha, the block effects have an SD of 317 kg/ha (427 before the shrinkage), and a plot departs
  from its line's value by 551 kg/ha SD. The line values run from 2,101 to 4,603 kg/ha (mean 3,582, SD 352;
  within a family 235); with 12 plots a line on average, the entry-mean heritability is 0.797, against the
  0.822 Diers et al. publish in their Table 2. (The 124,218 variance between the line values already carries
  the plot error's 303,391/12.)
- **Exception to SPLIT-26 (2026-11-26, Andrej):** we do not ship the source's rows. The source publishes
  62,478 plot yields and no line value; we ship one row per line, holding a value we compute: each plot is
  corrected for its environment and for its field block, both estimated on the plots of the six checks grown
  across the trial (model 1 of Diers et al. 2018, the block effects shrunk by `vb / (vb + ve / n)` over 1,867
  blocks, the 40 family founders left out of the check set), and a line's value is the mean of its own
  corrected plots, so no line's yield enters another line's value. The fact that sets the case apart: a plot
  yield carries an environment effect spanning 2,979 kg/ha and a shrunken block effect of SD 317 kg/ha
  against a line SD of 352, and a family misses up to 3 of the 19 environments, so no weighting of
  plot-level scores removes the confound, while the line is what the breeder acts on and is the source's own
  task unit. The model form is the source's, the data paper's model 1; the choice of which checks stand in it
  and the shrinkage are ours. The shipped values run 2,101 to 4,603 kg/ha (mean 3,582, SD 352, 235 within a
  family), reach an entry-mean heritability of 0.797 against the 0.822 the data paper publishes, and agree
  with a plain mean of a line's raw plots at r 0.945 pooled and 0.904 within a family. Serves P3 (the breeder
  acts per line) and P4 (a trial bookkeeping artefact is not what the metric should score).
- The line value is ours to compute, the source publishing none, and it is the data paper's model 1 run on
  the checks alone, not an object the package returns.
- Both corrections come from the check plots alone, so no line's yield enters another line's value
  (LEAK-10) and no statistic over the lines enters the target (LEAK-29, LEAK-30): a line's value is the mean
  of its own plots, and all the line table contributes to the correction is which 19 environments have a
  line yield at all. The check tables' 46 strains, which fill the 1,867 blocks with 10,577 plots, are not 46
  checks: 40 are the families' own founder parents, 39 of them standing only in their own family's blocks
  (43 to 49 blocks each, and PI507681B in the four Purdue 2014 blocks of family 46, the family the
  quality-assured release drops) and LD02-4485 serving as a general check in 19 families while 71 of its 457
  plots sit in the blocks of family 12, the family it fathered. The correction uses the other six, grown
  across the trial: IA3023, the common parent of every line, in the blocks of all 40 families (1,489), with
  U06-100052 (1,862), LD04-11056 (1,448) and LD04-13265 (1,444), and IA2094 and U09-215057 in 19 families
  each (409 and 408). Those six fill every one of the 1,867 blocks with 7,923 plots (1 to 16 a block, median
  4), so every line plot has both corrections and the same strains measure the field in every family's
  blocks. Taking the 40 founders in as well, each carrying its own family's genetics, moves the line values
  by 25.8 kg/ha SD (r 0.9973, within-family r 0.9949; family means by at most 36 kg/ha) and lifts the
  declared metric by 0.007 for ridge and 0.012 for an untuned LightGBM over 3 grouped folds, inside a
  fold-to-fold spread of 0.03 and 0.05.
  Removing the block at all is what matters: each family was planted in its own four blocks of an
  environment, so without the correction a family's value carries the patch of field it was grown on.
  Against a value corrected for the environment only, the line values correlate 0.9626 (Spearman 0.9533) and
  differ by 97 kg/ha SD, against a line SD of 352.
- IN_2014 joined the correction on 2026-11-26, after the rebuild below, so every target value is measured
  again on more of the source's own plots: 5,549 plots more, a line's 11 on average becoming 12. The values
  agree with the 18-environment ones at pooled r 0.9862 (Spearman 0.9828), within a family 0.9696 (lowest
  family 0.938), sit 3.5 kg/ha higher on average and differ by 59 kg/ha SD, 56 within a family, against a
  line SD of 352. The score moves less than a fold: over the 60 shipped splits ridge by eigendecomposition
  scores 0.2167 on the 18-environment values and 0.2180 on the shipped ones (at a ten times larger penalty,
  0.2271 against 0.2255), an untuned LightGBM 0.2045 against 0.1996, and ridge on markers centred inside
  the row's own family 0.2971 against 0.2961, while a model's score moves 0.02 to 0.03 between folds. The
  entry-mean heritability rises from 0.789 to 0.797, a line's value resting on more plots.
- The construction was brought into line with Lennart's build of this dataset on 2026-11-26. Before that the
  environment effects were fitted over all 56,929 line plots, which tied a test line's yield to the value of
  the training lines grown beside it, and the block correction was one slope on an index of all 45 check
  strains. The new values correlate 0.9925 with the old ones (Spearman 0.9906; within a family 0.987, the
  lowest family 0.956), sit 29 kg/ha lower on average and differ by 44 kg/ha SD, 39 kg/ha within a family,
  against a line SD of 354. The score moves less than a fold: over 3 grouped folds ridge by
  eigendecomposition scores 0.207 on the old values and 0.198 on the new ones (the paired difference per
  fold runs -0.002 to -0.017) and an untuned LightGBM 0.223 against 0.229 (-0.011 to +0.036 for the new
  values), while either model's score moves 0.03 to 0.06 between folds. The entry-mean heritability falls
  from 0.809 to 0.789, since the check-based corrections carry their own error into a plot.
- Note: the plain mean of a line's plots, the simplest alternative, correlates 0.945 (Spearman 0.932) with
  the shipped value and differs by 119 kg/ha SD. It is biased by which environments a family was grown in: a
  family misses up to 3 of the 19 environments, whose effects span 2,979 kg/ha.
- The quality-assured release is the one we read, not the original `soynam` objects of the same package
  (`data.line`, `data.check`, `gen.raw`) and not the Azodi et al. 2019 cut (below). The reason is the field
  block: `data.line`'s `spot` column has one value per environment (all 60,744 rows are set `2A`), so the
  block the data paper corrects for cannot be recovered from it, while `data.line.qa` carries the set (156
  blocks = 39 families x 4). The cost is 401 lines, one family (46) and 299 markers; family 46 is the
  source's own QA decision, dropped by Diers et al. because its lines were genotypically identical with the
  female founder. The two phenotype tables agree on 53,397 of the 55,945 plot yields they share.
- The third release object, `soyin`, is the Purdue trial at West Lafayette, and one of its three
  environments is new data for this task, so it is used. IN_2014 is a 19th environment: 5,549 line yields,
  none of them a line the quality-assured table already holds there, and check plots that carry all six
  common checks in every one of its 160 blocks (629 plots, 3 to 16 a block), so the environment effect and
  the field-block effect are built there exactly as for the other 18. Its yields are in bu/ac and are
  converted at 67.25 kg/ha, the bushel-per-acre constant and the ratio the two releases' shared IN_2013
  plots show (5,199 matched plot yields, median ratio 67.250, least-squares slope through the origin
  67.249, r 0.9916). The other two environments stay out, and for reasons of data quality rather than
  scope. IN_2013 is the same 5,199 plots the quality-assured table already carries, so taking it would
  count them twice; after the change no (environment, line) pair of the line table repeats that was not
  already repeated in the quality-assured release (572 pairs, every one of them inside it). IN_2015 has
  1,680 yields over 840 lines and no check plots at all, so neither correction can be built there and its
  plots are not comparable with the rest. The object's genotype matrix `gen.in` stays unread, MaCH-imputed
  and worth no line: of IN_2014's 5,549 strains, the 416 the shipped frame does not already hold have no
  `gen.qa` row either (405 of them are new to the line table), so the frame keeps its 5,143 rows.
- Missing marker calls stay missing (CLEAN-7): 25.65% of the calls are not scored. They are not noise but the
  design, and the structure is a block structure: of the 168,168 family-by-marker blocks (39 x 4,312), 41,304
  (24.56%) carry no call at all, 126,584 (75.27%) are scored on 90% or more of the family's lines, 280
  (0.17%) sit between 10% and 90% and none between 0.1% and 10%, and every one of the 126,864 blocks with
  any call is polymorphic within its family. So a marker is blank exactly where the cross does not
  segregate for it: the donor parent carries the common parent's allele there, and the design determines
  the line's genotype rather than failing to read it, so these are not values the breeder lacks. They stay
  blank because the shared allele cannot be read from what the source ships: the common parent IA3023 has
  no genotype row in `gen.qa`, and of the 500 markers that segregate in two or more families all 500 carry
  both homozygotes in every such family, so the matrix does not say which allele is the shared one. A fill
  would be our inference, not the source's call, and it buys nothing on the score. That a breeder meets the
  same pattern in a new cross is inference too, sound but not measured here: a new cross of the same common
  parent, genotyped on the same chip, is scored where it segregates. What the pattern is worth depends on
  the score, which an IID re-user of this frame should know: pooled, the mask of unscored calls alone is
  worth R^2 +0.1629 while the genotype values are worth +0.0016, and the mask names the family exactly
  (k-means on the mask recovers the 39 families at adjusted Rand 1.0000), so an IID split or a pooled
  metric here would measure the handling of missing values. Within a family, where the declared metric
  scores, the mask is worth r -0.028 against the calls' +0.213, and filling the blocks with the family mean
  moves the declared metric by +0.0009. No imputation, over all rows or within a family.
- Leak probes (3 splits, untuned LightGBM; every score below was measured on the line values before IN_2014
  joined the correction, which the shipped ones follow at a within-family r of 0.970, and the findings rest
  on the genotype matrix, which the change does not touch): no test line has an exact feature copy in
  training on any of the
  60 splits, the nearest-neighbour R^2 is negative (-0.42 on the closest tenth), and a depth-2 or depth-3
  tree on the label scores below the mean. Single features score high (`Gm19_40068456_A_G` alone R^2 0.145,
  two markers on chromosome 17 0.118 and 0.115; the all-feature fit falls from 0.072 to 0.047 without the
  first), and what they read is the missingness, not the allele: `Gm19_40068456_A_G` is scored in 1,928 of
  the 5,143 lines and segregates in 15 of the 39 families, its missing indicator alone scores 0.144 against
  the call's 0.145, and among the lines that carry a call the dose explains R^2 0.0078 pooled and 0.0022
  within a family (the three genotype classes differ by 70 kg/ha against a line SD of 352). The column is a
  label of the cross, which is also why a single feature beats the all-feature fit (0.072). It is not a
  shortcut: per family, the best single feature scores 0.016 against 0.244 for LightGBM on all markers, and
  under the family split a test family's own mean is unreachable. Which markers are unscored is information
  a breeder has for a new cross too, since its parents fix the same loci.
- The genotypes ship as the source codes them, 0, 1 or 2 copies of one allele (6.5% of the calls are
  heterozygous), as numeric counts (CLEAN-14), with the source's marker names (chromosome and position, such
  as `Gm01_10510009_G_T`). No marker is constant, all-missing or an exact copy of another on the shipped
  lines, and no two lines carry the same genotype, so the standard drops remove nothing.
- Anomaly: 70 of the 5,142 lines that both matrices hold have raw and quality-assured genotype rows that
  disagree on 10% to 85% of their shared calls, where every other line disagrees on none (median 0%), so for
  those lines one of the two matrices holds a different sample. Both rows still match their own family better
  than any other of the 39, so it is a mix-up inside the family, not a swapped family. The shipped matrix is
  the quality-assured one and nothing is mixed; the 70 lines stay, as there is no evidence which of the two
  rows is the line's own. (Noted while comparing the releases: 1,984 of the 4,312 markers are coded against
  the other allele in `gen.raw` than in `gen.qa`, which is why a naive comparison of the two matrices
  disagrees on 43.2% of all calls.)
- Version: the benchmark TabBench-Bio ships the Azodi et al. 2019 cut of this population (Dryad
  doi:10.5061/dryad.xksn02vb9, Zenodo record 4980429, CC0), 19 files of six species. Four are of this
  population: `soy_pheno.csv` (5,014 lines x HT, R8, YLD), `soy_geno.csv` (5,014 x 4,234 markers recoded
  -1/0/1) and `soy_CVFs.csv` (their random fold assignments), plus the shared `README.txt`. The definition
  reads none of them: their README and the paper's Methods say "Phenotype values were normalized between 0
  and 1" (the shipped YLD has mean 0 and SD 1), so the yield is off its kg/ha scale (MET-3), and the Methods
  say only that the data "were generated from the SoyNAM population", never how a line value was computed
  from the plots (PROV-13, PROV-8). Their 5,014 lines are what is left after "Lines with missing phenotypic
  value for any of the three traits were removed". The 15 files of the other five species (maize, rice,
  sorghum, spruce, switchgrass) are other panels and other tasks. The soy HT and R8 columns would be cuts of
  this table without a distinct task (PROV-6). Licences, since two are in play: what ships comes from the
  GPL-3 package, and the CC0 Dryad/Zenodo record is this derived cut, which we deliberately do not read.
- A public companion file holds a second, independently derived yield for these lines, and it bounds what a
  score here means. The CC0 deposit above is a different derivation of the same trait for the same panel:
  4,230 of our 4,312 markers are shared, so a participant matches a published line by genotype alone for
  91.9% of the test rows, with no identifier needed. Its values correlate 0.63 row-wise with ours and 0.30
  within a family; blended with the best honest model they lift the declared metric from 0.30848 to 0.399,
  and a join on the published line ids reaches about 0.9 within a family against the honest 0.308 (measured
  before IN_2014 joined the correction, on line values that agree with the shipped ones at a within-family
  r of 0.970). No remedy removes it: the markers are the features and the line identifiers are in the
  public file too, so dropping or perturbing columns would destroy the task without closing the join. It is
  recorded here so that a reader knows the bound: the honest ranking of honest models is unaffected, while
  a leaderboard open to the web can be topped by a lookup.
- The 37 rows of `gen.qa` that are parents or check cultivars, not lines, have no line yield and are left
  out, as are the 436 lines that have a yield but no genotype row (31 of the quality-assured table, 405 more
  grown only at Purdue) and the 5,643 line plots whose yield is missing. `data.line.qa` holds a 19th
  environment of its own, NE 2013, which carries no yield at all (5,230 of those 5,643 rows), so the
  correction runs over the 18 quality-assured environments that have one and the Purdue IN_2014.
- The family is the group column and no feature: a breeder predicting for a new cross has no family of their
  own in the training data. It is kept in the frame because the metric scores within it.
- Considered and rejected as a feature: `set`, the plot column that looks like a field position. It is a
  per-line maturity group in the main trial (5,149 of the 5,174 lines keep one letter across the 18
  quality-assured environments, while the Purdue 2014 blocks letter their sets E to H on another
  assignment, which leaves only 10 of the 5,143 shipped lines with one letter across all 19), it
  carries within-family R^2 0.1157 on the target in sample, more than the markers earn, and 0.6044 on
  adjusted R8, and it is half of the target's own block correction. It is a plot attribute, recorded with
  the trial and not held before the season, so it is out under LEAK-10. It is also the channel behind the
  row order: a predictor that is nothing but a line's position in the unshuffled frame scores 0.134 on the
  declared metric, because the line order tracks the maturity set. The framework's seed-42 shuffle is left
  on and is load-bearing here: after it, row position scores -0.0011.
- Scope (USE-8): one population of 39 crosses that all share the parent IA3023, one 2011-2014 Midwest trial
  network of 19 environments, one SNP chip (Song et al. 2017, the SoyNAM 6K BreadChip). The germplasm is
  broader than a breeding programme's, and that is the gap the fit statement names: the panel was designed
  unselected, and 7 of the 38 non-recurrent parents are exotic PI accessions whose families average 3,168
  against 3,673 kg/ha for the 32 elite-parent families, so an elite programme crosses a narrower set than
  this and the level reached here is not a breeder's at-home accuracy. The direction is measured and it is
  not the flattering one: dropping the 7 exotic families lifts the declared metric from 0.236 to 0.276,
  while dropping 7 elite families instead lowers it to 0.219 (20 draws, SD 0.008; measured before IN_2014
  joined the correction), so the breadth costs about 0.06 of within-family ability, a heterogeneous training
  panel predicting the elite families worse.
  What the breadth does inflate is a pooled score: 55.7% of the line-value variance lies between families
  here against 36.1% among the elite families alone, one more reason the metric is within the family.
  Within-family selection in this panel is a different task (a random split of the lines), as is yield in
  another network.
- Time basis: UnseenGroup: the breeder ranks the progeny of a cross the data does not hold, so whole crosses are held out and the trial years are not weighed: the target is the yield of a fixed genotype, measured once by one 2011-2014 protocol, and the field blocks the years differ by are removed from it. The split cannot test a later season, another trial network, or germplasm outside this panel's 40 parents. One limit follows from the panel's own design and is accepted with it: all 39 families share the parent IA3023, so every test line has half-sibs in training and no held-out cross is unrelated to the training ones (a held-out family is still ranked at a pooled r of 0.433 by LightGBM).

## Splits

The default repeated grouped protocol on the 39 families, 20 repeats of 3 folds: each test fold holds 13
whole families and about a third of the 5,143 lines. It replaces the split the work on this population uses,
"an 80/20 training/testing approach ... where 20% of the lines were held out" over 10 replicates (Azodi et
al. 2019, Methods), which was designed for their own question, benchmarking algorithms inside a population
that is already phenotyped, and is a habit rather than a choice for ours (SPLIT-5): a random split puts the
siblings of every test line in the training data, which a breeder ranking a new cross does not have. On a
pooled R^2 that buys a lot (LightGBM 0.579 +- 0.010 over random lines against 0.270 +- 0.055 over held-out
families, 3 x 3 folds), but nearly all of it is the family mean, which the declared metric does not score:
on that metric the departure costs 0.036 (ridge) to 0.117 (LightGBM); those three figures were measured
before IN_2014 joined the correction, and ridge's departure measures 0.030 on the values that ship. A test
family's own feature rows are
all on the test side and may be read (`context="all_rows"`, the grouping definition): centring the markers
within the row's own family is worth +0.078 on the declared metric, so a model that ignores the grouping
spends its fit on variance the metric discards. Leaf L-EXP.kind of the split tree. The repeats reuse the
same 39 families, so the spread over repeats is descriptive, not 39 independent crosses.

20 repeat(s) x 3 fold(s) with seed 4267; train 3,367 to 3,501 rows, test 1,642 to 1,776 rows.

<details>
<summary>Show all 60 splits</summary>

| repeat | fold | n_train | n_test |
|---|---|---|---|
| 0 | 0 | 3463 | 1680 |
| 0 | 1 | 3446 | 1697 |
| 0 | 2 | 3377 | 1766 |
| 1 | 0 | 3369 | 1774 |
| 1 | 1 | 3434 | 1709 |
| 1 | 2 | 3483 | 1660 |
| 2 | 0 | 3432 | 1711 |
| 2 | 1 | 3401 | 1742 |
| 2 | 2 | 3453 | 1690 |
| 3 | 0 | 3411 | 1732 |
| 3 | 1 | 3458 | 1685 |
| 3 | 2 | 3417 | 1726 |
| 4 | 0 | 3383 | 1760 |
| 4 | 1 | 3484 | 1659 |
| 4 | 2 | 3419 | 1724 |
| 5 | 0 | 3457 | 1686 |
| 5 | 1 | 3389 | 1754 |
| 5 | 2 | 3440 | 1703 |
| 6 | 0 | 3411 | 1732 |
| 6 | 1 | 3394 | 1749 |
| 6 | 2 | 3481 | 1662 |
| 7 | 0 | 3432 | 1711 |
| 7 | 1 | 3443 | 1700 |
| 7 | 2 | 3411 | 1732 |
| 8 | 0 | 3403 | 1740 |
| 8 | 1 | 3423 | 1720 |
| 8 | 2 | 3460 | 1683 |
| 9 | 0 | 3447 | 1696 |
| 9 | 1 | 3424 | 1719 |
| 9 | 2 | 3415 | 1728 |
| 10 | 0 | 3481 | 1662 |
| 10 | 1 | 3426 | 1717 |
| 10 | 2 | 3379 | 1764 |
| 11 | 0 | 3472 | 1671 |
| 11 | 1 | 3419 | 1724 |
| 11 | 2 | 3395 | 1748 |
| 12 | 0 | 3415 | 1728 |
| 12 | 1 | 3449 | 1694 |
| 12 | 2 | 3422 | 1721 |
| 13 | 0 | 3464 | 1679 |
| 13 | 1 | 3373 | 1770 |
| 13 | 2 | 3449 | 1694 |
| 14 | 0 | 3465 | 1678 |
| 14 | 1 | 3450 | 1693 |
| 14 | 2 | 3371 | 1772 |
| 15 | 0 | 3442 | 1701 |
| 15 | 1 | 3395 | 1748 |
| 15 | 2 | 3449 | 1694 |
| 16 | 0 | 3440 | 1703 |
| 16 | 1 | 3445 | 1698 |
| 16 | 2 | 3401 | 1742 |
| 17 | 0 | 3501 | 1642 |
| 17 | 1 | 3418 | 1725 |
| 17 | 2 | 3367 | 1776 |
| 18 | 0 | 3473 | 1670 |
| 18 | 1 | 3411 | 1732 |
| 18 | 2 | 3402 | 1741 |
| 19 | 0 | 3458 | 1685 |
| 19 | 1 | 3411 | 1732 |
| 19 | 2 | 3417 | 1726 |

</details>

## Group structure

One group is a biparental family of the SoyNAM population: the inbred progeny of IA3023 crossed with one
of 39 other parents, 98 to 140 lines each. The source designed the panel as more than 5,000 inbred lines
"derived from 40 biparental populations, where progenies were not exposed to selection", every family
sharing "the cultivar IA3023 as the standard parent" (SoyNAM package manual, Dataset); genomic selection
is used to rank the progeny of a cross before the season,
so whole families are held out: a test family's yields are unknown, as they are for a cross nobody has
grown. Each line is scored on its own. The breeder genotypes the whole progeny of the cross at once and
ranks them together, so a model may use all rows of a test family (`all_rows`), and that is worth
having: centring each marker within the row's own family lifts ridge on the declared metric from 0.229
to 0.308 (+0.0795 over the 60 splits, measured before IN_2014 joined the correction; +0.078 with both
sides measured again on the values that ship), as much as an oracle handed the test family's true mean
(0.309).
The grouping is recoverable from the missing-call pattern alone (k-means on the mask recovers the 39
families at adjusted Rand 1.0000), so the gain is open to every participant, with or without the column.

| field | value |
|---|---|
| group column | `family` |
| labels | per_sample |
| order inside a group | none |
| prediction unit | row |
| known about a group when predicting | all_rows |

| statistic | value |
|---|---|
| groups | 39 |
| rows per group (min / median / max) | 98 / 136.0 / 140 |
| largest group | 2.7% of the rows |
| test groups per fold | 13 |
| groups of two or more rows with a single label | 0.0% |
| nearest neighbour in the same group | 21.8% of the rows (chance: 2.6%) |
| label variance explained by the group | 0.56 (shuffled groups: 0.01) |

The nearest neighbour is computed on the standardised numeric features of a sample of up to 20,000 rows; chance is the share expected if the groups were unrelated to the features. The model-based diagnostics run with `.claude/skills/knowledge-data-foundry/scripts/group_probes.py`.

## Decisions

### 1. The line value corrects each plot for its environment and its field block, on the check plots alone

Each family was planted in its own four blocks of an environment, so an effect of the field becomes a difference between families, and a family misses up to 3 of the 19 environments. Both corrections come from the 6 checks grown across the trial: 7,923 plots that fill all 1,867 blocks (1 to 16 a block, median 4), so no line's yield enters another line's value. The environment effects span 2,979 kg/ha and the shrunken block effects have an SD of 317 kg/ha, against a line SD of 352.

| line value from | r with the shipped value | within-family r | difference SD (kg/ha) | SD (kg/ha) | between-family share |
|---|---|---|---|---|---|
| the six common checks (shipped) | 1 | 1 | 0 | 352.4 | 0.557 |
| the common checks and the 40 founders | 0.9973 | 0.9949 | 25.8 | 352.4 | 0.555 |
| the environment only, no field block | 0.9626 | 0.9454 | 97 | 356.7 | 0.536 |
| the plain mean of a line's plots | 0.9454 | 0.9036 | 119 | 364.4 | 0.517 |

### 2. Missing marker calls stay missing

A marker is blank exactly where the family's cross does not segregate for it, so the design determines the call rather than failing to read it. It stays blank because the shared allele cannot be read from the shipped matrix: the common parent has no genotype row, and all 500 markers segregating in two or more families carry both homozygotes in every such family, so any fill would be our inference, not the source's call.

| index | share of a family's marker calls not scored |
|---|---|
| count | 39 |
| mean | 0.258 |
| std | 0.065 |
| min | 0.146 |
| 25% | 0.217 |
| 50% | 0.257 |
| 75% | 0.288 |
| max | 0.44 |

## Bundle checks

0 error(s), 0 warning(s), 1 info (28 checks run, plus the dataset's own checks).

- **info** `task_metric_input_is_model_input`: The metric reads the task's group or time column(s) ['family'] where they are; they are not scoring columns.

Accepted on purpose:

- `groups_test_groups_few`: 39 families, 13 per test fold and about 1,714 lines scored per fold. The signal across groups is measured, not assumed: GBLUP, ridge, random forest and LightGBM all beat the dummy on the declared metric on 100% of the folds (the dummy scores exactly 0 under it); per-family r has SD 0.10 to 0.11, so the standard error of the metric over 39 families is 0.010 to 0.015 against a mean of 0.12 to 0.23, 12 to 21 standard errors from zero; a null that shuffles the labels inside each test family (500 runs, each scored over the 60 folds as the models are) gives mean +0.00003, SD 0.0029, max 0.0082, so the measured scores sit 41 to 78 null SDs above it at the p = 0.002 floor of 500 runs; and 38 or 39 of the 39 families score positive under each of the four.

## Data checks

### Feature summary

<details>
<summary>Show the table (4,314 rows)</summary>

| index | dtype | n_missing | pct_missing | n_unique | examples |
|---|---|---|---|---|---|
| Gm12_15420968_G_T | float32 | 4636 | 90.14 | 3 | 0.0, 2.0, 1.0 |
| Gm12_17864392_T_C | float32 | 4632 | 90.06 | 3 | 0.0, 2.0, 1.0 |
| Gm16_1411646_A_G | float32 | 4268 | 82.99 | 3 | 2.0, 0.0, 1.0 |
| Gm13_20431930_G_A | float32 | 4264 | 82.91 | 3 | 2.0, 0.0, 1.0 |
| Gm02_44265657_A_G | float32 | 3996 | 77.7 | 3 | 2.0, 0.0, 1.0 |
| Gm13_14346156_T_C | float32 | 3877 | 75.38 | 3 | 2.0, 0.0, 1.0 |
| Gm04_30604409_C_T | float32 | 3834 | 74.55 | 3 | 2.0, 0.0, 1.0 |
| Gm02_29931846_A_G | float32 | 3713 | 72.2 | 3 | 2.0, 0.0, 1.0 |
| Gm19_27288411_C_T | float32 | 3627 | 70.52 | 3 | 0.0, 2.0, 1.0 |
| Gm13_10353021_T_C | float32 | 3613 | 70.25 | 3 | 2.0, 0.0, 1.0 |
| Gm19_8669418_A_G | float32 | 3600 | 70 | 3 | 0.0, 2.0, 1.0 |
| Gm04_31890261_C_A | float32 | 3577 | 69.55 | 3 | 2.0, 0.0, 1.0 |
| Gm19_30894325_G_A | float32 | 3575 | 69.51 | 3 | 0.0, 2.0, 1.0 |
| Gm19_31161597_A_G | float32 | 3464 | 67.35 | 3 | 0.0, 2.0, 1.0 |
| Gm18_38907626_C_T | float32 | 3458 | 67.24 | 3 | 0.0, 2.0, 1.0 |
| Gm18_60309238_C_T | float32 | 3453 | 67.14 | 3 | 0.0, 2.0, 1.0 |
| Gm01_50071025_A_C | float32 | 3449 | 67.06 | 3 | 2.0, 0.0, 1.0 |
| Gm19_41558271_G_A | float32 | 3447 | 67.02 | 3 | 2.0, 0.0, 1.0 |
| Gm15_5213738_T_C | float32 | 3441 | 66.91 | 3 | 2.0, 0.0, 1.0 |
| Gm18_9903879_G_T | float32 | 3432 | 66.73 | 3 | 0.0, 2.0, 1.0 |
| Gm15_7127856_G_A | float32 | 3383 | 65.78 | 3 | 2.0, 0.0, 1.0 |
| Gm19_12002408_C_A | float32 | 3376 | 65.64 | 3 | 0.0, 2.0, 1.0 |
| Gm20_42993516_T_C | float32 | 3371 | 65.55 | 3 | 2.0, 0.0, 1.0 |
| Gm16_32186777_A_C | float32 | 3369 | 65.51 | 3 | 0.0, 2.0, 1.0 |
| Gm18_33370738_C_A | float32 | 3368 | 65.49 | 3 | 0.0, 2.0, 1.0 |
| Gm04_18306789_T_G | float32 | 3364 | 65.41 | 3 | 2.0, 0.0, 1.0 |
| Gm20_25425331_G_T | float32 | 3359 | 65.31 | 3 | 0.0, 2.0, 1.0 |
| Gm03_3358231_C_T | float32 | 3354 | 65.21 | 3 | 2.0, 0.0, 1.0 |
| Gm01_42629908_G_A | float32 | 3346 | 65.06 | 3 | 0.0, 2.0, 1.0 |
| Gm04_9038964_T_C | float32 | 3345 | 65.04 | 3 | 2.0, 0.0, 1.0 |
| Gm02_3579235_A_G | float32 | 3333 | 64.81 | 3 | 2.0, 0.0, 1.0 |
| Gm04_2571383_C_T | float32 | 3332 | 64.79 | 3 | 2.0, 0.0, 1.0 |
| Gm03_7577071_A_G | float32 | 3329 | 64.73 | 3 | 2.0, 0.0, 1.0 |
| Gm13_2550479_T_G | float32 | 3305 | 64.26 | 3 | 0.0, 2.0, 1.0 |
| Gm05_7682777_T_C | float32 | 3246 | 63.11 | 3 | 2.0, 0.0, 1.0 |
| Gm19_8296940_C_T | float32 | 3245 | 63.1 | 3 | 0.0, 2.0, 1.0 |
| Gm16_36383355_G_T | float32 | 3235 | 62.9 | 3 | 0.0, 2.0, 1.0 |
| Gm13_3307988_A_G | float32 | 3229 | 62.78 | 3 | 2.0, 0.0, 1.0 |
| Gm04_11262744_C_T | float32 | 3227 | 62.75 | 3 | 0.0, 2.0, 1.0 |
| Gm15_13803483_C_T | float32 | 3224 | 62.69 | 3 | 2.0, 0.0, 1.0 |
| Gm16_30876174_T_C | float32 | 3222 | 62.65 | 3 | 0.0, 2.0, 1.0 |
| Gm16_30835093_T_C | float32 | 3219 | 62.59 | 3 | 2.0, 0.0, 1.0 |
| Gm19_40068456_A_G | float32 | 3215 | 62.51 | 3 | 0.0, 2.0, 1.0 |
| Gm20_42999237_C_A | float32 | 3215 | 62.51 | 3 | 2.0, 0.0, 1.0 |
| Gm15_15220084_T_G | float32 | 3210 | 62.41 | 3 | 2.0, 0.0, 1.0 |
| Gm02_3100048_A_G | float32 | 3207 | 62.36 | 3 | 2.0, 0.0, 1.0 |
| Gm17_24350939_A_G | float32 | 3204 | 62.3 | 3 | 0.0, 2.0, 1.0 |
| Gm17_16755278_A_G | float32 | 3203 | 62.28 | 3 | 2.0, 0.0, 1.0 |
| Gm19_40774629_T_C | float32 | 3203 | 62.28 | 3 | 2.0, 0.0, 1.0 |
| Gm11_6338133_C_T | float32 | 3192 | 62.06 | 3 | 2.0, 0.0, 1.0 |
| Gm17_18902038_T_G | float32 | 3190 | 62.03 | 3 | 0.0, 2.0, 1.0 |
| Gm17_37901800_C_T | float32 | 3187 | 61.97 | 3 | 0.0, 2.0, 1.0 |
| Gm06_14716659_C_T | float32 | 3181 | 61.85 | 3 | 0.0, 2.0, 1.0 |
| Gm02_5591380_G_A | float32 | 3177 | 61.77 | 3 | 2.0, 0.0, 1.0 |
| Gm19_40740547_C_A | float32 | 3177 | 61.77 | 3 | 0.0, 2.0, 1.0 |
| Gm07_37180340_G_A | float32 | 3175 | 61.73 | 3 | 0.0, 2.0, 1.0 |
| Gm19_40729055_G_A | float32 | 3173 | 61.7 | 3 | 0.0, 2.0, 1.0 |
| Gm06_14723656_C_T | float32 | 3168 | 61.6 | 3 | 2.0, 0.0, 1.0 |
| Gm07_15058491_T_C | float32 | 3148 | 61.21 | 3 | 0.0, 2.0, 1.0 |
| Gm09_88026_C_T | float32 | 3138 | 61.01 | 3 | 2.0, 0.0, 1.0 |

(4,254 more rows not shown)

</details>

### Target distribution

| index | y_missing_count | non_positive_pct | skew_y | skew_log | var_y | var_log | log_used | aic_exponential | aic_lognormal | dist_hint |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | -0.592 | -0.909 | 124218 | 0.011 | log | 99974.3 | 6.80603e+15 | exponential |

### Numeric features

<details>
<summary>Show the table (4,314 rows)</summary>

| index | count | mean | std | min | max |
|---|---|---|---|---|---|
| family | 5143 | 25.5347 | 15.1658 | 2 | 64 |
| yield_kg_ha | 5143 | 3581.85 | 352.446 | 2101.11 | 4603.34 |
| Gm01_3321482_T_C | 2464 | 0.980114 | 0.967189 | 0 | 2 |
| Gm01_4755976_C_T | 2516 | 0.999603 | 0.958586 | 0 | 2 |
| Gm01_8340015_T_C | 3409 | 1.00763 | 0.965028 | 0 | 2 |
| Gm01_9714061_A_G | 3666 | 0.994817 | 0.971195 | 0 | 2 |
| Gm01_10510009_G_T | 3819 | 0.991359 | 0.963547 | 0 | 2 |
| Gm01_28793495_C_T | 2633 | 0.983669 | 0.964077 | 0 | 2 |
| Gm01_34588039_T_C | 3285 | 1.04079 | 0.972605 | 0 | 2 |
| Gm01_38475026_A_C | 2315 | 1.02505 | 0.963587 | 0 | 2 |
| Gm01_38891638_T_C | 3694 | 0.991879 | 0.963419 | 0 | 2 |
| Gm01_38919120_C_T | 3732 | 1.01099 | 0.969454 | 0 | 2 |
| Gm01_39354140_T_C | 3208 | 1.00561 | 0.963619 | 0 | 2 |
| Gm01_39591768_C_T | 3225 | 1.00279 | 0.963827 | 0 | 2 |
| Gm01_39642734_C_T | 3205 | 0.981903 | 0.955461 | 0 | 2 |
| Gm01_39831714_A_G | 3189 | 1.00659 | 0.966318 | 0 | 2 |
| Gm01_39853236_G_A | 3589 | 0.999164 | 0.962942 | 0 | 2 |
| Gm01_40577463_T_C | 3468 | 1.01817 | 0.971152 | 0 | 2 |
| Gm01_40624109_G_A | 3485 | 1.0043 | 0.969236 | 0 | 2 |
| Gm01_41204902_T_C | 3494 | 0.998283 | 0.964884 | 0 | 2 |
| Gm01_41873812_G_A | 3471 | 1.00835 | 0.964015 | 0 | 2 |
| Gm01_41904086_C_T | 3469 | 1.00346 | 0.965668 | 0 | 2 |
| Gm01_42085990_C_T | 3460 | 1.00954 | 0.969122 | 0 | 2 |
| Gm01_42204672_C_A | 3495 | 0.997139 | 0.96741 | 0 | 2 |
| Gm01_42629908_G_A | 1797 | 0.991653 | 0.962803 | 0 | 2 |
| Gm01_43040014_T_C | 3217 | 0.989742 | 0.965941 | 0 | 2 |
| Gm01_43068540_G_A | 3240 | 0.986111 | 0.962138 | 0 | 2 |
| Gm01_43140215_G_A | 3221 | 0.989444 | 0.958071 | 0 | 2 |
| Gm01_43216800_T_C | 3887 | 0.965526 | 0.959469 | 0 | 2 |
| Gm01_43514372_A_G | 3388 | 0.971074 | 0.961798 | 0 | 2 |
| Gm01_43645223_A_G | 3227 | 0.979857 | 0.962678 | 0 | 2 |
| Gm01_43770219_C_T | 3251 | 0.986466 | 0.955857 | 0 | 2 |
| Gm01_43796439_C_T | 3214 | 0.999067 | 0.957061 | 0 | 2 |
| Gm01_43822355_T_C | 3238 | 0.970352 | 0.963202 | 0 | 2 |
| Gm01_43856898_C_A | 3199 | 1.05689 | 0.959408 | 0 | 2 |
| Gm01_43878915_C_T | 3238 | 0.982397 | 0.960447 | 0 | 2 |
| Gm01_43905376_A_G | 3108 | 1.06499 | 0.956551 | 0 | 2 |
| Gm01_43956122_T_C | 3255 | 0.973579 | 0.959815 | 0 | 2 |
| Gm01_43979136_A_C | 3755 | 0.992277 | 0.96126 | 0 | 2 |
| Gm01_44034244_T_G | 3747 | 0.990392 | 0.962685 | 0 | 2 |
| Gm01_44127031_G_A | 3185 | 1.00157 | 0.959119 | 0 | 2 |
| Gm01_44196291_C_T | 3225 | 0.992868 | 0.95767 | 0 | 2 |
| Gm01_44260009_A_G | 3253 | 0.980633 | 0.960438 | 0 | 2 |
| Gm01_44395542_G_A | 3770 | 0.990186 | 0.961812 | 0 | 2 |
| Gm01_44427389_T_G | 3746 | 0.982114 | 0.962279 | 0 | 2 |
| Gm01_44553966_C_A | 3754 | 0.99414 | 0.963201 | 0 | 2 |
| Gm01_44639502_A_G | 3766 | 0.991768 | 0.960957 | 0 | 2 |
| Gm01_44716333_G_A | 3597 | 1.00556 | 0.965173 | 0 | 2 |
| Gm01_44766507_G_T | 3618 | 1.01189 | 0.958424 | 0 | 2 |
| Gm01_44785197_A_C | 3611 | 0.985877 | 0.961053 | 0 | 2 |
| Gm01_44832947_G_A | 3602 | 1.00361 | 0.965232 | 0 | 2 |
| Gm01_44893034_C_A | 3476 | 0.989356 | 0.965686 | 0 | 2 |
| Gm01_44922432_T_C | 3579 | 1.01062 | 0.959725 | 0 | 2 |
| Gm01_44944261_T_C | 3620 | 0.996133 | 0.960385 | 0 | 2 |
| Gm01_45053878_A_C | 3626 | 0.999448 | 0.962468 | 0 | 2 |
| Gm01_45119676_T_G | 3611 | 0.995846 | 0.960283 | 0 | 2 |
| Gm01_45145490_G_A | 3642 | 1.00137 | 0.962207 | 0 | 2 |
| Gm01_45171495_T_C | 3612 | 0.991417 | 0.963288 | 0 | 2 |
| Gm01_45193520_T_C | 3739 | 1.00508 | 0.966383 | 0 | 2 |
| Gm01_45275480_A_G | 3765 | 0.991501 | 0.963429 | 0 | 2 |

(4,254 more rows not shown)

</details>

### Categorical features

No categorical/object features to summarize.

## Build

Not built yet. `dataset build` saves the container to the warehouse and records its UUID, checksum and provenance here.
