---
unique_name: gse42861_rheumatoid_arthritis_methylation
name: GEO-GSE42861-Methylation-RA (Rheumatoid Arthritis DNA Methylation)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- Selection Bias
tags:
- AI-Filled (Verify)
- Many features
- 'Samples: Over Time'
- 'Time: Lost'
- Clinical Study
collections:
- TabBench-Bio
original_source: Other
year: '2013'
domain: medical & healthcare
problem_type: Binary Classification
source_links:
- https://doi.org/10.1038/nbt.2487
- https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE42861
- https://arxiv.org/abs/2609.07441
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-11-25):** `TBD -> 2nd Tier`, priority 1: incident, untreated ACPA-positive rheumatoid arthritis against healthy matched controls from 450K blood methylation (Liu et al. 2013); a real diagnosis, but published for association, against healthy controls rather than other arthritis, with cases and controls run on different dates.
- Source: Liu, Aryee, Padyukov et al., "Epigenome-wide association data implicate DNA methylation as an intermediary of genetic risk in rheumatoid arthritis", Nat Biotechnol 31(2):142-147, 2013 (https://doi.org/10.1038/nbt.2487, read on PMC3598632); data GEO GSE42861, public 2013-01-21. As published (series matrix, re-read 2026-11-25): 689 peripheral-blood-leukocyte samples (354 RA, 335 normal), every one "extracted and purified from PBLs using Qiagen DNeasy Kit" (one protocol for both classes), with `disease state`, `age`, `gender` and `smoking status`; a processed matrix, methylated and unmethylated signal matrices, and IDATs whose names carry the BeadChip barcode (72 chips).
- Use case: a rheumatologist at a patient's first visit deciding whether the arthritis is RA; the cases fit that moment ("Cases were recruited at the first visit to a rheumatology clinic before initiation of treatment", Results), but the controls are healthy people "matched by sex, age, smoking status and residence area", not patients with other arthritis, and every case is ACPA positive, so the serology that decides the diagnosis today already defines the cases; fit approximate at best (USE-8). Collection: incident cases and population controls of the Swedish EIRA case-control study, recruited over time with no date per sample (`Samples: Over Time`, `Time: Lost`); the diagnosis exists with the blood draw (no target tag); one sample per person. Type Clinical Study.
- Split: leaf L-FORCED.random (Random · `ForcedIIDFromTemporal`) because [CLI.meets] is a clinic's later patients, [CLI.dated] is no, [ORDER.order] finds no recruitment order (the chip barcodes order the lab run), [FORCED.test] can measure nothing, [FORCED.reason] and [FORCED.risk] are a person's (answered no), and [FORCED.groups] has no repeated unit or period; open: whether the chip or the scan date in the IDATs should group as a batch key, given the run-date imbalance below.
- Siblings and duplicates: no other RA methylation record; GSE207605 re-analyses it with `gse40279_methylation_age` and `gse147221_schizophrenia_methylation`. External collections: TabBench-Bio (Table 4).
- Better data: none found (quick look; the 2026-10-31 run searched no further).
- Papers and pages: Liu et al. 2013 (above); GEO lists a second paper on the series (PubMed 29921915), not read.
- Metric: none found: an association and mediation study with no classifier (read on PMC3598632), so the fallback `roc_auc` (MET-1, MET-8). Inputs none.
- Risks for /add-dataset: "there was an imbalance between the number of cases and controls run per date", and assay date moved overall methylation (Discussion): a recording route linked to the label, to probe with the chip and scan date from the IDATs (LEAK-15, LEAK-39; `Class-dependent Recording` if confirmed; unlike `gse147221_schizophrenia_methylation`, sample type and extraction are the same for both classes); cases from clinics against population controls (`Selection Bias`, USE-8); the processed matrix normalised over all samples (LEAK-30, weak; IDATs allow a per-sample rebuild, PROV-13); 485k probes, no subset chosen on the target (CLEAN-22, LEAK-31).
- Priority: gap 0 (medical not thin, binary not thin), use case 0 (approximate: healthy controls, ACPA already decides), source + (paper and GEO), shape 0 (689 rows), risk - (cases and controls run on different dates).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 689 x 30,000 (of 485,577 probes; 30,000 complete probes picked by probe-ID hash); target: disease state (354 RA / 335 normal).
- Why: Rheumatoid arthritis vs control from peripheral-blood leukocyte 450K methylation beta values
- Notes: Liu et al. 2013.
