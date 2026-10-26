---
unique_name: subseafloor_arc_2
name: subseafloor_arc
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target / Scientific Discovery
tags:
- Many features
- AI-Filled (Verify)
collections:
- New (BeyondArena)
domain: biology & life sciences
required_split:
- '?'
problem_type: TBD
original_data_state: Database (or multiple to-be-joined tables)
source_row: 862
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`No Good Target / Scientific Discovery`, SEL-3): the Bacteria amplicon table of the same marine-sediment diversity census as `subseafloor_arc`; no predictive task in the source.
- Source: Hoshino et al., PNAS 2020 (https://doi.org/10.1073/pnas.1919139117); 40 sampling locations, sediment depths 0.1-678 m; metadata in SI Tables 1 and 2 (PDF), the record's OTU-table link is empty. The record's `name` reads `subseafloor_arc` though the note says Bacteria.
- Use case: none; the paper describes composition and the environmental factors that explain it (Significance). Fit none.
- Siblings and duplicates: `subseafloor_arc` (Archaea, same samples and metadata): a second cut of one study that adds no distinct task (PROV-6) even if a target were found.
- Metric: none (a discovery study).
- Reject check (AI, 2026-10-22): stands. SEL-3 as for subseafloor_arc (same paper, Bacteria table of the same 299 samples, https://doi.org/10.1073/pnas.1919139117); also PROV-6, a second cut of one study adding no distinct task.
- Collection (AI, 2026-10-22): this record is one of the environmental-metabarcoding datasets of Zschaubitz et al. 2025, "A benchmark analysis of feature selection and machine learning methods for environmental metabarcoding datasets" (CSBJ, doi 10.1016/j.csbj.2025.04.017), whose Table 1 fixes one target per dataset (a measured environmental variable such as depth, pH, temperature or a nutrient). The collection picked targets "based on an expectation that there is a correlation" to benchmark feature selection, not for a decision, and the targets are measured at sampling anyway; so the reject holds under SEL-3 and SEL-8 (reject check 6).

The Bacteria counterpart of the subseafloor microbiome project (same PNAS source 10.1073/pnas.1919139117), again assembled by joining PDF-supplement metadata with an OTU table. Same concerns apply: many features, heavy wrangling, microbiome scientific-discovery framing, and an unclear/likely-small sample size with no defined deployable target. It also overlaps strongly with subseafloor_arc (Archaea), raising a near-duplicate question. A human must define the target, check sample size, and decide whether the Archaea/Bacteria variants are distinct enough to keep.

---

Subseafloor microbiome project, Bacteria; metadata source: SI Table 1&2 (PDF); otu table source:

## Reference

10.1073/pnas.1919139117
