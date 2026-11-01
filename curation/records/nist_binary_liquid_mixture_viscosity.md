---
unique_name: nist_binary_liquid_mixture_viscosity
name: NIST viscosity of binary liquid mixtures (Bilodeau et al. curation of NIST TRC data)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- Non-IID (Grouped)
- AI-Filled (Verify)
original_source: Other
year: '2023'
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://zenodo.org/records/8042966
- https://doi.org/10.1016/j.cej.2023.142454
- https://github.com/chemcognition-lab/chemixhub/tree/main/datasets/nist-logV
- https://arxiv.org/abs/2506.12231
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: measured viscosities of binary liquid mixtures from NIST's literature collection, curated by Bilodeau et al. (Chemical Engineering Journal 2023; CC BY 4.0 on Zenodo), with the two components as SMILES, mole fraction and temperature; a large experimental mixture-property regression, grouped by mixture.
- Source: Bilodeau, Kazakov, Mukhopadhyay, Emerson, Kalantar, Muzny and Jensen, "Machine learning for predicting the viscosity of binary liquid mixtures", Chemical Engineering Journal (2023), doi 10.1016/j.cej.2023.142454; Zenodo 10.5281/zenodo.8042966 (2023-05-15, CC BY 4.0; one file, pretrained_models.zip, 95 MB, which holds nist_dippr_source/NIST_Visc_Data.csv per the CheMixHub README). The Zenodo abstract: "we also developed an automated curation pipeline and applied it to a large dataset collected from the literature by the National Institute of Standards and Technology (NIST)", providing "a large set of curated viscosity data that can be used for future machine learning efforts". Sizes from the Assessment, not checked against the CSV: 34,374 measurements of 4,566 binary mixtures over 1,397 molecules after filtering; 239,201 points of 84,133 mixtures in the full NIST set. CheMixHub reprocesses it as processed_NISTlogV.csv (22.8 MB, "log-transformed dynamic viscosity values for various binary liquid mixtures across different temperatures and compositions").
- Use case: a formulation or process engineer (coatings, lubricants, personal care and pharmaceuticals are named in the abstract) estimates a candidate mixture's viscosity at a composition and temperature before measuring it, to choose solvents and compositions; the source names the fields and the design need, not a decision; fit direct for unmeasured mixtures of known components; regime grouped by mixture (each recurs over compositions and temperatures), with unseen components as the harder variant (CheMixHub's splits).
- Siblings and duplicates: the CheMixHub siblings `ilthermo_ionic_liquid_mixture_viscosity` (ILThermo ionic liquids, another source), `drug_solubility_binary_solvent_mixtures`, `bigsoldb_2`, `flash_point_sun_morgan` and `solid_polymer_electrolyte_ionic_conductivity` (other sources and properties): no duplicate (PROV-4, PROV-7). External collections: CheMixHub (arXiv 2506.12231; not in our vocabulary).
- Better data: from the curator's Zotero collection (item 77, the CheMixHub paper); no further search this round.
- Papers and pages: the CEJ paper (abstract via Zenodo; the full text was not read); CheMixHub's README and processing script (read).
- Metric: the paper reports MAE 0.043 and RMSE 0.080 in log10 cP side by side (abstract), so the fallback `rmse` on log10 viscosity (MET-5, MET-3); CheMixHub's own metric was not read; inputs: the mixture as the group, from the two component ids.
- Risks for /add-dataset: the inputs are two molecules, so featurise each component with pinned descriptors and order the pair consistently (CLEAN-24); rows at mole fraction 0 or 1, if present, are pure-component viscosities that tie a mixture's curve to its components (group by mixture or by component); the curation pipeline's filters (outliers, the ensemble reliability classifier) shape the target; the row counts above are to check.
- Priority: gap 0 (chemistry & material science, regression and grouped are not thin), use case 0 (fields named, no decision), source + (a peer-reviewed paper with NIST co-authors, an open deposit), shape + (tens of thousands of measurements, thousands of mixtures, numeric conditions plus structures), risk 0.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 77: "CheMixHub: Datasets and Benchmarks for Chemical Mixture Property Prediction".
- as published: filtered: 34,374 measurements of 4,566 binary mixtures over 1,397 molecules; full NIST set: 239,201 points, 84,133 mixtures, 1,648 molecules; columns: two components (SMILES), mole fraction, ...; target: ln viscosity (cP); access: open.
- Why: large, experimental, documented by NIST; an established engineering property-prediction task
- Adds: mixture thermophysical-property regression, a domain absent from the records
