---
unique_name: unified_bug_dataset
name: Unified Bug Dataset (A Public Unified Bug Dataset for Java and its Assessment Regarding Metrics and Bug Prediction)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
tags:
- AI-Filled (Verify)
original_source: Other
year: '2020'
domain: technology & internet
problem_type: Binary Classification
source_links:
- https://doi.org/10.5281/zenodo.3693686
- https://doi.org/10.1007/s11219-020-09515-0 (Software Quality Journal 2020; paper not opened)
- https://doi.org/10.1007/s11219-020-09515-0
- https://doi.org/10.1145/3273934.3273936
- https://arxiv.org/abs/2504.17977
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: five public Java bug datasets re-measured with one static analyser, 47,618 classes (43,744 files) with a bug count; a documented, larger form of the static-metric defect task, which the curator called dated and warned against taking as a merged set.
- Source: University of Szeged (Ferenc, Tóth, Ladányi, Siket, Gyimóthy), "A public unified bug dataset for Java and its assessment regarding metrics and bug prediction", Software Quality Journal 2020 (doi 10.1007/s11219-020-09515-0, open access); data on Zenodo (doi 10.5281/zenodo.3693686, v1.2, 2020-03-02, CC BY 4.0, `UnifiedBugDataset-1.2.zip`, 1.0 GB). Zenodo: "We considered 5 public datasets and we downloaded the corresponding source code for each system in the datasets and performed source code analysis to obtain a common set of source code metrics"; "we merged all classes (and files) into one large dataset which consists of 47,618 elements (43,744 for files)". The five sources (the run's Assessment, not checked against the paper): PROMISE (the Jureczko-Madeyski Java projects, not the NASA MDP sets), the Eclipse Bug Dataset, the Bug Prediction Dataset, Bugcatchers and the GitHub Bug Dataset. Target: the number of bugs of a class or file (buggy when above zero).
- Use case: before a release, a QA lead picks the classes to review or test first from their static metrics; the source names bug prediction research and no actor; fit approximate (bugs were collected differently in each source dataset); regime grouped by system or temporal by release, to settle.
- Siblings and duplicates: `jm1` (`Yes`, NASA module metrics), `defect_data` (`TBD -> 2nd Tier`; the curator: "take one or two representative cases", "The task type is outdated", merged sets "not recommended from a task POV"), `kc2`, `mc1`, `pc1`, `piechart3`, `pizzacutter3` (`No`), `mozilla4` (`TBD -> 2nd Tier`), `apachejit` (`TBD -> Yes`, priority 2, commit level). Not a duplicate of the NASA sets (other systems, Java); its PROMISE part re-measures Java projects that other records may hold (PROV-6, to check). External collections: none found; the curator's Zotero item 94 (a survey of defect datasets) lists it.
- Better data: found as better data for `defect_data`, `jm1`, `piechart3`, `pizzacutter3` (the run's Assessment; Zotero item 94); no further search this round.
- Papers and pages: the SQJ paper (53 citations; not read: Springer's page redirected to a login); the Zenodo record; arXiv 2504.17977 (the survey).
- Metric: none found (the Zenodo text names a decision tree and no metric; the paper not read), so the fallback `roc_auc` (MET-1, MET-8).
- Risks for /add-dataset: the five sources counted bugs in different ways (release windows, issue links), so the label means something different per source: take one source or one large system, or group the split by source and system (LEAK-13, `Class-dependent Recording` to check); several releases of one system repeat the same classes (near duplicates across a random split); class level and file level are two views of the same code (ship one); duplicate metric vectors with both labels, as found in `jm1`'s audit; the curator's concern that the task is dated stands.
- Not checked: the paper's text (the per-source counts, the bug definitions, its metric); the zip's layout (1.0 GB, not opened).
- Priority: gap 0 (technology & internet has 4 accepted, binary not thin), use case 0 (no actor named), source + (peer-reviewed paper, Zenodo, institution), shape + (47,618 classes, systems and releases), risk - (a merge of sources with different labels).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `defect_data`, `jm1`, `piechart3`, `pizzacutter3`; the curator's Zotero collection, item 94: "From Bugs to Benchmarks: A Comprehensive Survey of Software Defect Datasets".
- as published: 47,618 Java classes (class level) and 43,744 files (file level), merged from 5 public bug datasets (PROMISE, Eclipse Bug Dataset, Bug Prediction Dataset, Bugcatchers, GitHub Bug Dataset) with one ...; target: bug count of a class or file (buggy or not); access: open, open (CC BY 4.0).
- Why: Same task as defect_data (defect-prone module prediction from static code metrics), with the metrics computed one way across all systems | Same task as jm1: static code metrics of a code unit (size, complexity, coupling) predict whether defects are reported in it; the features are of the same kind, computed by one ...
- Adds: About 5x the rows of the largest NASA set (jm1, ~10.9k modules), newer open-source Java systems instead of 2004 NASA C/C++ modules, documented metric definitions (the NASA sets' origins and cleaning are the record's complaint). The curator's note warns against merged sets: take one large system or one source dataset, ...
