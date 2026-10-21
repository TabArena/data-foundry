---
unique_name: blood_transfusion
name: blood-transfusion-service-center / blood_transfusion
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: 'Yes'
original_source: UCI
year: '2008'
required_split:
- Random (IID)
problem_type: Binary Classification
source_links:
- https://www.openml.org/search?type=data&id=1464
- https://doi.org/10.24432/C5GS39
notebook_path: datasets/beyond_iid/old_iid/blood_transfusion/blood_transfusion.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/blood_transfusion/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Nice task with time-invariant features to predict a future event, so already framed so it can be used with random splits. NNs outperform trees & linear performs similar to trees, so likely pretty simple task; known to make models overfit quickly

Potential issue: maybe trivial

Lennart: no objection

Andrej: Matches criteria

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — The paper fits an RFMTC (Bernoulli sequence) model and compares predicted with actual response across donor groups and against plain RFM; no per-donor metric is named in what is accessible (full text paywalled). The ranking of donors to contact fits ROC AUC.

## Reference

Yeh, I-Cheng, Yang, King-Jang, and Ting, Tao-Ming, "Knowledge discovery on RFM model using Bernoulli sequence", Expert Systems with Applications, 2008.
