---
unique_name: wri_us_school_bus_fleets
name: US School Bus Fleet
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
original_source: Website
year: '2022'
problem_type: Regression
source_links:
- https://datasets.wri.org/dataset/usa-school-bus-fleets
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/us-school-bus-fleet
- https://arxiv.org/abs/2605.12292
- https://doi.org/10.46830/writn.22.00076.v2
- '# version 3 (May 2024) on the WRI data portal (zip, 84 MB)'
- https://datasets.wri.org/private-admin/dataset/933d7fd5-6ef3-47b9-acfa-d723e33ff0a9/resource/c45be134-6f0d-4d61-a5c9-4233599cf59c/download/dataset_us_school_bus_fleets_v3_may_2024.zip
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: WRI's inventory of more than 475,000 US school buses from state records is real and documented, but STRABLE's target, a bus's age, is a recorded attribute that its own columns compute in half of its rows, and no decision is made on it.
- Source: WRI Electric School Bus Initiative; Lazer, Freehafer and Wang, "Dataset of U.S. School Bus Fleets", technical note of December 2022, v2.0 of May 2024 (https://doi.org/10.46830/writn.22.00076.v2); data versions 1 (December 2022), 2 (February 2023) and 3 (May 2024) on the WRI data portal, CC BY 4.0. As published (technical note, Sec. 1): "The dataset includes over 475,000 buses and over 11,000 entities", from records requests to 46 states and DC "between March and November 2022"; "approximately 30 variables", and "The specific data available vary by state"; 41 state files are bus-level and 7 district-level. The STRABLE copy holds 17,011 buses of four states only (Connecticut 8,744, South Dakota 3,583, Maine 2,807, Washington 1,877) x 19 columns, target `Bus age` as ln(years). The record's first link (datasets.wri.org/dataset/usa-school-bus-fleets) returns 404 on 2026-10-31; the DOI and the portal's v3 file work.
- Use case: none for predicting a bus's age: the note's uses are "identifying school districts with the oldest and probably most polluting school buses", emission and health estimates for electrification, and grid planning (Abstract), all uses of the recorded age, not predictions of it (`No Good Target (yet)`). For example, imputing the age of buses a state reports without a year; fit approximate at best. Regime grouped by state if that use holds, since states record age differently ("states used different dates to indicate age, such as 'Purchase Date' (Iowa), 'Build Date' (Florida), or 'Date Into Operation' (Georgia)", Sec. 4).
- Siblings and duplicates: no record holds school bus data; WRI's "Dataset of Electric School Bus Adoption in the United States" (Lazer, Freehafer and Zepka, v9, 2025) is a separate table without a record. External collections: STRABLE (config `us-school-bus-fleet`; its paper row 103 links the HIFLD school buses layer and says "The task is to predict bus counts", while the config's source is WRI and its target `Bus age`, a mismatch of that copy, PROV-15).
- Better data: a candidate of the benchmark STRABLE; no new search in this run.
- Papers and pages: the technical note above (https://www.wri.org/research/technical-note-dataset-us-school-bus-fleets); STRABLE, Blayer et al. 2026 (https://arxiv.org/abs/2605.12292), App. C.4.
- Metric: none found (the technical note, the WRI data portal); STRABLE's R^2 on its transformed scale (App. D.1, "Evaluation metrics") is benchmark-wide, so the fallback `rmse` on log age; inputs none (MET-1, MET-5).
- Risks for /add-dataset: the target is computed from shipped columns: in Connecticut `Bus age` equals 2023 minus `Model year` for all 8,744 buses, and the VIN's tenth character encodes the model year (it matches on 88.6% of the 10,484 17-character VINs; WRI itself "used the VIN to look up the model year" for about 6,700 buses, Sec. 3), so both go (SEL-5, LEAK-10); in Washington the age differs from 2023 minus the model year on 94% of buses (by -28 to +3 years), so what age means varies by state (USE-5); STRABLE's four-state cut is not WRI's release, so a build starts from the v3 file (PROV-8); district and entity ids repeat across buses (LEAK-17).
- Priority: gap 0, use case 0, source + (WRI technical note), shape + (17,011 buses in the cut, over 475,000 in the release, mixed types), risk - (a target computed from its own columns, and no decision on it).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 17,011 rows x 19 columns incl. target (STRABLE parquet); target: Bus age.
- Why: Predict the age of a school bus from the fleet record
- Notes: Mismatch: the paper links HIFLD school buses, but the config source is WRI and the raw file is 'Dataset of U.S. School Bus Fleets_FULL_v3_2024-05-10.xlsx'. The script docstring says 'whether the age is known (classification)'; the config target is 'Bus age' (regression).
