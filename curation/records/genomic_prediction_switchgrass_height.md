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

**Screening (AI, 2026-11-25):** `TBD -> 2nd Tier`, priority 2: plant height of 514 switchgrass genotypes of 66 upland populations from 217,150 SNP markers, genomic selection in a bioenergy crop; secondary on 514 rows against 217,150 markers, a target shipped without its natural scale, and populations of 2 to 10 genotypes in one panel.
- Source: "Switchgrass phenotypic (Lipka et al. 2014) and genotypic (Evans et al. 2017) data were generated from the Northern Switchgrass Association Panel (Evans et al. 2015) which contains clones or genotypes from 66 diverse upland switchgrass populations" (the release's README, re-read 2026-11-25); compiled by Azodi CB et al., "Benchmarking Parametric and Machine Learning Models for Genomic Prediction of Complex Traits", G3 9(11):3691-3702, 2019 (doi 10.1534/g3.119.400498), deposited on Dryad (doi 10.5061/dryad.xksn02vb9), mirrored as Zenodo record 4980429 (CC0, deposited 2019-10-04). As published: `switchgrass_pheno.csv` 514 lines x 3 traits (ST, HT, AN; header and row count re-read 2026-11-25) and `switchgrass_geno.csv` (237.1 MB) 514 lines x 217,150 markers coded -1/0/1, joined on the line id, plus `switchgrass_CVFs.csv` with the authors' fold assignments. Counted on the preview of 2026-10-31: the ids name the population (`Blackwell_5001`), 66 populations of 2 to 10 genotypes. Target `HT`, plant height.
- Use case: a switchgrass breeder selecting among genotypes before a field trial (genomic selection): predicting traits from genotypes "is accelerating the speed of crop and livestock breeding" (Introduction), the paper recommending that "breeders test the performance of multiple algorithms on their training population"; fit direct within the panel; collection `Samples: No Time Dimension`: one association panel of clonally propagated genotypes grown in the same field trials, the genotype fixed before the trial; the release dates neither genotypes nor plots; type `Experimental Results` (a closed set of genotypes measured by one trial protocol, SPLIT-34).
- Split: leaf L-EXP.random (Random · `Timeless`) because [EXP.meets] a new genotype of the populations the panel holds (selection among the panel's germplasm), [EXP.repeated] no (one row per genotype, its clones averaged at the source); open: whether the use case meets a population the panel lacks — then [EXP.kind-key] yes (the population, read from the line id, 66 groups) and L-EXP.kind; a person decides which, from Lipka et al. 2014's own design; duplicate marker profiles to check before splitting (LEAK-19). Azodi's random 80/20 holdout over lines is a habit (SPLIT-5).
- Siblings and duplicates: the other three cuts of the same release are other species, distinct tasks (PROV-7); switchgrass ST and AN would be cuts without a distinct task (PROV-6). No other switchgrass or bioenergy-crop record (grep on "switchgrass", "Lovell", "genomic selection", 2026-11-25). External collections: TabBench-Bio (`gp-switchgrass-HT`).
- Better data: possibly the switchgrass diversity panel of Lovell et al., "Genomic mechanisms of climate adaptation in polyploid bioenergy switchgrass", Nature 590:438-444, 2021 (https://doi.org/10.1038/s41586-020-03127-1): 732 resequenced tetraploid genotypes clonally planted in up to 10 common gardens (5,521 plants); more genotypes and sites than the 514 here, but upland and lowland ecotypes, and whether per-genotype height and markers are public was not checked in this quick look (no Dryad deposit found); no record yet.
- Papers and pages: Azodi et al. 2019 (G3, https://academic.oup.com/g3journal/article/9/11/3691/6026746), with Lipka et al. 2014 and Evans et al. 2015/2017 for the panel (not read); the Zenodo mirror https://zenodo.org/records/4980429; TabBench-Bio (arXiv 2609.07441), Table 4 row gp-switchgrass-HT.
- Metric: Pearson's correlation over the test lines, the source's own ranked criterion — the Methods say it "was used as it is the standard metric for GP performance", while the hyper-parameter grid search used MSE; one deliberate choice of the field (MET-5). TabBench-Bio's RMSE (Sec. 3.5) is a benchmark convention. The metric library carries correlations (MET-13), so the source's metric can ship; `rmse` would also need the natural scale (MET-3). Inputs: none.
- Risks for /add-dataset: the trait columns are standardized (mean 0, sd 1 on the preview of 2026-10-31; values such as -0.86 in the rows re-read 2026-11-25), while the README says "Phenotype values were normalized between 0 and 1" — the natural units are lost, and a repair from Lipka et al. 2014 is the first question (PROV-8, PROV-13). Two tables joined on the line id. Marker calls were "obtained in the form of biallelic SNPs with missing marker data already dropped or imputed by the original authors" (README), an imputation at the source we cannot check (LEAK-30 at most). Clones in the panel can put the same genotype on both sides of a random split: check duplicate marker profiles first (LEAK-19). 217,150 columns for 514 rows is the extreme of p >> n; width is no reason to drop markers (CLEAN-22), and any filter fit on the data is fit inside the training side only (LEAK-27).
- Priority: gap 0 (biology & life sciences has 10 accepted datasets, thin at 6 or fewer; regression and both candidate regimes are not thin), use case + (the breeder and the selection decision are named), source + (a peer-reviewed paper, a README and CC0 data), shape 0 (514 lines), risk - (the target ships without its natural scale; clones and populations in one panel).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 514 x 217,150; target: HT.
- Why: Plant height of switchgrass lines from SNP genotypes
- Notes: Same Azodi et al. release.

**Assessment (AI, 2026-11-27):** the per-group metric rule was walked over the collection today, and this record carries its shape.
- The screening declares the source's pooled Pearson's r. Under the rule as it now reads, a task whose actor ranks inside one group and never between groups takes the metric per group, and overruling a metric the source chose deliberately, which Azodi et al. do, needs the extra condition: a predictor knowing only each group's mean must beat a model whose penalty or capacity was chosen on the training side.
- Nothing changes here, because there is no definition to change. The measurement belongs at `/add-dataset` if this record is ever taken up, and it is named so that it is not missed.
