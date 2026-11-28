---
unique_name: mgnify_hiv_gut_host_sex
name: MGYS00001255 MGnify functional profile
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target / Scientific Discovery
tags:
- AI-Filled (Verify)
- Dated Event Log
- 'Samples: Over Time'
- 'Time: Dated'
collections:
- TabBench-Bio
collection_period: 2010-2014
source_links:
- https://www.ebi.ac.uk/metagenomics/studies/MGYS00001255
- https://arxiv.org/abs/2609.07441
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-11-25):** `No` (`No Good Target / Scientific Discovery`, SEL-3 with USE-2 and SEL-8): the target is the participants' recorded sex, a metadata field TabBench-Bio picked from a study of HIV-1 and the gut microbiome; sex is recorded at enrolment and no one decides anything by predicting it from a stool sample.
- Source: MGnify MGYS00001255 (https://www.ebi.ac.uk/metagenomics/studies/MGYS00001255), harvested from BioProject PRJNA307231 / SRP068240, "Human feces metagenome 16s rDNA sequencing" (IrsiCaixa Foundation, registered 2015-12-30); the study: Noguera-Julian, Rocafort, Guillen et al., "Gut Microbiota Linked to Sexual Preference and HIV Infection", EBioMedicine 5:135-146, 2016 (https://doi.org/10.1016/j.ebiom.2016.01.032). In MGnify: 350 samples (cohorts BCN0 156, BCN1 110, STK 84 by sample name) with `host sex` (261 male, 89 female), `host age`, `host body-mass index`, `collection date` and other fields; TabBench-Bio keeps 152 x 14,103 (122 male, 30 female; registry, read 2026-11-25) and calls the features an InterPro functional profile, while MGnify titles the study 16S amplicon sequencing.
- Use case: none (fit none, USE-8). The registry's words: "Target metadata field 'host sex', 2 classes"; the study's own task is HIV status and sexual practice (SEL-8). The parent BioSamples also carry `HIV_serostatus`, `CD4+_Tcell_counts` and `HIV_viral_load`, all measured in blood, so no re-target gives a decision either. Collection: samples over time, each MGnify sample carrying a `collection date` (2010-01-15 to 2014-12-23 over all 350); the target exists with the features; whether a person has several samples is not settled (no subject id in MGnify or the BioSamples; BCN1 and STK are further cohorts); type `Dated Event Log` (patients' stool samples whose rows record a date, SPLIT-34 rule 3).
- Split: no leaf walked: no task (USE-2).
- Siblings and duplicates: the other MGnify host-sex records of TabBench-Bio (`mgnify_preterm_infant_gut_host_sex`, `mgnify_t2d_gut_host_sex`, `mgnify_vegetable_oil_diet_gut_host_sex`, `mgnify_skin_virome_host_sex`) carry the same kind of label; precedents `road_safety_gender` (a field picked as a target) and `bog_lakes` (a target that replays the sampling design). External collections: TabBench-Bio (arXiv 2609.07441, Table 4).
- Better data: not searched (no task).
- Metric: none from the source for this target; TabBench-Bio ranks by macro-F1 (Sec. 3.5).
- Reject check (AI, 2026-11-25): stands. The registry calls the target a "Target metadata field 'host sex'" (https://raw.githubusercontent.com/not-a-feature/TabBench-Bio/main/src/tabbench_bio/bio/data/bio_datasets.json), and the study was collected for HIV-1 and the gut microbiome (SEL-8). A sex check on a metagenome reads the human X/Y reads, which MGnify removes, so no QC use rests on microbial profiles; the study's other labels (HIV serostatus, CD4 count, viral load in the BioSamples, e.g. SAMN04382195) are blood measurements.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 152 x 14,103; target: host sex (122 male / 30 female).
- Why: Host sex from human faecal metagenome profiles (PRJNA307231, an HIV-1 microbiome study)
- Notes: MGnify titles the study '16s rDNA sequencing', while the registry calls the features an InterPro functional profile. Target is a metadata field.
