---
unique_name: eicu_collaborative_research_database
name: eICU Collaborative Research Database
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
decision_markers:
- Needs extensive data wrangling
- No Good Target  / Scientific Discovery
tags:
- 2nd Tier / Scientfic Discovery
- '?'
- AI-Filled (Verify)
collections:
- New (BeyondArena)
domain: medical & healthcare
required_split:
- Grouped (NON-IID)
problem_type: TBD
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://physionet.org/content/eicu-crd/2.0/
source_row: 841
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

The eICU Collaborative Research Database (PhysioNet) is a large multi-center ICU relational database with many tables (patients, vitals, labs, diagnoses), not a single curated predictive table. Real tabular tasks (e.g., ICU mortality, length-of-stay) can be derived from it, but doing so requires substantial wrangling, cohort definition, and a patient-grouped split, and it is credentialed-access (data-use agreement). It is already flagged 2nd Tier / '?'. A human must decide on a specific extracted task and target, handle the credentialing/access, and define the join and grouping before this could be promoted.
