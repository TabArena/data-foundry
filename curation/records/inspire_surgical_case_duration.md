---
unique_name: inspire_surgical_case_duration
name: 'INSPIRE perioperative dataset (Seoul National University Hospital): surgical case duration'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
original_source: Other
year: '2023'
domain: medical & healthcare
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.13026/1eay-yc85
- https://doi.org/10.1038/s41597-024-03517-4
- https://physionet.org/content/inspire/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: INSPIRE, about 130,000 operations at Seoul National University Hospital (2011-2020, a random half of the patients) in a credentialed PhysioNet database; case duration (`opend_time` minus `opstart_time`) is a target we define for operating-room scheduling. Large and documented, but the source names no duration task, calendar time was removed, and some of VitalDB's operations are in it too.
- Source: Lim, Lee et al., "INSPIRE, a publicly available research dataset for perioperative medicine", Scientific Data 11:655 (2024, https://doi.org/10.1038/s41597-024-03517-4; full text read via Europe PMC, PMC11192876); PhysioNet project (https://doi.org/10.13026/1eay-yc85), first released as v0.1 in September 2023, now v1.4.2, credentialed access under the Korea Credentialed Health Data License and DUA. As published: Table 1 "INSPIRE dataset (N = 131,109)"; Methods: "we excluded random 50% of the patients to populate the publicly released dataset"; six tables (operations, diagnosis, vitals, ward_vitals, labs, medications) joined on `subject_id`, `hadm_id`, `op_id`; the operations table holds demographics, ASA class, department, `opstart_time`, `opend_time`, `anstart_time`, `aneend_time`, `icd10_pcs` (leading characters of the procedure code), `antype`, bypass variables, ICU in and out within 24 hours, and mortality. "All times were converted to times (minutes) relative to the time zero" (each subject's first admission for an operation), so no calendar date survives.
- Use case: an operating-room scheduler, when a case is booked, predicts its duration to plan the room's day. Not in this source, whose stated aims are complication models and external validation; the Zotero paper (Barrowcliff, Lovegrove and Kunz, "Automated Machine Learning Approaches for Surgery Duration Prediction in Orthopaedics", MIE 2026, https://doi.org/10.3233/SHTI260121) states it on 94,502 private elective orthopaedic procedures. Fit approximate: no surgeon or team id and no booked duration, and the columns known at booking (diagnoses, labs, medications with relative times) must be cut by time. Regime: temporal by nature (practice drifts over ten years), but without calendar time only a split grouped by `subject_id` can be built (SPLIT-7, SPLIT-8: to settle).
- Siblings and duplicates: `vitaldb_postoperative_icu_admission` (`TBD -> Yes`, priority 2; VitalDB, the same hospital, 6,388 cases of 2016-2017): the INSPIRE paper checks lab values "of which operations were included in both datasets", so part of VitalDB's operations are also in INSPIRE (a random half of the patients was released); another target on partly the same operations (PROV-4 to settle if both enter). `mover_perioperative_outcomes` (unscreened; UC Irvine, its own source); `core_temperature_surgical_infection` (another task). External collections: none found.
- Better data: from the curator's Zotero collection (item 204, the MIE 2026 paper, whose NHS data is not public); no further search this round.
- Papers and pages: the Sci Data paper (a 30-day mortality model as its validation study); the PhysioNet page (versions 0.1 to 1.4.2); MOVER (https://doi.org/10.24432/C5VS5G), VitalDB (https://doi.org/10.1038/s41597-022-01411-5) and the MIE 2026 paper were moved here from the source links, as related work rather than this dataset's links (PROV-12).
- Metric: none found for case duration on INSPIRE (the data paper and the PhysioNet page define no duration task); the MIE 2026 paper scores MAE alone (abstract), on other data: a stand-in to weigh against the fallback `rmse` (MET-1, MET-5). Inputs: none.
- Risks for /add-dataset: credentialed download under a DUA (EV-4: no reason for a verdict, but the build needs a credentialed curator); the target is ours (operation or anaesthesia time; emergency cases, about 10% of operations, kept or dropped); keep only what is known at booking and drop intra-operative vitals, ICU times, mortality and post-operative labs and diagnoses (LEAK-10, USE-3); no calendar time for a temporal split (SPLIT-7); joins over six tables; the VitalDB overlap (PROV-4).
- Priority: gap 0 (medical regression is well covered), use case 0 (written by us for this data; the source names complication models), source + (Sci Data paper and PhysioNet documentation), shape + (131,109 operations, mixed types, patient groups), risk - (target and prediction point to define, no calendar time, VitalDB overlap).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 204: "Automated Machine Learning Approaches for Surgery Duration Prediction in Orthopaedics".
- as published: about 130,000 operations under anaesthesia (Table 1: 131,109), a 50% sample of the hospital's surgical cases, adults 18-90, 2011-2020. Six tables: operations, diagnosis, labs, medications, intra-op ...; target: operation duration in minutes (opend_time - opstart_time); alternative: anaesthesia duration; access: registration.
- Why: Real, large, peer-reviewed perioperative dataset with recorded times. Case-duration prediction is an established operational task, and its mixed-type features are known at booking. The paper's NHS data is not public.
- Adds: Better data for the task of item 204: public on credentialing, larger, ten years, all specialties (department allows an orthopaedic subset). Caveats: published as a research dataset, not for this task (the target is ours to define), and no surgeon identifier, which is the strongest predictor in hospital models. ...
