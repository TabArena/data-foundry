---
unique_name: therlid_infrared_vs_contact_temperature
name: 'TherLiD: A Thermometry Linked Dataset (infrared temporal readings paired with contact reference temperatures)'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- Non-IID (Grouped)
- AI-Filled (Verify)
original_source: Website
year: '2025'
domain: medical & healthcare
required_split:
- Grouped (NON-IID)
original_data_state: One Table
source_links:
- https://doi.org/10.13026/tkww-8b64
- https://physionet.org/content/therlid/1.0.0/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: 13,251 ICU pairs of an infrared temporal-artery reading and a contact reference temperature (oral, rectal or core) within one hour, with demographics, labs and vitals, published on PhysioNet to study infrared thermometry bias; a measurement-correction task like `infrared_thermography_temperature`, on sick patients of many hospitals, with post-reading columns to drop.
- Source: TherLiD v1.0.0, PhysioNet, 2025-01-21 (Tan, Martins, Matos, Sousa Gonçalves, Ohnuma, dos Santos Cardoso, Celi, Krishnamoorthy, Lane, Wong; doi 10.13026/tkww-8b64; code on GitHub, joamats/therlid; credentialed access with CITI training and the PhysioNet Credentialed Health Data Use Agreement 1.5.0, no criterion, EV-4). As published: one CSV of 13,251 pairs of 8,511 patients, a temporal and a reference reading "within a 1-hour window" in either order, 30-45 C: MIMIC-IV v2.2 1,552 pairs, eICU-CRD v2.0 (2014-2015) 7,307, eICU-CRD-2 (2019-2022) 4,392; columns: patient, hospital and ICU-stay ids, source, the two temperatures with time and site, time differences, vitals, blood counts, coagulation, chemistry, liver, blood gas, SOFA before and after the reading, day-one SOFA, age (capped at 90), sex, weight, height, BMI, race and ethnicity, Charlson index, in-hospital mortality, length of stay; dates shifted. Purpose: "provide a standardized dataset with paired temperatures", for retrospective studies, disparities research and machine-learning models; motivated by Bhavani et al. (JAMA 2022), where temporal thermometers missed fever more often in Black patients.
- Use case: a nurse reads a temporal-artery thermometer and decides whether the patient has a fever or hypothermia; a model corrects the reading to the reference from what is charted then. The page names the purpose, no actor; fit approximate. Regime grouped by hospital (the hospital id ships; eICU spans many hospitals), patients repeat (8,511 for 13,251 pairs).
- Siblings and duplicates: `infrared_thermography_temperature` (`Disagreement`, DF: Yes; a thermal camera's facial temperatures of 1,001 mostly young volunteers: another source and design, no duplicate); `pulse_oximetry_sao2_correction` (`TBD -> Yes`, priority 2; BOLD, the same group's linked-pair design for SpO2); built from `mimic_iv`, `eicu_collaborative_research_database` and `eicu_crd_2020_2021` as a task of its own (PROV-7). External collections: none found.
- Better data: found as better data for `infrared_thermography_temperature`.
- Papers and pages: the PhysioNet page; the GitHub README (the manuscript is not linked); Bhavani et al. 2022.
- Metric: none found (PhysioNet page, GitHub README; the example notebook not read), so the fallback `rmse` on the reference temperature (MET-8); the sibling declares `rmse` from its source.
- Risks for /add-dataset: SOFA after the reading, in-hospital mortality and length of stay come after the prediction point (LEAK-10); the reference may precede the infrared reading, so set the prediction point at the infrared reading and decide on such pairs (USE-3); the reference site varies (a feature, or one site as the target, USE-5); race and ethnicity as features (the source's own question; keep with a note); with one infrared number as the main input the task may be close to the reading itself or very noisy (TP-4 probe).
- Priority: gap 0 (medical, regression, grouped not thin), use case 0 (purpose named, no actor), source + (PhysioNet, documented columns, code), shape + (13,251 pairs, mixed features, hospital groups), risk - (post-reading columns, mixed reference sites).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `infrared_thermography_temperature`.
- as published: 13,251 pairs of 8,511 patients: an infrared temporal reading and a contact reference (oral, rectal or core) within 1 hour, 30-45 C. Sources: eICU-CRD v2.0 (2014-2015, 7,307 pairs), eICU-CRD-2 ...; target: The contact reference temperature (or fever or hypothermia by it), given the infrared temporal reading; access: registration.
- Why: The record predicts oral temperature from facial infrared readings plus demographics to screen for fever. This predicts the contact-measured body temperature from a non-contact infrared reading plus demographics, so it is the same quantity and the same decision. Differences: one handheld temporal-artery reading ...
- Adds: 13 times the record's 1,001 people, with real fevers and hypothermia in sick patients instead of mostly healthy students aged 18-25 (the record's Selection Bias), race and ethnicity for the known infrared bias, and 2008-2022.
