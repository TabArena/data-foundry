---
report_format: data-foundry-report-v2
unique_name: chromophore_optical_properties_db
container_format: 2
checksum: v2:723817f8112324dea0515f03fe8f347ca4ca7f57ac735b0f3e48192888166e5b
build:
  uuid: 01a1c4ae-5ada-74a4-b90e-d5924662a442
  checksum: v2:97decdfc67653a344bdbc617300599730e279e24d81cdd2d821e68525f89ccb2
  built_at: '2026-11-10T08:58:44+00:00'
  path: chromophore_optical_properties_db/01a1c4ae-5ada-74a4-b90e-d5924662a442
  data_foundry_version: 0.0.5
  git_sha: 8a50be6ccb71d6b8fb77047ba7603028dd37e596
  libraries:
    python: 3.12.3
    pandas: 3.1.0
    numpy: 2.5.4
    pyarrow: 26.0.0
    scikit-learn: 1.7.2
    polars: 2.0.0
build_stale: true
data:
  n_rows: 17509
  n_features: 3
  dtypes:
    category: 1
    float64: 1
    int64: 1
    string: 2
  n_test_dataset_rows: null
task:
  target: Absorption max (nm)
  problem_type: regression
  metric: rmse
  metric_origin: fallback
  scoring_columns: null
  split_regime: temporal_non_iid
  stratify_on: null
  time_on: first_year
  time_unit: years
  time_of: label
  group_on: null
  group_labels: null
  group_time_on: null
  grouping: null
  special_features:
    Chromophore_SMILES: smiles, one column; encoding required; recommended encoding
      rdkit2d-maccs-ecfp4-rdkit2026.03.6-r1
    Solvent_SMILES: smiles, one column; encoding required; recommended encoding rdkit2d-maccs-ecfp4-rdkit2026.03.6-r1
splits:
  n_repeats: 6
  n_folds: 1
  random_state: 4267
  time_horizon: 1
  time_horizon_unit: years
  time_gap: null
  time_gap_unit: null
  n_train:
    min: 8944
    max: 17212
  n_test:
    min: 297
    max: 2040
bundle_checks:
  ok: true
  errors: []
  warnings: []
  infos:
  - dataset_conflicting_duplicate_rows
  - meta_time_horizon_unit
  accepted:
    splits_below_target: 'Accepted by Andrej on 2026-11-24 with the six one-year windows
      2015-2020: 6 windows against the 9 an IID split of 17,509 rows would get; the
      2014 window would train on 44.4% of the rows, under the half-the-rows floor,
      and the one-year length is the curator''s sign-off (splits comment).'
    dataset_smiles_column: 'Accepted by Myunghwan on 2026-11-10 for the 20 gas rows,
      19 since Andrej dropped the betaine dye''s extrapolated gas row on 2026-11-24:
      the gas-state observations have no solvent molecule. Solvent_SMILES is therefore
      absent by definition, with medium_state=gas explicitly retained; these are not
      rows with an unexplained missing molecular input.'
decisions: []
---

# chromophore_optical_properties_db

> Generated from [`dataset.py`](dataset.py) by `dataset check` (or `build`). Do not edit this page: change `dataset.py` and re-run the check.

Regression of `Absorption max (nm)`, scored with `rmse` on temporal splits by `first_year` (one step is a year). 17,509 rows and 3 features. Source: Other (2020).

