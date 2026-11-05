---
report_format: data-foundry-report-v2
unique_name: open_soil_spectral_library
container_format: 2
checksum: v2:d348231e2c016f64b5173df0ab4750c93dfe832c780ae58562fe9d71d968d73f
build:
  uuid: 01a1862b-1d5c-7d64-a5ce-76cc983104eb
  checksum: v2:11b25638601b22b60a19c314b909e58a563ac455faa240266bc5fd65e731f145
  built_at: '2026-10-29T05:39:30+00:00'
  path: open_soil_spectral_library/01a1862b-1d5c-7d64-a5ce-76cc983104eb
  data_foundry_version: 0.0.5
  git_sha: 6d189a922994ddb0221c8249d07552d4df8af88b
  libraries:
    python: 3.12.3
    pandas: 3.1.0
    numpy: 2.5.4
    pyarrow: 26.0.0
    scikit-learn: 1.7.2
    polars: 2.0.0
build_stale: true
data:
  n_rows: 75929
  n_features: 1700
  dtypes:
    category: 1
    float64: 1701
  n_test_dataset_rows: null
task:
  target: log1p_organic_carbon_weight_percent
  problem_type: regression
  metric: rmsle
  metric_origin: source
  scoring_columns: null
  split_regime: grouped_non_iid
  stratify_on: null
  time_on: null
  group_on: pedon_id
  group_labels: per_sample
  group_time_on: null
  grouping:
    prediction_unit: row
    aggregation: null
    context: none
    n_groups: 20626
    test_groups_per_fold:
      min: 6875
      max: 6876
  special_features:
    mir_spectrum: spectrum, a group of 1,700 columns (infrared, raw, cm-1 602 to 4000);
      numbers a model can read; recommended encoding spectrum-as-is-r1
splits:
  n_repeats: 3
  n_folds: 3
  random_state: 4267
  time_horizon: null
  time_horizon_unit: null
  time_gap: null
  time_gap_unit: null
  n_train:
    min: 49960
    max: 51059
  n_test:
    min: 24870
    max: 25969
bundle_checks:
  ok: true
  errors: []
  warnings: []
  infos:
  - dataset_duplicates_skipped
  accepted: {}
decisions:
- Source support and missing inputs
- Reference scale
---

# open_soil_spectral_library

> Generated from [`dataset.py`](dataset.py) by `dataset check` (or `build`). Do not edit this page: change `dataset.py` and re-run the check.

Regression of `log1p_organic_carbon_weight_percent`, scored with `rmsle` on grouped splits by `pedon_id`. 75,929 rows and 1,700 features. Source: Other (2023).

