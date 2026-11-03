---
unique_name: block_copolymer_phase
name: block_polymers_morphology
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 4
decision_markers:
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
collections:
- ChemPile
original_source: Other
year: '2024'
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://doi.org/10.1021/acs.jcim.4c00242
- 'https://huggingface.co/datasets/jablonkagroup/chempile-lift/tree/main/block_polymers_morphology ; ChemNLP builder https://github.com/OpenBioML/chemnlp/tree/main/data/tabular/block_polymers_morphology ; original: https://github.com/olsenlabmit/BCDB (data/diblock.csv) ; http://doi.org/10.5281/zenodo.4780309'
- https://arxiv.org/abs/2505.12534
- https://github.com/olsenlabmit/BCDB/blob/main/data/BCPs.xlsx
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 4: 4,438 measured diblock-copolymer phase observations, a real multiclass materials task outside drug discovery, and multiclass is thin in the benchmark.
- Source: Rebello et al. 2024, "The Block Copolymer Phase Behavior Database", J Chem Inf Model 64:6118 (doi 10.1021/acs.jcim.4c00242, online 2024-08-10), Olsen lab at MIT; the data sit in github.com/olsenlabmit/BCDB and on Zenodo (doi 10.5281/zenodo.4780309, CC BY 4.0). The abstract: the schema "at the time of publication contains over 5400 block copolymer total melt phase measurements mined from the literature and manually curated"; the README adds "A DOI is provided for each data point" and "Data from figures was extracted using WebPlotDigitizer". As published: one table per architecture (the repo now ships data/BCPs.xlsx with a diblock tab; the data/diblock.csv the ChemNLP builder reads is gone from the default branch, checked 2026-10-31). The ChemNLP cut keeps phase1, T, BigSMILES, Mn, f1, Mw, D and drops rows with a second phase: 4,438 rows.
- Use case: a polymer scientist designing a self-assembling material, before synthesis and annealing, predicts which ordered morphology (lamellar, cylinder, gyroid, disordered, ...) a melt of a given composition and molar mass forms at a temperature; fit direct for that design decision; regime grouped, because each point carries the DOI of the paper it was mined from and one sample contributes several temperatures (SPLIT-29, LEAK-17).
- Siblings and duplicates: no record of this source. Other polymer records of this run: `bicerano_polymer_tg`, `polymer_gas_solubility_rhnet`, `solid_polymer_electrolyte_ionic_conductivity` (other targets, PROV-7). External collections: ChemPile / ChemNLP (config `block_polymers_morphology`).
- Better data: a candidate of the benchmark ChemPile; no further search this round.
- Papers and pages: Rebello et al. 2024 (the database and its schema); the BCDB README and Zenodo deposit; the ChemNLP builder `data/tabular/block_polymers_morphology`.
- Metric: none found. The paper defines a database, not a prediction task, and names no metric for the phase label (its F1 of 0.74 is for the GPT-4 screen that finds candidate papers); looked at the paper's abstract, the BCDB README and the ChemNLP meta. So the fallback, `log_loss` for a multiclass target.
- Risks for /add-dataset: rebuild from data/BCPs.xlsx or the Zenodo deposit, since the builder's CSV is gone (`Needs extensive data wrangling`); in the ChemPile cut Mw and D are prose ("average molecular mass of ... g/mol", with a REPLACENULL sentinel), so take them from the BCDB file as numbers (CLEAN-12); the phase classes are many and unbalanced, so count them per fold (TP-5, TP-8); repeats of one sample across temperatures and of one paper across rows need the grouping decided (SPLIT-29); values digitised from figures carry a reading error (PROV-9 keeps them as the published rows).
- Priority: gap + (multiclass classification is thin, 24 of 173 accepted), use case 0 (the source is a database paper and names no actor), source + (a paper, a schema, a DOI per data point), shape + (4,438 rows with mixed types), risk 0.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark ChemPile (https://arxiv.org/abs/2505.12534).
- as published: 4,438 diblock measurements in ChemNLP; the BCDB holds over 5,400 phase measurements; in ChemPile-LIFT 22,190 text prompts over 1 config(s); target: phase1 (ordered morphology: lamellar, cylinder, gyroid, disordered, ...).
- Why: Predict the self-assembled phase of a di-block copolymer melt from composition, molar mass and temperature
- Notes: Block Copolymer Database (BCDB), Rebello et al. 2024 (J Chem Inf Model 64:6118), Olsen lab at MIT, hand-curated from the literature with a DOI per data point (so rows group by paper). Features: BigSMILES of the two blocks, volume fraction f1, Mn, dispersity, temperature. A real experimental multiclass table outside ...
