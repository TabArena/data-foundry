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

first-order-theorem-proving (OpenML d/1475) is an **algorithm-selection** dataset: each row is a first-order-logic conjecture described by static syntactic / derived features, and the target is which theorem-prover heuristic (under a time bound) proves it fastest — a genuine tabular **multiclass classification** task, *not* a robotics / RL problem. The prior `Robotics (RL)` and `Wrong Domain / Source Modality` markers were incorrect and have been removed. It is kept as **No** on `Outdated` grounds (confirmed by Lennart, 2026-07-27): the ASlib-style algorithm-selection framing predates modern RL / LLM-based proving and is a niche, dated benchmark. To verify: confirm the prover set / class count and whether the algorithm-selection framing is itself in-scope.

CC: "Likely done with something like reinforcement learning or LLMs nowadays, but clearly an unsolved problem. Would need to read the paper; sounds like an algorithm selection problem too"
