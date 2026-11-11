---
unique_name: sdss_17
name: SDSS17
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
- WIP (DF)
claimed_by: Andrej
suggestion: 'Yes'
priority: 3
decision_markers:
- Selection Bias
tags:
- Non-IID (Temporal)
- 'Samples: Over Time'
- 'Time: Dated'
- 'Target: Varying Delay'
original_source: Other
year: '2021'
required_split:
- Temporal (NON-IID)
source_links:
- https://www.kaggle.com/datasets/fedesoriano/stellar-classification-dataset-sdss17
notebook_path: datasets/beyond_iid/old_iid/sdss_17/sdss_17.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/sdss_17/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

The data consists of 100,000 observations of space taken by the SDSS (Sloan Digital Sky Survey). Every observation is described by 17 feature columns and 1 class column which identifies it to be either a star, galaxy or quasar. Spatial correlations. Might require spatial/temporal split. Sounds like a pretty cool task. Might have spatial information with alpha and delta

Potential issue: -

Lennart: Likely impact of time can be ingored and all features are time invariant as far as I can tell. Spatial impact might be ignorable as well, or remove these features

Andrej: Possibly license issues

CC (2026-10-01, Lennart): Leak audit fixes (v2 definition), now a photometric task (position + u, g, r, i, z + cam_col):
- Dropped `redshift`: the SDSS pipeline fits class and redshift in one step and stars are only fitted within +-1200 km/s (Bolton et al. 2012, Sec. 3.1), so |redshift| <= 0.0041 marks stars almost perfectly.
- Dropped `plate` and `fiber_ID`: a plate is one spectroscopic pointing (6,284 plates vs 6,352 plate-MJD pairs, so it duplicates the already dropped MJD) designed for one targeting program; it encodes how the object was pre-selected from photometry, not what it is. 11% of rows sit on plates that are >= 99% one class (5,860 galaxy and 5,428 star rows), and plate + fiber alone give OvR AUC 0.80. A new object has no plate before it is targeted, and the fiber is only a slot on the plate. Adding both to the photometry also hurts LightGBM (log loss 0.334 -> 0.404, high-cardinality overfit); grouping folds by plate does not change the photometry-only score (0.340), so the split stays IID.
- Deduplication by sky position instead of `obj_ID`: the Kaggle CSV stores obj_ID as a rounded float, so `drop_duplicates(obj_ID)` had removed 21,947 distinct objects (78,053 -> now 99,999 rows); by position there is one object observed on two plates.
- The sentinel -9999 (one row in u, g, z) is set to missing.
Photometric LightGBM: log loss about 0.33, OvR AUC about 0.96.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback log_loss — SDSS DR17 (Abdurro'uf et al. 2022) is a data release with no prediction task or metric; the Kaggle 'Stellar Classification Dataset - SDSS17' is a dataset page, not a competition, with no evaluation metric. Our task (photometric classification, redshift/plate/fiber dropped) also differs from the SDSS pipeline's spectroscopic classification.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): codes shipped as numbers, left for the curator's review: `cam_col`.

CC (2026-10-31, Lennart): marks on the review board of PR #37 (ordinal scales in the codebook's order, also when shipped as numbers; a state outside a scale missing when the column has no other missing value, else the lowest level; cycles ordered; codes shipped as numbers as categories): cam_col a category.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `desi_dr1_star_galaxy_quasar` (TBD -> Yes, priority 3). Each is screened in its own record; this record's verdict stays the curator's.

**Assessment (AI, 2026-11-04):** reviewed for the BeyondArena v0.2 review page, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the folder's `REVIEW.md`. Ship as defined: a photometric star/galaxy/quasar task from public-domain SDSS DR17 with the spectroscopic leaks dropped and the selection marked. Priority 3: gap 1, use case 0, source 1, shape 1, risk -1.

CC (2026-11-11, Andrej): split by the year of the spectrum instead of at random, and the collection facts corrected (review page, issues 2, 4 and 5):
- Split: nine one-year windows, 2012 to 2020, newest first, each trained on every spectrum taken before it (51.3% to 99.9% of the 99,999 objects; 141 to 11,044 test spectra). Every row is a spectrum taken on a dated night through a plate drilled for one targeting programme, and the programmes changed what they observed (quasars 3-11% of each year's spectra in 2000-2009, 14-16% in 2010-2013, 31-46% from 2014 on). A classifier in use is trained on the spectra taken so far and labels objects the survey has not yet observed, so it has neither the test object's plate-mates nor the later programmes, which the random split gave it. The raw `MJD` returns as the time column `date`, never as a feature of its own right; `required_split` is Temporal (NON-IID).
- Measured (log loss, lower is better; untuned LightGBM on the shipped features): 0.331 random, 0.338 by plate, 0.354 by sky cell of 10 degrees, 0.506 by year. On the same rows, the 48,743 spectra of 2012-2020, 0.391 random against 0.506 by year; trained on a random draw of the other years instead of the earlier ones, the loss on 2014 falls from 0.530 to 0.470 and on 2016 from 0.501 to 0.444. The sky position lowers the random score (0.353 -> 0.331) and raises the year score (0.491 -> 0.506): it teaches the sky footprints of past programmes. Under the year split TabPFN 3.5 scores 0.439 and logistic regression 0.755, against the class shares at 1.121.
- Window sizes: the 2019 and 2020 windows hold 935 and 141 spectra, both above the 50 test rows below which windows are widened, and nine windows is what a task of this size gets as folds; 0 to 5 plates per window were also observed before it, at most 90 test rows (0.9% of the 2013 window).
- No time basis: a temporal split carries no time-basis tag, so neither `Timeless` nor any other is set (issue 4, option B).
- Collection facts (issue 5, option C): `Samples: Over Time` and `Time: Dated` in place of `Samples: No Time Dimension` — the spectra arose over 2000 to 2020, each on a dated night — plus `Target: Varying Delay`: the class comes with a spectrum taken after the imaging, by a delay that differs from object to object.

## Reference

fedesoriano. (January 2022). Stellar Classification Dataset - SDSS17. Retrieved [Date Retrieved] from https://www.kaggle.com/fedesoriano/stellar-classification-dataset-sdss17.
