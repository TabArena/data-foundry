---
unique_name: chebi_20
name: chebi_20
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- NLP (Text)
tags:
- AI-Filled (Verify)
collections:
- ChemPile
source_links:
- https://aclanthology.org/2021.emnlp-main.47/
- 'https://huggingface.co/datasets/jablonkagroup/chempile-lift/tree/main/chebi_20 ; ChemNLP builder https://github.com/OpenBioML/chemnlp/tree/main/data/tabular/chebi_20 ; original: https://github.com/cnedwards/text2mol ; https://huggingface.co/datasets/OpenBioML/chebi_20'
- https://arxiv.org/abs/2505.12534
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`NLP (Text)`, SEL-3 with SEL-9 and SEL-12): the target is a free-text ChEBI description and the task the data was published for is text-to-molecule retrieval, not a classification or regression.
- Source: Edwards, Zhai and Ji, "Text2Mol: Cross-Modal Molecule Retrieval with Natural Language Queries", EMNLP 2021 (https://aclanthology.org/2021.emnlp-main.47/): "We propose a new task, Text2Mol, to retrieve molecules using natural language descriptions as queries", scored by MRR; as published: 33,008 molecule-description pairs with SMILES, the PubChem CID and the ChEBI description (ChemNLP `chebi_20/meta.yaml`: target `description`, "a natural language description of the molecule SMILE", `type: string`, `num_points: 33008`).
- Use case: none for a tabular prediction: writing or retrieving a description is a language task where language models are the tool (SEL-12), and the original task is retrieval (SEL-8, SEL-9).
- Siblings and duplicates: no other record holds ChEBI-20; the other text-target records of this run are `chempile_reaction_and_generated_tasks`, `mp_descriptions`, `mofdscribe_descriptions`, `bio_ner`, `biomedical_ner_corpora`, `drugchat_instructions`, `uniprot_tasks` and `sigma_aldrich_safety_data`. External collections: ChemPile (config `chebi_20`), Hugging Face `OpenBioML/chebi_20`.
- Better data: a candidate of the benchmark ChemPile; no new search in this run.
- Papers and pages: Text2Mol (EMNLP 2021) and its repository https://github.com/cnedwards/text2mol.
- Metric: MRR, a retrieval metric (the paper's abstract); no classification or regression metric applies (MET-1).
- Risks for /add-dataset: none, nothing to add.
- Reject check (AI, 2026-10-31): stands. The builder's only target is `description`, 'a natural language description of the molecule SMILE', type string, next to the SMILES and the PubChem CID (https://github.com/OpenBioML/chemnlp/blob/main/data/tabular/chebi_20/meta.yaml), so no class or number is there to re-target; Text2Mol introduced the data to 'retrieve molecules using natural language descriptions as queries', scored by MRR (https://aclanthology.org/2021.emnlp-main.47/).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark ChemPile (https://arxiv.org/abs/2505.12534).
- as published: 33,008 molecule-description pairs; in ChemPile-LIFT 330,080 text prompts over 1 config(s); target: natural-language description.
- Why: Molecule captioning: write the ChEBI description of a molecule from its SMILES, or the reverse
- Notes: Edwards et al. 2021 (Text2Mol, EMNLP). Caption target, text. Out of scope.
