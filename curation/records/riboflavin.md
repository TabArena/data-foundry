---
unique_name: riboflavin
name: OpenML-46983 Riboflavin Production
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
tags:
- AI-Filled (Verify)
- Tiny Data
- Many features
collections:
- TabBench-Bio
original_source: Other
year: '2014'
domain: biology & life sciences
problem_type: Regression
source_links:
- https://www.openml.org/d/46983
- https://arxiv.org/abs/2609.07441
- https://doi.org/10.1146/annurev-statistics-022513-115545
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: log riboflavin production of Bacillus subtilis from 4,088 log gene expressions, 71 samples from DSM; a classic teaching set for high-dimensional inference, tiny, with an undocumented sampling design.
- Source: data "kindly provided by DSM (Switzerland)", published with Bühlmann, Kalisch and Meier (2014), "High-dimensional statistics with a view towards applications in biology", Annual Review of Statistics and Its Application 1:255-278, and the R package hdi (`riboflavin`: "n=71 observations of p=4088 predictors", response "Log-transformed riboflavin production rate (original name: q_RIBFLV)"). OpenML 46983 (uploaded 2025-05-07 by T. Guyard) is a copy. As published: 71 x 4,088, target `x`.
- Use case: a strain engineer at a producer picks genes to modify; the source uses the data for variable selection and p-values (which genes go with production), not to predict the rate of a new culture, which is measured directly. Fit approximate at best (a discovery purpose, a SEL-3 question); regime open: the hdi help page does not say whether the 71 samples are distinct strains or repeated time points of fewer strains.
- Siblings and duplicates: none among the records (grep by name, organism and package). External collections: TabBench-Bio (Table 4: 71 x 4,088, regression).
- Better data: a candidate of the benchmark TabBench-Bio (the run searched no further).
- Papers and pages: Bühlmann et al. 2014 (not read in full); https://rdrr.io/cran/hdi/man/riboflavin.html; https://www.openml.org/d/46983.
- Metric: none found for prediction (the hdi help page and OpenML name none; the source paper is about inference); TabBench-Bio ranks regression by RMSE (Sec. 3.5). Fallback `rmse`.
- Risks for /add-dataset: the sampling design (strains, time points, fermentation runs) decides the split and is undocumented (SPLIT-24, SPLIT-25); 71 rows (TP-5 on the target's spread); the target ships as a log rate, so state the scale the metric means (MET-3); the log expression values may have been normalised over all samples (LEAK-30, check).
- Priority: gap 0 (biology has 4 accepted, not thin), use case 0, source + (a paper documents it), shape 0 (71 rows), risk - (a discovery purpose and an unknown design).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 71 x 4,088; target: x (log production rate).
- Why: Log riboflavin production rate of Bacillus subtilis strains from log gene expression
- Notes: Classic statistics teaching set (R package hdi).
