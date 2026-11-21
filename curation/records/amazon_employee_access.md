---
unique_name: amazon_employee_access
name: Amazon_employee_access
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: 'Yes'
tags:
- 'Samples: Over Time'
- 'Time: Lost'
- 'Target: Varying Delay'
- 'Entities: Recur'
- Database Snapshot
original_source: Kaggle
year: '2013'
collection_period: 2010-2011
required_split:
- Random (IID)
problem_type: Binary Classification
source_links:
- https://www.openml.org/search?type=data&id=4135
- https://www.kaggle.com/c/amazon-employee-access-challenge
notebook_path: datasets/beyond_iid/old_iid/amazon_employee_access/amazon_employee_access.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/amazon_employee_access/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

I LOVE this dataset - we need to include it. BUT: Need to carefully check how the split in the Kaggle challenge was. Also could require time split - but it seems as if the task was conceptualized with time-invariant features

Potential issue: grouped data (manager-employees); test data was temporal (only on new employees!); problem in words: if the train samples in the kaggle data would have the same employee multiple times for multiple resources, then it breaks non-grouped/non-temporal assumptions

Lennart: Yes, if the groups are not a problem and we do not have repeated employee entries? Time should be ignorable as the processes did not change during collection (?);

Andrej: Fits criteria

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source roc_auc — Area Under Receiver Operating Characteristic Curve (https://www.kaggle.com/competitions/amazon-employee-access-challenge (Kaggle API evaluationMetric)).

CC (2026-11-17, Andrej): the declared split (random, 3x3 folds, `ForcedIIDFromTemporal`) is checked: the split decision tree, walked without the current split, reaches the split it ships (blind split walk, cross-dataset item).

CC (2026-11-18, Andrej): the forced tag stays (Review issue 1, A; stationarity reasoning, SPLIT-32 as amended today): no reason to take later samples as interchangeable. A use right after the period would support ASR, but the benchmark stands for later requests under a policy and role structure that change; Lennart's earlier view was a question, not evidence.

## Review

**Outcome:** added. Stationarity reasoning of 2026-11-18: the forced tag stays (issue 1, A, Andrej).

**Main points:** Nothing open: `ForcedIIDFromTemporal` stays, not `AssumedStationaryRelation` (issue 1 resolved on 2026-11-18).

**Issues for Andrej:**

1. **Keep `ForcedIIDFromTemporal`, or tag `AssumedStationaryRelation`?**

   * **Problem:**
     - Time: Requests made 2010-2011 with no request date; Kaggle's training file is shuffled (denial rate flat over tenths, chi-squared p = 0.45), and UCI 216's dated access history uses other ids.
     - Use: Amazon predicts whether a new access request would be granted, for requests after 2011.
     - Mechanism: Grants follow the company's role-based access policy: role, department and resource codes map to a decision by policy, which changes with reorganisations, new resources and security rules.
   * **Background:** similar datasets[^asr].

     | Similar dataset or source | What was measured | Verdict | Why similar |
     |---|---|---|---|
     | none in the collection (literature, cited from memory: check) | no dated access-control set measured | none | - |

   * **For a stationary use case:**
     - A policy mapping from role to grant is stable within an organisation for a while; the competition's own use was right after the 2010-2011 period.
     - No adversary or price in the decision.
   * **Against:**
     - Changed rules: access policy and role structure change with reorganisations; resource ids and role codes appear and retire.
     - Target: Varying Delay (grant/revoke decided later).
     - Entities: Recur (managers, roles repeat), so later requests meet new roles not seen.
     - Nothing dated measured, here or in a similar set.
   * **Earlier views:**
     - Undated note (Lennart, record): 'Time should be ignorable as the processes did not change during collection (?)', raised as a question.
     - CC (2026-11-17, Andrej): blind walk reaches the shipped random split with ForcedIIDFromTemporal.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep `ForcedIIDFromTemporal` (implemented) | The folds stay; the Time basis line names the reasoning below | Claims only what is known | The split stands for later samples only as far as the use case is stationary |
     | B | `AssumedStationaryRelation` | The folds stay; you give the reason (eight words or more) | Documents why random folds stand for later samples | Changed rules: access policy and role structure change with reorganisations; resource ids and role codes appear and retire.; Target: Varying Delay (grant/revoke decided later). |

   * **Recommendation:** A, a use right after the period would support ASR, but the benchmark stands for later requests under a policy and role structure that change; Lennart's earlier view was a question, not evidence. Confidence: medium. **Decision:** A or B?

   [^asr]: **SPLIT-32** (Should; amended 2026-11-18, Andrej): "where it holds none, the review reasons whether the use case can be taken as stationary, from the domain's mechanism and from similar datasets ..., where the AI offers `AssumedStationaryRelation` with a recommendation for a person to decide." `AssumedStationaryRelation` keeps the forced split's folds and replaces only the tag; its line opens `AssumedStationaryRelation (<person>, <date>): <reason>`.

   **Andrej (2026-11-18, ok):** as implemented.

   **Resolved (2026-11-18, Andrej):** A, as implemented: the forced tag stays; the `Time basis:` line gives the reasoning (A use right after the period would support ASR, but the benchmark stands for later requests under a policy and role structure that change; Lennart's earlier view was a question, not evidence.)

## Reference

https://www.kaggle.com/c/amazon-employee-access-challenge
