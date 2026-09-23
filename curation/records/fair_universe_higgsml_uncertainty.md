---
unique_name: fair_universe_higgsml_uncertainty
name: FAIR Universe HiggsML Uncertainty Challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
decision_markers:
- AHDS (Artifical/Handmade/Deterministic/Simulated)
tags:
- AI-Filled (Verify)
- 2nd Tier / Scientfic Discovery
original_source: Website
year: '2024'
domain: physics & astronomy
required_split:
- Custom
problem_type: Other
original_data_state: One Table
source_links:
- https://arxiv.org/abs/2410.02867
- https://zenodo.org/records/15131565
- https://github.com/FAIR-Universe/FAIR_Universe_dataset
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

NeurIPS 2024 competition dataset (Bhimji et al., arXiv 2410.02867), the HEP community's successor to HiggsML 2014. 13 TeV pp collisions, Pythia 8.2 + Delphes 3.5.0 with an ATLAS-like detector; H -> tau tau signal vs Z -> tau tau, diboson and t tbar (DetailedLabel). 28 tabular features (13 `PRI_*`, 15 `DER_*`) plus Weight, Label, DetailedLabel; 280M training events, 120M held-out; public zip 15.1 GB on Zenodo, CC BY 4.0 (2025-04-03).

Native task is not classification: participants return a 68.27% confidence interval on the Higgs signal strength mu for pseudo-experiments whose data are shifted by six nuisance parameters (systematics); paper Sec. 3.2 on the limits ("known unknowns" only). A Label-classification reframing would discard weights and systematics, i.e. the point of the dataset, and the data are simulated (criterion 4B). Listed in the HEP-ML living review Datasets section. Data not inspected.
