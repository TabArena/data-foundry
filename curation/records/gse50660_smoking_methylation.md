---
unique_name: gse50660_smoking_methylation
name: GEO-GSE50660-Methylation-Smoking (Smoking Status DNA Methylation)
checked_by:
- AI (UNVERIFIED)
- Andrej
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- Not Representative
tags:
- AI-Filled (Verify)
- Many features
- 'Samples: Over Time'
- 'Time: Lost'
- Clinical Study
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

**Screening (AI, 2026-11-25):** `TBD -> 2nd Tier`, priority 2: self-reported smoking status (never, former, current) from 450K blood methylation of 464 CARDIOGENICS participants (Tsaprouni et al. 2014); a known biomarker use, but published as an association study, the use case ours, with only 22 current smokers.
- Source: Tsaprouni, Yang, Bell et al., "Cigarette smoking reduces DNA methylation levels at multiple genomic loci but the effect is partially reversible upon cessation", Epigenetics 9(10):1382-1396, 2014 (https://doi.org/10.4161/15592294.2014.969637, read on PMC4623553); data GEO GSE50660, public 2014-11-25. As published (series matrix, re-read 2026-11-25): 464 peripheral-blood samples, one protocol for all ("extracted from whole blood samples using Qiagen DNeasy Kit"), with `smoking` (0 never 179, 1 former 263, 2 current 22), `age` and `gender` (327 male, 137 female), the sample id CXMA-0k-nnn; processed and signal matrices; `RAW.tar` (192 MB) lists only manifest files, no IDATs. "At the discovery phase 464 subjects were analyzed, of which 238 were CAD cases" (Methods).
- Use case: checking a person's smoking status from a blood sample when the self-report is not trusted (an insurer, a cessation trial); the paper names no user ("We conducted an epigenome wide association study", Abstract), so the use case is ours; fit approximate (the label is the self-report such a test would check). Collection: CAD cases and controls recruited at several sites over time, no date per sample (`Samples: Over Time`, `Time: Lost`); the smoking answer is given with the draw (no target tag); one sample per person. Type Clinical Study.
- Split: leaf L-PLACE.groups (Grouped · `UnseenGroup` (groups)) if the CXMA codes are recruitment sites, because [CLI.meets] for a test used on anyone is another site and [PLACE.several] then holds 5 codes; open: whether the codes are sites (94, 47, 70, 238, 15 samples; 238 equals the CAD cases, so they may be case status instead), and the enough-groups check with 22 current smokers; if they are not sites, the clinic branch leads to L-FORCED.random (Random · `ForcedIIDFromTemporal`).
- Siblings and duplicates: no other smoking methylation record. External collections: TabBench-Bio (Table 4).
- Better data: none found (quick look: public GEO smoking sets such as GSE53045 and GSE85210 are smaller; the large cohorts with smoking, such as Generation Scotland or KORA, are access-controlled; the 2026-10-31 run searched no further).
- Papers and pages: Tsaprouni et al. 2014 (above), replicated in EPITWIN (not in this series).
- Metric: none found: linear regressions and ANOVA, no classifier (read on PMC4623553), so the fallback `log_loss` for three classes (MET-1, MET-8). Inputs none.
- Risks for /add-dataset: 22 current smokers, about 4 per test fold (TP-5, TP-8; a never-against-ever framing is the curator's alternative); SEL-7 to weigh: the label is the respondent's own answer, though the features are a blood measurement, not the interview; half the people are CAD patients, so the cohort stands in for the general population it was not drawn from (`Not Representative`), and "Recruitment site, Beadchip, and BS-treated DNA input" are named sources of variation (SPLIT-3); the processed matrix normalised over all samples with no IDATs to rebuild from (LEAK-30, weak; the signal matrix is the route, PROV-13); no probe subset chosen on the target (LEAK-31).
- Priority: gap + (multiclass thin, 22 accepted), use case 0 (ours, not the source's), source + (paper and GEO), shape 0 (464 rows), risk - (22 current smokers; a CAD cohort standing in for the general population).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 464 x 30,000; target: smoking (179 never / 263 former / 22 current).
- Why: Smoking status (never / former / current) from peripheral-blood 450K methylation
- Notes: Tsaprouni et al. 2014.

**CC (2026-11-26, Andrej):** `Not Representative` added.
- Half the 464 people are CAD cases of a cardiac cohort, so the sample stands in for a general population it was
  not drawn from. The fact was already in the risks line; the marker was missing, and the risks and priority lines
  now name it.
- Verdict and priority unchanged.
