---
unique_name: orchid_organ_procurement
name: 'ORCHID: Organ Retrieval and Collection of Health Information for Donation'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
decision_markers:
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
original_source: Other
year: '2023'
domain: medical & healthcare
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.13026/b1c0-3506
- https://physionet.org/content/orchid/2.1.1/
- https://doi.org/10.13026/rfeq-j318
- https://doi.org/10.1038/s41597-025-06435-1
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: 133,101 referrals of ventilated patients for organ donation at six US organ procurement organisations (OPOs), 2015-2021, with whether each became a donor; a large, documented process dataset with a decision at referral, behind a data use agreement and with event tables to join.
- Source: Adam, Suriyakumar, Pollard, Moody, ..., Wilson and Ghassemi, ORCHID on PhysioNet (v1.0.0 2023-07-25; v2.1.1 2025-09-29, doi 10.13026/rfeq-j318; the record's doi 10.13026/b1c0-3506 belongs to an earlier version, not checked), built with the Federation of American Scientists and six OPOs; data paper "Organ retrieval and collection of health information for donation: The ORCHID dataset", Sci. Data 13:120 (2026, doi 10.1038/s41597-025-06435-1). As published: `referrals.csv`, one row per patient (`PatientID`, 38 columns: demographics, cause of death, timestamps of approach, authorization, procurement and death, the outcomes approached, authorized and procured, and the outcome of each recovered organ); seven OPO event tables linked by `PatientID` (chemistry, CBC, arterial blood gas, serology, cultures, haemodynamics, fluid balance); `CalcDeaths.csv` and a data dictionary. 133,101 referrals and 8,972 donations; 12,516 to 33,641 referrals per OPO.
- Use case: when a hospital refers a ventilated patient, the OPO decides whether to send staff to evaluate and pursue the case (the paper: "The detailed clinical data available in ORCHID enables prediction of outcomes such as transplant"; "These models may form the basis of decision-support tools that may ultimately be deployed in OPOs"); fit direct for a model on the referral row and the labs charted before a fixed cut-off. Regime temporal (an OPO applies the model to its later referrals, dated 2015-2021) or grouped by OPO for a new OPO (USE-10); the curator picks one.
- Siblings and duplicates: no other ORCHID, OPO or referral record (grep: orchid, organ procurement, organ donor); `optn_liver_waitlist_90day_mortality` and `optn_kidney_delayed_graft_function` are transplant tasks downstream of procurement. External collections: none found.
- Better data: from the curator's Zotero collection, item 80; no new search this run.
- Papers and pages: the PhysioNet page; the Sci. Data paper (PMC12855849: Background, Usage Notes, Table 1), which also proposes to "audit both the efficiency and equity of the current procurement process".
- Metric: none found (the PhysioNet page, the paper's Usage Notes), so the fallback `roc_auc` (MET-1, MET-8); inputs none.
- Risks for /add-dataset: fix the prediction point at the referral and keep every later timestamp and event out (approach, authorization, procurement; LEAK-10, USE-3); choose the target (a donor with an organ transplanted, or procured; USE-5): an authorization target would make the family's consent the label and needs an ethics look first (SEL-1); OPOs cover different years (OPO 2 starts 2018) and practice differs by OPO; "implausible values" were left raw by design; event tables to aggregate up to the cut-off; access by the PhysioNet restricted-data use agreement (noted only, EV-4).
- Priority: gap 0 (medical & healthcare, binary and temporal are not thin), use case + (the paper names decision support for OPOs and the outcome to predict), source + (PhysioNet with a data dictionary and a Sci. Data paper), shape + (133,101 referrals, mixed types, dated, six OPOs), risk - (event tables to join and a prediction point to fix).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 80: "PhysioNet".
- as published: 133,101 referred potential donors from 6 OPOs, 2015-2021, ten CSV tables (referrals, OPO events, deaths) linked by PatientID; target: whether a referral leads to authorisation or procurement of a transplantable organ; access: registration.
- Why: First multi-centre organ-procurement data, real process outcomes, a decision at the referral point; OPO gives a grouped split.
- Adds: Transplant logistics, a domain absent from the records. Caveats: restricted DUA, tables must be joined, the prediction point must be fixed carefully.
