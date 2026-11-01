---
unique_name: medical_appointments_no_show_itajai
name: Medical Appointments No-Show (CER Univali, Itajai, Brazil)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
original_source: Other
year: '2023'
domain: medical & healthcare
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://data.mendeley.com/datasets/wm6w2fvkfj/1
- https://doi.org/10.17632/wm6w2fvkfj.1
- https://doi.org/10.3390/fi14010003
- https://doi.org/10.3390/info13110507
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: 49,593 appointments of a public rehabilitation centre in Itajaí, Brazil, 2016-2022, with a no-show flag, released by the university that runs it; a traceable source for the no-show task, with a post-outcome column and noisy labels to clean.
- Source: Luiz Henrique Salazar (Universidade do Vale do Itajaí), "Medical Appointments No-Show", Mendeley Data, doi 10.17632/wm6w2fvkfj.1, published 2023-02-14, CC BY 4.0: "49,593 medical records transcribed from a spreadsheet" of the Centro Especializado em Reabilitação (CER) that serves the Unified Health System (SUS), with weather data and ICD codes added. As published: one CSV, `medical-appointments-no-show-en.csv` (6.8 MB), 26 columns: specialty, appointment time and date, gender, `no_show` (yes/no), `no_show_reason`, disability, date of birth, entry date into the service, city, ICD, month, year, shift, age, two age flags, companion needed, seven day-level weather columns (header of a preview). No patient id, no booking date.
- Use case: the clinic, when it confirms an appointment, flags likely no-shows for a reminder call or overbooking ("develop a prediction model able to identify whether the patient will attend their scheduled appointment", Salazar et al. 2021, abstract); fit direct. Regime temporal: appointments 2016-2022, the model is used on future appointments; patients repeat but no id ships (SPLIT-13, SPLIT-24).
- Siblings and duplicates: `medical_noshow_appointments` (`TBD -> Yes`; the Kaggle file of about 110k appointments in Vitória, 2016, source unclear; the curator's comment there names this dataset as "a better version of the data with a source"): another clinic and another source, so its own record (PROV-4). No other record links wm6w2fvkfj. External collections: none found.
- Better data: found as better data for `medical_noshow_appointments`, and in the curator's Zotero collection (item 34); no further search this round.
- Papers and pages: Salazar, Leithardt, Parreira, da Rocha Fernandes, Barbosa, Correia, "Application of Machine Learning Techniques to Predict a Patient's No-Show in the Healthcare Sector", Future Internet 14(1):3, 2021 (doi 10.3390/fi14010003; "a real collected dataset with about 5000 samples" from the same clinics, approved by the Univali ethics committee, opinion 4270,234); Salazar et al., "No-Show in Medical Appointments with Machine Learning Techniques: A Systematic Literature Review", Information 13(11):507, 2022. Full texts not reachable (MDPI returned 403); abstracts via Crossref.
- Metric: the 2021 paper reports recall (0.91) and ROC AUC (0.969) side by side on an earlier cut of about 5,000 rows (abstract), no single ranked criterion found, so the fallback `roc_auc` (MET-5, MET-8); inputs none.
- Risks for /add-dataset: `no_show_reason` is written after the outcome (drop, LEAK-10); in a 5,046-row preview the reasons under `no_show = yes` include "consulta desmarcada" (appointment cancelled) and "yes atendeu" (attended), so cancelled and mislabelled rows need a rule (USE-5); the weather columns are the day's observed values, known on the day but not at booking (USE-3: fix the prediction point); about a quarter of the rows lack the patient fields (date of birth, city, ICD), 28% of no-shows against 22% of attendances in the preview (LEAK-13 to check on the full file); a patient key built from date of birth, entry date, gender and city would be a constructed group (SPLIT-24).
- Priority: gap 0 (medical, binary and temporal are not thin), use case + (the paper names the clinic's attendance prediction), source + (a university deposit with an ethics-approved study), shape + (49,593 rows, mixed types, seven years), risk - (a post-outcome column and noisy labels).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `medical_noshow_appointments`; the curator's Zotero collection, item 34: "Medical Appointments No-Show".
- as published: Appointments: 49,593 rows x 26 columns, 2016-2022, one CSV of 6.8 MB (specialty, time, gender, date, no_show, no_show_reason, disability, date of birth, entry date, city, ICD, age, companion and ...; target: no_show (binary); access: open.
- Why: Real appointment records transcribed from the clinic's own spreadsheet, with a named institution, ethics approval (Univali), an earlier study on the same clinics, and a CC BY 4.0 licence. The curator's comment on medical_noshow_appointments already points here. | the same target and use case as ...
- Adds: Compared with medical_noshow_appointments (Kaggle, about 110k appointments in Vitoria in 2016, source unclear): a traceable source and seven years for a temporal split, at about half the rows. It is a different clinic, so it needs its own record (PROV-4), not a version. Risks: no_show_reason is a post-outcome leak ...
