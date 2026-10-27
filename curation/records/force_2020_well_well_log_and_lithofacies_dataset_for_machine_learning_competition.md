---
unique_name: force_2020_well_well_log_and_lithofacies_dataset_for_machine_learning_competition
name: FORCE 2020 Well well log and lithofacies dataset for machine learning competition
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
suggestion: 'Yes'
priority: 4
tags:
- Non-IID (Grouped)
- Review Prio 1 (Atlas)
collections:
- TabArena Submission
original_source: Github
year: '2020'
domain: environmental science & climate
required_split:
- Grouped (NON-IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://github.com/bolgebrygg/Force-2020-Machine-Learning-competition/tree/master
- https://zenodo.org/records/4351156
- https://github.com/TabArena/tabarena_dataset_curation/issues/2
- https://github.com/bolgebrygg/Force-2020-Machine-Learning-competition/tree/master/lithology_competition
- https://docs.google.com/document/d/13XAftsBVHIm01ZN0lP56Q4hZ9hgdYR1G_6KeV2DdzOA/edit?tab=t.0
v2_path: datasets/_dev/tabarena-v0pt2/force_2020_well_well_log_and_lithofacies_dataset_for_machine_learning_competition/dataset.py
source_row: 660
type_adapter_id: curation-record-v1
---

## Comments

Data based on images or other data is made tabular. But competitions used tabular models?

Need to double-check. Also, once checked, update GitHub issue! "

"We held out 10 wells where we only provided the logs (test dataset) and 10 wells that were not provided at all to the contestants."
"10 random wells from the train data set were used in preparing a validation set. Two validation sets were made from each train set prepared. "

**Assessment (AI, 2026-10-07):** Valid; added as a task grouped by well. Each row holds wireline readings at one depth, not a vectorised image, and tree ensembles won: XGBoost first and second, random forests third (technical retrospective in the repository, p. 3-4), and all 13 finalists used tree ensembles. All 118 wells have published labels, so they are stacked and split by well; the Zenodo LAS files carry the same labels. GROUP and FORMATION are NPD's stratigraphic picks (Zenodo NPD tables, Interpreter NPD), not the label interpreters', and the competition gave them as features. Licence: CC BY 4.0 (Zenodo), original logs NLOD 2.0. Open: whether models may use the well's other depths (the winners added depth windows).

CC (2026-10-12, Lennart): Kept in TabArena v0.2 after the task-probe review (flag `few_minority`, multiclass). Anhydrite (1,807 rows in 10 wells) and Halite (14,711 rows in 4 wells) are each missing from one of the 3 well-grouped test folds. These are not small classes: the well split leaves them out, which the definition already accepts as `splits_test_class_missing` with that reason.

**Assessment (AI, 2026-10-20):** priority 5 for the review of the added dataset: gap + (problem_type multiclass_classification), use case +, source +, shape +, no known risk. Large well-grouped multiclass task with a documented competition source and a direct use case; strong grouped-regime addition.

**Assessment (AI, 2026-10-20):** review panel (full): ship after changes; open for the curator are the fit with NPD's GROUP and FORMATION (a released-well use case or an approximate fit) and the metric (TP-6). Applied: values below -900, impossible negatives, DCAL above 100 and DRHO in 36/7-3 and 31/4-10 masked; a splits comment (departure from 98 / 10 / 10, test wells have drilled neighbours); the GROUP and FORMATION note reworded (boundaries 4x enriched on lithology changes, shared post-well sources); off-scale wells and metric facts noted; stale numbers corrected; fit_reason names the mud-log gap; domain environmental science & climate in the definition. Corrections to earlier lines: 12 of 13 finalists used only tree ensembles (one also a neural network); the GROUP and FORMATION timing is a known risk. Priority 4: gap + (multiclass), use case + (the competition's own task, interpreting a well's lithology), source + (organisers' repository, Zenodo record, retrospective), shape +, risk - (GROUP and FORMATION may postdate the prediction point, issue 2).

**Assessment (AI, 2026-10-20):** correction to the earlier 2026-10-20 lines: the "no known risk" of the first one does not hold. Whether NPD's GROUP and FORMATION exist when a newly drilled well is first interpreted is open (REVIEW.md issue 2), and the 2026-10-07 line's "all 13 finalists used tree ensembles" should read 12 of 13 used only tree ensembles (one team also a neural network).

CC (2026-10-21, Lennart): the declared metric documents the original use case's metric; overrule it only when it is biased or wrong (evidence from the paper); keep the note of the original metric (TP-6 amended).

