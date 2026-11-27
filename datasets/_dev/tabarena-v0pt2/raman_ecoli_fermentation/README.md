---
report_format: data-foundry-report-v2
unique_name: raman_ecoli_fermentation
container_format: 2
checksum: v2:2b07306ce438049ccbf87bbe116f70c379bcf2fab9be2138ee012ba693718596
build: null
build_stale: false
data:
  n_rows: 373
  n_features: 1870
  dtypes:
    category: 1
    float64: 1
    int64: 1870
  n_test_dataset_rows: null
task:
  target: glucose_g_per_l
  problem_type: regression
  metric: mae
  metric_origin: source
  scoring_columns: null
  split_regime: grouped_non_iid
  stratify_on: null
  time_on: null
  group_on: experiment_group
  group_labels: per_sample
  group_time_on: null
  grouping:
    prediction_unit: row
    aggregation: null
    context: none
    n_groups: 3
    test_groups_per_fold:
      min: 1
      max: 1
  special_features:
    raman_spectrum: spectrum, a group of 1,870 columns (raman, raw, cm-1 390.63 to
      3384.7); numbers a model can read; recommended encoding spectrum-as-is-r1
splits:
  n_repeats: 20
  n_folds: 3
  random_state: 4267
  time_horizon: null
  time_horizon_unit: null
  time_gap: null
  time_gap_unit: null
  n_train:
    min: 236
    max: 259
  n_test:
    min: 114
    max: 137
bundle_checks:
  ok: true
  errors: []
  warnings: []
  infos:
  - groups_not_clustered
  accepted:
    task_group_count_low: 'Three groups is what the release allows: the 24 cultivations
      were divided into three random groups of eight and no cultivation id ships in
      either copy, so the file a sample comes from is the finest cut there is. The
      signal across groups is real: LightGBM scores R2 0.696 (SE 0.040) with a group
      held out against 0.738 (SE 0.069) on a random split, a gap of 0.042 over 3 repeats
      of 3 folds.'
    groups_test_groups_few: 'One group per test fold, for the same reason: three is
      the finest cut the release allows. Across held-out groups ridge reaches R2 0.780,
      LightGBM 0.696 and a 5-nearest-neighbour 0.585 against a baseline of 0, so a
      cultivation the model has not seen is not a different problem. The spread over
      three folds understates how much a new cultivation could differ; read the score
      with that.'
    groups_largest_share_high: The largest of the three groups holds 37% of the 373
      rows, which is what eight of 24 cultivations sampled at different rates come
      to. The groups are the source's own random draw, not a catch-all value, and
      the glucose floor sits in all three alike (49.1%, 50.8%, 54.0%).
    task_target_value_dominant: 'The 192 zeros (51.5%) are the analyser''s limit of
      quantification, not a placeholder: the next values are 0.0279, 0.0660 and 0.0742
      g/L, a gap rather than a tail, and a glucose-limited fed-batch spends half its
      samples at the floor by design. The rows stay because the floor is a real state
      of the culture and the quantity the feeding strategy acts on (curation notes).'
decisions: []
---

# raman_ecoli_fermentation

> Generated from [`dataset.py`](dataset.py) by `dataset check` (or `build`). Do not edit this page: change `dataset.py` and re-run the check.

Regression of `glucose_g_per_l`, scored with `mae` on grouped splits by `experiment_group`. 373 rows and 1,870 features. Source: Other (2025).

Not built yet. The current definition gives checksum `v2:2b07306ce438049ccbf87bbe116f70c379bcf2fab9be2138ee012ba693718596`.

## In brief

**Question.** How much glucose is in a fed-batch E. coli culture, from an at-line Raman spectrum of its supernatant?

**Use case.** A high-throughput bioprocess facility reads each at-line sample's glucose instead of waiting for the enzymatic analyser, and writes the reading back to the database, where the feeding strategy uses it: 'the predictions are written to the database to allow other models to use them for adjusting feeding strategies' (Lange et al. 2025, Sec. 2.3).

**One row.** One Raman spectrum of the cell-free supernatant of one at-line sample, measured for ten seconds.

**Predicted.** The sample's glucose concentration in g/L, as the Cedex Bio HT analyser measures it on the same sample. The analyser result arrives after the spectrum, which is why the spectrum is worth reading.

**Known at prediction time.** The spectrum. Nothing else: no cultivation id, no time, no setup.

**What the test data stands for.** A cultivation the model has not seen, run in the same facility on the same platform.

**Our changes to the source.** Acetate, the second reference the analyser gives, is dropped: one target ships. The six samples the release leaves without a glucose value are dropped with it.

