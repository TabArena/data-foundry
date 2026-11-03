---
unique_name: nhanes_iii_gallstones
name: NHANES III (1988-1994) gallbladder ultrasonography, with the examination's bioelectrical impedance and the laboratory file
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
original_source: GOV Website
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://wwwn.cdc.gov/nchs/nhanes/nhanes3/datafiles.aspx
- https://wwwn.cdc.gov/Nchs/data/nhanes3/1a/exam-acc.pdf
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: gallbladder ultrasound of about 14,000 adults in NHANES III (1988-1994), with bioimpedance and lab values of the kind `gallstone_disease` uses; a national sample with about 7% gallstones against half in the clinic file, but 30 years old and a task we construct.
- Source: CDC/NCHS NHANES III Examination Data File (exam.dat, codebook exam-acc.pdf): final adjudicated primary finding GUPFDX1R, "If gallstones were present (codes 3-5), it was indicated in the final, primary diagnosis"; counts 11,666 normal, 305 one gallstone, 758 multiple, 86 gallbladder filled, 860 and 10 cholecystectomy, plus small "no conclusion" and abnormal-wall codes; radiologist and technician readings, disagreements adjudicated by a senior radiologist. The same file has BIA resistance and reactance (PEP12A1, PEP12B1, ages 12 and over) and body measures; the lab file has lipids, glucose, liver enzymes and CRP (the scout's note, not opened). Ruhl and Everhart 2011 (Gastroenterology 140:508-516, PMC3060665): "14,228 participants aged 20-74", "Gallstone disease was defined as ultrasound-documented gallstones or evidence of a cholecystectomy", gallstones 7.1% and cholecystectomy 5.3% (weighted).
- Use case: a clinician at a check-up decides from body composition and routine blood tests whether to order an abdominal ultrasound for suspected gallstones, the framing of Esen et al. 2024 for `gallstone_disease`; fit approximate: most gallstones a survey finds are silent, and a scan is usually ordered on symptoms; regime IID (one survey, one row per adult).
- Siblings and duplicates: `gallstone_disease` (`Yes`, 319 patients of one Turkish clinic, Selection Bias); `nhanes_cvd_mortality` (the same NHANES III exam, another task, PROV-7). The NHANES III hepatic steatosis re-read of the same ultrasound videos (HGUHS, 14,797 records, published 2011, https://wwwn.cdc.gov/nchs/data/nhanes3/34a/HGUHS.htm) is not this task's data but a possible fatty-liver task, a sibling of `nhanes_liver_elastography_fibrosis`; moved from the source links to here (PROV-12). External collections: none known (not searched: the run's web search budget was used up).
- Better data: found as better data for `gallstone_disease`; no further search this round.
- Papers and pages: Everhart et al. 1999, Gastroenterology 117:632-639 (the prevalence paper, per the scout, not opened); Ruhl and Everhart 2011 (https://pmc.ncbi.nlm.nih.gov/articles/PMC3060665; a mortality association by Cox models, not a prediction task; a paper that used the data, moved from the source links to here, PROV-12).
- Metric: none found (the papers estimate prevalence and hazard ratios); `gallstone_disease` declared the fallback `roc_auc`, so the same here (MET-5, MET-8); inputs none.
- Risks for /add-dataset: the label for a cholecystectomy (drop the rows, or count them as gallstone disease as Ruhl and Everhart do; USE-5); NHANES III has raw BIA resistance and reactance, not the body-composition outputs of the clinic's device; the lab file join and fasting subsamples; data from 1988-1994 (`Outdated` to weigh); survey weights not used.
- Priority: gap 0, use case 0 (the decision is the sibling's; no source names it for this data), source + (NCHS codebook, two papers), shape + (about 14,000 adults, mixed features), risk - (old data, a constructed label with a cholecystectomy choice).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `gallstone_disease`.
- as published: One row per adult. 14,228 adults aged 20-74 had the gallbladder ultrasound (Ruhl & Everhart 2011, PMC3060665, Methods: 'The analysis sample, therefore, consisted of 14,228 participants'). Final ...; target: gallstones on ultrasound (GUPFDX1R codes 3-5). People with a cholecystectomy can be dropped, or counted as gallstone disease as Everhart's definition does.; access: open.
- Why: Same target as gallstone_disease (gallstones confirmed by ultrasound) and features of the same kind: bioimpedance body composition plus lipid, glucose, liver-enzyme and CRP labs, which is what Esen et al. 2024 used.
- Adds: About 13,000 adults against 319. A national probability sample instead of one Turkish clinic with unstated patient selection, which addresses the record's Selection Bias marker: gallstone prevalence is about 7% here against 50% in the UCI file. Radiologist-confirmed ultrasound reads. Older, though (1988-1994).
