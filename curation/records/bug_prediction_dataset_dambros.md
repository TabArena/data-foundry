---
unique_name: bug_prediction_dataset_dambros
name: 'Bug Prediction Dataset (D''Ambros, Lanza & Robbes, MSR 2010): Eclipse JDT Core, PDE UI, Equinox, Lucene, Mylyn'
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Outdated
tags:
- AI-Filled (Verify)
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
- https://arxiv.org/abs/1910.13717
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-20 from a web search for zero-inflated regression candidates, the source pages and, where the notes say so, the downloaded data. A human must verify the suggestion, the metadata and the notes before relying on them.**

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
