---
unique_name: higgsml_2014
name: Higgs Boson Machine Learning Challenge (HiggsML, ATLAS / Kaggle 2014)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
decision_markers:
- AHDS (Artifical/Handmade/Deterministic/Simulated)
tags:
- AI-Filled (Verify)
- 2nd Tier / Scientfic Discovery
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

The Kaggle HiggsML challenge (2014, 1785 teams), a *different* dataset from UCI `higgs`: ATLAS full detector simulation, H -> tau tau signal at 125 GeV vs Z -> tau tau, t tbar and W backgrounds. Full release on CERN Open Data record 328 (CC0): 818,238 events, 30 features (`DER_*` derived, `PRI_*` primary) plus EventId, Weight, Label, KaggleSet (t/b/v/u) and KaggleWeight; Kaggle used 250,000 training events. Undefined values are coded -999.0 (challenge doc, Appendix B: "their value is -999.0, which is outside the normal range of all variables") -> convert to NA.

Why it is not a plain classification set (Adam-Bourdarios et al., JMLR W&CP 42): the simulation is enriched in signal while real S/B is ~2/1000, so every event carries an importance weight and the metric is the Approximate Median Significance (AMS) on the weighted selection; Sec. 2.2: "classification accuracy is a very poor measure of success in this case. Indeed, the AMS is not a function of classification accuracy." Weight must never be a feature. An unweighted AUC task on Label is possible but is a different, less physical task; still simulated (criterion 4B). This is what the old `higgs` comment about a "challenge with special evaluation/postprocessing" referred to. Kaggle discussion threads not read here (forum links in the write-up). Data not inspected.
