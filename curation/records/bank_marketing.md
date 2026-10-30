---
unique_name: bank_marketing
name: bank-marketing
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: 'Yes'
original_source: UCI
year: '2011'
required_split:
- Random (IID)
problem_type: Binary Classification
source_links:
- https://www.openml.org/search?type=data&id=1461
- https://doi.org/10.24432/C5K306
notebook_path: datasets/beyond_iid/old_iid/bank_marketing/bank_marketing.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/bank_marketing/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

predict if the client will subscribe a term deposit. Might actually require temporal split - but as features seem to be time-invariant the task should be fine

Potential issue: preprocssed date features

Lennart: We can likely ignore the time impact but might need to restore the date features

Andrej: Fits criteria

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source roc_auc — AUC (with ALIFT second) in Moro, Cortez & Rita 2014, Decision Support Systems 62:22-31.

CC (2026-10-30, Lennart): `campaign` and `previous` are counts and stay numeric, as the UCI description gives them ("number of contacts performed during this campaign", "... before this campaign"); the BeyondArena notebook had typed them categorical (issue #34, raised by Adrian). CLEAN-14: a count stays numeric.

## Reference

S. Moro, R. Laureano and P. Cortez. Using Data Mining for Bank Direct Marketing: An Application of the CRISP-DM Methodology. In P. Novais et al. (Eds.), Proceedings of the European Simulation and Modelling Conference - ESM'2011, pp. 117-121, Guimarães, Portugal, October, 2011. EUROSIS.
