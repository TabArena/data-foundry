---
unique_name: first_order_theorem_proving
name: first-order-theorem-proving
checked_by:
- Lennart
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Outdated
tags:
- AI-Filled (Verify)
collections:
- TabArena Reject
- TabSTAR
problem_type: Multiclass Classification
source_links:
- https://www.openml.org/d/1475
- https://doi.org/10.24432/C5RC9X
source_row: 425
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Assessment (AI, 2026-10-22):** the curator's `No` (`Outdated`, Lennart, 2026-07-27) stands; the research gives one argument for and one against it, and the open consistency check of 2026-10-19 is the place to settle it.
- Source: UCI 249 (donated 2013-04-16; Bridge, Holden and Paulson, dataset citation 2012) and OpenML 1475; "Given a theorem, predict which of five heuristics will give the fastest proof when used by a first-order prover. A sixth prediction declines to attempt a proof, should the theorem be too difficult"; 6,118 rows, static and dynamic features of the conjecture; paper: Bridge, Holden and Paulson, "Machine Learning for First-Order Theorem Proving: Learning to Select a Good Heuristic", Journal of Automated Reasoning 53 (2014).
- Use case: a prover picks its heuristic per conjecture before the run (algorithm selection); fit direct; regime IID over conjectures (TPTP problems; families of related problems may call for a grouped check).
- For `No`: the labels are tied to one prover version and five fixed heuristic settings of 2012; a selector trained on them serves that configuration only.
- Against `No`: `asp_potassco_classification` and `sat11_hand_algo_runtime` ship as `Yes` with the same kind of fixed solver portfolio, and `Outdated` has no rule (selection.md). A fact that sets this one apart is still to be named.
- Metric: the paper ranks selectors by theorems proved and time taken under the selection (read from the abstract), which needs the per-heuristic timings; the multiclass mirror on OpenML loses them, so the fallback (log loss) unless the timings ship in the UCI files (MET-1, MET-5).
- Siblings: `asp_potassco_classification`, `sat11_hand_algo_runtime` (ASlib, `Yes`); external collections TabSTAR (as recorded). Not checked: the UCI files for the timings; the paper's full text.

first-order-theorem-proving (OpenML d/1475) is an **algorithm-selection** dataset: each row is a first-order-logic conjecture described by static syntactic / derived features, and the target is which theorem-prover heuristic (under a time bound) proves it fastest — a genuine tabular **multiclass classification** task, *not* a robotics / RL problem. The prior `Robotics (RL)` and `Wrong Domain / Source Modality` markers were incorrect and have been removed. It is kept as **No** on `Outdated` grounds (confirmed by Lennart, 2026-07-27): the ASlib-style algorithm-selection framing predates modern RL / LLM-based proving and is a niche, dated benchmark. To verify: confirm the prover set / class count and whether the algorithm-selection framing is itself in-scope.

CC: "Likely done with something like reinforcement learning or LLMs nowadays, but clearly an unsolved problem. Would need to read the paper; sounds like an algorithm selection problem too"

**Consistency check (AI, 2026-10-19):** this record is `No` on `Outdated` alone ("a niche, dated benchmark", confirmed 2026-07-27), while two algorithm-selection tasks of the same ASlib kind ship as `Yes`: asp_potassco_classification and sat11_hand_algo_runtime. `Outdated` has no rule behind it (selection.md, decision markers), and the precedents keep datasets with that concern unless a further fact excludes them (machine_cpu: newer data exists). What sets this one apart? (a) A fact about this data, such as an obsolete prover set the task depends on, recorded as the reason; (b) treat it like its ASlib siblings and reopen it; (c) reopen the siblings; (d) give `Outdated` a rule. Found by the precedent checker of the review-panel pilot on airfoil_self_noise.
