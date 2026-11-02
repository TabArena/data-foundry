---
unique_name: commpass_myeloma_survival
name: 'MMRF CoMMpass: survival of newly diagnosed multiple myeloma from baseline stage and labs'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
original_source: Other
domain: medical & healthcare
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://portal.gdc.cancer.gov/projects/MMRF-COMMPASS
- https://research.themmrf.org
- https://registry.opendata.aws/mmrf-commpass/
- https://arxiv.org/abs/2603.20341
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: the open clinical tier of the MMRF CoMMpass study on the GDC (995 newly diagnosed myeloma patients, 191 deaths) as a prognosis task from stage and baseline labs; a documented cohort, but the target has to be built from censored follow-up and the labs picked from follow-up tables.
- Source: the Multiple Myeloma Research Foundation's CoMMpass study (dbGaP phs000748), released through the NCI Genomic Data Commons as project MMRF-COMMPASS and in full through the MMRF Researcher Gateway (registration). As published (GDC API, 2026-10-31): 995 cases, vital status alive 804 and dead 191, ISS stage I 348, II 353, III 266, unknown 28; the data categories are genomic (variants for 961 cases, copy number, structural variants, transcriptome for 787); the clinical tables (demographic, diagnoses, follow-ups with lab values) and a median follow-up of 778 days (maximum 1,984) are the run's notes, not verified here.
- Use case: at diagnosis, a haematologist stratifies a patient's risk (ISS, R-ISS) to choose treatment intensity and follow-up; the record's paper (Rachidi, Bozorgpanah, Fey and Jung, arXiv 2603.20341) predicts five-year survival of 812 Helsinki patients, data closed; fit approximate (the target, death within 2 years, is ours, and CoMMpass is a study cohort). Regime IID, one row per patient; enrolment dates are not in the open tier as far as checked.
- Siblings and duplicates: no myeloma record (grep by myeloma, CoMMpass, MMRF). External collections: none found on the pages read.
- Better data: from the curator's Zotero collection (item 150); no further search this round.
- Papers and pages: the GDC project and its API; Rachidi et al. 2026 (arXiv 2603.20341, abstract: five-year survival, accuracy up to 0.721 on Helsinki data); the CoMMpass design papers not read.
- Metric: none from the data's source; the arXiv paper reports accuracy only, on other data; the fallback `roc_auc` (MET-1, MET-5, MET-6, MET-8); inputs none.
- Risks for /add-dataset: build the target with censoring: patients alive with less follow-up than the horizon have no label and leave (USE-7), which shrinks the 995 by a share to count; pick baseline labs from the follow-up tables at diagnosis only (USE-3, LEAK-10), treatment fields are after baseline; the paper's five-year horizon needs the Gateway's longer follow-up; genomic features would make a wide omics task (a choice to state).
- Priority: gap 0 (medical, binary and IID are covered), use case 0 (the target is ours), source + (MMRF and the NCI GDC), shape 0 (995 patients before censoring), risk - (a censored target to build, labs to join from follow-ups).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 150: "Interpretable Multiple Myeloma Prognosis with Observational Medical Outcomes Partnership ...".
- as published: GDC open tier: 995 patients with ISS stage (I 348, II 353, III 266), age, sex, race, vital status (191 deaths), follow-up (median 778 days, max 1,984) and repeated labs incl. albumin, B2M, LDH, ...; target: Death within 2 years of diagnosis from the GDC cut (or overall survival); 5-year death as in the paper needs the Gateway releases; access: open (GDC clinical) / registration (MMRF Researcher Gateway).
- Why: A public instance of the paper's task (its Helsinki data is closed) with nearly the same lab panel, from a documented prospective study.
- Adds: Myeloma prognosis, no record. Caveats: the open GDC follow-up is short; baseline labs must be picked from follow_ups at diagnosis; the Gateway needs registration and 30 days' notice before publication; small (about 1,000).
