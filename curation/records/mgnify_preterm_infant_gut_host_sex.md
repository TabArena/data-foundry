---
unique_name: mgnify_preterm_infant_gut_host_sex
name: MGYS00002425 MGnify functional profile
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
collection_period: 2009-2013
source_links:
- https://www.ebi.ac.uk/metagenomics/studies/MGYS00002425
- https://arxiv.org/abs/2609.07441
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-11-25):** `No` (`No Good Target / Scientific Discovery`, SEL-3 with USE-2 and SEL-8): the target is the recorded sex of preterm infants in a study of antibiotics and the infant gut resistome; the sex is known at birth and no decision rests on predicting it from stool.
- Source: MGnify MGYS00002425, EMBL-EBI's TPA assemblies of BioProject PRJNA301903, "Metagenomic sequencing of preterm infant gut microbiota raw sequence reads" (Washington University in St. Louis, registered 2015-11-11); the paper: Gibson, Wang, Ahmadi et al., "Developmental dynamics of the preterm infant gut microbiota and antibiotic resistome", Nat Microbiol 1:16024, 2016 (https://doi.org/10.1038/nmicrobiol.2016.24). MGnify: 387 samples, `host sex` male 157, female 230, counted per sample, not per infant, with a `collection date`; the parent BioSamples add `host_subject_id`, `host_day_of_life` and `birthweight`. TabBench-Bio keeps 394 x 12,651 (registry, read 2026-11-25).
- Use case: none (fit none, USE-8). The original task is the effect of antibiotics (SEL-8); host sex is a sampling field known at birth (USE-2). Collection: samples collected over time (`collection date` 2009-10-29 to 2013-03-17 over all 387), several per infant: 83 `host_subject_id`s in the parent BioSamples, 380 of 387 samples from infants sampled twice or more, each dated and with a day of life; the target exists with the features; type `Panel Data` (the release identifies the infant and dates each sample, SPLIT-34 rule 1).
- Split: no leaf walked: no task (USE-2).
- Siblings and duplicates: `mgnify_hiv_gut_host_sex`, `mgnify_t2d_gut_host_sex`, `mgnify_vegetable_oil_diet_gut_host_sex` and `mgnify_skin_virome_host_sex` carry the same kind of label; precedents `road_safety_gender`, `bog_lakes`. External collections: TabBench-Bio (arXiv 2609.07441, Table 4).
- Better data: not searched (no task).
- Metric: none from the source for this target; TabBench-Bio ranks by macro-F1 (Sec. 3.5).
- Reject check (AI, 2026-11-25): stands. The registry calls the target a "Target metadata field 'host sex'" (https://raw.githubusercontent.com/not-a-feature/TabBench-Bio/main/src/tabbench_bio/bio/data/bio_datasets.json), and the BioProject studies antibiotics and the preterm resistome (https://www.ncbi.nlm.nih.gov/bioproject/PRJNA301903, SEL-8). An infant's sex is known at birth and no actor predicts it from stool (road_safety_gender); the parent BioSamples' other fields (day of life, birth weight, e.g. SAMN04436924) are known without the stool.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 394 x 12,651; target: host sex.
- Why: Host sex from preterm infant gut metagenome InterPro profiles (TPA of PRJNA301903)
- Notes: Longitudinal infant sampling in the source project (repeated samples per infant likely). Target is a metadata field.
