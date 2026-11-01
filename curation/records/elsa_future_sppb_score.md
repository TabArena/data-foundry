---
unique_name: elsa_future_sppb_score
name: English Longitudinal Study of Ageing (ELSA), future SPPB score from questionnaire and nurse-visit data
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
decision_markers:
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
original_source: Other
domain: medical & healthcare
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.elsa-project.ac.uk/accessing-elsa-data
- https://arxiv.org/abs/2508.05222
- https://doi.org/10.1109/TELFOR63250.2024.10819122
- https://g2aging.org/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: the SPPB physical-performance score (0-12) measured at a nurse visit four years later, predicted from the ELSA interview and the current nurse-visit tests of English adults aged 55-85 (7,739 person-wave pairs, waves 2 to 4 and 4 to 6); a measured future outcome from a documented national cohort, but the target has to be built across waves and the current SPPB dominates.
- Source: the English Longitudinal Study of Ageing (wave 1 in 2002, nine waves to 2019 in the paper), used through the Harmonized ELSA file (Gateway to Global Aging, g2aging.org); access by registration under the UK Data Service End User Licence (a note, EV-4). The task: Kolakowski and Ben Bader, "ML-based Short Physical Performance Battery future score prediction based on questionnaire data", TELFOR 2024 (doi 10.1109/TELFOR63250.2024.10819122; arXiv 2508.05222). As published there (Sec. III): "The dataset was constructed by taking the person's answers from waves 2 and 4 and combining them with SPPB scores calculated based on subsequent waves 4 and 6 results, respectively"; balance, walk and chair-stand tests only at the nurse visits of waves 2, 4 and 6; the 8-ft walk rescored to the 4-m thresholds; ages 55-85; 7,739 samples; 95 features (health, physical performance with the current SPPB and its parts, demographics, daily activities; marital status one-hot).
- Use case: a GP or geriatric service decides on preventive exercise or falls-prevention referral from a routine check (the paper: scores below 4 "indicate very poor physical performance and a higher mortality risk"); fit approximate (the paper names no actor; the 4-year horizon is fixed by the nurse-visit schedule). Regime grouped by person: people in both pairs appear twice, and the paper's 10-fold CV did not group them; temporal would need three windows and there are two pairs (SPLIT-14).
- Siblings and duplicates: no ELSA record (grep for ELSA, SPPB, ageing); `charls_incident_stroke` (CHARLS, a sister study, another target). External collections: none found.
- Better data: from the curator's Zotero collection (item 58); no search for better data in this run. Later ELSA nurse visits (waves 8 and 9) may add pairs; not checked.
- Papers and pages: the TELFOR paper (XGBoost MAE 0.79 points; 10 to 20 SHAP-selected features MAE 0.82).
- Metric: the paper reports MAE and MSE side by side (Table III) and names the best model by MAE ("an MAE of approximately 0.79 SPPB points"): borderline MET-5, `mae` if read as its choice, else the fallback `rmse`; inputs none.
- Risks for /add-dataset: build the target across waves from the nurse-visit data (check which test times the harmonized file carries; the walk rescoring is the paper's) (`Needs extensive data wrangling`); persons repeat across pairs (group by the ELSA person id); the current SPPB is the strongest input, so measure the persistence baseline (TP-4, TP-2); people who died or dropped out between waves have no label (survivor selection, USE-7); registration to build (EV-4).
- Priority: gap 0 (medical & healthcare, regression and grouped are not thin), use case 0 (no actor named), source + (ELSA documentation and the paper), shape + (7,739 pairs, 95 mixed features, a person grouping), risk - (a label built across waves).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 58: "ML-based Short Physical Performance Battery future score prediction based on ...".
- as published: persons x wave pairs; 7,739 samples (aged 55-85, waves 2->4 and 4->6) x about 100 questionnaire, health and physical-performance variables in the paper; later nurse waves may add more; target: SPPB score (0-12, from timed balance, gait-speed and chair-rise tests at the nurse visit) 4 years later; regression or a low-SPPB threshold; access: registration.
- Why: real measured future outcome (a physical test by a nurse, not self-report) from a large national cohort; mixed tabular features known at the prediction point; the prediction is used in practice for preventive geriatrics
- Adds: an ageing and physical-decline task, a gap among the records; a few thousand rows; persons repeat across wave pairs, so it needs a grouped split by person
