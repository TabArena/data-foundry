---
unique_name: spec_cpu2017_results
name: SPEC CPU2017 published results (all four suites, CSV dump of all records)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
original_source: Website
year: '2017'
domain: technology & internet
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.spec.org/cpu2017/results/
- https://www.spec.org/cgi-bin/osgresults?conf=cpu2017
- https://www.spec.org/cgi-bin/osgresults?conf=cpu2017;op=dump;format=csvdump
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: every SPEC CPU2017 result published since 2017, one row per system and suite with about 35 columns of hardware, software and dates and the base and peak scores; the current form of the task `machine_cpu` was rejected for (Outdated), set by Tousi and Luján (2022) as predicting the score from the configuration; near-duplicate submissions to handle.
- Source: Standard Performance Evaluation Corporation (SPEC), SPEC CPU2017 results, published "since the announcement of the benchmark in June 2017" by quarter (results page), with "Dump All Records As CSV" on the search page (https://www.spec.org/cgi-bin/osgresults?conf=cpu2017;op=dump;format=csvdump). As published (preview of the first 40 KB of the CSV dump, 2026-10-31): 35 columns: `Benchmark` (the suite; the preview shows only `CINT2017` rows, the dump is sorted by suite), `Hardware Vendor`, `System`, `Peak Result`, `Base Result`, `Energy Peak Result`, `Energy Base Result`, `# Cores`, `# Chips`, `# Enabled Threads Per Core`, `Processor`, `Processor MHz`, `CPU(s) Orderable`, `Parallel`, two pointer sizes, four cache fields, `Memory`, `Storage`, `Operating System`, `File System`, `Compiler`, `HW Avail`, `SW Avail`, `License`, `Tested By`, `Test Sponsor`, `Test Date`, `Published`, `Updated`, `Disclosure` (links to the full report). Result ids run to cpu2017-20250419-47592, so tens of thousands of results over the four suites; rows not counted (the dump was not downloaded).
- Use case: a system architect, buyer or vendor estimates a configuration's score without running the benchmark. Tousi and Luján ask "can we accurately predict the SPEC results based on the configurations provided in the dataset, without having to actually run the benchmarks?" and "can we predict the performance of future systems using the past data?" (abstract; the body was not reachable, IEEE answered 418); fit approximate (the motivation is replacing slow simulation, and no buyer's decision is named). Regime temporal by hardware availability or publication date (the paper's question IV), with the processor model as a group inside it (SPLIT-13).
- Siblings and duplicates: `machine_cpu` (`No`, Outdated; Lennart: "There would be more relevant and newer datasets that could be used"): this record is that suggestion. No other SPEC record. External collections: none found.
- Better data: found as better data for `machine_cpu`; no further search this round.
- Papers and pages: Tousi and Luján, "Comparative Analysis of Machine Learning Models for Performance Prediction of the SPEC Benchmarks", IEEE Access, 2022 (doi 10.1109/access.2022.3142240, CC BY; abstract read through Semantic Scholar): elastic net, decision trees, random forests and MLPs, "tree-based models with the original 29 features provide accurate predictions with an average error of less than 4%". A paper that used the data, moved here from the links (PROV-12).
- Metric: the abstract reports an average percentage error; whether it is MAPE and whether the paper ranks models by it was not read (MET-5). Fallback `rmse` until the evaluation section is read; scores span a wide range, so a log target fits (MET-3); inputs none.
- Risks for /add-dataset: near-duplicate rows: one platform submitted by several vendors or with small changes, and one system in several suites (group by processor and system, SPLIT-29); the peak and energy results come from the same run as the base result and go when the base score is the target (LEAK-10); one target per suite, or the suite as a feature; free-text fields to parse (cache, memory, operating system, compiler; CLEAN); `Disclosure` holds links only; public use follows SPEC's Fair Use Guidelines (a note, EV-4).
- Priority: gap 0 (technology & internet has 4 accepted datasets; regression and temporal not thin), use case 0 (the paper names a purpose, not an actor, read from the abstract only), source + (SPEC's own disclosures and a paper that frames the task), shape + (tens of thousands of results, mixed types, dates), risk - (near-duplicate submissions).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `machine_cpu`.
- as published: one row per published system result in four suites (SPECrate and SPECspeed, integer and floating point); the CSV dump has about 58 columns: hardware vendor, system, cores, chips, threads per core, ...; target: the overall SPECrate or SPECspeed score (base) of a system configuration; access: open.
- Why: The same task as machine_cpu (Ein-Dor and Feldmesser 1987: a CPU's published relative performance from cycle time, memory, cache and channels), with features of the same kind (clock, cores, cache, memory), from the benchmark body that publishes the scores.
- Adds: Current hardware (2017 to now) instead of 209 machines of the early 1980s that the record rejected as Outdated, tens of thousands of results, availability dates for a temporal split ('predict the performance of future systems', question IV of the IEEE Access paper). Risks: many near-duplicate submissions of one ...
