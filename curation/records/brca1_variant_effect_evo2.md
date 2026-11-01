---
unique_name: brca1_variant_effect_evo2
name: local-BRCA_Evo2-VEP (BRCA VEP, Evo2)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- Wrong Domain / Source Modality
tags:
- AI-Filled (Verify)
collections:
- TabBench-Bio
original_source: Other
year: '2018'
domain: biology & life sciences
required_split:
- Grouped (NON-IID)
source_links:
- https://doi.org/10.1038/s41586-018-0461-z
- https://github.com/not-a-feature/TabBench-Bio/releases/download/v0.1.0/brca_evo2_vep.parquet
- https://arxiv.org/abs/2609.07441
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: 3,893 BRCA1 SNVs with function classes from saturation genome editing (Findlay et al., Nature 2018), shipped by TabBench-Bio as 8,192 Evo2-7B embedding dimensions. The SEL-12 reject was refuted because the field's best BRCA1 predictor is a supervised classifier on such embeddings, so whether tabular models are competitive needs a measurement; which features may ship is the open doubt.
- Proposed reject (refuted): `No` (`Wrong Domain / Source Modality`, SEL-12): every column is a dimension of a DNA language model's hidden state over an 8.2 kb sequence, a modality whose own models are the tool. Reject check (AI, 2026-10-31): refuted. The reject rested on "Evo2 scores BRCA1 variants directly", but the Evo 2 paper's best BRCA1 result is this table's own construction: "Evo 2 embeddings are extracted and concatenated to train a supervised classifier for BRCA1 variant effect prediction", AUROC 0.94 and AUPRC 0.84 on the coding-SNV test set (Brixi et al. 2025, Sec. 2.3, Fig. 3, https://www.biorxiv.org/content/10.1101/2025.02.18.638918v1.full). SEL-12 allows vectorized data where tabular models are competitive, which needs a measurement. The source, Findlay 2018, is a per-SNV table with no other record.
- Source: Findlay, Daza, Martin, Zhang, Leith, Gasperini, Janizek, Huang, Starita and Shendure, "Accurate classification of BRCA1 variants with saturation genome editing", Nature 562:217-222, 2018 (https://doi.org/10.1038/s41586-018-0461-z, PMC6181777): they "assay 96.5% of all possible single nucleotide variants (SNVs) in 13 exons", 3,893 SNVs scored; "Function scores were bimodally distributed"; the classes are thresholds on P_nf, the posterior probability that a score comes from the non-functional distribution (above 0.99 non-functional, below 0.01 functional, intermediate between), 72.5% functional, 21.1% non-functional, 6.4% intermediate; the per-SNV scores are Supplementary Table 1. As built by TabBench-Bio (registry `local-BRCA_Evo2-VEP`, read 2026-10-31): "concat of mean-pooled reference and variant sequence embeddings (4096+4096=8192-d) ... Target y=func.class (FUNC/LOF/INT). 3893x8192", group column `group_id`, a hash of the reference sequence (App. G.1); its DNABERT-2 and NT-v2 builds of the same rows are disabled.
- Use case: a clinical laboratory classifying a BRCA1 variant of uncertain significance, the problem Findlay et al. set out to solve ("Variants of uncertain significance fundamentally limit the clinical utility of genetic information"). For a predictor the fit is approximate: the 13 exons are almost fully assayed, so a prediction stands for variants outside the assayed regions. Regime grouped, by exon or reference window, so a test fold stands for an unassayed region.
- Siblings and duplicates: no other record of the Findlay data (grep for findlay, brca1, saturation genome). TabBench-Bio's other embedding tables, each from a different source: `deeploc2_fungi_membrane_esm2`, `peer_tem1_beta_lactamase_esm2` and `fusionai_gene_fusion_ntv2` (all `No`, SEL-12, AI-screened, reject checks stood). External collections: TabBench-Bio (`local-BRCA_Evo2-VEP`, enabled).
- Better data: a candidate of the benchmark TabBench-Bio; no further search this round.
- Papers and pages: Findlay et al. 2018; Evo 2 (Brixi et al., bioRxiv 10.1101/2025.02.18.638918), Sec. 2.3: embeddings of the 40B model, loss of function against functional and intermediate, test N = 779; TabBench-Bio (Kreuer et al., https://arxiv.org/abs/2609.07441), App. G.1; the release asset (in `source_links`).
- Metric: none from the data's source (Findlay et al. assay the variants; their ROC against ClinVar, 96.7% sensitivity at 98.2% specificity, scores the assay). The Evo 2 paper reports AUROC and AUPRC for LOF against the rest, and TabBench-Bio's "Macro-F1 is the primary classification metric" (Sec. 3.5) is a benchmark convention (MET-5), so the fallback on the framing that ships. Input: the group column, which ships.
- Risks for /add-dataset: (1) the source table is Findlay's per-SNV data (PROV-8): ship its variant columns (position, alleles, consequence where published) and decide whether third-party Evo2 embeddings may ship at all (CLEAN-6 bars building them ourselves); drop the function and RNA scores that make or accompany the label (SEL-5, LEAK-10). (2) SEL-12 measured: a tabular model on the shipped features against Evo 2 zero-shot and the paper's embedding classifier, on a split grouped by exon or reference window. (3) FUNC/INT/LOF is a threshold of the measured score: ship the classes or the score (USE-5). (4) Supplementary Table 1's columns not read here.
- Priority: gap + (multiclass thin), use case 0 (approximate: the assay already covers the exons), source + (a Nature paper with the per-SNV supplement), shape 0 (3,893 SNVs, but what ships is open: 8,192 embedding dimensions or a handful of variant columns), risk - (third-party embeddings as the features, SEL-12 unmeasured).

**Consistency check (AI, 2026-10-31):** this record stays a candidate while `protein_location_prediction_challenge` and `deeploc2_fungi_membrane_esm2` (both `No`, SEL-12, AI-screened with reject checks that stood) were rejected as sequence-embedding tables. What sets it apart? (a) The AI's best guess: the field's best BRCA1 predictor is a supervised classifier on the pooled embedding vector (Evo 2, Sec. 2.3), while DeepLoc 2.0 pools by learned attention over the residues and PEER shows frozen embeddings clearly behind (`peer_tem1_beta_lactamase_esm2`); and Findlay's table has variant columns besides the sequence. (b) Treat it like them: `No`, SEL-12. (c) Reopen them. (d) Amend SEL-12 or CLEAN-6 to say whether a third-party embedding table may ship.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 3,893 x 8,192; target: y = func.class (FUNC / INT / LOF).
- Why: BRCA1 variant function class (saturation genome editing, Findlay et al. 2018) from DNA language-model embeddings
- Notes: Built by the authors: features are mean-pooled Evo2-7B embeddings of the reference and variant sequences (4,096 + 4,096), not measured variables. Groups by reference-sequence hash. The paper's table says C; the registry says multiclass.
