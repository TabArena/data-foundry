---
unique_name: ljubljana_primary_tumor
name: Ljubljana Primary Tumor
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
tags:
- Tiny Data
collections:
- New (BeyondArena)
original_source: UCI
year: '1988'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C5WK5Q
notebook_path: datasets/beyond_iid/new_iid/ljubljana_primary_tumor/ljubljana_primary_tumor.ipynb
source_row: 770
type_adapter_id: curation-record-v1
---

## Comments

Need to resolve ordinal encoding, otherwise looks good!

Has a lot of classes, need to see there are enough labels per class or if I need to group some cases / remove some samples

## Reference

UCI
