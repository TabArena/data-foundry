---
unique_name: hbdc_audiogram_air_bone_gap
name: 'Hearing Big Data Center (HBDC) pure-tone audiograms from five Korean tertiary hospitals: air-bone gap from air-conduction thresholds'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- Non-IID (Grouped)
- AI-Filled (Verify)
original_source: Other
domain: medical & healthcare
required_split:
- Grouped (NON-IID)
source_links:
- https://doi.org/10.3390/jcm14186549
- https://pmc.ncbi.nlm.nih.gov/articles/PMC12470468/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: 60,718 pure-tone audiograms of 26,417 patients of five Korean tertiary hospitals, published to predict bone-conduction thresholds and the air-bone gap from the air-conduction audiogram, age and sex; a real measurement-substitution task, but the paper's counts disagree, missing bone thresholds were filled with the air thresholds, and the data is on request only.
- Source: Yoon, Lee, Kim, You, Kwak and Seo, "AI-Based Prediction of Bone Conduction Thresholds Using Air Conduction Audiometry Data", J Clin Med 14(18):6549, 2025 (doi 10.3390/jcm14186549, PMC12470468), on the Hearing Big Data Center (HBDC) of five tertiary hospitals in the Republic of Korea; collection years not stated; `year` left empty (earlier HBDC publications not checked). As published: inputs air-conduction thresholds 0.25-8 kHz, age and sex; outputs bone-conduction thresholds 0.25-4 kHz and air-bone-gap status at 10 dB and 15 dB; 60,718 records of 26,417 people (abstract, Methods), 70,937 records in the 8:2 split (Table 1, Section 2.3) and 72,864 values of 12,144 patients (Table 2), not reconciled. Access: "Data are not publicly available due to patient privacy protection and institutional review board (IRB) restrictions but may be available from the corresponding author upon reasonable request and with permission from the respective institutions" (Data Availability Statement); no criterion (EV-4).
- Use case: an audiologist or a tele-audiology service with only an air-conduction audiogram decides whether bone-conduction testing or an ENT referral for a conductive component is needed. The paper names the setting ("clinical audiology and telemedicine, particularly for remote screening and diagnosis", abstract, Conclusions), not the actor; fit approximate. Regime grouped by person (several audiograms per person; the paper does not say its split was by person), a split by hospital possible.
- Siblings and duplicates: `audiology_diagnosis` (`Yes`, the 1992 UCI teaching collection of 195 cases; another source and target, no duplicate); no other audiogram record (grep audiogram, air-bone, audiometr). External collections: none found.
- Better data: found as better data for `audiology_diagnosis`.
- Papers and pages: the J Clin Med paper (abstract via Crossref, text via PMC).
- Metric: the paper reports accuracy, sensitivity, precision and F1 for the air-bone gap and accuracy within 5 and 10 dB for the thresholds, side by side, none ranked (MET-5), so the fallback: `roc_auc` for the gap, `rmse` for a threshold.
- Risks for /add-dataset: the paper replaced missing bone-conduction values with the air-conduction value (Methods), which sets the gap to zero on those rows: rebuild the label from the raw thresholds or drop the rows (PROV-13, USE-7); the three record counts disagree; SMOTE in the paper (never ours); whether HBDC data can be obtained and shipped is open.
- Priority: gap 0, use case 0 (setting named, no actor), source + (a peer-reviewed paper, five named hospitals), shape + (60,718 audiograms, person groups), risk - (filled labels, inconsistent counts).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `audiology_diagnosis`.
- as published: 60,718 pure-tone audiometry records of 26,417 people after removing incomplete records (the paper also reports 70,937 records in its modelling split; the counts are inconsistent). Columns: ...; target: Air-bone gap status (a conductive component, >=10 or >=15 dB criteria) or the bone-conduction thresholds, predicted from air-conduction thresholds, age and sex; access: request.
- Why: The record's target is normal / sensorineural / conductive_or_mixed, and the air-bone gap is the measurement that defines the conductive part. Normal against loss comes from the air thresholds, so the same distinction is measured directly here, from audiometric features of the same kind.
- Adds: About 300 times the record's 195 cases, from a recent clinical caseload instead of a 1992 teaching collection, which addresses the record's Tiny Data, Outdated and Selection Bias. Caveats: not public ('Data are not publicly available due to patient privacy protection'), access only on request to the corresponding ...
