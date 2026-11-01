---
unique_name: eu_safety_gate_alerts
name: RASNF Notification List
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- No Good Target (yet)
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
- Free Text (Sentences)
collections:
- STRABLE
original_source: GOV Website
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://ec.europa.eu/safety-gate-alerts/screen/search
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/rasnf_notification_list
- https://arxiv.org/abs/2605.12292
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: EU alerts on dangerous non-food products, 2005-2025. STRABLE's target counts the other countries where the product was later found; that count grows after the alert, is read at the download date, and was not recorded before 2009.
- Source: European Commission, Safety Gate (formerly RAPEX), "the EU rapid alert system for dangerous non-food products" (https://ec.europa.eu/safety-gate-alerts/screen/search; the pages are a web app and nothing more could be read). As published in STRABLE (RASNF_window.csv; parquet previewed 2026-10-31): 42,186 rows x 26 columns, one alert per row, alert numbers from 2005 to 2025 (705 in 2005, 4,106 in 2024); STRABLE built the target from the column "Products were found and measures were taken also in" (one plus the countries listed), then binarised it: One country 31,291, More than one country 10,895 (its script's docstring still says "predict of Number of countries effected (regression)"). Inputs: alert type (serious risk or other), consumer or professional, submitting country, country of origin, counterfeit, risk type, legal provision and risk text, product, name, description, brand, category, model, OECD category, compulsory and voluntary measures, recall page, barcode, batch, production dates, packaging.
- Use case: when a member state notifies a dangerous product, the other authorities decide whether to look for it on their markets; predicting at the alert whether it will be found elsewhere is a stand-in, and the count also measures how hard they looked. Fit approximate; regime temporal by alert date.
- Measured on the preview: the multi-country share is 0 for 2005-2008 (the field was not filled), between 0.22 and 0.40 for 2009-2021, then 0.32, 0.27, 0.21 and 0.16 for 2022-2025: the count grows with the time since the alert, a window shared by all rows (SEL-6).
- Siblings and duplicates: `eu_rasff_window` (the Commission's food and feed system); `fda_food_enforcement_recalls` and `fda_drug_enforcement_recalls` (US recall classes, STRABLE). External collections: STRABLE (Blayer et al. 2026, arXiv 2605.12292, App. C.2), "RASNF Notification List": "The EU rapid alert system for dangerous non-food products. The task is to predict whether the product affects more than one country."
- Better data: a candidate of the benchmark STRABLE; no further search this round.
- Papers and pages: STRABLE and `preprocess_european-commission_rasnf.py`; the Safety Gate pages (unreadable app); papers that used the data: not searched (the session's web search budget ran out).
- Metric: none found (the Commission publishes alerts, no task); STRABLE scores R2 for regression and AUROC for classification over all its tables (App. D.1), a benchmark's habit, not the source's. So the fallback, `roc_auc` (MET-8); inputs none.
- Risks for /add-dataset: the label (SEL-6) needs a fixed horizon after each alert, which needs the date of each follow-up (not in the file, as far as the preview shows) or a cut to alerts old enough for follow-ups to have settled, without 2005-2008; the measures and the company recall page may be added after the alert (LEAK-10); most inputs are free text (description, risk, measures) (SEL-12); `Alert number`, `URL of Case`, barcode and batch are ids.
- Priority: gap 0 (binary not thin), use case 0, source + (a Commission system), shape + (42,186 alerts over 20 years, mixed), risk - (a label over a shared window, recorded only from 2009).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 42,186 rows x 26 columns incl. target (STRABLE parquet); target: num_countries_affected.
- Why: Predict whether a dangerous non-food product alert concerns more than one country
- Notes: EU Safety Gate (formerly RAPEX) alerts. Binary target derived from the number of countries affected (the script docstring calls it regression).
