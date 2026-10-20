# glioma_grading_clinical_and_mutation_features

**Outcome:** added. A binary classification of the glioma grade (TCGA lower-grade glioma against glioblastoma)
from 20 mutation flags, sex, race and age, on UCI 759's original file of 862 patients, with an IID split. The AI
recommends shipping it, with the label and the small signal beyond IDH1 and age as concerns.

**Main points:** The TCGA-era histological grade; IDH1 and age carry most of the signal.

**Record judgment:** valid with concerns. A classification task, the source's own; feature selection is only the
paper's method. The concern is the label (issue 1).

**Issues for Lennart:**

1. **The label is the TCGA-era histological grade. That fits the task, but WHO 2021 renames part of it.**
   - Question: is a histological LGG / GBM label acceptable when today's classification renames some of its tumours?
   - Evidence: `Grade` is the TCGA project. The GDC dates 858 of the diagnoses between 1989 and 2013. 128 LGG rows
     are "Mixed glioma" (oligoastrocytoma), which WHO 2021 counts among the "poorly defined entities". WHO 2016 still
     graded IDH-mutant tumours "depending on histological parameters" (Louis et al. 2021, Neuro-Oncology 23(8):1231).
     WHO 2021 reserves glioblastoma for IDH-wildtype tumours, but the 25 IDH-mutant GBM rows would become "Astrocytoma,
     IDH-mutant", still CNS WHO grade 4. So the grade stays the same, and only a "glioblastoma or not" label would
     follow from IDH. Some of the 87 IDH-wildtype LGG rows would become glioblastomas (TERT promoter, EGFR
     amplification, +7/-10), and an IDH-mutant astrocytoma with a CDKN2A/B deletion becomes grade 4. None of these
     markers is in the data. The label is not built from the features: without IDH1 and IDH2, ROC AUC is 0.888
     (logistic regression) and 0.893 (random forest), against 0.92 with all features.
   - Implemented: the source's label, with a corrected curation note.
   - Alternative: a WHO-2021 relabel. It needs copy-number and TERT data from the GDC, which makes it a new dataset.
     I do not recommend it.

2. **The 23 patients with a missing sex, age or race are kept: 862 rows.**
   - Question: keep them, or match the source's 839?
   - Evidence: the authors' file and OpenML 46604 drop them (839 rows). Missingness carries no label (indicator AUC
     0.500; 12 LGG, 11 GBM), and the GDC has no age for the 5 rows without one either.
   - Implemented: kept, with NaN.
   - Alternative: drop them to match the paper and OpenML. That is one `dropna` on the three demographic columns.

4. **IDH1 and age carry most of the signal.**
   - Question: is the remaining signal enough for a benchmark task?
   - Evidence: IDH1 alone gives 0.860 and IDH1 with age 0.902, against 0.92 for all features. Both are the natural
     core of glioma grading (rule 4 of task_probes.md), and the probes raise no `one_feature` or `no_spread` flag.
     Methods spread: random forest 0.922, logistic regression 0.919, untuned LightGBM 0.897.
   - Implemented: kept as a small tabular task.
   - Alternative: none recommended. The tuned BeyondArena results do not cover this new dataset.
