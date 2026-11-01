---
unique_name: mgnify_preterm_infant_gut_host_sex
name: MGYS00002425 MGnify functional profile
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
- https://www.ebi.ac.uk/metagenomics/studies/MGYS00002425
- https://arxiv.org/abs/2609.07441
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`No Good Target / Scientific Discovery`, USE-2 with SEL-8): the target is the recorded sex of preterm infants in a study of antibiotics and the infant gut resistome; the sex is known at birth and no decision rests on predicting it from stool.
- Source: MGnify MGYS00002425, EMBL-EBI's TPA assemblies of BioProject PRJNA301903, "Metagenomic sequencing of preterm infant gut microbiota raw sequence reads" (Washington University in St. Louis, registered 2015-11-11); the paper: Gibson, Wang, Ahmadi et al., "Developmental dynamics of the preterm infant gut microbiota and antibiotic resistome", Nat Microbiol 1:16024, 2016-03-07 (https://doi.org/10.1038/nmicrobiol.2016.24). MGnify: 387 samples, `host sex` male 157, female 230, counted per sample, not per infant; TabBench-Bio keeps 394 x 12,651.
- The task: "By analyzing 401 fecal samples from 84 longitudinally-sampled preterm infants, we demonstrate that meropenem, cefotaxime, and ticarcillin-clavulanate significantly reduce species richness during their administration" (BioProject); the benchmark's registry: "Target metadata field 'host sex', 2 classes". The original task is the effect of antibiotics (SEL-8); host sex is a sampling field (USE-2); and with about 5 samples per infant, any task here would rest on 84 units.
- Siblings and duplicates: `mgnify_hiv_gut_host_sex`, `mgnify_t2d_gut_host_sex`, `mgnify_vegetable_oil_diet_gut_host_sex` and `mgnify_skin_virome_host_sex` carry the same kind of label; precedent `bog_lakes`. External collections: TabBench-Bio (arXiv 2609.07441, Table 4).
- Better data: a candidate of the benchmark TabBench-Bio; no new search in this run.
- Metric: none (no task).
- Reject check (AI, 2026-10-31): stands. TabBench-Bio's registry: 'MGnify IPR functional profile. Target metadata field 'host sex', 2 classes' (MGYS00002425, https://raw.githubusercontent.com/not-a-feature/TabBench-Bio/main/src/tabbench_bio/bio/data/bio_datasets.json); the paper gives no reason for its MGnify targets. The BioProject studies antibiotics and the preterm gut resistome (https://www.ncbi.nlm.nih.gov/bioproject/PRJNA301903): an infant's sex is known at birth and no actor predicts it from stool (precedent road_safety_gender, Lennart: 'likely gender was picked as random target'). No other target in MGnify's metadata to re-target to.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 394 x 12,651; target: host sex.
- Why: Host sex from preterm infant gut metagenome InterPro profiles (TPA of PRJNA301903)
- Notes: Longitudinal infant sampling in the source project (repeated samples per infant likely). Target is a metadata field.
