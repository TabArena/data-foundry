---
unique_name: melting_point
name: melting-point
checked_by:
- Andrej
suggestion: TBD -> Yes
decision_markers:
- TBD
tags:
- New IID
collections:
- New (BeyondArena)
original_source: Kaggle
year: '2025'
domain: chemistry & material science
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/competitions/melting-point/overview
source_row: 599
type_adapter_id: curation-record-v1
---

## Comments

Contains SMILES, so likely requires domain-specific solutions. Could also be seen as a kind of text. Don't know whether a custom split is needed, but assume IID for now. Competition was leaky, because test data was partially online.

## Reference

Frank Mtetwa and John Hedengren. Thermophysical Property: Melting Point. https://kaggle.com/competitions/melting-point, 2025. Kaggle.