> **Use case fit: direct (the rows, features and split mirror the use case).** The source's own question on the source's own samples: an at-line spectrum in, the analyser's glucose out, for the feeding decision the paper names. The gap is that a cultivation is held out only as one of three random groups of eight, because no cultivation id ships.

## Files in this folder

| file | what it is |
|---|---|
| [`dataset.py`](dataset.py) | The definition, and the only file edited by hand: metadata, reading and cleaning the raw files, feature types and splits. |
| [`README.md`](README.md) | This page, generated by `dataset check` and `dataset build`. |

- The curation record, with the triage decision, its sources and the review: [`curation/records/raman_ecoli_fermentation.md`](../../../../curation/records/raman_ecoli_fermentation.md)
- The original source: <https://doi.org/10.1002/bit.70006>
- A copy (the fermentation spectra on the measuring instrument's own grid, which this definition reads): <https://huggingface.co/datasets/chlange/RamanSpectraEcoliFermentation>
- The collection this folder belongs to: [`tabarena-v0pt2/README.md`](../README.md) and [`tabarena-v0pt2/CHANGELOG.md`](../CHANGELOG.md)

## Rebuild

`dataset.py` reads its raw files from `local-data-warehouse/raman_ecoli_fermentation/`. To get them:

```text
The spectra are on Hugging Face from the authors, as three CSV files named after the source's three
experiment groups.

mkdir -p local-data-warehouse/raman_ecoli_fermentation/hf
cd local-data-warehouse/raman_ecoli_fermentation/hf
for f in train val test; do
  curl -L -o $f.csv             "https://huggingface.co/datasets/chlange/RamanSpectraEcoliFermentation/resolve/main/$f.csv"
done
```

Then, from the repository root:

```bash
.venv/bin/python -m data_foundry.curation.cli dataset check datasets/_dev/tabarena-v0pt2/raman_ecoli_fermentation   # pipeline and checks, no UUID; rewrites this page
.venv/bin/python -m data_foundry.curation.cli dataset build datasets/_dev/tabarena-v0pt2/raman_ecoli_fermentation   # also saves the container and records its UUID
```

Only curators run `build`, when the dataset ships.

## Dataset and task

| field | value |
|---|---|
| source | Other: https://doi.org/10.1002/bit.70006 |
| year | 2025 |
| domain | biology & life sciences |
| license | CC BY 4.0 |
| data_tags | Non-IID, Grouped, Timeless |
| reference | lange2025raman |
| copy: the fermentation spectra on the measuring instrument's own grid, which this definition reads | HuggingFace (2025): https://huggingface.co/datasets/chlange/RamanSpectraEcoliFermentation; license: CC BY 4.0 |
| rows x columns | 373 x 1,872 |
| task.target | glucose_g_per_l |
| task.problem_type | regression |
| task.metric | mae |
| task.split_regime | grouped_non_iid |
| task.group_on | experiment_group |
| task.group_labels | per_sample |

**Metric**

| field | value |
|---|---|
| name | `mae` (standard; takes value; lower is better) |
| origin | source: the source's metric |
| original | MAE |
| reference | https://doi.org/10.1002/bit.70006 |
| definition | mean(\|y - p\|) |

<details>
<summary>Feature types: 1 categorical, 0 string, 0 datetime, spectrum `raman_spectrum`</summary>

- categorical (1): `experiment_group`
- string (0): none
- datetime (0): none
- special feature `raman_spectrum`: spectrum, a group of 1,870 columns (raman, raw, cm-1 390.63 to 3384.7); numbers a model can read; recommended encoding spectrum-as-is-r1; columns `raman_390.63` to `raman_3384.7`

</details>

<details>
<summary>BibTeX</summary>

```bibtex
@article{lange2025raman,
  title={A Setup for Automatic {Raman} Measurements in High-Throughput Experimentation},
  author={Lange, Christoph and Seidel, Simon and Altmann, Jonas and Stors, Lucas and Kemmer, Annina
          and Cai, Linda and Born, Stefan and Neubauer, Peter and Cruz Bournazou, Mariano Nicolas},
  journal={Biotechnology and Bioengineering},
  volume={122},
  number={10},
  pages={2751--2769},
  year={2025},
  doi={10.1002/bit.70006}
}
```

</details>

## Sample rows

The first 5 of 373 rows of the final frame (random rows: the frame is shuffled); 12 of 1,872 columns, the target first. Cells are cut at 40 characters.

| glucose_g_per_l | experiment_group | raman_390.63 | raman_392.92 | raman_395.2 | raman_397.48 | raman_399.77 | raman_402.05 | raman_404.32 | raman_406.6 | raman_408.88 | raman_411.16 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | train | 12117 | 12152 | 12125 | 12071 | 12137 | 12039 | 12160 | 12115 | 12159 | 12032 |
| 0 | val | 10613 | 10550 | 10482 | 10513 | 10520 | 10624 | 10668 | 10612 | 10535 | 10638 |
| 1.35468 | test | 9827 | 9770 | 9607 | 9579 | 9685 | 9701 | 9698 | 9747 | 9760 | 9637 |
| 0 | train | 13193 | 13060 | 13136 | 13076 | 13195 | 13218 | 13291 | 13158 | 13394 | 13277 |
| 1.22839 | test | 11816 | 11750 | 11622 | 11588 | 11732 | 11634 | 11898 | 11844 | 11773 | 11755 |

## Curation notes

We start with the three CSV files of the Hugging Face release: 379 at-line Raman spectra of cell-free
supernatant from 24 E. coli fed-batch cultivations, 1,870 bands from 390.63 to 3,384.7 cm-1, with the
Cedex Bio HT analyser's glucose and acetate. Every file is read.

- Prediction point: an at-line sample has been drawn from a cultivation and measured on the Raman probe;
  the analyser has not reported yet. Only the spectrum is known. The answer is the glucose concentration
  in g/L.
- Which copy is the data (PROV-8). The paper's repository (git.tu-berlin.de, `raman-kiwi-experiments`)
  holds the same validation and test samples as this release, by their reference values, but its training
  file has 2,400 rows against this release's 139, and its axis is 838 bands from 300.78 to 1,941.12 cm-1
  against 1,870 from 390.63 to 3,384.7. The difference of 2,261 rows is exactly the "2,261 extra spectra
  from eight spectrometers" the paper adds to its training set, and its narrower, coarser axis is the grid
  those eight instruments share. The repository file is therefore the paper's model-training matrix, not
  the fermentation measurement: it is harmonised across instruments and padded with a second dataset,
  which our records carry separately. This definition reads the Hugging Face release, the fermentation
  samples on the measuring instrument's own grid, and declares the repository as a copy.
- The replicate pair. Two ten-second spectra were taken of each sample, and they share the sample's
  reference values: of the 373 rows with both references, 186 reference pairs occur exactly twice and one
  occurs once, so the reference pair identifies the sample (SPLIT-24). The replicates are not separated by
  the split, because the experiment group that holds them is coarser than the sample.
- The split is the source's own (SPLIT-19). The 24 cultivations were "divided into three groups at random"
  of eight (Sec. 2.6.4), and the three files are those groups. No cultivation id ships in either copy, so
  the group is the file a sample comes from: three groups, one held out per fold. Three is few, and it is
  the finest cut the release allows; cultivation ids from the authors would give 24 (SPLIT-25).
- One target ships (CLEAN-18). Glucose is the quantity the feeding strategy acts on and is measured on
  373 of the 379 samples; acetate is dropped. The six samples without a glucose value (two in the first
  group, four in the second) are dropped with their rows.
- The spectrum ships as the release publishes it and is declared as one (`special_features`, CLEAN-26),
  state `raw`: the card names no baseline correction, normalisation or derivative. The bands are renamed
  from the bare wavenumber to `raman_<cm-1>` so the build reads the axis from the names; no value changes.
- The experiment group is the grouping key and never a model input. It carries no information about the
  sample beyond which eight cultivations it came from.
- The signal across the three groups is real, which is what the few-groups warning asks for. Holding a
  group out costs little: LightGBM scores R2 0.696 (SE 0.040) grouped against 0.738 (SE 0.069) on a
  random split, a gap of 0.042 over 3 repeats of 3 folds, and across held-out groups ridge reaches 0.780,
  LightGBM 0.696 and a 5-nearest-neighbour 0.585 against a baseline of 0. A cultivation the model has not
  seen is therefore not a different problem, which is why three groups still carry a score.
- Half the target is a floor, and it is censored, not zero-inflated. 192 of the 373 glucose values are
  exactly 0.0 (51.5%), spread evenly over the three groups (49.1%, 50.8%, 54.0%), and the next smallest
  values are 0.0279, 0.0660 and 0.0742 g/L: a gap, not a continuum. The analyser reports a concentration
  below its limit of quantification as 0, and a glucose-limited fed-batch spends half its samples there
  by design. The zeros are a real state of the culture, not missing data, so the rows stay; what the
  curator decides is whether the task keeps a target that is at its floor half the time (the review's
  issue on the target). Acetate, the other reference, is at 0 on 2 of the 373 rows and runs to 1.592 g/L.
- 373 rows over 187 samples in 24 cultivations is a tiny table (TP-9); glucose runs from 0 to 4.14 g/L.
- Time basis: Timeless: the glucose in a sample is a property of that sample, not of when it was drawn, and the task reads the current concentration from the current spectrum rather than forecasting one. The samples are drawn along the cultivations, but no timestamp, run id or order ships, and the model meets a new cultivation, so whole experiment groups are held out with all their samples and both replicate spectra of each. The split cannot test a later campaign, another facility or another instrument.

## Splits

Default splits.

20 repeat(s) x 3 fold(s) with seed 4267; train 236 to 259 rows, test 114 to 137 rows.

<details>
<summary>Show all 60 splits</summary>

| repeat | fold | n_train | n_test |
|---|---|---|---|
| 0 | 0 | 259 | 114 |
| 0 | 1 | 251 | 122 |
| 0 | 2 | 236 | 137 |
| 1 | 0 | 259 | 114 |
| 1 | 1 | 251 | 122 |
| 1 | 2 | 236 | 137 |
| 2 | 0 | 251 | 122 |
| 2 | 1 | 236 | 137 |
| 2 | 2 | 259 | 114 |
| 3 | 0 | 236 | 137 |
| 3 | 1 | 259 | 114 |
| 3 | 2 | 251 | 122 |
| 4 | 0 | 236 | 137 |
| 4 | 1 | 251 | 122 |
| 4 | 2 | 259 | 114 |
| 5 | 0 | 251 | 122 |
| 5 | 1 | 259 | 114 |
| 5 | 2 | 236 | 137 |
| 6 | 0 | 251 | 122 |
| 6 | 1 | 259 | 114 |
| 6 | 2 | 236 | 137 |
| 7 | 0 | 251 | 122 |
| 7 | 1 | 236 | 137 |
| 7 | 2 | 259 | 114 |
| 8 | 0 | 251 | 122 |
| 8 | 1 | 259 | 114 |
| 8 | 2 | 236 | 137 |
| 9 | 0 | 251 | 122 |
| 9 | 1 | 236 | 137 |
| 9 | 2 | 259 | 114 |
| 10 | 0 | 259 | 114 |
| 10 | 1 | 251 | 122 |
| 10 | 2 | 236 | 137 |
| 11 | 0 | 259 | 114 |
| 11 | 1 | 251 | 122 |
| 11 | 2 | 236 | 137 |
| 12 | 0 | 259 | 114 |
| 12 | 1 | 236 | 137 |
| 12 | 2 | 251 | 122 |
| 13 | 0 | 259 | 114 |
| 13 | 1 | 251 | 122 |
| 13 | 2 | 236 | 137 |
| 14 | 0 | 236 | 137 |
| 14 | 1 | 259 | 114 |
| 14 | 2 | 251 | 122 |
| 15 | 0 | 236 | 137 |
| 15 | 1 | 259 | 114 |
| 15 | 2 | 251 | 122 |
| 16 | 0 | 251 | 122 |
| 16 | 1 | 259 | 114 |
| 16 | 2 | 236 | 137 |
| 17 | 0 | 251 | 122 |
| 17 | 1 | 236 | 137 |
| 17 | 2 | 259 | 114 |
| 18 | 0 | 251 | 122 |
| 18 | 1 | 236 | 137 |
| 18 | 2 | 259 | 114 |
| 19 | 0 | 236 | 137 |
| 19 | 1 | 259 | 114 |
| 19 | 2 | 251 | 122 |

</details>

## Group structure

One group is one of the source's three randomly drawn sets of eight cultivations, which is the only
key to the cultivation the release ships. Holding a group out tests a cultivation the model has not
seen, and keeps both replicate spectra of every one of its samples out with it. Each spectrum is
predicted on its own, as the facility reads one at-line sample at a time.

| field | value |
|---|---|
| group column | `experiment_group` |
| labels | per_sample |
| order inside a group | none |
| prediction unit | row |
| known about a group when predicting | none |

| statistic | value |
|---|---|
| groups | 3 |
| rows per group (min / median / max) | 114 / 122.0 / 137 |
| largest group | 36.7% of the rows |
| test groups per fold | 1 |
| groups of two or more rows with a single label | 0.0% |
| nearest neighbour in the same group | 46.4% of the rows (chance: 33.4%) |
| label variance explained by the group | 0.00 (shuffled groups: 0.02) |

The nearest neighbour is computed on the standardised numeric features of a sample of up to 20,000 rows; chance is the share expected if the groups were unrelated to the features. The model-based diagnostics run with `.claude/skills/knowledge-data-foundry/scripts/group_probes.py`.

## Bundle checks

0 error(s), 0 warning(s), 1 info (28 checks run, plus the dataset's own checks).

- **info** `groups_not_clustered`: Rows are no closer to their own group than chance (46.4% of nearest neighbours vs 33.4%), and the group explains no more of the label than shuffled groups (0.00 vs 0.02). (hint: The grouping may not be needed: compare IID and grouped scores with `.claude/skills/knowledge-data-foundry/scripts/group_probes.py`.)

Accepted on purpose:

- `task_group_count_low`: Three groups is what the release allows: the 24 cultivations were divided into three random groups of eight and no cultivation id ships in either copy, so the file a sample comes from is the finest cut there is. The signal across groups is real: LightGBM scores R2 0.696 (SE 0.040) with a group held out against 0.738 (SE 0.069) on a random split, a gap of 0.042 over 3 repeats of 3 folds.
- `groups_test_groups_few`: One group per test fold, for the same reason: three is the finest cut the release allows. Across held-out groups ridge reaches R2 0.780, LightGBM 0.696 and a 5-nearest-neighbour 0.585 against a baseline of 0, so a cultivation the model has not seen is not a different problem. The spread over three folds understates how much a new cultivation could differ; read the score with that.
- `groups_largest_share_high`: The largest of the three groups holds 37% of the 373 rows, which is what eight of 24 cultivations sampled at different rates come to. The groups are the source's own random draw, not a catch-all value, and the glucose floor sits in all three alike (49.1%, 50.8%, 54.0%).
- `task_target_value_dominant`: The 192 zeros (51.5%) are the analyser's limit of quantification, not a placeholder: the next values are 0.0279, 0.0660 and 0.0742 g/L, a gap rather than a tail, and a glucose-limited fed-batch spends half its samples at the floor by design. The rows stay because the floor is a real state of the culture and the quantity the feeding strategy acts on (curation notes).

## Data checks

### Feature summary

<details>
<summary>Show the table (1,872 rows)</summary>

| index | dtype | n_missing | pct_missing | n_unique | examples |
|---|---|---|---|---|---|
| experiment_group | category | 0 | 0 | 3 | train, test, val |
| glucose_g_per_l | float64 | 0 | 0 | 92 | 0.0, 1.3547, 1.2284, 2.9183, 2.7404, 3.0544, 0.8252, 0.5596, 2.655, 0.1101 |
| raman_390.63 | int64 | 0 | 0 | 342 | 12705, 12579, 12595, 12585, 12796, 12924, 12682, 12824, 12743, 9844 |
| raman_392.92 | int64 | 0 | 0 | 342 | 12562, 12529, 12543, 12979, 12806, 12792, 12664, 12755, 13190, 12644 |
| raman_395.2 | int64 | 0 | 0 | 340 | 12536, 12676, 12826, 12460, 12438, 12602, 12451, 12568, 8303, 12875 |
| raman_397.48 | int64 | 0 | 0 | 344 | 12608, 12570, 12618, 8654, 11852, 12707, 8533, 12573, 12532, 12700 |
| raman_399.77 | int64 | 0 | 0 | 347 | 12703, 12480, 12695, 12642, 12530, 12679, 7873, 12823, 13195, 12960 |
| raman_402.05 | int64 | 0 | 0 | 346 | 12549, 12672, 12628, 12622, 11478, 12769, 8796, 12838, 12751, 12914 |
| raman_404.32 | int64 | 0 | 0 | 346 | 12736, 12769, 12542, 12636, 12535, 12526, 12620, 13037, 12622, 12571 |
| raman_406.6 | int64 | 0 | 0 | 346 | 12820, 12713, 12901, 12886, 8872, 12479, 12897, 8750, 12771, 12539 |
| raman_408.88 | int64 | 0 | 0 | 346 | 12762, 12541, 12904, 12880, 12923, 8806, 12616, 12816, 12634, 12769 |
| raman_411.16 | int64 | 0 | 0 | 351 | 12846, 12473, 12763, 12822, 12771, 12619, 12615, 12700, 12644, 12525 |
| raman_413.43 | int64 | 0 | 0 | 339 | 9729, 13002, 12032, 12759, 12857, 9887, 11105, 12975, 12771, 7922 |
| raman_415.71 | int64 | 0 | 0 | 350 | 12826, 12193, 11183, 12690, 12968, 12733, 12791, 12210, 12780, 12838 |
| raman_417.98 | int64 | 0 | 0 | 348 | 12742, 12750, 12658, 12784, 12713, 12706, 13029, 13085, 10988, 12221 |
| raman_420.25 | int64 | 0 | 0 | 351 | 12977, 12738, 12753, 12794, 12762, 8651, 12722, 12692, 12590, 9999 |
| raman_422.52 | int64 | 0 | 0 | 341 | 12849, 12860, 12880, 12878, 13070, 12875, 12794, 12834, 12086, 12883 |
| raman_424.79 | int64 | 0 | 0 | 353 | 12893, 12701, 10520, 12403, 12566, 12638, 12696, 12568, 7641, 12639 |
| raman_427.06 | int64 | 0 | 0 | 347 | 12949, 12226, 12850, 12894, 12481, 12493, 12662, 9763, 12633, 12551 |
| raman_429.33 | int64 | 0 | 0 | 348 | 12670, 12790, 12675, 12901, 12865, 12571, 12954, 12928, 13091, 12945 |
| raman_431.6 | int64 | 0 | 0 | 351 | 8616, 12917, 12726, 12799, 12893, 12702, 12509, 11023, 12870, 12619 |
| raman_433.87 | int64 | 0 | 0 | 357 | 12813, 12460, 12660, 9723, 12964, 12383, 12504, 12642, 12829, 12559 |
| raman_436.13 | int64 | 0 | 0 | 347 | 8764, 12998, 12512, 12916, 12839, 8500, 12762, 13073, 12733, 12800 |
| raman_438.4 | int64 | 0 | 0 | 353 | 12473, 8798, 12939, 12935, 13076, 12134, 12813, 12629, 12634, 12583 |
| raman_440.66 | int64 | 0 | 0 | 352 | 12652, 12876, 12982, 8146, 12996, 12517, 12889, 12008, 12785, 8767 |
| raman_442.92 | int64 | 0 | 0 | 340 | 12655, 12477, 12859, 12462, 12975, 12368, 12536, 12798, 12778, 12516 |
| raman_445.18 | int64 | 0 | 0 | 344 | 12593, 12645, 12627, 12662, 12632, 12735, 12739, 12529, 12610, 12960 |
| raman_447.44 | int64 | 0 | 0 | 348 | 12293, 12552, 11877, 12330, 12588, 12515, 12640, 12610, 12456, 12493 |
| raman_449.7 | int64 | 0 | 0 | 350 | 12496, 12422, 12506, 12336, 12210, 12521, 12513, 12560, 10114, 12412 |
| raman_451.96 | int64 | 0 | 0 | 347 | 12226, 12516, 12325, 12354, 12095, 12336, 12305, 12300, 12275, 12463 |
| raman_454.22 | int64 | 0 | 0 | 342 | 12446, 12280, 12422, 12401, 12428, 12728, 12492, 12232, 9664, 12817 |
| raman_456.48 | int64 | 0 | 0 | 345 | 12176, 12203, 9569, 12073, 12232, 12357, 8267, 12220, 11951, 12103 |
| raman_458.73 | int64 | 0 | 0 | 350 | 12164, 11965, 11942, 9385, 12442, 12086, 12047, 11888, 8159, 9480 |
| raman_460.99 | int64 | 0 | 0 | 352 | 12030, 8209, 12320, 12171, 12129, 12068, 11926, 12081, 12120, 8330 |
| raman_463.24 | int64 | 0 | 0 | 350 | 9336, 12102, 12172, 11962, 11960, 12074, 11856, 11926, 12094, 12093 |
| raman_465.49 | int64 | 0 | 0 | 347 | 12095, 11876, 11717, 11868, 12058, 11956, 11791, 11861, 11931, 8327 |
| raman_467.75 | int64 | 0 | 0 | 344 | 11773, 12038, 11887, 11876, 11774, 11893, 8181, 11361, 11711, 8221 |
| raman_470.0 | int64 | 0 | 0 | 341 | 11823, 11867, 11718, 11747, 11916, 11937, 7440, 11737, 11935, 11651 |
| raman_472.25 | int64 | 0 | 0 | 341 | 11686, 11639, 10933, 11988, 11794, 11754, 11177, 12038, 11576, 11735 |
| raman_474.5 | int64 | 0 | 0 | 344 | 11702, 11679, 11706, 11805, 11987, 11709, 11087, 11916, 11856, 7973 |
| raman_476.74 | int64 | 0 | 0 | 344 | 11734, 11301, 11554, 11683, 11682, 11632, 11708, 9119, 11785, 11497 |
| raman_478.99 | int64 | 0 | 0 | 343 | 11660, 11594, 8158, 11700, 11769, 11878, 10886, 12127, 11641, 11618 |
| raman_481.24 | int64 | 0 | 0 | 348 | 11661, 11701, 11653, 9490, 11851, 11502, 11800, 11380, 9209, 11593 |
| raman_483.48 | int64 | 0 | 0 | 350 | 11646, 11550, 7645, 11469, 11663, 11725, 11623, 8032, 11559, 11883 |
| raman_485.73 | int64 | 0 | 0 | 350 | 11697, 11467, 11600, 11524, 11396, 11495, 11659, 11591, 11631, 11578 |
| raman_487.97 | int64 | 0 | 0 | 350 | 11277, 11481, 11393, 11619, 11429, 11563, 11279, 11424, 11545, 11493 |
| raman_490.21 | int64 | 0 | 0 | 346 | 11540, 11531, 10907, 11677, 11443, 8974, 11505, 7661, 11928, 11321 |
| raman_492.45 | int64 | 0 | 0 | 347 | 11428, 11440, 11704, 11255, 11450, 11528, 11380, 10922, 7886, 11374 |
| raman_494.69 | int64 | 0 | 0 | 352 | 10800, 11407, 11155, 11318, 11283, 10726, 11314, 11649, 11508, 11422 |
| raman_496.93 | int64 | 0 | 0 | 353 | 11455, 11278, 11123, 11193, 11135, 11156, 11083, 11025, 11206, 11420 |
| raman_499.17 | int64 | 0 | 0 | 355 | 11135, 10739, 11206, 11196, 11109, 11313, 11106, 11735, 11033, 11319 |
| raman_501.41 | int64 | 0 | 0 | 346 | 11027, 10851, 11002, 10374, 11008, 10409, 10929, 11045, 11106, 11177 |
| raman_503.65 | int64 | 0 | 0 | 345 | 11384, 11076, 7590, 10849, 8944, 10992, 10316, 10925, 11266, 10871 |
| raman_505.88 | int64 | 0 | 0 | 340 | 10854, 10921, 10784, 10930, 10750, 10610, 10805, 10795, 10936, 11087 |
| raman_508.12 | int64 | 0 | 0 | 346 | 10893, 10757, 10723, 11007, 10791, 10853, 10770, 10933, 9839, 10683 |
| raman_510.35 | int64 | 0 | 0 | 345 | 10812, 10753, 10717, 10882, 10711, 11110, 10799, 10954, 10886, 10063 |
| raman_512.58 | int64 | 0 | 0 | 349 | 10643, 10597, 10692, 10677, 10478, 10897, 10767, 10676, 10801, 10790 |
| raman_514.82 | int64 | 0 | 0 | 342 | 10922, 10729, 10897, 10686, 10744, 10934, 10600, 10749, 7783, 10857 |
| raman_517.05 | int64 | 0 | 0 | 343 | 10550, 10574, 10530, 10661, 10739, 10826, 10751, 10579, 10854, 10674 |
| raman_519.28 | int64 | 0 | 0 | 346 | 10597, 10487, 10625, 10712, 10264, 10623, 10777, 10645, 10785, 10880 |

(1,812 more rows not shown)

</details>

### Target distribution

| index | y_missing_count | non_positive_pct | skew_y | skew_log | var_y | var_log | log_used | aic_exponential | aic_lognormal | dist_hint |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 51.47 | 0.781 | 0.507 | 1.731 | 0.374 | log1p | 640.8 | 6.49221e+15 | exponential |

### Numeric features

<details>
<summary>Show the table (1,871 rows)</summary>

| index | count | mean | std | min | max |
|---|---|---|---|---|---|
| raman_390.63 | 373 | 11131.9 | 2229.39 | 2382 | 13497 |
| raman_392.92 | 373 | 11081.6 | 2233.44 | 2367 | 13362 |
| raman_395.2 | 373 | 11039.9 | 2233.73 | 2293 | 13265 |
| raman_397.48 | 373 | 11036.6 | 2232.95 | 2300 | 13377 |
| raman_399.77 | 373 | 11078.7 | 2232.69 | 2305 | 13386 |
| raman_402.05 | 373 | 11095.6 | 2238.51 | 2351 | 13469 |
| raman_404.32 | 373 | 11151.4 | 2240.57 | 2426 | 13409 |
| raman_406.6 | 373 | 11126.5 | 2244.57 | 2366 | 13571 |
| raman_408.88 | 373 | 11168.1 | 2251.99 | 2355 | 13517 |
| raman_411.16 | 373 | 11111.9 | 2251.05 | 2322 | 13448 |
| raman_413.43 | 373 | 11131.7 | 2255.9 | 2300 | 13541 |
| raman_415.71 | 373 | 11179.4 | 2259.97 | 2375 | 13652 |
| raman_417.98 | 373 | 11160.1 | 2257.92 | 2353 | 13678 |
| raman_420.25 | 373 | 11150.2 | 2272.07 | 2325 | 13598 |
| raman_422.52 | 373 | 11198 | 2268.72 | 2371 | 13644 |
| raman_424.79 | 373 | 11178 | 2267.81 | 2347 | 13562 |
| raman_427.06 | 373 | 11154.5 | 2259.87 | 2344 | 13570 |
| raman_429.33 | 373 | 11217.7 | 2270.49 | 2451 | 13690 |
| raman_431.6 | 373 | 11107.5 | 2262.3 | 2281 | 13517 |
| raman_433.87 | 373 | 11107.3 | 2260.51 | 2352 | 13601 |
| raman_436.13 | 373 | 11157.5 | 2261.4 | 2377 | 13600 |
| raman_438.4 | 373 | 11106.2 | 2255.12 | 2346 | 13510 |
| raman_440.66 | 373 | 11117.6 | 2250.3 | 2367 | 13562 |
| raman_442.92 | 373 | 11121.7 | 2239.35 | 2420 | 13544 |
| raman_445.18 | 373 | 11039.6 | 2230.14 | 2348 | 13464 |
| raman_447.44 | 373 | 10928 | 2212.22 | 2278 | 13389 |
| raman_449.7 | 373 | 10911.3 | 2200.2 | 2364 | 13323 |
| raman_451.96 | 373 | 10840 | 2180.42 | 2298 | 13192 |
| raman_454.22 | 373 | 10833.8 | 2173.83 | 2352 | 13229 |
| raman_456.48 | 373 | 10692 | 2147.07 | 2256 | 12927 |
| raman_458.73 | 373 | 10657.1 | 2127.93 | 2320 | 12991 |
| raman_460.99 | 373 | 10589.2 | 2119.97 | 2270 | 12784 |
| raman_463.24 | 373 | 10558.6 | 2109.53 | 2296 | 12831 |
| raman_465.49 | 373 | 10529.6 | 2096.68 | 2285 | 12785 |
| raman_467.75 | 373 | 10438.8 | 2082.37 | 2258 | 12621 |
| raman_470.0 | 373 | 10383 | 2072.39 | 2222 | 12653 |
| raman_472.25 | 373 | 10351.6 | 2055.55 | 2260 | 12467 |
| raman_474.5 | 373 | 10373.3 | 2048.2 | 2310 | 12558 |
| raman_476.74 | 373 | 10270.7 | 2037.52 | 2264 | 12370 |
| raman_478.99 | 373 | 10268.1 | 2026.31 | 2273 | 12336 |
| raman_481.24 | 373 | 10239.7 | 2021.12 | 2276 | 12281 |
| raman_483.48 | 373 | 10159.8 | 2017.8 | 2247 | 12345 |
| raman_485.73 | 373 | 10176.6 | 2014.2 | 2269 | 12365 |
| raman_487.97 | 373 | 10110.4 | 1999.22 | 2275 | 12243 |
| raman_490.21 | 373 | 10096 | 1987.05 | 2293 | 12238 |
| raman_492.45 | 373 | 9988.57 | 1977.64 | 2195 | 12085 |
| raman_494.69 | 373 | 9909.58 | 1959.42 | 2180 | 11976 |
| raman_496.93 | 373 | 9896.87 | 1944.54 | 2204 | 11975 |
| raman_499.17 | 373 | 9860.68 | 1925.27 | 2205 | 12023 |
| raman_501.41 | 373 | 9714.86 | 1902.29 | 2092 | 11832 |
| raman_503.65 | 373 | 9620.21 | 1878.8 | 2034 | 11752 |
| raman_505.88 | 373 | 9576.83 | 1866.61 | 2040 | 11542 |
| raman_508.12 | 373 | 9525.47 | 1852.35 | 2005 | 11619 |
| raman_510.35 | 373 | 9483.49 | 1842.96 | 1952 | 11496 |
| raman_512.58 | 373 | 9485.21 | 1843.74 | 1998 | 11575 |
| raman_514.82 | 373 | 9554.41 | 1827.2 | 2055 | 11676 |
| raman_517.05 | 373 | 9361.84 | 1819.21 | 1906 | 11476 |
| raman_519.28 | 373 | 9399.19 | 1813.4 | 1931 | 11364 |
| raman_521.51 | 373 | 9294.61 | 1796.83 | 1883 | 11283 |
| raman_523.73 | 373 | 9293.46 | 1788.08 | 1953 | 11207 |

(1,811 more rows not shown)

</details>

### Categorical features

| column | rank | value | count | pct |
|---|---|---|---|---|
| experiment_group | 1 | train | 137 | 36.73 |
| experiment_group | 2 | test | 122 | 32.71 |
| experiment_group | 3 | val | 114 | 30.56 |

## Build

Not built yet. `dataset build` saves the container to the warehouse and records its UUID, checksum and provenance here.
