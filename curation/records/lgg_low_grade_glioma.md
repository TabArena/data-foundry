---
unique_name: lgg_low_grade_glioma
name: LGG (low grade glioma)
checked_by:
- Andrej
suggestion: 'No'
decision_markers:
- Data Quality Issue
- Anonymized
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
source_row: 779
type_adapter_id: curation-record-v1
---

## Comments

Used in the TabPFN-Wide paper. Run download.sh in the git repo to get the data

**Assessment (AI, 2026-10-07):** Recommend `No` with `Data Quality Issue`; whether `Trivial` applies too is the curator's call. The MLOmics GS-LGG files are faulty in all three revisions. The methylation profiles do not match the patients (patient-similarity r with mRNA -0.005). The gene names do not describe the values: 1,147 mRNA and 1,425 copy-number rows are named `ZZZ<n>`/`ZZEF<n>`, 13 mRNA columns separate the patients' sex at AUC ≥ 0.997 under autosomal names, and GS-LGG shares one name column with GS-OV. The label is close to a two-column rule. A CNV column chosen on training data separates the codeletion class at test AUC 0.995. Two columns reach log loss 0.194, against 0.149-0.171 for full models. The task is multiclass, not binary.

CC (2026-10-16, Lennart): retired (`No`, `Data Quality Issue`) and removed from the working copy, as decided on 2026-10-12 (the release is faulty: methylation of other patients, gene names that do not describe the values). No rebuild from TCGA for now.

**Assessment (AI, 2026-10-16):** like `coad_colon_adenocarcinoma`, the expression values look standardised across patients by the release: over these 247 patients each mRNA and miRNA feature has a mean between -0.45 and 0.45 and an SD of 0.82-1.21 (copy number is not standardised). The definition is in git at commit 2475ea2.

## Reference

Z. Yang, R. Kotoge, X. Piao, Z. Chen, L. Zhu, P. Gao, Y. Matsubara, Y. Sakurai, and J. Sun. MLOmics: Cancer multi-omics database for machine learning. Scientific Data, 12(1):1–9, 2025.
