---
unique_name: uniprot_tasks
name: uniprot_binding_single, uniprot_binding_sites_multiple, uniprot_organisms, uniprot_reactions, uniprot_sentences
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
- https://doi.org/10.1093/nar/gkac1052
- 'https://huggingface.co/datasets/jablonkagroup/chempile-lift/tree/main/<config> (configs: uniprot_binding_single, uniprot_binding_sites_multiple, uniprot_organisms, uniprot_reactions, uniprot_sentences) ; ChemNLP builder https://github.com/OpenBioML/chemnlp/tree/main/data/tabular/uniprot_binding_single ; original: https://www.uniprot.org'
- https://arxiv.org/abs/2505.12534
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`NLP (Text)`, SEL-12): five UniProt configs whose only input is an amino-acid sequence and whose targets are free text, position indices or annotation strings; nothing tabular on either side, and sequence models are the tool.
- Source: UniProt, "the Universal Protein Knowledgebase" (The UniProt Consortium, Nucleic Acids Research 51:D523-D531, 2023, https://doi.org/10.1093/nar/gkac1052), a curated annotation database; the configs are ChemNLP/ChemPile-LIFT cuts of it (`uniprot_binding_single` 604,383 rows, `uniprot_binding_sites_multiple` 176,066, `uniprot_organisms` 559,428, `uniprot_reactions` 253,713, `uniprot_sentences` 396,241; 12,306,219 text prompts in ChemPile-LIFT, licence MIT in the ChemNLP metadata). As published: ChemNLP's `meta.yaml` for `uniprot_binding_single` gives `identifiers: - id: sequence, type: AS_SEQUENCE` and `targets: - id: start_binding_site, description: index for start of the binding sites of a protein, type: text`; for `uniprot_organisms`, `identifiers: - id: other, type: AS_SEQUENCE` and `targets: - id: organisms, description: organisms in which a protein can be found, type: text`. The templates are generation prompts ("Task: Predict the organism in which this protein can be found. Result: {organisms#}"; "Task: Create a molecule that binds to the given binding site ... Result: {SMILES#}").
- Use case: none that a tabular model serves. Naming a protein's binding-site indices, its organisms, its reactions or writing its function sentence is reading a knowledgebase entry or a sequence-model task (SEL-3: a knowledgebase annotation is not a predictive target; SEL-12: a raw amino-acid sequence is a non-tabular modality where sequence models clearly win).
- Siblings and duplicates: one record for five configs of one source (PROV-6); no other record holds UniProt (checked `curation/records/` for uniprot, protein sequence, binding site). Related out-of-scope ChemPile records of this run: `chempile_reaction_and_generated_tasks` (generation targets), `bio_ner` and `biomedical_ner_corpora` (text), `chebi_20` (captioning). External collections: ChemPile-LIFT (5 configs), ChemNLP.
- Better data: a candidate of the benchmark ChemPile; no new search this run.
- Papers and pages: the UniProt 2023 database paper above; ChemNLP builder https://github.com/OpenBioML/chemnlp/tree/main/data/tabular/uniprot_binding_single; ChemPile https://arxiv.org/abs/2505.12534.
- Metric: none found and none applies: ChemNLP declares no metric, and the targets are strings, so no classification or regression metric is defined (MET-1 does not arise).
- Risks for /add-dataset: none; the record is rejected on scope. If a tabular UniProt task is ever wanted, it would have to be built from annotation fields we choose, which would be our invention rather than the source's task (SEL-3, SEL-8).
- Reject check (AI, 2026-10-31): stands. The builders' metas give an `AS_SEQUENCE` identifier and text targets only, e.g. `start_binding_site` 'index for start of the binding sites of a protein', type text, and `organisms` 'organisms in which a protein can be found', type text (https://raw.githubusercontent.com/OpenBioML/chemnlp/main/data/tabular/uniprot_binding_single/meta.yaml): residue indices, organism lists, reaction strings and function sentences, no class or number. Unlike `peptides_hemolytic` (a measured outcome on a sequence, left open under SEL-12), there is no outcome to keep; any label we picked from UniProt would be our invention (SEL-8).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark ChemPile (https://arxiv.org/abs/2505.12534).
- as published: uniprot_binding_single 604,383; uniprot_binding_sites_multiple 176,066; uniprot_organisms 559,428; uniprot_reactions 253,713; uniprot_sentences 396,241; in ChemPile-LIFT 12,306,219 text prompts over ...; target: binding-site positions / organism names / reaction strings / function sentences.
- Why: From a protein sequence: name the binding-site indices, the organisms it occurs in, the reactions it catalyzes, or write its function description
- Notes: Five configs of UniProt (The UniProt Consortium 2023). Targets are free text, position lists or annotation strings over an amino-acid sequence, none of them a tabular label. Out of scope.
