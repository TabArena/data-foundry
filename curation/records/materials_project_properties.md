---
unique_name: materials_project_properties
name: mp_self_supervised
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
- https://doi.org/10.1063/1.4812323
- 'https://huggingface.co/datasets/jablonkagroup/chempile-lift/tree/main/mp_self_supervised ; ChemNLP builder https://github.com/OpenBioML/chemnlp/tree/main/data/tabular/mp_self_supervised ; original: https://materialsproject.org'
- https://arxiv.org/abs/2505.12534
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`AHDS (Artifical/Handmade/Deterministic/Simulated)`, SEL-16; also `Trivial`, SEL-5 and TP-4): a database of computed properties, and both targets are read off the same CIF that serves as the input.
- Source: the Materials Project (Jain et al., "Commentary: The Materials Project: A materials genome approach to accelerating materials innovation", APL Materials 1:011002, 2013, doi 10.1063/1.4812323), through the ChemNLP config `mp_self_supervised`, 130,542 materials. As published: identifiers `cif` (the crystal structure file) and `formula` (the reduced formula); targets `density` in g/cm3, `spacegroup` and `spacegroup_number`; "The Materials Project is a database of computed properties of materials" (ChemNLP `data/tabular/mp_self_supervised/meta.yaml`).
- Use case: none the source names. The config is a self-supervised pre-training cut (its name), and the targets are properties of the very structure handed to the model: the density is the cell's mass over its volume, and the space group is the symmetry a CIF records (SEL-5; with those inputs removed nothing of the task is left, TP-4). The structures and their properties are DFT calculations, not measurements (SEL-16).
- Siblings and duplicates: `mp_descriptions` (free-text prose about the same entries) and `mp_formation_energies` (DFT formation and decomposition energies) are the other Materials Project cuts of this run; `experimental_band_gap_zhuo` is the counter-case that stays in scope, a measured band gap on compositions. One source, different targets, so no `Duplicate` marker.
- Better data: a candidate of the benchmark ChemPile (this run searched no further).
- Papers and pages: Jain et al. 2013; materialsproject.org; the ChemNLP builder.
- Metric: none found; not needed for a rejected record.
- Risks for /add-dataset: not applicable.
- Reject check (AI, 2026-10-31): stands. The builder: 'The materials project is a dabase [sic] of computed properties of materials' (https://github.com/OpenBioML/chemnlp/blob/main/data/tabular/mp_self_supervised/meta.yaml), so structures and density are DFT results (SEL-16, precedent `molecularproperties`, CC 2026-09-23). `Trivial` also fits, since density and space group follow from the input CIF, but that is physics, not a TP-4 probe, and the reject does not need it.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark ChemPile (https://arxiv.org/abs/2505.12534).
- as published: 130,542 materials (ChemNLP cut); in ChemPile-LIFT 1,435,951 text prompts over 1 config(s); target: density, spacegroup.
- Why: Predict density and spacegroup of a material from its CIF / formula
- Notes: Materials Project (Jain et al. 2013); computed structures and properties, CIF input. Out of scope.
