---
unique_name: sepsis_survival_minimal_clinical_records
name: Sepsis Survival Minimal Clinical Records
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: No (Retired)
decision_markers:
- Trivial
tags:
- Larger IID Data
- Tiny Data
- 'Samples: Over Time'
- 'Time: Lost'
- 'Target: Varying Delay'
- 'Entities: Recur'
collections:
- New (BeyondArena)
original_source: Other
year: '2017'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://archive.ics.uci.edu/dataset/827/sepsis+survival+minimal+clinical+records
- https://doi.org/10.24432/C53C8N
notebook_path: datasets/beyond_iid/new_iid/sepsis_survival_minimal_clinical_records/sepsis_survival_minimal_clinical_records.ipynb
source_row: 662
type_adapter_id: curation-record-v1
---

## Comments

CC: "It has three features, which sound hard to be fully meaningful. But it is a real task"

3 Features, unsure how trivial the dataset is

The dataset is full of "real" duplicates and is technically just a small or tiny dataset. We keep it as is to see how methods can handle it, but this is not really large data...

CC (2026-10-06, Lennart): Kept in TabArena v0.2 as a valid task by design after the task-probe review (flag `one_feature`). The 110,204 admissions hold only 975 distinct feature rows (age, sex, episode number; 7.4% died): the duplicates are real patients, and predicting survival from these three fields alone is the source paper's question. Age carries most of the signal but not all of it: age alone, chosen on each split's training side, gives ROC AUC 0.704, above only 6 of 28 BeyondArena configurations and below the best on all 9 folds; the best methods (TabPFN-3, tuned LightGBM, RealMLP) reach 0.707, a default random forest 0.689, and a lookup of each cell's death rate on the training side 0.689. So `Trivial` does not hold: sex and episode number add a small, consistent gain, and the methods gain by smoothing over age.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — Chicco & Jurman 2020 call PR AUC with Alive (92.6%) as positive their 'principal indicator', with ROC AUC, MCC, F1 and others; on our folds PR AUC sits at its floor 0.926 with a best of 0.966, so it resolves models poorly (MET-9). Original rejected: PR AUC on the majority class. roc_auc is the binary fallback.

CC (2026-10-21, Lennart): the roc_auc fallback, as proposed, over average_precision with Alive as positive (the paper's principal indicator): AUPRC on the 92.6% majority class sits between its floor of 0.926 and a best of 0.966 and resolves models poorly, while ROC AUC (about 0.7) separates them.

CC (2026-11-10, Andrej): retired (`No (Retired)`, `Trivial`): a clinician's rule, age plus about five years for men, ranks the patients within 0.001 of ROC AUC of TabPFN 3.5, and nothing learnable from the three columns lies beyond it.
- **The rule matches the best method:** on the 9 shipped splits, age alone reaches ROC AUC 0.7044, age + 5 years for men (not fitted) 0.7059, the best train-only smoother (an age spline per sex with a repeat-episode term by age, regularisation by inner cross-validation) 0.7065, TabPFN 3.5 0.7068; the rule trails TabPFN by 0.0010 ± 0.0002, while the splits' own ROC AUC runs from 0.699 to 0.710. An offset fitted per training side comes out at 3 to 5 years and scores the same (0.7058).
- **Nothing is left beyond the age-and-sex curve:** the best achievable ranking, each cell's true death rate, is estimated at about 0.709 (cell rates measured on all rows reach 0.722, of which 0.013 is the noise the same estimate shows on labels simulated from the smooth curve alone); shrinking each of the 975 cells toward the curve, with the strength chosen by inner cross-validation, takes it all the way to the curve on every split.
- **What TabPFN adds over age:** it keeps age's order on 94% of (died, survived) pairs; its gain (+0.0024) is men counted a few years older (+0.0019 net of large gains and losses) and a repeat episode in younger patients (+0.0005).
- **Why the earlier keep does not hold:** age alone below the best on every fold (Lennart, 2026-10-06) met the single-feature test of the time; the amended test counts a rule within the spread of the folds as a match, which makes the dataset a candidate to drop, not a forced retirement.
- **Curator call on top of the rules:** retired because the task is both almost solved and very simple. Almost solved: TabPFN 3.5 (0.7068) sits within about 0.002 of the best achievable ranking (about 0.709). Very simple: its gain over a naive baseline is +0.0024 ROC AUC over age alone and +0.0010 over the unfitted rule, too small to change any decision in practice; a benchmark task on which every method lands within 0.003 of a clinician's rule ranks nothing but smoothing.
Marker `Trivial` added, `v2_path` cleared, folder removed. Evidence: `~/claude_jobs/sepsis_tabpfn/` (TabPFN 3.5 on an A100, Slurm 1376270 and 1376610; `offset_fit.py`, `optimal.py`, `oracle_null.py`, `train_optimal.py`, `pairs.py`).

## Reference

@article{chicco2020survival,
  title={Survival prediction of patients with sepsis from age, sex, and septic episode number alone},
  author={Chicco, Davide and Jurman, Giuseppe},
  journal={Scientific reports},
  volume={10},
  number={1},
  pages={17156},
  year={2020},
  publisher={Nature Publishing Group UK London}
}
