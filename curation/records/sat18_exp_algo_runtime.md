---
unique_name: sat18_exp_algo_runtime
name: ASlib SAT20-MAIN (SAT Competition 2020 main track)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
original_source: ASlib
domain: technology & internet
required_split:
- Grouped (NON-IID)
problem_type: Regression
source_links:
- https://github.com/coseal/aslib_data/tree/master/SAT20-MAIN
- https://satcompetition.github.io/2020/
- https://doi.org/10.1016/j.artint.2016.04.003
- https://github.com/coseal/aslib_data/tree/master/SAT11-HAND
- https://github.com/coseal/aslib_data/tree/master/SAT18-EXP-ALGO
- http://sat2018.forsyte.tuwien.ac.at/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: a newer SAT runtime scenario from ASlib for the slot of `sat11_hand_algo_runtime`. The record joins two scenarios (its unique name says SAT18-EXP-ALGO, its title SAT20-MAIN), and the curator should settle it to one.
- Source: ASlib (COSEAL); both scenarios read 2026-10-31. SAT18-EXP-ALGO ("source: http://sat2018.forsyte.tuwien.ac.at/", translated by Damir Pulatov; algorithm features as in Pulatov et al. 2022, PMLR v188): 353 instances x 37 solvers = 13,061 runs (ok 6,380, timeout 6,681; 67 instances solved by no solver), cutoff 5000 s, about 50 instance features in 2 feature steps, algorithm features for all 37 solvers. Its readme: "The data does not distinguish between timeout, memout and crashes" and "I excluded instances for which I couldn't extract instance features due to timeout or memout." SAT20-MAIN ("all the solvers and instances of the main track of the SAT 2020 competition", translated by Marie Anastacio and Théo Matricon): 400 instances x 67 solver configurations = 26,800 runs (ok 12,955, timeout 13,423, crash 234, other 116, memout 72; 77 instances unsolved), about 108 SATzilla features computed "with a timeout of 1 minute for each feature category", and no algorithm features.
- Use case: as for `sat11_hand_algo_runtime`, a portfolio solver predicts each solver's runtime on a new instance from cheap features and runs the fastest. Fit direct. Regime grouped by instance.
- Siblings and duplicates: `sat11_hand_algo_runtime` (`Yes`); `sat03_16_indu_algo_runtime` (this run; industrial instances of 2003-2016, 2,000 instances, with algorithm features); the other ASlib records listed there. Whether the 2018 and 2020 main tracks reuse instances of the older competitions in SAT03-16 was not checked. External collections: not on OpenML under these names; others not checked.
- Better data: found as better data for `sat11_hand_algo_runtime`, and in the curator's Zotero collection (item 153); no further search.
- Papers and pages: the two scenario readmes and descriptions; the SAT Competition 2018 and 2020 pages; Bischl et al. 2016; Pulatov et al. 2022.
- Metric: both descriptions declare "performance_measures: runtime" with a 5000 s cutoff; ASlib scores runtime scenarios by PAR10 (Bischl et al. 2016), so `par_k` (k = 10) of the selected solver per instance, as for `sat11_hand_algo_runtime` (MET-5); inputs the instance id as the group.
- Risks for /add-dataset: one scenario has to be picked and the record's name and title aligned (SAT18-EXP-ALGO keeps sat11's algorithm-feature format; SAT20-MAIN is newer and larger but identifies a solver only by its name). SAT18-EXP-ALGO dropped the instances whose features failed, likely the largest, and does not separate timeouts from crashes. About a fifth of the instances are unsolved by every solver. The curator's open question how many ASlib scenarios to keep.
- Priority: gap 0 (technology & internet, regression and grouped are not thin), use case + (algorithm selection), source + (ASlib readmes and the competitions), shape + (13,061 or 26,800 runs over 353 or 400 instance groups), risk - (two scenarios in one record; instances dropped on feature failure).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `sat11_hand_algo_runtime`; the curator's Zotero collection, item 153: "aslib_data/SAT11-HAND at master · coseal/aslib_data".
- as published: 400 SAT instances x 67 solver configurations = 26,800 runs; about 108 SATzilla instance features (1-minute cap per feature group); 5000 s cutoff; 2020; target: solver runtime in seconds per (instance, solver); timeouts, memouts and errors are set to the cutoff (scored PAR10); access: open.
- Why: Same task, same kind of features and same grouped-by-instance setting as sat11_hand_algo_runtime. That record's note asks for newer SAT cases and says to focus on SAT solving. Repo licence: GPLv3. | Exactly the format of sat11_hand_algo_runtime ((instance features, algorithm features) -> runtime), from the same ...
- Adds: Nine years newer, with modern CDCL solvers: 67 solvers instead of 15 and 26,800 runs instead of 4,440, all from one competition main track. There are no algorithm features (only solver identity), unlike the -ALGO variant the record uses. Same library, different data, so not a version (the cpmp record warns against ...

**Assessment (AI, 2026-10-31):** cleanup flag of the data-scouting run: the record mixes two ASlib scenarios: its name says SAT18-EXP-ALGO, its title SAT20-MAIN; split it or pick one.
