---
unique_name: qmof_gcmc
name: qmof_gcmc
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
- https://doi.org/10.1016/j.matt.2021.02.015
- 'https://huggingface.co/datasets/jablonkagroup/chempile-lift/tree/main/qmof_gcmc ; ChemNLP builder https://github.com/OpenBioML/chemnlp/tree/main/data/tabular/qmof_gcmc ; original: https://github.com/kjappelbaum/mofdscribe ; QMOF database'
- https://arxiv.org/abs/2505.12534
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`AHDS (Artifical/Handmade/Deterministic/Simulated)`, SEL-16): Henry coefficients and adsorption energies from grand-canonical Monte Carlo simulation on QMOF structures, simulated data; the ChemNLP cut also has only 88 MOFs.
- Source: the QMOF structures (Rosen et al., Matter 4:1578, 2021) with gas-adsorption properties from Jablonka, Rosen, Krishnapriyan and Smit, "An Ecosystem for Digital Reticular Chemistry", ACS Cent Sci 9:563, 2023 (doi 10.1021/acscentsci.2c01177): "we used reproducible computational workflows to compute diverse gas separation properties (CO2, CH4, H2, N2, O2 isotherms; H2S, H2O, Kr, Xe Henry coefficient ...) for nearly seven thousand materials from the QMOF database"; Methods, "Molecular Simulations": "All grand-canonical Monte Carlo simulations for the reference data set were performed using the RASPA code, describing the force-field as a rigid framework with the UFF force field"; "The new data set of predicted properties derived from grand canonical Monte Carlo simulations reported with this work is available on the MaterialsCloud". ChemNLP's meta: "Jablonka et al. added gas adsorption properties"; its transform keeps the rows complete in 45 columns: 88 MOFs.
- Use case: a surrogate for the simulation in computational screening of adsorbents; no observed uptake.
- Siblings and duplicates: `qmof_quantum` (the same structures with DFT electronic properties, another task, PROV-7; also proposed `No`); `core_mof_gas_uptake` (CoRE MOF with simulated uptake, the same ecosystem paper, screen batch 02); `mofdscribe_descriptions` (batch 04); `mofsimplify_mof_stability` is the measured counter-case. External collections: ChemPile (ChemPile-LIFT `qmof_gcmc`), ChemNLP, mofdscribe.
- Better data: no new search; a candidate of the benchmark ChemPile.
- Reject check (AI, 2026-10-31): stands. Jablonka et al. 2023, Methods, 'Molecular Simulations': 'All grand-canonical Monte Carlo simulations for the reference data set were performed using the RASPA code, describing the force-field as a rigid framework with the UFF force field' (https://doi.org/10.1021/acscentsci.2c01177): every target is simulator output on DFT structures, as `core_mof_gas_uptake` in rejects_01. The 88 MOFs of the ChemNLP cut would not rescue it either.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark ChemPile (https://arxiv.org/abs/2505.12534).
- as published: 88 MOFs (ChemNLP); in ChemPile-LIFT 5,046 text prompts over 1 config(s); target: log10 Henry coefficients and adsorption energies per gas.
- Why: Predict gas adsorption properties (Henry coefficients, adsorption energies) of a MOF
- Notes: QMOF (Rosen et al. 2021, Matter 4:1578) with GCMC-computed adsorption added by Jablonka et al. Labels are simulation output and there are 88 rows. Out of scope.
