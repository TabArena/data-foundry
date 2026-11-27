---
report_format: data-foundry-report-v2
unique_name: maize_nam_flowering_time
container_format: 2
checksum: v2:e5c4a82b957afe55c2c289a9724a085cd64ffd4f522488f41156aee10e42993f
build: null
build_stale: false
raw_files:
  markergenotypes062508.txt: d2c837df384285fc8cec6d79d6f1a0916a6ca0f157d16d90ba6ef685dda85cc3
  markers061208.txt: e4319eb39526a02b3fe07c649ec4cafdb39e77cdf48ece6df1ba6418de0a8634
  NAMSum0607FloweringTraitBLUPsAcross8Envs.txt: 435488a619b6dd1f24e83f663dd97532b5873c7a4d450e0f13d3cf1578e5594e
data:
  n_rows: 4699
  n_features: 1106
  dtypes:
    float32: 1106
    float64: 1
    int16: 1
  n_test_dataset_rows: null
task:
  target: days_to_anthesis
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
    n_groups: 25
    test_groups_per_fold:
      min: 8
      max: 9
splits:
  n_repeats: 20
  n_folds: 3
  random_state: 4267
  time_horizon: null
  time_horizon_unit: null
  time_gap: null
  time_gap_unit: null
  n_train:
    min: 2970
    max: 3257
  n_test:
    min: 1442
    max: 1729
bundle_checks:
  ok: true
  errors: []
  warnings: []
  infos:
  - task_metric_input_is_model_input
  accepted:
    groups_test_groups_few: '25 families, 8 or 9 per test fold and 1,442 to 1,729
      lines scored per fold. The signal across groups is measured, not assumed, and
      on the spread that matters, which is over the families rather than over the
      60 splits that reuse them: the ridge at alpha 1,000 scores a per-family 0.351
      with an SD of 0.150 over the 25 families, an SE of 0.030, positive in 24 of
      them, running from -0.043 (P39, sweet corn) to +0.506; a random forest scores
      0.303 and beats the dummy on 100% of the 30 splits the task probe runs by +0.3026
      (SE 0.0087); the training mean is undefined per family because it is constant
      there, and a predictor given each test family''s true mean scores exactly 0.
      A within-family label permutation null over 200 runs has mean 0.0005 and SD
      0.0068, putting the observed 53 SDs above it with no run reaching it. The task
      is a breeder''s own: the families are the crosses a breeder makes, and a few
      of them is what a breeding programme holds.'
decisions: []
---

# maize_nam_flowering_time

> Generated from [`dataset.py`](dataset.py) by `dataset check` (or `build`). Do not edit this page: change `dataset.py` and re-run the check.

Regression of `days_to_anthesis`, scored with `mean_group_pearsonr` on grouped splits by `family`. 4,699 rows and 1,106 features. Source: Other (2009).

Not built yet. The current definition gives checksum `v2:e5c4a82b957afe55c2c289a9724a085cd64ffd4f522488f41156aee10e42993f`.

## In brief

**Question.** Which lines of one maize cross will flower earliest, from their marker genotypes alone?

**Use case.** A maize breeder ranks the inbred progeny of a cross before the field season and picks which lines to advance, from the genotype alone (genomic selection), without having grown any of them.

**One row.** One recombinant inbred line of the maize Nested Association Mapping population (4,699 lines of 25 families, each a cross of B73 with one other founder), with its marker calls and its flowering time over the 2006 and 2007 trials.

**Predicted.** The line's days to anthesis in days, as the trials measured it: the best linear unbiased prediction the source published for the line over eight environments. What the task delivers is the ordering inside one cross, not a date (the notes measure both).

**Known at prediction time.** For each of 1,106 linkage-map markers, how much of the line's genome there came from the family's non-B73 founder rather than from B73, as the source imputed it (0, 1 or 2, with 0.5, 1 and 1.5 marking where the imputation places a switch of parental origin), and which family the line comes from.

**What the test data stands for.** Whole families are held out: the test lines are the progeny of a cross whose flowering nobody has measured, which is what a breeder faces with a new cross.

**Our changes to the source.** Days to silk and the anthesis-silking interval, measured in the same plots, are left out: they are not known before the season. The markers take the source's own names, chromosome and map position from the released marker list, and the line id is read from the genotype table and kept out of the features.

> **Use case fit: approximate (a stand-in with a known gap).** The inputs are the genotype a breeder holds before the season and the target is the flowering time the trials measured, in days, on the scale the breeder selects on. The gap is the germplasm: this is a research panel designed to span the species, all crossed to one parent and deliberately unselected, so the level reached here is not a breeder's at-home accuracy.

## Files in this folder

| file | what it is |
|---|---|
| [`dataset.py`](dataset.py) | The definition, and the only file edited by hand: metadata, reading and cleaning the raw files, feature types and splits. |
| [`README.md`](README.md) | This page, generated by `dataset check` and `dataset build`. |

- The curation record, with the triage decision, its sources and the review: [`curation/records/maize_nam_flowering_time.md`](../../../../curation/records/maize_nam_flowering_time.md)
- The original source: <https://doi.org/10.1126/science.1174276>
- The collection this folder belongs to: [`tabarena-v0pt2/README.md`](../README.md) and [`tabarena-v0pt2/CHANGELOG.md`](../CHANGELOG.md)

## Rebuild

`dataset.py` reads its raw files from `local-data-warehouse/maize_nam_flowering_time/`. To get them:

