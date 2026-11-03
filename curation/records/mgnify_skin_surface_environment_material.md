---
unique_name: mgnify_skin_surface_environment_material
name: MGYS00005379 MGnify functional profile
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
- https://doi.org/10.1038/nature13786
- https://www.ebi.ac.uk/metagenomics/studies/MGYS00005379
- https://arxiv.org/abs/2609.07441
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`No Good Target / Scientific Discovery`; SEL-3, USE-2, SEL-8): the coded sampling material of skin metagenomes from the NISC skin project, predicted from InterPro profiles; a sample-metadata field TabBench-Bio picked as the target, set by whoever took the sample.
- Source: NISC BioProject PRJNA46333, "Gene-Environment Interactions at the Skin Surface" (NIH Intramural Sequencing Center; the ENA text describes the umbrella project's skin microbiota of atopic dermatitis patients and controls). The record's DOI, Oh et al., "Biogeography and individuality shape function in the human skin metagenome", Nature 514:59-64 (2014; doi 10.1038/nature13786), is inferred from the project, not linked by MGnify (which links only its own pipeline paper). MGnify MGYS00005379, a third-party assembly: 420 samples, 1,884 analyses, collected 2011-2014; `environment (material)` takes the codes Ss (358), Sw (34), Cut (22) and pool (4), 2 missing; `environment (feature)` codes the body site and side (Al-R, Ea-R, Tw-R ...). As TabBench-Bio ships it: 1,450 x 14,826 InterPro counts, target `environment (material)`, 2 classes.
- Why out: the registry's words: "MGnify IPR functional profile. Target metadata field 'environment (material)', 2 classes" (TabBench-Bio `bio_datasets.json`, MGYS00005379). The material is a code of the sampling protocol, known to whoever took the sample; no actor predicts it (USE-2, SEL-3), fit none (USE-8). The project collected the samples to describe skin communities by site, person and time (SEL-8). Precedent: `road_safety_gender` (`No`, a field picked as a target).
- Also noted: 1,450 rows for 420 samples (several analyses per sample), many body sites per person, no group column in the registry.
- Siblings and duplicates: `mgnify_skin_virome_host_sex` (another skin project, PRJNA266117), `mgnify_hmp_isolation_source` and `mgnify_latin_america_resistome_biome` (sampling fields as targets), the host-sex records `mgnify_t2d_gut_host_sex`, `mgnify_hiv_gut_host_sex`, `mgnify_preterm_infant_gut_host_sex`, `mgnify_vegetable_oil_diet_gut_host_sex`. External collections: TabBench-Bio (Table 4).
- Better data: a candidate of the benchmark TabBench-Bio (the run searched no further).
- Metric: none from the source for this target; TabBench-Bio ranks by macro-F1 (Sec. 3.5).
- Reject check (AI, 2026-10-31): stands. Registry: 'Target metadata field 'environment (material)', 2 classes' (MGYS00005379, https://raw.githubusercontent.com/not-a-feature/TabBench-Bio/main/src/tabbench_bio/bio/data/bio_datasets.json); MGnify's sample metadata codes it 'Ss' or 'Sw' beside the site code in 'environment (feature)' (e.g. SRS1307608 'Ss', SRS728457 'Sw'; https://www.ebi.ac.uk/metagenomics/api/v1/studies/MGYS00005379/samples): a sampling code the sampler sets, which nobody predicts. The project describes skin communities (SEL-8).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 1,450 x 14,826; target: environment (material).
- Why: Environment material from InterPro functional profiles (TPA of PRJNA46333, 'Gene-Environment Interactions at the Skin Surface')
- Notes: First publication inferred from the project (NISC skin metagenome, Oh et al. 2014). Many body sites per person; target is sampling metadata.
