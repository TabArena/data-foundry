---
unique_name: mgnify_latin_america_resistome_biome
name: MGYS00005381 MGnify functional profile
checked_by:
- AI (UNVERIFIED)
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
collection_period: 2012-2014
source_links:
- https://doi.org/10.1038/nature17672
- https://www.ebi.ac.uk/metagenomics/studies/MGYS00005381
- https://arxiv.org/abs/2609.07441
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-11-25):** `No` (`No Good Target / Scientific Discovery`, SEL-3 with USE-2 and SEL-8): the target `environment (biome)` is where a sample was collected (a rural village in El Salvador, a peri-urban shantytown in Lima), the sampling design of a resistome study, known when the sample is taken.
- Source: MGnify MGYS00005381, EMBL-EBI's TPA assemblies of BioProject PRJNA300541, "Antibiotic resistance exchange between microbiota in resource-poor settings in Latin America" (Washington University in St. Louis, registered 2015-10-29); the paper: Pehrsson, Tsukayama, Patel et al., "Interconnected microbiomes and resistomes in low-income human habitats", Nature 533:212-216, 2016 (https://doi.org/10.1038/nature17672). MGnify sample fields: `environment (biome)` rural village 129, periurban shantytown 68, sewage system 23 (220 samples), with `environment (material)` (feces, sewage, soil, water, composting feces), `host sex` and `collection date`; the parent BioSamples add `host_subject_id` on 161 human samples and `house` on 59 environmental ones. TabBench-Bio keeps 218 x 13,394 with two classes (registry, read 2026-11-25), which two not stated.
- Use case: none (fit none, USE-8). All 129 rural-village samples are from El Salvador and all 91 shantytown and sewage samples from Lima (MGnify country field), so the label is the country sampled and replays the design (precedent `bog_lakes`). Collection: households and their surroundings sampled over 2012-2014 (`collection date` 2012-01-15 to 2014-01-17); 85 people by `host_subject_id`, 49 of them sampled two or three times on different dates (2013-01-07, 2013-01-14, 2014-01-14), so 125 of 220 samples come from people seen twice or more; the target exists with the features; type `Panel Data` by SPLIT-34 rule 1, a curator's call against `Survey` since 59 rows are environmental samples.
- Split: no leaf walked: no task (USE-2).
- Siblings and duplicates: the other sampling-label records of TabBench-Bio, `mgnify_hmp_isolation_source` and `mgnify_skin_surface_environment_material`. External collections: TabBench-Bio (arXiv 2609.07441, Table 4).
- Better data: not searched (no task).
- Metric: none from the source for this target; TabBench-Bio ranks by macro-F1 (Sec. 3.5).
- Reject check (AI, 2026-11-25): stands. The registry calls the target a "Target metadata field 'environment (biome)'" (https://raw.githubusercontent.com/not-a-feature/TabBench-Bio/main/src/tabbench_bio/bio/data/bio_datasets.json), and the project studies the "Microbiome and resistome of human fecal and environmental microbiota from rural El Salvador and peri-urban Lima, Peru" (https://www.ncbi.nlm.nih.gov/bioproject/PRJNA300541, SEL-8). Over all 220 MGnify samples the biome and the country coincide (https://www.ebi.ac.uk/metagenomics/studies/MGYS00005381), so the target replays where the samples were taken (bog_lakes); no source names an actor who would predict it.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 218 x 13,394; target: environment (biome).
- Why: Sample biome from InterPro functional profiles (TPA of PRJNA300541, antibiotic resistance exchange in low-income settings, El Salvador and Peru)
- Notes: First publication inferred from the project title (Pehrsson et al. 2016). Target is a sampling-metadata field.
