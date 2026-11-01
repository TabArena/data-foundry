---
unique_name: happy_teddy_sdss_photo_z
name: Happy and Teddy photometric-redshift catalogues (SDSS DR12)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
decision_markers:
- Selection Bias
tags:
- AI-Filled (Verify)
original_source: Github
year: '2017'
domain: physics & astronomy
problem_type: Regression
source_links:
- https://doi.org/10.1093/mnras/stx687
- https://github.com/COINtoolbox/photoz_catalogues
- https://arxiv.org/abs/1701.08748
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: photometric redshift of SDSS galaxies, an astronomy regression (a domain with no accepted dataset), from a paper that built it as a photo-z benchmark; only five inputs, and its test sets are designed shifts.
- Source: Beck, Lin, Ishida, Gieseke, de Souza, Costa-Duarte, Hattab, Krone-Martins (COIN), "On the realistic validation of photometric redshifts", MNRAS 468:4323-4339 (2017), arXiv 1701.08748; data at github.com/COINtoolbox/photoz_catalogues (GPL-3.0). As published (paper Table 1): Teddy A/B/C/D 74,309 / 74,557 / 97,980 / 75,924 and Happy A/B/C/D 74,950 / 74,900 / 60,315 / 74,642 galaxies. ML files `id mag_r u-g g-r r-i i-z z_spec feat1..feat5` (feat = the five inputs standardised on set A); template files with dereddened ugriz magnitudes, their errors and the redshift error; density-ratio weight files for B-D (repository READMEs). All objects are real SDSS DR12 objects: Teddy A and B split a colour-box selection of about 150,000 DR12 spectroscopic objects, and the paper says "the colour and magnitude distributions in Teddy are not realistic" (Sec. 2.1); Happy extends DR12 spectroscopy by cross-matches with nine surveys (GAMA, WiggleZ, PRIMUS, VIPERS and others) and draws C and D as nearest neighbours of photometric-sample objects in that set (Sec. 2.2).
- Use case: a survey pipeline (the paper's "future large scale surveys") assigns a redshift from five-band photometry to galaxies without a spectrum; fit direct for A/B within the spectroscopic coverage, while the targets of the use case lie partly outside it (the paper's point; `Selection Bias` as on `sdss_17`: objects picked for a spectrum, the use case predicts for the others). Regime IID on A+B (A "was randomly drawn from the SDSS DR12 spectroscopic sample", B "the same as Teddy A"); the shifted C and D sets are a prescribed covariate-shift test that our regimes do not cover (SPLIT-5: a prescribed split is a claim).
- Siblings and duplicates: `sdss_17` (`Yes`, `Selection Bias`: star, galaxy or quasar from SDSS photometry, another task of the same survey, PROV-7); `desi_bgs_photometric_redshift` (a candidate of this run: the same photo-z task on DESI spectra and Legacy Surveys photometry, another source, so not a duplicate under PROV-4, though the curator may want one photo-z task); `first_principles_hubble` (`No`, AHDS). External collections: none found.
- Better data: from the gap scout for physics and astronomy, a related task next to `first_principles_hubble`; no further search this round.
- Papers and pages: Beck et al. 2017 (Sec. 2 construction, Sec. 4 evaluation of ML and template-fitting methods); the per-catalogue READMEs of the repository.
- Metric: the paper scores the normalised error (z_spec - z_phot)/(1 + z_spec) by its mean and standard deviation without outliers, its median absolute deviation, and the outlier rate (above 0.15) side by side (Sec. 4.1), with no single ranked criterion; so the regression fallback `rmse` (MET-5, MET-8). The field's normalisation by 1 + z is noted for the curator (it would be a custom metric, MET-13). Inputs none.
- Risks for /add-dataset: five numeric inputs (r magnitude and four colours, all from the same five magnitudes), the photometric errors only in the template files; `feat1..feat5` are standardised copies of the inputs, fit on set A (drop them, CLEAN; LEAK-30 if kept); the catalogue is a 75,000-object cut of about 2 million DR12 spectroscopic objects (PROV-6, a cut: the curator may prefer to build from SDSS directly or take the DESI record); which catalogue (Teddy or Happy) and which subsets ship.
- Priority: gap + (physics & astronomy has no accepted dataset), use case + (the paper names the survey use), source + (an MNRAS paper documents the construction, with a repository), shape 0 (about 75,000 rows per subset, but five numeric inputs of one kind), risk - (a cut of a much larger public sample, with designed shifts in place of a natural split).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through a related task next to `first_principles_hubble`; the gap scout for physics and astronomy.
- as published: Galaxies with SDSS DR12 photometry and spectroscopic redshift: Happy A-D and Teddy A-D, each subsample roughly 75,000 galaxies (files 7-13 MB; exact rows to verify); columns r magnitude, four ...; target: Spectroscopic redshift z_spec (regression); access: open.
- Why: A paper-defined photo-z benchmark built for ML with a realistic mismatch between training and target samples; public | The real-data task behind the Hubble record's target: a galaxy's recession velocity (redshift) estimated from cheap observables, done today at survey scale; the Hubble law itself (velocity from ...
- Adds: Astronomy regression with a designed covariate shift (train A, test C or D). Risks: only five features; same survey as sdss_17 (a different task, PROV-7); the subsets are resampled from SDSS to mimic distributions; GPL-3.0 | Same hit as gap_physics_astronomy (happy_teddy_sdss_photo_z); listed here only to link it to ...
