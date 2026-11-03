---
unique_name: nomad_structure
name: nomad_structure
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- AHDS (Artifical/Handmade/Deterministic/Simulated)
tags:
- AI-Filled (Verify)
collections:
- ChemPile
source_links:
- https://doi.org/10.1557/mrs.2018.208
- 'https://huggingface.co/datasets/jablonkagroup/chempile-lift/tree/main/nomad_structure ; ChemNLP builder https://github.com/OpenBioML/chemnlp/tree/main/data/tabular/nomad_structure ; original: https://nomad-lab.eu'
- https://arxiv.org/abs/2505.12534
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`AHDS (Artifical/Handmade/Deterministic/Simulated)`, SEL-16): DFT-modelled structures, and targets (density, crystal system, space group, point group) that are geometric functions of the input CIF; precedent `molecularproperties` (`No`, CC 2026-09-23, Lennart).
- Source: NOMAD, Draxl and Scheffler, "NOMAD: The FAIR concept for big data-driven materials science", MRS Bull. 43:676, 2018 (https://doi.org/10.1557/mrs.2018.208); Scheidgen et al., JOSS 8:5388, 2023. As cut by ChemNLP (https://github.com/OpenBioML/chemnlp/blob/main/data/tabular/nomad_structure/meta.yaml) from the Hugging Face upload n0w0f/nomad-structure-csv: "A subset from NOMAD dataset, which is a database of DFT computed results of materials ... All materials in this dataset are modeled using Density Functional Theory using GGA functional."; 527,984 rows, inputs `cif` and `formula`; targets density (kg/m^3), crystal system, space group, point group, space-group number.
- Use case: none; a symmetry analysis of the CIF's cell and atoms gives the space group, point group and crystal system, and its cell mass and volume give the density, so the input yields the label (SEL-5).
- Siblings and duplicates: `oqmd`, `mp_formation_energies`, `materials_project_properties` (DFT materials databases of this run; `materials_project_properties` asks the same density and space group of Materials Project entries); `molecularproperties` (`No`, DFT). External collections: ChemPile (config `nomad_structure`).
- Better data: a candidate of the benchmark ChemPile; no further search for this run's finds.
- Papers and pages: Draxl and Scheffler 2018; Scheidgen et al. 2023; ChemPile, arXiv 2505.12534.
- Metric: not looked up (out of scope).
- Reject check (AI, 2026-10-31): stands. 'All materials in this dataset are modeled using Density Functional Theory using GGA functional' (https://github.com/OpenBioML/chemnlp/blob/main/data/tabular/nomad_structure/meta.yaml), and the targets (density, crystal system, space group, point group) are properties of the input CIF; SEL-16 with the `molecularproperties` precedent.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark ChemPile (https://arxiv.org/abs/2505.12534).
- as published: 527,984 structures (ChemNLP cut of NOMAD); in ChemPile-LIFT 12,671,592 text prompts over 1 config(s); target: density, crystal system, spacegroup, point group.
- Why: Predict density and crystal system / spacegroup of a bulk material from its CIF
- Notes: NOMAD repository of DFT calculations; the inputs are CIF structure files and the properties come from the computed structures, so neither the features nor the labels are an observed tabular measurement. Out of scope.
