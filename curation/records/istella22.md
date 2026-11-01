---
unique_name: istella22
name: Istella
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Out-of-scope Task (CTR/RecSys/Ranking)
tags:
- AI-Filled (Verify)
collections:
- tabular-dl-more-data
source_links:
- https://doi.org/10.1145/3477495.3531740
- https://www.istella.ai/sdm_downloads/istella22-dataset/
- https://arxiv.org/abs/2610.26794
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`Out-of-scope Task (CTR/RecSys/Ranking)`, SEL-9): Istella22 is a learning-to-rank collection of an industrial web search engine; the tabular-dl-more-data benchmark's regression on its relevance grades re-frames a ranking task, which SEL-9 excludes "also when a mirror serves them as classification or regression".
- Source: Dato, MacAvaney, Nardini, Perego, Tonellotto, "The Istella22 Dataset: Bridging Traditional and Neural Learning to Rank Evaluation", SIGIR 2022 (https://doi.org/10.1145/3477495.3531740; open copy https://eprints.gla.ac.uk/268514/). Abstract: "we present Istella22, a new dataset that enables such comparisons by providing both query/document text and strong query-document feature vectors used by an industrial search engine. The dataset consists of a comprehensive corpus of 8.4M web documents, a collection of query-document pairs including 220 hand-crafted features, relevance judgments on a 5-graded scale, and a set of 2,198 textual queries used for testing purposes. Istella22 enables a fair evaluation of traditional learning-to-rank and transfer ranking techniques on the same data." CCS concepts: "Information systems → Learning to rank; Test collections". As published (Table 1): 8,421,456 documents; train 44,249 queries and 8,349,810 query-document vectors; validation 11,005 and 2,062,424; test 2,198 text queries and 1,501,704 vectors; SVM-Rank files (relevance, qid, 220 features).
- Original task: Sec. 3.3, "feature vectors for train and validation queries are used in the training process of LtR models"; the train and validation lists come from "negative sampling strategies", the test lists from the first-stage ranker's top 1,000 documents per query. Sec. 6.1 evaluates with P@1/5/10, NDCG@10/20, MRR and MAP and tunes the models on NDCG@10: per-query ranking metrics, none for a per-row prediction.
- Siblings and duplicates: `microsoft_mslr` and `yahoo_learning_to_rank_challenge_data` (both `No`, `Out-of-scope Task (CTR/RecSys/Ranking)`, Lennart: "Learning to rank"), `yahoo` (`No`); Istella's earlier LETOR release (2016) has no record. External collections: tabular-dl-more-data (Rubachev, Lazarev, Babenko 2026, arXiv 2610.26794, "Istella": "We treat the graded relevance labels as regression targets", RMSE, validation and test as disjoint query groups of the official test partition).
- Better data: a candidate of the benchmark tabular-dl-more-data; no further search this round.
- Metric: the paper's are ranking metrics (Sec. 6.1); no use for the record after the reject.
- Reject check (AI, 2026-10-31): stands. Abstract: 'Istella22 enables a fair evaluation of traditional learning-to-rank and transfer ranking techniques on the same data' (https://eprints.gla.ac.uk/268514/); the label is a query-document relevance grade, the ranking target itself, which SEL-9 excludes 'also when a mirror serves them as ... regression'. Curator precedents microsoft_mslr and yahoo_learning_to_rank_challenge_data (Lennart: 'Learning to rank').

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark tabular-dl-more-data (https://arxiv.org/abs/2610.26794).
- as published: 9.21M train / 600K val / 600K test, 200 non-constant features; validation and test are disjoint query groups of the official test partition; RMSE. Release (from the script): train 8,349,810 rows / ...; target: graded query-document relevance label, treated as a regression target.
- Why: Web-search learning to rank: graded relevance of a query-document pair from 220 hand-crafted ranking features (Istella22, Dato et al., SIGIR 2022)
- Notes: Plainly out of scope: a learning-to-rank / information-retrieval task (SEL-9, Out-of-scope Task (CTR/RecSys/Ranking)), as microsoft_mslr and yahoo_learning_to_rank_challenge_data, both 'No'. The archive also holds raw query and document text (docs.jsonl), unused here.
