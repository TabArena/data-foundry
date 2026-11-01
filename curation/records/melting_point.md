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

**Assessment (AI, 2026-10-31):** the benchmark ChemPile (https://arxiv.org/abs/2505.12534) carries a related version, "melting_points", not this record's data, so no collection tag: Literature-mined melting points behind Tetko et al. 2014 (J Chem Inf Model 54:3320), served from OCHEM. Related record: melting_point ('TBD -> Yes', the 2025 Kaggle melting-point competition, which the record calls leaky because test data was partly online); this OCHEM compilation is the larger and traceable source for the same target. The ChemNLP copy comes through a Dropbox link, so a record should pull from OCHEM

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `melting_point_patents` (TBD -> Yes, priority 3), `bradley_open_melting_point` (TBD -> Yes, priority 3). Each is screened in its own record; this record's verdict stays the curator's.

**Assessment (AI, 2026-11-01):** ChemPile's "melting_points" is the record `melting_point_patents`, now tagged ChemPile.

## Reference

Frank Mtetwa and John Hedengren. Thermophysical Property: Melting Point. https://kaggle.com/competitions/melting-point, 2025. Kaggle.
