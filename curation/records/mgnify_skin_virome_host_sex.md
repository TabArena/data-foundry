---
unique_name: mgnify_skin_virome_host_sex
name: MGYS00005384 MGnify functional profile
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
collection_period: Jul 2013 - Oct 2013
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

**Screening (AI, 2026-11-25):** `No` (`No Good Target / Scientific Discovery`, SEL-3 with USE-2 and SEL-8): the sex of 16 healthy volunteers, predicted from 674 skin bacterial and viral metagenome profiles; a sample-metadata field TabBench-Bio picked as the target of a study of the skin virome.
- Source: Hannigan et al., "The Human Skin Double-Stranded DNA Virome: Topographical and Temporal Diversity, Genetic Enrichment, and Dynamic Associations with the Host Microbiome", mBio 6 (2015; doi 10.1128/mBio.01578-15); BioProject PRJNA266117 (University of Pennsylvania), MGnify MGYS00005384: 674 samples (host sex 334 male, 340 female); MGnify's sample fields: collection date, host sex, host taxon. The parent BioSamples carry `SubjectID`, `TimePoint` (1 to 3), `Visit_Date`, `Site_Symbol`, `Type` (Virome or Microbiome), age and sex; 69 samples are negative controls (`Site_Symbol` Neg) that still carry a subject's sex. As TabBench-Bio ships it: 674 x 17,026 InterPro counts, target host sex (registry, read 2026-11-25).
- Use case: none (fit none, USE-8). The study describes the skin virome by site, person and time (SEL-8); a donor's sex is recorded at sampling and no decision rests on predicting it. Skin-microbiome forensics is a research topic, but no source names it here. Collection: 20 subject ids (16 with about 37 samples each, 4 with 3), sampled at three time points from 2013-07-22 to 2013-10-08 (`Visit_Date`; MGnify's `collection date`, 2013-08 to 2014-05, does not match it), so samples over time, dated, several per person; the target exists with the features; type `Panel Data` by SPLIT-34 rule 1 (301 of 310 subject-site-library units seen at two or more time points), a curator's call against `Experimental Results` since a visit gives several rows.
- Split: no leaf walked: no task (USE-2). The label has 16 independent units.
- Siblings and duplicates: `mgnify_skin_surface_environment_material` (another skin project, PRJNA46333), `mgnify_t2d_gut_host_sex`, `mgnify_hiv_gut_host_sex`, `mgnify_preterm_infant_gut_host_sex`, `mgnify_vegetable_oil_diet_gut_host_sex`. Precedent: `road_safety_gender` (CC: "likely gender was picked as random target"). External collections: TabBench-Bio (Table 4).
- Better data: not searched (no task).
- Metric: none from the source for this target; TabBench-Bio ranks by macro-F1 (Sec. 3.5).
- Reject check (AI, 2026-11-25): stands. The registry calls the target a "Target metadata field 'host sex'" (https://raw.githubusercontent.com/not-a-feature/TabBench-Bio/main/src/tabbench_bio/bio/data/bio_datasets.json), and the study sampled "eight anatomical skin sites of 16 healthy individuals over two months" to describe the virome (https://www.ebi.ac.uk/metagenomics/studies/MGYS00005384, SEL-8). No source names a forensic or QC use; the label has 16 independent units, and 69 of its rows are negative controls (BioSamples, e.g. SAMN03160151 for the fields).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 674 x 17,026; target: host sex.
- Why: Host sex from InterPro functional profiles of skin bacterial and viral metagenomes (PRJNA266117, Hannigan et al. 2015)
- Notes: Target is a sample-metadata field (host sex), not a clinical outcome. Several samples per person and body site in the source study.
