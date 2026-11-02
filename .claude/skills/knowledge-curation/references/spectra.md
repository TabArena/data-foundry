# Spectrum datasets

A guide for datasets whose rows hold a spectrum: mass spectra (MALDI-TOF, SELDI-TOF), Raman, infrared and
near-infrared spectra. It adds no rules of its own. The rules live in their part files and are cited by ID here
(CLEAN-26, SEL-12, SEL-15, SPLIT-23, SPLIT-29, SPLIT-30). This file collects what a curator needs to apply them to
spectra: the background, what ships, the encodings and their evidence, and the pitfalls. The last section says where
Data Foundry implements each part.

Read it when screening or adding a dataset whose features are intensities along an axis (m/z, wavenumber, wavelength),
or bins numbered along one.

## The background in brief

* **Mass spectra** (MALDI-TOF, SELDI-TOF) give an intensity (an ion count) per mass-to-charge ratio, m/z. A raw
  spectrum carries a baseline that falls with m/z, noise, and an intensity scale of its own, which differs from shot
  to shot and from spot to spot. Peaks shift slightly between spectra (calibration).
* **Vibrational spectra** (Raman, infrared, near-infrared) give an intensity, an absorbance or a reflectance per Raman
  shift or wavenumber (cm-1) or per wavelength (nm). Raman spectra carry a fluorescence baseline and the odd cosmic-ray
  spike; near-infrared spectra are broad overlapping bands where scatter shifts and tilts the whole spectrum.
* **What the source did** decides what the data is:
  * `raw`: the instrument's values as read, with their baseline and scale (pancreatic_cancer_mouse_detection);
  * `processed`: a baseline removed, a normalisation or a derivative applied by the source;
  * `peaks`: peaks detected and put on fixed bins, often by the instrument's software (micro_mass: the VITEK MS
    routine algorithm's 1,300 bins).
* **Binning.** Many sources put every spectrum on one grid (pancreatic: bins of 400 ppm from m/z 800 to 11,993), so the
  columns line up. A spectrum at the instrument's own resolution has tens of thousands of points.
* **Replicates.** A sample is often measured several times (spots, shots, map points, days): technical replicates of
  one specimen, strain or patient, much closer to each other than to anything new.

## What ships (CLEAN-26)

* The spectrum as the source publishes it: one numeric column per position, the whole range, in the source's state.
  Do not smooth, correct the baseline, normalise, take derivatives or align in `_clean`: each has free choices, and the
  benchmark applies one default to every method (and lets a method switch it off).
* Name the columns `<prefix><position>` (`M/Z:800.32`, `cm_1001.5`) so the build reads the axis from the names. When
  the source gives the axis in a separate file, build the names from it. When it gives no axis, number the bins
  (`unit="bin"`, micro_mass).
* Declare the spectrum in `special_features` as a group of columns, `Spectrum(name=..., prefix=..., unit=...,
  technique=..., state=...)`. The container records it as a special feature of kind `spectrum`: the columns in axis
  order, their positions, the unit, the technique, the state and the recommended encoding.
* Dropping bins that are constant or copy another bin is fine (micro_mass: 1,300 to 1,082); the recorded axis keeps the
  positions of the bins that remain. Cutting a range off is a modelling choice: keep what the source publishes.
* Spectra from instruments with different grids need one grid. Prefer the source's own common grid; an interpolation
  in `_clean` is a decision for the curation notes.

## Splits (SPLIT-23, SPLIT-29, SPLIT-30)

