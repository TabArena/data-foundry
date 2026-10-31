---
unique_name: vdss_lombardo
name: volume_of_distribution_at_steady_state_lombardo_et_al
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
collections:
- ChemPile
original_source: Other
year: '2016'
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.1021/acs.jcim.6b00044
- 'https://huggingface.co/datasets/jablonkagroup/chempile-lift/tree/main/volume_of_distribution_at_steady_state_lombardo_et_al ; ChemNLP builder https://github.com/OpenBioML/chemnlp/tree/main/data/tabular/volume_of_distribution_at_steady_state_lombardo_et_al ; original: https://tdcommons.ai/single_pred_tasks/adme/#vdss-volumn-of-distribution-at-steady-state-lombardo-et-al'
- https://arxiv.org/abs/2505.12534
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: a curated human pharmacokinetic endpoint with a real pre-clinical decision behind it, published with a paper and carried by TDC's ADMET group; small (1,130 drugs) and SMILES-only.
- Source: Franco Lombardo and Yankang Jing, "In Silico Prediction of Volume of Distribution in Humans. Extensive Data Set and the Exploration of Linear and Nonlinear Methods Coupled with Molecular Interaction Fields Descriptors", Journal of Chemical Information and Modeling 56(10):2042-2052, 2016 (https://doi.org/10.1021/acs.jcim.6b00044; the publisher's page returns 403 here and the PubMed lookup by DOI returned nothing, so the paper's text, its compound count and its own evaluation metric were not read). As published through TDC (`ADME(name="VDss_Lombardo")`) and ChemNLP: 1,130 rows, identifiers `SMILES` and `compound_name` ("mix of drug name and ids"), target `VDss_Lombardo`, "volume of distribution at steady state (VDss)", units L/kg, continuous; licence CC BY 4.0 in the ChemNLP metadata. The values are human intravenous-dosing data the authors compiled from the literature.
- Use case: a DMPK scientist, before a compound goes into human studies (or when picking between candidates), predicts its steady-state volume of distribution to set dose and dosing interval; fit approximate, because the target is pooled from published IV studies of different designs and populations rather than one protocol; regime grouped on the Bemis-Murcko scaffold, since the rows are exact structures and a new candidate comes from an unmeasured series (SPLIT-31 as amended 2026-10-26) — TDC's own ADMET benchmark group also splits VDss by scaffold (https://tdcommons.ai/benchmark/admet_group/overview/).
- Siblings and duplicates: no earlier record (checked for vdss, lombardo, volume_of_distribution). Other ADME endpoints of this run are separate records with their own targets, not duplicates (PROV-7): `drug_half_life_obach`, `hepatocyte_clearance_astrazeneca`, `caco2_permeability_merged`, `human_intestinal_absorption_hou`, `oral_bioavailability_ma`, `bbbp_martins`, `tdc_lipophilicity_astrazeneca`. SMILES-only precedents that shipped: `apistox` (`Yes`; CC 2026-10-14 drops the SMILES and ships RDKit 2D descriptors), `qsar_tid_11`, `qsar_oral_toxicity`. External collections: ChemPile-LIFT (`volume_of_distribution_at_steady_state_lombardo_et_al`), ChemNLP, TDC (ADME and the ADMET benchmark group).
- Better data: a candidate of the benchmark ChemPile; no new search this run. Worth the main session's eye: a later compilation of the same endpoint, "A Benchmarking Dataset with 2440 Organic Molecules for Volume Distribution at Steady State" (Liu et al., arXiv 2211.05661, 2022; 13 public sources plus DrugBank, IV administration only), came up incidentally while reading on this record and was not followed further.
- Papers and pages: the JCIM paper above; TDC page https://tdcommons.ai/single_pred_tasks/adme/#vdss-volumn-of-distribution-at-steady-state-lombardo-et-al; TDC's ADMET leaderboard for VDss.
- Metric: none found at the source. The paper is paywalled (pubs.acs.org 403 here) and its ranked criterion was not read; PK work of this kind usually reports geometric mean fold error and the share within 2-fold, which would be a MET-5 question once the text is available. TDC's ADMET benchmark group — a later benchmark, not the source — ranks VDss by Spearman correlation on a scaffold split (https://tdcommons.ai/benchmark/admet_group/overview/: "Spearman is used for benchmarks that depend on factors beyond chemical structure"). Until the paper is read, the regression fallback `rmse` (MET-8), with MET-3 in mind: VDss spans orders of magnitude, so the modelling scale is log10 while the metric is on L/kg.
- Risks for /add-dataset: the paper's own compound count against TDC's 1,130 and what TDC dropped (PROV-15); whether the values are pooled across studies per drug (one target value per compound, with its spread unknown); 1,130 rows is not far above the size floor for a regression (TP-5); one column as published, so the features come from the shared RDKit descriptor helper; `compound_name` is an identifier, not a feature (CLEAN).
- Priority: gap 0 (chemistry & material science, regression and grouped are not thin), use case + (dose setting from VDss, the paper's own motivation), source + (a peer-reviewed paper with the data set, carried by TDC), shape 0 (1,130 rows, one column as published), risk 0.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark ChemPile (https://arxiv.org/abs/2505.12534).
- as published: 1,130 drugs (TDC VDss_Lombardo); in ChemPile-LIFT 22,600 text prompts over 1 config(s); target: VDss (L/kg).
- Why: Predict the steady-state volume of distribution of a drug in humans
- Notes: Lombardo and Jing 2016, curated human intravenous pharmacokinetic data. Features: SMILES string only, so a container keeps the string and adds computed descriptors, as the apistox record does. No record.
