---
unique_name: apistox
name: ApisTox
checked_by:
- Andrej
data_foundry_status:
- 'DF: Yes'
suggestion: 'Yes'
tags:
- Non-IID (Temporal)
collections:
- New (BeyondArena)
original_source: Other
year: '2024'
domain: chemistry & material science
required_split:
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

**Assessment (AI, 2026-10-14):** the original source is the Zenodo record (concept DOI 10.5281/zenodo.11062076); UCI 995 holds no file and links to it, so `original_source` is Other. The reference is now the published data descriptor (Scientific Data 12:5, 2025), which the definition's BibTeX cites. Licence: CC BY-NC 4.0 in the current Zenodo version, CC BY 4.0 in v1 (noted only; the licence is no verdict reason). The question "what to do with SMILES" is answered in the definition: the SMILES stays a string feature and RDKit's 2D descriptors of it are added (since 2026-10-12).

CC (2026-10-14, Lennart): Ship (review of the 2026-10-07 run).

CC (2026-10-14, Lennart): Drop the SMILES as a feature, as in every SMILES dataset; the structure ships as RDKit's 2D descriptors from one shared helper, the same tooling for all (review page, issue 1).

**Assessment (AI, 2026-10-14):** Next to the descriptors the SMILES as character n-grams adds 0.010 ROC AUC to LightGBM over the 4 windows (standard error 0.023). The definition now drops it and keeps the 199 descriptors, computed by `data_foundry.v2.rdkit_descriptors` (CHANGELOG, 2026-10-14).

CC (2026-10-21, Lennart): one domain for the molecule-property datasets (the input is the molecule): "chemistry & material science", for all ten QSAR siblings.

CC (2026-10-21, Lennart): "yes we should have one clear way to treat 0/1 flags": every 0/1 flag (a feature holding only 0 and 1, plus missing values; booleans too) is categorical (CLEAN-14, amended). Typed categorical here: herbicide, fungicide, insecticide, other_agrochemical and the 14 RDKit fragment counts that hold only 0 and 1 (found on the data in `_feature_types`).

CC (2026-10-21, Lennart): on which 0/1 columns are flags: "no if we can infer from the semantic context, keep it a number, this is a real-world bias. We want to make things categorical if we know from the context they are indeed such" (CLEAN-14, amended again). Kept categorical: herbicide, fungicide, insecticide, other_agrochemical. Reverted: the 14 RDKit fragment counts that hold only 0 and 1 stay numeric.

## Reference

ApisTox: a new benchmark dataset for the classification of small molecules toxicity on honey bees
By Jakub Adamczyk, Jakub Poziemski, Paweł Siedlecki. 2024

Published in Scientific Data 12:5 (2025), doi 10.1038/s41597-024-04232-w; preprint on arXiv (2024).
