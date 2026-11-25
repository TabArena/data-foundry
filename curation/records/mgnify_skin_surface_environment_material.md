---
unique_name: mgnify_skin_surface_environment_material
name: MGYS00005379 MGnify functional profile
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
- Experimental Results
- 'Samples: Over Time'
- 'Time: Dated'
- 'Entities: Recur'
collections:
- TabBench-Bio
collection_period: 2011-2014
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

**Screening (AI, 2026-11-25):** `No` (`No Good Target / Scientific Discovery`, SEL-3 with USE-2 and SEL-8): the coded sampling material of skin metagenomes from the NISC skin project, predicted from InterPro profiles; a sample-metadata field TabBench-Bio picked as the target, set by whoever took the sample.
- Source: NISC BioProject PRJNA46333, "Gene-Environment Interactions at the Skin Surface" (NIH Intramural Sequencing Center). The record's DOI, Oh et al., "Biogeography and individuality shape function in the human skin metagenome", Nature 514:59-64 (2014; doi 10.1038/nature13786), is inferred from the project, not linked by MGnify. MGnify MGYS00005379, a third-party assembly: 420 samples, 1,884 analyses; `environment (material)` takes the codes Ss (358), Sw (34), Cut (22) and pool (4), 2 missing, and no source spells the codes out, so "material" is MGnify's field name, not a decoded meaning; `environment (feature)` codes the body site and side. As TabBench-Bio ships it: 1,450 x 14,826 InterPro counts, 2 classes (registry, read 2026-11-25).
- Use case: none (fit none, USE-8). The material is a code of the sampling protocol, known to whoever took the sample; the project collected the samples to describe skin communities by site, person and time (SEL-8). Collection: healthy volunteers sampled at many body sites over 2011-2014 (`collection date` 2011-06-24 to 2014-05-29 on 416 of 420 samples, 4 "not applicable"), so samples over time, dated, several per person; 1,450 rows for 420 samples (several analyses per sample), no person id in MGnify or the BioSamples; the target exists with the features; type `Experimental Results` (volunteers measured by a study protocol; its dated rows keep the type, SPLIT-34 rule 3).
- Split: no leaf walked: no task (USE-2).
- Siblings and duplicates: `mgnify_skin_virome_host_sex` (another skin project, PRJNA266117), `mgnify_hmp_isolation_source` and `mgnify_latin_america_resistome_biome` (sampling fields as targets), the host-sex records `mgnify_t2d_gut_host_sex`, `mgnify_hiv_gut_host_sex`, `mgnify_preterm_infant_gut_host_sex`, `mgnify_vegetable_oil_diet_gut_host_sex`. Precedent: `road_safety_gender` (`No`, a field picked as a target). External collections: TabBench-Bio (Table 4).
- Better data: not searched (no task).
- Metric: none from the source for this target; TabBench-Bio ranks by macro-F1 (Sec. 3.5).
- Reject check (AI, 2026-11-25): stands. The registry calls the target a "Target metadata field 'environment (material)'" (https://raw.githubusercontent.com/not-a-feature/TabBench-Bio/main/src/tabbench_bio/bio/data/bio_datasets.json), and MGnify and the BioSamples (e.g. SAMN04359892) hold it as a protocol code beside the site code (https://www.ebi.ac.uk/metagenomics/api/v1/studies/MGYS00005379/samples): a sampling code the sampler sets, which no actor predicts. The project describes skin communities (SEL-8).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 1,450 x 14,826; target: environment (material).
- Why: Environment material from InterPro functional profiles (TPA of PRJNA46333, 'Gene-Environment Interactions at the Skin Surface')
- Notes: First publication inferred from the project (NISC skin metagenome, Oh et al. 2014). Many body sites per person; target is sampling metadata.
