---
unique_name: qsar_tid_11
name: QSAR-TID-11
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: 'Yes'
year: '2015'
required_split:
- Random (IID)
problem_type: Regression
source_links:
- https://www.openml.org/search?type=data&id=3050
- https://doi.org/10.17632/SPWGRCNJDG.1
- https://doi.org/10.1007/S10994
type_adapter_id: curation-record-v1
---

# QSAR-TID-11

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Chemistry dataset. features represent FCFP 1024bit Molecular Fingerprints. Unsure what that is, but I think there are no local correlations;hard to tell usability without domain expert even from paper

Potential issue: We are no domain experts

Lennart: tend towards yes - hard to tell if domain is appropiate. The papers and meta-learning use this still and it might be outdated but tabular is sitll a strong baseline (even once they have deep learning method as for other bio applicaiton domains)

Andrej: Not in TabRepo, need to clarify
