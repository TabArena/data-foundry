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
suggestion: 'Yes'
original_source: Kaggle
year: '2022'
required_split:
- Random (IID)
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

## Reference

fedesoriano. (January 2022). Stellar Classification Dataset - SDSS17. Retrieved [Date Retrieved] from https://www.kaggle.com/fedesoriano/stellar-classification-dataset-sdss17.
