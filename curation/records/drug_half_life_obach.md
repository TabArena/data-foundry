---
unique_name: drug_half_life_obach
name: half_life_obach
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
tags:
- AI-Filled (Verify)
- Tiny Data
- Non-IID (Grouped)
collections:
- ChemPile
original_source: Other
year: '2008'
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.1124/dmd.108.020479
- 'https://huggingface.co/datasets/jablonkagroup/chempile-lift/tree/main/half_life_obach ; ChemNLP builder https://github.com/OpenBioML/chemnlp/tree/main/data/tabular/half_life_obach ; original: https://tdcommons.ai/single_pred_tasks/adme/#half-life-obach-et-al'
- https://arxiv.org/abs/2505.12534
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: 667 drugs with a human elimination half-life, a well documented compilation, but small and only weakly determined by structure.
- Source: Obach, Lombardo and Waters, "Trend Analysis of a Database of Intravenous Pharmacokinetic Parameters in Humans for 670 Drug Compounds", Drug Metab Dispos 36(7):1385, 2008 (https://doi.org/10.1124/dmd.108.020479, abstract read on PubMed 18426954): "a compilation and trend analysis of human i.v. pharmacokinetic data on 670 drugs", tabulating "clearance, volume of distribution at steady state, mean residence time, and terminal phase half-life" from original references that dosed intravenously; the authors build no model and write that the dataset "should enable future efforts aimed toward developing quantitative structure-pharmacokinetic relationships". As published through TDC and ChEMBL assay 1614674: 667 drugs, SMILES, a ChEMBL id and the half-life in hours (ChemNLP `half_life_obach/meta.yaml`, licence CC BY 4.0).
- Use case: a pharmacokineticist or medicinal chemist estimating the dosing interval and exposure of a candidate before the first human study; the source names the modelling purpose but no actor; fit approximate (half-life also depends on dose, route and formulation, which do not ship); regime grouped on the Bemis-Murcko scaffold (SPLIT-31).
- Siblings and duplicates: `vdss_lombardo` (volume of distribution) and `hepatocyte_clearance_astrazeneca` are the other pharmacokinetic records, and they come from the same kind of compilation: distinct parameters, so distinct tasks (PROV-7); note that VDss and half-life for many drugs come from this same Obach database, which the curator should check before shipping both (PROV-6). No other half-life record. External collections: ChemPile (config `half_life_obach`), TDC ADME and its leaderboard.
- Better data: a candidate of the benchmark ChemPile (ChemPile-LIFT config `half_life_obach`); no new search in this run.
- Papers and pages: the 2008 paper; TDC's ADME page ("Regression. Given a drug SMILES string, predict the half life duration", 667 drugs) and the ADMET group overview.
- Metric: TDC's ADMET leaderboard scores Half Life by Spearman, with the stated reason that "Spearman's correlation coefficient is used for benchmarks that depend on factors beyond the chemical structure" - a deliberate choice of the benchmark that defined the ML task, not of the data's publisher, which declares none (MET-1, MET-5). Candidate: `spearman` from TDC, or the fallback `rmse` on a log half-life (MET-3 for the scale, MET-8); the curator decides at the add stage. Inputs none.
- Risks for /add-dataset: 667 rows, so `Too Small` must be measured (TP-5); the target spans orders of magnitude and is usually modelled on a log scale (MET-3, CLEAN-11 for impossible values); the signal from structure alone is weak by TDC's own metric choice, so TP-2 matters; SMILES-only features (CLEAN-24); overlap with `vdss_lombardo` through the same compilation.
- Priority: gap 0, use case 0 (no actor named), source + (a documented compilation with a ChEMBL deposit), shape 0 (667 rows), risk 0.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark ChemPile (https://arxiv.org/abs/2505.12534).
- as published: 667 drugs (TDC Half_Life_Obach); in ChemPile-LIFT 12,673 text prompts over 1 config(s); target: half-life (hours).
- Why: Predict a drug's elimination half-life in humans
- Notes: Obach, Lombardo and Waters 2008 (Drug Metab Dispos 36:1385), deposited as ChEMBL assay 1614674. Small. Features: SMILES string only, so a container keeps the string and adds computed descriptors, as the apistox record does. No record.
