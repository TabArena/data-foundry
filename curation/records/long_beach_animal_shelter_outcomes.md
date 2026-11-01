---
unique_name: long_beach_animal_shelter_outcomes
name: 'Long Beach Animal Shelter intakes and outcomes: outcome of each animal from its intake record'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
original_source: GOV Website
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://data.longbeach.gov/explore/dataset/animal-shelter-intakes-and-outcomes/
- https://vincentarelbundock.github.io/Rdatasets/doc/modeldata/cat_adoption.html
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: the City of Long Beach Animal Care Services' intake and outcome records (57,984 stays, intakes 2013-07-24 to 2026-10-29) with the outcome of each stay (rescue, adoption, euthanasia, transfer, return to owner and smaller classes); a real operational record in a domain the benchmark lacks, but the source defines no task, outcome-time fields must go and the portal is a live daily export.
- Source: City of Long Beach open-data portal, "Animal Shelter Data" (https://data.longbeach.gov/explore/dataset/animal-shelter-intakes-and-outcomes/), publisher "City of Long Beach Animal Care Services", licence CC BY, published daily and automatically (portal API, 2026-10-31); first publication date not stated. As published: one table of 29 fields, each described: `animal_id`, `kennel_identity`, `animal_name`, `animal_type`, colours, `sex`, `dob`, `intake_date`, `intake_cond`, `intake_type`, `intake_subtype`, `reason` (owner's surrender reason), `crossing`, `jurisdiction`, latitude and longitude, and outcome fields (`outcome_date`, `outcome_type`, `outcome_subtype`, `intake_duration`, `outcome_is_*`, `was_outcome_alive`). Outcome counts (API): RESCUE 13,815, ADOPTION 12,709, EUTHANASIA 11,101, TRANSFER 7,867, RETURN TO OWNER 5,822, DIED 1,441, then shelter-neuter-return, community cat, transport, return to wild habitat and smaller classes, 305 without an outcome.
- Use case: shelter staff, at intake, estimate an animal's likely outcome to plan care, foster and rescue-partner placement; written by the curation, not the source. Fit approximate. Regime temporal by intake date (outcome policies shift over the years, for example community-cat and neuter-return outcomes), with repeat stays of one `animal_id` kept together (SPLIT-13).
- Siblings and duplicates: none in the records (grep: shelter, animal center, adoption, cat_adoption); `petfinder_pet_age` (`TBD -> Yes`, priority 4) is another adoption task on listings. The Rdatasets/modeldata `cat_adoption` (2,257 cats) is a subset of this portal (a cut, not a separate source). Austin Animal Center outcomes (https://data.austintexas.gov/d/9t4d-g238) is another shelter's data for the same task, moved here from the source links (PROV-12); the Kaggle "Shelter Animal Outcomes" competition of 2016 used Austin's data (from memory, not checked in this pass). External collections: Rdatasets (modeldata).
- Better data: from the curator's Zotero collection (item 131, the Rdatasets index); no further search this round.
- Papers and pages: the portal's field descriptions; the Rdatasets page of `cat_adoption`.
- Metric: none found for this data (the portal and the Rdatasets page define no task), so the fallback `log_loss` for the outcome classes, or `roc_auc` for a live-outcome flag (MET-1, MET-8). Inputs: none.
- Risks for /add-dataset: drop the outcome-time fields (`outcome_date`, `outcome_subtype`, `intake_duration`, `outcome_is_*`, `was_outcome_alive`, `is_current_month`; LEAK-10); `animal_name` with a "*" marks a name given by the shelter, possibly after intake (check timing); stays still open (no outcome) and the newest intakes are unmatured labels (SPLIT-9, SPLIT-10); pin a dated snapshot of the live export; merge or drop rare classes and decide whether wildlife and other species stay (USE-5); euthanasia as a predicted class is a sensitive use to state (SEL-1: no objection found).
- Priority: gap + (multiclass is thin; animal welfare is a new domain), use case 0 (no actor or decision in the source), source + (a city agency's portal with field descriptions, CC BY), shape + (57,984 stays, mixed types, thirteen years of dates), risk - (outcome fields to drop, censoring, policy drift).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 131: "vincentarelbundock.github.io/Rdatasets/datasets.html".
- as published: 57,984 intake-outcome records x 29 fields, intakes 2013-07-24 to 2026-10-29; 27,490 cats, 18,287 dogs, plus birds, wildlife, rabbits and others. Fields: animal type, colours, sex, date of birth, ...; target: outcome_type (rescue 13,815, adoption 12,709, euthanasia 11,101, transfer 7,867, return to owner 5,822, died 1,441, and smaller classes), or a live vs ...; access: open.
- Why: Real operational records with a documented outcome and a decision at intake. modeldata's cat_adoption (2,257 cats) is a subset of this portal.
- Adds: A new domain (animal welfare). Caveats: drop outcome-time fields (outcome_date, intake_duration, outcome_is_*, was_outcome_alive); the portal is live, so pin a snapshot; outcome policy shifts over the years; merge or drop rare classes. A sibling source is Austin Animal Center outcomes (173,775 rows, 2013-2025, behind ...
