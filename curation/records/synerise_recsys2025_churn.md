---
unique_name: synerise_recsys2025_churn
name: 'RecSys Challenge 2025 (Synerise): churn of active shoppers from six months of event logs'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
original_source: Company
year: '2025'
domain: business & marketing
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://recsys.synerise.com/data-set
- https://doi.org/10.1145/3705328.3748172
- https://github.com/Synerise/recsys2025
- https://basemodel.ai/data-set
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source pages and papers, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: six months of event logs of one online retailer, released by Synerise for the ACM RecSys Challenge 2025, whose disclosed churn task (an active client makes no purchase in the next 14 days) is scored by AUROC; a real retailer and a defined label, but the challenge was a representation-learning contest for recommender systems, and a tabular task would be our own aggregation of the logs.
- Source: Synerise with academic partners, the RecSys Challenge 2025 (Dabrowski, Janicka, Sienkiewicz, Stomfai, Jannach, Barile, Polignano and Pomo, "RecSys Challenge 2025: Universal Behavioral Profiles for Recommender Systems", RecSys '25, 2025-09, doi 10.1145/3705328.3748172, not read); data at recsys.synerise.com/data-set, code at github.com/Synerise/recsys2025. As published (data page and README): event tables `product_buy`, `add_to_cart`, `remove_from_cart` (client_id, timestamp, sku), `page_visit` (client_id, timestamp, url as an integer id) and `search_query` (client_id, timestamp, a 20-dimensional quantized query), and `product_properties` (sku, category id, price bucket, a quantized name embedding); a raw release (1.9 GB) and a challenge release (1.3 GB) with `relevant_clients.npy` (1M clients). The event counts per type in the run's note (1.7M buys, 150.7M page visits) were not re-checked.
- Use case: the retailer's CRM team picks active clients likely to stop buying for a retention action; the challenge page says "Common predictive tasks in such organizations include recommendation, propensity prediction, churn prediction" (recsys.acm.org); fit approximate: "The only task for participants is to submit universal user representations", and the organisers train each downstream model on them (README). Churn is "Binary classification into 1: user will churn or 0: user will not churn", on "a subset of active users with at least one product_buy event in history", the label being whether the client buys in the 14 days after the input (README). Regime temporal: the labels are later windows of the same clients (the training target is the 14 days after the input, the validation target the next 14 days).
- Siblings and duplicates: no record of this source (grep: Synerise, RecSys Challenge). Event-log tasks from other sources: `coveo_sigir_ecom_purchase_intent` (`TBD -> Yes`, 2), `sber_mbd_product_propensity` (`TBD -> 2nd Tier`, 2: published for sequence models, a tabular version our own aggregation, the same call as here), `xuetangx_mooc_dropout` (`TBD -> Yes`, 4), `customer_retention_in_the_media_industry_datathon` (`TBD -> Yes`, 3). The challenge's propensity tasks are SEL-9 and not part of this record. External collections: none found.
- Better data: from the curator's Zotero collection (item 40, the data page); no further search this round.
- Papers and pages: the challenge paper (RecSys '25); participant papers such as arXiv 2508.07748 (second place overall) and 2508.06970 (a fourth place), which learn sequence encoders.
- Metric: "The primary metric used to measure model performance is AUROC" (README), the leaderboard metric of the churn task (MET-4), so `roc_auc`; the overall ranking aggregates all tasks by Borda count, which does not apply to one task; inputs none.
- Risks for /add-dataset: the features are ours to build from the logs (counts, recency, spend buckets over the input window), so the table is a curation choice and far from the data as published (`Needs extensive data wrangling`; P2); a no-purchase label over 14 days counts every active client who simply did not buy that fortnight as a churner, a weak and noisy target (USE-5); the official test targets are hidden, so labels come from the released windows; the licence was not stated on the pages read (the run's note says CC BY-NC 4.0; EV-4, no criterion).
- Priority: gap 0 (business & marketing and binary classification are not thin), use case 0 (the source lists churn among common tasks, with no actor or decision), source + (an ACM challenge with a paper and a documented release), shape + (a million clients, a temporal structure), risk - (our own aggregation, a short label window).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 40: "RecSys Challenge 2025 by Synerise | Data set".
- as published: One retailer over 6 months: 1,682,296 product_buy, 5,235,882 add_to_cart, 1,697,891 remove_from_cart, 150,713,186 page_visit and 9,571,258 search_query events. Product properties are category, price ...; target: churn: an active client makes no purchase in the 14 days after the input cut-off (binary; AUROC in the challenge); access: open.
- Why: Real behaviour logs from a real retailer, with a churn task the organisers define and score. Open download under CC BY-NC 4.0, with an ACM RecSys challenge paper.
- Adds: An e-commerce event-log churn source; our churn records are mostly telco and bank snapshots. Caveats: features must be aggregated from the logs (Needs extensive data wrangling). The challenge is framed as recommendation, so only churn is in scope (propensity tasks are SEL-9). A 14-day no-purchase window is a weak ...
