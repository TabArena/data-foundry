---
unique_name: data_science_bowl_2019_measure_up
name: 'Data Science Bowl 2019 (PBS KIDS Measure Up!): how a child will do on the next in-app assessment'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
decision_markers:
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
original_source: Kaggle
year: '2019'
domain: education
problem_type: Multiclass Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.kaggle.com/c/data-science-bowl-2019
- https://huggingface.co/datasets/pytorch-lifestream/datascience-bowl2019
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: a Kaggle competition of the data owner (PBS KIDS with Booz Allen Hamilton) on how a child will do on an in-app assessment, from the play history so far, scored by quadratic weighted kappa; education and multiclass are thin, but the features must be aggregated from 11.3M events with leak traps.
- Source: 2019 Data Science Bowl, Kaggle (Booz Allen Hamilton with PBS KIDS), launched 2019-10-24, closed 2020-01-22, 3,493 teams, "Uncover the factors to help measure how young children learn" (Kaggle API). As published (the Hugging Face mirror pytorch-lifestream/datascience-bowl2019, read 2026-10-31, and the run's first pass): train events about 11.3M rows with 11 columns (`event_id`, `game_session`, `timestamp`, `event_data` as JSON, `installation_id`, `event_count`, `event_code`, `game_time`, `title` with 44 values, `event_type` and `world` with 4 each), train labels about 17.7k assessment attempts (`game_session`, `installation_id`, `title`, `num_correct`, `num_incorrect`, `accuracy`, `accuracy_group`), test events about 1.16M with hidden labels, and a specs table. Target `accuracy_group`: 3 solved on the first attempt, 2 on the second, 1 after more, 0 never.
- Use case: the app, when a child starts an assessment, predicts how many attempts the child will need from the play so far, to adapt content (ours: the organisers frame it as measuring how young children learn, to design better media); fit approximate; regime grouped by `installation_id`: each installation contributes several assessments, and a deployed model meets new children (the competition's test installations are said to be new ones; to check).
- Siblings and duplicates: `riiid_answer_correctness` (`TBD -> 2nd Tier`, answer correctness in a learning app, Kaggle 2020), `assistments`, `duolingo_spaced_repetition_recall`, `open_university_learning_analytics_dataset` (accepted): other sources and tasks. No other record of the competition (grep: data science bowl, measure up, pbs kids). External collections: pytorch-lifestream (sequence-modelling benchmarks; the Hugging Face mirror).
- Better data: from the curator's Zotero collection (item 141); no further search this round.
- Papers and pages: the competition page (kaggle.com/c/data-science-bowl-2019); the top solutions were gradient-boosted trees on aggregated features (the run's first pass; not re-read).
- Metric: quadratic weighted kappa, the competition's metric (Kaggle API `evaluationMetric`: QuadraticWeightedKappa); deliberate (MET-4); it scores hard labels, so methods pick their class cut-offs on the training side; inputs none.
- Risks for /add-dataset: features must be aggregated from each installation's events up to the start of the assessment (`Needs extensive data wrangling`); the label is computed from the assessment's own attempt events, which must be cut from the features (LEAK-10, SEL-5); later assessments of an installation must not feed earlier ones (LEAK-12); only the training labels are public, so the benchmark uses the train side (about 17.7k assessments from about 3.6k installations, to check); `event_data` is JSON; children's play data under anonymous installation ids, no objection to ML use found (SEL-1); Kaggle competition terms noted only (EV-4).
- Priority: gap + (education has 3 accepted datasets and multiclass is thin), use case 0 (the source names the research aim, not a per-child decision), source + (the data owner's competition with a data description), shape + (about 17.7k assessments, rich event logs, grouped), risk - (heavy event aggregation with leak traps).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 141: "pytorch-lifestream (PyTorch-Lifestream)".
- as published: Training: 11,341,042 game events (11 columns) from about 17,000 app installations, with 17,690 labelled assessment attempts (train_labels, 7 columns). Test: 1,156,414 events with hidden labels.; target: accuracy_group of an assessment: 3 solved on the first attempt, 2 on the second, 1 later, 0 not solved (quadratic weighted kappa); access: registration.
- Why: Real usage logs from an educational app with an organiser-defined target; the top solutions were GBDTs on aggregated features.
- Adds: Education technology. Caveats: events must be aggregated up to each assessment start (Needs extensive data wrangling); children's data under anonymized installation ids; only the training labels are usable, so the size in units is about 17.7k assessments from about 3.6k installations (from memory, check).
