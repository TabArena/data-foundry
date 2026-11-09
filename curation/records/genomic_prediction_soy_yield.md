---
unique_name: genomic_prediction_soy_yield
name: gp-soy-YLD (Soybean Yield Genomic Prediction)
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 4
tags:
- AI-Filled (Verify)
- Many features
collections:
- TabBench-Bio
original_source: Other
year: '2015'
domain: biology & life sciences
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://cran.r-project.org/package=SoyNAM
- https://doi.org/10.1534/g3.118.200332
- https://doi.org/10.1534/g3.119.400498
- https://doi.org/10.5061/dryad.xksn02vb9
- https://arxiv.org/abs/2609.07441
- https://zenodo.org/records/4980429
v2_path: datasets/_dev/tabarena-v0pt2/genomic_prediction_soy_yield/dataset.py
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

**Assessment (AI, 2026-11-08):** size check for the large-datasets review: the Azodi table is 5,014 lines x 4,234 markers with one standardized yield per line. Its origin, the SoyNAM R package, has yield in kg/ha per line and environment (60,390 plots of 5,546 lines in 18 environments) and 4,611 raw markers, so a build from SoyNAM gives about 5,544 lines x 4,611 markers on the natural scale (PROV-8, PROV-13); the call stands, priority 3.
- As published (Azodi): Zenodo 4980429 (CC0, 2019-10-04), counted 2026-11-08: `soy_pheno.csv` 5,014 rows with ID, HT, R8 and YLD (YLD has mean 0 and sd 1, although the README says "normalized between 0 and 1"), `soy_geno.csv` (50,038,368 bytes) with ID and 4,234 markers (header counted; the paper says 4,240), and `soy_CVFs.csv`. Neither the README nor the paper says whether YLD is a mean or a BLUP over environments. The line ids carry 38 families of 98 to 140 lines.
- As published (origin): CRAN package `SoyNAM` 1.6.2 (2022-01-04, GPL-3, Xavier, Beavis, Specht, Diers et al.; data "downloaded on November 16th 2015 from https://soybase.org/SoyNAM/index.php", which now returns 404), counted from the package's .RData files on 2026-11-08. `data.line` has 60,744 line-environment rows, 60,390 with yield in kg/ha, for 5,546 lines of 40 families in 18 environments (IA, IL, IN, KS, MI, MO, NE and two Ohio sites, 2011-2013), with height, R8, lodging, protein, oil and seed size. `data.check` has 9,043 rows of checks and parents, and `gen.raw` 5,590 lines x 4,611 markers coded 0/1/2 (4.9% missing). The QA versions are `data.line.qa` (62,572 rows, 39 families) and `gen.qa` (5,180 x 4,312). Of Azodi's 5,014 lines, 5,007 have SoyNAM yields (54,602 plots, a median of 11 environments per line), and 4,230 of the 4,234 markers are in `gen.qa`.
- The task's table: the breeder decides per line (SPLIT-23), so one row per line: 5,544 lines with yield and raw genotypes x 4,611 markers (or 4,312 QA markers), computed from the package files. The target is a line value in kg/ha computed from the plots: the package's `BLUP()` fits environment and check effects with lme4, and a mean over environments is the simpler option (a choice for the curator). One row per plot (60,366 rows with genotypes, the environment as an input) is a genotype-by-environment framing, another task.
- Access: CRAN source tarball, 4,948,970 bytes, .RData, no login, GPL-3. The Azodi soy files on Zenodo are about 51 MB, CC0.
- Changes the call: the origin repairs the scale problem the screening raised (MET-3, PROV-13): the yields exist in kg/ha per plot, so the record's first source is SoyNAM (PROV-8), and the Azodi table becomes a derived cut to cite. The split stays grouped by family (40 families) for a new cross. The priority stays 3: the standardized target is no longer a risk, but the line value is ours to compute (BLUP or mean), which keeps the risk point.
- Not checked: how Azodi computed the line value; the SoyNAM papers (Song et al. 2017, Diers et al. 2018, Xavier et al. 2016) were not read; whether SoyBase serves the data at a new address (its project list names a data store SoyNAM_2014).

CC (2026-11-08, Lennart): accepted for adding (`Yes`) in the screening review of the large candidates (most rows, most features).

**Assessment (AI, 2026-11-09):** review panel (full): ship after changes (made: the line value now removes environment and field-block effects estimated on the check plots alone, as Diers et al. 2018 do; 70 lines whose raw genotype row was another sample take their own calls from the QA matrix, none dropped; `context="all_rows"`; the record's year 2015 and the CRAN and Diers 2018 links); disputed: MET-1/MET-2/MET-5 (pooled r against the within-family r), the fold design (only a few groups, stratify or not); for the curator: issues 1-3. Priority 4: gap 0, use case +, source +, shape +, risk 0 (the target the size check called ours to compute now follows the data paper; the open metric question changes the score's unit, not the data).
