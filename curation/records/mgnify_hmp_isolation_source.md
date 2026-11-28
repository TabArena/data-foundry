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
- Experimental Results
- 'Samples: Over Time'
- 'Time: Lost'
- 'Entities: Recur'
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

**Screening (AI, 2026-11-25):** `No` (`No Good Target / Scientific Discovery`, SEL-3 with USE-2 and SEL-8): the HMP published these samples as "a unique reference resource of microbiome samples from healthy adults", and TabBench-Bio picked the metadata field `isolation source`, the body site a sample was taken from (oral, gut, vaginal), as the target.
- Source: HMP Phase III whole-genome shotgun, BioProject PRJNA275349 (JCVI), in MGnify twice: MGYS00001056 from the reads (289 samples) and MGYS00005380, EMBL-EBI's TPA assemblies of the same project (275 samples); the paper: Lloyd-Price, Mahurkar, Rahnavard et al., "Strains, functions and dynamics in the expanded Human Microbiome Project", Nature 550:61-66, 2017 (https://doi.org/10.1038/nature23889). MGnify `isolation source`: ORAL 172, GUT 89, VAGINAL 28 (MGYS00001056) and 163, 87, 25 (MGYS00005380); TabBench-Bio keeps two classes, 306 x 15,268 and 264 x 16,690 (registry, read 2026-11-25).
- Use case: none (fit none, USE-8). The data is a reference resource (SEL-8). The one actor we could think of, a forensic lab naming the body fluid of a stain, is named by no source; forensic stains are not clinical swabs from healthy volunteers, and oral against gut communities would likely be `Trivial` too (TP-4), not tested. Collection: healthy volunteers sampled at several body sites over up to three visits, so samples over time with several rows per person; `collection date` is "missing" on all samples of both studies, and neither MGnify nor the BioSamples name subject or visit, so time lost here; the target exists with the features; type `Experimental Results` (volunteers measured by a study protocol).
- Split: no leaf walked: no task (USE-2).
- Siblings and duplicates: the two MGnify studies are one project and share samples (the record holds both, PROV-6); `mgnify_skin_surface_environment_material` and `mgnify_latin_america_resistome_biome` carry sampling labels of the same kind. External collections: TabBench-Bio (arXiv 2609.07441, Table 4).
- Better data: not searched (no task).
- Metric: none from the source for this target; TabBench-Bio ranks by macro-F1 (Sec. 3.5).
- Reject check (AI, 2026-11-25): stands. HMP Phase III "represents a unique reference resource of microbiome samples from healthy adults" (https://www.ebi.ac.uk/metagenomics/studies/MGYS00001056, SEL-3, SEL-8), and the registry calls the target a "Target metadata field 'isolation source'" (https://raw.githubusercontent.com/not-a-feature/TabBench-Bio/main/src/tabbench_bio/bio/data/bio_datasets.json). Forensic body-fluid identification is the only plausible actor and no source names it; the BioSamples (e.g. SAMN03351684) hold only the sample id, the isolation source and a missing date.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 264 x 16,690; target: isolation source (2 classes; the paper writes 'source').
- Why: Body-site isolation source from InterPro functional profiles (MGnify TPA assemblies of HMP WGS project PRJNA275349) | Body-site isolation source from InterPro functional profiles (HMP phase III WGS, PRJNA275349)
- Notes: Same HMP project PRJNA275349 as MGYS00001056 (one from TPA assemblies, one from reads), so the two tasks share samples. Target is sampling metadata. | Shares the HMP project with MGYS00005380. Target is sampling metadata.
