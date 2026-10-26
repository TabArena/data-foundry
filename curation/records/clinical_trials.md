---
unique_name: clinical_trials
name: Clinical Trials
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- No Good Target (yet)
- TBD
tags:
- 2nd Tier / Scientific Discovery
- Non-IID (Temporal)
- AI-Filled (Verify)
collections:
- New (BeyondArena)
domain: medical & healthcare
required_split:
- Temporal (NON-IID)
problem_type: TBD
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/thedevastator/a-quick-overview-of-clinical-trials
- https://www.aerodatalab.org/birds-eye-view-of-research-landscape
source_row: 849
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 1: a descriptive extract of ClinicalTrials.gov published "to provide a bird's-eye view of the clinical trial landscape", with no target; a trial-termination task would need its own build from the registry.
- Source: Kaggle upload by thedevastator (2022-11-25, one file `AERO-BirdsEye-Data.csv`, 9.7 MB, about 13K trials per its subtitle), credited to Aero Data Lab, whose page (the second link) now shows an expired Squarespace site. The Kaggle text: "The purpose of this dataset is to provide a bird's-eye view of the clinical trial landscape"; columns NCT, Sponsor, Title, Summary, Start Year, Start Month, Phase, Enrollment, Status (Recruiting ... Completed, Suspended, Terminated), Condition; "Research Ideas": "Identify patterns in clinical trials", "Understand how different sponsors fund clinical trials". The trials themselves come from ClinicalTrials.gov (NCT numbers), the first publisher of the records (PROV-8).
- Use case: none named; a framing that exists in the literature is predicting whether a trial terminates early from what is known at registration (a sponsor or a funder deciding on a trial), but the table mixes ongoing trials (Recruiting, Active) with finished ones and keeps only a few registration fields; fit approximate at best. Regime temporal by start date if a target is defined.
- Siblings and duplicates: `covid_trials` (Alex, Mustafa, Lennart `No`, `No Good Target / Scientific Discovery`: another ClinicalTrials.gov extract where no meaningful predictive task was seen), `trec_2022_clinical_trials_dataset` (retrieval, a different task). Not a duplicate of either. External collections: none found.
- Papers and pages: the Kaggle page only; no paper or competition defines a task on this extract.
- Metric: none found (the Kaggle description, the dead Aero Data Lab page), so the fallback if a target is ever defined (MET-1, MET-11).
- Risks for /add-dataset: no target (SEL-3; `No Good Target (yet)`); Status is a snapshot at download, so a termination label for recent trials is unmatured (SPLIT-9); Title and Summary are free text (SEL-12); the publisher's page is gone, so a build should start from ClinicalTrials.gov or AACT instead (PROV-8, PROV-11). The closest precedent `covid_trials` went to `No`; treat like cases alike unless a real termination task is built.
- Priority: gap 0 (medical and temporal not thin), use case 0 (none named), source 0 (third-party extract, the publisher's page is dead), shape + (about 13K rows, mixed types), risk - (no target, unmatured status, text columns).

A Kaggle 'overview of clinical trials' table (aggregated research-landscape data), already tagged 2nd Tier / Scientific Discovery and Non-IID (Temporal). It reads as a descriptive registry/overview table rather than a dataset built around a clear predictive target, which risks falling into the non-predictive/scientific-discovery exclusion. It could be reframed as a predictive task (e.g. predicting trial outcome/completion) if a sensible target and adequate clean rows exist. A human must define whether a real predictive target is available, the row count after cleaning, and confirm the temporal split regime.
