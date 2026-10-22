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

**Screening (AI, 2026-10-22):** `No` (`Time-series (Forecasting)`, SEL-10): the source asks for a forecast of each corporate client's activity series, the 6-hour windows of the day after seven weeks of raw event logs; no fixed per-row task table is published.
- Source: Zindi, "Absa Corporate Client Activity Forecasting Challenge", 1-27 Nov 2022, Absa CIB (https://zindi.africa/competitions/absa-corporate-client-activity-forecasting-challenge, read through Zindi's page API); as published: Train.csv (58 MB) of events (`eventdatetime`, `event`, `userid`, `dayofweek`, `useremaildomain`, `userrole`, `companyprofileid`, `country`) for "4 200 customers, across five countries over a period of seven weeks"; Test.csv (0.7 MB) lists user x 6-hour slots of one day, e.g. `User2504_Wed_3_6`.
- Deciding words: subtitle "Can you forecast if a corporate banking client will be active in the following week?"; Data tab "The training set is 7 weeks of data, and the last day of the final week will be the test set, where the target is whether a client performed event 14 during that day at 6-hour intervals"; Zindi's problem type "Forecast".
- Use case: Absa CIB anticipating platform usage ("help Absa anticipate their clients' needs, allowing for better planning, delivery and customer service"); the prediction is the next values of each client's event series over a one-day horizon.
- Why not SEL-11: the label is built from the same event series the features come from, one horizon day is shared by all clients, and the older note records that the winning solution was an LSTM; a per-client churn-like reframing would be our task, not the source's (SEL-8).
- Siblings and duplicates: `absa_customer_income_prediction_challenge` is another dataset; none else.
- Metric: F1 on hard labels ("The error metric for this competition is the F1 score", Evaluation tab), MET-4.
- Reject check (AI, 2026-10-22): stands. SEL-10 (Must). Data tab: "The training set is 7 weeks of data, and the last day of the final week will be the test set, where the target is whether a client performed event 14 during that day at 6-hour intervals". Zindi type_of_problem ["Forecast"]. The target event is in the same raw event log as the features. All clients share one horizon day, no row table is published, and the older note says the winner used an LSTM. A TP-10 per-client reframing would be our own task (SEL-8). https://zindi.africa/competitions/absa-corporate-client-activity-forecasting-challenge

Predict whether a corporate client performs a specific action within a 6-hour window across a day, using seven weeks of prior event history. This is a sequential/temporal forecasting task over future windows (the winning solution used an LSTM), which is excluded time-series forecasting rather than a fixed IID tabular task. The temporal tag and the 'forecasting' framing both reinforce this. A human could double-check whether an aggregated per-client tabular reformulation exists, but as posed it should be rejected.

---

Predict if a user performs a specific action (such as making a purchase) in a 6-hour period over the course of a day, based on previous event data for seven weeks.

Winning solution used LSTM - likely time-series
