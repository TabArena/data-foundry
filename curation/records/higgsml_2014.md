---
unique_name: higgsml_2014
name: Higgs Boson Machine Learning Challenge (HiggsML, ATLAS / Kaggle 2014)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- AHDS (Artifical/Handmade/Deterministic/Simulated)
tags:
- AI-Filled (Verify)
- 2nd Tier / Scientific Discovery
original_source: Kaggle
year: '2014'
domain: physics & astronomy
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://opendata.cern.ch/record/328
- https://www.kaggle.com/c/higgs-boson
- http://proceedings.mlr.press/v42/cowa14.pdf
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 2: the proposed fast reject (SEL-16 (PROV-3)) did not hold in the reject check, so it stays a candidate with the doubt listed.
- Proposed reject (refuted): `No` (`AHDS (Artifical/Handmade/Deterministic/Simulated)`, SEL-16): ATLAS full-detector Monte Carlo events of the 2014 HiggsML challenge, simulated physics with its own benchmark.
- Source: ATLAS collaboration, CERN Open Data record 328 (2014, CC0): "built from official ATLAS full-detector simulation", "an extended version of the data provided for the Higgs Boson Machine Learning Challenge on Kaggle"; 818,238 events, 35 columns (EventId, 13 `DER_*`, 17 `PRI_*`, Weight, Label, KaggleSet, KaggleWeight); Kaggle used 250,000 training events; undefined values are -999.0.
- Use case: event selection for an H -> tau tau search; the label is Monte Carlo truth; regime IID within the simulation.
- Siblings and duplicates: `higgs` (Lennart, 2026-09-22: No, `AHDS`, `Not Representative`), `higgs_tautau` and `fair_universe_higgsml_uncertainty` (AI, 2nd Tier, `AHDS`), `fair_higgs_boson_decay` (AI, No). Not a duplicate of UCI `higgs` (other process, other simulation).
- Papers and pages: Adam-Bourdarios et al., "The Higgs boson machine learning challenge", JMLR W&CP 42 (2015); Kaggle `higgs-boson` (2014, 1,785 teams).
- Metric: AMS on the weighted selection (Kaggle evaluation, paper Sec. 4), deliberate; needs Weight, which ships; the paper, Sec. 2.2: "classification accuracy is a very poor measure of success in this case".
- Counterpoint for the checker: physics & astronomy has no accepted dataset (gap), and unlike `higgs` this release carries the physics metric (weights and AMS), which answers part of the curator's metric argument on `higgs`; the simulation itself (SEL-16, "Higgs" in its Cases) still decides.
- Reject check (AI, 2026-10-22): does not stand. The release is simulated ("built from official ATLAS full-detector simulation", https://opendata.cern.ch/record/328). But the curator's higgs No rested on the missing physics objective ("AUC on balanced classes, which is not the physics objective"), and named HiggsML 2014, with event weights and AMS, as the field's benchmark that encodes "exactly what this one omits". This dataset carries those weights and the AMS. The curator also wrote that training on simulation "is the real workflow". So the higgs precedent does not carry over as it stands. Whether SEL-16's "simulated physics that has its own benchmarks" excludes the field's benchmark itself is a reading for the curator, not a clear failure. Judged together with the other three: they share higgs's facts; this one differs on exactly the fact the curator named.
- For /add-dataset: TBD -> 2nd Tier, priority 2 (gap + physics & astronomy; source + CERN Open Data CC0; risk - SEL-16 reading). A weighing call for the curator first: is HiggsML 2014 in scope under SEL-16? If yes, the add stage must check: AMS on the weighted selection as the metric (MET-4; Weight as a scoring column, never a feature); use the KaggleSet split (t/b/v) or justify IID; -999.0 to missing; whether KaggleWeight or Weight is the scoring weight; and that `fair_universe_higgsml_uncertainty` is not the better successor version (TP-6).

The Kaggle HiggsML challenge (2014, 1785 teams), a *different* dataset from UCI `higgs`: ATLAS full detector simulation, H -> tau tau signal at 125 GeV vs Z -> tau tau, t tbar and W backgrounds. Full release on CERN Open Data record 328 (CC0): 818,238 events, 30 features (`DER_*` derived, `PRI_*` primary) plus EventId, Weight, Label, KaggleSet (t/b/v/u) and KaggleWeight; Kaggle used 250,000 training events. Undefined values are coded -999.0 (challenge doc, Appendix B: "their value is -999.0, which is outside the normal range of all variables") -> convert to NA.

Why it is not a plain classification set (Adam-Bourdarios et al., JMLR W&CP 42): the simulation is enriched in signal while real S/B is ~2/1000, so every event carries an importance weight and the metric is the Approximate Median Significance (AMS) on the weighted selection; Sec. 2.2: "classification accuracy is a very poor measure of success in this case. Indeed, the AMS is not a function of classification accuracy." Weight must never be a feature. An unweighted AUC task on Label is possible but is a different, less physical task; still simulated (criterion 4B). This is what the old `higgs` comment about a "challenge with special evaluation/postprocessing" referred to. Kaggle discussion threads not read here (forum links in the write-up). Data not inspected.
