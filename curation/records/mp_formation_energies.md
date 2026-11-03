---
unique_name: mp_formation_energies
name: formation_energies
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
- https://doi.org/10.1038/s41524-020-00362-y
- 'https://huggingface.co/datasets/jablonkagroup/chempile-lift/tree/main/formation_energies ; ChemNLP builder https://github.com/OpenBioML/chemnlp/tree/main/data/tabular/formation_energies ; original: https://github.com/CJBartel/TestStabilityML'
- https://arxiv.org/abs/2505.12534
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`AHDS (Artifical/Handmade/Deterministic/Simulated)`, SEL-16): every label is a DFT computation of the Materials Project, simulated physics with its own benchmarks; precedent `molecularproperties` (`No`, CC 2026-09-23, Lennart: DFT-computed values are simulated data, as `higgs`).
- Source: Bartel, Trewartha, Wang, Dunn, Jain and Ceder, "A critical examination of compound stability predictions from machine-learned formation energies", npj Comput. Mater. 6:97, online 2020-07-10 (https://doi.org/10.1038/s41524-020-00362-y; arXiv 2001.10591), data at https://github.com/CJBartel/TestStabilityML. Abstract: "using the Materials Project database of DFT calculations for 85,014 unique chemical compositions". As cut by ChemNLP (meta.yaml): "Formation and decomposition energies of inorganic solids mined from the Materials Project database.", 85,014 rows, input `composition`; targets `Ef` and `Ed` (eV/atom), `stability` (boolean, read off `Ed`) and the decomposition reaction `rxn` (text).
- Use case: a materials scientist screens compositions for stability before running DFT or a synthesis, the setting Bartel et al. test; the model would learn DFT output, not a measurement.
- Siblings and duplicates: `materials_project_properties` and `mp_descriptions` (other Materials Project cuts in ChemPile, PROV-6); `oqmd`, `nomad_structure`, `qm9`, `qm8`, `qmof_quantum` (DFT siblings of this run); `molecularproperties` (`No`, DFT); `experimental_band_gap_zhuo` (measured band gaps, the in-scope counterpart). External collections: ChemPile (config `formation_energies`); Matbench carries Materials Project formation energies as its own benchmark task.
- Better data: a candidate of the benchmark ChemPile; no further search for this run's finds.
- Papers and pages: Bartel et al. 2020 (abstract read); Jain et al. 2013 (https://doi.org/10.1063/1.4812323); ChemPile, arXiv 2505.12534.
- Metric: not looked up (out of scope).
- Reject check (AI, 2026-10-31): stands. Bartel et al. work 'using the Materials Project database of DFT calculations for 85,014 unique chemical compositions' (https://arxiv.org/abs/2001.10591), and `stability` is read off the DFT `Ed`. The composition input is tabular, but SEL-16 decides on the label, and `molecularproperties` (CC 2026-09-23, Lennart) set DFT values as simulated; `experimental_band_gap_zhuo` is the measured counterpart.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark ChemPile (https://arxiv.org/abs/2505.12534).
- as published: 85,014 solids (Bartel et al. 2020, mined from the Materials Project); in ChemPile-LIFT 1,190,182 text prompts over 1 config(s); target: formation energy Ef, decomposition energy Ed, stability (boolean).
- Why: Predict formation and decomposition energy, and the stability flag, of an inorganic solid
- Notes: Labels are DFT energies from the Materials Project. Out of scope on simulated labels, even though the table itself (composition plus energies) is tabular.
