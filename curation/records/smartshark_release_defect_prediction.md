---
unique_name: smartshark_release_defect_prediction
name: SmartSHARK release-level defect prediction data (Herbold, Trautsch, Trautsch, Ledel 2022), IND-JLMIV+R labels
checked_by:
- Lennart
data_foundry_status:
- WIP (Triage)
claimed_by: Lennart
suggestion: 'Yes'
priority: 3
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
- Many features
original_source: Other
year: '2021'
domain: technology & internet
required_split:
- Grouped (NON-IID)
problem_type: Binary Classification
source_links:
- https://doi.org/10.5281/zenodo.5675024
- https://doi.org/10.1007/s10664-021-10092-4
- https://doi.org/10.5281/zenodo.4071448
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: file-level defect labels for 398 releases of 38 Apache Java projects, from manually validated bug issues (IND-JLMIV+R), with 4,198 static, process and warning features; a documented, recent form of the defect task `jm1` ships, with label timing and recurring files to handle.
- Source: Herbold, Trautsch, Trautsch and Ledel (TU Clausthal, University of Goettingen), "Problems with SZZ and Features: An empirical study of the state of practice of defect prediction data collection", Empirical Software Engineering, 2022 (doi 10.1007/s10664-021-10092-4; preprint arXiv 1911.08938, read); replication kit on Zenodo (doi 10.5281/zenodo.5675024, v1 2021-11-11, "All materials are licensed under the Apache 2.0 License"): `release-level-data.tar.gz` (616 MB, "labeled with IND-JLMIV+R for the 398 releases") and `DO_NOT_USE_release-level-data.tar.gz` (6M-SZZ labels, which "should not be re-used"). Built from SmartSHARK MongoDB Release 1.0 (doi 10.5281/zenodo.4071448, 2020, 36.2 GB, CC BY 4.0): issue, mailing-list and version-control data of 38 Java Apache projects with manually validated issue types and links. As published (Sec. 5.1): static code metrics, clone metrics, PMD warnings, AST node counts, change and refactoring counts "from the last six months", churn metrics and aggregations; "The data set contains a total of 4198 features"; per file the number of bugs fixed, and a file-by-issue matrix whose column names hold the issue id, its severity and "the date of the last bug fixing commit". Releases per project in Table 4 (for example commons-lang 1.0 to 3.7); release dates, rows per release and the file layout not read (archive not opened).
- Use case: before a release, a project team decides where to spend quality assurance; the paper scores models by Herbold's (2019) cost model, built on "the ratio C between the costs for quality assurance and the cost of defects" (Sec. 5.2); fit direct for release-level QA planning. Regime: the source trains on the other projects and tests on one release (Sec. 5.9: releases with at least 100 files and five defective files, 203 releases), so grouped by project; a temporal split by release within a project is the other reading (USE-10: a known project has history), and the curator picks one.
- Siblings and duplicates: `jm1` (`Yes`, shipped; NASA MDP modules, 2004), `defect_data` (`TBD -> 2nd Tier`, Outdated; the curator: "take one or two representative cases"), `kc2`, `mc1`, `pc1`, `pc3` (`No`, Duplicate), `mozilla4` (`TBD -> 2nd Tier`), `apachejit` (AI `TBD -> Yes`, priority 2: commit-level labels of 14 Apache projects), `unified_bug_dataset` (unscreened: class and file level, five older sets merged). The same family from other sources and units: no duplicate (PROV-4, PROV-7); the curator may want one release-level and one commit-level set. External collections: none found; the curator's Zotero items 93 and 94.
- Better data: found as better data for `defect_data` and `jm1`, and from the curator's Zotero collection (item 93); no further search this round.
- Papers and pages: the EMSE paper; Herbold, Trautsch and Grabowski, "A Comparative Study to Benchmark Cross-Project Defect Prediction Approaches", IEEE TSE (doi 10.1109/TSE.2017.2724538), the Zotero item, whose cross-project procedure the paper reuses on other data: related work, moved here from the links (PROV-12); Trautsch et al. on the SmartSHARK platform.
- Metric: the source evaluates cost bounds (a lower and an upper bound on the cost ratio C, Sec. 5.2, eq. 3) that need lines of code as effort and the file-by-issue matrix, with no single score; it sets recall, precision and F-measure aside and does not adopt MCC. No threshold or cost is fixed (MET-6, MET-7), so the fallback `roc_auc` (MET-8); inputs none.
- Risks for /add-dataset: label maturity: a bug fixed after a training cut must not label a training row (the issue dates ship; SPLIT-9, SPLIT-10, LEAK-24); the same file recurs in every release of a project (SPLIT-29); 4,198 features, many of them aggregations (width is no reason to drop, CLEAN-22); the bug count and the issue matrix define the target and are never features (SEL-5); the 6M-SZZ archive stays unused, as the authors ask.
- Priority: gap 0 (technology & internet has 4 accepted datasets; binary and grouped not thin), use case + (the source names the QA decision and its cost), source + (a peer-reviewed paper with a replication kit), shape + (398 releases, project groups, many features), risk - (label maturity, files recurring across releases).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `defect_data`, `jm1`; the curator's Zotero collection, item 93: "A Comparative Study to Benchmark Cross-Project Defect Prediction Approaches".
- as published: Java source files per release: 398 releases of 38 Apache projects (about 2003-2020), static code, process and warning metrics; release-level-data.tar.gz 616 MB; row and column counts not on the page; target: file is defective in the release, from bug issues validated by issue type and link (IND-JLMIV+R); the 6M-SZZ variant is marked DO_NOT_USE by the authors; access: open.
- Why: Same task as defect_data and jm1 (defect-prone module prediction from code metrics) by the authors of the Zotero CPDP benchmark, with validated labels and the authors' explicit release for re-use
- Adds: Newer (to about 2020 instead of 2004), far larger, curated labels instead of unknown labelling (MDP), project and release structure for a grouped or temporal split

CC (2026-11-08, Lennart): accepted for adding (`Yes`) in the screening review of the large candidates (most rows, most features).
