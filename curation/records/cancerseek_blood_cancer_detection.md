---
unique_name: cancerseek_blood_cancer_detection
name: 'CancerSEEK: detection and localization of surgically resectable cancers with a multi-analyte blood test'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
decision_markers:
- Selection Bias
tags:
- AI-Filled (Verify)
original_source: Other
year: '2018'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
source_links:
- https://doi.org/10.1126/science.aar3247
- https://pmc.ncbi.nlm.nih.gov/articles/PMC6080308/
- https://pmc.ncbi.nlm.nih.gov/articles/instance/6080308/bin/NIHMS982921-supplement-Tables_S1_to_S11.xlsx
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: 1,817 people (1,005 with stage I-III cancer of eight types, 812 healthy) with plasma protein levels and ctDNA mutation results in open supplementary tables of a Science paper; a real blood-test task, from a case-control cohort.
- Source: Cohen et al., "Detection and localization of surgically resectable cancers with a multi-analyte blood test", Science 359(6378):926-930, 2018 (doi 10.1126/science.aar3247; author manuscript PMC6080308), Johns Hopkins. As published: Tables S1-S11 in one open xlsx (PMC supplement); the complete per-sample data are in "tables S5 and S6" (plasma mutations, protein levels), S4 the clinical characteristics, S8 the tumour-type predictions; the test combines eight proteins (CA-125, CEA, CA19-9, PRL, HGF, OPN, MPO, TIMP-1) with mutations at 1,933 genomic positions. The sheets were not opened.
- Use case: a screening programme decides from one blood draw whether a person needs a diagnostic work-up for cancer, and for which organ; fit approximate: the patients "had been diagnosed", "most diagnosed on the basis of symptoms of disease" (Limitations), against healthy controls, not a screened population (`Selection Bias`, USE-8). Regime IID: one sample per person.
- Siblings and duplicates: `arcene` (`No`, Missing source information, Data Quality Issue) and `genomic_data_for_cancer` (`No`, AHDS), for which the run proposed it; no other liquid-biopsy record (grep for cancerseek, aar3247, ctdna, cfdna). External collections: none found.
- Better data: from the run's search, found as better data for `arcene` and `genomic_data_for_cancer`; no further search this round.
- Papers and pages: Cohen et al. 2018 (above).
- Metric: sensitivity at a specificity above 99% ("The red point on the curve indicates the test's average performance (62%) at >99% specificity", Fig. 2A), estimated over "10 iterations of 10-fold cross-validations": a deliberate operating point for a screening test (MET-5, MET-7), but no standard metric of the library: a custom metric (MET-13) or the fallback `roc_auc` with the paper's point in the notes, the curator's call.
- Risks for /add-dataset: case-control design with symptomatic cases (`Selection Bias`); how the mutation score is built, and whether it uses this cohort's control plasmas as reference outside the cross-validation (LEAK-27, in the supplementary methods, not read); protein values at detection limits (CLEAN); join S5 and S6 by sample; stage and tumour type are outcomes, not inputs (LEAK-10); which proteins ship (the final eight or all measured).
- Priority: gap 0 (medical and binary are not thin), use case + (the paper names early detection by a blood test), source + (a Science paper with open per-sample tables), shape + (1,817 people, protein and mutation measures), risk - (case-control selection; a mutation score that may use the controls).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `arcene`, `genomic_data_for_cancer`.
- as published: 1,817 people (1,005 with non-metastatic stage I-III cancer of 8 types: ovary, liver, stomach, pancreas, esophagus, colorectum, lung, breast; 812 healthy controls); per-sample plasma protein levels ...; target: cancer vs healthy (binary); tumour type as a second target; access: open.
- Why: Arcene is cancer vs normal from serum mass spectra (the NCI ovarian and prostate SELDI sets). CancerSEEK is the same task, detecting cancer from blood protein measurements, with named, calibrated analytes in place of spectra. | genomic_data_for_cancer is simulated ('Data collected from simulated genomic ...
- Adds: About 9 times the units of arcene (200 rows) and the NCI originals, newer, 8 cancer types and real analyte concentrations, with no added random probes or whole-set preprocessing. Caveats: a case-control design (Selection Bias), and the protein assay thresholds were tuned on this cohort. | real, traceable, ...
