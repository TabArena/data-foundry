---
unique_name: heart_disease
name: Heart Disease
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
suggestion: 'Yes'
priority: 2
decision_markers:
- Outdated
tags:
- Tiny Data
- Non-IID (Grouped)
collections:
- New (BeyondArena)
original_source: UCI
year: '1988'
domain: medical & healthcare
required_split:
- Grouped (NON-IID)
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://archive.ics.uci.edu/dataset/45/heart-disease
- https://doi.org/10.24432/C52P4X
v2_path: datasets/_dev/tabarena-v0pt2/heart_disease/dataset.py
source_row: 113
type_adapter_id: curation-record-v1
---

## Comments

Duplicate of heart disease from PMLB above

CC (2026-10-21, Andrej): Why the three hospital datasets are merged into this one. The benchmark had three tasks from the same study, `heart_disease_cleveland`, `heart_disease_hungary` and `heart_disease_va_long_beach`; they are retired as duplicates of this dataset.
- **One study, one question:** Detrano et al. (1989) collected the same 13 findings (history, resting ECG, an exercise test and two imaging tests), coded the same way, from the patients of each hospital, and labelled them the same way: does angiography, an X-ray of the heart arteries, show more than 50% narrowing? UCI publishes the hospitals as one dataset ("Each database has the same instance format"). A file per hospital is a slice of one cohort, which the curation guidelines treat as a duplicate unless the slice adds a distinct task.
- **The slices are not distinct tasks:** the link between findings and disease holds across hospitals. A model trained on two hospitals ranks the third hospital's patients nearly as well as a model trained on that hospital itself (TabPFN 3.5, ROC AUC: Cleveland 0.888 against 0.913, Budapest 0.906 against 0.914), and in Long Beach better (0.739 against 0.708), whose own 200 patients are a smaller training set than the other hospitals' 597. Kept apart, one clinical question counted three times in the benchmark.
- **Merged, the data poses the source's own question:** the study built its model in Cleveland and tested whether it holds at the other hospitals. It found that the model ranks patients well but misjudges how common the disease is at a new hospital ("Both algorithms overpredicted the probability of disease at the Hungarian and American centers", abstract). No single-hospital dataset can pose that question; the merged one, split by hospital, does (next comment).
- **Against merging, the hospitals differ:** in how many of their patients have the disease (46%, 36%, 75%, reflecting whom each hospital sends to angiography) and in which tests they recorded (calcium on fluoroscopy and the thallium scan almost only in Cleveland; no exercise test for a quarter of the Long Beach patients). Not a reason to keep them apart: these are the differences a model meets at a new hospital, and the split by hospital makes them part of the task, not a shortcut.
- **Against merging, each hospital alone is a real task too** (a model built and used at one clinic). True, but it is the same task three times, each on 200 to 303 patients.
- **Reference:** Detrano R, Janosi A, Steinbrunn W, Pfisterer M, Schmid JJ, Sandhu S, Guppy KH, Lee S, Froelicher V. International application of a new probability algorithm for the diagnosis of coronary artery disease. Am J Cardiol. 1989;64(5):304-310. doi:10.1016/0002-9149(89)90524-9

CC (2026-10-21, Andrej): Switzerland is left out, and the split is by hospital (train on two, test on the third), replacing the random split with a hospital column first proposed on 2026-10-20.
- **Switzerland:** its UCI file keeps only 8 of the paper's 23 patients without disease (94% diseased against 84%), so its disease rate comes from the release, not the hospital; as a held-out hospital it would be scored on 8 patients without disease.
- **Split by hospital:** the source built its model in Cleveland and applied it in Budapest and Long Beach, which is the task here. A held-out hospital brings its own disease rate (36-75%, as in the paper) and test habits, and is scored on its own patients; a random split would compare patients of two hospitals in 68% of the positive-negative pairs, which no clinician does. The hospital's role in the random split looked like a selection artefact; this way it is part of the real task.
- **Referred patients only** (all were sent to angiography): not a reason to exclude, since pretest-probability models are built this way (Genders TS et al. A clinical prediction rule for the diagnosis of coronary artery disease: validation, updating, and extension. Eur Heart J. 2011;32(11):1316-1330. doi:10.1093/eurheartj/ehr014); `fit` stays `approximate`.
- **Verdict:** ship; `heart_disease_cleveland`, `heart_disease_hungary` and `heart_disease_va_long_beach` are retired as duplicates of this dataset.

CC (2026-10-21, Andrej): Why the split is by hospital. The data holds patients of three hospitals (Cleveland, Budapest, Long Beach) that differ in how many of their patients have the disease (46%, 36%, 75%) and in which tests they recorded. There are two ways to split them into training and test data:
| | Random split, hospital given as a feature | Split by hospital (chosen) |
|---|---|---|
| The test data stands for | New patients at the same three hospitals | The patients of a hospital the model has never seen |
| Matches | A model built at several hospitals and used there | The source study: a model built in Cleveland, then used in Budapest and Long Beach |
| What the score compares | Mostly patients from two different hospitals (68% of the pairs ROC AUC compares), which no doctor does | Only patients of the same hospital |
| The hospital's disease rate | Learned from that hospital's training patients | Unknown to the model, as at a new hospital (the source found its model off there too) |
| Tests recorded differently per hospital | Seen in training | A real hurdle: two tests were recorded almost only in Cleveland |
| Number of splits | 30 (10 repeats of 3 folds), stable scores | 3 (one per hospital), scores vary a lot |
| Weak point | Part of the score is knowing which hospital refers sicker patients | A hospital would usually adjust a model to its own disease rate; here the model cannot |

