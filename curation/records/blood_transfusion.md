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
tags:
- 'Samples: One Moment'
- 'Target: Later'
- Database Snapshot
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

CC (2026-11-16, Andrej): time basis `ForcedIIDFromTemporal` instead of `DelayedTarget`, which is retired:
- A shared scoring date with a target window closed for every row makes the random split valid within that date only; one date is one period, too few for three windows, so the split is forced (SPLIT-8).
- The random split stays.

CC (2026-11-17, Andrej): the declared split (random, 20x3 folds, `ForcedIIDFromTemporal`) is checked: the split decision tree, walked without the current split, reaches the split it ships (blind split review, cross-dataset item).

CC (2026-11-18, Andrej): the forced tag stays (Review issue 1, A; stationarity reasoning, SPLIT-32 as amended today): no reason to take later samples as interchangeable. Use right after the moment counts for ASR, but behavioural response to a seasonal university drive moves, and similar behavioural sets measured not flat; mixed.

## Review

**Outcome:** added. Stationarity reasoning of 2026-11-18: the definition reaches the forced step with no time to measure; decided below.

**Main points:** Keep `ForcedIIDFromTemporal`, or tag `AssumedStationaryRelation`?

**Issues for Andrej:**

1. **Keep `ForcedIIDFromTemporal`, or tag `AssumedStationaryRelation`?**

   * **Problem:**
     - Time: One moment: one draw of 748 donors before the March 2007 drive, history counted to one reference date; no earlier or later drive in the release.
     - Use: The service picks donors to contact before the next drive, about three months after the data.
     - Mechanism: Recency, frequency and tenure to turning up at a university bus drive: donor behaviour, which moves with the academic calendar, campaigns and drive timing.
   * **Background:** similar datasets[^asr].

     | Similar dataset or source | What was measured | Verdict | Why similar |
     |---|---|---|---|
     | online_shoppers_purchasing_intention_dataset | v3 stationary-relation test by month | not flat | RFM-style behavioural response |
     | mobile_churn (splits.md Cases) | trained on June, tested on later joiners | not flat: ROC AUC 0.661 vs 0.690 IID | one-moment behavioural customer base |

   * **For a stationary use case:**
     - use right after the collected moment (next drive, ~3 months)
     - the RFM relation is a long-known regularity.
   * **Against:**
     - behaviour, not physiology: response depends on campaigns and calendar.
     - the bus collects at a university: a summer drive meets students away.
     - one drive is one period: nothing measured.
     - similar behavioural sets test not flat.
   * **Earlier views:**
     - CC 2026-11-16 (Andrej): ForcedIIDFromTemporal instead of DelayedTarget; one drive is one period.
     - CC 2026-11-17 (Andrej): random 20x3 checked by blind walk.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep `ForcedIIDFromTemporal` (implemented) | The folds stay; the Time basis line names the reasoning below | Claims only what is known | The split stands for later samples only as far as the use case is stationary |
     | B | `AssumedStationaryRelation` | The folds stay; you give the reason (eight words or more) | Documents why random folds stand for later samples | behaviour, not physiology: response depends on campaigns and calendar; the bus collects at a university: a summer drive meets students away |

   * **Recommendation:** A, use right after the moment counts for ASR, but behavioural response to a seasonal university drive moves, and similar behavioural sets measured not flat; mixed. Confidence: medium. **Decision:** A or B?

   [^asr]: **SPLIT-32** (Should; amended 2026-11-18, Andrej): "where it holds none, the review reasons whether the use case can be taken as stationary, from the domain's mechanism and from similar datasets ..., where the AI offers `AssumedStationaryRelation` with a recommendation for a person to decide." `AssumedStationaryRelation` keeps the forced split's folds and replaces only the tag; its line opens `AssumedStationaryRelation (<person>, <date>): <reason>`.

   **Andrej (2026-11-18, ok):** as implemented.

   **Resolved (2026-11-18, Andrej):** A, as implemented: the forced tag stays; the `Time basis:` line gives the reasoning (Use right after the moment counts for ASR, but behavioural response to a seasonal university drive moves, and similar behavioural sets measured not flat; mixed.)

## Reference

Yeh, I-Cheng, Yang, King-Jang, and Ting, Tao-Ming, "Knowledge discovery on RFM model using Bernoulli sequence", Expert Systems with Applications, 2008.
