---
unique_name: hiva_agnostic
name: hiva_agnostic
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: 'Yes'
year: '2007'
required_split:
- Custom
problem_type: Binary Classification
source_links:
- https://www.openml.org/search?type=data&id=1039
type_adapter_id: curation-record-v1
---

# hiva_agnostic

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Data previously was 3-class, originally had a custom split, also was preprocessed to be binary. Was a challenge held in 2007 - https://www.agnostic.inf.ethz.ch/datasets.php - but may be still representative of similar tasks.Also submission might still be possible. Could ask organizers for hidden test data. However could also be solved differently nowadays. 1618 features. In TabRepo trees are much better than NNs. Either a result of the unfair time limits for NNs or a bias through random splits; original source data links point to scam websites now

Potential issue: Preprocessing

Lennart: Preprocessing and original data state seem problematic

Andrej: Might consider to restore it to be a 3-class problem

## Reference

Datasets from the Agnostic Learning vs. Prior Knowledge Challenge (http://www.agnostic.inf.ethz.ch)
