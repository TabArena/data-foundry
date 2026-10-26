---
unique_name: glioma_grading_clinical_and_mutation_features
name: Glioma Grading Clinical and Mutation Features
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 2
tags:
- New IID
collections:
- TabSTAR
original_source: UCI
year: '2022'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.openml.org/search?type=data&id=46604
- https://www.kaggle.com/datasets/vinayjose/glioma-grading-clinical-and-mutation-features
- https://doi.org/10.24432/C5R62J
v2_path: datasets/_dev/tabarena-v0pt2/glioma_grading_clinical_and_mutation_features/dataset.py
source_row: 678
type_adapter_id: curation-record-v1
---

## Comments

"The main objective is to find the optimal subset of mutation genes and clinical features for the glioma grading process to improve performance and reduce costs." -> mostly a feature selection task?

I think we can still use it (as it is still suggested to be used this way)

**Assessment (AI, 2026-10-07):** A classification task. The paper classifies the grade with 10-fold CV (Tasci et al. 2022, Sec. 2.1; AUC 0.91-0.92, Table 3), and feature selection is its method. `Grade` is the TCGA project (LGG grade II/III vs GBM), and `Primary_Diagnosis` gives it away (dropped). The 20 flags are the GDC's whole-exome calls (17,220 of 17,240 cells match the GDC API). Each tissue site sent patients to one project, yet a by-site split scores like a random one (AUC 0.919 vs 0.918). This is not a duplicate of lgg_low_grade_glioma or glioblastoma: they share patients but have other targets. The label is TCGA-era histology. Under WHO 2021 the 25 IDH-mutant GBMs would be astrocytomas, still grade 4.

**Assessment (AI, 2026-10-20):** priority 2 for the review of the added dataset: gap -, use case -, source +, shape -, no known risk. A small, clean clinical-genomic binary task (862 patients); IDH1 and age carry most of the signal, and the label is TCGA-era histology.

**Assessment (AI, 2026-10-20):** review panel: ship after changes (text only, the data is unchanged; fit now approximate). Open (REVIEW.md): is a cross-check of a grade that already exists a use case (issue 5, USE-1), and confirm keeping a label right in its era but partly renamed by WHO 2021 (issue 1, USE-5); the tissue-site split is to be decided with sarcoma's issue 4 (features do not predict the site; grouped by site 0.921 / 0.927 against 0.921 / 0.924). The batch between the two TCGA projects is not triggered (LEAK-14/LEAK-15: one sequencing centre, one GDC workflow; amplified DNA not visible, ROC AUC 0.532). Priority 2: gap -, use case -, source +, shape -, risk 0 (use case: a cross-check we wrote, fit approximate; shape: 862 patients; risk: no leak, the open issues are rule readings, not an unclear target).

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — Tasci et al. 2022 select by accuracy with no threshold or costs for LGG vs GBM; accuracy rejected (MET-6, MET-8).

## Reference

@article{tasci2022hierarchical,
  title={Hierarchical voting-based feature selection and ensemble learning model scheme for glioma grading with clinical and molecular characteristics},
  author={Tasci, Erdal and Zhuge, Ying and Kaur, Harpreet and Camphausen, Kevin and Krauze, Andra Valentina},
  journal={International Journal of Molecular Sciences},
  volume={23},
  number={22},
  pages={14155},
  year={2022},
  publisher={MDPI}
}