```text
The archive the maize diversity project publishes for Buckler et al. 2009, listed on its phenotypes page as
"Flowering time phenotypes and imputed genotypes of our maize NAM population from Buckler et al. 2009.
Science 325: 714-718". The definition reads three of its seven files.

mkdir -p local-data-warehouse/maize_nam_flowering_time
cd local-data-warehouse/maize_nam_flowering_time
curl -L --fail https://cornell.box.com/shared/static/su1vodojjq5g8wg2aw8crimdx6328px6 -o nam_flowering.zip
# sha256 f7144a2e934aa04402a18d57c7b0cd6d79797cdbff0fc036b8fd2360745adab8
unzip -o nam_flowering.zip
rm nam_flowering.zip
Expected SHA-256:
markergenotypes062508.txt d2c837df384285fc8cec6d79d6f1a0916a6ca0f157d16d90ba6ef685dda85cc3,
markers061208.txt e4319eb39526a02b3fe07c649ec4cafdb39e77cdf48ece6df1ba6418de0a8634,
NAMSum0607FloweringTraitBLUPsAcross8Envs.txt
435488a619b6dd1f24e83f663dd97532b5873c7a4d450e0f13d3cf1578e5594e.
The archive also holds four per-plot tables (days to tassel, days to silk and the two raw dates, 43,054 to
43,459 rows each), which this definition does not read.
```

| file | source | bytes | rows | sha256 (start) |
|---|---|---|---|---|
| `markergenotypes062508.txt` | Other publication | 20,959,975 |  | `d2c837df384285fc` |
| `markers061208.txt` | Other publication | 28,160 |  | `e4319eb39526a02b` |
| `NAMSum0607FloweringTraitBLUPsAcross8Envs.txt` | Other publication | 302,380 |  | `435488a619b6dd1f` |

Then, from the repository root:

```bash
.venv/bin/python -m data_foundry.curation.cli dataset check datasets/_dev/tabarena-v0pt2/maize_nam_flowering_time   # pipeline and checks, no UUID; rewrites this page
.venv/bin/python -m data_foundry.curation.cli dataset build datasets/_dev/tabarena-v0pt2/maize_nam_flowering_time   # also saves the container and records its UUID
```

Only curators run `build`, when the dataset ships.

## Dataset and task

