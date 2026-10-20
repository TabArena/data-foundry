---
unique_name: coad_colon_adenocarcinoma
name: COAD (colon adenocarcinoma)
checked_by:
- Andrej
suggestion: 'No'
decision_markers:
- Data Quality Issue
tags:
- Tiny Data
collections:
- New (BeyondArena)
original_source: Github
year: '2024'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://github.com/chenzRG/Cancer-Multi-Omics-Benchmark.git
source_row: 781
type_adapter_id: curation-record-v1
---

## Comments

Used in the TabPFN-Wide paper. Run download.sh in the git repo to get the data.

**Assessment (AI, 2026-10-07):** The task is multiclass, not binary. The label codes match the TCGA PanCancer Atlas classes for all 260 patients (CIN 174, MSI 48, GS 34, HM-SNV 4), and TabPFN-Wide (arXiv 2510.06162, Appendix D) uses them unchanged. The classes come from data that do not ship: exome indel density for MSI (tumour mutation burden separates it at AUC 1.000), and a clonal deletion score > 0.0249 for CIN against GS (Liu et al. 2018, "Molecular Subtypes within GIAC"). No rule on the shipped blocks reproduces them (trees AUC 0.79-0.84, full models 0.93). Unlike GS-LGG and GS-OV of the same release, the gene names pass every check. No reason for `DF: Suspended` is recorded.

CC (2026-10-12, Lennart): Drop the copy-number block. Copy-number changes define CIN against GS (Liu et al. 2018), so a lab that has them computes the subtype by the published procedure; the realistic task is the DNA-defined subtype from expression and methylation. Without the block a random forest still reaches macro ROC AUC 0.923 (0.935 with it; 0.901 on the block alone).

CC (2026-10-15, Lennart): multiclass (CIN, MSI, GS), the 4 HM-SNV tumours dropped. Keep every relevant feature however wide (36,355 ship); width and a model's feature cap are no argument.

CC (2026-10-16, Lennart): retired for now. The release z-scored every feature over all 260 patients, test rows included: a transductive leak, since a deployed model never has the test patients' means and SDs. The data are to be rebuilt from TCGA's own files as `tcga_coad_molecular_subtype`; the task decisions above carry over.

**Assessment (AI, 2026-10-16):** I had called the scaling harmless because it uses no labels and leaves the predictions of tree models, and of models that standardise each feature on the train side, unchanged. That was too narrow. Every stored value depends on the test rows: from the training rows alone, a test fold's mean of each feature is minus n_train/n_test times the training mean of its z-scores, and its variance follows the same way, so each split shows the model the test patients' distribution, which no deployed model has. A model that does not rescale every feature on its training rows also sees values shifted by the test rows. MLOmics publishes neither unscaled values nor the scaling constants (GitHub issue #3), so the fix is a rebuild from the source. The folder left the working copy on 2026-10-16; the definition is in git at commit 2475ea2.

## Reference

Z. Yang, R. Kotoge, X. Piao, Z. Chen, L. Zhu, P. Gao, Y. Matsubara, Y. Sakurai, and J. Sun. MLOmics: Cancer multi-omics database for machine learning. Scientific Data, 12(1):1–9, 2025.
