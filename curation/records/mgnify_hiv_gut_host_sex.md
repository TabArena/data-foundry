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
collections:
- TabBench-Bio
source_links:
- https://www.ebi.ac.uk/metagenomics/studies/MGYS00001255
- https://arxiv.org/abs/2609.07441
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`No Good Target / Scientific Discovery`, USE-2 with SEL-8): the target is the participants' recorded sex, a metadata field the benchmark picked from a study of HIV-1 and the gut microbiome; no one decides anything by predicting a person's sex from a stool sample.
- Source: MGnify study MGYS00001255 (https://www.ebi.ac.uk/metagenomics/studies/MGYS00001255), harvested from BioProject PRJNA307231 / SRP068240, "Human feces metagenome 16s rDNA sequencing" (IrsiCaixa Foundation, registered 2015-12-30); the study: Noguera-Julian, Rocafort, Guillen et al., "Gut Microbiota Linked to Sexual Preference and HIV Infection", EBioMedicine 5:135-146, 2016 (https://doi.org/10.1016/j.ebiom.2016.01.032). In MGnify: 350 samples with `host sex` (261 male, 89 female), `host age`, `host body-mass index` and other fields; TabBench-Bio keeps 152 x 14,103 (122 male, 30 female) and calls the features an InterPro functional profile, while the study is 16S amplicon sequencing.
- The task: the study's aim, in its abstract: "The precise effects of HIV-1 on the human microbiome are unclear ... we first tested 129 HIV-1-infected subjects and 27 HIV-negative controls in Barcelona (BCN0)"; the benchmark's registry: "Target metadata field 'host sex', 2 classes". The original task is HIV status and sexual practice (SEL-8); host sex is recorded at enrolment, so no decision fits (USE-2). HIV status is diagnosed by a blood test, so the study's own label gives no prediction task either.
- Siblings and duplicates: the other MGnify host-sex records of TabBench-Bio, `mgnify_preterm_infant_gut_host_sex`, `mgnify_t2d_gut_host_sex`, `mgnify_vegetable_oil_diet_gut_host_sex` and `mgnify_skin_virome_host_sex`, carry the same kind of label; precedent `bog_lakes` (`No`, SEL-3: a target that replays the sampling design). External collections: TabBench-Bio (arXiv 2609.07441, Table 4).
- Better data: a candidate of the benchmark TabBench-Bio; no new search in this run.
- Metric: none (no task).
- Reject check (AI, 2026-10-31): stands. The benchmark picked 'Target metadata field 'host sex'' (TabBench-Bio registry, https://github.com/not-a-feature/TabBench-Bio) from a study of HIV-1 and the gut microbiome (https://www.ebi.ac.uk/metagenomics/studies/MGYS00001255). Sex is recorded at enrolment and no decision predicts it from stool, as on bog_lakes. The study's own label, HIV status, is diagnosed by a blood test, so no re-target fixes it.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 152 x 14,103; target: host sex (122 male / 30 female).
- Why: Host sex from human faecal metagenome profiles (PRJNA307231, an HIV-1 microbiome study)
- Notes: MGnify titles the study '16s rDNA sequencing', while the registry calls the features an InterPro functional profile. Target is a metadata field.
