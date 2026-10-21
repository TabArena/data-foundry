---
unique_name: digicow_farmer_training_adoption_challenge
name: DigiCow Farmer Training Adoption Challenge
checked_by:
- Andrej
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 1
decision_markers:
- Needs extensive data wrangling
tags:
- Non-IID (Temporal)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2026'
domain: environmental science & climate
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://zindi.africa/competitions/digicow-farmer-training-adoption-challenge/data
v2_path: datasets/_dev/tabarena-v0pt2/digicow_farmer_training_adoption_challenge/dataset.py
source_row: 731
type_adapter_id: curation-record-v1
---

## Comments

"You are allowed to access and, use and share challenge data for the competition. for any commercial, non-commercial, research or education purposes, by open source."

Domain: agriculture

Discussion on possibly leaking features:
https://zindi.africa/competitions/digicow-farmer-training-adoption-challenge/discussions/30808

three classification tasks for 7, 90, and 120-day adoption windows. Competition used weighted average of logloss (25%) and ROC-AUC (75%)

**Correction (AI, 2026-10-20):** the weights in the line above are reversed: Zindi's evaluation page gives log loss 75% and ROC AUC 25% (rubric: 7-day log loss 0.65, 7-day ROC AUC 0.15, the 90- and 120-day log loss and ROC AUC 0.05 each).

**Assessment (AI, 2026-10-07):** Recommend `No` with `Too Small` and `Data Quality Issue`. The label shows adoption only where and when DigiCow recorded it. Of the 120-day adopters, 1 of the 1,021 trained in Aug-Oct 2024 adopted within 7 days, against 45%, 64% and 95% for Nov 2024, Dec 2024 and Feb 2025. One date, 2024-12-12, lies inside the adoption window of 1,028 of 2,389 adopters. TRA_gertumxc's farmers adopted at 5-13% in late 2024 and never in 2025. The temporal windows hold 9, 5, 19 and 103 adopters, from 1, 1, 2 and 7 trainers. The stored dates have day and month swapped. The challenge scored log loss 75% and ROC AUC 25% (reversed above).

**Assessment (AI, 2026-10-19):** No other split design fixes the small test windows (run of 2026-10-07): a random split gives LightGBM ROC AUC 0.959 against 0.937 for a trainer x month lookup; folds grouped by `group_name` 0.937 against 0.916; leaving one trainer out leaves one trainer with adopters per fold; a rebuild from Prior.csv shows the same recording waves (163 + 41 adopters in 2025, from TRA_rkvyofbh and TRA_kkzpfdtu).

**Assessment (AI, 2026-10-20):** priority 1 for the review of the added dataset: gap -, use case -, source -, shape +, risk - (Issue 1: run recommends No (Too Small, Data Quality Issue)). Labels record follow-up waves rather than adoption, and test windows hold 5-103 adopters from 1-7 trainers; little value for the benchmark.

**Assessment (AI, 2026-10-20):** after the review panel's re-check, recommend `No` (never shipped) with `Data Quality Issue` and `Too Small`; the curator has the call. LEAK-25: the label records when trainers followed farmers up (of the 120-day adopters in Train.csv, 1 of 95 trained in Aug-Oct 2024 adopted within 7 days, against 69 of 77 in Dec 2024; TRA_gertumxc has 0 adopters in 4,906 Train.csv and Prior.csv rows of Mar-Jul 2025). TP-9: the test windows hold 9, 5, 19 and 103 adopters, and the 50% train floor leaves no wider window. Revisit if DigiCow documents who was followed up and when. Priority 1: gap -, use case -, source -, shape -, risk - (no thin domain, problem type or regime; the fit is approximate; the codebook is thin and contradicts the data on the label's anchor; 13,536 rows but 9 and 5 adopters in the newest windows; recommended not to ship).

CC (2026-10-21, Lennart): the declared metric documents the original use case's metric; overrule it only when it is biased or wrong (evidence from the paper); keep the note of the original metric (TP-6 amended).

**Assessment (AI, 2026-10-21):** metric set to `log_loss` (was ROC AUC): Zindi's rubric (log loss 0.75, ROC AUC 0.25 over the 7-, 90- and 120-day targets) is no listed metric and scores targets the task does not ship; log loss carries 0.65 of the 7-day target's 0.80. Moot while the dataset is recommended No.
