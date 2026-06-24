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
type_adapter_id: curation-record-v1
---

# blood-transfusion-service-center / blood_transfusion

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Nice task with time-invariant features to predict a future event, so already framed so it can be used with random splits. NNs outperform trees & linear performs similar to trees, so likely pretty simple task; known to make models overfit quickly

Potential issue: maybe trivial

Lennart: no objection

Andrej: Matches criteria

## Reference

Yeh, I-Cheng, Yang, King-Jang, and Ting, Tao-Ming, "Knowledge discovery on RFM model using Bernoulli sequence", Expert Systems with Applications, 2008.
