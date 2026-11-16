---
unique_name: github_pull_request_acceptance
name: 'Pull request decisions explained: an empirical overview (3.35M GitHub pull requests)'
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 3
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
original_source: Other
year: '2020'
domain: technology & internet
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://zenodo.org/record/4837134
- https://arxiv.org/abs/2105.13970
- https://doi.org/10.1109/TSE.2022.3165056
- '# the first release (MSR 2020 Data Showcase, public version, pull-request ids removed)'
- https://zenodo.org/records/3922907
v2_path: datasets/_dev/tabarena-v0pt2/github_pull_request_acceptance_1m/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-11-08):** `TBD -> Yes`, priority 2: 3.35 million closed GitHub pull requests of 11,230 projects (GHTorrent dump of June 2019) with 95 factors and the decision merged or not, published to explain integrators' decisions; predicting the merge when a pull request arrives is a real task, but about half the factors are measured after it was opened.
- Source: first published as Zhang, Rastogi, Yu, "On the Shoulders of Giants: A New Dataset for Pull-based Development Research", MSR 2020 Data Showcase (doi 10.1145/3379597.3387489; Zenodo 3922907 of 2020-03-07, 96 factors, pull-request ids removed "because there are some person related factors in the dataset"); enlarged for Zhang, Yu, Gousios, Rastogi, "Pull Request Decisions Explained: An Empirical Overview", IEEE TSE 49(2):849-871, 2023 (doi 10.1109/TSE.2022.3165056, arXiv 2105.13970, read), data on Zenodo 4837135 (2021-05-28, CC BY 4.0: `new_pullreq.csv` 1.95 GB and an SQL dump). As published: "3,347,937 pull requests with 95 features from 11,230 diverse projects" (abstract), closed pull requests to the default branch, up to the GHTorrent dump of 2019-06-01 (the paper studies periods before June 2016 to June 2019). The CSV header (a 200 KB preview, 334 rows, 81% merged) has 101 columns: `id`, `project_id`, `creator_id`, `last_closer_id`, the target `merged_or_not`, `last_close_time` and the 95 factors of Table 2 (developer, project and pull-request characteristics). No creation time ships; it is `last_close_time` minus `lifetime_minutes`.
- The task's table: one row per pull request, 3,347,937 rows (stated; the paper removed about 2% with negative times, and whether the CSV still holds them was not checked) x about 48 inputs known when the pull request is opened (the contributor's history, followers, prior reviews and core membership; the project's size, age, open issues and pull requests and success rates; the change: churn, files, commits, tests, description length), with `project_id` as the group. Access: open, CC BY 4.0, one 1.95 GB CSV, no login.
- Use case: an integrator who receives a pull request decides whether to review it now, ask for changes or close it, and a merge score at submission orders the queue. The paper explains decisions and names no such actor ("suggesting an improvement for decision making", Sec. 3.1.1), so the use case is ours. Fit direct once the later factors go. Regime temporal: the paper splits "on close time", the first 90% for training (Sec. 2.4.3); projects recur, and a known project's history is legitimate (USE-10, SPLIT-13).
- Siblings and duplicates: no other pull-request record (grep: pull request, pullreq, ghtorrent). The MSR 2020 and TSE releases are versions of one dataset (PROV-6); the TSE one fills missing countries and adds factors, so it is the one to build. Gousios and Zaidman's MSR 2014 pull-request dataset is the ten times smaller predecessor (no record). External collections: none found.
- Better data: none searched (found by the data-scouting run of 2026-11-08).
- Papers and pages: the TSE paper (Sec. 2.2 data collection, Table 2, Sec. 2.4.3 evaluation); the MSR 2020 paper (not read).
- Metric: the TSE paper reports weighted precision, weighted recall, weighted F-score and AUC_test side by side for its basic model (Sec. 2.4.3 and 3.1.1: 0.89, 0.90, 0.89, 0.82) with no single criterion, so the fallback `roc_auc` (MET-5, MET-8). Inputs: none.
- Risks for /add-dataset: 47 factors are measured after submission and go (LEAK-10): `same_user` (the closer is the submitter, the paper's strongest factor), `lifetime_minutes`, `first_response_time`, every comment, emotion and participant field, the CI build counts and statuses, `reopen_or_not`, and every factor about the integrator (`inte_*`, `same_country`, `same_affiliation`, `contrib_follow_integrator`, the personality differences), since the integrator is the one who closed it; `last_closer_id` too. The change-size fields (churn, commits, files) may hold the final state rather than the one at submission (check against the MSR 2020 definitions). `contrib_gender` (inferred), country, affiliation and personality scores inferred from comments are personal attributes; whether they stay as inputs is the curator's call. `bug_fix` is 99.3% empty (paper). The size calls for a cut (recent years, or a 1M cap).
- Priority: gap 0 (technology & internet, binary and temporal are covered), use case 0 (not named by the source), source + (journal paper and documented Zenodo release), shape + (3.35M rows, about 48 mixed inputs, temporal with projects), risk - (half the factors leak).

Found by the data-scouting run of 2026-11-08 for the large-datasets review (wide tables outside biology and medicine, and tables with 2M+ rows).

CC (2026-11-08, Lennart): accepted for adding (`Yes`) in the screening review of the large candidates, round 2 (wide tables outside biology and medicine, tables with 2M+ rows).

**Assessment (AI, 2026-11-09):** review panel (full): ship after changes (made: `contrib_perc_commit` dropped as counted after the merge, LEAK-10, 64.6% against 22.8% above 0 among outsiders' merged and unmerged first pull requests, model cost 0.0006-0.0036 ROC AUC; `integrator_availability` dropped as no code, no gain; a LEAK-9 protocol line for the task gamer's test-row exploit, 0.81-0.82 to 0.90-0.92; `description_length` kept with its note, at most +0.0024; notes on the label, `pushed_delta` in seconds, the 94-95% known-project share, the row counts, the 180-day selection beside smartshark's one-year horizon and the pooled score); disputed: MET-5/MET-1 (pooled ROC AUC against within-project scoring: project merge rate alone 0.71-0.72 of 0.80-0.81 pooled, LightGBM 0.61-0.63 within projects; tied to the across-datasets item on scoring within groups); for the curator: issue 1. Priority 3: gap 0, use case 0, source +, shape +, risk 0 (use case: the integrator is ours with an approximate fit; source: Zhang et al., IEEE TSE 2023, with code; shape: 1,304,081 shipped rows, mixed types, temporal; risk: the panel's leaks are fixed, the open issue is the metric).
