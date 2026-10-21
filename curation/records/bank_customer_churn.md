---
unique_name: bank_customer_churn
name: Bank_Customer_Churn_Dataset / bank_customer_churn
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: 'Yes'
original_source: Kaggle
year: '2022'
required_split:
- Random (IID)
source_links:
- https://www.kaggle.com/datasets/gauravtopre/bank-customer-churn-dataset
notebook_path: datasets/beyond_iid/old_iid/bank_customer_churn/bank_customer_churn.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/bank_customer_churn/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Source for the Kaggle dataset likely from a data science course from (https://www.superdatascience.com/deep-learning), and the data/code is from here https://drive.google.com/drive/folders/1hGpnrfAVzcuHpNVQeHz46c_4tWmu1Y23

However, this does not seem to be the original dataset either.
Given the heavy usage of this data from this course, we keep the data source as is.

Looks like a recent and good dataset for churn applications over an international company with time invariant fetatures

Duplicate with shrutime (which however is older and has fake names?)

Potential issue: -

Lennart: No objection

Andrej: Licence & data source unclear

CC (2026-10-14, Lennart): No licence is known (Kaggle: 'Other (specified in description)', and the description names none), so the definition's licence is None.

CC (2026-10-21, Lennart): option (a) of the consistency check on one-snapshot churn sets: tagged `ForcedIIDFromTemporal`; SPLIT-8 now covers a release with one stock month or one undated snapshot.

**Assessment (AI, 2026-10-21):** tag and one note line added; a dated window would test the model on a later period's customers; not measurable on one undated snapshot.

CC (2026-10-21, Lennart): an upload whose first platform cannot be traced is kept for now, case by case, when the data looks sound and there is a source to point to ("if the data looks good enough even without a good source but there is a source, we want to keep it for now and risk it"); PROV-1/PROV-2 amended, the gap written as an approximate fit with a note.

**Assessment (AI, 2026-10-21):** listed as a case of the amended PROV-2; no change to the definition.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — Kaggle dataset (likely a course dataset) with no stated task metric; no first publication.
