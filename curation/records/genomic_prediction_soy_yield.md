---
unique_name: genomic_prediction_soy_yield
name: gp-soy-YLD (Soybean Yield Genomic Prediction)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
- Many features
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

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: yield of 5,014 soybean lines from 4,234 SNP markers — genomic selection as a plain regression, and the one of the four Azodi cuts with a comfortable shape.
- Source: the SoyNAM population, "recombinant inbred lines (RILs) derived from 40 biparental populations" (Xavier et al. 2016, quoted in the release's README); compiled by Azodi CB et al., "Benchmarking Parametric and Machine Learning Models for Genomic Prediction of Complex Traits", G3 9(11):3691-3702, 2019 (doi 10.1534/g3.119.400498), who compiled 18 traits of six plant species and deposited them on Dryad (doi 10.5061/dryad.xksn02vb9), mirrored as Zenodo record 4980429 (CC0, deposited 2019-10-04). As published: `soy_pheno.csv` 5,014 lines x 3 traits (HT, R8, YLD) and `soy_geno.csv` 5,014 lines x 4,234 markers coded -1/0/1 (marker names such as `Gm01_3321482`), joined on the line id, plus `soy_CVFs.csv` with the authors' fold assignments. Counted on a preview of the files, 2026-10-31: 5,014 rows, 4,234 marker columns, trait columns standardized to mean 0 and sd 1. Target `YLD`, yield.
- Use case: a soybean breeder, before the field season, decides which RILs to advance from the genotype alone (genomic selection): predicting traits from genotypes "is accelerating the speed of crop and livestock breeding" (Introduction), and the paper recommends that "breeders test the performance of multiple algorithms on their training population". Fit direct for selection inside the population. Regime: the source's "80/20 training/testing approach ... where 20% of the lines were held out", replicated 10 times (SPLIT-5); the line ids carry the family (DS11-XX..., 38 families of 98 to 140 lines on a preview), so a grouped split by family tests the cold start of a new cross, which is the question for new germplasm (SPLIT-31, USE-10).
- Siblings and duplicates: the other three cuts of the same release are other species and panels, distinct tasks (PROV-7); soy HT and R8 would be cuts of this one without a distinct task (PROV-6). `uniform_soybean_tests_yield` (Shook et al. 2021, 103,365 variety x location x year records with daily weather, a candidate of this run) is soybean yield as well, but a genotype-by-environment task from weather and location rather than genomic prediction from markers (PROV-7); `soybean` (UCI 1988) is the unrelated disease diagnosis set. External collections: TabBench-Bio (`gp-soy-YLD`).
- Better data: a candidate of the benchmark TabBench-Bio; no new search this round.
- Papers and pages: Azodi et al. 2019 (G3, https://academic.oup.com/g3journal/article/9/11/3691/6026746) and Xavier et al. 2016 for SoyNAM; the Zenodo mirror https://zenodo.org/records/4980429; TabBench-Bio (arXiv 2609.07441), Table 4 row gp-soy-YLD.
- Metric: Pearson's correlation, the source's own ranked criterion — the Methods say it "was used as it is the standard metric for GP performance", while the hyper-parameter grid search used MSE; that is one deliberate choice of the field (MET-5), and it is what a breeder reads (the ranking of lines). TabBench-Bio scores this table with its own "RMSE is the primary regression metric" (Sec. 3.5). If the spec carries no correlation metric, `rmse` is the fallback (MET-8), but then MET-3 needs the natural scale, which this release does not ship. Inputs: none.
- Risks for /add-dataset: the trait columns are standardized (mean 0, sd 1 on a preview of the files, 2026-10-31), while the release's README says "Phenotype values were normalized between 0 and 1" — either way the natural units are lost, so the metric is not on the scale the task means (MET-3) and a repair from the original publication is the first question (PROV-13). The genotype and phenotype CSVs join on the line id (two tables). Marker calls were "obtained in the form of biallelic SNPs with missing marker data already dropped or imputed by the original authors" and recoded to -1/0/1 (README), an imputation done at the source that we cannot check (LEAK-30 at most). All columns are numeric marker codes, no mixed types. The 38 families readable from the line ids make the IID split optimistic; decide the regime from the use case before building (SPLIT-1).
- Priority: gap 0 (biology & life sciences and regression are not thin), use case + (the paper names the breeder and the selection decision), source + (a peer-reviewed paper, a README and CC0 data), shape + (5,014 lines x 4,234 markers), risk - (the target ships standardized, without its natural scale).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 5,014 x 4,234; target: YLD.
- Why: Yield of soybean lines from SNP genotypes
- Notes: Same Azodi et al. release; the existing soybean record is the unrelated UCI disease set.
