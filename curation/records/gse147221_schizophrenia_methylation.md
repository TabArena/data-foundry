---
unique_name: gse147221_schizophrenia_methylation
name: GEO-GSE147221-Methylation-Schizophrenia (Schizophrenia DNA Methylation)
checked_by:
- AI (UNVERIFIED)
data_foundry_status:
- WIP (Triage)
claimed_by: Andrej
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- Selection Bias
- Class-dependent Recording
tags:
- AI-Filled (Verify)
- Many features
- 'Samples: Over Time'
- 'Time: Lost'
- Clinical Study
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

**Screening (AI, 2026-11-25):** `TBD -> 2nd Tier`, priority 1: schizophrenia cases against controls from 450K blood methylation (the Dublin cohort of Hannon et al. 2021); the GEO series records every case as an EDTA whole-blood draw and every control as a blood-donor buffy coat, so the sample type follows the class one to one, and no decision fits established, treated cases.
- Source: GEO GSE147221 ("Blood DNA methylation profiles from schizophrenia cases and controls"), public 2020-12-31, the cohort "Dublin" of Hannon, Dempster, Mansell et al., "DNA methylation meta-analysis reveals cellular alterations in psychosis and markers of treatment-resistant schizophrenia", eLife 10:e58430, 2021 (https://doi.org/10.7554/eLife.58430, read on PMC8009672). As published (series matrix characteristics, re-read 2026-11-25): 720 samples, 364 cases, 349 controls and 7 fully methylated controls, with `Sex`, `age`, `status` and `consensus_diagnosis` (schizophrenia 297, schizoaffective disorder 56, a few others); 34 samples flagged "excluded from the final analysis due to low quality" leave 348 cases and 331 controls (the 679 of TabBench-Bio's registry). Processed and raw signal CSVs; the sample title carries the BeadChip barcode (60 chips).
- Use case: none clear. Schizophrenia is diagnosed by clinical interview; the paper's named use is in first-episode psychosis ("may have utility as diagnostic and prognostic biomarkers in individuals with FEP", Conclusion), while this cohort holds established cases only; fit None to approximate (USE-1, USE-8). Collection: cases "selected from the Irish Schizophrenia Genomics" consortium and controls "ascertained ... from the Irish GeneBank" (Methods), recruited over time with no date per sample (`Samples: Over Time`, `Time: Lost`; the chip barcode orders the lab run, not recruitment); the diagnosis exists when the blood is drawn (no target tag); one sample per person. Type Clinical Study (SPLIT-34 rule 5).
- Split: leaf L-FORCED.random (Random · `ForcedIIDFromTemporal`) because the type's question [CLI.meets] has no stated use case and, read as a clinic's later patients, [CLI.dated] is no, [ORDER.order] finds no order, [FORCED.test] can measure nothing, and [FORCED.reason], [FORCED.risk] are a person's (answered no) and [FORCED.groups] has no repeated unit or period; open: the use case itself, and whether the BeadChip should group as a batch key (TabBench-Bio groups by chip).
- Siblings and duplicates: `schizo` is the unrelated PMLB/OpenML 466 table; GEO GSE207605 re-analyses this series with `gse40279_methylation_age` and `gse42861_rheumatoid_arthritis_methylation`; the meta-analysis's other cohorts (London, Aberdeen and others) are separate GEO series without records. Precedent for a class recorded through its own route: `prostate_cancer_detection` (retired, LEAK-15, no batch id survives); `biogeographical_ancestry_prediction` (a class from a separate assay dropped, LEAK-14). External collections: TabBench-Bio (arXiv 2609.07441, Table 4).
- Better data: none found (quick look: the meta-analysis's other cohorts are separate series of the same design, none larger with cases and controls drawn alike; the 2026-10-31 run searched no further).
- Papers and pages: Hannon et al. 2021 (above); https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE147221.
- Metric: none found: the paper reports EWAS effects and meta-analysis p-values and no classifier (read on PMC8009672), so the fallback `roc_auc` (MET-1, MET-8). Inputs: the chip barcode, if a batch group is chosen, from the sample title, never a feature.
- Risks for /add-dataset: GEO `source_name`: "Blood - EDTA tube" on all 364 cases, "Blood - buffy coat" on all 349 controls, and the extraction protocol "Phenol-Chloroform" on 79 cases and no control: a recording route through the whole methylome (whole blood and buffy coat differ in cell make-up) that no column can undo, so LEAK-15 likely retires it (`Class-dependent Recording`, probes 7, 8 and 17 decide; part 3, so no fast reject at screening); cases and controls collected apart (`Selection Bias`, USE-8); chronic, treated cases who smoke more put medication and smoking into the signal; signals normalised over all samples (wateRmelon dasen; LEAK-30, weak). Options for the curator: (a) `No` now on LEAK-15 with the GEO fields as the evidence; (b) keep it at 2nd Tier until a probe measures the route; (c) look for another cohort of the meta-analysis whose cases and controls share one sample type.
- Priority: gap 0 (medical not thin, binary not thin), use case 0 (none clear), source + (paper and GEO), shape 0 (679 rows), risk - (class-dependent sample type).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 679 x 30,000; target: status (348 cases / 331 controls).
- Why: Schizophrenia case vs control from whole-blood 450K methylation (one cohort of Hannon et al. 2021)
- Notes: CV grouped by assay plate. The existing schizo record is the unrelated PMLB/OpenML 466 table.
