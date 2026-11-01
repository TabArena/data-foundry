---
unique_name: genomic_prediction_switchgrass_height
name: gp-switchgrass-HT (Switchgrass Height Genomic Prediction)
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

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: plant height of 514 switchgrass genotypes from 217,150 SNP markers, genomic selection in a bioenergy crop; secondary on 514 rows against 217,150 markers and the clones in the panel.
- Source: "Switchgrass phenotypic (Lipka et al. 2014) and genotypic (Evans et al. 2017) data were generated from the Northern Switchgrass Association Panel (Evans et al. 2015) which contains clones or genotypes from 66 diverse upland switchgrass populations" (the release's README); compiled by Azodi CB et al., "Benchmarking Parametric and Machine Learning Models for Genomic Prediction of Complex Traits", G3 9(11):3691-3702, 2019 (doi 10.1534/g3.119.400498), who compiled 18 traits of six plant species and deposited them on Dryad (doi 10.5061/dryad.xksn02vb9), mirrored as Zenodo record 4980429 (CC0, deposited 2019-10-04). As published: `switchgrass_pheno.csv` 514 lines x 3 traits (ST, HT, AN) and `switchgrass_geno.csv` 514 lines x 217,150 markers coded -1/0/1, joined on the line id, plus `switchgrass_CVFs.csv` with the authors' fold assignments. Counted on a preview, 2026-10-31: 514 phenotype rows whose ids name the population (`Blackwell_5001`), 66 populations of 2 to 10 lines. Target `HT`, plant height.
- Use case: a switchgrass breeder selecting among the panel's genotypes before a field trial (genomic selection): predicting traits from genotypes "is accelerating the speed of crop and livestock breeding" (Introduction), the paper recommending that "breeders test the performance of multiple algorithms on their training population". Fit direct within the panel. Regime: the source's random "80/20 training/testing approach" over lines (SPLIT-5), but the panel is 66 populations with clones, so a split grouped by population is the variant that tests an unseen population (SPLIT-31, USE-10).
- Siblings and duplicates: the other three cuts of the same release are other species, distinct tasks (PROV-7); switchgrass ST and AN would be cuts without a distinct task (PROV-6). No other switchgrass or bioenergy-crop record. External collections: TabBench-Bio (`gp-switchgrass-HT`).
- Better data: a candidate of the benchmark TabBench-Bio; no new search this round.
- Papers and pages: Azodi et al. 2019 (G3, https://academic.oup.com/g3journal/article/9/11/3691/6026746), with Lipka et al. 2014 and Evans et al. 2015/2017 for the panel; the Zenodo mirror https://zenodo.org/records/4980429; TabBench-Bio (arXiv 2609.07441), Table 4 row gp-switchgrass-HT.
- Metric: Pearson's correlation, the source's own ranked criterion — the Methods say it "was used as it is the standard metric for GP performance", while the hyper-parameter grid search used MSE; that is one deliberate choice of the field (MET-5), and it is what a breeder reads (the ranking of lines). TabBench-Bio scores this table with its own "RMSE is the primary regression metric" (Sec. 3.5). If the spec carries no correlation metric, `rmse` is the fallback (MET-8), but then MET-3 needs the natural scale, which this release does not ship. Inputs: none.
- Risks for /add-dataset: the trait columns are standardized (mean 0, sd 1 on a preview of the files, 2026-10-31), while the release's README says "Phenotype values were normalized between 0 and 1" — either way the natural units are lost, so the metric is not on the scale the task means (MET-3) and a repair from the original publication is the first question (PROV-13). The genotype and phenotype CSVs join on the line id (two tables). Marker calls were "obtained in the form of biallelic SNPs with missing marker data already dropped or imputed by the original authors" and recoded to -1/0/1 (README), an imputation done at the source that we cannot check (LEAK-30 at most). All columns are numeric marker codes, no mixed types. Clones in the panel can put the same genotype on both sides of a random split (LEAK-17 by near-duplicate rows): check for duplicate marker profiles before splitting, and read the population from the line id. 217,150 columns for 514 rows is the extreme of p >> n, and any feature cap is fit on the training side only (LEAK-27).
- Priority: gap 0 (biology & life sciences and regression are not thin), use case + (the breeder and the selection decision are named), source + (a peer-reviewed paper, a README and CC0 data), shape 0 (514 lines), risk - (the target ships without its natural scale, clones and populations in one panel).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 514 x 217,150; target: HT.
- Why: Plant height of switchgrass lines from SNP genotypes
- Notes: Same Azodi et al. release.
