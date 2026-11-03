---
unique_name: genomic_prediction_maize_flowering_time
name: gp-maize-FT (Maize Flowering Time Genomic Prediction)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
tags:
- AI-Filled (Verify)
- Many features
- Tiny Data
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

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: flowering time of 391 maize lines from 244,781 SNP markers, genomic selection as a plain regression from a documented CC0 release; secondary because 391 rows against a quarter of a million markers is a very thin shape.
- Source: the maize pan-genome population, phenotypes from Hansey et al. 2011 and genotypes from Hirsch et al. 2014, "maize trait values were averaged over replicate plots" (the release's README); compiled by Azodi CB et al., "Benchmarking Parametric and Machine Learning Models for Genomic Prediction of Complex Traits", G3 9(11):3691-3702, 2019 (doi 10.1534/g3.119.400498), who compiled 18 traits of six plant species and deposited them on Dryad (doi 10.5061/dryad.xksn02vb9), mirrored as Zenodo record 4980429 (CC0, deposited 2019-10-04). As published: `maize_pheno.csv` 391 lines x 3 traits (HT, FT, YLD) and `maize_geno.csv` 391 lines x 244,781 markers coded -1/0/1, joined on the line id, plus `maize_CVFs.csv` with the authors' fold assignments (`cv_1`...). Counted on a preview of the files, 2026-10-31: 391 phenotype rows, 244,781 marker columns, values in {-1, 0, 1}. The paper says "leaving 332,178 markers for the maize analysis", which the deposited file does not match — a discrepancy to clear up. Target `FT`, flowering time.
- Use case: a breeder, before the field season, decides which lines to advance from the genotype alone (genomic selection): predicting traits from genotypes "is accelerating the speed of crop and livestock breeding" (Introduction), and the paper closes by recommending that "breeders test the performance of multiple algorithms on their training population". Fit direct within the panel, approximate for new germplasm. Regime: the source used "an 80/20 training/testing approach ... where 20% of the lines were held out", replicated 10 times, a random split over lines (SPLIT-5: a prescribed split is a claim); the lines of a diversity panel are related, so a grouped split is the harder question the use case may ask for (SPLIT-31, USE-10).
- Siblings and duplicates: `genomic_prediction_rice_flowering_time`, `genomic_prediction_soy_yield` and `genomic_prediction_switchgrass_height` are the other three cuts of the same Azodi release — different species, panels and first publications, so distinct tasks (PROV-7) rather than duplicates; the other two traits of this species (HT, YLD) are further cuts that would be duplicates without a distinct task (PROV-6), and the release also holds sorghum and spruce. No other maize or genomic-prediction record (grep on "Azodi", "genomic prediction", "maize", "dryad.xksn02vb9"); `raman_wheat_lines` is a spectroscopy task, `cy_bench_subnational_crop_yield` and `digital_green_crop_yield_estimate_challenge` are agronomic yield tasks without genotypes. External collections: TabBench-Bio (`gp-maize-FT`).
- Better data: a candidate of the benchmark TabBench-Bio; no new search this round.
- Papers and pages: Azodi et al. 2019 (G3, https://academic.oup.com/g3journal/article/9/11/3691/6026746), its code at github.com/ShiuLab/Manuscript_Code/tree/master/2019_GP_Comparison, the Zenodo mirror https://zenodo.org/records/4980429; TabBench-Bio (arXiv 2609.07441), Table 4 row gp-maize-FT.
- Metric: Pearson's correlation, the source's own ranked criterion — the Methods say it "was used as it is the standard metric for GP performance", while the hyper-parameter grid search used MSE; that is one deliberate choice of the field (MET-5), and it is what a breeder reads (the ranking of lines). TabBench-Bio scores this table with its own "RMSE is the primary regression metric" (Sec. 3.5). If the spec carries no correlation metric, `rmse` is the fallback (MET-8), but then MET-3 needs the natural scale, which this release does not ship. Inputs: none.
- Risks for /add-dataset: the trait columns are standardized (mean 0, sd 1 on a preview of the files, 2026-10-31), while the release's README says "Phenotype values were normalized between 0 and 1" — either way the natural units are lost, so the metric is not on the scale the task means (MET-3) and a repair from the original publication is the first question (PROV-13). The genotype and phenotype CSVs join on the line id (two tables). Marker calls were "obtained in the form of biallelic SNPs with missing marker data already dropped or imputed by the original authors" and recoded to -1/0/1 (README), an imputation done at the source that we cannot check (LEAK-30 at most). All columns are numeric marker codes, no mixed types. 244,781 columns for 391 rows is the extreme of p >> n: the benchmark caps features at 2k, 10k, 25k or full, and any cap we use has to be fit inside the training side only (LEAK-27).
- Priority: gap 0 (biology & life sciences has 4 accepted datasets, just above thin; regression is not thin), use case + (the paper names the breeder and the selection decision), source + (a peer-reviewed paper, a README and CC0 data), shape 0 (391 lines), risk - (the target ships without its natural scale, and the four cuts overlap one release).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 391 x 244,781; target: FT.
- Why: Flowering time of maize lines from SNP genotypes (genomic prediction for breeding)
- Notes: Azodi et al. 2019 compiled 18 traits of 6 species (Dryad, mirrored on Zenodo 4980429, CC0); the underlying line panels have their own earlier publications, cited in Azodi et al.
