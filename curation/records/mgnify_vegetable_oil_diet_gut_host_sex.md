---
unique_name: mgnify_vegetable_oil_diet_gut_host_sex
name: MGYS00006282 MGnify functional profile
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target / Scientific Discovery
tags:
- AI-Filled (Verify)
collections:
- TabBench-Bio
source_links:
- https://www.ebi.ac.uk/metagenomics/studies/MGYS00006282
- https://arxiv.org/abs/2609.07441
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`No Good Target / Scientific Discovery`; SEL-3, USE-2, SEL-8): the sex of the volunteers of a dietary-oil trial, predicted from gut-metagenome InterPro profiles; a sample-metadata field TabBench-Bio picked as the target.
- Source: BioProject PRJNA728374, "Gut microbiome responses to dietary intervention with hypocholesterolemic vegetable oils" (first public 2022-02-17): "The objective of this 8-week double-blinded randomized clinical trial was to investigate the effects of consuming 30 grams of two different blended cooking oils, rich in omega-3 alpha-linolenic acid and phytonutrients, or refined olive oil on the intestinal microbiota in 126 volunteers with borderline hypercholesterolemia." The trial's paper was not identified (MGnify links only its own 2020 pipeline paper; web search was unavailable). MGnify MGYS00006282: third-party assembly, 256 samples (host sex 129 male, 127 female; no subject id, no time point). As TabBench-Bio ships it: 256 x 12,968 InterPro counts, target host sex.
- Why out: the registry's words: "MGnify IPR functional profile. Target metadata field 'host sex', 2 classes" (TabBench-Bio `bio_datasets.json`, MGYS00006282). The trial studies the effect of the oils (SEL-8); a volunteer's sex is known at enrolment and no decision rests on predicting it (USE-2, SEL-3), fit none (USE-8). Precedent: `road_safety_gender` (`No`; CC: "likely gender was picked as random target").
- Also noted: 256 samples from 126 volunteers, about two per person (before and after the 8 weeks), with no person id, so a random split would let a person's other sample give their sex away.
- Siblings and duplicates: `mgnify_t2d_gut_host_sex`, `mgnify_hiv_gut_host_sex`, `mgnify_preterm_infant_gut_host_sex`, `mgnify_skin_virome_host_sex` (host sex from other studies). External collections: TabBench-Bio (Table 4).
- Better data: a candidate of the benchmark TabBench-Bio (the run searched no further).
- Metric: none from the source for this target; TabBench-Bio ranks by macro-F1 (Sec. 3.5).
- Reject check (AI, 2026-10-31): stands. Registry: 'Target metadata field 'host sex', 2 classes' (MGYS00006282, https://raw.githubusercontent.com/not-a-feature/TabBench-Bio/main/src/tabbench_bio/bio/data/bio_datasets.json); the trial's question is 'to investigate the effects of consuming 30 grams of two different blended cooking oils ... on the intestinal microbiota' (https://www.ebi.ac.uk/ena/browser/view/PRJNA728374). A volunteer's sex is known at enrolment; no actor predicts it (road_safety_gender).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 256 x 12,968; target: host sex.
- Why: Host sex from gut metagenome InterPro profiles (TPA of PRJNA728374, a dietary intervention with hypocholesterolemic vegetable oils)
- Notes: Intervention study with repeated samples per person likely; the registry gives no group column. Target is a metadata field.
