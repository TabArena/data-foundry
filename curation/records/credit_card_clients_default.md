---
unique_name: credit_card_clients_default
name: Default of Credit Card Clients / credit_card_clients_default
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: 'Yes'
original_source: UCI
year: '2016'
required_split:
- Random (IID)
source_links:
- https://doi.org/10.24432/C55S3H
notebook_path: datasets/beyond_iid/old_iid/credit_card_clients_default/credit_card_clients_default.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/credit_card_clients_default/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Predict default on payment or not, uses time-invariant temporal features of the payment history

Potential issue: temporal features?

Lennart: Temporal impact can likely be ignored with these features

Andrej: Seems fine

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source roc_auc — Yeh & Lien 2009 score the lift chart's area ratio, which equals 2 x ROC AUC - 1.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): left unordered: `EDUCATION` (a level outside the scale is a state of its own).

## Reference

The comparisons of data mining techniques for the predictive accuracy of probability of default of credit card clients
By I. Yeh, Che-hui Lien. 2009

Published in Expert systems with applications
