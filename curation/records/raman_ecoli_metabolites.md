---
unique_name: raman_ecoli_metabolites
name: Bio-Catalysis Monitoring of AXP
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- TBD
tags:
- AI-Filled (Verify)
- Multi-target
- Many features
collections:
- RamanBench
original_source: Other
problem_type: Regression
source_links:
- https://arxiv.org/abs/2605.02003
- https://huggingface.co/datasets/chlange/HTRamanBioCatalysisAXP
- https://huggingface.co/datasets/HTW-KI-Werkstatt/RamanSpectraEcoliMetabolites
- https://huggingface.co/datasets/HTW-KI-Werkstatt/RamanSpectraEcoliMetabolitesDig4Bio
- https://doi.org/10.1002/bit.70006
- '# Kaggle competition on the Dig4Bio spectra (R2 Score)'
- https://www.kaggle.com/competitions/dig-4-bio-raman-transfer-learning-challenge
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: three calibration sets from one high-throughput Raman platform (TU Berlin), robot-pipetted mixtures whose targets are the pipetting set-points rather than measurements of a process; the record merges three distinct experiments.
- Source: first released on Hugging Face by the authors of the platform paper (Lange et al., Biotechnology and Bioengineering 122(10), 2025, https://doi.org/10.1002/bit.70006): chlange/HTRamanBioCatalysisAXP (created 2026-03-20), HTW-KI-Werkstatt/RamanSpectraEcoliMetabolites (2026-03-03), HTW-KI-Werkstatt/RamanSpectraEcoliMetabolitesDig4Bio (2026-02-27), all CC BY 4.0 and all marked new in RamanBench (Table 16). The Dig4Bio spectra "were used for a Kaggle challenge" (card): the Dig4Bio Raman Transfer Learning Challenge (Kaggle, Community, 172 teams, closed 2025-09-26), so that part was out in 2025 and the year is left empty. As published (parquet schemas read by range requests): AXP 344 spectra x 2,048 bins + adenosine, ADP, AMP, ATP in g/L, each spread evenly over about 0.05-5.0 (Metrohm, 785 nm, a deep eutectic solvent with Tris buffer, A.17.4); E. coli metabolites 1,920 spectra x 594 bins (402-1599 cm-1) + glucose (0.1-10 g/L) and sodium acetate (0.03-2 g/L), 384 samples x 5 scans (card); Dig4Bio 384 spectra x 1,869 bins + glucose, sodium acetate and magnesium acetate (column names; the card and A.17.3 say magnesium sulfate), 192 samples x 2 scans.
- Use case: a lab calibrates a Raman soft sensor for fermentation analytes, or screens enzymes by reading AXP concentrations ("it can serve as an analytic method to evaluate the suitability of different enzymes", A.17.4); fit approximate: "The concentrations that the liquid handling robot was supposed to pipet into the wells were assumed to be the ground truth" (A.17.3; the AXP card says the concentrations "represent the actual values achieved via a Tecan Liquid Handling Robot"), so the rows are designed mixtures with independent concentrations standing in for reaction or broth samples. Regime grouped by sample (several scans per pipetted sample, no sample id; identical target tuples mark them, SPLIT-24).
- Siblings and duplicates: no duplicate (grep for the HF ids, bit.70006, dig-4-bio). The three experiments have different analytes and media: distinct tasks of one platform (PROV-7), so one dataset per experiment or one chosen. Platform siblings: `raman_ecoli_fermentation` (the cultivations), `raman_bioprocess_analytes_anton_532` (the eight-instrument mixtures, the training side of the Kaggle challenge), `raman_bioprocess_substrates` (8-substrate mixtures). External collections: RamanBench (Tables 21, 22; raman-data ids `ht_raman_bio_catalysis_axp`, `ecoli_metabolites`, `ecoli_metabolites_dig4bio`).
- Better data: a candidate of the benchmark RamanBench; no new search (run brief).
- Papers and pages: Lange et al. 2025 (the platform; no AXP or mixture results in its Sec. 2.6.4 and 3.3); the three HF cards; RamanBench A.17.3-A.17.4; the Kaggle competition.
- Metric: for the Dig4Bio part the Kaggle challenge scores "R2 Score" (API `evaluationMetric`), a leaderboard metric (MET-4), but of a transfer task (train on other instruments, predict this plate); for AXP and the binary mixtures none found (cards, RamanBench appendix, Lange 2025), so the fallback `rmse` (MET-1); inputs none.
- Risks for /add-dataset: the target is a set-point, not a measured value (A.17.3 cites [97] for its agreement with enzymatic assays); designed, independent concentrations of handmade samples (a SEL-16 and `Not Representative` question for the curator, not a fast reject: the spectra are real measurements); A.17.3 also calls these mixtures "in-line Raman spectra from E. coli cultivations", a contradiction to settle (PROV-2); three experiments in one record (PROV-6, PROV-7); repeated scans without a sample id (SPLIT-24); raw spectral bins (SEL-15).
- Priority: gap 0, use case 0 (approximate: pipetted mixtures), source + (platform paper, the owners' cards, a competition), shape 0 (192-384 samples per experiment, one feature type), risk - (set-point targets, merged experiments).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark RamanBench (https://arxiv.org/abs/2605.02003).
- as published: 344 spectra x 2,048 wavenumber features; 4 target(s) (raman-data id: ht_raman_bio_catalysis_axp); target: adenosine, ADP, AMP, ATP concentrations (4 targets).
- Why: Quantify adenosine phosphates during biocatalytic reactions in deep eutectic solvent from high-throughput Raman spectra | Quantify E. coli fermentation metabolites in robot-pipetted aqueous mixtures (high-throughput Raman)
- Notes: Raw Raman spectral bins (2,048 wavenumber points, -32-3385 cm-1) as features; SEL-15 judges such signals case by case. New dataset first released with RamanBench (HTW / TU Berlin). Multi-target; RamanBench scores one task per target. HF mirror: ...