CC (2026-10-21, Andrej): The four `dataset check` warnings that come from having only three hospitals are accepted in `dataset.py`, each with its reason (few groups, one repeat, one hospital per test fold, Cleveland's 38% share); the check is clean.

**Assessment (AI, 2026-10-27):** review panel (full) on the merged definition: ship after changes. Applied: one Long Beach patient entered twice is dropped (raw ids 143 and 192 share the exercise and angiogram dates and all ten vessel readings; the equal Hungarian pair is two patients), 796 rows; codes labelled, target Yes/No; the use case restated as the check before a scheduled angiogram (every patient was referred; the exercise test came a median of 1, 4 and 11 days before the angiogram), the 30 exercise tests dated after the angiogram named and kept (LEAK-11); the metric reason names the 0.5 threshold, the test prices and Statlog's matrix; numbers updated. Corrections to the CC lines of 2026-10-21: the hospitals share the 13 attributes and their coding, not the same findings (`ca` and `thal` almost only in Cleveland); the TabPFN numbers were not reproduced (TabPFN is not installed here; logistic regression shows the same pattern); the abstract has the Cleveland model overpredicting by 5 points in Long Beach, where our models underpredict, so the data reproduces the paper in Budapest only, and "ranks patients well" is not in the abstract (the full text was not read). The first comment ("Duplicate of heart disease from PMLB above") is superseded: this record is the UCI original the merge builds on. UCI's raw 76-attribute files hold the same 294 Hungarian, 200 Long Beach and 123 Swiss patients as the processed files, so there is nothing to repair from (PROV-13). Open for the curator (REVIEW.md): the fit, the three-hospital split against covertype, the merge against the earlier duplicate calls, the paper's PDF. Priority 2: gap -, use case - (fit approximate, open), source +, shape - (796 patients), risk none.

CC (2026-10-27, Lennart): review of PR #20, marks on REVIEW.md. Fit `approximate` kept (issue 1): the referral for angiography is the setting of the restated use case, the check before a scheduled angiogram, and no longer the gap named in the CC of 2026-10-21; the gap is Cleveland's testing by study protocol and two inputs no longer used (the thallium-201 scan and calcium on fluoroscopy, replaced by CT). Split by hospital kept over the few-groups factor, unlike covertype (issue 2). The merge confirmed, against the earlier duplicate calls (issue 3). No amendment for `unstable` on grouped tasks for now (issue 5). Metric `roc_auc` (fallback) as declared. Shared the paper (issue 4).

**Assessment (AI, 2026-10-27):** Detrano et al. 1989, full text (Am J Cardiol 64:304-310) read. The model used the 13 variables of the UCI files, fitted as 352 logistic regressions, one per clinically relevant set of available tests (p. 305). In Cleveland the exercise test, thallium scan and fluoroscopy were a research protocol, read after the angiogram and without knowledge of it (p. 305); at the other hospitals the test results reached the physician (work-up bias), every test came within 6 weeks before the angiogram, and the thallium scan was done for a minority (41 patients in Long Beach, 33 in Budapest, Table II) with no fluoroscopy listed (p. 306), so the missing `ca` and `thal` there are the hospitals' practice, not the release. The 30 exercise tests dated after the angiogram in the raw files are then likely date errors; kept. Reliability is the mean predicted probability against the disease rate, overall and by quintiles (p. 306); accuracy was scored over the thresholds 0.2 to 0.8 (p. 307); neither "ranks patients well" nor a ROC analysis is in the paper. The paper's Table I gives the Swiss patients 81% diseased (85 in Basel at 85%, 58 in Zurich at 74%), about 27 without disease, not the 23 of the 84% in the abstract that the CC lines of 2026-10-21 use. The Hungarian 425 were all catheterizations of 1983 to 1987 without prior infarction or valve disease (p. 306); how UCI's 294 were chosen is not stated. Notes, metric reason and use case now cite the pages. Priority 2: gap -, use case - (fit approximate), source +, shape - (796 patients), risk none.

CC (2026-10-27, Lennart): verdict ship, nothing open after the review of PR #20. To be built on the curator's ask.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): 1 ordinal scales typed as ordered categories in the codebook's order (CLEAN-14, amended): `slope` (the README lists their levels); left unordered: `cp` (asymptomatic is half the rows and the most diseased; the order is contested).

## Reference

@article{detrano1989international,
  title={International application of a new probability algorithm for the diagnosis of coronary artery disease},
  author={Detrano, Robert and Janosi, Andras and Steinbrunn, Walter and Pfisterer, Matthias and Schmid, Johann-Jakob and Sandhu, Sarbjit and Guppy, Kern H and Lee, Stella and Froelicher, Victor},
  journal={The American journal of cardiology},
  volume={64},
  number={5},
  pages={304--310},
  year={1989},
  publisher={Elsevier}
}
