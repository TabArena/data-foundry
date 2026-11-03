---
unique_name: deeploc2_fungi_membrane_esm2
name: local-DeepLoc2-Fungi-ESM2 (DeepLoc2 Fungi, ESM-2)
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
- https://doi.org/10.1093/nar/gkac278
- https://github.com/not-a-feature/TabBench-Bio/releases/download/v0.1.0/deeploc2_fungi_esm2_t33.parquet
- https://arxiv.org/abs/2609.07441
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`Wrong Domain / Source Modality`, SEL-12): the only input is a protein sequence, turned into 1,280 ESM-2 embedding dimensions; it is the task `protein_location_prediction_challenge` was rejected for, with a newer language model.
- Source: the labels and sequences come from Thumuluri, Almagro Armenteros, Johansen, Nielsen and Winther, "DeepLoc 2.0: multi-label subcellular localization prediction using protein language models", Nucleic Acids Research 50(W1):W228-W234, 2022 (doi 10.1093/nar/gkac278, PMC9252801); its Swiss-Prot training and validation file has the columns ACC, Kingdom, Partition, Membrane, the ten location columns and Sequence (header previewed from services.healthtech.dtu.dk, 2026-10-31), so the input beside the kingdom is the amino-acid string. The table under screening was built by TabBench-Bio: "Complete fungal subset of the official DeepLoc 2.0 Swiss-Prot training/validation data: 5841 unique proteins (1306 membrane-associated, 4535 soluble). Features are 1280-d residue-mean-pooled ESM-2 650M embeddings (facebook/esm2_t33_650M_UR50D, pinned revision) ... The five published homology partitions are retained as groups" (the registry, read 2026-10-31).
- Why out: a protein-sequence task whose features are the output of a protein language model; DeepLoc 2.0 itself is that tool ("We achieve state-of-the-art performance in DeepLoc 2.0 by using a pre-trained protein language model", abstract), so modality-specific models are clearly the method of the field (SEL-12). Precedent: `protein_location_prediction_challenge` (`No`, SEL-12) is the same prediction from the same kind of data, with ESM-1b embeddings shipped by the organisers; also `instadeep_kinase_classification_challenge` and `antigen_avida_hil6` (`No`, Lennart, Mustafa, Alex: "NLP task / data").
- The doubt: as on `brca1_variant_effect_evo2` — SEL-12 is judged per dataset and a frozen-embedding table is vectorized data, which SEL-12 allows where tabular models are competitive; the comparison here is against the same language model fine-tuned, which DeepLoc 2.0 reports as the state of the art.
- Siblings and duplicates: `brca1_variant_effect_evo2`, `fusionai_gene_fusion_ntv2` and `peer_tem1_beta_lactamase_esm2`, the benchmark's other embedding tables (PROV-6 on the construction, different sources). External collections: TabBench-Bio (`local-DeepLoc2-Fungi-ESM2`).
- Better data: a candidate of the benchmark TabBench-Bio; no new search this round.
- Papers and pages: DeepLoc 2.0 (NAR 2022) and its data at services.healthtech.dtu.dk; TabBench-Bio (arXiv 2609.07441), Table 4 and App. G.1; the release asset https://github.com/not-a-feature/TabBench-Bio/releases/download/v0.1.0/deeploc2_fungi_esm2_t33.parquet.
- Metric: the benchmark's own Macro-F1 (Sec. 3.5). DeepLoc 2.0 scores each label by the Matthews correlation coefficient and sets its thresholds by maximising MCC on the training data ("A threshold for each output label is computed by maximizing Matthew's Correlation Coefficient (MCC) ... Accuracy-based metrics are susceptible to imbalance"), but for the whole localisation task, not for this membrane cut. Inputs: the group column `homology_partition` (five partitions), which ships.
- Reject check (AI, 2026-10-31): stands. The source's input is the amino-acid string (Swiss-Prot file: ACC, Kingdom, Partition, Membrane, locations, Sequence). Its state of the art pools the language model's per-residue outputs by learned attention, 'The output representation is the attention weighted sum of the token representations' (DeepLoc 2.0, https://pmc.ncbi.nlm.nih.gov/articles/PMC9252801/), which is a sequence architecture. That is the same task and the same facts as protein_location_prediction_challenge (`No`). Unlike brca1, no source shows a classifier on the pooled vector as the field's tool, and the source holds no tabular attribute besides the kingdom.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 5,841 x 1,280; target: membrane (1,306 membrane / 4,535 soluble).
- Why: Membrane-associated vs soluble fungal protein (DeepLoc 2.0 Swiss-Prot set) from protein language-model embeddings
- Notes: Built by the authors: features are mean-pooled ESM-2 650M embeddings of the sequence. Grouped by the five DeepLoc homology partitions. Related: protein_location_prediction_challenge (Zindi, ESM-1b embeddings, 'No' as a sequence task).
