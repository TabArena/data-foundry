---
unique_name: stock_pledge_default_china
name: Stock pledge financing default of controlling shareholders (Chinese listed firms, 2017-2022)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- Class-dependent Recording
tags:
- AI-Filled (Verify)
original_source: Kaggle
year: '2025'
domain: finance
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/jiaoyouzhang/stock-pledge-defaults-prediction
- https://www.kaggle.com/competitions/stock-pledge-financing-default-prediction-2026
- https://www.kaggle.com/competitions/stock-pledge-financing-default-prediction
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source pages, papers and a preview of the files, NOT from a full inspection of the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: a Kaggle upload (2025) of 1,442 labelled Chinese listed firms with 60 financial, governance and market features and a pledge-default flag, sourced from the commercial iFinD database with no paper; a preview shows that the two classes were written differently: a trailing space in any feature cell marks all 266 defaults and none of the 1,176 non-defaults.
- Source: Kaggle dataset `jiaoyouzhang/stock-pledge-defaults-prediction` (files created 2025-02-22, DbCL 1.0, "userSpecifiedSources": "iFinD"): "This data set contains information on the default status of pledge financing of controlling shareholders of Chinese listed companies from 2017 to 2022. The column IsDefault has two statuses: 1 represents default status, 0 represents normal status." Files: `train.csv` (1,442 rows x 62 columns: a masked `Stock code` (X00001, X00002, ...), one row per code, 60 features such as Z-score, pledge ratios, volatility, P/E, ROA, liquidity and leverage ratios, audit opinion, ownership, analyst coverage and the macro `Financial cycle m2/gdp`, and `IsDefault`) and `test.csv` (184 rows, no label). The uploader opened a Kaggle community competition the same day (`stock-pledge-financing-default-prediction`, F1, 24 teams); a second one, `stock-pledge-financing-default-prediction-2026` (2026-02-07 to 03-02, 140 USD, 127 teams), scores ROC AUC. How defaults were identified (the run's note says judicial freeze events), how the firms were sampled and when the features were measured are not documented (PROV-2).
- Use case: a securities firm or bank lending against listed shares assesses whether the controlling shareholder will default on the pledge financing ("How to effectively manage the risks of equity pledge financing has become an important issue that urgently needs to be addressed", dataset page); fit approximate: the page names the problem, not an actor or a decision, and the feature dates relative to the default are unknown. Regime: temporal over 2017-2022 would mirror the use, but no year column ships; the macro column is a period proxy (SPLIT-7).
- Siblings and duplicates: no record of this source or of pledge defaults (grep: pledge, iFinD). The two competitions serve the same data and stay as links of this record. External collections: none found.
- Better data: from the curator's Zotero collection (item 113, the 2026 competition); no further search this round.
- Papers and pages: the Kaggle dataset and the two competition pages (overview pages not readable here; metadata through the Kaggle API); no paper found.
- Metric: the 2026 competition, the larger and later one, scores `Roc Auc Score` (Kaggle API `evaluationMetric`); the 2025 competition scored F1; MET-4 gives `roc_auc` (the run's note that the 2026 test set was resampled to 50% defaults does not change a rank metric); inputs none.
- Risks for /add-dataset: class-dependent recording, measured on the `train.csv` preview (2026-10-31): in 37 of 60 feature columns the defaults are written with fewer decimals (2 or 4) than the non-defaults (6 to 9), in 6 with more, and in 31 every default cell ends in a space ("0.00 " for a binary flag; `IsDefault` itself is "1 "); `Financial cycle m2/gdp` takes exactly 147 non-defaults for each of 8 values at 9 decimals, while the defaults carry the same values rounded to 2: the classes were assembled from separate files. Strip and harmonise to the coarsest precision, then test whether the format still separates the classes and whether the values were processed differently per class (the run's note says the uploader imputed and winsorized; LEAK-13, LEAK-39, and LEAK-15 if it cannot be undone). The non-defaults look sampled per period, which changes only the class shares (no `Selection Bias`). Feature timing against the default is unknown (USE-3).
- Priority: gap 0 (finance and binary classification are not thin), use case 0 (no actor named), source 0 (a Kaggle upload naming a commercial database, no paper or codebook), shape + (1,442 firms, 60 numeric features with flags), risk - (class-dependent recording, undocumented sampling and timing).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 113: "Stock Pledge Financing Default Prediction 2026 | Kaggle".
- as published: one row per listed company (controlling shareholder with a pledge): 1,442 labelled train rows (266 defaults, 18.4%) + 184 test rows (dataset) or 376 hidden-label test rows (2026 competition, about ...; target: IsDefault: the controlling shareholder defaults on the equity pledge financing (judicial freeze events); access: open.
- Why: real credit-risk task on Chinese listed firms with financial, governance and market features; in scope as credit default
- Adds: an equity-pledge default task, a credit setting not in the records. Risks (PROV-1, PROV-2): no paper; the sample construction from iFinD and the timing of the features relative to the default are undocumented; the uploader imputed and winsorized the data, and the 2026 test set was resampled to 50% defaults; small ...
