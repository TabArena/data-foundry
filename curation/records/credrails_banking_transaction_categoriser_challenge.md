---
unique_name: credrails_banking_transaction_categoriser_challenge
name: credrails-banking-transaction-categoriser-challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- NLP (Text)
- TBD
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2022'
domain: finance
required_split:
- Random (IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/credrails-banking-transaction-categoriser-challenge/data
- https://zindi.africa/competitions/credrails-banking-transaction-categoriser-challenge
source_row: 995
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 2: a real categorisation need, but the data is an
unnamed "public data source", the labels are not explained, and the signal is most likely the description text.
- Source: Zindi #ZindiWeekendz hackathon for Credrails (open-banking API), 2-4 September 2022. Data page: "This data is
  from a public data source but is very similar to the data we usually see. It is 80 000 transactions over a 7-year
  period"; columns named include `DATE` and `BALANCE AMT`; 21 target classes (category/subcategory). The column names
  match the anonymous Kaggle upload "Bank Transaction Data" (Indian bank statements; `TRANSACTION DETAILS`, `WITHDRAWAL
  AMT`, `DEPOSIT AMT`, `BALANCE AMT`), which has no categories, so Credrails probably added the labels (unverified: the
  Zindi files need a login).
- Use case: Credrails "categorise any transaction on our platform" for customer analytics: actor the API provider, at
  ingestion of a statement; fit approximate (public statements, not Credrails' own). Regime: temporal by `DATE` (7 years)
  or grouped by account; IID would mix one account's recurring payees across folds.
- Siblings and duplicates: `alvin_smart_money_management_classification_challenge` (purchase categories, `No`, Too Small,
  Lennart 2026-10-12) is a different source; no duplicate found.
- Papers and pages: Zindi competition page (description, data, evaluation read through the Zindi API); no paper.
- Metric: multiclass log loss over 21 classes, Zindi evaluation page ("The evaluation metric for this challenge is Log
  Loss. Note there are 21 classes"); deliberate (leaderboard, MET-4); inputs none.
- Risks for /add-dataset: labels likely assigned by keyword rules on the description (SEL-5, `Trivial`) and the task is
  then text matching (SEL-12, `NLP (Text)`); the upstream source is anonymous (PROV-2); `ID` is built from `DATE` and
  `BALANCE AMT` (drop); balance columns leak the row order within an account.
- Priority: gap 0, use case + (Credrails names the decision), source - (unnamed public source), shape + (80k rows,
  amounts, dates, text), risk - (text-driven, rule-made labels).

Zindi/Credrails challenge to categorise banking transactions for an API. Transaction categorisation is typically driven by free-text transaction descriptions/merchant strings, which makes it primarily an NLP (text-classification) task where text models tend to dominate, rather than a representative numeric/categorical tabular task. It could be partly tabular if amount, channel, and other structured fields carry most of the signal. A human must inspect the feature set to see whether the predictive signal is mostly in text fields versus structured columns, plus the number of target categories and the data size.

---

categorise banking transactions for the Credrails API
