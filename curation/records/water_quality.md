---
unique_name: water_quality
name: water_quality
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- AHDS (Artifical/Handmade/Deterministic/Simulated)
tags:
- 2nd Tier / Scientfic Discovery
- AI-Filled (Verify)
collections:
- TabArena Reject
year: '2021'
domain: environmental science & climate
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/mssmartypants/water-quality
source_row: 822
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`AHDS (Artifical/Handmade/Deterministic/Simulated)`, SEL-16): the uploader says the data is made up.
- Source: Kaggle `mssmartypants/water-quality`, "Water quality", one file waterQuality1.csv (840,687 bytes, 2021-06-30), licence "copyright-authors"; 20 numeric contaminant columns (aluminium to uranium, each listed with "dangerous if greater than" a limit) and `is_safe`. The card: "This is a set of data created from imaginary data of water quality in an urban environment. I recommend using this dataset for educational purposes", and "Idea was to create dataset that is good for binary classification and that gives adequate results." No place, date or lab.
- Siblings and duplicates: `water_quality_and_potability` (`No`, `AHDS`, another synthetic potability file) and `water_potability_classification_hackathon_by_indabax_nigeria_2021` (a copy of it) are different files. Already tagged TabArena Reject; the CC line quotes the same sentence.
- Metric: none (a Kaggle dataset), moot.
- Reject check (AI, 2026-10-22): stands. The uploader's own words on Kaggle mssmartypants/water-quality (https://www.kaggle.com/datasets/mssmartypants/water-quality): "This is a set of data created from imaginary data of water quality in an urban environment. I recommend using this dataset for educational purposes". SEL-16 (Must), detection PROV-3; source's words, top evidence rank.

A Kaggle water-quality dataset that, per the CC comment and the Kaggle description, was created from imaginary/synthetic data of water quality in an urban environment and is recommended only for educational use. As artificial/simulated data it is not representative of real-world tabular ML and fails the criteria; it is already tagged TabArena Reject. It should be rejected as AHDS; no further verification needed.

---

CC: "created from imaginary data of water quality in an urban environment, recommended using this dataset for educational purposes"

## Reference

Kaggle
