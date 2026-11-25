---
unique_name: deeploc2_fungi_membrane_esm2
name: local-DeepLoc2-Fungi-ESM2 (DeepLoc2 Fungi, ESM-2)
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
- Expanding Science Catalogue
- 'Samples: Over Time'
- 'Time: Dated'
- 'Target: Revised Later'
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

**Screening (AI, 2026-11-25):** `No` (`Wrong Domain / Source Modality`, SEL-12): on the fungal cut the source's own table holds nothing but the amino-acid string — `Kingdom` is the constant `Fungi`, `Partition` is the group, the ten location columns are other targets (DeepLoc 2.0's Swiss-Prot file, counted 2026-11-25) — and the 1,280 ESM-2 embedding dimensions TabBench-Bio ships cannot be our features (CLEAN-6); what is left is sequence to localisation, the task `protein_location_prediction_challenge` was rejected for, where sequence models are the field's tool.
- Source: Thumuluri, Almagro Armenteros, Johansen, Nielsen and Winther, "DeepLoc 2.0: multi-label subcellular localization prediction using protein language models", Nucleic Acids Research 50(W1):W228-W234, 2022 (doi 10.1093/nar/gkac278, PMC9252801); its Swiss-Prot training and validation file (downloaded and counted 2026-11-25) has the columns ACC, Kingdom, Partition, Membrane, the ten location columns and Sequence, with Kingdom in {Metazoa 16,741, Viridiplantae 5,116, Fungi 5,841, Other 605}. The table under screening was built by TabBench-Bio: "Complete fungal subset of the official DeepLoc 2.0 Swiss-Prot training/validation data: 5841 unique proteins (1306 membrane-associated, 4535 soluble). Features are 1280-d residue-mean-pooled ESM-2 650M embeddings (facebook/esm2_t33_650M_UR50D, pinned revision) ... The five published homology partitions are retained as groups" (the registry, read 2026-10-31); the file's 5,841 fungal rows, its 1,306 / 4,535 membrane split and its five partitions (1,198 / 1,208 / 1,120 / 1,186 / 1,129) match that cut row for row.
- Use case: a researcher annotating a newly sequenced fungal protein, deciding whether to treat it as membrane-associated before an experiment; fit approximate (curated Swiss-Prot proteins); collection `Samples: Over Time`, `Time: Dated`: a cut of Swiss-Prot, whose entries UniProt dates by accession (entry creation and annotation versions), `Target: Revised Later`: a localisation annotation can be updated in a later release; type `Expanding Science Catalogue` (a sequence database, SPLIT-34).
- Split: leaf L-FAMILY.key (Grouped · `UnseenGroup`, the homology partition) because [CAT.next-items] yes (new proteins, no time scope stated), [CAT.entry-date] no (the labels are revised later), [FAMILY.key] yes (the five published homology partitions, which ship); open: none for the verdict.
- Why out: once the embeddings leave as features (CLEAN-6; as the source columns computed from a structure leave a SMILES task, CLEAN-24: "the real task here is going from smiles to a prediction"), no column of the source's fungal cut survives beside the sequence, a modality with no declared feature type (the two special kinds are `smiles` and `spectrum`), and the field's models read it per residue: DeepLoc 2.0 pools the language model's token representations by learned attention, and light attention over frozen per-residue embeddings reaches 86.0% ten-class accuracy on setDeepLoc against 43.5% for the same model on one-hot residues (Stärk et al. 2021, Table 2). Modality-specific models are clearly better (SEL-12). Precedent: `protein_location_prediction_challenge` (`No`, SEL-12: the same localisation task, the organisers shipped ESM-1b embeddings beside Sequence, Kingdom and Seq_length), `instadeep_kinase_classification_challenge` (`No`, AI-screened), and the curators' `No` on `antigen_avida_hil6` (`Wrong Domain / Source Modality`, `NLP (Text)`, checked by Lennart, Mustafa and Alex: "NLP task / data"). The line those cases draw, as `huesken_sirna_efficacy`'s precedent check of 2026-11-04 states it: "a raw full-length string or a learned embedding goes out; aligned positions or fixed-rule descriptors stay in".
- The doubt: a classifier on the mean-pooled vector is not far behind — "The simple FNNs even improved over the SOTA, DeepLoc, for some pLMs" (Stärk et al. 2021), though "LA consistently distilled more information from the embeddings" — so if a frozen-embedding table were allowed to ship, SEL-12's "tabular models are competitive" would need a measurement here as on `brca1_variant_effect_evo2`. It does not ship: CLEAN-6 bars learned embeddings, and what sets `brca1_variant_effect_evo2` apart is not its embeddings but what remains without them — Findlay's own table keeps variant columns (position, alleles, consequence), while this cut keeps a single string. Nor does the kept `ecoli_proteins` (the same localisation use case, `Yes`) reopen it: its columns are fixed-rule descriptors published with the data, and this source publishes none; computing today's equivalents would run other predictors over the sequences, which is new data and CLEAN-6 ground again. A curator who wants third-party embedding tables in scope would amend CLEAN-6, and then this record, `peer_tem1_beta_lactamase_esm2` and `protein_location_prediction_challenge` reopen together.
- Siblings and duplicates: `brca1_variant_effect_evo2`, `fusionai_gene_fusion_ntv2` and `peer_tem1_beta_lactamase_esm2`, the benchmark's other embedding tables (different sources); `protein_location_prediction_challenge` (the same localisation task from UniProt sequences with ESM-1b embeddings); `ecoli_proteins` and `huesken_sirna_efficacy` (`Yes`), the kept side of the line. External collections: TabBench-Bio (`local-DeepLoc2-Fungi-ESM2`).
- Better data: a candidate of the benchmark TabBench-Bio; no new search this round.
- Papers and pages: DeepLoc 2.0 (NAR 2022) and its data at services.healthtech.dtu.dk; Stärk, Dallago, Heinzinger and Rost, "Light attention predicts protein location from the language of life", Bioinformatics Advances 1(1):vbab035, 2021 (https://pmc.ncbi.nlm.nih.gov/articles/PMC9710637/; workshop version https://icml-compbio.github.io/2021/papers/WCBICML2021_paper_3.pdf); TabBench-Bio (arXiv 2609.07441), Table 4 and App. G.1; the release asset https://github.com/not-a-feature/TabBench-Bio/releases/download/v0.1.0/deeploc2_fungi_esm2_t33.parquet.
- Metric: the benchmark's own Macro-F1 (Sec. 3.5). DeepLoc 2.0 scores each label by the Matthews correlation coefficient and sets its thresholds by maximising MCC on the training data ("A threshold for each output label is computed by maximizing Matthew's Correlation Coefficient (MCC) ... Accuracy-based metrics are susceptible to imbalance"), for the whole localisation task, not for this membrane cut. Inputs: the group column `homology_partition` (five partitions), which ships.
- Reject check (AI, 2026-11-25): stands. The source's file was downloaded and counted this round: its fungal rows are exactly this table (5,841; Membrane 1,306 / 4,535; partitions 1,198 / 1,208 / 1,120 / 1,186 / 1,129), and on that cut `Kingdom` is the constant `Fungi`, so after CLEAN-6 drops the 1,280 ESM-2 dimensions and CLEAN-5 the constant, the source's own table holds no input but the amino-acid string — the table `protein_location_prediction_challenge` was rejected on, one language model later. The screener's own doubt was weighed: Stärk et al. 2021 do write "The simple FNNs even improved over the SOTA, DeepLoc, for some pLMs", but they also write "LA consistently distilled more information from the embeddings" (Table 2: light attention 86.0 against DeepLoc's LSTM 79.4 and one-hot 43.5), and either way that measures the barred feature set, not a table we could ship.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 5,841 x 1,280; target: membrane (1,306 membrane / 4,535 soluble).
- Why: Membrane-associated vs soluble fungal protein (DeepLoc 2.0 Swiss-Prot set) from protein language-model embeddings
- Notes: Built by the authors: features are mean-pooled ESM-2 650M embeddings of the sequence. Grouped by the five DeepLoc homology partitions. Related: protein_location_prediction_challenge (Zindi, ESM-1b embeddings, 'No' as a sequence task).
