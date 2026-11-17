---
unique_name: lung_cancer_epithelial_genexp
name: SMK_CAN_187
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
- WIP (DF)
claimed_by: Andrej
suggestion: 'Yes'
priority: 2
decision_markers:
- Class-dependent Recording
tags:
- Non-IID (Grouped)
- Many features
- 'Samples: Over Time'
- 'Time: Inferred'
- 'Target: Varying Delay'
collections:
- FS Benchmark
original_source: GOV Website
year: '2006'
domain: medical & healthcare
required_split:
- Grouped (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.openml.org/d/45100
- https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE4115
notebook_path: datasets/beyond_iid/new_iid/lung_cancer_epithelial_genexp/lung_cancer_epithelial_genexp.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/lung_cancer_epithelial_genexp/dataset.py
source_row: 1038
type_adapter_id: curation-record-v1
---

## Comments

CC: "Dominika: gene-expression profiles from Affymetrix HG-U133A microarrays. Need to check whether it's different from the Lung dataset."

OpenML Rel: https://arxiv.org/abs/2311.12879

Use NCBI source.

Version from NCBI has more columns than on OpenML.

CC (2026-10-19, Lennart): the GEO values are RMA, normalised across the arrays processed together; kept, with a `Potential leak, kept on purpose` note in the definition: a scaling over all rows is no strong leak and often happens in reality. It is a reason for `No` only when a strong leak is suspected or the data can be rebuilt.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — Spira et al. 2007 report accuracy with sensitivity and specificity of the 80-gene predictor (83/80/84%); the clinical claim rests on sensitivity and NPV, no single metric or threshold. roc_auc is the binary fallback.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `aegis_bronchial_airway_lung_cancer` (TBD -> Yes, priority 3). Each is screened in its own record; this record's verdict stays the curator's.

**Assessment (AI, 2026-11-04):** reviewed for the BeyondArena v0.2 review page, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the folder's `REVIEW.md`. Keep after dropping the 24 QC-failed arrays (19 of them cancer, Fisher p = 0.004): the expression biomarker task is pre-diagnostic with a residual signal of 0.72 after demographics, though clinical findings predict better and an array-spread confound is unresolved. Priority 2: gap 0, use case 1, source 1, shape 0, risk -1.

CC (2026-11-12, Andrej): BeyondArena v0.2 review page, lung_cancer_epithelial_genexp: record fields set to the definition's values (mark `update`):
- `year` 2006: GEO made the series GSE4115 public on 2006-02-27, the first publication of the rows; the paper followed in 2007.
- `original_source` GOV Website: NCBI GEO, the source the definition downloads; the OpenML copy (SMK_CAN_187) is derived from it.

CC (2026-11-12, Andrej): BeyondArena v0.2 review page, lung_cancer_epithelial_genexp: the split is grouped by scan period, forced from temporal (issue 3, D).
- **Why:** the sample number in the GEO titles is the scan order (scan dates of 31 arrays from linked GEO copies, April 2003 to January 2006, Spearman 0.997). Within each class the expression tells an array's period (ROC AUC 0.90 to 0.98), and the cancer share moves from 6% to 81% between periods, so random folds let a model read a period's cancer share: held-out periods score 0.05 to 0.14 ROC AUC lower at equal training size. Windows forward in time cannot be scored with 187 arrays (three windows of 31; the oldest ranks below chance whatever trains).
- **Done in `dataset.py`:** `scan_period`, the sixth of the sample number's rank (31 or 32 arrays), is the group and no model input, and the number itself is not shipped; grouped 3-fold with 20 repeats, two periods per test fold; `data_tags` `ForcedGroupedFromTemporal` with its `Time basis:` line; `task_summary.split`, `changes` and `splits_comment` updated.
- **Record:** `required_split` Grouped (NON-IID); the tag `New IID` replaced by `Non-IID (Grouped)`.
- Sources: Spira A, Beane JE, Shah V, et al. Airway epithelial gene expression in the diagnostic evaluation of smokers with suspect lung cancer. Nature Medicine 2007;13(3):361-366, https://doi.org/10.1038/nm1556. Beane J, Sebastiani P, Whitfield TH, et al. A prediction model for lung cancer diagnosis that integrates genomic and clinical features. Cancer Prevention Research 2008;1(1):56-64, https://doi.org/10.1158/1940-6207.CAPR-08-0011. GEO series GSE4115 and GSE19027 (CEL headers), https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE4115.

CC (2026-11-13, Andrej): BeyondArena v0.2 review page, lung_cancer_epithelial_genexp: the 8 clinical findings known before the brushing join the expression (issue 2, C).
- **Why:** they are there at the bronchoscopy and none is the diagnosis. On the 163 arrays with clinical fields, under the grouped splits, logistic regression scores ROC AUC 0.819 on the clinical findings, 0.744 on the expression and 0.834 on both. The expression adds +0.015 (SE 0.006), and +0.036 on the 118 non-diagnostic bronchoscopies, which is the source's own question (Beane et al. 2008).
- **Done in `dataset.py`:** `age`, `sex`, `race`, `smoking_status`, `pack_years`, `haemoptysis`, `lymphadenopathy` and `mass_over_3cm` are parsed from GEO's sample characteristics; flags and categories are categorical. `bronch_status` (the bronchoscopy's own result) and `subjective_assessment` (the study's blinded risk rating made afterwards) stay out, with a curation note on why, and so do `biomarker_score` and `cancer_status`. `known`, `changes` and `fit_reason` are updated.
- **Open:** the 24 arrays without GEO clinical data (19 cancer) keep missing values until issue 1 is decided. `dataset check`: 0 errors, 0 warnings.
- Sources: Spira A, Beane JE, Shah V, et al. Airway epithelial gene expression in the diagnostic evaluation of smokers with suspect lung cancer. Nature Medicine 2007;13(3):361-366, https://doi.org/10.1038/nm1556. Beane J, Sebastiani P, Whitfield TH, et al. A prediction model for lung cancer diagnosis that integrates genomic and clinical features. Cancer Prevention Research 2008;1(1):56-64, https://doi.org/10.1158/1940-6207.CAPR-08-0011. GEO series GSE4115, https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE4115.

CC (2026-11-13, Andrej): BeyondArena v0.2 review page, lung_cancer_epithelial_genexp: the 24 arrays that failed the authors' quality control are dropped, 163 arrays remain (issue 1, B).
- **Why:** GEO gives no clinical data for 24 of the 187 labelled arrays, the series says "23 of these samples were then filtered for quality control reasons", and these 24 correlate worse with the median profile (0.93 against 0.98). They are 19 cancer and 5 not (79% against 48%, Fisher p = 0.004), a lab difference tied to the class; with the clinical findings in, trees read their empty fields as cancer. Kept as test-only rows they cost every model 0.05 to 0.13 ROC AUC, and a clinic never reads a failed array.
- **Done in `dataset.py`:** `_clean` drops the arrays without GEO clinical characteristics before the scan periods are cut, so the six periods are sixths of the 163 (27 or 28 arrays, 4% to 70% cancer) and the 8 clinical columns have no missing values. `row`, `predicted` (48%), `changes`, `fit_reason`, the curation notes, the grouping definition, `splits_comment` and both accepted group warnings are updated; untuned LightGBM and logistic regression beat chance on all 14 test pairs that occur. Marker `Class-dependent Recording` added (rows of mostly one class marked by a recording difference, dropped), as for gallstone_disease.
- `dataset check`: 0 errors, 0 warnings (two accepted). Not rebuilt.
- Source: GEO series GSE4115, https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE4115. Spira A, Beane JE, Shah V, et al. Airway epithelial gene expression in the diagnostic evaluation of smokers with suspect lung cancer. Nature Medicine 2007;13(3):361-366, https://doi.org/10.1038/nm1556.

## Reference

@article{spira2007airway,
  title={Airway epithelial gene expression in the diagnostic evaluation of smokers with suspect lung cancer},
  author={Spira, Avrum and Beane, Jennifer E and Shah, Vishal and Steiling, Katrina and Liu, Gang and Schembri, Frank and Gilman, Sean and Dumas, Yves-Martine and Calner, Paul and Sebastiani, Paola and others},
  journal={Nature medicine},
  volume={13},
  number={3},
  pages={361--366},
  year={2007},
  publisher={Nature Publishing Group US New York}
}
