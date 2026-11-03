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
collections:
- TabBench-Bio
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

**Screening (AI, 2026-10-31):** `No` (`No Good Target / Scientific Discovery`, USE-2 with SEL-8): the target `environment (biome)` is where a sample was collected (a rural village in El Salvador, a peri-urban shantytown in Lima), the sampling design of a resistome study, known when the sample is taken.
- Source: MGnify MGYS00005381, EMBL-EBI's TPA assemblies of BioProject PRJNA300541, "Antibiotic resistance exchange between microbiota in resource-poor settings in Latin America" (Washington University in St. Louis, registered 2015-10-29); the paper: Pehrsson, Tsukayama, Patel et al., "Interconnected microbiomes and resistomes in low-income human habitats", Nature 533:212-216, 2016 (https://doi.org/10.1038/nature17672). MGnify sample fields: `environment (biome)` rural village 129, periurban shantytown 68, sewage system 23 (220 samples), with `environment (material)` (feces, sewage, soil, water, composting feces) and `host sex`; TabBench-Bio keeps 218 x 13,394 with two classes.
- The task: "Microbiome and resistome of human fecal and environmental microbiota from rural El Salvador and peri-urban Lima, Peru" (BioProject); the benchmark's registry: "Target metadata field 'environment (biome)', 2 classes". Every rural-village sample is from El Salvador and every shantytown and sewage sample from Lima (MGnify country field), so the label is the country sampled and replays the design (SEL-8, USE-2; precedent `bog_lakes`).
- Siblings and duplicates: the other sampling-label records of TabBench-Bio, `mgnify_hmp_isolation_source` and `mgnify_skin_surface_environment_material`. External collections: TabBench-Bio (arXiv 2609.07441, Table 4).
- Better data: a candidate of the benchmark TabBench-Bio; no new search in this run.
- Metric: none (no task).
- Reject check (AI, 2026-10-31): stands. The project studies the 'Microbiome and resistome of human fecal and environmental microbiota from rural El Salvador and peri-urban Lima, Peru' (https://www.ncbi.nlm.nih.gov/bioproject/PRJNA300541). In MGnify every rural-village sample is from El Salvador and every shantytown and sewage sample from Lima (https://www.ebi.ac.uk/metagenomics/studies/MGYS00005381), so the biome target replays where the samples were taken (bog_lakes).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 218 x 13,394; target: environment (biome).
- Why: Sample biome from InterPro functional profiles (TPA of PRJNA300541, antibiotic resistance exchange in low-income settings, El Salvador and Peru)
- Notes: First publication inferred from the project title (Pehrsson et al. 2016). Target is a sampling-metadata field.
