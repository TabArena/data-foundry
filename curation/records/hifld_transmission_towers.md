---
unique_name: hifld_transmission_towers
name: Transmission Towers
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
- '# STRABLE''s paper link (also its ASR row); the data are FCC ULS licence-site records, not this ASR layer (screening 2026-10-31)'
- https://hifld-geoplatform.opendata.arcgis.com/datasets/geoplatform::antenna-structure-registration/
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/transmission-towers
- https://arxiv.org/abs/2605.12292
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: FCC radio-licence site records (mostly land mobile licences, not power towers), where STRABLE predicts the filed support-structure height from licensee, location and structure type; the height is a licence attribute the licensee files, and no decision predicts it.
- Source: the first publisher is the FCC Universal Licensing System (the `url` column links each row to its ULS licence-location page on wireless2.fcc.gov); HIFLD Open repackaged ULS site data in its tower layers (STRABLE's raw file `Transmission_Towers_reduced.csv`) and went offline in August-September 2025. STRABLE's paper links the Antenna Structure Registration layer for this table (Table C.4 row 102: "Structures for wireless and broadcast transmission. The task is to predict tower height."), the same link as its row 4, but the columns are ULS site fields (`Callsign`, `LocNum`, `SupStruc`, `StrucType`, `TowReg`, `QZone`, `Nepa`). As used by STRABLE (HF parquet, previewed): 75,000 rows x 28 columns, subsampled; target `SupStruc` on a log scale; call signs WQ, WP, WR, WN dominate (fire departments, emergency districts, utilities).
- Use case: none in the source; licensees file the height with the FCC. Fit none; regime IID, with several locations per licence (`LocNum`).
- Siblings and duplicates: `fcc_antenna_structure_registration` (STRABLE's ASR table, target the structure height): 14.5% of these rows carry an ASR number in `TowReg`, so the two share some structures and the same kind of target from two FCC databases (ULS and ASR), a version question for the curator (PROV-6, PROV-7). External collections: STRABLE.
- Better data: a candidate of the benchmark STRABLE; no further search for this run's finds.
- Papers and pages: STRABLE, Blayer et al., arXiv 2605.12292 (v2, 2026-10-19), Sec. 3 and Table C.4; the FCC ULS public access files (fcc.gov refused automated requests, 403).
- Metric: none found (the FCC defines no task; STRABLE's R², App. D.1, is benchmark-wide, MET-5), so the fallback `rmse` on the height in metres; inputs none.
- Risks for /add-dataset: no task (`No Good Target (yet)`, SEL-3); the overall structure height of the HIFLD tower layers (`AllStruc`, absent from the cut) would be a near-copy of the target if restored (LEAK-10); the record's first link is STRABLE's ASR link, not this data (noted in the links; PROV-4); which HIFLD tower layer the raw file came from is not confirmed.
- Priority: gap 0, use case 0, source + (FCC ULS is a documented licence database), shape + (75,000 sites, mixed columns), risk - (no task, overlap with the ASR record).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 75,000 rows x 28 columns incl. target (STRABLE parquet); capped at 75,000 by STRABLE; target: SupStruc.
- Why: Predict the support-structure height of a transmission tower
- Notes: Raw file Transmission_Towers_reduced.csv (HIFLD cellular/broadcast transmission towers, FCC-based); the paper link points to the ASR layer (row 4), so the two may overlap in source. Subsampled by STRABLE to 75,000 rows.
