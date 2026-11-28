---
unique_name: mgnify_t2d_gut_host_sex
name: MGYS00005285 MGnify functional profile
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target / Scientific Discovery
tags:
- AI-Filled (Verify)
- Clinical Study
- 'Samples: Over Time'
- 'Time: Lost'
collections:
- TabBench-Bio
source_links:
- https://doi.org/10.1038/nature11450
- https://www.ebi.ac.uk/metagenomics/studies/MGYS00005285
- https://arxiv.org/abs/2609.07441
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-11-25):** `No` (`No Good Target / Scientific Discovery`, SEL-3 with USE-2 and SEL-8): the sex of the donors of a type 2 diabetes gut-metagenome study, predicted from InterPro profiles; a sample-metadata field TabBench-Bio picked as the target, and no decision rests on predicting a person's sex from their stool.
- Source: Qin et al., "A metagenome-wide association study of gut microbiota in type 2 diabetes", Nature 490:55-60 (2012; doi 10.1038/nature11450); ENA PRJNA422434 (SRP008047; linked to PubMed 23023125). MGnify MGYS00005285 is EMBL-EBI's third-party assembly of it: 369 samples and 439 analyses; its sample metadata holds age, host sex (213 male, 156 female), instrument and host taxon, and no diabetes status and no collection date; the parent BioSamples hold only nation, gender and age. As TabBench-Bio ships it: 438 x 12,705 InterPro counts, target host sex (registry, read 2026-11-25).
- Use case: none (fit none, USE-8). The data was collected to study type 2 diabetes (SEL-8); a donor's sex is recorded at sampling. The study's own label (type 2 diabetes against control) is not in MGnify's metadata, so it is no re-target of this table; a case-control MGWAS label would be a record of its own (curatedMetagenomicData carries the cohort with its labels), not this one. Collection: Chinese volunteers recruited over time for a two-stage case-control study; no date among MGnify's or the BioSamples' fields, so time lost; one sample per person as far as the sample names show (369 distinct names, `bgi-T2D-143A` and the like; 438 rows for 369 samples are several analyses per sample); the target exists with the features; type `Clinical Study`.
- Split: no leaf walked: no task (USE-2).
- Siblings and duplicates: `mgnify_hiv_gut_host_sex`, `mgnify_preterm_infant_gut_host_sex`, `mgnify_skin_virome_host_sex`, `mgnify_vegetable_oil_diet_gut_host_sex` (host sex from other studies), `mgnify_skin_surface_environment_material`, `mgnify_hmp_isolation_source`, `mgnify_latin_america_resistome_biome` (sampling fields). No record of the Qin 2012 cohort with its diabetes label (grep: nature11450, PRJNA422434). Precedent: `road_safety_gender`. External collections: TabBench-Bio (Table 4).
- Better data: not searched (no task).
- Metric: none from the source for this target; TabBench-Bio ranks by macro-F1 (Sec. 3.5).
- Reject check (AI, 2026-11-25): stands. The registry calls the target a "Target metadata field 'host sex'" (https://raw.githubusercontent.com/not-a-feature/TabBench-Bio/main/src/tabbench_bio/bio/data/bio_datasets.json), and the study is a "metagenome-wide association study" of type 2 diabetes (https://www.ebi.ac.uk/ena/browser/view/PRJNA422434, SEL-8). A donor's sex is recorded at sampling and no actor predicts it (road_safety_gender); the BioSamples (e.g. SAMN00791948) carry no other label to re-target to.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 438 x 12,705; target: host sex.
- Why: Host sex from gut metagenome InterPro profiles (TPA of PRJNA422434, titled as the type 2 diabetes MGWAS of Qin et al. 2012)
- Notes: First publication inferred from the MGnify study title; the link from PRJNA422434 to Qin et al. 2012 is not confirmed. Target is a metadata field.
