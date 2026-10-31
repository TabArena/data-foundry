---
unique_name: fusionai_gene_fusion_ntv2
name: FusionAI-NTv2-GeneFusion (Gene Fusion Breakpoints, NT-v2)
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- AHDS (Artifical/Handmade/Deterministic/Simulated)
- Wrong Domain / Source Modality
- Class-dependent Recording
tags:
- AI-Filled (Verify)
collections:
- TabBench-Bio
source_links:
- https://doi.org/10.1016/j.isci.2021.103164
- https://doi.org/10.5281/zenodo.18713246
- https://arxiv.org/abs/2609.07441
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`Wrong Domain / Source Modality`, `AHDS (Artifical/Handmade/Deterministic/Simulated)`, SEL-12 with SEL-16): 2,048 DNA language-model embedding dimensions of two 10 kb sequences, and half the rows are pseudo-fusions the authors assembled.
- Source: Kim and Zhou, "FusionAI: Predicting fusion breakpoint from DNA sequence with deep learning", iScience 24(10):103164, 2021 (doi 10.1016/j.isci.2021.103164, PMC8501764): "We used these 26K fusions as the positive data. For the negative data, we made pseudo fusion breakpoint sequences by stringent criteria with a similar number of ~26K"; "The input is a sequence of 20 kb one-hot encoded nucleotides" and the model is a CNN. The table under screening is Krupicka's Zenodo release 18713246 (CC BY 4.0, 2026-02-18, "Embeddings and benchmarks results for fusionAI dataset": "calculated middle embeddings derived from raw DNA sequences"), as the benchmark describes it: "FusionAI gene-fusion-breakpoint classification from the published Nucleotide Transformer v2 500M multi-species layer-20 middle-token embeddings ... The two 1024-d partner embeddings are concatenated into 2048 features for 51859 rows (25956 fusion-positive, 25903 pseudo-negative)" (the registry, read 2026-10-31).
- Why out: first, the input is a DNA sequence vectorized by a genomic foundation model, the modality's own tool (SEL-12, as `brca1_variant_effect_evo2`); second, the negative class does not come from a real draw — the negatives are gene pairs the authors combined and filtered, so the two classes differ by construction and not only by biology (SEL-16, with `Class-dependent Recording` as the mechanism). The registry says what that costs: "Negatives are pseudo-fusions assembled from genes not known to participate in fusions, so performance must be interpreted as discrimination under this benchmark construction rather than prospective breakpoint detection" — the source itself states that no prospective decision rests on the score (USE-2).
- The doubt: the positives are real TCGA fusion breakpoints, and a pseudo-negative is the only way such a label can exist; a curator who reads the construction as "how the label comes to exist" (selection.md, "Selection bias", no marker) would keep the task and would still have to answer SEL-12 for the embeddings.
- Siblings and duplicates: `brca1_variant_effect_evo2`, `deeploc2_fungi_membrane_esm2` and `peer_tem1_beta_lactamase_esm2`, the benchmark's other embedding tables (PROV-6 on the construction, different sources). No record of the FusionAI sequences themselves. External collections: TabBench-Bio (`FusionAI-NTv2-GeneFusion`).
- Better data: a candidate of the benchmark TabBench-Bio; no new search this round.
- Papers and pages: Kim and Zhou 2021 (iScience, PMC8501764), its data at https://compbio.uth.edu/FusionGDB2/FusionAI/; Zenodo 18713246; TabBench-Bio (arXiv 2609.07441), Table 4 row FusionAI-NTv2-GeneFusion.
- Metric: the benchmark's own Macro-F1 (Sec. 3.5). The paper reports accuracy and AUROC on its own 70/30 split ("The accuracies for training and test datasets were 97.4% (AUROC = 0.9962) and 90.8% (AUROC = 0.9706)"), two metrics side by side (MET-5). Inputs: the benchmark keeps "connected components of rows sharing an exact partner embedding" within folds, a group it derives rather than ships.
- Reject check (AI, 2026-10-31): stands. FusionAI's STAR Methods: 'we excluded 17,110 genes, which are involved in 48K known human fusion genes ... From the rest of those genes (27,116), which are not known as involved in any fusion genes, we randomly chose two genes as fusion partners' (Kim and Zhou 2021, https://doi.org/10.1016/j.isci.2021.103164, read via Europe PMC). Half the rows are artificial pairings of genes that never occur among the positives, so the class is set by construction and cannot be dropped without losing the task. The source's own model is a CNN on a one-hot '20 kb length DNA sequence'.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 51,859 x 2,048; target: fusion (25,956 positive / 25,903 pseudo-negative).
- Why: Gene-fusion breakpoint vs pseudo-fusion from Nucleotide Transformer v2 embeddings of the two partner sequences
- Notes: Features are DNA language-model embeddings (Zenodo 2026 release by Krupicka for a genomic-foundation-model benchmark); the negatives are constructed pseudo-fusions, so the registry itself warns it is not prospective breakpoint detection. Underlying data: FusionAI (Kim and Zhou 2021).
