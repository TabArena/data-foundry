---
unique_name: sber_mbd_product_propensity
name: 'Multimodal Banking Dataset (MBD): Understanding Client Needs through Event Sequences'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- Anonymized
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
original_source: Other
year: '2024'
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
source_links:
- https://arxiv.org/abs/2409.17587
- https://huggingface.co/datasets/ai-lab/MBD
- https://huggingface.co/datasets/ai-lab/MBD-mini
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: Sber AI Lab's open event logs of about 2.2M corporate clients with monthly purchase flags for four unnamed bank products. A real propensity task, but published for sequence models, with anonymized codes and products; a tabular version would be our own aggregation of 69 GB of events.
- Source: Mollaev, Kostin, Postnova, Karpukhin, Kireev, Gusev, Savchenko, "Multimodal Banking Dataset: Understanding Client Needs through Event Sequences", arXiv 2409.17587 (v1 2024-09-26, v2 2025-06-02, read 2026-10-31); data on Hugging Face `ai-lab/MBD` (CC BY 4.0, 69 GB) and `ai-lab/MBD-mini` (about 10% of the clients). As published: 2,186,230 clients with "947,899,612 financial operations, 1,117,213,760 geo position events, and 5,080,781 dialogues" (768-dimensional embeddings); tables `client_split` (client_id, fold), `trx` (event_time, amount, currency, event_type, event_subtype, source and destination type codes), `geo` (geohash at precision 4-6), `dialog`, and `targets` (client_id, reporting month `mon`, `target_1` to `target_4`, trans_count, diff_trans_date, fold). Each target is "a binary label for each product that indicates whether a customer purchases it in a certain month"; "All ID fields are hashed with a random salt" and "All categorical field values are mapped to enumerated indexes".
- Use case: the bank decides each month which corporate clients to offer which product. The paper names future purchase prediction as a practical task but no actor. Fit approximate (the products are not named). Regime temporal by reporting month with the client as a group (the paper's own protocol is 5 folds by client).
- Siblings and duplicates: `rosbank1` (`Yes`, card churn from aggregated transactions) and `alfa_battle_2_0_task_1` (`No`, files lost) are other banks' event-log tasks; no record of MBD. External collections: the paper's own multimodal benchmark; others not checked.
- Better data: found as a related task next to `alfa_battle_2_0_task_1` and `rosbank1` (the data-scouting run of 2026-10-30/31); no further search.
- Papers and pages: the arXiv paper; the two Hugging Face dataset cards.
- Metric: the paper scores "the mean ROC AUC across four binary product labels over the 12 months of 2022", one deliberate choice (MET-5). With one product shipped, that product's `roc_auc` stands in for the mean over four (MET-11); inputs none.
- Risks for /add-dataset: the tabular task is our featurisation of event sequences, and the paper's hand-crafted aggregates with gradient boosting reach 0.783 against 0.819 for a supervised RNN on the transactions (Table 2), so SEL-12 is a real question. The codes and products are anonymized (`Anonymized`). Which of the four products to ship, or four datasets. The feature window must end at the reporting date. The dialogue embeddings are a text modality to drop. The size calls for MBD-mini or a client sample.
- Priority: gap 0 (business & marketing, binary and temporal are not thin), use case 0 (approximate, no actor named), source + (paper and dataset cards), shape + (millions of clients, 12 reporting months), risk - (sequence modality, anonymized, our own aggregation).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through a related task next to `alfa_battle_2_0_task_1`, `rosbank1`.
- as published: more than 2M corporate clients of a large bank (abstract): 950M transactions, 1B geo events, 5M support-dialogue embeddings over 12 months, and monthly targets per client and reporting month; ...; target: per client and reporting month, four binary flags: does the client take each of four (anonymized) bank products in the month after the reporting date; access: open.
- Why: a real bank-customer behaviour task from event logs, like rosbank1 and the lost Alfa task 1 (the client's next action in the app), with an actor and a decision; open (CC BY 4.0) and documented in a paper
- Adds: a different task in the same domain (product propensity rather than churn or next app action), far more clients, monthly reporting dates that allow a temporal split. Caveats: needs per-client-month aggregation of the logs (as rosbank1 did), one of the four products must be picked as the target, product names hidden, ...
