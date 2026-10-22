---
unique_name: traffic_violations
name: Traffic_violations
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- No Good Target  / Scientific Discovery
tags:
- 2nd Tier / Scientfic Discovery
- Non-IID (Temporal)
- AI-Filled (Verify)
collections:
- TabArena Reject
- TabSTAR
year: '2015'
domain: social science
required_split:
- Temporal (NON-IID)
problem_type: TBD
original_data_state: One Table
source_links:
- https://www.openml.org/d/42345
- https://catalog.data.gov/dataset/traffic-violations
- https://www.kaggle.com/datasets/nikhil1e9/traffic-violations
source_row: 846
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 2: a real county traffic-stop log, but the OpenML target (citation, warning or repair order) is the officer's own disposition, which no actor predicts, and the charge columns largely set it.
- Source: Montgomery County, Maryland, "all electronic traffic violations issued in the County" (open data portal, mirrored on data.gov; the CC line counts about 1.5M rows first, 2M now). OpenML 42345 (`Traffic_violations` v5, uploaded 2020-04-03, CC0): "downsampled to 5% of the original size", "some features were removed", 70,340 rows x 21 columns, target `Violation.Type` with 3 classes (34,382 in the largest, 3,506 in the smallest; "SERO and ESERO were collapsed"); columns `Description`, `Charge`, `Belts`, `Personal.Injury`, `Property.Damage`, `Commercial.License`, `Commercial.Vehicle`, `State`, `VehicleType`, `Year`, `Make`, `Model`, `Color`, `Contributed.To.Accident`, `Race`, `Gender`, `Driver.City`, `Driver.State`, `DL.State`, `Arrest.Type`. The Kaggle link is a later re-upload.
- Use case: none stated; the OpenML version was cut as a high-cardinality categorical benchmark. Who would predict, at a stop, whether the officer writes a citation or a warning? The officer decides it; a model of it describes enforcement practice (a look back, SEL-3, USE-2). A curated alternative (predict `Contributed.To.Accident` or `Personal.Injury`) would be ours. Fit approximate at best. Regime: the stops are dated in the county data (the OpenML cut dropped the date), so temporal if the date is restored.
- Siblings and duplicates: none among `curation/records/` (grep traffic violation, Montgomery; `employee_salaries` is another Montgomery County table). External collections: TabSTAR; tagged `TabArena Reject`.
- Papers and pages: OpenML 42345; the county open-data page; no paper that defines a task found.
- Metric: none found (OpenML description, data.gov entry), so the fallback.
- Risks for /add-dataset: `Charge` and `Description` (the statute and its text) likely determine the repair-order class and much of the rest (SEL-5, TP-4); `Race` and `Gender` as inputs to a model of police enforcement need a look under SEL-1 (no objection by the source found); the 5% OpenML cut versus the full county data (PROV-6, PROV-13, use the origin); free-text `Description` (SEL-12).
- Priority: gap 0 (`domain` says social science, which is thin, but a police record fits it only loosely; not counted), use case 0, source + (a county's open data with a column guide), shape + (70k-2M rows, mixed categorical), risk - (no decision for the target; charge columns may fix it).

Maryland traffic-violations log (~1.5-2M rows) with spatial and temporal fields, available on OpenML/data.gov/Kaggle. The data is large and genuinely tabular, but the CC comment flags that it may simply have been crawled because it is available and may not correspond to a meaningful predictive task; columns like violation type, race, gender, or fine could each be a target. It carries TabArena Reject and 2nd Tier/Scientific Discovery tags. A human must define a non-arbitrary target, confirm a sensible temporal split, and check for leakage and ethical concerns (race/demographic fields), so a provisional 2nd-tier hold is appropriate.

---

CC: "Large scale, spatial, and temporal. Need to think about split. Also unsure whether this data was simply crawled because it's available but does not correspond to a meaningful task. Not much information is given on OpenML. 1.5M samples originally; now has 2M"
