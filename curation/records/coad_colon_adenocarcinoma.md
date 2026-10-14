---
unique_name: coad_colon_adenocarcinoma
name: COAD (colon adenocarcinoma)
checked_by:
- Andrej
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
tags:
- Tiny Data
collections:
- New (BeyondArena)
original_source: Github
year: '2024'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://github.com/chenzRG/Cancer-Multi-Omics-Benchmark.git
v2_path: datasets/_dev/tabarena-v0pt2/coad_colon_adenocarcinoma/dataset.py
source_row: 781
type_adapter_id: curation-record-v1
---

## Comments

Used in the TabPFN-Wide paper. Run download.sh in the git repo to get the data.

**Assessment (AI, 2026-10-07):** The task is multiclass, not binary. The label codes match the TCGA PanCancer Atlas classes for all 260 patients (CIN 174, MSI 48, GS 34, HM-SNV 4), and TabPFN-Wide (arXiv 2510.06162, Appendix D) uses them unchanged. The classes come from data that do not ship: exome indel density for MSI (tumour mutation burden separates it at AUC 1.000), and a clonal deletion score > 0.0249 for CIN against GS (Liu et al. 2018, "Molecular Subtypes within GIAC"). No rule on the shipped blocks reproduces them (trees AUC 0.79-0.84, full models 0.93). Unlike GS-LGG and GS-OV of the same release, the gene names pass every check. No reason for `DF: Suspended` is recorded.

CC (2026-10-12, Lennart): Drop the copy-number block. Copy-number changes define CIN against GS (Liu et al. 2018), so a lab that has them computes the subtype by the published procedure; the realistic task is the DNA-defined subtype from expression and methylation. Without the block a random forest still reaches macro ROC AUC 0.923 (0.935 with it; 0.901 on the block alone).

## Reference

Z. Yang, R. Kotoge, X. Piao, Z. Chen, L. Zhu, P. Gao, Y. Matsubara, Y. Sakurai, and J. Sun. MLOmics: Cancer multi-omics database for machine learning. Scientific Data, 12(1):1–9, 2025.
