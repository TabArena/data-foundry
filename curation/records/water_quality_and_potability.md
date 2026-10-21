---
unique_name: water_quality_and_potability
name: Water_Quality_and_Potability
suggestion: 'No'
decision_markers:
- Missing source information
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

**Open issues (AI, 2026-10-21):** not added; recommended keep `No` (`Missing source information` + `AHDS`). The re-check under the amended PROV-2 finds the first upload labelled "Synthetically generated" and physically impossible values.

1. **Reopen water_quality_and_potability under the amended PROV-2?**
   - Question: PROV-2 as amended (2026-10-21) keeps an untraceable upload when the data looks sound (passes PROV-3)
     and there is a source to point to. Does this dataset meet both conditions?
   - Source to point to: yes. Every link ends at the Kaggle upload `adityakadiwal/water-potability` of
     2021-04-25; the record's `uom190346a` upload (2024) and the MainakRepositor GitHub file are byte-identical
     copies of it (same MD5, 3,276 rows, 1,278 potable).
   - Sound data: no. The first upload's own source field reads "Synthetically generated"
     (https://www.kaggle.com/datasets/adityakadiwal/water-potability, metadata `userSpecifiedSources`); the top
     discussion threads ("IS THAT REAL DATA?", 54 votes; "Where are these data from?") asked for the method and
     got no answer from the uploader. The data card's figures ("6.52–6.83" pH, "Wondo Genet Campus (0.98 NTU)")
     come from other studies and do not match the file (pH 0-14, turbidity 1.45-6.74).
   - PROV-3 tests on the file:

     | Test | Result |
     |---|---|
     | 6, structure the world would show | TDS against conductivity: Spearman 0.021; TDS is 50 times the conductivity in the median row and above it in every row (real water: about 0.5-0.7 times) |
     | 6, the label | 1,277 of 1,278 "potable" samples have TDS above 1,000 mg/l (WHO maximum) and 518 a pH outside 6.5-8.5 |
     | 3 and 4, dependence and marginals | largest correlation between any two of the 9 features 0.154; every column near-normal (skew within ±0.62) |
     | 5, class-conditional generation | two pairs change sign by class: Sulfate-pH 0.23 / -0.27, Chloramines-pH -0.18 / 0.17 |
     | `generated_probes.py` | no flag: 13% of feature pairs dependent, no uniform column, no rule leaves |
     | Task | ROC AUC 0.657 (gradient boosting), 0.509 (logistic regression), 5-fold |

   - Implemented: nothing; the verdict stays `No`.
   - Alternative: reopen to `TBD -> Yes` as an untraceable upload with a source to point to (PROV-2). Cost: a table
     its uploader calls synthetic, with values no water sample can have, enters the benchmark.
   - Rule: PROV-2 (Should) needs the data to pass PROV-3 (Must); PROV-3 and SEL-16 retire generated data. The
     source statement and the measured marks agree, so the evidence standard of PROV-3 is met however it is read.
   - Recommendation (AI): keep `No`, and add `AHDS` to `Missing source information`, since the reason is now the
     data, not only the source.
   - Decision needed: keep `No` (with or without `AHDS`), or reopen to `TBD -> Yes`.

## Reference

https://www.kaggle.com/datasets/uom190346a/water-quality-and-potability
