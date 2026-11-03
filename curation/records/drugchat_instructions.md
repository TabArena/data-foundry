---
unique_name: drugchat_instructions
name: drugchat_liang_zhang_et_al
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
- https://www.techrxiv.org/articles/preprint/DrugChat_Towards_Enabling_ChatGPT-Like_Capabilities_on_Drug_Molecule_Graphs/22945922
- 'https://huggingface.co/datasets/jablonkagroup/chempile-lift/tree/main/drugchat_liang_zhang_et_al ; ChemNLP builder https://github.com/OpenBioML/chemnlp/tree/main/data/tabular/drugchat_liang_zhang_et_al ; original: https://github.com/UCSD-AI4H/drugchat'
- https://arxiv.org/abs/2505.12534
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`NLP (Text)`, SEL-12; also SEL-3): the target is a free-text answer to a generated question, an instruction-tuning corpus for a chat model, not a classification or regression task.
- Source: Liang, Zhang, Zhang, Xie, "DrugChat: Towards Enabling ChatGPT-Like Capabilities on Drug Molecule Graphs", TechRxiv preprint (2023), doi 10.36227/techrxiv.22945922.v1; data at github.com/UCSD-AI4H/drugchat, licence BSD-3-Clause. As published: 143,517 question-answer pairs over 10,834 compounds from ChEMBL and PubChem; the builder declares the identifiers `SMILES` and `quest` ("a question about the SMILES") and one target `answ`, "The answer to the question about the SMILES", type string (ChemNLP `data/tabular/drugchat_liang_zhang_et_al/meta.yaml`).
- Use case: none a tabular model serves: the set trains the LLM part of DrugChat, and the questions were generated from each molecule's classification, properties and descriptions in ChEBI, LOTUS and YMDB (same meta.yaml), so the answers restate database fields rather than an observed outcome (SEL-3; PROV-3 on derived data).
- Siblings and duplicates: the other free-text ChemPile configs of this run, `mp_descriptions` (generated prose about a material) and `chebi_20`; no duplicate. External collections: ChemPile-LIFT (arXiv 2505.12534), itself "a text corpus for language-interfaced fine-tuning" with one `text` column per row.
- Better data: a candidate of the benchmark ChemPile (this run searched no further).
- Papers and pages: the DrugChat preprint (techrxiv 22945922); github.com/UCSD-AI4H/drugchat; the ChemNLP builder.
- Metric: none - a text-generation task, nothing to declare (MET-1 does not apply).
- Risks for /add-dataset: not applicable.
- Reject check (AI, 2026-10-31): stands. The builder's only target is `answ`, 'answer to the question about the SMILES', type string, in an 'Instruction tuning dataset used for the LLM component of DrugChat' whose '143,517 questions were generated using the molecules' classification, properties and descriptions from ChEBI, LOTUS & YMDB' (https://github.com/OpenBioML/chemnlp/blob/main/data/tabular/drugchat_liang_zhang_et_al/meta.yaml); the answers restate database fields, and any numeric property behind them belongs to its own source.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark ChemPile (https://arxiv.org/abs/2505.12534).
- as published: 143,517 question-answer pairs over 10,834 compounds (ChEMBL and PubChem); in ChemPile-LIFT 717,170 text prompts over 1 config(s); target: free-text answer.
- Why: Answer generated questions about a drug molecule (instruction tuning)
- Notes: Liang, Zhang et al. 2023 (DrugChat preprint). Questions and answers generated from ChEMBL/PubChem fields, so it is a derived instruction set, not measured data. Out of scope.
