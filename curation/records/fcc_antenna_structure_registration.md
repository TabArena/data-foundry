---
unique_name: fcc_antenna_structure_registration
name: Antenna Structure Registration
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- No Good Target (yet)
tags:
- AI-Filled (Verify)
collections:
- STRABLE
original_source: GOV Website
problem_type: Regression
original_data_state: One Table
source_links:
- https://hifld-geoplatform.opendata.arcgis.com/datasets/geoplatform::antenna-structure-registration/
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/antenna-structure-registration
- https://arxiv.org/abs/2605.12292
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: the FCC's register of antenna structures, with STRABLE's target the structure's height. The owner files that height when registering, so no decision needs it predicted.
- Source: FCC Antenna Structure Registration (ASR), served as an HIFLD Geoplatform layer (https://hifld-geoplatform.opendata.arcgis.com/datasets/geoplatform::antenna-structure-registration/); each row links to its FCC registration page (wireless2.fcc.gov, AsrSearch). The HIFLD layer page and the FCC's ASR documentation were not read in this pass. As published in STRABLE (Antenna_Structure_Registration_(ASR).csv; parquet previewed 2026-10-31): 17,633 rows x 29 columns, one registration per row; target `Strucht` (structure height, log scale); inputs registration and system ids, owner entity and contact (person's name, address, city, state, ZIP), coordinates in four encodings, location address, city and state, FAA study number, FAA circular (the marking and lighting advisory circular).
- Use case: none; the height is what the owner files with the FCC after the FAA's study, and filling in a missing height elsewhere would be imputation, not a decision. Fit none as published; regime spatial if anything.
- Siblings and duplicates: `hifld_transmission_towers` (HIFLD, from FCC license locations: licensee, call sign, `TowReg`, `SupStruc`; 75,000 rows, capped by STRABLE) is another FCC source with the same kind of target, a tower's height, and registered towers appear in both: keep at most one (PROV-6, to check on the registration number); the other `hifld_*` records share the platform only. External collections: STRABLE (Blayer et al. 2026, arXiv 2605.12292, App. C.2), "Antenna Structure Registration": "FCC registration data for antenna structures. The task is to predict the height of the structures."
- Better data: a candidate of the benchmark STRABLE; no further search this round.
- Papers and pages: STRABLE and `preprocess_HIFLD-antenna-structure-registration.py`; papers that used the data: not searched (the session's web search budget ran out).
- Metric: none found (a register, no task); STRABLE scores R2 for regression and AUROC for classification over all its tables (App. D.1), a benchmark's habit, not the source's. So the fallback, `rmse` with a log transform (MET-3, MET-8); inputs none.
- Risks for /add-dataset: the FAA circular and study tie to the height (structures above 200 ft need marking and lighting), so check whether they give it away (LEAK, TP-4); the contact columns name private persons (no feature, and handle with care); coordinates repeat in four encodings; `url`, `RegNum`, `UniqSysID` and `FID` are ids.
- Priority: gap 0 (regression not thin), use case 0, source + (a federal register with per-row FCC pages; its documentation unread), shape + (17,633 structures, mixed, spatial), risk - (no decision fits; overlap with `hifld_transmission_towers`).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 17,633 rows x 29 columns incl. target (STRABLE parquet); target: Strucht.
- Why: Predict the height of a registered antenna structure from its registration record
- Notes: HIFLD layer of the FCC Antenna Structure Registration (ASR). Overlaps in source with 'Transmission Towers' (row 102), whose paper link also points to the ASR layer.
