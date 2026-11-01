---
unique_name: detroit_blight_ticket_compliance
name: 'Detroit Blight Tickets: compliance with property-maintenance fines'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
original_source: GOV Website
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://services2.arcgis.com/qvkbeam7Wirps6zC/arcgis/rest/services/blight_tickets/FeatureServer/0
- https://opengis.detroitmi.gov/opengis/rest/services/DAH/blight_violation_citations/FeatureServer/0
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: 911,637 blight tickets of the City of Detroit's Department of Administrative Hearings, with ordinance, agency, dates, fines and payment status, for predicting whether a ticket found responsible is paid; large, temporal and from the first publisher, but the use case is remembered from a course and the outcome columns must go.
- Source: City of Detroit Open Data, ArcGIS layer "Blight Tickets" (services2.arcgis.com/qvkbeam7Wirps6zC/.../blight_tickets/FeatureServer/0), updated continuously (the year waits for the snapshot we pin, PROV-9): "Blight Tickets are issued by city inspectors, police officers, and other city officials with the power to investigate and cite code violations. Blight Tickets are adjudicated as civil cases by the Department of Administrative Hearings (DAH)"; "This dataset largely models the Blight Violation Case History system". Preview through the layer API (2026-10-31): 911,637 tickets; 48 fields (ticket id and number, address, ordinance law and description, disposition, agency, inspector name, issue, hearing, judgment and payment dates, fine, admin, state and late fees, discount, clean-up cost, judgment, payment and balance amounts, payment status, collection status, owner id, name and address, neighbourhood, council district, zip, parcel, coordinates); payment status: no payment applied 364,700, no payment due 319,171, paid in full 219,611, partial payment 7,725, empty 430; 236,361 "In Collections". The second link (opengis.detroitmi.gov) is an older layer (629,962 tickets per the scout).
- Use case: the city, once a ticket is found responsible, decides which ones need costly follow-up enforcement and collection; the framing comes from the University of Michigan course assignment and the Michigan Data Science Team ("enforcing unpaid blight fines is a costly and tedious process"), quoted by the scout from memory and not read here, so the use case is ours until checked. Fit approximate. Regime temporal (tickets since 2005, by issue date).
- Siblings and duplicates: none in `curation/records/` (searched Detroit, blight); the course's train and test files (Kaggle copies exist) would be a cut of this source (PROV-6) and have no record. External collections: none found.
- Better data: from the gap scout for social science; no further search this round.
- Papers and pages: the layer's description and field list; the course and MDST pages were not read.
- Metric: none found in a source read (the layer description; the course assignment, which scored AUC as remembered, was not read), so the fallback `roc_auc` (MET-1, MET-8); inputs none.
- Risks for /add-dataset: the label among tickets found responsible (disposition), the "no payment due" rows out; payment date and amount, balance, collection status, judgment amount, late fee and `ticket_updated_at` are the outcome or come after it (LEAK); hearing and judgment dates come after the issue date (prediction point at issue or at judgment, USE-3); recent tickets have not had time to be paid (SPLIT-9, SPLIT-10); owner and inspector names and owner addresses are personal data (drop; a derived owner-outside-Detroit flag only if the curator agrees); out-of-range dates in the layer (the scout: 1824 and 8535).
- Priority: gap + (social science thin), use case 0 (remembered, not read), source + (the city's layer with a description), shape + (911,637 tickets, mixed types, temporal), risk - (outcome columns, label maturity, personal data).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the gap scout for social science.
- as published: 911,564 tickets (ArcGIS Hub catalog count, 2026-10-30) x 48 columns: ordinance, issuing agency, inspector, issue/hearing/judgment dates, fine, fee and discount amounts, disposition, payment status, ...; target: Ticket paid in full (payment_status) among tickets found responsible; access: open.
- Why: Real municipal administrative data on a recurring enforcement decision, large and temporal, from the first publisher.
- Adds: Housing and public services; temporal regime; mixed types (ordinance codes, agencies, amounts, owner in or out of Detroit, location). Risks: payment date and amount, balance, collection status, judgment and late fee are the outcome (drop); owner names and addresses are personal data (drop); out-of-range dates in the ...
