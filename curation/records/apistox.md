---
unique_name: apistox
name: ApisTox
checked_by:
- Andrej
data_foundry_status:
- WIP (DF)
suggestion: 'Yes'
tags:
- Non-IID (Temporal)
collections:
- New (BeyondArena)
original_source: Other
year: '2024'
domain: biology & life sciences
required_split:
- Custom
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.5281/zenodo.11062076
v2_path: datasets/_dev/tabarena-v0pt2/apistox/dataset.py
source_row: 717
type_adapter_id: curation-record-v1
---

## Comments

Contains SMILES. Authors provide custom splits: maximum diversity (MaxMin) split and a novel approximation of time split using PubChem literature data

Unclear what to do with SMILES. To correctly use this dataset, we would need to better understand the domain

**Assessment (AI, 2026-10-07):** Valid; curated as a temporal task on the first publication year (four ten-year windows), dropping `ppdb_level`, `toxicity_type` and `source` (derived from the measured LD50 or the label's database). Open question: the benchmark's default pipeline lowercases a string column and embeds it with Qwen3-Embedding-8B at 32 dimensions, which gets almost none of the structure out of a SMILES. On the four windows that embedding with the agrochemical flags and the year reaches ROC AUC 0.78-0.81, no better than the flags and the year alone (0.70-0.82), while ECFP4 bits or character n-grams reach 0.83-0.85. So either a pinned fingerprint ships with the data or the benchmark needs a SMILES encoder. The source is Zenodo, not UCI.

## Reference

ApisTox: a new benchmark dataset for the classification of small molecules toxicity on honey bees
By Jakub Adamczyk, Jakub Poziemski, Paweł Siedlecki. 2024

Published in arXiv
