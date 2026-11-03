---
unique_name: js_vulnerable_functions
name: JavaScript vulnerable-function dataset with static source code metrics (Ferenc et al., RAISE 2019); process-metric extension (Viszkok, Hegedus, ...
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
original_source: Website
year: '2019'
domain: technology & internet
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.1109/RAISE.2019.00010
- http://www.inf.u-szeged.hu/~ferenc/papers/JSVulnerabilityDataSet/
- https://doi.org/10.5281/zenodo.4590021
- https://doi.org/10.5220/0010558501850195
- https://doi.org/10.5281/zenodo.8369963
- https://doi.org/10.3390/e24050651
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: a peer-reviewed, open set of about 12,100 JavaScript functions from Node.js projects, labelled vulnerable when a fix for a known vulnerability (Node Security Platform, Snyk) changed them, with 35 static metrics and a 2021 version adding process metrics; the documented version of the task `vulnonevul` could not trace.
- Source: Ferenc, Hegedűs, Gyimesi, Antal, Bán and Gyimóthy, "Challenging Machine Learning Algorithms in Predicting Vulnerable JavaScript Functions", RAISE 2019 (doi 10.1109/RAISE.2019.00010), online appendix with JSVulnerabilityDataSet 1.0 at the University of Szeged; process-metric version by Viszkok, Hegedűs and Ferenc (ICSOFT 2021) on Zenodo 4590021 (`pm_uom_all_full.csv`, 5 MB, CC BY 4.0, 2021-03-09). As published (header of the 2021 file): about 60 static and process metrics (McCC, LOC and LLOC, nesting, parameters, Halstead measures, warnings, churn, number of changes and contributors) plus `name`, `longname`, `path`, `full_repo_path` (GitHub URL), commit `hash`, line and column positions, target `Vuln`. Size per Kalouptsoglou et al. 2022 (Zenodo 8369963): "12,106 JavaScript functions, from which 1,493 are considered vulnerable" (12.3%).
- Use case: a development or security team ranks its functions by predicted vulnerability to focus review and testing before a release; the abstract motivates "finding vulnerable components and applying existing mitigation techniques". Fit approximate (positives are functions later fixed; negatives come from the same project versions). Regime grouped by project (functions of one repository and commit share code and history); to settle at add.
- Siblings and duplicates: `vulnonevul` (No, `Missing source information`; OpenML 44150, 5,692 rows); `apachejit` (a just-in-time defect candidate, another unit). No duplicate (grep vulnerab, snyk). External collections: none found.
- Better data: found as better data for `vulnonevul`; another source (PROV-4).
- Papers and pages: RAISE 2019 (abstract read); Viszkok et al., ICSOFT 2021 (doi 10.5220/0010558501850195); Kalouptsoglou et al., Entropy 24:651 (2022), adding token sequences.
- Metric: the RAISE paper ranks models by F-measure after grid search and re-sampling ("KNN ... F-measure of 0.76 (0.91 precision and 0.66 recall)", abstract), with no fixed threshold or costs: a threshold metric without a fixed decision (MET-6), so the fallback `roc_auc`.
- Risks for /add-dataset: process metrics (changes, churn, contributors) must count only history up to the labelled commit (LEAK-10; check the 2021 extraction); ids and positions (`hash`, path, URL, lines) go; the same function at several commits may appear twice (LEAK-16, LEAK-17); only projects with a known vulnerability, up to about 2018 (a `Selection Bias` question at add).
- Priority: gap 0, use case 0 (a motivation, no actor or decision named), source + (peer-reviewed paper, university appendix, Zenodo), shape + (12,106 rows, about 60 numeric metrics, grouped by repository), risk - (timing of the process metrics).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `vulnonevul`.
- as published: one row per JavaScript function from real open-source Node.js projects on GitHub: 'more than 12,000 functions', 1,493 vulnerable (Kalouptsoglou et al. 2022, Entropy 24:651, which re-uses it); 35 ...; target: Vuln: 1 if the function was changed by the commits that fixed a vulnerability listed in the Node Security Platform or Snyk databases (taken at the parent ...; access: open.
- Why: the same task as vulnonevul: function-level binary vulnerability prediction from static code metrics (vulnonevul's 16 columns are of the same kind: cyclomatic number, loops, nesting degree, SLOC, parameters, callers/callees), with labels traced to public vulnerability databases and a peer-reviewed paper
- Adds: a traceable source and labelling procedure (vulnonevul has none: OpenML 44150 says only 'Vulnerability Dataset For Binary Classification'), about twice the rows (12,000+ against 5,692), more metrics. Caveats: JavaScript rather than C (no pointer metrics); non-vulnerable functions come from the same files and commits, ...
