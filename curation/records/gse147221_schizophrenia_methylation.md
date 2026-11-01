---
unique_name: gse147221_schizophrenia_methylation
name: GEO-GSE147221-Methylation-Schizophrenia (Schizophrenia DNA Methylation)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- Selection Bias
- Class-dependent Recording
tags:
- AI-Filled (Verify)
- Many features
collections:
- TabBench-Bio
original_source: Other
year: '2020'
domain: medical & healthcare
problem_type: Binary Classification
source_links:
- https://doi.org/10.7554/eLife.58430
- https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE147221
- https://arxiv.org/abs/2609.07441
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: schizophrenia cases against controls from 450K blood methylation (the Dublin cohort of Hannon et al. 2021); every case was drawn as EDTA whole blood and every control as a blood-donor buffy coat, so the class follows the sample type, and no clinical decision fits established cases.
- Source: GEO GSE147221 ("Blood DNA methylation profiles from schizophrenia cases and controls"), public 2020-12-31, the cohort "Dublin" of Hannon, Dempster, Mansell et al., "DNA methylation meta-analysis reveals cellular alterations in psychosis and markers of treatment-resistant schizophrenia", eLife 10:e58430, 2021-02-26 (https://doi.org/10.7554/eLife.58430, read on PMC8009672). As published: 720 samples ("364 schizophrenia cases, 349 controls and 7 fully methylated controls", overall design) in a processed-signal and a raw-signal CSV (the processed file holds 679 QC-passed samples, 348 cases and 331 controls, per the TabBench-Bio registry), with `status`, `consensus_diagnosis` (schizophrenia 297, schizoaffective disorder 56, a few others), `Sex` and `age`.
- Use case: none clear: schizophrenia is diagnosed by clinical interview, and the use the paper names is in first-episode psychosis ("may have utility as diagnostic and prognostic biomarkers in individuals with FEP", Conclusion), while this cohort holds established cases only (Table 1: no first-episode cases); fit approximate at best; regime grouped by BeadChip (the sample title's prefix, as TabBench-Bio does); the paper says samples were assigned to chips and plates to balance cases and controls (Methods, paraphrased).
- Siblings and duplicates: the record `schizo` is the unrelated PMLB/OpenML 466 table; GEO GSE207605 re-analyses this series with `gse40279_methylation_age` and `gse42861_rheumatoid_arthritis_methylation`; the meta-analysis's other cohorts are separate GEO series without records. External collections: TabBench-Bio (arXiv 2609.07441, Table 4); others not searched (web search used up).
- Better data: a candidate of the benchmark TabBench-Bio; no new search in this run.
- Papers and pages: Hannon et al. 2021 (above): cases "selected from the Irish Schizophrenia Genomics" consortium, controls "ascertained ... from the Irish GeneBank" (Methods, "Dublin samples").
- Metric: none found: the paper reports EWAS effects and meta-analysis p-values and no classifier ("may have utility as a molecular classifier" is a suggestion, Discussion), so the fallback `roc_auc` (MET-1, MET-8). Inputs: the chip for the split, from the sample title, never a feature.
- Risks for /add-dataset: the GEO sample fields put all 364 cases on "Blood - EDTA tube" and all 349 controls on "Blood - buffy coat", and DNA of 79 cases and of no control was extracted by phenol-chloroform: a recording route through the whole methylome (whole blood and buffy coat differ in cell make-up) that cannot be undone, so LEAK-15 likely retires the dataset (`Class-dependent Recording`, set here as a provisional concern; probes 7, 8 and 17 decide); cases and controls collected apart (`Selection Bias`); chronic, treated cases who smoke more (the paper's smoking score) put medication and smoking into the signal; signals normalised over all samples (wateRmelon dasen; LEAK-30, weak). The curator may prefer `No` now on LEAK-15.
- Priority: gap 0 (medical 44, binary not thin), use case 0 (none clear), source + (paper and GEO), shape 0 (679 rows), risk - (class-dependent sample type).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 679 x 30,000; target: status (348 cases / 331 controls).
- Why: Schizophrenia case vs control from whole-blood 450K methylation (one cohort of Hannon et al. 2021)
- Notes: CV grouped by assay plate. The existing schizo record is the unrelated PMLB/OpenML 466 table.