Built as `01a1c4ae-5ada-74a4-b90e-d5924662a442` on 2026-11-10, but `dataset.py` has changed since: it now gives checksum `v2:723817f8112324dea0515f03fe8f347ca4ca7f57ac735b0f3e48192888166e5b`, so the build is stale. See [Build](#build).

## In brief

**Question.** At what wavelength will a proposed dye have its first absorption peak in a specified environment?

**Use case.** A chemist screens proposed chromophore structures and their solvent or host environments before synthesis and spectroscopy, to choose candidates with useful light absorption.

**One row.** One literature-reported dye and environment measurement with a recorded first absorption-peak wavelength.

**Predicted.** The first absorption-peak position, measured in nanometres, without a target transformation.

**Known at prediction time.** The dye structure and the solvent or host structure, or the source's neat-solid or gas-state designation.

**What the test data stands for.** Each dye is dated by the year of its first paper, and each publication year from 2015 to 2020 is tested on the dyes first reported before it; every environment and measurement of a dye goes with its first year. Solvents may recur across training and testing.

**Our changes to the source.** Use the absorption target alone, omit other measured optical outcomes and provenance identifiers, canonicalize the structures, remove duplicate input-target records, drop the betaine dye's extrapolated gas-phase value and replace random-row splitting with windows by each dye's first publication year (Crossref year of its papers). Decode gas separately from a molecular solvent.

> **Use case fit: approximate (a stand-in with a known gap).** The structures exist before measurement, but literature selection and unrecorded conditions limit transport to new designs; the archive mixes solutions, hosts and neat solids, which a structure alone does not specify. The solvent moves the peak little next to the dye (SD 19.9 nm within a dye, 108.7 nm between dyes; LightGBM RMSE 53.9 nm with the solvent, 54.0 without, on scaffold folds), so scores mostly rank dye-structure models.

## Files in this folder

| file | what it is |
|---|---|
| [`dataset.py`](dataset.py) | The definition, and the only file edited by hand: metadata, reading and cleaning the raw files, feature types and splits. |
| [`README.md`](README.md) | This page, generated by `dataset check` and `dataset build`. |

- The curation record, with the triage decision, its sources and the review: [`curation/records/chromophore_optical_properties_db.md`](../../../../curation/records/chromophore_optical_properties_db.md)
- The original source: <https://doi.org/10.6084/m9.figshare.12045567.v3>
- The collection this folder belongs to: [`tabarena-v0pt2/README.md`](../README.md) and [`tabarena-v0pt2/CHANGELOG.md`](../CHANGELOG.md)

## Rebuild

`dataset.py` reads its raw files from `local-data-warehouse/chromophore_optical_properties_db/`. To get them:

```text
Download the publisher's v3 CSV (file 49887156), not the unversioned search webpage:

mkdir -p local-data-warehouse/chromophore_optical_properties_db/raw
curl -L --fail https://ndownloader.figshare.com/files/49887156 -o local-data-warehouse/chromophore_optical_properties_db/raw/DB_for_chromophore_v3.csv

Publisher MD5: 565dbb010480d94e8bb41af1bfb75ea8. SHA256:
f92a55144c46ca0a0ef063c5ea82996161d65ea5c21643796cdeb897e173994c.
The downloaded CSV has 20,836 rows; the 2020 paper's 20,236 rows describe v2.

Then date each paper once: the Crossref `issued` year of every distinct Reference string, written to
raw/crossref_years.csv (Reference, year; empty where Crossref answers 400 or 404). The build reads this
file and never calls Crossref:

cd local-data-warehouse/chromophore_optical_properties_db
python - <<'EOF'
import csv, json, re, time, urllib.error, urllib.parse, urllib.request
import pandas as pd
def year(ref):
    doi = re.sub(r"^https?://(dx\.)?doi\.org/", "", ref.strip())
    url = "https://api.crossref.org/works/" + urllib.parse.quote(doi, safe="/")
    for attempt in range(6):
        try:
            request = urllib.request.Request(url, headers={"User-Agent": "dataset-curation/0.1"})
            with urllib.request.urlopen(request, timeout=30) as f:
                parts = (json.load(f)["message"].get("issued") or {}).get("date-parts") or [[None]]
            return parts[0][0]
        except urllib.error.HTTPError as e:
            if e.code in (400, 404):
                return None
        except OSError:
            pass
        time.sleep(2**attempt)
    raise RuntimeError(f"Crossref gave no answer for {ref!r}; run again")
refs = sorted(pd.read_csv("raw/DB_for_chromophore_v3.csv")["Reference"].dropna().astype(str).unique())
with open("raw/crossref_years.csv", "w", newline="") as f:
    writer = csv.writer(f, lineterminator="\n")
    writer.writerow(["Reference", "year"])
    writer.writerows((ref, year(ref) or "") for ref in refs)
EOF

Written on 2026-11-24: 1,354 References, 1,240 with a year; SHA256
3c617cb17b159439c95d74415c6643c6c86e34ba6caf23ec6ce42f05e9748c9c (pinned in `_load_raw`). It equals the
table measured on 2026-11-21 except four References Crossref did not answer then (2011, 2011, 2013, 2017
now). A later run that differs fails the pin: Crossref changed a record, and the windows must be checked again.
```

Then, from the repository root:

```bash
.venv/bin/python -m data_foundry.curation.cli dataset check datasets/_dev/tabarena-v0pt2/chromophore_optical_properties_db   # pipeline and checks, no UUID; rewrites this page
.venv/bin/python -m data_foundry.curation.cli dataset build datasets/_dev/tabarena-v0pt2/chromophore_optical_properties_db   # also saves the container and records its UUID
```

Only curators run `build`, when the dataset ships.

## Dataset and task

| field | value |
|---|---|
| source | Other: https://doi.org/10.6084/m9.figshare.12045567.v3 |
| year | 2020 |
| domain | chemistry & material science |
| license | CC BY 4.0 |
| data_tags | Non-IID, Temporal |
| reference | joung2020experimental |
| rows x columns | 17,509 x 5 |
| task.target | Absorption max (nm) |
| task.problem_type | regression |
| task.metric | rmse |
| task.split_regime | temporal_non_iid |
| task.time_on | first_year |
| task.time_unit | years |
| task.time_of | label |

**Metric**

| field | value |
|---|---|
| name | `rmse` (standard; takes value; lower is better) |
| origin | fallback: the default for the problem type: the source defines no metric the task would use in practice |
| definition | sqrt(mean((y - p)^2)) |
| reason | The 2020 Scientific Data descriptor defines no predictive metric. Joung et al. 2021 (https://doi.org/10.1021/jacsau.1c00035) report RMSE and Pearson R-squared and optimize joint standardized MSE over seven targets; a unique absorption-only model-selection metric is not established. Use regression fallback RMSE on the retained absorption wavelengths in nm. |

<details>
<summary>Feature types: 1 categorical, 0 string, 0 datetime, smiles `Chromophore_SMILES`, smiles `Solvent_SMILES`</summary>

- categorical (1): `medium_state`
- string (0): none
- datetime (0): none
- special feature `Chromophore_SMILES`: smiles, one column; encoding required; recommended encoding rdkit2d-maccs-ecfp4-rdkit2026.03.6-r1
- special feature `Solvent_SMILES`: smiles, one column; encoding required; recommended encoding rdkit2d-maccs-ecfp4-rdkit2026.03.6-r1

</details>

<details>
<summary>BibTeX</summary>

```bibtex
@article{joung2020experimental,
  title={Experimental database of optical properties of organic compounds},
  author={Joung, Joonyoung F. and Han, Minhi and Jeong, Minseok and Park, Sungnam},
  journal={Scientific Data},
  volume={7},
  pages={295},
  year={2020},
  doi={10.1038/s41597-020-00634-8}
}
```

</details>

## Sample rows

The first 5 of 17,509 rows of the final frame (the oldest rows: the frame is sorted by `first_year`). Cells are cut at 40 characters.

| Absorption max (nm) | Chromophore_SMILES | Solvent_SMILES | medium_state | first_year |
|---|---|---|---|---|
| 409 | O=C(O)Cn1c2ccccc2c(=O)c2ccccc21 | O | solvent or host | 1967 |
| 351 | O=\[N+\](\[O-\])c1ccc(-c2nc3c(c4c2-c2ccccc2… | Cc1ccccc1 | solvent or host | 1967 |
| 338 | CN(C)c1ccc(-c2nc3c(c4c2-c2ccccc2CC4)-c2… | CCOC(C)=O | solvent or host | 1967 |
| 360 | CCN(CC)c1ccc(-c2nc3c(c4c2-c2ccc(C#N)cc2… | CO | solvent or host | 1967 |
| 534 | CCOC(=O)CCCCCn1c2ccc(Cl)cc2c(=O)c2cc3c(… | CO | solvent or host | 1967 |

## Curation notes

- Prediction point: before synthesizing or measuring a candidate dye in its planned solvent, host or gas
  environment. Only the two structures and decoded medium state enter prediction.
- The publisher's Figshare v3 file contains 20,836 rows and 17,703 nonmissing absorption values. Pin its exact
  bytes rather than reuse the paper's or metadata card's historical counts. Target values stay in nm.
- The v3 source population includes small nonorganic species, metal complexes and structures with up to
  225 nonhydrogen atoms. Its scope is broader than the historical organic/150-atom description. Preserve
  published rows with absorption labels unless an origin-supported correction establishes an error.
- Emission peak, both absorption/emission bandwidth representations, quantum yield, lifetime and extinction
  coefficient are other experimental outcomes, not inputs known at this prediction point. Tag is a row
  number and Reference a source DOI; both leave the inputs. Molecular weight leaves as a structure-derived
  quantity rather than an independent measurement needed by this task.
- Both structures ship as typed SMILES in RDKit's canonical form, with fragments and stereochemistry kept.
  The benchmark encodes them; no descriptor or fingerprint chosen by the curator ships as a raw feature.
- The source uses gas instead of solvent SMILES in 20 labeled rows. Preserve the 19 measured ones:
  medium_state is gas and Solvent_SMILES is missing because there is no solvent molecule. They come from
  papers of 1967-2006 (the 13 with a dated DOI); the small molecules at 128-143 nm (vacuum UV) are
  measurements kept at the margin of the dye use case. The twentieth, at 1,055 nm, is not a measurement
  and is dropped (dye 30 note below). When the source writes the same
  structure for dye and environment it denotes a neat solid; other structures can denote solvent or host.
  The latter state remains solvent or host because the release supplies no independent phase column.
  About 20 rows are doped films in OLED host matrices (such as CBP, mCP or DPEPO in the solvent column);
  the paper uses the solid matrix as the solvent, so they stay solvent or host, mixed with solutions.
- Protonation and charge forms of one molecule (a merocyanine as phenol or phenolate/quinoid form, an
  oxime or its oximate, an acid or its anion) are distinct species with different wavelengths. They are
  separate dyes and may get different first years; aliases of one species share one.
- Remove exact repeated model-input and target records after canonicalization. Distinct observed wavelengths
  for one dye/environment remain separate measurements: laboratory conditions and literature disagreement
  may reflect physical-condition variation or literature/transcription disagreement; this cause is not verified.
  No averaging or target-dependent conflict filtering is invented.
- Input/target deduplication removes 193 labeled records (17,509 rows remain after the gas row below). Only 50 excess labeled rows also match every raw
  field except Tag; the other 143 removals are a weighting policy, not proven copies of physical experiments.
  Myunghwan approved that weighting on 2026-11-10 separately from retaining differing wavelengths.
- Split by first publication year (Andrej, 2026-11-24): each dye (structure without stereochemistry,
  aliases with one nonempty InChIKey or one canonical tautomer joined) takes the earliest Crossref year over
  the papers of all its labeled rows, deduplicated ones included, and every row of the dye goes with that
  year (`first_year`, which orders and splits the rows and is no input). 6,367 of 6,498 dyes (98.0%;
  98.9% of rows) have a dated paper; the other 131 dyes (194 rows) take the earliest year, 1967, so they
  always train. The alias join moves 5 dyes (30 rows) to an alias's earlier year. The year is the
  literature entry, not the catalogue entry, as for apistox. Measured on 2026-11-21 with this dating
  (before the dedup-inclusive and alias refinements), the forward split leaves 4.8-8.9% of test dyes a
  close training analogue (Morgan radius 2, Tanimoto at least 0.7) against 58.3-63.1% for a random draw of
  the same number of dyes, and 0-11% of test rows a row of their own paper in training, against 58-65%
  under the former scaffold folds. Solvents recur; the test stands for the dyes the literature reports
  next, not new solvents.
- The source paper compiles experimental values, not simulated quantum-chemistry labels. Most were read from
  the spectra of the cited papers; the 335 rows of Reichardt's betaine dye 30 (334 shipped) come from one
  review's ET(30) table instead (next note). Its model follow-up (JACS Au 2021, doi:10.1021/jacsau.1c00035)
  reports RMSE for absorption peak positions in nm. Its random-row scores and expanded database are not
  qualification results for our temporal release.
- Reichardt's betaine dye 30 had 335 rows, all citing Reichardt, Chem. Rev. 1994 (doi:10.1021/cr00032a005).
  334 of them equal 28591/ET(30). ET(30) is defined from this dye's measured long-wavelength
  charge-transfer peak in kcal/mol, so these rows are measured peaks converted back to nm, rounded to the
  table's 0.1 kcal/mol (0.2-1.6 nm). Whether every tabulated solvent value was measured on dye 30 itself
  or derived from a secondary standard is unverified. The gas row (1,055 nm, ET(30) = 27.1), the scale's
  extrapolated gas-phase value, is dropped (Andrej, 2026-11-24); 334 rows of the dye remain, all first
  dated 1994, so the dye always trains.
- Literature selection and missing temperature, concentration and some physical-state detail remain limits;
  no row is removed simply for an extreme wavelength. The 17,703 observed targets are positive and finite.
- Curator decision (2026-11-10, Myunghwan), issues 1A and 2A: keep one row per canonical input and wavelength,
  and retain the 61 input sets with differing published responses. Apply the genuine-ambiguity clause for
  continuous measurements under incomplete conditions; the cause of each disagreement remains unverified.
  Grouping does not validate labels. Repair any later demonstrated source error from its original reference.
- Myunghwan checked the declared fallback RMSE in untransformed nm and accepted the gas/no-solvent warning
  on 2026-11-10. These are scientific review decisions; no model-only gas accuracy claim follows.
- Split walk (the split decision tree, SPLIT-36, from the record's collection type Expanding Science Catalogue): [CAT.next-items] the source aims at newly designed chromophores before synthesis, the items the catalogue adds next: yes → [CAT.entry-date] each dye is dated by the earliest Crossref year of its papers (98.0% of dyes), and the record has no `Target: Revised Later`: yes → [CAT.arrival] a forward split by that year leaves clearly fewer close training analogues than a random draw (4.8-8.9% against 58.3-63.1% of test dyes at Tanimoto 0.7): yes → [CAT.windows] one-year windows 2015 to 2020 each train on at least half the rows (51.1-98.3%): yes → leaf L-CAT.entry-date, Temporal · entry date, the split the definition ships (`split_leaf`; Andrej, 2026-11-24, issue 3 B and the Horizon B).

## Splits

Expanding windows on each dye's first publication year (`first_year`, no input), leaf L-CAT.entry-date of
the split tree: six one-year test windows, 2020 back to 2015, newest first, no gap (a published label is
final when its paper appears); training is every dye first published before the test year. Test windows
(year: rows, dyes, train share): 2020: 297, 97, 98.3%; 2019: 2,040, 784, 86.7%; 2018: 1,959, 709, 75.5%;
2017: 1,443, 535, 67.2%; 2016: 1,611, 437, 58.0%; 2015: 1,215, 423, 51.1%. The one-year length is the
finest step the year gives, and the curator signed it off (Andrej, 2026-11-24); the use case sets no
other. SPLIT-33's target is 9 splits for 17,509 rows; 6 are reached, because the 2014 window would train
on 44.4% of the rows, under the half-the-rows floor. The 131 undated dyes (194 rows) train in every
window; without them 2015 still trains on 50.5%. All rows of a dye stay in one window.

6 repeat(s) x 1 fold(s) with seed 4267; train 8,944 to 17,212 rows, test 297 to 2,040 rows. Prediction horizon: 1 years. The time column `first_year` dates the label, which arrives after the prediction point: it orders and splits the rows, so every training label was known at its window's start, and is no model input (`feature_columns(container)` leaves it out).

| repeat | fold | n_train | n_test | train_start | train_end | test_start | test_end |
|---|---|---|---|---|---|---|---|
| 0 | 0 | 17212 | 297 | 1967 | 2019 | 2020 | 2020 |
| 1 | 0 | 15172 | 2040 | 1967 | 2018 | 2019 | 2019 |
| 2 | 0 | 13213 | 1959 | 1967 | 2017 | 2018 | 2018 |
| 3 | 0 | 11770 | 1443 | 1967 | 2016 | 2017 | 2017 |
| 4 | 0 | 10159 | 1611 | 1967 | 2015 | 2016 | 2016 |
| 5 | 0 | 8944 | 1215 | 1967 | 2014 | 2015 | 2015 |


### The test windows

Each test window against its train side, by statistics of the data, never of a model: the target, and the population stability index (PSI) of each feature, its largest value and the features that drift most (below 0.1 little shift, above 0.25 a large one), and the share of test rows with a category the train side never shows. Up to 20,000 rows per side. The candidates the windows were chosen from: `.venv/bin/python -m data_foundry.curation.cli dataset windows chromophore_optical_properties_db`.

| window | period | n_test | train_share | target_test | target_train | psi_max | top_drift | unseen_categories |
|---|---|---|---|---|---|---|---|---|
| 0 | 2020 - 2020 (years) | 297 | 0.983 | mean 402.8, median 365, p10 331, p90 636.4 | mean 427.7, median 398, p10 326, p90 583 | 0.016 | medium_state (0.02) | 0 |
| 1 | 2019 - 2019 (years) | 2040 | 0.867 | mean 429.7, median 396, p10 334, p90 581 | mean 427.5, median 398, p10 325, p90 584 | 0.014 | medium_state (0.01) | 0 |
| 2 | 2018 - 2018 (years) | 1959 | 0.755 | mean 422, median 403, p10 341, p90 535.2 | mean 428.3, median 397, p10 323, p90 593 | 0.011 | medium_state (0.01) | 0 |
| 3 | 2017 - 2017 (years) | 1443 | 0.672 | mean 420.2, median 389, p10 325, p90 546.8 | mean 429.3, median 397.7, p10 322, p90 596 | 0.017 | medium_state (0.02) | 0 |
| 4 | 2016 - 2016 (years) | 1611 | 0.58 | mean 425.7, median 399, p10 324, p90 591 | mean 429.8, median 397, p10 321, p90 598 | 0.009 | medium_state (0.01) | 0 |
| 5 | 2015 - 2015 (years) | 1215 | 0.511 | mean 424.3, median 396, p10 326, p90 584.1 | mean 430.6, median 397.1, p10 321, p90 602 | 0.013 | medium_state (0.01) | 0 |

## Bundle checks

0 error(s), 0 warning(s), 2 info (28 checks run, plus the dataset's own checks).

- **info** `dataset_conflicting_duplicate_rows`: 63 row(s) (0.4%) share all features with another row but carry a different target. (hint: Either the rows differ in a dropped column, or the label is noisy — this caps the achievable score.)
- **info** `meta_time_horizon_unit`: `time_horizon_unit='years'` implies calendar time, but `time_on='first_year'` has dtype int64, so the horizon cannot be cross-checked. (hint: Fine when the numeric values themselves are calendar units (e.g. a year column); otherwise use `time_horizon_unit='steps'` for a plain numeric time index.)

Accepted on purpose:

- `splits_below_target`: Accepted by Andrej on 2026-11-24 with the six one-year windows 2015-2020: 6 windows against the 9 an IID split of 17,509 rows would get; the 2014 window would train on 44.4% of the rows, under the half-the-rows floor, and the one-year length is the curator's sign-off (splits comment).
- `dataset_smiles_column`: Accepted by Myunghwan on 2026-11-10 for the 20 gas rows, 19 since Andrej dropped the betaine dye's extrapolated gas row on 2026-11-24: the gas-state observations have no solvent molecule. Solvent_SMILES is therefore absent by definition, with medium_state=gas explicitly retained; these are not rows with an unexplained missing molecular input.

## Data checks

### Feature summary

| index | dtype | n_missing | pct_missing | n_unique | examples |
|---|---|---|---|---|---|
| medium_state | category | 0 | 0 | 3 | solvent or host, neat solid, gas |
| Absorption max (nm) | float64 | 0 | 0 | 1681 | 360.0, 340.0, 350.0, 364.0, 366.0, 341.0, 368.0, 370.0, 362.0, 343.0 |
| first_year | int64 | 0 | 0 | 38 | 2019, 2018, 2016, 2017, 2015, 2014, 2012, 2013, 2011, 2009 |
| Solvent_SMILES | string | 19 | 0.11 | 729 | ClCCl, CC#N, Cc1ccccc1, C1CCOC1, ClC(Cl)Cl, CO, CCO, CS(C)=O, C1CCCCC1, CN(C)C=O |
| Chromophore_SMILES | string | 0 | 0 | 6498 | \[O-\]c1c(-c2ccccc2)cc(-\[n+\]2c(-c3ccccc3)cc(-c3ccccc3)cc2-c2ccccc2)cc1-c1ccccc1, … |

### Target distribution

| index | y_missing_count | non_positive_pct | skew_y | skew_log | var_y | var_log | log_used | aic_exponential | aic_lognormal | dist_hint |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 1.24 | 0.586 | 11258.4 | 0.053 | log | 249635 | 227220 | lognormal |

### Numeric features

| index | count | mean | std | min | max |
|---|---|---|---|---|---|
| Absorption max (nm) | 17509 | 427.311 | 106.105 | 127.7 | 931.303 |
| first_year | 17509 | 2011.77 | 8.41014 | 1967 | 2020 |

### Categorical features

<details>
<summary>Show the table (13 rows)</summary>

| column | rank | value | count | pct |
|---|---|---|---|---|
| Chromophore_SMILES | 1 | \[O-\]c1c(-c2ccccc2)cc(-\[n+\]2c(-c3ccccc3)cc(-c3ccccc3)cc2-c2ccccc2... | 334 | 1.91 |
| Chromophore_SMILES | 2 | COC(=O)C(Cc1ccc2oc(-c3ccc(Nc4ccccc4)cc3)nc2c1)NC(=O)OC(C)(C)C | 36 | 0.21 |
| Chromophore_SMILES | 3 | COC(=O)C(Cc1ccc2oc(-c3ccc(N(C)C)cc3)nc2c1)NC(=O)OC(C)(C)C | 36 | 0.21 |
| Chromophore_SMILES | 4 | COC(=O)C(Cc1ccc2oc(-c3ccc4c(c3)c3ccccc3n4-c3ccccc3)nc2c1)NC(=O)O... | 36 | 0.21 |
| Chromophore_SMILES | 5 | COC(=O)C(Cc1ccc2oc(-c3ccc(N(C)c4ccccc4)cc3)nc2c1)NC(=O)OC(C)(C)C | 35 | 0.2 |
| Solvent_SMILES | 1 | ClCCl | 2461 | 14.06 |
| Solvent_SMILES | 2 | CC#N | 1828 | 10.44 |
| Solvent_SMILES | 3 | Cc1ccccc1 | 1386 | 7.92 |
| Solvent_SMILES | 4 | C1CCOC1 | 1258 | 7.18 |
| Solvent_SMILES | 5 | ClC(Cl)Cl | 1228 | 7.01 |
| medium_state | 1 | solvent or host | 17121 | 97.78 |
| medium_state | 2 | neat solid | 369 | 2.11 |
| medium_state | 3 | gas | 19 | 0.11 |

</details>

## Build

| field | value |
|---|---|
| uuid | 01a1c4ae-5ada-74a4-b90e-d5924662a442 |
| checksum | v2:97decdfc67653a344bdbc617300599730e279e24d81cdd2d821e68525f89ccb2 |
| built_at | 2026-11-10T08:58:44+00:00 |
| path | chromophore_optical_properties_db/01a1c4ae-5ada-74a4-b90e-d5924662a442 |
| data_foundry_version | 0.0.5 |
| git_sha | 8a50be6ccb71d6b8fb77047ba7603028dd37e596 |
| libraries | {'python': '3.12.3', 'pandas': '3.1.0', 'numpy': '2.5.4', 'pyarrow': '26.0.0', 'scikit-learn': '1.7.2', 'polars': '2.0.0'} |
| stale | yes: the definition now gives checksum `v2:723817f8112324dea0515f03fe8f347ca4ca7f57ac735b0f3e48192888166e5b` |