**Assessment (AI, 2026-10-21):** metric set to `force_2020_penalty_matrix`, the competition's 12 x 12 penalty matrix over hard labels (was the default log loss). No listed metric ranks the same; the name is not registered downstream, so TabArena scores log loss until it is. Needs a rebuild to reach the container.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source cost_matrix (the competition's 11 x 11 penalty matrix without Basement, labels in the starter notebook's order) — the FORCE 2020 starter notebook's penalty matrix score on hard labels, renamed from force_2020_penalty_matrix; the scored metric changes from log_loss to cost_matrix (MET-4, MET-7, MET-12).

CC (2026-10-21, Lennart): use case restated as "a newly drilled or a released well" (option (a) of REVIEW.md issue 2): NPD publishes its GROUP and FORMATION picks for released wells, the wells the labels were built for; both stay as features and the fit stays direct (USE-9).

CC (2026-10-21, Lennart): curves on a second scale: follow the recommendation. ROP in 25/6-2, ROPA in 34/4-10 R, SGR in 34/12-1 and 35/11-15 S and MUDWEIGHT above 100 (16/10-2 and 281 rows of 15/9-14) are masked; MUDWEIGHT's two main scales stay, as both occur on every training side. His question whether the scales can be normalised is open (REVIEW.md issue 8).

CC (2026-10-21, Lennart): duplicate formation codes merged as proposed: Grid Mb., Skade Mb. and Ty Mb. become Grid Fm., Skade Fm. and Ty Fm. (CLEAN-14).

CC (2026-10-21, Lennart): Basement drop confirmed (103 rows, all in 16/4-1); recorded as a CLEAN-17 case.

**Assessment (AI, 2026-10-21):** domain set to environmental science & climate, the definition's. The LAS headers in the Zenodo zip were read (118 files): MUDWEIGHT and ROPA have no unit in any well, ROP says m/h in all 67 wells and SGR gAPI in all 14, so the headers were harmonised and do not identify a well's unit. From the data: ROPA is in ft/h in 32/2-1 and 16/10-5 (median ROP / ROPA 0.31 and 0.30, against 0.83-1.08 in 26 other wells); the 0.13-0.17 MUDWEIGHT wells fit bar/m (divided by 0.0981: per-well medians 1.34-1.77 g/cm3, against 1.08-1.80 in the g/cm3 wells); 16/7-4 (880 rows) and 25/3-1 (932 rows) hold both MUDWEIGHT scales; ROPA in 34/4-10 R is 1/87 of its ROP and SGR in 34/12-1 and 35/11-15 S is 1/5,283 and 1/3,323 of GR, no unit factor. Depth-window features under the declared penalty (random forest, 3 grouped folds, 2026-10-07 run before the masks): mean penalty 0.662 raw, 0.668 with windows (log loss 0.776 and 0.764). Scripts and logs: local-data-warehouse/_runs/2026-10-21_marks/force_2020/.

CC (2026-10-21, Lennart): Depth context: declare the depth order (`Grouping(time_on="DEPTH_MD")`) and ship no window features. Second scales: convert as the AI recommends.

**Assessment (AI, 2026-10-21):** Applied. `Grouping.time_on="DEPTH_MD"` records the order inside a well (it does not change the split; the derived regime tag becomes GroupedTemporal). `_clean` converts ROP in 32/2-1 and 16/10-5 from ft/h to m/h (x 0.3048, 5,814 rows; ROPA / ROP 0.31 and 0.30 before, 1.00 and 1.00 after) and MUDWEIGHT below 0.5 from bar/m to g/cm3 (/ 0.0980665, 225,528 rows; the 28 wells' per-well medians are now 1.08-1.80 g/cm3). Correction to the review-page answer of 2026-10-21: the ft/h curve in those two wells is ROP, not ROPA (the ratio there is ROPA / ROP = 0.31). The other off-scale curves stay masked. A CLEAN-21 case row records the conversion. dataset check: 0 errors, 0 warnings. Not rebuilt.

CC (2026-10-21, Lennart): the benchmark's LightGBM default is checked on this dataset later, not now ("we dont need to check the benchmark case, we can do that later, it is fine as is for now"): untuned LightGBM with `min_child_weight` 0.001 diverged here before the impossible readings were masked (test log loss 14-15 on grouped fold 0, 0.81 with `min_child_weight=1`). Tracked in the working copy's BENCHMARK_CHANGES_TODO.md (Model defaults).

CC (2026-10-26, Lennart): verdict ship.

## Reference

Bormann P., Aursand P., Dilib F., Dischington P., Manral S. 2020. FORCE Machine Learning Competition. https://github.com/bolgebrygg/Force-2020-Machine-Learning-competition
