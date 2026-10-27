---
unique_name: susy
name: SUSY
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- AHDS (Artifical/Handmade/Deterministic/Simulated)
tags:
- AI-Filled (Verify)
- 2nd Tier / Scientific Discovery
original_source: UCI
year: '2014'
domain: physics & astronomy
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C54606
- https://archive.ics.uci.edu/dataset/279/susy
- https://arxiv.org/abs/1402.4735
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`AHDS (Artifical/Handmade/Deterministic/Simulated)`, SEL-16): simulated collider events, the second benchmark of the paper behind `higgs`, which the curator rejected on the same ground.
- Source: Baldi, Sadowski & Whiteson 2014 (arXiv 1402.4735), UCI donated 2014-02-11 (https://archive.ics.uci.edu/dataset/279/susy): "The data has been produced using Monte Carlo simulations"; 5,000,000 events, 8 low-level and 10 derived features, label = simulated signal (chargino pair) vs background.
- Use case: physics analyses train on simulation, but the benchmark scores simulation-vs-simulation separability on balanced classes, as for `higgs` (CC 2026-09-22, Lennart).
- Siblings and duplicates: `higgs` (`No`, Lennart; SEL-16 Cases), `hepmass`, `higgs_tautau` (same group and pipeline). Not a duplicate of `higgs` (different process), but the same verdict applies.
- Metric: AUC reported in the paper (one of several measures).
- Reject check (AI, 2026-10-22): stands. SEL-16 (Must, Cases: Higgs): UCI https://archive.ics.uci.edu/dataset/279/susy: "The data has been produced using Monte Carlo simulations"; the second benchmark of the same paper (arXiv 1402.4735) and pipeline as higgs, which Lennart rejected (CC 2026-09-22) as simulated physics with dedicated benchmarks scored as balanced sim-vs-sim AUC. No fact sets SUSY apart (like cases alike).

Second benchmark of the same paper as `higgs` (Baldi, Sadowski & Whiteson 2014, arXiv 1402.4735, "Benchmark Case for Supersymmetry Particles (SUSY)", p. 4-5): 5M fully simulated 8 TeV events (MadGraph5 + Pythia + Delphes), signal = chargino pair production "chi+- -> W chi0" with "m chi+- = 200 GeV and m chi0 = 100 GeV", background = W-pair production; final state two leptons + missing momentum. 8 low-level + 10 high-level features, 46% signal, last 500k rows = test set (UCI, donated 2014-02-11, CC BY 4.0). Features are globally standardized the same way as `higgs` (p. 10), same judgement applies. Paper reports little gain from deep nets or high-level features here (AUC ~0.87-0.88, Table II, p. 8), i.e. a smoother, less feature-hungry task than `higgs`.

Not a duplicate of `higgs` (different process and feature set), but the same pipeline and the same curation question, so the verdict should follow whatever is decided for `higgs` (see its 2026-09-22 comment: simulated physics with dedicated benchmarks, criterion 4B). Data not inspected here beyond the UCI page.
