---
unique_name: human_intestinal_absorption_hou
name: human_intestinal_absorption
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
- Tiny Data
collections:
- ChemPile
original_source: Other
year: '2007'
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.1021/ci600343x
- 'https://huggingface.co/datasets/jablonkagroup/chempile-lift/tree/main/human_intestinal_absorption ; ChemNLP builder https://github.com/OpenBioML/chemnlp/tree/main/data/tabular/human_intestinal_absorption ; original: https://tdcommons.ai/single_pred_tasks/adme/#hia-human-intestinal-absorption-hou-et-al'
- https://arxiv.org/abs/2505.12534
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: a real ADME decision with a benchmark that fixes metric and split, on 578 drugs whose negative class is a small minority - the fold counts decide whether it is buildable.
- Source: Hou, Wang, Zhang, Xu, "ADME evaluation in drug discovery. 7. Prediction of oral absorption by correlation and classification", J Chem Inf Model 47(1):208 (2007), doi 10.1021/ci600343x; TDC serves it as HIA_Hou, "**Dataset Statistics:** 578 drugs", binary classification from SMILES ("Oral drugs must be absorbed from the gastrointestinal tract into the bloodstream", tdcommons.ai/single_pred_tasks/adme). As published: one table, SMILES and a binary human-intestinal-absorption label.
- Use case: an early go/no-go on an oral candidate - whether a compound given by mouth reaches the bloodstream at all - taken before formulation or an animal study; the task description names the moment, not the actor, so fit approximate; regime grouped on the Bemis-Murcko scaffold (SPLIT-31 as amended; TDC's split for the ADMET benchmarks).
- Siblings and duplicates: `caco2_permeability_merged` (a candidate of the same run) holds the in-vitro cell-monolayer stand-in for the same property, a distinct measurement (PROV-7); `pampa_ncats`, `oral_bioavailability_ma`, `hepatocyte_clearance_astrazeneca` and `astrazeneca_chembl_logd74` are the other ADME candidates; no duplicate (`grep -il intestinal` matches only this record among the chemistry ones). External collections: ChemPile-LIFT config `human_intestinal_absorption` (arXiv 2505.12534), TDC ADMET Benchmark Group.
- Better data: a candidate of the benchmark ChemPile (this run searched no further).
- Papers and pages: Hou et al. 2007 (paywalled, not read here); the TDC ADME page and the ADMET Benchmark Group leaderboard.
- Metric: the TDC ADMET Benchmark Group ranks HIA_Hou by AUROC on a scaffold split (tdcommons.ai/benchmark/admet_group/overview), a deliberate choice of the benchmark that defined the task (MET-1, MET-5) and the binary fallback besides; inputs none.
- Risks for /add-dataset: 578 rows with a strongly imbalanced label (well-absorbed drugs dominate; the negatives were not counted here), so count the minority class per test fold first (TP-5, TP-8) - this is the reason for 2nd Tier; the absorption cut behind the binary label (a percentage threshold Hou et al. fixed) and the provenance of the absorption values need checking; features are the SMILES only.
- Priority: gap 0 (chemistry not thin), use case + (an oral-candidate go/no-go), source + (a journal paper plus a benchmark that defines the task), shape 0 (578 drugs, one input column), risk - (few negatives per fold).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark ChemPile (https://arxiv.org/abs/2505.12534).
- as published: 578 drugs (TDC HIA_Hou); in ChemPile-LIFT 10,982 text prompts over 1 config(s); target: HIA (1/0).
- Why: Classify whether an orally given drug is well absorbed from the gut
- Notes: Hou et al. 2007. Small. Features: SMILES string only, so a container keeps the string and adds computed descriptors, as the apistox record does. No record.
