---
unique_name: plco_lung_cancer_incidence
name: PLCO Cancer Screening Trial, Lung dataset (NCI CDAS)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 4
tags:
- AI-Filled (Verify)
original_source: GOV Website
domain: medical & healthcare
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://cdas.cancer.gov/plco/
- https://cdas.cancer.gov/datasets/plco/21/
- https://doi.org/10.1056/NEJMoa1211776
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 4: about 155,000 PLCO trial participants (enrolled 1993-2001) with baseline questionnaire answers and confirmed lung cancer with its diagnosis day in one person file, the cohort behind the PLCOm2012 model for choosing who gets lung screening; access by an NCI project proposal.
- Source: the Prostate, Lung, Colorectal and Ovarian (PLCO) Cancer Screening Trial of the US National Cancer Institute, through the Cancer Data Access System (cdas.cancer.gov/plco/: "Approximately 155,000 participants were enrolled between November 1993 and July 2001"; cancers to 2009, deaths to 2022). As published (cdas.cancer.gov/datasets/plco/21/): the Lung datasets, "nearly all the PLCO study data available for lung cancer screening, incidence, and mortality analyses": Lung (one row per participant, about 155,000), Lung Screening (about 236,000, one per screening year), Screening Abnormalities (138,000), Diagnostic Procedures (63,000), Medical Complications (1,400), Treatments (6,000), X-ray image linkage (89,000); dictionaries tagged 2024-10-11. The person-file dictionary (lung_prsn, 2024-10-15, read) holds `center` and the arm, the baseline questionnaire (demographics, smoking with `pack_years`, family history, body type, NSAIDs, diseases, female and male items, screening history), `lung_cancer` ("confirmed primary invasive lung cancer diagnosed during the trial"), `lung_cancer_diagdays`, `entrydays_bq`, the flag `lung_eligible_bq`, and later sections (screening, work-up, cancer characteristics, treatments, mortality).
- Use case: a doctor or screening programme decides whether to refer a person to low-dose CT screening from questionnaire risk factors: Tammemägi et al., "Selection Criteria for Lung-Cancer Screening", NEJM 2013 (doi 10.1056/NEJMoa1211776; abstract read): risk "was the probability of a diagnosis of lung cancer during the 6-year study period", developed and validated on "the 80,375 persons in the PLCO control and intervention groups who had ever smoked"; fit direct; regime IID by participant (one baseline per person), or grouped by `center` (10 centres) if the curator wants transfer across sites.
- Siblings and duplicates: `sleuth_case2002` (`TBD -> 2nd Tier`, `Outdated`: 147 people of a 1985 case-control study), `lung_cancer_dataset` (`No`, generated, no source), `plco_ovarian_cancer_screening` (the same trial, another file and cancer: a distinct task, PROV-7); no duplicate. External collections: none found.
- Better data: found as better data for `lung_cancer_dataset` and `sleuth_case2002` (the data-scouting run of 2026-10-30/31); no further search this round.
- Papers and pages: the trial design, Prorok et al., Controlled Clinical Trials 21(6 Suppl):273S-309S, 2000 (not opened); Tammemägi et al. 2013 (PLCOm2012, AUC 0.803 in development and 0.797 in validation); the CDAS pages and the lung_prsn dictionary.
- Metric: Tammemägi et al. assess "Discrimination (area under the receiver-operating-characteristic curve [AUC]) and calibration" and compare sensitivity and PPV at a number screened matched to the NLST criteria, which fixes no threshold of its own (MET-6, MET-7): `roc_auc` (MET-5, MET-8); inputs none, but a 6-year label needs a rule for people who die or leave before 6 years (USE-3).
- Risks for /add-dataset: build the label from `lung_cancer`, `lung_cancer_diagdays` and `entrydays_bq` with a horizon and censoring; keep only the baseline questionnaire and entry columns (the person file also holds screening, work-up, staging, treatment and death fields, LEAK-10); restrict to `lung_eligible_bq` (and to ever-smokers as PLCOm2012 did, a choice); the screening arm's chest X-rays change when cancers are found (the arm as a feature, or one arm); access through a CDAS project proposal and a Data Transfer and Use Agreement, terms not read (a practical point, EV-4).
- Priority: gap 0 (medical, binary and IID are not thin), use case + (PLCOm2012 for screening selection, from this cohort), source + (NCI, dictionaries, the trial papers), shape + (about 155,000 people, mixed questionnaire features, a centre column).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `lung_cancer_dataset`, `sleuth_case2002`.
- as published: About 155,000 participants aged 55-74, enrolled November 1993 to July 2001 at 10 US centres; Lung file one row per participant (~155,000 rows, CDAS page), plus screening (~236,000 rows) and ...; target: Lung cancer diagnosed during follow-up (e.g. within 6 years of the baseline questionnaire, as in PLCOm2012); access: request (CDAS project proposal reviewed by NCI, then a Data Transfer and Use Agreement; check whether the terms allow commercial use).
- Why: The same target as sleuth_case2002 (lung cancer vs none) from personal risk-factor answers of the same kind (smoking, age, sex, socio-economic status), but in a prospective cohort instead of 49 cases and 98 controls; the use case is current (screening eligibility). | lung_cancer_dataset (Kaggle akashnath29, about ...
- Adds: About 1,000 times more people, prospective cohort (no case-control sampling), 1993-2009 instead of 1985, a published reference model to compare against. No bird-keeping variable: the record's specific risk factor is lost. | real, traceable data from a named trial instead of an untraceable Kaggle upload; about 50 ...
