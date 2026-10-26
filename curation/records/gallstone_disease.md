---
unique_name: gallstone_disease
name: Gallstone
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
decision_markers:
- Selection Bias
- Class-dependent Recording
tags:
- Tiny Data
collections:
- New (BeyondArena)
original_source: UCI
year: '2025'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://archive.ics.uci.edu/dataset/1150/gallstone-1
- https://doi.org/10.1097/md.0000000000037258
notebook_path: datasets/beyond_iid/new_iid/gallstone_disease/gallstone_disease.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/gallstone_disease/dataset.py
source_row: 768
type_adapter_id: curation-record-v1
---

## Comments

looks good

CC (2026-10-06, Lennart): Kept after the task-probe review: the `no_spread` flag does not hold. The three untuned families differ by 0.036 in skill (+0.683 to +0.719), which the probe compared, unpaired, with twice their typical standard error over 5 splits (0.054). Tuned methods spread clearly: on BeyondArena TabPFN-3.5 reaches ROC AUC 0.911 and the median method 0.883, with 8 of 29 methods tied with the best.

CC (2026-10-21, Andrej): Keep, with three changes to the data in `dataset.py` (not built). 319 outpatients of one Ankara clinic (2022-2023), in the file the 161 without gallstones first, then the 158 with; 242 remain. ROC AUC (3-fold x 20): TabPFN 3.5 0.838 (0.913 on the UCI file), gradient boosting 0.778, random forest 0.773, logistic regression 0.762 (0.857).

**Changes made:**
1. **Problem:** 77 rows (72 with gallstones, 5 without) were recorded through a second route: body fat to two decimals, water in whole kg, obesity % not from BMI, and a lower extracellular share of body water although they are heavier. Models recognise the route, not the disease: TabPFN 3.5 separates these cases from the controls at 0.993, the other cases at 0.842, and gives the 5 such controls a gallstone probability of 0.77 (0.22 for the others). Only 5 controls, so the route cannot be aligned with the other rows. **Change:** the 77 rows are dropped.
2. **Problem:** hyperlipidemia is set for 8 people with gallstones and nobody without, although total cholesterol of 240 mg/dL or more is as common (32 of 158 with, 35 of 161 without): it was recorded for one group only. **Change:** the column is dropped.
3. **Problem:** the number format gives the group away. GFR (kidney filtration rate) has two decimals for 80% of those without gallstones and 15% of those with, and the filled cells (below) carry up to 8 decimals in one group only; formatting alone gives ROC AUC 0.947. **Change:** GFR is written in whole numbers, vitamin D and visceral muscle area to one decimal, CRP (an inflammation marker) and creatinine to two, the precision of their measured values; formatting alone now gives 0.557.
4. **Problem:** UCI documents the label reversed (0 = gallstones), but the paper and the risk factors (57% vs 42% women, more body fat, lower vitamin D, more diabetes in class 1) show 1 = gallstones. **Change:** the task description says 1 = gallstones (86 of 242); the label values stay.
5. **Problem:** the task description did not say that the study left out 134 of its 454 outpatients, those whose gallbladder had been removed. **Change:** the description of a row says so, and that the second route is dropped.
6. **Problem:** the task description listed liver fat as a bioimpedance measure, but the fatty-liver grade comes from the ultrasound that also finds gallstones. **Change:** the list of known features names it as an ultrasound grade.
7. **Problem:** the use-case fit was rated "direct", although the groups were recorded apart and the liver grade needs an ultrasound. **Change:** rated "approximate", with both gaps named.
8. **Problem:** none of this was documented. **Change:** the curation comments describe each problem with its effect on the scores, with a table of the second route and a figure of the filled cells.
9. Record: Andrej added as reviewer (`checked_by`).
10. **Problem:** no marker said that the classes were measured, formatted and filled differently (`Selection Bias` is about which rows were sampled). **Change:** new marker `Class-dependent Recording`.

**Problems found, not changed** (they do not let a model tell the groups apart for reasons other than gallstones):
- Filled-in cells: 134 of the remaining values were filled with straight lines between the rows above and below (e.g. CRP 5.2, 4.16, 3.12, 2.08, 1.04, 0), although UCI calls the file complete: vitamin D 77 (all without gallstones), visceral muscle area 35 (all with), GFR 13, CRP 6, creatinine 3. Not a leak: re-imputed from the other features inside each training fold, without the label, TabPFN 3.5 reaches 0.864 (0.838 with the fills). Set to missing they would mark the groups, since vitamin D was measured for all 86 with gallstones but only 79 of the 156 without.
- The fatty-liver grade from ultrasound: a real association (TabPFN 3.5 0.834 without it).
- Data-entry errors, e.g. GFR 11.34 where the CKD-EPI 2021 equation gives 111.34, triglyceride 1.39.
- AST (a liver enzyme) is lower with gallstones (median 16.5 against 20), against what biliary disease would suggest, while ALT does not differ; possibly the groups' labs were run differently. It does not carry the score: TabPFN 3.5 0.826 without it, 0.827 with it (same folds).
- The fatty-liver grades look like two scales: no fatty liver about as common in both groups (41% without gallstones, 44% with), mild much rarer with gallstones (6% against 21%), moderate more common (38% against 29%). Small effect (TabPFN 3.5 0.834 without the column, 0.838 with it).
- Task probes flag `no_spread` (untuned linear model, random forest, LightGBM 0.754-0.768), but methods spread: TabPFN 3.5 beats the other three by 0.06-0.08 on 92-93% of the splits.
- Data access: the full data are not public (the paper: third-party data, shared on request); UCI lists the paper's authors as donors under CC BY 4.0.
- Not `Data Quality Issue`, which is for damage that cannot be repaired: the remaining artefacts do not leak.

Reference: Inker LA, Eneanya ND, Coresh J, et al. New creatinine- and cystatin C-based equations to estimate GFR without race. N Engl J Med. 2021;385(19):1737-1749. doi:10.1056/NEJMoa2102953.

## Reference

@article{esen2024early,
  title={Early prediction of gallstone disease with a machine learning-based method from bioimpedance and laboratory data},
  author={Esen, {\.I}rfan and Arslan, Hilal and Esen, Selin Akt{\"u}rk and G{\"u}l{\c{s}}en, Mervenur and K{\"u}ltekin, Nimet and {\"O}zdemir, O{\u{g}}uzhan},
  journal={Medicine},
  volume={103},
  number={8},
  pages={e37258},
  year={2024},
  publisher={LWW}
}
