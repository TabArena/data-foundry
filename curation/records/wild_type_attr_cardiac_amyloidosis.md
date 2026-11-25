---
unique_name: wild_type_attr_cardiac_amyloidosis
name: Wild-type transthyretin amyloid cardiomyopathy risk from claims and EHR features (Huda et al. 2021; Arasteh et al. 2024 copy)
checked_by:
- AI (UNVERIFIED)
- Andrej
suggestion: TBD -> Yes
priority: 3
decision_markers:
- Selection Bias
tags:
- AI-Filled (Verify)
- Clinical Study
- 'Samples: Over Time'
- 'Time: Lost'
- 'Target: Varying Delay'
- 'Features: Read Later'
- Many features
original_source: Other
year: '2021'
collection_period: Unknown
domain: medical & healthcare
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.nature.com/articles/s41467-021-22876-9
- https://www.nature.com/articles/s41467-024-45879-8
- https://doi.org/10.1186/s12911-026-03654-3
- https://static-content.springer.com/esm/art%3A10.1038%2Fs41467-021-22876-9/MediaObjects/41467_2021_22876_MOESM4_ESM.zip
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-11-25):** `TBD -> Yes`, priority 3: Huda et al. released the real IQVIA derivation cohort (2,142 heart-failure patients, 1,874 binary ICD-code flags, wild-type ATTR cardiomyopathy against matched non-amyloid HF) with the paper; not synthetic, but the code flags are lifetime presence, not cut at a prediction point, and one flag the source itself calls a leak ships in the file.
- Source: Huda, Castaño, Niyogi, Schumacher, Stewart, Bruno et al., "A machine learning model for identifying patients at risk for wild-type transthyretin amyloid cardiomyopathy", Nat Commun 12:2725 (2021), doi 10.1038/s41467-021-22876-9 (read from Europe PMC, PMC8113237). Data availability: "The IQVIA training and validation datasets have been made available for download (see Source Data). The Optum and Northwestern Medicine Enterprise Data Warehouse datasets used for this study could not be made available publicly". As published (Source Data zip `41467_2021_22876_MOESM4_ESM.zip`, previewed): `training_input (IQVIA derivation dataset).csv`, 2,142 rows x 1,877 columns (`patient_id`, `cohort_type`, 1,874 binary ICD-10 phenotype flags, target `cohort_flag`; 1,071 cases "Wild Type" / 1,071 "Control Group", one row per patient, no missing values, no duplicate feature rows); `ca_validation_group_input (IQVIA validation dataset).csv`, 15,394 rows of `patient_id` and a comma-separated list of raw ICD-10 codes (Cohort 3, the general "cardiac amyloid" label, 7,296 + 7,296 matched in the paper, Table 1); the authors' training and validation notebooks and `icd_map.csv`. Real claims rows: the generated-data question (SEL-16) does not arise. Methods, "Dataset curation": "Two sets of case/control cohorts of patients were created for model training from the IQVIA data"; controls were "selected ... using a propensity score matching algorithm, with age, gender, duration of medical history in the database, and number of healthcare visits as matching parameters".
- Use case: Discussion: "ML models, such as the one that we developed, can be used to calculate the probability of wild-type ATTR-CM in HF patients and elevate the index of suspicion, after which further confirmatory testing can be done". Actor: a health system or cardiologist screening heart-failure patients' coded history to refer them for scintigraphy or biopsy; fit approximate (the derivation set is a 1:1 matched case-control cut, while use meets a prevalence near 0.7% as in the NMEDW cohort, 261 of 39,654; and the flags cover the whole history, not the history up to a referral moment). Collection: patients whose claims ran over years, no date per row (`Samples: Over Time`, `Time: Lost`); the ATTR-CM code arrives after the HF code at a varying delay (`Target: Varying Delay`); the flags were read from the full history at extraction, also after the diagnosis ("Only the presence or absence of the ICD codes (and not the temporal sequence of ICD codes) were included as features", Methods, `Features: Read Later`); type Clinical Study (SPLIT-34 rule 5: patient data without dates, arriving over time). Collection period not stated in the paper text read (Arasteh et al. 2024 say "a dataset spanning 2008-2019"; unverified).
- Split: leaf [L-PLACE.random] (Random · `ForcedIIDFromGrouped`, one place, the transfer untested) because [CLI.meets] the source's use is another health system (validated in Optum and at Northwestern, "the setting in which it would be used clinically"), [PLACE.several] the derivation file holds one source (IQVIA) with no site or region column, [PLACE.units] one row per patient. Open: whether the released IQVIA Cohort 3 file (15,394 patients, raw code lists, the general cardiac-amyloid label) can serve as a held-out cohort of a different label definition, a person's call; the source's own split is an 80:20 random split of the derivation set (`train_test_split(..., test_size=0.2, random_state=42)` in `Model Training.ipynb`).
- Siblings and duplicates: none among `curation/records/` (grep amyloid, transthyretin, Huda, IQVIA). Arasteh et al. 2024 (Nat Commun 15:1603, doi 10.1038/s41467-024-45879-8) used the same derivation file: "our analysis adhered to the original study's internal validation strategy: 80% as the training set and 20% for testing, resulting in 1712 individuals for training and 430 for testing" (Methods, "Patient cohorts"), with "1874 numerical (0 or 1 ...) feature vectors" (Methods, "Cardiac amyloidosis"), i.e. all flags including the two the source dropped as leaks; its Data availability points back to Huda ("available per the original study"). Shaktah et al. 2026 reads `training_input.csv` (its repository holds a 99-row excerpt of it), drops only `patient_id` and `cohort_type` and draws its own random split (`KeepSplit = False`). Both are copies of Huda's file, no new data (PROV-4, PROV-8): /add-dataset starts from the Huda Source Data zip. External collections: Arasteh et al. 2024; Shaktah et al. 2026 (not in our vocabulary).
- Better data: none found (data scout, 2026-11-25: Zenodo, figshare, PhysioNet, Kaggle, Mendeley and the web). Later ML studies of amyloid cardiomyopathy screening (JAMA Cardiol 2026, n=850; GWTG-HF; DATASUS, PLOS ONE 2024) release no rows; Mendeley dx4z7zx639 (São Paulo TTR registry, 755 people, CC BY 4.0) holds ATTR cases only, without heart-failure controls, so it is not the same task.
- Papers and pages: Huda et al. 2021 (RF AUROC 0.93 on the internal 20%; Optum ATTR-CM, IQVIA and Optum cardiac-amyloid cohorts, NMEDW); Arasteh et al. 2024 (ChatGPT ADA RF 0.954, re-implemented RF 0.952); Shaktah et al. 2026 (CatBoost 0.936, LR 0.914, TabPFN 0.922).
- Metric: Huda et al. report sensitivity, specificity, PPV, NPV, accuracy and ROC AUC side by side (Table 2), at no threshold fixed by a decision: several reported, so the fallback `roc_auc` (MET-1, MET-5, MET-6); inputs none.
- Risks for /add-dataset: the source's own leak list, `potential_target_leaks = ['cardiomyopathy_in_diseases_classified_elsewhere','other_forms_of_heart_disease']` (`Model Training.ipynb`; Methods: removed "to ensure no information relevant to the diagnosis of ATTR-CM or cardiac amyloidosis was 'leaked'"), is not applied in the file: measured on the preview, `cardiomyopathy_in_diseases_classified_elsewhere` is 1 in 70.0% of cases against 2.2% of controls, and Arasteh and Shaktah kept it (LEAK-10). Beyond it, every flag is lifetime presence, so codes coded at or after the ATTR-CM work-up (`cardiomyopathy` 72.6% against 29.0%, `cardiomyopathy__unspecified`, HFpEF codes) may be consequences of the diagnosis process rather than antecedents: the prediction point (before referral) cannot be rebuilt from the release (USE-3, LEAK-10); decide whether to keep it as a "coded history" task with a note or drop the cardiomyopathy family. Feature selection on case prevalence ("present in at least 2% of wild-type ATTR-CM patients in the IQVIA medical claims data") used all 1,071 cases including the test rows, a weak transductive selection (LEAK-27/LEAK-30 note). 1:1 propensity matching on visit count and history length sets the prevalence and removes those signals (`Selection Bias`); ICD-coded labels, so undiagnosed cases sit among controls (paper's own limitation). `Many features` (1,874 sparse binaries).
- Priority: gap 0 (medical, binary, not thin), use case + (named actor and decision in the paper), source + (Nat Commun with the released rows and code), shape + (2,142 patients, 1,874 features, wide sparse), risk - (lifetime flags and the unapplied leak list).

