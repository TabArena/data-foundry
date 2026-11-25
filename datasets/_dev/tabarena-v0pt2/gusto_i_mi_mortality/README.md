---
report_format: data-foundry-report-v2
unique_name: gusto_i_mi_mortality
container_format: 2
checksum: v2:eb33eaa600d9f4c27ca3aa19809fabd015b5345540acc67d68be67e1214bde97
build: null
build_stale: false
raw_files:
  gusto.csv: 5a96c74ab43305fcaabd94a645e02c8b901c40321112e196295a64867a9b4b20
data:
  n_rows: 40826
  n_features: 22
  dtypes:
    category: 19
    float64: 4
    int64: 1
  n_test_dataset_rows: null
task:
  target: death_by_day_30
  problem_type: binary_classification
  metric: roc_auc
  metric_origin: fallback
  scoring_columns: null
  split_regime: grouped_non_iid
  stratify_on: death_by_day_30
  time_on: null
  group_on: region
  group_labels: per_sample
  group_time_on: null
  grouping:
    prediction_unit: row
    aggregation: null
    context: none
    n_groups: 16
    test_groups_per_fold:
      min: 2
      max: 2
splits:
  n_repeats: 1
  n_folds: 8
  random_state: 4267
  time_horizon: null
  time_horizon_unit: null
  time_gap: null
  time_gap_unit: null
  n_train:
    min: 33037
    max: 36665
  n_test:
    min: 4161
    max: 7789
bundle_checks:
  ok: true
  errors: []
  warnings: []
  infos:
  - dataset_duplicate_rows
  - dataset_conflicting_duplicate_rows
  - groups_not_clustered
  accepted:
    groups_test_groups_few: 'Accepted (Andrej, 2026-11-25): a test region stands for
      the patients of a region the model has never seen, so two whole regions per
      test fold is the task (8 folds, each of the 16 regions tested once; 4,161 to
      7,789 patients and 256 to 554 deaths per test fold). The signal across regions
      is real: the group probe scores ROC AUC 0.824 (logistic regression), 0.814 (random
      forest) and 0.821 (LightGBM) on the held-out regions, and LightGBM 0.821 grouped
      against 0.819 on random folds (2026-11-25).'
    splits_dimensions_off_protocol: 'Accepted (Andrej, 2026-11-25): 1 x 8 region folds
      instead of the protocol''s 3 x 3. Over 6 draws each (`height` dropped, mean
      ROC AUC over the folds), 1 x 8 keeps the gap of lightly tuned LightGBM over
      logistic regression that holding out each region alone shows (0.0067 against
      0.0067), while 3 x 3, which trains on 10 or 11 of the 16 regions, shrinks it
      to 0.0056; the splits comment says why.'
decisions:
- 'Time to relief of chest pain dropped: the randomised treatment changes it'
- 'Height dropped: its filled-in values mark patients who died'
---

# gusto_i_mi_mortality

> Generated from [`dataset.py`](dataset.py) by `dataset check` (or `build`). Do not edit this page: change `dataset.py` and re-run the check.

Binary classification of `death_by_day_30`, scored with `roc_auc` on grouped splits by `region`. 40,826 rows and 22 features. Source: Other (1995).

Not built yet. The current definition gives checksum `v2:eb33eaa600d9f4c27ca3aa19809fabd015b5345540acc67d68be67e1214bde97`.

## In brief

**Question.** Will a patient presenting with an acute myocardial infarction be dead 30 days later?

**Use case.** At initial presentation with an evolving heart attack with ST elevation, within 6 hours of the onset and eligible for thrombolysis, the cardiologist estimates the patient's risk of death, which guides the choice of reperfusion therapy and of care resources (Lee et al. 1995: "Appropriate choices among alternative therapies and the use of clinical resources depend on an estimate of the patient's risk").

**One row.** One of 40,826 patients of the GUSTO-I trial (1990-1993, 1,081 hospitals in 15 countries), randomised to one of the trial's thrombolytic regimens.

**Predicted.** Whether the patient died within 30 days of enrolment; 7.0% did.

**Known at prediction time.** Age, sex, weight, the heart rate, systolic blood pressure and Killip class at presentation, the infarct's location and the number of ECG leads with ST elevation, history (earlier heart attack, angina, hypertension, diabetes, stroke, bypass surgery, smoking, family history), the source's five flags that summarise some of these (shock, hypotension, tachycardia, anterior infarct, high risk) and the assigned thrombolytic regimen.

