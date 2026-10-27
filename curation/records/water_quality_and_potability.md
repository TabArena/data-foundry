---
unique_name: water_quality_and_potability
name: Water_Quality_and_Potability
suggestion: 'No'
decision_markers:
- Missing source information
- AHDS (Artifical/Handmade/Deterministic/Simulated)
original_source: Kaggle
year: '2021'
required_split:
- '?'
source_links:
- https://www.kaggle.com/datasets/uom190346a/water-quality-and-potability and https://github.com/MainakRepositor/Datasets/blob/master/water_potability.csv
type_adapter_id: curation-record-v1
---

## Comments

Imported from the TabArena curation workbook.

TabArena curation verdict: None-Source.

water quality measurements and assessments related to potability, which is the suitability of water for human consumption. Each row in the dataset represents a water sample with specific attributes, and the "Potability" column indicates whether the water is suitable for consumption. Might require temporal or grouped split. No information on location or collection time given.

Potential issue: Unclear source information

Lennart: Enough info about data to see the  features are invariant of gorups/temporal nature IMO. But sitll unclear source

Andrej: Unclear whether grouped/temporal nature of data might be an issue

CC (2026-10-21, Lennart): recheck it under the amended PROV-2 and the PROV-3 tests, and "add it for me to be verified here" on the review page, whatever the result.

**Assessment (AI, 2026-10-21):** re-checked under PROV-2 as amended and the PROV-3 tests; recommend keeping `No` and adding `AHDS` to `Missing source information`; the curator has the call. The first upload is Kaggle `adityakadiwal/water-potability` (2021-04-25, CC0); its source field reads "Synthetically generated". The record's two links (`uom190346a`, 2024, and the MainakRepositor GitHub file) are byte-identical copies of it (same MD5, 3,276 rows). The data card gives no place, date or lab, and quotes figures from other studies ("6.52–6.83", "Wondo Genet Campus (0.98 NTU)") that the file does not show. Measured on the file: `Solids` (TDS) and `Conductivity` correlate at Spearman 0.021, and TDS is 50 times the conductivity in the median row, above it in 100% of rows (real water has TDS about 0.5-0.7 times EC, PROV-3 test 6); the largest feature correlation is 0.154; every column is near-normal (skew within ±0.62); 1,277 of 1,278 "potable" rows have TDS above 1,000 mg/l and 518 have pH outside 6.5-8.5; within each class two pairs change sign (Sulfate-pH 0.23 vs -0.27, Chloramines-pH -0.18 vs 0.17; test 5). `generated_probes` raises no flag (13% of pairs dependent, no uniform column); a classifier gives ROC AUC 0.657 (gradient boosting) and 0.509 (logistic regression).

CC (2026-10-22, Lennart): the update is correct: keep `No`, with `AHDS` added to `Missing source information`.

**Assessment (AI, 2026-10-22):** `AHDS` added (the first upload's source field reads "Synthetically generated"; TDS is 50 times the conductivity and 1,277 of 1,278 "potable" samples exceed the WHO TDS maximum). Open-issues block removed.

## Reference

https://www.kaggle.com/datasets/uom190346a/water-quality-and-potability
