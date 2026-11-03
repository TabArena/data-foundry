---
unique_name: eu_rasff_window
name: RASFF Window
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
- Free Text (Short)
collections:
- STRABLE
original_source: GOV Website
required_split:
- Temporal (NON-IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://ec.europa.eu/food/safety/rasff_en
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/rasff_window
- https://arxiv.org/abs/2605.12292
- '# the public RASFF Window (the first link redirects to https://food.ec.europa.eu/safety/rasff_en)'
- https://webgate.ec.europa.eu/rasff-window/screen/search
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: the risk decision on each EU food and feed safety notification, an expert call made when a notification is assessed. It covers 25,702 notifications from 2020 to 2025 in six classes, and the notification's classification column has to go.
- Source: European Commission, RASFF (Rapid Alert System for Food and Feed), "based on Article 50 of Regulation (EC) No 178/2002"; the public RASFF Window gives "summary information about the most recently transmitted RASFF notifications", searchable back to 2020 only, without "commercial details such as brands and business operators" (https://food.ec.europa.eu/safety/rasff_en). As published in STRABLE (RASFF_window.csv; parquet previewed 2026-10-31): 25,702 rows x 14 columns, one notification per row (3,856 in 2020 rising to 5,364 in 2024, 2,533 in 2025 up to early July, 56 earlier ones); target `risk_decision`: serious 13,987, not serious 3,910, undecided 3,060, potential risk 2,303, potentially serious 2,041, no risk 401; inputs category, type (food, feed, food contact material), subject (short free text, often in two languages), date, notifying country, classification, distribution, forAttention, forFollowUp, operator countries, origin, hazards.
- Use case: when a member state notifies a product and a hazard, its authority and the Commission's RASFF team assess the risk, which sets how the notification is classified and who must follow up; a model would pre-classify incoming notifications for triage. The source names no prediction task. Fit approximate (the experts decide with the full lab results, which the table reduces to `hazards`); regime temporal by notification date.
- Siblings and duplicates: none for RASFF among the records (searched rasff, rapex, safety gate); `fda_food_enforcement_recalls` (FDA recall class I/II/III, STRABLE) is the US analogue, a risk class per food incident; `eu_safety_gate_alerts` is the Commission's non-food system. External collections: STRABLE (Blayer et al. 2026, arXiv 2605.12292, App. C.2), "RASFF Window": "Food and feed safety alerts from the EU Rapid Alert System. The task is to predict the risk level."
- Better data: a candidate of the benchmark STRABLE; no further search this round.
- Papers and pages: the RASFF page and Regulation 178/2002; STRABLE and `preprocess_european-commission_rasff.py`; papers that used the data: not searched (the session's web search budget ran out).
- Metric: none found (the Commission publishes notifications, no task); STRABLE scores R2 for regression and AUROC for classification over all its tables (App. D.1), a benchmark's habit, not the source's. So the fallback, `log_loss` (MET-8); inputs none.
- Risks for /add-dataset: `classification` follows the risk decision (alert notifications: 6,652 of 7,527 serious; information notifications for follow-up: 53 of 4,343 serious), and `forAttention` and `forFollowUp` are set with it: drop them (LEAK-10); the six classes mix risk levels with a state ("undecided", 3,060 rows) and near-synonyms ("potential risk", "potentially serious"): read the RASFF codebook before deciding classes (USE-5); `reference` is an id that orders by time; `subject` is multilingual free text (SEL-12: check that a text model does not dominate); the Window reaches back to 2020 only.
- Priority: gap + (multiclass is thin), use case 0 (not named by the source), source + (a Commission system with a legal basis), shape + (25,702 notifications, mixed, dated), risk - (the classification columns leak and must be dropped).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 25,702 rows x 14 columns incl. target (STRABLE parquet); target: risk_decision.
- Why: Predict the risk decision of an EU food/feed safety notification
- Notes: RASFF Window export (6 risk classes).
