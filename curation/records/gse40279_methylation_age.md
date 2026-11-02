---
unique_name: gse40279_methylation_age
name: GEO-GSE40279-Methylation-Age (Blood DNA Methylation Age)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
- Many features
- Non-IID (Grouped)
collections:
- TabBench-Bio
original_source: Other
year: '2012'
domain: biology & life sciences
required_split:
- Grouped (NON-IID)
problem_type: Regression
source_links:
- https://doi.org/10.1016/j.molcel.2012.10.016
- https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE40279
- https://arxiv.org/abs/2609.07441
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: chronological age from whole-blood 450K methylation of 656 people (Hannum et al. 2012), the cohort behind a standard epigenetic clock, published with a predictive model and a second cohort to validate it.
- Source: Hannum, Guinney, Zhao et al., "Genome-wide Methylation Profiles Reveal Quantitative Views of Human Aging Rates", Mol Cell 49(2):359-367, online 2012-11-21 (https://doi.org/10.1016/j.molcel.2012.10.016, read on PMC3780611); data GEO GSE40279, public 2012-11-21. As published: 656 samples x 473,034 probes of average beta values (series matrix; raw signal intensities and IDATs ship too), with per sample `age (y)` (19-101), `gender` (338 F, 318 M), `ethnicity` (426 Caucasian - European, 230 Hispanic - Mexican), `source` (UCSD 304, Utah 178, USC 139, Boston 35) and `plate` (9 plates). TabBench-Bio keeps 30,000 complete probes picked by probe-ID hash.
- Use case: a forensic lab estimating the age of an unknown blood donor, or a study reading the residual as an aging rate; the paper names both ("from health assessment and prevention of disease to forensic analysis", Conclusions); fit direct for age estimation from blood (forensic assays measure a few CpGs, the same kind of feature); regime grouped, because a clock is applied to samples run in other batches and cohorts: the paper validates on a second cohort ("two different cohorts (N1 = 482, N2 = 174)"; the GEO sites UCSD + Utah = 482 and USC + Boston = 174 match), and the plates differ in age (plate means 38.5 to 76.2 years; TabBench-Bio groups by plate).
- Siblings and duplicates: no other record holds GSE40279; `skull_bone_molecular_age` (skull bone, 6 CpGs and other markers, 190 people) is the same quantity from another tissue and source, a distinct task (PROV-7); GEO GSE207605 (Varshavsky et al. 2023, age from a few CpGs) re-analyses this series together with GSE42861 and GSE147221 (`gse42861_rheumatoid_arthritis_methylation`, `gse147221_schizophrenia_methylation`); `cns_tumor_methylation_classification` and `sarcoma_methylation_classification` are other 450K tasks. External collections: TabBench-Bio (arXiv 2609.07441, Table 4, "Blood DNA Methylation Age"); others not searched (web search used up).
- Better data: a candidate of the benchmark TabBench-Bio; no new search in this run.
- Papers and pages: Hannum et al. 2012 (above); Varshavsky et al. 2023 (GSE207605, PubMed 37751697) trains on it; TabBench-Bio registry entry `GEO-GSE40279-Methylation-Age`.
- Metric: Hannum reports two criteria side by side, "a correlation between age and predicted age of 96% and an error of 3.9 years" on the primary cohort and 91% and 4.9 years on the validation cohort (section "A predictive model for the aging methylome"), the error unnamed; no single deliberate one, so the fallback `rmse` in years (MET-5, MET-8); TabBench-Bio's RMSE is the benchmark's habit, not the source's. Inputs: the group (plate or site) for the split, a sample characteristic that ships, never a feature.
- Risks for /add-dataset: plate and site are confounded with age and ethnicity (UCSD mean age 70.0, Boston 52.0; USC 138 of 139 Hispanic), so the group comes from the use case (SPLIT-3) and under an IID split the batch signal can carry age; the series-matrix betas were processed over all samples (BeadStudio; LEAK-30, weak; rebuild from the IDATs if needed, PROV-13); 473k probes: width is no reason to drop features, and no subset chosen on the target (CLEAN-22, LEAK-31); ethnicity and sex ship as characteristics and are fair inputs.
- Priority: gap 0 (biology & life sciences 4, regression and grouped not thin), use case + (the paper names forensic age estimation), source + (paper and documented GEO characteristics), shape 0 (656 rows), risk 0.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 656 x 30,000 (of 473,034 probes); target: age (y).
- Why: Chronological age from whole-blood 450K methylation (Hannum epigenetic clock cohort)
- Notes: CV grouped by 9 assay plates (plate-age imbalance).
