---
unique_name: nhtsa_crss_crash_severity
name: NHTSA Crash Report Sampling System (CRSS), crash injury severity
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
decision_markers:
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
collections:
- New (BeyondArena)
original_source: GOV Website
year: '2016'
domain: social science
required_split:
- Temporal (NON-IID)
problem_type: Multiclass Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.nhtsa.gov/crash-data-systems/crash-report-sampling-system
- https://crashstats.nhtsa.dot.gov/Api/Public/Publication/812688
- https://www.nhtsa.gov/file-downloads?p=nhtsa/downloads/CRSS/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

NHTSA's nationally representative probability sample of police crash reports, in place since data year 2016 when it replaced NASS-GES; target sample "about 50,000" police accident reports a year drawn from the ~7 million issued annually (NHTSA, "Crash Report Sampling System: Design Overview, Analytic Guidance", DOT HS 812 688; 2016 file: 47,515 eligible PCRs). Annual releases as ACCIDENT / VEHICLE / PERSON tables (SAS + CSV) with a crash-level maximum injury severity (KABCO) and per-person injury severity; US government work, public domain. Sibling `fars` (fatal-crash census, OpenML/PMLB copy of unknown vintage) is a different NHTSA system; CRSS covers all severities, which is what makes it a severity task.

To decide: crash-level target (MAX_SEV, 5 imbalanced classes, or injury vs none) from crash / vehicle / driver descriptors known from the scene report; drop outcome fields (HARM_EV after the fact, tow, EMS). The file carries survey weights (WEIGHT) and a stratified design; an unweighted classification is a different task from NHTSA's estimates, same caveat as `higgsml_2014`. Yearly files -> temporal split, mind coding changes across years. NHTSA pages returned 403 here, so the download layout was not checked. Data not inspected.

Opened 2026-09-23 as the injury-severity counterpart to `us_accidents` (rejected: its Severity is a traffic-delay code). Police crash reports carry the injury outcome the first-responder / crash-severity use case needs; the target is the standard one in road-safety research, unlike the gender target that sank `road_safety`.

## Reference

National Center for Statistics and Analysis (2018). Crash Report Sampling System: Design Overview, Analytic Guidance, and FAQs (Report No. DOT HS 812 688). NHTSA.
