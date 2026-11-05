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
suggestion: No (Retired)
decision_markers:
- AHDS (Artifical/Handmade/Deterministic/Simulated)
- Missing source information
original_source: Kaggle
year: '2022'
required_split:
- Random (IID)
source_links:
- https://www.kaggle.com/datasets/gauravtopre/bank-customer-churn-dataset
notebook_path: datasets/beyond_iid/old_iid/bank_customer_churn/bank_customer_churn.ipynb
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

**Assessment (AI, 2026-11-04):** reviewed for the BeyondArena v0.2 review page, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the folder's `REVIEW.md`. Retire as generated: seven of ten columns carry next to nothing beyond the class (within-class shuffle AUC 0.48-0.53 against 0.54-0.76 on the real bank_marketing), tenure is flat over age, and a hand-written class-first Bayes net beats all 41 benchmark methods. Priority 1: gap 0, use case 0, source 0, shape 1, risk -1.

CC (2026-11-04, Andrej): retired as generated data (`No (Retired)`, `AHDS`, `Missing source information`). The table comes from a data-science course (SuperDataScience, Deep Learning A-Z) and names no bank, period or generation method.
- **How it was generated:** a class-rooted Bayes net (a sampler that draws the label first, then each column given the label and at most two other columns), written down by hand: churn first; country, gender, activity and number of products given churn; a zero balance given churn, country and products; a positive balance around one shared centre (about 120,000), its spread given churn and country; age given churn and activity; credit score given churn (capped at 850); tenure, salary and the card flag independent noise.
- **The generator beats every method:** used as a classifier on the 9 shipped splits it scores 1 - ROC AUC 0.1213, ahead of all 40 benchmark methods (best 0.1233, TabPFN-3.5 0.1240), so the task ranks methods by how well they recover a sampler's densities, not how customers leave.
- **Checks calibrated on a real bank table agree:** seven of the ten columns cannot be told from a copy shuffled within each class (ROC AUC 0.48-0.53; every client column of bank_marketing 0.54-0.76), tenure does not rise with age, salary is uniform from 12 to 200,000.
- **Why the keep of 2026-10-21 no longer holds:** it rested on a named course counting as a source when the data shows no marks of generation; the data shows them, as for credit_card_customers.

