---
unique_name: gse50660_smoking_methylation
name: GEO-GSE50660-Methylation-Smoking (Smoking Status DNA Methylation)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
tags:
- AI-Filled (Verify)
- Many features
collections:
- TabBench-Bio
original_source: Other
year: '2014'
domain: medical & healthcare
problem_type: Multiclass Classification
source_links:
- https://doi.org/10.4161/15592294.2014.969637
- https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE50660
- https://arxiv.org/abs/2609.07441
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: self-reported smoking status (never, former, current) from 450K blood methylation of 464 CARDIOGENICS participants (Tsaprouni et al. 2014); a known biomarker use, but published as an association study, with only 22 current smokers.
- Source: Tsaprouni, Yang, Bell et al., "Cigarette smoking reduces DNA methylation levels at multiple genomic loci but the effect is partially reversible upon cessation", Epigenetics 9(10):1382-1396, 2014 (https://doi.org/10.4161/15592294.2014.969637, read on PMC4623553); data GEO GSE50660, public 2014-11-25. As published: 464 peripheral-blood samples x 450K probes (processed and signal matrices, IDATs), with per sample `smoking` (0 never 179, 1 former 263, 2 current 22), `age` (38-67) and `gender` (327 male, 137 female); "At the discovery phase 464 subjects were analyzed, of which 238 were CAD cases" (Methods); smoking from a questionnaire, no cotinine.
- Use case: checking a person's smoking status from a blood sample when the self-report is not trusted (an insurer, a cessation trial); the paper names no user ("We conducted an epigenome wide association study", Abstract), so the use case is ours; fit approximate (the label is the self-report such a test would check; the former smokers include 12 who still smoked within 12 weeks of recruitment); regime IID (one sample per person) or grouped by recruitment site: the paper names "Recruitment site, Beadchip, and BS-treated DNA input" as sources of variation, and the sample ids carry a code CXMA-01 to -05 (94, 47, 70, 238, 15 samples; 238 equals the CAD cases, to check).
- Siblings and duplicates: no other smoking methylation record. External collections: TabBench-Bio (arXiv 2609.07441, Table 4); others not searched (web search used up).
- Better data: a candidate of the benchmark TabBench-Bio; no new search in this run.
- Papers and pages: Tsaprouni et al. 2014 (above), replicated in EPITWIN (356 female twins, not in this series).
- Metric: none found: the paper fits linear regressions and ANOVA comparisons and reports no classifier (read on PMC4623553), so the fallback `log_loss` for three classes (MET-1, MET-8). Inputs none.
- Risks for /add-dataset: 22 current smokers, about 4 per test fold over 5 folds (TP-5, TP-8; a never-against-ever framing is the curator's alternative); SEL-7 to weigh: the label is the respondent's own answer, though the features are a blood measurement, not the same interview; half the people are CAD patients, and the site and chip confounding needs a look (SPLIT-3); the processed matrix was normalised over all samples (LEAK-30, weak); no probe subset chosen on the target (LEAK-31).
- Priority: gap + (multiclass, 24 accepted, thin), use case 0 (ours, not the source's), source + (paper and GEO), shape 0 (464 rows), risk - (22 current smokers).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 464 x 30,000; target: smoking (179 never / 263 former / 22 current).
- Why: Smoking status (never / former / current) from peripheral-blood 450K methylation
- Notes: Tsaprouni et al. 2014.
