---
unique_name: customer_churn_prediction_challenge_for_azubian
name: customer-churn-prediction-challenge-for-azubian
checked_by:
- Lennart
suggestion: 'No'
decision_markers:
- Duplicate
collections:
- New (BeyondArena)
original_source: Zindi
year: '2023'
domain: business & marketing
required_split:
- '?'
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://zindi.africa/competitions/customer-churn-prediction-challenge-for-azubian
- https://github.com/BrianBassey37/Azubi_Capstone/tree/main/DataSet
- https://github.com/M-travis123/Customer-Churn-Prediction-for-Azubian/tree/main/Data
source_row: 961
type_adapter_id: curation-record-v1
---

## Comments

**AI summary:**
Customer churn prediction challenge (Zindi, 'for Azubian'). Telco/customer churn task with a binary target. Likely transaction/usage records that must be aggregated per customer before modelling; the appropriate split (random vs temporal vs grouped-by-customer) and the post-aggregation row count are unknown and need to be confirmed from the data. Real competition data with a clear predictive task → worth investigating for the benchmark.



Comments from Lennart: there seems to be a backup for the data on GitHub, and I cannot accept the terms for an arleady finishes competition; data has regions and thus has geospatial signal

**Duplicate of `expresso_churn_prediction`** — same Expresso data, a different train/test cut. Zindi's
Azubian page names Expresso as the provider and the 19 columns match exactly; `expresso_churn_prediction`
already lists five Zindi re-runs of this data, so Azubian is a sixth. Which cut we keep is still open.

Labelled train downloads from the `M-travis123` mirror without a Zindi login, via the Git LFS endpoint
(`media.githubusercontent.com/media/.../Data/Train.csv`; the plain `raw.` URL returns only the pointer).
Checked: 1,077,024 x 19, `CHURN` 18.8% positive, one row per customer, no time index → `Random (IID)`,
and `original_data_state` is really one table (the "database" was Azubi's SQL Server teaching setup).
