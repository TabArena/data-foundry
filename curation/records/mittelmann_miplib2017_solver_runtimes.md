---
unique_name: mittelmann_miplib2017_solver_runtimes
name: 'Mittelmann''s Benchmarks for Optimization Software: MILP benchmark on the MIPLIB 2017 benchmark set, 12 threads, per-instance run times'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
tags:
- Non-IID (Grouped)
- AI-Filled (Verify)
original_source: Website
domain: technology & internet
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://plato.asu.edu/ftp/milp.html
- https://plato.asu.edu/ftp/milp_tables/12threads.res
- https://plato.asu.edu/ftp/milp_res12/
- https://plato.asu.edu/ftp/milp_log12/
- https://miplib.zib.de/download.html
- https://doi.org/10.1007/s12532-020-00194-3
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: Mittelmann's current MILP benchmark (240 MIPLIB 2017 instances x 7 solver runs, 2-hour limit), the source the ASlib MIP-2016 scenario took its run times from, on a newer library and current solvers; a small table that changes with each solver release, without algorithm features, run on SCIP-perturbed instances, in a family the curator keeps at the second tier.
- Source: H. Mittelmann (Arizona State University), "Benchmarks for Optimization Software", page "The MIPLIB2017 Benchmark Instances (preprocessed data)", last updated 2026-10-28 (read): "The following codes were run with a limit of 2 hours on an AMD Ryzen 9 5900X (12 cores, 128GB)"; COPT-9.0.0, SCIP/spx-10.0.0, FiberSCIP-11.0.0, HiGHS-1.15.0 and 1.15.1 (parallel), Optverse-2.0.1 (SCIPCO forthcoming); the instances were preprocessed with SCIP, which randomly perturbed rows and columns and ran a quick presolve ("Testset: modified", names prefixed `p_`); scored by shifted geometric means, "All non-successes are counted as max-time". The 12-thread table (read): 240 rows, run times in seconds or `timeout` / `abort` (solved per solver: 136 to 225 of 240). Instance features: MIPLIB 2017's raw_data.zip, "raw feature data before and after trivial presolving, for all instances" (miplib.zib.de; Gleixner et al. 2021, Mathematical Programming Computation, doi 10.1007/s12532-020-00194-3).
- Use case: a user with a new MIP instance picks the solver expected to be fastest from cheap instance features (ASlib's algorithm selection); Mittelmann's page compares solvers and names no selection. Fit approximate (MIPLIB's features describe the original instances, the runs perturbed and presolved copies). Regime grouped by instance, as `sat11_hand_algo_runtime`.
- Siblings and duplicates: `mip_2016_regression_from_aslib_data` (TBD -> 2nd Tier; its ASlib readme takes the run times from the "12 threads" table of Mittelmann's evaluations on MIPLIB 2010, features from the UBC EPM code), so a newer release of the same source (PROV-6): the curator decides which one enters. `sat11_hand_algo_runtime` and `asp_potassco_classification` (Yes), `sat03_16_indu_algo_runtime` and `sat18_exp_algo_runtime` (TBD -> Yes, this run), `cpmp_2015_regression_from_aslib_data` (TBD -> 2nd Tier; "too much of the same might add a negative bias"). External collections: none found.
- Better data: found as better data for `mip_2016_regression_from_aslib_data`; no further search this round.
- Papers and pages: the Mittelmann pages with per-solver result and log files; the MIPLIB 2017 paper; BenLOC (arXiv 2506.02752; COPT under two configurations on 627 MIPLIB 2017 instances), seen by the scout, not proposed.
- Metric: Mittelmann ranks solvers by the shifted geometric mean of run time with failures at the limit, a solver comparison rather than a selection score; the ASlib family declares PAR10 of the selected solver, so `par_k` (k = 10, cutoff 7200) as on `sat11_hand_algo_runtime` (MET-5 through the scenario precedent); inputs the instance id as the group.
- Risks for /add-dataset: the page is overwritten with each solver release, so pin a dated snapshot of the result files; features of the original MIPLIB instances against runs on perturbed copies (or recompute them with MIPLIB's feature extractor); no algorithm features, so the solver is a categorical input or a multi-output target; 240 instances with many all-timeout rows (`p_bab2`) make a small grouped task (TP-5 at add); two SCIP and two HiGHS columns are versions or settings of one solver.
- Priority: gap 0 (technology & internet, regression and grouped not thin), use case 0 (not named by the source), source + (Mittelmann's documented benchmark and MIPLIB), shape 0 (240 instances), risk - (a version of a record's source, a moving table on perturbed instances).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `mip_2016_regression_from_aslib_data`.
- as published: 240 MIPLIB 2017 benchmark instances x 7 solver columns (COPT 9.0, FiberSCIP, HiGHS 1.15 serial and parallel, Optverse 2.0.1, SCIP 10/11), wall-clock seconds with a 2-hour limit ('timeout', 'abort' ...; target: per-instance run time of each solver (PAR10 with a timeout, as in ASlib), for per-instance solver selection; access: open (plain-text tables and logs on plato.asu.edu; MIPLIB features open).
- Why: The ASlib MIP-2016 readme says its run times were 'directly taken from the 12 threads table of H. Mittelmann's evaluations' on the solvable MIPLIB 2010 instances, with features from the UBC EPM code. This is the same publisher's same table, now on MIPLIB 2017 with current solvers, and MIPLIB 2017 publishes the ...
- Adds: A newer instance library (MIPLIB 2017 against 2010) and solver versions from 2026, 240 against 218 instances, 7 solvers against 5. The table is refreshed with each solver release, so it can be versioned. The record's open questions stay: grouped split by instance, and multi-output runtime against selection. Not much ...
- A newer release of the same source as the record(s) named above (PROV-6): the curator decides which one enters.