Candidate from Shaktah et al. 2026, "Established machine learning matches tabular foundation models in clinical predictions", BMC Med Inform Decis Mak 26:364 (https://doi.org/10.1186/s12911-026-03654-3), one of its twelve binary clinical tasks.

CC (2026-11-25, Andrej): screening review: issue 1 A (drop the source's two leak flags; reconsider while building and reopen on the added dataset); verdict and issue 2 under discussion.

## Review

**Outcome:** not added; screened `TBD -> Yes`, priority 3. Real IQVIA claims rows from Huda et al. 2021 (2,142 heart-failure patients, 1,874 lifetime ICD-code flags, 1:1 matched wild-type ATTR-CM cases and controls); the source's own leak list is not applied in the released file.

**Main points:** Which code flags to drop (issue 1); keep the forced random split or use the released validation file (issue 2).

**Issues for Andrej:**

1. **Which code flags go: the source's two, or the whole cardiomyopathy family?**

   * **Problem:**
     - The released file still holds the two flags Huda's own notebook drops as target leaks; `cardiomyopathy_in_diseases_classified_elsewhere` is 1 in 70.0% of cases and 2.2% of controls[^leak10].
     - Every flag is lifetime presence, so codes written during the amyloid work-up (`cardiomyopathy` 72.6% against 29.0%) cannot be cut at a moment before referral[^use3].
     - The use case runs on undiagnosed heart-failure patients, whose history holds no work-up codes yet.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Drop the source's two leak flags (implemented) | as Huda's notebook | the paper's own task; one-line change | other work-up codes stay and may carry the diagnosis |
     | B | Drop the whole cardiomyopathy family and the heart-failure subtype codes | our list, drawn by /add-dataset from the ICD map; the drop measured against A | closer to a pre-referral history | our own cut; real antecedents (cardiomyopathy coded for other reasons) go too |
     | C | Not add | `No` | no doubt about the prediction point | the paper's real screening task lost |

   * **Recommendation:** B, with the score of A beside it in the review: the screening model meets patients before any work-up, so codes the work-up writes are consequences of the label. **Decision:** A, B or C?

   **Andrej (2026-11-25, ok):** A. When building the dataset, consider whether this choice was right and in any case also reopen this as a discussion point on the added dataset.

   **Resolved (2026-11-25, Andrej):** A: the source's two leak flags (`cardiomyopathy_in_diseases_classified_elsewhere`, `other_forms_of_heart_disease`) go, the other flags stay; /add-dataset measures the score with and without the cardiomyopathy family and reopens the question as an issue in the added dataset's review.

   [^leak10]: **LEAK-10** (Must): a feature holds only what existed at the prediction point and never gives the target away; out: a column recorded after the outcome, a part, a consequence or another encoding of the target.
   [^use3]: **USE-3** (Must): name the prediction point: when the model is used and what is known then. A value that did not exist at that point is a leak.

2. **Keep the random split within the IQVIA cohort?**

   * **Problem:**
     - The use is another health system (validated on Optum and Northwestern, neither released), but the file holds one source with no site column, so the split tree reaches a forced random leaf[^split36].
     - The released validation file (15,394 IQVIA patients) carries a different label (any cardiac amyloidosis) as raw code lists.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Repeated 3-fold cross-validation on the 2,142 patients (implemented) | the forced random leaf | the task as released; varied training sides | transfer to another system untested |
     | B | Train on the derivation set, test on the validation file | a second label mapped to the 1,874 flags | a held-out cohort | a different target (any cardiac amyloidosis); one test split; flags rebuilt by us |

   * **Recommendation:** A: B changes the target, so it tests another task. **Decision:** A or B?

   **Andrej (2026-11-25, discuss):** Wait, could the validation file be an own new dataset for us?

   **Answer (AI, 2026-11-25):** it could replace this record's file, but as a second record it would repeat the same task.

   * **Problem:**
     - The validation file has no label column: Huda's notebook labels a patient a case when the code list holds E85.82 (wild-type ATTR) or E85.4 (organ-limited amyloidosis), so the label is read from the codes that would be the features.
     - 597 of its patients (505 cases, 92 controls) are rows of the training file, with the same labels.
     - It is the same task on more patients: heart-failure patients, a 1:1 matched case-control set, any cardiac amyloidosis instead of the wild-type form only[^a1].
   * **Data:** downloaded from Huda's Source Data on 2026-11-25.

     | File | Patients | Cases | Controls | Features as released |
     |---|---|---|---|---|
     | derivation (this record) | 2,142 | 1,071 wild-type ATTR-CM | 1,071 | 1,874 binary flags |
     | validation | 15,394 | 7,697 any cardiac amyloid code | 7,697 | raw ICD-10 lists, median 108 codes |

   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Keep the derivation file (implemented) | 2,142 patients, Huda's flags | the paper's own model task; the label is the curated wild-type cohort | small; the flags were chosen on all cases |
     | b | A second record from the validation file | its own definition next to this one | 7x the patients | the same task twice; 597 patients in both |
     | c | Build this record from the validation file instead | label from the codes, every E85 code removed, flags built with Huda's ICD map | 7x the patients; our own feature build, so the leak cut is ours | a broader label (any cardiac amyloidosis); the label is a code we must remove cleanly |

   * **Recommendation:** c, with a's score beside it at /add-dataset; b repeats the task. **Decision:** a, b or c?

   **Andrej (2026-11-25, discuss):** How many features would we have for the validation task and how would they differ from the derivation task features?

   **Answer (AI, 2026-11-25):** about as many, nearly all the same; it adds patients, not features.

   * **Problem:**
     - Built as Huda's notebook builds them: each ICD-10 code mapped with the released ICD map to its description, category and sub-chapter, one flag per name, kept when at least 2% of cases have it; the E85 amyloidosis codes that define the label removed first.
     - The leak flag of issue 1 separates the classes there too, and the heart-failure sub-chapter is in every patient, so it carries nothing[^a2].
   * **Data:** validation file, 15,394 patients, 22,222 distinct codes (99.9% in the map).

     | Feature set | Count |
     |---|---|
     | all three levels, amyloidosis codes removed | 23,853 |
     | in at least 2% of the cases (Huda's rule) | 1,742 |
     | derivation flags | 1,874 |
     | derivation flags present in the validation set at all | 1,863 |
     | shared by both 2% sets | 1,628 |
     | new in the validation set (acute and late-stage conditions, e.g. respiratory failure, ischaemic heart disease) | 114 |
     | derivation flags under 2% there | 246 |

     | Flag | Cases | Controls |
     |---|---|---|
     | `cardiomyopathy_in_diseases_classified_elsewhere` | 52.4% | 1.4% |
     | `cardiomyopathy` | 51.9% | 26.5% |
     | `other_forms_of_heart_disease` | 100% | 100% |

   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Keep the derivation file (implemented) | 2,142 patients, Huda's 1,874 flags | the paper's own model task; the curated wild-type label | small |
     | b | A second record from the validation file | its own definition next to this one | 7x the patients | the same task and nearly the same features twice; 597 patients in both |
     | c | Build this record from the validation file instead | 15,394 patients, about 1,742 flags built with Huda's map, E85 codes and the issue 1 leak flags removed | 7x the patients; the feature build is ours, so the leak cut is ours | a broader label (any cardiac amyloidosis) |

   * **Recommendation:** c, unchanged: the two tasks share almost every feature, so the larger file is the better version of the same task. **Decision:** a, b or c?

   [^a2]: **LEAK-10** (Must): a feature holds only what existed at the prediction point and never gives the target away; out: a part, a consequence or another encoding of the target.

   [^a1]: **PROV-6** (Must): different versions or cuts of one underlying dataset are duplicates too when neither adds a distinct task: a swapped target, another slice of the same cohort, added or dropped rows or columns.

   [^split36]: **SPLIT-36** (Should): a definition's split is decided by walking the split decision tree; a forced leaf is for the curator to look at.
