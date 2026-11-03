---
unique_name: peer_tem1_beta_lactamase_esm2
name: local-PEER-BetaLactamase-ESM2 (TEM-1 Activity, ESM-2)
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Wrong Domain / Source Modality
tags:
- AI-Filled (Verify)
collections:
- TabBench-Bio
source_links:
- https://doi.org/10.1093/molbev/msu081
- https://github.com/not-a-feature/TabBench-Bio/releases/download/v0.1.0/peer_beta_lactamase_esm2_t33.parquet
- https://arxiv.org/abs/2609.07441
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`Wrong Domain / Source Modality`; SEL-12): the activity of 5,198 TEM-1 beta-lactamase single mutants from mean-pooled ESM-2 embeddings of each mutant's sequence, a table TabBench-Bio built with a protein language model; the input is a protein sequence, and sequence models are clearly better on this task (PEER, Table 3).
- Source: Firnberg et al., "A Comprehensive, High-Resolution Map of a Gene's Fitness Landscape", Mol Biol Evol 31:1581-1592 (2014; doi 10.1093/molbev/msu081), the deep mutational scan; PEER (Xu et al. 2022, arXiv 2206.02096, Sec. 3.1) defines the task: "The sequences of mutants along with their labels are taken from Envision", the target "the experimentally tested fitness score which records the scaled mutation effect for each mutant", splits 4,158 / 520 / 520 (Table 1). TabBench-Bio (App. G.1): "The PEER TEM-1 dataset combines the official training, validation, and test files into 5,198 unique single-mutant sequences", embedded with "the pinned facebook/esm2_t33_650M_UR50D revision" and "mean-pooled its 1,280-dimensional residue representations"; "the position of the sole amino-acid substitution defines 286 cross-validation groups". As published by TabBench-Bio: 5,198 x 1,280 (GitHub release v0.1.0 parquet), target `activity`.
- Why out: every feature is the output of a language model run on the sequence; nothing was measured on the protein but the target. On this task, PEER Table 3 (Spearman's rho) gives fine-tuned ESM-1b 0.839 and a CNN on the sequence 0.781, against 0.528 for frozen ESM-1b with a head ("Used as a feature extractor with pre-trained weights frozen"), the setting this table freezes in. Sequence models are clearly better (SEL-12). Precedent: `protein_location_prediction_challenge` (`No`, `Wrong Domain / Source Modality`: the organisers shipped ESM-1b embeddings, still a sequence task), with `instadeep_enzyme_classification_challenge` and `instadeep_kinase_classification_challenge`.
- Siblings and duplicates: `deeploc2_fungi_membrane_esm2`, `brca1_variant_effect_evo2`, `fusionai_gene_fusion_ntv2` (TabBench-Bio's other embedding tables, screened in another batch; the same question). External collections: TabBench-Bio (Table 4; App. G.1), PEER.
- Better data: a candidate of the benchmark TabBench-Bio (the run searched no further).
- Metric: PEER scores the task by Spearman's rho (Table 1), its one metric for the task; TabBench-Bio ranks regression by RMSE.
- Not the reason: the target is a real measurement and the grouping by mutated position is sound; the problem is the input modality.
- Reject check (AI, 2026-10-31): stands. PEER Table 3 on this task (Spearman): fine-tuned ESM-1b 0.839, CNN on the sequence 0.781, frozen ESM-1b ('Used as a feature extractor with pre-trained weights frozen') 0.528, DDE features 0.623 (https://arxiv.org/html/2206.02096v2): the sequence models are clearly better. Every column is a learned embedding (TabBench-Bio App. G.1), which CLEAN-6 bars as a feature, so no fix inside the record. For the curator, not a rescue: PEER's labels come from Envision, a 'stochastic gradient boosting' model with 27 features per variant (https://pubmed.ncbi.nlm.nih.gov/29226803/); such a table would be its own candidate (PROV-11).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 5,198 x 1,280; target: activity (scaled_effect1).
- Why: Fitness (scaled activity) of TEM-1 beta-lactamase single mutants (deep mutational scan, Firnberg et al. 2014; PEER task) from protein language-model embeddings
- Notes: Built by the authors: mean-pooled ESM-2 650M embeddings of the mutant sequence. Grouped by mutated position (286 groups). Benchmark task source: PEER (arXiv 2206.02096).
