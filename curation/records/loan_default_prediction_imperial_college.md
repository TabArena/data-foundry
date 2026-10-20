---
unique_name: loan_default_prediction_imperial_college
name: Loan Default Prediction - Imperial College London (Kaggle 2014)
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Data Quality Issue
tags:
- AI-Filled (Verify)
- Two-Regime Zeros
original_source: Kaggle
year: '2014'
domain: finance
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/competitions/loan-default-prediction
- https://www.kaggle.com/competitions/loan-default-prediction/discussion/6962
- https://www.kaggle.com/competitions/loan-default-prediction/discussion/7115
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-20 from a web search for zero-inflated regression candidates, the source pages and, where the notes say so, the downloaded data. A human must verify the suggestion, the metadata and the notes before relying on them.**

Kaggle research competition sponsored by researchers at Imperial College London (2014), data from an unnamed lender,
"standardized, de-trended, and anonymized" (data page). Target `loss`: 0 unless the loan defaulted, else the loss as
a percentage of the notional. Measured on train_v2.csv (2026-10-20): 105,471 rows x 769 anonymised features, 90.7%
zeros, 9,783 positives (integers 1-100, median 5), no missing or negative values. A host reply in forum topic 6862
says a default with full recovery also has loss 0. The rows are listed old to new, so a split would be temporal.
This is not `loan_default_prediction_challenge` (Zindi, a binary good/bad-loan task).

No for data quality. Mid-competition the host removed 9 columns that "incorporate some ex-post information" and
called any remaining leakage "fair game" (topic 6962). Two leaks remain. The difference f528 - f527 alone reaches
ROC AUC 0.92 for loss > 0, while untuned LightGBM on all raw columns reaches 0.72-0.73 (row-order, random and
f274-grouped 80/20 splits; R^2 0.53-0.55 on log1p loss among positives); a competitor noted that the removed pairs
f462/f463 and f473/f474 behaved the same way (topics 7115, 7398). And the rows are not independent loans: sorted by
f274 and f521, 96.5% of defaults are the last row of an f274 block (20.6% default rate there, 0.6% elsewhere), so a
sequence ends at its default, as in `iranian_churn`; that flag alone gives AUC 0.79, with the pair 0.94. The leak rules
keep unverified anonymised suspects (`homesite_quote_conversion`, `kick`), but here the host found ex-post aggregates of the same kind, and
with anonymised columns neither the prediction point nor the entity can be rebuilt. To check: whether a curator would
rather take TBD -> 2nd Tier with the pair and the id-like columns dropped. Terms: Kaggle rules, data for the
competition only.

## Reference

Imperial College London and Kaggle (2014). Loan Default Prediction - Imperial College London. Kaggle research
competition, closed 2014-03-14, https://www.kaggle.com/competitions/loan-default-prediction.

Lead: web search 2026-10-20 for zero-inflated regression candidates (not in the v4 workbook).
