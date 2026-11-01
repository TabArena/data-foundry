---
unique_name: mona_spectral_entropy
name: mona
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target / Scientific Discovery
tags:
- AI-Filled (Verify)
collections:
- ChemPile
source_links:
- https://doi.org/10.1021/acs.analchem.5b01114
- 'https://huggingface.co/datasets/jablonkagroup/chempile-lift/tree/main/mona ; ChemNLP builder https://github.com/OpenBioML/chemnlp/tree/main/data/tabular/mona ; original: https://mona.fiehnlab.ucdavis.edu/ ; https://huggingface.co/datasets/adamoyoung/mona'
- https://arxiv.org/abs/2505.12534
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`No Good Target / Scientific Discovery`, SEL-3, SEL-8): MoNA is a reference library of mass spectra for identifying compounds, published for no predictive task, and the ChemNLP builder that made this target says it chose spectral entropy arbitrarily.
- Source: MassBank of North America (MoNA), West Coast Metabolomics Center, UC Davis (https://mona.fiehnlab.ucdavis.edu/; registry https://doi.org/10.17616/R3ND3Z): "a metadata-centric, auto-curating repository designed for efficient storage and querying of mass spectral records ... over 200,000 mass spectral records from experimental and in-silico libraries as well as from user contributions" (re3data r3d100012318). No journal paper found for MoNA itself; the record's first link, https://doi.org/10.1021/acs.analchem.5b01114, does not resolve (doi.org 404). As cut: the Hugging Face upload adamoyoung/mona, 194,721 spectra with SMILES, InChI, instrument, ionization mode, collision energy, precursor type and two entropy columns; ChemNLP keeps the SMILES as the only input and the spectral and normalized entropy as targets.
- Use case: none. ChemNLP's transform.py (https://github.com/OpenBioML/chemnlp/blob/main/data/tabular/mona/transform.py): "Unclear with this type of data what exactly the targets should be" / "Arbitrarily chose spectral entropy since it is a continuous value". The entropy is a summary computed from each measured spectrum and changes with the instrument and collision energy of each spectrum of a compound, which a SMILES-only task does not see; MoNA also holds in-silico spectra, so part of the rows may be generated (SEL-16, not checked).
- Siblings and duplicates: `metlin_smrt_retention_time` (a measured LC-MS property used in compound identification); no duplicate. External collections: ChemPile (config `mona`).
- Better data: a candidate of the benchmark ChemPile; no further search for this run's finds.
- Papers and pages: ChemPile, arXiv 2505.12534; the ChemNLP builder (meta.yaml `bibtex: []`).
- Metric: none found (ChemNLP meta.yaml, `benchmarks: []`).
- Reject check (AI, 2026-10-31): stands. The builder that made the target says so: '# Unclear with this type of data what exactly the targets should be' / '# Arbitrarily chose spectral entropy since it is a continuous value' (https://github.com/OpenBioML/chemnlp/blob/main/data/tabular/mona/transform.py, lines 18-19), and MoNA is a 'public repository of mass spectra for small molecules' (meta.yaml, `benchmarks: []`). What MoNA serves, spectrum prediction and library search for identification, is a structured output and retrieval (SEL-9), so no tabular target can be redefined from it.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark ChemPile (https://arxiv.org/abs/2505.12534).
- as published: 194,721 spectra (ChemNLP cut of MassBank of North America); in ChemPile-LIFT 3,115,536 text prompts over 1 config(s); target: spectral entropy, normalized entropy.
- Why: Predict the spectral entropy of a compound's mass spectrum from its structure
- Notes: MassBank of North America, a public repository of measured small-molecule mass spectra. The target here is an information-theoretic summary the ChemNLP authors computed from each spectrum, not a property anyone acts on, and rows are spectra of the same compound under different instruments. Out of scope as framed; the ...