**What the test data stands for.** Whole regions are held out (16 regions, 8 in the US and 8 elsewhere), two per test fold, so the test data stands for the patients of a region the model has never seen; every region is tested once.

**Our changes to the source.** We drop the time to relief of chest pain, which the randomised treatment changes and so is measured after presentation, and the height, whose filled-in values mark patients who died. A few impossible pulse and blood pressure values become missing.

> **Use case fit: direct (the rows, features and split mirror the use case).** Every input is recorded at presentation, before the thrombolytic acts; the outcome is fixed at day 30. The trial took the patients the decision is made for (ST elevation, within 6 hours, eligible for thrombolysis). The file lacks the source model's time to treatment. The care is that of the thrombolysis era: primary angioplasty has since become the first choice where available.

## Files in this folder

| file | what it is |
|---|---|
| [`dataset.py`](dataset.py) | The definition, and the only file edited by hand: metadata, reading and cleaning the raw files, feature types and splits. |
| [`README.md`](README.md) | This page, generated by `dataset check` and `dataset build`. |

- The curation record, with the triage decision, its sources and the review: [`curation/records/gusto_i_mi_mortality.md`](../../../../curation/records/gusto_i_mi_mortality.md)
- The original source: <https://doi.org/10.1161/01.cir.91.6.1659>
- A copy (the patient file on the Vanderbilt Department of Biostatistics data repository): <https://hbiostat.org/data/repo/gusto.rda>
- The collection this folder belongs to: [`tabarena-v0pt2/README.md`](../README.md) and [`tabarena-v0pt2/CHANGELOG.md`](../CHANGELOG.md)

## Rebuild

`dataset.py` reads its raw files from `local-data-warehouse/gusto_i_mi_mortality/`. To get them:

```text
The patient file gusto.rda from the Vanderbilt Department of Biostatistics data repository (served at the URL
below, not listed in the repository's index; 595,125 bytes; the R package predtools ships the same 40,830 x 29
table). We export it to CSV with pyreadr.

mkdir -p local-data-warehouse/gusto_i_mi_mortality && cd local-data-warehouse/gusto_i_mi_mortality
wget https://hbiostat.org/data/repo/gusto.rda
sha256sum gusto.rda
# e12bc58730894fa26f31b5b4ea963a878e855d7f2d53e47991cf8bb80b84d8e1
uvx --from pyreadr==0.5.9 --with pandas==3.1.1 python -c "import pyreadr; pyreadr.read_r('gusto.rda')['gusto'].to_csv('gusto.csv', index=False)"
sha256sum gusto.csv
# 5a96c74ab43305fcaabd94a645e02c8b901c40321112e196295a64867a9b4b20
```

| file | source | bytes | rows | sha256 (start) |
|---|---|---|---|---|
| `gusto.csv` | the patient file on the Vanderbilt Department of Biostatistics data repository | 3,814,849 |  | `5a96c74ab43305fc` |

Then, from the repository root:

```bash
.venv/bin/python -m data_foundry.curation.cli dataset check datasets/_dev/tabarena-v0pt2/gusto_i_mi_mortality   # pipeline and checks, no UUID; rewrites this page
.venv/bin/python -m data_foundry.curation.cli dataset build datasets/_dev/tabarena-v0pt2/gusto_i_mi_mortality   # also saves the container and records its UUID
```

Only curators run `build`, when the dataset ships.

## Dataset and task

| field | value |
|---|---|
| source | Other: https://doi.org/10.1161/01.cir.91.6.1659 |
| year | 1995 |
| domain | medical & healthcare |
| license | Free use with attribution: hbiostat.org/data states "Permission is granted to anyone wishing to use the data sets provided here. Please reference the original paper" |
| data_tags | Non-IID, Grouped, UnseenGroup |
| reference | lee1995predictors,gusto1993international |
| copy: the patient file on the Vanderbilt Department of Biostatistics data repository | Other: https://hbiostat.org/data/repo/gusto.rda; license: Free use with attribution: hbiostat.org/data states "Permission is granted to anyone wishing to use the data sets provided here. Please reference the original paper" |
| rows x columns | 40,826 x 24 |
| task.target | death_by_day_30 |
| task.problem_type | binary_classification |
| task.metric | roc_auc |
| task.split_regime | grouped_non_iid |
| task.stratify_on | death_by_day_30 |
| task.group_on | region |
| task.group_labels | per_sample |

