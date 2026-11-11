---
unique_name: lung_cancer
name: Lung
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
decision_markers:
- Class-dependent Recording
tags:
- New IID
- Many features
- Tiny Data
collections:
- FS Benchmark
original_source: Other
year: '2001'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- 'https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE83227 (origin: the study''s deposit of all 254 arrays, per-array MAS5 files; used since 2026-11-10)'
- 'https://www.pnas.org/doi/10.1073/pnas.191502998#supplementary-materials (data set A of the paper''s supplement, dataseta_12600gene.xls: per-patient means of MAS4 values)'
- https://www.openml.org/d/45093 (later copy of data set A)
- 'https://ftp.ncbi.nlm.nih.gov/geo/series/GSE83nnn/GSE83227/suppl/GSE83227_caArray_meyer-00191.tar.gz (the study''s annotation sheet SampleData.xls, sheet DATASET B: the metastasis flags, the target since 2026-11-11)'
notebook_path: datasets/beyond_iid/new_iid/lung_cancer/lung_cancer.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/lung_cancer/dataset.py
source_row: 1033
type_adapter_id: curation-record-v1
---

## Comments

CC: "No raw data available, using OpenML (shapes match). Original 6 classes were merged into 5 (adenocarcinomas). "

From the paper:
"We built a supervised classifier by first defining subclasses based on hierarchical and probabilistic clustering and chose marker genes by using ''K-Nearest Neighbor'' classifiers based on the signal-to-noise statistic"

The label for the task on OpenML is unclear, I cannot find the source. The paper talks about clusters they computed in an unsupervised way on the original data. In other words, we don't have a real predictive task with a real target. This was mostly done for scientific discovery. Comparing models on this data does not make a lot of sense and does not hold valuable information or a valuable new task.

Fun fact, the data contains survival prediction data, as well as it seems.

The way we can make this a real task is to use the info from the original investigation about the type of lung cancer:
"The 203 specimens (Dataset A) include histologically defined lung adenocarcinomas (n = 127), squamous cell lung carcinomas (n = 21), pulmonary carcinoids (n = 20), SCLC (n = 6) cases, and normal lung (n = 17) specimens. Other adenocarcinomas (n = 12) were suspected to be extrapulmonary metastases based on clinical history"

Thus, we use the data not for clustering as in the original work, but re-use for classification of the original data (simulating as if we were to predict this for new patients).
From the use case, it is unclear if this would really be done, as it is likely not trivial to get the features for an unharmed patient.

**Assessment (AI, 2026-10-14):** the data first appeared as data set A in the supplement of Bhattacharjee et al. (PNAS 2001), which the v2 definition downloads; OpenML 45093 is a later copy. `original_source` is now Other, as in the definition.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback log_loss — The source paper clusters the samples (hierarchical and probabilistic clustering) to find adenocarcinoma subclasses and declares no classification metric for predicting the class.

**Assessment (AI, 2026-10-27):** The open questions for the curator are in the folder's `REVIEW.md` (review of the Tiny Data datasets, written from the earlier findings, no review panel); the AI recommends shipping it after changes. Priority 2: gap +, use case - (our use case), source + (PNAS supplement), shape -, risk - (class-dependent recording, open fixes).
**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `tcga_lung_histology` (TBD -> Yes, priority 2). Each is screened in its own record; this record's verdict stays the curator's.

**Assessment (AI, 2026-11-04):** reviewed for the BeyondArena v0.2 review page, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the folder's `REVIEW.md`. Ship after dropping the 67 control probes: the class-dependent recording (47 averaged adenocarcinoma rows, spike-ins that track each array's scale) moves no score, and the label is a valid expert annotation near its ceiling. Priority 2: gap 1, use case 0, source 1, shape 0, risk -1.

**Assessment (AI, 2026-11-05):** marker `Class-dependent Recording`: 47 of the 139 adenocarcinoma rows are means of 2 to 4 arrays (repeated measurements of one sample), none of the other 58 rows, and the non-human spike-in control probes (added to every array for quality control) alone separate the classes (ROC AUC 0.85). Kept, since neither carries the score: rounding every value to the shared 0.01 grid, dropping the averaged rows or dropping all 67 control probes moves logistic regression's log loss by at most 0.005 (0.141 as shipped). Noted in the definition's curation comments; data unchanged.

CC (2026-11-06, Andrej): time basis `Timeless` accepted on the BeyondArena v0.2 review page (issue 3, A, through the cross-dataset item on routine `Timeless` issues): the label is the histology of an excised specimen, which does not change, profiled for one study. The `Time basis:` line is in the definition's notes, ending with what the split cannot test; the tag enters `data_tags` once PR #50 is in the working copy.

CC (2026-11-10, Andrej): rebuilt from the study's arrays in GEO GSE83227 instead of the PNAS Dataset A (BeyondArena v0.2 review page, issue 1, D). Under this record pending issue 4.
- **Changes made** (the input data changed):
  1. **Problem:** Dataset A averages all arrays of each adenocarcinoma patient (47 rows, that class only) and its non-human spike-in control probes separate the classes (one-vs-rest ROC AUC 0.85). **Change:** one array per specimen, the first piece and first hybridisation, with that array's own MAS5 signal; the spike-ins then reach 0.57 and the scan date 0.58.
  2. **Problem:** patient 268 gave an adenocarcinoma and a normal lung specimen. **Change:** split grouped by patient (196 patients, 197 specimens).
  3. **Problem:** the PNAS supplement downloads only through a browser. **Change:** source is GEO (automatic download); `required_split` Grouped, `source_links` reordered, `checked_by` adds Andrej.
