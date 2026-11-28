---
report_format: data-foundry-report-v2
unique_name: fremtpl2
container_format: 2
checksum: v2:f24fc5f06954b6a12cc6abc6849534b336131dc829dabe528697fc2c772bc826
build:
  uuid: 01a217ff-2459-7f5a-826b-f258d60038dc
  checksum: v2:f24fc5f06954b6a12cc6abc6849534b336131dc829dabe528697fc2c772bc826
  built_at: '2026-11-26T13:15:43+00:00'
  path: fremtpl2/01a217ff-2459-7f5a-826b-f258d60038dc
  data_foundry_version: 0.0.5
  git_sha: e3ddd55462cc45eed6aa71c38abd183086888b36
  libraries:
    python: 3.12.3
    pandas: 2.3.3
    numpy: 2.1.3
    pyarrow: 20.0.0
    scikit-learn: 1.7.2
    polars: 1.41.1
build_stale: false
data:
  n_rows: 677991
  n_features: 9
  dtypes:
    category: 4
    float64: 5
    int64: 3
  n_test_dataset_rows: null
task:
  target: claim_frequency
  problem_type: regression
  metric: mean_poisson_deviance
  metric_origin: source
  scoring_columns:
  - Exposure
  sample_weight: Exposure
  split_regime: temporal_non_iid
  stratify_on: null
  time_on: idpol_block
  time_of: label
  group_on: null
  group_labels: null
  group_time_on: null
  grouping: null
