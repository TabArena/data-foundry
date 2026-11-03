---
unique_name: oqmd
name: oqmd
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
- https://doi.org/10.1007/s11837-013-0755-4
- 'https://huggingface.co/datasets/jablonkagroup/chempile-lift/tree/main/oqmd ; ChemNLP builder https://github.com/OpenBioML/chemnlp/tree/main/data/tabular/oqmd ; original: https://oqmd.org ; https://zenodo.org/records/7118055'
- https://arxiv.org/abs/2505.12534
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`AHDS (Artifical/Handmade/Deterministic/Simulated)`, SEL-16): every property is a high-throughput DFT computation, simulated physics with its own benchmarks; precedent `molecularproperties` (`No`, CC 2026-09-23, Lennart).
- Source: Saal, Kirklin, Aykol, Meredig and Wolverton, "Materials Design and Discovery with High-Throughput Density Functional Theory: The Open Quantum Materials Database (OQMD)", JOM 65:1501, online 2013-09-27 (https://doi.org/10.1007/s11837-013-0755-4); https://oqmd.org. As cut by ChemNLP (https://github.com/OpenBioML/chemnlp/blob/main/data/tabular/oqmd/meta.yaml; data https://zenodo.org/records/7118055): "a database of DFT-computed thermodynamic and structural properties of materials. We used a compilation of a prior version of this database."; 561,882 rows, inputs the OQMD id and formula; targets space group, energy, formation energy, band gap, volume and magnetization per atom, each "computed using DFT (with the PAW method as implemented in VASP) using the PBE functional".
- Use case: a materials scientist screens hypothetical compounds for stability before computing or making them; the model would learn DFT output, not a measurement.
- Siblings and duplicates: `mp_formation_energies`, `materials_project_properties`, `nomad_structure`, `qm9`, `qm8`, `qmof_quantum` (DFT siblings of this run); `molecularproperties` (`No`, DFT); `experimental_band_gap_zhuo` (measured band gaps). External collections: ChemPile (config `oqmd`).
- Better data: a candidate of the benchmark ChemPile; no further search for this run's finds.
- Papers and pages: Saal et al. 2013; Kirklin et al., npj Comput. Mater. 1:15010, 2015; ChemPile, arXiv 2505.12534.
- Metric: not looked up (out of scope).
- Reject check (AI, 2026-10-31): stands. OQMD calls itself 'a database of DFT calculated thermodynamic and structural properties' (https://oqmd.org), and each target in the builder is 'computed using DFT (with the PAW method as implemented in VASP) using the PBE functional' (https://github.com/OpenBioML/chemnlp/blob/main/data/tabular/oqmd/meta.yaml); SEL-16 with the `molecularproperties` precedent.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark ChemPile (https://arxiv.org/abs/2505.12534).
- as published: 561,882 entries (ChemNLP cut of OQMD); in ChemPile-LIFT 10,675,739 text prompts over 1 config(s); target: formation energy per atom, band gap, energy per atom, volume per atom, magnetization, spacegroup.
- Why: Predict DFT properties (formation energy, band gap, volume, magnetization) of an inorganic crystal
- Notes: Open Quantum Materials Database, Saal et al. 2013 / Kirklin et al. 2015. All properties are DFT output. Out of scope.
