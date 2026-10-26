---
unique_name: credit_card_dataset_for_clustering
name: Credit Card Dataset for Clustering
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target / Scientific Discovery
- Missing source information
tags:
- 2nd Tier / Scientific Discovery
- AI-Filled (Verify)
collections:
- TabSTAR
domain: finance
problem_type: Other
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/arjunbhasin2013/ccdata
- https://www.openml.org/search?type=data&id=43618&sort=runs&status=active
source_row: 840
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`No Good Target / Scientific Discovery`, `Missing source information`; SEL-3, PROV-1): the source publishes a
segmentation case with no predictive target, from an untraced "sample Dataset".
- Source: Kaggle arjunbhasin2013/ccdata ("Credit Card Dataset for Clustering"), CC0; OpenML 43618 is a copy. As
  published: about 9,000 active card holders x 18 behavioural variables over 6 months (`BALANCE`, `PURCHASES`,
  `CASH_ADVANCE`, `CREDIT_LIMIT`, `PAYMENTS`, `PRCFULLPAYMENT`, `TENURE`, ...), one table, no label.
- Use case: "This case requires to develop a customer segmentation to define marketing strategy": clustering, no actor
  deciding on a predicted outcome (SEL-3). A target could be carved out (`PRCFULLPAYMENT`, `CREDIT_LIMIT`), but it
  would be our construction from features of the same window, not the source's task.
- Provenance: the page names no bank, institution or paper ("The sample Dataset summarizes ..."); no upstream found
  (PROV-1). The old note "unclear if real data" stays open.
- Siblings: `customer_segmentation_data` (`No`, AHDS, no target) is the same pattern; external collection TabSTAR.
- Metric: none (no predictive task).
- Reject check (AI, 2026-10-22): stands. SEL-3 (SEL-8, original task): the source's own task is unsupervised, "This case requires to develop a customer segmentation to define marketing strategy" (https://www.kaggle.com/datasets/arjunbhasin2013/ccdata); no label ships. PROV-1 is weaker under the amended PROV-2 (the first upload is a source to point to), but SEL-3 decides alone.

Kaggle 'Credit Card Dataset for Clustering' of credit-card customer behavior features, explicitly published for unsupervised clustering with no supervised predictive target, and the record notes it is 'not a predictive task, unclear if real data'. Lacking a real classification/regression target and with questionable provenance, it does not satisfy the predictive-task and uniqueness/quality criteria. A human could check whether any sensible supervised target could be carved out, but as published it should be rejected.

---

Not a predictive task, unclear if real data
