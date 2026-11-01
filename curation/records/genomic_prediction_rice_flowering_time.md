---
unique_name: genomic_prediction_rice_flowering_time
name: gp-rice-FT (Rice Flowering Time Genomic Prediction)
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

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: flowering time of 327 rice lines from 57,542 SNP markers, the IRRI elite breeding panel; a real genomic-selection regression, secondary on its 327 rows.
- Source: "elite breeding lines from the International Rice Research Institute irrigated rice breeding program (Spindel et al. 2015), and dry season trait data averaged over four years were used" (the release's README); compiled by Azodi CB et al., "Benchmarking Parametric and Machine Learning Models for Genomic Prediction of Complex Traits", G3 9(11):3691-3702, 2019 (doi 10.1534/g3.119.400498), who compiled 18 traits of six plant species and deposited them on Dryad (doi 10.5061/dryad.xksn02vb9), mirrored as Zenodo record 4980429 (CC0, deposited 2019-10-04). As published: `rice_pheno.csv` 327 lines x 3 traits (YLD, FT, HT) and `rice_geno.csv` 327 lines x 57,542 markers coded -1/0/1 (header and first rows previewed 2026-10-31; marker names such as `S1_11984`), joined on the line id, plus `rice_CVFs.csv` with the authors' fold assignments. Target `FT`, flowering time.
- Use case: a rice breeder, before the season, picks the lines to advance from their genotype (genomic selection): predicting traits from genotypes "is accelerating the speed of crop and livestock breeding" (Introduction); the paper recommends that "breeders test the performance of multiple algorithms on their training population". Fit direct inside an elite breeding programme, approximate beyond it. Regime: the source's "80/20 training/testing approach" over lines, replicated 10 times (SPLIT-5); elite lines share pedigrees, so a grouped split by family is the variant the use case may need (SPLIT-31, USE-10).
- Siblings and duplicates: the other three cuts of the same release (`genomic_prediction_maize_flowering_time`, `genomic_prediction_soy_yield`, `genomic_prediction_switchgrass_height`) are other species and panels, distinct tasks (PROV-7); the species' other traits (YLD, HT) would be cuts without a distinct task (PROV-6). `csisa_lds_rice_yield_india_2018` is rice too but an agronomic survey of farm yields, not genomic prediction; `rice_cammeo_and_osmancik` is an image-derived grain-shape set. External collections: TabBench-Bio (`gp-rice-FT`).
- Better data: a candidate of the benchmark TabBench-Bio; no new search this round.
- Papers and pages: Azodi et al. 2019 (G3, https://academic.oup.com/g3journal/article/9/11/3691/6026746) and Spindel et al. 2015 for the panel; the Zenodo mirror https://zenodo.org/records/4980429; TabBench-Bio (arXiv 2609.07441), Table 4 row gp-rice-FT.
- Metric: Pearson's correlation, the source's own ranked criterion — the Methods say it "was used as it is the standard metric for GP performance", while the hyper-parameter grid search used MSE; that is one deliberate choice of the field (MET-5), and it is what a breeder reads (the ranking of lines). TabBench-Bio scores this table with its own "RMSE is the primary regression metric" (Sec. 3.5). If the spec carries no correlation metric, `rmse` is the fallback (MET-8), but then MET-3 needs the natural scale, which this release does not ship. Inputs: none.
- Risks for /add-dataset: the trait columns are standardized (mean 0, sd 1 on a preview of the files, 2026-10-31), while the release's README says "Phenotype values were normalized between 0 and 1" — either way the natural units are lost, so the metric is not on the scale the task means (MET-3) and a repair from the original publication is the first question (PROV-13). The genotype and phenotype CSVs join on the line id (two tables). Marker calls were "obtained in the form of biallelic SNPs with missing marker data already dropped or imputed by the original authors" and recoded to -1/0/1 (README), an imputation done at the source that we cannot check (LEAK-30 at most). All columns are numeric marker codes, no mixed types. 327 rows is a tiny-data regression (TP-5 counts the spread of the target, not a class here); the four-year averaging of the dry-season phenotype is the source's, and the per-year values are in Spindel et al. 2015 if the curator wants them.
- Priority: gap 0 (biology & life sciences and regression are not thin), use case + (the breeder and the selection decision are named), source + (a peer-reviewed paper, a README and CC0 data), shape 0 (327 lines), risk - (the target ships without its natural scale, and the four cuts overlap one release).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 327 x 57,542; target: FT.
- Why: Flowering time of rice lines from SNP genotypes
- Notes: Same Azodi et al. release as gp-maize-FT.
