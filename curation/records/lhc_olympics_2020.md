---
unique_name: lhc_olympics_2020
name: LHC Olympics 2020 (anomaly detection challenge)
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target  / Scientific Discovery
- Wrong Domain / Source Modality
- AHDS (Artifical/Handmade/Deterministic/Simulated)
tags:
- AI-Filled (Verify)
original_source: Website
year: '2020'
domain: physics & astronomy
problem_type: Other
original_data_state: Other
source_links:
- https://lhco2020.github.io/homepage/
- https://doi.org/10.5281/zenodo.3547721
- https://doi.org/10.5281/zenodo.2629072
- https://arxiv.org/abs/2101.08320
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

Community challenge for model-agnostic anomaly detection at the LHC (Kasieczka et al., arXiv 2101.08320). Each simulated event is "a list of all hadrons (pT, eta, phi, ...) zero-padded up to 700 hadrons"; a labelled R&D dataset plus unlabelled "black boxes" that "may contain some new signal(s)". Hosted on Zenodo.

Out of scope on three counts: the task is unsupervised / weakly supervised anomaly detection, not a fixed classification or regression target; the input is a variable-length particle list, not a table; and the data are simulated (criterion 4B). Listed in the HEP-ML living review Datasets section. Data not inspected.
