---
unique_name: alfa_bank_credit_history_default
name: Alfa-Bank credit history data competition (Data Fest 2022, ODS.ai); Alfa BKI dataset
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
decision_markers:
- Needs extensive data wrangling
tags:
- Non-IID (Temporal)
- AI-Filled (Verify)
original_source: Other
year: '2022'
domain: finance
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
source_links:
- https://ods.ai/competitions/dl-fintech-bki
- https://huggingface.co/datasets/mllab/alfa_bki
- https://huggingface.co/datasets/pytorch-lifestream/alfa-scoring-bki
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: Alfa-Bank's 2022 credit-bureau competition (ODS.ai): 3,000,000 loan applications, each with the applicant's credit-bureau history and a default flag, for the bank's decision to issue the loan; the bank and target of `alfa_battle_2_0_task_2`, from bureau records instead of card transactions.
- Source: Alfa-Bank with ODS.ai, competition dl-fintech-bki (2022; the ODS page timed out here, so the dates, participants and metric are the scout's: 2022-06-04 to 2022-07-31, 447 participants, ROC AUC); data on Hugging Face as mllab/alfa_bki (CC BY 4.0; one train split of 3M applications in 12 parquet files, 1.12 GB) and pytorch-lifestream/alfa-scoring-bki (names the ODS competition; train_data with 26.2M product rows, test_data with 4.72M, train_target and test_target files). As published (mllab card): per application an `id`, a `history` (one entry per credit product, each with documented fields: days since opening and to the planned and actual closing, limit, balance, overdue amounts, late-payment counts by bucket, utilisation ratios, monthly payment statuses `enc_paym_0..n`, holder type, status, currency and credit type) and `flag` (1 when the client defaulted). The values are binned and encoded per field; every field is described.
- Use case: the bank scores an applicant at application from the bureau history to decide whether to issue the loan (mllab card: models "that predict applicant default"); fit direct; regime temporal by the competition's design (test applications from the months after training, per the scout), though no calendar date ships per application.
- Siblings and duplicates: `alfa_battle_2_0_task_2` (Yes, DF: Yes; AlfaBattle 2.0 card transactions, default on a credit product) and `alfa_battle_2_0_task_1` (`No`) come from the same bank with other data; the same lender and target with other inputs and applications make a distinct task (PROV-7); whether the applicants overlap is unknown. No other record of the BKI data (grep: alfa, lifestream, dl-fintech). External collections: none in our vocabulary; the pytorch-lifestream Hugging Face organisation hosts a copy.
- Better data: a related task next to `alfa_battle_2_0_task_2`, and from the curator's Zotero collection (item 141, pytorch-lifestream); no further search this round.
- Papers and pages: the ODS.ai competition page (not readable here); the two Hugging Face cards; the pytorch-lifestream library.
- Metric: ROC AUC, the competition's leaderboard metric per the scout (MET-4), not confirmed on the ODS page; it is the fallback too; inputs none.
- Risks for /add-dataset: sequence data: aggregate the products per application as the competition's solutions did (`Needs extensive data wrangling`; the precedent of `alfa_battle_2_0_task_2`, CC 2026-10-13); no calendar date per application, so the temporal split rests on the competition's train and test parts and on whether the test labels are open (the pytorch-lifestream viewer shows test_target as locked) (SPLIT-7, SPLIT-19); binned and encoded values are documented per field, so no `Anonymized` marker (as on `home_credit_default_stability`), but read the encoding of each field; the day counts are relative to the data collection date, so check that no field is recorded after the application (LEAK-10).
- Priority: gap 0 (finance, binary and temporal not thin), use case +, source + (an organiser-run competition and a documented field list), shape + (3,000,000 applications), risk - (sequence aggregation, no dates for the split).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through a related task next to `alfa_battle_2_0_task_2`; the curator's Zotero collection, item 141: "pytorch-lifestream (PyTorch-Lifestream)".
- as published: 3,000,000 applications (Hugging Face train split, 1.12 GB parquet), each with the applicant's credit-bureau history: one record per past credit product with about 37 fields (amounts, limits, overdue ...; target: flag: the applicant defaulted on the loan (binary); metric ROC AUC; access: open, registration.
- Why: same bank, same default target and the same application decision as alfa_battle_2_0_task_2, but the inputs are bureau records instead of the bank's card transactions; may be read as the same task by the curator | Real bank credit-bureau data at scale, with a lending decision and an organiser-defined target and metric.
- Adds: about three times the applications, newer, licence stated (CC BY 4.0 on Hugging Face) where the AlfaBattle files carry competition rules; caveats: anonymized, sequence data needing aggregation like task 2, and the competition test labels are likely not public | Bureau-history features, unlike the card transactions of ...
