---
unique_name: seer_hepatocellular_carcinoma_lung_metastasis
name: 'SEER hepatocellular carcinoma (C22): lung metastasis at diagnosis'
checked_by:
- Andrej
suggestion: 'Yes'
priority: 2
tags:
- Dated Event Log
- 'Samples: Over Time'
- 'Time: Dated'
- 'Entities: Recur'
- 'Features: Revised Later'
original_source: GOV Website
collection_period: 2000-2021
domain: medical & healthcare
problem_type: Binary Classification
source_links:
- https://seer.cancer.gov/
- https://doi.org/10.1186/s12911-026-03654-3
- https://seer.cancer.gov/data/access.html
- https://seer.cancer.gov/data-software/documentation/seerstat/nov2025/seerstat-variable-dictionary-nov2025.pdf
- https://github.com/KatherLab/tabpfnbenchmark
- https://arxiv.org/abs/2501.11720
type_adapter_id: curation-record-v1
---

## Comments

**AI summary:**

**Screening (AI, 2026-11-25):** `TBD -> 2nd Tier`, priority 2: lung metastasis at diagnosis of liver cancer in the NCI SEER registries (2010+, tens of thousands of cases), a real staging task from features known at diagnosis, but the target is read off the same staging work-up whose other columns (M, stage group, summary stage) encode it, the treatment columns follow it, and the source code labels unknown and pre-2010 cases as negative. Not "distant metastasis": both papers predict lung metastasis.
- Source: National Cancer Institute, SEER Program, "Incidence - SEER Research Data, 17 Registries, Nov 2023 Sub (2000-2021)" (Shaktah et al. 2026, Methods, "Datasets": "HCC metastasis; ... Primary Site C22"). SEER Research Data is per person through SEER*Stat after acknowledging the SEER Research Data Use Agreement ("Each person who will access the data must submit a separate request", seer.cancer.gov/data/access.html). The agreement (November 2025 submission) says in clause 10 "Authorized User will not release, nor permit others to release, the Data to any other person", and its clause 19 ("Permitted Use of AI/ML Tools") allows approved users to "develop or validate analytical and generative AI models using the Data" within an approved request, but "may not share the model, including model parameters, except with collaborators who are also Approved Users" and may not use the data with any tool "that transmits data to an external provider": a release-checklist item, no criterion (EV-4), but no row of it can ship and every user must extract it themselves. As published: case listings, one row per tumour (Patient ID, Sequence number), with year of diagnosis, age, sex, race, marital status, site and histology, grade, T/N/M and stage (AJCC 6th 2004-2015, 7th 2010-2015, EOD 2018+), "SEER Combined Mets at DX-bone/brain/liver/lung (2010+)", AFP pretreatment (2010+), first-course surgery, radiation and chemotherapy, survival months, vital status and cause of death (SEER*Stat variable dictionary, Nov 2025). Rows not counted (needs SEER*Stat). The target in Shaktah's code (github.com/KatherLab/tabpfnbenchmark, `SEER_HCC/TabPFN_SEER-HCC_CPU.py`): `LungMets = np.where(df2['SEER Combined Mets at DX-lung (2010+)'] == 'Yes', 1, 0)`, so "No", "Unknown" and the blank pre-2010 values are all 0; Supplemental List 1 drops every stage and mets column, "Histologic Type ICD-O-3", "Time from diagnosis to treatment in days recode" and "Year of diagnosis", but not survival months, vital status or cause of death (the droplist has none of them).
- Use case: the paper it reproduces, Kim, Nahass, Dai, Tulabandhula, "Prediction of lung metastasis from hepatocellular carcinoma using the SEER database", arXiv 2501.11720 (2025), read from its HTML: cohort "HCC patients diagnosed from 2010 - 2021", "age between 20 to 84", one primary, "Known metastasis status to the bone, brain, or lung" (Sec. 2.1); features include surgery, "surgery not recommended", follow-up duration and follow-up year; "in a clinical setting, recall, or the ability to detect true positives, is the most salient" (Sec. 4); it may serve "as a low bandpass filter screening tool" but is "unsuitable for wide-spread clinical deployment". Actor: a hepatologist or oncologist at diagnosis deciding on chest imaging and the treatment intent; fit approximate (staging guidelines already image the chest, and the features from the same work-up arrive with the label). Collection: samples over time, dated by year of diagnosis (month only in Research Plus); the label exists with the features (staging at diagnosis); a patient can hold several tumours; each submission resubmits all cases with recodes applied back; type Dated Event Log (SPLIT-34 rule 3: the rows record the year of diagnosis).
- Split: leaf [L-ORDER.windows] (Temporal · windows on the time key) because [LOG.meets] the model meets later patients, [ORDER.order] the year of diagnosis orders them, [ORDER.windows] 2010-2023 holds three or more yearly windows of thousands of cases, [ORDER.small] no (a large table); no gap (the label arrives at diagnosis). Open: the window length and refit cadence (one diagnosis year proposed, for sign-off, SPLIT-12); rows before 2010 have no lung-mets value and go.
- Siblings and duplicates: `seer_breast_cancer_5y_survival` (`TBD -> Yes`, 3: the same registry, five-year breast-cancer-specific death), `seer_breast_cancer_survival` (`TBD -> 2nd Tier`, 2: a 4,024-row DataPort cut of it, a PROV-6 version of the former), `seer_primary_site_from_metastases` (`TBD -> Yes`, 3: another task on the same registry, PROV-7), `fosp_cancer_registry_survival` (`TBD -> Yes`, 2: São Paulo registry, survival by site, which left "one dataset per cancer site or all sites with the topography as a feature" open). The siblings' precedent is one record per task on SEER (PROV-7: distinct cohorts and targets), not one SEER record; this one is the only metastasis-at-diagnosis task on SEER (PROV-7), and `seer_primary_site_from_metastases` uses the same mets fields as features for another target. External collections: Shaktah et al. 2026 benchmark (not in our vocabulary).
- Better data: none from another source (data scout, 2026-11-25: no public row-level registry beyond SEER; NCDB and the English, Taiwanese and NPCR survival files are restricted). Newer versions of this source (PROV-6): SEER Research Data, 17 Registries, Nov 2025 submission (diagnoses 2000-2023, released April 2026); the 21-registry Limited-Field file is wider (about 1.7x the tumours) but drops every mets-at-diagnosis field, so it cannot carry this target.
- Papers and pages: Shaktah et al., BMC Med Inform Decis Mak 26:364 (2026), doi 10.1186/s12911-026-03654-3: AUROC LightGBM 0.826, LR 0.764, TabPFN 0.831 (Supplementary Table 2), 70/30 random split, "any datasets with more than 100,000 samples were randomly sampled down to 100,000" (Methods, "Model training"); Kim et al. 2025 (AUROC 0.82, precision 0.14-0.17); SEER*Stat variable dictionary (Nov 2025).
- Metric: Kim et al. report accuracy, precision, recall, F1 and AUROC and name recall "the most salient" without fixing a threshold; Shaktah AUROC with Youden-threshold balanced accuracy and F1. No threshold fixed, so the fallback `roc_auc` (MET-1, MET-6, MET-8); inputs none.
- Risks for /add-dataset: the label as coded by Shaktah treats "Unknown" and pre-2010 blanks as negative: build it from 2010+ with "Unknown" dropped or kept as its own state (USE-5); AJCC M and stage group (6th and 7th editions, which Supplemental List 1 does not name), EOD 2018 M and stage, summary stages, "CS mets at dx", the other mets-at-DX sites and "Mets at DX-Other/Distant LN" encode M1 and go (LEAK); first-course surgery, "Reason no cancer-directed surgery", radiation, chemotherapy and time to treatment are decided after staging, by the metastasis, and go unless the prediction point is set after treatment planning (USE-3, LEAK); survival months, vital status and cause of death are post-outcome and go (Kim's "follow up duration" ranks among its top features); Primary Site C22 also holds intrahepatic cholangiocarcinoma and hepatoblastoma: restrict to HCC histology (8170-8175) and drop histology then, or keep it as a feature, to decide; T and N come from the same imaging (a staging shortcut, to probe, TP-4); one tumour per patient. Release: the Research 17-registry Nov 2025 submission (2000-2023) is the newest with these fields; the 21-registry Limited-Field database has no mets-at-DX fields (variable dictionary: "SEER Combined Mets at DX-lung (2010+) Yes No No Yes", Limited-Field "No"), so it cannot carry this target. The agreement bars shipping rows (above).
- Priority: gap 0 (medical, binary and temporal not thin), use case 0 (approximate; "identifying high-risk patients", no decision named), source + (NCI SEER, variable dictionary, a paper), shape + (thousands of cases per year, mixed types), risk - (staging and treatment columns encode the target; label coding).

Candidate from Shaktah et al. 2026, "Established machine learning matches tabular foundation models in clinical predictions", BMC Med Inform Decis Mak 26:364 (https://doi.org/10.1186/s12911-026-03654-3), one of its twelve binary clinical tasks.

CC (2026-11-25, Andrej): accepted for adding in the screening review (issues 1 A (HCC from 2010, Unknown dropped; revisit on the added dataset) and 2 A (at diagnosis)).

## Review

**Outcome:** not added; screened `TBD -> 2nd Tier`, priority 2. Lung metastasis at diagnosis of liver cancer in SEER (2010+); the target comes from the same staging work-up whose other columns encode it, and Shaktah's code labels unknown and pre-2010 cases as negative.

**Main points:** Cohort and label coding (issue 1); which staging and treatment columns stay (issue 2).

**Issues for Andrej:**

1. **Which cohort and label coding?**

   * **Problem:**
     - Shaktah's code sets the label to 1 only for "Yes", so "Unknown" and the blank pre-2010 rows count as no lung metastasis[^leak25].
     - Primary Site C22 also holds intrahepatic cholangiocarcinoma and hepatoblastoma; the source paper (Kim and colleagues) restricts to HCC, 2010-2021, ages 20-84, known metastasis status[^use5].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Kim et al.'s cohort (implemented) | HCC histology, diagnoses from 2010, "Unknown" dropped | the source task; a clean label | fewer rows |
     | B | Shaktah's extract | all C22, 2000 on, "Unknown" and blank as No | the benchmark paper's task | mixes "no metastasis" with "not recorded"; mixes three cancers |

   * **Recommendation:** A. **Decision:** A or B?

   **Andrej (2026-11-25, ok):** A, but when the dataset is added we can revisit this question in the dataset's review.

   **Resolved (2026-11-25, Andrej):** A: HCC histology, diagnoses from 2010, "Unknown" dropped. /add-dataset reopens the question as an issue in the added dataset's review, with the built data in hand.

   [^leak25]: **LEAK-25** (Must): "No event" mixed with "not recorded" is a censoring bias: retire unless the recording process can be recovered; recovered includes unrecorded rows located by a rule that does not read the label, and dropped.
   [^use5]: **USE-5** (Must): predict what the actor would act on, at the resolution they act on it. Check how the source built its label before accepting it.
   [^source]: Source task before our own: the source's own task and split are tested first and preferred when valid.

2. **Which staging and treatment columns stay?**

   * **Problem:**
     - M, stage group, summary stages and the other metastasis-site columns encode the label; Shaktah drops them but keeps survival months, vital status and cause of death[^leak10].
     - Surgery, radiation and chemotherapy are chosen after staging, by the metastasis; T and N come from the same imaging[^use3].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | At diagnosis before treatment (implemented) | drop M, stages, other sites, treatment, survival and cause of death; keep T, N, size, AFP, demographics | the hepatologist's moment of ordering chest imaging | T and N may still act as a staging shortcut (probed at /add-dataset) |
     | B | Also drop T and N | demographics, AFP, histology, size only | no staging shortcut | drops information the clinician has at diagnosis |
     | C | Kim et al.'s features | treatment and follow-up kept | the source's feature set | treatment follows the label; follow-up is after it |

   * **Recommendation:** A, with the T and N shortcut probed when the dataset is built. **Decision:** A, B or C?

   **Andrej (2026-11-25, ok):** As implemented (A).

   **Resolved (2026-11-25, Andrej):** A: at diagnosis before treatment; M, stages, other metastasis sites, treatment, survival and cause of death go; T, N, size, AFP and demographics stay, with the T and N shortcut probed at /add-dataset.

   [^leak10]: **LEAK-10** (Must): a feature holds only what existed at the prediction point and never gives the target away; out: a column recorded after the outcome, a part, a consequence or another encoding of the target.
   [^use3]: **USE-3** (Must): name the prediction point: when the model is used and what is known then. A value that did not exist at that point is a leak.
