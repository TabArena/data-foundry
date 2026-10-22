---
unique_name: bedford_basin_v6v8
name: bedford_basin_V6V8
checked_by:
- AI (UNVERIFIED)
data_foundry_status:
- 'DF: Suspended'
suggestion: 'No'
decision_markers:
- No Good Target  / Scientific Discovery
tags:
- '?'
- AI-Filled (Verify)
collections:
- New (BeyondArena)
domain: biology & life sciences
problem_type: Other
original_data_state: Other
source_row: 794
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`No Good Target  / Scientific Discovery`, SEL-3): the V6-V8 16S table of the same Bedford Basin study as `bedford_basin_v4v5`, published for a descriptive study of community dynamics, with no target named.
- Source: Robicheau et al., ISME Communications 2022, doi 10.1038/s43705-022-00119-2 (SI table of the V6-V8 amplicon, which the paper also used for the Scotian Shelf samples); metadata from the Bedford Basin Monitoring Program.
- Use case: none; the study describes seasonal and interannual shifts and indicator taxa, without a prediction (USE-1, USE-2).
- Siblings and duplicates: a second amplicon of the same samples as `bedford_basin_v4v5` (PROV-6; it would be a duplicate even if a target were defined). `DF: Suspended` kept.
- Metric: none.
- Reject check (AI, 2026-10-22): stands. SEL-3 as bedford_basin_v4v5 (same paper, https://academic.oup.com/ismecommun/article/7461061); also the second primer set on the same weekly samples, so a cut without a distinct task (PROV-6).
- Collection (AI, 2026-10-22): this record is one of the environmental-metabarcoding datasets of Zschaubitz et al. 2025, "A benchmark analysis of feature selection and machine learning methods for environmental metabarcoding datasets" (CSBJ, doi 10.1016/j.csbj.2025.04.017), whose Table 1 fixes one target per dataset (a measured environmental variable such as depth, pH, temperature or a nutrient). The collection picked targets "based on an expectation that there is a correlation" to benchmark feature selection, not for a decision, and the targets are measured at sampling anyway; so the reject holds under SEL-3 and SEL-8 (reject check 6).

Same Bedford Basin Monitoring Program microbiome dataset as the V4V5 record but for the V6V8 amplicon region (OTU table from supplementary information); also marked 'DF: Suspended' and tagged '?'. As an OTU abundance matrix for scientific monitoring/discovery it has no clear predictive target and is not representative of tabular ML. Excluded on the same grounds as its V4V5 counterpart (and it is effectively a sister table). A human can confirm the suspension and that V4V5/V6V8 are not meant to be merged.

---

Multiyear monitoring in the Bedford Basin Monitoring Program; metadata source: https://www.bio.gc.ca/science/monitoring-monitorage/bbmp-pobb/bbmp-pobb-en.php (TODO); otu table source: SI Table 3

## Reference

10.1038/s43705-022-00119-2
