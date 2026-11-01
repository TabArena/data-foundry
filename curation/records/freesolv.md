---
unique_name: freesolv
name: freesolv
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
- Tiny Data
collections:
- ChemPile
original_source: Github
year: '2014'
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.1007/s10822-014-9747-x
- 'https://huggingface.co/datasets/jablonkagroup/chempile-lift/tree/main/freesolv ; ChemNLP builder https://github.com/OpenBioML/chemnlp/tree/main/data/tabular/freesolv ; original: https://github.com/MobleyLab/FreeSolv ; https://tdcommons.ai/single_pred_tasks/adme/#hydrationfreeenergy-freesolv'
- https://arxiv.org/abs/2505.12534
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: a real measured target, but 642 molecules, a database published to validate simulation methods rather than for a decision, and a simulated column next to the experimental one.
- Source: Mobley and Guthrie, "FreeSolv: a database of experimental and calculated hydration free energies, with input files", J Comput Aided Mol Des 28:711 (2014), doi 10.1007/s10822-014-9747-x; the database is versioned at github.com/MobleyLab/FreeSolv (v0.1 "contains 642 molecules"; the last numbered release is v0.52, Jan 2018). As published: one semicolon-delimited `database.txt` with the compound id, SMILES, IUPAC name, the experimental hydration free energy with its uncertainty, a GAFF/TIP3P-calculated value with its uncertainty, reference DOIs and notes. The experimental values are taken from earlier literature compilations (the Rizzo set, Abraham et al. 1990, Guthrie's data, SAMPL4), so this is a compilation, not one lab. TDC serves it as HydrationFreeEnergy_FreeSolv, "642 drugs".
- Use case: a computational chemist estimating a small neutral molecule's hydration free energy without running a free-energy calculation; the database itself was published to version, cite and benchmark such calculations and names no actor or decision, so fit approximate; regime grouped on the Bemis-Murcko scaffold (SPLIT-31 as amended; TDC also recommends its scaffold split for the set).
- Siblings and duplicates: `solprop_solvation_free_energy` (a candidate record of the same run) holds about 10,145 experimental solvation free energies over many solvents, roughly 15 times this set and a superset of the water case; no other hydration record (`grep -il freesolv/"hydration free"`). Not a duplicate of anything recorded. External collections: ChemPile-LIFT config `freesolv` (arXiv 2505.12534), MoleculeNet, TDC.
- Better data: a candidate of the benchmark ChemPile (this run searched no further); the larger SolProp collection is already its own record, `solprop_solvation_free_energy`.
- Papers and pages: Mobley and Guthrie 2014; MoleculeNet (Wu et al. 2018) carries the set as a regression benchmark; the SAMPL blind challenges use the same measurements.
- Metric: none found at the source. The TDC ADME page names no metric for it, and it is not among the 22 datasets of the TDC ADMET Benchmark Group (tdcommons.ai/benchmark/admet_group/overview); the database paper reports the RMS error of its GAFF values against experiment, not a model ranking; MoleculeNet reports RMSE on FreeSolv (not re-checked here). So the regression fallback `rmse` (MET-5, MET-8); inputs none.
- Risks for /add-dataset: the calculated GAFF value is a simulation of the target and must never become a feature (LEAK); 642 rows with SMILES-only features (TP-5: small, a tiny-data regression task rather than an automatic `Too Small`); the experimental values come from several compilations and carry per-row uncertainties, so duplicates and disagreements need a rule; the licence reads CC BY 4.0 in the repository README and CC BY-NC-SA 4.0 on the TDC page (noted only, no criterion: EV-4).
- Priority: gap 0 (chemistry not thin), use case 0 (a method-validation database, no actor or decision), source + (paper plus a versioned, documented repository), shape 0 (642 rows, one input column), risk - (the much larger SolProp record covers the same measurement, and the GAFF column is a leak if mishandled).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark ChemPile (https://arxiv.org/abs/2505.12534).
- as published: 642 molecules (FreeSolv v0.5 / TDC); in ChemPile-LIFT 20,544 text prompts over 1 config(s); target: experimental hydration free energy (kcal/mol); the file also carries a GAFF calculated value.
- Why: Predict the experimental hydration free energy of a small neutral molecule in water
- Notes: Mobley and Guthrie 2014 (J Comput Aided Mol Des 28:711). The experimental column is real measurement; the GAFF column is simulated and would be a leak as a feature. Very small. Licence CC BY-NC-SA 4.0. Features: SMILES string only, so a container keeps the string and adds computed descriptors, as the apistox record ...
