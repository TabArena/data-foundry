---
unique_name: secom_semiconductor_yield
name: SECOM (semiconductor manufacturing process data, UCI 179)
checked_by:
- AI (UNVERIFIED)
data_foundry_status:
- WIP (Triage)
claimed_by: Lennart
suggestion: TBD -> Yes
priority: 2
decision_markers:
- Anonymized
tags:
- AI-Filled (Verify)
original_source: UCI
year: '2008'
domain: industry & manufacturing
problem_type: Binary Classification
source_links:
- https://doi.org/10.24432/C54305
- https://archive.ics.uci.edu/dataset/179/secom
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: 1,567 production entities of a real semiconductor fab with 591 unnamed process measurements, a pass/fail line-test label (104 fails) and a time stamp per entity, donated to UCI in 2008; a real yield task with a temporal split, but the features are anonymous, the source's own aim is feature selection, and the data is small.
- Source: McCann & Johnston, "SECOM", UCI Machine Learning Repository, donated 2008-11-18 (doi 10.24432/C54305, CC BY 4.0); no paper linked. The page: "A complex modern semi-conductor manufacturing process is normally under consistent surveillance via the monitoring of signals/variables collected from sensors and or process measurement points"; "each example represents a single production entity with associated measured features and the labels represent a simple pass/fail yield for in house line testing, figure 2, and associated date time stamp. Where –1 corresponds to a pass and 1 corresponds to a fail"; "SECOM Dataset: 1567 examples 591 features, 104 fails". As published: two space-separated files, the 1,567 x 591 matrix ("null values varying in intensity depending on the individuals features", NaN) and the labels with their time stamps.
- Use case: the source's: "The Process Engineers may then use these signals to determine key factors contributing to yield excursions downstream in the process", by feature selection "to rank features according to their impact on the overall yield"; the prediction reading: a process engineer flags entities likely to fail in-house line testing from the in-line measurements, to hold, rework or scrap them before the test; fit approximate (the source names the engineer, but its decision is a root-cause search). Regime temporal: production drifts and each label has a time stamp (SPLIT-6); the page suggests cross validation, a claim (SPLIT-5).
- Siblings and duplicates: `synthetic_control` (`No`, `AHDS`), the record this was found next to; `experimental_band_gap_zhuo` (`TBD -> Yes`, materials, another task). Not on OpenML under its name (API lookup, 2026-10-31). External collections: not searched (web search budget used up).
- Better data: found as a related task next to `synthetic_control` (the data-scouting run of 2026-10-30/31); no further search.
- Papers and pages: the UCI page (summary, variable information, baseline table).
- Metric: the page: "Results may be submitted in terms of feature relevance for predictability using error rates as our evaluation metrics"; its baselines use 10-fold cross validation and "the balanced error rate (*BER) generated as our initial performance metric", a hard-label metric with no threshold or costs fixed (MET-6); so the fallback `roc_auc` (MET-8), with BER named as the original in the reason; inputs none.
- Risks for /add-dataset: features are anonymous (`Anonymized`: what each measures and whether it is taken after the line test cannot be checked; LEAK-32); 104 fails, about 20 per test fold of five and fewer per temporal window (TP-5, TP-9); constant and mostly-missing columns (CLEAN-5); the time stamps live in the label file (split columns, never features), their span to check; re-uploads elsewhere may differ (PROV-15).
- Priority: gap 0 (industry & manufacturing and binary not thin), use case 0 (the source's decision is a root-cause search), source + (the donors' documented UCI page), shape + (1,567 entities x 591 measurements, timestamped), risk − (anonymous features, few fails).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through a related task next to `synthetic_control`.
- as published: 1,567 production entities (wafers) x 591 anonymized process sensor and measurement features, with a date-time stamp per entity in the labels file; missing values as NaN; 104 fails; target: pass/fail yield of the entity in in-house line testing (-1 pass, 1 fail); access: open.
- Why: the real side of what synthetic_control only simulates (process monitoring: tell an abnormal production process from a normal one so an engineer acts), here as a tabular per-unit task from a real fab; the timestamps allow a temporal split; CC BY 4.0
- Adds: real manufacturing data instead of six generated chart patterns, tabular rather than one raw series per row; risks: features anonymized (Anonymized), heavy missingness, only 104 fails, small (about 1.6k units), no paper behind it