Built as `01a1862b-1d5c-7d64-a5ce-76cc983104eb` on 2026-10-29, but `dataset.py` has changed since: it now gives checksum `v2:d348231e2c016f64b5173df0ab4750c93dfe832c780ae58562fe9d71d968d73f`, so the build is stale. See [Build](#build).

## In brief

**Question.** What is the laboratory-reference organic-carbon weight percent of a prepared soil sample from its mid-infrared scan?

**Use case.** A soil spectroscopy laboratory estimates a prepared sample's organic carbon from its mid-infrared scan instead of running the wet chemistry, as the OSSL Engine does for an uploaded scan. Evaluation holds out whole soil profiles and predicts each layer separately.

**One row.** One archived KSSL soil layer with its averaged mid-infrared spectrum and laboratory-reference label, from the July 2022 source snapshot released in OSSL v1.2.

**Predicted.** Organic carbon in weight percent, estimated analytically from total carbon, with the archived S-preparation reference preferred over N preparation when both exist. It ships as log1p of the percent, the scale the source models it on, under a name that says so, and is scored by the RMSE on that log scale, the scale of the source's cross-validation and tuning.

**Known at prediction time.** The sample's mid-infrared absorbance spectrum, 1,700 positions from 602 to 4,000 cm-1 every 2 cm-1, declared as a spectrum. Other laboratory outcomes, identifiers and field metadata are not inputs to the source's scan-upload task, which takes the spectrum alone. A KSSL laboratory scanning its own sample also knows the layer's depths and preparation code; leaving them out is a choice of actor, the source's service over the laboratory's own use.

**What the test data stands for.** Whole KSSL pedon keys (lims.pedon.id) are held out: a key is usually one soil profile whose layers are the rows, while archive campaigns and research projects share a key. Each test layer comes from a key not seen in training, scanned by the same laboratory and instrument.

**Our changes to the source.** We restrict OSSL to KSSL mid-infrared samples, ship the reference as log1p as the source models it and hold out KSSL profiles. Rows without a spectrum or reference label cannot form this prediction task.

> **Use case fit: approximate (a stand-in with a known gap).** The task is the source's own calibration within one laboratory and one instrument. A laboratory using the OSSL models scans on its own instrument, and that transfer, where the source's independent evaluation finds the errors grow, is not tested. Nor are later scans or new survey projects, where one model scored about 8 to 26% worse.

## Files in this folder

| file | what it is |
|---|---|
| [`dataset.py`](dataset.py) | The definition, and the only file edited by hand: metadata, reading and cleaning the raw files, feature types and splits. |
| [`REVIEW.md`](REVIEW.md) | The open questions for the curator, removed once they are settled. Not needed to rebuild. |
| [`README.md`](README.md) | This page, generated by `dataset check` and `dataset build`. |

- The curation record, with the triage decision and its sources: [`curation/records/open_soil_spectral_library.md`](../../../../curation/records/open_soil_spectral_library.md)
- The original source: <https://zenodo.org/records/7599269>
- The collection this folder belongs to: [`tabarena-v0pt2/README.md`](../README.md) and [`tabarena-v0pt2/CHANGELOG.md`](../CHANGELOG.md)

## Rebuild

`dataset.py` reads its raw files from `local-data-warehouse/open_soil_spectral_library/`. To get them:

````text
Recreate the lossless raw inputs with Python 3, R 4.3 or later and qs 0.27.3.
The following complete Python script downloads the four immutable Zenodo v1.2 files,
checks their published MD5 values and decodes them without fitting or cleaning.
Save it as prepare_raw.py, then run:

```sh
python3 prepare_raw.py --raw-dir local-data-warehouse/open_soil_spectral_library
```

Use --existing-only when source files were fetched through a download gateway.
No model is fitted. The archived QS originals remain beside the exports.
A network failure is an access limitation, never evidence against the dataset.

```python
# Standalone raw-input preparation; no fitting or curation decisions.
import argparse,hashlib,subprocess,urllib.request
from pathlib import Path
FILES={
 'ossl_soillab_L0_v1.2.qs':'6817a47891b2281545917e543bf3b7f0',
 'ossl_soillab_L1_v1.2.qs':'652f7bf633d969d6d45cf21007c91a31',
 'ossl_soilsite_L0_v1.2.qs':'232fb5bef505a8b5bfa4fe2120c913d9',
 'ossl_mir_L0_v1.2.qs':'de56ed6d11ea9ca8c54475a674586b00'}
a=argparse.ArgumentParser();a.add_argument('--raw-dir',type=Path,required=True);a.add_argument('--rscript',default='Rscript');a.add_argument('--existing-only',action='store_true');args=a.parse_args();d=args.raw_dir;d.mkdir(parents=True,exist_ok=True)
for name,expected in FILES.items():
 f=d/name
 if not f.exists():
  if args.existing_only:raise SystemExit('Missing '+str(f))
  urllib.request.urlretrieve('https://zenodo.org/records/7599269/files/'+name+'?download=1',f)
 h=hashlib.md5()
 with f.open('rb') as s:
  for block in iter(lambda:s.read(8*1024*1024),b''):h.update(block)
 if h.hexdigest()!=expected:raise SystemExit('Checksum mismatch '+name)
LAB_R="args <- commandArgs(trailingOnly=TRUE)\nlibrary(qs)\noptions(digits=17)\nfor (path in args) {\n cat('\\nFILE ', basename(path), '\\n', sep='')\n x <- qread(path, nthreads=2)\n cat('CLASS ', paste(class(x),collapse=','), ' DIM ', paste(dim(x),collapse=' x '), '\\n', sep='')\n cat('COLUMNS\\n'); cat(paste(names(x),collapse='\\n'),'\\n')\n if ('dataset.code_ascii_txt' %in% names(x)) {cat('DATASET_COUNTS\\n'); print(table(x[['dataset.code_ascii_txt']],useNA='always'))}\n cols <- grep('(^oc_|^c.tot_|^caco3_|^id[.]|^layer[.]|^scan)',names(x),value=TRUE)\n write.csv(data.frame(column=names(x),type=sapply(x,function(z)paste(class(z),collapse=':'))), paste0(path,'.schema.csv'),row.names=FALSE)\n # Export all lab/site columns for exact source-key qualification. Decimal strings preserve 17 significant digits.\n y <- as.data.frame(x)\n for (n in names(y)) if(is.numeric(y[[n]])) y[[n]] <- ifelse(is.na(y[[n]]),NA,format(y[[n]],digits=17,scientific=TRUE,trim=TRUE))\n write.csv(y,gzfile(paste0(path,'.csv.gz')),row.names=FALSE,na='')\n cat('EXPORTED ',nrow(y),' ROWS\\n',sep='')\n}\n"
MIR_R="args <- commandArgs(trailingOnly=TRUE)\nlibrary(qs)\nx <- qread(args[1],nthreads=2)\ncat('DIM ',paste(dim(x),collapse=' x '),'\\n');cat('DATASET_COUNTS\\n');print(table(x[['dataset.code_ascii_txt']],useNA='always'))\nbins <- grep('^scan_mir[.]',names(x),value=TRUE)\ncat('BIN_COUNT ',length(bins),'\\n');cat('NONBIN_COLUMNS\\n');cat(paste(setdiff(names(x),bins),collapse='\\n'),'\\n')\nk <- x[x[['dataset.code_ascii_txt']]=='KSSL.SSL',,drop=FALSE]\ncat('KSSL_ROWS ',nrow(k),'\\n');writeLines(bins,paste0(args[2],'.bins.txt'))\n# R columns are written sequentially; Python reconstructs with Fortran order.\nwriteBin(as.double(as.matrix(k[,bins])),paste0(args[2],'.float64.bin'),size=8,endian='little')\nm <- as.data.frame(k[,setdiff(names(k),bins)])\nfor(n in names(m))if(is.numeric(m[[n]]))m[[n]]<-ifelse(is.na(m[[n]]),NA,format(m[[n]],digits=17,scientific=TRUE,trim=TRUE))\nwrite.csv(m,gzfile(paste0(args[2],'.metadata.csv.gz')),row.names=FALSE,na='')\nwrite.csv(data.frame(column=names(x),type=sapply(x,function(z)paste(class(z),collapse=':'))),paste0(args[2],'.schema.csv'),row.names=FALSE)\n"
lab=d/'decode-lab.R';mir=d/'decode-mir.R';lab.write_text(LAB_R);mir.write_text(MIR_R)
subprocess.run([args.rscript,str(lab),*[str(d/n) for n in FILES if 'mir_L0' not in n]],check=True)
subprocess.run([args.rscript,str(mir),str(d/'ossl_mir_L0_v1.2.qs'),str(d/'kssl_mir')],check=True)
print('Verified source checksums and prepared lossless inputs in',d)
```
````

Then, from the repository root:

```bash
.venv/bin/python -m data_foundry.curation.cli dataset check datasets/_dev/tabarena-v0pt2/open_soil_spectral_library   # pipeline and checks, no UUID; rewrites this page
.venv/bin/python -m data_foundry.curation.cli dataset build datasets/_dev/tabarena-v0pt2/open_soil_spectral_library   # also saves the container and records its UUID
```

Only curators run `build`, when the dataset ships.

## Dataset and task

| field | value |
|---|---|
| source | Other: https://zenodo.org/records/7599269 |
| year | 2023 |
| domain | environmental science & climate |
| license | CC BY 4.0 |
| data_tags | Non-IID, Grouped |
| reference | safanelli2023ossl |
| rows x columns | 75,929 x 1,702 |
| task.target | log1p_organic_carbon_weight_percent |
| task.problem_type | regression |
| task.metric | rmsle |
| task.split_regime | grouped_non_iid |
| task.group_on | pedon_id |
| task.group_labels | per_sample |

**Metric**

| field | value |
|---|---|
| name | `rmsle` (standard; takes value; lower is better) |
| origin | source: the source's metric |
| original | RMSE of log1p organic carbon in the source's 10-fold cross-validation and model tuning |
| reference | https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0296545 |
| definition | sqrt(mean((log1p(y) - log1p(y_hat))**2)) per layer on weight percent, after expm1 of the shipped log1p values and of the predictions: the RMSE of the shipped values. The paper's 10-fold CV and its tuning use RMSE on log1p (S2: "reported in the natural logarithm space"); its independent sets report RMSE in percent, and it ranks model types by Lin's CCC with RPIQ. |
| target scale | ships on the `log1p` scale for modelling; scored on the original scale after the inverse of `log1p` |

<details>
<summary>Feature types: 1 categorical, 0 string, 0 datetime, spectrum `mir_spectrum`</summary>

- categorical (1): `pedon_id`
- string (0): none
- datetime (0): none
- special feature `mir_spectrum`: spectrum, a group of 1,700 columns (infrared, raw, cm-1 602 to 4000); numbers a model can read; recommended encoding spectrum-as-is-r1; columns `mir_602` to `mir_4000`

</details>

<details>
<summary>BibTeX</summary>

```bibtex
@dataset{safanelli2023ossl,
  author={Safanelli, Jose L. and Hengl, Tomislav and Sanderman, Jonathan and Parente, Leandro},
  title={Open Soil Spectral Library (training data and calibration models)},
  year={2023}, version={v1.2}, publisher={Zenodo}, doi={10.5281/zenodo.7599269}
}
```

</details>

## Sample rows

The first 5 of 75,929 rows of the final frame (random rows: the frame is shuffled); 12 of 1,702 columns, the target first. Cells are cut at 40 characters.

| log1p_organic_carbon_weight_percent | mir_602 | mir_604 | mir_606 | mir_608 | mir_610 | mir_612 | mir_614 | mir_616 | mir_618 | mir_620 | mir_622 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.536493 | 1.47982 | 1.47895 | 1.47925 | 1.4814 | 1.48182 | 1.48093 | 1.47804 | 1.47368 | 1.46919 | 1.46545 | 1.46223 |
| 0.81093 | 1.5989 | 1.6095 | 1.61978 | 1.63558 | 1.64416 | 1.65427 | 1.66141 | 1.6661 | 1.6693 | 1.67163 | 1.67361 |
| 0.277329 | 1.4504 | 1.4564 | 1.46528 | 1.48438 | 1.4953 | 1.50646 | 1.51433 | 1.52092 | 1.52721 | 1.53289 | 1.53715 |
| 0.314811 | 1.28147 | 1.27585 | 1.2716 | 1.26437 | 1.25849 | 1.2498 | 1.23994 | 1.22975 | 1.22038 | 1.21192 | 1.20383 |
| 1.07691 | 1.6581 | 1.66245 | 1.66865 | 1.67934 | 1.68423 | 1.68854 | 1.68955 | 1.68935 | 1.68994 | 1.6909 | 1.69211 |

## Curation notes

We start with the lab L1, site L0 and MIR L0 tables of Zenodo record 7599269, v1.2, with archived L0 lab references retained for auditing.

- Prediction point: a prepared scan is available, a new chemical reference is not. Keep 1,700 raw spectral bins (602 to 4,000 cm-1; the 600 cm-1 edge is dropped). The source scan-upload service does not require field metadata (superseded 2026-11-05: it accepts none, see the next line); other chemistry outcomes and carbon equivalents never enter its inputs (USE-3, LEAK-10).
- CC (2026-11-05, Lennart): the spectrum only, with the source's scan-upload service as the actor (issue 6, ok on the implemented option; USE-3, USE-6). A KSSL laboratory also knows the layer's two depths and the preparation code (XS or XN); adding them lowered RMSLE by 3.6% on the two folds tried, and leaving them out is a choice of actor. The service accepts none of them: the OSSL API v1.2 prediction call takes the spectra file, the property, the spectral range, the subset (KSSL or OSSL) and the model, depth is only a filter for downloading library rows, and every v1.2 model is coded `na`, "only the spectra data" (api.soilspectroscopy.org, the ossl-models README; checked 2026-11-05).
- The metric is the source's cross-validation metric, RMSE on log1p, which is `rmsle` on the percent (Lennart, 2026-11-04: "follow the recommendation, following the source").
- The spectrum ships as KSSL exported it and OSSL v1.2 published it, and is declared as one (`special_features`, CLEAN-26; Lennart, 2026-11-04): the absorbance of the finely ground sample on KSSL's Bruker Vertex 70 with the HTS-XT accessory, replicate scans averaged, on KSSL's 2 cm-1 grid from 600 to 4,000 cm-1, stored to 5 decimals. OSSL applies the standard normal variate inside its models, not in the table, so the state is `raw`. The bins are renamed from `scan_mir.<wavenumber>_abs` to `mir_<wavenumber>` so the build reads the axis from the names; no value changes.
- The 600 cm-1 edge: 53 spectra read exactly 0 at 600 cm-1 while their 602 cm-1 value is 1.27 to 1.86 (50 of them scanned in 2011, 42 on two days), a fill at the edge of the range. The bin is dropped for every row (Lennart, 2026-11-04: "do (b)"), so each spectrum stays whole, 602 to 4,000 cm-1. The other 32 exact zeros are sign changes of a near-zero absorbance above 2,000 cm-1. The 600 cm-1 bin's distinct-value count (27,193) is ordinary: the counts run from about 23,000 to 55,000 along the whole axis, and the bins to 606 cm-1 have as few. 36 spectra in 21 pedons have a negative mean absorbance, sloping to between -0.5 and -0.97 at the high-wavenumber end (a tilted baseline); they ship as published, since dropping them and similar rows from training made an honest LightGBM worse on every split (by 0.0005 to 0.006, 2026-11-04).
- CC (2026-11-05, Lennart): the dropped 600 cm-1 edge is filed as an amendment of the spectrum rule, not an exception (issue 10, A; CLEAN-26 as amended 2026-11-05, narrowing CLEAN-11): a fill at an edge position drops that position for every row, a fill at an inner position is set missing and the column stays. Re-counted on the raw export on 2026-11-05: 53 spectra read 0 at 600 cm-1 beside 1.27 to 1.86 at 602 cm-1, and no other position from 602 to 610 cm-1 holds a 0.
- Encodings (2026-11-04, the three folds of repeat 0, untuned: LightGBM with 500 trees, learning rate 0.1 and 30% of the bins per tree; PLS with 30 components; ridge with alpha by GCV on the training fold). On the declared scale (fitted on the shipped log1p, RMSE on log1p), LightGBM falls from 0.155 on the spectrum as it is to 0.130 with the registered ALS baseline and SNV, 0.136 with SNV alone and 0.118 with a Savitzky-Golay first derivative (11 points, order 2; both registered on 2026-11-04 as `vib-snv-r1` and `vib-sg11-d1-r1`), lower on 3 of 3 folds each. PLS gains from SNV (0.158 to 0.145, 3 of 3) and the derivative (0.150, 3 of 3), not from ALS and SNV (0.164, 0 of 3); ridge gains a little from SNV (0.142 to 0.138, 2 of 3) and from nothing else. The recommended encoding stays the spectrum as it is (CLEAN-26). The earlier figures were fitted and scored in percent (LightGBM 1.74 as it is, 1.33, 1.39 and 1.24 processed; ridge best as it is at 1.84); fitted on log1p and scored in percent, the same LightGBM gives 1.85 as it is. In percent, layers above 12% organic carbon (16% of rows) carry 79 to 95% of the squared error, and an unclipped linear fit on log1p put one layer at 118,759% (ridge with SNV, one fold: RMSE 745, and 1.86 with the predictions clipped to the training range).
- Restrict the source code to KSSL.SSL. Join on dataset.code_ascii_txt and id.layer_uuid_txt with one-to-one validation, never by row position or rounded coordinates. The native KSSL pedon key lims.pedon.id (renamed id.dataset.site_ascii_txt by the 2023-01-09 importer) is the group, never a model feature.
- The L1 organic-carbon label is an analytical estimate, not a spectroscopy prediction. Archived KSSL L0 S-preparation values take precedence over N preparation; the row-wise coalescence reproduces every KSSL L1 value and missingness mask (2026-10-27; not re-tested on 2026-11-04, when the local L0 export had one organic-carbon column). The upstream importer had already converted negative laboratory references to missing; this cannot recover their pre-import count.
- Drop rows without any spectrum, and rows with a missing target. Do not clip the reference, discard zero endpoints, average repeated entities or fit a spectral transform over all rows. Raw reference values and source identities remain in the warehouse.
- 151 layers read above 58% organic carbon, 3 of them above 70% (up to 78.45%; RaCA project MO14, N preparation, O horizons). The three above 70% equal the source's measured total carbon with no carbonate measured, and the source's L0 table carries the same values, so they stay unclipped (CLEAN-11: unusual, not shown impossible). A later KSSL release that revises these samples would reopen this.
- Hold out whole KSSL pedon keys. A key is usually one sampled soil profile whose layers are the rows; archive campaigns and research projects share a key (the largest, 640 rows over 151 depths, is a North Dakota archive campaign; 1,779 keys with 14% of rows repeat a depth), and replicate pits at one site have separate keys (348 locations; grouping by location gives about 0.150 against 0.148 RMSE on log1p, LightGBM, three folds). Holding a key out tests a new sample from the same laboratory and instrument. Each layer is predicted and scored separately. Myunghwan chose the key over coordinates on 2026-10-27 ("group id is slightly better. stick to group id").
- Ship the reference as log1p(weight percent) and score the RMSE on that scale, `rmsle` on weight percent, the source's CV and tuning scale (MET-3; Lennart, 2026-11-04: "Follow the source metric and scale"). The source fits organic carbon on log1p (`log1p()` for every property but clay, silt, sand and the two pH values) and back-transforms with `expm1()` for its independent evaluation. Myunghwan's 2026-10-27 choice of the original target compared percent with a fraction, not with log1p.
- CC (2026-11-05, Lennart): the target column is renamed from `organic_carbon_weight_percent` to `log1p_organic_carbon_weight_percent`, the values unchanged (issue 9, A with (a); CLEAN-16). The old name stated a unit, weight percent, that the shipped values (0 to 4.375) contradict, and the blind reviewer, reading the data without our notes, concluded they could not be percent. The four kept names, `price` (diamonds, mercari), `loss` (allstate) and `area` (forest_fires), state no unit. The name puts the transform before the source's quantity, as ashrae's `log1p_meter_reading` does.
- Metric provenance: the source tunes Cubist by RMSE on log1p (inner 5-fold CV on 2,000 samples), reports its 10-fold CV on log1p (for KSSL MIR organic carbon n = 75,929 as here, RMSE 0.114 and CCC 0.995, in `out/fitted_models_performance_v1.2.csv` of github.com/soilspectroscopy/ossl-models; the paper's S2 Table gives 0.11 and 0.99 "in the natural logarithm space"), reports its independent evaluation in percent after back-transformation (Table 5, S3 Table) and ranks its models by Lin's CCC with an RPIQ cut-off of 2 (Fig 5). The declared RMSLE is on the scale of the source's CV and tuning; the percent scale belongs to its independent evaluation sets, the instrument transfer this task does not test.
- CC (2026-11-05, Lennart): the fact that sets the log-scale metric apart from forest_fires is filed as a MET-5 case (issue 8, A; MET-5): the source tunes by RMSE on log1p and reports its 10-fold CV on log1p for exactly this cut (n = 75,929, RMSE 0.114), with the laboratory and instrument this split keeps; the CCC-with-RPIQ ranking is a compound grade of the published models, and the percent results come from the independent sets.
- CC (2026-11-05, Lennart): the declared metric (`rmsle` on weight percent, the RMSE of the shipped log1p values, the source's) is checked and stays as declared.
- Version note: this growing-source snapshot was created on Zenodo in February 2023 and uses July 2022 KSSL inputs; the landing page also displays a 2021 publication date. The current record and definition use the 2023 snapshot convention; the historical 2021 landing-page date remains disclosed.
- Source overlap: WoSIS documents USDA-NCSS ancestry, and KSSL contains ISRIC-labelled projects. The tasks differ from this MIR calibration; physical aliquot overlap is unmeasured. All 76,813 complete KSSL spectra compared with 8,871 complete other-library spectra show no exact full-grid copies (2026-10-27; not re-tested on 2026-11-04, which needs R to decode the other libraries); rescans and partial-grid records remain outside that claim.
- Preparation audit: 55,855 usable XS scans use S references; 20,043 XN scans use N references; 31 XS scans use the source N fallback. Preserve all usable scan/reference rows and source coalescence; identity harmonization is not an analytical-equivalence claim.

- Curator-requested few-band diagnostics (2026-10-27, on the percent target with all 1,701 bins, before the 600 cm-1 bin was dropped) on three fixed grouped samples found two-band OLS RMSE 5.98 and five-band OLS 4.01 percentage points, versus 1.96 for retained full-spectrum Ridge. Ten training-fitted PCs retained 98.6% of input variance; PCA10 Ridge RMSE was 4.55 and PCA10 LightGBM 2.77, versus full-spectrum LightGBM 2.43. These are bounded, untuned comparisons on identical 5,000-row train/test samples per fold, not full-data rankings or deployed preprocessing. All 1,700 retained bins ship as inputs.

## Splits

Whole KSSL profiles (pedon keys) held out, three repeats of three folds with seed 4267: a test layer's key is never in training, and the laboratory and instrument are the same in training and test. 93-96% of test layers have their survey project in training; a model applied to later scans or new projects scores about 8-26% worse in RMSLE (LightGBM, 2026-11-04), and whether rankings change is untested. A project or scan-date split is a candidate variant (SPLIT-31), not built.

3 repeat(s) x 3 fold(s) with seed 4267; train 49,960 to 51,059 rows, test 24,870 to 25,969 rows.

| repeat | fold | n_train | n_test |
|---|---|---|---|
| 0 | 0 | 51059 | 24870 |
| 0 | 1 | 50551 | 25378 |
| 0 | 2 | 50248 | 25681 |
| 1 | 0 | 50909 | 25020 |
| 1 | 1 | 50989 | 24940 |
| 1 | 2 | 49960 | 25969 |
| 2 | 0 | 51050 | 24879 |
| 2 | 1 | 50030 | 25899 |
| 2 | 2 | 50778 | 25151 |

## Group structure

The KSSL pedon key lims.pedon.id (archived as id.dataset.site_ascii_txt): usually one sampled soil profile, whose layers are the rows. Archive campaigns and research projects share a key (the largest has 640 rows), and replicate pits at one site have separate keys (348 locations; grouping by location gives about 0.150 against 0.148 RMSLE). Holding a key out tests a new sample from the same laboratory and instrument. Each layer is predicted and scored on its own, with no group context.

| field | value |
|---|---|
| group column | `pedon_id` |
| labels | per_sample |
| order inside a group | none |
| prediction unit | row |
| known about a group when predicting | none |

| statistic | value |
|---|---|
| groups | 20,626 |
| rows per group (min / median / max) | 1 / 3.0 / 640 |
| largest group | 0.8% of the rows |
| test groups per fold | 6,875 to 6,876 |
| groups of two or more rows with a single label | 0.1% |
| nearest neighbour in the same group | 10.4% of the rows (chance: 0.0%) |
| label variance explained by the group | 0.78 (shuffled groups: 0.27) |

The nearest neighbour is computed on the standardised numeric features of a sample of up to 20,000 rows; chance is the share expected if the groups were unrelated to the features. The model-based diagnostics run with `.claude/skills/knowledge-data-foundry/scripts/group_probes.py`.

## Decisions

### 1. Source support and missing inputs

An absent scan is not this task's input; a missing reference cannot be scored (USE-7, CLEAN-15).

| index | 0 |
|---|---|
| KSSL source rows | 86603 |
| rows without MIR | 9790 |
| missing OC references | 934 |
| usable MIR and OC | 75929 |
| native KSSL source keys | 20626 |
| zero OC endpoints retained | 62 |
| spectra with a 0 at 600 cm-1 (bin dropped) | 53 |

### 2. Reference scale

Organic carbon in weight percent ships as log1p, the scale the source fits and tunes on; the score is the RMSE on that scale (`rmsle` on weight percent), the source's CV and tuning scale (MET-3).

| index | weight percent | shipped log1p |
|---|---|---|
| count | 75929 | 75929 |
| mean | 7.0173 | 1.19437 |
| std | 13.7142 | 1.15633 |
| min | 0 | 0 |
| 1% | 0.0288 | 0.0283931 |
| 50% | 1.19 | 0.783902 |
| 99% | 53.57 | 3.99948 |
| max | 78.45 | 4.37513 |

## Bundle checks

0 error(s), 0 warning(s), 1 info (27 checks run, plus the dataset's own checks).

- **info** `dataset_duplicates_skipped`: Skipped duplicate-column/row checks: 129,231,158 cells exceed the budget of 50,000,000. (hint: Raise `heavy_cell_budget=` to force them, or rely on `dataset_checks.run_all_checks`.)

## Data checks

### Feature summary

<details>
<summary>Show the table (1,702 rows)</summary>

| index | dtype | n_missing | pct_missing | n_unique | examples |
|---|---|---|---|---|---|
| pedon_id | category | 0 | 0 | 20626 | 39678, 10520, 6273, 28853, 11914, 13275, 10569, 33562, 32468, 12011 |
| mir_602 | float64 | 0 | 0 | 27376 | 1.5564, 1.5672, 1.5952, 1.5683, 1.6055, 1.5067, 1.5417, 1.5719, 1.4989, 1.594 |
| mir_604 | float64 | 0 | 0 | 27514 | 1.5705, 1.5877, 1.5935, 1.5649, 1.5216, 1.5429, 1.5934, 1.5009, 1.542, 1.5239 |
| mir_606 | float64 | 0 | 0 | 27598 | 1.5658, 1.5609, 1.4825, 1.5573, 1.5619, 1.5839, 1.5825, 1.5914, 1.5347, 1.5883 |
| mir_608 | float64 | 0 | 0 | 42243 | 1.6167, 1.6106, 1.5868, 1.6142, 1.5832, 1.5722, 1.4722, 1.5419, 1.6444, 1.5867 |
| mir_610 | float64 | 0 | 0 | 42322 | 1.5241, 1.6049, 1.5473, 1.5276, 1.6377, 1.5691, 1.4863, 1.5803, 1.5745, 1.5776 |
| mir_612 | float64 | 0 | 0 | 42479 | 1.571, 1.608, 1.5286, 1.5747, 1.625, 1.608, 1.6376, 1.6876, 1.6726, 1.5676 |
| mir_614 | float64 | 0 | 0 | 42727 | 1.6165, 1.6072, 1.6846, 1.5929, 1.5396, 1.5797, 1.6082, 1.5869, 1.6399, 1.7057 |
| mir_616 | float64 | 0 | 0 | 43017 | 1.6373, 1.6044, 1.6456, 1.6237, 1.5704, 1.5817, 1.5753, 1.6108, 1.6543, 1.5708 |
| mir_618 | float64 | 0 | 0 | 43282 | 1.6391, 1.6288, 1.5676, 1.6608, 1.6285, 1.6567, 1.6028, 1.6033, 1.5153, 1.793 |
| mir_620 | float64 | 0 | 0 | 43477 | 1.6223, 1.5823, 1.6409, 1.7487, 1.5405, 1.6179, 1.5903, 1.5835, 1.7032, 1.6316 |
| mir_622 | float64 | 0 | 0 | 43751 | 1.5751, 1.5869, 1.6892, 1.6062, 1.6368, 1.61, 1.565, 1.5974, 1.669, 1.6156 |
| mir_624 | float64 | 0 | 0 | 43742 | 1.6519, 1.5965, 1.578, 1.6306, 1.6606, 1.6459, 1.5804, 1.5779, 1.6525, 1.6621 |
| mir_626 | float64 | 0 | 0 | 43835 | 1.5794, 1.708, 1.5863, 1.5672, 1.5438, 1.596, 1.661, 1.6401, 1.5647, 1.7276 |
| mir_628 | float64 | 0 | 0 | 44109 | 1.6928, 1.632, 1.603, 1.6305, 1.6144, 1.5947, 1.6227, 1.6721, 1.6814, 1.6212 |
| mir_630 | float64 | 0 | 0 | 44269 | 1.6309, 1.6344, 1.6094, 1.713, 1.5853, 1.6581, 1.603, 1.6587, 1.5404, 1.6661 |
| mir_632 | float64 | 0 | 0 | 44419 | 1.6752, 1.6189, 1.576, 1.4384, 1.598, 1.6764, 1.5962, 1.6175, 1.6584, 1.6067 |
| mir_634 | float64 | 0 | 0 | 29911 | 1.6662, 1.6307, 1.6719, 1.6514, 1.6763, 1.5926, 1.5831, 1.5961, 1.6414, 1.6192 |
| mir_636 | float64 | 0 | 0 | 29915 | 1.6077, 1.5833, 1.6368, 1.5544, 1.6042, 1.5451, 1.6226, 1.6419, 1.6053, 1.6427 |
| mir_638 | float64 | 0 | 0 | 30209 | 1.6674, 1.5987, 1.6358, 1.652, 1.6576, 1.6057, 1.6154, 1.6544, 1.6327, 1.6068 |
| mir_640 | float64 | 0 | 0 | 30161 | 1.5956, 1.601, 1.5675, 1.5284, 1.5989, 1.6403, 1.5734, 1.6719, 1.6585, 1.5903 |
| mir_642 | float64 | 0 | 0 | 30402 | 1.6493, 1.6368, 1.6235, 1.6945, 1.668, 1.5725, 1.5619, 1.6308, 1.6067, 1.6268 |
| mir_644 | float64 | 0 | 0 | 30430 | 1.565, 1.6448, 1.6052, 1.6526, 1.578, 1.5464, 1.6596, 1.5519, 1.6646, 1.6936 |
| mir_646 | float64 | 0 | 0 | 30649 | 1.5826, 1.6345, 1.6096, 1.5415, 1.5612, 1.5728, 1.5362, 1.5521, 1.5874, 1.5413 |
| mir_648 | float64 | 0 | 0 | 30853 | 1.617, 1.5358, 1.5626, 1.5707, 1.5963, 1.5136, 1.5955, 1.6294, 1.5413, 1.5758 |
| mir_650 | float64 | 0 | 0 | 31080 | 1.5433, 1.6494, 1.6381, 1.5398, 1.7314, 1.5678, 1.6252, 1.5735, 1.6199, 1.5123 |
| mir_652 | float64 | 0 | 0 | 31320 | 1.5743, 1.5527, 1.5647, 1.5212, 1.5615, 1.5705, 1.5872, 1.6769, 1.6409, 1.6817 |
| mir_654 | float64 | 0 | 0 | 31460 | 1.6013, 1.6164, 1.5686, 1.5413, 1.5915, 1.5355, 1.5049, 1.6249, 1.6459, 1.6091 |
| mir_656 | float64 | 0 | 0 | 31620 | 1.6127, 1.5269, 1.5412, 1.6181, 1.5731, 1.6304, 1.5888, 1.5494, 1.5376, 1.5662 |
| mir_658 | float64 | 0 | 0 | 31750 | 1.6209, 1.5443, 1.5848, 1.6024, 1.5397, 1.5679, 1.6245, 1.5908, 1.568, 1.5501 |
| mir_660 | float64 | 0 | 0 | 31769 | 1.6141, 1.5061, 1.6218, 1.6278, 1.6069, 1.622, 1.6213, 1.5608, 1.5669, 1.6685 |
| mir_662 | float64 | 0 | 0 | 46639 | 1.6284, 1.4918, 1.6429, 1.6994, 1.62, 1.4908, 1.6635, 1.6165, 1.5907, 1.5173 |
| mir_664 | float64 | 0 | 0 | 46622 | 1.7032, 1.5922, 1.6373, 1.5599, 1.573, 1.6088, 1.6081, 1.5203, 1.6647, 1.588 |
| mir_666 | float64 | 0 | 0 | 46435 | 1.5037, 1.5224, 1.4815, 1.532, 1.6681, 1.6194, 1.5601, 1.6624, 1.5444, 1.5543 |
| mir_668 | float64 | 0 | 0 | 46476 | 1.4345, 1.5999, 1.5644, 1.6247, 1.6403, 1.5954, 1.5743, 1.5262, 1.6331, 1.5661 |
| mir_670 | float64 | 0 | 0 | 46596 | 1.654, 1.5147, 1.5845, 1.5499, 1.6738, 1.5489, 1.6753, 1.6261, 1.5382, 1.5857 |
| mir_672 | float64 | 0 | 0 | 46264 | 1.6037, 1.5803, 1.7017, 1.5348, 1.453, 1.6482, 1.5317, 1.6085, 1.5766, 1.5784 |
| mir_674 | float64 | 0 | 0 | 46257 | 1.6104, 1.5695, 1.5892, 1.5757, 1.5298, 1.6005, 1.575, 1.5861, 1.5546, 1.6197 |
| mir_676 | float64 | 0 | 0 | 46067 | 1.654, 1.5278, 1.5898, 1.5618, 1.5683, 1.5944, 1.518, 1.6401, 1.537, 1.5674 |
| mir_678 | float64 | 0 | 0 | 46063 | 1.6094, 1.5733, 1.558, 1.571, 1.6757, 1.5317, 1.5735, 1.4241, 1.5883, 1.6502 |
| mir_680 | float64 | 0 | 0 | 45742 | 1.5628, 1.5743, 1.572, 1.5029, 1.566, 1.5104, 1.6009, 1.6211, 1.5177, 1.6051 |
| mir_682 | float64 | 0 | 0 | 45277 | 1.5451, 1.6226, 1.5612, 1.5607, 1.5502, 1.4999, 1.5887, 1.5481, 1.5232, 1.5924 |
| mir_684 | float64 | 0 | 0 | 44844 | 1.6284, 1.5231, 1.5397, 1.6867, 1.6021, 1.6617, 1.6318, 1.5396, 1.622, 1.5412 |
| mir_686 | float64 | 0 | 0 | 44407 | 1.5851, 1.5831, 1.6705, 1.5142, 1.5946, 1.6902, 1.6495, 1.5086, 1.6025, 1.5352 |
| mir_688 | float64 | 0 | 0 | 28953 | 1.6355, 1.568, 1.5711, 1.5703, 1.6423, 1.551, 1.6023, 1.6233, 1.6291, 1.6267 |
| mir_690 | float64 | 0 | 0 | 28294 | 1.5611, 1.6086, 1.6483, 1.5534, 1.5279, 1.5938, 1.5545, 1.6051, 1.5301, 1.587 |
| mir_692 | float64 | 0 | 0 | 27717 | 1.5344, 1.639, 1.6267, 1.5905, 1.6176, 1.6046, 1.6063, 1.6887, 1.5768, 1.5729 |
| mir_694 | float64 | 0 | 0 | 27081 | 1.5965, 1.6053, 1.6298, 1.5812, 1.6747, 1.6706, 1.6759, 1.6592, 1.613, 1.6224 |
| mir_696 | float64 | 0 | 0 | 26523 | 1.5848, 1.6691, 1.6218, 1.6868, 1.6168, 1.6311, 1.6044, 1.6874, 1.6756, 1.6107 |
| mir_698 | float64 | 0 | 0 | 26385 | 1.7085, 1.6663, 1.6123, 1.6309, 1.6423, 1.6802, 1.6511, 1.7098, 1.6966, 1.6632 |
| mir_700 | float64 | 0 | 0 | 26533 | 1.6943, 1.7284, 1.6885, 1.6167, 1.648, 1.6045, 1.6845, 1.6911, 1.6521, 1.5897 |
| mir_702 | float64 | 0 | 0 | 27066 | 1.771, 1.6136, 1.7149, 1.7013, 1.6577, 1.5999, 1.6162, 1.6364, 1.5933, 1.6151 |
| mir_704 | float64 | 0 | 0 | 27813 | 1.6585, 1.5969, 1.5947, 1.5847, 1.5983, 1.6337, 1.6361, 1.6205, 1.6311, 1.5527 |
| mir_706 | float64 | 0 | 0 | 28530 | 1.5825, 1.629, 1.656, 1.6036, 1.6178, 1.5828, 1.5997, 1.6228, 1.5863, 1.6236 |
| mir_708 | float64 | 0 | 0 | 29103 | 1.5828, 1.6011, 1.5684, 1.5694, 1.4846, 1.5956, 1.6479, 1.6791, 1.609, 1.6243 |
| mir_710 | float64 | 0 | 0 | 29589 | 1.5415, 1.5767, 1.6332, 1.5883, 1.6387, 1.6362, 1.6223, 1.5356, 1.5905, 1.5488 |
| mir_712 | float64 | 0 | 0 | 29980 | 1.4593, 1.6059, 1.5675, 1.5623, 1.5986, 1.569, 1.5781, 1.6176, 1.5657, 1.434 |
| mir_714 | float64 | 0 | 0 | 30389 | 1.5874, 1.5413, 1.5839, 1.4945, 1.4799, 1.661, 1.4728, 1.5621, 1.5633, 1.5811 |
| mir_716 | float64 | 0 | 0 | 45584 | 1.6297, 1.4795, 1.5733, 1.4732, 1.3834, 1.6309, 1.4955, 1.5394, 1.4725, 1.5497 |
| mir_718 | float64 | 0 | 0 | 45560 | 1.4599, 1.6401, 1.5863, 1.5456, 1.5624, 1.6218, 1.6038, 1.5428, 1.5724, 1.4945 |

(1,642 more rows not shown)

</details>

### Target distribution

| index | y_missing_count | non_positive_pct | skew_y | skew_log | var_y | var_log | log_used | aic_exponential | aic_lognormal | dist_hint |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 0.08 | 1.229 | 0.629 | 1.337 | 0.216 | log1p | 178811 | 188443 | exponential |

### Numeric features

<details>
<summary>Show the table (1,701 rows)</summary>

| index | count | mean | std | min | max |
|---|---|---|---|---|---|
| mir_602 | 75929 | 1.5607 | 0.158091 | 0.18747 | 3.60783 |
| mir_604 | 75929 | 1.56541 | 0.159038 | 0.18634 | 3.56007 |
| mir_606 | 75929 | 1.57114 | 0.159859 | 0.18645 | 3.52065 |
| mir_608 | 75929 | 1.58187 | 0.161298 | 0.18675 | 3.49811 |
| mir_610 | 75929 | 1.58758 | 0.162213 | 0.1867 | 3.50972 |
| mir_612 | 75929 | 1.59347 | 0.163758 | 0.18513 | 3.53036 |
| mir_614 | 75929 | 1.59751 | 0.165573 | 0.18159 | 3.53082 |
| mir_616 | 75929 | 1.60065 | 0.167698 | 0.17708 | 3.51414 |
| mir_618 | 75929 | 1.60375 | 0.169995 | 0.17285 | 3.51623 |
| mir_620 | 75929 | 1.60696 | 0.172249 | 0.16911 | 3.51864 |
| mir_622 | 75929 | 1.60968 | 0.174303 | 0.16585 | 3.49201 |
| mir_624 | 75929 | 1.61168 | 0.176156 | 0.16307 | 3.44849 |
| mir_626 | 75929 | 1.6131 | 0.177804 | 0.16081 | 3.41642 |
| mir_628 | 75929 | 1.61397 | 0.179201 | 0.15901 | 3.397 |
| mir_630 | 75929 | 1.61397 | 0.180362 | 0.15713 | 3.37839 |
| mir_632 | 75929 | 1.6135 | 0.181194 | 0.15508 | 3.37081 |
| mir_634 | 75929 | 1.61049 | 0.182349 | 0.15242 | 3.34385 |
| mir_636 | 75929 | 1.60787 | 0.183022 | 0.15012 | 3.31153 |
| mir_638 | 75929 | 1.60488 | 0.183713 | 0.14798 | 3.28285 |
| mir_640 | 75929 | 1.60162 | 0.184489 | 0.14592 | 3.2647 |
| mir_642 | 75929 | 1.59808 | 0.185419 | 0.14354 | 3.25493 |
| mir_644 | 75929 | 1.59424 | 0.186563 | 0.14092 | 3.2454 |
| mir_646 | 75929 | 1.59005 | 0.187983 | 0.13772 | 3.2279 |
| mir_648 | 75929 | 1.58575 | 0.189718 | 0.13273 | 3.19925 |
| mir_650 | 75929 | 1.58198 | 0.191722 | 0.12562 | 3.17157 |
| mir_652 | 75929 | 1.5791 | 0.19377 | 0.11774 | 3.159 |
| mir_654 | 75929 | 1.57699 | 0.195623 | 0.11034 | 3.15463 |
| mir_656 | 75929 | 1.57547 | 0.197115 | 0.10392 | 3.14355 |
| mir_658 | 75929 | 1.57446 | 0.198157 | 0.09868 | 3.12493 |
| mir_660 | 75929 | 1.5738 | 0.19871 | 0.09479 | 3.1093 |
| mir_662 | 75929 | 1.57289 | 0.198831 | 0.09234 | 3.09176 |
| mir_664 | 75929 | 1.57127 | 0.19849 | 0.09145 | 3.08265 |
| mir_666 | 75929 | 1.56636 | 0.197824 | 0.08994 | 3.07526 |
| mir_668 | 75929 | 1.5606 | 0.196788 | 0.08687 | 3.06225 |
| mir_670 | 75929 | 1.55995 | 0.196025 | 0.08548 | 3.04081 |
| mir_672 | 75929 | 1.56166 | 0.195559 | 0.08705 | 3.02282 |
| mir_674 | 75929 | 1.56119 | 0.194714 | 0.08891 | 3.00788 |
| mir_676 | 75929 | 1.56007 | 0.193363 | 0.09137 | 2.99498 |
| mir_678 | 75929 | 1.55975 | 0.191534 | 0.09558 | 2.98253 |
| mir_680 | 75929 | 1.56083 | 0.189107 | 0.10249 | 2.96674 |
| mir_682 | 75929 | 1.56331 | 0.186163 | 0.11249 | 2.95215 |
| mir_684 | 75929 | 1.56796 | 0.18241 | 0.12641 | 2.94187 |
| mir_686 | 75929 | 1.57259 | 0.179021 | 0.143 | 2.93481 |
| mir_688 | 75929 | 1.58694 | 0.171742 | 0.1688 | 2.92778 |
| mir_690 | 75929 | 1.59935 | 0.166939 | 0.19588 | 2.92453 |
| mir_692 | 75929 | 1.61562 | 0.162323 | 0.19565 | 2.92168 |
| mir_694 | 75929 | 1.63728 | 0.15784 | 0.1953 | 2.92168 |
| mir_696 | 75929 | 1.66163 | 0.153999 | 0.19492 | 2.92465 |
| mir_698 | 75929 | 1.67747 | 0.152474 | 0.19422 | 2.92525 |
| mir_700 | 75929 | 1.67449 | 0.154267 | 0.1928 | 2.91882 |
| mir_702 | 75929 | 1.65587 | 0.158985 | 0.19082 | 2.90735 |
| mir_704 | 75929 | 1.63219 | 0.165098 | 0.1887 | 2.89417 |
| mir_706 | 75929 | 1.61005 | 0.170999 | 0.1828 | 2.8806 |
| mir_708 | 75929 | 1.59138 | 0.175955 | 0.15979 | 2.86642 |
| mir_710 | 75929 | 1.57635 | 0.180077 | 0.14183 | 2.85208 |
| mir_712 | 75929 | 1.56441 | 0.183983 | 0.12756 | 2.8396 |
| mir_714 | 75929 | 1.55407 | 0.187767 | 0.1161 | 2.82805 |
| mir_716 | 75929 | 1.53755 | 0.191056 | 0.10586 | 2.80539 |
| mir_718 | 75929 | 1.52914 | 0.191022 | 0.09947 | 2.79509 |
| mir_720 | 75929 | 1.52024 | 0.19126 | 0.09428 | 2.78711 |

(1,641 more rows not shown)

</details>

### Categorical features

| column | rank | value | count | pct |
|---|---|---|---|---|
| pedon_id | 1 | 39678 | 640 | 0.84 |
| pedon_id | 2 | 10520 | 210 | 0.28 |
| pedon_id | 3 | 6273 | 112 | 0.15 |
| pedon_id | 4 | 28853 | 66 | 0.09 |
| pedon_id | 5 | 11914 | 63 | 0.08 |

## Build

| field | value |
|---|---|
| uuid | 01a1862b-1d5c-7d64-a5ce-76cc983104eb |
| checksum | v2:11b25638601b22b60a19c314b909e58a563ac455faa240266bc5fd65e731f145 |
| built_at | 2026-10-29T05:39:30+00:00 |
| path | open_soil_spectral_library/01a1862b-1d5c-7d64-a5ce-76cc983104eb |
| data_foundry_version | 0.0.5 |
| git_sha | 6d189a922994ddb0221c8249d07552d4df8af88b |
| libraries | {'python': '3.12.3', 'pandas': '3.1.0', 'numpy': '2.5.4', 'pyarrow': '26.0.0', 'scikit-learn': '1.7.2', 'polars': '2.0.0'} |
| stale | yes: the definition now gives checksum `v2:d348231e2c016f64b5173df0ab4750c93dfe832c780ae58562fe9d71d968d73f` |
