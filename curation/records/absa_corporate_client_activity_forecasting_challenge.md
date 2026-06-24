---
unique_name: absa_corporate_client_activity_forecasting_challenge
name: absa-corporate-client-activity-forecasting-challenge
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Time-series (Forecasting)
tags:
- Non-IID (Temporal)
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
domain: finance
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
source_links:
- https://zindi.africa/competitions/absa-corporate-client-activity-forecasting-challenge/data
source_row: 895
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

Predict whether a corporate client performs a specific action within a 6-hour window across a day, using seven weeks of prior event history. This is a sequential/temporal forecasting task over future windows (the winning solution used an LSTM), which is excluded time-series forecasting rather than a fixed IID tabular task. The temporal tag and the 'forecasting' framing both reinforce this. A human could double-check whether an aggregated per-client tabular reformulation exists, but as posed it should be rejected.

---

Predict if a user performs a specific action (such as making a purchase) in a 6-hour period over the course of a day, based on previous event data for seven weeks.

Winning solution used LSTM - likely time-series
