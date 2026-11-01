---
unique_name: debernardi_urinary_pancreatic_cancer
name: A combination of urinary biomarker panel and PancRISK score for earlier detection of pancreatic cancer (Debernardi et al. 2020, S1 Data)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
decision_markers:
- Selection Bias
tags:
- AI-Filled (Verify)
original_source: Other
year: '2020'
domain: medical & healthcare
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.1371/journal.pmed.1003489
- https://www.kaggle.com/datasets/johnjdavisiv/urinary-biomarkers-for-pancreatic-cancer
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: a urine-biomarker test for pancreatic cancer in 590 patients from six centres, with a triage use the paper names; small, case-control, and the centre gives the class away.
- Source: Debernardi et al., "A combination of urinary biomarker panel and PancRISK score for earlier detection of pancreatic cancer: A case-control study", PLOS Medicine 17(12):e1003489 (2020-12-10, CC BY 4.0); the data is the supplement S1 Table, "Sample details and ELISA results for 590 samples" ("All relevant data are within the manuscript and its Supporting Information files"). As published: 590 urine samples, 183 controls, 208 benign hepatobiliary disease (119 chronic pancreatitis), 199 PDAC (102 stage I-II, 97 stage III-IV); urinary creatinine, LYVE1, REG1B, TFF1, age, sex, plasma CA19-9 (350 rows) and REG1A (306 rows). The Kaggle copy (johnjdavisiv, 2020-12-10, 590 x 14) says "I have not changed any of the data from the paper, other than renaming the columns".
- Use case: PancRISK is "a clinically applicable risk stratification tool with a binary output for risk of developing PDAC" (Conclusions), in two versions, for people with a familial predisposition (sensitivity fixed at 0.85) and for symptomatic patients (specificity fixed at 0.80): a clinician triages a person at risk with a urine test before imaging; fit approximate, since the samples are a retrospective biobank case-control set ("retrospectively collected urine and plasma samples", Methods), not a triaged population. Regime IID (one sample per patient).
- Siblings and duplicates: `pancreatic_cancer_mouse_detection` (`Yes`, 73 mice, serum spectra) is the record this was found for, another population and assay (PROV-7); `cancerseek_blood_cancer_detection` is a multi-cancer blood test. No other record of this data (grep: debernardi, LYVE1, PancRISK, urinary biomarkers). External collections: none found.
- Better data: found as better data for `pancreatic_cancer_mouse_detection`; no further search this round.
- Papers and pages: Debernardi et al. 2020 (PLOS Medicine) and its S1 Table; the Kaggle copy.
- Metric: the paper's discrimination measure is the ROC AUC with DeLong intervals, for two binary comparisons (controls against PDAC, benign against PDAC), plus sensitivity or specificity at the fixed operating points above; no single pooled task. `roc_auc`, also the fallback (MET-5, MET-8); the fixed points belong to the paper's two comparisons, not to a pooled target (MET-2, MET-6); inputs none.
- Risks for /add-dataset: the target framing (PDAC against controls and benign together, one of the paper's two comparisons, or the three-class `diagnosis` of the Kaggle copy); `stage` and `benign_sample_diagnosis` exist only after diagnosis and go (LEAK); `sample_origin` gives the class away: all 183 controls are from BPTB (Barts), UCL holds only benign cases (20), Liverpool 93 PDAC and 39 benign (preview of the Kaggle copy), so the centre and `patient_cohort` go and the case-control design stays a `Selection Bias` (LEAK-13 to check on the biomarkers); CA19-9 and REG1A are missing by design; age and sex differ between groups (Results).
- Priority: gap 0 (medical & healthcare, binary, IID not thin), use case + (the paper names the tool and the two populations), source + (peer-reviewed paper with its data), shape 0 (590 patients, about 7 inputs), risk - (case-control from biobanks, centre tied to the class): 2.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `pancreatic_cancer_mouse_detection`.
- as published: 590 urine samples, one per patient: 183 healthy controls, 208 benign hepatobiliary disease (119 chronic pancreatitis), 199 PDAC (102 stage I-II, 97 stage III-IV); features urinary creatinine, LYVE1, ...; target: Pancreatic ductal adenocarcinoma vs not (the paper also scores control vs PDAC and benign vs PDAC); access: open (CC BY 4.0, PLOS supporting information; Kaggle re-upload unchanged per its uploader).
- Why: The same target as the mouse study (pancreatic cancer present or not) and the same aim (early detection from a body-fluid protein test), now in patients rather than a mouse model; protein levels in a fluid sample, the same kind of feature as the serum spectra.
- Adds: 590 humans instead of 73 mice, a clinical use case, an explicit benign-disease group, and none of the open batch question of the NCI-FDA spectra. Case-control and only about 7 features, so Selection Bias likely and the AUC is already high (0.93 in the paper).
