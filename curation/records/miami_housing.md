---
unique_name: miami_housing
name: miami_housing
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: 'Yes'
original_source: OpenML
year: '2021'
required_split:
- Random (IID)
source_links:
- https://www.openml.org/search?type=data&id=43093&sort=runs&status=active
- https://www.openml.org/search?type=data&id=44983
notebook_path: datasets/beyond_iid/old_iid/miami_housing/miami_housing.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/miami_housing/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

housing datasets with a lot of spatial information but all within one yea

Potential issue: spatial and semi temporal

Lennart: We can likely ignore temporal and spatial influences for this housing predictive task with the given data / features

Andrej: We need to write down the reason why we consider some housing datasets as random split data and others as temporal

**Assessment (AI, 2026-10-14):** The file first appeared on OpenML 43093 (MiamiHousing2016, uploaded 2021-09-24, creator and contributor Steven C. Bourassa, citing Mayer, Bourassa, Hoesli and Scognamiglio 2021, SSRN 3924412), so the source is OpenML, 2021; the definition said Kaggle and now says OpenML. The Kaggle dataset deepcontractor/miami-housing-dataset (last updated 2022-01-30) copies the OpenML description and names openml.org as its source; OpenML 44983 (2022-12-22) is a copy of that Kaggle dataset. All three describe the same 13,932 sales of 2016.

## Reference

https://doi.org/10.1177/0042098020982508
