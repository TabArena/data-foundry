---
unique_name: heloc
name: heloc
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: 'Yes'
original_source: Other
year: '2018'
required_split:
- Random (IID)
source_links:
- https://www.kaggle.com/datasets/averkiyoliabev/home-equity-line-of-creditheloc
notebook_path: datasets/beyond_iid/old_iid/heloc/heloc.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/heloc/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Default prediction

Potential issue: preprocessing

Lennart: Likely include a version of the original data; likely time invariant

Andrej: Use the most extensive data version

**Assessment (AI, 2026-10-19):** open since the leak audit of 2026-10-01 (no leak): 588 rows are -9 in every feature, the source's code for no bureau record; the open `dataset_missing_value_sentinel` warning comes from them. To decide in the next pass: keep them as applicants without a credit file (the real population) or drop them as empty records, and say which in the notes.

## Reference

https://www.kaggle.com/datasets/averkiyoliabev/home-equity-line-of-creditheloc
