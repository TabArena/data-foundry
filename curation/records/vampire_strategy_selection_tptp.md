---
unique_name: vampire_strategy_selection_tptp
name: Vampire strategy performance measurements
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
decision_markers:
- Needs extensive data wrangling
tags:
- Non-IID (Grouped)
- AI-Filled (Verify)
original_source: Other
year: '2024'
domain: technology & internet
required_split:
- Grouped (NON-IID)
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.5281/zenodo.10814478
- https://zenodo.org/records/10814478
- https://doi.org/10.1007/978-3-031-63498-7_12
- https://arxiv.org/abs/2403.12869
- https://ceur-ws.org/Vol-3717/short2.pdf
- https://tptp.org/cgi-bin/SeeTPTP?Category=Problems&Domain=SET&File=SET014+4.p
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: 8.6 million runs of 1,096 strategies of the Vampire prover on 7,866 TPTP first-order problems (2024), with status and time per run; a current algorithm-selection task of the ASlib kind, once a feature table is built from the TPTP problem headers and the class set is chosen.
- Source: Bártek and Suda (Czech Technical University in Prague), "Vampire strategy performance measurements", Zenodo 2024-03-14 (doi 10.5281/zenodo.10814478, CC BY 4.0), supplement to Bártek, Chvalovský and Suda, "Regularization in Spider-Style Strategy Discovery and Schedule Construction", IJCAR 2024 (doi 10.1007/978-3-031-63498-7_12, arXiv 2403.12869). As published (README): `runs.csv`, 8,621,136 runs (strategy, problem, status UNS/TMO/GUP/ERR, search and parse time in megainstructions); `strategies.csv` (the strategy string, its limit of 2,000 to 256,000 Mi, the witness problem it was discovered on); `problems.txt` (7,866 FOF problems of TPTP v8.2.0, known-satisfiable ones excluded); 6,796 problems solved by some strategy, 4,264 by the default. No problem features.
- Use case: the prover picks a strategy or schedule for a new problem before proof search, from the problem's features. The README's "Target task" is schedule construction, "to find a schedule that (approximately) maximizes the number of problems solved within the budget"; the group's PAAR 2024 extended abstract on these runs ("Cautious Specialization of Strategy Schedules", CEUR Vol-3717) branches schedules on problem features ("the number of atoms, the presence of certain syntactic traits, or the membership in standard logical fragments") and tests on held-out problems. A per-problem selection target is ours; fit approximate. Regime grouped by TPTP domain (problems of a domain share axioms), as the ASlib siblings are grouped.
- Siblings and duplicates: `first_order_theorem_proving` (`No`, `Outdated`; UCI 249, the E prover, 6,118 problems, 2012: another prover and source, no duplicate, PROV-4); `asp_potassco_classification` and `sat11_hand_algo_runtime` (`Yes`, ASlib). External collections: none found (the README names ASlib as similar data, not as a carrier).
- Better data: found as better data for `first_order_theorem_proving`.
- Papers and pages: the Zenodo README; the IJCAR 2024 paper (not read beyond its record); the PAAR 2024 abstract and introduction (read).
- Metric: the source's criterion is problems solved within the budget on test problems (README, "Target task"; PAAR 2024); for a per-problem selector, the share of test problems the chosen strategy solves within its limit, read from the run times as scoring columns (MET-2, MET-13), to argue at the add stage; otherwise the fallback `log_loss`.
- Risks for /add-dataset: features to assemble from the TPTP v8.2.0 headers (the syntax block; the "Rating" line comes from prover results and goes, LEAK-10) or from Vampire's own feature extraction (PROV-11); the class set (which strategies, the fastest per problem, a "none" class for the 1,070 unsolved) is our choice (USE-5); the strategies were discovered on these same problems (a witness each), so the portfolio is fit to the problem set.
- Priority: gap + (multiclass is thin), use case 0 (the selection target is ours), source + (Zenodo README, two papers), shape + (7,866 problems, TPTP domains as groups), risk - (no feature table, the class set to define).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `first_order_theorem_proving`.
- as published: 8,621,136 runs = 1,096 Vampire strategies x 7,866 first-order (FOF) problems of TPTP v8.2.0 (known-satisfiable problems excluded); per run: status (UNS/TMO/GUP/ERR), search time and parse time in ...; target: per problem, which strategy of a fixed portfolio proves it fastest, or none within the budget (the shape of UCI 249: five heuristics plus decline); the ...; access: open.
- Why: same task as first_order_theorem_proving: heuristic selection for a first-order prover from features of the conjecture known before any run. Features of the same kind are in the TPTP problem headers ('% Syntax': numbers of formulae, atoms, connectives, predicates, functors, variables, maximal formula and term depth; ...
- Adds: 7,866 problems against 6,118; a current, maintained prover (Vampire) and 1,096 strategies against a 2012 E setup with five heuristics, which answers the record's Outdated marker; the timings ship (the OpenML mirror lost them), so the paper-style metric can be computed. Caveats: no feature table in the deposit ...
