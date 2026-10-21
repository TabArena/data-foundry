---
unique_name: force_2020_well_well_log_and_lithofacies_dataset_for_machine_learning_competition
name: FORCE 2020 Well well log and lithofacies dataset for machine learning competition
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 4
tags:
- Non-IID (Grouped)
- Review Prio 1 (Atlas)
collections:
- TabArena Submission
original_source: Github
year: '2020'
domain: chemistry & material science
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

## Reference

Bormann P., Aursand P., Dilib F., Dischington P., Manral S. 2020. FORCE Machine Learning Competition. https://github.com/bolgebrygg/Force-2020-Machine-Learning-competition
