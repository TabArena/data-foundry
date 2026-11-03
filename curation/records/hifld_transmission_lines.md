---
unique_name: hifld_transmission_lines
name: Transmission Lines
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 3
decision_markers:
- No Good Target (yet)
tags:
- AI-Filled (Verify)
collections:
- STRABLE
original_source: GOV Website
required_split:
- Random (IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://hifld-geoplatform.opendata.arcgis.com/datasets/geoplatform::electric-power-transmission-lines/
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/transmission-lines
- https://arxiv.org/abs/2605.12292
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 3: a national map of power transmission lines where STRABLE predicts the voltage class from owner, type, status, dates and length; filling unknown voltages is a real mapping need (the layer infers voltages itself), but two thirds of the labels in STRABLE's cut carry `INFERRED = Y`, so the target is partly the layer's own estimate.
- Source: HIFLD Open layer "Electric Power Transmission Lines" (fields `VOLTAGE`, `VOLT_CLASS`, `INFERRED`, `OWNER`, `SUB_1`, `SUB_2`, source and validation dates; an Esri Living Atlas copy, "U.S. Electric Power Transmission Lines (Archive)", last data update 09/30/2024: "Lines are operated at relatively high voltages varying from 69 kV up to 765 kV"). HIFLD Open went offline in August-September 2025 (archived in DataLumos). As used by STRABLE (HF parquet, previewed): 75,000 rows x 11 columns, a stratified subsample; target `VOLT_CLASS` in three classes (100-161 53%, under 100 34%, 220 and above 13%); `VOLTAGE` and the substation names dropped; `INFERRED` is Y for 50,004 of the 75,000 rows.
- Use case: a grid-mapping agency assigns a voltage class to lines no source gives a voltage for; the source names no such decision (the curation's reading, USE-1). Fit approximate (the labels of inferred lines are HIFLD's estimates); regime IID (one snapshot), owners repeat.
- Siblings and duplicates: no duplicate (grep for transmission, HIFLD, the layer link); `hifld_transmission_towers` (FCC radio sites, not power lines), `hifld_electric_generating_plants`, `hifld_power_plants`, `hifld_electric_retail_service_territories`. External collections: STRABLE (Table C.4 row 101: "Electric power transmission infrastructure in the US. The task is to predict voltage levels.").
- Better data: a candidate of the benchmark STRABLE; no further search for this run's finds.
- Papers and pages: STRABLE, Blayer et al., arXiv 2605.12292 (v2, 2026-10-19), Sec. 3; the archived layer copy above.
- Metric: none found (HIFLD defines no task; STRABLE's AUROC, App. D.1, is benchmark-wide, MET-5), so the fallback `log_loss` (multiclass); inputs none.
- Risks for /add-dataset: label quality (train and test on `INFERRED = N` rows, or say why not; USE-5); what `INFERRED` means is read from its name, to confirm in the archived layer metadata; the substation names `SUB_1`/`SUB_2` would help a mapper and were dropped by STRABLE (restore them from the source, USE-6); the source is offline (PROV-13).
- Priority: gap + (multiclass is thin), use case 0 (the curation's reading), source + (HIFLD layer metadata), shape + (75,000 lines, mixed columns), risk - (inferred labels).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 75,000 rows x 11 columns incl. target (STRABLE parquet); capped at 75,000 by STRABLE; target: VOLT_CLASS.
- Why: Predict the voltage class of an electric power transmission line
- Notes: HIFLD layer. Subsampled by STRABLE to 75,000 rows (stratified).
