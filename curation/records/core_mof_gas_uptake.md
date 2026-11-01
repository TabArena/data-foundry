---
unique_name: core_mof_gas_uptake
name: core_mof_no_topo
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
- https://doi.org/10.1021/cm502594j
- 'https://huggingface.co/datasets/jablonkagroup/chempile-lift/tree/main/core_mof_no_topo ; ChemNLP builder https://github.com/OpenBioML/chemnlp/tree/main/data/tabular/core_mof_no_topo ; original: https://huggingface.co/datasets/kjappelbaum/chemnlp-core-mof ; CoRE MOF database'
- https://arxiv.org/abs/2505.12534
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`AHDS (Artifical/Handmade/Deterministic/Simulated)`, SEL-16, with `Too Small`, TP-5): every target is a simulator's output and the cut holds 142 structures.
- Source: CoRE MOF (Chung et al., Chem Mater 26:6185, 2014, https://doi.org/10.1021/cm502594j), with the adsorption properties added in Jablonka, Rosen, Krishnapriyan and Smit, "An Ecosystem for Digital Reticular Chemistry", ACS Cent Sci 9:563, 2023; as published in the ChemNLP cut (`core_mof_no_topo/meta.yaml`): `num_points: 142`, a CIF text column with `smiles_linkers` and `smiles_nodes`, and nine targets, each simulated: "heat of adsorption of CO2, simulated using Widom insertion", "CO2 uptake at 298 K and 15000 Pa as obtained from GCMC simulations", "simulated methane uptake at 298 K and 580000 Pa".
- Use case: screening MOFs for a gas-capture application is a real decision, but the label a model would learn here is the output of a grand-canonical Monte Carlo simulation, not a measurement (SEL-16); the structures themselves are experimental, which is what CoRE MOF contributes.
- Siblings and duplicates: `qmof_gcmc` (88 MOFs, the same simulated adsorption labels) is out for the same reason, and `qmof_quantum`, `mofdscribe_descriptions`, `mp_formation_energies`, `materials_project_properties`, `oqmd` and `nomad_structure` are the other simulated-label records of this run; `mofsimplify_mof_stability` (about 3,000 MOFs with a thermal decomposition temperature read from TGA traces) is the measured MOF task to keep instead. The full CoRE MOF database (about 14,000 structures) is the source this 142-row cut comes from (PROV-6).
- Better data: a candidate of the benchmark ChemPile; no new search in this run.
- Papers and pages: Chung et al. 2014 and 2019 (CoRE MOF), Jablonka et al. 2023 (the properties).
- Metric: none stated by the source.
- Risks for /add-dataset: none, nothing to add.
- Reject check (AI, 2026-10-31): stands. All nine targets are simulator output in the builder's own words ('heat of adsorption of CO2, simulated using Widom insertion', 'CO2 uptake at 298 K and 15000 Pa as obtained from GCMC simulations'; https://github.com/OpenBioML/chemnlp/blob/main/data/tabular/core_mof_no_topo/meta.yaml), simulated physics as in the `molecularproperties` precedent. `Too Small` does not hold and is dropped: 142 rows of a regression is a tiny-data task under TP-5 (musk, 102 molecules, kept), and a cut of the larger CoRE MOF.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark ChemPile (https://arxiv.org/abs/2505.12534).
- as published: 142 MOFs in the ChemNLP cut (the CoRE MOF database has about 14,000 structures); in ChemPile-LIFT 41,575 text prompts over 1 config(s); target: CO2 and methane uptake at given pressures, Henry coefficients, heats of adsorption.
- Why: Predict gas uptake and heat of adsorption of a metal-organic framework from its structure
- Notes: CoRE MOF (Chung et al. 2014, Chem Mater 26:6185) with properties added in the digital reticular chemistry ecosystem paper (Jablonka et al. 2023, doi 10.1021/acscentsci.2c01177). The property values are GCMC and Widom simulation output, not measurement, so the labels are simulated; also only 142 rows here. Noted for ...
