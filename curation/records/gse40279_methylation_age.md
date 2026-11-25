---
unique_name: gse40279_methylation_age
name: GEO-GSE40279-Methylation-Age (Blood DNA Methylation Age)
checked_by:
- AI (UNVERIFIED)
data_foundry_status:
- WIP (Triage)
claimed_by: Andrej
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
- Many features
- Non-IID (Grouped)
- 'Samples: No Time Dimension'
- Experimental Results
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

**Screening (AI, 2026-11-25):** `TBD -> Yes`, priority 2: chronological age from whole-blood 450K methylation of 656 people (Hannum et al. 2012), the cohort behind a standard epigenetic clock, published with a predictive model validated on a second cohort; a larger blood cohort with age (GEO GSE55763, 2,664 people) is better data for the same task.
- Source: Hannum, Guinney, Zhao et al., "Genome-wide Methylation Profiles Reveal Quantitative Views of Human Aging Rates", Mol Cell 49(2):359-367, 2012 (https://doi.org/10.1016/j.molcel.2012.10.016, read on PMC3780611); data GEO GSE40279, public 2012-11-21. As published: 656 samples, one per person, x 473,034 probes of average beta (BeadStudio v3.2; the paper's QC subset of the 485,577 manifest probes), with `age (y)` (19-101), `gender`, `ethnicity`, `source` (UCSD 304, Utah 178, USC 139, Boston 35) and `plate` (9 plates). Files: series matrix, average betas, signal intensities (5.0 GB); `RAW.tar` holds only the manifests, no IDATs (size check of 2026-11-08 on PR #67). TabBench-Bio keeps 30,000 complete probes picked by probe-ID hash.
- Use case: a study reading the residual as an aging rate, or a lab estimating the age of a blood donor; the paper names both ("from health assessment and prevention of disease to forensic analysis", Conclusions); fit direct for age estimation from blood. Collection: volunteers' blood measured once by a study protocol, no date per sample, age a fixed fact at the draw (`Samples: No Time Dimension`, no target tag); one row per person. Type Experimental Results (SPLIT-34 rule 5; as `biogeographical_ancestry_prediction`).
- Split: leaf L-PLACE.groups (Grouped · `UnseenGroup` (groups)) because [EXP.meets] is another laboratory, site or cohort (a clock is applied to samples run elsewhere; the paper validates on a second cohort, "two different cohorts (N1 = 482, N2 = 174)", which the GEO sites UCSD + Utah and USC + Boston match), and [PLACE.several] is yes (4 sites, 9 plates); open: the group key, plate or site (the enough-groups check: 4 sites, 2 cohorts), and plate and site confounded with age and ethnicity (plate means 38.5 to 76.2 years; USC 138 of 139 Hispanic).
- Siblings and duplicates: no other record on this branch holds GSE40279; `skull_bone_molecular_age` is the same quantity from another tissue (PROV-7); GSE207605 re-analyses it with `gse42861_rheumatoid_arthritis_methylation` and `gse147221_schizophrenia_methylation`. On the open large-datasets PR (#67) this record carries Lennart's `Yes` (2026-11-08) and a review panel (2026-11-09), not on this branch. External collections: TabBench-Bio (Table 4).
- Better data: GEO GSE55763 (Lehne et al., Genome Biology 2015, Imperial College London, public 2015-01-22, https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE55763): 2,664 people, 2,711 peripheral-blood 450K arrays, `age` 23.7-75.0 and `gender`; 4 times the people and newer, a narrower age range (no one over 75, against 19 to 101 here); its record `gse55763_methylation_age` exists on PR #67, not on this branch.
- Papers and pages: Hannum et al. 2012 (above); Varshavsky et al. 2023 (GSE207605) trains on it; TabBench-Bio registry `GEO-GSE40279-Methylation-Age`.
- Metric: Hannum reports two criteria side by side, a correlation of 96% and "an error of 3.9 years" (section "A predictive model for the aging methylome"), the error unnamed; no single deliberate one, so the fallback `rmse` in years (MET-5, MET-8). Inputs: the group (plate or site) for the split, a sample characteristic that ships, never a feature.
- Risks for /add-dataset: plate and site confounded with age and ethnicity (the group from the use case, SPLIT-3); betas processed over all samples and missing cells KNN-imputed over all samples per the paper (LEAK-30, weak; the rebuild route is the signal-intensity file, PROV-13); 473k probes, no subset chosen on the target (CLEAN-22, LEAK-31); an ultra-wide table may need library changes to build.
- Priority: gap 0 (biology & life sciences 10, regression and grouped not thin), use case + (the paper names the uses), source + (paper and documented GEO characteristics), shape 0 (656 rows), risk - (better data found: GSE55763).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 656 x 30,000 (of 473,034 probes); target: age (y).
- Why: Chronological age from whole-blood 450K methylation (Hannum epigenetic clock cohort)
- Notes: CV grouped by 9 assay plates (plate-age imbalance).
