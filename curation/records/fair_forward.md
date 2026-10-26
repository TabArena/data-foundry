---
unique_name: fair_forward
name: fair-forward
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Duplicate
tags:
- AI-Filled (Verify)
required_split:
- '?'
problem_type: TBD
source_links:
- https://fair-forward.github.io/datasets/
source_row: 1042
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`Duplicate`, PROV-4): the record holds the same single link as `row_876`, the FAIR Forward catalog page; that record keeps the pointer for browsing.
- Source: https://fair-forward.github.io/datasets/, "FAIR Forward - Catalog of Open Source AI Datasets, Models & AI Systems", "Reusable AI building blocks for global challenges across agriculture, language technology, climate action, energy, and more"; GitHub repo Fair-Forward/datasets: "A catalog that links to the various datasets and use-cases created throughout our programme." A catalog, not one dataset: no rows, target or task.
- Siblings: `row_876` (same URL, note "Several interesting datasets").
- Next step: candidate tabular datasets from the catalog get records of their own (via `row_876`).
- Reject check (AI, 2026-10-22): stands. fair_forward.md and row_876.md both list https://fair-forward.github.io/datasets/ as their only source link (PROV-4). The page is a catalog ('A catalog that links to the various datasets and use-cases created throughout our programme'), not a dataset. row_876 keeps the pointer.

The record is only a link to a 'fair-forward' datasets landing page with no description, comments, or metadata. 'FAIR Forward' is an open-data initiative that likely hosts a collection of multiple datasets rather than a single curated tabular task, so it is unclear whether any individual dataset, target, modality, or size is benchmark-suitable. There is too little information to decide and it should not be rejected on that basis alone. A human must open the page, enumerate the available datasets, and pick/evaluate any concrete tabular predictive task.
