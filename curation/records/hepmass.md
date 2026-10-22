---
unique_name: hepmass
name: HEPMASS
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- AHDS (Artifical/Handmade/Deterministic/Simulated)
- Not Representative
tags:
- AI-Filled (Verify)
- 2nd Tier / Scientfic Discovery
original_source: UCI
year: '2016'
domain: physics & astronomy
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C5PP5W
- https://archive.ics.uci.edu/dataset/347/hepmass
- https://arxiv.org/abs/1601.07913
- https://mlphysics.ics.uci.edu/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`AHDS (Artifical/Handmade/Deterministic/Simulated)`, `Not Representative`; SEL-16): simulated collider events, the same group, pipeline and question as `higgs`, which the curator rejected.
- Source: UCI 347 "HEPMASS", donated 2016-01-27 (Whiteson group), with Baldi, Cranmer, Faucett, Sadowski, Whiteson, "Parameterized Machine Learning for High-Energy Physics" (arXiv 1601.07913). UCI: the signatures "are learned from Monte Carlo simulations of the collisions that produce these particles and the resulting decay products"; 10.5M events, three variants (`1000`, `not1000`, `all`), each 7M train / 3.5M test, "50% of the data is from a signal process, while 50% is from the background process", 27 normalized features plus a mass that for background rows is "selected randomly".
- Label: Monte Carlo truth of a hypothetical new particle, balanced by construction; the mass column is a hypothesis parameter, not a measurement.
- Precedent: `higgs` (Lennart, 2026-09-22: `No`, `AHDS (Artifical/Handmade/Deterministic/Simulated)`, `Not Representative`; simulation-vs-simulation separability on balanced classes is not the physics objective, and the field has its own benchmarks: HiggsML 2014, FAIR Universe).
- Siblings: `higgs` (`No`), `susy`, `higgs_tautau` (same group; open), `higgsml_2014`, `fair_universe_higgsml_uncertainty`, `fair_higgs_boson_decay`.
- Reject check (AI, 2026-10-22): stands. Same group, pipeline and setup as higgs (the curator's No, 2026-09-22; SEL-16 Cases "Higgs"): UCI 347, "learned from Monte Carlo simulations" and "50% of the data is from a signal process", balanced by construction, with a hypothesised-mass column (https://archive.ics.uci.edu/dataset/347/hepmass). No fact sets it apart from higgs.

Third UCI benchmark from the Whiteson group, same simulation family as `higgs` / `susy`. UCI page: 10.5M Monte Carlo events, "27 normalized features (22 low-level and 5 high-level)" plus a mass feature; 50% signal; three variants: `1000` (signal mass fixed at 1000, no mass feature), `not1000` (mass drawn from {500, 750, 1250, 1500}) and `all` ({500, ..., 1500}); background rows get a mass drawn at random from the same set; 7M train / 3.5M test per variant; donated 2016-01-27, CC BY 4.0. Associated paper per the UCI physics portal: Baldi, Cranmer, Faucett, Sadowski, Whiteson, "Parameterized Machine Learning for High-Energy Physics" (arXiv 1601.07913).

Curation notes: the mass column is a *hypothesis parameter*, not a measurement (random noise for background by construction), so a plain classifier on `all` mixes five tasks; `1000` is the clean single-task variant. Features are "normalized" like `higgs` (global standardization, judged harmless there). Simulated physics with dedicated benchmarks (criterion 4B): verdict should follow `higgs`. Data not inspected.
