---
unique_name: bug_prediction_dataset_dambros
name: 'Bug Prediction Dataset (D''Ambros, Lanza & Robbes, MSR 2010): Eclipse JDT Core, PDE UI, Equinox, Lucene, Mylyn'
checked_by:
- Andrej
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- Outdated
tags:
- Two-Regime Zeros
original_source: Website
year: '2010'
domain: technology & internet
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://bug.inf.usi.ch/
- https://bug.inf.usi.ch/download.php
- https://doi.org/10.1109/MSR.2010.5463279
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-20 from a web search for zero-inflated regression candidates, the source pages and, where the notes say so, the downloaded data. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `TBD -> 2nd Tier`, priority 2: a documented class-level benchmark of post-release
defect counts in five Java systems, but each system has one labelled release, so the honest release-to-release split
cannot be built.
- Source: D'Ambros, Lanza and Robbes, "An extensive comparison of bug prediction approaches", MSR 2010 (University
  of Lugano), data at bug.inf.usi.ch; extended in Empirical Software Engineering 17 (2012). As published (Fig. 1):
  Eclipse JDT Core 3.4 (997 classes), PDE UI 3.4.1 (1,562), Equinox 3.4 (439), Mylyn 3.1 (2,196), Lucene 2.4.0
  (691); per class 17 CK and object-oriented metrics, 15 change metrics, earlier-defect counts, metric churn and
  entropy over biweekly versions, and post-release defect counts by severity and priority. The earlier AI triage
  (2026-10-20) measured 5,371 classes in the CSVs (fewer than Fig. 1), 84.1% without a post-release defect, max 28.
- Target: Sec. III: "Given a release x of a software system s, released at date d, the task is to predict, for each
  class of x, the number of post release defects, i.e., the number of defects reported from d to six months later."
  The zeros are observed (no linked defect report in the window).
- Use case: Sec. III: "We predict the number of bugs in each class ... as this better fits the resource allocation
  scenario, where we want an ordered list of classes"; Sec. VII: it "helps project managers to optimize the available
  resources by focusing on the problematic system parts". At a release, managers rank classes for review and testing.
  Fit approximate: a deployed model is trained on earlier releases, which carry no labels here, and the paper's "50
  random 90%-10% splits of the data" (Sec. III-B) train on labels of the same release that exist only six months
  after the prediction point.
- Regime: temporal by nature with one labelled release per system, so it ships forced under SPLIT-8: grouped by
  system (5 groups, a cross-project test; earlier probe, untuned LightGBM, leave-one-system-out ROC AUC 0.66-0.73 for
  any defect) or IID within releases (pooled random ROC AUC 0.84, R^2 0.06 on log1p defects among defective classes).
- Siblings and duplicates: `eclipse_bug_data_zimmermann` (Eclipse 2.0-3.0 files over three releases, the same task
  with a release split; other releases and unit, not a duplicate); `jm1` (Yes, TabArena v0.1: NASA module defects,
  binary, IID); `defect_data` and `mozilla4` (2nd Tier, `Outdated`, Lennart on defect_data: "The task type is
  outdated and might be solved very differently nowadays", "take one or two representative cases but not all of
  them"); `kc2`, `mc1`, `pc1` to `pc3` (`Duplicate`). External collections: the Unified Bug Dataset (Ferenc et al.
  2020, Zenodo 3693686) merges five public Java bug datasets; whether this is one of them was not confirmed.
- Papers and pages: the MSR 2010 paper (read) and the dataset site; Rodriguez et al. (arXiv 1910.13717) fit
  zero-inflated Poisson models to Equinox (per the earlier triage).
- Metric: Spearman correlation between predicted and actual defect counts on the test classes (Sec. III-B, chosen
  "as it is recommended with skewed data (which is the case here, as most classes have no bugs)"), the paper's one
  argued measure of predictive power next to the adjusted R^2 it reports for explanation (MET-5); inputs none.
- Risks for /add-dataset: drop `nonTrivialBugs`, `majorBugs`, `criticalBugs` and `highPriorityBugs` (parts of the
  target, LEAK-10); the forced split with 5 systems (SPLIT-8, TP-5); five per-system tables to stack; the siblings'
  `Outdated` call (code of 2005-2009).
- Priority: gap 0, use case 0 (actor named, fit approximate), source + (paper and site document the data), shape +
  (5,371 classes, 37 metrics, five systems), risk - (no release-to-release split; target parts among the columns).

CC (2026-10-30, Andrej): `TBD -> 2nd Tier`, priority 2, as screened (verified on the zero-inflated screening review
page).

Class-level benchmark of D'Ambros, Lanza and Robbes (MSR 2010): one release each of Eclipse JDT Core 3.4, PDE UI
3.4.1, Equinox 3.4, Mylyn 3.1 and Lucene 2.4.0 (Fig. 1), with 17 CK and object-oriented metrics, 15 change metrics,
5 counts of earlier defects and the target, "the number of defects reported from d to six months later" (Sec. III).
Downloaded the per-system CSVs from bug.inf.usi.ch: 5,371 classes (324 to 1,862 per system, fewer than Fig. 1
lists), 84.1% without a post-release defect (Equinox 60.2% to Lucene 90.7%), 853 with one or more, max 28. The zeros
are observed (no linked defect report in the window). Rodriguez et al. (arXiv 1910.13717) fit zero-inflated Poisson
models to Equinox and compare them by AIC (abstract), with no held-out test.

Each system has one labelled release, so the realistic setup, a model trained on an earlier release, cannot be
built. The paper uses "50 random 90%-10% splits of the data" within a release (Sec. III-B), which trains on labels
that exist only six months after that release; across systems there are 5 groups, a domain-shift test. Untuned
LightGBM, after dropping `nonTrivialBugs`, `majorBugs`, `criticalBugs` and `highPriorityBugs` (parts of the target):
pooled random 5-fold AUC 0.84 for any defect, R^2 0.06 on log1p defects among defective classes; leave-one-system-out
AUC 0.66-0.73. `eclipse_bug_data_zimmermann` has the same task with three releases and almost five times the rows,
so a defect-count task for the family should come from there. Outdated like `defect_data`. The site states no
licence and asks for the MSR 2010 citation.

## Reference

D'Ambros M., Lanza M., Robbes R. (2010). An extensive comparison of bug prediction approaches. Proceedings of MSR
2010 (7th IEEE Working Conference on Mining Software Repositories), pp. 31-41. doi:10.1109/MSR.2010.5463279. Extended
version: D'Ambros M., Lanza M., Robbes R. (2012). Evaluating defect prediction approaches: a benchmark and an extensive
comparison. Empirical Software Engineering 17:531-577. doi:10.1007/s10664-011-9173-9.

Lead: web search 2026-10-20 for zero-inflated regression candidates (not in the v4 workbook).
