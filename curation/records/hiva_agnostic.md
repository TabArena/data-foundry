---
unique_name: hiva_agnostic
name: hiva_agnostic
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: 'Yes'
year: '2007'
required_split:
- Random (IID)
problem_type: Binary Classification
source_links:
- https://www.openml.org/search?type=data&id=1039
notebook_path: datasets/beyond_iid/old_iid/hiva_agnostic/hiva_agnostic.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/hiva_agnostic/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Data previously was 3-class, originally had a custom split, also was preprocessed to be binary. Was a challenge held in 2007 - https://www.agnostic.inf.ethz.ch/datasets.php - but may be still representative of similar tasks.Also submission might still be possible. Could ask organizers for hidden test data. However could also be solved differently nowadays. 1618 features. In TabRepo trees are much better than NNs. Either a result of the unfair time limits for NNs or a bias through random splits; original source data links point to scam websites now

Potential issue: Preprocessing

Lennart: Preprocessing and original data state seem problematic

Andrej: Might consider to restore it to be a 3-class problem

**Assessment (AI, 2026-10-14):** the challenge split the screen's 42,678 compounds into training (3,845, 135 active), validation (384, 14 active) and test (38,449, labels never released), as `hiva.param` lists them. The validation compounds have the same 1,617 descriptors; their labels are in ValidAgnos.zip, which the download already fetched. The fixed list of dropped descriptors removed 99 of the 191 copies in the training file; the definition now drops every descriptor that copies an earlier one over all 4,229 compounds (188).

CC (2026-10-14, Lennart): Add the 384 validation compounds (4,229 compounds, 149 active).

## Reference

Datasets from the Agnostic Learning vs. Prior Knowledge Challenge (http://www.agnostic.inf.ethz.ch)
