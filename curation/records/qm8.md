---
unique_name: qm8
name: qm8
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
- https://doi.org/10.1063/1.4928757
- 'https://huggingface.co/datasets/jablonkagroup/chempile-lift/tree/main/qm8 ; ChemNLP builder https://github.com/OpenBioML/chemnlp/tree/main/data/tabular/qm8 ; original: https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/gdb8.tar.gz'
- https://arxiv.org/abs/2505.12534
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`AHDS (Artifical/Handmade/Deterministic/Simulated)`, SEL-16): excitation energies and oscillator strengths computed with TDDFT and CC2, simulated chemistry with its own benchmarks, as `qm9` and `molecularproperties` (Lennart, 2026-09-23).
- Source: Ramakrishnan, Hartmann, Tapavicza and von Lilienfeld, "Electronic spectra from TDDFT and machine learning in chemical space", J Chem Phys 143:084111, 2015. Abstract: "We resolve this issue with machine learning models trained on deviations of reference second-order approximate coupled-cluster (CC2) singles and doubles spectra from TDDFT counterparts", applied "to low-lying singlet-singlet vertical electronic spectra of over 20 000 synthetically feasible small organic molecules with up to eight CONF atoms". ChemNLP's meta: "QM8 is a dataset of quantum mechanical simulations of electronic spectra and the energy levels of excited states in small molecules". As published (MoleculeNet's `gdb8.tar.gz`): E1, E2, f1, f2 at CC2, LR-TDPBE0/def2SVP and CAM-B3LYP/def2TZVP per molecule; ChemNLP states 7,015 rows (num_points), the paper "over 20 000".
- Use case: correcting or replacing an excited-state calculation; no observed outcome.
- Siblings and duplicates: `qm9` (same group, ground-state DFT, also proposed `No`), `molecularproperties` (`No`, `AHDS`, Lennart 2026-09-23). External collections: MoleculeNet (QM8), ChemPile (ChemPile-LIFT `qm8`), ChemNLP.
- Better data: no new search; a candidate of the benchmark ChemPile.
- Metric: not needed for a reject (MoleculeNet scores MAE).
- Reject check (AI, 2026-10-31): stands. Every target is a quantum-chemistry computation: 'machine learning models trained on deviations of reference second-order approximate coupled-cluster singles and doubles (CC2) spectra from TDDFT counterparts' (Ramakrishnan et al., https://arxiv.org/abs/1504.01966, abstract; https://doi.org/10.1063/1.4928757), and ChemNLP's meta calls QM8 'quantum mechanical simulations of electronic spectra'. Same facts as `molecularproperties` (CC 2026-09-23, Lennart: DFT-computed, a dedicated benchmark community); no measured spectra in the release.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark ChemPile (https://arxiv.org/abs/2505.12534).
- as published: 7,015 molecules (MoleculeNet QM8); in ChemPile-LIFT 77,165 text prompts over 1 config(s); target: E1/E2 and f1/f2 at CC2, PBE0 and CAM-B3LYP levels.
- Why: Predict excited-state energies and oscillator strengths of a small molecule
- Notes: Ramakrishnan et al. 2015, time-dependent DFT and CC2 computations on GDB-8 molecules. Simulated labels, out of scope.
