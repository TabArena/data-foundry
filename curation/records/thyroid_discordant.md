---
unique_name: thyroid_discordant
name: Thyroid Disease
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
decision_markers:
- Trivial
tags:
- Tiny Data
- New IID
collections:
- TabArena Reject
- TabSTAR
original_source: UCI
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: TBD
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://github.com/EpistasisLab/pmlb/blob/master/datasets/new_thyroid/metadata.yaml
- https://www.kaggle.com/datasets/juliusgonsior/uci-new-thyroid
- (10.24432/C5D010)
source_row: 790
type_adapter_id: curation-record-v1
---

# Thyroid Disease

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
