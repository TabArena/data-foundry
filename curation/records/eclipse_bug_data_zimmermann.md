---
unique_name: eclipse_bug_data_zimmermann
name: 'Eclipse Bug Data (Zimmermann, Premraj & Zeller, PROMISE 2007), release 2.0a: Eclipse 2.0, 2.1, 3.0'
checked_by:
- Andrej
- Lennart
data_foundry_status:
- WIP (Triage)
claimed_by: Lennart
suggestion: TBD -> Yes
priority: 3
decision_markers:
- Outdated
tags:
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
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-20 from a web search for zero-inflated regression candidates, the source pages and, where the notes say so, the downloaded data. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `TBD -> 2nd Tier`, priority 3: file-level post-release defect counts for three
Eclipse releases with about 200 code metrics, a real cross-release task, but three releases give one valid temporal
window and the code is from 2002-2004.
- Source: Zimmermann, Premraj and Zeller, "Predicting Defects for Eclipse", PROMISE 2007 (Saarland University); data
  release 2.0a (2007-12-28) at st.cs.uni-saarland.de/softevo/bug-data/eclipse/ (no answer on 2026-10-20 nor on
  2026-10-27; Wayback copy in the links). As published (Sec. 3.2): "one file for each level (files, packages) and
  release (2.0, 2.1, 3.0)", with pre- and post-release defect counts, complexity metrics and AST node counts. The earlier AI triage (2026-10-20) measured 6,729 / 7,888 / 10,593 file rows with 85.5% / 89.2% /
  85.2% zero `post` (max 31).
- Target: `post`, "The number of non-trivial defects that were reported in the first six months after release" (Sec.
  3.2); the zeros are observed.
- Use case: Sec. 3.3: "Which files/packages have defects (a classification problem)? And which are the files/packages
  with the most defects (a ranking problem)? Having reliable predictions for both supports allocation of resources
  for quality assurance (such as testing) to parts of a system that are most defect-prone." Sec. 4.2: "We tested the
  models across releases of Eclipse". At a release, QA ranks files for testing from their metrics and pre-release
  defects; fit direct with a split by release.
- Regime: temporal by release (SPLIT-6), with files recurring across releases (56-67% of a release's files exist in an
  earlier one, earlier triage; SPLIT-13). Three releases allow one window above the 50% floor (train 2.0 + 2.1, test
  3.0: 58% of the file rows), so SPLIT-14 is not met and the task ships forced grouped by file under SPLIT-8, with the
  3.0 window as the check. Earlier probe (untuned LightGBM): ROC AUC 0.79 for any post-release defect across releases
  (0.87 at random), R^2 0.09 on log1p defects among defective files (train 2.0 + 2.1, test 3.0).
- Siblings and duplicates: `bug_prediction_dataset_dambros` (classes of Eclipse 3.4 components, Mylyn and Lucene; not
  a duplicate); `jm1` (Yes, TabArena v0.1), `defect_data` and `mozilla4` (2nd Tier, `Outdated`, Lennart). External
  collections: the PROMISE workshop's repository; the Unified Bug Dataset (Ferenc et al. 2020) merges five public Java
  bug datasets, which ones was not confirmed.
- Papers and pages: the PROMISE 2007 paper (read; its Table 2 counts and the pre/post Spearman of 0.907 in Table 3
  predate the 2.0a corrections, where the earlier triage measured 0.33-0.39).
- Metric: for the count target, Spearman correlation (Sec. 3.3.2: "To measure the quality of such a ranking, we
  recommend using the Spearman correlation"); for a binary framing, precision, recall and accuracy at a 0.5 cut (Sec.
  3.3.1, 4.2), several threshold metrics, so the fallback (MET-5, MET-6). Inputs none.
- Risks for /add-dataset: use release 2.0a only; `pre` is known at release and stays (USE-6); files rather than
  packages (the unit testers act on); the forced split (SPLIT-14, SPLIT-8); the site does "not allow redistribution of
  the archive" (no criterion, EV-4).
- Priority: gap 0, use case + (the paper names the QA allocation decision and tests across releases), source + (paper
  and release page), shape + (25,210 file-releases, about 200 metrics, three releases), risk - (one valid temporal
  window, files overlapping across releases).

CC (2026-10-30, Andrej): `TBD -> Yes`, priority 3 (the AI screening had `TBD -> 2nd Tier`, priority 3; zero-inflated
screening review page).

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

