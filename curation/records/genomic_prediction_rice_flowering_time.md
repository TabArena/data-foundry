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

**Screening (AI, 2026-11-25):** `TBD -> 2nd Tier`, priority 2: flowering time of 327 elite rice lines of the IRRI irrigated breeding programme from 57,542 SNP markers; a real genomic-selection regression, secondary on its 327 rows and a target shipped without its natural scale.
- Source: "elite breeding lines from the International Rice Research Institute irrigated rice breeding program (Spindel et al. 2015), and dry season trait data averaged over four years were used" (the release's README, re-read 2026-11-25); Spindel et al., PLoS Genetics 11(2):e1004982, 2015 (https://doi.org/10.1371/journal.pgen.1004982) for the panel; compiled by Azodi CB et al., "Benchmarking Parametric and Machine Learning Models for Genomic Prediction of Complex Traits", G3 9(11):3691-3702, 2019 (doi 10.1534/g3.119.400498), deposited on Dryad (doi 10.5061/dryad.xksn02vb9), mirrored as Zenodo record 4980429 (CC0, deposited 2019-10-04). As published: `rice_pheno.csv` 327 lines x 3 traits (YLD, FT, HT; header and row count re-read 2026-11-25) and `rice_geno.csv` (50.5 MB) 327 lines x 57,542 markers coded -1/0/1 (marker names such as `S1_11984`, previewed 2026-10-31), joined on the line id, plus `rice_CVFs.csv` with the authors' fold assignments. Target `FT`, flowering time.
- Use case: a rice breeder, before the season, picks the lines to advance from their genotype (genomic selection): predicting traits from genotypes "is accelerating the speed of crop and livestock breeding" (Introduction); the paper recommends that "breeders test the performance of multiple algorithms on their training population"; fit direct inside an elite breeding programme, approximate beyond it; collection `Samples: No Time Dimension`: the lines grown in the same dry-season trials and their trait averaged over four years, the genotype fixed before the trials; the release dates neither the lines nor the breeding cycle each came from; type `Experimental Results` (a closed set of lines measured by one trial protocol, SPLIT-34).
- Split: leaf L-EXP.random (Random · `Timeless`) because [EXP.meets] a new line of the programme's kinds (the breeder ranks the next unphenotyped lines of the same programme), [EXP.repeated] no (one averaged row per line); open: whether the lines' breeding cycles or crosses can be recovered from Spindel et al. 2015 (pedigrees or cycle years would give a family for [EXP.kind-key] or an order for a later-cycle test); duplicate marker profiles to check (LEAK-19). Azodi's random 80/20 holdout is a habit (SPLIT-5).
- Siblings and duplicates: the other three cuts of the same release (`genomic_prediction_maize_flowering_time`, `genomic_prediction_soy_yield`, `genomic_prediction_switchgrass_height`) are other species and panels, distinct tasks (PROV-7); the species' other traits (YLD, HT) would be cuts without a distinct task (PROV-6). `csisa_lds_rice_yield_india_2018` is rice too but an agronomic survey of farm yields, not genomic prediction; `rice_cammeo_and_osmancik` is an image-derived grain-shape set. External collections: TabBench-Bio (`gp-rice-FT`).
- Better data: none found in a quick look (a web search for public rice genomic-selection panels with heading date or flowering time and more lines, 2026-11-25: a southern US rice panel on Dryad, doi 10.5061/dryad.j9kd51ctd, is smaller; Dryad doi 10.5061/dryad.7369p, tropical elite breeding lines of 2016, likely the same IRRI programme, was not opened); the 2026-10-31 run searched no further.
- Papers and pages: Azodi et al. 2019 (G3, https://academic.oup.com/g3journal/article/9/11/3691/6026746) and Spindel et al. 2015 for the panel (not read); the Zenodo mirror https://zenodo.org/records/4980429; TabBench-Bio (arXiv 2609.07441), Table 4 row gp-rice-FT.
- Metric: Pearson's correlation over the test lines, the source's own ranked criterion — the Methods say it "was used as it is the standard metric for GP performance", while the hyper-parameter grid search used MSE; one deliberate choice of the field (MET-5), and what a breeder reads (the ranking of lines). TabBench-Bio's RMSE (Sec. 3.5) is a benchmark convention. The metric library carries correlations (MET-13), so the source's metric can ship; `rmse` would also need the natural scale (MET-3). Inputs: none.
- Risks for /add-dataset: the trait columns are standardized (mean 0, sd 1 on the preview of 2026-10-31; values such as -1.36 in the rows re-read 2026-11-25), while the README says "Phenotype values were normalized between 0 and 1" — either way the natural units are lost, and a repair from Spindel et al. 2015 (days to flowering per season) is the first question (PROV-8, PROV-13). Two tables joined on the line id. Marker calls were "obtained in the form of biallelic SNPs with missing marker data already dropped or imputed by the original authors" (README), an imputation at the source that we cannot check (LEAK-30 at most). 327 rows is a tiny-data regression (TP-5); the four-year averaging is the source's, and the per-season values may be in Spindel et al. 2015.
- Priority: gap 0 (biology & life sciences has 10 accepted datasets, thin at 6 or fewer; regression and the IID regime are not thin), use case + (the breeder and the selection decision are named), source + (a peer-reviewed paper, a README and CC0 data), shape 0 (327 lines), risk - (the target ships without its natural scale).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 327 x 57,542; target: FT.
- Why: Flowering time of rice lines from SNP genotypes
- Notes: Same Azodi et al. release as gp-maize-FT.

**Assessment (AI, 2026-11-27):** the per-group metric rule was walked over the collection today, and this record carries its shape.
- The screening declares the source's pooled Pearson's r. Under the rule as it now reads, a task whose actor ranks inside one group and never between groups takes the metric per group, and overruling a metric the source chose deliberately, which Azodi et al. do, needs the extra condition: a predictor knowing only each group's mean must beat a model whose penalty or capacity was chosen on the training side.
- Nothing changes here, because there is no definition to change. The measurement belongs at `/add-dataset` if this record is ever taken up, and it is named so that it is not missed.
