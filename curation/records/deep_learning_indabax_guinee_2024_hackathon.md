---
unique_name: deep_learning_indabax_guinee_2024_hackathon
name: deep-learning-indabax-guinee-2024-hackathon
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Duplicate
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2024'
required_split:
- '?'
problem_type: TBD
source_links:
- https://zindi.africa/competitions/deep-learning-indabax-guinee-2024-hackathon/data
source_row: 935
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`Duplicate`, PROV-4): a re-run of the UmojaHack Africa 2023 Carbon Dioxide Prediction Challenge (BEGINNER), whose data `carbon_dioxide_prediction_challenge` already carries.
- Source: Zindi "Deep Learning IndabaX Guinee 2024 Hackathon", 2-4 November 2024 (https://zindi.africa/competitions/deep-learning-indabax-guinee-2024-hackathon); the Zindi API names its parent `umojahack-africa-2023-beginner-challenge` (18 March 2023), and both ship the same files (Train.csv 93,563,905 bytes, Test.csv 35,229,807, SampleSubmission.csv 725,308, the same "EY_Carbon_Prediction_StarterNotebook.ipynb") and the same data description word for word.
- As published: weekly Sentinel-5P pollutant columns (SO2, CO, NO2, HCHO, aerosol index, O3, cloud) from January 2019 to November 2022 for about 500 locations in South Africa; target CO2 emissions from GRACED and EDGAR; "The test set is from a different province to the train set".
- Siblings and duplicates: `carbon_dioxide_prediction_challenge` lists https://zindi.africa/competitions/umojahack-africa-2023-beginner-challenge among its links, so the first publication is recorded there; that record decides the task (its own open questions: remote-sensing modality, spatio-temporal framing). The `data_type` "Structured" and the deep-learning name do not matter for the verdict.
- Metric: RMSE (Zindi Evaluation page), the same as the parent.
- For the main session: the year of first publication is 2023 (the parent), not 2024.
- Reject check (AI, 2026-10-22): stands. Zindi API (api.zindi.world/v1/competitions/deep-learning-indabax-guinee-2024-hackathon) names parent umojahack-africa-2023-beginner-challenge; Train.csv 93,563,905 and Test.csv 35,229,807 bytes are identical to the parent's; carbon_dioxide_prediction_challenge already lists the parent link. PROV-4 with PROV-5 confirmed.

Zindi 'Deep Learning IndabaX Guinee 2024' hackathon with no description or metadata in the record. The 'deep learning' framing of an IndabaX hackathon raises the likelihood that the data is image/text/audio rather than tabular, which would make it out of scope, but this is unconfirmed. Too little information to decide, and insufficient info alone is not grounds for rejection. A human must open the competition to determine the data modality (tabular vs image/text), the task and target, size, and split.
