---
unique_name: wildfireia_initial_attack_failure
name: 'WildfireIA: U.S. national benchmark for wildfire initial-attack failure prediction'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- Non-IID (Temporal)
- AI-Filled (Verify)
original_source: Other
year: '2026'
domain: environmental science & climate
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
source_links:
- https://huggingface.co/datasets/WildfireIA/Anonymous-WildfireIA
- https://arxiv.org/abs/2606.15529
- https://github.com/LabRAI/WildfireIA
- https://doi.org/10.2737/RDS-2013-0009.6
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: WildfireIA, 38,128 naturally caused US wildfires of 2016-2020 from FPA-FOD with discovery-time weather, fire danger, fuel, terrain, access, population and satellite detections, labelled initial-attack failure by final size (50 ha or more against 10 ha or less); a defined triage task with a forbidden-feature list, a chronological split and AUPRC, but a size proxy and a cut of the same fires as `fpa_fod_attributes_wildfire_size`.
- Source: Xu, Cheng, Dong, "A Nationwide Benchmark for Wildfire Initial Attack Failure Prediction with Public Environmental Data", arXiv 2606.15529 (2026-06-14); data https://huggingface.co/datasets/WildfireIA/Anonymous-WildfireIA (2.42 GB: event-level, source-level and patch-level feature tables, labels, splits and manifests, croissant.json; licence "other"; "It should not be used as a standalone operational dispatch system without agency validation"), code https://github.com/LabRAI/WildfireIA; the fires from FPA FOD, 6th edition (Short 2022, https://doi.org/10.2737/RDS-2013-0009.6). As published (paper §2 and §4.3, card): one row per natural FPA-FOD fire of 2016-2020 in the contiguous US; label 0 for a final size of 10 ha or less, 1 for 50 ha or more, the fires between excluded "to reduce label ambiguity"; inputs from FIRMS/VIIRS detections up to discovery day (D+1 onward dropped), gridMET weather and fire danger, LANDFIRE fuel, vegetation and topography, OpenStreetMap access and WorldPop; final size, containment times, MTBS ids and label-derived variables removed by a forbidden-feature manifest; a second task, log(1 + containment hours).
- Use case: fire management agencies, at discovery, triage which fires may "escape early control" for early escalation and resource prioritisation (§1, §5.5); fit direct for the triage, with a final-size proxy for the initial-attack outcome because "direct operational IA outcomes are not consistently reported" in public records (§2.1); regime temporal as the source sets it: train 2016-2018, validation 2019, test 2020, failure rates 7.55%, 6.07%, 8.32% (§4) (SPLIT-6).
- Siblings and duplicates: `fpa_fod_attributes_wildfire_size` (`TBD -> Yes`, 2): 2.3 million FPA-FOD fires of 1992-2020 with about 270 ignition-point covariates and the final size as a proposed target: the same fires and target quantity, a cut under PROV-6, so the curator decides which framing enters (this one defines the task, the prediction point and the metric; that one is larger and longer); `fpa_fod_wildfire_cause` (`TBD -> Yes`, 3): the cause, a distinct task (PROV-7); `forest_fires` (`Yes`): another source. External collections: none in our vocabulary.
- Better data: from the curator's Zotero collection (item 208); no further search this round.
- Papers and pages: Xu, Cheng, Dong 2026 (16 models; XGBoost best at AUPRC 53.3%; FIRMS/VIIRS the least redundant source, fuel the strongest static predictor).
- Metric: AUPRC as the primary metric because "escaped fires are rare and the benchmark emphasizes ranking high-risk events" (§3.2), with AUROC, Recall@5%, F1, Brier score and ECE as secondary: one deliberate choice (MET-5), so `average_precision`, weighed against MET-9 (the stated reason is ranking for triage, not imbalance alone); inputs none.
- Risks for /add-dataset: gridMET daily values of the discovery day include hours after discovery (a weak leak: note it or lag to D-1, LEAK-30 style); the excluded 10-50 ha band makes the task easier than real triage (a note in the fit, USE-8); patch-level rasters and source tables reduce to the event table (the event-level tables ship); the card's licence "other" and upstream terms (ODbL for OpenStreetMap-derived columns, EV-4); the overlap with `fpa_fod_attributes_wildfire_size` (PROV-6).
- Priority: gap 0 (environmental science, binary and temporal are covered), use case + (the source names the agencies and the triage decision), source + (arXiv paper with a data card and code), shape + (38,128 fires, about 195 mixed columns, five years), risk - (a cut of the same fires and target as another record).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 208: "A Nationwide Benchmark for Wildfire Initial Attack Failure Prediction with Public ...".
- as published: 38,128 naturally caused wildfire events (one row per fire), contiguous US, discovered 2016-2020; about 195 event-level columns (metadata 9, gridMET weather 53 and fire danger 36 for D-4..D, LANDFIRE ...; target: IA failure: 1 if final size >= 50 ha, 0 if <= 10 ha, 10-50 ha excluded (from FPA-FOD final fire size); positive rate 7.6/6.1/8.3% in train/val/test. Auxiliary ...; access: open.
- Why: Real national event records with only discovery-time inputs, a published forbidden-feature list (size, containment, MTBS ids) and a temporal split. Tree models lead (XGBoost best, AUPRC 53.3%), and the columns mix numeric and categorical types (state, county, cause, fuel and vegetation codes).
- Adds: A natural-hazard triage task with a temporal split that the collection lacks (the existing fire records are Zimbabwe monthly burned-area grids). Caveats: the label is a size proxy, not an operational IA outcome; lightning fires only; the data falls under source terms (OSM-derived features are ODbL) and the HF card ...
