---
unique_name: dtc_milan_nijmegen_progression
name: 'Differentiated thyroid cancer in two European referral centres: impact of different diagnostic and therapeutic strategies (raw data)'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
tags:
- AI-Filled (Verify)
original_source: Other
year: '2025'
domain: medical & healthcare
source_links:
- https://doi.org/10.5281/zenodo.15551122
- https://doi.org/10.1530/ETJ-25-0161
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: 919 thyroid-cancer patients of two referral centres (Milan, Nijmegen), published for a two-centre comparison, not a prediction; the creators write that the raw data "cannot be made publicly avaiable as including sensitive information", yet the file sits open on Zenodo, so the data has to be requested rather than taken from the open file (an ethics question, SEL-1, not a licence one).
- Source: Ceruti, Ottevanger, De Leo, Bonenkamp, Colombo, Gotthardt, Fugazzola and Netea-Maier (University of Milan and IRCCS Istituto Auxologico Italiano; Radboud University Medical Centre), raw data on Zenodo 2025-05-30 (doi 10.5281/zenodo.15551122, one file `raw data DTC.xlsx`, no licence stated), with "Differentiated thyroid cancer in two European referral centres: impact of different diagnostic and therapeutic strategies", European Thyroid Journal 14(4):e250161, 2025 (CC BY-NC). As published: "We retrospectively included 919 patients (586 Italian, 333 Dutch)", compared by ATA risk class with dynamic risk stratification and Kaplan-Meier progression-free and disease-specific survival (abstract, via Crossref). Columns not read: I did not open the file (first risk below).
- Use case: as in `differentiated_thyroid_cancer_recurrence`: at initial staging the endocrinologist decides radioiodine, the TSH target and the follow-up schedule from the recurrence risk. The paper's aim is "To evaluate differences in the presentation, diagnostic/therapeutic approaches, and outcome" (Objective), no prediction; fit approximate. Regime IID over patients with the centre as a feature (a split by centre has two groups).
- Siblings and duplicates: `differentiated_thyroid_cancer_recurrence` (`Yes`, 383 patients of a Hamadan clinic: another source and cohort, no duplicate, PROV-4); `thyroid_discordant`, `new_thyroid`, `lymphus_cervical_lymph_node_metastasis` are other tasks. External collections: none found.
- Better data: found as better data for `differentiated_thyroid_cancer_recurrence`.
- Papers and pages: the Zenodo record; the ETJ paper (abstract only, the full text returned 403).
- Metric: none found (the abstract reports group comparisons and Kaplan-Meier curves, no prediction model), so the fallback `roc_auc` for progression by a fixed horizon (MET-8).
- Risks for /add-dataset: (1) SEL-1: the Zenodo description reads "This set of raw data cannot be made publicly avaiable as including sensitive information, but may be avaiable to intrested reserchers by sending a request" to the first author, while the record is marked open and the file downloads; use the data only with the authors' consent, and whether a public benchmark may carry it is the curator's call. (2) Response to therapy and further treatments come after the staging decision (USE-4, LEAK-10). (3) The label is progression over variable follow-up, perhaps with persistent disease counted, as in the sibling (USE-5, LEAK-24). (4) Half of the Dutch cohort is high risk against mostly low or intermediate risk in Milan, so the centre carries much of the label.
- Priority: gap 0, use case 0 (the paper names no prediction), source + (a paper, named centres), shape 0 (919 patients, two centres, columns unknown), risk - (the creators' statement against public release, the label).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `differentiated_thyroid_cancer_recurrence`.
- as published: 919 DTC patients (586 Italian, 333 Dutch), one xlsx 'raw data DTC.xlsx' (201 KB, columns not opened); the paper compares clinicopathological features, ATA risk class, first treatment and further ...; target: structural recurrence or progression during follow-up (the paper's progression-free survival event), as a binary at a fixed horizon or time-to-event; access: open.
- Why: Same target (recurrence after initial treatment of DTC) from the same kind of features known at staging (age, sex, histology, TNM, ATA risk, extent of surgery), on 2.4 times the patients, from two referral centres in two countries.
- Adds: 919 against 383 patients; two centres, so a site-grouped split is possible; newer and from Europe. Caveats: the Zenodo description says the raw data 'cannot be made publicly available as including sensitive information' and are available on request, yet the record is open access and the file downloads (HTTP 200): ...
