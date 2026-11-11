---
unique_name: lung_adenocarcinoma_metastasis
name: Lung adenocarcinoma, metastasis from another organ or primary (Bhattacharjee 2001, GEO arrays)
checked_by:
- Andrej
data_foundry_status:
- 'DF: Yes'
suggestion: 'Yes'
tags:
- New IID
- Many features
- Tiny Data
original_source: Other
year: '2001'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- 'https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE83227 (the study''s deposit of all 254 arrays, per-array MAS5 files)'
- 'https://ftp.ncbi.nlm.nih.gov/geo/series/GSE83nnn/GSE83227/suppl/GSE83227_caArray_meyer-00191.tar.gz (the study''s annotation sheet SampleData.xls, sheet DATASET B: the metastasis flags; also the paper, 13790.pdf)'
- https://www.pnas.org/doi/10.1073/pnas.191502998
v2_path: datasets/_dev/tabarena-v0pt2/lung_adenocarcinoma_metastasis/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

CC (2026-11-11, Andrej): new record for the metastasis task on the arrays of `lung_cancer`, whose histology target was retired on 2026-11-10 (BeyondArena v0.2 review page, lung_cancer issues 7, B, and 4, B: a new record, as coad_colon_adenocarcinoma and aeolus were rebuilt). Ship.
- **The source's own task:** "A key issue in lung tumor diagnosis is the discrimination of a primary lung adenocarcinoma from a distant metastasis to the lung" (Bhattacharjee et al. 2001, Results); "metastases of nonlung origin can be difficult to distinguish from lung adenocarcinomas" (Introduction). The paper finds them by clustering and scores no classifier.
- **The label comes from outside the arrays:** the study's annotation sheet (`SampleData.xls`, sheet DATASET B, in GEO's caArray archive) flags 16 of its 139 adenocarcinomas as "possible mets" (8 colon, 4 breast, 4 other), from the clinical history and pathology report. All 16 count, the soft "c/w" and "?" calls included (issue 8, A).
- **Rows:** the 127 adenocarcinomas with a clinical history; the 12 `A` patients have no clinical annotation, so "no flag" is no finding for them. One MAS5 array per tumour, scaled on that array alone (the GEO rebuild of lung_cancer's issue 1).
- **Size:** 5 or 6 metastases per test fold. The task probe raises no flag (10 repeats of 3 folds; random forest ROC AUC 0.887, ahead of the class shares on 30 of 30 splits; SVM 0.885, TabPFN 3.5 0.882, logistic regression 0.850, k-nearest neighbours 0.779); ten unfitted pathology marker genes reach 0.819. Metric ROC AUC: logistic regression and LightGBM score worse than the class shares on log loss.
- **Recording:** the 67 control probes carry no signal on this target (ROC AUC 0.42, non-human spike-ins 0.40, array QC values 0.52).
- **Known gaps:** the label is "possible", not a confirmed origin (fit approximate); the paper's colon cluster held 7 previously diagnosed colon metastases against 8 colon flags, so one flag may come from the expression clusters (not recorded which).

## Reference

@article{bhattacharjee2001classification,
  title={Classification of human lung carcinomas by mRNA expression profiling reveals distinct adenocarcinoma subclasses},
  author={Bhattacharjee, Arindam and Richards, William G and Staunton, Jane and Li, Cheng and Monti, Stefano and Vasa, Priya and Ladd, Christine and Beheshti, Javad and Bueno, Raphael and Gillette, Michael and others},
  journal={Proceedings of the National Academy of Sciences},
  volume={98},
  number={24},
  pages={13790--13795},
  year={2001},
  publisher={The National Academy of Sciences}
}
