---
unique_name: eclipse_bug_data_zimmermann
name: 'Eclipse Bug Data (Zimmermann, Premraj & Zeller, PROMISE 2007), release 2.0a: Eclipse 2.0, 2.1, 3.0'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
decision_markers:
- Outdated
tags:
- AI-Filled (Verify)
- Two-Regime Zeros
- Non-IID (Temporal)
original_source: Website
year: '2007'
domain: technology & internet
required_split:
- Temporal (NON-IID)
problem_type: Regression
source_links:
- https://www.st.cs.uni-saarland.de/softevo/bug-data/eclipse/
- http://web.archive.org/web/20260918052843/https://www.st.cs.uni-saarland.de/softevo/bug-data/eclipse/
- https://doi.org/10.1109/PROMISE.2007.10
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-20 from a web search for zero-inflated regression candidates, the source pages and, where the notes say so, the downloaded data. A human must verify the suggestion, the metadata and the notes before relying on them.**

Eclipse Bug Data of Zimmermann, Premraj and Zeller (Saarland University, release 2.0a of 2007-12-28): for each file
and package of Eclipse 2.0, 2.1 and 3.0, the non-trivial defects reported in the six months before (`pre`) and after
(`post`) release, plus about 200 complexity metrics and AST node counts (PROMISE 2007, Sec. 3.2). The site did not
answer on 2026-10-20 (no route to host); the CSV zips came from the Wayback Machine. Files: 6,729 / 7,888 / 10,593
rows with 85.5% / 89.2% / 85.2% zeros in `post` (max 31); packages: 377 / 434 / 661 rows, about half zero. The zeros
are observed (no fixed defect in the window). The paper frames classification and ranking for "allocation of
resources for quality assurance (such as testing)" (Sec. 3.3) and tests "the models across releases of Eclipse"
(Sec. 4.2).

Split: temporal by release. Under the 50% training floor only one split is valid (train 2.0 + 2.1, 58% of the file
rows; test 3.0); grouping by plugin (42-70 per release) is the alternative. 56-67% of a release's files exist in an
earlier one, so a random split is optimistic: untuned LightGBM on files gives AUC 0.87 for any post-release defect at
random and 0.79 across releases, with R^2 0.09 on log1p defects among defective files (train 2.0 + 2.1, test 3.0) and
-0.14 (train 2.0, test 2.1). `pre` alone reaches AUC 0.74; it is known at release and legitimate. The paper's counts
(Table 2: 6,740 / 7,900 / 6,614 files) and its pre/post Spearman of 0.907 (Table 3) predate the 2007 corrections; in
release 2.0a the Spearman is 0.33-0.39, so only 2.0a should be used. 2nd tier for the age of the code (Eclipse
2002-2004, like `defect_data`) and because the family already has `jm1`. Terms: "facts are free", but the archive's XML
and texts are copyrighted and the site does "not allow redistribution of the archive" (FAQ).

## Reference

Zimmermann T., Premraj R., Zeller A. (2007). Predicting defects for Eclipse. Third International Workshop on
Predictor Models in Software Engineering (PROMISE'07). doi:10.1109/PROMISE.2007.10. Data: Eclipse Bug Data, release
2.0a, https://www.st.cs.uni-saarland.de/softevo/bug-data/eclipse/.

Lead: web search 2026-10-20 for zero-inflated regression candidates (not in the v4 workbook).
