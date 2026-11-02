---
unique_name: telangana_crop_health_challenge
name: telangana-crop-health-challenge
checked_by:
- Andrej
- AI (UNVERIFIED)
data_foundry_status:
- WIP (Triage)
suggestion: TBD -> Yes
priority: 3
decision_markers:
- TBD
tags:
- Non-IID (Grouped)
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
domain: environmental science & climate
required_split:
- Grouped (NON-IID)
problem_type: Multiclass Classification
source_links:
- https://zindi.africa/competitions/telangana-crop-health-challenge/data
source_row: 880
needs_review:
- ai_unverified
- wip_unclaimed
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Assessment (AI, 2026-10-22):** recommend keeping `TBD -> Yes` with priority 3; the inputs are a real cultivation-practice table, with Sentinel-2 imagery as an optional extra that the benchmark version should leave out. The curator has the call.
- Source: Zindi competition by GIZ (FAIR Forward), the Government of Telangana and ADeX, 8 Nov 2024 to 10 Feb 2025 (https://zindi.africa/competitions/telangana-crop-health-challenge, read through Zindi's page API); data_type "Structured, Satellite"; as published: Train.csv, Test.csv, VariableDefinitions.docx; "The tabular data includes information on cultivation practices such as crop type, sowing and irrigation methods, past yield, and crop coverage (boundaries)", with a notebook to pull Sentinel-2 time series "from sowing ... to harvest"; data also on the ADeX platform, CC-BY-SA 4.0.
- Use case: "This model will help both farmers and government bodies monitor crop conditions and take proactive measures" (Description); fit approximate (the label is the field's condition over the season, and the season's imagery runs to harvest). Regime: grouped by district (the fairness metric is computed "based on crop district"), as the record has.
- Siblings and duplicates: none found in `curation/records/` (other GIZ/ADeX Telangana challenges, if any, have no record).
- Metric: multiclass F1 ("The error metric for this competition is F1 Multi Class", Evaluation tab; the averaging is not stated), plus a fairness score by district for the final rank; inputs: the district column for the fairness part (MET-1, MET-5).
- Risks for /add-dataset: keep only columns known before the season's outcome; Sentinel-2 features would be image-derived (SEL-13); the crop-coverage boundaries are geometry; the four classes are probably imbalanced (Healthy majority); check the F1 averaging.
- Priority: gap + (Grouped regime thin), use case + (named by the source), source 0 (a competition page; ADeX not read), shape + (field-level table with mixed types and districts), risk - (imagery may carry the signal).

A Zindi 'Telangana Crop Health Challenge' to predict crop health, already flagged Non-IID (Grouped) and marked WIP by curator Andrej (data_foundry_status WIP (Triage)). Crop-health challenges can be either tabular (field/sensor/weather features) or remote-sensing image based, so the modality is the key open question. Given it is actively being worked on and has a clear classification target with a grouped split, it is a plausible Yes. A human must verify the input modality is genuinely tabular (not satellite imagery) and confirm the target and group/split structure.

---

predict crop health
