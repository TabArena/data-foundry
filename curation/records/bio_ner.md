---
unique_name: bio_ner
name: bio_ner, bio_ner_2, bio_ner_3, bio_ner_5, bio_ner_6, bio_ner_7, bio_ner_8, bio_ner_9, bio_ner_10, bio_ner_12, bio_ner_13, bio_ner_14, bio_ner_16, ...
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
- 'https://huggingface.co/datasets/jablonkagroup/chempile-lift/tree/main/<config> (configs: bio_ner, bio_ner_2, bio_ner_3, bio_ner_5, bio_ner_6, bio_ner_7, bio_ner_8, bio_ner_9, bio_ner_10, bio_ner_12, bio_ner_13, bio_ner_14, bio_ner_16, bio_ner_17, bio_ner_18, bio_ner_19, bio_ner_20, bio_ner_22, bio_ner_23, bio_ner_24) ; ChemNLP builder https://github.com/OpenBioML/chemnlp/tree/main/data/tabular/bio_ner ; original: https://github.com/ML4LitS/bio-datasets'
- https://arxiv.org/abs/2505.12534
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`NLP (Text)`, SEL-12): named-entity recognition on biomedical sentences; one row is a sentence and the target is the list of entity spans in it, so there is no tabular predictive target and language models are the tool (SEL-3 as well).
- Source: EMBL-EBI's ML4LitS bio-datasets (https://github.com/ML4LitS/bio-datasets), taken into ChemPile through the ChemNLP builder `data/tabular/bio_ner`. Its meta.yaml reads "description: NER task on bio-related text", with the identifier `Sentence` and the targets `entity_1` and `json`, and its prompt template reads "Task: Please carry out the named entity recognition (NER) task for the the text below. Text: {Sentence#}. Constrain: Please, list the entities in the form NER entity, span start, span end, and type ... Result: {entity_1#}" (read 2026-10-31). As published: 123,509 sentences in the main config; the 20 ChemPile configs are cuts by the number of entity types, from 69,192 rows down to 8. The builder carries `license: unknown` and `bibtex: ???`.
- Use case: none that a tabular model serves: the decision is an annotation of free text, and no actor makes a classification or regression call on a row (SEL-3, USE-2).
- Siblings and duplicates: `biomedical_ner_corpora` (five NER corpora of the same benchmark) is the same kind of task and is proposed as a reject too; the 20 configs here are cuts of one source (PROV-6), so no duplicate record is needed. External collections: ChemPile / ChemNLP.
- Better data: a candidate of the benchmark ChemPile; no further search this round.
- Papers and pages: the builder names no paper (`bibtex: ???`); the data repository is github.com/ML4LitS/bio-datasets.
- Metric: none found; the builder names a `split_column` but no metric (looked at the ChemNLP meta.yaml and the ChemPile-LIFT card). NER is scored by entity-level precision, recall and F1, a text-annotation metric no tabular task of ours uses.
- Reject check (AI, 2026-10-31): stands. The builder's own meta reads 'description: NER task on bio-related text', identifier `Sentence`, targets `entity_1` and `json`, and its prompt asks to 'list the entities in the form NER entity, span start, span end, and type' (https://github.com/OpenBioML/chemnlp/tree/main/data/tabular/bio_ner): the output is a set of spans in a sentence, with no class or number to re-target and no tabular reading any actor uses.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark ChemPile (https://arxiv.org/abs/2505.12534).
- as published: 123,509 sentences in the main config; the numbered configs are cuts by number of entity types, from 69,192 down to 8 rows; in ChemPile-LIFT 250,761 text prompts over 20 config(s); target: the matched entity spans.
- Why: Named entity recognition in biomedical sentences: mark the entities of n types in a sentence
- Notes: 20 configs, one source (EMBL-EBI ML4LitS bio-datasets). NER on sentences: not tabular, no predictive tabular target. Out of scope.
