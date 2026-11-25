---
unique_name: brca1_variant_effect_evo2
name: local-BRCA_Evo2-VEP (BRCA VEP, Evo2)
checked_by:
- AI (UNVERIFIED)
data_foundry_status:
- WIP (Triage)
claimed_by: Andrej
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- Wrong Domain / Source Modality
tags:
- AI-Filled (Verify)
- 'Samples: No Time Dimension'
- Experimental Results
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

**Screening (AI, 2026-11-25):** `TBD -> 2nd Tier`, priority 2: function classes of 3,893 BRCA1 single-nucleotide variants from saturation genome editing (Findlay et al., Nature 2018); a candidate on Findlay's own variant table (position, alleles, consequence), not on the 8,192 Evo2-7B embedding dimensions TabBench-Bio ships, which cannot be our features (CLEAN-6); whether tabular models are competitive on that table against Evo 2 is the open SEL-12 question.
- Source: Findlay, Daza, Martin, Zhang, Leith, Gasperini, Janizek, Huang, Starita and Shendure, "Accurate classification of BRCA1 variants with saturation genome editing", Nature 562:217-222, 2018 (https://doi.org/10.1038/s41586-018-0461-z, PMC6181777): they "assay 96.5% of all possible single nucleotide variants (SNVs) in 13 exons", 3,893 SNVs scored; "Function scores were bimodally distributed"; the classes are thresholds on P_nf, the posterior probability that a score comes from the non-functional distribution (above 0.99 non-functional, below 0.01 functional, intermediate between), 72.5% functional, 21.1% non-functional, 6.4% intermediate; the per-SNV scores are Supplementary Table 1, which the Evo 2 tutorial reads as `chrom`, `pos`, `ref`, `alt`, `score` and `class` (FUNC, INT, LOF; NVIDIA BioNeMo notebook, read 2026-11-25); its other columns were not read. As built by TabBench-Bio (registry `local-BRCA_Evo2-VEP`, read 2026-10-31): "concat of mean-pooled reference and variant sequence embeddings (4096+4096=8192-d) ... Target y=func.class (FUNC/LOF/INT). 3893x8192", group column `group_id`, a hash of the reference sequence (App. G.1).
- Use case: a clinical laboratory classifying a BRCA1 variant of uncertain significance, the problem Findlay et al. set out to solve ("Variants of uncertain significance fundamentally limit the clinical utility of genetic information"); fit approximate: the 13 exons are almost fully assayed, so a predictor stands for variants outside the assayed regions; collection `Samples: No Time Dimension`: one designed experiment that edits every possible SNV of the exons into a cell line and reads the function score from cell survival; the target exists with the experiment, no row is dated; type `Experimental Results` (a designed library of variants, SPLIT-34).
- Split: leaf L-EXP.kind (Grouped · `UnseenGroup`, the region) because [EXP.meets] a kind the data does not contain (variants of exons or regions not assayed), [EXP.kind-key] yes (the exon or the editing region, computable from the position, 13 exons); open: the enough-groups check on 13 exons with LOF present in every test fold, and whether the group is the exon or TabBench-Bio's reference window.
- Siblings and duplicates: no other record of the Findlay data (grep for findlay, brca1, saturation genome, 2026-11-25). TabBench-Bio's other embedding tables, each from a different source: `deeploc2_fungi_membrane_esm2`, `peer_tem1_beta_lactamase_esm2` and `fusionai_gene_fusion_ntv2` (`No`, SEL-12, AI-screened, reject checks stood; proposed again 2026-11-25). The same reading applies to all four: the embedding columns leave (CLEAN-6; as source columns computed from a molecule's structure leave a SMILES task, CLEAN-24, "the real task here is going from smiles to a prediction"), and the question is what tabular task the source's own table holds without them. DeepLoc's file holds only the sequence and the kingdom; PEER's mutants are one protein's missense sequences, where its Table 3 measures sequence models clearly ahead; FusionAI's negatives are constructed. Findlay's table holds the variant's position and alleles, from which a fixed annotation gives the consequence (synonymous, missense, nonsense, splice), and no source measures a tabular model on them against Evo 2. External collections: TabBench-Bio (`local-BRCA_Evo2-VEP`, enabled).
- Better data: a candidate of the benchmark TabBench-Bio; no new search beyond a quick look (saturation genome editing of other genes, such as BRCA2 or other MAVE sets, would be other tasks, PROV-7).
- Papers and pages: Findlay et al. 2018; Evo 2 (Brixi et al., bioRxiv 10.1101/2025.02.18.638918), Sec. 2.3 (re-read 2026-11-25): "a supervised deep neural network trained specifically on BRCA1 variants" on Evo 2 40B embeddings, AUROC 0.94 and AUPRC 0.84 for coding SNVs (0.95 and 0.86 on all SNVs), test N = 779, the split procedure not given in the visible text; zero-shot Evo 2 "performed strongly for coding SNVs"; TabBench-Bio (Kreuer et al., https://arxiv.org/abs/2609.07441), App. G.1; the release asset (in `source_links`).
- Metric: none from the data's source (Findlay et al. assay the variants; their ROC against ClinVar, 96.7% sensitivity at 98.2% specificity, scores the assay). The Evo 2 paper reports AUROC and AUPRC for LOF against the rest, and TabBench-Bio's "Macro-F1 is the primary classification metric" (Sec. 3.5) is a benchmark convention (MET-5), so the fallback on the framing that ships (MET-8). Inputs: the group (exon), computable from the position.
- Risks for /add-dataset: (1) build from Findlay's Supplementary Table 1 (PROV-8): position, alleles and the consequence from a fixed annotation; the embeddings do not ship (CLEAN-6); drop the function and RNA scores and P_nf, which make or accompany the label (SEL-5, LEAK-10). (2) SEL-12 measured: a tabular model on the variant columns against Evo 2 zero-shot on a split grouped by exon; if Evo 2 is clearly better, `No` with `Wrong Domain / Source Modality`. (3) FUNC/INT/LOF is a threshold of the measured score: ship the classes or the score (USE-5); the Evo 2 framing is LOF against the rest. (4) The consequence carries much of the class (nonsense and canonical splice mostly LOF, synonymous mostly FUNC): a check that the task is not trivial on it (TP rules).
- Priority: gap + (multiclass classification is thin, 22 accepted), use case 0 (approximate: the assay already covers the exons), source + (a Nature paper with the per-SNV supplement), shape 0 (3,893 SNVs and a handful of variant columns once the embeddings leave), risk - (SEL-12 unmeasured against Evo 2; the shipped features drop).

**Consistency check (AI, 2026-10-31):** this record stays a candidate while `protein_location_prediction_challenge` and `deeploc2_fungi_membrane_esm2` (both `No`, SEL-12, AI-screened with reject checks that stood) were rejected as sequence-embedding tables. What sets it apart? (a) The AI's best guess: the field's best BRCA1 predictor is a supervised classifier on the pooled embedding vector (Evo 2, Sec. 2.3), while DeepLoc 2.0 pools by learned attention over the residues and PEER shows frozen embeddings clearly behind (`peer_tem1_beta_lactamase_esm2`); and Findlay's table has variant columns besides the sequence. (b) Treat it like them: `No`, SEL-12. (c) Reopen them. (d) Amend SEL-12 or CLEAN-6 to say whether a third-party embedding table may ship.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 3,893 x 8,192; target: y = func.class (FUNC / INT / LOF).
- Why: BRCA1 variant function class (saturation genome editing, Findlay et al. 2018) from DNA language-model embeddings
- Notes: Built by the authors: features are mean-pooled Evo2-7B embeddings of the reference and variant sequences (4,096 + 4,096), not measured variables. Groups by reference-sequence hash. The paper's table says C; the registry says multiclass.
