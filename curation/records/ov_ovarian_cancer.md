---
unique_name: ov_ovarian_cancer
name: OV (ovarian cancer)
checked_by:
- Andrej
suggestion: 'No'
decision_markers:
- No Good Target  / Scientific Discovery
tags:
- Tiny Data
collections:
- New (BeyondArena)
original_source: Github
year: '2025'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://github.com/chenzRG/Cancer-Multi-Omics-Benchmark.git
source_row: 780
type_adapter_id: curation-record-v1
---

## Comments

used in the TabPFN-Wide paper. Run download.sh in the git repo to get the data

**Assessment (AI, 2026-10-07):** The task is multiclass, not binary. The codes match the TCGA 2011 expression subtypes for 255 of 284 patients (Differentiated 64, Immunoreactive 79, Mesenchymal 67, Proliferative 74); MLOmics does not name its label source. In every MLOmics revision the gene names do not describe the values: thousands of rows are named `ZZZ<n>`/`ZZEF<n>`, GS-OV shares one name column with GS-LGG, and miRNAs of one genomic cluster do not correlate (r +0.05; GS-COAD +0.55). The values are real and match the patients, so the v2 folder names features by file row (Anonymized). The labels are microarray NMF clusters, but no rule reproduces them: a centroid model reaches log loss 0.511, LightGBM 0.413. No reason for `DF: Suspended` is recorded.

CC (2026-10-12, Lennart): No: the label, the TCGA 2011 transcriptional subtype, is an NMF cluster of the same tumours' expression; we do not benchmark labels that come from unsupervised learning; they are not a real predictive task.

## Reference

Z. Yang, R. Kotoge, X. Piao, Z. Chen, L. Zhu, P. Gao, Y. Matsubara, Y. Sakurai, and J. Sun. MLOmics: Cancer multi-omics database for machine learning. Scientific Data, 12(1):1–9, 2025.