splits:
  n_repeats: 3
  n_folds: 1
  random_state: 4267
  time_horizon: 1
  time_horizon_unit: steps
  time_gap: null
  time_gap_unit: null
  reason: 'Three windows on the IDpol blocks (Andrej, 2026-11-20): block 6, 5 and
    4 are tested, each

    trained on all earlier blocks (split 0: train blocks 0-5, 640,557 rows or 94.5%,
    test 37,434; split 1: train

    0-4, 597,998 or 93.4%, test 42,559; split 2: train 0-3, 488,801 or 81.7%, test
    109,197). The release has no

    dates: `idpol_block` (IDpol // 1,000,000) is read as a period because renewals
    link each block to the next

    (next_year_rows; the curation notes give the counts and the caveats: blocks 0-1,
    2-3 and 4-6 look like three

    sub-portfolios), so the periods are inferred, not dated, and the order is a judgement
    call. A window stands for

    the portfolio of a later period priced from the earlier ones. No gap: a period''s
    claims are known at its end,

    and the blocks are inferred periods, with no finer time to leave a gap in. Three
    windows meet the target of

    three for 677,991 rows (SPLIT-33), and the oldest train side is above half the
    rows. The random folds shipped

    before are replaced because the stationary-relation test reads not flat (LightGBM
    weighted Poisson deviance gap

    +0.0003 ± 0.0001 on block 4, +0.0014 ± 0.0006 on block 5, inconclusive on block
    6, floor 0.0001; flat or

    inconclusive inside the sub-portfolios); on the same rows at the same training
    size, windows scored 0.0009 to

    0.0038 worse than random folds. Under random folds 16% of test rows had the policy''s
    next-year record on the

    training side; here a policy''s later record never trains. The 19 rows of the
    high-count profile (blocks 2-3)

    only train.'
  n_train:
    min: 488801
    max: 640557
  n_test:
    min: 37434
    max: 109197
bundle_checks:
  ok: true
  errors: []
  warnings: []
  infos: []
  accepted:
    dataset_duplicate_rows: 'Accepted (Lennart, 2026-11-04); counts of 2026-11-06
      on the 9 rating factors: 181,197 rows (26.7%) copy an earlier row with the same
      target, and 327,862 sit in 138,537 groups of identical factors, 92.9% of which
      sum to at most 1.01 years, so most groups look like one policy-year split into
      records (each with its own IDpol) rather than distinct policies. The harm is
      at the folds'' noise of about 0.0006: a memorizer of training twins gains +0.0001,
      the group''s size and the other records'' exposure +0.0004, the count of identical
      rows over train and test +0.0005; the one exception is the profile of the high
      counts (notes).'
    dataset_conflicting_duplicate_rows: 'Accepted (Lennart, 2026-11-04); counts of
      2026-11-06: 8,128 rows (1.2%) share every rating factor with another row but
      differ in the target, 7,971 of them in the claim count: claims are rare, random
      events of identical risk profiles, not noise.'
    task_target_value_dominant: '96% of the policies have no claim: real no-claim
      policies, the nature of claim frequency.'
    splits_feature_missing_in_test: 'Accepted (Andrej, 2026-11-20): the block-5 window
      trains on IDpol blocks 0-4, where `BonusMalus` is blanked (recorded after the
      year''s own claims there), and tests on block 5, where it is a start-of-year
      value; a pricing model meets a factor once it starts being recorded, and block
      6''s window learns it from block 5. Measured: most of block 5''s stationarity
      gap is this column (+0.0014 with it, +0.0005 without).'
    task_time_on_few_unique: 'Accepted (Andrej, 2026-11-20): the split is ordered
      by the seven IDpol blocks, the only time key the release holds (no dates); each
      window tests one whole block.'
decisions:
- Windows on the IDpol blocks, read as consecutive periods
---

# fremtpl2

> Generated from [`dataset.py`](dataset.py) by `dataset check` (or `build`). Do not edit this page: change `dataset.py` and re-run the check.

Regression of `claim_frequency`, scored with `mean_poisson_deviance` on temporal splits by `idpol_block`. 677,991 rows and 9 features. Source: Other (2014).

Built as `01a217ff-2459-7f5a-826b-f258d60038dc` on 2026-11-26. See [Build](#build).

## In brief

**Question.** How many claims per year insured will a French motor-insurance policy make?

**Use case.** For example, a pricing actuary sets the yearly premium of motor third-party liability policies at the quote, estimating each policy's expected claims per year insured from its rating factors.

**One row.** One of 677,991 policy records of an unnamed French insurer's motor portfolio, each observed mostly within one accounting year, about 2011 to 2013.

**Predicted.** Claims per year insured: the claims with a recorded cost in the record's period divided by the time it was insured (96.3% have none). Each record counts in proportion to that time, in training and scoring.

**Known at prediction time.** The car's power, age, brand and fuel, the driver's age, the bonus-malus level (in 12% of the records only: blank in the rest, where it looks recorded after the year's own claims), and the density, area and region of residence.

**Known only when scoring.** How long each record was insured, recorded with its claims. A claim can cut it short, so it is no input: it is the rate's denominator and each record's weight in training and scoring.

**What the test data stands for.** Three windows, the last three of the seven policy-number blocks, each trained on all earlier blocks, so the test data stands for the portfolio of a later period. The release has no dates: the blocks are read as consecutive periods from renewals that link them, an inferred order, not a dated one.

**Our changes to the source.** We divide the claim count by the time insured and weight each record by that time, as the source's models do with an offset. We blank the bonus-malus level in the first five policy-number ranges (88% of the records), where it looks recorded after the year's own claims, and set default codes of car age (99, 100) and driver age (99, in the first range) to missing.

> **Use case fit: approximate (a stand-in with a known gap).** Rating factors and claim frequency mirror pricing, and later periods are held out, but the periods are inferred from policy-number blocks, not dated; the insurer is unknown. The bonus-malus level, the tariff's main factor, is blank in 88% of records; a model removes about 2% of a constant rate's error (6% before the blanking), so strong methods differ in the fourth decimal.

## Files in this folder

| file | what it is |
|---|---|
| [`dataset.py`](dataset.py) | The definition, and the only file edited by hand: metadata, reading and cleaning the raw files, feature types and splits. |
| [`README.md`](README.md) | This page, generated by `dataset check` and `dataset build`. |

- The curation record, with the triage decision, its sources and the review: [`curation/records/fremtpl2.md`](../../../../curation/records/fremtpl2.md)
- The original source: <https://dutangc.github.io/CASdatasets/reference/freMTPL.html>
- The collection this folder belongs to: [`tabarena-v0pt2/README.md`](../README.md) and [`tabarena-v0pt2/CHANGELOG.md`](../CHANGELOG.md)

## Rebuild

`dataset.py` reads its raw files from `local-data-warehouse/fremtpl2/`. To get them:

```text
Download the two tables of the CASdatasets R package (Dutang and Charpentier) at a pinned commit of its
GitHub repository. Install rdata==1.1.0 and its dependencies in the environment used to run this definition.
mkdir -p "${DATA_FOUNDRY_WAREHOUSE:-local-data-warehouse}/fremtpl2"
curl -L --fail https://raw.githubusercontent.com/dutangc/CASdatasets/227fb56b8734bdb7c0327a41180e01d2ddaeaf26/data/freMTPL2freq.rda -o "${DATA_FOUNDRY_WAREHOUSE:-local-data-warehouse}/fremtpl2/freMTPL2freq.rda"
curl -L --fail https://raw.githubusercontent.com/dutangc/CASdatasets/227fb56b8734bdb7c0327a41180e01d2ddaeaf26/data/freMTPL2sev.rda -o "${DATA_FOUNDRY_WAREHOUSE:-local-data-warehouse}/fremtpl2/freMTPL2sev.rda"
Expected SHA-256: freMTPL2freq.rda 82c8598513d9fa78226b6c7d271a9940eca4b8083e9e32320a75d377bdfe15a3,
freMTPL2sev.rda 78e6e5016ae046603b37e88ff8ad8ca327f5d59f827c1f75d140388de09b14b3.
OpenML 41214 and 41215 are copies of the older CASdatasets 1.0-8 (2018), before the package's update of
June 2022: 678,013 policies whose claim counts do not all match the claims table, so they are not this data.
From the repository root, set DATA_FOUNDRY_DATASETS_ROOT=datasets/_dev/tabarena-v0pt2.
```

Then, from the repository root:

```bash
.venv/bin/python -m data_foundry.curation.cli dataset check datasets/_dev/tabarena-v0pt2/fremtpl2   # pipeline and checks, no UUID; rewrites this page
.venv/bin/python -m data_foundry.curation.cli dataset build datasets/_dev/tabarena-v0pt2/fremtpl2   # also saves the container and records its UUID
```

Only curators run `build`, when the dataset ships.

## Dataset and task

| field | value |
|---|---|
| source | Other: https://dutangc.github.io/CASdatasets/reference/freMTPL.html |
| year | 2014 |
| domain | insurance |
| license | GPL (>= 2), declared by CASdatasets; the insurer's terms not stated |
| data_tags | Non-IID, Temporal, Spatial |
| reference | DutangCharpentierCASdatasets,NollSalzmannWuthrich2018 |
| rows x columns | 677,991 x 12 |
| task.target | claim_frequency |
| task.problem_type | regression |
| task.metric | mean_poisson_deviance |
| task.sample_weight | Exposure |
| task.split_regime | temporal_non_iid |
| task.time_on | idpol_block |
| task.time_of | label |

**Metric**

| field | value |
|---|---|
| name | `mean_poisson_deviance` (standard; takes value; lower is better) |
| origin | source: the source's metric |
| original | Poisson deviance loss of the claim counts against the expected counts, in and out of sample (reported as 100 times the mean) |
| reference | https://github.com/JSchelldorfer/ActuarialDataScience/blob/3f761ef830d28c14dda5443d504d192069a64ca3/1%20-%20French%20Motor%20Third-Party%20Liability%20Claims/Tools/FreMTPL_1b%20load%20data.r#L35 |
| definition | 2*sum(w*(y*log(y/mu)-y+mu))/sum(w) over the claims per year y and the predicted rates mu, w = Exposure (years insured); 0*log(0/mu)=0; mu below 1e-4 claims per year counts as 1e-4. For mu above the floor it equals the source's mean count deviance of the expected counts Exposure*mu times n/sum(Exposure) of the scored rows (1.741 to 2.803 on the three test windows); the case study's Poisson.Deviance is 100 times the count deviance |
| params | {'min_prediction': 0.0001} |
| inputs | weight: `Exposure` |

**Scoring columns**

Kept in the frame for the metric; do not use them as features. Drop them from the inputs (`feature_columns(container)`), then pass the test rows' values to the scorer (`data_foundry.metrics.scorer(container)(y_test, y_pred, test_idx)`).

| column | role | how the metric uses it | model input |
|---|---|---|---|
| `Exposure` | weight | mean_poisson_deviance: years insured in the record's period (1/366 to 2.01), realized: shorter when the policy ended early, often after a claim; in IDpol blocks 5-6 mostly cut at a calendar date (block 6 never exceeds 0.74 of a year, 99.8% of block 5 is a partial year). The claim frequency's denominator; each row's weight in the metric and in training; never a feature | training weight; never a feature |

The test-row values of `Exposure` are for the scorer only: never read them when predicting a test row.

**Training weight**

Fit every model with `Exposure` as each row's sample weight (`sample_weight(container)` from `data_foundry.curation_container`), and never use it as a feature. The metric weights the test rows by the same column, so a model fitted without it targets another quantity.

<details>
<summary>Feature types: 3 categorical, 1 ordinal, 0 string, 0 datetime</summary>

- categorical (3): `VehBrand`, `VehGas`, `Region`
- ordinal (1): `Area (A < B < C < D < E < F)`
- string (0): none
- datetime (0): none

</details>

<details>
<summary>BibTeX</summary>

```bibtex
@manual{DutangCharpentierCASdatasets,
  author = {Dutang, Christophe and Charpentier, Arthur},
  title = {{CASdatasets}: Insurance Datasets},
  year = {2026},
  note = {R package version 1.2-1, GitHub commit 227fb56b8734bdb7c0327a41180e01d2ddaeaf26; freMTPL2freq and freMTPL2sev entered on 14 October 2014},
  doi = {10.57745/P0KHAG},
  url = {https://github.com/dutangc/CASdatasets}
}
@misc{NollSalzmannWuthrich2018,
  author = {Noll, Alexander and Salzmann, Robert and W{\"u}thrich, Mario V.},
  title = {Case Study: {French} Motor Third-Party Liability Claims},
  year = {2018},
  howpublished = {SSRN},
  doi = {10.2139/ssrn.3164764},
  note = {Code: https://github.com/JSchelldorfer/ActuarialDataScience, folder 1}
}
```

</details>

## Sample rows

The first 5 of 677,991 rows of the final frame (the oldest rows: the frame is sorted by `idpol_block`). Cells are cut at 40 characters.

| claim_frequency | Exposure | VehPower | VehAge | DrivAge | BonusMalus | VehBrand | VehGas | Area | Density | Region | idpol_block |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0.05 | 7 | 13 | 24 | nan | B2 | Regular | C | 222 | Centre | 0 |
| 0 | 0.68 | 7 | 18 | 29 | nan | B1 | Regular | D | 1214 | Rhone-Alpes | 0 |
| 0 | 1 | 5 | 7 | 34 | nan | B4 | Diesel | D | 776 | Lorraine | 0 |
| 0 | 0.28 | 4 | 9 | 32 | nan | B4 | Diesel | B | 59 | Rhone-Alpes | 0 |
| 0 | 1 | 6 | 2 | 69 | nan | B2 | Diesel | D | 1535 | Aquitaine | 0 |

## Curation notes

We start with data/freMTPL2freq.rda (677,991 policies) and data/freMTPL2sev.rda (26,444 claims) from CASdatasets commit 227fb56b8734bdb7c0327a41180e01d2ddaeaf26, joined on IDpol, the link the help page names.

- Prediction point: the quotation of the policy for the accounting year, from the rating factors the help page lists; the source gives no dates ("observed mostly on one year", "approximately 2011-2013").
- Target: claim_frequency = ClaimNb / Exposure, the claims per year insured (MET-14), with Exposure as the row weight of the metric and the training weight (`sample_weight`, MET-15) and never a feature (LEAK-41). A fit without the weight scores worse than the weighted constant rate (LightGBM 0.50043 against 0.47980 on fold 0, the book priced 1.56 times too high), so a method must take the training weight, and results say whether it did. ClaimNb leaves the frame as a part of the target, and _clean checks that claim_frequency x Exposure gives it back. The counts are as released (0 to 16). CASdatasets' update of 23 June 2022 set each count to the policy's claims in freMTPL2sev, as Wüthrich and Merz (2023, Appendix B, Sec. 13.1) do by hand: the old counts of the first policies "do not seem to be correct because these claims do not have claim severity counterparts". _clean checks that every count equals the claims table and that no claim names a missing policy. Those first 9,387 policies (IDpol up to 24,951) all had claims before (9,942), 293 have now, and they stay: their next-year rows claim at 0.048 a year against 0.076 for the rest of block 0.
- Not capped: the 8 policies with 5 to 16 claims (Noll et al.'s code caps at 4, "that might be data error", FreMTPL_1b load data.r line 30; Wüthrich and Merz drop them as "may be data error", Sec. 13.1) each have as many claims with a cost. Exposure above one year (1,224 rows, up to 2.01, IDpol blocks 1 and 2 only), capped at 1 by both, stays: the help page says only "mostly on one year", so it is unusual, not shown impossible (CLEAN-11).
- Counts of 5 to 16 (Lennart, 2026-11-04: kept): seven of the eight policies, 66 claims over 1.38 years, every claim with a positive cost, belong to one profile, the same car and driver a year apart (power 4, brand B1, area D, density 824, Languedoc-Roussillon, bonus-malus 50 before the blanking; car and driver aged 12 and 52 in block 2, 13 and 53 in block 3), which Wüthrich and Merz suspect to be one driver or a rental fleet: its 19 rows hold 72 claims over 3.63 years, 19.8 claims a year against the portfolio's 0.074. A cap is a modelling choice of the literature, not a shown error, and the 2022 update ties each count to a costed claim; the 19 rows carry 0.0023 of the constant rate's declared score 0.4793 (0.0012 of 0.2534 on the count). They fall 6/7/6 into the three test folds, and LightGBM predicts 3.8 to 17.2 claims a year for them from their copies on the training side (0.073 to 0.078 with the folds grouped on identical rating factors): this makes 94-102% of the 0.0007 to 0.0017 by which the random split scores better than the grouped one, which is -0.0002 to +0.00015 without these rows (7 runs of 3 folds). Under the block windows of 2026-11-20 the profile's rows (15 in block 2, 4 in block 3) only train.
- Exposure above one year (Lennart, 2026-11-04: kept): 1,224 rows of 1.01 to 2.01 years (median 1.04) in two policy ranges, IDpol 1,179,653-1,199,005 (961 rows) and the end of block 2 (263), which record a whole contract period rather than cutting at the accounting year and have no links to other years. The literature caps at 1 on the assumption that every policy lies inside one year, which these rows contradict; capping would raise their modelled rate by 11% on average. Exposure is the time at risk; these rows keep weights of up to 2.01.
- Exposure (LEAK-41, MET-15; resolved 2026-11-06): the share of the year insured is shorter when the policy ended during the year, often after a claim, so as a free feature it recorded the outcome. On the count target, beyond a log(Exposure) offset it was worth another 0.0039 to 0.0045 of mean deviance (0.0033 to 0.0047 after the BonusMalus blanking, 3 folds), a Poisson GLM gave log(Exposure) a coefficient of 0.641 where an offset is 1, and at the quote (every policy priced for a full year) the free model was never better than the offset model while actual claims came in 1.29 times its price. On the declared metric (LightGBM fitted with the weight, the 3 random folds shipped then) Exposure as a feature gains +0.0082 with a Poisson fit (0.0086 / 0.0087 / 0.0073 per fold, 43% of what that model gains over the constant rate) and +0.0075 with an L2 fit, and in probe 22 (50,000 rows a side, 3 folds x 3 seeds) +0.0048 and +0.0067; the worse of the two decides, and the column is out either way. The weight alone, reported next to that gain and no ceiling (LEAK-41 as reworded on 2026-11-08): a rate fitted on Exposure alone scores 0.47114 against the constant rate's 0.47929, and 1/Exposure as the prediction about 3.65, worse than the constant. The rating factors predict Exposure at R^2 0.17 (probe 22), and no feature's gain runs through it above 2 SD in either fit; the highest, Region and DrivAge (1.1 to 1.4 SD), are known at the quote and stay (USE-6). Exposure now ships as the rate's denominator and each row's weight, the source's offset model: with the weight, dividing does not inflate short records. Part of the short records are renewals during the year recorded as two records (Wüthrich and Merz, Sec. 13.1).
- Metric: the mean Poisson deviance of the claim frequency weighted by Exposure, sum(w*d)/sum(w). For predictions above the floor it equals the mean Poisson deviance of ClaimNb against the expected count Exposure x rate, by which Noll, Salzmann and Wüthrich compare models in and out of sample (FreMTPL_1b load data.r line 35, 100 times the mean) and Wüthrich and Merz's out-of-sample loss (Sec. 5.2.4), times n/sum(Exposure) of the scored rows (1.741, 2.647 and 2.803 on the test windows of blocks 4, 5 and 6, 1.891 overall; 1.886 to 1.896 on the random folds shipped before): the source's metric on its offset model, so models rank as by the source's metric on every window (MET-11, origin source). Floor 1e-4 claims per year on the predicted rate, two orders below the smallest plausible rate (MET-13, Lennart's rule of 2026-11-04 on the scale the metric scores). Deviances measured before 2026-11-06 (in the CC lines, and where these notes say "on the count target") are on the claim count with Exposure a feature; the declared score is about 1.891 times the count deviance.
- One task, the claims per year insured (2026-11-08; closes D12 of 2026-11-06): the claim cost per year insured was measured as the alternative and is not created as a second dataset of the same policies. Built from freMTPL2sev (ClaimAmount summed per IDpol, over Exposure, weighted by Exposure), its join is clean: 26,444 claims on 24,944 policies, each count equal to its policy's claims with an amount, no amount without a claim, amounts of 1 to 4,075,401 EUR (42.3% at the five IRSA-IDA flat amounts). The tail is real, not a data error (CLEAN-11): French motor liability covers bodily injury without a limit (Code des assurances, R211-7); the largest claim is 6.8% of all claim amounts and 18 to 19% of the test fold it falls in (19.3% of the first shipped fold), and the three largest (4.08M, 1.40M and 1.30M EUR) came from drivers aged 18 to 20. On 9 random splits (the 3 random folds shipped then and two more partitions of the same rows), five honest models fitted with the weight: on the claims per year the best LightGBM removes 2.26% of the constant rate's deviance (SD 0.18%, 9 of 9) and the GLM 1.79%, a regularised LightGBM beats the GLM on 9 of 9 by 0.32% (split SD 0.03%, bootstrap SE within a test fold 0.08%), and the five models keep their order (Kendall's W 0.89). On the cost per year the weighted Gini is 0.23 to 0.27 (split SD 0.07 to 0.09): the GLM and the regularised LightGBM score 0.34 to 0.40 on the three test folds that hold the 4.08M claim and 0.13 to 0.27 on the other six, the GLM leads by +0.011 (7 of 9, bootstrap SE within a fold 0.021), W 0.43; the weighted Tweedie deviance at power 1.5 (floor 0.1 EUR) gives the GLM 5.4% of the constant's (SD 4.4%, -0.3% to 11.5%). The rating factors predict no claim size beyond the tail: a gamma GLM gains 5.8% (SD 8.5%) over the mean claim as released and -0.8% (above 0 on 3 of 9) with claims capped at 200,000 EUR, and the frequency LightGBM times the mean claim ranks the cost per year better (Gini 0.29) than any model fitted on it (0.23 to 0.27). The insurer prices the cost per year, from a frequency and a severity model (USE-5); on this table the rating part of that price is the frequency's, which the source scores (MET-11), while a score of the cost follows where a few claims land.
- Dtypes: Area ordered A (rural) to F (urban centre) as the help page defines it, bands of Density; VehBrand, VehGas and Region (22 regions before 2016) nominal; the rest numbers. IDpol dropped. A car age of 99 or 100 (48 rows) is a default date, as no car is 86 to 98 and the 14 of the 23 aged 99 that next_year_rows pairs are all 100 a year later: missing (CLEAN-10). Anomaly: a driver age of 99 has 70 rows against 5 at 98, kept as possible (superseded 2026-11-05: the 66 in block 0 are missing, CC below); 66 of them are in block 0, after 1 row at 96 and none at 97-98, and none of the 66 has a next-year row (62.7% of block 0 has one).
- Copies kept: every IDpol is distinct, yet on the 9 rating factors 327,862 rows (48.4%) sit in 138,537 groups of identical rows and 181,197 copy an earlier row with the same target; 92.9% of these groups sum to at most 1.01 years, so most look like one policy-year split into records. Neighbouring IDpols often share all rating factors, and about half the rows of blocks 1, 3, 5 and 6 (48.7%, 48.3%, 49.2%, 60.3%) repeat a car of the block before with the driver a year older (decision table: 161,883 pairs, against 16 to 75 under shuffled or shifted controls), with no key the source states. These shares are lower bounds: a wider IDpol offset finds up to 75.3% in block 6. Chaining these pairs with neighbouring IDpols that share every rating factor gives 430,298 groups; on the count target, grouping on them moved LightGBM skill over the portfolio frequency from 0.0821 to 0.0819 (3 folds each). On the declared metric a model that scores one row at a time gains nothing from the copies outside the profile of the high counts (a memorizer of training twins +0.0001). A model that reads other rows could do more under the random folds shipped until 2026-11-20: for 16% of test rows the policy's next-year row was on the training side and the shipped columns single it out for 55% of linked rows (under the block windows a policy's later record never trains); flags of a previous or next record, read without labels, are worth about 0.0010, an oracle that also reads the linked row's claims, exposure and bonus-malus 0.0014 to 0.0025 (upper bounds: they read IDpol, which does not ship), and the count of identical rows over train and test +0.0005 (+0.00071 on the count target); the protocol line of LEAK-9 covers them.
- Split, windows on the IDpol blocks (Andrej, 2026-11-20): an insurer fits on past years and prices the next. `idpol_block` = IDpol // 1,000,000 (0 to 6) orders the rows and is no model input (`Temporal(..., time_of="label")`): a position in the release, not a date the insurer holds at the quote. The blocks are read as consecutive periods because the renewals of next_year_rows link each block to the next (46,445 to 57,212 one-to-one links from 0 to 1, 1 to 2, 2 to 3 and 3 to 4, 7,907 from 4 to 5, 10,470 from 5 to 6, under 300 between any other pair, 16 to 75 under shuffled or shifted controls); seven yearly steps do not fit the source's "approximately 2011-2013", so the periods are inferred, not dated, and only their order is used (SPLIT-22: nothing in the release is dated to check it against). Two caveats: from block 0 to 1 and 2 to 3 the bonus-malus barely moves (94.5% unchanged from 0 to 1, where the French system lowers it after every claim-free year), and in blocks 4-6 0.2% of linked rows cover a full year and 63-66% of linked pairs have exposures summing to at most 1.01, so blocks 0-1, 2-3 and 4-6 look like three sub-portfolios and the blocks may be accounting periods rather than years. This replaces the random 3-fold CV forced from temporal: the stationary-relation test on the blocks reads not flat (LightGBM weighted Poisson deviance of a model trained on all earlier blocks minus one trained on the tested block, 5 seeds, floor 0.0001: +0.0003 ± 0.0001 on block 4, +0.0014 ± 0.0006 on block 5, +0.0002 ± 0.0006 on block 6, inconclusive; inside the sub-portfolios flat or inconclusive), and on the same rows at the same training size a window scored 0.0009 to 0.0038 worse than the random folds (0.0009 to 0.0022 without the 19 rows of the high-count profile; inside one sub-portfolio -0.0021 to +0.0003), mostly a falling claim level (0.086 claims a year in block 0 to 0.059 in block 6). Under the random folds 16% of test rows had the policy's next-year record on the training side; under the windows a policy's later record never trains, and its earlier record is history the insurer holds. Recover the years if a release has them.
- Year 2014: the tables entered CASdatasets on 14 October 2014 (`pkg/inst/NEWS` at CASdatasets commit 324c15c999; the NEWS.md of the pinned commit does not list them); the first release holding them is not pinned. Source: "Unknown private insurer".
- CC (2026-11-05, Lennart): BonusMalus blanked in IDpol blocks 0-4 (597,998 rows, 88.2%), where it looks recorded after the row's own claims (LEAK-10, LEAK-7). There it is frozen from block 0 to 1 and 2 to 3 and claimants pile on the first malus step 62-63; in blocks 5-6 it follows the previous year's claims, as a start-of-year value does, and stays, as in zillow_prize, melbourne_housing_market and online_shoppers. bemtpl97 keeps its bm: its source says "The risk factors are registered at the start of the policy period" (binning manuscript, Sec. 2), the freMTPL2 help page says nothing of the kind, and the 2026-11-04 call that the two are treated alike covered the split and the fit. LightGBM Poisson, Exposure a free feature, the random folds shipped then (3): mean deviance 0.2327 before, 0.2435 after (+0.0127 in blocks 0-3, -0.0013 in blocks 5-6); dropping the column too costs 0.0009 more in blocks 5-6.
- CC (2026-11-05, Lennart): DrivAge 99 set to missing in block 0 (66 rows), a default code like VehAge 99 (CLEAN-10). None of the 66 has a next-year row, so the missing value marks the same rows the 99 did. The 4 rows at 99 outside block 0 stay at 99: next_year_rows pairs the one in block 3 with a block-2 row at 98, and two of the three in block 4 with block-5 rows at 100.
- CC (2026-11-05, Lennart): the label-free renewal signal stays: it is an evaluation leak, read from other rows, handled by LEAK-9 as amended on 2026-11-05 (a protocol line the benchmark checks; a method that learns from the test block is called out and not benchmarked), as medical_facility_operational_data. After the BonusMalus blanking a model that reads the next-year record gains 0.0008 mean deviance (0.0009-0.0010 without `BonusMalus`).
- CC (2026-11-06, Lennart): Exposure resolved: the target is the claims per year insured, Exposure the weight of the metric and of training and never a feature (LEAK-41, MET-14, MET-15), the floor 1e-4 a year (MET-13). Supersedes the call of 2026-10-20 (Andrej: Exposure "a feature, not a divisor", capped at 1) and the parking of 2026-11-05: the conditional measurement came later (+0.0040; never better at quotation), and with the weight, dividing does not inflate short records.
- CC (2026-11-06, Lennart): the claim amounts (decision D12 of the exposure study) stay out for now; a task on amounts per year insured or on the claim size is a separate decision, made on leak-free numbers.
- CC (2026-11-08, Lennart): on D12, the claim-amount task: "which task is more representative of the real use case? use that one and the other is not created as we dont want to have duplicates". One task ships, the claims per year insured as implemented, the AI's pick on the numbers of the bullet "One task" (for Lennart to confirm); the claim cost per year insured is not created. Closes his CC of 2026-11-06 that kept the amounts out "for now".

## Splits

Expanding-window temporal splits: 3 test window(s) of 1 time value, walking back from the newest data, newest first; train is all earlier data. The test windows by `idpol_block`, as listed: 6 (37,434 test, 640,557 train rows); 5 (42,559 test, 597,998 train rows); 4 (109,197 test, 488,801 train rows).

Three windows on the IDpol blocks (Andrej, 2026-11-20): block 6, 5 and 4 are tested, each
trained on all earlier blocks (split 0: train blocks 0-5, 640,557 rows or 94.5%, test 37,434; split 1: train
0-4, 597,998 or 93.4%, test 42,559; split 2: train 0-3, 488,801 or 81.7%, test 109,197). The release has no
dates: `idpol_block` (IDpol // 1,000,000) is read as a period because renewals link each block to the next
(next_year_rows; the curation notes give the counts and the caveats: blocks 0-1, 2-3 and 4-6 look like three
sub-portfolios), so the periods are inferred, not dated, and the order is a judgement call. A window stands for
the portfolio of a later period priced from the earlier ones. No gap: a period's claims are known at its end,
and the blocks are inferred periods, with no finer time to leave a gap in. Three windows meet the target of
three for 677,991 rows (SPLIT-33), and the oldest train side is above half the rows. The random folds shipped
before are replaced because the stationary-relation test reads not flat (LightGBM weighted Poisson deviance gap
+0.0003 ± 0.0001 on block 4, +0.0014 ± 0.0006 on block 5, inconclusive on block 6, floor 0.0001; flat or
inconclusive inside the sub-portfolios); on the same rows at the same training size, windows scored 0.0009 to
0.0038 worse than random folds. Under random folds 16% of test rows had the policy's next-year record on the
training side; here a policy's later record never trains. The 19 rows of the high-count profile (blocks 2-3)
only train.

3 repeat(s) x 1 fold(s) with seed 4267; train 488,801 to 640,557 rows, test 37,434 to 109,197 rows. Prediction horizon: 1 steps. The time column `idpol_block` dates the label, which arrives after the prediction point: it orders and splits the rows, so every training label was known at its window's start, and is no model input (`feature_columns(container)` leaves it out).

| repeat | fold | n_train | n_test | train_start | train_end | test_start | test_end |
|---|---|---|---|---|---|---|---|
| 0 | 0 | 640557 | 37434 | 0 | 5 | 6 | 6 |
| 1 | 0 | 597998 | 42559 | 0 | 4 | 5 | 5 |
| 2 | 0 | 488801 | 109197 | 0 | 3 | 4 | 4 |


### The test windows

Each test window against its train side, by statistics of the data, never of a model: the target, and the population stability index (PSI) of each feature, its largest value and the features that drift most (below 0.1 little shift, above 0.25 a large one), and the share of test rows with a category the train side never shows. Up to 20,000 rows per side. The candidates the windows were chosen from: `.venv/bin/python -m data_foundry.curation.cli dataset windows fremtpl2`.

| window | period | n_test | train_share | target_test | target_train | psi_max | top_drift | unseen_categories |
|---|---|---|---|---|---|---|---|---|
| 0 | 6 - 6 | 37434 | 0.945 | mean 0.0924, median 0, p10 0, p90 0 | mean 0.1334, median 0, p10 0, p90 0 | 11.069 | BonusMalus (11.07), VehBrand (2.07), VehAge (1.41) | 0 |
| 1 | 5 - 5 | 42559 | 0.882 | mean 0.07349, median 0, p10 0, p90 0 | mean 0.1089, median 0, p10 0, p90 0 | 18.419 | BonusMalus (18.42), VehBrand (2.33), VehAge (1.91) | 0 |
| 2 | 4 - 4 | 109197 | 0.721 | mean 0.1072, median 0, p10 0, p90 0 | mean 0.1526, median 0, p10 0, p90 0 | 0.144 | VehBrand (0.14), Region (0.04), VehAge (0.03) | 0 |

## Decisions

### 1. Windows on the IDpol blocks, read as consecutive periods

The release has no dates. IDpol runs in seven blocks; in blocks 1, 3, 5 and 6 a share of the rows repeat a row of the block before with the same car and region, the driver one year older (the rule in next_year_rows), and within a block neighbouring IDpols often share every rating factor. The renewals order the blocks as periods, so blocks 6, 5 and 4 are tested on all earlier blocks (Andrej, 2026-11-20); the order is inferred, not dated.

| IDpol block | rows | claims per year | rows with an earlier-year row (rule) | rows equal in all rating factors to the previous IDpol |
|---|---|---|---|---|
| 0 | 87025 | 0.0863 | 0 | 9033 |
| 1 million | 111964 | 0.0795 | 54571 | 9511 |
| 2 million | 157665 | 0.0735 | 2 | 14898 |
| 3 million | 132147 | 0.0717 | 63800 | 18105 |
| 4 million | 109197 | 0.0644 | 9 | 19260 |
| 5 million | 42559 | 0.0659 | 20924 | 14695 |
| 6 million | 37434 | 0.0586 | 22577 | 10974 |

## Bundle checks

0 error(s), 0 warning(s), 0 info (28 checks run, plus the dataset's own checks).


Accepted on purpose:

- `dataset_duplicate_rows`: Accepted (Lennart, 2026-11-04); counts of 2026-11-06 on the 9 rating factors: 181,197 rows (26.7%) copy an earlier row with the same target, and 327,862 sit in 138,537 groups of identical factors, 92.9% of which sum to at most 1.01 years, so most groups look like one policy-year split into records (each with its own IDpol) rather than distinct policies. The harm is at the folds' noise of about 0.0006: a memorizer of training twins gains +0.0001, the group's size and the other records' exposure +0.0004, the count of identical rows over train and test +0.0005; the one exception is the profile of the high counts (notes).
- `dataset_conflicting_duplicate_rows`: Accepted (Lennart, 2026-11-04); counts of 2026-11-06: 8,128 rows (1.2%) share every rating factor with another row but differ in the target, 7,971 of them in the claim count: claims are rare, random events of identical risk profiles, not noise.
- `task_target_value_dominant`: 96% of the policies have no claim: real no-claim policies, the nature of claim frequency.
- `splits_feature_missing_in_test`: Accepted (Andrej, 2026-11-20): the block-5 window trains on IDpol blocks 0-4, where `BonusMalus` is blanked (recorded after the year's own claims there), and tests on block 5, where it is a start-of-year value; a pricing model meets a factor once it starts being recorded, and block 6's window learns it from block 5. Measured: most of block 5's stationarity gap is this column (+0.0014 with it, +0.0005 without).
- `task_time_on_few_unique`: Accepted (Andrej, 2026-11-20): the split is ordered by the seven IDpol blocks, the only time key the release holds (no dates); each window tests one whole block.

## Data checks

### Feature summary

<details>
<summary>Show the table (12 rows)</summary>

| index | dtype | n_missing | pct_missing | n_unique | examples |
|---|---|---|---|---|---|
| VehBrand | category | 0 | 0 | 11 | B12, B1, B2, B3, B5, B6, B4, B10, B11, B13 |
| VehGas | category | 0 | 0 | 2 | Regular, Diesel |
| Area | category | 0 | 0 | 6 | C, D, E, A, B, F |
| Region | category | 0 | 0 | 22 | Centre, Rhone-Alpes, Provence-Alpes-Cotes-D'Azur, Ile-de-France, Bretagne, Pays… |
| BonusMalus | float64 | 597998 | 88.2 | 82 | 50.0, 100.0, 76.0, 80.0, 72.0, 68.0, 64.0, 57.0, 60.0, 85.0 |
| VehAge | float64 | 48 | 0.01 | 76 | 1.0, 2.0, 0.0, 3.0, 4.0, 5.0, 10.0, 6.0, 7.0, 8.0 |
| DrivAge | float64 | 66 | 0.01 | 83 | 36.0, 38.0, 39.0, 37.0, 52.0, 34.0, 40.0, 51.0, 41.0, 42.0 |
| Exposure | float64 | 0 | 0 | 181 | 1.0, 0.08, 0.07, 0.24, 0.5, 0.49, 0.03, 0.04, 0.12, 0.2 |
| claim_frequency | float64 | 0 | 0 | 224 | 0.0, 1.0, 2.0, 2.0408, 12.5, 1.3333, 4.1667, 1.3514, 1.1494, 2.439 |
| VehPower | int64 | 0 | 0 | 12 | 6, 7, 5, 4, 8, 10, 9, 11, 12, 13 |
| Density | int64 | 0 | 0 | 1607 | 27000, 3317, 1313, 9307, 3744, 1326, 405, 4128, 4762, 57 |
| idpol_block | int64 | 0 | 0 | 7 | 2, 3, 1, 4, 0, 5, 6 |

</details>

### Target distribution

| index | y_missing_count | non_positive_pct | skew_y | skew_log | var_y | var_log | log_used | aic_exponential | aic_lognormal | dist_hint |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 96.32 | 78.581 | 7.997 | 4.099 | 0.055 | log1p | 109046 | 95761.4 | lognormal |

### Numeric features

| index | count | mean | std | min | max |
|---|---|---|---|---|---|
| Exposure | 677991 | 0.528743 | 0.364441 | 0.00273224 | 2.01 |
| VehPower | 677991 | 6.45465 | 2.05091 | 4 | 15 |
| VehAge | 677943 | 7.0377 | 5.61274 | 0 | 85 |
| DrivAge | 677925 | 45.4939 | 14.1283 | 18 | 100 |
| BonusMalus | 79993 | 59.9113 | 15.9218 | 50 | 190 |
| Density | 677991 | 1792.41 | 3958.57 | 1 | 27000 |
| claim_frequency | 677991 | 0.118629 | 2.02458 | 0 | 365 |
| idpol_block | 677991 | 2.50434 | 1.64673 | 0 | 6 |

### Categorical features

<details>
<summary>Show the table (17 rows)</summary>

| column | rank | value | count | pct |
|---|---|---|---|---|
| Area | 1 | C | 191874 | 28.3 |
| Area | 2 | D | 151592 | 22.36 |
| Area | 3 | E | 137163 | 20.23 |
| Area | 4 | A | 103952 | 15.33 |
| Area | 5 | B | 75457 | 11.13 |
| Region | 1 | Centre | 160595 | 23.69 |
| Region | 2 | Rhone-Alpes | 84748 | 12.5 |
| Region | 3 | Provence-Alpes-Cotes-D'Azur | 79315 | 11.7 |
| Region | 4 | Ile-de-France | 69789 | 10.29 |
| Region | 5 | Bretagne | 42120 | 6.21 |
| VehBrand | 1 | B12 | 166022 | 24.49 |
| VehBrand | 2 | B1 | 162730 | 24 |
| VehBrand | 3 | B2 | 159854 | 23.58 |
| VehBrand | 4 | B3 | 53393 | 7.88 |
| VehBrand | 5 | B5 | 34752 | 5.13 |
| VehGas | 1 | Regular | 345863 | 51.01 |
| VehGas | 2 | Diesel | 332128 | 48.99 |

</details>

## Build

| field | value |
|---|---|
| uuid | 01a217ff-2459-7f5a-826b-f258d60038dc |
| checksum | v2:f24fc5f06954b6a12cc6abc6849534b336131dc829dabe528697fc2c772bc826 |
| built_at | 2026-11-26T13:15:43+00:00 |
| path | fremtpl2/01a217ff-2459-7f5a-826b-f258d60038dc |
| data_foundry_version | 0.0.5 |
| git_sha | e3ddd55462cc45eed6aa71c38abd183086888b36 |
| libraries | {'python': '3.12.3', 'pandas': '2.3.3', 'numpy': '2.1.3', 'pyarrow': '20.0.0', 'scikit-learn': '1.7.2', 'polars': '1.41.1'} |
