---
unique_name: scimago_media_ranking
name: Media Ranking
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- No Good Target (yet)
tags:
- AI-Filled (Verify)
collections:
- STRABLE
original_source: Website
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.scimagomedia.com/
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/media-ranking_wide
- https://arxiv.org/abs/2605.12292
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: the target is SCImago's equal-weight composite of four SEO metrics that are not in the table, to be predicted from an outlet's name, domain, country and language; no decision fits, as for its sibling `journal_score_sjr` (Lennart: `TBD -> 2nd Tier`, `No Good Target (yet)`).
- Source: SCImago Media Rankings (SMR), SCImago Lab, "updated three times a year" (spring, summer and winter waves), "4,500+ media outlets evaluated" (https://www.scimagomedia.com/). Methodology (https://www.scimagomedia.com/methodology.php): "Using four metrics—Authority Score, Referring Domains, Citation Flow, and Trust Flow—with an equal weight of 25%, we construct an overall indicator that reflects media websites' digital reputation"; Authority Score and Referring Domains come from Semrush, Citation Flow and Trust Flow from Majestic. First edition year not found. As published by STRABLE (`media-ranking_wide`, raw file "SCImago Media Ranking_2025_Summer.xlsx"): 6,009 rows x 7 columns, target `Overall` (6 to 87.75), features media name (5,647), web domain (unique per row), country (204), region (8), language (300 combinations), typology (general, finance, sports).
- Use case: none; SMR describes outlets for researchers and marketers ("select samples, research competitors, and compare media outlets"), and the score is computed, not observed. Fit none as framed (USE-2); regime IID (one wave, one row per outlet).
- Siblings and duplicates: `journal_score_sjr` (SCImago Journal Rank; CARTE/TARTE, MulTaBench, STRABLE) has the same publisher and the same kind of target: a distinct table, not a duplicate, and its decision is the precedent here. External collections: STRABLE (config `media-ranking_wide`).
- Better data: a candidate of the benchmark STRABLE; no new search in this run.
- Papers and pages: the two SMR pages above; STRABLE, Blayer et al. 2026, "STRABLE: Benchmarking Tabular Machine Learning with Strings", arXiv:2605.12292, App. C item 72, which describes it as "Rankings for media and social science publications", task "predict the impact factor", and links scimagojr.com (the journal ranking), not SMR.
- Metric: none from SCImago (a ranking). STRABLE, the benchmark that framed the task, scores R² for every regression table (arXiv:2605.12292, App. D.1: "R2 for regression; AUROC for classification"; 3 outer folds, rendered "33", on a target it transformed to minimise skew, App. C): one metric for the whole benchmark, not a choice for this task (MET-5), so the fallback `rmse` (MET-8) on the amount as published, with any log shipped as `target_transform` (MET-3); inputs none (MET-1, MET-6).
- Risks for /add-dataset: the target is a deterministic mean of four metrics; if they ever ship as features the task is `Trivial` (SEL-5, TP-4), and without them it is a lookup of an outlet's web reputation from its name and domain, which tests a string encoder's world knowledge more than tabular learning; STRABLE's description names the wrong source (PROV-15).
- Priority: gap 0, use case 0, source + (the method is published), shape 0 (besides two name columns only country, region, language and typology), risk - (a computed index as the target).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 6,009 rows x 7 columns incl. target (STRABLE parquet); target: Overall.
- Why: Predict a media outlet's overall SCImago Media Ranking score
- Notes: Raw file 'SCImago Media Ranking_2025_Summer.xlsx'. Only 7 columns; the overall score is a composite of web indicators, check for components among the features.
