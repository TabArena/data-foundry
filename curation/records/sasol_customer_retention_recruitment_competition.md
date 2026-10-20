---
unique_name: sasol_customer_retention_recruitment_competition
name: sasol-customer-retention-recruitment-competition
checked_by:
- Andrej
suggestion: 'Yes'
priority: 1
tags:
- Non-IID (Temporal)
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

**Open issues (AI, 2026-10-07):** not added; duplicate. A renamed 70% sample of the Expresso data (regions renamed,
money divided by 2.34).

1. **Verdict.**
   - Question: should this record go to No + Duplicate of expresso_churn_prediction?
   - Evidence: the assessment above.
   - Implemented: nothing added.
   - Proposal: No + Duplicate. By the convention the record becomes `expresso_churn_prediction_duplicate`.
   - Alternative: none worth keeping. The Sasol cut is a subset (70% of the labelled rows) with renamed regions and
     rescaled money, and its files cannot be obtained.

2. **The `Non-IID (Temporal)` tag has no basis.** None of the 19 columns is a date, and the Expresso extract is one
   snapshot of the customer base (expresso_churn_prediction_1m `curation_comments`). This is moot if the record goes
   to No.

5. **FYI, no action: the "simulated" suspicion.**
   - Participants suspected simulated data (skaak in discussion 19432: "I think the data is simulated and probably 0.7
     is the built in max"; in 19601: "I started to (and still do) suspect that the data is simulated and not real").
   - The reuse explains it. The rows are real Expresso rows, and Zindi's test set is a random sample of the same
     extract. The expresso unit found that a model separating the two files scores ROC AUC 0.500.

6. **FYI: a different Sasol competition with a Kaggle copy.**
   - Zindi's "Sasol Customer Value Recruitment Challenge" runs from 23 September to 18 October 2026 and is still open.
     It is scored on "CLV fuel", "CLV non-fuel" and "Opportunity"; its train.csv "is transaction data" (Zindi API).
   - The Kaggle upload `kimp1995/sasol-customer-value-recruitment` (2026-10-02) has the file sizes the Zindi API lists
     for that competition, among them LABEL_RULES.md and label_rules.py.
   - It is not this record's data. It would be a new candidate with its own triage. I did not look at its labels.

**Assessment (AI, 2026-10-20):** priority 1 for the review of the added dataset: gap -, use case -, source -, shape +, risk - (Open issue 1: duplicate of expresso_churn_prediction; run recommends No + Duplicate). Renamed 70% sample of the Expresso churn data already shipped; adds nothing to the benchmark.
