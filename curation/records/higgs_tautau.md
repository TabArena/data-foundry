---
unique_name: higgs_tautau
name: Higgs to Tau Tau (Baldi, Sadowski & Whiteson 2015)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
decision_markers:
- AHDS (Artifical/Handmade/Deterministic/Simulated)
tags:
- AI-Filled (Verify)
- 2nd Tier / Scientfic Discovery
original_source: Website
year: '2015'
domain: physics & astronomy
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: Other
source_links:
- https://mlphysics.ics.uci.edu/data/htautau/
- https://arxiv.org/abs/1410.3469
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

Dataset behind "Enhanced Higgs Boson to tau+ tau- Search with Deep Learning" (PRL 114, 111801, 2015), hosted only on the UCI physics portal (not UCI ML repo / OpenML). Readme: two gzipped CSVs, `htautau` (signal, 3.8 GB) and `ztautau` (background, 3.7 GB), "produced using Monte Carlo simulations"; "The first 10 columns are the low level features, followed by the 15 high level features" (lepton momenta, MET, jets; axial MET, scalar momentum sum, delta-phi/eta/R of the leptons, m_ll, MMC missing mass, sphericities, visible mass). Label = which file a row comes from. Event count and whether features are standardized are not in the readme; check on download.

Same pipeline and curation question as `higgs` (simulated collider events, criterion 4B); the physics target here is the real 125 GeV Higgs rather than an exotic one. Verdict should follow `higgs`. Data not inspected.
