---
unique_name: riboflavin
name: OpenML-46983 Riboflavin Production
checked_by:
- AI (UNVERIFIED)
data_foundry_status:
- WIP (Triage)
claimed_by: Andrej
suggestion: TBD -> 2nd Tier
priority: 1
tags:
- AI-Filled (Verify)
- Tiny Data
- Many features
- 'Samples: No Time Dimension'
- 'Entities: Recur'
- Experimental Results
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

**Screening (AI, 2026-11-25):** `TBD -> 2nd Tier`, priority 1: log riboflavin production of Bacillus subtilis from 4,088 log gene expressions, 71 samples from DSM; a teaching set for high-dimensional inference whose samples are repeated hybridisations of fewer strains, with no strain id shipped.
- Source: data "kindly provided by DSM (Switzerland)", published with Bühlmann, Kalisch and Meier, "High-dimensional statistics with a view towards applications in biology", Annu Rev Stat Appl 1:255-278, 2014 (https://doi.org/10.1146/annurev-statistics-022513-115545, read on stat.ethz.ch/Manuscripts/buhlmann/paper-AnnRev.pdf), and the R package hdi (`riboflavin`: "n=71 observations of p=4088 predictors", response "Log-transformed riboflavin production rate (original name: q_RIBFLV)"). OpenML 46983 (uploaded 2025-05-07) is a copy. As published: 71 x 4,088, target `y`.
- The design, Section 1 of the paper: "n = 71 samples that were hybridized repeatedly during a fed-batch fermentation process where different engineered strains and strains grown under different fermentation conditions were analyzed"; the expressions "were normalized using the default in the R-package affy". A second set, `riboflavinGrouped`, holds "N = 28 groups each having 2 to 6 observations at different times ... from the same strain", n = 111.
- Use case: a strain engineer at a producer screens engineered strains for production; the source uses the data for variable selection and p-values, not to predict a new culture's rate, which is measured directly (a SEL-3 question); fit approximate at best. Collection: designed fermentation runs, no calendar time (`Samples: No Time Dimension`); several samples of one strain (`Entities: Recur`), the strain not identified in the 71-row set; the production rate is measured with the run. Type Experimental Results.
- Split: leaf L-EXP.item (Grouped · `Timeless` (the item)) because [EXP.meets] is a new strain and [EXP.repeated] is yes (repeated hybridisations of one strain); open: the 71-row set ships no strain key, so the unit check cannot group, and repeats that matter but cannot be identified retire the dataset for a reviewer (SPLIT-25), unless `riboflavinGrouped` supplies the key.
- Siblings and duplicates: none among the records (grep by name, organism and package). External collections: TabBench-Bio (Table 4: 71 x 4,088, regression).
- Better data: `riboflavinGrouped` of the same source (111 samples, 28 strains, the strain and time recorded), a version (PROV-6) that carries the group key; the paper says "we make it available (see Supplemental Materials)", not located on the web in this run; no record.
- Papers and pages: Bühlmann et al. 2014 (above); https://rdrr.io/cran/hdi/man/riboflavin.html; https://www.openml.org/d/46983.
- Metric: none found for prediction (hdi and OpenML name none; the paper is about inference), so the fallback `rmse` on the log rate (MET-8, MET-3).
- Risks for /add-dataset: the unidentified strain repeats (SPLIT-24, SPLIT-25); affy's default (RMA) normalises over all arrays (LEAK-30, weak); 71 rows (TP-5); `Outdated` array data (SEL-18, a note).
- Priority: gap 0 (biology not thin, regression not thin), use case 0, source + (a paper documents it), shape 0 (71 rows), risk - (no strain key; a grouped version found).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 71 x 4,088; target: x (log production rate).
- Why: Log riboflavin production rate of Bacillus subtilis strains from log gene expression
- Notes: Classic statistics teaching set (R package hdi).
