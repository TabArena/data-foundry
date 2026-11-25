---
unique_name: genomic_prediction_soy_yield
name: gp-soy-YLD (Soybean Yield Genomic Prediction)
checked_by:
- AI (UNVERIFIED)
data_foundry_status:
- WIP (Triage)
claimed_by: Andrej
suggestion: TBD -> Yes
priority: 4
tags:
- AI-Filled (Verify)
- Many features
- 'Samples: No Time Dimension'
- 'Entities: Recur'
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

**Screening (AI, 2026-11-25):** `TBD -> Yes`, priority 4: yield of about 5,000 SoyNAM recombinant inbred lines of 40 biparental families from about 4,300 SNP markers — genomic selection as a plain regression, the one of the four Azodi cuts with a comfortable shape, and an origin (the SoyNAM data) that holds the yields in kg/ha per plot.
- Source: the SoyNAM population, "recombinant inbred lines (RILs) derived from 40 biparental populations" (Xavier et al. 2016, quoted in the Azodi release's README); the data were released by the SoyNAM project on SoyBase (offline) and are kept in the CRAN package `SoyNAM` (https://cran.r-project.org/package=SoyNAM, first version 2015-07-29, GPL-3, data "downloaded on November 16th 2015 from https://soybase.org/SoyNAM/index.php"); the yield trials are described by Diers et al., G3 8(10):3367, 2018 (https://doi.org/10.1534/g3.118.200332). Compiled as a derived cut by Azodi CB et al., "Benchmarking Parametric and Machine Learning Models for Genomic Prediction of Complex Traits", G3 9(11):3691-3702, 2019 (doi 10.1534/g3.119.400498; Dryad doi 10.5061/dryad.xksn02vb9, Zenodo 4980429, CC0). As published by Azodi: `soy_pheno.csv` 5,014 lines x 3 traits (HT, R8, YLD), standardized, and `soy_geno.csv` 5,014 lines x 4,234 markers coded -1/0/1, plus fold assignments. As published at the origin (package 1.6.2, counted 2026-11-08 in the size check of the large candidates): 60,390 line-environment plots with yield in kg/ha for 5,546 lines of 40 families in 18 environments (2011-2013; Iowa, Illinois, Indiana, Kansas, Michigan, Missouri, Nebraska and two Ohio sites), with height, R8, lodging, protein, oil and seed size, check plots in `data.check`, and 5,590 lines x 4,611 raw markers coded 0/1/2 (a QA set of 5,180 x 4,312). Target: yield per line.
- Use case: a soybean breeder, before the field season, ranks the progeny of a new cross from the genotype alone (genomic selection): predicting traits from genotypes "is accelerating the speed of crop and livestock breeding" (Azodi et al., Introduction), and the paper recommends that "breeders test the performance of multiple algorithms on their training population"; fit direct; collection `Samples: No Time Dimension`: a designed population of RILs grown in a multi-environment trial (2011-2013), each family in field blocks with common checks, the genotype fixed before the trials; `Entities: Recur` at the origin (a line has a median of 11 environment plots), one row per line once the line value is computed; type `Experimental Results` (a designed population measured by one trial protocol, SPLIT-34).
- Split: leaf L-EXP.kind (Grouped · `UnseenGroup`, the family) because [EXP.meets] a kind the data does not contain (the breeder ranks the lines of a new cross, with no phenotyped sibling), [EXP.kind-key] yes (the family is in the line id, `DS11-XX...`; 40 families of about 98 to 140 lines, 39 after the QA, enough to hold out whole); open: within-family selection (a random split of lines, L-EXP.random) is the other common genomic-selection design, and about half the variance of the line values lies between families, so the metric question below goes with it; Azodi's random 80/20 holdout over lines is a habit, not a choice for this use case (SPLIT-5).
- Siblings and duplicates: the other three cuts of the same Azodi release are other species and panels, distinct tasks (PROV-7); soy HT and R8 would be cuts of this one without a distinct task (PROV-6). `uniform_soybean_tests_yield` (Shook et al. 2021, variety x location x year records with daily weather) is soybean yield as well, but a genotype-by-environment task from weather and location rather than genomic prediction from markers (PROV-7); `soybean` (UCI 1988) is the unrelated disease diagnosis set. External collections: TabBench-Bio (`gp-soy-YLD`).
- Better data: the origin itself, SoyNAM (above): about 5,500 lines on the natural scale instead of Azodi's 5,014 standardized values, the same source, so the first publication to build from rather than another record (PROV-8, PROV-13); no other hit in a quick look.
- Papers and pages: Azodi et al. 2019 (G3, https://academic.oup.com/g3journal/article/9/11/3691/6026746); Xavier et al. 2016 and Song et al. 2017 (Plant Genome, https://doi.org/10.3835/plantgenome2016.10.0109) for the population and the SNP chip; Diers et al. 2018 for the trials; the CRAN package; the Zenodo mirror https://zenodo.org/records/4980429; TabBench-Bio (arXiv 2609.07441), Table 4 row gp-soy-YLD.
- Metric: Pearson's correlation over the test lines, the ranked criterion of Azodi et al. ("as it is the standard metric for GP performance"; MSE only tuned the hyper-parameters), one deliberate choice of the field (MET-5) that matches a selection ranking lines. Open for the curator: on held-out families a pooled r also scores the ranking of the families, while the ranking within a cross is what genomics adds; `mean_group_pearsonr` on the family is in the library (MET-13). TabBench-Bio's RMSE (Sec. 3.5) is a benchmark convention. Inputs: the family, for a within-family score; it is computable from the line id.
- Risks for /add-dataset: build from the origin, not from Azodi's standardized `YLD` (README: "normalized between 0 and 1", observed mean 0 and sd 1; MET-3, PROV-13). The line value is ours to compute from the plots: Diers et al. 2018 adjust for environment and field-block effects estimated on the check plots, the simpler option is a mean over environments; either way no line's plots may enter another line's value (LEAK-10). Some lines' raw genotype rows may belong to another sample (compare the raw and the QA matrices per line). Missing marker calls stay missing: no imputation over all rows (CLEAN-7). Late maturity correlates with yield; R8 is measured with the yield and does not ship as an input (LEAK-10).
- Priority: gap 0 (biology & life sciences has 10 accepted datasets, thin at 6 or fewer; regression and the grouped regime are not thin), use case + (the breeder and the selection decision are named), source + (data papers, a maintained package from the project's members, CC0 for the cut), shape + (about 5,500 lines x 4,300 markers, 40 families), risk 0 (the origin repairs the scale; the line value follows the data paper's model).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 5,014 x 4,234; target: YLD.
- Why: Yield of soybean lines from SNP genotypes
- Notes: Same Azodi et al. release; the existing soybean record is the unrelated UCI disease set.
