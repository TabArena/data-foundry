---
unique_name: forensic_glass_identification
name: glass2
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
decision_markers:
- Outdated
tags:
- Tiny Data
collections:
- TabArena Reject
original_source: UCI
year: '1987'
domain: chemistry & material science
required_split:
- Random (IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://github.com/EpistasisLab/pmlb/blob/master/datasets/glass2/metadata.yaml
- https://doi.org/10.24432/C5WW2P
- https://www.openml.org/d/41
notebook_path: datasets/beyond_iid/new_iid/forensic_glass_identification/forensic_glass_identification.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/forensic_glass_identification/dataset.py
source_row: 755
type_adapter_id: curation-record-v1
---

## Comments

PMLB version has less samples and less classes, so likely filtered (?)

Generally a valid potential task, might be outdated but still valid for the task?

CC (2026-10-12, Lennart): Kept in TabArena v0.2 after the task-probe review (flag `few_minority`, multiclass). Tableware (class 6) has 9 rows, 3 in every test fold, and class 5 has 13 (4-5). Together they are 10% of the test rows and 14% of a random forest's log loss (0.70 against 1.51 for the class shares). Too Small is for a task whose scored units are a handful; one rare class of the source's own labels that does not decide the score is part of the task.

CC (2026-10-20, Andrej): Keep; no reason to exclude found, but the use case is dated.

- **Outdated:** 36% of rows are non-float window glass, which float glass (formed on molten tin) had replaced by the mid-1970s; casework today compares fragments by trace elements (LA-ICP-MS, laser mass spectrometry), not glass type by major oxides. Covered by the `Outdated` marker; methods still separate (29 configurations beat the dummy on 19/19 folds, Kendall's W 0.79).
- **Short classes:** the hardest is vehicle float glass (17 rows, 5-6 per test fold): 8% of the rows, 17% of a random forest's log loss; with containers and tableware, 18% of the rows carry 30%. Well below the share at which short classes decide the score (alvin: 51-54%).
- **Row order:** the file is sorted by class and, within a class, in a few blocks that each run roughly from high to low Mg (magnesium oxide; Kendall's tau -0.4 to -0.9); the features predict the Id order (Spearman 0.67-0.90 out of sample). Holding out stretches of Ids therefore holds out Mg ranges, not new objects: an order built from the features alone costs the same (TabPFN log loss 0.85, against 0.55 on random splits). Beyond the sort, fragments of one object sit next to each other (Ids 39-40 identical, 67-69 share the refractive index), but holding out blocks of 3 neighbours adds only 0.01 (TabPFN) to 0.06 (logistic regression) log loss and leaves the ranking unchanged. The random split stays.
- **Provenance:** rows were collected per class, not sampled from casework, so the class shares are arbitrary; the original technical note is unknown (`glass.names`). The creator was the UK Home Office Forensic Science Service (UCI's abstract says "USA"). PMLB glass2 is the 163-row float vs non-float window subset.

Done in `dataset.py`: dropped the exact duplicate (Ids 39 and 40), with a curation note on the row order; origin set to the UK Home Office Forensic Science Service; use-case fit set to approximate (dated features and glass types, class shares of a collection).

References: German B. Glass Identification. UCI Machine Learning Repository; 1987. doi:10.24432/C5WW2P. ASTM E2927-16e1, Standard Test Method for Determination of Trace Elements in Soda-Lime Glass Samples Using Laser Ablation Inductively Coupled Plasma Mass Spectrometry for Forensic Comparisons. ASTM International; 2016.

## Reference

@misc{German1987glass,
  author       = {German, B.},
  title        = {{Glass Identification}},
  year         = {1987},
  howpublished = {UCI Machine Learning Repository},
  note         = {{DOI}: https://doi.org/10.24432/C5WW2P}
}
