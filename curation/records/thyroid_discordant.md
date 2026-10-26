---
unique_name: thyroid_discordant
name: Thyroid Disease
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
tags:
- Tiny Data
- New IID
collections:
- TabArena Reject
- TabSTAR
original_source: UCI
year: '1987'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://github.com/EpistasisLab/pmlb/blob/master/datasets/new_thyroid/metadata.yaml
- https://www.kaggle.com/datasets/juliusgonsior/uci-new-thyroid
- (10.24432/C5D010)
notebook_path: datasets/beyond_iid/new_iid/thyroid_discordant/thyroid_discordant.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/thyroid_discordant/dataset.py
source_row: 790
type_adapter_id: curation-record-v1
---

## Comments

Data might be trivial, could be good to investigate all the data in this collection and add all the useful cases

Checkout all the data and add the datasets as we see valid

Insights from the reference:
1. Hypothyroid -> main dataset
2. dis -> version / same data as Hypothyroid

Based on this, we strongly believe that all other cases that have the same sample and feature count as listed below are just different versions/duplicates of Hypothyroid! Thus, for now, we only take Hypothyroid and ignore the other faulty entries. We might come back to this if Hypothyroid is too simple.
After a simple test, we saw that Hypothyroid is trivial to solve (almost 100 ROC AUC). Hence, we use dis instead. It still seems trivial. We will likely filter this later.


Patient ID at the end of the line does not matter.


A lot of weird data but a lot of okay ones that are super similar, so likely not use multiple? Read paper and make judgement call

Data in the repo:
1. thyroid0387 - Thyroid disease, Garavan Institute -> does not have a real target but just various diagnosis, seems like a scientific discovery task without a good target
2. sick-euthyroid.data -> according to UCI it might be corrupted, the .names file does not include any more information, missing more source information this is quite risky to use
3. sick -> has a clear class, but is missing any source information (first entry in the UCI description), likely a real predictive task
4. new-thyroid -> data from Stefan Aeberhard, seems good and has more source information
5. Hypothyroid -> same as sick-euthyroid
6. dis -> same as sick, looks good
7. ann-thyroid -> same as above, good
8. allrep -> same as above, good
9. allhypo -> same as above
10. allhyper -> same as above
11. allbp -> same as above

**Assessment (AI, 2026-10-19):** open since the leak audit of 2026-10-01 (no leak): one row has an `age` of 455. Under the rule for impossible values (they become missing and the row stays; caracas_cervical_cancer, 2026-10-15) the definition should set it to missing in the next pass.

CC (2026-10-21, Lennart): "ok" on the cross-dataset item that the `Trivial` marker was never tested under TP-4: run the test and keep or remove the marker by the result.

**Assessment (AI, 2026-10-21):** TP-4 test on the 30 shipped splits: the best single raw feature, chosen on each training side, is `FTI` on all 30, ROC AUC 0.822 on average (0.691 to 0.897), against 0.974 (0.913 to 0.996) for a default random forest and 0.973 (0.900 to 0.996) for LightGBM; the single feature is worse than both on 30 of 30 splits (task probe: one-feature LightGBM 0.869, random forest 0.976, no flag). The marker is refuted; recommend removing it (REVIEW.md issue 1); the curator has the call.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — no publication defines a task or metric for the discordant file; accuracy is uninformative at about 1.6% positives.

CC (2026-10-22, Lennart): verdict ship. Issue 1: remove the `Trivial` marker and go ahead.

**Assessment (AI, 2026-10-22):** `Trivial` removed (TP-4: the best single feature, `FTI`, reaches ROC AUC 0.822 against 0.974 for a random forest on the 30 shipped splits). REVIEW.md removed (nothing left open). Not built yet.

## Reference

@article{quinlan1987simplifying,
  title={Simplifying decision trees},
  author={Quinlan, J. Ross},
  journal={International journal of man-machine studies},
  volume={27},
  number={3},
  pages={221--234},
  year={1987},
  publisher={Elsevier}
}
@inproceedings{quinlan1987inductive,
  title={Inductive knowledge acquisition: a case study},
  author={Quinlan, John Ross and Compton, Paul J and Horn, KA and Lazarus, Leslie},
  booktitle={Proceedings of the Second Australian Conference on Applications of expert systems},
  pages={137--156},
  year={1987}
}