- **Problems found, not changed:**
  - The 26 human control probes (GAPDH, actin) still separate the classes (0.94): tissue genes, kept.
  - GEO's age, sex, stage and pack-years exist only for adenocarcinomas, so they would give the class away: not added.
  - Dataset B of the supplement (a binary subset of A) is not used.
  - The task is easy (log loss 0.126, accuracy 0.95): open as issue 5 of the folder's `REVIEW.md`.

**Assessment (AI, 2026-11-10):** evidence for the rebuild (logistic regression, 20 repeats of 3 folds; `~/claude_jobs/lung_raw/`): the GEO arrays give the same 197 specimens (139 / 21 / 20 / 17); the 12 adenocarcinoma titles starting `A` are the adenocarcinomas without clinical annotation, and the study's annotation sheet (caArray archive in GEO) flags 16 possible metastases; log loss 0.123 at random, 0.126 grouped by patient, 0.141 on Dataset A; 10 pathology marker genes alone reach accuracy 0.93.

CC (2026-11-10, Andrej): retired (`No (Retired)`, `No Good Target / Scientific Discovery`; BeyondArena v0.2 review page, issue 6, B): no decision rests on the prediction for these specimens. The label is the histology pathologists read on resected tumours, where the slide is clear; the use case ("a check on the microscope reading") was ours, and a pathologist in doubt orders a two-stain panel, not an expression array.
- **The source never predicts the histology:** Bhattacharjee et al. (2001) build "a molecular taxonomy of lung carcinoma": hierarchical and probabilistic clustering finds adenocarcinoma subclasses, and their supervised classifier (k-nearest neighbours on signal-to-noise marker genes) predicts those clusters ("by first defining subclasses based on hierarchical and probabilistic clustering"). Their survival result is a retrospective association of one subclass with outcome. The only diagnostic claim of the abstract is "to discriminate primary lung adenocarcinomas from metastases of extra-pulmonary origin", and the clinical value is left general ("could aid in diagnosis"). Predicting histology was our own reuse (CC of the first screening: "This was mostly done for scientific discovery"); the source's one diagnostic task is the metastasis target below (16 possible metastases among 127 annotated adenocarcinomas).
- **Why not kept for the task's general value:** telling lung tumour types apart from molecular data matters on small biopsies and cytology that come back "non-small cell carcinoma, not otherwise specified", and for tumours of unknown origin; those cases are not in this data, so the test labels come from the easy cases only (log loss 0.126, one-vs-rest ROC AUC 0.996 on the GEO rebuild).
- **Other targets checked** from the study's annotation sheet (GEO's caArray archive, `SampleData.xls`): metastasis from another organ vs primary, ROC AUC 0.861 but 16 cases, about 5 per test fold (too few to rank methods); death within 24/36/60 months after resection, expression 0.58/0.55/0.51 against 0.49-0.52 on shuffled labels, while stage and age reach 0.63/0.71/0.80 (not a gene-expression task); lymph-node involvement 0.60 (staged at surgery anyway).
- **Not a rule change:** an expert annotation stays a valid target; the dataset fails the use case (no actor, moment or decision for these rows), as glioma_grading_clinical_and_mutation_features did. A dataset of ambiguous small biopsies labelled by the later resection would be a real task.
- Folder removed and `v2_path` cleared; the GEO rebuild of issue 1 is the commit before this retirement. Issues 4 and 5 of the review are closed with this decision.

CC (2026-11-11, Andrej): retirement reversed and the dataset re-targeted to metastasis against primary lung adenocarcinoma (BeyondArena v0.2 review page, issue 7, B): the task the source names, on the arrays rebuilt from GEO on 2026-11-10.
- **The source's own task:** "A key issue in lung tumor diagnosis is the discrimination of a primary lung adenocarcinoma from a distant metastasis to the lung" (Bhattacharjee et al. 2001, Results); the histology stays retired, since the slide settles it on resected tumours.
- **The label comes from outside the arrays:** the study's annotation sheet (`SampleData.xls`, sheet DATASET B, in GEO's caArray archive) flags 16 of 139 adenocarcinomas as possible metastases (8 colon, 4 breast, 4 other) from the clinical history and pathology report, a work-up separate from the profile.
- **Not too small:** the 2026-11-10 bullet "too few to rank methods" was the AI's judgment, not a rule. On 127 rows with 5 or 6 metastases per test fold, the task probe raises no flag (random forest ROC AUC 0.887, ahead of the class shares on 30 of 30 splits; SVM 0.885, TabPFN 3.5 0.882, logistic regression 0.850, k-nearest neighbours 0.779), and the unfitted marker genes a pathologist stains for reach 0.819.
- **Changes made:** target `Metastasis` (binary) from the sheet; rows the 127 adenocarcinomas with a clinical history (the 12 `A` patients have none); one array per tumour as before; metric ROC AUC (fallback; log loss rewards overconfidence on 5 positives per fold); random split, one tumour per patient; `problem_type` Binary, `required_split` Random (IID), `v2_path` restored, the caArray archive added to `source_links`.
- **Open:** which flagged rows count as metastases (soft "c/w" and "?" calls; one flag whose pathology note reads only "ad 5.0 m BAC"; the paper's colon cluster held 7 previously diagnosed metastases against 8 colon flags): `REVIEW.md`, issue 8.


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
