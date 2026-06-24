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
problem_type: Binary Classification
source_links:
- https://www.openml.org/search?type=data&id=1461
- https://doi.org/10.24432/C5K306
type_adapter_id: curation-record-v1
---

# bank-marketing

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

predict if the client will subscribe a term deposit. Might actually require temporal split - but as features seem to be time-invariant the task should be fine

Potential issue: preprocssed date features

Lennart: We can likely ignore the time impact but might need to restore the date features

Andrej: Fits criteria

## Reference

S. Moro, R. Laureano and P. Cortez. Using Data Mining for Bank Direct Marketing: An Application of the CRISP-DM Methodology. In P. Novais et al. (Eds.), Proceedings of the European Simulation and Modelling Conference - ESM'2011, pp. 117-121, Guimarães, Portugal, October, 2011. EUROSIS.
