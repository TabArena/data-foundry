---
unique_name: peer_tem1_beta_lactamase_esm2
name: local-PEER-BetaLactamase-ESM2 (TEM-1 Activity, ESM-2)
checked_by:
- AI (UNVERIFIED)
data_foundry_status:
- WIP (Triage)
claimed_by: Andrej
suggestion: 'No'
decision_markers:
- Wrong Domain / Source Modality
tags:
- AI-Filled (Verify)
- Experimental Results
- 'Samples: No Time Dimension'
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

**Screening (AI, 2026-11-25):** `No` (`Wrong Domain / Source Modality`, SEL-12): on this exact task PEER measures sequence models clearly ahead — fine-tuned ESM-1b 0.839 and a CNN on the sequence 0.781 Spearman, against 0.528 for the frozen language model with a head, the setting of this table (PEER, Table 3); every column is a mean-pooled ESM-2 embedding of a mutant's sequence, which cannot be our feature (CLEAN-6), and what remains is one protein's missense sequences.
- Source: Firnberg et al., "A Comprehensive, High-Resolution Map of a Gene's Fitness Landscape", Mol Biol Evol 31:1581-1592 (2014; doi 10.1093/molbev/msu081), the deep mutational scan of TEM-1 beta-lactamase; PEER (Xu et al. 2022, arXiv 2206.02096, Sec. 3.1) defines the task: "The sequences of mutants along with their labels are taken from Envision", the target "the experimentally tested fitness score which records the scaled mutation effect for each mutant", splits 4,158 / 520 / 520 (Table 1). TabBench-Bio (App. G.1): "The PEER TEM-1 dataset combines the official training, validation, and test files into 5,198 unique single-mutant sequences", embedded with "the pinned facebook/esm2_t33_650M_UR50D revision" and "mean-pooled its 1,280-dimensional residue representations"; "the position of the sole amino-acid substitution defines 286 cross-validation groups". As published by TabBench-Bio: 5,198 x 1,280 (GitHub release v0.1.0 parquet), target `activity`.
- Use case: a protein engineer ranking untested substitutions of TEM-1 before building them; fit approximate (the scan already measures nearly every single substitution); collection `Samples: No Time Dimension`: one designed mutant library measured by one selection experiment, the target read from it, no row dated; type `Experimental Results` (a designed library, SPLIT-34).
- Split: leaf L-EXP.kind (Grouped · `UnseenGroup`, the mutated position) because [EXP.meets] a kind the data does not contain (substitutions at positions not measured), [EXP.kind-key] yes (the position, 286 groups, as TabBench-Bio groups); open: none for the verdict.
- Why out: once the embeddings leave as features (CLEAN-6; as source columns computed from a structure leave a SMILES task, CLEAN-24: "the real task here is going from smiles to a prediction"), the input is the mutant's amino-acid sequence, and on this task the sequence models are measured clearly better than both the frozen embedding with a head (0.528) and hand-made sequence features (DDE 0.623): CNN 0.781, fine-tuned ESM-1b 0.839, the literature column 0.89 (PEER, Table 3; SEL-12). Precedent: `protein_location_prediction_challenge` (`No`, `Wrong Domain / Source Modality`: the organisers shipped ESM-1b embeddings, still a sequence task), with `instadeep_enzyme_classification_challenge` and `instadeep_kinase_classification_challenge`; the line, as `huesken_sirna_efficacy`'s precedent check of 2026-11-04 puts it, is "a raw full-length string or a learned embedding goes out; aligned positions or fixed-rule descriptors stay in", and it names PEER's 0.839 against 0.528 as the one place where the gap was measured.
- Not the positional route either: a single-mutant library of one 286-residue protein is a fixed-length sequence, so the `splice` / `huesken_sirna_efficacy` treatment (one categorical column per position) is open in principle — but for single mutants that table is exactly (position, substituted residue) written out, and under this task's own split, whole positions held out (286 groups, [L-EXP.kind]), a test row's position column is constant in training, so nothing but the bare substituted residue reaches the model, while the CNN and the language model carry residue context and chemistry across positions. That is what the measured gap looks like from the data's side.
- The doubt, and what sets `brca1_variant_effect_evo2` apart: both are one gene's saturation mutagenesis. For BRCA1 the source's best model is a classifier on the pooled embedding vector, Findlay's table keeps tabular variant columns whose consequence classes (nonsense, splice, synonymous) carry much of the label and keep carrying it in held-out regions, and nothing measures sequence models clearly ahead; here the mutants are missense only, the held-out position strips the one other column, and PEER measures the gap. A variant table of TEM-1 with per-variant descriptors (Envision's 27 features, Gray et al. 2018, https://pubmed.ncbi.nlm.nih.gov/29226803/) would be its own candidate (PROV-11), not a fix of this record.
- Not the reason: the target is a real measurement and the grouping by mutated position is sound.
- Siblings and duplicates: `deeploc2_fungi_membrane_esm2`, `brca1_variant_effect_evo2`, `fusionai_gene_fusion_ntv2` (TabBench-Bio's other embedding tables; the same question); `splice`, `huesken_sirna_efficacy`, `ecoli_proteins` (`Yes`), the kept side of the line. External collections: TabBench-Bio (Table 4; App. G.1), PEER.
- Better data: a candidate of the benchmark TabBench-Bio (the run searched no further).
- Papers and pages: Firnberg et al. 2014; PEER (https://arxiv.org/html/2206.02096v2), Tables 1 and 3; Envision (Gray et al. 2018); TabBench-Bio (arXiv 2609.07441), App. G.1; the release asset https://github.com/not-a-feature/TabBench-Bio/releases/download/v0.1.0/peer_beta_lactamase_esm2_t33.parquet.
- Metric: PEER scores the task by Spearman's rho (Table 1), its one metric for the task (MET-5); TabBench-Bio ranks regression by RMSE, a benchmark convention. Inputs: none beyond the position group, which ships.
- Reject check (AI, 2026-11-25): stands. PEER's Beta-lactamase column was re-read this round and the gap is the source's own: frozen ESM-1b 0.528 (0.009) — "Used as a feature extractor with pre-trained weights frozen", which is what this table is — against CNN 0.781 (0.011), fine-tuned ESM-1b 0.839 (0.053) and a literature 0.89, with DDE at 0.623 the best hand-made sequence features. The one way back in was checked and closes: TEM-1's single mutants are a fixed-length sequence, but a positional table of them is (position, substituted residue) by another name, and the benchmark's own split holds whole positions out, so that table is empty where it must predict. CLEAN-6 bars the shipped columns, so there is no fix inside this record; a TEM-1 variant table with Envision's descriptors would be its own candidate (PROV-11).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 5,198 x 1,280; target: activity (scaled_effect1).
- Why: Fitness (scaled activity) of TEM-1 beta-lactamase single mutants (deep mutational scan, Firnberg et al. 2014; PEER task) from protein language-model embeddings
- Notes: Built by the authors: mean-pooled ESM-2 650M embeddings of the mutant sequence. Grouped by mutated position (286 groups). Benchmark task source: PEER (arXiv 2206.02096).
