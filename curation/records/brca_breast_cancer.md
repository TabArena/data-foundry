---
unique_name: brca_breast_cancer
name: BRCA (breast cancer)
checked_by:
- Andrej
suggestion: 'No'
decision_markers:
- No Good Target / Scientific Discovery
tags:
- Tiny Data
collections:
- New (BeyondArena)
original_source: Website
year: '2018'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://acgt.cs.tau.ac.il/multi_omic_benchmark/download.html
source_row: 782
type_adapter_id: curation-record-v1
---

## Comments

used in the TabPFN-Wide paper. from their download instructions: to map the methylation probe IDs to gene symbols, download the file from `https://webdata.illumina.com/downloads/productfiles/humanmethylation450/humanmethylation450_15017482_v1-2.csv`

**Assessment (AI, 2026-10-07):** No reason for `DF: Suspended` is recorded here or in git. TabPFN-Wide (arXiv 2510.06162v1, Sec. 5; loader `analysis/load_mm_data.py`) classifies `PAM50Call_RNAseq`: five classes, so `problem_type` should be Multiclass Classification. That call is the PAM50 rule applied to the same RNA-seq: the published centroids on its 50 genes reproduce 347 of the 381 calls, and a regression on the 5 centroid correlations beats a random forest on all 26,035 omic columns (log loss 0.35 against 0.55). Added as `datasets/_dev/tabarena-v0pt2/brca_breast_cancer/` without the expression block: methylation and miRNA, 381 x 5,864 (random forest macro ROC AUC 0.94). The alternative is to retire it as `Trivial`.

CC (2026-10-12, Lennart): No: the label, the PAM50 subtype, is a taxonomy that came from clustering expression profiles and is assigned by a centroid rule on 50 genes; we do not benchmark labels that come from unsupervised learning; they are not a real predictive task.

## Reference

N. Rappoport and R. Shamir. Multi-omic and multi-view clustering algorithms: review and cancer benchmark. Nucleic Acids Research, 46(20):10546–10562, Oct 2018. URL https://doi. org/10.1093/nar/gky889.
