---
unique_name: kumc_inpatient_aki_prediction
name: Multi-perspective AKI prediction in general hospital populations (KUMC EMR)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
original_source: Other
year: '2018'
domain: medical & healthcare
problem_type: Binary Classification
source_links:
- https://doi.org/10.5061/dryad.qc90qb4
- https://doi.org/10.1093/jamiaopen/ooy043
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: 76,957 adult inpatient encounters at the University of Kansas Health System (2007-2016) with hospital-acquired AKI by the KDIGO creatinine criteria (7,259 encounters), from a JAMIA Open paper that frames prediction at admission as a clinical scenario; open under CC0, but the layout of the scrubbed file, and whether it keeps the time stamps the admission cut needs, were not seen.
- Source: He, Hu, Zhang, Wu, Waitman and Liu, "Multi-perspective predictive modeling for acute kidney injury in general hospital populations using electronic medical records", JAMIA Open (online 2018, issue 2019; https://doi.org/10.1093/jamiaopen/ooy043; full text read via Europe PMC, PMC6447093). Data: Dryad, "Data from: Multi-perspective predictive modeling ..." (https://doi.org/10.5061/dryad.qc90qb4, 2018-11-16, CC0 1.0 per the Dryad API): AKI_Prediction_Scrubbed_EMR.zip (8.1 MB) and a README (not readable: the Dryad API asks for a token). As published (Methods): inpatients over 18 with a stay of at least 2 days, excluding stays with fewer than 2 creatinine values or with eGFR below 60 or creatinine above 1.3 mg/dL within 24 hours of admission; "The final analysis cohort consisted of 76 957 encounters"; AKI in 7,259; 1,917 attributes (demographics, vitals, labs, admission diagnosis, comorbidities, medications before and during the stay, history), labs and vitals coded "present and normal", "present and abnormal" or "unknown"; "SCr and eGFR were not included as predictive variables".
- Use case: the paper's Perspective #2, "This aligns with a clinical application scenario in which clinicians can use the models to make AKI risk prediction for everyone at admission and make subsequent treatment decisions": the admitting team, at admission, decides on preventive care. Fit direct if the file allows the admission cut. Regime: temporal by admission if the file keeps a date (2007-2016), otherwise grouped by patient (repeat encounters); to settle (SPLIT-7, USE-10).
- Siblings and duplicates: `elaia1_aki_progression` (`TBD -> Yes`, priority 3; AKI progression after detection in an alert trial, another task and source); `eicu_collaborative_research_database`, `amsterdamumcdb` (ICU databases, other sources). No duplicate (grep: kumc, kansas, dryad.qc90qb4, HERON). External collections: none found.
- Better data: from the curator's Zotero collection (item 155, Dryad); no further search this round.
- Papers and pages: the paper's four perspectives (one day before onset; at admission for the stay; at admission for 1 to 30 days; daily during the stay); the Dryad page.
- Metric: the paper reports AUC, sensitivity, specificity, precision and F-measure side by side (Methods: "Area under the receiver operating characteristic (ROC) curve (AUC), sensitivity, specificity, precision, and F-measure were reported"), with the threshold picked for the best F-measure; several metrics and no fixed threshold, so the fallback `roc_auc` (MET-5, MET-6, MET-8). Inputs: none.
- Risks for /add-dataset: the scrubbed format is unknown (one wide table per perspective, or long time-stamped tables) and decides whether Perspective #2 can be rebuilt (`Needs extensive data wrangling` possible); medications, vitals and labs during the stay must be cut at admission (LEAK-10, USE-3); repeat encounters of one patient (SPLIT-29); the labs are pre-coded by reference ranges, a fixed rule and no fit on the data.
- Priority: gap 0 (medical binary tasks are well covered), use case + (the paper names the actor, the moment and the decision), source + (a peer-reviewed paper and a CC0 deposit), shape + (76,957 encounters, 1,917 coded attributes), risk - (file layout unknown; the admission cut to rebuild).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 155: "Dryad | Publish and preserve your data".
- as published: 76,957 inpatient encounters at one tertiary academic hospital, November 2007 to December 2016; an 8 MB zip (AKI_Prediction_Scrubbed_EMR) with a readme; file layout not previewed; target: onset of acute kidney injury during the stay, as defined in the paper (next-day and fixed-lead-time settings); access: open.
- Why: A public CC0 EMR extract for a general inpatient population, with the prediction settings (at admission, fixed lead time) spelled out in the paper.
- Adds: An inpatient deterioration task with public data. The snapshot design (at admission or fixed lead time) needs picking, and the scrubbed EMR format needs a look.
