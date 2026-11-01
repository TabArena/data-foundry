---
unique_name: nfip_redacted_claims
name: NFIP Redacted Claims (v3), FEMA OpenFEMA
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
original_source: GOV Website
domain: insurance
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.fema.gov/openfema-data-page/nfip-redacted-claims-v3
- https://www.fema.gov/openfema-data-page/fima-nfip-redacted-claims-v2
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: FEMA's open NFIP claim transactions (2,725,989 rows, refreshed monthly) with payments, damage amounts and policy, building and flood-zone attributes, a claim-severity task in the thin insurance domain; FEMA poses no task, many columns are post-outcome, and the paid amount has zeros and negatives.
- Source: FEMA OpenFEMA, "NFIP Redacted Claims (v3)" (https://www.fema.gov/openfema-data-page/nfip-redacted-claims-v3; the v2 page linked), derived from the NFIP system of record and redacted to protect the policyholders' personal information (page summary); last refresh 2026-09-09, monthly; the first release year is not on the page. As published: one row per claim transaction, with dateOfLoss, floodEvent and eventDesignationNumber, ratedFloodZone and floodZoneCurrent, elevation fields (base flood elevation, lowest floor, elevation difference, elevated building, obstruction type), occupancy, coverage amounts and deductible codes, waterDepth (inches, "there are instances where measurements were provided in feet") and exterior and interior depth, amountPaidOnBuildingClaim (where "a negative amount may appear" when an uncashed check is reissued), buildingDamageAmount ("The actual cash value amount of damage to a main property in whole dollars"), net payments, ICC, payment and recovery dates and non-payment reasons; latitude and longitude rounded to one decimal.
- Use case: an NFIP adjuster or claims reserving team estimates the building payment when a flood claim is opened, to set the reserve and route the claim; FEMA publishes for transparency and names no decision; fit approximate (ours); regime grouped by flood event (a model serves the next event) or temporal by dateOfLoss (SPLIT-3, to decide).
- Siblings and duplicates: none for NFIP (grep: nfip, flood insurance, openfema); `fio_homeowners_insurance_zip_2018_2022` (`TBD -> 2nd Tier`, ZIP-level aggregates, another unit); `allstate_claims_severity` (`Yes`), for which the run also named this data, "another line of business, so the same task only in kind" (the run's already_recorded list). External collections: none found.
- Better data: no new search; found through the gap scout for insurance (also named as better data for `allstate_claims_severity`, the same task only in kind).
- Papers and pages: the OpenFEMA data page and its field list (read); papers on NFIP claims not read.
- Metric: none found (the OpenFEMA page; no competition or paper read), so the fallback `rmse` on the paid amount, its modelling scale (log1p) to settle under MET-3 (MET-1, MET-8). Inputs: none.
- Risks for /add-dataset: payment, net-payment, recovery, ICC, non-payment-reason and payment-date columns are post-outcome and go (LEAK); buildingDamageAmount is the adjuster's assessment, either the target or a leak (USE-5: the actor acts on the payment); water depth is read by the adjuster after the flood, known at the prediction point only if the reserve is set after inspection (the prediction point to settle); zero and negative payments (claims closed without payment, reissued checks) to filter or model in two parts; v3 replaces v2 (PROV-6) and the monthly refresh needs a pinned snapshot.
- Priority: gap + (insurance is thin), use case 0 (FEMA names no decision), source + (a federal agency with a field dictionary), shape + (2.7 million claims, mixed types, events and dates), risk - (many post-outcome columns; the target to define).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the gap scout for insurance.
- as published: 2,725,989 claim transactions, about 98 fields (building and contents payments and damage amounts, coverage, deductibles, flood zone, elevation, occupancy, foundation, floors, construction dates, ...; target: amountPaidOnBuildingClaim (or buildingDamageAmount; contents as a second framing); access: open.
- Why: strong source (a federal agency, documented data dictionary), open, very large, temporal by date of loss and grouped by flood event, mixed numeric, categorical and date features; claim severity on property, a peril the benchmark lacks
- Adds: a property-flood severity task from a public agency, far larger and newer than any insurance set we hold, with natural temporal and event-grouped splits. Risks for screening: payment, recovery, net-payment, ICC and non-payment-reason columns are post-outcome and must go; water depth and duration come from the ...
