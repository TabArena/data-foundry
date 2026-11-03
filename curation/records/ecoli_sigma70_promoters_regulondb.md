---
unique_name: ecoli_sigma70_promoters_regulondb
name: E. coli K-12 sigma70 promoter benchmark (RegulonDB 9.0, 81 bp) and independent set (RegulonDB 10.8), as published with Sigma70Pred
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- Selection Bias
tags:
- AI-Filled (Verify)
original_source: Other
domain: biology & life sciences
problem_type: Binary Classification
source_links:
- https://doi.org/10.3389/fmicb.2022.1042127
- https://pmc.ncbi.nlm.nih.gov/articles/PMC9701712/
- https://doi.org/10.1186/s12918-018-0570-1
- https://github.com/ronicse59/iPromoter-FSEn
- https://doi.org/10.5281/zenodo.20163591
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: 741 experimentally verified E. coli sigma70 promoters (RegulonDB 9.0) against 1,400 sampled genome windows, 81 bp each, with a later-release test set; a real annotation task in the format of `splice`, but the negatives are constructed and published models already reach AUROC 0.996.
- Source: the 741/1,400 benchmark as published by 70ProPred (He, Jia, Duan & Zou, BMC Systems Biology 12, 2018, doi 10.1186/s12918-018-0570-1, Datasets section): "A total of 741 σ70 promoter samples were selected from the E.coli K-12 genome, which have been verified by experiments and downloaded from the RegulonDB9.0"; the region "[TSS-60…TSS + 20] ... with a length of 81 bp"; "As there are not enough experimental confirmed negative sequences, negative samples are collected from both coding and non-coding regions" (700 coding, 700 convergent intergenic). 70ProPred says "we used the latest datasets in both [15] and [16]" (Lin, Liang, Tang & Chen, IEEE/ACM TCBB 2017; Lin & Li, Theory Biosci 2011), so the set was likely first assembled by Lin et al. 2017 (not read). Sigma70Pred (Patiyal et al., Front Microbiol 13:1042127, 2022) reuses it and adds an independent set from RegulonDB 10.8, 1,134 promoters and 638 non-promoters ("There is no identical sequence in training and independent dataset"). As published: FASTA, one sequence and its class per entry. Preview (2026-10-31) of the GitHub copy ronicse59/iPromoter-FSEn `BenchmarkData.txt`: 2,141 sequences. Sigma70Pred's data page says "The datasets will be available soon", so no download of the independent set was found; the Zenodo deposit 10.5281/zenodo.20163591 is the tool's code (one 20 KB zip, GPL-3.0), too small to hold the sequences.
- Use case: a microbiologist or genome annotator, scanning a region or designing a promoter, decides which windows to treat or test as sigma70 promoters (70ProPred built its server "to facilitate experimental biologists"); fit approximate: the negatives are coding and convergent-intergenic windows, not the upstream windows a scan meets. Regime grouped by genomic locus: in the preview, `promoter-2` holds `promoter-1` shifted by 11 bp (several start sites of one region), so overlapping windows must share a fold; the RegulonDB 10.8 set is a natural later-release test.
- Siblings and duplicates: `molecular_biology_promoters` (`TBD -> 2nd Tier`, `Outdated`, `Trivial`; the UCI set of 106 sequences of 57 bp), the record this was found for; `splice` (`Yes`), a DNA-window classification in the same format. No other promoter record (grep: promoter). External collections: not searched (web search budget used up).
- Better data: found as better data for `molecular_biology_promoters` (the data-scouting run of 2026-10-30/31); no further search.
- Papers and pages: 70ProPred (jackknife; 95.56% accuracy, MCC 0.90); Sigma70Pred (5-fold CV and the independent set: AUROC 0.996 on the benchmark, 0.953 on the independent set); iPromoter-FSEn (the GitHub copy); RegulonDB 9.0 (Gama-Castro et al., NAR 2016).
- Metric: no deliberate one: 70ProPred reports Sn, Sp, Acc and MCC, Sigma70Pred adds AUROC, and neither names a criterion (MET-5); accuracy and MCC need a threshold neither fixes (MET-6), so the fallback `roc_auc`; inputs none.
- Risks for /add-dataset: constructed negatives (`Selection Bias`): coding windows differ from promoters by codon structure, so the task may be easier than a genome scan (TP-4 against the published AUROC 0.996); shifted, overlapping windows need a locus group (LEAK-17, SPLIT-24); the 81 positions are categorical columns as in `splice`, with k-mer composition the papers' route (SEL-12: judge whether sequence models clearly win); the independent set must be requested or rebuilt from RegulonDB 10.8; no licence on the GitHub copy (no criterion, EV-4).
- Priority: gap 0 (biology & life sciences has 4 accepted, binary not thin), use case 0 (approximate), source + (two papers, RegulonDB), shape + (2,141 sequences x 81 positions, a later test set), risk − (constructed negatives, near-saturated scores).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `molecular_biology_promoters`.
- as published: training: 741 experimentally verified sigma70 promoters (TSS-60 to TSS+20, 81 bp, RegulonDB 9.0) and 1,400 non-promoter 81 bp windows (700 from coding regions, 700 from convergent intergenic ...; target: promoter vs non-promoter (binary); access: open per the papers (Sigma70Pred data page webs.iiitd.edu.in/raghava/sigma70pred/data.html and the 70ProPred server; neither resolved from here on 2026-10-31); a copy of the 741/1,400 benchmark is on GitHub (ronicse59/iPromoter-FSEn, BenchmarkData.txt, no license).
- Why: Same organism, same binary target and the same kind of input (a fixed-length DNA window, one nucleotide per position, the format of UCI promoters and of splice, which is in TabArena), with promoters taken from the curated RegulonDB database rather than a hand-assembled list. Negatives are sampled genomic windows, as ...
- Adds: About 37x the sequences (about 3,900 against 106), a longer window (81 bp against 57), current RegulonDB annotations, and a published independent test set from a later database release (a temporal 'new annotations' test). Risk: constructed negatives (Selection Bias), and the 81 positions are categorical columns; the ...
