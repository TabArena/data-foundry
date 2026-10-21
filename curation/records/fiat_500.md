---
unique_name: fiat_500
name: Another-Dataset-on-used-Fiat-500-(1538-rows) / fiat_500
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: 'Yes'
original_source: Kaggle
year: '2020'
required_split:
- Random (IID)
source_links:
- https://www.openml.org/search?type=data&id=43828
- https://www.kaggle.com/datasets/paolocons/another-fiat-500-dataset-1538-rows
notebook_path: datasets/beyond_iid/old_iid/fiat_500/fiat_500.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/fiat_500/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Some guy crawled data in Fiat cars - target is to predict the price, is a self-constructed application, but useful; only time-invariant features, some spatial information

Potential issue: spatial information

Lennart: impact of spatial data can be likely ignored, otherwise dataset fits criteria even if crawled

Andrej: Is crawled data, but one could imagine people to be interested in estimating whether some cars are overpriced

**Assessment (AI, 2026-10-14):** the duplicates are not natural. Most of the 18 exact copies sit 12-14 rows after their first copy (one results page), so the crawler saw the listing twice. The same car (model, age in days, an odd km reading such as 9,248, owners) appears at up to 9 places a median 396 km apart, mostly at one price: 104 rows repeat another car (78 at the same price); among the 753 rows with a non-round km reading, 681 distinct age-km pairs, so a shared odd reading by chance is very unlikely.

CC (2026-10-14, Lennart): Keep one row per car, its first listing (1,434 rows).

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback rmse — Kaggle dataset without a competition or paper; the data card names no metric.

## Reference

https://www.kaggle.com/datasets/paolocons/another-fiat-500-dataset-1538-rows
