---
unique_name: sasol_customer_retention_recruitment_competition
name: sasol-customer-retention-recruitment-competition
checked_by:
- Andrej
suggestion: 'No'
decision_markers:
- Duplicate
tags:
- Review Prio 1 (Atlas)
collections:
- New (BeyondArena)
original_source: Zindi
source_links:
- https://zindi.africa/competitions/sasol-customer-retention-recruitment-competition/data
source_row: 892
type_adapter_id: curation-record-v1
---

## Comments

forecast the probability of each customer becoming inactive and refraining from making any transactions for a period of 90 days (1.5 million clients in train)

Awesome dataset, but restrictive license.

**Assessment (AI, 2026-10-07):** Duplicate of expresso_churn_prediction (shipped as expresso_churn_prediction_1m); suggest No + Duplicate. Zindi reused the Expresso data. VariableDescription.csv is the English column of Expresso's VariableDefinitions.csv with renamed columns (ORANGE, TIGO → Procuct_1, Procuct_2). Train.csv (1,507,834 rows) is a 70.0% sample of Expresso's Train.csv, and Test.csv (380,127 rows) is Expresso's Test.csv: all 17 columns have the same non-missing counts. The ten rows with activity values printed in a public notebook (GitHub Ambiqour/Sasol-Customer-Retention-Prediction) each match exactly one Expresso row on 12 columns. Money is divided by 2.34, and the regions are renamed (Mandalore = DAKAR). No column holds a date, so the Temporal tag has no basis. Zindi's Rules page limits entry to South African citizens and forbids redistribution.

**Assessment (AI, 2026-10-20):** priority 1 for the review of the added dataset: gap -, use case -, source -, shape +, risk - (Open issue 1: duplicate of expresso_churn_prediction; run recommends No + Duplicate). Renamed 70% sample of the Expresso churn data already shipped; adds nothing to the benchmark.

CC (2026-10-22, Lennart): leave out: No + Duplicate of expresso_churn_prediction.

**Assessment (AI, 2026-10-22):** `No` + `Duplicate` (a renamed 70% sample of the Expresso data, regions renamed, money divided by 2.34); the `Non-IID (Temporal)` tag is removed (no date column; the extract is one snapshot). The record keeps its name so links stay valid. A different, still-open Sasol competition (Customer Value Recruitment, 2026) would be a new candidate. Open-issues block removed.
