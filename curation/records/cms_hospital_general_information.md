---
unique_name: cms_hospital_general_information
name: 'CMS Provider Data Catalog: Hospital General Information (current release)'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- No Good Target (yet)
tags:
- AI-Filled (Verify)
original_source: GOV Website
domain: medical & healthcare
original_data_state: One Table
source_links:
- https://data.cms.gov/provider-data/dataset/xubh-q36u
- https://data.cms.gov/provider-data/api/1/metastore/schemas/dataset/items/xubh-q36u
- https://data.cms.gov/provider-data/archived-data/hospitals
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: the current CMS release of the table `hospital_ratings` mirrors as a 2019 file. Its only target is CMS's own overall star rating, a composite of the measures the table summarises, so the precedent's call holds.
- Source: Centers for Medicare & Medicaid Services, Provider Data Catalog, "Hospital General Information" (xubh-q36u), read through the API on 2026-10-31. Its description: "A list of all hospitals that have been registered with Medicare. The list includes addresses, phone numbers, hospital type, and overall hospital rating". The metastore gives issued 2025-01-08, modified 2026-07-22, released 2026-08-13. As published: 5,419 rows x 38 columns: facility id, name, address, city, state, ZIP, county, phone, hospital type, ownership, emergency services, birthing-friendly designation, and `hospital_overall_rating` (1-5 or not available) with a footnote. For mortality, safety and readmission it gives the number of measures and the counts better, no different and worse than the nation; for patient experience and timely and effective care only the measure counts.
- Use case: none stated. CMS computes the star rating and publishes it for comparison, so a prediction of it serves no named decision; a curated use would be estimating the rating of a hospital CMS does not rate yet. Fit approximate at best. Regime IID for one snapshot, or a yearly panel grouped by hospital (next year's rating from this year's measures) if the archive holds yearly files; the archive page is rendered by script and was not read.
- Siblings and duplicates: `hospital_ratings` (`TBD -> 2nd Tier`, priority 2, `No Good Target (yet)`) is the Kaggle mirror of the 2019 file of the same CMS table. This record is a newer release of that source (PROV-6), so at most one of the two enters, and the curator decides which. External collections: none found.
- Better data: found as better data for `hospital_ratings` (the data-scouting run of 2026-10-30/31); no further search.
- Papers and pages: the catalog page and its metastore entry. CMS's star-rating methodology (measure scores standardized and averaged into group scores, then clustered into stars) was not re-read here.
- Metric: none found (a published list, no task), so the fallback: `log_loss` for the five stars as classes, or `rmse` as an ordinal regression, decided at /add-dataset (MET-1, MET-8). Inputs none.
- Risks for /add-dataset: the target is CMS's composite of the same measure groups whose counts ship: SEL-5 if the counts reproduce it, a strong leak-like signal otherwise (LEAK). Hospitals without a rating drop out (count not checked). Name, address and phone are identifiers. The rating method changed over the years, so a panel across a change mixes definitions.
- Priority: gap 0 (medical not thin), use case 0 (none stated), source + (CMS catalog with a data dictionary), shape + (5,419 hospitals, mixed types), risk - (composite target, no decision).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `hospital_ratings`.
- as published: one row per Medicare-registered hospital: 5,419 rows x 38 columns (type, ownership, emergency services, birthing-friendly, overall rating, per measure group the counts of measures better / no ...; target: hospital overall star rating (1-5); access: open.
- Why: The record's own source in a newer release. The record's 2019 Kaggle mirror notes that a newer one exists on data.cms.gov
- Adds: 7 years newer, a different column layout (measure counts instead of above/below flags), and 5,419 hospitals. The archive has the yearly snapshots, so a panel task (next year's rating from this year's measures) would avoid the deterministic-composite problem the record names. The target issue stays for a single snapshot
- A newer release of the same source as the record(s) named above (PROV-6): the curator decides which one enters.