| field | value |
|---|---|
| source | Other: https://doi.org/10.1126/science.1174276 |
| year | 2009 |
| domain | biology & life sciences |
| license | No licence stated by the host, which asserts copyright without granting one; a public release of the NSF-funded maize diversity project |
| data_tags | Non-IID, Grouped, UnseenGroup |
| reference | buckler2009flowering |
| rows x columns | 4,699 x 1,108 |
| task.target | days_to_anthesis |
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
| reason | The decision is which lines of one new cross to advance, a ranking inside the cross, and the split holds out whole families. The original from context is the pooled correlation the field reports; Buckler et al. map flowering-time QTL and declare no prediction metric at all, and the closest published prediction work on this very population and these traits, Ogut et al. 2015 (Heredity 114:552-563), reports ability within each family and across families side by side and warns that the across-family figures run up to twice the within-family ones. MET-18 is what makes the declaration per family: 69.3% of the variance of the line values lies between the 25 families, and a predictor that knows nothing but each test family's own true mean scores a pooled r of 0.793, against 0.209 for a ridge at alpha 1,000 and 0.245 for an untuned LightGBM on the markers, while that same predictor scores exactly 0 within a family, which is this metric's convention for a prediction that does not vary inside a group. A pooled score would therefore rank models by how well they recover a ranking of the crosses that the breeder already holds: the non-recurrent founder's own days to tassel, measured in these very trials, predicts its family's mean at r = 0.965, and predicting held-out lines from that number alone scores a pooled r of 0.764 against the markers' 0.225. Per family, over all 60 shipped splits, the ridge at alpha 1,000 scores 0.351 (SE 0.005 over splits, 0.030 over the 25 families) and the untuned LightGBM 0.265, where the repo's untuned ridge at alpha 1 scores 0.164; the best honest model found is a ridge at alpha 3,000 on within-family centred inputs at 0.421. The metric is what the breeder buys: response to selection is intensity x accuracy x the within-family SD, and that SD is fixed at 1.99 days here, so ranking models by the within-family correlation ranks them by realised gain. Selecting the earliest fifth of each held-out cross returns about 1.0 days for the ridge against 0.77 for a random forest, which is 40% of what a perfect ranking would return, and is positive in 94% of crosses. |
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
@article{buckler2009flowering,
  title = {The genetic architecture of maize flowering time},
  author = {Buckler, Edward S. and Holland, James B. and Bradbury, Peter J. and Acharya, Charlotte B.
            and Brown, Patrick J. and Browne, Chris and Ersoz, Elhan and Flint-Garcia, Sherry and
            Garcia, Arturo and Glaubitz, Jeffrey C. and Goodman, Major M. and Harjes, Carlos and
            Guill, Kate and Kroon, Dallas E. and Larsson, Sara and Lepak, Nicholas K. and Li, Huihui
            and Mitchell, Sharon E. and Pressoir, Gael and Peiffer, Jason A. and Rosas, Marco Oropeza
            and Rocheford, Torbert R. and Romay, M. Cinta and Romero, Susan and Salvo, Stella and
            Villeda, Hector Sanchez and da Silva, H. Sofia and Sun, Qi and Tian, Feng and Upadyayula,
            Narasimham and Ware, Doreen and Yates, Heather and Yu, Jianming and Zhang, Zhiwu and
            Kresovich, Stephen and McMullen, Michael D.},
  journal = {Science},
  volume = {325},
  number = {5941},
  pages = {714--718},
  year = {2009},
  doi = {10.1126/science.1174276},
}
```

</details>

## Sample rows

The first 5 of 4,699 rows of the final frame (random rows: the frame is shuffled); 12 of 1,108 columns, the target first. Cells are cut at 40 characters.

| days_to_anthesis | family | PZA01271.1_chr1_0cM | PZA03613.1_chr1_0.9cM | PZA02129.1_chr1_3.7cM | PZA02032.1_chr1_5.1cM | PHM2244.142_chr1_9.7cM | PZA02372.1_chr1_11.5cM | PHM6238.36_chr1_13.4cM | PZA00181.2_chr1_15.6cM | PZA00528.1_chr1_15.6cM | PZA00175.2_chr1_16.2cM |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 77.7185 | 23 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |
| 78.812 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 79.3474 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 74.6628 | 14 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 69.0565 | 24 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

## Curation notes

The maize Nested Association Mapping population as its own project released it: 4,699 recombinant inbred
lines of 25 families, each the progeny of B73 crossed with one other founder, with 1,106 imputed
linkage-map markers and flowering time measured over eight environments in 2006 and 2007.

- Prediction point: before the field season, when the cross has been made and its inbred progeny genotyped,
  and before any of them has been grown. Everything measured in the plots is after it: days to anthesis is
  the target, and days to silk and the anthesis-silking interval, which the genotype table carries in the
  same three columns, are left out (LEAK-10). They are measured on the same plants within days of the
  target: days to silk correlates 0.886 with it within a family and is predicted equally well (0.373
  against 0.372), so it is the same trait rather than a second one.
- **What a marker column is, and what it is not.** These are not SNP calls. The source coded every marker
  relative to B73, so a 2 means "this line's segment here came from this family's non-B73 founder" and
  names a different plant in each of the 25 families. Measured: every one of the 25 x 1,106 family-by-marker
  mean calls lies between 0.441 and 1.581, 93.5% of them between 0.8 and 1.2, and not one marker is fixed in
  any family, where a real SNP panel across 25 diverse founders would be monomorphic in many of them. Two
  consequences run through everything below. The coding discards founder identity, so the between-family
  part of the target is not reachable from the features at all, which is why no model predicts an unseen
  cross's mean and why the metric is declared per family. And a model fitted here cannot be carried to a
  breeder's own genotype file, which holds alleles rather than parent-of-origin dosages.
- How much of the matrix is a call: no cell is missing, but 7.71% of them are not a call either. 6.27% hold
  1 and 1.44% hold 0.5 or 1.5, and these are the source's posterior over where the parental origin switches,
  not heterozygosity: walking each line along a chromosome, every run of 0.5 is flanked by a 0 and a 1,
  every run of 1.5 by a 1 and a 2, and 79.6% of the runs of 1 by a 0 on one side and a 2 on the other, so
  the values climb a ladder 0, 0.5, 1, 1.5, 2 across each breakpoint. The release carries no unimputed
  version of this marker set, so it is kept with this note rather than repaired (LEAK-30 at most).
- The line value is the source's, not ours (SPLIT-26): the released line table is a best linear unbiased
  prediction per line across the eight environments, in days, which is the scale a breeder selects on
  (MET-3). The archive also ships the 43,459 per-plot observations behind it, which this definition does
  not read; the published line value is the one the population's own papers use. Against an
  environment-adjusted plot mean built from those tables it correlates 0.976, and the between-family share
  of the variance is 0.605 on the raw plot means against 0.635 after adjusting for environment, so the
  family differences are genetic rather than an artefact of where each family was grown.
- The field design behind that value, from the per-plot tables: nine location-year-rep cells over 2006 and
  2007, which are the source's eight environments (Raleigh's two reps are one environment), with environment
  effects spanning 26 days. The eight are not the same eight for every family: nine families miss Columbia
  MO 2006 and get Columbia MO 2007 instead, and a line appears in 2 to 9 cells (median 7). Field blocks are
  balanced, each holding 24 or 25 of the 25 families, so there is no family-by-block confound to remove.
- The genotype table's first column is the line id (`Z001E0001` and so on); it is read, checked against the
  line table and then dropped, since an identifier is no model input. All 4,699 ids are in the line table
  and every one of their three trait values matches it exactly.
- The marker columns arrive unnamed as `i0` to `i1105` and take their names from the released map, whose
  fourth column is the global index 1 to 1,106 and so gives linkage order. Three facts confirm that order on
  the data itself: all nine chromosome boundaries have an adjacent correlation of at most 0.024 while all
  1,096 within-chromosome adjacencies are at least 0.696 (median 0.980); the breaks fall at columns 175,
  302, 432, 543, 682, 760, 838, 944 and 1,029, exactly the map's own chromosome blocks; and, since
  reversing a chromosome would preserve every adjacency, the direction is fixed by comparing the observed
  recombination fractions with the map's distances in sequence, which agree at Spearman 0.936 forward
  against 0.049 reversed, in every one of the ten chromosomes.
- What the genotype table leaves out. The line table holds 5,463 rows: the 25 families, plus the IBM
  population (`pop` 17, B73 crossed with Mo17 and intermated, 200 lines with `MO` identifiers) and a
  281-row block of inbreds (`pop` 27) that includes B73 itself and the founder lines. Neither is a family
  of this panel and neither is genotyped here, so the checks and the founders never become rows of the
  task. Of the 764 line-table rows with a value and no markers, those two account for 481; the other 283
  sit inside the 25 families, 74 of them in `pop` 13, which ships 126 lines against 181 to 196 elsewhere.
  Those 283 flower slightly earlier than their genotyped family-mates (family-centred mean -0.343 days
  against +0.021, p = 0.030) and are more variable (SD 2.76 against 2.04), while their unadjusted means are
  indistinguishable.
- No two lines share a marker profile. Seven pairs are more than 95% identical on the binarised calls, and
  all seven are inside one family, so a grouped split never puts them on opposite sides.
- The family is the group column and no feature: a breeder predicting for a new cross has no family of
  their own in the training data. It stays in the frame because the metric scores within it. No single
  marker gives it away either: the largest between-family share of a marker's variance is 0.037.
- Scope (USE-8): one designed population of 25 crosses that all share B73 as a parent, one 2006-2007 trial
  network of eight environments, one 2008 linkage map of 1,106 markers. Density is not the limit: a line
  carries about 25 recombination breakpoints over a 1,399 cM map, so 1,106 markers is roughly 31 per
  segment, and a tenth of them keeps 92% of the declared metric. The same population now has a genotype
  three orders of magnitude denser, but in absolute alleles rather than parent-of-origin dosages, which
  would be another task rather than a denser version of this one.
- Time basis: UnseenGroup: the breeder ranks the progeny of a cross the data does not hold, so whole families are held out and the two trial years are not weighed: the target is the flowering time of a fixed genotype, published as a line value across its eight environments. The split cannot test a later season, another trial network, or germplasm outside this panel's 26 founders; the last of those is measurable here and is markedly harder, since holding out a whole germplasm group (tropical, temperate, mixed, sweet, popcorn) drops the declared metric to 0.116 for ridge and 0.202 for a random forest, with the two-family sweet-corn group negative for every model. Five groups are too few to split on, so it stays a limit rather than the split. One limit follows from the panel's own design and is accepted with it: every family is a cross to B73, so each test line has half-sibs in training and no held-out family is unrelated to the training ones.

## Splits

The default repeated grouped protocol on the 25 families, 20 repeats of 3 folds, 60 splits: each test fold
holds 8 or 9 whole families and 1,442 to 1,729 of the 4,699 lines. It replaces the random holdout over
lines that the benchmarking work on these panels uses, which was designed for a different question,
comparing algorithms inside a population that is already phenotyped, and is a habit rather than a choice
for ours (SPLIT-5): a random split puts the full siblings of every test line in the training data, which a
breeder ranking a new cross does not have, and it is measurably not harmless, since the markers name a
line's family on 50.3% of held-out lines against 4.0% by chance, so an IID split hands a model the
between-family component the grouped one withholds (pooled R^2 +0.220 against +0.051). Leaf L-EXP.kind of
the split tree. All 60 training sides are distinct family sets and each family is a test family exactly 20
times, but the sides overlap at a mean Jaccard of 0.498, so the honest unit is the family: the spread over
repeats is descriptive, and the uncertainty about a new cross is the spread over the 25 families, four to
six times the spread over splits.

What the split costs, measured on both metrics, since they disagree. On the declared metric it costs 0.024
for the untuned ridge, 0.035 for a random forest and 0.036 for LightGBM against the same 60 splits drawn at
random over lines; paired family by family it costs 0.017 to 0.028. On a pooled R^2 it costs 0.370. The
alternatives were run and none is better: a map-keyed split inside each family is no harder than random
lines, a founder's half-sib group is the family itself since B73 is the only common parent, and
leave-one-germplasm-group-out is markedly harder but has five groups, one of them a single family.

A pooled R^2 can be made to read as no signal here, and it is worth saying why that reading is wrong,
because the first models anyone reaches for produce it. An under-regularised ridge and the group probe's
defaults score below the training mean on unseen families (pooled R^2 down to -0.84; the probe's
learnability line reads ridge -0.500, random forest -0.028, LightGBM -0.025, 5-NN -0.222), which on its
face is a task with no signal across its groups. That is mis-specification, not an absence: the figures
climb monotonically toward zero as the penalty rises, and models that fit the problem clear it. Over 21 of
the shipped splits, a ridge whose penalty is chosen by inner cross-validation scores +0.044 (positive on
20 of 21 folds), a shrunk LightGBM +0.056 (19 of 21), a random forest +0.047 (19 of 21), and a ridge on
markers centred inside each family +0.057, positive on 21 of 21 and the best model found here on the
declared metric as well, at 0.424. The field's own GBLUP was attempted and the implementation was
mis-scaled, so it is not reported.

What is genuinely unreachable is narrower, and it is the reason for the metric rather than a defect: no
model predicts an unseen cross's mean, because the markers are parent-of-origin dosages that name no
founder. Models do not merely miss those means, they get them backwards, predicting in a 76.6 to 77.7 band
against a true 70.2 to 82.9 and correlating -0.72 (ridge) and -0.78 (random forest) with them across the
25 families. The signal is inside the family, where the decision and the declared metric are: the ridge at
alpha 1,000 scores a per-family 0.351, positive on 60 of 60 splits and in 24 of the 25 families, a random
forest 0.303, and a null that shuffles the labels inside each test family puts the observed score 53
standard deviations above it (200 runs, null mean 0.0005, SD 0.0068, none reaching the observed). The curator signs that reading off in the record's review.

20 repeat(s) x 3 fold(s) with seed 4267; train 2,970 to 3,257 rows, test 1,442 to 1,729 rows.

<details>
<summary>Show all 60 splits</summary>

| repeat | fold | n_train | n_test |
|---|---|---|---|
| 0 | 0 | 2986 | 1713 |
| 0 | 1 | 3226 | 1473 |
| 0 | 2 | 3186 | 1513 |
| 1 | 0 | 3044 | 1655 |
| 1 | 1 | 3166 | 1533 |
| 1 | 2 | 3188 | 1511 |
| 2 | 0 | 2971 | 1728 |
| 2 | 1 | 3170 | 1529 |
| 2 | 2 | 3257 | 1442 |
| 3 | 0 | 2974 | 1725 |
| 3 | 1 | 3178 | 1521 |
| 3 | 2 | 3246 | 1453 |
| 4 | 0 | 3050 | 1649 |
| 4 | 1 | 3174 | 1525 |
| 4 | 2 | 3174 | 1525 |
| 5 | 0 | 2984 | 1715 |
| 5 | 1 | 3183 | 1516 |
| 5 | 2 | 3231 | 1468 |
| 6 | 0 | 3038 | 1661 |
| 6 | 1 | 3178 | 1521 |
| 6 | 2 | 3182 | 1517 |
| 7 | 0 | 3044 | 1655 |
| 7 | 1 | 3180 | 1519 |
| 7 | 2 | 3174 | 1525 |
| 8 | 0 | 3002 | 1697 |
| 8 | 1 | 3164 | 1535 |
| 8 | 2 | 3232 | 1467 |
| 9 | 0 | 3033 | 1666 |
| 9 | 1 | 3171 | 1528 |
| 9 | 2 | 3194 | 1505 |
| 10 | 0 | 2973 | 1726 |
| 10 | 1 | 3236 | 1463 |
| 10 | 2 | 3189 | 1510 |
| 11 | 0 | 2997 | 1702 |
| 11 | 1 | 3161 | 1538 |
| 11 | 2 | 3240 | 1459 |
| 12 | 0 | 2983 | 1716 |
| 12 | 1 | 3180 | 1519 |
| 12 | 2 | 3235 | 1464 |
| 13 | 0 | 3032 | 1667 |
| 13 | 1 | 3185 | 1514 |
| 13 | 2 | 3181 | 1518 |
| 14 | 0 | 2975 | 1724 |
| 14 | 1 | 3235 | 1464 |
| 14 | 2 | 3188 | 1511 |
| 15 | 0 | 2981 | 1718 |
| 15 | 1 | 3251 | 1448 |
| 15 | 2 | 3166 | 1533 |
| 16 | 0 | 3061 | 1638 |
| 16 | 1 | 3175 | 1524 |
| 16 | 2 | 3162 | 1537 |
| 17 | 0 | 3031 | 1668 |
| 17 | 1 | 3179 | 1520 |
| 17 | 2 | 3188 | 1511 |
| 18 | 0 | 2970 | 1729 |
| 18 | 1 | 3201 | 1498 |
| 18 | 2 | 3227 | 1472 |
| 19 | 0 | 2979 | 1720 |
| 19 | 1 | 3170 | 1529 |
| 19 | 2 | 3249 | 1450 |

</details>

## Group structure

One group is one family of the Nested Association Mapping population: the recombinant inbred progeny of
B73 crossed with one of 25 other founders, 126 to 196 genotyped lines each. The source designed the
panel so that every family shares B73 as a parent and the other founders span the diversity of the
species; genomic selection is used to rank the progeny of a cross before the season, so whole families
are held out: a test family's flowering times are unknown, as they are for a cross nobody has grown.
Each line is scored on its own. The breeder genotypes the whole progeny of the cross at once and ranks
them together, so a model may use all rows of a test family (`all_rows`). That grant is declared for
the use case and not for a gain, and here it is worth nothing measurable: centring a test family's
markers on its own mean rather than on the training mean gives identical scores, because the declared
metric is a correlation inside the group and a per-family shift does not change it. What does pay is
centring the markers inside every family on the training side, which needs no grant at all and lifts
the untuned ridge from 0.164 to 0.278.

| field | value |
|---|---|
| group column | `family` |
| labels | per_sample |
| order inside a group | none |
| prediction unit | row |
| known about a group when predicting | all_rows |

| statistic | value |
|---|---|
| groups | 25 |
| rows per group (min / median / max) | 126 / 192.0 / 196 |
| largest group | 4.2% of the rows |
| test groups per fold | 8 to 9 |
| groups of two or more rows with a single label | 0.0% |
| nearest neighbour in the same group | 5.9% of the rows (chance: 4.0%) |
| label variance explained by the group | 0.69 (shuffled groups: 0.01) |

The nearest neighbour is computed on the standardised numeric features of a sample of up to 20,000 rows; chance is the share expected if the groups were unrelated to the features. The model-based diagnostics run with `.claude/skills/knowledge-data-foundry/scripts/group_probes.py`.

## Bundle checks

0 error(s), 0 warning(s), 1 info (28 checks run, plus the dataset's own checks).

- **info** `task_metric_input_is_model_input`: The metric reads the task's group or time column(s) ['family'] where they are; they are not scoring columns.

Accepted on purpose:

- `groups_test_groups_few`: 25 families, 8 or 9 per test fold and 1,442 to 1,729 lines scored per fold. The signal across groups is measured, not assumed, and on the spread that matters, which is over the families rather than over the 60 splits that reuse them: the ridge at alpha 1,000 scores a per-family 0.351 with an SD of 0.150 over the 25 families, an SE of 0.030, positive in 24 of them, running from -0.043 (P39, sweet corn) to +0.506; a random forest scores 0.303 and beats the dummy on 100% of the 30 splits the task probe runs by +0.3026 (SE 0.0087); the training mean is undefined per family because it is constant there, and a predictor given each test family's true mean scores exactly 0. A within-family label permutation null over 200 runs has mean 0.0005 and SD 0.0068, putting the observed 53 SDs above it with no run reaching it. The task is a breeder's own: the families are the crosses a breeder makes, and a few of them is what a breeding programme holds.

## Data checks

### Feature summary

<details>
<summary>Show the table (1,108 rows)</summary>

| index | dtype | n_missing | pct_missing | n_unique | examples |
|---|---|---|---|---|---|
| PZA01271.1_chr1_0cM | float32 | 0 | 0 | 3 | 0.0, 2.0, 1.0 |
| PZA03613.1_chr1_0.9cM | float32 | 0 | 0 | 5 | 0.0, 2.0, 1.0, 0.5, 1.5 |
| PZA02129.1_chr1_3.7cM | float32 | 0 | 0 | 5 | 0.0, 2.0, 1.0, 0.5, 1.5 |
| PZA02032.1_chr1_5.1cM | float32 | 0 | 0 | 5 | 0.0, 2.0, 1.0, 1.5, 0.5 |
| PHM2244.142_chr1_9.7cM | float32 | 0 | 0 | 5 | 2.0, 0.0, 1.0, 1.5, 0.5 |
| PZA02372.1_chr1_11.5cM | float32 | 0 | 0 | 5 | 2.0, 0.0, 1.0, 0.5, 1.5 |
| PHM6238.36_chr1_13.4cM | float32 | 0 | 0 | 5 | 0.0, 2.0, 1.0, 1.5, 0.5 |
| PZA00181.2_chr1_15.6cM | float32 | 0 | 0 | 5 | 0.0, 2.0, 1.0, 1.5, 0.5 |
| PZA00528.1_chr1_15.6cM | float32 | 0 | 0 | 5 | 0.0, 2.0, 1.0, 1.5, 0.5 |
| PZA00175.2_chr1_16.2cM | float32 | 0 | 0 | 5 | 0.0, 2.0, 1.0, 1.5, 0.5 |
| PZA00447.8_chr1_17.4cM | float32 | 0 | 0 | 5 | 0.0, 2.0, 1.0, 1.5, 0.5 |
| PZA02284.1_chr1_17.9cM | float32 | 0 | 0 | 5 | 0.0, 2.0, 1.0, 1.5, 0.5 |
| PZA00731.7_chr1_17.9cM | float32 | 0 | 0 | 5 | 0.0, 2.0, 1.0, 1.5, 0.5 |
| PZA00566.5_chr1_19.6cM | float32 | 0 | 0 | 5 | 0.0, 2.0, 1.0, 1.5, 0.5 |
| PZA00106.10_chr1_20.1cM | float32 | 0 | 0 | 5 | 0.0, 2.0, 1.0, 0.5, 1.5 |
| PZA03521.1_chr1_20.1cM | float32 | 0 | 0 | 5 | 0.0, 2.0, 1.0, 0.5, 1.5 |
| PZA00887.1_chr1_21.9cM | float32 | 0 | 0 | 5 | 0.0, 2.0, 1.0, 0.5, 1.5 |
| PZA03551.1_chr1_24.4cM | float32 | 0 | 0 | 5 | 0.0, 2.0, 1.0, 1.5, 0.5 |
| PZA01497.1_chr1_29.7cM | float32 | 0 | 0 | 5 | 2.0, 0.0, 1.0, 1.5, 0.5 |
| csu1171.2_chr1_29.7cM | float32 | 0 | 0 | 5 | 2.0, 0.0, 1.0, 1.5, 0.5 |
| PZA01652.1_chr1_29.9cM | float32 | 0 | 0 | 5 | 0.0, 2.0, 1.0, 0.5, 1.5 |
| PZA02094.9_chr1_31.7cM | float32 | 0 | 0 | 5 | 0.0, 2.0, 1.0, 1.5, 0.5 |
| PZA02393.2_chr1_33.1cM | float32 | 0 | 0 | 5 | 0.0, 2.0, 1.0, 1.5, 0.5 |
| PZB00648.5_chr1_33.9cM | float32 | 0 | 0 | 5 | 0.0, 2.0, 1.0, 1.5, 0.5 |
| PZB00718.5_chr1_33.9cM | float32 | 0 | 0 | 5 | 0.0, 2.0, 1.0, 1.5, 0.5 |
| PZA01030.1_chr1_34.3cM | float32 | 0 | 0 | 5 | 0.0, 2.0, 1.0, 1.5, 0.5 |
| PZA00425.11_chr1_37.8cM | float32 | 0 | 0 | 5 | 2.0, 0.0, 1.0, 1.5, 0.5 |
| PHM13619.5_chr1_39.2cM | float32 | 0 | 0 | 5 | 2.0, 0.0, 1.0, 1.5, 0.5 |
| PZA02487.1_chr1_39.5cM | float32 | 0 | 0 | 5 | 2.0, 0.0, 1.0, 1.5, 0.5 |
| PHM3226.15_chr1_39.5cM | float32 | 0 | 0 | 5 | 2.0, 0.0, 1.0, 1.5, 0.5 |
| PHM4531.46_chr1_39.7cM | float32 | 0 | 0 | 5 | 2.0, 0.0, 1.0, 1.5, 0.5 |
| PZB01957.1_chr1_43.2cM | float32 | 0 | 0 | 5 | 2.0, 0.0, 1.0, 1.5, 0.5 |
| PZB02058.1_chr1_47.3cM | float32 | 0 | 0 | 5 | 2.0, 0.0, 1.0, 0.5, 1.5 |
| PZA02490.1_chr1_51.7cM | float32 | 0 | 0 | 5 | 2.0, 0.0, 1.0, 0.5, 1.5 |
| PZA01348.1_chr1_54cM | float32 | 0 | 0 | 5 | 2.0, 0.0, 1.0, 0.5, 1.5 |
| PZB01662.1_chr1_54cM | float32 | 0 | 0 | 5 | 2.0, 0.0, 1.0, 0.5, 1.5 |
| PZA01455.1_chr1_54cM | float32 | 0 | 0 | 5 | 2.0, 0.0, 1.0, 0.5, 1.5 |
| PZA02686.1_chr1_54cM | float32 | 0 | 0 | 5 | 2.0, 0.0, 1.0, 0.5, 1.5 |
| PZA02271.1_chr1_56.5cM | float32 | 0 | 0 | 5 | 2.0, 0.0, 1.0, 1.5, 0.5 |
| PZA02195.1_chr1_57.2cM | float32 | 0 | 0 | 5 | 2.0, 0.0, 1.0, 0.5, 1.5 |
| PZA00240.6_chr1_59cM | float32 | 0 | 0 | 5 | 2.0, 0.0, 1.0, 0.5, 1.5 |
| PHM3726.129_chr1_59cM | float32 | 0 | 0 | 5 | 2.0, 0.0, 1.0, 0.5, 1.5 |
| PZA00962.1_chr1_59.9cM | float32 | 0 | 0 | 5 | 2.0, 0.0, 1.0, 0.5, 1.5 |
| PZA02376.1_chr1_60.8cM | float32 | 0 | 0 | 5 | 2.0, 0.0, 1.0, 0.5, 1.5 |
| PZA03742.1_chr1_60.8cM | float32 | 0 | 0 | 5 | 2.0, 0.0, 1.0, 1.5, 0.5 |
| PZA03243.2_chr1_60.8cM | float32 | 0 | 0 | 5 | 2.0, 0.0, 1.0, 0.5, 1.5 |
| PZA00081.18_chr1_61.6cM | float32 | 0 | 0 | 5 | 2.0, 0.0, 1.0, 1.5, 0.5 |
| umc13.1_chr1_62.1cM | float32 | 0 | 0 | 5 | 2.0, 0.0, 1.0, 1.5, 0.5 |
| PZA03183.5_chr1_62.1cM | float32 | 0 | 0 | 5 | 2.0, 0.0, 1.0, 1.5, 0.5 |
| PZB00872.3_chr1_62.3cM | float32 | 0 | 0 | 5 | 2.0, 0.0, 1.0, 1.5, 0.5 |
| PHM4913.18_chr1_64.9cM | float32 | 0 | 0 | 5 | 2.0, 0.0, 1.0, 1.5, 0.5 |
| PZA02292.1_chr1_65.7cM | float32 | 0 | 0 | 5 | 0.0, 2.0, 1.0, 1.5, 0.5 |
| PZA03168.5_chr1_66cM | float32 | 0 | 0 | 5 | 0.0, 2.0, 1.0, 0.5, 1.5 |
| PZA02737.1_chr1_69.1cM | float32 | 0 | 0 | 5 | 0.0, 2.0, 1.0, 0.5, 1.5 |
| PZA02550.1_chr1_69.4cM | float32 | 0 | 0 | 5 | 0.0, 2.0, 1.0, 0.5, 1.5 |
| PZA02114.1_chr1_69.6cM | float32 | 0 | 0 | 5 | 0.0, 2.0, 1.0, 1.5, 0.5 |
| PZB01062.3_chr1_70.3cM | float32 | 0 | 0 | 5 | 0.0, 2.0, 1.0, 1.5, 0.5 |
| PZA03561.1_chr1_72cM | float32 | 0 | 0 | 5 | 0.0, 2.0, 1.0, 1.5, 0.5 |
| PZA01315.1_chr1_72cM | float32 | 0 | 0 | 5 | 0.0, 2.0, 1.0, 1.5, 0.5 |
| PZA01476.1_chr1_72.5cM | float32 | 0 | 0 | 5 | 0.0, 2.0, 1.0, 1.5, 0.5 |

(1,048 more rows not shown)

</details>

### Target distribution

| index | y_missing_count | non_positive_pct | skew_y | skew_log | var_y | var_log | log_used | aic_exponential | aic_lognormal | dist_hint |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | -0.036 | -0.193 | 13.542 | 0.002 | log | 87746.1 | 3.30013e+14 | exponential |

### Numeric features

<details>
<summary>Show the table (1,108 rows)</summary>

| index | count | mean | std | min | max |
|---|---|---|---|---|---|
| family | 4699 | 13.2807 | 7.64997 | 1 | 26 |
| days_to_anthesis | 4699 | 77.156 | 3.68 | 66.0158 | 91.2349 |
| PZA01271.1_chr1_0cM | 4699 | 0.989359 | 0.980164 | 0 | 2 |
| PZA03613.1_chr1_0.9cM | 4699 | 0.993084 | 0.979084 | 0 | 2 |
| PZA02129.1_chr1_3.7cM | 4699 | 0.992871 | 0.965619 | 0 | 2 |
| PZA02032.1_chr1_5.1cM | 4699 | 0.996808 | 0.976354 | 0 | 2 |
| PHM2244.142_chr1_9.7cM | 4699 | 1.00745 | 0.972727 | 0 | 2 |
| PZA02372.1_chr1_11.5cM | 4699 | 1.00787 | 0.963931 | 0 | 2 |
| PHM6238.36_chr1_13.4cM | 4699 | 0.99883 | 0.967517 | 0 | 2 |
| PZA00181.2_chr1_15.6cM | 4699 | 0.996701 | 0.966246 | 0 | 2 |
| PZA00528.1_chr1_15.6cM | 4699 | 0.99585 | 0.969102 | 0 | 2 |
| PZA00175.2_chr1_16.2cM | 4699 | 0.993509 | 0.9643 | 0 | 2 |
| PZA00447.8_chr1_17.4cM | 4699 | 0.99319 | 0.965153 | 0 | 2 |
| PZA02284.1_chr1_17.9cM | 4699 | 0.993403 | 0.966312 | 0 | 2 |
| PZA00731.7_chr1_17.9cM | 4699 | 0.995531 | 0.965442 | 0 | 2 |
| PZA00566.5_chr1_19.6cM | 4699 | 0.996063 | 0.959446 | 0 | 2 |
| PZA00106.10_chr1_20.1cM | 4699 | 0.994041 | 0.967031 | 0 | 2 |
| PZA03521.1_chr1_20.1cM | 4699 | 0.993616 | 0.96488 | 0 | 2 |
| PZA00887.1_chr1_21.9cM | 4699 | 0.990636 | 0.954877 | 0 | 2 |
| PZA03551.1_chr1_24.4cM | 4699 | 0.994999 | 0.94671 | 0 | 2 |
| PZA01497.1_chr1_29.7cM | 4699 | 1.00245 | 0.945877 | 0 | 2 |
| csu1171.2_chr1_29.7cM | 4699 | 1.00096 | 0.945992 | 0 | 2 |
| PZA01652.1_chr1_29.9cM | 4699 | 0.998085 | 0.948042 | 0 | 2 |
| PZA02094.9_chr1_31.7cM | 4699 | 0.993935 | 0.95337 | 0 | 2 |
| PZA02393.2_chr1_33.1cM | 4699 | 0.99468 | 0.96301 | 0 | 2 |
| PZB00648.5_chr1_33.9cM | 4699 | 0.995425 | 0.968056 | 0 | 2 |
| PZB00718.5_chr1_33.9cM | 4699 | 0.996063 | 0.971078 | 0 | 2 |
| PZA01030.1_chr1_34.3cM | 4699 | 0.999787 | 0.97199 | 0 | 2 |
| PZA00425.11_chr1_37.8cM | 4699 | 1.01234 | 0.946671 | 0 | 2 |
| PHM13619.5_chr1_39.2cM | 4699 | 1.015 | 0.9507 | 0 | 2 |
| PZA02487.1_chr1_39.5cM | 4699 | 1.01862 | 0.963093 | 0 | 2 |
| PHM3226.15_chr1_39.5cM | 4699 | 1.0199 | 0.963067 | 0 | 2 |
| PHM4531.46_chr1_39.7cM | 4699 | 1.02054 | 0.93939 | 0 | 2 |
| PZB01957.1_chr1_43.2cM | 4699 | 1.02735 | 0.965754 | 0 | 2 |
| PZB02058.1_chr1_47.3cM | 4699 | 1.03299 | 0.946908 | 0 | 2 |
| PZA02490.1_chr1_51.7cM | 4699 | 1.02543 | 0.933702 | 0 | 2 |
| PZA01348.1_chr1_54cM | 4699 | 1.03288 | 0.944351 | 0 | 2 |
| PZB01662.1_chr1_54cM | 4699 | 1.02362 | 0.956079 | 0 | 2 |
| PZA01455.1_chr1_54cM | 4699 | 1.01702 | 0.96668 | 0 | 2 |
| PZA02686.1_chr1_54cM | 4699 | 1.01532 | 0.967148 | 0 | 2 |
| PZA02271.1_chr1_56.5cM | 4699 | 1.01341 | 0.968936 | 0 | 2 |
| PZA02195.1_chr1_57.2cM | 4699 | 1.01351 | 0.953907 | 0 | 2 |
| PZA00240.6_chr1_59cM | 4699 | 1.01213 | 0.960181 | 0 | 2 |
| PHM3726.129_chr1_59cM | 4699 | 1.01011 | 0.961782 | 0 | 2 |
| PZA00962.1_chr1_59.9cM | 4699 | 1.01053 | 0.958119 | 0 | 2 |
| PZA02376.1_chr1_60.8cM | 4699 | 1.01011 | 0.954395 | 0 | 2 |
| PZA03742.1_chr1_60.8cM | 4699 | 1.00883 | 0.965109 | 0 | 2 |
| PZA03243.2_chr1_60.8cM | 4699 | 1.00841 | 0.964727 | 0 | 2 |
| PZA00081.18_chr1_61.6cM | 4699 | 1.00479 | 0.966735 | 0 | 2 |
| umc13.1_chr1_62.1cM | 4699 | 1.00958 | 0.967277 | 0 | 2 |
| PZA03183.5_chr1_62.1cM | 4699 | 1.00904 | 0.967035 | 0 | 2 |
| PZB00872.3_chr1_62.3cM | 4699 | 1.00979 | 0.965072 | 0 | 2 |
| PHM4913.18_chr1_64.9cM | 4699 | 1.0016 | 0.946273 | 0 | 2 |
| PZA02292.1_chr1_65.7cM | 4699 | 0.997872 | 0.963685 | 0 | 2 |
| PZA03168.5_chr1_66cM | 4699 | 0.993084 | 0.964463 | 0 | 2 |
| PZA02737.1_chr1_69.1cM | 4699 | 0.987338 | 0.960146 | 0 | 2 |
| PZA02550.1_chr1_69.4cM | 4699 | 0.991381 | 0.967149 | 0 | 2 |
| PZA02114.1_chr1_69.6cM | 4699 | 0.988402 | 0.965411 | 0 | 2 |
| PZB01062.3_chr1_70.3cM | 4699 | 0.98638 | 0.954881 | 0 | 2 |
| PZA03561.1_chr1_72cM | 4699 | 0.987231 | 0.957564 | 0 | 2 |

(1,048 more rows not shown)

</details>

### Categorical features

No categorical/object features to summarize.

## Build

Not built yet. `dataset build` saves the container to the warehouse and records its UUID, checksum and provenance here.
