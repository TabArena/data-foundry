---
unique_name: silicon_valley_21st_century_education_hackathon
name: silicon-valley-21st-century-education-hackathon
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- Missing source information
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2021'
domain: education
required_split:
- '?'
problem_type: Regression
source_links:
- https://zindi.africa/competitions/silicon-valley-21st-century-education-hackathon/data
- https://zindi.africa/competitions/silicon-valley-21st-century-education-hackathon
source_row: 1001
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 2: a 2-day Zindi hackathon to predict 2010 literacy rates from "historical survey data"; the upstream survey, the unit of a row and the columns are not named, so the target and the regime are unclear.
- Source: Zindi hackathon "Silicon Valley 21st Century Education and Silicon Valley Propellers Hackathon" (subtitle "Semaine Africaine de l'Intelligence Artificielle"), 30 June to 2 July 2021, $700, 87 participants, page in French (https://zindi.africa/competitions/silicon-valley-21st-century-education-hackathon, read through the Zindi API). As published: "Le jeu de données d'entraînement contient ~14 000 réponses et celui de test contient ~1000 réponses à un sondage"; target column `target` (example values 68.92, 41.67, 98.12, a percentage); Train.csv 1.96 MB, Test.csv 145 kB, VariablesDefinition.txt 879 bytes (not read: download needs a login).
- Use case: the page states only the goal: "prédire le taux d'alphabétisation des populations en Afrique et dans le monde pour l'année 2010 à partir de données historiques de sondages". No actor or decision is named; a literacy rate per population is an aggregate, so a row is probably a population-year or area, not a respondent (unverified). Fit unknown. Regime unknown: "2010 from historical data" suggests temporal, a repeated area suggests grouped.
- Siblings and duplicates: no other record on literacy (grep over `curation/records/`). The upstream data (UNESCO UIS, DHS or a census series) is not named on the page; no external collection found.
- Papers and pages: none found (one web search on the title and the French goal).
- Metric: MAE (Évaluation page: "La métrique d'évaluation pour ce challenge est l'Erreur Absolue Moyenne"), a leaderboard metric (MET-4); inputs none (MET-1).
- Risks for /add-dataset: PROV-1/PROV-2: name the upstream survey before anything else (the existing `Missing source information` marker stays as that concern); the unit of a row and whether 2010 rows of the same area appear in train (a temporal or grouped leak); whether it is forecasting of a country series (SEL-10). Zindi rules forbid redistribution (no criterion, EV-4).
- Priority: gap + (education is thin), use case - (none named), source - (upstream unnamed, no codebook read), shape + (~14,000 rows), risk - (unclear unit and target, possible forecasting).


This Zindi education hackathon record has no comments, target description, or metadata beyond the competition link, so the task type, target, modality, and size are unknown. There is too little information to decide and education hackathons can be survey/non-predictive or NLP-heavy. A human must open the competition page to verify whether it is a genuine tabular predictive classification/regression task with a clear target and adequate size.
