---
unique_name: hospital_ratings
name: Hospital ratings
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- No Good Target (yet)
tags:
- 2nd Tier / Scientific Discovery
- AI-Filled (Verify)
collections:
- New (BeyondArena)
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: TBD
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.kaggle.com/datasets/center-for-medicare-and-medicaid/hospital-ratings
- Medicare.gov
- '# origin named by the Kaggle card (CMS Hospital Compare, now the CMS Provider Data Catalog)'
- https://data.medicare.gov/data/hospital-compare
source_row: 835
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 2: a CMS hospital listing published for comparison, not for a predictive task; the only candidate target is CMS's own composite star rating.
- Source: CMS Hospital Compare (Medicare.gov), the `Hospital General Information` file, mirrored on Kaggle by Kaggle staff (dataset 1743, CC0, file of 2019-09-20, 2.6 MB); the card: "official datasets used on the Medicare.gov Hospital Compare Website ... These data allow you to compare the quality of care at over 4,000 Medicare-certified hospitals". As published: one table, one row per hospital ("over 4,000", count not checked), 28 columns: ID, name, address, city, state, ZIP, county, phone, hospital type, ownership, emergency services, EHR meaningful use, `Hospital overall rating` (1-5 stars) and seven measure-group national comparisons (mortality, safety, readmission, patient experience, effectiveness, timeliness, imaging; each above / same / below national average) with footnotes.
- Use case: none stated; the card's "Inspiration" is finding the best hospital for a broken leg, a lookup. A predicted star rating has no actor: CMS computes the rating from the measure-group scores itself. A curated use case (predict a hospital's rating before CMS publishes it) would be written by us; fit approximate at best. Regime IID (one row per hospital, one snapshot).
- Siblings and duplicates: none among `curation/records/` (grep for hospital rating, CMS, Hospital Compare); external collections: none found.
- Papers and pages: the Kaggle card; CMS star-rating methodology (latent variable model over the measure groups, then clustering into stars) not read here.
- Metric: none found (Kaggle card, no task, no competition), so the fallback.
- Risks for /add-dataset: the target is a composite of the same seven measure groups the table ships as comparisons (SEL-5 when the rule is deterministic, a leak otherwise, LEAK checks); name, address and phone are identifiers; the release is old (2019 snapshot), a newer one from data.cms.gov exists. The old `Data Quality Issue` marker is dropped: nothing irreversible is shown, the concern is the target (SEL-3), now `No Good Target (yet)`.
- Priority: gap 0 (medical not thin), use case 0 (none stated), source + (CMS), shape + (over 4,000 rows, mixed categorical columns); `original_data_state` says Database but the Kaggle release is one file (2.6 MB), left as set, risk - (target computed from the shipped measure groups).

Kaggle dataset of CMS/Medicare.gov hospital ratings, already tagged 2nd Tier / Scientific Discovery. Predicting a hospital star rating is plausible as a tabular task, but the overall rating is computed deterministically from the same quality-measure columns, creating a strong leakage risk, and much of the file is administrative/descriptive metadata rather than predictive features. A human must determine whether a non-leaky target and adequate clean feature set exist (and how to join the multiple measure tables). Keep in 2nd tier pending that inspection.
