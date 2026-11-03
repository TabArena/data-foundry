---
unique_name: travistorrent_ci_build_outcome
name: 'TravisTorrent: Travis CI builds joined with GitHub commit data'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
original_source: Website
year: '2015'
domain: technology & internet
source_links:
- https://doi.org/10.6084/m9.figshare.19314170
- https://doi.org/10.1109/MSR.2017.24
- https://github.com/TestRoots/travistorrent-tools
- http://web.archive.org/web/20201111222314/https://travistorrent.testroots.org/page_access/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: TravisTorrent, the MSR 2017 Mining Challenge data of Travis CI builds joined with GitHub commit data; build-outcome prediction at push time is a studied task (build skipping to save CI cost), the data is large and multi-project, but many columns are post-build and the job rows must be collapsed to builds.
- Source: Beller, Gousios and Zaidman, "TravisTorrent: Synthesizing Travis CI and GitHub for Full-Stack Research on Continuous Integration", MSR 2017, pp. 447-450 (doi 10.1109/MSR.2017.24); the authors' figshare deposit (doi 10.6084/m9.figshare.19314170, 2022-03-06, CC BY 4.0) holds `final-2017-01-25.csv.gz` (264.6 MB), the earlier releases of 2015-08-28 and 2016-03-05, and the paper; the first public release is the one of August 2015. As published (header of the final release, previewed): 66 columns, one row per Travis job: tr_build_id, gh_project_name, gh_is_pr, gh_lang, git_branch, gh_num_commits_in_push, git_prev_commit_resolution_status, tr_prev_build, gh_team_size, gh_num_issue_comments, gh_num_commit_comments, gh_num_pr_comments, git_diff_src_churn, git_diff_test_churn, files added, deleted and modified, tests added and deleted, gh_num_commits_on_files_touched, gh_sloc, test density per kloc, gh_by_core_team_member, gh_description_complexity, gh_pushed_at, gh_build_started_at, gh_repo_age, gh_repo_num_commits, tr_job_id, the tr_log_* log-analysis columns (test counts, failures, durations, frameworks), tr_duration, tr_status (the build outcome) and tr_jobs. The counts of the assessment (3,881,992 jobs, 925,897 builds, 948 projects) come from a third-party profile and were not checked; the paper was not read (no PDF reader in this session).
- Use case: a CI service or a project's maintainers decide at push time whether to run, skip or postpone a build by predicting whether it will fail, to save CI cost; Jin and Servant, "A cost-efficient approach to building in continuous integration", ICSE 2020 (doi 10.1145/3377811.3380437; title read, text not) frame build prediction that way. Fit direct for the push-time decision. Regime temporal within projects (a model trained on past builds predicts the next ones); grouped by project is the alternative for new projects; one regime (USE-10), the curator's call.
- Siblings and duplicates: `apachejit` (`TBD -> Yes`, just-in-time defect prediction on Apache commits; another source and target, PROV-7); no other CI record (grep for travis, CI build). External collections: the MSR 2017 Mining Challenge.
- Better data: found through the dead-link check of the curator's Zotero collection and its item 148 (awesome-public-datasets); no further search this round.
- Papers and pages: Beller et al. 2017 (the data); Jin and Servant 2020 (build skipping; moved here from the links, PROV-12); the MSR 2017 challenge papers on build outcome prediction (not read); the generating tools (github.com/TestRoots/travistorrent-tools).
- Metric: none read: the build-skipping papers weigh saved builds against observed failures, several criteria (not read, MET-5); so the fallback `roc_auc` for a failed (or errored) build against a passed one. Inputs none.
- Risks for /add-dataset: post-build columns leak the outcome (tr_log_*, tr_duration, tr_jobs; LEAK-10); job rows to collapse to builds; comment counts may be taken after the build (check their timing); the previous build's status only from earlier builds; the target classes (passed, failed, errored, canceled) and the framing (binary or multiclass); size (cap); Travis CI's open-source service ended around 2021 (the decision lives on under other CI services; an `Outdated` question at most).
- Priority: gap 0 (technology & internet has 4 accepted, just above thin; binary and temporal are covered), use case + (build skipping in Jin and Servant 2020), source + (MSR paper, the authors' deposit), shape + (hundreds of thousands of builds, mixed types, timestamps and projects), risk - (post-build columns, the job-to-build collapse).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the dead-link check of the curator's Zotero collection; the curator's Zotero collection, item 148: "awesomedata/awesome-public-datasets".
- as published: final-2017-01-25.csv.gz, 265 MB. A third-party profile (github.com/ayushman46/releaselens, not verified here) counts 3,881,992 job rows, 925,897 builds, 948 GitHub projects (Java, Ruby, Python, Go) ...; target: build outcome (tr_status: passed / failed / errored), per build; access: open.
- Why: The standard open dataset for CI build-outcome prediction, released by its authors under CC BY 4.0. It is large and multi-project and has features known at push time: churn, files changed, commits in the push, team size, core-member author, PR or push, project age and size, test density, previous build status.
- Adds: Software engineering / DevOps build-failure prediction; the records have no CI data. Caveats: many tr_* and tr_log_* columns are post-build (duration, test counts) and leak. Job rows must be collapsed to builds. Builds within a project form a sequence, so split by project or by time. The Travis CI open-source era ...
