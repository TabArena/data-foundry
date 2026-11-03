---
unique_name: vitaldb_postoperative_icu_admission
name: VitalDB, a high-fidelity multi-parameter vital signs database in surgical patients (clinical information table)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
original_source: Other
year: '2022'
domain: medical & healthcare
problem_type: Binary Classification
source_links:
- https://doi.org/10.1038/s41597-022-01411-5
- https://physionet.org/content/vitaldb/
- https://vitaldb.net/dataset/
- https://api.vitaldb.net/cases
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: 6,388 non-cardiac operations at Seoul National University Hospital with 74 clinical columns (pre-op labs, operation, anaesthesia, intra-op fluids and drugs) and the ICU days of the stay; postoperative ICU admission is a target we define, 18.6% positive in a preview, and the operation type sets much of it.
- Source: Lee, Jung et al., "VitalDB, a high-fidelity multi-parameter vital signs database in surgical patients", Scientific Data 9:279 (2022, doi 10.1038/s41597-022-01411-5); PhysioNet v1.0.0 and vitaldb.net, CC BY 4.0 ("Anyone can access the files"). As published (PhysioNet page): "6,388 cases were included from 7,051 eligible cases", non-cardiac general, thoracic, urological and gynaecological surgery, Aug 2016 to Jun 2017; clinical information (the page gives 72 to 74 parameters), waveform and numeric tracks and lab results per case. Preview of the clinical table (https://api.vitaldb.net/cases, first 2,363 cases): 74 columns, among them `subjectid`, time offsets (`adm`, `dis`, `opstart`, `opend`, ...), `icu_days`, `death_inhosp`, demographics, `asa`, `emop`, `department`, `optype`, `dx`, `opname`, `approach`, `ane_type`, pre-op history, ECG, PFT and labs, airway and line fields, and 15 `intraop_*` totals (blood loss, urine, transfusions, fluids, drugs).
- Use case: not in the source (its intended uses are ML on biosignals, signal processing and outcome studies); an anaesthesiologist or bed manager deciding at the end of surgery between ICU and ward is our reading, fit approximate: `icu_days` counts ICU days of the stay, so planned admissions and later ICU stays are mixed in. In the preview the ICU share is 18.6% (439 of 2,363): 51% for major resections, 45% for transplantations, 0% for breast surgery; in-hospital death 0.7%. Regime grouped by `subjectid` (39 repeat patients in the preview) or IID; time exists only as offsets.
- Siblings and duplicates: `post_operative_patient` (Lennart, `No`, `Too Small`, 90 rows) and `postoperative_patient_data` (`No`, `Duplicate`); `inspire_surgical_case_duration` (unscreened; INSPIRE, the same hospital, about 130,000 operations 2011-2020, credentialed; its target is case duration, but its operations may include VitalDB's cases, so check the overlap before both enter, PROV-4); `mover_perioperative_outcomes` (unscreened; UC Irvine, 64,354 EPIC surgeries with postoperative ICU transfer as a candidate target: another source, the same target); `core_temperature_surgical_infection` (another task). External collections: none of our vocabulary.
- Better data: found as better data for `post_operative_patient`; no further search this round (INSPIRE and MOVER, larger, are recorded above).
- Papers and pages: the PhysioNet page (read); the Sci Data paper (redirected to a login, not read); the vitaldb.net parameter list (not read); the cases API (previewed).
- Metric: none found (PhysioNet page, vitaldb.net overview; the data paper defines no prediction task), so the fallback `roc_auc` (MET-8). Inputs: none.
- Risks for /add-dataset: define the target from `icu_days` at the end of surgery and drop the outcomes (`icu_days`, `death_inhosp`, `dis` and other offsets after the operation, LEAK); ICU admissions planned by protocol (the operation type nearly decides some groups; USE-3, USE-8); repeat patients (SPLIT-29); possible overlap with INSPIRE (PROV-4). The INSPIRE link that sat in `source_links` moved to this block: it is another dataset's link.
- Priority: gap 0 (medical, binary not thin), use case 0 (the decision is ours), source + (a data paper, PhysioNet, a documented API), shape + (6,388 cases, 74 mixed columns), risk - (a target to define from ICU days with planned admissions, and larger sources for the same target).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `post_operative_patient`.
- as published: 6,388 non-cardiac surgical cases (one row per case), Aug 2016 - Jun 2017; clinical_data.csv with about 74 columns: demographics, ASA, emergency flag, department, operation and approach, anaesthesia ...; target: postoperative ICU admission (icu_days > 0) as the destination after surgery; in-hospital death also available; access: open.
- Why: same decision as post_operative_patient (where to send the patient after the recovery area: ICU, floor, home), with features of the same kind (vital signs, temperature, blood pressure, oxygen saturation, stability during and after the operation) known at the end of surgery
- Adds: 70 times the patients (6,388 vs 90), recent (2016-2017), a real hospital record instead of a hand-coded table of 8 discretised attributes, open access; INSPIRE (credentialed) scales the same task to about 130,000 operations with ICU admission within 24 hours recorded explicitly. Caveat for screening: some ICU stays ...
