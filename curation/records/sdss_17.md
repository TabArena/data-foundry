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
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

The data consists of 100,000 observations of space taken by the SDSS (Sloan Digital Sky Survey). Every observation is described by 17 feature columns and 1 class column which identifies it to be either a star, galaxy or quasar. Spatial correlations. Might require spatial/temporal split. Sounds like a pretty cool task. Might have spatial information with alpha and delta

Potential issue: -

Lennart: Likely impact of time can be ingored and all features are time invariant as far as I can tell. Spatial impact might be ignorable as well, or remove these features

Andrej: Possibly license issues

## Reference

fedesoriano. (January 2022). Stellar Classification Dataset - SDSS17. Retrieved [Date Retrieved] from https://www.kaggle.com/fedesoriano/stellar-classification-dataset-sdss17.
