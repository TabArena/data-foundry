---
unique_name: fusionai_gene_fusion_ntv2
name: FusionAI-NTv2-GeneFusion (Gene Fusion Breakpoints, NT-v2)
checked_by:
- AI (UNVERIFIED)
data_foundry_status:
- WIP (Triage)
claimed_by: Andrej
suggestion: 'No'
decision_markers:
- Wrong Domain / Source Modality
- AHDS (Artifical/Handmade/Deterministic/Simulated)
- Class-dependent Recording
tags:
- AI-Filled (Verify)
- Expanding Science Catalogue
- 'Samples: Unknown'
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

**Screening (AI, 2026-11-25):** `No` (`Wrong Domain / Source Modality`, `AHDS (Artifical/Handmade/Deterministic/Simulated)`, `Class-dependent Recording`; SEL-12, with SEL-16): every column is a Nucleotide Transformer embedding of two 10 kb DNA sequences, which cannot be our feature (CLEAN-6), and the source holds no tabular column behind them — the input is DNA, read by the authors with a CNN on "a sequence of 20 kb one-hot encoded nucleotides" (SEL-12); independently, half the rows are pseudo-fusions the authors assembled from a gene pool they had emptied of every gene ever seen in a fusion, so the classes differ by construction (SEL-16).
- Source: Kim and Zhou, "FusionAI: Predicting fusion breakpoint from DNA sequence with deep learning", iScience 24(10):103164, 2021 (doi 10.1016/j.isci.2021.103164, PMC8501764): the positives are FusionGDB breakpoints, "~33K fusion genes from the TCGA cohort" of the "48K" downloaded, "We used these 26K fusions as the positive data"; "For the negative data, we made pseudo fusion breakpoint sequences by stringent criteria with a similar number of ~26K", built after "we excluded 17,110 genes, which are involved in 48K known human fusion genes ... From the rest of those genes (27,116), which are not known as involved in any fusion genes, we randomly chose two genes as fusion partners"; the model is a CNN whose "input ... is a sequence of 20 kb one-hot encoded nucleotides". The table under screening is Krupicka's Zenodo release 18713246 (CC BY 4.0, 2026-02-18, "Embeddings and benchmarks results for fusionAI dataset": "calculated middle embeddings derived from raw DNA sequences"), as the benchmark describes it: "FusionAI gene-fusion-breakpoint classification from the published Nucleotide Transformer v2 500M multi-species layer-20 middle-token embeddings ... The two 1024-d partner embeddings are concatenated into 2048 features for 51859 rows (25956 fusion-positive, 25903 pseudo-negative)" (the registry, read 2026-10-31).
- Use case: none the source stands behind: the registry says the score is "discrimination under this benchmark construction rather than prospective breakpoint detection" (USE-2); collection `Samples: Unknown` (the positives are FusionGDB's TCGA fusions, but no date per row was found, and the negatives have none by construction; a fact the source does not settle is `Unknown`); type `Expanding Science Catalogue` for the positives (a cut of a growing fusion database, SPLIT-34, rule 4), the negatives being made rather than collected.
- Split: leaf L-FAMILY.key (Grouped · `UnseenGroup`, the partner gene) if it were built: [CAT.next-items] yes (no scope stated), [CAT.entry-date] no (no dated entries found), [FAMILY.key] yes (the partner genes; TabBench-Bio keeps "connected components of rows sharing an exact partner embedding" within folds); open: none for the verdict.
- Why out: first, nothing tabular is left. Once the embeddings leave (CLEAN-6; as source columns computed from a structure leave a SMILES task, CLEAN-24), the row is two 10 kb genomic windows, which no declared feature type covers and which the field reads with sequence models — the source's own CNN on 20 kb of one-hot nucleotides, 90.8% accuracy and AUROC 0.9706 on its held-out 30% (SEL-12, as on `deeploc2_fungi_membrane_esm2` and `peer_tem1_beta_lactamase_esm2`; 20 kb is far past the `splice`-style positional table that keeps a short fixed window in scope). Second, and on its own: the negative class is not a draw from anything. The authors emptied the pool first — the 17,110 genes involved in any known fusion are excluded, the pairs come from the remaining 27,116 "which are not known as involved in any fusion genes" — so the two classes are built from disjoint gene sets and the partner's identity alone tells them apart, before any breakpoint is looked at; the embeddings are per partner gene (the benchmark groups rows "sharing an exact partner embedding", so the same gene's 1,024 values recur across rows), which is exactly the column that carries the construction. A model learns which genes ever fuse, not where a breakpoint lies, and the negatives cannot be dropped without losing the task (SEL-16; `Class-dependent Recording` as the mechanism, the LEAK-14 shape of one class through a separate route, unfixable as in LEAK-15).
- The doubt: the positives are real TCGA breakpoints, and a pseudo-negative is the only way such a label can exist; `ecoli_sigma70_promoters_regulondb` is the weighed counter-case — its negatives are constructed too and it stays a candidate with `Selection Bias`, priority 2. What separates them is that its negatives are real genome windows sampled from the organism a scan would meet, so the rows exist and only the population differs (selection.md, "Selection bias"), while a pseudo-fusion is a pair the authors made and the pool it was drawn from was defined by the label. And even for a curator who reads the construction as how the label comes to exist, SEL-12 still decides: the source holds no tabular column beside the gene pair and its coordinates.
- Siblings and duplicates: `brca1_variant_effect_evo2`, `deeploc2_fungi_membrane_esm2` and `peer_tem1_beta_lactamase_esm2`, the benchmark's other embedding tables (different sources); `ecoli_sigma70_promoters_regulondb` (`TBD -> 2nd Tier`), constructed negatives kept as a candidate; `splice` (`Yes`), the short DNA window that stays in scope. No record of the FusionAI sequences themselves. External collections: TabBench-Bio (`FusionAI-NTv2-GeneFusion`).
- Better data: a candidate of the benchmark TabBench-Bio; no new search this round.
- Papers and pages: Kim and Zhou 2021 (iScience, PMC8501764), its data at https://compbio.uth.edu/FusionGDB2/FusionAI/; Zenodo 18713246; TabBench-Bio (arXiv 2609.07441), Table 4 row FusionAI-NTv2-GeneFusion.
- Metric: the benchmark's own Macro-F1 (Sec. 3.5). The paper reports accuracy and AUROC on its own 70/30 split ("The accuracies for training and test datasets were 97.4% (AUROC = 0.9962)" and 90.8% with AUROC 0.9706), two metrics side by side (MET-5). Inputs: the partner-gene group, derived rather than shipped.
- Reject check (AI, 2026-11-25): stands, on two independent grounds. The paper's STAR Methods were re-read in full this round: the negative pairs are drawn only from the 27,116 genes left after "we excluded 17,110 genes, which are involved in 48K known human fusion genes", so the classes come from disjoint gene pools and the partner embedding — which the benchmark itself treats as a gene key, grouping rows that share one exactly — carries the label before any breakpoint is read (SEL-16, with `Class-dependent Recording` for the mechanism; the registry concedes the point: "discrimination under this benchmark construction rather than prospective breakpoint detection"). The counter-case was checked and does not transfer: `ecoli_sigma70_promoters_regulondb` keeps constructed negatives that are real genome windows, while a pseudo-fusion is an object the authors made. Independently, the lead reason needs none of that argument: CLEAN-6 bars the 2,048 embedding dimensions, and behind them lies 20 kb of DNA with no tabular column in the source, which the authors themselves read with a CNN on one-hot nucleotides (SEL-12).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 51,859 x 2,048; target: fusion (25,956 positive / 25,903 pseudo-negative).
- Why: Gene-fusion breakpoint vs pseudo-fusion from Nucleotide Transformer v2 embeddings of the two partner sequences
- Notes: Features are DNA language-model embeddings (Zenodo 2026 release by Krupicka for a genomic-foundation-model benchmark); the negatives are constructed pseudo-fusions, so the registry itself warns it is not prospective breakpoint detection. Underlying data: FusionAI (Kim and Zhou 2021).
