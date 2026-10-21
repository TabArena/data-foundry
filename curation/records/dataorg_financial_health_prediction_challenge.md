---
unique_name: dataorg_financial_health_prediction_challenge
name: dataorg-financial-health-prediction-challenge
checked_by:
- Andrej
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 3
tags:
- New IID
collections:
- New (BeyondArena)
original_source: Zindi
year: '2025'
domain: business & marketing
required_split:
- Random (IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/dataorg-financial-health-prediction-challenge/data
v2_path: datasets/_dev/tabarena-v0pt2/dataorg_financial_health_prediction_challenge/dataset.py
source_row: 680
type_adapter_id: curation-record-v1
---

## Comments

Evaluation: F1

**Assessment (AI, 2026-10-07):** The rows are FinMark Trust's FinScope MSME surveys: Eswatini 2023, Lesotho 2023, Zimbabwe 2022 (exact interview counts) and Malawi 2019 (2,985 of n = 2,993). The licence is CC-BY SA 4.0 (Zindi rules). Lesotho's label runs against the index. There, loan accounts, debit cards, internet banking, motor insurance, tax compliance and higher income all go with a lower class (income Spearman −0.12; +0.14 to +0.24 elsewhere). Models trained on other countries rank Lesotho at AUC 0.46, against 0.63-0.68 among themselves. The definition drops Lesotho (7,674 rows left). The FHI is a rule on the product columns plus a residual: a depth-6 tree gets log loss 0.285 against LightGBM's 0.260, worse on 9 of 9 splits.

**Assessment (AI, 2026-10-20):** priority 3 for the review of the added dataset: gap + (problem_type multiclass_classification), use case -, source +, shape +, risk - (Issues 1-2: label is an unpublished FHI formula over feature columns, kept; Lesotho labels inverted). One of few multiclass survey tasks (African small-business finance), but the task largely recovers an unpublished index formula from product columns.

**Assessment (AI, 2026-10-20):** review panel (full): ship after changes; the 11 product answers dropped as inputs of the index's access-to-finance dimension (LEAK-10; the rest scores log loss 0.694 against 0.796 for the class shares), the use case moved to a development partner or government screening businesses for support (fit approximate), the Lesotho decision completed (sentinel caveat, damaged answers), 6 impossible business ages made missing, notes on not-ticked answers, the amounts' periods and the cross-country score. Priority 3: gap + (multiclass), use case - (the index was introduced by the challenge; no source shows anyone acting on its class), source + (Zindi page and codebook, FinScope interview counts), shape +, risk - (unclear target, issue 5; Lesotho origin not asked).

CC (2026-10-21, Lennart): the declared metric documents the original use case's metric; overrule it only when it is biased or wrong (evidence from the paper); keep the note of the original metric (TP-6 amended).

**Assessment (AI, 2026-10-21):** metric set to `f1_weighted` (was the default log loss). Zindi's evaluation page says "F1 score" (API `f1_multiclass`) without the averaging; participants who submitted single-class files found the leaderboard fits weighted F1 (Zindi discussion 29971, not confirmed by the host), and a 47th-place entry's cross-validated weighted F1 of 0.878 sits closer to its private score of 0.884 than its macro F1 of 0.819 (discussion 31245). The notes name the source of the averaging. Needs a rebuild to reach the container.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source f1_weighted — Zindi's F1 (API f1_multiclass); weighted per the participants' probe in Zindi discussion 29971.
