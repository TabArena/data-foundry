---
unique_name: sustainable_development_goals_sdgs_text_classification_challenge
name: sustainable-development-goals-sdgs-text-classification-challenge
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- NLP (Text)
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
domain: Other
required_split:
- Random (IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/sustainable-development-goals-sdgs-text-classification-challenge/data
source_row: 952
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`NLP (Text)`, SEL-12): a multi-label classification of raw English text (contract names, news titles, organisation and opportunity descriptions) into SDG 3 indicators; language models are the tool.
- Source: Zindi competition hosted by Devex, 5 Sept to 13 Nov 2018 (https://zindi.africa/competitions/sustainable-development-goals-sdgs-text-classification-challenge, read through Zindi's page API); as published: devex_train.csv with ID, Type, Text and Label_1 to Label_12 ("manually classified by Devex analysts"), about 3,000 texts; 27 indicator labels.
- Use case: Devex tags development projects and documents by SDG indicator to "align resources, find partners" (Description); fit direct, but the input is the text itself.
- Siblings and duplicates: none found in `curation/records/`.
- Metric: Hamming loss over 27 labels ("The Hamming Loss metric be used", Evaluation tab), multi-label (also no single-target task).
- Reject check (AI, 2026-10-22): stands. SEL-12: Zindi Data Description: "Text: text to be classified ... The text contains some HTML mark-up. Dealing with this 'dirtiness' of the text is part of the challenge. All the text is in English"; Description: "approximately 3,000 web-scraped text from tenders, programs, and documents, as well as news articles"; type_of_problem 'Natural Language Processing' (api.zindi.world/v1/competitions/sustainable-development-goals-sdgs-text-classification-challenge). The only other input is the Type column; language models are the tool. Multi-label over 27 indicators (Hamming loss) as well.

A Zindi 'SDGs text classification challenge'. By name and design this is a text-classification task (classifying documents into Sustainable Development Goals), where NLP/text models dominate, so it is not representative of standard tabular ML. Recommend reject as a wrong-modality (text) task.
