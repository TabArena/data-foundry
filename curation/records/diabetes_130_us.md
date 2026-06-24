---
unique_name: diabetes_130_us
name: Diabetes130US
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: 'Yes'
original_source: UCI
year: '2014'
required_split:
- Random (IID)
problem_type: Multiclass Classification
source_links:
- https://www.openml.org/search?type=data&id=4541
- https://doi.org/10.24432/C5230J
type_adapter_id: curation-record-v1
---

# Diabetes130US

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Not sure if date is available, encounter_id might be sorted by date. Generally an interesting tabular data task. Same patients are in the dataset - need to account for that with preprocessing. Task has temporal nature, but features should be time invariant

Lennart: After preprocessing (handling duplicated patiens, handling one-hot encoded categories, ...)

Andrej: Requires proper preprocessing and handling of duplicate patients before inclusion

## Reference

Beata Strack, Jonathan P. DeShazo, Chris Gennings, Juan L. Olmo, Sebastian Ventura, Krzysztof J. Cios, and John N. Clore, “ Impact of HbA1c Measurement on Hospital Readmission Rates: Analysis of 70,000 Clinical Database Patient Records,” BioMed Research International, vol. 2014, Article ID 781670, 11 pages, 2014.
