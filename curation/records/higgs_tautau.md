---
unique_name: higgs_tautau
name: Higgs to Tau Tau (Baldi, Sadowski & Whiteson 2015)
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- AHDS (Artifical/Handmade/Deterministic/Simulated)
- Not Representative
tags:
- AI-Filled (Verify)
- 2nd Tier / Scientific Discovery
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

**Screening (AI, 2026-10-22):** `No` (`AHDS (Artifical/Handmade/Deterministic/Simulated)`, `Not Representative`; SEL-16): two Monte Carlo files, signal and background, from the same group and pipeline as `higgs`, which the curator rejected.
- Source: UCI physics portal (mlphysics.ics.uci.edu/data/htautau/), files dated 2017-01-03, for Baldi, Sadowski & Whiteson, "Enhanced Higgs Boson to tau+ tau- Search with Deep Learning", Phys. Rev. Lett. 114, 111801 (2015). The readme: "The data has been produced using Monte Carlo simulations. The first 10 columns are the low level features, followed by the 15 high level features"; files `htautau.txt.gz` (signal, 3.8 GB) and `ztautau.txt.gz` (background, 3.7 GB); the label is which file a row comes from; the event count is not stated.
- Unlike `higgs`, the signal is the observed 125 GeV Higgs; the curator's reason for `higgs` (simulation-vs-simulation on a class balance set by construction, not the physics objective) applies unchanged. The field's benchmark for this very channel is HiggsML 2014 (`higgsml_2014`), with event weights and the AMS.
- Precedent: `higgs` (Lennart, 2026-09-22: `No`, `AHDS (Artifical/Handmade/Deterministic/Simulated)`, `Not Representative`; simulation-vs-simulation separability on balanced classes is not the physics objective, and the field has its own benchmarks: HiggsML 2014, FAIR Universe).
- Siblings: `higgs` (`No`), `susy`, `hepmass`, `higgsml_2014`, `fair_universe_higgsml_uncertainty`, `fair_higgs_boson_decay`.
- Reject check (AI, 2026-10-22): stands. readme: "The data has been produced using Monte Carlo simulations" (https://mlphysics.ics.uci.edu/data/htautau/readme.txt), two files whose label is the file. The curator's reason for higgs (simulation-vs-simulation separability without weights or AMS) applies unchanged; the real 125 GeV signal does not touch that reason. SEL-16 and the higgs precedent.

Dataset behind "Enhanced Higgs Boson to tau+ tau- Search with Deep Learning" (PRL 114, 111801, 2015), hosted only on the UCI physics portal (not UCI ML repo / OpenML). Readme: two gzipped CSVs, `htautau` (signal, 3.8 GB) and `ztautau` (background, 3.7 GB), "produced using Monte Carlo simulations"; "The first 10 columns are the low level features, followed by the 15 high level features" (lepton momenta, MET, jets; axial MET, scalar momentum sum, delta-phi/eta/R of the leptons, m_ll, MMC missing mass, sphericities, visible mass). Label = which file a row comes from. Event count and whether features are standardized are not in the readme; check on download.

Same pipeline and curation question as `higgs` (simulated collider events, criterion 4B); the physics target here is the real 125 GeV Higgs rather than an exotic one. Verdict should follow `higgs`. Data not inspected.
