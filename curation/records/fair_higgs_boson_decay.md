---
unique_name: fair_higgs_boson_decay
name: A FAIR and AI-ready Higgs boson decay dataset (CMS H(bb) jets)
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Wrong Domain / Source Modality
- AHDS (Artifical/Handmade/Deterministic/Simulated)
tags:
- AI-Filled (Verify)
original_source: Website
year: '2021'
domain: physics & astronomy
problem_type: Binary Classification
original_data_state: Other
source_links:
- https://arxiv.org/abs/2108.02214
- https://doi.org/10.1038/s41597-021-01109-0
- https://opendata.cern.ch/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

Chen et al., Scientific Data 9:31 (2022). CMS open *simulation* on the CERN Open Data Portal, released in ROOT and HDF5, CC0. One record is a jet: "the dataset consists of 3.9 million H(bb) jets and 1.9 million QCD jets". Branches are per-jet scalars plus variable-length lists of particle-flow candidates, tracks and secondary vertices ("there may be a variable number per jet"), built for jet tagging with particle-cloud / graph models.

Not a tabular task: the informative content is the variable-length constituent lists (source modality), so `Wrong Domain / Source Modality`, and it is simulated (criterion 4B). Per-jet scalar summaries could be tabulated but would recreate a weaker version of a benchmark that belongs to jet-tagging models. Data not inspected.
