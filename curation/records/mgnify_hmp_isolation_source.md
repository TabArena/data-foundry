---
unique_name: mgnify_hmp_isolation_source
name: MGYS00005380 MGnify functional profile
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
- https://doi.org/10.1038/nature23889
- https://www.ebi.ac.uk/metagenomics/studies/MGYS00005380
- https://arxiv.org/abs/2609.07441
- https://www.ebi.ac.uk/metagenomics/studies/MGYS00001056
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`No Good Target / Scientific Discovery`, USE-2 with SEL-8): the target is the body site a Human Microbiome Project sample was taken from (oral, gut, vaginal), recorded when the sample is taken; the HMP published these samples as a reference resource, not for predicting the site.
- Source: HMP Phase III whole-genome shotgun, BioProject PRJNA275349 (JCVI), in MGnify twice: MGYS00001056 from the reads (289 samples) and MGYS00005380, EMBL-EBI's TPA assemblies of the same project (275 samples); the paper: Lloyd-Price, Mahurkar, Rahnavard et al., "Strains, functions and dynamics in the expanded Human Microbiome Project", Nature 550:61-66, online 2017-09-20 (https://doi.org/10.1038/nature23889). MGnify `isolation source`: ORAL 172, GUT 89, VAGINAL 28 (MGYS00001056) and 163, 87, 25 (MGYS00005380); TabBench-Bio keeps two classes, 306 x 15,268 and 264 x 16,690.
- The task: "The sample collection represents a unique reference resource of microbiome samples from healthy adults ... In Phase III, a focus was placed on six of the 18 body sites", with "as many of the longitudinal samples (second and third visits by the same individual) as possible" (MGYS00001056 abstract); the benchmark's registry: "Target metadata field 'isolation source', 2 classes". The body site is the sampling design, known when the sample is taken (SEL-8, USE-2; as on `bog_lakes`, where lake and layer as targets "would replay the sampling design"). Oral against gut communities would likely be `Trivial` too (TP-4), not tested.
- Siblings and duplicates: the two MGnify studies are one project and share samples (the record holds both, PROV-6); `mgnify_skin_surface_environment_material` and `mgnify_latin_america_resistome_biome` carry sampling labels of the same kind. External collections: TabBench-Bio (arXiv 2609.07441, Table 4).
- Better data: a candidate of the benchmark TabBench-Bio; no new search in this run.
- Metric: none (no task).
- Reject check (AI, 2026-10-31): stands. HMP Phase III 'represents a unique reference resource of microbiome samples from healthy adults', with 'a focus ... on six of the 18 body sites' (https://www.ebi.ac.uk/metagenomics/studies/MGYS00001056). The target 'isolation source' (oral, gut, vaginal) is the sampling design, known when the sample is taken (bog_lakes).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 264 x 16,690; target: isolation source (2 classes; the paper writes 'source').
- Why: Body-site isolation source from InterPro functional profiles (MGnify TPA assemblies of HMP WGS project PRJNA275349) | Body-site isolation source from InterPro functional profiles (HMP phase III WGS, PRJNA275349)
- Notes: Same HMP project PRJNA275349 as MGYS00001056 (one from TPA assemblies, one from reads), so the two tasks share samples. Target is sampling metadata. | Shares the HMP project with MGYS00005380. Target is sampling metadata.
