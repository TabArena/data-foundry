---
unique_name: mice_protein_trisomy_discriminant
name: MiceProtein
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: No (Retired)
decision_markers:
- No Good Target  / Scientific Discovery
tags:
- Non-IID (Grouped)
collections:
- TabArena Reject
- TabSTAR
year: '2015'
domain: biology & life sciences
required_split:
- Grouped (NON-IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C50S3Z
notebook_path: datasets/beyond_iid/grouped/mice_protein_trisomy_discriminant/mice_protein_trisomy_discriminant.ipynb
source_row: 692
type_adapter_id: curation-record-v1
---

## Comments

CC: "Data clustered by 77 proteins and 72 mice. Each protein contains 1080 measurements which are recommended to be seen as separate mice. Therefore a group-based split based on proteins makes sense. Unsure whether predictive performance is the goal or rather interpretation. Also unsure whether the 8 classes given should also be used as they are for classification, might also be framed as a multi-task problem."

CC (2026-10-01, Lennart): **Retired: no predictive target (crit. 3, scientific discovery).** The 8 classes are the experimental design: genotype (from breeding), training protocol (context-shock or shock-context) and injection (memantine or saline), all known for every mouse before any protein is measured. Neither source predicts: Higuera et al. 2015 cluster the mice with self-organising maps to find proteins linked to learning, and Ahmed et al. 2015 (PLoS ONE 10:e0119491, where the measurements come from) test group differences with mixed-effects models. The one outcome that would be a target, learning, was not measured: "Mice were sacrificed at 60 minutes post training without measurement of freezing" (Ahmed et al.).
- On the data (72 mice, per-mouse means, grouped 20x3): every model separates the protocol perfectly (AUC 1.0; SOD1 alone does, about 2.4x lower after context-shock), genotype reaches AUC 0.93 and treatment 0.77, so the 8-class score (macro AUC 0.92) mixes a trivial part with two labels set by the experimenter.
- The 1,080 rows are 15 spots per mouse (three replicates of a five-point dilution series of one lysate), with 7-10 mice per class. The rows are grouped by mouse, not by protein (the proteins are the columns).

## Reference

Higuera C, Gardiner KJ, Cios KJ (2015) Self-Organizing Feature Maps Identify Proteins Critical to Learning in a Mouse Model of Down Syndrome. PLoS ONE 10(6): e0129126.
