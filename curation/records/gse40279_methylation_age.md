---
unique_name: gse40279_methylation_age
name: GEO-GSE40279-Methylation-Age (Blood DNA Methylation Age)
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
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
v2_path: datasets/_dev/tabarena-v0pt2/gse40279_methylation_age/dataset.py
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

**Assessment (AI, 2026-11-08):** size check for the large-datasets review: 656 people x 473,034 CpG probes plus sex and ethnicity, age in years; the task stands, but a larger blood cohort with age (GEO GSE55763, 2,664 people) is better data for the same task, so priority 2 is proposed.
- As published: GEO GSE40279 (public 2012-11-21, https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE40279): 656 whole-blood samples, one per person (the abstract: "the whole blood of 656 human individuals"), each with 473,034 probes (`Sample_data_row_count`) of average beta from "BeadStudio software v3.2". Files (https://ftp.ncbi.nlm.nih.gov/geo/series/GSE40nnn/GSE40279/): series matrix 1.2 GB gz; `GSE40279_average_beta.txt.gz` 1.1 GB (also split into four files of about 300 MB); `GSE40279_signal_intensities.txt.gz` 5.0 GB; `GSE40279_sample_key.txt.gz` 4.5 KB; `GSE40279_RAW.tar` 183 MB, which by its `filelist.txt` holds only the 450K manifest and BPM files. There are no IDATs, so the screening block's "IDATs ship too" is wrong. Per-sample characteristics: `age (y)`, `source`, `plate`, `gender`, `ethnicity`, `tissue`. One table and no join. The 473,034 rows are the paper's QC subset: 485,577 manifest probes, less the 11,648 on X and Y (11,232 + 416, counted in the GPL13534 v1.1 manifest), less the 65 SNP (rs) probes, less the "830 markers ... removed as they had greater than 5% missing values" (Experimental Procedures), is exactly 473,034 (computed). The paper set values with "a detection p-value greater than 0.01" to missing and imputed them "with the KNN approach (10 nearest markers)". The first 4,447 probes of the series matrix (a streamed preview) have no missing cell, so the deposit probably holds the imputed values. The paper also removed one sample for missing values and 24 PCA outliers; GEO's 656 equals the paper's analysed count.
- The task's table: 656 rows (one per person, so no grouping by person) x 473,034 probes + `gender` + `ethnicity` = 473,036 inputs, with `plate` or `source` as the group and never as a feature (stated: GEO row and sample counts). The source names no narrower QC subset. TabBench-Bio's 30,000 probes picked by hash is that benchmark's cut, not a QC.
- Access: open on GEO, no login; the series states no licence. 1.2 GB for the series matrix. Without IDATs, the only per-sample rebuild is from the 5.0 GB signal-intensity file.
- Changes the call: (1) Better data for the same task: GEO GSE55763 (Lehne et al., Genome Biology 2015, Imperial College London; public 2015-01-22; https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE55763): "2,664 individuals, and 36 samples measured in duplicate", 2,711 peripheral-blood 450K arrays with `age` (23.7 to 75.0, counted in the series matrix) and `gender`. Normalised betas 9.7 GB (normalised over the cohort, LEAK-30); signal intensities 5.7 GB; `RAW.tar` 183 MB, the same size as here, so probably manifests only (not opened). It has 4 times the people and is newer, but its ages are narrower (no one over 75, against 19 to 101 here). It has no record. By the screening factors, better data found takes one point off, so priority 2 is proposed (from 3), and the curator weighs the age range. (2) The rebuild route for LEAK-30 is the signal-intensity file, not IDATs (PROV-13). The KNN imputation drew on all samples for the imputed cells, a weak transductive leak (LEAK-30): keep it with a note or rebuild. The grouping by plate stands.
- Not checked: the missing cells over all 473,034 probes (the 1.2 GB matrix was only previewed), so whether the deposit holds imputed values is an inference; the column layout of the signal-intensity file; GSE55763's paper and its characteristics beyond age, sex and the duplicate flags.

CC (2026-11-08, Lennart): accepted for adding (`Yes`) in the screening review of the large candidates (most rows, most features).

**Assessment (AI, 2026-11-08):** better data for the same task was found by the size check, GSE55763 (Lehne et al. 2015, Imperial College London: 2,664 people, blood 450K arrays, ages 23.7-75.0); per screen-candidates "Better data" it is screened as its own record, and the curator picks which one enters once both are known. This record keeps its verdict.

**Assessment (AI, 2026-11-09):** review panel (full): ship after changes (made: notes on the plate-constant ethnicity, the use case led by the aging study with forensic estimation second and approximate, the rmse reason citing Fig. 7A, the 18 distinct partitions, the ultra-wide label); the build waits on the library's parquet read limits; rebuttal round skipped (briefs converged); disputed: keep `ethnicity` (USE-6, USE-3); for the curator: issues 1-3. Priority 3: gap 0, use case +, source +, shape 0, risk − (a larger sibling cohort, gse55763, 9 plates only, an ultra-wide table that needs a library change to build).
