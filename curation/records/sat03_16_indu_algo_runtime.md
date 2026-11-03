---
unique_name: sat03_16_indu_algo_runtime
name: ASlib scenario SAT03-16_INDU-ALGO (10 SAT solvers on 2,000 industrial instances, with algorithm features)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 4
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
original_source: ASlib
year: '2017'
domain: technology & internet
required_split:
- Grouped (NON-IID)
problem_type: Regression
source_links:
- https://github.com/coseal/aslib_data/tree/master/SAT03-16_INDU-ALGO
- https://github.com/coseal/aslib_data/tree/master/SAT03-16_INDU
- https://github.com/coseal/aslib_data/tree/master/SAT20-MAIN
- https://github.com/coseal/aslib_data/tree/master/SAT18-EXP-ALGO
- http://www.satcompetition.org/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 4: the ASlib scenario of 10 SAT solvers on 2,000 industrial instances (20,000 runtimes) with instance and algorithm features: the task and format of `sat11_hand_algo_runtime` on about 7 times its instances, with solvers from 2016.
- Source: ASlib (COSEAL), scenario SAT03-16_INDU-ALGO by Rolf-David Bergdoll, "Part of Open Algorithm Challenge 2017 ("Sora")" (readme.txt); library paper Bischl et al. 2016, Artificial Intelligence 237:41-58. As published (files read 2026-10-31): "10 modern SAT solvers run on 2000 industrial instances of SAT-Competitions" 2003 to 2016, the solvers chosen from the 2016 industrial track. `algorithm_runs.arff` has 20,000 rows, one run per instance and solver (ok 15,063, timeout 4,754, crash 146, other 36, memout 1; 269 instances solved by no solver), as PAR10 values with a 5000 s cutoff (timeouts stored as 50,000). `feature_values.arff` holds about 480 instance features (SATzilla 2012 and the TU Dresden `tud_` features, 18 feature steps); `algorithm_feature_values.arff` about 75 code features for 8 of the 10 solvers (none for cominisatps and riss5); `cv.arff` 10 folds by instance. SAT03-16_INDU holds the same runs without algorithm features (a version, PROV-6).
- Use case: a portfolio SAT solver picks, for a new instance, the solver predicted fastest from cheap instance features before running any (ASlib's algorithm selection). Fit direct, as for `sat11_hand_algo_runtime`. Regime grouped by instance (the curator's choice for sat11, CC 2026-10-06: hold out instances, not families).
- Siblings and duplicates: `sat11_hand_algo_runtime` (`Yes`, BeyondArena; crafted instances of 2011, 296 instances, 4,440 runs) is the same task on another scenario, not a duplicate. `sat18_exp_algo_runtime` (this run) is the other newer SAT candidate. `asp_potassco_classification` (`Yes`), `cpmp_2015_regression_from_aslib_data` and `mip_2016_regression_from_aslib_data` (both `TBD -> 2nd Tier`: "too much of the same might add a negative bias") are other ASlib scenarios. External collections: not on OpenML under its name (data-list API); others not checked.
- Better data: found as better data for `sat11_hand_algo_runtime` (the data-scouting run of 2026-10-30/31); no further search.
- Papers and pages: the scenario's readme and description; Bischl et al. 2016; Pulatov et al. 2022 (PMLR v188) for algorithm features.
- Metric: `description.txt` declares "performance_measures: PAR10" with "algorithm_cutoff_time: 5000", so `par_k` (k = 10, cutoff 5000) of the selected solver per instance, as declared for `sat11_hand_algo_runtime` (MET-5: the scenario's one declared measure); inputs the instance id as the group, which ships as the split group.
- Risks for /add-dataset: algorithm features exist for 8 of the 10 solvers (drop two solvers, or add the solver's name); 269 of the 2,000 instances time out for every solver, so all their rows carry the cutoff penalty; instances were de-duplicated by feature vector, "which might however also have removed some instances that simply had the same features"; the curator's open question how many ASlib scenarios to keep (the cpmp and mip records).
- Priority: gap 0 (technology & internet, regression and grouped are not thin; ASlib as a source is), use case + (algorithm selection, named by the library), source + (ASlib readme, description and paper), shape + (20,000 runs over 2,000 instance groups, about 555 features), no known risk.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `sat11_hand_algo_runtime`.
- as published: 2,000 instances x 10 solvers = 20,000 runtime rows; SATzilla 2012 plus TU Dresden instance features (18 feature steps), algorithm features file, 5000 s cutoff, PAR10, a 10-fold cv.arff by instance. ...; target: solver runtime on an instance (seconds, censored at the 5000 s cutoff), scored as PAR10 of the selected solver; access: open.
- Why: the same task as the record: (instance features, algorithm features) -> runtime, held out by instance, from the same benchmark library and format, so the record's metric (par_k, group instance_id) carries over
- Adds: about 4.5x the rows (20,000 vs 4,440) and 7x the instances (2,000 vs 296), industrial instances from 14 competition years and solvers from 2016 rather than 2011; the curator's note on the record asks for newer SAT cases ('maybe checkout if any newer cases exist'); SAT20-MAIN is the newest SAT option if algorithm ...