* Replicate spectra of one specimen, strain, mouse or patient are one group: hold the group out (pancreatic: by mouse;
  micro_mass: by strain; MLROD's map points by specimen). Each spectrum can still be one prediction (SPLIT-23).
* Measurement batches (a plate, a day, an instrument) can separate classes on their own: a hidden-group probe hit is a
  question (SPLIT-30). pancreatic's file marker `t` separates some control spectra at AUC 0.67 and is open with the
  authors.

## Encodings and their evidence

Every encoding works on one spectrum at a time, with no fitting and no labels, so it cannot leak and gives each row the
same values in every split. The defaults follow the field's published workflows, never a tuning on our folds.

| Spectrum | Recommended (spec id) | Steps |
|---|---|---|
| mass, `raw` | `ms-sqrt-sg21-snip100-tic-r1` | MALDIquant's vignette (Gibb and Strimmer 2012): square root, Savitzky-Golay over 21 points (order 3), SNIP baseline (100 iterations) removed, divided by the total ion current |
| mass, `raw`, candidates to compare | `ms-driams-sqrt-sg21-snip20-snip100-tic-r1` | DRIAMS's settings (Weis et al. 2022): as above, the SNIP baseline removed twice (20, then 100 iterations) |
| | `ms-cromwell-udwt-mm-tic-log2-r1` | Cromwell's wavelet denoising and monotone-minimum baseline (Coombes et al. 2005), then the total ion current and log2 (the Cromwell and Ciphergen pipelines, Wegdam et al. 2009) |
| mass, `peaks` or `processed` | `spectrum-as-is-r1` | none: the source already processed it |
| vibrational (Raman, infrared, near-infrared) | `spectrum-as-is-r1`, and check `vib-als-snv-r1` | RamanBench's linear-model default: asymmetric least squares baseline (lambda 1e5, p 0.01, 10 iterations), then the standard normal variate |

MALDIquant's later steps (aligning spectra on common peaks, detecting peaks and binning them across spectra) fit across
spectra, so they are no per-row default.

* **Raw mass spectra need the processing.** pancreatic_cancer_mouse_detection, the 60 shipped splits by mouse, ROC AUC
  (2026-11-02):

  | Model | Raw bins | MALDIquant (recommended) | PR #21's chain, reconstructed |
  |---|---|---|---|
  | HistGradientBoosting | 0.585 | 0.685 (55/60) | 0.642 |
  | LightGBM | 0.577 | 0.676 (53/60) | 0.649 |
  | Random forest | 0.536 | 0.681 (60/60) | 0.657 |
  | PLS-DA, 5 components | 0.635 | 0.691 (47/60) | 0.713 |
  | Logistic regression | 0.663 | 0.646 (26/60) | 0.708 |
  | TabPFN v3.5 | 0.659 | 0.690 (44/60) | 0.716 |

  In parentheses the splits on which the encoding beats the raw bins. PR #21's chain (smoothing over 11 bins, a
  rolling-minimum baseline, division by the total, a log) is reconstructed: the PR names no polynomial order or
  rolling window (order 2 and 101 bins here). It beats MALDIquant's steps for TabPFN (on 44 of 60 splits) and the
  linear models, likely through its log; MALDIquant's steps suit the trees better. PR #21 measured TabPFN 3.5 at 0.656
  raw and 0.733 processed on its own 12 folds. On these binned spectra the DRIAMS and Cromwell candidates trail
  MALDIquant's steps for every CPU model (0.59 to 0.66).
* **The raw mass-spectrum default is the benchmark's choice.** The comparison studies find no pipeline that wins
  everywhere (Cruz-Marcelo et al. 2008; Wegdam et al. 2009: "the settings for pre-processing parameters lead to large
  differences in classification accuracy"). There are two published traditions, the square root (MALDIquant, DRIAMS)
  and the log (Cromwell, Ciphergen, and PR #21's chain). MALDIquant's steps stay the placeholder until the benchmark
  compares the three registered candidates on every raw mass-spectrum dataset and three model families, by a rule
  fixed in advance (`BENCHMARK_CHANGES_TODO.md`, "Spectra").
* **Vibrational spectra may not.** RamanBench (arXiv:2605.02003, 77 datasets, 325,862 spectra): the leading methods
  (AutoGluon 1.5, then TabPFN v2.5 and TabICL v2) read the raw spectra; the baseline and SNV were the chemometric
  baselines' convention (PLS: smoothing, baseline and SNV; the linear model: baseline and SNV; kNN: SNV). No foundation
  model or tree was tested on processed spectra, so check both encodings on the first such datasets we add.
* **Width.** The encodings keep every bin (pancreatic: 6,771 columns). Averaging adjacent bins costs little (PR #21:
  TabPFN 0.733 against 0.725 with 8-bin averages), but the width is left to the benchmark's feature-limit step.

## Pitfalls

* A spectrum bin of 999 is a reading, not a missing-value code: the sentinel check skips declared spectra.
* A spectrum with a missing value cannot be smoothed: the processing encodings return it missing, and the bundle check
  warns.
* A source's "binned" or "preprocessed" can mean a peak list or a corrected profile: read the documentation and set the
  state from it (micro_mass's README: "pre-processed by the standard algorithm used for routine (culture-based)
  bacterial identification, which provided a peak-list representation").
* A raw spectrum can have negative intensities (an instrument offset); MALDIquant's square root counts them as 0.

## In Data Foundry

* `special_features = (Spectrum(name=..., prefix=..., unit=..., technique=..., state=..., description=...),)` on the
  definition (`data_foundry.v2.Spectrum`, a special feature in a group of columns); leave the columns out of
  `_feature_types`. The build records each as a `SpecialFeature` of kind `spectrum` (layout `group`, with
  `SpectrumDetails`) in `task_metadata.special_features`, with the recommended encoding's spec id.
* `special_features(container, "spectrum")` (`data_foundry.curation_container`) lists them;
  `encode_special_feature(df, feature)` (`data_foundry.v2.special`) encodes one in place of its columns, and
  `encodings_for(feature)` gives its candidates, the recommended one first. `encode_spectrum(frame, axis, encoding)`
  (`data_foundry.v2.spectra`) is the encoder underneath.
* The bundle check `dataset_spectrum`: the columns are numeric and finite; missing values are a warning.
* The probes see a spectrum in its recommended encoding; the blind reviewer's clean room sees it as shipped
  ([checks_and_probes.md](../../knowledge-data-foundry/references/checks_and_probes.md)).
* What TabArena still has to do: `datasets/_dev/tabarena-v0pt2/BENCHMARK_CHANGES_TODO.md`, "Spectra".
