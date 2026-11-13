---
unique_name: fmcsa_roadside_inspection_out_of_service
name: FMCSA MCMIS roadside inspections (out-of-service outcome)
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 3
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
original_source: GOV Website
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
source_links:
- https://data.transportation.gov/d/fx4q-ay7w
- https://data.transportation.gov/d/wt8s-2hbx
- https://data.transportation.gov/d/876r-jsdb
v2_path: datasets/_dev/tabarena-v0pt2/fmcsa_roadside_inspection_out_of_service_1m/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-11-08):** `TBD -> Yes`, priority 3: FMCSA's roadside inspection records, 8,280,108 inspections from 2023-11-08 to 2026-11-06 (a rolling three-year window) with 63 columns, from which "was the vehicle or driver put out of service" is built for the trucks inspectors pick; a federal register with a documented selection decision, and outcome columns and carrier history to handle.
- Source: Federal Motor Carrier Safety Administration, Motor Carrier Management Information System (MCMIS) inspection data, "Vehicle Inspection File" on data.transportation.gov (fx4q-ay7w, view created 2024-04-24, updated daily, rights "public"): "Violations of the Federal Motor Carrier Safety Regulations (FMCSRs) severe enough may result in a vehicle and/or driver being placed 'out-of-service'"; "Due to privacy restrictions driver information is not included". As published (Socrata API, 2026-11-08): 8,280,108 rows, `insp_date` from 2023-11-08 to 2026-11-06, 63 columns: ids (`inspection_id`, `dot_number`, `report_number`), date, start and end times, state, county, location, inspection level, facility, hazmat and cargo-tank flags, gross weight, post-accident flag, enforcement and search flags, shipper, carrier name and address, and the counts `viol_total`, `oos_total` with their driver, vehicle and hazmat parts. Companion views: Inspections Per Unit (wt8s-2hbx, 12 columns) and Vehicle Inspections and Violations (876r-jsdb, 14 columns); the carrier census is a separate file.
- The task's table: one row per inspection, 8,280,108 x the inputs known when the inspection starts (about 40 of the 63, to settle), target `oos_total > 0` (or its vehicle part), plus carrier history counted from earlier inspections; above the 1M row cap. Access open (Socrata API and CSV export, no registration).
- Use case: roadside enforcement chooses which vehicles to inspect; FMCSA's Inspection Selection System is the agency's decision aid for that choice (ISS algorithm document, ai.fmcsa.dot.gov/SMS/HelpFiles/ISS_Algorithm.pdf, not read in full), and an inspector at a weigh station decides whether to pull a truck in; fit direct for the trucks inspected: the label exists only for inspected vehicles, as repayment only for granted loans (no `Selection Bias` marker, selection.md, "Selection bias"). Regime temporal: inspections arrive in time and a model would be refit on past ones (SPLIT-6).
- Siblings and duplicates: `osha_inspection_violations` (`TBD -> Yes`, 3), `chicago_food_inspections` (`TBD -> Yes`, 4) and `labour_inspection_compliance` (`Yes`): the same kind of task at other inspectorates, no duplicate. grep: fmcsa, mcmis, roadside, motor carrier. External collections: none found.
- Better data: none searched (found by the data-scouting run of 2026-11-08).
- Papers and pages: the dataset page and its column list; the ISS algorithm document; FMCSA's MCMIS data dictionary (not read).
- Metric: none found (the dataset page states no task; the ISS ranks carriers by a score, without a metric), so the fallback `roc_auc`; inputs none.
- Risks for /add-dataset: the outcome columns (`viol_total`, `oos_total` and their parts) and fields set during or after the inspection (`insp_end_time`, `final_status_date`, `change_date`, the transaction, upload and input dates, drug interdiction searches and arrests, perhaps the enforcement flags) leave (LEAK-10); the inspection level is chosen at the start but sets how much can be found (keep, with a note); carrier history must be counted from earlier inspections only, and a census join gives today's carrier size, not that of the inspection date (LEAK-10); carrier and shipper names and numbers are identifiers or free text; the window rolls daily, so pin a snapshot (PROV-9: the year of the snapshot); this view holds three years at most.
- Priority: gap 0 (binary and temporal not thin; transport has no domain value of its own), use case + (FMCSA documents the selection decision; fit direct), source + (a federal register with column documentation), shape + (8.3M dated inspections, mixed types, carriers), risk - (outcome columns, point-in-time carrier history and joins).

Found by the data-scouting run of 2026-11-08 for the large-datasets review (wide tables outside biology and medicine, and tables with 2M+ rows).

CC (2026-11-08, Lennart): accepted for adding (`Yes`) in the screening review of the large candidates, round 2 (wide tables outside biology and medicine, tables with 2M+ rows).

**Assessment (AI, 2026-11-09):** review panel (full): ship after changes (made: `inspection_level` dropped as the level performed, LEAK-10 cl.2, 0.057-0.058 ROC AUC, so the prediction point is the selection of the vehicle; `size_weight_enf` and `traffic_enf` dropped as of unknown timing, 0.0008-0.0024; `vehicle_days_since_inspection` dropped and a LEAK-9 protocol line for the task gamer's vehicle chain, +0.010/+0.023/+0.034; cargo-tank and hazmat blanks as not applicable, NON as none, model year float; pooled-score note; the changed-records note corrected with the changed share per month, 12-16% in 2025 to 10.4%/6.2%/3.9% in the Aug/Sep/Oct 2026 test months, and the drift among never-changed records; the raw CSVs' sha256 in the notes); disputed: LEAK-24 (ship with less-corrected test labels or move the windows), CLEAN-10 (`location_desc`); the finisher's LEAK-9 check found the carrier history chains too, +0.0085/+0.0110/+0.0124 ROC AUC against noise 0.0001, so a rebuild freezing the history at the window start is proposed; for the curator: issues 1-3. Priority 3: gap 0, use case +, source +, shape +, risk - (use case: FMCSA's Inspection Selection System supports the choice, fit direct; source: FMCSA's national inspection database; shape: 1,778,366 shipped rows, mixed types, temporal; risk: labels at different correction stages, the carrier chain open, a rolling view that can only be rebuilt from the kept download).
