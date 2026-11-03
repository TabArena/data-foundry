---
unique_name: jnu_ctg_fetal_wellbeing
name: 'JNU-CTG: A Large-Scale Continuous Cardiotocography Dataset for Fetal Well-being Assessment'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
decision_markers:
- Time-series (Classification)
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
original_source: Other
year: '2026'
domain: medical & healthcare
required_split:
- Grouped (NON-IID)
problem_type: Binary Classification
source_links:
- https://zenodo.org/records/21800730
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: 20,769 antepartum CTG recordings from 12,606 pregnancies at one Guangzhou hospital (Zenodo 2026, CC BY 4.0) with 103 engineered signal features, demographics, an expert FIGO reading and neonatal outcomes; ten times cardiotocography, but the target has to be chosen, the signal is the primary data, and many delivery-time columns must go.
- Source: Jieyun Bai (Jinan University), Zenodo 10.5281/zenodo.21800730, v1.0.0, 2026-08-05; the record says "Published in Scientific Data, 2026" but links no article, and the README's citation is a placeholder. As published (README in the zip, read by range request): `metadata.csv` with 20,769 rows x 215 columns (identifiers, maternal demographics, labour and delivery, neonatal biometrics, Apgar totals and sub-scores at 1, 5 and 10 minutes, amniotic fluid, placenta, perineum, pregnancy complications, fetal ultrasound, 55 FHR, 23 UC and 25 cross-signal engineered features, 5 encoder features `NetFea_*`, labels `figo_label` and `neonatal_asphyxia`) plus one 30-minute 4 Hz FHR and UC file per recording. `figo_label`: 46.2% normal, 53.8% abnormal, "manually classified ... following the FIGO diagnostic criteria by two senior obstetricians"; neonatal asphyxia: 154 recordings, 91 of 12,606 patients (0.72%).
- Use case: an obstetric team reads an antepartum CTG (README: "typically 1-2 weeks prior to delivery") and decides on further surveillance or delivery; the README frames automated CTG interpretation and suggests "Apgar scores ... and neonatal asphyxia diagnosis as outcome endpoints". Fit direct for the FIGO reading, as in cardiotocography; the asphyxia outcome is the better target but rare. Regime grouped by pregnancy: "Patient-level splitting is essential ... Use `patient_id` with scikit-learn's `GroupKFold`" (README).
- Siblings and duplicates: `cardiotocography` (Yes; UCI SisPorto, 2,126 recordings; carries `Wrong Domain / Source Modality` and `Time-series (Classification)`, whose second marker is carried here), `cardiotocography_duplicate`; no record of JNU-CTG or CTU-UHB (grep ctg, cardiotocograph, intrapartum). External collections: none found.
- Better data: found as better data for `cardiotocography`; another source (PROV-4).
- Papers and pages: the Zenodo record and its README; the Scientific Data article not found (no DOI given); the source's baseline is a 1D CNN on the raw waveforms (`code/baseline_1DCNN_2w.py`).
- Metric: the README advises "Use AUC-ROC and AUC-PR rather than accuracy" for the rare outcomes: two metrics, no unique one (MET-5), so the fallback `roc_auc` (binary); `patient_id` is the group, never a feature (LEAK-33).
- Risks for /add-dataset: choose one target (`figo_label` is the experts' reading of the same trace the features summarise; `neonatal_asphyxia` is the outcome, about 18 positive pregnancies per test fold with 5 folds, TP-5 to check); drop everything recorded at or after delivery (labour, delivery mode, Apgar, birth biometrics, placenta, perineum; LEAK-10) and check how the `NetFea_*` encoder was trained (LEAK-27 if with labels on all rows); SEL-12 and SEL-13: the signal ships and the source's tool is a CNN on it, so whether the engineered features keep tabular models competitive is the add-stage question (cardiotocography precedent); zeros in the signals mean missing.
- Priority: gap 0 (medical, binary and grouped are well covered), use case 0 (no decision named; the outcome fit is approximate), source + (hospital cohort with ethics approval and a codebook), shape + (20,769 rows, about 100 mixed features, grouped), risk - (target to choose, delivery-time columns, encoder features).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `cardiotocography`.
- as published: 20,769 continuous 30-minute CTG recordings (4 Hz) from 12,606 pregnancies in routine antenatal monitoring; ships 'more than 100 pre-computed features', maternal-fetal demographics and pregnancy ...; target: Expert-annotated CTG morphological patterns, and neonatal outcomes (1-, 5-, 10-minute Apgar, neonatal asphyxia diagnosis); which one is the target to be ...; access: open.
- Why: Same task as cardiotocography (fetal state from CTG-derived features: baseline, variability, accelerations, decelerations) with tabular pre-computed features of the same kind, plus an outcome label
- Adds: About 10x the recordings (20,769 vs 2,126), recent (2026 release vs 1990s SisPorto), a pregnancy id for a grouped split (several recordings per pregnancy, which the UCI set lacks), neonatal outcomes; caveat: no peer-reviewed paper linked yet, and the curated features include deep-learning representations that would ...
