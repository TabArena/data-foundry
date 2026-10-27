---
unique_name: dataset_from_feature_selection_based_dynamic_transfer_ensemble_model_for_customer_churn_prediction
name: Dataset from Feature-selection-based dynamic transfer ensemble model for customer churn prediction
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- Data Requested
- Duplicate
tags:
- '?'
- AI-Filled (Verify)
collections:
- New (BeyondArena)
- TabSTAR
domain: business & marketing
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://link.springer.com/article/10.1007/s10115-013-0722-y
- '# AI note 2026-10-22: OpenML 46444 is credit_risk_china (bank personal credit risk, 27,522 rows, target five_categories), not China-Churn'
- https://www.openml.org/search?type=data&id=46444
source_row: 797
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 1: the paper's first dataset is a duplicate (curator's note) and its second, "China-Churn", is not public; the OpenML link the record found is a different dataset, so the old `No` rests only on dataset (1).
- Source: Xiao, Xiao, Huang, Liu and Wang (2014 online, 2015 print), "Feature-selection-based dynamic transfer ensemble model for customer churn prediction", Knowledge and Information Systems 43, 29-51 (doi:10.1007/s10115-013-0722-y, closed access; abstract: two churn datasets). Dataset (1) is the churn set already in TabArena (curator's note); dataset (2) "China-Churn" was requested on 07/03/2026.
- The OpenML link: OpenML 46444 is `credit_risk_china`, "Multi-classification assessment of bank (china) personal credit risk based on multi-source information fusion" (27,522 rows, 27 features, target `five_categories`, 92.7% majority), uploaded by "AutoML Benchmark" with the citation "Metaverse Financial Transactions Dataset". It is not China-Churn and not churn at all; the `TabSTAR` collection tag likely comes from that link. A credit-risk candidate in its own right (no record found for it), with its own provenance question.
- Use case: a telecom operator's retention campaign (transfer between customer groups); fit direct if China-Churn arrives; regime unknown.
- Siblings and duplicates: the TabArena churn dataset (curator's note); the other churn-paper records are other data. External collections: none for China-Churn.
- Papers and pages: the KAIS paper (full text not read: closed access).
- Metric: not checked (closed access), so the fallback `roc_auc` until read (MET-1, MET-8).
- Risks for /add-dataset: no access to China-Churn; whether it is a cut of a known telecom set (PROV-4).
- Priority: gap -, use case + (retention), source - (closed paper, data not described where we could read), shape - (unknown), risk - (dataset (1) duplicate, wrong link): floor 1. `Duplicate` stays for dataset (1).

Two-part record for a churn-prediction paper: the first linked dataset is explicitly noted as a duplicate of the churn dataset already in TabArena, and the second (a 'China-Churn' / OpenML id 46444 set) was data-requested with uncertainty about whether it is the same or distinct. Given the explicit duplicate flag on the primary dataset, this should be rejected as a duplicate; only if the China-Churn set proves genuinely distinct and original would a separate Yes be warranted. A human must determine whether the OpenML 46444 set is a distinct, non-duplicate source; if so it could be reconsidered.

---

Dataset (1) is a duplicate from the churn dataset in TabArena.

"China-Churn" Data Requested on 07/03/2026 by Lennart

Found the data on OpenML via TabSTAR? Unclear if duplicate or different data?
