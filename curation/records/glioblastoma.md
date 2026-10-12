---
unique_name: glioblastoma
name: GBM
checked_by:
- Andrej
suggestion: 'No'
decision_markers:
- No Good Target  / Scientific Discovery
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
v2_path: datasets/_dev/tabarena-v0pt2/glioblastoma/dataset.py
source_row: 784
type_adapter_id: curation-record-v1
---

## Comments

used in the TabPFN-Wide paper. From their download instructions: to map the methylation probe IDs to gene symbols, download the file from `https://webdata.illumina.com/downloads/productfiles/humanmethylation450/humanmethylation450_15017482_v1-2.csv`

**Assessment (AI, 2026-10-07):** No reason for `DF: Suspended` is recorded here or in git. TabPFN-Wide (arXiv 2510.06162v1) used GBM for model selection (Sec. 4.2) with `GeneExp_Subtype`: four classes, so `problem_type` should be Multiclass Classification. That label is the TCGA 2013 expression subtype: Brennan et al. (Cell 2013) assigned the 342 tumours outside Verhaak 2010 "using single sample gene set enrichment analysis", and the Verhaak gene sets scored on the shipped U133A block reproduce 216 of 274 labels. Added as `datasets/_dev/tabarena-v0pt2/glioblastoma/` without the expression block: methylation and miRNA, 274 x 5,534 (random forest macro ROC AUC 0.87). The patients overlap glioma_grading, whose features and target differ.

CC (2026-10-12, Lennart): No: the label, the expression subtype, is a taxonomy from clustering expression profiles, assigned from signature scores of the same expression; we do not benchmark labels that come from unsupervised learning; they are not a real predictive task.

## Reference

N. Rappoport and R. Shamir. Multi-omic and multi-view clustering algorithms: review and cancer benchmark. Nucleic Acids Research, 46(20):10546–10562, Oct 2018. URL https://doi. org/10.1093/nar/gky889.