**Metric**

| field | value |
|---|---|
| name | `roc_auc` (standard; takes proba; higher is better) |
| origin | fallback: the default for the problem type: the source defines no metric the task would use in practice |
| definition | area under the ROC curve |
| reason | Lee et al. 1995 report chi-square statistics per predictor and that the model "accurately estimated the likelihood of death" (abstract; the full text could not be reached); the GUSTO-I case study on this file (Steyerberg and Vergouwe 2014, Eur Heart J, https://pmc.ncbi.nlm.nih.gov/articles/PMC4155437/) scores its models by the c statistic together with calibration in the large and the calibration slope, so no single deliberate metric (MET-5). roc_auc is the binary fallback and the c statistic the case study reports (0.813 internal, 0.812 US to non-US); log loss would also score the calibration the case study weighs. |

<details>
<summary>Feature types: 18 categorical, 1 ordinal, 0 string, 0 datetime</summary>

- categorical (18): `region`, `sex`, `miloc`, `pmi`, `smk`, `tx`, `htn`, `pan`, `fam`, `prevcvd`, `prevcabg`, `dia`, `sho`, `hig`, `ant`, `hyp`, `hrt`, `death_by_day_30`
- ordinal (1): `Killip (I < II < III < IV)`
- string (0): none
- datetime (0): none

</details>

<details>
<summary>BibTeX</summary>

```bibtex
@article{lee1995predictors,
  title={Predictors of 30-day mortality in the era of reperfusion for acute myocardial infarction. Results from an international trial of 41,021 patients},
  author={Lee, Kerry L and Woodlief, Lynn H and Topol, Eric J and Weaver, W Douglas and Betriu, Amadeo and Col, Jacques and Simoons, Maarten and Aylward, Phil and Van de Werf, Frans and Califf, Robert M},
  journal={Circulation},
  volume={91},
  number={6},
  pages={1659--1668},
  year={1995},
  doi={10.1161/01.cir.91.6.1659}
}
@article{gusto1993international,
  title={An international randomized trial comparing four thrombolytic strategies for acute myocardial infarction},
  author={{The GUSTO Investigators}},
  journal={New England Journal of Medicine},
  volume={329},
  number={10},
  pages={673--682},
  year={1993},
  doi={10.1056/NEJM199309023291001}
}
```

</details>

## Sample rows

The first 5 of 40,826 rows of the final frame (random rows: the frame is shuffled); 12 of 24 columns, the target first. Cells are cut at 40 characters.

| death_by_day_30 | sho | hig | dia | hyp | hrt | sex | Killip | age | ste | pulse | sysbp |
|---|---|---|---|---|---|---|---|---|---|---|---|
| No | no | yes | yes | yes | yes | male | II | 43.281 | 2 | 94 | 98 |
| Yes | no | no | yes | no | no | female | I | 73.328 | 5 | 70 | 175 |
| No | no | yes | no | no | no | male | I | 69.5 | 6 | 60 | 154 |
| No | no | no | yes | no | no | male | I | 71.469 | 2 | 74 | 147 |
| No | no | no | no | no | no | male | I | 53.477 | 6 | 47 | 133 |

## Curation notes

We start with gusto.rda, the GUSTO-I patient file of the Vanderbilt Department of Biostatistics repository: 40,830 patients x 29 columns, one row per patient, 2,851 deaths by day 30 (7.0%). It is the one file of the release; the R package predtools ships the same table, and the case-study subsamples of Steyerberg's Clinical Prediction Models (the 2,188-patient West region set among them) are cuts of it.

- Prediction point: initial presentation, before the thrombolytic acts (Lee et al. 1995: "clinical descriptors routinely collected at initial presentation"). Every kept input is recorded then; the target is death within 30 days of enrolment.
- The file's own labels: the R file carries a `label` attribute on 15 columns (pyreadr drops it; read from the serialised file). Among them `dia` "Diabetes", `htn` "History of Hypertension", `fam` "Family History of MI", `pmi` "Previous MI", `miloc` "MI Location", `tx` "Tx in 3 groups", `sysbp` "Systolic Blood Pressure" (mmHg) and `ttr` "Time to Relief of Chest Pain > 1h". `ste` is the number of ECG leads with ST elevation; `pan` (no label) is previous angina pectoris, as the published West-region table confirms (module comment).
- `ttr` (time to relief of chest pain over one hour, yes for 64.9%) is dropped: it is measured after presentation. Randomisation balances the baseline columns across the three arms (chi-square p 0.09 to 0.97; the count of ST leads by a rank test, 0.50), but not `ttr`: 66.3% under streptokinase, 64.6% under the combination and 62.3% under accelerated tPA (p = 3e-11), the order of the regimens' speed of reperfusion, so the treatment given at enrolment changes it. The 8-predictor model of the case-study literature includes it; at the prediction point it is not known (USE-3, LEAK-1). Kept, it would add 0.003 ROC AUC (logistic regression and LightGBM, 5-fold x 3 by region).
- Five flags of the source's simplified models stay as released: `sho` (shock) is Killip class III or IV, `hig` (high risk) is an anterior infarct or a previous MI, `ant` is `miloc` Anterior, all exactly; `hyp` (hypotension) is systolic pressure below 100 and `hrt` (tachycardia) a pulse above 80, except 5 and 8 patients exactly at 100 and 80. None is an exact copy of another column, so none leaves for what it is (CLEAN-5, CLEAN-22), as `ARPU_SEGMENT` in expresso_churn_prediction and `dzclass` in 2_month_survival_rate_prediction stayed. They raise a logistic regression's ROC AUC by 0.003 (15 of 15 folds by region) and LightGBM's not at all (-0.001): they hand a linear model the source's cut points.
- `tpa` is dropped: it is the treatment arm again (1 for tPA, 0 for streptokinase, blank for the combination arm), which `tx` holds. `tx` stays as an input: the arm was randomised and known at enrolment, Lee et al. include the thrombolytic among the predictors, and a model with it gives the risk under each regimen. `tx` merges the two streptokinase arms (subcutaneous or intravenous heparin) as published. Without it ROC AUC drops by 0.000 to 0.002.
- Place codes: `regl` holds 16 regions (1,231 to 4,352 patients, 95 to 294 deaths each). Regions 1, 7, 9, 10, 11, 12, 14 and 15 hold 23,034 patients and 1,565 deaths, exactly the US cohort of Steyerberg and Vergouwe (2014); the other eight hold the 17,796 non-US patients and 1,286 deaths. Region 1 is the "West region" subsample. `grpl` (48 groups) and `grps` (121 groups) are nested in the regions but not in each other, and every `grps` group holds at least 20 deaths, every `grpl` group at least 47: groups of hospitals cut to a minimum number of events for validation studies, not places a model meets. The region is the group column (renamed `region`, never a feature); `grpl` and `grps` are dropped. Held-out regions score as random folds do (LightGBM ROC AUC 0.821 on the 8 region folds, 0.819 on random folds; group probe), and so do the finer groupings (0.823 to 0.825); training on the US and testing outside it, and the reverse, gives 0.815 (LightGBM) and 0.820 (logistic regression), inside the range of the region folds.
- The 191 patients of the 41,021 enrolled who are not in the file are not explained by the release (Steyerberg and Vergouwe's case study uses the same 40,830). The death rates by arm in the file (7.3% for the merged streptokinase arms, 6.3% tPA, 7.0% combination) are the trial's (7.2% and 7.4%, 6.3%, 7.0%). Were all 191 dead, the death rate would be 7.4% instead of 7.0%.
- Imputed values: Steyerberg and Vergouwe say the missing predictor values of this cohort "were filled in with a single imputation procedure considering correlations between predictor variables", so the file holds no blank and cannot show which values were filled. One pattern looks like such fills: 28 patients share every categorical and whole-number value (male, Killip I, inferior infarct, 2 ST leads, pulse 53 or 54, systolic pressure 97 or 104, never smoked, family history and no other history, time to relief over an hour) and differ only in age (31.1 to 40.7), height and weight, which move together; they come from 7 regions and all three arms, and 7 of them died (25%, against 7.0% overall). Kept as published: 0.07% of the rows, and the file cannot show which values were filled.
- Duplicates: 4 rows repeat another row exactly, the arm and the site group included (3 sets of 2 or 3, all survivors, all in that pattern and in region 4); one row of each set stays (LEAK-19), leaving 40,826 patients and 2,851 deaths. Whether they are one patient entered twice or patients filled alike cannot be told. After the drops, 8 more rows of the pattern repeat another row (they differed only in the dropped site groups), and 2 rows share all inputs with a row of the other outcome; kept, as above.
- Class-dependent recording (record marker `Class-dependent Recording`): the heights the source's single imputation filled in mark patients who died. 2,132 heights (5.2% of the rows) are neither whole or half centimetres nor a converted inch value (171.8, 171.3, 170.3, ...), spread less than measured heights, and 19.9% of these patients died against about 6% of the others. The gap holds in 15 of 16 regions and given everything known at presentation (age, sex, Killip class, blood pressure, pulse, infarct location, ST leads, previous MI, region: odds ratio 2.65, p = 2e-54), so the fill follows the outcome (an early death left the height unmeasured, or the outcome entered the imputation), which a model at the door cannot know (LEAK-10 through LEAK-38's conditional test). A model that spots the fills gains 0.0045 ROC AUC (LightGBM, 9 of 9 folds of the earlier 3 x 3 region folds) and a fill flag 0.007 for a regression. Milder fixes fail: the fills set to missing keep the signal (LEAK-40), and heights rounded to whole centimetres still let a model find the filled rows at ROC AUC 0.82 (LEAK-13). So `height` is dropped: it costs a logistic regression nothing (+0.0001) and tuned LightGBM 0.001 to 0.002, the leak itself; without it the filled-height rows cannot be found from the other columns (ROC AUC 0.535). The 1,026 weights of the same look carry no outcome signal (adjusted odds ratio 1.01, p = 0.91; a weight-fill flag adds 0.0000), so `weight` stays. The categorical columns may hold fills the file cannot show; the 28-row pattern above is the visible trace.
- Impossible values set to missing (CLEAN-11, 7 cells): a pulse of 1 to 9 (4 patients, 3 of them Killip I, one with systolic pressure 180), and a pulse or systolic pressure of 0 in a Killip I patient, who is not in shock (3 patients). The other zeros stay as recorded: systolic pressure 0 in 5 patients of Killip III or IV and pulse 0 in 2 of them, all dead, an unmeasurable pressure in shock. Ages over 100 in 3 patients (108, 108, 110, whole numbers while 98.8% of ages carry a fraction) and under 25 in 26 are kept as recorded.
- Outdated (record marker `Outdated`, SEL-18): the care is that of the thrombolysis era; primary angioplasty, stents and newer antiplatelet drugs have lowered the death rate since, while thrombolysis remains the therapy where angioplasty cannot be done in time. The task is still made today, so the fit stays direct (USE-8) and the era is a note.
- Note: the builder's untuned task probes flagged `no_spread` (logistic regression, random forest and LightGBM ROC AUC 0.819, 0.817 and 0.820 by region, with `height` in and the five flags out); on the shipped inputs and the 8 region folds they score 0.829, 0.823 and 0.823 with no flag, and age alone 0.733 (2026-11-25). A few smooth predictors carry most of the signal (Lee et al.: five carry 90% of the prognostic information). Tuned methods separate: on the shipped inputs and the 8 region folds (2026-11-25), a logistic regression with splines reaches 0.8264 and a lightly tuned LightGBM 0.8272 against 0.8234 for a plain logistic regression (splines +0.0030, standard error 0.0008, better on 7 of 8 folds; LightGBM +0.0038, standard error 0.0014, 7 of 8; log loss 0.1997 and 0.1996 against 0.2008). Not `Trivial`: the TIMI risk score for STEMI (Morrow et al. 2000), a published score not fitted on these data, reaches 0.794 on the whole file.
- Codes get their words: the 1/2 history codes become no/yes, `dia` and the five flags 0/1 no/yes (CLEAN-12); Killip class is an ordered category (CLEAN-14); the target `day30` becomes `death_by_day_30` (Yes/No, CLEAN-25).
- Time basis: UnseenGroup: a risk model at presentation is used at hospitals and in regions other than the ones it was built in, and the case study on this file validates the model built on the US patients on the patients of the other countries (Steyerberg and Vergouwe 2014), so whole regions are held out (16 regions). The patients were enrolled one by one in 1990-1993, but the file records no date and no enrolment order (its rows are sorted by age), so a later period at a known region is not tested, nor are later patients at all: the care of the thrombolysis era has changed since.

## Splits

Whole regions in 8 folds, one repeat (leaf L-PLACE.groups; Andrej, 2026-11-25): each of the 16 regions is held out once, two regions per test fold, US and non-US mixed, assigned by the framework's grouped k-fold stratified by the outcome with shuffled regions and its fixed seed; each split trains on the other 14 regions. The test folds hold 4,161 to 7,789 patients and 256 to 554 deaths. One repeat of 8 folds was chosen over the protocol's 3 repeats of 3 folds, as for economic_well_being_prediction_challenge: folds of 5 or 6 regions train on 10 or 11 regions, and the repeats share most of their training regions. Measured (2026-11-25, `height` dropped, 6 draws of each design, mean ROC AUC over the folds; reference: each region held out alone): the reference gives logistic regression 0.8189, logistic regression with splines 0.8248 and lightly tuned LightGBM 0.8256, a gap of 0.0067 between LightGBM and logistic regression; 1 x 8 keeps that gap (0.0067, SD of the design's mean over draws 0.0010), 3 x 3 shrinks it to 0.0056 (SD 0.0003) and swaps the two best models by 0.0002. The file records no hospital; its finer codes (`grpl`, `grps`) are groups of hospitals cut to a minimum number of deaths for validation studies and are not used. The case study's own split (US against non-US) is two groups, too few for repeated folds; its transfer scores 0.815 to 0.820 ROC AUC (LightGBM and logistic regression, both directions), inside the range of the region folds, so the mixed folds lose nothing the source tested.

1 repeat(s) x 8 fold(s) with seed 4267; train 33,037 to 36,665 rows, test 4,161 to 7,789 rows.

| repeat | fold | n_train | n_test |
|---|---|---|---|
| 0 | 0 | 35844 | 4982 |
| 0 | 1 | 36472 | 4354 |
| 0 | 2 | 36341 | 4485 |
| 0 | 3 | 33037 | 7789 |
| 0 | 4 | 35419 | 5407 |
| 0 | 5 | 36665 | 4161 |
| 0 | 6 | 36237 | 4589 |
| 0 | 7 | 35767 | 5059 |

## Group structure

One group is one of the file's 16 regions (8 in the US, 8 in the other countries; 1,231 to 4,352 patients each). A risk model at presentation is used at hospitals other than those it was built at, and the case study on this file builds its model on the US patients and validates it on the patients outside the US: "We validate these models in patients enrolled outside of the USA (n = 17 796, 1286 deaths)" (Steyerberg and Vergouwe 2014). Holding out whole regions generalises that design. Each patient is one prediction, made from their own data alone. Every region is tested once, in 8 folds of 2 regions.

| field | value |
|---|---|
| group column | `region` |
| labels | per_sample |
| order inside a group | none |
| prediction unit | row |
| known about a group when predicting | none |

| statistic | value |
|---|---|
| groups | 16 |
| rows per group (min / median / max) | 1,231 / 2,533.5 / 4,352 |
| largest group | 10.7% of the rows |
| test groups per fold | 2 |
| groups of two or more rows with a single label | 0.0% |
| nearest neighbour in the same group | 7.5% of the rows (chance: 6.8%) |
| label variance explained by the group | 0.00 (shuffled groups: 0.00) |

The nearest neighbour is computed on the standardised numeric features of a sample of up to 20,000 rows; chance is the share expected if the groups were unrelated to the features. The model-based diagnostics run with `.claude/skills/knowledge-data-foundry/scripts/group_probes.py`.

## Decisions

### 1. Time to relief of chest pain dropped: the randomised treatment changes it

Randomisation balances what is known at enrolment across the arms; `ttr` alone differs, lowest under accelerated tPA, the regimen that reperfuses fastest (chi-square p = 3e-11 against 0.09 to 0.97 for the other inputs). So it is recorded after the thrombolytic was given, not at presentation. Share of patients with the flag, % by arm:

| index | SK | SK+tPA | tPA |
|---|---|---|---|
| ttr (time to relief of chest pain > 1 h) | 66.3 | 64.6 | 62.3 |
| dia (diabetes) | 15.1 | 14.2 | 14.5 |
| sho (Killip III or IV) | 2.1 | 2.1 | 2.1 |
| hig (anterior infarct or previous MI) | 48.8 | 49 | 48.9 |
| htn (history of hypertension) | 38.1 | 37.6 | 38.2 |
| pan (previous angina) | 36.9 | 36.3 | 37.7 |
| pmi (previous MI) | 16.5 | 16.2 | 16.8 |

### 2. Height dropped: its filled-in values mark patients who died

The source filled missing predictor values by a single imputation. Heights that are neither whole or half centimetres nor a converted inch value are the fills; their patients died far more often, in nearly every region and given everything known at presentation (odds ratio 2.65), and setting them to missing or rounding them keeps the signal. Weights of the same look do not differ. Patients (the 40,826 that stay) and the share who died by day 30, %:

| height | patients | died_pct |
|---|---|---|
| filled (fraction off the grid) | 2132 | 19.9 |
| measured | 38694 | 6.3 |

## Bundle checks

0 error(s), 0 warning(s), 3 info (28 checks run, plus the dataset's own checks).

- **info** `dataset_duplicate_rows`: 8 exact duplicate row(s) (0.0% of the data). (hint: Duplicates spread across train and test inflate scores — deduplicate unless the repetition is meaningful.)
- **info** `dataset_conflicting_duplicate_rows`: 2 row(s) (0.0%) share all features with another row but carry a different target. (hint: Either the rows differ in a dropped column, or the label is noisy — this caps the achievable score.)
- **info** `groups_not_clustered`: Rows are no closer to their own group than chance (7.5% of nearest neighbours vs 6.8%), and the group explains no more of the label than shuffled groups (0.00 vs 0.00). (hint: The grouping may not be needed: compare IID and grouped scores with `.claude/skills/knowledge-data-foundry/scripts/group_probes.py`.)

Accepted on purpose:

- `groups_test_groups_few`: Accepted (Andrej, 2026-11-25): a test region stands for the patients of a region the model has never seen, so two whole regions per test fold is the task (8 folds, each of the 16 regions tested once; 4,161 to 7,789 patients and 256 to 554 deaths per test fold). The signal across regions is real: the group probe scores ROC AUC 0.824 (logistic regression), 0.814 (random forest) and 0.821 (LightGBM) on the held-out regions, and LightGBM 0.821 grouped against 0.819 on random folds (2026-11-25).
- `splits_dimensions_off_protocol`: Accepted (Andrej, 2026-11-25): 1 x 8 region folds instead of the protocol's 3 x 3. Over 6 draws each (`height` dropped, mean ROC AUC over the folds), 1 x 8 keeps the gap of lightly tuned LightGBM over logistic regression that holding out each region alone shows (0.0067 against 0.0067), while 3 x 3, which trains on 10 or 11 of the 16 regions, shrinks it to 0.0056; the splits comment says why.

## Data checks

### Feature summary

<details>
<summary>Show the table (24 rows)</summary>

| index | dtype | n_missing | pct_missing | n_unique | examples |
|---|---|---|---|---|---|
| death_by_day_30 | category | 0 | 0 | 2 | No, Yes |
| sho | category | 0 | 0 | 2 | no, yes |
| hig | category | 0 | 0 | 2 | no, yes |
| dia | category | 0 | 0 | 2 | no, yes |
| hyp | category | 0 | 0 | 2 | no, yes |
| hrt | category | 0 | 0 | 2 | no, yes |
| sex | category | 0 | 0 | 2 | male, female |
| Killip | category | 0 | 0 | 4 | I, II, III, IV |
| ant | category | 0 | 0 | 2 | no, yes |
| miloc | category | 0 | 0 | 3 | Inferior, Anterior, Other |
| pmi | category | 0 | 0 | 2 | no, yes |
| htn | category | 0 | 0 | 2 | no, yes |
| smk | category | 0 | 0 | 3 | never, current, quit |
| pan | category | 0 | 0 | 2 | no, yes |
| fam | category | 0 | 0 | 2 | no, yes |
| prevcvd | category | 0 | 0 | 2 | no, yes |
| prevcabg | category | 0 | 0 | 2 | no, yes |
| region | category | 0 | 0 | 16 | 12, 14, 7, 9, 2, 8, 4, 15, 11, 13 |
| tx | category | 0 | 0 | 3 | SK, tPA, SK+tPA |
| pulse | float64 | 6 | 0.01 | 162 | 60.0, 80.0, 70.0, 72.0, 68.0, 90.0, 64.0, 76.0, 75.0, 62.0 |
| age | float64 | 0 | 0 | 5575 | 66.938, 69.391, 68.797, 66.359, 64.438, 72.047, 70.422, 69.5, 71.766, 70.094 |
| sysbp | float64 | 1 | 0 | 209 | 120.0, 130.0, 140.0, 110.0, 150.0, 160.0, 100.0, 170.0, 125.0, 135.0 |
| weight | float64 | 0 | 0 | 658 | 70.0, 80.0, 75.0, 82.0, 73.0, 90.0, 68.0, 84.0, 77.0, 85.0 |
| ste | int64 | 0 | 0 | 12 | 3, 4, 5, 2, 6, 7, 1, 8, 0, 9 |

</details>

### Target distribution

| death_by_day_30 | count | pct |
|---|---|---|
| No | 37975 | 93.02 |
| Yes | 2851 | 6.98 |

### Numeric features

| index | count | mean | std | min | max |
|---|---|---|---|---|---|
| age | 40826 | 60.9037 | 11.9388 | 19.027 | 110 |
| ste | 40826 | 4.10065 | 1.89634 | 0 | 11 |
| pulse | 40820 | 75.4247 | 17.8169 | 0 | 246 |
| sysbp | 40825 | 128.984 | 23.8857 | 0 | 280 |
| weight | 40826 | 79.3799 | 15.7344 | 36 | 213 |

### Categorical features

<details>
<summary>Show the table (46 rows)</summary>

| column | rank | value | count | pct |
|---|---|---|---|---|
| Killip | 1 | I | 34821 | 85.29 |
| Killip | 2 | II | 5141 | 12.59 |
| Killip | 3 | III | 551 | 1.35 |
| Killip | 4 | IV | 313 | 0.77 |
| ant | 1 | no | 24926 | 61.05 |
| ant | 2 | yes | 15900 | 38.95 |
| death_by_day_30 | 1 | No | 37975 | 93.02 |
| death_by_day_30 | 2 | Yes | 2851 | 6.98 |
| dia | 1 | no | 34821 | 85.29 |
| dia | 2 | yes | 6005 | 14.71 |
| fam | 1 | no | 23501 | 57.56 |
| fam | 2 | yes | 17325 | 42.44 |
| hig | 1 | no | 20861 | 51.1 |
| hig | 2 | yes | 19965 | 48.9 |
| hrt | 1 | no | 27432 | 67.19 |
| hrt | 2 | yes | 13394 | 32.81 |
| htn | 1 | no | 25306 | 61.99 |
| htn | 2 | yes | 15520 | 38.01 |
| hyp | 1 | no | 37448 | 91.73 |
| hyp | 2 | yes | 3378 | 8.27 |
| miloc | 1 | Inferior | 23491 | 57.54 |
| miloc | 2 | Anterior | 15900 | 38.95 |
| miloc | 3 | Other | 1435 | 3.51 |
| pan | 1 | no | 25739 | 63.05 |
| pan | 2 | yes | 15087 | 36.95 |
| pmi | 1 | no | 34100 | 83.53 |
| pmi | 2 | yes | 6726 | 16.47 |
| prevcabg | 1 | no | 39031 | 95.6 |
| prevcabg | 2 | yes | 1795 | 4.4 |
| prevcvd | 1 | no | 39994 | 97.96 |
| prevcvd | 2 | yes | 832 | 2.04 |
| region | 1 | 12 | 4352 | 10.66 |
| region | 2 | 14 | 3437 | 8.42 |
| region | 3 | 7 | 3150 | 7.72 |
| region | 4 | 9 | 3123 | 7.65 |
| region | 5 | 2 | 2952 | 7.23 |
| sex | 1 | male | 30548 | 74.82 |
| sex | 2 | female | 10278 | 25.18 |
| sho | 1 | no | 39962 | 97.88 |
| sho | 2 | yes | 864 | 2.12 |
| smk | 1 | never | 17539 | 42.96 |
| smk | 2 | current | 12077 | 29.58 |
| smk | 3 | quit | 11210 | 27.46 |
| tx | 1 | SK | 20160 | 49.38 |
| tx | 2 | tPA | 10347 | 25.34 |
| tx | 3 | SK+tPA | 10319 | 25.28 |

</details>

## Build

Not built yet. `dataset build` saves the container to the warehouse and records its UUID, checksum and provenance here.