**Assessment (AI, 2026-11-08):** size check for the large-datasets review: the task's table is 25,210 file-releases (6,729 / 7,888 / 10,593 for Eclipse 2.0 / 2.1 / 3.0) x 154 inputs once 44 constant and 2 copied columns leave (153 numeric and `plugin`), and 61 of the 153 are shares derived from counts kept beside them. The table is wide only at the lower edge, and `smartshark_release_defect_prediction`, accepted today, carries the same task with newer and wider data. By the factors the priority stays 3.
- As published: release 2.0a of 2007-12-28 (archived page, http://web.archive.org/web/20260918052843/https://www.st.cs.uni-saarland.de/softevo/bug-data/eclipse/; the site did not answer on 2026-11-08). File level, `promise-2_0a-files-csv.zip` (5,913,784 bytes in the Wayback copy of 2023-03-07): `eclipse-metrics-files-2.0.csv`, `-2.1.csv` and `-3.0.csv`, semicolon-separated, 6,729 / 7,888 / 10,593 rows x 202 columns (counted): `plugin`, `filename`, `pre`, `post`, 31 complexity metrics (ACD, FOUT, MLOC, NBD, NOF, NOI, NOM, NOT, NSF, NSM, PAR, TLOC, VG, most as avg, max and sum), 83 AST node counts with their `SUM`, and 83 `NORM_` columns (each count divided by `SUM`). Package level, `promise-2_0a-packages-csv.zip` (815,647 bytes): 377 / 434 / 661 rows x 211 columns. The three releases share the columns; no cell is missing. The page also lists a revised PROMISE paper (2009-12-10) that "supersedes the original, published version, being based on the revised 2.0a data", an R file of the experiments, and an XML archive with the bug and CVS references (no metrics).
- The task's table: one row per file and release, 25,210 rows (counted) with 13,975 distinct file names; `post` > 0 in 975 / 854 / 1,568 files (14.5% / 10.8% / 14.8%), max 31. The inputs as published are `pre`, `plugin` and 198 metrics (200). 44 columns are constant over all three releases (the Java 5 nodes such as EnhancedForStatement, annotations and enums, the comment nodes, AssertStatement, CompilationUnit and PackageDeclaration, with their `NORM_` columns), and 2 copy another column in every row (`AnonymousClassDeclaration` = `ACD`, `NORM_PackageDeclaration` = `NORM_CompilationUnit`). That leaves 153 numeric inputs and `plugin` (42 / 52 / 70 plugins per release): `pre`, 31 complexity metrics, 59 AST counts, `SUM` and 61 `NORM_` shares, so 92 distinct measurements plus their shares (computed on the files).
- Access: open download from the Wayback Machine, no login: 5.9 MB and 0.8 MB of CSV zips. The page's terms: "facts are free (as in freedom), and are not copyrightable", while "The XML representation of the data is copyrighted ... we currently do not allow redistribution of the archive"; cite the PROMISE 2007 paper. No named licence (a note, EV-4).
- Changes the call: two facts, neither moves the priority by the factors. First, the width: about 200 columns become 154 inputs. Second, better data for the same task is now accepted: `smartshark_release_defect_prediction` (`Yes`, Lennart, 2026-11-08) labels the files of 398 releases of 38 Apache projects for the same QA decision at a release, with 4,198 features and manually validated labels up to about 2020, where Eclipse gives three releases of 2002-2004 and one valid temporal window. The risk point is already taken (one window, files recurring across releases), so the factors give 3 again (gap 0, use case +, source +, shape +, risk -). The reasons for 2nd Tier in the earlier note (the age of the code, a family already shipped with `jm1`) now have a second, newer member in the family. `unified_bug_dataset` re-measures the Eclipse Bug Dataset with another analyser per its record, so taking both would need a PROV-6 check.
- Not checked: the revised 2009 paper's text; the Eclipse part of the Unified Bug Dataset.

CC (2026-11-08, Lennart): kept for later (`TBD -> Yes`, priority 3) in the screening review of the large candidates, round 2.

## Reference

Zimmermann T., Premraj R., Zeller A. (2007). Predicting defects for Eclipse. Third International Workshop on
Predictor Models in Software Engineering (PROMISE'07). doi:10.1109/PROMISE.2007.10. Data: Eclipse Bug Data, release
2.0a, https://www.st.cs.uni-saarland.de/softevo/bug-data/eclipse/.

Lead: web search 2026-10-20 for zero-inflated regression candidates (not in the v4 workbook).
