---
unique_name: apachejit
name: 'ApacheJIT: A Large Dataset for Just-In-Time Defect Prediction'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
original_source: Other
year: '2022'
domain: technology & internet
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.5281/zenodo.5907847
- https://arxiv.org/abs/2203.00101
- https://github.com/harsh8398/apachejit
- https://conf.researchr.org/details/msr-2022/msr-2022-data-showcase/1/ApacheJIT-A-Large-Dataset-for-Just-In-Time-Defect-Prediction
- https://doi.org/10.1145/3524842.3527996
- https://arxiv.org/abs/2504.17977
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: 106,674 Java commits of 14 Apache projects (2003-2019) labelled bug-inducing or clean by a filtered SZZ, with 13 change metrics and a date; the commit-level form of the defect task, with label noise and classes built by different filters.
- Source: Keshavarz and Nagappan (University of Waterloo), "ApacheJIT: A Large Dataset for Just-In-Time Defect Prediction", MSR 2022 Data Showcase (doi 10.1145/3524842.3527996; arXiv 2203.00101); data on Zenodo (doi 10.5281/zenodo.5907847, v2, 2022-01-26, CC BY 4.0): a replication zip with four CSVs, `apachejit_total.csv`, a balanced training set for 2003-2016, and a large and a small unbalanced test set of the last three years. As published: "106,674 commits (28,239 bug-inducing and 78,435 clean)"; columns (Sec. 3) "change date, # of lines added, # lines deleted, # files touched, # directories touched, # of subsystems touched, change entropy, # of distinct developers touched files, the average time from last change, # of unique changes in files, change author experience, change author recent experience, change author subsystem experience" (the metrics of Kamei et al. 2013); target `buggy`. One table.
- Use case: at commit or review time, a team flags a risky change for more review or testing (just-in-time quality assurance); ApacheJIT says only that JIT models estimate whether a change is likely to introduce a bug and names no actor, fit approximate; regime temporal: the authors train on 2003-2016 and test on the last three years (README), with the project as a possible group.
- Siblings and duplicates: `defect_data` (`TBD -> 2nd Tier`), `jm1` (`Yes`), `kc2`, `mc1`, `pc1` (`No`): NASA module-level static metrics; `mozilla4` (`TBD -> 2nd Tier`); `smartshark_release_defect_prediction` and `unified_bug_dataset` (unscreened, file and class level); `travistorrent_ci_build_outcome` (unscreened, build outcome). Another unit and prediction point, so no duplicate (PROV-7). External collections: none found; the curator's Zotero item 94 (a survey of defect datasets).
- Better data: found as better data for `mozilla4`, and as a related task for `defect_data` and `jm1`; no further search this round.
- Papers and pages: the MSR paper; McIntosh and Kamei 2018 (the labelling it follows); GitHub harsh8398/apachejit.
- Metric: none found (the paper builds the data and fits no model; the README and the Zenodo page name no metric), so the fallback `roc_auc` (MET-8); inputs none.
- Risks for /add-dataset: the classes were built by different steps (Sec. 4.3-4.4): bug-inducing commits passed filters on issue date, fix count, bug count and an AST check that drops trivial changes, while clean commits are all other Java commits between 2003-09-11 and 2019-12-26 with only the size and language filters, so commits dropped from the bug-inducing side can return as clean; check whether size, date or a trivial-change signal tells the class (LEAK-13 to LEAK-15, `Class-dependent Recording`). The bug-inducing share runs from 14% (Camel) to 61% (Hive) by project (Table 2). Bugs come only from issues reported 2010-2019, so commits before 2010 and late in 2019 are under-labelled (LEAK-24, SPLIT-9, SPLIT-10). SZZ label noise, traded toward false negatives (Sec. 4.2).
- Priority: gap 0 (technology & internet has 4 accepted datasets, not thin), use case 0 (no actor in the source), source + (a peer-reviewed data paper with its method and code), shape + (106,674 dated commits), risk - (class-dependent construction, immature labels).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `defect_data`, `jm1`, `mozilla4`; a related task next to `defect_data`, `jm1`; the curator's Zotero collection, item 94: "From Bugs to Benchmarks: A Comprehensive Survey of Software Defect Datasets".
- as published: 106,674 commits (28,239 bug-inducing, 78,435 clean) from Apache projects, 2003-2019; apachejit_total.csv with commit metrics; the authors' split trains on 2003-2016 and tests on the last 3 years; CC ...; target: buggy: whether the commit introduced a bug (SZZ on linked bug-fix commits); access: open, open (CC BY 4.0).
- Why: Answers the record's question whether a newer form of the task exists: just-in-time (commit-level) defect prediction is how the task is done in CI today. A different unit (commit with change metrics such as lines added, files, entropy, developer experience) from defect_data's module with static metrics, so related ...
- Adds: Large, recent, temporal by design (dated commits, the authors' own temporal split), one consistent labelling. Risks: SZZ label noise, and recent commits are under-labelled because their fixes come later | A large, dated, temporal defect task across projects. Caveat: the label comes from an SZZ-style tracing heuristic ...
