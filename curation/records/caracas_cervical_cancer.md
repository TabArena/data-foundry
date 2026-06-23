---
unique_name: caracas_cervical_cancer
name: Caracas Cervical Cancer
checked_by:
- Lennart
suggestion: 'Yes'
tags:
- New IID
- Multi-target
collections:
- New (BeyondArena)
- TabSTAR
original_source: UCI
year: '2017'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: TBD
original_data_state: One Table
source_links:
- 10.24432/C5Z310
- https://www.openml.org/search?type=data&id=46592
- http://vcmi.inescporto.pt/reproducible research/ibpria2017/CervicalCancer/
source_row: 688
type_adapter_id: curation-record-v1
---

# Caracas Cervical Cancer

## Comments

Some features are multi-categoricals as one-hot encoding.  Might want to reverse this

Has 4 target variables, unsure which one to use. Likely want to use Biopsy as the real ground turth (not just an indicator)

## Reference

@inproceedings{fernandes2017transfer,
  title={Transfer learning with partial observability applied to cervical cancer screening},
  author={Fernandes, Kelwin and Cardoso, Jaime S and Fernandes, Jessica},
  booktitle={Iberian conference on pattern recognition and image analysis},
  pages={243--250},
  year={2017},
  organization={Springer}
}
