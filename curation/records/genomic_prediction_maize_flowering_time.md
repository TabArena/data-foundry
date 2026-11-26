---
unique_name: genomic_prediction_maize_flowering_time
name: gp-maize-FT (Maize Flowering Time Genomic Prediction)
checked_by:
- AI (UNVERIFIED)
data_foundry_status:
- WIP (Triage)
claimed_by: Andrej
suggestion: TBD -> 2nd Tier
priority: 2
tags:
- AI-Filled (Verify)
- Many features
- Tiny Data
- 'Samples: No Time Dimension'
- Experimental Results
collections:
- TabBench-Bio
original_source: Other
year: '2019'
domain: biology & life sciences
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.1534/g3.119.400498
- https://doi.org/10.5061/dryad.xksn02vb9
- https://arxiv.org/abs/2609.07441
- https://zenodo.org/records/4980429
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-11-25):** `TBD -> 2nd Tier`, priority 2: flowering time of 391 maize inbred lines from 244,781 SNP markers, genomic selection as a plain regression from a documented CC0 release; secondary because 391 rows against a quarter of a million markers is a very thin shape, the target ships without its natural scale, and the maize NAM population holds the same trait for about 5,000 lines.
- Source: the maize pan-genome population, phenotypes from Hansey et al. 2011 and genotypes from Hirsch et al. 2014, "maize trait values were averaged over replicate plots" (the release's README, re-read 2026-11-25); compiled by Azodi CB et al., "Benchmarking Parametric and Machine Learning Models for Genomic Prediction of Complex Traits", G3 9(11):3691-3702, 2019 (doi 10.1534/g3.119.400498), who compiled 18 traits of six plant species and deposited them on Dryad (doi 10.5061/dryad.xksn02vb9), mirrored as Zenodo record 4980429 (CC0, deposited 2019-10-04). As published: `maize_pheno.csv` 391 lines x 3 traits (HT, FT, YLD; header and row count re-read 2026-11-25) and `maize_geno.csv` (217.2 MB) 391 lines x 244,781 markers coded -1/0/1 (counted on the preview of 2026-10-31), joined on the line id, plus `maize_CVFs.csv` with the authors' fold assignments. The README says "leaving 332,178 markers for the maize analysis", which the deposited file does not match — a discrepancy to clear up. Target `FT`, flowering time.
- Use case: a breeder, before the field season, decides which lines to advance from the genotype alone (genomic selection): predicting traits from genotypes "is accelerating the speed of crop and livestock breeding" (Introduction), and the paper closes by recommending that "breeders test the performance of multiple algorithms on their training population"; fit direct within the panel, approximate for new germplasm; collection `Samples: No Time Dimension`: one panel of inbred lines grown in the same replicated field trials, each line's trait averaged over its plots, the genotype fixed before the season and the trait read at flowering; the release dates neither lines nor plots; type `Experimental Results` (a closed set of lines measured by one study protocol, SPLIT-34).
- Split: leaf L-EXP.random (Random · `Timeless`) because [EXP.meets] a new line of the kinds the panel contains (genomic selection predicts the unphenotyped lines of the breeding population), [EXP.repeated] no (one averaged row per line); open: whether the use case meets a germplasm group the panel lacks (a heterotic group or subpopulation, then [EXP.kind-key] and L-EXP.kind): the release has no group column and the line ids name no family, so the kind would have to come from a published assignment (Hansey et al. 2011), not from clustering the markers; duplicate marker profiles to check before splitting (LEAK-19). Azodi's random 80/20 holdout over lines, replicated 10 times, is a habit, not a choice for the use case (SPLIT-5).
- Siblings and duplicates: `genomic_prediction_rice_flowering_time`, `genomic_prediction_soy_yield` and `genomic_prediction_switchgrass_height` are the other three cuts of the same Azodi release — different species, panels and first publications, so distinct tasks (PROV-7) rather than duplicates; the other two traits of this species (HT, YLD) are further cuts that would be duplicates without a distinct task (PROV-6), and the release also holds sorghum and spruce. No other maize or genomic-prediction record (grep on "Azodi", "genomic prediction", "genomic selection", "maize", "NAM", "Panzea", "dryad.xksn02vb9", 2026-11-25); `raman_wheat_lines` is a spectroscopy task, `cy_bench_subnational_crop_yield` and `digital_green_crop_yield_estimate_challenge` are agronomic yield tasks without genotypes. External collections: TabBench-Bio (`gp-maize-FT`).
- Better data: the maize Nested Association Mapping (NAM) population, Buckler et al., "The genetic architecture of maize flowering time", Science 325:714-718, 2009 (https://doi.org/10.1126/science.1174276), now the record `maize_nam_flowering_time` (`TBD -> Yes`, priority 4). Its archive was downloaded and counted on 2026-11-26: 4,699 recombinant inbred lines of 25 families crossed to B73, twelve times the lines here, with 1,106 imputed linkage-map markers, days to anthesis as a BLUP across eight environments in its natural unit of days (58.40 to 121.21), the families as a group key, and the raw plot values shipped beside the line values. It is from another population, so it is its own record and no duplicate (PROV-4), and it does not settle this record's own verdict.
- Papers and pages: Azodi et al. 2019 (G3, https://academic.oup.com/g3journal/article/9/11/3691/6026746), its code at github.com/ShiuLab/Manuscript_Code/tree/master/2019_GP_Comparison, the Zenodo mirror https://zenodo.org/records/4980429; Hansey et al. 2011 and Hirsch et al. 2014 for the panel (not read); TabBench-Bio (arXiv 2609.07441), Table 4 row gp-maize-FT.
- Metric: Pearson's correlation over the test lines, the source's own ranked criterion — the Methods say it "was used as it is the standard metric for GP performance", while the hyper-parameter grid search used MSE; one deliberate choice of the field (MET-5), and what a breeder reads (the ranking of lines). TabBench-Bio scores this table with its own "RMSE is the primary regression metric" (Sec. 3.5), a benchmark convention. The metric library carries correlations (MET-13), so the source's metric can ship; `rmse`, the fallback, would also need the natural scale (MET-3), which this release does not ship. Inputs: none.
- Risks for /add-dataset: the trait columns are standardized (mean 0, sd 1 on the preview of 2026-10-31; negative values such as -1.17 in the rows re-read 2026-11-25), while the README says "Phenotype values were normalized between 0 and 1" — either way the natural units are lost, and a repair from the original publication (Hansey et al. 2011) is the first question (PROV-8, PROV-13). Two tables joined on the line id. Marker calls were "obtained in the form of biallelic SNPs with missing marker data already dropped or imputed by the original authors" and recoded to -1/0/1 (README), an imputation done at the source that we cannot check (LEAK-30 at most). 244,781 columns for 391 rows is the extreme of p >> n; width is no reason to drop markers (CLEAN-22), and any filter fit on the data is fit inside the training side only (LEAK-27).
- Priority: gap 0 (biology & life sciences has 10 accepted datasets, thin at 6 or fewer; regression and the IID regime are not thin), use case + (the paper names the breeder and the selection decision), source + (a peer-reviewed paper, a README and CC0 data), shape 0 (391 lines), risk - (the target ships without its natural scale; better data found, the NAM population).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 391 x 244,781; target: FT.
- Why: Flowering time of maize lines from SNP genotypes (genomic prediction for breeding)
- Notes: Azodi et al. 2019 compiled 18 traits of 6 species (Dryad, mirrored on Zenodo 4980429, CC0); the underlying line panels have their own earlier publications, cited in Azodi et al.

**Assessment (AI, 2026-11-26):** the better data named in the screening now has a record, `maize_nam_flowering_time`, screened from the archive's own files rather than from a page: 4,699 lines x 1,106 markers, the target in days and not standardized, and 25 families to group on. This record's verdict and priority are unchanged; what it adds is that the alternative is now checked and no longer a lead.
