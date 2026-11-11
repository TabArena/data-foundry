---
unique_name: lung_adenocarcinoma_metastasis
name: Lung adenocarcinoma, metastasis from another organ or primary (Bhattacharjee 2001, GEO arrays)
checked_by:
- Andrej
data_foundry_status:
- 'DF: Yes'
suggestion: 'Yes'
priority: 1
decision_markers:
- Class-dependent Recording
- Selection Bias
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

CC (2026-11-11, Andrej): new record for the metastasis task on the arrays of `lung_cancer`, whose histology target was retired on 2026-11-10 (BeyondArena v0.2 review page, lung_cancer issues 7, B, and 4, B: a new record, since rows, target and values all changed). Ship.
- **The source's own task:** "A key issue in lung tumor diagnosis is the discrimination of a primary lung adenocarcinoma from a distant metastasis to the lung" (Bhattacharjee et al. 2001, Results); "metastases of nonlung origin can be difficult to distinguish from lung adenocarcinomas" (Introduction). The paper finds them by clustering and scores no classifier.
- **Where the label comes from:** the study's annotation sheet (`SampleData.xls`, sheet DATASET B, in GEO's caArray archive) flags 16 of its 139 adenocarcinomas as "possible mets" (8 colon, 4 breast, 4 other). 15 are written in the resected tumour's own pathology note, AD218's only in the study's second reading. The call is read from the specimen's pathology but not settled there: it rests on the earlier cancer outside the specimen, and the source calls the two "difficult to distinguish". The 8 colon flags are the firmest and the easiest part. All count but AD218's (below), leaving 15.
- **Rows:** 123 adenocarcinomas: the paper's 125 with clinical data, less AD218 and AD224; the 12 `A` patients and AD355, AD360 have no clinical data, so "no flag" is no finding for them. One MAS5 array per tumour, scaled on that array alone (the GEO rebuild of lung_cancer's issue 1); the 67 control probes are dropped.
- **Size:** 5 metastases per test fold. The task probe raises no flag (shipped splits; random forest ROC AUC 0.876, ahead of the class shares on every split; logistic regression 0.836, LightGBM 0.811); ten unfitted pathology marker genes reach 0.819. Out of fold, colon metastases separate at 0.984, breast at 0.76, other at 0.83. Metric: ROC AUC, the binary fallback.
- **Recording:** corrected on 2026-11-11 by the review panel: an earlier run paired labels with the wrong arrays. The metastasis arrays call fewer probe sets present (ROC AUC 0.722) and show more 18S rRNA (0.784); the 67 control probes (0.695 together) are dropped, at no cost; the share present runs through every gene and stays, with the `Class-dependent Recording` marker (noise floor subtracted: logistic regression 0.855 to 0.857).
- **AD218 and AD224 dropped as undetermined (review issue 2, B):** AD218's only metastasis note is the study's second pathology review ("ad w met?") and it lies in the paper's colon expression cluster, so its flag may follow the clustering; AD224 has the same kind of note ("ad m met?") and is coded primary. Dropping both removes the contradiction without taking a side; on the same folds no score moves.
- **Known gaps:** the label is "possible", not a confirmed origin; the rows are all resected adenocarcinomas while the question arises only after an earlier cancer elsewhere, which is not recorded (`Selection Bias`, fit approximate). AD320 and AD368 are primaries the source suspects. No colon flag follows the clustering: the 7 inside it are the paper's "previously diagnosed".

**Assessment (AI, 2026-11-11):** review panel (full): ship after changes (applied: the 67 control probes and the two rows without clinical data dropped, the recording note corrected, `Class-dependent Recording` and `Selection Bias` added); curator: issue 1 A (restated use-case reason), issue 2 B (AD218 and AD224 dropped). Priority 1: gap 0, use case 0 (named by the source, fit approximate), source + (paper and the study's own deposit), shape 0 (123 rows), risk - (soft label, recording difference kept).

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
