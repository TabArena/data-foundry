---
unique_name: mgnify_vegetable_oil_diet_gut_host_sex
name: MGYS00006282 MGnify functional profile
checked_by:
- AI (UNVERIFIED)
data_foundry_status:
- WIP (Triage)
claimed_by: Andrej
suggestion: 'No'
decision_markers:
- No Good Target / Scientific Discovery
tags:
- AI-Filled (Verify)
- Panel Data
- 'Samples: Over Time'
- 'Time: Dated'
- 'Entities: Recur'
collections:
- TabBench-Bio
collection_period: Nov 2018 - May 2019
source_links:
- https://www.ebi.ac.uk/metagenomics/studies/MGYS00006282
- https://arxiv.org/abs/2609.07441
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-11-25):** `No` (`No Good Target / Scientific Discovery`, SEL-3 with USE-2 and SEL-8): the sex of the volunteers of a dietary-oil trial, predicted from gut-metagenome InterPro profiles; a sample-metadata field TabBench-Bio picked as the target, known at enrolment.
- Source: BioProject PRJNA728374, "Gut microbiome responses to dietary intervention with hypocholesterolemic vegetable oils" (first public 2022-02-17); the trial's paper not identified (MGnify links only its own pipeline paper). MGnify MGYS00006282: third-party assembly, 256 samples (host sex 129 male, 127 female; `collection date` 2018-11-26 to 2019-05-21). The sample names encode arm, subject and visit (`B.M118_2`), and the parent BioSamples carry `Day` (0, 14, 56), `Randomisation` (A, B, C) and blood lipids, glucose and insulin per visit. As TabBench-Bio ships it: 256 x 12,968 InterPro counts, target host sex (registry, read 2026-11-25).
- Use case: none (fit none, USE-8). The trial studies the effect of the oils (SEL-8); a volunteer's sex is known at enrolment and no decision rests on predicting it. Predicting a person's lipid response to an oil from the baseline microbiome would be a task of our own and a record of its own, not a re-target of this one. Collection: 114 subject codes in the sample names, sampled at day 0, 14 and 56 (55 three times, 32 twice, 27 once; 229 of 256 samples from people sampled twice or more), dated; the target exists with the features; type `Panel Data` (the release identifies the volunteer and dates each visit, SPLIT-34 rule 1).
- Split: no leaf walked: no task (USE-2).
- Siblings and duplicates: `mgnify_t2d_gut_host_sex`, `mgnify_hiv_gut_host_sex`, `mgnify_preterm_infant_gut_host_sex`, `mgnify_skin_virome_host_sex` (host sex from other studies). Precedent: `road_safety_gender`. External collections: TabBench-Bio (Table 4).
- Better data: not searched (no task).
- Metric: none from the source for this target; TabBench-Bio ranks by macro-F1 (Sec. 3.5).
- Reject check (AI, 2026-11-25): stands. The registry calls the target a "Target metadata field 'host sex'" (https://raw.githubusercontent.com/not-a-feature/TabBench-Bio/main/src/tabbench_bio/bio/data/bio_datasets.json), and the trial's question is "to investigate the effects of consuming 30 grams of two different blended cooking oils ... on the intestinal microbiota" (https://www.ebi.ac.uk/ena/browser/view/PRJNA728374, SEL-8). A volunteer's sex is known at enrolment and no actor predicts it (road_safety_gender); the BioSamples' other labels (LDL, ApoB, glucose, e.g. SAMN19078564) are blood measurements.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 256 x 12,968; target: host sex.
- Why: Host sex from gut metagenome InterPro profiles (TPA of PRJNA728374, a dietary intervention with hypocholesterolemic vegetable oils)
- Notes: Intervention study with repeated samples per person likely; the registry gives no group column. Target is a metadata field.
