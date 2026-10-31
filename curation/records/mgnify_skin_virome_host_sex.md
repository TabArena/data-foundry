---
unique_name: mgnify_skin_virome_host_sex
name: MGYS00005384 MGnify functional profile
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
- https://doi.org/10.1128/mBio.01578-15
- https://www.ebi.ac.uk/metagenomics/studies/MGYS00005384
- https://arxiv.org/abs/2609.07441
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`No Good Target / Scientific Discovery`; SEL-3, USE-2, SEL-8): the sex of 16 healthy volunteers, predicted from 674 skin bacterial and viral metagenome profiles; a sample-metadata field TabBench-Bio picked as the target of a study of the skin virome.
- Source: Hannigan et al., "The Human Skin Double-Stranded DNA Virome: Topographical and Temporal Diversity, Genetic Enrichment, and Dynamic Associations with the Host Microbiome", mBio 6 (2015; doi 10.1128/mBio.01578-15); BioProject PRJNA266117 (University of Pennsylvania), MGnify MGYS00005384: "To assess spatial, interpersonal, and temporal variance, samples were collected from eight anatomical skin sites of 16 healthy individuals over two months" (674 samples; sample metadata: collection date, host sex, host taxon). As TabBench-Bio ships it: 674 x 17,026 InterPro counts, target host sex.
- Why out: the registry's words: "MGnify IPR functional profile. Target metadata field 'host sex', 2 classes" (TabBench-Bio `bio_datasets.json`, MGYS00005384). The study describes the skin virome by site, person and time (SEL-8); a donor's sex is recorded at sampling and no decision rests on predicting it (USE-2, SEL-3), fit none (USE-8). Precedent: `road_safety_gender` (`No`; CC: "likely gender was picked as random target").
- Also noted: the 674 samples come from 16 people, so the label has 16 independent units, and the registry gives no person id; were it kept, a grouped split (SPLIT-24) would leave a handful of people per fold (TP-5).
- Not the reason: skin-microbiome forensics (inferring traits of a trace's donor) is a research topic, but the study names no such use, and its samples are virus-like-particle and whole metagenomes of 16 volunteers.
- Siblings and duplicates: `mgnify_skin_surface_environment_material` (another skin project, PRJNA46333), `mgnify_t2d_gut_host_sex`, `mgnify_hiv_gut_host_sex`, `mgnify_preterm_infant_gut_host_sex`, `mgnify_vegetable_oil_diet_gut_host_sex`. External collections: TabBench-Bio (Table 4).
- Better data: a candidate of the benchmark TabBench-Bio (the run searched no further).
- Metric: none from the source for this target; TabBench-Bio ranks by macro-F1 (Sec. 3.5).
- Reject check (AI, 2026-10-31): stands. Registry: 'Target metadata field 'host sex', 2 classes' (MGYS00005384, https://raw.githubusercontent.com/not-a-feature/TabBench-Bio/main/src/tabbench_bio/bio/data/bio_datasets.json); MGnify's abstract: 'samples were collected from eight anatomical skin sites of 16 healthy individuals over two months' (https://www.ebi.ac.uk/metagenomics/studies/MGYS00005384). A virome description study (SEL-8); sex of 16 volunteers is no decision (road_safety_gender), and the label has 16 independent units. Skin forensics is not named by any source.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 674 x 17,026; target: host sex.
- Why: Host sex from InterPro functional profiles of skin bacterial and viral metagenomes (PRJNA266117, Hannigan et al. 2015)
- Notes: Target is a sample-metadata field (host sex), not a clinical outcome. Several samples per person and body site in the source study.
