---
unique_name: gse55763_methylation_age
name: 'GSE55763: whole-blood DNA methylation of 2,664 people with age (Lehne et al. 2015)'
checked_by:
- AI (UNVERIFIED)
data_foundry_status:
- WIP (Triage)
claimed_by: Lennart
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
- Many features
original_source: Other
year: '2015'
domain: biology & life sciences
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE55763
- https://doi.org/10.1186/s13059-015-0600-x
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-11-08):** `TBD -> Yes`, priority 3: chronological age from peripheral-blood 450K methylation of 2,664 people of the LOLIPOP study (Lehne et al. 2015, Imperial College London), the same task as `gse40279_methylation_age` with four times the people, a narrower age range (23.7 to 75.0) and betas normalised over the cohort; the curator picks which one enters.
- Source: Lehne, Drong, Loh, ..., Chambers, "A coherent approach for analysis of the Illumina HumanMethylation450 BeadChip improves data quality and performance in epigenome-wide association studies", Genome Biology 16:37, 2015 (doi 10.1186/s13059-015-0600-x, PMC4365767, read through the PMC text); GEO GSE55763 (Imperial College London, submitted 2014-03-10, public 2015-01-22, platform GPL13534). The paper: "a population study of type 2 diabetes comprising 2,687 samples; and a technical replication dataset comprising 36 samples measured in duplicate", from the London Life Sciences Prospective Population (LOLIPOP) study; 22 samples failed QC and one more fell below a 98% call rate at the paper's detection threshold P < 10^-16, "leaving 2,664 samples". As published (series matrix, read): 2,711 arrays with `dataset` (population study 2,639, technical replication 47, both 25), `gender` (M 1,840, F 871), `age` (23.7 to 75.0, mean 51.0) and tissue peripheral blood; the sample title holds the chip barcode and position (`7786915023_R02C02`). The values sit only in supplementary files: `GSE55763_normalized_betas.txt.gz` (9.7 GB; 5,423 columns, the probe id and then a beta and a detection p-value per array), `GSE55763_unmethylated_methylated_signal_intensities.txt.gz` (5.7 GB) and `GSE55763_RAW.tar` (183 MB), which by its `filelist.txt` holds only the 450K manifests and BPM files, no IDATs. The probe count is not stated; the compressed size per row puts it near the full 485k array (estimate).
- The task's table: one row per person, the 2,664 population-study arrays x the probes of the beta file (not counted, about 485k) + `gender`; target age in years; the chip from the sample title as the group (SPLIT-24, a batch id from the source). Access: open on GEO, no login, no licence stated; 9.7 GB for the betas.
- Use case: as for `gse40279_methylation_age`, a forensic laboratory estimating an unknown blood donor's age, or a study reading the residual as an ageing rate. Lehne et al. use the data for association studies and predict no age, so the use case comes from the task (Hannum et al. 2012 name it), not from this source. Fit direct for age estimation from blood. Regime grouped by chip, as the sibling groups by plate.
- Siblings and duplicates: `gse40279_methylation_age` (`Yes`, Lennart, 2026-11-08) is the same task from another source and cohort, so each keeps its record (PROV-4). Against it: 2,664 people against 656; ages 23.7 to 75.0 (mean 51.0) against 19 to 101; arrays 1,840 men and 871 women against 318 and 338; no ethnicity on GEO here (LOLIPOP recruited Indian Asians and Europeans, from the cohort's descriptions, not read) against Caucasian and Hispanic given there; both 450K (GPL13534) blood; here betas quantile-normalised over the cohort with a detection p-value per value, there BeadStudio averages with KNN imputation over 473,034 probes kept by QC; neither ships IDATs and both ship signal intensities for a rebuild; groups by chip here, by plate and site there. `skull_bone_molecular_age` predicts age from bone; `gse50660_smoking_methylation`, `gse42861_rheumatoid_arthritis_methylation` and `gse147221_schizophrenia_methylation` are 450K blood series with other targets. External collections: none found.
- Better data: found as better data for `gse40279_methylation_age` (the size check of 2026-11-08); no further search.
- Papers and pages: Lehne et al. 2015 (above); the series also cites PMID 28002404 (not read).
- Metric: Lehne et al. predict no age, so there is no source metric; the fallback `rmse` in years, as for `gse40279_methylation_age` (MET-1, MET-8). Inputs: the chip, a split column and never a feature.
- Risks for /add-dataset: the betas were normalised over all arrays (quantile normalisation of the intensities, the paper's CPACOR pipeline: LEAK-30, weak; rebuild from the intensities if needed, PROV-13); the cohort is "a population study of type 2 diabetes", so whether people were selected on diabetes is to be read (`Selection Bias` if so); no one is over 75 and two thirds of the arrays are men; keep the 2,664 population-study arrays and drop the replication-only ones (one array per person); about 485k x 2,711 values in a 9.7 GB file; width is no reason to drop probes (CLEAN-22).
- Priority: gap 0 (biology & life sciences, regression and grouped covered), use case 0 (not named by this source), source + (journal paper and GEO characteristics), shape + (2,664 people, about 485k probes, a chip grouping), risk 0 (a weak normalisation leak, like the sibling's imputation).

Found as better data for `gse40279_methylation_age` by the size check of 2026-11-08.
