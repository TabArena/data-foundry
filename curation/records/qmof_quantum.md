---
unique_name: qmof_quantum
name: qmof_quantum
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
- 'https://huggingface.co/datasets/jablonkagroup/chempile-lift/tree/main/qmof_quantum ; ChemNLP builder https://github.com/OpenBioML/chemnlp/tree/main/data/tabular/qmof_quantum ; original: https://github.com/kjappelbaum/mofdscribe ; QMOF database'
- https://arxiv.org/abs/2505.12534
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`AHDS (Artifical/Handmade/Deterministic/Simulated)`, SEL-16): band gaps and band edges of MOFs from DFT (PBE, HLE17, HSE06), simulated materials data whose source names graph networks as the tool, as `qm9` and `molecularproperties`.
- Source: Rosen et al., "Machine learning the quantum-chemical properties of metal-organic frameworks for accelerated materials discovery" (ChemRxiv 2020-10-29, doi 10.26434/chemrxiv.13147616; Matter 4:1578, 2021). Abstract: "we have developed the first publicly available quantum-chemical database for MOFs (the "QMOF database"), which consists of properties derived from density functional theory (DFT) for over 14,000 experimentally synthesized MOFs" and "crystal graph convolutional neural networks are capable of achieving superior predictive performance, making it possible to circumvent computationally expensive quantum-chemical calculations". As published: CIF structures with DFT properties; the ChemNLP cut (Hugging Face kjappelbaum/chemnlp-qmof-data, rows complete at all three levels of theory) holds 1,986 MOFs, with the pore diameters (PLD, LCD) and density, which are computed from the structure too.
- Use case: a surrogate for the DFT band gap in computational screening of MOFs; no observed outcome.
- Siblings and duplicates: `qmof_gcmc` (the same QMOF structures with simulated adsorption, another task, PROV-7; also proposed `No`); ChemPile MOF siblings `core_mof_gas_uptake` (screen batch 02) and `mofdscribe_descriptions` (batch 04); `mofsimplify_mof_stability` is the measured counter-case (TGA). DFT precedent: `molecularproperties` (`No`, `AHDS`, Lennart 2026-09-23). External collections: ChemPile (ChemPile-LIFT `qmof_quantum`), ChemNLP, mofdscribe.
- Better data: no new search; a candidate of the benchmark ChemPile.
- Reject check (AI, 2026-10-31): stands. QMOF 'consists of properties derived from density functional theory (DFT) for over 14,000 experimentally synthesized MOFs' (Rosen et al., https://doi.org/10.1016/j.matt.2021.02.015); the structures are real, but every target (PBE, HLE17, HSE06 band gap and edges) and the pore descriptors are computed, the `molecularproperties` precedent, as `mp_formation_energies` and `nomad_structure` in rejects_01.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark ChemPile (https://arxiv.org/abs/2505.12534).
- as published: 1,986 MOFs (ChemNLP); in ChemPile-LIFT 117,115 text prompts over 1 config(s); target: PBE/HLE17/HSE06 band gap, CBM, VBM.
- Why: Predict DFT electronic properties (band gap, band edges) of a MOF
- Notes: QMOF (Rosen et al. 2021). Every label is a DFT computation, so the target is simulated. Out of scope.
