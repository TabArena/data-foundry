---
unique_name: antarex_hpc_fault_classification
name: Antarex HPC Fault Dataset
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 3
decision_markers:
- Time-series (Classification)
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
original_source: Other
year: '2018'
domain: technology & internet
required_split:
- Temporal (NON-IID)
problem_type: Multiclass Classification
source_links:
- https://doi.org/10.5281/zenodo.2553224
- https://doi.org/10.1016/j.future.2019.11.029
- https://doi.org/10.1007/978-3-030-29400-7_1
- https://arxiv.org/abs/1810.11208
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 3: 32 days of per-second LDMS performance metrics from one experimental HPC node at ETH Zurich with faults injected on a schedule, published for online fault classification (healthy or one of 8 fault programs); a real monitoring decision on real metrics, but the faults are emulated, the rows are windows we build from series, and the source's random forest already reaches an F-score of 0.98.
- Source: Netti, Kiziltan, Babaoglu, Sîrbu, Bartolini & Borghesi, "Antarex HPC Fault Dataset", Zenodo, 2018-10-10 (doi 10.5281/zenodo.2553224, CC BY 4.0; Antarex.zip 1.6 GB and a readme PDF), with "Online Fault Classification in HPC Systems through Machine Learning" (arXiv 1810.11208, Euro-Par 2019, doi 10.1007/978-3-030-29400-7_1) and the FINJ fault-injection paper (Euro-Par 2018 workshops). Zenodo: "trace data collected from the homonymous experimental HPC system located at ETH Zurich while it was subjected to fault injection, for the purpose of conducting machine learning-based fault detection studies"; "we executed benchmark applications and at the same time injected faults in the system at specific times via dedicated programs"; "4 dataset blocks for 32 days of data acquisition, and 20GB of uncompressed data". As published: CSV files of LDMS metrics per time point and FINJ logs of the application and fault program running at each time point (two tables joined on time). Paper, Table 1: CPU-memory blocks (12 days; DGEMM, HPCC, STREAM, HPL; faults leak, memeater, ddot, dial, cpufreq, pagefail) and hard-drive blocks (4 days; IOZone, Bonnie++; ioerr, copy), each single-core and parallel. Section 3: "Each feature vector corresponds to a 60-second aggregation window and is related to a specific CPU core. The step between feature vectors is of 10 seconds", with per-metric mean, standard deviation, median, minimum, maximum, skewness, kurtosis and percentiles, labelled by the fault program running in the window or "healthy".
- Use case: an HPC centre's monitoring diagnoses a fault on a compute node as it happens, so the operator can act (drain or restart the node, stop an interfering process); the paper proposes a method "suitable for online deployment in HPC systems" (Introduction); fit approximate: the faults are programs that emulate faults ("This simulates a system misconfiguration or failing CPU fault", for cpufreq) on one node, and the authors note "training is performed before HPC nodes move into production (i.e., in a test environment)" (Conclusion). Regime temporal: the paper keeps the folds in "time-stamp order", "each containing data from a specific time frame", as the "realistic, online scenario" (Section 4).
- Siblings and duplicates: `tokyo1` (`TBD -> 2nd Tier`, `Data Quality Issue`, `Outdated`, `Not Representative`; good or bad server state from 1990s counters), the record this was found for; `backblaze_hard_drive_failure` (`TBD -> Yes`), drive failure from SMART data, another task. External collections: not searched (web search budget used up).
- Better data: found as better data for `tokyo1` (the data-scouting run of 2026-10-30/31); no further search.
- Papers and pages: the Zenodo record; arXiv 1810.11208 (Sections 2-4); the extension in Future Generation Computer Systems 2020 (doi 10.1016/j.future.2019.11.029, not read); the FINJ paper.
- Metric: "We chose 5-fold cross-validation for evaluation of classifiers, using the average F-score as metric" (arXiv 1810.11208, Section 4), one deliberate criterion (MET-5), but a hard-label metric with no threshold or costs fixed (MET-6), and macro or weighted is not stated; so the fallback `log_loss` for the multiclass target unless the curator keeps a macro F1; inputs none.
- Risks for /add-dataset: the rows are windows we build (`Time-series (Classification)`, `Needs extensive data wrangling`: join the LDMS CSVs with the FINJ logs, window, label by the window's mode); windows overlap (10-second step on 60 seconds) and the per-core rows of one time point are near-copies, so random folds leak (LEAK-17; the paper tests on "only one randomly-selected core for each time point"); emulated faults on one node (`Not Representative` to weigh, USE-8); the F-score of 0.98 asks for a TP-4 probe; 20 GB raw.
- Priority: gap + (multiclass is thin), use case 0 (approximate), source + (Zenodo with two papers), shape + (32 days of windows over many metrics, temporal), risk − (emulated faults, windowing, near-perfect scores).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `tokyo1`.
- as published: four blocks (CPU/memory faults and hard-drive faults, each single-core and multi-core), 32 days of continuously sampled LDMS performance metrics from the experimental Antarex HPC node, about 20 GB ...; target: the node's state at each time point: healthy or the injected fault type (hardware, misconfiguration, interference from other processes); access: open.
- Why: same task as tokyo1: classify a server's state (good/bad) from system performance counters (tokyo1: 46 SGI Performance Co-Pilot counters with a good/bad label; here LDMS counters with the known fault as label)
- Adds: a label set by design (the injected fault), not an unknown judgement; multi-class; newer (2018 vs 1990s); far more time points; open licence and two papers. Caveats: one experimental node with injected faults, so not representative of production faults; a time series that needs windowing and a temporal split, which ...
